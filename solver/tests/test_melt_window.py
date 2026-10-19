# 용융 창 등엔트로피 시험 — 심은 닫힌 주머니가 고체 등엔트로피선으로 돌아오는지, 세 자리가 한 식과 같은지, 곡선 기울기, 이음매 주석 (melt-window 등록)
"""melt-window registration (artifacts rewrite/melt-window/reg-melt-window.frozen.md) §4.1 and §4.2's seam note.

    solver/.venv/bin/python -m unittest solver.tests.test_melt_window
    NEARSTARS_HEAVY=1 solver/.venv/bin/python -m unittest solver.tests.test_melt_window   # + full solves (PC)
"""
import math
import os
import sys
import unittest
from unittest import mock

from scipy.integrate import solve_ivp

from solver import legacy_materials as lm  # noqa: F401  (puts engine/ on sys.path)
import eos  # noqa: E402
import interior  # noqa: E402
import rtpress  # noqa: E402

HEAVY = os.environ.get("NEARSTARS_HEAVY") == "1"
GPA = 1.0e9


class _Ph:
    """The two attributes `_latent_cp` / `_latent_window` read of a phase."""
    melt = "silicate"
    melt_variant = "peridotitic"


def _psi(phi):
    """Ψ(φ) = ∫₀^φ w dφ′ for the smoothstep w over LATENT_EDGE_PHI at each edge (registration §2)."""
    e = eos.LATENT_EDGE_PHI

    def lo(x):                                   # ∫₀^x s(u/e) du, x ≤ e
        u = x / e
        return e * (u ** 3 - 0.5 * u ** 4)
    phi = min(max(phi, 0.0), 1.0)
    if phi <= e:
        return lo(phi)
    if phi <= 1.0 - e:
        return lo(e) + (phi - e)
    return lo(e) + (1.0 - 2.0 * e) + (lo(e) - lo(1.0 - phi))


class PlantedPocket(unittest.TestCase):
    """§4.1: constant c and g, a convex planted solidus (T_liq = T_sol + 150 K), the shared `_latent_window` integrated in
    P alone. A closed pocket returns to the solid isentrope; today's form (X = 0) does not."""
    C, DH = 1200.0, eos.SILICATE_MELT_DH

    def _run(self, g_gpa, a, b, k, t0, isentropic, p_end=60.0):
        sol = lambda p: a + b * p / GPA + k * (p / GPA) ** 2
        slopes = (lambda p, variant="peridotitic", d_fe=None: (b / GPA + 2.0 * k * p / GPA ** 2,) * 2) if isentropic \
            else (lambda p, variant="peridotitic", d_fe=None: (0.0, 0.0))
        ph, g = _Ph(), g_gpa / GPA
        with mock.patch.object(eos, "silicate_solidus", lambda p, v="peridotitic", d_fe=None: sol(p)), \
                mock.patch.object(eos, "silicate_liquidus", lambda p, v="peridotitic", d_fe=None: sol(p) + 150.0), \
                mock.patch.object(eos, "silicate_melt_slopes", slopes):
            r = solve_ivp(lambda x, y: [eos.Material._latent_window(ph, x * GPA, y[0], g, self.C) * GPA],
                          (0.0, p_end), [t0], rtol=1e-11, atol=1e-9, max_step=0.05, dense_output=True)
        xs = [0.01 * i for i in range(int(p_end * 100) + 1)]
        ts = [float(r.sol(x)[0]) for x in xs]
        phis = [(t - sol(x * GPA)) / 150.0 for x, t in zip(xs, ts)]
        return xs, ts, phis

    def test_closed_pocket_returns(self):
        xs, ts, phis = self._run(20.0, 1500.0, 5.0, 0.5, 1480.0, True)
        self.assertLess(phis[0], 0.0)                                       # starts solid
        self.assertGreater(max(phis), 0.2)                                  # a real pocket
        self.assertLess(phis[-1], 0.0)                                      # and leaves it
        h = [self.C * (t - 20.0 * x) + self.DH * _psi(f) for x, t, f in zip(xs, ts, phis)]
        self.assertLess((max(h) - min(h)) / abs(h[0]), 1e-6)               # assert 1: H* invariant
        self.assertLess(abs(ts[-1] - 20.0 * xs[-1] - 1480.0), 1e-5)        # assert 2: back on the solid isentrope

    def test_todays_form_misses(self):
        xs, ts, _ = self._run(20.0, 1500.0, 5.0, 0.5, 1480.0, False)       # assert 3: negative control (X = 0)
        self.assertGreater(abs(ts[-1] - 20.0 * xs[-1] - 1480.0), 1.0)

    def test_never_entering_path(self):
        a = self._run(10.0, 1500.0, 8.0, 0.4, 1495.0, True)
        b = self._run(10.0, 1500.0, 8.0, 0.4, 1495.0, False)
        self.assertLess(max(a[2]), 0.0)
        self.assertEqual(a[1], b[1])                                        # assert 4: the two forms identical
        self.assertLess(abs(a[1][-1] - 10.0 * a[0][-1] - 1495.0), 1e-9)


