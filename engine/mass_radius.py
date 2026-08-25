# 질량에서 반지름과 밀도를 도출한다 — 레짐이 넷이고, 잘못 고르는 것이 지배적 오류다
"""Assign a radius and bulk density from a mass, per mass-radius-relation-methodology.

    from mass_radius import assign

    assign(mass_earth=1.22)      → 1.07 R⊕, 5.5 g/cm³   (Proxima b, 문서 §7)

이 레시피의 핵심은 계산이 아니라 **레짐 선택**이다. 문서가 그렇게 말한다 —
"choosing the wrong one is the dominant error". 암석 지수를 서브넵튠에 쓰면 질량이
자릿수로 틀리고, 거대행성에 거듭제곱 법칙을 쓰면 관계가 평평-감소라 그냥 틀렸다.

그래서 넷 중 셋은 값을 내지 않고 **거절한다**.

* 암석  — interior_layers 가 층을 적분해서 낸다. 여기만 확정값이다.
* 밸리  — 애매하다고 밝히고 양쪽을 함께 돌려준다. 하나로 고르지 않는다.
* 서브넵튠 — 반지름이 질량의 나쁜 대리라 확률 관계를 써야 한다. 여기서 안 낸다.
* 거대행성 — 전자축퇴라 R 이 질량에 거의 무관하다. 범위를 주되 거듭제곱은 금지.
"""
from __future__ import annotations

from interior import COMPOSITIONS, solve
from payload import Result, out_of_domain

RECIPE = "mass-radius-relation-methodology"
VERSION = "1"

REFS = (
    "2016ApJ...819..127Z",      # Zeng+ 2016 — PREM 보정 2층 격자, 이 레시피의 기준선
    "2007ApJ...669.1279S",      # Seager+ 2007 — 고체 행성 M-R 의 기초
    "2017AJ....154..109F",      # Fulton+ 2017 — 반지름 밸리 실측
    "2015ApJ...801...41R",      # Rogers 2015 — 1.6 R⊕ 위는 대개 암석이 아니다
    "2007ApJ...659.1661F",      # Fortney+ 2007 — 휘발성·거대행성 격자
)

# 조성 이름은 이제 **재료 배정** 이지 반지름 배율이 아니다. 어떤 질량분율이 어떤
# 재료로 가는지는 interior.COMPOSITIONS 한 곳에만 있고, 반지름은 그 층을 적분해서
# 나온다.
#
# 2026-08-25 까지 여기에는 조성별 반지름 배율표가 있었다. earth_like 만 정의상 1.0
# 이었고 나머지 셋은 방법론 문서 §2 의 *산문 순서* ("밀한 재료일수록 작다", "순철
# ≳ 1.5 ρ⊕") 를 숫자로 옮긴 것이었다 — 층을 풀어서 나온 값이 아니었다. 그래서
# density_gate 의 순철 문턱이 문서 §7 의 기각 사례를 재현하지 못했다. 표가 사라지고
# 순철 곡선이 실제 Fe(ε) 상태방정식의 적분이 되면서 그 문제도 같이 사라진다.
COMPOSITION_KO = {
    "iron":       "순철 (초수성급)",
    "earth_like": "지구식 암석 (철 약 1/3)",
    "silicate":   "순규산염 (철 결핍, 달·화성식)",
    "water":      "물·얼음 세계 (H₂O 50 %)",
}

# 반지름 밸리. 문서 §5 — Fulton 갭은 ~1.5-2.0 R⊕, 중심은 ~1.8 R⊕ 부근.
VALLEY_LO = 1.5
VALLEY_HI = 1.8

ROCKY_MASS_MAX = 8.0        # M⊕. 이 위에서는 Zeng 근사가 깨진다 (§3 regime 1)
GIANT_M_MIN_MJ = 0.1        # M_J. 전자축퇴 영역의 하단 (§3 regime 3)

M_EARTH_PER_MJ = 317.8
EARTH_DENSITY_GCC = 5.513


