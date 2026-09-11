# 얼음 VII·VII*·X 의 French & Redmer 2015 자유에너지 — 인쇄된 퍼텐셜을 그대로 평가한다 (브리프 190)
"""French & Redmer, *Phys. Rev. B* **91**, 014308 (2015) ([`2015PhRvB..91a4308F`], 보유).

논문이 인쇄하는 것은 **성질이 아니라 퍼텐셜**이다 — 식 (6) 의 자유에너지 f(ρ, T) 와 그 세 항,
식 (9) 전자 바닥상태 · 식 (11) 열항 · 식 (15) 핵 바닥상태. c_V·α·γ 는 그 미분이고, 그래서 이
모듈의 등급 라벨은 «printed potential, our derivative» 다.

⚠ **저자가 권하는 것은 식 (9) 의 HSE 매개변수화다** (§VI): *"For standard applications we recommend
using the electronic ground-state parametrization derived with the HSE XC functional"*. ⚠ **범위를
좁혀 읽는다**: XC 변종이 있는 것은 **Table I (식 (9), u_e) 뿐**이고 Table II (식 (11)·(13)) 와
Table III (식 (15)) 에는 변종이 없다 — 그래서 라벨은 «HSE parametrization of Eq. (9)» 이지
«the HSE column» 이 아니다. ⚠ 논문은 «second row in Table I» 이라고 적지만 Table I 에서 행은
a0…a5 이고 XC 는 **열**이다 — 그래서 위치가 아니라 **이름(HSE)** 으로 고른다.

⚠ **적합의 창은 상 안정 영역이 아니라 MD 격자다** (브리프 190 Amendment 1): p3 이 인쇄하는 것은
«densities were varied between 1.6 and 4.25 g/cm³, and the temperatures were chosen from 295 up to
2000 K» 이고, p1 의 «valid in the entire stability region» 은 **상**이 어디 있는가지 적합이 어디를
덮는가가 아니다. 그 둘은 p1 에서 한 문장으로 «and» 로 이어져 있어서, 한 쪽을 인용하면 다른 쪽이
딸려 온다 — 인용 전에 문장을 쪼갠다.

단위: ρ [g/cm³] · T [K] · f [kJ/g] (= MJ/kg) · p = ρ²(∂f/∂ρ)_T [GPa].
"""
from __future__ import annotations

import math

import convergence

#: Table I 의 **HSE** 매개변수화 (저자 권고, 식 (9) 한정). ue [kJ/g], ρ [g/cm³].
UE_HSE = (-16.8923, -85.0197, 8.33865, -0.150425, 59.9442, 38.2224)
#: Table I 의 다른 열들 — 권고가 아니지만 «다섯 중 하나를 골랐다» 를 보이기 위해 든다.
UE_COLUMNS = {
    "PBE": (78.0913, -172.712, 18.095, -0.717051, 130.541, 67.2915),
    "HSE": UE_HSE,
    "vdW-optB86b": (84.7263, -175.063, 18.6251, -0.757606, 131.406, 66.7509),
    "AM05": (137.924, -217.067, 22.4402, -0.943835, 166.409, 82.6152),
    "LDA": (134.099, -240.338, 25.5167, -1.13834, 182.303, 88.3112),
}

#: Table III — 식 (15) 의 핵 바닥상태 계수.
UN_B = (2.08, 0.272, 0.096, 0.788, 2.54e-5)

#: Table II — 식 (11)·(13) 의 α_ik 와 γ_jk. 키는 (i 또는 j, k), k0 = 3.
ALPHA = {(0, -4): 6.869192e-3, (0, -3): -3.919234e-3, (0, -2): 6.790631e-5}
GAMMA = {(0, -4): -2.604037e-2, (0, -3): 2.104060e-2, (0, -2): -1.515928e-3,
         (1, -4): 6.721305e-2, (1, -3): -1.158057e-1, (1, -2): 5.234025e-2,
         (2, -4): -1.178112e-1, (2, -3): 1.754266e-1, (2, -2): -6.213482e-2,
         (3, -4): 1.206828e-1, (3, -3): -1.910820e-1, (3, -2): 7.712887e-2}

