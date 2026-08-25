# 정수압 평형과 질량보존을 상태방정식과 함께 적분해 층 구조를 푼다 — 층 밀도는 결과지 입력이 아니다
"""Integrate a body's interior instead of assuming its layer densities.

    from interior import solve

    solve(mass_earth=1.0, core_mass_fraction=0.325)
        → R 1.000 R⊕ · C/MR² 0.332 · 핵 경계 0.546 R · 중심압 358 GPa
          (지구 발표값 1.000 R⊕ · 0.3307 · 0.546)

**무엇이 바뀌었나.** 2026-08-25 까지 이 레시피는 층을 균질하다고 두고 닫힌 형태
두 줄을 평가했다. 층 밀도는 조성별 상수표에서 왔고, 그 표는 지구 질량 근처에서만
맞았다 — 수성을 그 표로 풀면 C/MR² 가 8.6 % 어긋났다. 층 밀도가 그 층이 받는
압력의 함수인데 상수로 뒀기 때문이다.

이제는 표가 없다. 질량과 조성만 받아서

    dm/dr = 4π r² ρ(P)
    dP/dr = −G m ρ(P) / r²
    ρ = ρ(P)                     ← eos.py, 재료마다 발표된 적합

를 중심에서 표면까지 적분한다. 층 밀도·반지름·중심압이 전부 **적분의 결과** 로
나온다. 중심압을 미지수로 두고 겉질량이 주어진 질량과 맞을 때까지 이분법으로
좁히는, 표준적인 사격법이다 (Seager+ 2007 §II, arXiv:0707.2895 의 eq. 1-3).

**등온이다.** 열보정은 넣지 않았다. 다만 핵과 하부맨틀의 상태방정식이 PREM 적합
(Zeng+ 2016) 이라서 지구의 실제 지오섬과 가벼운 원소가 그 유효 ρ₀ 안에 이미
들어 있다 — 열을 무시한 게 아니라 지구에서 교정된 형태로 흡수한 것이고, 그래서
지구가 재현된다. eos.py 의 fe_prem 주석에 그 사정이 적혀 있다.
"""
from __future__ import annotations

import math

from eos import MATERIALS, PhaseGap
from payload import Result, out_of_domain
from porosity import (MASS_COMPACT_KG, PHI0_NOMINAL, P_GRAIN_FRACTURE, P_LAB_MAX,
                      bulk_factor, porosity)

RECIPE = "interior-structure-methodology"
VERSION = "2"

REFS = (
    "2016ApJ...819..127Z",      # Zeng+ 2016 — PREM 을 BM2 로 적합한 핵·하부맨틀 EOS
    "2007ApJ...669.1279S",      # Seager+ 2007 — 구조 방정식과 enstatite·얼음VII EOS
    "2006JPCRD..35.1021F",      # Feistel & Wagner 2006 (IAPWS-06) — 얼음 Ih
    "2020JGRE..12506176J",      # Journaux+ 2020 (SeaFreeze) — 얼음 III·V·VI
    "2019Icar..326...10B",      # Bierson+ 2019 — 압력이 공극을 닫는 관계와 그 계수
    "2012P&SS...73...98C",      # Carry 2012 — 10 MPa 파쇄 문턱, 관측된 전이질량
    "1981PEPI...25..297D",      # PREM — 앵커로 쓰는 지구 C/MR²
)

G = 6.67430e-11
EARTH_MASS_KG = 5.972e24
EARTH_RADIUS_M = 6.371e6

# 조성 이름 → (핵질량분율, 얼음질량분율, 핵 재료). 숫자를 직접 주면 이건 기본값일 뿐이다.
#
# `iron` 만 순철(fe_eps)을 쓴다. 그 곡선의 용도가 "이보다 밀할 수 없다" 는 한계선을
# 긋는 것이라서, 가벼운 원소가 섞인 PREM 핵이 아니라 실험실 순철이어야 한다.
COMPOSITIONS: dict[str, tuple[float, float, str]] = {
    "iron":       (1.000, 0.00, "fe_eps"),
    "earth_like": (0.325, 0.00, "fe_prem"),
    "silicate":   (0.000, 0.00, "fe_prem"),
    "water":      (0.163, 0.50, "fe_prem"),
}

# 적분 격자. 1500 단계에서 C/MR² 가 격자를 네 배 촘촘히 해도 1.2e-4 (상대) 안에서
# 같다 — 앵커가 발표값과 어긋나는 폭(0.3 %)의 30분의 1이라 격자는 오차원이 아니다.
# test_interior.py 의 격자 수렴 검사가 그 숫자를 실제로 낸다.
STEPS = 1500
MAX_STEPS = 40000
SHOOT_ITERS = 200
SHOOT_TOL = 1e-8            # 겉질량의 상대오차


class Structure:
    """적분 한 번의 결과. Result 로 포장하기 전의 알맹이."""

    __slots__ = ("radius_m", "mass_kg", "moi", "core_radius_m", "p_center",
                 "p_cmb", "p_ice_base", "phases", "v_pore", "m_above_lab")

    def __init__(self, radius_m, mass_kg, moi, core_radius_m, p_center,
                 p_cmb, p_ice_base, phases, v_pore=0.0, m_above_lab=0.0):
        self.radius_m = radius_m
        self.mass_kg = mass_kg
        self.moi = moi
        self.core_radius_m = core_radius_m
        self.p_center = p_center
        self.p_cmb = p_cmb
        self.p_ice_base = p_ice_base
        self.phases = phases
        self.v_pore = v_pore              # 빈 공간의 부피 [m³]
        self.m_above_lab = m_above_lab    # 실험압 위에서 법칙을 외삽한 질량 [kg]

    @property
    def nmoi(self) -> float:
        return self.moi / (self.mass_kg * self.radius_m ** 2)

    @property
    def volume(self) -> float:
        return 4.0 / 3.0 * math.pi * self.radius_m ** 3

    @property
    def phi_bulk(self) -> float:
        """벌크 공극률. 빈 공간의 부피를 천체 부피로 나눈 것."""
        return self.v_pore / self.volume


