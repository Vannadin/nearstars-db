# ρ rev3d 시험 — 노드에 묶인 조각(D1 읽기 가능·D2 착지 목록), 짓기의 좁은 틈 나누기(D3), 밴드로 막은 넓히기(D4) 의 심기 P1–P5 와 변이 M1–M4 (68 설계 5257255e, 수정 1 79f66fb0)
"""ρ rev 3, rev3d (artifacts main 68db31be, rewrite/rho-bridge/rev3d-node-fixed-pieces.md, blob 5257255e; amendment 1
79f66fb0): the plants P1–P5 and the mutants M1–M4 of §5, on Mac-sized windows. The sets are built here by the build's
own cell_falls / sets_from over two cells and a narrow ln P window, then installed on the view (the read's own
_fall_sets), with the repair on.

    solver/.venv/bin/python -m unittest solver.tests.test_rho_rev3d
"""
import math
import unittest
from unittest import mock

from solver import material_assemblage as ma
from solver import rho_fall_build as rfb

BSE, DMM, KHAN = "silicate_slb_default_bse", "silicate_slb_earth_dmm_wh2005", "silicate_slb_mars_khan2022"
NSUB = 4
#: the cases named in §2–§4 (T_k a node; P in Pa) and r2's R2 khan case, with a window half-width in ln P
CASE_A = (BSE, 2200.0, 4.0e6, 2.0)           # §2 (A): a corner/outer refusal at the shared row
CASE_B = (KHAN, 2350.0, 15.14e9, 0.15)      # §2 (B): the holding row gained at T_k (R2ContinuityInT's khan reds)
CASE_D4 = (BSE, 912.5, 12.991e9)             # §4: the widening overshoot
#: §2 (B)'s data, as Job B's PC build left them (artifacts jobB-sets-af8408a7 ec38f7f0,
#: pc/ea-jobB/raw-af8408a7/sets/silicate_slb_mars_khan2022.json, blob 3758f7ae): khan's S_41..S_43 near 23.40 ln P,
#: the sets R2ContinuityInT reds at 2300 K on (curves 171 / 174 / 199) — a fixture for D2, which no rebuild can move
B_SETS = {41: [[23.27536984245836, 23.335444673221588], [23.38841541674191, 23.513694991854138]],
          42: [[23.275259712194785, 23.335444673221588], [23.387974150578323, 23.513694991854138]],
          43: [[23.275259712194785, 23.335444673221588], [23.34649666407458, 23.362590716802146],
               [23.387974150578323, 23.51367633587454]]}
B_POINTS = (14.5764e9, 14.6118e9, 14.8152e9)  # R2's points (exp(x_b + 0.4 w)) on those curves at 2300 K


def _local(rid, tk, p, half, nsub=NSUB):
    """A fresh view with S_k built over cells k − 1 and k and ln P ± half around p, installed as its fall sets."""
    v = _fresh(rid)
    k = v.ts.index(tk)
    x = math.log(p)
    per = {ib: rfb.cell_falls(v, ib, nsub=nsub, xr=(x - half, x + half)) for ib in (k - 1, k) if 0 <= ib < len(v.ts) - 1}
    dropped = []
    sets = rfb.sets_from(v, per, dropped)
    v._fall_sets = sets
    return v, k, x, sets, dropped


def _fresh(rid):
    from solver import material_registry as mr
    from solver.from_v1 import thaw
    reg = mr.load()
    return ma.view(thaw(reg.get(rid)), reg.tables[rid], 1600.0)


def _cut_swaps(v, t):
    return lambda: [math.log(pe) for c in v._cut if c.kind == "swap" for pe in (c.p_b_ext(t, v._reach),)
                    if pe is not None]


def _p1(v, k, sets):
    """P1 on one view: [(x, piece from cell k − 1, piece from cell k)] at T_k for every interval midpoint of S_k."""
    tk = v.ts[k]
    out = []
    for a, b in sets.get(k, ()):
        x = 0.5 * (a + b)
        with mock.patch.object(ma, "RHO_BRIDGE", True):
            lo = v._fall_piece(x, tk, k - 1, k, sets, _cut_swaps(v, tk))
            hi = v._fall_piece(x, tk, k, k, sets, _cut_swaps(v, tk))
        out.append((x, lo, hi))
    return out


