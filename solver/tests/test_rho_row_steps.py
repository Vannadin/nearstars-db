# ρ 보수의 외삽 0 행 계단 시험 — 빌더가 내리막 행 계단을 다리 놓을 하강으로, 오르막을 적힌 계단으로 다루는지(«unresolved» 아님), 보수가 오르막에서 구간을 쪼개는지
"""The ρ repair on the reach-0 read (swap extension note 1, r2 addendum 4 (4); the PC stage-1 STOPs of 10-19).

The build listed only swaps with a P_b_ext as landed steps, so every other value step reached the resolution floor
as «unresolved»: the reach-0 holding-row steps (their own P_b, weighted by the row's T weight) all STOPped. Here: the
first STOP cell of each record on the PC builds, a narrow window, with no STOP; the downward step bridged, the upward
one listed and landed. One window solves a few hundred reads (seconds)."""
import math
import unittest
from unittest import mock

from solver import material_assemblage as ma, material_registry as mr, rho_fall_build as rb
from solver.tests import test_assemblage_c1 as tc

BSE = "silicate_slb_default_bse"


def _view(rid):
    reg = mr.load()
    if rid not in reg.tables or "extension" not in reg.tables[rid].get("boundaries", {}):
        raise unittest.SkipTest("the regenerated record (with the extension block) is not shipped here")
    return tc._view(reg, rid)


def _ib(v, t):
    return min(max(i for i, q in enumerate(v.ts) if q <= t), len(v.ts) - 2)


class BuildKnowsRowSteps(unittest.TestCase):
    def test_the_first_stop_cells_build(self):
        # PC 10-19: bse 656.25 K at ln P 22.351331646, dmm 1062.5 at 23.379150256, khan 721.875 at 22.452545210 —
        # each a downward holding-row step (−0.484 / −0.396 / −0.065 kg/m³); dmm's also STOPped on the shipped records
        for rid, t, lo, hi in ((BSE, 656.25, 5.0, 5.3), ("silicate_slb_earth_dmm_wh2005", 1062.5, 14.2, 14.5),
                               ("silicate_slb_mars_khan2022", 721.875, 5.5, 5.75)):
            with self.subTest(rid=rid):
                v = _view(rid)
                iv, _un, stops, _fl, _sj, ex = rb.falls_at(v, t, _ib(v, t), math.log(lo * 1e9), math.log(hi * 1e9))
                self.assertEqual(stops, [])
                downs = [r for r in ex["row_steps"] if r["jump"] < 0.0]
                self.assertTrue(downs)
                for r in downs:                          # each downward step lies inside a fall interval (bridged)
                    self.assertTrue(any(a < r["x"] < b for a, b, _a, _c in iv), (r, iv))

    def test_an_upward_step_is_landed_not_bridged(self):
        v = _view(BSE)
        t = 656.25
        iv, _un, stops, _fl, sj, ex = rb.falls_at(v, t, _ib(v, t), math.log(5.0e9), math.log(5.3e9))
        ups = [r for r in ex["row_steps"] if r["jump"] >= 0.0]
        self.assertTrue(ups)                             # row 650's +10.8 kg/m³
        for r in ups:
            self.assertFalse(any(a < r["x"] < b for a, b, _a, _c in iv), (r, iv))
        self.assertFalse(any(isinstance(j.get("curve"), str) for j in sj))   # never in the swap gate's list

    def test_the_old_build_stops_there(self):
        # the mutant: no row steps known (as before the fix) — the downward step reaches the floor and STOPs
        v = _view(BSE)
        t = 656.25
        with mock.patch.object(type(v), "_row_step_p", lambda self, i, t: None):
            with self.assertRaises(rb.Unresolved):
                rb.falls_at(v, t, _ib(v, t), math.log(5.0e9), math.log(5.3e9))


