# 입력 검사 시험 — 스키마 전체에서 만든 경계 표 · 키와 꼴 거절 · 유효한 0 · YAML 1.2 수 · 닫힘 미지수 · 깨진 입력에도 예외 없음 (등록 c8 T-boundary · T-keys)
"""T-boundary and T-keys of rewrite/phase1-impl-c8.frozen.md, each with its negative control.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_validate
"""
import copy
import math
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import yaml

from solver import body as bd
from solver import validate as vd
from solver import yamlio
from solver.result import Refusal

BASE = {
    "name": "T", "kind": "planet",
    "inputs": {"mass_earth": 1.0, "potential_temperature": 1600.0, "surface_temperature_k": 293.0},
    "layers": [{"id": "core", "role": "core", "material": "fe_prem", "extent": {"mass_fraction": 0.325}},
               {"id": "mantle", "role": "mantle", "material": "silicate"}],
    "closure": {"kind": "R"},
}
BLOCK = {"grade": "analog", "source": "s", "note": "n"}


def doc(**patch):
    d = copy.deepcopy(BASE)
    d.update(copy.deepcopy(patch))
    return d


def with_input(key, value):
    d = doc()
    d["inputs"][key] = value
    return d


def violates(x, dom):
    return not all({"gt": x > b, "ge": x >= b, "lt": x < b, "le": x <= b}[op] for op, b in dom.items())


def refused(test, out, id_, **ev):
    test.assertIsInstance(out, Refusal, f"expected {id_}, got a Body")
    test.assertEqual(out.id, id_, out.text)
    for k, v in ev.items():
        if k == "key_prefix":
            test.assertTrue(str(out.evidence.get("key", "")).startswith(v), f"{dict(out.evidence)} vs {v}")
        else:
            test.assertEqual(out.evidence[k], v, out.text)


# ── slots: every numeric place in the schema, with a setter and its expected key (r2 S2-B4) ─────────────────
def _set_input(key, block=False):
    def setter(d, x):
        d["inputs"][key] = {"value": x, **BLOCK} if block else x
    return setter


def _set_layer(path):
    def setter(d, x):
        layers = d["layers"]
        if path == "mass_fraction":
            layers[0]["extent"] = {"mass_fraction": x}
        elif path == "radius_from_centre":
            layers[0]["extent"] = {"radius_from_centre": x}
        elif path == "depth_from_surface":
            layers.append({"id": "lid", "role": "lid", "material": "silicate", "thermal": "conductive",
                           "extent": {"depth_from_surface": x}})
        elif path == "thickness_above":
            layers.insert(1, {"id": "basal", "role": "basal_layer", "material": "b",
                              "extent": {"thickness_above": {"layer": "core", "km": x}}})
        elif path == "t_declared":
            layers[1]["thermal"], layers[1]["t_declared"] = "isothermal", x
    return setter


def _set_closure(kind, end):
    def setter(d, x):
        if kind == "boundary_mass":
            d["layers"] = [{"id": "core", "role": "core", "material": "fe"}, {"id": "mantle", "role": "mantle", "material": "s"}]
            d["inputs"]["radius_earth"] = 0.95
            d["closure"] = {"kind": kind, "layer": "core", "lo": 0.1, "hi": 0.9}
        else:
            d["closure"] = {"kind": kind, "lo": 0.5, "hi": 2.0}
        d["closure"][end] = x
    return setter


def _set_jump(d, x):
    d["jumps"] = {"cmb": x}


def _set_band(end):
    def setter(d, x):
        b = {"lo": 1500.0, "hi": 1700.0}
        b[end] = x
        d["inputs"]["potential_temperature"] = {"value": 1600.0, "band": b, **BLOCK}
    return setter


def _set_uncertainty(d, x):
    d["inputs"]["potential_temperature"] = {"value": 1600.0, "uncertainty": x, "uncertainty_basis": "±", **BLOCK}


def _set_record(field):
    def setter(d, x):
        d["inputs"]["radiogenic_concentration"] = {"U_ppb": 20.0, "Th_ppb": 80.0, "K_ppm": 200.0, field: x,
                                                   "grade": "literature", "source": "s"}
    return setter


