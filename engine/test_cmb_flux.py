# 핵-맨틀 경계 열류의 앵커 — 논문 자신의 값으로 전사 폐합(140 km · 9 TW), 포텐셜 온도 오독 고정, 단열 열류, 거절 라벨, 로스터 (Brief 60)
"""Anchor Nimmo+ 2004 eqs 37–39 and the adiabatic flow.

    python3 engine/test_cmb_flux.py

1. Transcription closure on the paper's own inputs — T_c 4161 K, T̃_m 2694 K (eq. 29 on 1603 K at
   2890 km), R 3480 km: δ_b 144 km vs printed 140, Q_C 8.9 TW vs printed 9. The potential-temperature
   reading (T_m = 1603) gives 738 km — pinned so nobody re-adopts it.
2. k_b = κ_b ρ_m C_pm = 5.76; the ζ × κ_b band brackets the nominal.
3. Adiabatic flow on the paper-shaped core (fe_prem, 135.3 GPa, 3760 K, r 0.547 R⊕, M_core 0.325 M⊕):
   ~6.6 TW at k 50 (paper 6.2 on its own density model), band 4.0–9.3 over k 30–70.
4. Labels — no declared core-side temperature → refuse by name; T_c ≤ T̃_m → refuse; giant → out of domain.
5. Roster — engine Earth (declared T_c 3760, adiabat base 2526) lands OUTSIDE the paper's 4.5–9 TW
   (≈ 2.75 TW) and below its adiabat: branch ②, reported not tuned.
"""
from __future__ import annotations

import math
import sys

import cmb_flux as cf
import mantle_flux as mf


def main() -> int:
    fails: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # ── 1. transcription closure ────────────────────────────────────────────
    t_m_base = 1603.0 * math.exp(mf.ALPHA_M * mf.EARTH_G * 2.89e6 / mf.C_PM)     # eq. 29
    ok(abs(t_m_base - 2694.0) < 2.0, f"1: eq. 29 base temperature {t_m_base:.0f} K, expected 2694")
    p = cf.bottom_layer(4161.0, t_m_base, 3.48e6)
    ok(abs(p["delta_b_m"] / 1e3 - 144.2) < 1.0, f"1: δ_b {p['delta_b_m'] / 1e3:.1f} km, expected 144.2 (printed 140)")
    ok(abs(p["q_c_w"] / 1e12 - 8.92) < 0.05, f"1: Q_C {p['q_c_w'] / 1e12:.2f} TW, expected 8.92 (printed 9)")
    ok(abs(p["delta_b_m"] / 1e3 - cf.PAPER["delta_b_km"]) / cf.PAPER["delta_b_km"] < 0.04, "1: within 4 % of the printed 140 km")
    wrong = cf.bottom_layer(4161.0, 1603.0, 3.48e6)
    ok(abs(wrong["delta_b_m"] / 1e3 - 738.0) < 5.0, f"1: the potential-temperature reading must give ~738 km, got {wrong['delta_b_m'] / 1e3:.0f}")
    # ── 2. k_b and the band ─────────────────────────────────────────────────
    ok(abs(cf.K_B - 5.76) < 1e-9, f"2: k_b {cf.K_B}, expected 5.76")
    band = [cf.bottom_layer(4161.0, t_m_base, 3.48e6, z, kb)["q_c_w"] for z in mf.ZETA_RANGE for kb in cf.KAPPA_B_RANGE]
    ok(min(band) < p["q_c_w"] < max(band), "2: the ζ × κ_b band must bracket the nominal")
    # ── 3. adiabatic flow ───────────────────────────────────────────────────
    r = 0.547 * cf.R_EARTH_M
    ad = cf.adiabatic_flow("fe_prem", 135.3e9, 3760.0, r, 0.325 * cf.M_EARTH_KG)
    ok(6.3 < ad["q_ad_w"] / 1e12 < 7.0, f"3: Q_ad {ad['q_ad_w'] / 1e12:.2f} TW at k 50, expected ~6.6 (paper 6.2)")
    ok(0.8 < abs(ad["dt_dr_ad"]) * 1e3 < 1.0, f"3: |dT/dr| {abs(ad['dt_dr_ad']) * 1e3:.2f} K/km, expected ~0.87")
    # ── 4. labels ───────────────────────────────────────────────────────────
    nodecl = cf.solve(1.0, 0.325, 0.547, 135.3, 2526.0, 2526.0, core_cmb_declared=False)
    ok(not nodecl.applicable and cf.NO_JUMP in nodecl.reason, "4: undeclared core-side temperature must refuse by name")
    inverted = cf.solve(1.0, 0.325, 0.547, 135.3, 2526.0, 2400.0, core_cmb_declared=True)
    ok(not inverted.applicable and "점프" in inverted.reason, "4: T_c ≤ T̃_m must refuse")
    giant = cf.solve(120.0, 0.1, 0.3, 1000.0, 5000.0, 6000.0, True, body_class="giant")
    ok(not giant.applicable, "4: giant out of domain")
    # ── 5. roster ───────────────────────────────────────────────────────────
    earth = cf.solve(1.0, 0.325, 0.547, 135.3, 2526.0, 3760.0, core_cmb_declared=True, body_class="rocky")
    v = earth.values
    ok(earth.applicable and 2.6 < v["q_cmb"] / 1e12 < 2.9 and not v["q_cmb_in_paper_range"],
       f"5: engine Earth Q_CMB {v.get('q_cmb', 0) / 1e12:.2f} TW must land outside 4.5–9 (branch ②)")
    ok(v["cmb_flux_verdict"] == cf.SUB_ADIABATIC and v["q_cmb"] < v["q_adiabat"], "5: engine Earth is sub-adiabatic at the declared T_c")
    ok(380.0 < v["cmb_boundary_layer"] < 410.0, f"5: δ_b {v['cmb_boundary_layer']:.0f} km, expected ~394")
    ok(set(v) <= set(earth.units), "5: every value carries a unit")
    ok(any("선언" in n and "γ = 1.5" in n for n in earth.notes), "5: the notes must carry the declared k and the γ caveat")

    for f in fails:
        print(f"  [FAIL] {f}")
    if not fails:
        print(f"  [PASS] 핵-맨틀 경계 열류 — 논문 폐합 δ_b {p['delta_b_m'] / 1e3:.0f} km / Q_C {p['q_c_w'] / 1e12:.1f} TW (인쇄 140 / 9) · "
              f"포텐셜 오독 738 km 고정 · k_b 5.76 · Q_ad {ad['q_ad_w'] / 1e12:.2f} TW (k 50) · 거절 3건 · "
              f"엔진 지구 {v['q_cmb'] / 1e12:.2f} TW 범위 밖(②)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
