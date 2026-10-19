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


def swap_gibbs(v, curve_id, t, p_b):
    """68 addendum 2 (r2 ruling ce571b67): at a downward swap jump, the generator's G per atom of the swap's two
    assemblages at (P_b, T): ΔG = G₊ − G₋ (J/mol·atom), with the generator's own tangent-plane tolerance TP_TOL. The
    sides' labels are the curve's nearest row's. None for both when the generator module is not given."""
    m = _builder()
    row = v._events[curve_id].nearest(t)
    out = {"left": row["left_label"], "right": row["right_label"], "g_left": None, "g_right": None, "dg": None,
           "tol": None, "composition_same": True,
           "composition_why": "one bulk per record: both sides are equilibria of the same bulk"}
    if m is None:
        return out
    comp = v.material_id.removeprefix("silicate_slb_")
    bulk = m.atomic_bulk(m.COMPOSITIONS[comp]["oxides_wt"])
    import numpy as np
    with np.errstate(all="raise"):
        res = m.equilibrate_node(bulk, p_b, t, {})
    kl, kr = m.canon_key(row["left_label"]), m.canon_key(row["right_label"])
    gl, gr = (res.get(kl) or {}).get("g_atom"), (res.get(kr) or {}).get("g_atom")
    out.update(g_left=gl, g_right=gr, dg=None if gl is None or gr is None else gr - gl, tol=m.TP_TOL,
               candidates=sorted(res))
    return out


def _reader(v, t, ib):
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
        except Exception:                                # a corner with no run, a missing cell: no value
            got = None
        finally:
            v._in_bridge = was
            del v.notes[n:]
            v.cut_counts.clear()
            v.cut_counts.update(counts)
            v._marks, v._read_memo = marks, memo_r
        if got is None or isinstance(got, stp.Stop):
            out = None
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
    g = _reader(v, t, ib)
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
        step = (grid[1] - grid[0]) / 4.0 if len(grid) > 1 else 1e-4
        a = xf
        while True:
            q = g(a - step)
            if q is None or a - step < left:
                a = max(a - step, left) if q is not None else a
                break
            if q[1] >= 0.0:
                a = _bisect(lambda z: (g(z) or (0, 1))[1], a - step, a, q[1])
                break
            a -= step
        e = xf                                           # the end of the falling run: g back above 0
        while True:
            q = g(e + step)
            if q is None or e + step > right:
                break
            if q[1] >= 0.0:
                e = _bisect(lambda z: (g(z) or (0, 1))[1], e, e + step, -1.0)
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
                c = _bisect(lambda z: (g(z) or (ra[0], 0))[0] - ra[0], x, x + step, (g(x) or (ra[0] - 1, 0))[0] - ra[0])
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
    return intervals, unrecovered, stops, floor_cells, swap_jumps


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
            ivs, un, st, fl, sj = falls_at(v, t, ib, xlo, xhi)
        except Unresolved as e:
            ivs, un, st, fl, sj = [], [], [{"t": t, "why": str(e)}], [], []
        for j_ in sj:
            j_["v_ratio"] = j_["r_after"] / j_["r_before"]          # V₋/V₊ at one mass: ρ₊/ρ₋
            if j_["jump"] < 0.0:
                try:
                    j_.update(swap_gibbs(v, j_["curve"], t, math.exp(j_["x"])))
                except Exception as e:                   # an equilibration that fails is recorded, not a crash
                    j_["gibbs_error"] = f"{type(e).__name__}: {str(e)[:200]}"
        out.append({"t": t, "intervals": [list(iv) for iv in ivs], "unrecovered": un, "stops": st, "floor_cells": fl,
                    "swap_jumps": sj})
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


def document(v, per_cell):
    return {"record": v.material_id, "ps": list(v.ps), "ts": list(v.ts), "stamp": _stamp(),
            "sets": {str(k): s for k, s in sets_from(v, per_cell).items()},
            "unrecovered": [u for c in per_cell.values() for smp in c for u in smp["unrecovered"]],
            "stops": [s_ for c in per_cell.values() for smp in c for s_ in smp["stops"]],
            "samples": sum(len(c) for c in per_cell.values()),
            # listed per ln P position (1e-7), each with its sample count and T range: a P node's kink recurs at every T
            "floor_cells": _floor_list([f_ for c in per_cell.values() for smp in c for f_ in smp["floor_cells"]]),
            "swap_jumps": [j for c in per_cell.values() for smp in c for j in smp["swap_jumps"]]}


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
