# §T 물리 시험(나머지) — 닫힘 왕복, 분할 불변성, 사건 감시 상한, T_pot 고상선 자 — 각자 음성 대조와 함께 (설계 §T, 사후 노트 4)
"""phase1-design.frozen.md §T «Physics tests», the items not covered elsewhere, as amended by post-freeze note 4.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_t_physics
"""
import dataclasses
import math
import statistics
import unittest

from solver import body as bd, context, events, from_v1, result, rhs, solve as sv
from solver import legacy_materials as lm
from solver import stepper as st
from solver.tests.test_events import M as M_SYN, Synthetic

OPT = context.Options(sensitivity_dt=0.0)
T1 = 1e-9


def _q(a):
    return {q.key: q.point for q in a.quantities}


def _earth():
    e, _ = from_v1.load_v1("engine/bodies/earth.yaml")
    return e


class ClosureRoundTrip(unittest.TestCase):
    """Mass conservation and closure: Earth's declared CMF → forward R; the boundary_mass inverse at that R returns the
    CMF to ≤ 1e-9 (measured 4.8e-10). Control: a planted wrong residual sign (F → |F|) gives solve.no_bracket."""

    def _inverse(self):
        e = _earth()
        a, _ = sv.solve(e, OPT)
        layers = tuple(dataclasses.replace(l, extent=None) if l.id == "core" else l for l in e.layers)
        return dataclasses.replace(e, layers=layers, closure=bd.Closure("boundary_mass", 0.001, 0.999, layer="core"),
                                   radius=bd.Declared(_q(a)["radius"]))

    def test_cmf_returns(self):
        b, x = sv.solve(self._inverse(), OPT)
        self.assertIsInstance(b, result.Answer, getattr(b, "text", None))
        self.assertLess(abs(x - 0.325) / 0.325, 1e-9)

    def test_control_wrong_sign(self):
        inv = self._inverse()
        orig = rhs.residual
        rhs.residual = lambda m, r, rho, rs: abs(orig(m, r, rho, rs))
        try:
            b, _ = sv.solve(inv, OPT)
        finally:
            rhs.residual = orig
        self.assertEqual(getattr(b, "id", None), "solve.no_bracket")


class SplitInvariance(unittest.TestCase):
    """Earth's mantle re-declared as 5 same-material layers by mass: per key |Δ| ≤ max(T1, |y(rtol) − y(rtol/10)|)
    (note 4 item 2). Control: a 1 K temperature jump planted at one internal split interface moves a key past that
    bound (moving a split between same-material layers would change nothing, so it cannot be the control)."""

    @classmethod
    def setUpClass(cls):
        e = _earth()
        cls.base = _q(sv.solve(e, OPT)[0])
        fine = _q(sv.solve(e, dataclasses.replace(OPT, rtol=OPT.rtol / 10.0))[0])
        cls.bound = {k: max(T1, abs(fine[k] - v) / abs(v)) for k, v in cls.base.items() if v}
        cls.e = e

    def _split(self, jumps=None):
        core, mantle, lid = self.e.layers
        n = 5
        parts = [dataclasses.replace(mantle, id=f"mantle{i}",
                                     extent=bd.Extent("mass_fraction", 0.675 / n))
                 for i in range(n - 1)]
        parts.append(dataclasses.replace(mantle, id="mantle"))
        body = dataclasses.replace(self.e, layers=(core, *parts, lid))
        if jumps:
            body = dataclasses.replace(body, jumps={**dict(body.jumps), **jumps})
        return _q(sv.solve(body, OPT)[0])

    def test_within_resolution(self):
        got = self._split()
        for k, b in self.bound.items():
            self.assertLessEqual(abs(got[k] - self.base[k]) / abs(self.base[k]), b, k)

    def test_control_moved_split_is_seen(self):
        got = self._split({"mantle1/mantle2": 1.0})
        self.assertTrue(any(abs(got[k] - self.base[k]) / abs(self.base[k]) > b for k, b in self.bound.items()))


