# 열진화를 층 목록으로 — 층(핵 · 기저층 · 맨틀 · 뚜껑 · 지각)을 자료로 받아 하나의 적분기로 민다 (T2 사전등록)
"""The thermal evolution over a list of layers (pre-registration `prereg-T2-layer-list.md`).

A `Stack` is a list of `Layer`s from the centre out. Each layer names its `kind` — `lumped` (one
temperature: the core), `convective` (one mean temperature with a thermal boundary layer at each side:
the mantle), `conductive` (a temperature grid: the basal layer, the lid) — its radii, its properties and
the rule at its lower boundary. The integrator reads the stack; it does not know which paper built it.

T2 is a reproduction plate: `samuel_stack(...)` builds the stacks of plates 2 and 4 (and 2P, 4P) and this
integrator must give `samuel_run`'s numbers **bit for bit** (T2 §7 R2 · R2P · R4 · R4P). So the arithmetic
here keeps `samuel_run`'s order, and `samuel_run` stays frozen beside it as the comparison.

⚠ **The mantle layer carries the meaning of `V` in eq. (10)/(18) as a field** (T2 §3):
`volume="silicate"` is plate 2's whole-silicate volume (lid and crust included — never registered,
C113, v2-31), `volume="convective"` is plate 4's `V_conv′` as the source prints it.

⚠ **The lid's heat in a layered run** is split as in the run without a layer (`samuel_run.run` calls
`heat_split` on the whole silicate for the lid grid even when a basal layer holds `Λ_d` of the heat). T2
reproduces that; it is reported, not changed here.

Inner core: the core layer has an `inner_core` slot (Nimmo+ 2004 latent and gravitational terms, T2 §6).
It is off in every reproduction stack and nothing here fills it yet — the slot being empty is B1′.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
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
BISECT_ITERS = 50                      # v2-17 supplement: bracket solves
INNER_SCAN = 48
OUTER_SCAN = 32
ROOT_JUMP_M = 5e3
STEP_FRACTION = 0.1                    # core_history's h = min(cap, 0.1 τ), Brief 157


def _shell(r_out: float, r_in: float) -> float:
    return 4.0 / 3.0 * math.pi * (r_out ** 3 - r_in ** 3)


@dataclass
class Layer:
    """One layer. `r_bot`/`r_top` are fixed radii, or None where the state or a neighbour sets them."""
    role: str                          # core · basal · mantle · lid (the crust grows inside the lid)
    kind: str                          # lumped · convective · conductive
    r_bot: float | None
    r_top: float | None
    params: dict = field(default_factory=dict)


class Stack:
    """A list of layers plus the run's options and the state a run carries (root tracking, grids)."""

    def __init__(self, layers: list, *, profile, g: float, options: dict):
        self.layers = layers
        self.profile, self.g = profile, g
        self.opt = options
        self.core = self._one("core")
        self.mantle = self._one("mantle")
        self.lid = self._one("lid")
        self.basal = self._maybe("basal")
        self.r_p = self.lid.r_top
        self.r_c = self.core.r_top
        self.r_base = self.r_c if self.basal is None else self.basal.r_top
        m = self.mantle.params
        self.eta0, self.e_star, self.v_star = m["eta0"], m["e_star"], m["v_star"]
        self.lam = self.lid.params["crust_lambda"]
        # run state (as `samuel_run.Setup` carries it)
        self.eps_frozen = None
        self.guard_stage_hits: list = []
        self.guard_iter_hits: list = []
        self.fixed_point_limit_hits: list = []
        self.fixed_point_start: tuple | None = None
        self.multi_root_evals = 0
        self.root_jumps: list = []
        self.root_notes: list = []
        self.last_root_count = None
        self.path_checks: list = []
        self.eval_count = 0
        self.layer_grid = None
        self.layer_q = None
        self.layer_t_i = None

    def _one(self, role: str) -> Layer:
        got = [x for x in self.layers if x.role == role]
        if len(got) != 1:
            raise ValueError(f"a stack needs exactly one «{role}» layer, got {len(got)}")
        return got[0]

    def _maybe(self, role: str):
        got = [x for x in self.layers if x.role == role]
        return got[0] if got else None

    def eta(self, t: float, p: float) -> float:
        return sm.viscosity(t, p, self.eta0, self.e_star, self.v_star, st.T_REF_K, st.P_REF_PA, st.R_GAS_J_PER_MOL_K)

    def pressure(self, r: float) -> float:
        return self.profile.pressure(r)

    def melt_p(self, r: float) -> float:
        if self.opt["melt_pressure"] == "hydrostatic":
            return sm.hydrostatic_pressure(r, rho_m=st.RHO_MANTLE_KG_M3, g=3.7, r_p=self.r_p)
        return self.profile.pressure(r)


