# 옛 물질 어댑터 시험 — 등록된 프로세스 상태 전체 되돌리기, 지구·금성·화성 층 재료의 밀도·단열 기울기 비트 일치 (등록 S4)
"""S4 acceptance of rewrite/phase1-a1-impl.frozen.md, each with its negative control.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_adapter
"""
import math
import unittest

from solver import context, legacy_materials as lm
from solver import stepper as st

eos, interior, process_state = lm.eos, lm.interior, lm.process_state

T_POT = 1600.0
N_P, N_T = 20, 10                      # 200 (P, T) per material


def stacks():
    """The layer materials of the Earth, Venus and Mars stacks at 097a8aa3, built by the old stack builder
    (interior._stack; Mars inside its Fe–S–O–C core and declared-mantle contexts, plus the basal layer)."""
    core = interior.COMPOSITIONS["earth_like"][3]
    out = {"earth": [m for _f, m in interior._stack(0.325, 0.0, "fe_prem")],
           "venus": [m for _f, m in interior._stack(0.30, 0.0, core)]}
    mars_wt = {"SiO2": 46.66, "Al2O3": 3.49, "MgO": 32.81, "CaO": 2.66, "FeO": 13.68, "Na2O": 0.69}
    with interior._sulphur_core(0.16, "box_ceiling"), interior._mantle(mars_wt):
        mars = [m for _f, m in interior._stack(0.20, 0.0, interior.COMPOSITIONS["earth_like"][3])]
        mars.append(interior.BasalConstDensity(4050.0))
        out["mars"] = [(m, _grid_ref(m)) for m in mars]   # evaluate inside the contexts the old solve uses
    for b in ("earth", "venus"):
        out[b] = [(m, _grid_ref(m)) for m in out[b]]
    return out


def _grid():
    for i in range(N_P):
        p = 1e5 * (4e11 / 1e5) ** (i / (N_P - 1))
        for j in range(N_T):
            yield p, 300.0 + 6000.0 * j / (N_T - 1)


def _ref(mat, p, t):
    """The old stage expressions (interior.py :1562–1580 density, :1603 dT/dP) with p_stop 0 and no porosity."""
    lo = getattr(mat, "shoot_lo", 0.0)
    at = lambda q: lo if (lo and q < lo) else q
    try:
        rho = mat.density(at(max(p, 0.0)), t, T_POT)
        g = interior._adiabatic_dtdp(mat, max(p, 0.0), mat.density(at(max(p, 0.0)), t, T_POT), t, T_POT)
    except eos.PhaseGap as exc:
        return ("refused", type(exc).__name__, str(exc))
    return (rho, g)


def _grid_ref(mat):
    view = lm.LegacyView(getattr(mat, "name", "basal"), mat, T_POT)
    rows = []
    for p, t in _grid():
        got = view.state(p, t)
        if isinstance(got, st.Stop):
            got = ("refused", got.record.kind, got.record.message_old)
        else:
            got = got[:2]
        rows.append((p, t, got, _ref(mat, p, t)))
    return rows


class SameAsOldStage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lm.reset_engine_state()
        cls.stacks = stacks()

    def test_bit_identical_per_material(self):
        n = 0
        for body, mats in self.stacks.items():
            for mat, rows in mats:
                self.assertEqual(len(rows), N_P * N_T)
                for p, t, got, ref in rows:
                    self.assertEqual(got, ref, f"{body} {getattr(mat, 'name', mat)} P={p:.6g} T={t:.6g}")
                    n += 1
        self.assertGreaterEqual(n, 200 * 6)

    def test_control_wrong_t_pot_differs(self):
        # the silicate's thermal pressure is referenced to the body's T_pot (W-L11-02); fe_prem's is not
        mat = interior._stack(0.325, 0.0, "fe_prem")[1][1]
        view = lm.LegacyView("silicate", mat, T_POT + 100.0)
        diffs = sum(1 for p, t in _grid() if not isinstance(view.state(p, t), st.Stop)
                    and view.state(p, t)[:2] != _ref(mat, p, t))
        self.assertGreater(diffs, 0)