def _r2(v, p, tk):
    """R2ContinuityInT's measure at (p, T_k), relative: |(ρ₊₁ − ρ₋₁) − ½(ρ₊₂ − ρ₋₂)| / |ρ₋₁| at T_k ± (1, 2)·1e-6·ΔT."""
    e = 1e-6 * (v.ts[1] - v.ts[0])
    a2, a1, b1, b2 = (_rho(v, p, tk + j * e) for j in (-2, -1, 1, 2))
    return abs((b1 - a1) - 0.5 * (b2 - a2)) / abs(a1)


def _rho(v, p, t, on=True):
    with mock.patch.object(ma, "RHO_BRIDGE", on):
        return v.state(p, t)[0]


class _Cases(unittest.TestCase):
    _memo = {}

    @classmethod
    def local(cls, case, **kw):
        key = (case, tuple(sorted(kw.items())))
        if key not in cls._memo:
            cls._memo[key] = _local(*case, **kw)
        return cls._memo[key]


class Plants(_Cases):
    def test_p1_a_node_piece_is_one_function(self):
        """P1 (D1, r2's check): at T_k, piece k from cell k − 1 and from cell k share the interval and the landed list
        bit for bit, and their values agree to 1e-9 relative, at every interval midpoint of S_k; n > 0."""
        n = 0
        for case in (CASE_A, CASE_B):
            v, k, _x, sets, _d = self.local(case)
            for x, lo, hi in _p1(v, k, sets):
                with self.subTest(rid=case[0], x=x):
                    self.assertEqual((lo[1], lo[2]), (hi[1], hi[2]))
                    self.assertEqual(lo[0] is None, hi[0] is None)
                    if lo[0] is not None:
                        self.assertLessEqual(abs(lo[0] - hi[0]), 1e-9 * abs(hi[0]))
                    n += 1
        self.assertGreater(n, 0)

    def test_p2_no_step_at_the_shared_row(self):
        """P2 (A): bse 2200 K, 0.004 GPa: the repaired ρ across T_k ± 0.01 K has no step above the off read's largest
        step × 2."""
        v, k, x, _s, _d = self.local(CASE_A)
        tk, p = v.ts[k], math.exp(x)
        ts = [tk + 0.001 * j for j in range(-10, 11)]
        on = [_rho(v, p, t, True) for t in ts]
        off = [_rho(v, p, t, False) for t in ts]
        d_on = max(abs(b - a) for a, b in zip(on, on[1:]))
        d_off = max(abs(b - a) for a, b in zip(off, off[1:]))
        self.assertLessEqual(d_on, 2.0 * d_off + 1e-12, (d_on, d_off))

    def test_p3_continuity_at_the_khan_case(self):
        """P3 (B): R2ContinuityInT's check with the repair on — at T = T_k ± 1e-6·ΔT and ± 2e-6·ΔT,
        |(ρ₊₁ − ρ₋₁) − ½(ρ₊₂ − ρ₋₂)| ≤ 1e-9·ρ — at khan 2350 K / 15.14 GPa on sets built here (the design's named case),
        and at R2's three 2300 K points on Job B's own sets (B_SETS), where the old t-derived row-step stencil split the
        interval at T_k."""
        v, k, x, _s, _d = self.local(CASE_B)
        self.assertLessEqual(_r2(v, math.exp(x), v.ts[k]), 1e-9)
        w = _fresh(KHAN)
        w._fall_sets = B_SETS
        for p in B_POINTS:
            with self.subTest(p=p):
                self.assertLessEqual(_r2(w, p, 2300.0), 1e-9)

    def test_p4_the_sliver_is_found(self):
        """P4 (D3): falls_at at bse T 2478.125, ib 45, x ± 0.02 around 15.906 GPa returns an interval holding it."""
        v = _fresh(BSE)
        x = math.log(15.906e9)
        ivs = rfb.falls_at(v, 2478.125, 45, x - 0.02, x + 0.02)[0]
        self.assertTrue(any(a < x < b for a, b, *_r in ivs), ivs)

    def test_p5_the_widening_is_capped(self):
        """P5 (D4): bse 12.991 GPa, 912.5 K: the regain-side end b′ sits on R(b)·(1 + τ_w) to the bisection's 1e-6 in
        ln P (τ_w from the build's own cap at that cell), and the repaired ρ there is ≤ max(R(a), R(x))·(1 + τ_w) + 1e-8·R."""
        rid, t, p = CASE_D4
        v = _fresh(rid)
        ib = min(max(sum(1 for q in v.ts if q <= t) - 1, 0), len(v.ts) - 2)
        x = math.log(p)
        ivs, _u, _st, _fl, _sj, ur = rfb.falls_at(v, t, ib, x - 0.3, x + 0.3)
        (iv,) = [iv for iv in ivs if iv[0] < x < iv[1]]
        lo_, hi_, a, c = iv
        cap = next(cp for cp in ur["caps"] if cp["side"] == "hi" and cp["x0"] == c)
        tau = cap["tau_w"]
        g = rfb._reader(v, t, ib, [])
        rb_, rc = g(hi_)[0], g(c)[0]
        if not cap["at_limit"]:
            self.assertLessEqual(rb_, rc * (1.0 + tau) * (1.0 + 1e-12))
            self.assertGreaterEqual(g(hi_ + 1e-6)[0], rc * (1.0 + tau) * (1.0 - 1e-12))
        v._fall_sets = {ib: [[lo_, hi_]], ib + 1: [[lo_, hi_]]}
        rx = _rho(v, p, t, True)
        ra, r_own = g(a)[0], g(x)[0]
        self.assertLessEqual(rx, max(ra, r_own) * (1.0 + tau) + 1e-8 * r_own)


