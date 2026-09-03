# 핵 에너지 수지 (Nimmo+ 2004 식 30) 로 핵 쪽 CMB 온도 T_c 를 근찾기로 푼다 — 선언 하한을 해로. C14, 되먹임 없음
"""Core energy balance — solve the core-side CMB temperature (C14).

    bottom_layer(T_c) = Q̃(T_c) · (−dT_c/dt) + M_c · H        Nimmo+ 2004 (2004GeoJI.156..363N) eq. 30, with 31

The left side is the mantle's bottom boundary layer (eqs 37–39, `cmb_flux.bottom_layer`). The right side is
what the core can supply: secular cooling — Q_s (eq. 10), Q_L (17), Q_g (19–21), all linear in dT_c/dt — and
radiogenic Q_R = M_c H (16). With **dT_c/dt declared** the balance is algebraic in T_c and is closed by one
root-find; no time integration (Brief 62 step 1's measurement). Q_H is omitted by name (R_H, Table 1).

**The core profile is built here** (route B): from the CMB inward, `material.density(P, T_ad)` with
hydrostatics dP/dr = −ρ g, g = G m(r)/r², m falling from M_core; the adiabat T = T_c (ρ/ρ_cmb)^γ
(`core_state`, γ = 1.5 — the h.c.p. solid value on a liquid core, the standing caveat, now under a heat
flow twice over); ψ(r) = −∫_r^R g dr (zero at the CMB; the zero point cancels in Q_g). The ICB is where the
adiabat meets the core material's melting curve (`core_state`'s own test), C_r = dR_i/dT_c from the two
slopes there — a ratio of two nearly parallel slopes, so it is reported with its sensitivity.

Nimmo's analytic core (eqs 1–9, Table 1) is **not here** — it lives in `test_core_energy.py` only, as the
transcription that reproduces Table 4; a recipe-side copy would invite Earth's core shape to be declared
on another body.

**Declarations, each with its band carried into the emitted values** — all Nimmo Table 1/2/4, Earth's:
dT_c/dt −33 K/Gyr (band 33–126, Gubbins' comparison model, Table 3 note — a 4× model-to-model spread, and
for an exoplanet it is the thermal history this engine does not compute: the solved T_c is *"T_c under an
Earth-like present-day cooling rate"*); core H 1.5 pW/kg (Table 4, 400 ppm K; floor 0 — the paper's own
no-potassium case §5.3; the same first author uses 100 ppm K in 2020); C_p 840; α_c 1.35 ± 0.15e−5;
L_h 750 kJ/kg; β_c 1.1 ± 0.1; χ 4.2 wt %. **Nothing here is fed back into `core_state`** — the solved T_c is
reported beside the declared lower bound (C14's scope; feeding back moves anchors and is a separate decision).
"""
from __future__ import annotations

import math

import cmb_flux as cf
import core_state as cs
from eos import MATERIALS, PhaseGap
from payload import Result, out_of_domain

RECIPE = "internal-heat-luminosity-methodology"
VERSION = "1"
REFS = (
    "docs/reference/internal-heat-luminosity-methodology.md",
    "2004GeoJI.156..363N",      # Nimmo, Price, Brodholt & Gubbins 2004 — eqs 10, 16, 17, 19–21, 30, 31; Tables 1, 2, 3, 4
    "engine/core-energy-balance-context-notes.md",
)

GYR_S = 3.156e16
DTC_DT = -33.0 / GYR_S            # K/s, Table 4 nominal (present day)
DTC_DT_RANGE = (-126.0 / GYR_S, -33.0 / GYR_S)   # Table 3 note (Gubbins, k = 60) … Table 4 — model-to-model
H_CORE = 1.5e-12                  # W/kg, Table 4 (400 ppm K)
H_CORE_RANGE = (0.0, 1.5e-12)     # floor: no potassium (§5.3); 2020's 100 ppm K sits inside
C_P = 840.0                       # J/(kg K), Table 1
ALPHA_C = 1.35e-5                 # 1/K, ± 0.15, Table 1 (used only through the adiabat's γ here — not directly)
L_H = 750.0e3                     # J/kg, Table 1
BETA_C = 1.1                      # —, ± 0.1, Table 1 (eq. 21)
CHI = 0.042                       # wt fraction, Table 2 χ₀ 4.2 (+1.5 −1.7)
GAMMA = cs.GAMMA_CORE
G = cf.G_NEWTON
STEPS = 400

