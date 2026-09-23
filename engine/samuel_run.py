# Samuel 층 없는 모형의 시간 적분 — 판 2 A0: RK4 로 (T_c, T_m, D_l, D_cr) 를 0.001 → 4.5 Gyr 까지 민다
"""Plate 2's integration: the no-layer Samuel model from t = 0.001 Gyr to 4.5 Gyr (pre-registration v2 §5 A0,
v2-3 … v2-8; brief `c18bbe3c`).

State `(T_c, T_m, D_l, D_cr)`. Classical RK4 with `h = min(cap, 0.1 τ)` — the same scheme as `core_history.integrate`,
**written again here, not called**: that function hard-wires its own `rates()` and its two-temperature
state, and the pre-registration forbids editing it (v2 §1). The lid's temperature profile (`samuel_lid`)
is not an RK state: it advances once per accepted step with the step's end values (operator splitting),
and its base gradient is held through the four RK stages.

Inputs: `samuel_thermal` only, plus the engine's Mars profile (`samuel_structure`, v2-7). Choices no paper
prints are arguments of `run()` and printed by the caller.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import samuel_lid as sl                # noqa: E402
import samuel_model as sm              # noqa: E402
import samuel_thermal as st            # noqa: E402

GYR_S = 3.15576e16
AGE_GYR = 4.5
D_CR_0_M = 1.0                         # 2021 PDF p12: "small values for D_cr = 1 m and D_l = 10 m"
D_L_0_M = 10.0


def _shell(r_out: float, r_in: float) -> float:
    return 4.0 / 3.0 * math.pi * (r_out ** 3 - r_in ** 3)


class Setup:
    """One run's fixed choices. Every field is printed with the result."""

    def __init__(self, *, lam: float, profile, g: float, g_c: float, eps_mode: str = "derived",
                 p_m_mode: str = "mid", melt_pressure: str = "engine", stefan_mode: str = "printed",
                 lid_mode: str = "grid", lid_nodes: int = 41, melt_shells: int = 120):
        self.lam, self.profile, self.g, self.g_c = lam, profile, g, g_c
        self.eps_mode, self.p_m_mode = eps_mode, p_m_mode
        self.melt_pressure, self.stefan_mode, self.lid_mode = melt_pressure, stefan_mode, lid_mode
        self.lid_nodes, self.melt_shells = lid_nodes, melt_shells
        self.r_p, self.r_c = st.R_PLANET_M, st.R_CORE_NO_BML_M
        self.eps_frozen = None

    def pressure(self, r: float) -> float:
        return self.profile.pressure(r)

    def melt_p(self, r: float) -> float:
        if self.melt_pressure == "hydrostatic":
            return sm.hydrostatic_pressure(r, rho_m=st.RHO_MANTLE_KG_M3, g=3.7, r_p=self.r_p)
        return self.profile.pressure(r)


def _eta(t: float, p: float) -> float:
    return sm.viscosity(t, p, st.ETA0_NO_BML_PA_S, st.E_STAR_NO_BML_J_PER_MOL, st.V_STAR_NO_BML_M3_PER_MOL,
                        st.T_REF_K, st.P_REF_PA, st.R_GAS_J_PER_MOL_K)


