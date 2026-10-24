# ALE 열역사 방식(D2 재설계 메모 §7) — 덮개를 고정 마디 u 에서 격자 이동 항과 함께 IMEX ARS(2,2,2) 로 푸는 T2 옆의 새 방식; thermal_stack·samuel_run·fold_track 은 그대로
"""The ALE-formulated thermal-history mode of the D2 redesign note §7 (artifacts review2-fix-c8 c8c7472c, cleared by 68
and r2). A new mode beside T2 (`thermal_stack.run`): it calls T2's `state_terms` for the ODE rates and never changes
T2's, `samuel_run`'s or `fold_track`'s behaviour; the boundary-layer roots are tracked by `hop_track` (D), installed in
place of thermal_stack's `_continued` / `track_at` for the duration of `run` only.

Mode options (D2 note §7.5; `s.opt["ale_options"]` overrides the defaults in `ALE_DEFAULTS`, all on in this mode):
- `melt_rule` "exact": state_terms' melt integrals by `melt_exact` (splits at r_x and the solidus seam) through T2's
  `s.opt["melt_rule"]`, whose default "midpoint" keeps T2 byte-identical; set for the run only.
- `events`: the 13 event signs (`event_signs`: the stefan sign; T′(r_x) − T_sol and − T_sol,depleted; T′(r_s) −
  T_sol,high and − T_sol,low; each at T_m − 1, T_m, T_m + 1 K, T_b moved with T_m) are compared at a step's start and
  end; a change lands the step just past the first change (bisection of the step length to min(1e-9 Gyr, 1e-6 h)),
  and the run re-steps to that length.
- `ramp_cap`: a step starting inside a ramp (a family whose T_m + 1 and T_m − 1 signs differ) is capped at the run's
  nominal step cap / 8 (f4 order rounds 4 and 4b).
The options in force are returned as `manifest`.

State: (T_c, T_m, D_l, D_cr) explicit; the lid profile θ on fixed nodes u_j = j/(n−1), r = r_p − D_l (1 − u)
(u = 0 the base); the basal grid (plates with a layer) on its own fixed nodes.
- Lid: ∂T/∂t|_u = (L_{D_l} T + H)/ρc − Ḋ_l (1 − u)/D_l ∂T/∂u, L = LidGrid.step's operator at the stage's own D_l and
  D_cr, central ALE difference; Dirichlet T_l(T_m) at u = 0 and T_s at u = 1, at the stage's own state. No re-mesh.
- Basal grid: E(T)_t = L T + H with E = ρc T + ρ_d f L_m φ(T), φ linearised and iterated as LayerGrid (≤ MELT_MAX_ITER,
  else `Refused`), Dirichlet T_c and T_i at the stage's own state.
- IMEX ARS(2,2,2) (γ = 1 − 1/√2, stiffly accurate): explicit part = the ODE rates (T2's state_terms with the stage's
  own lid-base gradient and basal fluxes); implicit part = both grids.
- Ḋ_l in each implicit stage: ddl is affine in the lid-base gradient (samuel_model.lid_rate), ddl = a + b ∇T, with
  a, b from one state_terms at the stage; Ḋ solves g(Ḋ) = a + b ∇T(θ(Ḋ)) − Ḋ = 0 by the secant method to
  |g| ≤ DDOT_TOL·|Ḋ| (DDOT_ABS when Ḋ = 0) in ≤ DDOT_MAX_IT iterations; an unconverged stage raises `Lost` (the trial
  is rejected and halved, counted), never a silent cap.
- Base gradient: the 4-point one-sided stencil (−11, 18, −9, 2)/(6 Δr), fixed (§7.2).
- Cold start: T2's (D_l = 10 m, the lid started linear), no ramp, no minimum.
Counts kept per run in `STATS` (§7.2, §7.4): Ḋ rejects, worst accepted |g|/|Ḋ|, worst |ddl(stage) − Ḋ|/|Ḋ| at the
final stage evaluation, shortened steps (and those with t < 0.05 Gyr), guard trips, fold events, refusals."""
from __future__ import annotations

