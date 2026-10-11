# 사후 검토 수정 B4 (입력층 시험, c8) — G4-T-01~11: 지키는 줄 하나하나에 실패할 수 있는 시험과 대조를 심는다
"""Post-phase-1 review fix plan B4 (c8 writes; b9 re-verified): P1R-G4-T-01 … G4-T-11. Each test plants the input
that the named guard line refuses, so deleting that line fails it. Test-only: no solver code changes.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_b4_input
"""
import copy
import math
import subprocess
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import yaml

from solver import body as bd
from solver import from_v1 as fv
from solver import validate as vd
from solver.result import Refusal
from solver.tests.test_validate import BASE, refused

ROOT = Path(__file__).resolve().parents[2]
TRIO = {"grade": "analog", "source": "s", "counter_evidence_searched": "c"}


def v1(name):
    return yaml.safe_load((ROOT / "engine/bodies" / f"{name}.yaml").read_text(encoding="utf-8"))


def doc(**patch):
    d = copy.deepcopy(BASE)
    d.update(copy.deepcopy(patch))
    return d


class T01DeclaredIce(unittest.TestCase):
    """from_v1.py's declared-branch ice guard: an ice fraction on a declared body is refused, not dropped."""

    def test_refused(self):
        d = v1("earth")
        d["inputs"]["ice_mass_fraction"] = 0.1
        out = fv.from_v1(d)
        refused(self, out, "input.v1_unmapped", key="ice_mass_fraction")

    def test_control_zero_ice(self):
        d = v1("earth")
        d["inputs"]["ice_mass_fraction"] = 0.0
        self.assertNotIsInstance(fv.from_v1(d), Refusal)


class T02PresetOverride(unittest.TestCase):
    """R-PO-1..3: a declared core fraction or material that differs from the preset wins, with its note."""

    def test_core_fraction_and_material(self):
        d = v1("earth")
        d["inputs"]["core_mass_fraction"] = 0.30
        d["inputs"]["core_material"] = "fe_eps"
        raw, notes, _ = fv.from_v1(d)
        core = raw["layers"][0]
        self.assertEqual((core["extent"], core["material"]), ({"mass_fraction": 0.30}, "fe_eps"))
        self.assertEqual(sum(n.kind == "preset_override" for n in notes), 2)

    def test_control_preset_values(self):
        raw, notes, _ = fv.from_v1(v1("earth"))
        self.assertEqual(raw["layers"][0]["extent"], {"mass_fraction": 0.325})
        self.assertFalse(any(n.kind == "preset_override" for n in notes))


class T03LidOnInversionV1(unittest.TestCase):
    """from_v1's R-LITHO-6 guard: a lid on an inversion body is refused through phase 1 (owner Q3)."""

    def test_venus_with_lid(self):
        d = v1("venus")
        d["inputs"]["lithosphere_thickness_km"] = {"value": 100.0, **TRIO}
        d.setdefault("units", {})["lithosphere_thickness_km"] = "km"
        refused(self, fv.from_v1(d), "input.v1_unmapped", key="lithosphere_thickness_km")


class T04Vocabularies(unittest.TestCase):
    """`input.not_in_vocabulary`, `input.not_boolean`, `input.duplicate_layer_id`, each planted."""

    def test_closure_kind_word(self):
        refused(self, vd.validate(doc(closure={"kind": "radius"})), "input.not_in_vocabulary")

    def test_thermal_word(self):
        d = doc()
        d["layers"][1]["thermal"] = "convective"
        refused(self, vd.validate(d), "input.not_in_vocabulary")

    def test_not_boolean(self):
        d = doc()
        d["inputs"]["tidal_heating"] = "yes"
        refused(self, vd.validate(d), "input.not_boolean")

    def test_duplicate_layer_id(self):
        d = doc()
        d["layers"][1]["id"] = "core"
        refused(self, vd.validate(d), "input.duplicate_layer_id")


