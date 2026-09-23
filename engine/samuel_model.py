# Samuel 방식 층 없는 열진화의 우변 조각 — 판 2 첫 판: 인쇄식만, 결정이 안 난 셋은 이름 대고 거절
"""The no-layer Samuel model's right-hand side, in pieces — plate 2, first cut.

Pre-registration `prereg-thermal-v2.md` (blob `26c605c9`) §2–§5; brief `BRIEF-thermal-plate2.md` (blob
`c18bbe3c`). Inputs come from `samuel_thermal` only; this module holds no number of its own except the
coefficients printed inside an equation.

Every equation is cited with its **year**, because the two papers number differently and overlap
(2019 SI eq. (21) is the lid conduction equation; 2021 eq. (21) is the layer diffusion equation):

* **2019 SI** — Samuel, Lognonné, Panning & Lainey 2019, Nature 569, 523, Supplementary Information
  (`2019Natur.569..523S-si.pdf`). Page numbers are PDF pages, read off a 110 dpi render.
* **2021** — Samuel, Ballmer, Padovan, Tosi, Rivoldini & Plesa 2021, JGR Planets 126, e2020JE006613
  (`2021JGRE..12606613S.pdf`), §4.1, PDF pp. 11–12, read off a render.

Where the two print the same relation differently, the 2021 form is used, because the pre-registration
takes the energy balance from 2021: 2021 writes `ΔT = T_m − T_l + max(T_c − T_b, 0)` and
`ΔT_i = T_m − T_s + max(T_c − T_b, 0)`, where 2019 SI eqs (9) and (12) have no `max`.

The temperature gradient at the base of the lid (2019 SI eq. (21)) is `samuel_lid`'s — a grid, by owner
decision (pre-registration v2-3), with a quasi-steady comparison beside it.

⚠ **Not built here, and refused by name when asked** (none of them gets a stand-in value):

* the heat production `H_m`, `H_cr` — the crustal-enrichment definition and the decay data are being
  sourced (2019 SI eqs (22)–(23) use a different `Λ` from the pre-registration's);
* the melt fraction, the solidus and the Stefan number — two printed parameterizations disagree
  (2019 SI eqs (14)–(15), (19) against 2021 eqs (8)–(9)), and `ΔT_sol` is not printed.

Gravity and pressure are arguments with no default: neither the fixed set nor the pre-registration names
a value, and the bottom heat flow must print which gravity it used (acceptance G).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import samuel_thermal as st  # noqa: E402


class Refused(Exception):
    """A quantity this plate does not build yet. The message names it and says why."""


# ── Viscosity — 2019 SI eq. (1), PDF p1 ────────────────────────────────────────────────────────
def viscosity(t_k: float, p_pa: float, eta0: float, e_star: float, v_star: float,
              t_ref: float, p_ref: float, r_gas: float) -> float:
    """η(T, P) = η₀ exp[(E* + P V*)/(R T) − (E* + P_ref V*)/(R T_ref)]. No melt weakening (refused, see
    the module docstring)."""
    return eta0 * math.exp((e_star + p_pa * v_star) / (r_gas * t_k)
                           - (e_star + p_ref * v_star) / (r_gas * t_ref))


# ── The lid's base — 2019 SI eq. (4), PDF p2 (also 2021 PDF p11) ───────────────────────────────
def lid_base_temperature(t_m: float, e_star: float, a_rh: float, r_gas: float) -> float:
    """T_l = T_m − a_rh R T_m² / E*."""
    return t_m - a_rh * r_gas * t_m * t_m / e_star


# ── The adiabat to the bottom of the convecting mantle — 2021 eq. (14), PDF p12 ────────────────
def convecting_thickness(r_p: float, d_l: float, r_c: float, delta_u: float, delta_b: float) -> float:
    """ΔR = R_p − D_l − R_c − δ_u − δ_c (2021 eq. (14)'s definition)."""
    return r_p - d_l - r_c - delta_u - delta_b


def mantle_base_temperature(t_m: float, alpha: float, g: float, c_pm: float, d_r: float) -> float:
    """T_b = T_m + (α g T_m / C_pm) ΔR."""
    return t_m + alpha * g * t_m / c_pm * d_r


# ── Upper boundary layer — 2021 eqs (15)–(16) and (12), PDF pp. 11–12 ──────────────────────────
def upper_layer(t_m: float, t_l: float, t_c: float, t_b: float, eta_m: float, *, rho_m: float,
                alpha: float, g: float, k_m: float, c_pm: float, r_p: float, d_l: float, r_c: float,
                ra_c: float, beta_u: float) -> dict:
    """Ra (2021 eq. (16)), δ_u (eq. (15)), q_m (eq. (12)).

    ⚠ **`Ra < Ra_c` sets `q_m` and `δ_u` to 0** — printed in 2019 SI PDF p4, and v2-2 ②. The branch
    taken is returned, so a run can print it."""
    kappa = k_m / (rho_m * c_pm)
    d_t = t_m - t_l + max(t_c - t_b, 0.0)
    ra = rho_m * alpha * g * d_t * (r_p - d_l - r_c) ** 3 / (eta_m * kappa)
    if ra < ra_c:
        return {"ra": ra, "delta_u": 0.0, "q_m": 0.0, "subcritical": True}
    r_l = r_p - d_l
    delta_u = (r_l - r_c) * (ra_c / ra) ** beta_u
    return {"ra": ra, "delta_u": delta_u, "q_m": k_m * (t_m - t_l) / delta_u, "subcritical": False}


# ── Lower boundary layer — 2021 eq. (17) and (13), PDF pp. 11–12 ───────────────────────────────
def lower_layer(t_m: float, t_c: float, t_b: float, eta_m: float, eta_c: float, *, rho_m: float,
                alpha: float, g: float, k_m: float, c_pm: float, r_p: float, r_c: float,
                t_s: float) -> dict:
    """Ra_i, Ra_δb = 0.28 Ra_i^0.21, δ_b = (κ η_c Ra_δb / (ρ_m α g |T_c − T_b|))^(1/3), q_c = k_m (T_c − T_b)/δ_b.

    `η_c = η((T_b + T_c)/2, P_c)` is the caller's to evaluate — the pressure is an argument there."""
    kappa = k_m / (rho_m * c_pm)
    d_t_i = t_m - t_s + max(t_c - t_b, 0.0)
    ra_i = rho_m * alpha * g * d_t_i * (r_p - r_c) ** 3 / (eta_m * kappa)
    ra_db = st.RA_DELTA_B_COEFF * ra_i ** st.RA_DELTA_B_EXP
    delta_b = (kappa * eta_c * ra_db / (rho_m * alpha * g * abs(t_c - t_b))) ** (1.0 / 3.0)
    return {"ra_i": ra_i, "ra_delta_b": ra_db, "delta_b": delta_b, "q_c": k_m * (t_c - t_b) / delta_b}


# ── Crust growth — 2019 SI eqs (16)–(18), PDF p5 ───────────────────────────────────────────────
def crust_reference_thickness(r_p: float, r_c: float) -> float:
    """D_ref = (0.2/3)(R_p³ − R_c³)/R_p²."""
    return 0.2 / 3.0 * (r_p ** 3 - r_c ** 3) / r_p ** 2


def convective_velocity(ra: float, ra_c: float, u0: float) -> float:
    """u = u₀ (Ra/Ra_c)^(2/3)."""
    return u0 * (ra / ra_c) ** (2.0 / 3.0)


def crust_growth_rate(u: float, m_a: float, v_a: float, r_p: float) -> float:
    """dD_cr/dt = u m_a V_a / (4π R_p³). `m_a` and `V_a` come from the melt model, which is refused."""
    return u * m_a * v_a / (4.0 * math.pi * r_p ** 3)


# ── Energy balance — 2021 eqs (10)–(11), PDF p11 ───────────────────────────────────────────────
def mantle_rate(*, q_m: float, q_c: float, h_m: float, d_cr_rate: float, t_m: float, t_l: float,
                stefan: float, eps_m: float, rho_m: float, c_pm: float, v_m: float, a_m: float, a_c: float,
                rho_cr: float, l_m: float, c_pcr: float) -> float:
    """ρ_m C_pm V_m ϵ_m (St + 1) dT_m/dt = −{q_m + ρ_cr Ḋ_cr [L_m + C_pcr (T_m − T_l)]} A_m + q_c A_c + H_m V_m."""
    rhs = -(q_m + rho_cr * d_cr_rate * (l_m + c_pcr * (t_m - t_l))) * a_m + q_c * a_c + h_m * v_m
    return rhs / (rho_m * c_pm * v_m * eps_m * (stefan + 1.0))


def core_rate(*, q_c: float, rho_c: float, c_pc: float, v_c: float, eps_c: float, a_c: float) -> float:
    """ρ_c C_pc V_c ϵ_c dT_c/dt = −q_c A_c."""
    return -q_c * a_c / (rho_c * c_pc * v_c * eps_c)


# ── Lid growth — 2019 SI eq. (20), PDF p6 ──────────────────────────────────────────────────────
def lid_rate(*, q_m: float, d_cr_rate: float, lid_base_gradient: float, t_m: float, t_l: float,
             t_s: float, rho_m: float, c_m: float, rho_cr: float, l_m: float, k_m: float) -> float:
    """ρ_m C_m (T_m − T_l) dD_l/dt = −{q_m − ρ_cr [L_m + C_m (T_m − T_s)] dD_cr/dt} − k_m ∂T/∂r|_{R_l}.

    ⚠ **The last term is wired `−`: the v2 interpretation.** The render of PDF p6 prints `+`; Samuel+ 2021
    (PDF p11) says that term carries a sign typo and prints no corrected equation (v2 §3, risk 3).
    The braces hold `C_m (T_m − T_s)` as printed — not the `C_cr (T_m − T_l)` of 2019 SI eq. (2)."""
    rhs = -(q_m - rho_cr * (l_m + c_m * (t_m - t_s)) * d_cr_rate) - k_m * lid_base_gradient
    return rhs / (rho_m * c_m * (t_m - t_l))


# ── Refused slots ──────────────────────────────────────────────────────────────────────────────
def heat_production(*_args, **_kwargs) -> float:
    raise Refused("H_m and H_cr are not built: the crustal-enrichment definition (v2 §3, Drilleau's) has "
                  "no printed split, and the decay data have no chosen source")


def melt_state(*_args, **_kwargs) -> dict:
    raise Refused("melt fraction, solidus and Stefan number are not built: 2019 SI eqs (14)–(15), (19) "
                  "and 2021 eqs (8)–(9) disagree, and ΔT_sol is not printed")
