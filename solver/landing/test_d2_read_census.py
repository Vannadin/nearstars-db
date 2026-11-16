# D2 읽기 독자 조사 도구의 시험 — 다시 만든 목록 = 커밋된 목록, 종류별 규칙, 임시 사본에 심은 대조군(D2 읽기 등록 §7)
"""D2-read rev 7 §7's tests: regenerated equals committed; each kind's rule (with c8's `switch` kind and its `use`,
§5b); the planted controls (a raw table["boundaries"] read, a table_regardless= site, a boundary_block call with a
non-literal or unlisted use), planted in a temp copy of the tree, never in the tree."""
import contextlib
import io
import json
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

from solver.landing import d2_read_census as c

ROOT = Path(__file__).resolve().parents[2]


def kinds(src, path="solver/x.py"):
    return sorted((line, kind, fn) for _, line, kind, fn, _use in c.sites_of(path, textwrap.dedent(src)))


class TempCopy:
    """the tree's census inputs (every .py git lists, the schema, the committed JSON, .gitignore files) copied into a
    fresh git work tree, so a plant never touches the real one"""

    def __enter__(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="d2-census-")
        self.root = Path(self.tmp.name)
        names = c.py_files(ROOT) + [c.SCHEMA, c.OUT, c.OWN_TEST]
        names += subprocess.run(["git", "-C", str(ROOT), "ls-files", "--", "*.gitignore", ".gitignore"],
                                capture_output=True, text=True, check=True).stdout.split()
        for n in names:
            if (ROOT / n).is_file():
                (self.root / n).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / n, self.root / n)
        git(self.root, "init", "-q")
        git(self.root, "add", "--", *[n for n in names if (self.root / n).is_file()])
        return self.root

    def __exit__(self, *exc):
        self.tmp.cleanup()


def git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


def check(root):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = c.main(["check"], root=root)
    return rc, buf.getvalue()


class Kinds(unittest.TestCase):
    """each kind's recognizer, with its near misses"""

    def test_option(self):
        self.assertEqual(kinds("""
            def f(opts, silicate_records=False):
                a = opts.silicate_records
                b = opts["silicate_records"]
                c = opts.get("requires_switch")
                d = rec.get("requires_switch") == "silicate_records"
                g(silicate_records=True)
                print("silicate_records")
            """), [(2, "option", "f"), (3, "option", "f"), (4, "option", "f"), (5, "option", "f"), (6, "option", "f"),
                   (7, "option", "f")])

    def test_record_key(self):
        self.assertEqual(kinds("""
            class R:
                def load(self, rec):
                    return rec["d2_read"], rec.get("d2_read_basis"), rec.get("d2_store", {}), rec["d2_reads"]
            """), [(4, "record_key", "R.load")])

    def test_view_through_aliases_and_inside_material_assemblage(self):
        self.assertEqual(kinds("""
            import solver.material_assemblage as m
            from solver import material_assemblage
            from solver.material_assemblage import view as v, AssemblageView
            m.view(r, t, 1.0)
            material_assemblage.view(r, t, 1.0)
            v(r, t, 1.0)
            AssemblageView(r)
            other.view(r)
            """), [(5, "view", "<module>"), (6, "view", "<module>"), (7, "view", "<module>"), (8, "view", "<module>")])
        self.assertEqual(kinds("def g():\n    return view(r, t, 1.0)\n", path=c.MA_PATH), [(2, "view", "g")])
        self.assertEqual(kinds("def g():\n    return view(r, t, 1.0)\n"), [])

    def test_solid_boundaries_table_regardless(self):
        self.assertEqual(kinds("""
            def h(v, table):
                v._solid(1, 2)
                v.s_path(1, 2)
                _solid(1)
                rows = table["boundaries"]["rows"]
                b = table.get("boundaries")
                d = {"boundaries": []}
                v2 = make(table, table_regardless="reread")
                raise E("x", check="boundaries")
            """), [(3, "solid", "h"), (4, "solid", "h"), (6, "boundaries", "h"), (7, "boundaries", "h"),
                   (9, "table_regardless", "h")])


    def test_switch_with_its_use(self):
        got = c.sites_of("solver/x.py", textwrap.dedent("""
            from solver import material_assemblage as ma
            from solver.material_assemblage import boundary_block as bb
            def r(rec, t, s, u):
                ma.boundary_block(rec, t, s, "position")
                bb(rec, t, s, use="read")
                ma.boundary_block(rec, t, s, u)
                ma.boundary_block(rec, t, s)
                other.boundary_block(rec, t, s, "read")
            """))
        self.assertEqual(sorted((ln, k, u) for _, ln, k, _, u in got),
                         [(5, "switch", "position"), (6, "switch", "read"), (7, "switch", None), (8, "switch", None)])
        inside = c.sites_of(c.MA_PATH, "def f(r, t):\n    return boundary_block(r, t, None, 'read')\n")
        self.assertEqual(inside, {(c.MA_PATH, 2, "switch", "f", "read")})
        self.assertEqual({u for *_, u in c.sites_of("solver/x.py", "x = t['boundaries']\n")}, {None})


