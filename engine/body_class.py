# 천체가 무엇인가 — 여덟 갈래가 여기서 갈린다. 고르지 않고 좁히고, 선언과 대조한다
"""Narrow a body to the class (or classes) its mass and radius allow.

    from body_class import solve

    solve(mass_earth=14.54, radius_earth=3.981)   → 'ice_giant'   (Uranus)
    solve(mass_earth=95.16, radius_earth=9.140)   → 'gas_giant'   (Saturn)

Eight `selects` edges leave this node and every one of them picks which physics applies —
`interior_layers`, the three class tables, `body_figure`, `spin_axis_inclination`, the two
dynamos and `core_state`. Until now the value they read was a string typed into
`bodies/*.yaml` that nothing checked, so declaring Neptune a `giant` would have run an H/He
polytrope on it and returned a **confidently wrong** number.

Three things shape this recipe.

**It narrows; it does not choose.** Every boundary is a band, and a body inside one comes
back with both neighbours alive. Forcing a boundary-dweller into a box is the error mode
here, not indecision.

**It does not replace the declaration.** `bodies/*.yaml` keeps its `body_class`, because for
an invented body there is nothing to derive it from. This node **contrasts** the two and
says when they disagree; which one is wrong is the owner's call.

**The ladder reads two different quantities.** Below the giants the discriminant is radius:
the valley is a radius feature and Rogers 2015's argument is that at a given radius you can
tell whether there is an envelope. Above the giants it is mass: fusion thresholds are mass
thresholds, and radius is nearly degenerate there. The one place composition is
load-bearing — gas giant against ice giant — is the one boundary neither quantity draws.

Grounding: `docs/reference/body-class-methodology.md`.
"""
from __future__ import annotations

from interior import COMPOSITIONS
from mass_radius import VALLEY_HI, VALLEY_LO
from payload import Result, out_of_domain
from registry import recipe

RECIPE = "body-class-methodology"
VERSION = "1"

REFS = (
    "2017ApJ...834...17C",      # Chen & Kipping 2017 — 자료가 정한 전이질량 셋
    "2015ApJ...801...41R",      # Rogers 2015 — 1.6 R⊕ 위는 대개 암석이 아니다
    "2017AJ....154..109F",      # Fulton+ 2017 — 반지름 밸리 실측
    "2018MNRAS.479.4786V",      # Van Eylen+ 2018 — 밸리의 기울기, 벗겨진 핵
    "2023MNRAS.519.4056H",      # Ho & Van Eylen 2023 — 밸리가 주기·항성질량에 따라 움직인다
    "2020A&A...634A..43O",      # Otegi+ 2020 — 암석 개체군이 ~25 M⊕ 에서 끝난다
    "2014A&A...572A..35L",      # Lambrechts & Johansen 2014 — 페블 고립질량이 둘을 가른다
    "2011ApJ...727...57S",      # Spiegel+ 2011 — 중수소 연소 한계와 그 폭
    "2000ARA&A..38..337C",      # Chabrier & Baraffe 2000 — 수소연소 최소질량
    "2010arXiv1004.1091L",      # Lineweaver & Norman 2010 — 감자 반지름
)

# ── 어휘 ────────────────────────────────────────────────────────────────
#
# 여섯이다. 여기 들어오려면 **소비처를 이름 댈 수 있어야** 한다 — 새 이름을 만들면 그
# 여덟 selects 엣지가 전부 그것을 어떻게 다룰지 답해야 하기 때문이다. 여섯 전부
# 이름이 있다: interior.py 의 FLUID_CLASSES 가 갈색왜성과 별을 각각 다른 이유로 거절하고,
# GAS_GIANT_CLASSES · ICE_GIANT_CLASSES · SUB_NEPTUNE_CLASSES 가 외피 있는 셋을 받고
# (셋 다 가스질량분율과 포텐셜 온도를 선언으로 받는다), 나머지 하나가 암석 경로다.
#
# 질량 오름차순이다. 사다리의 순서가 곧 경계의 순서다.
LADDER = ("rocky", "sub_neptune", "ice_giant", "gas_giant", "brown_dwarf", "star")

