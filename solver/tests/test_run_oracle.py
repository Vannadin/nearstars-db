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
#: keys an answer record may carry beyond FIELDS, each written only on an answer (zones-prereg post-freeze note 1, 68 B1;
#: fe_budget_misfit: layers S1 §2.5, written in the answer branch for a bulk_plan body only)
ANSWER_ONLY = {"zones", "fe_budget_misfit"}


def contract_problems(rec) -> list:
    """The record's key set against the contract FIELDS ∪ (ANSWER_ONLY on an answer): [] when it holds."""
    keys = set(rec)
    out = [f"missing {sorted(FIELDS - keys)}"] if FIELDS - keys else []
    extra = keys - FIELDS - (ANSWER_ONLY if rec.get("outcome_kind") == "answer" else set())
    return out + ([f"unknown {sorted(extra)}"] if extra else [])


class Earth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rec = ro.one("engine/bodies/earth.yaml", "declared", FAST)

    def test_contract_fields(self):
        self.assertEqual(contract_problems(self.rec), [])
        self.assertEqual(self.rec["outcome_kind"], "answer")
        self.assertTrue(self.rec["header"]["engine_identical_to_oracle_tree"])
        self.assertEqual(len(self.rec["header"]["solve_id"]), 64)

    def test_header_carries_both_oracle_trees(self):
        """Owner-direction c573d894: the phase-1 commit stays named, and the engine tree the oracle now is (the core
        two-anchor item's engine/) is the one `engine_identical_to_oracle_tree` compares against."""
        h = self.rec["header"]
        self.assertEqual(h["oracle_tree"], "097a8aa3cfaf0b42f0b8c3a451a391095cc5c6cc")
        self.assertEqual(h["oracle_engine_tree"], ro.ORACLE_ENGINE_TREE)
        self.assertRegex(ro.ORACLE_ENGINE_TREE, r"^[0-9a-f]{40}$")
        real = ro.ORACLE_ENGINE_TREE
        try:                                         # negative control: another declared tree is not identical
            ro.ORACLE_ENGINE_TREE = "0" * 40
            self.assertFalse(ro._header(FAST, "")["engine_identical_to_oracle_tree"])
        finally:
            ro.ORACLE_ENGINE_TREE = real

    def test_notes_are_written_as_kinded_objects(self):
        """Switch-over §6.7: `notes` is a list of objects with a text `kind` (comparator note 15's shape)."""
        self.assertIsInstance(self.rec["notes"], list)
        self.assertTrue(all(isinstance(n, dict) and isinstance(n.get("kind"), str) for n in self.rec["notes"]))

    def test_table_read_from_the_committed_table(self):
        """B1: true because core_thermal_history read engine/structure_grid/earth.json at its TABLE_TREE blob (E-steps R7b)."""
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


class Venus(unittest.TestCase):
    def test_boundary_mass_body_writes_a_record_without_the_fe_budget(self):
        """68 51c3a7658 (ii): at ab5287970 run_oracle.one raised on every boundary_mass body (fe_budget_record read
        `q.value` before its plan check, S1 9c4ea96b); venus (from_v1: fe_prem core, plain silicate mantle, closure
        boundary_mass) now writes its record, with no fe_budget_misfit since it carries no bulk_plan."""
        rec = ro.one("engine/bodies/venus.yaml", "declared", FAST)
        self.assertEqual(contract_problems(rec), [])
        self.assertEqual(rec["outcome_kind"], "answer")
        self.assertNotIn("fe_budget_misfit", rec)
        self.assertIn("core_mass_fraction", {q["key"] for q in rec["quantities"]})


