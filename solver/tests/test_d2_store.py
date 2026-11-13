# D2 저장소 적재 검사(d2_store.py) 시험 — 잠든 조각의 핀(모듈 blob·closure), coincident·_reach 재구현의 동등, 적재 거절의 이름, edges 블록 검사, ea 와 함께 쓰는 고정 입력의 (2b)·(S1) STOP 집합
"""The view piece's tests (D2-read rev 7 §2, §3, §5b; post-freeze note 2 (1) conditions 1–4 and (3)'s shared
fixtures). Run under the gate's Python from the engine root:  python -B -m unittest solver.tests.test_d2_store"""
import copy
import gzip
import hashlib
import json
import os
import subprocess
import tempfile
import types
import unittest
from pathlib import Path

from solver import d2_store as ds
from solver import fall_sets
from solver import material_assemblage as ma
from solver import material_registry as mr
from solver.from_v1 import thaw

ROOT = Path(__file__).resolve().parents[2]
RECORDS = ("silicate_slb_default_bse", "silicate_slb_earth_dmm_wh2005", "silicate_slb_mars_khan2022")
PINNED_BLOB = "a21205fa634a7d0910e257f051d2eb7108eb45fd"     # the tables' closure_terms.monotone pin (P1)
EXPECTED = Path(__file__).resolve().parent / "data" / "d2_store_shared_fixtures_expected.json"
_REG = None


def reg():
    global _REG
    if _REG is None:
        _REG = mr.load()
    return _REG


# ── note 2 (1) condition 1: no pinned module changed, and this module is outside the read closure ──────────────────
class Dormant(unittest.TestCase):
    def test_material_assemblage_is_the_blob_the_tables_pin(self):
        self.assertEqual(ma.module_blob(), PINNED_BLOB)
        for rid in RECORDS:
            mono = reg().tables[rid]["closure_terms"]["monotone"]
            self.assertEqual(mono["material_assemblage_blob"], PINNED_BLOB, rid)

    def test_a_one_byte_plant_moves_the_blob(self):
        data = Path(ma.__file__).read_bytes() + b" "
        planted = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
        self.assertNotEqual(planted, PINNED_BLOB)
        with tempfile.TemporaryDirectory() as d:          # module_blob reads its own file: the same rule on a copy
            f = Path(d) / "material_assemblage.py"
            f.write_bytes(data)
            out = subprocess.run(["git", "hash-object", str(f)], capture_output=True, text=True, check=True).stdout
            self.assertEqual(out.strip(), planted)

    def test_d2_store_is_not_in_the_read_closure(self):
        self.assertNotIn("d2_store", fall_sets.closure(ROOT))
        self.assertIn("material_assemblage", fall_sets.closure(ROOT))


# ── conditions 2 and 3: the coincident set and _reach, re-implemented, equal to init's ────────────────────────────
class EqualToInit(unittest.TestCase):
    def test_reach_equals_the_views_on_each_shipped_record(self):
        for rid in RECORDS:
            v = ma.view(thaw(reg().get(rid)), reg().tables[rid], 1600.0)
            got = ds.reach(v.ts)
            print(f"\n  _reach {rid}: d2_store {got!r} K, view {v._reach!r} K")
            self.assertEqual(got, v._reach, rid)

    def test_coincident_count_and_kinds_equal_inits_on_each_shipped_record(self):
        total = 0
        for rid in RECORDS:
            t = reg().tables[rid]
            v = ma.view(thaw(reg().get(rid)), t, 1600.0)
            runs = ma._cut_runs(ma.build_curves(thaw(t["boundaries"]), v.ts))
            n, ids = ds.coincident(runs)
            init_swaps = {(c.phase, tuple(r["t"] for r in c.rows), tuple(r["p_lo"] for r in c.rows))
                          for c in v._cut if c.kind == "swap"}
            mine = {(c.phase, tuple(r["t"] for r in c.rows), tuple(r["p_lo"] for r in c.rows))
                    for c in runs if c.kind == "swap" or c.id in ids}
            print(f"\n  coincident {rid}: d2_store {n} groups' edge runs, init {v.coincident}")
            self.assertEqual(n, v.coincident, rid)
            self.assertEqual(mine, init_swaps, rid)
            total += n
        self.assertGreaterEqual(total, 1)

    def _pair(self, rel):
        """two one-row cut edge runs over the same T whose P_b differ by `rel`, relative"""
        def run(cid, pb):
            c = ma._Curve(cid, "edge", f"x{cid}", [{"t": 1000.0, "p_b": pb, "p_lo": 1e9, "across": False}])
            return c
        return [run(0, 5e9), run(1, 5e9 * (1 + rel))]

    def test_the_tolerance_is_inits(self):
        self.assertEqual(ds.coincident(self._pair(5e-10))[0], 2)
        self.assertEqual(ds.coincident(self._pair(5e-9))[0], 0)      # a 1e-8 tolerance would merge these: the mutant

    def test_mutants_change_the_count(self):
        # tolerance 1e-9 → 1e-8, and the group key changed (T rows → T rows and kind): each must make the shipped
        # equality fail somewhere (here on planted runs that separate them)
        orig = ds.TOL_COINCIDENT
        try:
            ds.TOL_COINCIDENT = 1e-8
            self.assertNotEqual(ds.coincident(self._pair(5e-9))[0], 0)
        finally:
            ds.TOL_COINCIDENT = orig
        a, b = self._pair(0.0)
        b.kind = "swap"                                      # a swap run and an edge run at one P_b: init groups them
        self.assertEqual(ds.coincident([a, b])[0], 1)


