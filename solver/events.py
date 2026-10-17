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

import bisect
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


#: P1R-G1-R-11: the engine's refusal channels these direct material calls (event g, the cap, the band test, the graze
#: monitor) read as «not here»: PhaseGap, SpinodalGap and, as the adapter maps it since G3-C-01, ValueError. The density
#: path refuses by name at the same state when the material itself cannot answer there.
ENGINE_GAPS = ("PhaseGap", "SpinodalGap", "ValueError")


def _curve_at(mat, name, p, t, p_stop=0.0):
    """T − T_onset of the named curve at (P, T), or None where the material reports no such curve. The surface start
    (P ≤ 0) is read at max(1 bar, p_stop), as dT/dP is."""
    oc = getattr(mat, "onset_curves", None)
    if oc is None or t <= 0.0:
        return None
    try:
        curves = oc(p if p > 0.0 else max(1.0e5, p_stop), t)
    except Exception as exc:                     # a material domain edge: no curve read here (the density path
        if type(exc).__name__ in ENGINE_GAPS:   # refuses by name at the same state)
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


def layer_events(src, p_stop: float = 0.0) -> list:
    """The events of one layer, from its view (switch-over registration §2): a phase-2 record view builds them from its
    own declarations (record_events); any other view, or a bare legacy material, from the legacy material as before."""
    if hasattr(src, "record") and hasattr(src, "transitions"):
        return record_events(src)
    mat = getattr(src, "mat", None) or src
    return seam_events(mat) + ammonia_events(mat) + onset_events(mat, p_stop)


def melting_events(view) -> dict:
    """{event name: (phase a, phase b)} of a record view's melting boundaries; {} for any other view."""
    if not hasattr(view, "transitions") or not hasattr(view, "record"):
        return {}
    return {f"melt:{a}|{b}": (a, b) for (a, b), kind, _c in view.transitions() if kind == "melting"}


#: T samples [K] for a curve's P scale: every record T range lies inside, and the scale needs only P_b's size
CURVE_SCALE_TS = tuple(50.0 * k for k in range(1, 201))


def curve_p_scale(view, curve) -> float:
    """The landing scale of a curve event g = P − P_b(T): the largest |P_b| over the curve's T range, sampled every
    50 K, so the landing tolerance event_tol·scale is relative to P as phase 1's seams (scale = p_b) have it. A fixed
    1e9 gave 1e-3 Pa, 6e-14 of P at 17 GPa, under the ±4e-3 Pa that re-steps reproduce P to there; the landing never
    put a new-side iterate within it and chattered (pre-run on 68e47ffc, C1: 28 earth and venus O9 states on exported
    edges). 1e9 where the curve is absent at every sample."""
    pbs = [abs(pb) for t in CURVE_SCALE_TS if (pb := view.boundary_pressure(curve, t)) is not None]
    return max(pbs) if pbs and max(pbs) > 0.0 else 1.0e9


def record_events(view) -> list:
    """Switch-over registration §2: a record view's events.
    - P seams: seams() (phase windows, thermal-set seams), landed as legacy's seam events.
    - Field boundaries from transitions(): a solid–solid curve is a seam event g = P − P_b(T_ad) (None where the curve is
      absent); a gibbs boundary (curve form library) g = G_a − G_b at (P, T_ad); a melting curve is terminal: reaching
      it refuses as solve.melting_not_in_phase2 (D-P3).
    - Source-seam isotherms: T_ad = t (design note 5).
    - Onset curves: none for a record that declares none (legacy's onset_curves gives none for iron either); a view
      that declares `onset_curve_names` (the assemblage kind: legacy silicate's solidus, registration §3.1) gets
      phase 1's solidus seam and onset events, as legacy silicate does."""
    out = [st.Event(f"seam:{p_b:.9g}", (lambda m, y, p_b=p_b: y[1] - p_b), scale=p_b, terminal=False, seam=True,
                    component=1) for p_b in view.seams()]
    by_id = {ph.id: ph for ph in view.phases}
    for between, kind, curve in view.transitions():
        name = f"{'melt' if kind == 'melting' else 'phase'}:{between[0]}|{between[1]}"
        if curve.get("form") == "library":
            a, b = by_id[between[0]], by_id[between[1]]

            def g(m, y, a=a, b=b):
                from solver import material_library as ml
                try:
                    return a.library.at(y[1], y[2])["g"] - b.library.at(y[1], y[2])["g"]
                except ml.LibraryOutOfRange:            # 68 N64: only «outside its spline» means no boundary here
                    return None
            scale = 1.0e3
        else:
            def g(m, y, curve=curve):
                pb = view.boundary_pressure(curve, y[2])
                return None if pb is None else y[1] - pb
            scale = curve_p_scale(view, curve)
        # a curve g = P − P_b(T) lands with its landing stages held on the old side in P (component 1, as curve_seams):
        # without it a stage that crosses the curve reads the new side's dT/dP, the re-step's end T jumps with its
        # length, and on a steep curve g jumps with it (Mars 1774 K on (R1)'s swap extension: |g| between 0.17 and 40
        # Pa, never ≤ 1e-3; solve.event_chatter). A gibbs boundary has no such component
        comp = 1 if curve.get("form") != "library" and kind != "melting" else None
        out.append(st.Event(name, g, scale=scale, terminal=(kind == "melting"), seam=(kind != "melting"),
                            component=comp))
    for t_s, between in view.source_seams():
        out.append(st.Event(f"source_seam:{between[0]}|{between[1]}", (lambda m, y, t_s=t_s: y[2] - t_s),
                            scale=t_s, terminal=False, seam=True, component=2))
    if getattr(view, "onset_curve_names", ()):     # a record view declaring legacy onset curves (the assemblage kind,
        out += seam_events_of_curves(view)          # silicate registration §3.1): phase 1's solidus seams and onsets
        out += onset_events(view, getattr(view, "p_stop", 0.0))
    return out