#: the two reproduction targets' constants — the same bundles as `samuel_run.MODELS`
MODELS = {
    "no_bml": dict(eta0=st.ETA0_NO_BML_PA_S, e_star=st.E_STAR_NO_BML_J_PER_MOL, v_star=st.V_STAR_NO_BML_M3_PER_MOL,
                   r_c=st.R_CORE_NO_BML_M, t_c0=st.T_CORE_0_NO_BML_K, t_m0=st.T_MANTLE_0_NO_BML_K),
    "bml": dict(eta0=st.ETA0_PA_S, e_star=st.E_STAR_J_PER_MOL, v_star=st.V_STAR_M3_PER_MOL,
                r_c=st.R_CORE_M, t_c0=st.T_CORE_0_K, t_m0=st.T_MANTLE_0_K),
}


def samuel_stack(*, lam: float, profile, g: float, model: str = "no_bml", layer: dict | None = None,
                 eps_mode: str = "derived", p_m_mode: str = "mid", melt_pressure: str = "engine",
                 stefan_mode: str = "printed", lid_mode: str = "grid", lid_nodes: int = 41,
                 melt_shells: int = 1920, fixed_lid_m: float | None = None, delta_b_cap_fraction: float = 0.5,
                 root_branch: str = "nearest", path_check_every: int = 0, r_c: float | None = None,
                 source_volume: bool = False, source_lid_heat: bool = False) -> Stack:
    """The stacks of plates 2 · 2P (no layer) and 4 · 4P (basal layer) — `samuel_run.Setup`'s arguments,
    as layers. `layer` with D_d = 0 is no layer (B1). `r_c` overrides the bundle's core radius.

    Source-form switches (prereg-source-form-plates, frozen d9d5af99), both off = T2's bit reproduction:
    `source_volume` — the mantle balance over the convective volume as 2021 PDF p. 11 prints it («Vm is
    the volume of the convective mantle»), not plate 2's whole silicate (C113; grade literature);
    `source_lid_heat` — in a layered stack the lid grid's heat is split like the mantle's, eq. (1) first
    and the crust share from V_sil′ (C114; grade our inference — v2-22 ② calls that step our reading)."""
    m = MODELS[model]
    rc = m["r_c"] if r_c is None else r_c
    layer = layer if layer and layer["d_d"] != 0.0 else None
    core = Layer("core", "lumped", 0.0, rc, {"t0": m["t_c0"], "inner_core": None})
    layers = [core]
    if layer is not None:
        layers.append(Layer("basal", "conductive", rc, rc + layer["d_d"], dict(layer)))
    mantle = Layer("mantle", "convective", None, None,
                   {"t0": m["t_m0"], "eta0": m["eta0"], "e_star": m["e_star"], "v_star": m["v_star"],
                    "volume": "convective" if (layer is not None or source_volume) else "silicate",
                    "bottom": "tbl" if layer is None else "grid_flux+jump"})
    layers.append(mantle)
    layers.append(Layer("lid", "conductive", None, st.R_PLANET_M,
                        {"nodes": lid_nodes, "fixed_m": fixed_lid_m, "crust_lambda": lam,
                         "source_heat": source_lid_heat}))
    return Stack(layers, profile=profile, g=g,
                 options=dict(eps_mode=eps_mode, p_m_mode=p_m_mode, melt_pressure=melt_pressure,
                              stefan_mode=stefan_mode, lid_mode=lid_mode, melt_shells=melt_shells,
                              delta_b_cap_fraction=delta_b_cap_fraction, root_branch=root_branch,
                              path_check_every=path_check_every))


def layer_contrast(s: Stack, t_m: float) -> float:
    """ΔT′_b = T_i − T′_b = 1.43 R T_m² / E* (2021 PDF p. 13, Deschamps & Sotin 2000) — the `jump` rule."""
    return 1.43 * st.R_GAS_J_PER_MOL_K * t_m * t_m / s.e_star


