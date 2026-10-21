# s 읽기 가장자리 사건 감쇠 시험 — 노트 5 수정 1·delta 1: 심기 (d) C⁰·감쇠 끔 변이·겹침 변이, ρ 와 구간 밖 비트 동일
"""s-read post-freeze note 5 amendment 1 and its delta 1 (68; artifacts 3486dc52, d91925e8): the s path holds an
edge's (c′) window toward its position at each T event (t0, t1, t0 − reach, t1 + reach) inside |T − T_e| < Δ_e.
- Plant (d) (test_c0, r2 32cf0efe): bse 18.679 GPa at 2400 K (edge 228's (b′) end) — the s read's dT/dP and c_P C⁰ in
  T by the J₄ test; the taper-off mutant (S_EDGE_TAPER False) red.
- The overlap mutant (S_TAPER_OVERLAP True: half-width ΔT, the nearer event): bse two-row edge 234 at 1675 K (midway
  between its ends) steps c_P by ~7 %; with the rule's Δ_e = ½ · gap it is continuous.
- ρ bit-identical with the taper on and off; s, dT/dP and c_P bit-identical at reads whose T lies outside every zone
  of the edges near x.
The s read is forced on (the records' own default is s off on T′; the F13 records declare it)."""
import math
import unittest
from unittest import mock

from solver import material_assemblage as ma

BSE = "silicate_slb_default_bse"
D_P, D_T = 18.679e9, 2400.0
O_X, O_T = 23.71190360389735, 1675.0


def _view():
    from solver import material_registry as mr
    from solver.from_v1 import thaw
    reg = mr.load()
    v = ma.view(thaw(reg.get(BSE)), reg.tables[BSE], 1600.0)
    v.s_read = True
    return v


def _c0(v, p, t, i):
    from solver.tests.test_assemblage_c1 import _c0_j4
    ref = abs(v._solid(p, t)[i])
    return _c0_j4(lambda h: v._solid(p, t + h)[i] - v._solid(p, t - h)[i], ref, 1e-9 * ref)


def _cp_jump(v, x, t):
    a, b = v._solid(math.exp(x), t - 1e-7), v._solid(math.exp(x), t + 1e-7)
    return abs(b[2] - a[2]) / abs(a[2])


@mock.patch.object(ma, "RHO_BRIDGE", False)
class EdgeTaper(unittest.TestCase):
    def test_plant_d_c0_in_t(self):
        v = _view()
        for i, f in ((1, "dtdp"), (2, "c_p")):
            got = _c0(v, D_P, D_T, i)
            with self.subTest(field=f):
                self.assertTrue(got["resolved"] and got["ok"], got)

    def test_mutant_taper_off(self):
        with mock.patch.object(ma, "S_EDGE_TAPER", False):
            self.assertFalse(_c0(_view(), D_P, D_T, 1)["ok"])

    def test_overlap_mutant(self):
        self.assertLessEqual(_cp_jump(_view(), O_X, O_T), 1e-7)
        with mock.patch.object(ma, "S_TAPER_OVERLAP", True):
            self.assertGreater(_cp_jump(_view(), O_X, O_T), 1e-3)

    def test_rho_and_outside_the_zones_bit_identical(self):
        on, off = _view(), None
        with mock.patch.object(ma, "S_EDGE_TAPER", False):
            off = _view()
        pts = [(D_P * math.exp(q * 0.01), D_T + d) for q in (-2, 0, 2) for d in (-130.0, -60.0, -1e-6, 0.0, 30.0, 75.0)]
        pts += [(math.exp(O_X + q * 0.01), O_T + d) for q in (-1, 0, 1) for d in (-60.0, 0.0, 60.0)]
        compared = 0
        for p, t in pts:
            a = on._solid(p, t)
            with mock.patch.object(ma, "S_EDGE_TAPER", False):
                b = off._solid(p, t)
            self.assertEqual(a[0], b[0], (p, t))           # ρ: never moved
            x = math.log(p)
            zoned = any(abs(t - z[0]) < z[1] for c in on._cut if c.kind == "edge"
                        for pe in (c.p_b_ext(t, on._reach),) if pe is not None and abs(x - math.log(pe)) < on._width(math.log(pe))
                        for z in on._taper_zones(c))
            if not zoned:
                compared += 1
                self.assertEqual(a[:3], b[:3], (p, t))
        self.assertGreater(compared, 0)


if __name__ == "__main__":
    unittest.main()
