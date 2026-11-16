# D2 «추가된 곡선» 재계수 시험 — 합성 저장 파일·edges 로 zone_added 규칙(같은 T·같은 칸·같은 상이면 쓰임, p_dataset 위는 셈 밖, swap 행 제외, P_b 없는 edge 는 행의 P_b)과 match 기록 대조를 봄
"""python -B -m unittest solver.tests.test_d2_added_recount   (gate Python, engine root; no registry load)"""
import contextlib
import gzip
import io
import json
import tempfile
import unittest
from pathlib import Path

from solver.landing import d2_added_recount as ar

PS = [1.0e9, 2.0e9, 3.0e9, 4.0e9]


def store(rows, pd=3.0e9):
    return {"grid": {"ps": PS, "ts": [1000.0, 1100.0]}, "header": {"p_dataset": pd}, "edges": {"rows": rows}}


def edge_row(t, p_b, phase, cls="edge_in", own_pb=True, match=None):
    e = {"phase": phase, "match": match or {"kind": "none"}}
    if own_pb:
        e["p_b"] = p_b
    return {"class": cls, "t": t, "p_b": p_b, "edges": [e]}


def acc(t, p, x, x_base=None):
    return {"direction": "P", "accepted": True, "p": p, "x": x, "x_base": x_base or x, "line": {"t": t}}


def um(t, p, a, b):
    return {"direction": "P", "t": t, "p": p, "a_parts": a, "b_parts": b}


class Rule(unittest.TestCase):
    def test_same_t_same_column_same_phase_is_used(self):
        doc = store([edge_row(1000.0, 1.5e9, "gt")])
        ed = {"edges": [acc(1000.0, 1.4e9, "gt")], "unmatched": [um(1000.0, 1.6e9, ["gt2", "ol"], ["ol"])]}
        r = ar.recount(doc, ed)
        self.assertEqual(r["added"], {"accepted": 0, "unmatched": 0})          # «gt2» → base «gt»

    def test_another_phase_t_or_column_is_added(self):
        doc = store([edge_row(1000.0, 1.5e9, "gt")])
        ed = {"edges": [acc(1000.0, 1.4e9, "ol"), acc(1100.0, 1.4e9, "gt"), acc(1000.0, 2.4e9, "gt")], "unmatched": []}
        self.assertEqual(ar.recount(doc, ed)["added"], {"accepted": 3, "unmatched": 0})

    def test_above_p_dataset_is_out_of_the_count_and_a_row_there_uses_nothing(self):
        doc = store([edge_row(1000.0, 3.5e9, "gt")])
        ed = {"edges": [acc(1000.0, 3.4e9, "gt"), acc(1000.0, 2.5e9, "gt")], "unmatched": []}
        r = ar.recount(doc, ed)
        self.assertEqual(r["points_in_region"]["accepted"], 1)
        self.assertEqual(r["added"]["accepted"], 1)

    def test_swap_rows_use_nothing(self):
        doc = store([edge_row(1000.0, 1.5e9, "gt", cls="swap_two_edges")])
        ed = {"edges": [acc(1000.0, 1.4e9, "gt")], "unmatched": []}
        self.assertEqual(ar.recount(doc, ed)["added"]["accepted"], 1)

    def test_an_edge_without_its_own_p_b_takes_the_rows(self):
        doc = store([edge_row(1000.0, 1.5e9, "gt", own_pb=False)])
        ed = {"edges": [acc(1000.0, 1.4e9, "gt")], "unmatched": []}
        self.assertEqual(ar.recount(doc, ed)["added"]["accepted"], 0)

    def test_t_direction_and_unaccepted_points_are_not_points(self):
        doc = store([])
        ed = {"edges": [{**acc(1000.0, 1.4e9, "gt"), "direction": "T"}, {**acc(1000.0, 1.4e9, "gt"), "accepted": False}],
              "unmatched": [{**um(1000.0, 1.6e9, ["gt"], []), "direction": "T"}]}
        self.assertEqual(ar.recount(doc, ed)["points_in_region"], {"accepted": 0, "unmatched": 0})

    def test_the_cross_check_names_what_the_match_record_and_the_rule_disagree_on(self):
        m = {"kind": "accepted", "record": {"list": "edges", "index": 1}}
        doc = store([edge_row(1000.0, 1.5e9, "gt", match=m)])
        ed = {"edges": [acc(1000.0, 1.4e9, "gt"), acc(1100.0, 2.5e9, "ol")], "unmatched": []}
        x = ar.recount(doc, ed)["cross_check_by_match_record"]
        self.assertEqual((x["used_by_the_rule_but_named_by_no_row"], x["named_by_a_row_but_not_used_by_the_rule"]),
                         (1, [["accepted", 1]]))

    def test_the_cli_writes_both_shas_and_the_forecast(self):
        doc = store([edge_row(1000.0, 1.5e9, "gt")])
        ed = {"edges": [acc(1000.0, 1.4e9, "gt")], "unmatched": []}
        with tempfile.TemporaryDirectory() as t, contextlib.redirect_stdout(io.StringIO()):
            t = Path(t)
            (t / "s.json.gz").write_bytes(gzip.compress(json.dumps(doc).encode(), mtime=0))
            (t / "e.json").write_text(json.dumps(ed))
            rc = ar.main(["--out", str(t / "o.json"), f"default_bse={t / 's.json.gz'},{t / 'e.json'}"])
            out = json.loads((t / "o.json").read_text())["records"]["default_bse"]
        self.assertEqual(rc, 0)
        self.assertEqual(out["forecast_upper_bound"], {"accepted": 20, "unmatched": 501})
        self.assertEqual(len(out["store_sha256"]) + len(out["edges_sha256"]), 128)

    def test_a_bad_input_stops(self):
        with contextlib.redirect_stdout(io.StringIO()) as o:
            rc = ar.main(["--out", "/dev/null", "khan=/nonexistent.json.gz,/nonexistent.json"])
        self.assertEqual(rc, 2)
        self.assertIn("STOP", o.getvalue())


if __name__ == "__main__":
    unittest.main()
