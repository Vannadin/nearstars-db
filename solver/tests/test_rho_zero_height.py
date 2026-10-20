# ρ rev3c 시험 — 일치 가장자리 쌍의 허용 오차 안 내림 계단은 높이 0: 떨어짐 아님·ΔG 없음·게이트 밖·흡수 안 됨·목록에 듦 (68 설계 40d180cc, r2 clear 1916061f)
"""ρ rev 3, rev3c (artifacts main f11695a0, rewrite/rho-bridge/rev3c-zero-height.md, blob 40d180cc): the plants P1–P5
and the mutants M1–M7 of §5, khan only, in a narrow window ln P x_s ± 0.3 at T 1100 K (x_s the coincident pair 123/124's
ln P_b, 24.852 GPa).

    solver/.venv/bin/python -m unittest solver.tests.test_rho_zero_height
"""
import inspect
import math
import os
import textwrap
import unittest
from unittest import mock

from solver import material_assemblage as ma
from solver import rho_fall_build as rfb

RID = "silicate_slb_mars_khan2022"
X_S = 23.936222088018862
T = 1100.0
W = 0.3


def _mutant(fn, old, new, owner=rfb):
    src = textwrap.dedent(inspect.getsource(getattr(owner, fn)))
    assert src.count(old) == 1, (fn, old)
    ns = dict(vars(owner))
    exec(src.replace(old, new), ns)
    return ns[fn]


class _Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v = rfb._view(RID)
        cls.ib = cls.v.ts.index(T)

    def setUp(self):
        for a in ("_rev3c_tol",):                       # the view-kept τ_e: re-read per test (M1 patches it)
            if hasattr(self.v, a):
                delattr(self.v, a)

    def p1(self):
        ivs, _un, stops, _fl, sj, _ur = rfb.falls_at(self.v, T, self.ib, X_S - W, X_S + W)
        mine = [j for j in sj if j["curve"] in (123, 124)]
        return ivs, stops, mine

    def p2(self):
        env = {k: v_ for k, v_ in os.environ.items() if k != "NS_BUILD_ASSEMBLAGE"}
        with mock.patch.dict(os.environ, env, clear=True):
            per = {ib: rfb.cell_falls(self.v, ib, nsub=1, xr=(X_S - W, X_S + W)) for ib in (self.ib - 1, self.ib)}
            return rfb.document(self.v, per)


class Plants(_Base):
    def test_p1_both_curves_zero_height_no_interval_through_x_s(self):
        ivs, stops, mine = self.p1()
        self.assertEqual(sorted(j["curve"] for j in mine), [123, 124])
        for j in mine:
            self.assertTrue(j.get("zero_height"))
            self.assertAlmostEqual(j["rel"], -8.9056e-05, delta=1e-9)
            self.assertEqual(j["tol"], 7.5e-4)
            self.assertEqual(j["pair"], [123, 124])
        self.assertEqual(stops, [])
        self.assertFalse(any(a < X_S < b for a, b, *_ in ivs))

    def test_p2_document_the_pc_shape(self):
        doc = self.p2()
        self.assertEqual(doc["stops"], [])
        self.assertEqual(len(doc["zero_height"]), 1)
        z = doc["zero_height"][0]
        self.assertEqual((z["pair"], z["n"], z["t"]), ([123, 124], 4, T))
        self.assertEqual(doc["swap_counts"]["zero_height"], 1)
        self.assertEqual(doc["coincident_edge"]["gate_stops"], 0)
        self.assertEqual(doc["coincident_edge"]["zero_height"], 1)
        self.assertEqual(doc["stamp"]["rules"]["EDGE_DRHO_TOL"], 7.5e-4)

    def test_p3_the_read_is_untouched(self):
        v = self.v
        self.assertEqual((v._events[123].kind, v._events[124].kind), ("swap", "swap"))
        self.assertTrue(v._events[123].was_edge and v._events[124].was_edge)
        p_lo, p_hi = math.exp(X_S - 2 * rfb.SWAP_EPS), math.exp(X_S + 2 * rfb.SWAP_EPS)
        with mock.patch.object(ma, "RHO_BRIDGE", False):
            base = v.state(p_hi, T)[0] - v.state(p_lo, T)[0]
        saved = v._fall_sets
        try:
            v._fall_sets = {self.ib: [[X_S - 0.01, X_S + 0.01]]}     # a synthetic set straddling x_s at node ib
            with mock.patch.object(ma, "RHO_BRIDGE", True):
                on = v.state(p_hi, T)[0] - v.state(p_lo, T)[0]
        finally:
            v._fall_sets = saved
        self.assertLess(base, 0.0)
        self.assertLess(abs(on - base) / abs(base), 1e-6)

    def test_p4_absorber(self):
        x = 1.0
        swaps = [(x, 7)]
        self.assertIsNone(rfb._absorber(swaps, [x], x - rfb.SWAP_EPS))
        self.assertEqual(rfb._absorber(swaps, [], x - rfb.SWAP_EPS), (x, 7))

    def test_p5_zero_height_reasons(self):
        tol = 7.5e-4
        ok = {"coincident_edge": True, "extrap_k": 0.0, "jump": -1.0, "rel": -tol}
        self.assertIsNotNone(rfb._zero_height(ok, tol))
        self.assertIsNone(rfb._zero_height({**ok, "coincident_edge": False, "rel": -1e-6}, tol))
        self.assertIsNone(rfb._zero_height({**ok, "extrap_k": 50.0}, tol))
        self.assertIsNone(rfb._zero_height({**ok, "rel": -tol * (1 + 1e-9)}, tol))
        self.assertIsNone(rfb._zero_height({**ok, "jump": 1.0, "rel": tol / 2}, tol))
        self.assertIsNone(rfb._zero_height(ok, None))


