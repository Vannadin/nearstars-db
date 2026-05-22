# Firefly cfg skill — Checklist

## Setup

- [x] Workspace directory created
- [x] plan.md / checklist.md / context-notes.md drafted

## Step 1 — Research (Firefly GitHub inventory)

- [x] Repo located (M1rageDev/Firefly @ master, GPL-3.0)
- [x] cfg loader source identified (`Source/Firefly/ConfigManager.cs`
      + `Source/Firefly/SettingsManager.cs`)
- [x] Top-level nodes listed with source citation (5 nodes)
- [x] All leaf keys per node listed with type + range
- [x] Example configs inventoried (Default, Stock, RSS, OPM, MPE,
      KSRSS, Kcalbeloh)
- [x] No separate Patreon/dev branch — master is current
- [x] Findings written to `research-notes.md`

## Step 2 — Schema writeup (references/*.md)

- [x] color-format.md (HDR color value syntax — shared)
- [x] atmofx-body.md
- [x] atmofx-planet-pack.md
- [x] atmofx-part.md
- [x] atmofx-particles.md
- [x] atmofx-settings.md
- [x] composition-color.md (verified thunderchild chart + bulk-gas
      reentry plasma table)
- [x] pitfalls.md
- [x] Each example block validated against shipped configs

## Step 3 — Phase 3 → Firefly mapping

- [x] phase3-mapping.md — every Firefly field mapped or marked
      "NearStars-fixed" / new Phase 3 fields proposed
- [x] Synthesis rules documented (pressure → multipliers, composition
      → color via composition-color.md, temp → particle_threshold)
- [x] Worked example: TRAPPIST-1 e (full atmo) + b (airless edge)

## Step 4 — SKILL.md

- [x] Frontmatter (name, description with pushy triggers, mod_version
      pinned to 1.0.6)
- [x] Inputs / outputs documented (Phase 3 directory → cfg)
- [x] 8-step workflow (trigger → derive → emit → validate)
- [x] References pointers to 9 reference files
- [x] 206 lines (target <500)
- [x] Korean header skipped (per kopernicus-cfg precedent — SKILL.md
      is config-with-content, not source)

## Step 5 — Test cases

- [ ] evals/evals.json with 2-3 hosts
- [ ] Each test exercises a different atmosphere class

## Step 6 — Eval loop

- [ ] with-skill + baseline runs
- [ ] feedback.json reviewed
- [ ] Iterate until pass rate satisfactory

## Apply

- [ ] User review of draft skill
- [ ] Swap to live (`.agents/skills/firefly-cfg/`)
- [ ] Update `project_nearstars_mod_refs_pending` memory (Firefly →
      covered)
- [ ] Single commit