class ClipNetFall(_Cases):
    """68 B1 on a7f3251b: a D1 clip that leaves R(b₂) < R(a₂) at a sample, with no landed step to absorb it, STOPs
    («net fall after unreadable-end clip»); the mutant (the check removed) lets it through to the bridge's secant."""

    def _plant(self):
        """The first (case, node interval, sample (T, ib), x) where R(x) < R(a) inside an S_k interval: refusing the
        upper edge past x clips b into the fall at that sample."""
        for case in (CASE_A, CASE_B):
            v, k, _x, sets, _d = self.local(case)
            dt = v.ts[k] - v.ts[k - 1]
            samples = [(v.ts[ib] + dt * j / NSUB, ib) for ib in (k - 1, k) for j in range(NSUB + 1)]
            for a, b in sets.get(k, ()):
                for t, ib in samples:
                    ea = v._edge_read(a, t, ib, True)
                    if ea is None:
                        continue
                    for q in range(1, 64):
                        xd = a + (b - a) * q / 64
                        r = v._edge_read(xd, t, ib, False)
                        if r is not None and r[0] < ea[0]:
                            real_er = ma.AssemblageView._edge_read

                            def er(self, xe, t_, ib_, below, xd=xd):
                                if not below and xe > xd:
                                    return None          # the plant: the upper edge refuses past xd
                                return real_er(self, xe, t_, ib_, below)
                            return v, k, a, b, er, samples
        self.skipTest("no fall inside an S_k interval in the cases' windows")

    def test_a_clip_into_the_fall_stops(self):
        v, k, a, b, er, samples = self._plant()
        stops = []
        with mock.patch.object(ma.AssemblageView, "_edge_read", er):
            got = rfb._node_readable(v, a, b, samples, [], k, stops)
        self.assertLess(got[1], b)
        self.assertEqual([s_["why"] for s_ in stops], ["net fall after unreadable-end clip"])

    def test_m_the_check_removed(self):
        v, k, a, b, er, samples = self._plant()
        stops = []
        with mock.patch.object(ma.AssemblageView, "_edge_read", er), \
                mock.patch.object(rfb, "_clip_net_fall", lambda *a_: []):
            rfb._node_readable(v, a, b, samples, [], k, stops)
        self.assertEqual(stops, [])