NO_INPUTS = "cannot-say (no core-side CMB temperature declared, or no mantle base temperature — the balance needs both sides)"
NO_ROOT = "cannot-say (the core energy balance has no root in its physical bracket — bracket not widened)"
CONDITION = ("Nimmo+ 2004 eq. 30 closed at the present epoch with dT_c/dt declared (Earth's −33 K/Gyr; band 33–126); "
             "core H declared (1.5 pW/kg; floor 0); Q_H omitted; γ = 1.5 solid value on a liquid core; "
             "model calibrated on present-day Earth; the solved T_c is not fed back to core_state")


def core_profile(material_name: str, p_cmb: float, t_c: float, r_cmb: float, m_core: float,
                 steps: int = STEPS) -> dict:
    """ρ, g, T, ψ, m on r from the CMB inward (route B). Returns arrays (outer → inner) and the closure residuals."""
    mat = MATERIALS[material_name]
    rho_cmb = mat.density(p_cmb, t_c, 0.0)
    r, p, m = r_cmb, p_cmb, m_core
    rs, rhos, gs, ts, psis, ms, ps = [], [], [], [], [], [], []
    psi = 0.0
    dr = r_cmb / steps
    # The innermost 2 % of the radius (10⁻⁵ of the volume) is not integrated: an inward integration that
    # closes M_core to a few 10⁻³ leaves a residual that G m / r² turns into a divergence at r → 0. The
    # residual is returned as the profile's own closure number (pre-registered check), not hidden.
    r_min = 0.02 * r_cmb
    while r > r_min:
        rho = mat.density(p, t_c, 0.0)
        t = t_c * (rho / rho_cmb) ** GAMMA
        rho = mat.density(p, t, 0.0)                     # one re-evaluation at the adiabat's own T
        g = G * max(m, 0.0) / (r * r)
        rs.append(r); rhos.append(rho); gs.append(g); ts.append(t); psis.append(psi); ms.append(m); ps.append(p)
        # step inward
        p += rho * g * dr
        m -= 4.0 * math.pi * r * r * rho * dr
        psi -= g * dr                                     # ψ decreases inward (zero at the CMB)
        r -= dr
    return {"r": rs, "rho": rhos, "g": gs, "t": ts, "psi": psis, "m": ms, "p": ps,
            "m_center_residual": m / m_core, "p_center": p, "rho_cmb": rho_cmb, "material": mat,
            "r_min": r_min}


def _integrate_shell(prof: dict, f, r_lo: float, r_hi: float) -> float:
    """∫ f(i) 4π r² dr over the profile samples with r_lo ≤ r ≤ r_hi (outer → inner samples, uniform dr)."""
    dr = prof["r"][0] - prof["r"][1]
    return sum(f(i) * 4.0 * math.pi * prof["r"][i] ** 2 * dr
               for i in range(len(prof["r"])) if r_lo <= prof["r"][i] <= r_hi)


def inner_core(prof: dict) -> dict | None:
    """Where the adiabat crosses the material's melting curve, inward. None if the whole core is liquid
    (or the melting curve is undefined). Also the two slopes at the ICB and C_r = dR_i/dT_c."""
    mat = prof["material"]
    margin = []
    for p, t in zip(prof["p"], prof["t"]):
        tm = mat.t_melt(p)
        if tm is None:
            return None
        margin.append(t - tm)
    if margin[0] <= 0.0:
        return {"status": "solid_at_cmb"}          # no liquid outer core — eq. 30's terms do not apply
    if all(mg > 0.0 for mg in margin):
        return {"status": "all_liquid"}            # no inner core: Q_L = Q_g = 0
    i = next(k for k in range(1, len(margin)) if margin[k] <= 0.0)
    # linear interpolation of the crossing between samples i-1 (liquid) and i (solid)
    f = margin[i - 1] / (margin[i - 1] - margin[i])
    r_i = prof["r"][i - 1] + f * (prof["r"][i] - prof["r"][i - 1])
    p_i = prof["p"][i - 1] + f * (prof["p"][i] - prof["p"][i - 1])
    t_i = prof["t"][i - 1] + f * (prof["t"][i] - prof["t"][i - 1])
    rho_i = prof["rho"][i - 1] + f * (prof["rho"][i] - prof["rho"][i - 1])
    dr = prof["r"][i - 1] - prof["r"][i]
    dt_ad_dr = (prof["t"][i - 1] - prof["t"][i]) / dr
    dt_m_dr = (mat.t_melt(prof["p"][i - 1]) - mat.t_melt(prof["p"][i])) / dr
    t_c = prof["t"][0]
    c_r = (t_i / t_c) / (dt_m_dr - dt_ad_dr)            # dR_i/dT_c, chain rule at the crossing
    return {"status": "inner_core", "r_i": r_i, "p_i": p_i, "t_i": t_i, "rho_i": rho_i,
            "dt_ad_dr": dt_ad_dr, "dt_m_dr": dt_m_dr, "c_r": c_r, "index": i}


