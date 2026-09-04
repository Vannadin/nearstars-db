# 암석체의 방사성 가열 예산 — 네 핵종의 현재값과 붕괴 이력, internal_heat_nontidal 의 암석 갈래 (Brief 44)
"""Radiogenic heat budget of a rocky body, present day, plus its decay history.

    from radiogenic import budget, history_factor
    budget(silicate_mass_kg=4.0e24)["total_w"] / 1e12          -> 21.15 TW (Earth (1) set)
    history_factor(-4.0)                                        -> 3.67

⚠ Where the constants come from — say all three things, every time.
The four isotope constants below are **standard nuclear data** (half-life, isotopic abundance,
heat production per kg of isotope): any handbook prints them, which is why the closure works.
**We read them from Nimmo & Primack 2020's unpublished draft table** — it sits after
`\\end{document}` in `docs/phase3/_papers/2020ApJ...903L..37N.src/main.tex` (lines 494–499), never
compiled, caption ending `\\textcolor{red}{check}`, absent from the PDF (0 hits for every number).
**There is no "Nimmo & Primack 2020 Table 1"; never cite one.** The closure in `test_radiogenic.py`
is the check that we read them right: 21.15 / 10.63 / 21.55 TW against the draft's own 21.4 / 10.8
and the appendix's printed "22 TW at the present day" (`main.tex:420–421`).

⚠ The draft caption says the heating rates refer to the *initial* composition. Read that way the set
gives 11.59 TW today, 1.9× short of the paper's own appendix; **the concentrations are present-day**
(the appendix settles it). engine/radiogenic-budget-context-notes.md §1.

What this module does not do: thermal evolution. H(t) is four exponentials and is built; turning it
into a core that is or is not still convecting is Nimmo+ 2004 (`2004GeoJI.156..363N`) — held (cached
with PROVENANCE; Brief 60 transcribed its eqs 37–39 into `cmb_flux.py`). The supplier of the CMB flux now
exists; the chain.yaml edge to dynamo_rocky stays a gap because its consumer wiring is the φ step
(core entropy production), not because the paper is missing. ("not cached" stood here from 10:15 on 2026-09-03
until Brief 64 corrected it.) The giant branch (cooling
luminosity L(M, age)) is refused here exactly as `dynamo.py` refuses it.
"""
from __future__ import annotations

import math

import mantle_flux
from payload import Result, out_of_domain

RECIPE = "internal-heat-luminosity-methodology"
VERSION = "1"
REFS = (
    "2020ApJ...903L..37N",     # Nimmo & Primack 2020, ApJL 903, L37 — the appendix (22 TW, 70 %) is in
                               # the paper; the four constants are in its UNPUBLISHED draft table only
    # The constants are standard nuclear data; **the canonical tabulation is not held.** Read from
    # N&P's draft table and closure-checked against that table's own totals — which certifies the
    # transcription, not the constants (the authors computed those totals from the same numbers).
    # Candidate standard source, named from memory and NOT read (on the request list):
    # Ruedas 2017, Geochem. Geophys. Geosyst. — radioactive heat production of the long-lived nuclides.
    "standard-nuclear-data (not held; see engine/radiogenic-budget-context-notes.md §5)",
)

SIGMA_SB = 5.670374419e-8            # W m⁻² K⁻⁴
M_EARTH_KG = 5.972e24
R_EARTH_M = 6.371e6
GYR_S = 1e9 * 365.25 * 86400.0

# (half-life Gyr, isotopic mass fraction of the element, W per kg of isotope) — main.tex:494-499
ISOTOPES = {
    "K40":   (1.25,  0.0117e-2, 2.92e-5),
    "Th232": (14.0,  1.0,       2.64e-5),
    "U238":  (4.47,  0.99275,   9.46e-5),
    "U235":  (0.704, 0.0072,    5.69e-4),
}
ELEMENT_OF = {"K40": "K", "Th232": "Th", "U238": "U", "U235": "U"}

