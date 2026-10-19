# 노드용 솔버 추가분(C1)이 순수 추가인지 — solve_id 를 뺀 풀이 결과 동일성과 거절 사전 동일성 (prereg-t-eq-stellar N1·N2)
"""Registration `rewrite/nodes/prereg-t-eq-stellar.frozen.md` (artifacts, blob 9e9f08ae), acceptance N1 and N2.

C1 adds to solver/ only: METHODS += read, chosen; a `_NODE` refusal tuple; NODE_ITERATE_PASSES. These tests prove
nothing existing changed.

N1 (moved to nodes/landing/n1_identity.py, a one-time landing proof outside the suite; audit 68 L1): solve() on
Earth (T_pot 1700 K), Mars and Venus, as `plain((ans, warm))` with every `solve_id` removed, hashes
to the values captured at C1's parent. solve_id itself must move (it hashes every solver/*.py, 707aa7a4), so it is
dropped, as in the silicate switch-off identity. Planted controls: a 1-ulp change must fail, a solve_id-only
change must pass.

N2: every refusal entry of C1's parent is unchanged and renders the same text; the registries grew by exactly the
node ids and the one budget.

Capture (run at C1's parent, before the edit):
    solver/.venv/bin/python -m solver.tests.test_node_additive capture
Run (N2 only; the hashes and helpers stay here because the landing proof and `capture` use them):
    solver/.venv/bin/python -m unittest solver.tests.test_node_additive
"""
import dataclasses
import hashlib
import json
import math
import sys
import unittest

#: C1's parent, where the hashes below were captured.
PARENT = "b0a17107"
#: sha256 of canonical(plain((ans, warm)) without solve_id), captured at PARENT.
CAPTURED = {
    "earth_1700": "71c8bdd08452b72ab3ce1aa97eadff2b19362645ba090d7632d926ab0f2b907c",
    "mars": "716ea6f2906a339635df54e5c6e0069694f1ae9037a6e5300aeb616cc9bd2a7b",
    "venus": "2867f4d10c4e10bafc42072f5e25d0e35be3ea3a978fdd562c3125beefffaa7e",
}
#: The registry ids at PARENT (N2), captured with the hashes.
PARENT_IDS = ["input.bad_grade",
              "input.class_out_of_scope",
              "input.closure_count",
              "input.composition_component",
              "input.composition_fraction",
              "input.composition_missing",
              "input.composition_sum",
              "input.composition_system",
              "input.composition_undeclared",
              "input.composition_window",
              "input.cross_field",
              "input.declared_grade_not_wired",
              "input.deviation",
              "input.duplicate_key",
              "input.duplicate_layer_id",
              "input.duplicate_name",
              "input.empty",
              "input.extent_invalid",
              "input.extent_order",
              "input.extent_overdetermined",
              "input.jump_at_lithosphere",
              "input.jump_boundary",
              "input.layer_order",
              "input.mass_fraction_sum",
              "input.material_record_unavailable",
              "input.material_registry",
              "input.missing_key",
              "input.non_finite",
              "input.not_boolean",
              "input.not_in_vocabulary",
              "input.not_mapping",
              "input.not_number",
              "input.not_text",
              "input.null_value",
              "input.out_of_domain",
              "input.param_not_for_material",
              "input.provenance_missing",
              "input.role_material_class",
              "input.source_kind",
              "input.source_kind_not_built",
              "input.thickness_above_pattern",
              "input.unit_mismatch",
              "input.unknown_key",
              "input.unknown_material",
              "input.unknown_role",
              "input.unreadable",
              "input.v1_unmapped",
              "input.value_missing",
              "input.zero_extent",
              "solve.basal_not_attached",
              "solve.basal_unconverged",
              "solve.closure_discontinuous",
              "solve.event_chatter",
              "solve.event_undefined",
              "solve.layer_order",
              "solve.lid_unconverged",
              "solve.material_domain",
              "solve.material_record",
              "solve.melting_not_in_phase2",
              "solve.no_bracket",
              "solve.non_finite",
              "solve.two_roots",
              "solve.unlocated_discontinuity"]
PARENT_NO_ANSWER_IDS = ["span_too_long", "unconverged"]
PARENT_BUDGETS = ["CLOSE_ITERS", "MAX_STEPS_SOLVE", "WALL_SHOTS", "MAX_SPLITS"]
NODE_IDS = ("node.out_of_domain", "node.input_missing", "node.source_not_cached", "node.undeclared_read",
            "node.record_not_measured", "node.fiction_in_measured_db")   # sixth: prereg-orbit-adopted D1
