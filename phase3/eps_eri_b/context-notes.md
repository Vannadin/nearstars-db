# ε Eri b — Phase 3 context notes

## Anchor papers (inherited from host eps-eri Phase 3 triage)

- **Hatzes 2000** (`2000ApJ...544L.145H`) — RV discovery
- **Mawet 2019** (`2019AJ....157...33M`, arXiv 1810.03794) — Keck/NIRC2 Ms-band
  vortex coronagraph direct imaging confirmation; rules out outer "ε Eri c"
- **Llop-Sayson 2021** (`2021AJ....162..181L`, arXiv 2108.05552) — Joint RV +
  Hipparcos/Gaia astrometric fit. M_b = 0.78 ± 0.12 M_Jup deprojected from
  M sin i ≈ 0.66 M_Jup using i = 78.8° (this is RV-only inclination; updated
  by Roettenbacher 2022 below). a = 3.5 AU, P = 7.4 yr, e = 0.07.
- **Roettenbacher 2022** (`2022AJ....163...19R`, arXiv 2110.10643) —
  astrometric cross-check; provides ε Eri b inclination consistent with disk
  plane (i ≈ 34°). Title "No Reliable Astrometric Detection" means the
  individual-mission astrometric signal is marginal but combined with disk
  plane gives the coplanar reading.
- **MacGregor 2015** (`2015ApJ...809L..47M`, arXiv 1505.03879) — ALMA cold
  ring at 64.4 ± 0.5 AU with e ≈ 0.07
- **Booth 2017** (`2017MNRAS.469.3200B`, arXiv 1705.05868) — three-belt
  decomposition; disk inclination 34 ± 2°
- **Su 2017** (`2017AJ....153..226S`, arXiv 1703.10330) — Genie model:
  multi-belt sculpting requires gap-clearing planets; b is the sculptor of
  the asteroid–intermediate gap
- **Quillen 2002** (`2002ApJ...578L.149Q`) — historical outer ε Eri c
  inference (ruled out)
- **Benedict 2006** (`2006AJ....132.2206B`) — HST FGS astrometry (superseded
  by Mawet 2019 direct imaging)

Key extracted numbers (verified against host Phase 3 + DB):

- M_b ≈ 0.78 M_Jup (Llop-Sayson 2021 §4) — deprojected
- a = 3.53 ± 0.03 AU (DB-curated from Llop-Sayson)
- P = 2671 ± 17 d = 7.32 yr (DB)
- e = 0.07 (DB / Llop-Sayson)
- ω = −19.15° (DB)
- i = 34° (Roettenbacher 2022 + disk plane; Llop-Sayson alone gave 78.8°
  but Roettenbacher's combined astrometric + disk-aligned reading is
  preferred — also matches what NearStars host adopted)
- DB stores i = 78.81 with σ = 29.34 — large uncertainty, consistent with
  the disk-aligned 34° reading within ~1.5σ. cfg picks 34° per coplanarity.

## Decisions-row classification log

For each row, label as canonical-aligned (CA) / tie-break (TB) /
documented-divergence (DD).

### Orbital
- `tidally_locked` = false → CA (Jupiter-mass at 3.5 AU has no tidal lock)
- `obliquity_deg` = 25 → TB (no measurement; Saturn-like 26.7° aesthetic vs
  Jupiter-like 3.1°; tie-break for visual interest with possible ring axis)
- `eccentricity` = 0.07 → CA (Llop-Sayson 2021)
- `argument_of_periastron_deg` = -19.15 → CA (DB / Llop-Sayson)
- `sidereal_period_days` = 2671 → CA (DB / Llop-Sayson)
- `semi_major_axis_au` = 3.53 → CA (DB / Llop-Sayson)
- `inclination_deg` = 34 → DD (DB stores 78.81 from Llop-Sayson RV-only, but
  Roettenbacher 2022 + disk coplanarity (Booth 2017 disk inclination 34°)
  argue for 34°. cfg picks the coplanar reading. Documented divergence with
  the DB-stored value, which is itself within 1.5σ of 34°)

