# 핵 엔트로피 생성 φ 의 앵커 — Nimmo 해석 핵(경로 A)으로 Table 4 의 여섯 엔트로피 항 성분별 재현, 엔진 지구는 밴드로 보고, 3 Gyr 거절 (C15)
"""Anchor the core entropy production (C15).

    python3 engine/test_core_entropy.py

1. **Route A (test only)** — Nimmo's analytic core from `test_core_energy` plus the entropy terms: Table 4's six
   entropy components reproduced **one by one** on the paper's own inputs — E_R 89 · E_s 64 · E_L 159 ·
   E_H −134 · E_g 375 · E_k 202 MW/K, ΔE 351 — each within the pre-registered 10 % (E_L, E_g, E_H ≈ −6 %: the
   C_r factor of C14, left low). E_k's closed form (eq. 26) and Q_k (eq. 5) re-closed as the parallel seat did.
   Pinned labels: E_s needs the 1/T_c prefactor (without it: 10⁵ off); E_H's bracket order is recovered by
   closure (the other order gives +125 against the printed −134).
2. **Route B — the engine's Earth** (`core_entropy.solve` on C14's solved T_c, inputs from `interior.solve()`):
   structural facts asserted, the numbers printed — no expectation was written.
3. Branches: no inner core → E_L = E_g = E_H = 0 exactly; an inner core → all three non-zero (same profile,
   two T_c). The H = 0 corner is emitted.
4. Labels — the history verdict is always `cannot-say (needs C20)`; no solved T_c → refuse by name; giant → out.
"""
from __future__ import annotations

import math
import sys

import cmb_flux as cf
import core_energy as ce
import core_entropy as cp
import test_core_energy as tc

PRINTED_E = {"e_r": 89.0, "e_s": 64.0, "e_l": 159.0, "e_h": -134.0, "e_g": 375.0, "e_k": 202.0, "de": 351.0}   # Table 4, MW/K


def route_a_entropy(t_c: float, dtc_dt: float = tc.DTC4, h: float = tc.H4, k: float = 50.0,
                    c_r: float = tc.CR_TABLE4_KM_K * 1e3, bracket_recovered: bool = True) -> dict:
    """Entropy terms on Nimmo's analytic core (eqs 10, 16, 17, 24, 26; I_S and I_T numeric on eqs 1, 5)."""
    R, Ri, D = tc.R_CORE, tc.R_ICB, tc.D_LEN
    t_cen = t_c * math.exp((R / D) ** 2)

    def T(r):
        return t_cen * math.exp(-(r / D) ** 2)
    m_c = tc.mass_a(R)
    m_oc = m_c - tc.mass_a(Ri)
    terms = tc.route_a_terms(t_c, dtc_dt, h, c_r)
    t_i = T(Ri)
    i_s = tc.integ(lambda r: tc.rho_a(r) * T(r), 0.0, R)
    i_t = tc.integ(lambda r: tc.rho_a(r) / T(r), 0.0, R)
    i_t_oc = tc.integ(lambda r: tc.rho_a(r) / T(r), Ri, R)
    e_r = (m_c / t_c - i_t) * h
    e_s = (tc.C_P / t_c) * (m_c - i_s / t_c) * dtc_dt
    e_l = terms["q_l"] * (t_i - t_c) / (t_c * t_i)
    e_g = terms["q_g"] / t_c
    rho_i = tc.rho_a(Ri)
    c_c = 4 * math.pi * Ri ** 2 * rho_i * tc.CHI4 / m_oc
    dri_dt = c_r * dtc_dt
    bracket = (m_oc / t_i - i_t_oc) if bracket_recovered else (i_t_oc - m_oc / t_i)
    e_h = -cp.R_H * bracket * c_c * dri_dt
    e_k = 16 * math.pi * k * R ** 5 / (5 * D ** 4)                                  # eq. 26
    return {"e_r": e_r, "e_s": e_s, "e_l": e_l, "e_h": e_h, "e_g": e_g, "e_k": e_k,
            "de": e_r + e_s + e_l + e_h + e_g - e_k, "i_s": i_s, "m_c": m_c}


