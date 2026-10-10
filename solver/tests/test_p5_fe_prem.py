# fe_prem 기록 시험 — 등록부에 읽히고, 옛 FE_PREM 과 상수를 하나씩 견주어 다른 것은 이름 붙은 결함만이며, 인쇄값 검산이 맞는지 (phase-2 impl P5 · note 1)
"""P5 tests that need no P3 view (rewrite/phase2-impl.frozen.md P5, amended by impl note 1):

1. The record loads in the registry the solver reads.
2. The constant diff (note 1 §4, «closure of the list»): every numeric constant of the record's structure path is
   compared with the legacy `eos.FE_PREM` objects. Each difference must be on the expected list with its finding id,
   and each legacy field the record does not carry must be on the not-carried list with its reason, or the test fails.
   Expected differences: W-L1-01 (alpha_k) only; W-L20-01 takes the legacy treatment, so it has no override.
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
EXPECTED_DIFF = {"phase.thermal.pressure.alpha_k": "W-L1-01: I&A print 12.1e-3 GPa/K; legacy 0.00121 (Seager+ 2007)"}

#: legacy Phase / ThermalSet fields the record does not carry, with the reason
NOT_CARRIED = {
    "melt": "G1: the melting curve is core-energy history data, not in phase 2",
    "melt_scale": "G1", "melt_ref": "G1", "melt_variant": "G1",
    "join": "G1: prose", "join_note": "G1: prose",
    "huang.t_ref": "the 19 GPa set's anchor temperature (2100 K, isotherm): no schema slot (G5, raised to 7c)",
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
            ("sets[1].window.p_min", float(sets[1]["window"]["p_min"]), doro.p_min),
        ]

    def test_every_difference_is_named(self):
        unnamed = []
        for path, new, old in self.pairs():
            same = new == old or (old != 0 and abs(new - old) <= 1e-12 * abs(old))
            if not same and path not in EXPECTED_DIFF:
                unnamed.append((path, new, old))
            if same and path in EXPECTED_DIFF:
                unnamed.append((path, "expected a difference", old))
        self.assertEqual(unnamed, [])

    def test_alpha_k_is_the_corrected_value(self):
        self.assertAlmostEqual(_v(self.rec["thermal"]["pressure"]["alpha_k"]) / self.ph.alpha_k, 10.0, places=12)

    def test_dorogokupets_set_is_bounded_by_the_phase_window(self):
        # legacy runs the set to ∞; the record bounds it at the phase window (12 TPa, D-M2: γ has its own window)
        doro = self.ph.gamma_sets[1]
        self.assertEqual(doro.p_max, math.inf)
        self.assertEqual(float(self.rec["thermal"]["sets"][1]["window"]["p_max"]), self.ph.p_max)
        self.assertEqual(self.rec["thermal"]["sets"][1]["evaluator"]["name"], doro.evaluator)

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
