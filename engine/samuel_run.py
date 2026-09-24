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
import samuel_layer as lay             # noqa: E402
import samuel_lid as sl                # noqa: E402
import samuel_model as sm              # noqa: E402
import samuel_thermal as st            # noqa: E402

GYR_S = 3.15576e16
AGE_GYR = 4.5
D_CR_0_M = 1.0                         # 2021 PDF p12: "small values for D_cr = 1 m and D_l = 10 m"
D_L_0_M = 10.0


#: The two reproduction targets' own constants (2023 Fig. 1 caption and source data, `samuel_thermal`).
#: "no_bml" is plate 2 (panels a–f); "bml" is plate 4 (panels g–l), whose layer is declared on `Setup`.
MODELS = {
    "no_bml": dict(eta0=st.ETA0_NO_BML_PA_S, e_star=st.E_STAR_NO_BML_J_PER_MOL, v_star=st.V_STAR_NO_BML_M3_PER_MOL,
                   r_c=st.R_CORE_NO_BML_M, t_c0=st.T_CORE_0_NO_BML_K, t_m0=st.T_MANTLE_0_NO_BML_K),
    "bml": dict(eta0=st.ETA0_PA_S, e_star=st.E_STAR_J_PER_MOL, v_star=st.V_STAR_M3_PER_MOL,
                r_c=st.R_CORE_M, t_c0=st.T_CORE_0_K, t_m0=st.T_MANTLE_0_K),
}


def _shell(r_out: float, r_in: float) -> float:
    return 4.0 / 3.0 * math.pi * (r_out ** 3 - r_in ** 3)


class Setup:
    """One run's fixed choices. Every field is printed with the result."""

    def __init__(self, *, lam: float, profile, g: float, g_c: float, eps_mode: str = "derived",
                 p_m_mode: str = "mid", melt_pressure: str = "engine", stefan_mode: str = "printed",
                 lid_mode: str = "grid", lid_nodes: int = 41, melt_shells: int = 1920,
                 fixed_lid_m: float | None = None, delta_b_cap_fraction: float = 0.5,
                 root_branch: str = "nearest", path_check_every: int = 0, model: str = "no_bml",
                 layer: dict | None = None):
        self.lam, self.profile, self.g, self.g_c = lam, profile, g, g_c
        self.model = model
        m = MODELS[model]
        self.eta0, self.e_star, self.v_star = m["eta0"], m["e_star"], m["v_star"]
        self.t_c0, self.t_m0 = m["t_c0"], m["t_m0"]
        self.eps_mode, self.p_m_mode = eps_mode, p_m_mode
        self.melt_pressure, self.stefan_mode, self.lid_mode = melt_pressure, stefan_mode, lid_mode
        self.lid_nodes, self.melt_shells = lid_nodes, melt_shells
        self.r_p, self.r_c = st.R_PLANET_M, m["r_c"]
        self.eps_frozen = None
        # L1 comparison plate (v2 §2 plate 2′): the lid does not grow; its thickness is declared.
        self.fixed_lid_m = fixed_lid_m
        # δ_b guard (v2-14, our derivation): δ_b ≤ fraction · (R_l − δ_u − R_c); sensitivity ¼ and 1
        self.delta_b_cap_fraction = delta_b_cap_fraction
        self.guard_stage_hits: list = []   # (t, |T_c − T_b|) of every RK stage the guard bit, not only step starts
        self.guard_iter_hits: list = []    # (t, |T_c − T_b|) of every fixed-point iteration the guard bit
        # v2-15: evaluations whose δ_u/δ_b fixed point hit the 60-iteration limit without converging —
        # (t, |Δδ_u| and |Δδ_b| of the last two iterations, m). Recorded, not acted on.
        self.fixed_point_limit_hits: list = []
        self.fixed_point_start: tuple | None = None   # the last converged (δ_u, δ_b) — the warm start
        self.multi_root_evals = 0
        self.root_jumps: list = []      # (t, old δ_b, new δ_b, T_c − T_b)
        self.root_notes: list = []
        self.last_root_count = None
        self.root_branch = root_branch             # v2-17 supplement 3 ①: nearest | smallest | largest | middle
        self.path_check_every = path_check_every   # supplement 2: cold-start comparison every n-th evaluation
        self.path_checks: list = []
        self.eval_count = 0
        # Plate 4 (v2-23 · v2-24): the basal layer. `layer` declares d_d, k_d, lambda_d, fe_mean, fe_top,
        # nodes, melting, source. D_d = 0 is no layer at all — the plate 2 path, untouched (B1).
        self.layer = layer if layer and layer["d_d"] != 0.0 else None
        self.r_base = self.r_c if self.layer is None else self.r_c + self.layer["d_d"]
        self.layer_grid = None
        self.layer_q = None                        # (q_c, q_d) of the layer profile, held through a step
        self.layer_t_i = None                      # T_i of the last evaluation — the layer step's top value

    def eta(self, t: float, p: float) -> float:
        return sm.viscosity(t, p, self.eta0, self.e_star, self.v_star, st.T_REF_K, st.P_REF_PA, st.R_GAS_J_PER_MOL_K)

    def pressure(self, r: float) -> float:
        return self.profile.pressure(r)

    def melt_p(self, r: float) -> float:
        if self.melt_pressure == "hydrostatic":
            return sm.hydrostatic_pressure(r, rho_m=st.RHO_MANTLE_KG_M3, g=3.7, r_p=self.r_p)
        return self.profile.pressure(r)


