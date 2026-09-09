# 정체뚜껑 맨틀 에너지 수지 — Foley 2018 식 (1)(2)(3)(4) 전사, 현재 에포크만 (C51 1단계)
"""Stagnant-lid mantle energy budget — Foley 2018 (`2018AsBio..18..873F`, held), eqs (1)–(4).

    python3 engine/test_mantle_budget.py

**Why this file exists.** The engine had a stagnant-lid *flux law* (`stagnant_lid.py`, Korenaga 2009
eq. 30) and no *budget* around it, so secular cooling was an input nobody supplied rather than an
output (C51). This transcribes the budget. ⚠ **Stage 1 is the present epoch only**: `dT_p/dt` is the
unknown, (1) is solved for it at a state that already exists, and secular cooling comes out as a
number rather than as a history. Coupling to C20's time axis is a separate brief.

**What is transcribed, in the paper's own numbering.**

    (1)  V_man ρ c_p dT_p/dt = Q_man − A_man F_man − f_m ρ_m (c_p ΔT_m + L_m)
    (2)  ρ c_p (T_p − T_l) dδ/dt = −F_man − k ∂T/∂z|_{z = R_p − δ}
    (3)  F_man = c₁ k (T_p − T_s)/d · θ^(−4/3) Ra_i^(1/3)
    (4)  T_l = T_p − a_rh R T_p² / E_v

with `V_man = (4/3)π((R_p − δ)³ − R_c³)`, `A_man = 4π(R_p − δ)²`, `θ = E_v(T_p − T_s)/(R T_p²)`,
`Ra_i = ρ g α (T_p − T_s) d³/(κ μ_i)` and `μ_i = μ_n exp(E_v/(R T_p))` — all printed under eq. (3).

⚠ **(3) is not new physics here.** At `n = 1` its exponents are exactly Korenaga eq. 30's `−1−β` and
`β`, so the shape is called from `stagnant_lid.nu_asymptotic(..., a=C1)` rather than retyped. **The
normalisation is not shared**: Foley's `θ` and `Ra_i` stand on a *potential* temperature `T_p`, while
Korenaga's stand on his eq. 20 `T̄_i` (the average below the boundary layer) and S&M 2000's on the
maximum horizontally averaged temperature. Three definitions, and mixing their constants is the trap
commit `c23e69b0` exists to prevent — see `engine/interior-core.md@«comparisons that crossed a definition boundary»`.

⚠ **The paper's own caveat on (3), carried as printed:** it uses `T_p − T_s` and `d` rather than
`T_p − T_l` and `d − δ`, because *"in the heat flux scaling law both the mantle thickness and
temperature difference cancel out, so the equation for the heat flux to the base of the lid is
independent of the definition of mantle thickness or temperature difference."* Transcribed as printed;
the claim is the paper's, not ours, and `f_man_lid_variables()` exists to measure it.

⚠ **Two inputs this engine cannot supply, refused by name rather than defaulted.**
· **the melt term** of (1) — there is no melt-production node. `secular_cooling()` reports the budget
  at `f_m` = 0 **and** the melt power that would move the answer by a declared fraction, so the size of
  the gap is printed instead of assumed (C51's pre-registration).
· **the lid-base conductive gradient** of (2) — that comes from the paper's eq. (5) lid diffusion
  problem, which needs `Q_crust`, `δ_c` and the crustal/mantle production split. `ddelta_dt()` takes it
  as an argument and **refuses by name** when it is absent. Not built here.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stagnant_lid as sl              # noqa: E402

REFS = (
    "2018AsBio..18..873F",             # Foley 2018 — eqs (1)–(5), Table 1 (held)
    "2009GeoJI.179..154K",             # Korenaga 2009 — eq. 30, the shape (3) shares at n = 1
    "2000JGR...10521795S",             # Solomatov & Moresi 2000 — eq. (9)/Table 5, the fit behind both
)

# ── Foley 2018 Table 1, printed values only ──────────────────────────────────
RHO_KG_M3 = 4000.0                     # mantle density
C_P_J_KG_K = 1250.0                    # heat capacity
RHO_MELT_KG_M3 = 2800.0                # melt density
L_M_J_KG = 600.0e3                     # latent heat of fusion
R_P_M = 6378.1e3                       # planet radius (Earth, this study's only size)
R_C_M = 3488.1e3                       # core radius
K_W_M_K = 5.0                          # ⚠ thermal conductivity — Korenaga's transcription uses 4.0
C1 = 0.5                               # *"We use c1 = 0.5 and arh = 2.5"*
D_MANTLE_M = 2890.0e3                  # whole mantle thickness, = R_p − R_c as printed
T_S_K = 273.0                          # surface temperature
A_RH = 2.5                             # constant for the rheological temperature scale
E_V_J_MOL = 300.0e3                    # activation energy (Karato & Wu 1993)
R_GAS_J_MOL_K = 8.314
G_M_S2 = 9.8
KAPPA_M2_S = 1.0e-6
ALPHA_1_K = 3.0e-5                     # ⚠ thermal expansivity — Korenaga's Ra normalisation differs
MU_N_PA_S = 4.0e10                     # viscosity pre-exponential factor
T_R_K = 1623.0                         # *"T_r = 1623 K is Earth's present day mantle temperature"*
MU_R_PRINTED_PA_S = 2.0e20             # *"Using our baseline value of μ_n = 4 × 10¹⁰ Pa s, μ_r ≈ 2 × 10²⁰"*
TAU_RAD_GYR = 2.94                     # *"A constant decay constant, τ_rad ≈ 2.94 Gyrs"*
Q0_RANGE_TW = (5.0, 250.0)             # *"Q0 is varied over a range of 5-250 TW"*
Q0_EARTH_ESTIMATE_TW = (70.0, 100.0)   # *"typical estimates for the Earth span ≈ 70 − 100 TW"*
DELTA_TYPICAL_M = 100.0e3              # *"a typical lid thickness of ∼ 100 km (see §4.1)"*

NO_LID_GRADIENT = ("cannot-say (the lid-base conductive gradient ∂T/∂z|_{R_p−δ} is not supplied — it is "
                   "the output of the paper's eq. (5) lid diffusion problem, which needs Q_crust, δ_c and "
                   "the crust/mantle production split; not built)")


def viscosity_pa_s(t_p_k: float, mu_n: float = MU_N_PA_S) -> float:
    """`μ_i = μ_n exp(E_v/(R T_p))` — printed under eq. (3)."""
    return mu_n * math.exp(E_V_J_MOL / (R_GAS_J_MOL_K * t_p_k))


def theta_fk(t_p_k: float, t_s_k: float = T_S_K) -> float:
    """`θ = E_v (T_p − T_s)/(R T_p²)` — the Frank-Kamenetskii parameter as (3) defines it."""
    return E_V_J_MOL * (t_p_k - t_s_k) / (R_GAS_J_MOL_K * t_p_k ** 2)


def ra_internal(t_p_k: float, t_s_k: float = T_S_K, d_m: float = D_MANTLE_M,
                g: float = G_M_S2) -> float:
    """`Ra_i = ρ g α (T_p − T_s) d³ / (κ μ_i)` — printed under eq. (3)."""
    return RHO_KG_M3 * g * ALPHA_1_K * (t_p_k - t_s_k) * d_m ** 3 / (KAPPA_M2_S * viscosity_pa_s(t_p_k))


def f_man_w_m2(t_p_k: float, t_s_k: float = T_S_K, d_m: float = D_MANTLE_M, g: float = G_M_S2,
               c1: float = C1, k: float = K_W_M_K) -> float:
    """eq. (3) — `F_man = c₁ k (T_p − T_s)/d · θ^(−4/3) Ra_i^(1/3)`.

    The `θ` and `Ra_i` powers are `stagnant_lid`'s eq. 30 at n = 1; the shape is called, not retyped."""
    nu = sl.nu_asymptotic(theta_fk(t_p_k, t_s_k), ra_internal(t_p_k, t_s_k, d_m, g), n=1, a=c1)
    return nu * k * (t_p_k - t_s_k) / d_m


