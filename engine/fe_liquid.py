# 액체 순철의 Dorogokupets+ 2017 열역학 세트 — 35 GPa 위 구간의 γ·c_V 를 공급한다 (C58, 브리프 180 C)
"""Dorogokupets, Dymshits, Litasov & Sokolova 2017, *Sci. Rep.* **7**, 41863
([`2017NatSR...741863D`](https://ui.adsabs.harvard.edu/abs/2017NatSR...741863D), 보유) 의
**액체 철** 세트. 논문의 식 (2)·(9)–(11)·(13)–(15)·(17)–(18) 을 **인쇄된 그대로** 옮긴 것이고,
매개변수는 Table 1 의 «liquid» 열이다.

**이 모듈이 무엇을 공급하고 무엇을 안 하는가.** 공급하는 것은 (∂P/∂T)_V · C_V · γ 셋이다 —
`eos.ThermalSet` 이 35 GPa 위 구간에서 읽는다. **밀도 경로는 이 모듈을 읽지 않는다** (오너 검토
대기 중인 결정 (A), 2026-09-11): `fe_prem` 의 밀도는 PREM 적합과 그 단열선 기준에 남아 있고,
여기 세트를 밀도에까지 얹으면 2100 K 등온에서 잰 열압력을 이미 뜨거운 PREM 적합에 더해 **지구를
두 번 데운다**. 그 되돌리기는 배선 한 줄이고, 그때는 밀도 표를 사전등록한다.

⚠ **이 세트는 Huang+ 2023 의 저압 실측과 일치하지 않는다** — 19·35 GPa 두 앵커에서 밀도는
0.5 % 안으로 맞지만 C_V·α·γ 는 40 % 규모로 어긋난다 (C58 (a) ⓐ′ 표). 그래서 이 구간의 값은
**등급 라벨을 달고** 나가고, 경계에서의 불연속은 수로 보고된다 (`boundary_jump`). 라벨 없이
쓰지 않는 것이 이 모듈의 존재 조건이다.
"""
from __future__ import annotations

import math

R_GAS = 8.314462618          # J/(mol·K)

# ── Table 1 의 «liquid Fe» 열, 인쇄값 ───────────────────────────────────────
N_ATOM = 1.0
V0 = 7.95784e-6              # m³/mol (7.95784 cm³/mol)
K0 = 83.7e9                  # Pa
K0P = 5.97
THETA0 = 263.0               # K
GAMMA0 = 2.033
BETA = 1.168
GAMMA_INF = 0.0
E0 = 198e-6                  # K⁻¹ — 전자 항
G_EL = 0.884
T_REF = 1811.0               # K. 액체 세트의 기준 온도 (녹는점, 1 bar)
MOLAR_MASS = 55.845e-3       # kg/mol
ETA = 1.5 * K0P - 1.5

REF = ("Dorogokupets+ 2017 Sci. Rep. 7, 41863 (2017NatSR...741863D) Table 1 liquid Fe, "
       "eqs (2)(9)-(11)(13)-(15)(17)-(18)")


def _gamma_v(x: float) -> float:
    """식 (11) 의 γ(V) — x = V/V₀."""
    return GAMMA_INF + (GAMMA0 - GAMMA_INF) * x ** BETA


def _q_v(x: float) -> float:
    """q = (∂ln γ/∂ln V)_T, 식 (11) 의 미분."""
    return BETA * x ** BETA * (GAMMA0 - GAMMA_INF) / _gamma_v(x)


def _theta_v(x: float) -> float:
    """식 (10) 의 Debye 온도 θ(V)."""
    return THETA0 * x ** (-GAMMA_INF) * math.exp((GAMMA0 - GAMMA_INF) / BETA * (1.0 - x ** BETA))


def _p_cold(v: float) -> float:
    """식 (2) — Rydberg-Vinet 냉각 압력."""
    xx = (v / V0) ** (1.0 / 3.0)
    return 3.0 * K0 * xx ** -2 * (1.0 - xx) * math.exp(ETA * (1.0 - xx))


def _c_v_th(v: float, t: float) -> float:
    """식 (13) — 격자 C_V [J/(mol·K)], 아인슈타인 항."""
    u = _theta_v(v / V0) / t
    return 3.0 * N_ATOM * R_GAS * u * u * math.exp(u) / (math.exp(u) - 1.0) ** 2


def _p_th(v: float, t: float) -> float:
    """식 (9) — 격자 열압력."""
    th = _theta_v(v / V0)
    return 3.0 * N_ATOM * R_GAS * _gamma_v(v / V0) / v * th / (math.exp(th / t) - 1.0)


