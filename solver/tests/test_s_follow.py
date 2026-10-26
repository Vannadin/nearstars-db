# s 읽기 경계 추종 형태 시험 — §3 형태(S_FOLLOW)와 사후 노트 1·2: bse ri-out 에서 계단이 x_F(T)를 따라감, 반대 부호 복사본 없음, ρ·오늘 필드 비트 동일, 연속성·Dual·접힘 거절·보호·이음, 변이 M1–M7 빨강
"""Form note §4 (rewrite/rebuild/s-follow-form.md, frozen c15300b7, with post-freeze notes 1 and 2), plants P1–P8 with their
mutants, on the shipped bse record (the ri-out families: parents 38 → 39 fp, 40 → 41 ri). Each mutant is a module switch
of material_assemblage; a mutant read builds its own view, since FOLLOW_JOINS, FOLLOW_RIGHT_LABELS and FOLLOW_XF_PCHIP
act when the families are built."""
import math
import statistics
import unittest
from unittest import mock

from solver import material_assemblage as ma
from solver import material_registry as mr
from solver import stepper as st
from solver.tests.test_assemblage_c1 import _c0_j4, _view

BSE = "silicate_slb_default_bse"
RI_OUT = {38, 39, 40, 41}                                # the full curves of ri-out's two families (diagnosis PA)
_REG = None


def _reg():
    global _REG
    if _REG is None:
        _REG = mr.load()
    return _REG


def _v():
    return _view(_reg(), BSE)


def _ri_fams(v):
    return [f for f in v._families if any(c.parent.id in RI_OUT for c in f.members)]


def _mid(v, t):
    """The two ri-out families' midpoint exp(x_F(t)) in Pa."""
    fs = _ri_fams(v)
    return sum(math.exp(f.x(t, v._reach)) for f in fs) / len(fs)


def _stretches(v, t):
    """PB's scan (diagnosis pab.py): dT/dP at fixed t over 23.30–23.80 GPa every 0.5 MPa; stretches above 10× the
    median |dT/dP|, each (∫ dT/dP dP in K, peak P)."""
    ps = [23.30e9 + k * 0.5e6 for k in range(1001)]
    g = []
    for p in ps:
        d = v.dtdp(p, t)
        g.append(None if isinstance(d, st.Stop) else d * 1e9)
    med = statistics.median(abs(x) for x in g if x is not None)
    runs, cur = [], []
    for p, x in zip(ps, g):
        if x is None or abs(x) <= 10.0 * med:
            continue
        if cur and p - cur[-1][0] > 0.6e6:
            runs.append(cur)
            cur = []
        cur.append((p, x))
    if cur:
        runs.append(cur)
    return [(sum(x for _, x in r) * 0.5e6 / 1e9, max(r, key=lambda z: abs(z[1]))[0]) for r in runs]


def _main_peak(v, t):
    return max(_stretches(v, t), key=lambda e: abs(e[0]))[1]


def _wrong_signed(v, t):
    ss = _stretches(v, t)
    main = max(ss, key=lambda e: abs(e[0]))[0]
    return [e for e in ss if abs(e[0]) > 0.05 and e[0] * main < 0.0]


def _raw(v, p, t):
    """Today's three float fields (ρ, dtdp_eq, c_p) of the exported read, no s blend."""
    pr = max(p, v.ps[0])
    ia = min(max(ma.bisect.bisect_left(v.ps, pr, 1) - 1, 0), len(v.ps) - 2)
    ib = min(max(ma.bisect.bisect_right(v.ts, t) - 1, 0), len(v.ts) - 2)
    got = v._read(p, t, pr, math.log(pr), ia, ib)
    return got if isinstance(got, st.Stop) else got[:3]


def _xf_points(v, t, offs=(-0.5, 0.5)):
    """P at the ri-out midpoint position ± offs·w at t."""
    x = math.log(_mid(v, t))
    w = v._width(x)
    return [math.exp(x + o * w) for o in offs]


