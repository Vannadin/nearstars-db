# 옛 핵 노드 연결부 시험 — 지구·금성에서 옛 사슬을 새 구조로 돌리고, 읽힌 키가 등록된 출력 집합과 선언 쪽으로 정확히 갈리는지 (등록 S8)
"""S8 acceptance of rewrite/phase1-a1-impl.frozen.md §3, with its negative control.

Mars is not here yet: its layers need the fe_core_light / silicate_decl builders, which land with Mars (S10).
Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_legacy_view
"""
import unittest

from solver import from_v1, legacy_view as lv, result, solve as sv

REGISTERED_OUTPUTS = {"core_radius", "cmb_pressure", "cmb_temperature", "core_pressure", "core_temperature", "radius",
                      "converged", "core_mass_fraction", "ice_mass_fraction"}


def _run(stem, **kw):
    body, _ = from_v1.load_v1(f"engine/bodies/{stem}.yaml")
    ans, _w = sv.solve(body)
    assert isinstance(ans, result.Answer), getattr(ans, "text", ans)
    return ans, lv.run_chain(f"engine/bodies/{stem}.yaml", ans, **kw)


class CorelessCmf(unittest.TestCase):
    """Directing 2026-10-10 «Dante internal_heat_nontidal verdict»: a body with no core_mass_fraction in its Answer
    injects none (as the old interior_layers did), so internal_heat_nontidal declines by the old reason. Control:
    Venus declares no CMF either but infers one; it is injected and the node answers, as at 097a8aa3 (O1)."""

    def test_dante_ihn_declines(self):
        ans, chain = _run("dante_fixture")
        self.assertNotIn("core_mass_fraction", chain.injected.values)
        r = chain.body.results["internal_heat_nontidal"]
        self.assertFalse(r.applicable)
        self.assertIn("core_mass_fraction 이 선언되지 않아", r.reason)

    def test_control_venus_inferred_cmf_answers(self):
        ans, chain = _run("venus")
        self.assertNotIn("core_mass_fraction", chain.declared_keys)
        self.assertIn("core_mass_fraction", chain.injected.values)
        self.assertTrue(chain.body.results["internal_heat_nontidal"].applicable)


class Earth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ans, cls.chain = _run("earth")
        cls.reads = lv.reads(cls.chain)

    def test_core_nodes_run_on_the_new_structure(self):
        for node in lv.IN_SCOPE_READERS:
            r = self.chain.body.results.get(node)
            self.assertIsNotNone(r, node)
            self.assertTrue(r.applicable, (node, r.reason))

    def test_output_reads_are_the_registered_set(self):
        outs = set().union(*(d["outputs"] for d in self.reads.values()))
        self.assertTrue(outs <= REGISTERED_OUTPUTS, outs - REGISTERED_OUTPUTS)
        self.assertTrue({"core_radius", "cmb_pressure", "cmb_temperature", "radius"} <= outs)

    def test_declared_reads_are_declarations(self):
        decl = set().union(*(d["declared"] for d in self.reads.values()))
        self.assertTrue(decl <= set(self.chain.body.inputs), decl - set(self.chain.body.inputs))

    def test_check_reads_clean(self):
        self.assertEqual(lv.check_reads(self.chain), [])

    def test_control_structure_key_from_declared_fails(self):
        """r2 S8-2: the declared-side rule can fail — core_radius served as an input is caught."""
        bad = lv.run_chain("engine/bodies/earth.yaml", self.ans, serve_from_declared=("core_radius",))
        self.assertIn("structure key served from the declared side", [v[2] for v in lv.check_reads(bad)])


class Venus(unittest.TestCase):
    """The inverse body: CMF is the solver's, so it must be read from the outputs side and equal the rewrite's."""

    @classmethod
    def setUpClass(cls):
        cls.ans, cls.chain = _run("venus")
        cls.reads = lv.reads(cls.chain)

    def test_cmf_read_from_outputs(self):
        readers = [n for n, d in self.reads.items() if "core_mass_fraction" in d["outputs"]]
        self.assertTrue(readers)
        for d in self.reads.values():
            self.assertNotIn("core_mass_fraction", d["declared"])
        cmf = next(q.point for q in self.ans.quantities if q.key == "core_mass_fraction")
        self.assertEqual(self.chain.body.get("core_mass_fraction"), cmf)

    def test_control_cmf_served_as_declared_is_caught(self):
        _ans, bad = _run("venus", serve_cmf_from_declared=True)
        r = lv.reads(bad)
        self.assertTrue(any("core_mass_fraction" in d["declared"] for d in r.values()))
        self.assertIn("structure key served from the declared side", [v[2] for v in lv.check_reads(bad)])

    def test_check_reads_clean(self):
        self.assertEqual(lv.check_reads(self.chain), [])


if __name__ == "__main__":
    unittest.main()
