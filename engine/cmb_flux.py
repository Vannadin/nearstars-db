# 핵-맨틀 경계 열류 — Nimmo+ 2004 식 37–39 (맨틀 하단 경계층) 전사 + 선언된 철 열전도로 핵 쪽 단열 열류 (Brief 60)
"""Heat flux across the core–mantle boundary — Nimmo+ 2004 eqs 37–39, and the core-side adiabatic flow.

    from cmb_flux import bottom_layer, adiabatic_flow, solve
    bottom_layer(t_c=4161.0, t_m_base=2694.0, r_cmb=3.48e6)   -> δ_b 144 km, F_b 0.0586 W/m², Q_C 8.9 TW

Nimmo, Price, Brodholt & Gubbins 2004, GJI 156, 363 (2004GeoJI.156..363N, cached), extraction lines
741–749 and Table 2 (layout line 532 ff.):

    δ_b = [Ra_c κ_b η_b(T_a) / (ρ_m g α_m (T_c − T̃_m))]^(1/3)     (37)
    F_b = k_b (T_c − T̃_m) / δ_b                                   (38)
    η_b(T_a) = f η₀ exp[−ζ (T_a − T₁)],   T_a = (T_c + T̃_m)/2     (39; line 903)
    Q_C = 4π R² F_b                                                (line 578)

⚠ Conditions on every number out of here (the top layer's, in `mantle_flux.py`, apply unchanged):
* **T̃_m is the REAL temperature at the base of the mantle**, eq. 29 — not the potential temperature.
  Recovered by closure: with the paper's own T_c = 4161 K and 1603 K potential → 2694 K at 2890 km,
  eqs 37–38 give δ_b 144 km / Q_C 8.9 TW against the printed 140 km / 9 TW (lines 1316–1317); the
  potential-temperature reading gives 738 km. The engine supplies T̃_m as `interior_layers`'s
  `cmb_temperature` (the mantle adiabat evaluated at the CMB), and T_c as `core_state`'s declared
  `core_cmb_temperature_used`.
* **k_b is derived, not printed, exactly as k_t was**: κ_b ρ_m C_pm = 5.76 W/(m·K), on the same
  Hofmeister sentence (line 944 names κ_t AND κ_b).
* **Iron k = 50 ± 20 W/(m·K) is a DECLARATION** (Table 1, layout line 444, eq. 25; Gaidos+ 2010's
  28–100 contains it). A value, a band, a source — not a k(P,T) front (Brief 54's refusal stands).
* **γ = 1.5 is the h.c.p. SOLID value used on a liquid outer core** (`core_state`'s standing caveat,
  Alfè+ 2002 liquid 1.51–1.52) — now upstream of a heat flow, so it rides on `q_adiabat`.
* **Calibrated at source** on present-day Earth; g in eq. 37 is the paper's surface g (Table 2).
* **Without a declared core-side CMB temperature there is no jump** — `core_state`'s lower-bound branch
  sets the core-side temperature equal to the mantle adiabat — and this node refuses by name.
"""
from __future__ import annotations

import math

import mantle_flux as mf
from eos import MATERIALS
from payload import Result, out_of_domain

RECIPE = "internal-heat-luminosity-methodology"
VERSION = "1"
REFS = (
    "2004GeoJI.156..363N",     # Nimmo, Price, Brodholt & Gubbins 2004 — eqs 37–39, Table 1 k, Table 2 constants
    "2010ApJ...718..596G",     # Gaidos+ 2010 — iron k spread 28–100 W/(m·K) (lines 972–989), eq. 14 form
    "cond-mat/0107307",        # Alfè, Price & Gillan 2002 — γ ≈ 1.5 (solid), 1.51–1.52 (liquid)
)

