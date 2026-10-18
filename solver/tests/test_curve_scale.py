# 곡선 착지 척도 시험 — g = P − P_b(T) 의 척도가 T·|dP_b/dT| 항까지 세는지(심은 κ≈124 곡선·되걷기 T 지터), 기울기 없는 곡선은 비트 그대로, «off» 는 비트 그대로 (venus-pocket 등록)
"""venus-pocket registration (artifacts rewrite/venus-pocket): a record curve event's landing scale is the largest of
max|P_b| and |P_b| + T·|dP_b/dT| over the curve as read.

    solver/.venv/bin/python -m unittest solver.tests.test_curve_scale
    NEARSTARS_HEAVY=1 solver/.venv/bin/python -m unittest solver.tests.test_curve_scale   # + «off» bit identity (PC)
"""
import contextlib
import math
import os
import struct
import unittest
from unittest import mock

from solver import context, events, material_assemblage as ma, material_registry as mr, stepper as st
from solver.from_v1 import thaw

#: planted re-step round-off in T_ad [K]: ±(0.5–1)×, deterministic in the step length's bits
JITTER_K = 1.0e-9
HEAVY = os.environ.get("NEARSTARS_HEAVY") == "1"
SILICATE = ("silicate_slb_default_bse", "silicate_slb_earth_dmm_wh2005", "silicate_slb_mars_khan2022")
_REG = []


def _reg():
    if not _REG:
        _REG.append(mr.load())
    return _REG[0]


def _view(rid):
    reg = _reg()
    return ma.view(thaw(reg.get(rid)), reg.tables[rid], 1600.0)


def _curves(v):
    return [c for _b, kind, c in v.transitions() if kind != "melting" and c.get("form") == "assemblage_curve"]


def _old_scale(view, curve):
    """curve_p_scale at 35b7a24b: max|P_b| on the 50 K samples, 1e9 where absent."""
    pbs = [abs(pb) for t in events.CURVE_SCALE_TS if (pb := view.boundary_pressure(curve, t)) is not None]
    return max(pbs) if pbs and max(pbs) > 0.0 else 1.0e9


class PlantedLanding(unittest.TestCase):
    """A curve steep in T (κ = T·|dP_b/dT| / max|P_b| ≈ 124, venus edge275 is 91) and a planted re-step round-off in
    T_ad of ±(0.5–1)·1e-9 K (10× the sd measured at edge275, so the control fails by a margin). Under max|P_b| the g spread
    (|dP_b/dT|·δT, 0.025–0.05 Pa) exceeds tol (6.5e-4 Pa) and the event chatters; under the full scale (tol 0.081 Pa) it lands. Without
    the planted jitter both land, so the jitter is what the scale must cover."""
    M, R, PB0, K, T_LO, T_HI = 5.972e24, 6.371e6, 3.0e8, 5.0e7, 1595.0, 1607.0

    def _pb(self, t):
        return self.PB0 + self.K * (t - 1600.0)

    def _curve(self):
        test = self

        class Curve:
            def boundary_pressure(self, curve, t):
                return test._pb(t) if test.T_LO <= t <= test.T_HI else None

            def curve_slope_points(self, curve):
                return ((test.T_LO, test._pb(test.T_LO), test.K), (test.T_HI, test._pb(test.T_HI), test.K))
        return Curve()

    def _run(self, scale, jitter, h0=1e-3):
        from solver import rhs
        pb = self._pb

        class Flat:
            def state(self, p, t, guess):
                return 3500.0, 9.6e-9
        real = st.step

        def jittered(f, x, y, h, k1, stage_f=None):
            out = real(f, x, y, h, k1, stage_f)
            if isinstance(out, st.Stop):
                return out
            u = struct.unpack("<q", struct.pack("<d", h))[0] * 2654435761 % 2001 / 2000.0       # [0, 1], from h's bits
            d = math.copysign(0.5 + 0.5 * u, u - 0.5) * JITTER_K                           # ±[0.5, 1]·JITTER_K
            y_new = tuple(v + (d if j == 2 else 0.0) for j, v in enumerate(out[0]))
            return (y_new,) + tuple(out[1:])
        rs = rhs.r_scale_of(self.M, 3.0 * self.M / (4.0 * math.pi * self.R ** 3))
        o = st.Options(rtol=1e-10, floors=rhs.floors(self.M, rs), h0=h0 * self.M, h_min=1e-15 * self.M,
                       h_max=self.M / 20.0, max_steps=200000, event_rewalks=32)
        e = st.Event("phase:planted", lambda m, y: y[1] - pb(y[2]),       # read past the scale's range too: a step
                     # that leaves [T_LO, T_HI] would otherwise skip the crossing (None does not cross)
                     scale=scale, terminal=False, seam=True, component=1)
        with mock.patch.object(st, "step", jittered if jitter else real):
            return st.run(rhs.make_rhs(Flat()), self.M, (self.R, 0.0, 1600.0, 1600.0, 0.0, 0.0), 0.5 * self.M, o, [e])

    def test_scale_counts_the_t_term(self):
        c = self._curve()
        self.assertEqual(_old_scale(c, {}), self._pb(1600.0))          # the 50 K samples see 1600 K only
        self.assertEqual(events.curve_p_scale(c, {}), self._pb(self.T_HI) + self.T_HI * self.K)
        self.assertGreater(self.T_HI * self.K / self._pb(self.T_HI), 100.0)

    def test_lands_under_the_full_scale(self):
        full = events.curve_p_scale(self._curve(), {})
        old = max(self._pb(self.T_LO), self._pb(self.T_HI))
        for h0 in (1e-3, 7.3e-4, 1.37e-3):
            self.assertEqual(self._run(full, True, h0).stop.kind, "end", h0)
            self.assertEqual(self._run(old, True, h0).stop.kind, "chatter", h0)   # negative control: the P term alone
            self.assertEqual(self._run(old, False, h0).stop.kind, "end", h0)      # control: no jitter, P suffices


