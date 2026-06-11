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

## Kerbalism stellar wind / astrosphere fields (star body)

The section above is the *planetary* side (the planet's own magnetosphere,
belts, surface dose). This is the *stellar* side — the star itself as a
`RadiationBody`: the dose source and the heliosphere that shields galactic
cosmic rays. Derived from the Phase 2 stellar measurements
(`mass_loss_measurements`, `activity_cycle_measurements`,
`magnetic_field_measurements`) + luminosity + 6D astrometry. Consumed by the
(future) kerbalism-cfg writer and the heliotail Harmony plugin. See
[[project-nearstars-stellar-wind-kerbalism]] for the reverse-engineered
mechanism.

**Kerbalism stellar model (grounded in `Radiation.cs`).** A star carries
`radiation_surface` (rad/h, inverse-square wind/cosmic dose), `solar_cycle`
(s), and a heliopause pause (large `pause_radius`, *negative* `radiation_pause`
= a GCR shield). No belts on stars. Sun (ROKerbalism) baseline:
`radiation_surface` 46.5, `solar_cycle` 11 yr, `pause_radius` 1000 R☉. The
nose–tail axis is `gsm.x_axis` (body→reference); a self-referencing star
collapses to a fixed world axis, so a per-star tail is **plugin-only** (patch
`Radiation.Gsm_space`).

| Field | Unit | Sun anchor | Derivation |
|---|---|---|---|
| `solar_cycle_yr` | yr | 11 | = `activity_cycle_yr` (Phase 2) directly. flat star → omit / very long (no modulation) |
| `astrosphere_standoff_au` | AU | ~120 | `120 · sqrt(Ṁ_rel) · (V_ISM,⊙ / V_ISM,star)` (ram-pressure balance, assuming v_wind = 400 km/s and common LIC density). Ṁ upper limit → standoff upper bound |
| `local_ism_inflow_speed_kms` | km/s | ~26 | V_ISM = \|v_star − v_LIC\|. Wood Table 1 where measured; else from 6D astrometry. Sets standoff + is the apex speed |
| `stellar_wind_speed_kms` | km/s | ~400 | assumed 400 (Wood) unless measured |
| `stellar_radiation_surface_relative_sun` | × Sun (1.0 ≡ 46.5 rad/h) | 1.0 | SEP/flare-driven crew dose ∝ activity. Inactive old dwarf ≲1; flare star (Proxima) ≫1. **R'HK underrepresents M-dwarf flares** — use flare/X-ray for M, R'HK for FGK. Confidence low–medium |
| `astrosphere_apex_ra_deg` / `_dec_deg` | deg | (nose ~ Sco/Oph) | upwind = −(v_star − v_LIC) from 6D astrometry; tail = opposite. **PLUGIN-ONLY** (stock cfg = sphere). >5 pc → LSR-relative fallback |

**Decisions-table presentation rule.** Every field above gets a row in each
host's Decisions table — never drop a row. The status lives in the value
cell: a *measured absence* is `none (...)` with a real confidence (τ Cet's
~50-yr flat record → `none (flat)`, high; a mere non-detection → `none (not
detected)`, low); a field with *no measurement at all* is `(unconstrained)`
with confidence `—`. "Omit" in the `solar_cycle_yr` derivation refers to the
emitted cfg axis, not the report row. One exception: a companion that shares
the representative's astrosphere (α Cen B) collapses the wind fields into a
single delegating `astrosphere` row, per the binary-layout principle.

Source priority:
1. Wood astrospheric Lyα paper (gives Ṁ + V_ISM + θ at once): α Cen / Proxima
   (Wood 2001/2005), ε Ind (Wood 2005), Barnard / τ Cet (Wood 2021 limits).
2. V_ISM + apex computed from the star's 6D astrometry vs the LIC flow vector
   (Lallement & Bertin 1992, ~26 km/s).
3. Ṁ from `mass_loss_measurements`; cycle from `activity_cycle_measurements`.
4. `radiation_surface` from activity level (interesting-first, Sun-anchored).

