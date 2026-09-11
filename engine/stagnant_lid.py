# 정체뚜껑 대류의 열류 스케일링 — Korenaga 2009 식 29·30·44 를 인쇄된 Table 2 에 대조 가능한 형태로 전사
"""Stagnant-lid heat-flow scaling — Korenaga 2009 (`2009GeoJI.179..154K`).

    python3 engine/stagnant_lid.py     Table 2 의 Δη=1 블록 행별 대조를 출력

**C47 (f), brief 148 단계 1.** 이 모듈이 하는 일은 하나뿐이다 — 논문이 **행으로 인쇄한**
숫자에 우리 전사를 맞춰 보는 것. ⚠ **아직 플럭스를 내지 않는다.** 차원화는 단계 3–4 이고,
절대 스케일에는 앵커가 없다(C47 (c)·(e)).

⚠ **eq. 30 이 아니라 eq. 29 가 시험 대상이다.** 논문은 eq. 30 을 *"In the limit of Nu ≫ 1"*
의 점근형이라 적고, Table 2 의 Nu 는 3.1–7.2 다 — 점근이 아니다. C47 (c) 가 eq. 30 으로
방향 시험을 돌린 것은 그래서 절반만 맞는 시험이었다. 여기서 eq. 29 를 푼다.

⚠ **Table 2 만 앵커가 된다.** Table 1 은 선형지수 블록에 `Nu` 는 인쇄하지만 `Ra_i` 는
Arrhenius 쪽에만 인쇄하므로 (θ, Ra_i, Nu) 세 쌍이 안 나온다. Table 2 의 Δη=1 블록이
이 엔진이 가진 **유일한** 행별 앵커다.
"""
from __future__ import annotations
import convergence

import math

# ── Korenaga 2009 의 인쇄값 ───────────────────────────────────────────────────
#: eq. 29 아래 본문: *"I repeated their regression analysis and obtained that a ≈ 0.30 + 0.25n.
#: The rms error of the fit is ∼1.2 per cent (Fig. 4a)."* ⚠ 그 적합은 **Table 1** 에 대한 것이고
#: 아래 대조는 Table 2 에 대한 것이다 — 적합에 안 쓰인 집합이라 오차가 커지는 게 정상이다.
A_COEFF = (0.30, 0.25)          # a = 0.30 + 0.25 n
#: §2.2 본문: 선형지수 *"a_rh is ∼2.5 (n = 1), ∼3.0 (n = 2) and ∼4.0 (n = 3)"*, Arrhenius 는
#: *"∼2.3 (n = 1), ∼2.9 (n = 2) and ∼3.7 (n = 3)"*. ⚠ Fig. 3 은 θ 에 따라 2.1–3.0 으로 흩어진
#: 것을 보이지만 **본문이 단일값을 쓰므로 단일값을 쓴다** — 그림에서 읽어 오지 않는다.
A_RH_LINEAR_EXP = {1: 2.5, 2: 3.0, 3: 4.0}
A_RH_ARRHENIUS = {1: 2.3, 2: 2.9, 3: 3.7}


def beta(n: int) -> float:
    """eq. 29 아래: *"where β = n/(n + 2)"*."""
    return n / (n + 2.0)


def a_of_n(n: int) -> float:
    """a ≈ 0.30 + 0.25 n — eq. 29 에 적합된 계수."""
    return A_COEFF[0] + A_COEFF[1] * n


def ra_crit(n: int) -> float:
    """eq. 44 — `Ra_crit(n) ≈ exp(3.84 + 2.25/n)`.

    본문이 *"∼450 (n = 1), ∼134 (n = 2) and ∼104 (n = 3)"* 라 적는다. ⚠ n=2 는 이 식이 143 을
    주어 **7 % 어긋난다**; n=1·3 은 맞는다. 우리가 n=2 를 쓰게 되면 여기가 먼저 의심받아야 한다."""
    return math.exp(3.84 + 2.25 / n)


def nu_asymptotic(theta: float, ra_i: float, n: int = 1, a: float | None = None) -> float:
    """eq. 30 — `Nu ≈ a θ^(−1−β) Ra_i^β`. **Nu ≫ 1 에서만** eq. 29 의 극한이다.

    `a` 를 주면 그 선행 상수로 같은 **꼴**을 쓴다 — Foley 2018 식 (3) 이 n=1 에서 이 식과 같은
    지수(−4/3, 1/3)를 갖고 `c₁ = 0.5` 를 쓰기 때문이다 (`mantle_budget.py`, C51). ⚠ 꼴만 공유하고
    **정규화는 공유하지 않는다**: 그쪽 `θ` 와 `Ra_i` 는 퍼텐셜 온도로 세운 것이고 여기 것은
    Korenaga eq. 20 의 `T̄_i` 다. 두 논문의 상수를 섞으면 안 되는 이유가 그것이다."""
    b = beta(n)
    return (a_of_n(n) if a is None else a) * theta ** (-1.0 - b) * ra_i ** b


