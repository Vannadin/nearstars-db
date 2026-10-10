# 기록마다 만들어지는 시험 — 적재 · 선언된 가장자리 너머 질의 · 검산식 · 인용 파일 존재와 해시 (phase-2 등록 P4)
"""P4 of rewrite/phase2-impl.frozen.md, generated from the registry: one set of checks per shipped record, nothing
hand-listed. Per record:
- it loads, and its view builds;
- every declared window edge, queried just beyond, gives its declared outcome (a refusal by its id);
- every formula check evaluates through the grammar (note 3 C4) and lies within its stated tolerance;
- every cache cite names a file that exists in the paper cache with the cited sha256 (impl P2/P4, note 3 C3).
  Where the cache is absent the test fails loudly; a host without it by design sets NEARSTARS_PAPERS_ABSENT=declared,
  and the test is then an expected failure counted in the summary, never a silent skip.
Per-side continuity across boundaries (P4's fourth item) waits for the first branched record (P6).

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_materials_generated
(the paper cache is found through the git common dir; set NEARSTARS_PAPERS for a clone elsewhere)
"""
import copy
import hashlib
import os
import tempfile
import unittest
from collections.abc import Mapping
from pathlib import Path

from solver import material_checks as mc
from solver import material_registry as mr
from solver import material_view as mv
from solver import stepper as st
from solver.from_v1 import thaw

T_POT = 1600.0
def _default_papers() -> Path:
    """The main checkout's paper cache: the git common dir's parent (any worktree of ~/Desktop/NearStars finds it),
    else beside the worktree (68 N20). NEARSTARS_PAPERS overrides both."""
    import subprocess
    here = Path(__file__).resolve().parent
    p = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], cwd=here,
                       capture_output=True, text=True)
    if p.returncode == 0 and p.stdout.strip():
        return Path(p.stdout.strip()).parent / "docs/phase3/_papers"
    return here.parents[3] / "NearStars/docs/phase3/_papers"


PAPERS = Path(os.environ.get("NEARSTARS_PAPERS") or _default_papers())
PAPERS_ABSENT_DECLARED = os.environ.get("NEARSTARS_PAPERS_ABSENT") == "declared"


def _records():
    reg = mr.load()
    if isinstance(reg, mr.LoadStop):
        raise AssertionError(f"registry STOP: {reg.id} {dict(reg.evidence)}")
    return {k: thaw(v) for k, v in reg.records.items()}


