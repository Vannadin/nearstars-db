# ResearchBodies cfg skill — Plan

## Goal

Build a `researchbodies-cfg` skill that converts each NearStars body's
**real detection status** into ResearchBodies MM patches (`ONDISCOVERY` +
`IGNORELEVELS`), implementing the optional **discoverability** axis.

Model: `firefly-cfg` / `principia-cfg` skills (SKILL.md + references/ one
file per node group + a deterministic `scripts/emit_*.py`).

## Why

Discoverability was chosen (2026-06-22) as an optional ResearchBodies
layer: a body stays hidden until the player discovers it via an
observatory/telescope research plan. The mapping principle is the heart
of NearStars' "real observation evidence" identity — in-game discovery
re-enacts how the real exoplanet/star was actually detected. There is no
deep cfg-schema reference for ResearchBodies yet; this skill supplies it
plus the DB → cfg mapping.

## Settled by memory (do NOT re-litigate)

- Optional dependency: `:NEEDS[ResearchBodies&Kopernicus]`. Uninstalled →
  NearStars works normally (everything visible).
- Per-body granularity ceiling = `ONDISCOVERY` + `IGNORELEVELS` only.
  Cost / odds / telescope levels are GLOBAL (not per-body).
- Mapping: **actual detection status → discovery difficulty.**
  - Stars (naked-eye) → always visible.
  - Confirmed planets → visible-ish / low difficulty.
  - Candidates (e.g. JWST) → discovered by observation; `ONDISCOVERY`
    message cites the real detection paper (e.g. Polyphemus =
    Sanghi & Beichman 2024).
  - Fictional moons → revealed after reach/observation.
- Kopernicus auto-integration: RB hides NearStars bodies even with zero
  per-body config; barycenter/binary anchors (radius<100m) handled.
- **Emit runs at project END**, batched with the other cfg writers
  (defer-emit decision). The SKILL is built now; we do NOT run the bulk
  emit yet, and do NOT proactively propose running it.

## Scope

- **In:** ResearchBodies cfg schema reference (source-cited from
  JPLRepo/ResearchBodies), grounded per node group.
- **In:** DB detection-status → IGNORELEVELS difficulty mapping table +
  ONDISCOVERY message template (with real detection-paper citation).
- **In:** deterministic emitter `emit_researchbodies_cfg.py`
  (DB/Phase-anything → MM patch), but NOT a project-wide emit run.
- **Out:** global settings tuning (cost/odds/telescope) — document the
  knobs, but these are a single global block, not per-body work.
- **Out:** Contract Configurator contract authoring (RB supports CC
  integration; note it, don't build it).

## Steps

1. **Research** (delegated subagent) — RB repo cfg loader: every node +
   leaf key the mod reads, each with `file.cs:line` citation; confirm
   ONDISCOVERY / IGNORELEVELS value formats; global vs per-body split;
   shipped example cfgs; Kopernicus/barycenter handling; difficulty enum.
   → verify: a complete schema inventory, source-cited.
2. **Mapping design** — detection method/status → difficulty table.
   Draft proposal, present to owner for review (art-direction facet).
   → verify: owner picks the mapping (no silent passthrough).
3. **references/** — one .md per node group (ondiscovery.md,
   ignorelevels.md, global-settings.md, db-mapping.md, pitfalls.md).
   → verify: every schema claim cites source.
4. **SKILL.md** — frontmatter (name/description trigger phrases/
   mod_version) + body; NearStars conventions pre-set (NEEDS tag, file
   layout, name convention).
   → verify: matches firefly-cfg structure.
5. **emit_researchbodies_cfg.py** — deterministic DB → MM patch.
   → verify: dry-run on confirmed set produces valid-looking cfg; no
   per-body invention beyond the mapping.
6. **Graduate** to `.claude/skills/researchbodies-cfg/`; update
   `docs/reference/tools.md` index + memory pointer.

## Open design question (for owner)

The IGNORELEVELS difficulty mapping — see `mapping-proposal.md` once the
schema research lands.