def nu_preasymptotic(theta: float, ra_i: float, n: int = 1, a_rh: float | None = None) -> float:
    """eq. 29 — `Nu[1 − 2Nu⁻¹(1 − a_rh θ⁻¹)]^(1−β(n+2)/(2n)) = a θ^(−1−β) Ra_i^β`, Nu 로 풀어서.

    ⚠ 쪽 이미지(p. 158)에서 읽었다 — 텍스트 레이어는 이 식의 지수를 깨뜨린다."""
    if a_rh is None:
        a_rh = A_RH_LINEAR_EXP[n]
    b = beta(n)
    expo = 1.0 - b * (n + 2.0) / (2.0 * n)
    rhs = nu_asymptotic(theta, ra_i, n)
    c = 2.0 * (1.0 - a_rh / theta)          # 대괄호 안 = 1 − c/Nu
    lo, hi = max(c, 0.0) + 1e-9, 1.0e4
    # ⚠ **기준 가지가 없는 이분법** — 상태 `None`, 묻는 것은 진입 괄호뿐이다
    #   (브리프 189 Amendment 2).
    convergence.note("stagnant_lid.nu_asymptotic_bisect", None,
                     bracket_valid=convergence.bracket_valid(
                         lo * max(1.0 - c / lo, 0.0) ** expo - rhs,
                         hi * max(1.0 - c / hi, 0.0) ** expo - rhs))
    for _ in range(200):                     # 좌변은 Nu 에 단조증가 — 이분법
        mid = 0.5 * (lo + hi)
        if mid * max(1.0 - c / mid, 0.0) ** expo < rhs:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


#: Table 2 의 **Δη = 1 블록** — *"Numerical results for cases with temperature- and depth-dependent
#: viscosity (n = 1 and θ_H = 50)"*, 각주 *"Viscosity contrast for z* > 0.75 (Δη of 1 denotes no
#: depth-dependency)"*. 열은 `Ra_H,0` · `Δη_a` · `θ` · `Ra_i` · `d*_L` · `Nu` · `v*_rms`.
#: 여기 담은 것은 (θ, Ra_i, Nu) 세 쌍. ⚠ `d*_L` 은 δ 가 아니라 **뚜껑 두께**(eq. 27–28)라 안 쓴다.
THETA_H_TABLE2 = 50.0
TABLE2_DETA1 = (
    (16.05, 2.99e6, 3.12), (15.11, 3.31e6, 3.31), (14.12, 3.84e6, 3.54),
    (13.18, 4.19e6, 3.79), (12.11, 4.41e6, 4.13), (11.11, 4.45e6, 4.50),
    (10.02, 4.50e6, 4.99), (9.03, 4.51e6, 5.54), (7.93, 4.40e6, 6.31),
    (6.93, 4.23e6, 7.22),
)


def table2_residuals(a_rh: float | None = None) -> list[tuple[float, float, float, float]]:
    """Table 2 Δη=1 행별 (θ, Nu 인쇄, Nu eq.29, 오차 %)."""
    out = []
    for theta, ra_i, nu_printed in TABLE2_DETA1:
        pred = nu_preasymptotic(theta, ra_i, 1, a_rh)
        out.append((theta, nu_printed, pred, (pred / nu_printed - 1.0) * 100.0))
    return out


def table2_rms(a_rh: float | None = None) -> float:
    """행별 오차의 rms [%]."""
    errs = [r[3] for r in table2_residuals(a_rh)]
    return math.sqrt(sum(e * e for e in errs) / len(errs))


if __name__ == "__main__":
    print(f"Korenaga 2009 Table 2, Δη=1 블록 (n=1, θ_H={THETA_H_TABLE2:g}) — eq. 29 대조")
    print(f"{'θ':>7} {'Ra_i':>10} {'Nu 인쇄':>8} {'Nu eq29':>8} {'오차 %':>8} {'θ_H/θ':>8}")
    for theta, nu_p, pred, err in table2_residuals():
        print(f"{theta:7.2f} {dict((t, r) for t, r, _ in TABLE2_DETA1)[theta]:10.3g} "
              f"{nu_p:8.2f} {pred:8.3f} {err:+8.2f} {THETA_H_TABLE2 / theta:8.3f}")
    print(f"\nrms {table2_rms():.2f} %  — 논문이 **Table 1** 에 대해 적은 적합 rms 는 ~1.2 %")
    print(f"eq. 44  Ra_crit: n=1 {ra_crit(1):.0f} (본문 ~450) · n=2 {ra_crit(2):.0f} (~134, ⚠ 7 % 차) "
          f"· n=3 {ra_crit(3):.0f} (~104)")


