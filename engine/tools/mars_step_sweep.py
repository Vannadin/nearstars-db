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
           (present-day core-side CMB temperature), and T_p at the 3.7 Ga checkpoint (⚠ from 2026-09-19 **interpolated** by `core_history.t_at_gyr`, not the row nearest
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
import core_history as ch             # noqa: E402
import radiogenic as rg               # noqa: E402
import mantle_flux as mf            # noqa: E402  — 픽스처 표면온도
from interior import solve as isolve  # noqa: E402
from interior import infer_composition  # noqa: E402

STEPS_MYR = (4.0, 2.0, 1.0, 0.5, 0.25)
TOL_K = 5.0
CHECKPOINT_GYR = -3.7
EARTH_ANCHOR_T_P = 1525.46
# ⚠ **Brief 166 D.** Every number this file prints or compares — the liveness anchor 1525.46, the 0.25 Myr
# row 1382.90 / 3893.07 / 1669.12 — was measured with the core heating at **1.5 pW/kg**, which was the engine's
# nominal until owner decision ⑤ (2026-09-09) lowered it to 0.14. The sweep keeps its own condition explicitly
# so that a later change of the nominal cannot silently move a recorded sweep: `EARTH_ANCHOR_T_P` tests the
# integrator, not `core_energy.H_CORE`. Re-running under the declared H is a different sweep and would be
# recorded as one. (Same H as `test_core_energy.H4`, Nimmo+ 2004 Table 4's 400 ppm K.)
H_NIMMO = 1.5e-12
# ⚠ **이 둘은 바디 파일의 사본이었다 — 화성 쪽 사본은 지웠다** (2026-09-20, 미결 25).
#   화성의 `core_mass_fraction` 선언이 C57 (c) 에서 트리에서 사라진 뒤에도 이 dict 가 **0.24** 를
#   계속 내줬다. 원본 없는 사본이라 아무도 대조하지 않았고, 터지지 않으니 게이트도 안 잡았다.
#   ⚠ **값을 그냥 빼면 더 나빴다 — 실측이다.** `core_mass_fraction=None` 으로 `interior.solve` 를
#   부르면 역산으로 가지 않고 **프리셋 0.325(지구)** 로 물러선다. 화성의 핵을 지구 값으로 계산하면서
#   「화성」이라 인쇄하므로 사본보다 조용히 틀린다. 역산은 `interior.infer_composition(mass, radius, …)`
#   라는 **다른 함수**이고, 질량과 반지름 **둘** 로 미지수 하나를 푼다.
#   ⚠ 그래서 사본을 지우면서 **읽는 길을 같이 놨다** — `_composition()` 의 세 갈래(선언 · 역산 ·
#   이름 대는 정지)이고, `build()` 가 `radius_earth` 를 호출에 넘긴다. 이 dict 가 그 값을 이미
#   들고 있었는데 호출이 안 넘기고 있었다. **없던 것은 파일이 아니라 호출이다.**
#   ⚠ 지구 쪽 `core_mass_fraction=0.325` 는 **사본이 아니라 지구의 값**이라 남긴다. 그래서 지구는
#   갈래 1 로, 화성은 갈래 2 로 돈다 — 두 갈래가 한 판에서 같이 돌아야 둘 다 살아 있음이 보인다.
MARS = dict(mass_earth=0.1074, radius_earth=0.5320, age_gyr=4.54)
EARTH = dict(mass_earth=1.0, core_mass_fraction=0.325, radius_earth=1.0, age_gyr=4.54)


# ⚠ **조성 이름과 핵질량비의 «출처» 는 다른 양이다** (2026-09-20, 감사석이 이 자리에서 잡음).
#   `composition` 은 **엔진의 재료 어휘**다 — `interior.COMPOSITIONS` 의 다섯 키(`iron` ·
#   `earth_like` · `silicate` · `water` · `gas_giant`) 밖의 이름을 주면 `interior.py` 가
#   «재료가 배정된 조성이 아니다» 로 **거절**하고, 그 거절은 `values` 를 안 싣는다.
#   ⚠ **한 번 그렇게 지었다가 화성 갈래를 통째로 죽였다.** 역산 결과의 `inputs["composition"]` 은
#   항상 `"inferred"` 인데 그것을 `isolve` 에 넘겼다. 엔진이 적분 전에 거절하고, `v = ii.values`
#   가 `{}` 가 되어 `v["cmb_pressure"]` 에서 `KeyError` 로 죽는다. 지구는 갈래 1 이라 살아서
#   **한 판에서 한 갈래만 죽는 모양**이었다.
#   ⚠ **프리셋으로 물러서는 주체는 이름이 아니라 `core_mass_fraction` 이다** (`interior.py` 의
#   `preset_cmf` 는 그 인자가 `None` 일 때만 읽힌다). 그러므로 **cmf 를 명시로 넘기는 한**
#   이 이름이 `earth_like` 여도 0.325 로 물러서지 않는다. 출처는 아래 `_composition()` 이 낸
#   `cmf_source` 가 말하고, **그 줄은 인쇄된다**.
ENGINE_COMPOSITION = "earth_like"


def _composition(body: dict, t_pot: float) -> tuple[float, str]:
    """핵질량비와 그 출처를 세 갈래로 얻는다 — 선언 · 역산 · 이름 대는 정지.

    `.get` 으로 눅여 `None` 을 흘리지 않는다. ⚠ **두 `solve` 가 `None` 을 다르게 다룬다** —
    `interior.solve` 는 거절하지 않고 **프리셋 0.325(지구)로 조용히 물러서고**, `core_history.solve`
    (`ch.solve`) 는 `NO_CORE` 로 거절한다. 앞쪽이 더 위험하다: 거절은 눈에 띄지만 프리셋은 안 띈다."""
    declared = body.get("core_mass_fraction")
    if declared is not None:
        return float(declared), "바디가 선언한 핵질량비"
    res = infer_composition(float(body["mass_earth"]), float(body["radius_earth"]),
                            ice_allowed=False, potential_temperature=t_pot)
    cmf = res.values.get("core_mass_fraction", res.inputs.get("core_mass_fraction"))
    if cmf is None:
        raise SystemExit(
            f"  [STOP] 핵질량비를 못 얻었다 — 이 바디는 선언이 없고"
            f" (`core_mass_fraction` 키 없음, 질량 {body['mass_earth']} · 반지름"
            f" {body['radius_earth']} R⊕), `infer_composition` 도 값을 안 냈다"
            f" (regime {res.regime} · {res.reason or '사유 문장 없음'})."
            f" 이 스윕은 그 값을 전제하므로 인쇄하지 않는다")
    return float(cmf), "역산이 푼 핵질량비 (선언 없음)"


def say(msg: str) -> None:
    print(msg, flush=True)


def build(body: dict, t_pot: float, core_init: float) -> tuple[dict, float, float]:
    """The same `params` dict **`core_history.solve`** (`ch.solve`) builds, plus the two initial
    temperatures (mantle = core/r_b). ⚠ Not `interior.solve`, which this function *calls* as
    `isolve` — the two take different arguments and the names sat one line apart."""
    # ⚠ **핵질량비는 «풀린 상태»에서 읽고, 그 값의 출처를 같이 들고 다닌다** (2026-09-20).
    #   `_composition()` 이 세 갈래를 가르고, 여기서는 그것이 낸 수를 넘긴다. `radius_earth` 도
    #   같이 넘긴다 — 안 넘기면 풀 것이 없어 프리셋으로 물러서고, 그게 이 항목이 고친 결함이다.
    cmf, _cmf_source = _composition(body, t_pot)
    ii = isolve(mass_earth=body["mass_earth"], core_mass_fraction=cmf,
                radius_earth=body["radius_earth"], composition=ENGINE_COMPOSITION,
                body_class="rocky", potential_temperature=t_pot)
    # ⚠ **거절은 `values` 를 안 싣는다.** 여기서 안 보면 다음 줄이 `KeyError` 로 죽고, 인쇄는
    #   「키가 없다」고 말하는데 실제 원인은 **엔진이 이 입력을 거절했다** 이다.
    if "cmb_pressure" not in ii.values:
        raise SystemExit(f"  [STOP] interior.solve 가 이 입력을 안 받았다 — regime {ii.regime}"
                         f" · {ii.reason or '사유 문장 없음'}."
                         f" 아래 줄들이 읽는 `cmb_pressure` 가 결과에 없다")
    # ⚠ **출처와 `regime` 을 한 줄에 같이 찍는다.** 수가 어디서 왔는지와 엔진이 그 입력을 받았는지는
    #   다른 사실이고, 둘이 떨어져 있으면 「역산이 값을 냈다」를 「스윕이 돌았다」로 읽게 된다 —
    #   이 항목이 한 번 그렇게 틀렸다. `regime` 이 `out-of-domain` 이면 위 줄에서 이미 멈춘다.
    say(f"  [출처] {body['mass_earth']} M⊕ — 핵질량비 {cmf!r} · {_cmf_source} · regime {ii.regime}")
    v = ii.values
    m_kg = body["mass_earth"] * cf.M_EARTH_KG
    r_p = body["radius_earth"] * cf.R_EARTH_M
    params = {"material": "fe_prem", "p_cmb": v["cmb_pressure"] * 1e9, "r_cmb": v["core_radius"] * cf.R_EARTH_M,
              "m_core": m_kg * cmf, "m_mantle": m_kg * (1.0 - cmf),
              "r_b": v["cmb_temperature"] / t_pot,
              "g": cf.G_NEWTON * m_kg / r_p ** 2, "r_p": r_p, "h_core": H_NIMMO,
              "h_m_present_w": rg.budget(m_kg * (1.0 - cmf))["mantle_w"],
              "t_surface_k": mf.T_S}   # 픽스처: 모듈 값을 명시로 (레시피는 바디 선언을 읽는다)
    # ⚠ **이 줄은 기록이지 시험이 아니다** (2026-09-20, 감사석이 자를 뒤집어 보임). 위 `[출처]`
    #   줄이 찍는 것은 역산이 **돌려준** 수 그대로이고, 아래는 질량 둘로 되돌려 나눈 수다.
    #   ⚠ **「되돌린 값 == 인쇄값」을 수락선으로 쓰면 안 된다 — 그 자는 뒤집혀 있다.**
    #   m_kg = 6.413928e+23 에서 참값 `0.23958333333333331` 은 `0.2395833333333333` 로 돌아와
    #   **안 맞고**, 틀린 값 `0.24` 와 `0.325` 는 **정확히 맞는다**. 손실은 나눗셈이 아니라
    #   `1.0 - cmf` 에서 나고 (`1.0 - (1.0 - cmf) != cmf`), 대수로 고쳐 쓸 수 없다.
    #   ⚠ **`m_core + m_mantle == m_kg` 도 자가 아니다** — 어떤 cmf 에서도 참이다.
    #   그래서 차를 **감추지도 판정하지도 않고 그대로 찍는다.** 어긋남이 커지면 눈에 보이고,
    #   그때 그것이 어디서 났는지 이 줄이 말한다.
    _back = params["m_core"] / (params["m_core"] + params["m_mantle"])
    say(f"  [검산] 질량 둘로 되돌린 핵질량비 {_back!r} · 인쇄값과의 차 {_back - cmf!r}")
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
    # ⚠ 최근접 표본 행이 아니라 **보간** 이다 (2026-09-19, 사전등록 ec974a1d) — 걸음 상한을
    #   바꿔도 이 칸이 안 움직인다. 그래서 `t_37_actual` 은 표본 시각이 아니라 **요청한 시각**이다.
    near_t_m = ch.t_at_gyr(rows, CHECKPOINT_GYR)
    out = {"n": hist["n_steps"], "t_p": last["t_m"], "t_c": last["t_c"], "t_p_37": near_t_m,
           "t_37_actual": CHECKPOINT_GYR, "seconds": time.time() - t0}
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
