# 순철의 Dorogokupets+ 2017 열역학 세트 — 열 위 하나의 식에 Table 1 의 «열» 을 꽂아 γ·c_V 를 공급한다 (C58 · 브리프 187)
"""Dorogokupets, Dymshits, Litasov & Sokolova 2017, *Sci. Rep.* **7**, 41863
([`2017NatSR...741863D`](https://ui.adsabs.harvard.edu/abs/2017NatSR...741863D), 보유) 의
세트. 논문의 식 (1)·(2)·(9)–(11)·(13)–(17) 을 **인쇄된 그대로** 옮긴 것이고, 매개변수는 Table 1 의
**한 열**이다 — 열을 `Column` 으로 받으므로 식은 한 벌이고 상이 여럿이다 (브리프 187, 지휘석 결정).

⚠ **식 번호가 브리프 187 에서 고쳐졌다** (감사석 지적, 2026-09-11). 예전 독스트링은 논문 번호를
뒤섞어 달고 있었다 — 격자 C_V 를 (13), 열압력을 (9), K_T,th 를 (14), γ(x) 를 (11), Θ(V) 를 (10),
전자 압력을 (15) 라고 적었다. **구현은 전부 맞았고 라벨만 틀렸다**, 그래서 아무것도 깨지지 않았고
아무도 못 봤다. 논문의 번호는 C_V (9) · P_th (10) · K_T,th (11) · γ (13) · q (14) · Θ(V) (15) ·
F_e (16) · 전자 유도량 블록 (17) 이고, 기준 온도에서 빼는 형태 자체는 식 (1) 이다.

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
import convergence
from dataclasses import dataclass

R_GAS = 8.314462618          # J/(mol·K)
MOLAR_MASS = 55.845e-3       # kg/mol. 철의 몰질량 — 열에 무관하다


@dataclass(frozen=True)
class Column:
    """Table 1 의 한 **열**. 식은 한 벌이고, 상을 가르는 것은 이 값들뿐이다 (브리프 187).

    ⚠ **`t_ref` 는 필드다 — 암묵값이 아니다.** 고체 열들은 기준 등온 T₀ = 298.15 K 이고(식 (2)),
    액체 열만 Table 1 의 머리글에서 자기 T₀ = 1811 K 를 들고 있다. 식 (1) 의 «기준에서 빼기» 가
    이 필드를 읽으므로, 틀리면 열압력 전체가 조용히 어긋난다 — 그래서 시험이 하나 붙어 있다."""
    name: str
    n_atom: float
    v0: float                # m³/mol
    k0: float                # Pa
    k0p: float
    theta0: float            # K
    gamma0: float
    beta: float
    gamma_inf: float
    e0: float                # K⁻¹
    g_el: float
    t_ref: float             # K
    ref: str

    @property
    def eta(self) -> float:
        """η = 3K₀′/2 − 3/2, 식 (2) 아래에 인쇄된 그대로."""
        return 1.5 * self.k0p - 1.5


#: Table 1 의 «Liquid Fe» 열 (T₀ = 1811 K, 머리글에 인쇄).
LIQUID = Column(
    name="dorogokupets2017_liquid_fe", n_atom=1.0,
    v0=7.95784e-6, k0=83.7e9, k0p=5.97, theta0=263.0,
    gamma0=2.033, beta=1.168, gamma_inf=0.0, e0=198e-6, g_el=0.884,
    t_ref=1811.0,
    ref=("Dorogokupets+ 2017 Sci. Rep. 7, 41863 (2017NatSR...741863D) Table 1 liquid Fe, "
         "eqs (1)(2)(9)-(11)(13)-(17)"))

#: Table 1 의 «hcp-Fe (ε)» 열. 고체이므로 기준 등온은 식 (2) 의 T₀ = 298.15 K 다.
#: ⚠ `g` 가 **음수인 유일한 열**이다 — 전자 압력의 부호가 뒤집힌다 (브리프 187 §4).
HCP = Column(
    name="dorogokupets2017_hcp_fe", n_atom=1.0,
    v0=6.8175e-6, k0=148.0e9, k0p=5.86, theta0=227.0,
    gamma0=2.20, beta=0.01, gamma_inf=0.0, e0=126e-6, g_el=-0.83,
    t_ref=298.15,
    ref=("Dorogokupets+ 2017 Sci. Rep. 7, 41863 (2017NatSR...741863D) Table 1 hcp-Fe, "
         "eqs (1)(2)(9)-(11)(13)-(17)"))


def _gamma_v(col: Column, x: float) -> float:
    """식 (13) 의 γ(V) — Altshuler 형, x = V/V₀."""
    return col.gamma_inf + (col.gamma0 - col.gamma_inf) * x ** col.beta


def _q_v(col: Column, x: float) -> float:
    """식 (14) 의 q = (∂ln γ/∂ln V)_T."""
    return col.beta * x ** col.beta * (col.gamma0 - col.gamma_inf) / _gamma_v(col, x)


def _theta_v(col: Column, x: float) -> float:
    """식 (15) 의 아인슈타인 온도 Θ(V)."""
    return (col.theta0 * x ** (-col.gamma_inf)
            * math.exp((col.gamma0 - col.gamma_inf) / col.beta * (1.0 - x ** col.beta)))


def _p_cold(col: Column, v: float) -> float:
    """식 (2) — Rydberg-Vinet 냉각 압력."""
    xx = (v / col.v0) ** (1.0 / 3.0)
    return 3.0 * col.k0 * xx ** -2 * (1.0 - xx) * math.exp(col.eta * (1.0 - xx))


def _c_v_th(col: Column, v: float, t: float) -> float:
    """식 (9) — 격자 C_V [J/(mol·K)], 아인슈타인 항."""
    u = _theta_v(col, v / col.v0) / t
    return 3.0 * col.n_atom * R_GAS * u * u * math.exp(u) / (math.exp(u) - 1.0) ** 2


def _p_th(col: Column, v: float, t: float) -> float:
    """식 (10) — 격자 열압력."""
    th = _theta_v(col, v / col.v0)
    return (3.0 * col.n_atom * R_GAS * _gamma_v(col, v / col.v0) / v
            * th / (math.exp(th / t) - 1.0))


def _k_t_th(col: Column, v: float, t: float) -> float:
    """식 (11) — 열압력의 체적탄성률 몫."""
    x = v / col.v0
    return (_p_th(col, v, t) * (1.0 + _gamma_v(col, x) - _q_v(col, x))
            - _gamma_v(col, x) ** 2 * t * _c_v_th(col, v, t) / v)


def _c_v_el(col: Column, v: float, t: float) -> float:
    """식 (17) 블록의 C_Ve [J/(mol·K)]. 자유에너지는 식 (16), e(V) = e₀ x^g."""
    return 3.0 * col.n_atom * R_GAS * col.e0 * (v / col.v0) ** col.g_el * t


def _p_el(col: Column, v: float, t: float) -> float:
    """식 (17) 블록의 전자 압력 P_e = (g/V)·E_e.

    ⚠ **`g` 의 부호를 그대로 물려받는다** — hcp 열은 `g < 0` 이라 이 항이 음수다."""
    return (col.g_el / v * 1.5 * col.n_atom * R_GAS * col.e0
            * (v / col.v0) ** col.g_el * t * t)


def _k_t_el(col: Column, v: float, t: float) -> float:
    """식 (17) 블록의 K_Te = P_e(1 − g).

    ⚠ **`g` 에 선형이 아니라 g(1 − g) 꼴이다** (감사석, 2026-09-11): `g < 0` 에서도 `g > 1`
    에서도 음수이고, 그래서 시험은 `g` 의 부호를 베끼지 않고 이 규칙을 묻는다."""
    return _p_el(col, v, t) * (1.0 - col.g_el)


def pressure(v: float, t: float, col: Column = LIQUID) -> float:
    """P(V, T) [Pa]. 기준 온도의 열 항을 빼는 형태가 식 (1) 이다."""
    return (_p_cold(col, v) + _p_th(col, v, t) - _p_th(col, v, col.t_ref)
            + _p_el(col, v, t) - _p_el(col, v, col.t_ref))


def k_t(v: float, t: float, col: Column = LIQUID) -> float:
    """K_T(V, T) [Pa]."""
    xx = (v / col.v0) ** (1.0 / 3.0)
    k_cold = (col.k0 * xx ** -2 * math.exp(col.eta * (1.0 - xx))
              * (1.0 + (1.0 - xx) * (col.eta * xx + 1.0)))
    return (k_cold + _k_t_th(col, v, t) - _k_t_th(col, v, col.t_ref)
            + _k_t_el(col, v, t) - _k_t_el(col, v, col.t_ref))


def volume_at(p: float, t: float, col: Column = LIQUID) -> float:
    """P, T 에서 몰부피 [m³/mol]. P(V) 는 단조감소라 뿌리가 하나다.

    ⚠ **이 자리가 적분기의 안쪽 고리다** (브리프 180 C). 첫 판은 200회 이분법이었고, γ 가 걸음마다
    이것을 부르니 `core_state` 한 판이 2 분을 넘겼다 — 답은 맞고 **쓸 수 없이 느렸다.** 그래서
    Newton 으로 바꾸고(수치미분, 보통 4–6회) 이분법은 **발산했을 때의 안전망**으로만 남긴다.
    `interior.py` 의 밀도 뒤집기가 같은 이유로 같은 모양이다."""
    v = col.v0 * 0.9
    for _ in range(40):
        f = pressure(v, t, col) - p
        if abs(f) < 1.0:                      # 1 Pa. P 는 GPa 규모라 상대오차 1e-11 이하다
            convergence.note("fe_liquid.volume_newton", True)
            return v
        h = v * 1e-6
        dfdv = (pressure(v + h, t, col) - pressure(v - h, t, col)) / (2.0 * h)
        if dfdv == 0.0:
            break
        step = f / dfdv
        v_new = v - step
        if not (0.2 * col.v0 < v_new < 1.5 * col.v0):  # 창을 벗어나면 Newton 을 믿지 않는다
            break
        if abs(step) < v * 1e-12:
            convergence.note("fe_liquid.volume_newton", True)
            return v_new
        v = v_new
    # ⚠ Newton 이 기준으로 못 나갔다 — 창 밖으로 튀었거나 도함수가 죽었거나 예산을 다 썼다.
    #   아래 이분법은 **그 실패의 안전망**이고, 기준 가지가 없어 상태가 `None` 이다 (브리프 189).
    convergence.note("fe_liquid.volume_newton", False)
    convergence.note("fe_liquid.volume_bisect", None,
                     bracket_valid=convergence.bracket_valid(
                         pressure(0.2 * col.v0, t, col) - p,
                         pressure(1.5 * col.v0, t, col) - p))
    lo, hi = 0.2 * col.v0, 1.5 * col.v0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if pressure(mid, t, col) > p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


#: (열, P, T) → 결과. 적분기가 같은 자리를 여러 번 묻는다 (K_S 와 γ, 그리고 걸음의 반 칸 차분).
#: ⚠ **열 이름이 키에 들어간다** — 두 상이 같은 (P, T) 를 묻는데 캐시가 상을 모르면 한쪽의 값이
#:   다른 쪽에 배달된다.
_CACHE: dict[tuple[str, float, float], dict] = {}
_CACHE_MAX = 4096


def thermal_at(p: float, t: float, col: Column = LIQUID) -> dict:
    """이 세트가 공급하는 셋 — (∂P/∂T)_V [Pa/K] · c_V [J/(kg·K)] · γ [무차원].

    γ 는 새 상수가 아니라 항등식 γ = (∂P/∂T)_V · V / C_V 다 — `eos.Phase.gruneisen` 이
    ρ c_V 로 쓰는 것과 같은 양이고, 여기서는 몰부피로 쓴다. (∂P/∂T)_V 자체는 식 (12) 이고,
    전자 몫은 식 (17) 블록의 gC_Ve/V 다."""
    key = (col.name, p, t)
    hit = _CACHE.get(key)
    if hit is not None:
        return hit
    v = volume_at(p, t, col)
    c_v_mol = _c_v_th(col, v, t) + _c_v_el(col, v, t)
    dpdt = (_gamma_v(col, v / col.v0) * _c_v_th(col, v, t) / v
            + col.g_el * _c_v_el(col, v, t) / v)
    out = {"dpdt_v": dpdt,
           "c_v": c_v_mol / MOLAR_MASS,
           "gruneisen": dpdt * v / c_v_mol,
           "k_t": k_t(v, t, col),
           "density": MOLAR_MASS / v}
    if len(_CACHE) < _CACHE_MAX:
        _CACHE[key] = out
    return out


def thermal_at_hcp(p: float, t: float) -> dict:
    """hcp (ε) 열로 같은 식을 돈다 — `eos.THERMAL_EVALUATORS` 가 이름으로 잡는다 (브리프 187)."""
    return thermal_at(p, t, HCP)


#: 예전 이름. `fe_prem` 의 세트가 문자열로 들고 있으므로 남긴다.
REF = LIQUID.ref