def slots():
    out = []
    for key, spec in vd.SCHEMA["inputs"].items():
        if spec["shape"] in ("number", "number_or_block"):
            out.append((f"inputs.{key}", _set_input(key), key, spec.get("domain", {})))
            if spec["shape"] == "number_or_block":
                out.append((f"inputs.{key}{{value}}", _set_input(key, True), key, spec.get("domain", {})))
        elif spec["shape"] == "block" and spec.get("value_shape") is None:
            out.append((f"inputs.{key}{{value}}", _set_input(key, True), key, spec.get("domain", {})))
        elif spec["shape"] == "record":
            for f, fs in spec.get("fields", {}).items():
                if fs.get("shape") == "number":
                    out.append((f"inputs.{key}.{f}", _set_record(f), f"{key}.{f}", fs.get("domain", {})))
    for form in ("mass_fraction", "radius_from_centre", "depth_from_surface", "thickness_above"):
        out.append((f"extent.{form}", _set_layer(form), "", vd.SCHEMA["extent"][form]["domain"]))
    out.append(("layer.t_declared", _set_layer("t_declared"), "mantle.t_declared", {"gt": 0}))
    out.append(("jumps.cmb", _set_jump, "jumps.cmb", vd.SCHEMA["jump"]["domain"]))
    for kind in ("R", "boundary_mass"):
        for end in ("lo", "hi"):
            out.append((f"closure.{kind}.{end}", _set_closure(kind, end), f"closure.{end}",
                        vd.SCHEMA["closure"]["kinds"][kind]["domain"]))
    for end in ("lo", "hi"):
        out.append((f"band.{end}", _set_band(end), "potential_temperature.band", {}))
    out.append(("uncertainty", _set_uncertainty, "potential_temperature.uncertainty", {"ge": 0}))
    return out


class TBase(unittest.TestCase):
    def test_base_loads(self):
        b = vd.validate(doc())
        self.assertIsInstance(b, bd.Body)
        self.assertEqual(b.surface.m, 5.972e24)
        self.assertEqual(b.interface("cmb").name, "core/mantle")
        self.assertEqual(b.closure.lo, 0.05 * 6.371e6)
        self.assertEqual(b.surface_declared["potential_temperature"].value, 1600.0)

    def test_schema_is_frozen(self):
        with self.assertRaises((TypeError, AttributeError)):
            vd.SCHEMA["grades"]["input"].append("calibrated")
        with self.assertRaises(TypeError):
            vd.SCHEMA["grades"]["new"] = 1


class TBoundaryTable(unittest.TestCase):
    """Every numeric place in the schema (r2 S2-B4): NaN, ±inf, a quoted number, None, True, plus 0 and −1 where the
    domain excludes them. The evidence key is asserted."""

    def test_every_numeric_slot(self):
        for label, setter, key, dom in slots():
            cases = [(math.nan, "input.non_finite"), (math.inf, "input.non_finite"), (-math.inf, "input.non_finite"),
                     ("1.0", "input.not_number"), (None, "input.null_value"), (True, "input.not_number")]
            for probe in (0.0, -1.0):
                if violates(probe, dom):
                    cases.append((probe, "input.out_of_domain"))
            for bad, want in cases:
                with self.subTest(slot=label, bad=bad):
                    d = doc()
                    setter(d, bad)
                    out = vd.validate(d)
                    refused(self, out, want, **({"key_prefix": key} if key and "key" in out.evidence else {}))

    def test_every_slot_accepts_a_valid_value(self):
        for label, setter, key, dom in slots():
            ok = 0.5 if not violates(0.5, dom) else 2.0
            if label.startswith("band.") or label == "uncertainty":
                ok = 1600.0 if label == "band.lo" else 1650.0 if label == "band.hi" else 10.0
            if label == "closure.R.hi":
                ok = 5.0
            if label == "closure.boundary_mass.hi":
                ok = 0.95
            with self.subTest(slot=label):
                d = doc()
                setter(d, ok)
                self.assertIsInstance(vd.validate(d), bd.Body, label)

    def test_control(self):
        # control: with finiteness unchecked, NaN no longer gives input.non_finite
        with mock.patch.object(vd, "math", types.SimpleNamespace(isfinite=lambda x: True)):
            out = vd.validate(with_input("mass_earth", math.nan))
        self.assertFalse(isinstance(out, Refusal) and out.id == "input.non_finite")

    def test_si_overflow(self):
        refused(self, vd.validate(with_input("mass_earth", 1e300)), "input.out_of_domain", key="mass_earth")
        refused(self, vd.validate(with_input("mass_earth", 10 ** 400)), "input.non_finite", key="mass_earth")
        d = doc()
        d["layers"][0]["extent"] = {"radius_from_centre": 1e306}
        refused(self, vd.validate(d), "input.out_of_domain")

    def test_1e400_from_text(self):
        text = yaml.safe_dump(doc()).replace("mass_earth: 1.0", "mass_earth: 1e400")
        refused(self, vd.validate(yamlio.parse(text)), "input.non_finite", key="mass_earth")

    def test_valid_zeros_load(self):
        self.assertIsInstance(vd.validate(with_input("eccentricity", 0.0)), bd.Body)
        self.assertIsInstance(vd.validate(doc(jumps={"cmb": 0.0})), bd.Body)
        d = doc(layers=[{"id": "core", "role": "core", "material": "fe", "extent": {"mass_fraction": 0.2}},
                        {"id": "basal", "role": "basal_layer", "material": "b",
                         "extent": {"thickness_above": {"layer": "core", "km": 0.0}}},          # R-BL-7
                        {"id": "mantle", "role": "mantle", "material": "s"}])
        self.assertIsInstance(vd.validate(d), bd.Body)
        d = doc(layers=[{"id": "core", "role": "core", "material": "fe", "extent": {"mass_fraction": 0.3}},
                        {"id": "ice", "role": "ice", "material": "h2o", "extent": {"mass_fraction": 0.0}},
                        {"id": "mantle", "role": "mantle", "material": "s"}])
        self.assertIsInstance(vd.validate(d), bd.Body)