class BulkMarsEndToEnd(unittest.TestCase):
    """Directing 11-13 (iii): S1 §2.5's (b2) Fe-budget record had only the planted test; this is one real run.
    The fixture is S1's bulk Mars (test_bulk_validate.mars_doc: Khan 2022 bulk, a measured radius, so (E) gives
    closure boundary_mass on the core), written to a body file and run through run_oracle.one with silicate_records
    on (its composition key is the khan record's). Wang's bulk Earth cannot be the fixture: its solve refuses
    no_table_for_composition (S1 test 4's note)."""

    def test_the_record_carries_the_fe_budget_by_hand(self):
        import dataclasses
        import yaml
        from solver.tests.test_bulk_validate import mars_doc
        opt = dataclasses.replace(FAST, silicate_records=True)
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "bulk_mars.yaml"
            doc = mars_doc()
            doc["inputs"]["potential_temperature"] = 1600.0     # mars.yaml's declared T_pot: the read needs a T path
            path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
            body = ro.load_body(str(path))
            rec = ro.one(str(path), "declared", opt)
        self.assertEqual(rec["outcome_kind"], "answer", rec.get("refusal") or rec.get("no_answer"))
        fe = rec["fe_budget_misfit"]
        plan = body.layers[1].composition.extra["bulk_plan"]
        cmf = next(q["point"] for q in rec["quantities"] if q["key"] == "core_mass_fraction")
        # by hand: implied = x_Fe × fitted CMF, declared = fe_metal_fraction × bulk Fe (partition.fe_budget_misfit)
        self.assertEqual(fe["fitted_core_mass_fraction"], cmf)
        self.assertEqual(fe["implied_core_Fe"], plan["x_Fe"] * cmf)
        self.assertEqual(fe["declared_core_Fe"], plan["fe_metal_fraction"] * plan["bulk_Fe"])
        self.assertEqual(fe["misfit"], plan["x_Fe"] * cmf - plan["fe_metal_fraction"] * plan["bulk_Fe"])
        print(f"\n  bulk Mars: fitted CMF {cmf!r}, implied core Fe {fe['implied_core_Fe']!r}, declared "
              f"{fe['declared_core_Fe']!r}, misfit {fe['misfit']!r}")


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
        self.assertEqual(contract_problems(rec), [])
        for node in ("core_state", "cmb_heat_flux", "core_energy_balance"):
            if node in rec["legacy_nodes"]:
                self.assertFalse(rec["legacy_nodes"][node]["applicable"], node)


class ContractControls(unittest.TestCase):
    """contract_problems' own controls (68 B1 on zones note 1): no solve."""

    def _rec(self, kind):
        return {**{k: None for k in FIELDS}, "outcome_kind": kind}

    def test_answer_with_zones_holds(self):
        self.assertEqual(contract_problems({**self._rec("answer"), "zones": []}), [])

    def test_unknown_extra_key_is_red(self):
        self.assertEqual(contract_problems({**self._rec("answer"), "zones": [], "bogus": 1}), ["unknown ['bogus']"])

    def test_zones_on_a_refusal_is_red(self):
        self.assertEqual(contract_problems({**self._rec("refusal"), "zones": []}), ["unknown ['zones']"])

    def test_answer_with_fe_budget_misfit_holds(self):
        self.assertEqual(contract_problems({**self._rec("answer"), "zones": [], "fe_budget_misfit": {}}), [])

    def test_fe_budget_misfit_on_a_refusal_is_red(self):
        self.assertEqual(contract_problems({**self._rec("refusal"), "fe_budget_misfit": {}}),
                         ["unknown ['fe_budget_misfit']"])

    def test_missing_field_is_red(self):
        rec = self._rec("answer")
        del rec["table_read"]
        self.assertEqual(contract_problems(rec), ["missing ['table_read']"])


