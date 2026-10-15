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
from solver import material_view as mv
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
        rec.update(id=rid, composition_key=key, requires_switch="silicate_records")
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
        basal layer the basal record (Q6); Dante stays legacy (Q5)."""
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
                        if l.material == lm.BASAL_CONST:              # Q6: the basal record over the mantle's view
                            self.assertIsInstance(views[l.id], ma.BasalView)
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


def with_layer(b, lid, **over):
    return dataclasses.replace(b, layers=tuple(dataclasses.replace(l, **over) if l.id == lid else l for l in b.layers))


def closure_on(b, lid, name):
    return dataclasses.replace(b, closure=dataclasses.replace(b.closure, kind="composition", layer=lid, name=name,
                                                              lo=0.1, hi=0.9))


class Routes(unittest.TestCase):
    """68 B1, B3 on aa48d1bf: one test per route guard."""

    def test_closure_axis_refused_as_legacy(self):
        """B1 / R13: a closure axis on a routed layer refuses exactly as legacy does, switched on or off."""
        with tempfile.TemporaryDirectory() as d:
            reg = registry(d, allow_development=True)
            for name, lid, axis in (("earth", "mantle", "mg_number"), ("mars", "mantle", "fe_number")):
                b = closure_on(body(name), lid, axis)
                layer = next(l for l in b.layers if l.id == lid)
                off = sv._view_for(b, layer, 0.5, 0.0, reg, False)
                on = sv._view_for(b, layer, 0.5, 0.0, reg, True)
                with self.subTest(body=name):
                    self.assertIsNone(on[0])
                    self.assertEqual(on, off)
                    self.assertEqual(on[1][0], "closure_axis")

    def test_one_record_per_composition(self):
        """R4: two assemblage records with one composition key STOP at load."""
        with tempfile.TemporaryDirectory() as d:
            for f in mr.MATERIALS_DIR.glob("*.yaml"):
                if f.name not in mr.NOT_RECORDS:
                    (Path(d) / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
            (Path(d) / "sources.yaml").write_text((mr.MATERIALS_DIR / "sources.yaml").read_text(encoding="utf-8"),
                                                  encoding="utf-8")
            (Path(d) / "tables").mkdir()
            tb = T.table()
            raw = (json.dumps(tb, sort_keys=True, separators=(",", ":")) + "\n").encode()
            for rid in ("silicate_slb_a", "silicate_slb_b"):
                (Path(d) / "tables" / f"{rid}.json").write_bytes(raw)
                rec = T.record(hashlib.sha256(raw).hexdigest(), "pinned")
                rec.update(id=rid, composition_key=MARS_KEY)
                rec["assemblage"]["file"] = f"tables/{rid}.json"
                (Path(d) / f"{rid}.yaml").write_text(yaml.safe_dump(rec, sort_keys=False), encoding="utf-8")
            got = mr.load(Path(d))
        self.assertIsInstance(got, mr.LoadStop)
        self.assertEqual(got.id, "material.kind_rule")
        self.assertIn("one assemblage record per composition", got.evidence["why"])

    def test_ambiguous_key_at_the_resolver(self):
        """R4: a hand-built registry with two records under one key is refused by name, never resolved to one."""
        from types import MappingProxyType
        from solver.result import freeze
        with tempfile.TemporaryDirectory() as d:
            reg = registry(d, allow_development=True)
            twin = dict(result.plain(reg.records["silicate_slb_mars_khan2022"]), id="silicate_slb_mars_twin")
            reg2 = mr.Registry(MappingProxyType({**reg.records, "silicate_slb_mars_twin": freeze(twin)}),
                               reg.unavailable, reg.warnings, True,
                               MappingProxyType({**reg.tables, "silicate_slb_mars_twin": reg.tables[
                                   "silicate_slb_mars_khan2022"]}))
            b = body("mars")
            layer = next(l for l in b.layers if l.material == "silicate_decl")
            v, why = sv._view_for(b, layer, None, 0.0, reg2, True)
        self.assertIsNone(v)
        self.assertEqual(why[0], "composition_key_ambiguous")

    def test_registry_loads_for_silicate_routes(self):
        """R5: a body whose only record-named layers are silicate routes gets a registry only when switched on."""
        import types
        b = types.SimpleNamespace(layers=[types.SimpleNamespace(material="silicate")])
        with tempfile.TemporaryDirectory() as d:
            reg = registry(d, allow_development=True)
            self.assertIsNone(sv.registry_for(b, context.Options(), reg))
            self.assertIs(sv.registry_for(b, context.Options(silicate_records=True), reg), reg)

    def test_option_reaches_every_views_call(self):
        """R6, R7: the solve's views and the sensitivity rebuild both read options.silicate_records."""
        seen = []
        real = sv._views

        def spy(*a, **k):
            seen.append(k.get("silicate", a[3] if len(a) > 3 else False))
            raise _Stop()

        class _Stop(Exception):
            pass
        with tempfile.TemporaryDirectory() as d:
            reg = registry(d, allow_development=True)
            try:
                sv._views = spy
                with self.assertRaises(_Stop):
                    sv.solve(body("earth"), context.Options(silicate_records=True), registry=reg)
                with self.assertRaises(_Stop):
                    sv._with_sensitivity(body("earth"), {}, None, context.Options(silicate_records=True), None, (),
                                         registry=reg)
            finally:
                sv._views = real
        self.assertEqual(seen, [True, True])

    def test_named_record_direct(self):
        """R8, R15: a layer naming an assemblage record directly gets an AssemblageView (switch on: the record requires
        it), and with params it refuses."""
        with tempfile.TemporaryDirectory() as d:
            reg = registry(d, allow_development=True)
            b = with_layer(body("earth"), "mantle", material="silicate_slb_default_bse")
            layer = next(l for l in b.layers if l.id == "mantle")
            v, why = sv._view_for(b, layer, None, 0.0, reg, True)
            self.assertIsInstance(v, ma.AssemblageView)
            mars = body("mars")
            dens = next(l.params["density"] for l in mars.layers if l.material == lm.BASAL_CONST)
            b2 = with_layer(b, "mantle", params={"density": dens})
            v, why = sv._view_for(b2, next(l for l in b2.layers if l.id == "mantle"), None, 0.0, reg, True)
            self.assertIsNone(v)
            self.assertEqual(why[0], "record_params")

    def test_silicate_with_composition_stays_legacy(self):
        """R11: `silicate` with a declared composition is not routed (only the no-composition line is): it refuses
        as today, switched on or off."""
        with tempfile.TemporaryDirectory() as d:
            reg = registry(d, allow_development=True)
            mars = body("mars")
            comp = next(l for l in mars.layers if l.material == "silicate_decl")
            b = with_layer(body("earth"), "mantle", composition=comp.composition, system=comp.system)
            on = sv._views(b, registry=reg, silicate=True)
            off = sv._views(b, registry=reg, silicate=False)
        self.assertIsInstance(on, result.Refusal)
        self.assertEqual((on.id, on.evidence.get("rule")), (off.id, off.evidence.get("rule")))
        self.assertEqual(on.evidence.get("rule"), "composition_not_consumed")


