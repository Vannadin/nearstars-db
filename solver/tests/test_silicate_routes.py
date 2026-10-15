# 규산염 기록 경로 시험 — silicate_records 스위치 하나가 모든 경로를 켜고 끔, 조성 지문 맞춤·불일치 거절, 경계 미정 표는 개발 때만, solve_id 묶음 (규산염 기록 등록 §4)
"""Tests of the silicate routes (rewrite/phase2-silicate-record-registration.frozen.md §4; 68 S1, S3; §7 item 10).
Records are synthetic and live in a temporary directory; the roster bodies are the shipped body files.

Run from the worktree root:  <solver venv>/python -m unittest solver.tests.test_silicate_routes
"""
import dataclasses
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import yaml

from solver import context, from_v1, legacy_materials as lm, material_registry as mr, refusals, result
from solver import material_assemblage as ma
from solver import solve as sv
from solver.tests import test_material_assemblage as T

ROOT = Path(__file__).resolve().parents[2]
ROSTER = ("earth", "venus", "mars", "pandora", "dante_fixture")
MARS_KEY = "19e84b63bac74c9a"


def body(name):
    got = from_v1.load_v1(str(ROOT / "engine/bodies" / f"{name}.yaml"))
    return got[0] if isinstance(got, tuple) else got


def registry(d, keys=(("silicate_slb_default_bse", "14f8758a7681f418"), ("silicate_slb_mars_khan2022", MARS_KEY)),
             status="pinned", allow_development=False):
    """A registry holding the shipped records plus synthetic assemblage records under the given ids and keys."""
    for f in mr.MATERIALS_DIR.glob("*.yaml"):
        if f.name not in mr.NOT_RECORDS:
            (Path(d) / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
    (Path(d) / "sources.yaml").write_text((mr.MATERIALS_DIR / "sources.yaml").read_text(encoding="utf-8"),
                                          encoding="utf-8")
    (Path(d) / "tables").mkdir(exist_ok=True)
    tb = T.table()
    body_ = (json.dumps(tb, sort_keys=True, separators=(",", ":")) + "\n").encode()
    for rid, key in keys:
        (Path(d) / "tables" / f"{rid}.json").write_bytes(body_)
        rec = T.record(hashlib.sha256(body_).hexdigest(), status)
        rec.update(id=rid, composition_key=key)
        rec["assemblage"]["file"] = f"tables/{rid}.json"
        (Path(d) / f"{rid}.yaml").write_text(yaml.safe_dump(rec, sort_keys=False), encoding="utf-8")
    got = mr.load(Path(d), allow_development=allow_development)
    assert isinstance(got, mr.Registry), got
    return got


def kinds(views):
    return {lid: (type(v).__name__, getattr(v, "material_id", None)) for lid, v in views.items()}


class Switch(unittest.TestCase):
    def test_off_is_today(self):
        """§4: with the switch off every layer of every roster body resolves exactly as today; no silicate route is
        consulted, even one planted in SILICATE_ROUTES (a fifth route not under the flag fails this)."""
        today = mr.load()                                   # the shipped records, no assemblage record among them
        with tempfile.TemporaryDirectory() as d:
            reg = registry(d, allow_development=True)
            real, planted = sv._silicate_route, dict(sv.SILICATE_ROUTES)
            try:
                sv._silicate_route = lambda *a, **k: (_ for _ in ()).throw(AssertionError("route consulted"))
                sv.SILICATE_ROUTES = {**planted, "silicate_basal_const": "silicate_slb_default_bse"}
                for name in ROSTER:
                    b = body(name)
                    with self.subTest(body=name):
                        off = sv._views(b, registry=reg, silicate=False)
                        base = sv._views(b, registry=today)
                        self.assertEqual(kinds(off) if isinstance(off, dict) else off,
                                         kinds(base) if isinstance(base, dict) else base)
            finally:
                sv._silicate_route, sv.SILICATE_ROUTES = real, planted

    def test_on_routes(self):
        """§4's table: Earth's mantle and lid and Venus read default_bse; Mars's mantle reads its record by key, its
        basal layer stays legacy (Q6 not built); Dante stays legacy (Q5)."""
        with tempfile.TemporaryDirectory() as d:
            reg = registry(d, allow_development=True)
            for name, want in (("earth", "silicate_slb_default_bse"), ("venus", "silicate_slb_default_bse"),
                               ("pandora", "silicate_slb_default_bse"), ("mars", "silicate_slb_mars_khan2022")):
                b = body(name)
                views = sv._views(b, registry=reg, silicate=True)
                with self.subTest(body=name):
                    self.assertIsInstance(views, dict)
                    sil = [l for l in b.layers if l.material in ("silicate", "silicate_decl")]
                    self.assertTrue(sil)
                    for l in sil:
                        self.assertIsInstance(views[l.id], ma.AssemblageView)
                        self.assertEqual(views[l.id].material_id, want)
                    for l in b.layers:
                        if l.material == lm.BASAL_CONST:
                            self.assertIsInstance(views[l.id], lm.LegacyView)
            b = body("dante_fixture")
            on = sv._views(b, registry=reg, silicate=True)
            self.assertEqual(kinds(on), kinds(sv._views(b, registry=None)))

    def test_boundaries_pending_refused_outside_development(self):
        """68 S3: an assemblage record with pending boundaries is not read unless the registry is a development one."""
        with tempfile.TemporaryDirectory() as d:
            reg = registry(d)
            got = sv._views(body("earth"), registry=reg, silicate=True)
        self.assertIsInstance(got, result.Refusal)
        self.assertEqual(got.id, "input.cross_field")
        self.assertEqual(got.evidence["rule"], "record_boundaries_pending")

    def test_composition_key_misses(self):
        """§4, §7 item 10 at the resolver: a silicate_decl layer whose fingerprint has no record refuses by name,
        naming the key and the built keys; one changed oxide misses."""
        with tempfile.TemporaryDirectory() as d:
            reg = registry(d, allow_development=True)
            b = body("mars")
            layers = []
            for l in b.layers:
                if l.material == lm.BASAL_CONST:       # it stays legacy and would refuse first on the moved oxides
                    continue
                if l.material == "silicate_decl":
                    v = dict(l.composition.value)
                    v["MgO"] += 0.01
                    l = dataclasses.replace(l, composition=dataclasses.replace(l.composition, value=v))
                layers.append(l)
            got = sv._views(dataclasses.replace(b, layers=tuple(layers)), registry=reg, silicate=True)
        self.assertIsInstance(got, result.Refusal)
        self.assertEqual(got.id, "input.no_table_for_composition")
        self.assertNotEqual(got.evidence["composition_key"], MARS_KEY)
        self.assertIn(MARS_KEY, got.evidence["built_keys"])
        self.assertIn("input.no_table_for_composition", refusals.REGISTRY)


class SolveId(unittest.TestCase):
    def test_option_and_table_bind_solve_id(self):
        """The Option enters solve_id (§4); the view's record carries the compact sha, so a changed table moves the
        material bytes (68 S1), and two loads give one id."""
        b = body("earth")
        canon = {"x": 1}
        self.assertNotEqual(context.solve_id_of(canon, b"m", context.Options()),
                            context.solve_id_of(canon, b"m", context.Options(silicate_records=True)))
        ids = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as d:
                reg = registry(d, allow_development=True)
                ids.append(sv._material_bytes(sv._views(b, registry=reg, silicate=True)))
        self.assertEqual(ids[0], ids[1])
        with tempfile.TemporaryDirectory() as d:
            reg = registry(d, allow_development=True)
            views = sv._views(b, registry=reg, silicate=True)
            lid = next(l.id for l in b.layers if l.material == "silicate")
            rec = dict(result.plain(views[lid].record))
            rec["assemblage"] = {**rec["assemblage"], "sha256": "f" * 64}
            moved = {**views, lid: ma.view(rec, reg.tables[views[lid].material_id], 1600.0)}
            self.assertNotEqual(sv._material_bytes(moved), ids[0])


if __name__ == "__main__":
    unittest.main()
