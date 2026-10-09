# S10 시험 — 화성 물질 빌더 비트 일치, 조성 닫힘, 화성 · Dante 답, 민감도 항목 (등록 노트 5 의 3a–3g)
"""S10 acceptance of rewrite/phase1-a1-impl.frozen.md note 5 item 3, each with its control.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_s10
"""
import dataclasses
import math
import random
import unittest

from solver import body as b, context, from_v1, legacy_materials as lm, legacy_view as lv, result, solve as sv
from solver import stepper as st

I, eos = lm.interior, lm.eos
MARS_OXIDES = {"SiO2": 46.66, "Al2O3": 3.49, "MgO": 32.81, "CaO": 2.66, "FeO": 13.68, "Na2O": 0.69}
ANCHOR_S = 0.1890625


def _pts(n=200):
    rng = random.Random(20261009)
    return [(10 ** rng.uniform(9.5, 11.5), rng.uniform(1500, 3500)) for _ in range(n)]


def _dens(m, p, t):
    """density and (dT/dP)_ad through the adapter's view (the spec's «density and dT/dP», r2 S10)."""
    got = lm.LegacyView(getattr(m, "name", "?"), m, 1600.0).state(p, t)
    if isinstance(got, st.Stop):
        return ("refused", got.record.kind, got.record.message_old)
    return got[:2]


class Builders(unittest.TestCase):
    """3b/3c: the builders give the same material as the old context managers, bit for bit, without the swap."""

    def test_fe_core_light(self):
        for s in (ANCHOR_S, 0.15, 0.22):
            new = lm.build_fe_core_light(s, 0.04, 0.014)
            with I._sulphur_core(s, "box_ceiling"):
                old = I.MATERIALS[I.COMPOSITIONS["earth_like"][3]]
                ref = [_dens(old, p, t) for p, t in _pts()]
            self.assertEqual([_dens(new, p, t) for p, t in _pts()], ref, s)
            self.assertNotIn(new.name, I.MATERIALS)                     # never registered

    def test_control_other_s_differs(self):
        a = lm.build_fe_core_light(ANCHOR_S, 0.04, 0.014)
        c = lm.build_fe_core_light(0.15, 0.04, 0.014)
        self.assertNotEqual([_dens(a, p, t) for p, t in _pts(20)], [_dens(c, p, t) for p, t in _pts(20)])

    def test_silicate_decl(self):
        new, why = lm.build_silicate_decl(MARS_OXIDES)
        self.assertIsNone(why)
        before = I.MATERIALS["silicate"]
        with I._mantle(MARS_OXIDES):
            ref = [_dens(I.MATERIALS["silicate"], p, t) for p, t in _pts()]
        self.assertEqual([_dens(new, p, t) for p, t in _pts()], ref)
        self.assertIs(I.MATERIALS["silicate"], before)                  # no swap left behind


class Uniform:
    def __init__(self, rho):
        self.rho, self.mat, self.p_floor = rho, None, 0.0

    def state(self, p, t, guess):
        return (self.rho, 0.0, ())


class XCore(Uniform):
    """A core whose density is a known function of the closure value: ρ(x) = 9000 (1 + x)."""
    def at(self, x):
        return Uniform(9000.0 * (1.0 + x))


class CompositionClosure(unittest.TestCase):
    """3a: the closure value reaches the pass through the closure layer's view, and closes at the known x."""
    M, F_CORE, X_TRUE = 5.0e24, 0.3, 0.3

    def _body(self, layer="core", name="S"):
        rho_c, rho_m = 9000.0 * (1 + self.X_TRUE), 3000.0
        R = (3 / (4 * math.pi) * (self.F_CORE * self.M / rho_c + (1 - self.F_CORE) * self.M / rho_m)) ** (1 / 3)
        layers = (b.Layer("core", "core", "x", b.Extent("mass_fraction", self.F_CORE)), b.Layer("mantle", "mantle", "y"))
        return b.Body("fixture", "planet", b.SurfaceState(self.M, t_pot=None), layers,
                      b.Closure("composition", 0.0, 1.0, layer, name), radius=b.Declared(R, "m"))

    def test_closes_at_known_x(self):
        out, x = sv.solve(self._body(), views={"core": XCore(0.0), "mantle": Uniform(3000.0)})
        self.assertIsInstance(out, result.Answer, getattr(out, "text", out))
        self.assertLess(abs(x - self.X_TRUE), 1e-9)

    def test_control_axis_the_material_lacks_is_refused(self):
        layers = (b.Layer("core", "core", "fe_prem", b.Extent("mass_fraction", 0.3)), b.Layer("mantle", "mantle", "silicate"))
        body = b.Body("fixture", "planet", b.SurfaceState(5.0e24, t_pot=1600.0, t_s=300.0), layers,
                      b.Closure("composition", 0.0, 1.0, "mantle", "Q"), radius=b.Declared(6.0e6, "m"))
        out, _ = sv.solve(body)
        self.assertIsInstance(out, result.Refusal)
        self.assertEqual((out.id, out.evidence["rule"]), ("input.cross_field", "closure_axis"))


