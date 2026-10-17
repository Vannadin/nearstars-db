# 칸별 띠 항 시험 — 표의 interp_terms 블록 적재 검사(check_term_block)·칸 조회·«read interpolation» 노트와 그 분모(scale), 값 불변 (등록 reg-interp-term §4·§6)
"""Tests of the per-cell band terms on the assemblage read (registration reg-interp-term §4, §6), on
test_assemblage_view's synthetic table, plus the load gate on a shipped table."""
import copy
import math
import unittest

from solver import material_assemblage as ma
from solver import material_registry as mr
from solver import material_view as mv
from solver.tests.test_assemblage_view import PS, TS, record, table

import bisect


def block(tb, cells=None, edit=None):
    """A dense interp_terms block for `tb`: e = (1e-4·(ia + 1), 1e-2 + 1e-4·ib, 2e-3) per cell, the table's floor."""
    ps = sorted({c["p"] for c in tb["cells"]})
    nt = len({c["t"] for c in tb["cells"]})
    rows = cells if cells is not None else [
        [ia, ib, 1e-4 * (ia + 1), 1e-2 + 1e-4 * ib, 2e-3]
        for ib in range(nt - 1) for ia in range(len(ps) - 1) if ps[ia + 1] <= tb["p_dataset"]]
    b = {"source": {"floor": ma.term_floor(tb["cells"], tb["p_dataset"]), "tool_blob": "f" * 40},
         "fields": list(ma.TERM_FIELDS), "cells": rows}
    return edit(b) if edit is not None else b


def with_block(**kw):
    tb = table()
    tb["interp_terms"] = block(tb, **kw)
    return tb


def terms(v, p, t):
    got = v.state(p, t)
    return [n for n in got[2] if isinstance(n, mv.BandNote) and n.edge == "read interpolation"], got


class Gate(unittest.TestCase):
    def test_a_good_block_passes(self):
        ma.check_term_block(with_block(), "interp_terms", sparse=False)

    def test_stops(self):
        tb = table()
        good = block(tb)
        cases = {
            "fields": lambda b: {**b, "fields": ["rho", "c_p", "dtdp"]},
            "floor": lambda b: {**b, "source": {**b["source"], "floor": {**b["source"]["floor"], "dtdp": 1.0}}},
            "have no entry": lambda b: {**b, "cells": b["cells"][1:]},
            "doubled": lambda b: {**b, "cells": b["cells"] + b["cells"][:1]},
            "not a cell up to p_dataset": lambda b: {**b, "cells": b["cells"] + [[len(PS) - 2, 0, 0.0, 0.0, 0.0]]},
            "not finite terms": lambda b: {**b, "cells": [b["cells"][0][:2] + [-1e-3, 0.0, 0.0]] + b["cells"][1:]},
            "not finite terms ": lambda b: {**b, "cells": [b["cells"][0][:2] + [math.nan, 0.0, 0.0]] + b["cells"][1:]},
            "is not \\[ia": lambda b: {**b, "cells": [b["cells"][0][:4]] + b["cells"][1:]}}
        for why, edit in cases.items():
            with self.subTest(why=why):
                t2 = copy.deepcopy(tb)
                t2["interp_terms"] = edit(copy.deepcopy(good))
                with self.assertRaisesRegex(ma.TableStop, why.strip()):
                    ma.check_term_block(t2, "interp_terms", sparse=False)

    def test_sparse_allows_a_subset(self):
        tb = table()
        tb["loop_terms"] = block(tb, cells=[[3, 4, 0.0, 0.5, 0.1]])
        ma.check_term_block(tb, "loop_terms", sparse=True)
        with self.assertRaisesRegex(ma.TableStop, "have no entry"):
            ma.check_term_block(tb, "loop_terms", sparse=False)

    def test_floor_matches_the_generator_rule(self):
        cells = [{"p": float(i), "t": 0.0, "kind": "frozen" if i == 0 else "equilibrium", "rho": float(40 - i),
                  "dtdp_eq": -float(i), "c_p": 1e9, "c_p_eq": float(i)} for i in range(40)]
        cells.append({"p": 1e12, "t": 0.0, "kind": "equilibrium", "rho": 0.0, "dtdp_eq": 0.0, "c_p_eq": 0.0})
        self.assertEqual(ma.term_floor(cells, 100.0), {"rho": 3.0, "dtdp": 2.0, "c_p": 3.0})

    def test_shipped_tables_carry_the_block_and_pass(self):
        """The loader's check_table on the shipped records, and an exported table without the block STOPs."""
        reg = mr.load()
        rid = "silicate_slb_mars_khan2022"
        tb = mv.thaw_plain(reg.tables[rid])
        ps = sorted({c["p"] for c in tb["cells"]})
        nt = len({c["t"] for c in tb["cells"]})
        self.assertEqual(len(tb["interp_terms"]["cells"]), sum(1 for x in ps[1:] if x <= tb["p_dataset"]) * (nt - 1))
        ma.check_term_block(tb, "interp_terms", sparse=False)
        del tb["interp_terms"]
        with self.assertRaisesRegex(ma.TableStop, "carries no interp_terms"):
            ma.check_table(reg.get(rid)["assemblage"], tb)


