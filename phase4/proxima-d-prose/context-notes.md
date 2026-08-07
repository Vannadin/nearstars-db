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