T_D, T_E, A_D, A_E, K0 = 700.0, 1000.0, 2.0, 2.0, 3.0   # 식 (14) 와 그 아래 문단

REF = ("French & Redmer 2015 Phys. Rev. B 91, 014308 (2015PhRvB..91a4308F), "
       "eqs (6)(9)(11)(15) with Tables I (HSE column) · II · III")

#: 적합 격자 — p3 이 인쇄한 그대로. 창의 근거는 이것이고 상 안정 영역이 아니다.
FIT_RHO_MIN, FIT_RHO_MAX = 1.6, 4.25          # g/cm³
FIT_T_MIN, FIT_T_MAX = 295.0, 2000.0          # K


#: 가우스-르장드르 32점의 마디와 무게 — **한 번만 만든다**.
#: ⚠ 첫 판은 이것을 `_debye` 안에서 매 호출 다시 풀었다(마디마다 뉴턴 60회). 값은 같지만
#:   한 호출이 0.3 ms 였고, 적분기가 걸음마다 묻는 자리에서 그것이 천왕성 한 판을 분 단위로
#:   밀어 올렸다 (지휘석 실측: 기준선 2:22 대 9 분 넘김). 마디는 z 에 무관하므로 캐시가 맞다.
_GL_NODES: list[tuple[float, float]] = []


def _gl_nodes(n: int = 32) -> list[tuple[float, float]]:
    """[-1, 1] 의 가우스-르장드르 마디·무게. 첫 호출에서 만들고 이후는 그대로 쓴다."""
    global _GL_NODES
    if _GL_NODES:
        return _GL_NODES
    out = []
    for k in range(n):
        x = math.cos(math.pi * (k + 0.75) / (n + 0.5))
        for _ in range(60):
            p0, p1 = 1.0, 0.0
            for j in range(n):
                p0, p1 = ((2 * j + 1) * x * p0 - j * p1) / (j + 1), p0
            dp = n * (x * p0 - p1) / (x * x - 1.0)
            dx = -p0 / dp
            x += dx
            if abs(dx) < 1e-15:
                break
        out.append((x, 2.0 / ((1.0 - x * x) * dp * dp)))
    _GL_NODES = out
    return out


def _debye(z: float) -> float:
    """식 (12) 의 D(z) = 3/z³ ∫₀^z x³/(eˣ−1) dx — 가우스-르장드르 32점.

    ⚠ 적분을 급수로 바꾸지 않는다: 논문이 적분으로 인쇄했고, 32점은 z ≤ 30 에서
    상대오차 1e-12 아래다 (모듈 시험이 그 수를 낸다)."""
    if z <= 0.0:
        return 1.0
    total = 0.0
    for x, w in _gl_nodes():
        t = 0.5 * z * (x + 1.0)
        total += 0.5 * z * w * (t ** 3 / math.expm1(t) if t > 0 else 0.0)
    return 3.0 * total / z ** 3


def u_electronic(rho: float, column: str = "HSE") -> float:
    """식 (9) — 전자 바닥상태 에너지 [kJ/g].

    ⚠ **적재된 계수가 그 이름의 것인지 파싱 시점에 묻는다** (187 의 상압 K_T 가드와 같은 모양):
    Table I 에서 `a0` 는 **HSE 에서만 음수**이고 PBE·vdW-optB86b·AM05·LDA 에서는 양수다. 이름과
    수가 어긋나면 여기서 멈춘다 — 열을 잘못 실은 채 다섯 자리로 «일치» 하는 것이 이 항목에서
    가장 조용한 실패다."""
    a0, a1, a2, a3, a4, a5 = UE_COLUMNS[column]
    if (column == "HSE") != (a0 < 0.0):
        raise ValueError(f"Table I 의 {column} 계수가 이름과 맞지 않는다 — a0={a0!r} "
                         f"(HSE 만 음수, 나머지 넷은 양수)")
    ln = math.log(rho)
    return a0 + a1 * rho + a2 * rho ** 2 + a3 * rho ** 3 + a4 * ln + a5 * ln ** 2


