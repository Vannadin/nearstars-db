# 풀이 입구 시험 — 지구 첫 결합, 정방향→역산 왕복, 결정성(두 번 · 풀 1/3 · 두 순서), 중심 바닥 경고, 시험용 손잡이 차단 (등록 S7)
"""S7 acceptance of rewrite/phase1-a1-impl.frozen.md (with notes 1–2), each with its negative control.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_solve
"""
import concurrent.futures as cf
import dataclasses
import math
import multiprocessing as mp
import pickle
import unittest

from solver import body as b, context, from_v1, result, solve as sv
from solver import stepper as st


def earth():
    body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
    return body


def q(answer, key):
    return next(x.point for x in answer.quantities if x.key == key)


class FirstJoin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ans, cls.warm = sv.solve(earth())

    def test_earth_answers(self):
        self.assertIsInstance(self.ans, result.Answer, getattr(self.ans, "text", None))
        for key in ("radius", "nmoi", "core_radius", "cmb_pressure", "cmb_temperature", "core_pressure",
                    "core_temperature", "core_mass_fraction"):
            self.assertTrue(math.isfinite(q(self.ans, key)), key)
        self.assertAlmostEqual(q(self.ans, "core_mass_fraction"), 0.325, delta=1e-12)
        for x in self.ans.quantities:
            self.assertEqual(x.band_reason, result.BAND_NOT_MEASURED)        # note 1 Q4 ②: direct solve
        self.assertEqual(self.warm, q(self.ans, "radius"))

    def test_round_trip_inverse_returns_cmf(self):
        """Forward R from the declared CMF, fed back with R declared and CMF free, returns the CMF (≤ 1e-9)."""
        e = earth()
        R = q(self.ans, "radius")
        layers = tuple(dataclasses.replace(l, extent=None) if l.id == "core" else l for l in e.layers)
        inv = b.Body(e.name + "-inverse", e.kind, e.surface, layers, b.Closure("boundary_mass", 0.05, 0.95, "core"),
                     parent=e.parent, radius=b.Declared(R, "m"), jumps=e.jumps, declarations=e.declarations,
                     solver_flags=e.solver_flags)
        ans, _w = sv.solve(inv)
        self.assertIsInstance(ans, result.Answer, getattr(ans, "text", None))
        self.assertLess(abs(q(ans, "core_mass_fraction") - 0.325), 1e-9)

    def test_control_round_trip_with_wrong_radius_misses(self):
        e = earth()
        R = q(self.ans, "radius") * (1 + 1e-6)
        layers = tuple(dataclasses.replace(l, extent=None) if l.id == "core" else l for l in e.layers)
        inv = b.Body(e.name + "-inverse", e.kind, e.surface, layers, b.Closure("boundary_mass", 0.05, 0.95, "core"),
                     parent=e.parent, radius=b.Declared(R, "m"), jumps=e.jumps, declarations=e.declarations,
                     solver_flags=e.solver_flags)
        ans, _w = sv.solve(inv)
        self.assertGreater(abs(q(ans, "core_mass_fraction") - 0.325), 1e-9)


def _one(t_pot):
    import solver.solve as s2
    e = earth()
    body = dataclasses.replace(e, surface=dataclasses.replace(e.surface, t_pot=t_pot))
    return t_pot, pickle.dumps(s2.solve(body)[0].quantities)


POINTS = (1600.0, 1650.0, 1700.0, 1750.0, 1800.0, 1850.0)


class Determinism(unittest.TestCase):
    def test_twice_identical(self):
        a, _ = sv.solve(earth())
        c, _ = sv.solve(earth())
        self.assertEqual(pickle.dumps(a.quantities), pickle.dumps(c.quantities))

    def test_pool_size_and_order(self):
        def run(pool, order):
            with cf.ProcessPoolExecutor(pool, mp_context=mp.get_context("spawn")) as ex:
                return dict(ex.map(_one, order))
        a = run(1, POINTS)
        c = run(3, tuple(reversed(POINTS)))
        self.assertEqual(a, c)
        self.assertEqual(len(set(a.values())), len(POINTS))      # control: the points do differ


