# 라이브러리 형식 시험 — 고정(버전 · 트리 해시) 검사, 맞지 않으면 그 기록만 못 씀, 단위 변환, 기록 뷰가 어댑터 값을 그대로 냄 (phase-2 impl note 1 §6)
"""Note 1 §6: the SeaFreeze library form behind its pin.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_material_library
"""
import copy
import importlib.metadata
import tempfile
import unittest
from pathlib import Path

import yaml

from solver import material_library as ml
from solver import material_registry as mr
from solver import material_view as mv
from solver import stepper as st
from solver.tests.test_material_registry import CITE, GOOD, SHA, const


def lib_record(sha=None, version=None, submodel="water1"):
    """GOOD as one library-form phase (SeaFreeze water1) with a window inside the source's printed range."""
    d = copy.deepcopy(GOOD)
    ph = d["phases"][0]
    ph["state"] = "liquid"
    ph["eos"] = {"form": "library", "reference": {"kind": "state", "p": const(0.0, "Pa"), "t": const(273.15, "K")},
                 "library": {"name": "SeaFreeze", "version": version or importlib.metadata.version("SeaFreeze"),
                             "sha256": sha or ml.tree_sha256("SeaFreeze"), "submodel": submodel}}
    ph["window"] = {"p_min": 1.0e5, "p_max": 1.0e9, "t_min": 250.0, "t_max": 350.0}
    ph["field"]["box"] = {"p_min": 1.0e5, "p_max": 1.0e9}
    for k in ("sets", "phase_constants", "gamma_window"):
        ph["thermal"].pop(k, None)
    ph["edges"] = {"t_min": {"refusal": "input.material_out_of_data"}, "t_max": {"refusal": "input.material_out_of_data"}}
    return d


def load(*recs):
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "sources.yaml").write_text(yaml.safe_dump({"sources": [{"sha256": SHA}]}), encoding="utf-8")
        for r in recs:
            Path(tmp, f"{r['id']}.yaml").write_text(yaml.safe_dump(r, sort_keys=False), encoding="utf-8")
        return mr.load(Path(tmp))


class Pin(unittest.TestCase):
    def test_tree_sha_is_stable_and_hex(self):
        a, b = ml.tree_sha256("SeaFreeze"), ml.tree_sha256("SeaFreeze")
        self.assertEqual(a, b)
        self.assertRegex(a, r"^[0-9a-f]{64}$")

    def test_pin_ok_and_each_mismatch(self):
        good = lib_record()["phases"][0]["eos"]["library"]
        self.assertIsNone(ml.check_pin(good))
        for change, word in (({"version": "0.9.0"}, "pins"), ({"sha256": "0" * 64}, "differs"),
                             ({"submodel": "VII_X_French"}, "not one a record may name"),
                             ({"name": "Other"}, "no adapter")):
            with self.subTest(change=change):
                got = ml.check_pin({**good, **change})
                self.assertIsInstance(got, ml.PinStop)
                self.assertIn(word, got.why)

    def test_test_only_submodel(self):
        with self.assertRaises(ValueError):
            ml.SeaFreezePhase("VII_X_French")
        ml.SeaFreezePhase("VII_X_French", test_only=True)


class Units(unittest.TestCase):
    def test_water_at_one_bar_25c(self):
        """ρ of liquid water at 0.1 MPa, 298.15 K is 997.05 kg/m³ (IAPWS-95 reference value); K_T near 2.2 GPa.
        Checks the MPa ↔ Pa conversion at the adapter boundary."""
        got = ml.SeaFreezePhase("water1").at(1.0e5, 298.15)
        self.assertAlmostEqual(got["rho"], 997.05, delta=0.1)
        self.assertGreater(got["k_t"], 2.0e9)
        self.assertLess(got["k_t"], 2.4e9)


class Registry(unittest.TestCase):
    def test_pinned_record_loads_and_its_view_reads_the_library(self):
        reg = load(lib_record())
        self.assertIsInstance(reg, mr.Registry, getattr(reg, "evidence", None))
        self.assertIn("toy", reg.records)
        v = mv.RecordView(lib_record(), 300.0)
        rho, dtdp, _n = v.state(5.0e8, 300.0)
        want = ml.SeaFreezePhase("water1").at(5.0e8, 300.0)
        self.assertEqual((rho, dtdp), (want["rho"], want["dtdp"]))

    def test_mismatched_pin_makes_only_that_record_unavailable(self):
        bad = lib_record(sha="1" * 64)
        other = copy.deepcopy(GOOD)
        other["id"] = "other"
        reg = load(bad, other)
        self.assertIsInstance(reg, mr.Registry)
        self.assertIn("other", reg.records)
        self.assertNotIn("toy", reg.records)
        self.assertEqual(reg.unavailable["toy"].id, "material.library_pin")

    def test_unavailable_record_lookup_gives_the_stop(self):
        """68 N31: asking for an unavailable record returns its LoadStop with fix text."""
        reg = load(lib_record(sha="1" * 64))
        got = reg.get("toy")
        self.assertIsInstance(got, mr.LoadStop)
        self.assertIn("tree_sha256", got.fix)
        self.assertIsNone(reg.get("nonexistent"))

    def test_library_phase_with_thermal_sets_stops(self):
        rec = lib_record()
        rec["phases"][0]["thermal"]["gamma_window"] = {"p_min": 1.0e5, "p_max": 1.0e9}
        self.assertEqual(load(rec).id, "material.kind_rule")

    def test_past_the_library_range_is_a_named_stop(self):
        """68 N28: VI at 5 GPa / 300 K makes SeaFreeze raise; the view gives a named Stop."""
        rec = lib_record(submodel="VI")
        rec["phases"][0]["window"] = {"p_min": 1.0e5, "p_max": 1.0e10, "t_min": 250.0, "t_max": 350.0}
        s = mv.RecordView(rec, 300.0).state(5.0e9, 300.0)
        self.assertIsInstance(s, st.Stop)
        self.assertIn("VI at", s.record.why)

    def test_outside_the_knot_box_before_getprop(self):
        """68 N34: past VI's knot box (3000 MPa) the adapter refuses before calling SeaFreeze."""
        with self.assertRaises(ml.LibraryOutOfRange) as cm:
            ml.SeaFreezePhase("VI").at(3.15e9, 300.0)
        self.assertIn("knot box", str(cm.exception))

    def test_past_the_window_refuses(self):
        s = mv.RecordView(lib_record(), 300.0).state(5.0e8, 400.0)
        self.assertIsInstance(s, st.Stop)


if __name__ == "__main__":
    unittest.main()
