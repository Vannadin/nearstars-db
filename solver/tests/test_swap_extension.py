# 스왑 연장 행의 읽기 쪽 시험 — 연장 블록이 있는 기록은 스왑 곡선의 바깥 끝에서 외삽 0, 인증 행은 곡선 행, 그 밖(모서리 곡선 · 안쪽 끝 · 블록 없는 기록)은 비트 동일
"""The read's half of the swap-extension registration (frozen 8402255e; r2's addenda, with the Q2 ruling: reach 0 only
at a swap curve's true outer ends, an interior check and its mutant)."""
import copy
import math
import unittest

from solver import material_assemblage as ma

L, R = "ol+opx+cpx+gt", "ol+c2c+cpx+gt"
TS = [600.0 + 50.0 * i for i in range(9)]           # 600 … 1000 K


def swap_row(t, pb):
    return {"t": t, "p_lo": pb - 1e8, "p_hi": pb + 1e8, "left": L, "right": R, "class": "swap", "p_b": pb,
            "converged": True, "delta_rho": 0.003, "delta_s": -2.7}


def edge_row(t, pb, over=False):
    """An edge class row with one converged edge: read across unless `over` (then cut)."""
    return {"t": t, "p_lo": pb - 1e8, "p_hi": pb + 1e8, "left": "gt+st", "right": "gt+st+capv", "class": "edge_in",
            "converged": True, "edges": [{"phase": "capv", "converged": True, "p_b": pb, "delta_rho": 1e-4,
                                          "over_tolerance": over}]}


def block(extension=None):
    rows = [swap_row(t, 5e9 + 4e6 * (t - 700.0)) for t in (700.0, 750.0, 800.0)]
    # an edge curve cut on 700–750 and 850–900, read across at 800: two cut runs with interior ends at 750 and 850
    rows += [edge_row(t, 20e9 + 1e6 * (t - 700.0), over=(t != 800.0)) for t in (700.0, 750.0, 800.0, 850.0, 900.0)]
    b = {"status": "exported", "rows": rows}
    if extension is not None:
        b["extension"] = extension
    return b


EXT_NONE = {"rows": [{"t": 650.0, "left": L, "right": R, "class": "swap", "extension": True, "k": 1,
                      "certified": False, "reason": "cells_disagree"}], "rule": {"ext_rows": 2}}


def curves(b):
    cs = ma.build_curves(b, TS)
    return [c for c in cs if c.kind == "swap"], ma._cut_runs(cs), cs


class SwapExtensionRead(unittest.TestCase):
    def test_without_the_block_the_read_extrapolates_as_today(self):
        sw, _, _ = curves(block())
        c = sw[0]
        self.assertIsNotNone(c.p_b_ext(650.0, 100.0))
        self.assertIsNotNone(c.p_b_ext(850.0, 100.0))

    def test_with_the_block_reach_is_zero_at_the_outer_ends(self):
        sw, _, _ = curves(block(copy.deepcopy(EXT_NONE)))
        c = sw[0]
        self.assertIsNone(c.p_b_ext(650.0, 100.0))
        self.assertIsNone(c.p_b_ext(850.0, 100.0))
        ref, _, _ = curves(block())
        for t in (700.0, 725.0, 800.0):                  # on its own rows: bit-identical
            self.assertEqual(c.p_b_ext(t, 100.0), ref[0].p_b_ext(t, 100.0))

    def test_interior_and_edge_run_ends_are_bit_identical(self):
        # r2 Q2: only a swap curve's true outer ends change. The edge curve's cut runs end at 750 (next to the row read
        # across at 800) and at 850: their extrapolation is the same with and without the block. The mutant «reach 0
        # at every run end» makes these differ, so this test is red against it
        _, runs_on, _ = curves(block(copy.deepcopy(EXT_NONE)))
        _, runs_off, _ = curves(block())
        edges_on = [c for c in runs_on if c.kind == "edge"]
        edges_off = [c for c in runs_off if c.kind == "edge"]
        self.assertEqual(len(edges_on), 2)
        for a, b in zip(edges_on, edges_off):
            for t in (650.0, 775.0, 800.0, 825.0, 950.0):
                self.assertEqual(a.p_b_ext(t, 100.0), b.p_b_ext(t, 100.0), (t, a.t0, a.t1))
        self.assertIsNotNone(edges_on[0].p_b_ext(775.0, 100.0))   # an interior run end still extrapolates

    def test_a_certified_extension_row_is_a_row_of_its_curve(self):
        ext = copy.deepcopy(EXT_NONE)
        ext["rows"].append({**swap_row(850.0, 5e9 + 4e6 * 150.0), "extension": True, "k": 1, "certified": True})
        sw, _, _ = curves(block(ext))
        c = sw[0]
        self.assertEqual(c.t1, 850.0)
        self.assertEqual(c.p_b(850.0), 5e9 + 4e6 * 150.0)
        self.assertIsNone(c.p_b_ext(900.0, 100.0))       # past the last certified row: reach 0



