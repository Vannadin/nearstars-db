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
        diffs = sum(1 for p, t in _grid() if view.state(p, t) != _ref(mat, p, t)
                    and not isinstance(view.state(p, t), st.Stop))
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
