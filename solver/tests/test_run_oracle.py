# 오라클 대조 드라이버 시험 — 계약 칸, 표 읽기, 핵 없는 Dante, 거절 천체의 옛 노드, 상태 규칙, 빈 출력 폴더 (r2 run_oracle HOLD)
"""Tests of solver/run_oracle.py against c8's comparator contract (registration §4) and r2's run_oracle HOLD.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_run_oracle
"""
import json
import tempfile
import unittest
from pathlib import Path

from solver import context, run_oracle as ro

FIELDS = {"header", "body", "state", "outcome_kind", "quantities", "boundaries", "refusal", "no_answer",
          "legacy_nodes", "table_read", "notes"}   # notes: switch-over §5 (Q2), comparator note 15
FAST = context.Options(sensitivity_dt=0.0)


class Earth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rec = ro.one("engine/bodies/earth.yaml", "declared", FAST)

    def test_contract_fields(self):
        self.assertEqual(set(self.rec), FIELDS)
        self.assertEqual(self.rec["outcome_kind"], "answer")
        self.assertTrue(self.rec["header"]["engine_identical_to_oracle_tree"])
        self.assertEqual(len(self.rec["header"]["solve_id"]), 64)

    def test_notes_are_written_as_kinded_objects(self):
        """Switch-over §6.7: `notes` is a list of objects with a text `kind` (comparator note 15's shape)."""
        self.assertIsInstance(self.rec["notes"], list)
        self.assertTrue(all(isinstance(n, dict) and isinstance(n.get("kind"), str) for n in self.rec["notes"]))

    def test_table_read_from_the_committed_table(self):
        """B1: true because core_thermal_history read engine/structure_grid/earth.json at its 097a8aa3 blob."""
        self.assertTrue(self.rec["table_read"])
        self.assertIn("core_thermal_history", self.rec["legacy_nodes"])


class CoreBalanceGuard(unittest.TestCase):
    """Switch-over note 7 (directing, r2): core_energy_balance's bisection has no residual check; on the corrected
    fe_prem, Earth's declared state puts its sign change on the inner-core nucleation jump (Mac −15.93 with an inner
    core, PC +0.23 without). |balance_residual| > 1e-9 gives no values and the Note core_balance_not_solved; the
    structure answer stands. Control: both corrections put back, the true root (≈ 1e-12) keeps its values."""

    @staticmethod
    def _balance(rec):
        return rec["legacy_nodes"]["core_energy_balance"]

    def test_earth_corrected_has_no_root(self):
        rec = ro.one("engine/bodies/earth.yaml", "declared", FAST)
        node = self._balance(rec)
        self.assertEqual(rec["outcome_kind"], "answer")
        self.assertFalse(node["applicable"])
        self.assertEqual(node["values"], {})
        got = [n for n in rec["notes"] if n["kind"] == "core_balance_not_solved"]
        self.assertEqual(len(got), 1)
        self.assertGreater(abs(got[0]["fields"]["residual"]), ro.lv.BALANCE_TOL)
        self.assertEqual(got[0]["fields"]["reason"], "root on a discontinuity")

    def test_control_both_put_back_keeps_the_root(self):
        from solver.tests.test_switchover import Step2PutBack
        rec = ro.one("engine/bodies/earth.yaml", "declared", FAST, registry=Step2PutBack._registry("W-L1-01", "P5-F1"))
        node = self._balance(rec)
        self.assertTrue(node["applicable"])
        self.assertLess(abs(node["values"]["balance_residual"]), ro.lv.BALANCE_TOL)
        self.assertTrue(node["values"]["has_inner_core"])
        self.assertFalse([n for n in rec["notes"] if n["kind"] == "core_balance_not_solved"])

    def test_guard_on_planted_results(self):
        import payload
        ok = payload.Result(recipe="r", version="v", regime="x", reason="", grade="analog", inputs={},
                            values={"balance_residual": 6.5e-13}, units={"balance_residual": ""})
        bad = payload.Result(recipe="r", version="v", regime="x", reason="", grade="analog", inputs={},
                             values={"balance_residual": -15.93}, units={"balance_residual": ""})
        self.assertEqual(ro.lv.balance_guard(ok), (ok, None))
        out, note = ro.lv.balance_guard(bad)
        self.assertFalse(out.applicable)
        self.assertEqual((note["kind"], note["fields"]["residual"]), ("core_balance_not_solved", -15.93))
        refused = payload.out_of_domain("r", "v", "no core", inputs={})
        self.assertEqual(ro.lv.balance_guard(refused), (refused, None))