import copy
import math

import fold_track as ft
import hop_track as hp
import melt_exact
import samuel_layer as lay
import samuel_lid as sl
import samuel_model as sm
import thermal_stack as ts
from thermal_stack import GYR_S, D_L_0_M, D_CR_0_M, state_terms, _rates, _tau_s, _shell, lid_heat

G = 1.0 - 1.0 / math.sqrt(2.0)
DEL = 1.0 - 1.0 / (2.0 * G)
DDOT_TOL = 1e-12            # §7.2: |g| ≤ 1e-12 |Ḋ|
DDOT_ABS = 1e-30            # m/s, when Ḋ = 0
DDOT_MAX_IT = 12
COLD_GYR = 0.05             # §7.2 cold-start gate window
ALE_DEFAULTS = {"melt_rule": "exact", "events": True, "ramp_cap": True}     # §7.5
RAMP_DIVISOR = 8            # ramp cap = nominal step cap / 8 (order round 4b)
LAND_TOL_GYR = 1e-9
STATS: dict = {}


def reset_stats() -> None:
    STATS.clear()
    STATS.update(ddot_rejects=0, ddot_worst_rel=0.0, ddot_consistency_worst=0.0, shortened=0, shortened_cold=0,
                 accepted=0, melt_iter_max=0, landings=0, ramp_capped=0, landed_before_fold=0, landings_cold=0,
                 ramp_capped_cold=0)


def _radius_at(s, p_pa: float, r_top: float, r_bot: float) -> float | None:
    a, b = r_bot, r_top
    if not (s.melt_p(a) >= p_pa >= s.melt_p(b)):
        return None
    for _ in range(80):
        m = 0.5 * (a + b)
        if s.melt_p(m) >= p_pa:
            a = m
        else:
            b = m
    return 0.5 * (a + b)


def event_signs(s, y: list, t_gyr: float, c: float) -> tuple:
    """The 13 event signs at (y, t) (§7.5): stefan > 0, then per k = −1, 0, +1 K: T′(r_x) > T_sol(P_x),
    T′(r_x) > T_sol,depleted(P_x), T′(r_s) > T_sol,high(seam), T′(r_s) > T_sol,low(seam). A radius outside the
    convecting shell gives False for its pair. `c` is y's time fraction in the step (0 its start, 1 its end); the run
    state, STEP included, is restored around the evaluation."""
    snap = hp.snapshot(s)
    hp.STEP["c"] = c
    try:
        f = state_terms(s, *y, t_gyr, s._ale_state["grad"])
    finally:
        hp.restore(s, snap)
    r_top, r_bot = s.r_p - y[2] - f["delta_u"], s.r_base + f["delta_b"]
    cv = s.body["curves"]
    p_x = s.body["melt_extraction_below_pa"]
    rx, rs = _radius_at(s, p_x, r_top, r_bot), _radius_at(s, cv["seam_gpa"] * 1e9, r_top, r_bot)
    t_deep, t_shal, seam_hi, seam_lo = event_thresholds(s, y[3])
    out = [f["stefan"] > 0.0]
    for k in (-1.0, 0.0, 1.0):
        tm = y[1] + k
        tb = f["t_b"] * tm / y[1]

        def temp(r):
            return tb + (tm - tb) * (r - r_bot) / (r_top - r_bot)
        out += [rx is not None and temp(rx) > t_deep, rx is not None and temp(rx) > t_shal,
                rs is not None and temp(rs) > seam_hi, rs is not None and temp(rs) > seam_lo]
    return tuple(out)


