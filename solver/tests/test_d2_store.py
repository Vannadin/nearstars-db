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
EXPECTED = Path(__file__).resolve().parent / "fixtures" / "d2_store_shared_fixtures_expected.json"
_REG = None


def reg():
    global _REG
    if _REG is None:
        _REG = mr.load()
    return _REG


# ── note 2 (1) condition 1 (view piece), and S1's closure change (read piece) ───────────────────────────────────────
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

    def test_d2_store_enters_the_read_closure_with_the_read_piece(self):
        """View piece: d2_store was outside closure() (note 2 (1) condition 1). Read piece S1: material_registry loads
        the store (Registry.d2_store), so d2_store enters the closure, 13 → 14 modules (note 2 «Hence»; row c8-12)."""
        got = fall_sets.closure(ROOT)
        self.assertIn("d2_store", got)
        self.assertIn("material_assemblage", got)
        self.assertEqual(len(got), 14, got)


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
    """A planted view whose full curves are their own event runs (no cut / across split, no merge)."""
    return types.SimpleNamespace(ts=ts, _reach=REACH, _curves=curves, _events=curves)


# ── fixtures through ma.view on a planted block (68 n1 on 039c875b): init's own curves, runs, merge and stops ─────
KHAN = "silicate_slb_mars_khan2022"


def _edge(t, p_lo, p_hi, pb, phases, across):
    return {"t": t, "p_lo": p_lo, "p_hi": p_hi, "left": "a+b", "right": "a+c", "class": "edge_in", "converged": True,
            "edges": [{"phase": ph, "p_b": pb, "converged": True, "delta_rho": 1e-4 if across else None,
                       "over_tolerance": False if across else True, "p_b_source": "today"} for ph in phases]}


def real_view(rows, extension):
    """(store, view): the khan compact with its boundaries replaced by `rows`, the view built by ma.view (init runs),
    and a store on the compact's grid with no cells yet (each fixture plants its own)."""
    compact = thaw(reg().tables[KHAN])
    block = {"status": "exported", "rows": rows, "source": {}}
    if extension:
        block["extension"] = {"rows": [], "rule": {"ext_rows": 2}}
    compact["boundaries"] = block
    v = ma.view(thaw(reg().get(KHAN)), compact, 1600.0)
    ps, ts = ds.nodes(compact)
    return {"grid": {"ps": ps, "ts": ts}, "cells": {}, "edges": block}, v


def joining_segment_fixture():
    """68 B1: one edge curve over four T rows, cut on the first two and read across on the last two; the segment that
    joins row 1 (cut) to row 2 (across) climbs three P columns, and a d2 cell sits on a column it crosses strictly
    between its ends. The full-curve walk STOPs there; a walk of the event runs (their own rows, and flat stubs at the
    interior run ends) does not."""
    ps, ts = ds.nodes(thaw(reg().tables[KHAN]))
    k, j = 2, 10
    def pb(jj): return 0.5 * (ps[jj] + ps[jj + 1])
    rows = [_edge(ts[k - 1], ps[j], ps[j + 1], pb(j), ("x",), False),
            _edge(ts[k], ps[j], ps[j + 1], pb(j), ("x",), False),
            _edge(ts[k + 1], ps[j + 3], ps[j + 4], pb(j + 3), ("x",), True),
            _edge(ts[k + 2], ps[j + 3], ps[j + 4], pb(j + 3), ("x",), True)]
    st, v = real_view(rows, extension=False)
    st["cells"] = {f"{j + 1},{k}": {"class": "d2"}}
    return st, v, (j + 1, k)


def coincident_fixture(extension):
    """Two edges of one row, cut, at one P_b, over two T rows: init merges them into swaps, with reach-0 ends when the
    block has `extension`. d2 cells at the rows' interval and one interval past each end."""
    ps, ts = ds.nodes(thaw(reg().tables[KHAN]))
    k, j = 3, 12
    pb = 0.5 * (ps[j] + ps[j + 1])
    rows = [_edge(ts[k], ps[j], ps[j + 1], pb, ("x", "y"), False),
            _edge(ts[k + 1], ps[j], ps[j + 1], pb, ("x", "y"), False)]
    st, v = real_view(rows, extension)
    st["cells"] = {f"{j},{kk}": {"class": "d2"} for kk in (k - 1, k, k + 1)}
    return st, v, (j, k)


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