class T05BoundaryTableIndependent(unittest.TestCase):
    """A boundary table written here, not derived from the schema it tests, including the upper bounds; and the
    data files pinned by blob, so an edit to a domain or an order rule fails until this test is updated on purpose."""

    TABLE = [  # (input key, a value just inside, a value just outside)
        ("mass_earth", 1e-6, 0.0), ("potential_temperature", 1.0, 0.0), ("surface_pressure_pa", 0.0, -1.0),
        ("basal_iron_number", 100.0, 100.5), ("eccentricity", 0.99, 1.0), ("eccentricity_forced", 0.0, 1.0),
    ]
    PINS = {"schema.yaml": "f33d84cee6fd0226d5fa08693b8560dbcfe957b9",
            "roles.yaml": "7c7796d359b86112db75c4745ba849dd3a9d268a",
            "presets.yaml": "c2c366ccb236941452fcf93a13fc14f17007f8ef"}

    def test_table(self):
        for key, ok, bad in self.TABLE:
            with self.subTest(key=key, value=bad):
                d = doc()
                d["inputs"][key] = bad
                refused(self, vd.validate(d), "input.out_of_domain")
            with self.subTest(key=key, value=ok):
                d = doc()
                d["inputs"][key] = ok
                self.assertIsInstance(vd.validate(d), bd.Body)

    def test_mass_fraction_upper(self):
        d = doc()
        d["layers"][0]["extent"] = {"mass_fraction": 1.0 + 1e-6}
        refused(self, vd.validate(d), "input.out_of_domain")

    def test_data_files_pinned(self):
        for name, blob in self.PINS.items():
            with self.subTest(file=name):
                got = subprocess.run(["git", "hash-object", str(ROOT / "solver/data" / name)], capture_output=True,
                                     text=True, check=True).stdout.strip()
                self.assertEqual(got, blob, f"{name} changed: update this pin on purpose, with the rule it moves")


class T06TrioRefused(unittest.TestCase):
    """R-A1-12's trio, in the refusing direction, on a composition and a params block."""

    def test_composition_without_counter_evidence(self):
        d = doc()
        d["layers"][0] = {"id": "core", "role": "core", "material": "fe_core_light", "system": "iron_alloy",
                          "extent": {"mass_fraction": 0.25},
                          "composition": {"value": {"S": 0.15, "O": 0.04, "C": 0.014}, "grade": "analog",
                                          "source": "s"}}
        refused(self, vd.validate(d), "input.provenance_missing")

    def test_params_without_counter_evidence(self):
        d = doc()
        d["layers"][1]["params"] = {"initial_porosity": {"value": 0.3, "grade": "analog", "source": "s"}}
        refused(self, vd.validate(d), "input.provenance_missing")


class T07MassFractionSums(unittest.TestCase):
    """The two sum clauses, each the line that refuses, and the tolerance edge."""

    def _layers(self, *fr, remainder=False):
        out = [{"id": f"l{i}", "role": "core" if i == 0 else "mantle", "material": "fe_prem" if i == 0 else "silicate",
                "extent": {"mass_fraction": f}} for i, f in enumerate(fr)]
        if remainder:
            out.append({"id": "rest", "role": "crust", "material": "silicate"})
        return vd.validate(doc(layers=out))

    def test_all_fractions_below_one(self):
        refused(self, self._layers(0.3, 0.6), "input.mass_fraction_sum")

    def test_over_one_with_a_remainder(self):
        refused(self, self._layers(0.5, 0.6, remainder=True), "input.mass_fraction_sum")

    def test_tolerance_edge(self):
        tol = vd.SCHEMA["tolerances"]["mass_fraction_sum"]
        self.assertIsInstance(self._layers(0.325, 0.675 + 0.5 * tol), bd.Body)
        refused(self, self._layers(0.325, 0.675 + 3 * tol), "input.mass_fraction_sum")


class T08SurfacePressure(unittest.TestCase):
    """A declared surface pressure is read back with its source word."""

    def test_declared(self):
        d = doc()
        d["inputs"]["surface_pressure_pa"] = 9.2e6
        body = vd.validate(d)
        self.assertEqual((body.surface.p_s, body.surface.p_s_source), (9.2e6, "declared"))

    def test_control_floor(self):
        body = vd.validate(doc())
        self.assertEqual((body.surface.p_s, body.surface.p_s_source), (None, "material_floor"))


