# T 점프 시험 — 쐐기 끝 표시 곡선에서 s 보존 점프, 띠·q·도달 거리, 곡선 자신의 g 로만 풀림, 2×띠 거절, 곡선 끝(g None) 즉시 정지, pass 마다 초기화, 전도층 두 경우, 기록·경로 소비자, 결정성; 변형마다 identity 통과·변형 실패 (reg-coexistence note 6 J1–J8; C3)
"""reg-coexistence post-freeze note 6 (frozen, artifacts main 9ff9ecaf6) on an engine-native toy read: two fields A, B
split by a tagged Mid P_b(T) = P0 + K (T − T0), K = 1e6 Pa/K; field B's dT/dP = ratio / K, so q = ratio.

Run from the worktree root:  PY -B -m unittest solver.tests.test_tjump
"""
import dataclasses
import math
import unittest
from unittest import mock

from solver import read_view as rv, rhs
from solver import solve as sv
from solver import stepper as st
from solver.tests._mutants import variant

P0, T0, K = 1.0e10, 1700.0, 1.0e6
DT_JUMP = -0.01


class ReadRefusal(ValueError):
    def __init__(self, kind, why):
        super().__init__(why)
        self.kind = kind


class Toy:
    """Fields A (P < P_b(T)) and B. t_jump: T → T + dtj, A → B upward. folds: dPb_dT_max = K, walk_reach_pa."""

    def __init__(self, ratio_b=1.2, dtj=DT_JUMP, reach=1e9, t_hi=math.inf, t_edges=()):
        self.dtdp = {"A": 1e-8, "B": ratio_b / K}
        self.dtj, self.t_hi, self.t_edges = dtj, t_hi, list(t_edges)
        self.folds = [{"zone": 0, "curve": "c0", "dPb_dT_max_Pa_per_K": K, "walk_reach_pa": reach}]
        self.jumps = []

    def p_b(self, t):
        return None if t > self.t_hi else P0 + K * (t - T0)

    def state(self, p, t, field=None):
        pb = self.p_b(t)
        f = field or ("A" if pb is None or p < pb else "B")
        return {"rho": 3500.0, "dtdp": self.dtdp[f], "s": 0.0, "c_p": 1200.0, "alpha": 1e-5, "K_T": 1e11, "field": f}

    def events(self, t_index=2):
        def g(m, y, ti=t_index):
            pb = self.p_b(y[ti])
            return None if pb is None else y[1] - pb
        out = [st.Event("c0", g, scale=P0, terminal=False, seam=True, component=1,
                        tag={"curve": "c0", "zone": 0, "tagged": True})]
        for i, te in enumerate(self.t_edges):
            out.append(st.Event(f"tedge:{i}", (lambda m, y, te=te, ti=t_index: y[ti] - te), scale=T0,
                                terminal=False, seam=True))
        return out

    def t_jump(self, p, t, zone, curve, upward=True):
        a, b = ("A", "B") if upward else ("B", "A")
        d = self.dtj if upward else -self.dtj
        self.jumps.append(p)
        return {"T_new": t + d, "ds": 0.0, "dT": d, "from": a, "to": b}


def opt():
    return st.Options(rtol=1e-10, floors=(1.0, 1.0, 1e-6, 1e-6, 1.0, 1.0), h0=-1e15, h_min=1e8, h_max=1e17,
                      max_steps=100000, event_tol=1e-13, event_rewalks=32, event_min_progress=1e12)


def run(toy, dm=2e19, view=None, o=None):
    view = view or rv.ReadView(toy, 0.0, "toy")
    y0 = (5.0e6, P0 - 3.0e4, T0 - 1e-3, T0 - 1e-3, 0.0, 0.0)
    return st.run(rhs.make_rhs(view), 4.0e24, y0, 4.0e24 - dm, o or opt(), list(view.events())), view


def jumps(r):
    return [c for c in r.coexist if c.get("kind") == "tjump"]


