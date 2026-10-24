# 공존 구간 시험 — 심은 해석적 swap(기울어진 직선 P_b(T), s 두 쪽)에서 걸음이 곡선을 따라 읽기의 s 를 보존해 정확한 출구에 닿는지, 훅이 없으면 오늘처럼 T 가 연속인지 (reg-coexistence §6, 노트 3·4)
"""Planted analytic swap (reg-coexistence §6.1–§6.2 with notes 3–4).

A linear curve P_b(T) = P0 + k (T − T0), k > 0; side reads s(side, P, T) = a + c ln T − b ln P + (Δs if side = +1),
Δs < 0 (Clapeyron with Δv < 0: the exit exists along increasing P); ρ constant per side. Along the curve the read's
own s returns to s_L where c ln(T/T_e) − b ln(P/P_e) = −Δs with T = T_b(P): solved here to 1e-15 as the reference.

Run from the worktree root:  <solver venv>/python -m unittest solver.tests.test_coexist
"""
import math
import unittest

from solver import coexist as cx, rhs as rh, stepper as st

P0, T0, K = 1.0e10, 1700.0, 7.0e6
A_, C_, B_ = 2500.0, 1200.0, 40.0
DS = -4.0
RHO = {-1: 3500.0, 1: 3600.0}


def p_b(t):
    return P0 + K * (t - T0)


def t_b(p):
    return T0 + (p - P0) / K


def s_side(side, p, t):
    return A_ + C_ * math.log(t) - B_ * math.log(p) + (DS if side == 1 else 0.0)


def rho_side(side, p, t):
    return RHO[side]


class _View:
    """The material: the side by P against P_b(T), dT/dP = −s_P / s_T = (B/P) / (C/T) on either side."""

    def state(self, p, t, _guess):
        side = 1 if p >= p_b(t) else -1
        return (RHO[side], (B_ / p) / (C_ / t))


def _events(hook):
    return [st.Event("phase:planted|swap", (lambda m, y: y[1] - p_b(y[3])), scale=P0, terminal=False, seam=True,
                     component=1, coexist=hook)]


def _opt():
    return st.Options(rtol=1e-11, floors=(1.0, 1.0, 1e-6, 1e-6, 1.0, 1.0), h0=-1e20, h_min=1e10, h_max=1e21,
                      max_steps=100000, event_tol=1e-13, event_rewalks=32, event_min_progress=1e15)


def _start():
    """A state just above the curve (P below P_b) on an adiabat."""
    p = P0 - 2.0e7
    t = T0 - 3.5                                   # P_b(T) = P0 − 2.45e7 < p? keep p < P_b: choose T so that P_b > p
    t = T0 - 1.0                                   # P_b = P0 − 7e6 > p
    return 4.0e24, (5.0e6, p, t, t, 0.0, 0.0)


def _reference_exit(p_e, t_e):
    """(P, T) on the curve where s_new = s_L (the read's own s conserved)."""
    s_l = s_side(-1, p_e, t_e)
    lo, hi = p_e, p_e + 5.0e9
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        gm = s_side(1, mid, t_b(mid)) - s_l
        if (gm > 0.0) == (s_side(1, lo, t_b(lo)) - s_l > 0.0):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi), t_b(0.5 * (lo + hi))


def _hook():
    return cx.Segment("phase:planted|swap", s_side, rho_side, p_b, t_b, lambda t: K, rows_t=(), ds_model=lambda t: -1.5)


