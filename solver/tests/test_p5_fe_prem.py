# fe_prem 기록 시험 — 등록부에 읽히고, 옛 FE_PREM 과 상수를 하나씩 견주어 다른 것은 이름 붙은 결함만이며, 인쇄값 검산이 맞는지 (phase-2 impl P5 · note 1)
"""P5 tests that need no P3 view (rewrite/phase2-impl.frozen.md P5, amended by impl note 1):

1. The record loads in the registry the solver reads.
2. The constant diff (note 1 §4, «closure of the list»): every numeric constant of the record's structure path is
   compared with the legacy `eos.FE_PREM` objects. Each difference must be on the expected list with its finding id,
   and each legacy field the record does not carry must be on the not-carried list with its reason, or the test fails.
   Expected differences: W-L1-01 (alpha_k) and G4 (the Dorogokupets set ends at its printed 350 GPa, legacy ∞);
   W-L20-01 takes the legacy treatment, so it has no override. The closure covers each legacy ThermalSet's fields
   too (68 N6): every field is compared or listed with its reason.
3. The reference adiabat is legacy's table, node for node.
4. The formula checks, evaluated here on the record's own constants, as printed (I&A P_TH and its nonlinear part,
   Huang's γ). The planted control: alpha_k = 0.00121 GPa/K (Seager's transcription, W-L1-01) fails the P_TH check.

Stage (a) and (b) of the legacy equivalence need P3's view (state(P, T)) and land with it.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_p5_fe_prem
"""
import math
import sys
import unittest

from solver import material_registry as mr

GPA = 1.0e9

#: record path → legacy value differs, by finding (note 1 §4)
EXPECTED_DIFF = {"phase.thermal.pressure.alpha_k": "W-L1-01: I&A print 12.1e-3 GPa/K; legacy 0.00121 (Seager+ 2007)",
                 "sets[1].window.p_max": "G4 (owner-direction 8b86499): printed scope 350 GPa; legacy ∞",
                 "sets[1].evaluator.params.v0": "P5-F1: Table 1 prints V0 7.957 with reference superscript 84; "
                                                "legacy 7.95784e-6 glued the superscript on"}

#: legacy fe_liquid.LIQUID (Column) fields the record's evaluator params do not carry, with the reason
COLUMN_NOT_CARRIED = {
    "name": "the record's evaluator.name",
    "ref": "prose; each param carries its source",
    "n_atom": "atoms per formula unit, 1 for Fe; not a Table 1 parameter (the evaluator's formula unit)",
}
#: Table 1 liquid values the record carries that legacy's Column has no slot for
PARAMS_NOT_IN_LEGACY = {
    "u0": "U0, the constant term of eq. (22); no V or T derivative (P, (∂P/∂T)_V, C_V, γ) reads it",
    "a_s": "a_S enters eq. (22) only as −a_S R (T − T0), V-independent («in the first approximation», p.3) and "
           "linear in T: it adds a_S R to S and nothing to P, (∂P/∂T)_V, C_V or γ, so legacy's evaluator is the "
           "printed model for what the set supplies (68 N13)",
}

#: legacy Phase / ThermalSet fields the record does not carry, with the reason
NOT_CARRIED = {
    "melt": "G1: the melting curve is core-energy history data, not in phase 2",
    "melt_scale": "G1", "melt_ref": "G1", "melt_variant": "G1",
    "join": "G1: prose", "join_note": "G1: prose",
}

#: legacy ThermalSet fields compared below (pairs / string pairs), or not carried with the reason (68 N6)
SET_CARRIED = {"p_min", "p_max", "alpha_k", "c_v_ref", "t_ref", "t_ref_kind", "source_state", "source_composition",
               "evaluator", "alpha_k_dt", "t_max", "t_min", "p_edge"}
SET_NOT_CARRIED = {
    "ref": "prose; the record's source carries cache, page, where and sha256 instead",
    "grade_note": "prose; the record's set grade carries it (checked to name the disagreement)",
    "grade_kind": "legacy delivery rule; the record's grade text and edge band grade carry the kind",
}


def _record():
    reg = mr.load()
    if isinstance(reg, mr.LoadStop):
        raise AssertionError(f"registry STOP: {reg}")
    return reg.records["fe_prem"] if hasattr(reg, "records") else reg["fe_prem"]


def _legacy():
    import solver.legacy_materials  # noqa: F401  (puts engine/ on the path, 097a8aa3)
    return sys.modules["eos"]


def _v(c):
    return float(c["value"])


class Loads(unittest.TestCase):
    def test_record_loads(self):
        rec = _record()
        self.assertEqual(rec["id"], "fe_prem")
        self.assertEqual(len(rec["phases"]), 1)                          # one PREM-path phase (r2 IB1)


