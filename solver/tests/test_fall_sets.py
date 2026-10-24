# 출하 떨어짐 집합 꾸러미 시험 — 모든 진입로에 적재기 설치, 없음·낡음의 이름 붙은 거절, 폐포·엔진 조사 도장과 그 변이체, E24 조건부 xfail, 내보내기 (E24 등록 §5)
"""The E24 fall-sets package (registration rewrite/c1-read/reg-e24-fallsets.md §5).

Each test names the rule it pins; each mutant is a planted variant the test shows red. The census drift test runs the
census sweep (a subprocess over every shipped record × every read region kind) and is the slow one."""
import gzip
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from solver import fall_sets as fs, material_assemblage as ma, material_registry as mr
from solver.from_v1 import thaw

REPO = fs.REPO
FIX = Path(__file__).resolve().parent / "fixtures" / "fall_sets"
RECORDS = ("silicate_slb_default_bse", "silicate_slb_earth_dmm_wh2005", "silicate_slb_mars_khan2022")
RID = "silicate_slb_mars_khan2022"


def _run(code, env=None):
    """A fresh interpreter from the repo root (PYTHONPATH=repo): its stdout, stripped."""
    e = dict(os.environ, PYTHONPATH=str(REPO), PYTHONDONTWRITEBYTECODE="1", **(env or {}))
    got = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, env=e, cwd=str(REPO))
    if got.returncode != 0:
        raise AssertionError(got.stderr[-3000:])
    return got.stdout.strip()


def _shipped_present():
    return all(fs.find(fs.directory(), r) for r in RECORDS)


class EntryPoints(unittest.TestCase):
    """Rule 2 (68's pre-flag): a view built through every entry point uses the installed loader."""

    PROBE = "from solver import fall_sets as fs\nprint(M.AssemblageView._fall_set_load is fs.load)"
    ROUTES = {
        "from-import": "from solver import material_assemblage as M\n",
        "dotted-import": "import solver.material_assemblage\nM = solver.material_assemblage\n",
        "importlib": "import importlib\nM = importlib.import_module('solver.material_assemblage')\n",
        "registry": "from solver import material_registry as mr\nmr.MATERIALS_DIR\n"
                    "from solver import material_assemblage as M\n",
        "s-read load check": "from solver import material_assemblage as M\n"
                             "v = M.AssemblageView.__new__(M.AssemblageView)\n",
    }

    def test_every_route_installs_the_loader(self):
        for name, pre in self.ROUTES.items():
            self.assertEqual(_run(pre + self.PROBE), "True", name)

    def test_hook_removed_mutant_is_inert(self):
        """Mutant: the hook taken off sys.meta_path before the import leaves the old loader (the repair inert)."""
        pre = ("import sys, solver\nsys.meta_path.remove(solver._FALL_SETS_HOOK)\n"
               "from solver import material_assemblage as M\n")
        self.assertEqual(_run(pre + self.PROBE), "False")


class Missing(unittest.TestCase):
    """Rule 3: a registry record with no file refuses by name with the repair on; a non-registry id gets {}; the
    repair off reads nothing."""

    def _view(self, rid=RID):
        reg = mr.load(); self.assertIsInstance(reg, mr.Registry)
        return ma.view(thaw(reg.get(RID)), reg.tables[RID], 1600.0), reg

    def _in(self, d, fn):
        old = ma.FALL_SETS_DIR
        ma.FALL_SETS_DIR = d
        try:
            return fn()
        finally:
            ma.FALL_SETS_DIR = old

    @unittest.skipUnless(_shipped_present(), "no shipped sets in solver/materials/fall_sets")
    def test_missing_refuses_on_a_view(self):
        v, _ = self._view()
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ma.TableStop, "fall sets: no file for silicate_slb_mars_khan2022"):
                self._in(tmp, v._fall_set_load)

    @unittest.skipUnless(_shipped_present(), "no shipped sets in solver/materials/fall_sets")
    def test_missing_refuses_at_registry_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            got = self._in(tmp, mr.load)
        self.assertIsInstance(got, mr.LoadStop)
        self.assertEqual(got.id, "material.assemblage_table")
        self.assertIn("fall sets: no file", got.evidence["why"])

    @unittest.skipUnless(_shipped_present(), "no shipped sets in solver/materials/fall_sets")
    def test_repair_off_reads_nothing(self):
        from unittest import mock
        v, _ = self._view()
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(ma, "RHO_BRIDGE", False):
            self.assertEqual(self._in(tmp, v._fall_set_load), {})
            self.assertIsInstance(self._in(tmp, mr.load), mr.Registry)

    @unittest.skipUnless(_shipped_present(), "no shipped sets in solver/materials/fall_sets")
    def test_non_registry_id_gets_none(self):
        v, _ = self._view()
        v.material_id = "planted_not_a_registry_record"
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self._in(tmp, v._fall_set_load), {})