def _land(s, step, y0: list, t: float, y_new: list, h_used: float, sg0: tuple) -> float:
    """§7.5 landing: if any event sign differs between the step's start and end, the step length is bisected to
    min(LAND_TOL_GYR, 1e-6 h) and the first change is landed just past (hi); returns the length to re-step to."""
    if event_signs(s, y_new, t + h_used / GYR_S, 1.0) == sg0:
        return h_used
    tol = min(LAND_TOL_GYR * GYR_S, 1e-6 * h_used)
    snap = hp.snapshot(s)
    lo, hi = 0.0, h_used
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        hp.restore(s, snap)
        hp.STEP["ratio"] = mid / hp.STEP["h_last"] if hp.STEP["h_last"] else 1.0
        try:
            y_mid = step(list(y0), t, mid)
        except ft.Lost as e:                          # 68: a loss inside the landing bisection is its own refusal
            hp.restore(s, snap)
            raise sm.Refused(f"a trial inside the event landing lost {e.equation} at t = {t + mid / GYR_S:.6f} Gyr") from e
        if event_signs(s, y_mid, t + mid / GYR_S, 1.0) == sg0:
            lo = mid
        else:
            hi = mid
    hp.restore(s, snap)
    STATS["landings"] += 1
    return hi


def event_thresholds(s, d_cr: float) -> tuple:
    """The solidus values the event pairs compare with, from melt_exact's own branch rule (r2 S2): at r_x the deep
    side (p > P_x: undepleted) and the shallow side (depleted), on the line of P_x's side of the seam; at r_s the high
    and the low line, each depleted when the seam is shallower than P_x."""
    cv, p_x = s.body["curves"], s.body["melt_extraction_below_pa"]
    kw = dict(d_cr=d_cr, d_ref=sm.crust_reference_thickness(s.r_p, s.r_c, s.body["crust_reference_fraction"]),
              delta_t_sol=s.body["delta_t_sol"], curves=cv)
    seam, px = cv["seam_gpa"], p_x / 1e9
    t_deep = melt_exact.solidus_branch(px, False, px > seam, **kw)
    t_shal = melt_exact.solidus_branch(px, True, px > seam, **kw)
    shallow_seam = seam * 1e9 < p_x
    return t_deep, t_shal, melt_exact.solidus_branch(seam, shallow_seam, True, **kw), \
        melt_exact.solidus_branch(seam, shallow_seam, False, **kw)


def in_ramp(signs: tuple) -> bool:
    """Between a family's T_m + 1 K and T_m − 1 K images: some pair's k = −1 and k = +1 signs differ."""
    lo, hi = signs[1:5], signs[9:13]
    return any(a != b for a, b in zip(lo, hi))


# ── lid on fixed u nodes ──────────────────────────────────────────────────────────────────────────────────
def lid_coeffs(lid, d_l: float, d_cr: float, h_m: float, h_cr: float):
    """LidGrid.step's operator on the mesh of thickness d_l: (Δr, ρc, H, w_lo, w_hi) per interior node."""
    n = lid.n
    r = [lid.r_p - d_l + i * d_l / (n - 1) for i in range(n)]
    dr = d_l / (n - 1)
    r_crust = lid.r_p - d_cr
    (rc_m, k_m), (rc_cr, k_cr) = lid.mantle, lid.crust

    def crust_len(lo, hi):
        return max(0.0, hi - max(lo, r_crust))
    rho, src, wl, wh = [0.0] * n, [0.0] * n, [0.0] * n, [0.0] * n
    for i in range(1, n - 1):
        ri = r[i]
        rm, rp = ri - dr / 2, ri + dr / 2
        f_cr = crust_len(rm, rp) / dr
        rho[i] = f_cr * rc_cr + (1 - f_cr) * rc_m
        src[i] = f_cr * h_cr + (1 - f_cr) * h_m
        l_lo, l_hi = crust_len(r[i - 1], ri), crust_len(ri, r[i + 1])
        k_lo = dr / (l_lo / k_cr + (dr - l_lo) / k_m)
        k_hi = dr / (l_hi / k_cr + (dr - l_hi) / k_m)
        wl[i] = rm * rm * k_lo / (ri * ri * dr * dr)
        wh[i] = rp * rp * k_hi / (ri * ri * dr * dr)
    return dr, rho, src, wl, wh


