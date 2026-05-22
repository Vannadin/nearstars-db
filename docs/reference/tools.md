# Tools — NearStars

The project has grown to roughly thirty scripts plus several agent skills spread across multiple directories. This document indexes them **by purpose**, not by location. Each section is one logical unit of work — fetch data, build a viewer, generate mod cfg — and lists every file that participates.

## At a glance

| # | Group | What it does | Entry point |
|---|-------|--------------|-------------|
| 1 | Data engine | Fetch raw → assemble per-system JSON → validate | `./run_pipeline.sh` |
| 2 | DB → HTML viewer | Render `db/systems/` into the static site | `scripts/pipeline/build_site.py` |
| 3 | Phase 3 synthesis | ADS+arXiv triage → cfg-ready Decisions + bilingual viewer | `nearstars-phase3` skill |
| 4 | Stability sandbox | REBOUND N-body for hypothetical moons / extra planets | `phase3/stability-sim/scripts/run.py` |
| 5 | External cross-check | Compare DB positions against Stellarium | `scripts/verification/stellarium_crosscheck.py` |
| 6 | Kopernicus cfg | DB → Kopernicus `.cfg` patches | `kopernicus-cfg` skill |
| 7 | Principia cfg | DB → Principia n-body patches | `principia-cfg` skill |
| 8 | Add star / Phase 2 curation | New-star DB entry procedure | `nearstars-add-star` skill |
| 9 | Dev helpers | Markdown preview, ko/ mirror parity | `scripts/preview-md.sh`, `scripts/check-mirrors.sh` |

## Verification & QA — index

Correctness checks live across several functional groups. This index gathers them in one place for visibility — each tool is also documented in its parent group.

