# `ATMOFX_PARTICLES` — particle system definitions

Defines the particle systems (sparks, debris, smoke) used during
reentry. Loaded by `ConfigManager.LoadParticleConfigs`
(`ConfigManager.cs:404`). The mod ships exactly one node named
`FireflyParticles_Default` and uses it for all bodies.

## Skeleton

```
ATMOFX_PARTICLES
{
	name = <set_name>

	Sparks
	{
		prefab = SparksParticles
		main_texture = Firefly/Assets/Textures/ChunkSprite
		emission_texture = Firefly/Assets/Textures/ChunkSprite
		is_active = True
		offset = 0.5
		use_half_offset = False
		rate = 46 46
		lifetime = 0.07 0.7
		velocity = 30 70
	}

	Debris { … }
	AlternateDebris { … }
	Smoke { … }
}
```

## Top-level keys

| Key | Type | Notes |
|---|---|---|
| `name` | string | Set name. The mod's default loader expects `FireflyParticles_Default` (`ConfigManager.cs:192`). Custom sets can use other names but the GUI / runtime currently doesn't switch between sets — having one is the practical mode. |

Each sub-node inside `ATMOFX_PARTICLES` defines one particle system.
The sub-node's name is the system label; the loader stores it in
`particleConfigs[name]` (`ConfigManager.cs:563`). Stock sub-node names:
`Sparks`, `Debris`, `AlternateDebris`, `Smoke`.

## Per-system keys

Required:

| Key | Type | Notes |
|---|---|---|
| `prefab` | string | Unity prefab name in the Firefly asset bundle. Stock: `SparksParticles`, `DebrisParticles`, `AlternateDebrisParticles`, `SmokeParticles`. Mismatched prefab → silent zero-effect. |
| `main_texture` | string | KSP asset path (e.g., `Firefly/Assets/Textures/ChunkSprite` — no extension). |
| `emission_texture` | string | Same format. Value `"unused"` or `""` → no emission texture (`ConfigManager.cs:581`). |

Optional (defaults from `ConfigManager.cs:149-154`):

| Key | Type | Default | Notes |
|---|---|---|---|
| `is_active` | bool | `True` | Toggle the system off without removing it. |
| `offset` | float | `0` | Distance from the vessel surface where particles spawn. |
| `use_half_offset` | bool | `False` | Halves the spawn offset (used by Smoke for closer-to-hull positioning). |
| `rate` | FloatPair `min max` | `0 0` | Particles per second range. The system picks a random value each tick. |
| `lifetime` | FloatPair `min max` | `0 0` | Per-particle lifetime in seconds. |
| `velocity` | FloatPair `min max` | `0 0` | Per-particle initial velocity in m/s. |

`FloatPair` parsing requires exactly two space-separated floats
(`Utils.cs:190`). One number → parse fails; the entire particle config
is rejected.

## Shipped values for reference

| System | rate | lifetime | velocity | offset | half? |
|---|---|---|---|---|---|
| Sparks | 46 46 | 0.07 0.7 | 30 70 | 0.5 | No |
| Debris | 20 20 | 0.25 1.23 | 30 70 | 1.24 | No |
| AlternateDebris | 0.1 2 | 0.3 1 | 15 20 | 1.62 | No |
| Smoke | 206 255 | 8 10 | 400 400 | 2 | Yes |

Smoke is the heavy lifter — 200+ particles/sec, 8-10 second lifetime,
high velocity, placed farthest from the hull.

## Phase 3 relevance

Phase 3 does **not** drive `ATMOFX_PARTICLES`. The mod's single default
set covers all bodies. There is no per-body particle override mechanism
in the loader.

If a NearStars-wide aesthetic shift is wanted (e.g., quieter particle
effects across the whole star system), edit `FireflyParticles.cfg` in
place rather than shipping a system-specific particle cfg.

## Where the particle textures and prefabs live

- Textures: `GameData/Firefly/Assets/Textures/<Name>.png` —
  `ChunkSprite`, `ChunkSprite1`, `SmokeSprite`, `SparkSprite`, `Icon`.
- Prefabs: bundled inside `GameData/Firefly/Assets/fireflybundle.ksp`
  (Unity AssetBundle). Adding new prefab names requires rebuilding
  the bundle in the Firefly Unity project (`Unity/` in the repo).

Custom textures shipped by NearStars can be referenced by full path
(`NearStarsSystem/Assets/Textures/MyDust`) but the prefabs must remain
the stock 4.

## Validation checklist

- [ ] `name` is unique across all loaded particle configs.
- [ ] Each sub-node has `prefab`, `main_texture`, `emission_texture`.
- [ ] `rate`, `lifetime`, `velocity` each have exactly 2 floats.
- [ ] Texture paths exist in GameData and resolve from the Firefly
      asset root.
- [ ] Prefab name matches one of the four shipped prefabs (unless a
      custom asset bundle is also shipped).

## Source citations

- Loader: `ConfigManager.cs:404-420`
- Per-system parser: `ConfigManager.cs:537-590`
- Texture queueing: `ConfigManager.cs:560-561`
- Default node name constant: `ConfigManager.cs:192`

## See also

- [[atmofx-body]] — particle activation is gated by the body's
  `particle_threshold` speed.
- [[pitfalls]] — FloatPair parse failures are the common error.
