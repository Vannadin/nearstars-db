# 핵 에너지 수지의 앵커 — Nimmo+ 2004 해석 핵(경로 A)으로 Table 4 를 성분별 재현, 엔진 지구(경로 B) 보고, 거절 라벨 (C14)
"""Anchor the core energy balance (C14).

    python3 engine/test_core_energy.py

1. **Route A — Nimmo's analytic core, transcribed here and only here** (eqs 1–10, 16–21, Table 1/2/4):
   Table 4 reproduced **component by component** on the paper's own inputs — Q_s 2.0 · Q_L 2.6 · Q_g 1.6 ·
   Q_R 2.9 · Q_k 6.2 TW, T_i 5581 K — each within the pre-registered 10 % of its printed one-decimal value;
   and the root-find on the paper's own mantle side (eq. 29 base 2694 K, Brief 60) returns T_c ≈ 4155 K.
   A sum that matches with components that do not is not a reproduction. ψ's zero point is shown to cancel.
   C_r: Gubbins −9.56 (printed, other model) · Table 4 ratio −13.5 (our division) · slope-derived −26 (ours)
   — three labels, not mixed; the slope value's factor-2 miss is pinned as the knife-edge it is.
2. **Route B — the engine's own Earth** (`core_energy.solve`): structural facts asserted (a root exists, the
   balance closes to machine precision, the profile closes M_core to < 1 %, all four band corners solve), the
   numbers **printed, not asserted** — no expectation was written for them (pre-registration ②).
3. **Branch ⑤** (no inner core → Q_L = Q_g = 0) and its complement (an inner core → Q_L, Q_g > 0) are both
   exercised on the same profile at two T_c.
4. Labels — undeclared core-side temperature → refuse by name; giant → out of domain.
"""
from __future__ import annotations

import math
import sys

import cmb_flux as cf
import core_energy as ce
import mantle_flux as mf

G = cf.G_NEWTON
# ── Nimmo+ 2004 Table 1 (layout line 436) · Table 2 (532) · Table 4 (715) — the paper's Earth ──
RHO_CEN, L_LEN, D_LEN, R_CORE, R_ICB = 12500.0, 7272e3, 5969e3, 3480e3, 1220e3
C_P, L_H, BETA_C, CHI4 = 840.0, 750e3, 1.1, 0.0430          # Table 4 prints χ 4.30 wt %
T_C4, T_I4, DTC4, H4 = 4155.0, 5581.0, -33.0 / ce.GYR_S, 1.5e-12
P_C2, TM0, TM1, TM2, THETA = 139e9, 1695.0, 10.9e-12, -8.0e-24, 0.11   # Table 2, eqs 7 and 40
PRINTED = {"q_s": 2.0, "q_l": 2.6, "q_g": 1.6, "q_r": 2.9, "q_k": 6.2, "q_c": 9.0}     # Table 4, TW
CR_GUBBINS_KM_K = -9.56                                     # Table 3 note — Gubbins' model, printed
CR_TABLE4_KM_K = -444.0 / 33.0                              # our division of two printed Table 4 values


def rho_a(r):          # eq. 1
    return RHO_CEN * math.exp(-(r / L_LEN) ** 2)


def mass_a(r):         # eq. 3
    return 4 * math.pi * RHO_CEN * (-(L_LEN ** 2 / 2) * r * math.exp(-(r / L_LEN) ** 2)
                                    + (L_LEN ** 3 * math.sqrt(math.pi) / 4) * math.erf(r / L_LEN))


def psi_a(r):          # eq. 18 (its zero point cancels — checked below)
    return (2 * math.pi / 3) * G * RHO_CEN * r * r * (1 - 3 * r * r / (10 * L_LEN ** 2))


def p_a(r):            # eq. 7
    def f(x):
        return (3 * x * x / 10 - L_LEN ** 2 / 5) * math.exp(-(x / L_LEN) ** 2)
    return P_C2 + (4 * math.pi * G * RHO_CEN ** 2 / 3) * (f(R_CORE) - f(r))


def t_melt_a(p):       # eq. 40
    return TM0 * (1 - THETA) * (1 + TM1 * p + TM2 * p * p)


def integ(f, a, b, n=4000):
    h = (b - a) / n
    return sum(f(a + (i + 0.5) * h) * 4 * math.pi * (a + (i + 0.5) * h) ** 2 * h for i in range(n))