class NoChainForPoints(unittest.TestCase):
    """--no-chain-for-points: a T_pot state skips the old chain (O9 reads interior_layers only); the declared state
    keeps it (control)."""

    def test_point_has_no_legacy_nodes(self):
        rec = ro.one("engine/bodies/earth.yaml", 2093.0, context.Options(sensitivity_dt=0.0), chain=False)
        self.assertEqual((rec["outcome_kind"], rec["legacy_nodes"], rec["table_read"], rec["header"]["chain"]),
                         ("answer", {}, False, False))
        self.assertEqual(contract_problems(rec), [])

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

    def test_on_with_legacy_materials_stops(self):
        """68 B2: a legacy solve resolves no record, so «on» there would be a header that lies."""
        self.assertEqual(self._main_options("--silicate-records", "on", "--legacy-materials")[0], 2)
        self.assertEqual(self._main_options("--silicate-records", "off", "--legacy-materials")[0], 0)

    def test_member_of_solves_under_the_switch(self):
        """68 B1: the switch reaches member_of's own declared-state solve, not only member_of's signature."""
        from solver import from_v1, member as mb, solve as sv
        got = from_v1.load_v1("engine/bodies/mars.yaml")
        body = got[0] if isinstance(got, tuple) else got
        seen, real = [], sv.solve

        def spy(b, options=context.Options(), *a, **k):
            seen.append(options.silicate_records)
            return object(), None                                     # not an Answer: member_of returns early
        sv.solve = spy
        try:
            for want in (True, False):
                mb.member_of(body, silicate_records=want)
        finally:
            sv.solve = real
        self.assertEqual(seen, [True, False])

    def test_one_passes_the_switch_to_its_member_fallback(self):
        """68 S1b: one() with member=None solves the member itself, under the options' switch."""
        seen, real = [], ro.mb.member_of

        def member_of(body, materials="registry", registry=None, silicate_records=False):
            seen.append(silicate_records)
            return None, {"declared_outcome": "Refusal", "x": None}
        ro.mb.member_of = member_of
        try:
            for want in (True, False):
                ro.one("engine/bodies/mars.yaml", 1800.0, context.Options(sensitivity_dt=0.0, silicate_records=want),
                       chain=False, member=None)
        finally:
            ro.mb.member_of = real
        self.assertEqual(seen, [True, False])




class BulkRecord(unittest.TestCase):
    """layers S1 §2.5 (1346ffc6): `fe_budget_misfit` is written only for a bulk_plan body under boundary_mass, with
    its inputs and grade; every other record keeps exactly FIELDS (the contract becomes FIELDS ∪ optional {member,
    fe_budget_misfit}). No solve: a planted answer carries the fitted core mass."""

    def test_builder_and_its_absence(self):
        import types
        from solver import validate as vd
        from solver.tests.test_bulk_validate import mars_doc
        b = vd.validate(mars_doc(), "bulk_mars", vd.production_materials(vd.PRODUCTION))
        # a real result.Quantity (68 51c3a7658: the SimpleNamespace double with `.value` hid that a Quantity has `point`)
        import dataclasses
        from solver.tests.test_types import _q
        ans = types.SimpleNamespace(quantities=[dataclasses.replace(_q(point=0.251), key="core_mass_fraction", unit="1")])
        fe = ro.fe_budget_record(b, ans)
        plan = b.layers[1].composition.extra["bulk_plan"]
        self.assertEqual(set(fe), {"implied_core_Fe", "declared_core_Fe", "misfit", "fitted_core_mass_fraction",
                                   "x_Fe", "bulk_Fe", "fe_metal_fraction", "grade"})
        self.assertAlmostEqual(fe["implied_core_Fe"], plan["x_Fe"] * 0.251, places=15)
        self.assertAlmostEqual(fe["declared_core_Fe"], plan["fe_metal_fraction"] * plan["bulk_Fe"], places=15)
        self.assertAlmostEqual(fe["misfit"], plan["x_Fe"] * 0.001, places=12)    # declared = x_Fe × 0.250
        earth = from_v1_body("earth")
        self.assertIsNone(ro.fe_budget_record(earth, ans))           # no bulk_plan: nothing written
        venus = from_v1_body("venus")                                # boundary_mass, no bulk_plan: nothing read
        self.assertEqual(venus.closure.kind, "boundary_mass")
        unreadable = types.SimpleNamespace(quantities=[types.SimpleNamespace(key="core_mass_fraction")])
        self.assertIsNone(ro.fe_budget_record(venus, unreadable))   # the plan check comes before the answer's read

    def test_v2_branch_keyed_on_top_level_bulk(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.yaml"
            p.write_text("name: x\nkind: planet\ninputs: {mass_earth: 1.0}\nbulk: {preset: earth_like}\n")
            self.assertTrue(ro.is_bulk_v2(str(p)))
        self.assertFalse(ro.is_bulk_v2(str(Path(ro.REPO) / "engine" / "bodies" / "earth.yaml")))


def from_v1_body(stem):
    from solver import from_v1
    return from_v1.load_v1(str(Path(ro.REPO) / "engine" / "bodies" / f"{stem}.yaml"))[0]

if __name__ == "__main__":
    unittest.main()
