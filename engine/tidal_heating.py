# 조석 가열 — fixed-Q 식으로 Ė·표면 플럭스를 내고(§1), 표면 열수송 모드·결과 분류 라벨을 붙인다(§6.1·§6.2); C30
"""Tidal heating from the fixed-Q law (`tidal-heating-methodology.md`), plus the two label sets §6 attaches to it.

    Ė = (21/2) · (k₂/Q) · G M_p² R⁵ n e² / a⁶,   n = √(G M_p / a³)   (doc @«Ė  =  (21/2) · (k₂/Q) · (G M_p² R⁵ n e²) / a⁶»; m ≪ M_p)
    F = Ė / (4πR²)                                                 (doc @«`F = Ė / (4πR²)`, the number that decides volcanism/melting»)

Two recipes live here because both are the same document's outputs:
- `tidal_heating` — `power` [W], `surface_flux` [W/m²], `io_power_ratio` [—], `heat_transport_regime` (the §6.1 outcome
  table, doc @«### 6.1 The flux → regime table», strings verbatim; the 10⁻³–10⁻² decade has no row → "unclassified (between table rows)").
- `heat_transport_mode` — `mode` (the §6.2 table, doc @«### 6.2 How the heat actually leaves: the three-mode ladder»: plate tectonics · stagnant lid · heat pipe), judged on the
  **total** surface flux (tidal + radiogenic, the latter as l_int / 4πR² from `internal_heat_nontidal`).
  `resurfacing_rate` is declared in chain.yaml and NOT emitted — the document prints no formula for it.

Both tables are "guides, not sharp lines" (doc @«(these are guides, not sharp lines):») and "there is no published W/m² boundary between the modes"
(doc @«published W/m² boundary** between the modes»); the labels carry that. Not emitted in this version: `radius_ceiling` and `plains_temperature` (the §6.3–6.5
Dante axis — a separate item), and `tidal_transport.derive_potential_temperature` is not consulted (its own docstring
labels it validation-failed, and Pandora is not a §6 lid-bearing case, doc @«**Scope — lid-bearing bodies only.**»).

Inputs `eccentricity_forced` and `k2_over_q` are DECLARATIONS (the board fits k₂/Q, phase4/alpha_centauri.yaml@«The tidal term needs k₂/Q ≈ 0.0016 at the simulated e ≈ 0.005, which is fitted rather than predicted, but it»); the
result says so. Missing orbit or k₂/Q → cannot-say by name, never a default.
"""
from __future__ import annotations

import math

from bands import Band, Choice
from payload import Result, out_of_domain

# Anchors for the sentences the values below stand on. They are cited here rather than inside the
# shipped strings, because a citation that reaches a reader should be short: the string says §6.2,
# this comment says which sentence, and check_refs resolves the comment.
#   the law            doc @«Ė  =  (21/2) · (k₂/Q) · (G M_p² R⁵ n e²) / a⁶»
#   the flux           doc @«`F = Ė / (4πR²)`, the number that decides volcanism/melting»
#   mean motion        doc @«with the mean motion `n = √(G(M_p + m)/a³) ≈ √(G M_p / a³)`»
#   §6.1 label table   doc @«### 6.1 The flux → regime table»
#   §6.2 mode table    doc @«### 6.2 How the heat actually leaves: the three-mode ladder»
#   §6.3 lid scope     doc @«**Scope — lid-bearing bodies only.**»
#   §6.5 size ceiling  doc @«### 6.5 The super-Io ceiling: what size a lava moon can be»
#   Io calibration     doc @«output at ~10¹⁴ W, i.e. a surface flux ~2 W/m²»
#   k₂/Q spread        doc @«`k₂/Q` is the **dominant uncertainty**»
#   R³ flux scaling    doc @«**surface flux scales as `R³` at fixed density**»
RECIPE = "tidal-heating-methodology"
VERSION = "1"
REFS = ("docs/reference/tidal-heating-methodology.md@«Ė  =  (21/2) · (k₂/Q) · (G M_p² R⁵ n e²) / a⁶»", ":99-100", ":264-269", ":295-299")

