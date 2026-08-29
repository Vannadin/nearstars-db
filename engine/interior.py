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

import water_hot
import water_table
from eos import (EARTH_POTENTIAL_T, IAPWS_VII_END, ICE_VII_TO_X,
                 ICE_VII_X_T_MAX, MATERIALS, REINHARDT_P_MAX, SILICATE_PREM_TO_PV,
                 PhaseGap, mix, water_phase_name, water_vii1_vii2_boundary)
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
    "2019JChPh.151e4501B",      # Bollengier+ 2019 (SeaFreeze water1) — 액체 물, 0–2.3 GPa
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
# 걸음 안의 경계 둘 — 층 전환과 표 바닥 — 을 걸음 안에서 보간한다. False 는 2026-08-28
# 이전의 경로(둘 다 걸음 단위 양자화)이고, 격자 대조 검사만 그것을 켠다 — 답이 어느 쪽으로
# 가는지를 재는 대조 상대로.
INTERPOLATE_LAYERS = True
# 얼음 기둥 안에서 국소 (P, T) 가 녹는곡선 위이면 액체 물로 적분한다 (2026-08-29). False 는
# 판정만 내고 밀도는 고체상으로 두던 2026-08-27 의 경로이고, 바다가 밀도를 실제로 움직이는지를
# 재는 대조 검사만 그것을 켠다.
OCEAN_LAYER = True
# 기체 외피가 표의 영역을 벗어난 자리가 **표면인가, 시험 온도의 잘못인가.** 1 bar 의 몇 배 안에서
# 벗어나면 표면이다 — 천왕성의 1 bar 온도(76 K)가 표 바닥(100 K) 아래라 실제로 그 몇 bar 위에서
# 걸리고, 1 bar 온도는 T ∝ P^∇ 로 닫힌다. 그 배수 밖에서 벗어나는 것은 표면이 아니라 외피 바닥이
# 대류가 닿는 온도 아래라는 뜻이고, 시험 중심 온도를 올려야 풀린다. 2026-08-29 까지 둘을 가르지
# 않아 5 M⊕ 서브넵튠의 외피가 244 GPa 에서 '표면' 으로 잘려 질량 0 이 됐고, 사다리가 철 천장까지
# 올라가 거짓 거절을 냈다 (sub-neptune-context-notes.md). 100 은 앵커의 시험 경로가 실제로 닿는
# 최대 9 bar (해왕성) 의 열 배 위라, 앵커는 이 갈래를 한 번도 타지 않는다.
FLOOR_EXTRAPOLATION_MAX = 100.0
MAX_STEPS = 40000
SHOOT_ITERS = 200
SHOOT_TOL = 1e-8            # 겉질량의 상대오차


