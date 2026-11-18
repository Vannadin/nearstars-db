# EXACT 시험 — 걸친 거절 시도를 옛쪽 뿌리 걸음으로 바꾸는지, 거짓 교차(오차만 넘긴 끝값)에서 착지 없이 제어기 h 로 가는지, 진짜 교차는 착지하는지, 받아들인 걸음의 단계가 한쪽에만 있는지(분석·표 구간), 집계가 맞는지, 변형마다 identity 통과·변형 실패 (A1 impl note 9 E1·E6·E7, N1·N2·N4; C2 + 68 HOLD)
"""A1 impl post-freeze note 9 (frozen, artifacts main 21646821a): E1, E6, E7 and the mutants N1, N2, N4 on analytic
rhs and on the legacy silicate table (a table leg that needs no record registry). Every mutant test runs the identity
copy (the function rebuilt from source on the module's globals, solver/tests/_mutants.py) and shows it passes, then the
mutant on the same globals and shows it fails (68 B1 on 1ccbfe91).

Run from the worktree root:  PY -B -m unittest solver.tests.test_stepper_exact
"""
import math
import unittest
from unittest import mock

from solver import events, legacy_materials as lm, rhs
from solver import stepper as st
from solver.tests._mutants import variant

A, W = 1.0, 3.0
PMAX = 2 * A / W
PC_KINK = 0.5


def sine(x, y):
    return (0.0, A * math.sin(W * x), 0.0, 0.0, 0.0, 0.0)


def kink(x, y):
    return (0.0, 1.0 if y[1] < PC_KINK else 3.0, 0.0, 0.0, 0.0, 0.0)


def opt(h0=3.0, step_check=None):
    return st.Options(rtol=1e-8, floors=(1.0, 1e-9, 1.0, 1.0, 1.0, 1.0), h0=h0, h_min=1e-12, h_max=50.0,
                      max_steps=100000, event_tol=1e-12, event_rewalks=32, event_min_progress=1e-9,
                      step_check=step_check)


def seam_at(pc):
    return st.Event("seam", lambda x, y: y[1] - pc, scale=1.0, terminal=False, seam=True, component=1)


def run(f, pc, h0=3.0, x1=4.0, step_check=None):
    nodes = []
    r = st.run(f, 0.0, (1.0, 0.0, 1.0, 1.0, 0.0, 0.0), x1, opt(h0, step_check), [seam_at(pc)],
               on_accept=lambda x, y: nodes.append((x, y[1])))
    return r, nodes


def c4(c):
    return (c.exact_tried, c.exact_unlanded, c.exact_replaced, c.exact_no_landing)


# ── E6: the false-positive trigger ─────────────────────────────────────────────────────────────────────────────────
class FalsePositive(unittest.TestCase):
    def test_trial_end_overshoots_no_landing(self):
        r, nodes = run(sine, 1.02 * PMAX)
        c = r.counters
        self.assertGreater(c.exact_tried, 0)
        self.assertEqual(len(r.events), 0)
        self.assertTrue(all(p < 1.02 * PMAX for _, p in nodes))
        self.assertEqual(r.stop.kind, "end")
        self.assertEqual(c.exact_tried, c.exact_unlanded + c.exact_failed + c.exact_replaced)
        self.assertEqual(c.exact_no_landing, c.exact_replaced)

    def planted_case(self):
        """_land planted to give a root at 0.2 % of the rejected trial: the replacement is short and passes, nothing
        lands, and the next trial's h is the controller's (≤ 5 × the replacement's), never the rejected h."""
        hs = []
        real_stepper = st._stepper

        def planted_land(f, ev, x, y, k1, h, out, g0, o, cnt):
            return ((x + 0.002 * h, None, None), None)

        def logging(o, stage_f=None):
            step = real_stepper(o, stage_f)

            def go(f, x, y, h, k1):
                hs.append(h)
                return step(f, x, y, h, k1)
            return go
        with mock.patch.object(st, "_land", planted_land), mock.patch.object(st, "_stepper", logging):
            r, nodes = run(sine, 1.02 * PMAX)
        self.assertEqual(c4(r.counters)[:1] + c4(r.counters)[2:], (1, 1, 1))
        self.assertEqual(len(r.events), 0)
        self.assertEqual(hs[0], 3.0)
        self.assertAlmostEqual(hs[1], 0.006)
        self.assertLessEqual(hs[2], 5 * 0.006 + 1e-12)
        self.assertNotEqual(hs[2], 3.0)

    def test_replacement_accepted_without_landing_takes_the_controllers_h(self):
        self.planted_case()

    def test_N4_identity_passes_mutant_fails(self):
        """N4: keeping h_restart after a replacement with no landing restarts at the rejected h."""
        with mock.patch.object(st, "run", variant(st.run)):
            self.planted_case()
        mut = variant(st.run, "            cnt.exact_no_landing += 1\n        h_restart = None\n",
                      "            cnt.exact_no_landing += 1\n            h, h_restart = h_restart, None\n")
        with mock.patch.object(st, "run", mut):
            with self.assertRaises(AssertionError):
                self.planted_case()