# ── Nimmo+ 2004 Table 2, bottom-layer constants (layout extraction) ──────────────
KAPPA_B = 10.0e-7                 # m²/s, ± 2 (eq. 37)
KAPPA_B_RANGE = (8.0e-7, 12.0e-7)
F_DEEP = 10.0                     # —, "allows the deep mantle a higher viscosity" (eq. 39)
T_1 = 3400.0                      # K, reference temperature appropriate for the deep mantle (eq. 39)
K_B = KAPPA_B * mf.RHO_M * mf.C_PM   # 5.76 W/(m·K), derived as k_t was
# ── Nimmo+ 2004 Table 1 — the core's thermal conductivity, DECLARED ──────────────
K_CORE = 50.0                     # W/(m·K), ± 20 (eq. 25)
K_CORE_RANGE = (30.0, 70.0)
GAMMA = 1.5                       # core_state.GAMMA_CORE — solid value, liquid 1.51–1.52
G_NEWTON = 6.674e-11
M_EARTH_KG = 5.972e24
R_EARTH_M = 6.371e6
PAPER = {"delta_b_km": 140.0, "q_c_tw": 9.0, "q_k_tw": 6.2, "range_tw": (4.5, 9.0)}   # lines 1316–1317, 1341

NO_JUMP = "cannot-say (no declared core-side CMB temperature — the lower-bound branch has no jump to drive a boundary layer)"
NO_CORE = "cannot-say (no core — no core radius or no core mass fraction)"
SUB_ADIABATIC = "Q_CMB (lower bound) below Q_adiabat — the declared lower-bound T_c does not sustain a superadiabatic core at this k; the true Q_CMB is higher"
SUPER_ADIABATIC = "Q_CMB above Q_adiabat"
CONDITION = ("Nimmo+ 2004 eqs 37–39 calibrated at source on present-day Earth; k_b derived (κ_b ρ_m C_pm); "
             "iron k 50 ± 20 W/(m·K) declared; γ = 1.5 solid value on a liquid core; g in eq. 37 is the paper's surface g")


def eta_b(t_a_k: float, zeta: float = mf.ZETA) -> float:
    """eq. 39 [Pa·s]."""
    return F_DEEP * mf.ETA_0 * math.exp(-zeta * (t_a_k - T_1))


def bottom_layer(t_c: float, t_m_base: float, r_cmb: float,
                 zeta: float = mf.ZETA, kappa_b: float = KAPPA_B, g: float = mf.EARTH_G) -> dict:
    """eqs 37–38 at a core-side CMB temperature t_c and the mantle's real base temperature t_m_base.
    Returns δ_b [m], η_b [Pa·s], F_b [W/m²], Q_C [W]. Raises on t_c ≤ t_m_base (no jump)."""
    if t_c <= t_m_base:
        raise ValueError(f"T_c {t_c} K ≤ T̃_m {t_m_base} K — no superadiabatic jump, eq. 37 undefined")
    t_a = 0.5 * (t_c + t_m_base)
    eta = eta_b(t_a, zeta)
    d_b = (mf.RA_C * kappa_b * eta / (mf.RHO_M * g * mf.ALPHA_M * (t_c - t_m_base))) ** (1.0 / 3.0)
    k_b = kappa_b * mf.RHO_M * mf.C_PM
    f_b = k_b * (t_c - t_m_base) / d_b
    return {"delta_b_m": d_b, "eta_b": eta, "f_b_w_m2": f_b, "q_c_w": f_b * 4.0 * math.pi * r_cmb ** 2}


def adiabatic_flow(material_name: str, p_cmb: float, t_c: float, r_cmb: float, m_core: float,
                   k: float = K_CORE) -> dict:
    """Core-side adiabatic heat flow at the CMB: Q = 4π r² k |dT/dr|, dT/dr from T ∝ ρ^γ and dP/dr = −ρ g.
    dρ/dP is a central finite difference of the material's own density(P, T)."""
    mat = MATERIALS[material_name]
    rho = mat.density(p_cmb, t_c, 0.0)
    h = 1.0e-3 * p_cmb
    drho_dp = (mat.density(p_cmb + h, t_c, 0.0) - mat.density(p_cmb - h, t_c, 0.0)) / (2.0 * h)
    g_cmb = G_NEWTON * m_core / r_cmb ** 2
    dt_dr = -GAMMA * t_c / rho * drho_dp * rho * g_cmb          # K/m, negative outward
    return {"rho_cmb": rho, "g_cmb": g_cmb, "dt_dr_ad": dt_dr,
            "q_ad_w": 4.0 * math.pi * r_cmb ** 2 * k * abs(dt_dr)}


