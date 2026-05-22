# Firefly cfg — Research notes

Ground-truth schema extracted from `firefly-repo/` (Firefly @ master,
GPL-3.0, M1rageDev/Firefly). Every claim cites source file + line.

## 1. Top-level cfg nodes registered by the loader

| Node | Loaded by | Source | Purpose |
|---|---|---|---|
| `ATMOFX_BODY` | `ConfigManager.LoadPlanetConfigs` | `ConfigManager.cs:294` | Per-celestial-body atmofx config |
| `ATMOFX_PLANET_PACK` | `ConfigManager.LoadPlanetPackConfigs` | `ConfigManager.cs:245` | Wrapper that multiplies `strength_multiplier` across a list of bodies |
| `ATMOFX_PART` | `ConfigManager.LoadPartConfigs` | `ConfigManager.cs:377` | Per-part color override (`BodyColors` only, no multipliers) |
| `ATMOFX_PARTICLES` | `ConfigManager.LoadParticleConfigs` | `ConfigManager.cs:409` | Particle system definitions (Sparks / Debris / etc.) |
| `ATMOFX_SETTINGS` | `SettingsManager.LoadModSettings` | `SettingsManager.cs:147` | Global mod toggles (HDR, disable bowshock, etc.) |

## 2. ATMOFX_BODY schema (authoritative)

Required:
- `name` (string) — celestial body name. Duplicate → silent skip (`ConfigManager.cs:478`).
- `config_version` (int) — must equal `5`. Missing → assumed `4` → wrong-version error.
- `Color { … }` subnode — required for body configs; every leaf required (see §3).

Optional floats (defaults in `ConfigManager.cs:76-84`):

| Key | Default | Units / range | Notes |
|---|---|---|---|
| `strength_multiplier` | 1.0 | multiplier | Multiplied post-load by matching `ATMOFX_PLANET_PACK` (`ConfigManager.cs:523`) |
| `length_multiplier` | 1.0 | multiplier | |
| `opacity_multiplier` | 1.0 | multiplier | |
| `glow_multiplier` | 1.0 | multiplier | |
| `wrap_opacity_multiplier` | 1.0 | multiplier | |
| `wrap_fresnel_modifier` | 1.0 (code) / 0 (shipped Default/Kerbin/Duna) | modifier | **Discrepancy: code default 1f, shipped configs split between 0 and 1.** Treat 0 (thin atmo, no rim) vs 1 (full rim, thick atmo) as the intended convention. |
| `particle_threshold` | 1800 | m/s | Speed above which particle systems activate. Shipped range: 1350 (Duna) – 1800 (Kerbin/Jool/Default). |
| `streak_probability` | 0.0 | 0–1 | Probability streak appears per frame |
| `streak_threshold` | 0.0 | float | Source comment claims "0-1 range, 1 = 4000 m/s, default 0.5" but actual code default is 0 and shipped configs use **negative** values (Eve -0.2, Duna -0.5). Treat as: lower = streaks start sooner. |

## 3. Color subnode schema

`Color { … }` keys (`ConfigManager.cs:22-33`, all required for body, all
optional for part):

- `glow`, `glow_hot`
- `trail_primary`, `trail_secondary`, `trail_tertiary`, `trail_streak`
- `wrap_layer`, `wrap_streak`
- `shockwave`

**HDR color value format** (`Utils.cs:EvaluateColorHDR:235`):

`R G B intensity` — four floats, space-separated.

- `R G B`: 0–255 (divided by 255 internally, line 254-257).
- `intensity`: float exponent; final HDR color = `(R/255, G/255, B/255) × 2^intensity`.
- Fewer than 4 tokens → parse fails.
- Strings `"null"` or `"default"` (case-insensitive) → falls back to default:
  - In `ATMOFX_PART`: allowed, uses body default.
  - In `ATMOFX_BODY`: counts as error (`ConfigManager.cs:661-666`).

Shipped color examples (intensity range 1.0 – 3.0 observed, no upper cap
enforced by parser):

| Body | glow | trail_primary | shockwave |
|---|---|---|---|
| Default / Kerbin | 191 80 50 1.4 | 191 99 72 3 | 74 90 191 3 |
| Duna | 191 80 50 1.4 | 76 116 191 2.5 | 34 41 191 3 |
| Eve | 191 80 50 1.4 | 83 92 191 2 | 96 191 159 3 |
| Jool | 191 80 50 1.4 | 32 20 191 1.4 | 140 191 161 1 |

Observation: `glow` and `glow_hot` are identical across all shipped
stock configs. Variation is concentrated in trail/wrap/shockwave.

## 4. ATMOFX_PLANET_PACK schema

`ConfigManager.cs:422-465` (`ProcessPlanetPackNode`).

Required:
- `name` (string) — internal label, no semantic effect.
- `strength_multiplier` (float).
- `transition_offset` (float, 0–1; comment line 124).
- `affected_bodies` (comma-separated string list, trimmed, must be ≥1).

Module Manager directives observed: `:NEEDS[RealSolarSystem|SolSystem]`
on the node line (`Configs/RSS.cfg:1`).

