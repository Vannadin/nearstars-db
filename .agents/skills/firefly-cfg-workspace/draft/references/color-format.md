# Firefly HDR color format

The single most error-prone field in Firefly configs. Read this before
writing any `Color { … }` block.

## Format

```
key_name = R G B intensity
```

Four floats, space-separated. Parsed by `Utils.EvaluateColorHDR`.

| Token | Type | Range | Meaning |
|---|---|---|---|
| R | float | 0–255 | Red channel, integer-style values typical |
| G | float | 0–255 | Green |
| B | float | 0–255 | Blue |
| intensity | float | observed 1.0–3.0 | HDR exponent — final RGB is multiplied by `2^intensity` |

The parser splits on a single space. Fewer than 4 tokens → parse fails
and the entire body config is rejected.

## How intensity is applied

```
final.R = (R / 255) × 2^intensity
final.G = (G / 255) × 2^intensity
final.B = (B / 255) × 2^intensity
```

So `intensity = 0` means no boost (LDR), `intensity = 1` doubles, `2`
quadruples, `3` is 8×. The shipped configs cluster around 1.4–3.0.

There is no parser-enforced cap on intensity. Values above ~4 saturate
the screen and look identical to lower values, so don't go beyond 3.5
without a reason.

## Null / default

Inside `ATMOFX_PART`, individual color keys may be:

- `null` (case-insensitive)
- `default` (case-insensitive)
- Or simply omitted

…which falls back to the body's color for that key.

Inside `ATMOFX_BODY`, omission or `"null"` is an **error** — every key
in the `Color { … }` block must be a valid HDR color string.

## All Color keys

Both `ATMOFX_BODY` and `ATMOFX_PART` accept the same 9 keys:

| Key | What it tints |
|---|---|
| `glow` | Cool surface glow on the vessel hull |
| `glow_hot` | Hot core surface glow (replaces `glow` at high heat) |
| `trail_primary` | Main plasma trail color |
| `trail_secondary` | Secondary plasma trail tint |
| `trail_tertiary` | Edge / fade plasma trail tint |
| `trail_streak` | Particle streak color |
| `wrap_layer` | Outer plasma envelope around the vessel |
| `wrap_streak` | Streaks within the wrap layer |
| `shockwave` | Bow shockwave color (front of vessel) |

## Reference values (shipped stock)

Default (orange-blue plasma — Earth-like baseline):

```
glow           = 191 80 50 1.4
glow_hot       = 191 90 65 2.5
trail_primary  = 191 99 72 3
trail_secondary= 191 70 42 1.5
trail_tertiary = 74 80 191 2
trail_streak   = 74 80 191 2
wrap_layer     = 69 69 191 2
wrap_streak    = 191 99 72 3
shockwave      = 74 90 191 3
```

Eve (sulfuric CO2, blue-green plasma):

```
trail_primary  = 83 92 191 2
trail_tertiary = 122 191 170 2
shockwave      = 96 191 159 3
```

Jool (gas giant, yellow-blue plasma):

```
trail_primary  = 32 20 191 1.4
trail_secondary= 191 6 6 3
trail_tertiary = 191 191 88 1.7
shockwave      = 140 191 161 1
```

Observation: `glow` and `glow_hot` are identical across all stock
bodies. Variation lives in trail/wrap/shockwave.

## Composition → color hints

The Firefly wiki "Useful information" page documents a periodic-table
mapping of plasma emission lines per element. Phase 3 mapping (see
[[phase3-mapping]]) uses this to translate atmosphere composition into
suggested trail colors. Quick summary:

| Dominant species | Plasma color tendency |
|---|---|
| N2 / O2 (Earth-like) | Orange-pink-violet (Default) |
| CO2 / H2SO4 (Venus / Eve) | Green-blue |
| H2 / He (gas giant) | Pale yellow / red |
| H2O / CH4 | Tealâ€“cyan |
| Trace metals (Na, K, Fe) | Yellow / violet streaks |

Use these as a starting point — final tuning is aesthetic and goes
through cfg variant review.

## Common mistakes

- **3 tokens instead of 4** — forgetting the intensity. Parse fails.
- **Comma separators** — KSP cfg uses spaces. `191, 80, 50, 1.4` will
  not parse as a color (the comma is part of the first token).
- **Intensity in 0–255 range** — intensity is an exponent, not a 0–255
  value. `intensity = 100` gives `2^100` ≈ infinity → engine artifacts.
- **HDR color in a non-HDR field** — `Color { … }` is the only place
  HDR colors are accepted. Don't reuse this format in particle prefab
  fields or settings.

## See also

- [[atmofx-body]] — where the `Color { … }` block lives.
- [[atmofx-part]] — same format, partial overrides allowed.
- [[pitfalls]] — broader cfg pitfalls.