def seam_events_of_curves(view) -> list:
    """The onset curves' own seam events (curve_seams) for a view that declares onset curve names."""
    return [st.Event(f"seam:{p_b:.9g}", (lambda m, y, p_b=p_b: y[1] - p_b), scale=p_b, terminal=False, seam=True,
                     component=1) for p_b in sorted(curve_seams(view))]


def _table_phases(mat) -> list:
    out = []
    for m, w in (getattr(mat, "parts", None) or ((mat, 1.0),)):
        if w > 0.0:
            out += [ph for ph in (getattr(m, "phases", ()) or ()) if getattr(ph, "table_key", "")]
    return out


#: Phase-1 design note 12a: the cell cap acts only where g lies within this many K of a legacy table's blend band;
#: 4 × the largest |Δg| an uncapped step made on Mars 1978–1989 K (49 K, measured with the window rule).
BAND_MARGIN = 200.0


def step_cap(mat, t_index: int = 2):
    """Phase-1 design note 12: the stepper's h cap for a material that declares a fine scale (today the legacy
    mantle table: one ln P cell), as (x, y, k1) → max |h| in mass from the ΔP cap and dP/dm = k1[1]; None for every
    other material, whose runs are then unchanged.
    Note 12a: the fine scale is the blend band's (its entry and exit move with E(P) cell by cell), so the cell cap
    applies only where g = E(P) − T_STEP/2 − T lies within BAND_MARGIN of the band [0, BLEND_K]. Outside that window a
    step is uncapped except that its estimated |Δg| (the current cell's edge secant and dT/dP) stays ≤ BAND_MARGIN / 2,
    so no step can carry g from outside the window across the band (measured: uncapped steps move g ≤ 49 K).
    `t_index`: the state component the material is read at, T_ad = y[2] in a segment, the lid's profile y[3] in a lid
    (note 13a item 4)."""
    if not _table_phases(mat):
        return None
    from solver.legacy_materials import table_band, table_cell_factor
    factors = {}                 # S1: the table constants once per phase, held by this cap (one material view)

    def cap(x, y, k1):
        p = y[1] if y[1] > 0.0 else 1.0e5
        try:
            ph = mat.phase_at(p)
        except Exception as exc:
            if type(exc).__name__ in ENGINE_GAPS:
                return None
            raise
        if id(ph) not in factors:
            factors[id(ph)] = (ph, table_cell_factor(ph), table_band(ph))   # the phase object is kept, so its id is not reused
        _ph, f, band = factors[id(ph)]
        dp = None if f is None else p * f
        if dp is None or not k1[1]:
            return None
        hc = abs(dp / k1[1])
        if band is None:
            return hc
        edge_at, offset, width, lnp, secant, t_lo = band
        e = edge_at(p)
        t = y[t_index]
        if not math.isfinite(e) or t < t_lo + width + BAND_MARGIN:
            return hc
        g = e - offset - t
        if -BAND_MARGIN <= g <= width + BAND_MARGIN:
            return hc
        i = min(max(bisect.bisect_right(lnp, math.log(p)) - 1, 0), len(secant) - 1)
        rate = secant[i] / p + abs(k1[t_index] / k1[1])     # |dg/dP| estimated on the current cell [K/Pa]
        if not math.isfinite(rate):
            return hc
        return None if rate == 0.0 else max(hc, abs(0.5 * BAND_MARGIN / rate / k1[1]))
    return cap