class T09PreChecks(unittest.TestCase):
    """The six pre-checks that keep validate from raising: each refuses by name (not just «some refusal»)."""

    def test_band_lo_above_hi(self):
        d = doc()
        d["inputs"]["potential_temperature"] = {"value": 1600.0, **TRIO, "band": {"lo": 1700.0, "hi": 1500.0}}
        refused(self, vd.validate(d), "input.cross_field", rule="band lo ≤ hi")

    def test_isothermal_without_t(self):
        d = doc()
        d["layers"][1]["thermal"] = "isothermal"
        refused(self, vd.validate(d), "input.cross_field", rule="t_declared goes with thermal isothermal")

    def test_composition_without_system(self):
        d = doc()
        d["layers"][0] = {"id": "core", "role": "core", "material": "fe_core_light", "extent": {"mass_fraction": 0.3},
                          "composition": {"value": {"S": 0.15, "O": 0.04, "C": 0.014}, **TRIO}}
        refused(self, vd.validate(d), "input.cross_field", rule="composition needs a system (R-LAYERGEN-1)")

    def test_closure_layer_not_in_list(self):
        d = doc(closure={"kind": "boundary_mass", "layer": "ice"})
        d["inputs"]["radius_earth"] = 1.0
        refused(self, vd.validate(d), "input.cross_field", rule="closure names a layer of the list")

    def test_boundary_mass_layer_with_extent(self):
        d = doc(closure={"kind": "boundary_mass", "layer": "core"})
        d["inputs"]["radius_earth"] = 1.0
        refused(self, vd.validate(d), "input.cross_field", rule="boundary_mass solves a layer declared without extent")


class T10Controls(unittest.TestCase):
    """The date control on a complete document, and the finiteness control on a slot with no domain."""

    def test_date_is_a_string(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "b.yaml"
            text = yaml.safe_dump(doc()).replace("name: T", "name: 2024-13-45")
            p.write_text(text, encoding="utf-8")
            body = vd.load(str(p), materials=None)
        self.assertIsInstance(body, bd.Body, getattr(body, "text", ""))
        self.assertEqual(body.name, "2024-13-45")

    def test_finiteness_on_a_domainless_slot(self):
        d = doc()
        d["inputs"]["potential_temperature"] = {"value": 1600.0, **TRIO, "band": {"lo": math.nan, "hi": 1700.0}}
        refused(self, vd.validate(d), "input.non_finite")
        # control: with validate's finiteness check neutralised, the NaN reaches Declared's own check and raises,
        # so it is validate's line that keeps «never raises» on this domainless slot (lesson 1: it can fire)
        with mock.patch.object(vd, "math", types.SimpleNamespace(isfinite=lambda x: True, fsum=math.fsum)):
            with self.assertRaises(ValueError):
                vd.validate(d)


class T11FromV1(unittest.TestCase):
    """from_v1's layer-key units, the parent rules, the unknown top-level section, and load_v1's error handlers."""

    def test_layer_key_unit(self):
        d = v1("mars")
        d["units"]["core_plus_layer_radius_km"] = "m"
        refused(self, fv.from_v1(d), "input.unit_mismatch")

    def test_null_parent_note(self):
        d = v1("earth")
        d["parent"] = None
        _raw, notes, _ = fv.from_v1(d)
        self.assertTrue(any(n.kind == "v1_null_parent" for n in notes))

    def test_parent_copied(self):
        raw, _notes, _ = fv.from_v1(v1("earth"))
        self.assertEqual(raw["parent"], "Sun")

    def test_unknown_top_level(self):
        d = v1("earth")
        d["orbit"] = {"a_au": 1.0}
        self.assertIsInstance(fv.from_v1(d), Refusal)

    def test_load_v1_unreadable(self):
        with tempfile.TemporaryDirectory() as t:
            missing, _ = fv.load_v1(str(Path(t) / "none.yaml"))
            bad = Path(t) / "bad.yaml"
            bad.write_bytes(b"name: \xff\xfe\n")
            not_utf8, _ = fv.load_v1(str(bad))
            broken = Path(t) / "broken.yaml"
            broken.write_text("name: [unclosed\n", encoding="utf-8")
            yaml_err, _ = fv.load_v1(str(broken))
        for out in (missing, not_utf8, yaml_err):
            with self.subTest(out=getattr(out, "evidence", None)):
                refused(self, out, "input.unreadable")


if __name__ == "__main__":
    unittest.main()
