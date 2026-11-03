# 파생 파일 관문 시험 — 조사(기본 거부)가 오늘 트리에서 통과하고, 해시 규칙·스탬프 대조·DAG·재스탬프 까닭·닫힘이 심은 대조군에서 제 결과를 내는지
"""python3 derived/test_derived.py   (prereg pc/sg-gate/prereg-sg-gate.frozen.md 1765b55c; the landing runs it as the
census step's companion). Planted controls run on strings and scratch dicts; nothing in the tree is changed."""
import json
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
        """N12b: NEARSTARS_ARTIFACTS unset → the entry's stamp cannot be read (red)."""
        with self.assertRaises(LookupError):
            ck.out_of_tree_blobs(["rewrite/phase2-records/gen_h2o.py"], art_env="")


if __name__ == "__main__":
    unittest.main()
