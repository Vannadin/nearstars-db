# 핵 엔트로피 생성 φ (Nimmo+ 2004 식 43, 현재 시점) — C14 프로파일 위의 여섯 항. 밴드이지 판정이 아니다. C15
"""Core entropy production φ = ΔE at the present epoch (C15).

    ΔE = E_R + E_s + E_L + E_H + E_g − E_k              Nimmo+ 2004 (2004GeoJI.156..363N) eq. 43

on the route-B core profile that C14 builds (`core_energy.core_profile`, `core_terms`), at the solved T_c:

    E_R = (M_c/T_c − I_T) H                            eq. 16      I_T = ∫ ρ/T dV (eqs 11/13; numeric here)
    E_s = (C_p/T_c)(M_c − I_S/T_c) dT_c/dt             eq. 10      ⚠ the 1/T_c prefactor — without it E_s is 10⁵ off
    E_L = Q_L (T_i − T_c)/(T_c T_i)                    eq. 17
    E_g = Q_g / T_c                                    text: "E_g is simply Q_g/T_c"
    E_H = −R_H [M_oc/T_i − ∫_oc ρ/T dV] C_c dR_i/dt    eq. 24      ⚠ bracket order recovered by closure on the printed −134
    E_k = k ∫ (∇T/T)² dV                               eq. 25      (eq. 26's closed form is the analytic core's; test only)

**What this node says and does not.** It emits ΔE with three bands (k 30–70 W/(m·K), core H 0–1.5 pW/kg,
dT_c/dt 33–126 K/Gyr) and the paper's own criterion `ΔE > 0` — adopted **as the paper's choice and labelled as
threshold-avoidance**: the excess entropy a dynamo needs is *"probably ∼100 MW K⁻¹, but could lie anywhere within
the range 0.1–1000 MW K⁻¹"* (§5.2), Roberts+ 2003's 2 TW implies ≈ 400 while ≈ 100 *"makes it easier"* (§6.2), and the
paper's own Earth (351) sits between those two readings. **It is not wired into `dynamo_rocky`'s verdict** — a
threshold that cannot decide has no standing to overwrite the ladder; Q_C-vs-Q_k (Brief 60) and φ stand side by
side, as in the paper. **It refuses the 3-Gyr statement by name**: two of the paper's three criteria (mean and
minimum of ΔE over the last 3.1 Gyr) are history quantities, the discriminating one is ΔE_min (Table 5), and a
present-day φ > 0 does not imply a sustained dynamo — that needs the integrator, **C20**, this node's first real
consumer. Without an inner core E_L = E_g = E_H = 0 (all carry dR_i/dt) and ΔE = E_R + E_s − E_k — the paper's
own early-Earth case (*"a completely liquid core"*), which its potassium keeps positive; **our H band's floor is
0, so the H = 0 corner is emitted as the honest corner.** Anchors, γ, `core_state`, `interior` untouched; nothing
fed back; no default changed.
"""
from __future__ import annotations

import math

import cmb_flux as cf
import core_energy as ce
from eos import PhaseGap
from payload import Result, out_of_domain

RECIPE = "internal-heat-luminosity-methodology"
VERSION = "1"
REFS = (
    "docs/reference/internal-heat-luminosity-methodology.md",
    "2004GeoJI.156..363N",      # Nimmo+ 2004 — eqs 10, 11/13, 16, 17, 24, 25, 43; §5.2, §5.3, §6.2; Tables 4, 5
    "engine/core-entropy-context-notes.md",
)
R_H = -27.7e6                  # J/kg, Table 1 (eq. 24)
K_RANGE = cf.K_CORE_RANGE
THRESHOLD_LABEL = ("ΔE > 0 is the paper's own criterion and a threshold-avoidance: the required excess entropy is "
                   "'probably ∼100 MW K⁻¹, but could lie anywhere within the range 0.1–1000' (§5.2); ≈400 (Roberts+ 2003, "
                   "2 TW) vs ≈100 (§6.2) straddle the paper's own Earth (351)")
HISTORY_REFUSAL = ("cannot-say for the last 3 Gyr: the paper's mean and minimum criteria over 3.1 Gyr are history "
                   "quantities and ΔE_min is the discriminating one (Table 5); a present-day φ needs the integrator — C20")
NO_INPUT = "cannot-say (no solved core-side CMB temperature — C15 sits on C14's solution)"


