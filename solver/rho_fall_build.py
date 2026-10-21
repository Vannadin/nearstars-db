# ρ 떨어짐 구간 집합 짓기(원형, 68 설계 rev 3) — T 칸마다 하위 표본에서 인증 탐색으로 ρ 의 P 방향 떨어짐을 찾아 노드별 S_i 를 만든다
"""PROTOTYPE (68 design rev 3 b2599b5d): the build-time fall-interval sets for the ρ monotone repair.

    python3 -m solver.rho_fall_build RECORD_ID OUT.json [--cells IB0:IB1] [--p GPA0:GPA1] [--nsub 16]
    (or as a unitq job: unitq.py solver/rho_fall_build.py OUTDIR --slots N -- RECORD_ID; one unit per T cell)

R is rowblend's read of ρ (the bridge off), as a Dual in ln P. For every T cell ib and its sub-samples
T = T_ib + (T_ib+1 − T_ib)·j/nsub, j = 0 … nsub:
- **Locate falls** (∂R/∂lnP < −1e-5 R) over ln P, by an adaptive heuristic in x (68 addendum 1: «certified» withdrawn; the evidence is the independent
  4× half-offset lattice and the near-step plant): the base grid is SUB_P points per P cell plus the read's own
  breakpoints (the P cell bounds, the stencil rows' curve positions, each edge window's centre and ends at T, and every
  cut swap's P_b_ext(T) ± SWAP_EPS); a grid cell
  [x, x + h] is fall-free when min(g(x), g(x + h)) − M·h/2 ≥ −1e-5, g = R′/R, M = SAFETY × the largest |Δg|/Δx over
  the cell and its two neighbours (the R″ estimate), **and** the secant test 1.5·d − 0.25·(g(x) + g(x + h)) ≥ −1e-5,
  d = (R(x + h) − R(x))/(h·R(x)) (the midpoint of the slope quadratic through both end slopes and the mean slope). Otherwise it is split at its midpoint, down to H_MIN = 1e-6 ln P;
  a cell still uncertain there is a STOP («unresolved»), unless both its ends rise (g ≥ −1e-5) and R does not fall
  across it: then it is a kink of R′ the estimate can't resolve, accepted and counted («floor_cells»).
- **A fall interval** runs from the local maximum before the falling run (g crosses 0 going down, bisected) to the
  point where R regains that value after it (bisected); it is widened by C_WIDEN·extent on each side. A fall that does
  not regain before 3 × the local window half-width past its start or before p_dataset is listed «unrecovered» and
  left out.
- **Net fall** (r2 a69976dc): at the sample, R(b′) < R(a′) for a widened interval. (1) b′ moves right, the side that
  regains, up to the next landed step or p_dataset, until R(b′) ≥ R(a′) («widened»). (2) Else, if b′ is a landed
  step's near side, the read ends the bridge flat at R(a′) and the step's jump absorbs the fall («absorbed»; the jump
  from R(a′) must stay ≥ 0). (3) Otherwise a STOP, naming its bound.
- **A widened end where the read refuses** (r2 8e0d13fa, rev3b class 3) is clipped at the refusal boundary (the last
  readable point, bisected) and listed «clipped»; the net-fall rules then apply to the clipped interval.
- **At the floor, the fall line** (r2 8e0d13fa, rev3b class 2): a cell whose ends and secant are all ≥ THR is no fall
  though R decreases; it is accepted and listed «slow_floor» with its secant.
- **rev3c: zero-height coincident downsteps** (68's design, r2 clear 1916061f, artifacts main f11695a0 blob 40d180cc): a
  coincident edge pair's downward jump on its own row within the table's EDGE_DRHO_TOL is height 0 — kept as a landed
  bound, never a fall, no ΔG solve, not gated, never an absorber, listed «zero_height»; above τ_e or past its rows a
  STOP.
The set S_i of T node i is the union of the widened intervals from every sample in cells i − 1 and i, overlaps merged.
Output: {"record", "ps", "ts", "stamp", "sets": {i: [[a′, b′], …]}, "unrecovered", "stops", "samples"}."""
from __future__ import annotations

import bisect
import json
import math
import sys

THR = -1e-5          # a fall: ∂R/∂lnP / R below this (rho_window's rule)
SUB_P = 16           # base grid points per P cell
SAFETY = 4.0         # on the R″ estimate
H_MIN = 1e-6         # ln P
C_WIDEN = 0.5        # 68 rev 3: c, a declared judgment
REGAIN_W = 3.0       # unrecovered past this many window half-widths
SWAP_EPS = 1e-9      # ln P: a landed swap's two sides are read this far from its P_b(t)
W_S = 0.01           # rev3d D3: a stencil row's two adjacent curve positions closer than this are a sliver (ln P)
N_S = 32             # rev3d D3: forced subcells across a sliver
TAU_W_DIV = 10.0     # rev3d D4: the widening stops where R has moved by the cell's ρ band / TAU_W_DIV
TAU_W_RULE = ("τ_w = (the ρ band of the cell holding the uncapped end, its sample's own ib, ia by bisect_left)/10; "
              "no band → τ_w = 0 (rev3d D4, amendment 1)")


class Unresolved(Exception):
    pass


_BA = {}


def _builder():
    """The records generator's own module (rewrite/phase2-records/build_assemblage.py, BurnMan 2.1.0), from
    NS_BUILD_ASSEMBLAGE (its directory); imported only when a downward swap jump needs its ΔG."""
    if "m" not in _BA:
        import importlib.util
        import os
        d = os.environ.get("NS_BUILD_ASSEMBLAGE")
        if not d:
            _BA["m"] = None
        else:
            spec = importlib.util.spec_from_file_location("build_assemblage", os.path.join(d, "build_assemblage.py"))
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            _BA["m"] = m
    return _BA["m"]


def _two_sides(m, bulk, kl, kr, p, t, warm):
    """(G, V) per atom of each label's equilibrium at (p, t), the generator's own solve at its final tol, warm-started
    per label; None for a side that does not converge."""
    out = []
    for k in (kl, kr):
        ok, rock, _why = m._equilibrate(bulk, k, warm.get(k), p, t, tol=m.EQ_TOL_FINAL)
        if not ok:
            ok, rock, _why = m._equilibrate(bulk, k, None, p, t, tol=m.EQ_TOL_FINAL)
        if not ok:
            out.append(None)
            continue
        warm[k] = m._state(rock)
        n = sum(rock.formula.values())
        out.append((float(rock.molar_gibbs / n), float(rock.molar_volume / n)))
    return out