def state_terms(s: Setup, t_c: float, t_m: float, d_l: float, d_cr: float, t_gyr: float,
                lid_gradient: float) -> dict:
    """Everything the right-hand side needs at one state. Raises `sm.Refused` above the Λ ceiling."""
    r_p, r_c, g = s.r_p, s.r_c, s.g
    r_l = r_p - d_l
    t_l = sm.lid_base_temperature(t_m, st.E_STAR_NO_BML_J_PER_MOL, st.A_RH, st.R_GAS_J_PER_MOL_K)
    # δ_u, δ_b and T_b depend on each other through ΔR (2021 eq. (14)); fixed-point iteration from 0.
    d_u = d_b = 0.0
    for _ in range(60):
        d_r = sm.convecting_thickness(r_p, d_l, r_c, d_u, d_b)
        t_b = sm.mantle_base_temperature(t_m, st.ALPHA_SILICATE_PER_K, g, st.CP_MANTLE_J_PER_KG_K, d_r)
        r_top, r_bot = r_l - d_u, r_c + d_b
        p_m = {"mid": s.pressure(0.5 * (r_top + r_bot)), "top": s.pressure(r_top),
               "bottom": s.pressure(r_bot)}[s.p_m_mode]
        eta_m = _eta(t_m, p_m)
        up = sm.upper_layer(t_m, t_l, t_c, t_b, eta_m, rho_m=st.RHO_MANTLE_KG_M3, alpha=st.ALPHA_SILICATE_PER_K,
                            g=g, k_m=st.K_MANTLE_W_PER_M_K, c_pm=st.CP_MANTLE_J_PER_KG_K, r_p=r_p, d_l=d_l,
                            r_c=r_c, ra_c=st.RA_CRITICAL, beta_u=st.BETA_U)
        eta_c = _eta(0.5 * (t_b + t_c), s.pressure(r_c))
        lo = sm.lower_layer(t_m, t_c, t_b, eta_m, eta_c, rho_m=st.RHO_MANTLE_KG_M3, alpha=st.ALPHA_SILICATE_PER_K,
                            g=g, k_m=st.K_MANTLE_W_PER_M_K, c_pm=st.CP_MANTLE_J_PER_KG_K, r_p=r_p, r_c=r_c,
                            t_s=st.T_SURFACE_K)
        new_u, new_b = up["delta_u"], lo["delta_b"]
        if abs(new_u - d_u) < 1e-6 and abs(new_b - d_b) < 1e-6:
            d_u, d_b = new_u, new_b
            break
        d_u, d_b = new_u, new_b
    r_top, r_bot = r_l - d_u, r_c + d_b
    # ϵ_m — v2-7 ①, and its two sensitivity forms
    eps = sm.mantle_mean_ratio(t_m, t_b, r_top, r_bot)
    if s.eps_mode == "one":
        eps = 1.0
    elif s.eps_mode == "frozen":
        if s.eps_frozen is None:
            s.eps_frozen = eps
        eps = s.eps_frozen
    # heat — Ruedas 2017 back in time, split by 2019 SI eq. (22)
    v_sil = _shell(r_p, r_c)
    v_cr = _shell(r_p, r_p - d_cr)
    h_pm = sm.primitive_heat((AGE_GYR - t_gyr) * 1000.0, st.RHO_MANTLE_KG_M3)
    h_m, h_cr = sm.heat_split(h_pm, v_cr, v_sil - v_cr, s.lam)
    # melt, Stefan, crust growth
    d_ref = sm.crust_reference_thickness(r_p, r_c)
    mkw = dict(d_cr=d_cr, d_ref=d_ref, delta_t_sol=st.DELTA_T_SOL_K,
               extraction_below_pa=st.MELT_EXTRACTION_BELOW_PA, shells=s.melt_shells)
    mi = sm.melt_integrals(t_m, t_b, r_top, r_bot, s.melt_p, **mkw)
    v_conv = _shell(r_top, r_bot)
    sfn = sm.stefan_number if s.stefan_mode == "printed" else sm.stefan_number_total
    stefan = sfn(t_m, t_b, r_top, r_bot, s.melt_p, v_m=v_conv, l_m=st.L_MANTLE_J_PER_KG,
                 c_m=st.CP_MANTLE_J_PER_KG_K, dt_k=1.0, **mkw)
    if up["subcritical"] or mi["shallow_v"] == 0.0:
        d_cr_rate = 0.0
    else:
        u = sm.convective_velocity(up["ra"], st.RA_CRITICAL, st.U0_M_PER_S)
        d_cr_rate = sm.crust_growth_rate(u, mi["shallow_phi_v"] / mi["shallow_v"], mi["shallow_v"], r_p)
    a_m, a_c = 4 * math.pi * r_l ** 2, 4 * math.pi * r_c ** 2
    dtm = sm.mantle_rate(q_m=up["q_m"], q_c=lo["q_c"], h_m=h_m, d_cr_rate=d_cr_rate, t_m=t_m, t_l=t_l,
                         stefan=stefan, eps_m=eps, rho_m=st.RHO_MANTLE_KG_M3, c_pm=st.CP_MANTLE_J_PER_KG_K,
                         v_m=v_sil, a_m=a_m, a_c=a_c, rho_cr=st.RHO_CRUST_KG_M3, l_m=st.L_MANTLE_J_PER_KG,
                         c_pcr=st.CP_CRUST_J_PER_KG_K)
    dtc = sm.core_rate(q_c=lo["q_c"], rho_c=st.RHO_CORE_KG_M3, c_pc=st.CP_CORE_J_PER_KG_K,
                       v_c=4 / 3 * math.pi * r_c ** 3, eps_c=st.EPSILON_CORE, a_c=a_c)
    if s.lid_mode == "quasi_steady":
        lid_gradient = sl.quasi_steady_gradient(r_p=r_p, d_l=d_l, d_cr=d_cr, t_l=t_l, t_s=st.T_SURFACE_K,
                                                k_m=st.K_MANTLE_W_PER_M_K, k_cr=st.K_CRUST_W_PER_M_K,
                                                h_m=h_m, h_cr=h_cr)
    ddl = sm.lid_rate(q_m=up["q_m"], d_cr_rate=d_cr_rate, lid_base_gradient=lid_gradient, t_m=t_m, t_l=t_l,
                      t_s=st.T_SURFACE_K, rho_m=st.RHO_MANTLE_KG_M3, c_m=st.CP_MANTLE_J_PER_KG_K,
                      rho_cr=st.RHO_CRUST_KG_M3, l_m=st.L_MANTLE_J_PER_KG, k_m=st.K_MANTLE_W_PER_M_K)
    return {"dtc": dtc, "dtm": dtm, "ddl": ddl, "ddcr": d_cr_rate, "t_l": t_l, "t_b": t_b, "delta_u": d_u,
            "delta_b": d_b, "q_m": up["q_m"], "q_c": lo["q_c"], "ra": up["ra"], "subcritical": up["subcritical"],
            "eps_m": eps, "stefan": stefan, "h_m": h_m, "h_cr": h_cr, "p_m": p_m,
            "ceiling": sm.crust_enrichment_ceiling(v_cr, v_sil - v_cr), "lid_gradient": lid_gradient}