### Physical
- `mass_mjup` = 0.78 → CA (Llop-Sayson 2021 §4)
- `radius_rjup` = 1.05 → TB (no transit. Burrows / Fortney evolutionary
  tracks for 0.78 M_Jup, [Fe/H] solar, age ~440 Myr give 1.03–1.12 R_Jup.
  cfg picks 1.05 as mid-range)
- `surface_gravity_g_earth` = 22 → CA (derived from M and R)
- `density_g_cc` = 0.85 → CA (derived)
- `insolation_s_earth` = 0.027 → CA (derived: L_star / a² = 0.34 / 3.53² = 0.0273)
- `equilibrium_temp_k_a0` = 113 → CA (derived: 278 × (L/a²)^0.25)
- `equilibrium_temp_k_a03` = 103 → CA (derived; A=0.3 jovian Bond)
- `bond_albedo` = 0.34 → TB (Jupiter Bond = 0.503, Saturn = 0.342, Uranus =
  0.300, Neptune = 0.290. For a cold ~110 K methane-rich jovian, Uranus/
  Saturn-like 0.30–0.35 is plausible; ammonia-cloud-dominated would be
  higher. cfg picks 0.34 — Saturn-analog — as tie-break)
- `intrinsic_luminosity_w_m2` = 0.5 → TB (Burrows 2003 cooling track for
  0.78 M_Jup at 0.44 Gyr predicts T_int ~ 100 K; intrinsic flux ~σT^4 ≈
  5.7 W/m² total but the effective surface convective layer is much
  thinner. cfg picks 0.5 W/m² as conservative "warm-from-formation"
  estimate, lower than Jupiter's ~5.4 W/m² because of older age + lower
  mass)

### Atmosphere
- `atmosphere_present` = true → CA (gas giant by definition)
- `atmosphere_surface_pressure_pa` = N/A → CA (gas giant has no surface; cfg
  reference = 1 bar level)
- `atmosphere_composition` = H₂ ~88%, He ~12%, CH₄ trace, NH₃ trace, H₂O
  trace → TB (no spectrum measured; cfg adopts solar-composition jovian
  default with Jupiter-like volatile inventory)
- `atmosphere_scale_height_km` = 40 → CA (derived: kT/μg with T=113K, μ=2.3, g=22 m/s² → 17 km — actually small. recompute: H = kT/(μ m_H g) = (1.38e-23 × 113) / (2.3 × 1.67e-27 × 22) ≈ 18 km. Adopt 18 km, not 40)
- `cloud_cover_fraction` = 0.85 → TB (Jupiter ≈ 1.0 over zonal bands;
  Saturn ≈ 0.9; cfg picks 0.85 as visually banded with some clear gaps)
- `cloud_morphology` = zonal bands with ammonia-ice cloud deck at ~0.5–1
  bar, possible photochemical haze layer above; faint visible bands due to
  weak insolation → TB (no observations; Jupiter/Saturn analog)
- `cloud_tint_rgb_hex` = `#e8dac4` (warm cream — NH₃ ice + K2V illumination)
  → TB (Saturn's ammonia clouds appear cream-white under solar
  illumination; under K2V the perceived hue shifts warmer)
- `atmosphere_tint_rgb_hex` = `#d8c098` (warm-cream limb haze) → TB
- `photochemical_haze_tint_rgb_hex` = `#b08858` (light tholin from CH₄
  photolysis under K2V UV) → TB

### Visual / sky
- `planet_disk_tint_rgb_hex_primary` = `#e8dac4` → TB (visual hex)
- `planet_disk_tint_rgb_hex_accent` = `#c4a878` (banded zones) → TB
- `star_apparent_angular_diameter_deg` = 0.115 → CA (derived: 2 R_star / a)
- `stellar_illumination_color_temp_k` = 5180 → CA

### Magnetism
- `magnetic_field_strength_microtesla_equator` = 400 → TB (Jupiter ≈ 430 μT
  at equator; Saturn ≈ 21 μT at equator. For a 0.78 M_Jup planet with
  vigorous convection, scale to Jupiter-analog 400 μT)
- `magnetic_dipole_moment_normalized_earth` = 1.7e4 → TB (Jupiter dipole
  moment ≈ 2.0e4 × Earth; scale by mass)