def core_terms(prof: dict, dtc_dt: float = DTC_DT, h: float = H_CORE) -> dict:
    """Q_s, Q_L, Q_g, Q_R [W] on a built profile at its own T_c. Q_L = Q_g = 0 without an inner core."""
    t_c = prof["t"][0]
    r_cmb = prof["r"][0]
    m_c = prof["m"][0]
    i_s = _integrate_shell(prof, lambda k: prof["rho"][k] * prof["t"][k], 0.0, r_cmb)
    q_s = -(C_P / t_c) * i_s * dtc_dt
    q_r = m_c * h
    ic = inner_core(prof)
    if ic is None or ic["status"] != "inner_core":
        return {"q_s": q_s, "q_l": 0.0, "q_g": 0.0, "q_r": q_r, "i_s": i_s, "inner_core": None,
                "core_status": (ic or {}).get("status", "no_melting_curve"), "q_total": q_s + q_r}
    r_i = ic["r_i"]
    m_oc = _integrate_shell(prof, lambda k: prof["rho"][k], r_i, r_cmb)
    q_l = 4.0 * math.pi * r_i ** 2 * L_H * ic["rho_i"] * ic["c_r"] * dtc_dt
    c_c = 4.0 * math.pi * r_i ** 2 * ic["rho_i"] * CHI / m_oc
    psi_i = prof["psi"][ic["index"]]
    int_rho_psi = _integrate_shell(prof, lambda k: prof["rho"][k] * prof["psi"][k], r_i, r_cmb)
    q_g = (int_rho_psi - m_oc * psi_i) * BETA_C * c_c * ic["c_r"] * dtc_dt
    return {"q_s": q_s, "q_l": q_l, "q_g": q_g, "q_r": q_r, "i_s": i_s, "inner_core": ic, "m_oc": m_oc,
            "q_total": q_s + q_l + q_g + q_r}


def balance(t_c: float, t_m_base: float, material_name: str, p_cmb: float, r_cmb: float, m_core: float,
            dtc_dt: float = DTC_DT, h: float = H_CORE) -> tuple[float, dict, dict]:
    """f(T_c) = Q_C(T_c) − [Q_s + Q_L + Q_g + Q_R](T_c). Returns (f, boundary-layer dict, terms dict)."""
    bl = cf.bottom_layer(t_c, t_m_base, r_cmb)
    prof = core_profile(material_name, p_cmb, t_c, r_cmb, m_core)
    terms = core_terms(prof, dtc_dt, h)
    return bl["q_c_w"] - terms["q_total"], bl, terms


