# D2 읽기 §9 항목 1 대조 시험 — 기준 읽기기(고정 blob)·계약 시험 고정 저장 파일(sha256 고정)로 대조 도구가 같은 답은 통과·심은 차이는 잡는지 보고, 엔진 read_point 가 기준과 비트까지 같은지 봄(S2 전에는 기대된 실패)
"""python -B -m unittest solver.tests.test_d2_read_reference   (gate Python, engine root)

D2-read rev 7 §9 item 1 and the deferred corners/centre check (map rows c8-12, c8-14). Inputs, pinned here:
- the reference reader, vendored from artifacts rewrite/phase2-records/bmcpp/d2_store_reader.py at blob 59b2f27e (the g_solved amendment, artifacts ea-gsolved-reader 282a4f871);
- the contract test's fixture stores, written by artifacts gen_d2read_fixtures.py (manifest.json names its blob, the
  contract test's and the reader's), each pinned by sha256.
The engine's own comparison (`test_engine_read_equals_the_reference`) is an expected failure while read_point is S0's
stub; S2 removes the decorator, and an unexpected success fails the run until it does."""
import copy
import hashlib
import json
import math
import unittest
from pathlib import Path

from solver import d2_store as ds
from solver.landing import d2_read_compare as dc

FIX = Path(__file__).resolve().parent / "fixtures" / "d2_reference"
READER = FIX / "d2_store_reader.py"
STORES = FIX / "stores"
READER_BLOB = "59b2f27e7d11178f1fbd90eb116370925f2bc054"
SHA256 = {                                    # gen_d2read_fixtures.py's output, as committed
    "d2": "d398b8c61b3e2107", "d2_fieldless": "f825de28807ec5b4", "fallback": "874f52f54539ded1",
    "cut": "c0074fc059cecff2", "cut_a_virtual": "2f4ab0006ab7eb89", "subgrid": "84f48ac867abc1ab",
    "subgrid_reversed": "0207bc03c40be944", "subgrid_c_fallback": "a821b417ecbc2d75", "limit": "310b6114cff4fdae",
    "grid136": "508b5198a63acbed"}


def git_blob(path):
    b = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


class Inputs(unittest.TestCase):
    def test_the_reader_is_the_pinned_blob(self):
        self.assertEqual(git_blob(READER), READER_BLOB)

    def test_every_store_is_its_pinned_bytes_and_the_manifest_agrees(self):
        man = json.loads((STORES / "manifest.json").read_text())
        self.assertEqual(man["reference_reader_blob"], READER_BLOB)
        self.assertEqual(sorted(man["stores"]), sorted(SHA256))
        for name, pre in SHA256.items():
            sha = hashlib.sha256((STORES / f"{name}.json.gz").read_bytes()).hexdigest()
            self.assertEqual((sha[:16], sha), (pre, man["stores"][name]["sha256"]), name)

    def test_the_fixtures_reach_every_d2_answer_class(self):
        ref = dc.load_reference(READER)
        seen = set()
        for name in SHA256:
            raw = (STORES / f"{name}.json.gz").read_bytes()
            r = dc.compare_store(raw, ref, ref.read, item1=True)        # the reference against itself
            seen.update(r["by_read"])
        self.assertEqual(seen, {"table", "d2", "cut", "subgrid"})

    def test_every_store_class_is_present_limit_included(self):
        classes = set()
        for name in SHA256:
            classes.update(json.loads((STORES / "manifest.json").read_text())["stores"][name]["classes"])
        self.assertEqual(classes, {"d2", "cut", "subgrid", "fallback", "limit"})
        ref = dc.load_reference(READER)
        doc = ref.load((STORES / "limit.json.gz").read_bytes())
        self.assertEqual(ref.read(doc, 1.5e9, 1350.0), {"read": "table", "why": "limit"})     # cell (0, 0)


    def test_item1_cases_are_all_reached_by_the_fixtures(self):
        """68 B1 on 270edf72: every registered case of §9 item 1 has a reference answer somewhere in the fixtures"""
        ref = dc.load_reference(READER)
        cover = set()
        for name in SHA256:
            cover.update(dc.compare_store((STORES / f"{name}.json.gz").read_bytes(), ref, ref.read, item1=True)["covered"])
        self.assertEqual([c for c in dc.ITEM1_CASES if c not in cover], [])
        man = json.loads((STORES / "manifest.json").read_text())
        self.assertEqual([n for n in dc.ITEM1_STORES if n not in man["stores"]], [])   # 68 n1

    def test_cut_both_sides_needs_both_fields_answered(self):
        import gzip
        ref = dc.load_reference(READER)
        raw = (STORES / "cut.json.gz").read_bytes()
        self.assertIn("cut both sides", dc.compare_store(raw, ref, ref.read, item1=True)["covered"])
        doc = json.loads(gzip.decompress(raw))
        cell = next(c for c in doc["cells"].values() if c["class"] == "cut")
        cell["cut"]["b"] = cell["cut"]["a"]                    # one field on both sides: B's side is never a second field
        raw2 = gzip.compress(json.dumps(doc).encode(), mtime=0)
        self.assertNotIn("cut both sides", dc.compare_store(raw2, ref, ref.read, item1=True)["covered"])

    def test_the_cli_names_a_case_no_store_reaches(self):
        import contextlib
        import io
        import tempfile
        with tempfile.TemporaryDirectory() as t, contextlib.redirect_stdout(io.StringIO()) as o:
            rc = dc.main(["--item1", "--reference", str(READER), "--out", str(Path(t) / "o.json"),
                          str(STORES / "d2.json.gz")])
            out = json.loads((Path(t) / "o.json").read_text())
        self.assertEqual(rc, 2)
        self.assertIn("point p136", out["item1_missing"])
        self.assertIn("why limit", out["item1_missing"])
        self.assertIn("§9 item 1's cases with no reference answer", o.getvalue())

