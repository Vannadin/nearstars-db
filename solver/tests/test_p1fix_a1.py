# 리뷰 수정 A1 시험 — 거절 경로와 근거: ValueError 경로·물질 벽의 축·도달 상태·no_solved 의 scan·고립 시행·벽 너머 부호 바뀜
"""Post-phase-1 review fix batch A1 (rewrite/p1review/fix-plan.md; phase-1 design note 13 §3): G3-C-01, G2-R-03 =
G4-R-01, G2-R-02 = G4-R-02, G2-C-07, G2-R-04. Each test fails on dc8d69ad.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_p1fix_a1
"""
import unittest
from types import SimpleNamespace as NS
from unittest import mock

from solver import closure as cl, context, from_v1, legacy_materials as lm, material_registry as mr
from solver import material_view as mv, refusals, solve as sv
from solver import stepper as st
from solver.from_v1 import thaw


def _earth():
    body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
    return body


def _mantle_view(body):
    return sv._views(body)["mantle"]


class AdapterChannel(unittest.TestCase):
    def test_engine_value_error_is_a_named_stop(self):
        """G3-C-01: the engine's ValueError channel becomes a refusal, not an exception."""
        v = _mantle_view(_earth())
        with mock.patch.object(type(v.mat), "density", side_effect=ValueError("engine says no")):
            got = v.state(1.0e10, 2000.0)
        self.assertIsInstance(got, st.Stop)
        self.assertEqual((got.kind, got.record.kind), ("refused", "ValueError"))
        node = {"m": 1.0, "r": 2.0, "P": 9.0e9, "T": 1990.0}
        ev = sv._to_refusal(st.Stop(got.kind, got.record, node), "fixture.solve", 1.0, "R", "wall").evidence
        self.assertEqual((ev["axis"], ev["bound_kind"], ev["gap"]), ("none", "engine_value_error", "ValueError"))

    def test_a_temperature_wall_names_the_t_axis(self):
        """G2-R-03 = G4-R-01: a PhaseGap naming a temperature reports axis T, the reached T, and the wall's side."""
        v = _mantle_view(_earth())
        gap = lm.eos.PhaseGap("silicate", 1.0e10, "over the T ceiling", temperature_k=5000.0)
        with mock.patch.object(type(v.mat), "density", side_effect=gap):
            stop = v.state(1.0e10, 5000.0)
        self.assertEqual((stop.record.axis, stop.record.too_cold), ("T", False))
        node = {"m": 1.0, "r": 2.0, "P": 9.0e9, "T": 4990.0}
        got = sv._to_refusal(st.Stop(stop.kind, stop.record, node), "fixture.solve", 1.0, "R", "wall")
        ev = got.evidence
        self.assertEqual((got.id, ev["axis"], ev["bound"], ev["bound_kind"], ev["t"], ev["gap"]),
                         ("solve.material_domain", "T", 5000.0, "reached_t_above_ceiling", 5000.0, "PhaseGap"))


class _WallAbove(mv.RecordView):
    """fe_prem_legacy that refuses above P_WALL: a material wall inside Earth's core."""
    P_WALL = 2.0e11

    def state(self, p, t, guess_rho=None):
        if p > self.P_WALL:
            return st.Stop("refused", mv.RecordRefusal(self.material_id, p, t, "input.material_out_of_data", "planted"))
        return super().state(p, t, guess_rho)


class _AlwaysRefuses(mv.RecordView):
    def state(self, p, t, guess_rho=None):
        return st.Stop("refused", mv.RecordRefusal(self.material_id, p, t, "input.material_out_of_data", "planted"))


def _with_core(body, cls):
    leg = sv._views(body)
    reg = mr.load()
    return {**leg, "core": cls(thaw(reg.records["fe_prem_legacy"]), body.surface.t_pot, leg["core"].p_stop)}


