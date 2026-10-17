# 광물 집합 뷰의 내보낸 경계 시험 — 한쪽 스텐실(P 먼저), 스텐실 폭, 기운 곡선, 계단·변 보정·한 칸 여럿, 표지 규칙, 모서리 행, 적재 검사, 전이 이벤트 (경계 내보내기 범위 노트 b0057863 §3–§4)
"""Tests of the exported-boundary support in AssemblageView (rewrite/boundary-export-scope.frozen.md, artifacts 41675349;
registration §3.2–§3.3). A synthetic table carries two label regions with a planted ρ offset on the right side, so a
read that crosses the curve is visibly wrong; each test plants one thing.

Run from the worktree root:  <solver venv>/python -m unittest solver.tests.test_assemblage_boundaries
"""
import copy
import math
import unittest

from solver import events
from solver import material_assemblage as ma
from solver import stepper as st
from solver.tests.test_assemblage_view import PS, TS, record, rho_of

OFF = 0.02                                   # the right side's planted ρ offset (relative)


def pb_const(t):
    return math.sqrt(PS[15] * PS[16])        # between columns 15 and 16 at every T


def pb_slope(t):
    """Sloped: between columns 13/14 at 1000 K and 17/18 at 1400 K (it crosses read cells diagonally)."""
    a, b = math.log(math.sqrt(PS[13] * PS[14])), math.log(math.sqrt(PS[17] * PS[18]))
    w = min(max((t - 1000.0) / 400.0, 0.0), 1.0)
    return math.exp(a + w * (b - a))


def table(pb=pb_const, left="ol+opx", right="wa+opx", cls="swap", t_end=None, third=None, edges=None,
          off=OFF, t_lo=1000.0, t_hi=1400.0, tops=None, p_dataset=None):
    """Cells to 1600 K, non-frozen from 400 K; the label is `left` below P_b(t) and `right` above it for
    t_lo ≤ t ≤ t_hi (outside, `left` everywhere, or `third` above t_end). Rows of the exported block at every T row
    where the two neighbouring columns of P_b differ in label."""
    cells, cols, rows = [], [], []
    ts = [t for t in TS if t <= 1600.0]
    tops = tops or {}
    for i, p in enumerate(PS):
        for t in ts:
            if t > tops.get(i, ts[-1]):
                continue
            fr = t < 400.0
            lab = left
            inside = t_lo <= t <= t_hi and (t_end is None or t <= t_end)
            if inside and p > pb(t):
                lab = right
            if third is not None and t_end is not None and t > t_end and t_lo <= t <= t_hi and p > pb(t):
                lab = third                                   # the right side's label changes past the curve's end
            r = rho_of(p, t) * (1.0 + off if lab == right else 1.0)
            c = {"p": p, "t": t, "kind": "frozen" if fr else "equilibrium", "assemblage": lab, "rho": r,
                 "c_p": 1200.0 + 0.1 * t, "dtdp_s": 1e-8 * t / 1000.0, "freeze_t": 400.0 if fr else None,
                 "freeze_class": "convergence edge" if fr else None, "dtdp_eq_band": None if fr else 2.5e-4}
            c["dtdp_eq"] = c["dtdp_s"]
            c["c_p_eq"] = None if fr else c["c_p"] * 1.03
            cells.append(c)
        top = tops.get(i, ts[-1])
        cols.append({"p": p, "t_sol": 1500.0, "t_window_top": top,
                     "window": {"cause": "grid_end"} if top == ts[-1] else {"cause": "eos_edge", "phase": "opx"}})
    for t in ts:
        if not (t_lo <= t <= t_hi) or (t_end is not None and t > t_end) or t < 400.0:
            continue
        j = max(i for i in range(len(PS) - 1) if PS[i] < pb(t))
        row = {"t": t, "p_lo": PS[j], "p_hi": PS[j + 1], "left": left, "right": right, "class": cls,
               "converged": True}
        if cls == "swap":
            row.update(p_b=pb(t), delta_rho=off, delta_s=1.0)
        else:
            row["edges"] = edges(t) if edges else [{"phase": "gt", "p_b": pb(t), "p_b_driving_force": pb(t),
                                                    "p_b_amount": pb(t), "converged": True, "location_error": 0.0,
                                                    "by_amount_only": False, "delta_rho": off,
                                                    "over_tolerance": True}]
        rows.append(row)
    return {"cells": cells, "columns": cols, "p_dataset": p_dataset or PS[-3],
            "boundaries": {"status": "exported", "rows": rows}}


def view(tb):
    return ma.view(record(tb["p_dataset"]), tb, 1600.0)


def solid(v, p, t):
    got = v._solid(p, t)
    assert not isinstance(got, st.Stop), got
    return got


def rel(a, b):
    return abs(a / b - 1.0)


def tb_cell(tb, p, t):
    return next(c for c in tb["cells"] if (c["p"], c["t"]) == (p, t))


#: refusal boundaries met by the scans (a step into a refusal is not a jump; 68: listed by class)
REFUSED = []


def jumps_p(v, ts_, n=12, tol=1e-6):
    """Off-event steps of ρ along P at each T of ts_ ((R1) acceptance, 68's probe_ev2 form): n samples per cell, a pair
    departing from its neighbours bisected to 1e-12 in ln P, kept if |Δρ/ρ| > tol and not at a cut swap's P_b_ext(t).
    Refused reads are skipped (refusal boundaries are tested by class elsewhere)."""
    out = []
    for t in ts_:
        xs = []
        for ia in range(len(v.ps) - 1):
            if v.ps[ia + 1] > v.p_dataset:
                break
            xl, xh = v.lnps[ia], v.lnps[ia + 1]
            xs += [xl + (xh - xl) * (i + 0.5) / n for i in range(n)] + [xh]
        vals = [v._solid(math.exp(x), t) for x in xs]
        vals = [None if isinstance(g, st.Stop) else g[0] for g in vals]
        d = [None if None in (vals[i], vals[i + 1]) else vals[i + 1] / vals[i] - 1 for i in range(len(xs) - 1)]
        for i, di in enumerate(d):
            if di is None:
                continue
            nb = [z for z in (d[i - 1] if i else None, d[i + 1] if i + 1 < len(d) else None) if z is not None]
            if abs(di - (sum(nb) / len(nb) if nb else 0.0)) < tol:
                continue
            lo, hi = xs[i], xs[i + 1]
            refused = None
            while hi - lo > 1e-12:
                m = 0.5 * (lo + hi)
                g = [v._solid(math.exp(z), t) for z in (lo, m, hi)]
                if any(isinstance(q, st.Stop) for q in g):
                    refused = next(q for q in g if isinstance(q, st.Stop)).record.why
                    break
                a, b, c = (q[0] for q in g)
                if abs(b / a - 1) >= abs(c / b - 1):
                    hi = m
                else:
                    lo = m
            if refused is not None:
                REFUSED.append((t, math.exp(lo), refused))
                continue
            a, c = v._solid(math.exp(lo), t)[0], v._solid(math.exp(hi), t)[0]
            if abs(c / a - 1) <= tol:
                continue
            x = 0.5 * (lo + hi)
            if any(cc.kind == "swap" and (q := cc.p_b_ext(t, v._reach)) is not None and abs(math.log(q) - x) < 1e-9
                   for cc in v._cut):
                continue
            out.append((t, math.exp(x), abs(c / a - 1)))
    return out


def jumps_t(v, ps_, n=6, tol=1e-6):
    """Off-event steps of ρ along T at each P of ps_: n samples per T cell plus each row line ± 1e-7 K, bisected to
    1e-10 K, kept if |Δρ/ρ| > tol and not where a cut swap's P_b_ext(t) = P."""
    out = []
    for p in ps_:
        ts_ = []
        for k in range(len(v.ts) - 1):
            a, b = v.ts[k], v.ts[k + 1]
            ts_ += [a + 1e-7] + [a + (b - a) * (i + 0.5) / n for i in range(n)] + [b - 1e-7]
        vals = [v._solid(p, t) for t in ts_]
        vals = [None if isinstance(g, st.Stop) else g[0] for g in vals]
        d = [None if None in (vals[i], vals[i + 1]) else vals[i + 1] / vals[i] - 1 for i in range(len(ts_) - 1)]
        for i, di in enumerate(d):
            if di is None:
                continue
            nb = [z for z in (d[i - 1] if i else None, d[i + 1] if i + 1 < len(d) else None) if z is not None]
            if abs(di - (sum(nb) / len(nb) if nb else 0.0)) < tol:
                continue
            lo, hi = ts_[i], ts_[i + 1]
            refused = None
            while hi - lo > 1e-10:
                m = 0.5 * (lo + hi)
                g = [v._solid(p, z) for z in (lo, m, hi)]
                if any(isinstance(q, st.Stop) for q in g):
                    refused = next(q for q in g if isinstance(q, st.Stop)).record.why
                    break
                a, b, c = (q[0] for q in g)
                if abs(b / a - 1) >= abs(c / b - 1):
                    hi = m
                else:
                    lo = m
            if refused is not None:
                REFUSED.append((p, lo, refused))
                continue
            a, c = v._solid(p, lo)[0], v._solid(p, hi)[0]
            if abs(c / a - 1) <= tol:
                continue
            t = 0.5 * (lo + hi)
            if any(cc.kind == "swap" and (q := cc.p_b_ext(t, v._reach)) is not None and abs(q / p - 1) < 1e-6
                   for cc in v._cut):
                continue
            out.append((p, t, abs(c / a - 1)))
    return out