def _k_t_th(v: float, t: float) -> float:
    """식 (14) — 열압력의 체적탄성률 몫."""
    x = v / V0
    return (_p_th(v, t) * (1.0 + _gamma_v(x) - _q_v(x))
            - _gamma_v(x) ** 2 * t * _c_v_th(v, t) / v)


def _c_v_el(v: float, t: float) -> float:
    """식 (17) — 전자 C_V [J/(mol·K)]. e(V) = e₀ x^g."""
    return 3.0 * N_ATOM * R_GAS * E0 * (v / V0) ** G_EL * t


def _p_el(v: float, t: float) -> float:
    """식 (15) — 전자 압력."""
    return G_EL / v * 1.5 * N_ATOM * R_GAS * E0 * (v / V0) ** G_EL * t * t


def _k_t_el(v: float, t: float) -> float:
    return _p_el(v, t) * (1.0 - G_EL)


def pressure(v: float, t: float) -> float:
    """P(V, T) [Pa]. 기준 온도의 열 항을 빼는 것이 식 (2) 의 형태다."""
    return (_p_cold(v) + _p_th(v, t) - _p_th(v, T_REF)
            + _p_el(v, t) - _p_el(v, T_REF))


def k_t(v: float, t: float) -> float:
    """K_T(V, T) [Pa]."""
    xx = (v / V0) ** (1.0 / 3.0)
    k_cold = K0 * xx ** -2 * math.exp(ETA * (1.0 - xx)) * (1.0 + (1.0 - xx) * (ETA * xx + 1.0))
    return k_cold + _k_t_th(v, t) - _k_t_th(v, T_REF) + _k_t_el(v, t) - _k_t_el(v, T_REF)


def volume_at(p: float, t: float) -> float:
    """P, T 에서 몰부피 [m³/mol]. P(V) 는 단조감소라 뿌리가 하나다.

    ⚠ **이 자리가 적분기의 안쪽 고리다** (브리프 180 C). 첫 판은 200회 이분법이었고, γ 가 걸음마다
    이것을 부르니 `core_state` 한 판이 2 분을 넘겼다 — 답은 맞고 **쓸 수 없이 느렸다.** 그래서
    Newton 으로 바꾸고(수치미분, 보통 4–6회) 이분법은 **발산했을 때의 안전망**으로만 남긴다.
    `interior.py` 의 밀도 뒤집기가 같은 이유로 같은 모양이다."""
    v = V0 * 0.9
    for _ in range(40):
        f = pressure(v, t) - p
        if abs(f) < 1.0:                      # 1 Pa. P 는 GPa 규모라 상대오차 1e-11 이하다
            return v
        h = v * 1e-6
        dfdv = (pressure(v + h, t) - pressure(v - h, t)) / (2.0 * h)
        if dfdv == 0.0:
            break
        step = f / dfdv
        v_new = v - step
        if not (0.2 * V0 < v_new < 1.5 * V0):  # 창을 벗어나면 Newton 을 믿지 않는다
            break
        if abs(step) < v * 1e-12:
            return v_new
        v = v_new
    lo, hi = 0.2 * V0, 1.5 * V0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if pressure(mid, t) > p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


#: (P, T) → 결과. 적분기가 같은 자리를 여러 번 묻는다 (K_S 와 γ, 그리고 걸음의 반 칸 차분).
_CACHE: dict[tuple[float, float], dict] = {}
_CACHE_MAX = 4096


def thermal_at(p: float, t: float) -> dict:
    """이 세트가 공급하는 셋 — (∂P/∂T)_V [Pa/K] · c_V [J/(kg·K)] · γ [무차원].

    γ 는 새 상수가 아니라 항등식 γ = (∂P/∂T)_V · V / C_V 다 — `eos.Phase.gruneisen` 이
    ρ c_V 로 쓰는 것과 같은 양이고, 여기서는 몰부피로 쓴다."""
    key = (p, t)
    hit = _CACHE.get(key)
    if hit is not None:
        return hit
    v = volume_at(p, t)
    c_v_mol = _c_v_th(v, t) + _c_v_el(v, t)
    dpdt = _gamma_v(v / V0) * _c_v_th(v, t) / v + G_EL * _c_v_el(v, t) / v
    out = {"dpdt_v": dpdt,
           "c_v": c_v_mol / MOLAR_MASS,
           "gruneisen": dpdt * v / c_v_mol,
           "k_t": k_t(v, t),
           "density": MOLAR_MASS / v}
    if len(_CACHE) < _CACHE_MAX:
        _CACHE[key] = out
    return out