# ── J1: the re-cross set (ported from the harness's runs/tjump-69f7bae5e/test_recross.py) ────────────────────────────
class Recross(unittest.TestCase):
    def case_second_crossing_after_band(self):
        r, _ = run(Toy(0.8, dtj=+0.01))
        self.assertEqual(r.stop.kind, "end", r.stop)
        self.assertEqual(len(jumps(r)), 1, [e[0] for e in r.events])
        self.assertAlmostEqual(jumps(r)[0]["band_pa"], 1e4 / 0.2, delta=5.0)

    def case_q07_no_refire(self):
        r, _ = run(Toy(0.7, dtj=+0.01))
        self.assertEqual(r.stop.kind, "end", r.stop)
        self.assertEqual(len(jumps(r)), 1, [e[0] for e in r.events])

    def case_next_event_does_not_release(self):
        r0, _ = run(Toy(0.5, dtj=+0.01))
        t_new = jumps(r0)[0]["T_new"]
        toy = Toy(0.5, dtj=+0.01, t_edges=[t_new + 0.5 / K * 1e3])
        r, _ = run(toy)
        self.assertIn("tedge:0", [e[0] for e in r.events])
        self.assertEqual(r.stop.kind, "end", r.stop)
        self.assertEqual(len(jumps(r)), 1, [e[0] for e in r.events])

    def case_not_cleared_refused(self):
        toy = Toy(0.5, dtj=+0.01)
        orig, base = toy.state, {}

        def state(p, t, field=None):
            d = orig(p, t, field)
            if d["field"] == "B" and toy.jumps and p - toy.jumps[0] > 0.6 * 2e4:
                d = dict(d, dtdp=2.0 * d["dtdp"])
            return d
        toy.state = state
        r, _ = run(toy)
        self.assertEqual(r.stop.kind, "refused", r.stop)
        self.assertEqual(r.stop.record.kind, "tjump_not_cleared")
        self.assertEqual(r.stop.record.record["reason"], "not_cleared")

    def case_pin_and_run_start(self):
        toy = Toy(0.1)
        r, view = run(toy)
        j = jumps(r)[0]
        pm, band = j["P"], j["band_pa"]
        t_a = (pm + 0.5 * band - P0) / K + T0 + 1.0             # a T where the point is on A by position
        view.pins["c0"] = ("A", "B", pm, band, True)
        self.assertEqual(view.props(pm + 0.5 * band, t_a)["field"], "B")     # pinned inside the window
        self.assertEqual(view.props(pm + 2.5 * band, t_a + 2.0 * band / K)["field"], "A")   # outside: by position
        view.pins["c0"] = ("A", "B", pm - 2e4, 1e9, True)                   # stale from an earlier pass
        r2, _ = run(toy, view=view)
        self.assertEqual([n[:2] for n in r2.path], [n[:2] for n in r.path])  # run_start cleared it

    def test_second_crossing_after_band(self):
        self.case_second_crossing_after_band()

    def test_q07_no_refire(self):
        self.case_q07_no_refire()

    def test_q_above_max_refused(self):
        r, _ = run(Toy(0.95, dtj=+0.01))
        self.assertEqual(r.stop.kind, "refused", r.stop)
        self.assertEqual(r.stop.record.kind, "tjump_refused")
        self.assertIn("near-tangent", r.stop.record.record["why"])

    def test_no_second_crossing_when_path_outruns_curve(self):
        r, _ = run(Toy(0.1))
        self.assertEqual(len(jumps(r)), 1)
        self.assertAlmostEqual(jumps(r)[0]["band_pa"], 1e4 / 0.9, delta=1.0)

    def test_next_event_does_not_release(self):
        self.case_next_event_does_not_release()

    def test_not_cleared_refused(self):
        self.case_not_cleared_refused()

    def test_later_real_crossing_fires(self):
        toy = Toy(0.5, dtj=+0.01)
        orig = toy.state

        def state(p, t, field=None):
            d = orig(p, t, field)
            if d["field"] == "B" and toy.jumps and p - toy.jumps[0] > 6e4:
                d = dict(d, dtdp=3.0 * d["dtdp"])
            return d
        toy.state = state
        r, _ = run(toy)
        lands = [(n, yy[1]) for n, _m, yy in r.events if n == "c0"]
        self.assertGreaterEqual(len(lands), 2, [e[0] for e in r.events])
        self.assertGreater(lands[1][1] - toy.jumps[0], 6e4)

    def test_pin_inside_band_and_cleared_per_pass(self):
        self.case_pin_and_run_start()

    # the four mutants (68's set), each beside its identity copy
    def check_mutant(self, case, old, new, more=()):
        with mock.patch.object(st, "run", variant(st.run)):
            case()
        with mock.patch.object(st, "run", variant(st.run, old, new, more)):
            with self.assertRaises(AssertionError):
                case()

    def test_mutant_release_at_next_event(self):
        self.check_mutant(self.case_next_event_does_not_release, "            landed.append((fired.name, x, y))\n",
                          "            for _nm in list(retired):\n                _r = retired.pop(_nm)\n"
                          "                _r[3].release()\n                live.append(_r[0])\n"
                          "            landed.append((fired.name, x, y))\n")

    def test_mutant_release_by_band(self):
        self.check_mutant(self.case_q07_no_refire, "            if gv * sg > 0.0:\n",
                          "            if gv * sg > 0.0 or abs(ya[1] - pm) > 1.0 * b_ / 3.0:\n")

    def test_mutant_no_refusal(self):
        self.check_mutant(self.case_not_cleared_refused, "            elif abs(ya[1] - pm) > 2.0 * b_:\n",
                          "            elif False:\n")

    def test_mutant_no_run_start(self):
        self.check_mutant(self.case_pin_and_run_start, "        if rs_ is not None:\n            rs_()\n",
                          "        pass\n")


