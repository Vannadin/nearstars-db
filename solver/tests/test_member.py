# 순방향 표 구성원 시험 — 선언 온도에서 구성원이 선언 답을 되풀이하고, 다른 온도에서 옛 O9 구성원 값에 붙으며, 순방향 천체는 그대로임
"""solver.member (owner-direction «O9 for inverse bodies: compare like for like»; o9-forward-member-note.md)."""
import dataclasses
import json
import unittest
from pathlib import Path

from solver import context, from_v1, member as mb, result, run_oracle as ro, solve as sv

OPT = context.Options(sensitivity_dt=0.0)
O4O9 = Path(__file__).resolve().parents[4] / "NearStars-artifacts/rewrite/oracle/097a8aa3/O4O9"


def _q(a, k):
    return next(q.point for q in a.quantities if q.key == k)


class Identity(unittest.TestCase):
    """At the declared T_pot the member is the declared answer again: R, CMF and the located boundaries to the closure
    tolerance. Venus (boundary_mass) and Mars (S, radius-declared core and basal) each exercise one closure kind."""

    def _check(self, stem, keys):
        body, _ = from_v1.load_v1(f"engine/bodies/{stem}.yaml")
        a, x = sv.solve(body, OPT)
        fb = mb.forward_member(body, a, x)
        self.assertEqual(fb.closure.kind, "R")
        f, _ = sv.solve(fb, OPT)
        self.assertIsInstance(f, result.Answer, getattr(f, "text", None))
        for k in keys:
            self.assertLess(abs(_q(f, k) - _q(a, k)) / abs(_q(a, k)), 1e-8, k)

    def test_venus(self):
        self._check("venus", ("radius", "core_mass_fraction", "core_radius", "nmoi", "cmb_temperature"))

    def test_mars(self):
        self._check("mars", ("radius", "core_mass_fraction", "core_radius", "nmoi", "cmb_temperature"))


class OldMember(unittest.TestCase):
    """Venus at its hottest O9 point: the member's radius sits on the old O4O9 entry-A radius (the old s0 is the
    declared composition), measured 7.7e-6 at 3188.87 K. Control: the inverse solve at the same T_pot keeps R at the
    declared value, about 6 % from the old member (at 1723 K the two are only 1.4e-3 apart, too close for a control)."""

    T = 3188.87

    @unittest.skipUnless(O4O9.exists(), "artifacts capture not beside the worktree")
    def test_venus_point(self):
        old = next(p for p in json.loads((O4O9 / "venus.json").read_text())["points"]
                   if p.get("entry", "").startswith("A ") and p["t_pot"] == self.T)["values"]["radius"] * 6.371e6
        body, _ = from_v1.load_v1("engine/bodies/venus.yaml")
        fb, _info = mb.member_of(body)
        f, _ = sv.solve(dataclasses.replace(fb, surface=dataclasses.replace(fb.surface, t_pot=self.T)), OPT)
        self.assertLess(abs(_q(f, "radius") - old) / old, 2e-5)
        inv, _ = sv.solve(dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=self.T)), OPT)
        self.assertGreater(abs(_q(inv, "radius") - old) / old, 0.04)


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
