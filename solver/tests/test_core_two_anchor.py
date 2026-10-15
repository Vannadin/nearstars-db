# 핵 두 앵커 EOS 시험 — 앵커 재현, 해석 K_T, C¹ 이음매, 격자 게이트 1–3, 답하는 범위 전체, 거절·등급, 세 음성 대조 (핵 두 앵커 등록 1cdff0a3)
"""Tests of the two-anchor liquid core EOS (rewrite/core-two-anchor-registration.frozen.md, artifacts 1cdff0a3; owner
a7181489): eos.huang_core_phase and eos.huang_fes_phase.

§1 G: ρ at both anchors (pure Fe and c_S 0.1, 0.2, 0.3) and pure Fe's K_T and α, to 1e-9; the analytic K_T against a
central difference on §3's grid, to 1e-6. §2 G: C¹ joins at 19 and 35 GPa (analytic one-sided limits, 1e-9); the whole
answering range [0, 51] GPa (α, C_V, K_T, bracket > 0; γ in [1.0, 3.5]); the ceiling and the floor refuse by name;
the grades above 35 GPa and above c_S 0.30 name their distance. §3 G: gates 1–3 on the grid, and the three negative
controls fail them (today's 19-GPa-only phase gate 1, rev 1's ρ-blend gate 2, alternative (d) gate 3).

Run from the worktree root:  <solver venv>/python -m unittest solver.tests.test_core_two_anchor
"""
import math
import unittest

from solver import legacy_materials  # noqa: F401  (puts engine/ on sys.path: the one solver module that imports it)
import eos

G = eos.GPA
P19, P35 = 19.0 * G, 35.0 * G
OC = ((0.04, 0.014), (0.01, 0.005), (0.0, 0.0))


def mix(s, o, c):
    return eos.core_mole_fractions({"S": s, "O": o, "C": c})


def grid_comps():
    """§3's compositions: S 0.10–0.25 wt in 0.005 steps at three (O, C), plus the binary c_S 0–0.30 in 0.01 steps."""
    out = [("wt", o, c, [mix(0.10 + 0.005 * i, o, c) for i in range(31)]) for o, c in OC]
    out.append(("binary", 0.0, 0.0, [{"S": 0.01 * i} for i in range(31)]))
    return out


GRID_P = [15.0 + 0.5 * i for i in range(61)]
GRID_T = (1800.0, 2100.0, 2400.0)
#: gate 2's declared extension (post-result note 1, r2's F2 ruling): S 0.10–0.30 wt in 0.005 steps, T 1500–2700 K,
#: the same P and (O, C); the rule and control (b) run on the same cells. Cells with c_S > 0.30 are graded (§2).
EXT_T = (1500.0, 1800.0, 2100.0, 2400.0, 2700.0)


def ext_comps():
    return [[mix(0.10 + 0.005 * i, o, c) for i in range(41)] for o, c in OC]


def t_path(p):
    return 2100.0 + 300.0 * (p - P19) / (P35 - P19)


# ── negative controls: the forms the registration rejected, rebuilt here as they were ───────────────────────────
def old_phase(x, anchor):
    """Today's (pre-item) one-anchor phase: bm2_ref at that anchor with the mixture's eq-7 ρ and eq-8 K_T."""
    p_ref, t_ref, _r, _k = eos.HUANG_FE_ANCHORS[anchor]
    alpha, c_v, _g = eos.HUANG_FE_THERMAL[anchor]
    k_t = eos.huang_core_k_t_gpa(x, anchor) * G
    return eos.Phase(name=f"old_{anchor}", form="bm2_ref", rho0=eos.huang_core_density(x, anchor) * 1e3, k0=k_t,
                     k0p=4.0, p_max=350.0 * G, p_min=0.0, p_ref=p_ref, alpha_k=alpha * k_t, t_ref=t_ref,
                     c_v_ref=c_v, ref="control")


def blend_rho(x, p, t):
    """Rev 1's ρ-blend: the two one-anchor phases mixed in ρ by a smoothstep in P over 19–35 GPa."""
    u = min(max((p - P19) / (P35 - P19), 0.0), 1.0)
    w = u * u * (3.0 - 2.0 * u)
    return (1.0 - w) * old_phase(x, "19GPa").density(p, t) + w * old_phase(x, "35GPa").density(p, t)