class ThroughSites(unittest.TestCase):
    """§4.1: S1 (`interior._adiabatic_dtdp`), S2 (`Material.grad_ad`·T/P) and S3 (`silicate_melt_mix`) each equal
    `_latent_window` of mixed and c_mix = (1 − φ)c_s + φc_ℓ computed here, not taken from the site (68 B1)."""

    def test_sites_equal_the_shared_form(self):
        m = interior.MATERIALS["silicate"]
        real = eos.Material._latent_window
        for gpa in (1, 5, 10, 15, 25, 60):
            p = gpa * GPA
            sol, liq = eos.silicate_solidus(p), eos.silicate_liquidus(p)
            for phi in (0.02, 0.1, 0.5, 0.97):
                t = sol + phi * (liq - sol)
                ph = m.phase_at(p)
                lat = m._latent_cp(ph, p, t)
                c_s, (_rl, grad_l, c_l) = m.c_p(p, t) - lat, rtpress.liquid(p, t)
                dtdp_l = grad_l * t / p
                w_s, w_l = (1.0 - phi) * c_s, phi * c_l
                c_mix = w_s + w_l
                seen = []                                      # S1's own solid dT/dP, read through the shared call
                with mock.patch.object(eos.Material, "_latent_window",
                                       staticmethod(lambda ph_, p_, t_, mixed, cp: seen.append(mixed) or mixed)):
                    interior._adiabatic_dtdp(m, p, m.density(p, t), t, 0.0)
                self.assertEqual(len(seen), 1, ("S1 does not call _latent_window", gpa, phi))
                dtdp_s = (seen[0] * (w_s + w_l) - w_l * dtdp_l) / w_s
                mixed = (w_s * dtdp_s + w_l * dtdp_l) / c_mix
                want = real(ph, p, t, mixed, c_mix)
                s1 = interior._adiabatic_dtdp(m, p, m.density(p, t), t, 0.0)
                s2 = m.grad_ad(p, t) * t / p
                s3 = lm.silicate_melt_mix(p, t, "peridotitic", m.solid_density(p, t), dtdp_s, c_s)[1]
                for name, got in (("S1", s1), ("S2", s2), ("S3", s3)):
                    self.assertLess(abs(got - want) / abs(want), 1e-12, (name, gpa, phi, got, want))


