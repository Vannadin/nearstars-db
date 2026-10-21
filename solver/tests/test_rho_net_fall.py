# ρ 보수의 순하강 규칙 시험(r2 a69976dc) — 넓혀 되찾기, 착지 스왑이 흡수하는 평평한 끝, 경계가 스왑이 아니면 STOP
"""The net-fall rules of the ρ fall build (r2 a69976dc, the khan 2000 K case; no size floor):
(1) b′ widens right, the side that regains, up to the next landed step or p_dataset;
(2) b′ on a landed step's near side and still a net fall: the read ends the bridge flat at R(a′), the step's upward
    jump absorbing the fall (it must stay ≥ 0);
(3) any other bound: a STOP, naming it.
The khan 2000 K window (swap299's high-end row) is a few hundred reads (seconds)."""
import math
import unittest
from unittest import mock

from solver import material_assemblage as ma, rho_fall_build as rb

KHAN = "silicate_slb_mars_khan2022"
T = 2000.0
XLO, XHI = 23.80, 23.95


def _khan():
    try:
        return rb._view(KHAN)
    except Exception as e:                               # the regenerated record is not shipped here
        raise unittest.SkipTest(f"{KHAN}: {e}")


class _Uncapped(unittest.TestCase):
    """rev3d D4 caps the widening at the cell's ρ band / 10. These plants test the rules downstream of it (rules 1–3,
    the rev3b class 3 clip), as built before the cap: the band is set out of reach (τ_w 100, never crossed, so each
    end sits at C_WIDEN·extent as before). D4 itself is test_rho_rev3d's."""

    def setUp(self):
        p = mock.patch.object(rb, "_band_at", lambda v, x, ib: 1e3)
        p.start()
        self.addCleanup(p.stop)


def _fake(swap_at=None, jump=0.0):
    """A fake read for falls_at: R = 1000 + 0.004·cos(π(x − 2)) on ln P cells of 1, plus `jump` past a landed swap at
    `swap_at` (ln P). Returns (the view class, R, g)."""
    class Swap:
        kind = "swap"
        t0 = t1 = 0.0

        def p_b_ext(self, t, reach):
            return math.exp(swap_at)
    sw = [Swap()] if swap_at is not None else []

    class Fake:
        lnps = [float(k) for k in range(9)]
        ts = [0.0, 1.0]
        _cut, _events, _reach = sw, sw, 0
        p_dataset = math.exp(8.0)

        def _partition(self, k):
            return []

        def _width(self, x):
            return 1.0

        def _swap_has_lambda(self, c):
            return False                                 # rev3d amendment 2 delta 2: the fake's swap owns no step
    up = (lambda x: jump if swap_at is not None and x > swap_at else 0.0)               # noqa: E731
    r = lambda x: 1000.0 + 0.004 * math.cos(math.pi * (x - 2.0)) + up(x)               # noqa: E731
    g = lambda x: (r(x), -0.004 * math.pi * math.sin(math.pi * (x - 2.0)) / r(x))      # noqa: E731
    return Fake, r, g


def _swap299(v):
    """khan's 1950–2000 K swap, found by position (its rows and its P_b at 2000 K), not by id: the gap marks renumber
    the cut runs (299 before them, 271 after); the name keeps the old id."""
    (c,) = [c for c in v._cut if c.kind == "swap" and (c.t0, c.t1) == (1950.0, 2000.0)
            and abs(c.p_b(2000.0) / 23317173540.3313 - 1.0) <= 1e-12]
    return c


