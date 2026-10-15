# 순방향 표 구성원 시험 — 선언 온도에서 구성원이 선언 답을 되풀이하고, 다른 온도에서 옛 O9 구성원 값에 붙으며, 순방향 천체는 그대로임
"""solver.member (owner-direction «O9 for inverse bodies: compare like for like»; o9-forward-member-note.md)."""
import dataclasses
import json
import os
import unittest
from pathlib import Path

from solver import context, from_v1, member as mb, result, run_oracle as ro, solve as sv

OPT = context.Options(sensitivity_dt=0.0)
# the artifacts checkout: NEARSTARS_ARTIFACTS (the PC batch sets it), else beside the worktree on the Mac
O4O9 = Path(os.environ.get("NEARSTARS_ARTIFACTS") or Path(__file__).resolve().parents[4] / "NearStars-artifacts") \
    / "rewrite/oracle/097a8aa3/O4O9"


def _q(a, k):
    return next(q.point for q in a.quantities if q.key == k)


def tier_error(y1, y10, y100):
    """One solve's error estimate at rtol from three tiers (rtol, /10, /100; o9-forward-member-note amendment 2, 68's
    measurement): where the tiers converge monotonically with per-decade ratio ρ = (y1−y10)/(y10−y100) > 1, the
    geometric tail e = |y1−y10|·ρ/(ρ−1); otherwise (non-monotone, ρ ≤ 1, or an exact repeat) the largest span
    max(|y1−y10|, |y1−y100|). Absolute, in y's units."""
    d1, d2 = y1 - y10, y10 - y100
    if d2 != 0.0 and d1 / d2 > 1.0:
        rho = d1 / d2
        return abs(d1) * rho / (rho - 1.0)
    return max(abs(d1), abs(y1 - y100))


#: Each solve's e/|y| above this is «resolution not measured», and the test fails naming it (68 B1 on amendment 2): near
#: ρ = 1 the geometric tail ρ/(ρ−1) grows without limit, so a key whose tiers barely converge would pass against any
#: miss. 1e-7 is the closure-noise level solve.py names for rtol 1e-10 (the note-8 retry comment, «~1e-7»); today's
#: largest per-solve e/|y| is 2.73e-8 (Mars cmb_temperature, inverse).
E_CEILING = 1e-7


def identity_bound(y, inv, fwd):
    """(bound, None) for one key from the inverse's and the forward's three tiers, or (None, why) when either solve's
    e/|y| is over E_CEILING (its ρ named)."""
    out = 0.0
    for name, t in (("inverse", inv), ("forward", fwd)):
        e = tier_error(*t) / y
        if e > E_CEILING:
            d1, d2 = t[0] - t[1], t[1] - t[2]
            rho = d1 / d2 if d2 != 0.0 else float("inf")
            return None, f"{name} e/|y| {e:.3e} over the ceiling {E_CEILING:g} (ρ {rho:.6g}): resolution not measured"
        out += e
    return max(1e-8, out), None


