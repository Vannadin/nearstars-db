# Phase 3 → Firefly cfg mapping

How a Phase 3 synthesis output translates into a Firefly `ATMOFX_BODY`
(plus optional system-wide `ATMOFX_PLANET_PACK`). Includes the new
Phase 3 Decisions fields this skill expects.

## 1. Trigger condition

A Firefly `ATMOFX_BODY` should be written for a planet iff its
atmosphere is thick enough to produce visible reentry effects. Rule of
thumb:

```
emit_firefly_body  = (atmosphere_pressure_pa >= 100 Pa)
                     OR (atmosphere_present == true with no pressure
                         number — uncertain thin)
```

100 Pa ≈ 0.001 bar — about the threshold below which a probe entry is
indistinguishable from vacuum impact. Mars surface pressure (~600 Pa)
sits well above this; Pluto-like 1 Pa sits below.

For airless bodies, ship **no** Firefly cfg. The mod falls back to its
own Default config, which gives no atmosphere transition rendering on
a body Kopernicus declared atmosphere-less.

## 2. Phase 3 field → Firefly field map

### Direct mappings (Phase 3 fields that already exist)

| Phase 3 Decisions field | Maps to Firefly field | Transform |
|---|---|---|
| `atmosphere_present` | (gate) | If false, skip entire `ATMOFX_BODY` |
| `atmosphere_pressure_pa` | `strength_multiplier`, `wrap_opacity_multiplier`, `wrap_fresnel_modifier` | See §3 (atmosphere-thickness mapping) |
| `atmosphere_composition_volume_pct` (dominant >50%) | `trail_primary`, `trail_secondary`, `trail_tertiary`, `wrap_layer`, `shockwave` | See §4 + [[composition-color]] §3 (bulk-gas table) |
| `atmosphere_composition_volume_pct` (secondary 0.5–10%) | `trail_streak`, `wrap_streak` | See §4 + [[composition-color]] §4 (secondary-species table) |
| `atmosphere_temperature_K_surface` | `particle_threshold` | See §5 (temperature mapping) |
| `body_radius_km` | (no direct) | Influences scale_height + cloud height, indirect |
| `body_kopernicus_name` | `name` | String copy. Match exactly. |

> **Note: aurora colors are NOT mapped to Firefly fields.** Aurora is
> a separate optical phenomenon (low-density upper-atmosphere
> forbidden-line emission) that does not produce the same visible
> signature as reentry plasma. Aurora_color_* fields feed EVE / aurora
> mods, not Firefly. See [[composition-color]] "Do NOT use aurora
> colors" note for the spectroscopy reasoning.

### Indirect / derived (Phase 3 needs new fields)

These don't exist in Phase 3 today. To get tight Firefly outputs, the
next Phase 3 pass should add them to the Decisions table:

| Proposed Phase 3 field | Maps to Firefly | Notes |
|---|---|---|
| `atmofx_strength_override` | `strength_multiplier` | Optional override on the pressure-derived default. Useful for stylized worlds. |
| `atmofx_streak_probability` | `streak_probability` | 0–1. Default 0.07 if atmosphere present. |
| `atmofx_streak_threshold` | `streak_threshold` | Float. Default 0 if not specified; tune empirically. |
| `atmofx_trail_primary_hex_intensity` | `trail_primary` | Format `#RRGGBB×INTENSITY`. e.g. `#bf6348x3` for `191 99 72 3`. |
| `atmofx_trail_secondary_hex_intensity` | `trail_secondary` | Same format. |
| `atmofx_trail_tertiary_hex_intensity` | `trail_tertiary` | Same format. |
| `atmofx_trail_streak_hex_intensity` | `trail_streak` | Same format. |
| `atmofx_wrap_layer_hex_intensity` | `wrap_layer` | Same format. |
| `atmofx_wrap_streak_hex_intensity` | `wrap_streak` | Same format. |
| `atmofx_shockwave_hex_intensity` | `shockwave` | Same format. |
| `atmofx_glow_hex_intensity` | `glow` | Usually Default `#bf5032x1.4`. |
| `atmofx_glow_hot_hex_intensity` | `glow_hot` | Usually Default `#bf5a41x2.5`. |

All `*_hex_intensity` fields use a compact ASCII-safe format:
`#RRGGBB×INTENSITY` (Unicode multiplication sign or plain `x`) so Phase
3 markdown tables stay readable. Conversion at cfg emit time:

