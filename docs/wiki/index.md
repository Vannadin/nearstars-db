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

## Cluster: methodology ✓ (Phase 2 ingested 2026-05-24)

> The DB-side schema, fetch pipeline, multi-star epoch resolution,
> and curation workflow.

**Hub:** [methodology](../reference/methodology.md) — schema + epoch rules

| Page | Role | Summary |
|---|---|---|
| [methodology](../reference/methodology.md) | hub | DB schema, epoch handling, source recording, data-sources index |
| [adding_stars](../reference/adding_stars.md) | member | Add a new component to the pipeline |
| [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) | member + physics-epoch hub | Kepler → ICRS for multi-star systems |
| [data-sources](../reference/data-sources.md) | member | External catalog attribution policy |
| [archive_issues](../reference/archive_issues.md) | member | Upstream catalog defects (NASA Archive, TEPCat) |
| [tools](../reference/tools.md) | member | Project-wide tool index by purpose |
| [mod-reference](../reference/mod-reference.md) | member | KSP mod install reference |
| [mod-release-layout](../reference/mod-release-layout.md) | member | Mod-release repo conventions |
| [guideline](../reference/guideline.md) | member | Project-level scope + phases |

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

## Cluster: mod-kopernicus ✓ (Phase 2 ingested 2026-05-25 — Related only)

> Kopernicus cfg generation for new bodies.

**Hub:** `.agents/skills/kopernicus-cfg/SKILL.md`
(Skill-system frontmatter retained; wiki added Related section only.)

(Member listing: see the skill's `references/` directory.)

---

## Cluster: mod-principia ✓ (Phase 2 ingested 2026-05-25)

> Principia n-body patches per scale variant.

**Hub:** [principia-cfg-reference](../reference/principia-cfg-reference.md)
(also a member of [physics-epoch](../reference/binary-epoch-pipeline.md)
secondary cluster)
+ `.agents/skills/principia-cfg/SKILL.md`

---

## Cluster: mod-firefly ✓ (Phase 2 ingested 2026-05-25 — Related only)

> Firefly reentry-effect cfg.

**Hub:** `.agents/skills/firefly-cfg/SKILL.md`
(Skill-system frontmatter retained; wiki added Related section only.)

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

## Cluster: phase3-procedure ✓ (Phase 2 ingested 2026-05-25 — Related only)

> Phase 3 synthesis methodology (paper triage → cfg-ready decisions
> with bilingual viewer).

**Hub:** `.agents/skills/nearstars-phase3/SKILL.md`
(Skill-system frontmatter retained; wiki added Related section only.)

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

## Cluster: system-alpha-cen ✓ (Phase 2 ingested 2026-05-24)

> Alpha Centauri triple system: A, B, Proxima + Proxima's planets.
> α Cen AB is the canonical worked example of the multi-star
> Kepler→ICRS pipeline ([binary-epoch-pipeline §9](../reference/binary-epoch-pipeline.md)).

**Hub:** `phase3/alpha-cen-proxima-system/` workspace

| Page | Type | Scenario | Confidence |
|---|---|---|---|
| [alpha-centauri-a](../phase3/alpha-centauri-a.md) | star | quiet G2V solar twin, visual binary with B | high |
| [alpha-centauri-b](../phase3/alpha-centauri-b.md) | star | quiet K1V metal-rich, no confirmed planets, warm-orange contrast to A | high |
| [proxima-cen](../phase3/proxima-cen.md) | star | M5.5Ve flare star, kG dipole, 7-yr cycle, frequent superflares | high |
| [proxima-cen-b](../phase3/proxima-cen-b.md) | planet | tidally-locked 1.055 M⊕ terrestrial, 1-bar N₂/CO₂ + substellar lens | medium |
| [proxima-cen-d](../phase3/proxima-cen-d.md) | planet | hot tidally-locked Mercury-like sub-Earth, vestigial Na exosphere | medium |

---

## Cluster: comparisons ✓ (Phase 2 ingested 2026-05-24)

> External cross-validation and historical analyses (type=synthesis).

| Page | Status | Summary |
|---|---|---|
| [rex-data-comparison](../reference/rex-data-comparison.md) | promoted | REX v0.9.6 baseline comparison; §10 quantifies Phase 3 → REX delta on TRAPPIST-1 |
| [stellarium-binary-orbit-comparison](../../plans/stellarium-binary-orbit-comparison.md) | active | Stellarium multi-star convention check (Hilditch/Pourbaix match confirmed) |

---

## Cluster: attribution

> Third-party license obligations and citation policy.

**Hub:** [data-sources](../reference/data-sources.md)

(Plus `LICENSE`, `NOTICE` at repo root.)

---

## Recent activity

*Auto-pulled from [log.md](log.md) — top 5 entries.*

1. **2026-05-25 lint** — Phase 2 bootstrap health check (0 orphans, 0 EA leaks, 26/27 frontmatter coverage)
2. **2026-05-25 ingest** — mod-principia cluster + skill cross-refs (4 pages)
3. **2026-05-24 ingest** — methodology concept cluster + comparisons cluster (11 pages: 9 concept + 2 synthesis)
4. **2026-05-24 ingest** — system-alpha-cen cluster (5 entity pages: 3 stars + 2 planets)
5. **2026-05-24 ingest** — system-trappist-1 cluster (7 entity pages)
