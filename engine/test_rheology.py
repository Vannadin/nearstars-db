# 완화 판정 축의 앵커 — 전사 검산, 문턱 불감성의 측정, 라벨 규율, 로스터 판정 (Brief 39)
"""Anchor the figure-relaxation verdict on what Brief 39 measured.

    python3 engine/test_rheology.py

1. Transcription closure — the two printed laws return their own printed anchors
   (Rovira-Navarro η(T_s) = η_s exactly; Monteux ~10²³ Pa·s at the parallel seat's
   (4500, 2400) pair and four orders lower at (4000, 2600)); the two laws agree to 18 % at
   T_sol/T_liq = 0.80 (survey ㉑).
2. The insensitivity that justifies relayed constants — the 4.5 Gyr threshold family spans
   ~300 K across two decades of η_s and 300–540 kJ/mol, and ~70 K across 0.1–10 Gyr. The
   directing seat's table (689–986 K) reproduces at T_s = 1600 K; the engine's own 0 GPa
   solidus (1661 K) shifts it to 700–1009 K. Both pinned, so a change in either the law or
   the solidus chain rings here.
3. Label discipline — every verdict is one of the registered strings and carries the
   condition; refusals refuse by name (no temperature, no silicate, solidus undefined).
4. Roster measurement — Earth (T_pot 1600 K) relaxes on both laws; the inside-spread and
   cannot-relax branches are reachable and land where the family says.
"""
from __future__ import annotations

import math
import sys

import eos
import rheology as rh


