# 리뷰 LOW 묶음 L2 시험 — 사건·덮개·어댑터 가장자리: 같은 물질 층 경계의 스침 창, 표면 껍질, 엔진 ValueError, T_pot 없는 덮개, 기저층의 표 위상
"""Post-phase-1 review LOW batch L2 (rewrite/p1review/low-triage.md; phase-1 design note 17 §2, §2b): G1-C-09, G1-C-10,
G1-R-11, G1-R-09 with c8's G4-C-12, G3-R-02. Each test fails on ffe41345 except G3-R-02's, which pins note 17 §2's
reading (no code changes there).

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_p1fix_l2
"""
import dataclasses
import unittest
from types import SimpleNamespace as NS
from unittest import mock

from solver import context, events, from_v1, member as mb, result, solve as sv
from solver import stepper as st

OPT = context.Options(sensitivity_dt=0.0)


def _earth():
    body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
    return body


class LidWithoutTPot(unittest.TestCase):
    """Note 17 §2b (G1-R-09, closes G4-C-12): a body with a conductive layer and no T_pot is refused by name, and never
    answers with «no_temperature_path»."""

    def test_refused(self):
        e = _earth()
        no_t = dataclasses.replace(e, surface=dataclasses.replace(e.surface, t_pot=None))
        got, _w = sv.solve(no_t, OPT)
        self.assertIsInstance(got, result.Refusal)
        self.assertEqual((got.id, got.evidence["rule"]), ("input.cross_field", "lid_without_t_pot"))
        self.assertNotIn("no_temperature_path", [n.kind for n in getattr(got, "notes", ())])

    def test_control_no_lid_no_t_pot_still_answers(self):
        """Without a lid, a body with no T_pot keeps its answer and its «no_temperature_path» note."""
        e = _earth()
        no_lid = dataclasses.replace(e, layers=tuple(l for l in e.layers if l.thermal != "conductive"),
                                     surface=dataclasses.replace(e.surface, t_pot=None))
        got, _w = sv.solve(no_lid, OPT)
        self.assertIsInstance(got, result.Answer)
        self.assertIn("no_temperature_path", [n.kind for n in got.notes])


class SurfaceShellIsNotInSolve(unittest.TestCase):
    """G1-C-10: a view with a surface shell reaches solve.inward only by a bug; it raises by name, not ZeroDivision."""

    def test_raises(self):
        e = _earth()
        views = sv._views(e)
        top = e.layers[-1].id
        shell_view = NS(**{k: getattr(views[top], k) for k in ("state",)}, surface_shell=lambda *a: (0.0, 0.0),
                        p_floor=None)
        with self.assertRaises(NotImplementedError):
            sv.inward(e, {**views, top: shell_view}, 0.5 * (e.closure.lo + e.closure.hi), OPT)


class EngineValueErrorIsAGap(unittest.TestCase):
    """G1-R-11: a ValueError from the engine inside an event g, the cap or the graze monitor reads as «not here», as the
    adapter maps it (G3-C-01); it does not escape the stepper."""

    def test_curve_g(self):
        mat = NS(onset_curves=mock.Mock(side_effect=ValueError("variant")))
        self.assertIsNone(events._curve_at(mat, "고상선", 1.0e9, 2000.0))

    def test_graze_monitor(self):
        mat = NS(onset_curves=mock.Mock(side_effect=ValueError("variant")), name="m")
        mon = events.GrazeMonitor(mat)
        mon(0.0, (0.0, 1.0e9, 2000.0, 2000.0))
        self.assertIsNone(mon.best)

    def test_control_other_exceptions_raise(self):
        mat = NS(onset_curves=mock.Mock(side_effect=KeyError("bug")))
        with self.assertRaises(KeyError):
            events._curve_at(mat, "고상선", 1.0e9, 2000.0)


class GrazeWindowAcrossASameMaterialBoundary(unittest.TestCase):
    """G1-C-09: two layers of one material share one graze monitor, so the boundary node can be a window's middle (the
    old detector cleared only on a material change)."""

    def test_one_monitor_for_two_same_material_layers(self):
        e = _earth()
        from solver import body as bd
        core = next(l for l in e.layers if l.id == "core")
        mantle = next(l for l in e.layers if l.id == "mantle")
        lower = dataclasses.replace(mantle, id="mantle_lower", extent=bd.Extent("mass_fraction", 0.3))
        body = dataclasses.replace(e, layers=(core, lower, mantle))
        made, real = [], events.GrazeMonitor

        def spy(*a, **k):
            m = real(*a, **k)
            made.append(m)
            return m
        views = sv._views(body)
        x = 0.5 * (body.closure.lo + body.closure.hi)
        with mock.patch.object(events, "GrazeMonitor", spy):
            sv.inward(body, sv._views_at(body, views, x), x, context.Options())
        self.assertEqual(len(made), 2)              # mantle + mantle_lower share one; the core has its own


class BasalLayerTakesTheTableRules(unittest.TestCase):
    """Note 17 §2 (G3-R-02): Mars's basal layer delegates to the mantle's table phase, so the cap and the band test reach
    it (note 12's scope as amended)."""

    def test_basal_view_has_cap_and_band(self):
        body, _aside = from_v1.load_v1("engine/bodies/mars.yaml")
        body, _m = mb.member_of(body)
        v = sv._views(body)["basal"]
        self.assertIsNotNone(events.step_cap(v.mat))
        self.assertIsNotNone(sv._band(v))


if __name__ == "__main__":
    unittest.main()
