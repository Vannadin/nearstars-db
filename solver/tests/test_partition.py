# 덩어리(bulk:) → 층 계획 순수 함수 시험 — 지구(Wang 2018 표 1)·화성(Khan 2022 왕복)·O 점검·순수성·schema 의 bulk 칸 (layers S0·S1)
"""layers S0 registration f298b628 §3, tests 1–6, with 68's S0 notes and directing's 11-07 rulings.

Run from the worktree root:  python -m unittest solver.tests.test_partition
Every control and mutant below must go red; each asserts that it does.
"""
import importlib.util
import json
import math
import re
import subprocess
import sys
import types
import unittest
from pathlib import Path

from solver import partition as pt
from solver.from_v1 import thaw
from solver.result import Refusal
from solver.yamlio import load_data

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "wang2018_table1.json"
TRIO = {"source_kind": "measured", "grade": "read", "counter_evidence_searched": "test fixture"}


def wang():
    return json.loads(FIXTURE.read_text())


def wang_bulk(with_sigma=True):
    """Wang Table 1's bulk column, every element, divided by its printed sum (1.000953: the table's rounding; its
    footnote a says the column was rescaled to 1e6 ppm). A symmetric ± goes in as sigma."""
    rows = wang()["rows"]
    s = math.fsum(r["bulk"]["value"] for r in rows)
    el = {}
    for r in rows:
        b = r["bulk"]
        sym = b["plus"] == b["minus"]
        el[r["element"]] = {"value": b["value"] / s, "sigma": b["plus"] / s} if (with_sigma and sym) else b["value"] / s
    return {"elements": el, "source": "Wang+ 2018 Table 1 bulk column", **TRIO}, s


def mutant(old, new):
    """partition.py with one exact text replaced (asserted unique), loaded as its own module."""
    src = Path(pt.__file__).read_text()
    if src.count(old) != 1:
        raise AssertionError(f"mutant anchor count {src.count(old)} != 1: {old!r}")
    mod = types.ModuleType("partition_mutant")
    mod.__file__ = pt.__file__
    sys.modules["partition_mutant"] = mod          # dataclass resolves its module through sys.modules
    try:
        exec(compile(src.replace(old, new), "partition_mutant", "exec"), mod.__dict__)
    finally:
        del sys.modules["partition_mutant"]
    return mod


class Materials(unittest.TestCase):
    """Test 1, (M) and (P)."""

    def test_earth_like_written_out_equals_the_preset(self):
        m = pt.partition({"materials": [{"material": "fe_prem", "mass_fraction": 0.325},
                                         {"material": "silicate", "mass_fraction": 0.675}]})
        presets = load_data(ROOT / "solver" / "data" / "presets.yaml")
        want = json.dumps(thaw(presets["earth_like"]["layers"]))
        self.assertEqual(json.dumps(thaw(m.layers)), want)              # byte-equal, mantle without extent
        p = pt.partition({"preset": "earth_like"})
        self.assertEqual(json.dumps(thaw(p.layers)), want)
        swapped = pt.partition({"materials": [{"material": "silicate", "mass_fraction": 0.675},
                                               {"material": "fe_prem", "mass_fraction": 0.325}]})
        self.assertEqual(json.dumps(thaw(swapped.layers)), want)        # ordered by role, not by listing

    def test_fractions_not_summing_to_one_refuse(self):
        r = pt.partition({"materials": [{"material": "fe_prem", "mass_fraction": 0.325},
                                         {"material": "silicate", "mass_fraction": 0.675 - 1e-9}]})
        self.assertIsInstance(r, Refusal)
        self.assertEqual(r.id, "input.bulk_fractions")
        r = pt.partition({"materials": [{"material": "basalt", "mass_fraction": 1.0}]})
        self.assertEqual((r.id, r.evidence["got"]), ("input.not_in_vocabulary", "basalt"))


