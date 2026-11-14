# 스왑 연장 행의 읽기 쪽 시험 — 연장 블록이 있는 기록은 스왑 곡선의 바깥 끝에서 외삽 0, 인증 행은 곡선 행, 그 밖(모서리 곡선 · 안쪽 끝 · 블록 없는 기록)은 비트 동일
"""The read's half of the swap-extension registration (frozen 8402255e; r2's addenda, with the Q2 ruling: reach 0 only
at a swap curve's true outer ends, an interior check and its mutant)."""
import copy
import math
import unittest
from unittest import mock

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




# D2-read §5b (2c) (design 7939346ba; 68 n1–n3): check_boundaries runs H6 on every certified extension row
T_X, PB_X = 850.0, 5.6e9
P_LO, P_HI = PB_X - 1e8, PB_X + 1e8
PS_X = [P_LO - 1e8, P_LO, P_HI, P_HI + 1e8]          # P_LO and P_HI adjacent; P_HI + 1e8 for the non-adjacent case


def _cells(kinds=None):
    """One T row of cells at T_X: L below and at P_LO, R at P_HI and above; `kinds` overrides a cell's kind by P."""
    kinds = kinds or {}
    return [{"p": p, "t": T_X, "assemblage": L if p <= P_LO else R, "kind": kinds.get(p, "solved")} for p in PS_X]


def _ext_row(**over):
    r = {**swap_row(T_X, PB_X), "extension": True, "k": 1, "certified": True}
    r.update(over)
    return r


def _check(rows, kinds=None):
    tb = {"boundaries": {"status": "exported", "rows": [], "extension": {"rows": rows, "rule": {"ext_rows": 2}}}}
    cells = _cells(kinds)
    return ma.check_boundaries(tb, {(c["p"], c["t"]): c for c in cells}, PS_X)