def real_fixtures():
    """name → (store, view) for the fixtures built through ma.view (68 n1, B1)."""
    j_st, j_v, _c = joining_segment_fixture()
    c_on, v_on, _c = coincident_fixture(True)
    c_off, v_off, _c = coincident_fixture(False)
    return {"real_joining_segment_cut_to_across": (j_st, j_v), "real_coincident_pair_extension": (c_on, v_on),
            "real_coincident_pair_no_extension": (c_off, v_off)}


def stop_sets():
    """name → sorted [(refusal id, cell or reason)]: the engine side's decisions on the shared fixtures."""
    out = {}
    for name, (st, v) in {**shared_fixtures(), **real_fixtures()}.items():
        got = ds.today_segments(st, v)
        out[name] = sorted([rid, text.split("cell ")[-1] if "cell (" in text else text] for rid, text in got["stops"])
    return out


class RealViewFixtures(unittest.TestCase):
    """68 B1 and n1 on 039c875b: the walk is every full curve, row to row, with extensions only at true ends."""

    def cells(self, st, v):
        return {t.split("cell ")[-1] for _i, t in ds.today_segments(st, v)["stops"]}

    def test_the_joining_segment_of_a_cut_and_an_across_run_is_walked(self):
        st, v, (j, k) = joining_segment_fixture()
        self.assertEqual({c.kind for c in v._curves}, {"edge"})
        self.assertEqual(len(v._curves), 1)
        self.assertEqual(len(v._events), 2)                       # one cut run, one across run
        self.assertIn(f"({j}, {k})", self.cells(st, v))
        # the mutant: walking the event runs instead of the full curves misses that cell
        runs = types.SimpleNamespace(ts=v.ts, _reach=v._reach, _curves=v._events, _events=v._events)
        self.assertNotIn(f"({j}, {k})", self.cells(st, runs))

    def test_a_coincident_pair_with_extension_stops_at_its_rows_only(self):
        st, v, (j, k) = coincident_fixture(True)
        self.assertEqual(v.coincident, 2)
        self.assertEqual({c.kind for c in v._cut}, {"swap"})
        self.assertEqual(self.cells(st, v), {f"({j}, {k})"})

    def test_the_same_pair_without_extension_stops_past_its_ends(self):
        st, v, (j, k) = coincident_fixture(False)
        got = self.cells(st, v)
        self.assertIn(f"({j}, {k})", got)
        self.assertTrue({f"({j}, {k - 1})", f"({j}, {k + 1})"} & got, got)


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



class ReadPieceInterface(unittest.TestCase):
    """S0: the read piece's frozen interface (D2-read note 2 (1); §5b (2), §6, §7). Shape only: the logic is S1–S4's."""

    def test_count_names_and_the_no_field_line_match_the_reference_reader(self):
        self.assertEqual(ds.NO_FIELD, "d2: no field at the point → table read")
        self.assertEqual(ds.COUNT_NAMES[0], ds.NO_FIELD)
        self.assertEqual(len(set(ds.COUNT_NAMES)), 4)
        self.assertEqual(ds.RUN_RECORD_LINE.format(name=ds.NO_FIELD, n=3, m=10),
                         "d2: no field at the point → table read: 3 of 10 reads")

    def test_read_point_is_the_reference_readers_shape(self):
        self.assertEqual(ds.READ_CLASSES, ("table", "d2", "cut", "subgrid"))
        self.assertEqual(ds.VALUE_KEYS, ("c_p", "dtdp", "rho", "s"))
        self.assertEqual(ds.SUBGRID_VALUE_KEYS, ("alpha", "c_p", "dtdp", "rho", "s"))
        doc = {"grid": {"ps": [1e9, 2e9], "ts": [1000.0, 1100.0]}, "cells": {}}
        self.assertEqual(ds.read_point(doc, 3e9, 1000.0)["read"], "table")          # S2: outside the grid → table

    def test_boundary_block_returns_todays_block_until_routing_and_names_its_use(self):
        table = {"boundaries": {"status": "exported", "rows": []}}
        for use in ma.BLOCK_USES:
            self.assertIs(ma.boundary_block({}, table, None, use), table["boundaries"])
        with self.assertRaises(ValueError):
            ma.boundary_block({}, table, None, "both")

    def test_census_keys(self):
        from solver.landing import d2_read_census as c
        self.assertEqual(c.SITE_KEYS, ("path", "line", "kind", "function"))
        self.assertEqual(c.KINDS, ("option", "record_key", "view", "solid", "boundaries", "table_regardless"))


