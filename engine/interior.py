# 2층 기하와 관성모멘트를 푼다 — 네 레시피가 각자 가정하던 내부 구조의 정적 부분
"""Solve two-layer geometry and the normalised moment of inertia.

    from interior import layers

    layers(mass_earth=1.0, radius_earth=1.0, core_mass_fraction=0.325)
        → C/MR² 0.347, f 0.549      (지구, 발표값 0.3307 / 0.546)

층이 균질하다고 두므로 자기압축을 무시한다. 실제 천체는 안쪽으로 질량을 몰기
때문에 도출값은 **항상 발표값보다 크다** — 오차가 한쪽으로만 난다. 지구가 최악
(4.8 %)이고 달이 최선(0.8 %)인 것이 그 증거다. 압축이 클수록 나빠진다.

세 층이 필요한 천체는 거절한다. 가니메데를 2층으로 풀면 핵 경계가 0.46 으로
나오는데 실측은 0.27 이다 — 값이 조금 틀리는 게 아니라 자리가 틀린다.
"""
from __future__ import annotations

from payload import Result, out_of_domain

RECIPE = "interior-structure-methodology"
VERSION = "1"

REFS = (
    "1981PEPI...25..297D",      # PREM — 지구 층 밀도의 출처
    "2016ApJ...819..127Z",      # Zeng+ 2016 — 핵질량분율 매개변수화
)

# 층 평균밀도 [kg/m³]. 표면값이 아니라 층 전체의 평균이다.
#
# ⚠ 이 표는 **지구 질량 근처에서만** 쓸 수 있다. 층 밀도는 그 층이 받는 압력의
# 함수이고, 압력은 구조 전체를 풀어야 나온다. 수성 핵은 ~7800 kg/m³ 인데 지구
# 핵은 ~10900 이다 — 같은 철인데 압축이 다르다. 질량의 거듭제곱으로 맞춰보면
# 지수가 천체마다 0.10~0.23 으로 흩어져 하나로 안 잡힌다.
#
# 그래서 밀도는 **입력으로 받을 수 있게** 두고, 표는 지구 근처의 기본값일 뿐이다.
# 밖에서는 거절한다. 이 표가 사라지는 것이 진짜 내부 솔버의 일이다.
LAYER_DENSITY = {
    "earth_like": (10900.0, 4500.0, "철핵 + 규산염 맨틀 (PREM 평균)"),
    "iron_rich":  (10500.0, 3300.0, "수성형 — 큰 철핵, 얇은 규산염"),
    "silicate":   (7000.0, 3300.0, "철 결핍 — 작은 핵, 달·화성형"),
}

# 기본 밀도표를 믿을 수 있는 질량 구간. 밖에서는 밀도를 직접 받아야 한다.
DEFAULT_TABLE_MASS_RANGE = (0.5, 2.0)      # M⊕

# 평균밀도 하한. 아래로는 얼음각이 두꺼워 3층이 되고, 2층으로 풀면
# 핵 경계가 틀린 자리에 놓인다. 가니메데(1936)·칼리스토(1834)가 여기 걸린다.
ROCKY_DENSITY_MIN = 3000.0

EARTH_MASS_KG = 5.972e24
EARTH_RADIUS_M = 6.371e6
UNIFORM_SPHERE_NMOI = 0.4


def mean_density(mass_earth: float, radius_earth: float) -> float:
    """평균밀도 [kg/m³]."""
    m = mass_earth * EARTH_MASS_KG
    r = radius_earth * EARTH_RADIUS_M
    return m / (4.0 / 3.0 * 3.141592653589793 * r ** 3)


def core_fraction(core_mass_fraction: float, rho_core: float, rho_mantle: float) -> float:
    """질량 적분을 반지름 비로 뒤집는다. f³ = x ρ_m / [ρ_c(1-x) + x ρ_m]."""
    x = core_mass_fraction
    f3 = x * rho_mantle / (rho_core * (1.0 - x) + x * rho_mantle)
    return f3 ** (1.0 / 3.0)


def nmoi_two_layer(core_mass_fraction: float, f: float) -> float:
    """C/MR² = (2/5)[x f² + (1-x)(1-f⁵)/(1-f³)]."""
    x = core_mass_fraction
    f3 = f ** 3
    return 0.4 * (x * f * f + (1.0 - x) * (1.0 - f ** 5) / (1.0 - f3))