class Rule1Widens(_Uncapped):
    def test_widen_regains_inside_the_bound(self):
        # R dips 1e-3 below R(a′) at b′ = 2 and rises at 0.01 per ln P: it regains at 2.1
        r = lambda x: 1000.0 - 1e-3 + 0.01 * (x - 2.0)   # noqa: E731
        g = lambda x: (r(x), 0.01 / r(x))                 # noqa: E731
        got, refused = rb._widen(g, g, 1.0, 2.0, 1000.0, 3.0, 0.01)
        self.assertFalse(refused)
        self.assertAlmostEqual(got, 2.1, places=9)
        self.assertGreaterEqual(r(got), 1000.0)           # the end that holds: R(b′) ≥ R(a′) exactly

    def test_widen_never_crosses_the_bound(self):
        # the regain lies past the bound (a landed step's near side at 2.05): no widening
        r = lambda x: 1000.0 - 1e-3 + 0.01 * (x - 2.0)   # noqa: E731
        g = lambda x: (r(x), 0.01 / r(x))                 # noqa: E731
        self.assertEqual(rb._widen(g, g, 1.0, 2.0, 1000.0, 2.05, 0.01), (None, False))

    def test_falls_at_widens_a_net_fall(self):
        # R = 1000 + 0.004·cos(π(x − 2)) on a fake read (no swaps): the fall from the max at 2 regains near 4, widened
        # by C_WIDEN to about [xlo = 1.2, 5], where R(b′) < R(1.2): a net fall; R regains R(a′) at 4 + a′ < xhi
        Fake, r, g = _fake()
        with mock.patch.object(rb, "_reader", lambda v, t, ib, un: g):
            iv, un, stops, _fl, _sj, ex = rb.falls_at(Fake(), 0.0, 0, 1.2, 5.6)
        self.assertEqual(stops, [])
        (w,) = ex["widened"]
        self.assertLess(r(w["was_b"]), r(w["a"]))          # the net fall it started from
        self.assertAlmostEqual(w["b"], 4.0 + w["a"], places=6)   # cos(π(b − 2)) = cos(π(a − 2)) on (5, 6)
        self.assertGreaterEqual(r(w["b"]), r(w["a"]))
        self.assertIn((w["a"], w["b"]), [(a, b) for a, b, _a, _c in iv])
        with mock.patch.object(rb, "_reader", lambda v, t, ib, un: g), mock.patch.object(rb, "_widen",
                                                                                        lambda *a: (None, False)):
            _iv, _un, stops2, _fl, _sj, _ex = rb.falls_at(Fake(), 0.0, 0, 1.2, 5.6)
        self.assertEqual([s_["bound"] for s_ in stops2], ["the window's end"])   # the mutant (no widening): STOP


class Rule2SwapAbsorbs(_Uncapped):
    def test_khan_2000_is_absorbed_by_swap299(self):
        v = _khan()
        for ib in (35, 36):                              # 2000 K is both cells' end sample
            with self.subTest(ib=ib):
                iv, _un, stops, _fl, _sj, ex = rb.falls_at(v, T, ib, XLO, XHI)
                self.assertEqual(stops, [])
                self.assertEqual(ex["widened"], [])
                (ab,) = ex["absorbed"]
                self.assertEqual(ab["by"], v._events.index(_swap299(v)))     # the clip is swap299 itself
                self.assertAlmostEqual(ab["b"], ab["x"] - rb.SWAP_EPS, delta=1e-15)
                self.assertGreater(ab["dR"], 0.0)
                self.assertLess(ab["dR"], 2e-3)          # 1.05e-3 kg/m³ on the PC and here
                self.assertGreater(ab["jump"], 100.0)    # +283 kg/m³: the landed step stays upward

    def _read_ends(self, v, flat_on, sliver_on=True):
        _iv, _un, _st, _fl, _sj, ex = rb.falls_at(v, T, 36, XLO, XHI)
        ab = ex["absorbed"][0]
        sets = {35: [(ab["a"], ab["b"])], 36: [(ab["a"], ab["b"])], 37: [(ab["a"], ab["b"])]}
        orig = ma.AssemblageView._fall_bridge

        def bridge(self, x, t, ib, x0, x1, flat=False, sliver=False):
            if sliver and not sliver_on:
                return None                              # the mutant: R itself in the sliver
            return orig(self, x, t, ib, x0, x1, flat and flat_on, sliver)
        # every read inside the patches, the repair on whatever NS_RHO_BRIDGE says (the PC's repair-off suite ran
        # these with the bridge off, and a read after the block met the real set file)
        with mock.patch.object(ma, "RHO_BRIDGE", True), \
                mock.patch.object(type(v), "_fall_set_load", lambda self: sets), \
                mock.patch.object(type(v), "_fall_bridge", bridge):
            r = lambda x: v.state(math.exp(x), T)[0]     # noqa: E731
            xs = (ab["a"] + 1e-6, 0.5 * (ab["a"] + ab["b"]), ab["b"] - 1e-6, ab["x"] - 0.5 * rb.SWAP_EPS,
                  ab["x"] + 2e-9)
            return [r(x) for x in xs], ab

    def test_the_read_ends_flat_and_the_swap_stays_upward(self):
        v = _khan()
        vals, ab = self._read_ends(v, True)
        self.assertGreaterEqual(vals[1] - vals[0], 0.0)
        self.assertGreaterEqual(vals[2] - vals[1], 0.0)  # no fall to the swap's near side
        self.assertGreater(vals[4] - vals[2], 100.0)     # past the swap

    def test_the_sliver_before_the_swap_reads_flat(self):
        # r2 c40f792a: a read at x_swap − SWAP_EPS/2 (past b′, before the swap) is the flat R(a′), not R falling by ΔR
        v = _khan()
        vals, ab = self._read_ends(v, True)
        self.assertEqual(vals[3], vals[1])
        vals_m, _ab = self._read_ends(v, True, sliver_on=False)
        self.assertLess(vals_m[3], vals_m[1] - 0.5 * ab["dR"])          # the mutant «own in the sliver» falls

    def test_the_secant_mutant_falls(self):
        # the old read: the secant from R(a′) to R(b′) ships the 1e-3 fall
        v = _khan()
        vals, _ab = self._read_ends(v, False)
        self.assertLess(vals[2], vals[0])


    def test_a_short_end_runs_flat_to_the_swap(self):
        # the cosine fake with an upward swap (+1 kg/m³) at 5.1, before R's own regain at 4 + a′ ≈ 5.2: the walk meets
        # the swap's near side without regaining, so b′ moves there and the swap's jump absorbs the fall
        Fake, r, g = _fake(5.1, 1.0)
        with mock.patch.object(rb, "_reader", lambda v, t, ib, un: g):
            iv, _un, stops, _fl, _sj, ex = rb.falls_at(Fake(), 0.0, 0, 1.2, 5.6)
        self.assertEqual(stops, [])
        self.assertTrue(ex["absorbed"])
        moved = [ab for ab in ex["absorbed"] if ab["was_b"] < ab["b"]]
        self.assertTrue(moved, ex["absorbed"])
        for ab in moved:
            self.assertEqual(ab["by"], 0)
            self.assertEqual(ab["b"], 5.1 - rb.SWAP_EPS)
            self.assertIn((ab["a"], ab["b"]), [(a, b) for a, b, _a, _c in iv])
            self.assertGreaterEqual(ab["jump"], 0.0)