class Reset(unittest.TestCase):
    def _plant(self):
        import fe_liquid, water_hot
        water_hot._LAST_DENSITY = (1.0, 2.0, 3.0)
        fe_liquid._CACHE[("planted", 1.0, 2.0)] = 42.0
        interior.ADAPTIVE_STATS["accepted"] = 7
        return fe_liquid, water_hot

    def _clean(self, fe_liquid, water_hot):
        return (water_hot._LAST_DENSITY == (0.0, 0.0, 0.0) and ("planted", 1.0, 2.0) not in fe_liquid._CACHE
                and interior.ADAPTIVE_STATS["accepted"] == 0)

    def test_every_registry_entry_reset(self):
        mods = self._plant()
        touched = lm.reset_engine_state()
        self.assertTrue(self._clean(*mods))
        names = {(m, n) for m, n, _k in touched}
        expected = set()
        for (m, n), (kind, why, _i) in process_state.REGISTRY.items():
            if kind == process_state.FLAG:
                continue
            if (m, n) in lm.CONSTANT_MEMOS:
                continue
            if (m, n) in lm.IMPORT_REGISTRIES:
                self.assertIn("at import", why)          # the exclusion is exactly the import-time registries
                continue
            try:
                mod = __import__(m)
            except ImportError:
                continue
            if hasattr(mod, n):
                expected.add((m, n))
        self.assertEqual(names, expected)

    def test_flags_untouched(self):
        before = lm.flags_snapshot()
        lm.reset_engine_state()
        self.assertEqual(lm.flags_snapshot(), before)
        self.assertIsInstance(interior.COMPOSITIONS["earth_like"], tuple)

    def test_memo_filled_before_import_does_not_survive(self):
        import fe_liquid
        fe_liquid._CACHE[("stale-from-before", 0.0, 0.0)] = 1.0
        lm.reset_engine_state()
        self.assertNotIn(("stale-from-before", 0.0, 0.0), fe_liquid._CACHE)
        for (m, n), (kind, _w, init) in process_state.REGISTRY.items():
            if kind != process_state.MEMO or (m, n) in lm.IMPORT_REGISTRIES:
                continue
            try:
                mod = __import__(m)
            except ImportError:
                continue
            if hasattr(mod, n):
                if (m, n) not in lm.CONSTANT_MEMOS:
                    self.assertTrue(lm._at_rest((m, n), getattr(mod, n)), (m, n))

    def test_control_snapshot_refuses_filled_memo(self):
        """Importing the adapter after a memo was filled must fail by name (fresh interpreter)."""
        import subprocess, sys
        code = ("import sys; sys.path.insert(0, 'engine'); import fe_liquid; fe_liquid._CACHE[('x', 0.0, 0.0)] = 1;"
                " import solver.legacy_materials")
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("fe_liquid._CACHE", r.stderr)

    def test_control_start_only_reset_leaves_memos(self):
        mods = self._plant()
        process_state.reset()                      # the old hand-picked reset: START entries only
        self.assertFalse(self._clean(*mods))
        lm.reset_engine_state()

    def test_context_build_resets(self):
        mods = self._plant()
        ctx = context.build(context.Options(), {})
        self.assertTrue(self._clean(*mods))
        self.assertEqual(ctx.trace[0]["kind"], "legacy_reset")


if __name__ == "__main__":
    unittest.main()


class StartFilledBeforeImport(unittest.TestCase):
    def test_start_goes_back_to_registry_initial(self):
        """r2 S4 B1: a START value set before the adapter's import must not become the reset value."""
        import subprocess, sys
        code = ("import sys; sys.path.insert(0, 'engine'); import water_hot; water_hot._LAST_DENSITY = (1.0, 2.0, 3.0);"
                " import solver.legacy_materials as lm; lm.reset_engine_state();"
                " import water_hot as w; print(w._LAST_DENSITY)")
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.strip().splitlines()[-1], "(0.0, 0.0, 0.0)")