# ── the shared fixtures with ea's writer (note 2 (3); ea-bmcpp-l eb7888474 test_d2_store_checks.py 100a9061) ─────
PS = [float(i) * 1e9 for i in range(1, 9)]
TS = [1000.0, 1100.0, 1200.0, 1300.0, 1400.0, 1500.0]
REACH = 200.0


class Curve:
    """A planted curve with ma._Curve's p_b_ext semantics: linear in T past an end within reach, None past a stopped
    end or beyond reach."""

    def __init__(self, cid, rows, kind="edge", phase="x", stop_lo=False, stop_hi=False):
        self.id, self.kind, self.phase, self.stop_lo, self.stop_hi = cid, kind, phase, stop_lo, stop_hi
        self.rows = [{"t": t, "p_b": p, "p_lo": lo, "p_hi": lo + 1e9, "left_label": "a+b", "right_label": "a+c"}
                     for t, p, lo in rows]
        self.t0, self.t1 = self.rows[0]["t"], self.rows[-1]["t"]

    def p_b_ext(self, t, reach):
        r = self.rows
        if self.t0 <= t <= self.t1:
            for a, b in zip(r, r[1:]):
                if a["t"] <= t <= b["t"]:
                    return a["p_b"] + (b["p_b"] - a["p_b"]) * (t - a["t"]) / (b["t"] - a["t"])
            return r[0]["p_b"]
        hi = t > self.t1
        if (self.stop_hi if hi else self.stop_lo) or (t - self.t1 if hi else self.t0 - t) > reach:
            return None
        a, b = (r[-2], r[-1]) if hi else (r[1], r[0])
        return b["p_b"] + (b["p_b"] - a["p_b"]) * (t - b["t"]) / (b["t"] - a["t"])


def _block(curves, source="today"):
    rows = []
    for c in curves:
        for r in c.rows:
            s = source(c, r) if callable(source) else source
            rows.append({"t": r["t"], "p_lo": r["p_lo"], "p_hi": r["p_hi"], "left": "a+b", "right": "a+c",
                         "class": "edge_in", "edges": [{"phase": c.phase, "p_b": r["p_b"], "p_b_source": s}]})
    return {"status": "exported", "rows": rows, "source": {}}


def _store(cells, curves, source="today"):
    return {"grid": {"ps": PS, "ts": TS}, "cells": {f"{j},{k}": v for (j, k), v in cells.items()},
            "edges": _block(curves, source)}


def _view(curves, ts=TS):
    return types.SimpleNamespace(ts=ts, _reach=REACH, _events=curves)


def _d2(*cells):
    return {c: {"class": "d2"} for c in cells}


def _subgrid_p(la, lb, k):
    t0, t1 = TS[k], TS[k + 1]
    return {"class": "subgrid", "direction": "P",
            "sides": [{"nodes": [[0, k]], "A": "a+b", "lines": [[la, t0], [lb, t0]]},
                      {"nodes": [[0, k + 1]], "A": "a+b", "lines": [[la, t1], [lb, t1]]}]}