class ReachedState(unittest.TestCase):
    def test_a_pass_refusal_carries_the_last_accepted_node(self):
        """G2-R-02 = G4-R-02 (note 13 §3): `state` is the last accepted node, below the refusing P in the evidence."""
        body = _earth()
        views = _with_core(body, _WallAbove)
        opt = context.Options(sensitivity_dt=0.0)
        _ans, x = sv.solve(body, opt)
        seen = []
        real = sv._segment

        def spy(*a, **k):
            res = real(*a, **k)
            seen.append(res)
            return res
        with mock.patch.object(sv, "_segment", spy):
            stop = sv.inward(body, sv._views_at(body, views, x), x, opt)
        self.assertIsInstance(stop, st.Stop)
        m_last, y_last, _k = seen[-1].path[-1]                 # 68 N70: equal to the path's last accepted node
        self.assertEqual(stop.state, {"m": m_last, "r": y_last[0], "P": y_last[1], "T": y_last[3]})
        got = sv._to_refusal(stop, "fixture.solve", x, "R", "accepted")
        self.assertEqual(got.id, "solve.material_record")
        self.assertLessEqual(got.evidence["state"]["P"], _WallAbove.P_WALL)
        self.assertGreater(got.evidence["p"], got.evidence["state"]["P"])

    def test_the_registry_requires_state_on_pass_refusals(self):
        """The rule can fail: a pass-reached refusal without `state` is rejected by the registry."""
        e = refusals.REGISTRY["solve.material_domain"]
        self.assertIn("state", e.fields)
        with self.assertRaises(ValueError):
            refusals.make("solve.material_domain", "w", x=1.0, closure_kind="R", pass_kind="wall", material_id="m",
                          axis="P", bound=1.0, bound_kind="reached_p_outside_table", source="s", message_old="o",
                          t=1.0, gap="PhaseGap")

    def test_no_solved_carries_the_scan_and_a_state(self):
        body = _earth()
        got, _x = sv.solve(body, context.Options(sensitivity_dt=0.0), views=_with_core(body, _AlwaysRefuses))
        self.assertIn(got.id, ("solve.material_record", "solve.material_domain"))   # whichever refuses first
        self.assertGreaterEqual(len(got.evidence["scan"]), context.Options().n_scan)
        self.assertTrue(all(len(row) == 3 and row[1] is None for row in got.evidence["scan"]))
        self.assertIsNotNone(got.evidence["state"])


def _trial(x, F, kind="scan"):
    return cl.Trial(x, F, None if F is not None else st.Stop("refused"), kind)


class StraddleWiring(unittest.TestCase):
    def test_solve_returns_the_straddled_walls_refusal_with_the_scan(self):
        """68 N71: solve() itself, not only the helper: a no_bracket outcome whose solved F changes sign across a wall
        returns that wall's refusal, with its state and the scan."""
        node = {"m": 1.0, "r": 1.0, "P": 1.0e11, "T": 3000.0}
        rec = mv.RecordRefusal("fe_prem_legacy", 1.1e11, 3010.0, "input.material_out_of_data", "planted")
        wall_stop = st.Stop("refused", rec, node)
        trials = [cl.Trial(1.0, -1.0, None, "scan"), cl.Trial(2.0, -0.5, None, "scan"),
                  cl.Trial(3.0, None, wall_stop, "scan"), cl.Trial(4.0, 0.5, None, "scan")]
        out = NS(kind="no_bracket", trials=trials, walls=[cl.Wall(3.0, wall_stop, 2.0)], roots=[], detail={})
        with mock.patch.object(cl, "solve_scalar", return_value=out):
            got, _w = sv.solve(_earth(), context.Options(sensitivity_dt=0.0))
        self.assertEqual((got.id, got.evidence["pass_kind"], got.evidence["state"]), ("solve.material_record", "wall", node))
        self.assertEqual(len(got.evidence["scan"]), 4)


