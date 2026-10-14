# 채택 궤도 시험 — 권장 예측·이론 궤도를 authored 로 읽기, 관측 창 안/밖 노트, 가상 천체 거절, 명단 (prereg-orbit-adopted M1–M6, M5b·M5c)
"""Acceptance of `rewrite/nodes/prereg-orbit-adopted.frozen.md` (artifacts). M5c was added at audit (68).

    solver/.venv/bin/python -m unittest nodes.tests.test_orbit_adopted
"""
import copy
import json
import unittest
from pathlib import Path

from solver.result import Answer, Refusal

from nodes import records, spec as sp
from nodes.runner import Runner

REPO = Path(__file__).resolve().parents[2]
AU = 1.495978707e11
A_CEN_A_B = {"name": "Alpha Centauri A b", "kind": "planet", "hosts": ["Alpha Centauri A"], "parent": None}
X = {"name": "Synthetic b", "kind": "planet", "hosts": ["Synthetic"], "parent": None, "fictional": False}


def notes(out, kind):
    return [n for n in out.notes if n.kind == kind]


def run_block(block, body=X):
    spec = sp.load_all()["orbit_elements"]
    real = records._block
    records._block = lambda s, b, d: (block, "Synthetic[pl_name=Synthetic b].orbital")
    try:
        return records.run(spec, body, "w")[0]
    finally:
        records._block = real


def rec(e, method, recommended, ue=None, bib="2000Synth...1....1X"):
    r = {"semi_major_axis_au": 1.0, "eccentricity": e, "method": method, "bibcode": bib, "recommended": recommended}
    if ue is not None:
        r["uncertainty_eccentricity"] = ue
    return r


class M1AlphaCenAb(unittest.TestCase):
    def test_reads_authored(self):
        r = Runner()
        out, _ = r.result("orbit_elements", A_CEN_A_B)
        self.assertIsInstance(out, Answer)
        a = next(q for q in out.quantities if q.key == "orbit_elements.a")
        e = next(q for q in out.quantities if q.key == "orbit_elements.e")
        self.assertEqual((a.point, e.point), (1.6 * AU, 0.1))
        for q in (a, e):
            self.assertEqual((q.provenance.grade, q.method), ("authored", "chosen"))
            src = q.provenance.sources[0]
            self.assertTrue(src.ref["key"].endswith(".orbital[1]"))
            self.assertEqual(src.cites, "2025ApJ...989L..22B")
        sa = notes(out, "stability_adopted")
        self.assertEqual(len(sa), 1)
        self.assertEqual(sa[0].fields["method"], "predicted")
        avo = notes(out, "adopted_vs_observed")
        self.assertEqual(sorted(n.fields["output"] for n in avo), ["a", "e"])
        for n in avo:
            self.assertTrue(n.fields["observed_record"].endswith(".orbital[0]"))
            self.assertIsNone(n.fields["inside"])        # Beichman prints no uncertainty
        self.assertEqual(next(n for n in avo if n.fields["output"] == "e").fields["observed_value"], 0.4)
        t, _ = r.result("t_eq_stellar", A_CEN_A_B)
        self.assertEqual((t.id, t.evidence["input"]), ("node.input_missing", "albedo"))


class M2M3Window(unittest.TestCase):
    def test_inside(self):
        out = run_block([rec(0.20, "rv", False, ue=0.15), rec(0.10, "predicted", True)])
        n = next(n for n in notes(out, "adopted_vs_observed") if n.fields["output"] == "e")
        self.assertIs(n.fields["inside"], True)
        self.assertEqual(out.quantities[0].provenance.grade, "authored")

    def test_outside(self):
        out = run_block([rec(0.40, "rv", False, ue=0.10), rec(0.10, "predicted", True)])
        n = next(n for n in notes(out, "adopted_vs_observed") if n.fields["output"] == "e")
        self.assertIs(n.fields["inside"], False)
        self.assertTrue(all(q.provenance.grade == "authored" for q in out.quantities))


class M4Cases(unittest.TestCase):
    def test_theoretical_reads_authored(self):
        out = run_block([rec(0.1, "theoretical", True)])
        self.assertEqual(out.quantities[0].provenance.grade, "authored")

    def test_no_method_and_unknown_method_refuse(self):
        r0 = rec(0.1, "rv", True)
        r0.pop("method")
        self.assertEqual(run_block([r0]).id, "node.record_not_measured")
        self.assertEqual(run_block([rec(0.1, "analytic", True)]).id, "node.record_not_measured")

    def test_legacy_dict_refuses(self):
        self.assertEqual(run_block({"semi_major_axis_au": 1.0}).id, "node.record_not_measured")


class M5Fiction(unittest.TestCase):
    def test_real_40_eri_c_d_refuse(self):
        r = Runner()
        for name in ("40 Eridani A c", "40 Eridani A d"):
            out, _ = r.result("orbit_elements", {"name": name, "kind": "planet", "hosts": ["40 Eridani A"],
                                                 "parent": None})
            self.assertEqual(out.id, "node.fiction_in_measured_db", name)

    def test_explicit_fictional_observed_record_refuses(self):
        out = run_block([rec(0.1, "rv", True)], body=dict(X, fictional=True))
        self.assertEqual(out.id, "node.fiction_in_measured_db")

    def test_census(self):
        """M5b: the non-fictional bodies the adopted route reads are exactly the owner's two."""
        spec = sp.load_all()["orbit_elements"]
        adopted = set(spec["reads"]["adopted_methods"])
        census = records.fictional_census()
        data = json.loads((REPO / "db/planets_curated.json").read_text())
        found = set()
        for host, pls in data.items():
            for pl in pls:
                o = pl.get("orbital")
                if isinstance(o, list):
                    for e in o:
                        if e.get("recommended") and e.get("method") in adopted and pl["pl_name"] not in census:
                            found.add(pl["pl_name"])
        self.assertEqual(found, {"Alpha Centauri A b", "J1407b"})
        out, _ = Runner().result("orbit_elements", {"name": "J1407b", "kind": "planet", "hosts": ["V1400 Centauri"],
                                                    "parent": None})
        self.assertEqual(out.quantities[0].provenance.grade, "authored")
        self.assertEqual(notes(out, "stability_adopted")[0].fields["method"], "theoretical")

    def test_no_fictional_body_has_an_observational_record(self):
        """M5c (68): the measured route reads no derived flag, so the data must not hold an observed record for fiction."""
        census = records.fictional_census()
        specs = sp.load_all()
        stars = json.loads((REPO / "db/stellar_props_curated.json").read_text())
        planets = json.loads((REPO / "db/planets_curated.json").read_text())
        bad = []
        for name in census:
            for field in ("luminosity_measurements",):
                for e in (stars.get(name) or {}).get(field) or []:
                    if e.get("method") in specs["star_physical"]["reads"]["methods"]:
                        bad.append((name, field))
            for pls in planets.values():
                for pl in pls:
                    if pl["pl_name"] != name:
                        continue
                    o = pl.get("orbital")
                    for e in (o if isinstance(o, list) else [o]):
                        if isinstance(e, dict) and e.get("method") in specs["orbit_elements"]["reads"]["methods"]:
                            bad.append((name, "orbital"))
        self.assertEqual(bad, [])


class M6Spec(unittest.TestCase):
    def test_overlap_fails(self):
        s = copy.deepcopy(sp.load_all()["orbit_elements"])
        s["reads"]["adopted_methods"].append("rv")
        with self.assertRaises(sp.SpecError) as cm:
            sp.check(s)
        self.assertEqual(cm.exception.kind, "spec.bad_value")


if __name__ == "__main__":
    unittest.main()
