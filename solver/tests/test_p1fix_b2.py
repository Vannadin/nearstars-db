# 리뷰 수정 B2 시험 — 닫힘·풀이의 빈 시험 채우기: 거절 매핑 갈래·결과 꼬리·탐침 거짓양성·solve_id·구간·예산·확인 사격·민감도 갈래·지구 절대값
"""Post-phase-1 review fix batch B2 (rewrite/p1review/fix-plan.md (B)): tests only, for G2-T-01, -02, -04 … -10
(G2-T-03 closes with A3). Each class names the finding and the mutation it kills.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_p1fix_b2
"""
import dataclasses
import math
import unittest
from types import SimpleNamespace as NS
from unittest import mock

from solver import closure as cl, context, from_v1, refusals, result, solve as sv
from solver import stepper as st

NODE = {"m": 1.5, "r": 2.5, "P": 3.5e9, "T": 4500.0}


def _earth():
    body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
    return body


def plain(x):
    """Evidence is frozen to tuples; compare it as lists."""
    if isinstance(x, (list, tuple)):
        return [plain(v) for v in x]
    if isinstance(x, dict):
        return {k: plain(v) for k, v in x.items()}
    return x


def _trial(x, F, kind="scan", stop=None):
    return cl.Trial(x, F, None if F is not None else (stop or st.Stop("refused")), kind)


class ToRefusalBranches(unittest.TestCase):
    """G2-T-01: every branch of `_to_refusal`, each evidence key from a distinct planted value (a swapped or misspelled
    key, or a wrong id, fails)."""

    def _map(self, kind, rec, state=NODE):
        return sv._to_refusal(st.Stop(kind, rec, state), "fixture.solve", 7.25, "R", "wall")

    def _common(self, got, state=NODE):
        ev = got.evidence
        self.assertEqual((ev["x"], ev["closure_kind"], ev["pass_kind"]), (7.25, "R", "wall"))
        self.assertEqual(ev.get("state"), state)

    def test_chatter(self):
        got = self._map("chatter", {"event": "onset_x", "count": 9, "cap_name": "EVENT_REWALKS", "cap_value": 8})
        self.assertEqual(got.id, "solve.event_chatter")
        self.assertEqual({k: got.evidence[k] for k in ("event_name", "count", "cap_name", "cap_value")},
                         {"event_name": "onset_x", "count": 9, "cap_name": "EVENT_REWALKS", "cap_value": 8})
        self._common(got)

    def test_chatter_wrapped_in_a_refused_stage(self):
        inner = st.Stop("chatter", {"event": "e2", "count": 5, "cap_name": "EVENT_REWALKS", "cap_value": 4})
        got = self._map("refused", inner)
        self.assertEqual((got.id, got.evidence["event_name"], got.evidence["count"]), ("solve.event_chatter", "e2", 5))

    def test_h_min(self):
        rec = {"h": 1.0e-3, "h_min": 2.0e-3, "m_at": 3.0e22, "err_norm": 4.0, "rejected_in_row": 5}
        got = self._map("h_min", rec)
        self.assertEqual(got.id, "solve.unlocated_discontinuity")
        self.assertEqual({k: got.evidence[k] for k in rec}, rec)
        self._common(got)

    def test_lid_unconverged(self):
        got = self._map("lid_unconverged", {"layer_id": "lid", "trail": (1600.0, 1610.0), "iters": 8, "tol": 1e-7})
        self.assertEqual(got.id, "solve.lid_unconverged")
        self.assertEqual((got.evidence["layer_id"], plain(got.evidence["trail"]), got.evidence["iters"], got.evidence["tol"]),
                         ("lid", [1600.0, 1610.0], 8, 1e-7))
        self._common(got)

    def test_lid_input_surface_temperature(self):
        got = self._map("lid_input", {"field": "surface_temperature_k", "layer_id": "lid", "value": None})
        self.assertEqual((got.id, got.evidence["key"]), ("input.missing_key", "surface_temperature_k"))

    def test_lid_input_depth(self):
        got = self._map("lid_input", {"field": "depth_km", "layer_id": "lid", "value": -3.0})
        self.assertEqual((got.id, got.evidence["layer_id"]), ("input.extent_invalid", "lid"))
        self.assertIn("-3.0", got.evidence["why"])

    def test_lid_base_not_reached(self):
        got = self._map("lid_base_not_reached", {"layer_id": "lid", "m": 6.5e24})
        self.assertEqual(got.id, "solve.layer_order")
        ev = got.evidence
        self.assertEqual((ev["layer_id"], ev["rule"], ev["got_m"]), ("lid", "depth_from_surface", 6.5e24))
        self.assertTrue(math.isnan(ev["got_r"]))
        self._common(got)

    def test_layer_order_passes_its_record(self):
        rec = {"layer_id": "mantle", "rule": "r_monotone", "expected": "r falls", "got_m": 1.0e24, "got_r": 3.0e6}
        got = self._map("layer_order", rec)
        self.assertEqual(got.id, "solve.layer_order")
        self.assertEqual({k: got.evidence[k] for k in rec}, rec)
        self._common(got)

    def test_max_steps_is_a_no_answer_with_its_budget(self):
        got = self._map("max_steps", {"budget": 123457})
        self.assertIsInstance(got, result.NoAnswer)
        self.assertEqual((got.reason, got.evidence["budget_name"], got.evidence["budget_value"], got.evidence["x"],
                          got.evidence["pass_kind"]), ("unconverged", "MAX_STEPS_SOLVE", 123457, 7.25, "wall"))

    def test_an_unmapped_kind_raises(self):
        with self.assertRaises(RuntimeError):
            self._map("no_such_kind", {})