Worked example (ε Ind A): Ṁ = 0.5, V_ISM = 68 km/s → standoff =
120·√0.5·(26/68) ≈ 32 AU — a compact astrosphere, matching Wood's own
description. (α Cen: √2·(26/25) ≈ 1.5× solar ≈ 176 AU.)

Plugin note: `solar_cycle_yr`, `astrosphere_standoff_au`, and
`radiation_surface` are all stock-cfg-able (RadiationBody + a heliopause
pause). Only the **apex direction** needs the Harmony plugin — same pattern as
[[project-nearstars-flux-tube-plugin]] (custom C# for cfg-impossible aims).

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
`Rings { Ring { ... } }` block attached as a **direct child of the
star `Body`** (sibling to `ScaledVersion` and `Atmosphere`, NOT nested
inside `ScaledVersion`). This follows the ballisticfox/Kopernicus
convention documented in
[`.claude/skills/kopernicus-cfg/references/gas-giant.md`](../../kopernicus-cfg/references/gas-giant.md)
§ Rings.

This section maps Phase 3 Decisions fields (defined in
[`synthesis-template.md`](synthesis-template.md) § "Circumstellar
disk") to the Kopernicus Ring fields the emitter writes. Emitter must
also read the star's mean radius (from `stars[0].principia.mean_radius_km`)
to convert AU geometry into Kopernicus's body-radius-multiplier
convention.

| Phase 3 field | Kopernicus Ring field | Unit conversion | Notes |
|---|---|---|---|
| `disk_present` | (presence gate) | — | If false, omit the entire `Rings` block |
| `disk_inner_radius_au` | `innerRadius` | `(au × 1.495978707e8) / star_radius_km` | **Body-radius multiplier** (Kopernicus convention), not km |
| `disk_outer_radius_au` | `outerRadius` | same as inner | **Body-radius multiplier** |
| `disk_tint_rgb_hex` | `color` | hex → 4 floats `R,G,B,A` | `A` = `disk_opacity`; linear-space, 0–1 |
| `disk_opacity` | (alpha of `color`) | direct | — |
| `disk_imaging_inclination_deg` | `angle` | direct (degrees) | Ring tilt vs equatorial plane; emit only when `disk_resolved_imaging=true` |
| `disk_morphology` | (`steps` + `texture` path) | prose → texture variant | Single-ring → `steps=128` solid; multi-ring → higher steps + per-belt texture; asymmetric → custom texture; placeholder path under `NearStars-Textures/PluginData/<star>/disk_<belt>.dds` |
| `disk_planetesimal_belt_inferred` | (asteroid belt cfg, separate from Rings) | bool | If true, optionally emit a sparse `Asteroid` group at the disk midpoint; not part of the `Rings` block |
| `disk_dust_temperature_k` | (informational, drives `disk_tint_rgb_hex` synth) | — | Phase 3 step uses dust T to pick the hex; cfg writer just uses the hex |
| `disk_aspect_ratio` (or per-belt `disk_<belt>_aspect_ratio`) | (none — flat Ring) | — | Vertical scale-height ratio h = H/r. Kopernicus `Ring` is a flat annulus with **no thickness parameter**, so this is NOT emitted. Carried in the DB (`disks_curated` `aspect_ratio`) + Phase 3 for completeness + a future volumetric / Parallax disk renderer. Only the few resolved/edge-on disks have it (Fomalhaut cold ring 0.0175, AU Mic 0.031). |

Default Ring fields emitted with fixed values (per `gas-giant.md` § Rings template; not driven by Phase 3 sources):

- `longitudeOfAscendingNode = 0`
- `unlit = false`, `useNewShader = true`, `lockRotation = true`
- `penumbraMultipler = 1000.0`, `albedoStrength = 1`, `scatteringStrength = 1`, `anisotropy = 0.9`, `fadeoutMinAlpha = 1`
- `steps = 128` (single ring) or higher with per-belt finer divisions for multi-ring textures

**Multi-paper geometry merge**: when the `recommended: true` entry per belt has a null field (e.g. Su 2013 warm component lacks `outer_radius_au`; Sibthorpe 2010 supplies it from resolved imaging), the emitter falls back to non-recommended same-belt entries to fill null fields. The recommended entry stays canonical for its non-null fields.

**Multi-belt → one `Ring` per belt.** When the host has more than one belt
(Phase 3 `disk_belts` lists them; `disks_curated` has >1 distinct `belt`), emit
**one `Ring { ... }` node per belt inside the single `Rings { }` block**, reading
that belt's keyed fields. The table above applies per belt:
`disk_<belt>_inner_radius_au` → that Ring's `innerRadius`,
`disk_<belt>_outer_radius_au` → `outerRadius`,
`disk_<belt>_tint_rgb_hex` + `disk_<belt>_opacity` → that Ring's `color` (RGBA),
`disk_<belt>_imaging_inclination_deg` → `angle`. Each belt keeps its own tint, so
a warm inner belt and a cold outer belt render distinctly. Order the `Ring` nodes
inner→outer; each belt's geometry comes from its own `recommended:true`
`disks_curated` entry (same per-belt merge as above). A single-belt host emits one
`Ring` from the unsuffixed `disk_*` fields (unchanged). Texture paths stay per
belt: `…/PluginData/<star>/disk_<belt>.dds`.

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
[`phase3/kopernicus-emit-workspace/context-notes.md`](../../../../phase3/kopernicus-emit-workspace/context-notes.md)):
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
[`phase3/kopernicus-emit-workspace/context-notes.md`](../../../../phase3/kopernicus-emit-workspace/context-notes.md)
so the emitter can read Phase 3 Decisions directly without a sidecar
yaml indirection.

| Phase 3 field | Kopernicus Ring field | Unit conversion | Notes |
|---|---|---|---|
| `ring_present` | (presence gate) | — | If false, omit the entire `Rings` block |
| `ring_inner_au` | `innerRadius` | `(au × 1.495978707e8) / planet_radius_km` | **Body-radius multiplier** (Kopernicus convention), not km |
| `ring_outer_au` | `outerRadius` | same as inner | **Body-radius multiplier** |
| `ring_color_hex` | `color` | hex → 4 floats `R,G,B,A` | `A` = `ring_opacity`; linear-space, 0–1 |
| `ring_opacity` | (alpha of `color`) | direct | — |
| `ring_morphology` | (`steps` + `texture` path) | prose → texture variant | Single-ring → `steps=128`; multi-ring → higher steps + per-section texture; shepherded → divisions at shepherd-moon resonances |

Same nesting + default-field convention as the Circumstellar-disk
section above: `Rings { Ring { ... } }` is a **direct child of
`@Body[<planet>]`**, sibling to `ScaledVersion`. Default Ring fields
(`longitudeOfAscendingNode`, `unlit`, `useNewShader`, `lockRotation`,
`penumbraMultipler`, `albedoStrength`, `scatteringStrength`,
`anisotropy`, `fadeoutMinAlpha`) emit at the same fixed values per
`gas-giant.md`.

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
| `circumplanetary_disk_present` | (presence gate) | — | If false, omit the entire `Rings` block |
| `circumplanetary_disk_radius_planet_radii` | `outerRadius` | direct (already a multiplier) | Body-radius multiplier; planet-relative |
| `circumplanetary_disk_tint_rgb_hex` | `color` | hex → 4 floats `R,G,B,A` | Warmer (yellower) than debris disks due to dust T ~150–300 K |
| `circumplanetary_disk_opacity` | (alpha of `color`) | direct | Typically higher than debris (still actively accreting) |
| `circumplanetary_disk_dust_temperature_k` | (informational) | — | Drives tint synth |

Inner radius defaults to planet Roche limit unless cited explicitly
(emit as a low multiplier such as 1.2). Nesting + default fields per
the Circumstellar-disk section.
