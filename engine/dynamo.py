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
    brown_dwarf     13 - 70 M_J                    out of domain, see below
    ice_giant       < 0.3 M_J                      out of domain, analog only
    rocky           (caller's class says so)       out of domain, other recipe

The brown-dwarf branch is deliberately *not* implemented. The document sends it
to `B_dyn = 4.8 (M L^2 / R^7)^(1/6)`, which needs the body's internal cooling
luminosity, and the same document explicitly refuses to supply `L(M, age)`
rather than ground a cooling track it has not verified. A branch that cannot
run is worse as silent code than as an honest refusal, so it returns
out-of-domain naming the missing input.
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


def dipole_field(mass_mj: float, radius_rj: float, age_gyr: float,
                 body_class: str = "giant") -> Result:
    """Return the dipole field of a giant / substellar body.

    `body_class` is the caller's dispatch key. It is taken at face value for
    the rocky case only — mass decides the rest, because mass is what the
    paper's validated range is expressed in.
    """
    inputs = {"mass_mj": mass_mj, "radius_rj": radius_rj,
              "age_gyr": age_gyr, "body_class": body_class}

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
        return out_of_domain(
            RECIPE, VERSION,
            f"{mass_mj:.3g} M_J 는 갈색왜성 영역(13-70 M_J)이다. 이 영역은 "
            "B_dyn 을 직접 써야 하는데 그러려면 내부 냉각 광도 L(M, age) 가 "
            "필요하고, 방법론 문서가 검증되지 않은 냉각 트랙을 쓰느니 L 을 "
            "공급하지 않기로 했다. 값을 내려면 Burrows/Baraffe 트랙을 먼저 근거화하라.",
            inputs, REFS,
            ("missing input: internal cooling luminosity L(M, age)",))

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
    )
