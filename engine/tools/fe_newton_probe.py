# fe_liquid.volume_newton 미수렴 표지가 값을 틀리게 하는지 재는 계측 도구 (prereg-fe-liquid-newton e1bbe64c)
"""Measure whether `fe_liquid.volume_newton`'s UNCONVERGED flag means a wrong value or a strict flag.

    python3 engine/tools/fe_newton_probe.py earth venus pandora

Per body, three solves on the body file as declared, each from an empty `fe_liquid._CACHE`:
  base   — the engine untouched (no instrumentation);
  probe  — `volume_at` replaced by an instrumented copy of the same code (must return bit-identical values: P-0);
  tight  — as probe, but every call whose Newton failed is polished to |P(v) − p| < 1e-3 Pa
           (Newton from the returned v, no window, 40 steps; if the bracket was false, bisection on [0.05, 3]·v0 first;
           if Newton still does not reach 1e-3 Pa, bisection on [0.05, 3]·v0 until the midpoint stops moving).
Prints the call census, the (P, T) range of failed calls, and the verdict of prereg §3. Changes no engine file.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent
sys.path.insert(0, str(ENGINE))

import convergence  # noqa: E402
import fe_liquid  # noqa: E402
import registry  # noqa: E402
import run  # noqa: E402

ORIGINAL = fe_liquid.volume_at
TIGHT_PA = 1e-3
T_C_LIMIT_K = 0.22   # prereg §3 ①: 1/100 of prereg-structure-coupling addendum 11's 22 K
T_C_KEYS = ("core_temperature", "t_cmb", "cmb_temperature", "t_c")


def _instrumented(log: list, tight: bool):
    """Same code as fe_liquid.volume_at, recording each call; `tight` polishes failed calls."""
    P = fe_liquid.pressure

    def volume_at(p, t, col=fe_liquid.LIQUID):
        rec = {"p": p, "t": t, "col": col.name}
        v = col.v0 * 0.9
        out = None
        n = 0
        exit_ = "budget"
        for n in range(1, 41):
            f = P(v, t, col) - p
            if abs(f) < 1.0:
                convergence.note("fe_liquid.volume_newton", True)
                out, exit_ = v, "f<1Pa"
                break
            h = v * 1e-6
            dfdv = (P(v + h, t, col) - P(v - h, t, col)) / (2.0 * h)
            if dfdv == 0.0:
                exit_ = "dfdv0"
                break
            step = f / dfdv
            v_new = v - step
            if not (0.2 * col.v0 < v_new < 1.5 * col.v0):
                exit_ = "window"
                break
            if abs(step) < v * 1e-12:
                convergence.note("fe_liquid.volume_newton", True)
                out, exit_ = v_new, "step"
                break
            v = v_new
        rec.update(n_iter=n, exit=exit_)
        if out is not None:
            log.append(rec | {"ok": True})
            return out
        rec["f_newton"] = abs(P(v, t, col) - p)
        convergence.note("fe_liquid.volume_newton", False)
        valid = convergence.bracket_valid(P(0.2 * col.v0, t, col) - p, P(1.5 * col.v0, t, col) - p)
        convergence.note("fe_liquid.volume_bisect", None, bracket_valid=valid)
        lo, hi = 0.2 * col.v0, 1.5 * col.v0
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if P(mid, t, col) > p:
                lo = mid
            else:
                hi = mid
        out = 0.5 * (lo + hi)
        rec.update(ok=False, bracket_valid=valid, f_final=abs(P(out, t, col) - p), v_over_v0=out / col.v0)
        if tight:
            out = _polish(out, p, t, col, valid, rec)
        log.append(rec)
        return out

    return volume_at


def _bisect_wide(p, t, col):
    P = fe_liquid.pressure
    lo, hi = 0.05 * col.v0, 3.0 * col.v0
    mid = 0.5 * (lo + hi)
    while True:
        if P(mid, t, col) > p:
            lo = mid
        else:
            hi = mid
        new = 0.5 * (lo + hi)
        if new == mid:
            return mid
        mid = new


def _polish(v, p, t, col, valid, rec):
    P = fe_liquid.pressure
    if not valid:
        v = _bisect_wide(p, t, col)
    for _ in range(40):
        f = P(v, t, col) - p
        if abs(f) < TIGHT_PA:
            rec.update(tight_reached=True, tight_f=abs(f))
            return v
        h = v * 1e-6
        dfdv = (P(v + h, t, col) - P(v - h, t, col)) / (2.0 * h)
        if dfdv == 0.0:
            break
        v = v - f / dfdv
    w = _bisect_wide(p, t, col)
    rec.update(tight_reached=False, tight_f=abs(P(w, t, col) - p), substituted=True)
    return w


def _solve(name: str, mode: str):
    fe_liquid._CACHE.clear()
    log: list = []
    fe_liquid.volume_at = ORIGINAL if mode == "base" else _instrumented(log, tight=(mode == "tight"))
    try:
        body, expected = run.load_body(ENGINE / "bodies" / f"{name}.yaml")
        run.solve(body, run.load_chain())
    finally:
        fe_liquid.volume_at = ORIGINAL
    vals = {k: v for k, v in body.resolved.items() if isinstance(v, float)}
    return vals, expected, log


def _census(tag: str, log: list) -> None:
    bad = [r for r in log if not r["ok"]]
    ex: dict[str, int] = {}
    for r in log:
        ex[r["exit"]] = ex.get(r["exit"], 0) + 1
    print(f"  [{tag}] 호출 {len(log)} · Newton 못 맞춤 {len(bad)} · exit {ex}")
    if bad:
        ps = [r["p"] for r in bad]
        ts = [r["t"] for r in bad]
        print(f"      못 맞춘 호출 P {min(ps):.4g}–{max(ps):.4g} Pa · T {min(ts):.1f}–{max(ts):.1f} K · "
              f"열 {sorted({r['col'] for r in bad})}")
        print(f"      f_newton 최대 {max(r['f_newton'] for r in bad):.4g} Pa · f_final 최대 "
              f"{max(r['f_final'] for r in bad):.4g} Pa · 괄호 거짓 {sum(not r['bracket_valid'] for r in bad)}")
        for r in bad:
            if not r["bracket_valid"]:
                print(f"      ⚠ 괄호 거짓 — P {r['p']:.6g} Pa · T {r['t']:.3f} K · v/v0 {r['v_over_v0']:.6f}")
        if any("tight_reached" in r for r in bad):
            miss = [r for r in bad if not r.get("tight_reached")]
            print(f"      조인: 1e-3 Pa 닿음 {len(bad) - len(miss)} · 못 닿아 대체 {len(miss)}"
                  + (f" (그 최소 |f| {min(r['tight_f'] for r in miss):.4g} Pa)" if miss else "")
                  + f" · 조인 |f| 최대 {max(r['tight_f'] for r in bad):.4g} Pa")
            for r in miss:
                print(f"      대체 — P {r['p']:.6g} Pa · T {r['t']:.3f} K · |f| {r['tight_f']:.4g}")


def main(names: list[str]) -> int:
    registry.load_all()
    worst = 0
    for name in names:
        print(f"\n== {name}")
        base, expected, _ = _solve(name, "base")
        probe, _, plog = _solve(name, "probe")
        same = base.keys() == probe.keys() and all(base[k] == probe[k] or (math.isnan(base[k]) and math.isnan(probe[k]))
                                                   for k in base)
        print(f"  P-0 비트 같음: {same}")
        if not same:
            print("  ⚠ 계측이 값을 건드렸다 — 멈춤 (prereg §3 P-0)")
            return 2
        _census("원판", plog)
        tight, _, tlog = _solve(name, "tight")
        _census("조인 판", tlog)
        verdict_ok = True
        print("  대조 칸 (몸 파일 tol / 100)")
        for key, spec in sorted(expected.items()):
            if "tol" not in spec or key not in base:
                continue
            lim = spec["tol"] * abs(base[key]) / 100
            d = abs(tight[key] - base[key])
            ok = d < lim
            verdict_ok &= ok
            print(f"    {key:22} 원판 {base[key]:.10g} · 조인 {tight[key]:.10g} · 차 {d:.3g} · 한 {lim:.3g} · {'○' if ok else '×'}")
        tk = next((k for k in T_C_KEYS if k in base), None)
        if tk is None:
            print(f"    ⚠ T_c 키를 못 찾음 {T_C_KEYS} — 멈춤")
            return 2
        d = abs(tight[tk] - base[tk])
        ok = d < T_C_LIMIT_K
        verdict_ok &= ok
        print(f"    {tk:22} 원판 {base[tk]:.6f} · 조인 {tight[tk]:.6f} · 차 {d:.3g} K · 한 {T_C_LIMIT_K} K · {'○' if ok else '×'}")
        for k in ("core_cmb_temperature_solved", "cmb_temperature", "core_center_temperature_used"):
            if k in base and k != tk:
                print(f"    {k:22} 원판 {base[k]:.6f} · 조인 {tight[k]:.6f} · 차 {abs(tight[k] - base[k]):.3g} K (인쇄만)")
        for k in ("radius", "nmoi"):
            if k in base and k not in {kk for kk, s in expected.items() if "tol" in s}:
                print(f"    {k:22} 원판 {base[k]:.10g} · 조인 {tight[k]:.10g} · 차 {abs(tight[k] - base[k]):.3g} (인쇄만)")
        moved = sorted(k for k in base if k in tight and base[k] != tight[k])
        print(f"  움직인 칸 {len(moved)} / {len(base)}")
        print(f"  판정: {'① 표지 엄격' if verdict_ok else '② 실제 미수렴'}")
        worst = max(worst, 0 if verdict_ok else 1)
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["earth", "venus", "pandora"]))
