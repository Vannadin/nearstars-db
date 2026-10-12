# 리뷰 LOW 묶음 L1 시험 — 걸음 함수의 착지: 봉합선 앞 사건을 놓치지 않음, 착지 재걸음의 옛 쪽 단계, 사건 이름 충돌, 덮개의 재시작 상한
"""Post-phase-1 review LOW batch L1 (rewrite/p1review/low-triage.md, r2 clear 4fd9275d): G1-C-03 with G1-R-04, G1-R-05,
G1-C-11, G1-C-06. (G1-R-06 waits for its note; G1-C-07 and G1-R-07 need refusal mappings and go with L3.) Each test fails
on f7a5b95c except the one regression case named in its docstring.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_p1fix_l1
"""
import unittest
from unittest import mock

from solver import context, from_v1, lid, solve as sv
from solver import stepper as st


def _opt(h0=8.0, rtol=1e-10):
    return st.Options(rtol=rtol, floors=(1e-12,), h0=h0, h_min=1e-12, h_max=100.0, max_steps=10000,
                      event_rewalks=32)           # production's EVENT_REWALKS (A1 impl note 8)


class EventsBeforeASeam(unittest.TestCase):
    """G1-C-03 / G1-R-04 (the review's probe p8): a seam on a linear component and a terminal event 1e-3 before it,
    both inside one step. As is, the seam lands with no old-side iterate and the terminal event is dropped."""

    def test_linear_component(self):
        f = lambda x, y: (1.0,)
        seam = st.Event("seam", lambda x, y: y[0] - 5.0, scale=5.0, seam=True, component=0)
        stop_ev = st.Event("end_here", lambda x, y: y[0] - 4.999, scale=5.0, terminal=True)
        res = st.run(f, 0.0, (0.0,), 10.0, _opt(), [seam, stop_ev])
        self.assertEqual((res.stop.kind, res.event), ("event", "end_here"))
        self.assertAlmostEqual(res.x, 4.999, delta=1e-9)

    def test_an_event_in_the_sliver_next_to_the_seam(self):
        """G1-R-04: a curved component, so the secant leaves an old-side iterate; the terminal event sits 1e-8 before the
        seam. A regression case, not a failing-first one: on f7a5b95c this toy's last old-side iterate already lies
        past the event, so it passes there too; the re-step short of the seam is what makes it hold in general."""
        f = lambda x, y: (1.0 + 0.3 * x,)
        seam = st.Event("seam", lambda x, y: y[0] - 5.0, scale=5.0, seam=True, component=0)
        stop_ev = st.Event("end_here", lambda x, y: y[0] - (5.0 - 1e-8), scale=5.0, terminal=True)
        res = st.run(f, 0.0, (0.0,), 10.0, _opt(), [seam, stop_ev])
        self.assertEqual((res.stop.kind, res.event), ("event", "end_here"))

    def test_control_without_the_seam_the_event_lands(self):
        f = lambda x, y: (1.0,)
        stop_ev = st.Event("end_here", lambda x, y: y[0] - 4.999, scale=5.0, terminal=True)
        res = st.run(f, 0.0, (0.0,), 10.0, _opt(), [stop_ev])
        self.assertEqual(res.event, "end_here")


class LandingReStepsReadTheOldSide(unittest.TestCase):
    """G1-R-05: an adaptive landing re-step's inner stages read the old side of the seam (as the fixed mode's did)."""

    def test_no_inner_stage_reads_past_the_seam(self):
        reads = []

        def f(x, y):
            reads.append(y[0])
            return (1.0 if y[0] <= 5.0 else 2.0,)
        seam = st.Event("seam", lambda x, y: y[0] - 5.0, scale=5.0, seam=True, component=0)
        y0 = (4.0,)
        k1 = f(0.0, y0)
        out = st.step(f, 0.0, y0, 3.0, k1)
        reads.clear()
        cnt = st.Counters()
        got = st._land(f, seam, 0.0, y0, k1, 3.0, out, -1.0, _opt(), cnt)
        node, _lo = got
        # every read during the re-steps is on the old side (≤ the seam, with the clamp's margin), except FSAL ends
        past = [r for r in reads if r > 5.0 * (1 + 1e-11)]
        self.assertLessEqual(len(past), cnt.rewalks)              # at most one FSAL end per re-step
        self.assertAlmostEqual(node[1][0], 5.0, delta=1e-9)


class EventNamesMustBeDistinct(unittest.TestCase):
    """G1-C-11: two events with one name would share g_prev and last_fire; the run refuses to start (a bug)."""

    def test_collision_raises(self):
        evs = [st.Event("seam:2e+10", lambda x, y: y[0] - 1.0, scale=1.0, seam=True, component=0),
               st.Event("seam:2e+10", lambda x, y: y[0] - 1.0000000001, scale=1.0, seam=True, component=0)]
        with self.assertRaises(ValueError):
            st.run(lambda x, y: (1.0,), 0.0, (0.0,), 2.0, _opt(0.1), evs)


class LidGetsTheRestartCaps(unittest.TestCase):
    """G1-C-06: the context's EVENT_RESTARTS caps reach the lid's PassOptions."""

    def test_caps_passed(self):
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        opt = context.Options(sensitivity_dt=0.0, event_restarts_step=3, event_restarts_solve=1234)
        seen, real = [], lid.lid_pass

        def spy(*a, **k):
            seen.append(a[8])
            return real(*a, **k)
        x = 0.5 * (body.closure.lo + body.closure.hi)
        with mock.patch.object(lid, "lid_pass", spy):
            sv.inward(body, sv._views_at(body, sv._views(body), x), x, opt)
        self.assertEqual((seen[0].event_restarts_step, seen[0].event_restarts_run), (3, 1234))


if __name__ == "__main__":
    unittest.main()
