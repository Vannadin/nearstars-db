# 고리 칸 항 시험 — 표의 loop_terms 블록 적재 검사(성긴 블록·null·전부 0 금지)·«under-resolved loop» 노트와 분모·테이퍼 구간 (1 − w)·e_loop·보간 항과 합산·값 불변 (등록 §7.3–§7.5)
"""Tests of the «under-resolved loop» term on the assemblage read (registration §7.3–§7.5), on test_assemblage_view's
synthetic table (and test_assemblage_taper's planted hand-over for the zone), plus the shipped records."""
import bisect
import copy
import gzip
import json
import types
import unittest

from solver import material_assemblage as ma
from solver import material_notes
from solver import material_registry as mr
from solver import material_view as mv
from solver.tests import test_assemblage_taper as tt
from solver.tests.test_assemblage_terms import block as iblock
from solver.tests.test_assemblage_view import PS, TS, record, table

P0, T0 = PS[10] * 1.2, TS[20] + 17.0                 # a read inside cell (10, 20)


def cell_of(p, t):
    return bisect.bisect_right(PS, p) - 1, bisect.bisect_right(TS, t) - 1


def lblock(tb, cells=None):
    """A sparse loop_terms block for `tb`: two cells, the table's floor."""
    ia, ib = cell_of(P0, T0)
    rows = cells if cells is not None else [[ia, ib, 2e-3, 3.5, 0.25], [ia + 1, ib, 0.0, 0.8, 0.0]]
    return {"source": {"floor": ma.term_floor(tb["cells"], tb["p_dataset"]), "tool_blob": "1" * 40},
            "fields": list(ma.TERM_FIELDS), "cells": rows}


def with_loop(tb=None, interp=False, **kw):
    tb = tb or table()
    tb["loop_terms"] = lblock(tb, **kw)
    if interp:
        tb["interp_terms"] = iblock(tb)
    return tb


def notes(v, p, t, edge="under-resolved loop"):
    got = v.state(p, t)
    return [n for n in got[2] if isinstance(n, mv.BandNote) and n.edge == edge], got


class Gate(unittest.TestCase):
    def test_a_sparse_block_passes(self):
        tb = with_loop()
        ma.check_term_block(tb, "loop_terms", sparse=True)

    def test_stops(self):
        """check_term_block's own gates on a sparse block (range, floor); null and all-zero are check_table's loop line."""
        ia, ib = cell_of(P0, T0)
        tb = with_loop(cells=[[len(PS) - 2, ib, 0.0, 1.0, 0.0]])
        with self.assertRaisesRegex(ma.TableStop, "not a cell up to p_dataset"):
            ma.check_term_block(tb, "loop_terms", sparse=True)
        tb = with_loop()
        tb["loop_terms"]["source"]["floor"] = {**tb["loop_terms"]["source"]["floor"], "c_p": 1.0}
        with self.assertRaisesRegex(ma.TableStop, "floor"):
            ma.check_term_block(tb, "loop_terms", sparse=True)

    def test_check_table_runs_the_loop_line(self):
        """The shipped mars table passes check_table with its loop block; a null or all-zero cell planted in it STOPs."""
        reg = mr.load()
        rid = "silicate_slb_mars_khan2022"
        asm = reg.get(rid)["assemblage"]
        tb = mv.thaw_plain(reg.tables[rid])
        ma.check_table(asm, tb)
        for bad in ([None, 1.0, 0.0], [0.0, 0.0, 0.0]):
            with self.subTest(bad=bad):
                t2 = copy.deepcopy(tb)
                t2["loop_terms"]["cells"][0] = t2["loop_terms"]["cells"][0][:2] + bad
                with self.assertRaisesRegex(ma.TableStop, "loop_terms: cell"):
                    ma.check_table(asm, t2)


class Read(unittest.TestCase):
    def test_the_cell_terms_and_scale(self):
        tb = with_loop()
        v = ma.view(record(tb["p_dataset"]), tb, 1600.0)
        F = ma.term_floor(tb["cells"], tb["p_dataset"])
        (n,), _ = notes(v, P0, T0)
        self.assertEqual((n.error, n.dtdp_error, n.c_p_error), (2e-3, 3.5, 0.25))
        r, g, cp, _ = v._solid(P0, T0)
        self.assertEqual(n.scale, (max(abs(r), F["rho"]), max(abs(g), F["dtdp"]), max(abs(cp), F["c_p"])))
        self.assertEqual(n.grade, "a grid-unresolved loop")
        self.assertIn("cell (10, 20)", n.origin)
        (n2,), _ = notes(v, PS[11] * 1.2, T0)                      # the second listed cell
        self.assertEqual((n2.error, n2.dtdp_error, n2.c_p_error), (0.0, 0.8, 0.0))

    def test_unlisted_cell_no_note(self):
        """Sparse: a cell the block does not list reads 0, so no note."""
        v = ma.view(record(), with_loop(), 1600.0)
        for p, t in ((PS[12] * 1.2, T0), (P0, TS[21] + 17.0), (PS[3] * 1.1, 500.0)):
            self.assertEqual(notes(v, p, t)[0], [])

    def test_values_unchanged_and_no_block_no_note(self):
        """Control: the block changes notes only."""
        a, b = ma.view(record(), table(), 1600.0), ma.view(record(), with_loop(), 1600.0)
        for p, t in ((PS[3] * 1.1, 500.0), (P0, T0), (PS[11] * 1.2, T0), (PS[20] * 1.3, 1333.0)):
            self.assertEqual(a.state(p, t)[:2], b.state(p, t)[:2])
            self.assertEqual(a._solid(p, t)[:3], b._solid(p, t)[:3])
            self.assertEqual(notes(a, p, t)[0], [])

    def test_beside_read_interpolation_and_summed(self):
        """§7.4: shown beside «read interpolation», and the band is their sum (material_notes, term × scale)."""
        tb = with_loop(interp=True)
        v = ma.view(record(tb["p_dataset"]), tb, 1600.0)
        got = v.state(P0, T0)
        lo = next(n for n in got[2] if isinstance(n, mv.BandNote) and n.edge == "under-resolved loop")
        ri = next(n for n in got[2] if isinstance(n, mv.BandNote) and n.edge == "read interpolation")
        mc = next(n for n in got[2] if isinstance(n, mv.BandNote) and n.edge == "dT/dP model consistency")
        self.assertEqual(lo.scale, ri.scale)
        body = types.SimpleNamespace(layers=[types.SimpleNamespace(id="m")])
        acc = types.SimpleNamespace(profiles={"m": [(0.0, (0.0, P0, T0, T0), 0)]})
        s = next(n for n in material_notes.collect(body, {"m": v}, acc) if n.kind == "material_band_sum")
        self.assertAlmostEqual(s.fields["dtdp"]["band"], mc.dtdp_error * abs(got[1]) + ri.dtdp_error * ri.scale[1]
                               + lo.dtdp_error * lo.scale[1], delta=1e-21)
        self.assertAlmostEqual(s.fields["c_p"]["band"], ri.c_p_error * ri.scale[2] + lo.c_p_error * lo.scale[2],
                               delta=1e-9)


