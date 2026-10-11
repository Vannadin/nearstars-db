# 사후 검토 수정 A6 3묶음 시험 — 0 범위 · 닫힌 params 어휘 · 경계 출처 하나 · 외피는 물질로 · 운영 로드의 Materials (설계 노트 14 · 14a · 14b)
"""Post-phase-1 review fix plan A6, batch 3 (c8): phase-1 design post-freeze notes 14, 14a, 14b.
Each refusal is planted and fails at engine/rewrite-p2 3fd0e147; each has a control.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_fix_a6_b3
"""
import ast
import copy
import glob
import tempfile
import unittest
from pathlib import Path

import yaml

from solver import body as bd
from solver import from_v1
from solver import legacy_materials as lm
from solver import validate as vd
from solver.result import Refusal
from solver.tests.test_validate import BASE, refused

ROOT = Path(__file__).resolve().parents[2]
TRIO = {"grade": "analog", "source": "s", "counter_evidence_searched": "c"}


def doc(**patch):
    d = copy.deepcopy(BASE)
    d.update(copy.deepcopy(patch))
    return d


def blk(v, **kw):
    return {"value": v, **TRIO, **kw}


class ZeroExtent(unittest.TestCase):
    """Note 14 item 1. A zero mass-fraction layer, and a remainder left at 0, are refused by name. Control: a
    non-zero layer loads. v1's R-BL-7 zero basal thickness is omitted by from_v1 with a v1 note."""

    def test_zero_remainder(self):
        d = doc(layers=[{"id": "core", "role": "core", "material": "fe_prem", "extent": {"mass_fraction": 0.4}},
                        {"id": "mantle", "role": "mantle", "material": "silicate", "extent": {"mass_fraction": 0.6}},
                        {"id": "crust", "role": "crust", "material": "silicate"}])
        refused(self, vd.validate(d), "input.zero_extent", layer_id="crust")

    def test_control_nonzero(self):
        d = doc(layers=[{"id": "core", "role": "core", "material": "fe_prem", "extent": {"mass_fraction": 0.4}},
                        {"id": "mantle", "role": "mantle", "material": "silicate", "extent": {"mass_fraction": 0.5}},
                        {"id": "crust", "role": "crust", "material": "silicate"}])
        self.assertIsInstance(vd.validate(d), bd.Body)

    def test_v1_zero_basal_omitted(self):
        text = (ROOT / "engine/bodies/mars.yaml").read_text(encoding="utf-8")
        raw = yaml.safe_load(text)
        raw.setdefault("inputs", {})["basal_layer_thickness_km"]["value"] = 0.0
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "mars0.yaml"
            p.write_text(yaml.safe_dump(raw, allow_unicode=True), encoding="utf-8")
            body, _ = from_v1.load_v1(str(p))
        self.assertIsInstance(body, bd.Body, getattr(body, "text", ""))
        self.assertEqual([l.id for l in body.layers], ["core", "mantle"])
        self.assertTrue(any(n.kind == "v1_field_dropped" and "basal_layer_thickness_km" in n.text for n in body.notes))