def _stack(cmf: float, imf: float, core_material: str):
    """바깥으로 가는 층의 열. (누적질량분율 상한, 재료) 로 준다."""
    out = []
    if cmf > 0:
        out.append((cmf, MATERIALS[core_material]))
    if 1.0 - cmf - imf > 0:
        out.append((1.0 - imf, MATERIALS["silicate"]))
    if imf > 0:
        out.append((1.0, MATERIALS["h2o"]))
    return out


def integrate(p_center: float, mass_kg: float, cmf: float, imf: float,
              core_material: str, phi0: float = 0.0,
              p_cap: float | None = None) -> Structure:
    """중심압 하나에서 바깥으로 적분한다. 표면(P=0)에서 멈춘다.

    층 경계는 **목표 질량** 의 누적 분율로 잡는다. 사격이 수렴하면 겉질량이 목표와
    같으므로 이 선택은 수렴점에서 정확하고, 반복마다 경계가 흔들리지 않아 이분법이
    단조를 유지한다.

    `phi0` 가 0 보다 크면 각 자리의 고체 밀도에 (1 − φ(P)) 를 곱한다. φ 는 **국소
    압력의 함수** 이므로 자유 매개변수가 아니다 — porosity.py 를 보라. φ₀ 자체는
    강착과 가열이 정하고 이 레시피에 그 둘이 없어서 선언으로 들어온다."""
    stack = _stack(cmf, imf, core_material)
    mat = stack[0][1]

    rho_c = mat.density(p_center) * bulk_factor(mat.name, p_center, phi0, p_cap)
    r_scale = (3.0 * mass_kg / (4.0 * math.pi * rho_c)) ** (1.0 / 3.0)
    dr = r_scale / STEPS

    r = dr
    m = 4.0 / 3.0 * math.pi * r ** 3 * rho_c
    moi = 8.0 / 15.0 * math.pi * r ** 5 * rho_c
    p = p_center
    core_radius = 0.0 if cmf <= 0 else None
    p_cmb = None
    p_ice_base = None
    phases: list[str] = []
    layer = 0
    v_pore = 4.0 / 3.0 * math.pi * r ** 3 * porosity_at(mat, p, phi0, p_cap)
    m_above_lab = m if p > P_LAB_MAX else 0.0

    def material_for(m_now: float):
        nonlocal layer
        while layer < len(stack) - 1 and m_now >= stack[layer][0] * mass_kg:
            layer += 1
        return stack[layer][1]

    steps = 0
    while p > 0.0 and steps < MAX_STEPS:
        steps += 1
        prev_layer = layer
        mat = material_for(m)
        if layer != prev_layer:
            # 층이 바뀐 자리의 압력을 기록해둔다. core_state 와 얼음 상 판정이 쓴다.
            if prev_layer == 0 and cmf > 0:
                core_radius, p_cmb = r, p
            if stack[layer][1].name == "h2o":
                p_ice_base = p
        if mat.name not in phases:
            phases.append(mat.name)

        # 4차 Runge-Kutta. 한 단계 안에서는 재료를 고정한다 — 경계에서 한 단계
        # 어긋나는 오차는 dr/R ~ 3e-4 이라 C/MR² 의 유효숫자 밖이다.
        def deriv(rr, mm, pp):
            if rr <= 0.0:
                return 0.0, 0.0, 0.0, 0.0
            rr_rho = mat.density(pp) if pp > 0.0 else mat.rho0
            phi = porosity_at(mat, pp, phi0, p_cap)
            rr_rho *= 1.0 - phi
            return (4.0 * math.pi * rr * rr * rr_rho,
                    -G * mm * rr_rho / (rr * rr),
                    8.0 / 3.0 * math.pi * rr ** 4 * rr_rho,
                    4.0 * math.pi * rr * rr * phi)

        k1 = deriv(r, m, p)
        k2 = deriv(r + dr / 2, m + dr / 2 * k1[0], p + dr / 2 * k1[1])
        k3 = deriv(r + dr / 2, m + dr / 2 * k2[0], p + dr / 2 * k2[1])
        k4 = deriv(r + dr, m + dr * k3[0], p + dr * k3[1])
        dm = dr / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        dp = dr / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        di = dr / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
        dv = dr / 6 * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3])

        if p + dp <= 0.0:
            # 표면을 넘어섰다. P=0 자리로 선형 보간해서 멈춘다.
            frac = p / (-dp) if dp != 0 else 0.0
            r += dr * frac
            m += dm * frac
            moi += di * frac
            v_pore += dv * frac
            p = 0.0
            break

        if p > P_LAB_MAX:
            m_above_lab += dm
        r += dr
        m += dm
        p += dp
        moi += di
        v_pore += dv

    if steps >= MAX_STEPS:
        raise ValueError(f"{MAX_STEPS} 단계 안에 표면에 닿지 못했다 "
                         f"(중심압 {p_center / 1e9:.3g} GPa)")

    if core_radius is None:
        core_radius = r      # 핵만 있는 천체
        p_cmb = p
    return Structure(r, m, moi, core_radius, p_center, p_cmb, p_ice_base, phases,
                     v_pore=v_pore, m_above_lab=m_above_lab)


