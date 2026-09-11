# 전이 영역 대류 스케일링 — Foley & Bercovici 2014 (GJI) 식 (54)·(58)·(59)·(60) 과 Table 1 전사
"""Transitional-regime convection scaling — Foley & Bercovici 2014 (`2014GeoJI.199..580F`, held).

    python3 engine/test_transitional_lid.py

**Why this file exists.** C47 (e) named a two-regime law family, and C51's commit C transcribes the
one paper in that family that prints its constants. ⚠ **It is transcription only.** Every input this
law needs is non-dimensional and comes out of that paper's numerical models; **this engine supplies
none of them** (see `MISSING_INPUTS`), so nothing here is evaluated on a body. What it buys is that
the law's shape, its constants and its own stated caveats are in our records instead of in a summary.

**The chain, in the paper's numbering.** Grain-damage shear stress first — eq. (9)
`τ'_xz = 2C₁ Ra'^(2/3) A'_i^(−m/3)`, eq. (10) the steady-state grainsize balance
`D τ'²_xz A'_i = H A'_i^p`, eq. (11) `A'_i = (D τ'²_xz/H)^(1/(p−m))`, eq. (12) their combination — then
the two boundary layers and the closure:

    (54)  δ'_l = C₅ L'^βL μ'_l^βμ (D/(H h'_l))^βD (Ra' T'_i)^βRa
    (58)  δ'_m = C₆ μ'_i^(p/(3p−m)) (4D/(H h'_i))^(−m/(3p−m)) (Ra_c/(Ra'(1−T'_i)))^((p+m)/(3p−m))
    (59)  T'_i = δ'_l / (δ'_l + δ'_m)                    ← the energy balance that closes it
    (60)  Nu = (T'_i/C₅) L'^(−1/10) μ'_l^(−1/4) (D/(H h'_l))^(1/3) (Ra' T'_i)^(2/3)

⚠ **eq. (60) is (54) with the exponents rounded**, and the paper prints both sets: Table 1's fits for
(m, p) = (2, 4) are (β_L, β_μ, β_D, β_Ra) = (0.1071, 0.2484, −0.3151, −0.6603) while (60) uses
(1/10, 1/4, −1/3, −2/3). `nu_eq60` and `nu_from_table1` are both here so the gap is a number in our
records rather than a choice we made silently.

⚠ **Three things the paper says about itself, and they matter more than the constants.**
· **`L′` is an unknown by the paper's own decision:** *"we choose to exploit our numerical results and
  calculate L′ directly from the models. We therefore **treat the plate length, L′, as an unknown** in
  (54)."* Changing the domain aspect ratio from 4 × 1 to 16 × 1 moves `L′` from ≈1.5 to ≈4.
· **`β_L` changes sign across the three (m, p) rows** (+0.1071 · −0.0218 · +0.0582) and `C₅` spans
  **11 to 86**, so "how does plate length enter" has no single answer in the source.
· ⚠ **The paper's headline is that the regime is not a binary.** *"with grain-damage, the transition
  between stagnant lid convection and fully mobile convection is gradual and takes place over a large
  transitional regime, **with plate-tectonics lying within the transitional regime**"*, and Venus *"can
  be explained by convection in the transitional regime, close to the fully-stagnant lid regime, with a
  very slow «plate» speed"*. **Our bodies declare `stagnant_lid: true` or `false`** — a two-valued
  field this source says does not describe either Earth or Venus. Named, not repaired
  (`engine/interior-core.md@«it is four choices of the same declaration»`).
"""
from __future__ import annotations
import convergence

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

REFS = (
    "2014GeoJI.199..580F",             # Foley & Bercovici 2014 (GJI) — eqs 9–12, 54, 57–60, Table 1, Fig. 13 (held)
)