BISECT_ITERS = 50                      # v2-17 supplement: bracket solves
INNER_SCAN = 48
OUTER_SCAN = 32
ROOT_JUMP_M = 5e3                      # a lost root: the chosen δ_b moves by more than this as roots vanish


def solve_layers(s: "Setup", t_c: float, t_m: float, d_l: float, t_l: float, prev, branch: str):
    """(δ_u, δ_b, inner roots, up, lo, T_b, P_m, η_m, note) — no side effects; None if δ_u has no bracket.

    Outer δ_u: bisection on F(δ_u) = G_u(δ_u, δ_b*(δ_u)) − δ_u, in the scanned bracket nearest the previous
    δ_u. Inner δ_b: every root of G_b(δ_u, ·) − δ_b on [0, shell − δ_u] by scan + bisection, then chosen by
    `branch` — "nearest" the previous δ_b (v2-17 supplement 1, the main path); "smallest", "largest",
    "middle" (of three, else nearest) the sensitivity branches (supplement 3 ①). With no previous state,
    "nearest" takes a root where the iteration map is stable, |∂G_b/∂δ_b| < 1, the smaller of two
    (supplement 3 ②)."""
    r_p, r_c, g = s.r_p, s.r_base, s.g
    r_l = r_p - d_l

    def layers(du, db):
        d_r = sm.convecting_thickness(r_p, d_l, r_c, du, db)
        t_b_ = sm.mantle_base_temperature(t_m, st.ALPHA_SILICATE_PER_K, g, st.CP_MANTLE_J_PER_KG_K, d_r)
        # with a layer, (17)–(20) take T_i = T′_b + ΔT′_b and R_c + D_d in place of T_c and R_c (v2-24 ②)
        t_bot = t_c if s.layer is None else t_b_ + layer_contrast(s, t_m)
        rt, rb = r_l - du, r_c + db
        p_m_ = {"mid": s.pressure(0.5 * (rt + rb)), "top": s.pressure(rt), "bottom": s.pressure(rb)}[s.p_m_mode]
        eta_m_ = s.eta(t_m, p_m_)
        up_ = sm.upper_layer(t_m, t_l, t_bot, t_b_, eta_m_, rho_m=st.RHO_MANTLE_KG_M3, alpha=st.ALPHA_SILICATE_PER_K,
                             g=g, k_m=st.K_MANTLE_W_PER_M_K, c_pm=st.CP_MANTLE_J_PER_KG_K, r_p=r_p, d_l=d_l,
                             r_c=r_c, ra_c=st.RA_CRITICAL, beta_u=st.BETA_U)
        eta_c_ = s.eta(0.5 * (t_b_ + t_bot), s.pressure(r_c))
        cap_ = s.delta_b_cap_fraction * (r_l - up_["delta_u"] - r_c)
        lo_ = sm.lower_layer(t_m, t_bot, t_b_, eta_m_, eta_c_, rho_m=st.RHO_MANTLE_KG_M3, alpha=st.ALPHA_SILICATE_PER_K,
                             g=g, k_m=st.K_MANTLE_W_PER_M_K, c_pm=st.CP_MANTLE_J_PER_KG_K, r_p=r_p, r_c=r_c,
                             t_s=st.T_SURFACE_K, delta_b_cap=cap_)
        return up_, lo_, t_b_, p_m_, eta_m_

    def bisect(f, a, b, fa):
        for _ in range(BISECT_ITERS):
            m = 0.5 * (a + b)
            fm = f(m)
            if (fm > 0) == (fa > 0):
                a, fa = m, fm
            else:
                b = m
        return 0.5 * (a + b)

    def inner_roots(du):
        top = max(r_l - du - r_c, 1.0)
        h = lambda db: layers(du, db)[1]["delta_b"] - db
        roots, a, fa = [], 0.0, h(0.0)
        for k in range(1, INNER_SCAN + 1):
            b = top * k / INNER_SCAN
            fb = h(b)
            if (fa > 0) != (fb > 0):
                roots.append(bisect(h, a, b, fa))
            a, fa = b, fb
        return roots

    ref_b = prev[1] if prev is not None else None
    note = []

    def choose(du, rts, record=False):
        if not rts:
            return None
        if branch == "smallest":
            return min(rts)
        if branch == "largest":
            return max(rts)
        if branch == "middle" and len(rts) == 3:
            return sorted(rts)[1]
        if ref_b is not None:
            return min(rts, key=lambda x: abs(x - ref_b))
        stable = []
        for x in rts:
            e = max(1.0, 1e-6 * x)
            slope = (layers(du, x + e)[1]["delta_b"] - layers(du, x - e)[1]["delta_b"]) / (2 * e)
            if abs(slope) < 1.0:
                stable.append(x)
        pick = min(stable) if stable else min(rts)
        if record:
            note.append(f"첫 평가 근 {len(rts)} · 안정한 근 {len(stable)}"
                        + (" — 임의 선택(작은 쪽)" if len(stable) > 1 else "")
                        + ("" if stable else " — 안정한 근 없음, 가장 작은 근"))
        return pick

    def outer(du):
        db = choose(du, inner_roots(du))
        return math.nan if db is None else layers(du, db)[0]["delta_u"] - du

    top_u = r_l - r_c
    grid = [top_u * k / OUTER_SCAN for k in range(OUTER_SCAN + 1)]
    vals = [outer(x) for x in grid]
    brackets = [(grid[k], grid[k + 1], vals[k]) for k in range(OUTER_SCAN)
                if not (math.isnan(vals[k]) or math.isnan(vals[k + 1])) and (vals[k] > 0) != (vals[k + 1] > 0)]
    if not brackets:
        return None
    ref_u = prev[0] if prev is not None else None
    a, b, fa = (min(brackets, key=lambda br: abs(0.5 * (br[0] + br[1]) - ref_u)) if ref_u is not None
                else brackets[0])
    d_u = bisect(outer, a, b, fa)
    rts = inner_roots(d_u)
    d_b = choose(d_u, rts, record=prev is None)
    up, lo, t_b, p_m, eta_m = layers(d_u, d_b)
    return d_u, d_b, rts, up, lo, t_b, p_m, eta_m, "; ".join(note)


