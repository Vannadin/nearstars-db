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
          off=OFF, t_lo=1000.0, t_hi=1400.0):
    """Cells to 1600 K, non-frozen from 400 K; the label is `left` below P_b(t) and `right` above it for
    t_lo ≤ t ≤ t_hi (outside, `left` everywhere, or `third` above t_end). Rows of the exported block at every T row
    where the two neighbouring columns of P_b differ in label."""
    cells, cols, rows = [], [], []
    ts = [t for t in TS if t <= 1600.0]
    for i, p in enumerate(PS):
        for t in ts:
            fr = t < 400.0
            lab = left
            inside = t_lo <= t <= t_hi and (t_end is None or t <= t_end)
            if inside and p > pb(t):
                lab = right
            if third is not None and t_end is not None and t > t_end and t_lo <= t <= t_hi:
                lab = third
            r = rho_of(p, t) * (1.0 + off if lab == right else 1.0)
            c = {"p": p, "t": t, "kind": "frozen" if fr else "equilibrium", "assemblage": lab, "rho": r,
                 "c_p": 1200.0 + 0.1 * t, "dtdp_s": 1e-8 * t / 1000.0, "freeze_t": 400.0 if fr else None,
                 "freeze_class": "convergence edge" if fr else None, "dtdp_eq_band": None if fr else 2.5e-4}
            c["dtdp_eq"] = c["dtdp_s"]
            c["c_p_eq"] = None if fr else c["c_p"] * 1.03
            cells.append(c)
        cols.append({"p": p, "t_sol": 1500.0, "t_window_top": ts[-1], "window": {"cause": "grid_end"}})
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
    return {"cells": cells, "columns": cols, "p_dataset": PS[-3],
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
        v0._curves = []                                       # planted control: the cut disabled
        self.assertGreater(rel(solid(v0, left, t)[0], rho_of(left, t)), 1e-3)

    def test_span_one_cell_away(self):
        """68 M3: a read one cell left of the curve's cell still has column 16 in its stencil, and must not use it."""
        tb = table()
        v = view(tb)
        p, t = math.sqrt(PS[14] * PS[15]), 1210.0
        self.assertTrue(v._crossing(p, t, 14, int((t - TS[0]) // 50)))
        self.assertLess(rel(solid(v, p, t)[0], rho_of(p, t)), 1e-5)
        v0 = view(tb)
        v0._curves = []
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
        v0._curves = []                                       # T-first, uncut: reads across
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
            for cc in self._curves:
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
    """68 M2: past a curve's end, nodes are classified by label; a corner row with no read-side node refuses by name;
    an outer row with none drops out."""

    def test_label_rule_and_no_node(self):
        tb = table(t_end=1250.0, third="cpx+opx")             # above 1250 K the right side is a third label
        v = view(tb)
        p = pb_const(1200.0) * 0.98
        got = solid(v, p, 1205.0)                              # rows 1150–1300: 1300 past the end, by label
        self.assertLess(rel(got[0], rho_of(p, 1205.0)), 1e-3)
        self.assertGreater(v.cut_counts["label_rule_rows"], 0)
        q = pb_const(1200.0) * 1.02                            # the right side: its label is gone past the end
        got = v._solid(q, 1255.0)                              # corner row 1300 K has no right-side node
        self.assertIsInstance(got, st.Stop)
        self.assertIn("no read-side node in row 1300 K", got.record.why)
        self.assertEqual(v.cut_counts["no_node_refusals"], 1)

    def test_corner_row_extrapolates_further_out(self):
        """68 S1: a steep curve moves six columns in 50 K, so at the upper corner row the right side's nodes all lie
        beyond the stencil span: the row is read from them (counted, with its reach) and the read answers."""
        def steep(t):
            a, b = math.log(math.sqrt(PS[13] * PS[14])), math.log(math.sqrt(PS[19] * PS[20]))
            w = min(max((t - 1200.0) / 50.0, 0.0), 1.0)
            return math.exp(a + w * (b - a))
        tb = table(pb=steep, t_lo=1150.0, t_hi=1300.0)
        v = view(tb)
        t = 1205.0
        p = v._curves[0].p_b(t) * 1.001                       # right of the curve at the read's T (P_b linear in T)
        got = solid(v, p, t)[0]
        self.assertEqual(v.cut_counts["corner_extrapolations"], 3)       # ρ, dT/dP, c_P each read the row
        self.assertGreaterEqual(v.cut_counts["corner_max_reach"], 3)
        self.assertLess(rel(got, rho_of(p, t) * (1 + OFF)), 2e-2)


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

    def test_duplicate_t_in_a_group(self):
        """68 M6: two rows of one group at one T STOP; the control is the same table without the duplicate."""
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


class Disclosures(unittest.TestCase):
    """§5's per-table disclosures: edge δ, multi-curve cells, T-direction changes split located/unlocated (68 M5)."""

    def test_edge_delta_and_t_changes(self):
        tb = table(cls="edge_in", right="ol+opx+gt", pb=pb_slope)
        d = ma.boundary_disclosures(record(tb["p_dataset"]), tb)
        self.assertEqual(d["curves"]["edge"], 1)
        self.assertEqual(d["edge_delta"]["n"], 8)                       # rows 1000–1350 K …
        self.assertEqual([(u["t"], u["why"]) for u in d["edge_delta"]["unreadable"]], [(1400.0, "_NoNode")])
        # … and 1400 K, the curve's last row: its right side has no node in the corner row 1450 K (the gt field closes)
        self.assertGreater(d["edge_delta"]["max"], 1e-2)               # the planted 2 % offset
        self.assertTrue(d["over_tolerance"])
        self.assertTrue(d["t_changes"]["located"])                     # the sloped curve crosses columns between rows
        self.assertTrue(all(x["on_curve"] == 0 for x in d["t_changes"]["located"]))
        self.assertTrue(d["t_changes"]["unlocated"])                    # the region's T ends (950/1000, 1400/1450)
        self.assertGreater(d["sweep"]["cut_reads"], 0)

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


if __name__ == "__main__":
    unittest.main()