class CertifiedExtensionRowsAreChecked(unittest.TestCase):
    def stops(self, rows, why, kinds=None):
        with self.assertRaises(ma.TableStop) as cm:
            _check(rows, kinds)
        self.assertEqual(cm.exception.check, "boundaries")
        self.assertIn("certified extension row", str(cm.exception))
        self.assertIn(why, str(cm.exception))

    def test_1_a_frozen_side_is_refused(self):
        for p in (P_LO, P_HI):
            self.stops([_ext_row()], "a frozen cell is not a boundary side", kinds={p: "frozen"})

    def test_2_labels_other_than_the_cells_are_refused(self):
        self.stops([_ext_row(left=R, right=L)], f"labels {R!r}/{L!r} are not the cells'")

    def test_3_a_non_adjacent_pair_is_refused(self):
        self.stops([_ext_row(p_hi=P_HI + 1e8)], "not a pair of adjacent columns")

    def test_4_p_b_on_the_pair_end_is_refused(self):
        for pb in (P_LO, P_HI):
            self.stops([_ext_row(p_b=pb)], "is not strictly inside its pair")
        self.stops([_ext_row(p_b=float("nan"))], "is not strictly inside its pair")

    def test_5_each_read_key_missing_is_refused_by_name(self):
        for k in ma._EXT_ROW_KEYS:
            with self.subTest(key=k):
                r = _ext_row()
                del r[k]
                self.stops([r], f"missing {k} (the keys the load path reads)")

    def test_5b_a_certified_row_must_be_a_swap_row(self):
        self.stops([_ext_row(**{"class": "edge_in"})], "must be a swap row, not edge_in")
        self.stops([_ext_row(node_resolved=True)], "must be a swap row, not node-resolved swap")

    def test_6_uncertified_rows_are_not_checked_and_a_good_certified_row_loads(self):
        bad = [_ext_row(p_b=P_LO, left=R, p_hi=P_HI + 1e8, certified=False),
               {"t": 650.0, "left": L, "right": R, "class": "swap", "extension": True, "k": 1, "certified": False,
                "reason": "cells_disagree"}]
        self.assertEqual(_check(bad, kinds={P_LO: "frozen"}), [])
        cs = _check(bad + [_ext_row()])
        self.assertEqual([(c.kind, c.t0, c.t1, c.p_b(T_X)) for c in cs], [("swap", T_X, T_X, PB_X)])

    def test_7_shipped_tables_pass_and_have_no_certified_extension_rows(self):
        seen = 0
        for tid, (_a, tb) in _shipped_tables().items():
            b = tb.get("boundaries") or {}
            if b.get("status") != "exported":
                continue
            seen += 1
            with self.subTest(table=tid):
                ma.check_boundaries(tb, {(c["p"], c["t"]): c for c in tb["cells"]}, sorted({c["p"] for c in tb["cells"]}))
                self.assertEqual(sum(bool(r.get("certified")) for r in (b.get("extension") or {}).get("rows", ())), 0)
        self.assertGreater(seen, 0)

    def test_8_inert_on_the_shipped_records_and_live_on_a_planted_row(self):
        """Directing 11-15 condition 3: while no record carries a certified extension row (every part-1 record), the
        table load never calls the extension check; the planted counterpart shows the spy can count."""
        with mock.patch.object(ma, "check_extension_row", wraps=ma.check_extension_row) as spy:
            tables = _shipped_tables()
            for tid, (a, tb) in tables.items():
                with self.subTest(table=tid):
                    ma.check_table(a, tb)
            self.assertGreater(len(tables), 0)
            self.assertEqual(spy.call_count, 0)
            _check([_ext_row()])
            self.assertEqual(spy.call_count, 1)

    def test_9_the_store_side_runs_the_same_helper(self):
        """D2-read note 3 (5): d2_store.check_extension_h6 calls check_extension_row, one H6 code; its TableStop
        becomes the store's refusal by name."""
        from solver import d2_store as ds
        compact = {"cells": _cells({P_LO: "frozen"})}
        with mock.patch.object(ma, "check_extension_row", wraps=ma.check_extension_row) as spy:
            with self.assertRaises(ds.StoreRefusal) as cm:
                ds.check_extension_h6({"extension": {"rows": [_ext_row()]}}, compact, "x")
        self.assertEqual(spy.call_count, 1)
        self.assertEqual(cm.exception.id, "material.d2_store_edges_rows")
        self.assertIn("a frozen cell is not a boundary side", str(cm.exception))
        self.assertIn("(H6)", str(cm.exception))
        ds.check_extension_h6({"extension": {"rows": [_ext_row()]}}, {"cells": _cells()}, "x")     # control: loads
        for row, why in ((_ext_row(left=R, right=L), "are not the cells'"),
                         (_ext_row(p_hi=P_HI + 1e8), "not a pair of adjacent columns"),
                         (_ext_row(p_b=P_LO), "is not strictly inside its pair"),
                         (_ext_row(**{"class": "edge_in"}), "must be a swap row"),
                         ({k: v for k, v in _ext_row().items() if k != "p_b"}, "missing p_b")):
            with self.subTest(why=why), self.assertRaises(ds.StoreRefusal) as cm:
                ds.check_extension_h6({"extension": {"rows": [row]}}, {"cells": _cells()}, "x")
            self.assertIn(why, str(cm.exception))


def _shipped_tables():
    """{record id: (assemblage block, compact table)} for every shipped assemblage record, read and sha-checked as
    the registry reads them, without the registry's closure-term pins (which this commit's module blob moves until
    part 2's re-pin)."""
    from solver import material_registry as mr
    out = {}
    for f in sorted(mr.MATERIALS_DIR.glob("*.yaml")):
        if f.name in mr.NOT_RECORDS:
            continue
        rec = mr.parse(f.read_text(encoding="utf-8"))
        a = rec.get("assemblage") if isinstance(rec, dict) else None
        if a:
            out[f.stem] = (a, ma.read_table(mr.MATERIALS_DIR / a["file"], a["sha256"]))
    return out


BSE = "silicate_slb_default_bse"
T_STEP = 1568.5                      # in the cell [1550, 1600], next to swap277's reach-0 end at 1600 K


def _bse_view():
    from solver import material_registry as mr
    from solver.tests import test_assemblage_c1 as tc
    reg = mr.load()
    if BSE not in reg.tables or "extension" not in reg.tables[BSE].get("boundaries", {}):
        raise unittest.SkipTest("the regenerated bse record (with the extension block) is not shipped here")
    return tc._view(reg, BSE)