class Dante(unittest.TestCase):
    def test_coreless_body_writes_a_record(self):
        """B2: no crash; the absent core / temperature keys reach the old chain as the old engine's zeros."""
        rec = ro.one("engine/bodies/dante_fixture.yaml", "declared", FAST)
        self.assertEqual(rec["outcome_kind"], "answer")
        keys = {q["key"] for q in rec["quantities"]}
        self.assertFalse({"core_temperature", "cmb_temperature", "core_radius"} & keys)
        self.assertTrue(rec["legacy_nodes"])

    def test_t_pot_state_on_a_body_without_t_pot_is_refused(self):
        rec = ro.one("engine/bodies/dante_fixture.yaml", 1600.0, FAST)
        self.assertEqual(rec["refusal"]["evidence"]["rule"], "t_pot_state_without_t_pot")


class RefusingBody(unittest.TestCase):
    def test_old_nodes_run_and_decline(self):
        """B3: the giant's refusal is injected as interior_layers' result; the old nodes run and decline."""
        rec = ro.one("engine/bodies/alpha_centauri_a_b.yaml", "declared", FAST)
        self.assertEqual(rec["outcome_kind"], "refusal")
        self.assertTrue(rec["legacy_nodes"])
        self.assertIn("internal_heat_nontidal", rec["legacy_nodes"])

    def test_structure_readers_decline(self):
        """The nodes that read the structure decline on the injected refusal, as in the old chain."""
        rec = ro.one("engine/bodies/alpha_centauri_a_b.yaml", "declared", FAST)
        self.assertEqual(set(rec), FIELDS)
        for node in ("core_state", "cmb_heat_flux", "core_energy_balance"):
            if node in rec["legacy_nodes"]:
                self.assertFalse(rec["legacy_nodes"][node]["applicable"], node)


class NoChainForPoints(unittest.TestCase):
    """--no-chain-for-points: a T_pot state skips the old chain (O9 reads interior_layers only); the declared state
    keeps it (control)."""

    def test_point_has_no_legacy_nodes(self):
        rec = ro.one("engine/bodies/earth.yaml", 2093.0, context.Options(sensitivity_dt=0.0), chain=False)
        self.assertEqual((rec["outcome_kind"], rec["legacy_nodes"], rec["table_read"], rec["header"]["chain"]),
                         ("answer", {}, False, False))
        self.assertEqual(set(rec), FIELDS)

    def test_control_declared_keeps_the_chain(self):
        rec = ro.one("engine/bodies/dante_fixture.yaml", "declared", context.Options(sensitivity_dt=0.0), chain=False)
        self.assertTrue(rec["legacy_nodes"])
        self.assertTrue(rec["header"]["chain"])


class Cli(unittest.TestCase):
    def test_non_empty_out_dir_stops(self):
        d = tempfile.mkdtemp()
        Path(d, "stale.json").write_text("{}")
        self.assertEqual(ro.main(["engine/bodies/earth.yaml", "-", d]), 2)

    def test_states_deduplicated(self):
        p = Path(tempfile.mkdtemp(), "pts.json")
        p.write_text(json.dumps([["earth", 2093.0, "node"], ["earth", 2093.0, "family"], ["mars", 1800.0, "node"]]))
        self.assertEqual(ro.states_for("earth", str(p)), ["declared", 2093.0])


if __name__ == "__main__":
    unittest.main()
