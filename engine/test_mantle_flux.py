# 함의 열류 사슬의 앵커 — Table 2 전사 폐합(42 TW → 1614 K), ζ 민감도의 두 방향, 판정 라벨, 로스터 (Brief 46)
"""Anchor Nimmo+ 2004 eqs 34–36 and the heat-flow consistency verdict.

    python3 engine/test_mantle_flux.py

1. Transcription closure — at T_m 1600 K with the paper's R_p and g: δ_t 58.8 km, F_t 0.0768 W/m²,
   Q_M 39.5 TW; inverting for the paper's own present-day ~42 TW gives T_m = 1614 K (Earth's
   canonical potential temperature). This is what licenses the derived k_t = κ_t ρ_m C_pm.
2. Sensitivity, both directions — forward at fixed T_m: 37.8 / 39.5 / 41.4 TW across ζ 0.5/1.0/1.5
   ×10⁻² (±4 %); inverted for 42 TW: 1639 / 1614 / 1603 K (±1 %).
3. Labels — every verdict is a registered string and carries the calibrated-at-source condition;
   missing T_m and missing budget refuse by name.
4. Roster — Earth's declared 1600 K against its 21.3 TW budget lands inside the secular gap
   (ratio ≈ 1.85); a cold and a hot declaration land in the two flag branches.
"""
from __future__ import annotations

import sys

import mantle_flux as mf
import radiogenic as rg


