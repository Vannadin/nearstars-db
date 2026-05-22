# Firefly cfg pitfalls

Common mistakes encountered when writing Firefly configs. Each entry
explains the symptom, the cause, and the fix. Read these before
hand-writing a body config.

## Parse-level failures

### "wrong version config" error

Symptom: body fails to load, Error Manager window shows "wrong
version" red bar.

Cause: `config_version` is missing, 0, or anything other than 5.
`ConfigManager.cs:494-497` silently sets missing version to 4 → fails
the equality check at line 302.

Fix: ensure every `ATMOFX_BODY` has `config_version = 5`.

### "could not be registered" with no further detail

Symptom: body loads but renders with default appearance.

Likely causes:
1. A color key in `Color { … }` is missing, `null`, `default`, or
   malformed → entire body rejected. Body-level Color rejects partial
   specs (`ConfigManager.cs:651-666`).
2. A multiplier value is not a parseable float (typo like
   `strength_multiplier = 1.0f` — the `f` suffix fails `float.TryParse`
   in `Utils.cs:175`).
3. Duplicate body name with another loaded `ATMOFX_BODY`. Silent skip
   — but the first one wins, so a NearStars body shadowed by a stock
   Default loads only the first occurrence.

Fix: check all 9 color keys are present + parse cleanly; check all
floats are bare numbers like `0.5`, not `0.5f` or `0,5`.

### Color "comma trap"

Symptom: parse fails with no specific reason, body uses default.

Cause: writing colors with commas (`191, 80, 50, 1.4`) — KSP cfg
splits on space, so the comma becomes part of the token (`"191,"`)
which fails `float.TryParse`.

Fix: spaces only. `191 80 50 1.4`.

### FloatPair single-value failure (particles)

Symptom: particle config rejected, particles invisible.

Cause: writing `rate = 46` instead of `rate = 46 46`. `EvaluateFloatPair`
requires exactly 2 tokens (`Utils.cs:194-197`).

Fix: always emit two floats even when min and max are equal.

## Semantic / load-order issues

### Body affected by no `ATMOFX_PLANET_PACK`

Symptom: per-system tuning via `strength_multiplier` is not applied
to all bodies.

Cause: a body name in the `affected_bodies` list doesn't match the
actual `ATMOFX_BODY` `name = …`. Case-sensitive.

Fix: list exact names. The loader compares with `.Contains` on the
parsed string array (`ConfigManager.cs:520`).

### Multiple packs affecting one body

Symptom: only one pack's multiplier applied even when two should
combine.

Cause: `ConfigManager.cs:517-525` iterates packs and overwrites
`body.planetPack` each time — only the **last** matching pack wins.
There's no multiplication chaining across packs.

Fix: don't ship overlapping packs. If two presets need to combine,
merge them into one pack.

### `:NEEDS[…]` missing on pack node

Symptom: pack multipliers apply even when the planet pack mod isn't
installed.

Cause: the cfg loads unconditionally because Module Manager didn't
strip it.

Fix: always tag the pack node with `:NEEDS[<PackMod>]`. For NearStars,
use `:NEEDS[NearStarsSystem]`.

### Custom body has no `ATMOFX_BODY` → uses Default

Symptom: a NearStars body shows Earth-like (Default) reentry colors
instead of the intended palette.

Cause: no `ATMOFX_BODY` ships for that body name. `TryGetBodyConfig`
returns the Default config with `fallback=true`
(`ConfigManager.cs:681-696`).

Fix: ship one `ATMOFX_BODY` per system body. Atmosphere-less bodies
still need a config if you want any reentry effect at all (they get
none if the body lacks atmosphere, but the config still influences
near-atmosphere transition rendering).

## HDR / visual issues

### Colors look washed out / dull

Causes:
- `intensity` is 0 or negative on the HDR color. The boost is
  `2^intensity`, so 0 means no boost.
- `hdr_override = False` in `ATMOFX_SETTINGS` and the scene camera is
  LDR.
- `glow_multiplier`, `opacity_multiplier`, or `wrap_opacity_multiplier`
  is below 1.

Fix: target intensity 1.4–3.0 for body colors; confirm HDR is on.

### Colors over-saturate / screen-blowing

Causes:
- `intensity > 4` on multiple keys.
- `strength_multiplier > 2` combined with a planet pack multiplier > 1.

Fix: keep multipliers ≤ 1.5 by default; reserve intensity > 3 for
hot-trail accents only.

### Streaks never appear

Causes:
- `streak_probability = 0` (default).
- `streak_threshold` too high — comment in source claims 1 = 4000 m/s
  but observed shipped values use negative numbers; tune empirically.

Fix: set `streak_probability` to ~0.07 (shipped value for Duna, Eve,
Jool), tune `streak_threshold` between -0.5 and 0.

## NearStars-specific gotchas

### Body name mismatch with Kopernicus

Symptom: an `ATMOFX_BODY` config exists but is never used at runtime.

Cause: `name = …` doesn't match the Kopernicus body's `name = …`
exactly. Case + spelling sensitive.

Fix: copy the Kopernicus body name verbatim. For NearStars systems
that name bodies with star prefixes (e.g., `Trappist1b`), ensure no
spaces or dashes leak in.

### Part-override shipped without `:NEEDS[Firefly]`

Symptom: NearStars manifest references a Firefly part config but the
game console logs warnings about missing nodes when Firefly is
uninstalled.

Fix: add `:NEEDS[Firefly]` on any `ATMOFX_PART` node shipped from a
NearStars-side patches directory.

### Shipping a `ModSettings.cfg`

Symptom: player's custom HDR / bowshock / particle settings get
overridden.

Fix: never ship `ATMOFX_SETTINGS`. It's user-side preference
(`SettingsManager.cs`). The mod creates a default file on first
launch.

## Editor / GUI mismatches

The in-game effect editor saves to `GameData/Firefly/Configs/Saved/`
(`ConfigManager.cs:189`). A cfg writer's hand-authored config can be
shadowed by an editor-saved file with the same body name. If a body
"won't update" after editing the cfg, check the Saved/ directory first.

## Debugging tips

1. **Check the KSP log** — Firefly logs every config load with prefix
   `[Firefly]` (`Utils.cs:411`). Look for `"Body couldn't be loaded"`
   or `"Body config is not formatted correctly"`.
2. **Use the Error Manager window** — shows red bars per failed cfg
   with the source URL of the offending cfg.
3. **Compare with shipped Default** — if a hand-written body cfg
   doesn't load, compare structure against `GameData/Firefly/Configs/Default.cfg`.
4. **Verify with stock body cfgs** — `Configs/Stock/<Body>.cfg` and
   `Configs/RSS/<Body>.cfg` are known-good schema samples.

## Source citations

All source-line citations refer to
`firefly-repo/Source/Firefly/ConfigManager.cs` and `Utils.cs` at the
master branch as of clone (see `../research-notes.md` §13 for the
clone reference).

## See also

- [[atmofx-body]] — schema reference.
- [[color-format]] — HDR color value rules.
- [[atmofx-planet-pack]] — pack-level interaction.