class SolveOutcomeTails(unittest.TestCase):
    """G2-T-01 (the tails) and G2-T-05 (no_bracket's evidence): solve() on a planted closure outcome."""

    def _solve(self, out, **opt):
        with mock.patch.object(cl, "solve_scalar", return_value=out):
            got, _w = sv.solve(self.body, context.Options(sensitivity_dt=0.0, **opt))
        return got

    @classmethod
    def setUpClass(cls):
        cls.body = _earth()

    def test_two_roots(self):
        trials = [_trial(6.0e6, -1.0), _trial(6.2e6, None), _trial(6.4e6, 2.0), _trial(6.6e6, -3.0)]
        got = self._solve(NS(kind="two_roots", roots=[6.3e6, 6.5e6], trials=trials, walls=[], detail={}))
        self.assertEqual(got.id, "solve.two_roots")
        ev = got.evidence
        self.assertEqual((ev["x"], ev["pass_kind"], ev["roots"], ev["n_scan"]),
                         (None, "scan", (6.3e6, 6.5e6), context.Options().n_scan))
        self.assertEqual(plain(ev["F_scan"]), [[6.0e6, -1.0], [6.4e6, 2.0], [6.6e6, -3.0]])

    def test_unconverged_names_its_budget_and_last_residual(self):
        trials = [_trial(6.0e6, -1.0), _trial(6.4e6, 0.25, "brent"), _trial(6.5e6, None, "brent")]
        for budget, value in (("MAX_SPLITS", cl.MAX_SPLITS), (None, cl.CLOSE_ITERS)):
            with self.subTest(budget=budget):
                got = self._solve(NS(kind="unconverged", roots=[], trials=trials, walls=[],
                                     detail={"budget": budget} if budget else {}))
                self.assertIsInstance(got, result.NoAnswer)
                self.assertEqual((got.evidence["budget_name"], got.evidence["budget_value"], got.evidence["last_residual"]),
                                 (budget or "CLOSE_ITERS", value, 0.25))

    def test_no_bracket_evidence(self):
        chatter = st.Stop("chatter", {"event": "e", "count": 3, "cap_name": "EVENT_REWALKS", "cap_value": 2}, NODE)
        steps = st.Stop("max_steps", {"budget": 99})
        trials = [_trial(6.0e6, 1.0), _trial(6.1e6, 2.0), _trial(6.2e6, None, stop=chatter), _trial(6.3e6, 3.0),
                  _trial(6.4e6, None, stop=steps), _trial(6.5e6, 4.0)]
        walls = [cl.Wall(6.2e6, chatter, 6.1e6), cl.Wall(6.4e6, steps, 6.3e6)]
        got = self._solve(NS(kind="no_bracket", roots=[], trials=trials, walls=walls, detail={}))
        self.assertEqual(got.id, "solve.no_bracket")
        ev = got.evidence
        self.assertEqual((ev["x_lo"], ev["x_hi"], ev["F_lo"], ev["F_hi"]),
                         (self.body.closure.lo, self.body.closure.hi, 1.0, 4.0))
        self.assertEqual(plain(ev["solved_regions"]), [[6.0e6, 6.1e6], [6.3e6, 6.3e6], [6.5e6, 6.5e6]])
        self.assertEqual(plain(ev["walls"]), [
            {"x": 6.2e6, "outcome_kind": "refusal", "id_or_reason": "solve.event_chatter", "state": NODE, "located": True},
            {"x": 6.4e6, "outcome_kind": "no_answer", "id_or_reason": "unconverged", "state": None, "located": True}])

    def test_an_unlocated_wall_leaves_the_search_unconverged(self):
        stop = st.Stop("chatter", {"event": "e", "count": 3, "cap_name": "EVENT_REWALKS", "cap_value": 2})
        trials = [_trial(6.0e6, 1.0), _trial(6.2e6, None, stop=stop)]
        got = self._solve(NS(kind="no_bracket", roots=[], trials=trials,
                             walls=[cl.Wall(6.2e6, stop, 6.0e6, located=False)], detail={}))
        self.assertIsInstance(got, result.NoAnswer)
        self.assertEqual((got.evidence["budget_name"], got.evidence["budget_value"], got.evidence["x"]),
                         ("WALL_SHOTS", cl.WALL_SHOTS, 6.2e6))


