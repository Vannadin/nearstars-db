# 표 무관 읽기 방식의 정상 경로 거절 시험 — 그 방식의 view 가 solve·run_oracle 에 닿으면 «material.table_regardless_in_solve» 로 거절, 방식이 꺼진 같은 경로는 그대로 (D2 읽기 등록 §5a)
"""D2-read rev 7 §5a, «The normal lanes refuse it»: solve.py's route refuses a view whose `table_regardless` is set,
by name («material.table_regardless_in_solve»), and a solve through run_oracle with the mode set refuses by that name
(§5a's planted control).

The view is the real one, built by material_assemblage.view(..., table_regardless=<tool>): the test makes solve's
one view site pass the keyword (the only way a normal lane could carry the mode), it does not stand in for the view.

The registry is test_silicate_routes' synthetic one, with allow_development: the shipped earth_dmm_wh2005 record is
left out because, on the read piece's path, the shipped assemblage records stop at load on the stale
material_assemblage pin until the re-pin (closure_terms.monotone), which is not what this test is about."""
import contextlib
import tempfile
import unittest
from unittest import mock

from solver import context, run_oracle, result
from solver import material_assemblage as ma
from solver import solve as sv
from solver.tests import test_silicate_routes as S

TOOL = "note 33 re-read (test)"
ID = "material.table_regardless_in_solve"
EARTH = str(S.ROOT / "engine/bodies/earth.yaml")


@contextlib.contextmanager
def synthetic_registry():
    orig = S.copy_shipped
    with tempfile.TemporaryDirectory() as d, \
            mock.patch.object(S, "copy_shipped", lambda dd, skip=(): orig(dd, skip=("silicate_slb_earth_dmm_wh2005.yaml",))):
        yield S.registry(d, allow_development=True)


@contextlib.contextmanager
def mode_on(tool=TOOL):
    """solve's view site builds its view with the mode set: the real view(), the keyword passed"""
    real = ma.view

    def view(*a, **k):
        return real(*a, **{**k, "table_regardless": tool})
    with mock.patch.object(ma, "view", view):
        yield


class NormalLanesRefuse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._reg = synthetic_registry()
        cls.reg = cls._reg.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls._reg.__exit__(None, None, None)

    def test_control_without_the_mode_the_route_builds_its_views(self):
        views = sv._views(S.body("earth"), registry=self.reg, silicate=True)
        self.assertIsInstance(views, dict)
        av = [v for v in views.values() if isinstance(v, ma.AssemblageView)]
        self.assertTrue(av)
        self.assertEqual({v.table_regardless for v in av}, {None})

    def test_a_view_in_the_mode_is_refused_by_name(self):
        with mode_on():
            got = sv._views(S.body("earth"), registry=self.reg, silicate=True)
        self.assertIsInstance(got, result.Refusal)
        self.assertEqual(got.id, ID)
        self.assertEqual(got.evidence["tool"], TOOL)
        self.assertTrue(got.evidence["material_id"].startswith("silicate_slb_"))
        self.assertIn("D2 읽기 등록 §5a", got.text)

    def test_the_guard_passes_a_view_without_the_mode(self):
        class V:
            table_regardless = None
        v = V()
        self.assertEqual(sv._refuse_table_regardless(v, "r"), (v, None))
        v.table_regardless = TOOL
        self.assertEqual(sv._refuse_table_regardless(v, "r"), (None, ("table_regardless_in_solve", ("r", TOOL))))

    def test_planted_control_a_solve_through_run_oracle_with_the_mode_refuses_by_name(self):
        """§5a: «a solve through run_oracle with the mode set must refuse by that name»"""
        with mode_on():
            rec = run_oracle.one(EARTH, 1600.0, context.Options(silicate_records=True), chain=False, registry=self.reg)
        self.assertEqual(rec["outcome_kind"], "refusal")
        self.assertEqual(rec["refusal"]["id"], ID)
        self.assertEqual(rec["refusal"]["evidence"]["tool"], TOOL)


if __name__ == "__main__":
    unittest.main()