def base_gradient(th: list, dr: float) -> float:
    """∂T/∂r at the lid base, the 4-point one-sided stencil (§7.2, fixed)."""
    return (-11.0 * th[0] + 18.0 * th[1] - 9.0 * th[2] + 2.0 * th[3]) / (6.0 * dr)


def _bc_src(s, y: list, t_gyr: float):
    t_l = sm.lid_base_temperature(y[1], s.e_star, s.opt["a_rh"], s.opt["r_gas"])
    v_sil, v_cr = _shell(s.r_p, s.r_c), _shell(s.r_p, s.r_p - y[3])
    h_pm = sm.primitive_heat((s.body["age_gyr"] - t_gyr) * 1000.0, s.mantle.params["rho"], s.body["concentration"])
    h_m, h_cr = lid_heat(s, h_pm, v_sil, v_cr)
    return t_l, h_m, h_cr, h_pm


def _lid_solve(lid, rhs: list, alpha: float, y: list, co, t_l: float, ddot: float) -> list:
    """θ − α F_I(θ) = rhs at the interior, F_I = (L θ + H)/ρc − Ḋ (1 − u)/D_l ∂θ/∂u; Dirichlet t_l, T_s."""
    n = lid.n
    dr, rho, src, wl, wh = co
    du = 1.0 / (n - 1)
    a, b, c, d = [0.0] * n, [0.0] * n, [0.0] * n, [0.0] * n
    b[0], d[0] = 1.0, t_l
    b[-1], d[-1] = 1.0, lid.t_s
    for i in range(1, n - 1):
        adv = (-ddot * (1.0 - i * du) / y[2]) / (2.0 * du)
        a[i] = -alpha * (wl[i] / rho[i] - adv)
        b[i] = 1.0 + alpha * (wl[i] + wh[i]) / rho[i]
        c[i] = -alpha * (wh[i] / rho[i] + adv)
        d[i] = rhs[i] + alpha * src[i] / rho[i]
    return sl._solve_tridiagonal(a, b, c, d)


def _lid_fimp(lid, th: list, y: list, co, ddot: float) -> list:
    n = lid.n
    dr, rho, src, wl, wh = co
    du = 1.0 / (n - 1)
    out = [0.0] * n
    for i in range(1, n - 1):
        out[i] = ((wl[i] * th[i - 1] - (wl[i] + wh[i]) * th[i] + wh[i] * th[i + 1] + src[i]) / rho[i]
                  - ddot * (1.0 - i * du) / y[2] * (th[i + 1] - th[i - 1]) / (2.0 * du))
    return out


def _lid_stage(s, lid, rhs: list, alpha: float, y: list, t_gyr: float, f_pre: dict):
    """The implicit lid stage with Ḋ_l converged: (θ, Ḋ, |g|/|Ḋ|). Raises Lost when the secant does not converge."""
    t_l, h_m, h_cr, _ = _bc_src(s, y, t_gyr)
    co = lid_coeffs(lid, y[2], y[3], h_m, h_cr)
    dr = co[0]
    if s.lid.params["fixed_m"] is not None:
        th = _lid_solve(lid, rhs, alpha, y, co, t_l, 0.0)
        return th, 0.0, 0.0, co
    m = s.mantle.params
    bcoef = -m["k"] / (m["rho"] * m["cp"] * (y[1] - t_l))
    acoef = f_pre["ddl"] - bcoef * f_pre["lid_gradient"]

    def g(dd):
        th_ = _lid_solve(lid, rhs, alpha, y, co, t_l, dd)
        return acoef + bcoef * base_gradient(th_, dr) - dd, th_
    d0 = f_pre["ddl"]
    g0, th0 = g(d0)
    d1 = d0 + (abs(d0) * 1e-6 if d0 else 1e-20)
    g1, th1 = g(d1)
    for _ in range(DDOT_MAX_IT):
        if abs(g1) <= max(DDOT_TOL * abs(d1), DDOT_ABS):
            rel = abs(g1) / abs(d1) if d1 else 0.0
            STATS["ddot_worst_rel"] = max(STATS["ddot_worst_rel"], rel)
            return th1, d1, rel, co
        if g1 == g0:
            break
        d0, g0, (d1) = d1, g1, d1 - g1 * (d1 - d0) / (g1 - g0)
        g1, th1 = g(d1)
    STATS["ddot_rejects"] += 1
    raise ft.Lost("Ḋ_l", False)