# **철자가 둘인 클래스 하나.** `giant` 와 `gas_giant` 를 가르는 것이 이 저장소 어디에도
# 없다 — interior.py 는 GAS_GIANT_CLASSES 에 둘 다 넣고, core_state.py 도 그렇고,
# dynamo.py 는 `giant` 를 기본값으로 쓰고, bodies/alpha_centauri_a_b.yaml 은 `giant` 로
# 선언한다. derivation-discipline §7 이 적은 base_color/base_colour 와 같은 병이고, 거기
# 교훈이 "철자 변종을 메뉴에 들이는 것이 표류를 합법으로 만든다" 였다.
#
# 그래서 정본은 `gas_giant` 하나다 — `ice_giant` 옆에 섰을 때 모호하지 않은 쪽이다.
# `giant` 는 읽을 때만 받아 정규화하고 **내보내지 않는다**. 선언 자체는 오너 결정이라
# 건드리지 않는다.
ALIASES = {"giant": "gas_giant"}

# ── 경계 ────────────────────────────────────────────────────────────────
#
# 경계마다 **양이 하나, 띠가 하나**다. 띠 안이면 양쪽이 다 살아 있다. 띠의 양 끝은
# 전부 발표된 수이고, 지어낸 문턱은 없다.

# 1. 암석 ↔ 서브넵튠 — 반지름. 밸리는 mass_radius.py 의 상수를 **가져다 쓴다**.
#    사본을 두 벌 만들면 그중 하나가 표류한다. 저쪽 문서 §5 가 Fulton+ 2017 의 실측
#    결핍(1.5–2.0 R⊕)과 Van Eylen+ 2018 의 중심을 근거로 잡은 값이다.
#    (VALLEY_LO, VALLEY_HI = 1.5, 1.8 R⊕)

# 1b. 반지름이 없을 때의 대체 — 질량. Chen & Kipping 2017 이 316개에 꺾은
#     거듭제곱을 맞춰 **가정 없이** 뽑은 첫 전이점이다. 반지름 판정보다 약하다:
#     질량만으로는 외피가 있는지 말할 수 없기 때문이고, 그래서 등급이 내려간다.
TERRAN_BREAK_ME = 2.04              # Chen & Kipping 2017 Table 2, T(1)
TERRAN_BAND_ME = (1.45, 2.70)       # 같은 행의 −0.59 / +0.66

# 2. 서브넵튠 ↔ 얼음거대행성 — 반지름. Kopparapu+ 2018 이 Fulton+ 2017 의 반지름
#    분포에서 읽어 자기 구간표에 쓴 선이다. 이 자리에는 측정된 특징이 없다 — 두
#    클래스를 실제로 가르는 것은 조성(암석핵 + 얇은 H/He 대 얼음이 지배하는 내부)이고,
#    이건 그 대리다. **관례이므로 이 경계로 갈린 판정은 등급이 judgment 다.**
SUB_NEPTUNE_R_MAX = 3.5             # R⊕. Kopparapu+ 2018 §2.1