BSE = "silicate_slb_default_bse"
T_STEP = 1568.5                      # in the cell [1550, 1600], next to swap277's reach-0 end at 1600 K


def _bse_view():
    from solver import material_registry as mr
    from solver.tests import test_assemblage_c1 as tc
    reg = mr.load()
    if BSE not in reg.tables or "extension" not in reg.tables[BSE].get("boundaries", {}):
        raise unittest.SkipTest("the regenerated bse record (with the extension block) is not shipped here")
    return tc._view(reg, BSE)


class ReachZeroEnds(unittest.TestCase):
    """Post-freeze note 1 (r2 addendum 4 143d0a96): past a reach-0 end the read takes no side for the curve and each
    stencil row holding it steps at its own P_b(T_k), weighted by its T weight; every such step is a landed event
    (form assemblage_row_step) while the read cell's stencil holds the row. Monotone ρ is the ρ repair's."""

    @classmethod
    def setUpClass(cls):
        cls.v = _bse_view()
        cls.c = next(c for c in cls.v._cut if c.kind == "swap" and c.t0 == 1600.0 and c.stop_lo)
        cls.steps = [x[2] for x in cls.v.transitions() if x[2]["form"] == "assemblage_row_step"]

    def events(self, t):
        return sorted(q for e in self.steps if (q := self.v.boundary_pressure(e, t)) is not None)

    def test_events_are_the_holding_rows_own_p_b(self):
        self.assertEqual(self.events(T_STEP), sorted([self.c.p_b(1600.0), self.c.p_b(1650.0)]))
        self.assertEqual(self.events(1525.0), [self.c.p_b(1600.0)])      # 1650 is out of [1500, 1550]'s stencil
        self.assertEqual(self.events(1475.0), [])                          # 1600 is out of [1450, 1500]'s stencil
        self.assertEqual(self.events(1600.0), [])                          # the curve has its P_b there

    def bisect_step(self, p, t, field=0):
        lo, hi = math.log(p) - 1e-4, math.log(p) + 1e-4
        r = lambda x: self.v.state(math.exp(x), t)[field]
        a, b = r(lo), r(hi)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if abs(r(mid) - a) < abs(r(mid) - b):
                lo = mid
            else:
                hi = mid
        return math.exp(hi)

    def test_the_read_steps_at_the_events(self):
        # the walk lands on the read's discontinuities only if they are where the events say (1568.5 K: row 1650's
        # +47.9 kg/m³ enters with a negative T weight, −0.63; row 1600's with a positive one)
        for q in self.events(T_STEP):
            j = self.v.state(q * math.exp(1e-9), T_STEP)[0] - self.v.state(q * math.exp(-1e-9), T_STEP)[0]
            self.assertGreater(abs(j), 0.1, q)
            self.assertAlmostEqual(self.bisect_step(q, T_STEP) / q, 1.0, delta=1e-9)

    def test_the_s_path_steps_at_the_same_events(self):
        for q in self.events(T_STEP):
            j = self.v.s_path(q * math.exp(1e-9), T_STEP).v - self.v.s_path(q * math.exp(-1e-9), T_STEP).v
            self.assertGreater(abs(j), 1e-3, q)

    def test_no_events_is_red(self):
        # the mutant: no row-step events; a step of the read is then where no event is
        from unittest import mock
        v = _bse_view()
        with mock.patch.object(type(v), "_row_step_p", lambda self, i, t: None):
            got = [q for x in v.transitions() if x[2]["form"] == "assemblage_row_step"
                   if (q := v.boundary_pressure(x[2], T_STEP)) is not None]
        self.assertEqual(got, [])
        q = self.c.p_b(1650.0)
        self.assertGreater(abs(self.v.state(q * math.exp(1e-9), T_STEP)[0] - self.v.state(q * math.exp(-1e-9), T_STEP)[0]),
                           0.1)                                            # the read does step there: unlanded

if __name__ == "__main__":
    unittest.main()
