# s 읽기 전환 띠 시험 — 얼어붙은 스텐실 전환을 한 T 행에 걸쳐 C¹ 로 섞기, 갇힌 띠의 표시와 받아들인 걸음의 이름 붙은 거절 (s-read 사후 노트 3)
"""s-read post-freeze note 3 (artifacts rewrite/s2-loop-entropy/reg-s-read.frozen.md, note 3 blob 7cb634f6) with note 4's
flags: the frozen-stencil switch blended over one T row (§2.2), its C¹ claim on w (§2.3), the precheck (§2.3's cost
line), the islands (68 n3), 68's planted switch (§6), and the trapping band's refusal on an accepted pass (§2.4).

    solver/.venv/bin/python -m unittest solver.tests.test_s_read_band
"""
import inspect
import math
import textwrap
import unittest
from unittest import mock

from scipy.integrate import solve_ivp

from solver import context, legacy_materials as lm, material_assemblage as ma, solve as sv
from solver.tests.test_p1fix_b2 import _earth
from solver.tests.test_s_read import _view

#: note 3 §1's contours where the band starts, as note 4's flags place them (the cell middle in P; k is the first T cell
#: whose s path holds no frozen node, so cell k − 1 is flagged and the band is cell k), and whether the band traps:
#: bse at 10.56 / 12.22 GPa starts at 1100 K with both reads positive; the 24.2 GPa contours have opposite signs (§1)
POINTS = (("silicate_slb_default_bse", 113, 18, False), ("silicate_slb_default_bse", 116, 18, False),
          ("silicate_slb_default_bse", 130, 24, True), ("silicate_slb_earth_dmm_wh2005", 130, 25, True),
          ("silicate_slb_mars_khan2022", 130, 26, True))


def _at(v, ia):
    return math.sqrt(v.ps[ia] * v.ps[ia + 1])


def _dtdp(v, p, t):
    return v.state(p, t)[1]