def entropy_terms(prof: dict, terms: dict, dtc_dt: float = ce.DTC_DT, h: float = ce.H_CORE,
                  k: float = cf.K_CORE) -> dict:
    """The six terms [W/K] on a C14 profile with its energy terms, at the profile's own T_c."""
    t_c, r_cmb, m_c = prof["t"][0], prof["r"][0], prof["m"][0]

    def integ(f, lo, hi):
        return ce._integrate_shell(prof, f, lo, hi)
    i_s = integ(lambda i: prof["rho"][i] * prof["t"][i], 0.0, r_cmb)
    i_t = integ(lambda i: prof["rho"][i] / prof["t"][i], 0.0, r_cmb)
    e_r = (m_c / t_c - i_t) * h
    e_s = (ce.C_P / t_c) * (m_c - i_s / t_c) * dtc_dt
    dr = prof["r"][0] - prof["r"][1]
    n = len(prof["t"])
    grad = [(prof["t"][max(i - 1, 0)] - prof["t"][min(i, n - 1)]) / dr if i > 0 else (prof["t"][0] - prof["t"][1]) / dr
            for i in range(n)]
    e_k = k * integ(lambda i: (grad[i] / prof["t"][i]) ** 2, 0.0, r_cmb)
    ic = terms.get("inner_core")
    if ic:
        r_i, t_i, m_oc = ic["r_i"], ic["t_i"], terms["m_oc"]
        e_l = terms["q_l"] * (t_i - t_c) / (t_c * t_i)
        e_g = terms["q_g"] / t_c
        i_t_oc = integ(lambda i: prof["rho"][i] / prof["t"][i], r_i, r_cmb)
        c_c = 4.0 * math.pi * r_i ** 2 * ic["rho_i"] * ce.CHI / m_oc
        e_h = -R_H * (m_oc / t_i - i_t_oc) * c_c * ic["c_r"] * dtc_dt
    else:
        e_l = e_g = e_h = 0.0
    return {"e_r": e_r, "e_s": e_s, "e_l": e_l, "e_g": e_g, "e_h": e_h, "e_k": e_k,
            "delta_e": e_r + e_s + e_l + e_g + e_h - e_k, "i_s": i_s, "i_t": i_t}