class NearestWall(unittest.TestCase):
    """Directing 10-17: a refusal names its real cause, not the first scan point's (pre-run on 68e47ffc: earth 2950 K
    reported a tiny-core trial at 391 GPa; mars 2850 K a 4800 K trial at 131 GPa)."""

    def test_no_bracket_names_the_wall_f_falls_toward(self):
        """No stretch changes sign, but |F| falls toward the wall at 3: the root lies past it, so that wall's refusal is
        the outcome. Control: |F| grows toward the wall (None, no_bracket stands)."""
        wall = cl.Wall(3.0, st.Stop("refused"), 2.0)
        out = NS(trials=[_trial(1.0, 1.0), _trial(2.0, 0.4), _trial(3.0, None), _trial(4.0, None)], walls=[wall])
        self.assertIs(sv._nearest_wall(out), wall)
        grow = NS(trials=[_trial(1.0, 0.4), _trial(2.0, 1.0), _trial(3.0, None), _trial(4.0, None)], walls=[wall])
        self.assertIsNone(sv._nearest_wall(grow))
        near, far = cl.Wall(3.0, st.Stop("refused"), 2.0), cl.Wall(0.5, st.Stop("refused"), 1.0)   # of two, the one
        two = NS(trials=[_trial(0.5, None), _trial(1.0, 0.9), _trial(1.5, 0.95), _trial(2.0, 0.3), _trial(3.0, None)],
                 walls=[far, near])                                       # whose neighbour has the smaller |F|
        self.assertIs(sv._nearest_wall(two), near)

    def test_no_solved_names_the_gap_between_opposite_walls(self):
        """Nothing solves: the refusal reported is the narrowest opposite-wall gap's lower side (P a GAP_RATIO apart),
        not the lowest x. Control: no such pair, None."""
        def ref(x, p):
            return cl.Trial(x, None, st.Stop("refused", {"p": p}), "scan")
        out = NS(trials=[ref(1.0, 3.0e11), ref(2.0, 3.5e11), ref(3.0, 3.5e11), ref(3.5, 1.4e10), ref(4.0, 1.1e10)])
        self.assertEqual(sv._gap_trial(out).x, 3.0)
        same = NS(trials=[ref(1.0, 3.0e11), ref(2.0, 3.5e11)])
        self.assertIsNone(sv._gap_trial(same))
        rec = mv.RecordRefusal("fe_core_planted", 3.5e11, 6000.0, "input.material_out_of_data", "planted")
        trials = [ref(1.0, 3.0e11), cl.Trial(3.0, None, st.Stop("refused", rec, {"m": 1.0}), "scan"), ref(3.5, 1.4e10)]
        no = NS(kind="no_solved", trials=trials, walls=[], roots=[], detail={})
        with mock.patch.object(cl, "solve_scalar", return_value=no):             # and solve() reports it
            got, _w = sv.solve(_earth(), context.Options(sensitivity_dt=0.0))
        self.assertEqual((got.evidence["x"], got.evidence["material_id"]), (3.0, "fe_core_planted"))

    def test_solve_returns_the_nearest_walls_refusal(self):
        """solve() itself: a no_bracket outcome with |F| falling toward a wall returns that wall's refusal."""
        node = {"m": 1.0, "r": 1.0, "P": 1.0e11, "T": 4800.0}
        rec = mv.RecordRefusal("silicate_slb_default_bse", 1.09e11, 4800.0, "input.material_above_solid_window",
                               "above the table's last T node 4800 K (grid_end)")
        wall_stop = st.Stop("refused", rec, node)
        trials = [cl.Trial(1.0, 1.0, None, "scan"), cl.Trial(2.0, 0.4, None, "scan"),
                  cl.Trial(3.0, None, wall_stop, "scan"), cl.Trial(4.0, None, wall_stop, "scan")]
        out = NS(kind="no_bracket", trials=trials, walls=[cl.Wall(3.0, wall_stop, 2.0)], roots=[], detail={})
        with mock.patch.object(cl, "solve_scalar", return_value=out):
            got, _w = sv.solve(_earth(), context.Options(sensitivity_dt=0.0))
        self.assertEqual((got.id, got.evidence["refusal"], got.evidence["pass_kind"]),
                         ("solve.material_record", "input.material_above_solid_window", "wall"))


class ScanEvidence(unittest.TestCase):
    def test_an_isolated_refusal_does_not_split_a_solved_stretch(self):
        """G2-C-07: _regions skips isolated trials (A1 impl note 8 rule 2)."""
        out = NS(trials=[_trial(1.0, 1.0), _trial(2.0, 1.1), _trial(3.0, None, "isolated"), _trial(4.0, 1.2)])
        self.assertEqual(sv._regions(out), [[1.0, 4.0]])

    def test_a_sign_change_across_a_wall_names_the_wall(self):
        """G2-R-04: F < 0 below a refusing stretch and > 0 above it: the wall is the outcome, not «no sign change»."""
        wall = cl.Wall(3.0, st.Stop("refused"), 2.0)
        out = NS(trials=[_trial(1.0, -1.0), _trial(2.0, -0.5), _trial(3.0, None), _trial(4.0, 0.5)], walls=[wall])
        self.assertIs(sv._straddled_wall(out), wall)
        same = NS(trials=[_trial(1.0, 1.0), _trial(2.0, 0.5), _trial(3.0, None), _trial(4.0, 0.5)], walls=[wall])
        self.assertIsNone(sv._straddled_wall(same))                     # control: no sign change, no wall outcome


if __name__ == "__main__":
    unittest.main()