# 3. 얼음거대행성 ↔ 가스거대행성 — 질량, 두 발표값이 만드는 띠.
#
#    Kopparapu+ 2018 의 6.0 R⊕ 선은 **쓰지 않는다.** 그 논문이 자기 입으로 "the
#    *assumed* upper limit on Neptune-size planets" 라고 적는다. 지어낸 수를 그대로
#    옮기면 근거가 아니라 장식이 된다.
#
#    아래쪽 (근거 있음) — Lambrechts & Johansen 2014. 핵이 페블 고립질량에 닿으면
#    고체 강착이 끊기고 봉투가 폭주 수축해 가스거대행성이 되고, 못 닿으면 핵이 지배하는
#    채로 남아 얼음거대행성이 된다. 총질량이 고립질량보다 작으면 핵이 거기 닿은 적이
#    없으므로, 이 판정은 **한쪽만** 묶는다.
#    M_iso = 20 M⊕ (a / 5 AU)^(8/7) — 조사받는 원반, 논문 §4.1.
PEBBLE_ISO_ME_AT_5AU = 20.0
PEBBLE_ISO_REF_AU = 5.0
PEBBLE_ISO_EXPONENT = 8.0 / 7.0
#    장반경을 모르면 5 AU 값을 쓴다. M_iso 는 a 와 함께 커지므로 이것이 **가장 작은**
#    값이고, 얼음거대행성 판정을 가장 적게 내리는 쪽이다 — 안전한 방향의 기본값이다.

#    위쪽 (근거 있음) — Otegi+ 2020 이 암석 개체군이 ~25 M⊕ 에서 끝나는 것을 두고
#    "possibly indicating the maximum core mass that can be formed" 이라고 적는다.
#    질량이 그 두 배를 넘으면 절반 이상이 핵일 수 없다. 곱하기 2 는 지어낸 계수가
#    아니라 '가스가 지배한다'는 말의 정의다.
MAX_CORE_ME = 25.0                  # Otegi+ 2020 초록
GAS_DOMINATED_ME = 2.0 * MAX_CORE_ME

#    조성이 선언되면 그것이 먼저다 — 이 경계가 원래 묻는 것이 조성이기 때문이다.
GAS_DOMINATED_FRACTION = 0.5

# 4. 가스거대행성 ↔ 갈색왜성 — 질량. 중수소 연소.
#    Spiegel+ 2011: 흔한 조건에서 13.0 ± 0.8 M_J 이고, 금속도·헬륨·연소분율 정의를
#    전부 흔들면 11.0 (3배 태양금속도, 10 % 연소) ~ 16.3 (금속도 0, 90 % 연소) 이다.
#    띠는 그 전체 폭이다.
#    이 경계는 **질량-반지름에 흔적이 없다** (Chen & Kipping 2017: "brown dwarfs are
#    merely high-mass members of a continuum of Jovians"). 그래도 경계인 이유는
#    소비처가 구조가 아니라 **열이력** 에서 갈리기 때문이다 — interior.py 도 dynamo.py 도
#    "중수소가 탄다, 이 레시피에 그 열이력이 없다" 로 거절한다.
DEUTERIUM_MJ = 13.0
DEUTERIUM_BAND_MJ = (11.0, 16.3)

# 5. 갈색왜성 ↔ 항성 — 질량. 수소 연소 최소질량.
#    Chabrier & Baraffe 2000: 태양조성에서 0.075 M_sun, [M/H] = −2 에서 0.083 M_sun
#    (Fig. 3 캡션). 대기의 먼지 처리에 따라 태양조성 값이 0.070~0.072 로도 내려간다
#    (본문 §4.5.2). 띠는 그 폭이고, Chen & Kipping 의 자료가 정한 T(3) = 0.0800 ±
#    0.0081 M_sun 이 그 안에 떨어진다 — 서로 다른 방법 둘이 같은 자리를 가리킨다.
HBMM_MSUN = 0.075
HBMM_BAND_MSUN = (0.070, 0.083)

# 0. 아래 끝 — 정수압 평형. 이 어휘의 여섯은 전부 자기중력이 모양을 정하는 천체를
#    전제하고, 소비처도 그렇다: body_figure 의 J2 는 Radau–Darwin 에서 오고 그 식이
#    유체 평형 도형을 가정한다. Lineweaver & Norman 2010 이 태양계의 얼음 위성과
#    암석 소행성이 "at an average radius of ~200 km - 300 km" 에서 감자에서 구로
#    넘어간다고 적는다. 아래면 거절하고, 그 안이면 통과시키되 등급을 내린다.
POTATO_R_KM = (200.0, 300.0)
EARTH_R_KM = 6371.0

