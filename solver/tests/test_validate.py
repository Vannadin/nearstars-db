# 입력 검사 시험 — 스키마에서 만든 경계 표 · 키와 꼴 거절 · 유효한 0 · YAML 1.2 수 · 닫힘 미지수 수 (등록 c8 T-boundary · T-keys)
"""T-boundary and T-keys of rewrite/phase1-impl-c8.frozen.md, each with its negative control.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_validate
"""
import copy
import math
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

from solver import body as bd
from solver import validate as vd
from solver.result import Refusal

BASE = {
    "name": "T", "kind": "planet",
    "inputs": {"mass_earth": 1.0, "potential_temperature": 1600.0},
    "layers": [{"id": "core", "role": "core", "material": "fe_prem", "extent": {"mass_fraction": 0.325}},
               {"id": "mantle", "role": "mantle", "material": "silicate"}],
    "closure": {"kind": "R"},
}


def doc(**patch):
    d = copy.deepcopy(BASE)
    for k, v in patch.items():
        d[k] = v
    return d


def with_input(key, value):
    d = doc()
    d["inputs"][key] = value
    return d


def without_input(key):
    d = doc()
    d["inputs"].pop(key, None)
    return d


def violates(x, dom):
    return not all({"gt": x > b, "ge": x >= b, "lt": x < b, "le": x <= b}[op] for op, b in dom.items())


def refused(test, out, id_, **ev):
    test.assertIsInstance(out, Refusal, f"expected {id_}, got a Body")
    test.assertEqual(out.id, id_, out.text)
    for k, v in ev.items():
        test.assertEqual(out.evidence[k], v, out.text)


class TBase(unittest.TestCase):
    def test_base_loads(self):
        b = vd.validate(doc())
        self.assertIsInstance(b, bd.Body)
        self.assertEqual(b.surface.m, 5.972e24)
        self.assertEqual(b.interface("cmb").name, "core/mantle")
        self.assertEqual(b.closure.lo, 0.05 * 6.371e6)


class TBoundaryTable(unittest.TestCase):
    """Generated from schema.yaml: a new key is covered without a new test line."""

    def test_numeric_keys(self):
        for key, spec in vd.SCHEMA["inputs"].items():
            if spec["shape"] not in ("number", "number_or_block"):
                continue
            dom = spec.get("domain", {})
            cases = [(math.nan, "input.non_finite"), (math.inf, "input.non_finite"), (-math.inf, "input.non_finite"),
                     ("1.0", "input.not_number"), (None, "input.null_value"), (True, "input.not_number")]
            for probe in (0.0, -1.0):                    # zero and a negative, only where the domain excludes them
                if violates(probe, dom):
                    cases.append((probe, "input.out_of_domain"))
            for bad, want in cases:
                with self.subTest(key=key, bad=bad):
                    refused(self, vd.validate(with_input(key, bad)), want)
            if spec.get("required"):
                with self.subTest(key=key, bad="missing"):
                    refused(self, vd.validate(without_input(key)), "input.missing_key", key=key)

    def test_1e400_from_text(self):
        text = yaml.safe_dump(doc()).replace("mass_earth: 1.0", "mass_earth: 1e400")
        refused(self, vd.validate(vd.parse(text)), "input.non_finite", key="mass_earth")

    def test_bool_and_enum_keys(self):
        for key, spec in vd.SCHEMA["inputs"].items():
            with self.subTest(key=key):
                if spec["shape"] == "bool":
                    refused(self, vd.validate(with_input(key, "false")), "input.not_boolean")
                    refused(self, vd.validate(with_input(key, 1)), "input.not_boolean")
                    refused(self, vd.validate(with_input(key, None)), "input.null_value")
                elif spec["shape"] == "enum":
                    refused(self, vd.validate(with_input(key, "nope")), "input.not_in_vocabulary")
                    refused(self, vd.validate(with_input(key, 5)), "input.not_text")

    def test_valid_zeros_load(self):
        self.assertIsInstance(vd.validate(with_input("eccentricity", 0.0)), bd.Body)
        d = doc(jumps={"cmb": 0.0})
        self.assertIsInstance(vd.validate(d), bd.Body)
        d = doc(layers=[{"id": "core", "role": "core", "material": "fe", "extent": {"mass_fraction": 0.2}},
                        {"id": "basal", "role": "basal_layer", "material": "b",
                         "extent": {"thickness_above": {"layer": "core", "km": 0.0}}},          # R-BL-7
                        {"id": "mantle", "role": "mantle", "material": "s"}])
        self.assertIsInstance(vd.validate(d), bd.Body)
        d = doc(layers=[{"id": "core", "role": "core", "material": "fe", "extent": {"mass_fraction": 0.3}},
                        {"id": "ice", "role": "ice", "material": "h2o", "extent": {"mass_fraction": 0.0}},
                        {"id": "mantle", "role": "mantle", "material": "s"}])
        # an ice layer below a mantle is not an order violation in the registry (only core and envelope are placed)
        self.assertIsInstance(vd.validate(d), bd.Body)