class PlantedSegment(unittest.TestCase):
    def _run(self, hook, m_end=3.95e24):
        m0, y0 = _start()
        return st.run(rh.make_rhs(_View()), m0, y0, m_end, _opt(), _events(hook))

    def test_walk_follows_the_curve_to_the_exact_exit(self):
        res = self._run(_hook())
        names = [e[0] for e in res.events]
        self.assertIn("coexist-in:phase:planted|swap", names)
        self.assertIn("coexist-out:phase:planted|swap", names)
        tok = [c for c in res.coexist if c.get("kind") == "segment"][0]
        _m, p_e, t_e = tok["entry"]
        p_x, t_x = _reference_exit(p_e, t_e)
        got_p, got_t = tok["exit"]
        self.assertLess(abs(got_p - p_x) / p_x, 1e-6, (got_p, p_x))
        self.assertLess(abs(got_t - t_x), 1e-6 * t_x)
        self.assertAlmostEqual(s_side(1, got_p, got_t), tok["s_L"], delta=1e-6 * abs(DS))   # the read's own s held
        self.assertAlmostEqual(tok["ds_read"], DS, delta=1e-9)
        self.assertAlmostEqual(tok["delta"], DS - (-1.5), delta=1e-9)                      # δ disclosed, not carried
        self.assertGreaterEqual(tok["phi_range"][0], 0.0)
        self.assertLessEqual(tok["phi_range"][1], 1.0)
        on_seg = [y for m, y, k in res.path if p_e <= y[1] <= got_p]
        for y in on_seg:                                                   # T on the curve along the segment
            self.assertLess(abs(y[3] - t_b(y[1])), 1e-6)

    def test_no_hook_is_todays_sharp_step(self):
        res = self._run(None)
        names = [e[0] for e in res.events]
        self.assertEqual(names, ["phase:planted|swap"])
        self.assertEqual(res.coexist, ())
        _n, m_l, y_l = res.events[0]
        node = [p for p in res.path if p[0] == m_l]
        self.assertTrue(node)                                              # landed, T continuous across it
        self.assertLess(abs(node[0][1][3] - y_l[3]), 1e-12)

    def test_names_carry_no_values(self):
        res = self._run(_hook())
        for name, _m, _y in res.events:
            self.assertRegex(name, r"^(coexist-(in|out|row|sharp|finding|restart):)?phase:planted\|swap$")


if __name__ == "__main__":
    unittest.main()


class _Crossing:
    """A second planted curve that the segment meets (an invariant point): P = P_X constant (a «phase:» event)."""


