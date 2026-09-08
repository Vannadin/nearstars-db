# C48 진단용 — C20 의 적분 스텝을 실제로 바꿔 가며 화성 발산이 스텝 탓인지 가르는 일회성 측정 스크립트 (사전등록 포함)
"""Does C20's fixed 4 Myr step follow Mars's mantle time constant, or is the Mars result an integrator artefact?

⚠ Brief 157 (2026-09-08): `core_history.integrate` now sets its own step from the mantle time constant
(h = min(cap, 0.1·τ)); `step_myr` is the CAP. This sweep therefore became an upper-bound sweep — it still
runs, but "4 Myr" no longer means a fixed 4 Myr step. The fixed-step result it measured on 2026-09-08
(4/2/1 Myr diverge, 0.5/0.25 agree within 1.3 K) is recorded in interior-core.md's C48 and in test_core_history
(`adaptive=False` reproduces the divergence). The "τ ≈ 0.717 Myr" that stood in older comments here was the
²⁶Al half-life, not a mantle time constant; the derived values are in tools/adaptive-step-prereg.md.

    nohup python3 engine/tools/mars_step_sweep.py > /tmp/mars_sweep.log 2>&1 &

═══ PRE-REGISTRATION (Brief 156, 2026-09-08) — committed BEFORE the first run; nothing below it was known ═══

Question.  h/τ is 0.1 on Earth and 5.6 on Mars (τ ≈ 0.717 Myr from the mantle time constant at the start).
           Does halving the step change the Mars answer?

Steps.     4 · 2 · 1 · 0.5 · 0.25 Myr — these five, none added afterwards.

Compared.  Three numbers per step: final T_p (present-day mantle potential temperature), final T_c
           (present-day core-side CMB temperature), and T_p at the 3.7 Ga checkpoint (the row nearest
           t = −3.7 Gyr; Monders, Médard & Grove 2007 put Mars's mantle "similar to modern Earth" until then).

Verdict — one of these sentences, verbatim, on the successive-halving differences |Δ| of all three:
  A  "따라간다"                       every halving (4→2, 2→1, 1→0.5, 0.5→0.25) has all three |Δ| < 5 K.
  B  "못 따라간다"                    some halving has any |Δ| ≥ 5 K, including the last one.
  C  "0.25 에서 겨우 따라간다 — 기본 스텝을 바꿀 근거"   only the last halving (0.5→0.25) has all three < 5 K.
  D  "발산"                           a step diverges (integrator leaves the physical range or the declared
                                      domain); recorded per step, and a diverging step has no |Δ|.
  The 5 K width is the directing seat's choice; its only basis is that the Earth anchor reproduces to two
  decimals (T_p 1525.46 K), so 5 K is far above reproduction noise. No better basis was found before running.
  An outcome outside A–D is written down as its own kind afterwards, and the kind is registered then.

Not changed.  Gate body code (`core_history.py`) is untouched; the sweep sets the step through
              `integrate`'s call argument and builds the same `params` dict `solve` builds.

═══ WHY THIS FILE EXISTS (kept from 2026-09-08) ═══

⚠ **파이썬의 기본 인자는 정의 시점에 묶인다.** `core_history.STEP_MYR = 0.1` 로 모듈 전역을 바꿔도
`integrate(..., step_myr=STEP_MYR)` 의 기본값은 4.0 그대로다. 2026-09-08 에 이 좌석이 정확히 그 함정에 빠져
**스텝 넷을 돌리고 넷 다 4 Myr 로 돌았다** — 출력 네 줄이 전부 "발산" 이라 그럴듯했고, "스텝 탓이 아니다"
라고 적을 뻔했다. 지금은 `integrate(params, …, step_myr=step)` 로 **인자로** 넘긴다 — 기본값을 건드리지 않는다.

⚠ **그래서 스윕은 먼저 자기가 살아 있음을 증명한다** (`prove_live`): 지구를 4 Myr 와 200 Myr 로 돌려 걸음 수가
다르고, 4 Myr 의 T_p 가 게이트 앵커 1525.46 K 를 재현하는지. `engine/test_interior.py`: *"늘 발화하면 상수다"*.

Memory: only the three compared numbers per step are kept; the history rows are dropped after each step.
Every line is flushed as it is written, so a killed run leaves the steps it finished.
"""
from __future__ import annotations

import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import cmb_flux as cf                 # noqa: E402
import core_energy as ce              # noqa: E402
import core_history as ch             # noqa: E402
import radiogenic as rg               # noqa: E402
from interior import solve as isolve  # noqa: E402

STEPS_MYR = (4.0, 2.0, 1.0, 0.5, 0.25)
TOL_K = 5.0
CHECKPOINT_GYR = -3.7
EARTH_ANCHOR_T_P = 1525.46
MARS = dict(mass_earth=0.1074, core_mass_fraction=0.24, radius_earth=0.5320, age_gyr=4.54)
EARTH = dict(mass_earth=1.0, core_mass_fraction=0.325, radius_earth=1.0, age_gyr=4.54)


def say(msg: str) -> None:
    print(msg, flush=True)