def layer_contrast(s: "Setup", t_m: float) -> float:
    """ΔT′_b = T_i − T′_b = 1.43 R T_m² / E* (2021 PDF p. 13, Deschamps & Sotin 2000)."""
    return 1.43 * st.R_GAS_J_PER_MOL_K * t_m * t_m / s.e_star


def printed_t_b(s: "Setup", t_m: float, d_l: float, d_u: float, d_b: float) -> float:
    """T′_b as printed, α g T_m (R_c + D_d − D_l − δ_u − δ′_b) / C_pm — compared, never used (v2-22 ①)."""
    return t_m + st.ALPHA_SILICATE_PER_K * s.g * t_m * (s.r_base - d_l - d_u - d_b) / st.CP_MANTLE_J_PER_KG_K


def state_terms(s: Setup, t_c: float, t_m: float, d_l: float, d_cr: float, t_gyr: float,
                lid_gradient: float) -> dict:
    """Everything the right-hand side needs at one state. Raises `sm.Refused` above the Λ ceiling."""
    r_p, r_c, g = s.r_p, s.r_c, s.g
    r_l = r_p - d_l
    t_l = sm.lid_base_temperature(t_m, s.e_star, st.A_RH, st.R_GAS_J_PER_MOL_K)
    # δ_u, δ_b and T_b depend on each other through ΔR (2021 eq. (14)). Solved by brackets — v2-17
    # supplements 1–3, our choice; see `solve_layers`.
    guard_gap = None
    prev = s.fixed_point_start
    sol = solve_layers(s, t_c, t_m, d_l, t_l, prev, s.root_branch)
    if sol is None:
        s.fixed_point_limit_hits.append((t_gyr, math.nan, math.nan))
        raise sm.Refused(f"no bracket for δ_u at t = {t_gyr:.4f} Gyr (v2-17 supplement)")
    d_u, d_b, rts, up, lo, t_b, p_m, eta_m, note = sol
    if note:
        s.root_notes.append(f"{t_gyr:.4f} Gyr: {note}")
    if len(rts) > 1:
        s.multi_root_evals += 1
    if prev is not None and s.last_root_count is not None and len(rts) < s.last_root_count \
            and abs(d_b - prev[1]) > ROOT_JUMP_M:
        s.root_jumps.append((t_gyr, prev[1], d_b, t_c - t_b))
    s.last_root_count = len(rts)
    if s.path_check_every and s.eval_count % s.path_check_every == 0 and len(s.path_checks) < 20:
        cold = solve_layers(s, t_c, t_m, d_l, t_l, None, s.root_branch)
        s.path_checks.append((t_gyr, len(rts), d_u, d_b, cold[0] if cold else math.nan,
                              cold[1] if cold else math.nan, [x for x in rts], t_c - t_b))
    s.eval_count += 1
    if lo["guarded"]:
        guard_gap = abs(t_c - t_b)
        s.guard_iter_hits.append((t_gyr, guard_gap))
    s.fixed_point_start = (d_u, d_b)
    r_top, r_bot = r_l - d_u, s.r_base + d_b
    # ⚠ any iteration counts, not only the last (audit seat: the last alone missed 67 bites at Λ 20, cap 10)
    if guard_gap is not None:
        s.guard_stage_hits.append((t_gyr, guard_gap))
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
    lay_terms = None
    if s.layer is None:
        h_m, h_cr = sm.heat_split(h_pm, v_cr, v_sil - v_cr, s.lam)
    else:
        lay_terms = _layer_heat(s, h_pm, v_sil, v_cr)
        h_m, h_cr = lay_terms["h_m"], lay_terms["h_cr"]
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
    q_c_core, q_base, a_base, v_bal = lo["q_c"], lo["q_c"], a_c, v_sil
    if s.layer is not None:
        # (18): the mantle takes q_d A_d over V_conv′; the core balance (11) takes the layer's q_c (v2-23 §1)
        t_i = t_b + layer_contrast(s, t_m)
        s.layer_t_i = t_i
        if s.layer_grid is None:
            _start_layer(s, t_c, t_i)
        q_c_core, q_base = s.layer_q
        a_base = 4 * math.pi * s.r_base ** 2
        v_bal = _shell(r_l, s.r_base)
        lay_terms["v_conv_p"] = v_bal
        lay_terms.update(t_i=t_i, q_d=q_base, q_c_layer=q_c_core,
                         t_b_printed=printed_t_b(s, t_m, d_l, d_u, d_b))
    dtm = sm.mantle_rate(q_m=up["q_m"], q_c=q_base, h_m=h_m, d_cr_rate=d_cr_rate, t_m=t_m, t_l=t_l,
                         stefan=stefan, eps_m=eps, rho_m=st.RHO_MANTLE_KG_M3, c_pm=st.CP_MANTLE_J_PER_KG_K,
                         v_m=v_bal, a_m=a_m, a_c=a_base, rho_cr=st.RHO_CRUST_KG_M3, l_m=st.L_MANTLE_J_PER_KG,
                         c_pcr=st.CP_CRUST_J_PER_KG_K)
    dtc = sm.core_rate(q_c=q_c_core, rho_c=st.RHO_CORE_KG_M3, c_pc=st.CP_CORE_J_PER_KG_K,
                       v_c=4 / 3 * math.pi * r_c ** 3, eps_c=st.EPSILON_CORE, a_c=a_c)
    if s.lid_mode == "quasi_steady":
        lid_gradient = sl.quasi_steady_gradient(r_p=r_p, d_l=d_l, d_cr=d_cr, t_l=t_l, t_s=st.T_SURFACE_K,
                                                k_m=st.K_MANTLE_W_PER_M_K, k_cr=st.K_CRUST_W_PER_M_K,
                                                h_m=h_m, h_cr=h_cr)
    ddl = sm.lid_rate(q_m=up["q_m"], d_cr_rate=d_cr_rate, lid_base_gradient=lid_gradient, t_m=t_m, t_l=t_l,
                      t_s=st.T_SURFACE_K, rho_m=st.RHO_MANTLE_KG_M3, c_m=st.CP_MANTLE_J_PER_KG_K,
                      rho_cr=st.RHO_CRUST_KG_M3, l_m=st.L_MANTLE_J_PER_KG, k_m=st.K_MANTLE_W_PER_M_K)
    if s.fixed_lid_m is not None:
        ddl = 0.0
    return {"dtc": dtc, "dtm": dtm, "ddl": ddl, "ddcr": d_cr_rate, "t_l": t_l, "t_b": t_b, "delta_u": d_u,
            "delta_b": d_b, "q_m": up["q_m"], "q_c": lo["q_c"], "ra": up["ra"], "subcritical": up["subcritical"],
            "guarded": guard_gap is not None, "guard_gap": guard_gap, "delta_b_raw_over_shell": lo["delta_b_raw"] / (r_l - d_u - r_c),
            "tc_tb_gap": abs(t_c - t_b),
            "eps_m": eps, "stefan": stefan, "h_m": h_m, "h_cr": h_cr, "p_m": p_m,
            "ceiling": sm.crust_enrichment_ceiling(v_cr, v_sil - v_cr), "lid_gradient": lid_gradient,
            "layer": lay_terms}


