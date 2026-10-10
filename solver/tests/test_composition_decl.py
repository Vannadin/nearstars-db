# 층 조성 선언 시험 — 체계별 합 규칙 · 출처 종류와 짝 칸 · 편차 · 표 열쇠가 옛 엔진과 비트 같음, 각 규칙에 심은 대조 (phase-2 등록 P1, 덧붙임 2)
"""P1 body side of rewrite/phase2-impl.frozen.md with post-freeze note 2: the per-system composition rule, the
source kind and its companion fields, the deviation block, and the table key staying bit-identical to legacy.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_composition_decl
"""
import copy
import math
import unittest

from solver import body as bd
from solver import legacy_materials  # noqa: F401  (puts engine/ on the path)
from solver import validate as vd
from solver.result import Refusal
from solver.tests.test_validate import BASE, refused

import mantle_composition as mc  # noqa: E402  (engine/, at the tree's own commit)

TRIO = {"grade": "analog", "source": "s", "counter_evidence_searched": "c"}
#: The two declarations legacy's own test pins (engine/test_mantle_composition.py: W&H 2005 Table 3 Bulk DMM and
#: Khan+ 2022 Table 1), copied from that file at this tree's commit.
DMM_WH2005 = {"SiO2": 44.71, "Al2O3": 3.98, "FeO": 8.18, "MnO": 0.13, "MgO": 38.73, "CaO": 3.17, "Na2O": 0.13,
              "Cr2O3": 0.57, "TiO2": 0.13, "NiO": 0.24, "K2O": 0.006, "P2O5": 0.019}
MARS_KHAN2022 = {"SiO2": 46.66, "Al2O3": 3.49, "MgO": 32.81, "CaO": 2.66, "FeO": 13.68, "Na2O": 0.69}


def mantle(value, **extra):
    d = copy.deepcopy(BASE)
    d["layers"][1].update(system="silicate", composition={"value": dict(value), **TRIO, "source_kind": "measured",
                                                          **extra})
    return d


def core(value, **extra):
    d = copy.deepcopy(BASE)
    d["layers"][0].update(system="iron_alloy", composition={"value": dict(value), **TRIO, **extra})
    return d


def comp_of(out, layer_id):
    assert not isinstance(out, Refusal), out.text
    return next(l.composition for l in out.layers if l.id == layer_id)


class TSystems(unittest.TestCase):
    def test_both_legacy_declarations_load_as_printed(self):
        for name, wt in (("earth", DMM_WH2005), ("mars", MARS_KHAN2022)):
            with self.subTest(body=name):
                c = comp_of(vd.validate(mantle(wt)), "mantle")
                self.assertEqual(dict(c.value), wt)                      # stored as printed, no second normalisation

    def test_unknown_system(self):
        d = mantle(MARS_KHAN2022)
        d["layers"][1]["system"] = "silicates"
        refused(self, vd.validate(d), "input.composition_system", system="silicates")

    def test_component_outside_enum(self):
        refused(self, vd.validate(mantle(dict(MARS_KHAN2022, H2O=0.1))), "input.composition_component",
                component="H2O")
        refused(self, vd.validate(core({"S": 0.1, "Si": 0.02})), "input.composition_component", component="Si")

    def test_silicate_cfmasna_and_sum(self):
        refused(self, vd.validate(mantle({k: v for k, v in MARS_KHAN2022.items() if k != "Na2O"})),
                "input.composition_missing", missing=("Na2O",))
        refused(self, vd.validate(mantle(dict(MARS_KHAN2022, SiO2=49.0))), "input.composition_sum")   # 102.33
        ok = vd.validate(mantle(dict(MARS_KHAN2022, SiO2=48.6)))                                       # 101.93
        self.assertNotIsInstance(ok, Refusal)
        refused(self, vd.validate(mantle(dict(MARS_KHAN2022, FeO=-1.0))), "input.out_of_domain")

    def test_iron_alloy_partial_controls(self):
        """The four planted controls of note 2 item 4, and the valid forms they sit beside."""
        fit = core({"S": "fit", "O": 0.04})
        fit["inputs"]["radius_earth"] = 1.0
        fit["closure"] = {"kind": "composition", "layer": "core", "name": "S"}
        self.assertNotIsInstance(vd.validate(fit), Refusal)
        self.assertNotIsInstance(vd.validate(core({"S": 0.0, "O": 0.99})), Refusal)    # no sum-to-1 rule
        for value, comp in (({"S": -0.01}, "S"), ({"S": 1.2}, "S"), ({"S": 0.5, "O": 0.3, "C": 0.2}, "S+O+C"),
                            ({"S": "fitt"}, "S")):
            with self.subTest(value=value):
                refused(self, vd.validate(core(value)), "input.composition_fraction", component=comp)