def porosity_at(mat, p_pa: float, phi0: float,
                p_cap: float | None = None) -> float:
    """이 재료가 이 압력에서 들고 있는 공극률. 법칙이 없는 재료는 0."""
    if phi0 <= 0.0:
        return 0.0
    return 1.0 - bulk_factor(mat.name, max(p_pa, 0.0), phi0, p_cap)


def shoot(mass_kg: float, cmf: float, imf: float,
          core_material: str, phi0: float = 0.0,
          p_cap: float | None = None) -> tuple[Structure, bool]:
    """겉질량이 목표와 맞는 중심압을 찾는다. 질량은 중심압에 단조증가한다.

    수렴 여부를 값과 함께 돌려준다 — 못 맞춘 것은 예외가 아니라 `converged=False`
    를 단 결과다. 예외로 던지면 호출자가 그 사실을 조용히 삼킬 수 있다."""
    # 비압축 반지름에서 중심압을 어림해 괄호를 잡는다. 재료의 유효 상한을 넘겨서
    # 잡으면 상 구간 밖이라 PhaseGap 이 나므로, 위쪽은 그 상한에서 멈춘다.
    stack = _stack(cmf, imf, core_material)
    rho0_bar = 1.0 / sum(
        (hi_f - (stack[i - 1][0] if i else 0.0))
        / (mat.rho0 * bulk_factor(mat.name, 0.0, phi0, p_cap))
        for i, (hi_f, mat) in enumerate(stack))
    r0 = (3.0 * mass_kg / (4.0 * math.pi * rho0_bar)) ** (1.0 / 3.0)
    # 중심압은 가장 안쪽 재료가 받는다. 바깥 층의 상한은 적분 중에 PhaseGap 이
    # 스스로 잡으므로 여기서 겹쳐 걸면 엉뚱한 층 때문에 거절하게 된다.
    p_ceiling = stack[0][1].p_max
    lo = 1.0e2
    hi = min(3.0 * G / (8.0 * math.pi) * mass_kg ** 2 / r0 ** 4 * 4.0, p_ceiling)
    while integrate(hi, mass_kg, cmf, imf, core_material, phi0, p_cap).mass_kg < mass_kg:
        if hi >= p_ceiling:
            raise ValueError(
                f"이 질량을 담으려면 중심압이 {stack[0][1].name} 의 근거 구간 상한"
                f"({p_ceiling / 1e9:.0f} GPa) 을 넘어야 한다. 그 위는 전자축퇴가 "
                "지배하는 영역이고 (Thomas-Fermi-Dirac), 이 레시피에는 그 상태방정식이 "
                "없다 — Seager+ 2007 §III.2 가 그 자리를 채우는 방법을 적어두었다.")
        hi = min(hi * 4.0, p_ceiling)
    # log M 은 log P_c 에 거의 선형이라 할선법이 몇 번 만에 붙는다. 벗어나면
    # 괄호 안의 로그 이분법으로 되돌린다 — 적분 한 번이 비싸서 반복 횟수가 곧 비용이다.
    st = integrate(hi, mass_kg, cmf, imf, core_material, phi0, p_cap)
    if abs(st.mass_kg - mass_kg) / mass_kg < SHOOT_TOL:
        return st, True
    x0, y0 = math.log(hi), math.log(st.mass_kg / mass_kg)
    x1 = math.log(max(lo, hi * 1e-3))
    st = integrate(math.exp(x1), mass_kg, cmf, imf, core_material, phi0, p_cap)
    y1 = math.log(st.mass_kg / mass_kg)
    for _ in range(SHOOT_ITERS):
        if abs(st.mass_kg - mass_kg) / mass_kg < SHOOT_TOL:
            return st, True
        if st.mass_kg < mass_kg:
            lo = math.exp(x1)
        else:
            hi = math.exp(x1)
        if y1 != y0:
            x2 = x1 - y1 * (x1 - x0) / (y1 - y0)
        else:
            x2 = 0.5 * (math.log(lo) + math.log(hi))
        if not (math.log(lo) <= x2 <= math.log(hi)):
            x2 = 0.5 * (math.log(lo) + math.log(hi))
        x0, y0 = x1, y1
        x1 = x2
        st = integrate(math.exp(x1), mass_kg, cmf, imf, core_material, phi0, p_cap)
        y1 = math.log(st.mass_kg / mass_kg)
    return st, False


# 고체 표면이 없는 천체. 여기 있는 상태방정식은 전부 응축상이라 H/He 외피에는
# 쓸 수 없다 — 그쪽은 폴리트로프이고 다른 문헌이다.
FLUID_CLASSES = ("giant", "gas_giant", "ice_giant", "sub_neptune", "brown_dwarf", "star")