G = 6.67430e-11            # m³ kg⁻¹ s⁻², CODATA 2018
M_EARTH_KG = 5.9722e24     # IAU 2015 B3 nominal
R_EARTH_M = 6.371e6
# Io's tidal output as the document prints it: "~10¹⁴ W" (doc @«output at ~10¹⁴ W, i.e. a surface flux ~2 W/m²»). The Dante rows of §6.5 (doc @«### 6.5 The super-Io ceiling: what size a lava moon can be»)
# imply 1.016e14 W when inverted (2.44 W/m² at R 1822 km) — 1.6 % from this constant; that is a convention difference.
IO_POWER_W = 1.0e14
# Two Io flux anchors with different sources: ~2 W/m² = Veeder+ 2012 (2012Icar..219..701V, ABSENT from the cache);
# 2.5 W/m² = Kankanamge & Moore 2019 (2019JGRE..124..114K, HELD; doc @«| **Heat pipe** | melt migrates through the lid and erupts | Io's own melt flux, 2.5 W/m²; a floor, not a boundary»,
# doc @«**Do not transcribe Kankanamge §6's "totaling ∼1 TW".**»). Neither is used in a verdict here.
IO_FLUX_VEEDER_W_M2 = 2.0
IO_FLUX_KM2019_W_M2 = 2.5

# §6.1 outcome table, doc @«### 6.1 The flux → regime table» — strings verbatim
REGIME_VIGOROUS = "vigorous silicate volcanism, possible magma ocean"
REGIME_ACTIVE = "active resurfacing, episodic volcanism"
REGIME_OCEAN = "enough to maintain a subsurface ocean under an ice shell"
REGIME_DEAD = "geologically dead; no ocean, no plumes from tides alone"
# "unclassified" is not a classifier failure — it is the band where the DOCUMENT prints no row.
# The two tables have different empty bands, so the two labels must not read alike: a value's
# consumer could not tell which table declined to answer when both said the same words.
REGIME_UNCLASSIFIED = "unclassified — §6.1 prints no row for this flux"
# §6.2 transport-mode table, doc @«### 6.2 How the heat actually leaves: the three-mode ladder»
MODE_PLATE = "plate tectonics"
MODE_STAGNANT = "stagnant lid"
MODE_HEAT_PIPE = "heat pipe"
MODE_UNCLASSIFIED = ("unclassified — §6.2 prints no boundary for this flux; §6.1's own figure for Io, "
                     "~2 W/m², lands in this band too")
# 정체뚜껑 상한은 **문서가 양끝을 다 인쇄한** 유일한 문턱이다 (10–30 mW/m², Reese+ 1998).
# 코드는 그동안 위쪽 끝만 썼다 — 폭을 버린 게 아니라 한쪽 끝을 조용히 고른 것이었다.
# 여기서는 밴드로 싣고, 어느 끝이 서 있는지는 아래 선택지가 말한다.
# doc @«| **Stagnant lid** | conduction through an immobile lid | ceiling **10–30 mW/m²** | Venus 10–20, Mars 15–30»
STAGNANT_LID_CEILING = Band(0.030, 0.010, 0.030,
                            "tidal-heating-methodology §6.2 prints the ceiling as 10–30 mW/m² "
                            "(Reese, Solomatov & Moresi 1998, 1998JGR...10313643R)",
                            "calibrated")