def route_a_terms(t_c: float, dtc_dt: float = DTC4, h: float = H4, c_r: float = CR_TABLE4_KM_K * 1e3,
                  psi=psi_a) -> dict:
    t_cen = t_c * math.exp((R_CORE / D_LEN) ** 2)                       # eq. 5 at the CMB
    m_c = mass_a(R_CORE)
    m_oc = m_c - mass_a(R_ICB)
    a2 = 1.0 / (1.0 / L_LEN ** 2 + 1.0 / D_LEN ** 2)                     # eq. 9
    a = math.sqrt(a2)
    i_s = 4 * math.pi * t_cen * RHO_CEN * (-(a2 * R_CORE / 2) * math.exp(-(R_CORE / a) ** 2)
                                          + (a ** 3 * math.sqrt(math.pi) / 4) * math.erf(R_CORE / a))   # eq. 8
    rho_i = rho_a(R_ICB)
    c_c = 4 * math.pi * R_ICB ** 2 * rho_i * CHI4 / m_oc                 # eq. 20
    q_s = -(C_P / t_c) * i_s * dtc_dt                                    # eq. 10
    q_l = 4 * math.pi * R_ICB ** 2 * L_H * rho_i * c_r * dtc_dt          # eq. 17 with C_r dT_c/dt = dR_i/dt
    q_g = (integ(lambda r: rho_a(r) * psi(r), R_ICB, R_CORE) - m_oc * psi(R_ICB)) * BETA_C * c_c * c_r * dtc_dt   # eq. 19
    q_r = m_c * h                                                         # eq. 16
    q_k = 4 * math.pi * R_CORE ** 2 * 50.0 * (2 * R_CORE / D_LEN ** 2) * t_c   # k |dT/dr| at the CMB, eq. 5 with Table 1's k
    t_i = t_cen * math.exp(-(R_ICB / D_LEN) ** 2)
    return {"q_s": q_s, "q_l": q_l, "q_g": q_g, "q_r": q_r, "q_k": q_k, "t_i": t_i, "m_c": m_c,
            "q_total": q_s + q_l + q_g + q_r}