class Uniform:
    def __init__(self, rho):
        self.rho = rho
        self.mat = None
        self.p_floor = 0.0

    def state(self, p, t, guess):
        return (self.rho, 0.0, ())


def _two_layer(core_rho):
    M = 5.0e24
    layers = (b.Layer("core", "core", "x", b.Extent("mass_fraction", 0.5)), b.Layer("mantle", "mantle", "y"))
    body = b.Body("fixture", "planet", b.SurfaceState(M, t_pot=0.0), layers, b.Closure("R", 1e5, 1e8))
    return body, {"core": Uniform(core_rho), "mantle": Uniform(3000.0)}


class FloorGuard(unittest.TestCase):
    """Note 1 item 2: an accepted pass ending at the r floor is noted (ρ_c/ρ̄ > 10³); a normal body is not."""

    def test_dense_centre_noted(self):
        body, views = _two_layer(1.0e7)
        ans, _ = sv.solve(body, views=views)
        self.assertIsInstance(ans, result.Answer, getattr(ans, "text", None))
        self.assertIn("centre_closed_at_floor", [n.kind for n in ans.notes])

    def test_control_ordinary_centre_not_noted(self):
        body, views = _two_layer(6000.0)
        ans, _ = sv.solve(body, views=views)
        self.assertIsInstance(ans, result.Answer, getattr(ans, "text", None))
        self.assertNotIn("centre_closed_at_floor", [n.kind for n in ans.notes])


class Knobs(unittest.TestCase):
    def test_use_wall_trials_unreachable(self):
        import inspect
        self.assertNotIn("use_wall_trials", inspect.getsource(sv))
        self.assertNotIn("use_wall_trials", {f.name for f in dataclasses.fields(context.Options)})



class EveryLayerEntered(unittest.TestCase):
    """Note 3 (r2): at the root every declared layer must have been entered, else solve.layer_order at x*."""

    def _body(self, r_core):
        M = 5.0e24
        layers = (b.Layer("core", "core", "x", b.Extent("radius_from_centre", r_core)), b.Layer("mantle", "mantle", "y"))
        body = b.Body("fixture", "planet", b.SurfaceState(M, t_pot=0.0), layers, b.Closure("R", 1e5, 1e8))
        return body, {"core": Uniform(9000.0), "mantle": Uniform(3000.0)}

    def test_core_never_entered_is_refused(self):
        body, views = self._body(5.0e4)        # 50 km: above the r floor (~7 km), below the mantle's centre end (~74 km)
        out, _ = sv.solve(body, views=views)
        self.assertIsInstance(out, result.Refusal)
        self.assertEqual((out.id, out.evidence["layer_id"], out.evidence["rule"]), ("solve.layer_order", "core", "entered"))

    def test_control_core_entered(self):
        body, views = self._body(3.0e6)
        out, _ = sv.solve(body, views=views)
        self.assertIsInstance(out, result.Answer, getattr(out, "text", None))