class RecordScales(unittest.TestCase):
    def test_edge275(self):
        """venus's pocket curve: two rows (2250 K, 2300 K), a cut run, so its 100 K extension's upper reach end sets
        the scale: P_b(2400)·(1 + 2400·ln(P_2300/P_2250)/50)."""
        v = _view("silicate_slb_default_bse")
        (c,) = [c for b, _k, c in v.transitions() if b[0].startswith("edge275:")]
        rows = v._events[c["id"]].rows
        k = math.log(rows[1]["p_b"] / rows[0]["p_b"]) / (rows[1]["t"] - rows[0]["t"])
        pb = v.boundary_pressure(c, 2400.0)
        self.assertAlmostEqual(events.curve_p_scale(v, c), pb + 2400.0 * pb * k, delta=1e-9 * pb * 2400.0 * k)
        self.assertGreater(events.curve_p_scale(v, c) / _old_scale(v, c), 90.0)

    def test_never_smaller_and_flat_curves_bit_identical(self):
        """Every assemblage curve: the scale never falls below 35b7a24b's; a curve with no slope anywhere keeps it bit
        for bit."""
        flat = 0
        for rid in SILICATE:
            v = _view(rid)
            for c in _curves(v):
                new, old = events.curve_p_scale(v, c), _old_scale(v, c)
                self.assertGreaterEqual(new, old, (rid, c))
                if all(s == 0.0 for _t, _p, s in v.curve_slope_points(c)):
                    flat += 1
                    self.assertEqual(new, old, (rid, c))
        self.assertGreater(flat, 0)

    def test_other_forms_give_no_slope_points(self):
        v = _view("silicate_slb_default_bse")
        self.assertEqual(v.curve_slope_points({"form": "clapeyron"}), ())


@unittest.skipUnless(HEAVY, "NEARSTARS_HEAVY=1 (PC job)")
class OffUnchanged(unittest.TestCase):
    """Records «off» read no assemblage curve: every off solve here is bit-identical with the slope term removed
    (curve_slope_points → ()), at the declared state and one hot T_pot per body. Control: venus 2284.29 «on» refuses
    solve.event_chatter without the term and answers with it."""

    def _solve(self, stem, t_pot, on, term):
        """run_oracle's record of (body, state): a T_pot state is solved on the body's member, as the rounds do."""
        from solver import run_oracle as ro
        opt = context.Options(sensitivity_dt=0.0, materials="registry", silicate_records=on)
        patch = (contextlib.nullcontext() if term
                 else mock.patch.object(ma.AssemblageView, "curve_slope_points", lambda self, c: ()))
        with patch:
            return ro.one(f"engine/bodies/{stem}.yaml", "declared" if t_pot is None else t_pot, opt, False, None, _reg())

    def test_off_bit_identical(self):
        for stem, t in (("earth", None), ("earth", 2083.0), ("venus", None), ("venus", 2284.29), ("mars", None),
                        ("mars", 2075.0)):
            a, b = self._solve(stem, t, False, True), self._solve(stem, t, False, False)
            self.assertEqual(a, b, (stem, t))

    def test_on_control(self):
        old, new = self._solve("venus", 2284.29, True, False), self._solve("venus", 2284.29, True, True)
        self.assertEqual((old["outcome_kind"], old["refusal"]["id"]), ("refusal", "solve.event_chatter"))
        self.assertEqual(new["outcome_kind"], "answer")


if __name__ == "__main__":
    unittest.main()