class CurveSlopes(unittest.TestCase):
    """§4.1 (68 B3): the branch-analytic slopes against differences of the curves, on every branch, both variants."""
    BRANCHES = ((1, 10, 19), (25, 80, 135), (145, 160, 175), (182, 190, 198), (250, 350, 490))
    SEAMS = (20.0, 140.0, 180.0, 200.0)

    def _fd(self, f, p, h, side=0):
        if side > 0:
            return (-3.0 * f(p) + 4.0 * f(p + h) - f(p + 2.0 * h)) / (2.0 * h)
        return (f(p + h) - f(p - h)) / (2.0 * h)

    def test_branches(self):
        for v in ("peridotitic", "chondritic"):
            for br in self.BRANCHES:
                for gpa in br:
                    p, h = gpa * GPA, gpa * GPA * 1e-6
                    got = eos.silicate_melt_slopes(p, v)
                    for i, f in enumerate((lambda q: eos.silicate_solidus(q, v), lambda q: eos.silicate_liquidus(q, v))):
                        fd = self._fd(f, p, h)
                        self.assertLess(abs(got[i] - fd) / abs(fd), 1e-7, (v, gpa, i, got[i], fd))

    def test_seams_take_the_value_branch(self):
        for v in ("peridotitic", "chondritic"):
            for gpa in self.SEAMS:
                p, h = gpa * GPA, gpa * GPA * 1e-6
                got = eos.silicate_melt_slopes(p, v)
                for i, f in enumerate((lambda q: eos.silicate_solidus(q, v), lambda q: eos.silicate_liquidus(q, v))):
                    fd = self._fd(f, p, h, side=1)              # the value at the seam P is the upper branch's
                    self.assertLess(abs(got[i] - fd) / abs(fd), 1e-6, (v, gpa, i, got[i], fd))

    def test_off_the_curve_and_iron(self):
        self.assertIsNone(eos.silicate_melt_slopes(500e9 * (1 + 1e-12)))
        self.assertIsNotNone(eos.silicate_melt_slopes(500e9))
        for gpa in (5, 60, 150):
            self.assertEqual(eos.silicate_melt_slopes(gpa * GPA, "peridotitic", 3.0),
                             eos.silicate_melt_slopes(gpa * GPA, "peridotitic"))


class SeamNoteUnit(unittest.TestCase):
    """The seam note's rule at the read (light): 0 < φ < 1 at P ≥ WINDOW_SEAM_P, through both views' entry points."""

    def test_rule(self):
        def t_at(p, phi):
            sol, liq = eos.silicate_solidus(p), eos.silicate_liquidus(p)
            return sol + phi * (liq - sol)
        n = lm.window_seam_note("m", 150 * GPA, t_at(150 * GPA, 0.3), "peridotitic")
        self.assertEqual((n.phase, n.text), (lm.WINDOW_SEAM_PHASE, lm.WINDOW_SEAM_NOTE))
        self.assertIsNone(lm.window_seam_note("m", 130 * GPA, t_at(130 * GPA, 0.3), "peridotitic"))
        self.assertIsNone(lm.window_seam_note("m", 150 * GPA, t_at(150 * GPA, -0.2), "peridotitic"))
        lv = lm.LegacyView("silicate", interior.MATERIALS["silicate"], 1600.0)
        self.assertEqual(len(lv.typed_notes(150 * GPA, t_at(150 * GPA, 0.3))), 1)
        self.assertEqual(lv.typed_notes(130 * GPA, t_at(130 * GPA, 0.3)), ())


class GradeNoteUnit(unittest.TestCase):
    """The melting-curve grade note's rule at the read (light; window-edge item, directing's N1): MELT_GRADE_P < P ≤ 500 GPa,
    through both views' entry points, whatever φ (every silicate melt read reads the curves)."""

    def test_rule(self):
        n = lm.melt_grade_note("m", 300 * GPA)
        self.assertEqual((n.phase, n.text), (lm.MELT_GRADE_PHASE, lm.MELT_GRADE_NOTE))
        self.assertIn("graded-extrapolation", n.text)
        self.assertIn("Fei+ 2021", n.text)
        self.assertEqual(eos.silicate_melt_grade(300 * GPA), ("graded-extrapolation", eos.SILICATE_MELT_GRADE_REASON))
        for p in (200 * GPA, 150 * GPA, 501 * GPA):                       # the bound itself, below, past the curve's end
            self.assertIsNone(lm.melt_grade_note("m", p), p)
        lv = lm.LegacyView("silicate", interior.MATERIALS["silicate"], 1600.0)
        sub = eos.silicate_solidus(300 * GPA) - 500.0                       # sub-solidus: no window, still the curve's read
        self.assertEqual([x.phase for x in lv.typed_notes(300 * GPA, sub)], [lm.MELT_GRADE_PHASE])
        self.assertEqual(lv.typed_notes(150 * GPA, eos.silicate_solidus(150 * GPA) - 500.0), ())
        self.assertEqual(lm.LegacyView("fe_prem", interior.MATERIALS["fe_prem"], 1600.0).typed_notes(300 * GPA, 5000.0),
                         ())                                                # control: no silicate curve, no note