# ── J1b: g undefined while retired (the curve ended inside the band) ───────────────────────────────────────────────
class CurveEnded(unittest.TestCase):
    def case(self):
        r0, _ = run(Toy(0.5, dtj=+0.01))
        t_new = jumps(r0)[0]["T_new"]
        r, _ = run(Toy(0.5, dtj=+0.01, t_hi=t_new + 2e-3))        # the curve ends 2 mK past the jump
        self.assertEqual(r.stop.kind, "refused", r.stop)
        self.assertEqual(r.stop.record.kind, "tjump_not_cleared")
        self.assertEqual(r.stop.record.record["reason"], "curve_ended")

    def test_curve_ended_stops_at_once(self):
        self.case()

    def test_mutants(self):
        a = ('            if gv is None:                              # note 7 item 1: a curve end only inside 2 × band\n'
             '                return stop("refused", Stop("tjump_not_cleared", '
             '{"curve": name, "m": xa, "P": ya[1], "T": ya[3],\n')
        with mock.patch.object(st, "run", variant(st.run)):
            self.case()
        for new in ("            if gv is None:\n                gv = sg\n"        # None as release
                    "            if False:\n                return stop(\"refused\", Stop(\"tjump_not_cleared\", "
                    "{\"curve\": name, \"m\": xa, \"P\": ya[1], \"T\": ya[3],\n",
                    "            if gv is None:\n                continue\n"        # stays retired
                    "            if False:\n                return stop(\"refused\", Stop(\"tjump_not_cleared\", "
                    "{\"curve\": name, \"m\": xa, \"P\": ya[1], \"T\": ya[3],\n"):
            with mock.patch.object(st, "run", variant(st.run, a, new)):
                with self.assertRaises(AssertionError):
                    self.case()


# ── J4: named refusals ─────────────────────────────────────────────────────────────────────────────────────────────
class Refusals(unittest.TestCase):
    def test_untagged_jump_request_refused(self):
        toy = Toy(0.5)

        def t_jump(p, t, zone, curve, upward=True):
            raise ReadRefusal("tjump_untagged", "refused: T jump requested at an untagged crossing")
        toy.t_jump = t_jump
        r, _ = run(toy)
        self.assertEqual((r.stop.kind, r.stop.record.kind), ("refused", "tjump_refused"))
        self.assertIn("untagged", r.stop.record.record["why"])

    def test_short_reach_refused(self):
        r, _ = run(Toy(0.5, reach=10.0))
        self.assertEqual(r.stop.record.kind, "tjump_refused")
        self.assertIn("walk reach short", r.stop.record.record["why"])

    def test_refusals_map_to_registered_ids(self):
        r, _ = run(Toy(0.95, dtj=+0.01))
        ref = sv._to_refusal(sv._at(r.stop, r.y, r.x), "toy", 1.0, "R", "scan")
        self.assertEqual(ref.id, "solve.tjump_refused")
        toy = Toy(0.5, dtj=+0.01)
        r0, _ = run(Toy(0.5, dtj=+0.01))
        r, _ = run(Toy(0.5, dtj=+0.01, t_hi=jumps(r0)[0]["T_new"] + 2e-3))
        ref = sv._to_refusal(sv._at(r.stop, r.y, r.x), "toy", 1.0, "R", "scan")
        self.assertEqual((ref.id, dict(ref.evidence)["reason"]), ("solve.tjump_not_cleared", "curve_ended"))


# ── J5, J6: records and determinism ────────────────────────────────────────────────────────────────────────────────
class RecordsAndDeterminism(unittest.TestCase):
    def test_record_fields_and_landed_name(self):
        r, _ = run(Toy(0.1))
        j = jumps(r)[0]
        for k in ("curve", "m", "P", "T", "dT", "ds", "from", "to", "band_pa"):
            self.assertIn(k, j)
        self.assertIn("coexist-tjump:c0", [e[0] for e in r.events])
        same_m = [i for i in range(1, len(r.path)) if r.path[i][0] == r.path[i - 1][0]]
        self.assertTrue(same_m, "the jump's second node at the same m")

    def test_two_runs_byte_identical(self):
        r1, _ = run(Toy(0.1))
        r2, _ = run(Toy(0.1))
        self.assertEqual(repr([n[:2] for n in r1.path]), repr([n[:2] for n in r2.path]))
        self.assertEqual(repr(r1.coexist), repr(r2.coexist))