def t_lid_base_k(t_p_k: float, a_rh: float = A_RH) -> float:
    """eq. (4) — `T_l = T_p − a_rh R T_p² / E_v`."""
    return t_p_k - a_rh * R_GAS_J_MOL_K * t_p_k ** 2 / E_V_J_MOL


def volumes(delta_m: float, r_p_m: float = R_P_M, r_c_m: float = R_C_M) -> dict:
    """`V_man`, `A_man` and the sub-crustal lid volume `V_lid`, all printed below (1) and under (5)."""
    r_top = r_p_m - delta_m
    return {"v_man_m3": (4.0 / 3.0) * math.pi * (r_top ** 3 - r_c_m ** 3),
            "a_man_m2": 4.0 * math.pi * r_top ** 2,
            "v_lid_m3": (4.0 / 3.0) * math.pi * (r_p_m ** 3 - r_top ** 3)}


def melt_power_w(f_m_m3_s: float, delta_t_m_k: float) -> float:
    """(1)'s last term — `f_m ρ_m (c_p ΔT_m + L_m)` [W]. ⚠ `ΔT_m` has no value in this engine."""
    return f_m_m3_s * RHO_MELT_KG_M3 * (C_P_J_KG_K * delta_t_m_k + L_M_J_KG)


def dtp_dt_k_s(t_p_k: float, delta_m: float, q_man_w: float, melt_w: float = 0.0,
               **flux_kw) -> dict:
    """eq. (1), solved for the unknown `dT_p/dt` at the present state.

    `V_man ρ c_p dT_p/dt = Q_man − A_man F_man − (melt term)`, so `dT_p/dt` is what falls out. A
    negative value is secular cooling — which is the quantity C51 exists to produce."""
    v = volumes(delta_m)
    f = f_man_w_m2(t_p_k, **flux_kw)
    surface_w = v["a_man_m2"] * f
    capacity_j_k = v["v_man_m3"] * RHO_KG_M3 * C_P_J_KG_K
    dtp = (q_man_w - surface_w - melt_w) / capacity_j_k
    return {"dtp_dt_k_s": dtp, "dtp_dt_k_gyr": dtp * 3.156e16,
            "f_man_w_m2": f, "q_surface_w": surface_w, "q_man_w": q_man_w,
            "melt_w": melt_w, "capacity_j_k": capacity_j_k,
            "urey": q_man_w / surface_w if surface_w > 0.0 else None,
            "t_lid_base_k": t_lid_base_k(t_p_k), "theta": theta_fk(t_p_k),
            "ra_i": ra_internal(t_p_k), "mu_i_pa_s": viscosity_pa_s(t_p_k)}