STEP_FRACTION = 0.1                    # core_history's h = min(cap, 0.1 τ), Brief 157


def _tau_s(y: list, f: dict) -> float:
    """The shortest e-folding time among the states that can move fast: T_c, T_m, D_l, and D_cr once it
    is thicker than 1 km (a 1 m seed crust would otherwise set the step)."""
    taus = []
    for val, rate in ((y[0], f["dtc"]), (y[1], f["dtm"]), (y[2], f["ddl"])):
        if rate:
            taus.append(abs(val / rate))
    if y[3] > 1e3 and f["ddcr"]:
        taus.append(abs(y[3] / f["ddcr"]))
    return min(taus) if taus else float("inf")


def run(s: Setup, cap_myr: float) -> dict:
    """RK4 from T_INITIAL_ROW_GYR to AGE_GYR with core_history's step rule, h = min(cap, 0.1 τ), landing
    exactly on the end. A refusal (Λ above its ceiling) stops the run and is returned with its time."""
    t0 = st.T_INITIAL_ROW_GYR
    cap = cap_myr * 1e-3 * GYR_S
    y = [st.T_CORE_0_NO_BML_K, st.T_MANTLE_0_NO_BML_K, D_L_0_M, D_CR_0_M]
    lid = sl.LidGrid(s.lid_nodes, r_p=s.r_p, t_s=st.T_SURFACE_K, rho_m=st.RHO_MANTLE_KG_M3,
                     c_m=st.CP_MANTLE_J_PER_KG_K, k_m=st.K_MANTLE_W_PER_M_K, rho_cr=st.RHO_CRUST_KG_M3,
                     c_cr=st.CP_CRUST_J_PER_KG_K, k_cr=st.K_CRUST_W_PER_M_K)
    t_l0 = sm.lid_base_temperature(y[1], st.E_STAR_NO_BML_J_PER_MOL, st.A_RH, st.R_GAS_J_PER_MOL_K)
    lid.start(y[2], t_l0)
    grad = (st.T_SURFACE_K - t_l0) / y[2]
    rows = []
    t = t0
    n = 0
    h_min = None
    worst = (0.0, None)
    while True:
        try:
            f1 = state_terms(s, *y, t, grad)
        except sm.Refused as e:
            return {"refused": str(e), "refused_at_gyr": t, "rows": rows, "n_steps": n}
        rows.append({"t": t, "t_c": y[0], "t_m": y[1], "d_l": y[2], "d_cr": y[3], "delta_u": f1["delta_u"],
                     "q_m": f1["q_m"], "q_c": f1["q_c"], "eps_m": f1["eps_m"], "stefan": f1["stefan"],
                     "subcritical": f1["subcritical"], "p_m": f1["p_m"], "ceiling": f1["ceiling"]})
        if s.lam / f1["ceiling"] > worst[0]:
            worst = (s.lam / f1["ceiling"], t)
        remaining = (AGE_GYR - t) * GYR_S
        if remaining <= 1e-9 * GYR_S:
            break
        h = min(cap, STEP_FRACTION * _tau_s(y, f1), remaining)
        h_min = h if h_min is None else min(h_min, h)
        dt_gyr = h / GYR_S
        try:
            k1 = _rates(f1)
            y2 = [a + 0.5 * h * b for a, b in zip(y, k1)]
            k2 = _rates(state_terms(s, *y2, t + 0.5 * dt_gyr, grad))
            y3 = [a + 0.5 * h * b for a, b in zip(y, k2)]
            k3 = _rates(state_terms(s, *y3, t + 0.5 * dt_gyr, grad))
            y4 = [a + h * b for a, b in zip(y, k3)]
            k4 = _rates(state_terms(s, *y4, t + dt_gyr, grad))
        except sm.Refused as e:
            return {"refused": str(e), "refused_at_gyr": t, "rows": rows, "n_steps": n}
        y = [a + h * (b + 2 * c + 2 * d + e) / 6.0 for a, b, c, d, e in zip(y, k1, k2, k3, k4)]
        t = AGE_GYR if h == remaining else t + dt_gyr
        n += 1
        # the lid profile: one implicit step with the step's end values
        t_l = sm.lid_base_temperature(y[1], st.E_STAR_NO_BML_J_PER_MOL, st.A_RH, st.R_GAS_J_PER_MOL_K)
        v_sil, v_cr = _shell(s.r_p, s.r_c), _shell(s.r_p, s.r_p - y[3])
        h_pm = sm.primitive_heat((AGE_GYR - t) * 1000.0, st.RHO_MANTLE_KG_M3)
        try:
            h_m, h_cr = sm.heat_split(h_pm, v_cr, v_sil - v_cr, s.lam)
        except sm.Refused as e:
            return {"refused": str(e), "refused_at_gyr": t, "rows": rows, "n_steps": n}
        grad = lid.step(h, d_l=y[2], d_cr=y[3], t_l=t_l, h_m=h_m, h_cr=h_cr)
    return {"rows": rows, "n_steps": n, "cap_myr": cap_myr, "h_min_myr": h_min / GYR_S * 1e3,
            "max_lambda_over_ceiling": worst}


