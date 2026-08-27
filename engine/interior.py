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

from eos import (EARTH_POTENTIAL_T, ICE_VII_TO_X,
                 ICE_VII_X_T_MAX, MATERIALS, SILICATE_PREM_TO_PV,
                 PhaseGap, mix)
from payload import Result, out_of_domain
from porosity import (MASS_COMPACT_KG, PHI0_NOMINAL, P_GRAIN_FRACTURE, P_LAB_MAX,
                      bulk_factor, porosity, voids_expected)

RECIPE = "interior-structure-methodology"
VERSION = "2"

REFS = (
    "2016ApJ...819..127Z",      # Zeng+ 2016 — PREM 을 BM2 로 적합한 핵·하부맨틀 EOS
    "2007ApJ...669.1279S",      # Seager+ 2007 — 구조 방정식과 enstatite·얼음VII EOS
    "2006JPCRD..35.1021F",      # Feistel & Wagner 2006 (IAPWS-06) — 얼음 Ih
    "2020JGRE..12506176J",      # Journaux+ 2020 (SeaFreeze) — 얼음 III·V·VI
    "2011JPCRD..40d3103W",      # Wagner+ 2011 / IAPWS R14-08(2011) — 물의 융해곡선
    "2019Icar..326...10B",      # Bierson+ 2019 — 압력이 공극을 닫는 관계와 그 계수
    "2012P&SS...73...98C",      # Carry 2012 — 10 MPa 파쇄 문턱, 관측된 전이질량
    "2022arXiv220210046H",      # Helled+ 2022 — n=1 폴리트로프와 그 계수
    "1999P&SS...47.1183G",      # Guillot 1999 — 목성·토성의 중원소 질량
    "2021ApJ...910...38N",      # Neuenschwander+ 2021 — 목성 NMoI 앵커
    "2008A&A...482..315B",      # Baraffe+ 2008 §3.3 — 부피 가법 혼합의 형태
    "2007PhRvB..75b4206V",      # Vorberger+ 2007 — 그 혼합의 정량적 유효 한계
    "1981PEPI...25..297D",      # PREM — 앵커로 쓰는 지구 C/MR²
)

G = 6.67430e-11
EARTH_MASS_KG = 5.972e24
EARTH_RADIUS_M = 6.371e6

# 조성 이름 → (핵질량분율, 얼음질량분율, 가스질량분율, 핵 재료).
# 숫자를 직접 주면 이건 기본값일 뿐이다.
#
# `iron` 만 순철(fe_eps)을 쓴다. 그 곡선의 용도가 "이보다 밀할 수 없다" 는 한계선을
# 긋는 것이라서, 가벼운 원소가 섞인 PREM 핵이 아니라 실험실 순철이어야 한다.
#
# `gas_giant` 의 가스질량분율 0.90 은 목성의 값이다. Guillot 1999 (arXiv:astro-ph/9907402)
# 이 목성의 중원소 총량(핵 포함)을 11–42 M⊕ 로, 토성을 19–31 M⊕ 로 제약한다. 목성
# 317.83 M⊕ 의 중간값 26.5 M⊕ 는 8.3 % 이므로 가스 91.7 % 인데, 프리셋은 그 구간의
# 중앙 근처인 0.90 으로 둔다. **프리셋은 기본값일 뿐이고 천체마다 넘겨주는 것이 정상이다** —
# 토성은 같은 논문의 25 M⊕ / 95.16 M⊕ = 26 % 가 되어 가스 0.74 다.
COMPOSITIONS: dict[str, tuple[float, float, float, str]] = {
    "iron":       (1.000, 0.00, 0.00, "fe_eps"),
    "earth_like": (0.325, 0.00, 0.00, "fe_prem"),
    "silicate":   (0.000, 0.00, 0.00, "fe_prem"),
    "water":      (0.163, 0.50, 0.00, "fe_prem"),
    "gas_giant":  (0.000, 0.00, 0.90, "fe_prem"),
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
                 "p_cmb", "p_ice_base", "phases", "v_pore", "m_above_lab",
                 "p_silicate_max", "t_center", "t_cmb", "t_surface", "ice_samples")

    def __init__(self, radius_m, mass_kg, moi, core_radius_m, p_center,
                 p_cmb, p_ice_base, phases, v_pore=0.0, m_above_lab=0.0,
                 p_silicate_max=0.0, t_center=0.0, t_cmb=0.0, t_surface=0.0,
                 ice_samples=()):
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
        # 규산염을 들고 있는 층이 받는 가장 높은 압력 [Pa]. 압력은 바깥으로 갈수록
        # 낮아지므로, 규산염이 처음 나타나는 자리의 압력이 곧 최대다. 이 값 하나로
        # "3.5 TPa 위의 외삽 구간을 실제로 밟았는가" 를 판정한다.
        self.p_silicate_max = p_silicate_max
        # 온도 [K]. 0 은 "선언되지 않았다" 는 뜻이지 0 K 가 아니다.
        self.t_center = t_center
        self.t_cmb = t_cmb
        self.t_surface = t_surface
        # 얼음 기둥을 지나며 찍은 (압력, 온도) 표본. 녹는곡선에 대는 것은 적분이 끝난
        # 뒤이고, 사격이 반복될 때마다 뒤집기를 돌리지 않으려고 그렇게 나눴다.
        self.ice_samples = tuple(ice_samples)

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


def _stack(cmf: float, imf: float, core_material: str, gmf: float = 0.0,
           envelope_z: float = 0.0, differentiated: bool = True):
    """바깥으로 가는 층의 열. (누적질량분율 상한, 재료) 로 준다.

    가스 외피가 있으면 그것이 가장 바깥 층이다. 폴리트로프는 **별도의 가지가 아니라
    상태방정식의 한 형태** 이므로, 층 하나가 늘 뿐 적분기는 그대로다.

    층에 들어가는 것이 순수 재료인지 혼합인지는 적분기가 묻지 않는다. 여기서 두 자리가
    혼합을 쓴다 — 미분화 천체의 암석+금속 한 층, 그리고 중원소가 녹은 가스 외피."""
    out = []
    if not differentiated:
        # 금속이 가라앉지 않았다. 핵과 맨틀이 아니라 **섞인 한 층** 이다.
        rock_metal = mix("rock_metal", "미분화 암석+금속",
                         (MATERIALS[core_material], cmf),
                         (MATERIALS["silicate"], 1.0 - cmf))
        out.append((1.0, rock_metal))
        return out
    if cmf > 0:
        out.append((cmf, MATERIALS[core_material]))
    if 1.0 - cmf - imf - gmf > 0:
        out.append((1.0 - imf - gmf, MATERIALS["silicate"]))
    if imf > 0:
        out.append((1.0 - gmf, MATERIALS["h2o"]))
    if gmf > 0:
        # 외피에 중원소가 녹아 있으면 그 층이 혼합이다. envelope_z 는 **행성 전체가
        # 아니라 이 외피 안에서의** 질량분율이다.
        out.append((1.0, mix("h_he_z", "중원소 섞인 수소-헬륨 외피",
                             (MATERIALS["h_he"], 1.0 - envelope_z),
                             (MATERIALS[ENVELOPE_Z_MATERIAL], envelope_z))))
    return out


# 단열 기울기를 한 단계에 한 번만 다시 잰다. 적분기가 이미 한 단계 안에서 재료를
# 고정하고 있고(경계에서 dr/R ~ 3e-4 의 오차), 온도 기울기는 그보다 매끄럽다.
# 단계마다 RK 네 자리에서 다시 재면 밀도 뒤집기가 여덟 번 더 돌아 비싸다.
def _cold_phases(cmf, imf, core_material, gmf, envelope_z, differentiated):
    """이 천체의 층들 중 발표된 열 상수가 없어 등온으로 남는 상들의 이름."""
    out: list[str] = []
    for _hi, mat in _stack(cmf, imf, core_material, gmf, envelope_z, differentiated):
        out.extend(mat.cold_phases())
    return out


