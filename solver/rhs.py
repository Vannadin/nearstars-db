# 질량 꼴 구조 방정식과 한 층 안쪽 적분 · 중심 잔차 (phase-1 설계 §A1.1 · §A1.2 · §A1.5)
"""Hydrostatic structure in mass form, one inward pass through one material, and the centre residual.

Frozen design: rewrite/phase1-design.frozen.md §A1.1 (equations), §A1.2 (surface start), §A1.5 (residual).
Registration: rewrite/phase1-a1-impl.frozen.md, step S2. The multi-layer pass is solve.py's (S7).

State y = (r, P, T_ad, T, I, V_p); independent variable m, running inward from M; I accumulates (2/3) r² dm and
V_p the pore volume (dV_p/dm = −φ dV/dm, growing inward from 0, r2 on 973b89ef), both quadratures kept out of the error norm.
    dr/dm = 1 / (4π r² ρ)
    dP/dm = −G m / (4π r⁴)
    dT_ad/dm = (dT/dP)_ad · dP/dm          (dT/dP)_ad from the material view, not from a formula here
    dT/dm = dT_ad/dm                        (adiabatic layers; the conductive lid is lid.py's)
    dI/dm = −(2/3) r²                       (I grows inward from 0 at the surface; the shell's moment, for C/MR²)

A material view is any object with
    state(P, T, guess_rho) -> (rho, dTdP_ad[, notes]) | stepper.Stop      (only the first two are read here)
and, only where ρ(P_s) → 0 (a polytrope), surface_shell(P_start, g_surface, R) -> (shell_mass, depth): the mass
and depth of the spherical shell above the start pressure, from the material's own near-surface series (§A1.2).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from solver import stepper as st

G = 6.67430e-11          # the old engine's constant (interior.py:79)
FOUR_PI = 4.0 * math.pi


def make_rhs(view):
    """dy/dm for one adiabatic material. Returns a Stop from the view unchanged (a refusal at that state)."""
    def f(m: float, y: tuple):
        r, p, t_ad, t = y[:4]
        if r <= 0.0:
            return st.Stop("centre_crossed", {"m": m, "r": r})
        got = view.state(p, t_ad, None)
        if isinstance(got, st.Stop):
            return got
        rho, dtdp = got[0], got[1]
        drdm = 1.0 / (FOUR_PI * r * r * rho)
        dpdm = -G * m / (FOUR_PI * r ** 4)
        dtdm = dtdp * dpdm
        por = view.porosity(p) if hasattr(view, "porosity") else 0.0
        return (drdm, dpdm, dtdm, dtdm, -2.0 / 3.0 * r * r, -por * drdm * FOUR_PI * r * r)
    return f


@dataclass(frozen=True)
class PassOptions:
    rtol: float = 1e-10
    eps: float = 1e-6                 # the pass ends at m_ε = ε·M
    r_floor_frac: float = 1e-3        # terminal event r = r_floor_frac · r_scale (see `residual`)
    max_steps: int = 200000           # MAX_STEPS_SOLVE (per pass; fixed by the S2 dated line)
    event_min_progress: float = 1e-9  # × M (registration §6)
    event_restarts_step: int = 4
    event_restarts_run: int = 2000
    fixed_dr: float = 0.0             # m; > 0: fixed_grid.run_r (T2 method-term registration)


@dataclass(frozen=True)
class PassResult:
    m: float
    y: tuple
    rho_end: float
    F: float | None                   # centre residual, None when the pass stopped early
    stop: st.Stop
    r_scale: float
    path: tuple
    counters: st.Counters
    events: tuple = ()


def floors(mass: float, r_scale: float) -> tuple:
    """Error-scale floors of (r, P, T_ad, T, I) (registration note 2 item 9). I's floor is infinite: the moment of
    inertia is a quadrature carried along, kept **out** of the step-size error norm, so adding it moves no step
    (r2 S4-fix: with it inside, 302 vs 303 steps)."""
    return (1e-12 * r_scale, 1e5, 10.0, 10.0, math.inf, math.inf)


def r_scale_of(mass: float, rho_mean: float) -> float:
    return (3.0 * mass / (FOUR_PI * rho_mean)) ** (1.0 / 3.0)


def residual(m: float, r: float, rho: float, r_scale: float) -> float:
    """F = [r³ − 3m/(4πρ)] / r_scale³ at the pass's end point (design §A1.5, one definition).
    At m_ε it is the constant-density centre series; at the r-floor event it is the (negative) leftover mass.
    Both ends use the same expression, so F is continuous where the end point switches."""
    return (r ** 3 - 3.0 * m / (FOUR_PI * rho)) / r_scale ** 3


def surface_start(view, mass: float, radius: float, p_s: float, t_pot: float):
    """(m0, r0, P0) at which the integration starts. Normally (M, R, P_s). A view with `surface_shell` (ρ(P_s) = 0)
    starts below a thin analytic shell: m0 = M − shell_mass, r0 = R − depth."""
    shell = getattr(view, "surface_shell", None)
    if shell is None:
        return mass, radius, p_s
    dm, depth = shell(p_s, G * mass / radius ** 2, radius)
    return mass - dm, radius - depth, p_s


def inward_pass(view, mass: float, radius: float, p_s: float, t_pot: float, rho_mean: float,
                opt: PassOptions = PassOptions(), events=(), on_accept=None) -> PassResult:
    """One single-material pass from the surface to the centre end, with the centre residual."""
    rs = r_scale_of(mass, rho_mean)
    m0, r0, p0 = surface_start(view, mass, radius, p_s, t_pot)
    m_end = opt.eps * mass
    f = make_rhs(view)
    sopt = st.Options(rtol=opt.rtol, floors=floors(mass, rs), h0=1e-3 * mass,
                      h_min=1e-15 * mass, h_max=mass / 20.0, max_steps=opt.max_steps,
                      event_min_progress=opt.event_min_progress * mass,
                      event_restarts_step=opt.event_restarts_step, event_restarts_run=opt.event_restarts_run)
    floor_ev = st.Event("r_floor", lambda m, y: y[0] - opt.r_floor_frac * rs, scale=rs)
    res = st.run(f, m0, (r0, p0, t_pot, t_pot, 0.0, 0.0), m_end, sopt, [floor_ev, *events], on_accept=on_accept)
    if res.stop.kind not in ("end", "event"):
        return PassResult(res.x, res.y, float("nan"), None, res.stop, rs, res.path, res.counters, res.events)
    got = view.state(res.y[1], res.y[2], None)
    if isinstance(got, st.Stop):
        return PassResult(res.x, res.y, float("nan"), None, st.Stop("refused", got), rs, res.path, res.counters,
                          res.events)
    rho = got[0]
    return PassResult(res.x, res.y, rho, residual(res.x, res.y[0], rho, rs), res.stop, rs, res.path, res.counters,
                      res.events)