def main() -> int:
    fails: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    mw = 1e6
    print("핵 엔트로피 생성 (C15) — 경로 A: Nimmo+ 2004 해석 핵으로 Table 4 의 엔트로피 여섯 항을 성분별 재현")
    a = route_a_entropy(tc.T_C4)
    for key in ("e_r", "e_s", "e_l", "e_h", "e_g", "e_k", "de"):
        got, want = a[key] / mw, PRINTED_E[key]
        inside = abs(got - want) / abs(want) <= 0.10
        ok(inside, f"1: {key} {got:.1f} MW/K vs printed {want} — outside the pre-registered 10 %")
        print(f"  [{'PASS' if inside else 'FAIL'}] {key} {got:7.1f} MW/K (인쇄 {want:6.0f}, {(got / want - 1) * 100:+.0f} %)")
    # E_k and Q_k closed as the parallel seat did
    e_k_closed = 16 * math.pi * 50.0 * tc.R_CORE ** 5 / (5 * tc.D_LEN ** 4) / mw
    q_k = 8 * math.pi * tc.R_CORE ** 3 * 50.0 * tc.T_C4 / tc.D_LEN ** 2 / 1e12
    ok(abs(e_k_closed - 202.0) < 1.0 and abs(q_k - 6.17) < 0.05, f"1: E_k {e_k_closed:.1f} (202.0) · Q_k {q_k:.2f} (6.17) closure")
    print(f"  [{'PASS' if abs(e_k_closed - 202.0) < 1.0 else 'FAIL'}] E_k 식 26 = {e_k_closed:.1f} MW/K (병렬석 202.0, 인쇄 202) · Q_k = {q_k:.2f} TW (6.17, 인쇄 6.2)")
    # the two closure-recovered readings, pinned
    no_prefactor = tc.C_P * (a["m_c"] - a["i_s"] / tc.T_C4) * tc.DTC4 / mw
    ok(abs(no_prefactor) > 1e4, "1: E_s without the 1/T_c prefactor must be grossly off (the relayed formula)")
    other = route_a_entropy(tc.T_C4, bracket_recovered=False)["e_h"] / mw
    ok(other > 0.0 and a["e_h"] < 0.0, f"1: the other bracket order must give the wrong sign (+{other:.0f} vs printed −134)")
    print(f"  [PASS] 폐합으로 회수한 둘 — E_s 는 1/T_c 없이 {no_prefactor:.0f} MW/K (10⁵ 배); E_H 는 다른 괄호 순서로 {other:+.0f} (인쇄 −134) — 읽어서가 아니라 되짚어서")

    # ── 2. the engine's Earth ─────────────────────────────────────────────────
    print("\n경로 B — 엔진 자신의 지구, C14 가 푼 T_c 위에서 (예상 없음; 입력은 interior.solve() 출력)")
    from interior import solve as _isolve
    earth = _isolve(1.0, core_mass_fraction=0.325, potential_temperature=1600.0)
    ev = earth.values
    c14 = ce.solve(1.0, 0.325, ev["core_radius"], ev["cmb_pressure"], ev["cmb_temperature"], 3760.0, body_class="rocky")
    ok(c14.applicable, f"2: C14 must solve — {c14.reason}")
    t_solved = c14.values["core_cmb_temperature_solved"]
    res = cp.solve(1.0, 0.325, ev["core_radius"], ev["cmb_pressure"], t_solved, body_class="rocky")
    ok(res.applicable, f"2: C15 must solve — {res.reason}")
    if res.applicable:
        v = res.values
        ok(v["entropy_production_min"] <= v["entropy_production"] <= v["entropy_production_max"], "2: the band must bracket the nominal")
        ok(v["entropy_history_verdict"] == "cannot-say (needs C20)", "2: the history verdict must refuse by name")
        ok(abs(v["e_l"]) + abs(v["e_g"]) + abs(v["e_h"]) == 0.0 if not v["has_inner_core_solved"] else True,
           "2: without an inner core E_L, E_g, E_H must be exactly 0")
        # 2026-09-04: two layers, two convergence orders — the profile is RK4, the integrals on it are O(h) and
        # E_R, E_s cancel one digit. Measured: ΔE moves 2.7 MW/K from 400 to 1600 steps (5 % of |ΔE|, two orders
        # below the declaration band). Frozen at 10 MW/K so a coarser sampling or a deeper cancellation rings.
        ok(v["entropy_integration_width"] < 10.0e6,
           f"2: entropy integration width {v['entropy_integration_width'] / mw:.1f} MW/K ≥ 10 — the integrals on the profile are not converged")
        print(f"  [{'PASS' if not fails else 'FAIL'}] T_c {t_solved:.0f} K · ΔE {v['entropy_production'] / mw:+.0f} MW/K "
              f"(밴드 {v['entropy_production_min'] / mw:+.0f} … {v['entropy_production_max'] / mw:+.0f}, 양수 모서리 {v['entropy_corners_positive']}/8, "
              f"H=0 {v['entropy_production_h0'] / mw:+.0f}) = E_R {v['e_r'] / mw:.0f} + E_s {v['e_s'] / mw:.0f} + E_L {v['e_l'] / mw:.0f} "
              f"+ E_H {v['e_h'] / mw:.0f} + E_g {v['e_g'] / mw:.0f} − E_k {v['e_k'] / mw:.0f} · 내핵 {'있음' if v['has_inner_core_solved'] else '없음'} · "
              f"0 가로지름 {v['entropy_band_straddles_zero']} · 적분 폭(4×) {v['entropy_integration_width'] / mw:.1f} MW/K · 이력 {v['entropy_history_verdict']}")

    # ── 3. both branches on one profile ──────────────────────────────────────
    print("\n분기 — 내핵 없음(E_L = E_g = E_H = 0) / 내핵 있음, 같은 프로파일의 두 T_c")
    r_cmb, m_core, p_cmb = ev["core_radius"] * cf.R_EARTH_M, 0.325 * cf.M_EARTH_KG, ev["cmb_pressure"] * 1e9
    p_cold = ce.core_profile("fe_prem", p_cmb, 3760.0, r_cmb, m_core)
    e_cold = cp.entropy_terms(p_cold, ce.core_terms(p_cold))
    p_hot = ce.core_profile("fe_prem", p_cmb, 4000.0, r_cmb, m_core)
    e_hot = cp.entropy_terms(p_hot, ce.core_terms(p_hot))
    ok(e_cold["e_l"] > 0.0 and e_cold["e_g"] > 0.0 and e_cold["e_h"] < 0.0, "3: at 3760 K (inner core) E_L, E_g > 0 and E_H < 0")
    ok(e_hot["e_l"] == e_hot["e_g"] == e_hot["e_h"] == 0.0, "3: at 4000 K (all liquid) E_L = E_g = E_H = 0")
    print(f"  [{'PASS' if e_cold['e_l'] > 0 and e_hot['e_l'] == 0 else 'FAIL'}] 3760 K: ΔE {e_cold['delta_e'] / mw:+.0f} (E_L {e_cold['e_l'] / mw:.0f} E_g {e_cold['e_g'] / mw:.0f} E_H {e_cold['e_h'] / mw:.0f}) · "
          f"4000 K: ΔE {e_hot['delta_e'] / mw:+.0f} (E_L = E_g = E_H = 0)")

    # ── 4. labels ─────────────────────────────────────────────────────────────
    print("\n라벨")
    none = cp.solve(1.0, 0.325, 0.547, 135.3, None, body_class="rocky")
    ok(not none.applicable and cp.NO_INPUT in none.reason, "4: no solved T_c → refuse by name")
    giant = cp.solve(120.0, 0.1, 0.3, 1000.0, 6000.0, body_class="giant")
    ok(not giant.applicable, "4: giant out of domain")
    print(f"  [{'PASS' if not none.applicable and not giant.applicable else 'FAIL'}] 풀린 T_c 없음 → 이름 대며 거절 · 거대행성 → 도메인 밖")

    if fails:
        print(f"\nFAIL: {len(fails)}")
        for f in fails:
            print("  ·", f)
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