@unittest.skipUnless(HEAVY, "NEARSTARS_HEAVY=1 (PC job)")
class GradeNoteAnswers(unittest.TestCase):
    """The grade note on Answer.notes from a full solve (directing's N1): MELT_GRADE_P lowered to 5 GPa, so earth 2083's
    silicate walk reads «past the bound»; one material_declared_note per silicate layer, «on» and «off»; unpatched, none
    (earth's mantle stays below 136 GPa)."""

    def _rec(self, on, grade_p=None):
        from solver import context, material_registry as mr, run_oracle as ro
        opt = context.Options(sensitivity_dt=0.0, materials="registry", silicate_records=on)
        patches = [mock.patch.object(lm, "MELT_GRADE_P", grade_p)] if grade_p is not None else []
        for pt in patches:
            pt.start()
        try:
            return ro.one("engine/bodies/earth.yaml", 2083.0, opt, False, None, mr.load())
        finally:
            for pt in patches:
                pt.stop()

    def _grade(self, rec):
        return [n for n in rec["notes"] if n["kind"] == "material_declared_note"
                and n["fields"]["text"] == lm.MELT_GRADE_NOTE]

    def test_planted_on_and_off(self):
        for on in (True, False):
            rec = self._rec(on, grade_p=5 * GPA)
            self.assertEqual(rec["outcome_kind"], "answer", on)
            per_layer = {}
            for n in self._grade(rec):
                per_layer[n["fields"]["layer"]] = per_layer.get(n["fields"]["layer"], 0) + 1
                self.assertGreater(n["fields"]["p_max"], 5 * GPA, on)
            self.assertTrue(per_layer, on)
            self.assertTrue(all(c == 1 for c in per_layer.values()), (on, per_layer))
            self.assertEqual(self._grade(self._rec(on)), [], on)          # unpatched: none


@unittest.skipUnless(HEAVY, "NEARSTARS_HEAVY=1 (PC job)")
class SeamNoteAnswers(unittest.TestCase):
    """§4.1 seam note on Answer.notes from full solves (directing's ruling on B4): WINDOW_SEAM_P lowered to 5 GPa, inside
    earth 2083's window, gives one material_declared_note per layer that reads it, «on» and «off»; unpatched, none. Earth's
    declared «off» notes are identical with and without collect's typed-notes branch."""

    def _notes(self, state, on, seam_p=None, branch=True):
        from solver import context, material_notes as mn, material_registry as mr, run_oracle as ro
        opt = context.Options(sensitivity_dt=0.0, materials="registry", silicate_records=on)
        patches = [mock.patch.object(lm, "WINDOW_SEAM_P", seam_p)] if seam_p is not None else []
        if not branch:
            patches.append(mock.patch.object(mn, "_typed_notes", lambda layer, view, path, typed: []))
        for pt in patches:
            pt.start()
        try:
            rec = ro.one("engine/bodies/earth.yaml", state, opt, False, None, mr.load())
        finally:
            for pt in patches:
                pt.stop()
        return rec

    def _seam(self, rec):
        return [n for n in rec["notes"] if n["kind"] == "material_declared_note"
                and n["fields"]["text"] == lm.WINDOW_SEAM_NOTE]

    def test_planted_on_and_off(self):
        for on in (True, False):
            rec = self._notes(2083.0, on, seam_p=5 * GPA)
            self.assertEqual(rec["outcome_kind"], "answer", on)
            seam = self._seam(rec)
            per_layer = {}
            for n in seam:
                per_layer[n["fields"]["layer"]] = per_layer.get(n["fields"]["layer"], 0) + 1
            self.assertTrue(per_layer, on)                                   # at least one layer reads it
            self.assertTrue(all(c == 1 for c in per_layer.values()), (on, per_layer))   # one per layer (68 nit 3)
            self.assertEqual(self._seam(self._notes(2083.0, on)), [], on)   # unpatched: none

    def test_off_declared_notes_unchanged(self):
        self.assertEqual(self._notes("declared", False)["notes"], self._notes("declared", False, branch=False)["notes"])


if __name__ == "__main__":
    unittest.main()
