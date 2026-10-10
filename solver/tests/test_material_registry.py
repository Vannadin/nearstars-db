# 물질 등록부 시험 — 좋은 기록은 읽히고, 적재 규칙마다 심은 나쁜 기록이 제 이름의 멈춤으로 서는지 (phase-2 등록 P2)
"""P2 acceptance of rewrite/phase2-impl.frozen.md: a good record loads, and one planted bad record per load rule STOPs
with its named id. The composition `source_kind` controls of the P2 list (an unknown kind, `inherited`) live with the
body validator (solver/tests/test_composition_decl.py), where the declaration is read.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_material_registry
"""
import copy
import tempfile
import unittest
from pathlib import Path

import yaml

from solver import material_registry as mr

SHA = "0" * 64
CITE = {"cache": "2007ApJ...669.1279S.pdf", "page": "1281", "where": "eq. (5)", "sha256": SHA}


def const(v, unit):
    return {"value": v, "unit": unit, "source": dict(CITE), "grade": "read"}


#: A minimal single record: every required key, a sourced field inside its window on P, open in T with refusals.
GOOD = {
    "id": "toy", "label": "toy solid", "kind": "single", "system": "toy", "fit_composition": "toy",
    "phases": [{
        "id": "toy_solid", "state": "solid",
        "eos": {"form": "bme3", "params": {"rho0": const(4000.0, "kg/m3"), "k0": const(2.0e11, "Pa"),
                                           "k0p": const(4.0, "1")},
                "reference": {"kind": "state", "p": const(0.0, "Pa"), "t": const(300.0, "K"),
                              "t_ref_kind": "isotherm"}},
        "thermal": {"source_state": "solid", "source_composition": "toy",
                    "pressure": {"alpha_k": const(1.0e6, "Pa/K")},
                    "sets": [{"window": {"p_min": 0.0, "p_max": 5.0e10}, "source_state": "solid",
                              "source_composition": "toy", "constants": {"c_v": const(1000.0, "J/kg/K")}}],
                    "gamma_window": {"p_min": 0.0, "p_max": 1.0e11}},
        "field": {"kind": "sourced", "box": {"p_min": 0.0, "p_max": 1.0e11}, "source": dict(CITE)},
        "window": {"p_min": 0.0, "p_max": 1.0e11, "t_min": 100.0, "t_max": 3000.0},
        "edges": {"t_min": {"refusal": "input.material_out_of_data"},
                  "t_max": {"band": {"form": "relative", "error": 0.02, "grade": "declared",
                                     "origin": "the spread of the source's sampled points at the edge"}}},
    }],
    "formula_checks": [{"quantity": "P at ρ = 4400", "state": {"rho": 4400.0}, "expected": 2.1e10, "unit": "Pa",
                        "tolerance": 1.0e8, "tolerance_reason": "printed to 2 figures", "expression": "bme3(rho)",
                        "source": dict(CITE)}],
}


def plant(edit):
    d = copy.deepcopy(GOOD)
    edit(d)
    return d


PH = lambda d: d["phases"][0]                     # noqa: E731

#: (rule, edit, expected STOP id) — one planted bad record per load rule (P2 controls).
CONTROLS = (
    ("missing field", lambda d: PH(d).pop("field"), "material.missing_key"),
    ("missing window", lambda d: PH(d).pop("window"), "material.missing_key"),
    ("edge with neither band nor refusal", lambda d: PH(d)["edges"].pop("t_min"), "material.edge_undeclared"),
    ("edge with both", lambda d: PH(d)["edges"]["t_min"].update(band=PH(d)["edges"]["t_max"]["band"]),
     "material.edge_both"),
    ("field passes p_max, undeclared", lambda d: PH(d)["field"]["box"].update(p_max=2.0e11),
     "material.edge_undeclared"),
    ("band without origin", lambda d: PH(d)["edges"]["t_max"]["band"].pop("origin"), "material.missing_key"),
    ("γ set past its window", lambda d: PH(d)["thermal"]["sets"][0]["window"].update(p_max=2.0e11),
     "material.gamma_window"),
    ("a γ fallback field", lambda d: PH(d)["thermal"].update(gamma_fallback=1.5), "material.unknown_key"),
    ("dangling cite: two kinds", lambda d: d["formula_checks"][0]["source"].update(doi="doi:10.1086/521346"),
     "material.bad_cite"),
    ("cache cite without page", lambda d: d["formula_checks"][0]["source"].pop("page"), "material.bad_cite"),
    ("cache cite, bad sha256", lambda d: d["formula_checks"][0]["source"].update(sha256="abc"), "material.bad_cite"),
    ("library without version", lambda d: d["formula_checks"][0].update(source={"library": "SeaFreeze"}),
     "material.bad_cite"),
    ("unknown key", lambda d: d.update(colour="grey"), "material.unknown_key"),
    ("bme4 form (not built)", lambda d: PH(d)["eos"].update(form="bme4"), "material.bad_shape"),
    ("no formula check", lambda d: d.update(formula_checks=[]), "material.bad_shape"),
    ("single with two phases", lambda d: d["phases"].append(dict(PH(d), id="toy_b")), "material.kind_rule"),
    ("branched without boundary", lambda d: (d.update(kind="branched"), d["phases"].append(dict(PH(d), id="toy_b"))),
     "material.kind_rule"),
    ("library form without pin", lambda d: PH(d)["eos"].update(form="library"), "material.kind_rule"),
)


