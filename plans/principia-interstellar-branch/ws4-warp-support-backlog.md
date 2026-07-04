# WS4 — warp (FTL) support under Principia [BACKLOG — owner-approved 2026-07-03, not started]

Owner decision (2026-07-03): a fourth workstream, to be done AFTER WS1–3 are validated
in-game. This file is a stub so the idea and its grounding survive.

**RESEARCH DONE (2026-07-04): see `research/R7-warp-support.md`** — current-code re-grounding,
failure catalog, approach decision. **Owner chose minimal-fork (2026-07-04).** The C++ side is
**verified done, no fork needed** — `WarpReadoptionLandsInDestinationSubsystem` (fork commit
`1727a86fa`) confirms a re-adopted vessel lands in its destination star's subsystem at the correct
origin. **C#/adapter implementation handoff: `ws4-minimal-warp-adapter-handoff.md`** (Windows
session). The big-fork `VesselWarpTo` C ABI sketched in §3 below is the rejected alternative.

## Problem

FTL/warp-drive mods (Alcubierre-style) write the stock `Orbit` or teleport the vessel,
which Principia forbids. WS1–3 do not change this. Native support means honestly re-seeding a
vessel at a new position/velocity — either via a plugin API inside Principia's own model
(big-fork), or by detaching the vessel so a cruise layer moves it and letting Principia re-seed
on dropout (minimal-fork, R7-recommended). [Correction: the incompatibility was previously
attributed to "PersistentThrust, Principia issue #2347" — #2347 is actually the still-open
"Burn in time warp with RO ion engines" request; the anti-warp position is in Principia's FAQ,
which names Blueshift explicitly. See R7 §8.]

## Why it is NOW feasible (what WS1–3 already provide)

- WS1: per-subsystem representations + `Ephemeris::subsystem_conversion` — a warp
  destination light-years away is representable at full precision, and the vessel
  rebasing mechanism (vessel.cpp `rebase_distance_threshold`) already handles switching
  representation on arrival.
- WS2: the void is exactly force-free (far-field damping) — a mid-void warp entry/exit
  state is numerically clean; no tail forces to reconcile.
- WS3: the `VesselSetOnRailsBurn` pattern (journal.proto extension + interface +
  adapter harvest branch) is the template for the new API; a "displace vessel" call is
  strictly simpler (no integration change, one trajectory re-seed).

## Expected shape (to be confirmed by an R6 research pass)

1. Plugin API `VesselWarpTo(guid, degrees_of_freedom, …)` (name TBD): terminate the
   psychohistory, append a discontinuity-marked point (or start a fresh history — check
   how DiscreteTrajectory segments + downsampling react to a teleport), trigger the
   subsystem rebase if the destination is across the void.
2. Journal messages + C interface + adapter hook (per the WS3 recipe).
3. Interop layer for existing warp mods is per-mod work (they must call our API);
   shipping our own minimal warp part/module may be simpler than patching foreign mods.
4. Open questions for the research pass: energy bookkeeping (do we care?), history
   semantics of a discontinuity (flight plans/predictions across a warp,
   checkpointer/reanimator per the R5 §7 lifecycle rule), save compatibility, and
   whether upstream would ever take this (likely fork-only — flag in every commit).

## Priority

After: WS2 gate (done on Mac), cross-workstream interaction tests, Windows adapter +
in-game validation of WS1–3. Owner: "이거는 나중에 하자."
