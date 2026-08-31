# The ice axis — checklist

Brief 23, 2026-08-31 (owner-approved order ③). Measure the ice half of the fuzzy core the
way the rock axis was measured (C13): end A = anchor, end B = the ice spread outward,
renormalized as I/(M·R_pub²) against the N13 P_Voy mean-radius targets — **the same
renormalization, or the 26 %/41 % table cannot sit beside it.**

## Pre-registered BEFORE implementation

**Outcome branches, five.**

1. The ice axis **closes** the deficit → immediate suspicion: an exactly-closing answer is
   the shape this list refused twice (C5, C10). If it closes, trace what forced it.
2. Partial coverage like the rock axis → also measure whether the **two axes' sum** covers
   the deficit, and whether the sum is a simple sum (run both declarations together —
   interactions are possible).
3. The axis stays **unrepresentable** → name the blocker. Post-Brief-22, "the corridor
   killed it" is no longer an acceptable name.
4. **The mixing rule has no grounding** → the axis closes the way C4's methane did
   (recorded, not measured). A legitimate ending.
5. Outside the register → name the kind, extend the register.

**Acceptance format**: four I/(M·R_pub²) values (end A/end B × two planets) and two
gap-covered percentages, in a table that sits beside the rock axis's.

**Hard constraints**: anchors bit-identical; gate FAIL 0 with measured time delta; no new
runtime dependency; English commits, one logical unit; declare–integrate–report; plus the
three rules registered today — a correction request is opened before it is sent; **a new
number reopens the old numbers it bears on**; `git diff --stat` before staging.

## Work items

- [x] Physics question first: grounding **found twice** — Soubiran & Militzer 2015
      (2–70 GPa × 1000–6000 K DFT-MD: ideal mixing good to a few %, ≤10 % locally) and the
      target's own LM-REOS (Nettelmann+ 2008). Both fetched to cache, checked by title.
      Branch 4 does not fire. No delegation needed (two ADS queries, main thread)
- [x] Representation decided and written (notes §2): `envelope_z_rock_fraction` (default
      1.0 = legacy, bit-identical), `_EnvelopeWater` dispatching part, the ice_giant class
      gate widened for dissolved ice, **water1's c_P baked** (the source always carried it)
- [x] End B (ice) and end B (both) run, both planets — all four reach mass closure and
      **none converges**: the cold boundary path dies in the steam wedge (notes §3)
- [x] λ / renorm table recorded (notes §3); **no gap-covered numbers** — non-converged
      ends are not measured ends (branch 3 refined, blocker named: p ≲ 0.1 GPa ×
      500–1000 K liquid, filler = IAPWS-95 steam, an owner decision)
- [x] Anchors bit-identical (--fast before and after eos change); --refresh in the
      landing commit (fingerprint moved: _stack/integrate/_shoot_pressure/shoot/solve)
- [x] Full gate; c_P crosscheck added to the water-table check (time delta ~0)
- [x] interior-core.md C13 row + notes; report with reproduction pointers
      (`scratchpad/ice_axis_runs.py`; the refusal spy is three lines in notes §3)