def main() -> int:
    fails: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # ── 1. transcription closure ────────────────────────────────────────────
    ok(rh.viscosity_rovira(1400.0, 1400.0) == rh.RN_ETA_S_PA_S,
       "1: Rovira-Navarro η(T_s) must equal η_s exactly")
    eta_m = rh.viscosity_monteux(2400.0, 4500.0)
    ok(0.5e23 < eta_m < 1.5e23, f"1: Monteux (4500, 2400) gives {eta_m:.2e}, not ~1e23")
    eta_m2 = rh.viscosity_monteux(2600.0, 4000.0)
    ok(3.0 < math.log10(eta_m / eta_m2) < 5.0,
       f"1: Monteux (4000, 2600) should sit ~4 orders below; got {math.log10(eta_m / eta_m2):.2f}")
    agree = rh.viscosity_monteux(1400.0, 1400.0 / 0.80) / rh.RN_ETA_S_PA_S
    ok(abs(agree - 1.18) < 0.01, f"1: the two laws at T_sol/T_liq = 0.80 differ by {agree:.3f}×, not 1.18×")

    # ── 2. insensitivity — the whole justification for relayed constants ────
    age = 4.5 * rh.GYR_S
    tab = {(ea, es): rh.threshold_temperature_k(age, 1600.0, es, ea)
           for ea in rh.RN_E_A_RANGE_J_MOL for es in rh.RN_ETA_S_RANGE_PA_S}
    want = {(300e3, 1e15): 689, (300e3, 1e16): 720, (300e3, 1e17): 755,
            (540e3, 1e15): 922, (540e3, 1e16): 953, (540e3, 1e17): 986}
    for k, w in want.items():
        ok(abs(tab[k] - w) < 1.5, f"2: threshold(T_s=1600, E_a={k[0]/1e3:.0f}, η_s={k[1]:.0e}) = {tab[k]:.1f}, directing seat {w}")
    ts0 = eos.silicate_solidus(0.0)
    ok(abs(ts0 - 1661.2) < 0.5, f"2: engine 0 GPa solidus moved: {ts0:.1f} K (was 1661.2)")
    fam = rh.threshold_spread_k(age, ts0)
    lo, hi = min(fam.values()), max(fam.values())
    ok(abs(lo - 700.4) < 1.5 and abs(hi - 1009.0) < 1.5,
       f"2: engine-solidus family {lo:.1f}–{hi:.1f} K, expected 700–1009")
    ok(250.0 < hi - lo < 350.0, f"2: family width {hi - lo:.0f} K — the ~300 K insensitivity claim")
    t_young = rh.threshold_temperature_k(0.1 * rh.GYR_S, ts0)
    t_old = rh.threshold_temperature_k(10.0 * rh.GYR_S, ts0)
    ok(50.0 < t_young - t_old < 100.0, f"2: age 0.1→10 Gyr moves the threshold {t_young - t_old:.0f} K, expected ~70")
    # τ_M spans >20 decades across mantle temperatures while the family is worth ~2 decades
    span = math.log10(rh.viscosity_rovira(500.0, ts0) / rh.viscosity_rovira(2500.0, ts0))
    ok(span > 20.0, f"2: η spans {span:.1f} decades over 500–2500 K, expected > 20")

    # ── 3. label discipline ─────────────────────────────────────────────────
    labels = {rh.RELAXES, rh.CANNOT_RELAX, rh.INSIDE_SPREAD, rh.NO_TEMPERATURE,
              rh.NO_SILICATE, rh.NO_SOLIDUS, rh.OTHER_LAYER}
    cases = [
        rh.relaxation_verdict(1600.0, 2526.0, 0.0, 135.3e9, 4.54),
        rh.relaxation_verdict(None, None, 0.0, None, 5.3, "undecided"),
        rh.relaxation_verdict(1600.0, None, 0.0, None, 5.3, "none"),
        rh.relaxation_verdict(1600.0, None, 0.0, None, None),
        rh.relaxation_verdict(1600.0, None, 600e9, None, 4.5),
        rh.relaxation_verdict(76.0, None, 0.0, None, 4.5, "solid", silicate_is_outermost=False),
    ]
    for c in cases:
        ok(c["figure_relaxation"] in labels, f"3: unregistered label {c['figure_relaxation']!r}")
        ok(len(c["notes"]) >= 1, "3: a verdict without its note")
    ok(cases[1]["figure_relaxation"] == rh.NO_TEMPERATURE, "3: undeclared temperature must refuse by name")
    ok(cases[2]["figure_relaxation"] == rh.NO_SILICATE, "3: no silicate must refuse by name")
    ok(cases[3]["figure_relaxation"] == rh.NO_TEMPERATURE, "3: no age must refuse by name")
    ok(cases[4]["figure_relaxation"] == rh.NO_SOLIDUS, "3: solidus undefined at 600 GPa must refuse by name")
    ok(cases[5]["figure_relaxation"] == rh.OTHER_LAYER,
       "3: a 1-bar temperature over a non-silicate outer layer must refuse by name (audit ①)")
    ok("relayed" in cases[0]["notes"][0] and "Maxwell floor" in cases[0]["notes"][0],
       "3: the headline note must carry the relayed-constant and Maxwell-floor conditions")

    # ── 4. roster measurement and reachable branches ────────────────────────
    earth = cases[0]
    ok(earth["figure_relaxation"] == rh.RELAXES and earth["second_law"] == rh.RELAXES,
       f"4: Earth verdict {earth['figure_relaxation']} / second law {earth['second_law']}")
    ok(earth["maxwell_time_mantle_top"] < 1.0,
       f"4: Earth τ_M at 1600 K = {earth['maxwell_time_mantle_top']:.2e} yr, expected < 1 yr")
    mid = rh.relaxation_verdict(850.0, None, 0.0, None, 4.5)
    ok(mid["figure_relaxation"] == rh.INSIDE_SPREAD, f"4: 850 K should sit inside the spread, got {mid['figure_relaxation']}")
    cold = rh.relaxation_verdict(600.0, None, 0.0, None, 4.5)
    ok(cold["figure_relaxation"] == rh.CANNOT_RELAX, f"4: 600 K should refuse, got {cold['figure_relaxation']}")

    for f in fails:
        print(f"  [FAIL] {f}")
    if not fails:
        print(f"  [PASS] 완화 판정 축 — 전사 {4}건 · 문턱 가족 {len(want)}칸 (T_s 1600) + 엔진 솔리더스 "
              f"{lo:.0f}–{hi:.0f} K · 라벨 {len(cases)}건 · 로스터 지구 {earth['figure_relaxation']}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
