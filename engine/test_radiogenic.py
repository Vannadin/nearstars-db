# 방사성 예산의 앵커 — 초안 표 폐합 세 건, 캡션 오독, 과거 방향 붕괴 배율, ²³⁵U 의 몫, 로스터 판정 (Brief 44)
"""Anchor the radiogenic budget on the closure that checks our reading of the constants.

    python3 engine/test_radiogenic.py

0. R1 — the nuclide sums reproduce Ruedas 2017's element rates: pinned to 1e-12 at the sums themselves
   (U 9.831432361e-5, Th 2.6368e-5, K 3.430136938e-9 W/kg), and within 3e-5 of the printed element
   values (the difference is printed). R3 — each paper's composition gives that paper's number, on the
   engine Earth's silicate mass (4.0311e24 kg), within ±0.5 TW (prereg-radiogenic addenda 1, 2, 5).
1. Closure — with the standard BSE mass 4.0e24 kg: Earth (1) and appendix are now the same set (N&P 2020
   published, 260/23/85) and give 21.58 TW. Earth (2) is now O'Neill & Palme 2008 as the published papers print it
   (10/40/140, addendum 10): 10.07 TW here, 10.1506 on the engine Earth's silicate mass — no longer the draft
   table's set, so it is pinned and not closed against the draft's 10.8.
2. The caption trap — read as "initial composition" and decayed 4.5 Gyr the set gives 11.79 TW,
   1.9× short. Pinned so nobody re-adopts the caption's reading. (11.59 until the Earth set's U moved
   22 → 23, prereg-radiogenic addenda 2 and 6.)
3. Direction — H(−4 Gyr)/H(now) = 3.66 against the paper's 3.5; computed forward it is 1.74,
   believable and wrong. ²³⁵U carries it: 0.37 TW today, without it the factor is 2.83, Th + ²³⁸U
   alone 1.53. (Ruedas 2017 constants; with the draft table these read 3.67 · 0.38 · 2.8 · 1.5.)
4. Roster — Earth's own silicate mass gives ~21 TW and a radiogenic-only t_int ≈ 29 K (the
   methodology's 35 K is the total 0.087 W/m², radiogenic + secular); giants refuse; a body
   without core_mass_fraction refuses; labels carry the declarations.
"""
from __future__ import annotations

import sys

import radiogenic as rg