class EventGuard(unittest.TestCase):
    """Note 4 item 3. The registered fixture (g = 1e-3 sin(P / 1 kPa)) trips the guard at the default caps
    (test_events.Chatter). With every cap × 100 the pass must terminate (end, a cap, or MAX_STEPS_SOLVE); with all caps
    off and a small max_steps it stops on MAX_STEPS_SOLVE."""

    def _run(self, k, max_steps):
        view = Synthetic(lambda p: 1600.0 + 2e-8 * p - 1e-3 * math.sin(p / 1e3))
        r0 = (3 * M_SYN / (4 * math.pi * 5000.0)) ** (1 / 3)
        o = st.Options(rtol=1e-10, floors=rhs.floors(M_SYN, r0), h0=1e-3 * M_SYN, h_min=1e-15 * M_SYN,
                       h_max=M_SYN / 20, max_steps=max_steps, event_rewalks=8 * k, event_min_progress=1e-9 * M_SYN / k,
                       event_restarts_step=4 * k, event_restarts_run=2000 * k)
        return st.run(rhs.make_rhs(view), M_SYN, (r0, 0.0, 1600.0, 1600.0, 0.0, 0.0), 1e-6 * M_SYN, o,
                      events.onset_event(view))

    def test_default_caps_trip(self):
        self.assertEqual(self._run(1, 200000).stop.kind, "chatter")

    def test_caps_x100_terminate(self):
        self.assertIn(self._run(100, 200000).stop.kind, ("end", "chatter", "max_steps"))

    def test_caps_off_stop_on_max_steps(self):
        res = self._run(10 ** 9, 100)
        self.assertEqual(res.stop.kind, "max_steps")


M_RULER = 0.05 * 5.972e24
RULER_T0, RULER_STEP, RULER_N = 1900.0, 0.05, 41          # declared before the run (note 4 item 1): the solidus onset
                                                            # event fires there (≈ 1700–2100 K on this body)


def _coreless(t):
    return bd.Body("ruler", "planet", bd.SurfaceState(M_RULER, t_pot=t), (bd.Layer("rock", "mantle", "silicate"),),
                   bd.Closure("R", 0.05 * 6.371e6, 30 * 6.371e6))


def _ruler(key="core_pressure"):
    ys = [_q(sv.solve(_coreless(RULER_T0 + RULER_STEP * i), OPT)[0])[key] for i in range(RULER_N)]
    dy = [(ys[i + 1] - ys[i]) / abs(ys[i]) for i in range(RULER_N - 1)]
    med = statistics.median(dy)
    return max(abs(d - med) for d in dy)


class Ruler(unittest.TestCase):
    """R-C157-8 restated in T_pot (§T, note 4 item 1): max |dy − median| ≤ 1e-6 between 0.05 K neighbours across the
    solidus onset. Control: with onset events off, a planted 1e-2 relative density step above the solidus must be
    seen (> 1e-6). Measured on 21 points (999f1be7): events off 2.1e-6, events on 5.2e-7; a 1e-5 step (note 4's
    «e.g.») stayed at 7e-8 in every mode, since the adaptive steps resolve a step that small."""

    def test_smooth(self):
        self.assertLessEqual(_ruler(), 1e-6)

    def test_control_planted_step(self):
        orig_state, orig_onset = lm.LegacyView.state, events.onset_events

        def stepped(self, p, t, guess):
            got = orig_state(self, p, t, guess)
            if isinstance(got, st.Stop):
                return got
            g = events._curve_at(self.mat, "고상선", p, t)
            return (got[0] * (1.0 + 1e-2), *got[1:]) if g is not None and g > 0.0 else got
        lm.LegacyView.state, events.onset_events = stepped, (lambda mat, p_stop=0.0: [])
        try:
            self.assertGreater(_ruler(), 1e-6)
        finally:
            lm.LegacyView.state, events.onset_events = orig_state, orig_onset


if __name__ == "__main__":
    unittest.main()
