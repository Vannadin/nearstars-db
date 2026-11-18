# 출하 데이터 건너뜀 검사 시험 — «shipped» 를 이유로 건너뛰는 모든 skipUnless·skipTest 조건이 기록이 실린 TIP 에서 참인지
"""A guard that skips a test when the shipped data is absent must not skip at a tip that ships it (directing 10-18: a
«*.json» glob against tables shipped as «*.json.gz» skipped test_planted_coverage_real at every tip, and the EVC physics
gate, which fails on any skip, caught it on the PC).

Every guard in solver/tests whose reason names shipped data — a «@unittest.skipUnless(cond, "… shipped …")» decorator,
or «if not cond: self.skipTest("… shipped …")» — is found by reading the test sources, and its condition is evaluated in
its own module. An operand of an «and» that reads a tier switch (env_tiers.yaml class «tier»: NEARSTARS_HEAVY,
NS_SLOW_TESTS; HEAVY-onctl P3) is dropped (that half is the environment's, not the data's). When
this tip ships the SLB records, every such condition must be true.
A guard on shipped data must say «shipped» in its reason: the scan keys on that word, and one worded otherwise escapes
it (68 n2 on e129f820; the ≥12 control catches only a lost guard)."""
import ast
import importlib
import unittest
from pathlib import Path

import yaml

from solver import material_registry as mr

TESTS = Path(__file__).resolve().parent
RECORDS = sorted(mr.MATERIALS_DIR.glob("silicate_slb_*.yaml"))          # the anchor: the record files, not a table glob
TIER_ENVS = sorted(n for n, v in yaml.safe_load(TESTS.joinpath("env_tiers.yaml").read_text())["names"].items()
                   if v["class"] == "tier")


def _is_heavy(node):
    src = ast.unparse(node)
    return src == "HEAVY" or any(n in src for n in TIER_ENVS)     # P3: every tier, not NEARSTARS_HEAVY alone


def _data_part(cond):
    """The condition without its tier operands (None if nothing else is left)."""
    if isinstance(cond, ast.BoolOp) and isinstance(cond.op, ast.And):
        rest = [v for v in cond.values if not _is_heavy(v)]
        if not rest:
            return None
        return rest[0] if len(rest) == 1 else ast.BoolOp(op=ast.And(), values=rest)
    return None if _is_heavy(cond) else cond


def _reason(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else ""


def guards():
    """[(module, line, condition source, reason)] for every shipped-data guard in solver/tests."""
    out = []
    for path in sorted(TESTS.glob("test_*.py")):
        tree = ast.parse(path.read_text())
        mod = f"solver.tests.{path.stem}"
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and ast.unparse(node.func) in ("unittest.skipUnless", "skipUnless")
                    and len(node.args) == 2 and "shipped" in _reason(node.args[1])):
                cond = _data_part(node.args[0])
                if cond is not None:
                    out.append((mod, node.lineno, ast.unparse(cond), _reason(node.args[1])))
            if isinstance(node, ast.If) and isinstance(node.test, ast.UnaryOp) and isinstance(node.test.op, ast.Not):
                for st in node.body:
                    call = st.value if isinstance(st, ast.Expr) else None
                    if (isinstance(call, ast.Call) and ast.unparse(call.func).endswith("skipTest") and call.args
                            and "shipped" in _reason(call.args[0])):
                        out.append((mod, node.lineno, ast.unparse(node.test.operand), _reason(call.args[0])))
    return out