def swap_gibbs(v, curve_id, t, p_b, p_lo, p_hi):
    """A downward swap jump at (P_b_ext(T), T), classed by r2's rulings (ce571b67 with addendum 1, bbcbcd23); G and V
    per atom from the records generator's own solve (build_assemblage.py at EQ_TOL_FINAL), labels from the curve's
    nearest row, ΔG = G₊ − G₋ and ΔV = V₊ − V₋ (right minus left).
    - **row-located** (T within the curve's own rows, t0 … t1): ΔG at P_b against the generator's TP_TOL (addendum 2's
      gate: |ΔG| > TP_TOL is a STOP).
    - **extension band** (T outside its rows, P_b_ext extrapolated): the true crossing at T, ΔG(P) = 0 between the two
      labels, bisected on [p_lo, p_hi] (the neighbouring swaps at T), with P_true, the displacement P_true − P_b_ext
      and ΔV at P_true: ΔV ≤ 0 «read-extension step» (the record is sound); ΔV > 0 «record STOP»; no sign change on the
      bracket «read-extension STOP».
    The bulk is one per record, so both sides share it (composition_same, by construction)."""
    m = _builder()
    c = v._events[curve_id]
    row = c.nearest(t)
    located = c.t0 <= t <= c.t1
    out = {"class": "row-located" if located else "extension band", "left": row["left_label"],
           "right": row["right_label"], "composition_same": True,
           "composition_why": "one bulk per record: build_assemblage.py builds a record from «bulk = atomic_bulk("
                               "COMPOSITIONS[comp_key][\"oxides_wt\"])» and equilibrates every candidate on it"}
    if m is None:
        out["verdict"] = "not evaluated (NS_BUILD_ASSEMBLAGE not set)"
        return out
    import numpy as np
    comp = v.material_id.removeprefix("silicate_slb_")
    bulk = m.atomic_bulk(m.COMPOSITIONS[comp]["oxides_wt"])
    kl, kr = m.canon_key(row["left_label"]), m.canon_key(row["right_label"])
    cands = set(m.candidates(p_b))
    out["labels_are_candidates"] = kl in cands and kr in cands       # r2 n2: both sides are the generator's own
    warm = {}
    with np.errstate(all="raise"):
        at_b = _two_sides(m, bulk, kl, kr, p_b, t, warm)
        if None in at_b:
            out.update(verdict="a side does not converge at P_b", tol=m.TP_TOL)
            return out
        dg_b = at_b[1][0] - at_b[0][0]
        out.update(dg_at_pb=dg_b, dv_at_pb=at_b[1][1] - at_b[0][1], tol=m.TP_TOL)
        if located:
            out["verdict"] = "STOP: |ΔG| > TP_TOL at a row-located swap" if abs(dg_b) > m.TP_TOL else "within TP_TOL"
            return out
        # the bracket grows from P_b outward on both sides (ln P steps 0.002, doubling), never past the neighbouring
        # swaps at T, and stops where a side stops converging: the root must lie where both labels exist
        xb_, br = math.log(p_b), None
        lo_lim, hi_lim = math.log(p_lo), math.log(p_hi)
        step, alive = 0.002, {-1: True, 1: True}
        while br is None and (alive[-1] or alive[1]):
            for sgn in (-1, 1):
                if not alive[sgn]:
                    continue
                x2 = xb_ + sgn * step
                if (sgn < 0 and x2 <= lo_lim) or (sgn > 0 and x2 >= hi_lim):
                    alive[sgn] = False
                    continue
                s2 = _two_sides(m, bulk, kl, kr, math.exp(x2), t, warm)
                if None in s2:
                    alive[sgn] = False
                    continue
                f2 = s2[1][0] - s2[0][0]
                if (f2 > 0) != (dg_b > 0):
                    br = (min(xb_, x2), max(xb_, x2), dg_b if x2 > xb_ else f2)
                    break
            step *= 2.0
        if br is None:
            out["verdict"] = "read-extension STOP: no crossing between the neighbouring swaps where both labels exist"
            return out
        out.update(p_lo=p_lo, p_hi=p_hi, bracket_gpa=[math.exp(br[0]) / 1e9, math.exp(br[1]) / 1e9])
        a, b, fa = br
        for _ in range(30):                              # to ~1e-9 in ln P
            mid = 0.5 * (a + b)
            sm = _two_sides(m, bulk, kl, kr, math.exp(mid), t, warm)
            if None in sm:
                out["verdict"] = "read-extension STOP: a side does not converge in the bisection"
                return out
            fm = sm[1][0] - sm[0][0]
            if (fm > 0) == (fa > 0):
                a, fa = mid, fm
            else:
                b = mid
        p_true = math.exp(0.5 * (a + b))
        st_ = _two_sides(m, bulk, kl, kr, p_true, t, warm)
        dv = st_[1][1] - st_[0][1]
        out.update(p_true=p_true, displacement=p_true - p_b, dv_true=dv, dv_rel=dv / st_[0][1],
                   verdict="read-extension step (record sound: ΔV ≤ 0 at the nearest crossing found)" if dv <= 0.0 else
                   "record STOP: ΔV > 0 at the true crossing")
    return out


def _reader(v, t, ib, unreadable):
    from solver import material_assemblage as ma, stepper as stp
    memo = {}

    def g(x):
        """(R, R′/R) at x, or None when the read refuses; on scratch state, the bridge off."""
        if x in memo:
            return memo[x]
        pr = math.exp(x)
        ia = min(max(bisect.bisect_left(v.ps, pr, 1) - 1, 0), len(v.ps) - 2)
        n, counts, marks, memo_r = len(v.notes), dict(v.cut_counts), v._marks, v._read_memo
        was = v._in_bridge
        v._in_bridge = True
        try:
            got = v._read(pr, t, pr, ma.Dual(x, 1.0, 0.0), ia, ib, fields=("rho",))
        except (ma._NoRead, ma.CellMissing):             # the read's own refusals (as _edge_read); anything else raises
            got = None
        finally:
            v._in_bridge = was
            del v.notes[n:]
            v.cut_counts.clear()
            v.cut_counts.update(counts)
            v._marks, v._read_memo = marks, memo_r
        if got is None or isinstance(got, stp.Stop):
            out = None
            unreadable.append(x)
        else:
            r = got["rho"]                               # a piece with no x dependence comes back as a float
            out = (r.v, r.dx / r.v) if isinstance(r, ma.Dual) else (r, 0.0)
        memo[x] = out
        return out
    return g


def _bisect(f, a, b, fa, n=60):
    for _ in range(n):
        m = 0.5 * (a + b)
        fm = f(m)
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
    return 0.5 * (a + b)


def _edge_tol(rid):
    """τ_e: the table's own boundaries.source.edge_drho_tol from the registry (rev3c §2; never re-derived), or None."""
    from solver import material_registry as mr
    tb = mr.load().tables.get(rid) or {}
    return ((tb.get("boundaries") or {}).get("source") or {}).get("edge_drho_tol")


def _view_tol(v):
    """_edge_tol for v's record, read once per view (kept on the view, not in module state)."""
    if not hasattr(v, "_rev3c_tol"):
        v._rev3c_tol = (_edge_tol(v.material_id),)
    return v._rev3c_tol[0]


def _zero_height(j, tol):
    """rev3c §2, the single decision point: the reason a swap jump is a zero-height case, or None. It qualifies when it is
    a coincident edge pair (was_edge), on the pair's own row (extrap_k 0), downward, and |rel| ≤ τ_e (the table's
    edge_drho_tol; None: nothing qualifies)."""
    if tol is None or not j.get("coincident_edge") or j.get("extrap_k", 0.0) != 0.0 or not j["jump"] < 0.0:
        return None
    if abs(j["rel"]) > tol:
        return None
    return f"a coincident edge pair's downstep on its own row within EDGE_DRHO_TOL ({abs(j['rel']):.4g} ≤ {tol:g})"


def _absorber(swaps, zero_x, right):
    """rev3c §3.4: the landed swap on a net fall's `right` bound that rule 2 may credit, or None when there is none or it
    is a zero-height case (its far side's lower value is never credited)."""
    xs_, cid = next(((xs_, c_) for xs_, c_ in swaps if xs_ - SWAP_EPS == right), (None, None))
    if xs_ is None or any(abs(xs_ - z) <= 1e-12 for z in zero_x):
        return None
    return xs_, cid