# ── basal grid (fixed domain) ─────────────────────────────────────────────────────────────────────────────
def _basal_energy(lg, t: list, phi) -> list:
    return [lg.rho_c[i] * t[i] + (lg.rho_d * lg.f[i] * lg.latent * phi[i] if lg.latent is not None else 0.0)
            for i in range(lg.n)]


def _basal_phi(lg, t: list):
    return [sm.melt_fraction(x, a, b) for x, a, b in zip(t, lg.t_sol, lg.t_liq)] if lg.latent is not None else None


def _basal_lap(lg, t: list) -> list:
    dr, k = lg.dr, lg.k
    out = [0.0] * lg.n
    for i in range(1, lg.n - 1):
        ri = lg.r[i]
        rm, rp = ri - dr / 2, ri + dr / 2
        out[i] = (rm * rm * k * (t[i - 1] - t[i]) + rp * rp * k * (t[i + 1] - t[i])) / (ri * ri * dr * dr)
    return out


def _basal_solve(lg, rhs_e: list, alpha: float, t_c: float, t_i: float, t_start: list) -> list:
    """E(T) − α L T = rhs_e at the interior (Dirichlet t_c, t_i), φ linearised about the last iterate (LayerGrid's)."""
    n, dr, k = lg.n, lg.dr, lg.k
    wl, wh = [0.0] * n, [0.0] * n
    for i in range(1, n - 1):
        ri = lg.r[i]
        rm, rp = ri - dr / 2, ri + dr / 2
        wl[i] = rm * rm * k / (ri * ri * dr * dr)
        wh[i] = rp * rp * k / (ri * ri * dr * dr)

    def solve(lin):
        a, b, c, d = [0.0] * n, [0.0] * n, [0.0] * n, [0.0] * n
        b[0], d[0] = 1.0, t_c
        b[-1], d[-1] = 1.0, t_i
        for i in range(1, n - 1):
            a[i], b[i], c[i] = -alpha * wl[i], lg.rho_c[i] + alpha * (wl[i] + wh[i]), -alpha * wh[i]
            d[i] = rhs_e[i]
            if lin is not None:
                rl = lg.rho_d * lg.f[i] * lg.latent
                b[i] += rl * lin[i][0]
                d[i] -= rl * lin[i][1]
        return lay._solve_tridiagonal(a, b, c, d)
    if lg.latent is None:
        return solve(None)
    t_k = t_start[:]
    change = math.inf
    for it in range(1, lay.MELT_MAX_ITER + 1):
        lin = []
        for i in range(n):
            lo, hi = lg.t_sol[i], lg.t_liq[i]
            slope = 1.0 / (hi - lo) if lo < t_k[i] < hi else 0.0
            lin.append((slope, sm.melt_fraction(t_k[i], lo, hi) - slope * t_k[i]))
        t_new = solve(lin)
        change = max(abs(x - y) for x, y in zip(t_new, t_k))
        t_k = t_new
        if change < lay.MELT_TOL_K:
            STATS["melt_iter_max"] = max(STATS["melt_iter_max"], it)
            return t_k
    raise sm.Refused(f"ALE basal stage did not converge in {lay.MELT_MAX_ITER} iterations ({change:.3e} K)")


def _basal_fluxes(lg, t: list) -> tuple:
    dr, k = lg.dr, lg.k
    g_c = (-3.0 * t[0] + 4.0 * t[1] - t[2]) / (2.0 * dr)
    g_d = (3.0 * t[-1] - 4.0 * t[-2] + t[-3]) / (2.0 * dr)
    return -k * g_c, -k * g_d


