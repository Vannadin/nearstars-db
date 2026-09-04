# 암석 다이나모 사다리의 앵커 — 문서 검증 표 재현, RM22 Table 8 과의 차이 고정, 게이트 라벨, 격자 미선출, 로스터 (Brief 47)
"""Anchor the rocky dynamo ladder.

    python3 engine/test_dynamo_rocky.py

1. Transcription — the closing relation reproduces the methodology's own Solar-System table on its
   observed column (Mercury 4e-4 / 0.38 → 0.22 µT; Ganymede 2e-3 / 0.41 → 0.87; Earth 30; Mars and
   Venus 0 as class judgements). And the doc-versus-paper difference is pinned: RM22 Table 8 COMPUTES
   Mercury 0.0003 (→ 0.16 µT) and Venus 0.0007 (→ 0.024 µT) — not the doc's zeros.
2. Gates are labels — undecided conductor → cannot-say; solid → dead; stagnant lid declared true → dead;
   undeclared lid → cannot-say; regime-5 body past the declared death age → dead. Every note carries
   "QUOTED, not evaluated" for Rm > 40.
3. Declarations are families — regimes 2 and 3 emit endpoints and no elected moment; the undeclared
   regime gate emits both branches with OC06's own 0.05–0.10 width (2×, base-heated only; RM22's 0.06 inside
   it; the 0.15 that stood here until 2026-09-04 was Grießmeier's different quantity, and {0.05, 0.06} for one
   hour was not two independent sources).
4. Roster — Earth: regime 1, alive, dipolar 1.0 ℳ⊕ → 30 µT (the anchor reproduced), multipolar
   1.5–3.0 µT; an undecided core → cannot-say.
"""
from __future__ import annotations

import sys

import dynamo_rocky as dr