# ── C47 (g), brief 148 단계 3 — eq. 42·43 의 국소 안정해석과 용융 보정 ──────────
#: ⚠ **여기부터는 n = 1 전용이다.** eq. 46 의 `η* = (τ*)^{1−n} Z(z*) exp(−θT*)` 에서 응력항
#: `(τ*)^{1−n}` 이 n=1 에서만 정확히 1 이고, 아래 유도는 그 항을 빼고 있다. 확인: 이 유도가
#: 내는 계수가 n=1 에서 논문 적합 `a = 0.55` 를 0.7 % 로 재현하는데(0.5539), n=2·3 에서는
#: 0.274·0.187 대 0.80·1.05 로 안 맞는다. 논문 자신도 §4.1 을 n=1 로 하고 Table 2 도 n=1 이다.
#: ⚠ **그 `0.55` 는 Korenaga 자신의 재적합** `a ≈ 0.30 + 0.25n` 의 n=1 값이다 (rms ~1.2 % — 우리
#: 0.7 % 는 논문 적합오차 **안**이다). 같은 양의 다른 수 넷: S&M 2000 Table 5 한 매개 적합
#: **0.528 ± 0.002**, Korenaga 가 요약한 S&M `0.31 + 0.22n` = **0.53**, 그의 Fig. 6 부분집합 적합
#: **0.57**, Foley 2018 인쇄 `c₁` **0.5**. 흩어짐의 원인은 논문이 적어 두었다 — *"my definition of
#: T̄_i (eq. 20) results in slightly different values of Nu, Ra_i and a_rh"*. 그래서 **논문 세트를
#: 섞지 말 것**(C51 첫 앵커, 3.65× 절대 플럭스 차의 유일한 후보 설명).
#:
#: 기하(eq. 42 · Fig. 5): 경계층은 위쪽에 있고 `z*` 는 위로 증가한다(Table 2 각주의 `z* > 0.75`
#: 가 굳은 탈수층이라는 것이 그 방향을 정한다). 부층은 **경계층 밑에서 위로** 재고, `η*` 는
#: `η(T_i)` 기준이라(`Ra_i` 가 이미 `exp[E/(nRT_i)]` 를 품는다) `⟨1−T*⟩ = u/2` 에서
#: `η*_eff = exp(θu/2)`. 그러면 최대가 `u* = 4(n+1)/(nθ)` 에 내부점으로 서고, δ 를 소거하면
#: `Nu ∝ θ^{−(2n+2)/(n+2)} Ra_i^β` — 그리고 `(2n+2)/(n+2) = 1+β` 가 정확히 성립해 eq. 30 의
#: 꼴이 된다. 즉 논문의 *"the boundary-layer stability approach reproduces exactly the
#: asymptotic heat-flow scaling"* 가 검증된다.
Z_D_TABLE2 = 0.75              # Table 2·3 각주: *"Viscosity contrast for z* > 0.75"*
#: eq. 50 — `(dρ/dF) ≈ −1.2 kg m⁻³ per cent` (Korenaga 2006). ⚠ 단위가 **퍼센트당**이다.
D_RHO_D_F = -1.2
#: §5: *"Melt productivity (dF/dP)_S is assumed to be 15 per cent/GPa (Korenaga 2006), and for
#: simplicity, the final pressure of melting P_f is set to zero."*
D_F_D_P_PERCENT_PER_GPA = 15.0
P_F_GPA = 0.0
#: §4: *"To calculate melting-related parameters such as P₀ and Δρ, ρ₀ of 3300 kg m⁻³ is used."*
RHO_0_MELT = 3300.0
#: ⚠ **논문이 자기 α 를 반증한다 — 결함 #24.** §4 의 상수 목록은 `α = 2 × 10⁻³ K⁻¹` 를 인쇄하지만
#: §3.2 는 자기 워크드 예제로 *"The factor αΔT is ∼0.05, so Δρ of 0.99 corresponds to ΔT*_ρ of
#: ∼0.2"* 라 적는다. 논문 자신의 `ΔT = 1350 K` 에서 §4 값은 `αΔT = 2.7`·`ΔT*_ρ = 0.0037` 로
#: **두 수 다 못 맞히고**, `3.7 × 10⁻⁵` 는 `0.0499`·`0.2002` 로 **둘 다 0.2 % 안에서 맞힌다.**
#: 그래서 §3.2 쪽을 쓰되 ⚠ **두 값을 다 들고 다니고 결과를 양쪽으로 보고한다**(C47 (g) 사전등록).
ALPHA_SECTION_3_2 = 3.7e-5     # §3.2 의 워크드 예제가 못 박는 값
ALPHA_SECTION_4_PRINTED = 2.0e-3   # §4 가 인쇄한 값 — 자기 §3.2 를 재현하지 못한다
DELTA_T_PAPER_K = 1350.0       # §4 의 지구 조건