def _rates(f: dict) -> list:
    return [f["dtc"], f["dtm"], f["ddl"], f["ddcr"]]


# ── A0 — pre-registration v2 §5 ─────────────────────────────────────────────────────────────
def read_panel(path: Path) -> list:
    return [tuple(map(float, line.split())) for line in path.read_text().splitlines() if line.strip()]


def at(rows: list, key: str, t_gyr: float) -> float:
    for a, b in zip(rows, rows[1:]):
        if a["t"] <= t_gyr <= b["t"]:
            w = (t_gyr - a["t"]) / (b["t"] - a["t"])
            return a[key] + w * (b[key] - a[key])
    return rows[-1][key] if t_gyr >= rows[-1]["t"] else rows[0][key]


def a0(rows: list, tc_data: list, tm_data: list) -> dict:
    """The seven conditions of A0 and their values."""
    tc_end, tm_end = rows[-1]["t_c"], rows[-1]["t_m"]
    win = [(tt, v) for tt, v in tc_data if 0.5 <= tt <= 4.5]
    rms_c = math.sqrt(sum((at(rows, "t_c", tt) - v) ** 2 for tt, v in win) / len(win))
    winm = [(tt, v) for tt, v in tm_data if 0.5 <= tt <= 4.5]
    rms_m = math.sqrt(sum((at(rows, "t_m", tt) - v) ** 2 for tt, v in winm) / len(winm))
    tc1 = at(rows, "t_c", 1.0) - rows[0]["t_c"]
    tm1 = at(rows, "t_m", 1.0) - rows[0]["t_m"]
    peak = max(rows, key=lambda r: r["t_m"])
    peak_ok = peak["t_m"] > rows[0]["t_m"] and peak["t_m"] > rows[-1]["t_m"] and 0.5 <= peak["t"] <= 2.0
    c = {"㉠c": (tc_end, abs(tc_end - 2081.49) <= 40), "㉠m": (tm_end, abs(tm_end - 1867.39) <= 50),
         "㉡c": (rms_c, rms_c <= 40), "㉡m": (rms_m, rms_m <= 50), "①": (tc1, tc1 < 0),
         "②": ((peak["t_m"], peak["t"]), peak_ok), "①′": (tm1, tm1 > 0)}
    return {"conditions": c, "pass": all(ok for _, ok in c.values())}