def _adiabatic_dtdp(mat, p: float, rho: float, t: float, t_pot: float) -> float:
    """단열 기울기 dT/dP = γ T / K_S [K/Pa].

    **열 상수가 없는 층에서는 0 이다.** 그러면 그 층을 지나는 동안 온도가 변하지
    않고, 그 사실이 결과의 note 에 이름과 함께 적힌다 — 기울기를 지어내지 않는다.

    K_S = K_T (1 + αγT) 이고 αK_T 는 이미 재료가 들고 있으므로 새 상수가 없다.
    K_T 는 냉각 곡선의 수치 미분으로 잰다."""
    gamma = mat.gruneisen(p, rho, t, t_pot)
    if gamma <= 0.0 or t <= 0.0:
        return 0.0
    h = p * 1e-4
    d_hi, d_lo = mat.density(p + h, t, t_pot), mat.density(p - h, t, t_pot)
    if d_hi <= d_lo:
        return 0.0
    k_t = rho * 2.0 * h / (d_hi - d_lo)
    # αK_T·γ·T = K_T·αγT 이므로 K_S 가 새 상수 없이 닫힌다.
    ph = mat.phase_at(p) if hasattr(mat, "phase_at") else None
    k_s = k_t + (ph.dpdt_v(t, t_pot) * gamma * t if ph is not None else 0.0)
    return gamma * t / max(k_s, 1.0)


def _carries_silicate(mat) -> bool:
    """이 층 재료가 규산염을 들고 있는가. 혼합이면 성분 중에 있는지를 본다."""
    if mat.name == "silicate":
        return True
    return any(m.name == "silicate" for m, w in getattr(mat, "parts", ()) if w > 0.0)


def integrate(p_center: float, mass_kg: float, cmf: float, imf: float,
              core_material: str, phi0: float = 0.0,
              p_cap: float | None = None, gmf: float = 0.0,
              envelope_z: float = 0.0, differentiated: bool = True,
              t_center: float = 0.0, t_pot: float = 0.0) -> Structure:
    """중심압 하나에서 바깥으로 적분한다. 표면(P=0)에서 멈춘다.

    층 경계는 **목표 질량** 의 누적 분율로 잡는다. 사격이 수렴하면 겉질량이 목표와
    같으므로 이 선택은 수렴점에서 정확하고, 반복마다 경계가 흔들리지 않아 이분법이
    단조를 유지한다.

    `phi0` 가 0 보다 크면 각 자리의 고체 밀도에 (1 − φ(P)) 를 곱한다. φ 는 **국소
    압력의 함수** 이므로 자유 매개변수가 아니다 — porosity.py 를 보라. φ₀ 자체는
    강착과 가열이 정하고 이 레시피에 그 둘이 없어서 선언으로 들어온다."""
    stack = _stack(cmf, imf, core_material, gmf, envelope_z, differentiated)
    mat = stack[0][1]

    # 온도가 선언되지 않으면 t_center 가 0 이고, 아래 모든 density 호출이 예전과
    # 같은 인자로 떨어진다 — 비트까지 같은 경로다.
    t = t_center
    rho_c = mat.density(p_center, t, t_pot) * bulk_factor(mat.name, p_center, phi0, p_cap)
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
    p_si_max = p if _carries_silicate(mat) else 0.0
    t_cmb = None
    t_surface = t
    ice_samples: list[tuple[float, float]] = []
    ICE_SAMPLE_EVERY = 20

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
                core_radius, p_cmb, t_cmb = r, p, t
            if stack[layer][1].name == "h2o":
                p_ice_base = p
        if mat.name not in phases:
            phases.append(mat.name)
        if mat.name == "h2o" and (not ice_samples
                                  or steps % ICE_SAMPLE_EVERY == 0):
            ice_samples.append((p, t))
        if p_si_max == 0.0 and _carries_silicate(mat):
            p_si_max = p

        # 4차 Runge-Kutta. 한 단계 안에서는 재료를 고정한다 — 경계에서 한 단계
        # 어긋나는 오차는 dr/R ~ 3e-4 이라 C/MR² 의 유효숫자 밖이다.
        # 이 단계의 단열 기울기. 한 단계에 한 번만 잰다 (위 _adiabatic_dtdp 주석).
        dtdp = _adiabatic_dtdp(mat, p, mat.density(p, t, t_pot), t, t_pot) if t > 0.0 else 0.0

        def deriv(rr, mm, pp):
            if rr <= 0.0:
                return 0.0, 0.0, 0.0, 0.0
            rr_rho = mat.density(pp, t, t_pot) if pp > 0.0 else mat.rho0
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
            t += dtdp * dp * frac
            p = 0.0
            t_surface = t
            break

        if p > P_LAB_MAX:
            m_above_lab += dm
        r += dr
        m += dm
        p += dp
        moi += di
        v_pore += dv
        # 온도는 압력을 따라간다 — dT = (dT/dP) dP. 열 상수가 없는 층에서는
        # dtdp 가 0 이라 온도가 그 층을 그대로 통과한다.
        t += dtdp * dp
        t_surface = t

    if steps >= MAX_STEPS:
        raise ValueError(f"{MAX_STEPS} 단계 안에 표면에 닿지 못했다 "
                         f"(중심압 {p_center / 1e9:.3g} GPa)")

    if core_radius is None:
        core_radius = r      # 핵만 있는 천체
        p_cmb = p
        t_cmb = t
    if ice_samples and mat.name == "h2o":
        # 기둥 꼭대기. 얼음 III·V·VI 구간에서는 녹는곡선이 단열선보다 가파르므로
        # T − T_melt 가 제일 큰 자리가 여기다. 가스 외피가 있으면 마지막 층이 얼음이
        # 아니라서 이 표본을 넣지 않는다 — 다른 층의 점을 얼음이라고 부르지 않는다.
        ice_samples.append((p, t))
    return Structure(r, m, moi, core_radius, p_center, p_cmb, p_ice_base, phases,
                     v_pore=v_pore, m_above_lab=m_above_lab,
                     p_silicate_max=p_si_max, t_center=t_center,
                     t_cmb=t_cmb if t_cmb is not None else 0.0,
                     t_surface=t_surface, ice_samples=ice_samples)


def porosity_at(mat, p_pa: float, phi0: float,
                p_cap: float | None = None) -> float:
    """이 재료가 이 압력에서 들고 있는 공극률. 법칙이 없는 재료는 0."""
    if phi0 <= 0.0:
        return 0.0
    return 1.0 - bulk_factor(mat.name, max(p_pa, 0.0), phi0, p_cap)


# 좁히기의 상한과 멈춤 조건. 적분 한 번이 비싸므로 둘 다 필요하다.
#
# 답을 담은 시험압을 만나면 즉시 멈추므로 **풀리는 천체는 서너 번** 이면 끝난다.
# 비싼 것은 거절하는 쪽이다 — 담는 압력이 아예 없으므로 그 조건이 안 걸린다. 그래서
# 깨지기 시작하는 압력을 얼마나 정밀하게 찾을지를 따로 정해야 하고, 그 정밀도는
# 거절 메시지가 인용할 압력의 자릿수만 있으면 된다. 1 % 면 충분하다.
NARROW_ITERS = 24            # 안전 상한. 보통 그 전에 아래 조건이 먼저 걸린다
NARROW_RATIO = 1.01          # bad/good 가 이보다 가까우면 멈춘다


def _narrow_bracket(good: float, bad: float, at, mass_kg: float):
    """적분이 되는 `good` 과 바깥 층이 깨지는 `bad` 사이에서 괄호의 위쪽을 찾는다.

    바깥 층의 바닥은 중심압에 단조증가하므로 이 구간에 "깨지기 시작하는 압력" 이
    하나 있고, 답이 있다면 그 아래다. 목표 질량을 담는 시험압을 만나는 즉시 멈춘다 —
    그 아래를 더 재는 것은 이 함수의 일이 아니라 뒤따르는 할선법의 일이다.

    돌려주는 것은 (압력, 그 압력의 구조) 이고, 구조의 겉질량이 목표에 못 미치면
    호출자가 그것을 진짜 거절의 근거로 쓴다."""
    best_p, best_st = good, at(good)
    for _ in range(NARROW_ITERS):
        if bad / good < NARROW_RATIO:
            break                        # 깨지는 자리를 충분히 좁혔다
        mid = math.sqrt(good * bad)      # 로그 중점. 압력이 자릿수로 움직인다
        try:
            st = at(mid)
        except PhaseGap:
            bad = mid
            continue
        good, best_p, best_st = mid, mid, st
        if st.mass_kg >= mass_kg:
            break                        # 괄호가 잡혔다. 정밀도는 할선법의 일이다
    return best_p, best_st