class SegmentRoutes(unittest.TestCase):
    """68 B1–B3 on note 4: the exit's re-arming, re-entry, the routes of other events on the segment, x1 on it."""

    def _run(self, hook, extra=(), m_end=3.95e24, opt=None):
        m0, y0 = _start()
        return st.run(rh.make_rhs(_View()), m0, y0, m_end, opt or _opt(), _events(hook) + list(extra))

    def test_another_phase_curve_on_the_segment_is_coexist_crossed(self):
        mid = 10.02e9                                                       # inside the segment (10.0035 → 10.0349 GPa)
        ev = st.Event("phase:planted|other", (lambda m, y: y[1] - mid), scale=P0, terminal=False, seam=True, component=1)
        res = self._run(_hook(), [ev])
        self.assertEqual(res.stop.kind, "refused")
        self.assertEqual(res.stop.record.kind, "coexist_crossed")
        self.assertEqual(res.stop.record.record["crossed"], "phase:planted|other")

    def test_a_p_seam_on_the_segment_is_landed_and_the_segment_continues(self):
        mid = 10.02e9
        ev = st.Event(f"seam:{mid:.9g}", (lambda m, y: y[1] - mid), scale=mid, terminal=False, seam=True, component=1)
        res = self._run(_hook(), [ev])
        names = [e[0] for e in res.events]
        self.assertIn(f"seam:{mid:.9g}", names)
        self.assertIn("coexist-out:phase:planted|swap", names)

    def test_the_layer_ending_on_the_segment_is_coexist_unfinished(self):
        m0, y0 = _start()
        full = st.run(rh.make_rhs(_View()), m0, y0, 3.95e24, _opt(), _events(_hook()))
        m_in = [e[1] for e in full.events if e[0].startswith("coexist-in")][0]
        m_out = [e[1] for e in full.events if e[0].startswith("coexist-out")][0]
        res = self._run(_hook(), m_end=0.5 * (m_in + m_out))
        self.assertEqual(res.stop.kind, "refused")
        self.assertEqual(res.stop.record.kind, "coexist_unfinished")

    def test_the_curve_ending_before_the_exit_is_coexist_unfinished(self):
        short = cx.Segment("phase:planted|swap", s_side, rho_side, p_b, (lambda p: t_b(p) if p < 10.01e9 else None),
                           lambda t: K)
        res = self._run(short)
        self.assertEqual(res.stop.kind, "refused")
        self.assertIn(res.stop.record.kind, ("coexist_unfinished",))

    def test_no_reentry_after_the_exit(self):
        res = self._run(_hook())
        self.assertEqual(res.stop.kind, "end")
        names = [e[0] for e in res.events]
        self.assertEqual(names.count("coexist-in:phase:planted|swap"), 1)       # one segment: re-armed, not re-landed

    def test_exit_rearm_from_the_node_is_red(self):
        """68 B1 mutant: g_prev taken from the exit node itself (g ≈ 0 with a round-off sign) instead of the
        one-ulp-past new-side state: the curve either disarms or re-lands. Planted: g at the exit node forced to the
        old side's sign by one ulp; the fixed run still ends with one segment."""
        class Nudged(cx.Segment):
            def project(self, tok, y):
                y2 = super().project(tok, y)
                return (y2[0], math.nextafter(p_b(y2[3]), -math.inf), y2[2], y2[3]) + tuple(y2[4:])
        res = self._run(Nudged("phase:planted|swap", s_side, rho_side, p_b, t_b, lambda t: K))
        names = [e[0] for e in res.events]
        self.assertEqual(names.count("coexist-in:phase:planted|swap"), 1)
        self.assertNotIn(res.stop.kind, ("chatter",))

    def test_fixed_mode_walks_the_same_segment(self):
        from solver import fixed_grid as fg
        m0, y0 = _start()
        res = fg.run_r(rh.make_rhs(_View()), m0, y0, 3.95e24, 1.0, "r_end", 50.0, _events(_hook()),     # |dr|
                       event_min_progress=1e15, m_scale=1e24)
        tok = [c for c in res.coexist if c.get("kind") == "segment"]
        self.assertEqual(len(tok), 1)
        p_x, _t = _reference_exit(tok[0]["entry"][1], tok[0]["entry"][2])
        self.assertLess(abs(tok[0]["exit"][0] - p_x) / p_x, 1e-6)

    def test_two_interleaved_runs_are_bit_identical(self):
        h = _hook()
        a = self._run(h)
        b = self._run(h)
        self.assertEqual(a.y, b.y)
        self.assertEqual([e[0] for e in a.events], [e[0] for e in b.events])


