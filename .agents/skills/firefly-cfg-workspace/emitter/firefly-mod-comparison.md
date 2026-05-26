# Firefly mod — shipped configs comparison

Subagent analysis (2026-05-26) of all 27 ATMOFX_BODY nodes in the
Firefly mod's shipped configs. Used as ground truth for our 6 bulk-gas
palette decisions in `emit_firefly_cfg.py`.

## Coverage

- **Default** (1) — fallback for unrecognized bodies
- **Stock KSP** (4) — Kerbin, Eve, Duna, Jool
- **RSS** (8) — Earth, Venus, Mars, Jupiter, Saturn (via MM), Titan, Uranus (via MM), Neptune
- **OPM** (5) — Sarnus, Urlum, Neidon, Tekto, Thatmo
- **MPE** (1) — Ervo
- **Kcalbeloh** (15) — 15 exoplanet system bodies

`glow = 191 80 50 1.4` and `glow_hot = 191 90 65 2.5` are identical
across all 27 nodes. Our `DEFAULTS_HEX_RGB` agrees.

## Composition → color mapping (Firefly author's actual pattern)

| Composition | Firefly intent | Representative `trail_primary` | `shockwave` |
|---|---|---|---|
| N2/O2 (Earth-like) | warm orange + deep blue | 191 99 72 | 74 90 191 |
| CO2 thick (Venus) | cool blue + cool blue | 83 92 191 | 40 61 191 |
| CO2 thin (Mars/Duna) | cool blue + deep blue | 76 116 191 | 34 41 191 |
| N2/CH4 haze thick (Titan) | warm orange + warm orange | 191 99 63 | 191 99 62 |
| N2/CH4 haze cryo (Tekto/Thatmo) | yellow-amber + dim teal | 184 116 6 / 241 187 34 | 41 113 153 |
| H2/He gas giant (Jupiter/Saturn) | purple + deep blue | 136 98 191 | 11 29 191 |
| H2/He+CH4 ice giant (Uranus/Neptune) | purple-magenta + deep blue | 141 91 191 | 64 41 191 |
| OPM ice giant template (Neidon) | deep indigo + lavender | 78 17 208 | 176 178 230 |
| thin cryo (Ervo) | dim teal + dim teal (low alpha) | 15 121 133 (α=0.23) | 41 113 153 |
| Joolian unique | deep blue + green (stylized) | 32 20 191 | 140 191 161 |

## Agreement with our 6 palettes

| Our palette | Firefly counterpart | Agreement | Divergence |
|---|---|---|---|
| `earth_like` | Default / Kerbin / Earth | **100% match** | None |
| `co2` | Eve (full match), Venus / Mars (trail match, shockwave deeper blue) | trail ✓, shockwave partial | Our teal `shockwave 96 191 159` aligns with Eve only; Venus/Mars use deeper blue 34-61/191. Eve was the actual source of our co2 row |
| `gas_giant` | Jupiter / Saturn / Sarnus | **divergent** | We chose physics-faithful pink-red (Balmer Hα). Firefly chose stylized purple+blue. Both defensible; per `composition-color.md §5`, the H2/He gas-giant row explicitly notes Jool/Jupiter as a stylized choice |
| `methane` | Titan / Tekto / Thatmo / Mehtna | **direction differs** | We chose Swan-band green (C2 photochemistry). Firefly chose tholin yellow-amber (Mie haze scattering). Both physically real — different layers being modeled |
| `steam` | none in Firefly's shipped configs | **N/A** | No KSP body is a hot waterworld; our `steam` palette has no ground truth here |
| `pure_h2` | Sedah (Kcalbeloh) | partial | Sedah's hot pink trail (208 17 155) is the only close match in shipped configs |

## Patterns we initially missed

### 1. Thin atmosphere → low alpha (not just strength_multiplier)

Tekto, Thatmo, Ervo, Uleg all use `trail_primary` alpha ∈ [0.23, 0.6]
instead of our default 3.0. The `strength_multiplier` parameter only
scales the overall effect; the alpha channel inside each `Color { … }`
key is independent and controls visibility of the specific layer.