def main() -> int:
    fails: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # ── 1. transcription closure ────────────────────────────────────────────
    ok(abs(mf.K_T - 3.456) < 1e-9, f"1: k_t = κ ρ C_p = {mf.K_T:.4f}, expected 3.456 W/(m K)")
    c = mf.implied_flux(1600.0, mf.EARTH_G, mf.EARTH_R_P)
    ok(abs(c["delta_t_m"] / 1e3 - 58.8) < 0.2, f"1: δ_t {c['delta_t_m'] / 1e3:.1f} km, expected 58.8")
    ok(abs(c["f_t_w_m2"] - 0.0768) < 0.0003, f"1: F_t {c['f_t_w_m2']:.4f} W/m², expected 0.0768")
    ok(abs(c["q_m_w"] / 1e12 - 39.5) < 0.2, f"1: Q_M {c['q_m_w'] / 1e12:.1f} TW, expected 39.5")
    t_inv = mf.invert_for_flow(mf.PAPER_PRESENT_DAY_Q_TW * 1e12)
    ok(abs(t_inv - 1614.0) < 1.5, f"1: T_m for 42 TW = {t_inv:.1f} K, expected 1614 (closure on the derived k_t)")
    # the paper prints its own present-day potential temperature: 1330 °C (McKenzie & Bickle 1988) = 1603 K
    ok(abs(t_inv - 1603.15) < 15.0, f"1: 42 TW ← {t_inv:.1f} K against the paper's printed 1603 K — must agree within ~15 K")
    # ── 2. sensitivity, both directions ─────────────────────────────────────
    fwd = [mf.implied_flux(1600.0, mf.EARTH_G, mf.EARTH_R_P, z)["q_m_w"] / 1e12 for z in (0.5e-2, 1.0e-2, 1.5e-2)]
    ok(all(abs(a - b) < 0.2 for a, b in zip(fwd, (37.8, 39.5, 41.4))), f"2: forward ζ band {fwd}, expected 37.8/39.5/41.4")
    inv = [mf.invert_for_flow(42e12, zeta=z) for z in (0.5e-2, 1.0e-2, 1.5e-2)]
    ok(all(abs(a - b) < 1.5 for a, b in zip(inv, (1639.0, 1614.0, 1603.0))), f"2: inverted ζ band {[round(x) for x in inv]}, expected 1639/1614/1603")
    ok((max(fwd) - min(fwd)) / fwd[1] < 0.10 and (max(inv) - min(inv)) / inv[1] < 0.03,
       "2: forward ±4 % and inverted ±1 % — the steepness cuts one way")
    # ── 3. labels ───────────────────────────────────────────────────────────
    labels = {mf.CONSISTENT, mf.TOO_HOT, mf.TOO_COLD, mf.NO_T, mf.NO_BUDGET}
    g_e, r_e = 9.82, 6.371e6
    cases = [mf.consistency(1600.0, 21.3e12, g_e, r_e), mf.consistency(None, 21.3e12, g_e, r_e),
             mf.consistency(1600.0, None, g_e, r_e), mf.consistency(1400.0, 21.3e12, g_e, r_e),
             mf.consistency(1800.0, 21.3e12, g_e, r_e)]
    for x in cases:
        ok(x["verdict"] in labels, f"3: unregistered verdict {x['verdict']!r}")
        ok("calibrated at source" in x["notes"][0] or x["verdict"] == mf.NO_T, "3: the note must carry calibrated-at-source")
    ok(cases[1]["verdict"] == mf.NO_T and cases[2]["verdict"] == mf.NO_BUDGET, "3: missing inputs must refuse by name")
    # ── 4. roster and the two flags ─────────────────────────────────────────
    ok(abs(mf.SECULAR_RATIO_MAX - 3.0) < 1e-12 and abs(mf.UREY_FLOOR - 1 / 3) < 1e-12, "4: the ceiling is a Urey floor of 1/3 (ratio 3), soft")
    ok(cases[0]["verdict"] == mf.CONSISTENT and 1.7 < cases[0]["ratio"] < 2.0,
       f"4: Earth 1600 K vs 21.3 TW → {cases[0]['verdict']} ratio {cases[0]['ratio']}")
    ok(cases[3]["verdict"] == mf.TOO_COLD, f"4: 1400 K must flag less-than-radiogenic, got {cases[3]['verdict']}")
    ok(cases[4]["verdict"] == mf.TOO_HOT, f"4: 1800 K must flag more-than-secular, got {cases[4]['verdict']}")
    earth = rg.solve(1.0, 0.325, 1.0, "rocky", 4.54, potential_temperature=1600.0)
    ok(earth.applicable and abs(earth.values["implied_surface_heat_flow"] / earth.values["radiogenic_power"] - 1.85) < 0.03,
       f"4: Earth ratio on the declared R⊕ must be 1.85, got {earth.values['implied_surface_heat_flow'] / earth.values['radiogenic_power']:.3f}")
    ok(earth.applicable and earth.values["heat_flow_consistency"] == mf.CONSISTENT
       and 55.0 < earth.values["mantle_top_boundary_layer"] < 62.0,
       f"4: recipe Earth → {earth.values.get('heat_flow_consistency')}, δ_t {earth.values.get('mantle_top_boundary_layer')}")
    pandora = rg.solve(0.6447, 0.325, 0.8984, "rocky", 5.3)
    ok(pandora.applicable and pandora.values["heat_flow_consistency"] == mf.NO_T,
       "4: a body without a declared potential temperature must say cannot-say (⑤), not default")

    # ── 5. Brief 57 — the band, its four widths, and the bracket refusal ───
    band = earth.values
    ok(band["mantle_temperature_floor_verdict"] == mf.BAND_OK
       and 1050.0 < band["mantle_temperature_floor_min"] < 1070.0 and 1480.0 < band["mantle_temperature_floor_max"] < 1500.0,
       f"5: Earth floor band expected ~1060–1490 K, got {band['mantle_temperature_floor_min']}–{band['mantle_temperature_floor_max']} ({band['mantle_temperature_floor_verdict']})")
    wz, ws, wd, wt = (band["mantle_temperature_width_zeta"], band["mantle_temperature_width_set"],
                      band["mantle_temperature_width_denominator"], band["mantle_temperature_width_surface"])
    ok(all(x is not None for x in (wz, ws, wd, wt)) and 0.5 < max(wz, ws, wd) / min(wz, ws, wd) < 2.5,
       f"5: ζ/set/denominator widths must be of one order (none dominates), got {wz:.0f}/{ws:.0f}/{wd:.0f} K")
    ok(wt is not None and 0.0 < wt < wd, f"5: the T_s width must be present and the smallest, got {wt}")
    ok(abs(mf.invert_for_flow(14.81e12, 9.8, 6.4e6) - 1379.3) < 1.0, "5: 14.81 TW → 1379 K (the brief's own number)")
    ok(mf.invert_for_flow(0.10e12, 1.8, 1.82e6) is None, "5: an Io-mass budget below the bracket must return None, not 1000.0")
    io = rg.solve(0.015, 0.20, 0.286, "moon", 4.5)
    ok(io.applicable and io.values["mantle_temperature_floor_verdict"] == mf.BAND_OPEN_BELOW
       and io.values["mantle_temperature_floor_min"] is None and io.values["mantle_temperature_floor_max"] is not None,
       f"5: Io-mass body: part of the family under the floor → open below, got {io.values.get('mantle_temperature_floor_verdict')}")
    # the whole family under the floor is not reached by any roster-shaped body (budget ∝ M, Q_M(1000 K) ∝ R²
    # — a 0.001 M⊕ body still has a corner at 1235 K); the branch is pinned on the function directly.
    whole = mf.radiogenic_temperature_band({"a": {"mantle_w": 1e9, "total_w": 2e9}}, 9.8, 6.4e6)
    ok(whole["verdict"] == mf.BELOW_BRACKET and whole["t_max"] is None, f"5: whole family under the floor → refuse by name, got {whole['verdict']}")
    above = mf.radiogenic_temperature_band({"a": {"mantle_w": 1e20, "total_w": 2e20}}, 9.8, 6.4e6)
    ok(above["verdict"] == mf.ABOVE_BRACKET, f"5: whole family above the ceiling → refuse by name, got {above['verdict']}")
    ok(mf.invert_for_flow(1e20, 9.8, 6.4e6) is None, "5: a budget above the ceiling must return None too")
    ok(all(k in earth.units for k in band if k.startswith("mantle_temperature")), "5: every band value carries a unit")

    for f in fails:
        print(f"  [FAIL] {f}")
    if not fails:
        print(f"  [PASS] 함의 열류 — 1600 K → {c['q_m_w'] / 1e12:.1f} TW, 42 TW ← {t_inv:.0f} K (k_t 도출 폐합) · ζ 순방향 "
              f"{fwd[0]:.1f}–{fwd[2]:.1f} TW / 역방향 {inv[2]:.0f}–{inv[0]:.0f} K · 지구 {cases[0]['verdict']} "
              f"(비 {cases[0]['ratio']:.2f}) · 1400/1800 K 두 플래그 · 미선언 cannot-say")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