def _band_at(v, x, ib):
    """rev3d amendment 1: the ρ band of the cell (ia, ib) holding x, ia as the read takes it (bisect_left), ib passed
    in (the sample's own cell): the sum of its interp_terms + loop_terms relative ρ terms, None when it carries none."""
    pr = math.exp(x)
    ia = min(max(bisect.bisect_left(v.ps, pr, 1) - 1, 0), len(v.ps) - 2)
    tot, any_ = 0.0, False
    for key in ("interp_terms", "loop_terms"):
        cells = v._terms[key][0]
        e = cells.get((ia, ib)) if cells else None
        if e and e[0]:
            tot, any_ = tot + abs(e[0]), True
    return tot if any_ else None


def _cap(v, g, ib, t, x0, limit, sgn, step, caps, no_band):
    """rev3d D4: the widened end on one side (sgn −1: the max side, left of a; +1: the regain side, right of c) and its
    τ_w. Walked from x0 toward limit on the fine step; the first sample past R(x0)·(1 ± τ_w) brackets the crossing,
    bisected to H_MIN keeping the near side (R(end) on the threshold's x0 side). No crossing: limit. A refusing
    sample ends the walk there, and the class 3 clip then bisects it back to the readable side and lists it, as for an
    uncapped end. τ_w = 0 where the cell
    holds no ρ band: the end stays at x0, listed in no_band."""
    band = _band_at(v, x0, ib)
    if band is None:
        no_band.append({"record": v.material_id, "ib": ib, "t": t, "x": x0, "side": "hi" if sgn > 0 else "lo"})
        return x0, 0.0
    tau = band / TAU_W_DIV
    r0 = g(x0)
    if r0 is None:
        return x0, tau
    thr = r0[0] * (1.0 + sgn * tau)
    past = (lambda r: r >= thr) if sgn > 0 else (lambda r: r <= thr)
    x, end = x0, limit
    while (x < limit) if sgn > 0 else (x > limit):
        x1 = min(x + step, limit) if sgn > 0 else max(x - step, limit)
        q = g(x1)
        if q is None:
            end = x1                                     # the refusing point: the class 3 clip bisects it back, listed
            break
        if past(q[0]):
            near, far = x, x1
            while abs(far - near) > H_MIN:
                m = 0.5 * (near + far)
                qm = g(m)
                if qm is None or past(qm[0]):
                    far = m
                else:
                    near = m
            end = near
            break
        x = x1
    caps.append({"t": t, "ib": ib, "side": "hi" if sgn > 0 else "lo", "x0": x0, "end": end, "tau_w": tau,
                 "band": band, "at_limit": end == limit})
    return end, tau


def _sliver_dips(slivers, grid, vals):
    """rev3d §5 (r2 n1): per refined sliver its gap and the span of its negative-g subcells (the dip D3 resolves)."""
    out = []
    for x0, x1 in slivers:
        neg = [x for x, q in zip(grid, vals) if x0 <= x <= x1 and q is not None and q[1] < THR]
        out.append({"x0": x0, "gap": x1 - x0, "dip_span": (max(neg) - min(neg)) if neg else 0.0, "dip_points": len(neg)})
    return out


