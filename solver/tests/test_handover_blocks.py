# 인계 기록 블록과 그 SLB 기록의 압축표가 짝인지 보는 게이트 시험(prereg-bmcpp 노트 8 §3.4) — 실제 트리의 블록마다 source.compact_sha256 이 그 기록의 assemblage.sha256 과 같아야 함; 파일만 읽으므로 레지스트리 적재(낙하 집합 도장)와 무관
"""prereg-bmcpp note 8 §3.4's gate test, on the tree it runs in: every shipped hand-over block whose id is a shipped
assemblage record carries that record's compact (`source.compact_sha256` == the record's `assemblage.sha256`).

It reads the record files and the hand-over table directly (yaml + the gz table, its sha256 checked against the yaml's
pin), not through material_registry.load, so it runs before and after the load check lands (note 8 §6: L step 0's
§5.4 pre-8d leg runs it on the tree with c0f2a613; it passes there, and fails on 910fd42c, whose blocks carry
4fed99d8's compacts)."""
import gzip
import hashlib
import json
import unittest
from pathlib import Path

import yaml

MATERIALS = Path(__file__).resolve().parents[1] / "materials"
HANDOVER = "silicate_prem_zeng2016"


def pairs(materials=MATERIALS):
    """[(block id, block compact_sha256, record assemblage.sha256 or None)] over the hand-over table's blocks"""
    h = yaml.safe_load((materials / f"{HANDOVER}.yaml").read_text(encoding="utf-8"))
    raw = (materials / h["handover_table"]["file"]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != h["handover_table"]["sha256"]:
        raise AssertionError(f"{h['handover_table']['file']}'s sha256 is not the yaml's pin")
    table = json.loads(gzip.decompress(raw))
    out = []
    for bid, b in sorted(table["blocks"].items()):
        f = materials / f"{bid}.yaml"
        rec = yaml.safe_load(f.read_text(encoding="utf-8")) if f.is_file() else None
        want = (rec.get("assemblage") or {}).get("sha256") if isinstance(rec, dict) and rec.get("kind") == "assemblage" \
            else None
        out.append((bid, (b.get("source") or {}).get("compact_sha256"), want))
    return out


class HandoverBlocks(unittest.TestCase):
    def test_handover_blocks_match_their_compacts(self):
        got = pairs()
        self.assertTrue([p for p in got if p[2] is not None], "no shipped block names a shipped assemblage record")
        for bid, have, want in got:
            if want is None:
                continue
            with self.subTest(block=bid):
                self.assertEqual(have, want, f"{bid}: block compact_sha256 {have} is not the record's {want}")

    def test_a_planted_stale_block_is_seen(self):
        """the control: one block's compact_sha256 moved in a copy of the tree's files goes red"""
        import shutil
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            h = yaml.safe_load((MATERIALS / f"{HANDOVER}.yaml").read_text(encoding="utf-8"))
            (d / "tables").mkdir()
            for bid, _have, _want in pairs():
                if (MATERIALS / f"{bid}.yaml").is_file():
                    shutil.copyfile(MATERIALS / f"{bid}.yaml", d / f"{bid}.yaml")
            table = json.loads(gzip.decompress((MATERIALS / h["handover_table"]["file"]).read_bytes()))
            first = sorted(table["blocks"])[0]
            table["blocks"][first]["source"]["compact_sha256"] = "0" * 64
            raw = gzip.compress(json.dumps(table, sort_keys=True).encode(), mtime=0)
            (d / h["handover_table"]["file"]).write_bytes(raw)
            h["handover_table"]["sha256"] = hashlib.sha256(raw).hexdigest()
            (d / f"{HANDOVER}.yaml").write_text(yaml.safe_dump(h), encoding="utf-8")
            got = {bid: (have, want) for bid, have, want in pairs(d)}
        self.assertNotEqual(*got[first])


if __name__ == "__main__":
    unittest.main()