# ── E1 and N1, N2 on the kink (dP/dx 1 → 3 at the seam) ───────────────────────────────────────────────────────────
class Kink(unittest.TestCase):
    def kink_case(self):
        r, nodes = run(kink, PC_KINK, h0=2.0, x1=2.0)
        self.assertEqual([e[0] for e in r.events], ["seam"])
        self.assertGreaterEqual(r.counters.exact_replaced, 1)            # N1's killer (68 on C2)
        self.assertLessEqual(abs(r.events[0][2][1] - PC_KINK), 1e-12)
        self.assertAlmostEqual(r.y[1], PC_KINK + 3.0 * (2.0 - PC_KINK), delta=1e-7)
        return r

    def test_kink_replacement_counted(self):
        self.kink_case()

    def test_N1_identity_passes_mutant_fails(self):
        """N1: the replacement's stages read on the new side (no _old_side). The error test then rejects every
        replacement (68: 29/29/0), so answers and nodes are unchanged; the replacement count is what kills it."""
        with mock.patch.object(st, "run", variant(st.run)):
            self.kink_case()
        mut = variant(st.run, "o2 = _stepper(opt, None)(fo, x, y, x_e - x, k1)",
                      "o2 = _stepper(opt, None)(f, x, y, x_e - x, k1)")
        with mock.patch.object(st, "run", mut):
            with self.assertRaises(AssertionError):
                self.kink_case()

    def accepted(self, fn=None):
        with mock.patch.object(st, "run", fn or st.run):
            return run(kink, PC_KINK, h0=2.0, x1=2.0)[0].counters.accepted

    def test_N2_identity_passes_mutant_fails(self):
        """N2: without h_restart the run takes more accepted steps after the landing."""
        base = self.accepted()
        self.assertEqual(self.accepted(variant(st.run)), base)
        mut = variant(st.run, "            h = direction * min(abs(h_restart if h_restart is not None else h), opt.h_max)"
                              "    # A1 impl note 9\n",
                      "            h = direction * min(abs(h), opt.h_max)\n")
        self.assertGreater(self.accepted(mut), base)


# ── 68 B2 on C2: h_restart must not leak through the step_check halve branch ──────────────────────────────────────
class HalveOnce:
    """A step_check that halves once: the first trial whose end sits within 1e-6 of the seam (the replacement)."""

    def __init__(self):
        self.done = False

    def verdict(self, x, y, x_new, y_new, k1, k7):
        if not self.done and abs(y_new[1] - PC_KINK) < 1e-6:
            self.done = True
            return "halve"
        return None

    def commit(self, x, y, x_acc, y_acc):
        return None


class HalveBranch(unittest.TestCase):
    def halve_case(self):
        chk = HalveOnce()
        r, nodes = run(kink, PC_KINK, h0=2.0, x1=2.0, step_check=chk)
        self.assertTrue(chk.done)
        self.assertEqual(r.counters.band_halved, 1)
        self.assertEqual(r.counters.exact_no_landing, 0)    # a halved replacement is not a no-landing replacement
        self.assertEqual([e[0] for e in r.events], ["seam"])
        return r

    def test_halved_replacement_does_not_leak(self):
        self.halve_case()

    def test_mutant_without_the_clear_fails(self):
        with mock.patch.object(st, "run", variant(st.run)):
            self.halve_case()
        mut = variant(st.run, "            h_restart = None                          # 68 B2 on C2: a halved replacement is abandoned (counted\n",
                      "")
        with mock.patch.object(st, "run", mut):
            with self.assertRaises(AssertionError):
                self.halve_case()


# ── E1 on stages: every stage of every accepted step is on one side of each live seam (analytic and table legs) ──────
class StageRecorder:
    """Wraps stepper.step: records, per call, (x, h, the states f was given); `accepted(path)` keeps the calls whose
    (x, x + h) is an accepted interval of the path."""

    def __init__(self):
        self.calls = []
        self.real = st.step

    def step(self, f, x, y, h, k1, stage_f=None):
        seen = []

        def g(xx, yy):
            seen.append(tuple(yy))
            return f(xx, yy)
        out = self.real(g, x, y, h, k1, stage_f) if stage_f is not None else self.real(g, x, y, h, k1)
        self.calls.append((x, h, seen, out))
        return out

    def accepted_stages(self, path):
        ends = {(round(a[0], 15), round(b[0], 15)) for a, b in zip(path, path[1:]) if b[0] != a[0]}
        return [seen for x, h, seen, out in self.calls if (round(x, 15), round(x + h, 15)) in ends]


