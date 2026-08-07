# Proxima d prose modernization — context notes

## Scope decision (2026-08-07)

Full d audit (11 rows) found the data layer healthy: axis coverage at parity
with b, all 2026-07-14 hygiene items actually done (albedo numeric, figure
fills, internal_heat, Cassini obliquity), Proxima-lit color math verified
exact, refs provenance shape correct, validator clean. The debt is the prose
layer: 10 of 11 rows predate the 2026-07-24..08-04 prose contract hardening
(only appearance, rewritten in the 08-03 audit, is new-style — and even it
lacks the EN narrative).

Owner chose: fix axis by axis, one commit each. Values frozen; where a value
must move it gets a provenance line.

## Standing findings the rewrite must resolve

- Banned vocab in narratives: emit / de-perfect / passthrough (orbit),
  G-tokens G1/G5/G7/G8/G11 (identity, surface, environment, gameplay),
  raw field names ("body_type=", "breathability=∅", "radiation=" ...).
- Dated decision history in narratives: bulk "[§3.2 정규화 2026-07-12]",
  "[2026-07-14 figure]"; surface "직전 #34302c보다 밝게".
- Inline citations in narratives: Zapatero Osorio 2026 (identity, surface,
  environment), Garcia-Sage2017/Garraffo2016 (atmosphere), Faria2022 (orbit).
- evidence blocks use the old "rationale: / paper:" pseudo-key shape; target
  is the fixed 3-part shape. Memory wiki-links ([[...]]) render literally in
  the viewer — replace with plain words (orbit, rings evidence).
- Verdict taxonomy: bulk / atmosphere / surface / environment are recipe
  outputs gated as pass-in-window with criterion [derived-grounding]; current
  SPEC §2 has methodology-derived for exactly this (b bulk already migrated).
  magnetism stays pass-in-window (observation, not our recipe).
- gameplay narrative still carries the difficulty value retired 2026-08-03
  ("난도=항성간 플래그십 + 최근접 고방사선 착륙") — also violates the
  2026-08-04 no-travel-difficulty rule. RB discoverability tuples (T F F F)
  belong to the layer retired 2026-07-28 — drop from identity evidence and
  gameplay narrative.

## Decisions made during the pass

- 2026-08-07: owner redirected the pass to per-axis review (solo-run rewrites
  were presumptuous for owner-facing prose). New cadence: show each axis's
  rewritten narrative/evidence, owner approves or supplies wording, then
  commit. identity / atmosphere / surface got owner wording (dfe4097, a63d059,
  ee5f66b); orbit and bulk approved as written.
- 2026-08-07: night-hemisphere temperature filled at ~30 K (geothermal-flux
  sigma-T^4 balance, textbook-formula exception; lunar PSR 20-40 K anchor) on
  the owner's "n kelvin" prompt — narrative, typed field and evidence agree.
- 2026-08-07: polar-cap grounding question led to a real §4 gap: the npFe0
  optics were documented but the shielding/cusp geometry was board-level
  reasoning. §4 got a new subsection (lunar magnetic swirls, Ganymede caps)
  + ko mirror; surface evidence now points at it.
- 2026-08-07: crater-density art read recorded in the new
  phase4/art-direction/proxima-d-art-direction.md (owner asked for a light,
  art-direction-depth dig only).
- 2026-08-07: found + fixed a coefficient typo in the tidally-locked
  temperature doc (substellar ceiling "1.19" -> 1.41 = sqrt 2; computed values
  were already correct).
- 2026-08-07: environment side-quests grew out of owner questions: belt
  cross-section viz (proxima_d_phys, inner-belt lower cut = surface, owner
  catch), methodology-derived doses (inner 5e3 / outer 1e3 rad/h central,
  low confidence, scripts/refs/proxima_d_belt_dose.py), and the Alfven-wing
  figure redrawn on the real u +- v_A characteristics after an owner catch.
  Wing = future flux-tube-plugin use case (not expressible in Kerbalism SDF).
- 2026-08-07: repo-wide 공짜 calque sweep (boards + ko mirrors + wiki rebuild);
  banned as translationese in the ko-style memory, word allowed where it
  genuinely means free-of-charge.
- PASS CLOSED 2026-08-07: all 11 d axes owner-reviewed and confirmed, gate
  0 errors / 0 warnings, check.sh fully green. Style precedent for future
  passes: owner tight-form (no self-evident/definitional facts), per-axis
  confirm-before-commit, approved prose frozen (append-only edits).