def shared_fixtures():
    """name → (store, view): the planted inputs both sides run."""
    out = {}
    c = Curve(0, [(1000.0, 1.4e9, 1e9), (1100.0, 1.5e9, 1e9), (1200.0, 4.5e9, 4e9), (1300.0, 4.6e9, 4e9)],
              stop_lo=True, stop_hi=True)
    out["rev3_three_columns_between_two_rows"] = (_store(_d2((1, 1), (2, 1)), [c]), _view([c]))
    c = Curve(0, [(1100.0, 1.5e9, 1e9), (1200.0, 4.5e9, 4e9)], stop_lo=True, stop_hi=True)
    out["traced_through_d2"] = (_store(_d2((2, 1)), [c], source="traced"), _view([c]))
    c = Curve(0, [(1100.0, 1.5e9, 1e9), (1200.0, 4.5e9, 4e9)], stop_lo=True, stop_hi=True)
    out["one_today_end"] = (_store(_d2((2, 1)), [c], source=lambda cc, r: "today" if r["t"] == 1200.0 else "traced"),
                            _view([c]))
    c = Curve(0, [(1100.0, 1.5e9, 1e9), (1200.0, 2.5e9, 2e9)])
    out["extension_reach_crosses_d2"] = (_store(_d2((3, 3)), [c]), _view([c]))
    c = Curve(0, [(1100.0, 1.5e9, 1e9), (1200.0, 2.5e9, 2e9)], stop_hi=True)
    out["stopped_end_no_extension"] = (_store(_d2((3, 3)), [c]), _view([c]))
    for stopped in (True, False):
        a = Curve(0, [(1100.0, 2.4e9, 2e9), (1200.0, 2.5e9, 2e9)], kind="swap", phase="x", stop_lo=stopped, stop_hi=stopped)
        b = Curve(1, [(1100.0, 2.4e9, 2e9), (1200.0, 2.5e9, 2e9)], kind="swap", phase="y", stop_lo=stopped, stop_hi=stopped)
        name = "coincident_pair_split_next_to_d2" + ("" if stopped else "_bare_build_curves")
        out[name] = (_store(_d2((1, 1), (1, 3), (1, 0)), [a, b]), _view([a, b]))
    c = Curve(0, [(1100.0, 1.5e9, 1e9), (1200.0, 1.6e9, 1e9)], stop_lo=True, stop_hi=True)
    out["grid_mismatch"] = (_store({}, [c]), _view([c], ts=TS[:-1]))
    for name, pb in (("s1_inside", 3.5e9), ("s1_outside_over_p_tol", 3.8e9), ("s1_outside_within_p_tol", 3.6e9 + 5e4)):
        c = Curve(0, [(1100.0, pb, 3e9), (1200.0, pb, 3e9)], stop_lo=True, stop_hi=True)
        out[name] = (_store({(2, 1): _subgrid_p(3.4e9, 3.6e9, 1)}, [c]), _view([c]))
    return out


def stop_sets():
    """name → sorted [(refusal id, cell or reason)]: the engine side's decisions on the shared fixtures."""
    out = {}
    for name, (st, v) in shared_fixtures().items():
        got = ds.today_segments(st, v)
        out[name] = sorted([rid, text.split("cell ")[-1] if "cell (" in text else text] for rid, text in got["stops"])
    return out