class BandOnRecord(unittest.TestCase):
    """§2.2–§2.3 on the three records at §1's contours."""

    @classmethod
    def setUpClass(cls):
        cls.views = {}
        for rid, *_ in POINTS:
            if rid not in cls.views:
                cls.views[rid] = _view(rid)

    def test_the_band_sits_where_the_flags_say(self):
        for rid, ia, k, _trap in POINTS:
            v, = (self.views[rid],)
            p = _at(v, ia)
            d = v.ts[k + 1] - v.ts[k]
            with self.subTest(rid=rid, ia=ia, k=k):
                self.assertIsNone(v._s_path(p, v.ts[k] - d / 2, p, ia, k - 1))          # cell k − 1: frozen stencil
                self.assertIsNotNone(v._s_path(p, v.ts[k] + d / 2, p, ia, k))           # cell k: free
                self.assertIsNotNone(v._s_path(p, v.ts[k + 1] + d / 2, p, ia, k + 1))   # cell k + 1: free
                self.assertEqual(v._band_w(p, v.ts[k], p, ia, k), 0.0)
                self.assertEqual(v._band_w(p, v.ts[k] + d / 2, p, ia, k), 0.5)
                self.assertEqual(v._band_w(p, v.ts[k + 1], p, ia, k), 1.0)
                self.assertEqual(v._band_w(p, v.ts[k + 1], p, ia, k + 1), 1.0)     # cell k + 1 sees no flag below

    def test_w_is_c1_at_both_nodes(self):
        """§2.3 (r2 B2): w and its T-slope agree across both band nodes; S′ = 0 at each end. The slope is taken one-
        sided at h = 1e-6·Δ, where a smoothstep's own slope is 6h/Δ² — so the bound is 1e-5/Δ, not a fixed 1e-12."""
        for rid, ia, k, _trap in POINTS:
            v = self.views[rid]
            p = _at(v, ia)
            d = v.ts[k + 1] - v.ts[k]
            h = 1e-6 * d
            with self.subTest(rid=rid, ia=ia, k=k):
                self.assertLess(v._band_w(p, v.ts[k] + h, p, ia, k) / h, 1e-5 / d)
                self.assertLess((1.0 - v._band_w(p, v.ts[k + 1] - h, p, ia, k)) / h, 1e-5 / d)

    def test_the_switch_adds_no_step_at_either_node(self):
        """§6 «across a band node on the record», as §2.3 states the claim: the blend adds no step. At T_k the field is
        today's read on both sides (cell k − 1 frozen, w = 0 in cell k), at T_k+1 the s read on both sides (w = 1 in
        cells k and k + 1), bit for bit. Those reads' own T-node steps inside (c′) windows are §8's class, not the
        switch's (on the 24.2 GPa contours the s read steps 5e-4 to 6e-4 relative at T_k+1); today's read is
        continuous at T_k to 1e-9 here."""
        for rid, ia, k, _trap in POINTS:
            on, off = self.views[rid], _view(rid, s_read=False)
            p = _at(on, ia)
            eps = 1e-9 * (on.ts[k + 1] - on.ts[k])
            with self.subTest(rid=rid, ia=ia, k=k):
                lo, hi = (_dtdp(on, p, on.ts[k] + e) for e in (-eps, eps))
                self.assertEqual((lo, hi), tuple(_dtdp(off, p, on.ts[k] + e) for e in (-eps, eps)))
                self.assertLess(abs(lo - hi) / abs(lo), 1e-9, (lo, hi))
                for e in (-eps, eps):
                    t = on.ts[k + 1] + e
                    sv_ = on.s_path(p, t)
                    self.assertEqual(_dtdp(on, p, t), -(sv_.dx / p) / sv_.dt)

    def test_band_read_is_the_blend_with_its_note_and_mark(self):
        """§2.2's values at the band's middle (w = 0.5), BAND_NOTE on every band read, and a BandTrap mark exactly
        where the two reads have opposite signs (§2.4)."""
        for rid, ia, k, trap in POINTS:
            on, off = self.views[rid], _view(rid, s_read=False)
            p = _at(on, ia)
            t = on.ts[k] + (on.ts[k + 1] - on.ts[k]) / 2
            with self.subTest(rid=rid, ia=ia, k=k):
                n0 = dict(on.s_counts)
                got, today = on.state(p, t), off.state(p, t)
                sv_ = on.s_path(p, t)
                ds = -(sv_.dx / p) / sv_.dt
                self.assertAlmostEqual(got[1], 0.5 * today[1] + 0.5 * ds, delta=1e-12 * abs(today[1]) + 1e-24)
                self.assertEqual(got[0], today[0])                      # ρ is today's
                self.assertEqual(on.s_counts["band_reads"] - n0["band_reads"], 1)
                self.assertIn(ma.BAND_NOTE, [n.text for n in got[2] if hasattr(n, "text")])
                marks = [n for n in got[2] if isinstance(n, ma.BandTrap)]
                self.assertEqual(bool(marks), trap)
                self.assertEqual(today[1] * ds < 0.0, trap)
                if trap:
                    self.assertLess(marks[0].dtdp_today * marks[0].dtdp_s, 0.0)
                    self.assertEqual(marks[0].w, 0.5)

    def test_sign_mutant_marks_a_same_sign_band(self):
        """Mutant (§2.4): the sign test dropped, so every band read is marked; bse at 10.56 GPa (same sign) goes red."""
        src = textwrap.dedent(inspect.getsource(ma.AssemblageView._with_s))
        self.assertEqual(src.count("if got[1] * dtdp_s < 0.0:"), 1)
        ns = dict(vars(ma))
        exec(src.replace("if got[1] * dtdp_s < 0.0:", "if True:"), ns)
        rid, ia, k, trap = POINTS[0]
        self.assertFalse(trap)
        v = _view(rid)
        p = _at(v, ia)
        t = v.ts[k] + (v.ts[k + 1] - v.ts[k]) / 2
        self.assertFalse(any(isinstance(n, ma.BandTrap) for n in v.state(p, t)[2]))
        with mock.patch.object(ma.AssemblageView, "_with_s", ns["_with_s"]):
            self.assertTrue(any(isinstance(n, ma.BandTrap) for n in v.state(p, t)[2]))

    def test_precheck_reads_no_flag_above_the_frozen_rows(self):
        """§2.3's cost line: at T_ib − 2 above the table's highest frozen T no flag is read (counted), and the answer is
        the s read bit for bit. Mutant: flags always read (the precheck's bound at +∞); the count shows it."""
        rid, ia = "silicate_slb_default_bse", 130
        v = _view(rid)
        p = _at(v, ia)
        ib = next(i for i in range(2, len(v.ts) - 2) if v.ts[i - 2] > v._t_frozen_max)
        t = v.ts[ib] + 10.0
        n0 = v.s_counts["flag_reads"]
        got = v.state(p, t)
        sv_ = v.s_path(p, t)
        self.assertEqual(v.s_counts["flag_reads"], n0)
        self.assertEqual(got[1], -(sv_.dx / p) / sv_.dt)
        with mock.patch.object(v, "_t_frozen_max", math.inf):
            again = v.state(p, t)
        self.assertGreater(v.s_counts["flag_reads"], n0)
        self.assertEqual(again[1], got[1])

    def test_island_one_row(self):
        """68 n3: a planted one-row island, a free cell between two flagged ones: w ≤ 0.25 at its middle (S(½)²),
        today's read in the flagged cells, and w C¹ at both of its nodes (0 with zero slope)."""
        rid, ia, k, _trap = POINTS[2]
        v = _view(rid)
        p = _at(v, ia)
        real = v._s_path

        def planted(p_, t_, pr_, ia_, ib_, force=None):
            return None if ib_ != k else real(p_, t_, pr_, ia_, ib_, force)

        d = v.ts[k + 1] - v.ts[k]
        h = 1e-6 * d
        with mock.patch.object(v, "_s_path", planted), mock.patch.object(v, "_t_frozen_max", math.inf):
            self.assertEqual(v._band_w(p, v.ts[k] + d / 2, p, ia, k), 0.25)
            for tn, sgn in ((v.ts[k], 1.0), (v.ts[k + 1], -1.0)):
                self.assertEqual(v._band_w(p, tn, p, ia, k), 0.0)
                self.assertLess(v._band_w(p, tn + sgn * h, p, ia, k) / h, 1e-5 / d)