def _layer_heat(s: Setup, h_pm: float, v_sil: float, v_cr: float) -> dict:
    """Heat with a layer (v2-22 ② · v2-23 §4 ②). Eq. (1) first, on the whole silicate: H_d = Λ_d H_pm and
    H′_m = H_pm [1 − (V_d / V_sil′)(Λ_d − 1)], V_sil′ = V_sil − V_d (the preprint's V′_m, crust included).
    Then the crust share from V_sil′ — ⚠ our interpretation. V_conv′ (the published (18)'s V′_m, R_c + D_d
    to R_l) is where the mantle share is spent; both volumes are returned so every run prints them."""
    lam_d = s.layer["lambda_d"]
    v_d = _shell(s.r_base, s.r_c)
    v_sil_p = v_sil - v_d
    h_mp = h_pm * (1.0 - v_d / v_sil_p * (lam_d - 1.0))
    h_m, h_cr = sm.heat_split(h_mp, v_cr, v_sil_p - v_cr, s.lam)
    return {"h_d": lam_d * h_pm, "h_m_prime": h_mp, "h_m": h_m, "h_cr": h_cr, "v_d": v_d, "v_sil_p": v_sil_p}


def _start_layer(s: Setup, t_c: float, t_i: float) -> None:
    """The layer grid (plate 3), started linear between T_c and T_i (v2-23 §3, our choice)."""
    L = s.layer
    melting = L["melting"]
    s.layer_grid = lay.LayerGrid(L["nodes"], r_c=s.r_c, d_d=L["d_d"], c_p=st.CP_MANTLE_J_PER_KG_K, k_d=L["k_d"],
                                 fe_mean=L["fe_mean"], fe_top=L["fe_top"],
                                 latent=st.L_MANTLE_J_PER_KG if melting else None,
                                 pressure_gpa=(lambda r: s.pressure(r) / 1e9) if melting else None)
    s.layer_grid.start(t_c, t_i)
    s.layer_q = s.layer_grid.fluxes()


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
    y = [s.t_c0, s.t_m0,
         D_L_0_M if s.fixed_lid_m is None else s.fixed_lid_m, D_CR_0_M]
    lid = sl.LidGrid(s.lid_nodes, r_p=s.r_p, t_s=st.T_SURFACE_K, rho_m=st.RHO_MANTLE_KG_M3,
                     c_m=st.CP_MANTLE_J_PER_KG_K, k_m=st.K_MANTLE_W_PER_M_K, rho_cr=st.RHO_CRUST_KG_M3,
                     c_cr=st.CP_CRUST_J_PER_KG_K, k_cr=st.K_CRUST_W_PER_M_K)
    t_l0 = sm.lid_base_temperature(y[1], s.e_star, st.A_RH, st.R_GAS_J_PER_MOL_K)
    lid.start(y[2], t_l0)
    grad = (st.T_SURFACE_K - t_l0) / y[2]
    rows = []
    t = t0
    n = 0
    h_min = None
    n_remesh, remesh_loss = 0, []
    worst = (0.0, None)
    while True:
        try:
            f1 = state_terms(s, *y, t, grad)
        except sm.Refused as e:
            return {"refused": str(e), "refused_at_gyr": t, "rows": rows, "n_steps": n}
        # v2-9 ③ diagnosis: conduction out of the lid base minus the heat the mantle brings, beside dD_l/dt
        rows.append({"ddl": f1["ddl"], "lid_net": -st.K_MANTLE_W_PER_M_K * f1["lid_gradient"] - f1["q_m"],
                     "crust_term": st.RHO_CRUST_KG_M3 * (st.L_MANTLE_J_PER_KG + st.CP_MANTLE_J_PER_KG_K
                                                         * (y[1] - st.T_SURFACE_K)) * f1["ddcr"],
                     "t": t, "t_c": y[0], "t_m": y[1], "d_l": y[2], "d_cr": y[3], "delta_u": f1["delta_u"],
                     "q_m": f1["q_m"], "q_c": f1["q_c"], "eps_m": f1["eps_m"], "stefan": f1["stefan"],
                     "subcritical": f1["subcritical"], "p_m": f1["p_m"], "ceiling": f1["ceiling"],
                     "guarded": f1["guarded"], "guard_gap": f1["guard_gap"], "delta_b_raw_over_shell": f1["delta_b_raw_over_shell"],
                     "tc_tb_gap": f1["tc_tb_gap"], "layer": f1["layer"]})
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
        t_l = sm.lid_base_temperature(y[1], s.e_star, st.A_RH, st.R_GAS_J_PER_MOL_K)
        v_sil, v_cr = _shell(s.r_p, s.r_c), _shell(s.r_p, s.r_p - y[3])
        h_pm = sm.primitive_heat((AGE_GYR - t) * 1000.0, st.RHO_MANTLE_KG_M3)
        try:
            h_m, h_cr = sm.heat_split(h_pm, v_cr, v_sil - v_cr, s.lam)
        except sm.Refused as e:
            return {"refused": str(e), "refused_at_gyr": t, "rows": rows, "n_steps": n}
        if lid.r is not None:
            # diagnosis (v2-12): the heat one linear re-interpolation changes, over the lid both grids share
            lid_r0 = lid.r[:]
            lid_t0 = lid.t[:]
            r_new = [s.r_p - y[2] + i * y[2] / (lid.n - 1) for i in range(lid.n)]
            lo = max(lid_r0[0], r_new[0])
            lid.r, lid.t = r_new, [sl._interp(x, lid_r0, lid_t0) for x in r_new]
            after_shared = _heat_above(lid, lo)
            lid.r, lid.t = lid_r0, lid_t0
            remesh_loss.append(after_shared - _heat_above(lid, lo))
            n_remesh += 1
        grad = lid.step(h, d_l=y[2], d_cr=y[3], t_l=t_l, h_m=h_m, h_cr=h_cr)
        if s.layer_grid is not None:
            # the layer profile: one implicit step with the end T_c and the last stage's T_i (our choice —
            # that stage sits at t + h), H_d = Λ_d H_pm at the end time (v2-23 §3)
            try:
                s.layer_q = s.layer_grid.step(h, t_c=y[0], t_i=s.layer_t_i, h_d=s.layer["lambda_d"] * h_pm, t_now=t)
            except sm.Refused as e:
                return {"refused": str(e), "refused_at_gyr": t, "rows": rows, "n_steps": n}
    return {"rows": rows, "n_steps": n, "cap_myr": cap_myr, "h_min_myr": h_min / GYR_S * 1e3,
            "max_lambda_over_ceiling": worst, "n_remesh": n_remesh,
            "guard_stage_hits": list(s.guard_stage_hits), "guard_iter_hits": list(s.guard_iter_hits),
            "fixed_point_limit_hits": list(s.fixed_point_limit_hits),
            "multi_root_evals": s.multi_root_evals, "root_jumps": list(s.root_jumps), "root_notes": list(s.root_notes),
            "path_checks": list(s.path_checks), "remesh_loss_j": remesh_loss,
            "layer": None if s.layer_grid is None else {
                "describe": s.layer_grid.describe(), "margin": s.layer_grid.margin,
                "max_phi": max(s.layer_grid.phi) if s.layer_grid.latent is not None else None,
                "iterations_max": s.layer_grid.iterations_max, "source": s.layer.get("source")}}