class Earth(unittest.TestCase):
    """Test 2: Wang's bulk column in, the default fe_metal_fraction."""

    @classmethod
    def setUpClass(cls):
        cls.bulk, cls.bulk_sum = wang_bulk()
        cls.plan = pt.partition(cls.bulk)
        cls.rows = {r["element"]: r for r in wang()["rows"]}

    def test_core_mass_fraction(self):
        """68 n1: CMF = 0.325 × Σ(core column) / Σ(bulk column) exactly, since the core composition is the column
        renormalised over all 49 of its elements (all declared here). Σ(core column) = 0.99965032989 and
        Σ(bulk column) = 1.000953 as printed (fixture column_sums), so CMF = 0.324577, inside Wang's 32.5 ± 0.3."""
        sums = wang()["column_sums"]
        self.assertAlmostEqual(sums["core"], 0.99965032989, places=11)
        cmf = self.plan.core_mass_fraction
        self.assertLess(abs(cmf - 0.325 * sums["core"] / self.bulk_sum), 1e-12)
        self.assertLessEqual(abs(cmf - 0.325), 0.003)
        print(f"\nEarth CMF {cmf!r} = 0.325 × Σcore {sums['core']} / Σbulk {self.bulk_sum!r}")

    def test_residual(self):
        self.assertLessEqual(abs(self.plan.residual), 1e-12)

    def _mantle_check(self, plan, el, oxide, hand):
        """Mantle `el` per unit mantle (1 − CMF) against Wang's PM row, within the correlated band (S0 post-freeze
        note 3): σ = √(σ_PM² + ε²), ε = |bulk − (0.325·core + 0.675·PM)| / 0.675, the printed table's own closure
        residual for the row. Wang build the bulk column from the core and PM columns (eq. A.5), so bulk ± and core ±
        are not independent; the old √(σ_bulk² + (CMF σ_core)²)/(1 − CMF) ⊕ σ_PM counted the core's ± twice.
        By that construction the partition's mantle is the PM row up to ε, so this band mainly checks arithmetic.
        Its power to catch a wrong partition is the mutant (test_mutant_without_the_light_draw_is_red_on_si), which
        stays in this test for good (68 n1, directing). `hand` is the oxide wt % from the PM row by hand (quoted in
        the caller), checked through the same oxide factor."""
        r = self.rows[el]
        cmf = plan.core_mass_fraction
        ox = plan.ledger["mantle_oxides"][oxide]
        name, n_cat, n_o = pt.BULK["oxides"][el]
        mass = pt.BULK["atomic_mass_g_mol"]
        factor = (n_cat * mass[el] + n_o * mass["O"]) / (n_cat * mass[el])
        self.assertLess(abs(r["pm"]["value"] * 100 * factor - hand), 5e-4)            # the quoted hand value
        got = ox / (1 - cmf) / factor
        core = r["core"]["value"] if r["core"] else 0.0
        eps = abs(r["bulk"]["value"] - (0.325 * core + 0.675 * r["pm"]["value"])) / 0.675
        sigma = math.hypot(r["pm"]["plus"], eps)
        print(f"\n{el}: got {got!r} · PM {r['pm']['value']} · σ_PM {r['pm']['plus']} · ε {eps!r} · σ {sigma!r}")
        return got, r["pm"]["value"], sigma

    def test_mantle_against_the_primitive_mantle(self):
        """Hand values from the PM column: SiO₂ = 21.3 × 60.0843 / 28.0855 = 45.568 wt %; MgO = 22.3 × 40.3044 /
        24.305 = 36.980 wt %; FeO = 6.32 × 71.8444 / 55.845 = 8.131 wt %."""
        for el, ox, hand in (("Si", "SiO2", 45.568), ("Mg", "MgO", 36.980), ("Fe", "FeO", 8.131)):
            got, want, sigma = self._mantle_check(self.plan, el, ox, hand)
            self.assertLessEqual(abs(got - want), sigma, f"{el}: {got} vs PM {want} ± {sigma}")

    def test_ni_core_share(self):
        """§1: 0.325 × 5.06 / 1.77 = 0.929 ± 0.060 is what the draw gives for Wang's own bulk."""
        self.assertLessEqual(abs(self.plan.ledger["ni_core_share"] - 0.929), 0.060)

    def test_mutant_without_the_light_draw_is_red_on_si(self):
        """Directing's mutant: only Fe and Ni drawn (rev 0's rule) → mantle Si from all 16.0 % bulk Si, ≈ 11 %
        relative high per unit mantle, outside the band. This mutant carries test 2's power (the correlated band
        alone checks arithmetic, see _mantle_check); never drop it (S0 note 3, 68 n1)."""
        m = mutant("d = m - core.get(k, 0.0)", "d = m - (core.get(k, 0.0) if k in ('Fe', 'Ni') else 0.0)")
        plan = m.partition(self.bulk)
        got, want, sigma = self._mantle_check(plan, "Si", "SiO2", 45.568)
        self.assertGreater(abs(got - want), sigma)
        self.assertGreater(got / want - 1, 0.10)
        self.assertGreater(abs(plan.residual), 1e-3)                    # and the light shares are counted twice

    def _default_text(self, mod, sigma=None):
        """The fe_metal_fraction default disclosure `mod.partition` writes for Wang's bulk, with the yaml's σ replaced
        by `sigma` for that call when given (the BULK dict is copied, never edited in place)."""
        saved = mod.BULK
        if sigma is not None:
            d = dict(saved["defaults"])
            d["fe_metal_fraction"] = {**d["fe_metal_fraction"], "sigma": sigma}
            mod.BULK = {**saved, "defaults": d}
        try:
            plan = mod.partition(self.bulk)
        finally:
            mod.BULK = saved
        return next(x["text"] for x in plan.disclosures if x["text"].startswith("fe_metal_fraction default"))

    def test_default_disclosure_reads_the_yaml_sigma(self):
        """S0 note 3: the disclosure names schema.yaml's σ (0.0046), and a yaml σ of 0.1 prints «± 0.1»."""
        d = pt.BULK["defaults"]["fe_metal_fraction"]
        self.assertEqual(d["sigma"], 0.0046)
        self.assertEqual(self._default_text(pt), f"fe_metal_fraction default 0.8625 ± 0.0046 — {d['grade']}")
        self.assertIn("± 0.1 — ", self._default_text(pt, 0.1))

    def test_planted_sigma_literal_is_caught(self):
        """Guard control: partition.py with the σ written as a literal reads right at the default and wrong under the
        yaml σ 0.1, so the check above goes red on it."""
        m = mutant("± {fm['sigma']} — ", "± 0.0046 — ")
        self.assertIn("± 0.0046 — ", self._default_text(m))
        self.assertNotIn("± 0.1 — ", self._default_text(m, 0.1))

    def test_control_fe_metal_fraction_half_leaves_the_band(self):
        """With 0.5 the O check refuses first (more FeO: `input.bulk_oxygen_short`), so the control widens O's ± to 1
        to reach the band's assertion alone."""
        self.assertEqual(getattr(pt.partition(self.bulk, {"fe_metal_fraction": 0.5}), "id", None),
                         "input.bulk_oxygen_short")
        el = dict(self.bulk["elements"])
        el["O"] = {"value": el["O"]["value"], "sigma": 1.0}
        plan = pt.partition({**self.bulk, "elements": el}, {"fe_metal_fraction": 0.5})
        self.assertGreater(abs(plan.core_mass_fraction - 0.325), 0.003)

    def test_undeclared_core_elements_are_disclosed(self):
        """A bulk with the majors only: the core column is renormalised over the declared elements, and the factor
        and the undeclared share are disclosed. Registration §2.2's «1.90 %» is the column beyond Fe, Ni, O, Si, S, C
        against the nominal 100 %: 100 − 98.099 = 1.901. Against the printed sum 99.965 it is 1.867 %. This bulk also
        declares Mg and Na, which the core column lists (0.0588 %, 0.1372 %), so its undeclared share is 1.671 %."""
        keep = ("Fe", "Ni", "O", "Si", "S", "C", "Mg", "Ca", "Al", "Na")
        el = {k: self.bulk["elements"][k] for k in keep}
        s = math.fsum(pt._val(v) for v in el.values())
        el = {k: ({"value": v["value"] / s, "sigma": v["sigma"] / s} if isinstance(v, dict) else v / s)
              for k, v in el.items()}
        plan = pt.partition({**self.bulk, "elements": el})
        d = next(x["data"] for x in plan.disclosures if x["text"].startswith("fe_prem core composition"))
        core = {r["element"]: r["core"]["value"] for r in wang()["rows"] if r["core"]}
        s_col = math.fsum(core.values())
        six = 1 - math.fsum(core[k] for k in ("Fe", "Ni", "O", "Si", "S", "C")) / s_col
        self.assertAlmostEqual(six, 0.01867, delta=5e-6)
        self.assertAlmostEqual(d["undeclared_share_of_column"],
                               1 - math.fsum(core[k] for k in keep if k in core) / s_col, places=15)
        self.assertAlmostEqual(d["undeclared_share_of_column"], 0.01671, delta=5e-6)
        self.assertLessEqual(abs(plan.residual), 1e-12)