def solve(mass_earth: float,
          core_mass_fraction: float | None = None,
          ice_mass_fraction: float | None = None,
          composition: str = "earth_like",
          radius_earth: float | None = None,
          differentiated: bool = True,
          body_class: str | None = None,
          initial_porosity: float = 0.0,
          porosity_cap: float | None = None) -> Result:
    """질량과 조성에서 층 구조를 적분한다.

    `radius_earth` 는 계산에 **쓰이지 않는다** — 반지름은 출력이다. 주면 도출값과
    대조해서, 선언한 조성이 그 천체를 재현하는지 판정하고 어긋나면 무엇이 빠졌는지
    이름을 댄다."""
    preset_cmf, preset_imf, core_material = COMPOSITIONS.get(
        composition, (None, None, "fe_prem"))
    cmf = preset_cmf if core_mass_fraction is None else core_mass_fraction
    imf = preset_imf if ice_mass_fraction is None else ice_mass_fraction

    inputs = {"mass_earth": mass_earth, "radius_earth": radius_earth,
              "core_mass_fraction": cmf, "ice_mass_fraction": imf,
              "composition": composition, "differentiated": differentiated,
              "body_class": body_class, "initial_porosity": initial_porosity,
              "porosity_cap": porosity_cap}

    if body_class in FLUID_CLASSES:
        return out_of_domain(
            RECIPE, VERSION,
            f"'{body_class}' 는 고체 표면이 없다. 이 레시피의 상태방정식은 철·규산염·"
            "얼음, 전부 응축상이라 수소-헬륨 외피에 쓸 수 없다 — 그쪽은 폴리트로프 "
            "영역이고 다른 문헌이다 (Fortney+ 2007, Baraffe+ 2008). 무거운 원소 핵만 "
            "따로 풀고 싶다면 그 핵의 질량을 이 레시피에 주면 된다.",
            inputs=inputs, refs=REFS)

    if composition not in COMPOSITIONS:
        return out_of_domain(
            RECIPE, VERSION,
            f"'{composition}' 는 재료가 배정된 조성이 아니다. "
            f"쓸 수 있는 것: {', '.join(COMPOSITIONS)}",
            inputs=inputs, refs=REFS)

    if mass_earth <= 0:
        return out_of_domain(RECIPE, VERSION, "질량이 양수가 아니다",
                             inputs=inputs, refs=REFS)

    if not differentiated:
        return out_of_domain(
            RECIPE, VERSION,
            "미분화 천체다 — 금속이 있는데 가라앉지 않아 맨틀에 섞여 있는 상태다. "
            "이 솔버는 층마다 순수한 재료의 상태방정식을 쌓는 구조라, 금속과 규산염이 "
            "한 층 안에 섞인 혼합상을 표현할 방법이 없다. 필요한 것은 혼합물 "
            "상태방정식(부피 가법 혼합 또는 Voigt-Reuss-Hill 평균)이고, 그게 들어오면 "
            "이 천체는 풀린다. 핵질량분율을 0 으로 두는 것은 다른 상태다 — 그건 금속이 "
            "아예 없다는 뜻이지 섞여 있다는 뜻이 아니다.",
            inputs=inputs, refs=REFS)

    if not 0.0 <= initial_porosity < 1.0:
        return out_of_domain(
            RECIPE, VERSION,
            f"초기 공극률 {initial_porosity} 가 [0, 1) 밖이다. 0 은 '공극이 없다' 는 "
            "주장이 아니라 '이 레시피가 판정하지 않는다' 는 뜻이다 — φ₀ 는 강착이 "
            "정하고 가열이 지우며, 이 레시피에는 그 둘이 없다.",
            inputs=inputs, refs=REFS)

    if not 0.0 <= cmf <= 1.0 or not 0.0 <= imf <= 1.0 or cmf + imf > 1.0:
        return out_of_domain(
            RECIPE, VERSION,
            f"질량분율이 맞지 않는다 — 핵 {cmf}, 얼음 {imf}. "
            "둘 다 [0, 1] 안이고 합이 1 이하여야 한다.",
            inputs=inputs, refs=REFS)

    try:
        st, converged = shoot(mass_earth * EARTH_MASS_KG, cmf, imf, core_material,
                              initial_porosity, porosity_cap)
    except PhaseGap as gap:
        return out_of_domain(RECIPE, VERSION, gap.reason, inputs=inputs, refs=REFS,
                             notes=(f"막힌 재료: {gap.material}, "
                                    f"압력 {gap.pressure_pa / 1e9:.4f} GPa",))
    except ValueError as err:
        return out_of_domain(RECIPE, VERSION, f"적분이 실패했다 — {err}",
                             inputs=inputs, refs=REFS)

    radius = st.radius_m / EARTH_RADIUS_M
    rho_bar = st.mass_kg / (4.0 / 3.0 * math.pi * st.radius_m ** 3)
    bounds = [f"중심 {st.p_center / 1e9:.3g} GPa"]
    if st.p_cmb is not None and cmf > 0:
        bounds.append(f"핵-맨틀 경계 {st.p_cmb / 1e9:.3g} GPa")
    if st.p_ice_base is not None:
        bounds.append(f"얼음 기둥 바닥 {st.p_ice_base / 1e9:.3g} GPa")
    notes = [f"층별 상: {' → '.join(st.phases)}. {' · '.join(bounds)}, "
             f"평균밀도 {rho_bar:.0f} kg/m³.",]
    if initial_porosity > 0:
        notes.append(_porosity_note(st, initial_porosity, mass_earth))
    notes += [
             "이 노드는 결합 코어 안에 있다 (chain.yaml 순환 1·3). converged 는 "
             "**이 적분의 사격이 붙었는가** 를 말하지, 조석가열이 조성을 되바꾸는 "
             "그래프 고리가 닫혔는가를 말하지 않는다 — 그 고리는 러너가 코어를 "
             "돌릴 때 닫힌다.",
             "등온이다. 핵과 하부맨틀 EOS 가 PREM 적합이라 지구의 열구조와 가벼운 "
             "원소가 그 유효 ρ₀ 안에 흡수돼 있다."]

    reason = (f"{mass_earth:.4g} M⊕ 를 핵질량분율 {cmf:.3f}"
              + (f" · 얼음질량분율 {imf:.3f}" if imf > 0 else "")
              + (f" · 초기공극 {initial_porosity:.2f}" if initial_porosity > 0 else "")
              + f" 로 적분했다. 정수압 평형이 반지름 {radius:.4f} R⊕ 와 "
              f"중심압 {st.p_center / 1e9:.1f} GPa 를 주고, 그 압력 분포에서 층 밀도가 "
              f"결정되므로 자기압축이 C/MR² 에 들어간다.")

    if radius_earth is not None:
        off = (radius_earth - radius) / radius
        notes.append(
            f"선언된 반지름 {radius_earth:.4f} R⊕ 대비 도출값이 {off * -100:+.1f} % 다.")
        if abs(off) > 0.03:
            notes.append(
                "3 % 를 넘는다. 조성 선언이 이 천체를 재현하지 못한다는 뜻이므로, "
                "핵질량분율이나 얼음질량분율을 관측 반지름에서 역산할 것 "
                "(infer_composition)." )

    return Result(
        recipe=RECIPE, version=VERSION,
        regime="integrated_" + ("_".join(st.phases) if len(st.phases) > 1 else st.phases[0]),
        reason=reason,
        # 공극이 켜지면 등급이 내려간다. 압밀 곡선의 실험 상한 위로 외삽하게 되고,
        # φ₀ 자체가 이 레시피가 도출하지 못하는 선언값이다.
        grade="analog" if initial_porosity > 0 else "calibrated",
        inputs=inputs,
        cycles=(1, 3),
        converged=converged,
        values={"nmoi": st.nmoi,
                "core_radius_fraction": st.core_radius_m / st.radius_m,
                "core_radius": st.core_radius_m / EARTH_RADIUS_M,
                "radius": radius,
                "core_pressure": st.p_center / 1e9},
        units={"nmoi": "dimensionless",
               "core_radius_fraction": "dimensionless",
               "core_radius": "R_earth",
               "radius": "R_earth",
               "core_pressure": "GPa"},
        refs=REFS,
        notes=tuple(notes),
    )


