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


def _fake(swap_at=None, jump=0.0):
    """A fake read for falls_at: R = 1000 + 0.004·cos(π(x − 2)) on ln P cells of 1, plus `jump` past a landed swap at
    `swap_at` (ln P). Returns (the view class, R, g)."""
    class Swap:
        kind = "swap"

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
    up = (lambda x: jump if swap_at is not None and x > swap_at else 0.0)               # noqa: E731
    r = lambda x: 1000.0 + 0.004 * math.cos(math.pi * (x - 2.0)) + up(x)               # noqa: E731
    g = lambda x: (r(x), -0.004 * math.pi * math.sin(math.pi * (x - 2.0)) / r(x))      # noqa: E731
    return Fake, r, g


def _swap299(v):
    return next(c for c in v._cut if c.kind == "swap" and v._events.index(c) == 299)


class Rule1Widens(unittest.TestCase):
    def test_widen_regains_inside_the_bound(self):
        # R dips 1e-3 below R(a′) at b′ = 2 and rises at 0.01 per ln P: it regains at 2.1
        r = lambda x: 1000.0 - 1e-3 + 0.01 * (x - 2.0)   # noqa: E731
        g = lambda x: (r(x), 0.01 / r(x))                 # noqa: E731
        got, why = rb._widen(g, g, 1.0, 2.0, 1000.0, 3.0, 0.01)
        self.assertIsNone(why)
        self.assertAlmostEqual(got, 2.1, places=9)
        self.assertGreaterEqual(r(got), 1000.0)           # the end that holds: R(b′) ≥ R(a′) exactly

    def test_widen_never_crosses_the_bound(self):
        # the regain lies past the bound (a landed step's near side at 2.05): no widening
        r = lambda x: 1000.0 - 1e-3 + 0.01 * (x - 2.0)   # noqa: E731
        g = lambda x: (r(x), 0.01 / r(x))                 # noqa: E731
        self.assertEqual(rb._widen(g, g, 1.0, 2.0, 1000.0, 2.05, 0.01), (None, "bound"))

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
                                                                                        lambda *a: (None, "bound")):
            _iv, _un, stops2, _fl, _sj, _ex = rb.falls_at(Fake(), 0.0, 0, 1.2, 5.6)
        self.assertEqual([s_["bound"] for s_ in stops2], ["the window's end"])   # the mutant (no widening): STOP


class Rule2SwapAbsorbs(unittest.TestCase):
    def test_khan_2000_is_absorbed_by_swap299(self):
        v = _khan()
        for ib in (35, 36):                              # 2000 K is both cells' end sample
            with self.subTest(ib=ib):
                iv, _un, stops, _fl, _sj, ex = rb.falls_at(v, T, ib, XLO, XHI)
                self.assertEqual(stops, [])
                self.assertEqual(ex["widened"], [])
                (ab,) = ex["absorbed"]
                self.assertEqual(ab["by"], 299)          # the clip is swap299 itself
                self.assertAlmostEqual(ab["b"], ab["x"] - rb.SWAP_EPS, delta=1e-15)
                self.assertGreater(ab["dR"], 0.0)
                self.assertLess(ab["dR"], 2e-3)          # 1.05e-3 kg/m³ on the PC and here
                self.assertGreater(ab["jump"], 100.0)    # +283 kg/m³: the landed step stays upward

    def _read_ends(self, v, flat_on):
        _iv, _un, _st, _fl, _sj, ex = rb.falls_at(v, T, 36, XLO, XHI)
        ab = ex["absorbed"][0]
        sets = {35: [(ab["a"], ab["b"])], 36: [(ab["a"], ab["b"])], 37: [(ab["a"], ab["b"])]}
        orig = ma.AssemblageView._fall_bridge
        bridge = orig if flat_on else (lambda self, x, t, ib, x0, x1, flat=False: orig(self, x, t, ib, x0, x1, False))
        with mock.patch.object(type(v), "_fall_set_load", lambda self: sets), \
                mock.patch.object(type(v), "_fall_bridge", bridge):
            r = lambda x: v.state(math.exp(x), T)[0]     # noqa: E731
            return [r(x) for x in (ab["a"] + 1e-6, 0.5 * (ab["a"] + ab["b"]), ab["b"] - 1e-6)], ab, r

    def test_the_read_ends_flat_and_the_swap_stays_upward(self):
        v = _khan()
        vals, ab, r = self._read_ends(v, True)
        self.assertGreaterEqual(vals[1] - vals[0], 0.0)
        self.assertGreaterEqual(vals[2] - vals[1], 0.0)  # no fall to the swap's near side
        self.assertGreater(r(ab["x"] + 2e-9) - vals[2], 100.0)

    def test_the_secant_mutant_falls(self):
        # the old read: the secant from R(a′) to R(b′) ships the 1e-3 fall
        v = _khan()
        vals, _ab, _r = self._read_ends(v, False)
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


class Rule3OtherBoundStops(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