# 이 밴드는 **분류기**로 들어간다 — 소비처가 식이 아니라 라벨표라 폭이 통과하지 못하고 **갈래로 쪼개진다**.
# 그래서 엔진이 조용히 고르지 않고 선택지를 낸다 (C32 ②).
STAGNANT_LID_CEILING_CHOICE = Choice(
    at="heat_transport_mode",
    quantity="stagnant-lid ceiling [W/m²]",
    candidates=({"value": 0.010, "end": "low", "grade": "calibrated",
                 "source": "§6.2, Reese+ 1998 — the low end of the printed 10–30 mW/m² ceiling"},
                {"value": 0.030, "end": "high", "grade": "calibrated",
                 "source": "§6.2, Reese+ 1998 — the high end, and what this code has used all along"}),
    consequences={
        "solar-system control": "at 0.030 three of the four control bodies get the document's own "
                                "label (Mercury 15.75, Earth 41.80, Mars 15.87 mW/m² agree; Venus at "
                                "37.75 does not, and it is the document's own stagnant-lid anchor). "
                                "At 0.010 that becomes one of four — Mercury and Mars leave stagnant "
                                "lid as well.",
        "what the loser becomes": "the table has nothing between the ceiling and the plate row, so a "
                                  "body under the ceiling is not called unknown, it is called plate "
                                  "tectonics. At 0.010 that positive claim is made about Mercury and "
                                  "Mars, which the same table lists as stagnant lid.",
    },
    default=0.030,
    note="the owner has already said this one goes to the player as a choice; the default keeps "
         "today's behaviour until it does")

# The two sentences these labels rest on: doc @«(these are guides, not sharp lines):»
# and doc @«published W/m² boundary** between the modes». They are cited here, in a comment, and
# NOT inside the shipped string: a value's reader gets the pointer, not the document's prose.
GUIDES = "§6: guides, not sharp lines, and no published W/m² boundary between the modes"

# ── C46 (b): 열류로 체제 한 칸을 고르지 않고, **양립 가능한 체제 집합**을 낸다 ─────────────
# 오너 결정 2026-09-07. 문헌은 이 체제들을 **열류로 가르지 않는다** — Lourenço+ 2020 §3.4 의
# 판별자는 mobility(= v_rms 표면/맨틀)와 quiescent plateness(변형 80 % 가 일어나는 면적 분율)
# 이고, 둘 다 4.5 Gyr 시뮬레이션의 출력이라 관측 못 하는 천체에는 잴 수 없다. 그래서 **여기서
# 열류 문턱을 새로 만들지 않는다.** 하는 일은 하나뿐이다 — 문헌이 각 체제에 대해 **실제로
# 인쇄한 열류 값**을 모아 두고, 우리 계산값이 그 인쇄 구간 **밖일 때만 배제**한다.
# 열류는 **체**이지 분류기가 아니고, 대개 배제도 못 한다.
#
# ⚠ 인쇄된 것은 TW 이고 지구 크기 모형에 대한 값이다(Lourenço §2: *"realistic parameter values
# and physics descriptive of planet Earth"*). TW ↔ W/m² 변환은 **우리 것**이므로 라벨한다.
# ⚠ 그리고 인쇄값은 **성분별**이다 — 자기(magmatic)와 전도(conductive)가 따로 나오고, 각 체제에서
# 한쪽만 수로 인쇄되고 다른 쪽은 "낮다/중간" 같은 말이다. 우리 엔진이 내는 것은 **총 플럭스**라,
# 한 성분만 수로 묶인 체제는 총합에 대한 **상한이 없다**. 그래서 대부분 배제가 안 된다.
EARTH_AREA_M2 = 4.0 * math.pi * R_EARTH_M ** 2

