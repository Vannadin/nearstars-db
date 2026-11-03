# 파생 파일 관문 시험 — 조사(기본 거부)가 오늘 트리에서 통과하고, 해시 규칙·스탬프 대조·DAG·재스탬프 까닭·닫힘이 심은 대조군에서 제 결과를 내는지
"""python3 derived/test_derived.py   (prereg pc/sg-gate/prereg-sg-gate.frozen.md 1765b55c; the landing runs it as the
census step's companion). Planted controls run on strings and scratch dicts; nothing in the tree is changed."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check as ck                                     # noqa: E402
import digest as dg                                    # noqa: E402

DOC = ck.load_list()


class Census(unittest.TestCase):
    def test_tree_passes(self):
        self.assertEqual(ck.census(DOC), [])

    def test_every_prereg_row_is_listed(self):
        rows = {str(e["row"]) for e in ck.entries(DOC).values()}
        self.assertEqual(rows, {"1", "2", "3", "4", "5", "6", "7", "8a", "8b", "8c", "8d", "9", "10"})

    def test_planted_unlisted_json_and_generated_py_are_red(self):
        """N17: an unlisted .json under engine/, and a .py with the generated header that is not listed."""
        files = ck.tracked() + ["engine/planted_table.json", "engine/planted_gen.py"]
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for f in files:
                (root / f).parent.mkdir(parents=True, exist_ok=True)
                src = ck.REPO / f
                (root / f).write_bytes(src.read_bytes() if src.is_file() else b"")
            (root / "engine/planted_gen.py").write_text(f"# 표 — {ck.GENERATED_MARK}\nX = 1\n", encoding="utf-8")
            reds = ck.census(DOC, files=files, root=root)
        self.assertTrue(any(r.startswith("engine/planted_table.json:") for r in reds), reds)
        self.assertTrue(any(r.startswith("engine/planted_gen.py:") for r in reds), reds)

    def test_dropped_entry_is_red(self):
        """A5 / r2 N1: deleting one entry from the list turns the census red (the block cannot see a missing row)."""
        doc = json.loads(json.dumps(DOC))
        del doc["entries"]["10-graph-page"]
        self.assertTrue(any("engine/chain-explorer.html" in r for r in ck.census(doc)))


class Digest(unittest.TestCase):
    A = 'def f():\n    """doc"""\n    x = 1  # note\n    return x\n'

    def test_comment_docstring_blank_do_not_move(self):
        """N2 / N15 kind: comments, docstrings and blank lines are ignored."""
        b = 'def f():\n    """another doc"""\n\n    x = 1\n    return x   # other\n'
        self.assertEqual(dg.digest_text(self.A), dg.digest_text(b))

    def test_code_moves(self):
        self.assertNotEqual(dg.digest_text(self.A), dg.digest_text(self.A.replace("x = 1", "x = 2")))

    def test_reformat_inside_a_statement_moves(self):
        self.assertNotEqual(dg.digest_text(self.A), dg.digest_text(self.A.replace("x = 1", "x=1")))

    def test_same_line_docstring_cut_by_span(self):
        self.assertEqual(dg.stripped('class A: """d"""; y = 2\n'), "class A: ; y = 2")

    def test_a_string_that_is_not_a_docstring_stays(self):
        self.assertIn('"kept"', dg.stripped('x = 1\ny = "kept"\n'))


class Stamps(unittest.TestCase):
    def setUp(self):
        self.now = {"stamp_rule": dg.STAMP_RULE, "files": {"a.json": "1"}, "code": {"engine/x.py": "c"},
                    "data": {}, "derived": {"engine/reference_adiabats.json": "r"}, "out_of_tree": {}, "packages": {},
                    "external": {}}

    def test_no_rule_reads_as_moved(self):
        """N5: a stamp with no stamp_rule is moved, never matched."""
        then = dict(self.now)
        del then["stamp_rule"]
        self.assertTrue(ck.moved(then, self.now))
        self.assertEqual(ck.moved(None, self.now), ["no stamp"])

    def test_unchanged(self):
        self.assertEqual(ck.moved(json.loads(json.dumps(self.now)), self.now), [])

    def test_upstream_move_is_named_as_input(self):
        """N16's naming: an upstream refresh reads «input <file> moved» downstream."""
        then = json.loads(json.dumps(self.now))
        then["derived"]["engine/reference_adiabats.json"] = "old"
        self.assertEqual(ck.moved(then, self.now), ["input engine/reference_adiabats.json moved"])

    def test_python_and_own_bytes_are_not_inputs(self):
        then = json.loads(json.dumps(self.now)) | {"python": "3.0"}
        self.assertEqual(ck.moved(then, self.now), [])
        then["files"]["a.json"] = "0"
        self.assertEqual(ck.own_bytes_moved(then, self.now), ["a.json"])


