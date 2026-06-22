# Plugin brief — RB telescope moon-exclusion (Harmony)

**Status: backlog, delegated to Schultz (2026-06-22).** Separate C# plugin
deliverable, not part of the cfg skill. Batched with the other NearStars
plugins (flux tube, heliotail) at project end.

## Goal

Make NearStars **planets discoverable by telescope, but moons NOT** — moons
stay hidden and are revealed only by flyby (entering their SOI). Native RB
can't do this: its telescope scan adds *every* hidden body in view to the
candidate pool and randomly picks one, so a hidden moon can be found by
telescope (and cascades to reveal its parent).

## The minimal patch

Target: `ResearchBodies` `ModuleTrackBodies` telescope scan that builds the
in-view candidate list (`PartModule.cs`, the `BodiesInView` loop around
lines 222-260 — verify against the installed RB version).

Harmony **Postfix** (or Prefix that filters the list): drop any body that is
a **moon** — i.e. `body.referenceBody != null && !body.referenceBody.isStar`
(a body orbiting a planet, not a star). Leave planets (parent = star) in the
pool. Result: telescope only ever surfaces planets; hidden moons remain
telescope-immune and are found via RB's existing `discoveryByFlyby` (SOI
entry).

## Why Harmony, not a fork

RB ships as a compiled DLL and its README marks parts "All Rights Reserved"
(no redistribute). Harmony patches RB's method at runtime without copying or
shipping RB code — clean license-wise. Guard the plugin so it no-ops when RB
is absent (discoverability is optional).

## Interplay with the cfg skill

No cfg change needed. The `researchbodies-cfg` mapping already emits moons as
`fictional → F F F F` (hidden). This patch only changes *how* a hidden moon
can be found (flyby yes, telescope no). Until the plugin ships, native RB
lets the telescope randomly find hidden moons too — acceptable interim.

## Acceptance check (in-game)

1. New career with RB + NearStars + Kopernicus.
2. Telescope-scan a NearStars system → only the planet is ever discovered,
   never a moon, across repeated scans.
3. Flyby a moon's SOI → moon discovered (RB `discoveryByFlyby`).
4. RB uninstalled → NearStars normal (everything visible), plugin no-ops.