def _shoot_pressure(mass_kg: float, cmf: float, imf: float,
                    core_material: str, phi0: float = 0.0,
                    p_cap: float | None = None, gmf: float = 0.0,
                    envelope_z: float = 0.0, differentiated: bool = True,
                    t_center: float = 0.0,
                    t_pot: float = 0.0) -> tuple[Structure, bool]:
    """겉질량이 목표와 맞는 중심압을 찾는다. 질량은 중심압에 단조증가한다.

    수렴 여부를 값과 함께 돌려준다 — 못 맞춘 것은 예외가 아니라 `converged=False`
    를 단 결과다. 예외로 던지면 호출자가 그 사실을 조용히 삼킬 수 있다."""
    # 비압축 반지름에서 중심압을 어림해 괄호를 잡는다. 재료의 유효 상한을 넘겨서
    # 잡으면 상 구간 밖이라 PhaseGap 이 나므로, 위쪽은 그 상한에서 멈춘다.
    stack = _stack(cmf, imf, core_material, gmf, envelope_z, differentiated)
    # 괄호잡기용 평균밀도. 폴리트로프는 영압 밀도가 0 이라 `rho_seed` 가 n=1 해의
    # 평균밀도로 갈아 준다 — 계산 결과에는 들어가지 않고 첫 추측에만 쓰인다.
    rho0_bar = 1.0 / sum(
        (hi_f - (stack[i - 1][0] if i else 0.0))
        / (mat.rho_seed(mass_kg) * bulk_factor(mat.name, 0.0, phi0, p_cap))
        for i, (hi_f, mat) in enumerate(stack))
    r0 = (3.0 * mass_kg / (4.0 * math.pi * rho0_bar)) ** (1.0 / 3.0)
    # 중심압은 가장 안쪽 재료가 받는다. 바깥 층의 상한은 적분 중에 PhaseGap 이
    # 스스로 잡으므로 여기서 겹쳐 걸면 엉뚱한 층 때문에 거절하게 된다.
    p_ceiling = stack[0][1].p_max
    lo = 1.0e2
    hi = min(3.0 * G / (8.0 * math.pi) * mass_kg ** 2 / r0 ** 4 * 4.0, p_ceiling)

    def at(p: float):
        return integrate(p, mass_kg, cmf, imf, core_material, phi0, p_cap, gmf,
                         envelope_z, differentiated, t_center, t_pot)

    # 괄호잡기. 시험압을 네 배씩 올리며 겉질량이 목표에 닿는 자리를 찾는다.
    #
    # **바깥 층이 시험압에서 깨지는 것은 거절이 아니다.** 중심압을 올리면 프로파일
    # 전체가 올라가므로 바깥 층의 바닥도 같이 오른다. 그러니 어떤 시험압에서 그 층이
    # 근거 구간을 벗어났다는 것은 **답이 그 아래에 있다** 는 뜻이지, 이 천체가 안
    # 풀린다는 뜻이 아니다. 그런데도 PhaseGap 을 그대로 올려 보내면 버려질 시험값이
    # 물리인 척하고 나간다 — 6.84 M⊕ (2026-08-26, 규산염) 와 5.884 M⊕ (2026-08-27,
    # 물) 가 그렇게 나온 수였고 둘 다 물리로 읽혔다. 그래서 여기서는 좁힌다.
    #
    # 좁혀도 목표 질량에 못 닿으면 **그때가 진짜 거절** 이고, 그 거절은 좁혀서 얻은
    # 상태를 근거로 말한다. 버린 시험값을 인용하지 않는다.
    good = None                  # 마지막으로 적분이 끝난 시험압
    broke: PhaseGap | None = None
    while True:
        try:
            st = at(hi)
        except PhaseGap as gap:
            if good is None:
                raise            # 첫 시험부터 깨진다. 좁힐 바닥이 없다
            broke = gap
            hi, st = _narrow_bracket(good, hi, at, mass_kg)
            break
        good = hi
        if st.mass_kg >= mass_kg:
            break
        if hi >= p_ceiling:
            raise ValueError(
                f"이 질량을 담으려면 중심압이 {_ceiling_owner(stack[0][1])} 의 근거 "
                f"구간 상한({p_ceiling / 1e9:.0f} GPa) 을 넘어야 한다. "
                + _ceiling_why(stack[0][1]))
        hi = min(hi * 4.0, p_ceiling)

    if st.mass_kg < mass_kg:
        # 좁힌 위쪽 끝에서도 질량이 모자란다. 중심압을 더 올려야 하는데 그러면 바깥
        # 층이 깨지므로, 이건 실재하는 거절이다. 이유는 **바깥 층** 이지 안쪽 재료의
        # 상한이 아니다.
        raise ValueError(
            f"이 질량을 담으려면 중심압을 {hi / 1e9:.0f} GPa 위로 올려야 하는데, "
            f"그러면 바깥의 {broke.material} 층이 근거 구간을 벗어난다 "
            f"(그 층 바닥이 {broke.pressure_pa / 1e9:.0f} GPa). {broke.reason}")
    # log M 은 log P_c 에 거의 선형이라 할선법이 몇 번 만에 붙는다. 벗어나면
    # 괄호 안의 로그 이분법으로 되돌린다 — 적분 한 번이 비싸서 반복 횟수가 곧 비용이다.
    st = integrate(hi, mass_kg, cmf, imf, core_material, phi0, p_cap, gmf,
                        envelope_z, differentiated, t_center, t_pot)
    if abs(st.mass_kg - mass_kg) / mass_kg < SHOOT_TOL:
        return st, True
    x0, y0 = math.log(hi), math.log(st.mass_kg / mass_kg)
    x1 = math.log(max(lo, hi * 1e-3))
    st = integrate(math.exp(x1), mass_kg, cmf, imf, core_material, phi0, p_cap,
                    gmf, envelope_z, differentiated, t_center, t_pot)
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
        st = integrate(math.exp(x1), mass_kg, cmf, imf, core_material, phi0, p_cap,
                    gmf, envelope_z, differentiated, t_center, t_pot)
        y1 = math.log(st.mass_kg / mass_kg)
    return st, False


# 온도를 맞추는 바깥 고리의 횟수와 허용오차. 단열선이 앵커에 거의 선형이라
# 두세 번이면 붙는다 — 밀도가 온도에 몇 % 만 반응하기 때문이다.
T_PASSES = 6
T_TOL = 1e-6


def shoot(mass_kg: float, cmf: float, imf: float,
          core_material: str, phi0: float = 0.0,
          p_cap: float | None = None, gmf: float = 0.0,
          envelope_z: float = 0.0, differentiated: bool = True,
          potential_temperature: float | None = None) -> tuple[Structure, bool]:
    """겉질량과 **표면 온도** 를 동시에 맞춘다.

    온도가 선언되지 않으면(`potential_temperature is None`) 아래 고리가 아예 돌지
    않고 예전 경로 그대로다 — 비트까지 같다.

    선언되면 경계조건이 하나 더 붙는다. 적분은 중심에서 바깥으로 가는데 온도의
    경계조건은 **표면** 에 있으므로(Unterborn+ 2019 §2 의 T(R) = T_Pot), 중심 온도를
    미지수로 두고 표면 온도가 맞을 때까지 좁힌다. 사격을 두 개 겹치는 대신 단열선이
    앵커에 거의 선형이라는 것을 쓴다 — 중심 온도를 비율로 다시 재면 몇 번 만에 붙고,
    밀도가 온도에 되먹임하는 몫만 반복이 흡수한다."""
    args = (mass_kg, cmf, imf, core_material, phi0, p_cap, gmf, envelope_z,
            differentiated)
    if not potential_temperature:
        return _shoot_pressure(*args)
    t_pot = float(potential_temperature)
    t_c = t_pot * 2.0        # 첫 추측. 비율로 다시 재므로 값 자체는 중요하지 않다
    st, converged = _shoot_pressure(*args, t_center=t_c, t_pot=t_pot)
    for _ in range(T_PASSES):
        if st.t_surface <= 0.0:
            break            # 열 상수가 없는 재료뿐이다. 온도가 흐르지 않는다
        nxt = t_c * t_pot / st.t_surface
        done = abs(nxt / t_c - 1.0) < T_TOL
        t_c = nxt
        st, converged = _shoot_pressure(*args, t_center=t_c, t_pot=t_pot)
        if done:
            break
    return st, converged


def _ceiling_owner(mat) -> str:
    """상한을 정한 것이 누구인가. 혼합이면 **가장 낮은 성분** 이 정한다."""
    parts = getattr(mat, "parts", None)
    if not parts:
        return mat.name
    limiting = min(parts, key=lambda pw: pw[0].p_max)[0]
    return f"{mat.name} 안의 {limiting.name}"