class OneSided(unittest.TestCase):
    """§3 (b) as (R1) builds it: a read takes each stencil row's region on its side of every cut curve; the planted
    control (the cut disabled) reads across and fails."""

    def test_reads_stay_on_their_side(self):
        tb = table()
        v = view(tb)
        p_b, t = pb_const(1200.0), 1210.0
        left, right = p_b * 0.999, p_b * 1.001
        self.assertLess(rel(solid(v, left, t)[0], rho_of(left, t)), 1e-4)
        self.assertLess(rel(solid(v, right, t)[0], rho_of(right, t) * (1 + OFF)), 1e-4)
        v0 = view(tb)
        v0._cut, v0._parts, v0._runcache = [], {}, {}           # planted control: the cut disabled
        self.assertGreater(rel(solid(v0, left, t)[0], rho_of(left, t)), 1e-3)

    def test_span_one_cell_away(self):
        """68 M3: a read one cell left of the curve's cell takes no right-side node. The pin is 2e-5, not 1e-5: the run's
        end node takes the gentler of its PCHIP end slope and the gentlest secant (item 5d998d40, 68 ruling 2), which
        reads this end cell 1.7e-5 from the analytic ρ, inside the declared interpolation term (owner-direction
        85f41c2b). That pin no longer separates the mutant (the cut disabled reads 1.1e-5 here), so the right side is
        moved a further 5 %: the read is bit-identical, and the mutant's moves."""
        tb = table()
        v = view(tb)
        p, t = math.sqrt(PS[14] * PS[15]), 1210.0
        self.assertLess(rel(solid(v, p, t)[0], rho_of(p, t)), 2e-5)
        tb2 = copy.deepcopy(tb)                                   # the right side moved further: the read is unmoved
        for c in tb2["cells"]:
            if c["p"] > pb_const(t):
                c["rho"] *= 1.05
        self.assertEqual(solid(view(tb2), p, t)[0], solid(v, p, t)[0])
        v0 = view(tb)
        v0._cut, v0._parts, v0._runcache = [], {}, {}
        self.assertGreater(rel(solid(v0, p, t)[0], rho_of(p, t)), 1e-5)
        v2 = view(tb2)
        v2._cut, v2._parts, v2._runcache = [], {}, {}
        self.assertNotEqual(solid(v2, p, t)[0], solid(v0, p, t)[0])   # the mutant reads the right side

    def test_far_reads_match_cubic2(self):
        """(R1) voids «uncut bit-identical to cubic2» for exported-boundary records (owner e4cd7f01): every read goes P
        first through the row regions. Away from every curve it differs from cubic2 (T first) only by the
        interpolation order (68's measurement): here below 1e-6 relative."""
        tb = table()
        pend = copy.deepcopy(tb)
        pend["boundaries"] = {"status": "pending"}
        v, w = view(tb), view(pend)
        for p in (PS[3] * 1.1, PS[8] * 1.3, PS[24] * 1.2):
            for t in (450.0, 905.0, 1210.0, 1555.0):
                a, b = solid(v, p, t), solid(w, p, t)
                for k in range(3):
                    self.assertLess(rel(a[k], b[k]), 1e-6, (p, t, k))


class Sloped(unittest.TestCase):
    """r2 M1, 68 M1: each row is partitioned at its own P_b(t_k); a read follows its side at its own T."""

    def test_diagonal_cut_answers_one_sided(self):
        tb = table(pb=pb_slope)
        v = view(tb)
        t = 1225.0
        p = pb_slope(t) * 0.97
        self.assertLess(rel(solid(v, p, t)[0], rho_of(p, t)), 1e-3)
        v0 = view(tb)
        v0._cut, v0._parts, v0._runcache = [], {}, {}
        self.assertGreater(rel(solid(v0, p, t)[0], rho_of(p, t)), 1e-3)

    def test_row_regions_at_their_own_t(self):
        """A node's region is decided by its own row's P_b(t_k), never by the read's T."""
        v = view(table(pb=pb_slope))
        for k in range(len(TS)):
            if not 1000.0 <= TS[k] <= 1400.0:
                continue
            for j in range(len(PS) - 3):
                self.assertEqual(v._region_of(j, k), 0 if PS[j] < pb_slope(TS[k]) else 1, (j, TS[k]))