def _deep(n):
    d = {"value": 1.0, "grade": "literature", "source": "s", "counter_evidence_searched": "c"}
    for _ in range(n):
        d = {"x": d}
    return d


class TNeverRaises(unittest.TestCase):
    """r2 S2-B1: every malformed input gives a named refusal, never an exception."""

    RAW = [
        ("params list", lambda d: d["layers"][0].update(params=[1])),
        ("jumps list", lambda d: d.update(jumps=[1])),
        ("inputs list", lambda d: d.update(inputs=[1])),
        ("layers mapping", lambda d: d.update(layers={"a": 1})),
        ("layer not mapping", lambda d: d["layers"].append(5)),
        ("closure R with layer", lambda d: d.update(closure={"kind": "R", "layer": "core"})),
        ("closure R with name", lambda d: d.update(closure={"kind": "R", "name": "S"})),
        ("closure kind missing", lambda d: d.update(closure={"lo": 1.0})),
        ("closure kind not text", lambda d: d.update(closure={"kind": 5})),
        ("composition closure without name",
         lambda d: (d["inputs"].update(radius_earth=0.5), d.update(closure={"kind": "composition", "layer": "core"}))),
        ("deep record", lambda d: d["inputs"].update(thermal_evolution=_deep(1500))),
        ("record list", lambda d: d["inputs"].update(radiogenic_concentration=[1])),
        ("source list", lambda d: d["inputs"].update(potential_temperature={"value": 1600.0, "grade": "analog",
                                                                            "source": ["a"], "note": "n"})),
        ("note int", lambda d: d["inputs"].update(potential_temperature={"value": 1600.0, "grade": "analog",
                                                                         "source": "s", "note": 5})),
        ("extent two forms", lambda d: d["layers"][0].update(extent={"mass_fraction": 0.3, "radius_from_centre": 1.0})),
        ("composition not mapping", lambda d: d["layers"][0].update(system="iron_alloy", composition={"value": 3, **BLOCK})),
        ("params key int", lambda d: d["layers"][0].update(params={1: "fit"})),
    ]

    def test_raw_cases(self):
        for label, mutate in self.RAW:
            with self.subTest(case=label):
                d = doc()
                mutate(d)
                self.assertIsInstance(vd.validate(d), Refusal, label)

    def test_raw_control(self):
        # control: with the shape check gone, a list of params crashes instead of refusing
        d = doc()
        d["layers"][0]["params"] = [1]
        with mock.patch.object(vd, "_mapping", lambda v, key, where: v):
            with self.assertRaises(AttributeError):
                vd.validate(d)

    def test_files(self):
        cases = [("bytes.yaml", b"name: \xa4\xff\n", "input.unreadable"),
                 ("complex.yaml", "? [1, 2]\n: x\n".encode(), "input.not_text"),
                 ("date.yaml", b"name: 2024-13-45\n", "input.missing_key"),        # a date is a string now
                 ("nest.yaml", ("[" * 3000).encode(), "input.unreadable"),
                 ("tab.yaml", b"name:\t- x\n  :", "input.unreadable")]
        with tempfile.TemporaryDirectory() as tmp:
            for name, data, want in cases:
                with self.subTest(file=name):
                    p = Path(tmp) / name
                    p.write_bytes(data)
                    refused(self, vd.load(p), want)