def solidus_p0_gpa(t_p_celsius: float) -> float:
    """eq. 45 — `P₀ = (T_p − 1150)/100` [GPa], Takahashi & Kushiro 1983 의 건조 솔리더스.

    ⚠ 우리 `eos.silicate_solidus` 로 갈아끼우지 않는다: 그것은 다른 출처(Andrault+ 2011)의
    **역함수**(압력의 함수인 융해 온도)이고, 섞으면 논문 자신의 고갈층 깊이가 움직인다."""
    return max(0.0, (t_p_celsius - 1150.0) / 100.0)


def mean_melt_fraction_percent(t_p_celsius: float) -> float:
    """eq. 51 — `F̄ = 0.5 (P₀ − P_f) (dF/dP)_S` [퍼센트]."""
    return 0.5 * (solidus_p0_gpa(t_p_celsius) - P_F_GPA) * D_F_D_P_PERCENT_PER_GPA


def delta_rho(t_p_celsius: float) -> float:
    """eq. 53 — `Δρ = 1 + (F̄/ρ₀)(dρ/dF)`.

    ⚠ **Fig. 11 을 읽지 않는다.** §4 가 *"compositional buoyancy is calculated based on Fig. 11"*
    이라 적지만, eq. 51 과 §5 의 인쇄 상수로 전부 계산되므로 그 그림은 결과의 그림일 뿐이다."""
    return 1.0 + mean_melt_fraction_percent(t_p_celsius) * D_RHO_D_F / RHO_0_MELT


def delta_t_rho(t_p_celsius: float, alpha: float = ALPHA_SECTION_3_2,
                delta_t_k: float = DELTA_T_PAPER_K) -> float:
    """eq. 54 의 등가 온도차 `ΔT*_ρ ≈ (1 − Δρ)/(αΔT)`.

    논문 자기 예제로 대조: `Δρ = 0.99`, `αΔT ≈ 0.05` → `ΔT*_ρ ≈ 0.2`."""
    return (1.0 - delta_rho(t_p_celsius)) / (alpha * delta_t_k)


def _ra_local_max(delta: float, theta: float, d_eta: float, z_d: float,
                  dt_rho: float, samples: int = 4000) -> float:
    """eq. 42 의 `max[ δ_eff^{(n+2)/n} ΔT*_eff / η*_eff ]`, n = 1.

    `Δη` 는 eq. 46·47 의 계단으로 `η*_eff` 에 로그평균으로 들어가고, `ΔT*_ρ` 는 §3.2 끝문장대로
    `ΔT*_eff` 에서 빠진다 — *"This can be done if ΔT*_ρ is incorporated when calculating
    ΔT*_eff in eq. (42)."* 둘 다 **부층 중 `z*_D` 위쪽 몫에만** 걸린다."""
    best = 0.0
    for i in range(1, samples + 1):
        u = i / samples
        d_eff = u * delta
        top = 1.0 - delta + d_eff
        above = max(0.0, min(top, 1.0) - max(1.0 - delta, z_d))
        frac = above / d_eff if d_eff > 0.0 else 0.0
        eta_eff = d_eta ** frac * math.exp(theta * u / 2.0)
        dt_eff = u - frac * dt_rho
        if dt_eff <= 0.0:
            continue
        v = d_eff ** 3.0 * dt_eff / eta_eff
        if v > best:
            best = v
    return best


def nu_stability(theta: float, ra_i: float, d_eta: float = 1.0, z_d: float = Z_D_TABLE2,
                 dt_rho: float = 0.0) -> float:
    """eq. 43 — `Ra_l(δ) = Ra_crit(n)` 를 δ 로 풀고 `Nu = δ⁻¹`. n = 1 전용."""
    target = ra_crit(1)
    lo, hi = 1e-6, 0.999
    # ⚠ **기준 가지가 없는 이분법** — 상태 `None`, 묻는 것은 진입 괄호뿐이다
    #   (브리프 189 Amendment 2).
    convergence.note("stagnant_lid.ra_local_bisect", None,
                     bracket_valid=convergence.bracket_valid(
                         ra_i * _ra_local_max(lo, theta, d_eta, z_d, dt_rho) - target,
                         ra_i * _ra_local_max(hi, theta, d_eta, z_d, dt_rho) - target))
    for _ in range(90):
        mid = 0.5 * (lo + hi)
        if ra_i * _ra_local_max(mid, theta, d_eta, z_d, dt_rho) < target:
            lo = mid
        else:
            hi = mid
    return 1.0 / (0.5 * (lo + hi))