class Mutants(_Cases):
    """Each red on its plant (§5)."""

    def test_m1_one_stencil_at_the_node(self):
        """M1 (amendment 1): at T_k only one cell's stencil checked — P1 red. Planted: an end of S_k that reads
        everywhere except at T_k under cell k − 1's stencil (bse's real one-stencil ends also refuse inside cell k, which
        any stencil-per-sample check catches). D1 clips it; with (T_k, cell k − 1) left out of the check it stays, and
        the two cells' pieces at T_k differ (one reads the end, the other refuses it)."""
        v0, k, _x, sets0, _d = self.local(CASE_A)
        tk = v0.ts[k]
        (a_end, _b), *_rest = sets0[k]
        real_er = ma.AssemblageView._edge_read

        def er(self, xe, t, ib, below):
            if below and xe == a_end and t == tk and ib == k - 1:
                return None                              # the plant: this end refuses only here
            return real_er(self, xe, t, ib, below)
        real_nr = rfb._node_readable

        def one(v, a, b, samples, dropped, node):
            tk_ = v.ts[node]
            return real_nr(v, a, b, [(t, ib) for t, ib in samples if not (t == tk_ and ib == node - 1)], dropped, node)
        with mock.patch.object(ma.AssemblageView, "_edge_read", er):
            # the plant with D1 as built: the end is clipped, P1 holds
            full = rfb._node_readable(v0, a_end, _b, [(tk, k - 1), (tk, k)], [], k)
            self.assertNotEqual(full[0], a_end)
            with mock.patch.object(rfb, "_node_readable", one):
                kept = rfb._node_readable(v0, a_end, _b, [(tk, k - 1), (tk, k)], [], k)
            self.assertEqual(kept[0], a_end)             # M1: left in place
            sets_m = {**sets0, k: [[a_end, _b]] + [list(iv) for iv in sets0[k][1:]]}
            bad = [1 for _x2, lo, hi in _p1(v0, k, sets_m) if (lo[0] is None) != (hi[0] is None)]
        self.assertTrue(bad)

    def test_m2_row_steps_from_t(self):
        """M2: _row_step_p re-deriving ib from T (the stencil gains the holding row at T_k) — P1 or P3 red."""
        real = ma.AssemblageView._row_step_p
        w = _fresh(KHAN)
        w._fall_sets = B_SETS
        with mock.patch.object(type(w), "_row_step_p", lambda self, i, t, ib=None: real(self, i, t)):
            red = [p for p in B_POINTS if _r2(w, p, 2300.0) > 1e-9]
        self.assertTrue(red)

    def test_m3_no_sliver_subdivision(self):
        """M3: no sliver subdivision (W_S 0) — P4 red."""
        v = _fresh(BSE)
        x = math.log(15.906e9)
        with mock.patch.object(rfb, "W_S", 0.0):
            ivs = rfb.falls_at(v, 2478.125, 45, x - 0.02, x + 0.02)[0]
        self.assertFalse(any(a < x < b for a, b, *_r in ivs), ivs)

    def test_m4_uncapped(self):
        """M4: the widening uncapped (τ_w out of reach) — P5's bound red."""
        rid, t, p = CASE_D4
        v = _fresh(rid)
        ib = min(max(sum(1 for q in v.ts if q <= t) - 1, 0), len(v.ts) - 2)
        x = math.log(p)
        with mock.patch.object(rfb, "_band_at", lambda v_, x_, ib_: 1e3):
            ivs = rfb.falls_at(v, t, ib, x - 0.3, x + 0.3)[0]
        (iv,) = [iv for iv in ivs if iv[0] < x < iv[1]]
        lo_, hi_, a, _c = iv
        tau = rfb._band_at(v, _c, ib) / rfb.TAU_W_DIV
        g = rfb._reader(v, t, ib, [])
        v._fall_sets = {ib: [[lo_, hi_]], ib + 1: [[lo_, hi_]]}
        rx = _rho(v, p, t, True)
        self.assertGreater(rx, max(g(a)[0], g(x)[0]) * (1.0 + tau) + 1e-8 * g(x)[0])


if __name__ == "__main__":
    unittest.main()
