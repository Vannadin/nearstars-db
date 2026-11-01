# fe_prem 복사본 시험 — 두 fe_prem 기록이 이 트리의 엔진 기준 단열선 표(blob 전체 40자리 · 앵커 · 2338 마디)를 그대로 따르는지, 낡은 복사본은 빨개지는지 (FE-PREM-COPY §2(3))
"""FE-PREM-COPY (artifacts pc/ea-fpc/fpc-prereg.frozen.md §2(3)): the class fix, «a stale copy goes red».

For each of solver/materials/fe_prem.yaml and fe_prem_legacy.yaml:
- the table blob its source.formula cites equals the git blob of this tree's engine/reference_adiabats.json, and the
  tool blob equals engine/tools/reference_adiabats.py's, each compared whole (a 40-hex id, never a prefix);
- its adiabat anchor (p, t) and its (lnp, t) nodes equal the table's tables.fe_prem exactly.
The files are read directly, not through the registry, so no registry STOP can stand in front of the check.

Negative control: the same check on 8390fb09's fe_prem.yaml (citing bdc4e181 by its 8-hex prefix, with that table's
nodes) against this tree's table must fail on the blob line and on the nodes; the test is red if the control passes.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_fe_prem_copy
"""
import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path

from solver import yamlio

ROOT = Path(__file__).resolve().parents[2]
RECORDS = ("fe_prem", "fe_prem_legacy")
STALE_AT = "8390fb09b83f8697ea96349f7481994f3e23c786"   # the last tree whose records copy bdc4e181 (E-steps base)


def _blob(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def _table():
    data = (ROOT / "engine/reference_adiabats.json").read_bytes()
    return _blob(data), json.loads(data.decode("utf-8"))["tables"]["fe_prem"]


def failures(text: str) -> list:
    """Every way the record text differs from this tree's table, by kind ("blob", "tool", "anchor", "nodes")."""
    table_blob, tab = _table()
    tool_blob = _blob((ROOT / "engine/tools/reference_adiabats.py").read_bytes())
    a = yamlio.parse(text)["phases"][0]["eos"]["reference"]["adiabat"]
    formula = a["source"]["formula"]
    cited = re.search(r"engine/reference_adiabats\.json \(blob ([0-9a-f]+)\)", formula)
    cited_tool = re.search(r"engine/tools/reference_adiabats\.py \(blob ([0-9a-f]+)\)", formula)
    out = []
    if cited is None or cited.group(1) != table_blob:
        out.append(("blob", cited and cited.group(1), table_blob))
    if cited_tool is None or cited_tool.group(1) != tool_blob:
        out.append(("tool", cited_tool and cited_tool.group(1), tool_blob))
    anc = tab["anchor"]
    if (float(a["anchor"]["p"]), float(a["anchor"]["t"])) != (anc["p_pa"], anc["t_k"]):
        out.append(("anchor", (a["anchor"]["p"], a["anchor"]["t"]), (anc["p_pa"], anc["t_k"])))
    if list(map(float, a["lnp"])) != list(tab["lnp"]) or list(map(float, a["t"])) != list(tab["t"]):
        out.append(("nodes", len(a["lnp"]), len(tab["lnp"])))
    return out


class Copy(unittest.TestCase):
    def test_records_follow_the_table(self):
        for rid in RECORDS:
            with self.subTest(record=rid):
                text = (ROOT / f"solver/materials/{rid}.yaml").read_text(encoding="utf-8")
                self.assertEqual(failures(text), [])

    def test_stale_copy_is_red(self):
        """Control: 8390fb09's fe_prem.yaml (bdc4e181's nodes, an 8-hex citation) fails on the blob and the nodes."""
        r = subprocess.run(["git", "-C", str(ROOT), "show", f"{STALE_AT}:solver/materials/fe_prem.yaml"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        kinds = {f[0] for f in failures(r.stdout)}
        self.assertIn("blob", kinds)
        self.assertIn("nodes", kinds)


if __name__ == "__main__":
    unittest.main()
