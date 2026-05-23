---
type: index
title: "NearStars Wiki Index"
slug: wiki-index
updated: 2026-05-24
tier: public
bootstrap_status: in-progress
---

# NearStars Wiki Index

LLM-maintained catalog of project documentation, grouped by **cluster**.
This file is rebuilt by `/wiki refresh` and `/wiki ingest`; do not
edit cluster entries by hand — edit the source pages, then re-run.

**Navigation.** Start with [overview](overview.md) → cluster hub → member
pages. Recent activity in [log](log.md). Session context in [hot](hot.md).

> **Bootstrap state.** This index is being populated as the
> [llm-wiki](../../.agents/skills/llm-wiki/SKILL.md) skill ingests
> each existing wiki page. Until bootstrap completes, expect partial
> entries and stale cluster counts. See the skill's §11 for current
> bootstrap progress.

---

## Cluster: methodology

> The DB-side schema, fetch pipeline, multi-star epoch resolution,
> and curation workflow.

**Hub:** [methodology](../reference/methodology.md) — schema + epoch rules

| Page | Summary |
|---|---|
| [adding_stars](../reference/adding_stars.md) | Add a new component to the pipeline |
| [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) | Kepler → ICRS for multi-star systems |
| [data-sources](../reference/data-sources.md) | External catalog attribution policy |
| [archive_issues](../reference/archive_issues.md) | Upstream catalog defects (NASA Archive, TEPCat) |
| [tools](../reference/tools.md) | Project-wide tool index by purpose |
| [mod-reference](../reference/mod-reference.md) | KSP mod install reference |
| [mod-release-layout](../reference/mod-release-layout.md) | Mod-release repo conventions |
| [guideline](../reference/guideline.md) | Project-level scope + phases |
| [rex-data-comparison](../reference/rex-data-comparison.md) | REX v0.9.6 vs NearStars |

---

## Cluster: physics-epoch

> Multi-star Kepler → ICRS pipeline and Principia epoch handling.

**Hub:** [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md)

| Page | Summary |
|---|---|
| [principia-cfg-reference](../reference/principia-cfg-reference.md) | Principia cfg API |

(Overlaps with methodology cluster — `binary-epoch-pipeline.md` is a
member of methodology and a hub of physics-epoch.)

---

## Cluster: mod-kopernicus

> Kopernicus cfg generation for new bodies.

**Hub:** `.agents/skills/kopernicus-cfg/SKILL.md`

(Member listing: see the skill's `references/` directory.)

---

## Cluster: mod-principia

> Principia n-body patches per scale variant.

**Hub:** [principia-cfg-reference](../reference/principia-cfg-reference.md)
+ `.agents/skills/principia-cfg/SKILL.md`

---

## Cluster: mod-firefly

> Firefly reentry-effect cfg.

**Hub:** `.agents/skills/firefly-cfg/SKILL.md`

(Member listing: see the skill's `references/` directory.)

---

## Cluster: mod-scatterer (LOCAL-ONLY)

> Scatterer cfg generation. EA-derived; commit-blocked.

**Hub:** `.agents/skills/scatterer-cfg/SKILL.md` *(existence only;
content is local-only — see [feedback-patreon-assets memory])*

(Member listing only in the local-only wiki overlay.)

---

## Cluster: mod-eve / mod-volumetrics (LOCAL-ONLY, planned)

> EVE Volumetric Clouds V5 + V3→V5 conversion. Workspace not yet
> spawned (2026-05-24). EA-derived; commit-blocked.

---

## Cluster: phase3-procedure

> Phase 3 synthesis methodology (paper triage → cfg-ready decisions
> with bilingual viewer).

**Hub:** `.agents/skills/nearstars-phase3/SKILL.md`

---

## Cluster: system-trappist-1 ✓ (Phase 2 ingested 2026-05-24)

> The 7 confirmed TRAPPIST-1 planets. Host star entity page not yet
> created (M8V dwarf — see open follow-up in [log](log.md)).

**Hub:** `phase3/trappist-1-system/` workspace

| Page | Scenario | Confidence |
|---|---|---|
| [trappist-1-b](../phase3/trappist-1-b.md) | airless ultramafic (JWST-confirmed) | high |
| [trappist-1-c](../phase3/trappist-1-c.md) | thin O₂ over basalt | medium |
| [trappist-1-d](../phase3/trappist-1-d.md) | thin atm + terminator H₂O ice | low |
| [trappist-1-e](../phase3/trappist-1-e.md) | aquaplanet eyeball (best habitable) | high |
| [trappist-1-f](../phase3/trappist-1-f.md) | eyeball aquaplanet (1 bar CO₂) | medium |
| [trappist-1-g](../phase3/trappist-1-g.md) | full snowball | medium |
| [trappist-1-h](../phase3/trappist-1-h.md) | frozen sub-Mars + patchy frost | low |

---

## Cluster: system-alpha-cen

> Alpha Centauri triple system: A, B, Proxima + Proxima's planets.

**Hub:** `phase3/alpha-cen-proxima-system/` workspace

| Page | Summary |
|---|---|
| [alpha-centauri-a](../phase3/alpha-centauri-a.md) | G2V primary |
| [alpha-centauri-b](../phase3/alpha-centauri-b.md) | K1V companion |
| [proxima-cen](../phase3/proxima-cen.md) | M5.5V third component |
| [proxima-cen-b](../phase3/proxima-cen-b.md) | HZ rocky planet |
| [proxima-cen-d](../phase3/proxima-cen-d.md) | sub-Earth inner planet |

---

## Cluster: comparisons

> External cross-validation and historical analyses.

| Page | Summary |
|---|---|
| [rex-data-comparison](../reference/rex-data-comparison.md) | REX v0.9.6 baseline comparison |
| [stellarium-binary-orbit-comparison](../../plans/stellarium-binary-orbit-comparison.md) | Stellarium multi-star convention check |

---

## Cluster: attribution

> Third-party license obligations and citation policy.

**Hub:** [data-sources](../reference/data-sources.md)

(Plus `LICENSE`, `NOTICE` at repo root.)

---

## Recent activity

*Auto-pulled from [log.md](log.md) — top 5 entries.*

1. **2026-05-24 ingest** — system-trappist-1 cluster (7 entity pages)
2. **2026-05-24 initialize** — wiki scaffold created