# ── J7: conductive layer ────────────────────────────────────────────────────────────────────────────────────────────
class Conductive(unittest.TestCase):
    def lid_run(self, t_index, conductive):
        toy = Toy(0.1)
        view = rv.ReadView(toy, 0.0, "toy")
        evs = view.events(t_index=t_index, conductive=conductive)

        def f(m, y):                                      # P rises; T_ad by the read; the lid's T fixed 300 K below
            d = view.props(y[1], y[2])
            if isinstance(d, st.Stop):
                return d
            dp = 1e-15
            return (0.0, dp, d["dtdp"] * dp, d["dtdp"] * dp, 0.0, 0.0)
        y0 = (5.0e6, P0 - 3.0e4, T0 - 1e-3, T0 - 1e-3 - 300.0, 0.0, 0.0)
        if t_index == 3:                                   # the conductive T meets the curve instead
            y0 = (5.0e6, P0 - 3.0e4, T0 + 300.0, T0 - 1e-3, 0.0, 0.0)
        return st.run(f, 0.0, y0, 1e20, opt(), list(evs))

    def case_ad_shifts_t_ad_only(self):
        r = self.lid_run(2, True)
        j = jumps(r)
        self.assertEqual(len(j), 1, r.stop)
        y_b = [yy for n, _m, yy in r.events if n == "coexist-tjump:c0"][0]
        y_a = [yy for n, _m, yy in r.events if n == "c0"][0]
        self.assertAlmostEqual(y_b[2] - y_a[2], j[0]["dT"], delta=1e-12)
        self.assertEqual(y_b[3], y_a[3])

    def case_conductive_t_stops(self):
        r = self.lid_run(3, False)
        self.assertEqual(r.stop.kind, "refused", r.stop)
        self.assertEqual(r.stop.record.kind, "tjump_in_conductive_T")

    def test_ad_jump_shifts_t_ad_only(self):
        self.case_ad_shifts_t_ad_only()

    def test_conductive_t_crossing_stops(self):
        self.case_conductive_t_stops()

    def test_mutants(self):
        with mock.patch.object(rv.TJumpHook, "t_jump", variant(rv.TJumpHook.t_jump)):
            self.case_ad_shifts_t_ad_only()
        with mock.patch.object(rv.TJumpHook, "t_jump", variant(rv.TJumpHook.t_jump,
                                                              "shift=(2,) if self.conductive else (2, 3)", "shift=(2, 3)")):
            with self.assertRaises(AssertionError):
                self.case_ad_shifts_t_ad_only()
        with mock.patch.object(st, "run", variant(st.run)):
            self.case_conductive_t_stops()
        with mock.patch.object(st, "run", variant(st.run, "if tj is not None and fired.t_index == 3:",
                                                  "if tj is not None and False:")):
            with self.assertRaises(AssertionError):
                self.case_conductive_t_stops()


# ── 68 HOLD on C3 (8055a60d): B1 landed nodes, B2 engine errors, B3 band factor and release, B4 the lid wiring ──────
RETIRED_CALL_AT_LANDING = ('            if retired:                                 # 68 B1 on C3: the landed node too, '
                           'before a terminal return\n                got = check_retired(x, y)\n'
                           '                if got is not None:\n                    return got\n')


class HoldOnC3(unittest.TestCase):
    def case_terminal_landing_past_curve_end(self):
        """B1 (68's probe): the curve ends 2 mK past the jump; a terminal T_ad event δ past that end lands first.
        The landed node is past the curve's end while it is retired, so the run refuses (curve_ended)."""
        r0, _ = run(Toy(0.5, dtj=+0.01))
        t_hi = jumps(r0)[0]["T_new"] + 2e-3
        for d in (2e-7, 1e-5, 1e-3):
            toy = Toy(0.5, dtj=+0.01, t_hi=t_hi)
            view = rv.ReadView(toy, 0.0, "toy")
            stop_ev = st.Event("t_stop", (lambda m, y, te=t_hi + d: y[2] - te), scale=T0, terminal=True, seam=True)
            y0 = (5.0e6, P0 - 3.0e4, T0 - 1e-3, T0 - 1e-3, 0.0, 0.0)
            r = st.run(rhs.make_rhs(view), 4.0e24, y0, 4.0e24 - 2e19, opt(), list(view.events()) + [stop_ev])
            self.assertEqual(r.stop.kind, "refused", (d, r.stop, r.event))
            self.assertEqual(r.stop.record.kind, "tjump_not_cleared", d)
            self.assertEqual(r.stop.record.record["reason"], "curve_ended", d)

    def test_terminal_landing_past_curve_end_refused(self):
        self.case_terminal_landing_past_curve_end()

    def test_B1_mutant_no_check_at_landing(self):
        with mock.patch.object(st, "run", variant(st.run)):
            self.case_terminal_landing_past_curve_end()
        with mock.patch.object(st, "run", variant(st.run, RETIRED_CALL_AT_LANDING, "")):
            with self.assertRaises(AssertionError):
                self.case_terminal_landing_past_curve_end()

    def test_B2_plain_value_error_propagates(self):
        """A hook-side bug (a plain ValueError, e.g. a math domain error in the read) is an engine error."""
        toy = Toy(0.5)

        def t_jump(p, t, zone, curve, upward=True):
            return {"T_new": math.sqrt(-1.0)}
        toy.t_jump = t_jump
        with self.assertRaisesRegex(ValueError, "math domain error"):
            run(toy)

    def test_B2_read_refusal_in_state_is_named(self):
        """A ReadRefusal from the read inside the hook (the state at T_new) is the hook's named refusal."""
        toy = Toy(0.5)
        orig = toy.state

        def state(p, t, field=None):
            if field == "B":
                raise ReadRefusal("extent", "planted extent at T_new")
            return orig(p, t, field)
        toy.state = state
        r, _ = run(toy)
        self.assertEqual(r.stop.record.kind, "tjump_refused")
        self.assertIn("extent", r.stop.record.record["why"])

    def case_clears_between_band_and_twice(self):
        """B3: the path clears the curve at ΔP ≈ 2.8e4, between band (2e4) and 2·band (4e4): released, no refusal."""
        toy = Toy(0.5, dtj=+0.01)
        orig = toy.state

        def state(p, t, field=None):
            d = orig(p, t, field)
            if d["field"] == "B" and toy.jumps and p - toy.jumps[0] > 0.6 * 2e4:
                d = dict(d, dtdp=1.5 * d["dtdp"])            # q 0.5 → 0.75 past 1.2e4
            return d
        toy.state = state
        r, view = run(toy)
        self.assertEqual(r.stop.kind, "end", r.stop)
        self.assertEqual(len(jumps(r)), 1)
        self.assertAlmostEqual(jumps(r)[0]["band_pa"], 2e4, delta=5.0)
        self.assertEqual(view.pins, {})

    def test_clears_between_band_and_twice(self):
        self.case_clears_between_band_and_twice()

    def test_B3_mutant_one_band(self):
        a = "            elif abs(ya[1] - pm) > 2.0 * b_:\n"
        with mock.patch.object(st, "run", variant(st.run)):
            self.case_clears_between_band_and_twice()
        with mock.patch.object(st, "run", variant(st.run, a, "            elif abs(ya[1] - pm) > 1.0 * b_:\n")):
            with self.assertRaises(AssertionError):
                self.case_clears_between_band_and_twice()

    def case_released_reads_own_field(self):
        """B3: after the release, a read inside the old window on the old side by position reads its own field."""
        r, view = run(Toy(0.5, dtj=+0.01))
        self.assertEqual(r.stop.kind, "end", r.stop)
        j = jumps(r)[0]
        pm, band = j["P"], j["band_pa"]
        t_a = (pm + 0.5 * band - P0) / K + T0 + 1.0             # P < P_b(t_a): field A by position
        self.assertEqual(view.pins, {})
        self.assertEqual(view.props(pm + 0.5 * band, t_a)["field"], "A")

    def test_released_reads_own_field(self):
        self.case_released_reads_own_field()

    def test_B3_mutant_no_release(self):
        with mock.patch.object(st, "run", variant(st.run)):
            self.case_released_reads_own_field()
        with mock.patch.object(st, "run", variant(st.run, "                hk.release()\n", "")):
            with self.assertRaises(AssertionError):
                self.case_released_reads_own_field()