def _porosity_note(st, phi0: float, mass_earth: float) -> str:
    """공극이 켜졌을 때 무엇을 했고 어디가 외삽인지 한 줄로 적는다."""
    mass_kg = st.mass_kg
    frac = st.m_above_lab / mass_kg if mass_kg else 0.0
    line = (f"공극이 켜져 있다 — 초기공극 {phi0:.2f}, 벌크 공극률 {st.phi_bulk:.3f}. "
            f"φ 는 국소 압력의 함수이고(Bierson+ 2019 식 1·2) 자유 매개변수가 아니다. "
            f"중심압 {st.p_center / 1e6:.0f} MPa 가 규산염 입자 파쇄 문턱"
            f"({P_GRAIN_FRACTURE / 1e6:.0f} MPa) 의 "
            f"{st.p_center / P_GRAIN_FRACTURE:.0f} 배다.")
    if frac > 0:
        line += (f" 압밀 곡선을 실험 상한({P_LAB_MAX / 1e6:.0f} MPa) 위로 외삽한 질량 "
                 f"몫이 {frac * 100:.1f} % 다 — 그 구간은 측정된 적이 없다.")
    if mass_kg > MASS_COMPACT_KG:
        line += (f" 그리고 이 천체는 {mass_kg / MASS_COMPACT_KG:.0f} × 10²⁰ kg 이다. "
                 "Carry 2012 §5.2 는 10²⁰ kg 위의 천체가 관측상 전부 macroporosity ≈ 0 "
                 "이라고 보고한다 — 이 법칙의 검증 범위 밖이라는 뜻이고, 여기서 나온 "
                 "공극은 예측이 아니라 **상한** 으로 읽어야 한다.")
    return line


# ── 역산: 질량과 반지름에서 조성을 되찾는다 ──────────────────────────────
#
# 위성 대부분은 조성이 선언돼 있지 않고 질량과 반지름만 있다. 순방향 솔버를 한 번
# 뒤집으면 그 둘을 재현하는 자유 분율 하나가 나온다 — 암석보다 밀하면 핵질량분율,
# 덜 밀하면 얼음질량분율이다.
#
# **이 역산은 유일하지 않다.** 작은 천체에서 중심압이 낮으면 공극이 살아남고, 공극과
# 얼음은 밀도를 같은 방향으로 낮춘다. 얼음 30 % 인 치밀한 천체와 얼음 15 % 에 공극
# 15 % 인 천체는 이 솔버가 구분하지 못한다. 그래서 반환값의 note 가 그 축퇴를 명시하고,
# 등급을 analog 로 내린다.

INFER_TOL = 5e-4        # 반지름 상대오차
SCAN_POINTS = 13        # 자유 분율 축을 훑는 눈금 수