class _Layer:
    def __init__(self, lid):
        self.id = lid


class _Body:
    def __init__(self, *ids):
        self.layers = tuple(_Layer(i) for i in ids)


class _Acc:
    def __init__(self, profiles):
        self.profiles = profiles


def _path(p, ts):
    return [(0.0, (0.0, p, t, t), None) for t in ts]


class BasalAndQuietCheck(unittest.TestCase):
    """r2 B1 on e2386b42: a basal layer's dT/dP is the overlying read's, so its band reads carry BAND_NOTE and the
    BandTrap mark too (attributed to the basal record), and _band_trap checks a basal layer whose overlying view reads
    s. 68 B2 on e2386b42: _band_trap's re-reads leave the views' s_counts, cut_counts, marks and notes as they were."""

    def _basal(self, rid):
        over = _view(rid)
        rec = {"id": "basal_test", "kind": "assemblage", "phases": [{"id": "basal"}]}
        return over, ma.BasalView(rec, 4000.0, over, 1600.0)

    def test_basal_trapping_refuses_and_same_sign_answers(self):
        for rid, ia, k, trap in (POINTS[2], POINTS[0]):
            over, b = self._basal(rid)
            p = _at(over, ia)
            t = over.ts[k] + (over.ts[k + 1] - over.ts[k]) / 2
            got = b.state(p, t)
            with self.subTest(rid=rid, trap=trap):
                self.assertTrue(b.s_read)
                self.assertIn(ma.BAND_NOTE, [n.text for n in got[2] if isinstance(n, ma.mv.DeclaredNote)])
                marks = [n for n in got[2] if isinstance(n, ma.BandTrap)]
                self.assertEqual(bool(marks), trap)
                ev = sv._band_trap(_Body("basal"), {"basal": b}, _Acc({"basal": _path(p, (t,))}))
                if trap:
                    self.assertEqual(marks[0].material_id, "basal_test")
                    self.assertEqual((ev["layer_id"], ev["material_id"]), ("basal", "basal_test"))
                else:
                    self.assertIsNone(ev)
        _over, b = self._basal("silicate_slb_default_bse")
        b.overlying.s_read = False
        self.assertFalse(b.s_read)

    def _state(self, v):
        marks = getattr(v, "_marks", {})
        return ({k: (set(x) if isinstance(x, set) else x) for k, x in marks.items()},
                dict(getattr(v, "s_counts", {})), dict(getattr(v, "cut_counts", {})), list(v.notes))

    def test_the_scan_leaves_no_trace(self):
        rid, ia, k, _trap = POINTS[2]
        over, b = self._basal(rid)
        p = _at(over, ia)
        mid = over.ts[k] + (over.ts[k + 1] - over.ts[k]) / 2
        for ts in ((1900.0, 2000.0, 2100.0), (mid,)):           # a path with no trap, and one into a trapping band
            over.state(p, 2500.0)                                 # some prior read: its notes stand on the view
            for view, layer in ((over, "mantle"), (b, "basal")):
                before = [self._state(x) for x in (over, b)]
                sv._band_trap(_Body(layer), {layer: view}, _Acc({layer: _path(p, ts)}))
                with self.subTest(ts=ts, layer=layer):
                    self.assertEqual([self._state(x) for x in (over, b)], before)

    def test_without_the_restore_is_red(self):
        """Mutant: _band_trap without _quiet_views; the trap-free path's re-reads move the counts."""
        import contextlib
        rid, ia, _k, _trap = POINTS[2]
        over = _view(rid)
        p = _at(over, ia)
        before = self._state(over)
        with mock.patch.object(sv, "_quiet_views", lambda v: contextlib.nullcontext()):
            sv._band_trap(_Body("mantle"), {"mantle": over}, _Acc({"mantle": _path(p, (1900.0, 2000.0))}))
        self.assertNotEqual(self._state(over), before)


