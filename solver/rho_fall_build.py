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
- **Net-fall STOP:** at the sample, R(b′) < R(a′) for a widened interval.
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
    for xs_, _c in swaps:
        grid += [xs_ - SWAP_EPS, xs_ + SWAP_EPS]
    grid = sorted({x for x in grid if xlo <= x <= xhi})
    vals = [g(x) for x in grid]
    falling = []                                         # points where g < THR
    floor_cells = []                                     # cells accepted at H_MIN (rising ends, R not falling)
    swap_jumps = []                                      # every swap's jump at t (68 addendum 1: listed, never bridged)
    for xs_, cid in swaps:
        lo_r, hi_r = g(xs_ - SWAP_EPS), g(xs_ + SWAP_EPS)
        if lo_r is not None and hi_r is not None:
            swap_jumps.append({"t": t, "x": xs_, "curve": cid, "r_before": lo_r[0], "r_after": hi_r[0],
                               "jump": hi_r[0] - lo_r[0], "rel": (hi_r[0] - lo_r[0]) / lo_r[0]})

    def across_swap(a, b):
        return any(a < xs_ < b for xs_, _c in swaps)

    def slope(i):
        if vals[i] is None or vals[i + 1] is None:
            return 0.0
        return abs(vals[i + 1][1] - vals[i][1]) / (grid[i + 1] - grid[i])

    def screen(a, b, fa, fb, m_est, depth=0):
        if fa is None or fb is None:
            unscreened.append({"t": t, "a": a, "b": b})
            return
        if across_swap(a, b) and b - a <= 2.0 * SWAP_EPS * (1.0 + 1e-6):
            return                                       # the swap's own jump: listed above, not a fall
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
            # addendum 1, question B); one whose R falls is a STOP
            if fa[1] >= THR and fb[1] >= THR and fb[0] >= fa[0]:
                floor_cells.append({"t": t, "x": a})
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
        while True:
            q = g(a - step)
            if q is None or a - step < left:
                a = max(a - step, left) if q is not None else a
                break
            if q[1] >= 0.0:
                a = _bisect(lambda z: gv(z)[1], a - step, a, q[1])
                break
            a -= step
        e = xf                                           # the end of the falling run: g back above 0
        while True:
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
        lo_, hi_ = max(a - C_WIDEN * ext, left), min(c + C_WIDEN * ext, right)
        seen.append((a, c))
        r_lo, r_hi = g(lo_), g(hi_)
        if r_lo is None or r_hi is None:
            stops.append({"t": t, "why": "a widened end the read can't evaluate", "a": lo_, "b": hi_})
            continue
        if r_hi[0] < r_lo[0]:
            stops.append({"t": t, "why": "net fall over the widened interval", "a": lo_, "b": hi_,
                          "r_a": r_lo[0], "r_b": r_hi[0]})
        intervals.append((lo_, hi_, a, c))
    return intervals, unrecovered, stops, floor_cells, swap_jumps, {"unreadable": sorted(set(unreadable)),
                                                                   "unscreened": unscreened}


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
            ivs, un, st, fl, sj, ur = [], [], [{"t": t, "why": str(e)}], [], [], {"unreadable": [], "unscreened": []}
        for j_ in sj:
            j_["v_ratio"] = j_["r_after"] / j_["r_before"]          # V₋/V₊ at one mass: ρ₊/ρ₋
            if j_["jump"] < 0.0:
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
                    "swap_jumps": sj, "unreadable": len(ur["unreadable"]), "unscreened": ur["unscreened"]})
    return out


def sets_from(v, per_cell):
    """S_i = the merged widened intervals of every sample in cells i − 1 and i."""
    sets = {}
    for i in range(len(v.ts)):
        ivs = [(iv[0], iv[1]) for ib in (i - 1, i) for smp in per_cell.get(ib, ()) for iv in smp["intervals"]]
        if ivs:
            sets[i] = _merge(ivs)
    return sets


def _view(rid):
    from solver import material_registry as mr, material_assemblage as ma
    from solver.from_v1 import thaw
    reg = mr.load()
    return ma.view(thaw(reg.get(rid)), reg.tables[rid], 1600.0)


def _stamp():
    import hashlib
    import subprocess
    from pathlib import Path
    data = Path(__file__).read_bytes()
    eng = Path(__file__).resolve().parents[1]
    return {"tool_blob": hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(),
            "engine": subprocess.run(["git", "-C", str(eng), "rev-parse", "HEAD"], capture_output=True,
                                     text=True).stdout.strip(),
            "rules": {"THR": THR, "SUB_P": SUB_P, "SAFETY": SAFETY, "H_MIN": H_MIN, "C_WIDEN": C_WIDEN, "REGAIN_W": REGAIN_W}}


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
        if j["jump"] >= 0.0:
            continue
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


def document(v, per_cell):
    jumps = [j for c in per_cell.values() for smp in c for j in smp["swap_jumps"]]
    g_stops, g_exc = gate(v, jumps)
    unscreened = [u for c in per_cell.values() for smp in c for u in smp["unscreened"]]
    return {"record": v.material_id, "ps": list(v.ps), "ts": list(v.ts), "stamp": _stamp(),
            "sets": {str(k): s for k, s in sets_from(v, per_cell).items()},
            "unrecovered": [u for c in per_cell.values() for smp in c for u in smp["unrecovered"]],
            # every STOP: the samples' own (net fall, unresolved, a refusal inside a fall search) and the swap gate's
            "stops": [s_ for c in per_cell.values() for smp in c for s_ in smp["stops"]] + g_stops,
            "swap_exceptions": g_exc,
            "swap_counts": {"row-located": sum(1 for j in jumps if j["jump"] < 0 and j.get("class") == "row-located"),
                            "extension band": sum(1 for j in jumps if j["jump"] < 0 and j.get("class") == "extension band"),
                            "upward": sum(1 for j in jumps if j["jump"] >= 0)},
            "unreadable_points": sum(smp["unreadable"] for c in per_cell.values() for smp in c),
            "unscreened_cells": unscreened[:500], "unscreened_count": len(unscreened),
            "samples": sum(len(c) for c in per_cell.values()),
            # listed per ln P position (1e-7), each with its sample count and T range: a P node's kink recurs at every T
            "floor_cells": _floor_list([f_ for c in per_cell.values() for smp in c for f_ in smp["floor_cells"]]),
            "swap_jumps": [j for c in per_cell.values() for smp in c for j in smp["swap_jumps"]]}


# n4 (r2): floor cells are listed per 1e-7 ln P, so kinks closer than that share a row.

# ── the unitq job: one unit per T cell ──
_V = {}


def setup(argv):
    if argv[0] not in _V:
        _V[argv[0]] = _view(argv[0])
    v = _V[argv[0]]
    return {"units": [(["ib", ib], {"rid": argv[0], "ib": ib}) for ib in range(len(v.ts) - 1)]}


def identity(argv):
    return {"record": argv[0], **_stamp()}


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