class ReachZeroEnds(unittest.TestCase):
    """Post-freeze note 1 (r2 addendum 4 143d0a96): past a reach-0 end the read takes no side for the curve and each
    stencil row holding it steps at its own P_b(T_k), weighted by its T weight; every such step is a landed event
    (form assemblage_row_step) while the read cell's stencil holds the row. Monotone ρ is the ρ repair's."""

    @classmethod
    def setUpClass(cls):
        cls.v = _bse_view()
        cls.c = next(c for c in cls.v._cut if c.kind == "swap" and c.t0 == 1600.0 and c.stop_lo)
        cls.steps = [x[2] for x in cls.v.transitions() if x[2]["form"] == "assemblage_row_step"]
        #: this curve's own (note 2's coincident-edge pairs add their own events elsewhere, e.g. 16.29 GPa at 1450 K)
        cls.mine = [e for e in cls.steps if cls.v._row_steps[e["id"]][0] is cls.c]

    def events(self, t):
        return sorted(q for e in self.mine if (q := self.v.boundary_pressure(e, t)) is not None)

    def test_events_are_the_holding_rows_own_p_b(self):
        self.assertEqual(self.events(T_STEP), sorted([self.c.p_b(1600.0), self.c.p_b(1650.0)]))
        self.assertEqual(self.events(1525.0), [self.c.p_b(1600.0)])      # 1650 is out of [1500, 1550]'s stencil
        self.assertEqual(self.events(1475.0), [])                          # 1600 is out of [1450, 1500]'s stencil
        self.assertEqual(self.events(1600.0), [])                          # the curve has its P_b there

    def bisect_step(self, p, t, field=0):
        lo, hi = math.log(p) - 1e-4, math.log(p) + 1e-4
        r = lambda x: self.v.state(math.exp(x), t)[field]
        a, b = r(lo), r(hi)
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if abs(r(mid) - a) < abs(r(mid) - b):
                lo = mid
            else:
                hi = mid
        return math.exp(hi)

    def test_the_read_steps_at_the_events(self):
        # the walk lands on the read's discontinuities only if they are where the events say (1568.5 K: row 1650's
        # +47.9 kg/m³ enters with a negative T weight, −0.63; row 1600's with a positive one). The read here is the
        # repair-off read (directing on r2's rev 3 triage 9de49e95): with fall sets loaded, the ρ repair bridges a
        # falling step (test_the_repair_bridges_the_falling_step)
        with mock.patch.object(ma, "RHO_BRIDGE", False):
            self._steps_at_the_events()

    def _steps_at_the_events(self):
        for q in self.events(T_STEP):
            j = self.v.state(q * math.exp(1e-9), T_STEP)[0] - self.v.state(q * math.exp(-1e-9), T_STEP)[0]
            self.assertGreater(abs(j), 0.1, q)
            self.assertAlmostEqual(self.bisect_step(q, T_STEP) / q, 1.0, delta=1e-9)

    def test_the_s_path_steps_at_the_same_events(self):
        for q in self.events(T_STEP):
            j = self.v.s_path(q * math.exp(1e-9), T_STEP).v - self.v.s_path(q * math.exp(-1e-9), T_STEP).v
            self.assertGreater(abs(j), 1e-3, q)

    def test_a_row_step_never_carries_a_coexistence_hook(self):
        # r2 b4d0c0f4 n1: a row step is the read's weighted artefact past a curve's end, not a univariant crossing at
        # that T, so it carries no latent heat; the coexistence segment (reg-coexistence §3.3: a `coexist` factory on
        # each cut swap run) must never attach to it. Today no event has a hook; this pins the row steps' curve dicts
        # to {form, id}, so a hook added to them is red here
        self.assertTrue(self.steps)
        for e in self.steps:
            self.assertEqual(set(e), {"form", "id"}, e)

    def test_no_events_is_red(self):
        # the mutant: no row-step events; a step of the read is then where no event is (the repair-off read, as above)
        with mock.patch.object(ma, "RHO_BRIDGE", False):
            self._no_events_is_red()

    def test_the_repair_bridges_the_falling_step(self):
        """With the ρ repair on and this record's fall set loaded (NS_FALL_SETS, rev 3), a falling step at an event is
        bridged: no read across an event falls; the repair-off read does fall there, so the case is live."""
        if not self.v._fall_set_load():
            self.skipTest("no fall set loaded for bse (NS_FALL_SETS)")
        falls = 0
        for q in self.events(T_STEP):
            lo, hi = q * math.exp(-1e-9), q * math.exp(1e-9)
            with mock.patch.object(ma, "RHO_BRIDGE", False):
                off = self.v.state(hi, T_STEP)[0] - self.v.state(lo, T_STEP)[0]
            with mock.patch.object(ma, "RHO_BRIDGE", True):
                on = self.v.state(hi, T_STEP)[0] - self.v.state(lo, T_STEP)[0]
            if off < -0.1:
                falls += 1
                self.assertGreater(on, -1e-6 * self.v.state(lo, T_STEP)[0], q)
        self.assertGreater(falls, 0)

    def _no_events_is_red(self):
        v = _bse_view()
        with mock.patch.object(type(v), "_row_step_p", lambda self, i, t, ib=None: None):
            got = [q for x in v.transitions() if x[2]["form"] == "assemblage_row_step"
                   if (q := v.boundary_pressure(x[2], T_STEP)) is not None]
        self.assertEqual(got, [])
        q = self.c.p_b(1650.0)
        self.assertGreater(abs(self.v.state(q * math.exp(1e-9), T_STEP)[0] - self.v.state(q * math.exp(-1e-9), T_STEP)[0]),
                           0.1)                                            # the read does step there: unlanded

