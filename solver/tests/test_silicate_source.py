# 규산염 표 출처 뼈대 시험 — 출하 키 해석·요청서 붙은 거절·결정적 요청서·호출자가 쓰는 파일·material_assemblage 바이트 불변 (layers S2)
"""layers S2 registration 106041ab §4 (rev 1, 68 clear e41090d1).

Run from the worktree root:  python -m unittest solver.tests.test_silicate_source
No integration runs: every solve here refuses (or is stopped by a spy) at view building, before any pass.
"""
import gzip
import hashlib
import json
import random
import shutil
import tempfile
import types
import unittest
from pathlib import Path

import yaml

from solver import context, material_assemblage as ma, material_registry as mr, result as rs
from solver import run_oracle as ro, silicate_source as ss, solve as sv, validate as vd
from solver.tests import test_a6_state as a6
from solver.tests import test_bulk_validate as bv

ROOT = Path(__file__).resolve().parents[2]
SHIPPED = ("silicate_slb_default_bse", "silicate_slb_earth_dmm_wh2005", "silicate_slb_mars_khan2022")
MA_BLOB = "a21205fa634a7d0910e257f051d2eb7108eb45fd"   # material_assemblage.py at 42c1edfd and a9b9b596 (§4.5c)
#: §4.3's named control (seed 20261107): rev 0's rounded-cfmasna key differs from the declared oxides' key here
CONTROL = {"CaO": 5.716, "FeO": 39.153, "MgO": 48.943, "Al2O3": 27.008, "SiO2": 25.944, "Na2O": 49.827}


def registry():
    return mr.load()


def shipped_compositions():
    """The three shipped records' declared oxides, from in-tree sources (the records and tables do not carry them):
    default_bse = solver/data/bse_ms95.yaml (MS95 Table 4); earth_dmm_wh2005 = engine/test_mantle_composition.py's
    printed `DMM_WH2005` (read by AST, as engine/test_c143_guard.py reads it); mars_khan2022 = Khan 2022 Table 1
    (test_partition.Mars.MANTLE)."""
    import ast
    from solver.tests import test_partition as tp
    from solver.yamlio import load_data
    src = (ROOT / "engine" / "test_mantle_composition.py").read_text(encoding="utf-8")
    dmm = next(ast.literal_eval(n.value) for n in ast.parse(src).body
               if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "DMM_WH2005")
    return {"silicate_slb_default_bse": dict(load_data(ROOT / "solver" / "data" / "bse_ms95.yaml")["oxides_wt"]),
            "silicate_slb_earth_dmm_wh2005": dict(dmm), "silicate_slb_mars_khan2022": dict(tp.Mars.MANTLE)}


def earth_body():
    return vd.validate(bv.earth_doc(), "bulk_earth", bv.mats())


class Resolve(unittest.TestCase):
    """§4.1: a shipped key resolves to its record as today; two records on one key stay ambiguous."""

    @classmethod
    def setUpClass(cls):
        cls.reg = registry()

    def test_shipped_keys_resolve_to_their_records(self):
        comps = shipped_compositions()
        for rid in SHIPPED:
            ox = comps[rid]
            with self.subTest(record=rid):
                self.assertEqual(ss.resolve(ox, self.reg, source_kind="measured", grade="x", requested_by="t"),
                                 (rid, None))
                self.assertEqual(ss.lookup(ss.key(ox), self.reg), (rid,))

    def test_route_reaches_the_mars_record(self):
        """The bulk Mars body (MarsB2; 68 n3) reaches _assemblage_view with the Mars record, as before S2."""
        b = vd.validate(bv.mars_doc(), "bulk_mars", bv.mats())
        mantle = next(l for l in b.layers if l.material == "silicate_decl")
        seen, real = [], sv._assemblage_view
        sv._assemblage_view = lambda body, layer, rid, p_stop, reg: (seen.append(rid), ("view", rid))[1]
        try:
            got = sv._silicate_route(b, mantle, False, 0.0, self.reg)
        finally:
            sv._assemblage_view = real
        self.assertEqual(seen, ["silicate_slb_mars_khan2022"])
        self.assertEqual(got, ("view", "silicate_slb_mars_khan2022"))

    def test_control_two_records_one_key_is_ambiguous(self):
        k = ss.key(CONTROL)
        fake = types.SimpleNamespace(records={"a": {"kind": "assemblage", "composition_key": k},
                                              "b": {"kind": "assemblage", "composition_key": k}})
        rid, why = ss.resolve(CONTROL, fake, source_kind=None, grade=None, requested_by="t")
        self.assertIsNone(rid)
        self.assertEqual(why[0], "composition_key_ambiguous")

    def test_no_reduction_is_unknown_material(self):
        """68 n1: today's try/except around composition_key moved into resolve."""
        rid, why = ss.resolve({"SiO2": 45.0}, self.reg, source_kind=None, grade=None, requested_by="t")
        self.assertEqual((rid, why[0]), (None, "unknown_material"))