For NearStars: Phase 3 bodies with `atmosphere_surface_pressure_pa <
~10000 Pa` (0.1 bar) should consider an alpha-dampened variant of the
matched palette. Currently emit_firefly_cfg.py uses fixed intensity
multipliers from the palette dict, which works for the established
cases (TRAPPIST-1 e at 1 bar, ProximaCenB at 1 bar) but would
underperform for thin-atmosphere edge cases.

### 2. Ice giant ≠ gas giant

Firefly clearly distinguishes:
- **Gas giant** (Jupiter, Saturn, Sarnus): purple + deep blue
- **Ice giant** (Uranus, Neptune): magenta + purple + deep blue, with
  brighter wrap_layer

Our single `gas_giant` palette covers both. Adding an `ice_giant`
palette would track Firefly's authorial choice and reflect the real
physical difference (ice giants have more CH4 photochemistry coloring
the upper atmosphere). Trigger condition: dominant H2 with CH4 trace
≥ 1% by volume.

### 3. wrap_layer is mostly uniform across bodies

Of 27 nodes, the OPM/Kcalbeloh "default ice giant" template uses
`wrap_layer = 191 124 73` (dusty orange) for 15 bodies. Our palette
varies wrap_layer per type — this is over-specification relative to
the mod author's practice. A single dusty-warm default would also work.

### 4. Glow/glow_hot is universal

All 27 nodes share `glow = 191 80 50 1.4` and `glow_hot = 191 90 65 2.5`.
We do the same via `DEFAULTS_HEX_RGB`. Confirmed correct.

## Notable divergences worth documenting (not bugs)

- **Jool** (KSP stock) uses deep blue + red + green. KSP wiki says
  Jool atmosphere is "Joolian gas" without specifying composition —
  the author had license to stylize. Our `gas_giant` palette doesn't
  apply to KSP stock anyway (NearStars doesn't replace Jool).
- **Mehtna** (Kcalbeloh) is named "methane reversed" but uses red +
  yellow + blue, not our methane green. Either Kcalbeloh's Mehtna has
  oxidized atmosphere (different from CH4-dominant), or it's stylized
  artistic choice.
- **Sedah** (Kcalbeloh, "Hades reversed") matches our `pure_h2` hot
  pink. The only Kcalbeloh body whose trail color independently
  validates a NearStars palette decision.

## Implications for emit_firefly_cfg.py

Items below would refine the emitter; none are blocking issues.

1. **Add thin-atmosphere alpha damping.** When `pressure_pa < 10000`,
   multiply trail_primary/secondary/tertiary alpha by ~0.3. Mirrors
   what Firefly's Tekto/Thatmo do. Currently we only scale via
   `strength_multiplier`.

2. **Add `ice_giant` palette as 7th bulk-gas type.** Trigger when
   atmosphere is H2-dominant AND has ≥1% CH4 trace. Matches Firefly's
   Uranus/Neptune treatment vs. Jupiter/Saturn.

3. **Re-evaluate `co2` shockwave.** Currently teal (96/191/159) matching
   Eve. Could split into "thin CO2" (Mars/Duna template, deep blue
   shockwave) and "thick CO2" (Venus template, deeper blue). Firefly
   makes this distinction.

4. **Simplify wrap_layer.** Optional — collapse to a shared neutral
   warm tone (~191/124/73) across most palettes, reserve distinct
   wrap_layer only for cases where it's load-bearing (gas_giant rim).

## Source files analyzed

Located under `.agents/skills/firefly-cfg-workspace/firefly-repo/GameData/Firefly/Configs/`:

- `Default.cfg`
- `Stock/{Kerbin,Eve,Duna,Jool}.cfg`
- `RSS/{Earth,Venus,Mars,Jupiter,Saturn,Titan,Uranus,Neptune}.cfg`
- `OPM/{Sarnus,Urlum,Neidon,Tekto,Thatmo}.cfg`
- `MPE/Ervo.cfg`
- `Kcalbeloh/{Ahtpan,Anehta,Arorua,Efil,Iomena,Mehtna,Norihc,Noyreg,Rouqea,Sedah,Sera,Simeht,Simetra,Suluco,Uleg}.cfg`

## Related

- [emitter checklist](checklist.md) — overall emitter workspace state
- [context-notes](context-notes.md) — schema decisions
- [composition-color §3-5 in firefly-cfg skill](../../../../.claude/skills/firefly-cfg/references/composition-color.md) — our palette derivation reasoning
