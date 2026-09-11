# 층 유동학에서 degree-2 조석 Love 수(k₂·h₂·l₂)와 소산 Q 를 레올로지 밴드로 낸다 — 배출만, 선언값은 안 건드린다
"""Degree-2 tidal Love numbers and dissipation from a layered body.

    from tidal_response import solve_response

체인은 보유 논문 안에서 닫힌다.

* **액체 핵** — Saito 1974 §2.3. μ = 0 이면 퍼텐셜이 변위에서 풀려서 (y₅, y₇) 두
  변수로 적분된다(식 18), 중심 출발값은 식 (19), 핵-맨틀 경계에서 고체층으로 올라갈
  **독립 출발 벡터 셋**이 식 (20) 이다. Beuthe 가 Takeuchi & Saito 1972 I(98)–I(103)
  으로 넘긴 자리가 여기서 닫힌다 — 그 논문은 미보유다.
* **고체층** — Beuthe 2015 식 (13)–(18), degree n 의 여섯 ODE.
* **표면** — 식 (5) 세 조건으로 조합을 풀고, 식 (7) 이 Love 수를 읽는다.
* **레올로지** — Bagheri+ 2022 식 (7)(8) Maxwell, (21) Andrade, (26)(27) Sundberg–Cooper.
  셋 다 낸다. **고르지 않는다** — 그건 오너 결정이다.

⚠ **고체 핵은 이름 붙은 거절이다.** μ > 0 인 핵은 출발해가 T&S 1972 에 있고 미보유라,
지어내지 않고 거절한다. 선언으로 갈리는 자리다.

⚠ **정적 한계를 몸 전체에 적용한다** (Beuthe 식 22, "typically applied to the whole
body [e.g. Wahr et al., 2006]"). 점탄성은 ω² 관성항이 아니라 **복소 μ̃(ω)** 로 들어온다.
그래서 액체 핵(Saito 정적 해)과 고체층 사이에 이어붙일 가정이 남지 않는다 — 둘 다
정적이다. ω² 항은 코드에 인쇄된 대로 들어 있고 `STATIC_LIMIT` 하나로 꺼져 있다.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from payload import Result, out_of_domain
from registry import recipe

RECIPE = "tidal-response-methodology"
VERSION = "1"

REFS = (
    "2015Icar..258..239B",      # Beuthe 2015 — 전파자 식 (13)–(18), 표면 식 (5)(7), 막 한계 (27)
    "2022AdGeo..63..231B",      # Bagheri+ 2022 — 세 레올로지의 복소 컴플라이언스, Q
    "1981GeoJ...64..677W",      # Wahr 1981 — J1 의 탄성 지구 기준선
)

#: Saito 1974 는 ADS 기록이 없어 bibcode 가 없다 — 캐시 파일 키로 적는다.
SAITO_1974 = "_saito1974"        # J. Phys. Earth 22, 123-140 (J-STAGE), 식 (17)–(20)

G = 6.67430e-11
EARTH_RADIUS_M = 6.371e6
EARTH_MASS_KG = 5.9722e24

#: ⚠ **정적 한계**(Beuthe 식 22). 끄면 식 (14)(16) 의 −ω²ρ_r 항이 살아나는데, 그러면
#: 액체 핵이 Saito 의 **정적** 해인 것과 어긋난다. 그 어긋남을 이름 붙여 안고 가느니
#: 논문이 인쇄한 «몸 전체 정적» 을 택했다. 바꾸는 것은 별도 등록감이다.
STATIC_LIMIT = True

#: 층 하나를 적분하는 RK4 걸음 수. 500 에서 1000 으로 올려도 지구 k₂ 가 1e-6 안에서
#: 안 움직이는 것을 시험이 고정한다.
STEPS_PER_LAYER = 500

RHEOLOGIES = ("maxwell", "andrade", "sundberg_cooper")

#: 액체층 처리의 라벨. 바다는 막 한계고, 그것이 모든 출력에 붙는다.
MEMBRANE_LABEL = "membrane_limit (Beuthe 2015 eq. 27)"
STATIC_LABEL = "static limit applied to the whole body (Beuthe 2015 eq. 22)"


class Refusal(Exception):
    """이름 붙은 거절. 값이 아니라 문장으로 나간다."""


@dataclass(frozen=True)
class Layer:
    """균질 층 하나. ρ 는 선언 질량분율에서, μ·η 는 선언에서 온다."""

    name: str
    r_inner: float              # m
    r_outer: float              # m
    rho: float                  # kg/m³
    state: str                  # solid | liquid
    mu_pa: float = 0.0
    eta_pa_s: float = 0.0
    poisson: float = 0.5        # 선언이 없으면 비압축(ν = 1/2 → χ = 0)
    andrade_alpha: float = 0.0
    andrade_zeta: float = 0.0
    sc_delta_j: float = 0.0
    sc_tau: float = 0.0
    mu_source: str = "declared"

    @property
    def volume(self) -> float:
        return 4.0 / 3.0 * math.pi * (self.r_outer ** 3 - self.r_inner ** 3)

    @property
    def mass(self) -> float:
        return self.rho * self.volume


# ──────────────────────────────────────────────────────────────────────────
# 레올로지 — Bagheri+ 2022. 복소 컴플라이언스 J̄(χ) 를 인쇄된 대로 짓고 μ̃ = 1/J̄.
# ──────────────────────────────────────────────────────────────────────────

def complex_mu(layer: Layer, omega: float, rheology: str) -> complex:
    """층의 복소 전단탄성률 μ̃(ω). 대응원리는 μ 하나에만 적용한다."""
    if layer.mu_pa <= 0.0:
        return 0.0 + 0.0j
    j_u = 1.0 / layer.mu_pa
    if layer.eta_pa_s <= 0.0:
        raise Refusal(f"layer '{layer.name}': viscosity is not declared, "
                      f"and all three rheologies need it")
    tau_m = layer.eta_pa_s / layer.mu_pa          # Bagheri 식 (9)
    x = omega

    if rheology == "maxwell":
        # Bagheri 식 (7)(8): ℜ[J̄] = J, ℑ[J̄] = −J/(χ τ_M)
        j_bar = j_u * (1.0 - 1.0j / (x * tau_m))
    elif rheology == "andrade":
        if layer.andrade_alpha <= 0.0 or layer.andrade_zeta <= 0.0:
            raise Refusal(f"layer '{layer.name}': Andrade needs alpha and zeta, "
                          f"and this body declares neither")
        a = layer.andrade_alpha
        tau_a = layer.andrade_zeta * tau_m        # Andrade time, 식 (20) 의 τ_A
        # Bagheri 식 (21): J̄ = J_U [ 1 + (iχτ_A)^(−α) Γ(1+α) − i (χ τ_M)^(−1) ]
        j_bar = j_u * (1.0
                       + (1.0j * x * tau_a) ** (-a) * math.gamma(1.0 + a)
                       - 1.0j / (x * tau_m))
    elif rheology == "sundberg_cooper":
        if layer.andrade_alpha <= 0.0 or layer.andrade_zeta <= 0.0:
            raise Refusal(f"layer '{layer.name}': Sundberg-Cooper carries the Andrade "
                          f"term, so it needs alpha and zeta too")
        if layer.sc_delta_j <= 0.0 or layer.sc_tau <= 0.0:
            raise Refusal(f"layer '{layer.name}': Sundberg-Cooper needs the anelastic "
                          f"pair (delta_J, tau), and this body declares neither")
        a, d, t = layer.andrade_alpha, layer.sc_delta_j, layer.sc_tau
        tau_a = layer.andrade_zeta * tau_m
        # Bagheri 식 (26)(27) 을 실수부·허수부로 그대로 짓는다.
        re = j_u * (1.0 + math.gamma(1.0 + a) * (x * tau_a) ** (-a) * math.cos(a * math.pi / 2.0)
                    + d / (1.0 + x * x * t * t))
        im = -j_u * (math.gamma(1.0 + a) * (x * tau_a) ** (-a) * math.sin(a * math.pi / 2.0)
                     + x * t * d / (1.0 + x * x * t * t)
                     + 1.0 / (x * tau_m))
        j_bar = complex(re, im)
    else:
        raise Refusal(f"unknown rheology '{rheology}'")
    return 1.0 / j_bar


# ──────────────────────────────────────────────────────────────────────────
# 액체 핵 — Saito 1974 §2.3, 식 (18)(19)(20).
# ──────────────────────────────────────────────────────────────────────────

def _core_potential(n: int, rho: float, r_cmb: float, steps: int) -> tuple[float, float]:
    """중심에서 핵-맨틀 경계까지 (y₅, y₇) 를 올린다.

    Saito 식 (18) —
        ẏ₅ = (4πGρ/g − (n+1)/r) y₅ + y₇
        ẏ₇ = (2(n−1)/r)(4πGρ/g) y₅ + ((n−1)/r − 4πGρ/g) y₇
    출발값은 식 (19) — y₅ = rⁿ, r y₇ = 2(n−1) rⁿ.

    ⚠ 핵이 균질이면 g = (4/3)πGρ r 이라 4πGρ/g = 3/r 이다. 그래도 식을 그대로 둔다 —
    나중에 층이 쪼개지면 ρ 가 층마다 달라진다.
    """
    r0 = r_cmb / steps                       # 중심의 특이점을 한 걸음 비켜서 출발한다
    y5 = r0 ** n
    y7 = 2.0 * (n - 1) * r0 ** (n - 1)

    def rhs(r: float, y5: float, y7: float) -> tuple[float, float]:
        g_r = 4.0 / 3.0 * math.pi * G * rho * r
        a = 4.0 * math.pi * G * rho / g_r
        return ((a - (n + 1) / r) * y5 + y7,
                (2.0 * (n - 1) / r) * a * y5 + ((n - 1) / r - a) * y7)

    h = (r_cmb - r0) / steps
    r = r0
    for _ in range(steps):
        k1 = rhs(r, y5, y7)
        k2 = rhs(r + h / 2, y5 + h / 2 * k1[0], y7 + h / 2 * k1[1])
        k3 = rhs(r + h / 2, y5 + h / 2 * k2[0], y7 + h / 2 * k2[1])
        k4 = rhs(r + h, y5 + h * k3[0], y7 + h * k3[1])
        y5 += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        y7 += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        r += h
    return y5, y7


def _cmb_start_vectors(n: int, rho_l: float, g_b: float,
                       y5c: float, y7c: float) -> list[list[complex]]:
    """Saito 식 (20) — 핵-맨틀 경계에서 고체층으로 올라갈 세 독립 출발 벡터.

    적분상수는 y₁(b) 와 y₃(b), 그리고 핵 퍼텐셜 해의 규격화 하나다.

    * set 1 — y₁(b) = 0 이고 핵의 퍼텐셜 해를 싣는다. 유체 구속(식 25)이
      y₂ = ρ(g y₁ − y₅) 이므로 y₂ = −ρ y₅ᶜ, 식 (17) 이 y₆ = y₇ᶜ + (4πGρ/g) y₅ᶜ.
    * set 2 — y₁(b) = 1, 퍼텐셜 없음. y₂ = ρ g, y₆ = −4πGρ.
    * set 3 — y₃(b) = 1, 나머지 0.

    ⚠ 세 집합은 인쇄된 자리 그대로다. 그리고 **식 (25)(17) 로 되짚으면 서로 맞는다** —
    그것이 페이지 이미지에서 읽은 아래첨자가 맞다는 증거다(글자 모양이 아니라 식으로).
    """
    return [
        [0.0 + 0j, -rho_l * y5c + 0j, 0.0 + 0j, 0.0 + 0j,
         y5c + 0j, y7c + 4.0 * math.pi * G * rho_l / g_b * y5c + 0j],
        [1.0 + 0j, rho_l * g_b + 0j, 0.0 + 0j, 0.0 + 0j,
         0.0 + 0j, -4.0 * math.pi * G * rho_l + 0j],
        [0.0 + 0j, 0.0 + 0j, 1.0 + 0j, 0.0 + 0j, 0.0 + 0j, 0.0 + 0j],
    ]


# ──────────────────────────────────────────────────────────────────────────
# 고체층 — Beuthe 2015 식 (13)–(18).
# ──────────────────────────────────────────────────────────────────────────

def _beuthe_rhs(r: float, y: list[complex], n: int, rho: float,
                mu: complex, nu: float, m_offset: float, omega: float) -> list[complex]:
    """식 (13)–(18) 을 인쇄된 대로. χ = (1−2ν)/(1−ν), xₙ = (n−1)(n+2).

    `m_offset` 는 m(r) = m_offset + (4/3)πρ r³ 이 되도록 층 아래 질량에서 미리 뺀 상수다.
    """
    chi = (1.0 - 2.0 * nu) / (1.0 - nu)
    xn = (n - 1) * (n + 2)
    m_r = m_offset + 4.0 / 3.0 * math.pi * rho * r ** 3
    g_r = G * m_r / (r * r)
    w2 = 0.0 if STATIC_LIMIT else omega * omega
    nn = n * (n + 1)
    shear = 2.0 * y[0] - nn * y[2]

    dy1 = chi / (2.0 * mu) * y[1] - (1.0 - chi) / r * shear
    dy2 = (-w2 * rho * y[0]
           - 2.0 / r * chi * y[1]
           + 1.0 / (r * r) * (2.0 * mu * (1.0 + nu) / (1.0 - nu) - rho * g_r * r) * shear
           + nn / r * y[3]
           - rho * (y[5] - (n + 1) / r * y[4] + 2.0 / r * g_r * y[0]))
    dy3 = y[3] / mu + (y[2] - y[0]) / r
    dy4 = (-w2 * rho * y[2]
           - (1.0 - chi) / r * y[1]
           - 2.0 / (r * r) * mu * ((1.0 + nu) / (1.0 - nu) * y[0]
                                   - (xn + 1.0 + nu) / (1.0 - nu) * y[2])
           - 3.0 / r * y[3]
           - rho / r * (y[4] - g_r * y[0]))
    dy5 = y[5] + 4.0 * math.pi * G * rho * y[0] - (n + 1) / r * y[4]
    dy6 = (n - 1) / r * y[5] + 4.0 * math.pi * G * rho / r * (n + 1) * (y[0] - n * y[2])
    return [dy1, dy2, dy3, dy4, dy5, dy6]


def _integrate_layer(y: list[complex], layer: Layer, n: int, mu: complex,
                     m_below: float, omega: float, steps: int) -> list[complex]:
    """층 하나를 RK4 로 올린다. ρ·μ 는 층 안에서 상수다.

    `m_below` 는 **층 바닥 아래**의 질량이다 — 위가 아니다. 한 번 헷갈렸던 자리라 이름에
    적어 둔다.
    """
    h = (layer.r_outer - layer.r_inner) / steps
    r = layer.r_inner
    m_offset = m_below - 4.0 / 3.0 * math.pi * layer.rho * layer.r_inner ** 3

    def f(rr, yy):
        return _beuthe_rhs(rr, yy, n, layer.rho, mu, layer.poisson, m_offset, omega)

    for _ in range(steps):
        k1 = f(r, y)
        k2 = f(r + h / 2, [y[i] + h / 2 * k1[i] for i in range(6)])
        k3 = f(r + h / 2, [y[i] + h / 2 * k2[i] for i in range(6)])
        k4 = f(r + h, [y[i] + h * k3[i] for i in range(6)])
        y = [y[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(6)]
        r += h
    return y


def _love_numbers(layers: list[Layer], n: int, omega: float,
                  rheology: str, steps: int = STEPS_PER_LAYER) -> dict:
    """액체 핵 → 고체층 → 표면 조건 → 식 (7)."""
    core = layers[0]
    if core.state != "liquid":
        raise Refusal("solid core start values live in Takeuchi & Saito 1972 "
                      "I(98)-I(103), which is not held — declare the core liquid "
                      "or this recipe does not start")

    r_b = core.r_outer
    m_core = core.mass
    g_b = G * m_core / (r_b * r_b)
    y5c, y7c = _core_potential(n, core.rho, r_b, steps)
    sols = _cmb_start_vectors(n, core.rho, g_b, y5c, y7c)

    m_inner = m_core
    for layer in layers[1:]:
        mu = complex_mu(layer, omega, rheology)
        if mu == 0:
            # ⚠ **부수적 거절이 아니라 이 빌드의 경계다.** Beuthe 식 (27) 은 «유체층이
            #   표면에 닿을 때»(surface ocean / quasi-fluid crust) 성립하는 Love 수 관계다 —
            #   얼음 껍질 **아래**의 바다에 쓰는 식이 아니다. 그 경우는 §3 의 막 접근
            #   (유효 매개변수 Λ·δρ°)이고 이 빌드에 없다. 그리고 액체층 위로 다시 고체로
            #   올라가려면 식 (20) 의 «유체 위에서의 출발 벡터» 에 해당하는 것이 필요한데,
            #   Saito 는 그것을 핵-맨틀 경계에 대해서만 인쇄한다.
            raise Refusal(
                f"layer '{layer.name}' is liquid and sits above a solid layer. "
                f"Beuthe eq. (27) is the relation for a fluid layer that reaches the "
                f"SURFACE, not for an ocean under an ice shell; the subsurface case is "
                f"the membrane approach of his section 3 and is not built here. "
                f"Saito 1974 eq. (20) prints start vectors only at the core-mantle "
                f"boundary, so re-entering a solid layer above a fluid has no printed start")
        sols = [_integrate_layer(s, layer, n, mu, m_inner, omega, steps) for s in sols]
        m_inner += layer.mass

    r_s = layers[-1].r_outer
    g_s = G * m_inner / (r_s * r_s)

    # Beuthe 식 (5) — (y₂, y₄, y₆)(R) = (0, 0, (2n+1)/R).
    rhs = [0.0 + 0j, 0.0 + 0j, (2.0 * n + 1.0) / r_s + 0j]
    a = [[sols[j][i] for j in range(3)] for i in (1, 3, 5)]
    c = _solve3(a, rhs)
    y = [sum(c[j] * sols[j][i] for j in range(3)) for i in range(6)]

    # Beuthe 식 (7) — (hₙ, lₙ, kₙ) = (g y₁(R), g y₃(R), y₅(R) − 1).
    h_n = g_s * y[0]
    l_n = g_s * y[2]
    k_n = y[4] - 1.0
    q = abs(k_n.real / k_n.imag) if k_n.imag else float("inf")
    return {"k2": k_n, "h2": h_n, "l2": l_n, "q": q}


def _solve3(a: list[list[complex]], b: list[complex]) -> list[complex]:
    """3×3 복소 선형계. 가우스 소거에 부분 피벗."""
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(3):
        piv = max(range(col, 3), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) == 0.0:
            raise Refusal("the three solutions are not independent at the surface — "
                          "the propagator lost its conditioning")
        m[col], m[piv] = m[piv], m[col]
        for r in range(col + 1, 3):
            f = m[r][col] / m[col][col]
            for k in range(col, 4):
                m[r][k] -= f * m[col][k]
    x = [0j, 0j, 0j]
    for r in (2, 1, 0):
        s = m[r][3] - sum(m[r][k] * x[k] for k in range(r + 1, 3))
        x[r] = s / m[r][r]
    return x


# ──────────────────────────────────────────────────────────────────────────
# 층 사상 — 선언 층 이름 → (r_inner, r_outer). C62 (b) 의 고정 표.
# ──────────────────────────────────────────────────────────────────────────

def build_layers(radius_m: float, core_radius_m: float, mass_kg: float,
                 cmf: float, imf: float, declared: list[dict],
                 ocean_m: float = 0.0, ice_shell_m: float = 0.0,
                 crust_m: float = 0.0) -> list[Layer]:
    """경계 반지름에서 층 목록을 짓는다. 선언과 안 맞으면 이름 붙은 거절이다.

    ⚠ **맨틀 위쪽은 «존재하는 상위 경계 중 최소»** 다. 지각 바닥은 암석체의 원시 지각
    자리라 바다 천체에서 None 이고, 그때 «지각 바닥 아니면 표면» 규칙은 맨틀이 표면까지
    올라가 바다와 얼음 껍질을 **두 번 덮는다**. 전파자는 그 구간을 두 번 적분하고,
    이름 검사로는 안 잡힌다 — 다섯 이름이 다 경계를 찾기 때문이다.
    """
    r_ocean_top = radius_m - ice_shell_m if ice_shell_m > 0.0 else None
    r_ocean_base = (r_ocean_top - ocean_m) if (r_ocean_top and ocean_m > 0.0) else None
    r_crust_base = radius_m - crust_m if crust_m > 0.0 else None

    if imf > 0.0 and r_ocean_base is None and r_ocean_top is None:
        raise Refusal("ice column present (ice mass fraction > 0), no radius boundary "
                      "for it in the solved structure")

    uppers = [b for b in (r_crust_base, r_ocean_base, radius_m) if b is not None]
    bounds = {
        "core": (0.0, core_radius_m),
        "mantle": (core_radius_m, min(uppers)),
    }
    if r_crust_base is not None:
        bounds["crust"] = (r_crust_base, radius_m)
    if r_ocean_base is not None:
        bounds["ocean"] = (r_ocean_base, r_ocean_top)
    if r_ocean_top is not None:
        bounds["ice_shell"] = (r_ocean_top, radius_m)

    names = {d["name"] for d in declared}
    for missing in sorted(names - set(bounds)):
        raise Refusal(f'layer "{missing}" declared but absent from the solve')
    for extra in sorted(set(bounds) - names):
        raise Refusal(f'solve has layer "{extra}" with no tidal declaration')

    _check_coverage(bounds, radius_m)

    rock_names = [k for k in ("mantle", "crust") if k in bounds]
    ice_names = [k for k in ("ocean", "ice_shell") if k in bounds]
    masses = {"core": cmf * mass_kg}
    rock_mass = (1.0 - cmf - imf) * mass_kg
    ice_mass = imf * mass_kg
    for group, total in ((rock_names, rock_mass), (ice_names, ice_mass)):
        vol = sum(_shell_volume(*bounds[k]) for k in group)
        if vol <= 0.0:
            continue
        for k in group:                       # ⚠ 한 기둥은 한 밀도다 — 라벨이 그렇게 말한다
            masses[k] = total * _shell_volume(*bounds[k]) / vol

    spec = {d["name"]: d for d in declared}
    out = []
    for name in ("core", "mantle", "ocean", "ice_shell", "crust"):
        if name not in bounds:
            continue
        lo, hi = bounds[name]
        d = spec[name]
        out.append(Layer(name=name, r_inner=lo, r_outer=hi,
                         rho=masses[name] / _shell_volume(lo, hi),
                         state=d.get("state", "solid"),
                         mu_pa=float(d.get("mu_pa", 0.0) or 0.0),
                         eta_pa_s=float(d.get("eta_pa_s", 0.0) or 0.0),
                         poisson=float(d.get("poisson", 0.5)),
                         andrade_alpha=float(d.get("andrade_alpha", 0.0) or 0.0),
                         andrade_zeta=float(d.get("andrade_zeta", 0.0) or 0.0),
                         sc_delta_j=float(d.get("sc_delta_j", 0.0) or 0.0),
                         sc_tau=float(d.get("sc_tau", 0.0) or 0.0),
                         mu_source=d.get("mu_source", "declared")))
    out.sort(key=lambda lay: lay.r_inner)
    return out


def _shell_volume(lo: float, hi: float) -> float:
    return 4.0 / 3.0 * math.pi * (hi ** 3 - lo ** 3)


def _check_coverage(bounds: dict, radius_m: float, tol: float = 1e-6) -> None:
    """층 구간이 [0, R] 을 빈틈도 겹침도 없이 덮는가.

    ⚠ 겹침은 어떤 이름 거절로도 안 잡힌다 — 다섯 이름이 다 경계를 찾은 상태에서
    구간만 겹치기 때문이다. 그래서 이 검사가 따로 있다.
    """
    edges = sorted(bounds.values())
    if abs(edges[0][0]) > tol * radius_m:
        raise Refusal("layer coverage does not start at the centre")
    for (lo0, hi0), (lo1, hi1) in zip(edges, edges[1:]):
        if abs(hi0 - lo1) > tol * radius_m:
            kind = "gap" if hi0 < lo1 else "overlap"
            raise Refusal(f"layer coverage has a {kind} at r = {hi0:.0f} m — "
                          f"the propagator would integrate it {'0' if kind == 'gap' else '2'} times")
    if abs(edges[-1][1] - radius_m) > tol * radius_m:
        raise Refusal("layer coverage does not reach the surface")


def g_surface_identity(layers: list[Layer], mass_kg: float, radius_m: float) -> float:
    """g(R) 을 층 질량에서 다시 지어 G·M/R² 와 맞추는 **산술 항등식**.

    ⚠ 이름을 그렇게 지은 이유가 있다. 층 밀도를 선언 분율에서 지었으므로 Σm_i = M 은
    구성상 참이고, 이 줄이 잡는 것은 «덮음에 빈틈·겹침이 없고 분율의 합이 1» 뿐이다.
    **적분기가 실제로 푼 구조와 이 층 더미가 같은지는 말하지 못한다** — 그건 J9 가
    잰다. 구조 검증으로 읽히지 않게 이름에 identity 를 넣었다.
    """
    built = G * sum(lay.mass for lay in layers) / (radius_m * radius_m)
    want = G * mass_kg / (radius_m * radius_m)
    return abs(built - want) / want


def homogeneous_nmoi(layers: list[Layer], mass_kg: float, radius_m: float) -> float:
    """층별 균질 더미의 C/MR² — Σ (8π/15) ρᵢ (r_o⁵ − r_i⁵) / (M R²). J9 의 좌변."""
    moi = sum(8.0 / 15.0 * math.pi * lay.rho * (lay.r_outer ** 5 - lay.r_inner ** 5)
              for lay in layers)
    return moi / (mass_kg * radius_m * radius_m)


# ──────────────────────────────────────────────────────────────────────────
# 밴드 — 세 레올로지를 다 내고, 못 내는 것은 이름을 적는다.
# ──────────────────────────────────────────────────────────────────────────

def solve_response(layers: list[Layer], forcing_period_s: float, n: int = 2) -> dict:
    """세 레올로지의 Love 수와 Q, 그리고 밴드."""
    if forcing_period_s <= 0.0:
        raise Refusal("forcing period is not declared, and no orbital period reached "
                      "this node")
    omega = 2.0 * math.pi / forcing_period_s
    members, refused = {}, {}
    for rh in RHEOLOGIES:
        try:
            members[rh] = _love_numbers(layers, n, omega, rh)
        except Refusal as exc:
            refused[rh] = str(exc)
    if not members:
        raise Refusal("every rheology refused — " + " · ".join(
            f"{k}: {v}" for k, v in refused.items()))
    out = {"members": members, "refused": refused,
           "rheology_members_emitted": sorted(members)}
    for key in ("k2", "h2", "l2", "q"):
        vals = [abs(m[key]) if isinstance(m[key], complex) else m[key]
                for m in members.values()]
        out[key] = {rh: members[rh][key] for rh in members}
        out[f"{key}_band"] = [min(vals), max(vals)]
    kq = [abs(m["k2"]) / m["q"] for m in members.values() if m["q"] not in (0, float("inf"))]
    out["k2_over_q_band"] = [min(kq), max(kq)] if kq else None
    return out


def elastic_love(layers: list[Layer], n: int = 2) -> dict:
    """탄성 한계(ω → ∞). J1 이 서는 자리 — 점탄성 항이 사라지고 μ 가 실수로 남는다."""
    core = layers[0]
    if core.state != "liquid":
        raise Refusal("solid core start values live in Takeuchi & Saito 1972 "
                      "I(98)-I(103), which is not held")
    r_b = core.r_outer
    g_b = G * core.mass / (r_b * r_b)
    y5c, y7c = _core_potential(n, core.rho, r_b, STEPS_PER_LAYER)
    sols = _cmb_start_vectors(n, core.rho, g_b, y5c, y7c)
    m_inner = core.mass
    for layer in layers[1:]:
        sols = [_integrate_layer(s, layer, n, complex(layer.mu_pa, 0.0),
                                 m_inner, 0.0, STEPS_PER_LAYER) for s in sols]
        m_inner += layer.mass
    r_s = layers[-1].r_outer
    g_s = G * m_inner / (r_s * r_s)
    a = [[sols[j][i] for j in range(3)] for i in (1, 3, 5)]
    c = _solve3(a, [0j, 0j, (2.0 * n + 1.0) / r_s + 0j])
    y = [sum(c[j] * sols[j][i] for j in range(3)) for i in range(6)]
    return {"k2": (y[4] - 1.0).real, "h2": (g_s * y[0]).real, "l2": (g_s * y[2]).real}


# ──────────────────────────────────────────────────────────────────────────
# 노드 어댑터
# ──────────────────────────────────────────────────────────────────────────

def _composition_fractions(state) -> tuple[float, float, bool, str, list[str]]:
    """cmf·imf 를 선언 → 프리셋 → 이름 붙은 거절 순으로 얻는다 (C28/C65 길).

    ⚠ 여기서 거절해 버리면 **엔진 답이 둘** 이 된다 — `interior.solve` 는 cmf 가 없으면
    프리셋 슬롯 0 을 조용히 쓰고 반지름을 내기 때문이다(C65 (a) 가 이름 붙인 자리).
    그래서 같은 길을 가고, 프리셋을 썼다는 사실은 **이 노드의 값**으로 샌다.
    """
    from interior import COMPOSITIONS

    cmf = state.get_optional("core_mass_fraction")
    imf = state.get_optional("ice_mass_fraction")
    intent = state.get_optional("composition_intent")
    notes, used, name = [], False, ""
    if cmf is None or imf is None:
        if not intent or intent not in COMPOSITIONS:
            raise Refusal(
                "cannot-say (no composition preset): this body declares no core or ice "
                "mass fraction and no usable composition_intent. ⚠ If its composition was "
                "reached by inversion, that value lives in interior_layers' inputs and is "
                "not visible in state — it was inverse-solved, not undeclared")
        preset = COMPOSITIONS[intent]
        used, name = True, intent
        if cmf is None:
            cmf = preset[0]
            notes.append(f"core mass fraction from the preset '{intent}' "
                         f"(interior.COMPOSITIONS slot 0) = {cmf}")
        if imf is None:
            imf = preset[1]
            notes.append(f"ice mass fraction from the preset '{intent}' "
                         f"(interior.COMPOSITIONS slot 1, the C28 rule) = {imf}")
    return float(cmf), float(imf), used, name, notes


@recipe("tidal_response")
def _(state) -> Result:
    declared = state.get_optional("tidal_response")
    if not declared:
        # ⚠ **빈 조회를 증거에 이름으로 남기지 않는다** (C37, 클래스 ①). 예전 초안은
        #   `inputs = {"tidal_response": None}` 을 적었고, 그러면 «모든 조회가 미스인데
        #   그 None 이 같은 이름으로 증거에 앉는» 모양이 된다 — 없는 것을 있는 것처럼
        #   읽히게 하는 자리다. 부재는 `reason` 이 말한다.
        return out_of_domain(
            RECIPE, VERSION,
            "this body declares no tidal_response block, so the node does not run — "
            "an absence, not a refusal",
            {}, refs=REFS)
    inputs = {"tidal_response": declared}

    radius = state.get_optional("radius")
    core_radius = state.get_optional("core_radius")
    mass_earth = state.get_optional("mass_earth")
    inputs.update({"radius": radius, "core_radius": core_radius,
                   "mass_earth": mass_earth})
    ocean = state.get_optional("ocean_thickness") or 0.0
    ice_shell = state.get_optional("ice_shell_thickness") or 0.0
    crust = state.get_optional("crust_thickness") or 0.0
    inputs.update({"ocean_thickness": ocean, "ice_shell_thickness": ice_shell,
                   "crust_thickness": crust})

    try:
        if radius is None or core_radius is None or mass_earth is None:
            raise Refusal("the solved structure did not reach this node — "
                          "radius, core_radius and mass_earth are all required")
        cmf, imf, preset_used, preset_name, notes = _composition_fractions(state)
        inputs.update({"core_mass_fraction": cmf, "ice_mass_fraction": imf,
                       "composition_intent": state.get_optional("composition_intent")})
        layers = build_layers(
            radius_m=radius * EARTH_RADIUS_M,
            core_radius_m=core_radius * EARTH_RADIUS_M,
            mass_kg=mass_earth * EARTH_MASS_KG,
            cmf=cmf, imf=imf,
            declared=declared.get("layers", []),
            ocean_m=ocean * 1e3, ice_shell_m=ice_shell * 1e3, crust_m=crust * 1e3)
        band = solve_response(layers, float(declared.get("forcing_period_s", 0.0)))
    except Refusal as exc:
        return out_of_domain(RECIPE, VERSION, str(exc), inputs, refs=REFS)

    mass_kg = mass_earth * EARTH_MASS_KG
    radius_m = radius * EARTH_RADIUS_M
    values = {
        "k2": band["k2_band"][0], "h2": band["h2_band"][0],
        "l2": band["l2_band"][0], "q": band["q_band"][0],
        "k2_band": band["k2_band"], "h2_band": band["h2_band"],
        "l2_band": band["l2_band"], "q_band": band["q_band"],
        "k2_over_q_emitted": band["k2_over_q_band"],
        "layer_q": {lay.name: band["q_band"] for lay in layers},
        "rheology_members_emitted": band["rheology_members_emitted"],
        "liquid_layer_treatment": MEMBRANE_LABEL,
        "static_limit": STATIC_LABEL,
        "tidal_composition_preset_used": 1 if preset_used else 0,
        "tidal_composition_preset_name": preset_name,
        "g_surface_identity": g_surface_identity(layers, mass_kg, radius_m),
        "homogeneous_nmoi": homogeneous_nmoi(layers, mass_kg, radius_m),
    }
    units = {k: "" for k in values}
    for k in ("k2", "h2", "l2", "q", "g_surface_identity", "homogeneous_nmoi"):
        units[k] = "dimensionless"
    return Result(
        recipe=RECIPE, version=VERSION, regime="declared",
        reason="a tidal_response block is declared, so the propagator runs on the "
               "layer-homogeneous stack built from the solved boundaries",
        grade="analog", inputs=inputs, values=values, units=units, refs=REFS,
        notes=tuple(notes) + tuple(
            f"{rh} refused: {why}" for rh, why in band["refused"].items()))
