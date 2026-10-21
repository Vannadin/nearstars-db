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

    def test_m2_retired_presence_invariant(self):
        """M2 retired (r2 cfeaf0e3 on amendment 2): with §1 a row step's height comes from the reading cell, so the
        stencil a presence is taken with matters only where the read itself steps. Invariant instead: wherever the s_k
        presence and the T-derived presence differ (T_k ± 1e-4, every node within 3 of the step's row, all three
        tables), the reading cell's read has no step at x_s — h is its slope share over 2·SWAP_EPS to 1e-12·ρ (measured
        ≤ 4.4e-14) — and λ = 0; the count is printed."""
        n = 0
        for rid in (BSE, "silicate_slb_earth_dmm_wh2005", KHAN):
            v = _fresh(rid)
            for i, (_c, kr) in enumerate(v._row_steps):
                for k in range(max(kr - 3, 1), min(kr + 4, len(v.ts) - 1)):
                    for t in (v.ts[k] - 1e-4, v.ts[k] + 1e-4):
                        a, b = v._row_step_p(i, t, k), v._row_step_p(i, t)
                        if (a is None) == (b is None):
                            continue
                        n += 1
                        ib = min(max(sum(1 for q in v.ts if q <= t) - 1, 0), len(v.ts) - 2)
                        xs = math.log(a or b)
                        lo, hi = v._edge_read(xs - ma.SWAP_EPS, t, ib, True), v._edge_read(xs + ma.SWAP_EPS, t, ib, False)
                        if lo is not None and hi is not None:
                            share = 0.5 * (lo[1] + hi[1]) * 2.0 * ma.SWAP_EPS
                            self.assertLessEqual(abs(hi[0] - lo[0] - share), 1e-12 * lo[0], (rid, i, k, t))
                        lam = [z[1] for z in v._row_step_lambdas(t, k, ib, xs - 1e-3, xs + 1e-3) if abs(z[0] - xs) < 1e-12]
                        self.assertTrue(all(x == 0.0 for x in lam), (rid, i, k, t, lam))
        print(f"M2 invariant: {n} presence differences, no step (h = the slope share) and λ = 0 at each")
        self.assertGreater(n, 0)

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


#: rev3d amendment 2 (+ delta 1; 68 d8e82397 / 01e26b00, r2 cleared): khan's S_k intervals at the two R2 sites, from the
#: rev3d PC round's sets (artifacts 673cd6e7 raw-ae300563/sets), installed directly
KHAN_155 = {45: [[23.387925502475596, 23.389586550345008]], 46: [[23.387925502475596, 23.389586550345008]]}
KHAN_254 = {35: [[23.82767187441592, 23.876428525839785]], 36: [[23.82767187441592, 23.87543686958455]]}


def _r2_solid(v, cid, tk):
    """R2ContinuityInT's measure at curve cid's x_b + 0.4w and T_k, on the solid read (_solid, as R2 reads: `state` mixes
    the RTpress liquid in where φ > 0 — φ 0.944 at khan 14.37 GPa / 2450 K — and is not the read the repair acts on)."""
    c = next(c for c in v._cut if c.id == cid)
    xb = math.log(c.p_b_ext(tk, v._reach))
    p = math.exp(xb + 0.4 * v._width(xb))
    e = 1e-6 * (v.ts[1] - v.ts[0])
    a2, a1, b1, b2 = (v._solid(p, tk + j * e)[0] for j in (-2, -1, 1, 2))
    return abs((b1 - a1) - 0.5 * (b2 - a2)) / abs(a1)


def _khan(sets):
    v = _fresh(KHAN)
    v._fall_sets = sets
    return v