class P1StepFollows(unittest.TestCase):
    def test_p1_peak_on_x_f(self):
        v = _v()
        for t in (1860.0, 1875.0, 1890.0, 1896.0):
            self.assertLessEqual(abs(_main_peak(v, t) - _mid(v, t)), 2.0e6, t)
        moved = _main_peak(v, 1875.0) - _main_peak(v, 1900.0)
        self.assertLessEqual(abs(moved - (_mid(v, 1875.0) - _mid(v, 1900.0))), 5.0e6, moved)

    def test_m1_form_off_pinned(self):
        on = _v()
        with mock.patch.object(ma, "S_FOLLOW", False):
            pk = _main_peak(_view(_reg(), BSE), 1875.0)
        self.assertLessEqual(abs(pk - 23.4765e9), 0.5e6, pk)
        self.assertGreater(abs(pk - _mid(on, 1875.0)), 2.0e6)

    def test_m2_joins_off(self):
        """M2 (each piece its own family) is red on P1's own line: off the joined x_F by more than 2 MPa at 1875–1896 K.
        (The form note predicted > 10 MPa; measured on this tree 8.0 MPa at 1896 K, so P1's line is the mutant's.)"""
        on = _v()
        with mock.patch.object(ma, "FOLLOW_JOINS", False):
            m2 = _view(_reg(), BSE)
            for t in (1875.0, 1890.0, 1896.0):
                self.assertGreater(abs(_main_peak(m2, t) - _mid(on, t)), 2.0e6, t)


class P2NoWrongSignedCopies(unittest.TestCase):
    TS = (1825.0, 1840.0, 1860.0, 1875.0)

    def test_p2(self):
        v = _v()
        for t in self.TS:
            self.assertEqual(_wrong_signed(v, t), [], t)

    def test_m1_copies_today(self):
        with mock.patch.object(ma, "S_FOLLOW", False):
            v = _view(_reg(), BSE)
            self.assertTrue(all(_wrong_signed(v, t) for t in self.TS))


class P3Locality(unittest.TestCase):
    GRID = [(p * 1e9, t) for p in (21.0, 22.5, 23.3, 23.48, 23.55, 23.62, 23.7, 24.0, 26.0, 60.0, 124.0)
            for t in (1650.0, 1775.0, 1828.0, 1850.0, 1875.0, 1896.0, 1950.0, 2400.0)]

    def test_i_rho_and_today_fields_bit_identical(self):
        on = _v()
        with mock.patch.object(ma, "S_FOLLOW", False):
            off = _view(_reg(), BSE)
            want = [_raw(off, p, t) for p, t in self.GRID]
        self.assertEqual([_raw(on, p, t) for p, t in self.GRID], want)

    def test_m3_shift_on_rho_breaks_it(self):
        with mock.patch.object(ma, "S_FOLLOW", False):
            off = _view(_reg(), BSE)
            want = [_raw(off, p, t) for p, t in self.GRID]
        with mock.patch.object(ma, "FOLLOW_ON_RHO", True):
            m3 = _view(_reg(), BSE)
            got = [_raw(m3, p, t) for p, t in self.GRID]
        self.assertNotEqual(got, want)

    def test_ii_s_bit_identical_where_no_row_shifts(self):
        on = _v()
        pts = []
        for p, t in self.GRID:
            pr = on.follow_probe(p, t)
            if pr is None or all(ma._at(d, 0.0) for d in pr["rows"].values()):
                pts.append((p, t))
        self.assertGreater(len(pts), 10)
        with mock.patch.object(ma, "S_FOLLOW", False):
            off = _view(_reg(), BSE)
            want = [repr(off.s_path(p, t)) for p, t in pts]
        self.assertEqual([repr(on.s_path(p, t)) for p, t in pts], want)

    def test_iii_s_value_at_a_member_row(self):
        on = _v()
        with mock.patch.object(ma, "S_FOLLOW", False):
            off = _view(_reg(), BSE)
            for t in (1800.0, 1900.0):
                for p in _xf_points(on, t, (-1.5, -0.5, 0.0, 0.5, 1.5)):
                    self.assertEqual(on.s_path(p, t).v, off.s_path(p, t).v, (p, t))