#: 체제별로 문헌이 인쇄한 것. (성분, 하한 TW, 상한 TW, 근거). 상한 None = 인쇄된 총합 상한 없음.
#: 전부 Lourenço+ 2020 §4.3, 지구 크기 모형, 마지막 2 Gyr 평균.
REGIME_PRINTED_TW = {
    # ⚠ 정정 2026-09-07: 어제 이 항목을 "전도 성분만 인쇄, 총합 상한 없음" 으로 적었는데 **틀렸다.**
    # 같은 절이 **총합**을 인쇄한다 — 지휘석이 원문에서 찾았고 이 좌석이 놓쳤다. mobile lid 만은
    # 총합 양쪽이 다 묶이고, 나머지 셋은 여전히 한 성분의 상한뿐이다.
    "mobile lid": [("total", 40.0, 50.0,
                    "Lourenço+ 2020 (2020GGG....2108756L) §4.3: «the total surface heat flow (i.e., the sum of magmatic and conductive heat flows) for cases with a mobile lid obtained in our simulations are ∼40–50 TW»")],
    "stagnant lid": [("magmatic", None, 35.0,
                      "Lourenço+ 2020 (2020GGG....2108756L) §4.3: «cases in the stagnant-lid regime show a strong increase in the magmatic heat flow with increasing eruption efficiency, with values as high as 30–35 TW»"),
                     ("conductive", None, None, "printed as 'generally low', no number")],
    "episodic lid": [("magmatic", None, 20.0,
                      "Lourenço+ 2020 (2020GGG....2108756L) §4.3: «the magmatic heat flow increases slightly (up to 20 TW) with increasing surface yield stress»"),
                     ("conductive", None, None, "printed as 'intermediate', no number")],
    "plutonic-squishy lid": [("magmatic", None, 10.0,
                              "Lourenço+ 2020 (2020GGG....2108756L) §4.3: «the magmatic heat flux is also low, and always increases by a small amount with both increasing yield stress and eruption rate, up to ∼10 TW»"),
                             ("conductive", None, None,
                              "printed as 'intermediate', and 'very high compared to a planet covered with a stagnant lid' — relational, no number")],
    # ⚠ 열파이프는 별개 체제가 아니다. Lourenço §3.4 기준 (3): 정체뚜껑 조건 + 용출효율 100 %.
    "heat pipe (a stagnant-lid sub-case)": [("total", None, None,
                                             "no flux printed for this sub-case; it is defined by eruption efficiency, not by flux")],
}


#: ⚠ **넷째 출처 단어.** `bands.py` 의 printed/chosen/unchosen 도 `provisional.PROVISIONAL` 도 아니다.
#: 이 사다리의 눈금은 **경계를 잰 값이 아니라 우리가 아는 천체가 실제로 내는 값**이다. §6.2 자신이
#: 그렇게 적는다 — doc @«**0.09 W/m² is Earth** and **10–30 mW/m² is the Venus and Mars pair.**»
#: 그래서 이 사다리는 분류기가 아니라 **유추 눈금**이고, 하는 말은 *"지구만 한 열이면 지구만 한
#: 지각"* 이다. 그 문장이 출력에 그대로 실려야 한다.
ANALOGY_RUNG = "analogy-rung"

#: 오름차순. 천체의 총 플럭스가 넘긴 눈금 중 **가장 높은 것**의 칸으로 확정한다 (오너 결정
#: 2026-09-07). 천장이 없어도 사다리가 서고, 맨 위 칸에 천장이 없으니 `unclassified` 가 사라진다.
#: ⚠ **사다리 규칙은 우리 것이다.** 문헌은 열류로 체제를 가르지 않는다 — 판별자는 mobility 와
#: plateness 이고(Lourenço §3.1·§3.3) 둘 다 4.5 Gyr 시뮬레이션 출력이라 관측할 수 없다. 문서가
#: 적어 둔 *"어떤 플럭스 문턱이든 환산이지 인용이 아니다"* 는 이제 이 사다리에 대한 정확한 설명이다.
REGIME_LADDER = (
    ("stagnant lid", 0.010,
     "§6.2 prints 10–30 mW/m² for the Venus and Mars pair. ⚠ ORIGINALLY A CEILING, USED HERE AS A "
     "FLOOR — the form changed, and the value did not"),
    ("plate tectonics", 0.09,
     "§6.2 prints 0.09 W/m² for Earth. ⚠ Independently bracketed: Lourenço+ 2020 §4.3's mobile-lid "
     "total of 40–50 TW is 0.0784–0.0980 W/m² over Earth's area, and 0.09 falls inside it; that "
     "paper's own Earth reference is 44.4 TW = 0.0870 W/m² (Turcotte & Schubert 2014)"),
    ("heat pipe", 2.5,
     "§6.2 prints Io's 2.5 W/m², and the document already calls it a floor rather than a boundary"),
)
BELOW_LADDER = "below the lowest rung — no known body anchors this range"


