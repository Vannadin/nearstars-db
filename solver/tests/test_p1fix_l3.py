# 리뷰 LOW 묶음 L3 시험 — 닫힘·풀이: 사건별 재시작 상한, m_ε 밑 바닥, 코드가 든 solve_id, 네 멈춤의 거절, 안 쓰는 Options, 벽 중복, 끝 밀도, 훑기 끝 F, 벽 옆 0, git, 실패 괄호 잔차, 범위 밖 탐침
"""Post-phase-1 review LOW batch L3 (rewrite/p1review/low-triage.md; phase-1 design notes 17 §1, §4–§7 and 17a): G1-R-06,
G2-C-12, G2-R-06, G2-C-08 / G1-C-07 / G1-R-10 / G1-R-07, G2-C-09, G2-C-10, G2-C-11, G2-C-13, G2-C-14, G2-R-07, G2-R-08,
G2-R-10. Each test fails on 8c617e49 except two regression cases: G2-C-10 (duplicate walls) and G2-C-14 (an exact zero
beside a wall) no longer reproduce at 9ab7395e (S2's done_pairs and the wall trials joining the search, note 15 §1),
so their tests pass there too; the code guards are kept.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_p1fix_l3
"""
import dataclasses
import math
import subprocess
import unittest
from types import SimpleNamespace as NS
from unittest import mock

from solver import body as bd, closure as cl, context, from_v1, result, solve as sv
from solver import stepper as st
from solver import legacy_materials as lm, material_view as mv


def _opt(h0=8.0):
    return st.Options(rtol=1e-10, floors=(1e-12,), h0=h0, h_min=1e-12, h_max=100.0, max_steps=10000, event_rewalks=32)


def _earth():
    body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
    return body


OPT = context.Options(sensitivity_dt=0.0)


class RestartsPerEvent(unittest.TestCase):
    """Note 17 §1 (G1-R-06): the cap counts one event's landings since the last plain step."""

    def test_five_distinct_seams_in_one_step_land(self):
        evs = [st.Event(f"s{i}", (lambda x, y, c=5.0 + 0.01 * i: y[0] - c), scale=5.0, terminal=False, seam=True,
                        component=0) for i in range(5)]
        res = st.run(lambda x, y: (1.0,), 0.0, (0.0,), 10.0, _opt(), evs)
        self.assertEqual(res.stop.kind, "end")
        self.assertEqual([e[0] for e in res.events], [f"s{i}" for i in range(5)])

    def test_control_an_alternating_pair_still_trips(self):
        """A and B alternate every 0.1 and every step (0.15) holds one crossing, so no plain step comes between
        landings: A's own count passes 4 and trips EVENT_RESTARTS_STEP."""
        evs = [st.Event("A", lambda x, y: math.sin(math.pi * x / 0.2), scale=1.0, terminal=False),
               st.Event("B", lambda x, y: math.sin(math.pi * (x - 0.1) / 0.2), scale=1.0, terminal=False)]
        o = dataclasses.replace(_opt(0.15), h_max=0.15)
        res = st.run(lambda x, y: (1.0,), 0.05, (0.05,), 10.0, o, evs)
        self.assertEqual((res.stop.kind, res.stop.record.get("cap_name")), ("chatter", "EVENT_RESTARTS_STEP"))


class BaseBelowMEps(unittest.TestCase):
    """Note 17 §4 (G2-C-12): a mass base strictly inside (0, m_ε) is refused by name."""

    def test_refused_at_the_pass(self):
        """At Earth's own root x (a trial-level wall in x, r2 on note 17: the outcome of a whole solve is its lowest-x
        wall, here the lid's material domain at small R)."""
        e = _earth()
        _ans, x = sv.solve(e, OPT)
        tiny = dataclasses.replace(e, layers=tuple(dataclasses.replace(l, extent=bd.Extent("mass_fraction", 1e-8))
                                                   if l.id == "core" else l for l in e.layers))
        out = sv.inward(tiny, sv._views_at(tiny, sv._views(tiny), x), x, context.Options())
        self.assertIsInstance(out, st.Stop)
        self.assertEqual((out.kind, out.record["rule"]), ("layer_order", "base_below_m_eps"))
        got = sv._to_refusal(out, "w", x, "R", "accepted")
        self.assertEqual((got.id, got.evidence["rule"]), ("solve.layer_order", "base_below_m_eps"))


