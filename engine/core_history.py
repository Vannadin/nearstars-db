# 맨틀·핵 결합 열진화 적분기 (C20) — Nimmo+ 2004 식 30·32 를 시간 앞으로 적분해 T_c(t)·T_m(t)·ΔE(t) 를 낸다
"""Core thermal history — the C20 integrator.

Grounding: `docs/reference/internal-heat-luminosity-methodology.md` and Nimmo+ 2004
(`2004GeoJI.156..363N`). Pre-registration and the fixed design: `engine/core-thermal-history-context-notes.md`.

    core   (eq. 30)   Q_R − Q_C = (Q̃_s + Q̃_L + Q̃_g) · dT_c/dt
    mantle (eq. 32)   H_m M_m − Q_M + Q_C = M_m C_pm · dT_h/dt
    Q_C = 4π R_c² F_b  (eqs 37–39, `cmb_flux.bottom_layer`)     Q_M = 4π R_p² F_t  (eqs 34–36, `mantle_flux.implied_flux`)
    T̃_m = r_b · T_m   T_h = r_b^½ · T_m   (eq. 29's form; r_b read from the interior solve at the reference T_pot)

State (T_c, T_m); classical RK4 in time; the step is h = min(4 Myr, 0.1·τ) with Nimmo's own 4 Myr as the cap
(Brief 157; τ is the mantle time constant). The Q̃ coefficients come from
`core_energy.core_terms` at unit rate (they are linear in dT_c/dt); the inner core at each step is whatever
`core_energy.inner_core` finds on that step's profile. Entropy production at each step from
`core_entropy.entropy_terms` with the COMPUTED rate, on the four (k × H) corners — the declared-rate axis of
C15's eight corners is what this module computes, so its band is not comparable to C15's.

What this module does not claim: any body's "actual" value (the model is Earth-calibrated: outputs read
"consistent with an Earth-calibrated model"); the short-lived radiogenic pulse (C21, needs t_form); t_form
for anyone. Radiogenic heating here is the long-lived half (K · Th · U) through `radiogenic.history_factor`.

Convergence is pre-registered as the discriminating check: the quantity that must converge is ΔE_min over
the last 3.1 Gyr — not the endpoint T_c — at h, h/2, h/4, with |ΔE_min(h/4) − ΔE_min(h/2)| < 10 % of
|ΔE_min(h/2)| and the same inner-core case at all three steps. A run that fails it reports the step as the
result, not the physics.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cmb_flux as cf            # noqa: E402
import core_energy as ce         # noqa: E402
import core_entropy as cent      # noqa: E402
import mantle_flux as mf         # noqa: E402
import mantle_budget as mb      # noqa: E402  — 결정 8: 정체뚜껑 바디의 손실 법칙
import tectonic_regime as tect  # noqa: E402  — 선언을 읽는 **하나뿐인** 독자 (C53)
import radiogenic as rg          # noqa: E402
from eos import PhaseGap         # noqa: E402
from payload import Result, out_of_domain  # noqa: E402

RECIPE = "internal-heat-luminosity-methodology"
VERSION = "1"
REFS = (
    "docs/reference/internal-heat-luminosity-methodology.md",
    "2004GeoJI.156..363N",      # Nimmo+ 2004 — eqs 29–39 (thermal evolution), §3.2, Tables 2, 4; 4 Myr step (line 419)
    "engine/core-thermal-history-context-notes.md",
)

GYR_S = ce.GYR_S
STEP_MYR = 4.0                      # Nimmo's constant timestep ("a constant timestep of 4 Myr", their line 419)
WINDOW_GYR = 3.1                    # Nimmo's entropy-criteria window: mean and minimum over the last 3.1 Gyr
CONVERGENCE_TOL = 0.10              # pre-registered: |ΔE_min(h/4) − ΔE_min(h/2)| / |ΔE_min(h/2)| < 10 %
K_CORNERS = cf.K_CORE_RANGE         # (30, 70) W/(m K)
H_CORNERS = ce.H_CORE_RANGE         # (0, 0.088e-12) W/kg — owner decision ⑤ 2026-09-09 as corrected by
                                    # Brief 166 E; was (0, 0.14e-12) for one afternoon, (0, 1.5e-12) before that.
                                    # ⚠ This comment mirrors a constant declared elsewhere and it went stale once
                                    # already — C52's disease, caught by that item's closing sweep.
ROCKY_ONLY = ("giant", "gas_giant", "ice_giant", "sub_neptune", "brown_dwarf", "star")

NO_INITIAL = ("cannot-say (no initial temperatures declared — core_initial_temperature and "
              "mantle_initial_potential_temperature are the two declarations this integrator adds)")
NO_STRUCTURE = "cannot-say (no interior solution — needs core_radius, cmb_pressure, cmb_temperature, potential_temperature)"
#: 결정 8 — 정체뚜껑 법칙은 표면온도를 쓴다. 기본값은 지구의 273 K 이고, 그것을 다른 천체에
#: 조용히 대입하면 ΔT 가 두 번 들어가는 식에서 바로 값이 된다. **선언 없이는 안 돈다.**
NO_SURFACE_T = ("cannot-say (두 손실 법칙 다 표면온도를 쓰는데 surface_temperature_k 가 없거나 "
                "유한한 수가 아니다 — 모듈 기본값(Nimmo 293 K · Foley 273 K, 둘 다 지구)을 "
                "다른 천체에 대입하지 않는다)")
#: 결정 8 — 정체뚜껑인데 뚜껑 두께가 없으면 법칙을 못 고른다. **기본값으로 때우지 않는다**:
#: Nimmo 로 돌리면 그 바디는 자기 영역과 다른 법칙으로 식고, 아무도 그 사실을 안 읽는다.
NO_LID = ("cannot-say (tectonic_regime 이 stagnant 인데 lid_thickness_km 선언이 없다 — "
          "Foley 2018 eq. (3) 은 뚜껑 두께 δ 를 받아야 하고, 없는 값을 기본값으로 만들지 않는다)")
NOT_CONVERGED = "step-not-converged (the step is the result, not the physics — pre-registered branch ⑤ fail)"
CANNOT_SAY_HISTORY = "cannot-say (the four-corner band straddles zero inside the last 3.1 Gyr — C20 built, C15 still cannot say)"
SUSTAINED = "sustained (ΔE_min > 0 over the last 3.1 Gyr on all four k × H corners)"
FAILS = "fails (ΔE_min < 0 somewhere in the last 3.1 Gyr on all four corners)"
CONDITION = ("Earth-calibrated model: Nimmo+ 2004 eqs 30 and 32 integrated with RK4 at h = min(4 Myr, 0.1·τ) — Nimmo's "
             "4 Myr is the cap and τ the mantle time constant (Brief 157) — on the state "
             "(T_c, T_m); the mantle base temperature by the interior solve's own adiabat ratio (eq. 29's form); "
             "long-lived radiogenic heat only (K·Th·U, history factor); two new declarations (initial T_c, T_m); "
             "the result stands on ≈24 declarations in all — outputs read 'consistent with an Earth-calibrated model'")


def _core_side(material: str, p_cmb: float, t_c: float, r_cmb: float, m_core: float) -> dict:
    """Profile and rate coefficients at T_c. Q̃ = Q(dT_c/dt = −1 K/s) since Q_s, Q_L, Q_g are linear in the rate."""
    prof = ce.core_profile(material, p_cmb, t_c, r_cmb, m_core)
    # h = 0 deliberately: `core_terms`' h feeds Q_R only, and Q̃ below is Q_s + Q_L + Q_g. Until Brief 166 D this
    # read `ce.H_CORE` and threw the result away — inert, but it read as a second place the integrator takes H from.
    # The one path that reaches the answer is `params["h_core"]` in `rates`, which is why the caller can set it.
    unit = ce.core_terms(prof, dtc_dt=-1.0, h=0.0)
    # Heat released per unit cooling rate, positive: Q_s + Q_L + Q_g evaluated at dT_c/dt = −1 K/s.
    # (Nimmo's Q̃ carries the opposite sign; the physics is Q_C − Q_R = −Q̃_abs · dT_c/dt, cooling when Q_C > Q_R.)
    q_tilde = unit["q_s"] + unit["q_l"] + unit["q_g"]
    return {"prof": prof, "q_tilde": q_tilde, "inner_core": unit["inner_core"], "m_core": prof["m"][0],
            "core_status": unit.get("core_status", "inner_core")}


def rates(t_c: float, t_m: float, p: dict, t_gyr_from_present: float) -> dict:
    """dT_c/dt and dT_m/dt [K/s] at state (T_c, T_m) and epoch t (Gyr, negative = past)."""
    t_m_base = p["r_b"] * t_m
    side = _core_side(p["material"], p["p_cmb"], t_c, p["r_cmb"], p["m_core"])
    # Nimmo starts both at 4800 K (Fig. 2 caption): zero jump at t = 0. F_b ∝ ΔT^(4/3) → 0 continuously (eqs 37–38),
    # so Q_C = 0 for ΔT ≤ 0 is the continuous limit, not a patch. The mantle cools first; the core follows.
    notes = []
    if t_c > t_m_base:
        bl = cf.bottom_layer(t_c, t_m_base, p["r_cmb"])
        if bl["domain_refusal"] is not None:      # Brief 155: the callee refused; the integrator stops here by name
            return {"refused": bl["domain_refusal"]}
        q_c = bl["q_c_w"]
        if bl["extrapolation_note"]:
            notes.append(bl["extrapolation_note"])
    else:
        q_c = 0.0
    q_r = side["m_core"] * p["h_core"]
    dtc = -(q_c - q_r) / side["q_tilde"]          # K/s; negative = cooling
    # 결정 8 — 맨틀이 위로 버리는 열을 **그 바디의 영역이 고른 법칙**으로 낸다. 법칙 이름은
    # `params` 에 실려 오므로 어느 실행도 자기가 쓴 법칙을 숨길 수 없다 (사전등록 수락선 G).
    if p.get("loss_law") == "foley":
        # eq. (3) 은 **뚜껑 바닥**을 지나는 flux 다. 면적도 그 반지름의 것이어야 한다 — 표면적을
        # 쓰면 δ 350→500 km 에서 −9.6 % 가 조용히 섞인다 (사전등록 함정 3).
        delta = p["delta_m"]
        r_lid = p["r_p"] - delta
        # ⚠ **표면온도도 이 바디의 것이어야 한다.** `g` 와 `d_m` 만 넘기고 `T_s` 를 기본값에
        # 맡기면 **손이 셋 중 둘만 닿은 비대칭**이고, 그 기본값은 지구의 273 K 다. `F_man ∝
        # (T_p − T_s)·Ra^(1/3)` 이라 ΔT 가 두 번 들어가므로 작은 칸이 아니다 — 그래서 선언을
        # 요구하고, 없으면 위에서 이름 대며 거절한다 (`NO_SURFACE_T`).
        f_man = mb.f_man_w_m2(t_m, t_s_k=p["t_surface_k"], d_m=p["d_mantle_m"] - delta, g=p["g"])
        q_m = f_man * 4.0 * math.pi * r_lid ** 2
    else:
        top = mf.implied_flux(t_m, p["g"], p["r_p"], t_s=p["t_surface_k"])
        if top["domain_refusal"] is not None:
            return {"refused": top["domain_refusal"]}
        q_m = top["q_m_w"]
        if top["extrapolation_note"]:
            notes.append(top["extrapolation_note"])
    h_m = p["h_m_present_w"] * rg.history_factor(t_gyr_from_present)
    dtm = (h_m - q_m + q_c) / (p["m_mantle"] * mf.C_PM * math.sqrt(p["r_b"]))
    return {"dtc": dtc, "dtm": dtm, "q_c": q_c, "q_m": q_m, "h_m": h_m, "q_r": q_r, "side": side,
            "extrapolation_notes": tuple(notes)}


def t_at_gyr(rows: list[dict], t_gyr: float, key: str = "t_m") -> float:
    """`rows` 를 시간으로 선형 보간해 `t_gyr` 에서의 값을 낸다 — 표본 격자와 무관한 읽기.

    ⚠ **왜 최근접 행이 아니라 보간인가.** 예전에는 호출자들이 `min(rows, key=|t_gyr − t|)` 로
    **가장 가까운 표본 행**을 골랐고, 그러면 **걸음 상한을 바꾸면 값이 움직였다** — 3.7 Ga 칸에서
    4 → 1 Myr 로 촘촘히 하면 **±0.17 K**, 기준 B 여유 4.36 K 의 4 % 다 (2026-09-18 측정).
    보간은 그 흔들림을 없앤다. ⚠ **그래서 이 함수가 내는 수는 옛 수와 다르다** — 규칙이 바뀐
    것이지 궤적이 바뀐 것이 아니고, 그 사실은 인용하는 쪽이 적는다.

    ⚠ 범위 밖이면 이름 대며 거절한다. 양 끝은 그 끝의 값을 돌려주지 않는다 — 없는 시점을
    있는 것처럼 만들지 않기 위해서다.

    ⚠ **거절이 `ValueError` 인 이유.** 한 커밋 전(`91f5440b`)이 뚜껑 정의역에 `LidOutsideMantle`
    을 새로 만든 것은 «`ValueError` 를 다른 뜻으로 잡는 코드가 삼킨다» 였다. 여기서는 그 위험이
    없다 — 호출 셋이 시험·도구이고 그 경로에 넓은 `except` 가 없다. 도메인이 타입을 새로 만들
    만큼 크지도 않다. 위험이 생기면 그때 타입을 만든다."""
    if not rows:
        raise ValueError("t_at_gyr: rows 가 비었다")
    xs = [r["t_gyr"] for r in rows]
    lo, hi = min(xs), max(xs)
    if not (lo <= t_gyr <= hi):
        raise ValueError(f"t_at_gyr: t = {t_gyr:+.4f} Gyr 이 이력 [{lo:+.4f}, {hi:+.4f}] 밖이다")
    prev = rows[0]
    for row in rows[1:]:
        a, b = prev["t_gyr"], row["t_gyr"]
        if (a - t_gyr) * (b - t_gyr) <= 0.0:
            if b == a:
                return float(row[key])
            w = (t_gyr - a) / (b - a)
            return float(prev[key]) + w * (float(row[key]) - float(prev[key]))
        prev = row
    # ⚠ 위 범위 검사를 지나면 **여기 못 온다** — 어떤 쌍이든 브래킷되기 때문이다. 온다면 `rows`
    #   가 시간순이 아니라는 뜻이고, 끝 행을 조용히 돌려주면 **틀린 값이 답처럼 나간다**.
    raise ValueError("t_at_gyr: rows 가 시간순이 아니다 — 브래킷을 못 찾았다")


MYR_S = GYR_S / 1000.0
STEP_FRACTION = 0.1                 # F in h = min(STEP_MYR, F·τ) — Brief 157, tools/adaptive-step-prereg.md: 1/28 of RK4's
                                    # real-axis limit 2.78, 1/10 of the h/τ ≈ 1.02 Earth's first fixed step already passed


def mantle_time_constant_s(params: dict, t_m: float) -> float | None:
    """τ = C_eff / (dQ_m/dT_m) at the current mantle state [s] — the linearised relaxation time of eq. 32's
    stiff term. C_eff is dT_m/dt's own denominator (m_mantle·C_pm·√r_b); dQ_m/dT_m is a ±1 K central
    difference of eqs 34–36. None when the law refuses on either side (the caller then uses the cap)."""
    hi = mf.implied_flux(t_m + 1.0, params["g"], params["r_p"])
    lo = mf.implied_flux(t_m - 1.0, params["g"], params["r_p"])
    if hi["q_m_w"] is None or lo["q_m_w"] is None:
        return None
    dq = (hi["q_m_w"] - lo["q_m_w"]) / 2.0
    if dq <= 0.0:
        return None
    return params["m_mantle"] * mf.C_PM * math.sqrt(params["r_b"]) / dq


def integrate(params: dict, t_c0: float, t_m0: float, age_gyr: float, step_myr: float = STEP_MYR,
              adaptive: bool = True) -> dict:
    """RK4 from t = −age to 0. Returns the sampled history (one row per step) and the entropy corners per row.

    Brief 157: the step is `h = min(step_myr, STEP_FRACTION · τ(state))`, τ recomputed at the start of every
    step from `mantle_time_constant_s`; `step_myr` is the CAP (Nimmo's constant 4 Myr, their line 419).
    `adaptive=False` reproduces the fixed-step integrator bit for bit (Earth anchor 1525.46 K, 1135 steps, **at
    Nimmo's H 1.5 pW/kg** — `params["h_core"]`, not a constant of this module, Brief 166 D) and
    is what the Mars divergence test uses. The result carries `n_steps`, `h_min_myr` and `max_h_over_tau`."""
    n_fixed = max(1, int(round(age_gyr * 1000.0 / step_myr)))
    h_fixed = age_gyr * GYR_S / n_fixed
    cap_s = step_myr * MYR_S
    t_c, t_m = float(t_c0), float(t_m0)
    t_now = -age_gyr                                  # Gyr from present (≤ 0)
    rows = []
    extrapolated = {"eqs 34–36": 0, "eqs 37–39": 0}
    n = 0
    h_min = None
    max_ratio = 0.0

    def refused(reason: str) -> dict:
        return {"refused": reason, "rows": rows, "n_steps": n, "step_myr": step_myr,
                "refused_at": {"t_gyr": t_now, "t_c": t_c, "t_m": t_m}}

    while True:
        r1 = rates(t_c, t_m, params, t_now)
        if "refused" in r1:
            return refused(r1["refused"])
        for note in r1["extrapolation_notes"]:
            extrapolated["eqs 34–36" if "eqs 34–36" in note else "eqs 37–39"] += 1
        side = r1["side"]
        corners = {}
        for k in K_CORNERS:
            for hh in H_CORNERS:
                unit = ce.core_terms(side["prof"], dtc_dt=r1["dtc"], h=hh)
                corners[(k, hh)] = cent.entropy_terms(side["prof"], unit, r1["dtc"], hh, k)["delta_e"]
        ic = side["inner_core"]
        rows.append({"t_gyr": t_now, "t_c": t_c, "t_m": t_m, "dtc_dt_k_gyr": r1["dtc"] * GYR_S,
                     "q_c_w": r1["q_c"], "q_m_w": r1["q_m"], "h_m_w": r1["h_m"],
                     "r_i_km": (ic["r_i"] / 1e3) if ic else 0.0, "core_status": side["core_status"],
                     "delta_e_corners": corners,
                     "delta_e_min_corner": min(corners.values()), "delta_e_max_corner": max(corners.values())})
        if adaptive:
            remaining = -t_now * GYR_S
            if remaining <= 1e-9 * GYR_S:
                break
            tau = mantle_time_constant_s(params, t_m)
            h = cap_s if tau is None else min(cap_s, STEP_FRACTION * tau)
            if tau is not None:
                max_ratio = max(max_ratio, h / tau)
            if h >= remaining:
                h = remaining                          # land exactly on the present
            t_next = 0.0 if h == remaining else t_now + h / GYR_S
        else:
            if n == n_fixed:
                break
            h = h_fixed
            t_next = -age_gyr + (n + 1) * age_gyr / n_fixed
        h_min = h if h_min is None else min(h_min, h)
        # classical RK4 on (T_c, T_m)
        k1 = (r1["dtc"], r1["dtm"])
        r2 = rates(t_c + 0.5 * h * k1[0], t_m + 0.5 * h * k1[1], params, t_now + 0.5 * h / GYR_S)
        if "refused" in r2:
            return refused(r2["refused"])
        k2 = (r2["dtc"], r2["dtm"])
        r3 = rates(t_c + 0.5 * h * k2[0], t_m + 0.5 * h * k2[1], params, t_now + 0.5 * h / GYR_S)
        if "refused" in r3:
            return refused(r3["refused"])
        k3 = (r3["dtc"], r3["dtm"])
        r4 = rates(t_c + h * k3[0], t_m + h * k3[1], params, t_now + h / GYR_S)
        if "refused" in r4:
            return refused(r4["refused"])
        k4 = (r4["dtc"], r4["dtm"])
        t_c += h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0
        t_m += h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
        t_now = t_next
        n += 1
    return {"rows": rows, "n_steps": n, "step_myr": step_myr, "adaptive": adaptive,
            "h_min_myr": (h_min / MYR_S) if h_min is not None else None,
            "max_h_over_tau": max_ratio if adaptive else None, "extrapolated_steps": extrapolated}


def window_summary(rows: list[dict], window_gyr: float = WINDOW_GYR) -> dict:
    """ΔE statistics over the last `window_gyr` on each corner, and the nucleation epoch."""
    win = [r for r in rows if r["t_gyr"] >= -window_gyr - 1e-9]
    corners = list(win[0]["delta_e_corners"].keys())
    per_corner = {}
    for c in corners:
        vals = [r["delta_e_corners"][c] for r in win]
        per_corner[c] = {"min": min(vals), "mean": sum(vals) / len(vals), "present": vals[-1],
                         "t_min_gyr": win[min(range(len(vals)), key=lambda i: vals[i])]["t_gyr"]}
    mins = [v["min"] for v in per_corner.values()]
    if all(m > 0.0 for m in mins):
        verdict = SUSTAINED
    elif all(m < 0.0 for m in mins):
        verdict = FAILS
    else:
        verdict = CANNOT_SAY_HISTORY
    nucleation = next((r["t_gyr"] for r in rows if r["r_i_km"] > 0.0), None)
    always = rows[0]["r_i_km"] > 0.0
    return {"per_corner": per_corner, "delta_e_min_band": (min(mins), max(mins)), "verdict": verdict,
            "nucleation_t_gyr": nucleation, "inner_core_from_start": always,
            "inner_core_case": ("always" if always else "never" if nucleation is None else "nucleates")}


def sweep(params: dict, t_c0: float, t_m0: float, age_gyr: float, step_myr: float = STEP_MYR) -> dict:
    """h, h/2, h/4 — the pre-registered convergence test on ΔE_min (nominal corner) and the inner-core case.

    ⚠ **Fixed step, deliberately** (`adaptive=False`). Branch ⑤ was registered before the adaptive step
    existed (`core-thermal-history-context-notes.md@«⑤ Step convergence — *declare the test before the first run*»`),
    and it halves the STEP. Left adaptive, halving `step_myr` only lowers the CAP in `h = min(cap, 0.1·τ)`
    and changes nothing where τ binds — a different question, and one nobody registered. Restoring the
    original meaning was Brief 161's first item; **an adaptive-cap sweep is not built here** (C47 (i))."""
    out = {}
    for label, s in (("h", step_myr), ("h/2", step_myr / 2.0), ("h/4", step_myr / 4.0)):
        hist = integrate(params, t_c0, t_m0, age_gyr, s, adaptive=False)
        if "refused" in hist:
            return {"refused": hist["refused"], "h/4": {"hist": hist}}
        ws = window_summary(hist["rows"])
        nominal = (cf.K_CORE, ce.H_CORE)
        vals = [r["delta_e_corners"][nominal] if nominal in r["delta_e_corners"] else None for r in hist["rows"]]
        # the nominal (k 50, H 0.14) point is not a corner; use the k = 70, H 0.14 corner's ΔE_min as the convergence quantity
        # and the band ends, all three must move together
        out[label] = {"hist": hist, "summary": ws,
                      "delta_e_min_lo": ws["delta_e_min_band"][0], "delta_e_min_hi": ws["delta_e_min_band"][1],
                      "t_c_present": hist["rows"][-1]["t_c"], "t_m_present": hist["rows"][-1]["t_m"],
                      "case": ws["inner_core_case"]}
    a, b = out["h/2"], out["h/4"]
    widths = []
    for key in ("delta_e_min_lo", "delta_e_min_hi"):
        ref = abs(b[key]) if abs(b[key]) > 0 else 1.0
        widths.append(abs(b[key] - a[key]) / ref)
    same_case = out["h"]["case"] == out["h/2"]["case"] == out["h/4"]["case"]
    out["converged"] = max(widths) < CONVERGENCE_TOL and same_case
    out["convergence_width"] = max(widths)
    out["same_inner_core_case"] = same_case
    return out


def solve(mass_earth: float, core_mass_fraction: float | None, core_radius_earth: float | None,
          cmb_pressure_gpa: float | None, cmb_temperature: float | None, potential_temperature: float | None,
          radius_earth: float | None, age_gyr: float | None, core_initial_temperature: float | None,
          mantle_initial_potential_temperature: float | None, core_material: str = "fe_prem",
          body_class: str | None = None, tectonic_regime=None,
          lid_thickness_km=None, legacy_stagnant_lid=None, surface_temperature_k=None,
          run_sweep: bool = False) -> Result:
    inputs = {"mass_earth": mass_earth, "core_mass_fraction": core_mass_fraction, "core_radius": core_radius_earth,
              "cmb_pressure": cmb_pressure_gpa, "cmb_temperature": cmb_temperature,
              "potential_temperature": potential_temperature, "radius_earth": radius_earth, "age_gyr": age_gyr,
              "core_initial_temperature": core_initial_temperature,
              "mantle_initial_potential_temperature": mantle_initial_potential_temperature,
              "core_material": core_material, "body_class": body_class,
              "tectonic_regime": tectonic_regime, "lid_thickness_km": lid_thickness_km,
              "surface_temperature_k": surface_temperature_k,
              "step_myr": STEP_MYR, "step_fraction": STEP_FRACTION, "core_h_w_per_kg": ce.H_CORE}
    if body_class in ROCKY_ONLY:
        return out_of_domain(RECIPE, VERSION, f"'{body_class}' 에는 규산염 맨틀·금속 핵의 결합 열진화가 뜻이 없다 — 암석체의 것이다.",
                             inputs=inputs, refs=REFS)
    if not core_radius_earth or not core_mass_fraction or core_mass_fraction <= 0.0:
        return out_of_domain(RECIPE, VERSION, cf.NO_CORE, inputs=inputs, refs=REFS)
    if None in (cmb_pressure_gpa, cmb_temperature, potential_temperature, radius_earth, age_gyr):
        return out_of_domain(RECIPE, VERSION, NO_STRUCTURE, inputs=inputs, refs=REFS)
    if core_initial_temperature is None or mantle_initial_potential_temperature is None:
        return out_of_domain(RECIPE, VERSION, NO_INITIAL, inputs=inputs, refs=REFS)
    # 결정 8 — 영역이 법칙을 고른다. `mobile` 과 **미선언**은 둘 다 Nimmo 로 가는데, 그것은
    # ⚠ **증거가 아니라 엔진이 돌릴 수 있는 것**이다: 지구·판도라가 `mobile` 이고 판도라에는
    # 인쇄된 뚜껑 밴드가 아예 없다. 그 사실을 여기 적어 둬야 나중에 「판정했다」로 안 읽힌다.
    # ⚠ **독자는 하나다.** `tectonic_regime` 을 여기서 따로 풀지 않고 `tectonic_regime` 모듈의
    # 기존 경로를 그대로 부른다 — 맨 스칼라·옛 `stagnant_lid` 병존·어휘 밖 값의 거절이 전부 거기
    # 있고(C53), 두 번째 독자를 만들면 **같은 바디를 `dynamo_rocky` 는 거절하고 이 노드는
    # 통과시키는** 일이 생긴다. 거절은 그 이유 문장을 그대로 싣는다 — 조용히 nimmo 로 떨어지지
    # 않게 하는 것이 이 항목의 요점이다.
    m_kg = mass_earth * cf.M_EARTH_KG
    r_p = radius_earth * cf.R_EARTH_M
    # ⚠ 맨틀 두께는 **한 번만** 센다 — 가드와 `params` 가 각자 계산하면 대수적으로 같아도
    # 부동소수 마지막 자리가 갈린다.
    d_mantle_m = r_p - core_radius_earth * cf.R_EARTH_M

    # ⚠ **독자는 하나고, 표도 하나다.** 영역→법칙은 여기서 다시 적지 않고 `tectonic_regime` 의
    # `DERIVED` 결과에서 한 줄로 유도한다 — `True`(stagnant·contested) → Foley, `False`(mobile)
    # → Nimmo, `None`(transitional) 과 매핑 없는 값(episodic·heat_pipe)과 미선언은 **그 모듈의
    # 거절 문구를 그대로 싣고 멈춘다**. ⚠ `contested` 가 Foley 로 가는 것은 **오너 결정 (a) 를
    # 물려받은 것**이지 이 노드가 새로 판단한 것이 아니다.
    # ⚠ **사전등록과 갈리는 칸**: 등록은 「미선언 → Nimmo」였는데 `tect` 는 「판정 불가는
    # 기본값이 아니다」로 거절한다. 두 문장이 같이 참일 수 없어 C53 쪽을 따랐다 — 오늘 로스터에는
    # 미선언 암석체가 없어 값 영향은 0 이고, 이탈은 착지 기록에 적는다.
    derived = tect.derived_stagnant_lid(tectonic_regime, legacy_stagnant_lid)
    if derived.refusal is not None:
        return out_of_domain(RECIPE, VERSION, f"cannot-say ({derived.refusal})", inputs=inputs, refs=REFS)
    # ⚠ **미선언과 「선언됐는데 매핑이 없다」를 가른다.** `tect` 는 둘 다 `value None` 으로 내지만
    # 뜻이 다르다. 선언이 **아예 없는** 바디는 그래도 식어야 하고, 그 갈래를 거절로 만들면
    # 영역을 선언한 적 없는 모든 암석체가 C20 을 잃는다 — 이 파일의 기존 `solve()` 호출들이
    # 그것으로 죽는 것을 실측했다. 그래서 **미선언 → Nimmo**(사전등록 `0bbb3ad0` §1 그대로),
    # **선언됐으나 `transitional`·매핑 없음 → 그 모듈의 문구로 거절**.
    # ⚠ C53 의 「판정 불가는 기본값이 아니다」는 **다이나모 불리언**에 대한 문장이다. 여기서는
    # 「법칙을 못 고른다」가 아니라 「추가 선언 없이 도는 법칙이 Nimmo 다」이고, 그 사실은
    # §8b 와 `[증인·법칙]` 줄에 매번 인쇄된다.
    if tectonic_regime is None and legacy_stagnant_lid is None:
        # ⚠ **미선언과 `mobile` 은 출력에서 갈려야 한다.** 둘 다 Nimmo 로 가지만 뜻이 다르다 —
        # 하나는 「그렇게 선언했다」이고 하나는 「선언이 없어 기본 법칙으로 돈다」이다. 갈리지
        # 않으면 선언 빠진 바디가 선언한 바디처럼 읽힌다.
        derived = derived._replace(
            value=False,
            note="tectonic_regime 선언이 없다 — 추가 선언 없이 도는 법칙(Nimmo)으로 돈다. "
                 "이것은 이 바디의 영역에 대한 판정이 아니다")
    if derived.value is None:
        return out_of_domain(RECIPE, VERSION, f"cannot-say ({derived.note})", inputs=inputs, refs=REFS)
    lid_km = _declared_scalar(lid_thickness_km)
    lid_thickness_m = None if lid_km is None else lid_km * 1e3
    loss_law = "foley" if derived.value else "nimmo"
    if loss_law == "foley" and lid_thickness_m is None:
        return out_of_domain(RECIPE, VERSION, NO_LID, inputs=inputs, refs=REFS)
    # ⚠ **푼 뒤에 검사한다.** 원본만 보면 블록은 있는데 `value` 가 없거나 숫자가 아닌 판이
    # 이 검사를 **통과**하고, 법칙 안에서 이름 없는 `TypeError` 로 죽는다 — 우리가 세는 「이름
    # 없는 실패」다. 선언이 있다는 것과 쓸 수 있는 수라는 것은 다른 말이다.
    t_surface_k = _declared_scalar(surface_temperature_k)
    if not isinstance(t_surface_k, (int, float)) or isinstance(t_surface_k, bool) \
            or not math.isfinite(t_surface_k):
        return out_of_domain(RECIPE, VERSION, NO_SURFACE_T, inputs=inputs, refs=REFS)
    if loss_law == "foley":
        # ⚠ **이 길에는 뚜껑 가드가 없다.** `mantle_budget` 의 `LidOutsideMantle` 은
        # `dtp_dt_k_s`·`secular_cooling`·`integrate_tp` 에 걸려 있고, 우리가 부르는
        # `f_man_w_m2` 는 δ 를 아예 안 받는다 — 우리가 `d_m − δ` 를 **미리 빼서** 넘기므로
        # δ ≥ d_m 이면 0 이나 음수가 **조용히** 들어간다. `NO_LID` 는 「δ 없음」만 막는다.
        # 그래서 같은 정의역을 같은 문구로 여기서 다시 건다.
        if not (0.0 <= lid_thickness_m < d_mantle_m):
            return out_of_domain(RECIPE, VERSION,
                                 f"cannot-say ({mb._lid_domain_message(lid_thickness_m, d_mantle_m)})",
                                 inputs=inputs, refs=REFS)

    params = {"material": core_material, "p_cmb": cmb_pressure_gpa * 1e9, "r_cmb": core_radius_earth * cf.R_EARTH_M,
              "m_core": m_kg * core_mass_fraction, "m_mantle": m_kg * (1.0 - core_mass_fraction),
              "r_b": cmb_temperature / potential_temperature,
              "g": cf.G_NEWTON * m_kg / r_p ** 2, "r_p": r_p, "h_core": ce.H_CORE,
              "loss_law": loss_law, "delta_m": lid_thickness_m,
              "t_surface_k": t_surface_k,
              "d_mantle_m": d_mantle_m,
              "h_m_present_w": rg.budget(m_kg * (1.0 - core_mass_fraction))["mantle_w"]}
    try:
        if run_sweep:
            sw = sweep(params, core_initial_temperature, mantle_initial_potential_temperature, age_gyr)
            if "refused" in sw:
                return out_of_domain(RECIPE, VERSION, f"적분이 법칙의 선언 정의역 밖에서 시작하거나 그리로 갔다 — {sw['refused']}",
                                     inputs=inputs, refs=REFS)
            best = sw["h/4"]
            converged, width = sw["converged"], sw["convergence_width"]
        else:
            hist = integrate(params, core_initial_temperature, mantle_initial_potential_temperature, age_gyr)
            if "refused" in hist:
                return out_of_domain(RECIPE, VERSION, f"적분이 법칙의 선언 정의역 밖에서 시작하거나 그리로 갔다 — {hist['refused']}",
                                     inputs=inputs, refs=REFS)
            ws = window_summary(hist["rows"])
            best = {"hist": hist, "summary": ws, "t_c_present": hist["rows"][-1]["t_c"],
                    "t_m_present": hist["rows"][-1]["t_m"], "case": ws["inner_core_case"]}
            converged, width = None, None
    except (PhaseGap, ValueError) as e:
        return out_of_domain(RECIPE, VERSION, f"적분이 물리 범위를 벗어났다 — {e}", inputs=inputs, refs=REFS)

    rows = best["hist"]["rows"]
    ws = best["summary"]
    last = rows[-1]
    values = {
        "core_cmb_temperature_present": last["t_c"],
        "mantle_potential_temperature_present": last["t_m"],
        "dtc_dt_present_k_per_gyr": last["dtc_dt_k_gyr"],
        "q_cmb_present": last["q_c_w"],
        "q_mantle_present": last["q_m_w"],
        "inner_core_radius_present_km": last["r_i_km"],
        "inner_core_case": ws["inner_core_case"],
        "inner_core_nucleation_gyr_ago": (-ws["nucleation_t_gyr"]) if ws["nucleation_t_gyr"] is not None else None,
        "delta_e_min_3gyr_lo": ws["delta_e_min_band"][0],
        "delta_e_min_3gyr_hi": ws["delta_e_min_band"][1],
        "delta_e_present_lo": min(last["delta_e_corners"].values()),
        "delta_e_present_hi": max(last["delta_e_corners"].values()),
        "entropy_history_verdict": (ws["verdict"] if converged in (True, None) else NOT_CONVERGED),
        "history_converged": converged,
        "history_convergence_width": width,
        "history_steps": best["hist"]["n_steps"],
        "loss_law": loss_law,
        "loss_law_reason": derived.note,
    }
    units = {"core_cmb_temperature_present": "K", "mantle_potential_temperature_present": "K",
             "dtc_dt_present_k_per_gyr": "K/Gyr", "q_cmb_present": "W", "q_mantle_present": "W",
             "inner_core_radius_present_km": "km", "inner_core_case": "", "inner_core_nucleation_gyr_ago": "Gyr",
             "delta_e_min_3gyr_lo": "W/K", "delta_e_min_3gyr_hi": "W/K", "delta_e_present_lo": "W/K",
             "delta_e_present_hi": "W/K", "entropy_history_verdict": "", "history_converged": "",
             "history_convergence_width": "", "history_steps": "", "loss_law": "",
             "loss_law_reason": ""}
    if converged is None:
        values["history_converged"] = None   # the sweep is on demand (test_core_history.py --sweep); record: 2026-09-04 width 0.001 %
    mw = 1e6
    nuc = "" if ws["nucleation_t_gyr"] is None else f" ({-ws['nucleation_t_gyr']:.2f} Gyr 전)"
    reason = (f"Nimmo 식 30·32 를 {age_gyr:.2f} Gyr 동안 RK4 로 적분 (h = min({best['hist']['step_myr']:.2f} Myr, {STEP_FRACTION:g}·τ), "
              f"{best['hist']['n_steps']} 걸음{'' if converged is None else ', 수렴 폭 ' + format(width, '.1%')}). "
              f"현재 T_c {last['t_c']:.0f} K · T_m {last['t_m']:.0f} K · dT_c/dt {last['dtc_dt_k_gyr']:+.0f} K/Gyr · "
              f"Q_C {last['q_c_w']/1e12:.2f} TW · Q_M {last['q_m_w']/1e12:.1f} TW · 내핵 {ws['inner_core_case']}"
              f"{nuc} · "
              f"ΔE_min(3.1 Gyr) 네 모서리 {ws['delta_e_min_band'][0]/mw:+.0f}…{ws['delta_e_min_band'][1]/mw:+.0f} MW/K → "
              f"{values['entropy_history_verdict']}. 지구 보정 모형과의 일관성이지 이 천체의 실제 값이 아니다")
    ex = best["hist"].get("extrapolated_steps", {})
    n_steps = best["hist"]["n_steps"] + 1
    extrap_note = (f"⚠ declared extrapolation below the laws' expansion points (Brief 155): eqs 34–36 evaluated below "
                   f"T_0 = {mf.T_0:.0f} K on {ex.get('eqs 34–36', 0)} of {n_steps} sampled steps; eqs 37–39 evaluated at "
                   f"T_a below T_1 = {cf.T_1:.0f} K on {ex.get('eqs 37–39', 0)} of {n_steps}. Both laws' printed domain "
                   f"edge is 4800 K above and open below ({mf.EQ35_DOMAIN.anchor}); below the expansion point the paper "
                   "prints no limit, so the call is allowed and counted here rather than refused.")
    hist_ = best["hist"]
    step_note = (f"step (Brief 157): h = min({hist_['step_myr']:g} Myr, {STEP_FRACTION:g}·τ) with τ = C_eff/(dQ_m/dT_m) recomputed "
                 f"every step — {hist_['n_steps']} steps, smallest h {hist_['h_min_myr']:.4g} Myr, largest h/τ met "
                 f"{hist_['max_h_over_tau']:.3g} (must be ≤ {STEP_FRACTION:g}); tools/adaptive-step-prereg.md")
    return Result(recipe=RECIPE, version=VERSION, regime="thermal-history", reason=reason, grade="analog",
                  inputs=inputs, values=values, units=units, refs=REFS, notes=(CONDITION, extrap_note, step_note))


from registry import recipe  # noqa: E402


def _declared_scalar(declared):
    """선언 블록에서 스칼라 값을 꺼낸다 (`lid_thickness_km`·`surface_temperature_k`). ⚠ **여기는 맨 스칼라도 받는다** — 이 키에는
    엄격한 독자가 없고, 트리에 두 꼴이 같이 산다. 위 함수와 **일부러 다르고**, 다른 이유는
    「엄격한 독자가 이미 있느냐」 하나다."""
    if isinstance(declared, dict):
        return declared.get("value")
    return declared


@recipe("core_thermal_history")
def _from_state(state):
    return solve(mass_earth=state["mass_earth"], core_mass_fraction=state.get("core_mass_fraction"),
                 core_radius_earth=state.get("core_radius"), cmb_pressure_gpa=state.get("cmb_pressure"),
                 cmb_temperature=state.get("cmb_temperature"), potential_temperature=state.get("potential_temperature"),
                 radius_earth=state.get_optional("radius") or state.get_optional("radius_earth"),   # C45 (b): 선호-대체
                 age_gyr=state.get("age_gyr"),
                 core_initial_temperature=state.get("core_initial_temperature"),
                 mantle_initial_potential_temperature=state.get("mantle_initial_potential_temperature"),
                 core_material=state.get("core_material", "fe_prem"), body_class=state.get("body_class"),
                 # ⚠ **선언을 푸는 자리와 단위를 바꾸는 자리를 `solve()` 안 한 곳으로 모았다.**
                 #   사전등록은 «전환은 레시피에서» 였는데, 선언 블록 검증이 거절을 내야 해서
                 #   거절이 사는 곳으로 한 함수 안쪽으로 옮겼다 — 전환 자리가 **여전히 하나**인
                 #   것은 그대로다. 1 000 배 오류는 안 죽고 조용히 틀린 flux 를 내기 때문이다.
                 tectonic_regime=state.get_optional("tectonic_regime"),
                 legacy_stagnant_lid=state.get_optional("stagnant_lid"),
                 lid_thickness_km=state.get_optional("lid_thickness_km"),
                 surface_temperature_k=state.get_optional("surface_temperature_k"))