def main() -> int:
    fails: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    M = rg.BSE_MASS_STANDARD_KG
    # ── 0. R1 and R3 ───────────────────────────────────────────────────────
    sums = {el: sum(rg.ISOTOPES[n][1] * rg.ISOTOPES[n][2] for n in rg.ISOTOPES if rg.ELEMENT_OF[n] == el)
            for el in ("U", "Th", "K")}
    for el, pinned in (("U", 9.831432361070902e-05), ("Th", 2.6368e-05), ("K", 3.430136937926238e-09)):
        ok(abs(sums[el] / pinned - 1) < 1e-12, f"R1: {el} nuclide sum {sums[el]!r}, pinned {pinned}")
        printed = rg.RUEDAS_2017_ELEMENT_W_PER_KG[el]
        rel = sums[el] / printed - 1
        ok(abs(rel) < 3e-5, f"R1: {el} sum {sums[el]:.9e} vs Ruedas element {printed} — {rel:+.2e}")
        print(f"  [기록] R1 {el}: 핵종 합 {sums[el]:.9e} · Ruedas 원소값 {printed} · 차 {rel:+.2e}")
    silicate = 1.0 * rg.M_EARTH_KG * (1.0 - 0.325)       # the engine Earth's silicate mass (addendum 1 C)
    for label, conc, printed_tw in (("McDonough & Sun 1995", {"U": 20e-9, "Th": 80e-9, "K": 240e-6}, 20.0),
                                    ("Lyubetskaya & Korenaga 2007a", {"U": 17e-9, "Th": 63e-9, "K": 190e-6}, 16.0),
                                    ("Nimmo & Primack 2020", {"U": 23e-9, "Th": 85e-9, "K": 260e-6}, 22.0)):
        tw = rg.heat_per_kg(conc) * silicate / 1e12
        ok(abs(tw - printed_tw) <= 0.5, f"R3: {label} {tw:.4f} TW vs printed {printed_tw}")
        print(f"  [기록] R3 {label}: {tw:.4f} TW (인쇄 {printed_tw:g}, 차 {tw - printed_tw:+.4f}) · 질량 {silicate:.6e} kg")
    # ── 0b. R5 — declared concentrations, their grades, and the pair set (prereg-radiogenic §4, addendum 9) ──
    base = {"U_ppb": 14.0, "Th_ppb": 54.0, "K_ppm": 284.0, "source": "fixture"}
    def run(decl):
        return rg.solve(0.1074, 0.25, 0.532, "rocky", 4.54, radiogenic_concentration=decl)
    none = run(None)
    ok(none.applicable and none.values["radiogenic_concentration_grade"] == "declared-default"
       and none.values["radiogenic_power_low"] is not None, "R5/R6: no declaration → declared-default, _low kept")
    for g in ("measured", "literature"):
        r = run(dict(base, grade=g))
        ok(r.applicable and r.values["radiogenic_concentration_grade"] == g and r.values["radiogenic_power_low"] is None
           and r.values["mantle_temperature_width_set"] == 0.0, f"R5: {g} without a pair → _low empty, one-set band")
    ov = run(dict(base, grade="owner-override", reason="dynamo needs a liquid core", window="outside"))
    ok(ov.applicable and "문헌 창 밖" in " ".join(ov.notes), "R5: owner-override outside the window is printed")
    no_reason = run(dict(base, grade="owner-override", window="inside"))
    ok(not no_reason.applicable and "reason" in no_reason.reason, "R5: owner-override without a reason refuses by name")
    ok(not run(dict(base, grade="declared-default")).applicable, "R5: a body file may not declare declared-default")
    pair = {"U_ppb": 11.0, "Th_ppb": 43.0, "K_ppm": 130.0, "source": "fixture pair"}
    lit_pair = run(dict(base, grade="literature", alternative=dict(pair, grade="literature")))
    ok(lit_pair.applicable and lit_pair.values["radiogenic_power_low"] is not None
       and lit_pair.values["mantle_temperature_width_set"] > 0, "addendum 9: a literature pair keeps _low and the union")
    dd_pair = run(dict(base, grade="literature", alternative=dict(pair, grade="declared-default")))
    ok(dd_pair.applicable and dd_pair.values["radiogenic_power_low"] is None
       and "싣지 않는다" in " ".join(dd_pair.notes), "addendum 9: a declared-default pair is recorded and not used")
    # ── 1. closure ─────────────────────────────────────────────────────────
    # earth_2 10.63 → 10.64 (Ruedas constants, addendum 7) → 10.07 (the set itself replaced, addendum 10).
    tw2 = rg.budget(M, "earth_2_non_chondritic")["total_w"] / 1e12
    ok(abs(tw2 - 10.07) < 0.02, f"1: earth_2_non_chondritic = {tw2:.2f} TW, expected 10.07")
    tw2e = rg.budget(rg.M_EARTH_KG * 0.675, "earth_2_non_chondritic")["total_w"] / 1e12
    ok(abs(tw2e - 10.1506) < 1e-4, f"1: earth_2 on the engine Earth's silicate mass {tw2e:.4f} TW, expected 10.1506")
    want = {"earth_1_chondritic": (21.58, 22.0),
            "appendix": (21.58, 22.0)}
    for s, (mine, printed) in want.items():
        tw = rg.budget(M, s)["total_w"] / 1e12
        ok(abs(tw - mine) < 0.02, f"1: {s} = {tw:.2f} TW, expected {mine}")
        ok(abs(tw / printed - 1.0) < 0.03, f"1: {s} = {tw:.2f} TW vs the paper's {printed} — off by {(tw / printed - 1) * 100:.1f} %")
    # ── 2. caption trap ────────────────────────────────────────────────────
    initial_read = rg.budget(M, "earth_1_chondritic", t_gyr=4.5)["total_w"] / 1e12
    ok(abs(initial_read - 11.79) < 0.05, f"2: caption-as-initial read gives {initial_read:.2f} TW, expected 11.79")
    ok(22.0 / initial_read > 1.8, "2: the caption reading must fall ~1.9× short of the appendix's 22 TW")
    # ── 3. direction and ²³⁵U ──────────────────────────────────────────────
    past = rg.history_factor(-4.0)
    ok(abs(past - 3.67) < 0.02, f"3: H(-4 Gyr)/H(now) = {past:.3f}, expected 3.67 (paper 3.5)")
    ok(abs(past - 3.5) / 3.5 < 0.06, f"3: {past:.2f} is more than 6 % from the paper's printed 3.5")
    # The wrong-direction reading: H(now)/H(+4 Gyr) = 1.74. (A relayed "1.67" for this mistake had no
    # stated condition and does not reproduce at ±4 Gyr from now; the pin is the *shape* — a forward
    # factor under 2 against a past factor of 3.67 — not the relayed digit.)
    fwd = 1.0 / rg.history_factor(+4.0)
    ok(1.6 < fwd < 1.8, f"3: the forward (wrong-direction) reading should be ~1.7, got {fwd:.3f}")
    ok(past - fwd > 1.5, "3: past and forward factors must differ by the sign the parallel seat once dropped")
    no_u235 = rg.history_factor(-4.0, species=("K40", "Th232", "U238"))
    th_u238 = rg.history_factor(-4.0, species=("Th232", "U238"))
    ok(abs(no_u235 - 2.82) < 0.03, f"3: without U235 expected 2.82, got {no_u235:.3f}")
    ok(abs(th_u238 - 1.53) < 0.03, f"3: Th + U238 alone expected 1.53, got {th_u238:.3f}")
    u235_tw = rg.heat_per_kg(rg.CONCENTRATION_SETS["appendix"], 0.0, ("U235",)) * M / 1e12
    ok(abs(u235_tw - 0.38) < 0.02, f"3: U235 today {u235_tw:.3f} TW, expected 0.38")
    # ── 4. roster ──────────────────────────────────────────────────────────
    earth = rg.solve(1.0, 0.325, 1.0, "rocky", 4.54)
    ok(earth.applicable and 20.5 < earth.values["radiogenic_power"] / 1e12 < 22.0,
       f"4: Earth radiogenic power {earth.values.get('radiogenic_power', 0) / 1e12:.2f} TW, expected ~21")
    # t_int here is RADIOGENIC-ONLY: F = 21 TW / 4πR² = 0.042 W/m² → 29 K. The methodology's "≈ 35 K"
    # uses the TOTAL surface heat flow 0.087 W/m² (radiogenic + secular); this recipe does not carry
    # secular cooling, so its t_int is a floor on that number, and the label says so.
    ok(earth.applicable and 28.0 < earth.values["t_int"] < 31.0, f"4: Earth radiogenic-only t_int {earth.values.get('t_int')} K, expected ~29")
    ok(earth.applicable and abs(earth.values["mantle_radiogenic_power"] / earth.values["radiogenic_power"] - 0.70) < 1e-9,
       "4: mantle share must be the declared 0.70")
    ok(earth.applicable and earth.grade == "analog", "4: grade must be analog — the concentrations and the split are declarations")
    ok(earth.applicable and "선언" in " ".join(earth.notes) and "Ruedas 2017" in " ".join(earth.notes),
       "4: the label must say the set/split are declared and name the constants' source (Ruedas 2017)")
    giant = rg.solve(120.0, None, 11.2, "giant", 5.3)
    ok(not giant.applicable and "냉각광도" in giant.reason, "4: a giant must refuse by name (cooling luminosity)")
    # 얼음체 (감사, 44 후속 ①): 얼음 맨틀은 규산염이 아니다 — 같은 질량의 암석체 대비 예산이 규산염 분율만큼 준다
    icy = rg.solve(0.025, 0.10, 0.38, "icy", 4.5, ice_mass_fraction=0.40)
    rocky_same_mass = rg.solve(0.025, 0.10, 0.38, "rocky", 4.5, ice_mass_fraction=0.0)
    ok(icy.applicable and abs(icy.values["radiogenic_power"] / rocky_same_mass.values["radiogenic_power"] - 0.50 / 0.90) < 1e-9,
       "4: a 40 % ice body must carry (1 − 0.10 − 0.40)/(1 − 0.10) of the same-mass rocky budget")
    absurd = rg.solve(0.025, 0.60, 0.38, "icy", 4.5, ice_mass_fraction=0.50)
    ok(not absurd.applicable and "규산염 질량분율" in absurd.reason, "4: core 0.6 + ice 0.5 must refuse by name, not go negative")
    no_cmf = rg.solve(0.6, None, 0.9, "rocky", 5.0)
    ok(not no_cmf.applicable and "core_mass_fraction" in no_cmf.reason, "4: undeclared core_mass_fraction must refuse by name")

    for f in fails:
        print(f"  [FAIL] {f}")
    if not fails:
        print(f"  [PASS] 방사성 예산 — 폐합 2세트(≤ 2.1 %) · earth_2 10.07 TW 핀 · 캡션 오독 {initial_read:.2f} TW · 과거 배율 {past:.2f} "
              f"(순방향 {fwd:.2f}, ²³⁵U 없이 {no_u235:.2f}) · 지구 {earth.values['radiogenic_power'] / 1e12:.2f} TW, "
              f"t_int(방사성만) {earth.values['t_int']:.1f} K · 얼음체 규산염만 · 거대행성·핵질량분율 미선언 거절")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