# Bulk-silicate concentrations (element mass fractions), the declared family — main.tex:494-499,
# :420. Neither set is elected; the recipe emits the default and the second beside it.
CONCENTRATION_SETS = {
    "earth_1_chondritic":      {"K": 260e-6, "Th": 85e-9, "U": 22e-9},   # Palme & O'Neill 2014
    "earth_2_non_chondritic":  {"K": 130e-6, "Th": 43e-9, "U": 11e-9},   # O'Neill & Palme 2008
    "appendix":                {"K": 260e-6, "Th": 85e-9, "U": 23e-9},   # the paper's own model set
}
DEFAULT_SET = "earth_1_chondritic"
LOW_SET = "earth_2_non_chondritic"

# "the convecting mantle is responsible for 70 % of the total radiogenic heat at all times; the
# remainder is assumed to reside in the crust and will not contribute to mantle thermal evolution"
# — the appendix. Earth's number, DECLARED for every rocky body.
MANTLE_SHARE = 0.70

# Standard BSE mass used only by the test's closure against the paper's own arithmetic. The recipe
# uses the body's own silicate mass (mass × (1 − core_mass_fraction)), which is derived, not declared.
BSE_MASS_STANDARD_KG = 4.0e24


def heat_per_kg(conc: dict[str, float], t_gyr: float = 0.0,
                species: tuple[str, ...] | None = None) -> float:
    """W per kg of bulk silicate at time t (Gyr; negative = the past, positive = the future).
    Each species decays as 2^(−t/t½) from its present-day abundance."""
    total = 0.0
    for name, (t_half, iso_frac, rate) in ISOTOPES.items():
        if species is not None and name not in species:
            continue
        total += conc[ELEMENT_OF[name]] * iso_frac * rate * 2.0 ** (-t_gyr / t_half)
    return total


def budget(silicate_mass_kg: float, set_name: str = DEFAULT_SET, t_gyr: float = 0.0) -> dict:
    conc = CONCENTRATION_SETS[set_name]
    total = heat_per_kg(conc, t_gyr) * silicate_mass_kg
    return {"total_w": total, "mantle_w": MANTLE_SHARE * total,
            "crust_w": (1.0 - MANTLE_SHARE) * total, "set": set_name}


def history_factor(t_gyr: float, set_name: str = "appendix",
                   species: tuple[str, ...] | None = None) -> float:
    """H(t)/H(now). t = −4.0 is four billion years AGO. ⚠ The past is the negative argument:
    computed forward once (a future time compared to now), this gives ~1.7 instead of 3.67 — both
    believable, one sign apart.
    ²³⁵U carries the factor (51× over 4 Gyr from 0.38 TW today): prune it and 3.67 becomes 2.8."""
    conc = CONCENTRATION_SETS[set_name]
    return heat_per_kg(conc, t_gyr, species) / heat_per_kg(conc, 0.0, species)


ROCKY_CLASSES = ("rocky", "super_earth", "moon", "icy")
GIANT_CLASSES = ("giant", "gas_giant", "ice_giant", "sub_neptune", "brown_dwarf", "star")