def build(body: dict, t_pot: float, core_init: float) -> tuple[dict, float, float]:
    """The same `params` dict `core_history.solve` builds, plus the two initial temperatures (mantle = core/r_b)."""
    ii = isolve(mass_earth=body["mass_earth"], core_mass_fraction=body["core_mass_fraction"],
                composition="earth_like", body_class="rocky", potential_temperature=t_pot)
    v = ii.values
    m_kg = body["mass_earth"] * cf.M_EARTH_KG
    r_p = body["radius_earth"] * cf.R_EARTH_M
    cmf = body["core_mass_fraction"]
    params = {"material": "fe_prem", "p_cmb": v["cmb_pressure"] * 1e9, "r_cmb": v["core_radius"] * cf.R_EARTH_M,
              "m_core": m_kg * cmf, "m_mantle": m_kg * (1.0 - cmf),
              "r_b": v["cmb_temperature"] / t_pot,
              "g": cf.G_NEWTON * m_kg / r_p ** 2, "r_p": r_p, "h_core": ce.H_CORE,
              "h_m_present_w": rg.budget(m_kg * (1.0 - cmf))["mantle_w"]}
    return params, core_init, core_init / params["r_b"]


def run(params: dict, t_c0: float, t_m0: float, age_gyr: float, step_myr: float) -> dict:
    """One integration at an explicit step. Returns the three compared numbers, or the divergence by name."""
    t0 = time.time()
    try:
        hist = ch.integrate(params, t_c0, t_m0, age_gyr, step_myr=step_myr)
    except Exception as e:                      # PhaseGap / ValueError: the integrator left the physical range
        return {"diverged": f"{type(e).__name__}: {str(e)[:110]}", "seconds": time.time() - t0}
    if "refused" in hist:
        return {"diverged": f"domain: {hist['refused'][:110]}", "seconds": time.time() - t0}
    rows = hist["rows"]
    last = rows[-1]
    near = min(rows, key=lambda r: abs(r["t_gyr"] - CHECKPOINT_GYR))
    out = {"n": hist["n_steps"], "t_p": last["t_m"], "t_c": last["t_c"], "t_p_37": near["t_m"],
           "t_37_actual": near["t_gyr"], "seconds": time.time() - t0}
    if any(not math.isfinite(x) for x in (out["t_p"], out["t_c"], out["t_p_37"])):
        return {"diverged": "non-finite temperature", "seconds": out["seconds"]}
    del rows, hist
    return out


def prove_live() -> bool:
    params, tc0, tm0 = build(EARTH, 1600.0, 4800.0)
    a = run(params, tc0, tm0, EARTH["age_gyr"], 4.0)
    b = run(params, tc0, tm0, EARTH["age_gyr"], 200.0)
    na, nb = a.get("n"), b.get("n")
    tp = a.get("t_p")
    say(f"살아있음 증명 — 지구, 스텝 4 Myr: {na} 걸음, T_p {tp if tp is None else round(tp, 2)} K (앵커 {EARTH_ANCHOR_T_P}) · "
        f"200 Myr: {nb if nb is not None else b.get('diverged')}")
    ok = na is not None and na != nb and tp is not None and abs(tp - EARTH_ANCHOR_T_P) < 0.05
    say("  " + ("✓ 스텝이 실제로 걸리고 지구 앵커가 재현된다" if ok else "✗ 스윕이 죽었거나 앵커가 안 맞는다 — 아래 수는 전부 무의미"))
    return ok


def main() -> int:
    say(f"SWEEP START {time.strftime('%Y-%m-%d %H:%M:%S')} — pre-registered steps {STEPS_MYR}, tolerance {TOL_K} K")
    if not prove_live():
        say("SWEEP END rc=1 (liveness failed)")
        return 1
    params, tc0, tm0 = build(MARS, 1600.0, 4800.0)
    say(f"\n화성 — T_pot 1600 K 선언, 핵 초기 {tc0:.0f} K, 맨틀 초기 {tm0:.0f} K (= 4800 / r_b {params['r_b']:.4f})")
    say(f"{'step Myr':>9} {'steps':>7} {'T_p final':>10} {'T_c final':>10} {'T_p@3.7Ga':>10} {'dT_p':>7} {'dT_c':>7} {'dT_p37':>7}  {'sec':>6}")
    prev = None
    deltas = []          # per halving: (all three < TOL) or None if a side diverged
    for step in STEPS_MYR:
        r = run(params, tc0, tm0, MARS["age_gyr"], step)
        if "diverged" in r:
            say(f"{step:9.2f} {'—':>7} {'발산':>10} {'':>10} {'':>10} {'':>7} {'':>7} {'':>7}  {r['seconds']:6.0f}   {r['diverged']}")
            deltas.append(None)
            prev = None
            continue
        if prev is None:
            d = ("", "", "")
        else:
            dd = (r["t_p"] - prev["t_p"], r["t_c"] - prev["t_c"], r["t_p_37"] - prev["t_p_37"])
            d = tuple(f"{x:+.2f}" for x in dd)
            deltas.append(all(abs(x) < TOL_K for x in dd))
        say(f"{step:9.2f} {r['n']:7d} {r['t_p']:10.2f} {r['t_c']:10.2f} {r['t_p_37']:10.2f} {d[0]:>7} {d[1]:>7} {d[2]:>7}  {r['seconds']:6.0f}")
        prev = r
    halvings = [x for x in deltas if x is not None]
    n_div = sum(1 for x in deltas if x is None)
    if n_div:
        verdict = f"발산 ({n_div} of {len(STEPS_MYR)} steps)"
    elif len(halvings) == 4 and all(halvings):
        verdict = "따라간다"
    elif len(halvings) == 4 and halvings[-1] and not all(halvings[:-1]):
        verdict = "0.25 에서 겨우 따라간다 — 기본 스텝을 바꿀 근거"
    elif len(halvings) == 4:
        verdict = "못 따라간다"
    else:
        verdict = "등록되지 않은 결과 — 종류를 나중에 등록한다"
    say(f"\n판정(사전등록 문구): {verdict}")
    say(f"SWEEP END rc=0 {time.strftime('%H:%M:%S')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