class Amendment2(unittest.TestCase):
    """Rev3d amendment 2 and delta 1: a row step's sign from the reading cell (§1); its landing continuous in its height,
    λ = S(clamp(h/h₀, 0, 1)), h₀ = max(1e-6·ρ, 2·Rng′), Rng′ the fall around it on its sub-bridge without its own jump
    (§2, delta 1); a floor (λ·Rng′ ≤ 1e-12·ρ → 0); two steps in transition a named STOP; the build's absorbed ends by
    the read's own λ (§3)."""

    def test_p6_the_s1_falling_step_is_bridged(self):
        """P6: bse 1568.5 K, row step 12 at 23.3415 GPa (S1's falling step), S_k built locally: repair off falls
        (≈ −0.627), repair on bridges (> −1e-6·ρ). Mutant: the sign through s_k — red."""
        t = 1568.5
        v = _fresh(BSE)
        ib = min(max(sum(1 for q in v.ts if q <= t) - 1, 0), len(v.ts) - 2)
        (q,) = [q for i in range(len(v._row_steps)) if (q := v._row_step_p(i, t)) is not None and abs(q / 23.3415e9 - 1) < 1e-4]
        x = math.log(q)
        per = {c: rfb.cell_falls(v, c, nsub=NSUB, xr=(x - 0.05, x + 0.05)) for c in (ib - 1, ib, ib + 1)}
        sets = rfb.sets_from(v, per, [])

        def step(w):
            w._fall_sets = sets
            lo, hi = q * math.exp(-1e-9), q * math.exp(1e-9)
            off = _rho(w, hi, t, False) - _rho(w, lo, t, False)
            on = _rho(w, hi, t, True) - _rho(w, lo, t, True)
            return off, on, _rho(w, lo, t, True)
        off, on, rho = step(_fresh(BSE))
        self.assertLess(off, -0.1)
        self.assertGreater(on, -1e-6 * rho)
        real = ma.AssemblageView._row_step_lambdas
        with mock.patch.object(ma.AssemblageView, "_row_step_lambdas",
                               lambda self, t_, sk, ib_, lo, hi: real(self, t_, sk, sk, lo, hi)):
            _off, on_m, rho_m = step(_fresh(BSE))
        self.assertLess(on_m, -1e-6 * rho_m)

    def test_p7_khan_155_continuous_and_the_step_mutant_red(self):
        """P7: khan curve 155 at 2450 K, + 0.4w (the PC's R2 red before the amendment, 1.1e-9): R2 ≤ 1e-9. Mutant: λ a
        step function (0 / 1 at h = 0) — red."""
        self.assertLessEqual(_r2_solid(_khan(KHAN_155), 155, 2450.0), 1e-9)
        with mock.patch.object(ma, "ROW_STEP_LAMBDA", lambda u: 1.0 if u > 0 else 0.0):
            self.assertGreater(_r2_solid(_khan(KHAN_155), 155, 2450.0), 1e-9)

    def test_p8_two_steps_in_transition_stop(self):
        """P8: two non-coincident row steps in transition in one piece (planted λ 0.5, above the floor): the named STOP."""
        v = _khan(KHAN_254)
        x = 23.85
        with mock.patch.object(ma.AssemblageView, "_row_step_lambdas",
                               lambda self, *a: [(23.86, 0.5, 1.0, 2.0), (23.87, 0.5, 1.0, 2.0)]):
            with self.assertRaisesRegex(ma.TableStop, "two row steps in transition"):
                v._fall_piece(x, 2000.0, 35, 35, KHAN_254, _cut_swaps(v, 2000.0))

    def test_p9_cross_cell_disagreement_in_h(self):
        """P9 (r2 C1): at T_k, a planted 1e-9·ρ disagreement in the step's side read between cells k − 1 and k, over a
        deep fall (a wide planted interval around khan 155's step at 2450 K): piece k equal from both cells to 1e-9·ρ.
        Mutant: h₀ fixed at 1e-6·ρ — red."""
        xs = 23.388340765442948
        sets = {k: [[xs - 0.02, xs + 0.02]] for k in (44, 45, 46)}
        k, tk = 45, 2450.0
        x = xs + 0.01
        real = ma.AssemblageView._edge_read

        def planted(self, xe, t, ib, below):
            got = real(self, xe, t, ib, below)
            if got is not None and ib == k - 1 and abs(xe - (xs + ma.SWAP_EPS)) < 1e-12:
                return (got[0] + 1e-9 * got[0], got[1])
            return got

        def pieces(lam_patch=None):
            v = _khan(sets)
            with mock.patch.object(ma.AssemblageView, "_edge_read", planted):
                with lam_patch or mock.patch.object(ma, "SWAP_EPS", ma.SWAP_EPS):
                    return [v._fall_piece(x, tk, ib, k, sets, _cut_swaps(v, tk)) for ib in (k - 1, k)]
        a, b = pieces()
        self.assertLessEqual(abs(a[0] - b[0]), 1e-9 * abs(b[0]), (a, b))
        rl = ma.AssemblageView._row_step_lambdas

        def fixed_h0(self, t_, sk, ib_, lo, hi):
            out = []
            for xs_, _lam, h, _h0 in rl(self, t_, sk, ib_, lo, hi):
                e = real(self, xs_ - ma.SWAP_EPS, t_, ib_, True)
                h0 = 1e-6 * abs(e[0])
                u = min(max(h / h0, 0.0), 1.0)
                out.append((xs_, ma.ROW_STEP_LAMBDA(u), h, h0))
            return out
        a, b = pieces(mock.patch.object(ma.AssemblageView, "_row_step_lambdas", fixed_h0))
        self.assertGreater(abs(a[0] - b[0]), 1e-9 * abs(b[0]), (a, b))

    def test_p10_khan_254_hand_over_lands_fully(self):
        """P10 (delta 1): khan curve 254 at 2000 K — swap 271's cut swap hands over to its holding-row step 7 (h ≈ 283
        kg/m³): λ = 1 and R2 ≤ 1e-9. Mutant: Rng including the step's own jump (λ ≤ ½) — red (≈ 80 kg/m³ at T_k)."""
        v = _khan(KHAN_254)
        (z,) = v._row_step_lambdas(2000.00005, 36, 36, 23.82767187441592, 23.87543686958455)
        self.assertEqual(z[1], 1.0)
        self.assertLessEqual(_r2_solid(v, 254, 2000.0), 1e-9)
        rl = ma.AssemblageView._row_step_lambdas
        real = ma.AssemblageView._edge_read

        def with_jump(self, t_, sk, ib_, lo, hi):
            out = []
            for xs_, _lam, h, _h0 in rl(self, t_, sk, ib_, lo, hi):
                vals = [e[0] for e in (real(self, lo, t_, ib_, True), real(self, xs_ - ma.SWAP_EPS, t_, ib_, True),
                                       real(self, xs_ + ma.SWAP_EPS, t_, ib_, False), real(self, hi, t_, ib_, False))
                        if e is not None]
                h0 = max(1e-6 * vals[0], 2.0 * (max(vals) - min(vals)))
                out.append((xs_, ma.ROW_STEP_LAMBDA(min(max(h / h0, 0.0), 1.0)), h, h0))
            return out
        with mock.patch.object(ma.AssemblageView, "_row_step_lambdas", with_jump):
            self.assertGreater(_r2_solid(_khan(KHAN_254), 254, 2000.0), 1e-9)

    def test_the_floor_counts_and_bridges(self):
        """r2 877c7679: khan piece 35 at 1900.00005 K holds row steps 6 and 7 at λ ~1e-15 (h ~1e-5 against a fall of ~285
        kg/m³ on the sub-bridge): below the floor (λ·Rng′ ≤ 1e-12·ρ), λ = 0 and counted — no STOP."""
        v = _khan(KHAN_254)
        before = v.cut_counts.get("row_step_floored", 0)
        got = v._row_step_lambdas(1900.00005, 35, 34, 23.82767187441592, 23.876428525839785)
        self.assertTrue(got and all(z[1] == 0.0 for z in got), got)
        self.assertGreater(v.cut_counts.get("row_step_floored", 0), before)


