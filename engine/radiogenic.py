# 암석체의 방사성 가열 예산 — 네 핵종의 현재값과 붕괴 이력, internal_heat_nontidal 의 암석 갈래 (Brief 44)
"""Radiogenic heat budget of a rocky body, present day, plus its decay history.

    from radiogenic import budget, history_factor
    budget(silicate_mass_kg=4.0e24)["total_w"] / 1e12          -> 21.58 TW (Earth (1) set)
    history_factor(-4.0)                                        -> 3.67

⚠ Where the constants come from. The four nuclide constants are **Ruedas 2017 Table 2** (G³ 18, 3530,
PDF p6, rendered), chosen by us outside any chain (pre-registration `prereg-radiogenic.md` §1). Until
2026-09-24 they were read from Nimmo & Primack 2020's unpublished draft table (after `\\end{document}` in
`2020ApJ...903L..37N.src/main.tex`, never compiled); that is no longer their source. The default Earth
concentrations are the published N&P 2020 set (PDF p14), 260 ppm / 23 ppb / 85 ppb.

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
from payload import INPUT_GRADES, Result, out_of_domain, tagged_with_unconverged

RECIPE = "internal-heat-luminosity-methodology"
VERSION = "1"
REFS = (
    "2017GGG....18.3530R",     # Ruedas 2017, G³ 18, 3530 — Table 2, the four nuclide constants (PDF p6)
    "2020ApJ...903L..37N",     # Nimmo & Primack 2020, ApJL 903, L37 — the published Earth set 260/23/85
                               # (PDF p14) and the appendix's 22 TW, 70 %
)

SIGMA_SB = 5.670374419e-8            # W m⁻² K⁻⁴
M_EARTH_KG = 5.972e24
R_EARTH_M = 6.371e6
GYR_S = 1e9 * 365.25 * 86400.0

# Ruedas 2017, G³ 18, 3530 (`2017GGG....18.3530R`), Table 2, PDF p6 (rendered; the arXiv author's final
# manuscript) — pre-registration `prereg-radiogenic.md` §1, replacing N&P 2020's unpublished draft table.
# Per nuclide: half-life My, present atom fraction X_iso, heat per kg of the nuclide W/kg, atomic mass u.
# ⚠ The ²³⁸U row includes ²³⁴U (the table's footnote).
RUEDAS_2017 = {
    "K40":   {"half_life_my": 1248.0,  "x_iso": 1.1668e-4, "h_w_per_kg": 2.8761e-5,  "u": 39.963998166},
    "Th232": {"half_life_my": 14000.0, "x_iso": 1.0,       "h_w_per_kg": 2.6368e-5,  "u": 232.038053689},
    "U235":  {"half_life_my": 704.0,   "x_iso": 0.0072045, "h_w_per_kg": 5.68402e-4, "u": 235.043928190},
    "U238":  {"half_life_my": 4468.0,  "x_iso": 0.9927955, "h_w_per_kg": 9.4946e-5,  "u": 238.050786996},
}
ELEMENT_U = {"K": 39.0983, "Th": 232.038053689, "U": 238.02891}
# The element's printed rates, kept only to check the sum against (acceptance R1, ≤ 3×10⁻⁵ relative):
RUEDAS_2017_ELEMENT_W_PER_KG = {"K": 3.4302e-9, "Th": 2.6368e-5, "U": 9.8314e-5}

# (half-life Gyr, mass fraction of the nuclide in its element, W per kg of the nuclide).
# ⚠ The mass fraction is X_iso · u_iso / u_element — the atom fraction alone was used here until
#   2026-09-24, which made U 0.04 % high. The engine uses the nuclide sum (K 3.430137e-9 W/kg), not the
#   printed element rate (3.4302e-9): one set, the same one the decay runs on (addendum 5).
ELEMENT_OF = {"K40": "K", "Th232": "Th", "U238": "U", "U235": "U"}
ISOTOPES = {name: (row["half_life_my"] / 1000.0, row["x_iso"] * row["u"] / ELEMENT_U[ELEMENT_OF[name]],
                   row["h_w_per_kg"])
            for name, row in RUEDAS_2017.items()}

# Bulk-silicate concentrations (element mass fractions). Neither set is elected; the recipe emits the
# default and the second beside it.
# ⚠ `earth_1_chondritic` is now the PUBLISHED Nimmo & Primack 2020 set, PDF p14: "260 ppm, 23 ppb and 85 ppb
#   respectively for K, U and Th; this produces 22 TW of heat production at the present day" (addendum 2,
#   owner 2026-09-24). U 22 came only from the unpublished draft table (P&O 2014, no lawful open copy).
#   It is now the same set as `appendix`; both names stay, so the callers and the tests keep their names.
CONCENTRATION_SETS = {
    "earth_1_chondritic":      {"K": 260e-6, "Th": 85e-9, "U": 23e-9},   # N&P 2020 published, PDF p14
    # O'Neill & Palme 2008 as the published papers print it — U 10 · Th 40 · K 140 (prereg-radiogenic addendum 10,
    # second-hand: Šrámek+ 2013 — published version EPSL 361, PDF p3, and arXiv 1207.0853 PDF p5 — and Bellini+ 2022
    # arXiv 2109.01482 v1 Tables 16 and 18 (its published version not compared). The draft table's 11 / 43 / 130 is
    # dropped.
    "earth_2_non_chondritic":  {"K": 140e-6, "Th": 40e-9, "U": 10e-9},
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


def budget(silicate_mass_kg: float, set_name: str = DEFAULT_SET, t_gyr: float = 0.0,
           conc: dict[str, float] | None = None) -> dict:
    """`conc` (element mass fractions) overrides the named set — a body's declared concentration."""
    conc = conc if conc is not None else CONCENTRATION_SETS[set_name]
    total = heat_per_kg(conc, t_gyr) * silicate_mass_kg
    return {"total_w": total, "mantle_w": MANTLE_SHARE * total,
            "crust_w": (1.0 - MANTLE_SHARE) * total, "set": set_name}


