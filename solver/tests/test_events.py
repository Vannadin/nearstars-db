# 사건 시험 — 철 열 세트 이음매 착지, 시작 곡선 착지, 스침 기록, 사건 폭주 멈춤, 암모니아 등온선 사건 (등록 S5)
"""S5 acceptance of rewrite/phase1-a1-impl.frozen.md, each with its negative control.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_events
"""
import math
import unittest

from solver import events, rhs, legacy_materials as lm
from solver import stepper as st

M = 5.972e24


class SeamLanding(unittest.TestCase):
    """A pure fe_prem sphere (Earth mass) crosses fe_prem's thermal-set seams at 19 and 35 GPa (R-C157-5)."""

    def _pass(self, with_events):
        mat = lm.interior.MATERIALS["fe_prem"]
        view = lm.LegacyView("fe_prem", mat, 1600.0)
        evs = events.seam_events(mat) if with_events else []
        r = 4.3e6
        return rhs.inward_pass(view, M, r, 0.0, 1600.0, 3 * M / (4 * math.pi * r ** 3), events=evs), mat

    def test_seams_land(self):
        res, mat = self._pass(True)
        seams = sorted(events._material_seams(mat))
        self.assertIn(19.0e9, seams)
        self.assertIn(35.0e9, seams)
        landed = {name: y for name, _m, y in res.events}
        for p_b in (19.0e9, 35.0e9):
            y = landed[f"seam:{p_b:.9g}"]
            self.assertLessEqual(abs(y[1] - p_b), 1e-12 * p_b)
            self.assertGreaterEqual(y[1], p_b)                      # inward: landed on the high-pressure side

    def test_control_events_off_do_not_land(self):
        res, _mat = self._pass(False)
        for p_b in (19.0e9, 35.0e9):
            self.assertGreater(min(abs(y[1] - p_b) for _x, y, _k in res.path), 1e-10 * p_b)   # 100× the landing tol


class Synthetic:
    """ρ constant, dT/dP constant; one onset curve T_on(P) given as a function."""
    name = "synthetic"

    def __init__(self, t_on, dtdp=2e-8):
        self.t_on, self.k = t_on, dtdp

    def state(self, p, t, guess):
        return (5000.0, self.k)

    def onset_curves(self, p, t):
        return [("curve", self.t_on(p))]


def _run(view, evs, monitor=None, opt=rhs.PassOptions()):
    r = (3 * M / (4 * math.pi * 5000.0)) ** (1 / 3)
    return rhs.inward_pass(view, M, r, 0.0, 1600.0, 5000.0, opt, events=evs, on_accept=monitor)


class OnsetLanding(unittest.TestCase):
    def test_crossing_lands(self):
        view = Synthetic(lambda p: 1600.0 + 1e3 + 1e-8 * p)       # T rises faster (2e-8) than the curve (1e-8)
        res = _run(view, events.onset_event(view))
        hits = [y for name, _m, y in res.events if name == "onset"]
        self.assertEqual(len(hits), 1)
        g = hits[0][3] - view.t_on(hits[0][1])
        self.assertLessEqual(abs(g), 1e-12 * 1.0e3)

    def test_control_without_event_no_landing(self):
        view = Synthetic(lambda p: 1600.0 + 1e3 + 1e-8 * p)
        res = _run(view, [])
        best = min(abs(y[3] - view.t_on(y[1])) for _x, y, _k in res.path)
        self.assertGreater(best, 1e-6)


class GrazeRecord(unittest.TestCase):
    P0 = 1.0e11

    def _view(self):
        # the curve rises to touch T_ad − 0.5 K at P0 from below and turns back: g = T − T_on ≥ 0.5 K, minimum at P0
        return Synthetic(lambda p: 1600.0 + 2e-8 * p - 0.5 - 1e-21 * (p - self.P0) ** 2 * 1e-0)

    def test_graze_found(self):
        view = self._view()
        mon = events.GrazeMonitor(view)
        _run(view, events.onset_event(view), mon)
        self.assertIsNotNone(mon.best)
        self.assertEqual(mon.best.curve, "curve")
        self.assertLess(abs(mon.best.g - 0.5), 0.05)
        self.assertTrue(events.onset_graze_tag(mon.best, 20.0))
        self.assertFalse(events.onset_graze_tag(mon.best, 5.0))

    def test_control_no_monitor_no_record(self):
        view = self._view()
        res = _run(view, events.onset_event(view))
        self.assertEqual([e for e in res.events if e[0] == "onset"], [])   # no crossing, so no event either


class Chatter(unittest.TestCase):
    def test_oscillating_curve_trips_guard(self):
        view = Synthetic(lambda p: 1600.0 + 2e-8 * p - 1e-3 * math.sin(p / 1e3))   # g = 1e-3 sin(P/1 kPa)
        res = _run(view, events.onset_event(view), opt=rhs.PassOptions(event_restarts_run=50))
        self.assertEqual(res.stop.kind, "chatter")
        self.assertIn(res.stop.record["cap_name"], ("EVENT_RESTARTS_SOLVE", "EVENT_RESTARTS_STEP", "EVENT_REWALKS",
                                                    "EVENT_MIN_PROGRESS"))

    def test_control_smooth_curve_does_not_trip(self):
        view = Synthetic(lambda p: 1600.0 + 1e3 + 1e-8 * p)
        res = _run(view, events.onset_event(view), opt=rhs.PassOptions(event_restarts_run=50))
        self.assertNotEqual(res.stop.kind, "chatter")


class Ammonia(unittest.TestCase):
    def test_isotherm_events(self):
        nh3 = lm.interior.MATERIALS["nh3"] if "nh3" in lm.interior.MATERIALS else None
        self.assertIsNotNone(nh3)
        evs = events.ammonia_events(nh3)
        self.assertEqual([e.name for e in evs], [f"nh3_isotherm:{t:g}" for t in lm.ammonia_isotherms()])

    def test_control_no_ammonia_no_events(self):
        self.assertEqual(events.ammonia_events(lm.interior.MATERIALS["fe_prem"]), [])


if __name__ == "__main__":
    unittest.main()