class PlantedSwitch(unittest.TestCase):
    """§6, 68's planted test: two constant fields of opposite sign across a switch node, f_today = +a below and
    f_s = −b above. Unblended (§3.2 as frozen) the walk chatters on the node; blended over one row with note 3's w it
    passes with normal steps. Mutant: w a step function (w = 1 above the node): red."""

    A, B, TN, D = 5e-9, 7e-9, 1000.0, 50.0          # K/Pa, K/Pa, the node, one T row
    P0, P1 = 10e9, 30e9

    N = 50000                                              # N: the unblended walk's calls must reach it (blended: 356)

    class _Cap(Exception):
        pass

    def _walk(self, w):
        """RHS calls of one walk, cut at N (a chattering walk never ends on its own: millions of calls, note 3 §1)."""
        calls = [0]

        def f(_p, y):
            calls[0] += 1
            if calls[0] >= self.N:
                raise self._Cap
            return [(1.0 - w(y[0])) * self.A + w(y[0]) * (-self.B)]

        try:
            got = solve_ivp(f, (self.P0, self.P1), [self.TN - 20.0], rtol=1e-10, atol=1e-8)
        except self._Cap:
            return calls[0], False
        return calls[0], got.success

    def test_blended_walk_has_normal_steps(self):
        n_band, ok = self._walk(lambda t: 0.0 if t <= self.TN else ma._smoothstep((t - self.TN) / self.D))
        n_step, _ok = self._walk(lambda t: 0.0 if t <= self.TN else 1.0)     # mutant: w a step function
        self.assertTrue(ok)
        self.assertGreaterEqual(n_step, self.N, "the unblended switch no longer chatters: the plant is not testing")
        self.assertLess(n_band, self.N / 100)


class TrapOnTheAcceptedPass(unittest.TestCase):
    """§2.4 on a real solve (Earth, the old materials, 7 s): the view only marks; _solve refuses an accepted pass
    whose T_ad reads carry a BandTrap. The marks are planted on LegacyView.state, which the check reads through the
    same `s_read` gate. Trial passes see the same marks and keep going, so the closure still reaches its root."""

    def _solve(self, mark_if, sign=True):
        real = lm.LegacyView.state

        def state(view, p, t, guess_rho=None):
            got = real(view, p, t, guess_rho)
            if isinstance(got, tuple) and mark_if(t):
                n = ma.BandTrap(view.material_id, p, t, 0.5, 1e-9, -1e-9) if sign else \
                    ma.mv.DeclaredNote(view.material_id, ma.PHASE_ID, ma.BAND_NOTE)
                return got[0], got[1], tuple(got[2]) + (n,)
            return got

        with mock.patch.object(lm.LegacyView, "s_read", True, create=True), \
                mock.patch.object(lm.LegacyView, "state", state):
            return sv.solve(_earth(), context.Options(sensitivity_dt=0.0))[0]

    def test_trapping_band_on_t_ad_refuses_by_name(self):
        out = self._solve(lambda t: t > 1650.0)
        self.assertEqual(getattr(out, "id", None), "solve.frozen_band_trapped", out)
        ev = out.evidence
        self.assertEqual(ev["pass_kind"], "accepted")
        self.assertGreater(ev["t"], 1650.0)
        self.assertLess(ev["dtdp_today"] * ev["dtdp_s"], 0.0)
        self.assertIn(ev["layer_id"], ("lithosphere", "mantle"))

    def test_same_sign_band_answers(self):
        out = self._solve(lambda t: t > 1650.0, sign=False)
        self.assertEqual(type(out).__name__, "Answer", out)

    def test_lid_local_t_marks_answer_and_mutant_refuses(self):
        """68 B1: the conductive lid's local-T reads (Earth's lid runs from 293 K) are never checked; T_ad starts at
        1600 K. Mutant: the check also reads y[3]; the planted lid refuses."""
        out = self._solve(lambda t: t < 1000.0)
        self.assertEqual(type(out).__name__, "Answer", out)
        src = textwrap.dedent(inspect.getsource(sv._band_trap))
        old = "            got = view.state(y[1], y[2], None)\n"
        self.assertEqual(src.count(old), 1)
        mut = src.replace(old, "            got = view.state(y[1], y[3], None)\n")      # the lid's local T where it differs
        ns = dict(vars(sv))
        exec(mut, ns)
        with mock.patch.object(sv, "_band_trap", ns["_band_trap"]):
            out = self._solve(lambda t: t < 1000.0)
        self.assertEqual(getattr(out, "id", None), "solve.frozen_band_trapped", out)
        self.assertEqual(out.evidence["layer_id"], "lithosphere")

    def test_no_marks_answers(self):
        self.assertEqual(type(self._solve(lambda t: False)).__name__, "Answer")


if __name__ == "__main__":
    unittest.main()