class Mars(unittest.TestCase):
    """3e: Mars answers; S against the anchor; the radius events hold; S8's read check runs on Mars (note 5 item 1)."""

    @classmethod
    def setUpClass(cls):
        body, _ = from_v1.load_v1("engine/bodies/mars.yaml")
        cls.ans, cls.s = sv.solve(body)

    def test_answers_with_s_near_the_anchor(self):
        self.assertIsInstance(self.ans, result.Answer, getattr(self.ans, "text", self.ans))
        self.assertLess(abs(self.s - ANCHOR_S), 0.001875)          # within 0.1875 wt% (c8, r2)
        q = {x.key: x.point for x in self.ans.quantities}
        self.assertEqual(q["core_radius"], 1695000.0)
        self.assertEqual(q["core_plus_layer_radius_solved_km"], 1845.0)
        self.assertEqual(q["basal_layer_thickness_km"], 150.0)

    def test_read_check_on_mars(self):
        chain = lv.run_chain("engine/bodies/mars.yaml", self.ans)
        self.assertEqual(lv.check_reads(chain), [])
        cmf = next(x.point for x in self.ans.quantities if x.key == "core_mass_fraction")
        self.assertEqual(chain.body.get("core_mass_fraction"), cmf)


class Dante(unittest.TestCase):
    """3d: Dante answers on the porosity closure, with no temperature path."""

    def test_answers_without_temperatures(self):
        body, _ = from_v1.load_v1("engine/bodies/dante_fixture.yaml")
        out, phi0 = sv.solve(body)
        self.assertIsInstance(out, result.Answer, getattr(out, "text", out))
        self.assertTrue(0.0 < phi0 < 0.6)
        keys = {q.key for q in out.quantities}
        self.assertFalse({"core_temperature", "cmb_temperature"} & keys)
        self.assertIn("no_temperature_path", [n.kind for n in out.notes])


class Sensitivity(unittest.TestCase):
    """3f: the warm T_pot + δ field equals the forward difference of two independent cold solves, within the
    recorded-noise tolerance 3 · 2 · LID_T_TOL · |q| / |Δq|."""

    @classmethod
    def setUpClass(cls):
        e, _ = from_v1.load_v1("engine/bodies/earth.yaml")
        off = context.Options(sensitivity_dt=0.0)
        cls.field = {q.key: q for q in sv.solve(e)[0].quantities}
        cls.a = {q.key: q.point for q in sv.solve(e, off)[0].quantities}
        e2 = dataclasses.replace(e, surface=dataclasses.replace(e.surface, t_pot=e.surface.t_pot + 10.0))
        cls.c = {q.key: q.point for q in sv.solve(e2, off)[0].quantities}

    def _tol(self, key, dt):
        dq = self.c[key] - self.a[key]
        return 3 * 2 * context.Options().lid_t_tol * abs(self.a[key]) / abs(dq), dq / dt

    def test_field_matches_independent_difference(self):
        for key in ("core_temperature", "cmb_temperature", "radius"):
            tol, fd = self._tol(key, 10.0)
            got = self.field[key].sensitivity
            self.assertIsNotNone(got, key)
            self.assertLess(abs(got - fd) / abs(fd), tol, key)

    def test_control_wrong_divisor_fails(self):
        tol, fd = self._tol("cmb_temperature", 5.0)
        self.assertGreater(abs(self.field["cmb_temperature"].sensitivity - fd) / abs(fd), tol)


class BasalBase(unittest.TestCase):
    """r2 S10 B1: the basal layer's thermal side is the declared mantle, as in the old `_mantle` swap."""

    PTS = [(p * 1e9, t) for p in (17.0, 18.5, 19.5, 20.5) for t in (1800.0, 2000.0, 2200.0)]

    def test_basal_state_matches_the_old_swapped_context(self):
        body, _ = from_v1.load_v1("engine/bodies/mars.yaml")
        basal = next(l for l in body.layers if l.id == "basal")
        view, why = sv._view_for(body, basal, None, 0.0)
        self.assertIsNone(why)
        with I._mantle(MARS_OXIDES):
            old = lm.LegacyView("silicate_basal_const", I.BasalConstDensity(4050.0), 1600.0, 0.0)
            ref = [old.state(p, t)[:2] for p, t in self.PTS]
        self.assertEqual([view.state(p, t)[:2] for p, t in self.PTS], ref)

    def test_control_plain_silicate_base_differs(self):
        plain = lm.LegacyView("silicate_basal_const", I.BasalConstDensity(4050.0), 1600.0, 0.0)
        with I._mantle(MARS_OXIDES):
            old = lm.LegacyView("silicate_basal_const", I.BasalConstDensity(4050.0), 1600.0, 0.0)
            ref = [old.state(p, t)[:2] for p, t in self.PTS]
        self.assertNotEqual([plain.state(p, t)[:2] for p, t in self.PTS], ref)