def solve(mass_earth: float, core_mass_fraction: float | None, radius_earth: float | None,
          body_class: str | None, age_gyr: float | None,
          ice_mass_fraction: float = 0.0, potential_temperature: float | None = None,
          tidal_power: float | None = None) -> Result:
    inputs = {"mass_earth": mass_earth, "core_mass_fraction": core_mass_fraction,
              "ice_mass_fraction": ice_mass_fraction,
              "radius_earth": radius_earth, "body_class": body_class, "age_gyr": age_gyr,
              "potential_temperature": potential_temperature, "tidal_power": tidal_power}
    if body_class in GIANT_CLASSES:
        return out_of_domain(
            RECIPE, VERSION,
            f"'{body_class}' 의 내부열은 냉각광도 L(M, age) 이고, 이 레시피는 검증 안 된 냉각 궤적을 "
            "대지 않는다 (dynamo.py 의 갈색왜성 갈래와 같은 거절). 방사성 예산은 규산염 질량에 걸리는 "
            "값이라 여기서는 뜻이 없다.", inputs=inputs, refs=REFS)
    if core_mass_fraction is None:
        return out_of_domain(
            RECIPE, VERSION,
            "core_mass_fraction 이 선언되지 않아 규산염 질량을 잡을 수 없다 — 농도를 걸 조성이 없다. "
            "기본값을 넣지 않는다.", inputs=inputs, refs=REFS)
    # 농도는 **벌크 규산염 1 kg 당** 이다. 핵도 얼음도 규산염이 아니므로 둘 다 뺀다 — 얼음 질량분율을
    # 빼지 않으면 얼음 위성의 얼음 맨틀이 규산염으로 세어져 예산이 ~2배가 된다 (감사, 브리프 44 후속 ①;
    # 브리프 39 의 '다른 층의 온도' 와 같은 병인데 여기서는 빼는 값이 있어 거절 대신 고친다).
    imf = ice_mass_fraction or 0.0
    silicate_frac = 1.0 - core_mass_fraction - imf
    if silicate_frac <= 0.0 or core_mass_fraction < 0.0 or imf < 0.0:
        return out_of_domain(
            RECIPE, VERSION,
            f"규산염 질량분율이 {silicate_frac:.3f} 다 (1 − 핵 {core_mass_fraction} − 얼음 {imf}) — "
            "방사성 예산을 걸 규산염이 없거나 분율 선언이 어긋났다.", inputs=inputs, refs=REFS)
    silicate_kg = mass_earth * M_EARTH_KG * silicate_frac
    b = budget(silicate_kg, DEFAULT_SET)
    b_low = budget(silicate_kg, LOW_SET)
    r_m = (radius_earth or 0.0) * R_EARTH_M
    flux = b["total_w"] / (4.0 * math.pi * r_m ** 2) if r_m > 0.0 else None
    t_int = (flux / SIGMA_SB) ** 0.25 if flux else None
    hist = history_factor(-4.0)
    # Brief 46 — the declared potential temperature, checked against this budget (Nimmo+ 2004 eqs 34–36).
    # Composed here because both ends live here: the budget is this recipe's, the temperature is the
    # declaration interior_layers reads. Nothing in solve()'s physics changes.
    g_body = 6.674e-11 * mass_earth * M_EARTH_KG / r_m ** 2 if r_m > 0.0 else None
    cons = (mantle_flux.consistency(potential_temperature, b["total_w"], g_body, r_m)
            if g_body else {"verdict": "cannot-say (no radius)", "delta_t_km": None, "f_t_w_m2": None,
                            "q_m_w": None, "ratio": None, "notes": ("heat-flow consistency: no radius, no flux.",)})
    # Brief 57 — the same budget inverted: the mantle temperature at which the top boundary layer
    # sheds exactly the radiogenic power. A floor, a family (four named widths), never a point.
    band = (mantle_flux.radiogenic_temperature_band(
                {DEFAULT_SET: {"mantle_w": b["mantle_w"], "total_w": b["total_w"]},
                 LOW_SET: {"mantle_w": b_low["mantle_w"], "total_w": b_low["total_w"]}}, g_body, r_m)
            if g_body else {"verdict": "cannot-say (no radius)", "t_min": None, "t_max": None, "widths": {}})
    w = band["widths"]
    # C30 (2026-09-04) — the heat doc's own instruction (:34 "add the tidal flux into T_int if it is non-negligible"):
    # when tidal_heating supplied a power, emit the TOTAL beside the radiogenic-only values (which do not move), and
    # invert the floor against the total ONLY when the surface passes heat by a boundary layer. Under a heat pipe
    # (tidal doc §6.2, ≥ ~2.5 W/m²) melt carries the heat and Nimmo's top-boundary-layer inversion does not apply —
    # this file already says so of tidally heated bodies (the band note below) — so the total floor is a named refusal.
    total = _total_heat(b, b_low, tidal_power, r_m, g_body, flux)
    band_note = (
        f"맨틀 온도 하한 밴드 (브리프 57, {band['verdict']}): "
        + ((f"{band['t_min']:.0f}" if band['t_min'] is not None else f"< {mantle_flux.BRACKET_K[0]:.0f}")
           + f"–{band['t_max']:.0f} K — 상단 경계층이 방사성 출력만을 내보내는 포텐셜 온도. "
           f"**하한이다**: 영년 냉각은 열류를 더하지 빼지 않는다. 네 폭, 어느 것도 접지 않았다 — "
           f"ζ {mantle_flux.ZETA_RANGE[0]:.3f}–{mantle_flux.ZETA_RANGE[1]:.3f} (Table 2 의 ±0.5): {w['zeta']:.0f} K · "
           f"농도 세트 Earth (1)/(2): {w['set']:.0f} K · 분모 맨틀 몫/총량: {w['denominator']:.0f} K · "
           f"T_s 293→{mantle_flux.BAND_T_S_ALT:.0f} K: {w['surface']:.0f} K. **폭의 정의**: 앞의 셋은 T_s = 293 K 에서 나머지 "
           "두 선언을 고정하고 그 축을 따라 max − min 을 잰 것의 최대(T_s = 200 K 행을 섞어 최대를 잡으면 더 커진다 — "
           "다른 정의다); surface 는 (세트·분모·ζ) 전부에 대한 |T(200 K) − T(293 K)| 의 최대. 모두 이 천체의 g·R·예산으로 "
           f"잰 값이라 천체마다 움직인다. ζ 상단은 모듈 선언 {mantle_flux.ZETA_RANGE[1]:.3f} (Table 2 의 ±0.5) 이고 논문이 "
           "인쇄한 범위의 상단은 0.016 이다. 세 폭이 같은 자릿수라 하나가 지배하지 않는다 — "
           "폭은 구조적이지 골라서 좁힐 것이 아니다. 분모는 맨틀 몫이 like-for-like (F_t 는 상단 경계층을 건너고 지각 "
           "생산은 그 위다; Korenaga 2008 의 대류 Urey 비) 인데 순방향 판정은 총량을 쓴다 — 둘 다 싣고 어느 쪽도 뽑지 않는다."
           if band["t_max"] is not None else
           f"이름 대며 거절 — 이분법 괄호 {mantle_flux.BRACKET_K[0]:.0f}–{mantle_flux.BRACKET_K[1]:.0f} K 밖이라 값을 "
           "내지 않는다 (예전에는 괄호 끝을 값처럼 돌려줬다).")
        + " 조석 가열 천체에서는 이 하한이 맨틀 온도가 아니다. " + mantle_flux.CONDITION + ".")
    notes = (
        f"방사성 예산 (현재값): 규산염 질량 {silicate_kg:.3e} kg (= 질량 × (1 − 핵질량분율 {core_mass_fraction} "
        f"− 얼음질량분율 {imf}), 도출) × "
        f"Earth (1) 콘드라이트 농도(K 260 ppm · Th 85 ppb · U 22 ppb, Palme & O'Neill 2014) → 총 "
        f"{b['total_w'] / 1e12:.2f} TW; 맨틀 몫 70 % = {b['mantle_w'] / 1e12:.2f} TW, 지각 30 % = "
        f"{b['crust_w'] / 1e12:.2f} TW. **농도 세트와 70/30 은 선언이다** (Earth (2) 비콘드라이트 세트로는 "
        f"{b_low['total_w'] / 1e12:.2f} TW — 두 값을 다 싣고 어느 쪽도 뽑지 않는다). 핵종 상수는 표준 "
        "핵데이터이고, Nimmo & Primack 2020 의 **미발표 초안 표**(main.tex \\end{document} 뒤, PDF 에 없음)"
        "에서 읽었으며, 그 표 자신의 21.4 / 10.8 TW 와 부록의 22 TW 에 1–2 % 로 폐합하는 것이 읽기의 검산이다.",
        f"붕괴 이력: H(−4 Gyr)/H(now) = {hist:.2f} (논문 산문 3.5). ²³⁵U 가 그 배율을 끈다 — 지금 "
        f"{heat_per_kg(CONCENTRATION_SETS['appendix'], 0.0, ('U235',)) * BSE_MASS_STANDARD_KG / 1e12:.2f} TW 인 "
        "종을 빼면 2.8 로 준다. **이력은 여기서 끝난다**: 핵이 지금도 대류하는가는 열진화 모형(Nimmo+ 2004)의 몫이다 — "
        "그 논문의 하단 경계층(식 37–39)은 cmb_flux 가 이미 전사했고, dynamo_rocky 로의 배선은 φ(핵 엔트로피 생성) "
        "단계라 지금은 gap 으로 남는다.",
        "소비처 둘(interior_layers 의 포텐셜 온도, core_state 의 핵 쪽 경계 온도)은 이 예산을 받되 **여전히 "
        "선언한다** — 예산을 온도나 경계층 열류로 바꾸는 것은 이 레시피가 갖지 않은 열 모형이다.",
        (f"t_int {t_int:.1f} K 는 **방사성만** 의 값이다 (F = {flux:.4f} W/m², R = {radius_earth:.4f} R⊕ — "
         "선언된 radius_earth; 미선언이면 interior_layers 의 도출 반지름). 방법론 §1 의 '지구 ≈ 35 K' 는 "
         "총 표면 열류 0.087 W/m²(방사성 + 잔열)로 계산한 것이라, 잔열을 갖지 않은 이 값은 그 하한이다."
         if t_int else "반지름이 없어 표면 flux 와 t_int 를 내지 않는다."),
    ) + tuple(cons["notes"]) + (band_note,)
    values = {"l_int": b["total_w"], "t_int": t_int,
              "radiogenic_power": b["total_w"], "mantle_radiogenic_power": b["mantle_w"],
              "crust_radiogenic_power": b["crust_w"], "radiogenic_power_low": b_low["total_w"],
              "radiogenic_heat_w_m2": flux, "radiogenic_power_history_4gyr": hist,
              "mantle_top_boundary_layer": cons["delta_t_km"],
              "implied_surface_heat_flux": cons["f_t_w_m2"],
              "implied_surface_heat_flow": cons["q_m_w"],
              "heat_flow_consistency": cons["verdict"],
              "urey_ratio": cons.get("urey_ratio"),
              "mantle_temperature_floor_min": band["t_min"], "mantle_temperature_floor_max": band["t_max"],
              "mantle_temperature_floor_verdict": band["verdict"],
              "mantle_temperature_width_zeta": w.get("zeta"), "mantle_temperature_width_set": w.get("set"),
              "mantle_temperature_width_denominator": w.get("denominator"),
              "mantle_temperature_width_surface": w.get("surface"),
              "l_int_total": total["l_int_total"], "t_int_total": total["t_int_total"],
              "mantle_temperature_floor_total_min": total["floor_min"], "mantle_temperature_floor_total_max": total["floor_max"],
              "mantle_temperature_floor_total_verdict": total["verdict"]}
    notes = notes + (total["note"],)
    units = {"l_int": "W", "t_int": "K", "radiogenic_power": "W", "mantle_radiogenic_power": "W",
             "l_int_total": "W", "t_int_total": "K", "mantle_temperature_floor_total_min": "K",
             "mantle_temperature_floor_total_max": "K", "mantle_temperature_floor_total_verdict": "",
             "crust_radiogenic_power": "W", "radiogenic_power_low": "W",
             "radiogenic_heat_w_m2": "W/m2", "radiogenic_power_history_4gyr": "dimensionless",
             "mantle_top_boundary_layer": "km", "implied_surface_heat_flux": "W/m2",
             "implied_surface_heat_flow": "W", "heat_flow_consistency": "",
             "urey_ratio": "dimensionless",
             "mantle_temperature_floor_min": "K", "mantle_temperature_floor_max": "K",
             "mantle_temperature_floor_verdict": "", "mantle_temperature_width_zeta": "K",
             "mantle_temperature_width_set": "K", "mantle_temperature_width_denominator": "K",
             "mantle_temperature_width_surface": "K"}
    return Result(recipe=RECIPE, version=VERSION, regime="rocky_radiogenic_present_day",
                  reason=(f"규산염 {silicate_kg:.2e} kg 에 Earth (1) 농도(선언)를 걸어 총 "
                          f"{b['total_w'] / 1e12:.2f} TW, 맨틀 몫 70 %(선언) {b['mantle_w'] / 1e12:.2f} TW."),
                  # 농도 세트와 70/30 이 선언이므로 analog. 지구 자신을 재현하는 것은 폐합이지 예측이 아니다.
                  grade="analog", inputs=inputs, values=values, units=units, refs=REFS, notes=notes)