class TYaml12(unittest.TestCase):
    def test_numbers_bools_dates(self):
        d = yamlio.parse("a: 6.0e21\nb: 1e-3\nc: no\nd: true\ne: 017\nf: 1_000\ng: 1:30\nh: 0b101\n"
                         "i: 2024-01-01\nj: 0o17\nk: 0x1f\nl: .5\nm: on\n")
        self.assertEqual(d, {"a": 6.0e21, "b": 1e-3, "c": "no", "d": True, "e": 17, "f": "1_000", "g": "1:30",
                             "h": "0b101", "i": "2024-01-01", "j": 15, "k": 31, "l": 0.5, "m": "on"})

    def test_control_pyyaml_11(self):
        # control: PyYAML 1.1 reads each of these differently (R-A1-14, r2 S2-B2)
        d = yaml.safe_load("a: 6.0e21\nc: no\ne: 017\nf: 1_000\ng: 1:30\nh: 0b101\n")
        self.assertEqual(d, {"a": "6.0e21", "c": False, "e": 15, "f": 1000, "g": 90, "h": 5})
        self.assertNotIsInstance(yaml.safe_load("i: 2024-01-01\n")["i"], str)

    def test_duplicate_key_with_line(self):
        text = "name: T\nkind: planet\nname: U\n"
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "dup.yaml"
            p.write_text(text, encoding="utf-8")
            refused(self, vd.load(p), "input.duplicate_key", key="name", line=3)
        self.assertEqual(yaml.safe_load(text)["name"], "U")           # control: PyYAML keeps the last silently


class TKeys(unittest.TestCase):
    def test_unknown_key_with_hint(self):
        refused(self, vd.validate(with_input("potental_temperature", 1600.0)), "input.unknown_key",
                key="potental_temperature", nearest="potential_temperature")

    def test_unknown_key_control(self):
        with mock.patch.object(vd, "_keys", lambda m, allowed, where: None):
            try:
                out = vd.validate(with_input("potental_temperature", 1600.0))
            except Exception:
                out = None
            self.assertFalse(isinstance(out, Refusal) and out.id == "input.unknown_key")

    def test_empty_and_non_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name, text, want in (("e.yaml", "", "input.empty"), ("l.yaml", "- a\n- b\n", "input.not_mapping")):
                p = Path(tmp) / name
                p.write_text(text, encoding="utf-8")
                refused(self, vd.load(p), want)
            refused(self, vd.load(Path(tmp) / "absent.yaml"), "input.unreadable")

    def test_value_less_block(self):
        refused(self, vd.validate(with_input("lid_thickness_km", {"grade": "analog", "source": "s", "note": "n"})),
                "input.value_missing", key="lid_thickness_km")

    def test_block_needs_provenance(self):
        refused(self, vd.validate(with_input("lid_thickness_km", {"value": 100.0})), "input.provenance_missing")
        refused(self, vd.validate(with_input("lid_thickness_km", {"value": 100.0, "grade": "analog", "source": "s"})),
                "input.provenance_missing")

    def test_null_parent_refused(self):
        refused(self, vd.validate(doc(parent=None)), "input.null_value", key="parent")

    def test_units(self):
        refused(self, vd.validate(with_input("potential_temperature", {"value": 1600.0, "unit": "C", **BLOCK})),
                "input.unit_mismatch", expected="K")
        refused(self, vd.validate(with_input("potential_temperature",
                                             {"value": 1600.0, "unit": "Fe#(=100·Fe/(Fe+Mg), 몰비) — 0–100", **BLOCK})),
                "input.unit_mismatch")
        self.assertIsInstance(vd.validate(with_input("potential_temperature", {"value": 1600.0, "unit": "K", **BLOCK})),
                              bd.Body)

    def test_grades(self):
        for g in ("calibrated", "declared-default", 5):
            with self.subTest(grade=g):
                refused(self, vd.validate(with_input("age_gyr", {"value": 4.5, "grade": g, "source": "s", "note": "n"})),
                        "input.not_text" if g == 5 else "input.bad_grade")

    def test_class_out_of_scope(self):
        refused(self, vd.validate(with_input("body_class", "brown_dwarf")), "input.class_out_of_scope",
                body_class="brown_dwarf")

    def test_conductive_needs_surface_temperature(self):
        d = doc()
        del d["inputs"]["surface_temperature_k"]
        d["layers"].append({"id": "lid", "role": "lid", "material": "silicate", "thermal": "conductive",
                            "extent": {"depth_from_surface": 100.0}})
        refused(self, vd.validate(d), "input.cross_field")