def printed_t_b(s: Stack, t_m: float, d_l: float, d_u: float, d_b: float) -> float:
    """T′_b as printed — compared, never used (v2-22 ①)."""
    return t_m + st.ALPHA_SILICATE_PER_K * s.g * t_m * (s.r_base - d_l - d_u - d_b) / st.CP_MANTLE_J_PER_KG_K


def solve_boundary_layers(s: Stack, t_c: float, t_m: float, d_l: float, t_l: float, prev, branch: str):
    """The convective layer's two TBLs and base temperature (2021 (14)–(17)), by brackets (v2-17).
    With a basal layer below, its bottom rule is `grid_flux+jump`: T_i = T′_b + ΔT′_b stands for T_c and
    R_c + D_d for R_c (v2-24 ②)."""
    r_p, r_c, g = s.r_p, s.r_base, s.g
    r_l = r_p - d_l
    jump = s.mantle.params["bottom"] == "grid_flux+jump"
    cap_frac, p_m_mode = s.opt["delta_b_cap_fraction"], s.opt["p_m_mode"]

    def layers(du, db):
        d_r = sm.convecting_thickness(r_p, d_l, r_c, du, db)
        t_b_ = sm.mantle_base_temperature(t_m, st.ALPHA_SILICATE_PER_K, g, st.CP_MANTLE_J_PER_KG_K, d_r)
        t_bot = t_c if not jump else t_b_ + layer_contrast(s, t_m)
        rt, rb = r_l - du, r_c + db
        p_m_ = {"mid": s.pressure(0.5 * (rt + rb)), "top": s.pressure(rt), "bottom": s.pressure(rb)}[p_m_mode]
        eta_m_ = s.eta(t_m, p_m_)
        up_ = sm.upper_layer(t_m, t_l, t_bot, t_b_, eta_m_, rho_m=st.RHO_MANTLE_KG_M3, alpha=st.ALPHA_SILICATE_PER_K,
                             g=g, k_m=st.K_MANTLE_W_PER_M_K, c_pm=st.CP_MANTLE_J_PER_KG_K, r_p=r_p, d_l=d_l,
                             r_c=r_c, ra_c=st.RA_CRITICAL, beta_u=st.BETA_U)
        eta_c_ = s.eta(0.5 * (t_b_ + t_bot), s.pressure(r_c))
        cap_ = cap_frac * (r_l - up_["delta_u"] - r_c)
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


def _heat(s: Stack, h_pm: float, v_sil: float, v_cr: float):
    """(H_m, H_cr, layer terms). No basal layer: the crust share from the whole silicate (2019 SI (22)).
    With one: eq. (1) first on the whole silicate, then the crust share from V_sil′ (v2-22 ② · our reading)."""
    if s.basal is None:
        h_m, h_cr = sm.heat_split(h_pm, v_cr, v_sil - v_cr, s.lam)
        return h_m, h_cr, None
    lam_d = s.basal.params["lambda_d"]
    v_d = _shell(s.r_base, s.r_c)
    v_sil_p = v_sil - v_d
    h_mp = h_pm * (1.0 - v_d / v_sil_p * (lam_d - 1.0))
    h_m, h_cr = sm.heat_split(h_mp, v_cr, v_sil_p - v_cr, s.lam)
    return h_m, h_cr, {"h_d": lam_d * h_pm, "h_m_prime": h_mp, "h_m": h_m, "h_cr": h_cr, "v_d": v_d,
                       "v_sil_p": v_sil_p}


def _start_basal(s: Stack, t_c: float, t_i: float) -> None:
    L = s.basal.params
    melting = L["melting"]
    s.layer_grid = lay.LayerGrid(L["nodes"], r_c=s.r_c, d_d=L["d_d"], c_p=st.CP_MANTLE_J_PER_KG_K, k_d=L["k_d"],
                                 fe_mean=L["fe_mean"], fe_top=L["fe_top"],
                                 latent=st.L_MANTLE_J_PER_KG if melting else None,
                                 pressure_gpa=(lambda r: s.pressure(r) / 1e9) if melting else None,
                                 iron_shift=L.get("iron_shift", True), record=L.get("record", False))
    s.layer_grid.start(t_c, t_i)
    s.layer_q = s.layer_grid.fluxes()