class Regions(unittest.TestCase):
    """G2-T-05: `_regions` values: splits at a refusal, single-point stretches, refusing ends."""

    def test_values(self):
        cases = [
            ([_trial(1.0, 1.0), _trial(2.0, 1.0), _trial(3.0, 1.0)], [[1.0, 3.0]]),
            ([_trial(1.0, None), _trial(2.0, 1.0), _trial(3.0, 1.0), _trial(4.0, None)], [[2.0, 3.0]]),
            ([_trial(1.0, 1.0), _trial(2.0, None), _trial(3.0, 1.0), _trial(4.0, None), _trial(5.0, 1.0),
              _trial(6.0, 1.0)], [[1.0, 1.0], [3.0, 3.0], [5.0, 6.0]]),
            ([_trial(1.0, None), _trial(2.0, None)], []),
        ]
        for trials, want in cases:
            with self.subTest(want=want):
                self.assertEqual(sv._regions(NS(trials=trials)), want)


class ProbeFalsePositive(unittest.TestCase):
    """G2-T-02: clean roots carry no closure_probe_disclosure, and the probes did run (both sides judged ok with a
    finite allowance). Forcing `ok` False, or flipping the slope-sign clause, fails here."""

    def test_clean_declared_roots_disclose_nothing(self):
        for name in ("earth", "venus"):
            with self.subTest(body=name):
                body, _aside = from_v1.load_v1(f"engine/bodies/{name}.yaml")
                seen, real = [], sv._side_check

                def spy(*a, **k):
                    out = real(*a, **k)
                    seen.append(out)
                    return out
                with mock.patch.object(sv, "_side_check", spy):
                    ans, _x = sv.solve(body, context.Options(sensitivity_dt=0.0))
                self.assertIsInstance(ans, result.Answer)
                self.assertNotIn("closure_probe_disclosure", [n.kind for n in ans.notes])
                self.assertEqual(len(seen), 2)
                for sd in seen:
                    self.assertTrue(sd["ok"])
                    self.assertGreater(sd["allowed"], 0.0)
                    self.assertLessEqual(sd["deviation"], sd["allowed"])


