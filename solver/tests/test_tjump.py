# T 점프 시험 — 쐐기 끝 표시 곡선에서 s 보존 점프, 띠·q·도달 거리, 곡선 자신의 g 로만 풀림, 2×띠 거절, 곡선 끝(g None) 즉시 정지, pass 마다 초기화, 전도층 두 경우, 기록·경로 소비자, 결정성; 변형마다 identity 통과·변형 실패 (reg-coexistence note 6 J1–J8; C3)
"""reg-coexistence post-freeze note 6 (frozen, artifacts main 9ff9ecaf6) on an engine-native toy read: two fields A, B
split by a tagged Mid P_b(T) = P0 + K (T − T0), K = 1e6 Pa/K; field B's dT/dP = ratio / K, so q = ratio.

Run from the worktree root:  PY -B -m unittest solver.tests.test_tjump
"""
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


def run(toy, dm=2e19, view=None):
    view = view or rv.ReadView(toy, 0.0, "toy")
    y0 = (5.0e6, P0 - 3.0e4, T0 - 1e-3, T0 - 1e-3, 0.0, 0.0)
    return st.run(rhs.make_rhs(view), 4.0e24, y0, 4.0e24 - dm, opt(), list(view.events())), view


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
        self.check_mutant(self.case_q07_no_refire, "                if gv * sg > 0.0:\n",
                          "                if gv * sg > 0.0 or abs(y[1] - pm) > 1.0 * b_ / 3.0:\n")

    def test_mutant_no_refusal(self):
        self.check_mutant(self.case_not_cleared_refused, "                elif abs(y[1] - pm) > 2.0 * b_:\n",
                          "                elif False:\n")

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
        a = ('                if gv is None:\n                    return stop("refused", Stop("tjump_not_cleared", '
             '{"curve": name, "m": x, "P": y[1], "T": y[3],\n')
        with mock.patch.object(st, "run", variant(st.run)):
            self.case()
        for new in ("                if gv is None:\n                    gv = sg\n"        # None as release
                    "                if False:\n                    return stop(\"refused\", Stop(\"tjump_not_cleared\", "
                    "{\"curve\": name, \"m\": x, \"P\": y[1], \"T\": y[3],\n",
                    "                if gv is None:\n                    continue\n"        # stays retired
                    "                if False:\n                    return stop(\"refused\", Stop(\"tjump_not_cleared\", "
                    "{\"curve\": name, \"m\": x, \"P\": y[1], \"T\": y[3],\n"):
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
