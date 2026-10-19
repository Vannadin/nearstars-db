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
    """Post-freeze note 1 (r2 2c9018f3, addenda 1 ff656fed and 2 705a59e9): past a reach-0 end every row holding the
    curve takes its side against P_b(T_end), and a node past the end leaves the end row out of its T slope; the one
    remaining step is at P_b(T_end), with the swap's sign, and is landed."""

    @classmethod
    def setUpClass(cls):
        cls.v = _bse_view()
        cls.c = next(c for c in cls.v._cut if c.kind == "swap" and c.t0 == 1600.0 and c.stop_lo)

    def jump(self, p, field="rho"):
        lo, hi = p * math.exp(-1e-9), p * math.exp(1e-9)
        if field == "s":
            return self.v.s_path(hi, T_STEP).v - self.v.s_path(lo, T_STEP).v
        return self.v.state(hi, T_STEP)[0] - self.v.state(lo, T_STEP)[0]

    def test_no_step_at_the_outer_row_own_p_b(self):
        # before the fix: ρ −0.63 kg/m³ here (row 1650's +47.9 through a negative cubic weight)
        p = self.c.p_b(1650.0)                           # row 1650's own P_b (23.3415 GPa, a P node)
        self.assertLess(abs(self.jump(p)), 1e-3)
        self.assertLess(abs(self.jump(p, "s")), 1e-4)

    def test_the_landed_step_has_the_swap_sign(self):
        pb = self.c.p_b(1600.0)
        self.assertGreater(self.jump(pb), 1.0)            # the 660: ρ rises across it

    def test_the_own_geometry_fallback_is_red(self):
        # the mutant: no forced side and no node exclusion past a reach-0 end (the pre-fix read)
        from unittest import mock
        v = _bse_view()
        p = self.c.p_b(1650.0)
        with mock.patch.object(type(v), "_node_excl", lambda self, ib: None), \
                mock.patch.object(type(v), "_side_pb", lambda self, c, t: c.p_b_ext(t, self._reach)):
            self.assertLess(v.state(p * math.exp(1e-9), T_STEP)[0] - v.state(p * math.exp(-1e-9), T_STEP)[0], -0.1)

    def test_the_event_is_the_read_s_step(self):
        i = self.v._events.index(self.c)
        bp = lambda t: self.v.boundary_pressure({"form": "assemblage_curve", "id": i}, t)
        self.assertEqual(bp(T_STEP), self.c.p_b(1600.0))    # the cell next to the end: landed at P_b(T_end)
        self.assertIsNone(bp(1540.0))                        # the second cell: no step, no event
        self.assertIsNone(bp(1550.0))                        # the end row's weight is 0 at the far node
        # the read's discontinuity sits where the event says: bisect the ρ jump
        lo, hi = math.log(self.c.p_b(1600.0)) - 1e-3, math.log(self.c.p_b(1600.0)) + 1e-3
        r = lambda x: self.v.state(math.exp(x), T_STEP)[0]
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if r(mid) - r(lo) > 0.5 * (r(hi) - r(lo)):
                hi = mid
            else:
                lo = mid
        self.assertAlmostEqual(math.exp(hi) / bp(T_STEP), 1.0, delta=1e-9)

if __name__ == "__main__":
    unittest.main()