# 단위. dynamo.py 와 같은 값을 쓴다 — 한 양에 두 개의 상수를 만들지 않는다.
M_EARTH_PER_MJ = 317.8
M_EARTH_PER_MSUN = 332946.0         # IAU 2015 명목 GM 비
R_EARTH_PER_RJ = 11.209             # IAU 2015 명목 적도반지름 비

_GRADE_ORDER = ("measured", "calibrated", "analog", "judgment")

BELOW, INSIDE, ABOVE = -1, 0, 1

# 경계의 영어 이름. 문서의 앵커 표가 어느 경계가 그 천체를 갈랐는지 적는 데 쓴다 —
# 등급이 왜 갈리는지가 그 칸에 보인다.
BOUNDARY_NAMES = ("radius valley", "sub-Neptune ceiling", "envelope dominance",
                  "deuterium burning", "hydrogen burning")


def _band(value: float, lo: float, hi: float) -> int:
    """값이 띠의 아래인가 안인가 위인가. 띠 안은 판정하지 않는다는 뜻이다."""
    if value < lo:
        return BELOW
    if value > hi:
        return ABOVE
    return INSIDE


def _weakest(*grades: str) -> str:
    return max(grades, key=_GRADE_ORDER.index)


def pebble_isolation_mass(semi_major_axis_au: float | None) -> float:
    """Lambrechts & Johansen 2014 의 페블 고립질량 [M⊕]. 장반경을 모르면 5 AU 값."""
    a = semi_major_axis_au or PEBBLE_ISO_REF_AU
    return PEBBLE_ISO_ME_AT_5AU * (a / PEBBLE_ISO_REF_AU) ** PEBBLE_ISO_EXPONENT


# ── 경계 다섯 ───────────────────────────────────────────────────────────
# 각각 (판정, 등급, 한 줄 근거) 를 돌려준다. 판정이 INSIDE 면 양쪽이 살아남는다.

def _rocky_vs_sub_neptune(mass_earth, radius_earth):
    if radius_earth is not None:
        v = _band(radius_earth, VALLEY_LO, VALLEY_HI)
        return v, "calibrated", (
            f"반지름 {radius_earth:.2f} R⊕ 가 밸리({VALLEY_LO}–{VALLEY_HI} R⊕)의 "
            f"{'아래' if v < 0 else '위' if v > 0 else '안'}다")
    v = _band(mass_earth, *TERRAN_BAND_ME)
    return v, "judgment", (
        f"반지름이 없어 질량으로 읽는다 — {mass_earth:.2f} M⊕ 가 Chen & Kipping 의 "
        f"고체/휘발성 전이({TERRAN_BREAK_ME} M⊕, {TERRAN_BAND_ME[0]}–"
        f"{TERRAN_BAND_ME[1]})의 {'아래' if v < 0 else '위' if v > 0 else '안'}다. "
        "질량만으로는 외피의 유무를 말할 수 없어 반지름 판정보다 약하다")


def _sub_neptune_vs_ice_giant(radius_earth):
    if radius_earth is None:
        return INSIDE, "judgment", "반지름이 없다 — 이 경계는 반지름으로만 그어진다"
    v = BELOW if radius_earth < SUB_NEPTUNE_R_MAX else ABOVE
    return v, "judgment", (
        f"반지름 {radius_earth:.2f} R⊕ 가 {SUB_NEPTUNE_R_MAX} R⊕ 의 "
        f"{'아래' if v < 0 else '위'}다. 이 선은 관례다 — Kopparapu+ 2018 이 "
        "Fulton+ 2017 의 반지름 분포에서 읽어 구간표에 쓴 값이고, 이 자리를 실제로 "
        "가르는 것은 조성이다")