class Dag(unittest.TestCase):
    def test_order_puts_upstream_first(self):
        order = ck.dag_order(DOC)
        for down, up in (("1-earth", "2-reference-adiabats"), ("8b-fe-prem", "2-reference-adiabats"),
                         ("7-fall-sets", "8d-silicate-slb"), ("3-ice-giant-anchor", "9-water-table")):
            self.assertLess(order.index(up), order.index(down), (up, down))

    def test_cycle_and_stamp_dir_are_refused(self):
        doc = json.loads(json.dumps(DOC))
        doc["entries"]["2-reference-adiabats"]["derived"] = ["engine/structure_grid/earth.json"]
        with self.assertRaises(SystemExit):
            ck.dag_order(doc)
        doc = json.loads(json.dumps(DOC))
        doc["entries"]["10-graph-page"]["data"] = ["derived/stamps/1-earth.json"]
        with self.assertRaises(SystemExit):
            ck.dag_order(doc)


class Closure(unittest.TestCase):
    def test_structure_closure_is_the_computed_one(self):
        """M5: row 1's closure is computed (fe_liquid, rootfind and the generated tables are in it, not 4 hand-listed)."""
        mods = ck.closure(DOC["entries"]["1-earth"]["code"])
        for m in ("engine/interior.py", "engine/rootfind.py", "engine/fe_liquid.py", "engine/water_table.py"):
            self.assertIn(m, mods)
        self.assertGreater(len(mods), 4)


class Globs(unittest.TestCase):
    """68 n1 / n2 on 2be90e97 and B1's fix: data globs expand over tracked files only, and the DAG sees the expansion."""

    def test_glob_rule(self):
        rx = ck.glob_re("engine/**/*.py")
        for f, want in (("engine/x.py", True), ("engine/tools/x.py", True), ("engine/a/b/x.py", True),
                        ("engine2/x.py", False), ("engine/x.pyc", False), ("scripts/engine/x.py", False)):
            self.assertEqual(bool(rx.match(f)), want, f)
        self.assertFalse(ck.glob_re("phase4/*.yaml").match("phase4/sub/x.yaml"))

    def test_untracked_and_venv_are_no_input(self):
        files = ["phase4/a.yaml", "engine/.venv-gate/lib/x.py", "engine/x.py"]
        self.assertEqual(ck.expand(["phase4/*.yaml", "engine/**/*.py"], files), ["phase4/a.yaml", "engine/x.py"])

    def test_an_untracked_stray_stays_green(self):
        """a stray untracked phase4/*.yaml on this machine leaves row 10's stamp as it is (tracked files only)."""
        e = DOC["entries"]["10-graph-page"]
        before = ck.stamp("10-graph-page", e)
        stray = ck.REPO / "phase4" / "zz_untracked_stray_control.yaml"
        self.assertFalse(stray.exists())
        try:
            stray.write_text("planted: 1\n", encoding="utf-8")
            after = ck.stamp("10-graph-page", e)
        finally:
            stray.unlink()
        self.assertEqual(ck.moved(before, after), [])

    def test_a_glob_matching_an_unlisted_derived_file_is_refused(self):
        doc = json.loads(json.dumps(DOC))
        doc["entries"]["5-c143-inventory"]["derived"].remove("engine/water_table.py")
        with self.assertRaises(SystemExit) as cm:
            ck.dag_order(doc)
        self.assertIn("glob matches the derived file engine/water_table.py", str(cm.exception))

    def test_row5_reads_every_tracked_py_of_its_census(self):
        """B1: row 5's inputs cover every tracked .py under engine/ and scripts/ (data, derived or code)."""
        e = DOC["entries"]["5-c143-inventory"]
        st = ck.stamp("5-c143-inventory", e)
        have = set(st["data"]) | set(st["derived"]) | set(st["code"])
        want = {f for f in ck.tracked_all() if f.endswith(".py") and f.split("/")[0] in ("engine", "scripts")}
        self.assertEqual(want - have, set())


