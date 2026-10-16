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
