# 광물 집합 읽기 C¹ 항목(5d998d40) 시험 — 실제 기록에서 변 P_b 의 C⁰, 곁 읽기가 남기는 표시·노트 없음, 꺾임 조사 부분집합의 이름 붙은 부류·한도
"""The C¹ read's acceptance in the suite, on the shipped records (a TIP; skipped on the engine branch alone).
- C⁰ at every cut edge (68 ruling 1 (1)): across x_b the read's step over ±1e-9 in ln P is half its step over ±2e-9
  (only the slope's share, no jump), to 1e-9 of the field's size there, in all three fields, every third row,
  wherever neither side refuses. The blend's C⁰ there rests on the own read equalling the same-side side read.
- Side reads leave nothing on the read (ruling 1 (3)): inside the windows a read's notes and counts are its own read's
  (the blend switched off), and a point read cold (fresh view) and warm (after the other points) is the same.
- Slope jumps (68 ruling 4): kinkscan's subset of lines finds no kink outside the named classes or above their bounds;
  the full scan does the same as a NEARSTARS_HEAVY test, run once per landing.

Run from the worktree root:  <solver venv>/python -m unittest solver.tests.test_assemblage_c1
"""
import math
import os
import unittest

from solver import material_assemblage as ma, material_registry as mr
from solver.from_v1 import thaw
from solver.tests import kinkscan as ks

HEAVY = os.environ.get("NEARSTARS_HEAVY") == "1"
#: the in-suite kink subset (68 ruling 4, Q4): per record two fixed-T lines that hold T-clip kinks and one fixed-P line
#: (the full scan's line nearest the given GPa) that holds a T-row-line kink, at v4
SUBSET = {"silicate_slb_default_bse": ((1068.5, 1568.5), (0.9606,)),
          "silicate_slb_earth_dmm_wh2005": ((1668.5, 2268.5), (1.4193,)),
          "silicate_slb_mars_khan2022": ((1668.5, 1768.5), (120.3063,))}

RECORDS = ("silicate_slb_default_bse", "silicate_slb_earth_dmm_wh2005", "silicate_slb_mars_khan2022")


def _shipped():
    reg = mr.load()
    return all(reg.get(r) is not None and r in reg.tables for r in RECORDS)


def _view(reg, rid):
    return ma.view(thaw(reg.get(rid)), reg.tables[rid], 1600.0)