def history_factor(t_gyr: float, set_name: str = "appendix",
                   species: tuple[str, ...] | None = None, conc: dict[str, float] | None = None) -> float:
    """H(t)/H(now). t = −4.0 is four billion years AGO. ⚠ The past is the negative argument:
    computed forward once (a future time compared to now), this gives ~1.7 instead of 3.67 — both
    believable, one sign apart.
    ²³⁵U carries the factor (51× over 4 Gyr from 0.38 TW today): prune it and 3.67 becomes 2.8."""
    conc = conc if conc is not None else CONCENTRATION_SETS[set_name]
    return heat_per_kg(conc, t_gyr, species) / heat_per_kg(conc, 0.0, species)


# ── A body's declared concentration — prereg-radiogenic §4, R5 ────────────────────────────────
GRADES_DECLARED = ("measured", "literature", "declared")   # what a body file may say (payload.INPUT_GRADES 의 부분)
GRADE_DEFAULT = "declared"     # what the engine says when it says nothing — with `default` True (prereg-grade-vocabulary §1 ④)
assert set(GRADES_DECLARED) <= set(INPUT_GRADES)


def read_concentration(decl) -> tuple[dict[str, float] | None, str, str]:
    """(element mass fractions, grade, label) from a body's `radiogenic_concentration` block, or
    (None, "declared", label) when there is none — the engine default, marked by `default` True in the
    outputs. Raises ValueError, naming what is missing — the caller turns it into a named refusal.
    A deliberately changed set is `grade: declared` with an `override` block: a one-line `reason` and a
    `window` (inside | outside the literature's range); `outside` is printed (the old `owner-override`)."""
    if decl is None:
        return None, GRADE_DEFAULT, (f"농도 선언 없음 — 지구 기본 벌({DEFAULT_SET}: K 260 ppm · Th 85 ppb · U 23 ppb, "
                                     f"N&P 2020 출간본) · 등급 {GRADE_DEFAULT} · 기본 벌")
    if not isinstance(decl, dict):
        raise ValueError("radiogenic_concentration 은 U_ppb · Th_ppb · K_ppm · grade · source 를 가진 블록이어야 한다")
    missing = [k for k in ("U_ppb", "Th_ppb", "K_ppm", "grade") if decl.get(k) is None]
    if missing:
        raise ValueError(f"radiogenic_concentration 에 {', '.join(missing)} 가 없다")
    if "default" in decl:
        raise ValueError("radiogenic_concentration.default 는 천체 파일이 쓸 수 없다 — 엔진이 기본 벌에만 붙인다")
    grade = decl["grade"]
    if grade not in GRADES_DECLARED:
        raise ValueError(f"radiogenic_concentration 의 등급 '{grade}' 는 천체 파일이 쓸 수 없다 — "
                         f"{', '.join(GRADES_DECLARED)} 중 하나 (일부러 바꾼 값은 declared + override)")
    if not decl.get("source"):
        raise ValueError(f"radiogenic_concentration 등급 {grade} 에 source 가 없다")
    label = (f"농도 선언 — U {decl['U_ppb']:g} ppb · Th {decl['Th_ppb']:g} ppb · K {decl['K_ppm']:g} ppm · "
             f"등급 {grade} · 출처 {decl['source']}")
    if grade == "declared":
        ov = decl.get("override")
        if not isinstance(ov, dict):
            raise ValueError("radiogenic_concentration 등급 declared 에 override 블록(reason · window)이 없다")
        if not ov.get("reason"):
            raise ValueError("radiogenic_concentration.override 에 까닭 한 줄(reason)이 없다")
        if ov.get("window") not in ("inside", "outside"):
            raise ValueError("radiogenic_concentration.override 의 window 는 inside 또는 outside 여야 한다")
        label += f" · 까닭 «{ov['reason']}» · 문헌 창 {ov['window']}"
        if ov["window"] == "outside":
            label += " — ⚠ 문헌 창 밖"
    elif "override" in decl:
        raise ValueError(f"radiogenic_concentration.override 는 등급 declared 에만 붙는다 — 지금 {grade}")
    conc = {"U": float(decl["U_ppb"]) * 1e-9, "Th": float(decl["Th_ppb"]) * 1e-9, "K": float(decl["K_ppm"]) * 1e-6}
    return conc, grade, label