#: Notes 13 §1 / 13a: halving stops at the table's narrowest ln P cell over this, where the step is accepted and a
#: band_graze recorded.
BAND_FLOOR_DIV = 64.0
#: Note 13 §1: the declared margin on the T term of L (not a bound; the one inexact part).
BAND_T_MARGIN = 2.0


def _cell_slope_max(phase) -> tuple:
    """max |dE/d ln P| over each node cell of a table phase's upper edge E(P): the exact maximum of the cell's PCHIP
    derivative (engine smooth_table `_coeffs`, a quadratic in ln P per cell), or the chord slope in MODE «linear»;
    inf beside an empty column. Once per phase."""
    import importlib
    mc = importlib.import_module("mantle_composition")
    smooth = importlib.import_module("smooth_table")
    tab = mc._TABLES[phase.table_key]
    xs, ys = tab.lnp, tab.edge_ys
    out = []
    for i in range(len(xs) - 1):
        if ys[i] is None or ys[i + 1] is None:
            out.append(math.inf)
            continue
        if smooth.MODE == "linear":
            out.append(abs((ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i])))
            continue
        _x0, hh, y0, y1, m0, m1 = smooth._coeffs(xs, ys, i)
        # dE/dx = [(6t²−6t)y0 + (3t²−4t+1)h·m0 + (6t−6t²)y1 + (3t²−2t)h·m1] / h = (a t² + b t + c) / h, t in [0, 1]
        a = 6.0 * y0 + 3.0 * hh * m0 - 6.0 * y1 + 3.0 * hh * m1
        b = -6.0 * y0 - 4.0 * hh * m0 + 6.0 * y1 - 2.0 * hh * m1
        c = hh * m0
        cand = [0.0, 1.0] + ([-b / (2.0 * a)] if a != 0.0 and 0.0 < -b / (2.0 * a) < 1.0 else [])
        out.append(max(abs(a * t * t + b * t + c) for t in cand) / hh)
    return tuple(out)