def _cache_cites(x, path="record"):
    if isinstance(x, Mapping):
        if "cache" in x and "sha256" in x:
            yield path, x["cache"], x["sha256"]
        for k, v in x.items():
            yield from _cache_cites(v, f"{path}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from _cache_cites(v, f"{path}[{i}]")


def edge_probes(rec):
    """(phase index, edge name, P, T) just beyond each declared window edge."""
    for i, ph in enumerate(rec["phases"]):
        w = ph["window"]
        mid_t = 0.5 * (float(w.get("t_min", 300.0)) + float(w.get("t_max", 3000.0)))
        mid_p = 0.5 * (float(w["p_min"]) + min(float(w["p_max"]), 1e11))
        for name, e in ph["edges"].items():
            if name not in w:                                       # 68 N21
                raise AssertionError(f"phase {ph['id']}: edge {name} declared without a bound in the window")
            b = float(w[name])
            if name == "p_max":
                yield i, name, b * 1.001, mid_t, e
            elif name == "p_min" and b > 0.0:
                yield i, name, b * 0.999, mid_t, e
            elif name == "t_max":
                yield i, name, mid_p, b + 1.0, e
            elif name == "t_min" and b > 0.0:
                yield i, name, mid_p, b - 1.0, e


def cite_problems(recs, papers: Path = None) -> tuple:
    """68 T4: every (path, file, sha256) triple is compared, each file hashed once; not one cite per file.
    Returns (cites checked, [problem texts])."""
    papers = PAPERS if papers is None else papers
    hashes, n, bad = {}, 0, []
    for rid, rec in recs.items():
        for path, name, sha in _cache_cites(rec):
            f = papers / name
            if not f.is_file():
                bad.append(f"{rid} {path}: {name} not in the cache")
                continue
            if name not in hashes:
                hashes[name] = hashlib.sha256(f.read_bytes()).hexdigest()
            if hashes[name] != sha:
                bad.append(f"{rid} {path}: sha256 {sha[:12]}… is not {name}'s {hashes[name][:12]}…")
            n += 1
    return n, bad


def probe_overlaps(rec) -> tuple:
    """Impl note 6 item 5: walk a field record's declared probe grid; every node must give one phase or a declared
    refusal, and an overlap anywhere is a failure. Returns (nodes walked, [overlap nodes])."""
    pr = rec.get("field_probe")
    if not pr:
        return 0, []
    v = mv.RecordView(rec, T_POT)
    box = pr["box"]
    p_lo, p_hi, t_lo, t_hi = (float(box[k]) for k in ("p_min", "p_max", "t_min", "t_max"))
    dp, dt = float(pr["dp"]), float(pr["dt"])
    n, bad = 0, []
    p = p_lo
    while p <= p_hi + 1e-9 * dp:
        t = t_lo
        while t <= t_hi + 1e-9 * dt:
            got = v._phase_at(p, t)
            n += 1
            if isinstance(got, st.Stop) and "fields overlap" in got.record.why:
                bad.append((p, t, got.record.why))
            t += dt
        p += dp
    return n, bad


class Generated(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recs = _records()

    def test_some_record_is_shipped(self):
        self.assertGreater(len(self.recs), 0)

    def test_views_build(self):
        for rid, rec in self.recs.items():
            with self.subTest(record=rid):
                mv.RecordView(rec, T_POT)

    def test_edges_give_their_declared_outcome(self):
        self.assertGreater(sum(1 for r in self.recs.values() for _ in edge_probes(r)), 0)
        for rid, rec in self.recs.items():
            v = mv.RecordView(rec, T_POT)
            for i, name, p, t, e in edge_probes(rec):
                with self.subTest(record=rid, phase=i, edge=name):
                    s = v.state(p, t)
                    self.assertIsInstance(s, st.Stop, f"beyond {name} gave {s!r}")
                    if "refusal" in e:
                        self.assertEqual(s.record.refusal, e["refusal"])

    def test_formula_checks(self):
        for rid, rec in self.recs.items():
            for r in mc.run_formula_checks(rec, mv.RecordView(rec, T_POT)):
                with self.subTest(record=rid, check=r["quantity"]):
                    self.assertNotIn("stop", r, r.get("stop"))
                    self.assertTrue(r["passed"], r)

    def test_band_methods_evaluate(self):
        """68 N26: every band method in a shipped record evaluates through the grammar, so a broken method fails the
        suite before any solve meets it."""
        n = 0
        for rid, rec in self.recs.items():
            v = mv.RecordView(rec, T_POT)
            for pi, ph in enumerate(rec["phases"]):
                for si, s in enumerate(ph["thermal"].get("sets", ())):
                    band = (s.get("edge_above") or {}).get("band") or {}
                    if "method" not in band:
                        continue
                    with self.subTest(record=rid, phase=pi, set=si):
                        got = mc.evaluate(band["method"], ph, {}, mc.view_spread(v, pi))
                        self.assertNotIsInstance(got, mc.CheckStop, got)
                        n += 1
        self.assertGreater(n, 0)

    def test_field_records_have_no_overlap_on_their_probe_grid(self):
        for rid, rec in self.recs.items():
            if rec.get("kind") == "branched" and rec.get("choice") == "field":
                with self.subTest(record=rid):
                    self.assertIn("field_probe", rec, "a field record declares its probe grid (impl note 6 item 5)")
                    n, bad = probe_overlaps(rec)
                    self.assertGreater(n, 0)
                    self.assertEqual(bad, [])

    def test_cache_cites_exist_with_their_hash(self):
        if not PAPERS.is_dir():
            self.fail(f"paper cache not found at {PAPERS}; set NEARSTARS_PAPERS, or NEARSTARS_PAPERS_ABSENT=declared")
        n = 0
        n, bad = cite_problems(self.recs)
        self.assertEqual(bad, [])
        self.assertGreater(n, 0, "no cache cite was checked")

    # A host without the cache by declaration: the test above becomes an expected failure, counted in the summary
    # («expected failures=1»), never a silent skip (impl P2).
    if not PAPERS.is_dir() and PAPERS_ABSENT_DECLARED:
        test_cache_cites_exist_with_their_hash = unittest.expectedFailure(test_cache_cites_exist_with_their_hash)


class Controls(unittest.TestCase):
    """P4's planted controls: a formula check off by 2× its tolerance fails; an undeclared edge STOPs at load."""

    def test_formula_check_off_by_twice_its_tolerance_fails(self):
        rec = _records()["fe_prem"]
        fc = rec["formula_checks"][0]
        fc["expected"] = float(fc["expected"]) + 2.0 * float(fc["tolerance"]) + abs(
            mc.run_formula_checks(rec)[0]["got"] - float(fc["expected"]))
        self.assertFalse(mc.run_formula_checks(rec)[0]["passed"])

    def test_second_cite_of_a_file_with_another_files_sha_fails(self):
        """68 T4 (N25: runs everywhere, no real cache): two cites of one file, the second carrying the other registered
        file's sha256, give exactly one problem."""
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp, "a.pdf"), Path(tmp, "b.pdf")
            a.write_bytes(b"%PDF-1.4 a\n")
            b.write_bytes(b"%PDF-1.4 b\n")
            sa, sb = (hashlib.sha256(x.read_bytes()).hexdigest() for x in (a, b))
            rec = {"x": {"cache": "a.pdf", "sha256": sa}, "y": {"cache": "a.pdf", "sha256": sb},
                   "z": {"cache": "b.pdf", "sha256": sb}}
            self.assertEqual(cite_problems({"toy": rec}, Path(tmp))[0], 3)
            self.assertEqual(len(cite_problems({"toy": rec}, Path(tmp))[1]), 1)
            rec["y"]["sha256"] = sa
            self.assertEqual(cite_problems({"toy": rec}, Path(tmp))[1], [])

    def test_probe_finds_an_overlap(self):
        """Impl note 6 item 5 control: the toy field record with VI no longer bounded by VII overlaps above 2.2 GPa;
        intact, it does not."""
        from solver.tests.test_material_field import field_record
        rec = field_record()
        rec["field_probe"] = {"box": {"p_min": 2.0e9, "p_max": 2.3e9, "t_min": 290.0, "t_max": 310.0},
                              "dp": 0.05e9, "dt": 10.0}
        self.assertEqual(probe_overlaps(rec)[1], [])
        rec["boundaries"] = rec["boundaries"][1:]
        self.assertGreater(len(probe_overlaps(rec)[1]), 0)

    def test_edge_without_a_bound_fails(self):
        """68 N21: a declared edge whose bound is not in the window is a failure, not a skip."""
        rec = _records()["fe_prem"]
        rec["phases"][0]["edges"]["t_max"] = {"refusal": "input.material_out_of_data"}
        with self.assertRaises(AssertionError):
            list(edge_probes(rec))

    def test_undeclared_edge_stops_at_load(self):
        rec = copy.deepcopy(_records()["fe_prem"])
        rec["phases"][0]["edges"].pop("p_max")
        self.assertEqual(mr.check_record(rec, "fe_prem.yaml", frozenset(
            s for _p, _n, s in _cache_cites(rec))).id, "material.edge_undeclared")


if __name__ == "__main__":
    unittest.main()
