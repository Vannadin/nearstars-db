# `ATMOFX_PLANET_PACK` — pack-level wrapper

A planet pack uses this node to declare which bodies it ships configs
for and to apply pack-wide multipliers on top of each body's
`strength_multiplier`. Loaded by `ConfigManager.LoadPlanetPackConfigs`
(`ConfigManager.cs:240`).

## Skeleton

```
ATMOFX_PLANET_PACK:NEEDS[<PackMod>]
{
	name = <PackName>

	strength_multiplier = 1
	transition_offset = 0.2

	affected_bodies = Body1, Body2, Body3
}
```

## Required keys

| Key | Type | Notes |
|---|---|---|
| `name` | string | Internal label for logging. No semantic effect on rendering. |
| `strength_multiplier` | float | Multiplied into each affected body's `strength_multiplier` post-load (`ConfigManager.cs:523`). Typical: 1.0. |
| `transition_offset` | float (0–1) | Strength offset applied at runtime via the FxState system — controls how aggressively effects fade in/out as the vessel transitions through speed regimes. Higher = effects engage sooner. Typical: 0.2. |
| `affected_bodies` | comma-separated string list | Each entry is trimmed of whitespace. Empty list → pack is rejected. |

## Module Manager directives

The node line typically carries `:NEEDS[<PackMod>]` so the pack-level
multipliers only activate when the planet pack itself is installed.
Example from shipped `Configs/RSS.cfg:1`:

```
ATMOFX_PLANET_PACK:NEEDS[RealSolarSystem|SolSystem]
```

Pipe `|` = OR. Bracket can list multiple mod folder names that should
all enable the pack.

For NearStars: `:NEEDS[NearStarsSystem]` is the canonical pattern,
matching the directory name `GameData/NearStarsSystem/`.

## Interaction with `ATMOFX_BODY`

The pack does **not** create body configs — each body still needs its
own `ATMOFX_BODY` node. The pack only *modifies* existing bodies.

Sequence (`ConfigManager.cs:231-238`):

1. `LoadPlanetPackConfigs` — packs registered first.
2. `LoadPlanetConfigs` — for each body, `strength_multiplier` is
   multiplied by the first matching pack's multiplier.
3. The pack reference is stored on the body for runtime `FxState` use.

Only the first pack that lists the body is applied — duplicates are
silently ignored.

## Single-system pattern for NearStars

NearStars ships exactly one pack node covering every star system body
that has an `ATMOFX_BODY`. Example:

```
ATMOFX_PLANET_PACK:NEEDS[NearStarsSystem]
{
	name = NearStars

	strength_multiplier = 1
	transition_offset = 0.2

	affected_bodies = ProximaCentauriB, AlphaCentauriBb, Trappist1b, Trappist1c, ...
}
```

Keep `strength_multiplier = 1` by default and only adjust if a
system-wide tone shift is wanted (e.g., dialing down all entry effects
for stylized presentation). Use per-body `strength_multiplier` for
body-specific tuning.

## Validation checklist

- [ ] `:NEEDS[<PackMod>]` directive present (otherwise pack applies
      even when the planet pack is uninstalled — usually a bug).
- [ ] `affected_bodies` list is non-empty.
- [ ] Every name in `affected_bodies` matches an `ATMOFX_BODY` config
      that ships in the same pack.
- [ ] `strength_multiplier` is positive (negative or 0 zeroes out all
      affected bodies).
- [ ] `transition_offset` is in 0–1.

## Source citations

- Loader: `Source/Firefly/ConfigManager.cs:240-288`
- Field parser: `ConfigManager.cs:422-465`
- Apply step: `ConfigManager.cs:517-525`

## See also

- [[atmofx-body]] — per-body config.
- [[pitfalls]] — load-order pitfalls (packs must be visible when bodies
  load — guaranteed by MM postload ordering).