def _ceiling_why(mat) -> str:
    """그 상한 위가 무엇인지. 순수 재료와 혼합이 다른 답을 준다.

    순수 재료가 상한에 닿는 것은 전자축퇴 영역에 들어간다는 뜻이었다. 혼합에서는
    그렇지 않다 — 무거운 성분 하나의 적합이 끝났을 뿐이고, 나머지 성분은 멀쩡하다.
    두 경우에 같은 문장을 돌려주면 거절 이유가 거짓이 된다."""
    parts = getattr(mat, "parts", None)
    if not parts:
        return ("그 위는 전자축퇴가 지배하는 영역이고 (Thomas-Fermi-Dirac), 이 "
                "레시피에는 그 상태방정식이 없다 — Seager+ 2007 §III.2 가 그 자리를 "
                "채우는 방법을 적어두었다.")
    limiting = min(parts, key=lambda pw: pw[0].p_max)[0]
    return (f"섞인 층이라 전자축퇴 이야기가 아니다 — 성분 하나('{limiting.name}')의 "
            "적합이 거기서 끝날 뿐이고 나머지 성분은 멀쩡하다. 이 압력의 혼합 밀도에 "
            "근거가 없어서 멈추는 것이고, 그 성분을 더 높은 압력까지 적합한 상태방정식이 "
            "들어오면 이 천체는 풀린다.")


# 고체 표면이 없는 천체. 여기 있는 상태방정식은 전부 응축상이라 H/He 외피에는
# 쓸 수 없다 — 그쪽은 폴리트로프이고 다른 문헌이다.
# 수소-헬륨 외피가 있는 천체. 폴리트로프가 들어온 뒤로 이 둘은 **거절하지 않는다** —
# 가스질량분율을 주면 같은 적분기가 푼다.
GAS_GIANT_CLASSES = ("giant", "gas_giant")

# ── 거대행성 갈래의 검증 범위 ────────────────────────────────────────────
#
# n = 1 폴리트로프에는 **천체가 돌릴 손잡이가 없다.** K 가 상수 하나이고 R = √(πK/2G)
# 라서 질량도 조성도 반지름에 안 들어간다 — 어떤 거대행성에도 같은 반지름과 같은
# C/MR² 를 돌려준다. 그래서 "Jupiter 0.6 %, Saturn 20.7 %" 는 오차 두 개가 아니라
# **출력 하나를 두 행성에 대본 것** 이다.
#
# 그러면 이 갈래의 신뢰도는 계산이 아니라 **어디서 시험됐는가** 가 정한다. 시험된 곳은
# 딱 둘이고, 사이는 한 번도 확인된 적이 없다. 둘 사이에 문턱을 지어내지 않는 이유가
# 그것이다 — 지어낸 수는 근거가 아니라 장식이다.
#
# Saturn 이 왜 틀리는지는 Helled+ 2022 §2 가 적는다. P ∝ ρ² 가 토성 외피에 덜 맞고,
# 토성이 중원소가 더 많다 (Guillot 1999: 목성 총중원소 3–13 %, 토성 20–33 %). 둘 다
# 질량 자체의 이야기가 아니므로, 아래 두 상수는 **기작의 문턱이 아니라 시험의 좌표** 다.
# 거대행성 외피의 중원소를 어느 재료가 나르는가. **이 파일의 셋 중 옳은 것이 없고,
# 각자 다르게 틀린다** — 고른 이유가 아니라 고를 수 있는 것이 없다는 사실이 내용이다.
#
#   h2o       조성은 제일 맞다 (Guillot 의 Z 는 얼음이 주다). 상한 37.4 GPa 이라
#             거대행성 외피가 첫 몇 % 에서 지나쳐 버린다. 못 쓴다.
#   silicate  그럴듯한 중간. 상한 3.5 TPa 이라 토성 중심(709 GPa)은 덮고 목성 중심
#             (~4.4 TPa)은 못 덮는다. **이걸 쓴다.**
#   fe_prem   상한 12 TPa 로 둘 다 덮지만 철은 Z 의 무거운 끝이지 중간이 아니다.
#             이걸 골랐으면 목성이 돌았을 것이고, 그래서 안 골랐다 — 상한은 실재하는
#             한계이고 그것을 가리려고 재료를 고르는 것은 답을 고르는 것이다.
#             그쪽 수치는 test_giant.py 가 재서 기록에 남긴다.
ENVELOPE_Z_MATERIAL = "silicate"

GIANT_ANCHOR_PASS_ME = 317.8    # Jupiter. 평균반지름 대비 +0.6 % — 이 갈래가 맞은 유일한 곳
GIANT_ANCHOR_FAIL_ME = 95.2     # Saturn. +20.7 % — 이 갈래가 틀린 유일한 곳

# ── 규산염의 외삽 구간 ───────────────────────────────────────────────────
#
# 3.5 TPa 아래의 규산염은 **측정된 행성의 적합** 이다 — PREM 은 지진파에서 나온 지구의
# 밀도 분포다. 그 위는 다르다. Seager+ 2007 의 BME4 는 150 GPa 까지의 DFT 계산
# (Karki+ 2000) 을 90배 위로 끌고 간 것이고, 그 사이에서 MgSiO₃ 는 실제로 세 번
# 해리해 MgO + SiO₂ 가 된다 (Umemoto+ 2017: 0.75 · 1.31 · 3.10 TPa). 그 해리를
# 무시해도 되는 근거는 결정구조가 같다는 것이 아니라 **그 압력대에서 조성이 밀도를
# 거의 정하지 않는다** 는 것이다 (Zeng+ 2016 §II: MgO·SiO₂·MgSiO₃·Mg₂SiO₄ 의 TFD 가
# A=20, Z=10 로 거의 같다).
#
# 그건 근거이긴 하지만 측정이 아니다. 그래서 해가 이 구간을 실제로 밟으면 등급이
# 내려가고, note 가 왜인지를 적는다. 얼마나 맞는가가 아니라 **무엇에 기대는가** 를
# 등급이 말한다는 이 파일의 규율 그대로다.
SILICATE_EXTRAPOLATED_MIN = SILICATE_PREM_TO_PV

# 온도 갈래가 발표된 값과 대조된 반지름 상한. Unterborn+ 2019 eq. 7 의 적합이
# 0.75 ~ 1.5 R⊕ 이고, 그 안에서도 위쪽 절반은 우리 단열선이 낮게 흐른다 (1.0 에서
# 4.4 %, 1.46 에서 17 %). 그래서 "대조됐다" 고 말할 수 있는 자리를 좁게 잡는다.
UNTERBORN_TCMB_MAX_R = 1.05

# ── 따뜻한 얼음 창 ───────────────────────────────────────────────────────
#
# 2026-08-27 까지 이 자리에 거절이 하나 있었다 — 얼음 기둥 바닥이 209.5 MPa 과 2.216 GPa
# 사이이고 천체가 녹을 만큼 따뜻하면 "여기서 판정하지 않는다. 같은 압력이 액체 물도 담고,
# 고르려면 이 레시피가 들고 있지 않은 열 프로파일이 필요하다" 였다. 프로파일이 생겼고
# (2026-08-27 의 온도) 녹는곡선이 생겼으므로(IAPWS R14-08) 그 사유가 만료됐다.
#
# **판정만 하고 밀도는 손대지 않는다.** 액체 물은 얼음보다 밀도가 다르고, 그것까지 모형에
# 넣으려면 재료마다 액체 상태방정식이 하나씩 더 있어야 하고 적분기 안에 상분율이 들어와야
# 한다 — 이번 범위보다 크다. 그래서 녹았다고 판정된 해의 반지름과 C/MR² 는 **고체상의 답**
# 이고, 그렇게 적는다. 명시하지 않는 것이 결함이지 판정만 내는 것이 결함은 아니다.
#
# 표본은 기둥 바닥·중간·꼭대기다. 얼음 III·V·VI 구간에서 녹는곡선(약 52 K/GPa)이
# 단열선(약 21 K/GPa)보다 가파르므로 T − T_melt 의 최대는 기둥 **꼭대기** 에 있고,
# 얼음 Ih 은 녹는곡선이 내려가므로 반대로 바닥에 있다. 양쪽을 다 찍는다.
ICE_STATE_NONE = "none"
ICE_STATE_SOLID = "solid"
ICE_STATE_MOLTEN = "molten"
ICE_STATE_UNDECIDED = "undecided"