class TSourceKind(unittest.TestCase):
    def test_required_on_silicate_only(self):
        d = mantle(MARS_KHAN2022)
        del d["layers"][1]["composition"]["source_kind"]
        refused(self, vd.validate(d), "input.missing_key", key="mantle.composition.source_kind")
        self.assertNotIsInstance(vd.validate(core({"S": 0.1})), Refusal)

    def test_accepted_kinds(self):
        bse = _with_kind(mantle(dict(vd.BSE["oxides_wt"])), "default_bse")
        self.assertNotIsInstance(vd.validate(bse), Refusal)
        for kind, extra in (("measured", {}), ("preset", {"preset": "earth_like"}),
                            ("owner_override", {"owner_direction": "db20e171", "anchor": "an owner bullet"})):
            with self.subTest(kind=kind):
                out = vd.validate(_with_kind(mantle(MARS_KHAN2022, **extra), kind))
                self.assertNotIsInstance(out, Refusal, getattr(out, "text", ""))

    def test_not_built_and_unknown(self):
        for kind in ("inherited", "star_derived"):
            with self.subTest(kind=kind):
                refused(self, vd.validate(_with_kind(mantle(MARS_KHAN2022), kind)), "input.source_kind_not_built",
                        source_kind=kind)
        refused(self, vd.validate(_with_kind(mantle(MARS_KHAN2022), "default_mgsio3")), "input.source_kind",
                source_kind="default_mgsio3")

    def test_default_bse_is_pinned(self):
        """Impl note 5 item 3 (r2 on P1): default_bse cannot label arbitrary numbers."""
        for name, wt in (("Khan's Mars", MARS_KHAN2022), ("one oxide moved", dict(vd.BSE["oxides_wt"], FeO=8.06)),
                         ("one oxide dropped", {k: v for k, v in vd.BSE["oxides_wt"].items() if k != "P2O5"})):
            with self.subTest(case=name):
                refused(self, vd.validate(_with_kind(mantle(wt), "default_bse")), "input.source_kind",
                        source_kind="default_bse")

    def test_table5_cross_check(self):
        """Impl note 5 item 4: MS95 Table 5's element values, converted with standard molar masses, match Table 4
        col. 1 within the printed rounding of both. A planted Fe → Fe2O3 factor fails."""
        self.assertEqual(_table5_misses(_FACTORS), [])
        planted = dict(_FACTORS, Fe=("FeO", 159.6882 / (2 * 55.845)))
        self.assertEqual([m[0] for m in _table5_misses(planted)], ["Fe"])

    def test_companions(self):
        refused(self, vd.validate(_with_kind(mantle(MARS_KHAN2022), "preset")), "input.source_kind")
        refused(self, vd.validate(_with_kind(mantle(MARS_KHAN2022, preset="pure_mgsio3"), "preset")),
                "input.source_kind")                                       # not in presets.yaml
        refused(self, vd.validate(_with_kind(mantle(MARS_KHAN2022, owner_direction="db20e171"), "owner_override")),
                "input.source_kind")                                       # anchor missing
        refused(self, vd.validate(mantle(MARS_KHAN2022, preset="earth_like")), "input.source_kind")   # stray

    def test_deviation(self):
        good = {"kind": "distance_condensation", "grade": "derived; current orbit, migration not modelled"}
        self.assertNotIsInstance(vd.validate(mantle(MARS_KHAN2022, deviation=good)), Refusal)
        for dev in ({"kind": "migration", "grade": "g"}, {"kind": "none"},
                    {"kind": "distance_condensation", "grade": "derived"}):
            with self.subTest(dev=dev):
                refused(self, vd.validate(mantle(MARS_KHAN2022, deviation=dev)), "input.deviation")


