# 어댑터 대 옛 단계 함수 — 097a8aa3 의 _integrate_raw 를 실제로 돌려 단계마다 (재료, P, T, 밀도) 를 엿듣고 어댑터와 비트 대조 (등록 S4, r2 B3)
"""S4 acceptance against the old stage function itself (r2 S4 HOLD B3), not a restated expression.

The old stage function is a closure inside engine/interior.py `_integrate_raw` (097a8aa3, :1545–1580). Its density
path ends in `porosity_at(mat, pp, phi0, p_cap)` with the raw stage pressure pp; just before that it calls the
material's density (or COLUMN_STEAM's, or falls back to rho0). This test wraps both, runs real old integrations,
and for every stage compares adapter.density(pp, T_stage) with the old rr_rho·(1 − φ) bit for bit.
Bodies: Earth-like (fe_prem + silicate, T_pot 1600 K), Dante-like (porous silicate, φ₀ 0.39, P_LAB_MAX cap),
Venus-like hot surface (SURF_RHO at P ≤ 0) and a gas giant (h_he envelope: p_stop = 1 bar).

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_adapter_stage
"""
import functools
import unittest

from solver import legacy_materials as lm

interior, eos = lm.interior, lm.eos
M_E = interior.EARTH_MASS_KG
SEAMS = (19.0e9, 35.0e9, 23.83e9)


def _capture(run):
    """Run `run()` with the old stage's density and porosity calls recorded. Returns [(mat, pp, t, rho_old, phi0,
    p_cap)] per stage, rho_old being the old rr_rho after the porosity factor."""
    last = {}
    rows = []
    patched = []

    def wrap_density(cls):
        orig = cls.__dict__.get("density")
        if orig is None:
            return

        @functools.wraps(orig)
        def density(self, p, t=0.0, t_pot=0.0, *a, **k):
            try:
                v = orig(self, p, t, t_pot, *a, **k)
            except eos.PhaseGap:
                last["call"] = (self, p, t, None)
                raise
            last["call"] = (self, p, t, v)
            return v
        setattr(cls, "density", density)
        patched.append((cls, "density", orig))

    classes = {type(m) for m in interior.MATERIALS.values()} | {type(interior.COLUMN_STEAM),
                                                                interior.BasalConstDensity}
    for c in classes:
        wrap_density(c)
    orig_por = interior.porosity_at

    def porosity_at(mat, pp, phi0, p_cap=None):
        phi = orig_por(mat, pp, phi0, p_cap)
        call = last.pop("call", None)
        if call is not None:
            owner, p_eval, t, v = call
            rho_raw = mat.rho0 if v is None else v
            rows.append((mat, owner, pp, t, rho_raw * (1.0 - phi), phi0, p_cap, p_eval))
        return phi
    interior.porosity_at = porosity_at
    try:
        run()
    finally:
        interior.porosity_at = orig_por
        for cls, name, orig in patched:
            setattr(cls, name, orig)
    return rows


def _seam_near(mat, p, rel=1e-9):
    lo, hi = mat.stencil_bounds(p) if hasattr(mat, "stencil_bounds") else (0.0, float("inf"))
    return any(0.0 < b < float("inf") and abs(p - b) <= rel * b for b in (lo, hi))