class SolveIdBindsTheSolverCode(unittest.TestCase):
    """Note 17 §5 (G2-R-06): a committed blob change of solver code moves the digest; an untracked solver module too
    (r2); a test file does not."""

    def _bytes(self, tamper=None, untracked=None):
        real = subprocess.run

        def run(args, *a, **k):
            out = real(args, *a, **k)
            if "ls-files" in args and "-s" in args and tamper:
                lines = []
                for line in out.stdout.splitlines():
                    meta, p = line.split("\t", 1)
                    if p == tamper:
                        mode, b0, stage = meta.split()
                        line = f"{mode} {b0[:-1] + ('0' if b0[-1] != '0' else '1')} {stage}\t{p}"
                    lines.append(line)
                out = subprocess.CompletedProcess(out.args, 0, "\n".join(lines) + "\n", out.stderr)
            elif "--others" in args:
                out = subprocess.CompletedProcess(out.args, 0, (untracked or "") + "\n", out.stderr)
            elif "diff" in args:
                out = subprocess.CompletedProcess(out.args, 0, "", out.stderr)
            return out
        with mock.patch("subprocess.run", run):
            return context.solver_code_bytes()

    def test_code_moves_tests_do_not(self):
        base = self._bytes()
        self.assertNotEqual(base, self._bytes(tamper="solver/closure.py"))
        self.assertEqual(base, self._bytes(tamper="solver/tests/test_closure.py"))
        self.assertNotEqual(base, self._bytes(untracked="solver/closure.py"))   # an «untracked» path is hashed by content
        self.assertEqual(base, self._bytes(untracked="solver/tests/test_closure.py"))


class FourStopsGetRefusals(unittest.TestCase):
    """Note 17 §6: no_residual, a non-finite state, centre_crossed and an undefined g at a secant iterate."""

    NODE = {"m": 1.0, "r": 2.0, "P": 3.0, "T": 4.0}

    def test_no_residual(self):
        got = sv._to_refusal(st.Stop("no_residual", {"x": 5.0, "value": float("nan")}, self.NODE), "w", 5.0, "R", "scan")
        self.assertEqual((got.id, got.evidence["where_kind"]), ("solve.non_finite", "residual"))

    def test_non_finite_state_from_the_stepper(self):
        res = st.run(lambda x, y: (float("nan") if x > 1.0 else 1.0,), 0.0, (0.0,), 10.0, _opt(2.0))
        self.assertEqual((res.stop.kind, res.stop.record.kind), ("refused", "non_finite"))
        got = sv._to_refusal(st.Stop(res.stop.kind, res.stop.record, self.NODE), "w", 1.0, "R", "scan")
        self.assertEqual((got.id, got.evidence["where_kind"]), ("solve.non_finite", "state"))

    def test_centre_crossed(self):
        got = sv._to_refusal(st.Stop("refused", st.Stop("centre_crossed", {"m": 1.0, "r": -1.0}), self.NODE), "w",
                             1.0, "R", "wall")
        self.assertEqual((got.id, got.evidence["rule"], got.evidence["got_r"]), ("solve.layer_order", "centre_crossed", -1.0))

    def test_undefined_g_at_an_iterate(self):
        ev = st.Event("onset:x", lambda x, y: None if 3.0 < x < 6.0 else y[0] - 5.0, scale=5.0)
        res = st.run(lambda x, y: (1.0,), 0.0, (0.0,), 10.0, _opt(), [ev])
        self.assertEqual((res.stop.kind, res.stop.record.kind), ("refused", "event_undefined"))
        got = sv._to_refusal(st.Stop(res.stop.kind, res.stop.record, self.NODE), "w", 1.0, "R", "wall")
        self.assertEqual((got.id, got.evidence["event_name"]), ("solve.event_undefined", "onset:x"))


