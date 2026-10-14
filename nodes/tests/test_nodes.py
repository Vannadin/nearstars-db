# 첫 노드 등록의 합격 시험 — 명세 닫힌 키·그래프 양끝 간선·run id 불변성·읽기 가드·측정/오너/평형온도 노드 (prereg-t-eq-stellar N4–N13)
"""Acceptance N4–N13 of `rewrite/nodes/prereg-t-eq-stellar.frozen.md` (artifacts, blob 9e9f08ae).
N1–N3 (solver unchanged) are solver/tests/test_node_additive.py and the suite runs.

    solver/.venv/bin/python -m unittest nodes.tests.test_nodes
"""
import copy
import json
import math
import shutil
import tempfile
import types
import unittest
from pathlib import Path

from solver.result import Answer, Refusal

from nodes import graph, records, run_id as rid, spec as sp
from nodes.runner import Runner
from nodes import runner as runner_mod

REPO = Path(__file__).resolve().parents[2]
L_SUN = 3.828e26
AU = 1.495978707e11
PROXIMA_B = {"name": "Proxima Cen b", "kind": "planet", "hosts": ["Proxima Cen"], "parent": None,
             "companions": ["Alpha Centauri A", "Alpha Centauri B"]}
PROXIMA = {"name": "Proxima Cen", "kind": "star", "hosts": [], "parent": None}
A_CEN_A_B = {"name": "Alpha Centauri A b", "kind": "planet", "hosts": ["Alpha Centauri A"], "parent": None}


def specs():
    return copy.deepcopy(sp.load_all())


def q(answer, key):
    return next(x for x in answer.quantities if x.key == key)


class N4SpecLoad(unittest.TestCase):
    def _fails(self, mutate, kind):
        s = specs()["t_eq_stellar"]
        mutate(s)
        with self.assertRaises(sp.SpecError) as cm:
            sp.check(s)
        self.assertEqual(cm.exception.kind, kind)

    def test_unknown_key(self):
        self._fails(lambda s: s.__setitem__("colour", "blue"), "spec.unknown_key")

    def test_missing_method_grade(self):
        self._fails(lambda s: s["outputs"]["t_eq"].pop("method_grade"), "spec.missing_key")

    def test_authored_without_counter_evidence(self):
        self._fails(lambda s: s["outputs"]["t_eq"].__setitem__("method_grade", "authored"),
                    "spec.counter_evidence_missing")

    def test_all_specs_load(self):
        self.assertEqual(sorted(specs()), ["bond_albedo_declared", "orbit_elements", "star_physical", "t_eq_stellar"])


class N5Graph(unittest.TestCase):
    def _fails(self, mutate, kind):
        s = specs()
        mutate(s)
        with self.assertRaises(graph.GraphError) as cm:
            graph.check(s)
        self.assertEqual(cm.exception.kind, kind)

    def test_real_graph_passes(self):
        graph.check(specs())

    def test_consumer_end_only(self):
        self._fails(lambda s: s["star_physical"]["outputs"]["luminosity"].__setitem__("to", []), "graph.one_ended")

    def test_producer_end_only(self):
        self._fails(lambda s: s["orbit_elements"]["outputs"]["a"]["to"].append("star_physical"), "graph.one_ended")

    def test_duplicate_quantity(self):
        def dup(s):
            twin = copy.deepcopy(s["t_eq_stellar"])
            twin["id"] = "t_eq_twin"
            s["t_eq_twin"] = twin
            for key in ("luminosity",):
                s["star_physical"]["outputs"][key]["to"].append("t_eq_twin")
            for key in ("a", "e"):
                s["orbit_elements"]["outputs"][key]["to"].append("t_eq_twin")
            s["bond_albedo_declared"]["outputs"]["bond_albedo"]["to"].append("t_eq_twin")
        self._fails(dup, "graph.duplicate_quantity")

    def test_unit_mismatch(self):
        self._fails(lambda s: s["t_eq_stellar"]["inputs"]["a"].__setitem__("unit", "AU"), "graph.unit_mismatch")