def _density(mass_earth: float, radius_earth: float) -> float:
    """ρ = M / (4/3 π R³) 를 지구 단위로. 지구 밀도를 곱해 g/cm³ 로 돌린다."""
    return EARTH_DENSITY_GCC * mass_earth / radius_earth ** 3


def assign(mass_earth: float, composition: str = "earth_like") -> Result:
    """Assign a radius from a mass. 레짐 밖은 거절한다."""
    inputs = {"mass_earth": mass_earth, "composition": composition}

    if composition not in COMPOSITIONS:
        return out_of_domain(
            RECIPE, VERSION,
            f"'{composition}' 는 이 문서가 다루는 조성이 아니다. "
            f"쓸 수 있는 것: {', '.join(COMPOSITIONS)}",
            inputs=inputs, refs=REFS)

    if mass_earth <= 0:
        return out_of_domain(RECIPE, VERSION, "질량이 양수가 아니다",
                             inputs=inputs, refs=REFS)

    # 거대행성. 축퇴압이 반지름을 질량에서 떼어놓으므로 거듭제곱을 쓰면 안 된다.
    if mass_earth >= GIANT_M_MIN_MJ * M_EARTH_PER_MJ:
        return out_of_domain(
            RECIPE, VERSION,
            f"{mass_earth / M_EARTH_PER_MJ:.2f} M_J 는 전자축퇴 영역이다. "
            "0.3-4 M_J 에 걸쳐 R ≈ 1.0-1.2 R_J 로 평평하고 그 위에서는 오히려 줄어든다 "
            "(Fortney+ 2007, Baraffe+ 2008). 거듭제곱 외삽이 아니라 그 범위를 배정할 것 — "
            "젊거나 강한 복사를 받으면 위로 올린다.",
            inputs=inputs, refs=REFS)

    # 암석 반지름을 먼저 읽어야 밸리 판정을 할 수 있다. 문서 §5 는 이 게이트가
    # §3 의 레짐 선택보다 *먼저* 돈다고 못박는다. 이제 그 반지름은 거듭제곱 근사가
    # 아니라 층 적분의 결과다.
    comp_ko = COMPOSITION_KO[composition]
    structure = solve(mass_earth, composition=composition)
    if not structure.applicable:
        return out_of_domain(
            RECIPE, VERSION,
            f"층 적분이 이 천체를 거절했다 — {structure.reason}",
            inputs=inputs, refs=REFS)
    rocky_radius = structure.values["radius"]

    if mass_earth > ROCKY_MASS_MAX:
        return out_of_domain(
            RECIPE, VERSION,
            f"{mass_earth:.1f} M⊕ 는 Zeng 근사의 상한(~8 M⊕) 위다. "
            "고체 격자를 그대로 밀면 안 된다 — 이 질량대는 휘발성 외피를 가정해야 하고 "
            "반지름은 확률 관계로 가야 한다.",
            inputs=inputs, refs=REFS)

    if rocky_radius >= VALLEY_HI:
        return out_of_domain(
            RECIPE, VERSION,
            f"암석 격자가 {rocky_radius:.2f} R⊕ 를 주는데 이는 밸리(~{VALLEY_LO}-{VALLEY_HI} R⊕) "
            "위다. Rogers 2015 이후로 이 위는 통계적으로 암석이 아니다 — 휘발성 외피가 "
            "강제되고, 그러면 반지름이 질량의 나쁜 대리가 되어 확률 관계(Chen & Kipping / "
            "Otegi)를 써야 한다. 2.5 R⊕ 짜리에 지구식 표면을 얹지 말 것.",
            inputs=inputs, refs=REFS)

    density = _density(mass_earth, rocky_radius)

    if rocky_radius >= VALLEY_LO:
        # 밸리 안. 문서는 하나로 고르지 말고 양쪽을 들고 가라고 한다.
        return Result(
            recipe=RECIPE, version=VERSION, regime="radius_valley",
            reason=(f"{mass_earth:.2f} M⊕ 의 암석 반지름 {rocky_radius:.2f} R⊕ 가 "
                    f"밸리({VALLEY_LO}-{VALLEY_HI} R⊕) 안이다. 이 구간은 진짜로 애매해서 "
                    "암석과 휘발성 외피 양쪽이 다 가능하다 — 하나로 고르지 않고 표시한다."),
            grade="judgment",
            inputs=inputs,
            values={"radius": rocky_radius, "density": density},
            units={"radius": "R_earth", "density": "g/cm3"},
            refs=REFS,
            notes=("밸리 거주자다. 대기·표면 가정을 확정하기 전에 오너 판단이 필요하다.",
                   "휘발성 외피를 택하면 이 반지름은 하한이 된다."),
        )

    return Result(
        recipe=RECIPE, version=VERSION, regime="rocky",
        reason=(f"{mass_earth:.2f} M⊕ 는 암석 영역(≲ {ROCKY_MASS_MAX} M⊕)이고 "
                f"반지름 {rocky_radius:.2f} R⊕ 가 밸리({VALLEY_LO} R⊕) 아래다. "
                f"{comp_ko} 의 층을 정수압 평형으로 적분해서 나온 반지름이다 — "
                "자기압축이 그 안에 들어 있다."),
        grade="calibrated",
        inputs=inputs,
        values={"radius": rocky_radius, "density": density},
        units={"radius": "R_earth", "density": "g/cm3"},
        refs=REFS,
        notes=(structure.notes[0],),
    )