def one_sided(test, stage_lists, g, tol):
    for seen in stage_lists:
        gs = [g(y) for y in seen]
        gs = [v for v in gs if v is not None and abs(v) > tol]
        test.assertTrue(all(v > 0 for v in gs) or all(v < 0 for v in gs), f"stages on both sides: {gs}")


class StagesOneSided(unittest.TestCase):
    def test_analytic_kink(self):
        rec = StageRecorder()
        with mock.patch.object(st, "step", rec.step):
            r, _ = run(kink, PC_KINK, h0=2.0, x1=2.0)
        stages = rec.accepted_stages(r.path)
        self.assertGreater(len(stages), 0)
        one_sided(self, stages, lambda y: y[1] - PC_KINK, 1e-9)

    def test_table_leg(self):
        """The legacy silicate table (no registry): its own layer events, every accepted step's stages one-sided."""
        mat = lm.interior.MATERIALS["silicate"]
        tp, M = 1800.0, 3.0 * 5.972e24
        R = (3 * M / (4 * math.pi * 4500.0)) ** (1 / 3)
        evs = events.layer_events(mat)
        rec = StageRecorder()
        with mock.patch.object(st, "step", rec.step):
            res = rhs.inward_pass(lm.LegacyView("silicate", mat, tp), M, R, 0.0, tp, 4500.0, events=evs)
        self.assertGreater(len(res.events), 0)
        stages = rec.accepted_stages(res.path)
        self.assertGreater(len(stages), 0)
        for ev in evs:
            if ev.seam:
                one_sided(self, stages, lambda y, ev=ev: ev.g(0.0, y), 1e-9 * ev.scale)


# ── note 9 §1: the replacement's FSAL k7 is re-read unclamped at the root (68 on e0fb28eb) ────────────────────────────
class FsalReread(unittest.TestCase):
    """On the legacy silicate table leg: every path node off the seams carries k1 = f(x, y) as read unclamped (the
    structural check), and F is pinned to the identity copy's value (the answer check). A mutant that keeps the
    replacement's old-side k7 fails."""
    F_BASE = 0.0966013118349986                          # identity copy on bc71db0a + C1/C2 (68's figure)

    def leg(self):
        mat = lm.interior.MATERIALS["silicate"]
        tp, M = 1800.0, 3.0 * 5.972e24
        R = (3 * M / (4 * math.pi * 4500.0)) ** (1 / 3)
        evs = events.layer_events(mat)
        view = lm.LegacyView("silicate", mat, tp)
        res = rhs.inward_pass(view, M, R, 0.0, tp, 4500.0, events=evs)
        return res, rhs.make_rhs(view), evs

    REL_K1, REL_F = 1e-9, 1e-12                       # identity max |k1 − f|/|f| 1.5e-11 (68); F: Mac pin, Linux

    def k1_mismatch(self, res, f):
        """The largest per-component |k1 − f(x, y)| / |f| over every path node (none skipped: 68 on a5de93a4, the mutant moves a
        node at |g|/scale 4.8e-16)."""
        worst = 0.0
        for x, y, k1 in res.path:
            k = f(x, y)
            if isinstance(k, st.Stop):
                continue
            for a, b in zip(k1, k):                    # per component: a large component must not mask a small one
                worst = max(worst, abs(a - b) / abs(b) if b != 0.0 else (0.0 if a == 0.0 else math.inf))
        return worst

    def case(self, check_f=True):
        res, f, evs = self.leg()
        self.assertGreater(res.counters.exact_replaced, 0)
        self.assertLessEqual(self.k1_mismatch(res, f), self.REL_K1)
        if check_f:
            self.assertLessEqual(abs(res.F - self.F_BASE), self.REL_F * abs(self.F_BASE))

    def test_fsal_reread(self):
        self.case()

    def test_mutant_keeping_the_old_side_k7_fails(self):
        with mock.patch.object(st, "run", variant(st.run)):
            self.case()
        mut = variant(st.run, "                    h, out = x_e - x, (o2[0], o2[1], k7n)\n",
                      "                    h, out = x_e - x, o2\n")
        with mock.patch.object(st, "run", mut):
            with self.assertRaises(AssertionError):
                self.case()

    def test_structural_check_alone_kills_the_mutant(self):
        """68 on a5de93a4: the pair with the F check off — identity passes, the mutant fails on k1 alone."""
        with mock.patch.object(st, "run", variant(st.run)):
            self.case(check_f=False)
        mut = variant(st.run, "                    h, out = x_e - x, (o2[0], o2[1], k7n)\n",
                      "                    h, out = x_e - x, o2\n")
        with mock.patch.object(st, "run", mut):
            with self.assertRaises(AssertionError) as cm:
                self.case(check_f=False)
        print(f"\nFsalReread structural pair: identity max {self._identity_max():.3g}; mutant {cm.exception}")

    def _identity_max(self):
        with mock.patch.object(st, "run", variant(st.run)):
            res, f, _ = self.leg()
        return self.k1_mismatch(res, f)


if __name__ == "__main__":
    unittest.main()