NO_TIDAL = "cannot-say (no tidal_heating value — total equals radiogenic; nothing added)"
HEAT_PIPE_FLOOR = "cannot-say (heat-pipe regime: the boundary-layer inversion does not apply; radiogenic.py:183)"


def _total_heat(b: dict, b_low: dict, tidal_power: float | None, r_m: float, g_body: float | None,
                radiogenic_flux: float | None) -> dict:
    """Radiogenic + tidal (C30). The floor inversion is re-run against the total only inside a boundary-layer mode."""
    if tidal_power is None:
        return {"l_int_total": None, "t_int_total": None, "floor_min": None, "floor_max": None, "verdict": NO_TIDAL,
                "note": "총 내부열 (C30): tidal_heating 이 값을 내지 않아 총량을 내지 않는다 — 방사성만의 값이 위에 있다."}
    l_total = b["total_w"] + tidal_power
    area = 4.0 * math.pi * r_m ** 2 if r_m > 0.0 else None
    t_total = ((l_total / area) / SIGMA_SB) ** 0.25 if area else None
    total_flux = (l_total / area) if area else None
    import tidal_heating  # 라벨 표는 조석 문서의 것이라 그 모듈이 갖는다 (§6.2, doc :277–281)
    mode = tidal_heating.transport_mode(total_flux) if total_flux is not None else None
    if mode == tidal_heating.MODE_HEAT_PIPE or g_body is None:
        fmin = fmax = None
        verdict = HEAT_PIPE_FLOOR if g_body is not None else "cannot-say (no radius)"
    else:
        # 조석 소산은 맨틀에서 일어난다고 두어 두 분모에 같은 W 를 더한다 — 선언, 그렇게 라벨한다.
        tb = mantle_flux.radiogenic_temperature_band(
            {DEFAULT_SET: {"mantle_w": b["mantle_w"] + tidal_power, "total_w": b["total_w"] + tidal_power},
             LOW_SET: {"mantle_w": b_low["mantle_w"] + tidal_power, "total_w": b_low["total_w"] + tidal_power}}, g_body, r_m)
        fmin, fmax, verdict = tb["t_min"], tb["t_max"], tb["verdict"] + " (total heat: radiogenic + tidal, tidal counted in the mantle — declared)"
    note = (f"총 내부열 (C30, heat doc :34): l_int_total = 방사성 {b['total_w'] / 1e12:.2f} + 조석 {tidal_power / 1e12:.2f} = "
            f"{l_total / 1e12:.2f} TW → 표면 플럭스 {total_flux:.4g} W/m², t_int_total {t_total:.1f} K (방사성만 {radiogenic_flux:.4g} W/m²). "
            f"수송 모드(§6.2 표, 총 플럭스로): **{mode}** → 바닥 역산 " + ("**하지 않음** — " + HEAT_PIPE_FLOOR if fmin is None and mode == tidal_heating.MODE_HEAT_PIPE
            else f"{fmin:.0f}–{fmax:.0f} K (총열; 조석은 맨틀 몫에 더함, 선언)" if fmin is not None else verdict)
            + ". 방사성만의 값들은 그대로다.")
    return {"l_int_total": l_total, "t_int_total": t_total, "floor_min": fmin, "floor_max": fmax, "verdict": verdict, "note": note}


from registry import recipe  # noqa: E402


@recipe("internal_heat_nontidal")
def _from_state(state):
    return solve(mass_earth=state["mass_earth"],
                 core_mass_fraction=state.get("core_mass_fraction"),
                 # 브리프 46 후속 ③: 반지름은 **선언된** radius_earth 가 먼저다 (mass_or_radius 엣지, via radius);
                 # 미선언이면 interior_layers 의 도출 반지름으로 대체한다 — 그 엣지도 chain.yaml 에 선언돼 있다.
                 radius_earth=state.get("radius_earth", state.get("radius")),
                 body_class=state.get("body_class"),
                 age_gyr=state.get("age_gyr"),
                 ice_mass_fraction=state.get("ice_mass_fraction", 0.0),
                 potential_temperature=state.get("potential_temperature"),
                 tidal_power=state.get("power"))                 # C30: tidal_heating's Ė (chain :653 via power); absent → totals not emitted