class Taper(unittest.TestCase):
    """§7.4 above p_dataset: the dataset-top cell's loop term, (1 − w)·e_loop in the zone, none past its end."""
    def setUp(self):
        tb = table()
        ia = bisect.bisect_left(PS, tb["p_dataset"]) - 1
        self.ib = bisect.bisect_right(TS, 2017.0) - 1
        tb["loop_terms"] = lblock(tb, cells=[[ia, self.ib, 0.01, 2.0, 0.3]])
        self.ia, self.tb = ia, tb
        self.v = tt.view(tt.handover(), tb)

    def test_zone_carries_one_minus_w(self):
        for f in (0.1, 0.5, 0.9):
            p = tt.PD + f * (tt.PE - tt.PD)
            with self.subTest(f=f):
                (n,), got = notes(self.v, p, 2017.0)
                w = ma._smoothstep(f)
                for x, e in zip((n.error, n.dtdp_error, n.c_p_error), (0.01, 2.0, 0.3)):
                    self.assertAlmostEqual(x, (1.0 - w) * e, delta=1e-15)
                self.assertIn(f"dataset-top cell ({self.ia}, {self.ib})", n.origin)
                r, g, cp, _ = self.v._solid(p, 2017.0)
                F = ma.term_floor(self.tb["cells"], self.tb["p_dataset"])
                self.assertEqual(n.scale, (max(abs(r), F["rho"]), max(abs(g), F["dtdp"]), max(abs(cp), F["c_p"])))

    def test_full_term_below_the_top_and_none_past_the_end(self):
        (n,), _ = notes(self.v, tt.PD * 0.999, 2017.0)              # inside the top cell: the whole term
        self.assertEqual((n.error, n.dtdp_error, n.c_p_error), (0.01, 2.0, 0.3))
        self.assertEqual(notes(self.v, tt.PE * 1.05, 2017.0)[0], [])
        self.assertEqual(notes(self.v, tt.PD + 0.5 * (tt.PE - tt.PD), TS[5] + 17.0)[0], [])   # another T row

    def test_zone_values_unchanged(self):
        bare = tt.view(tt.handover(), table())
        for f in (0.1, 0.5, 0.9):
            p = tt.PD + f * (tt.PE - tt.PD)
            self.assertEqual(bare._solid(p, 2017.0)[:3], self.v._solid(p, 2017.0)[:3])


class Shipped(unittest.TestCase):
    def test_a_loop_cell_on_the_shipped_records(self):
        """Each shipped record: a read at the centre of its largest dT/dP loop cell carries the cell's terms."""
        reg = mr.load()
        for rid in ("silicate_slb_default_bse", "silicate_slb_earth_dmm_wh2005", "silicate_slb_mars_khan2022"):
            with self.subTest(rid=rid):
                tb = mv.thaw_plain(reg.tables[rid])
                ps, ts = sorted({c["p"] for c in tb["cells"]}), sorted({c["t"] for c in tb["cells"]})
                v = ma.view(reg.get(rid), reg.tables[rid], 1600.0)
                ok = 0
                for ia, ib, *e in sorted(tb["loop_terms"]["cells"], key=lambda r: -r[3]):
                    p, t = (ps[ia] * ps[ia + 1]) ** 0.5, 0.5 * (ts[ib] + ts[ib + 1])
                    got = v.state(p, t)
                    if not isinstance(got, tuple):
                        continue                                      # a refusing centre (melt, window): the next
                    (n,) = [x for x in got[2] if isinstance(x, mv.BandNote) and x.edge == "under-resolved loop"]
                    self.assertEqual([n.error, n.dtdp_error, n.c_p_error], e)
                    ok += 1
                    if ok == 3:
                        break
                self.assertEqual(ok, 3)


if __name__ == "__main__":
    unittest.main()