def layers(mass_earth: float, radius_earth: float, core_mass_fraction: float,
           composition: str = "earth_like",
           core_density: float | None = None,
           mantle_density: float | None = None) -> Result:
    """Solve the two-layer interior.

    층 밀도를 직접 주면 그것을 쓴다. 안 주면 조성 표의 지구 근처 기본값을 쓰되,
    질량이 그 구간 밖이면 거절한다 — 압축이 달라 표가 맞지 않기 때문이다.
    """
    given = core_density is not None and mantle_density is not None
    inputs = {"mass_earth": mass_earth, "radius_earth": radius_earth,
              "core_mass_fraction": core_mass_fraction, "composition": composition,
              "core_density": core_density, "mantle_density": mantle_density}

    if not given and composition not in LAYER_DENSITY:
        return out_of_domain(
            RECIPE, VERSION,
            f"'{composition}' 는 층 밀도가 정의된 조성이 아니다. "
            f"쓸 수 있는 것: {', '.join(LAYER_DENSITY)}",
            inputs=inputs, refs=REFS)

    if mass_earth <= 0 or radius_earth <= 0:
        return out_of_domain(RECIPE, VERSION, "질량 또는 반지름이 양수가 아니다",
                             inputs=inputs, refs=REFS)

    if not 0.0 < core_mass_fraction < 1.0:
        return out_of_domain(
            RECIPE, VERSION,
            f"핵질량분율 {core_mass_fraction} 는 (0, 1) 밖이다. "
            "0 이면 미분화라 놓을 핵이 없고 (균질구의 0.4), 1 이면 맨틀이 없다.",
            inputs=inputs, refs=REFS)

    rho_bar = mean_density(mass_earth, radius_earth)
    if rho_bar < ROCKY_DENSITY_MIN:
        return out_of_domain(
            RECIPE, VERSION,
            f"평균밀도 {rho_bar:.0f} kg/m³ 는 얼음이 두껍다는 뜻이고, 그런 천체는 "
            "금속핵-암석맨틀-얼음각의 3층이다. 2층으로 풀면 값이 조금 틀리는 게 "
            "아니라 핵 경계가 틀린 자리에 놓인다 — 가니메데에서 0.46 이 나오는데 "
            "실측은 0.27 이다.",
            inputs=inputs, refs=REFS)

    lo, hi = DEFAULT_TABLE_MASS_RANGE
    if not given and not lo <= mass_earth <= hi:
        return out_of_domain(
            RECIPE, VERSION,
            f"{mass_earth:.3f} M⊕ 는 기본 밀도표를 믿을 수 있는 구간({lo}-{hi} M⊕) 밖이다. "
            "층 밀도는 그 층이 받는 압력의 함수라 질량에 따라 달라진다 — 수성 핵은 "
            "~7800 kg/m³ 이고 지구 핵은 ~10900 이다. 이 질량대에서는 층 밀도를 "
            "직접 넘길 것 (core_density, mantle_density).",
            inputs=inputs, refs=REFS)

    if given:
        rho_c, rho_m = core_density, mantle_density
        comp_ko = "직접 지정한 층 밀도"
    else:
        rho_c, rho_m, comp_ko = LAYER_DENSITY[composition]
    f = core_fraction(core_mass_fraction, rho_c, rho_m)
    nmoi = nmoi_two_layer(core_mass_fraction, f)

    return Result(
        recipe=RECIPE, version=VERSION, regime="two_layer",
        reason=(f"평균밀도 {rho_bar:.0f} kg/m³ 로 암석-금속 영역이고, 핵질량분율 "
                f"{core_mass_fraction:.3f} 에서 {comp_ko} 층 밀도를 쓰면 핵 경계가 "
                f"{f:.3f} R 에 놓인다. 균질층 적분이라 자기압축을 무시하므로 "
                f"C/MR² 는 실제보다 크게 나온다 — 이 값이거나 조금 아래로 읽을 것."),
        grade="analog",
        inputs=inputs,
        values={"nmoi": nmoi,
                "core_radius_fraction": f,
                "core_radius": f * radius_earth},
        units={"nmoi": "dimensionless",
               "core_radius_fraction": "dimensionless",
               "core_radius": "R_earth"},
        refs=REFS,
        notes=("균질층 가정이라 자기압축을 무시한다. 지구에서 +4.8 %, 달에서 +0.8 % —"
               " 압축이 클수록 크게 나온다.",
               "층 밀도를 직접 지정했다." if given else
               "층 밀도가 조성 표의 지구 근처 기본값이다. 층을 실제로 적분하면 이 표가 사라진다."),
    )


# ── 그래프에 붙이기 ─────────────────────────────────────────────────────
from registry import recipe  # noqa: E402


@recipe("interior_layers")
def _from_state(state):
    return layers(
        mass_earth=state["mass_earth"],
        radius_earth=state["radius_earth"],
        core_mass_fraction=state["core_mass_fraction"],
        composition=state.get("composition_intent", "earth_like"),
    )