#: Solver ids added after C1 (b0a17107), one line each with the commit that added it; C1's PARENT_IDS stay pinned.
ADDED_AFTER_C1 = {"input.no_table_for_composition": "silicate step 4 aa48d1bf",
                  "core_fold_off_domain": "core-tc-fold C4 (engine/tc-fold-c8)",
                  "core_fold_states": "core-tc-fold C4 (engine/tc-fold-c8)",
                  "solve.frozen_band_trapped": "s-read post-freeze note 3 §2.4 (engine ea-sA-note3)"}
#: NoAnswer reasons added after C1, the same way; C1's PARENT_NO_ANSWER_IDS stay pinned.
ADDED_NO_ANSWER_AFTER_C1 = {"core_fold_budget": "core-tc-fold C4 (engine/tc-fold-c8)"}


def _drop_solve_id(x):
    if isinstance(x, dict):
        return {k: _drop_solve_id(v) for k, v in x.items() if k != "solve_id"}
    if isinstance(x, list):
        return [_drop_solve_id(v) for v in x]
    return x


def _digest(plain_obj) -> str:
    text = json.dumps(_drop_solve_id(plain_obj), sort_keys=True, ensure_ascii=False, allow_nan=False,
                      separators=(",", ":"))
    return hashlib.sha256(text.encode()).hexdigest()


def _solve_plain(name):
    from solver import from_v1, result, solve as sv
    path = {"earth_1700": "engine/bodies/earth.yaml", "mars": "engine/bodies/mars.yaml",
            "venus": "engine/bodies/venus.yaml"}[name]
    body, _aside = from_v1.load_v1(path)
    if name == "earth_1700":
        body = dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=1700.0))
    ans, warm = sv.solve(body)
    return result.plain((ans, warm))


def _render_all(registry):
    """One fixed evidence set per entry: every field set to its own name (rendering only, no vocab check)."""
    from solver import refusals as rf
    out = {}
    for rid, e in registry.items():
        ev = {f: f for f in e.fields + e.optional}
        out[rid] = (e.fields, e.optional, e.template, e.preamble, e.solve, rf.render(e, "where", ev))
    return out


def capture():
    from solver import refusals as rf
    hashes = {n: _digest(_solve_plain(n)) for n in CAPTURED}
    render = hashlib.sha256(repr(sorted(_render_all(rf.REGISTRY).items())).encode()).hexdigest()
    print(json.dumps({"hashes": hashes, "ids": sorted(rf.REGISTRY), "no_answer_ids": sorted(rf.NO_ANSWER_REGISTRY),
                      "budgets": list(rf.NO_ANSWER_BUDGETS), "render": render}, indent=1))


class N2Registry(unittest.TestCase):
    def test_parent_entries_unchanged(self):
        from solver import refusals as rf
        parent, node, added = set(PARENT_IDS), set(NODE_IDS), set(ADDED_AFTER_C1)
        self.assertEqual(set(rf.REGISTRY), parent | node | added)     # C1's pins, plus each later id by name
        self.assertFalse(parent & node or parent & added or node & added)
        self.assertEqual(sorted(rf.NO_ANSWER_REGISTRY), sorted(PARENT_NO_ANSWER_IDS + list(ADDED_NO_ANSWER_AFTER_C1)))
        self.assertEqual(list(rf.NO_ANSWER_BUDGETS), PARENT_BUDGETS + ["NODE_ITERATE_PASSES"])
        parent_only = {k: v for k, v in rf.REGISTRY.items() if k in PARENT_IDS}
        render = hashlib.sha256(repr(sorted(_render_all(parent_only).items())).encode()).hexdigest()
        self.assertEqual(render, PARENT_RENDER)

    def test_methods_appended(self):
        from solver import result
        self.assertEqual(result.METHODS, ("direct", "interpolated", "bridged", "derived", "read", "chosen"))


PARENT_RENDER = "d75c56444d4f9109e8e1fece0e524bfa6b623b08e1ce5e47affacb05817e615e"

if __name__ == "__main__":
    if sys.argv[1:] == ["capture"]:
        capture()
    else:
        unittest.main()