def _ice_giant_vs_gas_giant(mass_earth, gas_mass_fraction, semi_major_axis_au):
    if gas_mass_fraction is not None:
        v = ABOVE if gas_mass_fraction >= GAS_DOMINATED_FRACTION else BELOW
        return v, "analog", (
            f"가스질량분율 {gas_mass_fraction:.2f} 이 선언돼 있다 — 질량의 절반 "
            f"{'이상' if v > 0 else '미만'}이 수소-헬륨이다. 이 경계가 원래 묻는 것이 "
            "그것이라(Lambrechts & Johansen 2014) 선언이 먼저다")
    m_iso = pebble_isolation_mass(semi_major_axis_au)
    if mass_earth < m_iso:
        where = (f"{semi_major_axis_au:.2f} AU" if semi_major_axis_au
                 else f"{PEBBLE_ISO_REF_AU:.0f} AU 기본값")
        return BELOW, "analog", (
            f"총질량 {mass_earth:.1f} M⊕ 가 페블 고립질량 {m_iso:.0f} M⊕ ({where}) "
            "보다 작다 — 핵이 거기 닿은 적이 없으므로 봉투가 폭주할 수 없었다 "
            "(Lambrechts & Johansen 2014)")
    if mass_earth > GAS_DOMINATED_ME:
        return ABOVE, "analog", (
            f"총질량 {mass_earth:.1f} M⊕ 가 발표된 최대 핵질량 {MAX_CORE_ME:.0f} M⊕ "
            "(Otegi+ 2020) 의 두 배를 넘는다 — 절반 이상이 핵일 수 없으므로 가스가 "
            "지배한다")
    return INSIDE, "judgment", (
        f"총질량 {mass_earth:.1f} M⊕ 가 고립질량 {m_iso:.0f} M⊕ 와 최대 핵질량의 "
        f"두 배 {GAS_DOMINATED_ME:.0f} M⊕ 사이다. 이 구간을 가르는 발표된 기준이 "
        "없다 — `composition_intent` 의 가스질량분율을 선언하면 이 노드가 답한다")


def _gas_giant_vs_brown_dwarf(mass_earth):
    m_j = mass_earth / M_EARTH_PER_MJ
    v = _band(m_j, *DEUTERIUM_BAND_MJ)
    return v, "calibrated", (
        f"{m_j:.2f} M_J 가 중수소 연소 한계({DEUTERIUM_MJ} M_J, 모형 전체로는 "
        f"{DEUTERIUM_BAND_MJ[0]}–{DEUTERIUM_BAND_MJ[1]})의 "
        f"{'아래' if v < 0 else '위' if v > 0 else '안'}다 (Spiegel+ 2011)")


def _brown_dwarf_vs_star(mass_earth):
    m_sun = mass_earth / M_EARTH_PER_MSUN
    v = _band(m_sun, *HBMM_BAND_MSUN)
    return v, "calibrated", (
        f"{m_sun:.4f} M_sun 이 수소연소 최소질량({HBMM_MSUN} M_sun, 금속도와 대기 "
        f"처리로 {HBMM_BAND_MSUN[0]}–{HBMM_BAND_MSUN[1]})의 "
        f"{'아래' if v < 0 else '위' if v > 0 else '안'}다 (Chabrier & Baraffe 2000)")


