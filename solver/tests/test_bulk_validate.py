# bulk: 블록이 검증기를 지나 오늘의 층·닫힘이 되는지 시험 — 비트 동일 관문·프리셋 대조·화성(b2)·지구(a)·거절 (layers S1)
"""layers S1 registration 1346ffc6 §4, tests 1–5 (6–8 live in test_partition, test_b4_input and the guards).

Run from the worktree root:  python -m unittest solver.tests.test_bulk_validate
No test here solves a body except through the switch check at solve's entry (§2.4), which returns before any solve.
"""
import copy
import hashlib
import json
import math
import types
import unittest
from pathlib import Path

import yaml

from solver import context, from_v1 as fv, material_assemblage as ma, partition as pt, result as rs
from solver import solve as sv, validate as vd
from solver.tests.test_partition import Mars, wang_bulk

ROOT = Path(__file__).resolve().parents[2]
CANON = Path(__file__).resolve().parent / "fixtures" / "bulk_s1_body_canon.json"
E_TRIO = {"source_kind": "measured", "grade": "literature", "counter_evidence_searched": "test fixture"}
#: Mars's radius as a measured block (68's note on the S1 clear: mars.yaml's radius_earth is a bare 0.5320 with no
#: grade or source). Rivoldini+ 2011 (2011Icar..213..451R, cached), PDF p. 8, the mean radius «3389.5 ± 0.2» km;
#: 3389.5 / 6371 = 0.532020… R⊕ (6371 km: validate.EARTH_RADIUS_M). Khan+ 2022 PDF p. 13 prints the same 3389.5 km.
MARS_RADIUS = {"value": 3389.5 / 6371.0, "grade": "measured",
               "source": "2011Icar..213..451R (cached) PDF p. 8: Mars mean radius «3389.5 ± 0.2» km; / 6371 km",
               "counter_evidence_searched": "Khan+ 2022 (2022E_PSL.57817330K, cached) PDF p. 13 prints 3389.5 km"}
MARS_RECORD_KEY = "19e84b63bac74c9a"            # silicate_slb_mars_khan2022's composition key (S1 §4.3)


def mats():
    return vd.production_materials(vd.PRODUCTION)


def v1_doc(stem):
    return yaml.load((ROOT / "engine" / "bodies" / f"{stem}.yaml").read_text(encoding="utf-8"), Loader=fv._V1Loader)


def v2_of(stem):
    out = fv.from_v1(v1_doc(stem), stem)
    return copy.deepcopy(fv.thaw(out[0]))


def khan_elements():
    """S0 test 3's construction: Khan 2022 Table 1 mantle × 0.75 + the core × 0.25 (mars.yaml's S/O/C split)."""
    mass = pt.BULK["atomic_mass_g_mol"]
    by = {v[0]: (k, v[1], v[2]) for k, v in pt.BULK["oxides"].items()}
    s = math.fsum(Mars.MANTLE.values())
    el = {}
    for ox, w in Mars.MANTLE.items():
        k, n_cat, n_o = by[ox]
        m = 0.75 * w / s
        cat = m * n_cat * mass[k] / (n_cat * mass[k] + n_o * mass["O"])
        el[k] = el.get(k, 0.0) + cat
        el["O"] = el.get("O", 0.0) + m - cat
    for k, x in Mars.CORE.items():
        el[k] = el.get(k, 0.0) + 0.25 * x
    return el


def mars_doc(radius=MARS_RADIUS, core_light=None):
    el = khan_elements()
    return {"name": "bulk_mars", "kind": "planet", "inputs": {"mass_earth": 0.107, "radius_earth": radius},
            "bulk": {"elements": el, "source": "Khan+ 2022 round trip (S0 test 3)", **E_TRIO,
                     "params": {"fe_metal_fraction": 0.25 * 0.816 / el["Fe"], "core_material": "fe_core_light",
                                "core_light": core_light or {"S": 0.130, "O": 0.04, "C": 0.014}}}}