class Amendment2Build(unittest.TestCase):
    """§3: the build's rule-2 absorbed end at a row step stands for node k only where the read's own _row_step_lambdas
    lands the step fully (λ = 1), else rule 1 or the STOP; unlanded_for_nodes is then empty by construction."""

    def _scan(self, v):
        st, ab = [], []
        for smp in rfb.cell_falls(v, 9, nsub=NSUB, xr=(22.375, 22.392)):
            st += [s_ for s_ in smp.get("stops", []) if "amendment 2" in str(s_.get("bound", ""))]
            ab += [a for a in smp.get("absorbed", ()) if isinstance(a.get("by"), str)]
        return st, ab

    def test_row_step_absorbed_only_when_landed(self):
        """bse cell 9 at ln P 22.3834 (row step 16, the PC's 22.38 class): three samples absorb at the step, landed for
        both nodes (λ = 1, the sub-bridge's fall on the near side only); none STOPs."""
        st, ab = self._scan(_fresh(BSE))
        self.assertEqual(st, [])
        self.assertEqual(len(ab), 3)
        self.assertTrue(all(a["unlanded_for_nodes"] == [] for a in ab), ab)

    def test_mutant_partial_landing_is_not_absorbed(self):
        """With the read's λ forced to ½ (partial), the same samples are not absorbed: §3's STOP names the nodes."""
        rl = ma.AssemblageView._row_step_lambdas
        with mock.patch.object(ma.AssemblageView, "_row_step_lambdas",
                               lambda self, *a: [(z[0], 0.5, z[2], z[3]) for z in rl(self, *a)]):
            st, ab = self._scan(_fresh(BSE))
        self.assertEqual(ab, [])
        self.assertEqual(len(st), 3)