class Rule3OtherBoundStops(_Uncapped):
    def test_a_downward_swap_cannot_absorb(self):
        # the same with a downward swap (−1): its jump from R(a′) is negative, so the STOP stands, naming the swap
        Fake, r, g = _fake(5.1, -1.0)
        with mock.patch.object(rb, "_reader", lambda v, t, ib, un: g):
            _iv, _un, stops, _fl, _sj, ex = rb.falls_at(Fake(), 0.0, 0, 1.2, 5.6)
        self.assertEqual(ex["absorbed"], [])
        nf = [s_ for s_ in stops if s_["why"] == "net fall over the widened interval"]
        self.assertTrue(nf, stops)
        self.assertTrue(all(s_["bound"].startswith("swap 0 (its jump") for s_ in nf), nf)

    def test_a_bound_that_is_not_a_swap_stops(self):
        # the window ends inside the fall, before swap299: the bound is no landed step, so the STOP stands, named
        v = _khan()
        xs = math.log(_swap299(v).p_b_ext(T, v._reach))
        _iv, _un, stops, _fl, _sj, ex = rb.falls_at(v, T, 35, XLO, xs - 5e-5)
        nf = [s for s in stops if s["why"] == "net fall over the widened interval"]
        self.assertTrue(nf, stops)
        self.assertEqual(nf[0]["bound"], "the window's end")
        self.assertEqual(ex["absorbed"], [])


def _mutant(old, new):
    """rho_fall_build with one source line replaced (a rule taken back), as its own module."""
    import types
    src = open(rb.__file__, encoding="utf-8").read()
    assert src.count(old) == 1, old
    mut = types.ModuleType("rho_fall_build_mutant")
    mut.__file__ = rb.__file__
    exec(compile(src.replace(old, new), rb.__file__, "exec"), mut.__dict__)
    return mut


def _ibt(v, t):
    import bisect
    return min(max(bisect.bisect_right(v.ts, t) - 1, 0), len(v.ts) - 2)


DMM, BSE = "silicate_slb_earth_dmm_wh2005", "silicate_slb_default_bse"


