# ResearchBodies × RO / RP-1 compatibility

**Status: planned for a future update (2026-06-22 owner decision).** The
current skill targets non-RP-1 environments (Sandbox / Science on RSS,
where RB works as shipped). RP-1 career support is a documented backlog
item — design captured here so it is not re-derived.

## The problem (verified from RB source v1.13.0.0)

NearStars only authors `ONDISCOVERY` + `IGNORELEVELS` (hide/show data),
but the **discovery action** depends on RB's own machinery, which is
built for the stock tech tree + stock funds economy:

- **Telescope parts** `TrackBodiesTelescope` / `InfraredTelescope` ship
  with `TechRequired = spaceExploration`, `entryCost = 9530`
  (`Distribution/.../Parts/telescope/telescope.cfg:11-12`). RP-1 uses a
  custom tech tree + a non-funds economy, so the part lands in a
  wrong/unreachable node and can't be bought normally.
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

1. **Drop the part dependency.** Set the global
   `@RESEARCHBODIES:AFTER[ResearchBodies] { @allowTrackingStationLvl1 =
   true }` so discovery uses the **Tracking-Station-level observatory**
   instead of the telescope part — sidesteps the tech-tree problem
   entirely. (`allowTrackingStationLvl1` is a global key, see
   `global-settings.md`.)
2. **Reseat or hide RB's telescope part** in the RP-1 tech tree
   (`@PART[TrackBodiesTelescope]:NEEDS[RP-0] { @TechRequired = <rp1 node> }`)
   OR disable it if (1) is sufficient.
3. **Disable RB's stock contracts** under RP-1 to avoid clashing with
   RP-1's contract pack (delete/`-`the `CC_RB_*` contract groups, or
   gate them off `:NEEDS[!RP-0]`).
4. **Re-verify** discovery still reaches our ~50 ly bodies — RB already
   widens `observatorylvl1range`/`observatorylvl2range` under Kopernicus,
   but confirm the range covers NearStars distances at the chosen
   observatory level.

Until this patch exists, the recommended guidance is: **RP-1 players omit
ResearchBodies** — discoverability is `:NEEDS[ResearchBodies&Kopernicus]`
optional, so without RB every NearStars body is simply visible and the
game is fully playable.