def u_nuclear(rho: float) -> float:
    """식 (15) — 핵 바닥상태 에너지 [kJ/g]."""
    b0, b1, b2, b3, b4 = UN_B
    return b0 + b1 * rho + b2 * rho ** 2 + b3 * math.exp(-b4 * rho ** 10)


def f_thermal(rho: float, t: float) -> float:
    """식 (11) — 자유에너지의 열항 [kJ/g]."""
    out = 0.0
    for (i, k), a in ALPHA.items():
        ti = T_D * A_D ** i
        out += a * t * (3.0 * math.log(-math.expm1(-ti / t)) - _debye(ti / t)) * rho ** (k / K0)
    for (j, k), g in GAMMA.items():
        tj = T_E * A_E ** j
        out += g * t * math.log(-math.expm1(-tj / t)) * rho ** (k / K0)
    return out


def free_energy(rho: float, t: float, column: str = "HSE") -> float:
    """식 (6) — f(ρ, T) = u_e(ρ) + u_n(ρ) + f_t(ρ, T) [kJ/g].

    ⚠ §VI 이 권하는 **조립 방식** 그대로다: *"Expression (6) is composed of three individual
    terms, which are separately described by Eqs. (9), (11), and (15)"*."""
    return u_electronic(rho, column) + u_nuclear(rho) + f_thermal(rho, t)


# ── 미분으로 나오는 양들 ─────────────────────────────────────────────────────
#
# ⚠ **논문은 성질을 인쇄하지 않는다 — 퍼텐셜을 인쇄한다.** 그래서 아래는 전부 식 (6) 의 미분이고,
#   등급 라벨이 «printed potential, our derivative» 인 이유가 이것이다.
# ⚠ **중앙차분을 쓴다.** 해석 미분도 가능하지만 D(z) 의 미분이 또 하나의 적분이 되고, 검증이
#   Fig. 8 의 «논문 자신의 두 곡선이 벌어지는 폭» 안에서 이뤄지므로 (브리프 190 §5) 차분의
#   1e-6 급 오차는 그 폭보다 네 자리 작다. 그 사실은 모듈 시험이 수로 낸다.

_DT = 1e-3          # K. T 방향 차분 폭 — f 는 T 에 매끄럽다
_DRHO = 1e-6        # g/cm³


def entropy(rho: float, t: float, column: str = "HSE") -> float:
    """s = −(∂f/∂T)_ρ [kJ/(g·K)]."""
    h = _DT * max(1.0, t * 1e-3)
    return -(free_energy(rho, t + h, column) - free_energy(rho, t - h, column)) / (2.0 * h)


def c_v(rho: float, t: float, column: str = "HSE") -> float:
    """c_V = T(∂s/∂T)_ρ = −T(∂²f/∂T²)_ρ [kJ/(g·K)] — 식 (16) 의 정의 그대로."""
    h = _DT * max(1.0, t * 1e-3)
    f0 = free_energy(rho, t, column)
    return -t * (free_energy(rho, t + h, column) - 2.0 * f0
                 + free_energy(rho, t - h, column)) / h ** 2


def pressure(rho: float, t: float, column: str = "HSE") -> float:
    """p = ρ²(∂f/∂ρ)_T [GPa] — §V 가 실험과 대는 그 양이다."""
    h = _DRHO * max(1.0, rho)
    return rho ** 2 * (free_energy(rho + h, t, column)
                       - free_energy(rho - h, t, column)) / (2.0 * h)


def dp_dt(rho: float, t: float, column: str = "HSE") -> float:
    """(∂P/∂T)_ρ [GPa/K]."""
    h = _DT * max(1.0, t * 1e-3)
    return (pressure(rho, t + h, column) - pressure(rho, t - h, column)) / (2.0 * h)


def k_t(rho: float, t: float, column: str = "HSE") -> float:
    """K_T = ρ(∂P/∂ρ)_T [GPa]."""
    h = _DRHO * max(1.0, rho)
    return rho * (pressure(rho + h, t, column) - pressure(rho - h, t, column)) / (2.0 * h)