class ShippedGuards(unittest.TestCase):
    def test_the_scan_finds_the_guards(self):
        """Control: the scan sees the known guards (the glob fixed 10-18 and the module-level _shipped helpers), so an
        empty scan cannot pass for «every guard true»."""
        found = guards()
        mods = {m for m, *_ in found}
        self.assertGreaterEqual(len(found), 12)
        for m in ("solver.tests.test_material_assemblage", "solver.tests.test_assemblage_c1",
                  "solver.tests.test_assemblage_boundaries", "solver.tests.test_read_determinism",
                  "solver.tests.test_switchover", "solver.tests.test_closure"):
            self.assertIn(m, mods)

    @unittest.skipUnless(RECORDS, "no SLB record yaml at this tip (an engine branch without records)")
    def test_every_shipped_guard_is_true_at_a_tip_that_ships(self):
        """At a tip that ships the SLB records (their yaml), no shipped-data guard may skip: each condition is true in
        its own module."""
        for mod, line, cond, why in guards():
            with self.subTest(guard=f"{mod}:{line}", cond=cond):
                ns = vars(importlib.import_module(mod))
                self.assertTrue(eval(compile(cond, f"{mod}:{line}", "eval"), ns), f"{cond!r} is false: «{why}»")

    def test_a_wrong_glob_is_caught(self):
        """Control: the old guard, a «*.json» glob against the gzipped tables, evaluates false here."""
        self.assertFalse(sorted((mr.MATERIALS_DIR / "tables").glob("silicate_slb_*.json")))


# ── every skip site registered (directing 11-18, (B)): data skips evaluated at a tip with records ─────────────────────
def sites(sources=None):
    """{key: reason} for every skip site in solver/tests — a skipUnless / skipIf / skip decorator, a `.skipTest(` call,
    a `raise …SkipTest(…)` — keyed «module:qualname:form». `sources`: {stem: text} instead of the files (controls)."""
    if sources is None:
        sources = {p.stem: p.read_text() for p in sorted(TESTS.glob("*.py"))
                   if p.name not in ("test_skip_guards.py", "env_scan.py")}
    out = {}

    def walk(node, q, stem):
        for ch in ast.iter_child_nodes(node):
            qq = q
            if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                qq = q + [ch.name]
                for d in ch.decorator_list:
                    if isinstance(d, ast.Call) and ast.unparse(d.func).split(".")[-1] in ("skipUnless", "skipIf", "skip"):
                        form = ast.unparse(d.func).split(".")[-1]
                        out[f"{stem}:{'.'.join(qq)}:{form}"] = ast.unparse(d.args[-1]) if d.args else ""
            if isinstance(ch, ast.Call) and isinstance(ch.func, ast.Attribute) and ch.func.attr == "skipTest":
                out[f"{stem}:{'.'.join(q)}:skipTest"] = ast.unparse(ch.args[0]) if ch.args else ""
            if isinstance(ch, ast.Raise) and ch.exc is not None and "SkipTest" in ast.unparse(ch.exc):
                out[f"{stem}:{'.'.join(q)}:raise"] = ast.unparse(ch.exc)
            walk(ch, qq, stem)
    for stem, text in sources.items():
        walk(ast.parse(text), [], stem)
    return out


