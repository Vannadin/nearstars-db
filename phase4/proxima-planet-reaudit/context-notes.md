# Proxima planet/moon walk re-audit — context notes

## Why (2026-07-14)

Owner recalled Phase 4 as "stars only walked, planets/moons unfinished." Board
inspection contradicts that for Proxima: **all 53 rows are gated/passthrough,
0 open** — every planet/moon axis (b/c/c I/d × identity·orbit·bulk·atmosphere·
surface·appearance·magnetism·environment·rings·satellites·gameplay) already
carries a decision. Owner then chose **re-audit walk quality** (not just closing
figure sub-axes): check the already-gated planet rows for pre-skill carryover and
re-walk anything below the current v2/skill standard.

## What the validator already guarantees (don't re-audit these)

`check_phase4_gate.py` = 0 errors on the board. So the hard schema invariants
hold: gate keys ∈ {criterion,verdict,evidence,divergence_note}, no verdict:partial,
documented-divergence ⟹ divergence_note, status enum, typed-field presence for
declared fields. The re-audit targets what the validator **cannot** see.

## Re-audit rubric (soft-quality dimensions)

1. **Emit content outside typed fields** — numbers/colors/curves living in prose
   or in non-standard row keys (the `MIGRATION-FLAG` keys: `derived_temps`,
   `bond_albedo_cascade`, `cfg_colors_intrinsic`, `cfg_colors_displayed`). A
   writer can't read these. Flag as tech-debt (may be deliberate emit-末 deferral).
2. **Pre-skill carryover** — rows bundled/authored before the 2026-07-10 skill
   era that never got the axis-by-axis walk: thin narrative, no owner decision
   date, generic gate evidence, missing methodology/bibcode provenance.
3. **Coverage gaps (validator warnings)** — figure/internal_heat sub-axes not yet
   walked: b internal_heat; c obliquity·spin_axis·J2·flattening·internal_heat;
   c I J2·C22·flattening·internal_heat; d J2·C22·flattening·internal_heat.
4. **Silent passthrough** — measurement-less axis taking an engine default
   without an explicit passthrough/gated confirm row.
5. **Provenance** — gated derived rows should cite methodology doc or bibcode;
   `refs[]` machine-readable. "no refs[]" on pure canon/art rows is acceptable.

## Calibration read (main thread, 2026-07-14)

- **Proxima b (lines 209–606): HIGH quality, v2-native.** Not carryover. Typed
  fields, correct gate blocks, refs, dated owner decisions (2026-06-23), even a
  self-correction note (gameplay row: "직전 커밋 2bb8540은 오너 검토 없이 작성
  → 본 검토로 정정"). Only debt = MIGRATION-FLAG prose keys (hex colors, layered
  temps) outside typed fields — explicitly deferred to emit-末 art-pass; and the
  bulk internal_heat coverage gap.

## Method

Delegate full read of c / c I / d to one Opus agent (Phase 3 frozen → safe;
read-only, narrow scope) applying the rubric → ranked findings. Main thread
verifies top findings against the file before acting. Hygiene/schema fixes =
autonomous; decision re-opens (art-direction changes) = owner. (audit-cost +
agent-token-saving discipline.)

## Spin-axis sub-thread (owner, 2026-07-14) — Cassini obliquity

Owner probed the tidally-locked spin axis (b/d/c I "obliquity 0, spin = orbit
normal"). Verdict given: NOT a lazy default — it is the Cassini State 1
equilibrium (tidal damping pins obliquity near 0 for these close-in bodies),
categorically different from free-rotator c (where 17° is a real art choice).
The absolute pole direction = orbit normal, which tracks the de-perfected
(near-coplanar) orbit plane — not nailed to a fixed frame.

Owner then chose: **compute the ACTUAL Cassini-state obliquity** (not hard 0, not
random de-perfect) → then asked to **research the methodology first**. So:
- New methodology doc planned: `docs/reference/cassini-state-obliquity-methodology.md`
  (+ ko mirror), companion to body-figure-methodology.md.
- Research delegated to an Opus ADS agent (independent citation-sorted discovery,
  no seeded paper list, ADS token not WebSearch) → formula (Cassini State 1 ε vs
  orbital precession rate g and spin precession constant α), α for free vs
  synchronous (needs J₂ AND C₂₂ triaxiality), how to get g (Laplace–Lagrange for
  planets; planet-J₂/ring for the moon), calibration anchors (measured moon/planet
  Cassini obliquities), regime magnitudes.
- Then main thread verifies + writes the doc, computes ε for b/d/c I from board
  inputs already in hand:
  - b: a 0.04848 AU, P 11.18465 d, 1.22 M⊕, J₂ 2.8e-5, C₂₂ 8e-6, NMoI ~0.33
  - d: a 0.02885 AU, P 5.122 d, 0.30 M⊕, J₂ 1.7e-4, C₂₂ 5.0e-5, NMoI ~0.33
  - c I: moon of c(8 M⊕), a 69,000 km, P 17.7 h, R 950 km, J₂ 1.6e-2, C₂₂ 4.9e-3
  - (c is the free rotator — obliquity already set 17°, not a Cassini case)
- Expectation stated to owner: likely sub-degree for these, but compute to confirm
  (watch for Cassini-state resonance → could be larger).

### Methodology researched + computed (2026-07-14)

- New doc `docs/reference/cassini-state-obliquity-methodology.md` (+ ko mirror),
  indexed + cross-linked from body-figure. ADS research agent (Opus, independent
  citation-sorted discovery); 10 load-bearing bibcodes verified live against ADS
  (Peale 1969, Ward 1975, Ward & Hamilton 2004, Bills 2005, Baland 2011, Margot
  2007, Millholland 2024, Guerrero 2024, Colombo 1966, Fabrycky 2007). Committed
  fe3e40f.
- Computed (scratchpad script — Laplace–Lagrange g for {b,c,d}, planet-J₂ g for
  c I, synchronous α = 1.5·n·(J₂+C̄₂₂)/C̃, Cassini Eq.1):
  - b: α 1.92°/yr, |g| 0.033°/yr, **|g|/α 0.017** → ε₁ ≈ 0.02–0.05° (I 1–3°)
  - d: α 25.7°/yr, |g| 0.47°/yr, **|g|/α 0.018** → ε₁ ≈ 0.02–0.05°
  - c I: α 15970°/yr, |g| 13.3°/yr (c's J₂), **|g|/α 8.3e-4** → ε₁ ≲ 0.004°
  - ALL far below the state-2 critical ratio (~1.1) → firmly Cassini State 1, no
    dramatic obliquity (grounded, not assumed). ε₁ = (|g|/α)·sin I, couples to the
    de-perfected near-coplanar orbital inclination. Matches anchors (Mercury
    0.035°, Galileans 10⁻³–10⁻²°).
- Board application = **owner chose option A**: obliquity value kept ≈0 (ε is
  sub-visible and couples to de-perfected I → no false-precision number), but the
  obliquity note + spin_axis_orientation value on b/d/c I re-grounded from
  "조석고정의 자연 귀결" (assumed) to the computed Cassini State 1 result (|g|/α,
  ε estimate, far-from-resonance, method pointer). 0 errors, HTML rebuilt.