class SharedFixtures(unittest.TestCase):
    def test_the_stop_sets(self):
        s = stop_sets()
        self.assertEqual(s["rev3_three_columns_between_two_rows"],
                         [["material.d2_store_today_row", "(1, 1)"], ["material.d2_store_today_row", "(2, 1)"]])
        self.assertEqual(s["traced_through_d2"], [])
        self.assertEqual(s["one_today_end"], [["material.d2_store_today_row", "(2, 1)"]])
        self.assertEqual(s["extension_reach_crosses_d2"], [["material.d2_store_today_row", "(3, 3)"]])
        self.assertEqual(s["stopped_end_no_extension"], [])
        self.assertEqual({x[1] for x in s["coincident_pair_split_next_to_d2"]}, {"(1, 1)"})
        self.assertIn("(1, 3)", {x[1] for x in s["coincident_pair_split_next_to_d2_bare_build_curves"]})
        self.assertEqual([x[0] for x in s["grid_mismatch"]], ["material.d2_store_grid"])
        self.assertEqual(s["s1_inside"], [])
        self.assertEqual([x[0] for x in s["s1_outside_over_p_tol"]], ["material.d2_store_sliver"])
        self.assertEqual(s["s1_outside_within_p_tol"], [])

    def test_the_committed_expected_sets_are_this_codes(self):
        """note 2 (3) (a): the engine side's STOP sets, committed as a file for the writer's side to compare against"""
        self.assertEqual(json.loads(EXPECTED.read_text(encoding="utf-8"))["stop_sets"], stop_sets())

    def test_inside_offsets_are_disclosed(self):
        st, v = shared_fixtures()["s1_inside"]
        s1 = ds.today_segments(st, v)["s1"]
        self.assertEqual(len(s1[0]["offsets"]), 5)
        self.assertAlmostEqual(s1[0]["offsets"][0][1], 1e8)

    def test_a_p_b_on_a_column_line_touches_both_cells(self):
        # engine-only (not yet a shared fixture): P_b on the line between columns 1 and 2 (3 GPa) touches cells 1 and 2
        c = Curve(0, [(1100.0, 3e9, 2e9), (1200.0, 3e9, 2e9)], stop_lo=True, stop_hi=True)
        got = ds.today_segments(_store(_d2((1, 1)), [c]), _view([c]))["stops"]
        self.assertEqual([t.split("cell ")[-1] for _i, t in got], ["(1, 1)"])
        self.assertEqual(ds._cells_through(PS, TS, (1100.0, 3e9), (1200.0, 3e9)), [(1, 1), (2, 1)])

    def test_p_tol_is_boundary_pass_own(self):
        self.assertEqual(ds.P_TOL, 1e5)


# ── §2 and §3: the loader's refusals by name ───────────────────────────────────────────────────────────────────────
def _synthetic_edges(boundaries):
    """A v2 edges block from a compact's block with every unit «today» (the rules' kinds without traced points)."""
    e = copy.deepcopy(boundaries)
    counts = {k: 0 for k in ds.MATCH_KINDS}

    def mark(u, kind):
        u["p_b_source"], u["p_b_today"], u["match"] = "today", u.get("p_b"), {"kind": kind}
        counts[kind] += 1
    for r in e.get("rows", ()):
        if r.get("node_resolved"):
            mark(r, "node")
            for x in r.get("edges") or ():
                mark(x, "node")
        elif r.get("class") == "swap":
            mark(r, "swap")
        else:
            for x in r.get("edges") or ():
                mark(x, "no_p_b" if x.get("p_b") is None else "none")
    for r in (e.get("extension") or {}).get("rows", ()):
        mark(r, "extension")
    e["source"] = {**(e.get("source") or {}), "compact_boundaries_sha256": "0" * 64, "edges_json_sha256": "1" * 64,
                   "match_rule": {"name": "test", "version": 1},
                   "counts": {**counts, "unmatched_over_0p1_cell": 0, "multi_candidate": 0, "coincident_created": 0}}
    return e


def _store_doc(compact, rid):
    ps, ts = ds.nodes(compact)
    return {"contract": {"name": ds.CONTRACT_NAME, "version": 2},
            "header": {"record_id": rid, "table_blob": compact["source"]["table_blob"], "builder_manifest_blob": "b" * 40,
                       "inputs": {"interp_term_blob": "4" * 40}},
            "grid": {"ps": ps, "ts": ts}, "fields": {}, "cells": {}, "counts": {},
            "edges": _synthetic_edges(compact["boundaries"])}


