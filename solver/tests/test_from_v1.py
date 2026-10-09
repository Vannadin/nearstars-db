# 옛 천체 파일 변환 시험 — 8 개 몸의 정확한 변환 메모 · 세 거절 · v2 쌍둥이 거절 · 표에 없는 역산 몸 거절 (등록 c8 T-v1, 메모 1)
"""T-v1 of rewrite/phase1-impl-c8.frozen.md as amended by post-freeze note 1, each with its negative control.

Reads the v1 body files at engine/bodies (097a8aa3) as files; the engine is not imported.
Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_from_v1
"""
import copy
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

import yaml

from solver import body as bd
from solver import from_v1 as fv
from solver import validate as vd
from solver.result import Refusal

ROOT = Path(__file__).resolve().parents[2]
BODIES = ROOT / "engine" / "bodies"

#: Note 1 §1: the five bodies that load, with exactly these normalisation notes; the three refusals.
EXPECT_NOTES = {
    "dante_fixture": {"v1_unit_alias": 1, "v1_ice_excluded": 1},
    "earth": {"v1_aside": 1, "v1_lid_layer": 1},
    "mars": {"v1_aside": 2, "v1_unit_alias": 1, "v1_unit_assumed": 1, "v1_fixing_checked": 1,
             "v1_core_radius_derived": 1, "v1_field_dropped": 1, "v1_uncertainty": 1},
    "pandora": {"v1_aside": 2, "v1_unit_alias": 3},
    "venus": {"v1_aside": 2},
}
EXPECT_REFUSALS = {"alpha_centauri_a_b": "input.composition_undeclared",
                   "luhman_16_a": "input.class_out_of_scope", "luhman_16_b": "input.class_out_of_scope"}
#: Note 1 §2: the inversion axis per body (the Mac run at 097a8aa3; re-checked against O1 when the capture lands).
EXPECT_CLOSURE = {"venus": ("boundary_mass", "core", None), "dante_fixture": ("composition", "rock", "initial_porosity"),
                  "mars": ("composition", "core", "S"), "earth": ("R", None, None), "pandora": ("R", None, None)}


def v1(name):
    return yaml.safe_load((BODIES / f"{name}.yaml").read_text(encoding="utf-8"))


class TEightBodies(unittest.TestCase):
    def test_all_eight_files_covered(self):
        self.assertEqual(sorted(p.stem for p in BODIES.glob("*.yaml")), sorted(set(EXPECT_NOTES) | set(EXPECT_REFUSALS)))

    def test_loading_bodies_and_their_notes(self):
        for name, want in EXPECT_NOTES.items():
            with self.subTest(body=name):
                b, aside = fv.load_v1(BODIES / f"{name}.yaml")
                self.assertIsInstance(b, bd.Body, getattr(b, "text", ""))
                self.assertEqual(dict(Counter(n.kind for n in b.notes)), want)
                c = b.closure
                self.assertEqual((c.kind, c.layer, c.name), EXPECT_CLOSURE[name])
                self.assertIn("units", aside)

    def test_refusing_bodies(self):
        for name, want in EXPECT_REFUSALS.items():
            with self.subTest(body=name):
                r, _ = fv.load_v1(BODIES / f"{name}.yaml")
                self.assertIsInstance(r, Refusal)
                self.assertEqual(r.id, want)

    def test_note_fields(self):
        b, _ = fv.load_v1(BODIES / "mars.yaml")
        by = {n.kind: n for n in b.notes}
        self.assertEqual(dict(by["v1_core_radius_derived"].fields), {"r_top_km": 1845.0, "thickness_km": 150.0,
                                                                     "r_core_km": 1695.0})
        self.assertEqual(by["v1_unit_assumed"].fields["key"], "core_cmb_temperature")
        self.assertEqual(by["v1_fixing_checked"].fields["pin"], "box_ceiling")
        self.assertEqual(dict(by["v1_field_dropped"].fields), {"key": "core_light_elements", "field": "fit"})
        b, _ = fv.load_v1(BODIES / "pandora.yaml")
        self.assertEqual(sorted(n.fields["key"] for n in b.notes if n.kind == "v1_unit_alias"),
                         ["eccentricity", "eccentricity_forced", "k2_over_q"])

    def test_simple_layers(self):
        for name in ("venus", "pandora", "earth"):
            b, _ = fv.load_v1(BODIES / f"{name}.yaml")
            with self.subTest(body=name):
                self.assertEqual([(l.id, l.role, l.material) for l in b.layers[:2]],
                                 [("core", "core", "fe_prem"), ("mantle", "mantle", "silicate")])
        b, _ = fv.load_v1(BODIES / "pandora.yaml")
        self.assertEqual(b.layers[0].extent.value, 0.325)
        b, _ = fv.load_v1(BODIES / "earth.yaml")
        self.assertEqual(b.layers[2].material, "silicate")

    def test_mars_layers(self):
        b, _ = fv.load_v1(BODIES / "mars.yaml")
        core, basal, mantle = b.layers
        self.assertEqual(core.extent.value, (1845.0 - 150.0) * 1e3)
        self.assertEqual(basal.extent.value, 1845.0e3)
        self.assertEqual((basal.extent.declared.uncertainty, basal.extent.declared.uncertainty_basis), (25.0, "±"))
        self.assertEqual(dict(core.composition.value), {"S": "fit", "O": 0.04, "C": 0.014})
        self.assertEqual(basal.params["density"].value, 4050.0)
        self.assertEqual(basal.params["thickness_km"].value, 150.0)
        self.assertEqual((mantle.system, mantle.material), ("silicate", fv.MANTLE_DECL_MATERIAL))
        self.assertEqual(b.solver_flags["basal_iron_number"], 75.0)

    def test_earth_lid_keeps_provenance(self):
        b, _ = fv.load_v1(BODIES / "earth.yaml")
        lid = b.layers[-1]
        self.assertEqual((lid.role, lid.thermal, lid.extent.kind), ("lid", "conductive", "depth_from_surface"))
        self.assertEqual(lid.extent.value, 135.0e3)
        self.assertEqual(lid.extent.declared.grade, "analog")
        self.assertEqual(b.surface.t_s, 293.0)

    def test_dante_porosity(self):
        b, _ = fv.load_v1(BODIES / "dante_fixture.yaml")
        (rock,) = b.layers
        self.assertEqual(rock.params["initial_porosity"].value, "fit")
        self.assertEqual(rock.params["porosity_p_cap"].value, 150.0e6)
        self.assertEqual((b.closure.lo, b.closure.hi), (0.0, 0.6))
        self.assertTrue(b.solver_flags["tidal_heating"])