class Driver(unittest.TestCase):
    """the comparison itself: identical answers pass, every planted difference is found"""
    def setUp(self):
        self.ref = dc.load_reference(READER)

    def run_with(self, name, engine):
        return dc.compare_store((STORES / f"{name}.json.gz").read_bytes(), self.ref, engine, item1=True)

    def test_the_reference_against_itself_agrees_everywhere(self):
        for name in SHA256:
            r = self.run_with(name, lambda d, p, t: {**self.ref.read(d, p, t), "notes": (("X", "ignored"),)})
            self.assertEqual(r["n_differences"], 0, (name, r["differences"][:3]))
            self.assertEqual(r["points"] - sum(r["by_read"].values()), 0)

    def test_corners_and_centre_count_five_per_cell(self):
        doc = self.ref.load((STORES / "d2.json.gz").read_bytes())
        self.assertEqual(len(list(dc.cell_points(doc))), 5 * len(doc["cells"]))

    def planted(self, name, edit):
        def eng(d, p, t):
            a = copy.deepcopy(self.ref.read(d, p, t))
            edit(a)
            return a
        return self.run_with(name, eng)

    def test_one_ulp_in_one_value_is_a_difference(self):
        def e(a):
            if a["read"] != "table":
                a["values"]["rho"] = math.nextafter(a["values"]["rho"], math.inf)
        r = self.planted("d2", e)
        self.assertGreater(r["n_differences"], 0)
        self.assertIn("values.rho", r["differences"][0]["why"][0])

    def test_a_nan_with_other_bits_and_a_signed_zero_are_differences(self):
        self.assertFalse(dc.same_value(float("nan"), -float("nan")))
        self.assertTrue(dc.same_value(float("nan"), float("nan")))
        self.assertFalse(dc.same_value(0.0, -0.0))

    def test_a_class_a_field_a_why_and_a_key_are_differences(self):
        for name, edit, word in (
                ("cut", lambda a: a.update(read="d2") if a["read"] == "cut" else None, "read:"),
                ("cut_a_virtual", lambda a: a.update(field="z") if a["read"] == "cut" else None, "field:"),
                ("fallback", lambda a: a.update(why="limit") if a.get("why") == "fallback" else None, "why:"),
                ("subgrid", lambda a: a["values"].pop("alpha") if a["read"] == "subgrid" else None, "value keys"),
                ("d2", lambda a: a.update(extra=1), "keys:")):
            r = self.planted(name, edit)
            self.assertGreater(r["n_differences"], 0, name)
            self.assertTrue(any(word in w for d in r["differences"] for w in d["why"]), (name, r["differences"][:1]))

    def test_an_engine_raise_is_a_difference(self):
        def eng(d, p, t):
            raise NotImplementedError("S2")
        r = self.run_with("d2", eng)
        self.assertEqual(r["n_differences"], r["points"])

    def test_the_cli_stops_on_a_difference(self):
        import contextlib
        import io
        import tempfile
        import math
        from unittest import mock
        from solver import d2_store as ds
        real = ds.read_point

        def one_ulp_off(doc, p, t, view=None):                          # S2 (c8): a planted 1-ulp engine difference
            got = real(doc, p, t, view)
            if got["read"] != "table":
                got = {**got, "values": {**got["values"], "rho": math.nextafter(got["values"]["rho"], math.inf)}}
            return got
        with tempfile.TemporaryDirectory() as t, contextlib.redirect_stdout(io.StringIO()) as o, \
                mock.patch.object(ds, "read_point", one_ulp_off):
            rc = dc.main(["--reference", str(READER), "--out", str(Path(t) / "o.json"), str(STORES / "d2.json.gz")])
            out = json.loads((Path(t) / "o.json").read_text())
        self.assertEqual(rc, 2, o.getvalue())
        self.assertTrue(next(iter(out["stores"].values()))["differences"])


class EngineRead(unittest.TestCase):
    def test_engine_read_equals_the_reference(self):
        ref = dc.load_reference(READER)
        for name in SHA256:
            r = dc.compare_store((STORES / f"{name}.json.gz").read_bytes(), ref, ds.read_point, item1=True)
            self.assertEqual(r["n_differences"], 0, (name, r["differences"][:3]))


if __name__ == "__main__":
    unittest.main()