class Shipped(unittest.TestCase):
    """The shipped sets load at HEAD, through the registry, with no refusal; their stamp is this tree's."""

    @unittest.skipUnless(_shipped_present(), "no shipped sets in solver/materials/fall_sets")
    def test_every_shipped_record_loads(self):
        reg = mr.load()
        self.assertIsInstance(reg, mr.Registry, getattr(reg, "evidence", reg))
        for rid in RECORDS:
            v = ma.view(thaw(reg.get(rid)), reg.tables[rid], 1600.0)
            self.assertTrue(v._fall_set_load(), rid)


def _tree_copy(stamp):
    """A temporary root holding solver/*.py, engine/*.py and every stamped data file: the stamp checks against it."""
    tmp = Path(tempfile.mkdtemp())
    for sub in ("solver", "engine"):
        (tmp / sub).mkdir()
        for f in (REPO / sub).glob("*.py"):
            shutil.copy2(f, tmp / sub / f.name)
    for part in ("engine", "solver_data"):
        for p in stamp.get(part, {}):
            if not (tmp / p).exists():
                (tmp / p).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(REPO / p, tmp / p)
    for p in stamp["engine_static"]["data"]:
        if not (tmp / p).exists():
            shutil.copy2(REPO / p, tmp / p)
    return tmp


def _touch(path, old, new):
    t = path.read_text(encoding="utf-8")
    assert old in t, (path, old)
    path.write_text(t.replace(old, new, 1), encoding="utf-8")


class ClosureStamp(unittest.TestCase):
    """Rules 1 and 4 (r2 w1, w2; 68's guards): the solver closure, the static engine half and the census, each checked
    by re-hashing; the mutants each red."""

    @classmethod
    def setUpClass(cls):
        cls.stamp = fs.tree_stamp({"engine": {"engine/rtpress.py": fs.blob(REPO / "engine" / "rtpress.py")},
                                   "solver_data": {}})

    def setUp(self):
        self.root = _tree_copy(self.stamp)
        self.addCleanup(shutil.rmtree, self.root, True)

    def test_closure_lists(self):
        self.assertEqual(fs.closure(), sorted(self.stamp["solver"]))
        self.assertIn("material_view", self.stamp["solver"])
        self.assertIn("engine/rtpress.py", self.stamp["engine"])
        for d2 in ("fold_track", "thermal_stack", "thermal_ale", "hop_track", "body_stack", "samuel_model"):
            self.assertNotIn(f"engine/{d2}.py", self.stamp["engine"], d2)

    def test_the_copy_matches(self):
        fs.check_stamp(self.stamp, self.root)

    def test_material_view_byte_refuses(self):
        """Mutant (r2 w1): a change outside material_assemblage.py, invisible to a read_blob stamp."""
        _touch(self.root / "solver" / "material_view.py", "\n", "\n#\n")
        with self.assertRaisesRegex(ma.TableStop, "material_view.py blob"):
            fs.check_stamp(self.stamp, self.root)

    def test_rtpress_byte_refuses(self):
        """Mutant (r2 w2): an engine module the read loads, invisible to a solver-only stamp."""
        _touch(self.root / "engine" / "rtpress.py", "\n", "\n#\n")
        with self.assertRaisesRegex(ma.TableStop, "engine/rtpress.py blob"):
            fs.check_stamp(self.stamp, self.root)

    def test_d2_module_change_is_no_refusal(self):
        """Control (directing's census ruling): an engine module outside the read (thermal_stack) changes nothing."""
        _touch(self.root / "engine" / "thermal_stack.py", "\n", "\n#\n")
        fs.check_stamp(self.stamp, self.root)

    def test_unswept_branch_module_is_caught_by_the_static_half(self):
        """Mutant (68 guard i): an engine module the read reaches only on a branch the census never visits (here one
        of the static 50 outside this stamp's census, which holds rtpress alone) changes. The static half refuses;
        a census-only stamp, checked the same way, does not (red)."""
        x = next(p for p in self.stamp["engine_static"]["modules"] if p != "engine/rtpress.py")
        _touch(self.root / x, "\n", "\n#\n")
        with self.assertRaisesRegex(ma.TableStop, f"{x} blob"):
            fs.check_stamp(self.stamp, self.root)
        census_only = dict(self.stamp, engine={"engine/rtpress.py": self.stamp["engine"]["engine/rtpress.py"]})
        fs.check_stamp(census_only, self.root)                # the mutant stamp misses it

    def test_switch_refuses(self):
        st = dict(self.stamp, switches="00")
        with self.assertRaisesRegex(ma.TableStop, "engine switches"):
            fs.check_stamp(st, self.root)


