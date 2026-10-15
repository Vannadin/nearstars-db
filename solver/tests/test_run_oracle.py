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

    def test_planted_corner_on_a_jump_nulls_the_band(self):
        """68 H1: the band corners are roots too. Both corrections put back (a true central root); one corner's balance
        gets a planted jump at 3900 K, so its bisection lands there. The band's _min/_max give no value, the centre
        stands, and the note names that corner."""
        from unittest import mock
        import core_energy as ce
        from solver.tests.test_switchover import Step2PutBack
        real = ce.balance
        bad = (ce.DTC_DT_RANGE[0], ce.H_CORE_RANGE[0])

        def planted(t_c, t_m_base, material_name, p_cmb, r_cmb, m_core, dtc_dt=ce.DTC_DT, h=ce.H_CORE):
            f, bl, terms = real(t_c, t_m_base, material_name, p_cmb, r_cmb, m_core, dtc_dt, h)
            if (dtc_dt, h) == bad:
                f += (1.0 if t_c < 3900.0 else -1.0) * 1e3 * bl["q_c_w"]
            return f, bl, terms
        with mock.patch.object(ce, "balance", planted):
            rec = ro.one("engine/bodies/earth.yaml", "declared", FAST,
                         registry=Step2PutBack._registry("W-L1-01", "P5-F1"))
        node = self._balance(rec)
        self.assertTrue(node["applicable"])
        self.assertLess(abs(node["values"]["balance_residual"]), ro.lv.BALANCE_TOL)
        self.assertIsNone(node["values"]["core_cmb_temperature_solved_min"])
        self.assertIsNone(node["values"]["core_cmb_temperature_solved_max"])
        got = [n for n in rec["notes"] if n["kind"] == "core_balance_not_solved"]
        self.assertEqual(len(got), 1)
        self.assertEqual(got[0]["fields"]["failed"], "corners")
        self.assertEqual([(c["dtc_dt"], c["h"]) for c in got[0]["fields"]["corners"]], [bad])
        self.assertAlmostEqual(got[0]["fields"]["corners"][0]["t"], 3900.0, places=6)

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
        band = payload.Result(recipe="r", version="v", regime="x", reason="", grade="analog", inputs={},
                              values={"balance_residual": 6.5e-13, "core_cmb_temperature_solved_min": 3769.0,
                                      "core_cmb_temperature_solved_max": 4160.0},
                              units={"balance_residual": "", "core_cmb_temperature_solved_min": "K",
                                     "core_cmb_temperature_solved_max": "K"})
        roots = ((1, 1, 3770.0, 6.5e-13), (2, 0, 3769.0, 1e-12), (2, 1, 4160.0, 0.4))
        out, note = ro.lv.balance_guard(band, roots)
        self.assertTrue(out.applicable)
        self.assertEqual((out.values["core_cmb_temperature_solved_min"], out.values["core_cmb_temperature_solved_max"],
                          out.values["balance_residual"]), (None, None, 6.5e-13))
        self.assertEqual([(c["dtc_dt"], c["h"]) for c in note["fields"]["corners"]], [(2, 1)])
        self.assertEqual(ro.lv.balance_guard(band, roots[:2]), (band, None))


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


class SilicateFlag(unittest.TestCase):
    """Silicate record registration §4 / §6.1: a round states the switch either way, and an inverse body's member is
    solved under it (the member's CMF comes from the same mantle as the records)."""

    def _main_options(self, *flag, inverse=False):
        seen = {}
        real_one, real_member = ro.one, ro.mb.member_of

        def one(body_yaml, state, options=context.Options(), chain=True, member=None, registry=None):
            seen.setdefault("options", options)
            return {"header": {}, "state": state}

        def member_of(body, materials="registry", registry=None, silicate_records=False):
            seen["member_silicate"] = silicate_records
            return None
        p = Path(tempfile.mkdtemp(), "pts.json")
        p.write_text(json.dumps([["mars", 1800.0, "node"]] if inverse else []))
        ro.one, ro.mb.member_of = one, member_of
        try:
            rc = ro.main([f"engine/bodies/{'mars' if inverse else 'earth'}.yaml", str(p), tempfile.mkdtemp(), *flag])
        finally:
            ro.one, ro.mb.member_of = real_one, real_member
        return rc, seen

    def test_on_and_off_reach_the_options(self):
        for flag, want in ((("--silicate-records", "on"), True), (("--silicate-records", "off"), False),
                           ((), context.Options().silicate_records)):
            with self.subTest(flag=flag):
                rc, seen = self._main_options(*flag)
                self.assertEqual(rc, 0)
                self.assertIs(seen["options"].silicate_records, want)

    def test_a_bad_value_stops(self):
        for flag in (("--silicate-records",), ("--silicate-records", "yes")):
            with self.subTest(flag=flag):
                self.assertEqual(self._main_options(*flag)[0], 2)

    def test_the_member_is_solved_under_the_switch(self):
        """Mars is inverse with T_pot states: run_oracle.main solves its member once, under the round's switch."""
        for flag, want in ((("--silicate-records", "on"), True), (("--silicate-records", "off"), False)):
            with self.subTest(flag=flag):
                rc, seen = self._main_options(*flag, inverse=True)
                self.assertEqual(rc, 0)
                self.assertIs(seen["member_silicate"], want)


if __name__ == "__main__":
    unittest.main()
