# `RESEARCHBODIES` node + global settings

`RESEARCHBODIES` is the **only top-level node** ResearchBodies reads.
`ONDISCOVERY`, `IGNORELEVELS` (and legacy `IGNORE`) are subnodes of it.

## Two ways RB consumes config (source-cited, v1.13.0.0)

1. **Master file** `GameData/REPOSoftTech/ResearchBodies/database.cfg`,
   loaded by absolute path — `ConfigNode.Load` then
   `GetNode("RESEARCHBODIES")` (`Database.cs:210-212`). This holds the
   stock globals + stock Kerbol-system ONDISCOVERY/IGNORELEVELS.
2. **Mod nodes** scanned across the whole GameDatabase —
   `GameDatabase.Instance.GetConfigNodes("RESEARCHBODIES")`
   (`Database.cs:286`). **This is how a third-party pack hooks in.**

### `loadAs = mod` is MANDATORY for a pack

A `RESEARCHBODIES` mod node is only processed for discovery/ignore data
if it declares `loadAs = mod` (`Database.cs:289`). A node **without**
`loadAs` is re-read only for observatory-range overrides
(`Database.cs:403-406`) — its `ONDISCOVERY`/`IGNORELEVELS` are silently
ignored. **Always include `loadAs = mod` in the NearStars patch.**

## NearStars patch skeleton

```
RESEARCHBODIES:NEEDS[ResearchBodies&Kopernicus]
{
    loadAs = mod
    name = NearStars            // free-text label for the mod node

    ONDISCOVERY  { ... }         // see ondiscovery.md
    IGNORELEVELS { ... }         // see ignorelevels.md
}
```

- Guard with `:NEEDS[ResearchBodies&Kopernicus]` — discoverability is an
  optional layer; uninstalled RB → NearStars is fully visible/normal.
- To override RB's own defaults, patch `:AFTER[ResearchBodies]` (RB ships
  its patches `:FOR[ResearchBodies]` and no `:FINAL`/`:AFTER`).

## Global knobs (NOT per-body — granularity ceiling)

All of these live on the `RESEARCHBODIES` node and are global or indexed
by difficulty, never by body (`Database.cs:212-236`):

| Key | Type | Meaning |
|---|---|---|
| `chances` | int 1–6 | discovery-odds seed; higher = rarer finds |
| `enableInSandbox` | bool | RB active in sandbox |
| `allowTrackingStationLvl1` | bool | observatory usable at T/S level 1 |
| `observatorylvl1range` / `observatorylvl2range` | float (m) | telescope ranges |
| `allowOldResearchinCareer` | bool | |
| `discoveryByFlyby` | int | researchState granted on flyby |
| `ResearchPlanPercentage` | float | |
| `StartResearchCosts` | int[4] | per-difficulty (easy normal medium hard) |
| `ProgressResearchCosts` | int[4] | per-difficulty |
| `ScienceRewards` | int[4] | per-difficulty |

Cost/reward arrays must each be **exactly 4 ints** or `int.Parse` throws
(`Database.cs:228,232,236`).

**NearStars decision:** leave the globals to RB's defaults / the player's
difficulty settings. NearStars only authors per-body `ONDISCOVERY` +
`IGNORELEVELS`. If a future need arises (e.g. telescope range too short
for ~50 ly distances — note RB already bumps range under Kopernicus via
`ResearchBodiesMMKopernicus.cfg`), document it before touching globals.