def _heat_above(lid, r_lo: float) -> float:
    """∫ ρC T dV of the lid profile above `r_lo`, by trapezoids on its own nodes (diagnosis)."""
    pts = [(r, tt) for r, tt in zip(lid.r, lid.t) if r >= r_lo]
    if pts and pts[0][0] > r_lo:
        pts.insert(0, (r_lo, sl._interp(r_lo, lid.r, lid.t)))
    tot = 0.0
    for (ra, ta), (rb, tb) in zip(pts, pts[1:]):
        rc = lid.crust[0] if 0.5 * (ra + rb) > lid._r_crust else lid.mantle[0]
        tot += 0.5 * (ra * ra * ta + rb * rb * tb) * 4.0 * math.pi * (rb - ra) * rc
    return tot


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


def curve_values(rows: list) -> dict:
    """The A0 values that need no source data: today's T_c and T_m, the 1 Gyr changes, the T_m peak."""
    peak = max(rows, key=lambda r: r["t_m"])
    return {"T_c today": rows[-1]["t_c"], "T_m today": rows[-1]["t_m"],
            "T_c(1) − T_c0": at(rows, "t_c", 1.0) - rows[0]["t_c"],
            "T_m(1) − T_m0": at(rows, "t_m", 1.0) - rows[0]["t_m"],
            "T_m peak": peak["t_m"], "T_m peak time": peak["t"]}


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


