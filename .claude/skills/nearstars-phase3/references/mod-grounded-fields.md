<!-- Phase 3 → Kerbalism / EVE / Scatterer cfg 필드 매핑 — 모드 호환 필드와 출처 -->
# Mod-grounded cfg fields

Phase 3 outputs need specific values to feed the downstream mod cfg
writers cleanly. This file enumerates the fields required by each
mod and the literature sources that constrain them.

Add these to the Decisions table whenever Phase 3 work covers them.
If a field is unconstrained for a given planet, mark it as null /
"unknown" with Confidence=low and a `tie-break: airless-default`
note in the Basis cell.

## Kerbalism radiation / magnetosphere fields

Kerbalism uses the planet's magnetic dipole + atmospheric column to
compute crew radiation exposure inside its KSP-side cfg. Source data
goes in the Phase 3 Decisions table; the cfg writer reads from there.

| Field | Unit | Range typical | Notes |
|---|---|---|---|
| `magnetic_field_strength_microtesla_equator` | μT | 0–60 | Earth ≈ 30 μT at equator; M-dwarf tidal-lock planets usually 0–10 μT |
| `magnetic_dipole_moment_normalized_earth` | × Earth | 0–1 (rarely > 1) | Earth = 1.0. Dynamo-killed planets = 0. Rocky tidally-locked typically 0.01–0.3 |
| `magnetic_dipole_tilt_deg` | deg | 0–30 | Earth ≈ 11°. For tidally locked, no strong constraint — pick 5–15° for interesting auroral offset |
| `radiation_belt_present` | bool | true/false | Earth has van Allen belts; field strength < ~0.1× Earth probably can't sustain belts |
| `radiation_inner_belt_radius_planet_radii` | R_p | 1.2–2.0 | Earth inner belt ≈ 1.2–3 R_⊕ |
| `radiation_outer_belt_radius_planet_radii` | R_p | 3–8 | Earth outer belt ≈ 3–7 R_⊕ |
| `surface_radiation_dose_msv_yr` | mSv/yr | 0.1–10000 | Earth surface ≈ 2.4 mSv/yr (natural). M-dwarf HZ planet without B-field can be 10³–10⁴ mSv/yr |
| `atmospheric_shielding_g_cm2` | g/cm² | 0–2000 | Earth ≈ 1030 g/cm². Mars-thin ≈ 16. Vacuum = 0 |

Source priority order:
1. Direct planet-specific simulation paper (rare — Cohen 2014/2024
   for TRAPPIST-1 only)
2. System-wide MHD / SEP paper (Dong 2018 — 1705.05535; Cohen 2024
   if available)
3. Scaling relation from theory (Reiners 2010 dynamo scaling,
   Driscoll & Olson 2011)
4. Confidence=low aesthetic guess per interesting-first rule

## EVE aurora fields

EVE's aurora layer needs a position (latitude band), color, and
intensity. The cfg writer turns these into a sprite/shader cfg.

| Field | Unit | Range typical | Notes |
|---|---|---|---|
| `aurora_present` | bool | true/false | Requires both an atmosphere AND non-zero magnetic field. Airless → false |
| `aurora_color_primary_hex` | hex | `#00FF7F` etc. | Earth = green-ish ([OI] 557 nm). CO₂-dominated → UV/violet ~`#7030C0`. N₂-rich → cyan-violet `#3060FF` |
| `aurora_color_secondary_hex` | hex | optional | Earth has red [OI] 630 nm = `#FF4040` accent. Most cfg can omit |
| `aurora_emission_species_primary` | prose | — | "O[I] 557 nm", "CO₂⁺ doublet 289 nm", "N₂⁺ Meinel 391 nm", etc. |
| `aurora_oval_magnetic_latitude_deg` | deg | 50–75 | Earth aurora oval centers at ~67° magnetic lat. For weak fields, oval expands toward equator |
| `aurora_intensity_kR_typical` | kR (kilorayleighs) | 0.1–500 | Earth typical 10 kR; M-dwarf flare-driven planets can reach 100–500 kR |
| `aurora_visibility_fraction_year` | 0–1 | 0.01–1.0 | Earth ≈ 0.05 (visible at high lat). TRAPPIST-1 planets with frequent flares: 0.3–0.7 |