def _c0(f, t, ref):
    return _c0_j4(lambda h: f(t + h) - f(t - h), abs(ref), 1e-9 * abs(ref))


class P4Continuity(unittest.TestCase):
    """C⁰ (J₄) of s, dT/dP and c_P and C¹ of s in T at the form's T sites. A break the form-off read has at the same
    point at least as large is today's (pre-existing, printed and listed for the census), not the form's."""
    T_STAR = (1750.0, 1800.0, 1900.0, 1950.0, 1850.0, 1828.0, 1550.0)

    @staticmethod
    def _jumps(v, t, p):
        s = lambda tt: v.s_path(p, tt).v
        g = lambda tt: v._table_read(p, tt)[1]
        c = lambda tt: v._table_read(p, tt)[2]
        out = {}
        for name, f in (("s", s), ("dtdp", g), ("c_p", c)):
            got = _c0(f, t, f(t))
            out[name] = 0.0 if got["ok"] else abs(got["J"]) / abs(f(t))
        a, b = v.s_path(p, t - 1e-7).dt, v.s_path(p, t + 1e-7).dt
        out["s_dt"] = 0.0 if abs(b - a) <= 1e-6 * abs(a) else abs(b - a) / abs(a)
        return out

    def _c1(self, v, t, p):
        a, b = v.s_path(p, t - 1e-7).dt, v.s_path(p, t + 1e-7).dt
        return abs(b - a) <= 1e-6 * abs(a)

    def test_p4_in_t(self):
        on = _v()
        with mock.patch.object(ma, "S_FOLLOW", False):
            off = _view(_reg(), BSE)
            pts = [(t, p) for t in self.T_STAR for p in _xf_points(on, t)]
            want = {q: self._jumps(off, *q) for q in pts}
        new, old, grow = [], [], []
        for q in pts:
            got = self._jumps(on, *q)
            pr = on.follow_probe(q[1], q[0])
            g_row = pr is not None and pr["ramp"] and q[0] in pr["ramp_rows"]
            for k, j in got.items():
                if j > 0.0:
                    if want[q][k] >= j:
                        old.append((q, k, j, want[q][k]))
                    elif g_row:                          # note 1 r2 n9: x_G piecewise linear at G's own row, under a ramp
                        grow.append((q, k, j, want[q][k]))
                    else:
                        new.append((q, k, j, want[q][k]))
        if old:
            print("P4 member-row class, pre-existing (form-off at least as large):", old)
        if grow:
            print("P4 G-row class (named, note 1 n9):", grow)
        self.assertEqual(new, [])

    def test_p4_in_ln_p_across_phi_edges(self):
        v = _v()
        t = 1875.0
        x = math.log(_mid(v, t))
        w = v._width(x)
        for o in (-2.0, -1.0, 1.0, 2.0):
            p = math.exp(x + o * w)
            s = lambda q: v.s_path(p * math.exp(q), t).v
            self.assertTrue(_c0_j4(lambda h: s(h) - s(-h), abs(s(0.0)), 1e-9 * abs(s(0.0)))["ok"], o)
            dx = lambda q: v.s_path(p * math.exp(q), t).dx       # C¹: J₄ on ∂s/∂lnP (a plain ±h difference measures
            ref = abs(dx(0.0))                                   # curvature, F6)
            self.assertTrue(_c0_j4(lambda h: dx(h) - dx(-h), ref, 1e-6 * ref)["ok"], o)

    def test_m5_piecewise_linear_x_f_kinks(self):
        with mock.patch.object(ma, "FOLLOW_XF_PCHIP", False):
            v = _view(_reg(), BSE)
            bad = [t for t in (1800.0, 1900.0) if not all(self._c1(v, t, p) for p in _xf_points(v, t))]
        self.assertEqual(bad, [1800.0, 1900.0])