class LayerParams(unittest.TestCase):
    """Note 14 item 2 and 14a. A closed params vocabulary with units, domains and allowed materials."""

    def _rock(self, params, material="silicate"):
        d = doc()
        d["layers"][1] = {"id": "mantle", "role": "mantle", "material": material, "params": params}
        return vd.validate(d)

    def test_typo_refused(self):
        refused(self, self._rock({"initial_porosity": blk(0.3), "porosity_pcap": blk(1.5e8)}), "input.unknown_key",
                nearest="porosity_p_cap")

    def test_old_name_refused(self):
        refused(self, self._rock({"porosity_phi0": blk(0.3)}), "input.unknown_key", nearest="initial_porosity")

    def test_not_for_material(self):
        refused(self, self._rock({"density": blk(4050.0)}), "input.param_not_for_material", key="density")

    def test_density_unit_guard(self):
        d = doc()
        d["layers"].insert(1, {"id": "basal", "role": "basal_layer", "material": "silicate_basal_const",
                               "extent": {"radius_from_centre": 3700.0}, "params": {"density": blk(4.05)}})
        d["layers"][0]["extent"] = {"radius_from_centre": 3480.0}
        refused(self, vd.validate(d), "input.out_of_domain")

    def test_p_cap_needs_porosity(self):
        refused(self, self._rock({"porosity_p_cap": blk(1.5e8)}), "input.cross_field")

    def test_control_declared_porosity_reaches_the_view(self):
        body = self._rock({"initial_porosity": blk(0.3), "porosity_p_cap": blk(1.5e8)})
        self.assertIsInstance(body, bd.Body, getattr(body, "text", ""))
        view = lm.resolve(body.layers[1], 1600.0, 0.0)
        self.assertEqual((view.phi0, view.p_cap), (0.3, 1.5e8))

    def test_basal_thickness_consistent(self):
        d = doc()
        d["layers"] = [{"id": "core", "role": "core", "material": "fe_prem", "extent": {"radius_from_centre": 1695.0}},
                       {"id": "basal", "role": "basal_layer", "material": "silicate_basal_const",
                        "extent": {"radius_from_centre": 1845.0},
                        "params": {"density": blk(4050.0), "thickness_km": blk(200.0)}},
                       {"id": "mantle", "role": "mantle", "material": "silicate"}]
        refused(self, vd.validate(d), "input.cross_field", rule="basal_thickness_consistent")
        d["layers"][1]["params"]["thickness_km"] = blk(150.0)                # control
        self.assertIsInstance(vd.validate(d), bd.Body)

    def test_every_from_v1_params_key_is_in_the_vocabulary(self):
        """14a's class fix: every literal params key from_v1 can write is in layer_params."""
        tree = ast.parse((ROOT / "solver/from_v1.py").read_text(encoding="utf-8"))
        keys = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                for k, v in zip(node.keys, node.values):
                    if isinstance(k, ast.Constant) and k.value == "params" and isinstance(v, ast.Dict):
                        keys |= {kk.value for kk in v.keys if isinstance(kk, ast.Constant)}
        self.assertTrue(keys)
        self.assertLessEqual(keys, set(vd.SCHEMA["layer_params"]), keys - set(vd.SCHEMA["layer_params"]))


class ExtentsDetermined(unittest.TestCase):
    """Note 14 item 3 (14b). One source per interface; the top radius refused; monotone declarations."""

    def _layers(self, *layers):
        return vd.validate(doc(layers=list(layers)))

    def test_radius_plus_mass(self):
        refused(self, self._layers({"id": "core", "role": "core", "material": "fe_prem",
                                    "extent": {"radius_from_centre": 3480.0}},
                                   {"id": "mantle", "role": "mantle", "material": "silicate",
                                    "extent": {"mass_fraction": 0.675}}),
                "input.extent_overdetermined")

    def test_top_radius(self):
        refused(self, self._layers({"id": "core", "role": "core", "material": "fe_prem",
                                    "extent": {"mass_fraction": 0.325}},
                                   {"id": "mantle", "role": "mantle", "material": "silicate",
                                    "extent": {"radius_from_centre": 6371.0}}),
                "input.extent_overdetermined", interface="surface")

    def test_mass_plus_depth(self):
        refused(self, self._layers({"id": "core", "role": "core", "material": "fe_prem",
                                    "extent": {"mass_fraction": 0.3}},
                                   {"id": "mantle", "role": "mantle", "material": "silicate",
                                    "extent": {"depth_from_surface": 2900.0}},
                                   {"id": "crust", "role": "crust", "material": "silicate",
                                    "extent": {"depth_from_surface": 30.0}}),
                "input.extent_overdetermined", interface="core/mantle")

    def test_radii_not_monotone(self):
        refused(self, self._layers({"id": "core", "role": "core", "material": "fe_prem",
                                    "extent": {"radius_from_centre": 1845.0}},
                                   {"id": "basal", "role": "basal_layer", "material": "silicate",
                                    "extent": {"radius_from_centre": 1695.0}},
                                   {"id": "mantle", "role": "mantle", "material": "silicate"}),
                "input.extent_order")

    def test_control_basal_pattern(self):
        """14b: core mass + basal thickness_above is one source per interface, not two."""
        got = self._layers({"id": "core", "role": "core", "material": "fe_prem", "extent": {"mass_fraction": 0.2}},
                           {"id": "basal", "role": "basal_layer", "material": "silicate",
                            "extent": {"thickness_above": {"layer": "core", "km": 150.0}}},
                           {"id": "mantle", "role": "mantle", "material": "silicate"})
        self.assertIsInstance(got, bd.Body, getattr(got, "text", ""))


