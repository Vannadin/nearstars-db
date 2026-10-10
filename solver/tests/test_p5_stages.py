# fe_prem 단계 (a)·(b) — 지구 받아들인 사격의 핵 경로 노드에서, 옮긴 상수를 되돌린 기록 뷰가 옛 LegacyView 와 비트까지 같고, 출하 기록의 차이는 이름 붙은 결함 둘로만 갈린다 (phase-2 impl P5 · note 1 §3–§5)
"""P5 stages (a) and (b) (rewrite/phase2-impl.frozen.md P5, impl note 1 §3–§5), on the nodes note 1 §3 names: the
(P, T) at which Earth's accepted pass asks the core layer's fe_prem view (LegacyView), recorded from one Earth solve
at its declared state with the sensitivity passes off (the last `solve.inward` call is the accepted pass, as in
test_a6_trace).

(a) The record with the stage-(a) fixtures put back (note 1 §4: W-L1-01 αK_T; P5-F1 Dorogokupets V0) gives the same
    density, dT/dP and state as LegacyView at every node, bit for bit. W-L20-01 takes the legacy treatment in the
    record, so it has no fixture; W-L19-04 is on the history route only.
(b) The record as shipped, at the same nodes: it differs from legacy, and restoring each finding's fixture alone
    leaves only the other's difference, so every difference is named by W-L1-01 or P5-F1. The sizes are reported by
    rewrite/phase2-records/fe_prem_stages.py.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_p5_stages
"""
import unittest
from unittest import mock

from solver import context, from_v1
from solver import legacy_materials as lm
from solver import material_registry as mr
from solver import material_view as mv
from solver import solve as sv
from solver.from_v1 import thaw

import eos  # noqa: E402  (engine/, put on the path by legacy_materials)

#: stage (a) fixtures, by finding (note 1 §4); each is test-only, never a record field
FIXTURES = {
    "W-L1-01": lambda rec: rec["phases"][0]["thermal"]["pressure"].update(alpha_k={"value": 0.00121e9, "unit": "Pa/K"}),
    "P5-F1": lambda rec: rec["phases"][0]["thermal"]["sets"][1]["evaluator"]["params"].update(
        v0={"value": 7.95784e-6, "unit": "m3/mol"}),
}
METHODS = ("density", "dtdp", "state")


def record(*findings):
    rec = thaw(mr.load()["fe_prem"])
    for f in findings:
        FIXTURES[f](rec)
    return rec


def accepted_nodes():
    """(t_pot, sorted unique (P, T)) at which Earth's accepted pass asked the fe_prem view."""
    real_inward, calls, cur, seen = sv.inward, [], [], {}

    def inward(body, views, x, opt):
        cur.clear()
        out = real_inward(body, views, x, opt)
        calls.append(list(cur))
        return out

    def wrap(name):
        real = getattr(lm.LegacyView, name)

        def w(self, *a, **k):
            if self.material_id == "fe_prem":
                cur.append((a[0], a[1]))
                seen["t_pot"] = self.t_pot
            return real(self, *a, **k)
        return w

    body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
    with mock.patch.object(sv, "inward", inward), \
            mock.patch.multiple(lm.LegacyView, **{n: wrap(n) for n in METHODS}):
        sv.solve(body, context.Options(sensitivity_dt=0.0))
    return seen["t_pot"], sorted(set(calls[-1]))


def values(view, nodes):
    out = []
    for p, t in nodes:
        s = view.state(p, t)
        out.append((view.density(p, t), view.dtdp(p, t), (s[0], s[1]) if isinstance(s, tuple) else type(s).__name__))
    return out


class Stages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t_pot, cls.nodes = accepted_nodes()
        cls.legacy = values(lm.LegacyView("fe_prem", eos.FE_PREM, cls.t_pot), cls.nodes)

    def view(self, *findings):
        return values(mv.RecordView(record(*findings), self.t_pot), self.nodes)

    def test_nodes_are_the_core_path(self):
        ps = [p for p, _t in self.nodes]
        self.assertGreater(len(self.nodes), 100)
        self.assertLess(min(ps), 136e9)                                 # from the CMB
        self.assertGreater(max(ps), 350e9)                               # past the printed scope, into the edge band

    def test_stage_a_bit_identical(self):
        got = self.view(*FIXTURES)
        bad = [(n, a, b) for n, a, b in zip(self.nodes, got, self.legacy) if a != b]
        self.assertEqual(bad[:3], [], f"{len(bad)} of {len(self.nodes)} nodes differ")

    def test_stage_b_every_difference_is_named(self):
        shipped = self.view()
        self.assertNotEqual(shipped, self.legacy)                        # control: the corrections move the path
        for f in FIXTURES:                                               # each finding alone leaves a difference
            with self.subTest(restored=f):
                self.assertNotEqual(self.view(f), self.legacy)


if __name__ == "__main__":
    unittest.main()