# ── one ARS(2,2,2) step ───────────────────────────────────────────────────────────────────────────────────
def _step(s, lid, th0: list, tb0, y0: list, t0: float, hh: float, k1: list):
    """(y1, θ1, T_b1 or None, ∇1, q_layer1). Stage 1 is (y0, θ0, T_b0) with k1 its rates."""
    dt = hh / GYR_S
    lg = s.layer_grid
    lam_d = s.basal.params["lambda_d"] if s.basal is not None else None
    a2 = hh * G
    # stage 2
    y2 = [a + hh * G * b for a, b in zip(y0, k1)]
    t2 = t0 + G * dt
    hp.STEP["c"] = G                                           # f3: the guard's prediction at this stage's time
    f_pre2 = state_terms(s, *y2, t2, s._ale_state["grad"])     # sets layer_t_i at y2; a, b of ddl
    tb2 = None
    if lg is not None:
        h_pm2 = _bc_src(s, y2, t2)[3]
        hsrc2 = [lam_d * h_pm2 * lg.f[i] for i in range(lg.n)]
        e0 = _basal_energy(lg, tb0, _basal_phi(lg, tb0) or [0.0] * lg.n)
        rhs = [e0[i] + a2 * hsrc2[i] for i in range(lg.n)]
        tb2 = _basal_solve(lg, rhs, a2, y2[0], s.layer_t_i, tb0)
        s.layer_q = _basal_fluxes(lg, tb2)
    th2, dd2, _, co2 = _lid_stage(s, lid, th0, a2, y2, t2, f_pre2)
    f2 = state_terms(s, *y2, t2, base_gradient(th2, co2[0]))
    _consistency(f2, dd2)
    k2 = _rates(f2)
    fi2 = _lid_fimp(lid, th2, y2, co2, dd2)
    # stage 3
    y3 = [a + hh * (DEL * b + (1 - DEL) * c) for a, b, c in zip(y0, k1, k2)]
    t3 = t0 + dt
    hp.STEP["c"] = 1.0
    f_pre3 = state_terms(s, *y3, t3, base_gradient(th2, co2[0]))
    tb3 = None
    if lg is not None:
        h_pm3 = _bc_src(s, y3, t3)[3]
        hsrc3 = [lam_d * h_pm3 * lg.f[i] for i in range(lg.n)]
        lap2 = _basal_lap(lg, tb2)
        e0 = _basal_energy(lg, tb0, _basal_phi(lg, tb0) or [0.0] * lg.n)
        rhs = [e0[i] + hh * (1 - G) * (lap2[i] + hsrc2[i]) + a2 * hsrc3[i] for i in range(lg.n)]
        tb3 = _basal_solve(lg, rhs, a2, y3[0], s.layer_t_i, tb2)
        s.layer_q = _basal_fluxes(lg, tb3)
    rhs3 = [th0[i] + hh * (1 - G) * fi2[i] for i in range(lid.n)]
    th3, dd3, _, co3 = _lid_stage(s, lid, rhs3, a2, y3, t3, f_pre3)
    g3 = base_gradient(th3, co3[0])
    f3 = state_terms(s, *y3, t3, g3)                          # the end state keeps the roots (C145) and its rates
    _consistency(f3, dd3)
    return y3, th3, tb3, g3, s.layer_q


def _consistency(f: dict, ddot: float) -> None:
    if ddot:
        STATS["ddot_consistency_worst"] = max(STATS["ddot_consistency_worst"], abs(f["ddl"] - ddot) / abs(ddot))


