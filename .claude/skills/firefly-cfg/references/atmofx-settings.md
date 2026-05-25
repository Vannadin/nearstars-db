# `ATMOFX_SETTINGS` — global mod settings

Player-facing global toggles. Lives in
`GameData/Firefly/ModSettings.cfg`. Loaded by
`SettingsManager.LoadModSettings` (`SettingsManager.cs:144`). One node
per save; settings are persisted by the in-game GUI, not authored by
cfg writers.

## Skeleton

```
ATMOFX_SETTINGS
{
	hdr_override = True
	disable_bowshock = False
	disable_particles = False
	strength_base = 2800
	length_mult = 1
}
```

## Keys

| Key | Type | Default | Notes |
|---|---|---|---|
| `hdr_override` | bool | `True` | Force HDR rendering on the FX camera even if the user's scene cameras are LDR. Required for HDR colors (`intensity > 1`) to actually visibly boost. |
| `disable_bowshock` | bool | `False` | Hides the bow shock layer. Performance toggle for low-end systems. |
| `disable_particles` | bool | `False` | Hides all particle systems. Marked `needsReload=true` in source — change requires scene reload. |
| `strength_base` | float | `2800` | Global strength reference value. The final reentry strength scales relative to this. Lower → effects appear at higher altitudes; higher → effects only at extreme heat. |
| `length_mult` | float | `1` | Global multiplier applied on top of per-body `length_multiplier`. User-side trail-length scaling. |

## Phase 3 relevance

Phase 3 does **not** write this file. It is user / player preference:

- HDR toggle depends on the player's graphics settings.
- `disable_bowshock` / `disable_particles` are performance toggles.
- `strength_base` / `length_mult` are global scaling preferences.

NearStars should ship `ModSettings.cfg` only if the existing default is
inadequate — and it almost never is. The mod creates the file on first
launch with default values if it doesn't exist.

## NearStars exception: ensuring HDR works

If a NearStars system relies on `intensity > 2` HDR colors (very bright
plasma trails for a hot exoplanet), confirm `hdr_override = True`.
Don't ship a `ModSettings.cfg` that flips it off — let the user keep
their default.

## Validation checklist

- [ ] File path is exactly `GameData/Firefly/ModSettings.cfg` (Firefly
      writes there with that hardcoded path —
      `SettingsManager.cs:110`).
- [ ] Exactly one `ATMOFX_SETTINGS` node at top level. Multiple nodes
      → only the first is loaded (`SettingsManager.cs:157`).
- [ ] All values parse as their declared types.

## What happens if the file is missing or malformed

`SettingsManager.LoadModSettings:147-176`:

- Missing file → uses defaults silently.
- Malformed file → `isFormatted = false` → reverts to defaults +
  logs "Settings cfg formatted incorrectly".

The mod never refuses to start because of `ATMOFX_SETTINGS`.

## Source citations

- Loader: `Source/Firefly/SettingsManager.cs:144-176`
- Field defaults: `SettingsManager.cs:21-36`
- Persistence path: `SettingsManager.cs:110`
- Save method: `SettingsManager.cs:124-139`

## See also

- [[atmofx-body]] — per-body `length_multiplier` interacts with the
  global `length_mult` here (multiplication).
- [[pitfalls]] — don't ship a per-system ModSettings file.
