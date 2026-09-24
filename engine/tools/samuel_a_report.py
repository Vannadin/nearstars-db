# 판 4 A 보고 — k_d × Λ 상자를 층상 본판(3-1)과 균일 비교판으로 훑어 A 네 조건을 인쇄한다
"""Plate 4's A report (pre-registration v2 §5 A, v2-23, v2-24). Prints; decides nothing beyond A's own four
conditions, and the widths are ours (borrowed EDT1 σ), not an implementation tolerance.

    python3 engine/tools/samuel_a_report.py <MOESM3 DATA_FIG1 dir> [--jobs N] [--out results.jsonl]

The box is k_d 4–16 W/m/K × Λ 5–20, both in steps of 1 — the step is our choice (plate 2 swept Λ by 1).
Every point runs twice: the main plate (stratified, Fe#_di 94.1306, v2-24 ①) and the comparison plate
(uniform, f_e ≡ 1). If the two plates' A verdicts differ, A cannot pass — «depends on the layer
distribution» (v2-24 ①). Variant 3-1 is the main plate (v2-23 §4 ④); 3-0 runs once, at the main plate's
best point, as a comparison.
"""
from __future__ import annotations

import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import samuel_run as sr                # noqa: E402
import samuel_structure as ss          # noqa: E402
import samuel_thermal as st            # noqa: E402

CAP_MYR = 10.0
K_DS = [4.0 + i for i in range(13)]
LAMBDAS = [5.0 + i for i in range(16)]
FE_TOP_MAIN = 94.1306                  # v2-24 ①: the most stratified allowed top value (bottom Fe# 100)
LAYER_BASE = dict(d_d=st.D_D_M, lambda_d=14.373, fe_mean=96.97, nodes=41,
                  source="2023 Fig. 1 g–l · v2 §4 · v2-24")
_PROF = None


def _one(args):
    global _PROF
    k_d, lam, fe_top, melting, tc, tm = args
    if _PROF is None:
        _PROF = ss.mars_profile(Path(__file__).resolve().parent.parent / "bodies" / "mars.yaml")
    layer = dict(LAYER_BASE, k_d=k_d, fe_top=fe_top, melting=melting)
    s = sr.Setup(lam=lam, profile=_PROF, g=_PROF.gravity(_PROF.radius_m), g_c=_PROF.gravity(st.R_CORE_M),
                 model="bml", layer=layer)
    t0 = time.time()
    out = sr.run(s, CAP_MYR)
    res = {"k_d": k_d, "lam": lam, "fe_top": fe_top, "melting": melting, "secs": time.time() - t0,
           "n_steps": out.get("n_steps")}
    if "refused" in out:
        res["refused"] = [out["refused_at_gyr"], out["refused"]]
        return res
    a = sr.a_layer(out["rows"], tc, tm)
    res["pass"] = a["pass"]
    res["conditions"] = {k: [v, ok] for k, (v, ok) in a["conditions"].items()}
    last = out["rows"][-1]["layer"]
    res["t_b_printed_today"] = last["t_b_printed"]
    res["layer"] = {k: v for k, v in out["layer"].items() if k != "describe"}
    res["describe"] = out["layer"]["describe"]
    return res


def _line(r: dict) -> str:
    if "refused" in r:
        return f"  k_d {r['k_d']:>4.0f} Λ {r['lam']:>4.0f} — 거절 @ {r['refused'][0]:.3f} Gyr: {r['refused'][1]}"
    c = r["conditions"]
    (tm, tc), ok0 = c["㉠"]
    (rm, rc), ok1 = c["㉡"]
    tc1, ok2 = c["①"]
    (pk, pt), ok3 = c["②"]
    mark = lambda ok: "○" if ok else "×"
    margin = r["layer"]["margin"]
    melt = "녹음 끔" if margin is None else (f"최대 φ {r['layer']['max_phi']:.3f} · 녹음 거리 최소 {margin[0]:.0f} K "
                                             f"@ {margin[4]:.3f} Gyr")
    return (f"  k_d {r['k_d']:>4.0f} Λ {r['lam']:>4.0f} — ㉠{mark(ok0)} T_m {tm:.1f} T_c {tc:.1f} · ㉡{mark(ok1)} "
            f"RMS {rm:.1f}/{rc:.1f} · ①{mark(ok2)} {tc1:+.1f} · ②{mark(ok3)} {pk:.1f}@{pt:.2f} · "
            f"{'통과' if r['pass'] else '불통과'} · {melt} · 인쇄 꼴 T′_b 오늘 {r['t_b_printed_today']:.1f} K · "
            f"{r['secs']:.0f} s")