def main() -> int:
    fails: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    tw = 1e12
    # ── 1. route A: Table 4 component by component ────────────────────────
    print("핵 에너지 수지 (C14) — 경로 A: Nimmo+ 2004 해석 핵으로 Table 4 를 성분별 재현")
    t = route_a_terms(T_C4)
    for k in ("q_s", "q_l", "q_g", "q_r", "q_k"):
        got, want = t[k] / tw, PRINTED[k]
        ok(abs(got - want) / want <= 0.10, f"1: {k} {got:.2f} TW vs printed {want} — outside the pre-registered 10 %")
        print(f"  [{'PASS' if abs(got - want) / want <= 0.10 else 'FAIL'}] {k} {got:.2f} TW (인쇄 {want}, {(got / want - 1) * 100:+.0f} %)")
    ok(abs(t["t_i"] - T_I4) < 50.0, f"1: T_i {t['t_i']:.0f} K vs printed {T_I4}")
    ok(abs(t["m_c"] - 1.94e24) / 1.94e24 < 0.02, f"1: M_c {t['m_c']:.3e} vs PREM 1.94e24")
    print(f"  [{'PASS' if abs(t['t_i'] - T_I4) < 50 else 'FAIL'}] T_i {t['t_i']:.0f} K (인쇄 {T_I4:.0f}) · M_c {t['m_c']:.3e} kg · 합 {t['q_total'] / tw:.2f} TW (인쇄 Q_C 9.0, 성분 합 9.1)")
    # ψ zero point cancels
    t_shift = route_a_terms(T_C4, psi=lambda r: psi_a(r) - psi_a(R_CORE))
    ok(abs(t_shift["q_g"] - t["q_g"]) < 1e-6 * abs(t["q_g"]), "1: ψ's zero point must cancel in Q_g")
    print(f"  [{'PASS' if abs(t_shift['q_g'] - t['q_g']) < 1e-6 * abs(t['q_g']) else 'FAIL'}] ψ 영점(r=0 / CMB) 이 Q_g 에서 상쇄된다")
    # C_r — three labelled values, none mixed
    h = 1e3
    t_cen = T_C4 * math.exp((R_CORE / D_LEN) ** 2)
    dt_ad = (t_cen * math.exp(-((R_ICB + h) / D_LEN) ** 2) - t_cen * math.exp(-((R_ICB - h) / D_LEN) ** 2)) / (2 * h)
    dt_m = (t_melt_a(p_a(R_ICB + h)) - t_melt_a(p_a(R_ICB - h))) / (2 * h)
    c_r_slope = (t["t_i"] / T_C4) / (dt_m - dt_ad) / 1e3
    ok(-35.0 < c_r_slope < -20.0, f"1: slope-derived C_r {c_r_slope:.1f} km/K — recorded −26.4 (factor 2 from the Table 4 ratio)")
    print(f"  [{'PASS' if -35 < c_r_slope < -20 else 'FAIL'}] C_r: Gubbins {CR_GUBBINS_KM_K} (인쇄, 다른 모형) · Table 4 비 {CR_TABLE4_KM_K:.2f} (우리 나눗셈) · "
          f"기울기 도출 {c_r_slope:.1f} km/K (우리; 융해곡선 {dt_m * 1e3:.3f} vs 단열선 {dt_ad * 1e3:.3f} K/km, 거의 나란해 칼날) — 섞지 않는다")
    # root-find on the paper's own mantle side
    t_m_paper = 1603.0 * math.exp(mf.ALPHA_M * mf.EARTH_G * 2.89e6 / mf.C_PM)     # eq. 29, Brief 60

    def f_paper(tc):
        return cf.bottom_layer(tc, t_m_paper, R_CORE)["q_c_w"] - route_a_terms(tc)["q_total"]
    lo, hi = t_m_paper + 1.0, 6000.0
    f_lo = f_paper(lo)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if (f_paper(mid) > 0.0) == (f_lo > 0.0):
            lo = mid
        else:
            hi = mid
    root = 0.5 * (lo + hi)
    ok(abs(root - T_C4) < 20.0, f"1: root T_c {root:.0f} K vs Table 4 {T_C4}")
    print(f"  [{'PASS' if abs(root - T_C4) < 20 else 'FAIL'}] 논문 자신의 맨틀 쪽(식 29 밑 {t_m_paper:.0f} K)에서 근 T_c {root:.0f} K (Table 4 {T_C4:.0f})")

    # ── 2. route B: the engine's Earth — printed, not asserted ──────────────
    print("\n경로 B — 엔진 자신의 지구 (선언 3760 K 옆에 보고; 예상 없음)")
    res = ce.solve(1.0, 0.325, 0.547, 135.3, 2526.0, 3760.0, core_material="fe_prem", body_class="rocky")
    ok(res.applicable, f"2: engine Earth must solve — {res.reason}")
    if res.applicable:
        v = res.values
        ok(abs(v["balance_residual"]) < 1e-9, f"2: balance residual {v['balance_residual']:.1e}")
        ok(abs(v["core_profile_mass_residual"]) < 0.01, f"2: profile mass residual {v['core_profile_mass_residual']:+.4f}")
        ok(v["band_corners_with_root"] == 4, f"2: band corners with a root {v['band_corners_with_root']}/4")
        print(f"  [{'PASS' if not fails else 'FAIL'}] T_c 풀림 {v['core_cmb_temperature_solved']:.0f} K "
              f"(밴드 {v['core_cmb_temperature_solved_min']:.0f}–{v['core_cmb_temperature_solved_max']:.0f}; 선언 {v['core_cmb_temperature_declared']:.0f}, "
              f"차 {v['core_cmb_solved_minus_declared']:+.0f} K) · Q_C {v['q_cmb_solved'] / tw:.2f} = s {v['q_s'] / tw:.2f} + L {v['q_l'] / tw:.2f} + g {v['q_g'] / tw:.2f} + R {v['q_r'] / tw:.2f} TW · "
              f"내핵 {'있음' if v['has_inner_core_solved'] else '없음'} · 프로파일 중심압 {v['core_center_pressure_solved']:.0f} GPa, 질량 잔차 {v['core_profile_mass_residual']:+.4f} · 잔차 {v['balance_residual']:.1e}")
    # ── 3. both branches of the inner-core question on the same profile ────
    print("\n분기 ⑤ — 내핵 없음(Q_L = Q_g = 0)과 내핵 있음, 같은 프로파일의 두 T_c 에서")
    r_cmb, m_core = 0.547 * cf.R_EARTH_M, 0.325 * cf.M_EARTH_KG
    _, _, cold = ce.balance(3300.0, 2526.0, "fe_prem", 135.3e9, r_cmb, m_core)
    _, _, hot = ce.balance(4000.0, 2526.0, "fe_prem", 135.3e9, r_cmb, m_core)
    ok(cold["inner_core"] is not None and cold["q_l"] > 0.0 and cold["q_g"] > 0.0, "3: at 3300 K the profile must carry an inner core with Q_L, Q_g > 0")
    ok(hot["inner_core"] is None and hot["q_l"] == 0.0 and hot["q_g"] == 0.0 and hot.get("core_status") == "all_liquid",
       "3: at 4000 K the profile must be all liquid with Q_L = Q_g = 0")
    print(f"  [{'PASS' if cold['inner_core'] and hot['inner_core'] is None else 'FAIL'}] 3300 K: R_i {cold['inner_core']['r_i'] / 1e3 if cold['inner_core'] else 0:.0f} km, "
          f"Q_L {cold['q_l'] / tw:.2f} Q_g {cold['q_g'] / tw:.2f} TW · 4000 K: {hot.get('core_status')}, Q_L = Q_g = 0")
    # ── 4. labels ───────────────────────────────────────────────────────────
    print("\n라벨")
    nodecl = ce.solve(1.0, 0.325, 0.547, 135.3, 2526.0, None, body_class="rocky")
    ok(not nodecl.applicable and ce.NO_INPUTS in nodecl.reason, "4: undeclared core-side temperature must refuse by name")
    giant = ce.solve(120.0, 0.1, 0.3, 1000.0, 5000.0, 6000.0, body_class="giant")
    ok(not giant.applicable, "4: giant out of domain")
    print(f"  [{'PASS' if not nodecl.applicable and not giant.applicable else 'FAIL'}] 미선언 → 이름 대며 거절 · 거대행성 → 도메인 밖")

    if fails:
        print(f"\nFAIL: {len(fails)}")
        for f in fails:
            print("  ·", f)
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
