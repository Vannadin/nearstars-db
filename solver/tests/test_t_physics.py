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
T_KEYS = ("core_temperature", "cmb_temperature")      # the temperatures a lid's fixed point sets (EVC note 6 item 1)


def _q(a):
    return {q.key: q.point for q in a.quantities}


def _earth():
    e, _ = from_v1.load_v1("engine/bodies/earth.yaml")
    return e


class ClosureRoundTrip(unittest.TestCase):
    """Mass conservation and closure: Earth's declared CMF → forward R; the boundary_mass inverse at that R returns the
    CMF to ≤ 1e-9 (measured 4.8e-10). Control: a planted wrong residual sign (F → |F|) gives solve.no_bracket."""

    def _inverse(self):
        e = _earth()          # an inversion keeps no structural lid (R-LITHO-6, owner Q3; P1R-G4-C-08): both legs lid-free
        e = dataclasses.replace(e, layers=tuple(l for l in e.layers if l.thermal != "conductive"))
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

    #: design note 19 (K = 8 noise stop): core_pressure's bound also reads k·σ̂/|P_c|, σ̂ over 11 re-walks at the base
    #: root (x*·(1 + j·1e-10), j = −5…5, a line in x, 9 dof), k = √2·t₉⁻¹(1 − 0.05/2) for one comparison
    K_NOISE = 3.199173339927709
    NOISE_KEYS = ("core_pressure",)

    @classmethod
    def setUpClass(cls):
        e = _earth()
        ans, x = sv.solve(e, OPT)
        cls.base = _q(ans)
        sigma = cls._pass_noise(e, x)
        fine = _q(sv.solve(e, dataclasses.replace(OPT, rtol=OPT.rtol / 10.0))[0])
        # design note 7: T keys of a lidded body carry the lid fixed point's own tolerance, which the rtol pair cannot see
        lidded = any(l.thermal == "conductive" for l in e.layers)
        floor = {k: (OPT.lid_t_tol if lidded and k in T_KEYS else 0.0) for k in cls.base}
        noise = {k: (cls.K_NOISE * sigma[k] / abs(v) if k in cls.NOISE_KEYS else 0.0) for k, v in cls.base.items() if v}
        cls.bound = {k: max(T1, abs(fine[k] - v) / abs(v), floor[k], noise[k]) for k, v in cls.base.items() if v}
        cls.e = e

    @staticmethod
    def _pass_noise(e, x):
        """{key: σ̂}: each key's residual sd about a line in x over 11 accepted passes at x·(1 + j·1e-10)."""
        views = sv._views(e, registry=sv.registry_for(e, OPT), silicate=OPT.silicate_records)
        xs, rows = [], []
        for j in range(-5, 6):
            xx = x * (1.0 + j * 1e-10)
            vx = sv._views_at(e, views, xx)
            p = sv.inward(e, vx, xx, OPT, want_graze=False)
            xs.append(xx)
            rows.append({q.key: q.point for q in sv._quantities(e, p, "", xx, vx)})
        mx = statistics.fmean(xs)
        out = {}
        for k in rows[0]:
            ys = [r[k] for r in rows]
            my = statistics.fmean(ys)
            sxx = sum((u - mx) ** 2 for u in xs)
            slope = sum((u - mx) * (v - my) for u, v in zip(xs, ys)) / sxx
            out[k] = math.sqrt(sum((v - my - slope * (u - mx)) ** 2 for u, v in zip(xs, ys)) / (len(xs) - 2))
        return out

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
RULER_T0, RULER_STEP, RULER_N = 1762.5, 0.05, 41          # melt-window post-freeze note 1 (directing's rule): the
# midpoint of the first and last T_pot of the scan 1650–1900 K by 25 K whose accepted pass lands the solidus onset on
# the isentropic window (1675 and 1850 K). The old 1900 K (note 4 item 1: «≈ 1700–2100 K on this body») lies outside
# that range there: the walk stays in the window to the centre, so no onset was crossed and test_smooth was vacuous


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
    solidus onset. Control: with onset events off, a planted 1e-2 relative density step that no event lands must be
    seen (> 1e-6). Measured on 21 points (999f1be7): events off 2.1e-6, events on 5.2e-7; a 1e-5 step (note 4's
    «e.g.») stayed at 7e-8 in every mode, since the adaptive steps resolve a step that small.
    melt-window post-freeze note 1: the step was planted above the solidus, so the control read the window's form (the
    flat window's jumpy solidus exit made it 4.69e-6; the isentropic window exits smoothly, 3.58e-8). It is re-planted
    in a fixed P band, [0.40, 0.50]·P_c of the unplanted 1900 K solve, which the walk crosses at every T_pot of the
    control: 2.82e-6 at d8eb7aa7, 1.49e-6 at the isentropic window (both > 1e-6, pre-declared)."""

    def test_smooth(self):
        self.assertLessEqual(_ruler(), 1e-6)

    def test_onset_lands_in_every_pass(self):
        """melt-window post-freeze note 1 (68 B1): the ruler's subject is the solidus onset landing, so the onset event
        is landed in each of the RULER_N accepted passes (the pass at the solved x)."""
        for i in range(RULER_N):
            body = _coreless(RULER_T0 + RULER_STEP * i)
            _ans, x = sv.solve(body, OPT)
            out = sv.inward(body, sv._views_at(body, sv._views(body), x), x, OPT)
            self.assertIn("onset:고상선", out.events, i)                 # the ruler's subject exactly (68's nit)

    def test_control_planted_step(self):
        orig_state, orig_onset = lm.LegacyView.state, events.onset_events

        p_c = _q(sv.solve(_coreless(RULER_T0), OPT)[0])["core_pressure"]
        lo, hi = 0.40 * p_c, 0.50 * p_c                  # melt-window post-freeze note 1: a fixed P band

        def stepped(self, p, t, guess):
            got = orig_state(self, p, t, guess)
            if isinstance(got, st.Stop):
                return got
            return (got[0] * (1.0 + 1e-2), *got[1:]) if lo <= p <= hi else got
        lm.LegacyView.state, events.onset_events = stepped, (lambda mat, p_stop=0.0: [])
        try:
            self.assertGreater(_ruler(), 1e-6)
        finally:
            lm.LegacyView.state, events.onset_events = orig_state, orig_onset


if __name__ == "__main__":
    unittest.main()