class _TwoSteps:
    """A stand-in view for _row_step_lambdas: R(x) = 4000 + x·1 (a gentle slope) + 100 past each row step it shows."""
    ts = [1000.0, 1050.0, 1100.0]
    cut_counts = {}

    def __init__(self, steps, shown=None):
        self.steps, self.shown = steps, steps if shown is None else shown
        self._row_steps = [None] * len(self.shown)

    def _row_step_p(self, i, t, ib=None):
        return math.exp(self.shown[i])

    def _edge_read(self, x, t, ib, below):
        return (4000.0 + x + 100.0 * sum(1 for z in self.steps if x > z), 1.0)


class Amendment2Review(unittest.TestCase):
    """68's HOLD on 8aa2fcea: B2 the sub-bridge bounded by the other row steps; B1 §3 at the merged set."""

    def test_p11_two_tall_steps_each_land_fully(self):
        """P11 (68 B2 / r2 cfeaf0e3): two well-separated upward steps (h 100 each, local falls ≈ 0.01) in one swap-free
        interval: each lands at λ = 1. Mutant: the swap-only cut (the other step not bounding the sub-bridge: shown
        alone, its jump inside Rng′) — λ ≈ ½."""
        lo, hi, s1, s2 = 23.0, 23.03, 23.01, 23.02
        got = ma.AssemblageView._row_step_lambdas(_TwoSteps([s1, s2]), 1025.0, 1, 0, lo, hi)
        self.assertEqual([round(z[1], 12) for z in got], [1.0, 1.0], got)
        for s in (s1, s2):
            (z,) = ma.AssemblageView._row_step_lambdas(_TwoSteps([s1, s2], shown=[s]), 1025.0, 1, 0, lo, hi)
            self.assertLess(z[1], 0.6, z)

    def test_b1_the_merged_set_checks_the_reads_landing(self):
        """bse cells 9–10 at ln P 22.3834 (row step 16): sets_from records no «row step not fully landed by the read»
        STOP; with the read's λ forced to ½ it does, at the node's samples."""
        v = _fresh(BSE)
        per = {ib: rfb.cell_falls(v, ib, nsub=NSUB, xr=(22.375, 22.392)) for ib in (9, 10)}
        stops = []
        rfb.sets_from(v, per, [], stops)
        self.assertEqual([s for s in stops if s.get("why") == "row step not fully landed by the read"], [])
        rl = ma.AssemblageView._row_step_lambdas
        with mock.patch.object(ma.AssemblageView, "_row_step_lambdas",
                               lambda self, *a: [(z[0], min(z[1], 0.5), z[2], z[3]) for z in rl(self, *a)]):
            stops = []
            rfb.sets_from(_fresh(BSE), per, [], stops)
        self.assertTrue([s for s in stops if s.get("why") == "row step not fully landed by the read"], stops[:3])
