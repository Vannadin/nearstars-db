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
          "legacy_nodes", "table_read"}
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

    def test_table_read_from_the_committed_table(self):
        """B1: true because core_thermal_history read engine/structure_grid/earth.json at its 097a8aa3 blob."""
        self.assertTrue(self.rec["table_read"])
        self.assertIn("core_thermal_history", self.rec["legacy_nodes"])


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