class NoTable(unittest.TestCase):
    """§4.2: Wang's bulk Earth (S1's (E) body), solved with silicate_records on, refuses no_table_for_composition at
    view building with the request attached."""

    def test_refusal_carries_the_request(self):
        b = earth_body()
        reg = registry()
        calls, real = [], sv._views
        sv._views = lambda *a, **k: (lambda out: (calls.append(out), out)[1])(real(*a, **k))
        try:
            out, _ = sv.solve(b, context.Options(silicate_records=True, sensitivity_dt=0.0), registry=reg)
        finally:
            sv._views = real
        self.assertIsInstance(out, rs.Refusal, getattr(out, "text", ""))
        self.assertEqual(out.id, "input.no_table_for_composition")
        self.assertIs(calls[-1], out)                    # it came from view building, before any pass
        mantle = next(l for l in b.layers if l.material == "silicate_decl")
        want = ss.key(dict(mantle.composition.value))
        req = out.evidence["request"]
        self.assertEqual(req["composition_key"], want)
        self.assertEqual(out.evidence["composition_key"], want)
        self.assertEqual(list(out.evidence["built_keys"]),
                         sorted(reg.records[r]["composition_key"] for r in SHIPPED))
        self.assertEqual(req["requested_by"], "bulk_earth.mantle")
        self.assertEqual(req["source_kind"], "measured")


class Deterministic(unittest.TestCase):
    """§4.3 (rev 1, 68 B1; directing 11-07): the request carries the declared oxides, so the key recomputes."""

    def req(self, ox):
        return ss.request(ox, source_kind="measured", grade="literature", requested_by="b.mantle")

    def test_equal_bytes_and_order_free(self):
        a = dict(CONTROL)
        b = dict(reversed(list(CONTROL.items())))
        self.assertEqual(ss.request_json(self.req(a)), ss.request_json(self.req(b)))
        self.assertEqual(json.loads(ss.request_json(self.req(a))), rs.plain(self.req(a)))

    def test_20000_compositions_recompute(self):
        rnd = random.Random(20261107)
        bad_declared = bad_rounded = 0
        for _ in range(20000):
            ox = {k: round(rnd.uniform(0.1, 50.0), 3) for k in ma.CFMASNA}
            r = json.loads(ss.request_json(self.req(ox)))
            bad_declared += ss.key(r["oxides_wt"]) != r["composition_key"]
            bad_rounded += ss.key({k: round(v, 12) for k, v in ma.cfmasna(ox).items()}) != r["composition_key"]
        print(f"\n20000 compositions: declared-oxide mismatches {bad_declared}, rounded-cfmasna mismatches {bad_rounded}")
        self.assertEqual(bad_declared, 0)
        self.assertGreater(bad_rounded, 0)               # rev 0's rule: the control that shows the class

    def test_named_control(self):
        r = json.loads(ss.request_json(self.req(CONTROL)))
        self.assertEqual(r["composition_key"], "163a37e5f4f640e7")
        self.assertEqual(ss.key(r["oxides_wt"]), "163a37e5f4f640e7")
        self.assertEqual(ss.key({k: round(v, 12) for k, v in ma.cfmasna(CONTROL).items()}), "769b0b459c410b62")

    def test_earth_request_recomputes(self):
        b = earth_body()
        mantle = next(l for l in b.layers if l.material == "silicate_decl")
        r = json.loads(ss.request_json(self.req(dict(mantle.composition.value))))
        self.assertEqual(ss.key(r["oxides_wt"]), r["composition_key"])
        self.assertEqual(set(r["dropped_wt"]) & set(ma.CFMASNA), set())