def joined(d):
    """GOOD with two sources and a taper join (impl note 3 A8, note 4 items 1, 3)."""
    PH(d)["sources"] = [
        {"id": "meas", "source": dict(CITE), "basis": "measured", "data_range": {"p_min": 2.2e9, "p_max": 1.01e10},
         "data_range_where": "Table 2", "sigma": {"kind": "propagated", "from": {"K0": 1.0e9},
                                                 "correlation": "not_printed"}, "sigma_kind": "1sigma"},
        {"id": "dft", "source": {"doi": "doi:10.1103/PhysRevB.91.054112"}, "basis": "computed",
         "data_range": {"p_min": 3.3e9, "p_max": 1.0e11}, "data_range_where": "Fig. 1",
         "sigma": {"kind": "not_printed", "where": "§VI"}, "sigma_kind": "not_applicable"}]
    PH(d)["joins_within"] = [{"between": ["meas", "dft"], "kind": "taper", "edge_p": 1.01e10, "side": "upper",
                              "weight": "smoothstep_p", "k": 2}]
    PH(d)["precedence"] = {"by": "basis"}


def tabled(d):
    """GOOD as a user-declared (P, T) table with α and K_T columns (impl note 3 B1–B3)."""
    PH(d)["eos"] = {"form": "table", "reference": {"kind": "state", "p": const(0.0, "Pa"), "t": const(300.0, "K")},
                    "table": {"axes": "P_T", "first": [1.0e9, 2.0e9, 4.0e9], "t": [300.0, 600.0],
                              "columns": {"rho": [[4000.0, 3990.0], [4050.0, 4040.0], [4150.0, 4140.0]],
                                          "alpha": [[2.0e-5, 2.1e-5] for _ in range(3)],
                                          "k_t": [[2.0e11, 1.9e11] for _ in range(3)]},
                              "interpolation": "bilinear_lnp_t", "alpha_range": [0.0, 1.0e-4],
                              "source": {"user_declared": "a fictional rock for a test"}}}


def col(d, name):
    return PH(d)["eos"]["table"]["columns"][name]


def _set(d, name, i, row):
    col(d, name)[i] = row


#: Planted bad records for the notes-3/4 rules, each on its good base.
CONTROLS_JOINS = (
    ("σ propagated without correlation", lambda d: (joined(d), PH(d)["sources"][0]["sigma"].pop("correlation")),
     "material.sigma_rule"),
    ("a stand-in for an unprinted σ", lambda d: (joined(d), PH(d)["sources"][1]["sigma"].update(value=0.01)),
     "material.sigma_rule"),
    ("missing sigma_kind", lambda d: (joined(d), PH(d)["sources"][0].pop("sigma_kind")), "material.missing_key"),
    ("join names an unknown source", lambda d: (joined(d), PH(d)["joins_within"][0].update(between=["meas", "x"])),
     "material.join_rule"),
    ("k other than 2", lambda d: (joined(d), PH(d)["joins_within"][0].update(k=1)), "material.join_rule"),
    ("taper without edge_p", lambda d: (joined(d), PH(d)["joins_within"][0].pop("edge_p")), "material.join_rule"),
    ("a T weight", lambda d: (joined(d), PH(d)["joins_within"][0].update(weight="smoothstep_t")),
     "material.bad_shape"),
    ("taper width on the wrong side", lambda d: (joined(d), PH(d)["joins_within"][0].update(
        width={"p_end": 9.0e9, "reason": "r", "declared_before_comparison": "2026-10-10"})), "material.join_rule"),
    ("taper width without reason", lambda d: (joined(d), PH(d)["joins_within"][0].update(
        width={"p_end": 1.3e10, "declared_before_comparison": "2026-10-10"})), "material.missing_key"),
    ("no precedence", lambda d: (joined(d), PH(d).pop("precedence")), "material.precedence"),
    ("computed preferred over measured", lambda d: (joined(d), PH(d)["joins_within"][0].update(
        between=["dft", "meas"])), "material.precedence"),
    ("declared precedence without date", lambda d: (joined(d), PH(d).update(precedence={"by": "declared"})),
     "material.precedence"),
    ("table: ρ falls with P", lambda d: (tabled(d), _set(d, "rho", 2, [4040.0, 4000.0])), "material.table_check"),
    ("table: NaN", lambda d: (tabled(d), _set(d, "rho", 1, [float("nan"), 4040.0])), "material.table_check"),
    ("table: K_T ≤ 0", lambda d: (tabled(d), _set(d, "k_t", 0, [0.0, 1.9e11])), "material.table_check"),
    ("table: α outside its range", lambda d: (tabled(d), _set(d, "alpha", 0, [2.0e-3, 2.1e-5])),
     "material.table_check"),
    ("table: bilinear without α/K_T", lambda d: (tabled(d), PH(d)["eos"]["table"]["columns"].pop("k_t")),
     "material.table_check"),
    ("table: ragged column", lambda d: (tabled(d), _set(d, "rho", 0, [4000.0])), "material.table_check"),
)


