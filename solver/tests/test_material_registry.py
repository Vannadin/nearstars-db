# 물질 등록부 시험 — 좋은 기록은 읽히고, 적재 규칙마다 심은 나쁜 기록이 제 이름의 멈춤으로 서는지 (phase-2 등록 P2)
"""P2 acceptance of rewrite/phase2-impl.frozen.md: a good record loads, and one planted bad record per load rule STOPs
with its named id. The composition `source_kind` controls of the P2 list (an unknown kind, `inherited`) live with the
body validator (solver/tests/test_composition_decl.py), where the declaration is read.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_material_registry
"""
import copy
import math
import tempfile
import unittest
from pathlib import Path

import yaml

from solver import material_registry as mr
from solver import stepper as st
from solver import material_view as mv

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
                    "pressure": {"alpha_k": const(1.0e6, "Pa/K"), "c_v": const(1000.0, "J/kg/K")},
                    "sets": [{"window": {"p_min": 0.0, "p_max": 5.0e10}, "source_state": "solid",
                              "source_composition": "toy", "constants": {"alpha_k": const(1.0e6, "Pa/K"),
                                                                         "c_v": const(1000.0, "J/kg/K")}}],
                    "gamma_window": {"p_min": 0.0, "p_max": 1.0e11},
                    "phase_constants": {"p_min": 5.0e10, "p_max": 1.0e11, "reason": "toy: above the set"}},
        "field": {"kind": "sourced", "box": {"p_min": 0.0, "p_max": 1.0e11}, "source": dict(CITE)},
        "window": {"p_min": 0.0, "p_max": 1.0e11, "t_min": 100.0, "t_max": 3000.0},
        "edges": {"t_min": {"refusal": "input.material_out_of_data"},
                  "t_max": {"band": {"form": "relative", "error": 0.02, "grade": "declared",
                                     "origin": "the spread of the source's sampled points at the edge"}}},
    }],
    "formula_checks": [{"quantity": "K0 as printed", "state": {}, "expected": 2.0e11, "unit": "Pa",
                        "tolerance": 0.0, "tolerance_reason": "a transcription check", "expression": "params.k0",
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
    ("phase constants without c_v (P7 cold run)", lambda d: PH(d)["thermal"]["pressure"].pop("c_v"),
     "material.gamma_window"),
    ("a constants set without alpha_k", lambda d: PH(d)["thermal"]["sets"][0]["constants"].pop("alpha_k"),
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
    ("branched without choice", lambda d: (d.update(kind="branched"), d["phases"].append(dict(PH(d), id="toy_b"))),
     "material.kind_rule"),
    ("chain without boundary", lambda d: (d.update(kind="branched", choice="chain"),
                                          d["phases"].append(dict(PH(d), id="toy_b"))),
     "material.kind_rule"),
    ("library form without pin", lambda d: PH(d)["eos"].update(form="library"), "material.kind_rule"),
)


def _fr_params():
    """The F&R evaluator's params as full constants (value, unit, source, grade) so the registry accepts them."""
    from solver.tests.test_material_evaluators import legacy_params
    return {k: {"value": v["value"], "unit": "1", "source": dict(CITE), "grade": "read"}
            for k, v in legacy_params().items()}


def joined(d):
    """GOOD with two sources and a taper join (impl note 3 A8, note 4 items 1, 3)."""
    PH(d)["sources"] = [
        {"id": "meas", "source": dict(CITE), "basis": "measured", "data_range": {"p_min": 2.2e9, "p_max": 1.01e10},
         "data_range_where": "Table 2", "sigma": {"kind": "propagated", "from": {"K0": 1.0e9},
                                                 "correlation": "not_printed"}, "sigma_kind": "1sigma"},
        {"id": "dft", "source": {"doi": "doi:10.1103/PhysRevB.91.054112"}, "basis": "computed",
         "data_range": {"p_min": 3.3e9, "p_max": 1.0e11}, "data_range_where": "Fig. 1",
         "eos": {"form": "evaluator", "reference": {"kind": "state", "p": const(0.0, "Pa"), "t": const(300.0, "K")},
                 "evaluator": {"name": "french_redmer2015", "source": {"formula": "toy"}, "params": _fr_params()}},
         "sigma": {"kind": "not_printed", "where": "§VI"}, "sigma_kind": "not_applicable"}]
    PH(d)["sources"][0]["c_p_from"] = "dft"           # a taper needs c_P on both sides (note 3 A4 item 3)
    PH(d)["joins_within"] = [{"between": ["meas", "dft"], "kind": "taper", "edge_p": 1.01e10, "side": "upper",
                              "weight": "smoothstep_p", "k": 2}]
    PH(d)["precedence"] = {"by": "basis"}


def tabled(d):
    """GOOD as a user-declared (P, T) table with α and K_T columns (impl note 3 B1–B3)."""
    PH(d)["eos"] = {"form": "table", "reference": {"kind": "state", "p": const(0.0, "Pa"), "t": const(300.0, "K")},
                    "table": {"axes": "P_T", "first": [1.0e9, 2.0e9, 4.0e9], "t": [300.0, 600.0],
                              "columns": {"rho": [[4000.0, 3975.5], [4050.0, 4025.2], [4150.0, 4124.6]],
                                          "alpha": [[2.0e-5, 2.1e-5] for _ in range(3)],
                                          "k_t": [[2.0e11, 1.9e11] for _ in range(3)],
                                          "c_p": [[1000.0, 1000.0] for _ in range(3)]},
                              "interpolation": "bilinear_lnp_t", "alpha_range": [0.0, 1.0e-4],
                              "maxwell_tolerance": 0.05,          # one-sided differences over a 300 K step (B3)
                              "source": {"user_declared": "a fictional rock for a test"}}}
    PH(d)["window"] = {"p_min": 1.0e9, "p_max": 4.0e9, "t_min": 300.0, "t_max": 600.0}   # B1: the grid is the window
    for e in ("p_min", "p_max", "t_min", "t_max"):
        PH(d)["edges"].setdefault(e, {"refusal": "input.material_out_of_data"})          # outside the grid: refuse


def col(d, name):
    return PH(d)["eos"]["table"]["columns"][name]


def _set(d, name, i, row):
    col(d, name)[i] = row


def _region_sigma(d, drop=None, regions=None, other=None, kind="1sigma"):
    """A by_region σ on the second source of the joined base (c8: IAPWS-06 Table 7), with one part broken."""
    joined(d)
    sg = {"kind": "by_region", "where": "T7",
          "regions": [{"box": {"p_min": 0.0, "p_max": 2.0e8, "t_min": 238.0, "t_max": 273.0}, "value": 0.002,
                       "where": "T7"}] if regions is None else regions,
          "else": other or {"kind": "not_printed", "where": "Fig. 8"}}
    if drop:
        sg.pop(drop)
    PH(d)["sources"][1]["sigma"] = sg
    PH(d)["sources"][1]["sigma_kind"] = kind


#: Planted bad records for the notes-3/4 rules, each on its good base.
CONTROLS_JOINS = (
    ("σ propagated without correlation", lambda d: (joined(d), PH(d)["sources"][0]["sigma"].pop("correlation")),
     "material.sigma_rule"),
    ("a stand-in for an unprinted σ", lambda d: (joined(d), PH(d)["sources"][1]["sigma"].update(value=0.01)),
     "material.sigma_rule"),
    ("missing sigma_kind", lambda d: (joined(d), PH(d)["sources"][0].pop("sigma_kind")), "material.missing_key"),
    ("by_region without else", lambda d: _region_sigma(d, drop="else"), "material.sigma_rule"),
    ("by_region with an empty region list", lambda d: _region_sigma(d, regions=[]), "material.sigma_rule"),
    ("by_region's else is by_region", lambda d: _region_sigma(d, other={"kind": "by_region", "regions": [],
                                                                         "else": {"kind": "not_printed", "where": "§"}}),
     "material.sigma_rule"),
    ("by_region's else unprinted with a stand-in", lambda d: _region_sigma(d, other={"kind": "not_printed",
                                                                                     "where": "§", "value": 0.01}),
     "material.sigma_rule"),
    ("by_region as not_applicable", lambda d: _region_sigma(d, kind="not_applicable"), "material.sigma_rule"),
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
    ("taper side without c_P", lambda d: (joined(d), PH(d)["sources"][0].pop("c_p_from")), "material.join_rule"),
    ("no precedence", lambda d: (joined(d), PH(d).pop("precedence")), "material.precedence"),
    ("computed preferred over measured", lambda d: (joined(d), PH(d)["joins_within"][0].update(
        between=["dft", "meas"])), "material.precedence"),
    ("basis cannot decide two measured sources", lambda d: (joined(d), PH(d)["sources"][1].update(basis="measured")),
     "material.precedence"),
    ("declared precedence without date", lambda d: (joined(d), PH(d).update(precedence={"by": "declared"})),
     "material.precedence"),
    ("table: ρ falls with P", lambda d: (tabled(d), _set(d, "rho", 2, [4040.0, 4000.0])), "material.table_check"),
    ("table: NaN", lambda d: (tabled(d), _set(d, "rho", 1, [float("nan"), 4040.0])), "material.table_check"),
    ("table: K_T ≤ 0", lambda d: (tabled(d), _set(d, "k_t", 0, [0.0, 1.9e11])), "material.table_check"),
    ("table: α outside its range", lambda d: (tabled(d), _set(d, "alpha", 0, [2.0e-3, 2.1e-5])),
     "material.table_check"),
    ("table: bilinear without c_P (note 9)", lambda d: (tabled(d), PH(d)["eos"]["table"]["columns"].pop("c_p")),
     "material.table_check"),
    ("set edge limit below the set window", lambda d: PH(d)["thermal"]["sets"][0].update(edge_above={
        "band": {"form": "relative", "method": "gamma_spread", "grade": "extrapolated", "origin": "o"},
        "limit": 4.0e10, "limit_reason": "r"}), "material.gamma_window"),
    ("band with both error and method", lambda d: PH(d)["edges"]["t_max"]["band"].update(method="m"),
     "material.bad_shape"),
    ("band with neither error nor method", lambda d: PH(d)["edges"]["t_max"]["band"].pop("error"),
     "material.bad_shape"),
    ("reference adiabat unpaired", lambda d: PH(d)["eos"]["reference"].update(
        kind="path", path="toy path", t_ref_kind="adiabat",
        adiabat={"lnp": [20.0, 21.0, 22.0], "t": [1700.0, 1800.0], "interpolation": "pchip_lnp",
                 "anchor": {"p_pa": 1.0e9}, "source": {"formula": "toy"}}), "material.kind_rule"),
    ("reference adiabat lnp not increasing", lambda d: PH(d)["eos"]["reference"].update(
        kind="path", path="toy path", t_ref_kind="adiabat",
        adiabat={"lnp": [20.0, 22.0, 21.0], "t": [1700.0, 1800.0, 1900.0], "interpolation": "pchip_lnp",
                 "anchor": {"p_pa": 1.0e9}, "source": {"formula": "toy"}}), "material.kind_rule"),
    ("adiabat-kind set without t_ref", lambda d: PH(d)["thermal"]["sets"][0].update(t_ref_kind="adiabat"),
     "material.kind_rule"),
    ("set past its printed scope", lambda d: PH(d)["thermal"]["sets"][0].update(printed_scope={
        "p_max": 4.0e10, "source": dict(CITE)}), "material.gamma_window"),
    ("edge limit past the phase window", lambda d: PH(d)["thermal"]["sets"][0].update(edge_above={
        "band": {"form": "relative", "error": 0.4, "grade": "g", "origin": "o"},
        "limit": 2.0e11, "limit_reason": "r"}), "material.gamma_window"),
    ("edge limit inside the phase window without a refusal id", lambda d: PH(d)["thermal"]["sets"][0].update(
        edge_above={"band": {"form": "relative", "error": 0.4, "grade": "g", "origin": "o"},
                    "limit": 8.0e10, "limit_reason": "r"}), "material.gamma_window"),
    ("evaluator missing a param it needs", lambda d: PH(d)["thermal"]["sets"][0].update(evaluator={
        "name": "dorogokupets2017_liquid_fe", "source": dict(CITE), "params": {"v0": const(7.957e-6, "m3/mol")}}),
     "material.kind_rule"),
    ("evaluator not registered", lambda d: PH(d)["thermal"]["sets"][0].update(evaluator={
        "name": "toy_evaluator", "source": dict(CITE)}), "material.kind_rule"),
    ("γ window not tiled (68 N19)", lambda d: PH(d)["thermal"].pop("phase_constants"), "material.gamma_window"),
    ("non-library phase without gamma_window", lambda d: PH(d)["thermal"].pop("gamma_window"), "material.missing_key"),
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

    def test_set_edge_loads(self):
        rec = plant(lambda d: PH(d)["thermal"]["sets"][0].update(edge_above={
            "band": {"form": "relative", "method": "gamma_spread", "grade": "extrapolated beyond printed scope",
                     "origin": "extrapolation of the printed fit", "source": dict(CITE)},
            "limit": 8.0e10, "limit_reason": "r", "refusal": "input.material_out_of_data"},
            printed_scope={"p_max": 5.0e10, "source": dict(CITE)}))
        self.assertIsInstance(self._load(rec), mr.Registry, getattr(self._load(rec), "evidence", None))

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


class MultiSource(unittest.TestCase):
    """Design note 4 item 3: a non-family source answering in a phase warns (never STOPs), unless the phase gives
    multi_source_reason; a non-family cross-check does not."""

    @staticmethod
    def _phase(eos_cite, joins=(), sources=(), reason=None):
        ph = {"id": "p", "eos": {"form": "bm2", "params": {"rho0": {"value": 1.0, "source": {"cache": eos_cite}}}},
              "sources": list(sources), "joins_within": list(joins)}
        if reason:
            ph["multi_source_reason"] = {"reach": "beyond_primary", "text": reason}
        return ph

    def _warns(self, ph, family=("fam.pdf",)):
        rec = {"id": "toy", "primary_family": {"name": "fam", "sources": list(family), "reason": "r"}, "phases": [ph]}
        return mr.multi_source_warnings(rec, "toy.yaml")

    def test_family_and_controls(self):
        other = {"id": "o", "source": {"cache": "other.pdf"}}
        mine = {"id": "m", "source": {"cache": "fam.pdf"}}
        self.assertEqual(self._warns(self._phase("fam.pdf")), [])
        got = self._warns(self._phase("other.pdf"))                         # the phase's own eos is outside
        self.assertEqual((got[0].id, got[0].evidence["sources"]), ("material.multi_source", ("other.pdf",)))
        taper = {"between": ["m", "o"], "kind": "taper"}
        self.assertEqual(len(self._warns(self._phase("fam.pdf", [taper], [mine, other]))), 1)
        self.assertEqual(self._warns(self._phase("fam.pdf", [taper], [mine, other], reason="above SLB's range")), [])
        check = {"between": ["m", "o"], "kind": "cross_check"}                # a non-family cross-check: no warning
        self.assertEqual(self._warns(self._phase("fam.pdf", [check], [mine, other])), [])
        lib = self._phase("x")
        lib["eos"] = {"form": "library", "library": {"name": "SeaFreeze", "version": "1.1.0"}}
        self.assertEqual(self._warns(lib, family=("SeaFreeze@1.1.0",)), [])
        self.assertEqual(mr.multi_source_warnings({"id": "toy", "phases": [self._phase("other.pdf")]}, "t"), [])


class DirectTable(TRegistry):
    """Impl note 3 B1, B3 and note 4 item 5: the table's window is its grid; Maxwell consistency where the columns allow
    it, within the declared tolerance; the view reads the table bilinearly in (ln P, T) and takes (dT/dP)_S from the
    α and c_P columns only."""

    def _rec(self, change=None):
        d = copy.deepcopy(GOOD)
        tabled(d)
        if change:
            change(d)
        return d

    def test_loads_and_each_control(self):
        self.assertIsInstance(self._load(self._rec()), mr.Registry)
        for name, change, word in (
                ("α against ρ", lambda d: _set(d, "rho", 0, [4000.0, 3990.0]), "Maxwell"),
                ("no tolerance", lambda d: PH(d)["eos"]["table"].pop("maxwell_tolerance"), "maxwell_tolerance"),
                ("c_P against v", lambda d: col(d, "rho") and PH(d)["eos"]["table"]["columns"].update(
                    c_p=[[1000.0, 1000.0], [3000.0, 3000.0], [1000.0, 1000.0]]), "c_P"),
                ("window past the grid", lambda d: PH(d)["window"].update(p_max=5.0e9), "grid")):
            with self.subTest(name):
                got = self._load(self._rec(change))
                self.assertEqual(got.id, "material.table_check", dict(getattr(got, "evidence", {})))
                self.assertIn(word, got.evidence["why"])
        # 68 N61: α through 0 (water near its density maximum) passes against the floor, not a vanishing |α|
        def through_zero(d):
            col(d, "alpha")[:] = [[-2.0e-8, 2.0e-8] for _ in range(3)]       # fails without the floor (5e-2·2e-8)
            PH(d)["eos"]["table"]["alpha_range"] = [-1.0e-4, 1.0e-4]
            col(d, "rho")[:] = [[r[0], r[0]] for r in col(d, "rho")]
        self.assertIsInstance(self._load(self._rec(through_zero)), mr.Registry)
        got = self._load(self._rec(lambda d: PH(d)["eos"]["table"].update(axes="rho_T")))
        self.assertEqual(got.id, "material.kind_rule")                          # not built in phase 2

    def test_alpha_and_cp_required(self):
        """Impl note 9: {α, K_T} alone and {c_P, K_T} alone each STOP; {α, c_P} without K_T loads."""
        for name, drop, ok in (("α, K_T", "c_p", False), ("c_P, K_T", "alpha", False), ("α, c_P", "k_t", True)):
            with self.subTest(name):
                got = self._load(self._rec(lambda d, drop=drop: col(d, "rho") and
                                           PH(d)["eos"]["table"]["columns"].pop(drop)))
                if ok:
                    self.assertIsInstance(got, mr.Registry, dict(getattr(got, "evidence", {})))
                else:
                    self.assertEqual(got.id, "material.table_check")
                    self.assertIn("α and c_P", got.evidence["why"])

    def test_view_reads_the_table(self):
        d = self._rec()
        v = mv.RecordView(d, 300.0)
        u = (math.log(1.5e9) - math.log(1.0e9)) / (math.log(2.0e9) - math.log(1.0e9))
        want = (1 - u) * 0.5 * (4000.0 + 3975.5) + u * 0.5 * (4050.0 + 4025.2)
        rho, dtdp, _n = v.state(1.5e9, 450.0)
        self.assertAlmostEqual(rho, want, places=9)
        self.assertAlmostEqual(dtdp, 2.05e-5 * 450.0 / (rho * 1000.0), delta=1e-18)
        no_cp = self._rec(lambda d: PH(d)["eos"]["table"]["columns"].pop("c_p"))
        self.assertIsInstance(mv.RecordView(no_cp, 300.0).state(1.5e9, 450.0), st.Stop)   # the view refuses too
        self.assertIsInstance(v.state(5.0e9, 450.0), st.Stop)                  # past the grid: refused by its edge


if __name__ == "__main__":
    unittest.main()
