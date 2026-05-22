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