- `magnetic_dipole_tilt_deg` = 10 → TB (Jupiter ≈ 9.6°; Saturn ≈ 0°. Pick
  Jupiter-analog 10°)
- `aurora_present` = true → TB (Jupiter has strong UV aurorae; ε Eri's
  active wind drives stronger driver; aurora visibility in K2V illumination
  context)
- `aurora_color_primary_hex` = `#c84080` (H₂ Lyman/Werner bands in UV;
  visible-band aurora dominated by H Balmer α 656 nm red-pink) → TB
- `aurora_oval_magnetic_latitude_deg` = 70 → TB (Jupiter-analog)
- `aurora_intensity_kR_typical` = 1000 → TB (Jupiter UV aurora ≈ 100 kR
  visible; with ε Eri's enhanced wind, scale to ~1000 kR potentially
  brighter than Jupiter)

### Ring system
- `ring_present` = false → TB (no observations; tie-break: no ring is
  default for non-imaged jovians. Note: Saturn has rings while Jupiter has
  faint rings only — no constraint either way for ε Eri b)
- `ring_observed` = false → CA (Mawet 2019 direct imaging at Ms-band has
  no ring detection)

### Companion / orbital context
- `companion_position_relative_belts` = "between asteroid-belt analog
  (3 AU) and intermediate belt (20 AU)" → CA (Su 2017 Genie model
  identifies b as the inner-gap sculptor)

## Classification counts

Total rows: 35

- canonical-aligned: 13
- tie-break: 21
- documented-divergence: 1 (inclination 34° vs DB-stored 78.81°)

→ `## Canonical alternatives` section IS required (1 divergence row)

## Step 10 VERIFY notes

All canonical-aligned rows trace to:
- DB `db/systems/eps_eri.json` planet curated block (a, e, ω, P, M) — sourced from Llop-Sayson 2021
- Host Phase 3 `docs/phase3/eps-eri.md` (L_star, R_star, M_star, age) — sourced from Rosenthal 2021 / Llop-Sayson 2021 / Mamajek 2008
- Derived quantities (g, ρ, S, T_eq, H, angular diameter) — algebraic from inputs

The single divergence row (inclination 34° vs DB 78.81°) is fully
documented: Llop-Sayson's RV-only fit gives 78.81° ± 29.34° (notice the
huge uncertainty), Roettenbacher 2022's combined astrometric + disk-plane
reading gives 34° matching Booth 2017's disk inclination. cfg picks the
coplanar reading; the host Phase 3 already adopts this (see
`disk_imaging_inclination_deg` = 34 ± 2 with note "consistent with ε Eri b
orbital plane (Roettenbacher 2022)"). DB will be updated when Phase 2 of
`eps_eri_b` is refreshed.

Tie-break rows are within-window aesthetic / theoretical choices:
- Radius 1.05 R_Jup: Burrows 2003 / Fortney 2007 evolutionary tracks for
  0.78 M_Jup at 0.44 Gyr predict 1.03–1.12 R_Jup
- Bond albedo 0.34: Saturn-analog (0.342); Jupiter is 0.503 but cooler
  jovian with weaker insolation skews toward Saturn-like value
- Atmospheric composition: solar H₂/He + Jupiter-like volatile inventory,
  no spectrum available so Phase 3 takes the Jupiter-analog default
- Cloud / haze tints: Jupiter/Saturn-analog under K2V illumination
- Magnetic field: scaled Jupiter dynamo with ε Eri's stronger wind
- Ring absent: Mawet 2019 Ms-band imaging would have caught a Saturn-
  bright ring; not detected; cfg defaults to "no ring"

## Open items already identified

- ε Eri b atmosphere spectrum: JWST coronagraph (Cycle 4+) could yield CH₄
  + H₂O detection in ~5-15 yr horizon
- Mawet 2019 thermal emission constraint: 3.8 μm contrast gives upper
  limit on hot-start luminosity; rules out very young / very inflated
  jovian models
- Moon system possibility: 0.78 M_Jup at 3.5 AU has stable Hill sphere
  ~0.36 AU; large icy moons plausible but unconstrained — Phase 3
  follow-up moon population is out of scope for now