class SwapOnTheGrid(unittest.TestCase):
    def test_a_swap_on_a_grid_point_is_listed_not_screened(self):
        # PC rev3b: a one-row swap pair (bse's at 850 K, khan's at 1100 K; ids 168/170 and 123/124 before the across-gap
        # marks, found by position since) has its P_b on its own
        # row's partition point, so xs is a grid point and its jump sits at a half-cell's end; the strict skip let a
        # downward one bisect to the floor («unresolved»). Since note 2 (reach 0 for coincident-edge swaps) the pair
        # has a P_b at its own row only, where it still meets the grid
        from solver.tests.test_rho_zero_height import _pair
        from solver.tests.test_swap_extension import _pair850
        for rid, t, find in ((BSE, 850.0, _pair850), ("silicate_slb_mars_khan2022", 1100.0, _pair)):
            with self.subTest(rid=rid):
                v = _view(rid)
                ids = tuple(find(v))                     # by position: the gap marks renumber the ids
                xs = next(math.log(c.p_b_ext(t, v._reach)) for c in v._cut if c.kind == "swap"
                          and v._events.index(c) == ids[0])
                _iv, _un, stops, _fl, sj, _ex = rb.falls_at(v, t, _ib(v, t), xs - 0.01, xs + 0.01)
                self.assertEqual(stops, [])
                got = [j for j in sj if j["curve"] in ids]
                self.assertEqual(sorted(j["curve"] for j in got), sorted(ids))
                self.assertTrue(all(j["x"] == xs for j in got), got)                     # listed for the gate

    def test_the_strict_skip_stops_there(self):
        # the mutant: rho_fall_build with the old open skip (a < xs < b), loaded from its own source — the half-cell
        # ending on xs is screened and STOPs
        import types
        src = open(rb.__file__, encoding="utf-8").read()
        self.assertEqual(src.count("any(a <= xs_ <= b for xs_, _c in swaps)"), 1)
        mut = types.ModuleType("rho_fall_build_open_skip")
        mut.__file__ = rb.__file__
        exec(compile(src.replace("any(a <= xs_ <= b for xs_, _c in swaps)", "any(a < xs_ < b for xs_, _c in swaps)"),
                     rb.__file__, "exec"), mut.__dict__)
        v = _view("silicate_slb_mars_khan2022")
        t = 1100.0                                       # the pair's own row: its jump there is downward (−0.40)
        from solver.tests.test_rho_zero_height import _pair
        xs = next(math.log(c.p_b_ext(t, v._reach)) for c in v._cut if c.kind == "swap"
                  and v._events.index(c) == _pair(v)[0])                 # by position, not id 123
        with self.assertRaises(mut.Unresolved):
            mut.falls_at(v, t, _ib(v, t), xs - 0.01, xs + 0.01)


class RepairSplitsAtUpwardSteps(unittest.TestCase):
    def test_upward_split_downward_bridged(self):
        v = _view(BSE)
        t = 656.25
        ib = _ib(v, t)
        up = next(math.log(q) for i in range(len(v._row_steps)) if (q := v._row_step_p(i, t)) is not None
                  and v.ts[v._row_steps[i][1]] == 650.0)
        down = next(math.log(q) for i in range(len(v._row_steps)) if (q := v._row_step_p(i, t)) is not None
                    and v.ts[v._row_steps[i][1]] == 600.0)
        sets = {ib: [(down - 0.004, up + 0.004)], ib + 1: [(down - 0.004, up + 0.004)]}  # one interval over both
        with mock.patch.object(ma, "RHO_BRIDGE", True), mock.patch.object(type(v), "_fall_set_load", lambda self: sets):
            self.assertEqual(v._row_steps_up(t, ib), [up])
            r = lambda x: v.state(math.exp(x), t)[0]    # noqa: E731
            self.assertGreater(r(up + 2e-9) - r(up - 2e-9), 1.0)            # the upward step stays (split there)
            self.assertGreaterEqual(r(down + 2e-9) - r(down - 2e-9), 0.0)   # the downward one bridged: no fall


if __name__ == "__main__":
    unittest.main()