class TClosure(unittest.TestCase):
    CORE_FIT = {"id": "core", "role": "core", "material": "fe", "extent": {"mass_fraction": 0.2}, "system": "iron_alloy",
                "composition": {"value": {"S": "fit", "O": 0.04}, "grade": "declared", "source": "s",
                                "counter_evidence_searched": "c"}}

    def _comp(self, name):
        d = doc(layers=[self.CORE_FIT, {"id": "mantle", "role": "mantle", "material": "s"}],
                closure={"kind": "composition", "layer": "core", "name": name})
        d["inputs"]["radius_earth"] = 0.532
        return d

    def test_counts(self):
        refused(self, vd.validate(doc(layers=[self.CORE_FIT, {"id": "mantle", "role": "mantle", "material": "s"}])),
                "input.closure_count", count=2)                                  # R closure + a fit
        b = vd.validate(self._comp("S"))
        self.assertIsInstance(b, bd.Body)
        self.assertEqual((b.closure.lo, b.closure.hi), (0.13, 0.25))            # SULPHUR_FIT_BRACKET
        refused(self, vd.validate(self._comp("O")), "input.closure_count")      # closure on O while S is fit (S2-B3 a)
        d = doc(closure={"kind": "composition", "layer": "core", "name": "S"})
        d["inputs"]["radius_earth"] = 0.532
        refused(self, vd.validate(d), "input.closure_count", count=0)            # nothing marked fit
        refused(self, vd.validate(doc(layers=[self.CORE_FIT, {"id": "mantle", "role": "mantle", "material": "s"}],
                                      closure={"kind": "composition", "layer": "core", "name": "S"})),
                "input.cross_field")                                            # inverse needs radius

    def test_porosity_axis_in_params(self):
        d = doc(layers=[{"id": "rock", "role": "mantle", "material": "silicate",
                         "params": {"initial_porosity": "fit"}}],
                closure={"kind": "composition", "layer": "rock", "name": "initial_porosity"})
        d["inputs"]["radius_earth"] = 0.08
        b = vd.validate(d)
        self.assertIsInstance(b, bd.Body)
        self.assertEqual((b.closure.lo, b.closure.hi), (0.0, 0.6))

    def test_boundary_mass(self):
        d = doc(layers=[{"id": "core", "role": "core", "material": "fe"}, {"id": "mantle", "role": "mantle", "material": "s"}],
                closure={"kind": "boundary_mass", "layer": "core"})
        d["inputs"]["radius_earth"] = 0.95
        b = vd.validate(d)
        self.assertIsInstance(b, bd.Body)
        self.assertEqual(b.radius.value, 0.95 * 6.371e6)
        d["layers"][1]["extent"] = {"mass_fraction": 0.7}                       # the core's mass is fixed (S2-B3 b)
        refused(self, vd.validate(d), "input.closure_count", count=0)

    def test_ranges(self):
        refused(self, vd.validate(doc(closure={"kind": "R", "lo": -1.0, "hi": 2.0})), "input.out_of_domain")
        refused(self, vd.validate(doc(closure={"kind": "R", "lo": 2.0, "hi": 1.0})), "input.cross_field")