#: Table 1, *"Transitional Regime Scaling Law Constants for Various m and p"* — printed verbatim.
#: 열 순서: (m, p) → (C₅, β_Ra, β_D, β_μ, β_L).
TABLE1 = {
    (2, 4): {"c5": 20.0, "beta_ra": -0.6603, "beta_d": -0.3151, "beta_mu": 0.2484, "beta_l": 0.1071},
    (3, 4): {"c5": 86.0, "beta_ra": -0.8515, "beta_d": -0.4919, "beta_mu": 0.2598, "beta_l": -0.0218},
    (3, 5): {"c5": 11.0, "beta_ra": -0.6232, "beta_d": -0.4342, "beta_mu": 0.1931, "beta_l": 0.0582},
}
#: eq. (60) 이 쓰는 **반올림** 지수 — (2, 4) 행의 적합값과 나란히 두라고 여기 적는다.
EQ60_ROUNDED = {"beta_ra": -2.0 / 3.0, "beta_d": -1.0 / 3.0, "beta_mu": 1.0 / 4.0, "beta_l": 1.0 / 10.0}
#: Fig. 13 의 네 패널이 인쇄한 개별 적합 — 판정용이 아니라 기록이다.
FIG13_PANEL_FITS = {
    "ra": (574.5, -0.6603),            # A: 574.5 (Ra' T'_i)^(−0.6603)
    "damage": (0.041, -0.3151),        # B: 0.041 (D/(H h'_l))^(−0.3151)
    "viscosity": (0.0022, 0.2484),     # C: 0.0022 μ'_l^(0.2484)
    "plate_length": (0.036, 0.1071),   # D: 0.036 L'^(0.1071)
}
C6 = 0.07                              # eq. (58) 아래: *"this gives C6 ≈ 0.07"* — (16) 과의 극한 일치로 정한 값
RA_CRIT = 700.0                        # 본문: *"the critical Rayleigh number … (Rac ≈ 700)"*, free-slip
L_PRIME_RANGE = (1.5, 4.0)             # 본문: 종횡비 4×1 → 16×1 에서 L′ ≈ 1.5 → ≈4
E_H_J_MOL = 500.0e3                    # §8.1: *"we assume Eh = 500 kJ/mol"*
T_M0_EARTH_K = 1650.0                  # §8.1 eq. (68): *"Tm,0 = 1650 K is the Earth's mantle potential temperature"*
T_S0_EARTH_K = 273.0                   # 같은 식의 Ts,0

#: ⚠ 이 법칙이 요구하는 비차원 입력 전부 — 우리 엔진에 **하나도 값이 없다**.
MISSING_INPUTS = (
    "L' (plate length; the paper treats it as an unknown and reads it off its own models)",
    "mu'_l (lithosphere viscosity ratio)",
    "mu'_i (interior viscosity ratio)",
    "D/(H h'_l) (damage-to-healing in the lithosphere)",
    "D/(H h'_i) (damage-to-healing in the interior)",
    "Ra' (the paper's own Rayleigh normalisation, not Korenaga's and not Foley 2018's)",
    "(m, p) (the grain-damage pair; three printed combinations disagree in sign as well as magnitude)",
)
NO_INPUTS = ("cannot-say (the transitional law's inputs are non-dimensional quantities of Foley & "
             "Bercovici 2014's own models and this engine declares none of them: "
             + ", ".join(k.split(" (")[0] for k in MISSING_INPUTS) + ")")


def delta_l(l_prime: float, mu_l: float, damage_l: float, ra: float, t_i: float,
            m: int = 2, p: int = 4, constants: dict | None = None) -> float:
    """eq. (54) — `δ'_l = C₅ L'^βL μ'_l^βμ (D/(H h'_l))^βD (Ra' T'_i)^βRa`."""
    c = constants or TABLE1[(m, p)]
    return (c["c5"] * l_prime ** c["beta_l"] * mu_l ** c["beta_mu"]
            * damage_l ** c["beta_d"] * (ra * t_i) ** c["beta_ra"])