# ── reg-coexistence note 7 item 1: after a jump the step is capped at the band until release ──────────────────────
STEP_CAP = ('        if retired and not opt.fixed and k1[1] != 0.0:   # reg-coexistence note 7 item 1: from a jump to its '
            'release\n')


class SegmentedToy(Toy):
    """As Toy, but the curve's T range ends by zone segmentation only (w0.1's shape, c8 11-18): past t_hi the curve's
    g is None while the fields stay as they were, so the path's rhs is smooth across the curve's end."""

    def state(self, p, t, field=None):
        pb = P0 + K * (t - T0)
        f = field or ("A" if p < pb else "B")
        return {"rho": 3500.0, "dtdp": self.dtdp[f], "s": 0.0, "c_p": 1200.0, "alpha": 1e-5, "K_T": 1e11, "field": f}


class StoredMaxToy(SegmentedToy):
    """SegmentedToy whose stored max|dP_b/dT| is 1.25 K, above the curve's own K (r2 B1 on note 7): q = 0.625 at the
    jump, band = 0.01·1.25e6 / 0.375 = 33333.3 Pa, while the path's own q′ = 0.5 clears the curve at ΔP = 2e4 Pa,
    strictly inside the band. A node at the band is then strictly on the new side (g = +6667 Pa), never on a tie."""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.folds = [dict(self.folds[0], dPb_dT_max_Pa_per_K=1.25 * K)]