def alt_d_ln(x, p, t):
    """Alternative (d): the mixture's ln ρ as a Hermite on the path with eq 8's K_T in the end slopes."""
    h = P35 - P19
    u = (p - P19) / h
    dt = 300.0 / h
    ends = []
    for tag in ("19GPa", "35GPa"):
        a = eos.HUANG_FE_THERMAL[tag][0]
        ends.append((math.log(eos.huang_core_density(x, tag) * 1e3), 1.0 / (eos.huang_core_k_t_gpa(x, tag) * G) - a * dt))
    (l0, m0), (l1, m1) = ends
    lp = ((2 * u ** 3 - 3 * u ** 2 + 1) * l0 + (u ** 3 - 2 * u ** 2 + u) * h * m0 + (-2 * u ** 3 + 3 * u ** 2) * l1
          + (u ** 3 - u ** 2) * h * m1)
    a = eos.HUANG_FE_THERMAL["19GPa"][0] + (eos.HUANG_FE_THERMAL["35GPa"][0] - eos.HUANG_FE_THERMAL["19GPa"][0]) * u
    return lp - a * (t - (2100.0 + 300.0 * u))


def k_band_ratio(x, p, k):
    kb = sorted((eos.huang_core_k_t_gpa(x, "19GPa") * G, eos.huang_core_k_t_gpa(x, "35GPa") * G))
    return k / (0.9 * kb[0]), k / (1.1 * kb[1])


# ── gate counters (shared by the rule and its controls) ───────────────────────────────────────────────────────────
def gate1_fails(rho_of):
    """∂ρ/∂S < 0 at fixed (P, T): count consecutive-S pairs with ρ not falling."""
    n = 0
    for _k, _o, _c, xs in grid_comps():
        for pg in GRID_P:
            for t in GRID_T:
                rs = [rho_of(x, pg * G, t) for x in xs]
                n += sum(1 for a, b in zip(rs, rs[1:]) if not b < a)
    return n


def gate2_fails(rho_of, d=1e6, skip_refusals=False):
    """∂ρ/∂P > 0 at fixed (T, x), by central difference, on the declared extension (note 1). A control built from the
    old one-anchor phases refuses below its own BM2 turn; with skip_refusals those cells are not counted either way."""
    n = 0
    for xs in ext_comps():
        for x in xs:
            for pg in GRID_P:
                for t in EXT_T:
                    try:
                        ok = rho_of(x, pg * G + d, t) > rho_of(x, pg * G - d, t)
                    except (ValueError, eos.PhaseGap):
                        if not skip_refusals:
                            raise
                        continue
                    n += not ok
    return n


def gate3_fails(k_of):
    """The K_T band over 19–35 GPa: 0.9·min(K₁₉, K₃₅) ≤ K_T ≤ 1.1·max(K₁₉, K₃₅), eq 8's two values at that composition,
    evaluated at T_path(P) — eq 8's K₁₉ and K₃₅ are path values (post-result note 1, r2's F1 ruling (i))."""
    n = 0
    for _k, _o, _c, xs in grid_comps():
        for x in xs:
            for pg in GRID_P:
                if not 19.0 <= pg <= 35.0:
                    continue
                lo, hi = k_band_ratio(x, pg * G, k_of(x, pg * G, t_path(pg * G)))
                n += not (lo >= 1.0 and hi <= 1.0)
    return n


def new_rho(x, p, t):
    return eos.huang_core_phase(x).density(p, t)


def new_k(x, p, t):
    return eos.huang_core_phase(x).k_t_at(p, t)