def band_check(mat, t_index: int = 2):
    """Phase-1 design note 13 §1 as built (notes 13a, 13b): a factory of the Lipschitz test of an adaptive step [a, b]
    on a legacy table phase (one fresh test per stepper run, so no state crosses passes), or None for a material
    without one. For each band edge e in {0, W} of g = E(P) − T_STEP/2 − T (the g-band only, 13a N2): the edge passes
    when g − e changes sign over the step, or min |g − e| at the ends > ½·h·L, with h = |ln P_b − ln P_a| and
    L = max |dE/d ln P| over the spanned cells + BAND_T_MARGIN · max |P·dT/dP| at the step's end stages k1, k7 (13a
    item 3). Both pass → verdict None (accept). Else "halve", unless h ≤ the narrowest cell / BAND_FLOOR_DIV: the step
    is then accepted and the edge held as a graze candidate (13b), stored by commit() at the node the stepper accepts
    (68 H1). A candidate is dropped when g − e later changes sign (the edge was crossed: an approach, not a graze) and
    reported, as the dict commit() returns, when g − e later moves away from the edge with its sign kept (a turn: a
    graze). A step whose two ends are not on the same table phase, or
    that touches an empty column or a domain gap, is not tested (the seam landing and the cell cap cover it)."""
    if not _table_phases(mat):
        return None
    from solver.legacy_materials import table_band
    per = {}

    def consts(ph):
        got = per.get(id(ph))
        if got is None:
            band = table_band(ph)
            lnp = band[3]
            floor = min(b - a for a, b in zip(lnp, lnp[1:])) / BAND_FLOOR_DIV
            got = per[id(ph)] = (ph, band, _cell_slope_max(ph), floor)
        return got

    def phase(p):
        try:
            return mat.phase_at(p if p > 0.0 else 1.0e5)
        except Exception as exc:
            if type(exc).__name__ in ENGINE_GAPS:
                return None
            raise

    def g_at(ph, y):
        """(g, the band constants) at a state on table phase ph, or None where the edge is not finite."""
        _ph, band, cellmax, floor = consts(ph)
        e = band[0](y[1])
        return None if not math.isfinite(e) else e - band[1] - y[t_index]

    class Test:
        """One run's test (13b: candidates live per run). verdict() is pure: it judges the trial step [a, b] and keeps
        the edges it accepted at the floor; commit() runs on the node the stepper actually accepted, the trial's end or
        a landing short of it (68 H1), and resolves and stores the candidates there."""

        def __init__(self):
            self.pending = {}                       # edge → (sign of g − e, the record so far)
            self.floor_edges = ()                   # the last verdict's floor-accepted edges

        def verdict(self, x, y, x_new, y_new, k1, k7):
            self.floor_edges = ()
            pa, pb = y[1], y_new[1]
            if pa <= 0.0 or pb <= 0.0:
                return None
            ph = phase(pa)
            if ph is None or not getattr(ph, "table_key", "") or phase(pb) is not ph:
                return None
            _ph, band, cellmax, floor = consts(ph)
            edge_at, offset, width, lnp = band[:4]
            ea, eb = edge_at(pa), edge_at(pb)
            if not (math.isfinite(ea) and math.isfinite(eb)):
                return None
            la, lb = math.log(pa), math.log(pb)
            lo, hi = min(la, lb), max(la, lb)
            h = hi - lo
            i0 = min(max(bisect.bisect_right(lnp, lo) - 1, 0), len(cellmax) - 1)
            i1 = min(max(bisect.bisect_right(lnp, hi) - 1, 0), len(cellmax) - 1)
            l_e = max(cellmax[i0:i1 + 1])
            if not math.isfinite(l_e):
                return None
            l_t = max(abs(pa * k1[t_index] / k1[1]) if k1[1] else 0.0,
                      abs(pb * k7[t_index] / k7[1]) if k7[1] else 0.0)
            lip = l_e + BAND_T_MARGIN * l_t
            ga, gb = ea - offset - y[t_index], eb - offset - y_new[t_index]
            failing = []
            for e in (0.0, width):
                da, db = ga - e, gb - e
                if da * db < 0.0:
                    continue
                if not min(abs(da), abs(db)) > 0.5 * h * lip:
                    failing.append(e)
            if failing and h > floor:
                return "halve"
            self.floor_edges = tuple(failing)
            return None

        def commit(self, x, y, x_acc, y_acc):
            edges, self.floor_edges = self.floor_edges, ()
            ph = phase(y[1]) if y[1] > 0.0 else None
            if ph is None or not getattr(ph, "table_key", "") or y_acc[1] <= 0.0 or phase(y_acc[1]) is not ph:
                self.pending.clear()
                return None
            ga, gb = g_at(ph, y), g_at(ph, y_acc)
            if ga is None or gb is None:
                self.pending.clear()
                return None
            out = None
            for e, (sgn, rec) in list(self.pending.items()):
                da, db = ga - e, gb - e
                if da * sgn <= 0.0 or db * sgn <= 0.0:
                    del self.pending[e]               # crossed (or touched): an approach
                elif abs(db) < abs(da):
                    rec["min_abs_g"] = min(rec["min_abs_g"], abs(db))     # still closing in
                elif abs(db) > abs(da):
                    del self.pending[e]               # turned away on the same side: a graze
                    out = out or rec
            floor = consts(ph)[3]
            for e in edges:
                da, db = ga - e, gb - e
                if e not in self.pending and db != 0.0 and da * db > 0.0:
                    self.pending[e] = (1.0 if db > 0.0 else -1.0,
                                       {"material": getattr(mat, "name", "?"), "p": y_acc[1], "edge": e,
                                        "min_abs_g": min(abs(da), abs(db)), "h_floor": floor, "m": x_acc})
            return out

    return Test


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
        self.joins = sorted(curve_seams(mat))
        self.branch = None

    def __call__(self, m: float, y: tuple) -> None:
        p, t = y[1], y[3]
        oc = getattr(self.mat, "onset_curves", None)
        if oc is None or t <= 0.0:
            return
        # P1R-G1-R-01: a curve's branch join (a seam, landed at P = p_b, which reads the new branch) is not a graze;
        # the three-node window never spans it (the old detector's «clear on material change», per branch)
        branch = bisect.bisect_right(self.joins, p)
        if branch != self.branch:
            self.hist.clear()
            self.branch = branch
        try:
            curves = oc(p if p > 0.0 else max(1.0e5, self.p_stop), t)
        except Exception as exc:
            if type(exc).__name__ in ENGINE_GAPS:
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
