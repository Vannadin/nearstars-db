# 전환 등록 시험 — 기록 뷰의 사건 · 옛 물질과의 패스 동일성(SW1) · 기록 거절의 대응 (switch-over registration §2, §6)
"""Switch-over registration (rewrite/switchover-registration.frozen.md) §2 and §6, the parts that land before the
resolver switches: a record view's events, the identity of a pass through fe_prem_legacy with the legacy fe_prem
(r2 SW1), and a record view's refusals reaching the solver's refusal registry.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_switchover
"""
import unittest

from solver import context, events, from_v1, legacy_materials as lm, material_registry as mr, material_view as mv
from solver import refusals, solve as sv
from solver import stepper as st
from solver.from_v1 import thaw


def _record(rid):
    reg = mr.load()
    if isinstance(reg, mr.LoadStop):
        raise AssertionError(f"registry STOP: {reg.id} {dict(reg.evidence)}")
    return thaw(reg.records[rid])


class RecordEvents(unittest.TestCase):
    def test_h2o_events_from_its_declarations(self):
        """Seams, solid–solid curves (seam events), melting curves (terminal) and the 130 K source-seam isotherm."""
        v = mv.RecordView(_record("h2o"), 300.0)
        evs = events.layer_events(v)
        kinds = {(e.terminal, e.seam) for e in evs}
        self.assertIn((False, True), kinds)                                   # seams and solid–solid curves
        melts = events.melting_events(v)
        self.assertTrue(melts)
        self.assertEqual({e.name for e in evs if e.terminal}, set(melts))      # every melting curve is terminal
        self.assertIn("source_seam:ih_cold|Ih", {e.name for e in evs})
        self.assertEqual(len([e for e in evs if e.name.startswith("seam:")]), len(v.seams()))   # noqa: test-side name

    def test_a_legacy_view_keeps_its_events(self):
        """A legacy view (or its bare material) builds exactly the events it built before the switch-over."""
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        leg = sv._views(body)["mantle"]
        a = [(e.name, e.terminal, e.seam) for e in events.layer_events(leg)]
        b = [(e.name, e.terminal, e.seam) for e in events.layer_events(leg.mat)]
        self.assertEqual(a, b)
        self.assertTrue(a)


class LegacyIdentity(unittest.TestCase):
    """r2 SW1: the step-1 identity rests on the record view reproducing the legacy pass, not only state(): the same
    events, the same landed nodes, the same residual, on Earth's accepted pass."""

    def test_earth_pass_through_fe_prem_legacy(self):
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        opt = context.Options(sensitivity_dt=0.0)
        ans, x = sv.solve(body, opt)
        views = sv._views_at(body, sv._views(body), x)
        leg = views["core"]
        rec = mv.RecordView(_record("fe_prem_legacy"), body.surface.t_pot, getattr(leg, "p_stop", 0.0))
        self.assertEqual([(e.name, e.seam) for e in events.layer_events(rec)],
                         [(e.name, e.seam) for e in events.layer_events(leg)])
        a = sv.inward(body, views, x, opt)
        b = sv.inward(body, {**views, "core": rec}, x, opt)
        self.assertEqual(a.F, b.F)
        self.assertEqual(a.events, b.events)
        self.assertEqual(a.profiles["core"], b.profiles["core"])
        self.assertEqual(a.boundaries, b.boundaries)

    def test_control_the_corrected_record_moves_the_pass(self):
        """Control: the corrected fe_prem (step 2's record) does not reproduce the legacy pass."""
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        opt = context.Options(sensitivity_dt=0.0)
        _ans, x = sv.solve(body, opt)
        views = sv._views_at(body, sv._views(body), x)
        rec = mv.RecordView(_record("fe_prem"), body.surface.t_pot, getattr(views["core"], "p_stop", 0.0))
        self.assertNotEqual(sv.inward(body, views, x, opt).F, sv.inward(body, {**views, "core": rec}, x, opt).F)


class RecordRefusals(unittest.TestCase):
    def test_a_record_refusal_maps_to_its_registry_id(self):
        r = mv.RecordRefusal("h2o", 5.0e9, 120.0, "input.material_out_of_data", "past t_min")
        got = sv._to_refusal(st.Stop("refused", r), "fixture.solve", 1.0, "R", "scan")
        self.assertEqual((got.id, got.evidence["refusal"], got.evidence["material_id"]),
                         ("solve.material_record", "input.material_out_of_data", "h2o"))
        self.assertIn("solve.material_record", refusals.REGISTRY)

    def test_melting_stop_maps(self):
        got = sv._to_refusal(st.Stop("melting_not_in_phase2", {"material_id": "h2o", "boundary": ("water1", "VI"),
                                                               "p": 1.0e9, "t": 300.0}),
                             "fixture.solve", 1.0, "R", "accepted")
        self.assertEqual(got.id, "solve.melting_not_in_phase2")


if __name__ == "__main__":
    unittest.main()