def state_terms(s: Stack, t_c: float, t_m: float, d_l: float, d_cr: float, t_gyr: float,
                lid_gradient: float) -> dict:
    """Every layer's rate at one state. Raises `sm.Refused` above the Λ ceiling or without a bracket."""
    r_p, r_c, g = s.r_p, s.r_c, s.g
    r_l = r_p - d_l
    t_l = sm.lid_base_temperature(t_m, s.e_star, st.A_RH, st.R_GAS_J_PER_MOL_K)
    guard_gap = None
    prev = s.fixed_point_start
    sol = solve_boundary_layers(s, t_c, t_m, d_l, t_l, prev, s.opt["root_branch"])
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
    pce = s.opt["path_check_every"]
    if pce and s.eval_count % pce == 0 and len(s.path_checks) < 20:
        cold = solve_boundary_layers(s, t_c, t_m, d_l, t_l, None, s.opt["root_branch"])
        s.path_checks.append((t_gyr, len(rts), d_u, d_b, cold[0] if cold else math.nan,
                              cold[1] if cold else math.nan, [x for x in rts], t_c - t_b))
    s.eval_count += 1
    if lo["guarded"]:
        guard_gap = abs(t_c - t_b)
        s.guard_iter_hits.append((t_gyr, guard_gap))
    s.fixed_point_start = (d_u, d_b)
    r_top, r_bot = r_l - d_u, s.r_base + d_b
    if guard_gap is not None:
        s.guard_stage_hits.append((t_gyr, guard_gap))
    eps = sm.mantle_mean_ratio(t_m, t_b, r_top, r_bot)
    if s.opt["eps_mode"] == "one":
        eps = 1.0
    elif s.opt["eps_mode"] == "frozen":
        if s.eps_frozen is None:
            s.eps_frozen = eps
        eps = s.eps_frozen
    v_sil = _shell(r_p, r_c)
    v_cr = _shell(r_p, r_p - d_cr)
    h_pm = sm.primitive_heat((AGE_GYR - t_gyr) * 1000.0, st.RHO_MANTLE_KG_M3)
    h_m, h_cr, lay_terms = _heat(s, h_pm, v_sil, v_cr)
    d_ref = sm.crust_reference_thickness(r_p, r_c)
    mkw = dict(d_cr=d_cr, d_ref=d_ref, delta_t_sol=st.DELTA_T_SOL_K,
               extraction_below_pa=st.MELT_EXTRACTION_BELOW_PA, shells=s.opt["melt_shells"])
    mi = sm.melt_integrals(t_m, t_b, r_top, r_bot, s.melt_p, **mkw)
    v_conv = _shell(r_top, r_bot)
    sfn = sm.stefan_number if s.opt["stefan_mode"] == "printed" else sm.stefan_number_total
    stefan = sfn(t_m, t_b, r_top, r_bot, s.melt_p, v_m=v_conv, l_m=st.L_MANTLE_J_PER_KG,
                 c_m=st.CP_MANTLE_J_PER_KG_K, dt_k=1.0, **mkw)
    if up["subcritical"] or mi["shallow_v"] == 0.0:
        d_cr_rate = 0.0
    else:
        u = sm.convective_velocity(up["ra"], st.RA_CRITICAL, st.U0_M_PER_S)
        d_cr_rate = sm.crust_growth_rate(u, mi["shallow_phi_v"] / mi["shallow_v"], mi["shallow_v"], r_p)
    a_m, a_c = 4 * math.pi * r_l ** 2, 4 * math.pi * r_c ** 2
    # the mantle's lower boundary: `tbl` takes the core's q_c; `grid_flux+jump` the basal grid's q_d
    q_c_core, q_base, a_base = lo["q_c"], lo["q_c"], a_c
    if s.mantle.params["bottom"] == "grid_flux+jump":
        t_i = t_b + layer_contrast(s, t_m)
        s.layer_t_i = t_i
        if s.layer_grid is None:
            _start_basal(s, t_c, t_i)
        q_c_core, q_base = s.layer_q
        a_base = 4 * math.pi * s.r_base ** 2
    # the mantle's volume — the layer names its meaning (T2 §3; C113)
    v_bal = v_sil if s.mantle.params["volume"] == "silicate" else _shell(r_l, s.r_base)
    if lay_terms is not None:
        lay_terms["v_conv_p"] = v_bal
        lay_terms.update(t_i=s.layer_t_i, q_d=q_base, q_c_layer=q_c_core,
                         t_b_printed=printed_t_b(s, t_m, d_l, d_u, d_b))
    dtm = sm.mantle_rate(q_m=up["q_m"], q_c=q_base, h_m=h_m, d_cr_rate=d_cr_rate, t_m=t_m, t_l=t_l,
                         stefan=stefan, eps_m=eps, rho_m=st.RHO_MANTLE_KG_M3, c_pm=st.CP_MANTLE_J_PER_KG_K,
                         v_m=v_bal, a_m=a_m, a_c=a_base, rho_cr=st.RHO_CRUST_KG_M3, l_m=st.L_MANTLE_J_PER_KG,
                         c_pcr=st.CP_CRUST_J_PER_KG_K)
    dtc = sm.core_rate(q_c=q_c_core, rho_c=st.RHO_CORE_KG_M3, c_pc=st.CP_CORE_J_PER_KG_K,
                       v_c=4 / 3 * math.pi * r_c ** 3, eps_c=st.EPSILON_CORE, a_c=a_c)
    if s.core.params["inner_core"] is not None:
        raise NotImplementedError("the inner-core term is a slot in T2 (§6) — off in every reproduction stack")
    if s.opt["lid_mode"] == "quasi_steady":
        lid_gradient = sl.quasi_steady_gradient(r_p=r_p, d_l=d_l, d_cr=d_cr, t_l=t_l, t_s=st.T_SURFACE_K,
                                                k_m=st.K_MANTLE_W_PER_M_K, k_cr=st.K_CRUST_W_PER_M_K,
                                                h_m=h_m, h_cr=h_cr)
    ddl = sm.lid_rate(q_m=up["q_m"], d_cr_rate=d_cr_rate, lid_base_gradient=lid_gradient, t_m=t_m, t_l=t_l,
                      t_s=st.T_SURFACE_K, rho_m=st.RHO_MANTLE_KG_M3, c_m=st.CP_MANTLE_J_PER_KG_K,
                      rho_cr=st.RHO_CRUST_KG_M3, l_m=st.L_MANTLE_J_PER_KG, k_m=st.K_MANTLE_W_PER_M_K)
    if s.lid.params["fixed_m"] is not None:
        ddl = 0.0
    return {"dtc": dtc, "dtm": dtm, "ddl": ddl, "ddcr": d_cr_rate, "t_l": t_l, "t_b": t_b, "delta_u": d_u,
            "delta_b": d_b, "q_m": up["q_m"], "q_c": lo["q_c"], "ra": up["ra"], "subcritical": up["subcritical"],
            "guarded": guard_gap is not None, "guard_gap": guard_gap, "delta_b_raw_over_shell": lo["delta_b_raw"] / (r_l - d_u - r_c),
            "tc_tb_gap": abs(t_c - t_b),
            "eps_m": eps, "stefan": stefan, "h_m": h_m, "h_cr": h_cr, "p_m": p_m,
            "ceiling": sm.crust_enrichment_ceiling(v_cr, v_sil - v_cr), "lid_gradient": lid_gradient,
            "layer": lay_terms}