class TKeys(unittest.TestCase):
    def test_unknown_key_with_hint(self):
        out = vd.validate(with_input("potental_temperature", 1600.0))
        refused(self, out, "input.unknown_key", key="potental_temperature", nearest="potential_temperature")

    def test_unknown_key_control(self):
        # control: with the key check off, the typo key no longer gives the named refusal (it ends unnamed)
        with mock.patch.object(vd, "_keys", lambda m, allowed, where: None):
            try:
                out = vd.validate(with_input("potental_temperature", 1600.0))
            except Exception:
                out = None
            self.assertFalse(isinstance(out, Refusal) and out.id == "input.unknown_key")

    def test_duplicate_key_with_line(self):
        text = "name: T\nkind: planet\nname: U\n"
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "dup.yaml"
            p.write_text(text, encoding="utf-8")
            refused(self, vd.load(p), "input.duplicate_key", key="name", line=3)
        # control: PyYAML's own loader takes the last value silently
        self.assertEqual(yaml.safe_load(text)["name"], "U")

    def test_empty_and_non_mapping(self):
        with tempfile.TemporaryDirectory() as d:
            for name, text, want in (("e.yaml", "", "input.empty"), ("l.yaml", "- a\n- b\n", "input.not_mapping")):
                p = Path(d) / name
                p.write_text(text, encoding="utf-8")
                refused(self, vd.load(p), want)
            refused(self, vd.load(Path(d) / "absent.yaml"), "input.unreadable")

    def test_value_less_block(self):
        refused(self, vd.validate(with_input("lid_thickness_km", {"grade": "analog", "source": "s", "note": "n"})),
                "input.value_missing", key="lid_thickness_km")

    def test_null_parent_refused(self):
        refused(self, vd.validate(doc(parent=None)), "input.null_value", key="parent")

    def test_units(self):
        refused(self, vd.validate(with_input("potential_temperature", {"value": 1600.0, "unit": "C"})),
                "input.unit_mismatch", expected="K")
        refused(self, vd.validate(with_input("potential_temperature",
                                             {"value": 1600.0, "unit": "Fe#(=100·Fe/(Fe+Mg), 몰비) — 0–100"})),
                "input.unit_mismatch")
        self.assertIsInstance(vd.validate(with_input("potential_temperature", {"value": 1600.0, "unit": "K"})), bd.Body)

    def test_grades(self):
        refused(self, vd.validate(with_input("age_gyr", {"value": 4.5, "grade": "calibrated"})), "input.bad_grade")
        refused(self, vd.validate(with_input("age_gyr", {"value": 4.5, "grade": "declared-default"})), "input.bad_grade")

    def test_yaml12_numbers_and_bools(self):
        d = vd.parse("a: 6.0e21\nb: 1e-3\nc: no\nd: true\n")
        self.assertEqual(d, {"a": 6.0e21, "b": 1e-3, "c": "no", "d": True})
        # control: PyYAML 1.1 reads 6.0e21 as a string and «no» as False (R-A1-14)
        d11 = yaml.safe_load("a: 6.0e21\nc: no\n")
        self.assertEqual(d11, {"a": "6.0e21", "c": False})

    def test_closure_count(self):
        core = {"id": "core", "role": "core", "material": "fe", "extent": {"mass_fraction": 0.2}, "system": "iron_alloy",
                "composition": {"value": {"S": "fit", "O": 0.04}, "grade": "declared", "source": "s",
                                "counter_evidence_searched": "c"}}
        layers = [core, {"id": "mantle", "role": "mantle", "material": "s"}]
        refused(self, vd.validate(doc(layers=layers)), "input.closure_count", count=2)          # R closure + a fit
        d = doc(layers=layers, closure={"kind": "composition", "layer": "core", "name": "S"})
        d["inputs"]["radius_earth"] = 0.532
        b = vd.validate(d)
        self.assertIsInstance(b, bd.Body)
        self.assertEqual((b.closure.lo, b.closure.hi), (0.13, 0.25))                           # SULPHUR_FIT_BRACKET
        d = doc(closure={"kind": "composition", "layer": "core", "name": "S"})
        d["inputs"]["radius_earth"] = 0.532
        refused(self, vd.validate(d), "input.closure_count", count=0)                         # nothing marked fit
        refused(self, vd.validate(doc(layers=layers, closure={"kind": "composition", "layer": "core", "name": "S"})),
                "input.cross_field")                                                         # inverse needs radius

    def test_boundary_mass_closure(self):
        d = doc(layers=[{"id": "core", "role": "core", "material": "fe"}, {"id": "mantle", "role": "mantle", "material": "s"}],
                closure={"kind": "boundary_mass", "layer": "core"})
        d["inputs"]["radius_earth"] = 0.95
        b = vd.validate(d)
        self.assertIsInstance(b, bd.Body)
        self.assertEqual(b.radius.value, 0.95 * 6.371e6)

    def test_thickness_above_pattern(self):
        d = doc(layers=[{"id": "core", "role": "core", "material": "fe", "extent": {"mass_fraction": 0.2}},
                        {"id": "mantle", "role": "mantle", "material": "s", "extent": {"mass_fraction": 0.7}},
                        {"id": "crust", "role": "crust", "material": "c",
                         "extent": {"thickness_above": {"layer": "mantle", "km": 40.0}}}])
        refused(self, vd.validate(d), "input.thickness_above_pattern", layer_id="crust")

    def test_layer_rules(self):
        d = doc(layers=[{"id": "m", "role": "mantle", "material": "s", "extent": {"mass_fraction": 0.7}},
                        {"id": "c", "role": "core", "material": "fe"}])
        refused(self, vd.validate(d), "input.layer_order")
        d = doc(layers=[{"id": "c", "role": "core", "material": "fe"}, {"id": "m", "role": "mantle", "material": "s"}])
        refused(self, vd.validate(d), "input.extent_invalid")                                  # two remainders
        d = doc(layers=[{"id": "c", "role": "core", "material": "fe", "extent": {"mass_fraction": 0.6}},
                        {"id": "m", "role": "mantle", "material": "s", "extent": {"mass_fraction": 0.6}}])
        refused(self, vd.validate(d), "input.mass_fraction_sum")
        d = doc(layers=[{"id": "c", "role": "rock", "material": "fe"}])
        refused(self, vd.validate(d), "input.unknown_role", role="rock")
        d = doc(jumps={"core/crust": 100.0})
        refused(self, vd.validate(d), "input.jump_boundary")

    def test_material_resolver(self):
        class M:
            def known(self, mid):
                return mid != "unobtainium"

            def composition_window(self, mid, system):
                return {"O": (0.01, 0.04, "CORE_BOX_WT (R-CLE-4)")}
        core = {"id": "core", "role": "core", "material": "fe", "extent": {"mass_fraction": 0.2}, "system": "iron_alloy",
                "composition": {"value": {"O": 0.05}, "grade": "declared", "source": "s", "counter_evidence_searched": "c"}}
        refused(self, vd.validate(doc(layers=[core, {"id": "m", "role": "mantle", "material": "s"}]), materials=M()),
                "input.composition_window", component="O")
        refused(self, vd.validate(doc(layers=[{"id": "c", "role": "core", "material": "unobtainium",
                                                "extent": {"mass_fraction": 0.3}},
                                               {"id": "m", "role": "mantle", "material": "s"}]), materials=M()),
                "input.unknown_material")

    def test_load_all_isolates_files(self):
        with tempfile.TemporaryDirectory() as d:
            good = Path(d) / "a.yaml"
            good.write_text(yaml.safe_dump(doc()), encoding="utf-8")
            bad = Path(d) / "b.yaml"
            bad.write_text("", encoding="utf-8")
            out = vd.load_all([good, bad])
            self.assertIsInstance(out[str(good)], bd.Body)
            refused(self, out[str(bad)], "input.empty")
            twin = Path(d) / "c.yaml"
            twin.write_text(yaml.safe_dump(doc()), encoding="utf-8")
            out = vd.load_all([good, twin])
            refused(self, out[str(good)], "input.duplicate_name", name="T")


if __name__ == "__main__":
    unittest.main()