class Anchors(unittest.TestCase):
    """§1 G."""

    def test_rho_at_both_anchors(self):
        for cs in (0.0, 0.1, 0.2, 0.3):
            ph = eos.huang_core_phase({"S": cs})
            for tag in ("19GPa", "35GPa"):
                p, t, _r, _k = eos.HUANG_FE_ANCHORS[tag]
                want = eos.huang_core_density({"S": cs}, tag) * 1e3
                self.assertLessEqual(abs(ph.density(p, t) / want - 1.0), 1e-9, (cs, tag))

    def test_pure_fe_k_t_and_alpha(self):
        ph = eos.huang_core_phase({})
        for tag in ("19GPa", "35GPa"):
            p, t, _r, k = eos.HUANG_FE_ANCHORS[tag]
            self.assertLessEqual(abs(ph.k_t_at(p, t) / (k * G) - 1.0), 1e-9, tag)
            self.assertLessEqual(abs(ph.alpha_at(p) / eos.HUANG_FE_THERMAL[tag][0] - 1.0), 1e-9, tag)
            self.assertLessEqual(abs(ph.dpdt_v(t, 0.0, p) / (eos.HUANG_FE_THERMAL[tag][0] * k * G) - 1.0), 1e-9, tag)

    def test_c_v_and_gamma_at_the_anchors(self):
        """C_V is Table 1's 494 / 496 at the anchors; pure Fe's γ = αK_T/(C_V ρ) is §1 item 3's 2.731 / 2.664."""
        ph = eos.huang_core_phase({})
        for tag, g in (("19GPa", 2.731), ("35GPa", 2.664)):
            p, t, _r, _k = eos.HUANG_FE_ANCHORS[tag]
            self.assertEqual(ph.c_v_at(p, t), eos.HUANG_FE_THERMAL[tag][1])
            self.assertAlmostEqual(ph.gruneisen(ph.density(p, t), t, 0.0, p), g, delta=5e-4)

    def test_derived_k_t_is_the_registrations(self):
        """§1 item 4's prototype numbers (c_S binary; 19 GPa, then 35 GPa): 137.2/187.3, 116.9/158.5, 96.9/131.0."""
        for cs, want in ((0.1, (137.2, 187.3)), (0.2, (116.9, 158.5)), (0.3, (96.9, 131.0))):
            ph = eos.huang_core_phase({"S": cs})
            got = (ph.k_t_at(P19, 2100.0) / G, ph.k_t_at(P35, 2400.0) / G)
            self.assertAlmostEqual(got[0], want[0], delta=0.05)
            self.assertAlmostEqual(got[1], want[1], delta=0.05)

    def test_analytic_k_t_equals_central_difference(self):
        h, worst = 1e5, 0.0
        for _k, _o, _c, xs in grid_comps():
            for x in xs[::5]:
                ph = eos.huang_core_phase(x)
                for pg in GRID_P:
                    for t in GRID_T:
                        p = pg * G
                        fd = 2 * h / (math.log(ph.density(p + h, t)) - math.log(ph.density(p - h, t)))
                        worst = max(worst, abs(fd / ph.k_t_at(p, t) - 1.0))
        self.assertLessEqual(worst, 1e-6)

    def test_alpha_is_composition_independent(self):
        """The bracket is T-independent, so (∂ln ρ/∂T)_P = −α(P) for every composition."""
        for x in ({}, {"S": 0.25}, mix(0.2227, 0.04, 0.014)):
            ph = eos.huang_core_phase(x)
            for pg in (5.0, 25.0, 45.0):
                d = (math.log(ph.density(pg * G, 2101.0)) - math.log(ph.density(pg * G, 2099.0))) / 2.0
                self.assertAlmostEqual(-d, ph.alpha_at(pg * G), delta=1e-10)


class Joins(unittest.TestCase):
    """§2 G: ρ and (∂ρ/∂P)_T from either side agree at 19 and 35 GPa (analytic one-sided limits)."""

    def test_c1(self):
        e, worst = 1e-3, 0.0
        for _k, _o, _c, xs in grid_comps():
            for x in xs:
                ph = eos.huang_core_phase(x)
                for pj in (P19, P35):
                    for t in GRID_T:
                        (la, da), (lb, db) = ph.ln_rho(pj - e, t), ph.ln_rho(pj + e, t)
                        worst = max(worst, abs(lb - la), abs(db / da - 1.0))
        self.assertLessEqual(worst, 1e-9)