class TRegistry(unittest.TestCase):
    def _load(self, *records, registered=(SHA,)):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "sources.yaml").write_text(yaml.safe_dump(
                {"sources": [{"sha256": h, "name": "toy.pdf"} for h in registered]}), encoding="utf-8")
            for r in records:
                Path(tmp, f"{r['id']}.yaml").write_text(yaml.safe_dump(r, sort_keys=False), encoding="utf-8")
            return mr.load(Path(tmp))

    def test_good_record_loads(self):
        reg = self._load(GOOD)
        self.assertIsInstance(reg, mr.Registry, getattr(reg, "evidence", None))
        self.assertTrue(reg.known("toy"))

    def test_each_rule_stops_by_name(self):
        for rule, edit, id_ in CONTROLS:
            with self.subTest(rule=rule):
                out = self._load(plant(edit))
                self.assertIsInstance(out, mr.LoadStop, rule)
                self.assertEqual(out.id, id_, dict(out.evidence))

    def test_notes_3_4_good_bases_load(self):
        for name, edit in (("taper join", joined), ("user-declared table", tabled)):
            with self.subTest(base=name):
                out = self._load(plant(edit))
                self.assertIsInstance(out, mr.Registry, getattr(out, "evidence", None))
        self.assertEqual(self._load(plant(tabled)).declared(), ("toy",))      # counted (note 3 B2)
        self.assertEqual(self._load(GOOD).declared(), ())

    def test_notes_3_4_rules_stop_by_name(self):
        for rule, edit, id_ in CONTROLS_JOINS:
            with self.subTest(rule=rule):
                out = self._load(plant(edit))
                self.assertIsInstance(out, mr.LoadStop, rule)
                self.assertEqual(out.id, id_, dict(out.evidence))

    def test_unregistered_source_stops(self):
        """IB2 by the manifest (impl note 3 C3): a cache cite whose sha256 is not registered STOPs."""
        out = self._load(GOOD, registered=())
        self.assertEqual(out.id, "material.unregistered_source")

    def test_every_stop_has_a_fix(self):
        for id_, (fields, fix) in mr.STOPS.items():
            with self.subTest(id=id_):
                self.assertTrue(fields and isinstance(fix, str) and len(fix) > 20)

    def test_id_must_match_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "sources.yaml").write_text(yaml.safe_dump({"sources": [{"sha256": SHA}]}), encoding="utf-8")
            Path(tmp, "other.yaml").write_text(yaml.safe_dump(GOOD), encoding="utf-8")
            out = mr.load(Path(tmp))
        self.assertEqual(out.id, "material.id_mismatch")

    def test_load_does_not_touch_the_paper_cache(self):
        """IB2: the cite names a file that exists nowhere here, and the record still loads (form check only)."""
        rec = plant(lambda d: d["formula_checks"][0]["source"].update(cache="no-such-file-1999.pdf"))
        self.assertIsInstance(self._load(rec), mr.Registry)

    def test_shipped_records_load(self):
        """Whatever records the tree carries load (none before P5/P6; then fe_prem, h2o)."""
        out = mr.load()
        self.assertIsInstance(out, mr.Registry, getattr(out, "evidence", None))


if __name__ == "__main__":
    unittest.main()