class SolveIdMovesWithTheBody(unittest.TestCase):
    """G2-T-04: with the views held fixed, a change in a Body field the solve reads moves solve_id; the same Body
    keeps it."""

    def test_closure_range_moves_the_id(self):
        body = _earth()
        views = sv._views(body)
        moved = dataclasses.replace(body, closure=dataclasses.replace(body.closure, hi=body.closure.hi * 1.001))
        opt = context.Options(sensitivity_dt=0.0)
        a1, _ = sv.solve(body, opt, views=views)
        a2, _ = sv.solve(body, opt, views=views)
        a3, _ = sv.solve(moved, opt, views=views)
        sid = lambda a: a.quantities[0].provenance.solver.solve_id
        self.assertEqual(sid(a1), sid(a2))
        self.assertNotEqual(sid(a1), sid(a3))


class SplitBudget(unittest.TestCase):
    """G2-T-06: the planted F needs exactly one split. Budget 0 → unconverged; budget 1 → resolved. `range(MAX_SPLITS)`
    fails the second, `range(MAX_SPLITS + 2)` the first."""

    def test_exactly_one_split(self):
        scan = set(cl.scan_points(1.0, 10.0))
        F = lambda x: x - 2.0 if (x in scan or not 1.5 < x < 3.0) else st.Stop("domain", {})
        for budget, unconverged in ((0, True), (1, False)):
            with self.subTest(budget=budget), mock.patch.object(cl, "MAX_SPLITS", budget):
                out = cl.solve_scalar(F, 1.0, 10.0)
                self.assertEqual(out.kind == "unconverged", unconverged, (out.kind, out.detail.get("budget")))


class BrentBudget(unittest.TestCase):
    """G2-T-07: Brent out of CLOSE_ITERS gives «unconverged», and solve() reports that budget's own value."""

    def test_close_iters_exhausted(self):
        with mock.patch.object(cl, "CLOSE_ITERS", 2):
            out = cl.solve_scalar(lambda x: math.tanh(x - 3.3), 1.0, 10.0)
        self.assertEqual(out.kind, "unconverged")
        self.assertEqual(out.detail["problems"][0][0], "unconverged")

    def test_solve_reports_the_close_iters_value(self):
        body = _earth()
        with mock.patch.object(cl, "CLOSE_ITERS", 3):
            got, _w = sv.solve(body, context.Options(sensitivity_dt=0.0))
        self.assertIsInstance(got, result.NoAnswer)
        self.assertEqual((got.evidence["budget_name"], got.evidence["budget_value"]), ("CLOSE_ITERS", 3))


class ConfirmingShots(unittest.TestCase):
    """G2-T-08: the fold at the range end, the CONFIRM_MAX budget, and the stretch rule around an island."""

    def test_a_refusal_at_the_range_end_is_confirmed_inside_the_range(self):
        F = lambda x: st.Stop("domain", {}) if x == 10.0 else x - 2.0
        out = cl.solve_scalar(F, 1.0, 10.0)
        conf = [t for t in out.trials if t.kind == "confirm"]
        self.assertTrue(conf)
        self.assertTrue(all(1.0 <= t.x <= 10.0 for t in conf))
        self.assertIn((10.0, "isolated"), [(t.x, t.kind) for t in out.trials])

    def test_the_budget_ends_a_chain_of_changing_reasons(self):
        n = [0]

        def F(x):
            n[0] += 1
            return st.Stop(f"reason{n[0]}", {})
        for budget in (2, 4):
            with self.subTest(budget=budget), mock.patch.object(cl, "CONFIRM_MAX", budget):
                n[0], trials = 0, []
                what, x_last, stop = cl._confirm_chain(F, 5.0, st.Stop("reason0", {}), 4.0, 1.0, 10.0, trials)
                shots = [t for t in trials if t.kind in ("confirm", "isolated")]   # each superseded candidate is isolated
                self.assertEqual((what, len(shots)), ("wall", budget))
                self.assertEqual((x_last, stop.kind), (shots[-1].x, f"reason{budget}"))   # the last stands, unconfirmed

    def test_an_island_around_the_only_root_is_no_bracket_not_unconverged(self):
        F = lambda x: st.Stop("domain", {"x": x}) if 4.00 < x < 4.05 else x - 4.02
        out = cl.solve_scalar(F, 1.0, 10.0)
        self.assertEqual(out.kind, "no_bracket")


