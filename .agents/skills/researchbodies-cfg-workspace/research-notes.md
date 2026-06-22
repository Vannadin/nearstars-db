# ResearchBodies — source-cited schema inventory

Repo: `researchbodies-repo/` (JPLRepo/ResearchBodies, v1.13.0.0).

## TL;DR for NearStars cfg authoring

- **One top-level node: `RESEARCHBODIES`.** `ONDISCOVERY`, `IGNORELEVELS`,
  (legacy) `IGNORE` are SUBnodes of it.
- **Third-party packs ship `RESEARCHBODIES { loadAs = mod ... }`.**
  `loadAs = mod` is MANDATORY — a mod node without it has its
  discovery/ignore data silently ignored (only observatory-range
  overrides are read). (`Database.cs:286-289`, `Database.cs:403-406`)
- `ONDISCOVERY { <bodyName> = <message> }` — matched by `Contains`
  (substring!) against `CelestialBody.bodyName`; value = discovery
  screen message. Use EXACT internal body names. (`Database.cs:244,297`;
  field `CelestialBodyInfo.cs:25`)
- `IGNORELEVELS { <bodyName> = <e n m h> }` — exact `==` match; value =
  exactly 4 space-separated booleans `true`/`false` in order
  Easy Normal Medium Hard. `true` = visible at game start for that
  difficulty; `false` = hidden (must discover via telescope/observatory).
  `1`/`0` are INVALID (bool.Parse throws); fewer than 4 throws.
  (`Database.cs:251-259,334-338`; `BodyIgnoreData.cs:19-20,36-55`)
- **Default with no IGNORELEVELS entry = hidden at every difficulty**
  (`IgnoreData(false,false,false,false)`, `CelestialBodyInfo.cs:40`).
  Silence = hidden. No ONDISCOVERY entry → generic "Now tracking <body> !"
  (`CelestialBodyInfo.cs:39`).
- Body name = internal Kopernicus `bodyName` / `GetName()`, NOT
  `displayName`. Case-sensitive. (`Database.cs:244,255`)
- **Barycenters auto-handled**: bodies with `Radius < 100` m are detected
  as Kopernicus barycenters and dropped from the discovered-list UI
  (`Database.cs:91,164-173`). DO NOT author discovery data for them.
- Difficulty enum `Level { Easy=0, Normal=1, Medium=2, Hard=3 }`
  (`RBEnums.cs:17-23`); stock "Moderate" preset → Medium
  (`SettingsParms.cs:64-93`).

## Global-only knobs (in `RESEARCHBODIES`, NOT per-body)

`chances` (int, discovery-odds seed 1-6), `enableInSandbox`,
`allowTrackingStationLvl1`, `observatorylvl1range`/`observatorylvl2range`
(float m), `allowOldResearchinCareer`, `discoveryByFlyby` (int),
`ResearchPlanPercentage` (float), `StartResearchCosts`/
`ProgressResearchCosts`/`ScienceRewards` (each int[4] per-difficulty
`easy normal medium hard`). (`Database.cs:212-236`) Per-body granularity
ceiling = ONDISCOVERY + IGNORELEVELS only.

## Shipped master example (`database.cfg:1-55`)

```
RESEARCHBODIES
{
    chances = 3
    enableInSandbox = true
    allowTrackingStationLvl1 = false
    observatorylvl1range = 80000000000
    observatorylvl2range = 184000000000
    discoveryByFlyby = 30
    allowOldResearchinCareer = false
    StartResearchCosts = 20 25 35 45
    ProgressResearchCosts = 5 10 15 20
    ScienceRewards = 10 15 25 50
    ResearchPlanPercentage = 10
    ONDISCOVERY {
        Moho = So hot. This is one of the first things...
        Eeloo = So far, so cold, so white, so tiny...
    }
    IGNORELEVELS {
        // body = easy normal medium hard
        Sun = true true true true
        Kerbin = true true true true
        Minmus = true true true false
        Duna = true true false false
        Laythe = true false false false
    }
}
```

## Kopernicus / MM

- Modded bodies auto-enrolled (RB iterates all FlightGlobals.Bodies,
  `Database.cs:148-176`). RB's own Kopernicus patch is
  `:FOR[ResearchBodies]:NEEDS[Kopernicus]` and bumps telescope range +
  `@observatorylvl1range`/`@observatorylvl2range` (`ResearchBodiesMMKopernicus.cfg`).
- For NearStars: ship a `RESEARCHBODIES { loadAs = mod ... }` node guarded
  `:NEEDS[ResearchBodies&Kopernicus]`. To override RB defaults, patch
  `:AFTER[ResearchBodies]` (RB ships no :FINAL/:AFTER itself).

## License nuance (IMPORTANT)

Per-file headers declare MIT (simon56modder code), but GitHub `README.md:5`
adds other parts are "ALL RIGHTS RESERVED", no fork/redistribute without
permission. → We do NOT copy RB code or wholesale cfg. We author our OWN
`RESEARCHBODIES { loadAs = mod }` patch + a schema reference that CITES
source lines (same fair-use posture as the GPL-3.0 firefly skill). Quote
only minimal schema-illustrating snippets.

## Pitfalls (author-facing)

- ONDISCOVERY substring match vs IGNORELEVELS exact match — use exact
  names to avoid `Kerbin`⊂`Kerbinish` style mis-hits.
- IGNORELEVELS: exactly 4 `true`/`false`, else throws. No `1`/`0`.
- Cost/reward arrays: exactly 4 ints each, else throws.
- `NOTHING` node is a dead reference — don't author (`Database.cs:268-271`).
- Master `IGNORE` block is inert; `IGNORE` only honored in `loadAs=mod`
  nodes and is legacy pre-1.5 — prefer IGNORELEVELS.
- `loadAs = mod` mandatory or the whole node's discovery data is dropped.