def solve(mass_earth: float, core_mass_fraction: float | None, core_radius_earth: float | None,
          cmb_pressure_gpa: float | None, core_cmb_temperature_solved: float | None,
          core_material: str = "fe_prem", body_class: str | None = None) -> Result:
    inputs = {"mass_earth": mass_earth, "core_mass_fraction": core_mass_fraction, "core_radius": core_radius_earth,
              "cmb_pressure": cmb_pressure_gpa, "core_cmb_temperature_solved": core_cmb_temperature_solved,
              "core_material": core_material, "body_class": body_class,
              "k_core_w_m_k": cf.K_CORE, "core_h_w_per_kg": ce.H_CORE, "dtc_dt_k_per_gyr": ce.DTC_DT * ce.GYR_S}
    if body_class in ("giant", "gas_giant", "ice_giant", "sub_neptune", "brown_dwarf", "star"):
        return out_of_domain(RECIPE, VERSION, f"'{body_class}' 에는 이 엔트로피 수지가 뜻이 없다 — 암석체의 금속 핵의 것이다.",
                             inputs=inputs, refs=REFS)
    if not core_radius_earth or not core_mass_fraction or core_mass_fraction <= 0.0:
        return out_of_domain(RECIPE, VERSION, cf.NO_CORE, inputs=inputs, refs=REFS)
    if core_cmb_temperature_solved is None or cmb_pressure_gpa is None:
        return out_of_domain(RECIPE, VERSION, NO_INPUT, inputs=inputs, refs=REFS)
    t_c = float(core_cmb_temperature_solved)
    r_cmb = core_radius_earth * cf.R_EARTH_M
    m_core = mass_earth * cf.M_EARTH_KG * core_mass_fraction
    p_cmb = cmb_pressure_gpa * 1e9
    try:
        prof = ce.core_profile(core_material, p_cmb, t_c, r_cmb, m_core)
        terms = ce.core_terms(prof)
        base = entropy_terms(prof, terms)
        corners = {}
        for k in K_RANGE:
            for h in ce.H_CORE_RANGE:
                for d in ce.DTC_DT_RANGE:
                    corners[(k, h, d)] = entropy_terms(prof, terms, d, h, k)["delta_e"]
        h0 = entropy_terms(prof, terms, h=0.0)["delta_e"]
    except PhaseGap as e:
        return out_of_domain(RECIPE, VERSION, f"핵 프로파일이 재료 도메인 밖으로 나갔다 — {e}", inputs=inputs, refs=REFS)
    de = base["delta_e"]
    lo, hi = min(corners.values()), max(corners.values())
    positive = de > 0.0
    straddles = lo < 0.0 < hi
    ic = terms.get("inner_core")
    mw = 1e6
    values = {"entropy_production": de, "entropy_production_min": lo, "entropy_production_max": hi,
              "entropy_production_h0": h0, "e_r": base["e_r"], "e_s": base["e_s"], "e_l": base["e_l"],
              "e_g": base["e_g"], "e_h": base["e_h"], "e_k": base["e_k"],
              "entropy_positive_present": positive, "entropy_band_straddles_zero": straddles,
              "entropy_corners_positive": sum(1 for v in corners.values() if v > 0.0),
              "has_inner_core_solved": bool(ic), "entropy_history_verdict": "cannot-say (needs C20)"}
    units = {k: "W/K" for k in ("entropy_production", "entropy_production_min", "entropy_production_max",
                                "entropy_production_h0", "e_r", "e_s", "e_l", "e_g", "e_h", "e_k")}
    units.update({"entropy_positive_present": "", "entropy_band_straddles_zero": "", "entropy_corners_positive": "",
                  "has_inner_core_solved": "", "entropy_history_verdict": ""})
    notes = (
        f"**현재 시점 핵 엔트로피 생성 φ = ΔE = {de / mw:+.0f} MW/K** (풀린 T_c {t_c:.0f} K 위; C14) = E_R {base['e_r'] / mw:.0f} "
        f"+ E_s {base['e_s'] / mw:.0f} + E_L {base['e_l'] / mw:.0f} + E_H {base['e_h'] / mw:.0f} + E_g {base['e_g'] / mw:.0f} "
        f"− E_k {base['e_k'] / mw:.0f}. 밴드 {lo / mw:+.0f} … {hi / mw:+.0f} MW/K (k 30–70 × H 0–1.5 pW/kg × dT_c/dt 33–126 K/Gyr "
        f"의 여덟 모서리 중 양수 {sum(1 for v in corners.values() if v > 0.0)}/8), H = 0 모서리 {h0 / mw:+.0f}. "
        + ("내핵 없음 — E_L = E_g = E_H = 0 (셋 다 dR_i/dt 를 품는다), ΔE = E_R + E_s − E_k: 논문의 '완전 액체 핵' 경우이고 "
           "논문에서 그것을 양수로 지키는 것은 핵 안의 칼륨이다(§5.3, 무칼륨이면 −45 %). " if not ic else
           f"내핵 {ic['r_i'] / 1e3:.0f} km. ")
        + f"판정 라벨: {'ΔE > 0' if positive else 'ΔE ≤ 0'} — " + THRESHOLD_LABEL + ". "
        + ("**밴드가 0 을 가로지른다** — 부호가 선언 셋 안에서 갈리므로 이 수는 판정이 아니라 폭이다. " if straddles else "")
        + "**φ 는 dynamo_rocky 의 판정에 배선되지 않는다** — 문턱이 판정을 못 내므로 사다리를 덮어쓸 자격이 없고, "
        "논문도 Q_C 대 Q_k 와 φ 를 나란히 둔다. " + HISTORY_REFUSAL + ". 라벨: 지구에 보정된 모형 · dT_c/dt 4배 · H 4배(바닥 0) "
        "· k 50 ± 20 · γ = 1.5 고체값 · E_H 의 괄호 순서는 인쇄값 −134 에 대한 폐합으로 회수(텍스트층 불명) · "
        "E_k 는 식 25 를 이 프로파일에서 직접 적분(논문의 식 26 은 해석 핵의 닫힌 꼴).",
    )
    return Result(recipe=RECIPE, version=VERSION, regime="core_entropy_production",
                  reason=f"φ = {de / mw:+.0f} MW/K (밴드 {lo / mw:+.0f}…{hi / mw:+.0f}); "
                         f"{'양수' if positive else '음수/0'}; 3 Gyr 진술은 C20 없이 불가.",
                  grade="analog", inputs=inputs, values=values, units=units, refs=REFS, notes=notes)


from registry import recipe  # noqa: E402


@recipe("core_entropy_production")
def _from_state(state):
    return solve(mass_earth=state["mass_earth"], core_mass_fraction=state.get("core_mass_fraction"),
                 core_radius_earth=state.get("core_radius"), cmb_pressure_gpa=state.get("cmb_pressure"),
                 core_cmb_temperature_solved=state.get("core_cmb_temperature_solved"),
                 core_material=state.get("core_material", "fe_prem"), body_class=state.get("body_class"))
