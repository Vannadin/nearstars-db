---
title: Gameplay — playing NearStars (axis overview)
status: exploratory
created: 2026-06-29
---

# Gameplay — playing NearStars

NearStars has two distinct axes of work:

- **Modelling the bodies** — `phase2/` → `phase3/` → `phase4/`: curation,
  synthesis, and art-direction that turn real astrophysics into game-ready cfg.
- **Playing the mod** — *this directory*: everything that makes the modelled
  systems actually **reachable, navigable, and rewarding to visit.**

These are orthogonal. A perfectly modelled star system is dead content if the
player can never get there or has nothing to do on arrival (see
[`interstellar-expansion/README.md`](interstellar-expansion/README.md)). The
gameplay axis is a **first-class requirement, not afterthought polish** — hence
its own top-level home, parallel to the phase pipeline.

## What lives here

- [`rp1-integration/`](rp1-integration/plan.md) — riding the RP-1 / RO career
  stack (Sol-based). The base-independent career layer NearStars owns:
  ResearchBodies, ROKerbalism radiation, Principia gating, RealAntennas.
- [`interstellar-expansion/`](interstellar-expansion/README.md) — the post-RP-1
  end-game: crossing the gaps. Feasibility (Δv / light floor / relativity), warp
  under Principia, and the lead-intercept navigation planner.
  - `interstellar-expansion/prototypes/` — portable math prototypes (the half
    this side owns; in-game C# is Schultz's lane).
- *(future)* `science-values/` — per-system science payoff tuned to the extended
  tech tree.
- *(future)* `tech-tree/` — where the interstellar branch attaches past the
  completed RP-1 tree, and its balance.

## Status

**Exploratory / brainstorm.** This is the project's far-future layer — it lands
after the confirmed v1 roster and the RP-1 career integration. In-game C#/C++
(warp plugin, planner UI, any Principia fork) is Schultz's lane
([[project-nearstars-mod-plugins-schultz]]); this side does design, spec, cfg,
and math prototypes.

## Related

- [science-system](../docs/reference/science-system.md) — the per-body science
  reference the payoff is built on (kept in `docs/reference`, cross-cutting)
- `phase4/` — the body-modelling axis this sits alongside