class C1(unittest.TestCase):
    @unittest.skipUnless(_shipped(), "no shipped assemblage records with their tables")
    def test_continuous_at_every_cut_edge(self):
        reg = mr.load()
        for rid in RECORDS:
            v = _view(reg, rid)
            n, bad = 0, []
            for c in v._cut:
                if c.kind != "edge":
                    continue
                for r in c.rows[::3]:
                    for t in (r["t"], r["t"] + 17.0):
                        pb = c.p_b_ext(t, v._reach)
                        if pb is None or not v.ps[0] < pb < v.p_dataset:
                            continue
                        got = [v._solid(pb * math.exp(e), t) for e in (-2e-9, -1e-9, 1e-9, 2e-9)]
                        far = [v._solid(pb * math.exp(e * v._width(math.log(pb))), t) for e in (-0.5, 0.5)]
                        if not all(isinstance(g, tuple) for g in got + far):
                            continue                         # a refusal boundary
                        n += 1
                        for f in range(3):
                            a2, a1, b1, b2 = (g[f] for g in got)
                            scale = max(abs(a1), abs(far[0][f]), abs(far[1][f]))   # the field's size here, not a 0 crossing
                            # continuous: the step across x_b over 2e-9 is half the one over 4e-9 (the slope's share)
                            if abs((b1 - a1) - 0.5 * (b2 - a2)) > 1e-9 * scale:
                                bad.append((c.id, pb / 1e9, t, f, a1, b1))
            self.assertGreater(n, 100, rid)
            self.assertEqual(bad[:5], [], rid)

    @unittest.skipUnless(_shipped(), "no shipped assemblage records with their tables")
    def test_side_reads_leave_no_note(self):
        """Inside the windows, a read's notes and counts are its own read's: the same as with the blend switched off
        (side reads on scratch marks, 68 ruling 1 (3)); and a point read cold (fresh view) and warm (after the others)
        is the same, values and notes."""
        reg = mr.load()
        for rid in RECORDS:
            v = _view(reg, rid)
            pts = []
            for c in v._cut:
                if c.kind != "edge":
                    continue
                for r in c.rows[::3]:
                    xb = math.log(r["p_b"])
                    w = v._width(xb)
                    for f in (-0.6, -0.2, 0.2, 0.6):
                        p = math.exp(xb + f * w)
                        if v.ps[0] < p < v.p_dataset:
                            pts.append((p, r["t"] + 11.0))
            self.assertGreater(len(pts), 300, rid)
            on, off = _view(reg, rid), _view(reg, rid)
            off._blend_sides = lambda f, x, t, ib, sides, near, own: own
            keys = [k for k in on.cut_counts if k not in ("corrections", "blend_drops")]
            for p, t in pts:
                a, b = on.state(p, t), off.state(p, t)
                if isinstance(a, tuple) and isinstance(b, tuple):
                    self.assertEqual([repr(n) for n in a[2]], [repr(n) for n in b[2]], (rid, p, t))
                else:
                    self.assertEqual(type(a), type(b), (rid, p, t))
            self.assertEqual({k: on.cut_counts[k] for k in keys}, {k: off.cut_counts[k] for k in keys}, rid)
            for p, t in pts[:40]:                            # cold against warm
                self.assertEqual(repr(_view(reg, rid).state(p, t)), repr(on.state(p, t)), (rid, p, t))

    @unittest.skipUnless(_shipped(), "no shipped assemblage records with their tables")
    def test_kinks_named_and_bounded_subset(self):
        reg = mr.load()
        named = 0
        for rid, (t_lines_at, p_gpa) in SUBSET.items():
            v = _view(reg, rid)
            _ts, ps = ks.full_lines(v)
            p_lines = [min(ps, key=lambda q: abs(q / 1e9 - g)) for g in p_gpa]
            kinks = ks.scan(v, p_lines=t_lines_at, t_lines=p_lines)
            self.assertEqual(ks.violations(kinks), [], rid)
            named += len(kinks)
        self.assertGreater(named, 0)                         # the scan sees the named classes it bounds

    @unittest.skipUnless(HEAVY and _shipped(), "NEARSTARS_HEAVY=1 (the full kink scan, about 25 min per record)")
    def test_kinks_named_and_bounded_full(self):
        reg = mr.load()
        for rid in RECORDS:
            v = _view(reg, rid)
            ts, ps = ks.full_lines(v)
            self.assertEqual(ks.violations(ks.scan(v, p_lines=ts, t_lines=ps)), [], rid)


if __name__ == "__main__":
    unittest.main()