def solve(mass_earth: float, core_mass_fraction: float | None, core_radius_earth: float | None,
          cmb_pressure_gpa: float | None, cmb_temperature: float | None,
          core_cmb_temperature_used: float | None, core_cmb_declared: bool,
          core_material: str = "fe_prem", body_class: str | None = None) -> Result:
    # keys are the state's names (the contract's Needs); the declaration is recorded as its value or None
    inputs = {"mass_earth": mass_earth, "core_mass_fraction": core_mass_fraction,
              "core_radius": core_radius_earth, "cmb_pressure": cmb_pressure_gpa,
              "cmb_temperature": cmb_temperature, "core_cmb_temperature_used": core_cmb_temperature_used,
              "core_cmb_temperature": core_cmb_temperature_used if core_cmb_declared else None,
              "core_material": core_material, "body_class": body_class}
    if body_class in ("giant", "gas_giant", "ice_giant", "sub_neptune", "brown_dwarf", "star"):
        return out_of_domain(RECIPE, VERSION, f"'{body_class}' 에는 규산염 맨틀 하단 경계층이 없다 — 이 노드는 암석체의 것이다.",
                             inputs=inputs, refs=REFS)
    if not core_radius_earth or not core_mass_fraction or core_mass_fraction <= 0.0:
        return out_of_domain(RECIPE, VERSION, NO_CORE, inputs=inputs, refs=REFS)
    if not core_cmb_declared or core_cmb_temperature_used is None or cmb_temperature is None:
        return out_of_domain(RECIPE, VERSION, NO_JUMP, inputs=inputs, refs=REFS)
    t_c, t_m = float(core_cmb_temperature_used), float(cmb_temperature)
    if t_c <= t_m:
        return out_of_domain(RECIPE, VERSION,
                             f"핵 쪽 경계온도 {t_c:.0f} K 가 맨틀 단열선 밑 {t_m:.0f} K 이하 — 초단열 점프가 없어 식 37 이 정의되지 않는다.",
                             inputs=inputs, refs=REFS)
    r_cmb = core_radius_earth * R_EARTH_M
    m_core = mass_earth * M_EARTH_KG * core_mass_fraction
    core = bottom_layer(t_c, t_m, r_cmb)
    band = [bottom_layer(t_c, t_m, r_cmb, z, kb)["q_c_w"]
            for z in (mf.ZETA_RANGE[0], mf.ZETA, mf.ZETA_RANGE[1]) for kb in (KAPPA_B_RANGE[0], KAPPA_B, KAPPA_B_RANGE[1])]
    ad = adiabatic_flow(core_material, cmb_pressure_gpa * 1e9, t_c, r_cmb, m_core)
    ad_band = (ad["q_ad_w"] * K_CORE_RANGE[0] / K_CORE, ad["q_ad_w"] * K_CORE_RANGE[1] / K_CORE)
    verdict = SUPER_ADIABATIC if core["q_c_w"] > ad["q_ad_w"] else SUB_ADIABATIC   # on a lower-bound Q_CMB
    lo, hi = PAPER["range_tw"]
    inside = lo * 1e12 <= core["q_c_w"] <= hi * 1e12
    values = {"q_cmb": core["q_c_w"], "q_cmb_min": min(band), "q_cmb_max": max(band),
              "cmb_boundary_layer": core["delta_b_m"] / 1e3, "cmb_heat_flux_density": core["f_b_w_m2"],
              "eta_bottom": core["eta_b"], "q_adiabat": ad["q_ad_w"],
              "q_adiabat_min": ad_band[0], "q_adiabat_max": ad_band[1],
              "adiabat_gradient_cmb": ad["dt_dr_ad"] * 1e3, "g_cmb": ad["g_cmb"],
              "k_core": K_CORE, "cmb_jump": t_c - t_m, "cmb_flux_verdict": verdict,
              "q_cmb_in_paper_range": inside}
    units = {"q_cmb": "W", "q_cmb_min": "W", "q_cmb_max": "W", "cmb_boundary_layer": "km",
             "cmb_heat_flux_density": "W/m2", "eta_bottom": "Pa s", "q_adiabat": "W", "q_adiabat_min": "W",
             "q_adiabat_max": "W", "adiabat_gradient_cmb": "K/km", "g_cmb": "m/s2", "k_core": "W/(m K)",
             "cmb_jump": "K", "cmb_flux_verdict": "", "q_cmb_in_paper_range": ""}
    notes = (
        "⚠ **Q_CMB 는 하한이다** (브리프 62): 핵 쪽 경계온도는 선언된 **하한** 이고(core-state-methodology.md@«The core-side value on Earth is 3760 ± 290 K.» — "
        "지구 3760 ± 290 K, D″ 점프는 CMB 열류가 정하는데 이 리포지토리는 그 열류를 도출하지 않았고, 이름 붙은 편향 둘이 "
        "모두 아래를 가리킨다), η_b 가 T_a 에 지수적이라 하한 입력은 하한 열류를 낸다. 참값은 이보다 높다 — "
        "이 수로 '다이나모 없음' 을 읽지 말 것. 하한을 해로 바꾸는 것은 핵 에너지 수지의 폐합(브리프 62 B)이다.",
        f"핵-맨틀 경계 열류 (Nimmo+ 2004 식 37–39): 핵 쪽 경계온도 {t_c:.0f} K (선언 하한) − 맨틀 단열선 밑 {t_m:.0f} K "
        f"= 점프 {t_c - t_m:.0f} K, T_a {(t_c + t_m) / 2:.0f} K → η_b {core['eta_b']:.2e} Pa·s, δ_b {core['delta_b_m'] / 1e3:.0f} km, "
        f"F_b {core['f_b_w_m2']:.4f} W/m², Q_CMB {core['q_c_w'] / 1e12:.2f} TW (ζ ±0.5 × κ_b ±2 밴드 {min(band) / 1e12:.2f}–{max(band) / 1e12:.2f} TW). "
        f"논문 자신의 현재 지구 인쇄값은 δ_b 140 km · Q_C 9 TW (4.5–9 TW 범위) 이고, 이 값은 그 범위 "
        f"{'안' if inside else '밖'}이다 — {'폐합' if inside else '보정되지 않은 채 보고한다; k·γ·ζ·f·T₁ 는 선언이라 옮기지 않는다'}. "
        "T̃_m 은 포텐셜 온도가 아니라 맨틀 밑의 실온(식 29)이다 — 폐합으로 회수한 읽기.",
        f"핵 쪽 단열 열류: k {K_CORE:.0f} W/(m·K) (Table 1, 50 ± 20 — **선언**, Gaidos+ 2010 의 28–100 안) × "
        f"|dT/dr| {abs(ad['dt_dr_ad']) * 1e3:.2f} K/km (γ = 1.5 · ρ {ad['rho_cmb']:.0f} kg/m³ · g_cmb {ad['g_cmb']:.2f} m/s²) "
        f"× 4π r_cmb² → Q_ad {ad['q_ad_w'] / 1e12:.2f} TW (k 30–70: {ad_band[0] / 1e12:.2f}–{ad_band[1] / 1e12:.2f} TW; 논문 6.2 TW, 자기 밀도 모형). "
        f"판정 {verdict}. ⚠ γ = 1.5 는 h.c.p. 고체값이고 액체는 1.51–1.52 (Alfè+ 2002) — core_state 의 조건이 열류에 실려 온다. "
        + CONDITION + ".",
    )
    return Result(recipe=RECIPE, version=VERSION, regime="cmb_bottom_boundary_layer",
                  reason=f"Nimmo+ 2004 하단 경계층: 점프 {t_c - t_m:.0f} K → Q_CMB {core['q_c_w'] / 1e12:.2f} TW; 단열 {ad['q_ad_w'] / 1e12:.2f} TW ({verdict}).",
                  grade="analog", inputs=inputs, values=values, units=units, refs=REFS, notes=notes)


from registry import recipe  # noqa: E402


@recipe("cmb_heat_flux")
def _from_state(state):
    return solve(mass_earth=state["mass_earth"],
                 core_mass_fraction=state.get("core_mass_fraction"),
                 core_radius_earth=state.get("core_radius"),
                 cmb_pressure_gpa=state.get("cmb_pressure"),
                 cmb_temperature=state.get("cmb_temperature"),
                 core_cmb_temperature_used=state.get("core_cmb_temperature_used"),
                 core_cmb_declared=state.get("core_cmb_temperature") is not None,
                 core_material=state.get("core_material", "fe_prem"),
                 body_class=state.get("body_class"))
