# 물질 추가 명령 시험 — 뼈대가 스키마와 어긋나지 않고 FILL 에서 멈추는지, 검사기가 평이한 말로 고칠 법을 말하는지, 출처 등록이 목록에 들어가 인용이 읽히는지 (phase-2 impl note 3 C1–C3)
"""Impl note 3 C1–C3: the scaffold, the checker report, and source registration.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_materials_cli
"""
import contextlib
import copy
import hashlib
import io
import tempfile
import unittest
from collections.abc import Mapping
from pathlib import Path

import yaml

from solver import material_registry as mr
from solver.materials import __main__ as cli
from solver.tests.test_material_registry import GOOD
from solver.yamlio import parse

KINDS = ("single", "branched", "hand_over", "table")


def structure_problems(v, section, path="record") -> list:
    """Keys the scaffold writes that the schema lacks, and required keys it leaves out (values ignored)."""
    spec = mr.SCHEMA[section]
    if not isinstance(v, Mapping):
        return [f"{path}: not a mapping"]
    out = [f"{path}.{k}: unknown" for k in v if k not in spec]
    out += [f"{path}.{k}: required, missing" for k, s in spec.items() if s.get("required") and k not in v]
    for k, x in v.items():
        s = spec.get(k)
        if s is None:
            continue
        sub = s.get("of") or (s["shape"] if s["shape"] in ("constant", "source") else None)
        if sub is None or sub not in mr.SCHEMA:
            continue
        if s["shape"] == "list":
            for i, e in enumerate(x or ()):
                out += structure_problems(e, sub, f"{path}.{k}[{i}]")
        elif s["shape"] != "mapping":
            out += structure_problems(x, sub, f"{path}.{k}")
    return out


class TScaffold(unittest.TestCase):
    def test_scaffold_matches_the_schema_and_stops_on_fill(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                raw = parse(cli.scaffold(kind, "toy"))
                self.assertEqual(structure_problems(raw, "record"), [])
                out = mr.check_record(raw, "toy.yaml")
                self.assertEqual(out.id, "material.placeholder", dict(out.evidence))

    def test_comments_come_from_the_schema(self):
        self.assertIn("the composition the record was fitted to", cli.scaffold("single", "toy"))
        self.assertGreater(len(cli.schema_comments()), 60)

    def test_assemblage_is_refused(self):
        with self.assertRaises(SystemExit):
            cli.scaffold("assemblage", "toy")


class TCheckAndSource(unittest.TestCase):
    def _dir(self, tmp, rec, registered=True):
        d = Path(tmp)
        rows = [{"sha256": "0" * 64, "name": "toy.pdf"}] if registered else []
        (d / "sources.yaml").write_text(yaml.safe_dump({"sources": rows}), encoding="utf-8")
        (d / f"{rec['id']}.yaml").write_text(yaml.safe_dump(rec, sort_keys=False), encoding="utf-8")
        return d

    def _run(self, *a, **k):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cli.check(*a, **k)
        return code, buf.getvalue()

    def test_check_good_and_bad(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = self._dir(tmp, GOOD)
            code, text = self._run([d / "toy.yaml"], d)
            self.assertEqual((code, text.strip()), (0, "toy.yaml: loads"))
        bad = copy.deepcopy(GOOD)
        bad["phases"][0]["edges"].pop("t_min")
        with tempfile.TemporaryDirectory() as tmp:
            d = self._dir(tmp, bad)
            code, text = self._run([d / "toy.yaml"], d)
        self.assertEqual(code, 1)
        self.assertIn("phase toy_solid: edge undeclared — edge = t_min", text)
        self.assertIn("how to fix: The stability field reaches past this window edge", text)

    def test_add_source_registers_and_the_cite_then_loads(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp, "paper.pdf")
            pdf.write_bytes(b"%PDF-1.4 toy paper\n")
            sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
            rec = copy.deepcopy(GOOD)
            for c in [rec["formula_checks"][0]["source"], rec["phases"][0]["field"]["source"]]:
                c.update(cache="paper.pdf", sha256=sha)
            for ph in rec["phases"]:
                for blk in (ph["eos"]["params"].values(), (ph["eos"]["reference"]["p"], ph["eos"]["reference"]["t"]),
                            ph["thermal"]["pressure"].values(), ph["thermal"]["sets"][0]["constants"].values()):
                    for x in blk:
                        x["source"].update(cache="paper.pdf", sha256=sha)
            d = self._dir(tmp, rec, registered=False)
            self.assertEqual(self._run([d / "toy.yaml"], d)[0], 1)            # not yet registered
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                self.assertEqual(cli.add_source(pdf, "Toy 2026, a paper", None, d / "sources.yaml"), 0)
                self.assertEqual(cli.add_source(pdf, "Toy 2026, a paper", None, d / "sources.yaml"), 0)
            self.assertIn("already registered", buf.getvalue())
            self.assertTrue(Path(tmp, "paper.pdf.PROVENANCE.txt").exists())
            self.assertIn(sha, mr.read_manifest(d / "sources.yaml"))
            self.assertEqual(self._run([d / "toy.yaml"], d)[0], 0)

    def test_add_source_never_writes_a_manifest_that_does_not_read_back(self):
        """r2 on fa438fad: with content after the sources list, the append would land in the wrong place; nothing is
        written."""
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp, "paper.pdf")
            pdf.write_bytes(b"%PDF-1.4 another toy\n")
            man = Path(tmp, "sources.yaml")
            before = "sources:\n  - {name: a.pdf, sha256: " + "1" * 64 + "}\nother: 1\n"
            man.write_text(before, encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cli.add_source(pdf, "Toy", None, man), 1)
            self.assertEqual(man.read_text(encoding="utf-8"), before)


if __name__ == "__main__":
    unittest.main()