#: Element → oxide factors from standard molar masses (g/mol: O 15.999, Mg 24.305, Al 26.982, Si 28.085, Ca 40.078,
#: Fe 55.845, Na 22.990). A `formula` source (impl P1 follow-up), grade declared; inputs from IUPAC standard atomic
#: weights as commonly tabulated, not read from a cached file.
_FACTORS = {"Mg": ("MgO", 40.304 / 24.305), "Al": ("Al2O3", 101.961 / (2 * 26.982)), "Si": ("SiO2", 60.083 / 28.085),
            "Ca": ("CaO", 56.077 / 40.078), "Fe": ("FeO", 71.844 / 55.845), "Na": ("Na2O", 61.979 / (2 * 22.990))}


def _half_unit(printed: str) -> float:
    """Half a unit in the last printed digit of a value as printed (e.g. «2.35» → 0.005, «2670» → 0.5)."""
    return 0.5 * 10.0 ** -(len(printed.split(".")[1]) if "." in printed else 0)


def _table5_misses(factors) -> list:
    t5 = vd.BSE["table5_cross_check"]
    printed = {**t5["elements_wt"], **{k: v for k, v in t5["elements_ppm"].items()}}
    out = []
    for el, raw in printed.items():
        oxide, f = factors[el]
        scale = 1.0e-4 if el in t5["elements_ppm"] else 1.0              # ppm → wt%
        got = float(raw) * scale * f
        want = vd.BSE["oxides_wt"][oxide]
        col1 = repr(want)
        tol = _half_unit(raw) * scale * f + _half_unit(col1)
        if abs(got - want) > tol:
            out.append((el, oxide, got, want, tol))
    return out


def _with_kind(d, kind):
    d["layers"][1]["composition"]["source_kind"] = kind
    return d


class TTableKey(unittest.TestCase):
    """Note 2 item 2: the printed wt% reach legacy's key path unchanged, so `expected_key` is bit-identical."""

    def _key(self, wt):
        return mc.expected_key(dict(wt))

    def test_key_bit_identical_and_pinned(self):
        for name, wt in (("earth", DMM_WH2005), ("mars", MARS_KHAN2022)):
            with self.subTest(body=name):
                c = comp_of(vd.validate(mantle(wt)), "mantle")
                key = self._key(c.value)
                self.assertEqual(key, self._key(wt))
                self.assertTrue((mc.TABLE_DIR / f"{key}.json").exists(), f"{name}: no committed table for {key}")

    def test_planted_ratio_change_moves_the_key(self):
        for name, wt in (("earth", DMM_WH2005), ("mars", MARS_KHAN2022)):
            with self.subTest(body=name):
                planted = dict(wt, FeO=wt["FeO"] * (1.0 + 1e-9))
                self.assertNotEqual(self._key(planted), self._key(wt))

    def test_recorded_uniform_scaling(self):
        """Recorded case, not a control: all twelve oxides scaled to 100 before the key. cfmasna() renormalises the
        six, so the scale cancels to float error and round(v, 12) absorbs it (r2 on 651970e8). If a rounding flip
        ever moves the key, that is a finding to record, not a case to tune."""
        for name, wt in (("earth", DMM_WH2005), ("mars", MARS_KHAN2022)):
            with self.subTest(body=name):
                s = math.fsum(wt.values())
                scaled = {k: v * 100.0 / s for k, v in wt.items()}
                self.assertEqual(self._key(scaled), self._key(wt))


if __name__ == "__main__":
    unittest.main()