def _check(tc, rows, t_pot, p_stop, column_steam=False):
    """Every stage matches bit for bit, except the old landing-step clamp (C164 `stage_pmin`, interior.py:1569:
    a stage of a step that lands on a phase or seam boundary is read on the old side). The new solver lands every
    step on such a boundary (events), so it has no such stage; each clamped stage must be read within 1e-9 of a
    boundary of its material (measured: boundary × (1 + 4e-12)), and they are counted (measured 0.04–0.4 %)."""
    n, clamped = 0, 0
    for mat, owner, pp, t, rho_old, phi0, p_cap, p_eval in rows:
        if owner is interior.COLUMN_STEAM and not column_steam:
            continue
        view = lm.LegacyView(getattr(mat, "name", "?"), mat, t_pot, p_stop, phi0=phi0, p_cap=p_cap,
                             column_steam=column_steam)
        expect_eval = view._at_floor(max(pp, p_stop)) if pp > 0.0 else view._at_floor(max(1.0e5, p_stop))
        if p_eval is not None and pp > 0.0 and p_eval != expect_eval:
            tc.assertGreater(p_eval, expect_eval)
            tc.assertTrue(_seam_near(mat, p_eval), f"clamp away from a boundary: {getattr(mat, 'name', mat)} {p_eval}")
            clamped += 1
            continue
        got = view.density(pp, t)
        tc.assertEqual(got, rho_old, f"{getattr(mat, 'name', mat)} pp={pp!r} t={t!r}")
        n += 1
    tc.assertLess(clamped, max(1, n // 20))
    return n


class OldStage(unittest.TestCase):
    def setUp(self):
        lm.reset_engine_state()

    def test_earth_like(self):
        rows = _capture(lambda: interior._integrate_raw(3.6e11, M_E, 0.325, 0.0, "fe_prem",
                                                         t_center=5000.0, t_pot=1600.0))
        n = _check(self, rows, 1600.0, 0.0)
        self.assertGreater(n, 1000)
        for s in SEAMS[:2]:   # fe_prem's thermal-set seams are visited within ±1 %
            self.assertTrue(any(abs(r[2] - s) <= 0.01 * s for r in rows), s)
        self.assertTrue(any(abs(r[2] - SEAMS[2]) <= 0.01 * SEAMS[2] for r in rows))
        self.assertTrue(any(r[2] <= 0.0 for r in rows))           # the last half-step crosses the surface

    def test_dante_like_porosity(self):
        m = 0.00025987 * M_E
        p_cap = getattr(interior, "P_LAB_MAX", None)
        rows = _capture(lambda: interior._integrate_raw(2.0e8, m, 0.0, 0.0, "fe_prem", phi0=0.39, p_cap=p_cap))
        n = _check(self, rows, 0.0, 0.0)
        self.assertGreater(n, 100)
        self.assertTrue(any(r[5] > 0.0 for r in rows))

    def test_hot_surface(self):
        rows = _capture(lambda: interior._integrate_raw(3.0e11, 0.815 * M_E, 0.30, 0.0, "fe_prem",
                                                         t_center=4500.0, t_pot=1900.0))
        n = _check(self, rows, 1900.0, 0.0)
        self.assertGreater(n, 100)
        self.assertTrue(any(r[2] <= 0.0 for r in rows))

    def _envelope_rows(self):
        # an Earth-mass body with a 2 % h_he envelope: the run reaches the envelope (≈ 6e4 h_he stages)
        return _capture(lambda: interior._integrate_raw(2.0e11, M_E, 0.05, 0.0, "fe_prem", gmf=0.02,
                                                         t_center=6000.0, t_pot=0.0))

    def test_gas_envelope_p_stop(self):
        p_stop = interior.MATERIALS["h_he"].p_floor
        self.assertGreater(p_stop, 0.0)
        rows = self._envelope_rows()
        self.assertGreater(sum(1 for r in rows if getattr(r[0], "name", "") == "h_he"), 1000)
        # stages with 0 < pp < p_stop: the p_stop clamp is what the old stage applies there
        self.assertGreater(sum(1 for r in rows if 0.0 < r[2] < p_stop), 0)
        self.assertGreater(_check(self, rows, 0.0, p_stop), 1000)

    def test_mutation_without_p_stop_fails(self):
        p_stop = interior.MATERIALS["h_he"].p_floor
        rows = [r for r in self._envelope_rows() if 0.0 < r[2] < p_stop]
        bad = 0
        for mat, owner, pp, t, rho_old, phi0, p_cap, p_eval in rows:
            v = lm.LegacyView("x", mat, 0.0, 0.0, phi0=phi0, p_cap=p_cap)     # p_stop dropped
            if v.density(pp, t) != rho_old:
                bad += 1
        self.assertGreater(bad, 0)

    def test_control_wrong_p_stop_differs(self):
        rows = _capture(lambda: interior._integrate_raw(3.6e11, M_E, 0.325, 0.0, "fe_prem",
                                                         t_center=5000.0, t_pot=1600.0))
        surface = [r for r in rows if r[2] <= 1.0e5]
        self.assertTrue(surface)
        mat, _o, pp, t, rho_old, phi0, p_cap, _pe = surface[-1]
        view = lm.LegacyView("x", mat, 1600.0, 5.0e8)
        self.assertNotEqual(view.density(pp, t), rho_old)



class BranchesNotReachedByOldRuns(unittest.TestCase):
    """r2 S4-fix B3: the floor clamp and the hot-surface ρ₀ fallback are not reached by plausible old integrations
    (a hot rocky surface refuses with SpinodalGap deeper first; a stage below a fit floor ends the old step first).
    They are pinned here against the old lines (interior.py:1533–1542 `_at_floor`, :1570–1577 SURF_RHO at 097a8aa3),
    each with a mutation that fails."""

    def test_at_floor(self):
        mat = interior.MATERIALS["fe_s_13wt_19gpa"]
        lo = mat.shoot_lo
        view = lm.LegacyView("fe_s_13wt_19gpa", mat, 1600.0)
        p = 0.5 * lo
        self.assertEqual(view.density(p, 2000.0), mat.density(lo, 2000.0, 1600.0))
        mutant = lm.LegacyView("fe_s_13wt_19gpa", mat, 1600.0)
        mutant._at_floor = lambda q: q                                   # the clamp removed
        got = mutant.density(p, 2000.0)
        self.assertTrue(not isinstance(got, float) or got != mat.density(lo, 2000.0, 1600.0))

    def test_surface_fallback(self):
        mat = interior.MATERIALS["silicate"]
        view = lm.LegacyView("silicate", mat, 1600.0)
        self.assertEqual(view.density(0.0, 5500.0), mat.rho0)
        saved = interior.SURF_RHO
        try:
            interior.SURF_RHO = False                                    # the old knob off: ρ₀ directly
            self.assertEqual(lm.LegacyView("silicate", mat, 1600.0).density(0.0, 1600.0), mat.rho0)
        finally:
            interior.SURF_RHO = saved
        cool = lm.LegacyView("silicate", mat, 1600.0).density(0.0, 1600.0)
        self.assertNotEqual(cool, mat.rho0)                              # mutation-like: the 1 bar read is used

if __name__ == "__main__":
    unittest.main()