def main() -> int:
    fails: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # ── 1. transcription: the doc's observed column through B = 30 M R^-3 ─────
    table = {"Mercury": (4e-4, 0.38, 0.22), "Ganymede": (2e-3, 0.41, 0.87), "Earth": (1.0, 1.0, 30.0)}
    for body, (m, r, want) in table.items():
        got = dr.b_eq_ut(m, r)
        ok(abs(got - want) / want < 0.03, f"1: {body} B_eq {got:.3f} µT, doc {want}")
    # the doc-versus-paper difference, pinned so nobody reads the doc's zeros as RM22's output
    ok(abs(dr.b_eq_ut(0.0003, 0.38) - 0.164) < 0.005, "1: RM22's computed Mercury 0.0003 should give 0.16 µT, not the observed 0.22")
    ok(abs(dr.b_eq_ut(0.0007, 0.95) - 0.0245) < 0.002, "1: RM22's computed Venus 0.0007 should give 0.024 µT, not the doc's 0")
    # ── 2. gates as labels ───────────────────────────────────────────────────
    und = dr.ladder(1.0, 1.0, "undecided", False, 4.5)
    ok(und.applicable and und.values["dynamo_alive"] == dr.UNDECIDED_CORE and und.values["dipole_moment"] is None,
       "2: undecided conductor must be cannot-say with no moment")
    sol = dr.ladder(1.0, 1.0, "solid", False, 4.5)
    ok(sol.values["dynamo_alive"] == dr.DEAD_SOLID and sol.values["b_eq"] == 0.0, "2: solid core → dead, B = 0")
    lid = dr.ladder(1.0, 1.0, "liquid_outer_solid_inner", True, 4.5)
    ok(lid.values["dynamo_alive"] == dr.DEAD_LID, "2: declared stagnant lid → dead")
    nolid = dr.ladder(1.0, 1.0, "liquid_outer_solid_inner", None, 4.5)
    ok(nolid.values["dynamo_alive"] == dr.UNDECIDED_LID, "2: undeclared lid → cannot-say, not a default")
    mars_like = dr.ladder(0.107, 0.532, "liquid", False, 8.0)      # ρ ≈ 0.71 ρ⊕ → regime 5, past 7 Gyr
    ok(mars_like.values["ladder_regime"] == 5 and mars_like.values["dynamo_alive"] == dr.DEAD_AGE,
       f"2: Mars-like at 8 Gyr → regime 5 dead by declared age, got {mars_like.values['ladder_regime']} / {mars_like.values['dynamo_alive']}")
    for r in (und, sol, lid, nolid, mars_like):
        ok(any("QUOTED, not evaluated" in n for n in r.notes), "2: every result must say Rm > 40 is quoted, not evaluated")
    # ── 3. declared families ─────────────────────────────────────────────────
    se2 = dr.ladder(2.2, 1.25, "liquid", False, 3.0)
    ok(se2.values["ladder_regime"] == 2 and se2.values["dipole_moment"] is None
       and (se2.values["dipole_moment_min"], se2.values["dipole_moment_max"]) == (1.0, 2.0),
       "3: regime 2 must emit the 1.0–2.0 grid and no elected moment")
    se3 = dr.ladder(4.0, 1.5, "liquid", False, 3.0)
    ok(se3.values["ladder_regime"] == 3 and se3.values["dipole_moment"] is None and se3.values["b_eq"] is None,
       "3: regime 3 must emit no elected moment or field")
    both = dr.ladder(1.0, 1.0, "liquid_outer_solid_inner", False, 4.54)
    ok(both.values["regime"] == "undeclared (both emitted)"
       and abs(both.values["b_eq_multipolar_max"] / both.values["b_eq_multipolar_min"] - 2.0) < 1e-9,
       "3: undeclared regime emits both branches with OC06's own 0.05–0.10 width (2×; base-heated only)")
    ok(dr.MULTIPOLAR_FACTORS[0] <= dr.MULTIPOLAR_SOLAR_SYSTEM <= dr.MULTIPOLAR_FACTORS[1],
       "3: RM22's Solar-System point 0.06 must sit inside OC06's width")
    # C16 (2026-09-04): the regime gate's branch key is tidal_locking's `locked` — free → dipolar by RM22's rule (no
    # Ro_ℓ), locked → Ro_ℓ refused by three names (both emitted), absent → cannot-say (no tidal_locking), both emitted.
    free = dr.ladder(1.0, 1.0, "liquid_outer_solid_inner", False, 4.54, locked=False, rotation_period_h=24.0)
    ok(free.values["regime"] == "dipolar" and free.values["rossby_verdict"].startswith("dipolar by rule")
       and abs(free.values["b_eq"] - 30.0) < 1e-9, "3/C16: a free rotator is dipolar by rule, Ro_ℓ not evaluated")
    lockd = dr.ladder(1.0, 1.0, "liquid_outer_solid_inner", False, 4.54, locked=True, rotation_period_h=32.0)
    ok(lockd.values["regime"] == "undeclared (both emitted)" and lockd.values["rossby_verdict"] == dr.ROSSBY_REFUSAL
       and "ν" in dr.ROSSBY_REFUSAL and "q_conv" in dr.ROSSBY_REFUSAL and "Table 8" in dr.ROSSBY_REFUSAL,
       "3/C16: a locked body's Ro_ℓ is refused by the three names and both branches are emitted")
    ok(both.values["rossby_verdict"] == dr.NO_LOCK, "3/C16: without tidal_locking the gate says cannot-say (no tidal_locking)")
    print(f"  [PASS] C16 분기: 자유 자전 → {free.values['regime']} (Ro_ℓ 안 거침) · 잠김 → {lockd.values['regime']} + 세 이유 거절 · 열쇠 없음 → {both.values['rossby_verdict'][:40]}…")
    dec = dr.ladder(1.0, 1.0, "liquid_outer_solid_inner", False, 4.54, dynamo_regime="multipolar")
    ok(dec.values["regime"] == "multipolar" and dec.values["dipole_moment_min"] == 0.05 and dec.values["dipole_moment_max"] == 0.10,
       "3: a declared multipolar regime must carry the factor grid")
    # ── 4. roster ────────────────────────────────────────────────────────────
    ok(both.values["ladder_regime"] == 1 and both.values["dynamo_alive"] == dr.ALIVE
       and abs(both.values["b_eq"] - 30.0) < 1e-9 and abs(both.values["b_pol"] - 60.0) < 1e-9,
       f"4: Earth → regime 1 alive, 30 / 60 µT; got {both.values}")
    ok(abs(both.values["b_eq_multipolar_min"] - 1.5) < 1e-9 and abs(both.values["b_eq_multipolar_max"] - 3.0) < 1e-9,
       "4: Earth's multipolar branch is 1.5–3.0 µT (0.05–0.10 × 30; 1.8–4.5 until 2026-09-04 with the 0.15 point, 1.5–1.8 for one hour with {0.05, 0.06})")
    ok(both.grade == "judgment", "4: the ladder never grades above judgment — its gates are labels")
    giant = dr.ladder(120.0, 11.2, "liquid", False, 5.3, body_class="giant")
    ok(not giant.applicable, "4: a giant is out of domain here (dynamo_giant's recipe)")
    # ── 5. C28: the ice fraction comes from the composition preset unless declared ──────────
    from state import BodyState
    def st(**inputs):
        return BodyState(name="t", kind="planet", inputs=inputs)
    ok(dr.ice_fraction_from_state(st(composition_intent="earth_like")) == (0.0, "composition preset: earth_like (interior.COMPOSITIONS, grade class)"),
       "5/C28: earth_like preset → 0.0, labelled as the preset")
    ok(dr.ice_fraction_from_state(st(composition_intent="water"))[0] == 0.50, "5/C28: water preset → 0.50 (interior.COMPOSITIONS slot 1)")
    ok(dr.ice_fraction_from_state(st(composition_intent="water", ice_mass_fraction=0.1)) == (0.1, "declared ice_mass_fraction"),
       "5/C28: an explicit declaration overrides the preset")
    none_v, none_why = dr.ice_fraction_from_state(st(composition_intent="carbon_rich"))
    ok(none_v is None and "no composition preset" in none_why, "5/C28: an unknown preset refuses by name, it does not default to 0")
    wet = dr._from_state(st(mass_earth=1.0, radius_earth=1.0, conductor_phase="liquid_outer_solid_inner", stagnant_lid=False,
                            age_gyr=4.5, body_class="rocky", composition_intent="water"))
    ok(wet.applicable and wet.values["ladder_regime"] == 4 and "composition preset: water" in " ".join(wet.notes),
       "5/C28: through _from_state a water body reaches regime 4 with the source printed")
    refused = dr._from_state(st(mass_earth=1.0, radius_earth=1.0, body_class="rocky", composition_intent="carbon_rich"))
    ok(not refused.applicable and "no composition preset" in refused.reason, "5/C28: _from_state refuses an unknown preset by name")
    if not fails:
        print(f"  [PASS] C28 얼음 분율: earth_like 0.00 · water 0.50 (regime {wet.values['ladder_regime']}) · 선언 0.1 우선 · 미지 프리셋 거절")

    for f in fails:
        print(f"  [FAIL] {f}")
    if not fails:
        print("  [PASS] 암석 다이나모 사다리 — 문서 표 재현(수성 0.22 · 가니메데 0.87 · 지구 30 µT) + RM22 Table 8 차이 고정 "
              "(수성 0.16 · 금성 0.024 µT) · 게이트 라벨 5건 · 격자 미선출(regime 2·3) · 지구 30 µT / 다극자 1.5–3.0 µT · Rm 인용 표기")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