def falls_at(v, t, ib, xlo, xhi):
    """The widened fall intervals of R(·, t) on [xlo, xhi], with the unrecovered falls and net-fall STOPs."""
    unreadable = []                                      # r2 B1: points the read refuses, counted and listed
    g = _reader(v, t, ib, unreadable)

    def gv(z):
        """g(z), raising where the read refuses (a bisection never invents a value: r2 B1)."""
        q = g(z)
        if q is None:
            raise Unresolved(f"the read refuses at ln P {z:.9f} (T {t:.3f} K) inside a fall search")
        return q
    unscreened = []                                      # cells with a refusing end: a refusal boundary, listed
    swaps = []                                           # every cut swap's P_b_ext(t): a landed event, never bridged
    for c in v._cut:
        if c.kind == "swap":
            pe = c.p_b_ext(t, v._reach)
            if pe is not None and xlo < math.log(pe) < xhi:
                swaps.append((math.log(pe), v._events.index(c)))
    # swap extension note 1 (r2 addendum 4 (4)): a reach-0 end's holding-row steps (the read's landed events,
    # _row_step_p): an upward one is a landed step, like a swap's (listed, never bridged, the intervals stop at it); a
    # downward one is a fall to bridge, never an «unresolved» cell
    row_steps, down = [], []
    for i in range(len(getattr(v, "_row_steps", ()))):
        q = v._row_step_p(i, t, ib)                      # 68 n1 on a7f3251b: the sample's own cell, not T-derived
        if q is None or not xlo < math.log(q) < xhi:
            continue
        xs_ = math.log(q)
        lo_r, hi_r = g(xs_ - SWAP_EPS), g(xs_ + SWAP_EPS)
        if lo_r is None or hi_r is None:
            continue
        jump = hi_r[0] - lo_r[0]
        row_steps.append({"t": t, "x": xs_, "row": v.ts[v._row_steps[i][1]], "jump": jump})
        if jump >= 0.0:
            swaps.append((xs_, f"row{i}"))
        else:
            down.append(xs_)
    swaps.sort()
    grid = list(v.lnps)                                  # the P cell bounds (68 addendum 1)
    for j in range(len(v.lnps) - 1):
        a, b = v.lnps[j], v.lnps[j + 1]
        for k in range(SUB_P):
            x = a + (b - a) * k / SUB_P
            if xlo <= x <= xhi:
                grid.append(x)
    grid.append(min(xhi, v.lnps[-1]))
    # the read's own breakpoints, where it is not smooth: every stencil row's curve positions (its regions' bounds, where
    # an empty region's smoothstep runs between two curves that can sit 1e-4 ln P apart) and every edge window's
    # centre and ends at t; between them R is smooth and the R″ estimate holds
    n_t = len(v.ts)
    for k in range(max(ib - 1, 0), min(ib + 2, n_t - 1) + 1):
        for pb, c in v._partition(k):
            grid.append(math.log(pb))
            if c.kind == "edge":
                pe = c.p_b_ext(t, v._reach)
                if pe is not None:
                    xb = math.log(pe)
                    w = v._width(xb)
                    grid += [xb, xb - w, xb + w]
    for xs_ in [x_ for x_, _c in swaps] + down:
        grid += [xs_ - SWAP_EPS, xs_ + SWAP_EPS]
    # rev3d D3: a stencil row's sliver (two adjacent curve positions of one row closer than W_S) is subdivided into
    # N_S equal subcells before the adaptive tests (a dip between them can rise at both ends and in its secant)
    slivers = []
    for k in range(max(ib - 1, 0), min(ib + 2, n_t - 1) + 1):
        xs_k = sorted(math.log(pb) for pb, _c in v._partition(k))
        for x0, x1 in zip(xs_k, xs_k[1:]):
            if 0.0 < x1 - x0 < W_S and x1 > xlo and x0 < xhi:
                slivers.append((x0, x1))
                grid += [x0 + (x1 - x0) * q / N_S for q in range(N_S + 1)]
    grid = sorted({x for x in grid if xlo <= x <= xhi})
    vals = [g(x) for x in grid]
    falling = []                                         # points where g < THR
    step_fall = {}                                       # a downward row step's fall point → the step's ln P
    floor_cells = []                                     # cells accepted at H_MIN (rising ends, R not falling)
    slow_floor = []                                      # r2 8e0d13fa: at H_MIN, ends and secant ≥ THR, R decreasing
    swap_jumps = []                                      # every swap's jump at t (68 addendum 1: listed, never bridged)
    for xs_, cid in swaps:
        if isinstance(cid, str):
            continue                                     # a row step: listed in row_steps, not a swap at t
        lo_r, hi_r = g(xs_ - SWAP_EPS), g(xs_ + SWAP_EPS)
        if lo_r is not None and hi_r is not None:
            c_ = v._events[cid]
            swap_jumps.append({"t": t, "x": xs_, "curve": cid, "r_before": lo_r[0], "r_after": hi_r[0],
                               "jump": hi_r[0] - lo_r[0], "rel": (hi_r[0] - lo_r[0]) / lo_r[0],
                               # r2 e843daa8 / directing 10-20: a coincident edge pair the read re-kinds as a swap, and
                               # how far its P_b is extrapolated in T past its own rows (0: on them, a true crossing)
                               "coincident_edge": bool(getattr(c_, "was_edge", False)),
                               "extrap_k": max(c_.t0 - t, t - c_.t1, 0.0)})
    # rev3c §3.1: a coincident pair's downstep on its own row within τ_e is height 0, with its pair's ids; above τ_e or
    # past its rows it STOPs here, before gate()
    tol = _view_tol(v) if any(j["coincident_edge"] and j["jump"] < 0.0 for j in swap_jumps) else None
    zero_x, ce_stops = [], []
    for j in swap_jumps:
        if not (j["coincident_edge"] and j["jump"] < 0.0):
            continue
        if _zero_height(j, tol) is not None:
            pair = sorted(i for i, c2 in enumerate(v._events) if getattr(c2, "was_edge", False) and c2.kind == "swap"
                          and (q := c2.p_b_ext(t, v._reach)) is not None and abs(math.log(q) - j["x"]) <= 1e-12)
            j.update(zero_height=True, tol=tol, pair=pair)
            zero_x.append(j["x"])
        elif tol is not None:
            j["pre_gate_stop"] = True
            ce_stops.append({**j, "gate": ("coincident-edge jump past its rows" if j["extrap_k"] > 0.0
                                           else "coincident-edge downstep above EDGE_DRHO_TOL")})

    def slope(i):
        if vals[i] is None or vals[i + 1] is None:
            return 0.0
        return abs(vals[i + 1][1] - vals[i][1]) / (grid[i + 1] - grid[i])

    def screen(a, b, fa, fb, m_est, depth=0):
        if fa is None or fb is None:
            unscreened.append({"t": t, "a": a, "b": b})
            return
        if any(a <= xs_ <= b for xs_, _c in swaps) and b - a <= 2.0 * SWAP_EPS * (1.0 + 1e-6):
            # the swap's own jump: listed above, not a fall. Closed at both ends: a swap's xs can be a grid point (a
            # one-row curve's constant P_b is a stencil row's partition point, bit for bit), and the jump then sits at
            # a half-cell's end (rev3b: bse swap168/170, khan swap123/124)
            return
        if any(a <= xs_ <= b for xs_ in down) and b - a <= 2.0 * SWAP_EPS * (1.0 + 1e-3):
            # a downward row step (its own P_b is a grid point too, so the step sits in one of the two half-cells): a
            # fall, bridged, where R drops across the half-cell; the other half is smooth and passes as any cell
            if fb[0] < fa[0]:
                falling.append(b)
                step_fall[b] = next(xs_ for xs_ in down if a <= xs_ <= b)
            return
        if fa[1] < THR:
            falling.append(a)
            return
        if fb[1] < THR:
            falling.append(b)
            return
        h = b - a
        # the secant's own test: a slope quadratic through g(a) and g(b) with the cell's mean slope d has
        # q(½) = 1.5·d − 0.25·(g(a) + g(b)); a fall hidden between two rising ends shows here (a narrow region's
        # smoothstep between two curves 1e-4 ln P apart drops R with both end slopes rising)
        d = (fb[0] - fa[0]) / (h * fa[0])
        if 1.5 * d - 0.25 * (fa[1] + fb[1]) >= THR and min(fa[1], fb[1]) - m_est * h / 2.0 >= THR:
            return
        if h < H_MIN:
            # a kink in R′ (both ends rising, R′ jumping) never passes the R″ estimate, which grows as 1/h there; at the
            # resolution floor a cell whose ends rise and whose R does not fall is accepted, counted and listed (68
            # addendum 1, question B). r2 8e0d13fa (rev3b class 2): THR is the fall line, so a cell whose ends and
            # secant are all ≥ THR is no fall either though R decreases ("slow_floor", listed with its secant); a
            # cell below the line anywhere is a STOP
            if fa[1] >= THR and fb[1] >= THR and fb[0] >= fa[0]:
                floor_cells.append({"t": t, "x": a})
                return
            if fa[1] >= THR and fb[1] >= THR and d >= THR:
                slow_floor.append({"t": t, "x": a, "secant": d})
                return
            raise Unresolved(f"unresolved at ln P {a:.9f} (T {t:.3f} K)")
        m = 0.5 * (a + b)
        fm = g(m)
        if fm is None:
            unscreened.append({"t": t, "a": a, "b": b})
            return
        m_loc = SAFETY * max(abs(fm[1] - fa[1]) / (h / 2), abs(fb[1] - fm[1]) / (h / 2))
        screen(a, m, fa, fm, max(m_loc, m_est / 2.0), depth + 1)
        screen(m, b, fm, fb, max(m_loc, m_est / 2.0), depth + 1)

    for i in range(len(grid) - 1):
        m_est = SAFETY * max(slope(j) for j in range(max(i - 1, 0), min(i + 2, len(grid) - 1)))
        screen(grid[i], grid[i + 1], vals[i], vals[i + 1], m_est)
    # falling points → fall intervals
    intervals, unrecovered, stops, seen = [], [], [], []
    caps, no_band = [], []                               # rev3d D4: each capped end; ends with no ρ band (τ_w = 0)
    widened, absorbed = [], []                           # r2 a69976dc: the net-fall rules 1 and 2, recorded
    clipped = []                                         # r2 8e0d13fa: widened ends clipped at a refusal boundary
    top = math.log(v.p_dataset)
    for xf in sorted(set(falling)):
        if any(a <= xf <= c for a, c in seen):
            continue
        # fall intervals stop at swap points (68 addendum 1): every search and the widening stay on xf's own side
        left = max([xlo] + [xs_ + SWAP_EPS for xs_, _c in swaps if xs_ < xf])
        right = min([xhi] + [xs_ - SWAP_EPS for xs_, _c in swaps if xs_ > xf])
        # the local max before: g crosses 0 going down; walk left on a fine step, then bisect
        j_ = min(max(bisect.bisect_right(v.lnps, xf) - 1, 0), len(v.lnps) - 2)     # r2 B2: xf's own P cell
        step = (v.lnps[j_ + 1] - v.lnps[j_]) / SUB_P / 4.0
        a = xf
        while xf not in step_fall:                       # a slope fall: walk to the local max before it
            q = g(a - step)
            if q is None or a - step < left:
                a = max(a - step, left) if q is not None else a
                break
            if q[1] >= 0.0:
                a = _bisect(lambda z: gv(z)[1], a - step, a, q[1])
                break
            a -= step
        if xf in step_fall:                              # a downward row step: the jump's two sides
            a, e = step_fall[xf] - SWAP_EPS, step_fall[xf] + SWAP_EPS
        else:
            e = xf                                       # the end of the falling run: g back above 0
        while xf not in step_fall:
            q = g(e + step)
            if q is None or e + step > right:
                break
            if q[1] >= 0.0:
                e = _bisect(lambda z: gv(z)[1], e, e + step, -1.0)
                break
            e += step
        ra = g(a)
        if ra is None:
            continue
        w = v._width(a)
        c, x = None, e
        while x < min(a + REGAIN_W * w, top, right):
            q = g(x + step)
            if q is None:
                break
            if q[0] >= ra[0]:
                c = _bisect(lambda z: gv(z)[0] - ra[0], x, x + step, gv(x)[0] - ra[0])
                break
            x += step
        if c is None:
            unrecovered.append({"t": t, "x_a": a, "x_fall": xf,
                                "bounded_by_swap": right < min(a + REGAIN_W * w, top, xhi)})
            seen.append((a, e))
            continue
        ext = c - a
        # rev3d D4 (+ amendment 1): C_WIDEN·extent stays the ceiling; inside it each side stops where R has moved by
        # τ_w = (the cell's ρ band at the uncapped end)/TAU_W_DIV from that end's own value — the regain side at
        # R(x) = R(c)·(1 + τ_w), x ≥ c, the max side at R(x) = R(a)·(1 − τ_w), x ≤ a — bisected to H_MIN on the
        # threshold's near side; a cell with no band gives τ_w = 0 (no widening past the end), listed
        lo_, cap_lo = _cap(v, g, ib, t, a, max(a - C_WIDEN * ext, left), -1, step, caps, no_band)
        hi_, cap_hi = _cap(v, g, ib, t, c, min(c + C_WIDEN * ext, right), +1, step, caps, no_band)
        seen.append((a, c))
        # r2 8e0d13fa (rev3b class 3): a widened end where the read refuses is clipped at the refusal boundary, the
        # last readable point on the interval's side (bisected), and recorded; a net fall after it STOPs naming it
        for side, end, inner in (("lo", lo_, a), ("hi", hi_, c)):
            if g(end) is None:
                bad, ok = end, inner                     # g(bad) refuses, g(ok) reads
                for _ in range(60):
                    m = 0.5 * (bad + ok)
                    if g(m) is None:
                        bad = m
                    else:
                        ok = m
                clipped.append({"t": t, "side": side, "was": end, "now": ok})
                if side == "lo":
                    lo_ = ok
                else:
                    hi_ = ok
        r_lo, r_hi = g(lo_), g(hi_)
        if r_lo is None or r_hi is None:
            stops.append({"t": t, "why": "a widened end the read can't evaluate", "a": lo_, "b": hi_})
            continue
        if r_hi[0] < r_lo[0]:
            # r2 a69976dc (the khan 2000 K net fall; no size floor): (1) b′ widens right, the side that regains, up
            # to the next landed step or p_dataset; (2) no regain up to a landed step: b′ moves to its near side, the
            # read ends the bridge flat at R(a′) there (_fall_bridge) and the step's jump absorbs the fall, which must
            # stay ≥ 0; (3) otherwise a STOP, naming its bound
            got, refused = _widen(g, gv, lo_, hi_, r_lo[0], right, step)
            xs_, cid = _absorber(swaps, zero_x, right) or (None, None)
            zero_bound = next((z for z in zero_x if abs(z - SWAP_EPS - right) <= 1e-12), None)
            if got is None and not refused and zero_bound is not None:
                stops.append({"t": t, "why": "net fall over the widened interval", "a": lo_, "b": hi_, "r_a": r_lo[0],
                              "r_b": r_hi[0], "bound": f"a zero-height coincident pair at ln P {zero_bound!r} (not an "
                                                       "absorber)"})
                intervals.append((lo_, hi_, a, c))
                continue
            if got is not None:
                # rev3d D4: rule 1 is not capped (regaining is required); its excess over the regain end's own value
                # is reported against that end's τ_w, listed by name above it
                rc_ = g(c)
                exc = None if rc_ is None or (rg := g(got)) is None else rg[0] / rc_[0] - 1.0
                widened.append({"t": t, "a": lo_, "b": got, "was_b": hi_, "net": r_hi[0] - r_lo[0],
                                "excess": exc, "tau_w": cap_hi})
                hi_ = got
            elif not refused and xs_ is not None and (far := g(xs_ + SWAP_EPS)) is not None:
                # no regain up to a landed step: the bridge runs flat at R(a′) to its near side
                ab = {"t": t, "by": cid, "x": xs_, "a": lo_, "b": right, "was_b": hi_, "dR": r_lo[0] - r_hi[0],
                      "jump": far[0] - r_lo[0]}
                if ab["jump"] >= 0.0 and isinstance(cid, str):
                    # rev3d amendment 2 §3: a row step absorbs for node k only if the read's own piece-k rule lands it
                    # fully there (λ = 1 at this T, from this cell, over this interval: _row_step_lambdas, called, not
                    # copied); otherwise not absorbed — rule 1 has already failed, so the STOP
                    ab["unlanded_for_nodes"] = [k for k in (ib, ib + 1)
                                                if not any(abs(z[0] - xs_) <= 1e-12 and z[1] >= 1.0
                                                           for z in v._row_step_lambdas(t, min(k, len(v.ts) - 2), ib,
                                                                                        lo_, right))]
                if ab["jump"] >= 0.0 and not ab.get("unlanded_for_nodes"):
                    absorbed.append(ab)
                    hi_ = right
                elif ab["jump"] >= 0.0:
                    stops.append({"t": t, "why": "net fall over the widened interval", "a": lo_, "b": hi_,
                                  "r_a": r_lo[0], "r_b": r_hi[0],
                                  "bound": f"row step {cid} not fully landed by the read for node(s) "
                                           f"{ab['unlanded_for_nodes']} (rev3d amendment 2 §3)"})
                else:
                    stops.append({"t": t, "why": "net fall over the widened interval", "a": lo_, "b": hi_,
                                  "r_a": r_lo[0], "r_b": r_hi[0],
                                  "bound": f"swap {cid} (its jump from R(a′) would be negative: {ab['jump']:.6g})"})
            else:
                bound = ("a refusing read" if refused else
                         "p_dataset" if right >= top - 1e-12 else "the window's end" if right >= xhi else "table edge")
                stops.append({"t": t, "why": "net fall over the widened interval", "a": lo_, "b": hi_,
                              "r_a": r_lo[0], "r_b": r_hi[0], "bound": bound})
        intervals.append((lo_, hi_, a, c))
    stops += ce_stops
    return intervals, unrecovered, stops, floor_cells, swap_jumps, {"unreadable": sorted(set(unreadable)),
                                                                   "unscreened": unscreened, "row_steps": row_steps,
                                                                   "widened": widened, "absorbed": absorbed,
                                                                   "clipped": clipped, "slow_floor": slow_floor,
                                                                   "caps": caps, "no_band": no_band,
                                                                   "slivers": _sliver_dips(slivers, grid, vals)}