class NotYetImplemented(unittest.TestCase):
    """r2 S7 B2/B3: what phase 1 does not implement is refused by name, never misread."""

    def _body(self, **kw):
        M = 5.0e24
        core = kw.get("core", b.Layer("core", "core", "x", b.Extent("mass_fraction", 0.3)))
        top = kw.get("top", b.Layer("mantle", "mantle", "y"))
        closure = kw.get("closure", b.Closure("R", 1e5, 1e8))
        return b.Body("fixture", "planet", b.SurfaceState(M, t_pot=1600.0, t_s=300.0), (core, top), closure)

    def _refused(self, body, rule):
        out, _ = sv.solve(body, views={"core": Uniform(9000.0), "mantle": Uniform(3000.0)})
        self.assertIsInstance(out, result.Refusal)
        self.assertEqual((out.id, out.evidence["rule"]), ("input.cross_field", rule))

    def test_isothermal(self):
        core = b.Layer("core", "core", "x", b.Extent("mass_fraction", 0.3), thermal="isothermal", t_declared=5000.0)
        self._refused(self._body(core=core), "thermal_isothermal_not_in_phase1")

    def test_conductive_not_top(self):
        core = b.Layer("core", "core", "x", b.Extent("mass_fraction", 0.3), thermal="conductive")
        self._refused(self._body(core=core), "conductive_not_top")

    def test_conductive_top_needs_depth(self):
        top = b.Layer("mantle", "mantle", "y", b.Extent("mass_fraction", 0.7), thermal="conductive")
        self._refused(self._body(top=top), "conductive_extent")

    def test_composition_closure(self):
        self._refused(self._body(closure=b.Closure("composition", 0.0, 0.6, "core", "S")),
                      "composition_closure_not_yet")


class SolveId(unittest.TestCase):
    """r2 S7 B1: solve_id is set, deterministic, and moves with the body."""

    def test_set_and_deterministic_and_sensitive(self):
        body, views = _two_layer(6000.0)
        a, _ = sv.solve(body, views=views)
        c, _ = sv.solve(body, views=views)
        sid = a.quantities[0].provenance.solver.solve_id
        self.assertEqual(len(sid), 64)
        self.assertEqual(sid, c.quantities[0].provenance.solver.solve_id)
        body2, views2 = _two_layer(6100.0)
        d, _ = sv.solve(body2, views=views2)
        self.assertNotEqual(sid, d.quantities[0].provenance.solver.solve_id)   # control: another material


class NoTemperaturePath(unittest.TestCase):
    def test_no_t_pot_no_temperature_quantities(self):
        body, views = _two_layer(6000.0)
        b2 = dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=None))
        out, _ = sv.solve(b2, views=views)
        keys = {q.key for q in out.quantities}
        self.assertFalse({"core_temperature", "cmb_temperature"} & keys)
        self.assertIn("no_temperature_path", [n.kind for n in out.notes])

    def test_control_with_t_pot(self):
        body, views = _two_layer(6000.0)
        b2 = dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=1600.0))
        out, _ = sv.solve(b2, views=views)
        self.assertIn("core_temperature", {q.key for q in out.quantities})


class UnlocatedWall(unittest.TestCase):
    def test_wall_shots_exhausted_is_no_answer(self):
        import solver.closure as c

        class Capped(Uniform):
            def state(self, p, t, guess):
                return st.Stop("domain", {"p": p}) if p > 1e10 else (self.rho, 0.0, ())
        body, _v = _two_layer(6000.0)
        saved = c.WALL_SHOTS
        try:
            c.WALL_SHOTS = 1
            out, _ = sv.solve(body, views={"core": Capped(1e5), "mantle": Capped(3000.0)})
        finally:
            c.WALL_SHOTS = saved
        self.assertIsInstance(out, result.NoAnswer, getattr(out, "text", out))
        self.assertEqual(out.evidence["budget_name"], "WALL_SHOTS")


class MaterialBytes(unittest.TestCase):
    """r2 note-4 HOLD: a changed data byte that the process read gives a new material-bytes digest (hence solve_id)."""

    def test_changed_table_byte_changes_digest(self):
        import os
        import tempfile
        from solver import legacy_materials as lm
        d = tempfile.mkdtemp()
        p = os.path.join(d, "table.json")
        with open(p, "w") as fh:
            fh.write('{"rho": 1.0}')
        with open(p) as fh:                       # read through open(): the audit hook records it
            fh.read()
        a = lm.material_bytes()
        with open(p, "w") as fh:
            fh.write('{"rho": 2.0}')
        b2 = lm.material_bytes()
        self.assertNotEqual(a, b2)
        self.assertEqual(b2, lm.material_bytes())       # control: unchanged bytes, same digest


if __name__ == "__main__":
    unittest.main()
