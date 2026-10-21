# 리뷰 수정 A3 시험 — 전도 덮개 경로: 덮개 안 사건·스침이 통과 기록에 닿는지, 덮개의 걸음 상한, N_acc 는 받아들인 통과만, 덮개만 있는 천체 거절
"""Post-phase-1 review fix batch A3 (rewrite/p1review/fix-plan.md; phase-1 design note 13 §4): G1-R-02 = G2-R-01,
G1-C-04 = G2-C-06 (closing G2-T-03), G2-C-04, G2-C-05 with LOW G1-C-05. Each test fails on cc1d20f0.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_p1fix_a3
"""
import dataclasses
import unittest
from types import SimpleNamespace as NS
from unittest import mock

from solver import body as bd, context, events, from_v1, lid, member as mb, result, solve as sv

OPT = context.Options(sensitivity_dt=0.0)


def _earth(t_pot=None):
    body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
    if t_pot is not None:
        body = dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=t_pot))
    return body


def _accepted_pass(body):
    """(PassOut, the accepted pass's LidResult) at the body's root."""
    ans, x = sv.solve(body, OPT)
    assert isinstance(ans, result.Answer), getattr(ans, "text", ans)
    got, real = [], lid.lid_pass

    def spy(*a, **k):
        r = real(*a, **k)
        got.append(r)
        return r
    with mock.patch.object(lid, "lid_pass", spy):
        out = sv.inward(body, sv._views_at(body, sv._views(body), x), x, context.Options())
    return out, got[-1]


class LidEventsReachThePass(unittest.TestCase):
    """G1-R-02 = G2-R-01: Earth at 1800 K crosses the solidus inside its 135 km lid. The landed onset was dropped."""

    def test_the_lid_onset_is_in_the_pass_events(self):
        out, lr = _accepted_pass(_earth(1800.0))
        names = [e[0] for e in lr.events]
        self.assertTrue(any(n.startswith("onset:") for n in names), names)
        self.assertEqual(out.events[:len(names)], names)              # the lid's, first, in order

    def test_control_no_lid_onset_at_1600(self):
        out, lr = _accepted_pass(_earth(1600.0))
        self.assertEqual(lr.events, ())
        self.assertFalse(any(n.startswith("onset:") for n in out.events))


class LidGraze(unittest.TestCase):
    """G1-R-02: the lid runs a graze monitor on T_ad, one per pass, and the accepted pass's graze reaches the pass."""

    def test_the_monitor_reads_t_ad_and_the_last_pass_is_kept(self):
        seen, passes = [], []

        class Mon:
            t_index = 2                                                # as inward's factory builds it (SP-S-13)
            mat = None                                                 # names no material: no hand-over (X-04)

            def __init__(self):
                self.best = NS(curve="planted", material="m", p=1.0, g=float(len(passes)), m=0.0)
                passes.append(self)

            def __call__(self, m, y):
                seen.append((y[2], y[3]))
        body = _earth(1800.0)
        ans, x = sv.solve(body, OPT)
        # the lid pass as inward calls it (its r_scale, options and events), with the planted monitor in place of
        # inward's: a hand-built call (r_scale 6e6, default PassOptions) sat on the lid's noise floor and stopped
        # lid_unconverged once A5's fsum moved the last digits (the f7a5b95c suite)
        real, results, built = lid.lid_pass, [], []

        def call(*a, **k):
            built.append(k["monitor"]())
            got = real(*a, **{**k, "monitor": Mon})
            results.append(got)
            return got
        with mock.patch.object(lid, "lid_pass", call):
            sv.inward(body, sv._views_at(body, sv._views(body), x), x, context.Options())
        got = results[-1]
        self.assertIsInstance(got, lid.LidResult, got)
        self.assertTrue(seen)
        # review 2 SP-S-13: the monitor gets the state as stepped (T_ad at y[2], the lid's T at y[3], not rebuilt) and
        # inward's own monitor reads T_ad by its t_index
        self.assertTrue(any(a != b for a, b in seen))
        self.assertTrue(built and all(b.t_index == 2 for b in built))
        self.assertGreater(len(passes), 1)
        self.assertIs(got.graze, passes[-1].best)                     # the accepted (last) pass's

    def test_inward_takes_the_lids_graze(self):
        body = _earth(1800.0)
        ans, x = sv.solve(body, OPT)
        real = lid.lid_pass
        planted = events.Graze("planted", "m", 1.0e9, 1.0e-6, 1.0)

        def fake(*a, **k):
            return dataclasses.replace(real(*a, **k), graze=planted)
        with mock.patch.object(lid, "lid_pass", fake):
            out = sv.inward(body, sv._views_at(body, sv._views(body), x), x, context.Options())
        self.assertIs(out.graze, planted)


