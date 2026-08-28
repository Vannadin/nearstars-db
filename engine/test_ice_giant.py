# 얼음거대행성 앵커 — 천왕성·해왕성을 실제로 풀어 굳힌 값과 비트까지 대조한다
"""Anchor the ice-giant branch: Uranus and Neptune, solved live on every gate run.

    python3 engine/test_ice_giant.py              전체 풀이 둘 (~1.5 분) + 굳힌 값과 비트 대조
    python3 engine/test_ice_giant.py --fast       적분 한 번 + 경로 지문만 (1 초). 반복 작업용
    python3 engine/test_ice_giant.py --refresh    전체 재계산 → ice_giant_anchor.json 갱신
    python3 engine/test_ice_giant.py --table      문서의 얼음거대행성 표를 다시 낸다

**왜 이 파일이 있나.** 2026-08-28 아침까지 이 두 앵커는 `test_interior.py --icegiant` 뒤에
있었고 check.sh 는 그것을 돌리지 않았다 — 천왕성 하나가 1038 초였기 때문이다. 그 플래그마저
낡은 2500 K 선언으로 거절만 찍고 있었으니 지키는 것이 없었다. 같은 날 그 1038 초의 정체가
잡혔다: 상태방정식이 아니라 **층 경계가 걸음 단위로 양자화돼 겉질량이 계단이 되고, 압력
사격이 그 수직면에서 수렴하지 못해 200 회를 같은 중심압에 다시 적분** 하는 것이었다
(`speed-context-notes.md` §6). 경계를 걸음 안에서 보간하자 (§11) 천왕성이 40 초대로
내려왔고, 그래서 앵커가 게이트로 **실제 계산으로** 돌아왔다. 굳힌 파일은 그 계산의
회귀선이다 — 얼음 III·V·VI 상수와 같은 규율로, 값이 마지막 비트까지 같아야 통과하고,
물리를 바꾸는 작업은 `--refresh` 로 다시 굳혀 그 사실을 diff 에 남긴다.

**게이트가 보는 것 셋.**

1. **전체 풀이가 굳힌 값과 비트까지 같다** — 반지름·C/MR²·중심온도·중심압. 상태방정식,
   페르미 적분, 적분기, 층 쌓기, 사격, 온도 고리 어느 것이 바뀌어도 여기서 걸린다.
2. **격자 위상에 둔감하다** — 수렴점에서 1499 와 1501 걸음으로 적분한 반지름이 1e-5 안.
   계단 결함은 바로 이 검사에 걸린다 (보간 전에는 2e-3 이 흔들렸다). `test_interior.py`
   의 격자 수렴 검사가 지구에서 묻는 것을, 밀도 대비가 큰 얼음/가스 경계에서 묻는다.
3. **격자 수렴** — 1500 → 6000 걸음에서 반지름이 1e-3 안에서 움직인다 (측정: 4.6e-4, 2차).

`--fast` 는 굳힌 수렴점에서 적분 한 번과 사격 경로의 바이트코드 지문만 본다. 1 초.
전체 풀이 없이 적분기·상태방정식의 변화를 잡는 용도이고, 게이트는 이것을 쓰지 않는다.
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import interior
from interior import EARTH_MASS_KG, EARTH_RADIUS_M, integrate, solve

ANCHOR_FILE = Path(__file__).with_name("ice_giant_anchor.json")

# 얼음거대행성의 앵커. Scheibe+ 2019 Table 1 의 **Mazevet 물 EOS 행** 에서 왔다 —
# 우리가 쓰는 것과 같은 상태방정식으로 지은 모형이라야 조성을 빌려올 수 있다.
# 온도는 **1 bar 온도** 다 (Voyager 전파엄폐, hhe-eos-context-notes). 수소-헬륨 표가 들어온
# 뒤로 포텐셜 온도의 선언은 표면(1 bar)에 걸리고, 발표 반지름도 그 준위의 값이다.
# 2500 K (얼음 맨틀 꼭대기로 읽던 폴리트로프 시절의 값) 를 그대로 두면 두 행성 다 거절된다.
# (이름, M⊕, 발표 평균반지름 R⊕, 암석 핵 M⊕, H/He 총량 M⊕, 1 bar K)
ICE_GIANTS = (
    ("Uranus", 14.536, 3.9808, 0.79, 2.0, 76.0),
    ("Neptune", 17.147, 3.8646, 1.04, 2.2, 72.0),
)
PHASE_TOL = 1e-5        # 1499 ↔ 1501 걸음의 반지름 상대차. 계단이면 2e-3 이 나온다
GRID_TOL = 1e-3         # 1500 → 6000 걸음의 반지름 상대차. 측정 4.6e-4
BIT_KEYS = ("radius", "nmoi", "core_temperature", "core_pressure")


def _fractions(m: float, m_core: float, m_hhe: float) -> tuple[float, float]:
    gmf = m_hhe / m
    return 1.0 - gmf - m_core / m, gmf


def _body(name: str):
    for row in ICE_GIANTS:
        if row[0] == name:
            return row
    raise KeyError(name)


def _solve(name: str):
    _n, m, _r, m_core, m_hhe, t1bar = _body(name)
    imf, gmf = _fractions(m, m_core, m_hhe)
    return solve(m, body_class="ice_giant", core_mass_fraction=0.0,
                 ice_mass_fraction=imf, gas_mass_fraction=gmf,
                 potential_temperature=t1bar)


def _standalone(name: str, p_center_pa: float, t_center: float):
    """수렴점에서 적분 한 번. 풀이의 마지막 적분과 같은 인자다."""
    _n, m, _r, m_core, m_hhe, t1bar = _body(name)
    imf, gmf = _fractions(m, m_core, m_hhe)
    return integrate(p_center_pa, m * EARTH_MASS_KG, 0.0, imf, "fe_prem", gmf=gmf,
                     t_center=t_center, t_pot=t1bar, ice_material="h2o_hot")


def _radius_at_steps(name: str, p_center_pa: float, t_center: float, steps: int) -> float:
    base = interior.STEPS
    try:
        interior.STEPS = steps
        return _standalone(name, p_center_pa, t_center).radius_m / EARTH_RADIUS_M
    finally:
        interior.STEPS = base


# ── 경로 지문 (--fast) ──────────────────────────────────────────────────

# 굳힌 수렴점으로 가는 길을 정하는 것들. `--fast` 가 적분 한 번으로 못 보는 바깥 고리다.
PATH_FUNCTIONS = ("solve", "shoot", "_shoot_pressure", "_narrow_bracket",
                  "_surface_temperature_met", "_stack", "integrate")
PATH_CONSTANTS = ("STEPS", "INTERPOLATE_LAYERS", "MAX_STEPS", "SHOOT_ITERS", "SHOOT_TOL",
                  "T_PASSES", "T_TOL", "T_SURFACE_TOL", "T_BRACKET_TRIES", "NARROW_ITERS",
                  "NARROW_RATIO", "FLUID_CLASSES", "ICE_GIANT_CLASSES")


def _feed_code(h, code) -> None:
    """코드 객체를 재귀로 해시한다. docstring(첫 상수가 문자열이면) 은 뺀다."""
    h.update(code.co_code)
    h.update(repr(code.co_names).encode())
    consts = list(code.co_consts)
    if consts and isinstance(consts[0], str):
        consts = consts[1:]
    for c in consts:
        if hasattr(c, "co_code"):
            _feed_code(h, c)
        else:
            h.update(repr(c).encode())


def path_fingerprint() -> str:
    h = hashlib.sha256()
    for name in PATH_FUNCTIONS:
        _feed_code(h, getattr(interior, name).__code__)
    for name in PATH_CONSTANTS:
        h.update(f"{name}={getattr(interior, name)!r}".encode())
    # 바이트코드는 인터프리터 버전에 묶인다. 버전이 바뀌면 지문이 바뀌고, 그건 --refresh 로
    # 답할 일이지 지문을 넓힐 일이 아니다.
    h.update(platform.python_version().encode())
    return h.hexdigest()[:16]


# ── 굳히기 ──────────────────────────────────────────────────────────────

def _structure_record(st) -> dict:
    return {"radius_earth": repr(st.radius_m / EARTH_RADIUS_M),
            "mass_kg": repr(st.mass_kg), "moi": repr(st.moi), "nmoi": repr(st.nmoi),
            "t_surface": repr(st.t_surface), "core_radius_m": repr(st.core_radius_m)}


def _record(name: str, res, seconds: float) -> dict:
    _n, _m, r_pub, _mc, _mh, t1bar = _body(name)
    rec = {"seconds": round(seconds, 1), "regime": res.regime, "applicable": res.applicable,
           "converged": res.converged, "grade": res.grade, "t_1bar_k": t1bar,
           "r_published_earth": r_pub}
    if not res.applicable:
        rec["reason"] = res.reason
        return rec
    v = res.values
    rec["values"] = {k: (repr(x) if isinstance(x, float) else x) for k, x in v.items()}
    p_pa = v["core_pressure"] * 1e9
    st = _standalone(name, p_pa, v["core_temperature"])
    rec["standalone"] = {"p_center_pa": repr(p_pa), "t_center": repr(v["core_temperature"]),
                         **_structure_record(st)}
    rec["standalone_reproduces_solve"] = rec["standalone"]["radius_earth"] == repr(v["radius"])
    return rec


def refresh() -> int:
    out = {"python": platform.python_version(), "path_fingerprint": path_fingerprint(),
           "frozen_at": time.strftime("%Y-%m-%d"), "steps": interior.STEPS, "bodies": {}}
    for name, _m, r_pub, _mc, _mh, _t in ICE_GIANTS:
        print(f"{name} — 전체 풀이 …", flush=True)
        t0 = time.perf_counter()
        res = _solve(name)
        rec = _record(name, res, time.perf_counter() - t0)
        if res.applicable:
            v = res.values
            print(f"  {rec['seconds']:.0f} s · R {v['radius']:.4f} R⊕ "
                  f"({(v['radius'] / r_pub - 1) * 100:+.2f} %) · T_c {v['core_temperature']:.0f} K "
                  f"· converged={res.converged}")
        else:
            print(f"  {rec['seconds']:.0f} s · 거절 — {res.reason[:90]}")
        out["bodies"][name] = rec
    ANCHOR_FILE.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"굳혔다 → {ANCHOR_FILE.name}")
    return 0


def table() -> None:
    """문서의 얼음거대행성 표. 굳힌 파일에서 낸다 — 전체 풀이를 다시 돌리지 않는다."""
    frozen = json.loads(ANCHOR_FILE.read_text(encoding="utf-8"))
    print("| planet | T at 1 bar | R derived | R published | Δ | C/MR² | T_c | P_c | "
          "converged | grade |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for name, rec in frozen["bodies"].items():
        r_pub = rec["r_published_earth"]
        if not rec["applicable"]:
            print(f"| {name} | {rec['t_1bar_k']:.0f} K | declined | {r_pub:.3f} R⊕ | – | – | – | – "
                  f"| – | – |")
            continue
        v = {k: float(rec["values"][k]) for k in BIT_KEYS}
        print(f"| {name} | {rec['t_1bar_k']:.0f} K | {v['radius']:.3f} R⊕ | {r_pub:.3f} R⊕ | "
              f"{(v['radius'] / r_pub - 1) * 100:+.2f} % | {v['nmoi']:.4f} | "
              f"{v['core_temperature']:.0f} K | {v['core_pressure']:.0f} GPa | "
              f"{rec['converged']} | {rec['grade']} |")


# ── 게이트 ──────────────────────────────────────────────────────────────

def _fast(frozen: dict, fails: list[str]) -> None:
    """적분 한 번 + 경로 지문. 전체 풀이 없이 적분기·상태방정식의 변화를 잡는다."""
    fp_now, fp_then = path_fingerprint(), frozen["path_fingerprint"]
    ok = fp_now == fp_then
    if not ok:
        fails.append("사격·온도 고리·적분기의 경로 지문이 굳힐 때와 다르다 — 수렴점이 옮겨갔을 "
                     "수 있다. 전체 풀이(기본 실행)나 `--refresh` 로 확인하라")
    print(f"  [{'PASS' if ok else 'FAIL'}] 경로 지문 {fp_then} "
          f"{'그대로' if ok else '→ ' + fp_now + ' (바뀜)'} — "
          f"{', '.join(PATH_FUNCTIONS)} + 상수 {len(PATH_CONSTANTS)}개")
    for name, rec in frozen["bodies"].items():
        if not rec["applicable"]:
            print(f"  [FROZEN] {name} — 거절이 앵커다. 굳힌 이유: {rec['reason'][:70]}…")
            continue
        sa = rec["standalone"]
        t0 = time.perf_counter()
        st = _standalone(name, float(sa["p_center_pa"]), float(sa["t_center"]))
        dt = time.perf_counter() - t0
        now = _structure_record(st)
        moved = [k for k in ("radius_earth", "mass_kg", "moi", "t_surface") if now[k] != sa[k]]
        if moved:
            fails.append(f"{name}: 굳힌 수렴점에서 적분이 다른 값을 낸다 — "
                         + ", ".join(f"{k} {sa[k]} → {now[k]}" for k in moved))
        print(f"  [{'FAIL' if moved else 'PASS'}] {name} — 수렴점에서 적분 한 번 {dt:.1f} s: "
              f"{'움직였다: ' + ', '.join(moved) if moved else '반지름·질량·관성모멘트·표면온도 비트까지 같다'}")
    print("  [SKIP] --fast 는 전체 풀이를 돌리지 않는다. 게이트(기본 실행)가 돌린다")


def _live(frozen: dict, fails: list[str]) -> None:
    for name, rec in frozen["bodies"].items():
        t0 = time.perf_counter()
        res = _solve(name)
        dt = time.perf_counter() - t0
        if not rec["applicable"]:
            same = (not res.applicable) and res.reason == rec["reason"]
            if not same:
                fails.append(f"{name}: 굳힌 것은 거절인데 지금은 "
                             f"{'다른 이유로 거절한다' if not res.applicable else '풀린다'} — "
                             "의도한 변화면 --refresh")
            print(f"  [{'PASS' if same else 'FAIL'}] {name} — 거절이 앵커다 ({dt:.0f} s): "
                  f"{rec['reason'][:70]}…")
            continue
        if not res.applicable:
            fails.append(f"{name}: 풀려야 하는데 거절했다 — {res.reason[:80]}")
            print(f"  [FAIL] {name} 거절됨 ({dt:.0f} s)")
            continue
        v = res.values
        moved = [k for k in BIT_KEYS if repr(v[k]) != rec["values"][k]]
        if moved:
            fails.append(f"{name}: 전체 풀이가 굳힌 값과 다르다 — "
                         + ", ".join(f"{k} {rec['values'][k]} → {v[k]!r}" for k in moved)
                         + ". 의도한 변화면 `--refresh` 로 다시 굳혀 diff 에 남겨라")
        if not res.converged:
            fails.append(f"{name}: converged=False")
        r_pub = rec["r_published_earth"]
        print(f"  [{'FAIL' if moved or not res.converged else 'PASS'}] {name} — 전체 풀이 {dt:.0f} s"
              f" (굳힐 때 {rec['seconds']:.0f} s): "
              f"{'움직였다: ' + ', '.join(moved) if moved else '반지름·C/MR²·중심온도·중심압 비트까지 같다'}")
        print(f"         R {v['radius']:.4f} R⊕ vs 발표 {r_pub:.4f} ({(v['radius'] / r_pub - 1) * 100:+.2f} %) "
              f"· C/MR² {v['nmoi']:.4f} · T_c {v['core_temperature']:.0f} K "
              f"· P_c {v['core_pressure']:.0f} GPa · converged={res.converged}")

        # 격자 위상과 격자 수렴 — 수렴점에서 적분만 다시 한다 (사격은 안 돈다).
        p_pa, t_c = v["core_pressure"] * 1e9, v["core_temperature"]
        base = interior.STEPS
        r_lo = _radius_at_steps(name, p_pa, t_c, base - 1)
        r_hi = _radius_at_steps(name, p_pa, t_c, base + 1)
        r_4x = _radius_at_steps(name, p_pa, t_c, base * 4)
        phase = abs(r_hi - r_lo) / v["radius"]
        drift = abs(r_4x - v["radius"]) / r_4x
        ok = phase < PHASE_TOL
        if not ok:
            fails.append(f"{name}: 격자 위상 {base - 1} ↔ {base + 1} 에서 반지름이 {phase:.1e} "
                         "움직인다 — 걸음 안의 경계가 다시 양자화됐다 (계단)")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} — 격자 위상 {base - 1} ↔ {base + 1}: "
              f"반지름 상대차 {phase:.1e} (< {PHASE_TOL:.0e}; 계단이면 ~2e-3)")
        ok = drift < GRID_TOL
        if not ok:
            fails.append(f"{name}: 격자 {base} → {base * 4} 에서 반지름이 {drift:.1e} 움직인다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} — 격자 {base} → {base * 4}: "
              f"반지름 상대차 {drift:.1e} (< {GRID_TOL:.0e}; 발표값과의 차 "
              f"{abs(v['radius'] / r_pub - 1):.1e} 의 {abs(v['radius'] / r_pub - 1) / max(drift, 1e-12):.0f} 분의 1)")


def main() -> int:
    if "--refresh" in sys.argv:
        return refresh()
    if "--table" in sys.argv:
        table()
        return 0

    fails: list[str] = []
    if not ANCHOR_FILE.exists():
        print(f"  [FAIL] {ANCHOR_FILE.name} 이 없다 — `--refresh` 로 굳혀라")
        return 1
    frozen = json.loads(ANCHOR_FILE.read_text(encoding="utf-8"))
    print("얼음거대행성 앵커 — 천왕성·해왕성이 굳힌 값을 비트까지 다시 내는가")
    print(f"  굳힌 날 {frozen['frozen_at']} · python {frozen['python']} · {frozen.get('steps')} 걸음")
    if "--fast" in sys.argv:
        _fast(frozen, fails)
    else:
        _live(frozen, fails)

    if fails:
        print(f"\n실패 {len(fails)}건")
        for f in fails:
            print(f"  · {f}")
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