Source priority:
1. Aurora-specific paper for the planet (very rare)
2. Stellar SEP / proton flux paper (Fraschetti 2019 — 1902.03732;
   Atri 2020 — 1910.09871)
3. Atmospheric composition → emission species (chemistry papers)
4. Interesting-first aesthetic choice with Earth as baseline

## Scatterer atmosphere optics

Most atmosphere optics fields are already in the standard template
(`atmosphere_tint_rgb_hex`, `cloud_tint_rgb_hex`). Two new fields
specific to Scatterer's terminator rendering:

| Field | Unit | Range typical | Notes |
|---|---|---|---|
| `sunset_color_hex` | hex | — | Color at zenith from the terminator viewpoint. M-dwarf SED → red-orange `#FF4500` to deep `#A02000`; thin atmo → less saturation |
| `mie_scattering_aerosol_anisotropy_g` | -1..1 | 0.6–0.85 | Earth aerosol ≈ 0.76; haze ≈ 0.7; ice clouds ≈ 0.85 |

These come from the same atmosphere composition + SED reasoning
already in the synthesis. The cfg writer can compute these from
atmospheric pressure + composition + dominant aerosol if not
explicitly specified — they're optional Phase 3 outputs.

## Dependencies for Phase 3 magnetic-field decision

Magnetic field is the hardest to pin down per planet. Best practice:

1. **Check if the planet has a published dynamo model** — TRAPPIST-1
   has Driscoll/Olson-style scaling work for some planets
2. **Check if it has a measured field upper limit** — usually from
   radio non-detection (Vedantham 2020, Pineda & Villadsen)
3. **Apply tidally-locked dynamo penalty** — slow rotation (≥ days)
   typically reduces dipole moment to 0.1–0.3× the rapid-rotation
   value (Reiners & Christensen 2010)
4. **Apply core-cooling consideration** — small planets cool fast and
   may have frozen cores by 7+ Gyr. Mars-mass planets like h are
   nearly certain to be dynamo-dead today
5. **Default low estimate when uncertain** — 0.01–0.1× Earth dipole
   for active worlds; 0 for small / old / volatile-rich worlds
6. **Pick a dipole tilt within 5–15°** per interesting-first — too
   small makes auroras a uniform polar cap (boring); too large is
   physically implausible

## Circumstellar disk → Kopernicus Ring (star body)