class EnvelopeByMaterial(unittest.TestCase):
    """Note 14 item 4: through the production loads. (i) H-He under rock via validate.load on a v2 file;
    (ii) role envelope on fe_prem; (iii) the v1 gas giant still refuses; (iv) `known` fires through load_v1."""

    def _load_v2(self, d):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "b.yaml"
            p.write_text(yaml.safe_dump(d), encoding="utf-8")
            return vd.load(str(p))

    def test_h_he_under_rock(self):
        d = doc(layers=[{"id": "core", "role": "core", "material": "fe_prem", "extent": {"mass_fraction": 0.3}},
                        {"id": "gas", "role": "mantle", "material": "h_he", "extent": {"mass_fraction": 0.1}},
                        {"id": "rock", "role": "crust", "material": "silicate"}])
        refused(self, self._load_v2(d), "input.role_material_class", layer_id="gas")
        refused(self, vd.validate(d, materials=lm.LegacyMaterials()), "input.role_material_class")
        self.assertIsInstance(vd.validate(d), bd.Body)       # the raw entry has no Materials: why the default exists

    def test_envelope_role_on_iron(self):
        d = doc(layers=[{"id": "core", "role": "core", "material": "fe_prem", "extent": {"mass_fraction": 0.3}},
                        {"id": "mantle", "role": "mantle", "material": "silicate", "extent": {"mass_fraction": 0.6}},
                        {"id": "env", "role": "envelope", "material": "fe_prem"}])
        refused(self, self._load_v2(d), "input.role_material_class", layer_id="env")

    def test_control_envelope_outermost(self):
        d = doc(layers=[{"id": "core", "role": "core", "material": "fe_prem", "extent": {"mass_fraction": 0.3}},
                        {"id": "mantle", "role": "mantle", "material": "silicate", "extent": {"mass_fraction": 0.6}},
                        {"id": "env", "role": "envelope", "material": "h_he"}])
        self.assertIsInstance(self._load_v2(d), bd.Body)

    def test_v1_gas_giant_refuses(self):
        raw = yaml.safe_load((ROOT / "engine/bodies/earth.yaml").read_text(encoding="utf-8"))
        raw["inputs"]["composition_intent"] = "gas_giant"
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "g.yaml"
            p.write_text(yaml.safe_dump(raw, allow_unicode=True), encoding="utf-8")
            out, _ = from_v1.load_v1(str(p))
        self.assertIsInstance(out, Refusal)

    def test_unknown_material_through_load_v1(self):
        d = doc(layers=[{"id": "core", "role": "core", "material": "fe_prem", "extent": {"mass_fraction": 0.3}},
                        {"id": "mantle", "role": "mantle", "material": "unobtainium"}])
        refused(self, self._load_v2(d), "input.unknown_material", material="unobtainium")


class ShippedV1Unchanged(unittest.TestCase):
    """Notes 14/14a acceptance and r2's condition 1 on A6 rev 2: all 8 shipped v1 files load as before under the
    production Materials, the three refusing ones keep their refusal ids."""

    WANT = {"alpha_centauri_a_b.yaml": "input.composition_undeclared", "luhman_16_a.yaml": "input.class_out_of_scope",
            "luhman_16_b.yaml": "input.class_out_of_scope"}

    def test_all_eight(self):
        files = sorted(glob.glob(str(ROOT / "engine/bodies/*.yaml")))
        self.assertEqual(len(files), 8)
        for f in files:
            name = Path(f).name
            with self.subTest(file=name):
                new, _ = from_v1.load_v1(f)
                old, _ = from_v1.load_v1(f, materials=None)
                if name in self.WANT:
                    self.assertEqual((new.id, old.id), (self.WANT[name], self.WANT[name]))
                else:
                    self.assertIsInstance(new, bd.Body, getattr(new, "text", ""))
                    self.assertEqual(repr(new), repr(old))


if __name__ == "__main__":
    unittest.main()