class Read(unittest.TestCase):
    def cell_of(self, p, t):
        return bisect.bisect_right(PS, p) - 1, bisect.bisect_right(TS, t) - 1

    def test_the_cell_terms_and_scale(self):
        tb = with_block()
        v = ma.view(record(tb["p_dataset"]), tb, 1600.0)
        F = ma.term_floor(tb["cells"], tb["p_dataset"])
        for p, t in ((PS[10] * 1.2, TS[20] + 17.0), (PS[11] * 1.2, TS[20] + 17.0), (PS[10] * 1.2, TS[21] + 17.0)):
            ia, ib = self.cell_of(p, t)
            (n,), got = terms(v, p, t)
            self.assertEqual((n.error, n.dtdp_error, n.c_p_error), (1e-4 * (ia + 1), 1e-2 + 1e-4 * ib, 2e-3))
            r, g, cp, _ = v._solid(p, t)
            self.assertEqual(n.scale, (max(abs(r), F["rho"]), max(abs(g), F["dtdp"]), max(abs(cp), F["c_p"])))
            self.assertIn(f"cell ({ia}, {ib})", n.origin)

    def test_on_a_node_the_reads_own_cell(self):
        """On a P node the term is the cell below's, as _table_read reads it; on a T node the cell above's; below the
        grid's first P node, the first cell (c8 on d2977f99)."""
        tb = with_block()
        v = ma.view(record(tb["p_dataset"]), tb, 1600.0)
        (n,), _ = terms(v, PS[10], TS[20] + 17.0)
        self.assertEqual(n.error, 1e-4 * 10)                                   # ia 9: the cell below P_10
        (n,), _ = terms(v, PS[10] * 1.2, TS[20])
        self.assertEqual(n.dtdp_error, 1e-2 + 1e-4 * 20)                       # ib 20: the cell above T_20
        (n,), _ = terms(v, PS[0] * 0.5, TS[20] + 17.0)
        self.assertEqual(n.error, 1e-4)                                        # ia 0

    def test_floor_holds_a_zero_crossing(self):
        """Near dT/dP = 0 the scale is F_dtdp, not |dT/dP| (the absolute band does not vanish)."""
        tb = with_block()
        F = ma.term_floor(tb["cells"], tb["p_dataset"])
        tb["interp_terms"]["source"]["floor"]["dtdp"] = F["dtdp"]
        v = ma.view(record(tb["p_dataset"]), tb, 1600.0)
        v._solid = lambda p, t: (3300.0, 0.0, 1200.0, [])
        n = v.state(PS[10] * 1.2, 1000.0)[2]
        n = next(x for x in n if isinstance(x, mv.BandNote) and x.edge == "read interpolation")
        self.assertEqual(n.scale[1], F["dtdp"])

    def test_null_reads_zero_and_all_null_no_note(self):
        tb = table()
        ia, ib = self.cell_of(PS[10] * 1.2, TS[20] + 17.0)
        rows = block(tb)["cells"]
        rows = [[a, b, None, 0.05, None] if (a, b) == (ia, ib) else [a, b, None, None, None] if (a, b) == (ia + 1, ib)
                else r for r, (a, b) in ((r, (r[0], r[1])) for r in rows)]
        tb["interp_terms"] = block(tb, cells=rows)
        v = ma.view(record(tb["p_dataset"]), tb, 1600.0)
        (n,), _ = terms(v, PS[10] * 1.2, TS[20] + 17.0)
        self.assertEqual((n.error, n.dtdp_error, n.c_p_error), (0.0, 0.05, 0.0))
        self.assertEqual(terms(v, PS[11] * 1.2, TS[20] + 17.0)[0], [])

    def test_values_unchanged_and_no_block_no_note(self):
        """Control: the block changes notes only; a table without it reads as before, with no such note."""
        a, b = ma.view(record(), table(), 1600.0), ma.view(record(), with_block(), 1600.0)
        for p, t in ((PS[3] * 1.1, 500.0), (PS[10] * 1.2, 1117.0), (PS[20] * 1.3, 1333.0)):
            ga, gb = a.state(p, t), b.state(p, t)
            self.assertEqual(ga[:2], gb[:2])
            self.assertEqual(a._solid(p, t)[:3], b._solid(p, t)[:3])
            self.assertEqual(terms(a, p, t)[0], [])
            self.assertEqual(len(terms(b, p, t)[0]), 1)

    def test_no_term_above_p_dataset(self):
        tb = with_block()
        v = ma.view(record(tb["p_dataset"]), tb, 1600.0)
        v._solid = lambda p, t: (3300.0, 1e-8, 1200.0, [])
        n = v.state(PS[-2] * 1.01, 1000.0)[2]
        self.assertFalse([x for x in n if isinstance(x, mv.BandNote) and x.edge == "read interpolation"])

    def test_summed_with_model_consistency(self):
        """§4 «add»: on a node reading both notes, material_notes sums dT/dP as model consistency × |dT/dP| + e × scale."""
        import types
        from solver import material_notes
        tb = with_block()
        v = ma.view(record(tb["p_dataset"]), tb, 1600.0)
        p, t = PS[10] * 1.2, 1717.0
        got = v.state(p, t)
        mc = next(n for n in got[2] if isinstance(n, mv.BandNote) and n.edge == "dT/dP model consistency")
        ri = next(n for n in got[2] if isinstance(n, mv.BandNote) and n.edge == "read interpolation")
        body = types.SimpleNamespace(layers=[types.SimpleNamespace(id="m")])
        acc = types.SimpleNamespace(profiles={"m": [(0.0, (0.0, p, t, t), 0)]})
        s = next(n for n in material_notes.collect(body, {"m": v}, acc) if n.kind == "material_band_sum")
        self.assertAlmostEqual(s.fields["dtdp"]["band"], mc.dtdp_error * abs(got[1]) + ri.dtdp_error * ri.scale[1],
                               delta=1e-22)


if __name__ == "__main__":
    unittest.main()
