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

from solver import body as b, closure as cl, context, from_v1, result, solve as sv
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



class ThicknessAboveNotInPhase1(unittest.TestCase):
    """A1 impl note 7 (r2): a thickness_above layer is refused by name, not by whichever base the pass misses.
    Control: the same body with the layer bounded by radius is not refused by this rule."""

    def _body(self, extent):
        M = 5.0e24
        layers = (b.Layer("core", "core", "x", b.Extent("mass_fraction", 0.3)),
                  b.Layer("basal", "basal_layer", "y", extent), b.Layer("mantle", "mantle", "y"))
        return b.Body("fixture", "planet", b.SurfaceState(M, t_pot=0.0), layers, b.Closure("R", 1e5, 1e8)), \
            {"core": Uniform(9000.0), "basal": Uniform(4000.0), "mantle": Uniform(3000.0)}

    def test_refused_by_name(self):
        body, views = self._body(b.Extent("thickness_above", 1.5e5, ref="core"))
        out, _ = sv.solve(body, views=views)
        self.assertEqual((out.id, out.evidence["rule"]), ("input.cross_field", "thickness_above_not_in_phase1"))

    def test_control_radius_extent(self):
        body, views = self._body(b.Extent("radius_from_centre", 3.5e6))
        out, _ = sv.solve(body, views=views)
        self.assertNotEqual(getattr(out, "evidence", {}).get("rule"), "thickness_above_not_in_phase1")


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
    """r2 note-4 HOLDs: the material bytes are a function of the engine tree only — a changed engine data byte moves
    them, and the process's history (what was solved before) does not."""

    def test_changed_engine_byte_changes_digest(self):
        """A tracked engine data file modified in the working tree moves the digest; an untracked file does not."""
        import os
        from solver import legacy_materials as lm
        tracked = os.path.join(lm._ENGINE, "ice_giant_anchor.json")
        untracked = os.path.join(lm._ENGINE, "zz_material_bytes_probe.json")
        original = open(tracked, "rb").read()
        a = lm.material_bytes()
        try:
            with open(untracked, "w") as fh:
                fh.write('{"rho": 1.0}')
            self.assertEqual(lm.material_bytes(), a)            # untracked: no effect (r2)
            with open(tracked, "wb") as fh:
                fh.write(original + b" ")
            self.assertNotEqual(lm.material_bytes(), a)         # a tracked byte changed: a new digest
        finally:
            with open(tracked, "wb") as fh:
                fh.write(original)
            os.remove(untracked)
        self.assertEqual(lm.material_bytes(), a)                # control: restored, the same digest

    def test_history_does_not_move_solve_id(self):
        """Earth alone vs Earth after Venus in one process: the same solve_id."""
        first, _ = sv.solve(earth())
        venus, _ = from_v1.load_v1("engine/bodies/venus.yaml")
        sv.solve(venus)
        again, _ = sv.solve(earth())
        sid = lambda a: a.quantities[0].provenance.solver.solve_id
        self.assertEqual(sid(first), sid(again))