GRADES_ALTERNATIVE = ("measured", "literature", "declared")


def read_alternative(decl) -> tuple[dict[str, float] | None, str]:
    """The optional pair set of a declaration (`alternative`, prereg-radiogenic addendum 9): with it, `_low`
    and the temperature band's union stay; without it a declared body has no pair (decision A).
    Its grade may be `declared` with `default: true` — a set carried with no source held (the old
    `declared-default`) — and then it is recorded and NOT used: only a `measured` or `literature` pair
    keeps `_low` and the band's union (addendum 9 supplement)."""
    if not isinstance(decl, dict) or decl.get("alternative") is None:
        return None, ""
    alt = decl["alternative"]
    missing = [k for k in ("U_ppb", "Th_ppb", "K_ppm", "grade", "source") if not alt.get(k) and alt.get(k) != 0]
    if missing:
        raise ValueError(f"radiogenic_concentration.alternative 에 {', '.join(missing)} 가 없다")
    if alt["grade"] not in GRADES_ALTERNATIVE:
        raise ValueError(f"alternative 의 등급 '{alt['grade']}' — {', '.join(GRADES_ALTERNATIVE)} 중 하나여야 한다")
    if (alt["grade"] == "declared") != (alt.get("default") is True):
        raise ValueError("alternative 의 등급 declared 는 default: true 와만 함께 온다 (근거 없이 실은 짝 벌)")
    label = (f"짝 벌 — U {alt['U_ppb']:g} ppb · Th {alt['Th_ppb']:g} ppb · K {alt['K_ppm']:g} ppm · "
             f"등급 {alt['grade']} · 출처 {alt['source']}")
    if alt["grade"] == "declared":
        return None, label + " — declared(기본) 짝은 싣지 않는다(_low 빔, 밴드 한 세트)"
    return ({"U": float(alt["U_ppb"]) * 1e-9, "Th": float(alt["Th_ppb"]) * 1e-9, "K": float(alt["K_ppm"]) * 1e-6},
            label)


ROCKY_CLASSES = ("rocky", "super_earth", "moon", "icy")
GIANT_CLASSES = ("giant", "gas_giant", "ice_giant", "sub_neptune", "brown_dwarf", "star")