class InertOptions(unittest.TestCase):
    """G2-C-09: a non-default value of a declared-but-unwired Option is refused, not silently ignored."""

    def test_raises(self):
        for k, v in (("close_tol", 1e-6), ("wall_shots", 3), ("band_pass", True)):
            with self.subTest(option=k), self.assertRaises(NotImplementedError):
                sv.solve(_earth(), dataclasses.replace(OPT, **{k: v}))


class ClosureEvidence(unittest.TestCase):
    def test_walls_are_not_duplicated(self):
        """G2-C-10 (probe4): a wall plus an isolated Brent refusal used to list the wall twice."""
        clean = cl.solve_scalar(lambda x: st.Stop("domain", {}) if x < 1.0e6 else x - 3.4e6, 1.0e5, 1.0e8)
        xs = [t.x for t in clean.trials if t.kind == "brent"]
        F = lambda x: st.Stop("domain", {}) if x < 1.0e6 or x == xs[len(xs) // 2] else x - 3.4e6
        out = cl.solve_scalar(F, 1.0e5, 1.0e8)
        wx = [w.x for w in out.walls]
        self.assertEqual(len(wx), len(set(wx)))

    def test_an_exact_zero_beside_a_wall_is_a_root(self):
        """G2-C-14: F = x − 5 on [1, 10] with refusals in (5, 6) and 5 a scan point."""
        pts = cl.scan_points(1.0, 10.0, 10)
        x0, x1 = pts[4], pts[5]                         # F = x − x0, exactly 0 at a scan point; refusing up to x1
        out = cl.solve_scalar(lambda x: st.Stop("domain", {}) if x0 < x < x1 else x - x0, 1.0, 10.0, 10)
        self.assertIn(x0, out.roots)


class SolveEvidence(unittest.TestCase):
    def _solve(self, out):
        with mock.patch.object(cl, "solve_scalar", return_value=out):
            got, _w = sv.solve(_earth(), OPT)
        return got

    def test_no_bracket_reads_f_at_the_scan_ends(self):
        """G2-C-13: the lowest scan point refused, so F_lo is None, not the lowest solved trial's F."""
        stop = st.Stop("chatter", {"event": "e", "count": 3, "cap_name": "EVENT_RESTARTS_STEP", "cap_value": 2},
                       {"m": 1.0, "r": 2.0, "P": 3.0, "T": 4.0})
        trials = [cl.Trial(1.0e6, None, stop, "scan"), cl.Trial(2.0e6, 1.0, None, "scan"), cl.Trial(3.0e6, 2.0, None, "scan")]
        got = self._solve(NS(kind="no_bracket", roots=[], trials=trials, walls=[cl.Wall(1.0e6, stop, 2.0e6)], detail={}))
        self.assertEqual((got.evidence["F_lo"], got.evidence["F_hi"]), (None, 2.0))

    def test_unconverged_reports_the_failed_brackets_residual(self):
        """G2-R-08: the residual comes from the failed bracket's problem record, not from the last trial."""
        trials = [cl.Trial(1.0, -1.0, None, "scan"), cl.Trial(2.0, 7.0, None, "scan")]
        got = self._solve(NS(kind="unconverged", roots=[], trials=trials, walls=[],
                             detail={"problems": [("unconverged", 1.5, 0.25)]}))
        self.assertEqual(got.evidence["last_residual"], 0.25)


class EndDensity(unittest.TestCase):
    """G2-C-11 as amended (the 707aa7a4 cost regression; r2 on c8274a73): a pass that ends above the bottom layer
    (planted: the mantle segment reports the r-floor event at its end) reads ρ_end with the bottom layer's view, so F
    is one function across the end-layer switch. Only a domain or window refusal by that view hands the read to the
    ended layer's view; any other Stop propagates."""

    def _run(self, core_answer=None):
        e = _earth()
        _ans, x = sv.solve(e, OPT)
        views = sv._views_at(e, sv._views(e), x)
        real_seg = sv._segment

        def seg(view, *a, **k):
            r = real_seg(view, *a, **k)
            return dataclasses.replace(r, stop=st.Stop("event"), event="r_floor") if getattr(view, "lid", None) == "mantle" \
                else r
        ends = []

        class Spy:
            def __init__(self, lid, v, answer=None):
                self.lid, self.v, self.answer = lid, v, answer

            def __getattr__(self, k):
                return getattr(self.v, k)

            def state(self, p, t, g):
                ends.append(self.lid)
                return self.answer(p, t) if self.answer is not None else self.v.state(p, t, g)
        with mock.patch.object(sv, "_segment", seg):
            out = sv.inward(e, {**views, "mantle": Spy("mantle", views["mantle"]),
                                "core": Spy("core", views["core"], core_answer)}, x, context.Options())
        return out, ends, views

    def test_bottom_view_when_it_answers(self):
        out, ends, views = self._run()
        self.assertTrue(out.floor_end)
        self.assertEqual(out.entered[-1], "mantle")
        self.assertEqual(ends[-1:], ["core"])                   # one material for F: no jump at the end-layer switch
        self.assertEqual(ends.count("core"), 1)                 # the end read is the core view's only read (68)
        self.assertEqual(out.rho_end, views["core"].state(out.y[1], out.y[2], None)[0])

    def test_ended_layer_when_the_bottom_refuses_its_domain(self):
        """The finding's case: the bottom material refuses, by its domain, a state it never reached; not a wall."""
        for name, rec in (("legacy edge", lm.MaterialRefusal("fe", 1.0, 1.0, "PhaseGap", "planted", axis="P")),
                          ("record edge", mv.RecordRefusal("fe", 1.0, 1.0, "input.material_out_of_data", "planted")),
                          ("record-declared edge id", mv.RecordRefusal("fe", 1.0, 1.0, "input.planted_declared_edge",
                                                                      "planted"))):
            with self.subTest(name):
                out, ends, _v = self._run(lambda p, t, rec=rec: st.Stop("refused", rec))
                self.assertEqual(ends[-2:], ["core", "mantle"])
                self.assertEqual(ends.count("core"), 1)
                self.assertNotIsInstance(out, st.Stop)
                self.assertIsNotNone(out.F)
                self.assertTrue(out.floor_end)

    def test_any_other_stop_propagates(self):
        """r2 H1 on c8274a73: a non-domain Stop from the bottom view is not answered by the ended layer's view; the
        pass ends with that Stop (at its reached state)."""
        for name, stop in (("non-finite", st.Stop("non_finite", {"planted": True})),
                           ("engine ValueError", st.Stop("refused", lm.MaterialRefusal("fe", 1.0, 1.0, "ValueError",
                                                                                       "planted", axis="none"))),
                           ("field overlap", st.Stop("refused", mv.RecordRefusal("fe", 1.0, 1.0,
                                                                                 "material.field_overlap", "planted"))),
                           ("check grammar", st.Stop("refused", mv.RecordRefusal("fe", 1.0, 1.0,
                                                                                 "material.check_grammar", "planted")))):
            with self.subTest(name):
                out, ends, _v = self._run(lambda p, t, stop=stop: stop)
                self.assertEqual(ends[-1:], ["core"])          # the mantle's view is not read after the core's Stop
                self.assertEqual(ends.count("core"), 1)
                self.assertIsInstance(out, st.Stop)
                self.assertEqual((out.kind, out.record), (stop.kind, stop.record))


class GitWorkTree(unittest.TestCase):
    """G2-R-07: outside a git work tree the solve fails before any pass, with the reason named."""

    def test_raises_before_a_pass(self):
        passes = []
        with mock.patch("subprocess.run", lambda *a, **k: subprocess.CompletedProcess(a[0], 128, "", "not a repo")), \
                mock.patch.object(sv, "inward", lambda *a, **k: passes.append(1)):
            with self.assertRaises(RuntimeError):
                sv.solve(_earth(), OPT)
        self.assertEqual(passes, [])


class ProbesStayInRange(unittest.TestCase):
    """G2-R-10: a probe beyond the closure range is not taken; that side reports «outside_range»."""

    def test_outside(self):
        rt = {"delta": 1.0, "tol_F": 1e-9, "far": (None, None)}
        seen = []
        got = sv._side_check(lambda x: seen.append(x) or 0.0, 9.5, 0.0, 1.0, rt, 0.0, 10.0)
        self.assertEqual((got["stop"], got["ok"], seen), ("outside_range", False, []))


if __name__ == "__main__":
    unittest.main()