@unittest.skipUnless(os.environ.get("NS_SLOW_TESTS") == "1" and _shipped_present(),
                     "the census drift test is the slow tier (≈ 4 min per sweep on the Mac): NS_SLOW_TESTS=1, which the "
                     "stage-A PC block and every landing set; it needs the shipped sets")
class CensusDrift(unittest.TestCase):
    """Rule 6 (directing 10-25): the census sweep re-run over every shipped record × every read region kind loads
    nothing outside the shipped stamp, and every census entry still loads; the mutants each red."""

    # an engine module outside the stamp whose code the read now calls (a bare import is «imported, not read» under
    # directing's ruling of the census's first run; post-registration note 1)
    PLANT_IMPORT = ("from solver import material_assemblage as M\nreal = M.AssemblageView.state\n"
                    "def state(self, p, t, g=None):\n    import thermal_stack\n"
                    "    try:\n        thermal_stack._refused_fields(None)\n    except Exception:\n        pass\n"
                    "    return real(self, p, t, g)\n"
                    "M.AssemblageView.state = state\n")
    PLANT_OPEN = ("from solver import material_assemblage as M\nimport os\nreal = M.AssemblageView.state\n"
                  "F = os.path.join(%r, 'engine', 'chain.yaml')\n"
                  "def state(self, p, t, g=None):\n    open(F).close()\n    return real(self, p, t, g)\n"
                  "M.AssemblageView.state = state\n")

    @classmethod
    def setUpClass(cls):
        f = fs.find(fs.directory(), RECORDS[0])
        cls.shipped = fs._read(f)["stamp"][fs.STAMP_KEY]

    def _drift(self, cen):
        return fs.drift(self.shipped, cen)

    def test_closure_stopping_at_the_module_is_red(self):
        """Mutant: a closure() that stops at material_assemblage.py; the census's own solver modules drift from it."""
        cen = fs.engine_census(RECORDS[2:], fs.directory())
        self.assertEqual([x for x in self._drift(cen) if x.startswith("solver module")], [])
        self.assertTrue([x for x in fs.drift(self.shipped, cen, closure_list=["material_assemblage"])
                         if "material_view" in x])

    def test_census_matches_the_shipped_stamp(self):
        cen = fs.engine_census(RECORDS, fs.directory())
        self.assertEqual(self._drift(cen), [])
        for rid in RECORDS:
            self.assertEqual(sorted(cen["points"][rid]), sorted(fs.REGION_KINDS), rid)
        self.assertTrue(any(p.endswith("rtpress.py") for p in cen["engine"]))

    def test_d2_modules_are_imported_not_read(self):
        """Post-registration note 1: process_state's snapshot imports (samuel_model, samuel_thermal, …) are listed, not
        stamped, so a D2 commit does not void the sets; and their import changes no global of a module the read calls
        (directing 10-25)."""
        cen = self.shipped["census"]
        for m in ("engine/samuel_model.py", "engine/samuel_thermal.py"):
            self.assertIn(m, cen["imported_not_read"])
            self.assertNotIn(m, self.shipped["engine"])
        called = [p for p in cen["engine"] if p.endswith(".py")]
        only = [p for p in cen["imported_not_read"] if p not in self.shipped["engine_static"]["modules"]]
        got = fs.import_side_effects(called, only)
        self.assertEqual(got["changed"], [])

    def test_extra_import_in_the_read_is_red(self):
        cen = fs.engine_census(RECORDS[2:], fs.directory(), plant=self.PLANT_IMPORT)
        self.assertTrue(any("thermal_stack" in x for x in self._drift(cen)))

    def test_extra_data_open_in_the_read_is_red(self):
        cen = fs.engine_census(RECORDS[2:], fs.directory(), plant=self.PLANT_OPEN % str(REPO))
        self.assertTrue(any("chain.yaml" in x for x in self._drift(cen)) or
                        "engine/chain.yaml" in self.shipped["engine_static"]["data"])


