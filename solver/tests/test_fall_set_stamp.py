# ρ 보수 fall-set 파일의 출처 표시 시험 — 레코드 sha256·yaml·읽기 폐포 도장이 맞을 때만 실림, 아니면 STOP
"""The fall-set file's stamp (r2 on the swap-extension records): a set built on one record and one read loads only on
them; id and nodes alone are not enough. The read is stamped by its import closure (fall-sets registration rule 4,
r2 w1/w2), and a file with the old read_blob stamp alone refuses by name."""
import json
import os
import tempfile
import unittest
from pathlib import Path

from solver import fall_sets as fs, material_assemblage as ma, material_registry as mr
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
                       "record_yaml_sha256": ma.record_yaml_sha256(RID),
                       fs.STAMP_KEY: fs.tree_stamp({"engine": {}, "solver_data": {}})}}
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

    def test_read_blob_only_stamp_stops(self):
        # every build before the closure stamp: refused by name, never loaded on a blind stamp (r2 w1)
        def old(d):
            d["stamp"].pop(fs.STAMP_KEY)
            d["stamp"]["read_blob"] = ma.read_blob()
        with self.assertRaisesRegex(ma.TableStop, "read_blob stamp; rebuild"):
            self.load(old)

    def test_other_closure_blob_stops(self):
        with self.assertRaisesRegex(ma.TableStop, "material_view.py blob"):
            self.load(lambda d: d["stamp"][fs.STAMP_KEY]["solver"].update(material_view="0" * 40))

    def test_stops_carried_stop(self):
        with self.assertRaisesRegex(ma.TableStop, "build STOP"):
            self.load(lambda d: d.update(stops=[{"why": "planted"}]))

    def test_other_nodes_stop(self):
        with self.assertRaisesRegex(ma.TableStop, "does not match this record's table"):
            self.load(lambda d: d.update(ps=d["ps"][:-1]))

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
