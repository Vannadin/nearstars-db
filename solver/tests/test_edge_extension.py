# edge 곡선 끝 너머 확장 시험 — 참 끝은 안쪽 기울기를 잇다 평평해지는 C¹ 꼴, 안쪽 run 끝은 부모 곡선을 ψ 로 따라가다 평평 (규소 등록 사후 노트 8, s 읽기 사후 노트 5)
"""Silicate registration post-freeze note 8 (artifacts rewrite/phase2-silicate-record-registration.frozen.md, note blob
a8c67010; 68's design eecf1761, r2 clear ef6b62b6) and s-read post-freeze note 5 (86f56c0a): an edge curve's position
past a cut run's end.
- (a) a true curve end: x_b = ln P_e ± s1·g(τ), g = τ − τ²/(2Δ_c) up to Δ_c, Δ_c/2 after, None past the reach;
- (b′) an interior run end (note 8 delta 1, 6c819825): x_eff = x_r(t_e), the run row's own boundary, for 0 < τ ≤ reach;
- swaps keep the ln-linear extension.
Plants and the seven mutants of note 8 §4, each built from the module's own source.

    solver/.venv/bin/python -m unittest solver.tests.test_edge_extension
"""
import inspect
import math
import textwrap
import unittest
from unittest import mock

from solver import material_assemblage as ma
from solver.tests.test_s_read import _view

RECORDS = ("silicate_slb_default_bse", "silicate_slb_earth_dmm_wh2005", "silicate_slb_mars_khan2022")
#: bse curve 275 (cpx edge, 2250–2300 K, P_b 12.5 → 86.3 MPa): the s-read B1 dip in its outer-only cell
#: (r2 88ea23dc: −1.96 at 1.28 GPa, 2370 K on b1207fe2; −1.925 at 1.267 GPa on the note 3 tip)
DIP = (1.267e9, 2370.0)


def _mutant(old, new, fn="_edge_ext"):
    """The method `fn` of _Curve with `old` replaced by `new` in its source (one occurrence)."""
    src = textwrap.dedent(inspect.getsource(getattr(ma._Curve, fn)))
    assert src.count(old) == 1, (fn, old)
    ns = dict(vars(ma))
    exec(src.replace(old, new), ns)
    return ns[fn]


def _slope(c, t, reach):
    """d ln P_b_ext / dT at t, from a Dual T."""
    got = c.p_b_ext(ma.Dual(t, 0.0, 1.0), reach)
    return None if got is None else (got.dt / got.v if isinstance(got, ma.Dual) else 0.0)


def _ends(v):
    for c in v._cut:
        if c.kind == "edge":
            for hi in (True, False):
                if not (c.stop_hi if hi else c.stop_lo):
                    yield c, hi