class ClosureDiscontinuous(unittest.TestCase):
    """Phase-1 design notes 8–9: a root must meet tol_F (a), and each side's F at x* ± δ, ± 2δ must lie on one line
    through F(x*) (a″). Planted steps of F on the two-layer uniform fixture (R closure) and on its boundary_mass
    inverse (r2 CB1), and a planted slope kink at the root that must pass (r2 on note 9)."""

    def _bodies(self):
        body, views = _two_layer(6000.0)
        ans, x0 = sv.solve(body, views=views)
        self.assertIsInstance(ans, result.Answer, getattr(ans, "text", None))
        layers = (b.Layer("core", "core", "x"), b.Layer("mantle", "mantle", "y"))
        inv = b.Body("fixture-inverse", "planet", body.surface, layers, b.Closure("boundary_mass", 0.05, 0.95, "core"),
                     radius=b.Declared(x0, "m"))
        return (body, views, x0), (inv, views)

    def _slope(self, body, views, x):
        lo, hi = (sv.inward(body, sv._views_at(body, views, xx), xx, context.Options()).F for xx in
                  (x * (1 - 1e-4), x * (1 + 1e-4)))
        return (hi - lo) / (2e-4 * x)

    def _slope_sign(self, body, views, x):
        return math.copysign(1.0, self._slope(body, views, x))

    def _with_step(self, body, views, x_step, jump, kink=0.0):
        """F + jump past x_step; with `kink`, F + kink·(x − x_step) past x_step instead (a slope change, no jump)."""
        orig = sv.inward

        def stepped(bd, vw, x, opt):
            got = orig(bd, vw, x, opt)
            if not isinstance(got, st.Stop) and got.F is not None and x > x_step:
                got.F += jump + kink * (x - x_step)
            return got
        sv.inward = stepped
        try:
            return sv.solve(body, views=views)
        finally:
            sv.inward = orig

    def test_guard_skipped_is_noted(self):
        """r2 on 55117864 (1): a lone solved scan point with F = 0.0 exactly is a root with no bracket; the guard cannot
        run there, and the answer says so (Note closure_guard_skipped), never silently."""
        body, views = _two_layer(6000.0)
        _a, x0 = sv.solve(body, views=views)
        x_s = min(cl.scan_points(body.closure.lo, body.closure.hi, context.Options().n_scan), key=lambda z: abs(z - x0))
        orig = sv.inward

        def lone(bd, vw, x, opt):
            if x != x_s:
                return st.Stop("refused", {"planted": "every trial but one scan point refuses", "x": x})
            got = orig(bd, vw, x, opt)
            got.F = 0.0
            return got
        sv.inward = lone
        try:
            ans, x = sv.solve(body, views=views)
        finally:
            sv.inward = orig
        self.assertIsInstance(ans, result.Answer, getattr(ans, "text", None))
        self.assertEqual(x, x_s)
        self.assertIn("closure_guard_skipped", [n.kind for n in ans.notes])
        ans2, _x = sv.solve(body, views=views)                       # control: a bracketed root carries no such note
        self.assertNotIn("closure_guard_skipped", [n.kind for n in ans2.notes])

    def test_planted_steps(self):
        (fwd, views, r0), (inv, iviews) = self._bodies()
        ans, x_inv = sv.solve(inv, views=iviews)
        self.assertIsInstance(ans, result.Answer, getattr(ans, "text", None))
        for name, body, vw, x0 in (("R", fwd, views, r0), ("boundary_mass", inv, iviews, x_inv)):
            sg = self._slope_sign(body, vw, x0)
            with self.subTest(closure=name, control="(iii) no step: the same root"):
                got, x = self._with_step(body, vw, math.inf, 0.0)
                self.assertIsInstance(got, result.Answer, getattr(got, "text", None))
                self.assertEqual(x, x0)
            with self.subTest(closure=name, control="(ii) step just past the root: (a′)"):
                got, x = self._with_step(body, vw, x0 * (1 + 1e-9), sg * 1e-5)
                self.assertIsInstance(got, result.Refusal)
                self.assertEqual(got.id, "solve.closure_discontinuous")
                self.assertEqual(got.evidence["check"], "probe")
            with self.subTest(closure=name, control="(v) a 50 % slope change at the root passes (note 9, r2)"):
                got, x = self._with_step(body, vw, x0, 0.0, kink=0.5 * self._slope(body, vw, x0))
                self.assertIsInstance(got, result.Answer, getattr(got, "text", None))
                self.assertLess(abs(x / x0 - 1.0), 1e-12)          # Brent's path differs; the root does not
            with self.subTest(closure=name, control="(iv) a step below tol_F fires nothing"):
                got, x = self._with_step(body, vw, x0 * (1 + 1e-9), sg * 1e-11)
                self.assertIsInstance(got, result.Answer, getattr(got, "text", None))
        with self.subTest(control="(i) the root closes on the jump: (a)"):
            sg = self._slope_sign(fwd, views, r0)
            # F(x) − jump·sg for x ≤ x_step: the sign change sits at x_step, where F jumps by 1e-5
            got, x = self._with_step(fwd, views, r0 * (1 - 1e-7), sg * 1e-5)
            self.assertIsInstance(got, result.Refusal)
            self.assertEqual(got.id, "solve.closure_discontinuous")
            self.assertEqual(got.evidence["check"], "residual")
            self.assertGreater(abs(got.evidence["F_root"]), got.evidence["tol_F"])