def run(s, cap_myr: float) -> dict:
    """The ALE mode over the stack's history. Same row fields as thermal_stack.run's core set, plus `manifest`."""
    opts = dict(ALE_DEFAULTS, **s.opt.get("ale_options", {}))
    had_rule, old_rule = "melt_rule" in s.opt, s.opt.get("melt_rule")
    s.opt["melt_rule"] = opts["melt_rule"]
    try:
        out = _run(s, cap_myr, opts)
    finally:
        if had_rule:
            s.opt["melt_rule"] = old_rule
        else:
            del s.opt["melt_rule"]
    out["manifest"] = {"mode": "ALE", "cap_myr": cap_myr, "step_fraction": ts.STEP_FRACTION, **opts,
                       "ramp_divisor": RAMP_DIVISOR, "land_tol_gyr": LAND_TOL_GYR}
    return out


def _run(s, cap_myr: float, opts: dict) -> dict:
    reset_stats()
    t0 = s.body["t_initial_gyr"]
    cap = cap_myr * 1e-3 * GYR_S
    fixed = s.lid.params["fixed_m"]
    y = [s.core.params["t0"], s.mantle.params["t0"], D_L_0_M if fixed is None else fixed, D_CR_0_M]
    lid = sl.LidGrid(s.lid.params["nodes"], r_p=s.r_p, t_s=s.body["t_surface"], rho_m=s.mantle.params["rho"],
                     c_m=s.mantle.params["cp"], k_m=s.mantle.params["k"], rho_cr=s.lid.params["rho_crust"],
                     c_cr=s.lid.params["cp_crust"], k_cr=s.lid.params["k_crust"])
    t_l0 = sm.lid_base_temperature(y[1], s.e_star, s.opt["a_rh"], s.opt["r_gas"])
    lid.start(y[2], t_l0)
    grad = (s.body["t_surface"] - t_l0) / y[2]
    #: the ALE stage state a trial reads and a rollback restores (hop_track.snapshot): lid θ, basal T, lid gradient
    s._ale_state = {"th": lid.t[:], "tb": None, "grad": grad}
    rows = []
    s._rows = rows
    t, n, h_min = t0, 0, None
    moved = False                                     # r2 aa2b6ec6: s.track's roots are from the previous accepted state
    refused = None

    def refuse(e):
        return {"refused": str(e), "refused_at_gyr": t, "rows": rows, "n_steps": n, "stats": dict(STATS),
                "hop_stats": {k: v for k, v in hp.STATS.items() if k != "guard_log"}}
    hp.reset_stats()
    with hp.install():
        hp.STEP["ale"] = True                         # 68 (l.141): continuations predict at the stage's time fraction
        while True:
            hp.STEP["c"] = 1.0 if moved else 0.0     # r2 aa2b6ec6: a full step from s.track's state; 0 where the track is y's own
            try:
                f1 = state_terms(s, *y, t, grad, mode="accept")
            except sm.Refused as e:
                return refuse(e)
            rows.append({"t": t, "t_c": y[0], "t_m": y[1], "d_l": y[2], "d_cr": y[3], "delta_u": f1["delta_u"],
                         "delta_b": f1["delta_b"], "lid_gradient": grad})
            remaining = (s.body["age_gyr"] - t) * GYR_S
            if remaining <= 1e-9 * GYR_S:
                break
            h = min(cap, ts.STEP_FRACTION * _tau_s(y, f1), remaining)
            k1 = _rates(f1)
            if s.layer_grid is not None and s._ale_state["tb"] is None:
                s._ale_state["tb"] = s.layer_grid.t[:]          # the basal grid starts inside the first state_terms
            y0 = y[:]
            out = {}

            def step(yy, tt, hh):
                st0 = s._ale_state
                y1, th1, tb1, g1, q1 = _step(s, lid, st0["th"][:], None if st0["tb"] is None else st0["tb"][:],
                                             yy, tt, hh, k1)
                out.update(th=th1, tb=tb1, g=g1, q=q1)
                return y1
            tracked = s.track is not None and s.opt["root_branch"] == "nearest"
            try:
                if tracked:
                    snap = hp.snapshot(s)
                    h_try, sg0 = h, None
                    if opts["events"]:
                        sg0 = event_signs(s, y0, t, 0.0)
                        if opts["ramp_cap"] and in_ramp(sg0) and h > cap / RAMP_DIVISOR:
                            h_try = cap / RAMP_DIVISOR           # §7.5: a step starting inside a ramp
                            STATS["ramp_capped"] += 1
                    y_new, h_used, ev = hp.advance(step, y0, t, h_try, GYR_S, s)
                    h_adv = h_used                               # advance's own length: Lost halving or a fold
                    if opts["events"] and h_used > 0.0:
                        ratio_in = hp.STEP["ratio"]               # the check predicts at h_used; the re-step sets its own
                        hp.STEP["ratio"] = h_used / hp.STEP["h_last"] if hp.STEP["h_last"] else 1.0
                        h_land = _land(s, step, y0, t, y_new, h_used, sg0)
                        hp.STEP["ratio"] = ratio_in
                        if h_land < h_used:
                            h_used = h_land
                            if ev is not None:                   # 68: an event before the fold in the same step is
                                STATS["landed_before_fold"] += 1  # landed; the next step meets the fold again
                                ev = None
                    if (ev is not None or h_used != h_try) and h_used > 0.0:
                        hp.restore(s, snap)
                        hp.STEP["ratio"] = h_used / hp.STEP["h_last"] if hp.STEP["h_last"] else 1.0
                        y_new = step(y0, t, h_used)
                else:
                    y_new, h_used, ev = step(y0, t, h), h, None
            except sm.Refused as e:
                return refuse(e)
            except ft.Lost as e:
                return refuse(f"the adopted root of {e.equation} left its bracket and halving gave up at t = {t:.6f} Gyr")
            if tracked and h_adv != h_try or not tracked and h_used != h:
                STATS["shortened"] += 1                  # 68 G1 / r2 S1: Lost halving and folds only (§7.2's gate)
                if t - t0 < COLD_GYR:
                    STATS["shortened_cold"] += 1
            if t - t0 < COLD_GYR and tracked:
                STATS["landings_cold"] += h_used < h_adv
                STATS["ramp_capped_cold"] += h_try < h
            if h_used == 0.0:
                try:
                    hp.switch_branch(s, y, t, ev, c=0.0)    # y is the step start, where s.track is
                except sm.Refused as e:
                    return refuse(e)
                except ft.Lost as e:                 # r2 h1: a loss inside the branch switch is a named refusal
                    return refuse(f"the branch switch after the {ev.equation} fold lost {e.equation} at t = {t:.6f} Gyr")
                rows.pop()
                moved = False                        # switch_branch rebuilt the track at y
                continue
            h = h_used
            hp.STEP["h_last"] = h
            h_min = h if h_min is None else min(h_min, h)
            y, grad = y_new, out["g"]
            s._ale_state = {"th": out["th"], "tb": out["tb"], "grad": grad}
            if s.layer_grid is not None:
                lg = s.layer_grid
                lg.t = out["tb"][:]
                lg.phi = _basal_phi(lg, lg.t)
                s.layer_q = out["q"]
                if lg.latent is not None:
                    lg._track_margin(t + h / GYR_S)
            t = s.body["age_gyr"] if h == remaining else t + h / GYR_S
            n += 1
            STATS["accepted"] += 1
            moved = True
            if ev is not None:
                try:
                    hp.switch_branch(s, y, t, ev, c=1.0)    # 68 F1: y is the step end, s.track still the step start
                except sm.Refused as e:
                    return refuse(e)
                except ft.Lost as e:                 # r2 h1: a loss inside the branch switch is a named refusal
                    return refuse(f"the branch switch after the {ev.equation} fold lost {e.equation} at t = {t:.6f} Gyr")
                moved = False                        # switch_branch rebuilt the track at y
    return {"rows": rows, "n_steps": n, "cap_myr": cap_myr, "h_min_myr": h_min / GYR_S * 1e3, "stats": dict(STATS),
            "hop_stats": {k: v for k, v in hp.STATS.items() if k != "guard_log"},
            "fold_events": list(s.fold_events), "fold_rejected": list(s.fold_rejected)}
