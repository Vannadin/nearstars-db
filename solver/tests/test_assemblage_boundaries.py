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


class OneSided(unittest.TestCase):
    """§3 (b): a read on one side uses no node of the other side; the planted control reads across and fails."""

    def test_reads_stay_on_their_side(self):
        tb = table()
        v = view(tb)
        p_b, t = pb_const(1200.0), 1210.0
        left, right = p_b * 0.999, p_b * 1.001
        self.assertLess(rel(solid(v, left, t)[0], rho_of(left, t)), 1e-4)
        self.assertLess(rel(solid(v, right, t)[0], rho_of(right, t) * (1 + OFF)), 1e-4)
        v0 = view(tb)
        v0._cut = []                                       # planted control: the cut disabled
        self.assertGreater(rel(solid(v0, left, t)[0], rho_of(left, t)), 1e-3)

    def test_span_one_cell_away(self):
        """68 M3: a read one cell left of the curve's cell still has column 16 in its stencil, and must not use it."""
        tb = table()
        v = view(tb)
        p, t = math.sqrt(PS[14] * PS[15]), 1210.0
        self.assertTrue(v._crossing(p, t, 14, int((t - TS[0]) // 50)))
        self.assertLess(rel(solid(v, p, t)[0], rho_of(p, t)), 1e-5)
        v0 = view(tb)
        v0._cut = []
        self.assertGreater(rel(solid(v0, p, t)[0], rho_of(p, t)), 1e-5)

    def test_uncut_reads_bit_identical(self):
        """Away from every curve the read is cubic2's, bit for bit, against the same table with boundaries pending."""
        tb = table()
        pend = copy.deepcopy(tb)
        pend["boundaries"] = {"status": "pending"}
        v, w = view(tb), view(pend)
        for p in (PS[3] * 1.1, PS[8] * 1.3, PS[24] * 1.2):
            for t in (450.0, 905.0, 1210.0, 1555.0):
                self.assertEqual(solid(v, p, t)[:3], solid(w, p, t)[:3])


class Sloped(unittest.TestCase):
    """r2 M1, 68 M1: each node judged at its own T; the curve crosses the read cell diagonally and the read answers."""

    def test_diagonal_cut_answers_one_sided(self):
        tb = table(pb=pb_slope)
        v = view(tb)
        t = 1225.0
        p = pb_slope(t) * 0.97                                # left of the curve at the read's T
        ia = max(i for i in range(len(PS) - 1) if PS[i] <= p)
        ib = int((t - TS[0]) // 50)
        cuts = v._crossing(p, t, ia, ib)
        side = {c: c.side_of(p, t) for c in cuts}
        for k in range(ib - 1, ib + 3):                       # every read-side node is left of P_b at its own T
            for j in range(ia - 5, ia + 7):
                if v._node_ok(j, k, side, cuts):
                    self.assertLess(PS[j], pb_slope(TS[k]))
        got = solid(v, p, t)[0]
        self.assertLess(rel(got, rho_of(p, t)), 1e-3)
        v0 = view(tb)
        v0._cut = []                                       # T-first, uncut: reads across
        self.assertGreater(rel(solid(v0, p, t)[0], rho_of(p, t)), 1e-3)

    def test_node_side_at_its_own_t(self):
        """The read-T mutant: judging a node by P_b at the read's T keeps a node that is right of P_b at its own T."""
        tb = table(pb=pb_slope)
        v = view(tb)
        t, k = 1225.0, int((1225.0 - TS[0]) // 50) + 2       # an outer row at 1300 K, where P_b has moved right
        p = pb_slope(t) * 0.97
        (c,) = v._crossing(p, t, max(i for i in range(len(PS) - 1) if PS[i] <= p), int((t - TS[0]) // 50))
        j = next(j for j in range(len(PS)) if pb_slope(t) < PS[j] < pb_slope(TS[k]))
        self.assertTrue(v._node_ok(j, k, {c: 1}, [c]) is False)      # right of the read-T P_b, left at its own T
        self.assertTrue(v._node_ok(j, k, {c: -1}, [c]))


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
        """r2 Q2 / 68 M4: continuous at P_b; equal to the uncorrected read at the nodes; L − δ/4 at the left half's
        midpoint in ln P. Mutants: no correction, and the sign flipped (a 2δ step)."""
        tb = table(cls="edge_in", right="ol+opx+gt")
        v = view(tb)
        t = 1200.0                                            # on a row: the read's cell is the row's pair
        p_b = pb_const(t)
        lo, hi = PS[15], PS[16]
        a, b = solid(v, p_b * (1 - 1e-12), t)[0], solid(v, p_b * (1 + 1e-12), t)[0]
        self.assertLess(rel(a, b), 1e-9)
        self.assertEqual(solid(v, lo, t)[0], tb_cell(tb, lo, t)["rho"])
        self.assertEqual(solid(v, hi, t)[0], tb_cell(tb, hi, t)["rho"])
        ib = int((t - TS[0]) // 50)
        cuts = v._crossing(p_b, t, 15, ib)
        (c,) = cuts
        xb = math.log(p_b)
        L = v._cut_value("rho", xb, t, 15, ib, {c: -1}, cuts)
        R = v._cut_value("rho", xb, t, 15, ib, {c: 1}, cuts)
        xm = 0.5 * (math.log(lo) + xb)
        unc = v._cut_value("rho", xm, t, 15, ib, {c: -1}, cuts)
        self.assertAlmostEqual(solid(v, math.exp(xm), t)[0] - unc, -(L - R) / 4.0, delta=1e-9 * L)
        self.assertGreater(abs(L - R) / L, 1e-3)              # the planted δ is there to remove
        orig = ma.AssemblageView._solid_cut

        def no_corr(self, *a):
            for cc in self._cut:
                cc.kind = "swap"
            return orig(self, *a)
        mut = view(tb)
        mut._solid_cut = no_corr.__get__(mut)
        self.assertGreater(rel(solid(mut, p_b * (1 - 1e-12), t)[0], solid(mut, p_b * (1 + 1e-12), t)[0]), 1e-3)

    def test_two_curves_in_one_cell(self):
        """r2 Q1: two edges in one cell; between them the read is linear in ln P between the outer one-sided values,
        with its note; no edge correction there."""
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
        ib = int((t - TS[0]) // 50)
        cuts = v._crossing(math.exp(xa), t, 15, ib)
        self.assertEqual(len(cuts), 2)
        va = v._cut_value("rho", xa, t, 15, ib, {c: -1 for c in cuts}, cuts)
        vb = v._cut_value("rho", xb, t, 15, ib, {c: 1 for c in cuts}, cuts)
        x = xa + 0.25 * (xb - xa)
        self.assertAlmostEqual(solid(v, math.exp(x), t)[0], va + 0.25 * (vb - va), delta=1e-9 * va)
        got = v.state(math.exp(x), t)
        self.assertTrue(any(ma.MULTI_NOTE in n.text for n in got[2]))


def tb_cell(tb, p, t):
    return next(c for c in tb["cells"] if (c["p"], c["t"]) == (p, t))


class Ends(unittest.TestCase):
    """68 M2 and r2's R1: past a curve's ends the read side comes from the read cell's corner labels on the row nearest
    the curve past the end; nodes are classified by label; corners that decide nothing fall back to the nearest row."""

    def test_label_rule_left_of_the_curve(self):
        tb = table(t_end=1250.0, third="cpx+opx")
        v = view(tb)
        p = pb_const(1200.0) * 0.98
        got = solid(v, p, 1205.0)                              # rows 1150–1300: 1300 past the end, by label
        self.assertLess(rel(got[0], rho_of(p, 1205.0)), 1e-3)
        self.assertGreater(v.cut_counts["label_rule_rows"], 0)

    def test_closing_edge_reads_without_refusal(self):
        """r2's R1 test: past a closing edge (the gt field ends at 1400 K) no read refuses «no read-side node»; the
        nearest-row mutant (the read's side by the last row's P_b) reads the closed gt side where the read cell straddles
        the end (1410 K: the gt row 1400 K in its stencil, off by the planted 2 %). Wholly past the end (1460 K) the
        side no longer matters under P0′: ol+opx differs from ol+opx+gt by an edge, so both sides admit the same nodes."""
        tb = table(cls="edge_in", right="ol+opx+gt")
        p = pb_const(1400.0) * 1.003                          # right of where the curve was
        for t in (1410.0, 1460.0):                            # straddling the end, and a cell wholly past it
            v = view(tb)
            got = v._solid(p, t)
            self.assertNotIsInstance(got, st.Stop, (t, getattr(got, "record", None)))
            self.assertLess(rel(got[0], rho_of(p, t)), 1e-3)  # the closed field reads as the left label's
            mut = view(tb)
            mut._read_side = lambda c, p_, t_, ia, ib: c.side_of(p_, t_)
            if t == 1410.0:
                self.assertGreater(rel(solid(mut, p, t)[0], rho_of(p, t)), 1e-2)

    def test_before_the_curve_starts(self):
        tb = table()                                          # the curve starts at 1000 K
        v = view(tb)
        p = pb_const(1000.0) * 1.003
        got = v._solid(p, 990.0)
        self.assertNotIsInstance(got, st.Stop)
        self.assertLess(rel(got[0], rho_of(p, 990.0)), 1e-3)  # below 1000 K the right label is absent: the left side

    def test_mixed_corner_takes_the_matching_side(self):
        """One corner on the left label, the other on a third label: the read is on the left side (68)."""
        tb = table(t_end=1250.0, third="cpx+opx")
        v = view(tb)
        p = math.sqrt(PS[15] * pb_const(1200.0))              # inside the curve's cell, left of P_b
        got = v._solid(p, 1260.0)                             # corner row 1300: column 15 left label, 16 third
        self.assertNotIsInstance(got, st.Stop)
        self.assertLess(rel(got[0], rho_of(p, 1260.0)), 1e-3)
        self.assertEqual(v.cut_counts["side_fallbacks"], 0)

    def test_no_match_falls_back_and_drops_the_row(self):
        """Both corners on a third label past the end: the nearest row decides (counted). P0′ rejects the third-label
        nodes (a swap-type difference from the read's corner, wa+opx), so corner row 1300 has no read-side node and
        drops ((A″) S1, counted), as the outer row 1350 does; the read answers the right side's ρ from rows 1200–1250.
        The pre-(A″) rule refused here."""
        tb = table(t_end=1250.0, third="cpx+opx")
        v = view(tb)
        p = math.sqrt(PS[16] * PS[17])                        # right of the curve, both corners third past the end
        got = v._solid(p, 1260.0)
        self.assertNotIsInstance(got, st.Stop)
        self.assertLess(rel(got[0], rho_of(p, 1260.0) * (1 + OFF)), 2e-3)
        self.assertEqual((v.cut_counts["side_fallbacks"], v.cut_counts["no_node_refusals"]), (1, 0))
        self.assertEqual((v.cut_counts["row_drop_reads"], v.cut_counts["row_drop_max"]), (1, 1))

    def test_no_row_left_refuses_by_name(self):
        """S1 refuses only when no stencil row keeps a read-side node: planted by rejecting every node."""
        tb = table()
        v = view(tb)
        v._node_ok = lambda j, k, side, cuts: False
        got = v._solid(pb_const(1200.0) * 1.003, 1210.0)
        self.assertIsInstance(got, st.Stop)
        self.assertIn("no read-side node in any stencil row (1150–1300 K)", got.record.why)
        self.assertEqual(v.cut_counts["no_node_refusals"], 1)

    def test_corner_row_extrapolates_within_the_cap(self):
        """68 S1, N1, E11; r2 on 68 B2: a steep curve moves six columns in 50 K, so at the upper corner row the right
        side's nodes all lie beyond the stencil span; the row reads only nodes within CORNER_REACH columns of the read's
        cell (here one, 4 columns out), counted once per read with its reach. Nine columns: none within the cap, so the
        row drops (S1); the uncapped mutant extrapolates from 9 columns out."""
        def steep(n):
            def pb(t):
                a, b = math.log(math.sqrt(PS[13] * PS[14])), math.log(math.sqrt(PS[13 + n] * PS[14 + n]))
                w = min(max((t - 1200.0) / 50.0, 0.0), 1.0)
                return math.exp(a + w * (b - a))
            return pb
        t = 1205.0
        v = view(table(pb=steep(6), t_lo=1150.0, t_hi=1300.0))
        p = v._curves[0].p_b(t) * 1.001                       # right of the curve at the read's T (P_b linear in T)
        got = solid(v, p, t)[0]
        self.assertEqual(v.cut_counts["corner_extrapolations"], 1)
        self.assertEqual((v.cut_counts["corner_max_reach"], v.cut_counts["corner_max_nodes"]), (4, 1))
        self.assertLess(rel(got, rho_of(p, t) * (1 + OFF)), 2e-3)
        tb = table(pb=steep(9), t_lo=1150.0, t_hi=1300.0)
        v = view(tb)
        p = v._curves[0].p_b(t) * 1.001
        self.assertNotIsInstance(v._solid(p, t), st.Stop)
        self.assertEqual((v.cut_counts["row_drop_reads"], v.cut_counts["corner_max_reach"]), (1, 0))
        v = view(table(pb=steep(6), t_lo=1150.0, t_hi=1300.0))
        p6 = v._curves[0].p_b(t) * 1.001
        ia6 = max(i for i in range(len(PS) - 1) if PS[i] <= p6)
        v._region = lambda k, x, side: (PS[ia6], PS[ia6 + 2])   # a region holding no node beyond the span
        self.assertNotIsInstance(v._solid(p6, t), st.Stop)
        self.assertEqual((v.cut_counts["row_drop_reads"], v.cut_counts["corner_extrapolations"]), (1, 0))
        orig, ma.CORNER_REACH = ma.CORNER_REACH, 99           # the mutant: no cap
        try:
            mut = view(tb)
            mut._solid(p, t)
            self.assertGreater(mut.cut_counts["corner_max_reach"], 4)
        finally:
            ma.CORNER_REACH = orig

    def test_region_stops_at_the_next_curve(self):
        """S1's region: a corner row never takes nodes past the next cut curve. With two cut curves 3 columns apart, the
        region of a read between them is exactly the interval between their P_b (a no-region mutant returns (0, ∞))."""
        def edges(t):
            a, b = math.sqrt(PS[15] * PS[16]), math.sqrt(PS[18] * PS[19])
            e = {"converged": True, "location_error": 0.0, "by_amount_only": False, "delta_rho": 0.02,
                 "over_tolerance": True}
            return [{**e, "phase": "gt", "p_b": a, "p_b_driving_force": a, "p_b_amount": a},
                    {**e, "phase": "wa", "p_b": b, "p_b_driving_force": b, "p_b_amount": b}]
        v = view(table(cls="edge_in", right="ol+opx+gt", edges=edges))
        self.assertEqual(len(v._cut), 2)
        lo, hi = v._region(TS.index(1200.0), math.log(PS[17]), {c: (1 if c.p_b(1200.0) < PS[17] else -1) for c in v._cut})
        self.assertEqual((lo, hi), (math.sqrt(PS[15] * PS[16]), math.sqrt(PS[18] * PS[19])))

    def test_corner_without_a_cell_refuses_as_uncut(self):
        """68 E2: a cut read whose read-side corner has no cell (the column's window ended) refuses above the solid
        window, as the uncut path does; it never extrapolates there."""
        tb = table(tops={16: 1150.0})                         # column 16 (right of the curve) ends at 1150 K
        v = view(tb)
        got = v._solid(pb_const(1200.0) * 1.003, 1210.0)
        self.assertIsInstance(got, st.Stop)
        self.assertEqual(got.record.refusal, "input.material_above_solid_window")


class Crossing(unittest.TestCase):
    """68 B1 and B2: the crossing test covers the whole stencil T interval; the p_dataset cut stays in cut reads."""

    def test_curve_crossing_between_rows(self):
        """P_b at column 5.5 up to 1200 K and 20.5 from 1250 K; a read at column 8.5, 1205 K is left of P_b(1205) and its
        stencil's upper rows are across the curve, though no sampled P_b lies in the span."""
        def jump(t):
            return math.sqrt(PS[5] * PS[6]) if t <= 1200.0 else math.sqrt(PS[20] * PS[21])
        tb = table(pb=jump, t_lo=1050.0, t_hi=1350.0)
        v = view(tb)
        p, t = math.sqrt(PS[8] * PS[9]), 1205.0
        self.assertTrue(v._crossing(p, t, 8, int((t - TS[0]) // 50)))
        side = v._curves[0].side_of(p, t)
        want = rho_of(p, t) * (1 + OFF if side > 0 else 1.0)
        self.assertLess(rel(solid(v, p, t)[0], want), 1e-3)

    def test_p_dataset_cut_in_cut_reads(self):
        """A cut read near the dataset top does not move when every cell above p_dataset is perturbed (as uncut)."""
        def top(t):
            return math.sqrt(PS[25] * PS[26])
        tb = table(pb=top, p_dataset=PS[27])
        pert = copy.deepcopy(tb)
        for c in pert["cells"]:
            if c["p"] > PS[27]:
                c["rho"] *= 1.5
        p, t = math.sqrt(PS[26] * PS[27]), 1210.0
        self.assertTrue(view(tb)._crossing(p, t, 26, int((t - TS[0]) // 50)))
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
        self.assertIsNone(v.boundary_pressure(tr[2], 1500.0))  # absent past the curve's last row
        evs = [e for e in events.record_events(v) if e.name.startswith("phase:")]
        self.assertEqual(len(evs), 1)
        y = [0.0, pb_const(1200.0) * 1.01, 1200.0]
        self.assertAlmostEqual(evs[0].g(0.0, y), pb_const(1200.0) * 0.01, delta=1.0)

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
    everything else is cut; S1 drops a starved row; P0′ admits past a curve's end unless the label differs by a swap."""

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
        """Read as uncut (cubic2, bit for bit against boundaries pending), and still landed as an event; the planted
        control (the same rows over tolerance) cuts."""
        tb = table(cls="edge_in", right="ol+opx+gt", edges=within_tol)
        pend = copy.deepcopy(tb)
        pend["boundaries"] = {"status": "pending"}
        v, w = view(tb), view(pend)
        self.assertEqual(v._cut, [])
        p_b, t = pb_const(1200.0), 1210.0
        for p in (p_b * 0.999, p_b * 1.001, math.sqrt(PS[14] * PS[15])):
            self.assertEqual(solid(v, p, t)[:3], solid(w, p, t)[:3])
        self.assertEqual(len(v.transitions()), 1)
        over = copy.deepcopy(tb)
        for r in over["boundaries"]["rows"]:
            r["edges"][0]["over_tolerance"] = True
        self.assertTrue(view(over)._crossing(p_b, t, 15, int((t - TS[0]) // 50)))

    def test_node_resolved_reads_across_with_its_band(self):
        """Never forced into a step (§3.3): read as uncut, with NODE_NOTE carrying P_b and the band; landed as an
        event of kind «node»."""
        tb = node_resolved(table())
        pend = copy.deepcopy(tb)
        pend["boundaries"] = {"status": "pending"}
        v, w = view(tb), view(pend)
        self.assertEqual(v._cut, [])
        p, t = pb_const(1200.0) * 1.001, 1210.0
        self.assertEqual(solid(v, p, t)[:3], solid(w, p, t)[:3])
        notes = [n.text for n in v.state(p, t)[2] if ma.NODE_NOTE in getattr(n, "text", "")]
        band = 0.5 * (PS[16] - PS[15]) / 1e9
        pb = pb_const(1200.0) / 1e9                           # constant over the curve: the range is one value
        self.assertEqual(notes, [f"{ma.NODE_NOTE}; P_b {pb:.4g}–{pb:.4g} GPa, band ± {band:.3g}–{band:.3g} GPa"])
        self.assertEqual(notes, [n.text for n in v.state(p, 1255.0)[2] if ma.NODE_NOTE in getattr(n, "text", "")])
        self.assertFalse(any(ma.NODE_NOTE in getattr(n, "text", "") for n in v.state(PS[25] * 1.1, t)[2]))   # not in another cell
        self.assertEqual([c.kind for c in v._curves], ["node"])
        self.assertEqual(len(v.transitions()), 1)

    def test_p0_prime_past_the_end(self):
        """Past a curve's end a node whose label differs from the read's corner by an edge is admitted; by a swap,
        rejected. 68 M2's «label must equal» (the pre-(A″) rule) rejects both."""
        for third, want in (("wa+opx+gt", True), ("cpx+opx", False)):
            v = view(table(t_end=1250.0, third=third))
            (c,) = v._cut
            k = TS.index(1300.0)                              # past the curve's last row 1250 K
            v._ref = (ma._labels("wa+opx"), 16)
            self.assertIs(v._node_ok(17, k, {c: 1}, [c]), want, third)
            self.assertTrue(v._node_ok(17, k - 1, {c: 1}, [c]))        # defined at 1250 K: M1, right of P_b
        v = view(table(t_end=1250.0, third="cpx+opx"))
        (c,) = v._cut
        k = TS.index(1300.0)
        v._ref = None                                         # no reference corner: admitted
        self.assertTrue(v._node_ok(17, k, {c: 1}, [c]))
        v._ref = (ma._labels("wa+opx"), 16)
        v._cells.pop((PS[17], TS[k]))                          # no cell: not admitted
        self.assertFalse(v._node_ok(17, k, {c: 1}, [c]))

    def test_reference_corner_passes_m1(self):
        """_set_ref takes the nearest corner on the read's side at its own row: a read just right of P_b gets the right
        corner's label, never the nearer-in-ln-P left corner across the curve."""
        v = view(table(t_end=1250.0, third="cpx+opx"))
        (c,) = v._cut
        t = 1210.0
        ib = int((t - TS[0]) // 50)
        x = math.log(PS[16] * 0.999)                          # right of P_b, nearer column 16 than 15 in ln P
        v._set_ref(x, t, 15, ib, {c: 1}, [c])
        self.assertEqual(v._ref, (ma._labels("wa+opx"), 16))
        def pb_low(t):                                        # P_b at 0.2 of the 15→16 cell in ln P
            return math.exp(math.log(PS[15]) + 0.2 * (math.log(PS[16]) - math.log(PS[15])))
        v = view(table(pb=pb_low))
        (c,) = v._cut
        x = math.log(PS[15]) + 0.3 * (math.log(PS[16]) - math.log(PS[15]))   # right of P_b, nearer column 15
        self.assertLess(x - math.log(PS[15]), math.log(PS[16]) - x)
        self.assertNotEqual(tb_cell(table(pb=pb_low), PS[15], 1200.0)["assemblage"], "wa+opx")
        v._set_ref(x, t, 15, ib, {c: 1}, [c])
        self.assertEqual(v._ref, (ma._labels("wa+opx"), 16))  # the M1-less mutant takes column 15's ol+opx

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

    def test_starved_corner_row_drops(self):
        """S1: a corner row with no read-side node in the read's region drops and the read answers; the mutant that
        refuses on a starved corner row (the pre-(A″) rule) refuses the same read."""
        tb = table(t_end=1250.0, third="cpx+opx")
        p = math.sqrt(PS[16] * PS[17])
        self.assertNotIsInstance(view(tb)._solid(p, 1260.0), st.Stop)
        mut = view(tb)

        def starve(k, x, side):
            raise ma._NoNode(k)
        mut._region = starve
        self.assertIsInstance(mut._solid(p, 1260.0), st.Stop)


class Disclosures(unittest.TestCase):
    """§5's per-table disclosures: edge δ, multi-curve cells, T-direction changes split located/unlocated (68 M5)."""

    def test_edge_delta_and_t_changes(self):
        tb = table(cls="edge_in", right="ol+opx+gt", pb=pb_slope)
        d = ma.boundary_disclosures(record(tb["p_dataset"]), tb)
        self.assertEqual(d["curves"]["edge"], 1)
        self.assertEqual(d["edge_delta"]["n"], 9)                       # rows 1000–1400 K: at 1400 K, the curve's
        self.assertEqual(d["edge_delta"]["unreadable"], [])             # last row, the starved 1450 K row drops (S1)
        self.assertGreater(d["edge_delta"]["max"], 1e-2)               # the planted 2 % offset
        self.assertTrue(d["over_tolerance"])
        self.assertTrue(d["t_changes"]["located"])                     # the sloped curve crosses columns between rows
        self.assertTrue(all(x["on_curve"] == 0 for x in d["t_changes"]["located"]))
        self.assertTrue(d["t_changes"]["unlocated"])                    # the region's T ends (950/1000, 1400/1450)
        self.assertGreater(d["sweep"]["cut_reads"], 0)
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
        """(A″)'s disclosures: each row's read mode, the smoothing over rows read across, P0′'s past-end admissions."""
        tb = table(cls="edge_in", right="ol+opx+gt", edges=within_tol)
        d = ma.boundary_disclosures(record(tb["p_dataset"]), tb)
        n = len(tb["boundaries"]["rows"])
        self.assertEqual(d["read"]["counts"], {"cut": 0, "across": n, "node": 0})
        self.assertEqual(d["across"]["e_smooth"]["edge"]["n"] + d["across"]["skipped"], n)
        self.assertGreater(d["across"]["node_to_node"]["edge"]["max"][0], 1e-2)     # the planted 2 % across the cell
        self.assertEqual(d["sweep"]["cut_reads"], 0)
        d = ma.boundary_disclosures(record(tb["p_dataset"]), node_resolved(table()))
        self.assertEqual(d["read"]["counts"]["node"], len(tb["boundaries"]["rows"]))
        tb = table(t_end=1250.0, third="wa+opx+gt")                    # past the end, an edge-type label
        d = ma.boundary_disclosures(record(tb["p_dataset"]), tb)
        self.assertEqual(d["read"]["counts"]["cut"], len(tb["boundaries"]["rows"]))
        self.assertGreater(d["sweep"]["p0_prime"]["edge_type_nodes"], 0)
        tb = table(t_end=1250.0, third="cpx+opx")                      # … and a swap-type one
        self.assertGreater(ma.boundary_disclosures(record(tb["p_dataset"]), tb)["sweep"]["p0_prime"]
                           ["swap_type_rejected_nodes"], 0)


if __name__ == "__main__":
    unittest.main()