```
#bf6348 x 3
   → 191 99 72 3
```

Phase 3 can omit any of these — the cfg writer falls back to the
composition-derived defaults in §4.

## 3. Atmosphere thickness mapping

Pressure decides several multipliers. Calibration anchors from
shipped configs:

| Pressure regime | Example body | `strength_multiplier` | `wrap_opacity_multiplier` | `wrap_fresnel_modifier` |
|---|---|---|---|---|
| Mars-thin (≤ 0.01 bar) | Duna (0.0067 bar) | 0.5 | 1.0 | 0 |
| Thin (0.01–0.5 bar) | Trappist-1 e potential | 0.6–0.8 | 1.0 | 0 |
| Earth-like (0.5–2 bar) | Kerbin (1 bar), Earth | 1.0 | 1.0 | 0 (clear) – 1 (hazy) |
| Thick (2–20 bar) | Eve-thick (5 bar) | 1.0–1.2 | 1.0 | 1 |
| Venusian (50+ bar) | Venus (92 bar) | 1.0–1.5 | 1.0 | 1 |
| Gas giant outer | Jool, Jupiter | 1.0 | 1.0 | 1 |

Heuristic:
```
strength_multiplier = clamp(0.3 + 0.7 × log10(pressure_bar + 1), 0.3, 1.5)
wrap_fresnel_modifier = 1 if pressure_bar >= 1.0 else 0
wrap_opacity_multiplier = 1.0  // rarely deviates from 1
```

## 4. Composition → color (the meat)

Reentry plasma color is driven entirely by atmospheric composition.
Two layers:

### Bulk gas → trail / wrap / shockwave

For the dominant species (>50% volume), pick a row from
[[composition-color]] §3:

| Dominant species (>50%) | Palette row (composition-color §3) | Sets |
|---|---|---|
| N2 + O2 | "Earth-like" | `trail_primary` warm + `shockwave` blue-violet |
| CO2 | "Mars/Venus" | `trail_primary` blue + `shockwave` green |
| H2 + He | "Gas giant (physics)" or stylized | rose+gold (physics) or deep blue (stylized) |
| CH4 | "Titan/CH4" | green-cyan |
| H2O | "Steam atmosphere" | pink-rose |
| Pure H2 | "Cold sub-Neptune" | deep pink |