def _porous_rock_verdict(mass_earth: float, radius_earth: float,
                         rock: Result, inputs: dict) -> Result:
    """얼음이 선언으로 배제된 저밀도 천체를 공극으로 설명할 수 있는지 판정한다.

    **맞추지 않는다.** 발표된 법칙을 발표된 초기공극 φ₀ = 0.60 (Bierson+ 2019
    Table 1 의 nominal) 으로 돌려 이 질량이 가질 수 있는 **최대 반지름** 을 낸다.
    Bierson 자신이 자기 모형을 "a lower bound on the bulk density (the most
    porosity that can be retained)" 라고 적으므로, 그 반지름은 상한이다.

    봉투를 **두 개** 낸다. 발표된 대로 전 구간에 법칙을 적용한 것과, 실험 상한
    150 MPa 위에서는 아무것도 주장하지 않는 것. 판정은 **보수적인 쪽** 으로 한다 —
    결론이 측정된 적 없는 외삽에 기대면 안 되기 때문이다. 둘이 갈리면 그 사실이
    결론이 된다.

    그러면 선언된 반지름이 셋 중 하나에 떨어진다.

    * 공극 0 반지름보다 작다 → 공극이 아니라 금속이 필요하다. 호출자가 핵 축으로.
    * 공극 0 과 최대 사이 → 봉투 안이다. 그 반지름을 재현하는 φ₀ 를 되읽어 준다.
      **되읽은 값이지 적합한 상수가 아니다** — 등급이 analog 로 내려가고, φ₀ 를
      도출하는 것은 강착·열이력의 일이라고 note 가 말한다.
    * 최대보다 크다 → 발표된 최대 공극으로도 못 미친다. 선언된 질량-반지름 쌍이
      물리와 안 맞는다는 뜻이고, 그게 답이다.
    """
    km = EARTH_RADIUS_M / 1e3
    r_solid = rock.values["radius"]
    mass_kg = mass_earth * EARTH_MASS_KG

    def at(phi, cap):
        return solve(mass_earth, core_mass_fraction=0.0, ice_mass_fraction=0.0,
                     initial_porosity=phi, porosity_cap=cap)

    top_pub = at(PHI0_NOMINAL, None)
    top_cap = at(PHI0_NOMINAL, P_LAB_MAX)
    if not (top_pub.applicable and top_cap.applicable):
        blocked = top_pub if not top_pub.applicable else top_cap
        return out_of_domain(
            RECIPE, VERSION,
            f"공극을 켠 규산염 적분이 풀리지 않는다 — {blocked.reason}",
            inputs=inputs, refs=REFS)
    r_pub = top_pub.values["radius"]
    r_cap = top_cap.values["radius"]

    envelope = (f"공극 0 이면 {r_solid * km:.0f} km, 발표된 초기공극 "
                f"{PHI0_NOMINAL:.2f} 로는 {r_pub * km:.0f} km, 실험 상한"
                f"({P_LAB_MAX / 1e6:.0f} MPa) 위를 안 믿으면 {r_cap * km:.0f} km 다. "
                f"선언된 값은 {radius_earth * km:.0f} km.")
    heavy = (f"이 천체는 {mass_kg / MASS_COMPACT_KG:.0f} × 10²⁰ kg 이다. Carry 2012 "
             "§5.2 는 10²⁰ kg 위의 천체가 관측상 전부 macroporosity ≈ 0 이라고 보고하고"
             "('The pressure inside an object with a mass lower than ≈10²⁰ kg never "
             "reaches 10⁷ Pa'), 이 법칙이 검증된 곳은 그 아래다. 여기서 나온 공극은 "
             "예측이 아니라 **봉투** 로 읽어야 한다."
             ) if mass_kg > MASS_COMPACT_KG else ""

    if radius_earth > r_cap:
        over = "발표된 대로 외삽해도" if radius_earth > r_pub else "보수적으로 읽으면"
        return out_of_domain(
            RECIPE, VERSION,
            f"{over} 이 반지름에 못 미친다. {envelope} Bierson+ 2019 의 모형은 자기 "
            "자신을 밀도의 하한, 즉 남을 수 있는 **최대** 공극이라고 적으므로 이 봉투는 "
            "상한이다. 그래서 답은 다공도가 아니다 — **선언된 질량-반지름 쌍이 물리와 "
            "맞지 않는다**, 또는 암석이 이 레시피가 든 규산염보다 가볍다. " + heavy,
            inputs=inputs, refs=REFS,
            notes=(envelope, "선언값이 봉투 위에 있다.") +
                  ((heavy,) if heavy else ()))

    # 봉투 안이다. 반지름을 재현하는 φ₀ 를 보수적 읽기로 되읽는다.
    lo, hi = 0.0, PHI0_NOMINAL
    best, phi = top_cap, PHI0_NOMINAL
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        res = at(mid, P_LAB_MAX)
        if not res.applicable:
            break
        best, phi = res, mid
        got = res.values["radius"]
        if abs(got - radius_earth) / radius_earth < INFER_TOL:
            break
        if got < radius_earth:
            lo = mid
        else:
            hi = mid

    inputs["initial_porosity"] = phi
    inputs["porosity_cap"] = P_LAB_MAX
    notes = [f"역산이다 — 초기공극 φ₀ = {phi:.3f} 가 선언된 반지름을 재현한다. "
             f"실험 상한 위를 믿지 않는 보수적 읽기로 풀었으므로, 이 결론은 측정된 "
             f"구간에만 기댄다. {envelope}"]
    notes += list(best.notes)
    notes.append("φ₀ 는 **되읽은 값이지 적합한 상수가 아니다.** 그 값을 도출하는 것은 "
                 "강착이 남긴 초기 공극과 그 뒤의 가열 이력의 일이고, 이 레시피에는 "
                 "둘 다 없다. Bierson+ 2019 §2.2 가 자기 모형이 다루지 않는 것을 "
                 "나열한다 — melt production, differentiation, convection, impacts, "
                 "tidal heating. 다섯 다 공극을 **더** 없애는 방향이므로, 여기 나온 "
                 "φ₀ 는 그 반지름을 내는 데 필요한 값이고 그 다섯 중 하나가 이 천체에 "
                 "걸려 있으면 실제로 남았을 공극은 이보다 적다.")
    notes.append("얼음과 공극은 평균밀도를 같은 방향으로 낮춘다. 이 천체는 보드가 "
                 "얼음을 배제해서 공극 축으로 풀렸지만, 그 선언이 바뀌면 얼음 축의 해도 "
                 "똑같이 잘 맞는다 — 질량과 반지름만으로는 둘을 가를 수 없다.")
    if heavy:
        notes.append(heavy)

    return Result(
        recipe=RECIPE, version=VERSION, regime="inferred_initial_porosity",
        reason=(f"질량 {mass_earth:.3g} M⊕ 와 반지름 {radius_earth:.4f} R⊕ 가 둘 다 "
                "주어졌고 얼음이 선언으로 배제됐다. 남는 기작은 빈 공간이므로, 압력이 "
                f"공극을 닫는 발표된 관계식을 두고 초기공극 하나를 풀면 {phi:.3f} 에서 "
                "반지름이 맞는다."),
        grade="analog",
        inputs=inputs,
        cycles=(1, 3),
        converged=best.converged,
        values=dict(best.values), units=best.units, refs=REFS, notes=tuple(notes),
    )


