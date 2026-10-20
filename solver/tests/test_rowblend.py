# 행 단위 (c′) 섞기 시험 — 자른 edge 마다 P 연속·C¹, 행 바뀜의 T 연속, 창 밖 비트 동일, 동결 표시 양·음, 버림과 재정규화, 나눗셈 분기 (r2 R1–R7, rowblend 등록 초안)
"""Row-level (c′) blend registration (artifacts ea-rowblend rewrite/rowblend/reg-rowblend-draft.md, delta 2 blob
d533f248), r2's test list R1–R7 for the code read of 303b7795's `_row_blend` / `_flag_reads`, on the composed read.
Each test names the rule clause it pins.

    solver/.venv/bin/python -m unittest solver.tests.test_rowblend
"""
import inspect
import itertools
import math
import textwrap
import unittest
from unittest import mock

from solver import material_assemblage as ma, stepper as st
from solver.tests.test_s_read import _view

RECORDS = ("silicate_slb_default_bse", "silicate_slb_earth_dmm_wh2005", "silicate_slb_mars_khan2022")
FIELDS = ("rho", "dtdp_eq", "c_p")


def _landed(v, p, t):
    got = v._solid(p, t)
    return got[:3] if isinstance(got, tuple) else None


def _fields(v, p, t, s=None):
    """(ρ, dT/dP, c_P) of the landed read and, given an s-reading view, s; None where a read refuses."""
    a = _landed(v, p, t)
    if a is None:
        return None
    if s is None:
        return a
    sv = s.s_path(p, t)
    return None if sv is None or isinstance(sv, st.Stop) else a + (sv.v,)


def _edges(v, t):
    """(curve, x_b, w) of every cut edge at T with P_b_ext inside the dataset."""
    for c in v._cut:
        if c.kind != "edge":
            continue
        pb = c.p_b_ext(t, v._reach)
        if pb is None or not v.ps[0] < pb < v.p_dataset:
            continue
        xb = math.log(pb)
        yield c, xb, v._width(xb)


