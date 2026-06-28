# ResearchBodies × RO / RP-1 compatibility

**Status: planned for a future update (2026-06-22 owner decision; design
grounded 2026-06-26).** The current skill targets non-RP-1 environments
(Sandbox / Science, where RB works as shipped). RP-1 career support is a
documented backlog item — design captured here so it is not re-derived.
Integration approach below is grounded in upstream RP-1 source; see
[`plans/rp1-integration/`](../../../../plans/rp1-integration/plan.md) for the
project-wide context (NearStars stays Sol-based and rides on Sol-Configs'
upstream RP-1 bridge; only the base-independent career layers here are ours).

## The problem (verified from RB source v1.13.0.0)

NearStars only authors `ONDISCOVERY` + `IGNORELEVELS` (hide/show data),
but the **discovery action** depends on RB's own machinery, which is
built for the stock tech tree + stock funds economy:

- **Telescope parts** `TrackBodiesTelescope` / `InfraredTelescope` ship
  with `TechRequired = spaceExploration`, `entryCost = 9530`
  (`Distribution/.../Parts/telescope/telescope.cfg:11-12`). RP-1 deletes the
  stock tree and **routes `spaceExploration` to its unbuildable `orphanParts`
  sink** (`RP-1/Tree/OrphanNode.cfg`: `@TechRequired ^=:^spaceExploration$:orphanParts:`),
  so the part becomes junk that can't be unlocked.
- **RB Contract Configurator contracts** (`Distribution/.../Contracts/
  CC_RB_*.cfg`) are not balanced for RP-1's progression — clash /
  duplication risk.
- RB's Kopernicus patch only bumps telescope range
  (`ResearchBodiesMMKopernicus.cfg`) — no RP-1/RO awareness.

**Consequence in RP-1:** if the discovery mechanism is unreachable, a
NearStars body authored `false ...` in IGNORELEVELS stays hidden forever
= soft-lock.

Community status: RP-1's "Extra Mods to Consider" wiki lists RB neither
as recommended nor blacklisted — not a standard RP-1 combo.

## Planned RP-1 integration patch (when built)

Guard everything `:NEEDS[ResearchBodies&RP-0]` (RP-1's MM tag is `RP-0`)
or `:NEEDS[ResearchBodies&RealismOverhaul]`, so it only applies in that
stack:

1. **(Recommended) Drop the part dependency entirely.** Set the global
   `@RESEARCHBODIES:AFTER[ResearchBodies] { @allowTrackingStationLvl1 =
   true }` so RB performs discovery from the **stock Tracking Station
   building** rather than the telescope part — sidesteps the dead tech node
   entirely. (`allowTrackingStationLvl1` is an RB global key, see
   `global-settings.md`.) Note: RP-1 has **no astronomy-observatory mechanic
   of its own** (its TrackingStation is a DSN/comms facility upgraded via
   CustomBarnKit); this option works because it is RB repurposing the stock
   building, not a dependency on any RP-1 feature.
2. **(Alternative) Reseat the telescope part** onto a live RP-1 node instead
   of the dead `spaceExploration`:
   `@PART[TrackBodiesTelescope|InfraredTelescope]:NEEDS[RP-0] { @TechRequired
   = scienceSatellite }`. `scienceSatellite` ("Satellite Era Science",
   1956-60) is exactly where RP-1 relocates its own `spaceExploration`-tagged
   film cameras (`RP-1/Tree/TREE-Parts.cfg`); `deepSpaceScience` is the later
   alternative for a deep-space framing. Use this only if (1) is not wanted.
3. **Suppress RB's stock contracts under RP-1.** RP-1 does not disable
   third-party Contract Configurator packs, so `CC_RB_*` would appear and
   pollute its tuned progression. Cleanest: **ship NearStars' RB contracts
   gated `:NEEDS[!RP-0]`** so they load only outside RP-1 — RP-1 careers stay
   clean, non-RP-1 installs still get telescope-discovery contracts.
4. **Re-verify** discovery still reaches NearStars bodies — RB already widens
   `observatorylvl1range`/`observatorylvl2range` under Kopernicus; confirm the
   range covers our distances at the chosen TS level.

Until this patch exists, the recommended guidance is: **RP-1 players omit
ResearchBodies** — discoverability is `:NEEDS[ResearchBodies&Kopernicus]`
optional, so without RB every NearStars body is simply visible and the
game is fully playable.