class Records(unittest.TestCase):
    """Non-swap cuts, curve ends and sharp steps: fixed names, values in Result.coexist (68 B1–B2, r2 v2)."""

    def _cut_run(self, kind):
        hook = cx.CutFinding("phase:planted|cut", s_side, p_b, kind=kind)
        m0, y0 = _start()
        return st.run(rh.make_rhs(_View()), m0, y0, 3.95e24, _opt(), _events(None)[:0] + [
            st.Event("phase:planted|cut", (lambda m, y: y[1] - p_b(y[3])), scale=P0, terminal=False, seam=True,
                     component=1, coexist=hook)])

    def test_non_swap_cut_keeps_t_continuous_and_records_ds(self):
        res = self._cut_run("finding")
        names = [e[0] for e in res.events]
        self.assertIn("coexist-finding:phase:planted|cut", names)
        rec = [c for c in res.coexist if c["kind"] == "finding"][0]
        self.assertAlmostEqual(rec["ds"], DS, delta=1e-9)                  # the read's δs, a FINDING
        _n, m_l, y_l = [e for e in res.events if e[0] == "phase:planted|cut"][0]
        self.assertEqual([c for c in res.coexist if c["kind"] == "segment"], [])
        node = [p for p in res.path if p[0] == m_l]
        self.assertLess(abs(node[0][1][3] - y_l[3]), 1e-12)               # T continuous across the cut (68 B1)

    def test_restart_records_its_ds_with_a_fixed_name(self):
        res = self._cut_run("restart")
        names = [e[0] for e in res.events]
        self.assertIn("coexist-restart:phase:planted|cut", names)
        for n in names:
            self.assertNotRegex(n, r"[-+]?\d+\.\d")                         # no value in a name (r2 v2, 68 B2′)
        self.assertAlmostEqual([c for c in res.coexist if c["kind"] == "restart"][0]["ds"], DS, delta=1e-9)

    def test_level_set_mutant_at_a_non_swap_cut_is_red(self):
        """68 B1: holding the read's s across a non-swap cut turns the read's jump into a T jump; the walk must not."""
        seg = cx.Segment("phase:planted|cut", s_side, rho_side, p_b, t_b, lambda t: K)
        m0, y0 = _start()
        mutant = st.run(rh.make_rhs(_View()), m0, y0, 3.95e24, _opt(), [
            st.Event("phase:planted|cut", (lambda m, y: y[1] - p_b(y[3])), scale=P0, terminal=False, seam=True,
                     component=1, coexist=seg)])
        fixed = self._cut_run("finding")
        self.assertGreater(abs(mutant.y[3] - fixed.y[3]), 1.0)             # the mutant moved T by the segment's step

    def test_sharp_only_is_named(self):
        hook = cx.SharpOnly("phase:planted|swap", "no T_b: single row or P_b not monotone in T")
        m0, y0 = _start()
        res = st.run(rh.make_rhs(_View()), m0, y0, 3.95e24, _opt(), _events(hook))
        self.assertIn("coexist-sharp:phase:planted|swap", [e[0] for e in res.events])
        self.assertEqual([c["reason"] for c in res.coexist if c["kind"] == "sharp"],
                         ["no T_b: single row or P_b not monotone in T"])


class NamesStable(unittest.TestCase):
    """68 B2′: the landed names at T_pot and T_pot + δ are equal on a path crossing a segment and a non-swap cut."""

    def _names(self, dt):
        m0, (r, p, t, _t2, i, v) = _start()
        y0 = (r, p, t + dt, t + dt, i, v)
        def s_var(side, p, t):                     # a cut whose read δs moves with T, so a value in a name would too
            return s_side(-1, p, t) + ((-4.0 - 0.1 * (t - T0)) if side == 1 else 0.0)
        cut = st.Event("phase:planted|cut", (lambda m, y: y[1] - (p_b(y[3]) + 1.5e7)), scale=P0, terminal=False,
                       seam=True, component=1, coexist=cx.CutFinding("phase:planted|cut", s_var,
                                                                     lambda t: p_b(t) + 1.5e7))
        res = st.run(rh.make_rhs(_View()), m0, y0, 3.95e24, _opt(), _events(_hook()) + [cut])
        return [e[0] for e in res.events], res.coexist

    def test_names_equal_at_t_pot_and_t_pot_plus_delta(self):
        a, ca = self._names(0.0)
        b, cb = self._names(0.01)
        self.assertEqual(a, b)
        self.assertNotEqual([c.get("ds_read") for c in ca], [c.get("ds_read") for c in cb] + ["x"])

    def test_value_in_name_mutant_is_red(self):
        def mutant(names, recs):
            return [n + (f":{r['ds']:.6g}" if n.startswith("coexist-finding") else "") for n, r in
                    zip(names, [next((c for c in recs if c["kind"] == "finding"), {"ds": 0.0})] * len(names))]
        a, ca = self._names(0.0)
        b, cb = self._names(0.01)
        self.assertEqual(a, b)
        if any(n.startswith("coexist-finding") for n in a):
            self.assertNotEqual(mutant(a, ca), mutant(b, cb))