| Verifies | Tool / Activity | Group | Run when |
|----------|-----------------|:-----:|----------|
| Schema integrity of `db/systems/*.json` | `scripts/pipeline/validate.py` | [1](#1-data-engine) | After every build (auto-invoked by `run_pipeline.sh`) |
| Hierarchical binary structure | `scripts/pipeline/test_hierarchical.py` | [1](#1-data-engine) | Smoke test after binary-orbit edits |
| DB positions vs Stellarium | `scripts/verification/stellarium_crosscheck.py` | [5](#5-external-cross-check) | Spot-check before publishing |
| Dynamical stability of curated + hypothetical bodies | `phase3/stability-sim/scripts/run.py` | [4](#4-stability-sandbox) | Before shipping a moon / extra-body cfg, or as a baseline-DB sanity check |
| `ko/` mirror file parity | `scripts/check-mirrors.sh` | [9](#9-dev-helpers) | Before commit / release |
| Phase 3 synthesis policy fit | `nearstars-phase3` audit-pass procedure | [3](#3-phase-3-synthesis-pipeline) | After a synthesis batch — manual, output at `phase3/<system>/audit-pass-<YYYY-MM-DD>.md` |

## 1. Data engine

**Purpose.** Pull astrometry / photometry / stellar-property / planet measurements from public catalogs, assemble them into per-system JSON, and validate.

**Trigger.** New star added to target list, catalog refresh, schema change.

**Files.**
- `scripts/pipeline/fetch_astrometry.py` — Gaia DR3 TAP, SIMBAD fallback (RA, Dec, parallax, proper motion, RV)
- `scripts/pipeline/fetch_photometry.py` — Gaia G + Hipparcos V-mag
- `scripts/pipeline/fetch_stellar_props.py` — Teff, spectype, mass, radius via SIMBAD
- `scripts/pipeline/fetch_planets.py` — NASA Exoplanet Archive TAP
- `scripts/pipeline/fetch_planets_ps.py` — Planetary Systems default-param table
- `scripts/pipeline/fetch_stellarium_ids.py` — Stellarium Web skysource ID lookup
- `scripts/pipeline/build_systems.py` — raw + curated → `db/systems/*.json`
- `scripts/pipeline/build_curated_from_ps.py` — seed `planets_curated.json` from PS defaults
- `scripts/pipeline/generate_target_list.py` — rebuild `target_list.json` from `db/systems/`
- `scripts/pipeline/validate.py` — schema validation; exits non-zero on failure
- `scripts/pipeline/schema.py` — shared schema + validators
- `scripts/pipeline/test_hierarchical.py` — hierarchical binary structure test

**Orchestrator.** `./run_pipeline.sh` runs fetch → build → validate → site build in order.

**I/O.** `db/target_list.json` → `db/*_raw.json` → `db/systems/*.json`.

## 2. DB → HTML viewer

**Purpose.** Render `db/systems/` + Phase 2 measurements into the static HTML viewer at `docs/`.

**Files.**
- `scripts/pipeline/build_site.py` — generates `docs/data.json` + main `index.html`
- `scripts/pipeline/build_phase2_html.py` — per-system Phase 2 paper-by-paper viewer
- `scripts/pipeline/build_reports_index.py` — Phase 2/3 reports landing index

**Output.** `docs/{data.json, index.html, phase2/*.html, reports.html}`.

## 3. Phase 3 synthesis pipeline

**Purpose.** Convert Phase 2 measurements into cfg-ready synthesis decisions with a bilingual per-planet HTML viewer.

**Trigger.** Phrases like "Phase 3 진행", "<planet> 합성", "이 행성 Phase 3 까지 올려줘".

**Files.**
- `scripts/phase3/score_papers.py` — triage incoming bibcodes
- `scripts/phase3/fetch_arxiv_texts.py` — pull full-text PDFs from arXiv
- `scripts/phase3/build_bibliography.py` — bibcode → reference dict
- `scripts/phase3/build_manual_fetch.py` — list papers needing manual download
- `scripts/phase3/expand_citations.py` — inline citations in synthesis text
- `scripts/phase3/field_tooltips.py` — tooltip glossary for the viewer
- `scripts/phase3/build_html.py` — per-planet HTML (en + ko mirror, toggle)
- `phase3/<system>/add_missing_papers.py` — per-system follow-up additions

**Driver.** `nearstars-phase3` skill — defines the procedure (triage → deep-read → synthesize → validate → ko mirror → visual check).

**Audit pass.** After a synthesis batch the skill prescribes an external audit — each Decisions row reviewed against post-retrofit policies (mod-grounded fields, documented divergence). Output is a manual report at `phase3/<system>/audit-pass-<YYYY-MM-DD>.md`. See `phase3/trappist-1-system/audit-pass-2026-05-22.md` for the canonical example.

**Output.** `docs/phase3/*.html`, `phase3/<system>/manual-paper-followup.md`, `phase3/<system>/audit-pass-*.md`.

## 4. Stability sandbox

**Purpose.** Verify that hypothetical moons or extra planets stay dynamically stable before they get committed to a Kopernicus / Principia cfg. Doubles as a baseline-stability check for the curated systems themselves.

**Trigger.** Adding a moon or extra body, or sanity-checking the curated DB before shipping.

**Files.**
- `phase3/stability-sim/scripts/load.py` — DB JSON → REBOUND `Simulation`
- `phase3/stability-sim/scripts/run.py` — WHFast + MEGNO main entry
- `phase3/stability-sim/hypotheticals/<system>.json` — extra-body spec

**Stack.** REBOUND 5.0 in `.venv/`, AU / yr / Msun units, 10⁴ yr default horizon.

**Output.** `phase3/stability-sim/results/{system}_summary.json` + `_timeseries.csv`, `phase3/stability-sim/STABILITY_REPORT.md`.

## 5. External cross-check

**Purpose.** Validate DB-computed positions against an independent source.

**Files.**
- `scripts/verification/stellarium_crosscheck.py` — compare DB RA/Dec to Stellarium Web

**Output.** Console diff report.

## 6. Kopernicus cfg generation

**Purpose.** Turn `db/systems/` + Phase 3 synthesis into Kopernicus `.cfg` patches.

**Range.** ~50 ly (Kopernicus terrain budget cap).

**Driver.** `kopernicus-cfg` skill.

**Output.** `dist/NearStars-Configs/Patches/Kopernicus/`.

## 7. Principia cfg generation

**Purpose.** Turn `db/systems/` into Principia `gravity_model` + `initial_state` patches for n-body gravity.

**Range.** ~80 ly (further than Kopernicus — no terrain mesh required).

**Driver.** `principia-cfg` skill.

**Output.** `dist/NearStars-Configs/Patches/Principia/`.

## 8. Add star / Phase 2 curation

**Purpose.** Procedure for adding a new star (target list → fetch → curate → validate) and for upgrading an existing star's Phase 2 curation depth.

**Driver.** `nearstars-add-star` skill.

**Files.**
- `phase2/<system>/apply_phase2.py` — per-system script that loads paper-by-paper measurements into `db/planets_curated.json` (array form, recommended-flagged). Run when upgrading Phase 1 → Phase 2 for a specific system.

**Workflow.** Edit `target_list.json` → `./run_pipeline.sh` → manual curation of `stellar_props_curated.json`, `planets_curated.json`, `binary_orbits.json` (or run `apply_phase2.py` for systems with a paper-batch script) → re-validate.

## 9. Dev helpers

**Purpose.** Day-to-day workflow utilities.

**Files.**
- `scripts/preview-md.sh <md-file>` — render markdown to HTML and open in the browser
- `scripts/check-mirrors.sh` — verify `ko/` mirror parity (missing or stale files)

## Skills directory layout

Project-specific skills currently live in two parallel trees — pending consolidation.

| Skill | `.claude/skills/` | `.agents/skills/` |
|-------|:----:|:----:|
| `kopernicus-cfg` | ✓ | ✓ |
| `principia-cfg` | ✓ | — |
| `nearstars-add-star` | ✓ | ✓ |
| `nearstars-phase3` | — | ✓ |
| `find-skills` (generic) | ✓ | ✓ |

`firefly-cfg-workspace/` and `nearstars-phase3-workspace/` in `.agents/skills/` are working directories, not actual skills.

## Dependency graph

```
target_list.json
     ↓
[1] Data engine ──→ db/systems/*.json
                          │
                          ├──→ [2] HTML viewer ─────→ docs/
                          │
                          ├──→ [3] Phase 3 synth ───→ docs/phase3/
                          │
                          ├──→ [4] Stability sim ───→ phase3/stability-sim/results/
                          │
                          ├──→ [5] Stellarium x-check
                          │
                          ├──→ [6] kopernicus-cfg ──→ dist/.../Kopernicus/
                          │
                          └──→ [7] principia-cfg ──→ dist/.../Principia/

[8] nearstars-add-star — procedure that drives the whole chain for a new star
[9] Dev helpers — orthogonal to the chain
```
