---
type: overview
title: "NearStars Wiki Overview"
slug: wiki-overview
updated: 2026-05-24
tier: public
---

# NearStars Wiki Overview

Cluster map and high-level navigation. Updated less frequently than
[index](index.md) — revised on major ingests, not per ingest.

For the per-page catalog, see [index.md](index.md).
For chronological activity, see [log.md](log.md).
For per-session context, see [hot.md](hot.md).

---

## What this wiki covers

NearStars is two things:

1. A **data engine** (`db/systems/*.json`) that fetches and curates
   astronomical measurements for ~150 nearby stellar systems from
   public catalogs (Gaia DR3, SIMBAD, NASA Exoplanet Archive, ORB6).
2. **Downstream cfg writers** (Kopernicus, Principia, Firefly,
   Scatterer, eventually EVE/Volumetrics/Parallax) that turn that data
   into a KSP planet pack.

This wiki documents both, plus the synthesis layers (Phase 1 →
Phase 2 → Phase 3) that produce cfg-ready decisions per body.

---

## Cluster map

```
                      ┌─────────────────────────────────┐
                      │       methodology               │
                      │  (db schema + pipeline)         │
                      └─────┬──────────────────┬────────┘
                            │                  │
                            ▼                  ▼
                  ┌──────────────────┐  ┌──────────────────┐
                  │  physics-epoch   │  │   attribution    │
                  │ (binary Kepler   │  │  (data sources,  │
                  │  + ICRS + Principia│  license / NOTICE)│
                  └────────┬─────────┘  └──────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
     ┌──────────────┐ ┌──────────┐ ┌─────────────┐
     │ mod-kopernicus│ │mod-principia│ │ mod-firefly │
     │   (rendering)│ │  (n-body)│ │  (reentry)  │
     └──────────────┘ └──────────┘ └─────────────┘
              │                          │
              └──────────┐    ┌──────────┘
                         ▼    ▼
                  ┌────────────────────┐
                  │   phase3-procedure │
                  │  (paper triage →   │
                  │   cfg-ready rows)  │
                  └─────────┬──────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
    ┌────────────────┐ ┌────────────┐ ┌──────────────────┐
    │system-trappist-1│ │system-alpha-cen│ │ system-<others> │
    └────────────────┘ └────────────┘ └──────────────────┘

  ┌──────────────────────────────────────────────────────┐
  │  LOCAL-ONLY TIER (gitignored; EA-derived content)    │
  │  ┌──────────────┐ ┌──────────┐ ┌─────────────────┐   │
  │  │ mod-scatterer│ │mod-eve   │ │ mod-volumetrics │   │
  │  └──────────────┘ └──────────┘ └─────────────────┘   │
  │   (read+write by wiki agent; never leaves disk)      │
  └──────────────────────────────────────────────────────┘
```

---

## How to navigate

**By topic**: index → cluster hub → members.

**By system**: index → `system-<name>` cluster → entity pages → linked
papers in `docs/phase3/_papers/` (read-only raw tier).

**By workflow**: AGENTS.md §2 (document hierarchy) → tools.md (script
index) → the cluster relevant to your task.

**By recency**: [log.md](log.md) shows what was touched when.

---

## What this wiki is NOT

- Not a query-time RAG retriever. Pages are pre-curated; the LLM
  reads explicit links, not chunk embeddings.
- Not a Korean-mirror generator. `ko/` mirrors are regenerated from
  English by the user.
- Not an editor of `db/*` raw data. The DB pipeline owns those files;
  the wiki layer just documents them.
- Not a `/dist` builder. Generated cfg artifacts are out of scope.

See `.agents/skills/llm-wiki/SKILL.md` §10 safety rules for the full
list of what the maintainer agent will never do.