class DynamicImports(unittest.TestCase):
    """68 B1 class (measured on rows 4 and 7): modules imported by name at run time are in the closure."""

    def test_registry_walk_and_package_init(self):
        mods = ck.closure(DOC["entries"]["7-fall-sets"]["code"])
        for m in ("engine/hop_track.py", "engine/thermal_stack.py", "engine/samuel_model.py", "solver/__init__.py"):
            self.assertIn(m, mods)

    def test_literal_import_module(self):
        self.assertEqual(ck._dynamic_names("x.py", 'm = importlib.import_module("water_table")\n', ck.REPO),
                         {"water_table"})


class Restamp(unittest.TestCase):
    def test_reason_is_required_and_known(self):
        """N19's refusal half: no reason, or an unknown one, is refused (nothing written)."""
        for why in ("", "because", "rebuild", "verdict:abc"):
            with self.assertRaises(SystemExit):
                ck.restamp("6-mantle-tables", why)

    def test_ruling_only_for_stamp_only_entries(self):
        with self.assertRaises(SystemExit):
            ck.restamp("1-earth", "ruling:pc/x.md@abc")


class OutOfTree(unittest.TestCase):
    def test_artifacts_absent_is_red_not_skipped(self):
        """N12b: a NEARSTARS_ARTIFACTS that is not a checkout → the entry's stamp cannot be read (red)."""
        with self.assertRaises(LookupError):
            ck.out_of_tree_blobs(["rewrite/phase2-records/gen_h2o.py"], art_env="/nonexistent/artifacts")

    def test_failed_fetch_is_red_not_a_stale_main(self):
        """68 B1: a checkout whose fetch fails is red (named), even though an old main ref is there to read."""
        with tempfile.TemporaryDirectory() as d:
            run = lambda *a: subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, check=True)  # noqa
            run("init", "-q")
            run("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "x")
            run("update-ref", "refs/remotes/origin/main", "HEAD")              # a stale main is present
            run("remote", "add", "origin", "/nonexistent/remote.git")         # and the fetch must fail
            with self.assertRaises(LookupError) as cm:
                ck.artifacts_ref(Path(d))
            self.assertIn("fetch failed", str(cm.exception))


class NotRunLane(unittest.TestCase):
    """Directing's B2 ruling: an unset input var is «NOT RUN» outside the gate lane, red inside it."""
    E = {"files": ["engine/hhe_table.py"], "external": {"x": {"env": "NEARSTARS_EXTERNAL", "path": "nope"}}}

    def _judge(self, gate):
        lines = []
        saved = {k: os.environ.pop(k, None) for k in ("NEARSTARS_EXTERNAL", "GATE_RUNNING")}
        default = ck._default_dir
        try:
            ck._default_dir = lambda var: None                                # no default beside the repo
            if gate:
                os.environ["GATE_RUNNING"] = "1"
            rc = ck.judge_entry("planted-ext", self.E, out=lines.append)
        finally:
            ck._default_dir = default
            os.environ.pop("GATE_RUNNING", None)
            for k, v in saved.items():
                if v is not None:
                    os.environ[k] = v
        return rc, lines

    def test_outside_the_gate_lane(self):
        rc, lines = self._judge(False)
        self.assertEqual((rc, lines), (0, ["NOT RUN planted-ext: NEARSTARS_EXTERNAL unset"]))

    def test_inside_the_gate_lane(self):
        rc, lines = self._judge(True)
        self.assertEqual(rc, 1)
        self.assertTrue(lines[0].startswith("[RED] planted-ext"), lines)


class ExpectedRed(unittest.TestCase):
    """68 B4: the item matches only its registered trigger set; any other red on the entry stays red."""
    NINE = ["bytes.chain.yaml", "bytes.reference_adiabats.json", "chain_reads", "declared.basal_layer_density",
            "declared.basal_layer_thickness_km", "declared.core_light_elements", "declared.mantle_composition",
            "mantle_table", "sulphur_fixings"]

    def _named(self, data):
        lines, keep = [], ck.expected_red
        ck.expected_red = lambda name: {"id": "SG-MARS-HOLD", "triggers": self.NINE, "registered": "planted"}
        try:
            ck._named("1-mars", lines.append, data)
        finally:
            ck.expected_red = keep
        return lines

    def test_the_registered_set_is_expected(self):
        self.assertIn("EXPECTED RED", self._named(list(reversed(self.NINE)))[0])

    def test_a_tenth_trigger_stays_red(self):
        self.assertNotIn("EXPECTED RED", self._named(self.NINE + ["declared.mass_earth"])[0])

    def test_a_red_that_is_no_trigger_failure_stays_red(self):
        """own bytes edited, quick mode, the refusal cap, an unreadable input: data is None."""
        self.assertNotIn("EXPECTED RED", self._named(None)[0])

    def test_an_eight_trigger_subset_stays_red(self):
        """directing's registration 7aeef535: a smaller set changes the reason; the item is re-registered, not matched."""
        for drop in self.NINE:
            self.assertNotIn("EXPECTED RED", self._named([t for t in self.NINE if t != drop])[0])

    def test_the_registered_item(self):
        """the tree's item: exactly the nine, the registration blob, and no other entry cites it."""
        import yaml
        items = yaml.safe_load((ck.REPO / "scripts" / "gate_expected_red.yaml").read_text(encoding="utf-8"))
        mine = [i for i in items if i.get("id") == "SG-MARS-HOLD"]
        self.assertEqual(len(mine), 1)
        self.assertEqual(sorted(mine[0]["triggers"]), self.NINE)
        self.assertEqual(mine[0]["derived_entry"], "1-mars")
        self.assertEqual(mine[0]["step"], "derived 1-mars")
        self.assertEqual(mine[0]["registered"], "pc/sg-gate/sg-mars-hold-registration.md 7aeef535")
        self.assertEqual([i["id"] for i in items if i.get("derived_entry")], ["SG-MARS-HOLD"])

    def test_own_bytes_of_mars_json_stay_red(self):
        """an own-bytes edit of mars.json under the item: red, never EXPECTED (the real item and entry, a planted stamp)."""
        e = DOC["entries"]["1-mars"]
        then = json.loads(json.dumps(ck.stamp("1-mars", e)))
        then["files"]["engine/structure_grid/mars.json"] = "planted"
        lines, keep = [], ck.read_stamp
        ck.read_stamp = lambda name: then
        try:
            rc = ck.judge_entry("1-mars", e, out=lines.append)
        finally:
            ck.read_stamp = keep
        self.assertEqual(rc, 1)
        self.assertTrue(lines[0].startswith("[RED] 1-mars — its own bytes differ"), lines)
        self.assertFalse(any("EXPECTED RED" in ln for ln in lines), lines)

    def test_the_tree_lists_every_compact_8c_reads(self):
        """68 B3: 8c's derived inputs are the three SLB compacts its generator reads (measured)."""
        self.assertEqual(sorted(DOC["entries"]["8c-prem-handover"]["derived"]),
                         [f"solver/materials/tables/silicate_slb_{c}.json.gz"
                          for c in ("default_bse", "earth_dmm_wh2005", "mars_khan2022")])


class LoadCensus(unittest.TestCase):
    """G1 load census and N18: modules loaded by a run, judged against the entry's static closure (derived/load_census.py)."""
    PLANT = ("import importlib, sys\n"
             "sys.path.insert(0, {engine!r})\n"
             "def _imp(_):\n"
             "    importlib.import_module(''.join(['albe', 'do_table']))   # a computed name: no static scan sees it\n"
             "def direct():\n"
             "    _imp(0)\n"
             "def pooled():\n"
             "    import multiprocessing\n"
             "    with multiprocessing.get_context('fork').Pool(2) as p:\n"
             "        p.map(_imp, [0])\n")

    @classmethod
    def setUpClass(cls):
        import load_census as lc
        cls.lc = lc
        cls.row10 = set(ck.closure(ck.entries(DOC)["10-graph-page"]["code"]))

    def _run(self, func):
        self.assertNotIn("engine/albedo_table.py", self.row10)       # the control's precondition
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "plant_n18.py"
            f.write_text(self.PLANT.format(engine=str(ck.REPO / "engine")), encoding="utf-8")
            return subprocess.run([sys.executable, "-B", str(HERE / "load_census.py"), "--entry", "10-graph-page", "--",
                                   "--call", f"{f}:{func}"], cwd=ck.REPO, capture_output=True, text=True)

    def test_n18_computed_import_is_named_red(self):
        r = self._run("direct")
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn("[LOAD-RED] 10-graph-page", r.stdout)
        self.assertIn("engine/albedo_table.py", r.stdout)

    def test_n18_in_a_pool_worker_is_seen(self):
        """A pool worker's import is seen: the census replaces multiprocessing pools with an in-process stand-in."""
        r = self._run("pooled")
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn("engine/albedo_table.py", r.stdout)

    def test_outside_keeps_closure_and_names_the_rest(self):
        inside = sorted(self.row10)[0]
        self.assertEqual(self.lc.outside("10-graph-page", [inside, "engine/albedo_table.py"]), ["engine/albedo_table.py"])

    def test_target_files_of_unittest(self):
        self.assertEqual(self.lc.target_files(["-m", "unittest", "solver.tests.test_fall_set_stamp"]),
                         ["solver/__init__.py", "solver/tests/__init__.py", "solver/tests/test_fall_set_stamp.py"])

    def test_census_target_pc_substitution_and_external_env(self):
        self.assertIsNone(ck.census_target({"census": {"where": "pc", "how": "x"}}))
        with tempfile.TemporaryDirectory() as d:
            ext = ck.env_dir("NEARSTARS_EXTERNAL", given=d)
            e = {"census": {"argv": ["engine/tools/x.py", "{external}/T"], "restore": True},
                 "external": {"P": {"env": "NEARSTARS_EXTERNAL", "path": "T"}}}
            orig, ck.env_dir = ck.env_dir, lambda var, given=None: ext
            try:
                target, flags, env = ck.census_target(e)
            finally:
                ck.env_dir = orig
        self.assertEqual(target, ["engine/tools/x.py", f"{d}/T"])
        self.assertEqual(flags, ["--restore"])
        self.assertEqual(env, {"NEARSTARS_EXTERNAL": d})

    def test_every_entry_has_a_census_and_checks_name_tolerance(self):
        doc = json.loads(json.dumps(DOC))
        e = doc["entries"]["10-graph-page"]
        del e["check"]["tolerance"]
        doc["entries"]["9-hhe-table"].pop("census")
        reds = ck.census(doc)
        self.assertIn("10-graph-page: its check names no tolerance (G1)", reds)
        self.assertTrue(any(r.startswith("9-hhe-table: no load census (G1)") for r in reds), reds)

    def test_rebuild_restamp_refuses_on_a_census_red(self):
        """G1 «at each rebuild of the entry»: a stamp-only entry's rebuild restamp runs its census; a red refuses."""
        orig, ck.run_census = ck.run_census, lambda name, e: (False, "[LOAD-RED] planted")
        try:
            with self.assertRaises(SystemExit) as cm:
                ck.restamp("9-hhe-table", "rebuild:planted")
        finally:
            ck.run_census = orig
        self.assertIn("load census", str(cm.exception))

    def test_call_args_take_the_env_dirs(self):
        e = {"census": {"call": "derived/census_targets.py:ammonia_table", "args": ["{papers}"]}}
        orig, ck.env_dir = ck.env_dir, lambda var, given=None: "/P"
        try:
            target, _, _ = ck.census_target(e)
        finally:
            ck.env_dir = orig
        self.assertEqual(target, ["--call", "derived/census_targets.py:ammonia_table", '["/P"]'])

    def test_restore_removes_only_new_untracked(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "old.txt").write_text("x")
            before = self.lc.untracked(root)
            (root / "new.part").write_text("y")
            self.assertEqual(self.lc.remove_new(before, root), ["new.part"])
            self.assertTrue((root / "old.txt").is_file())
            self.assertFalse((root / "new.part").exists())


if __name__ == "__main__":
    unittest.main()