class R1ContinuityInP(unittest.TestCase):
    """R1 (§2.1, «inside a window the read is a C¹ mix», and §2.2): at every cut edge of the three records, at the
    middle T of its rows, every field (ρ, dT/dP, c_P of the landed read, and s of the s read) is C⁰ across x_b ± 1e-9
    and across each window end x_b ± w (jump ≤ 1e-9 of the field's size), and C¹ at the window ends: the one-sided
    3-point slopes on each side agree to 1e-4 of max(|slope|, the field's size). The C¹ tolerance is the 3-point
    difference's truncation at h = 1e-6·w (h²·f‴, with f‴ up to the blend's own H‴ ~ 1/w³ times the side gap), not the
    rule's."""

    def _check(self, rid):
        v, s = _view(rid, s_read=False), _view(rid)
        n, bad = 0, []
        for c in v._cut:
            if c.kind != "edge":
                continue
            t = c.rows[len(c.rows) // 2]["t"] + (12.5 if len(c.rows) > 1 else 0.0)
            pb = c.p_b_ext(t, v._reach)
            if pb is None or not v.ps[0] < pb < v.p_dataset:
                continue
            xb = math.log(pb)
            w = v._width(xb)
            for x0, kind in ((xb, "x_b"), (xb - w, "end"), (xb + w, "end")):
                got = [_fields(v, math.exp(x0 + e), t, s) for e in (-2e-9, -1e-9, 1e-9, 2e-9)]
                if None in got:
                    continue
                n += 1
                for f in range(len(got[0])):             # continuous: the step over 2e-9 is half the one over 4e-9
                    a2, a1, b1, b2 = (g[f] for g in got)
                    if abs((b1 - a1) - 0.5 * (b2 - a2)) > 1e-9 * max(abs(a1), 1e-30):
                        bad.append((c.id, kind, t, f, a1, b1))
                if kind != "end":
                    continue
                h = 1e-6 * w
                lo = [_fields(v, math.exp(x0 - j * h), t, s) for j in (0, 1, 2)]
                hi = [_fields(v, math.exp(x0 + j * h), t, s) for j in (0, 1, 2)]
                if None in lo or None in hi:
                    continue
                for f in range(len(lo[0])):
                    sl = (3.0 * lo[0][f] - 4.0 * lo[1][f] + lo[2][f]) / (2.0 * h)
                    sr = (-3.0 * hi[0][f] + 4.0 * hi[1][f] - hi[2][f]) / (2.0 * h)
                    if abs(sl - sr) > 1e-4 * max(abs(sl), abs(sr), abs(lo[0][f])):
                        bad.append((c.id, "C1", t, f, sl, sr))
        return n, bad

    def test_every_cut_edge(self):
        for rid in RECORDS:
            n, bad = self._check(rid)
            with self.subTest(rid=rid):
                self.assertGreater(n, 100)
                self.assertEqual(bad[:5], [])


class R2ContinuityInT(unittest.TestCase):
    """R2 (§2.2, «a shared row has one value whichever cell reads it»): where a stencil row's partition gains or loses
    an edge between neighbouring rows (the edge's run ends), the read is C⁰ in T across every node whose stencil holds
    that change, inside the edge's window: at T = node ± 1e-6·ΔT, every field to 1e-9 of its size (plus the slope's
    share over 2e-6·ΔT)."""

    def test_across_row_changes(self):
        n, bad = 0, []
        for rid in RECORDS:
            v, s = _view(rid, s_read=False), _view(rid)
            dt = v.ts[1] - v.ts[0]
            for c in v._cut:
                if c.kind != "edge":
                    continue
                for te in {c.t0, c.t1}:
                    j = v.ts.index(te)
                    for nn in range(j - 2, j + 3):
                        if not 1 <= nn < len(v.ts) - 1:
                            continue
                        tn = v.ts[nn]
                        pb = c.p_b_ext(tn, v._reach)
                        if pb is None or not v.ps[0] < pb < v.p_dataset:
                            continue
                        xb = math.log(pb)
                        p = math.exp(xb + 0.4 * v._width(xb))
                        e = 1e-6 * dt
                        got = [_fields(v, p, tn + k * e, s) for k in (-2, -1, 1, 2)]
                        if None in got:
                            continue
                        n += 1
                        for f in range(len(got[0])):
                            a2, a1, b1, b2 = (g[f] for g in got)
                            if abs((b1 - a1) - 0.5 * (b2 - a2)) > 1e-9 * max(abs(a1), 1e-30):
                                bad.append((rid[13:], c.id, tn, f, a1, b1))
        self.assertGreater(n, 100)
        self.assertEqual(bad[:5], [])


class R3OutsideWindows(unittest.TestCase):
    """R3 (§2.1, «outside windows there is no sum, so those reads are bit for bit today's»): where every listed edge's
    weight clips to exactly 0 or 1, the row blend returns the row's own value bit for bit; and a row whose partition
    holds none of `near` returns `own` itself."""

    def test_clipped_weights_return_own(self):
        v = _view("silicate_slb_default_bse", s_read=False)
        n = 0
        for t in (1500.0, 2200.0, 2950.0):
            k = v.ts.index(t)
            ib = k
            for c, xb, w in _edges(v, t):
                if c not in v._partition(k).cs:
                    continue
                for x in (xb - 1.5 * w, xb + 1.5 * w):        # outside the window: H = 0 or 1 exactly
                    if not v.lnps[0] < x < math.log(v.p_dataset):
                        continue
                    pr = math.exp(x)
                    sides = {cc: (None if (q := cc.p_b_ext(t, v._reach)) is None else (-1 if pr < q else 1))
                             for cc in v._partition(k).cs}
                    r = v._region(k, sides, x)
                    own = v._row_value("rho", k, r, x, False)
                    if own is None:
                        continue
                    self.assertEqual(v._row_blend("rho", k, x, sides, [(c, xb, w)], own), own)
                    n += 1
            del ib
        self.assertGreater(n, 10)

    def test_row_holding_none_of_near_returns_own(self):
        v = _view("silicate_slb_default_bse", s_read=False)
        t = 2200.0
        k = v.ts.index(t)
        other = next(c for c in v._cut if c.kind == "edge" and c not in v._partition(k).cs)
        own = object()
        self.assertIs(v._row_blend("rho", k, 23.0, {}, [(other, 23.0, 0.01)], own), own)


def _frozen_only_by_flag(rid, n_max=20000):
    """Record points whose s path is frozen only through _flag_reads (the read's own rows and blend hold no frozen run):
    (view, p, t, ia, ib)."""
    v = _view(rid)
    out = []
    real = ma.AssemblageView._flag_reads
    for ib in range(1, len(v.ts) - 2):
        if v.ts[ib - 1] > v._t_frozen_max:
            break
        for ia in range(len(v.ps) - 1):
            if v.ps[ia + 1] > v.p_dataset:
                break
            for f in (0.25, 0.5, 0.75):
                p = math.exp(v.lnps[ia] + f * (v.lnps[ia + 1] - v.lnps[ia]))
                t = v.ts[ib] + 0.5 * (v.ts[ib + 1] - v.ts[ib])
                if v._s_path(p, t, p, ia, ib) is not None:
                    continue
                with mock.patch.object(ma.AssemblageView, "_flag_reads", lambda *a, **k: None):
                    if v._s_path(p, t, p, ia, ib) is None:
                        continue
                out.append((v, p, t, ia, ib))
                if len(out) >= n_max:
                    return out
    del real
    return out


class R4FrozenFlagPositive(unittest.TestCase):
    """R4 (§2.4, «every side assignment … read for its frozen runs whatever its weight»): on the records, reads whose own
    rows and blended sides hold no frozen run but whose stencil rows' side regions do are flagged: the s path keeps
    today's read and counts it. Mutant: a side assignment of weight 0 skipped; some of them clear. A forced side
    (`force`) that picks the frozen region flags the read too."""

    @classmethod
    def setUpClass(cls):
        cls.pts = _frozen_only_by_flag("silicate_slb_default_bse")

    def test_flagged_and_counted(self):
        self.assertGreater(len(self.pts), 0)
        v, p, t, ia, ib = self.pts[0]
        n0 = v.s_counts["frozen_stencil_reads"]
        got = v._table_read(p, t)
        self.assertIsInstance(got, tuple)
        self.assertEqual(v.s_counts["frozen_stencil_reads"], n0 + 1)
        off = _view(v.material_id, s_read=False)._table_read(p, t)
        self.assertEqual(got[1], off[1])                 # §3.2: today's read stands

    def test_zero_weight_skipped_mutant_clears_some(self):
        src = textwrap.dedent(inspect.getsource(ma.AssemblageView._flag_reads))
        old = "for sig in itertools.product((-1, 1), repeat=len(ext)):"
        self.assertEqual(src.count(old), 1)
        ns = dict(vars(ma))
        exec(src.replace(old, "for sig in [tuple(sides[c] if sides[c] is not None else 1 for c in ext)]:"), ns)
        with mock.patch.object(ma.AssemblageView, "_flag_reads", ns["_flag_reads"]):
            cleared = sum(1 for v, p, t, ia, ib in self.pts if v._s_path(p, t, p, ia, ib) is not None)
        self.assertGreater(cleared, 0)

    def test_forced_side_picks_the_frozen_region(self):
        """A read beside a cut curve, s path clear on its own sides; forcing the curve to its other side (`force`, as
        §3.1's swap side reads do) makes that side's region the read's own, and where that region holds a frozen run
        the read is flagged. An edge's other side is already read by _flag_reads whatever the force, so the case
        lives on swaps (searched on the records)."""
        for rid in RECORDS:
            v = _view(rid)
            for ib in range(1, len(v.ts) - 2):
                if v.ts[ib - 1] > v._t_frozen_max:
                    break
                t = v.ts[ib] + 0.5 * (v.ts[ib + 1] - v.ts[ib])
                for c in v._cut:
                    pb = c.p_b_ext(t, v._reach)
                    if pb is None or not v.ps[0] < pb < v.p_dataset:
                        continue
                    for side in (-1, 1):
                        p = pb * math.exp(-side * 1e-3)            # on the side opposite the forced one
                        ia = min(max(next(i for i in range(len(v.ps) - 1) if v.ps[i] <= p <= v.ps[i + 1]), 0),
                                 len(v.ps) - 2)
                        if v._s_path(p, t, p, ia, ib) is None:
                            continue
                        if v._s_path(p, t, p, ia, ib, {c: side}) is None:
                            return                       # found: the forced side's frozen run flags the read
        self.fail("no curve whose forced side reaches a frozen run")


class R5FrozenFlagNegative(unittest.TestCase):
    """R5 (§2.4's precheck and window bound): with no frozen node in reach the flag is not set; a row above the table's
    highest frozen T is skipped by the precheck (planted: the bound lowered below a flagged read's rows clears it); and
    a frozen run beyond min(ends) − w_max … max(ends) + w_max is not read (mutant: the bound widened ×10 flags
    reads the rule leaves clear)."""

    def test_no_frozen_node_in_reach(self):
        v = _view("silicate_slb_default_bse")
        ib = next(i for i in range(2, len(v.ts) - 2) if v.ts[i - 2] > v._t_frozen_max)
        t = v.ts[ib] + 10.0
        n = 0
        for ia in range(0, len(v.ps) - 1, 7):
            if v.ps[ia + 1] > v.p_dataset:
                break
            p = math.sqrt(v.ps[ia] * v.ps[ia + 1])
            sv = v._s_path(p, t, p, ia, ib)
            if isinstance(sv, st.Stop):
                continue
            self.assertIsNotNone(sv, (p, t))
            n += 1
        self.assertGreater(n, 10)

    def test_precheck_skips_rows_above_the_bound(self):
        pts = _frozen_only_by_flag("silicate_slb_default_bse", n_max=5)
        self.assertGreater(len(pts), 0)
        v, p, t, ia, ib = pts[0]
        with mock.patch.object(v, "_t_frozen_max", v.ts[max(ib - 1, 0)] - 1.0):
            self.assertIsNotNone(v._s_path(p, t, p, ia, ib))

    def test_window_bound_pinned(self):
        src = textwrap.dedent(inspect.getsource(ma.AssemblageView._flag_reads))
        old = "if min(ends) - wm < x < max(ends) + wm:"
        self.assertEqual(src.count(old), 1)
        ns = dict(vars(ma))
        exec(src.replace(old, "if min(ends) - 10.0 * wm < x < max(ends) + 10.0 * wm:"), ns)
        v = _view("silicate_slb_default_bse")
        more = 0
        for ib in range(1, len(v.ts) - 2):
            if v.ts[ib - 1] > v._t_frozen_max:
                break
            t = v.ts[ib] + 0.5 * (v.ts[ib + 1] - v.ts[ib])
            for ia in range(0, len(v.ps) - 1, 3):
                if v.ps[ia + 1] > v.p_dataset:
                    break
                p = math.sqrt(v.ps[ia] * v.ps[ia + 1])
                if v._s_path(p, t, p, ia, ib) is None:
                    continue
                with mock.patch.object(ma.AssemblageView, "_flag_reads", ns["_flag_reads"]):
                    if v._s_path(p, t, p, ia, ib) is None:
                        more += 1
        self.assertGreater(more, 0)


class R6DropAndRenormalise(unittest.TestCase):
    """R6 (§2.1, «one with no value at all is dropped and counted (blend_drops), with the weights renormalised», and
    §2.2, «side values leave no mark, note or count»): a side region with no run and no _row_reach value adds 1 to
    blend_drops, the result is the kept-weight mean, and the marks and cut_counts reach_rows / side_fallbacks are as
    before the call."""

    def test_planted_drop(self):
        v = _view("silicate_slb_default_bse", s_read=False)
        t = 2200.0
        k = v.ts.index(t)
        c, xb, w = next((c, xb, w) for c, xb, w in _edges(v, t) if c in v._partition(k).cs)
        x = xb + 0.3 * w
        pr = math.exp(x)
        sides = {cc: (None if (q := cc.p_b_ext(t, v._reach)) is None else (-1 if pr < q else 1))
                 for cc in v._partition(k).cs}
        own_r = v._region(k, sides, x)
        own = v._row_value("rho", k, own_r, x, False)
        real_value, real_reach = v._row_value, v._row_reach

        def no_value(f, kk, r, xx, corner):
            return None if r != own_r else real_value(f, kk, r, xx, corner)

        before = (dict(v._marks), {q: v.cut_counts[q] for q in ("reach_rows", "side_fallbacks")},
                  v.cut_counts["blend_drops"])
        with mock.patch.object(v, "_row_value", no_value), mock.patch.object(v, "_row_reach", lambda *a: None):
            got = v._row_blend("rho", k, x, sides, [(c, xb, w)], own)
        self.assertEqual(got, own)                       # only the own assignment kept: its value, renormalised
        self.assertEqual(v.cut_counts["blend_drops"], before[2] + 1)
        self.assertEqual({q: v.cut_counts[q] for q in ("reach_rows", "side_fallbacks")}, before[1])
        self.assertEqual(dict(v._marks), before[0])


class R7Division(unittest.TestCase):
    """R7 (§2.1 as delta 2 writes it, r2 R3): the row blend divides by Σ W of the kept assignments unless that sum is
    exactly 1.0. Pinned on planted rows: two edges at u = ½ (four products of ¼, Σ = 1.0 exactly: no division) and at
    u = 0.05 and 0.1 (Σ = 1 to rounding only, 0.9999999999999999: divided)."""

    def _blend(self, us):
        v = _view("silicate_slb_default_bse", s_read=False)
        curves = [ma._Curve(i, "edge", "x", [{"t": 1000.0, "p_b": 1e9}]) for i in range(len(us))]
        part = ma._Part([(1e9, c) for c in curves])
        sides = {c: -1 for c in curves}
        vals = {}

        def row_value(f, k, r, x, corner):
            return vals.setdefault(r, 1.0 + len(vals))

        near = [(c, -(2.0 * u - 1.0), 1.0) for c, u in zip(curves, us)]    # x = 0: u = ½(κ(0 − x_b)/w + 1)
        with mock.patch.object(v, "_partition", lambda k: part), \
                mock.patch.object(v, "_region", lambda k, sd, x: tuple(sd[c] for c in curves)), \
                mock.patch.object(v, "_row_value", row_value):                 # ρ: κ = 1 (BLEND_SHARP)
            got = v._row_blend("rho", 0, 0.0, sides, near, 7.0)
        hs = [ma._smoothstep(u) for u in us]
        total = kept = 0.0
        for sig in itertools.product((-1, 1), repeat=len(us)):
            wgt = 1.0
            for s_, h in zip(sig, hs):
                wgt *= h if s_ > 0 else 1.0 - h
            y = 7.0 if sig == tuple(sides[c] for c in curves) else vals[sig]
            total += wgt * y
            kept += wgt
        return got, total, kept

    def test_branch(self):
        src = inspect.getsource(ma.AssemblageView._row_blend)
        self.assertEqual(src.count("return total if kept == 1.0 else total / kept"), 1)
        got, total, kept = self._blend((0.5, 0.5))
        self.assertEqual(kept, 1.0)
        self.assertEqual(got, total)                     # no division
        got, total, kept = self._blend((0.05, 0.1))                 # Σ W = 0.9999999999999999
        self.assertNotEqual(kept, 1.0)
        self.assertNotEqual(total, total / kept)
        self.assertEqual(got, total / kept)              # divided


if __name__ == "__main__":
    unittest.main()