class StepCap(unittest.TestCase):
    """reg-coexistence note 7 item 1. Toy(0.5, dtj=+0.01): past the jump T = T_new + (0.5 / K)·ΔP. With the stored max
    equal to K (q′ = q), g reaches 0 at ΔP = band = 2e4 exactly; StoredMaxToy separates the two (band 33333.3 Pa,
    release point D = 2e4 Pa)."""
    BAND = 2e4          # Toy / SegmentedToy (q′ = q)
    D = 2e4             # the path's own release point, both toys

    @staticmethod
    def o():
        """h_max raised so the smooth toy's natural steps after the jump are many bands long, as on w0.1."""
        return dataclasses.replace(opt(), h_max=1e20)

    def t_new(self):
        r0, _ = run(Toy(0.5, dtj=+0.01), o=self.o())
        return jumps(r0)[0]["T_new"], jumps(r0)[0]["P"]

    def t_at(self, t_new, dp):
        return t_new + 0.5 * dp / K

    def first_after_jump(self, r, pm):
        i = [k for k, n in enumerate(r.path) if n[1][1] == pm][-1]          # the jump's second node
        return r.path[i + 1][1][1] - pm

    def case_a_end_before_release(self):
        """(a) q′ = q: the curve ends at 0.9·band, before the release point at 1·band (68: at 1·band the end would race
        the release); the first capped node is past the end, inside 2·band: curve_ended."""
        t_new, _ = self.t_new()
        r, _ = run(SegmentedToy(0.5, dtj=+0.01, t_hi=self.t_at(t_new, 0.9 * self.BAND)), o=self.o())
        self.assertEqual((r.stop.kind, getattr(r.stop.record, "kind", None)), ("refused", "tjump_not_cleared"), r.stop)
        self.assertEqual(r.stop.record.record["reason"], "curve_ended")

    def case_b_end_after_release(self):
        """(b) q′ < q: the curve ends at 3·band; the first node after the jump is the capped one, at band to first
        order (|h| = band/|dP/dm| at k1), strictly on the new side: released there, and the run ends normally."""
        t_new, pm = self.t_new()
        toy = StoredMaxToy(0.5, dtj=+0.01, t_hi=self.t_at(t_new, 3.0 * 33333.33))
        r, view = run(toy, o=self.o())
        self.assertEqual(r.stop.kind, "end", r.stop)
        self.assertEqual(len(jumps(r)), 1)
        band = jumps(r)[0]["band_pa"]
        self.assertAlmostEqual(band, 1e4 * 1.25 / 0.375, delta=1e-6)
        self.assertEqual(view.pins, {})
        dp1 = self.first_after_jump(r, pm)
        self.assertLessEqual(dp1, band * (1 + 1e-6))
        self.assertGreater(dp1, self.D)                                      # past the release point: no tie

    def case_w01_shape(self):
        """w0.1's shape: the curve ends 4.5·D past P_m and the uncapped first step would reach 5.3·D (past the end,
        g None); with the cap the curve is released at the first node and the run ends normally."""
        t_new, pm = self.t_new()
        r, view = run(StoredMaxToy(0.5, dtj=+0.01, t_hi=self.t_at(t_new, 4.5 * self.D)), o=self.o())
        self.assertEqual(r.stop.kind, "end", r.stop)
        self.assertEqual(view.pins, {})

    def case_d_event_past_window(self):
        """(d) an untagged T event 1.5·band past P_m: the first node after the jump is the capped one, not its landing."""
        t_new, pm = self.t_new()
        band = 1e4 * 1.25 / 0.375
        toy = StoredMaxToy(0.5, dtj=+0.01, t_edges=[self.t_at(t_new, 1.5 * band)])
        r, view = run(toy, o=self.o())
        self.assertEqual(r.stop.kind, "end", r.stop)
        self.assertIn("tedge:0", [e[0] for e in r.events])
        dp1 = self.first_after_jump(r, pm)
        self.assertLessEqual(dp1, band * (1 + 1e-6))
        tedge_p = [yy[1] for n, _m, yy in r.events if n == "tedge:0"][0]
        self.assertLess(pm + dp1, tedge_p)

    def test_a_end_before_release_stops(self):
        self.case_a_end_before_release()

    def test_b_end_after_release_releases(self):
        self.case_b_end_after_release()

    def test_w01_shape_releases(self):
        self.case_w01_shape()

    def test_d_event_past_window_not_first(self):
        self.case_d_event_past_window()

    def test_c_no_cap_mutant(self):
        for case in (self.case_b_end_after_release, self.case_d_event_past_window, self.case_w01_shape):
            with mock.patch.object(st, "run", variant(st.run)):
                case()
            with mock.patch.object(st, "run", variant(st.run, STEP_CAP, "        if False:\n")):
                with self.assertRaises(AssertionError):
                    case()

    def test_none_beyond_window_is_not_cleared(self):
        """Without the cap (the mutant run), the first node after the jump lies at 5.3·D = 106 kPa, past 2·band
        (66.7 kPa) and past the curve's end: g None there is reason not_cleared, not curve_ended (note 7's scope)."""
        t_new, pm = self.t_new()
        with mock.patch.object(st, "run", variant(st.run, STEP_CAP, "        if False:\n")):
            r, _ = run(StoredMaxToy(0.5, dtj=+0.01, t_hi=self.t_at(t_new, 4.5 * self.D)), o=self.o())
        self.assertEqual((r.stop.kind, getattr(r.stop.record, "kind", None)), ("refused", "tjump_not_cleared"), r.stop)
        rec = r.stop.record.record
        self.assertIsNone(rec["g"])
        self.assertGreater(abs(rec["P"] - rec["P_m"]), 2.0 * rec["band_pa"])
        self.assertEqual(rec["reason"], "not_cleared")


