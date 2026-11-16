# D2 읽기 §6 실행 시 셈 시험 — 고정 저장 파일들의 점(칸 꼭짓점·가운데·§9 항목 1 점)에서 엔진 read_point 가 세는 «마당 없음» 수가 기준 읽기기의 수와 같은지, 이름·줄 형식이 고정값인지; S3 의 나머지 셋은 기대된 실패
"""python -B -m unittest solver.tests.test_d2_read_counts   (gate Python, engine root; no registry load)

D2-read rev 7 §6 and §9 (map rows c8-12, c8-15). The counts are per view (`view.d2_counts`, keyed by
d2_store.COUNT_NAMES); read_point(doc, p, t, view) raises NO_FIELD on any view carrying `d2_counts`, so a namespace
stands for the view here (c8, e901a8ac). Expected values come from the reference reader on the same points (its
COUNTS[NO_FIELD]). The three other counts are S3's: the (S1) sliver count is expected to equal the reference's subgrid
answers, and stays an expected failure until S3 counts it; the swap and forced-side counts need curves and forced reads,
which the fixture stores do not carry, so here they must stay 0."""
import types
import unittest
from pathlib import Path

from solver import d2_store as ds
from solver.landing import d2_read_compare as dc

FIX = Path(__file__).resolve().parent / "fixtures" / "d2_reference"
READER = FIX / "d2_store_reader.py"
STORES = sorted((FIX / "stores").glob("*.json.gz"))
SWAP, S1, FORCED = ds.COUNT_NAMES[1], ds.COUNT_NAMES[2], ds.COUNT_NAMES[3]


def points(doc):
    return [(p, t) for _, _, p, t in list(dc.cell_points(doc)) + list(dc.item1_points(doc, 0, 4))]


def counted(raw, ref):
    """(reference counts, engine counts, reference answers by «read») over one store's points"""
    doc = ref.load(raw)
    ref.COUNTS[ref.NO_FIELD] = 0
    view = types.SimpleNamespace(d2_counts={n: 0 for n in ds.COUNT_NAMES})
    by = {}
    for p, t in points(doc):
        a = ref.read(doc, p, t)
        by[a["read"]] = by.get(a["read"], 0) + 1
        ds.read_point(doc, p, t, view)
    return dict(ref.COUNTS), view.d2_counts, by


class Names(unittest.TestCase):
    def test_the_names_and_the_line_are_the_frozen_ones(self):
        ref = dc.load_reference(READER)
        self.assertEqual(ds.NO_FIELD, ref.NO_FIELD)                        # §6 and the reference, verbatim
        self.assertEqual(ds.COUNT_NAMES[0], ds.NO_FIELD)
        self.assertEqual(ds.RUN_RECORD_LINE.format(name=ds.NO_FIELD, n=7, m=114),
                         "d2: no field at the point → table read: 7 of 114 reads")


class NoField(unittest.TestCase):
    def test_the_engine_counts_what_the_reference_counts_on_every_store(self):
        ref = dc.load_reference(READER)
        total = 0
        for s in STORES:
            rc, ec, _ = counted(s.read_bytes(), ref)
            self.assertEqual(ec[ds.NO_FIELD], rc[ref.NO_FIELD], s.name)
            total += rc[ref.NO_FIELD]
        self.assertGreater(total, 0)                                       # the fieldless store reaches the count

    def test_no_view_counts_nothing(self):
        ref = dc.load_reference(READER)
        raw = (FIX / "stores" / "d2_fieldless.json.gz").read_bytes()
        doc = ref.load(raw)
        for p, t in points(doc):
            ds.read_point(doc, p, t)                                       # view None: nothing to raise, no error

    def test_swap_and_forced_side_stay_0_without_curves_or_forced_reads(self):
        ref = dc.load_reference(READER)
        for s in STORES:
            _, ec, _ = counted(s.read_bytes(), ref)
            self.assertEqual((ec[SWAP], ec[FORCED]), (0, 0), s.name)


class S3(unittest.TestCase):
    @unittest.expectedFailure                                              # S3 counts (S1)'s sliver reads
    def test_the_sliver_count_equals_the_references_subgrid_answers(self):
        ref = dc.load_reference(READER)
        for name in ("subgrid", "subgrid_reversed"):
            _, ec, by = counted((FIX / "stores" / f"{name}.json.gz").read_bytes(), ref)
            self.assertGreater(by.get("subgrid", 0), 0)
            self.assertEqual(ec[S1], by["subgrid"], name)


if __name__ == "__main__":
    unittest.main()