class GuardRedTeam(unittest.TestCase):
    """Directing's red-team of the closure guard as a class (phase-1 design note 11): one planted case per input the
    residual check and the probe depend on. Covered elsewhere: a step at the root and just past it on the R and
    boundary_mass closures, a kink at the root, a sub-tolerance step, a lone F = 0 root (ClosureDiscontinuous); a
    floor-closed centre (FloorGuard: a dense centre answers); the accepted pass's own N_acc (test_a6_trace)."""

    def setUp(self):
        self.body, self.views = _two_layer(6000.0)
        self.rt = []
        self._orig_rt, self._orig_inward = sv._root_tolerance, sv.inward

        def rt(*a):
            r = self._orig_rt(*a)
            self.rt.append(r)
            return r
        sv._root_tolerance = rt
        ans, self.x0 = sv.solve(self.body, views=self.views)
        self.assertIsInstance(ans, result.Answer, getattr(ans, "text", None))
        self.delta0 = self.rt[-1]["delta"]
        self.scan = cl.scan_points(self.body.closure.lo, self.body.closure.hi, context.Options().n_scan)

    def tearDown(self):
        sv._root_tolerance, sv.inward = self._orig_rt, self._orig_inward

    def _solve(self, alter):
        """Solve with each pass's F replaced by alter(x, F) (a Stop from alter refuses that trial)."""
        orig = self._orig_inward

        def wrapped(bd, vw, x, opt):
            got = orig(bd, vw, x, opt)
            if isinstance(got, st.Stop) or got.F is None:
                return got
            f = alter(x, got.F)
            if isinstance(f, st.Stop):
                return f
            got.F = f
            return got
        sv.inward = wrapped
        try:
            return sv.solve(self.body, views=self.views)
        finally:
            sv.inward = orig

    def _f_at(self, x):
        return self._orig_inward(self.body, sv._views_at(self.body, self.views, x), x, context.Options()).F

    def test_root_exactly_at_a_scan_point(self):
        """Venus's member: the root is itself a scan point; the slope skips it and δ stays finite."""
        x_s = min(self.scan, key=lambda z: abs(z - self.x0))
        f_s = self._f_at(x_s)
        ans, x = self._solve(lambda xx, f: f - f_s)
        self.assertIsInstance(ans, result.Answer, getattr(ans, "text", None))
        self.assertEqual(x, x_s)
        self.assertGreater(self.rt[-1]["delta"], 0.1 * self.delta0)

    def test_root_a_hair_from_a_scan_point(self):
        """Mars member at rtol/10: a root 1e-10 relative from a scan point; δ must not collapse (note 10)."""
        x_s = min(self.scan, key=lambda z: abs(z - self.x0))
        f_h = self._f_at(x_s * (1 + 1e-10))
        ans, x = self._solve(lambda xx, f: f - f_h)
        self.assertIsInstance(ans, result.Answer, getattr(ans, "text", None))
        self.assertGreater(self.rt[-1]["delta"], 0.1 * self.delta0)

    def test_walls_on_one_side(self):
        """Every trial below 0.999·x0 refuses: the slope and the reference come from the solved stretch; it answers."""
        cut = 0.999 * self.x0
        ans, x = self._solve(lambda xx, f: st.Stop("refused", {"planted": "wall", "x": xx}) if xx < cut else f)
        self.assertIsInstance(ans, result.Answer, getattr(ans, "text", None))
        self.assertLess(abs(x / self.x0 - 1.0), 1e-12)

    def test_wall_within_two_delta_refuses(self):
        """A wall δ/2 below the root: the lower probe refuses, so the solve refuses by name, never answers."""
        cut = self.x0 - 0.5 * self.delta0
        ans, x = self._solve(lambda xx, f: st.Stop("refused", {"planted": "wall", "x": xx}) if xx < cut else f)
        self.assertIsInstance(ans, result.Refusal)
        self.assertEqual((ans.id, ans.evidence["check"]), ("solve.closure_discontinuous", "probe"))

    def test_a_wall_between_the_root_and_its_scan_point(self):
        """r2 GB1: the trials from 0.5·x0 to 0.999·x0 refuse (the nearest scan point below among them) and F jumps by 10
        beyond them; the slope must come from inside the solved stretch, not from the scan point across the wall."""
        s0 = self.rt[-1]["s"]
        lo_w, hi_w = 0.5 * self.x0, 0.999 * self.x0
        sg = math.copysign(1.0, self._f_at(1.001 * self.x0) - self._f_at(0.9995 * self.x0))

        def alter(xx, f):
            if lo_w <= xx <= hi_w:
                return st.Stop("refused", {"planted": "wall band", "x": xx})
            return f - 10.0 * sg if xx < lo_w else f                 # away from zero: no second root
        self.rt.clear()
        ans, x = self._solve(alter)
        self.assertIsInstance(ans, result.Answer, getattr(ans, "text", None))
        self.assertLess(abs(x / self.x0 - 1.0), 1e-12)
        self.assertLess(abs(self.rt[-1]["s"] / s0 - 1.0), 0.5)          # the local slope, not the jump across the wall

    def test_a_wall_between_the_probes_and_the_reference(self):
        """r2 GB2: trials from 0.5·x0 to x0 − 5·δ_clean refuse and F is offset by 10 beyond them; no solved trial ≥ 4δ
        below lies inside the stretch, so the lower side refuses «no_solved_reference» and never reads past the wall."""
        lo_w, hi_w = 0.5 * self.x0, self.x0 - 5.0 * self.delta0         # 2δ < 5·δ0 < 4δ here (δ ≈ 1.6·δ0)
        sg = math.copysign(1.0, self._f_at(1.001 * self.x0) - self._f_at(0.9995 * self.x0))

        def alter(xx, f):
            if lo_w <= xx <= hi_w:
                return st.Stop("refused", {"planted": "wall band", "x": xx})
            return f - 10.0 * sg if xx < lo_w else f
        self.rt.clear()
        ans, x = self._solve(alter)
        d = self.rt[-1]["delta"]
        self.assertTrue(2.0 * d < self.x0 - hi_w < 4.0 * d, (d, self.x0 - hi_w))   # the case is the one meant
        self.assertIsInstance(ans, result.Refusal, getattr(ans, "quantities", None))
        self.assertEqual((ans.id, ans.evidence["check"]), ("solve.closure_discontinuous", "probe"))
        lower = next(sd for sd in ans.evidence["probes"]["sides"] if sd["side"] < 0)
        self.assertEqual(lower["stop"], "no_solved_reference")

    def test_very_flat_and_very_steep_F(self):
        """F scaled by 1e-3 and 1e3: δ follows the slope (capped by the scan pair), and the root is unchanged."""
        for k in (1e-3, 1e3):
            with self.subTest(scale=k):
                ans, x = self._solve(lambda xx, f, k=k: k * f)
                self.assertIsInstance(ans, result.Answer, getattr(ans, "text", None))
                self.assertLess(abs(x / self.x0 - 1.0), 1e-12)

    def test_composition_closure_step_refuses(self):
        """The third closure kind: a step just past the composition root refuses by the probe."""
        from solver.tests.test_s10 import CompositionClosure, XCore
        cc = CompositionClosure()
        body = cc._body()
        views = {"core": XCore(0.0), "mantle": Uniform(3000.0)}
        ans, x0 = sv.solve(body, views=views)
        self.assertIsInstance(ans, result.Answer, getattr(ans, "text", None))
        orig = self._orig_inward
        lo, hi = (orig(body, sv._views_at(body, views, z), z, context.Options()).F for z in (x0 * 0.99, x0 * 1.01))
        sg = math.copysign(1.0, hi - lo)

        def stepped(bd, vw, x, opt):
            got = orig(bd, vw, x, opt)
            if not isinstance(got, st.Stop) and got.F is not None and x > x0 * (1 + 1e-9):
                got.F += sg * 1e-5
            return got
        sv.inward = stepped
        try:
            ans, x = sv.solve(body, views=views)
        finally:
            sv.inward = orig
        self.assertIsInstance(ans, result.Refusal)
        self.assertEqual((ans.id, ans.evidence["check"]), ("solve.closure_discontinuous", "probe"))


if __name__ == "__main__":
    unittest.main()