def _ice_verdict(st, potential_temperature) -> tuple[str, str]:
    """얼음 기둥이 녹았는가. (상태, 한 줄 설명) 을 돌려준다."""
    if not st.ice_samples:
        return ICE_STATE_NONE, ""
    if not potential_temperature:
        return (ICE_STATE_UNDECIDED,
                "**얼음 기둥의 고체·액체를 판정하지 않았다** — 포텐셜 온도가 선언되지 "
                "않아 이 해에는 온도가 흐르지 않는다. 녹는곡선은 있고(IAPWS R14-08(2011)) "
                "압력도 있으니, 온도를 선언하면 이 행은 판정으로 바뀐다.")
    ice = MATERIALS["h2o"]
    best_margin = None
    best = None
    unseen = 0.0        # 녹는곡선 밖으로 나간 표본의 가장 낮은 압력
    for p_pa, t_k in st.ice_samples:
        if p_pa <= 0.0 or t_k <= 0.0:
            continue
        t_m = ice.t_melt(p_pa)
        if t_m is None:
            # 녹는곡선이 여기까지 안 온다. IAPWS 식 (5) 가 715 K 에서 끝나고 그건
            # 20.6 GPa 라 얼음 VII 구간 안이다. **못 본 것을 안 본 척하지 않는다.**
            unseen = p_pa if unseen == 0.0 else min(unseen, p_pa)
            continue
        margin = t_k - t_m
        if best_margin is None or margin > best_margin:
            best_margin, best = margin, (p_pa, t_k, t_m)
    blind = ("" if unseen == 0.0 else
             f" 기둥의 {unseen / 1e9:.1f} GPa 아래쪽만 판정했다 — 그 위는 녹는곡선이 "
             "닿지 않는다. IAPWS 식 (5) 가 715 K 에서 끝나고 그게 20.6 GPa 다.")
    if best_margin is None:
        return (ICE_STATE_UNDECIDED,
                "**얼음 기둥의 고체·액체를 판정하지 않았다** — 기둥 전체가 이 레시피가 "
                "들고 있는 녹는곡선(IAPWS R14-08(2011)) 의 압력 구간 위다. 그 위의 곡선을 "
                "고르는 것은 별건이고, 후보와 기각 이유는 engine/ice-x-context-notes.md 에 "
                "적어 두었다.")
    p_pa, t_k, t_m = best
    where = f"{p_pa / 1e6:.1f} MPa 에서 T {t_k:.1f} K · 녹는점 {t_m:.1f} K"
    if best_margin > 0.0:
        return (ICE_STATE_MOLTEN,
                f"**얼음 기둥이 녹는다** — {where} 로 {best_margin:+.1f} K 다 "
                f"(IAPWS R14-08(2011), 이 구간 불확도 3 %). **밀도는 손대지 않았다**: "
                "이 레시피에 액체 물의 상태방정식이 없어서, 여기 나온 반지름과 C/MR² 는 "
                "고체상의 답이다. 판정만 읽고 밀도는 읽지 말 것." + blind)
    if unseen != 0.0:
        # 본 자리는 전부 고체인데 못 본 자리가 있다. **'고체' 라고 말하면 안 된다** —
        # 하한이 한쪽만 묶는 것과 같은 규율이고, core_state 가 같은 규칙을 쓴다.
        return (ICE_STATE_UNDECIDED,
                f"**얼음 기둥의 고체·액체를 판정하지 않았다.** 본 자리는 전부 고체다 — "
                f"제일 녹기 쉬운 자리가 {where} 로 {best_margin:+.1f} K 다. 그런데 기둥의 "
                f"{unseen / 1e9:.1f} GPa 위쪽은 녹는곡선이 닿지 않아 보지 못했고, 못 본 "
                "구간이 있으면 '고체' 는 말할 수 없다. 'molten' 은 한 자리만 넘어도 참이지만 "
                "'solid' 는 전부를 봐야 참이다.")
    return (ICE_STATE_SOLID,
            f"얼음 기둥이 고체다 — 제일 녹기 쉬운 자리가 {where} 로 {best_margin:+.1f} K "
            f"다 (IAPWS R14-08(2011), 불확도 3 %).")


# 아직 거절하는 유체 천체. 각각 무엇이 있어야 답이 바뀌는지를 거절 이유가 말한다.
FLUID_CLASSES = ("ice_giant", "sub_neptune", "brown_dwarf", "star")