class Mars(unittest.TestCase):
    """Test 3: a round-trip on Khan+ 2022's own model (2022E_PSL.57817330K), not an independent check.

    Built from Khan's printed numbers: Table 1 (PDF p. 7) mantle CFMASNa SiO₂ 46.66, Al₂O₃ 3.49, MgO 32.81, CaO
    2.66, FeO 13.68 (1σ 0.43), Na₂O 0.69, core Fe 81.6 wt %; abstract (p. 1) CMF 0.250 ± 0.005, core radius
    1840 ± 10 km. Compared against Khan's own structure (no basal layer), not mars.yaml's layered body.
    The core's S/O/C split is mars.yaml's: O 0.04, C 0.014 declared and S = 1 − 0.816 − 0.04 − 0.014 = 0.130
    declared here (mars.yaml's `S: fit` is S1's closure). Caveat: Khan's Table 3 limits are S ≈ 9, C ⩾ 3, O ⩽ 2.5,
    H ⩽ 0.5 wt%; S 13.0 and O 4.0 exceed them and C 1.4 falls short of «⩾ 3 wt% C», so this bulk is not a
    physical Mars. The test checks the partition's arithmetic on Khan's numbers, nothing more.
    68 n2: fe_metal_fraction = 0.25 × 81.6 / bulk Fe; bulk Fe ≈ 28.4 wt %, against Khan p. 9 «a bulk planet Fe
    concentration of ∼28.5 wt%»."""

    MANTLE = {"SiO2": 46.66, "Al2O3": 3.49, "MgO": 32.81, "CaO": 2.66, "FeO": 13.68, "Na2O": 0.69}
    CORE = {"Fe": 0.816, "S": 0.130, "O": 0.04, "C": 0.014}

    def test_round_trip(self):
        mass = pt.BULK["atomic_mass_g_mol"]
        by_ox = {v[0]: (k, v[1], v[2]) for k, v in pt.BULK["oxides"].items()}
        s = math.fsum(self.MANTLE.values())
        el = {}
        for ox, w in self.MANTLE.items():
            k, n_cat, n_o = by_ox[ox]
            m = 0.75 * w / s
            cat = m * n_cat * mass[k] / (n_cat * mass[k] + n_o * mass["O"])
            el[k] = el.get(k, 0.0) + cat
            el["O"] = el.get("O", 0.0) + m - cat
        for k, x in self.CORE.items():
            el[k] = el.get(k, 0.0) + 0.25 * x
        self.assertLess(abs(math.fsum(el.values()) - 1.0), 1e-12)
        self.assertLess(abs(el["Fe"] - 0.284), 0.001)
        self.assertLess(abs(el["Fe"] - 0.285), 0.002)                    # Khan p. 9 «∼28.5 wt%»
        f = 0.25 * 0.816 / el["Fe"]
        plan = pt.partition({"elements": el, "source": "Khan+ 2022 round trip", **TRIO},
                            {"fe_metal_fraction": f, "core_material": "fe_core_light",
                             "core_light": {"S": 0.130, "O": 0.04, "C": 0.014}})
        self.assertNotIsInstance(plan, Refusal, getattr(plan, "text", ""))
        self.assertLessEqual(abs(plan.core_mass_fraction - 0.250), 0.005)
        self.assertLessEqual(abs(plan.layers[1]["composition"]["oxides_wt"]["FeO"] - 13.68), 0.43)
        self.assertLessEqual(abs(plan.residual), 1e-12)
        print(f"\nMars round trip: bulk Fe {el['Fe']!r}, fe_metal_fraction {f!r}, CMF {plan.core_mass_fraction!r}, "
              f"O check {plan.o_check['sigma_o_source']}")