def _widen(g, gv, lo, hi, r_lo, right, step):
    """r2 a69976dc rule 1: (hi′, False) with hi′ ≤ right the first point past hi where R regains R(lo) (the regaining
    side: a fall's start is its local max, so only the end moves); else (None, refused): refused True when a read
    refused on the way, False when R did not regain up to right. Walked on the regain search's step, the last step
    clamped to the bound (never across a landed step); bisected keeping the end that holds, so R(b′) ≥ R(a′) exactly
    (suites-1020 X3: a flag, never a string compared)."""
    x = hi
    while x < right:
        x1 = min(x + step, right)
        q = g(x1)
        if q is None:
            return None, True
        if q[0] >= r_lo:
            bad, ok = x, x1                              # R(bad) < R(lo) ≤ R(ok)
            for _ in range(60):
                m = 0.5 * (bad + ok)
                if gv(m)[0] >= r_lo:
                    ok = m
                else:
                    bad = m
            return ok, False
        x = x1
    return None, False


def _merge(ivs):
    out = []
    for a, b in sorted(ivs):
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def cell_falls(v, ib, nsub=16, xr=None):
    """Every sample of T cell ib: its intervals, unrecovered falls and STOPs."""
    xlo = v.lnps[0] if xr is None else max(xr[0], v.lnps[0])
    xhi = math.log(v.p_dataset) if xr is None else min(xr[1], math.log(v.p_dataset))
    out = []
    for j in range(nsub + 1):
        t = v.ts[ib] + (v.ts[ib + 1] - v.ts[ib]) * j / nsub
        try:
            ivs, un, st, fl, sj, ur = falls_at(v, t, ib, xlo, xhi)
        except Unresolved as e:
            ivs, un, st, fl, sj, ur = [], [], [{"t": t, "why": str(e)}], [], [], {"unreadable": [], "unscreened": [],
                                                                                "row_steps": []}
        for j_ in sj:
            j_["v_ratio"] = j_["r_after"] / j_["r_before"]          # V₋/V₊ at one mass: ρ₊/ρ₋
            if j_["jump"] < 0.0 and not j_.get("zero_height"):     # rev3c §3.5: a physical zero needs no ΔG
                try:
                    xs_all = sorted(math.log(pe) for c in v._cut if c.kind == "swap"
                                    for pe in (c.p_b_ext(t, v._reach),) if pe is not None)
                    below = [z for z in xs_all if z < j_["x"] - 1e-12]
                    above = [z for z in xs_all if z > j_["x"] + 1e-12]
                    p_lo = math.exp(below[-1]) if below else v.ps[0]
                    p_hi = math.exp(above[0]) if above else v.p_dataset
                    j_.update(swap_gibbs(v, j_["curve"], t, math.exp(j_["x"]), p_lo, p_hi))
                except Exception as e:                   # an equilibration that fails is recorded, not a crash
                    j_["gibbs_error"] = f"{type(e).__name__}: {str(e)[:200]}"
        out.append({"t": t, "intervals": [list(iv) for iv in ivs], "unrecovered": un, "stops": st, "floor_cells": fl,
                    "swap_jumps": sj, "unreadable": len(ur["unreadable"]), "unscreened": ur["unscreened"],
                    "row_steps": ur["row_steps"], "widened": ur.get("widened", []),
                    "absorbed": ur.get("absorbed", []), "clipped": ur.get("clipped", []),
                    "slow_floor": ur.get("slow_floor", []), "caps": ur.get("caps", []),
                    "no_band": ur.get("no_band", []), "slivers": ur.get("slivers", [])})
    return out