class SensitivityBranches(unittest.TestCase):
    """G2-T-09: the sensitivity block's fallbacks, its radius exclusion and every sensitivity_not_measured site."""

    @classmethod
    def setUpClass(cls):
        cls.body = _earth()

    def _sens(self, ans):
        return [n for n in ans.notes if n.kind.startswith("sensitivity")]

    def test_fallback_to_the_full_range(self):
        real, calls = cl.solve_scalar, []

        def ss(F, lo, hi, n=cl.N_SCAN, *a, **k):
            calls.append(n)
            if n == 5:                                         # the narrow re-solve: planted to miss
                return NS(kind="no_bracket", roots=[], trials=[], walls=[], detail={})
            return real(F, lo, hi, n, *a, **k)
        with mock.patch.object(cl, "refine", lambda *a, **k: None), mock.patch.object(cl, "solve_scalar", ss):
            ans, _x = sv.solve(self.body, context.Options())
        self.assertEqual(calls[1:], [5, context.Options().n_scan])     # narrow, then the full range
        self.assertTrue(any(q.sensitivity is not None for q in ans.quantities))

    def test_the_t_plus_delta_solve_without_a_root(self):
        real, calls = cl.solve_scalar, []

        def ss(*a, **k):
            calls.append(1)
            if len(calls) == 1:                                # the accepted solve
                return real(*a, **k)
            return NS(kind="no_bracket", roots=[], trials=[], walls=[], detail={})
        with mock.patch.object(cl, "refine", lambda *a, **k: None), mock.patch.object(cl, "solve_scalar", ss):
            ans, _x = sv.solve(self.body, context.Options())
        self.assertEqual(len(calls), 3)                        # narrow, then the full range, both without a root
        n = self._sens(ans)
        self.assertEqual([x.kind for x in n], ["sensitivity_not_measured"])
        self.assertIn("no_bracket", n[0].text)
        self.assertTrue(all(q.sensitivity is None for q in ans.quantities))

    def test_the_t_plus_delta_pass_stops(self):
        real, n = sv.inward, [0]
        t0 = self.body.surface.t_pot

        def inward(body, views, x, opt, want_graze=True):
            if body.surface.t_pot != t0 and want_graze:          # the accepted pass at T_pot + δ
                return st.Stop("max_steps", {"budget": 1})
            return real(body, views, x, opt, want_graze=want_graze)
        with mock.patch.object(sv, "inward", inward):
            ans, _x = sv.solve(self.body, context.Options())
        n = self._sens(ans)
        self.assertEqual([(x.kind, x.fields) for x in n], [("sensitivity_not_measured", {"dt": 10.0})])
        self.assertIn("max_steps", n[0].text)

    def test_the_t_plus_delta_views_fail(self):
        real = sv._views

        def views(body, x=None, registry=None, silicate=False):    # silicate: the silicate registration's switch
            if body.surface.t_pot != self.body.surface.t_pot:
                return refusals.make("input.missing_key", "fixture", key="planted")
            return real(body, x, registry, silicate)
        with mock.patch.object(sv, "_views", views):
            ans, _x = sv.solve(self.body, context.Options())
        self.assertEqual([x.kind for x in self._sens(ans)], ["sensitivity_not_measured"])
        self.assertIn("views", self._sens(ans)[0].text)

    def test_a_graze_appearing_at_t_plus_delta_omits_the_sensitivity(self):
        real, t0 = sv.inward, self.body.surface.t_pot

        def inward(body, views, x, opt, want_graze=True):
            got = real(body, views, x, opt, want_graze=want_graze)
            if body.surface.t_pot != t0 and want_graze and not isinstance(got, st.Stop):
                got = dataclasses.replace(got, graze=NS(curve="planted", material="m", p=1.0, g=0.0))
            return got
        with mock.patch.object(sv, "inward", inward):
            ans, _x = sv.solve(self.body, context.Options())
        self.assertEqual([x.kind for x in self._sens(ans)], ["sensitivity_across_boundary_change"])

    def test_radius_has_no_sensitivity_when_it_is_declared(self):
        e = dataclasses.replace(self.body, layers=tuple(l for l in self.body.layers if l.thermal != "conductive"))
        fwd, _w = sv.solve(e)
        R = next(q.point for q in fwd.quantities if q.key == "radius")
        layers = tuple(dataclasses.replace(l, extent=None) if l.id == "core" else l for l in e.layers)
        from solver import body as bd
        inv = dataclasses.replace(e, layers=layers, closure=bd.Closure("boundary_mass", 0.05, 0.95, "core"),
                                  radius=bd.Declared(R, "m"))
        ans, _w = sv.solve(inv)
        sens = {q.key: q.sensitivity for q in ans.quantities}
        self.assertIsNone(sens.get("radius"))
        self.assertTrue(any(v is not None for k, v in sens.items() if k != "radius"))   # control: others measured
        self.assertIsNotNone({q.key: q.sensitivity for q in fwd.quantities}.get("radius"))