class Rules(unittest.TestCase):
    def test_each_kind_is_held_to_its_allow_list(self):
        site = lambda kind, fn, use=None: {"path": c.MA_PATH, "line": 1, "kind": kind, "function": fn, "use": use}  # noqa: E731
        data = {"sites": [site("boundaries", "boundary_block"), site("boundaries", "check_table"),
                          site("table_regardless", "x"), site("solid", "anything"), site("option", "anything"),
                          site("switch", "fall", "position"), site("switch", "fall", "read"),
                          site("switch", "fall", None), site("switch", "unlisted", "read")]}
        got = [(s["kind"], s["function"], s["use"]) for _, s in
               c.violations(data, switch_uses={(c.MA_PATH, "fall"): {"position"}})]
        self.assertEqual(got, [("boundaries", "check_table", None), ("table_regardless", "x", None),
                               ("switch", "fall", "read"), ("switch", "fall", None), ("switch", "unlisted", "read")])


class Tree(unittest.TestCase):
    """the real tree, and plants in a temp copy of it"""

    @classmethod
    def setUpClass(cls):
        cls.data = c.census(ROOT)
        cls.base = {(t, json.dumps(s, sort_keys=True)) for t, s in c.violations(cls.data)}

    def test_regenerated_equals_committed(self):
        committed = json.loads((ROOT / c.OUT).read_text(encoding="utf-8"))
        self.assertEqual(c.diff(committed, self.data), [], "regenerate with: python -B -m solver.landing.d2_read_census write")
        self.assertEqual(list(committed), list(c.TOP_KEYS))
        self.assertEqual([list(s) for s in committed["sites"]], [list(c.SITE_KEYS)] * len(committed["sites"]))
        self.assertEqual({s["use"] for s in committed["sites"] if s["kind"] != "switch"} - {None}, set())

    @unittest.expectedFailure
    def test_each_kind_holds_its_rule_on_the_real_tree(self):
        """§7: every site obeys its kind's rule. Red until the read piece routes its readers and fills the allow-lists;
        c8 drops the marker at the final pass (an unexpected success fails the run, so the marker cannot be forgotten)"""
        self.assertEqual(c.violations(self.data), [])

    def test_the_unrouted_sites_are_exactly_the_named_finding(self):
        got = {(s["kind"], s["path"], s["function"]) for _, s in c.violations(self.data)}
        self.assertEqual(sorted(got - c.UNROUTED_KNOWN), [], "a new site outside its kind's rule")
        self.assertEqual(sorted(c.UNROUTED_KNOWN - got), [], "routed: remove it from UNROUTED_KNOWN (the list only shrinks)")

    def test_the_allow_lists_are_immutable(self):
        """phase1-design §A6 (68 B1 on e59a6739): no mutable module state"""
        self.assertIsInstance(c.SWITCH_USES, type(__import__("types").MappingProxyType({})))
        for allow in (c.BOUNDARIES_ALLOW, c.RECORD_KEY_ALLOW, c.VIEW_ALLOW, c.TABLE_REGARDLESS_ALLOW, c.UNROUTED_KNOWN):
            self.assertIsInstance(allow, frozenset)

    def test_schema_keys_are_the_record_keys(self):
        import yaml
        rec = yaml.safe_load((ROOT / c.SCHEMA).read_text(encoding="utf-8"))["record"]
        self.assertEqual(self.data["schema_keys"], sorted(rec))
        self.assertIn("requires_switch", self.data["schema_keys"])

    def test_the_tools_own_test_and_solver_tests_are_not_walked(self):
        paths = {s["path"] for s in self.data["sites"]}
        self.assertFalse([p for p in paths if p.startswith("solver/tests/") or p == c.OWN_TEST])

    def _plant(self, body, rel="solver/planted_reader.py"):
        with TempCopy() as root:
            (root / rel).write_text(textwrap.dedent(body), encoding="utf-8")
            git(root, "add", "--", rel)
            rc, out = check(root)
            data = c.census(root)
        new = {(t, json.dumps(s, sort_keys=True)) for t, s in c.violations(data)} - self.base
        return rc, out, sorted(new)

    def test_control_a_raw_boundaries_read_fails_the_boundaries_rule(self):
        rc, out, new = self._plant('def read_rows(table):\n    return table["boundaries"]["rows"]\n')
        self.assertEqual(rc, 1)
        self.assertEqual(len(new), 1, new)
        text, site = new[0][0], json.loads(new[0][1])
        self.assertIn("boundaries read outside boundary_block", text)
        self.assertEqual((site["path"], site["line"], site["function"]), ("solver/planted_reader.py", 2, "read_rows"))
        self.assertIn("+ sites: ", out)
        self.assertIn("solver/planted_reader.py:2 read_rows", out)

    def test_control_a_table_regardless_site_fails_the_5a_rule(self):
        rc, out, new = self._plant("def reread(ma, r, t):\n    return ma.view(r, t, 1.0, table_regardless='x')\n")
        self.assertEqual(rc, 1)
        self.assertEqual([json.loads(s)["kind"] for _, s in new], ["table_regardless"])
        self.assertIn("table_regardless= site outside the mode's own tests", out)

    def test_control_a_switch_call_with_a_non_literal_use_fails(self):
        rc, out, new = self._plant("from solver import material_assemblage as ma\n"
                                   "def reader(r, t, s, u):\n    return ma.boundary_block(r, t, s, u)\n")
        self.assertEqual(rc, 1)
        self.assertEqual([(json.loads(x)["kind"], json.loads(x)["use"]) for _, x in new], [("switch", None)])
        self.assertIn("solver/planted_reader.py:3 reader use=None", out)

    def test_an_untracked_file_is_not_walked(self):
        with TempCopy() as root:
            (root / "solver/untracked_reader.py").write_text('x = t["boundaries"]\n', encoding="utf-8")
            self.assertNotIn("solver/untracked_reader.py", {s["path"] for s in c.census(root)["sites"]})

    def test_a_site_removed_without_regenerating_fails_with_the_diff(self):
        gone = next(s for s in self.data["sites"] if s["kind"] == "view")
        with TempCopy() as root:
            p = root / gone["path"]
            lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
            lines[gone["line"] - 1] = lines[gone["line"] - 1].replace("view(", "view_renamed_by_plant(", 1) \
                .replace("AssemblageView(", "Renamed(", 1)
            p.write_text("".join(lines), encoding="utf-8")
            rc, out = check(root)
        self.assertEqual(rc, 1)
        self.assertIn("- sites: " + json.dumps(gone, sort_keys=True), out)

    def test_the_real_tree_is_untouched_by_the_plants(self):
        self.assertFalse((ROOT / "solver/planted_reader.py").exists())


if __name__ == "__main__":
    unittest.main()