class P5Duals(unittest.TestCase):
    TS = (1896.0, 1775.0, 1795.0, 1805.0)

    def _agree(self, v):
        out = []
        for t in self.TS:
            for p in _xf_points(v, t):
                d = v.s_path(p, t)
                ht, hx = 1e-3, 1e-6
                dt = (v.s_path(p, t + ht).v - v.s_path(p, t - ht).v) / (2.0 * ht)
                dx = (v.s_path(p * math.exp(hx), t).v - v.s_path(p * math.exp(-hx), t).v) / (2.0 * hx)
                out.append(abs(d.dt - dt) <= 1e-5 * abs(dt) and abs(d.dx - dx) <= 1e-5 * max(abs(dx), 1e-9))
        return out

    def test_p5(self):
        self.assertTrue(all(self._agree(_v())))

    def test_m4_float_delta_red(self):
        with mock.patch.object(ma, "FOLLOW_DUAL_DELTA", False):
            self.assertFalse(all(self._agree(_view(_reg(), BSE))))


class P6Map(unittest.TestCase):
    """Note 1 §2: every s read checks ∂x_k/∂x ≥ ¼ and refuses by name below it. Around ri-out 68 predicted 0; the grid
    gives six, pinned (note 2). Prints the guard-ramp share and the ri-out families' D_F and cap (note 1 r2 n10)."""

    #: post-freeze note 2: the six fold refusals of the ri-out grid (68's prediction miss; they count in the score),
    #: pinned so that any change in the set shows
    FOLDS = [(23.45e9, 1700.0), (23.5e9, 1700.0), (23.45e9, 1710.0), (23.25e9, 1750.0), (23.3e9, 1750.0),
             (23.2e9, 1760.0)]

    def test_p6_fold_refusals_near_ri_out(self):
        v = _v()
        folds, n, ramp, lo = [], 0, 0, 9.0
        for t in [1700.0 + 10.0 * i for i in range(31)]:
            for k in range(21):
                p = 23.0e9 + k * 0.05e9
                got = v.s_path(p, t)
                if isinstance(got, st.Stop) and "follow map folds" in str(got):
                    folds.append((p, t))
                pr = v.follow_probe(p, t)
                if pr is None or "fold" in pr:
                    continue
                n += 1
                ramp += pr["ramp"]
                for d in pr["rows"].values():
                    lo = min(lo, 1.0 - (d.dx if isinstance(d, ma.Dual) else 0.0))
        fs = _ri_fams(v)
        print(f"P6 ri-out: {n} reads with a family, guard ramp in {ramp} ({ramp / max(n, 1):.1%}), min dx_k/dx "
              f"{lo:.4f}; D_F {[round(f.dbound, 5) for f in fs]}, cap {[round(f.cap, 5) for f in fs]}; "
              f"fold refusals {len(folds)}")
        self.assertEqual([(round(p), t) for p, t in folds], [(round(p), t) for p, t in self.FOLDS])

    def test_fold_refuses_by_name(self):
        """The check itself: with the floor raised past every read's ∂x_k/∂x, a shifted read refuses by name."""
        v = _v()
        with mock.patch.object(ma, "FOLLOW_FOLD_FLOOR", 1.5):
            got = v.s_path(_mid(v, 1875.0), 1875.0)
        self.assertIsInstance(got, st.Stop)
        self.assertIn("follow map folds", str(got))