# ── A — pre-registration v2 §5 A (plate 4, 2023 Fig. 1 g–l) ─────────────────────────────────────
def a_layer(rows: list, tc_data: list, tm_data: list) -> dict:
    """The four conditions of A and their values (v2 §5 A; widths are ours, borrowed EDT1 σ)."""
    tc_end, tm_end = rows[-1]["t_c"], rows[-1]["t_m"]
    win = [(tt, v) for tt, v in tc_data if 0.5 <= tt <= 4.5]
    rms_c = math.sqrt(sum((at(rows, "t_c", tt) - v) ** 2 for tt, v in win) / len(win))
    winm = [(tt, v) for tt, v in tm_data if 0.5 <= tt <= 4.5]
    rms_m = math.sqrt(sum((at(rows, "t_m", tt) - v) ** 2 for tt, v in winm) / len(winm))
    tc1 = at(rows, "t_c", 1.0) - rows[0]["t_c"]
    peak = max(rows, key=lambda r: r["t_c"])
    peak_ok = peak["t_c"] > rows[0]["t_c"] and peak["t_c"] > rows[-1]["t_c"] and 1.5 <= peak["t"] <= 3.5
    c = {"㉠": ((tm_end, tc_end), abs(tm_end - 1531.66) <= 20 and abs(tc_end - 2843.69) <= 150),
         "㉡": ((rms_m, rms_c), rms_m <= 20 and rms_c <= 150), "①": (tc1, tc1 > 0),
         "②": ((peak["t_c"], peak["t"]), peak_ok)}
    return {"conditions": c, "pass": all(ok for _, ok in c.values())}
