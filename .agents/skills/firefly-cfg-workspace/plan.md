# Firefly cfg skill — Plan

## Goal

Build a `firefly-cfg` skill that converts Phase 3 synthesis output
(atmosphere composition, surface conditions, re-entry intensity, body
visual style) into Firefly mod cfg patches.

Model: `kopernicus-cfg` skill (SKILL.md + references/ with one file per
cfg node group).

## Why

Phase 3 produces fields that map to Firefly atmospheric-effects cfg,
but currently there is no deep cfg-schema reference for Firefly. Phase
3 visual rows that feed Firefly (re-entry color, intensity, shock
behavior, body-specific overrides) are therefore inferred. The memory
note `project-nearstars-mod-refs-pending` flags this as one of four
missing deep refs.

## Scope

- **In:** Firefly cfg schema across atmofx, body color profile, vessel
  override, particle config — every node the mod actually reads.
- **In:** Phase 3 row → Firefly field mapping table (which Phase 3
  Decisions or measurement feeds which cfg key).
- **Out:** Phase 3 skill itself (its overhaul is staged separately at
  `nearstars-phase3-workspace/`).
- **Out:** Other mod refs (Scatterer / EVE / Parallax — separate work).

## Steps

1. **Research** — Firefly GitHub repo (M1rageDev/Firefly):
   - Locate cfg loader source (which nodes / keys are parsed).
   - Inventory example configs shipped with the mod.
   - Note version (stock cfg surface vs Patreon/dev branch differences
     if any).
   - Verify: a list of all top-level nodes + every leaf key the loader
     reads, each with source-file:line citation.

2. **Schema writeup** — one references/*.md per node group, modeled
   on principia-cfg-reference.md / kopernicus-cfg references:
   - node-name, parent, required vs optional, value type, unit,
     accepted range / enum.
   - Realistic example block from shipped configs.
   - Pitfalls section (what silently fails, what crashes the loader).
   - Verify: every key in the inventory has a row; every example
     parses against the schema.

3. **Phase 3 → Firefly mapping** — one references/phase3-mapping.md:
   - For each Firefly cfg field, which Phase 3 Decisions row (or raw
     measurement) is the source.
   - Note synthesis rules (e.g., re-entry color from atmosphere
     composition + scale height).
   - Verify: every Firefly field is either mapped to Phase 3 or
     explicitly marked "NearStars-fixed / out of synthesis".

4. **SKILL.md draft** — workflow:
   - Inputs: Phase 3 host directory.
   - Steps: load Phase 3 → fill mapping → emit cfg patch → validate.
   - References pointers (don't inline schema).
   - Korean header comment per CLAUDE.md §6.
   - Verify: <500 lines, all references reachable.

5. **Test cases** — 2-3 real Phase 3 hosts that exercise different
   atmosphere types (e.g., TRAPPIST-1 e thin H2O, TRAPPIST-1 b airless,
   Proxima b speculative). Place in `evals/`.
   - Verify: each test produces a cfg that loads in Firefly without
     log warnings.

6. **Iterate** with skill-creator eval loop until tests pass.

## Non-goals (this pass)

- No Phase 3 skill changes.
- No mod-grounded-fields.md edits (the thin mapping there stays as-is
  until this skill lands).
- No commits until user reviews the draft.
