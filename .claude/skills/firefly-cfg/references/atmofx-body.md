# `ATMOFX_BODY` — per-body atmospheric effects

The primary node for cfg writers. One per celestial body in the system.
Loaded by `ConfigManager.LoadPlanetConfigs` (`ConfigManager.cs:294`).

## Skeleton

```
ATMOFX_BODY
{
	name = <BodyName>
	config_version = 5

	strength_multiplier = 1
	length_multiplier = 1
	opacity_multiplier = 1
	glow_multiplier = 1
	wrap_opacity_multiplier = 1
	wrap_fresnel_modifier = 0

	particle_threshold = 1800
	streak_probability = 0
	streak_threshold = 0

	Color
	{
		glow            = 191 80 50 1.4
		glow_hot        = 191 90 65 2.5
		trail_primary   = 191 99 72 3
		trail_secondary = 191 70 42 1.5
		trail_tertiary  = 74 80 191 2
		trail_streak    = 74 80 191 2
		wrap_layer      = 69 69 191 2
		wrap_streak     = 191 99 72 3
		shockwave       = 74 90 191 3
	}
}
```

## Required top-level keys

| Key | Type | Notes |
|---|---|---|
| `name` | string | Celestial body name. Must match the body's `Kopernicus` `name = …` exactly. Duplicate body names → silent skip of the second one. |
| `config_version` | int | Must equal `5`. Anything else (or omission) → "wrong version" error in the Error Manager window. |
| `Color { … }` | subnode | All 9 keys required — see [[color-format]]. |

## Optional multiplier keys

All floats. Defaults from `ConfigManager.cs:76-84`. If omitted, the
default is used silently.

| Key | Default | Effect when increased | Effect when decreased |
|---|---|---|---|
| `strength_multiplier` | 1.0 | More intense entry effect overall | Fainter, can suppress entry |
| `length_multiplier` | 1.0 | Longer plasma trail | Shorter trail |
| `opacity_multiplier` | 1.0 | More opaque plasma | More translucent |
| `glow_multiplier` | 1.0 | Brighter hull glow | Dimmer glow |
| `wrap_opacity_multiplier` | 1.0 | More opaque wrap layer | Wrap fades faster |
| `wrap_fresnel_modifier` | 1.0 (code) / 0 in some shipped cfgs | Strong rim-light look (thick atmo feel) | Flat wrap, no rim |

**Note on `wrap_fresnel_modifier`:** the C# default is `1.0` but shipped
`Default.cfg`, `Kerbin.cfg`, `Duna.cfg` ship `wrap_fresnel_modifier = 0`,
while `Eve.cfg` and `Jool.cfg` ship `1`. Treat 0 as "thin or no rim"
and 1 as "full rim glow"; pick based on atmosphere thickness.

## Particle / streak keys

| Key | Default | Units | Effect |
|---|---|---|---|
| `particle_threshold` | 1800 | m/s | Speed above which particle systems (sparks, debris) activate. Lower → particles start sooner. Shipped: 1350 (Duna, thin), 1500 (Eve), 1800 (Kerbin/Jool). |
| `streak_probability` | 0.0 | 0–1 | Probability of a streak appearing per frame. 0 = no streaks, 0.07 = ~once per ~14 frames (shipped Duna/Eve/Jool). |
| `streak_threshold` | 0.0 | float | Speed gate for streaks. Source comment claims 0–1 with 1 = 4000 m/s, but shipped configs use **negative** values (Eve −0.2, Duna −0.5). Negative = streaks visible at lower speeds. Tune empirically. |

## Color subnode

See [[color-format]] for the full HDR color value format. All 9 keys
required:

```
Color
{
	glow            = R G B intensity
	glow_hot        = R G B intensity
	trail_primary   = R G B intensity
	trail_secondary = R G B intensity
	trail_tertiary  = R G B intensity
	trail_streak    = R G B intensity
	wrap_layer      = R G B intensity
	wrap_streak     = R G B intensity
	shockwave       = R G B intensity
}
```

If any color is missing or set to `"null"`/`"default"`, the entire body
config is rejected (logged as `BadConfig`).

## Special body name: `Default`

A body named `Default` is loaded as the fallback for any celestial
body that has no `ATMOFX_BODY` of its own. The mod refuses to start
if `Default` is missing (`ConfigManager.cs:351-367`).

NearStars-shipped configs should NOT define a body named `Default` —
the mod's own `GameData/Firefly/Configs/Default.cfg` provides it.

## Interaction with `ATMOFX_PLANET_PACK`

After body configs load, the loader walks all `ATMOFX_PLANET_PACK`
nodes. For each pack whose `affected_bodies` list contains this body's
`name`, the pack's `strength_multiplier` multiplies into this body's
`strength_multiplier` (`ConfigManager.cs:520-525`). A body cannot be
affected by more than one pack at a time — the last one wins.

See [[atmofx-planet-pack]] for the pack node.

## Validation checklist for cfg writers

Before saving a body config, verify:

- [ ] `name` matches a Kopernicus body (exact case).
- [ ] `config_version = 5`.
- [ ] All 9 `Color` keys present and parse as `R G B intensity`.
- [ ] `R G B` values are 0–255 (not 0–1).
- [ ] `intensity` is a small float (1–3 typical).
- [ ] Multiplier values are positive floats.
- [ ] `streak_threshold` and `streak_probability` make sense as a pair
      (probability 0 makes threshold irrelevant).

## Source citations

- Loader: `Source/Firefly/ConfigManager.cs:290-371`
- Field defaults: `ConfigManager.cs:74-85`
- Color subnode parser: `ConfigManager.cs:607-672`
- Pack interaction: `ConfigManager.cs:517-525`

## See also

- [[color-format]] — HDR color details.
- [[atmofx-planet-pack]] — pack-level wrapper.
- [[phase3-mapping]] — which Phase 3 row feeds which field.
- [[pitfalls]] — common mistakes.