def _pair850(v):
    """bse's one-row coincident pair at 850 K (ri+cpx+gt+st → ri+gt+capv+st+nal), found by position: the one-row
    events at 850 K landing at the pair's P_b. Ids follow the records' cut runs (168/170 before the across-gap marks,
    153/155 after); the position does not."""
    pb = [c.p_b(850.0) for c in v._events if c.t0 == c.t1 == 850.0 and getattr(c, "was_edge", False)]
    ref = pb[0] if pb else None
    return [i for i, c in enumerate(v._events) if c.t0 == c.t1 == 850.0 and ref is not None and c.p_b(850.0) == ref]


class CoincidentEdgeSwapsReachZero(unittest.TestCase):
    """Swap-extension post-freeze note 2 (r2 6c6c1e94): a coincident edge pair the read re-kinds as a swap takes reach 0
    at both ends, as a swap curve's true ends; past its rows the same edges are read as their own runs, so an
    extrapolated step there would be a second, unlocated representation of one transition."""

    def test_a_one_row_pair_has_no_p_b_past_its_row_and_a_row_step_event(self):
        v = _bse_view()
        pair = _pair850(v)
        self.assertEqual(len(pair), 2, pair)
        for i in pair:                                     # ri+cpx+gt+st → ri+gt+capv+st+nal, one row at 850 K
            c = v._events[i]
            self.assertTrue(getattr(c, "was_edge", False))
            self.assertEqual((c.t0, c.t1), (850.0, 850.0))
            self.assertTrue(c.stop_lo and c.stop_hi)
            for t in (800.0, 825.0, 875.0, 900.0):
                self.assertIsNone(c.p_b_ext(t, v._reach), t)
            self.assertIsNotNone(c.p_b_ext(850.0, v._reach))
        steps = [x[2] for x in v.transitions() if x[2]["form"] == "assemblage_row_step"]
        mine = [e for e in steps if v._row_steps[e["id"]][0] in [v._events[i] for i in pair]]
        self.assertEqual(len(mine), 2)
        for e in mine:
            self.assertEqual(v.boundary_pressure(e, 825.0), v._events[pair[0]].p_b(850.0))
            self.assertIsNone(v.boundary_pressure(e, 850.0))        # the pair has its own P_b there
        self.assertEqual([c for c in v._cut if c.kind == "swap" and not (c.stop_lo and c.stop_hi)], [])

    def test_flags_left_to_build_curves_is_red(self):
        # the mutant: flags only where build_curves sets them (before the re-kinding) — the pair extrapolates its step
        import types
        from solver import material_registry as mr
        from solver.from_v1 import thaw
        src = open(ma.__file__, encoding="utf-8").read()
        self.assertEqual(src.count("                        if extension:\n"), 1)
        mut = types.ModuleType("material_assemblage_flags_before_rekind")
        mut.__file__ = ma.__file__
        exec(compile(src.replace("                        if extension:\n", "                        if False:\n"),
                     ma.__file__, "exec"), mut.__dict__)
        reg = mr.load()
        if "extension" not in reg.tables[BSE].get("boundaries", {}):
            raise unittest.SkipTest("the regenerated bse record is not shipped here")
        pb = _bse_view()._events[_pair850(_bse_view())[0]].p_b(850.0)
        v = mut.view(thaw(reg.get(BSE)), reg.tables[BSE], 1600.0)
        (i,) = [i for i, c in enumerate(v._events) if c.t0 == c.t1 == 850.0 and c.p_b(850.0) == pb][:1]
        c = v._events[i]
        self.assertFalse(c.stop_lo or c.stop_hi)
        self.assertIsNotNone(c.p_b_ext(800.0, v._reach))       # the extrapolated step 50 K past its only row


if __name__ == "__main__":
    unittest.main()