def earth_doc(**inputs):
    b, _ = wang_bulk()
    b = {**b, **E_TRIO}
    return {"name": "bulk_earth", "kind": "planet", "inputs": {"mass_earth": 1.0, **inputs}, "bulk": b}


def refused(tc, got, rid):
    tc.assertIsInstance(got, rs.Refusal, f"expected {rid}, got a {type(got).__name__}")
    tc.assertEqual(got.id, rid, got.text)
    return got


class BitIdentity(unittest.TestCase):
    """Test 1 (gate): every v1 body and every v2 test doc validates to the same Body as at ea3ae617 (the fixture is
    NearStars-artifacts rewrite/layers/s1/body_canon.py, blob 657769a3, run on a clean ea3ae617 worktree)."""

    def test_every_body_and_doc_equal_to_the_base(self):
        ref = json.loads(CANON.read_text())
        self.assertEqual(ref["tree"], "ea3ae6173987352ab33537dd0143793df937e901")
        digest = lambda x: hashlib.sha256(rs.canonical(x).encode()).hexdigest()   # noqa: E731
        paths = sorted((ROOT / "engine" / "bodies").glob("*.yaml"))
        self.assertEqual(sorted(p.name for p in paths), sorted(ref["bodies"]))
        for p in paths:
            got = fv.load_v1(str(p))
            b = got[0] if isinstance(got, tuple) else got
            with self.subTest(body=p.name):
                self.assertEqual({"kind": type(b).__name__, "sha256": digest(b)}, ref["bodies"][p.name])
        import importlib
        for mod, want in ref["docs"].items():
            b = vd.validate(importlib.import_module(f"solver.tests.{mod}").doc(), "<doc>", mats())
            with self.subTest(doc=mod):
                self.assertEqual({"kind": type(b).__name__, "sha256": digest(b)}, want)


class PresetAndMaterials(unittest.TestCase):
    """Test 2: earth and pandora through from_v1 → D; D with bulk (P) or (M) in place of layers + closure validates
    to a Body equal to validate(D)."""

    def swap(self, stem, bulk):
        d = v2_of(stem)
        lid = [l for l in d["layers"] if l["role"] == "lid"]
        del d["layers"], d["closure"]
        d["bulk"] = dict(bulk)
        if lid:
            d["bulk"]["lithosphere_thickness_km"] = lid[0]["extent"]["depth_from_surface"]
        return d

    def test_preset_and_materials_equal_from_v1(self):
        m = [{"material": "fe_prem", "mass_fraction": 0.325}, {"material": "silicate", "mass_fraction": 0.675}]
        for stem in ("earth", "pandora"):
            want = rs.canonical(vd.validate(v2_of(stem), stem, mats()))
            for bulk in ({"preset": "earth_like"}, {"materials": m}):
                with self.subTest(body=stem, form=next(iter(bulk))):
                    got = vd.validate(self.swap(stem, bulk), stem, mats())
                    self.assertIsInstance(got, vd.bd.Body, getattr(got, "text", ""))
                    self.assertEqual(rs.canonical(got), want)

    def test_control_another_mass_fraction_differs(self):
        m = [{"material": "fe_prem", "mass_fraction": 0.326}, {"material": "silicate", "mass_fraction": 0.674}]
        got = vd.validate(self.swap("earth", {"materials": m}), "earth", mats())
        self.assertIsInstance(got, vd.bd.Body)
        self.assertNotEqual(rs.canonical(got), rs.canonical(vd.validate(v2_of("earth"), "earth", mats())))


