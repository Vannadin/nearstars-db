---
title: Interstellar expansion — purpose & scope
status: exploratory
created: 2026-06-28
---

# Interstellar expansion — purpose

**Thesis.** A star system you cannot *reach and play* is dead content. NearStars
can model every nearby star system perfectly — real orbits, atmospheres, visuals,
science definitions — and it is still **worthless if the player can never get
there and do anything once they arrive.** Implementing the systems is *necessary
but not sufficient*. The gameplay layer — interstellar travel, navigation, and a
science payoff that justifies the trip — is a **first-class requirement, not
afterthought polish.**

This directory exists because that gameplay layer turned out to be the hard part,
and it must be solved (or proven solvable) for the whole mod to have a point.

## What "gameplay must work" concretely means

A reachable, playable NearStars needs all of:

1. **Travel is physically possible.** Can a craft actually cross the gap in a
   playable timeframe with plausible propulsion? → `feasibility.md` (gate 0: Δv,
   the light-speed floor, relativity, the warp-mod survey).
2. **Travel is mechanically possible in the engine.** Does the travel mechanic
   coexist with the stack the player runs (Principia + RP-1)? → `warp-and-
   navigation-brainstorm.md` (warp under Principia, the options ladder, the
   minimal-fork path).
3. **You can navigate it.** Principia moves the stars, so you must aim where the
   target will be on arrival → the interstellar lead-intercept planner.
4. **Arriving is worth it.** The science (and whatever else) on offer must justify
   a multi-year/decade mission → per-body science values
   ([[reference-science-system]]), balanced against the extended tech tree.
5. **It fits the progression.** This is a **post-RP-1 end-game expansion** — it
   attaches past the completed real-world tech tree, with its own propulsion and
   balance.

If any one of these fails, the star systems are scenery you can look at on the map
and never visit. That is the failure mode this work exists to prevent.

## Status

**Exploratory / brainstorm.** Foundations are captured but nothing is committed.
This is the project's far-future layer (after the confirmed v1 roster and RP-1
career integration land). In-game C#/C++ (warp plugin, planner UI, any Principia
fork) is Schultz's lane ([[project-nearstars-mod-plugins-schultz]]); this side
does design, spec, cfg, and math prototypes.

## Documents

- [`feasibility.md`](feasibility.md) — gate 0: is interstellar travel physically
  buildable/playable at real distances (Δv, light floor, relativity, warp mods).
- [`warp-and-navigation-brainstorm.md`](warp-and-navigation-brainstorm.md) — warp
  mechanics under Principia, options ladder (no-fork / minimal-fork / big-fork),
  cruise architecture, velocity continuity, the lead-intercept planner.
- [`planner-spec.md`](planner-spec.md) — the Δv-based lead-intercept planner: math
  spec, `v_avg = c·tanh(Δv/4)`, the three-leg profile, and the DB-data prototype.
  Prototypes in [`prototypes/`](prototypes/).

## Related

- [rp1-integration](../rp1-integration/plan.md) — the career stack this expansion sits on top of
- [science-system](../../docs/reference/science-system.md) — the per-body science payoff (point 4)
