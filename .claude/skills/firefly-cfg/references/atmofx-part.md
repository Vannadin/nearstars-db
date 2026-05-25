# `ATMOFX_PART` — per-part color override

Per-part color override for vessel components. Used to tint specific
parts differently from their host body's atmofx colors (e.g., a
heatshield that always glows green regardless of which body it's
entering). Loaded by `ConfigManager.LoadPartConfigs`
(`ConfigManager.cs:377`).

## Skeleton

```
ATMOFX_PART
{
	name = <part_cfg_name>

	Color
	{
		glow         = null
		trail_streak = 91 191 74 3
		wrap_streak  = 91 191 74 3
	}
}
```

## Required keys

| Key | Type | Notes |
|---|---|---|
| `name` | string | Part cfg name with dots replaced by underscores (see `Utils.GetPartCfgName:268`). Match the part's `part.partInfo.name`. |
| `Color { … }` | subnode | Same 9 keys as [[atmofx-body]] Color subnode, but **all keys are optional**. |

## Color subnode — partial override semantics

Unlike `ATMOFX_BODY`, `ATMOFX_PART` allows partial color specification.
Per `ConfigManager.cs:651-666`:

| Color value | Result |
|---|---|
| Valid `R G B intensity` | Use this color for this part |
| `null` (case-insensitive) | Use the body's color for this key |
| `default` (case-insensitive) | Use the body's color for this key |
| Key omitted entirely | Use the body's color for this key |

So `ATMOFX_PART` is *additive overrides on top of the body color*, not
a full replacement.

The shipped example (`Patches/Bluedog_DB/Apollo/bluedog_Apollo_Heatshield.cfg`)
overrides only `trail_streak` and `wrap_streak`, leaving everything
else at body default.

## Phase 3 relevance

NearStars Phase 3 produces **body**-level data, not part-level data.
`ATMOFX_PART` is only useful if a NearStars body ships a custom KSP
part (e.g., a system-specific lander), which is out of Phase 3 scope.

The mod itself ships part overrides for stock and popular part mods
(Bluedog DB, Benjee10 Shuttle, Space Shuttle System). NearStars
typically does not need to write any `ATMOFX_PART` nodes.

If a NearStars-specific part needs a unique entry color (e.g., a
ceremonial probe with a green plasma signature), a hand-written
`ATMOFX_PART` is the right tool, with the override only on
`trail_streak` + `wrap_streak`.

## Module Manager pattern

Part overrides usually live in `GameData/Firefly/Patches/<Mod>/<Part>.cfg`,
one node per part. The node itself is plain (no `:NEEDS` typically),
but the file is conventionally placed inside a mod-named subfolder so
manual install is straightforward.

If a NearStars part lives in NearStarsSystem/Parts/, the override can
ship in NearStarsSystem/Patches/firefly/<Part>.cfg with `:NEEDS[Firefly]`
on the node line so it only loads when Firefly is installed.

## Validation checklist

- [ ] `name` matches the part's KSP cfg `name = …` field (dots → `_`).
- [ ] `Color { … }` subnode present (even if empty content).
- [ ] Each defined color is either a valid HDR string, `null`, or
      `default`.
- [ ] No multiplier fields (those are body-only and would be silently
      ignored, but it's cleaner to omit them).

## Source citations

- Loader: `Source/Firefly/ConfigManager.cs:373-402`
- Parser: `ConfigManager.cs:530-535` (delegates to `ProcessBodyColors`
  with `partConfig=true`)
- Name munging: `Source/Firefly/Utils.cs:268`
- Color null/default semantics: `ConfigManager.cs:651-666`

## See also

- [[color-format]] — HDR color string syntax.
- [[atmofx-body]] — body-level config that supplies the defaults.
- [[pitfalls]] — common part-override mistakes.
