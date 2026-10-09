# §T 화성 무거운 시험 — 옛 두-가족 점의 근 개수(N_SCAN 대 4×), 녹는 창 12점 기준과 심은 톱니 대조 (PC 에서 NEARSTARS_HEAVY=1)
"""phase1-design.frozen.md §T «Two roots» and «Melt window» (§A1.8, as amended by post-freeze note 4), on the Mars
forward member (o9-forward-member-note): composition, core and basal mass fixed at the declared answer, R free.
Each Mars solve is ~10–30 s, so these run only with NEARSTARS_HEAVY=1 (the PC job).

    NEARSTARS_HEAVY=1 solver/.venv/bin/python -m unittest solver.tests.test_t_mars
"""
import dataclasses
import os
import unittest

from solver import context, from_v1, member as mb, result, solve as sv

HEAVY = os.environ.get("NEARSTARS_HEAVY") == "1"
OPT = context.Options(sensitivity_dt=0.0)
EPS_MELT = 5.858e-4                       # R-RK-13 (ii)
PLANTED_SAW = 0.0165                      # note 4 item 4: ±1.65 % alternating, the old 3.3 % neighbour step


def _member():
    m, _ = from_v1.load_v1("engine/bodies/mars.yaml")
    fb, _info = mb.member_of(m)
    return fb


def _at(fb, t, opt):
    return sv.solve(dataclasses.replace(fb, surface=dataclasses.replace(fb.surface, t_pot=t)), opt)[0]


def _roots(out) -> int:
    if isinstance(out, result.Answer):
        return 1
    if getattr(out, "id", None) == "solve.two_roots":
        return len(out.evidence["roots"])
    return 0


@unittest.skipUnless(HEAVY, "NEARSTARS_HEAVY=1 (PC job)")
class TwoRootsStable(unittest.TestCase):
    """At the old two-family points the root count at N_SCAN equals the count at 4 × N_SCAN (r2 M3). Control: the
    count itself is reported per point; a synthetic U-shaped F giving two roots is test_closure.TwoRoots."""

    POINTS = (2080.7, 1685.6, 1685.75, 1685.9)

    def test_same_count(self):
        fb = _member()
        for t in self.POINTS:
            a = _roots(_at(fb, t, OPT))
            b = _roots(_at(fb, t, dataclasses.replace(OPT, n_scan=4 * OPT.n_scan)))
            self.assertEqual(a, b, t)


def _melt_series(fb):
    rb, rp, chatter = [], [], 0
    for t in range(1978, 1990):
        out = _at(fb, float(t), OPT)
        if getattr(out, "id", None) == "solve.event_chatter":
            chatter += 1
        q = {x.key: x.point for x in out.quantities} if isinstance(out, result.Answer) else {}
        rb.append(q.get("core_plus_layer_radius_solved_km"))
        rp.append(q.get("radius"))
    return rb, rp, chatter


def _criterion(rb, rp):
    if any(x is None for x in rb + rp):
        return False
    step = max(abs(rb[i + 1] - rb[i]) / rb[i] for i in range(len(rb) - 1))
    return step <= EPS_MELT and all(rp[i + 1] > rp[i] for i in range(len(rp) - 1))


@unittest.skipUnless(HEAVY, "NEARSTARS_HEAVY=1 (PC job)")
class MeltWindow(unittest.TestCase):
    """R-RK-13 (ii): 12 points 1978–1989 K, max 1 K-neighbour |Δr_b|/r_b ≤ 5.858e-4, r_p monotone, zero event_chatter
    (measured on the Mac: 1.24e-5). Control (note 4 item 4): ±1.65 % alternating planted on the computed r_b must fail —
    it proves only that the criterion's failure path works; the rewrite does not make the defect itself."""

    @classmethod
    def setUpClass(cls):
        cls.rb, cls.rp, cls.chatter = _melt_series(_member())

    def test_criterion(self):
        self.assertTrue(_criterion(self.rb, self.rp), (self.rb, self.rp))
        self.assertEqual(self.chatter, 0)

    def test_control_planted_sawtooth_fails(self):
        saw = [x * (1 + PLANTED_SAW * (1 if i % 2 == 0 else -1)) for i, x in enumerate(self.rb)]
        self.assertFalse(_criterion(saw, self.rp))


if __name__ == "__main__":
    unittest.main()