class MarsB2(unittest.TestCase):
    """Test 3: Khan's round-trip bulk with a measured radius takes (b2), its mantle key is the shipped record's, and
    the plan's CMF and FeO sit in Khan's printed bands. This replaces design §7 item 2's comparison with today's Mars
    solve, which is held (E18-mars, C59; LAYERS-S1-MARS): no solve output is compared here."""

    @classmethod
    def setUpClass(cls):
        cls.body = vd.validate(mars_doc(), "bulk_mars", mats())

    def test_b2_and_the_record_key(self):
        b = self.body
        self.assertIsInstance(b, vd.bd.Body, getattr(b, "text", ""))
        self.assertEqual((b.closure.kind, b.closure.layer), ("boundary_mass", "core"))
        core, mantle = b.layers[0], b.layers[1]
        self.assertIsNone(core.extent)
        self.assertEqual(core.material, "fe_core_light")
        self.assertEqual(ma.composition_key(dict(mantle.composition.value)), MARS_RECORD_KEY)
        plan = mantle.composition.extra["bulk_plan"]
        self.assertLessEqual(abs(plan["core_mass_fraction"] - 0.250), 0.005)
        self.assertLessEqual(abs(mantle.composition.value["FeO"] - 13.68), 0.43)
        self.assertLessEqual(abs(plan["residual"]), 1e-12)


class EarthForms(unittest.TestCase):
    """Test 4: Wang's bulk validates; a radius block graded `measured` gives (b2), anything else (a). Not solved
    (68 n2): S1 validates this Body only. Its solve would refuse `no_table_for_composition` (S2) with silicate_records
    on, and `input.bulk_needs_silicate_records` with it off; the validation is not a solve claim."""

    R = {"value": 1.0, "grade": "measured", "source": "test", "counter_evidence_searched": "test"}

    def test_measured_radius_takes_b2(self):
        b = vd.validate(earth_doc(radius_earth=dict(self.R)), "bulk_earth", mats())
        self.assertIsInstance(b, vd.bd.Body, getattr(b, "text", ""))
        self.assertEqual(b.closure.kind, "boundary_mass")

    def test_otherwise_a_fully_forward(self):
        """Directing 11-07 / 68 B1: a radius graded `literature` takes (a): closure R, the core's extent the plan's
        CMF to 1e-15, no boundary_mass anywhere. A bare number and no radius do the same."""
        plan = pt.partition(earth_doc()["bulk"], {})
        for case, inputs in (("literature", {"radius_earth": {**self.R, "grade": "literature"}}),
                             ("bare", {"radius_earth": 1.0}), ("none", {})):
            with self.subTest(case=case):
                b = vd.validate(earth_doc(**inputs), "bulk_earth", mats())
                self.assertIsInstance(b, vd.bd.Body, getattr(b, "text", ""))
                self.assertEqual(b.closure.kind, "R")
                self.assertEqual(b.layers[0].extent.kind, "mass_fraction")
                self.assertLessEqual(abs(b.layers[0].extent.value - plan.core_mass_fraction), 1e-15)
                self.assertNotIn("boundary_mass", rs.canonical(b.closure))

    def test_source_kind_on_the_radius_block_refuses(self):
        """Rev 0's unreachable form (68 B1): input blocks take BLOCK_FIELDS only."""
        refused(self, vd.validate(earth_doc(radius_earth={**self.R, "source_kind": "measured"}), "bulk_earth",
                                  mats()), "input.unknown_key")