class Loader(unittest.TestCase):
    RID = "silicate_slb_mars_khan2022"

    def setUp(self):
        self.compact = thaw(reg().tables[self.RID])
        self.compact["interp_terms"]["source"]["file_blob"] = "4" * 40
        self.doc = _store_doc(self.compact, self.RID)
        self.dir = tempfile.TemporaryDirectory()
        (Path(self.dir.name) / "fields").mkdir()
        self.record = {"id": self.RID, "d2_read": "eligible", "d2_read_basis": {"report_blob": "r" * 40, "line": "x"},
                       "assemblage": {"pins": {"compact_sha256": "c" * 64,
                                               "builders": [{"role": "strict", "blob": "b" * 40}]}}}
        self.write()

    def tearDown(self):
        self.dir.cleanup()

    def write(self):
        raw = gzip.compress(json.dumps(self.doc).encode(), mtime=0)
        (Path(self.dir.name) / "fields" / f"{self.RID}.json.gz").write_bytes(raw)
        self.record["d2_store"] = {"path": f"fields/{self.RID}.json.gz", "sha256": hashlib.sha256(raw).hexdigest()}

    def load(self):
        return ds.load(self.record, self.compact, self.dir.name, compact_sha256="c" * 64)

    def refuses(self, rid):
        with self.assertRaises(ds.StoreRefusal) as cm:
            got = self.load()
            ds.check_edges(got, self.compact, thaw(reg().get(self.RID)) | {k: self.record[k] for k in ("id",)})
        self.assertEqual(cm.exception.id, rid, str(cm.exception))

    def test_a_good_store_loads(self):
        got = self.load()
        self.assertEqual(got.state, "eligible")

    def test_off_never_opens_the_store_and_absent_is_off(self):
        rec = {"id": self.RID}
        self.assertIsNone(ds.load(rec, self.compact, "/nonexistent"))
        self.assertIsNone(ds.load({**rec, "d2_read": "off"}, self.compact, "/nonexistent"))

    def test_s2_rows(self):
        self.record["d2_read"] = "maybe"
        self.refuses("material.d2_read_unknown")
        self.setUp()
        self.record["d2_read_basis"] = {"report_blob": "r" * 40}
        self.refuses("material.d2_read_basis")
        self.setUp()
        del self.record["d2_store"]
        self.refuses("material.d2_store_missing")
        self.setUp()
        self.record["d2_store"]["path"] = "../x.json.gz"
        self.refuses("material.d2_store_missing")
        self.setUp()
        self.record = {"id": self.RID, "d2_read": "off", "d2_store": self.record["d2_store"]}
        self.refuses("material.d2_store_missing")

    def test_contract_keys_class_grid(self):
        self.doc["contract"]["version"] = 1
        self.write()
        self.refuses("material.d2_store_contract")
        with self.assertRaises(ds.StoreRefusal) as cm:            # §2: v1 is refused once, by name
            self.load()
        self.assertIn("v1 has no edges block", str(cm.exception))
        self.setUp()
        self.doc["extra"] = 1
        self.write()
        self.refuses("material.d2_store_keys")
        self.setUp()
        self.doc["cells"]["0,0"] = {"class": "table"}
        self.write()
        self.refuses("material.d2_store_class")
        self.setUp()
        self.doc["grid"]["ts"] = self.doc["grid"]["ts"][1:]
        self.write()
        self.refuses("material.d2_store_grid")

    def test_interp_terms_source_stays_open(self):
        # note 3 (3), 68 n1: an unknown key in interp_terms.source loads through check_term_block and this loader
        self.compact["interp_terms"]["source"]["an_unknown_key"] = "x"
        ma.check_term_block(self.compact, "interp_terms", sparse=False)
        self.assertEqual(self.load().state, "eligible")

    def test_each_chain_link_planted_to_fail(self):
        plants = {"pins.compact_sha256": lambda: self.record["assemblage"]["pins"].update(compact_sha256="d" * 64),
                  "d2_store.sha256": lambda: self.record["d2_store"].update(sha256="e" * 64),
                  "builder_manifest_blob": lambda: self.doc["header"].update(builder_manifest_blob="f" * 40),
                  "record_id": lambda: self.doc["header"].update(record_id="other"),
                  "table_blob": lambda: self.doc["header"].update(table_blob="6" * 40),
                  "interp_term_blob": lambda: self.compact["interp_terms"]["source"].update(file_blob="7" * 40)}
        for link, plant in plants.items():
            with self.subTest(link=link):
                self.setUp()
                plant()
                if link != "d2_store.sha256":
                    sha = self.record["d2_store"]["sha256"]
                    self.write() if link in ("builder_manifest_blob", "record_id", "table_blob") else None
                    if link == "pins.compact_sha256":
                        self.record["d2_store"]["sha256"] = sha
                with self.assertRaises(ds.StoreRefusal) as cm:
                    self.load()
                self.assertEqual(cm.exception.id, "material.d2_store_chain")
                self.assertIn(f"link {link}:", str(cm.exception))