class Range(unittest.TestCase):
    """§2 G over the whole answering range [0, 51] GPa."""

    def test_positive_and_gamma_band(self):
        bad, gmin, gmax = [], 9.0, 0.0
        for o, c in OC:
            for s in [0.0] + [0.10 + 0.01 * i for i in range(16)]:
                ph = eos.huang_core_phase(mix(s, o, c) if s > 0 else {})
                for i in range(103):
                    p = 0.5 * i * G
                    d, dd = eos.huang_drho(ph._x(), p)
                    if not 1.0 + d / math.exp(eos.huang_fe_path(p)[0]) > 0.0:
                        bad.append(("bracket", p, s, o))
                    for t in (1500.0, 1800.0, 2100.0, 2400.0, 2700.0):
                        rho, k = ph.density(p, t), ph.k_t_at(p, t)
                        g = ph.gruneisen(rho, t, 0.0, p)
                        gmin, gmax = min(gmin, g), max(gmax, g)
                        if not (ph.alpha_at(p) > 0.0 and ph.c_v_at(p, t) > 0.0 and k > 0.0 and 1.0 <= g <= 3.5):
                            bad.append((p, t, s, o, k, g))
        self.assertEqual(bad, [])
        self.assertGreater(gmin, 1.0)
        self.assertLess(gmax, 3.5)

    def test_ceiling_refuses_by_name(self):
        m = eos.MATERIALS["fe_s19_o4_c5permil_19gpa"]
        self.assertGreater(m.density(51.0 * G, 2400.0), 0.0)
        with self.assertRaises(eos.PhaseGap) as cm:
            m.density(51.01 * G, 2400.0)
        self.assertIn("천장(51.0 GPa)", cm.exception.reason)
        with self.assertRaises(eos.PhaseGap):
            eos.MATERIALS["fe_s_13wt_19gpa"].density(51.01 * G, 2400.0)

    def test_floor_refuses_by_name(self):
        m = eos.MATERIALS["fe_s19_o4_c5permil_19gpa"]
        self.assertGreater(m.density(0.0, 2100.0), 0.0)
        with self.assertRaises(eos.PhaseGap) as cm:
            m.density(-0.1 * G, 2100.0)
        self.assertTrue(cm.exception.reason.startswith("-0.1000 GPa"))

    def test_grades_name_their_distance(self):
        ph = eos.huang_core_phase(mix(0.19, 0.04, 0.005))
        self.assertEqual(ph.density_reach(30.0 * G), ("ok", ""))
        kind, why = ph.density_reach(40.0 * G)
        self.assertEqual(kind, "graded-extrapolation")
        self.assertIn("위로 5 GPa", why)
        hi = eos.huang_core_phase(mix(0.25, 0.04, 0.014))
        self.assertGreater(hi.x_s, eos.HUANG_C_S_SAMPLED)
        kind, why = hi.density_reach(30.0 * G)
        self.assertEqual(kind, "graded-extrapolation")
        self.assertIn(f"{hi.x_s - 0.30:.4f}", why)

    def test_below_19_counts_as_today(self):
        ph = eos.huang_core_phase(mix(0.19, 0.04, 0.005))
        before = eos.DENSITY_REACH["beyond_measured"]
        ph.note_below_ref(10.0 * G)
        ph.note_below_ref(20.0 * G)
        self.assertEqual(eos.DENSITY_REACH["beyond_measured"], before + 1)

    def test_ceiling_reason_is_not_degeneracy(self):
        import interior
        why = interior._ceiling_why(eos.MATERIALS["fe_s19_o4_c5permil_19gpa"])
        self.assertIn("앵커 간격(16 GPa)", why)
        self.assertNotIn("Thomas-Fermi-Dirac", why)
        self.assertIn("Thomas-Fermi-Dirac", interior._ceiling_why(eos.MATERIALS["fe_prem"]))


class GridGates(unittest.TestCase):
    """§3 G: gates 1–3 hold for the rule; each negative control fails its gate."""

    def test_gate1_rule(self):
        self.assertEqual(gate1_fails(new_rho), 0)

    def test_gate2_rule(self):
        self.assertEqual(gate2_fails(new_rho), 0)

    def test_gate3_rule(self):
        self.assertEqual(gate3_fails(new_k), 0)

    def test_control_today_fails_gate1(self):
        self.assertGreater(gate1_fails(lambda x, p, t: old_phase(x, "19GPa").density(p, t)), 0)

    def test_control_blend_fails_gate2(self):
        """Note 1 (F2): rev 1's blend fails on the extension at every T (measured: 750 cells, S 0.255–0.30 wt,
        26.5–34 GPa), and passes on §3's grid as it stood."""
        self.assertGreater(gate2_fails(blend_rho, skip_refusals=True), 0)

    def test_control_alt_d_fails_gate3(self):
        def k(x, p, t, d=1e5):
            return 2 * d / (alt_d_ln(x, p + d, t) - alt_d_ln(x, p - d, t))
        self.assertGreater(gate3_fails(k), 0)


class Binary(unittest.TestCase):
    """huang_fes_phase: the same rule with the S column only; it starts at 19 GPa and carries pure Fe's α (§4)."""

    def test_binary_is_the_rule_with_s_only(self):
        a, b = eos.huang_fes_phase(0.2), eos.huang_core_phase({"S": 0.2})
        for pg in (19.0, 27.0, 35.0, 45.0):
            self.assertEqual(a.density(pg * G, 2200.0), b.density(pg * G, 2200.0))
        self.assertEqual((a.p_min, a.p_max, a.melt), (P19, 51.0 * G, "iron_fes_eutectic"))
        self.assertTrue(a.has_thermal)


if __name__ == "__main__":
    unittest.main()