def regime_ladder_cell(total_flux_w_m2: float) -> tuple:
    """확정 칸 하나. (칸, 눈금값, 그 눈금의 근거) — 넘긴 눈금 중 가장 높은 것.

    ⚠ 이것은 문헌의 판정이 아니라 **우리 규칙**이고, 눈금은 천체가 내는 값이지 경계가 아니다."""
    passed = [(n, f, w) for n, f, w in REGIME_LADDER if total_flux_w_m2 >= f]
    if not passed:
        return (BELOW_LADDER, None,
                f"{total_flux_w_m2:.4g} W/m² is under the lowest rung {REGIME_LADDER[0][1]:g}; no "
                f"known body sits here, so the ladder has nothing to compare it with")
    return passed[-1]


def regime_candidates(total_flux_w_m2: float, radius_earth: float) -> dict:
    """이 열류와 **양립 가능한** 체제 집합. 배제는 인쇄된 구간 밖일 때만 한다 (C46 (b)).

    반환: {체제: (판정, 이유)} — 판정은 "compatible" · "excluded" · "cannot decide".
    ⚠ 단일 체제 이름을 내지 않는다. 후보가 하나로 좁혀지는 것은 이 축에서 거의 일어나지 않는다."""
    area = 4.0 * math.pi * (radius_earth * R_EARTH_M) ** 2
    tw = total_flux_w_m2 * area / 1e12
    out = {}
    for regime, parts in REGIME_PRINTED_TW.items():
        lo = max((p[1] for p in parts if p[1] is not None), default=None)
        hi = min((p[2] for p in parts if p[2] is not None), default=None)
        # 총합에 대한 상한은 **모든** 성분이 수로 인쇄됐을 때만 성립한다.
        bounded_above = hi is not None and all(p[2] is not None for p in parts)
        if lo is None and hi is None:
            out[regime] = ("cannot decide", "no flux value is printed for this regime")
        elif lo is not None and tw < lo:
            out[regime] = ("excluded", f"{tw:.3g} TW is below the printed {lo:g} TW floor")
        elif bounded_above and tw > hi:
            out[regime] = ("excluded", f"{tw:.3g} TW is above the printed {hi:g} TW ceiling")
        else:
            why = f"{tw:.3g} TW is inside the printed range" if lo is not None else \
                  f"one component is printed (≤ {hi:g} TW) and the other only in words, so the total has no printed ceiling"
            out[regime] = ("compatible", why)
    return out


def tidal_power(k2_over_q: float, perturber_kg: float, radius_m: float, a_m: float, e: float) -> tuple[float, float, float]:
    """(Ė [W], F [W/m²], n [rad/s]) — doc @«Ė  =  (21/2) · (k₂/Q) · (G M_p² R⁵ n e²) / a⁶», doc @«`F = Ė / (4πR²)`, the number that decides volcanism/melting»."""
    n = math.sqrt(G * perturber_kg / a_m ** 3)
    power = 10.5 * k2_over_q * G * perturber_kg ** 2 * radius_m ** 5 * n * e ** 2 / a_m ** 6
    return power, power / (4.0 * math.pi * radius_m ** 2), n


def outcome_regime(flux_w_m2: float) -> str:
    """§6.1 table, doc @«### 6.1 The flux → regime table». The decade 10⁻³–10⁻² has no row."""
    if flux_w_m2 >= 1.0:
        return REGIME_VIGOROUS
    if flux_w_m2 >= 0.1:
        return REGIME_ACTIVE
    if flux_w_m2 >= 0.01:
        return REGIME_OCEAN
    if flux_w_m2 <= 1e-3:
        return REGIME_DEAD
    return REGIME_UNCLASSIFIED