# ── §5b: the edges checks ─────────────────────────────────────────────────────────────────────────────────────────
class Edges(unittest.TestCase):
    RID = "silicate_slb_mars_khan2022"

    def setUp(self):
        self.compact = thaw(reg().tables[self.RID])
        self.b = self.compact["boundaries"]
        self.e = _synthetic_edges(self.b)
        self.ps, self.ts = ds.nodes(self.compact)

    def run_all(self):
        ds.check_edges_rows(self.e, self.b)
        ds.check_units(self.e, self.b)
        ds.check_extension_h6(self.e, self.compact)
        ds.check_coincident(self.e, self.b, self.ts)

    def refuses(self, rid):
        with self.assertRaises(ds.StoreRefusal) as cm:
            self.run_all()
        self.assertEqual(cm.exception.id, rid, str(cm.exception))

    def first_edge(self):
        for r in self.e["rows"]:
            if not r.get("node_resolved") and r["class"] != "swap" and r.get("edges") and r["edges"][0].get("p_b"):
                return r, r["edges"][0]

    def test_the_synthetic_block_passes(self):
        self.run_all()

    def test_a_changed_delta_rho_is_refused(self):          # §10: edges_rows loosened to p_b must fail this
        r, e = self.first_edge()
        e["delta_rho"] = (e.get("delta_rho") or 0.0) + 1e-3
        self.refuses("material.d2_store_edges_rows")

    def test_a_changed_row_level_key_is_refused(self):
        r, _e = self.first_edge()
        r["converged"] = not r.get("converged")
        self.refuses("material.d2_store_edges_rows")

    def test_a_missing_row_is_refused(self):
        self.e["rows"].pop()
        self.refuses("material.d2_store_edges_rows")

    def test_today_must_keep_the_compacts_p_b(self):
        r, e = self.first_edge()
        e["p_b"] = e["p_b"] * (1 + 1e-6)
        self.refuses("material.d2_store_today_row")

    def _traced(self, pb):
        r, e = self.first_edge()
        e.update(p_b=pb, p_b_source="traced", match={"kind": "unmatched", "t": r["t"], "p": pb, "phase_key": "x",
                                                     "gap_cells": 0.0, "n_candidates": 1, "record": ["unmatched", 0]})
        c = self.e["source"]["counts"]
        c["none"] -= 1
        c["unmatched"] += 1
        return r

    def test_traced_strictly_inside(self):
        r, _e = self.first_edge()
        self._traced(r["p_lo"])                              # §10: the interval made inclusive must fail this
        self.refuses("material.d2_store_edges_rows")

    def test_a_traced_point_inside_passes_and_counts_must_match(self):
        r, _e = self.first_edge()
        self._traced(0.5 * (r["p_lo"] + r["p_hi"]))
        ds.check_units(self.e, self.b)
        self.e["source"]["counts"]["unmatched"] += 1
        self.refuses("material.d2_store_edges_rows")

    def test_kind_closed_and_keys_per_kind(self):
        _r, e = self.first_edge()
        e["match"] = {"kind": "guess"}
        self.refuses("material.d2_store_keys")
        self.setUp()
        _r, e = self.first_edge()
        e["match"] = {"kind": "none", "t": 1.0}
        self.refuses("material.d2_store_keys")

    def test_coincident_edges_taking_two_points_are_refused(self):
        # a coincident cut pair (init merges it into a swap) whose edges take two different traced points
        runs = ma._cut_runs(ma.build_curves(copy.deepcopy(self.b), self.ts))
        _n, ids = ds.coincident(runs)
        self.assertTrue(ids, "khan has coincident runs")
        target = next(c for c in runs if c.id in ids and c.kind == "edge")
        row_t, phase = target.rows[0]["t"], target.phase
        for r in self.e["rows"]:
            if r["t"] == row_t and not r.get("node_resolved") and r["class"] != "swap":
                for x in r.get("edges") or ():
                    if x["phase"] == phase and x["p_b"] == target.rows[0]["p_b"]:
                        x["p_b"] = r["p_lo"] + 0.25 * (r["p_hi"] - r["p_lo"])
        with self.assertRaises(ds.StoreRefusal) as cm:
            ds.check_coincident(self.e, self.b, self.ts)
        self.assertEqual(cm.exception.id, "material.d2_store_coincident")

    def test_h6_on_the_stores_certified_extension_rows(self):
        ext = self.e.get("extension") or {}
        if not ext.get("rows"):
            self.skipTest("no extension rows on this record")
        r = ext["rows"][0]
        r.update(certified=True, **{"class": "swap"})
        r.setdefault("p_lo", self.ps[0])
        r.setdefault("p_hi", self.ps[3])
        r.setdefault("p_b", self.ps[1])
        with self.assertRaises(ds.StoreRefusal) as cm:
            ds.check_extension_h6(self.e, self.compact)
        self.assertIn("(H6)", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