A stellar debris or protoplanetary disk renders in Kopernicus as a
`Ring` subnode attached to the **star body** (not a planet). This
section maps Phase 3 Decisions fields (defined in
[`synthesis-template.md`](synthesis-template.md) § "Circumstellar
disk") to the Kopernicus Ring fields the kopernicus-cfg emitter will
write.

| Phase 3 field | Kopernicus Ring field | Unit conversion | Notes |
|---|---|---|---|
| `disk_present` | (presence gate) | — | If false, omit the entire Ring subnode |
| `disk_inner_radius_au` | `innerRadius` | × 1.496e8 (AU → km) | KSP km |
| `disk_outer_radius_au` | `outerRadius` | × 1.496e8 (AU → km) | KSP km |
| `disk_tint_rgb_hex` | `color` | hex → RGBA (alpha = `disk_opacity`) | Linear-space; Kopernicus expects 0–1 floats |
| `disk_opacity` | (alpha channel of `color`) | direct | Or per-mesh `unlit` parameter; emitter chooses |
| `disk_imaging_inclination_deg` | `rotation` (axis tilt) | direct | Only emit if `disk_resolved_imaging=true` and value is constrained |
| `disk_morphology` | (steps / texture path) | prose → texture variant | Single-ring → solid; multi-ring → `steps` divisions; asymmetric → custom texture path with placeholder per `kopernicus-emit-workspace` convention |
| `disk_planetesimal_belt_inferred` | (asteroid belt cfg, separate from Ring) | bool | If true, optionally emit a sparse `Asteroid` group at the disk midpoint; not part of Ring subnode |
| `disk_dust_temperature_k` | (informational, drives `disk_tint_rgb_hex` synth) | — | Phase 3 step uses dust T to pick the hex; cfg writer just uses the hex |

Source priority for disk geometry:

1. ALMA / VLT-SPHERE / HST-STIS resolved imaging — gives
   `disk_inner_radius_au`, `disk_outer_radius_au`,
   `disk_imaging_inclination_deg` directly
2. Herschel / Spitzer SED fit (e.g. Su 2013, Sibthorpe 2018) —
   gives `disk_inner_radius_au` (or single representative radius)
   + `disk_dust_temperature_k` from black-body fit
3. Photometric IR excess only (IRAS, WISE, Spitzer-MIPS without
   spatially-resolved data) — gives `disk_present`,
   `disk_dust_temperature_k`; geometry needs the
   black-body-fit-with-assumed-grain-size shortcut

**Texture path convention** (deferred to the texture pipeline per
the open question in
[`phase3/kopernicus-emit-workspace/context-notes.md`](../../../phase3/kopernicus-emit-workspace/context-notes.md)):
emit a placeholder path string under
`GameData/NearStarsSystem/PluginData/<star>/disk_<variant>.dds` and
log the missing-asset entry. Module Manager won't fail to load with
a missing texture path; the star just uses the fallback ring shader
until the asset pipeline fills the dds.

## Planetary ring → Kopernicus Ring (planet body)

A Saturn-like planetary ring renders in Kopernicus as a `Ring`
subnode attached to the **planet body**. Same Kopernicus primitive
as Circumstellar disk; different parent body and different field
prefix.

Field names match the sidecar yaml defined in
[`phase3/kopernicus-emit-workspace/context-notes.md`](../../../phase3/kopernicus-emit-workspace/context-notes.md)
so the emitter can read Phase 3 Decisions directly without a sidecar
yaml indirection.

| Phase 3 field | Kopernicus Ring field | Unit conversion | Notes |
|---|---|---|---|
| `ring_present` | (presence gate) | — | If false, omit the entire Ring subnode |
| `ring_inner_au` | `innerRadius` | × 1.496e8 (AU → km) | KSP km |
| `ring_outer_au` | `outerRadius` | × 1.496e8 (AU → km) | KSP km |
| `ring_color_hex` | `color` | hex → RGBA (alpha = `ring_opacity`) | Linear-space; Kopernicus expects 0–1 floats |
| `ring_opacity` | (alpha channel of `color`) | direct | — |
| `ring_morphology` | (steps / texture path) | prose → texture variant | Single-ring → solid; multi-ring → `steps` divisions; shepherded → divisions at shepherd-moon resonances |

Source priority for planetary rings:

1. Direct imaging (Cassini-class observation) — almost never
   available for exoplanets; effectively Sol-only (Saturn, Jupiter
   faint, Uranus narrow, Neptune narrow)
2. Transit detection (J1407 b-class ring; rare and disputed)
3. Confidence=low aesthetic choice for gameplay variety —
   interesting-first rule applies. Document tie-break in Basis.

## Circumplanetary disk → Kopernicus Ring (planet body)

A young protoplanetary or moon-forming disk (e.g. PDS 70 c) uses
the same Kopernicus Ring primitive at the planet body but is
distinct from a Saturn-like ring in scale + dust temperature +
lifetime. Rare for NS targets — included for completeness.

| Phase 3 field | Kopernicus Ring field | Unit conversion | Notes |
|---|---|---|---|
| `circumplanetary_disk_present` | (presence gate) | — | If false, omit |
| `circumplanetary_disk_radius_planet_radii` | `outerRadius` | × planet `Properties.radius` km | Inner radius defaults to planet Roche limit unless cited |
| `circumplanetary_disk_tint_rgb_hex` | `color` | hex → RGBA | Warmer (yellower) than debris disks due to dust T ~150–300 K |
| `circumplanetary_disk_opacity` | (alpha channel) | direct | Typically higher than debris (still actively accreting) |
| `circumplanetary_disk_dust_temperature_k` | (informational) | — | Drives tint synth |