class Steps(unittest.TestCase):
    def test_swap_steps_with_its_note(self):
        tb = table()
        v = view(tb)
        p_b, t = pb_const(1200.0), 1210.0
        a, b = solid(v, p_b * (1 - 1e-9), t)[0], solid(v, p_b * (1 + 1e-9), t)[0]
        self.assertAlmostEqual(b / a - 1.0, OFF, delta=1e-4)
        got = v.state(p_b * 1.0001, t)
        self.assertTrue(any(ma.SWAP_NOTE in n.text for n in got[2]))

    def test_edge_correction(self):
        """r2 Q2 / 68 M4 in the blend form (item 5d998d40, 68 ruling 1): inside the window the read is
        (1 − H)·own + H·far with H the smoothstep over [x_b − w, x_b + w] for ρ, over its central half for dT/dP and c_P
        (BLEND_SHARP); (L + R)/2 at P_b, continuous there and C¹
        (one slope from both sides); the own raw read at and past the window's edge, joined C¹. Mutant: no blend (a
        step stays)."""
        tb = table(cls="edge_in", right="ol+opx+gt")
        v = view(tb)
        t = 1210.0
        p_b = pb_const(t)
        xb = math.log(p_b)
        a, b = solid(v, p_b * (1 - 1e-12), t)[0], solid(v, p_b * (1 + 1e-12), t)[0]
        self.assertLess(rel(a, b), 1e-9)
        ib = int((t - TS[0]) // 50)
        (c,) = v._cut
        L = v._value("rho", xb, t, 15, ib, {c: -1}, False)
        R = v._value("rho", xb, t, 15, ib, {c: 1}, False)
        self.assertGreater(abs(L - R) / L, 1e-3)              # the planted step the blend removes
        self.assertAlmostEqual(a, 0.5 * (L + R), delta=1e-9 * L)
        w = v._width(xb)
        xm = xb - 0.5 * w                                     # H = S(¼) = 5/32
        own = v._value("rho", xm, t, 15, ib, {c: -1}, False)
        far = v._value("rho", xm, t, 15, ib, {c: 1}, False)
        self.assertAlmostEqual(solid(v, math.exp(xm), t)[0], (27.0 / 32.0) * own + (5.0 / 32.0) * far, delta=1e-9 * L)
        xe = xb - w * (1 + 1e-9)
        self.assertEqual(solid(v, math.exp(xe), t)[0], v._value("rho", xe, t, 14, ib, {c: -1}, False))
        for x0 in (xb, xb - w, xb + w):                      # one slope from both sides: C¹ at P_b and the window's ends
            h = 1e-6
            lo = (solid(v, math.exp(x0), t)[0] - solid(v, math.exp(x0 - h), t)[0]) / h
            hi = (solid(v, math.exp(x0 + h), t)[0] - solid(v, math.exp(x0), t)[0]) / h
            self.assertLess(abs(hi - lo), 1e-3 * max(abs(lo), abs(hi)), x0 - xb)
        mut = view(tb)
        for cc in mut._cut:
            cc.kind = "swap"
        self.assertGreater(rel(solid(mut, p_b * (1 - 1e-12), t)[0], solid(mut, p_b * (1 + 1e-12), t)[0]), 1e-3)

    def test_two_curves_in_one_cell(self):
        """r2 Q1, per region: two cut edges in one cell; the region between them holds no node, so each row reads it
        between its neighbours' values at the two curves (a smoothstep in ln P, item 5d998d40 (c)), with MULTI_NOTE;
        the two windows blend it with the side reads (68 ruling 1). Continuous at both curves, and the read between
        them lies between the reads just outside them."""
        def edges(t):
            a, b = math.exp(math.log(PS[15]) + 0.3 * (math.log(PS[16]) - math.log(PS[15]))), \
                math.exp(math.log(PS[15]) + 0.7 * (math.log(PS[16]) - math.log(PS[15])))
            e = {"converged": True, "location_error": 0.0, "by_amount_only": False, "delta_rho": None}
            return [{**e, "phase": "ol", "p_b": a, "p_b_driving_force": a, "p_b_amount": a},
                    {**e, "phase": "wa", "p_b": b, "p_b_driving_force": b, "p_b_amount": b}]
        tb = table(cls="swap_two_edges", edges=edges)
        v = view(tb)
        t = 1200.0
        xa, xb = (math.log(e["p_b"]) for e in edges(t))
        va, vb = solid(v, math.exp(xa) * (1 - 1e-12), t)[0], solid(v, math.exp(xb) * (1 + 1e-12), t)[0]
        for f in (0.25, 0.5, 0.75):
            got = solid(v, math.exp(xa + f * (xb - xa)), t)[0]
            self.assertTrue(min(va, vb) <= got <= max(va, vb), (f, got, va, vb))
        self.assertLess(rel(solid(v, math.exp(xa) * (1 + 1e-12), t)[0], va), 1e-9)   # continuous at both curves
        self.assertLess(rel(solid(v, math.exp(xb) * (1 - 1e-12), t)[0], vb), 1e-9)
        got = v.state(math.exp(xa + 0.25 * (xb - xa)), t)
        self.assertTrue(any(ma.MULTI_NOTE in getattr(n, "text", "") for n in got[2]))

class Ends(unittest.TestCase):
    """(R1) §4 (68 (a)): a cut curve's P_b is extended two T rows past each end for sides and events; rows past the
    real end are not partitioned (read across). The read stays continuous through the end in P and T."""

    def test_closing_edge_continuous_through_the_end(self):
        tb = table(cls="edge_in", right="ol+opx+gt")         # the gt field ends at 1400 K
        v = view(tb)
        self.assertEqual(jumps_p(v, (1385.0, 1410.0, 1460.0, 1499.0)), [])
        self.assertEqual(jumps_t(v, (pb_const(1400.0) * 1.003, pb_const(1400.0) * 0.997)), [])
        p = pb_const(1400.0) * 1.003
        self.assertLess(rel(solid(v, p, 1560.0)[0], rho_of(p, 1560.0)), 1e-6)   # past the reach: read across

    def test_swap_past_its_end_steps_at_the_extension(self):
        """A swap ending at 1250 K: past the end the step lands at P_b_ext(t) and fades with the partitioned rows'
        T weight; no other step anywhere (68 B1)."""
        tb = table(t_end=1250.0, third="cpx+opx")
        v = view(tb)
        (c,) = v._cut
        for t in (1275.0, 1325.0):
            q = c.p_b_ext(t, v._reach)
            a, b = solid(v, q * (1 - 1e-9), t)[0], solid(v, q * (1 + 1e-9), t)[0]
            self.assertGreater(rel(a, b), 1e-6)
        self.assertIsNone(c.p_b_ext(1360.0, v._reach))
        self.assertEqual(jumps_p(v, (1230.0, 1260.0, 1290.0, 1340.0, 1380.0)), [])
        self.assertEqual(jumps_t(v, (pb_const(1200.0) * 0.99, pb_const(1200.0) * 1.01, PS[18] * 1.1)), [])

    def test_p0_case_continuous(self):
        """The case that broke a3728035's predecessor: an over-tolerance gt edge E at 15/16 and a swap S at 16/17 ending
        at 1250 K with a swap-type label (opx+gt, own ρ offset) past its end. Continuous in P and T except at S."""
        tb = table(cls="edge_in", right="ol+opx+gt")
        p_e = pb_const(0.0)
        p_s = math.sqrt(PS[16] * PS[17])
        for cell in tb["cells"]:
            if cell["kind"] == "frozen" or cell["p"] < p_e:
                continue
            if cell["t"] <= 1250.0 and cell["p"] > p_s:
                cell["assemblage"] = "wa+opx+gt"
            elif cell["t"] > 1250.0 and cell["p"] > p_s:
                cell["assemblage"] = "opx+gt"
                cell["rho"] = rho_of(cell["p"], cell["t"]) * 1.05
        for r in list(tb["boundaries"]["rows"]):
            if r["t"] <= 1250.0:
                tb["boundaries"]["rows"].append({"t": r["t"], "p_lo": PS[16], "p_hi": PS[17], "left": "ol+opx+gt",
                                                 "right": "wa+opx+gt", "class": "swap", "converged": True, "p_b": p_s,
                                                 "delta_rho": 0.02, "delta_s": 1.0})
        v = view(tb)
        REFUSED.clear()
        self.assertEqual(jumps_p(v, (1210.0, 1260.0, 1300.0, 1349.0)), [])
        self.assertEqual(jumps_t(v, (p_e * 0.999, p_e * 1.001, math.sqrt(p_e * p_s), p_s * 0.999999)), [])
        self.assertEqual(REFUSED, [])                         # no refusal either (an end extension's rounding once named
                                                              # no region in a 2e-8 Pa sliver)

    def test_refusal_classes(self):
        """A corner row with no usable value refuses by class: «cap» (its run more than 4 columns from the read),
        «region» (sides that name no region of a row), each counted; a read-side corner with no cell refuses above
        the window, as the uncut path does."""
        def steep(n):
            def pb(t):
                a, b = math.log(math.sqrt(PS[13] * PS[14])), math.log(math.sqrt(PS[13 + n] * PS[14 + n]))
                w = min(max((t - 1200.0) / 50.0, 0.0), 1.0)
                return math.exp(a + w * (b - a))
            return pb
        t = 1205.0
        v = view(table(pb=steep(9), t_lo=1150.0, t_hi=1300.0))
        p = v._curves[0].p_b(t) * 1.001
        got = v._solid(p, t)
        self.assertIsInstance(got, st.Stop)
        self.assertIn("within 4 P columns", got.record.why)
        self.assertEqual(v.cut_counts["cap_refusals"], 1)
        v = view(table(pb=steep(3), t_lo=1150.0, t_hi=1300.0))
        self.assertNotIsInstance(v._solid(v._curves[0].p_b(t) * 1.001, t), st.Stop)
        v = view(table(tops={16: 1150.0}))                     # column 16 (right of the curve) ends at 1150 K
        got = v._solid(pb_const(1200.0) * 1.003, 1210.0)
        self.assertIsInstance(got, st.Stop)
        self.assertEqual(got.record.refusal, "input.material_above_solid_window")

    def test_sides_naming_no_region_read_by_count(self):
        """68 H3: two cut curves whose P_b cross between a row and the read's T leave sides that name no region of that
        row in order; the row is read in region «count of curves the read is right of», which changes only where a
        side changes (an event), and the read is counted."""
        tb = table()
        v = view(tb)
        (c,) = v._cut
        other = ma._Curve(99, "swap", None, [dict(r, p_b=math.sqrt(PS[16] * PS[17])) for r in c.rows])
        v._cut, v._parts, v._runcache = [c, other], {}, {}
        k = TS.index(1200.0)
        x = math.log(pb_const(1200.0) * 1.001)
        self.assertEqual(v._region(k, {c: -1, other: 1}, x), 1)   # right of the right curve, left of the left one
        self.assertTrue(v._marks["by_count"])


class Crossing(unittest.TestCase):
    """68 B1 and B2: the p_dataset cut stays in exported-record reads."""

    def test_p_dataset_cut(self):
        """A read near the dataset top does not move when every cell above p_dataset is perturbed."""
        def top(t):
            return math.sqrt(PS[25] * PS[26])
        tb = table(pb=top, p_dataset=PS[27])
        pert = copy.deepcopy(tb)
        for c in pert["cells"]:
            if c["p"] > PS[27]:
                c["rho"] *= 1.5
        p, t = math.sqrt(PS[26] * PS[27]), 1210.0
        self.assertEqual(solid(view(tb), p, t)[0], solid(view(pert), p, t)[0])


class Load(unittest.TestCase):
    """§3 (d): rows on their own pairs with their labels (label/geometry agreement), P_b inside, single-valued."""

    def stops(self, tb, why):
        with self.assertRaises(ma.TableStop) as cm:
            ma.check_boundaries(tb, {(c["p"], c["t"]): c for c in tb["cells"]}, sorted({c["p"] for c in tb["cells"]}))
        self.assertIn(why, str(cm.exception))

    def test_clean_table_loads(self):
        tb = table()
        curves = ma.check_boundaries(tb, {(c["p"], c["t"]): c for c in tb["cells"]}, sorted({c["p"] for c in tb["cells"]}))
        self.assertEqual(len(curves), 1)

    def test_mislocated_p_b(self):
        tb = table()
        tb["boundaries"]["rows"][3]["p_b"] = tb["boundaries"]["rows"][3]["p_hi"] * 1.01
        self.stops(tb, "not strictly inside its pair")

    def test_label_mismatch(self):
        tb = table()
        tb["boundaries"]["rows"][2]["right"] = "cpx+opx"
        self.stops(tb, "are not the cells'")

    def test_not_a_pair(self):
        tb = table()
        tb["boundaries"]["rows"][1]["p_hi"] = PS[18]
        self.stops(tb, "not a pair of adjacent columns")

    def test_frozen_side(self):
        """68 E3: a frozen cell is not a boundary side (r2 H6)."""
        tb = table()
        r = tb["boundaries"]["rows"][2]
        c = tb_cell(tb, r["p_lo"], r["t"])
        c["kind"], c["freeze_t"] = "frozen", r["t"] + 50.0
        self.stops(tb, "a frozen cell is not a boundary side")

    def test_labels_are_string_equal(self):
        """68 E4: the row copies the cells' label strings; the same phase set in another order STOPs."""
        tb = table()
        tb["boundaries"]["rows"][2]["left"] = "opx+ol"
        self.stops(tb, "are not the cells'")

    def test_runs_split_at_a_t_gap(self):
        """68 E6: a group missing one row becomes two curves, and P_b is absent inside the gap."""
        tb = table()
        rows = tb["boundaries"]["rows"]
        gap = rows.pop(4)["t"]
        curves = ma.build_curves(tb["boundaries"], sorted({c["t"] for c in tb["cells"]}))
        self.assertEqual(len(curves), 2)
        self.assertTrue(all(c.p_b(gap) is None for c in curves))

    def test_two_branches_at_one_t(self):
        """ea on 76c0016f: one group with two rows at each T on different pairs (a phase out, back in, out again) is two
        single-valued curves, chained by rank, never one curve interpolated across them."""
        tb = table()
        extra = []
        for r in tb["boundaries"]["rows"]:
            e = copy.deepcopy(r)
            e.update(p_lo=PS[22], p_hi=PS[23], p_b=math.sqrt(PS[22] * PS[23]))
            extra.append(e)
        tb["boundaries"]["rows"] += extra
        curves = ma.build_curves(tb["boundaries"], sorted({c["t"] for c in tb["cells"]}))
        self.assertEqual(len(curves), 2)
        self.assertEqual(sorted(round(c.p_b(1200.0) / PS[15], 6) for c in curves),
                         sorted(round(x / PS[15], 6) for x in (pb_const(1200.0), math.sqrt(PS[22] * PS[23]))))

    def test_branch_count_change_ends_the_curves(self):
        """When a group's row count changes between T rows, its branches end and new ones start (counted ends)."""
        tb = table()
        e = copy.deepcopy(tb["boundaries"]["rows"][4])
        e.update(p_lo=PS[22], p_hi=PS[23], p_b=math.sqrt(PS[22] * PS[23]))
        tb["boundaries"]["rows"].append(e)                    # one T row with two rows, its neighbours with one
        curves = ma.build_curves(tb["boundaries"], sorted({c["t"] for c in tb["cells"]}))
        self.assertEqual(len(curves), 4)                       # before, the two at that row, after
        self.assertTrue(all(len({r["t"] for r in c.rows}) == len(c.rows) for c in curves))

    def test_duplicate_t_in_a_group(self):
        """68 M6: two rows of one group on one pair at one T STOP; the control is the same table without the duplicate."""
        tb = table()
        dup = copy.deepcopy(tb["boundaries"]["rows"][2])
        tb["boundaries"]["rows"].append(dup)
        with self.assertRaises(ma.TableStop) as cm:
            ma.build_curves(tb["boundaries"], sorted({c["t"] for c in tb["cells"]}))
        self.assertIn("not single-valued", str(cm.exception))

    def test_multi_curve_row_loads(self):
        """The label/geometry check sits on each row's own pair: a legitimate two-edge row does not STOP."""
        def edges(t):
            a = math.sqrt(PS[15] * math.sqrt(PS[15] * PS[16]))
            b = math.sqrt(PS[16] * math.sqrt(PS[15] * PS[16]))
            e = {"converged": True, "location_error": 0.0, "by_amount_only": False, "delta_rho": None}
            return [{**e, "phase": "ol", "p_b": a, "p_b_driving_force": a, "p_b_amount": a},
                    {**e, "phase": "wa", "p_b": b, "p_b_driving_force": b, "p_b_amount": b}]
        tb = table(cls="swap_two_edges", edges=edges)
        curves = ma.check_boundaries(tb, {(c["p"], c["t"]): c for c in tb["cells"]}, sorted({c["p"] for c in tb["cells"]}))
        self.assertEqual(len(curves), 2)


class Transitions(unittest.TestCase):
    def test_seam_events_at_p_b(self):
        v = view(table())
        (tr,) = v.transitions()
        self.assertEqual(tr[1], "solid_solid")
        self.assertEqual(v.boundary_pressure(tr[2], 1200.0), pb_const(1200.0))
        self.assertAlmostEqual(v.boundary_pressure(tr[2], 1450.0), pb_const(1400.0), delta=1e-6 * pb_const(0.0))
        self.assertIsNone(v.boundary_pressure(tr[2], 1501.0))  # past the extension (two rows past the last row)
        evs = [e for e in events.record_events(v) if e.name.startswith("phase:")]
        self.assertEqual(len(evs), 1)
        y = [0.0, pb_const(1200.0) * 1.01, 1200.0]
        self.assertAlmostEqual(evs[0].g(0.0, y), pb_const(1200.0) * 0.01, delta=1.0)

    def test_curve_events_land_on_the_old_side(self):
        """A record's curve event g = P − P_b(T) holds its landing stages on the old side in P (component 1, as
        curve_seams). Toy: a curve as steep as Mars's swap 304 extension (9.4e6 Pa/K) with dT/dP dropping 4 % across
        it; with the stages free (component None, the mutant) the re-step's end T jumps with its length and the landing
        never reaches |g| ≤ event_tol·scale (solve.event_chatter at Mars 1774 K); held, it lands at every step size."""
        from solver import rhs
        v = view(table())
        (ev,) = [e for e in events.record_events(v) if e.name.startswith("phase:")]
        self.assertEqual(ev.component, 1)
        m_, r_, pb, k = 5.972e24, 6.371e6, 23.83e9, 9.4e6

        class Sloped:
            def state(self, p, t, guess):
                new = p > pb + k * (t - 1600.0)
                return (3720.0 if new else 3717.0), (9.2e-9 if new else 9.6e-9)
        rs = rhs.r_scale_of(m_, 3.0 * m_ / (4.0 * math.pi * r_ ** 3))

        class Curve:                    # the planted curve over 1000–1900 K: its largest P_b (26.65 GPa) is near where the
            def boundary_pressure(self, curve, t):     # walk crosses it (26.19 GPa, 1851 K), the thinnest margin
                return pb + k * (t - 1600.0) if 1000.0 <= t <= 1900.0 else None   # (68 on C1, condition 1)
        scale = events.curve_p_scale(Curve(), {})          # record_events' rule, not a pinned 1e9 (condition 2)
        self.assertEqual(scale, pb + k * 300.0)
        for comp, want in ((1, "end"), (None, "chatter")):
            for h0 in (1e-3, 7.3e-4, 1.37e-3):
                o = st.Options(rtol=1e-10, floors=rhs.floors(m_, rs), h0=h0 * m_, h_min=1e-15 * m_, h_max=m_ / 20.0,
                               max_steps=200000)
                e = st.Event("phase:sloped", lambda m, y: y[1] - (pb + k * (y[2] - 1600.0)), scale=scale,
                             terminal=False, seam=True, component=comp)
                got = st.run(rhs.make_rhs(Sloped()), m_, (r_, 0.0, 1600.0, 1600.0, 0.0, 0.0), 0.5 * m_, o, [e])
                self.assertEqual(got.stop.kind, want, (comp, h0))

    def test_only_curve_seams_are_held(self):
        """68 B2 (c) on 652004f9: a melting curve (terminal: reaching it refuses) takes no component. A solid–solid curve
        g = P − P_b(T) and, since directing 10-17, a gibbs boundary (its g now (G_a − G_b)/(v_a − v_b), a P) take 1.
        Mutants: melting given 1; gibbs left None."""
        from types import SimpleNamespace
        ph = SimpleNamespace(id="a"), SimpleNamespace(id="b"), SimpleNamespace(id="c")
        stub = SimpleNamespace(phases=ph, seams=lambda: (), source_seams=lambda: (), boundary_pressure=lambda c, t: 1e9,
                               transitions=lambda: ((("a", "b"), "solid_solid", {"form": "library"}),
                                                    (("b", "c"), "melting", {"form": "clapeyron"}),
                                                    (("a", "c"), "solid_solid", {"form": "clapeyron"})))
        got = {e.name: e.component for e in events.record_events(stub)}
        self.assertEqual(got, {"phase:a|b": 1, "melt:b|c": None, "phase:a|c": 1})   # directing 10-17: gibbs held too

    def test_pending_gives_none(self):
        tb = table()
        tb["boundaries"] = {"status": "pending"}
        self.assertEqual(view(tb).transitions(), ())


def within_tol(t):
    """One converged gt edge at P_b, both sides solved and within the pass's tolerance."""
    return [{"phase": "gt", "p_b": pb_const(t), "p_b_driving_force": pb_const(t), "p_b_amount": pb_const(t),
             "converged": True, "location_error": 0.0, "by_amount_only": False, "delta_rho": 1e-4,
             "over_tolerance": False}]


def node_resolved(tb):
    """Every row made node-resolved, as the pass writes a failed swap_two_edges: midpoint P_b, ±half-cell band."""
    for r in tb["boundaries"]["rows"]:
        r.update({"class": "swap_two_edges", "converged": False, "node_resolved": True, "grade": "node-resolved",
                  "p_b": math.sqrt(r["p_lo"] * r["p_hi"]), "band": 0.5 * (r["p_hi"] - r["p_lo"]),
                  "edges": [{"phase": "ol", "p_b_driving_force": None, "p_b_amount": None, "converged": False}]})
        r.pop("delta_rho", None), r.pop("delta_s", None)
    return tb


class ReadRule(unittest.TestCase):
    """(A″) (r2's per-edge criterion, owner f43dac2a): within-tolerance edges and node-resolved rows are read across,
    everything else is cut; as built by (R1) (owner e4cd7f01)."""

    def test_criterion(self):
        e = within_tol(1200.0)[0]
        row = {"class": "edge_in", "converged": True, "edges": [e]}
        self.assertTrue(ma.row_across(row))
        self.assertTrue(ma.row_across({"class": "swap_two_edges", "node_resolved": True, "edges": []}))
        self.assertFalse(ma.row_across({"class": "swap", "converged": True, "p_b": 1.0, "delta_rho": 0.0}))
        for bad in ({"over_tolerance": True}, {"delta_rho": None}, {"converged": False}):
            b = {**e, **bad}
            if bad.get("delta_rho", 0) is None:
                b.pop("over_tolerance")                       # the pass writes no flag when a side is unsolved
            self.assertFalse(ma.row_across({**row, "edges": [b]}), bad)
            self.assertFalse(ma.row_across({**row, "edges": [e, b]}), bad)   # one bad edge cuts the row

    def test_within_tolerance_edge_reads_across(self):
        """Read across: no cut curve, no step at P_b, the read within 1e-6 of cubic2 (pending), still landed as an event;
        the planted control (the same rows over tolerance) cuts."""
        tb = table(cls="edge_in", right="ol+opx+gt", edges=within_tol)
        pend = copy.deepcopy(tb)
        pend["boundaries"] = {"status": "pending"}
        v, w = view(tb), view(pend)
        self.assertEqual(v._cut, [])
        p_b, t = pb_const(1200.0), 1210.0
        for p in (p_b * 0.999, p_b * 1.001, math.sqrt(PS[14] * PS[15])):
            self.assertLess(rel(solid(v, p, t)[0], solid(w, p, t)[0]), 1e-6)
        self.assertLess(rel(solid(v, p_b * (1 - 1e-12), t)[0], solid(v, p_b * (1 + 1e-12), t)[0]), 1e-12)
        self.assertEqual(len(v.transitions()), 1)
        over = copy.deepcopy(tb)
        for r in over["boundaries"]["rows"]:
            r["edges"][0]["over_tolerance"] = True
        self.assertEqual(len(view(over)._cut), 1)

    def test_node_resolved_reads_across_with_its_band(self):
        """Never forced into a step (§3.3): read as uncut, with NODE_NOTE carrying P_b and the band; landed as an
        event of kind «node»."""
        tb = node_resolved(table())
        pend = copy.deepcopy(tb)
        pend["boundaries"] = {"status": "pending"}
        v, w = view(tb), view(pend)
        self.assertEqual(v._cut, [])
        p, t = pb_const(1200.0) * 1.001, 1210.0
        self.assertLess(rel(solid(v, p, t)[0], solid(w, p, t)[0]), 1e-6)
        notes = [n.text for n in v.state(p, t)[2] if ma.NODE_NOTE in getattr(n, "text", "")]
        band = 0.5 * (PS[16] - PS[15]) / 1e9
        pb = pb_const(1200.0) / 1e9                           # constant over the curve: the range is one value
        self.assertEqual(notes, [f"{ma.NODE_NOTE}; P_b {pb:.4g}–{pb:.4g} GPa, band ± {band:.3g}–{band:.3g} GPa"])
        self.assertEqual(notes, [n.text for n in v.state(p, 1255.0)[2] if ma.NODE_NOTE in getattr(n, "text", "")])
        self.assertFalse(any(ma.NODE_NOTE in getattr(n, "text", "") for n in v.state(PS[25] * 1.1, t)[2]))   # not in another cell
        self.assertEqual([c.kind for c in v._curves], ["node"])
        self.assertEqual(len(v.transitions()), 1)

    def test_cut_curves_are_runs_of_the_full_set(self):
        """68 B1: two branches of one group (edges over tolerance at columns 15/16 and 22/23); the low branch's row is
        read across at 1200 K and the high branch's at 1250 K. Re-chaining the cut rows by rank would link the high
        row at 1200 K to the low row at 1250 K; the cut curves are runs of the full curves and link no two branches."""
        tb = table(cls="edge_in", right="ol+opx+gt")
        extra = []
        for r in tb["boundaries"]["rows"]:
            e = copy.deepcopy(r)
            pb = math.sqrt(PS[22] * PS[23])
            e.update(p_lo=PS[22], p_hi=PS[23])
            e["edges"][0].update(p_b=pb, p_b_driving_force=pb, p_b_amount=pb)
            extra.append(e)
        tb["boundaries"]["rows"] += extra
        for r in tb["boundaries"]["rows"]:
            if (r["t"], r["p_lo"]) in ((1200.0, PS[15]), (1250.0, PS[22])):
                r["edges"][0].update(delta_rho=1e-4, over_tolerance=False)
        v = view(tb)
        self.assertEqual(len(v._curves), 2)
        for c in v._cut:
            self.assertEqual(len({r["p_lo"] for r in c.rows}), 1, [(r["t"], r["p_lo"]) for r in c.rows])
        self.assertEqual(sorted((c.t0, c.t1, c.rows[0]["p_lo"] == PS[15]) for c in v._cut),
                         [(1000.0, 1150.0, True), (1000.0, 1200.0, False), (1250.0, 1400.0, True),
                          (1300.0, 1400.0, False)])
        rechained = ma.build_curves({"rows": [r for r in tb["boundaries"]["rows"] if not ma.row_across(r)]}, v.ts)
        self.assertTrue(any(len({r["p_lo"] for r in c.rows}) > 1 for c in rechained))   # the mutant links them

    def test_curve_ids_do_not_depend_on_hashing(self):
        """Curve ids order the groups by sorted phase names, not a frozenset's repr (which follows PYTHONHASHSEED):
        six swap groups with multi-phase labels get the same ids in processes with different hash seeds."""
        import os
        import subprocess
        import sys
        code = ("from solver import material_assemblage as ma; "
                "labs = [('aa+bb+cc', 'dd+ee+ff'), ('aa+dd+ee', 'bb+cc+ff'), ('bb+dd+ff', 'aa+cc+ee'), "
                "('cc+dd+ee', 'aa+bb+ff'), ('aa+cc+ff', 'bb+dd+ee'), ('bb+cc+ee', 'aa+dd+ff')]; "
                "rows = [{'t': 1000.0, 'p_lo': float(2 * i), 'p_hi': float(2 * i + 1), 'left': l, 'right': r, "
                "'class': 'swap', 'converged': True, 'p_b': 2 * i + 0.5} for i, (l, r) in enumerate(labs)]; "
                "print([(c.id, c.rows[0]['left_label']) for c in ma.build_curves({'rows': rows}, [1000.0])])")
        outs = {subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True,
                               env={**os.environ, "PYTHONHASHSEED": str(seed)}).stdout for seed in range(1, 9)}
        self.assertEqual(len(outs), 1, outs)
        self.assertEqual(outs.pop().count("'"), 12)            # six curves printed, not an empty or failed run

