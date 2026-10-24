# 고정 걸음 모드 — 옛 엔진의 격자(반지름 균일 dr, RK4, 걸음 안 온도 고정)로 한 층을 적분하고 질량 꼴 결과로 되돌림 (T2 적분법 항)
"""Fixed-step mode: one segment integrated on the old engine's discretisation, returned in the mass form.

Registration: rewrite/oracle/t2-method-term-registration.md (directing's H5 re-plan, owner-direction «the old engine's
ADAPTIVE path is broken for fe_prem cores»). It reproduces interior.py's fixed path at 097a8aa3 in three points:
- independent variable r, uniform |dr| (the caller's `dr`, = the old r_scale / STEPS);
- classical RK4 on (m, P, I, V_p) (stepper.step_rk4);
- T_ad and T held at their step-start value through the stages (the density reads the step-start T) and advanced
  after the step by (dT/dP)_ad(step start) · ΔP, i.e. Euler in P (interior.py `deriv(.., tt=None)` and
  `t + dtdp * dp`).
Events are landed exactly as in the adaptive mode (secant on re-steps of the same RK4 step); the grid restarts from a
landed event with the full dr. What it does not reproduce is listed in the registration.

The mass-form rhs f(m, y), y = (r, P, T_ad, T, I, V_p), is turned into the r-form z' = f / f[0] with
z = (m, P, T_ad, T, I, V_p); events g(m, y) are read at (z[0], (r, *z[1:])).
"""
from __future__ import annotations

import math

from solver import stepper as st

T_COMPONENTS = (2, 3)
P_COMPONENT = 1
# Secant re-steps per event in this mode. A full step (Earth: ~3.2 km, ~1e8 Pa) that crosses a seam has stages on both
# sides, so g(s) has kinks and the Illinois secant converges only linearly; 8 (the adaptive mode's, whose steps near
# a seam are short) chattered on Earth's 23.83 GPa seam at |g| 2.5e6 Pa. 64 halvings cover 1e8 Pa → 1e-12·scale.
EVENT_REWALKS = 64


def _y_of(r, z):
    return (r, *z[1:])


def _k_m(k):
    """dz/dr → dy/dm (k[0] = dm/dr)."""
    return (1.0 / k[0], *(c / k[0] for c in k[1:]))


class _RHook:
    """A coexistence hook (stepper.Event.coexist) seen in the r-form (note 4 S3): g and the segment's f wrapped through
    _y_of, as the events' g are; the token and records pass through unchanged."""

    def __init__(self, hook, f):
        self.hook, self.f = hook, f

    def enter(self, r, z):
        return self.hook.enter(z[0], _y_of(r, z))

    def rhs(self, tok, _fr):
        fm = self.hook.rhs(tok, self.f)

        def fr(r, z):
            k = fm(z[0], _y_of(r, z))
            if isinstance(k, st.Stop):
                return k
            if k[0] == 0.0:
                return st.Stop("refused", {"reason": "dr/dm = 0", "m": z[0], "r": r})
            return (1.0 / k[0], *(c / k[0] for c in k[1:]))
        return fr

    def exit_g(self, tok):
        g = self.hook.exit_g(tok)
        return lambda r, z: g(z[0], _y_of(r, z))

    def exit_scale(self, tok):
        return self.hook.exit_scale(tok)

    def row_events(self, tok):
        return [st.Event(ev.name, (lambda r, z, g=ev.g: g(z[0], _y_of(r, z))), ev.scale, ev.terminal, ev.seam,
                         ev.component) for ev in self.hook.row_events(tok)]

    def project(self, tok, z):
        return self.hook.project(tok, z)              # P, T_ad, T sit at the same indices in z as in y


def run_r(f, m0: float, y0: tuple, m_end: float, r_end: float, r_end_name: str, dr: float, events=(),
          on_accept=None, max_steps: int = 200000, event_min_progress: float = 0.0, event_restarts_step: int = 4,
          event_restarts_run: int = 2000, m_scale: float = 1.0) -> st.Result:
    """Integrate from (m0, y0) inward to r = r_end (reported as the terminal event `r_end_name`) or to m = m_end
    (reported as stop kind "end", as the mass-form run ends at its x1). Returns a stepper.Result in the mass form."""
    def fr(r, z):
        k = f(z[0], _y_of(r, z))
        if isinstance(k, st.Stop):
            return k
        if k[0] == 0.0:
            return st.Stop("refused", {"reason": "dr/dm = 0", "m": z[0], "r": r})
        return (1.0 / k[0], *(c / k[0] for c in k[1:]))

    evs = [st.Event(ev.name, (lambda r, z, g=ev.g: g(z[0], _y_of(r, z))), ev.scale, ev.terminal, ev.seam,
                     ev.component, None if ev.coexist is None else _RHook(ev.coexist, f))
           for ev in events]
    evs.append(st.Event("_m_end", lambda r, z: z[0] - m_end, scale=m_scale))
    opt = st.Options(rtol=1.0, floors=tuple(math.inf for _ in y0), h0=dr, h_min=0.0, h_max=dr, max_steps=max_steps,
                     event_min_progress=event_min_progress, event_restarts_step=event_restarts_step,
                     event_restarts_run=event_restarts_run, event_rewalks=EVENT_REWALKS, fixed=True, frozen=T_COMPONENTS,
                     frozen_ref=P_COMPONENT)
    acc = None if on_accept is None else (lambda r, z: on_accept(z[0], _y_of(r, z)))
    z0 = (m0, *y0[1:])
    res = st.run(fr, y0[0], z0, r_end, opt, evs, on_accept=acc)
    path = tuple((z[0], _y_of(r, z), _k_m(k)) for r, z, k in res.path)
    landed = tuple((name, z[0], _y_of(r, z)) for name, r, z in res.events)
    stop, event = res.stop, res.event
    if stop.kind == "end":
        stop, event = st.Stop("event"), r_end_name
    elif stop.kind == "event" and event == "_m_end":
        stop, event = st.Stop("end"), None
    return st.Result(res.y[0], _y_of(res.x, res.y), stop, event, res.h_last, path, landed, res.counters,
                     coexist=res.coexist)
