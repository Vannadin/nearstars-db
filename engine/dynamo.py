# 거대행성·갈색왜성 쌍극자 자기장 도출기 — planetary-dynamo-scaling 방법론의 실행 가능한 정본
"""Giant / substellar dipole field, as a callable recipe.

Grounding: `docs/reference/planetary-dynamo-scaling.md`. That document explains
*why* this relation; this module *is* the relation. Where the two disagree the
module wins and the document is wrong — that inversion is the point of the
pilot.

    B_pol = 9 G · (age / 4.5 Gyr)^-0.33 · (M / M_J)^0.93
    B_eq  = B_pol / 2
    moment / moment_Earth = (B_eq / 4.5 G) · (R / R_J)^3 · 20000

Four regimes, dispatched on mass. Three of them decline to answer, and each
says who does answer — misapplying a giant law to a rocky planet is a citation
error even when the paper is real, so the decline is the useful part.

    giant           0.3 - 13 M_J, age >= 0.2 Gyr   the interpolation above
    brown_dwarf     13 - 70 M_J                    B_dyn from a MEASURED luminosity (below)
    ice_giant       < 0.3 M_J                      out of domain, analog only
    rocky           (caller's class says so)       out of domain, other recipe

Brown dwarfs (C19, 2026-09-04). Until then this branch refused, because the
document sends it to `B_dyn = 4.8 (M L^2 / R^7)^(1/6)` [kG, solar units]
(Reiners & Christensen 2010 eq. 1) and refused to *derive* the internal cooling
luminosity from an unverified track. The refusal was about deriving L, not
about the scaling. For an ISOLATED brown dwarf there is nothing to derive: no
host irradiation, no fusion, so the observed bolometric luminosity IS the
internal cooling luminosity, and the DB holds it as a measurement. That
identification is the branch's precondition and is declared, not assumed
(`isolated`): it is true for a field brown dwarf and FALSE for an irradiated
planet - do not route a hot Jupiter through here.

    B_dyn      = 4.8 (M L^2 / R^7)^(1/6) kG        RC10 eq. 1, M L R in solar units
    B_dip^eq   = B_dyn / (2 sqrt 2)                  RC10 eq. 2 - and NO depth attenuation:
                                                     for a brown dwarf the dynamo top is at
                                                     or near the surface (RC10 sect. 2)
    B_dip^pol  = 2 B_dip^eq

Two more things the branch requires rather than assumes. (a) Saturation: the
scaling is rotation-independent only above a critical rotation rate whose value
RC10 calls "somewhat uncertain"; the evidence bound RC10 itself uses is that
M dwarfs with rotation periods up to at least 4 days are saturated (Reiners+
2009a), so a rotation period is required and must be <= 4 d. (b) The radius:
no field brown dwarf of the roster has a measured radius (the DB declares
0.09 +- 0.01 R_sun from the standard assumption), and R enters as R^(-7/6),
the steepest exponent in the formula on the only declared input. So a radius
band is required and the field is emitted as a band; a single value on this
branch is forbidden. Anchors: none traverse this branch.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from payload import Result, out_of_domain  # noqa: E402

RECIPE = "planetary-dynamo-scaling"
VERSION = "1"

REFS = (
    "2009Natur.457..167C",           # Christensen, Holzwarth & Reiners 2009
    "2010A&A...522A..13R",           # Reiners & Christensen 2010
    "arXiv:1007.1514",
    "docs/reference/planetary-dynamo-scaling.md",
)

# 보정 상수. 전부 문서 §"The practical interpolation formula" 에서 온다.
B_POL_AT_JUPITER_G = 9.0      # 1 M_J, 4.5 Gyr 에서의 극 쌍극자 [G]
AGE_EXPONENT = -0.33          # RC10 의 1 M_J 냉각 트랙 재현
MASS_EXPONENT = 0.93          # "5 M_J 는 1 M_J 보다 4-5배" 재현 (5^0.93 ~ 4.5)
B_EQ_AT_JUPITER_G = 4.5       # 목성 적도 표면장, 모멘트 정규화의 기준점
JUPITER_MOMENT_IN_EARTHS = 20000.0

# 검증된 적용 범위. 문서 §"Domain of validity: three regimes".
GIANT_M_MIN, GIANT_M_MAX = 0.3, 13.0      # M_J
GIANT_AGE_MIN = 0.2                        # Gyr
BD_M_MAX = 70.0                            # M_J

G_TO_UT = 100.0                            # 1 G = 100 µT
KG_TO_UT = 1.0e5                           # 1 kG = 0.1 T = 1e5 µT

# 갈색왜성 가지 (C19). RC10 식 1 의 상수와 단위, 포화 증거 한계.
B_DYN_PREFACTOR_KG = 4.8                   # RC10 eq. 1, [kG], M·L·R 태양단위
MJ_PER_MSUN = 1.0 / 9.5459e-4              # IAU 2015 nominal GM_J/GM_sun = 9.5459e-4 (교과서 상수)
RSUN_PER_RJ = 7.1492e7 / 6.957e8           # IAU 2015 nominal R_J(eq) / R_sun = 0.10276 (교과서 상수)
SATURATION_PERIOD_MAX_H = 4.0 * 24.0       # RC10 §2.1: "rotation periods up to at least 4 days" 는 포화 (Reiners+ 2009a) — 증거 한계이지 임계값이 아니다


def _bd_field(mass_mj, radius_rj, radius_rj_min, radius_rj_max, luminosity_lsun,
              rotation_period_h, isolated, inputs):
    """갈색왜성 가지. 측정 광도·선언 반지름 밴드·자전주기·고립 선언을 요구한다."""
    missing = [k for k, v in (("luminosity_lsun", luminosity_lsun),
                              ("rotation_period_h", rotation_period_h),
                              ("radius_rj_min", radius_rj_min),
                              ("radius_rj_max", radius_rj_max),
                              ("isolated", isolated)) if v is None]
    if missing:
        return out_of_domain(
            RECIPE, VERSION,
            f"{mass_mj:.3g} M_J 는 갈색왜성 영역(13-70 M_J)이다. 이 가지는 B_dyn = 4.8 (M L²/R⁷)^(1/6) 를 "
            "**측정된** 볼로메트릭 광도로 돌리는데, 그러려면 광도·자전주기·반지름 밴드·고립 선언이 "
            f"있어야 한다. 없는 입력: {', '.join(missing)}. (L(M, age) 트랙은 여전히 대지 않는다.)",
            inputs, REFS,
            tuple(f"missing input: {m}" for m in missing))
    if not isolated:
        return out_of_domain(
            RECIPE, VERSION,
            "isolated=False — 관측 볼로메트릭 광도를 내부 냉각광도와 동일시하는 것은 고립 갈색왜성에만 "
            "참이다. 조사받는 천체(뜨거운 목성 등)는 이 가지를 타지 않는다.",
            inputs, REFS, ("precondition: isolated body only",))
    if rotation_period_h > SATURATION_PERIOD_MAX_H:
        return out_of_domain(
            RECIPE, VERSION,
            f"자전주기 {rotation_period_h:.3g} h 는 RC10 이 포화 증거로 든 4 d 를 넘는다. 에너지플럭스 "
            "스케일링은 임계 자전율 위에서만 자전 무관이고, 그 임계값을 RC10 은 '다소 불확실' 하다고 "
            "적었다 — 증거 한계 밖은 답하지 않는다.",
            inputs, REFS, ("saturation not established",))
    if not (0 < radius_rj_min <= radius_rj <= radius_rj_max) or luminosity_lsun <= 0:
        return out_of_domain(
            RECIPE, VERSION,
            f"반지름 밴드가 물리적이지 않다 (min {radius_rj_min}, value {radius_rj}, max {radius_rj_max}) "
            f"또는 광도 {luminosity_lsun} 이 양수가 아니다.", inputs, REFS)

    m_sun = mass_mj / MJ_PER_MSUN
    def b_dyn_kg(r_rj):
        r_sun = r_rj * RSUN_PER_RJ
        return B_DYN_PREFACTOR_KG * (m_sun * luminosity_lsun ** 2 / r_sun ** 7) ** (1.0 / 6.0)
    b = b_dyn_kg(radius_rj)
    b_hi = b_dyn_kg(radius_rj_min)      # R^(-7/6): 작은 반지름이 큰 장
    b_lo = b_dyn_kg(radius_rj_max)
    two_root_two = 2.0 * 2.0 ** 0.5
    b_eq = b / two_root_two
    moment = (b_eq * 1000.0 / B_EQ_AT_JUPITER_G) * radius_rj ** 3 * JUPITER_MOMENT_IN_EARTHS
    width = (b_hi - b_lo) / b
    return Result(
        recipe=RECIPE, version=VERSION, regime="brown_dwarf",
        reason=(f"{mass_mj:.3g} M_J · L {luminosity_lsun:.3g} L☉ (측정) · R {radius_rj:.3g} R_J "
                f"(선언, 밴드 {radius_rj_min:.3g}–{radius_rj_max:.3g}) · P_rot {rotation_period_h:.3g} h "
                f"(≤ 4 d, 포화) · 고립. B_dyn 은 RC10 식 1, 표면 쌍극자는 식 2 (깊이 감쇠 없음 — "
                f"다이나모 꼭대기가 표면). 밴드 폭 {width*100:.0f} % 는 전부 선언된 반지름에서 온다"),
        grade="calibrated",
        inputs=inputs,
        values={"b_pol": 2.0 * b_eq * KG_TO_UT,
                "b_eq": b_eq * KG_TO_UT,
                "dipole_moment": moment,
                "b_dyn": b * KG_TO_UT,
                "b_dyn_min": b_lo * KG_TO_UT,
                "b_dyn_max": b_hi * KG_TO_UT,
                "b_eq_min": b_lo / two_root_two * KG_TO_UT,
                "b_eq_max": b_hi / two_root_two * KG_TO_UT},
        units={"b_pol": "µT", "b_eq": "µT", "dipole_moment": "×Earth", "b_dyn": "µT",
               "b_dyn_min": "µT", "b_dyn_max": "µT", "b_eq_min": "µT", "b_eq_max": "µT"},
        refs=REFS,
        notes=("band is radius-driven: R enters as R^(-7/6) and R is declared, not measured",
               "this is the field an energy-flux scaling predicts on a declared radius, not a measurement — "
               "no brown-dwarf field has been detected (Christensen+ 2009)",
               "moment normalisation reuses Jupiter's B_eq·R³ scale — a dipole moment is B_eq·R³ by definition, "
               "so the constant is not giant-specific"),
    )


def dipole_field(mass_mj: float, radius_rj: float, age_gyr: float,
                 body_class: str = "giant", luminosity_lsun: float | None = None,
                 rotation_period_h: float | None = None, radius_rj_min: float | None = None,
                 radius_rj_max: float | None = None, isolated: bool | None = None) -> Result:
    """Return the dipole field of a giant / substellar body.

    `body_class` is the caller's dispatch key. It is taken at face value for
    the rocky case only — mass decides the rest, because mass is what the
    paper's validated range is expressed in.
    """
    inputs = {"mass_mj": mass_mj, "radius_rj": radius_rj,
              "age_gyr": age_gyr, "body_class": body_class,
              # 갈색왜성 가지의 입력. 거대행성 가지는 읽지 않고 None 으로 기록만 한다.
              "luminosity_lsun": luminosity_lsun, "rotation_period_h": rotation_period_h,
              "radius_rj_min": radius_rj_min, "radius_rj_max": radius_rj_max, "isolated": isolated}

    if body_class == "rocky":
        return out_of_domain(
            RECIPE, VERSION,
            "암석 행성이다. 거대행성 다이나모 법칙은 적용되지 않는다 — "
            "rocky-planet-dynamo-methodology (RM22) 로 가라. "
            "실재하는 논문이어도 지구질량 천체에 이 스케일링을 인용하면 인용 오류다.",
            inputs, REFS,
            ("see docs/reference/rocky-planet-dynamo-methodology.md",))

    if mass_mj <= 0 or radius_rj <= 0 or age_gyr <= 0:
        return out_of_domain(
            RECIPE, VERSION,
            f"입력이 물리적이지 않다 (M={mass_mj}, R={radius_rj}, age={age_gyr}).",
            inputs, REFS)

    if mass_mj > BD_M_MAX:
        return out_of_domain(
            RECIPE, VERSION,
            f"{mass_mj:.3g} M_J 는 항성 영역이다 (> {BD_M_MAX:.0f} M_J).",
            inputs, REFS)

    if mass_mj > GIANT_M_MAX:
        return _bd_field(mass_mj, radius_rj, radius_rj_min, radius_rj_max, luminosity_lsun,
                         rotation_period_h, isolated, inputs)

    if mass_mj < GIANT_M_MIN:
        return out_of_domain(
            RECIPE, VERSION,
            f"{mass_mj:.3g} M_J 는 서브새턴 이하다. Reiners & Christensen 이 "
            "헬륨 분리에 의한 전도영역 성층화(Stevenson 1980)를 이유로 토성급 "
            "이하를 명시적으로 제외했고, 표면장 감쇠는 '정량화하기 어렵다'고 했다. "
            "태양계 얼음거인 아날로그(해왕성·천왕성 0.1-0.5 G, 강한 비쌍극자)를 "
            "쓰되 도출값이 아니라 자릿수 아날로그로 표시하라.",
            inputs, REFS,
            ("analog only: Connerney 1991 / Ness 1986",))

    if age_gyr < GIANT_AGE_MIN:
        return out_of_domain(
            RECIPE, VERSION,
            f"나이 {age_gyr:.3g} Gyr 는 보정 하한 {GIANT_AGE_MIN} Gyr 아래다. "
            "이 아래에서는 냉각 광도가 급변해 보간이 성립하지 않는다.",
            inputs, REFS)

    b_pol_g = (B_POL_AT_JUPITER_G
               * (age_gyr / 4.5) ** AGE_EXPONENT
               * mass_mj ** MASS_EXPONENT)
    b_eq_g = b_pol_g / 2.0
    moment = (b_eq_g / B_EQ_AT_JUPITER_G) * radius_rj ** 3 * JUPITER_MOMENT_IN_EARTHS

    return Result(
        recipe=RECIPE, version=VERSION, regime="giant",
        reason=(f"{mass_mj:.3g} M_J · {age_gyr:.3g} Gyr — 검증된 거대행성 영역 "
                f"({GIANT_M_MIN}-{GIANT_M_MAX} M_J, 나이 ≥ {GIANT_AGE_MIN} Gyr) 안. "
                "쌍극자는 자전율과 무관하고 내부 냉각 광도가 정한다"),
        grade="calibrated",
        inputs=inputs,
        values={"b_pol": b_pol_g * G_TO_UT,
                "b_eq": b_eq_g * G_TO_UT,
                "dipole_moment": moment},
        units={"b_pol": "µT", "b_eq": "µT", "dipole_moment": "×Earth"},
        refs=REFS,
    )


# ── 그래프에 붙이기 ─────────────────────────────────────────────────────
# dipole_field 는 순수 함수로 남긴다 — 테스트와 표 생성기가 그 형태로 부른다.
# 러너가 부르는 얇은 껍질만 여기서 등록한다. 상태에서 무엇을 꺼내는지가
# 이 한 곳에만 적히므로, 입력 이름이 바뀌어도 고칠 자리가 하나다.
from registry import recipe  # noqa: E402


M_EARTH_PER_MJ = 317.8      # 엔진은 질량을 M⊕ 로만 들고 있다. 별칭을 만들지 않는다.


@recipe("dynamo_giant")
def _from_state(state):
    return dipole_field(
        mass_mj=state["mass_earth"] / M_EARTH_PER_MJ,
        radius_rj=state["radius_rj"],
        age_gyr=state["age_gyr"],
        body_class=state.get("body_class", "giant"),
        luminosity_lsun=state.get("luminosity_lsun"),
        rotation_period_h=state.get("rotation_period_h"),
        radius_rj_min=state.get("radius_rj_min"),
        radius_rj_max=state.get("radius_rj_max"),
        isolated=state.get("isolated"),
    )