class Oxygen(unittest.TestCase):
    """Test 4. O is moved by s and every element divided by (1 + s), so the block still sums to 1; s is set from
    Δ's slope in s for a target n σ_Δ."""

    @classmethod
    def setUpClass(cls):
        cls.base, _ = wang_bulk()

    def shifted(self, s, partition=pt.partition, sigma=True):
        el = {}
        for k, v in self.base["elements"].items():
            val, sig = (v["value"], v["sigma"]) if isinstance(v, dict) else (v, None)
            if k == "O":
                val += s
            val /= 1 + s
            el[k] = {"value": val, "sigma": sig / (1 + s)} if (sig is not None and (sigma or k != "O")) else val
        return partition({**self.base, "elements": el})

    def target(self, n):
        """s with Δ ≈ n σ_Δ (linear in s to first order; one Newton step from two probes is enough here)."""
        p0, p1 = self.shifted(0.0), self.shifted(1e-3)
        slope = (p1.o_check["delta"] - p0.o_check["delta"]) / 1e-3
        return (n * p0.o_check["sigma_delta"] - p0.o_check["delta"]) / slope

    def test_short_and_excess_refuse_by_name(self):
        r = self.shifted(self.target(3.3))
        self.assertIsInstance(r, Refusal, "3.3 σ short passed")
        self.assertEqual(r.id, "input.bulk_oxygen_short")
        r = self.shifted(self.target(-3.3))
        self.assertEqual(getattr(r, "id", None), "input.bulk_oxygen_excess")

    def test_within_passes_and_prints_its_check(self):
        p = self.shifted(self.target(0.8))
        self.assertNotIsInstance(p, Refusal, getattr(p, "text", ""))
        c = p.o_check
        self.assertLessEqual(abs(c["delta"]), c["sigma_delta"])
        self.assertEqual(c["sigma_o_source"], "stated")
        print(f"\nO check: Δ {c['delta']!r}, σ_Δ {c['sigma_delta']!r}, σ_O {c['sigma_o']!r} ({c['sigma_o_source']})")

    def test_no_stated_o_sigma_uses_the_wang_default(self):
        p = self.shifted(0.0, sigma=False)
        label = "default from Wang 2018, not this body's"
        self.assertEqual(p.o_check["sigma_o_source"], label)
        self.assertAlmostEqual(p.o_check["sigma_o"], self.base["elements"]["O"]["value"] * 0.7 / 30.8, places=15)
        self.assertTrue(any(label in d["text"] for d in p.disclosures))
        print(f"\nO check width: {label}, σ_O {p.o_check['sigma_o']!r}")

    def test_mutant_without_the_check_passes_the_short_case(self):
        m = mutant('if abs(delta) > BULK["o_check_sigmas"] * sigma_d:', "if False:")
        s = self.target(3.3)
        self.assertIsInstance(self.shifted(s), Refusal)
        self.assertNotIsInstance(self.shifted(s, partition=m.partition), Refusal)   # caught only by the check