def _mars_with_lid(depth=100.0e3):
    body, _aside = from_v1.load_v1("engine/bodies/mars.yaml")
    body, _m = mb.member_of(body)
    top = body.layers[-1]
    lid_layer = dataclasses.replace(top, id="lithosphere", role="lid", thermal="conductive",
                                    extent=bd.Extent("depth_from_surface", depth))
    t_s = body.surface.t_s if body.surface.t_s is not None else 210.0
    return dataclasses.replace(body, layers=(*body.layers, lid_layer),
                               surface=dataclasses.replace(body.surface, t_s=t_s))


class LidStepCap(unittest.TestCase):
    """G1-C-04 = G2-C-06 (closes G2-T-03): a table-phase lid (Mars's mantle material) passes the note-12 cap and takes
    more steps than without it."""

    def test_capped_lid_takes_more_steps(self):
        body = _mars_with_lid()
        views = sv._views(body)
        x = 0.5 * (body.closure.lo + body.closure.hi)
        real = lid.lid_pass

        def steps(cap_on):
            got = []

            def spy(*a, **k):
                r = real(*a, **k)
                got.append((k.get("h_cap"), r))
                return r
            # the lid's cap is events.step_cap(mat, t_index=3) since note 13a item 4; the band test is held off in
            # both runs, so the step counts differ by the cap alone
            real_cap = events.step_cap
            cap = real_cap if cap_on else (lambda *a, **k: None)
            with mock.patch.object(lid, "lid_pass", spy), mock.patch.object(events, "step_cap", cap), \
                    mock.patch.object(events, "band_check", lambda *a, **k: None):
                sv.inward(body, sv._views_at(body, views, x), x, context.Options())
            cap, r = got[-1]
            self.assertEqual(cap is not None, cap_on)
            self.assertIsInstance(r, lid.LidResult, r)
            return r.counters["accepted"]
        self.assertGreater(steps(True), steps(False))


class LidOnlyBody(unittest.TestCase):
    """G2-C-04 (note 13 §4): a body whose only layer is a conductive lid is refused by name."""

    def test_refused(self):
        e = _earth()
        lid_only = dataclasses.replace(e, layers=(e.layers[-1],))
        got, _w = sv.solve(lid_only, OPT)
        self.assertIsInstance(got, result.Refusal)
        self.assertEqual((got.id, got.evidence["rule"]), ("input.cross_field", "lid_only_body"))

    def test_control_earth_answers(self):
        got, _w = sv.solve(_earth(), OPT)
        self.assertIsInstance(got, result.Answer)


class AcceptedPassNAcc(unittest.TestCase):
    """G2-C-05 (with LOW G1-C-05): N_acc counts the accepted lid pass's steps only; the discarded passes' are kept for
    cost under lid_discarded_accepted."""

    def test_n_acc(self):
        body = _earth(1800.0)
        ans, x = sv.solve(body, OPT)
        lids, segs, real_l, real_s = [], [], lid.lid_pass, sv._segment

        def spy_l(*a, **k):
            r = real_l(*a, **k)
            lids.append(r)
            return r

        def spy_s(*a, **k):
            r = real_s(*a, **k)
            segs.append(r)
            return r
        with mock.patch.object(lid, "lid_pass", spy_l), mock.patch.object(sv, "_segment", spy_s):
            out = sv.inward(body, sv._views_at(body, sv._views(body), x), x, context.Options())
        lr = lids[-1]
        self.assertEqual(out.counters["accepted"], lr.counters["accepted"] + sum(s.counters.accepted for s in segs))
        self.assertGreater(lr.discarded["accepted"], 0)                # Earth's lid iterates
        self.assertEqual(out.counters["lid_discarded_accepted"], lr.discarded["accepted"])


if __name__ == "__main__":
    unittest.main()