def transport_mode(total_flux_w_m2: float, stagnant_lid_ceiling: float | None = None) -> str:
    """§6.2 table, doc @«### 6.2 How the heat actually leaves: the three-mode ladder», read on the total surface flux. Plate tectonics sits at ~0.09 W/m² (Earth 92.1 mW/m²);
    the stagnant-lid ceiling is 10–30 mW/m² — **both ends printed**, and which one is in force is
    `STAGNANT_LID_CEILING_CHOICE`, defaulting to the high end; heat pipe from ≥ ~2.5 W/m². Between 0.14 (the plate row read at +50 %, the
    branch below) and 2.5 W/m² the table has no row."""
    ceiling = STAGNANT_LID_CEILING.high if stagnant_lid_ceiling is None else stagnant_lid_ceiling
    if total_flux_w_m2 >= IO_FLUX_KM2019_W_M2:
        return MODE_HEAT_PIPE
    if total_flux_w_m2 <= ceiling:
        return MODE_STAGNANT
    # ⚠ AUTHORED. The 0.09 is printed (Earth); the ×1.5 is not — no paper prints a ±50 % width for
    # that row, and this line invents a lower edge for the band so it has one. Consequence today,
    # measured: none. No roster body's total flux falls between 0.135 and 2.5 — Earth is 0.0418, well
    # under, and Pandora is 45.36, well over — so no verdict in this engine depends on where the edge
    # sits. It is written here rather than hidden because the next body could land in that gap.
    if total_flux_w_m2 <= 0.09 * 1.5:
        return MODE_PLATE
    return MODE_UNCLASSIFIED


def solve(mass_earth: float, radius_earth: float | None, semi_major_axis_km: float | None,
          perturber_mass_earth: float | None, eccentricity_forced: float | None, k2_over_q: float | None) -> Result:
    # km, not m: this is the key a body declares (`semi_major_axis_km`, e.g. bodies/pandora.yaml), and the contract is
    # only a signature if the name it prints is the name that works. The law wants metres, so convert at the call.
    semi_major_axis_m = semi_major_axis_km * 1e3 if semi_major_axis_km is not None else None
    inputs = {"mass_earth": mass_earth, "radius_earth": radius_earth, "semi_major_axis_km": semi_major_axis_km,
              "perturber_mass_earth": perturber_mass_earth, "eccentricity_forced": eccentricity_forced,
              "k2_over_q": k2_over_q}
    missing = [k for k, v in (("semi_major_axis", semi_major_axis_m), ("perturber_mass", perturber_mass_earth),
                              ("eccentricity_forced", eccentricity_forced)) if v is None]
    if missing:
        return out_of_domain(RECIPE, VERSION, f"cannot-say (no orbit): {', '.join(missing)} 미선언 — Ė ∝ M_p² e²/a⁶ (§1의 fixed-Q 식)",
                             inputs, REFS)
    if k2_over_q is None:
        return out_of_domain(RECIPE, VERSION, "cannot-say (no k2_over_q): 조석 소산 k₂/Q 미선언 — 클래스 밴드는 2–3 자리수 폭이라 "
                             "(§4의 k₂/Q 표) 값을 고르지 않는다", inputs, REFS)
    if radius_earth is None:
        return out_of_domain(RECIPE, VERSION, "cannot-say (no radius): Ė ∝ R⁵, F ∝ R³ (§1 · §6.5)", inputs, REFS)
    power, flux, n = tidal_power(k2_over_q, perturber_mass_earth * M_EARTH_KG, radius_earth * R_EARTH_M,
                                 semi_major_axis_m, eccentricity_forced)
    regime = outcome_regime(flux)
    notes = (
        f"fixed-Q law §1 with n = √(G M_p/a³) (m ≪ M_p): k₂/Q {k2_over_q} · e {eccentricity_forced} · "
        f"a {semi_major_axis_m / 1e3:,.0f} km · M_p {perturber_mass_earth:.4g} M⊕ · R {radius_earth:.4f} R⊕ → P_orb "
        f"{2 * math.pi / n / 3600:.3f} h. G CODATA 2018, M⊕ IAU 2015 nominal.",
        "e and k₂/Q are DECLARATIONS (grade declared): the board fits k₂/Q to its chosen flux (phase4/alpha_centauri.yaml@«The tidal term needs k₂/Q ≈ 0.0016 at the simulated e ≈ 0.005, which is fitted rather than predicted, but it» "
        "'fitted rather than predicted'); the class band for k₂/Q spans 2–3 decades (doc §5) and is not elected here.",
        f"io_power_ratio = Ė / {IO_POWER_W:.1e} W, the document's printed '~10¹⁴ W' (§2). The §6.5 Dante "
        "rows invert to 1.016e14 W (2.44 W/m² at R 1822 km), 1.6 % from this constant — a convention difference.",
        f"heat_transport_regime is the §6.1 outcome table read on the TIDAL flux alone; {GUIDES}.",
        "not emitted: radius_ceiling · plains_temperature (§6.3–6.5, the Dante lid axis — a separate item); "
        "tidal_transport.derive_potential_temperature is not consulted (validation failed by its own docstring; Pandora is not a "
        "§6 lid-bearing case, §6.3).",
    )
    return Result(recipe=RECIPE, version=VERSION, regime="fixed_q_synchronous",
                  reason=f"Ė {power:.3e} W · F {flux:.4g} W/m² ({power / IO_POWER_W:.3g}× Io's ~10¹⁴ W) → {regime}",
                  grade="analog",   # the law is the standard first-order form; e and k₂/Q are declarations
                  inputs=inputs,
                  values={"power": power, "surface_flux": flux, "io_power_ratio": power / IO_POWER_W,
                          "heat_transport_regime": regime, "orbital_period": 2 * math.pi / n / 3600},
                  units={"power": "W", "surface_flux": "W/m2", "io_power_ratio": "dimensionless",
                         "heat_transport_regime": "", "orbital_period": "h"},
                  refs=REFS, notes=notes)


