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
into a core that is or is not still convecting is Nimmo+ 2004 (`2004GeoJI.156..363N`), not cached,
and the chain.yaml edge to dynamo_rocky stays a gap for that reason. The giant branch (cooling
luminosity L(M, age)) is refused here exactly as `dynamo.py` refuses it.
"""
from __future__ import annotations

import math

from payload import Result, out_of_domain

RECIPE = "internal-heat-luminosity-methodology"
VERSION = "1"
REFS = ("2020ApJ...903L..37N",)     # Nimmo & Primack 2020, ApJL 903, L37 (draft table + appendix)

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
          body_class: str | None, age_gyr: float | None) -> Result:
    inputs = {"mass_earth": mass_earth, "core_mass_fraction": core_mass_fraction,
              "radius_earth": radius_earth, "body_class": body_class, "age_gyr": age_gyr}
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
    silicate_kg = mass_earth * M_EARTH_KG * (1.0 - core_mass_fraction)
    if silicate_kg <= 0.0:
        return out_of_domain(RECIPE, VERSION, "규산염 질량이 0 이다 — 방사성 예산을 걸 곳이 없다.",
                             inputs=inputs, refs=REFS)
    b = budget(silicate_kg, DEFAULT_SET)
    b_low = budget(silicate_kg, LOW_SET)
    r_m = (radius_earth or 0.0) * R_EARTH_M
    flux = b["total_w"] / (4.0 * math.pi * r_m ** 2) if r_m > 0.0 else None
    t_int = (flux / SIGMA_SB) ** 0.25 if flux else None
    hist = history_factor(-4.0)
    notes = (
        f"방사성 예산 (현재값): 규산염 질량 {silicate_kg:.3e} kg (= 질량 × (1 − 핵질량분율), 도출) × "
        f"Earth (1) 콘드라이트 농도(K 260 ppm · Th 85 ppb · U 22 ppb, Palme & O'Neill 2014) → 총 "
        f"{b['total_w'] / 1e12:.2f} TW; 맨틀 몫 70 % = {b['mantle_w'] / 1e12:.2f} TW, 지각 30 % = "
        f"{b['crust_w'] / 1e12:.2f} TW. **농도 세트와 70/30 은 선언이다** (Earth (2) 비콘드라이트 세트로는 "
        f"{b_low['total_w'] / 1e12:.2f} TW — 두 값을 다 싣고 어느 쪽도 뽑지 않는다). 핵종 상수는 표준 "
        "핵데이터이고, Nimmo & Primack 2020 의 **미발표 초안 표**(main.tex \\end{document} 뒤, PDF 에 없음)"
        "에서 읽었으며, 그 표 자신의 21.4 / 10.8 TW 와 부록의 22 TW 에 1–2 % 로 폐합하는 것이 읽기의 검산이다.",
        f"붕괴 이력: H(−4 Gyr)/H(now) = {hist:.2f} (논문 산문 3.5). ²³⁵U 가 그 배율을 끈다 — 지금 "
        f"{heat_per_kg(CONCENTRATION_SETS['appendix'], 0.0, ('U235',)) * BSE_MASS_STANDARD_KG / 1e12:.2f} TW 인 "
        "종을 빼면 2.8 로 준다. **이력은 여기서 끝난다**: 핵이 지금도 대류하는가는 열진화 모형(Nimmo+ 2004, "
        "미보유)의 몫이라 dynamo_rocky 로는 배선하지 않는다.",
        "소비처 둘(interior_layers 의 포텐셜 온도, core_state 의 핵 쪽 경계 온도)은 이 예산을 받되 **여전히 "
        "선언한다** — 예산을 온도나 경계층 열류로 바꾸는 것은 이 레시피가 갖지 않은 열 모형이다.",
        (f"t_int {t_int:.1f} K 는 **방사성만** 의 값이다 (F = {flux:.4f} W/m²). 방법론 §1 의 '지구 ≈ 35 K' 는 "
         "총 표면 열류 0.087 W/m²(방사성 + 잔열)로 계산한 것이라, 잔열을 갖지 않은 이 값은 그 하한이다."
         if t_int else "반지름이 없어 표면 flux 와 t_int 를 내지 않는다."),
    )
    values = {"l_int": b["total_w"], "t_int": t_int,
              "radiogenic_power": b["total_w"], "mantle_radiogenic_power": b["mantle_w"],
              "crust_radiogenic_power": b["crust_w"], "radiogenic_power_low": b_low["total_w"],
              "radiogenic_heat_w_m2": flux, "radiogenic_power_history_4gyr": hist}
    units = {"l_int": "W", "t_int": "K", "radiogenic_power": "W", "mantle_radiogenic_power": "W",
             "crust_radiogenic_power": "W", "radiogenic_power_low": "W",
             "radiogenic_heat_w_m2": "W/m2", "radiogenic_power_history_4gyr": "dimensionless"}
    return Result(recipe=RECIPE, version=VERSION, regime="rocky_radiogenic_present_day",
                  reason=(f"규산염 {silicate_kg:.2e} kg 에 Earth (1) 농도(선언)를 걸어 총 "
                          f"{b['total_w'] / 1e12:.2f} TW, 맨틀 몫 70 %(선언) {b['mantle_w'] / 1e12:.2f} TW."),
                  # 농도 세트와 70/30 이 선언이므로 analog. 지구 자신을 재현하는 것은 폐합이지 예측이 아니다.
                  grade="analog", inputs=inputs, values=values, units=units, refs=REFS, notes=notes)


from registry import recipe  # noqa: E402


@recipe("internal_heat_nontidal")
def _from_state(state):
    return solve(mass_earth=state["mass_earth"],
                 core_mass_fraction=state.get("core_mass_fraction"),
                 radius_earth=state.get("radius", state.get("radius_earth")),
                 body_class=state.get("body_class"),
                 age_gyr=state.get("age_gyr"))