def solve(mass_earth: float,
          core_mass_fraction: float | None = None,
          ice_mass_fraction: float | None = None,
          gas_mass_fraction: float | None = None,
          composition: str = "earth_like",
          radius_earth: float | None = None,
          differentiated: bool = True,
          body_class: str | None = None,
          initial_porosity: float = 0.0,
          porosity_cap: float | None = None,
          tidal_heating: bool = False,
          envelope_z: float = 0.0,
          potential_temperature: float | None = None) -> Result:
    """질량과 조성에서 층 구조를 적분한다.

    `radius_earth` 는 계산에 **쓰이지 않는다** — 반지름은 출력이다. 주면 도출값과
    대조해서, 선언한 조성이 그 천체를 재현하는지 판정하고 어긋나면 무엇이 빠졌는지
    이름을 댄다.

    `tidal_heating` 도 계산에 쓰이지 않는다. 공극이 남을 레짐인가를 판정하는 세
    지표 중 하나이고 (`porosity.voids_expected`), 다른 노드의 출력이므로 여기서는
    선언으로만 받는다.

    `potential_temperature` 는 **세 번째 선언** 이다. 대류하는 내부를 표면까지
    단열적으로 감압했을 때의 온도이고, 표면 온도가 아니다 — 그 둘 사이에는 전도하는
    뚜껑이 있고 지구에서 그 차이가 1300 K 쯤 된다. 뚜껑의 두께를 정하는 것은 열류이고,
    열류는 `internal_heat_nontidal` 의 출력이라 여기서 도출하지 않는다. 주지 않으면
    (`None`) 온도가 아예 흐르지 않고 예전 등온 경로 그대로다."""
    preset_cmf, preset_imf, preset_gmf, core_material = COMPOSITIONS.get(
        composition, (None, None, None, "fe_prem"))
    cmf = preset_cmf if core_mass_fraction is None else core_mass_fraction
    imf = preset_imf if ice_mass_fraction is None else ice_mass_fraction
    gmf = preset_gmf if gas_mass_fraction is None else gas_mass_fraction

    inputs = {"mass_earth": mass_earth, "radius_earth": radius_earth,
              "core_mass_fraction": cmf, "ice_mass_fraction": imf,
              "gas_mass_fraction": gmf,
              "composition": composition, "differentiated": differentiated,
              "body_class": body_class, "initial_porosity": initial_porosity,
              "porosity_cap": porosity_cap, "tidal_heating": tidal_heating,
              "envelope_z": envelope_z,
              "potential_temperature": potential_temperature}

    if body_class in FLUID_CLASSES:
        why = {
            "brown_dwarf": ("중수소가 탄다. 13 M_J 위는 광도가 시간에 따라 변하고 "
                            "(Spiegel+ 2011), 이 레시피에는 그 열이력이 없다 — 등온 "
                            "폴리트로프로 갈색왜성을 푸는 것은 나이를 무시하는 것이다."),
            "star": ("수소가 탄다. 별의 NMoI 는 이 레시피가 아니라 n = 3/2 폴리트로프의 "
                     "발표값 0.205 에서 오고 (Chandrasekhar 1939), 그 가지는 "
                     "body_figure 에 따로 있다."),
            "ice_giant": ("외피가 수소-헬륨이 아니라 물·암모니아·메탄이 섞인 '얼음' 이고, "
                          "그 혼합물의 상태방정식이 이 파일에 없다. n = 1 폴리트로프는 "
                          "H/He 압축성에 맞춰진 것이라 여기 쓸 수 없다.\n"
                          "**얼음 사다리로도 못 간다 — 온도가 안 맞는다.** 이 파일의 물은 "
                          f"20~{ICE_VII_X_T_MAX:.0f} K 의 응축상이고, 얼음거대행성의 얼음 "
                          "맨틀은 그 위에서 시작해 위로 간다: 깊은 내부가 100 GPa 에서 "
                          "5000~7000 K, 중심이 천왕성 5700 K · 해왕성 5500 K 다 "
                          "(Scheibe+ 2019, arXiv:1911.00447). 그래서 필요한 것은 고압 "
                          "고체 얼음이 아니라 **유체·초이온 갈래** 이고, 그건 이 레시피가 "
                          "2026-08-27 에 이름 대며 거절한 바로 그 상이다.\n"
                          "세 성분 중 옮겨 적을 형태가 있는 것은 물 하나뿐이다 — Mazevet+ "
                          "2019 (arXiv:1810.05658) 의 해석적 자유에너지 적합이고, "
                          "Scheibe+ 2019 가 천왕성·해왕성 모형을 그 위에 세운다. 암모니아"
                          "(Bethkenhagen+ 2013)와 메탄(Bethkenhagen+ 2017)은 표로만 있다. "
                          "물 하나로 얼음 전체를 대신하는 것은 이 분야의 관행이지만"
                          "(Redmer+ 2011 · Helled+ 2011 · Nettelmann+ 2013), **그 대가는 "
                          "정량돼 있지 않다.** Bethkenhagen+ 2017 의 4 % / 2.1 % 는 세 "
                          "성분의 순수 EOS 를 다 갖춘 뒤 부피 가법으로 섞는 단계의 한계이고, "
                          "물 하나로 가는 길은 그 단계를 아예 밟지 않는다. 물 EOS 와 혼합물 "
                          "EOS 의 차이는 다른 수이고 인용된 문헌 범위에서 측정되지 않았다 — "
                          "그 논문의 결론부가 세 순수 성분의 퍼텐셜 구축을 후속 과제로 꼽는 "
                          "것 자체가 물 하나로는 안 된다는 전제다. H-He 의 8 % 를 암석에 "
                          "옮겨 적지 않았던 것과 같은 규율로, 여기서도 옮겨 적지 않는다.\n"
                          "**그리고 그 상태방정식이 있어도 충분하지 않다.** Scheibe+ 2019 "
                          "가 바로 그 EOS 로 두 행성을 단열 모형으로 풀어 냉각시간을 "
                          "천왕성 5.1 Gyr · 해왕성 3.7 Gyr 로 얻었고 (실제 나이 4.56 Gyr), "
                          "결론이 \"neither planet is fully adiabatic in the deeper "
                          "interior\" 다. 둘을 가르는 것은 열경계층이고 그 크기는 열류가 "
                          "정한다 — core_state 가 핵 쪽 경계 온도를 선언으로 받는 것과 "
                          "같은 자리이고, 이 레시피에는 그 열류가 없다."),
            "sub_neptune": ("H/He 외피가 총질량의 몇 %뿐이라 두께가 조성이 아니라 "
                            "**나이와 항성 조사량** 이 정한다 (광증발). 이 레시피는 "
                            "등온이고 진화가 없으므로, 가스질량분율을 스스로 정할 수 "
                            "없다. 그 값을 넘겨주면 적분 자체는 돈다."),
        }.get(body_class, "이 클래스의 외피 상태방정식이 이 파일에 없다.")
        return out_of_domain(
            RECIPE, VERSION, f"'{body_class}' 는 아직 이 레시피 밖이다. {why}",
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

    if not differentiated and (imf > 0 or gmf > 0):
        return out_of_domain(
            RECIPE, VERSION,
            "미분화가 얼음이나 가스와 함께 선언됐다. 이 레시피가 섞는 것은 **암석과 "
            "금속** 한 쌍뿐이다 — 얼음이 암석에 섞인 천체(Callisto 형)는 부분 분화의 "
            "영역이고, 그건 완전히 섞였거나 완전히 갈렸거나가 아니라 그 사이라서 다른 "
            "문제다. 얼음질량분율과 가스질량분율을 0 으로 두면 이 천체는 풀린다.",
            inputs=inputs, refs=REFS)

    if not 0.0 <= envelope_z < 1.0:
        return out_of_domain(
            RECIPE, VERSION,
            f"외피 중원소분율 {envelope_z} 가 [0, 1) 밖이다. 0 은 '중원소가 없다' 는 "
            "주장이 아니라 '이 레시피가 판정하지 않는다' 는 뜻이다 — Z 는 강착과 "
            "진화가 정하고, 이 레시피에는 그 둘이 없다.",
            inputs=inputs, refs=REFS)

    if envelope_z > 0 and gmf <= 0:
        return out_of_domain(
            RECIPE, VERSION,
            f"외피 중원소분율 {envelope_z} 를 받았는데 가스 외피가 없다"
            f"(가스질량분율 {gmf}). envelope_z 는 **외피 안에서의** 질량분율이므로 "
            "외피가 있어야 뜻이 있다. 고체 천체에 무거운 성분을 섞으려면 "
            "differentiated=False 쪽이다.",
            inputs=inputs, refs=REFS)

    if potential_temperature is not None and potential_temperature < 0.0:
        return out_of_domain(
            RECIPE, VERSION,
            f"포텐셜 온도 {potential_temperature} K 가 음수다. 0 과 None 은 "
            "'0 K 다' 가 아니라 '이 레시피가 판정하지 않는다' 는 뜻이고 "
            "(`initial_porosity` · `envelope_z` 와 같은 규율), 그 경우 온도가 "
            "아예 흐르지 않는다. 음수는 그 어느 쪽도 아니다.",
            inputs=inputs, refs=REFS)

    if not 0.0 <= initial_porosity < 1.0:
        return out_of_domain(
            RECIPE, VERSION,
            f"초기 공극률 {initial_porosity} 가 [0, 1) 밖이다. 0 은 '공극이 없다' 는 "
            "주장이 아니라 '이 레시피가 판정하지 않는다' 는 뜻이다 — φ₀ 는 강착이 "
            "정하고 가열이 지우며, 이 레시피에는 그 둘이 없다.",
            inputs=inputs, refs=REFS)

    if (not 0.0 <= cmf <= 1.0 or not 0.0 <= imf <= 1.0
            or not 0.0 <= gmf <= 1.0 or cmf + imf + gmf > 1.0):
        return out_of_domain(
            RECIPE, VERSION,
            f"질량분율이 맞지 않는다 — 핵 {cmf}, 얼음 {imf}, 가스 {gmf}. "
            "셋 다 [0, 1] 안이고 합이 1 이하여야 한다.",
            inputs=inputs, refs=REFS)

    if gmf > 0 and body_class is not None and body_class not in GAS_GIANT_CLASSES:
        return out_of_domain(
            RECIPE, VERSION,
            f"가스질량분율 {gmf} 를 받았는데 body_class 가 '{body_class}' 다. "
            f"수소-헬륨 외피를 붙이는 것은 {' 또는 '.join(GAS_GIANT_CLASSES)} 로 "
            "선언된 천체에만 한다 — 선언과 조성이 어긋나면 조용히 엉뚱한 천체를 푼다.",
            inputs=inputs, refs=REFS)

    try:
        st, converged = shoot(mass_earth * EARTH_MASS_KG, cmf, imf, core_material,
                              initial_porosity, porosity_cap, gmf,
                              envelope_z, differentiated, potential_temperature)
    except PhaseGap as gap:
        return out_of_domain(RECIPE, VERSION, gap.reason, inputs=inputs, refs=REFS,
                             notes=(f"막힌 재료: {gap.material}, "
                                    f"압력 {gap.pressure_pa / 1e9:.4f} GPa"
                                    + (f", 온도 {gap.temperature_k:.0f} K"
                                       if gap.temperature_k else ""),))
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
    if st.t_center > 0.0:
        bounds.append(f"중심 온도 {st.t_center:.0f} K")
    notes = [f"층별 상: {' → '.join(st.phases)}. {' · '.join(bounds)}, "
             f"평균밀도 {rho_bar:.0f} kg/m³.",]
    if initial_porosity > 0:
        notes.append(_porosity_note(st, initial_porosity, mass_earth))
    ice_state, ice_note = _ice_verdict(st, potential_temperature)
    if ice_note:
        notes.append(ice_note)

    # 2026-08-26: 혼합 규칙이 들어오면서 **앵커 수가 하나에서 둘로 늘었다.** 목성이
    # Z = 0 에서 +0.6 %, 토성이 Z = 0.200 에서 −0.1 % 다. 그래서 이 강등 규칙을 다시
    # 판정했고, 판정은 이렇다.
    #
    # 지우지 않았다. n = 1 은 이제 조성에 반응하지만 **질량에는 여전히 반응하지 않는다** —
    # R = √(πK/2G) 에 M 이 없는 것은 그대로다. 그래서 두 앵커가 묶는 것은 질량 구간이
    # 아니라 조성이고, 두 앵커 사이의 200 M⊕ 천체는 두 검사점 사이를 보간하는 게 아니라
    # Z 가 시키는 값을 받을 뿐이다. 앵커 사이를 calibrated 로 올리는 안은 그래서 기각했다.
    #
    # 대신 강등 조건이 하나 늘었다 — **Z 가 선언되면 질량과 무관하게 analog** 다.
    # 토성이 맞은 것은 이 레시피가 토성을 예측해서가 아니라 논문이 준 조성을 받아썼기
    # 때문이고, 등급은 적합의 좋음이 아니라 **레시피가 검증할 수 없는 선언에 답이 기대는가**
    # 를 말해야 한다. initial_porosity 와 같은 규율이다.
    # 온도가 답에 실제로 들어갔는가. 기준 포텐셜 온도를 선언한 것은 "지구와 같은
    # 열구조" 라고 말한 것이고, 그러면 열압력이 항등적으로 0 이라 답이 안 움직인다.
    # 그 경우까지 등급을 내리면 등급이 뜻을 잃는다.
    thermal_declared = bool(potential_temperature)
    thermal_moves = (thermal_declared
                     and abs(potential_temperature - EARTH_POTENTIAL_T) > 1e-9)
    if thermal_declared:
        cold = sorted(set(_cold_phases(cmf, imf, core_material, gmf, envelope_z,
                                       differentiated)))
        notes.append(
            f"**포텐셜 온도 {potential_temperature:.0f} K 는 선언이다.** 대류하는 내부를 "
            "표면까지 단열 감압했을 때의 온도이고 표면 온도가 아니다 — 그 사이의 전도하는 "
            "뚜껑이 지구에서 1300 K 쯤 되고, 그 두께를 정하는 것은 열류다. 열류는 "
            "`internal_heat_nontidal` 의 출력이라 이 레시피가 도출하지 않는다. "
            f"기준은 {EARTH_POTENTIAL_T:.0f} K 이고 (Unterborn+ 2019 §2 의 지구형 맨틀 "
            "포텐셜 온도), 암석-금속 상들의 적합 기준이 그 단열선이라 거기서는 열압력이 "
            "정확히 0 이다. 지구가 안 움직이는 이유가 그것이고, 허용오차가 아니라 항등식이다."
            + (f" 열 상수가 없어 등온으로 남는 상: {', '.join(cold)}." if cold else ""))
    thermal_unchecked = thermal_declared and radius > UNTERBORN_TCMB_MAX_R
    if thermal_unchecked:
        notes.append(
            f"**반지름 {radius:.2f} R⊕ 는 온도 갈래가 대조된 구간 밖이다.** 단열선의 "
            f"판정선은 Unterborn+ 2019 eq. 7 이고 그 적합이 "
            f"{UNTERBORN_TCMB_MAX_R:.2f} R⊕ 까지다. 그 위에서 여기 단열선이 그들 값보다 "
            "낮게 흐르고, 1.46 R⊕ 에서 17 % 다 — αK_T 를 부피에 무관하다고 둔 Anderson & "
            "Goto 근사가 압축이 커지면 γ 를 1/ρ 로 떨어뜨리는데, Debye 모형으로 α(P,T) 와 "
            "C_P(P,T) 를 푸는 쪽은 그렇게 빨리 떨어지지 않는다. 밀도가 안 움직였더라도 "
            "**핵 온도가 대조 밖** 이므로 등급을 analog 로 내린다 — 그 값을 받는 쪽이 "
            "core_state 다.")
    if thermal_moves:
        notes.append(
            f"답이 그 선언에 기댄다 — 기준 {EARTH_POTENTIAL_T:.0f} K 에서 "
            f"{potential_temperature - EARTH_POTENTIAL_T:+.0f} K 떨어져 있고, 그만큼 열압력이 "
            "밀도를 움직인다. 단열선은 대류하는 층에만 맞고, 조석가열과 맨틀 안의 열경계층은 "
            "프로파일을 초단열로 만든다 (Unterborn+ 2019 §3.2). 등급을 analog 로 내린다.")
    # 얼음 기둥이 얼음 X 까지 내려갔는가. 그 상은 이 사다리에서 **읽은 게 아니라 적합한**
    # 유일한 얼음이고, 원 표현을 1.475 % 안에서만 재현한다 — 다른 얼음 상들의 0.006~
    # 0.118 % 와 자릿수가 다르다. 게다가 그 표현 자체가 제일원리 계산이지 측정이 아니다.
    # mgsio3_pv 가 3.5 TPa 위에서 등급을 내리는 것과 같은 종류의 자리다.
    ice_x_reached = (st.p_ice_base is not None
                     and st.p_ice_base > ICE_VII_TO_X)
    if ice_x_reached:
        notes.append(
            f"**얼음 기둥이 얼음 X 까지 내려갔다** — 기둥 바닥이 "
            f"{st.p_ice_base / 1e9:.0f} GPa 로 얼음 VII→X 전이({ICE_VII_TO_X / 1e9:.1f} GPa) "
            "아래다. 그 상은 측정된 압축 자료의 적합이 아니라 제일원리 자유에너지 "
            "퍼텐셜(French & Redmer 2015)이고, 이 파일의 다른 얼음 상들과 달리 읽은 값이 "
            "아니라 **적합** 이다 — 매듭 구간이 1.7 GPa 에서 시작해 P = 0 을 평가할 수 "
            "없어서 그 길이 막혔다. 그 적합이 원 표현을 재현하는 폭이 1.475 % 이고, "
            "얼음 III·V·VI 의 0.006~0.118 % 와 자릿수가 다르다. 37.4 GPa 이음매도 "
            "−2.26 % 로 규산염 이음매(0.21 %)의 열 배다. 등급을 analog 로 내린다.")
    silicate_extrapolated = st.p_silicate_max > SILICATE_EXTRAPOLATED_MIN
    if silicate_extrapolated:
        notes.append(
            f"**규산염이 외삽 구간에 들어갔다** — 규산염 층 바닥이 "
            f"{st.p_silicate_max / 1e12:.2f} TPa 로 PREM 적합의 상한 "
            f"{SILICATE_EXTRAPOLATED_MIN / 1e12:.1f} TPa 위다. 그 위는 측정된 행성의 "
            "적합이 아니라 제일원리 계산이다 — Seager+ 2007 §III.3 이 Karki+ 2000 의 "
            "150 GPa 까지의 DFT 계산을 BME4 로 13.5 TPa 까지 끌고 간 것이고, 그 사이에서 "
            "MgSiO₃ 는 실제로 MgO + SiO₂ 로 해리한다 (Umemoto+ 2017: 0.75 · 1.31 · "
            "3.10 TPa). 그 해리를 무시하는 근거는 그 압력대에서 조성이 밀도를 거의 정하지 "
            "않는다는 것이고 (Zeng+ 2016 §II, A=20·Z=10), 실험도 관측도 아니다. "
            "이음매 자체는 재봤다 — 3.5 TPa 에서 두 적합이 0.21 % 안에서 겹친다. "
            "등급을 analog 로 내린다.")
    giant_unvalidated = (gmf > 0 and envelope_z == 0.0
                         and mass_earth < GIANT_ANCHOR_PASS_ME)
    if envelope_z > 0:
        notes.append(
            f"**외피 중원소 {envelope_z:.3f} 는 선언이다.** 강착과 진화가 정하는 값이고 "
            "이 레시피에는 그 둘이 없으므로, 관측 반지름에서 되읽어 맞춘 것이 아니라 "
            "받아쓴 것이다. 이 갈래가 토성을 Z = 0.200 (Guillot 1999 예산의 아래 끝) 에서 "
            "평균반지름 대비 −0.1 % 로 재현하는데, 그것이 보이는 것은 혼합 규칙이 맞다는 "
            "것이지 이 레시피가 토성을 예측한다는 것이 아니다. 그래서 등급을 analog 로 "
            "내린다.")
    if not differentiated:
        notes.append(
            "**미분화 천체에는 측정 앵커가 없다.** 완전히 섞인 암석-금속 천체의 C/MR² 를 "
            "잰 사례를 찾지 못했다 — Ceres 와 Callisto 는 부분 분화이고 그건 다른 문제다. "
            "대신 판별 검사가 있다: 수성 질량·금속분율을 미분화로 풀면 C/MR² 가 0.393 이고 "
            "측정값 0.346 보다 13.7 % 높다. 수성이 분화했다는 것을 이 레시피가 맞게 "
            "말한다는 뜻이지, 미분화 값 자체가 검증됐다는 뜻은 아니다. 등급을 analog 로 "
            "내린다.")
    if giant_unvalidated:
        toward = ("토성 쪽에" if abs(mass_earth - GIANT_ANCHOR_FAIL_ME)
                  < abs(mass_earth - GIANT_ANCHOR_PASS_ME) else "목성 쪽에")
        notes.append(
            "**검증되지 않은 질량이다.** 이 갈래의 앵커는 둘뿐이다 — 목성"
            f"({GIANT_ANCHOR_PASS_ME:.4g} M⊕) 에서 평균반지름 대비 +0.6 %, 토성"
            f"({GIANT_ANCHOR_FAIL_ME:.4g} M⊕) 에서 Z = 0 이면 +20.7 %. {mass_earth:.4g} M⊕ "
            f"는 그 사이이고 {toward} 가깝다. **Z 를 선언하지 않았으므로** 여기 나온 "
            "반지름과 C/MR² 는 목성에 맞춰진 상수 하나가 어느 거대행성에나 돌려주는 같은 "
            "값이고 (R = √(πK/2G) 에 M 도 조성도 없다), 잔차가 0.6 % 쪽인지 20.7 % 쪽인지 "
            "말할 근거가 없다. 등급을 analog 로 내린다. 토성의 20.7 % 는 이제 이 갈래가 "
            "그 질량에서 틀렸다는 뜻이 아니라 **거기서는 조성이 필요하다** 는 뜻이다 — "
            "envelope_z 를 주면 −0.1 % 로 내려온다.")
    notes += [
             "이 노드는 결합 코어 안에 있다 (chain.yaml 순환 1·3). converged 는 "
             "**이 적분의 사격이 붙었는가** 를 말하지, 조석가열이 조성을 되바꾸는 "
             "그래프 고리가 닫혔는가를 말하지 않는다 — 그 고리는 러너가 코어를 "
             "돌릴 때 닫힌다.",
             "등온이다. 핵과 하부맨틀 EOS 가 PREM 적합이라 지구의 열구조와 가벼운 "
             "원소가 그 유효 ρ₀ 안에 흡수돼 있다."]
    if st.t_center > 0.0:
        notes.append(
            "**core_temperature 와 cmb_temperature 는 하한이지 핵의 온도가 아니다.** 이 "
            "적분은 표면에서 중심까지 단열선 하나를 이어서 그리므로, 핵이 맨틀의 단열선 "
            "위에 앉는다. 판정선이었던 Unterborn+ 2019 eq. 7 도 **맨틀** 단열선이고 그들의 "
            "2635 K 는 핵-맨틀 경계의 맨틀 쪽 값이다 (그 논문이 Lay+ 2008 의 2500–2800 K 와 "
            "대조하며 그렇게 적는다). 그 사이에 D″ 열경계층이 있고 그 ΔT 는 핵-맨틀 경계의 "
            "열류가 정한다 — 지구에서 1200 K 를 넘고 (Sinmyo+ 2019 의 핵 쪽 3760 ± 290 K), "
            "이 레시피에는 그 열류가 없다. 더해서 철의 단열 기울기가 낮다: γ 항등식이 "
            "Seager+ 2007 의 αK₀(열압력용 상수)를 받아 핵 압력대에서 γ_Fe ≈ 0.22 를 내는데, "
            "ab initio 값은 1.5 다 (Alfè+ 2002, arXiv:cond-mat/0107307). 두 편향이 같은 "
            "방향(아래)이라 이 값은 **하한** 이고, core_state 가 그 성질을 쓴다.")

    # 공극이 남을 레짐인가. 적분이 낸 중심압을 쓰므로 적분 뒤에만 물을 수 있다.
    voids_ok, voids_why = voids_expected(st.mass_kg, st.p_center, tidal_heating)
    notes.append(("공극 레짐 판정 — " if voids_ok else "공극 레짐 판정 ⚠ — ") + voids_why)

    reason = (f"{mass_earth:.4g} M⊕ 를 핵질량분율 {cmf:.3f}"
              + (f" · 얼음질량분율 {imf:.3f}" if imf > 0 else "")
              + (f" · 가스질량분율 {gmf:.3f}" if gmf > 0 else "")
              + (f" · 외피중원소 {envelope_z:.3f}" if envelope_z > 0 else "")
              + ("" if differentiated else " · 미분화(암석+금속 한 층)")
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
        # 등급은 적합의 좋음이 아니라 **답이 이 레시피가 검증할 수 없는 선언에 기대는가**
        # 를 말한다. φ₀ 도 Z 도 강착과 진화가 정하는 값이라 여기서 도출되지 않고,
        # 미분화는 측정 앵커가 없다.
        grade=("analog" if (initial_porosity > 0 or envelope_z > 0
                            or not differentiated or giant_unvalidated
                            or silicate_extrapolated or thermal_moves
                            or thermal_unchecked or ice_x_reached)
               else "calibrated"),
        inputs=inputs,
        cycles=(1, 3),
        converged=converged,
        values={"nmoi": st.nmoi,
                "core_temperature": st.t_center,
                "cmb_temperature": st.t_cmb,
                "cmb_pressure": (st.p_cmb or 0.0) / 1e9,
                "ice_column_state": ice_state,
                "core_radius_fraction": st.core_radius_m / st.radius_m,
                "core_radius": st.core_radius_m / EARTH_RADIUS_M,
                "radius": radius,
                "core_pressure": st.p_center / 1e9,
                "bulk_porosity": st.phi_bulk,
                "voids_expected": voids_ok},
        units={"nmoi": "dimensionless",
               "core_temperature": "K",
               "cmb_temperature": "K",
               "cmb_pressure": "GPa",
               "ice_column_state": "",
               "core_radius_fraction": "dimensionless",
               "core_radius": "R_earth",
               "radius": "R_earth",
               "core_pressure": "GPa",
               "bulk_porosity": "dimensionless",
               "voids_expected": ""},
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
                         rock: Result, inputs: dict,
                         tidal_heating: bool = False) -> Result:
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
                     initial_porosity=phi, porosity_cap=cap,
                     tidal_heating=tidal_heating)

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
                      ice_allowed: bool = True,
                      tidal_heating: bool = False) -> Result:
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
              "ice_allowed": ice_allowed, "body_class": None,
              "tidal_heating": tidal_heating}

    if mass_earth <= 0 or radius_earth <= 0:
        return out_of_domain(RECIPE, VERSION, "질량 또는 반지름이 양수가 아니다",
                             inputs=inputs, refs=REFS)

    rock = solve(mass_earth, core_mass_fraction=0.0, ice_mass_fraction=0.0,
                 tidal_heating=tidal_heating)
    if not rock.applicable:
        return rock

    if radius_earth <= rock.values["radius"]:
        axis, span = "core_mass_fraction", (0.0, 1.0)

        def at(x):
            return solve(mass_earth, core_mass_fraction=x, ice_mass_fraction=0.0,
                         tidal_heating=tidal_heating)
    elif not ice_allowed:
        # 기준선보다 가벼운데 얼음이 선언으로 배제돼 있다. 남는 기작은 빈 공간이고,
        # 이제 그 빈 공간에 근거된 관계식이 있다 — 그래서 여기서 끝나지 않는다.
        return _porous_rock_verdict(mass_earth, radius_earth, rock, inputs,
                                    tidal_heating)
    else:
        axis, span = "ice_mass_fraction", (0.0, 0.98)

        def at(x):
            return solve(mass_earth, core_mass_fraction=0.0, ice_mass_fraction=x,
                         tidal_heating=tidal_heating)

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
        gas_mass_fraction=state.get("gas_mass_fraction"),
        # Z 는 **선언** 이다. 강착과 진화가 정하는 값이고 이 레시피에 그 둘이 없다.
        envelope_z=state.get("envelope_z", 0.0),
        composition=state.get("composition_intent", "earth_like"),
        radius_earth=state.get("radius_earth"),
        differentiated=state.get("differentiated", True),
        body_class=state.get("body_class"),
        # 공극은 **선언** 으로 들어온다. 기본값 0 은 "공극이 없다" 가 아니라
        # "이 레시피가 판정하지 않는다" 는 뜻이다 — φ₀ 는 강착이 정하고 가열이 지운다.
        initial_porosity=state.get("initial_porosity", 0.0),
        porosity_cap=state.get("porosity_cap"),
        # 포텐셜 온도도 **선언** 이다. 없으면 온도가 아예 흐르지 않고 예전 등온 경로다.
        potential_temperature=state.get("potential_temperature"),
        tidal_heating=bool(state.get("tidal_heating", False)),
    )