class OnsetMat:
    """r2's fixture: onset curve T_on(P) = 1605 K + P / 1 GPa — not reached at T_pot 1600 K, crossed at 1610 K."""
    name = "fx_onset"
    phases = ()
    onset_curve_names = ("fx",)

    def onset_curves(self, p, t):
        return [("fx", 1605.0 + p / 1e9)]


class OnsetMantle:
    def __init__(self):
        self.mat, self.p_floor, self.p_stop = OnsetMat(), 0.0, 0.0

    def state(self, p, t, g):
        return (3000.0 * (0.9 if t > 1605.0 + p / 1e9 else 1.0), 0.0, ())


class SensitivityAcrossEvents(unittest.TestCase):
    """r2 S10 B2: an onset crossing that appears between T_pot and T_pot + δ makes the sensitivity omitted, noted."""

    def _body(self, t_pot):
        layers = (b.Layer("core", "core", "x", b.Extent("mass_fraction", 0.3)), b.Layer("mantle", "mantle", "y"))
        return b.Body("fx", "planet", b.SurfaceState(5.0e24, t_pot=t_pot), layers, b.Closure("R", 3.0e6, 2.0e7))

    def test_event_set_change_omits(self):
        out, _ = sv.solve(self._body(1600.0), views={"core": Uniform(9000.0), "mantle": OnsetMantle()})
        self.assertIsInstance(out, result.Answer, getattr(out, "text", out))
        self.assertIn("sensitivity_across_boundary_change", [n.kind for n in out.notes])
        self.assertIsNone(next(q for q in out.quantities if q.key == "radius").sensitivity)

    def test_control_no_crossing_keeps_the_field(self):
        out, _ = sv.solve(self._body(1500.0), views={"core": Uniform(9000.0), "mantle": OnsetMantle()})
        self.assertNotIn("sensitivity_across_boundary_change", [n.kind for n in out.notes])
        self.assertIsNotNone(next(q for q in out.quantities if q.key == "radius").sensitivity)


class ReadCheckControls(unittest.TestCase):
    """r2 S10: negative controls for check_reads rules 1 (output outside the set) and 3 (registered output missed)."""

    @classmethod
    def setUpClass(cls):
        e, _ = from_v1.load_v1("engine/bodies/earth.yaml")
        cls.chain = lv.run_chain("engine/bodies/earth.yaml", sv.solve(e, context.Options(sensitivity_dt=0.0))[0])

    def test_rule1_output_outside_the_set(self):
        self.chain.body.lookups.append(("core_state", "nmoi", "derived hit"))
        try:
            self.assertIn("output read outside the registered set", [v[2] for v in lv.check_reads(self.chain)])
        finally:
            self.chain.body.lookups.pop()

    def test_rule3_registered_output_missed(self):
        self.chain.body.lookups.append(("core_state", "core_radius", "derived miss"))
        try:
            self.assertIn("registered output missed", [v[2] for v in lv.check_reads(self.chain)])
        finally:
            self.chain.body.lookups.pop()


class RulingsA3A7(unittest.TestCase):
    """Comparator rulings 225888af: A3 core_radius_fraction (all bodies with a CMB) and A7 Dante's bulk_porosity."""

    def test_core_radius_fraction(self):
        e, _ = from_v1.load_v1("engine/bodies/earth.yaml")
        q = {x.key: x.point for x in sv.solve(e, context.Options(sensitivity_dt=0.0))[0].quantities}
        self.assertEqual(q["core_radius_fraction"], q["core_radius"] / q["radius"])

    def test_dante_bulk_porosity_near_the_old(self):
        """The old engine (097a8aa3, interior_layers on dante_fixture, run on the Mac) gave 0.18724686102568214 at its
        own φ₀ 0.39045639; the rewrite's φ₀ is 0.39043. V_p is integrated in the state, at stepper order. Agreement
        within 1e-5 relative (a check of the definition, not the oracle comparison). Control: a body without
        porosity emits no bulk_porosity."""
        d, _ = from_v1.load_v1("engine/bodies/dante_fixture.yaml")
        q = {x.key: x.point for x in sv.solve(d, context.Options(sensitivity_dt=0.0))[0].quantities}
        # with V_p in the state (r2 on 973b89ef) the gap is the φ₀ difference's effect only: measured 1e-6 relative
        self.assertLess(abs(q["bulk_porosity"] - 0.18724686102568214) / 0.18724686102568214, 1e-5)
        e, _ = from_v1.load_v1("engine/bodies/earth.yaml")
        self.assertNotIn("bulk_porosity", {x.key for x in sv.solve(e, context.Options(sensitivity_dt=0.0))[0].quantities})


if __name__ == "__main__":
    unittest.main()