class CallerWrites(unittest.TestCase):
    """§3 and §4.4–§4.5b: run_oracle writes the request beside OUT_DIR, inside the run's tmp-then-move step."""

    def setUp(self):
        self.d = Path(tempfile.mkdtemp(prefix="s2_caller_"))
        doc = bv.earth_doc()
        self.body = self.d / "bulk_earth.yaml"
        self.body.write_text(yaml.safe_dump(json.loads(json.dumps(doc)), sort_keys=False), encoding="utf-8")
        self.out = self.d / "out"

    def tearDown(self):
        shutil.rmtree(self.d, ignore_errors=True)

    def run_it(self):
        return ro.main([str(self.body), "-", str(self.out), "--silicate-records", "on", "--sensitivity-dt", "0"])

    def test_request_lands_beside_out_dir(self):
        self.assertEqual(self.run_it(), 0)
        recs = sorted(self.out.glob("*.json"))
        self.assertEqual([p.name for p in recs], ["bulk_earth__declared.json"])
        for p in recs:                                   # compare.load_rewrite's own condition (68 B2)
            self.assertTrue({"header", "body", "state", "outcome_kind", "refusal"} <= set(json.loads(p.read_text())))
        rec = json.loads(recs[0].read_text())
        req = rec["refusal"]["evidence"]["request"]
        reqs = sorted(ro.requests_dir(self.out).iterdir())
        self.assertEqual([p.name for p in reqs], [f"bulk_earth__{req['composition_key']}.json"])
        self.assertEqual(reqs[0].read_text(encoding="utf-8"), ss.request_json(req))
        self.assertEqual(sorted(p.name for p in self.out.iterdir()), ["bulk_earth__declared.json"])

    def test_failure_leg_leaves_neither(self):
        """A raise planted inside the run's try, after the request is written to tmp (68 n4: not the move loop)."""
        real = ro.write_request

        def planted(rec, stem, tmp):
            f = real(rec, stem, tmp)
            self.assertIsNotNone(f)
            raise RuntimeError("planted after the request write")
        ro.write_request = planted
        try:
            self.assertEqual(self.run_it(), 2)
        finally:
            ro.write_request = real
        self.assertFalse(self.out.exists() and any(self.out.iterdir()))
        rd = ro.requests_dir(self.out)
        self.assertFalse(rd.exists() and any(rd.iterdir()))


class MaterialAssemblageUnchanged(unittest.TestCase):
    """§4.5c (directing 11-07, §6 (a)): material_assemblage.py is byte-unchanged, checked against its pin sites."""

    def test_module_blob_equals_every_pin(self):
        self.assertEqual(ma.module_blob(), MA_BLOB)
        for rid in SHIPPED:
            t = json.loads(gzip.open(ROOT / "solver" / "materials" / "tables" / f"{rid}.json.gz").read())
            with self.subTest(table=rid):
                self.assertEqual(t["closure_terms"]["monotone"]["material_assemblage_blob"], MA_BLOB)
            fs = json.loads(gzip.open(ROOT / "solver" / "materials" / "fall_sets" / f"{rid}.json.gz").read())
            with self.subTest(fall_set=rid):
                self.assertEqual(fs["stamp"]["build"]["build_tree"]["solver"]["material_assemblage"], MA_BLOB)

    def test_control_one_byte_edit_differs(self):
        data = (ROOT / "solver" / "material_assemblage.py").read_bytes() + b"#"
        self.assertNotEqual(hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), MA_BLOB)


class Purity(unittest.TestCase):
    """§4.6."""

    def test_no_module_state_and_equal_calls(self):
        self.assertEqual(a6.findings((ROOT / "solver" / "silicate_source.py").read_text(), "silicate_source.py"), [])
        reg = registry()
        args = dict(source_kind="measured", grade="g", requested_by="b.l")
        self.assertEqual(ss.resolve(CONTROL, reg, **args), ss.resolve(CONTROL, reg, **args))


if __name__ == "__main__":
    unittest.main(verbosity=2)