def solve(mass_earth: float,
          radius_earth: float | None = None,
          declared_class: str | None = None,
          composition_intent: str | None = None,
          gas_mass_fraction: float | None = None,
          semi_major_axis_au: float | None = None) -> Result:
    """질량과 반지름에서 클래스를 좁힌다. 하나로 못 좁히면 좁히지 않는다.

    `declared_class` 는 계산에 **쓰이지 않는다** — 대조 상대다. 어긋나면 그 사실을
    출력에 싣고, 어느 쪽이 맞는지는 오너가 정한다."""
    inputs = {"mass_earth": mass_earth, "radius_earth": radius_earth,
              "declared_class": declared_class,
              "composition_intent": composition_intent,
              "gas_mass_fraction": gas_mass_fraction,
              "semi_major_axis_au": semi_major_axis_au}

    if mass_earth is None or mass_earth <= 0:
        return out_of_domain(RECIPE, VERSION, "질량이 양수가 아니다",
                             inputs=inputs, refs=REFS)

    notes: list[str] = []
    grade = "calibrated"

    # 조성 선언이 가스질량분율을 품고 있으면 꺼낸다. 재료 배정은 interior.COMPOSITIONS
    # 한 곳에만 있으므로 여기서 다시 적지 않는다.
    gmf = gas_mass_fraction
    if gmf is None and composition_intent in COMPOSITIONS:
        gmf = COMPOSITIONS[composition_intent][2]

    # ── 아래 끝. 자기중력이 모양을 정하는가 ──────────────────────────────
    if radius_earth is not None:
        r_km = radius_earth * EARTH_R_KM
        if r_km < POTATO_R_KM[0]:
            return out_of_domain(
                RECIPE, VERSION,
                f"반지름 {r_km:.0f} km 는 감자-구 전이({POTATO_R_KM[0]:.0f}–"
                f"{POTATO_R_KM[1]:.0f} km, Lineweaver & Norman 2010) 아래다. 이 어휘의 "
                "여섯은 전부 자기중력이 모양을 정하는 천체를 전제하고, 소비처도 "
                "그렇다 — body_figure 의 J2 는 Radau–Darwin 에서 오고 그 식은 유체 "
                "평형 도형을 가정한다. 이 크기에서는 조성이 아니라 강도가 모양을 정하고, "
                "그 이야기는 이 레시피에 없다.",
                inputs=inputs, refs=REFS)
        if r_km < POTATO_R_KM[1]:
            grade = "judgment"
            notes.append(
                f"반지름 {r_km:.0f} km 가 감자-구 전이 구간({POTATO_R_KM[0]:.0f}–"
                f"{POTATO_R_KM[1]:.0f} km) 안이다. 클래스는 나오지만 유체 평형이 "
                "보장되지 않으므로, 도형에 기대는 소비처(body_figure · nmoi)는 "
                "이 천체에서 별도 근거가 필요하다.")

    # ── 사다리 ──────────────────────────────────────────────────────────
    verdicts = [
        _rocky_vs_sub_neptune(mass_earth, radius_earth),
        _sub_neptune_vs_ice_giant(radius_earth),
        _ice_giant_vs_gas_giant(mass_earth, gmf, semi_major_axis_au),
        _gas_giant_vs_brown_dwarf(mass_earth),
        _brown_dwarf_vs_star(mass_earth),
    ]

    # 좁히는 경계만 등급에 든다. 이미 좁혀진 자리를 다시 미는 판정은 결론을 바꾸지
    # 않으므로, 그것의 약한 등급을 결론에 씌우면 답보다 낮게 말하게 된다 — 목성은
    # 3.5 R⊕ 의 관례선도 지나가지만 그 천체를 가스거대행성으로 만드는 것은 질량이다.
    lo, hi = 0, len(LADDER) - 1
    set_lo, set_hi = None, None
    for i, (v, _g, _why) in enumerate(verdicts):
        if v == ABOVE and i + 1 > lo:
            lo, set_lo = i + 1, i
        elif v == BELOW and i < hi:
            hi, set_hi = i, i
    decided_by = [BOUNDARY_NAMES[i] for i in (set_lo, set_hi) if i is not None]
    deciding = [verdicts[i][2] for i in (set_lo, set_hi) if i is not None]
    for i in (set_lo, set_hi):
        if i is not None:
            grade = _weakest(grade, verdicts[i][1])

    if lo > hi:
        # 경계들이 서로 어긋난다. 사다리는 질량 오름차순이므로 이건 물리가 아니라
        # 입력이 어긋났다는 뜻이다 — 좁히지 않고 겹치는 구간 전체를 돌려준다.
        lo, hi = hi, lo
        grade = "judgment"
        notes.append(
            "경계들이 서로 어긋난다. 사다리는 단조인데 반지름 쪽 판정과 질량 쪽 "
            "판정이 반대 방향을 가리켰다 — 질량과 반지름이 양립하지 않는다는 뜻이므로 "
            "(mass_radius.density_gate 가 그 검사다) 좁히지 않는다.")

    survivors = LADDER[lo:hi + 1]
    if len(survivors) > 1:
        grade = "judgment"

    # ── 선언과 대조 ─────────────────────────────────────────────────────
    declared = ALIASES.get(declared_class, declared_class)
    if declared_class in ALIASES:
        notes.append(
            f"선언이 '{declared_class}' 인데 이 어휘의 정본은 '{declared}' 다. 둘을 "
            "가르는 것이 이 저장소 어디에도 없고 (interior.GAS_GIANT_CLASSES 가 둘 다 "
            "받는다), 철자 변종을 메뉴에 들이는 것이 derivation-discipline §7 이 적은 "
            "표류의 경로다. 읽을 때만 정규화하고 선언은 건드리지 않는다.")
    agrees: bool | None = None
    if declared is not None:
        agrees = declared in survivors
        if declared not in LADDER:
            notes.append(
                f"선언된 '{declared_class}' 는 이 어휘 밖이다 — 쓸 수 있는 것: "
                f"{' · '.join(LADDER)}.")
        elif not agrees:
            notes.append(
                f"**선언과 도출이 어긋난다.** 보드는 '{declared_class}' 라고 적는데 "
                f"이 질량과 반지름이 허용하는 것은 {' 또는 '.join(survivors)} 다. "
                "어느 쪽이 맞는지는 이 노드가 정하지 않는다 — 선언이 관측 없는 "
                "천체의 오너 결정일 수 있고, 그러면 질량이나 반지름 쪽이 틀린 것이다.")

    narrowed = survivors[0] if len(survivors) == 1 else None
    head = (f"'{narrowed}' 로 좁혔다" if narrowed
            else f"좁히지 못했다 — {' 또는 '.join(survivors)} 가 다 살아 있다")
    reason = head + (". " + " · ".join(deciding) if deciding else
                     ". 어느 경계도 이 천체를 배제하지 못했다")

    return Result(
        recipe=RECIPE, version=VERSION,
        regime="narrowed" if narrowed else "ambiguous",
        reason=reason, grade=grade, inputs=inputs, refs=REFS,
        values={"class": narrowed,
                "classes": " | ".join(survivors),
                "decided_by": " + ".join(decided_by) or "nothing",
                "agrees_with_declared": agrees},
        units={"class": "", "classes": "", "decided_by": "",
               "agrees_with_declared": ""},
        notes=tuple(notes))


# ── 그래프에 붙이기 ─────────────────────────────────────────────────────
@recipe("body_class")
def _from_state(state):
    # **선언된 반지름만 읽는다.** interior_layers 도 mass_radius_relation 도 반지름을 내지만
    # 그건 조성을 가정하고 푼 결과라, 그걸로 분류하면 가정한 조성을 그대로 돌려받는다 —
    # rocky_roster.py 가 DB 의 "추정" 반지름에 역산을 걸지 않는 것과 같은 순환이다.
    # 선언이 없으면 질량 쪽 대체로 가고 등급이 내려간다.
    radius = state.get("radius_earth")
    if radius is None and state.get("radius_rj") is not None:
        radius = state["radius_rj"] * R_EARTH_PER_RJ
    return solve(
        mass_earth=state["mass_earth"],
        radius_earth=radius,
        declared_class=state.get("body_class"),
        composition_intent=state.get("composition_intent"),
        gas_mass_fraction=state.get("gas_mass_fraction"),
        semi_major_axis_au=state.get("semi_major_axis_au"),
    )