class TRules(unittest.TestCase):
    def test_unknown_inversion_body(self):
        d = v1("venus")
        d["name"] = "Venus (twin)"
        r = fv.from_v1(d)
        self.assertEqual(r.id, "input.v1_unmapped")

    def test_inversion_table_control(self):
        # control: with Venus removed from the table, Venus itself is refused
        with mock.patch.object(fv, "INVERSION_TABLE", {}):
            self.assertEqual(fv.from_v1(v1("venus")).id, "input.v1_unmapped")

    def test_fixing_disagreement(self):
        d = v1("mars")
        d["inputs"]["light_element_fixing"]["value"] = "box_floor"
        self.assertEqual(fv.from_v1(d).id, "input.cross_field")

    def test_unit_mismatch(self):
        d = v1("earth")
        d["units"]["potential_temperature"] = "C"
        self.assertEqual(fv.from_v1(d).id, "input.unit_mismatch")

    def test_unknown_v1_key_goes_to_validate(self):
        d = v1("earth")
        d["inputs"]["potental_temperature"] = 1600.0
        raw, _notes, _aside = fv.from_v1(d)
        self.assertEqual(vd.validate(raw).id, "input.unknown_key")

    def test_unconsumed_layer_key(self):
        d = v1("venus")
        d["inputs"]["mantle_composition"] = {"value": {"SiO2": 45.0}, "grade": "analog", "source": "s",
                                             "counter_evidence_searched": "c"}
        r = fv.from_v1(d)
        self.assertEqual((r.id, r.evidence["key"]), ("input.v1_unmapped", "mantle_composition"))

    def test_malformed_v1_never_raises(self):
        for mutate in (lambda d: d.update(inputs=[1]), lambda d: d.update(units=[1]),
                       lambda d: d["inputs"].update(core_light_elements=5),
                       lambda d: d["inputs"].update(core_plus_layer_radius_km={"value": "x"})):
            d = v1("mars")
            mutate(d)
            self.assertIsInstance(fv.from_v1(d), Refusal)

    def test_layer_keys_match_schema_map(self):
        self.assertEqual(sorted(vd.SCHEMA["v1_layer_keys"]), sorted(fv.LAYER_KEYS))


class TTwins(unittest.TestCase):
    """Every normalisation from_v1 makes has a v2 twin that validate refuses by name (D-A2-7)."""

    def _earth_raw(self):
        raw, _n, _a = fv.from_v1(v1("earth"))
        return copy.deepcopy(raw)

    def test_twins(self):
        cases = []
        r = self._earth_raw()
        r["parent"] = None
        cases.append(("null parent", r, "input.null_value"))
        r = self._earth_raw()
        r["inputs"]["k2_over_q"] = {"value": 0.1, "unit": "dimensionless", "grade": "analog", "source": "s", "note": "n"}
        cases.append(("unit alias", r, "input.unit_mismatch"))
        r = self._earth_raw()
        r["inputs"]["basal_iron_number"] = {"value": 75.0, "unit": "Fe#(=100·Fe/(Fe+Mg), 몰비) — 0–100 이지 0–1 이 아니다",
                                            "grade": "analog", "source": "s", "note": "n"}
        cases.append(("prose unit", r, "input.unit_mismatch"))
        r = self._earth_raw()
        r["layers"][2]["extent"]["depth_from_surface"]["uncertainty_km"] = 30.0
        cases.append(("uncertainty_km", r, "input.unknown_key"))
        r = self._earth_raw()
        r["inputs"]["light_element_fixing"] = {"value": "box_ceiling", "grade": "declared", "source": "s", "note": "n"}
        cases.append(("v1-only key", r, "input.unknown_key"))
        r = self._earth_raw()
        r["expected"] = {}
        cases.append(("expected section", r, "input.unknown_key"))
        r = self._earth_raw()
        r["inputs"]["ice_mass_fraction"] = 0.0
        cases.append(("ice_mass_fraction input", r, "input.unknown_key"))
        raw, _n, _a = fv.from_v1(v1("mars"))
        raw = copy.deepcopy(raw)
        raw["layers"][0]["composition"]["fit"] = True
        cases.append(("composition fit field", raw, "input.unknown_key"))
        for label, raw, want in cases:
            with self.subTest(twin=label):
                out = vd.validate(raw)
                self.assertIsInstance(out, Refusal, label)
                self.assertEqual(out.id, want, out.text)

    def test_twin_control(self):
        # control: the converted (normalised) Earth itself loads
        self.assertIsInstance(vd.validate(self._earth_raw()), bd.Body)


if __name__ == "__main__":
    unittest.main()