class BasalRecord(unittest.TestCase):
    """§7.4a: the basal record (Q6)."""

    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.reg = registry(self.d.name, allow_development=True)
        self.mars = body("mars")
        self.basal = next(l for l in self.mars.layers if l.material == lm.BASAL_CONST)

    def tearDown(self):
        self.d.cleanup()

    def test_density_and_dtdp(self):
        """ρ equals the declared 4050 kg/m³; dT/dP equals the overlying assemblage record's at the same (P, T) to
        1e-12; the notes name the declared grade."""
        views = sv._views(self.mars, registry=self.reg, silicate=True)
        bv = views[self.basal.id]
        above = bv.overlying
        self.assertIsInstance(above, ma.AssemblageView)
        self.assertEqual(above.material_id, "silicate_slb_mars_khan2022")
        for p, t in ((2.1e10, 420.0), (2.5e10, 510.0), (2.8e10, 375.0)):      # inside the synthetic table
            got, ref = bv.state(p, t), above.state(p, t)
            with self.subTest(p=p, t=t):
                self.assertEqual(got[0], 4050.0)
                self.assertLessEqual(abs(got[1] - ref[1]), 1e-12 * abs(ref[1]))
                self.assertTrue(any(isinstance(n, mv.DeclaredNote) and "declared" in n.text for n in got[2]))
        self.assertEqual(bv.name, lm.BASAL_CONST)
        self.assertEqual(bv.onset_curves(2e10, 2000.0), above.onset_curves(2e10, 2000.0))

    def test_no_overlying_assemblage_refuses(self):
        """Control: the record with no overlying assemblage layer refuses by name."""
        legacy_above = {l.id: lm.LegacyView("silicate", lm.eos.MATERIALS["silicate"], 1600.0) for l in self.mars.layers}
        v, why = sv._basal_view(self.mars, self.basal, legacy_above, self.reg)
        self.assertIsNone(v)
        self.assertEqual(why[0], "basal_without_assemblage")

    def test_missing_density_refuses(self):
        """Control: a missing `density` param refuses, as today's silicate_basal_const does."""
        b = with_layer(self.mars, self.basal.id, params={k: v for k, v in self.basal.params.items() if k != "density"})
        got = sv._views(b, registry=self.reg, silicate=True)
        self.assertIsInstance(got, result.Refusal)
        self.assertEqual(got.id, "input.unknown_material")
        off = sv._views(b, registry=self.reg, silicate=False)
        self.assertEqual(off.id, got.id)

    def test_other_params_refused(self):
        """The record_params lift is for density and thickness_km only."""
        b = with_layer(self.mars, self.basal.id, params={**self.basal.params, "porosity": self.basal.params["density"]})
        got = sv._views(b, registry=self.reg, silicate=True)
        self.assertEqual((got.id, got.evidence["rule"]), ("input.cross_field", "record_params"))

    def test_formula_check_identity(self):
        """The record's one formula check (ρ = the layer's declared density, tolerance 0), run here since P4 lists
        the record as a context record."""
        rec = result.plain(self.reg.records[lm.BASAL_CONST])
        fc = rec["formula_checks"][0]
        views = sv._views(self.mars, registry=self.reg, silicate=True)
        bv = ma.BasalView(rec, fc["state"]["layer_density"], views["mantle"], 1600.0)
        got = bv.state(2.5e10, 510.0)[0]
        self.assertLessEqual(abs(got - fc["expected"]), fc["tolerance"])

    def test_record_route_never_builds_it(self):
        """The plain record route refuses to build the basal record (it needs the layer above)."""
        v, why = sv._record_view(self.mars, self.basal, False, 0.0, self.reg)
        self.assertIsNone(v)
        self.assertEqual(why[0], "record_context")

    def test_notes_attributed_to_the_basal_record(self):
        """68: the overlying view's band note rides with the basal answer under the basal record's id."""
        views = sv._views(self.mars, registry=self.reg, silicate=True)
        notes = views[self.basal.id].state(2.5e10, 510.0)[2]
        bands = [n for n in notes if isinstance(n, mv.BandNote)]
        self.assertTrue(bands)
        self.assertTrue(all(n.material_id == lm.BASAL_CONST for n in bands))

    def test_rebuilds_carry_the_basal_view(self):
        """68: the sensitivity rebuild's basal view holds the rebuilt overlying view; a closure rebuild of the
        overlying layer rebuilds the basal view over the new one."""
        b2 = dataclasses.replace(self.mars, surface=dataclasses.replace(self.mars.surface,
                                                                        t_pot=self.mars.surface.t_pot + 10.0))
        v2 = sv._views(b2, registry=self.reg, silicate=True)
        self.assertIs(v2[self.basal.id].overlying, v2["mantle"])
        self.assertEqual(v2["mantle"].t_pot, b2.surface.t_pot)
        views = sv._views(self.mars, registry=self.reg, silicate=True)
        new_mantle = ma.view(result.plain(views["mantle"].record), self.reg.tables[views["mantle"].material_id],
                             1700.0)
        real = sv._view_for
        try:
            sv._view_for = lambda *a, **k: (new_mantle, None)
            b3 = closure_on(self.mars, "mantle", "fe_number")
            got = sv._views_at(b3, views, 0.5)
        finally:
            sv._view_for = real
        self.assertIs(got["mantle"], new_mantle)
        self.assertIs(got[self.basal.id].overlying, new_mantle)

    def test_registry_walkers_never_meet_a_context_record(self):
        """68: the registry's own RecordView builds (triple points, blend conflicts) return before a context record."""
        rec = dict(result.plain(self.reg.records[lm.BASAL_CONST]))
        rec["triple_points"] = [{"phases": ["a", "b", "c"]}]
        self.assertIsNone(mr.triple_point_misses(rec, "x.yaml"))
        rec["phases"] = [{**rec["phases"][0], "joins_within": [{"kind": "blend", "between": ["a", "b"]}]}]
        self.assertIsNone(mr.source_conflicts(rec, "x.yaml"))

    def test_named_assemblage_record_needs_the_switch(self):
        """68: a layer naming an assemblage record directly reads it only with the switch on (requires_switch)."""
        b = with_layer(body("earth"), "mantle", material="silicate_slb_default_bse")
        on = sv._views(b, registry=self.reg, silicate=True)
        self.assertIsInstance(on["mantle"], ma.AssemblageView)
        off = sv._views(b, registry=self.reg, silicate=False)
        self.assertIsInstance(off, result.Refusal)
        self.assertEqual(off.id, "input.unknown_material")

    def test_off_keeps_legacy_basal(self):
        """With the record file present and the switch off, the basal layer is today's LegacyView."""
        views = sv._views(self.mars, registry=self.reg, silicate=False)
        self.assertIsInstance(views[self.basal.id], lm.LegacyView)


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
