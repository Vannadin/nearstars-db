# 층 안 사건 — 상 경계 · 열 세트 이음매 · 암모니아 표 격자 · 시작 곡선(고상선, 물/얼음) 착지와 스침 감시 (설계 §A1.3)
"""Events inside a layer and the graze monitor.

Frozen design: rewrite/phase1-design.frozen.md §A1.3; registration rewrite/phase1-a1-impl.frozen.md S5.

Events are `stepper.Event`s on the state y = (r, P, T_ad, T), non-terminal: the stepper lands on each and restarts
on the new side, so no stage of a step straddles a discontinuity of the integrand.
- pressure seams: every finite phase boundary and thermal-set seam of the material (`eos.Material.stencil_bounds`'s
  set, R-C157-4/-5); mixtures take the union over their parts; the water ladder `h2o` is excluded as in the old
  engine (`interior.PHASE_CUT_EXCLUDED`; its phase follows (P, T) through the onset curves);
- ammonia table grid (R-C157-5's nh3 kinks, now located): the isotherm nodes T = T_k of `ammonia_table.T_K`;
- onset curves (R-C157-11): g = T − T_onset(P) of the nearest curve the material reports (silicate solidus, water
  fluid/ice). The liquidus is not an event (withdrawn in R-C157-11).
The graze monitor follows R-C157-10..12's node rule: at accepted nodes, a local extremum of g = T − T_onset with
|g| ≤ GRAZE_K and no sign change is a graze; the closest one is kept as a typed record.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from solver import stepper as st

GRAZE_K = 1.0                      # K, as interior.GRAZE_K at 097a8aa3
GRAZE_SLOPE = 10.0                 # the membership threshold on S, as interior.GRAZE_SLOPE


def _material_seams(mat, excluded=("h2o",)) -> set:
    out = set()
    if getattr(mat, "name", None) in excluded:
        return out
    parts = getattr(mat, "parts", None)
    if parts is not None:
        for m, w in parts:
            if w > 0.0:
                out |= _material_seams(m, excluded)
        return out
    for ph in getattr(mat, "phases", ()) or ():
        for b in (ph.p_min, ph.p_max, *(x for ts in (ph.gamma_sets or ()) for x in (ts.p_min, ts.p_max))):
            if 0.0 < b < math.inf:
                out.add(float(b))
    return out


def _has_ammonia(mat) -> bool:
    if type(mat).__name__ == "Ammonia":
        return True
    return any(w > 0.0 and _has_ammonia(m) for m, w in (getattr(mat, "parts", None) or ()))


def seam_events(mat) -> list:
    return [st.Event(f"seam:{p_b:.9g}", (lambda m, y, p_b=p_b: y[1] - p_b), scale=p_b, terminal=False)
            for p_b in sorted(_material_seams(mat))]


def ammonia_events(mat) -> list:
    if not _has_ammonia(mat):
        return []
    from solver.legacy_materials import ammonia_isotherms
    return [st.Event(f"nh3_isotherm:{t_k:g}", (lambda m, y, t_k=t_k: y[3] - t_k), scale=t_k, terminal=False)
            for t_k in ammonia_isotherms()]


def nearest_onset(mat, p: float, t: float):
    """(name, g = T − T_onset) of the nearest onset curve at (P, T), or None."""
    oc = getattr(mat, "onset_curves", None)
    if oc is None or t <= 0.0:
        return None
    try:
        curves = oc(p if p > 0.0 else 1.0e5, t)        # the surface start (P = 0) is read at 1 bar, as dT/dP is
    except Exception as exc:                     # a material domain edge: no curve read here (the density path
        if type(exc).__name__ in ("PhaseGap", "SpinodalGap"):   # refuses by name at the same state)
            return None
        raise
    if not curves:
        return None
    name, t_on = min(curves, key=lambda c: abs(t - c[1]))
    return name, t - t_on


def onset_event(mat) -> list:
    if getattr(mat, "onset_curves", None) is None:
        return []

    def g(m, y):
        got = nearest_onset(mat, y[1], y[3])
        return 1.0 if got is None else got[1]
    return [st.Event("onset", g, scale=1.0, terminal=False)]


def layer_events(mat) -> list:
    return seam_events(mat) + ammonia_events(mat) + onset_event(mat)


@dataclass(frozen=True)
class Graze:
    curve: str
    material: str
    p: float
    g: float                       # T − T_onset at the extremum node [K]
    m: float


class GrazeMonitor:
    """Node rule of the old detector (interior.py:1432–1452 at 097a8aa3), kept: per curve, the last two nodes; the
    middle one of three is a graze when Δg changes sign there and |g| ≤ GRAZE_K. The closest graze is kept."""

    def __init__(self, mat):
        self.mat = mat
        self.hist: dict = {}
        self.best: Graze | None = None

    def __call__(self, m: float, y: tuple) -> None:
        p, t = y[1], y[3]
        oc = getattr(self.mat, "onset_curves", None)
        if oc is None or t <= 0.0:
            return
        try:
            curves = oc(p if p > 0.0 else 1.0e5, t)
        except Exception as exc:
            if type(exc).__name__ in ("PhaseGap", "SpinodalGap"):
                return
            raise
        for name, t_on in curves:
            g = t - t_on
            h = self.hist.get(name, ())
            if len(h) == 2:
                (g_a, _m_a, _p_a), (g_b, m_b, p_b) = h
                if (g_b - g_a) * (g - g_b) < 0.0 and abs(g_b) <= GRAZE_K and g_b * g_a > 0.0 and g_b * g > 0.0:
                    if self.best is None or abs(g_b) < abs(self.best.g):
                        self.best = Graze(name, getattr(self.mat, "name", "?"), p_b, g_b, m_b)
            self.hist[name] = (h[-1], (g, m, p)) if h else ((g, m, p),)


def onset_graze_tag(graze: Graze | None, s: float | None) -> bool:
    """R-C157-11's membership rule as fields: a graze exists and S > GRAZE_SLOPE. In the new formulation S is
    |d ln T_pot / d ln T_c|, the quantity the old loop's |Δ ln T_surf / Δ ln T_c| measured (design §A1.7)."""
    return graze is not None and s is not None and s > GRAZE_SLOPE