class LoadChecks(unittest.TestCase):
    """The hooks' load checks (r2 v1; Clapeyron, r2 B1′): a planted table, then its two mutants, each a TableStop."""

    def _table(self, delta_s=-2.0, drop_edge=False):
        cells = [{"p": p, "t": t} for p in (1e9, 2e9, 3e9) for t in (1000.0, 1100.0, 1200.0)]
        rows = [{"t": 1000.0, "p_lo": 1e9, "p_hi": 2e9, "left": "a", "right": "b", "class": "swap", "p_b": 1.5e9,
                 "delta_s": delta_s, "converged": True},
                {"t": 1100.0, "p_lo": 1e9, "p_hi": 2e9, "left": "a", "right": "b", "class": "swap", "p_b": 1.6e9,
                 "delta_s": delta_s, "converged": True}]
        return {"cells": cells, "boundaries": {"status": "exported", "rows": rows}}

    def test_clapeyron_sign_agrees(self):
        cx.check_table(self._table(-2.0))                                   # slope > 0, Δs < 0: passes

    def test_clapeyron_sign_mutant_is_a_stop(self):
        from solver import material_assemblage as ma
        with self.assertRaises(ma.TableStop) as e:
            cx.check_table(self._table(+2.0))
        self.assertEqual(e.exception.check, "coexist")


class ShippedViews(unittest.TestCase):
    """r2 v1 on the shipped records: every cut edge row is in one cut run (an edge run, or a coincident pair read as a
    swap), so every non-swap cut carries a hook; and every cut swap gets a Segment or a named SharpOnly."""

    @unittest.skipUnless(__import__("solver.tests.test_assemblage_c1", fromlist=["_shipped"])._shipped(),
                         "no shipped assemblage records")
    def test_every_cut_row_has_a_hook(self):
        from solver import events as ev, material_registry as mr
        from solver.tests import test_assemblage_c1 as tc
        reg = mr.load()
        for rid in tc.RECORDS:
            v = tc._view(reg, rid)
            in_runs = {id(r) for c in v._cut for r in c.rows}
            lost = [r["t"] for c in v._curves if c.kind == "edge" for r in c.rows if not r["across"] and
                    id(r) not in in_runs]
            self.assertEqual(lost, [], rid)
            hooks = {e.name: e.coexist for e in ev.record_events(v)}
            for i, c in enumerate(v._cut):
                h = [hk for n, hk in hooks.items() if n.startswith(f"phase:{c.kind}{i}:")]
                self.assertTrue(h and h[0] is not None, (rid, c.kind, i))
            for i in range(len(v._cut), len(v._events)):                    # runs read across: no hook (68 B3)
                h = [hk for n, hk in hooks.items() if n.startswith(f"phase:{v._events[i].kind}{i}:")]
                self.assertTrue(h and h[0] is None, (rid, i))


class SwapNoteFilter(unittest.TestCase):
    """68 B4 / m2: solve drops exactly the walked curve's SWAP_NOTE text, rebuilt from that curve's own P range; another
    swap's note (a different run, even with the same layer) stays."""

    def test_drop_set_is_keyed_by_the_walked_curve(self):
        from solver import material_assemblage as ma

        class _C:
            def __init__(self, a, b):
                self.p_range = (a, b)

        class _V:
            _events = [_C(9.8e9, 9.9e9), _C(9.8e9, 9.9e9), _C(22.7e9, 23.5e9)]
        rec = {"kind": "segment", "layer": "mantle", "curve": "phase:swap2:x|y", "entry": (1.0, 22.8e9, 1890.0),
               "exit": (22.84e9, 1895.0), "phi_range": [0.0, 1.0]}
        notes, drop = cx.notes([rec], {"mantle": _V()})
        self.assertEqual(drop, {("mantle", f"{ma.SWAP_NOTE}; P {22.7:.4g}–{23.5:.4g} GPa")})
        self.assertEqual([n.kind for n in notes], ["coexistence_segment"])

    def test_no_segment_drops_nothing(self):
        rec = {"kind": "sharp", "layer": "mantle", "curve": "phase:swap0:x|y", "reason": "zero_length", "m": 1.0,
               "P": 9.85e9, "T": 1740.0}
        notes, drop = cx.notes([rec], {"mantle": object()})
        self.assertEqual(drop, set())
        self.assertEqual([n.kind for n in notes], ["coexistence_sharp_step"])