class TLayersThroughValidate(unittest.TestCase):
    def test_ten_layers(self):
        roles = ["core.inner", "core.outer", "basal_layer", "mantle", "mantle", "crust", "ice", "ocean", "ice", "envelope"]
        layers = [{"id": f"l{i}", "role": r, "material": "m", "extent": {"mass_fraction": 0.1}} for i, r in enumerate(roles)]
        layers[3].pop("extent")
        b = vd.validate(doc(layers=layers))
        self.assertIsInstance(b, bd.Body)
        self.assertEqual(len(b.boundaries), 9)
        self.assertEqual(b.interface("icb").name, "l0/l1")
        self.assertEqual(b.interface("cmb").name, "l1/l2")

    def test_two_core(self):
        b = vd.validate(doc(layers=[{"id": "ic", "role": "core.inner", "material": "fe", "extent": {"radius_from_centre": 1220.0}},
                                    {"id": "oc", "role": "core.outer", "material": "fe", "extent": {"radius_from_centre": 3480.0}},
                                    {"id": "m", "role": "mantle", "material": "s"}]))
        self.assertIsInstance(b, bd.Body)
        self.assertEqual(b.interface("cmb").name, "oc/m")
        self.assertEqual(b.layers[0].extent.value, 1220.0e3)

    def test_layer_rules(self):
        refused(self, vd.validate(doc(layers=[{"id": "m", "role": "mantle", "material": "s", "extent": {"mass_fraction": 0.7}},
                                              {"id": "c", "role": "core", "material": "fe"}])), "input.layer_order")
        refused(self, vd.validate(doc(layers=[{"id": "c", "role": "core", "material": "fe"},
                                              {"id": "m", "role": "mantle", "material": "s"}])), "input.extent_invalid")
        refused(self, vd.validate(doc(layers=[{"id": "c", "role": "core", "material": "fe", "extent": {"mass_fraction": 0.6}},
                                              {"id": "m", "role": "mantle", "material": "s", "extent": {"mass_fraction": 0.6}}])),
                "input.mass_fraction_sum")
        refused(self, vd.validate(doc(layers=[{"id": "c", "role": "rock", "material": "fe"}])), "input.unknown_role",
                role="rock")
        refused(self, vd.validate(doc(jumps={"core/crust": 100.0})), "input.jump_boundary")
        d = doc(layers=[{"id": "core", "role": "core", "material": "fe", "extent": {"mass_fraction": 0.2}},
                        {"id": "mantle", "role": "mantle", "material": "s", "extent": {"mass_fraction": 0.7}},
                        {"id": "crust", "role": "crust", "material": "c",
                         "extent": {"thickness_above": {"layer": "mantle", "km": 40.0}}}])
        refused(self, vd.validate(d), "input.thickness_above_pattern", layer_id="crust")

    def test_extent_keeps_provenance(self):
        d = doc()
        d["layers"].append({"id": "lid", "role": "lid", "material": "silicate", "thermal": "conductive",
                            "extent": {"depth_from_surface": {"value": 135.0, "grade": "analog", "source": "2018JGRB",
                                                              "counter_evidence_searched": "c",
                                                              "uncertainty": 30.0, "uncertainty_basis": "±"}}})
        b = vd.validate(d)
        ext = b.layers[-1].extent
        self.assertEqual(ext.value, 135.0e3)
        self.assertEqual((ext.declared.grade, ext.declared.uncertainty), ("analog", 30.0))

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


class TCrossField(unittest.TestCase):
    """r2 S2-B6: D-A7-5 rules."""

    def test_jump_alias_and_id(self):
        refused(self, vd.validate(doc(jumps={"cmb": 10.0, "core/mantle": 20.0})), "input.cross_field")

    def test_radiogenic_declared_needs_override(self):
        rec = {"U_ppb": 20.0, "Th_ppb": 80.0, "K_ppm": 200.0, "grade": "declared", "source": "s"}
        refused(self, vd.validate(with_input("radiogenic_concentration", rec)), "input.cross_field")
        rec["override"] = {"reason": "r", "window": "inside"}
        self.assertIsInstance(vd.validate(with_input("radiogenic_concentration", rec)), bd.Body)

    def test_contested_pairing_and_extra_kept(self):
        reg = {"value": "stagnant", "grade": "declared", "source": "s", "note": "n"}
        refused(self, vd.validate(with_input("tectonic_regime", {**reg, "contested": True})), "input.cross_field")
        refused(self, vd.validate(with_input("tectonic_regime", {**reg, "contested": []})), "input.cross_field")
        b = vd.validate(with_input("tectonic_regime", {**reg, "contested": ["A 2020", "B 2021"], "setting_override": "x"}))
        self.assertEqual(b.declarations["tectonic_regime"].extra["contested"], ("A 2020", "B 2021"))
        self.assertEqual(b.declarations["tectonic_regime"].extra["setting_override"], "x")


class TLoadAll(unittest.TestCase):
    def test_isolates_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "a.yaml"
            good.write_text(yaml.safe_dump(doc()), encoding="utf-8")
            bad = Path(tmp) / "b.yaml"
            bad.write_text("", encoding="utf-8")
            out = vd.load_all([good, bad])
            self.assertIsInstance(out[str(good)], bd.Body)
            refused(self, out[str(bad)], "input.empty")
            twin = Path(tmp) / "c.yaml"
            twin.write_text(yaml.safe_dump(doc()), encoding="utf-8")
            out = vd.load_all([good, twin])
            refused(self, out[str(good)], "input.duplicate_name", name="T")


if __name__ == "__main__":
    unittest.main()