def ddelta_dt_m_s(t_p_k: float, f_man: float, lid_gradient_k_m: float | None) -> dict:
    """eq. (2) — `ρ c_p (T_p − T_l) dδ/dt = −F_man − k ∂T/∂z|_{R_p−δ}`, solved for `dδ/dt`.

    ⚠ Refuses by name when the gradient is absent; it is eq. (5)'s output and eq. (5) is not built."""
    if lid_gradient_k_m is None:
        return {"refused": NO_LID_GRADIENT}
    denom = RHO_KG_M3 * C_P_J_KG_K * (t_p_k - t_lid_base_k(t_p_k))
    return {"ddelta_dt_m_s": (-f_man - K_W_M_K * lid_gradient_k_m) / denom, "denominator_j_m3_k": denom}


def f_man_lid_variables(t_p_k: float, delta_m: float, **flux_kw) -> dict:
    """The paper's cancel-out claim, measured rather than believed.

    (3) is printed on `(T_p − T_s, d)`; the paper says using `(T_p − T_l, d − δ)` gives the same flux.
    This evaluates both and returns the ratio, so the claim is a number in our records."""
    printed = f_man_w_m2(t_p_k, **flux_kw)
    alt = f_man_w_m2(t_p_k, t_s_k=t_lid_base_k(t_p_k), d_m=D_MANTLE_M - delta_m, **flux_kw)
    return {"printed_w_m2": printed, "lid_variables_w_m2": alt, "ratio": alt / printed}


def secular_cooling(t_p_k: float, delta_m: float, q_man_w: float, probe_fraction: float = 0.10,
                    **flux_kw) -> dict:
    """The stage-1 answer, with the melt gap printed instead of assumed (C51's pre-registration).

    Returns the `f_m` = 0 budget, plus the **melt power** that would change `dT_p/dt` by
    `probe_fraction`. The power is reported rather than `f_m` itself because `ΔT_m` has no value
    here — converting one to the other would be inventing a temperature."""
    zero = dtp_dt_k_s(t_p_k, delta_m, q_man_w, melt_w=0.0, **flux_kw)
    probe_w = abs(probe_fraction * zero["dtp_dt_k_s"]) * zero["capacity_j_k"]
    shifted = dtp_dt_k_s(t_p_k, delta_m, q_man_w, melt_w=probe_w, **flux_kw)
    return {"at_zero_melt": zero, "probe_melt_w": probe_w, "at_probe_melt": shifted,
            "probe_fraction": probe_fraction,
            "probe_melt_as_fraction_of_surface": probe_w / zero["q_surface_w"]}