def delta_m(mu_i: float, damage_i: float, ra: float, t_i: float, m: int = 2, p: int = 4,
            ra_crit: float = RA_CRIT, c6: float = C6) -> float:
    """eq. (58) — the bottom boundary layer. `damage_i` is `D/(H h'_i)`; the 4 of `4D/(H h'_i)` is here."""
    q = 3.0 * p - m
    return (c6 * mu_i ** (p / q) * (4.0 * damage_i) ** (-m / q)
            * (ra_crit / (ra * (1.0 - t_i))) ** ((p + m) / q))


def close_t_i(l_prime: float, mu_l: float, mu_i: float, damage_l: float, damage_i: float, ra: float,
              m: int = 2, p: int = 4, tol: float = 1.0e-12, max_iter: int = 200) -> dict:
    """eq. (59) — `T'_i = δ'_l/(δ'_l + δ'_m)`, solved as a fixed point by bisection on (0, 1).

    The paper closes the problem this way: *"The heat flux out of the mantle through the top boundary
    layer must match the heat flux into the mantle through the bottom boundary layer, and thus
    T'_i/δ'_l = (1 − T'_i)/δ'_m."*"""
    def residual(t: float) -> float:
        dl = delta_l(l_prime, mu_l, damage_l, ra, t, m, p)
        dm = delta_m(mu_i, damage_i, ra, t, m, p)
        return dl / (dl + dm) - t

    lo, hi = 1.0e-9, 1.0 - 1.0e-9
    f_lo, f_hi = residual(lo), residual(hi)
    if f_lo * f_hi > 0.0:
        return {"refused": f"no bracket for eq. (59) on (0, 1): residual {f_lo:+.3e} … {f_hi:+.3e}"}
    for i in range(max_iter):
        mid = 0.5 * (lo + hi)
        f_mid = residual(mid)
        if abs(f_mid) < tol or hi - lo < tol:
            dl = delta_l(l_prime, mu_l, damage_l, ra, mid, m, p)
            dm = delta_m(mu_i, damage_i, ra, mid, m, p)
            convergence.note("transitional_lid.eq59_bisect", True)
            return {"t_i": mid, "delta_l": dl, "delta_m": dm, "nu": mid / dl, "iterations": i + 1}
        if f_lo * f_mid <= 0.0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    # ⚠ 이 자리는 **이미** 이름 대며 거절한다 (C71 의 보고자 다섯 중 하나). 세는 칸만 더한다.
    convergence.note("transitional_lid.eq59_bisect", False)
    return {"refused": f"eq. (59) did not converge in {max_iter} bisections"}


def nu_eq60(l_prime: float, mu_l: float, damage_l: float, ra: float, t_i: float,
            c5: float = TABLE1[(2, 4)]["c5"]) -> float:
    """eq. (60) as printed — the **rounded** exponents (−1/10, −1/4, 1/3, 2/3)."""
    return (t_i / c5) * l_prime ** (-1.0 / 10.0) * mu_l ** (-1.0 / 4.0) \
        * damage_l ** (1.0 / 3.0) * (ra * t_i) ** (2.0 / 3.0)


def nu_from_table1(l_prime: float, mu_l: float, damage_l: float, ra: float, t_i: float,
                   m: int = 2, p: int = 4) -> float:
    """`Nu = T'_i/δ'_l` with **Table 1's fitted** exponents — the same quantity (60) rounds."""
    return t_i / delta_l(l_prime, mu_l, damage_l, ra, t_i, m, p)


def rounded_vs_fitted(l_prime: float, mu_l: float, damage_l: float, ra: float, t_i: float) -> dict:
    """How much the paper's own rounding of its own exponents is worth, as a ratio."""
    a = nu_eq60(l_prime, mu_l, damage_l, ra, t_i)
    b = nu_from_table1(l_prime, mu_l, damage_l, ra, t_i)
    return {"eq60_rounded": a, "table1_fitted": b, "ratio": a / b}


def solve_on_body(*_args, **_kwargs) -> dict:
    """⚠ There is no body path. Refuses by name and lists what is missing."""
    return {"refused": NO_INPUTS, "missing": MISSING_INPUTS}