class Identity(unittest.TestCase):
    """At the declared T_pot the member is the declared answer again: R, CMF and the located boundaries within the two
    solves' measured resolution. Venus (boundary_mass) and Mars (S, radius-declared core and basal) each exercise one
    closure kind. Bound per key (o9-forward-member-note amendment 2, replacing amendment 1's one-decade r):
    max(1e-8, (e_inverse + e_forward)/|y|), each e the solve's three-tier error at rtol (`tier_error`) measured here on
    this machine; a solve with e/|y| over E_CEILING fails by name (resolution not measured, 68 B1). Amendment 1's r = |y(rtol) − y(rtol/10)| understates the error when the per-decade ratio is near 1
    (Mars inverse ρ 1.6–2.4) and does not measure a non-monotone forward solve (68, 10-16)."""

    def _check(self, stem, keys):
        body, _ = from_v1.load_v1(f"engine/bodies/{stem}.yaml")
        o10 = dataclasses.replace(OPT, rtol=OPT.rtol / 10.0)
        o100 = dataclasses.replace(OPT, rtol=OPT.rtol / 100.0)
        a, x = sv.solve(body, OPT)
        a10, _ = sv.solve(body, o10)
        a100, _ = sv.solve(body, o100)
        fb = mb.forward_member(body, a, x)
        self.assertEqual(fb.closure.kind, "R")
        f, _ = sv.solve(fb, OPT)
        f10, _ = sv.solve(fb, o10)
        f100, _ = sv.solve(fb, o100)
        self.assertIsInstance(f, result.Answer, getattr(f, "text", None))
        for k in keys:
            y = abs(_q(a, k))
            bound, why = identity_bound(y, (_q(a, k), _q(a10, k), _q(a100, k)), (_q(f, k), _q(f10, k), _q(f100, k)))
            self.assertIsNone(why, f"{stem} {k}: {why}")
            self.assertLessEqual(abs(_q(f, k) - _q(a, k)) / y, bound, k)

    def test_tier_error(self):
        """The two branches: a geometric tail where the tiers converge (ρ = 2 doubles the one-decade span), the largest
        span where they do not (a sign change, or ρ ≤ 1)."""
        self.assertAlmostEqual(tier_error(1.0 + 4e-8, 1.0 + 2e-8, 1.0 + 1e-8), 2e-8 * 2.0, delta=1e-15)
        self.assertAlmostEqual(tier_error(1.0 + 1e-8, 1.0 - 3e-8, 1.0 + 2e-8), 4e-8, delta=1e-15)
        self.assertAlmostEqual(tier_error(1.0 + 1e-8, 1.0, 1.0 - 2e-8), 3e-8, delta=1e-15)
        self.assertEqual(tier_error(2.0, 2.0, 2.0), 0.0)
        self.assertAlmostEqual(tier_error(2.01e-9, 1e-9, 0.0), 1.01e-9 * 101.0, delta=1e-18)   # ρ 1.01: ×101

    def test_ceiling_fails_not_passes(self):
        """68 B1: a solve whose tiers barely converge (ρ 1.01, e/|y| ≈ 1e-6) is over the ceiling — the key fails by
        name instead of passing against any miss; under it the bound is the sum, floored at 1e-8."""
        bound, why = identity_bound(1.0, (2.01e-8, 1e-8, 0.0), (0.0, 0.0, 0.0))
        self.assertIsNone(bound)
        self.assertIn("inverse", why)
        self.assertIn("ρ 1.01", why)
        bound, why = identity_bound(1.0, (4e-8, 2e-8, 1e-8), (0.0, 0.0, 0.0))
        self.assertIsNone(why)
        self.assertAlmostEqual(bound, 4e-8, delta=1e-20)
        self.assertEqual(identity_bound(1.0, (1.0, 1.0, 1.0), (1.0, 1.0, 1.0)), (1e-8, None))

    def test_venus(self):
        self._check("venus", ("radius", "core_mass_fraction", "core_radius", "nmoi", "cmb_temperature"))

    def test_mars(self):
        self._check("mars", ("radius", "core_mass_fraction", "core_radius", "nmoi", "cmb_temperature"))


class OldMember(unittest.TestCase):
    """Venus at its hottest O9 point: the member's radius sits on the old O4O9 entry-A radius (the old s0 is the
    declared composition), measured 7.7e-6 at 3188.87 K. Control: the inverse solve at the same T_pot keeps R at the
    declared value, about 6 % from the old member (at 1723 K the two are only 1.4e-3 apart, too close for a control).
    Switch-over step 2: the old engine carries legacy's fe_prem constants, so the like-for-like member reads fe_prem with
    both put back (test_switchover.Step2PutBack); the shipped record moves the radius (measured 4.3e-3)."""

    T = 3188.87

    @unittest.skipUnless(O4O9.exists(), "artifacts capture not beside the worktree")
    def test_venus_point(self):
        old = next(p for p in json.loads((O4O9 / "venus.json").read_text())["points"]
                   if p.get("entry", "").startswith("A ") and p["t_pot"] == self.T)["values"]["radius"] * 6.371e6
        from solver.tests.test_switchover import Step2PutBack
        reg = Step2PutBack._registry("W-L1-01", "P5-F1")
        body, _ = from_v1.load_v1("engine/bodies/venus.yaml")
        fb, _info = mb.member_of(body, registry=reg)
        f, _ = sv.solve(dataclasses.replace(fb, surface=dataclasses.replace(fb.surface, t_pot=self.T)), OPT, registry=reg)
        self.assertLess(abs(_q(f, "radius") - old) / old, 2e-5)
        inv, _ = sv.solve(dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=self.T)), OPT,
                          registry=reg)
        self.assertGreater(abs(_q(inv, "radius") - old) / old, 0.04)
        fs, _info = mb.member_of(body)
        shipped, _ = sv.solve(dataclasses.replace(fs, surface=dataclasses.replace(fs.surface, t_pot=self.T)), OPT)
        self.assertGreater(abs(_q(shipped, "radius") - old) / old, 1e-3)


class ForwardUntouched(unittest.TestCase):
    def test_earth_has_no_member(self):
        body, _ = from_v1.load_v1("engine/bodies/earth.yaml")
        self.assertIsNone(mb.member_of(body))

    def test_run_oracle_records_the_member(self):
        rec = ro.one("engine/bodies/venus.yaml", 1723.2542652588522, OPT, chain=False)
        self.assertEqual(rec["outcome_kind"], "answer")
        self.assertEqual(rec["member"]["closure"], "boundary_mass")
        self.assertIn("core", rec["member"]["fractions"])


if __name__ == "__main__":
    unittest.main()