class ConstantDiff(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rec = _record()["phases"][0]
        cls.eos = _legacy()
        cls.ph = cls.eos.FE_PREM.phases[0]
        import fe_liquid
        cls.column = fe_liquid.LIQUID

    def pairs(self):
        r, ph = self.rec, self.ph
        p, sets = r["thermal"]["pressure"], r["thermal"]["sets"]
        huang, doro = ph.gamma_sets
        return [
            ("phase.eos.params.rho0", _v(r["eos"]["params"]["rho0"]), ph.rho0),
            ("phase.eos.params.k0", _v(r["eos"]["params"]["k0"]), ph.k0),
            ("phase.eos.params.k0p", _v(r["eos"]["params"]["k0p"]), ph.k0p),
            ("phase.window.p_min", float(r["window"]["p_min"]), ph.p_min),
            ("phase.window.p_max", float(r["window"]["p_max"]), ph.p_max),
            ("phase.eos.reference.t", _v(r["eos"]["reference"]["t"]), ph.t_ref),
            ("phase.thermal.pressure.alpha_k", _v(p["alpha_k"]), ph.alpha_k),
            ("phase.thermal.pressure.alpha_k_dt", _v(p["alpha_k_dt"]), ph.alpha_k_dt),
            ("phase.thermal.pressure.c_v", _v(p["c_v"]), ph.c_v_ref),
            ("sets[0].window.p_min", float(sets[0]["window"]["p_min"]), huang.p_min),
            ("sets[0].window.p_max", float(sets[0]["window"]["p_max"]), huang.p_max),
            ("sets[0].constants.alpha_k", _v(sets[0]["constants"]["alpha_k"]), huang.alpha_k),
            ("sets[0].constants.c_v", _v(sets[0]["constants"]["c_v"]), huang.c_v_ref),
            ("sets[0].t_ref", _v(sets[0]["t_ref"]), huang.t_ref),
            ("sets[1].window.p_min", float(sets[1]["window"]["p_min"]), doro.p_min),
            ("sets[1].window.p_max", float(sets[1]["window"]["p_max"]), doro.p_max),
        ] + [(f"sets[1].evaluator.params.{n}", _v(c), getattr(self.column, n))
             for n, c in sets[1]["evaluator"]["params"].items() if n not in PARAMS_NOT_IN_LEGACY]

    def test_evaluator_params_close(self):
        import dataclasses
        params = self.rec["thermal"]["sets"][1]["evaluator"]["params"]
        missing = [f.name for f in dataclasses.fields(self.column)
                   if f.name not in params and f.name not in COLUMN_NOT_CARRIED]
        self.assertEqual(missing, [])
        self.assertEqual(sorted(set(params) - {f.name for f in dataclasses.fields(self.column)}),
                         sorted(PARAMS_NOT_IN_LEGACY))
        self.assertEqual(self.column.n_atom, 1.0)

    def test_set_fields_close(self):
        import dataclasses
        sets = self.rec["thermal"]["sets"]
        for i, ts in enumerate(self.ph.gamma_sets):
            missing = [f.name for f in dataclasses.fields(ts)
                       if f.name not in SET_CARRIED and f.name not in SET_NOT_CARRIED]
            self.assertEqual(missing, [], f"set {i}")
            r = sets[i]
            self.assertEqual((r["source_state"], r["source_composition"]), (ts.source_state, ts.source_composition))
            self.assertEqual(r.get("evaluator", {}).get("name", ""), ts.evaluator)
            # zero / empty in legacy means «none»: the record carries none of these
            self.assertEqual((ts.alpha_k_dt, ts.t_max, ts.t_min, ts.p_edge), (0.0, 0.0, 0.0, ""))
            self.assertFalse({"alpha_k_dt", "t_max", "t_min", "p_edge"} & (set(r.get("constants", {})) | set(r)))
        self.assertIn("disagree", sets[1]["grade"])
        self.assertEqual(self.ph.gamma_sets[1].grade_kind, "disagreement")

    def test_every_difference_is_named(self):
        unnamed = []
        for path, new, old in self.pairs():
            same = new == old or (old != 0 and math.isfinite(old) and abs(new - old) <= 1e-12 * abs(old))
            if not same and path not in EXPECTED_DIFF:
                unnamed.append((path, new, old))
            if same and path in EXPECTED_DIFF:
                unnamed.append((path, "expected a difference", old))
        self.assertEqual(unnamed, [])

    def test_alpha_k_is_the_corrected_value(self):
        self.assertAlmostEqual(_v(self.rec["thermal"]["pressure"]["alpha_k"]) / self.ph.alpha_k, 10.0, places=12)

    def test_huang_set_reference_kind(self):
        self.assertEqual(self.rec["thermal"]["sets"][0]["t_ref_kind"], self.ph.gamma_sets[0].t_ref_kind)

    def test_dorogokupets_set_ends_at_its_printed_scope(self):
        # G4 (owner-direction 8b86499): the set and the γ window end at 350 GPa; only the edge band reaches the
        # phase window's 12 TPa, and above it the record refuses
        doro, rec = self.ph.gamma_sets[1], self.rec["thermal"]["sets"][1]
        self.assertEqual(doro.p_max, math.inf)
        self.assertEqual(float(rec["window"]["p_max"]), 350.0 * GPA)
        self.assertEqual(float(self.rec["thermal"]["gamma_window"]["p_max"]), 350.0 * GPA)
        edge = rec["edge_above"]
        self.assertEqual(float(edge["limit"]), self.ph.p_max)
        self.assertEqual(edge["band"]["grade"], "extrapolated beyond printed scope")
        self.assertEqual(edge["band"]["origin"], "declared stand-in: model disagreement at 35 GPa carried above the printed scope; not an extrapolation estimate")  # D1, directing
        self.assertNotIn("error", edge["band"])                          # the checker computes it (method)
        self.assertEqual(edge["band"]["source"]["page"], "7")
        self.assertEqual(float(rec["printed_scope"]["p_max"]), 350.0 * GPA)

    def test_edge_band_method_value(self):
        # the method evaluated here on legacy's evaluator (P3's checker replaces this): the set against Huang's
        # printed 35 GPa / 2400 K point; γ 1.3987 vs 2.66, (∂P/∂T)_V 7.494e6 vs 1.1417e7 Pa/K
        import fe_liquid
        got = fe_liquid.thermal_at(35.0 * GPA, 2400.0)
        g = abs(got["gruneisen"] / 2.66 - 1)
        d = abs(got["dpdt_v"] / (5.31e-5 * 215.0 * GPA) - 1)
        self.assertAlmostEqual(g, 0.4742, places=3)
        self.assertAlmostEqual(d, 0.3436, places=3)
        self.assertIn("printed=2.66", self.rec["thermal"]["sets"][1]["edge_above"]["band"]["method"])

    def test_not_carried_fields_are_listed(self):
        import dataclasses
        carried = {"name", "form", "rho0", "k0", "k0p", "p_max", "ref", "p_min", "p_ref", "k0pp", "alpha_k",
                   "alpha_k_dt", "t_ref", "t_ref_kind", "c_v_ref", "thermal_source_state", "thermal_source_composition",
                   "gamma_sets", "fit_state", "p_graded_above", "model_reason", "p_model_measured_max",
                   "p_measured_max", "graded_reason", "graded_below_ref", "t_max"}
        missing = [f.name for f in dataclasses.fields(self.ph)
                   if f.name not in carried and f.name not in NOT_CARRIED]
        self.assertEqual(missing, [])
        self.assertEqual((self.ph.p_ref, self.ph.k0pp, self.ph.p_graded_above, self.ph.t_max), (0.0, 0.0, 0.0, 0.0))


class Adiabat(unittest.TestCase):
    def test_nodes_equal_legacy(self):
        a = _record()["phases"][0]["eos"]["reference"]["adiabat"]
        old = _legacy().REFERENCE_ADIABAT["fe_prem"]
        self.assertEqual(list(map(float, a["lnp"])), list(old.lnp))
        self.assertEqual(list(map(float, a["t"])), list(old.t))
        self.assertEqual(a["interpolation"], "pchip_lnp")


class FormulaChecks(unittest.TestCase):
    """The record's formula checks, evaluated on its own constants (P3's evaluator will replace this)."""

    @classmethod
    def setUpClass(cls):
        rec = _record()
        cls.checks = {c["quantity"]: c for c in rec["formula_checks"]}
        ph = rec["phases"][0]
        cls.ns = {"alpha_k": _v(ph["thermal"]["pressure"]["alpha_k"]),
                  "alpha_k_dt": _v(ph["thermal"]["pressure"]["alpha_k_dt"])}
        cls.huang = {"alpha_k": _v(ph["thermal"]["sets"][0]["constants"]["alpha_k"]),
                     "c_v": _v(ph["thermal"]["sets"][0]["constants"]["c_v"])}

    def eval(self, c, ns):
        return eval(c["expression"], {"__builtins__": {}}, {**ns, **c["state"]})   # noqa: S307 (record data, tests only)

    def test_p_th_6000(self):
        c = self.checks["P_TH at 6000 K"]
        got = self.eval(c, self.ns)
        self.assertAlmostEqual(got / GPA, 81.6411, places=3)          # 68.97 + 12.6711
        self.assertLessEqual(abs(got - c["expected"]), c["tolerance"])

    def test_nonlinear_term(self):
        c = self.checks["P_TH nonlinear term at 6000 K"]
        self.assertLessEqual(abs(self.eval(c, self.ns) - c["expected"]), c["tolerance"])
        self.assertGreater(abs(2 * self.eval(c, self.ns) - c["expected"]), c["tolerance"])   # without the ½: 25.3 fails

    def test_huang_gamma(self):
        c = self.checks["γ of liquid Fe at 19 GPa / 2100 K"]
        got = self.eval(c, self.huang)
        self.assertAlmostEqual(got, 2.7309, places=3)
        self.assertLessEqual(abs(got - c["expected"]), c["tolerance"])

    def test_planted_seager_alpha_fails(self):
        c = self.checks["P_TH at 6000 K"]
        got = self.eval(c, {**self.ns, "alpha_k": 0.00121 * GPA})
        self.assertAlmostEqual(got / GPA, 19.567, places=2)
        self.assertGreater(abs(got - c["expected"]), c["tolerance"])


if __name__ == "__main__":
    unittest.main()
