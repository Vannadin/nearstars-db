# 사후 검토 수정 A6 2묶음 시험 — 쓰이지 않는 조성 거절, 조성 맞춤 축 ≤ 1, 덮개 바닥 온도 도약 거절, v1 중복 키 거절과 YAML 1.1 동등성
"""Post-phase-1 review fix plan A6, batch 2 (c8): P1R-G4-C-01, G4-C-03, G4-C-09 (+ G2-R-11's shared id), G4-R-05.
Each test fails at engine/rewrite-p2 dc8d69ad and has a control.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_fix_a6
"""
import copy
import glob
import tempfile
import unittest
from pathlib import Path

import yaml

from solver import from_v1
from solver import solve as sv
from solver import validate as vd
from solver.result import Refusal
from solver.tests.test_validate import BASE, refused

ROOT = Path(__file__).resolve().parents[2]
BLOCK = {"grade": "analog", "source": "s", "counter_evidence_searched": "c"}
OXIDES = {"SiO2": 45.0, "Al2O3": 4.45, "FeO": 8.05, "MgO": 37.8, "CaO": 3.55, "Na2O": 0.36}


def doc(**patch):
    d = copy.deepcopy(BASE)
    d.update(copy.deepcopy(patch))
    return d


class CompositionNotConsumed(unittest.TestCase):
    """G4-C-01: a composition on a legacy id the adapter builds without one is refused by name, not silently
    ignored. Control: the same layer without the composition builds its view."""

    def _views(self, mantle):
        d = doc()
        d["layers"][1] = mantle
        body = vd.validate(d)
        self.assertNotIsInstance(body, Refusal, getattr(body, "text", ""))
        return sv._views(body)

    def test_refused(self):
        got = self._views({"id": "mantle", "role": "mantle", "material": "silicate", "system": "silicate",
                           "composition": {"value": OXIDES, "source_kind": "measured", **BLOCK}})
        self.assertIsInstance(got, Refusal)
        self.assertEqual((got.id, got.evidence["rule"]), ("input.cross_field", "composition_not_consumed"))

    def test_control_no_composition(self):
        got = self._views({"id": "mantle", "role": "mantle", "material": "silicate"})
        self.assertNotIsInstance(got, Refusal, getattr(got, "text", ""))


class CompositionAxisIsAFraction(unittest.TestCase):
    """G4-C-03: a composition closure axis lies in [0, 1]; the owner's box written in wt% (13–25) is refused.
    Control: the same closure in mass fractions loads."""

    def _doc(self, lo, hi):
        d = doc()
        d["inputs"]["radius_earth"] = 0.532
        d["layers"][0] = {"id": "core", "role": "core", "material": "fe_core_light", "system": "iron_alloy",
                          "composition": {"value": {"S": "fit", "O": 0.04, "C": 0.014}, **BLOCK},
                          "extent": {"mass_fraction": 0.25}}
        d["closure"] = {"kind": "composition", "layer": "core", "name": "S", "lo": lo, "hi": hi}
        return d

    def test_wt_percent_refused(self):
        refused(self, vd.validate(self._doc(13.0, 25.0)), "input.out_of_domain")

    def test_control_fraction(self):
        self.assertNotIsInstance(vd.validate(self._doc(0.13, 0.25)), Refusal)


class JumpAtLithosphere(unittest.TestCase):
    """G4-C-09 + G2-R-11 (one id, agreed with 7c): a jump at the conductive lid's base, or on a boundary named
    lithosphere, is refused by name (R-LITHO-7), never applied or dropped silently. Control: a cmb jump loads."""

    def _doc(self, jumps, top_id="lid", thermal="conductive"):
        d = doc()
        d["layers"].append({"id": top_id, "role": "lid", "material": "silicate", "thermal": thermal,
                            "extent": {"depth_from_surface": 100.0}})
        d["jumps"] = jumps
        return d

    def test_lid_base(self):
        refused(self, vd.validate(self._doc({"mantle/lid": 50.0})), "input.jump_at_lithosphere",
                boundary="mantle/lid")

    def test_named_lithosphere(self):
        d = self._doc({"mantle/lithosphere": 50.0}, top_id="lithosphere", thermal="adiabatic")
        del d["layers"][2]["thermal"]
        refused(self, vd.validate(d), "input.jump_at_lithosphere", boundary="mantle/lithosphere")

    def test_control_cmb(self):
        self.assertNotIsInstance(vd.validate(self._doc({"cmb": 50.0})), Refusal)


class V1DuplicateKey(unittest.TestCase):
    """G4-R-05: a repeated key in a v1 file is refused, never last-wins. Control: the shipped file loads."""

    def test_duplicate_refused(self):
        src = (ROOT / "engine/bodies/earth.yaml").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "earth_dup.yaml"
            p.write_text(src + "\nname: Earth2\n", encoding="utf-8")
            out, _ = from_v1.load_v1(str(p))
        refused(self, out, "input.duplicate_key", key="name")

    def test_control_shipped(self):
        out, _ = from_v1.load_v1(str(ROOT / "engine/bodies/earth.yaml"))
        self.assertNotIsInstance(out, Refusal, getattr(out, "text", ""))


class V1LoaderParity(unittest.TestCase):
    """r2's condition 2 on the fix plan: the duplicate-key loader keeps v1's YAML 1.1 scalars. Every shipped v1
    file gives the same dict under PyYAML's safe_load and under the new loader."""

    def test_all_shipped_files(self):
        files = sorted(glob.glob(str(ROOT / "engine/bodies/*.yaml")))
        self.assertEqual(len(files), 8)
        for f in files:
            with self.subTest(file=Path(f).name):
                text = Path(f).read_text(encoding="utf-8")
                self.assertEqual(yaml.load(text, Loader=from_v1._V1Loader), yaml.safe_load(text))


if __name__ == "__main__":
    unittest.main()