def find_root(t_m_base: float, material_name: str, p_cmb: float, r_cmb: float, m_core: float,
              dtc_dt: float = DTC_DT, h: float = H_CORE, t_hi: float | None = None) -> float | None:
    """Bisection on the physical bracket [T_lo, T_hi]. T_lo = max(T̃_m + 1 K, T_melt(P_cmb) + 1 K): below the
    mantle base there is no jump (eq. 37 undefined), and below the CMB melting temperature the core is solid at
    the CMB and eq. 30's outer-core terms do not apply. T_hi = 3 T̃_m, or lower where the core material
    refuses (PhaseGap) first — the cap is named, not physical. An all-liquid core is **not** a bracket end: it
    is the Q_L = Q_g = 0 regime (registered branch ⑤) and f is continuous across it. Returns None if f keeps
    one sign on the bracket — the bracket is NOT widened to make a root."""
    mat = MATERIALS[material_name]
    t_melt_cmb = mat.t_melt(p_cmb)
    lo = max(t_m_base, t_melt_cmb if t_melt_cmb is not None else 0.0) + 1.0
    if t_hi is None:
        t_hi = 3.0 * t_m_base
        t_probe = lo
        while t_probe < t_hi:
            t_probe = min(t_probe * 1.05, t_hi)
            try:
                core_profile(material_name, p_cmb, t_probe, r_cmb, m_core)
            except PhaseGap:
                t_hi = t_probe / 1.05
                break
    f_lo = balance(lo, t_m_base, material_name, p_cmb, r_cmb, m_core, dtc_dt, h)[0]
    f_hi = balance(t_hi, t_m_base, material_name, p_cmb, r_cmb, m_core, dtc_dt, h)[0]
    if (f_lo > 0.0) == (f_hi > 0.0):
        return None
    hi = t_hi
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        f_mid = balance(mid, t_m_base, material_name, p_cmb, r_cmb, m_core, dtc_dt, h)[0]
        if (f_mid > 0.0) == (f_lo > 0.0):
            lo, f_lo = mid, f_mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def solve(mass_earth: float, core_mass_fraction: float | None, core_radius_earth: float | None,
          cmb_pressure_gpa: float | None, cmb_temperature: float | None,
          core_cmb_temperature: float | None, core_material: str = "fe_prem",
          body_class: str | None = None) -> Result:
    inputs = {"mass_earth": mass_earth, "core_mass_fraction": core_mass_fraction,
              "core_radius": core_radius_earth, "cmb_pressure": cmb_pressure_gpa,
              "cmb_temperature": cmb_temperature, "core_cmb_temperature": core_cmb_temperature,
              "core_material": core_material, "body_class": body_class,
              "dtc_dt_k_per_gyr": DTC_DT * GYR_S, "core_h_w_per_kg": H_CORE}
    if body_class in ("giant", "gas_giant", "ice_giant", "sub_neptune", "brown_dwarf", "star"):
        return out_of_domain(RECIPE, VERSION, f"'{body_class}' 에는 규산염 맨틀 하단 경계층이 없다 — 이 수지는 암석체의 것이다.",
                             inputs=inputs, refs=REFS)
    if not core_radius_earth or not core_mass_fraction or core_mass_fraction <= 0.0:
        return out_of_domain(RECIPE, VERSION, cf.NO_CORE, inputs=inputs, refs=REFS)
    if cmb_temperature is None or cmb_pressure_gpa is None or core_cmb_temperature is None:
        return out_of_domain(RECIPE, VERSION, NO_INPUTS, inputs=inputs, refs=REFS)
    t_m = float(cmb_temperature)
    r_cmb = core_radius_earth * cf.R_EARTH_M
    m_core = mass_earth * cf.M_EARTH_KG * core_mass_fraction
    p_cmb = cmb_pressure_gpa * 1e9
    try:
        t_root = find_root(t_m, core_material, p_cmb, r_cmb, m_core)
        if t_root is None:
            return out_of_domain(RECIPE, VERSION, NO_ROOT, inputs=inputs, refs=REFS)
        f0, bl, terms = balance(t_root, t_m, core_material, p_cmb, r_cmb, m_core)
        # bands: dT_c/dt (33–126 K/Gyr) × H (0 … 1.5 pW/kg), each corner re-solved
        roots = {}
        for d in DTC_DT_RANGE:
            for hh in H_CORE_RANGE:
                roots[(d, hh)] = find_root(t_m, core_material, p_cmb, r_cmb, m_core, d, hh)
    except PhaseGap as e:
        return out_of_domain(RECIPE, VERSION, f"핵 프로파일이 재료 도메인 밖으로 나갔다 — {e}", inputs=inputs, refs=REFS)
    band = [t for t in roots.values() if t is not None]
    prof = core_profile(core_material, p_cmb, t_root, r_cmb, m_core)
    ic = terms["inner_core"]
    declared = float(core_cmb_temperature)
    values = {"core_cmb_temperature_solved": t_root, "core_cmb_temperature_solved_min": min(band) if band else None,
              "core_cmb_temperature_solved_max": max(band) if band else None,
              "core_cmb_temperature_declared": declared, "core_cmb_solved_minus_declared": t_root - declared,
              "q_cmb_solved": bl["q_c_w"], "q_s": terms["q_s"], "q_l": terms["q_l"], "q_g": terms["q_g"], "q_r": terms["q_r"],
              "icb_radius_solved": (ic["r_i"] / 1e3) if ic else 0.0, "icb_pressure_solved": (ic["p_i"] / 1e9) if ic else 0.0,
              "c_r_km_per_k": (ic["c_r"] / 1e3) if ic else 0.0, "has_inner_core_solved": bool(ic),
              "core_profile_mass_residual": prof["m_center_residual"], "core_center_pressure_solved": prof["p_center"] / 1e9,
              "balance_residual": f0 / max(bl["q_c_w"], 1.0), "band_corners_with_root": len(band)}
    units = {"core_cmb_temperature_solved": "K", "core_cmb_temperature_solved_min": "K", "core_cmb_temperature_solved_max": "K",
             "core_cmb_temperature_declared": "K", "core_cmb_solved_minus_declared": "K", "q_cmb_solved": "W",
             "q_s": "W", "q_l": "W", "q_g": "W", "q_r": "W", "icb_radius_solved": "km", "icb_pressure_solved": "GPa",
             "c_r_km_per_k": "km/K", "has_inner_core_solved": "", "core_profile_mass_residual": "",
             "core_center_pressure_solved": "GPa", "balance_residual": "", "band_corners_with_root": ""}
    tw = 1e12
    notes = (
        f"**핵 에너지 수지(Nimmo+ 2004 식 30)로 푼 핵 쪽 CMB 온도: {t_root:.0f} K** — 선언 하한 {declared:.0f} K 보다 "
        f"{t_root - declared:+.0f} K. 밴드 {min(band):.0f}–{max(band):.0f} K (dT_c/dt 33–126 K/Gyr × 핵 H 0–1.5 pW/kg 의 "
        f"네 모서리 중 근이 잡힌 {len(band)}/4). 그 온도에서 맨틀이 빼가는 Q_C {bl['q_c_w'] / tw:.2f} TW = "
        f"Q_s {terms['q_s'] / tw:.2f} + Q_L {terms['q_l'] / tw:.2f} + Q_g {terms['q_g'] / tw:.2f} + Q_R {terms['q_r'] / tw:.2f} "
        f"(잔차 {f0 / tw:+.3f} TW). " + (f"내핵 반지름 {ic['r_i'] / 1e3:.0f} km (경계 {ic['p_i'] / 1e9:.0f} GPa), "
                                        f"C_r {ic['c_r'] / 1e3:.1f} km/K — 융해곡선과 단열선 두 기울기의 비라 칼날 위 "
                                        f"(ICB 에서 {ic['dt_m_dr'] * 1e3:.2f} vs {ic['dt_ad_dr'] * 1e3:.2f} K/km)." if ic
                                        else "내핵 없음 — Q_L·Q_g 가 떨어진 축약형 Q_C = Q_s + Q_R."),
        "⚠ **되먹이지 않는다.** 이 값은 보고이지 core_state 의 입력이 아니다 — 되먹이면 앵커가 움직이고 그건 별도 결정이다. "
        "라벨: ① 지구에 보정된 모형(성공 기준 자체가 현재 지구 재현); ② dT_c/dt 는 선언(−33 K/Gyr, 두 발표 지구 모형 "
        "사이 4배) — 외계 천체에는 이 엔진이 계산하지 않는 열역사 그 자체라 풀린 T_c 는 '지구형 현재 냉각률 하의 T_c'; "
        "③ 핵 H 는 선언(1.5 pW/kg = 400 ppm K, 바닥 0, 같은 저자의 2020 값은 100 ppm K); ④ γ = 1.5 는 고체 h.c.p. 값을 "
        "액체 외핵에 쓴 것; ⑤ Q_H(반응열, R_H −27.7 MJ/kg) 생략. "
        f"프로파일 폐합: 중심 질량 잔차 {prof['m_center_residual']:+.3f}, 중심압 {prof['p_center'] / 1e9:.0f} GPa. " + CONDITION + ".",
    )
    return Result(recipe=RECIPE, version=VERSION, regime="core_energy_balance",
                  reason=f"핵 에너지 수지: T_c {t_root:.0f} K (선언 {declared:.0f}), Q_C {bl['q_c_w'] / tw:.2f} TW, "
                         f"내핵 {'있음' if ic else '없음'}.",
                  grade="analog", inputs=inputs, values=values, units=units, refs=REFS, notes=notes)


from registry import recipe  # noqa: E402


@recipe("core_energy_balance")
def _from_state(state):
    return solve(mass_earth=state["mass_earth"],
                 core_mass_fraction=state.get("core_mass_fraction"),
                 core_radius_earth=state.get("core_radius"),
                 cmb_pressure_gpa=state.get("cmb_pressure"),
                 cmb_temperature=state.get("cmb_temperature"),
                 core_cmb_temperature=state.get("core_cmb_temperature"),
                 core_material=state.get("core_material", "fe_prem"),
                 body_class=state.get("body_class"))