class Shape(unittest.TestCase):
    """Note 8 §2's properties on every edge end of the three records."""

    @classmethod
    def setUpClass(cls):
        cls.views = {rid: _view(rid, s_read=False) for rid in RECORDS}

    def check_in_range(self):
        """No-touch set (a): inside every edge run's own T range the position is P_b(T), bit for bit."""
        n = 0
        for v in self.views.values():
            for c in v._cut:
                if c.kind != "edge":
                    continue
                for r, q in zip(c.rows, c.rows[1:] + [None]):
                    ts = [r["t"]] + ([0.5 * (r["t"] + q["t"])] if q else [])
                    for t in ts:
                        self.assertEqual(c.p_b_ext(t, v._reach), c.p_b(t))
                        n += 1
        return n

    def test_in_range_is_untouched(self):
        self.assertGreater(self.check_in_range(), 0)

    def check_shape(self):
        """A true end: C¹ at the end row and at Δ_c (|Δ d ln P/dT| ≤ 1e-12 relative to the inside slope's scale), flat
        on [Δ_c, reach]. An interior end (delta 1): P_b(t_e) held from the end row on, C⁰ at t_e, slope 0 past it. Both:
        None past the reach."""
        counts = {"true": 0, "interior": 0}
        for v in self.views.values():
            for c, hi in _ends(v):
                sgn = 1.0 if hi else -1.0
                te = c.t1 if hi else c.t0
                dc = (c.dc_hi if hi else c.dc_lo) or v._reach / ma.EXT_ROWS
                interior = c.interior_hi if hi else c.interior_lo
                h = 1e-13 * dc
                if interior:
                    pe = c.rows[-1 if hi else 0]["p_b"]
                    held = [c.p_b_ext(te + sgn * v._reach * j / 16, v._reach) for j in range(1, 17)]
                    with self.subTest(curve=c.id, hi=hi, at="held"):
                        self.assertEqual(set(held), {pe})
                        self.assertEqual(c.p_b_ext(te, v._reach), pe)
                        self.assertEqual(_slope(c, te + sgn * h, v._reach), 0.0)
                        self.assertIsNone(c.p_b_ext(te + sgn * (v._reach + 1e-6), v._reach))
                    counts["interior"] += 1
                    continue
                else:
                    rs = c.rows
                    e, o = (rs[-1], rs[-2] if len(rs) > 1 else None) if hi else (rs[0], rs[1] if len(rs) > 1 else None)
                    xr = 0.0 if o is None or o["p_b"] == e["p_b"] else (e["p_b"] - o["p_b"]) / ((e["t"] - o["t"]) * e["p_b"])
                    scale = max(abs(xr), 1e-12)
                out = _slope(c, te + sgn * h, v._reach)
                with self.subTest(curve=c.id, hi=hi, at="t_e"):
                    self.assertLessEqual(abs(out - xr), 1e-12 * scale + 1e-15)
                a, b = _slope(c, te + sgn * (dc - h), v._reach), _slope(c, te + sgn * (dc + h), v._reach)
                with self.subTest(curve=c.id, hi=hi, at="t_e + Δ_c"):
                    self.assertLessEqual(abs(a - b), 1e-12 * scale + 1e-15)
                    self.assertEqual(b, 0.0)
                flat = [c.p_b_ext(te + sgn * (dc + (v._reach - dc) * j / 8), v._reach) for j in range(9)]
                with self.subTest(curve=c.id, hi=hi, at="tail"):
                    self.assertEqual(len(set(flat)), 1, flat)
                    self.assertIsNone(c.p_b_ext(te + sgn * (v._reach + 1e-6), v._reach))
                counts["interior" if interior else "true"] += 1
        return counts

    def test_c1_flat_tail_and_reach(self):
        got = self.check_shape()
        self.assertGreater(got["true"], 0)
        self.assertGreater(got["interior"], 0)

    def test_one_row_true_edge_is_constant(self):
        n = 0
        for v in self.views.values():
            for c, hi in _ends(v):
                if len(c.rows) == 1 and not (c.interior_hi if hi else c.interior_lo):
                    sgn = 1.0 if hi else -1.0
                    te = c.t1 if hi else c.t0
                    for j in range(1, 9):
                        self.assertEqual(c.p_b_ext(te + sgn * v._reach * j / 8, v._reach), c.rows[0]["p_b"])
                    n += 1
        self.assertGreater(n, 0)

    def check_swaps(self):
        """Swaps keep the ln-linear extension (note 8 §1), bit for bit with its formula."""
        n = 0
        for v in self.views.values():
            for c in v._cut:
                if c.kind != "swap" or len(c.rows) < 2:
                    continue
                for hi in (True, False):
                    if c.stop_hi if hi else c.stop_lo:
                        continue
                    rs = c.rows
                    e, o = (rs[-1], rs[-2]) if hi else (rs[0], rs[1])
                    t = (c.t1 + 0.7 * v._reach) if hi else (c.t0 - 0.7 * v._reach)
                    want = e["p_b"] if o["p_b"] == e["p_b"] else e["p_b"] * ma._exp(
                        (t - e["t"]) * (math.log(e["p_b"]) - math.log(o["p_b"])) / (e["t"] - o["t"]))
                    self.assertEqual(c.p_b_ext(t, v._reach), want)
                    n += 1
        # on the regenerated records every true swap end is reach 0: a planted cut swap with open ends
        reach = next(iter(self.views.values()))._reach
        c = ma._Curve(0, "swap", None, [{"t": 1000.0, "p_b": 2.0e9}, {"t": 1050.0, "p_b": 2.4e9}])
        t = 1050.0 + 0.7 * reach
        self.assertEqual(c.p_b_ext(t, reach),
                         2.4e9 * ma._exp((t - 1050.0) * (math.log(2.4e9) - math.log(2.0e9)) / (1050.0 - 1000.0)))
        return n + 1

    def test_swaps_keep_the_ln_linear_extension(self):
        self.assertGreater(self.check_swaps(), 0)


class OuterOnlyCellSign(unittest.TestCase):
    """Note 8 §4's plant (r2 n6: > 0): bse 275's outer-only cell, where the ln-linear extension put the window's T term
    in with the outer row's negative weight (∂s/∂T −1.925 at 1.267 GPa, 2370 K)."""

    def _ds_dt(self, p, t):
        v = _view("silicate_slb_default_bse")
        return v.s_path(p, t).dt

    def test_positive_after_negative_under_ln_linear(self):
        p, t = DIP
        self.assertGreater(self._ds_dt(p, t), 0.0)
        lnlin = _mutant('    if self.kind == "edge":\n        return self._edge_ext(', '    if False:\n        return self._edge_ext(',
                        fn="p_b_ext")
        with mock.patch.object(ma._Curve, "p_b_ext", lnlin):
            self.assertLess(self._ds_dt(p, t), 0.0)


