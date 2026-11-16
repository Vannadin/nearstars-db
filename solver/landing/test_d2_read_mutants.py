# D2 읽기 변형 시험 실행기의 시험 — 행이 §10 목록을 빠짐없이 덮는지, 채운 앵커가 트리에 한 번씩 있는지, 합성 트리에서 잡힘·못 잡힘·STOP·대기를 가르는지
"""Tests of solver/landing/d2_read_mutants.py (D2-read rev 7 §10). The runner itself, with all its mutants, is run
per slice by the read piece (it takes minutes); here: the rows against §10's list, the anchors against the tree, and
the runner's verdicts on a synthetic tree."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from solver.landing import d2_read_mutants as dm

ROOT = Path(__file__).resolve().parents[2]

# §10's items, quoted (prereg-d2-engine-read.md blob 27bea44c, l.870–893); the writer side's two by their lead clause
SECTION_10 = (
    "precedence reordered (`d2` before `fallback`);",
    "a `fallback` cell read as `d2`;",
    "a chain link removed (one per link);",
    "the closed-key check removed;",
    "the lower-cell tie switched to upper;",
    "the subgrid side 1 not reversed;",
    "s_path on subgrid taking the blend's own derivative;",
    "d2_read off opening the store;",
    "global off × eligible routed to D2;",
    "the table-regardless mode on by default, or ignored by the dispatch, or with its note dropped;",
    "a `boundaries` reader left on the table's block (fall_sets' extension rows in particular);",
    "a v1 store accepted for positions;",
    "a «today» row through a `d2` cell accepted;",
    "a swap taking a traced P_b;",
    "`material.d2_store_coincident` removed: a fixture store whose coincident group took two different points must be "
    "refused (rev 5);",
    "`material.d2_store_edges_rows` loosened to compare `p_b` only: a fixture store with a changed `delta_rho` must be "
    "refused;",
    "the «traced» interval made inclusive: a fixture store with a traced p_b equal to p_lo must be refused.",
    "rule 5/6 taking the first point in file order instead of the nearest",
    "rule 4 removed must fail a fixture coincident group with each edge covered by its own point.",
)

# D2-read post-freeze note 11's mutants of the old walk geometry, quoted (its «Mutants» list)
NOTE_11 = (
    "note 11: the (b′) stubs past interior run ends left out of the walk (the old walk extended only at true ends);",
    "note 11: the row steps left out of the walk;",
    "note 11: a run read across extended past its ends (the old walk's over-reach at a true end held by a run read "
    "across);",
)


class Rows(unittest.TestCase):
    def test_the_rows_cover_section_10_and_nothing_else(self):
        items = [m[2] for m in dm.MUTANTS]
        self.assertEqual(set(items), set(SECTION_10) | set(NOTE_11))
        self.assertEqual(len({m[0] for m in dm.MUTANTS}), len(dm.MUTANTS))
        self.assertEqual(len([m for m in dm.MUTANTS if m[2] == SECTION_10[2]]), 6)   # one per §3 link
        self.assertEqual(len([m for m in dm.MUTANTS if m[2] == SECTION_10[9]]), 3)   # default, ignored, note dropped

    def test_each_filled_anchor_occurs_once_in_the_tree_and_names_its_tests(self):
        for mid, _s, _i, edits, modules in dm.MUTANTS:
            self.assertEqual(bool(edits), bool(modules), mid)
            for f, a, b in edits:
                self.assertEqual((ROOT / f).read_text(encoding="utf-8").count(a), 1, f"{mid}: {f}")
                self.assertNotEqual(a, b, mid)


MOD = "def f():\n    return 1  # one\n"
TEST = "import unittest\nfrom solver import mod\n\nclass T(unittest.TestCase):\n" \
       "    def test_f_is_one(self):\n        self.assertEqual(mod.f(), 1)\n"


class Runner(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="d2-mut-test-")
        self.root = Path(self.tmp.name)
        (self.root / "solver").mkdir()
        (self.root / "solver/__init__.py").write_text("")
        (self.root / "solver/mod.py").write_text(MOD)
        (self.root / "solver/test_mod.py").write_text(TEST)
        subprocess.run(["git", "-C", str(self.root), "init", "-q"], check=True)
        subprocess.run(["git", "-C", str(self.root), "add", "--", "solver"], check=True)

    def tearDown(self):
        self.tmp.cleanup()

    def run_with(self, mutants, argv=()):
        lines = []
        rc = dm.main(list(argv), root=self.root, mutants=mutants, out=lines.append)
        return rc, lines

    CAUGHT = ("X1", "S0", "returns two", [("solver/mod.py", "return 1", "return 2")], ["solver.test_mod"])
    MISSED = ("X2", "S0", "comment only", [("solver/mod.py", "# one", "# uno")], ["solver.test_mod"])
    PENDING = ("X3", "S2", "later", [], [])

    def test_caught_and_pending_pass_naming_the_test(self):
        rc, lines = self.run_with((self.CAUGHT, self.PENDING))
        self.assertEqual(rc, 0, lines)
        self.assertIn("baseline solver.test_mod: green", lines)
        self.assertIn("X1 (S0): rc 1 · caught by test_f_is_one — returns two", lines)
        self.assertIn("X3 pending (S2): later", lines)
        self.assertEqual(lines[-1], "d2-read mutants: 1 caught, 0 caught by nothing, 1 pending — PASS")

    def test_a_mutant_caught_by_nothing_fails(self):
        rc, lines = self.run_with((self.CAUGHT, self.MISSED))
        self.assertEqual(rc, 1, lines)
        self.assertIn("X2 (S0): rc 0 · caught by NOTHING — comment only", lines)

    def test_each_mutant_starts_from_the_restored_copy(self):
        twice = ("X4", "S0", "same anchor again", [("solver/mod.py", "return 1", "return 3")], ["solver.test_mod"])
        rc, lines = self.run_with((self.CAUGHT, twice))
        self.assertEqual(rc, 0, lines)
        self.assertEqual((self.root / "solver/mod.py").read_text(), MOD)     # the real tree is never written

    def test_a_test_red_at_baseline_never_counts_as_catching(self):
        (self.root / "solver/test_mod.py").write_text(TEST + "\n    def test_always_red(self):\n        self.fail('base')\n")
        subprocess.run(["git", "-C", str(self.root), "add", "--", "solver"], check=True)
        rc, lines = self.run_with((self.CAUGHT, self.MISSED))
        self.assertEqual(rc, 1, lines)
        self.assertIn("baseline solver.test_mod: red test_always_red", lines)
        self.assertIn("X1 (S0): rc 1 · caught by test_f_is_one — returns two", lines)
        self.assertIn("X2 (S0): rc 1 · caught by NOTHING — comment only", lines)

    def test_a_wrapper_launches_every_run_and_sees_the_source_objects(self):
        """c8 11-16: under a named double the baseline is green, so the mutant counts as caught; the double reads a
        blob of the source commit through the copy's borrowed objects"""
        (self.root / "solver/mod.py").write_text(MOD + "def pin():\n    return 'stale'\n")
        (self.root / "solver/test_mod.py").write_text(TEST + "\n    def test_pin(self):\n        self.assertEqual(mod.pin(), 'base')\n")
        subprocess.run(["git", "-C", str(self.root), "add", "--", "solver"], check=True)
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "base"],
                       check=True)
        sha = subprocess.run(["git", "-C", str(self.root), "rev-parse", "HEAD"], capture_output=True, text=True,
                             check=True).stdout.strip()
        wrapper = self.root.parent / f"{self.root.name}-double.py"
        wrapper.write_text("import subprocess, sys, unittest\nsys.path.insert(0, '.')\nfrom solver import mod\n"
                           f"b = subprocess.run(['git', 'rev-parse', '{sha}:solver/mod.py'], capture_output=True, "
                           "text=True).stdout.strip()\n"
                           "mod.pin = (lambda: 'base') if len(b) == 40 else mod.pin\n"
                           "unittest.main(module=None, argv=['unittest'] + sys.argv[1:])\n")
        try:
            rc, lines = self.run_with((self.CAUGHT,))
            self.assertIn("baseline solver.test_mod: red test_pin", lines)
            rc, lines = self.run_with((self.CAUGHT,), ["--python-wrapper", str(wrapper)])
            self.assertEqual(rc, 0, lines)
            self.assertTrue(lines[0].startswith(f"launcher: python -B {wrapper.resolve()} (blob "), lines)
            self.assertIn("baseline solver.test_mod: green", lines)
            self.assertIn("X1 (S0): rc 1 · caught by test_f_is_one — returns two", lines)
            self.assertEqual(self.run_with((self.CAUGHT,), ["--python-wrapper", str(wrapper) + ".absent"])[0], 2)
        finally:
            wrapper.unlink()

    def test_a_class_fixture_red_at_baseline_stops(self):
        (self.root / "solver/test_mod.py").write_text(TEST + "\n\nclass U(unittest.TestCase):\n    @classmethod\n"
                                                       "    def setUpClass(cls):\n        raise RuntimeError('pin')\n\n"
                                                       "    def test_masked(self):\n        pass\n")
        subprocess.run(["git", "-C", str(self.root), "add", "--", "solver"], check=True)
        rc, lines = self.run_with((self.CAUGHT,))
        self.assertEqual(rc, 2, lines)
        self.assertEqual(lines[-1], "STOP: baseline solver.test_mod: setUpClass red, which masks every test under it")

    def test_a_mutant_caught_only_by_a_fixture_fails(self):
        (self.root / "solver/test_mod.py").write_text(TEST + "\n\nclass U(unittest.TestCase):\n    @classmethod\n"
                                                       "    def setUpClass(cls):\n        assert mod.f() is not None\n\n"
                                                       "    def test_u(self):\n        pass\n")
        subprocess.run(["git", "-C", str(self.root), "add", "--", "solver"], check=True)
        breaks = ("X6", "S0", "f raises", [("solver/mod.py", "return 1", "raise RuntimeError('x')")], ["solver.test_mod"])
        rc, lines = self.run_with((breaks,))                        # a named test with the fixture: caught by the name
        self.assertEqual(rc, 0, lines)
        self.assertIn("X6 (S0): rc 1 · caught by test_f_is_one — f raises", lines)
        fix_only = ("X7", "S0", "only the fixture", [("solver/mod.py", "return 1", "return None")], ["solver.test_mod.U"])
        rc, lines = self.run_with((fix_only,))
        self.assertEqual(rc, 1, lines)
        self.assertEqual([ln for ln in lines if ln.startswith("X7 ")][0].split(" · ", 1)[1],
                         "caught only by a fixture: setUpClass — only the fixture")   # rc 5: no test ran

    def test_an_anchor_not_found_once_stops(self):
        gone = ("X5", "S0", "no anchor", [("solver/mod.py", "return 9", "return 2")], ["solver.test_mod"])
        rc, lines = self.run_with((gone,))
        self.assertEqual(rc, 2)
        self.assertTrue(lines[-1].startswith("STOP: X5: anchor in solver/mod.py found 0 times"), lines)

    def test_an_unknown_id_stops_and_ids_select(self):
        self.assertEqual(self.run_with((self.CAUGHT,), ["X9"])[0], 2)
        rc, lines = self.run_with((self.CAUGHT, self.MISSED), ["X1"])
        self.assertEqual(rc, 0)
        self.assertFalse([ln for ln in lines if ln.startswith("X2")])


if __name__ == "__main__":
    unittest.main()