class HminFloor(unittest.TestCase):
    """note 7 item 1, the h_min floor (r2 B2): where h_min·|dP/dm| ≥ 2·band the cap cannot place a node inside the
    window. The node the floor gives is judged like any: here it is still on the old side past 2·band, so the run stops
    tjump_not_cleared with reason not_cleared, a named outcome. A linear stepper problem, P = x, with a hand-made hook
    whose band is set directly."""

    class Hook:
        def __init__(self, band):
            self.band, self.released = band, 0

        def t_jump(self, m, y, upward):
            return {"T_new": y[2] + 1e-3, "ds": 0.0, "dT": 1e-3, "from": "A", "to": "B", "band_pa": self.band}

        def release(self):
            self.released += 1

        def run_start(self):
            pass

    def run_floor(self, band, h_min):
        hook = self.Hook(band)

        def g(m, y):                          # P_b(T) = 5 + 100 (T − 1000); the curve absent past P 6
            return None if y[1] > 6.0 else y[1] - (5.0 + 100.0 * (y[2] - 1000.0))
        ev = st.Event("c", g, scale=5.0, terminal=False, seam=True, component=1, coexist=hook,
                      tag={"curve": "c", "zone": 0, "tagged": True})
        o = st.Options(rtol=1e-10, floors=(1.0,) * 6, h0=0.5, h_min=h_min, h_max=1.0, max_steps=10000,
                       event_tol=1e-13, event_rewalks=32, event_min_progress=1e-9)
        f = lambda x, y: (0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
        return st.run(f, 0.0, (1.0, 0.0, 1000.0, 1000.0, 0.0, 0.0), 10.0, o, [ev]), hook

    def test_floor_beyond_window_is_named(self):
        r, hook = self.run_floor(band=1e-4, h_min=1e-3)            # 2·band = 2e-4 < h_min·dP/dm = 1e-3
        self.assertEqual((r.stop.kind, getattr(r.stop.record, "kind", None)), ("refused", "tjump_not_cleared"), r.stop)
        rec = r.stop.record.record
        self.assertEqual(rec["reason"], "not_cleared")
        self.assertGreater(abs(rec["P"] - rec["P_m"]), 2.0 * rec["band_pa"])
        self.assertLess(rec["g"], 0.0)

    def test_control_band_above_floor_releases(self):
        r, hook = self.run_floor(band=0.2, h_min=1e-6)             # the curve moved 0.1: released inside the band
        self.assertEqual(r.stop.kind, "end", r.stop)
        self.assertEqual(hook.released, 1)


class LidTJump(unittest.TestCase):
    """B4: a tagged curve crossed by T_ad in a lid pass, through the real solve._lid_wiring and lid.lid_pass."""

    def read(self):
        from solver.tests import test_read_view as V

        class LidToy(V.FixtureRead):
            def __init__(self):
                super().__init__([V.Curve("c_ad", 5.0e8, k=1e6, t0=1600.0, t_lo=1500.0, t_hi=1800.0)], drho=10.0)
                self.folds = [{"zone": 0, "curve": "c_ad", "dPb_dT_max_Pa_per_K": 1e6, "walk_reach_pa": 1e9}]

            def events(self, t_index=2):
                return [dataclasses.replace(e, tag={"curve": "c_ad", "zone": 0, "tagged": True})
                        for e in super().events(t_index)]

            def t_jump(self, p, t, zone, curve, upward=True):
                d = 0.01 if upward else -0.01
                return {"T_new": t + d, "ds": 0.0, "dT": d, "from": "f0", "to": "f1"}
        return V, LidToy()

    def case_lid_jump_shifts_t_ad_only(self):
        from solver import lid
        V, read = self.read()
        view = rv.ReadView(read, 0.0, "lid_toy")
        w = sv._lid_wiring(view)
        res = lid.lid_pass(view, V.M_E, V.R_E, V.D, 0.0, V.T_S, V.T_POT, V.RS, **w)
        self.assertNotIsInstance(res, st.Stop, res)
        names = [e[0] for e in res.events]
        self.assertIn("coexist-tjump:c_ad:ad", names, names)
        y_a = [e[2] for e in res.events if e[0] == "c_ad:ad"][0]
        y_b = [e[2] for e in res.events if e[0] == "coexist-tjump:c_ad:ad"][0]
        self.assertAlmostEqual(y_b[2] - y_a[2], 0.01, delta=1e-12)
        self.assertEqual(y_b[3], y_a[3])                          # the lid's own T is not shifted

    def test_lid_jump_shifts_t_ad_only(self):
        self.case_lid_jump_shifts_t_ad_only()

    def test_B4_mutant_conductive_false(self):
        a = "lv_.events(t_index=2, conductive=True)"
        with mock.patch.object(sv, "_lid_wiring", variant(sv._lid_wiring)):
            self.case_lid_jump_shifts_t_ad_only()
        with mock.patch.object(sv, "_lid_wiring", variant(sv._lid_wiring, a, "lv_.events(t_index=2, conductive=False)")):
            with self.assertRaises(AssertionError):
                self.case_lid_jump_shifts_t_ad_only()


    def case_seed_pass_keeps_y3_on_t_ad(self):
        """68 n on 23b8c826: in the T_b⁰ pass y[3] is stepped as T_ad; after the «:ad» jump it still equals y[2]."""
        from solver import lid
        V, read = self.read()
        view = rv.ReadView(read, 0.0, "lid_toy")
        w = sv._lid_wiring(view)
        runs, real = [], st.run

        def rec(*args, **kw):
            got = real(*args, **kw)
            runs.append(got)
            return got
        with mock.patch.object(st, "run", rec):
            res = lid.lid_pass(view, V.M_E, V.R_E, V.D, 0.0, V.T_S, V.T_POT, V.RS, **w)
        self.assertNotIsInstance(res, st.Stop, res)
        seed = runs[0]
        names = [e[0] for e in seed.events]
        self.assertIn("coexist-tjump:c_ad:ad", names, names)
        y_b = [e[2] for e in seed.events if e[0] == "coexist-tjump:c_ad:ad"][0]
        self.assertEqual(y_b[3], y_b[2])
        self.assertEqual(seed.y[3], seed.y[2])

    def test_seed_pass_keeps_y3_on_t_ad(self):
        self.case_seed_pass_keeps_y3_on_t_ad()

    def test_seed_shift_mutant(self):
        from solver import lid
        with mock.patch.object(lid._SeedShift, "t_jump", variant(lid._SeedShift.t_jump)):
            self.case_seed_pass_keeps_y3_on_t_ad()
        with mock.patch.object(lid._SeedShift, "t_jump", variant(lid._SeedShift.t_jump,
                                                                  '    got["shift"] = (2, 3)\n', "")):
            with self.assertRaises(AssertionError):
                self.case_seed_pass_keeps_y3_on_t_ad()

    def test_seed_pass_filter_mutant(self):
        """The T_b⁰ pass steps y[3] = T_ad: without the filter the tagged t_index 3 copy stops tjump_in_conductive_T."""
        from solver import lid
        old = '                   if not (a is None and e.t_index == 3 and getattr(e.coexist, "t_jump", None))]\n'
        with mock.patch.object(lid, "lid_pass", variant(lid.lid_pass)):
            self.case_lid_jump_shifts_t_ad_only()
        with mock.patch.object(lid, "lid_pass", variant(lid.lid_pass, old, "                   ]\n")):
            V, read = self.read()
            view = rv.ReadView(read, 0.0, "lid_toy")
            res = lid.lid_pass(view, V.M_E, V.R_E, V.D, 0.0, V.T_S, V.T_POT, V.RS, **sv._lid_wiring(view))
        self.assertIsInstance(res, st.Stop)
        inner = res.record if isinstance(res.record, st.Stop) else res
        self.assertEqual(inner.kind, "tjump_in_conductive_T", res)


class FixedGrid(unittest.TestCase):
    """C3 class sweep (on 68 B4): the r-form run rebuilt its events positionally (t_index, tag dropped) and wrapped the
    hook without t_jump, so a tagged crossing reached enter() as a silent «sharp» record. Now a named refusal."""

    def run_r(self, t_index=2):
        from solver import fixed_grid
        view = rv.ReadView(Toy(0.5), 0.0, "toy")
        y0 = (5.0e6, P0 - 3.0e4, T0 - 1e-3, T0 - 1e-3, 0.0, 0.0)
        return fixed_grid.run_r(rhs.make_rhs(view), 4.0e24, y0, 0.0, 5.0e6 - 100.0, "r_end", 0.05,
                                list(view.events(t_index=t_index)), m_scale=4.0e24)

    def case_refused_by_name(self):
        r = self.run_r()
        self.assertEqual((r.stop.kind, getattr(r.stop.record, "kind", None)), ("refused", "tjump_refused"), r.stop)
        self.assertIn("fixed-grid", r.stop.record.record["why"])
        r3 = self.run_r(t_index=3)
        self.assertEqual(getattr(r3.stop.record, "kind", None), "tjump_in_conductive_T", r3.stop)

    def test_refused_by_name(self):
        self.case_refused_by_name()

    def test_mutants(self):
        from solver import fixed_grid
        with mock.patch.object(fixed_grid, "run_r", variant(fixed_grid.run_r)):
            self.case_refused_by_name()
        old = ("    evs = [dataclasses.replace(ev, g=(lambda r, z, g=ev.g: g(z[0], _y_of(r, z))), "
               "coexist=_r_hook(ev.coexist, f))\n")
        for new in ("    evs = [dataclasses.replace(ev, g=(lambda r, z, g=ev.g: g(z[0], _y_of(r, z))), "      # old wrapper
                    "coexist=None if ev.coexist is None else _RHook(ev.coexist, f))\n",
                    "    evs = [st.Event(ev.name, (lambda r, z, g=ev.g: g(z[0], _y_of(r, z))), ev.scale, ev.terminal, "
                    "ev.seam, ev.component, _r_hook(ev.coexist, f))\n"):                              # fields dropped
            with mock.patch.object(fixed_grid, "run_r", variant(fixed_grid.run_r, old, new)):
                with self.assertRaises(AssertionError):
                    self.case_refused_by_name()


# ── J8: a jump runs through solve.inward and every path consumer ─────────────────────────────────────────────────────
class PathConsumers(unittest.TestCase):
    def test_full_solve_with_a_jump(self):
        from solver.tests import test_read_view as V
        view = rv.ReadView(Toy(0.1), 0.0, "toy", "s" * 64)
        ans, _ = sv.solve(V._body(), views={"core": V.Uniform(9000.0), "mantle": view})
        self.assertEqual(type(ans).__name__, "Answer", getattr(ans, "text", ""))   # notes, zones, result all ran
        kinds = [n.kind for n in ans.notes]
        self.assertIn("coexistence_tjump", kinds)
        self.assertIn("read_counts", kinds)
        m = ans.profiles["mantle"]["m"]
        self.assertEqual(len(m) - len(set(m)), 1)          # the jump's two nodes at one m, in the layer's profile


if __name__ == "__main__":
    unittest.main()