class Purity(unittest.TestCase):
    """Test 5."""

    def test_no_module_state_and_equal_calls(self):
        from solver.tests import test_a6_state as a6
        self.assertEqual(a6.findings(Path(pt.__file__).read_text(), "partition.py"), [])
        b, _ = wang_bulk()
        self.assertEqual(pt.partition(b), pt.partition(b))


class SchemaBulk(unittest.TestCase):
    """layers S1 §1 (1346ffc6): S0's bulk.yaml joined schema.yaml's top level as `bulk:`. The section equals ea3ae617's
    bulk.yaml key by key, but for S0 post-freeze note 3's σ and its source; bulk.yaml is gone; schema.yaml's code readers are validate.py and partition.py; the census
    stays PASS (S0's post-freeze note 1 tests, carried over)."""

    def test_section_equals_s0_bulk_yaml(self):
        old = subprocess.run(["git", "-C", str(ROOT), "show", "ea3ae617:solver/data/bulk.yaml"], capture_output=True,
                             text=True)
        self.assertEqual(old.returncode, 0, old.stderr)
        import yaml
        want = yaml.safe_load(old.stdout)
        # S0 post-freeze note 3 changes exactly fe_metal_fraction's sigma (0.042 → 0.0046) and adds the σ's source
        fm = want["defaults"]["fe_metal_fraction"]
        self.assertEqual(fm["sigma"], 0.042)
        fm["sigma"] = 0.0046
        fm["source"] += "; σ: Wang+ 2018 eq. A.5 dependence kept (3f, artifacts e38928ebe; S0 post-freeze note 3)"
        self.assertEqual(want, thaw(pt.BULK))
        self.assertFalse((ROOT / "solver" / "data" / "bulk.yaml").exists())

    def test_schema_readers(self):
        out = subprocess.run(["git", "-C", str(ROOT), "grep", "--untracked", "-l", "-I", "-E",
                              r"data\" / \"schema\.yaml\"|data/schema\.yaml|bulk\.yaml", "--", "engine", "solver",
                              "scripts", "derived", "tools"], capture_output=True, text=True).stdout.split()
        code = sorted(f for f in set(out) if f.endswith(".py") and "/tests/" not in f)
        self.assertEqual(code, ["solver/partition.py", "solver/validate.py"])

    def test_census_pass_on_the_join(self):
        sys.path.insert(0, str(ROOT))
        try:
            from derived import check as dc
        finally:
            sys.path.pop(0)
        doc = dc.load_list()
        self.assertNotIn("solver/data/bulk.yaml", set(dc.file_owner(doc)))
        for f in ("solver/data/schema.yaml", "solver/tests/fixtures/wang2018_table1.json",
                  "solver/tests/fixtures/bulk_s1_body_canon.json"):
            self.assertEqual([x for x in dc.census(doc, files=[f], root=ROOT) if x.startswith(f)], [])

    def test_core_column_matches_the_fixture(self):
        rows = {r["element"]: r for r in wang()["rows"] if r["core"]}
        printed = {k: pt._printed(v) for k, v in pt.BULK["fe_prem_core_printed"].items()}
        self.assertEqual(sorted(printed), sorted(rows))
        for k, v in printed.items():
            self.assertLess(abs(v - rows[k]["core"]["value"]), 1e-12 * max(v, 1e-9), k)

    def test_atomic_masses_match_burnman(self):
        spec = importlib.util.find_spec("burnman")     # both gate venvs carry burnman 2.1.0; no skip
        self.assertIsNotNone(spec, "burnman is not importable: the masses' source cannot be checked")
        f = Path(spec.origin).parent / "data" / "input_masses" / "atomic_masses.dat"
        table = {}
        for ln in f.read_text().splitlines():
            p = ln.split()
            if len(p) == 2 and not ln.startswith("%"):
                table[p[0]] = float(p[1]) * 1000.0
        for k, v in pt.BULK["atomic_mass_g_mol"].items():
            self.assertLess(abs(v - table[k]), 1e-9, k)


if __name__ == "__main__":
    unittest.main(verbosity=2)
