# S3 전이 검사의 출하 판정 — 출하 광물 집합 기록의 transition_check 블록마다 모든 행이 PASS·NOT EVALUABLE 이거나 실재하는 artifacts 커밋의 r2 판정을 단다 (등록 §2.4, 경계 내보내기 범위 노트 Q5)
"""The gate of the S3 transition check (registration §2.4; rewrite/boundary-export-scope.frozen.md §4, r2 Q5).

A shipped assemblage record that carries `assemblage.transition_check` (earth_dmm_wh2005) passes only if every row's
verdict is PASS or NOT EVALUABLE, or the row carries `ruling: <artifacts commit>` (a full 40-hex sha that exists in the
artifacts repo; free text never counts). It is a suite test in the gate the push depends on (Q5 (i)), not a load
check. The artifacts repo is NEARSTARS_ARTIFACTS, else the checkout beside the worktree; a ruling with no repo to check
it against fails, never skips.

Run from the worktree root:  <solver venv>/python -m unittest solver.tests.test_transition_check
"""
import os
import re
import subprocess
import unittest
from pathlib import Path

from solver import material_registry as mr

PASSING = ("PASS", "NOT EVALUABLE")
ARTIFACTS = Path(os.environ.get("NEARSTARS_ARTIFACTS") or Path(__file__).resolve().parents[4] / "NearStars-artifacts")


def failures(block, repo=ARTIFACTS) -> list:
    """Every row of a transition_check block that neither passes nor carries a verifiable ruling, with why."""
    out = []
    for r in block.get("rows", ()):
        if r.get("verdict") in PASSING:
            continue
        c = r.get("ruling")
        if c is None:
            out.append((r.get("transition"), f"verdict {r.get('verdict')} with no ruling"))
        elif not (isinstance(c, str) and re.fullmatch(r"[0-9a-f]{40}", c)):
            out.append((r.get("transition"), f"ruling {c!r} is not a full commit sha"))
        elif not (repo / ".git").exists():
            out.append((r.get("transition"), f"ruling {c} cannot be checked: no artifacts repo at {repo}"))
        elif subprocess.run(["git", "-C", str(repo), "cat-file", "-e", f"{c}^{{commit}}"],
                            capture_output=True).returncode != 0:
            out.append((r.get("transition"), f"ruling {c} is not a commit of the artifacts repo"))
    return out


def shipped_blocks():
    import yaml
    out = {}
    for f in sorted(mr.MATERIALS_DIR.glob("*.yaml")):
        if f.name in mr.NOT_RECORDS:
            continue
        rec = yaml.safe_load(f.read_text(encoding="utf-8"))
        b = (rec.get("assemblage") or {}).get("transition_check")
        if b is not None:
            out[rec["id"]] = b
    return out


class Shipped(unittest.TestCase):
    def test_every_shipped_block_passes_or_is_ruled(self):
        for rid, b in shipped_blocks().items():
            with self.subTest(record=rid):
                self.assertEqual(failures(b), [])
                self.assertEqual(b["passed"], all(r["verdict"] in PASSING for r in b["rows"]))


def head_commit():
    return subprocess.run(["git", "-C", str(ARTIFACTS), "rev-parse", "HEAD"], capture_output=True,
                          text=True).stdout.strip()


class Controls(unittest.TestCase):
    """The planted controls (scope note §4): a FAIL with no ruling, and a ruling to a nonexistent commit, both fail;
    r2's il-drop control (2): the il-dropped export's ak = bg rows, FAIL in a block with no ruling, fail the gate."""

    def block(self, rows):
        return {"rows": rows, "passed": all(r["verdict"] in PASSING for r in rows)}

    def test_fail_without_ruling(self):
        b = self.block([{"transition": "ol=wa", "verdict": "PASS"}, {"transition": "fp+st=bg", "verdict": "FAIL"}])
        self.assertEqual([f[0] for f in failures(b)], ["fp+st=bg"])

    def test_ruling_to_a_nonexistent_commit(self):
        b = self.block([{"transition": "fp+st=bg", "verdict": "FAIL", "ruling": "0" * 40}])
        self.assertIn("not a commit of the artifacts repo", failures(b)[0][1])
        b = self.block([{"transition": "fp+st=bg", "verdict": "FAIL", "ruling": "r2 said fine"}])
        self.assertIn("not a full commit sha", failures(b)[0][1])

    @unittest.skipUnless((ARTIFACTS / ".git").exists(), "the artifacts checkout is beside the worktree")
    def test_ruling_to_a_real_commit_passes(self):
        b = self.block([{"transition": "fp+st=bg", "verdict": "FAIL", "ruling": head_commit()}])
        self.assertEqual(failures(b), [])

    def test_il_drop_rows_fail_the_gate(self):
        """r2's il-drop control, assertion (2): with the il assemblages dropped from the export the tool's ak = bg rows
        FAIL (assertion (1), shown on the PC run of the pinned tool), and placed with no ruling they fail this gate."""
        rows = [{"transition": "ak=bg (fp)", "verdict": "FAIL"}, {"transition": "ak=bg (ri)", "verdict": "FAIL"},
                {"transition": "ol=wa", "verdict": "PASS"}]
        self.assertEqual(sorted(f[0] for f in failures(self.block(rows))), ["ak=bg (fp)", "ak=bg (ri)"])


if __name__ == "__main__":
    unittest.main()