def solve(mass_earth: float, core_mass_fraction: float | None, radius_earth: float | None,
          body_class: str | None, age_gyr: float | None,
          ice_mass_fraction: float = 0.0, potential_temperature: float | None = None,
          tidal_power: float | None = None, radiogenic_concentration: dict | None = None) -> Result:
    inputs = {"mass_earth": mass_earth, "core_mass_fraction": core_mass_fraction,
              "ice_mass_fraction": ice_mass_fraction,
              "radius_earth": radius_earth, "body_class": body_class, "age_gyr": age_gyr,
              "potential_temperature": potential_temperature, "tidal_power": tidal_power,
              "radiogenic_concentration": radiogenic_concentration}
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
    try:
        conc, grade, conc_label = read_concentration(radiogenic_concentration)
    except ValueError as e:
        return out_of_domain(RECIPE, VERSION, f"거절: {e}", inputs=inputs, refs=REFS)
    try:
        alt, alt_label = read_alternative(radiogenic_concentration)
    except ValueError as e:
        return out_of_domain(RECIPE, VERSION, f"거절: {e}", inputs=inputs, refs=REFS)
    b = budget(silicate_kg, DEFAULT_SET, conc=conc)
    # decision A (addendum 1): a declared value has no pair — `_low` is emptied, with the reason — unless the
    # declaration carries its own pair, `alternative` (addendum 9)
    b_low = (budget(silicate_kg, LOW_SET) if conc is None
             else budget(silicate_kg, LOW_SET, conc=alt) if alt is not None else None)
    r_m = (radius_earth or 0.0) * R_EARTH_M
    flux = b["total_w"] / (4.0 * math.pi * r_m ** 2) if r_m > 0.0 else None
    t_int = (flux / SIGMA_SB) ** 0.25 if flux else None
    hist = history_factor(-4.0) if conc is None else history_factor(-4.0, conc=conc)
    # Brief 46 — the declared potential temperature, checked against this budget (Nimmo+ 2004 eqs 34–36).
    # Composed here because both ends live here: the budget is this recipe's, the temperature is the
    # declaration interior_layers reads. Nothing in solve()'s physics changes.
    g_body = 6.674e-11 * mass_earth * M_EARTH_KG / r_m ** 2 if r_m > 0.0 else None
    cons = (mantle_flux.consistency(potential_temperature, b["total_w"], g_body, r_m)
            if g_body else {"verdict": "cannot-say (no radius)", "delta_t_km": None, "f_t_w_m2": None,
                            "q_m_w": None, "ratio": None, "notes": ("heat-flow consistency: no radius, no flux.",)})
    # Brief 57 — the same budget inverted: the mantle temperature at which the top boundary layer
    # sheds exactly the radiogenic power. A floor, a family (four named widths), never a point.
    band_sets = {DEFAULT_SET if conc is None else "declared": {"mantle_w": b["mantle_w"], "total_w": b["total_w"]}}
    if b_low is not None:
        band_sets[LOW_SET if conc is None else "alternative"] = {"mantle_w": b_low["mantle_w"], "total_w": b_low["total_w"]}
    band = (mantle_flux.radiogenic_temperature_band(band_sets, g_body, r_m)
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
        + ((f"{band['t_min']:.0f}" if band['t_min'] is not None else f"< {mantle_flux.INVERSION_BRACKET_K[0]:.0f}")
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
           f"이름 대며 거절 — 이분법 괄호 {mantle_flux.INVERSION_BRACKET_K[0]:.0f}–{mantle_flux.INVERSION_BRACKET_K[1]:.0f} K 밖이라 값을 "
           "내지 않는다 (예전에는 괄호 끝을 값처럼 돌려줬다).")
        + " 조석 가열 천체에서는 이 하한이 맨틀 온도가 아니다. " + mantle_flux.CONDITION + ".")
    conc_name = ("Earth (1) 농도(K 260 ppm · Th 85 ppb · U 23 ppb, Nimmo & Primack 2020 출간본 PDF 14 쪽)"
                 if conc is None else "선언 농도")
    low_text = (f"{'Earth (2) 비콘드라이트 세트' if conc is None else '선언의 짝 벌'}로는 {b_low['total_w'] / 1e12:.2f} TW"
                " — 두 값을 다 싣고 어느 쪽도 뽑지 않는다"
                if b_low is not None else
                "선언값에는 짝 세트가 없어 radiogenic_power_low 를 비운다(결정 A) — 온도 밴드의 세트 폭도 한 세트라 0")
    notes = (
        conc_label + (f" · {alt_label}" if alt_label else ""),
        f"방사성 예산 (현재값): 규산염 질량 {silicate_kg:.3e} kg (= 질량 × (1 − 핵질량분율 {core_mass_fraction} "
        f"− 얼음질량분율 {imf}), 도출) × {conc_name} → 총 "
        f"{b['total_w'] / 1e12:.2f} TW; 맨틀 몫 70 % = {b['mantle_w'] / 1e12:.2f} TW, 지각 30 % = "
        f"{b['crust_w'] / 1e12:.2f} TW. **농도와 70/30 은 선언이다** ({low_text}). 핵종 상수는 표준 "
        "핵데이터로 Ruedas 2017 Table 2(PDF 6 쪽)에서 읽었고 원소 1 kg 당 핵종 질량(X_iso·u_iso/u_원소)으로 가중한다. "
        "검산은 그 표의 원소값(U 9.8314e-5 · Th 2.6368e-5 · K 3.4302e-9 W/kg)을 상대 3e-5 안으로 내는 것이다.",
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
              "crust_radiogenic_power": b["crust_w"],
              "radiogenic_power_low": b_low["total_w"] if b_low is not None else None,
              "radiogenic_concentration_grade": grade,
              "radiogenic_concentration_default": radiogenic_concentration is None,
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
             "crust_radiogenic_power": "W", "radiogenic_power_low": "W", "radiogenic_concentration_grade": "", "radiogenic_concentration_default": "",
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
HEAT_PIPE_FLOOR = ("cannot-say (heat-pipe regime: the boundary-layer inversion does not apply; "
                   "radiogenic.py@«def _total_heat(»)")   # 자기 인용은 코드 줄이 아니라 함수 정의를 가리킨다 — 인용문이
                                                       # 그 코드 줄을 그대로 담으면 매치가 둘이 된다


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
    # 라벨 표는 조석 문서의 것이라 그 모듈이 갖는다. 여기서 `doc` 는 이 파일의 RECIPE(열 문서)를 뜻하므로
    # 표의 주인 문서를 이름으로 적는다 — tidal-heating-methodology.md@«### 6.2 How the heat actually leaves: the three-mode ladder»
    import tidal_heating
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
    note = (f"총 내부열 (C30, heat doc @«here folds in only the non-tidal sources (add the tidal flux into `T_int` if it is»): l_int_total = 방사성 {b['total_w'] / 1e12:.2f} + 조석 {tidal_power / 1e12:.2f} = "
            f"{l_total / 1e12:.2f} TW → 표면 플럭스 {total_flux:.4g} W/m², t_int_total {t_total:.1f} K (방사성만 {radiogenic_flux:.4g} W/m²). "
            f"수송 모드(§6.2 표, 총 플럭스로): **{mode}** → 바닥 역산 " + ("**하지 않음** — " + HEAT_PIPE_FLOOR if fmin is None and mode == tidal_heating.MODE_HEAT_PIPE
            else f"{fmin:.0f}–{fmax:.0f} K (총열; 조석은 맨틀 몫에 더함, 선언)" if fmin is not None else verdict)
            + ". 방사성만의 값들은 그대로다.")
    return {"l_int_total": l_total, "t_int_total": t_total, "floor_min": fmin, "floor_max": fmax, "verdict": verdict, "note": note}


from registry import recipe  # noqa: E402


@recipe("internal_heat_nontidal")
def _from_state(state):
    # C71: 미수렴 입력을 읽었으면 여기서 표지가 붙고 등급에 상한이 걸린다.
    return tagged_with_unconverged(solve(mass_earth=state["mass_earth"],
                 core_mass_fraction=state.get("core_mass_fraction"),
                 # 브리프 46 후속 ③: 반지름은 **선언된** radius_earth 가 먼저다 (mass_or_radius 엣지, via radius);
                 # 미선언이면 interior_layers 의 도출 반지름으로 대체한다 — 그 엣지도 chain.yaml 에 선언돼 있다.
                 radius_earth=state.get_optional("radius_earth", state.get_optional("radius")),   # C45 (b)
                 body_class=state.get("body_class"),
                 age_gyr=state.get("age_gyr"),
                 ice_mass_fraction=state.get("ice_mass_fraction", 0.0),
                 potential_temperature=state.get("potential_temperature"),
                 # C30: tidal_heating's Ė (chain :653 via power); absent → totals not emitted. The contract calls this
                 # `tidal_power`, the state key is the generic `power`: today tidal_heating is the only emitter of that
                 # name, and if a second node ever emits `power` this line would silently add the wrong term.
                 tidal_power=state.get("power"),
                 # prereg-radiogenic §4: a body's declared U · Th · K; absent → the Earth default, graded so
                 radiogenic_concentration=state.get_optional("radiogenic_concentration")), state)
