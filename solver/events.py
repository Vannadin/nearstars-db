# 층 안 사건 — 상 경계 · 열 세트 이음매 · 암모니아 표 격자 · 시작 곡선(고상선, 물/얼음) 착지와 스침 감시 (설계 §A1.3)
"""Events inside a layer and the graze monitor.

Frozen design: rewrite/phase1-design.frozen.md §A1.3; registration rewrite/phase1-a1-impl.frozen.md S5.

Events are `stepper.Event`s on the state y = (r, P, T_ad, T), non-terminal: the stepper lands on each and restarts
on the new side, so no stage of a step straddles a discontinuity of the integrand.
- pressure seams: every finite phase boundary and thermal-set seam of the material (`eos.Material.stencil_bounds`'s
  set, R-C157-4/-5); mixtures take the union over their parts; the water ladder `h2o` is excluded as in the old
  engine (`interior.PHASE_CUT_EXCLUDED`; its phase follows (P, T) through the onset curves);
- ammonia table grid (R-C157-5's nh3 kinks, now located): the isotherm nodes T = T_k of `ammonia_table.T_K`;
- onset curves (R-C157-11): one event per curve, g = T − T_onset(P), None where the curve is absent; the curve's
  branch joins and end are seam events, landed first (r2 S5 B2). The liquidus is not an event (withdrawn in
  R-C157-11). Water curves are not listed (the water family is not ported, note 2 item 10).
The graze monitor follows R-C157-10..12's node rule unchanged (interior.py:1432–1452): at accepted nodes, a local
extremum of g = T − T_onset with |g| ≤ GRAZE_K is a graze; the closest one is kept as a typed record.
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


def _melt_curve_names(mat) -> list:
    """Names of the onset curves a material can report (eos `onset_curves`): the silicate solidus for a phase with
    silicate melting. Mixtures take the union over their parts. Water curves are not listed: the water family is
    not in the phase-1 adapter (note 2 item 10)."""
    names = list(getattr(mat, "onset_curve_names", ()))   # a fixture or future material may declare its own
    for m, w in (getattr(mat, "parts", None) or ((mat, 1.0),)):
        if w <= 0.0:
            continue
        if any(getattr(ph, "melt", None) == "silicate" for ph in (getattr(m, "phases", ()) or ())):
            if "고상선" not in names:
                names.append("고상선")
    return names


def curve_seams(mat) -> set:
    """Pressures where an onset curve changes branch or ends (eos.silicate_solidus at 097a8aa3): the HZ96 → Monteux
    eq. (12) join at MONTEUX_JOIN_PA (20 GPa, a −1 K step), the rock → MgSiO₃ melt-point join at SILICATE_ROCK_MAX_PA
    (140 GPa, +1732 K) and the curve's end at SILICATE_MELT_MAX_PA (500 GPa). Each is a seam event, so a curve is
    never read across its own jump (r2 S5 B2)."""
    if "고상선" not in _melt_curve_names(mat):
        return set()
    from solver.legacy_materials import eos
    return {float(eos.MONTEUX_JOIN_PA), float(eos.SILICATE_ROCK_MAX_PA), float(eos.SILICATE_MELT_MAX_PA)}


def seam_events(mat) -> list:
    return [st.Event(f"seam:{p_b:.9g}", (lambda m, y, p_b=p_b: y[1] - p_b), scale=p_b, terminal=False, seam=True,
                     component=1)
            for p_b in sorted(_material_seams(mat) | curve_seams(mat))]


def ammonia_events(mat) -> list:
    if not _has_ammonia(mat):
        return []
    from solver.legacy_materials import ammonia_isotherms
    # the integrand reads the material at T_ad (rhs.make_rhs), so the isotherm is crossed in T_ad (y[2])
    return [st.Event(f"nh3_isotherm:{t_k:g}", (lambda m, y, t_k=t_k: y[2] - t_k), scale=t_k, terminal=False,
                     seam=True, component=2) for t_k in ammonia_isotherms()]


#: Onset-event landing scale [K]: |g| ≤ event_tol · ONSET_SCALE = 1e-9 K, well above T's ulp (~5e-13 K at 4000 K);
#: a 1 K scale (1e-12 K) stalled at 2–4 ulp on real solidus crossings (r2 S5 B1).
ONSET_SCALE = 1.0e3


def _curve_at(mat, name, p, t, p_stop=0.0):
    """T − T_onset of the named curve at (P, T), or None where the material reports no such curve. The surface start
    (P ≤ 0) is read at max(1 bar, p_stop), as dT/dP is."""
    oc = getattr(mat, "onset_curves", None)
    if oc is None or t <= 0.0:
        return None
    try:
        curves = oc(p if p > 0.0 else max(1.0e5, p_stop), t)
    except Exception as exc:                     # a material domain edge: no curve read here (the density path
        if type(exc).__name__ in ("PhaseGap", "SpinodalGap"):   # refuses by name at the same state)
            return None
        raise
    for n, t_on in curves:
        if n == name:
            return t - t_on
    return None


def onset_events(mat, p_stop: float = 0.0) -> list:
    """One event per onset curve (r2 S5 B2: no «nearest curve» switching). g is None where the curve is absent; its
    domain ends and branch jumps are seam events (`curve_seams`), landed first."""
    return [st.Event(f"onset:{name}", (lambda m, y, name=name: _curve_at(mat, name, y[1], y[2], p_stop)),
                     scale=ONSET_SCALE, terminal=False) for name in _melt_curve_names(mat)]


def onset_event(mat, p_stop: float = 0.0) -> list:
    """Kept name: the per-curve onset events."""
    return onset_events(mat, p_stop)


def layer_events(mat, p_stop: float = 0.0) -> list:
    return seam_events(mat) + ammonia_events(mat) + onset_events(mat, p_stop)


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

    def __init__(self, mat, p_stop: float = 0.0):
        self.mat = mat
        self.p_stop = p_stop
        self.hist: dict = {}
        self.best: Graze | None = None

    def __call__(self, m: float, y: tuple) -> None:
        p, t = y[1], y[3]
        oc = getattr(self.mat, "onset_curves", None)
        if oc is None or t <= 0.0:
            return
        try:
            curves = oc(p if p > 0.0 else max(1.0e5, self.p_stop), t)
        except Exception as exc:
            if type(exc).__name__ in ("PhaseGap", "SpinodalGap"):
                return
            raise
        for name, t_on in curves:
            g = t - t_on
            h = self.hist.get(name, ())
            if len(h) == 2:
                (g_a, _m_a, _p_a), (g_b, m_b, p_b) = h
                if (g_b - g_a) * (g - g_b) < 0.0 and abs(g_b) <= GRAZE_K:
                    if self.best is None or abs(g_b) < abs(self.best.g):
                        self.best = Graze(name, getattr(self.mat, "name", "?"), p_b, g_b, m_b)
            self.hist[name] = (h[-1], (g, m, p)) if h else ((g, m, p),)


def onset_graze_tag(graze: Graze | None, s: float | None) -> bool:
    """R-C157-11's membership rule as fields: a graze exists and S > GRAZE_SLOPE. In the new formulation S is
    |d ln T_pot / d ln T_c|, the quantity the old loop's |Δ ln T_surf / Δ ln T_c| measured (design §A1.7)."""
    return graze is not None and s is not None and s > GRAZE_SLOPE
