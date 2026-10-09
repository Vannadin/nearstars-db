# 전도 덮개(암석권) — 표면에서 깊이 d 까지 T = A/r + B, 단열선은 그 밑에서 이어짐, 바닥 온도의 작은 고정점 (설계 §A1.4)
"""The conductive lid and its small fixed point.

Frozen design: rewrite/phase1-design.frozen.md §A1.4 (R-LITHO-2/-3/-4); registration rewrite/phase1-a1-impl.frozen.md S6.

Inside a layer of thermal kind `conductive`, from r = R down to r_b = R − d:
    T(r) = A/r + B,   T(R) = T_s,   T(r_b) = T_b
The density is read at that local T; the adiabat T_ad keeps stepping on the same P(m) (R-LITHO-4: «the adiabat,
continued to the surface, would reach T_pot»), so T_ad starts at T_pot at the surface.
T_b must equal T_ad(r_b), which depends on the lid's own density. Fixed point inside one trial:
    T_b⁰ = T_ad(r_b) from the lid integrated adiabatically; T_b^{k+1} = T_ad(r_b) with the profile through T_b^k;
    stop when |ΔT_b| ≤ lid_t_tol·T_b, at most lid_iters iterations, else Stop("lid_unconverged", trail).
State y = (r, P, T_ad, T); dT/dm = −(A/r²)·dr/dm inside the lid.
"""
from __future__ import annotations

from dataclasses import dataclass

from solver import rhs
from solver import stepper as st


@dataclass(frozen=True)
class LidResult:
    m: float
    y: tuple                     # the base state, T = T_b = T_ad (continuous into the adiabatic layer below)
    t_b: float
    a: float
    b: float
    trail: tuple                 # T_b iterates
    path: tuple
    counters: st.Counters


def _lid_rhs(view, a: float | None, b: float | None):
    """a, b None: adiabatic (the T_b⁰ pass)."""
    def f(m, y):
        r, p, t_ad, t = y
        if r <= 0.0:
            return st.Stop("centre_crossed", {"m": m, "r": r})
        t_loc = t_ad if a is None else a / r + b
        got = view.state(p, t_loc, None)
        if isinstance(got, st.Stop):
            return got
        rho = got[0]
        g = view.state(p, t_ad, None) if a is not None else got
        if isinstance(g, st.Stop):
            return g
        dtdp_ad = g[1]
        drdm = 1.0 / (rhs.FOUR_PI * r * r * rho)
        dpdm = -rhs.G * m / (rhs.FOUR_PI * r ** 4)
        dtad = dtdp_ad * dpdm
        dt = dtad if a is None else -a / (r * r) * drdm
        return (drdm, dpdm, dtad, dt)
    return f


def _coeffs(radius: float, r_b: float, t_s: float, t_b: float):
    a = (t_s - t_b) / (1.0 / radius - 1.0 / r_b)
    return a, t_s - a / radius


def lid_pass(view, mass: float, radius: float, depth: float, p_s: float, t_s: float, t_pot: float,
             r_scale: float, opt: rhs.PassOptions = rhs.PassOptions(), lid_iters: int = 8,
             lid_t_tol: float = 1e-9, t_b_seed: float | None = None):
    """Integrate the lid from the surface to its base. Returns a LidResult, or a Stop: the pass's own stop, or
    Stop("lid_unconverged", {"trail", "iters", "tol"}). `t_b_seed` replaces T_b⁰ (a test control)."""
    r_b = radius - depth
    sopt = st.Options(rtol=opt.rtol, floors=(1e-12 * r_scale, 1e5, 10.0, 10.0), h0=1e-3 * mass,
                      h_min=1e-15 * mass, h_max=mass / 20.0, max_steps=opt.max_steps,
                      event_min_progress=opt.event_min_progress * mass,
                      event_restarts_step=opt.event_restarts_step, event_restarts_run=opt.event_restarts_run)
    base = st.Event("lid_base", lambda m, y: y[0] - r_b, scale=r_scale)

    def run(a, b):
        t0 = t_pot if a is None else t_s
        res = st.run(_lid_rhs(view, a, b), mass, (radius, p_s, t_pot, t0), 0.0, sopt, [base])
        if res.stop.kind != "event":
            return res.stop if res.stop.kind != "end" else st.Stop("lid_base_not_reached", {"m": res.x})
        return res

    first = run(None, None)
    if isinstance(first, st.Stop):
        return first
    t_b = first.y[2] if t_b_seed is None else t_b_seed
    trail = [t_b]
    for _ in range(lid_iters):
        a, b = _coeffs(radius, r_b, t_s, t_b)
        res = run(a, b)
        if isinstance(res, st.Stop):
            return res
        t_new = res.y[2]
        trail.append(t_new)
        if abs(t_new - t_b) <= lid_t_tol * abs(t_new):
            a, b = _coeffs(radius, r_b, t_s, t_new)
            r, p, t_ad, _t = res.y
            return LidResult(res.x, (r, p, t_ad, t_new), t_new, a, b, tuple(trail), res.path, res.counters)
        t_b = t_new
    return st.Stop("lid_unconverged", {"trail": tuple(trail), "iters": lid_iters, "tol": lid_t_tol})