def solve_mode(surface_flux: float | None, radiogenic_power: float | None, radius_earth: float | None) -> Result:
    inputs = {"surface_flux": surface_flux, "radiogenic_power": radiogenic_power, "radius_earth": radius_earth}
    refs = ("docs/reference/tidal-heating-methodology.md@«A body's surface has exactly three ways to pass internal heat, and they differ by **four orders of magnitude in capacity**.»",)
    if radius_earth is None:
        return out_of_domain(RECIPE, VERSION, "cannot-say (no radius): 총 표면 플럭스를 낼 반지름이 없다", inputs, refs)
    if surface_flux is None and radiogenic_power is None:
        return out_of_domain(RECIPE, VERSION, "cannot-say (no heat source): tidal_heating 도 internal_heat_nontidal 도 값을 내지 않았다",
                             inputs, refs)
    # ⚠ C34, 오너 결정 2026-09-07 — **먹이는 양은 조석 + 방사성 총 플럭스**다. 고른 것이 아니라
    # 문서 자신의 §6.2 앵커가 판별했다: 지구 기준 후보 넷(0.0418 엔진 · 0.0769 implied ·
    # 0.08 §6.1 · 0.0921 측정 표면열류)이 **2.203× 폭**으로 벌어져 있고, 저단은 앵커 라벨 4개 중
    # **3개**를 재현하고 고단은 **1개**(지구뿐)만 재현한다. 수성 0.01575 · 화성 0.01587 이 정체뚜껑
    # 경계 0.030 까지 **1.90× · 1.89× 여유**뿐이라, 먹이는 양을 1.9× 넘게 올리면 둘이 판구조로
    # 넘어간다 — 문서는 둘 다 정체뚜껑으로 적는다. 즉 **밴드는 판정 중립이 아니었다.**
    # ⚠ 이 줄의 값은 안 바뀌었다. 바뀐 것은 근거다 — 전에는 이 레시피 자기 계약 블록이 "총 플럭스"
    # 라 적은 것이 유일한 출처였고(b29b556e), 이제는 앵커 3/4 재현이다.
    # ⚠ 안 고쳐진 것 둘: 금성은 양쪽 끝에서 다 안 맞고(문서 정체뚜껑, 엔진 37.75 → 판구조),
    # 판구조 천장 0.135 는 여전히 authored 다. 이 결정은 **먹이는 양**에 대한 것이지 문턱이 아니다.
    area = 4.0 * math.pi * (radius_earth * R_EARTH_M) ** 2
    radiogenic_flux = (radiogenic_power or 0.0) / area
    total = (surface_flux or 0.0) + radiogenic_flux
    mode = transport_mode(total)
    # C46 (b): 우리 칸 이름은 **체제 이름이 아니다.** §6.2 사다리의 칸이고, 문헌 체제는 따로 낸다.
    cell, rung, rung_why = regime_ladder_cell(total)
    cand = regime_candidates(total, radius_earth)
    compatible = sorted(k for k, (v, _w) in cand.items() if v == "compatible")
    undecided = sorted(k for k, (v, _w) in cand.items() if v == "cannot decide")
    excluded = sorted(k for k, (v, _w) in cand.items() if v == "excluded")
    parts = []
    if surface_flux is not None:
        parts.append(f"tidal {surface_flux:.4g}")
    if radiogenic_power is not None:
        parts.append(f"radiogenic {radiogenic_flux:.4g}")
    else:
        parts.append("radiogenic absent")
    ladder_note = (
        f"⚠ `regime_ladder_cell` = {cell!r}, fixed by the highest rung the flux passed"
        + (f" ({rung:g} W/m²)" if rung is not None else "") + f". {rung_why} "
        f"⚠ **The ladder rule is OURS, origin `{ANALOGY_RUNG}`** — not the literature's verdict and not "
        f"a measured boundary. Its rungs are what bodies we know actually radiate, so the ladder says "
        f"*'Earth's worth of heat, Earth's worth of crust'* and nothing stronger. The literature cuts "
        f"these regimes on mobility and plateness (Lourenço+ 2020 §3.1, §3.3), which are outputs of a "
        f"4.5 Gyr simulation. ⚠ Earth coming out `plate tectonics` is therefore **not evidence** — that "
        f"rung IS Earth, and its margin is 0.2 %.")
    regime_note = (
        f"C46: flux is a sieve, not a classifier. Compatible with {len(compatible)} literature regime(s) "
        f"({', '.join(compatible) or 'none'}); excluded {', '.join(excluded) or 'none'}; "
        f"flux cannot decide for {', '.join(undecided) or 'none'}. ⚠ `mode` above is the §6.2 LADDER CELL, "
        f"not a tectonic regime — the literature cuts these on mobility and plateness (Lourenço+ 2020 §3.1, "
        f"§3.3), which are outputs of a 4.5 Gyr simulation and not observable here. No single regime is "
        f"emitted while more than one stands.")
    notes = (
        ladder_note,
        regime_note,
        f"§6.2 table read on the TOTAL surface flux {total:.4g} W/m² = {' + '.join(parts)} W/m²; "
        f"chain :631 supplies W/m² and :632 supplies W — the W is divided by 4πR² here. {GUIDES}.",
        "resurfacing_rate (chain.yaml outputs) is not emitted: the document prints no formula for it.",
        "selectors not wired in this version: global_fluid_layer (chain :633, no recipe) and t_eq_stellar (:634) — "
        "§6.3 names Pandora a global-fluid-layer case, so its selector is the next item.",
    )
    return Result(recipe=RECIPE, version=VERSION, regime=f"mode_{mode.split()[0]}",
                  reason=f"total surface flux {total:.4g} W/m² → {mode}",
                  grade="analog", inputs=inputs,
                  values={"mode": mode, "total_surface_flux": total,
                          "regime_ladder_cell": cell, "regime_ladder_rung": rung,
                          "regime_candidates": compatible,
                          "regime_flux_cannot_decide": undecided,
                          "regime_excluded": excluded},
                  units={"mode": "", "total_surface_flux": "W/m2", "regime_candidates": "",
                         "regime_ladder_cell": "", "regime_ladder_rung": "W/m2",
                         "regime_flux_cannot_decide": "", "regime_excluded": ""},
                  refs=refs, notes=notes)


from registry import recipe  # noqa: E402


@recipe("tidal_heating")
def _from_state(state):
    return solve(mass_earth=state["mass_earth"],
                 radius_earth=state.get("radius_earth", state.get("radius")),
                 semi_major_axis_km=state.get("semi_major_axis_km"),
                 perturber_mass_earth=state.get("perturber_mass_earth"),
                 eccentricity_forced=state.get("eccentricity_forced"),
                 k2_over_q=state.get("k2_over_q"))


@recipe("heat_transport_mode")
def _mode_from_state(state):
    return solve_mode(surface_flux=state.get("surface_flux"),
                      radiogenic_power=state.get("radiogenic_power"),
                      radius_earth=state.get("radius_earth", state.get("radius")))
