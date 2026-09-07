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


def nu_asymptotic(theta: float, ra_i: float, n: int = 1) -> float:
    """eq. 30 — `Nu ≈ a θ^(−1−β) Ra_i^β`. **Nu ≫ 1 에서만** eq. 29 의 극한이다."""
    b = beta(n)
    return a_of_n(n) * theta ** (-1.0 - b) * ra_i ** b


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