def nu_full(theta: float, ra_i: float, d_eta: float = 1.0, z_d: float = Z_D_TABLE2,
            dt_rho: float = 0.0, a_rh: float | None = None) -> float:
    """안정해석(eq. 43)에 eq. 29 의 사전점근 브래킷을 얹은 `Nu`.

    ⚠ 안정해석은 **점근형**을 낸다(eq. 30 과 행마다 1.0071 배로 일치). Table 2 의 `Nu` 3–7 은
    점근이 아니므로, eq. 43 의 결과를 eq. 29 의 우변으로 받아 `Nu` 를 다시 푼다. `Δη = 1` 에서
    이것이 정확히 eq. 29 가 되고, `Δη ≠ 1` 로의 확장은 **우리 것**이라 여기 적어 둔다."""
    rhs = nu_stability(theta, ra_i, d_eta, z_d, dt_rho)
    if a_rh is None:
        a_rh = A_RH_LINEAR_EXP[1]
    c = 2.0 * (1.0 - a_rh / theta)
    lo, hi = max(c, 0.0) + 1e-9, 1.0e4
    # ⚠ **기준 가지가 없는 이분법** — 상태 `None`, 묻는 것은 진입 괄호뿐이다
    #   (브리프 189 Amendment 2).
    convergence.note("stagnant_lid.nu_table2_bisect", None,
                     bracket_valid=convergence.bracket_valid(
                         lo * max(1.0 - c / lo, 0.0) ** 0.5 - rhs,
                         hi * max(1.0 - c / hi, 0.0) ** 0.5 - rhs))
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid * max(1.0 - c / mid, 0.0) ** 0.5 < rhs:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


#: Table 2 의 `Δη = 3` · `Δη = 10` 블록. ⚠ **이 20행은 `a`·`a_rh` 적합에 쓰이지 않았다** —
#: 논문의 적합은 Table 1 에 대한 것이므로, 이 행들은 탈수경화 기제에 대한 **독립 앵커**다.
TABLE2_DETA3 = (
    (16.16, 3.38e6, 3.09), (15.29, 3.99e6, 3.27), (14.36, 4.97e6, 3.48),
    (13.60, 6.61e6, 3.68), (12.85, 9.75e6, 3.89), (12.10, 1.31e7, 4.13),
    (10.98, 1.28e7, 4.56), (10.03, 1.37e7, 4.98), (8.95, 1.39e7, 5.58),
    (7.96, 1.37e7, 6.28),
)
TABLE2_DETA10 = (
    (16.14, 3.31e6, 3.10), (15.31, 4.11e6, 3.26), (14.44, 5.38e6, 3.46),
    (13.74, 7.65e6, 3.64), (13.10, 1.28e7, 3.82), (12.59, 2.21e7, 3.97),
    (12.05, 4.12e7, 4.15), (11.12, 4.52e7, 4.50), (10.06, 4.69e7, 4.97),
    (8.99, 4.34e7, 5.56),
)
TABLE2_BLOCKS = {1.0: TABLE2_DETA1, 3.0: TABLE2_DETA3, 10.0: TABLE2_DETA10}


def table2_block_rms(d_eta: float) -> tuple[float, float, float]:
    """한 블록의 (rms %, 편향 %p, 최악 %) — `nu_full` 대 인쇄 `Nu`."""
    errs = [(nu_full(t, r, d_eta) / n - 1.0) * 100.0 for t, r, n in TABLE2_BLOCKS[d_eta]]
    return (math.sqrt(sum(e * e for e in errs) / len(errs)),
            sum(errs) / len(errs), max(abs(e) for e in errs))


# ── C47 (k), brief 162 커밋 1 — 4단계 차원화. 09-07 인라인 러너를 고치지 않고 승격 ──────────
#
# ⚠ **이 절의 산수는 09-07 작업석의 두 번째 인라인 블록(16:39:56)과 한 글자도 다르지 않다.**
# 그 블록은 커밋된 적이 없고 트랜스크립트에서 복구됐다(C47 (j)). 알려진 결함 셋(b 를 eq. 30 으로
# 적합하고 실행은 eq. 29 로 함 · `Ra_i` 안의 α 하드코딩 · eq. 56 고정점 없음)은 **여기서 고치지
# 않는다** — 커밋 2·3·4 가 하나씩 고치고 각 변화를 따로 보고한다. 먼저 재현 앵커를 박는 것이 목적.