def _tau_s(y: list, f: dict) -> float:
    taus = []
    for val, rate in ((y[0], f["dtc"]), (y[1], f["dtm"]), (y[2], f["ddl"])):
        if rate:
            taus.append(abs(val / rate))
    if y[3] > 1e3 and f["ddcr"]:
        taus.append(abs(y[3] / f["ddcr"]))
    return min(taus) if taus else float("inf")


def _rates(f: dict) -> list:
    return [f["dtc"], f["dtm"], f["ddl"], f["ddcr"]]


def run(s: Stack, cap_myr: float) -> dict:
    """RK4 over the lumped and convective layers' temperatures and the growing lid and crust; the
    conductive grids advance once per accepted step (lid, then basal layer) — `samuel_run.run`'s order."""
    t0 = st.T_INITIAL_ROW_GYR
    cap = cap_myr * 1e-3 * GYR_S
    fixed = s.lid.params["fixed_m"]
    y = [s.core.params["t0"], s.mantle.params["t0"], D_L_0_M if fixed is None else fixed, D_CR_0_M]
    lid = sl.LidGrid(s.lid.params["nodes"], r_p=s.r_p, t_s=st.T_SURFACE_K, rho_m=st.RHO_MANTLE_KG_M3,
                     c_m=st.CP_MANTLE_J_PER_KG_K, k_m=st.K_MANTLE_W_PER_M_K, rho_cr=st.RHO_CRUST_KG_M3,
                     c_cr=st.CP_CRUST_J_PER_KG_K, k_cr=st.K_CRUST_W_PER_M_K)
    t_l0 = sm.lid_base_temperature(y[1], s.e_star, st.A_RH, st.R_GAS_J_PER_MOL_K)
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
        rows.append({"ddl": f1["ddl"], "lid_net": -st.K_MANTLE_W_PER_M_K * f1["lid_gradient"] - f1["q_m"],
                     "crust_term": st.RHO_CRUST_KG_M3 * (st.L_MANTLE_J_PER_KG + st.CP_MANTLE_J_PER_KG_K
                                                         * (y[1] - st.T_SURFACE_K)) * f1["ddcr"],
                     "t": t, "t_c": y[0], "t_m": y[1], "d_l": y[2], "d_cr": y[3], "delta_u": f1["delta_u"],
                     "q_m": f1["q_m"], "q_c": f1["q_c"], "eps_m": f1["eps_m"], "stefan": f1["stefan"],
                     "subcritical": f1["subcritical"], "p_m": f1["p_m"], "ceiling": f1["ceiling"],
                     "guarded": f1["guarded"], "guard_gap": f1["guard_gap"], "delta_b_raw_over_shell": f1["delta_b_raw_over_shell"],
                     "tc_tb_gap": f1["tc_tb_gap"], "t_b": f1["t_b"], "layer": f1["layer"]})
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
        t_l = sm.lid_base_temperature(y[1], s.e_star, st.A_RH, st.R_GAS_J_PER_MOL_K)
        v_sil, v_cr = _shell(s.r_p, s.r_c), _shell(s.r_p, s.r_p - y[3])
        h_pm = sm.primitive_heat((AGE_GYR - t) * 1000.0, st.RHO_MANTLE_KG_M3)
        try:
            if s.basal is not None and s.lid.params["source_heat"]:
                h_m, h_cr, _ = _heat(s, h_pm, v_sil, v_cr)     # C114 source form: the mantle's split
            else:
                # ⚠ the lid grid's heat is split without the basal layer even when there is one (module note)
                h_m, h_cr = sm.heat_split(h_pm, v_cr, v_sil - v_cr, s.lam)
        except sm.Refused as e:
            return {"refused": str(e), "refused_at_gyr": t, "rows": rows, "n_steps": n}
        grad = lid.step(h, d_l=y[2], d_cr=y[3], t_l=t_l, h_m=h_m, h_cr=h_cr)
        if s.layer_grid is not None:
            try:
                s.layer_q = s.layer_grid.step(h, t_c=y[0], t_i=s.layer_t_i, h_d=s.basal.params["lambda_d"] * h_pm,
                                              t_now=t)
            except sm.Refused as e:
                return {"refused": str(e), "refused_at_gyr": t, "rows": rows, "n_steps": n}
    return {"rows": rows, "n_steps": n, "cap_myr": cap_myr, "h_min_myr": h_min / GYR_S * 1e3,
            "max_lambda_over_ceiling": worst,
            "guard_stage_hits": list(s.guard_stage_hits), "guard_iter_hits": list(s.guard_iter_hits),
            "fixed_point_limit_hits": list(s.fixed_point_limit_hits),
            "multi_root_evals": s.multi_root_evals, "root_jumps": list(s.root_jumps), "root_notes": list(s.root_notes),
            "path_checks": list(s.path_checks),
            "layer": None if s.layer_grid is None else {
                "describe": s.layer_grid.describe(), "margin": s.layer_grid.margin,
                "max_phi": max(s.layer_grid.phi) if s.layer_grid.latent is not None else None,
                "iterations_max": s.layer_grid.iterations_max, "source": s.basal.params.get("source"),
                "history": s.layer_grid.history}}