`glow` and `glow_hot` typically stay at Default values (`191 80 50 1.4`
and `191 90 65 2.5`) — they're hull-surface heating, not gas-specific.
Override only for unusual materials (e.g., a vessel made of an
unusually-emissive alloy — but that's `ATMOFX_PART`, not `ATMOFX_BODY`).

### Secondary species → trail_streak / wrap_streak

For secondary species at 0.5–10% volume (CO2 in a N2 atmosphere, CH4
in Titan-like, He in gas giant, H2O steam fraction, etc.), pick from
[[composition-color]] §4:

| Secondary species present | Streak color (composition-color §4) |
|---|---|
| CO2 1–10% | `96 191 159 2.5` (green) or `116 96 191 2.5` (violet) |
| CH4 trace (in N2 atmo) | `86 93 191 2` (blue-violet, CN) |
| H2O steam fraction | `191 130 130 2` (pink-rose) |
| He in H2 giant | `255 200 100 2` (yellow) |
| NH3 (ice-giant ammonia) | `191 138 68 2` (amber, NH2) |
| SO2 / H2S Venus class | `150 200 180 2` (pale blue-green) |
| N2 (in CO2 atmo, Venus-class) | `191 138 68 2` (yellow-orange, N2 1+) |
| Atmospheric Na vapor (lava worlds) | `255 200 60 3` (bright yellow) |
| K vapor | `180 100 191 2.5` (violet) |
| Organic CN haze | `130 80 191 2.5` (violet) |

Selection rule:
1. Strongest visible emitter wins (Na > K > CO2 > CH4 > H2O > He > others).
2. Tie → pick the species Phase 3 atmosphere synthesis emphasizes.
3. No qualifying secondary (atmosphere is essentially pure dominant
   gas) → streak uses the same value as `trail_primary` (default).

**Do NOT** echo aurora colors into streaks. See [[composition-color]]
"Do NOT use aurora colors" note for the physical reasoning.

## 5. Temperature → `particle_threshold`

Lower threshold = particles activate at lower speeds, helpful for
hot atmospheres where reentry is hotter at any given velocity.

| Surface temperature | Suggested `particle_threshold` (m/s) |
|---|---|
| < 200 K (cold) | 1800 (Default) |
| 200–300 K (Earth-like) | 1800 |
| 300–500 K (hot) | 1500 |
| 500–1000 K (Eve-like) | 1500–1350 |
| > 1000 K (lava world) | 1200–1000 |

For thin atmospheres the threshold matters less because particles
rarely activate anyway. Default is fine.

## 6. Pack-level fields (ATMOFX_PLANET_PACK)

NearStars ships exactly one pack per system with:

```
ATMOFX_PLANET_PACK:NEEDS[NearStarsSystem]
{
	name = NearStars

	strength_multiplier = 1
	transition_offset = 0.2

	affected_bodies = <comma-separated list of all atmosphere-bearing bodies>
}
```

| Pack field | Phase 3 source | Notes |
|---|---|---|
| `name` | hard-coded `NearStars` | No Phase 3 input |
| `strength_multiplier` | system-wide aesthetic decision | Default 1.0 |
| `transition_offset` | system-wide aesthetic decision | Default 0.2 (matches shipped RSS pack) |
| `affected_bodies` | union of all bodies with `atmosphere_present = true` | Comma-join, trim whitespace |

For a Phase 3 batch covering multiple systems, ship one pack node per
system (or one global pack node listing all atmosphere bodies if the
multiplier is system-uniform).

## 7. Worked example — TRAPPIST-1 e

Phase 3 inputs (from `docs/phase3/trappist-1-e.md`):

- atmosphere_present = true
- atmosphere_pressure_pa = 100000 (1 bar)
- atmosphere_composition: N₂ 78%, O₂ ~5%, **CO₂ 1%** (secondary),
  **H₂O 0.1–1%** (secondary), Ar 0.5% (trace, no emission)
- atmosphere_temperature_K_surface ≈ 246 K (THAI II Hab 1 mid)
- body_kopernicus_name = `Trappist1e`
- *(aurora_color_* exists in Phase 3 but is NOT used here — see §4 note)*

Color derivation:
- Dominant N₂+O₂ → "Earth-like" row (composition-color §3): warm trail
  + blue-violet shockwave.
- Secondary: CO₂ 1% (stronger visible emission than H₂O 0.1–1%; selected
  per rule 1) → green streak from CN/C2 Swan (composition-color §4).

Derived Firefly cfg:

```
ATMOFX_BODY
{
	name = Trappist1e
	config_version = 5

	strength_multiplier = 1.0          # 1 bar pressure → Earth-like
	length_multiplier = 1.0
	opacity_multiplier = 1.0
	glow_multiplier = 1.0
	wrap_opacity_multiplier = 1.0
	wrap_fresnel_modifier = 0           # 1 bar with cloud cover, but clear-ish

	particle_threshold = 1800           # 246 K cold surface, Default-equivalent
	streak_probability = 0.07           # Default-active
	streak_threshold = 0                # neutral

	Color
	{
		# Bulk N2+O2 → Earth-like palette (composition-color §3 row 1)
		glow            = 191 80 50 1.4
		glow_hot        = 191 90 65 2.5
		trail_primary   = 191 99 72 3      # warm trail (N2+ + O atomic emission)
		trail_secondary = 191 70 42 1.5    # darker warm
		trail_tertiary  = 74 80 191 2      # cool fade (N2+ blue)
		wrap_layer      = 69 69 191 2      # blue envelope
		shockwave       = 74 90 191 3      # blue-violet shock (N2+ 391 nm)

		# Secondary CO2 1% → green streaks from CN + C2 Swan
		# (composition-color §4 CO2 secondary row)
		trail_streak    = 96 191 159 2.5
		wrap_streak     = 96 191 159 2
	}
}
```

Key choices and citations:
- Bulk palette: N2+O2 "Earth-like" row from composition-color.md §3.
- Streak palette: CO2 1% selected as the strongest secondary
  (composition-color.md §4 row "CO2 in N2/O2 atmosphere"). H2O 0.1–1%
  is also present but Hα emission is weaker than CN+C2 Swan at these
  concentrations.
- Aurora colors from Phase 3 (`#4DFF4D` green, `#FF4D4D` red) are NOT
  used. Aurora is a separate optical phenomenon (upper-atmosphere
  forbidden-line emission); it does not contribute to the lower-
  atmosphere shock layer that Firefly renders.
- particle_threshold = 1800: surface is cold (246 K), no need to lower.
- wrap_fresnel = 0: matches shipped Kerbin (1 bar + cloud cover).

## 8. Worked example — TRAPPIST-1 b (airless / minimal)

Phase 3 outputs for b indicate possible thin CO2 envelope (~0.001 bar
upper limit from Hu 2025) or fully airless (Greene 2023).

Decision tree:
- If Phase 3 commits to airless: ship **no** `ATMOFX_BODY`.
- If Phase 3 commits to thin CO2 atmosphere: ship a body cfg with
  `strength_multiplier = 0.3`, palette from CO2 row, all else Default.

For canonical-alternatives split: the cfg variant for the airless
interpretation simply removes the `ATMOFX_BODY` block.

## 9. NearStars pack worked example

```
ATMOFX_PLANET_PACK:NEEDS[NearStarsSystem]
{
	name = NearStars

	strength_multiplier = 1
	transition_offset = 0.2

	affected_bodies = ProximaCenB, AlphaCenBb, Trappist1c, Trappist1d,
                       Trappist1e, Trappist1f, Trappist1g, Trappist1h
}
```

(b excluded if airless interpretation chosen; included if thin-atmo
interpretation chosen.)

## 10. Open Phase 3 gaps

For Phase 3 to fully feed Firefly without cfg-writer judgment, future
passes could add (all optional, with the skill falling back to
composition-derived defaults if absent):

### Tier 1 — palette overrides (rare, only when default derivation is wrong)

- A single `atmofx_palette` enum (`earth_n2_o2` / `mars_co2` /
  `gas_giant_h2_he` / `titan_ch4` / `steam_h2o` / `custom`) plus
  override hex fields, OR the 12 individual `atmofx_*_hex_intensity`
  color fields.
- `atmofx_strength_override` (float).
- `atmofx_streak_probability` / `atmofx_streak_threshold` (floats).

### Tier 2 — exotic trace emitters (Phase 3 already covers ordinary cases)

`atmosphere_composition_volume_pct` already lists the common secondary
species (CO2, CH4, H2O, He, SO2, etc.) and the skill picks streaks
from there. But for some exotic bodies the spectroscopically active
species isn't in the headline composition table:

- Lava-world atmospheric **Na / K vapor** (e.g., 55 Cancri e class) at
  ppm-level partial pressure but with strong visible emission.
- **Photolysis products** (N2O, NO, O3) generated by stellar UV in
  evolved N2 atmospheres.
- **Tholin haze CN/C2** in Titan-like or sub-Neptune atmospheres.
- **Ablated rock vapor** (Mg, Fe) on bare-rock entries.

For these, an optional Phase 3 field would cleanly pass the data:

```
atmofx_trace_emitters:
  - species: "Na"
    role: "atmospheric vapor (volcanic outgassing)"
    emission_visible: "D-line 589 nm yellow"
    strength: "strong"
    source: "Castan 2011 lava world chemistry"
  - species: "Mg"
    role: "rock vapor (high-T ablation regime)"
    emission_visible: "Mg I 285 + green band"
    strength: "moderate"
```

If present, the skill uses these to set `trail_streak` / `wrap_streak`
in preference to the composition_volume_pct secondary. If absent
(typical), the skill falls back to the composition_volume_pct
secondary row (composition-color §4).

This field is **never required** — its absence is the default
expectation, not an error.

### Until those fields land

The cfg writer derives values from `atmosphere_pressure_pa` +
`atmosphere_composition_volume_pct` (dominant + secondary) +
`atmosphere_temperature_K_surface` using the heuristics in §3–§5.
This handles all common Earth-analog, Mars-analog, Venus-analog,
gas-giant, and Titan-analog cases.

## See also

- [[atmofx-body]] — full body schema.
- [[atmofx-planet-pack]] — pack schema.
- [[composition-color]] — verified composition → color table.
- [[color-format]] — HDR color string syntax.
- [[pitfalls]] — common write-time mistakes.