def sets_from(v, per_cell, dropped=None, stops=None):
    """S_i = the merged widened intervals of every sample in cells i − 1 and i, each kept only where its two edges read
    at every one of those samples under the stencil of the cell holding the sample — both at the shared node T_i
    (rev3d D1, amendment 1: read-faithful, as piece i is evaluated). An end that fails is clipped inward to the first
    point that reads everywhere, on the build's fine step (the rev3b class 3 rule under both stencils); an interval
    with no such point is dropped. `dropped`, a list, receives each clip and drop («unreadable_end»). A clipped interval
    is held to the net-fall rules again at every one of its samples (68 B1 on a7f3251b, as rev3b class 3 re-applies
    them): R(b₂) ≥ R(a₂), else rule 2 where b₂ sits on a landed step's near side (s_k's list) whose far side regains
    R(a₂), else a STOP «net fall after unreadable-end clip» in `stops`. The split ends inside an interval (a landed
    step's x_s ± SWAP_EPS) are not checked here: the read counts any of them that refuses (bridge_no_edge, 0 on G3's
    lattices, 68 n2)."""
    sets = {}
    for i in range(len(v.ts)):
        ivs = [(iv[0], iv[1]) for ib in (i - 1, i) for smp in per_cell.get(ib, ()) for iv in smp["intervals"]]
        if not ivs:
            continue
        samples = [(smp["t"], ib) for ib in (i - 1, i) for smp in per_cell.get(ib, ())]
        kept = []
        for a, b in _merge(ivs):
            got = _node_readable(v, a, b, samples, dropped, i, stops)
            if got is not None:
                kept.append(list(got))
        if kept:
            sets[i] = kept
    return sets


def _node_readable(v, a, b, samples, dropped, node, stops=None):
    """rev3d D1: (a, b), clipped inward until both edges read (_edge_read, the bridge's own edge reads) at every
    (T, stencil) of `samples`; None when the interval has no such pair. Each change is recorded in `dropped`."""
    def ok(x, below):
        return all(v._edge_read(x, t, ib, below) is not None for t, ib in samples)
    j_ = min(max(bisect.bisect_right(v.lnps, 0.5 * (a + b)) - 1, 0), len(v.lnps) - 2)
    step = (v.lnps[j_ + 1] - v.lnps[j_]) / SUB_P / 4.0
    def inward(x, lim, below, sgn):
        """The first point from x toward lim (sgn +1 right, −1 left) where the edge reads at every sample, bisected to
        H_MIN between the last failing and the first readable step; None when none is found before lim."""
        if ok(x, below):
            return x
        bad, y = x, x
        while (y < lim) if sgn > 0 else (y > lim):
            y = min(y + step, lim) if sgn > 0 else max(y - step, lim)
            if ok(y, below):
                good = y
                while abs(good - bad) > H_MIN:
                    m = 0.5 * (bad + good)
                    if ok(m, below):
                        good = m
                    else:
                        bad = m
                return good
            bad = y
        return None
    a2 = inward(a, b, True, +1)
    b2 = None if a2 is None else inward(b, a2, False, -1)
    if a2 is None or b2 is None:
        a2 = b2 = a
    if not a2 < b2:
        if dropped is not None:
            dropped.append({"node": node, "a": a, "b": b, "what": "unreadable_end: dropped"})
        return None
    if (a2, b2) != (a, b):
        if dropped is not None:
            dropped.append({"node": node, "a": a, "b": b, "now": [a2, b2], "what": "unreadable_end: clipped"})
        bad = _clip_net_fall(v, a2, b2, samples, node)
        if bad and stops is not None:
            stops.append({"why": "net fall after unreadable-end clip", "node": node, "a": a2, "b": b2, "was": [a, b],
                          "samples": bad[:5], "n": len(bad)})
    return a2, b2


def _clip_net_fall(v, a, b, samples, node):
    """68 B1: the samples (T, ib) where the clipped interval's bridge would be a net fall that rule 2 doesn't absorb —
    R(b) < R(a) with no landed upward step (a cut swap's P_b_ext(T), or s_k's row steps) within 2·SWAP_EPS above b
    whose far side reads ≥ R(a)."""
    on = 2.0 * SWAP_EPS * (1.0 + 1e-6)
    sk = min(node, len(v.ts) - 2)
    bad = []
    for t, ib in samples:
        ea, eb = v._edge_read(a, t, ib, True), v._edge_read(b, t, ib, False)
        if ea is None or eb is None or eb[0] >= ea[0]:
            continue
        landed = [math.log(pe) for c in v._cut if c.kind == "swap" for pe in (c.p_b_ext(t, v._reach),) if pe is not None]
        landed += [z[0] for z in v._row_step_lambdas(t, sk, ib, a, b) if z[1] >= 1.0]   # amendment 2 §3: the read's own
        far = [v._edge_read(xs_ + SWAP_EPS, t, ib, False) for xs_ in landed if b < xs_ <= b + on]
        if not any(f is not None and f[0] >= ea[0] for f in far):
            bad.append({"t": t, "ib": ib, "r_a": ea[0], "r_b": eb[0]})
    return bad