#: §4 의 상수 목록에서. ⚠ `ALPHA_IN_RA` 는 §4 가 인쇄한 `2 × 10⁻³` 이고, 이 값이 `Ra_i` 에
#: 들어간다 — 그런데 부력항의 α 는 C47 (g) 가 양쪽으로 보고하도록 등록한 값이다. 즉 한 실행이
#: 논문의 자기모순을 **양쪽으로 동시에** 채택한다. 커밋 3 이 이것만 고친다.
K_THERMAL_W_MK = 4.0            # 열전도도
KAPPA_M2_S = 1.0e-6             # 열확산율
RHO_MANTLE_KG_M3 = 4000.0       # 맨틀 밀도 (Ra_i 용; 용융 파라미터의 ρ₀ = 3300 과 다른 값이다)
E_ACTIVATION_J_MOL = 300.0e3    # 활성화 에너지
R_GAS_J_MOL_K = 8.314
ALPHA_IN_RA = 2.0e-3            # §4 인쇄값 — Ra_i 안에서만 쓰인다 (위 주석)

#: 두 대조 천체. ⚠ 여기 `D` 는 맨틀 두께이고 `cmf` 는 핵질량비다 — `radiogenic.budget` 이
#: 맨틀 질량을 받으므로 둘이 함께 필요하다. 값은 09-07 러너가 쓴 것 그대로.
STEP4_BODIES = {
    "Earth": {"g": 9.8, "D": 2900e3, "r_p": 6.371e6, "mass": 5.972e24, "cmf": 0.325},
    "Mars": {"g": 3.7, "D": 1800e3, "r_p": 3.3895e6, "mass": 6.417e23, "cmf": 0.24},
}

#: ⚠ **기록된 값이고 계산에 쓰지 않는다.** 09-07 실행이 인쇄한 `b` 는 유효숫자 넷(`4.1921e+10`)
#: 이라, 이 숫자를 그대로 쓰면 그 실행을 비트로 재현할 수 없다. `fit_b_eq30()` 이 같은 적합을
#: 다시 풀고, 러너가 그 값을 쓴다. 아래 상수는 대조용이다.
B_GRAIN_RECORDED = 4.1921e10

#: 표면온도. ⚠ **브리프 162 커밋 2 (결함 ④) — 하나로 통일했다.** 09-07 러너는 한 실행 안에서
#: `T_i = T_p + 273.15` 와 `ΔT = T_i − 273.0` 을 섞어 써서 `T_p = 1350 °C` 에서 `ΔT = 1350.15 K`
#: 였고, `b` 적합 줄은 리터럴 `1350.0`·`1623.0` 이었다 — 적합 조건과 실행 조건이 **0.15 K** 달랐다.
#: 적합의 부동점은 적합 조건에서만 정확하므로, 이 통일이 `b` 재적합(커밋 3)보다 **먼저** 와야 한다.
T_S_K = 273.15

#: b 적합이 쓰는 지구 조건 — 논문 자신의 `ΔT = 1350 K`, 그리고 같은 `T_s` 로 만든 `T_i`.
B_FIT_EARTH_DT_K = 1350.0
B_FIT_EARTH_TI_K = B_FIT_EARTH_DT_K + T_S_K
B_FIT_EARTH_Q_W_M2 = 0.050      # §4 의 인쇄된 지구 조건 50 mW/m²


def theta_fk(delta_t_k: float, t_i_k: float) -> float:
    """Frank-Kamenetskii 파라미터 `θ = E ΔT / (R T_i²)`.

    ⚠ 09-07 의 **첫** 인라인 블록은 `E ΔT / (R T_i)` 를 썼고 `OverflowError` 로 죽었다(C47 (k)).
    실행된 것은 이 정의다."""
    return E_ACTIVATION_J_MOL * delta_t_k / (R_GAS_J_MOL_K * t_i_k ** 2)