class EarthAbsolute(unittest.TestCase):
    """G2-T-10: Earth's declared answer pinned to absolute values: the PC landing record at 3d170377
    (artifacts 64ed0626, batch-3d170377-landing/o9/earth/earth__declared.json, blob 29ffc940, Python 3.12.3), at 1e-6 relative,
    which is past the Mac/PC band (Earth 4.1e-6 on the largest key at a moved state, ≤ 1e-8 at the declared state) and
    far inside any constant's change."""

    def test_declared_values(self):
        ans, _x = sv.solve(_earth(), context.Options(sensitivity_dt=0.0))
        got = {q.key: q.point for q in ans.quantities}
        for k, v in PINNED_EARTH.items():
            with self.subTest(key=k):
                self.assertLess(abs(got[k] - v) / abs(v), 1e-6, (got[k], v))


PINNED_EARTH = {                       # record blob 29ffc940
    "radius": 6390103.2933283085, "nmoi": 0.32971838204611453, "core_radius": 3485043.53751115,
    "cmb_pressure": 135254666993.38823, "core_pressure": 358352625161.5081, "cmb_temperature": 2527.3154329600775,
    "core_temperature": 3197.2526014468026, "core_radius_fraction": 0.545381408959346,
}
# core_temperature re-pinned (centre-series post-freeze note 2, its «Resolution (directing 10-18)»): from 29ffc940's
# 3197.1409514076045 to the PC's own read at Job B's TIP af8408a7, 3197.2526014468026 K (+3.49e-5, the centre series'
# (dT/dP)_ε·ΔP), quoted from the PC suite (repair 1 and 0 alike) in Job B's judge of record (artifacts
# ea-jobB-out-af8408a7 2595d66b, pc/ea-jobB/out-af8408a7/judge-81fb95db.txt, blob 6c662a63); the other keys stay at
# 29ffc940 (the series moves none of them, and they pass at 1e-6 there)


if __name__ == "__main__":
    unittest.main()