Behavior: matches against body names; for each match, multiplies the
body's `strength_multiplier` (line 523). `transition_offset` stored on
the body but not visibly used during cfg load — applied at runtime by
the FxState system per source comment.

## 5. ATMOFX_PART schema

`ConfigManager.cs:530` (`ProcessPartConfigNode` → `ProcessBodyColors`
with `partConfig=true`).

Required:
- `name` (string) — part cfg name (dots replaced with underscores, see
  `Utils.GetPartCfgName:268`).
- `Color { … }` subnode — see §3. Individual keys optional; missing key
  or `"null"`/`"default"` falls back to body color.

No multiplier fields. Pure color override.

## 6. ATMOFX_PARTICLES schema

`ConfigManager.cs:537` (`ProcessParticleConfigNode`). Each sub-node name
is the particle system name; per-node fields from `ProcessSingleParticleDef`:

Required:
- `prefab` (string) — Unity prefab name. Shipped prefabs:
  `SparksParticles`, `DebrisParticles`, `AlternateDebrisParticles`,
  `SmokeParticles` (`FireflyParticles.cfg`).
- `main_texture` (string) — texture path (e.g.,
  `Firefly/Assets/Textures/ChunkSprite`).
- `emission_texture` (string) — texture path or `"unused"` / `""` for
  none (`ConfigManager.cs:581`).

Optional (defaults `ConfigManager.cs:149-154`):
- `is_active` (bool, default `true`).
- `offset` (float, default 0).
- `use_half_offset` (bool, default false).
- `rate` (FloatPair `min max`, default `0 0`).
- `lifetime` (FloatPair `min max`, default `0 0`).
- `velocity` (FloatPair `min max`, default `0 0`).

Shipped default node name: `FireflyParticles_Default`
(`ConfigManager.cs:192`). The mod ships one global particle config.
Phase 3 typically does **not** need to override particle configs — these
are mod-internal effects.

## 7. ATMOFX_SETTINGS schema

`SettingsManager.cs:27-31`. Loaded from `GameData/Firefly/ModSettings.cfg`.

- `hdr_override` (bool, default `true`).
- `disable_bowshock` (bool, default `false`).
- `disable_particles` (bool, default `false`, `needsReload=true`).
- `strength_base` (float, default `2800`).
- `length_mult` (float, default `1`).

User-facing global setting. Phase 3 does **not** write this — it's a
player preference.

## 8. Parser primitives

| Type | Function | Source | Format |
|---|---|---|---|
| Float | `EvaluateFloat` | `Utils.cs:175` | `float.TryParse` |
| Int | `EvaluateInt` | `Utils.cs:180` | `int.TryParse` |
| Bool | `EvaluateBool` | `Utils.cs:185` | `bool.TryParse` on `.ToLower()` |
| FloatPair | `EvaluateFloatPair` | `Utils.cs:190` | Two floats separated by space |
| Float3 | `EvaluateFloat3` | `Utils.cs:205` | Three floats separated by space |
| HDR Color | `EvaluateColorHDR` | `Utils.cs:235` | `R G B intensity`, 0–255 + float |

## 9. File-system conventions

- `GameData/Firefly/Configs/<PlanetPack>/<Body>.cfg` — one `ATMOFX_BODY`
  per file (observed pattern, not enforced).
- `GameData/Firefly/Configs/<PlanetPack>.cfg` — `ATMOFX_PLANET_PACK`
  wrapper at the pack level.
- `GameData/Firefly/Patches/<Mod>/<Part>.cfg` — `ATMOFX_PART` overrides.
- `GameData/Firefly/Configs/Saved/` — user-saved configs from the
  in-game editor (`ConfigManager.cs:189`).

## 10. Error handling

`ErrorManager.cs` registers errors that display in the Error Manager
window. Causes (`ConfigManager.cs` usage):
- `BadConfig` — parse failure, missing required field.
- `ConfigVersionMismatch` — `config_version` ≠ 5.
- `IncorrectInstall` — Default body config missing (fatal).

The mod does NOT crash on bad cfg — it logs, falls back to Default for
missing bodies, and surfaces errors in the GUI.

## 11. Templates/ directory

`GameData/Firefly/Templates/Aluminum.txt`, `BoronHeatshield.txt` — `.txt`
not `.cfg`, not consumed by the cfg loader. Likely material templates
referenced by the Unity asset side (`ReentryColors/Reentry Aluminum.asset`
exists). Out of scope for cfg authoring.

## 12. Unity-side reentry color assets

`Unity/Assets/ReentryColors/Reentry <body>.asset` — these are Unity
ScriptableObjects bundled into `fireflybundle.ksp`, not cfg-editable.
The cfg `Color { … }` block is the only color authoring surface
available to cfg writers.

## 13. CI validator

`.github/workflows/validate-cfg-files.yml:16` delegates to
`KSPModdingLibs/KSPBuildTools/.github/workflows/validate.yml@1.1.1` —
generic KSP cfg syntax check (brace matching), **not Firefly-schema-aware**.
Our skill should do its own schema validation post-emit.