def ra_internal(g: float, d_m: float, delta_t_k: float, t_i_k: float, b_grain: float,
                alpha: float = ALPHA_IN_RA) -> float:
    """내부 가열 Rayleigh 수 `Ra_i = α ρ g ΔT D³ / (b κ exp[E/(R T_i)])`, n = 1.

    ⚠ **브리프 162 커밋 4 (결함 ②) — α 를 인수로 받는다.** 09-07 러너는 여기에 §4 의 `2 × 10⁻³` 을
    박아 두고 부력항에서만 α 를 쓸었다. 이제 스윕하는 α 가 양쪽에 같이 들어간다. ⚠ **그리고 그
    결과는 "아무 일도 일어나지 않는다" 이고, 그것이 발견이다**: `Ra_i ∝ α/b` 이고 `b` 는 지구
    조건에 적합되므로 α 는 `b` 에 그대로 흡수된다 — α 를 54배 줄이면 `b` 도 정확히 같은 비로
    줄고 `Ra_i` 는 소수 전부까지 같다. **논문의 α 자기모순은 `Ra_i` 를 통해서는 작용할 수 없고,
    `ΔT*_ρ` 를 통해서만 작용한다** (C47 (k) 커밋 4)."""
    return (alpha * RHO_MANTLE_KG_M3 * g * delta_t_k * d_m ** 3
            / (b_grain * KAPPA_M2_S * math.exp(E_ACTIVATION_J_MOL / (R_GAS_J_MOL_K * t_i_k))))


def z_d_from_solidus(g: float, d_m: float, t_p_celsius: float) -> tuple[float, float]:
    """`(z*_D, 고갈층 두께 [m])` — eq. 45 의 용융 개시 압력을 `ρ₀ g` 로 깊이로 바꾼 것.

    ⚠ eq. 56 의 고정점 `z*_D = Nu⁻¹` 이 아니다. 09-07 러너가 이렇게 잡았고 커밋 4 가 고친다."""
    depth = solidus_p0_gpa(t_p_celsius) * 1e9 / (RHO_0_MELT * g)
    return max(0.0, 1.0 - depth / d_m), depth


def flux_wm2(nu: float, delta_t_k: float, d_m: float) -> float:
    """`q = Nu k ΔT / D` [W/m²]."""
    return nu * K_THERMAL_W_MK * delta_t_k / d_m


def fit_b_eq30(alpha: float = ALPHA_IN_RA) -> float:
    """`b` — 논문 자기 지구 조건(q = 50 mW/m²)에 맞춘 **하나의 전역 선언**.

    ⚠ **eq. 30(`nu_asymptotic`)으로, 용융 없이 적합하는 것이 논문의 인쇄된 정의다** — §4:
    *"b … is determined so that the surface heat flux is 50 mW m⁻² at the present-day Earth condition
    … **without the effects of mantle melting (i.e. Δη = 1 and Δρ = 1)**"*, 그리고 Fig. 12 캡션의
    *"**conventional scaling** predicts surface heat flux of 50 mW m⁻²"* (본문이 conventional scaling
    을 eq. 30 이라 지칭한다). **그래서 이것은 결함이 아니다.** 이 `b` 로 eq. 30 을 평가하면 지구는
    구성상 정확히 50.0000 mW/m² 이고, 실행이 쓰는 eq. 29 + 안정해석에서는 51.99 로 +3.98 % 높다 —
    그 차는 두 식의 차이이고 적합의 잘못이 아니다 (C47 (k) 커밋 3). 09-07 의 이분법(기하평균,
    400회)을 그대로 옮긴 것이다."""
    lo, hi = 1e-40, 1e40
    # ⚠ **기준 가지가 없는 이분법** — 상태 `None`, 묻는 것은 진입 괄호뿐이다
    #   (브리프 189 Amendment 2).
    convergence.note("stagnant_lid.b_grain_bisect", None, bracket_checked=False)
    for _ in range(400):
        mid = math.sqrt(lo * hi)
        nu = nu_asymptotic(theta_fk(B_FIT_EARTH_DT_K, B_FIT_EARTH_TI_K),
                           ra_internal(STEP4_BODIES["Earth"]["g"], STEP4_BODIES["Earth"]["D"],
                                       B_FIT_EARTH_DT_K, B_FIT_EARTH_TI_K, mid, alpha), 1)
        if flux_wm2(nu, B_FIT_EARTH_DT_K, STEP4_BODIES["Earth"]["D"]) > B_FIT_EARTH_Q_W_M2:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


#: eq. 56 재귀의 수렴 기준과 상한. 논문 §3.1 은 *"until Nu converges. The convergence is usually
#: achieved within a few iterations."* 라 적는데, ⚠ **우리 경우는 "usually" 쪽이 아니다**: `Δη = 100`
#: 이 걸린 행에서 `Nu·z*_D − 1` 이 선형으로만 줄고 그 비가 **위로 표류**한다 — 초반 ≈0.66, 중반
#: ≈0.82, 후미 **≈0.847** (화성 1500 °C (a) 측정, 마지막 여섯 비 0.8465–0.8466). 후미 비로 1e-10
#: 까지 **~125 회**가 필요하고 실측은 117–129 회다. 상한 50 으로는 못 닿아서 400 으로 둔다 — 한
#: 반복은 `nu_full` 한 번이라 비용이 작다. 도달하면 실패로 보고한다 (C47 (k) 커밋 5).
EQ56_REL_TOL = 1.0e-10
EQ56_MAX_ITER = 400