class RunEnd(unittest.TestCase):
    """The truth check's run-end rule (item 5d998d40; 68 ruling on the bump): an open run end's node slope s_n is PCHIP's
    end slope capped at 4|s∞|, s∞ = minmod(PCHIP end, the run's gentlest secant); past the end, s∞'s line plus the bump
    (s_n − s∞)·d(1 − d/L)² within L = END_BUMP·h_end. Mutants: L = 0 (a kink at the node), no cap (the bump turns),
    the linear ramp with its offset (bse 2125 K falls past 21.42 GPa)."""

    XS, YS = [0.0, 1.0, 2.0, 3.0], [10.0, 20.0, 21.0, 22.0]       # a steep first segment: s_e 14.5, s∞ 1, s_n 4

    def _d(self, run, x, h):
        return (run.value(x + h) - run.value(x - h)) / (2.0 * h)

    def test_bump_shape(self):
        run = ma._Run(list(self.XS), list(self.YS), [0, 1, 2, 3], 0)
        self.assertEqual((run.se_lo, run.f_lo, run.m_lo), (14.5, 1.0, 4.0))
        x0, L, h = self.XS[0], run.L_lo, 1e-6
        self.assertEqual(L, ma.END_BUMP * 1.0)
        # the node: the same slope s_n from the run's end segment and from the bump
        inner = (run.value(x0 + h) - run.value(x0)) / h
        outer = (run.value(x0) - run.value(x0 - h)) / h
        self.assertAlmostEqual(inner, 4.0, delta=1e-3)
        self.assertAlmostEqual(outer, 4.0, delta=1e-3)
        # at L: C¹, slope s∞ on both sides
        self.assertAlmostEqual((run.value(x0 - L + h) - run.value(x0 - L)) / h, 1.0, delta=1e-3)
        self.assertAlmostEqual((run.value(x0 - L) - run.value(x0 - L - h)) / h, 1.0, delta=1e-3)
        # beyond L: exactly the line of s∞ (no offset)
        for d in (L, 2 * L, 1.0, 7.0):
            self.assertEqual(run.value(x0 - d), self.YS[0] - 1.0 * d)
        # monotone throughout, the cap at its bound included
        xs = [x0 - 2 * L + i * 2 * L / 400 for i in range(401)]
        self.assertTrue(all(run.value(a) <= run.value(b) for a, b in zip(xs, xs[1:])))
        cap = ma._Run([0.0, 1.0, 2.0], [0.0, 4.0, 5.0], [0, 1, 2], 0)       # s_e 5.5 > 4·s∞ = 4: s_n = 4 exactly
        self.assertEqual(cap.m_lo, 4.0)
        xs = [-0.5 + i * 0.5 / 400 for i in range(401)]
        self.assertTrue(all(cap.value(a) <= cap.value(b) for a, b in zip(xs, xs[1:])))

    def test_gap_end_shared_with_the_bridge(self):
        """An end facing a gap takes PCHIP's end slope clipped against the gap's secant, in its end segment and in the
        bridge alike: C¹ at both run ends."""
        a = ma._Run([0.0, 1.0, 2.0], [0.0, 1.0, 3.0], [0, 1, 2], 0)
        b = ma._Run([3.0, 4.0, 5.0], [4.0, 4.5, 5.0], [3, 4, 5], 0)
        s = (b[1][0] - a[1][-1]) / (b[0][0] - a[0][-1])
        a.set_end(True, s)
        b.set_end(False, s)
        self.assertEqual(a.m_hi, ma._clip_fc(a.se_hi, s, s))
        h = 1e-6
        for x, run_side, bridge_side in ((2.0, lambda x: a.value(x), lambda x: ma._bridge(x, a, b)),
                                         (3.0, lambda x: ma._bridge(x, a, b), lambda x: b.value(x))):
            left = (run_side(x) - run_side(x - h)) / h if x == 2.0 else (bridge_side(x) - bridge_side(x - h)) / h
            right = (bridge_side(x + h) - bridge_side(x)) / h if x == 2.0 else (run_side(x + h) - run_side(x)) / h
            self.assertAlmostEqual(left, right, delta=1e-4)

    @unittest.skipUnless(_shipped(), "no shipped assemblage record with its table (the engine branch without records)")
    def test_bse_2100K_case(self):
        """dd3e58a7's case: bse row 2100 K, a run whose first segment is a steep transition (22.49 → 23.62 GPa). At
        2125 K, ρ at cell centres from 19 to 25 GPa rises wherever the table rises (as Envelope's test, on this line)."""
        reg = mr.load()
        v = _view(reg, "silicate_slb_default_bse")
        ib = max(i for i, t in enumerate(v.ts) if t <= 2100.0)
        t, last, bad = 0.5 * (v.ts[ib] + v.ts[ib + 1]), None, []
        for ia in range(len(v.ps) - 1):
            if not 19e9 <= v.ps[ia] <= 25e9:
                continue
            got = v._solid(math.sqrt(v.ps[ia] * v.ps[ia + 1]), t)
            if not isinstance(got, tuple):
                last = None
                continue
            if last is not None:
                cols = [[(v._cell(j, k) or {}).get("rho") for k in (ib, ib + 1)] for j in (ia - 1, ia, ia + 1)]
                if all(p and q and r and p < q < r for p, q, r in zip(*cols)) and got[0] < last * (1.0 - 1e-5):
                    bad.append((v.ps[ia], got[0] / last - 1.0))
            last = got[0]
        self.assertEqual(bad, [])