class N6RunId(unittest.TestCase):
    def setUp(self):
        self.s = specs()
        self.body = PROXIMA

    def _rid(self, spec, records=None):
        return rid.run_id(spec, upstream={}, records=records or {"k": "x"}, body=self.body)

    def test_a_non_physics_edits_keep_run_id(self):
        base = self._rid(self.s["star_physical"])
        for mutate in (lambda s: s["outputs"]["luminosity"]["to"].append("someone"),
                       lambda s: s.__setitem__("label", "renamed"),
                       lambda s: s.__setitem__("tests", ["elsewhere.py"]),
                       lambda s: s.__setitem__("hand_checks", [{"output": "luminosity"}])):
            s = copy.deepcopy(self.s["star_physical"])
            mutate(s)
            self.assertEqual(self._rid(s), base)

    def _copy_db(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        (tmp / "db").mkdir()
        shutil.copy(REPO / "db/stellar_props_curated.json", tmp / "db")
        shutil.copy(REPO / "db/planets_curated.json", tmp / "db")
        (tmp / "nodes/owner").mkdir(parents=True)
        shutil.copy(REPO / "nodes/owner/bond_albedo.yaml", tmp / "nodes/owner")
        return tmp

    def _edit_star(self, tmp, star, field, i, key, value):
        p = tmp / "db/stellar_props_curated.json"
        d = json.loads(p.read_text())
        d[star][field][i][key] = value
        p.write_text(json.dumps(d))
        records._CACHE.clear()

    def test_b_c_record_entry_binding(self):
        tmp = self._copy_db()
        records._CACHE.clear()
        r0 = Runner(db_root=tmp)
        star0, teq0 = r0.result("star_physical", PROXIMA)[1], r0.result("t_eq_stellar", PROXIMA_B)[1]
        # (c) an entry the node does not read (another star's record) moves neither
        self._edit_star(tmp, "Alpha Centauri A", "luminosity_measurements", 0, "reference", "edited")
        r1 = Runner(db_root=tmp)
        self.assertEqual(r1.result("star_physical", PROXIMA)[1], star0)
        self.assertEqual(r1.result("t_eq_stellar", PROXIMA_B)[1], teq0)
        # (b) the entry it reads moves it and its consumer
        self._edit_star(tmp, "Proxima Cen", "luminosity_measurements", 0, "reference", "edited")
        r2 = Runner(db_root=tmp)
        self.assertNotEqual(r2.result("star_physical", PROXIMA)[1], star0)
        self.assertNotEqual(r2.result("t_eq_stellar", PROXIMA_B)[1], teq0)
        records._CACHE.clear()

    def test_d_solver_code_moves_every_run_id(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        for p in ("solver/result.py", "solver/refusals.py", "nodes/types.py", "nodes/runner.py", "nodes/records.py",
                  "nodes/t_eq_stellar.py"):
            (tmp / p).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(REPO / p, tmp / p)
        before = {n: rid.run_id(s, upstream={}, records={}, body=self.body, repo=tmp) for n, s in self.s.items()}
        with open(tmp / "solver/result.py", "a") as fh:
            fh.write("\n# edited\n")
        after = {n: rid.run_id(s, upstream={}, records={}, body=self.body, repo=tmp) for n, s in self.s.items()}
        for n in self.s:
            self.assertNotEqual(before[n], after[n], n)


class N7ReadGuard(unittest.TestCase):
    def test_undeclared_read_refuses(self):
        r = Runner()
        bad = types.SimpleNamespace(compute=lambda ctx: (ctx.read("l_host"), ctx.read("radius")))
        real = runner_mod.importlib.import_module
        runner_mod.importlib.import_module = lambda name: bad if name == "nodes.t_eq_stellar" else real(name)
        try:
            out, _ = r.result("t_eq_stellar", PROXIMA_B)
        finally:
            runner_mod.importlib.import_module = real
        self.assertIsInstance(out, Refusal)
        self.assertEqual((out.id, dict(out.evidence)), ("node.undeclared_read", {"key": "radius"}))


class N8StarPhysical(unittest.TestCase):
    def test_proxima_luminosity(self):
        out, _ = Runner().result("star_physical", PROXIMA)
        lum = q(out, "star_physical.luminosity")
        self.assertEqual(lum.point, 0.00155 * L_SUN)
        self.assertAlmostEqual(lum.band.lo, (0.00155 - 6e-05) * L_SUN, delta=1e10)
        self.assertAlmostEqual(lum.band.hi, (0.00155 + 6e-05) * L_SUN, delta=1e10)
        self.assertEqual(lum.band.sources.input.contrib, "catalogue uncertainty as printed")
        src = lum.provenance.sources[0]
        self.assertEqual((src.kind, src.ref["file"], src.ref["key"], src.cites),
                         ("record", "db/stellar_props_curated.json", "Proxima Cen.luminosity_measurements[0]",
                          "2012ApJ...757..112B"))
        self.assertEqual((lum.provenance.grade, lum.method), ("measured", "read"))
        self.assertEqual([n.kind for n in out.notes], [])          # Demory 2009 0.0015 lies inside the band

    def test_spread_note_fires_outside_band(self):
        block = [{"value_lsun": 0.00155, "uncertainty_lsun": 6e-05, "method": "bolometric_flux", "recommended": True},
                 {"value_lsun": 0.0020, "method": "photometric", "reference": "synthetic", "recommended": False}]
        spec = specs()["star_physical"]
        real = records._block
        records._block = lambda s, b, d: (block, "Synthetic.luminosity_measurements")
        try:
            out, _ = records.run(spec, PROXIMA, "w")
        finally:
            records._block = real
        self.assertEqual([n.kind for n in out.notes], ["measurement_spread"])


class N9OrbitElements(unittest.TestCase):
    def test_proxima_b(self):
        out, _ = Runner().result("orbit_elements", PROXIMA_B)
        a, e = q(out, "orbit_elements.a"), q(out, "orbit_elements.e")
        self.assertEqual(a.point, 0.04848 * AU)
        self.assertAlmostEqual(a.band.hi - a.point, 0.00029 * AU, delta=1.0)
        self.assertEqual(e.point, 0.0)
        self.assertIsNone(e.band)
        self.assertEqual(e.band_reason, "the recommended record prints no uncertainty")


class N10HandChecks(unittest.TestCase):
    def test_hand_checks(self):
        from nodes import t_eq_stellar as m
        ns = {"pi": math.pi, "sqrt": math.sqrt}
        for hc in specs()["t_eq_stellar"]["hand_checks"]:
            st = hc["state"]
            got = m.s_inst(st["l_host"], st["a"], st["e"])
            if hc["output"] == "t_eq":
                got = m.t_eq(got, st["albedo"])
            indep = eval(hc["expression"], ns, dict(st))
            expected = indep if hc["expected"] == "teff_form" else hc["expected"]
            self.assertLessEqual(abs(got - expected) / expected, hc["tolerance"], hc)
            self.assertLessEqual(abs(got - indep) / indep, hc["tolerance"], hc)


class N11NegativeControls(unittest.TestCase):
    def _run_with(self, **override):
        r = Runner()
        out, _ = r.result("t_eq_stellar", PROXIMA_B)          # populate memo with real inputs
        for (node, body), (o, run) in list(r._memo.items()):
            if node in ("orbit_elements", "bond_albedo_declared") and isinstance(o, Answer):
                qs = []
                for x in o.quantities:
                    short = x.key.split(".")[1]
                    if short in override:
                        x = x.__class__(**{**{f: getattr(x, f) for f in x.__dataclass_fields__},
                                           "point": override[short], "band": None, "band_reason": "test"})
                    qs.append(x)
                r._memo[(node, body)] = (Answer(quantities=tuple(qs)), run)
        r._memo.pop(("t_eq_stellar", runner_mod.body_key(PROXIMA_B)))
        return r.result("t_eq_stellar", PROXIMA_B)[0]

    def test_e_one(self):
        self.assertEqual(self._run_with(e=1.0).id, "node.out_of_domain")

    def test_albedo_above_one(self):
        self.assertEqual(self._run_with(bond_albedo=1.2).id, "node.out_of_domain")

    def test_albedo_missing(self):
        out, _ = Runner().result("t_eq_stellar", dict(PROXIMA_B, name="Proxima Cen d"))
        self.assertEqual((out.id, out.evidence["input"]), ("node.input_missing", "albedo"))


class N12Grades(unittest.TestCase):
    def test_proxima_b_grade_by_route(self):
        out, _ = Runner().result("t_eq_stellar", PROXIMA_B)
        t = q(out, "t_eq_stellar.t_eq")
        self.assertEqual(t.provenance.grade, "authored")
        self.assertIn(("bond_albedo_declared.bond_albedo", "authored"), t.provenance.inputs_read)
        self.assertIn(("star_physical.luminosity", "measured"), t.provenance.inputs_read)
        self.assertIn(("orbit_elements.a", "measured"), t.provenance.inputs_read)
        self.assertEqual([n.kind for n in out.notes], ["companion_hosts_not_combined"])

    def test_measured_albedo_gives_measured(self):
        r = Runner()
        r.result("t_eq_stellar", PROXIMA_B)
        k = ("bond_albedo_declared", runner_mod.body_key(PROXIMA_B))
        o, run = r._memo[k]
        x = o.quantities[0]
        prov = x.provenance.__class__(**{**{f: getattr(x.provenance, f) for f in x.provenance.__dataclass_fields__},
                                         "grade": "measured"})
        r._memo[k] = (Answer(quantities=(x.__class__(**{**{f: getattr(x, f) for f in x.__dataclass_fields__},
                                                          "provenance": prov}),)), run)
        r._memo.pop(("t_eq_stellar", runner_mod.body_key(PROXIMA_B)))
        out, _ = r.result("t_eq_stellar", PROXIMA_B)
        self.assertEqual(q(out, "t_eq_stellar.t_eq").provenance.grade, "measured")


class N13RecordNotMeasured(unittest.TestCase):
    def _run_block(self, block):
        spec = specs()["orbit_elements"]
        real = records._block
        records._block = lambda s, b, d: (block, "Synthetic[pl_name=x].orbital")
        try:
            return records.run(spec, PROXIMA_B, "w")[0]
        finally:
            records._block = real

    def test_real_alpha_cen_a_b(self):
        r = Runner()
        out, _ = r.result("orbit_elements", A_CEN_A_B)
        self.assertEqual((out.id, out.evidence["method"]), ("node.record_not_measured", "predicted"))
        self.assertEqual(r.result("t_eq_stellar", A_CEN_A_B)[0].id, "node.input_missing")

    def test_predicted_with_bibcode_refuses(self):
        rec = {"semi_major_axis_au": 1.0, "eccentricity": 0.1, "method": "predicted", "bibcode": "2025ApJ...989L..22B",
               "recommended": True}
        self.assertEqual(self._run_block([rec]).id, "node.record_not_measured")

    def test_same_record_with_rv_reads(self):
        rec = {"semi_major_axis_au": 1.0, "eccentricity": 0.1, "method": "rv", "bibcode": "2025ApJ...989L..22B",
               "recommended": True}
        self.assertIsInstance(self._run_block([rec]), Answer)

    def test_missing_method_refuses(self):
        rec = {"semi_major_axis_au": 1.0, "eccentricity": 0.1, "bibcode": "x", "recommended": True}
        self.assertEqual(self._run_block([rec]).id, "node.record_not_measured")

    def test_legacy_dict_form_refuses(self):
        self.assertEqual(self._run_block({"semi_major_axis_au": 1.0}).id, "node.record_not_measured")


if __name__ == "__main__":
    unittest.main()
