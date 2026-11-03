# 시험 환경 계층 조사 시험 — engine/·solver/·scripts/ 가 읽는 환경 변수가 모두 env_tiers.yaml 에 분류돼 있고, 환경으로 걸러지는 시험과 in_gate() 자리가 모두 목록에 있는지(기본 거부)
"""HEAVY-onctl rev 2 P2 (68 clear 3ddfb48c). Runs with no env switch; the landing judge reads the same list (P1).

    solver/.venv/bin/python -m unittest solver.tests.test_env_tiers

Default deny: an env name read and not classed is red, a classed name no longer read is red, a test gated by an env
switch and not listed (or listed and no longer gated) is red, and an in_gate() site count that differs is red."""
import unittest
from pathlib import Path

import yaml

from solver.tests import env_scan as es

ROOT = Path(__file__).resolve().parents[2]
LIST = yaml.safe_load((Path(__file__).with_name("env_tiers.yaml")).read_text())
TREES = ("engine", "solver", "scripts", "derived")     # derived/: the sg-gate tool (68 n1 on the go-live package)


SWITCHES = sorted(n for n, v in LIST["names"].items() if v["class"] in ("tier", "gate"))


def _sources():
    for d in TREES:
        for p in sorted((ROOT / d).rglob("*.py")):
            if ".venv" not in p.parts and "__pycache__" not in p.parts:
                yield p.relative_to(ROOT).as_posix(), p.read_text(errors="replace")


def _script_test(rel):
    return rel.split("/")[0] in ("engine", "scripts") and rel.rsplit("/", 1)[-1].startswith("test_")


def _census(extra=()):
    """extra: planted (relative path, source) pairs, scanned as if they were in the tree."""
    names, sites, gated, scripts = {}, {}, {}, {}
    for rel, src in list(_sources()) + list(extra):
        for n in es.env_names(src):
            names.setdefault(n, []).append(rel)
        c = es.in_gate_sites(src)
        if c and rel != "engine/gate_env.py":                  # gate_env defines in_gate(); its docstring names it
            sites[rel] = c
        if rel.startswith("solver/tests/test_"):
            gated.update(es.gated_tests(src, "solver.tests." + rel.rsplit("/", 1)[-1][:-3]))
        if _script_test(rel):
            r = es.script_reads(src, SWITCHES)
            if r:
                scripts[rel] = r
    return names, sites, gated, scripts


NAMES, SITES, GATED, SCRIPTS = _census()


class Names(unittest.TestCase):
    def test_every_env_name_is_classed(self):
        unclassed = {n: NAMES[n] for n in sorted(set(NAMES) - set(LIST["names"]))}
        self.assertEqual(unclassed, {}, "env names read under engine/, solver/ or scripts/ and not classed")

    def test_every_classed_name_is_read(self):
        self.assertEqual(sorted(set(LIST["names"]) - set(NAMES)), [], "classed names no longer read anywhere")

    def test_classes_are_known(self):
        known = {"tier", "gate", "machine", "path", "behaviour", "internal", "tool"}
        self.assertEqual({n: v["class"] for n, v in LIST["names"].items() if v["class"] not in known}, {})


class GatedTests(unittest.TestCase):
    def test_tier_gates_match_the_list(self):
        """Every test gated by a tier switch is in that tier, and every listed id is still gated by it."""
        for tier in LIST["tiers"].values():
            env = tier.get("gated_by")
            if env is None:
                continue
            with self.subTest(env=env):
                self.assertEqual(sorted(t for t, e in GATED.items() if env in e), sorted(tier["tests"]))

    def test_path_gates_match_the_list(self):
        listed = LIST["tiers"]["paths"]["path_gated"]
        found = {t: sorted(n for n in e if LIST["names"].get(n, {}).get("class") == "path") for t, e in GATED.items()}
        self.assertEqual({t: v for t, v in found.items() if v}, {t: [n] for t, n in listed.items()})

    def test_no_gate_outside_tier_and_path(self):
        """A test gated by a machine, behaviour, internal or tool switch has no landing tier to read it."""
        bad = {t: sorted(n for n in e if LIST["names"].get(n, {}).get("class") not in ("tier", "path"))
               for t, e in GATED.items()}
        self.assertEqual({t: v for t, v in bad.items() if v}, {})