class Choices(unittest.TestCase):
    """Each agreed (R1) design choice pinned by a case that its alternative fails (68 B2 on d7cc971d)."""

    def test_reach_reads_the_region_below_first(self):
        """_row_reach's side rule, pinned (68 N7 «reach hi first» on 7582ff4a): an empty region with runs on both sides
        reads the region below it, at its upper bounding curve; the region above only when none lies below. Either
        rule telescopes (it depends on the row and region alone); this one is the one the records were read with."""
        v = view(table(cls="edge_in", right="ol+opx+gt"))
        part = [(PS[10], None), (PS[14], None), (PS[18], None)]
        v._partition = lambda k: part
        v._run_value = lambda f, k, r, x, corner: (r, x)
        v._runs = lambda f, k: {0: [1], 3: [1]}
        self.assertEqual(v._row_reach("dtdp_eq", 0, 1), (0, math.log(PS[10])))
        self.assertEqual(v._row_reach("dtdp_eq", 0, 2), (0, math.log(PS[10])))
        v._runs = lambda f, k: {3: [1]}
        self.assertEqual(v._row_reach("dtdp_eq", 0, 1), (3, math.log(PS[18])))
        v._runs = lambda f, k: {}
        self.assertIsNone(v._row_reach("dtdp_eq", 0, 1))

    def test_far_side_unreadable_never_refuses_the_near_side(self):
        """68 B1, in the blend form (68 ruling 1): an edge whose far side has no dT/dP or c_P at a corner row (only ρ)
        never refuses the near side inside the window: the far side's read takes, in that row, the nearest region with
        a run at its bounding curve (_row_reach), and the read stays continuous in T across the row lines (δ := 0
        stepped dT/dP ×3 at default_bse 133 GPa, 3550 K). The side reads leave no mark or count on the read (ruling 1
        (3)). The far side's own read refuses."""
        tb = table(cls="edge_in", right="ol+opx+gt")
        p_b = pb_const(0.0)
        for c in tb["cells"]:
            if c["p"] > p_b and c["kind"] != "frozen":
                c["dtdp_eq"] *= 1.05                                # a planted dT/dP offset the blend carries
            elif c["kind"] != "frozen":                             # curved in P on the near side, so a reach at the
                c["dtdp_eq"] *= 1.0 + 0.002 * PS.index(c["p"]) ** 2   # last node and one at the curve differ (68 B2 (a))
            if c["t"] == 1250.0 and c["p"] > p_b:
                c["dtdp_eq"], c["c_p_eq"] = None, None
        v = view(tb)
        xb = math.log(p_b)
        w = v._width(xb)
        p = math.exp(xb - 0.5 * w)
        t = 1210.0
        got = v._solid(p, t)
        self.assertNotIsInstance(got, st.Stop)
        self.assertEqual(v.cut_counts["reach_rows"], 0)            # the far side's reach is a side read's: no count
        self.assertEqual(v.cut_counts["blend_drops"], 0)           # the reach gives it its corner row: none dropped
        self.assertEqual(v._marks["empty"], False)                 # side reads set no MULTI_NOTE mark (68 B2 (d))
        k = TS.index(1250.0)                                       # the far side's empty row reads the near side at P_b
        self.assertIsNone(v._row_value("dtdp_eq", k, 1, xb, False))
        self.assertEqual(v._row_reach("dtdp_eq", k, 1), v._row_value("dtdp_eq", k, 0, xb, False))
        for tl in (1200.0, 1250.0):                                # continuous in T at the row lines, every field
            a, b = v._solid(p, tl - 1e-7), v._solid(p, tl + 1e-7)
            for f in range(3):
                self.assertLess(abs(b[f] / a[f] - 1), 1e-6, (tl, f))
        self.assertIsInstance(v._solid(p_b * 1.001, t), st.Stop)
        self.assertEqual(jumps_p(v, (t,)), [])

    def test_blend_sharpness_per_field(self):
        """BLEND_SHARP (the loop-class truth check): H = S(κ(x − x_b)/(2w) + ½), κ 1 for ρ and 2 for dT/dP and c_P, so
        the latter two blend over the window's central half. With L = 1 and R = 2 the blend is 1 + H on either side.
        Mutant: one κ for every field (the dT/dP weight at w/4 is then S(3/8), not S(¼))."""
        tb = table(cls="edge_in", right="ol+opx+gt")
        v = view(tb)
        t = 1210.0
        xb = math.log(pb_const(t))
        w = v._width(xb)
        ib = int((t - TS[0]) // 50)
        (c,) = v._cut
        v._side_rows = lambda f, x, ib_, sides: {ib: 1.5 + 0.5 * sides[c], ib + 1: 1.5 + 0.5 * sides[c]}   # L 1, R 2
        near = [(c, xb, w)]
        S = lambda u: u * u * (3.0 - 2.0 * u)
        for f, at, want in (("rho", -0.25, S(0.375)), ("dtdp_eq", -0.25, S(0.25)), ("c_p", -0.25, S(0.25)),
                            ("rho", -0.5, S(0.25)), ("dtdp_eq", -0.5, 0.0), ("c_p", 0.5, 1.0), ("dtdp_eq", 0.0, 0.5)):
            got = v._blend_sides(f, xb + at * w, t, ib, {c: -1 if at < 0 else 1}, near, 1.0 if at < 0 else 2.0)
            self.assertAlmostEqual(got, 1.0 + want, places=12, msg=(f, at))

    def test_blend_drops_a_side_with_no_corner_row(self):
        """68 ruling 1 (2): a side assignment whose read has no corner row is dropped and the remaining weights
        renormalised (never 0 × a missing value), and counted; the read is then the own read alone."""
        tb = table(cls="edge_in", right="ol+opx+gt")
        v = view(tb)
        t = 1210.0
        xb = math.log(pb_const(t))
        w = v._width(xb)
        x = xb - 0.25 * w                                          # inside every field's blend (BLEND_SHARP ≤ 2)
        own = v._solid(math.exp(x), t)[0]
        v2 = view(tb)
        v2._side_rows = lambda f, x, ib, sides: {}                # every far side without rows
        got = v2._solid(math.exp(x), t)[0]
        (c,) = v2._cut
        ib = int((t - TS[0]) // 50)
        self.assertAlmostEqual(got, v2._value("rho", x, t, 15, ib, {c: -1}, False), delta=1e-14 * got)   # (1 − H)·v/(1 − H)
        self.assertNotEqual(got, own)                              # the full blend differs: the far side was there
        self.assertEqual(v2.cut_counts["blend_drops"], 3)          # one per field

    def test_far_side_past_the_cap_never_refuses_the_near_side(self):
        """68 B1, the cap: δ's side reads are uncapped (x_b moves with t, so a cap there would switch inside a T cell);
        a far side whose run starts more than 4 columns from x_b in a corner row leaves the near read standing, while
        the far side's own read refuses (its read-cell corner has no value)."""
        tb = table(cls="edge_in", right="ol+opx+gt")
        p_b = pb_const(0.0)
        for c in tb["cells"]:
            if c["t"] == 1250.0 and p_b < c["p"] < PS[22]:
                c["rho"] = None
        v = view(tb)
        xb = math.log(p_b)
        p = math.exp(xb - 0.5 * v._width(xb))
        self.assertNotIsInstance(v._solid(p, 1210.0), st.Stop)
        self.assertIsInstance(v._solid(p_b * 1.001, 1210.0), st.Stop)

    def test_liquid_alone_never_reads_the_solid_table(self):
        """The solver reads the view through state() and phase_read() only; at φ ≥ 1 neither reads the solid table, so
        a solid-table refusal there (default_bse's 15 cells at 0.11–0.22 GPa, 2325 K, φ = 1) is never met by a solve."""
        v = view(table())
        p, t = 1.0e8, 2400.0
        self.assertGreaterEqual(ma._lm().silicate_melt_phi(p, t, v.variant), 1.0)
        self.assertIsInstance(v._solid(p, t), st.Stop)               # the solid table refuses here
        def boom(*a):
            raise AssertionError("solid table read at φ ≥ 1")
        v._solid = boom
        got = v.state(p, t)
        self.assertNotIsInstance(got, st.Stop)
        self.assertTrue(any(ma.LIQUID_ALONE_NOTE in getattr(n, "text", "") for n in got[2]))
        self.assertEqual(v.phase_read(p, t), ma.PHASE_ID)

    def test_gap_inside_a_region_reads_by_a_bridge(self):
        """68 H1, item 5d998d40 (68 ruling 4): an outer row with a missing node inside a region reads across the gap by
        the cubic Hermite bridge from one run's end to the next with their end slopes (not the nearest run's value, and
        no longer the linear join, which kinked at both run ends): between the two end values, C¹ at both run ends,
        and the read stays continuous across the gap."""
        tb = table()
        tb_cell(tb, PS[11], 1300.0)["rho"] = None
        v = view(tb)
        k = TS.index(1300.0)
        x10, x12 = math.log(PS[10]), math.log(PS[12])
        a, b = tb_cell(tb, PS[10], 1300.0)["rho"], tb_cell(tb, PS[12], 1300.0)["rho"]
        for f in (0.1, 0.3, 0.5, 0.9):
            got = v._row_value("rho", k, 0, x10 + f * (x12 - x10), False)
            self.assertTrue(min(a, b) < got < max(a, b), (f, got))
        h = 1e-5                                             # one slope from both sides at both run ends (h large
        for x0 in (x10, x12):                                # enough for rounding, small for the curvature)
            lo = (v._row_value("rho", k, 0, x0, False) - v._row_value("rho", k, 0, x0 - h, False)) / h
            hi = (v._row_value("rho", k, 0, x0 + h, False) - v._row_value("rho", k, 0, x0, False)) / h
            self.assertLess(abs(hi - lo), 1e-3 * max(abs(lo), abs(hi)), x0)
        self.assertEqual(jumps_p(v, (1210.0,)), [])

    def test_outer_row_uncapped_and_dropped(self):
        """68 H2: an outer row reads past its run's end with no column cap, and an outer row with no run in the read's
        region drops; neither refuses (a corner row would)."""
        def steep(t):
            a, b = math.log(math.sqrt(PS[13] * PS[14])), math.log(math.sqrt(PS[22] * PS[23]))
            w = min(max((t - 1200.0) / 50.0, 0.0), 1.0)
            return math.exp(a + w * (b - a))
        v = view(table(pb=steep, t_lo=1150.0, t_hi=1400.0))
        p, t = PS[21] * 1.1, 1275.0                                 # row 1200's left run ends at column 13: 8 columns
        self.assertNotIsInstance(v._solid(p, t), st.Stop)
        def high(t):                                                # right of P_b at 1300 K: only columns above p_dataset
            j = {1150.0: 23, 1200.0: 24, 1250.0: 26}.get(t, 27)
            return math.sqrt(PS[j] * PS[j + 1])
        v = view(table(pb=high, t_lo=1150.0, t_hi=1400.0))
        got = v._solid(PS[26] * 1.1, 1210.0)
        self.assertNotIsInstance(got, st.Stop)
        self.assertEqual(v.cut_counts["row_drop_reads"], 1)

    def test_window_width_interpolated_in_ln_p(self):
        """68 (c): w at x is the node-centred cell width interpolated linearly in ln P between nodes, so it is
        continuous where x_b crosses a node (a step-valued w would step the correction there)."""
        v = view(table(cls="edge_in", right="ol+opx+gt"))
        v.lnps = [0.0, 1.0, 3.0, 4.0, 7.0, 8.0]
        self.assertAlmostEqual(v._width(2.0), 0.5 * (1.5 + 1.5), delta=1e-12)
        self.assertAlmostEqual(v._width(3.5), 0.5 * (1.5 + 2.0), delta=1e-12)
        self.assertAlmostEqual(v._width(3.0 - 1e-12), v._width(3.0 + 1e-12), delta=1e-9)

    def test_coincident_edges_are_a_swap(self):
        """68 N2: two cut edges at one P_b at every row are a step, read as a swap (no correction), counted."""
        def edges(t):
            e = {"converged": True, "location_error": 0.0, "by_amount_only": False, "delta_rho": OFF,
                 "over_tolerance": True, "p_b": pb_const(t), "p_b_driving_force": pb_const(t), "p_b_amount": pb_const(t)}
            return [{**e, "phase": "cpx"}, {**e, "phase": "wa"}]
        v = view(table(cls="swap_two_edges", edges=edges))
        self.assertEqual(v.coincident, 2)
        self.assertEqual({c.kind for c in v._cut}, {"swap"})
        p_b, t = pb_const(1200.0), 1210.0
        self.assertAlmostEqual(solid(v, p_b * (1 + 1e-9), t)[0] / solid(v, p_b * (1 - 1e-9), t)[0] - 1, OFF, delta=1e-4)

    def test_zero_width_region_reads_the_mean(self):
        """Two curves at one P_b in a row (crossing there, not coincident at every row): the zero-width region
        between them reads the mean of its neighbours' values at that P_b."""
        def edges(t):
            m = math.sqrt(PS[15] * PS[16])
            d = (t - 1200.0) / 2000.0
            a, b = m * math.exp(-d), m * math.exp(d)
            e = {"converged": True, "location_error": 0.0, "by_amount_only": False, "delta_rho": None}
            return [{**e, "phase": "ol", "p_b": a, "p_b_driving_force": a, "p_b_amount": a},
                    {**e, "phase": "wa", "p_b": b, "p_b_driving_force": b, "p_b_amount": b}]
        v = view(table(cls="swap_two_edges", edges=edges, t_lo=1150.0, t_hi=1250.0))
        k = TS.index(1200.0)
        (pa, _), (pb, _) = v._partition(k)
        self.assertEqual(pa, pb)
        xm = math.log(pa)
        vl, vr = v._run_value("rho", k, 0, xm, False), v._run_value("rho", k, 2, xm, False)
        self.assertGreater(abs(vr / vl - 1), 1e-3)
        self.assertEqual(v._row_value("rho", k, 1, xm, False), 0.5 * (vl + vr))

    def test_extension_ln_linear(self):
        """(R1) §4: past an end P_b continues ln-linearly from the two end rows (constant only for a one-row curve)."""
        rows = [{"t": 1000.0, "p_b": 2.0e9}, {"t": 1050.0, "p_b": 3.0e9}]
        c = ma._Curve(0, "swap", None, rows)
        self.assertAlmostEqual(c.p_b_ext(1100.0, 100.0), 4.5e9, delta=1e-3)
        self.assertAlmostEqual(c.p_b_ext(950.0, 100.0), 2.0e9 / 1.5, delta=1e-3)
        self.assertIsNone(c.p_b_ext(1151.0, 100.0))
        self.assertEqual(ma._Curve(0, "swap", None, rows[:1]).p_b_ext(1040.0, 100.0), 2.0e9)

    def test_missing_corner_off_the_reads_region_does_not_refuse(self):
        """D-M2 per region: a read-cell corner node with no cell refuses only when it is in the read's region; across a
        cut curve it is not read, so a read left of the curve stands when the right column ends below its T."""
        v = view(table(tops={16: 1150.0}))
        self.assertNotIsInstance(v._solid(pb_const(1200.0) * 0.997, 1210.0), st.Stop)
        self.assertIsInstance(v._solid(pb_const(1200.0) * 1.003, 1210.0), st.Stop)

    def test_swap_note_only_in_the_read_cell(self):
        """SWAP_NOTE goes on a read whose P cell holds the swap's P_b, not on every read whose stencil sees it."""
        v = view(table())
        t = 1210.0
        near = v.state(pb_const(1200.0) * 1.001, t)[2]
        far = v.state(math.sqrt(PS[12] * PS[13]), t)[2]
        self.assertTrue(any(ma.SWAP_NOTE in getattr(n, "text", "") for n in near))
        self.assertFalse(any(ma.SWAP_NOTE in getattr(n, "text", "") for n in far))


def _shipped():
    from solver import material_registry as mr
    reg = mr.load()
    if not isinstance(reg, mr.Registry):
        return []
    return [(rid, reg.records[rid], reg.tables[rid]) for rid in sorted(reg.records)
            if reg.records[rid]["kind"] == "assemblage" and rid in reg.tables]


class Envelope(unittest.TestCase):
    """68 B1 on 652004f9: no read leaves the physical envelope by carrying data past where it applies (the empty-region
    read extrapolated to c_P −0.38). On every shipped assemblage record (a TIP; skipped on the engine branch alone),
    every cell centre up to p_dataset reads c_P > 0. Mutant: the empty-region fraction unclamped."""

    @unittest.skipUnless(_shipped(), "no shipped assemblage record with its table (the engine branch without records)")
    def test_cp_positive_everywhere(self):
        for rid, rec, tb in _shipped():
            v = ma.view(ma.mv.thaw_plain(rec), tb, 1600.0)
            bad = []
            for ib in range(len(v.ts) - 1):
                t = 0.5 * (v.ts[ib] + v.ts[ib + 1])
                for ia in range(len(v.ps) - 1):
                    if v.ps[ia + 1] > v.p_dataset:
                        break
                    got = v._solid(math.sqrt(v.ps[ia] * v.ps[ia + 1]), t)
                    if not isinstance(got, st.Stop) and not got[2] > 0.0:
                        bad.append((v.ps[ia], t, got[2]))
            self.assertEqual(bad, [], rid)

    @unittest.skipUnless(_shipped(), "no shipped assemblage record with its table (the engine branch without records)")
    def test_rho_rises_where_the_table_rises(self):
        """Directing 10-17: along P at fixed T, ρ at consecutive cell centres rises wherever the table's nodes of both
        cells rise on both T rows (to 1e-5: the floor columns' rounding); where the table itself does not rise the read
        follows the data. Mutant: the PCHIP end slope past a run's end (bse 20.9 GPa, 2075 K fell 1.2 %)."""
        for rid, rec, tb in _shipped():
            v = ma.view(ma.mv.thaw_plain(rec), tb, 1600.0)
            bad = []
            for ib in range(len(v.ts) - 1):
                t, last = 0.5 * (v.ts[ib] + v.ts[ib + 1]), None
                for ia in range(len(v.ps) - 1):
                    if v.ps[ia + 1] > v.p_dataset:
                        break
                    got = v._solid(math.sqrt(v.ps[ia] * v.ps[ia + 1]), t)
                    if isinstance(got, st.Stop):
                        last = None
                        continue
                    if last is not None and ia >= 1:
                        cols = [[(v._cell(j, k) or {}).get("rho") for k in (ib, ib + 1)] for j in (ia - 1, ia, ia + 1)]
                        rises = all(a and b and c and a < b < c for a, b, c in zip(*cols))
                        if rises and got[0] < last * (1.0 - 1e-5):
                            bad.append((v.ps[ia], t, got[0] / last - 1.0))
                    last = got[0]
            self.assertEqual(bad, [], rid)

    def test_extrapolation_never_steepens(self):
        """Past a run's end the value follows the gentlest secant of the run (0 where the secants change sign)."""
        xs, ys = [0.0, 1.0, 2.0, 3.0], [10.0, 20.0, 21.0, 22.0]
        self.assertEqual(ma._pchip_1d(-1.0, xs, ys), 9.0)          # the gentlest secant 1, not the steep first one
        self.assertEqual(ma._pchip_1d(4.0, xs, ys), 23.0)
        self.assertEqual(ma._pchip_1d(-1.0, xs, [10.0, 20.0, 15.0, 16.0]), 10.0)   # secants change sign: held

    def test_empty_region_read_never_extrapolates(self):
        """The planted form of the dmm case: a row whose two cut edges bound an empty region elsewhere than the read's
        x; the empty-region read holds the nearer curve's value instead of carrying the neighbours' difference."""
        def edges(t):
            m = math.sqrt(PS[15] * PS[16])
            a, b = m * math.exp(-0.05), m * math.exp(0.05)
            e = {"converged": True, "location_error": 0.0, "by_amount_only": False, "delta_rho": None}
            return [{**e, "phase": "ol", "p_b": a, "p_b_driving_force": a, "p_b_amount": a},
                    {**e, "phase": "wa", "p_b": b, "p_b_driving_force": b, "p_b_amount": b}]
        v = view(table(cls="swap_two_edges", edges=edges))
        k = TS.index(1200.0)
        (pa, _), (pb, _) = v._partition(k)
        vl = v._run_value("rho", k, 0, math.log(pa), False)
        vr = v._run_value("rho", k, 2, math.log(pb), False)
        for x, want in ((math.log(pa) - 0.3, vl), (math.log(pb) + 0.3, vr)):
            self.assertEqual(v._row_value("rho", k, 1, x, False), want)


class Disclosures(unittest.TestCase):
    """§5's per-table disclosures: edge δ, multi-curve cells, T-direction changes split located/unlocated (68 M5)."""

    def test_edge_delta_and_t_changes(self):
        tb = table(cls="edge_in", right="ol+opx+gt", pb=pb_slope)
        d = ma.boundary_disclosures(record(tb["p_dataset"]), tb)
        self.assertEqual(d["curves"]["edge"], 1)
        self.assertEqual(d["edge_delta"]["n"], 9)                       # rows 1000–1400 K
        self.assertEqual(d["edge_delta"]["unreadable"], [])
        self.assertGreater(d["edge_delta"]["max"], 1e-2)               # the planted 2 % offset
        self.assertTrue(d["over_tolerance"])
        self.assertTrue(d["t_changes"]["located"])                     # the sloped curve crosses columns between rows
        self.assertTrue(all(x["on_curve"] == 0 for x in d["t_changes"]["located"]))
        self.assertTrue(d["t_changes"]["unlocated"])                    # the region's T ends (950/1000, 1400/1450)
        self.assertGreater(d["sweep"]["corrections"], 0)
        self.assertEqual(d["curve_ends"], 2)                           # 68 E15: starts at 1000 K, ends at 1400 K

    def test_multi_curve_cells_counted(self):
        def edges(t):
            a = math.sqrt(PS[15] * math.sqrt(PS[15] * PS[16]))
            b = math.sqrt(PS[16] * math.sqrt(PS[15] * PS[16]))
            e = {"converged": True, "location_error": 0.0, "by_amount_only": False, "delta_rho": None}
            return [{**e, "phase": "ol", "p_b": a, "p_b_driving_force": a, "p_b_amount": a},
                    {**e, "phase": "wa", "p_b": b, "p_b_driving_force": b, "p_b_amount": b}]
        tb = table(cls="swap_two_edges", edges=edges)
        self.assertEqual(ma.boundary_disclosures(record(tb["p_dataset"]), tb)["multi_curve_cells"], 9)

    def test_pending(self):
        tb = table()
        tb["boundaries"] = {"status": "pending"}
        self.assertEqual(ma.boundary_disclosures(record(tb["p_dataset"]), tb), {"status": "pending"})

    def test_read_modes_and_smoothing(self):
        """(A″)'s disclosures: each row's read mode, the smoothing over rows read across, and (R1)'s past-end label
        changes read across, by type."""
        tb = table(cls="edge_in", right="ol+opx+gt", edges=within_tol)
        d = ma.boundary_disclosures(record(tb["p_dataset"]), tb)
        n = len(tb["boundaries"]["rows"])
        self.assertEqual(d["read"]["counts"], {"cut": 0, "across": n, "node": 0})
        self.assertEqual(d["across"]["e_smooth"]["edge"]["n"] + d["across"]["skipped"], n)
        self.assertGreater(d["across"]["node_to_node"]["edge"]["max"][0], 1e-2)     # the planted 2 % across the cell
        self.assertEqual(d["sweep"]["corrections"], 0)
        d = ma.boundary_disclosures(record(tb["p_dataset"]), node_resolved(table()))
        self.assertEqual(d["read"]["counts"]["node"], len(tb["boundaries"]["rows"]))
        tb = table(t_end=1250.0, third="ol+opx+gt")                    # past the end, an edge-type label change
        d = ma.boundary_disclosures(record(tb["p_dataset"]), tb)
        self.assertEqual(d["read"]["counts"]["cut"], len(tb["boundaries"]["rows"]))
        self.assertGreater(d["past_end_read_across"]["edge"]["n"], 0)
        tb = table(t_end=1250.0, third="cpx+opx")                      # … and a swap-type one
        self.assertGreater(ma.boundary_disclosures(record(tb["p_dataset"]), tb)["past_end_read_across"]["swap"]["n"], 0)


if __name__ == "__main__":
    unittest.main()
