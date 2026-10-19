# ρ 보수 fall-set 파일의 출처 표시 시험 — 레코드 sha256 과 읽기 blob 이 맞을 때만 실림, 아니면 STOP
"""The fall-set file's stamp (r2 on the swap-extension records): a set built on one record and one read loads only on
them; id and nodes alone are not enough."""
import json
import os
import tempfile
import unittest
from pathlib import Path

from solver import material_assemblage as ma, material_registry as mr
from solver.from_v1 import thaw

RID = "silicate_slb_mars_khan2022"


class FallSetStamp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reg = mr.load()
        cls.rec, cls.tab = reg.get(RID), reg.tables[RID]

    def load(self, edit):
        v = ma.view(thaw(self.rec), self.tab, 1600.0)
        d = {"record": RID, "ps": list(v.ps), "ts": list(v.ts), "stops": [], "sets": {"3": [[1.0, 2.0]]},
             "stamp": {"record_sha256": v.record["assemblage"]["sha256"],
                       "record_yaml_sha256": ma.record_yaml_sha256(RID), "read_blob": ma.read_blob()}}
        edit(d)
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / f"{RID}.json").write_text(json.dumps(d))
            old = ma.FALL_SETS_DIR
            ma.FALL_SETS_DIR = tmp
            try:
                return v._fall_set_load()
            finally:
                ma.FALL_SETS_DIR = old

    def test_matching_stamp_loads(self):
        self.assertEqual(self.load(lambda d: None), {3: [(1.0, 2.0)]})

    def test_other_record_sha_stops(self):
        with self.assertRaisesRegex(ma.TableStop, "record sha256"):
            self.load(lambda d: d["stamp"].update(record_sha256="0" * 64))

    def test_other_record_yaml_stops(self):
        # r2 e843daa8: the yaml carries the extension pin; a set built on another yaml (or before this stamp) is refused
        with self.assertRaisesRegex(ma.TableStop, "record yaml sha256"):
            self.load(lambda d: d["stamp"].update(record_yaml_sha256="0" * 64))
        with self.assertRaisesRegex(ma.TableStop, "record yaml sha256"):
            self.load(lambda d: d["stamp"].pop("record_yaml_sha256"))

    def test_record_yaml_sha_is_the_file(self):
        import hashlib
        self.assertEqual(ma.record_yaml_sha256(RID),
                         hashlib.sha256((mr.MATERIALS_DIR / f"{RID}.yaml").read_bytes()).hexdigest())

    def test_other_read_blob_stops(self):
        with self.assertRaisesRegex(ma.TableStop, "read blob"):
            self.load(lambda d: d["stamp"].update(read_blob="0" * 40))

    def test_unstamped_file_stops(self):
        # the files built before the stamp (rev 3's sets) carry neither key: they no longer load
        with self.assertRaisesRegex(ma.TableStop, "record sha256"):
            self.load(lambda d: d.pop("stamp"))

    def test_read_blob_is_the_module_file(self):
        import hashlib
        data = Path(ma.__file__).read_bytes()
        self.assertEqual(ma.read_blob(), hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest())


if __name__ == "__main__":
    unittest.main()