class ReadPieceS1(unittest.TestCase):
    """S1 (D2-read §4, §5b (2), (2a), (6)): the switch, the two curve sets on a D2-routed view, the routing, the force
    map and the curve identity refusal. A routed view is built with a fixture store whose `edges` block is the khan
    compact's block with one cut run's P_b moved inside its pair (a «traced» row); the read set stays the compact's."""

    @classmethod
    def setUpClass(cls):
        cls.rec = thaw(reg().get(KHAN))
        cls.compact = thaw(reg().tables[KHAN])
        cls.edges = copy.deepcopy(cls.compact["boundaries"])
        v0 = ma.view(cls.rec, cls.compact, 1600.0)
        cut = next(c for c in v0._cut if c.kind == "edge" and len(c.rows) >= 2)
        cls.moved_t = cut.rows[0]["t"]
        for r in cls.edges["rows"]:                       # move that run's first row's P_b by a tenth of its pair
            if r["t"] == cls.moved_t and abs(r["p_lo"] - cut.rows[0]["p_lo"]) == 0.0:
                for e in r["edges"]:
                    if e.get("p_b") == cut.rows[0]["p_b"]:
                        e["p_b"] = e["p_b"] + 0.1 * (r["p_hi"] - e["p_b"])
                        cls.moved = True
        cls.store = ds.Loaded("eligible", {"edges": cls.edges, "grid": {"ps": [], "ts": []}, "cells": {}}, "0" * 64)

    def routed(self, **kw):
        return ma.view(self.rec, self.compact, 1600.0, store=self.store, **kw)

    def test_fixture_moves_a_position(self):
        self.assertTrue(getattr(self, "moved", False))

    def test_the_switch(self):
        """§5b (2): the store's block only for «position» on a routed record; the compact's for «read», unrouted, and
        in table-regardless mode (the view passes store=None then)."""
        self.assertIs(ma.boundary_block(self.rec, self.compact, self.store, "position"), self.edges)
        self.assertIs(ma.boundary_block(self.rec, self.compact, self.store, "read"), self.compact["boundaries"])
        self.assertIs(ma.boundary_block(self.rec, self.compact, None, "position"), self.compact["boundaries"])
        v = self.routed(table_regardless="test")
        self.assertIs(v._pos, v._read_set)

    def test_unrouted_is_one_set_object_for_object(self):
        v = ma.view(self.rec, self.compact, 1600.0)
        self.assertIs(v._pos, v._read_set)
        self.assertIsNone(v._pos_read)

    def test_positions_from_the_store_reads_from_the_compact(self):
        """§5b (2) test: on the routed view, transitions and boundary_pressure equal those of a view whose table block
        IS the store's block, bit for bit; the read curves equal the unrouted view's."""
        v = self.routed()
        as_table = ma.view(self.rec, {**self.compact, "boundaries": self.edges}, 1600.0)
        plain = ma.view(self.rec, self.compact, 1600.0)
        self.assertEqual(v.transitions(), as_table.transitions())
        for i, (_n, _k, cv) in enumerate(v.transitions()):
            for t in (self.moved_t, self.moved_t + 25.0):
                self.assertEqual(repr(v.boundary_pressure(cv, t)), repr(as_table.boundary_pressure(cv, t)), (i, t))
        self.assertEqual([[r["p_b"] for r in c.rows] for c in v._curves], [[r["p_b"] for r in c.rows] for c in plain._curves])
        moved = [c for c in v._pos.curves if any(r["t"] == self.moved_t for r in c.rows)]
        self.assertNotEqual([[r["p_b"] for r in c.rows] for c in v._pos.curves],
                            [[r["p_b"] for r in c.rows] for c in v._curves], moved)

    def test_mutant_position_reader_left_on_the_compact(self):
        """§5b's mutant «a position reader left on the compact's block» must fail the test above."""
        from unittest import mock
        with mock.patch.object(ma, "boundary_block", lambda rec, table, store, use: table["boundaries"]):
            v = self.routed()
        as_table = ma.view(self.rec, {**self.compact, "boundaries": self.edges}, 1600.0)
        self.assertNotEqual([c.rows[0]["p_b"] for c in v._pos.events], [c.rows[0]["p_b"] for c in as_table._events])

    def test_mutant_read_curves_from_the_store(self):
        """§5b (6)'s mutant «the read curves taken from the store» must change the read set."""
        from unittest import mock
        real = ma.boundary_block
        with mock.patch.object(ma, "boundary_block",
                               lambda rec, table, store, use: real(rec, table, store, "position")):
            v = self.routed()
        plain = ma.view(self.rec, self.compact, 1600.0)
        self.assertNotEqual([[r["p_b"] for r in c.rows] for c in v._curves],
                            [[r["p_b"] for r in c.rows] for c in plain._curves])

    def test_force_on_a_position_curve_forces_its_read_curve(self):
        """§5b (6) «Curve identity across the two sets»: a {curve: side} on a position run is the same force as on the
        read run with its id and T span."""
        v = self.routed()
        pos = next(c for c in v._pos.cut if c.kind == "swap") if any(c.kind == "swap" for c in v._pos.cut) else v._pos.cut[0]
        rd = v._pos_read[pos]
        self.assertIsNot(pos, rd)
        self.assertEqual((pos.id, pos.t0, pos.t1), (rd.id, rd.t0, rd.t1))
        t = 0.5 * (pos.t0 + pos.t1) if pos.t1 > pos.t0 else pos.t0
        p = rd.p_b(t)
        got = {}
        for side in (-1, 1):
            a = v.s_path(p * (1 + 1e-9), t, force={pos: side})
            b = v.s_path(p * (1 + 1e-9), t, force={rd: side})
            self.assertEqual(repr(a), repr(b), side)
            got[side] = repr(a)
        self.assertNotEqual(got[-1], got[1])               # not vacuous: the force decides the answer here
        v._pos_read = None                                   # the mutant: no map, a position curve's force is dropped
        self.assertNotEqual({repr(v.s_path(p * (1 + 1e-9), t, force={pos: s_})) for s_ in (-1, 1)}, set(got.values()))

    def test_a_curve_in_one_set_only_is_refused_by_name(self):
        edges = copy.deepcopy(self.edges)
        t_last = max(r["t"] for r in edges["rows"])
        edges["rows"] = [r for r in edges["rows"] if r["t"] != t_last]
        with self.assertRaises(ma.TableStop) as cm:
            ma.view(self.rec, self.compact, 1600.0, store=ds.Loaded("eligible", {"edges": edges, "grid": {"ps": [], "ts": []}, "cells": {}}, "0" * 64))
        self.assertIn("curve id in one set only", str(cm.exception))

    def test_fall_sets_reads_the_store_blocks_extension_rows(self):
        """§5b (2a): planted different extension rows in the table's block and the store's; the store's are read."""
        comp = copy.deepcopy(self.compact)
        edges = copy.deepcopy(self.edges)
        comp["boundaries"]["extension"] = {"rows": [], "rule": {"ext_rows": 2}}
        t = self.compact["cells"][0]["t"]
        edges["extension"] = {"rows": [{"t": t, "curve_end_t": -1.0, "p_b": 7.77e9}], "rule": {"ext_rows": 2}}
        v = ma.view(self.rec, comp, 1600.0, store=ds.Loaded("eligible", {"edges": edges, "grid": {"ps": [], "ts": []}, "cells": {}}, "0" * 64))
        pts = fall_sets._region_points(v, comp)["swap_extension"]
        self.assertTrue(any(abs(p / 7.77e9 - 1.0) < 1e-2 for p, _t in pts), pts[:4])
        v0 = ma.view(self.rec, comp, 1600.0)
        self.assertFalse(any(abs(p / 7.77e9 - 1.0) < 1e-2 for p, _t in fall_sets._region_points(v0, comp)["swap_extension"]))

    def test_routing_off_never_opens_the_store_and_reads_today(self):
        """§4: d2_read off (or absent) reads today's answer and never opens a store; a planted unreadable store file
        under fields/ stays unread. Registry.d2_store is None for it."""
        from unittest import mock
        rec_off = {**self.rec, "d2_read": "off"}
        opened = []
        real = Path.read_bytes
        with mock.patch.object(Path, "read_bytes", lambda self_: opened.append(str(self_)) or real(self_)):
            self.assertIsNone(ds.load(rec_off, self.compact, ROOT / "solver" / "materials"))
        self.assertFalse([f for f in opened if "/fields/" in f], opened)
        self.assertIsNone(reg().d2_store(KHAN))                 # no d2_read key: off, store never asked
        a, b = ma.view(rec_off, self.compact, 1600.0), ma.view(self.rec, self.compact, 1600.0)
        for p_, t_ in ((5e9, 1600.0), (2e10, 2100.0)):
            self.assertEqual(repr(a.state(p_, t_)), repr(b.state(p_, t_)))

    def test_global_off_never_asks_for_a_store(self):
        """§4's first row: global off × eligible stays legacy and the store is not even asked for."""
        from unittest import mock
        from solver import solve as sv
        asked = []

        class R:
            development = False
            tables = {KHAN: self.compact}

            def get(self_, rid):
                return reg().get(rid)

            def d2_store(self_, rid):
                asked.append(rid)
                raise AssertionError("asked")
        body = mock.Mock()
        body.surface.t_pot = 1600.0
        layer = mock.Mock(material="silicate", composition=None)
        with mock.patch.object(sv.lm.interior, "MATERIALS", {}):
            got = sv._assemblage_view(body, layer, KHAN, 0.0, R(), silicate=False)
        self.assertEqual(asked, [])
        self.assertIsNone(got[1])


