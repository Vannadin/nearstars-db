# D2 읽기 §9 항목 5 의 점검 쪽 시험 — d2·cut 칸에서 s_slopes 의 (s, ∂s/∂lnP, ∂s/∂T) 를 기준 읽기기 s 의 중심 차분과 대어 보고(관문 아님), sub-grid 칸에서는 −(∂s/∂P)/(∂s/∂T) 가 그 읽기의 dT/dP 와 맞는지(Q8), 표 읽기 칸은 None
"""python -B -m unittest solver.tests.test_d2_read_s_path   (gate Python, engine root; no registry load)

D2-read rev 7 §9 item 5: «the d2 and cut Dual against finite differences of the reference reader's s, as a sanity
check, never as the gate», and Q8's subgrid relation (map row c8-12). d2_store.s_slopes(doc, p, t) → (s, ∂s/∂lnP,
∂s/∂T) or None (c8, e901a8ac).
- d2 and cut: s equals the reference's s bit for bit (the same port); the slopes agree with centred differences of the
  reference's s at a relative step of 1e-5 of the cell, to FD_REL, at interior points away from the cell's edges.
- subgrid, inside the sliver: −(∂s/∂lnP / P) / (∂s/∂T) equals the read's dT/dP to SUBGRID_ULP ulp (c8 measured ≤ 3 ulp,
  not bitwise; raised with 68, and this bound stays until 68 rules). FD of s does not apply there: Q8's slopes are the
  read's own α and c_P, not s's derivative.
- a table answer (fallback, limit, no entry, outside the sliver) gives None."""
import math
import unittest
from pathlib import Path

from solver import d2_store as ds
from solver.landing import d2_read_compare as dc

FIX = Path(__file__).resolve().parent / "fixtures" / "d2_reference"
READER = FIX / "d2_store_reader.py"
FD_REL = 1e-6
SUBGRID_ULP = 3
STEP = 1e-5


def interior(doc, per_cell=6):
    """seeded points per population cell, kept 5 % inside the cell's edges so a centred difference stays in it"""
    ps, ts = doc["grid"]["ps"], doc["grid"]["ts"]
    for key, _, p, t in dc.item1_points(doc, 1, per_cell):
        if not key[0].isdigit():
            continue
        j, k = map(int, key.split(","))
        u, v = (p - ps[j]) / (ps[j + 1] - ps[j]), (t - ts[k]) / (ts[k + 1] - ts[k])
        if 0.05 < u < 0.95 and 0.05 < v < 0.95:
            yield j, k, p, t


def ulps(a, b):
    return abs(a - b) / math.ulp(max(abs(a), abs(b)))


class Surface(unittest.TestCase):
    def check(self, name, cls):
        ref = dc.load_reference(READER)
        doc = ref.load((FIX / "stores" / f"{name}.json.gz").read_bytes())
        ps, ts = doc["grid"]["ps"], doc["grid"]["ts"]
        n = 0
        for j, k, p, t in interior(doc):
            a = ref.read(doc, p, t)
            if a["read"] != cls:
                continue
            s, ds_dlnp, ds_dt = ds.s_slopes(doc, p, t)
            self.assertEqual(s, a["values"]["s"])                                  # the same port, bit for bit
            hp, ht = STEP * (ps[j + 1] - ps[j]), STEP * (ts[k + 1] - ts[k])
            fp = (ref.read(doc, p + hp, t)["values"]["s"] - ref.read(doc, p - hp, t)["values"]["s"]) / (2 * hp)
            ft = (ref.read(doc, p, t + ht)["values"]["s"] - ref.read(doc, p, t - ht)["values"]["s"]) / (2 * ht)
            self.assertLessEqual(abs(ds_dlnp - p * fp), FD_REL * max(abs(ds_dlnp), 1e-30) + 1e-12 * abs(s), (name, p, t))
            self.assertLessEqual(abs(ds_dt - ft), FD_REL * max(abs(ds_dt), 1e-30) + 1e-12 * abs(s), (name, p, t))
            n += 1
        self.assertGreater(n, 0, name)

    def test_d2_against_finite_differences(self):
        self.check("d2", "d2")

    def test_cut_on_both_sides_against_finite_differences(self):
        for name in ("cut", "cut_a_virtual"):
            self.check(name, "cut")


class Sliver(unittest.TestCase):
    def test_the_slopes_give_the_reads_dtdp(self):
        ref = dc.load_reference(READER)
        n = 0
        for name in ("subgrid", "subgrid_reversed"):
            doc = ref.load((FIX / "stores" / f"{name}.json.gz").read_bytes())
            for _, _, p, t in list(dc.cell_points(doc)) + list(dc.item1_points(doc, 0, 16)):
                a = ref.read(doc, p, t)
                if a["read"] != "subgrid":
                    continue
                s, ds_dlnp, ds_dt = ds.s_slopes(doc, p, t)
                self.assertLessEqual(ulps(-(ds_dlnp / p) / ds_dt, a["values"]["dtdp"]), SUBGRID_ULP, (name, p, t))
                n += 1
        self.assertGreater(n, 0)


class TableAnswers(unittest.TestCase):
    def test_a_table_answer_has_no_slopes(self):
        ref = dc.load_reference(READER)
        seen = set()
        for name in ("fallback", "limit", "grid136", "subgrid"):
            doc = ref.load((FIX / "stores" / f"{name}.json.gz").read_bytes())
            for _, _, p, t in list(dc.cell_points(doc)) + list(dc.item1_points(doc, 0, 4)):
                a = ref.read(doc, p, t)
                if a["read"] == "table":
                    self.assertIsNone(ds.s_slopes(doc, p, t), (name, p, t, a["why"]))
                    seen.add(a["why"])
        self.assertTrue({"fallback", "limit", "no entry (frozen corner or above p_dataset)",
                         "subgrid cell outside the sliver"} <= seen, seen)


if __name__ == "__main__":
    unittest.main()