#: every skip site, by kind. «data»: the data a tip with records ships; its probe must hold there — ("expr", source
#: evaluated in the test module), ("call", module function that must not raise SkipTest), ("run", Class.test that must
#: run without skipping). «tier»: an env_tiers.yaml tier switch (NEARSTARS_HEAVY, NS_SLOW_TESTS), listed, not
#: evaluated. «env»: an input from outside the tree, named; listed, not evaluated at the tip.
REGISTRY = {
    "test_assemblage_boundaries:Envelope.test_cp_positive_everywhere:skipUnless": ("data", ("expr", "_shipped()")),
    "test_assemblage_boundaries:Envelope.test_rho_rises_where_the_table_rises:skipUnless": ("data", ("expr", "_shipped()")),
    "test_assemblage_c1:C1.test_continuous_at_every_cut_edge:skipUnless": ("data", ("expr", "_shipped()")),
    "test_assemblage_c1:C1.test_c0_plants_go_red:skipUnless": ("data", ("expr", "_shipped()")),
    "test_assemblage_c1:C1.test_side_reads_leave_no_note:skipUnless": ("data", ("expr", "_shipped()")),
    "test_assemblage_c1:C1.test_kinks_named_and_bounded_subset:skipUnless": ("data", ("expr", "_shipped()")),
    "test_assemblage_c1:RunEnd.test_cap_by_field_wired:skipUnless": ("data", ("expr", "_shipped()")),
    "test_assemblage_c1:RunEnd.test_named_rho_cases:skipUnless": ("data", ("expr", "_shipped()")),
    "test_closure:GapOnMars.test_mars_2450_answers_inside_the_ceiling_or_refuses_by_it:skipUnless": ("tier", "NEARSTARS_HEAVY"),
    "test_closure:GapOnMars.test_mars_2450_answers_inside_the_ceiling_or_refuses_by_it:skipTest": ("data", ("expr", "_mars_shipped()")),
    "test_closure:GapOnMars.test_declared_state_keeps_its_margin_under_the_ceiling:skipUnless": ("tier", "NEARSTARS_HEAVY"),
    "test_closure:GapOnMars.test_declared_state_keeps_its_margin_under_the_ceiling:skipTest": ("data", ("expr", "_mars_shipped()")),
    "test_coexist:ShippedViews.test_every_cut_row_has_a_hook:skipUnless": ("data", ("expr", "__import__('solver.tests.test_assemblage_c1', fromlist=['_shipped'])._shipped()")),
    "test_coexist:FindingIsNotBlind.test_shipped_gap_rows_read_continuous:skipUnless": ("data", ("expr", "__import__('solver.tests.test_assemblage_c1', fromlist=['_shipped'])._shipped()")),
    "test_curve_scale:OffUnchanged:skipUnless": ("tier", "NEARSTARS_HEAVY"),
    "test_d2_store:Edges.test_h6_on_the_stores_certified_extension_rows:skipTest": ("data", ("run", "Edges.test_h6_on_the_stores_certified_extension_rows")),
    "test_fall_set_stamp:FallSetStamp.setUp:skipTest": ("data", ("expr", "not isinstance(mr.load(), mr.LoadStop)")),
    "test_fall_sets:Missing.test_missing_refuses_on_a_view:skipUnless": ("data", ("expr", "_shipped_present()")),
    "test_fall_sets:Missing.test_missing_refuses_at_registry_load:skipUnless": ("data", ("expr", "_shipped_present()")),
    "test_fall_sets:Missing.test_repair_off_reads_nothing:skipUnless": ("data", ("expr", "_shipped_present()")),
    "test_fall_sets:Missing.test_a_reused_shipped_id_is_not_the_shipped_record:skipUnless": ("data", ("expr", "_shipped_present()")),
    "test_fall_sets:Missing.test_non_registry_id_gets_none:skipUnless": ("data", ("expr", "_shipped_present()")),
    "test_fall_sets:Shipped.test_every_shipped_record_loads:skipUnless": ("data", ("expr", "_shipped_present()")),
    "test_fall_sets:CensusDrift:skipUnless": ("tier", "NS_SLOW_TESTS (its data half, _shipped_present(), is checked here)"),
    "test_fall_sets:E24Conditional.test_shipped_default_is_a_plain_pass:skipUnless": ("data", ("expr", "_shipped_present()")),
    "test_material_assemblage:TableChecks.test_planted_coverage_real:skipUnless": ("data", ("expr", "_shipped_tables()")),
    "test_melt_window:GradeNoteAnswers:skipUnless": ("tier", "NEARSTARS_HEAVY"),
    "test_melt_window:SeamNoteAnswers:skipUnless": ("tier", "NEARSTARS_HEAVY"),
    "test_member:OldMember.test_venus_point:skipUnless": ("env", "NEARSTARS_ARTIFACTS (the oracle capture beside the worktree)"),
    "test_read_conformance:Conformance.test_c8_committed_read:raise": ("env", "NEARSTARS_C8_PROTO (c8's committed read)"),
    "test_read_determinism:Determinism.test_reads_do_not_depend_on_addresses:skipUnless": ("data", ("expr", "_shipped()")),
    "test_read_determinism:Determinism.test_reads_do_not_depend_on_read_order:skipUnless": ("data", ("expr", "_shipped()")),
    "test_read_determinism:Determinism.test_solve_answer_sha:skipUnless": ("tier", "NEARSTARS_HEAVY (its data half, _shipped(), is checked here)"),
    "test_rho_net_fall:_khan:raise": ("data", ("call", "_khan")),
    "test_rho_rev3d:ClipNetFall._plant:skipTest": ("data", ("run", "ClipNetFall")),
    "test_rho_row_steps:_view:raise": ("data", ("expr", "all(_view(r) is not None for r in (BSE, 'silicate_slb_mars_khan2022', "
                                                "'silicate_slb_earth_dmm_wh2005'))")),
    "test_swap_extension:_bse_view:raise": ("data", ("call", "_bse_view")),
    "test_swap_extension:ReachZeroEnds.test_the_repair_bridges_the_falling_step:skipTest": ("env", "NS_FALL_SETS (the fall set loaded for bse)"),
    "test_swap_extension:CoincidentEdgeSwapsReachZero.test_flags_left_to_build_curves_is_red:raise": ("data", ("expr", "'extension' in __import__('solver.material_registry', "
                                                "fromlist=['load']).load().tables[BSE].get('boundaries', {})")),
    "test_switchover:RecordEvents.test_edge_lands_at_its_p_scale:skipUnless": ("data", ("expr", "_shipped_bse()")),
    "test_t_mars:TwoRootsStable:skipUnless": ("tier", "NEARSTARS_HEAVY"),
    "test_t_mars:MeltWindow:skipUnless": ("tier", "NEARSTARS_HEAVY"),
    "test_tjump:CommittedRead.read:raise": ("env", "NEARSTARS_C8_PROTO (c8's committed read)"),
}