def main() -> int:
    argv = sys.argv[1:]
    fig = Path(argv[0])
    jobs = int(argv[argv.index("--jobs") + 1]) if "--jobs" in argv else 4
    out_path = Path(argv[argv.index("--out") + 1]) if "--out" in argv else None
    tc = sr.read_panel(fig / "PANEL_H" / "Tc.dat")
    tm = sr.read_panel(fig / "PANEL_H" / "Tm.dat")
    print("판 4 A — 2023 그림 1 g–l · 폭은 우리가 고른 폭(EDT1 σ 를 빌림) — 구현 오차 폭이 아님")
    print(f"  상자 k_d {K_DS[0]:g}–{K_DS[-1]:g} × Λ {LAMBDAS[0]:g}–{LAMBDAS[-1]:g}, 간격 1 (우리 선택) · "
          f"본판 층상 Fe#_di {FE_TOP_MAIN} · 비교판 균일 · 3-1 본판")
    tasks = [(k, lam, top, True, tc, tm) for top in (FE_TOP_MAIN, None) for k in K_DS for lam in LAMBDAS]
    t0 = time.time()
    with ProcessPoolExecutor(jobs) as ex:
        results = list(ex.map(_one, tasks))
    if out_path:
        out_path.write_text("".join(json.dumps({k: v for k, v in r.items()}, ensure_ascii=False) + "\n"
                                    for r in results))
    main_r = [r for r in results if r["fe_top"] is not None]
    uni_r = [r for r in results if r["fe_top"] is None]
    for label, rs in (("본판 (층상, 3-1)", main_r), ("비교판 (균일, 3-1)", uni_r)):
        print(f"\n{label}")
        print(f"  [J] {next((r['describe'] for r in rs if 'describe' in r), '—')}")
        for r in rs:
            print(_line(r))
    pm = {(r["k_d"], r["lam"]) for r in main_r if r.get("pass")}
    pu = {(r["k_d"], r["lam"]) for r in uni_r if r.get("pass")}
    print(f"\n통과 점 — 본판 {len(pm)} · 비교판 {len(pu)} · 같은 점 {len(pm & pu)}")
    edge = [p for p in pm if p[0] in (K_DS[0], K_DS[-1]) or p[1] in (LAMBDAS[0], LAMBDAS[-1])]
    if edge:
        print(f"  ⚠ 본판 통과 점 중 상자 가장자리 {len(edge)}: {sorted(edge)}")
    if any(k >= 12 for k, _ in pm):
        print("  ⚠ k_d 12–16 에 통과 점 — v2 §5 A 의 신호(2023 은 사후 k_d ≈ 4)")
    verdict = bool(pm) and bool(pu)
    print(f"[A 판정] {'통과' if verdict else '불통과'}"
          + ("" if bool(pm) == bool(pu) else " — 두 판 판정이 다름: «층상 분포 선택에 의존» (v2-24 ①)"))
    # 3-0 comparison at the main plate's best point (smallest RMS sum)
    ok = [r for r in main_r if "conditions" in r]
    if ok:
        best = min(ok, key=lambda r: sum(r["conditions"]["㉡"][0]))
        r0 = _one((best["k_d"], best["lam"], FE_TOP_MAIN, False, tc, tm))
        print(f"\n3-0 비교(녹음 끔, 본판 RMS 최소 점 k_d {best['k_d']:g} Λ {best['lam']:g})")
        print(_line(r0))
    print(f"\n전체 {time.time() - t0:.0f} s · 실행 {len(results) + (1 if ok else 0)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