class SurfaceFallback(unittest.TestCase):
    def test_fallback_is_counted_and_noted(self):
        mat = interior._stack(0.325, 0.0, "fe_prem")[1][1]
        view = lm.LegacyView("silicate", mat, 1600.0)
        got = view.state(0.0, 5500.0)
        self.assertNotIsInstance(got, st.Stop)
        self.assertEqual(got[0], mat.rho0)
        self.assertEqual(got[2], ("surface_rho0_fallback",))
        self.assertEqual(view.surface_fallbacks, 1)

    def test_control_cool_surface_no_fallback(self):
        mat = interior._stack(0.325, 0.0, "fe_prem")[1][1]
        view = lm.LegacyView("silicate", mat, 1600.0)
        got = view.state(0.0, 1600.0)
        self.assertEqual(view.surface_fallbacks, 0)
        self.assertNotIn("surface_rho0_fallback", got[2])


class WaterNotPorted(unittest.TestCase):
    def test_water_layer_refuses(self):
        from solver import body as b
        for name in ("h2o", "h2o_liquid", "h2o_hot"):
            layer = b.Layer("ice", "ice" if "ice" in b.ROLES["roles"] else "mantle", name)
            self.assertIsNone(lm.resolve(layer, 300.0, 0.0), name)

    def test_control_silicate_resolves(self):
        from solver import body as b
        self.assertIsNotNone(lm.resolve(b.Layer("m", "mantle", "silicate"), 1600.0, 0.0))


class AtRestStrict(unittest.TestCase):
    """r2 S4-fix: a keyed cache holding a falsy value is not at rest; a counter filled before import fails too."""

    def _fresh(self, plant):
        import subprocess, sys
        code = f"import sys; sys.path.insert(0, 'engine'); {plant}; import solver.legacy_materials"
        return subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)

    def test_falsy_value_in_keyed_cache_fails(self):
        r = self._fresh("import fe_liquid; fe_liquid._CACHE[('x', 0.0, 0.0)] = 0")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("fe_liquid._CACHE", r.stderr)

    def test_counter_filled_before_import_fails(self):
        r = self._fresh("import interior; interior.SURF_RHO_FALLBACKS[0] = 7")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("interior.SURF_RHO_FALLBACKS", r.stderr)

    def test_control_clean_import_works(self):
        r = self._fresh("pass")
        self.assertEqual(r.returncode, 0, r.stderr)


class ExcludedSetLiteral(unittest.TestCase):
    """r2 S4-fix N6: the excluded set written out, not recomputed with the adapter's own filter."""

    def test_excluded(self):
        self.assertEqual(set(lm.IMPORT_REGISTRIES), {("provisional", "REGISTRY"), ("registry", "_REGISTRY")})
        self.assertEqual(set(lm.CONSTANT_MEMOS), {
            ("rtpress", "_VMIN_TAB"), ("ice_fr2015", "_GL_NODES"), ("mantle_composition", "_TABLE_PHASE"),
            ("mantle_composition", "_TABLES"), ("rocky_roster", "_ROWS"), ("eos", "_SPINODAL"),
            ("eos", "_PRESSURE_FAST"), ("water_table", "_CACHE"), ("water2_table", "_CACHE"), ("paleos", "_FACTS"),
            ("check_refs", "BASENAMES"), ("check_refs", "CACHE")})
        flags = {k for k, v in process_state.REGISTRY.items() if v[0] == process_state.FLAG}
        self.assertEqual(flags, {("interior", "COMPOSITIONS"), ("parallel_points", "_FN"), ("interior", "_REOPEN"),
                                 ("interior", "_SOLVE_DEPTH"), ("interior", "_LAST_GRAZE"), ("interior", "_LOOP_TRIALS"),
                                 ("interior", "_CALL"), ("interior", "_ENTRY"), ("interior", "_PIN"),
                                 ("structure_grid", "BUILDING"), ("structure_grid", "JUDGE_A_ONLY"),
                                 ("structure_grid", "GRID_DIR")})


class WaterMixture(unittest.TestCase):
    def test_mixture_with_water_refuses(self):
        wet = eos.mix("rock_ice_test", "test", (interior.MATERIALS["silicate"], 0.5), (interior.MATERIALS["h2o"], 0.5))
        self.assertTrue(lm._has_water(wet))

    def test_control_dry_mixture_resolves(self):
        dry = eos.mix("rock_iron_test", "test", (interior.MATERIALS["silicate"], 0.5),
                      (interior.MATERIALS["fe_prem"], 0.5))
        self.assertFalse(lm._has_water(dry))