class P7Guard(unittest.TestCase):
    """A swap G whose own position lies inside an active family's φ support: at x_G the guard holds every row's shift
    at 0 (no row is read across G), the read is not refused; M6 (no guard) shifts there. The site is the first found
    in the shipped records' row pairs (khan, then bse)."""

    def _site(self):
        for rid in ("silicate_slb_mars_khan2022", BSE):
            v = _view(_reg(), rid)
            for ib in range(len(v.ts) - 1):
                t = 0.5 * (v.ts[ib] + v.ts[ib + 1])
                for c in v._cut:
                    if c.kind != "swap" or (pb := c.p_b_ext(t, v._reach)) is None:
                        continue
                    xg = math.log(pb)
                    for f, a, b in v._fam_span:
                        if a <= t <= b and f.psi(t) > 0.0 and (xf := f.x(t, v._reach)) is not None \
                                and 0.0 < abs(xf - xg) < 1.5 * v._width(xf):
                            pr = v.follow_probe(pb, t)
                            if pr is not None:
                                return rid, pb, t
        return None

    def test_p7_guard_and_m6(self):
        site = self._site()
        if site is None:
            self.skipTest("no swap inside an active family's φ support in the shipped records")
        rid, p, t = site
        v = _view(_reg(), rid)
        pr = v.follow_probe(p, t)
        self.assertTrue(all(ma._at(d, 0.0) or abs(d.v if isinstance(d, ma.Dual) else d) == 0.0
                            for d in pr["rows"].values()), (rid, p, t, pr))
        self.assertNotIsInstance(v.s_path(p, t), st.Stop)
        with mock.patch.object(ma, "FOLLOW_GUARD", False):
            m6 = _view(_reg(), rid)
            pr6 = m6.follow_probe(p, t)
        self.assertTrue(any(abs(d.v if isinstance(d, ma.Dual) else d) > 0.0 for d in pr6["rows"].values()))


class P8Joins(unittest.TestCase):
    """C⁰ of s, dT/dP and c_P at every join's gap midpoint. A break the form-off read has at least as large is
    pre-existing (post-freeze note 2: family 165 at 1500 K, 1.688 GPa, 8.48e-4, on the BA-family list), listed and not
    counted, as P4's F5 rule."""

    @staticmethod
    def _j(fn, t):
        ref = fn(t)
        if isinstance(ref, st.Stop):
            return math.inf
        got = _c0(fn, t, ref)
        return 0.0 if got["ok"] else abs(got["J"]) / abs(ref)

    def test_p8_c0_at_every_gap_midpoint(self):
        v = _v()
        with mock.patch.object(ma, "S_FOLLOW", False):
            off = _view(_reg(), BSE)
        new, old = [], []
        for f in v._families:
            for a, b in zip(f.members, f.members[1:]):
                t = 0.5 * (a.t1 + b.t0)
                p = math.exp(f.x(t, v._reach))
                if v.s_path(p, t) is None:                # a frozen stencil: today's read stands, not the form's
                    continue
                for name, i in (("s", None), ("dtdp", 1), ("c_p", 2)):
                    def fn(tt, w=v, i=i):
                        return w.s_path(p, tt).v if i is None else w._table_read(p, tt)[i]
                    j = self._j(fn, t)
                    if j == 0.0:
                        continue
                    with mock.patch.object(ma, "S_FOLLOW", False):
                        jo = self._j(lambda tt, i=i: off.s_path(p, tt).v if i is None else off._table_read(p, tt)[i], t)
                    (old if jo >= j else new).append((f.id, name, t, j, jo))
        if old:
            print("P8 pre-existing (form-off at least as large):", old)
        self.assertEqual(new, [])

    def test_m7_left_labels_only_joins_the_refused(self):
        v = _v()
        right = [r for r in v.family_table["refused"] if r["why"] == "right labels differ"]
        with mock.patch.object(ma, "FOLLOW_RIGHT_LABELS", False):
            m7 = _view(_reg(), BSE)
        joined = lambda w: sum(len(f.members) - 1 for f in w._families)
        if right:
            self.assertGreater(joined(m7), joined(v))
        else:
            self.assertEqual(joined(m7), joined(v))


class FormOffIsCommit2(unittest.TestCase):
    """S_FOLLOW False is the form removed: no family is consulted and the s path is commit 2's."""

    def test_off_reads_no_family(self):
        with mock.patch.object(ma, "S_FOLLOW", False), mock.patch.object(ma.AssemblageView, "_follow",
                                                                           side_effect=AssertionError("called")):
            v = _view(_reg(), BSE)
            v.s_path(23.5e9, 1875.0)


if __name__ == "__main__":
    unittest.main()