class GateSites(unittest.TestCase):
    def test_in_gate_sites_match_the_list(self):
        self.assertEqual(SITES, LIST["tiers"]["gate"]["in_gate_sites"])

    def test_script_tests_reading_a_switch_are_listed(self):
        """engine/ and scripts/ tests are scripts: one that reads a tier or gate switch directly is listed per file."""
        self.assertEqual(SCRIPTS, LIST["tiers"]["gate"]["script_reads"])


class Controls(unittest.TestCase):
    """Planted sources: each would be red against the list, so the scan cannot pass by seeing nothing."""

    def test_census_sees_the_known_tiers(self):
        self.assertGreaterEqual(len(NAMES), 20)
        self.assertEqual(sum(SITES.values()), 16)          # 12 engine sites + derived/check.py's 2 + test_derived's 2 (sg-gate)
        self.assertGreaterEqual(sum(1 for e in GATED.values() if "NEARSTARS_HEAVY" in e), 11)

    def test_planted_decorator_gate(self):
        src = ('import os, unittest\nFAST = os.environ.get("NS_PLANTED_FAST") == "1"\n'
               'class T(unittest.TestCase):\n    @unittest.skipUnless(FAST, "planted")\n    def test_a(self):\n        pass\n')
        self.assertEqual(es.gated_tests(src, "m"), {"m.T.test_a": {"NS_PLANTED_FAST"}})
        self.assertNotIn("NS_PLANTED_FAST", LIST["names"])

    def test_planted_in_body_skip(self):
        src = ('import os, unittest\nclass T(unittest.TestCase):\n    def test_b(self):\n'
               '        if not os.environ.get("NS_PLANTED_DATA"):\n            self.skipTest("no data")\n')
        self.assertEqual(es.gated_tests(src, "m"), {"m.T.test_b": {"NS_PLANTED_DATA"}})

    def test_planted_setup_skip_and_constant_name(self):
        src = ('import os, unittest\nKEY = "NS_PLANTED_KEY"\nclass T(unittest.TestCase):\n    def setUp(self):\n'
               '        if KEY not in os.environ:\n            raise unittest.SkipTest("no key")\n'
               '    def test_c(self):\n        pass\n')
        self.assertEqual(es.gated_tests(src, "m"), {"m.T.test_c": {"NS_PLANTED_KEY"}})
        self.assertEqual(es.env_names(src), {"NS_PLANTED_KEY"})

    def test_planted_script_form_reads_in_each_tree(self):
        """68 B2: a script-form test in engine/ and one in scripts/ that read a tier switch, and a direct GATE_RUNNING
        read, each make the census differ from the list until listed."""
        heavy = 'import os\nif os.environ.get("NEARSTARS_HEAVY") != "1":\n    print("[SKIP] heavy only")\n'
        gate = 'import os\nif os.environ.get("GATE_RUNNING") == "1":\n    raise SystemExit(1)\n'
        planted = [("engine/test_planted_heavy.py", heavy), ("scripts/refs/test_planted_heavy.py", heavy),
                   ("engine/test_planted_gate.py", gate)]
        _n, sites, _g, scripts = _census(planted)
        self.assertEqual({k: v for k, v in scripts.items() if "planted" in k},
                         {"engine/test_planted_heavy.py": ["NEARSTARS_HEAVY"],
                          "scripts/refs/test_planted_heavy.py": ["NEARSTARS_HEAVY"],
                          "engine/test_planted_gate.py": ["GATE_RUNNING"]})
        self.assertNotEqual(scripts, LIST["tiers"]["gate"]["script_reads"])
        self.assertEqual(sites.get("engine/test_planted_gate.py"), 1)
        self.assertNotEqual(sites, LIST["tiers"]["gate"]["in_gate_sites"])

    def test_planted_in_gate_site(self):
        src = "from engine import gate_env\nif gate_env.in_gate():\n    pass\nelif gate_env.in_gate():\n    pass\n"
        self.assertEqual(es.in_gate_sites(src), 2)


if __name__ == "__main__":
    unittest.main()