class Structure:
    """적분 한 번의 결과. Result 로 포장하기 전의 알맹이."""

    __slots__ = ("radius_m", "mass_kg", "moi", "core_radius_m", "p_center",
                 "p_cmb", "p_ice_base", "phases", "v_pore", "m_above_lab",
                 "p_silicate_max", "t_center", "t_cmb", "t_surface", "ice_samples",
                 "p_surface", "r_ocean_base", "r_ocean_top", "surface_reached",
                 "ice_x_reached")

    def __init__(self, radius_m, mass_kg, moi, core_radius_m, p_center,
                 p_cmb, p_ice_base, phases, v_pore=0.0, m_above_lab=0.0,
                 p_silicate_max=0.0, t_center=0.0, t_cmb=0.0, t_surface=0.0,
                 ice_samples=(), p_surface=0.0, r_ocean_base=None, r_ocean_top=None,
                 surface_reached=True, ice_x_reached=False):
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
        # 적분이 멈춘 압력 [Pa]. 응축상 천체는 0 이다 — 표면이 P = 0 이니까. 기체 외피가
        # 있으면 그 재료의 압력 바닥(1 bar)이고, 발표된 거대행성 반지름이 그 준위의 값이다.
        self.p_surface = p_surface
        # 사다리의 얼음 X 를 실제로 밟았는가. 기둥 바닥의 압력이 37.4 GPa 위여도 그 자리가
        # 유체(h2o_hot)면 얼음 X 가 아니다 — 압력이 아니라 밟은 재료로 판정한다.
        self.ice_x_reached = ice_x_reached
        # 바다의 바닥과 꼭대기 반지름 [m]. 얼음 기둥 안에서 국소 (P, T) 가 녹는곡선 위에 있던
        # 구간이다. None 은 "액체인 자리가 없었다" 는 뜻이고, 온도가 흐르지 않은 해는 늘 None 이다.
        self.r_ocean_base = r_ocean_base
        self.r_ocean_top = r_ocean_top
        # False 면 표면(P = p_stop)에 닿기 전에 걸음 상한에서 잘린 부분 적분이다. 겉질량이 이미
        # 목표를 넘겼을 때만 그렇게 돌아오고, 사격의 괄호에만 쓰인다 — 수렴해가 될 수 없다.
        self.surface_reached = surface_reached

    @property
    def ocean_thickness_m(self) -> float:
        if self.r_ocean_base is None or self.r_ocean_top is None:
            return 0.0
        return self.r_ocean_top - self.r_ocean_base

    @property
    def ice_shell_thickness_m(self) -> float:
        """바다 위에 남은 고체 얼음의 두께. 바다가 없으면 0 — 기둥 전체를 껍질이라 부르지 않는다."""
        if self.r_ocean_top is None:
            return 0.0
        return self.radius_m - self.r_ocean_top

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
        # 얼음층의 이름은 사다리(h2o)다. 그 자리의 물이 액체인지 고체인지는 적분기가 걸음마다
        # 국소 (P, T) 를 녹는곡선에 대서 정하고, 액체면 h2o_liquid(2.3 GPa 까지) 또는
        # h2o_hot 으로 갈아탄다 — 2026-08-30 까지는 천체 종류가 h2o_hot 을 통째로 골랐다.
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
    K_T 는 냉각 곡선의 수치 미분으로 잰다.

    **재료가 자기 ∇_ad 를 들고 있으면 그것을 쓴다.** 조립하는 것은 Birch-Murnaghan 상이
    내줄 수 있는 것이 γ 와 K_T 뿐이라서이지, 그 경로가 더 옳아서가 아니다. 수소-헬륨
    표는 저자들이 자기 엔트로피에서 계산한 (∂lnT/∂lnP)_S 를 그대로 싣고 있고, 그걸 두고
    다시 만드는 것은 발표된 수를 우리 조립으로 바꿔 적는 것이다. 이 갈래가 없는 재료는
    한 줄도 지나지 않으므로 비트까지 같다."""
    own = getattr(mat, "dtdp_adiabat", None)
    if own is not None:
        return own(p, t, t_pot)
    gamma = mat.gruneisen(p, rho, t, t_pot)
    if gamma <= 0.0 or t <= 0.0:
        return 0.0
    h = p * 1e-4
    # 재료가 압력 바닥을 말하면 그 아래로 차분을 내밀지 않는다. 기체 외피의 표면(1 bar)
    # 에서 실제로 걸린다 — 반 칸 아래가 굳힌 창 밖이라 거절이 나고, 그건 물리가 아니라
    # 차분의 발이다. 그 자리에서는 한쪽 차분으로 바꾼다.
    p_lo, p_hi = p - h, p + h
    floor = getattr(mat, "p_floor", 0.0)
    if floor and p_lo < floor:
        p_lo, p_hi = p, p + 2.0 * h
    d_hi, d_lo = mat.density(p_hi, t, t_pot), mat.density(p_lo, t, t_pot)
    if d_hi <= d_lo:
        return 0.0
    k_t = rho * (p_hi - p_lo) / (d_hi - d_lo)
    # αK_T·γ·T = K_T·αγT 이므로 K_S 가 새 상수 없이 닫힌다.
    ph = mat.phase_at(p) if hasattr(mat, "phase_at") else None
    k_s = k_t + (ph.dpdt_v(t, t_pot) * gamma * t if ph is not None else 0.0)
    return gamma * t / max(k_s, 1.0)


def _grad_ad_at(mat, p: float, t: float, t_pot: float = 0.0) -> float:
    """이 재료가 이 자리에서 들고 있는 (∂lnT/∂lnP)_S = (dT/dP)·P/T.

    수소-헬륨은 발표된 ∇_ad 를 그대로 내고, 중원소가 녹은 혼합은 γ 와 K_S 로 조립한
    기울기를 같은 형태로 환산한다 — 어느 쪽이든 **적분기가 온도를 멱법칙으로 나르는
    데 쓰는 지수** 다."""
    if t <= 0.0 or p <= 0.0:
        return 0.0
    return _adiabatic_dtdp(mat, p, mat.density(p, t, t_pot), t, t_pot) * p / t


def _carries_silicate(mat) -> bool:
    """이 층 재료가 규산염을 들고 있는가. 혼합이면 성분 중에 있는지를 본다."""
    if mat.name == "silicate":
        return True
    return any(m.name == "silicate" for m, w in getattr(mat, "parts", ()) if w > 0.0)


def integrate(p_center: float, mass_kg: float, cmf: float, imf: float,
              core_material: str, phi0: float = 0.0,
              p_cap: float | None = None, gmf: float = 0.0,
              envelope_z: float = 0.0, differentiated: bool = True,
              t_center: float = 0.0, t_pot: float = 0.0,
              boundary_temperature_jump: float = 0.0,
              mantle_rock_fraction: float = 0.0) -> Structure:
    """중심압 하나에서 바깥으로 적분한다. 표면(P=0)에서 멈춘다.

    층 경계는 **목표 질량** 의 누적 분율로 잡는다. 사격이 수렴하면 겉질량이 목표와
    같으므로 이 선택은 수렴점에서 정확하고, 반복마다 경계가 흔들리지 않아 이분법이
    단조를 유지한다.

    `phi0` 가 0 보다 크면 각 자리의 고체 밀도에 (1 − φ(P)) 를 곱한다. φ 는 **국소
    압력의 함수** 이므로 자유 매개변수가 아니다 — porosity.py 를 보라. φ₀ 자체는
    강착과 가열이 정하고 이 레시피에 그 둘이 없어서 선언으로 들어온다."""
    stack = _stack(cmf, imf, core_material, gmf, envelope_z, differentiated)
    mat = stack[0][1]
    # 적분이 멈추는 압력. 응축상 천체는 0 — 표면이 P = 0 이다. 기체 외피가 바깥에 있으면
    # 그 재료가 자기 바닥을 말한다 (1 bar). 바깥 층 하나가 정하므로 여기서 한 번 본다.
    p_stop = getattr(stack[-1][1], "p_floor", 0.0)

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
    p_surface = 0.0
    last_grad = 0.0        # 마지막으로 잰 ∇_ad. 표면 밖에서는 다시 잴 수 없다
    ice_samples: list[tuple[float, float]] = []
    ICE_SAMPLE_EVERY = 20
    # ── 바다 ──
    # 얼음 기둥(h2o)의 한 자리가 액체인가는 그 자리의 (P, T) 를 녹는곡선에 댄 것으로 정한다.
    # 그 판정을 **걸음의 출발점에서 한 번만** 내리고 걸음 전체의 재료를 그것으로 고정한다 —
    # RK4 의 네 자리에서 각자 판정하게 두면 상이 걸음 안에서 뒤집혀 2026-08-28 에 걷어낸
    # 그 계단이 돌아온다. 걸음 안에서 상이 바뀌는 자리는 층 경계와 같은 방법으로 찾는다
    # (아래). 온도가 흐르지 않으면(t = 0) 이 판정은 아예 없고 예전 경로 그대로다.
    liquid_mat = MATERIALS["h2o_liquid"]
    hot_mat = MATERIALS["h2o_hot"]
    forced_liquid = None   # 방금 상 경계를 넘었다. 다음 걸음은 판정 없이 이 상으로 시작한다
    r_ocean_base = None
    r_ocean_top = None
    ice_x_stepped = False  # 사다리의 얼음 X 를 실제로 밟았는가. 압력만으로는 모른다 — 그 자리가 유체일 수 있다
    # ── 두 선언 (C5) ──
    # 얼음 맨틀에 섞인 암석. 물의 어느 상이든(사다리·바다·뜨거운 물) 같은 분율의 규산염과 부피
    # 가법으로 섞고, ∇_ad 는 c_P 가중이다 (Mixture). 상마다 혼합 객체를 하나씩 만들어 둔다.
    rock_mix: dict[str, object] = {}

    def with_rock(water_mat):
        if mantle_rock_fraction <= 0.0:
            return water_mat
        m = rock_mix.get(water_mat.name)
        if m is None:
            m = mix(f"{water_mat.name}_rock", "얼음 맨틀 + 암석",
                    (water_mat, 1.0 - mantle_rock_fraction),
                    (MATERIALS["silicate"], mantle_rock_fraction))
            rock_mix[water_mat.name] = m
        return m

    def apply_jump(prev_layer: int) -> None:
        """얼음 맨틀에서 기체 외피로 넘어가는 자리의 열경계층. 안쪽이 선언한 만큼 더 뜨겁다 —
        바깥으로 적분하므로 여기서 온도가 그만큼 **떨어진다** (Nettelmann+ 2016 의 TBL). 떨어진
        온도가 0 아래면 이 시험 중심 온도로는 경계층 위가 존재하지 않으므로 온도가 막은 것으로 던진다."""
        nonlocal t
        if boundary_temperature_jump <= 0.0 or t <= 0.0:
            return
        if (stack[prev_layer][1].name == "h2o"
                and getattr(stack[layer][1], "p_floor", 0.0)):
            if t - boundary_temperature_jump <= 0.0:
                raise PhaseGap(
                    "h_he", p,
                    f"얼음 맨틀 꼭대기 {t:.0f} K 에서 선언된 열경계층 {boundary_temperature_jump:.0f} K 를 "
                    "빼면 외피가 0 K 아래다 — 이 중심 온도로는 경계층 위의 외피가 없다.",
                    t, too_cold=True)
            t -= boundary_temperature_jump

    def liquid_material(pp: float, tt: float):
        """액체인 자리의 재료. 2.3 GPa 까지는 바다(SeaFreeze water1), 그 위는 뜨거운 물(Mazevet+ 2019)
        — 단 그 적합이 유체에 대해 적은 하한(1000 K) 위에서만. 그 아래는 이 저장소에 조밀한
        액체의 상태방정식이 없고, 바다 재료가 압력 상한을 이름 대며 거절한다 (2026-08-30 전과 같은
        거절이라 그 경로를 밟는 천체는 비트까지 같다)."""
        if pp > water_table.P_MAX_PA:
            if tt >= water_hot.T_MIN:
                return hot_mat
            # 조밀한 액체인데 그 온도의 상태방정식이 없다. **온도가 막은 것으로, 위로 던진다** —
            # 액체는 더 뜨거워져도 액체이고 이 저장소에서 그 위에 있는 유일한 적합이 Mazevet 이라,
            # 온도 괄호가 중심 온도를 올리면 풀린다. 2026-08-30 전에는 이 자리를 h2o_hot 의
            # 1800 K 하한이 같은 방향으로 던졌다.
            raise PhaseGap(
                hot_mat.name, pp,
                f"{pp / 1e9:.2f} GPa · {tt:.0f} K 의 물은 녹는곡선 위(액체)인데, 이 온도의 조밀한 액체 "
                f"상태방정식이 없다 — 바다 표(SeaFreeze water1)는 {water_table.P_MAX_PA / 1e9:.1f} GPa "
                f"에서 끝나고 뜨거운 물(Mazevet+ 2019)은 ρ ≳ 1 g/cc 에서 {water_hot.T_MIN:.0f} K 위를 "
                "적는다. 선반은 있다 — SeaFreeze water2 (Brown 2018, 0–100 GPa · 240–10 000 K).",
                tt, too_cold=True)
        if tt > water_table.T_MAX_K:
            # 낮은 압력의 뜨거운 액체. Mazevet+ 2019 §3.1 이 ρ ≲ 1 g/cc · T ≲ 2000 K 의 액체와
            # 10³ K 위의 플라스마를 적합 구간으로 적으므로 바다 표의 500 K 위는 그쪽이 받는다 —
            # 단 1000 K 부터다. 500–1000 K 의 액체는 두 적합 사이의 틈이고, 위와 같은 이유로 온도가
            # 막은 것으로 던진다 (얼음거대행성의 시험 경로가 외피 바닥 2 GPa · 986 K 로 실제로 지난다).
            if tt >= water_hot.T_MIN:
                return hot_mat
            raise PhaseGap(
                hot_mat.name, pp,
                f"{pp / 1e9:.2f} GPa · {tt:.0f} K 의 물은 녹는곡선 위(액체)인데 이 온도의 액체 상태방정식이 "
                f"없다 — 바다 표(SeaFreeze water1)는 {water_table.T_MAX_K:.0f} K 에서 끝나고 뜨거운 물"
                f"(Mazevet+ 2019)은 {water_hot.T_MIN:.0f} K 위를 적는다. 선반은 있다 — SeaFreeze water2 "
                "(Brown 2018, 0–100 GPa · 240–10 000 K).",
                tt, too_cold=True)
        return liquid_mat

    def liquid_at(pp: float, tt: float) -> bool:
        """이 (P, T) 의 얼음 기둥에 **유체의 상태방정식** 을 쓰는가.

        곡선이 닿는 자리는 곡선이 답한다. 20.6 GPa 까지는 IAPWS 의 녹는곡선(액체 ↔ 얼음). 그 위
        70 GPa 까지는 Reinhardt+ 2022 의 **VII′–VII″ 선** 이 경계다 — 그 아래의 VII·VII′·X 는 절연
        얼음이고 사다리(French & Redmer 2015)의 몫, 그 위의 VII″ 는 초이온 bcc 얼음이라 액체와 함께
        Mazevet+ 2019 의 한 적합(액체·플라스마·초이온을 한 형태로)이 받는다. 액체선(52.4 GPa 까지)은
        그 안에서 액체와 VII″ 를 **이름** 으로 가르는 데 쓰이고 밀도는 안 가른다.

        70 GPa 위는 어느 선도 닿지 않아 판정이 undecided 이고, 재료는 **가용성** 으로 고른다 —
        사다리의 적합이 서 있는 곳(1 TPa · 1800 K 아래, 둘 다 매듭의 끝이지 상 경계가 아니다)은
        사다리, 그 밖은 Mazevet(1000 K 위), 둘 다 없으면 온도가 막은 것으로 던진다. 그 선택이 상의
        판정이 아니라는 것을 _ice_verdict 가 적는다."""
        if pp <= IAPWS_VII_END:
            return bool(MATERIALS["h2o"].liquid_at(pp, tt))
        t_b = water_vii1_vii2_boundary(pp)
        if t_b is not None and tt >= t_b:
            return True
        # 선이 닿으면 VII′/X 고체, 안 닿으면 undecided. 어느 쪽이든 사다리의 적합이 서 있는 동안은
        # 사다리다. 그 밖(1800 K 위 또는 1 TPa 위)은 상이 무엇이든 읽을 수 있는 것이 Mazevet 뿐이다 —
        # 65–70 GPa 의 VII′/X 가 1800 K 위에 앉는 좁은 띠가 실제로 여기를 지난다(해왕성의 시험 경로).
        if tt < ICE_VII_X_T_MAX and pp <= MATERIALS["h2o"].p_max:
            return False
        if tt >= water_hot.T_MIN:
            return True
        # 사다리는 압력으로 끝났고(1 TPa) 유체 적합은 온도로 아직 안 열렸다(1000 K). 남은 표현이
        # 없다 — 그리고 이 자리는 더 뜨거우면 Mazevet 이 받으므로 **온도가 막은 것으로** 던진다.
        raise PhaseGap(
            "h2o", pp,
            f"{pp / 1e9:.0f} GPa · {tt:.0f} K 의 물에는 읽을 표현이 없다 — 얼음 사다리는 "
            f"{MATERIALS['h2o'].p_max / 1e9:.0f} GPa 에서 끝나고(French & Redmer 2015 의 매듭 구간), "
            f"뜨거운 물(Mazevet+ 2019)은 {water_hot.T_MIN:.0f} K 위를 적는다. 녹는곡선도 "
            f"{REINHARDT_P_MAX / 1e9:.1f} GPa 위에는 없어서 어느 상인지도 말하지 못한다.",
            tt, too_cold=True)

    def material_for(m_now: float):
        nonlocal layer
        while layer < len(stack) - 1 and m_now >= stack[layer][0] * mass_kg:
            layer += 1
        return stack[layer][1]

    def note_switch(prev_layer: int) -> None:
        """층이 바뀐 자리의 압력을 기록해둔다. core_state 와 얼음 상 판정이 쓴다."""
        nonlocal core_radius, p_cmb, t_cmb, p_ice_base
        if prev_layer == 0 and cmf > 0:
            core_radius, p_cmb, t_cmb = r, p, t
        if stack[layer][1].name == "h2o":
            p_ice_base = p

    steps = 0
    while p > p_stop and steps < MAX_STEPS:
        steps += 1
        prev_layer = layer
        mat = material_for(m)
        if layer != prev_layer:
            note_switch(prev_layer)
            apply_jump(prev_layer)
            forced_liquid = None
        in_column = OCEAN_LAYER and t > 0.0 and mat.name == "h2o"
        liquid = False
        if in_column:
            liquid = forced_liquid if forced_liquid is not None else liquid_at(p, t)
            forced_liquid = None
            if liquid:
                mat = liquid_material(p, t)
                if mat is liquid_mat and r_ocean_base is None:
                    r_ocean_base = r
        if mat.name == "h2o" and p > ICE_VII_TO_X:
            ice_x_stepped = True       # 등온 경로도 포함한다 — 사다리를 그 압력에서 실제로 밟았다
        if mat.name not in phases:
            phases.append(mat.name)
        if in_column and p > water_table.P_MAX_PA:
            # 물의 상은 위에서 정해졌다. 암석은 그 위에 섞인다 — 단 **깊은 맨틀** 에만 (Nettelmann 의
            # inner envelope). 바다 표의 2.3 GPa 아래는 바다·얕은 얼음이고, 거기 암석을 섞는 것은 물리도
            # 아니거니와 바다 표가 c_P 를 안 들고 있어 혼합의 ∇_ad 를 가중할 수도 없다.
            mat = with_rock(mat)

        # **기체에는 P = 0 인 표면이 없다.** 밀도가 압력과 함께 0 으로 가므로 적분이
        # 어디서 끝나는지를 재료가 말해야 하고, 그 자리가 발표된 반지름이 재어진
        # 준위(1 bar)다. 표의 온도 바닥 아래로 내려가는 것도 같은 뜻이다 — 그건 거절이
        # 아니라 **표면에 닿았다** 는 뜻이므로, 여기서 멈추고 그 사실을 들고 나간다.
        floor = getattr(mat, "p_floor", 0.0)
        if floor and (t > 0.0 and not mat.in_domain(p, t)):
            if p > floor * FLOOR_EXTRAPOLATION_MAX:
                # 표면이 아니다. 재료가 어느 벽인지 이름 대며 던지고, 온도 괄호가 받는다.
                mat.check_temperature(p, t)
            p_surface = p
            t_surface = t
            if p > floor * 1.001 and last_grad > 0.0:
                # 압력 바닥이 아니라 **온도 바닥** 에 먼저 닿았다. 표가 100 K 에서
                # 끝나고 천왕성의 1 bar 온도는 76 K 라 실제로 걸린다. 경계조건은
                # 1 bar 준위에 걸려 있으므로, 그 준위의 온도를 단열선의 국소 멱법칙
                # T ∝ P^∇_ad 으로 닫아 준다 — 압력 비가 서너 배라 한 줄이면 된다.
                # 반지름은 그렇게 늘리지 않는다. 그 결손은 note 가 수로 말한다.
                t_surface = t * (floor / p) ** last_grad
            break
        if mat.name in ("h2o", "h2o_liquid", "h2o_hot") and (not ice_samples
                                                             or steps % ICE_SAMPLE_EVERY == 0):
            ice_samples.append((p, t))
        if p_si_max == 0.0 and _carries_silicate(mat):
            p_si_max = p

        # 4차 Runge-Kutta. 한 단계 안에서는 재료를 고정한다 — 경계에서 한 단계
        # 어긋나는 오차는 dr/R ~ 3e-4 이라 C/MR² 의 유효숫자 밖이다.
        # 이 단계의 단열 기울기. 한 단계에 한 번만 잰다 (위 _adiabatic_dtdp 주석).
        dtdp = _adiabatic_dtdp(mat, p, mat.density(p, t, t_pot), t, t_pot) if t > 0.0 else 0.0
        # **기체 층에서는 온도를 선형이 아니라 멱법칙으로 나른다.** 반지름 격자가 균일한데
        # 기체 외피는 바깥 몇 걸음에서 압력이 자릿수로 떨어진다 — 한 걸음이 척도높이 두세
        # 개를 건너뛴다. dT = (dT/dP)dP 는 그 걸음에서 뜻을 잃고(목성 중심온도가 15,000 K
        # 대신 5,000 K 로 나왔다), 단열선은 그 구간에서 T ∝ P^∇_ad 이므로 같은 ∇_ad 로
        # 곱셈으로 나르면 걸음 크기에 둔감해진다. ∇_ad 를 들고 있는 재료만 이 갈래를
        # 타므로 나머지는 한 줄도 지나지 않는다.
        grad = (dtdp * p / t
                if (t > 0.0 and dtdp > 0.0 and getattr(mat, "p_floor", 0.0))
                else None)
        if grad:
            last_grad = grad

        def deriv(rr, mm, pp):
            if rr <= 0.0:
                return 0.0, 0.0, 0.0, 0.0
            # 마지막 반 걸음이 바닥 아래로 내려갈 수 있다. 그 자리의 밀도는 바닥의
            # 값으로 둔다 — 1 bar 의 수소-헬륨은 평균밀도의 10⁻⁴ 이라 질량에도
            # 반지름에도 유효숫자로 안 들어오고, 굳히지 않은 구간을 외삽하는 것보다
            # 이쪽이 정직하다.
            rr_rho = (mat.density(max(pp, p_stop), t, t_pot) if pp > 0.0
                      else mat.rho0)
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

        # **표 바닥도 걸음 안에서 찾는다.** 위의 in_domain 검사는 걸음의 출발점에서만 보므로
        # 온도 바닥에 닿는 자리가 걸음 단위로 양자화되고, 그러면 층 경계를 보간해도 반지름이
        # 격자 위상에 따라 dr/R 만큼 뛴다 (천왕성 1499·1500·1501 걸음에서 겉질량은 1e-6 안에
        # 고정인데 반지름이 2.5e-4 흔들렸다 — speed-context-notes §11). 걸음 안의 상태를 선형
        # 보간으로 두고 (표면 넘김과 같은 규칙) 바닥을 넘는 분율을 이분법으로 찾는다.
        # in_domain 은 표 조회 없이 부등식 둘이라 싸다.
        if (INTERPOLATE_LAYERS and getattr(mat, "p_floor", 0.0) and t > 0.0
                and p + dp > p_stop):
            t_end = t * ((p + dp) / p) ** grad if grad else t + dtdp * dp
            if not mat.in_domain(p + dp, t_end):
                if p + dp > floor * FLOOR_EXTRAPOLATION_MAX:
                    mat.check_temperature(p + dp, t_end)     # 위와 같다. 걸음 안의 자리
                lo_f, hi_f = 0.0, 1.0
                for _ in range(50):
                    mid = 0.5 * (lo_f + hi_f)
                    p_mid = p + dp * mid
                    t_mid = t * (p_mid / p) ** grad if grad else t + dtdp * dp * mid
                    if mat.in_domain(p_mid, t_mid):
                        lo_f = mid
                    else:
                        hi_f = mid
                frac = lo_f
                r += dr * frac
                m += dm * frac
                moi += di * frac
                v_pore += dv * frac
                p_new = p + dp * frac
                t = t * (p_new / p) ** grad if grad else t + dtdp * dp * frac
                p = p_new
                p_surface = p
                t_surface = t
                floor = mat.p_floor
                if p > floor * 1.001:
                    # 1 bar 준위까지의 외삽은 **탈출점 자신의** ∇_ad 로 닫는다. 2026-08-30 까지는 이
                    # 걸음 출발점의 값(last_grad)이었는데, 출발점은 반지름 격자 위에 있어서 어느 걸음이
                    # 바닥을 건너는지가 중심 온도에 따라 계단으로 바뀌고, 그러면 1 bar 온도가 중심
                    # 온도에 대해 ±0.4 K 로 들쭉날쭉해진다 (해왕성 72 K 에서 6300–6340 K 를 훑으면
                    # 71.46 ↔ 72.42 K). 온도 고리의 허용오차가 1e-3 이라 그 요철이 수렴을 운에
                    # 맡겼다 — 2026-08-30 전의 해왕성 converged=True 는 시험 경로가 우연히 요철의
                    # 골에 앉은 것이다. 탈출점의 (P, T) 는 이분법으로 찾은 자리라 격자에 안 묶인다.
                    g_exit = _grad_ad_at(mat, p, t, t_pot)
                    t_surface = t * (floor / p) ** (g_exit if g_exit > 0.0 else last_grad)
                break

        if p + dp <= p_stop:
            # 표면을 넘어섰다. 멈출 압력 자리로 선형 보간한다.
            frac = (p - p_stop) / (-dp) if dp != 0 else 0.0
            r += dr * frac
            m += dm * frac
            moi += di * frac
            v_pore += dv * frac
            p_new = p_stop
            t = t * (p_new / p) ** grad if grad else t + dtdp * dp * frac
            p = p_new
            p_surface = p_stop
            t_surface = t
            break

        # **층 경계가 이 걸음 안에 있으면 걸음을 경계까지 자른다.** 2026-08-28 까지는
        # 경계를 걸음 단위로만 넘겼다 — 걸음이 시작할 때의 누적질량이 경계를 넘어야 재료가
        # 바뀌었으므로, 경계 반지름이 dr = R/1500 로 양자화됐다. 그러면 겉질량이 중심압에
        # 대해 **계단** 이 된다. 경계가 한 걸음 옮겨갈 때마다 얼음 한 껍질이 기체로 바뀌므로
        # 단의 높이가 3·(dr/R)·(Δρ/ρ̄)·M ≈ 9×10⁻⁴ M 이고 (얼음→H/He 경계), SHOOT_TOL 10⁻⁸ 은 그
        # 10 만분의 1 이라 목표가 단의 수직면에 앉으면 할선법이 원리적으로 못 붙어 200 회를
        # 같은 중심압에 다시 적분했다 — 천왕성 1038 초의 정체 (speed-context-notes §6).
        # 걸음 안에서 경계 질량에 닿는 분율 f 를 이 걸음의 첫 기울기로 어림하고, f·dr 만큼을
        # 같은 RK4 로 다시 걷는다. 경계 위치의 오차가 O(dr) 에서 O(dr²) 로 내려가고 겉질량이
        # 중심압에 연속이 된다. 격자 대조가 이것이 고해상도 답 쪽으로 가는 것임을 보인다
        # (test_interior.py 의 격자 수렴 검사, 얼음거대행성 포함).
        h = dr
        crossed = False
        if INTERPOLATE_LAYERS and layer < len(stack) - 1:
            m_b = stack[layer][0] * mass_kg
            if dm > 0.0 and m + dm >= m_b:
                f = (m_b - m) / dm
                if 0.0 < f < 1.0:
                    h = f * dr
                    k2 = deriv(r + h / 2, m + h / 2 * k1[0], p + h / 2 * k1[1])
                    k3 = deriv(r + h / 2, m + h / 2 * k2[0], p + h / 2 * k2[1])
                    k4 = deriv(r + h, m + h * k3[0], p + h * k3[1])
                    dm = h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
                    dp = h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
                    di = h / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
                    dv = h / 6 * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3])
                    crossed = True

        # **상 경계도 걸음 안에서 찾는다.** 층 경계(질량)와 표 바닥(온도)을 걸음 안에서 보간하는
        # 것과 같은 자리다. 걸음 끝의 (P, T) 를 선형으로 내다보고 상이 뒤집히면, 뒤집히는 분율을
        # 이분법으로 찾아 그만큼만 걷는다. 층 경계가 이 걸음 안에 먼저 있었으면 이미 h 가 거기까지로
        # 잘려 있고, 그 안에서 상이 또 바뀌면 상 경계가 더 안쪽이므로 그쪽이 이긴다 — 층 경계는
        # 다음 걸음이 다시 찾는다. 판정은 walk 의 출발점 상과 같은 함수(liquid_at)라, 여기서 찾은
        # 자리와 다음 걸음의 판정이 어긋나지 않는다.
        phase_crossed = False
        if INTERPOLATE_LAYERS and in_column and p + dp > p_stop:
            t_end = t + dtdp * dp
            if liquid_at(p + dp, t_end) != liquid:
                lo_f, hi_f = 0.0, 1.0
                for _ in range(50):
                    mid = 0.5 * (lo_f + hi_f)
                    if liquid_at(p + dp * mid, t + dtdp * dp * mid) == liquid:
                        lo_f = mid
                    else:
                        hi_f = mid
                f = lo_f
                if 0.0 < f < 1.0:
                    h = f * h
                    k2 = deriv(r + h / 2, m + h / 2 * k1[0], p + h / 2 * k1[1])
                    k3 = deriv(r + h / 2, m + h / 2 * k2[0], p + h / 2 * k2[1])
                    k4 = deriv(r + h, m + h * k3[0], p + h * k3[1])
                    dm = h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
                    dp = h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
                    di = h / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
                    dv = h / 6 * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3])
                    crossed = False
                phase_crossed = True

        if p > P_LAB_MAX:
            m_above_lab += dm
        r += h
        m += dm
        moi += di
        v_pore += dv
        # 온도는 압력을 따라간다 — dT = (dT/dP) dP. 열 상수가 없는 층에서는
        # dtdp 가 0 이라 온도가 그 층을 그대로 통과한다.
        t = t * ((p + dp) / p) ** grad if grad else t + dtdp * dp
        p += dp
        t_surface = t
        if liquid and mat is liquid_mat:
            r_ocean_top = r
        if phase_crossed:
            # 상 경계에 섰다. 다음 걸음은 판정 없이 **반대 상** 으로 시작한다 — 이분법이 경계의
            # 이쪽에 멈추므로 다시 판정하면 같은 상이 나와 폭 0 의 걸음을 되풀이한다. 층 경계에서
            # material_for 의 문턱에 맡기지 않는 것과 같은 이유다.
            forced_liquid = not liquid
        if crossed:
            # 경계에 섰다. 다음 걸음은 새 재료로 시작한다 — material_for 의 문턱에 맡기지
            # 않는다. RK4 의 겉질량은 첫 기울기로 잰 m_b 와 O(dr²) 만큼 다를 수 있어서,
            # 문턱에 맡기면 같은 계단이 한 걸음 뒤로 옮겨갈 뿐이다.
            layer += 1
            note_switch(layer - 1)
            apply_jump(layer - 1)

    if steps >= MAX_STEPS and p > p_stop:
        if m > mass_kg * (1.0 + SHOOT_TOL):
            # 표면에 닿기 전에 목표 질량을 이미 넘겼다. 사격이 이 시험값에서 알아야 하는 것은
            # "질량이 넘친다" 뿐이므로 여기서 멈춰 그 사실을 들고 나간다 — 예전에는 예외를
            # 던졌고, 그 예외가 solve() 에서 물리인 척하는 거절로 나갔다 (5 M⊕ 서브넵튠의
            # 뜨거운 시험 온도에서 외피가 격자 밖까지 부풀었다, sub-neptune-context-notes.md).
            # 수렴해로 받아들여질 수는 없다: 겉질량이 목표와 SHOOT_TOL 안이 아니다.
            return Structure(r, m, moi, core_radius if core_radius is not None else r,
                             p_center, p_cmb if p_cmb is not None else p,
                             p_ice_base, phases, v_pore=v_pore, m_above_lab=m_above_lab,
                             p_silicate_max=p_si_max, t_center=t_center,
                             t_cmb=t_cmb if t_cmb is not None else 0.0,
                             t_surface=t, ice_samples=ice_samples, p_surface=p,
                             surface_reached=False)
        raise GridExceeded(
            f"{MAX_STEPS} 걸음(중심 격자 dr 의 {MAX_STEPS / STEPS:.0f} 배 반지름, 여기서는 "
            f"{r / EARTH_RADIUS_M:.1f} R⊕) 안에 표면에 닿지 못했다 — 중심압 "
            f"{p_center / 1e9:.3g} GPa · 중심 온도 {t_center:.0f} K 에서 그 반지름까지 담은 질량이 "
            f"목표의 {m / mass_kg:.3f} 배이고 그 자리의 압력이 {p / 1e5:.3g} bar 다. 외피가 격자가 "
            "닿는 것보다 멀리 부풀어 있다는 뜻이고, 격자의 한계이지 재료의 한계가 아니다.")

    if core_radius is None:
        core_radius = r      # 핵만 있는 천체
        p_cmb = p
        t_cmb = t
    if ice_samples and mat.name in ("h2o", "h2o_liquid", "h2o_hot"):
        # 기둥 꼭대기. 얼음 III·V·VI 구간에서는 녹는곡선이 단열선보다 가파르므로
        # T − T_melt 가 제일 큰 자리가 여기다. 가스 외피가 있으면 마지막 층이 얼음이
        # 아니라서 이 표본을 넣지 않는다 — 다른 층의 점을 얼음이라고 부르지 않는다.
        ice_samples.append((p, t))
    return Structure(r, m, moi, core_radius, p_center, p_cmb, p_ice_base, phases,
                     v_pore=v_pore, m_above_lab=m_above_lab,
                     p_silicate_max=p_si_max, t_center=t_center,
                     t_cmb=t_cmb if t_cmb is not None else 0.0,
                     t_surface=t_surface, ice_samples=ice_samples,
                     p_surface=p_surface, r_ocean_base=r_ocean_base,
                     r_ocean_top=r_ocean_top, ice_x_reached=ice_x_stepped)


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


class Unbound(ValueError):
    """이 중심 온도에서는 외피가 정수압 1 bar 준위를 갖지 못한다.

    괄호가 부동소수점 해상도까지 닫혔는데 한쪽은 외피 없는 암석뿐(질량 부족), 다른 쪽은 격자
    끝까지 가도 표면에 못 닿는 외피(질량 초과)다. 외피 바닥의 온도가 이 질량이 묶을 수 있는
    것보다 높아서 — 등온 대기라면 P(∞)/P_b = exp(−r_b/H) 가 p_stop/P_b 보다 커서 1 bar 가
    무한대에 놓인다 — 사이에 뿌리가 없다. 시험값이 아니라 그 온도의 성질이고, 온도 고리가 받아
    선언된 1 bar 온도가 닿을 수 없음을 말한다."""

    def __init__(self, t_center, mass_kg, rock_only, unbound):
        self.t_center = t_center
        self.rock_only = rock_only
        self.unbound = unbound
        super().__init__(
            f"중심 온도 {t_center:.0f} K 에서 외피가 묶이지 않는다 — 중심압 "
            f"{rock_only.p_center / 1e9:.4g} GPa 에서는 응축상만으로 목표의 "
            f"{rock_only.mass_kg / mass_kg:.4g} 배를 1 bar 에서 담고 외피가 없고, 그 바로 위 "
            f"{unbound.p_center / 1e9:.4g} GPa 에서는 외피가 격자 끝 "
            f"{unbound.radius_m / EARTH_RADIUS_M:.0f} R⊕ 까지 가도 1 bar 에 닿지 못한 채 이미 "
            f"목표의 {unbound.mass_kg / mass_kg:.3g} 배를 담는다 (그 자리 압력 "
            f"{unbound.p_surface / 1e5:.3g} bar).")


class GridExceeded(ValueError):
    """표면에 닿기 전에 걸음 상한이 왔고 질량은 아직 모자란다 — 외피가 격자가 닿는 것보다 멀리
    부풀어 있다. 격자의 한계이지 재료의 한계가 아니고, 온도 고리는 이것을 벽으로 받는다:
    더 뜨거운 시험은 더 부풀 뿐이다."""


class NoCompactRoot(ValueError):
    """이 중심 온도에서 겉질량의 U 자 최소가 목표 위다 — 오른쪽(치밀한) 가지에 뿌리가 없다.
    Unbound 와 같은 종류의 사실이고, 온도 고리가 같은 벽으로 받는다."""


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
                    t_center: float = 0.0, t_pot: float = 0.0,
                    boundary_temperature_jump: float = 0.0,
                    mantle_rock_fraction: float = 0.0) -> tuple[Structure, bool]:
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
    p_stop = getattr(stack[-1][1], "p_floor", 0.0)
    # 중심압의 아래 끝. 바깥 재료가 압력 바닥을 말하면 중심압이 그보다 낮을 수 없다 —
    # 기체 외피에서 실제로 걸린다. 할선의 두 번째 시험점이 그 아래로 내려가면 표 밖이라
    # 거절이 나고, 그건 물리가 아니라 시험값이다.
    lo = max(1.0e2, p_stop)
    hi = min(3.0 * G / (8.0 * math.pi) * mass_kg ** 2 / r0 ** 4 * 4.0, p_ceiling)

    def at(p: float):
        return integrate(p, mass_kg, cmf, imf, core_material, phi0, p_cap, gmf,
                         envelope_z, differentiated, t_center, t_pot,
                         boundary_temperature_jump, mantle_rock_fraction)

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
    # **사다리가 밟은 눈금이 그대로 괄호의 아래끝이 된다.**
    #
    # 표면이 P = 0 이면 겉질량이 중심압에 단조라 아래끝을 아무 데나 둬도 뿌리가 하나다.
    # 기체 외피는 다르다 — 표면이 1 bar 로 고정돼 있으면 중심압이 낮을수록 천체가 부풀어
    # 저밀도 가스가 먼 곳까지 1 bar 를 유지하며 질량을 담으므로, 겉질량이 중심압에 대해
    # **U 자** 를 그린다. 그건 경계조건의 성질이지 결함이 아니고, 1 bar 를 고른 것도 맞다
    # (가스에는 P = 0 인 표면이 없고 발표된 반지름도 그 준위다). 고칠 것은 뿌리 찾기다.
    #
    # 아래끝을 바닥에 두면 괄호가 **최소를 통째로 품고**, 그 안에 뿌리가 둘이라 두 번째
    # 시험점이 답을 정한다. 토성에서 hi × 10⁻³ 은 왼쪽 가지에 떨어져 반지름 650만 km 를
    # 냈다. 그래서 아래끝을 사다리가 이미 밟은 눈금 중 **질량이 목표에 못 미친 마지막
    # 자리** 로 둔다. 사다리는 위로 올라가며 그 눈금들의 질량을 이미 계산했으므로 적분이
    # 더 들지 않고, ×4 라는 눈금 간격이 답을 정하지도 않는다 — 정하는 것은 "최소를
    # 넘긴 뒤" 라는 조건이다.
    good = None                  # 마지막으로 적분이 끝난 시험압
    rung = None                  # 질량이 목표에 못 미친 마지막 눈금 (압력, 질량)
    broke: PhaseGap | None = None
    # **씨앗이 이미 목표를 넘긴 기체 천체.** U 자의 왼쪽 가지(부푼 쪽)에서 출발한 것일 수 있다.
    # 예전에는 사다리가 즉시 멈추고 할선의 둘째 점을 hi × 10⁻³ 에 두어 부푼 뿌리로 갔다 — 5 M⊕
    # 순수 가스 천체가 같은 중심 온도에서 11 R⊕ 와 131 R⊕ 두 답을 번갈아 냈다. 물리적인 쪽은
    # 오른쪽 가지(치밀한 쪽)다: 중심압을 올리면 질량이 늘어나는 구간이고, 발표된 거대행성 반지름은
    # 전부 그쪽이다. 그래서 질량이 줄어드는 동안 위로 오른다 — 목표 아래로 내려가면 그 눈금이
    # rung 이고 기존 사다리가 이어받는다. 최소를 지나서도 목표 아래로 못 내려가면 치밀한 뿌리가
    # 없다는 뜻이고, 그것은 묶이지 않는 외피와 같은 종류의 사실이다.
    if p_stop:
        try:
            st0 = at(hi)
        except PhaseGap:
            st0 = None
        if st0 is not None and st0.mass_kg >= mass_kg:
            # 먼저 내려가 본다. 오른쪽 가지의 뿌리 위에 앉은 씨앗이면(목성·토성 질량의 순수 가스
            # 천체가 그렇다) 내려갈수록 질량이 줄어 목표 아래로 떨어지고, 그 눈금이 rung 이다.
            # 내려갈수록 질량이 **늘면** 왼쪽(부푼) 가지이고, 그때는 위로 올라 최소를 넘긴다.
            prev, p_prev = st0, hi
            rung_found = False
            while p_prev / 4.0 > lo:
                p_dn = p_prev / 4.0
                try:
                    st_dn = at(p_dn)
                except PhaseGap:
                    break
                if st_dn.mass_kg < mass_kg:
                    rung = (p_dn, st_dn.mass_kg)
                    rung_found = True
                    break
                if st_dn.mass_kg > prev.mass_kg:
                    break                    # 내려가는데 질량이 는다. 부푼 가지다
                prev, p_prev = st_dn, p_dn
            if not rung_found:
                prev, p_prev = st0, hi
                while True:
                    nxt_p = min(p_prev * 4.0, p_ceiling)
                    try:
                        st1 = at(nxt_p)
                    except PhaseGap:
                        break                # 위가 막혔다. 기존 사다리가 좁힌다
                    if st1.mass_kg < mass_kg:
                        hi = nxt_p           # 최소를 지나 목표 아래로 내려왔다. 여기가 rung 이 된다
                        break
                    if st1.mass_kg >= prev.mass_kg or nxt_p >= p_ceiling:
                        raise NoCompactRoot(
                            f"중심 온도 {t_center:.0f} K 에서 치밀한 뿌리가 없다 — 중심압 {p_prev / 1e9:.4g} 에서 "
                            f"{nxt_p / 1e9:.4g} GPa 로 올려도 겉질량이 목표의 {prev.mass_kg / mass_kg:.3g} 배에서 "
                            f"{st1.mass_kg / mass_kg:.3g} 배로 줄지 않는다. 1 bar 에 묶인 외피의 겉질량이 중심압에 "
                            "U 자를 그리는데 그 최소가 목표 위에 있어서, 남는 해는 부푼 왼쪽 가지뿐이고 그것은 "
                            "발표된 어떤 거대행성도 앉아 있지 않은 가지다.")
                    prev, p_prev = st1, nxt_p
    while True:
        try:
            st = at(hi)
        except PhaseGap as gap:
            if gap.temperature_k:
                # **온도가 막은 것은 압력 괄호로 못 고친다.** 중심압을 낮춰도 그 층의
                # 온도는 중심 온도가 정하므로, 좁히는 대신 위로 올려 보낸다 — 바깥의
                # 온도 고리가 중심 온도를 올려 다시 잡는다.
                raise
            if good is None:
                raise            # 첫 시험부터 깨진다. 좁힐 바닥이 없다
            broke = gap
            hi, st = _narrow_bracket(good, hi, at, mass_kg)
            break
        good = hi
        if st.mass_kg >= mass_kg:
            break
        # 목표에 못 미치는 **마지막** 눈금을 들고 간다. 질량이 U 자를 그려도 마지막인
        # 것이 중요하다 — 내려가는 가지에서 목표 아래로 떨어진 눈금이 있었다면 그 뒤의
        # 눈금들도 최소까지 계속 목표 아래이므로, 마지막은 언제나 최소의 오른쪽,
        # 곧 질량이 중심압에 단조증가하는 구간에 있다.
        rung = (hi, st.mass_kg)
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
                        envelope_z, differentiated, t_center, t_pot,
                        boundary_temperature_jump, mantle_rock_fraction)
    if abs(st.mass_kg - mass_kg) / mass_kg < SHOOT_TOL:
        return st, True
    if p_stop and rung is not None:
        # 기체가 바깥에 있다. 사다리가 밟은 눈금을 아래끝으로 쓴다. 그 눈금의 질량이
        # 이미 있으므로 할선의 두 점이 **공짜** 이고, 이 구간 안에서는 질량이 중심압에
        # 단조증가하므로 뿌리가 하나다. st 는 위쪽 점(hi)의 것이라 x1 과 짝이 맞는다.
        lo = rung[0]
        x0, y0 = math.log(rung[0]), math.log(rung[1] / mass_kg)
        x1, y1 = math.log(hi), math.log(st.mass_kg / mass_kg)
    else:
        x0, y0 = math.log(hi), math.log(st.mass_kg / mass_kg)
        # 응축상. 표면이 P = 0 이라 질량이 중심압에 단조이고, 아래끝이 어디든 뿌리가
        # 하나다. 예전 경로를 그대로 둬서 앵커가 비트까지 같게 유지한다.
        x1 = math.log(max(lo, hi * 1e-3))
        st = integrate(math.exp(x1), mass_kg, cmf, imf, core_material, phi0, p_cap,
                        gmf, envelope_z, differentiated, t_center, t_pot,
                        boundary_temperature_jump, mantle_rock_fraction)
        y1 = math.log(st.mass_kg / mass_kg)
    last_short = None            # 질량이 모자란 마지막 구조 (외피 없는 암석)
    for _ in range(SHOOT_ITERS):
        if abs(st.mass_kg - mass_kg) / mass_kg < SHOOT_TOL:
            return st, True
        if st.mass_kg < mass_kg:
            lo = math.exp(x1)
            last_short = st
        else:
            hi = math.exp(x1)
            # **괄호가 닫혔는데 뿌리가 없다.** 아래쪽은 표면에 닿은 채 질량이 모자라고 위쪽은
            # 표면에 못 닿은 채 질량이 넘친다면, 그 사이의 어떤 중심압도 겉질량을 목표에 맞추지
            # 못한다 — 외피가 이 온도에서 묶이지 않는 것이고, 시험값의 문제가 아니다.
            if (not st.surface_reached and last_short is not None
                    and hi / lo - 1.0 < 1e-9):
                raise Unbound(t_center, mass_kg, last_short, st)
        if y1 != y0:
            x2 = x1 - y1 * (x1 - x0) / (y1 - y0)
        else:
            x2 = 0.5 * (math.log(lo) + math.log(hi))
        if not (math.log(lo) <= x2 <= math.log(hi)):
            x2 = 0.5 * (math.log(lo) + math.log(hi))
        x0, y0 = x1, y1
        x1 = x2
        st = integrate(math.exp(x1), mass_kg, cmf, imf, core_material, phi0, p_cap,
                    gmf, envelope_z, differentiated, t_center, t_pot,
                    boundary_temperature_jump, mantle_rock_fraction)
        y1 = math.log(st.mass_kg / mass_kg)
    return st, False


# 온도를 맞추는 바깥 고리의 횟수와 허용오차. 단열선이 앵커에 거의 선형이라
# 두세 번이면 붙는다 — 밀도가 온도에 몇 % 만 반응하기 때문이다.
# 온도 고리의 통과 횟수. 응축상은 두세 번이면 붙어서 6 으로 충분했다. 기체 외피는
# 다르다 — 표면이 1 bar 에 있고 단열선이 그 자리에서 가파르므로 비례 갱신의 수렴 인자가
# 0.3 쯤이고, 목성이 6 회에서 1.5 % 를 남긴 채 끝났다. 붙는 천체는 T_TOL 에서 먼저
# 빠져나가므로 이 상한을 올려도 답이 안 바뀐다.
T_PASSES = 14
T_TOL = 1e-6
# 표면 온도가 선언값에 이만큼 안에 들어와야 **온도 경계조건이 수렴한 것** 이다.
# 2026-08-28 까지 shoot() 이 돌려주는 converged 는 압력 사격의 것뿐이었고, 온도 고리가
# T_PASSES 를 다 쓰고도 못 맞추면 아무 표시 없이 나갔다. 도달 불가능한 표면 온도를 쫓다가
# 가짜 가지로 걸어간 해가 converged=True 배지를 달고 나온 일반 원인이 그 구멍이다.
T_SURFACE_TOL = 1e-3
# 온도 고리를 비례 갱신에서 좁히기로 바꾸는 문턱. 어긋남이 이보다 크면서 한 진동 전보다 줄지
# 않았을 때만 바꾼다 — 수렴 근처의 작은 흔들림으로 갈래를 바꾸면 앵커가 움직인다.
T_DIVERGENCE_MIN = 0.05
# 한 진동(두 걸음) 동안 어긋남이 이 배수 아래로 줄지 않으면 비례 갱신이 너무 느리다 — 지수 n 이
# 2 에 가까우면 (1 − n)² ≈ 0.8–1 로 줄어 열네 걸음으로 못 붙는다 (GJ 1214 b 가스 5 %). 앵커는
# 한 진동에 0.01–0.1 배로 준다 (목성 0.70 → 0.37 → 0.08 → 0.022, 천왕성 0.067 → 0.006 → 0.0004).
T_CONTRACTION_MIN = 0.5
# 온도 괄호잡기의 시도 횟수. 한 번에 1.6배씩 올린다.
T_BRACKET_TRIES = 12


def shoot(mass_kg: float, cmf: float, imf: float,
          core_material: str, phi0: float = 0.0,
          p_cap: float | None = None, gmf: float = 0.0,
          envelope_z: float = 0.0, differentiated: bool = True,
          potential_temperature: float | None = None,
          boundary_temperature_jump: float = 0.0,
          mantle_rock_fraction: float = 0.0) -> tuple[Structure, bool]:
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
    kw = {"boundary_temperature_jump": boundary_temperature_jump,
          "mantle_rock_fraction": mantle_rock_fraction}
    if not potential_temperature:
        return _shoot_pressure(*args, **kw)
    t_pot = float(potential_temperature)
    t_c = t_pot * 2.0        # 첫 추측. 비율로 다시 재므로 값 자체는 중요하지 않다

    # 직전 통과의 중심압을 괄호의 출발점으로 물려주는 것을 재봤고, 되돌렸다. 27 % 를
    # 벌지만 할선의 경로가 바뀌어 수렴점이 마지막 비트에서 달라지고, 그러면 "기준
    # 포텐셜 온도에서는 답이 비트까지 안 움직인다" 는 항등식이 깨진다. 그 항등식이
    # 속도보다 무겁다.
    def attempt(t_try: float) -> tuple[Structure, bool, float]:
        """중심 온도 하나로 사격한다. 온도 바닥에 걸리면 올려서 다시 잡는다.

        **온도에도 괄호잡기가 필요하다.** 압력 쪽에서 배운 것과 같은 자리다 — 중심
        온도를 낮게 잡으면 바깥으로 갈수록 단열선이 내려가 어떤 층의 온도 하한을
        뚫는데, 그건 이 천체가 안 풀린다는 뜻이 아니라 **시험값이 낮았다** 는 뜻이다.
        중심 온도를 올리면 프로파일 전체가 올라가므로 답이 그 위에 있다.
        **양쪽으로 넓힌다.** 수소-헬륨 표가 들어오면서 아래 벽만이 아니라 위 벽도
        생겼다. 거절이 어느 쪽 벽인지는 PhaseGap 이 말하고, 방향이 뒤집히면 두 벽 사이에
        답이 없다는 뜻이므로 거기서 멈춘다 — 계속 넓히면 두 벽 사이를 오간다."""
        t_now = t_try
        last = None
        for _ in range(T_BRACKET_TRIES):
            try:
                got, ok = _shoot_pressure(*args, t_center=t_now, t_pot=t_pot, **kw)
                return got, ok, t_now
            except PhaseGap as gap:
                if not gap.temperature_k:
                    raise        # 온도가 아니라 압력이 막았다. 그건 진짜다
                if last is not None and last != gap.too_cold:
                    raise        # 양쪽 벽에 다 부딪혔다. 넓혀서 될 일이 아니다
                last = gap.too_cold
                t_now = t_now * 1.6 if gap.too_cold else t_now / 1.6
        got, ok = _shoot_pressure(*args, t_center=t_now, t_pot=t_pot, **kw)
        return got, ok, t_now

    # **괄호가 옮긴 온도를 그대로 받아 온다.** 받지 않으면 바깥 고리가 자기가 요청한
    # 온도로 비율을 다시 재는데, 실제로 적분된 것은 괄호가 옮긴 온도라 매 통과가 같은
    # 배수만큼 틀리고 고리가 수렴하지 않는다. 통과 횟수를 6 에서 14 로 올렸더니 목성은
    # 붙고 토성은 +2.09 % 에서 +7.06 % 로 흔들린 것이 이 자리였다.
    st, converged, t_c = attempt(t_c)
    # **비례 갱신이 발산하는 천체가 있다.** T_c·T_pot/T_surf 는 T_surf ∝ T_c 를 놓는데, 얇은 외피가
    # 무거운 핵 위에 있으면 지수가 2 를 넘는다 — 외피 바닥이 핵 단열선을 그대로 타고 1 bar 온도는
    # 그 위에서 외피 두께까지 같이 바뀐다 (GJ 1214 b 가스 2 % 에서 2.3). 지수 n 의 비례 갱신은
    # 오차를 (1 − n) 배 하므로 n > 2 면 진동이 커지고, 거대행성(n ≈ 0.7, 오차가 0.3 배씩 준다)에서는
    # 그냥 붙는다. 그래서 **진동이 줄지 않을 때만** 갈래를 바꾼다: 두 걸음 전보다 어긋남이 줄지 않았거나
    # 묶이지 않는 벽에 닿았으면, 그때부터 양쪽 점 사이를 로그-로그 regula falsi 로 좁힌다. 앵커
    # 넷(목성·토성 둘·천왕성·해왕성)은 매 걸음 줄어들므로 이 갈래를 한 번도 타지 않는다 — 비트까지
    # 같다는 것을 그 경로로 보장한다.
    wall = None                  # 외피가 묶이지 않은 가장 낮은 중심 온도
    wall_why = ""                # 그 온도에서 왜 묶이지 않았는가 (사다리의 문장)
    lo = hi = None               # (log T_c, log T_surf/T_pot): 아래쪽(차다) · 위쪽(뜨겁다)
    devs: list[float] = []
    bracketed = False
    passes = T_PASSES
    # 가장 잘 붙은 시험값. 1 bar 온도는 중심 온도에 대해 격자 위상의 잔여 요철(해왕성에서 ±0.02 K,
    # 온도를 걸음마다 한 번의 ∇_ad 로 나르는 1차 오차)을 갖고 있어서, 어긋남이 허용오차 안으로
    # 들어온 뒤에도 비례 갱신이 요철의 국소 기울기(n ≈ 2.5)를 타고 다시 벌어질 수 있다. 그때 마지막
    # 시험값을 들고 나가면 붙었던 해가 converged=False 로 나간다 — 2026-08-30 에 해왕성이 3.5e-5 까지
    # 붙고 나서 열두 걸음 동안 1.5 배씩 벌어져 1.25e-3 으로 나갔다. 매 걸음 줄어드는 앵커는 마지막이
    # 곧 최선이라 이 갈래를 타지 않는다.
    best = None                  # (어긋남, Structure, 사격 수렴, 중심 온도)

    def remember(got, ok, t_now):
        nonlocal best
        if got.t_surface <= 0.0:
            return
        d = abs(got.t_surface / t_pot - 1.0)
        if best is None or d < best[0]:
            best = (d, got, ok, t_now)

    def note(t_now, got):
        nonlocal lo, hi
        if got.t_surface <= 0.0:
            return
        pt = (math.log(t_now), math.log(got.t_surface / t_pot))
        if pt[1] < 0.0:
            if lo is None or pt[0] > lo[0]:
                lo = pt
        elif hi is None or pt[0] < hi[0]:
            hi = pt

    note(t_c, st)
    remember(st, converged, t_c)
    while passes > 0:
        passes -= 1
        if st.t_surface <= 0.0:
            break            # 열 상수가 없는 재료뿐이다. 온도가 흐르지 않는다
        devs.append(abs(st.t_surface / t_pot - 1.0))
        # 어긋남이 **크면서** 한 진동 전보다 줄지 않았을 때만이다. 수렴 근처의 1e-4 급 흔들림은
        # 발산이 아니라 반올림이고, 거기서 갈래를 바꾸면 앵커의 마지막 비트가 움직인다 (2026-08-29
        # 에 천왕성·해왕성이 그렇게 움직였다).
        if (len(devs) >= 3 and devs[-1] >= T_CONTRACTION_MIN * devs[-3]
                and devs[-1] > T_DIVERGENCE_MIN):
            bracketed = True
        if bracketed and lo is not None and (hi is not None or wall is not None):
            if hi is not None:
                x_lo, y_lo = lo
                x_hi, y_hi = hi
                x = x_lo - y_lo * (x_hi - x_lo) / (y_hi - y_lo)
                if wall is not None:
                    x = min(x, 0.5 * (x_lo + math.log(wall)))
            else:
                x = 0.5 * (lo[0] + math.log(wall))
            nxt = math.exp(x)
            if wall is not None and wall / math.exp(lo[0]) - 1.0 < 1e-3:
                break        # 벽에 붙었다. 더 올릴 온도가 없다
        else:
            nxt = t_c * t_pot / st.t_surface
            if wall is not None and nxt >= wall:
                nxt = math.sqrt(t_c * wall)
        done = abs(nxt / t_c - 1.0) < T_TOL
        try:
            got, ok, t_now = attempt(nxt)
        except (Unbound, NoCompactRoot, GridExceeded) as why:
            wall, wall_why = nxt, str(why)
            bracketed = True
            passes += 1      # 벽을 찾은 걸음은 통과 횟수에서 빼 준다
            if passes > 3 * T_PASSES:
                break
            continue
        stuck = abs(t_now / t_c - 1.0) < 1e-9 if t_c else False
        st, converged, t_c = got, ok, t_now
        note(t_c, st)
        remember(st, converged, t_c)
        if stuck:
            break            # 괄호가 표의 온도 벽에서 같은 온도로 되돌렸다. 더 갈 데가 없다
        if bracketed is True and passes == 0 and not _surface_temperature_met(st, t_pot):
            passes = T_PASSES    # 좁히는 갈래에는 한 벌 더, **한 번만** 준다
            bracketed = "extended"
        if done:
            break
    if (best is not None and not _surface_temperature_met(st, t_pot)
            and best[0] < T_SURFACE_TOL):
        # 마지막 시험값은 벌어졌지만 그 전에 붙은 시험값이 있다. 그것이 답이다 (위 best 주석).
        _d, st, converged, t_c = best
    if wall is not None and not _surface_temperature_met(st, t_pot):
        # **선언된 1 bar 온도에 닿는 중심 온도가 없다.** 벽 아래의 가장 뜨거운 묶인 해와 벽을 둘 다
        # 들고 나간다 — 버린 시험값이 아니라 실제로 도달한 두 상태다.
        raise ValueError(
            f"선언된 포텐셜 온도 {t_pot:.0f} K 에 닿는 해가 없다. 외피가 묶이는 가장 뜨거운 중심 온도 "
            f"{t_c:.0f} K 에서 반지름 {st.radius_m / EARTH_RADIUS_M:.2f} R⊕ · 1 bar 온도 "
            f"{st.t_surface:.0f} K 이고, 그 위 {wall:.0f} K 에서는 외피가 묶이지 않는다: {wall_why} "
            "1 bar 에서 출발한 단열선이 이 질량이 묶을 수 있는 것보다 뜨겁다는 뜻이다 — 실제 "
            "서브넵튠은 복사층이 깊은 단열선을 더 차게 두는데 이 레시피에는 복사층이 없으므로, "
            "선언을 낮추거나(복사-대류 경계의 온도) 그 층이 들어와야 한다.")
    return st, converged and _surface_temperature_met(st, t_pot)


def _surface_temperature_met(st, t_pot: float) -> bool:
    """표면 온도가 선언값에 닿았는가. 못 닿았으면 그 해는 수렴한 것이 아니다.

    압력 사격이 붙었다는 것과 경계조건이 다 맞았다는 것은 다른 말이고, 둘을 한 배지로
    내보내면 후자가 안 맞은 해가 전자의 배지를 달고 나간다."""
    if st.t_surface <= 0.0:
        return True          # 열 상수가 없는 재료뿐이다. 맞출 경계조건이 없다
    return abs(st.t_surface / t_pot - 1.0) < T_SURFACE_TOL


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

# **2026-08-28 에 이 갈래의 앵커가 둘에서 셋으로 늘었다.** 폴리트로프였을 때는 앵커가
# 목성(맞음)과 토성(틀림) 둘뿐이었고, 그 사이를 강등 구간으로 둔 이유는 잔차가 어느 쪽인지
# 말할 근거가 없어서가 아니라 **n = 1 이 어떤 거대행성에나 같은 답을 냈기 때문** 이다
# (R = √(πK/2G) 에 질량도 조성도 안 들어간다). 그 전제가 사라졌다 — 표는 (P, T) 의
# 함수이고 질량·조성·온도에 전부 반응한다.
#
# 그래서 "목성보다 가벼우면 analog" 라는 규칙을 **지운다.** 대신 강등의 근거를 실제로
# 남아 있는 것에 건다: 이 갈래가 기대는 선언(포텐셜 온도)과, 굳힌 창의 가장자리다.
GIANT_ANCHORS = (
    ("목성", 317.828, -0.83),
    ("토성 (Z = 0)", 95.159, +7.06),
    ("천왕성", 14.536, +5.49),
)

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
# **2026-08-29 부터 판정이 밀도에 들어간다.** 2026-08-27 에는 판정만 내고 밀도는 고체상의
# 것으로 뒀다 — 액체 상태방정식과 적분기 안의 상분율이 이 범위 밖이었다. 둘 다 들어왔다:
# 액체 물은 eos.py 의 h2o_liquid (SeaFreeze water1, Bollengier+ 2019) 이고, integrate() 가
# 걸음마다 얼음 기둥의 국소 (P, T) 를 녹는곡선에 대서 사다리와 액체를 갈아 끼운다. 그래서
# 아래 판정은 적분이 실제로 밟은 상을 다시 읽는 것이고, molten 인 해의 반지름과 C/MR² 는
# 바다를 **담은** 답이다. 바다의 두께는 포텐셜 온도 선언이 정하므로 (열 이력이 이 레시피에
# 없다) 그 해는 선언에 기댄다 — core_state 가 핵 쪽 경계 온도를 받는 것과 같은 자리다.
#
# 표본은 기둥 바닥·중간·꼭대기다. 얼음 III·V·VI 구간에서 녹는곡선(약 52 K/GPa)이
# 단열선(약 21 K/GPa)보다 가파르므로 T − T_melt 의 최대는 기둥 **꼭대기** 에 있고,
# 얼음 Ih 은 녹는곡선이 내려가므로 반대로 바닥에 있다. 양쪽을 다 찍는다.
ICE_STATE_NONE = "none"
ICE_STATE_SOLID = "solid"
ICE_STATE_MOLTEN = "molten"
ICE_STATE_UNDECIDED = "undecided"


def _ice_verdict(st, potential_temperature) -> tuple[str, str]:
    """얼음 기둥이 녹았는가. (상태, 한 줄 설명) 을 돌려준다.

    액체인 자리가 있었으면 적분이 그것을 밟았으므로 그 사실이 판정이다. 표본은 못 본 구간
    (녹는곡선이 닿지 않는 압력)을 이름 대고, 고체 판정의 여유를 적는 데 쓴다. 기둥의
    꼭대기와 바닥은 **어느 상을 왜 골랐는지** 를 곡선 이름과 거리로 말한다 (water_phase_name)
    — 상이 조용히 갈리는 일이 이 항목이 지운 결함이다."""
    if not st.ice_samples:
        return ICE_STATE_NONE, ""
    if not potential_temperature:
        return (ICE_STATE_UNDECIDED,
                "**얼음 기둥의 고체·액체를 판정하지 않았다** — 포텐셜 온도가 선언되지 "
                "않아 이 해에는 온도가 흐르지 않는다. 녹는곡선은 있고(IAPWS R14-08(2011), "
                "Reinhardt+ 2022) 압력도 있으니, 온도를 선언하면 이 행은 판정으로 바뀐다.")
    samples = sorted((p_pa, t_k) for p_pa, t_k in st.ice_samples if p_pa > 0.0 and t_k > 0.0)
    if not samples:
        return ICE_STATE_NONE, ""

    def describe(p_pa: float, t_k: float) -> str:
        verdict, label, why = water_phase_name(p_pa, t_k)
        off_ladder = ("" if verdict == "liquid" or (t_k < ICE_VII_X_T_MAX
                                                     and p_pa <= MATERIALS["h2o"].p_max)
                      else "; 사다리의 적합 밖이라 밀도는 Mazevet+ 2019 가 냈다")
        return f"{p_pa / 1e9:.1f} GPa · {t_k:.0f} K → **{label or '판정 없음'}** ({why}{off_ladder})"

    (p_top, t_top), (p_base, t_base) = samples[0], samples[-1]
    ends = f" 기둥 꼭대기 {describe(p_top, t_top)}; 바닥 {describe(p_base, t_base)}."
    unseen = min((p_pa for p_pa, t_k in samples if water_phase_name(p_pa, t_k)[0] == "undecided"),
                 default=0.0)
    blind = ("" if unseen == 0.0 else
             f" 기둥의 {unseen / 1e9:.1f} GPa 위쪽은 녹는곡선이 닿지 않는다 — Reinhardt+ 2022 의 "
             f"액체선이 {REINHARDT_P_MAX / 1e9:.1f} GPa 에서 끝나고, 그 위의 유체·초이온은 가르지 "
             "않았다.")
    if st.ocean_thickness_m > 0.0:
        shell = st.ice_shell_thickness_m / 1e3
        return (ICE_STATE_MOLTEN,
                f"**얼음 기둥에 바다가 있다** — 두께 {st.ocean_thickness_m / 1e3:.0f} km, "
                + (f"그 위의 얼음 껍질 {shell:.0f} km" if shell > 0.0 else "표면까지 액체")
                + ". 국소 (P, T) 가 IAPWS R14-08(2011) 의 녹는곡선 위인 자리마다 적분기가 "
                "액체 물의 상태방정식(SeaFreeze water1, Bollengier+ 2019)을 썼으므로 반지름과 "
                "C/MR² 는 바다를 담은 값이다. **두께는 포텐셜 온도 선언이 정한다** — 껍질의 "
                "두께를 정하는 열 이력이 이 레시피에 없어서, 그 선언이 바뀌면 바다도 바뀐다."
                + ends + blind)
    if "h2o_hot" in st.phases:
        return (ICE_STATE_MOLTEN,
                "**얼음층이 유체다** — 국소 (P, T) 가 녹는곡선 위인 자리마다 적분기가 뜨거운 물의 "
                "적합(Mazevet+ 2019)을 썼다. 바다가 아니라 유체 맨틀이고, 반지름은 그 밀도의 값이다. "
                "곡선은 실험이 아니라 시뮬레이션(Reinhardt+ 2022)이라 등급은 analog 다."
                + ends + blind)
    ice = MATERIALS["h2o"]
    best_margin = None
    best = None
    for p_pa, t_k in samples:
        t_m = ice.t_melt(p_pa) if p_pa <= REINHARDT_P_MAX else None
        if t_m is None:
            continue
        margin = t_k - t_m
        if best_margin is None or margin > best_margin:
            best_margin, best = margin, (p_pa, t_k, t_m)
    if best_margin is None:
        return (ICE_STATE_UNDECIDED,
                "**얼음 기둥의 고체·액체를 판정하지 않았다** — 기둥 전체가 이 레시피가 "
                f"들고 있는 녹는곡선의 압력 구간({REINHARDT_P_MAX / 1e9:.1f} GPa) 위다. 드는 측정은 "
                "Millot+ 2018 의 점 하나(190 GPa · ~5000 K)뿐이고, 재료는 가용성으로 골랐다 — "
                "사다리의 적합 천장(1800 K) 아래면 사다리, 위면 Mazevet+ 2019." + ends)
    p_pa, t_k, t_m = best
    where = f"{p_pa / 1e6:.1f} MPa 에서 T {t_k:.1f} K · 녹는점 {t_m:.1f} K"
    if best_margin > 0.0:
        # 표본은 걸음 출발점의 (P, T) 이고 적분기가 같은 판정으로 상을 골랐으므로, 여기 오면
        # 적분이 액체를 밟았어야 한다. 오면 배선이 끊긴 것이다 — 조용히 넘기지 않는다.
        return (ICE_STATE_MOLTEN,
                f"**얼음 기둥이 녹는데 적분은 액체를 밟지 않았다** — {where} 로 "
                f"{best_margin:+.1f} K 다. 판정과 적분이 같은 함수를 써야 하는데 어긋났다. "
                "결함이다." + ends + blind)
    if unseen != 0.0:
        # 본 자리는 전부 고체인데 못 본 자리가 있다. **'고체' 라고 말하면 안 된다** —
        # 하한이 한쪽만 묶는 것과 같은 규율이고, core_state 가 같은 규칙을 쓴다.
        return (ICE_STATE_UNDECIDED,
                f"**얼음 기둥의 고체·액체를 판정하지 않았다.** 본 자리는 전부 고체다 — "
                f"제일 녹기 쉬운 자리가 {where} 로 {best_margin:+.1f} K 다. 그런데 기둥의 "
                f"{unseen / 1e9:.1f} GPa 위쪽은 녹는곡선이 닿지 않아 보지 못했고, 못 본 "
                "구간이 있으면 '고체' 는 말할 수 없다. 'molten' 은 한 자리만 넘어도 참이지만 "
                "'solid' 는 전부를 봐야 참이다." + ends)
    src = ("IAPWS R14-08(2011), 불확도 3 %" if p_pa <= 20.6e9
           else "IAPWS R14-08(2011) 아래 · Reinhardt+ 2022 (analog) 위")
    return (ICE_STATE_SOLID,
            f"얼음 기둥이 고체다 — 제일 녹기 쉬운 자리가 {where} 로 {best_margin:+.1f} K "
            f"다 ({src})." + ends)


# 아직 거절하는 유체 천체. 각각 무엇이 있어야 답이 바뀌는지를 거절 이유가 말한다.
FLUID_CLASSES = ("brown_dwarf", "star")

# 서브넵튠. 2026-08-29 까지 위 목록에 있었고 "가스질량분율을 주면 적분 자체는 돈다" 고 적혀
# 있었는데, 재보니 돌지 않았다 — 외피 바닥의 표 영역 이탈을 표면으로 오인하는 결함이 철 천장
# 거절로 나왔다 (sub-neptune-context-notes.md). 결함을 고치고 나서 목록에서 뺐다. 가스질량분율은
# **선언** 이다: 나이와 항성 조사량(광증발)이 정하고 이 레시피에 그 둘이 없다 — ice_allowed ·
# tidal_heating · initial_porosity · envelope_z · potential_temperature · core_cmb_temperature
# 와 같은 일곱 번째 선언이고, 등급을 같은 이유로 내린다.
SUB_NEPTUNE_CLASSES = ("sub_neptune",)

# 얼음거대행성. 2026-08-27 까지 위 목록에 있었고, 뜨거운 물 상태방정식이 들어오면서
# 나왔다. 2026-08-30 까지는 이 목록이 얼음층의 재료(h2o_hot)를 통째로 골랐다 — 지금은
# 국소 (P, T) 가 녹는곡선(Reinhardt+ 2022, 52.4 GPa 까지)에 대서 고르고, 이 목록은 온도
# 선언과 얼음 존재를 요구하는 데만 쓰인다.
ICE_GIANT_CLASSES = ("ice_giant",)


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
          potential_temperature: float | None = None,
          boundary_temperature_jump: float = 0.0,
          mantle_rock_fraction: float = 0.0) -> Result:
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
              "potential_temperature": potential_temperature,
              "boundary_temperature_jump": boundary_temperature_jump,
              "mantle_rock_fraction": mantle_rock_fraction}

    if body_class in FLUID_CLASSES:
        why = {
            "brown_dwarf": ("중수소가 탄다. 13 M_J 위는 광도가 시간에 따라 변하고 "
                            "(Spiegel+ 2011), 이 레시피에는 그 열이력이 없다 — 등온 "
                            "폴리트로프로 갈색왜성을 푸는 것은 나이를 무시하는 것이다."),
            "star": ("수소가 탄다. 별의 NMoI 는 이 레시피가 아니라 n = 3/2 폴리트로프의 "
                     "발표값 0.205 에서 오고 (Chandrasekhar 1939), 그 가지는 "
                     "body_figure 에 따로 있다."),
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
            "금속** 한 쌍뿐이고, 얼음은 그 규칙에 들어갈 수 없다 — 물이 규산염에 섞이는 것은 "
            "혼합이 아니라 **반응**(수화 광물은 제 밀도·제 부피 변화·제 열을 갖는다)이고, "
            "완전히 섞이지도 갈리지도 않은 **부분 분화**(Callisto 형)를 만드는 것은 **물이 어디까지 "
            "갔는가** 라는 수송 이력이라, 문헌은 이것을 정수압 풀이에 넘기는 조성이 아니라 "
            "열진화의 한 단계로 다룬다 (Malamud & Prialnik 2015; interior-core.md C7). "
            "얼음질량분율과 가스질량분율을 0 으로 두면 이 천체는 풀린다.",
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

    envelope_classes = GAS_GIANT_CLASSES + ICE_GIANT_CLASSES + SUB_NEPTUNE_CLASSES
    if gmf > 0 and body_class is not None and body_class not in envelope_classes:
        return out_of_domain(
            RECIPE, VERSION,
            f"가스질량분율 {gmf} 를 받았는데 body_class 가 '{body_class}' 다. "
            f"수소-헬륨 외피를 붙이는 것은 {' 또는 '.join(envelope_classes)} 로 "
            "선언된 천체에만 한다 — 선언과 조성이 어긋나면 조용히 엉뚱한 천체를 푼다.",
            inputs=inputs, refs=REFS)
    if body_class in SUB_NEPTUNE_CLASSES and gmf <= 0.0:
        return out_of_domain(
            RECIPE, VERSION,
            f"'{body_class}' 인데 가스질량분율이 {gmf} 다. 이 클래스를 만드는 것이 그 외피이고, "
            "그 분율은 나이와 항성 조사량(광증발)이 정하므로 이 레시피가 도출하지 않는다 — "
            "선언하면 풀린다. 0 이면 암석 행성이고 body_class 를 rocky 로 두는 쪽이다.",
            inputs=inputs, refs=REFS)

    # ── 두 선언 (C5): 얼음 맨틀 위 열경계층의 온도 점프, 얼음 맨틀의 암석 분율 ──
    # 둘 다 형성과 열 이력이 정하고 이 레시피가 도출하지 않는다 — gas_mass_fraction 과 같은 종류.
    if boundary_temperature_jump < 0.0 or not 0.0 <= mantle_rock_fraction < 1.0:
        return out_of_domain(
            RECIPE, VERSION,
            f"선언이 범위 밖이다 — 열경계층 점프 {boundary_temperature_jump} K (0 이상), 맨틀 암석 "
            f"분율 {mantle_rock_fraction} ([0, 1)).",
            inputs=inputs, refs=REFS)
    if (boundary_temperature_jump > 0.0 or mantle_rock_fraction > 0.0) and imf <= 0.0:
        return out_of_domain(
            RECIPE, VERSION,
            "열경계층 점프와 맨틀 암석 분율은 얼음 맨틀의 선언인데 얼음질량분율이 0 이다.",
            inputs=inputs, refs=REFS)
    if boundary_temperature_jump > 0.0 and (gmf <= 0.0 or not potential_temperature):
        return out_of_domain(
            RECIPE, VERSION,
            "열경계층 점프는 얼음 맨틀과 기체 외피 사이의 온도 차다 — 외피(gas_mass_fraction)와 "
            "선언된 온도가 있어야 그 자리가 있다.",
            inputs=inputs, refs=REFS)
    if mantle_rock_fraction > 0.0 and not potential_temperature:
        return out_of_domain(
            RECIPE, VERSION,
            "맨틀 암석 분율은 온도가 흐르는 얼음 맨틀의 선언이다 — 혼합의 단열 기울기가 c_P 가중이라 "
            "등온 경로에는 정의되지 않는다. 포텐셜 온도를 선언하면 풀린다.",
            inputs=inputs, refs=REFS)

    # 얼음층의 재료는 여기서 고르지 않는다 — 적분기가 걸음마다 국소 (P, T) 를 녹는곡선에 댄다.
    # 얼음거대행성에 남은 클래스 조건은 둘뿐이다: 온도가 선언돼야 하고, 얼음이 있어야 한다.
    ice_giant = body_class in ICE_GIANT_CLASSES
    if ice_giant and not potential_temperature:
        return out_of_domain(
            RECIPE, VERSION,
            "얼음거대행성은 등온으로 풀 수 없다. 이 클래스의 얼음층은 녹는곡선 위의 "
            "유체·초이온 물이고 (Mazevet+ 2019), 그 적합은 P(ρ,T) 가 통째로 "
            "하나라 온도가 인자다. 게다가 그 자리에서 온도가 밀도를 크게 움직인다 — "
            "같은 압력에서 2000 K 와 5700 K 사이에 30 GPa 에서 14 %, 800 GPa 에서 5 % "
            "다. 포텐셜 온도를 선언하면 풀린다.",
            inputs=inputs, refs=REFS)
    if ice_giant and imf <= 0.0:
        return out_of_domain(
            RECIPE, VERSION,
            f"'{body_class}' 인데 얼음질량분율이 {imf} 다. 이 클래스를 이름 그대로 "
            "만드는 것이 그 층이므로, 얼음이 없으면 얼음거대행성이 아니다.",
            inputs=inputs, refs=REFS)

    try:
        st, converged = shoot(mass_earth * EARTH_MASS_KG, cmf, imf, core_material,
                              initial_porosity, porosity_cap, gmf,
                              envelope_z, differentiated, potential_temperature,
                              boundary_temperature_jump, mantle_rock_fraction)
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
    if st.ocean_thickness_m > 0.0:
        bounds.append(f"바다 {st.ocean_thickness_m / 1e3:.0f} km · 얼음 껍질 "
                      f"{st.ice_shell_thickness_m / 1e3:.0f} km")
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
            f"**반지름 {radius:.2f} R⊕ 는 온도 갈래가 5 % 안에서 맞는 구간({UNTERBORN_TCMB_MAX_R:.2f} R⊕) "
            "밖이다.** 앵커는 둘이고 서로 어긋난다 — Unterborn+ 2019 eq. 7 에는 여기 단열선이 낮게 흐르고 "
            "(1.06 R⊕ 에서 −5.6 %, 1.22 R⊕ 에서 −9.5 %, 1.46 R⊕ 에서 −17 %), Noack & Lasbleis 2020 "
            "eq. (22) 에는 0.8 ~ 2 M⊕ 전 구간에서 −2.2 ~ −0.8 % 로 붙는다. 두 발표 추정치끼리 1 → 2 M⊕ 에서 "
            "4.4 ~ 9.7 % 어긋나고 엔진은 그 사이에 앉는다 (2026-08-30 측정, test_interior --adiabat). "
            "2 M⊕ (1.22 R⊕) 위는 그 논문의 천장이라 다시 앵커가 하나다. 핵 온도가 그 폭만큼 불확실하므로 "
            "등급을 analog 로 내린다 — 그 값을 받는 쪽이 core_state 다.")
    if thermal_moves:
        notes.append(
            f"답이 그 선언에 기댄다 — 기준 {EARTH_POTENTIAL_T:.0f} K 에서 "
            f"{potential_temperature - EARTH_POTENTIAL_T:+.0f} K 떨어져 있고, 그만큼 열압력이 "
            "밀도를 움직인다. 단열선은 대류하는 층에만 맞고, 조석가열과 맨틀 안의 열경계층은 "
            "프로파일을 초단열로 만든다 (Unterborn+ 2019 §3.2). 등급을 analog 로 내린다.")
    if boundary_temperature_jump > 0.0:
        notes.append(
            f"**열경계층 {boundary_temperature_jump:.0f} K 는 선언이다.** 얼음 맨틀 꼭대기와 기체 외피 "
            "바닥 사이의 온도 차이고, 그 층이 성층으로 안정한가와 그 폭은 열 이력이 정하므로 이 "
            "레시피가 도출하지 않는다 (Nettelmann+ 2016 의 TBL — 그들의 U15-II 가 2500 K, U15-III 가 "
            "4700 K, 경계는 0.1 Mbar 근처). 안쪽 전체가 그만큼 더 뜨겁고 같은 압력에서 덜 조밀하다. "
            "등급을 analog 로 내린다.")
    if mantle_rock_fraction > 0.0:
        notes.append(
            f"**얼음 맨틀의 암석 분율 {mantle_rock_fraction:.2f} 은 선언이다.** 얼음:암석 비는 형성이 정하고 "
            "관측이 묶지 않으므로 이 레시피가 도출하지 않는다 (Nettelmann+ 2016 §6 — 따뜻한 내부 맨틀은 "
            "중력장을 맞추려면 암석이 필요하다; 물·암석 혼합의 거동은 그들도 '잘 이해되지 않았다' 고 적는다). "
            "규산염을 부피 가법으로 섞고 ∇_ad 는 c_P 가중이다 (AVL 의 폭은 얼음 혼합에서 4 % 상한, "
            "물–암석에 대한 발표값은 없다). 등급을 analog 로 내린다.")
    # 얼음 기둥이 얼음 X 까지 내려갔는가. 그 상은 이 사다리에서 **읽은 게 아니라 적합한**
    # 유일한 얼음이고, 원 표현을 1.475 % 안에서만 재현한다 — 다른 얼음 상들의 0.006~
    # 0.118 % 와 자릿수가 다르다. 게다가 그 표현 자체가 제일원리 계산이지 측정이 아니다.
    # mgsio3_pv 가 3.5 TPa 위에서 등급을 내리는 것과 같은 종류의 자리다.
    ice_x_reached = st.ice_x_reached
    if ice_x_reached:
        # 순수 얼음 천체는 층 경계가 없어 p_ice_base 가 비어 있다. 그 기둥의 바닥은 중심이다.
        p_ice_base = st.p_ice_base if st.p_ice_base is not None else st.p_center
        notes.append(
            f"**얼음 기둥이 얼음 X 까지 내려갔다** — 기둥 바닥이 "
            f"{p_ice_base / 1e9:.0f} GPa 로 얼음 VII→X 전이({ICE_VII_TO_X / 1e9:.1f} GPa) "
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
    # 앵커가 셋이고 셋이 두 자릿수 질량 범위(14.5 ~ 318 M⊕)를 덮는다. 사이를 통째로
    # 강등하던 규칙은 근거를 잃었으므로 남기지 않는다. 남는 강등 사유는 **선언** 이다 —
    # 이 갈래는 포텐셜 온도 없이 못 풀고, 그 값은 이 레시피가 도출하지 않는다.
    giant_declared = gmf > 0
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
    if body_class in SUB_NEPTUNE_CLASSES:
        notes.append(
            f"**가스질량분율 {gmf:.3f} 는 선언이다.** 서브넵튠의 외피 두께는 조성이 아니라 나이와 "
            "항성 조사량이 정하고(광증발), 이 레시피에는 진화가 없어서 그 값을 도출하지 않는다 — "
            "ice_allowed · initial_porosity · envelope_z · potential_temperature 와 같은 종류의 "
            "선언이고, 답이 그 값에 기대므로 등급을 analog 로 내린다. 이 갈래의 앵커는 아직 "
            "없다: 거대행성 셋은 질량이 두 자릿수 위다.")
    if giant_declared:
        band = " · ".join(f"{n} {m:.4g} M⊕ {d:+.2f} %" for n, m, d in GIANT_ANCHORS)
        notes.append(
            "**이 갈래는 선언에 기댄다 — 포텐셜 온도다.** 수소-헬륨 외피는 등온으로 "
            "풀 수 없고 (표가 (P, T) 의 함수다), 1 bar 준위의 온도는 이 레시피가 "
            "도출하지 않는 값이다. 그래서 등급을 analog 로 내린다. **질량 때문이 "
            "아니다** — 2026-08-28 까지 여기 있던 '목성보다 가벼우면 강등' 규칙은 "
            "n = 1 폴리트로프가 어느 거대행성에나 같은 반지름을 돌려주던 데서 나온 "
            "것이고, 그 전제가 표로 바뀌면서 사라졌다. 지금 앵커는 셋이고 14.5 M⊕ "
            f"에서 318 M⊕ 까지를 덮는다: {band}.")
    notes += [
             "이 노드는 결합 코어 안에 있다 (chain.yaml 순환 1·3). converged 는 "
             "**이 적분의 사격이 붙었는가** 를 말하지, 조석가열이 조성을 되바꾸는 "
             "그래프 고리가 닫혔는가를 말하지 않는다 — 그 고리는 러너가 코어를 "
             "돌릴 때 닫힌다. 노드 안에도 고리가 하나 있다 (순환 7): 상이 밀도를 정하고 "
             "밀도가 온도 프로파일을 정하고 온도가 상을 정한다. 적분은 중심에서 바깥으로 "
             "가며 걸음마다 상을 그 자리의 (P, T) 로 정하므로 한 번의 적분 안에서는 인과가 "
             "한 방향이고, 되먹임은 표면 온도를 맞추는 바깥 고리가 닫는다 — converged 가 "
             "그 고리의 수렴(표면 온도 1e-3 안)까지 포함한다.",
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
                            or boundary_temperature_jump > 0 or mantle_rock_fraction > 0
                            or not differentiated or giant_declared
                            or silicate_extrapolated or thermal_moves
                            or thermal_unchecked or ice_x_reached)
               else "calibrated"),
        inputs=inputs,
        cycles=(1, 3, 7),
        converged=converged,
        values={"nmoi": st.nmoi,
                "core_temperature": st.t_center,
                "cmb_temperature": st.t_cmb,
                "cmb_pressure": (st.p_cmb or 0.0) / 1e9,
                "ice_column_state": ice_state,
                "ocean_thickness": st.ocean_thickness_m / 1e3,
                "ice_shell_thickness": st.ice_shell_thickness_m / 1e3,
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
               "ocean_thickness": "km",
               "ice_shell_thickness": "km",
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
        cycles=(1, 3, 7),
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
        km = EARTH_RADIUS_M / 1e3
        r_lo = min(r.values["radius"] for _, r in solved) * km
        r_hi = max(r.values["radius"] for _, r in solved) * km
        span_note = f"풀린 눈금의 반지름 범위 {r_lo:.0f}-{r_hi:.0f} km"

        if not blocked:
            # **막힌 눈금이 하나도 없다.** 축은 끝까지 풀렸고 목표가 그 밖이다 — 이건
            # "막힌 구간" 이 아니라 사정거리 문제이고, 둘을 같은 문구로 내보내면 거절이
            # 기작을 이름 대지 않는다. 어느 쪽 끝인지, 그리고 무엇이 있어야 닿는지를 말한다.
            if radius_earth * km > r_hi:
                # 목표가 제일 큰 눈금보다 크다 = 축이 낼 수 있는 것보다 가볍다.
                # 얼음 축에서는 위쪽 분기가 이미 이 경우를 잡으므로 여기 오는 것은
                # 핵 축이고, 핵을 **빼는** 방향으로는 순규산염이 끝이다.
                return out_of_domain(
                    RECIPE, VERSION,
                    f"{radius_earth * km:.0f} km 는 이 축이 닿는 것보다 가볍다 — 핵을 "
                    f"{solved[0][0]:.2f} 까지 빼도 {r_hi:.0f} km 다. 금속을 더 빼는 "
                    "것으로는 못 가므로 남는 기작은 더 가벼운 물질이다: 얼음이거나 "
                    "빈 공간이거나 H/He 외피다. 얼음이 선언으로 배제돼 있지 않다면 "
                    "얼음 축으로 풀렸을 것이므로, 이 거절은 그 선언이 있다는 뜻이다.",
                    inputs=inputs, refs=REFS, notes=(span_note,))
            # 목표가 제일 작은 눈금보다 작다 = 축이 낼 수 있는 것보다 밀하다.
            # 이 축의 끝은 fe_prem 이고 그건 가벼운 원소가 섞인 **지구** 핵이다. 순철
            # 곡선(fe_eps)이 "이보다 밀할 수 없다" 는 한계선으로 이 파일에 이미 있으므로,
            # 목표를 거기에 대면 조성 문제와 물리적 불가능이 갈린다.
            iron = solve(mass_earth, composition="iron", ice_mass_fraction=0.0)
            r_iron = iron.values["radius"] * km if iron.applicable else None
            if r_iron is not None and radius_earth * km < r_iron:
                return out_of_domain(
                    RECIPE, VERSION,
                    f"{radius_earth * km:.0f} km 는 이 질량을 **순철로 채워도** 못 "
                    f"미치는 크기다 (순철 {r_iron:.0f} km). 행성 물질 중 그보다 밀한 "
                    "것이 없으므로 남는 설명은 조성이 아니다 — 선언된 질량-반지름 쌍이 "
                    "서로 안 맞거나, 질량이 Msini 라 참값이 더 크거나다.",
                    inputs=inputs, refs=REFS,
                    notes=(span_note,
                           "순철 곡선은 이 레시피가 한계선으로 들고 있는 fe_eps 다 "
                           "(Seager+ 2007 Table 1). 밀도의 상한이지 조성 후보가 아니다.",))
            return out_of_domain(
                RECIPE, VERSION,
                f"{radius_earth * km:.0f} km 는 이 축이 닿는 것보다 밀하다 — 핵을 "
                f"{solved[-1][0]:.0f} 까지 채워도 {r_lo:.0f} km 다. 그런데 순철 곡선"
                + (f"({r_iron:.0f} km) 안쪽이므로" if r_iron is not None else " 안쪽이므로")
                + " 물리적으로 불가능한 것은 아니다. 이 축의 끝은 fe_prem, 곧 가벼운 "
                "원소가 섞인 **지구** 핵이고, 이 천체는 그보다 순수한 철을 요구한다. "
                "필요한 것은 핵 재료를 자유롭게 두는 것이지 새 상태방정식이 아니다.",
                inputs=inputs, refs=REFS,
                notes=(span_note,
                       "fe_prem 은 PREM 외핵 적합이라 지구의 가벼운 원소가 그 유효 ρ₀ "
                       "안에 흡수돼 있다. fe_eps 는 실험실 순철이다. 둘 사이가 이 "
                       "레시피가 지금 훑지 않는 축이다.",))

        return out_of_domain(
            RECIPE, VERSION,
            f"목표 반지름을 감싸는 배합이 {axis} 축의 **막힌 구간 안** 에 있다. "
            f"풀리는 눈금은 {len(solved)}/{len(scan)} 개뿐이고, 그 어느 쌍도 "
            f"{radius_earth * km:.0f} km 를 감싸지 못한다. {blocked[0][1].reason}",
            inputs=inputs, refs=REFS,
            notes=(span_note,))

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
        cycles=(1, 3, 7),
        converged=best.converged,
        values=v, units=best.units, refs=REFS, notes=tuple(notes),
    )


# ── 3층 역산: 금속 핵 + 암석 + 물 기둥(그 안의 바다) ─────────────────────
#
# 위의 역산은 자유 분율 **하나** 를 푼다 — 질량과 반지름 둘로 미지수 하나. 유로파·가니메데·
# 엔셀라두스 같은 천체는 금속 핵과 물 기둥을 같이 갖고, 그러면 미지수가 둘이다(핵질량분율·
# 얼음질량분율, 암석은 나머지). 바다의 두께는 **미지수가 아니다** — 포텐셜 온도 선언과
# 녹는곡선이 정하고, 이 함수는 그 선언을 받아 넘길 뿐이다.
#
# 미지수 둘에 관측 둘이면 해는 점이 아니라 **띠** 다. 그래서 고르지 않는다: 핵질량분율 축을
# 훑으며 자리마다 반지름을 재현하는 얼음질량분율을 풀고, 그 (핵, 얼음, C/MR²) 의 열을 그대로
# 돌려준다. 발표된 C/MR² 가 있으면(태양계 위성) 그것을 **세 번째 관측** 으로 받아 띠 위의 한
# 점으로 좁힌다 — 좁힌 것이지 고른 것이 아니고, 결과가 그렇게 적는다. 엔진이 스스로 핵질량분율을
# 정하는 일은 없다.
THREE_LAYER_CORE_GRID = (0.0, 0.15, 0.30, 0.45)   # 훑는 핵질량분율. 넷이면 띠의 모양이 보인다
THREE_LAYER_NMOI_TOL = 1e-3                        # C/MR² 로 좁힐 때의 상대 허용오차
_INFER_ITERS = 12                                  # 얼음질량분율의 regula falsi 상한


def _solve_ice_for_radius(mass_earth: float, radius_earth: float, cmf: float,
                          potential_temperature: float, tidal_heating: bool):
    """핵질량분율을 고정하고 반지름을 재현하는 얼음질량분율을 푼다. (분율, Result) 또는 None.

    반지름은 얼음에 단조증가이므로 양 끝을 재고 그 사이를 Illinois 형 regula falsi 로 좁힌다 —
    온도를 선언한 풀이가 한 번에 몇 초라 이분법 40 회는 못 쓴다. 양 끝 밖이면 None: 얼음을
    다 빼도 크거나(이 핵으로는 너무 가볍다), 거의 다 얼음이어도 작다(빈 공간이 필요하다)."""
    def at(imf):
        return solve(mass_earth, core_mass_fraction=cmf, ice_mass_fraction=imf,
                     potential_temperature=potential_temperature,
                     tidal_heating=tidal_heating)
    lo, hi = 0.0, max(0.0, 0.98 - cmf)
    r_lo = at(lo)
    if not r_lo.applicable:
        return None
    if r_lo.values["radius"] >= radius_earth:
        return (lo, r_lo) if abs(r_lo.values["radius"] - radius_earth) / radius_earth < INFER_TOL else None
    r_hi = at(hi)
    if not r_hi.applicable or r_hi.values["radius"] < radius_earth:
        return None
    f_lo = r_lo.values["radius"] - radius_earth
    f_hi = r_hi.values["radius"] - radius_earth
    best = None
    side = 0
    for _ in range(_INFER_ITERS):
        x = hi - f_hi * (hi - lo) / (f_hi - f_lo)
        res = at(x)
        if not res.applicable:
            return None
        f = res.values["radius"] - radius_earth
        best = (x, res)
        if abs(f) / radius_earth < INFER_TOL:
            break
        if f < 0.0:
            lo, f_lo = x, f
            if side == -1:
                f_hi *= 0.5
            side = -1
        else:
            hi, f_hi = x, f
            if side == 1:
                f_lo *= 0.5
            side = 1
    return best


def infer_three_layer(mass_earth: float, radius_earth: float,
                      potential_temperature: float, nmoi: float | None = None,
                      tidal_heating: bool = False,
                      core_grid: tuple[float, ...] = THREE_LAYER_CORE_GRID) -> Result:
    """질량과 반지름을 재현하는 (핵질량분율, 얼음질량분율) 의 띠를 돌려준다. C/MR² 를 주면 좁힌다.

    `potential_temperature` 는 필수다 — 온도가 흐르지 않으면 바다가 없고, 바다가 없으면 이
    함수가 위의 단일 축 역산과 다를 것이 없다. 그 선언이 바다의 두께를 정하므로 결과는 늘
    analog 다."""
    inputs = {"mass_earth": mass_earth, "radius_earth": radius_earth,
              "potential_temperature": potential_temperature, "nmoi_observed": nmoi,
              "composition": "inferred_three_layer", "differentiated": True,
              "body_class": None, "tidal_heating": tidal_heating,
              "core_mass_fraction": None, "ice_mass_fraction": None}
    if mass_earth <= 0 or radius_earth <= 0:
        return out_of_domain(RECIPE, VERSION, "질량 또는 반지름이 양수가 아니다",
                             inputs=inputs, refs=REFS)
    if not potential_temperature or potential_temperature <= 0.0:
        return out_of_domain(
            RECIPE, VERSION,
            "3층 역산에는 포텐셜 온도 선언이 있어야 한다. 바다의 자리를 정하는 것이 녹는곡선에 "
            "댄 온도이고, 온도가 흐르지 않으면 기둥은 전부 고체라 단일 축 역산(infer_composition)"
            "과 같은 문제가 된다.", inputs=inputs, refs=REFS)

    members = []
    for cmf in core_grid:
        got = _solve_ice_for_radius(mass_earth, radius_earth, cmf,
                                    potential_temperature, tidal_heating)
        if got is None:
            continue
        imf, res = got
        members.append({"core_mass_fraction": cmf, "ice_mass_fraction": imf,
                        "nmoi": res.values["nmoi"], "radius": res.values["radius"],
                        "ocean_thickness": res.values["ocean_thickness"],
                        "ice_shell_thickness": res.values["ice_shell_thickness"],
                        "converged": bool(res.converged)})
    if not members:
        return out_of_domain(
            RECIPE, VERSION,
            f"핵질량분율 {', '.join(f'{c:.2f}' for c in core_grid)} 어느 자리에서도 얼음질량분율로 "
            f"반지름 {radius_earth * EARTH_RADIUS_M / 1e3:.0f} km 를 재현하지 못한다. 암석·금속·"
            "물의 어떤 배합으로도 이 밀도가 안 나온다는 뜻이고, 남는 기작은 빈 공간(다공도)이거나 "
            "이 레시피의 규산염보다 가벼운 암석(함수 규산염)이다.",
            inputs=inputs, refs=REFS)

    n_lo, n_hi = (min(m["nmoi"] for m in members), max(m["nmoi"] for m in members))
    band_note = ("띠 — " + " · ".join(
        f"핵 {m['core_mass_fraction']:.2f} → 얼음 {m['ice_mass_fraction']:.3f}, "
        f"C/MR² {m['nmoi']:.4f}, 바다 {m['ocean_thickness']:.0f} km / 껍질 "
        f"{m['ice_shell_thickness']:.0f} km" for m in members)
        + ". 질량과 반지름 둘로는 이 열의 어느 점도 고를 수 없다.")
    lean = ("**바다의 두께는 포텐셜 온도 선언이 정한다.** 껍질 아래 바다 꼭대기는 그 압력의 "
            "녹는점에 있고, 표면까지 감압한 단열선의 온도가 곧 선언값이다 — 얼음 Ih 의 녹는점 "
            "251–273 K 사이 어디에 두느냐가 껍질 두께이고, 그것을 정하는 열 이력이 이 레시피에 "
            "없다. 그래서 analog 다.")
    converged = all(m["converged"] for m in members)

    if nmoi is None or not (n_lo <= nmoi <= n_hi):
        notes = [band_note, lean]
        if nmoi is not None:
            notes.insert(0, (
                f"**관측 C/MR² {nmoi:.4f} 는 띠 밖이다** — 띠는 {n_lo:.4f} 에서 {n_hi:.4f} 까지다. "
                + ("관측값이 띠보다 높다: 질량이 이 모형보다 **덜** 중심에 몰려 있어야 하고, "
                   "핵을 빼는 것으로는 이 띠의 위 끝(핵 0)이 한계다. 남는 기작은 암석 자체가 "
                   "이 레시피의 규산염보다 가벼운 것(함수 규산염 · 다공질 핵)이거나 부분 분화 — "
                   "층 수의 문제가 아니라 **재료** 의 문제다."
                   if nmoi > n_hi else
                   "관측값이 띠보다 낮다: 이 격자의 가장 큰 핵으로도 질량이 충분히 중심에 안 "
                   "몰린다. 핵 격자를 위로 넓히면 닿을 수 있다.")))
        return Result(
            recipe=RECIPE, version=VERSION, regime="inferred_three_layer_band",
            reason=(f"질량 {mass_earth:.3g} M⊕ 와 반지름 {radius_earth:.4f} R⊕ 를 재현하는 "
                    f"(핵, 얼음) 배합이 {len(members)} 점의 띠로 나온다 — C/MR² {n_lo:.4f}–"
                    f"{n_hi:.4f}. 미지수 둘에 관측 둘이라 좁히지 않는다."),
            grade="analog", inputs=inputs, cycles=(1, 3, 7), converged=converged,
            values={"nmoi_low": n_lo, "nmoi_high": n_hi, "members": members},
            units={"nmoi_low": "dimensionless", "nmoi_high": "dimensionless",
                   "members": ""},
            refs=REFS, notes=tuple(notes))

    # C/MR² 가 띠 안이다. 이웃한 두 점 사이를 보간해 출발하고, 핵질량분율에 대해 할선으로 좁힌다.
    members.sort(key=lambda m: m["core_mass_fraction"])
    pairs = [(a, b) for a, b in zip(members, members[1:])
             if min(a["nmoi"], b["nmoi"]) <= nmoi <= max(a["nmoi"], b["nmoi"])]
    a, b = pairs[0]
    x0, y0 = a["core_mass_fraction"], a["nmoi"] - nmoi
    x1, y1 = b["core_mass_fraction"], b["nmoi"] - nmoi
    best = None
    for _ in range(6):
        x = x1 - y1 * (x1 - x0) / (y1 - y0) if y1 != y0 else 0.5 * (x0 + x1)
        got = _solve_ice_for_radius(mass_earth, radius_earth, x,
                                    potential_temperature, tidal_heating)
        if got is None:
            break
        imf, res = got
        y = res.values["nmoi"] - nmoi
        best = (x, imf, res)
        if abs(y) / nmoi < THREE_LAYER_NMOI_TOL:
            break
        x0, y0, x1, y1 = x1, y1, x, y
    if best is None:
        return out_of_domain(
            RECIPE, VERSION, "띠 안인데 C/MR² 로 좁히는 할선이 풀리는 점을 못 찾았다",
            inputs=inputs, refs=REFS, notes=(band_note,))
    cmf, imf, res = best
    inputs["core_mass_fraction"] = cmf
    inputs["ice_mass_fraction"] = imf
    v = dict(res.values)
    v.update({"nmoi_low": n_lo, "nmoi_high": n_hi, "members": members})
    u = dict(res.units)
    u.update({"nmoi_low": "dimensionless", "nmoi_high": "dimensionless", "members": ""})
    notes = [f"역산이다 — 핵질량분율 {cmf:.3f} · 얼음질량분율 {imf:.3f} 가 질량·반지름과 "
             f"관측 C/MR² {nmoi:.4f} 를 재현한다. C/MR² 는 **세 번째 관측** 으로 받아 띠를 "
             "좁히는 데만 썼고, 이 값은 예측이 아니라 되읽은 값이다.",
             band_note, lean]
    notes += list(res.notes)
    return Result(
        recipe=RECIPE, version=VERSION, regime="inferred_three_layer_by_nmoi",
        reason=(f"질량 {mass_earth:.3g} M⊕ 와 반지름 {radius_earth:.4f} R⊕ 가 (핵, 얼음) 의 "
                f"띠를 남기고, 관측 C/MR² {nmoi:.4f} 가 그 띠 위의 한 점 — 핵 {cmf:.3f} · "
                f"얼음 {imf:.3f} — 을 고른다."),
        grade="analog", inputs=inputs, cycles=(1, 3, 7), converged=res.converged,
        values=v, units=u, refs=REFS, notes=tuple(notes))


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