class ReadPieceS2(unittest.TestCase):
    """S2 (D2-read §5, Q6, Q8, Q9): the class dispatch at the read's answer, s_path through it, the notes swapped."""

    @classmethod
    def setUpClass(cls):
        cls.rec = thaw(reg().get(KHAN))
        cls.compact = thaw(reg().tables[KHAN])
        cls.store = ds.Loaded("eligible", {"edges": copy.deepcopy(cls.compact["boundaries"]), "grid": {}, "cells": {}},
                              "0" * 64)
        cls.pt = (2.0e10, 2000.0)

    def routed(self):
        return ma.view(self.rec, self.compact, 1600.0, store=self.store)

    def test_a_table_answer_reads_today_bit_for_bit(self):
        from unittest import mock
        plain = ma.view(self.rec, self.compact, 1600.0)
        v = self.routed()
        with mock.patch.object(ds, "read_point", lambda doc, p, t, view=None: {"read": "table", "why": "fallback", "notes": ()}):
            self.assertEqual(repr(v.state(*self.pt)), repr(plain.state(*self.pt)))
            self.assertEqual(repr(v.s_path(*self.pt)), repr(plain.s_path(*self.pt)))

    def test_a_d2_answer_is_the_read_and_carries_its_class_note_not_the_tables_bands(self):
        from unittest import mock
        v = self.routed()
        ans = {"read": "d2", "field": "f", "values": {"rho": 4321.0, "s": 2500.0, "c_p": 1200.0, "dtdp": 2.5e-8},
               "notes": (("d2", ds.D2_NOTE),)}
        with mock.patch.object(ds, "read_point", lambda doc, p, t, view=None: ans):
            got = v._solid(*self.pt)
            self.assertEqual(got[:3], (4321.0, 2.5e-8, 1200.0))
            self.assertEqual(len(got[3]), 4)                  # Q9: the table's four corner cells stay
            out = v.state(*self.pt)
        texts = [getattr(n, "text", None) or str(n) for n in out[2]]
        self.assertTrue(any(ds.D2_NOTE in t for t in texts), texts)
        self.assertFalse(any("dT/dP model consistency" in t for t in texts), texts)

    def test_s_path_on_a_surface_and_inside_a_sliver(self):
        """Q6: Dual(s, −P·G_PT, −G_TT); Q8: Dual(s, −P·α/ρ, c_P/T)."""
        from unittest import mock
        v = self.routed()
        p_, t_ = self.pt
        with mock.patch.object(ds, "s_parts", lambda doc, p, t: ("surface", 2500.0, -3e-12, -0.6)):
            d = v.s_path(p_, t_)
            self.assertEqual((d.v, d.dx, d.dt) if hasattr(d, "dx") else tuple(d), (2500.0, -p_ * -3e-12, 0.6))
        with mock.patch.object(ds, "s_parts", lambda doc, p, t: ("sliver", 2500.0, 4000.0, 3e-5, 1200.0)):
            d = v.s_path(p_, t_)
            self.assertEqual((d.v, d.dx, d.dt) if hasattr(d, "dx") else tuple(d),
                             (2500.0, -p_ * 3e-5 / 4000.0, 1200.0 / t_))

    def test_q8_ratio_on_the_fixture_subgrid_stores(self):
        """Q8: −(∂s/∂P)/(∂s/∂T) from s_path's parts against the read's dT/dP on ea's subgrid fixture stores. Registered
        «bit for bit»; measured ≤ 3 ulp (two roundings in the Dual's slopes), raised with 68 (S2). Held at 3 ulp here."""
        import random
        import struct
        ulp = lambda a, b: abs(struct.unpack("<q", struct.pack("<d", a))[0] - struct.unpack("<q", struct.pack("<d", b))[0])  # noqa: E731
        base = Path(__file__).resolve().parent / "fixtures" / "d2_reference" / "stores"
        for name in ("subgrid", "subgrid_reversed"):
            doc = json.loads(gzip.decompress((base / f"{name}.json.gz").read_bytes()))
            ps, ts = doc["grid"]["ps"], doc["grid"]["ts"]
            rnd, n = random.Random(1), 0
            for _ in range(4000):
                p_, t_ = rnd.uniform(ps[0], ps[-1]), rnd.uniform(ts[0], ts[-1])
                r = ds.read_point(doc, p_, t_)
                if r["read"] != "subgrid":
                    continue
                _k, s_, rho, a, cp = ds.s_parts(doc, p_, t_)
                self.assertEqual(s_, r["values"]["s"])
                self.assertLessEqual(ulp(-(-p_ * a / rho / p_) / (cp / t_), r["values"]["dtdp"]), 3)
                n += 1
            self.assertGreater(n, 10, name)

    def test_the_no_field_count(self):
        base = Path(__file__).resolve().parent / "fixtures" / "d2_reference" / "stores"
        doc = json.loads(gzip.decompress((base / "d2_fieldless.json.gz").read_bytes()))
        v = types.SimpleNamespace(d2_counts={ds.NO_FIELD: 0})
        ps, ts = doc["grid"]["ps"], doc["grid"]["ts"]
        hits = 0
        for j in range(len(ps) - 1):
            for k in range(len(ts) - 1):
                for a in (0.05, 0.25, 0.5, 0.75, 0.95):
                    for b in (0.05, 0.25, 0.5, 0.75, 0.95):
                        r = ds.read_point(doc, ps[j] + a * (ps[j + 1] - ps[j]), ts[k] + b * (ts[k + 1] - ts[k]), v)
                        hits += r.get("why") == ds.NO_FIELD
        self.assertGreater(hits, 0)
        self.assertEqual(v.d2_counts[ds.NO_FIELD], hits)

if __name__ == "__main__":
    unittest.main()
