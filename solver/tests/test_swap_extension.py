# 스왑 연장 행의 읽기 쪽 시험 — 연장 블록이 있는 기록은 스왑 곡선의 바깥 끝에서 외삽 0, 인증 행은 곡선 행, 그 밖(모서리 곡선 · 안쪽 끝 · 블록 없는 기록)은 비트 동일
"""The read's half of the swap-extension registration (frozen 8402255e; r2's addenda, with the Q2 ruling: reach 0 only
at a swap curve's true outer ends, an interior check and its mutant)."""
import copy
import unittest

from solver import material_assemblage as ma

L, R = "ol+opx+cpx+gt", "ol+c2c+cpx+gt"
TS = [600.0 + 50.0 * i for i in range(9)]           # 600 … 1000 K


def swap_row(t, pb):
    return {"t": t, "p_lo": pb - 1e8, "p_hi": pb + 1e8, "left": L, "right": R, "class": "swap", "p_b": pb,
            "converged": True, "delta_rho": 0.003, "delta_s": -2.7}


def edge_row(t, pb, over=False):
    """An edge class row with one converged edge: read across unless `over` (then cut)."""
    return {"t": t, "p_lo": pb - 1e8, "p_hi": pb + 1e8, "left": "gt+st", "right": "gt+st+capv", "class": "edge_in",
            "converged": True, "edges": [{"phase": "capv", "converged": True, "p_b": pb, "delta_rho": 1e-4,
                                          "over_tolerance": over}]}


def block(extension=None):
    rows = [swap_row(t, 5e9 + 4e6 * (t - 700.0)) for t in (700.0, 750.0, 800.0)]
    # an edge curve cut on 700–750 and 850–900, read across at 800: two cut runs with interior ends at 750 and 850
    rows += [edge_row(t, 20e9 + 1e6 * (t - 700.0), over=(t != 800.0)) for t in (700.0, 750.0, 800.0, 850.0, 900.0)]
    b = {"status": "exported", "rows": rows}
    if extension is not None:
        b["extension"] = extension
    return b


EXT_NONE = {"rows": [{"t": 650.0, "left": L, "right": R, "class": "swap", "extension": True, "k": 1,
                      "certified": False, "reason": "cells_disagree"}], "rule": {"ext_rows": 2}}


def curves(b):
    cs = ma.build_curves(b, TS)
    return [c for c in cs if c.kind == "swap"], ma._cut_runs(cs), cs


class SwapExtensionRead(unittest.TestCase):
    def test_without_the_block_the_read_extrapolates_as_today(self):
        sw, _, _ = curves(block())
        c = sw[0]
        self.assertIsNotNone(c.p_b_ext(650.0, 100.0))
        self.assertIsNotNone(c.p_b_ext(850.0, 100.0))

    def test_with_the_block_reach_is_zero_at_the_outer_ends(self):
        sw, _, _ = curves(block(copy.deepcopy(EXT_NONE)))
        c = sw[0]
        self.assertIsNone(c.p_b_ext(650.0, 100.0))
        self.assertIsNone(c.p_b_ext(850.0, 100.0))
        ref, _, _ = curves(block())
        for t in (700.0, 725.0, 800.0):                  # on its own rows: bit-identical
            self.assertEqual(c.p_b_ext(t, 100.0), ref[0].p_b_ext(t, 100.0))

    def test_interior_and_edge_run_ends_are_bit_identical(self):
        # r2 Q2: only a swap curve's true outer ends change. The edge curve's cut runs end at 750 (next to the row read
        # across at 800) and at 850: their extrapolation is the same with and without the block. The mutant «reach 0
        # at every run end» makes these differ, so this test is red against it
        _, runs_on, _ = curves(block(copy.deepcopy(EXT_NONE)))
        _, runs_off, _ = curves(block())
        edges_on = [c for c in runs_on if c.kind == "edge"]
        edges_off = [c for c in runs_off if c.kind == "edge"]
        self.assertEqual(len(edges_on), 2)
        for a, b in zip(edges_on, edges_off):
            for t in (650.0, 775.0, 800.0, 825.0, 950.0):
                self.assertEqual(a.p_b_ext(t, 100.0), b.p_b_ext(t, 100.0), (t, a.t0, a.t1))
        self.assertIsNotNone(edges_on[0].p_b_ext(775.0, 100.0))   # an interior run end still extrapolates

    def test_a_certified_extension_row_is_a_row_of_its_curve(self):
        ext = copy.deepcopy(EXT_NONE)
        ext["rows"].append({**swap_row(850.0, 5e9 + 4e6 * 150.0), "extension": True, "k": 1, "certified": True})
        sw, _, _ = curves(block(ext))
        c = sw[0]
        self.assertEqual(c.t1, 850.0)
        self.assertEqual(c.p_b(850.0), 5e9 + 4e6 * 150.0)
        self.assertIsNone(c.p_b_ext(900.0, 100.0))       # past the last certified row: reach 0


if __name__ == "__main__":
    unittest.main()