class FloorOnTheFallLine(unittest.TestCase):
    # r2 8e0d13fa (rev3b class 2): a floor cell whose ends and secant are ≥ THR is no fall though R decreases
    CELLS = ((DMM, 1946.875, 23.202116088), (BSE, 884.375, 20.491211847))
    #: the rev3b PC's third cell; silicate note 8's edge extension (8bfb1c15) changed the read there, and it now screens
    #: as fall-free (no slow descent left): it must still build with no STOP
    GONE = ((BSE, 3675.0, 24.070046623),)

    def test_the_slow_descents_build(self):
        for rid, t, x in self.GONE:
            with self.subTest(rid=rid, t=t, gone=True):
                v = rb._view(rid)
                _iv, _un, stops, _fl, _sj, ex = rb.falls_at(v, t, _ibt(v, t), x - 0.01, x + 0.01)
                self.assertEqual((stops, ex["slow_floor"]), ([], []))
        for rid, t, x in self.CELLS:
            with self.subTest(rid=rid, t=t):
                v = rb._view(rid)
                _iv, _un, stops, _fl, _sj, ex = rb.falls_at(v, t, _ibt(v, t), x - 0.01, x + 0.01)
                self.assertEqual(stops, [])
                self.assertTrue(ex["slow_floor"])
                for c in ex["slow_floor"]:
                    self.assertGreaterEqual(c["secant"], rb.THR)
                    self.assertLess(c["secant"], 0.0)            # R does decrease there

    def test_the_old_floor_rule_stops(self):
        mut = _mutant("if fa[1] >= THR and fb[1] >= THR and d >= THR:", "if False:")
        rid, t, x = self.CELLS[0]
        v = rb._view(rid)
        with self.assertRaises(mut.Unresolved):
            mut.falls_at(v, t, _ibt(v, t), x - 0.01, x + 0.01)


class WideningClippedAtARefusal(_Uncapped):
    # r2 8e0d13fa (rev3b class 3): dmm 4200 K, cell 79 — the read refuses below ln P ≈ 23.055 (eos_edge) and the
    # widened a′ reached it
    def test_the_widened_end_is_clipped(self):
        v = rb._view(DMM)
        _iv, _un, stops, _fl, _sj, ex = rb.falls_at(v, 4200.0, 79, 22.9, 23.2)
        self.assertEqual([s_ for s_ in stops if s_["why"] == "a widened end the read can't evaluate"], [])
        (cl,) = [c for c in ex["clipped"] if c["side"] == "lo"]
        un = []
        g = rb._reader(v, 4200.0, 79, un)
        self.assertIsNone(g(cl["was"]))
        self.assertIsNotNone(g(cl["now"]))
        self.assertLess(cl["now"] - cl["was"], 0.02)

    def test_without_the_clip_it_stops(self):
        mut = _mutant("            if g(end) is None:\n", "            if False:\n")
        v = rb._view(DMM)
        _iv, _un, stops, _fl, _sj, _ex = mut.falls_at(v, 4200.0, 79, 22.9, 23.2)
        self.assertTrue([s_ for s_ in stops if s_["why"] == "a widened end the read can't evaluate"])


class CoincidentEdgeCensus(unittest.TestCase):
    # directing 10-20 (r2 e843daa8): the coincident edge pairs re-kinded as swaps are marked, with their extrapolation
    def test_bse_850_is_a_coincident_edge_pair_on_its_row(self):
        # since swap-extension note 2 the pair has a P_b only on its own row (reach 0), where it is a true crossing
        from solver.tests.test_swap_extension import _pair850     # by position: the gap marks renumber the ids
        v = rb._view(BSE)
        pair = _pair850(v)
        t = 850.0
        _iv, _un, _st, _fl, sj, _ex = rb.falls_at(v, t, _ibt(v, t), 23.774, 23.794)
        ce = [j for j in sj if j["curve"] in pair]
        self.assertEqual(len(ce), 2)
        self.assertTrue(all(j["coincident_edge"] and j["extrap_k"] == 0.0 for j in ce), ce)
        census = rb._coincident_edge_census(sj, [], [])
        self.assertEqual((census["n"], census["on_rows"], census["extrapolated"]), (2, 2, 0))
        _iv, _un, _st, _fl, sj2, _ex = rb.falls_at(v, 753.125, _ibt(v, 753.125), 23.774, 23.794)
        self.assertEqual([j for j in sj2 if j["curve"] in pair], [])     # none 97 K past its row
        self.assertTrue(all(not j["coincident_edge"] for j in sj if j["curve"] not in pair))


if __name__ == "__main__":
    unittest.main()