def nu_eq56(theta: float, ra_i: float, d_eta: float, z_thickness: float,
            dt_rho: float = 0.0) -> dict:
    """eq. 56 의 재귀 — `Nu = F_Nu(n, θ, Ra_i, Δη, z*_D)` 를 `z*_D = Nu⁻¹` 로 갱신하며 푼다.

    논문 §3.1·§4: *"eq. (56) is solved iteratively by setting `z*_D = Nu⁻¹` when `Nu > 1/z*_D`, to have
    a self-consistent pair of the surface heat flux and the assumed viscosity and density structure"*,
    그 조건은 §3.1 이 *"when the dehydrated layer becomes dynamically unstable, that is, `Nu > 1/z*_D`"*
    라 적은 것이다.

    ⚠ **`z*_D` 를 여기서는 탈수층의 두께 `d/D` 로 읽는다** — `1 − z*_D`(우리 `nu_full` 의 인수)가
    아니다. 두께로 읽으면 조건이 "탈수층이 경계층보다 두꺼운가"가 되고 지구는 안 걸리고 화성
    1500 °C 만 걸린다. 다른 읽기(경계 좌표 0.9787 을 그대로 `z*_D` 로)에서는 `1/z*_D ≈ 1.02` 라
    **모든 경우가 항상 걸리고** 갱신이 맨틀 상부 90 % 를 굳은 층으로 만든다 — 물리적으로 불가능한
    결과라 그 읽기는 배제했다. 이 판독은 우리 것이고, 그래서 여기 적는다 (C47 (k) 커밋 5).

    반환: `nu` · `z_thickness`(최종) · `iters` · `fired`(갱신이 한 번이라도 걸렸는가) · `converged`."""
    z = z_thickness
    for i in range(EQ56_MAX_ITER):
        nu = nu_full(theta, ra_i, d_eta, 1.0 - z, dt_rho)
        if nu * z <= 1.0 + EQ56_REL_TOL:
            # ⚠ 이 자리는 C47 (k) 부터 `converged` 를 돌려주고 있었다 — 189 는 그 모양을
            #   나머지에 퍼뜨리고, 여기서는 기록에 한 줄 더 남길 뿐이다.
            convergence.note("stagnant_lid.eq56_fixed_point", True)
            return {"nu": nu, "z_thickness": z, "iters": i, "fired": z != z_thickness,
                    "converged": True}
        z = 1.0 / nu
    convergence.note("stagnant_lid.eq56_fixed_point", False)
    return {"nu": nu_full(theta, ra_i, d_eta, 1.0 - z, dt_rho), "z_thickness": z,
            "iters": EQ56_MAX_ITER, "fired": True, "converged": False}


def step4_run(body: str, t_p_celsius: float, alpha: float, d_eta: float, buoyancy: bool,
              b_grain: float) -> dict:
    """한 런 — `q` [W/m²] 와 그 안의 중간값들. 09-07 러너의 `run()` 과 같은 산수."""
    b = STEP4_BODIES[body]
    t_i = t_p_celsius + T_S_K
    delta_t = t_i - T_S_K            # = t_p_celsius. 커밋 2 이전에는 273.0 을 빼서 0.15 K 컸다
    z_d, depth = z_d_from_solidus(b["g"], b["D"], t_p_celsius)
    dt_rho = delta_t_rho(t_p_celsius, alpha, delta_t) if buoyancy else 0.0
    theta = theta_fk(delta_t, t_i)
    ra = ra_internal(b["g"], b["D"], delta_t, t_i, b_grain, alpha)
    sol = nu_eq56(theta, ra, d_eta, 1.0 - z_d, dt_rho)      # 커밋 5: eq. 56 의 고정점
    nu = sol["nu"]
    return {"q_w_m2": flux_wm2(nu, delta_t, b["D"]), "nu": nu, "theta": theta, "ra_i": ra,
            "z_d": 1.0 - sol["z_thickness"], "z_d_initial": z_d, "depleted_m": depth,
            "eq56_iters": sol["iters"], "eq56_fired": sol["fired"],
            "eq56_converged": sol["converged"], "dt_rho": dt_rho, "t_i_k": t_i,
            "delta_t_k": delta_t}