class Mutants(unittest.TestCase):
    """Note 8 §4's mutants, each red on the check that names it."""

    def _red(self, check, method, mut):
        with mock.patch.object(ma._Curve, method, mut):
            sh = Shape()
            sh.views = {rid: _view(rid, s_read=False) for rid in RECORDS}
            with self.assertRaises(AssertionError):
                with mock.patch.object(Shape, "subTest", lambda *a, **k: _Null()):
                    check(sh)

    def test_flat_from_the_end(self):            # no decay: the slope break at t_e
        self._red(Shape.check_shape, "_edge_ext",
                  _mutant("g = tau - tau * tau / (2.0 * dc) if tau <= dc else 0.5 * dc", "g = 0.0 * tau"))

    def test_decay_over_two_rows(self):          # a T term in the outer-only cell
        self._red(Shape.check_shape, "_edge_ext",
                  _mutant("g = tau - tau * tau / (2.0 * dc) if tau <= dc else 0.5 * dc",
                          "g = tau - tau * tau / (4.0 * dc) if tau <= 2.0 * dc else dc"))

    def test_rule_on_swaps(self):
        self._red(lambda sh: sh.check_swaps(), "p_b_ext",
                  _mutant('    if self.kind == "edge":\n        return self._edge_ext(',
                          '    if True:\n        return self._edge_ext(', fn="p_b_ext"))

    def test_rule_inside_the_range(self):        # τ ≤ 0: no-touch set (a)
        self._red(Shape.check_in_range, "p_b_ext",
                  _mutant("    if pb is not None:\n        return pb\n",
                          "    if pb is not None and self.kind != 'edge':\n        return pb\n", fn="p_b_ext"))

    def test_parent_throughout_the_reach(self):  # x_r in the outer-only cell (delta 1 §4: stays red)
        self._red(Shape.check_shape, "_edge_ext",
                  _mutant("    if self.interior_hi if hi else self.interior_lo:\n        return e[\"p_b\"]\n",
                          "    if self.interior_hi if hi else self.interior_lo:\n"
                          "        return self.parent.p_b_ext(t, reach)\n"))


PSI = ("    if self.interior_hi if hi else self.interior_lo:\n        return e[\"p_b\"]\n",
       "    if self.interior_hi if hi else self.interior_lo:\n"
       "        dc = (self.dc_hi if hi else self.dc_lo) or reach / EXT_ROWS\n"
       "        tau = (t - e[\"t\"]) if hi else (e[\"t\"] - t)\n"
       "        if tau >= dc:\n            return e[\"p_b\"]\n"
       "        u = tau / dc\n        psi = 1.0 - u * u * (3.0 - 2.0 * u)\n"
       "        return e[\"p_b\"] * _exp((_log(self.parent.p_b(t)) - math.log(e[\"p_b\"])) * psi)\n")


class InteriorEnds(unittest.TestCase):
    """Note 8 delta 1 §4's plants and the ψ mutant."""

    def test_one_row_interior_runs_are_the_base_read(self):
        """A one-row interior run holds its own P_b over its whole extension: the base read (af12d75b), which kept a
        one-row curve constant, bit for bit; no-touch set (c) gains these ends."""
        n = 0
        for rid in RECORDS:
            v = _view(rid, s_read=False)
            for c in v._cut:
                if c.kind != "edge" or len(c.rows) != 1:
                    continue
                for hi in (True, False):
                    if not (c.interior_hi if hi else c.interior_lo):
                        continue
                    sgn = 1.0 if hi else -1.0
                    for j in range(1, 9):
                        self.assertEqual(c.p_b_ext(c.t0 + sgn * v._reach * j / 8, v._reach), c.rows[0]["p_b"])
                    n += 1
        self.assertGreater(n, 0)

    def _step_875(self):
        """The Envelope test's step at bse 875 K between the 11.64 and 12.22 GPa cell centres (ia 115 → 116)."""
        v = _view("silicate_slb_default_bse", s_read=False)
        a, b = (v._solid(math.sqrt(v.ps[j] * v.ps[j + 1]), 875.0)[0] for j in (115, 116))
        return b / a - 1.0

    def test_psi_tracking_mutant_is_red_at_curve_83(self):
        """Delta 1's control: ψ tracking in the corner cell puts curve 83's fall between the 875 K cell centres (the
        Envelope test's −1.011e-4); the held boundary does not (+2.660e-4). The fall itself is the base's, G3's to gate."""
        self.assertGreater(self._step_875(), 0.0)
        with mock.patch.object(ma._Curve, "_edge_ext", _mutant(*PSI)):
            self.assertLess(self._step_875(), -1e-4)


class _Null:
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


if __name__ == "__main__":
    unittest.main()
