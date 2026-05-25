# Firefly cfg skill — Context notes

## Why now (2026-05-22)

`project-nearstars-mod-refs-pending` flagged Scatterer / EVE / Parallax
/ Firefly as the four missing deep mod refs. User chose Firefly first
(out of order — Scatterer was my recommendation, user overrode).

## Why a skill, not just a doc

Phase 3 → mod cfg is a *transform*, not just reference reading. A
skill (SKILL.md + workflow + references/) captures the transform plus
the schema, mirroring `kopernicus-cfg`. A standalone reference doc
(like `docs/reference/principia-cfg-reference.md`) would only cover
the schema — the user would still need to manually write the cfg.

## Source-of-truth discipline

Per CLAUDE.md §10 (Read Errors, Don't Guess), every schema claim must
cite the Firefly source file (or shipped example cfg) it came from.
No "I think this field exists because it's a standard pattern" —
either grep the loader or omit the field.

This is especially important because Firefly is a relatively young
mod with no formal cfg documentation; community knowledge is sparse.

## Decisions made

- **Workspace before live**: same pattern as
  `nearstars-phase3-workspace/`. Skill lives at
  `.agents/skills/firefly-cfg-workspace/draft/` during build, swaps
  to `.claude/skills/firefly-cfg/` on completion.
- **References per node group, not per concept**: matches
  `kopernicus-cfg` (one file per cfg node). Easier to find the right
  file when writing a cfg by hand.
- **phase3-mapping.md is part of *this* skill, not Phase 3 skill**:
  The mapping is consumed when *writing Firefly cfg from Phase 3
  data*, so it belongs to the cfg-writer skill, not the synthesizer.

## Open questions for later

- Firefly version pinning — does NearStars currently target a
  specific Firefly release? If so, schema work pins to that.
- Whether to bundle a validator script (`scripts/validate.py`) that
  parses a Firefly cfg and checks against the documented schema.
  Defer until after Step 2 — if the schema is small enough, manual
  review is fine.

## Out of bounds

- Phase 3 skill (workspace at `nearstars-phase3-workspace/`).
- Other mod refs.
- NearStars cfg file structure (covered by `mod-release-layout.md`).