def infer_composition(mass_earth: float, radius_earth: float,
                      ice_allowed: bool = True) -> Result:
    """질량과 반지름을 재현하는 자유 분율 하나를 푼다.

    금속도 얼음도 없는 순수 규산염을 기준선으로 잡는다. 관측 반지름이 그보다
    작으면 금속을 넣어야 하므로 핵질량분율을 풀고, 크면 얼음을 넣어야 하므로
    얼음질량분율을 푼다.

    축을 **먼저 훑고** 이분법으로 좁힌다. 곧장 이분법을 돌리면 상 구간의 틈에
    떨어진 시험값 하나 때문에 멈추는데, 그 값이 답인지 지나가던 자리인지 구분이
    안 된다. 훑어두면 답이 틈 안에 있는지 밖에 있는지 말할 수 있다.

    `ice_allowed=False` 는 **선언이지 물리가 아니다.** 호출자가 그 천체를 얼음 없는
    것으로 이미 정해두었다는 뜻이고, 그러면 얼음 축은 후보에서 빠진다. 기준선보다
    가벼운데 얼음을 못 쓰면 남는 기작은 빈 공간뿐이므로 거기서 거절한다.

    이 인자가 없던 동안 이 함수는 밀도만 보고 축을 골랐고, 보드가 규산염 화산체로
    선언한 천체에 얼음을 붙여 "얼음 상이 필요하다" 는 틀린 진술을 냈다. 저밀도의
    원인을 가려내는 것이 이 레시피의 일인데, 바로 그 자리에서 새고 있었다."""
    inputs = {"mass_earth": mass_earth, "radius_earth": radius_earth,
              "core_mass_fraction": None, "ice_mass_fraction": None,
              "composition": "inferred", "differentiated": True,
              "ice_allowed": ice_allowed, "body_class": None}

    if mass_earth <= 0 or radius_earth <= 0:
        return out_of_domain(RECIPE, VERSION, "질량 또는 반지름이 양수가 아니다",
                             inputs=inputs, refs=REFS)

    rock = solve(mass_earth, core_mass_fraction=0.0, ice_mass_fraction=0.0)
    if not rock.applicable:
        return rock

    if radius_earth <= rock.values["radius"]:
        axis, span = "core_mass_fraction", (0.0, 1.0)

        def at(x):
            return solve(mass_earth, core_mass_fraction=x, ice_mass_fraction=0.0)
    elif not ice_allowed:
        # 기준선보다 가벼운데 얼음이 선언으로 배제돼 있다. 남는 기작은 빈 공간이고,
        # 이제 그 빈 공간에 근거된 관계식이 있다 — 그래서 여기서 끝나지 않는다.
        return _porous_rock_verdict(mass_earth, radius_earth, rock, inputs)
    else:
        axis, span = "ice_mass_fraction", (0.0, 0.98)

        def at(x):
            return solve(mass_earth, core_mass_fraction=0.0, ice_mass_fraction=x)

    # 1) 축을 훑는다. 값이 나오는 눈금과 막힌 눈금을 모두 들고 간다.
    grid = [span[0] + (span[1] - span[0]) * i / (SCAN_POINTS - 1)
            for i in range(SCAN_POINTS)]
    scan = [(x, at(x)) for x in grid]
    solved = [(x, res) for x, res in scan if res.applicable]

    if not solved:
        blocked = scan[0][1]
        return out_of_domain(
            RECIPE, VERSION,
            f"{axis} 축 위 어느 값에서도 구조가 나오지 않는다. {blocked.reason}",
            inputs=inputs, refs=REFS)

    # 2) 목표 반지름을 감싸는, **둘 다 풀린** 이웃 눈금 쌍을 찾는다.
    bracket = None
    for (xa, ra), (xb, rb) in zip(scan, scan[1:]):
        if not (ra.applicable and rb.applicable):
            continue
        lo_r, hi_r = sorted((ra.values["radius"], rb.values["radius"]))
        if lo_r <= radius_earth <= hi_r:
            bracket = (xa, xb)
            break

    if bracket is None:
        widest = max(solved, key=lambda t: t[1].values["radius"])
        blocked = [(x, res) for x, res in scan if not res.applicable]
        if axis == "ice_mass_fraction" and not blocked:
            return out_of_domain(
                RECIPE, VERSION,
                f"{radius_earth * EARTH_RADIUS_M / 1e3:.0f} km 는 이 질량을 물얼음으로 "
                f"거의 다 채워도 못 미치는 크기다 (얼음 {widest[0]:.2f} 가 "
                f"{widest[1].values['radius'] * EARTH_RADIUS_M / 1e3:.0f} km). 암석과 "
                "얼음의 어떤 배합으로도 이 밀도가 안 나온다 — 남은 기작은 빈 공간이 "
                "남아 있는 것(다공도)이거나 H/He 외피다. **다공도 모형이 없어서** 못 "
                "푸는 경우가 이것이고, 압밀 곡선이 들어오면 풀린다.",
                inputs=inputs, refs=REFS)
        why = blocked[0][1].reason if blocked else "이유 미상"
        return out_of_domain(
            RECIPE, VERSION,
            f"목표 반지름을 감싸는 배합이 {axis} 축의 **막힌 구간 안** 에 있다. "
            f"풀리는 눈금은 {len(solved)}/{len(scan)} 개뿐이고, 그 어느 쌍도 "
            f"{radius_earth * EARTH_RADIUS_M / 1e3:.0f} km 를 감싸지 못한다. {why}",
            inputs=inputs, refs=REFS,
            notes=(f"풀린 눈금의 반지름 범위 "
                   f"{min(r.values['radius'] for _, r in solved) * EARTH_RADIUS_M / 1e3:.0f}"
                   f"-{max(r.values['radius'] for _, r in solved) * EARTH_RADIUS_M / 1e3:.0f} km",
                   "**얼음층이 없어서** 가 아니라 그 압력의 얼음 상태방정식이 없어서 "
                   "막혔다. 물얼음 사다리는 Ih 부터 VII 까지 이어져 있으므로, 남은 상한은 "
                   "37.4 GPa 위의 얼음 X·초이온상 하나다.",))

    # 3) 이분법. 감싼 구간 안이라 반드시 값이 나온다. 얼음은 넣을수록 반지름이
    #    커지고 금속은 넣을수록 작아지므로, 어느 쪽으로 좁힐지는 축이 정한다.
    lo, hi = bracket
    grows = axis == "ice_mass_fraction"
    x, best = lo, at(lo)
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        res = at(mid)
        if not res.applicable:
            break
        best, x = res, mid
        got = res.values["radius"]
        if abs(got - radius_earth) / radius_earth < INFER_TOL:
            break
        if (got < radius_earth) == grows:
            lo = mid
        else:
            hi = mid
    inputs[axis] = x
    v = dict(best.values)
    notes = list(best.notes)
    notes.insert(0, f"역산이다 — {axis} = {x:.3f} 가 선언된 반지름을 재현한다.")
    notes.append(
        f"이 배합은 유일하지 않다. 중심압 {v['core_pressure'] * 1e3:.0f} MPa 는 공극이 "
        "살아남을 수 있는 크기이고, 공극과 얼음은 평균밀도를 같은 방향으로 낮춘다. "
        "얼음을 줄이고 다공도를 넣은 해가 똑같이 잘 맞는다 — 둘을 가르려면 압밀 곡선이 "
        "필요하고 그건 이 레시피에 없다.")

    return Result(
        recipe=RECIPE, version=VERSION, regime="inferred_" + axis,
        reason=(f"질량 {mass_earth:.3g} M⊕ 와 반지름 {radius_earth:.4f} R⊕ 가 둘 다 "
                f"주어져 조성이 과결정이다. 나머지를 고정하고 {axis} 하나를 풀면 "
                f"{x:.3f} 에서 반지름이 맞는다."),
        grade="analog",
        inputs=inputs,
        cycles=(1, 3),
        converged=best.converged,
        values=v, units=best.units, refs=REFS, notes=tuple(notes),
    )


# ── 그래프에 붙이기 ─────────────────────────────────────────────────────
from registry import recipe  # noqa: E402


@recipe("interior_layers")
def _from_state(state):
    return solve(
        mass_earth=state["mass_earth"],
        core_mass_fraction=state.get("core_mass_fraction"),
        ice_mass_fraction=state.get("ice_mass_fraction"),
        composition=state.get("composition_intent", "earth_like"),
        radius_earth=state.get("radius_earth"),
        differentiated=state.get("differentiated", True),
        body_class=state.get("body_class"),
        # 공극은 **선언** 으로 들어온다. 기본값 0 은 "공극이 없다" 가 아니라
        # "이 레시피가 판정하지 않는다" 는 뜻이다 — φ₀ 는 강착이 정하고 가열이 지운다.
        initial_porosity=state.get("initial_porosity", 0.0),
        porosity_cap=state.get("porosity_cap"),
    )
