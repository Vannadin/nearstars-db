# 물질 기록 스키마 시험 — 스키마가 읽히고, 설계 D-M1 · D-M2 · 주석 1 의 칸이 빠짐없이 있는지 목록 대조 (phase-2 등록 P1)
"""P1 acceptance of rewrite/phase2-impl.frozen.md: the material schema loads, and every field that design D-M1, D-M2,
D-P1, D-P3 and post-freeze note 1 item 3 ask for is present (and required where they say «carries»).

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_material_schema
"""
import unittest
from collections.abc import Mapping
from pathlib import Path

from solver import yamlio

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "materials" / "schema.yaml"

# What the frozen texts ask for, as (section, key path, must be required). Written from the design text, not from
# the schema, so a key dropped from the schema fails here.
DEMANDS = (
    # D-M1 identity, including the C58 field «now required»
    ("D-M1", "record.id", True), ("D-M1", "record.label", True), ("D-M1", "record.system", True),
    ("D-M1", "record.fit_composition", True), ("D-M1", "record.phases", True),
    # D-M1 phases: EOS form, parameters with units, reference state (a path allowed, r2 N5)
    ("D-M1", "phase.eos", True), ("D-M1", "eos.form", True), ("D-M1", "eos.params", False),
    ("D-M1", "eos.reference", True), ("D-M1", "reference.kind", True), ("D-M1", "reference.path", False),
    # thermal block with a source state and a source composition
    ("D-M1", "phase.thermal", True), ("D-M1", "thermal.source_state", True),
    ("D-M1", "thermal.source_composition", True),
    # stability field as data, every phase (D-M2, r2 B6), with «declared» and its reason
    ("D-M2", "phase.field", True), ("D-M2", "field.kind", True), ("D-M2", "field.reason", False),
    ("D-M2", "field.source", False),
    # EOS validity window; out-of-range behaviour per edge: refusal or band
    ("D-M1", "phase.window", True), ("D-M1", "phase.edges", True), ("D-M2", "edge.refusal", False),
    ("D-M2", "edge.band", False),
    # a band states its error's origin (r2 N10)
    ("D-M2", "band.origin", True), ("D-M2", "band.error", True), ("D-M2", "band.grade", True),
    # γ has its own window
    ("D-M2", "thermal.gamma_window", True),
    # provenance per constant: source, page/table/equation, printed units and conversion, grade
    ("D-M1", "constant.source", True), ("D-M1", "constant.grade", True), ("D-M1", "constant.printed", False),
    ("D-M1", "constant.conversion", False), ("D-M1", "constant.unit", True),
    ("note 1.3", "source.cache", False), ("note 1.3", "source.page", False), ("note 1.3", "source.where", False),
    ("note 1.3", "source.sha256", False), ("note 1.3", "source.library", False), ("note 1.3", "source.doi", False),
    ("note 1.3", "source.cites", False), ("note 1.3", "source.abstract_only", False),
    # one formula check: printed quantity, its state, expected as printed, tolerance with reason, expression
    ("D-M1", "record.formula_checks", True), ("D-M1", "formula_check.quantity", True),
    ("D-M1", "formula_check.state", True), ("D-M1", "formula_check.expected", True),
    ("D-M1", "formula_check.tolerance", True), ("D-M1", "formula_check.tolerance_reason", True),
    ("D-M1", "formula_check.expression", True), ("D-M1", "formula_check.source", True),
    # D-P1 kinds and D-P3 boundary kinds; hand-over joins with bands
    ("D-P1", "record.kind", True), ("D-P1", "record.boundaries", False), ("D-P1", "record.joins", False),
    ("D-P3", "boundary.kind", True), ("D-P3", "boundary.curve", True), ("D-P1", "join.band", True),
    # impl P6: hand-over band sampling declared before measuring; library pin (owner db20e171 (b))
    ("impl P6", "band.sampling", False), ("impl note 1.6", "library.version", True),
    ("impl note 1.6", "library.sha256", True),
)


def unmet(schema) -> list:
    """The demands the schema does not meet: (key, why)."""
    out = []
    for sec, path, required in DEMANDS:
        part, key = path.split(".")
        spec = (schema.get(part) or {}).get(key)
        if spec is None:
            out.append((path, f"missing ({sec})"))
        elif bool(spec.get("required")) != required:
            out.append((path, f"required should be {required} ({sec})"))
    return out


def dangling(schema) -> list:
    """Each `of:` must name a section of the schema, so no key points at nothing."""
    return [f"{sec}.{k} of: {spec['of']}" for sec, keys in schema.items() if isinstance(keys, Mapping)
            for k, spec in keys.items() if isinstance(spec, Mapping) and "of" in spec and spec["of"] not in schema]


class MaterialSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = yamlio.load_data(SCHEMA_PATH)

    def test_every_demanded_field_present(self):
        self.assertEqual(unmet(self.s), [])

    def test_kinds_and_forms(self):
        self.assertEqual(tuple(self.s["record"]["kind"]["values"]), ("single", "branched", "assemblage", "hand_over"))
        self.assertEqual(tuple(self.s["kinds"]), tuple(self.s["record"]["kind"]["values"]))
        self.assertEqual(tuple(self.s["boundary"]["kind"]["values"]), ("solid_solid", "melting"))
        # bme4 is not built until a cached source prints its formula (impl P3)
        self.assertNotIn("bme4", self.s["eos"]["form"]["values"])

    def test_every_record_reference_resolves(self):
        self.assertGreater(sum(1 for keys in self.s.values() if isinstance(keys, Mapping)
                               for spec in keys.values() if isinstance(spec, Mapping) and "of" in spec), 20)
        self.assertEqual(dangling(self.s), [])

    def test_controls(self):
        """Negative controls: a dropped demanded key, a flipped required flag, and a dangling `of:` are each caught."""
        def thawed():
            return {sec: ({k: dict(v) if isinstance(v, Mapping) else v for k, v in keys.items()}
                          if isinstance(keys, Mapping) else keys) for sec, keys in self.s.items()}
        s = thawed(); del s["band"]["origin"]
        self.assertEqual(unmet(s), [("band.origin", "missing (D-M2)")])
        s = thawed(); s["phase"]["field"]["required"] = False
        self.assertEqual(unmet(s), [("phase.field", "required should be True (D-M2)")])
        s = thawed(); s["phase"]["thermal"]["of"] = "thermals"
        self.assertEqual(dangling(s), ["phase.thermal of: thermals"])


if __name__ == "__main__":
    unittest.main()