class Refusals(unittest.TestCase):
    """Test 5: one planted case per S1 id and the expansion's cross checks; the switch's control."""

    def test_bulk_with_layers_refuses(self):
        d = earth_doc()
        d["layers"] = v2_of("earth")["layers"]
        refused(self, vd.validate(d, "x", mats()), "input.cross_field")

    def test_unknown_bulk_key_and_star_derived(self):
        d = earth_doc()
        d["bulk"]["colour"] = "red"
        refused(self, vd.validate(d, "x", mats()), "input.unknown_key")
        d = earth_doc()
        d["bulk"]["source_kind"] = "star_derived"
        refused(self, vd.validate(d, "x", mats()), "input.source_kind_not_built")

    def test_s0_ids_through_the_validator(self):
        d = earth_doc()
        d["bulk"]["elements"]["U"] = -1e-9             # a negative share refuses before the core is drawn
        refused(self, vd.validate(d, "x", mats()), "input.bulk_fractions")
        d = earth_doc()
        d["bulk"]["elements"]["U"] = 1e-6              # every share ≥ 0, the sum off by 1e-6
        refused(self, vd.validate(d, "x", mats()), "input.bulk_fractions")
        d = mars_doc(core_light={"S": 0.20, "O": 0.04, "C": 0.014})
        del d["bulk"]["elements"]["S"]                 # the core must draw S the bulk does not hold
        s = math.fsum(d["bulk"]["elements"].values())
        d["bulk"]["elements"] = {k: v / s for k, v in d["bulk"]["elements"].items()}
        refused(self, vd.validate(d, "x", mats()), "input.bulk_core_draw_short")

    def test_core_light_range(self):
        for cl in ({"S": 0.6, "O": 0.3, "C": 0.1}, {"S": 0.6, "O": 0.3, "C": 0.2}, {"S": -0.01, "O": 0.04, "C": 0.0}):
            with self.subTest(core_light=cl):
                r = refused(self, vd.validate(mars_doc(core_light=cl), "x", mats()), "input.bulk_core_light")
                self.assertAlmostEqual(r.evidence["total"], math.fsum(cl.values()))

    def test_mutant_without_the_core_light_check(self):
        """With partition's range check removed, the S + O + C = 1.1 case is not named input.bulk_core_light: Fe goes
        negative and some later check (or arithmetic) meets it instead. The check is what names the fault."""
        src = Path(pt.__file__).read_text()
        old = "        if tot >= 1.0 or any(v < 0.0 for v in x.values()):"
        self.assertEqual(src.count(old), 1)
        mod = types.ModuleType("partition_mutant")
        mod.__file__ = pt.__file__
        import sys
        sys.modules["partition_mutant"] = mod
        try:
            exec(compile(src.replace(old, "        if False:"), "partition_mutant", "exec"), mod.__dict__)
        finally:
            del sys.modules["partition_mutant"]
        doc = mars_doc(core_light={"S": 0.6, "O": 0.3, "C": 0.2})
        try:
            got = mod.partition(doc["bulk"], doc["bulk"]["params"])
            self.assertNotEqual(getattr(got, "id", None), "input.bulk_core_light")
        except (ZeroDivisionError, ValueError):
            pass

    def test_volatile_layer_refuses(self):
        d = earth_doc()
        el = d["bulk"]["elements"]
        el["H2O"] = 0.01
        s = math.fsum(pt._val(v) for v in el.values())
        d["bulk"]["elements"] = {k: ({"value": v["value"] / s, "sigma": v["sigma"] / s} if isinstance(v, dict) else v / s)
                                 for k, v in el.items()}
        r = refused(self, vd.validate(d, "x", mats()), "input.bulk_volatile_layer")
        self.assertGreater(r.evidence["h2o"], 0.0)

    def test_switch_off_refuses_at_solve_entry(self):
        """§2.4: a bulk_plan mantle solved with silicate_records off refuses before any solve. Control: with it on,
        the same body reaches `_solve` (stubbed here, so nothing is integrated)."""
        b = vd.validate(mars_doc(), "bulk_mars", mats())
        reached = []
        real = sv._solve
        sv._solve = lambda *a, **k: (reached.append(1), (rs.Refusal("stub", "stub", {}, "stub"), None))[1]
        try:
            out, _ = sv.solve(b, context.Options(silicate_records=False))
            refused(self, out, "input.bulk_needs_silicate_records")
            self.assertEqual(reached, [])
            sv.solve(b, context.Options(silicate_records=True))
            self.assertEqual(reached, [1])
        finally:
            sv._solve = real
        e = fv.load_v1(str(ROOT / "engine" / "bodies" / "earth.yaml"))[0]
        self.assertFalse(any(l.composition is not None and "bulk_plan" in l.composition.extra for l in e.layers))


if __name__ == "__main__":
    unittest.main(verbosity=2)