def density_gate(mass_earth: float, radius_earth: float) -> Result:
    """과결정된 천체를 검사한다. 배정이 아니라 기각이 목적이다 (문서 §6).

    질량·반지름·중력이 다 지정되면 셋 중 둘만 자유롭다. 순철 곡선보다 밀하면
    수성보다 철이 많다는 뜻이고, 충돌로 벗겨진 파편이 아닌 한 물리적이지 않다.

    순철 곡선의 절대 위치는 이제 Fe(ε) 상태방정식을 적분해서 나온다 (Seager+ 2007
    Table 1 의 Vinet 적합). 문턱이 유도된 배율 위에 서 있던 동안에는 문서 §7 의
    기각 사례가 재현되지 않았는데, 곡선이 실물이 되면서 그 자리가 정리됐다.
    """
    inputs = {"mass_earth": mass_earth, "radius_earth": radius_earth}
    iron = solve(mass_earth, composition="iron")
    if not iron.applicable:
        return out_of_domain(RECIPE, VERSION,
                             f"순철 곡선을 못 그렸다 — {iron.reason}",
                             inputs=inputs, refs=REFS)
    iron_radius = iron.values["radius"]
    density = _density(mass_earth, radius_earth)
    rho_rel = density / EARTH_DENSITY_GCC

    if radius_earth < iron_radius:
        return out_of_domain(
            RECIPE, VERSION,
            f"({mass_earth:.3f} M⊕, {radius_earth:.3f} R⊕) 는 밀도 {rho_rel:.2f} ρ⊕ 로 "
            f"순철 곡선({iron_radius:.3f} R⊕)보다 밀하다. 수성보다 철이 많다는 뜻이라 "
            "충돌로 벗겨진 파편이 아니면 물리적이지 않다 — 기각. 가장 방어 가능한 둘"
            "(대개 반지름과 목표 표면중력)을 고정하고 나머지를 풀 것.",
            inputs=inputs, refs=REFS)

    return Result(
        recipe=RECIPE, version=VERSION, regime="density_gate",
        reason=(f"밀도 {rho_rel:.2f} ρ⊕ 는 조성 그물 안이다 "
                f"(순철 한계 {iron_radius:.3f} R⊕ 보다 크다)."),
        grade="calibrated",
        inputs=inputs,
        values={"density": density},
        units={"density": "g/cm3"},
        refs=REFS,
    )


# ── 그래프에 붙이기 ─────────────────────────────────────────────────────
from registry import recipe  # noqa: E402


@recipe("mass_radius_relation")
def _from_state(state):
    return assign(
        mass_earth=state["mass_earth"],
        composition=state.get("composition_intent", "earth_like"),
    )