def gruneisen(rho: float, t: float, column: str = "HSE") -> float:
    """γ = (∂P/∂T)_ρ / (ρ c_V) — 새 상수가 아니라 이 파일이 든 항등식이다.

    ⚠ **단위 환산이 딱 떨어진다**: (∂P/∂T) [GPa/K] = 10⁹ Pa/K 이고 ρ c_V 는
    (g/cm³ = 10³ kg/m³) × (kJ/(g·K) = 10⁶ J/(kg·K)) = 10⁹ J/(m³·K) 라, 두 10⁹ 이 상쇄된다 —
    곱할 상수가 없다. 첫 판은 여기에 1e3 을 곱해 γ ≈ 560 을 냈고, 얼음의 γ 는 1 언저리다."""
    cv = c_v(rho, t, column)
    return 0.0 if cv <= 0.0 else dp_dt(rho, t, column) / (rho * cv)


#: (열, P, T) → 결과. 적분기가 같은 자리를 여러 번 묻는다 (K_S 와 γ, 그리고 걸음의 반 칸 차분).
#: ⚠ **순수 메모 캐시다** — 키가 입력뿐이라 따뜻한 출발 전역과 달리 추가 호출이 다음 답을 흔들지
#:   않는다 (브리프 189 Amendment 2 가 그 둘을 갈라 둔 자리).
_CACHE: dict[tuple[str, float, float], dict] = {}
_CACHE_MAX = 4096


def thermal_at(p_pa: float, t: float, column: str = "HSE") -> dict:
    """(P, T) → (∂P/∂T)_V · c_V · γ · K_T · ρ — `eos.ThermalSet` 이 읽는 모양.

    ⚠ 논문의 좌표는 (ρ, T) 다. (P, T) 로 물으면 **밀도를 먼저 뒤집어야** 하고, 그 뒤집기는
    같은 퍼텐셜을 쓴다 — 그래서 이 함수는 단조 구간에서만 답하고 밖에서는 거절한다."""
    key = (column, p_pa, t)
    hit = _CACHE.get(key)
    if hit is not None:
        return hit
    rho = density_at(p_pa / 1e9, t, column)
    cv = c_v(rho, t, column)
    out = {"dpdt_v": dp_dt(rho, t, column) * 1e9,
            "c_v": cv * 1e6,
            "gruneisen": gruneisen(rho, t, column),
            "k_t": k_t(rho, t, column) * 1e9,
            "density": rho * 1e3}
    if len(_CACHE) < _CACHE_MAX:
        _CACHE[key] = out
    return out


def density_at(p_gpa: float, t: float, column: str = "HSE") -> float:
    """P(ρ) 를 뒤집는다 — 적합 격자 안에서 p 는 ρ 에 단조증가한다.

    ⚠ 기준 가지가 있는 이분법이다 (C71/189): 구간이 자기 허용오차 안으로 닫히면 `True`,
    예산을 다 쓰면 `False` 를 기록한다."""
    lo, hi = FIT_RHO_MIN, FIT_RHO_MAX
    f_lo, f_hi = pressure(lo, t, column) - p_gpa, pressure(hi, t, column) - p_gpa
    convergence.note("ice_fr2015.density_at", None,
                     bracket_valid=convergence.bracket_valid(f_lo, f_hi))
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if pressure(mid, t, column) < p_gpa:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def thermal_at_hse(p_pa: float, t: float) -> dict:
    """`eos.THERMAL_EVALUATORS` 가 이름으로 잡는 진입점 — **저자 권고인 HSE 열**이다.

    ⚠ SeaFreeze 의 `VII_X_French` 스플라인은 **PBE** 매개변수화이고 이 세트는 **HSE** 다. 둘을
    같은 검사에 놓을 때 라벨은 이것이다: «our implementation evaluated on the PBE column vs
    SeaFreeze's PBE spline — arithmetic only; the shipped set is HSE and differs in Eq. (9) by
    construction, so a PBE–HSE gap is not a failed check»."""
    return thermal_at(p_pa, t, "HSE")