class Mutants(_Base):
    """Each mutant of §5 red on its named plant."""

    def test_m1_tol_zero(self):
        with mock.patch.object(rfb, "_edge_tol", lambda rid: 0.0):
            _ivs, stops, _mine = self.p1()
            self.assertEqual(sorted(s_["curve"] for s_ in stops if "curve" in s_), [123, 124])
            self.assertTrue(all(s_["gate"] == "coincident-edge downstep above EDGE_DRHO_TOL" for s_ in stops))
            self.setUp()
            self.assertNotEqual(self.p2()["stops"], [])

    def test_m2_zero_height_gated(self):
        mut = _mutant("gate", 'if j["jump"] >= 0.0 or j.get("zero_height"):', 'if j["jump"] >= 0.0:')
        with mock.patch.object(rfb, "gate", mut):
            doc = self.p2()
        self.assertTrue(any(s_.get("gate") == "not evaluated" for s_ in doc["stops"]))

    def test_m3_zero_pair_credited(self):
        mut = _mutant("_absorber", "if xs_ is None or any(abs(xs_ - z) <= 1e-12 for z in zero_x):", "if xs_ is None:")
        self.assertIsNotNone(mut([(1.0, 7)], [1.0], 1.0 - rfb.SWAP_EPS))           # P4's first case goes red

    def test_m4_without_was_edge(self):
        mut = _mutant("_zero_height", 'not j.get("coincident_edge") or ', "")
        self.assertIsNotNone(mut({"coincident_edge": False, "extrap_k": 0.0, "jump": -1.0, "rel": -1e-6}, 7.5e-4))

    def test_m5_with_extrapolation(self):
        mut = _mutant("_zero_height", 'j.get("extrap_k", 0.0) != 0.0 or ', "")
        self.assertIsNotNone(mut({"coincident_edge": True, "extrap_k": 50.0, "jump": -1.0, "rel": -1e-6}, 7.5e-4))

    def test_m6_case_dropped_or_merged(self):
        mut = _mutant("_zero_height_list", 'e["n"] += 1', 'e["n"] = 1')
        with mock.patch.object(rfb, "_zero_height_list", mut):
            doc = self.p2()
        self.assertNotEqual(doc["zero_height"][0]["n"], 4)

    def test_m7_pair_not_a_swap(self):
        mut = _mutant("falls_at", "    def slope(i):", "    swaps[:] = [q for q in swaps if q[0] not in zero_x]\n\n    def slope(i):")
        with mock.patch.object(rfb, "falls_at", mut):
            try:
                ivs, stops, _mine = self.p1()
            except rfb.Unresolved:
                return                                     # red: the screen meets the step
        self.assertTrue(stops or any(a < X_S < b for a, b, *_ in ivs))


if __name__ == "__main__":
    unittest.main()