def _view(rid):
    from solver import material_registry as mr, material_assemblage as ma
    from solver.from_v1 import thaw
    reg = mr.load()
    return ma.view(thaw(reg.get(rid)), reg.tables[rid], 1600.0)


def _ma():
    from solver import material_assemblage as ma
    return ma


def _stamp(edge_tol=None):
    import hashlib
    import subprocess
    from pathlib import Path
    data = Path(__file__).read_bytes()
    eng = Path(__file__).resolve().parents[1]
    return {"tool_blob": hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(),
            "engine": subprocess.run(["git", "-C", str(eng), "rev-parse", "HEAD"], capture_output=True,
                                     text=True).stdout.strip(),
            "rules": {"THR": THR, "SUB_P": SUB_P, "SAFETY": SAFETY, "H_MIN": H_MIN, "C_WIDEN": C_WIDEN, "REGAIN_W": REGAIN_W,
                      "EDGE_DRHO_TOL": edge_tol}}


def _floor_list(fl):
    by = {}
    for f_ in fl:
        k = round(f_["x"], 7)
        e = by.setdefault(k, {"x": k, "n": 0, "t_min": f_["t"], "t_max": f_["t"]})
        e["n"] += 1
        e["t_min"], e["t_max"] = min(e["t_min"], f_["t"]), max(e["t_max"], f_["t"])
    return sorted(by.values(), key=lambda e: e["x"])


def _band_rho(v, x, t):
    """The record's shipped ρ band at the cell holding (x, T): the sum of its per-cell relative ρ terms (interp_terms,
    loop_terms; the read ships them as BandNotes); None when the cell carries none."""
    ia = min(max(bisect.bisect_right(v.lnps, x) - 1, 0), len(v.lnps) - 2)
    ib = min(max(bisect.bisect_right(v.ts, t) - 1, 0), len(v.ts) - 2)
    tot, any_ = 0.0, False
    for key in ("interp_terms", "loop_terms"):
        cells = v._terms[key][0]
        e = cells.get((ia, ib)) if cells else None
        if e and e[0]:
            tot, any_ = tot + abs(e[0]), True
    return tot if any_ else None


def gate(v, jumps):
    """r2's swap rulings applied (68 addenda 2, r2 addendum 1, bbcbcd23), per downward jump: (STOP list, exceptions).
    row-located: |ΔG| > TP_TOL, a side unconverged, or a composition change → STOP; else |Δρ/ρ| ≤ the cell's ρ band →
    «a record defect within its band» (a declared exception), above it → record STOP. extension band: «record STOP» or
    «read-extension STOP» verdicts STOP; a read-extension step is listed with its band comparison (68 / directing's
    call). A jump not evaluated (no generator) is a STOP: the gate can't be passed unread."""
    stops, exceptions = [], []
    for j in jumps:
        if j["jump"] >= 0.0 or j.get("zero_height"):     # rev3c §3.6: a zero-height case is not gated
            continue
        if j.get("pre_gate_stop"):
            continue                                     # rev3c §2: a failing coincident pair STOPped before the gate
        band = _band_rho(v, j["x"], j["t"])
        j["band_rho"] = band
        within = band is not None and abs(j["rel"]) <= band
        verdict = j.get("verdict", "not evaluated")
        if j.get("class") == "row-located":
            if verdict != "within TP_TOL" or not j.get("composition_same", False):
                stops.append({**j, "gate": verdict})
            elif within:
                # r2 m2 (fc64f79e): with ΔV ≤ 0 at P_b the equilibria step upward, so the downward jump is the read's
                exceptions.append({**j, "gate": ("a read defect within its band" if (j.get("dv_at_pb") or 0.0) <= 0.0
                                                 else "a record defect within its band")})
            else:
                stops.append({**j, "gate": "record STOP: |Δρ/ρ| above the cell's ρ band"})
        elif verdict.startswith("read-extension step"):
            exceptions.append({**j, "gate": "read-extension step, " + ("within" if within else "above") + " the band"})
        else:
            stops.append({**j, "gate": verdict})
    return stops, exceptions


def _coincident_edge_census(jumps, g_stops, g_exc):
    """Directing 10-20 (r2 e843daa8): the coincident-edge «swaps» met — jumps, their gate verdicts, how many on their own
    rows (a true crossing) and how far their P_b is extrapolated past them."""
    ce = [j for j in jumps if j.get("coincident_edge")]
    key = lambda j: (j["t"], j["x"], j["curve"])          # noqa: E731
    stop_k, exc_k = {key(j) for j in g_stops if "curve" in j}, {key(j) for j in g_exc}
    down = [j for j in ce if j["jump"] < 0.0]
    zero = [j for j in down if j.get("zero_height")]
    classes = {}
    for j in down:
        classes[j.get("class", "not evaluated")] = classes.get(j.get("class", "not evaluated"), 0) + 1
    return {"n": len(ce), "curves": sorted({j["curve"] for j in ce}), "upward": len(ce) - len(down),
            "downward": len(down), "downward_by_class": classes,
            # rev3c §3.7 (68 n1 on bf370f23): the STOPs, before the gate (pre_gate_stop) or in it (no τ_e); «above
            # EDGE_DRHO_TOL» only where τ_e was compared, on the pair's own row
            "gate_stops": sum(1 for j in down if j.get("pre_gate_stop") or key(j) in stop_k),
            "gate_exceptions": sum(1 for j in down if key(j) in exc_k),
            "zero_height": len({(tuple(j["pair"]), j["t"], round(j["x"], 12)) for j in zero}),
            "above_tol": sum(1 for j in down if j.get("pre_gate_stop") and j["extrap_k"] == 0.0),
            "on_rows": sum(1 for j in ce if j["extrap_k"] == 0.0), "extrapolated": sum(1 for j in ce if j["extrap_k"] > 0.0),
            "extrap_k_max": max((j["extrap_k"] for j in ce), default=None),
            "rel_range": [min((j["rel"] for j in ce), default=None), max((j["rel"] for j in ce), default=None)],
            "abs_jump_max": max((abs(j["jump"]) for j in ce), default=None)}


def _zero_height_list(jumps):
    """rev3c §3.7: one entry per zero-height case, keyed by (pair, T, ln P to 1e-12), with n the (sample × member) rows
    it merges."""
    by = {}
    for j in jumps:
        if not j.get("zero_height"):
            continue
        k = (tuple(j["pair"]), j["t"], round(j["x"], 12))
        e = by.setdefault(k, {"pair": list(j["pair"]), "t": j["t"], "x": j["x"], "p_gpa": math.exp(j["x"]) / 1e9,
                              "jump": j["jump"], "rel": j["rel"], "tol": j["tol"], "n": 0})
        e["n"] += 1
    return sorted(by.values(), key=lambda e: (e["t"], e["x"], e["pair"]))