class ExportAndFixture(unittest.TestCase):
    """68 n1, n1′: compact = full on a planted pair, always run; the export is byte-stable."""

    def test_compact_equals_full(self):
        full = fs._read(FIX / "planted_fall_record.full.json")
        comp = fs._read(FIX / "compact" / "planted_fall_record.json.gz")
        self.assertEqual(fs.parse_sets(full), fs.parse_sets(comp))
        self.assertEqual(comp["stamp"]["build"], full["stamp"])

    def test_export_is_byte_stable(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            fa = fs.export(FIX / "planted_fall_record.full.json", Path(a), {"fixture": "planted"}, stale_test_only=True)
            fb = fs.export(FIX / "planted_fall_record.full.json", Path(b), {"fixture": "planted"}, stale_test_only=True)
            self.assertEqual(fa.read_bytes(), fb.read_bytes())
            self.assertEqual(fa.read_bytes(), (FIX / "compact" / "planted_fall_record.json.gz").read_bytes())

    def test_build_with_stops_exports_nothing(self):
        d = json.loads((FIX / "planted_fall_record.full.json").read_text())
        d["stops"] = [{"why": "planted"}]
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "x.json"
            f.write_text(json.dumps(d))
            with self.assertRaisesRegex(ma.TableStop, "STOP"):
                fs.export(f, Path(tmp), {}, stale_test_only=True)

    def test_a_build_from_another_tree_never_exports(self):
        """68 B2: the build's own tree is checked at export. A build with no build_tree, or another tree's, refuses;
        the same build with the check off (the stale_test_only mutant) exports (red without the check); stale_test_only
        never writes the shipped directory; a build stamped with this tree exports."""
        d = json.loads((FIX / "planted_fall_record.full.json").read_text())
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "x.json"
            for bt in (None, dict(fs.build_tree(), switches="00")):
                if bt is None:
                    d["stamp"].pop("build_tree", None)
                else:
                    d["stamp"]["build_tree"] = bt
                f.write_text(json.dumps(d))
                with self.assertRaisesRegex(ma.TableStop, "another tree"):
                    fs.export(f, Path(tmp), {})
                self.assertTrue(fs.export(f, Path(tmp), {}, stale_test_only=True).exists())
            with self.assertRaisesRegex(ma.TableStop, "never writes the shipped directory"):
                fs.export(f, fs.DEFAULT_DIR, {}, stale_test_only=True)
            d["stamp"]["build_tree"] = fs.build_tree()
            f.write_text(json.dumps(d))
            self.assertTrue(fs.export(f, Path(tmp), {}).exists())


class E24Conditional(unittest.TestCase):
    """Rule 7 (68 B2): the xfail is decided by the repair flag alone; a refused load errors the test, never an xfail."""

    TEST = "solver.tests.test_assemblage_boundaries.Envelope.test_rho_rises_where_the_table_rises"

    def _unit_outcome(self, env):
        e = dict(os.environ, PYTHONPATH=str(REPO), PYTHONDONTWRITEBYTECODE="1", **env)
        got = subprocess.run([sys.executable, "-B", "-m", "unittest", "-v", self.TEST], capture_output=True,
                             text=True, env=e, cwd=str(REPO))
        # unittest's own end line, not the «… ok» line a warning can split (memory: outcomes from the end blocks)
        end = [x for x in got.stderr.splitlines() if x.startswith(("OK", "FAILED"))]
        if not end:          # the module refused at import (its _shipped raises): an error by name, no test ran
            return "ERROR" if got.returncode != 0 and "the registry refused" in got.stderr else got.stderr[-500:]
        line = end[-1]
        for key, word in (("unexpected successes=", "unexpected success"), ("expected failures=", "expected failure"),
                          ("errors=", "ERROR"), ("failures=", "FAIL"), ("skipped=", "skipped")):
            if key in line:
                return word
        return "ok" if line == "OK" else line

    def test_flag_alone_decides(self):
        src = (Path(__file__).parent / "test_assemblage_boundaries.py").read_text(encoding="utf-8")
        self.assertIn("return unittest.expectedFailure(f) if not ma.RHO_BRIDGE else f", src)

    def test_repair_off_is_the_expected_failure(self):
        self.assertEqual(self._unit_outcome({"NS_RHO_BRIDGE": "0"}), "expected failure")

    @unittest.skipUnless(_shipped_present(), "no shipped sets in solver/materials/fall_sets")
    def test_shipped_default_is_a_plain_pass(self):
        """Under an unconditional decorator (mutant) this is an unexpected success: red."""
        self.assertEqual(self._unit_outcome({}), "ok")

    def test_refused_load_is_never_the_xfail(self):
        """An override directory without the files: the registry refuses and the test errors by name (its module's
        _shipped raises), never «expected failure» or a skip; the mutant condition «sets loaded» would pick the xfail
        here (red)."""
        with tempfile.TemporaryDirectory() as tmp:
            got = self._unit_outcome({"NS_FALL_SETS": tmp})
        self.assertEqual(got, "ERROR")

        def mutant_condition():
            try:
                return not fs.find(Path(tmp), RID)
            except Exception:
                return True
        self.assertTrue(mutant_condition())


if __name__ == "__main__":
    unittest.main()