class EverySkipRegistered(unittest.TestCase):
    def test_every_site_is_registered_and_every_entry_is_a_site(self):
        found = sites()
        self.assertEqual(sorted(set(found) - set(REGISTRY)), [], "unregistered skip sites: register each by kind")
        self.assertEqual(sorted(set(REGISTRY) - set(found)), [], "registry entries with no skip site: remove them")

    def test_a_planted_site_is_unregistered(self):
        """Control: a new skip site in a planted module is found and is not in the registry."""
        planted = {"test_planted": "import unittest\nclass X(unittest.TestCase):\n    def test_a(self):\n"
                                   "        if not 0:\n            self.skipTest('planted')\n"}
        self.assertEqual(set(sites(planted)) - set(REGISTRY), {"test_planted:X.test_a:skipTest"})

    @unittest.skipUnless(RECORDS, "no SLB record yaml at this tip (an engine branch without records)")
    def test_data_skips_hold_at_a_tip_with_records(self):
        for key, (kind, probe) in sorted(REGISTRY.items()):
            if kind != "data":
                continue
            stem = key.split(":")[0]
            mod = importlib.import_module(f"solver.tests.{stem}")
            with self.subTest(site=key):
                how, what = probe
                if how == "expr":
                    self.assertTrue(eval(compile(what, key, "eval"), vars(mod)), f"{what!r} is false at this tip")
                elif how == "call":
                    try:
                        getattr(mod, what)()
                    except unittest.SkipTest as e:
                        self.fail(f"{what}() skips at this tip: {e}")
                else:
                    suite = unittest.defaultTestLoader.loadTestsFromName(what, mod)
                    res = unittest.TestResult()
                    suite.run(res)
                    self.assertEqual([str(t) for t, _ in res.skipped], [], f"{what} skipped at this tip")
                    self.assertTrue(res.wasSuccessful(), f"{what} did not pass: {res.failures + res.errors}")


if __name__ == "__main__":
    unittest.main()