def _caps_summary(caps):
    """rev3d amendment 1's stamp lines: the rule, τ_w's range over banded capped ends, and how many sit at the table's
    floor τ_w (the smallest banded value, the term floor's band)."""
    taus = sorted(c["tau_w"] for c in caps)
    if not taus:
        return {"tau_w_rule": TAU_W_RULE, "tau_w_range": None, "tau_w_floor_ends": 0, "capped_ends": 0}
    lo = taus[0]
    return {"tau_w_rule": TAU_W_RULE, "tau_w_range": {"min": lo, "median": taus[len(taus) // 2], "max": taus[-1]},
            "tau_w_floor_ends": sum(1 for x in taus if x == lo), "capped_ends": len(taus),
            "at_ceiling": sum(1 for c in caps if c["at_limit"])}


def _sliver_margin(slivers):
    if not slivers:
        return {"refined": 0}
    dips = [s_ for s_ in slivers if s_["dip_points"]]
    narrow = min(dips, key=lambda s_: s_["dip_span"]) if dips else None
    return {"refined": len(slivers), "widest_gap": max(s_["gap"] for s_ in slivers), "W_S": W_S, "N_S": N_S,
            "dips": len(dips), "narrowest_dip": narrow,
            "under_two_subcells": [s_ for s_ in dips if s_["dip_span"] < 2.0 * s_["gap"] / N_S]}


def document(v, per_cell):
    jumps = [j for c in per_cell.values() for smp in c for j in smp["swap_jumps"]]
    dropped, clip_stops = [], []
    caps = [c_ for c in per_cell.values() for smp in c for c_ in smp.get("caps", ())]
    no_band = [c_ for c in per_cell.values() for smp in c for c_ in smp.get("no_band", ())]
    widened = [j for c in per_cell.values() for smp in c for j in smp.get("widened", ())]
    slivers = [s_ for c in per_cell.values() for smp in c for s_ in smp.get("slivers", ())]
    g_stops, g_exc = gate(v, jumps)
    zh = _zero_height_list(jumps)
    unscreened = [u for c in per_cell.values() for smp in c for u in smp["unscreened"]]
    return {"record": v.material_id, "ps": list(v.ps), "ts": list(v.ts),
            "stamp": {**_stamp(edge_tol=_view_tol(v)), **{k: x for k, x in _caps_summary(caps).items()
                                                          if k in ("tau_w_rule", "tau_w_range", "tau_w_floor_ends")},
                      "no_band_ends": len(no_band), "record_sha256": v.record["assemblage"]["sha256"],
                      "record_yaml_sha256": _ma().record_yaml_sha256(v.material_id), "read_blob": _ma().read_blob()},
            "sets": {str(k): s for k, s in sets_from(v, per_cell, dropped, clip_stops).items()},
            # rev3d D1: interval ends clipped or dropped because they don't read at every sample under its cell's stencil
            "unreadable_end": dropped,
            # rev3d D4: every capped end (τ_w per cell, amendment 1), the ends with no ρ band, and rule 1's excess above
            # the regain end's τ_w, by name
            "caps_summary": _caps_summary(caps),
            "no_band_end": no_band,
            "widen_excess": [w for w in widened if w.get("excess") is not None and w["excess"] > (w.get("tau_w") or 0.0)],
            # rev3d §5 (r2 n1): the sliver margin, the widest refined gap and the narrowest dip D3 found
            "sliver_margin": _sliver_margin(slivers),
            "unrecovered": [u for c in per_cell.values() for smp in c for u in smp["unrecovered"]],
            # every STOP: the samples' own (net fall, unresolved, a refusal inside a fall search) and the swap gate's
            "stops": [s_ for c in per_cell.values() for smp in c for s_ in smp["stops"]] + g_stops + clip_stops,
            "swap_exceptions": g_exc,
            "swap_counts": {"row-located": sum(1 for j in jumps if j["jump"] < 0 and j.get("class") == "row-located"),
                            "extension band": sum(1 for j in jumps if j["jump"] < 0 and j.get("class") == "extension band"),
                            "upward": sum(1 for j in jumps if j["jump"] >= 0), "zero_height": len(zh)},
            "zero_height": zh,
            "edge_tol": _view_tol(v) if _view_tol(v) is not None else "no edge_drho_tol",       # rev3c §2
            "unreadable_points": sum(smp["unreadable"] for c in per_cell.values() for smp in c),
            "unscreened_cells": unscreened[:500], "unscreened_count": len(unscreened),
            "samples": sum(len(c) for c in per_cell.values()),
            # listed per ln P position (1e-7), each with its sample count and T range: a P node's kink recurs at every T
            "floor_cells": _floor_list([f_ for c in per_cell.values() for smp in c for f_ in smp["floor_cells"]]),
            "swap_jumps": [j for c in per_cell.values() for smp in c for j in smp["swap_jumps"]],
            # swap extension note 1: the reach-0 holding-row steps met (upward: landed; downward: bridged)
            "row_steps": [j for c in per_cell.values() for smp in c for j in smp.get("row_steps", ())],
            # r2 a69976dc: net falls regained by widening (rule 1) and absorbed by a landed step's jump (rule 2)
            "widened": [j for c in per_cell.values() for smp in c for j in smp.get("widened", ())],
            "absorbed": [j for c in per_cell.values() for smp in c for j in smp.get("absorbed", ())],
            # r2 8e0d13fa: widened ends clipped at a refusal boundary (class 3), and floor cells accepted on the fall
            # line with R decreasing (class 2), each with its secant
            "clipped": [j for c in per_cell.values() for smp in c for j in smp.get("clipped", ())],
            "slow_floor": [j for c in per_cell.values() for smp in c for j in smp.get("slow_floor", ())],
            "coincident_edge": _coincident_edge_census(jumps, g_stops, g_exc)}


# n4 (r2): floor cells are listed per 1e-7 ln P, so kinks closer than that share a row.

# ── the unitq job: one unit per T cell ──
_V = {}


def setup(argv):
    if argv[0] not in _V:
        _V[argv[0]] = _view(argv[0])
    v = _V[argv[0]]
    return {"units": [(["ib", ib], {"rid": argv[0], "ib": ib}) for ib in range(len(v.ts) - 1)]}


def identity(argv):
    return {"record": argv[0], **_stamp(), "read_blob": _ma().read_blob()}   # parts of one build share one read


def run(payload):
    if payload["rid"] not in _V:
        _V[payload["rid"]] = _view(payload["rid"])
    return cell_falls(_V[payload["rid"]], payload["ib"])


def plan(state, results):
    todo = [(k, p) for k, p in state["units"] if canon(k) not in results]  # noqa: F821 (set by unitq)
    if todo:
        return todo
    rid = state["units"][0][1]["rid"]
    if rid not in _V:
        _V[rid] = _view(rid)
    per_cell = {p["ib"]: results[canon(k)] for k, p in state["units"]}  # noqa: F821
    doc = document(_V[rid], per_cell)
    return {"files": {f"{rid}.json": json.dumps(doc) + "\n"}}


def main(argv):
    rid, out = argv[0], argv[1]
    cells = [int(x) for x in argv[argv.index("--cells") + 1].split(":")] if "--cells" in argv else None
    xr = [math.log(float(x) * 1e9) for x in argv[argv.index("--p") + 1].split(":")] if "--p" in argv else None
    nsub = int(argv[argv.index("--nsub") + 1]) if "--nsub" in argv else 16
    v = _view(rid)
    rng = range(len(v.ts) - 1) if cells is None else range(cells[0], cells[1] + 1)
    per_cell = {ib: cell_falls(v, ib, nsub, xr) for ib in rng}
    doc = document(v, per_cell)
    doc["partial"] = {"cells": cells, "p_gpa": None if xr is None else [math.exp(z) / 1e9 for z in xr]}
    json.dump(doc, open(out, "w"))
    print(rid, "samples", doc["samples"], "sets", {k: len(s) for k, s in doc["sets"].items()},
          "unrecovered", len(doc["unrecovered"]), "stops", len(doc["stops"]), "floor_cells", sum(e["n"] for e in doc["floor_cells"]), "at", len(doc["floor_cells"]), "positions",
          "swap jumps", len(doc["swap_jumps"]), "down", sum(j["jump"] < 0 for j in doc["swap_jumps"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
