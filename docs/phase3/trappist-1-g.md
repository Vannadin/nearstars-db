<!-- TRAPPIST-1 g Phase 3 synthesis: cfg-ready decisions and reasoning -->
# TRAPPIST-1 g — Phase 3 Synthesis

TRAPPIST-1 g is a 1.13 R⊕, 1.32 M⊕ rocky planet on a 12.35-day orbit
around an M8V ultra-cool dwarf. Sixth planet out, receiving 0.26×
Earth's insolation — well beyond the conservative habitable zone. The
largest of the TRAPPIST-1 planets, and one of the most water-rich:
Bourgeois 2024 (2008.09599) magma-ocean evolution gives a water mass
fraction of 0.11–0.24, the highest in the system. No JWST observations
of g have been published as of 2026-05-21; the observational picture
is dominated by HST haze limits (Moran 2018) and theoretical climate
modeling (Lincowski 2018, Wolf 2017).

**Scenario choice for NearStars: globally ice-covered ocean world
with a very thin CO₂ atmosphere (~0.05 bar), no substellar open
water, sub-glacial liquid-water ocean.** This is the canonical
snowball / "ocean world" scenario for the cold outer-HZ planet. Even
elevated CO₂ greenhouse cannot keep surface liquid water at g's
insolation level (Wolf 2017 §5 finds complete snowball below
~0.3 S⊕). The thick global ice cover hides a substantial sub-glacial
liquid-water layer maintained by basal melting from radiogenic heat.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 12.35 d orbit, tidal damping; Agol 2021 |
| `obliquity_deg` | 0 | high | tidal damping; Agol 2021 |
| `eccentricity` | 0.00208 | high | Agol 2021 TTV (lowest in system) |
| `argument_of_periastron_deg` | 191 | medium | Agol 2021 (very low ecc → weak constraint) |
| `sidereal_period_days` | 12.3524 | high | Agol 2021 |
| `semi_major_axis_au` | 0.04683 | high | Agol 2021 |
| `mass_mearth` | 1.321 | high | Agol 2021 TTV |
| `radius_rearth` | 1.129 | high | Agol 2021 |
| `surface_gravity_g_earth` | 1.036 | high | derived = 1.321 / 1.129² |
| `density_g_cc` | 5.06 | high | Agol 2021 |
| `water_mass_fraction` | 0.11–0.50 | medium | Bourgeois 2024 (0.11–0.24); Unterborn 2018 inward-migration model gives upper bound ≥50 wt% — highest in system either way |
| `insolation_s_earth` | 0.26 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 194 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.6, snowball) | 154 | high | derived; high-albedo snowball |
| `bond_albedo` | 0.55 | medium | snowball ice + thin atmo; Wolf 2017 cold-snowball |
| `surface_temp_substellar_k` | 200 | medium | Wolf 2017 cold-snowball; basal-melt isolated from surface |
| `surface_temp_nightside_k` | 130 | medium | Wolf 2017 GCM; cold-trap nightside |
| `surface_temp_global_mean_k` | 175 | medium | Wolf 2017 cold-snowball mean |
| `atmosphere_present` | true (very thin CO₂) | medium | Moran 2018 rejects H₂-rich; outgassing-driven thin CO₂ |
| `atmosphere_surface_pressure_pa` | 5 000 | medium | 0.05 bar — below Turbet 2018 (1707.06927) stable equilibrium of 150 mbar for pure CO₂ at 174 K; non-equilibrium escape-balanced state assuming ongoing volcanic outgassing. At ≥150 mbar the atmosphere becomes self-sustaining; at <0.01 bar the planet is essentially airless. |
| `atmosphere_composition` | CO₂ 90%, N₂ 8%, trace H₂O, Ar | medium | volcanic outgassing without liquid-water carbonate-silicate cycle |
| `atmosphere_scale_height_km` | 4.5 | medium | derived: kT/μg with T≈180 K, μ=43, g=10.2 m/s² |
| `atmosphere_tint_rgb_hex` | `#403028` (negligible Rayleigh + CO₂ ice haze tint) | low | very thin atmo, minimal scattering |
| `cloud_cover_fraction` | 0.10 | medium | very limited — only CO₂ ice cirrus at terminator |
| `cloud_tint_rgb_hex` | `#d0c0b0` (CO₂ ice + dust, M-dwarf shifted) | medium | minimal cloud production in cold thin atmo |
| `ocean_present` | true (sub-glacial only, no surface expression) | medium | Bourgeois 2024 wmf 0.11–0.24 + Earth-analog radiogenic heat → basal melt likely |
| `ocean_extent_substellar_radius_deg` | 0 | high | full snowball; Wolf 2017 §5 |
| `ocean_tint_rgb_hex` | n/a (hidden under ice) | high | not surface-visible |
| `surface_ice_caps` | 100% global coverage | high | full snowball; Pierrehumbert 2011 outer-HZ branch |
| `surface_tint_rgb_hex_primary` | `#e8e0d4` (clean snow under M-dwarf light) | medium | high-albedo snow + 2566 K illumination |
| `surface_tint_rgb_hex_accent` | `#a09080` (CO₂ frost / dust patches at terminator) | low | sublimation-deposition cycle near terminator |
| `surface_morphology` | global glacial ice; tectonic stresses from differential rotation → pressure ridges; possible cryovolcanism at warm spots | medium | Wolf 2017 + Europa-Ganymede analog reasoning |
| `magnetic_field_present` | uncertain (possibly active from interior hydrosphere convection) | low | non-trivial wmf could sustain dynamo from internal mantle convection |
| `induction_heating_w_m2` | 0.002–0.02 | medium | Grayver 2022 — drops with distance |
| `tidal_heating_w_m2` | 2×10⁻⁷–0.001 | medium | Hay & Matsuyama 2019 — eccentricity-forced Maxwell-body surface flux ~2×10⁻⁷ W/m², Andrade rheology somewhat higher; g uniquely receives 2–20% from planet-planet tides (mostly f) |
| `xuv_flux_at_planet_F_earth` | ~120 (current) | high | Berardo 2025 (2506.12140) — revised L_XUV = 1.83×10²⁸ erg/s, 30× higher than 2017 estimates |
| `stellar_microflare_cadence_min` | 45 | high | Berardo 2025 — 10²⁹ erg microflares every ~45 min; 10³⁰ erg flares every 6 hours (JWST) |
| `radiogenic_heat_w_m2` | 0.04 | medium | Earth-analog mantle radiogenics |
| `magnetic_field_strength_microtesla_equator` | 10 | low | RM22 (2203.01065) scaling; 1.32 M⊕ (largest in system) supports active dynamo |
| `magnetic_dipole_moment_normalized_earth` | 0.35 | medium | RM22 + 2208.06523 (Earth-class core extends dynamo lifetime) — interior hydrosphere convection may also contribute |
| `magnetic_dipole_tilt_deg` | 12 | low | Tie-break: 12° offset for distinctive auroral cap |
| `magnetosphere_standoff_planet_radii` | 4 | medium | Garraffo 2017 Fig. 4 — outer planets less compressed than b/c; 4–5 R_p plausible at g's orbit |
| `radiation_belt_present` | true | medium | B-field sufficient + outer-planet wind less crushing |
| `surface_radiation_dose_msv_yr` | 5000 | high | Atri 2019 (1910.09871) Table 6 for g at 0.045 AU + 50 g/cm² shielding + B-field |
| `atmospheric_shielding_g_cm2` | 50 | medium | Phase 3 cfg pressure 0.05 bar → ~50 g/cm² column |
| `aurora_present` | true | high | Atm + B-field both supportive; CO₂-dominated emission |
| `aurora_color_primary_hex` | `#FF6B6B` | medium | CO₂⁺ Fox–Duffendack 600 nm red (Mars-analog snowball atmosphere); tie-break: red visible over UV-only |
| `aurora_color_secondary_hex` | `#87CEEB` | low | Trace N₂⁺ emission if present; otherwise scattered-UV perception as pale blue |
| `aurora_emission_species_primary` | `CO₂⁺ UV doublet 289 nm + CO Cameron bands` | medium | Mars-analog with snowball-thin CO₂ atm |
| `aurora_oval_magnetic_latitude_deg` | 58 | medium | Vidotto 2013 with R_mp ~4 R_p → α ≈ 30°, oval lat ~60° |
| `aurora_intensity_kR_typical` | 60 | low | Fraschetti 2019 proton flux at g's distance — moderate enhancement over Earth |
| `star_apparent_angular_diameter_deg` | 1.36 | high | derived: 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## Surface synthesis

TRAPPIST-1 g sits well outside the conservative habitable zone at
0.26 S⊕. Wolf 2017 §5 finds that even 10 bar CO₂ does not produce a
sustained open ocean at g's insolation under realistic atmospheric
escape constraints — the cold trap is too efficient. Lincowski 2018
similarly classifies g as a snowball in all considered atmospheric
compositions.

The redeeming geological feature is g's very high water mass
fraction. Bourgeois 2024 (2008.09599) finds wmf 0.11–0.24 for g —
the highest in the TRAPPIST-1 system, corresponding to 20–50 Earth
oceans of water. Most of this resides as a sub-glacial liquid-water
ocean (basal-melted by Earth-analog radiogenic heat at the ice-rock
interface, ~0.04 W/m²) overlain by a thick (~50–100 km) global ice
cover. Cryovolcanism (Europa / Ganymede analog) is plausible but
unconstrained.

For the surface morphology, the snowball template gives:

- **Substellar to ~30° from substellar:** thinnest ice (~30 km) due
  to slightly elevated insolation; possible tectonic activity from
  ice-flow toward the colder terminator and nightside.
- **Mid-zone (30–120° from substellar):** thick ice (~60 km),
  smooth at large scale.
- **Terminator (~90°):** highest pressure-ridge density, longest
  topographic shadows.
- **Nightside (>120°):** thickest ice (~100 km), with possible
  CO₂ frost deposits in the coldest regions.

**Color choice.** Clean snow / glacial ice albedo under M-dwarf
illumination: warm cream-white `#e8e0d4` primary, with tan-shaded
patches `#a09080` near the terminator from accumulated dust and
CO₂ frost cycling.

**Habitability caveat at upper water mass fraction.** Acuña 2021
(2101.08172) finds that at WMF ≥ 0.14, high-pressure ice phases
(HPPs) seal off the rock-water interface in the hydrosphere,
preventing nutrient exchange that's typically considered necessary
for subsurface ocean habitability. At WMF ≥ 0.10, less than 50% of
interior configurations enable a habitable sub-surface ocean. g's
wmf range (0.11–0.50) straddles this threshold — the sub-glacial
ocean exists but its habitability potential degrades at the upper
bound. For visual cfg this is not a rendering concern, but it's
worth noting in the Open items as a Principia / astrobiology-relevant
flag.

**Cryovolcanic warm spots as a canonical visual feature.** g's high
water mass fraction (0.11–0.50) combined with radiogenic + tidal
heating gives a substantial sub-glacial ocean (basal melt at
~0.04 W/m²) under a thick (50–100 km) ice shell. Europa-Ganymede
analog reasoning supports the possibility of cryovolcanism at
locations where the ice shell is thinnest — typically over
warm-mantle anomalies that allow basal water to reach the surface.
Per the interesting-first rule, the cfg promotes
cryovolcanic plumes from "possible" to **canonical**: visible plumes
near 2–4 substellar warm spots, each ~50–100 km across, producing
fresh-water-ice halos around their venting sites. This is
observation-consistent (no direct evidence either way) and
dramatically more interesting than a uniform ice surface. The
cfg-variant alternative is preserved: a featureless smooth snowball.

**Bedrock / iron oxide.** Essentially none visible — the global ice
cover is too thick for any bedrock exposure. Possible exception at
extreme terminator ridge tops where pressure-driven thinning could
expose dark patches; very low probability and not visible from orbit.

**Morphology under tidal lock.** Ice circulation is gentle due to
the minimal insolation gradient (substellar-to-antistellar
difference of only ~70 K). Tectonic activity is dominated by
basal-melt-driven convection in the ice shell (cf. Europa) rather
than by surface sublimation/deposition. The result is a
geologically active ice surface with cryovolcanic features at warm
spots — visually subtle but distinguishing g from a "dead snowball."

## Atmosphere synthesis

No published JWST observations of g exist. The HST haze limit
analysis (Moran 2018, 1810.05210) excludes cloud-free hydrogen-rich
atmospheres; secondary atmospheres are not constrained by HST.

Theoretical models converge:

- **Wolf 2017:** full snowball at g's insolation; even ~10 bar CO₂
  insufficient for liquid water.
- **Lincowski 2018:** g classed as "snowball" or "post-runaway
  O₂-rich" depending on initial water inventory.
- **Bourgeois 2024:** magma-ocean phase produces ~10 bar O₂ + CO₂
  atmosphere initially; most is lost over the system's age via
  hydrodynamic escape and surface oxidation.

For NearStars we adopt **0.05 bar CO₂-rich thin atmosphere**:

- **Pressure** 0.05 bar (5 kPa). Below the threshold needed for
  cloud formation at g's temperatures; thin enough that the
  surface communicates radiatively with space at most wavelengths.
  Above 0 because volcanic outgassing without a CO₂ sink (frozen
  surface → no carbonate-silicate weathering) should accumulate
  modest CO₂.
- **Composition** CO₂-dominated (90%), N₂ (8%), trace H₂O / Ar.
  CO₂ richness reflects outgassing accumulation; H₂O is trace
  because of the cold-trap.
- **Clouds.** Minimal (~10% global): only CO₂ ice cirrus at the
  terminator + nightside cold-trap.

**Caveat — atmosphere retention.** Van Looveren 2024 (2401.16490)
finds that at g's ~120 F_EUV,⊕ (revised upward from earlier estimates
by Berardo 2025 / 2506.12140, who measured L_XUV = 1.83×10²⁸ erg/s,
30× higher than 2017 values), CO₂ atmospheres are lost at roughly
**1 bar per 5 Myr** under Jeans escape alone. Even a 100 × Earth
atmosphere would be lost in tens of Myr. The 0.05 bar choice is
therefore **optimistic** and assumes ongoing volcanic replenishment.
A 0.01 bar / fully airless variant is preserved as a cfg backup. The
stellar microflare cadence (~10²⁹ erg every 45 min, per Berardo 2025
HST Ly-α multi-year monitoring) further stresses retention but does
not directly drive the cfg pressure.

**Turbet equilibrium reference.** Turbet 2018 (1707.06927) explicitly
solves the CO₂ atmosphere equilibrium for g: at 150 ± 1 mbar surface
pressure and 174 ± 0.1 K, the atmosphere is in stable
sublimation-condensation balance. Below this, CO₂ ice covers the
surface "potentially as much as the entire surface" and the
atmosphere is unstable to collapse. The cfg's 0.05 bar choice is
below this equilibrium and assumes a non-equilibrium state maintained
by continuous volcanic outgassing — physically reasonable but not the
natural attractor. An alternative cfg variant could adopt the Turbet
equilibrium pressure (0.15 bar) for a more thermodynamically
self-consistent atmosphere.

**Sky appearance.** The 0.05 bar atmosphere is barely visible from
orbit. From the surface, the sky is near-black with the host star
appearing as a deep red-orange disk against the void. CO₂ ice
clouds catch grazing light at the terminator as faint cream wisps.

**GCM cross-check.** Fauchez 2019 (1911.08596) confirms the snowball
state for g at all plausible CO₂ pressures ≤10 bar: even at 10 bar
CO₂, the planet is "almost fully ice-covered except at a few spots
near the substellar region where some water can evaporate from the
ocean and form relatively thin clouds (~0.1 kg/m²)." The cfg's
full-snowball default is well-supported.

**Aurora geometry over the ice.** With a moderate B-field (~0.35 ×
Earth) and a thin CO₂-rich atmosphere, g hosts Mars-analog auroras at
magnetic latitude ~58°. The dominant emission is CO₂⁺ red bands
(Fox–Duffendack at ~600 nm), giving a distinctive red auroral band
crossing the high-latitude ice. Intensity ~60 kR (~6× Earth) is
moderate but visible against the dark snowball surface; cfg renders
this as a `#FF6B6B` primary band with optional `#87CEEB` secondary
tint where trace nitrogen contributes. The auroral oval is wider than
Earth's, expanding equatorward toward ~50° during sub-Alfvénic
transits; players in equatorial regions can see the aurora as a glow
on the northern/southern horizon.

## Rotation & spin synthesis

Tidal damping at 12.35 days over 7.6 Gyr → synchronous (1:1)
configuration. Obliquity damped to zero. Eccentricity is 0.00208 —
the lowest in the system, deep inside the 3:2 stability boundary
(only 1:1 plausible).

**KSP implementation note.** Rotation period = orbital period =
12.3524 days (1 067 251 s).

**No seasons.** Obliquity = 0; libration-induced insolation
variation < 0.2% (lowest in system). Substellar point is fixed.

**Planet-planet tides.** Hay & Matsuyama 2019 (1903.04501) identifies
g as the planet that experiences the most significant **planet-planet
tidal heating relative to its eccentricity-forced tides** (2–20% of
total, mostly from neighbor f). For all other planets in the system
the planet-planet contribution is <1%. The absolute magnitude is
still small (~2×10⁻⁷ W/m² surface flux for a Maxwell-body rheology),
but the relative dominance of f's gravitational influence is unique
to g — a faithful annotation for the Principia cfg.

**Magnetic dynamo expectation.** g is the most massive TRAPPIST-1
planet (1.32 M⊕) and has the highest water mass fraction (Bourgeois
2024 + Unterborn 2018), supporting both a metallic core dynamo and
possibly a separate hydrosphere convection contribution. RM22
(2203.01065) scaling places g at ~0.35 × Earth dipole moment despite
the 12.4-day slow rotation. Garraffo 2017 finds outer planets less
compressed by stellar wind, giving g a relatively well-organized
magnetosphere with standoff at ~4 R_p. The Kerbalism cfg assumes
closed-magnetosphere radiation belts at 1.5–4 R_p.

## Visual styling

- **Global appearance.** Near-uniform warm cream-white snowball
  (`#e8e0d4`) with subtle tan tinting near the terminator
  (`#a09080`). No obvious "eyeball" feature — no open-water disk.
  The most visually subdued planet in the system.
- **Substellar region.** Slightly more textured / fractured ice
  due to tectonic ice-flow toward colder zones. Possible
  cryovolcanic features as bright fresh-ice patches.
- **Mid-zone and terminator.** Pressure ridges, crevasses, and
  long topographic shadows under grazing 2566 K illumination.
  Terminator is the most photogenic zone.
- **Nightside.** Slightly darker cream-tan from CO₂ frost. KSP
  nightside ambient ≈ 1–3% dayside.
- **Atmosphere haze.** Imperceptible from orbit; barely a hairline
  warm-gray glow (`#403028`) at the limb.
- **Cryovolcanic plumes.** 2–4 substellar warm spots produce
  ~50–100 km-wide plumes of fresh water ice ejected into the thin
  atmosphere. Each plume forms a bright halo around its vent,
  visible from orbit as small bright patches against the snowball.
  Plumes are intermittent (timescales hours-days) so KSP rendering
  should treat them as static features for fidelity.
- **High-latitude aurora band.** A `#FF6B6B` red CO₂⁺ aurora at
  ~58° magnetic latitude, visible against the dark nightside ice.
  The aurora intensity peaks during stellar-wind sub-Alfvénic
  transits (50–80% of each orbit per Garraffo 2017).
- **Star in sky.** TRAPPIST-1 subtends 1.36° in g's sky (2.7× the
  Sun from Earth). Surface illumination is 0.26 S⊕ — comparable to
  outer Mars's solar flux. The red-orange star against the cream
  snowscape gives a permanent dim-dawn quality. Stellar surface
  heterogeneity matters for the realistic sky tint. Wakeford 2019
  (1811.04877) finds a 3-temperature spot model best fits TRAPPIST-1:
  64% photosphere at 2400 K, 35% spot coverage at 3000 K, 1% facula
  at 5825 K. The dominant disk color is set by the 2400 K cool
  photosphere (already cfg's `stellar_illumination_color_temp_k`
  value of 2566 K from Agol 2021); the 35% 3000 K coverage adds a
  subtle yellow-orange overtone to the disk at high resolution.
- **Sister planets in sky.** f (next inward) at angular size ~0.3°
  in conjunction; h (next outward) at ~0.2° at outer conjunction.
  Resonant chain ensures frequent multi-planet alignments.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2008.09599** Bourgeois 2024 — Magma ocean evolution for e/f/g.
  Establishes g as the most water-rich planet in the system (wmf
  0.11–0.24). Drives the sub-glacial ocean cfg.
- **2412.10192** Cherubim 2024 — From CO₂- to H₂O-dominated
  atmospheres in magma ocean phase. Provides composition framework
  for g's evolved atmosphere.
- **1809.07498** Lincowski 2018 — Evolved climates of TRAPPIST-1
  worlds. g classified as snowball in all considered scenarios.
  Already read for d/e/f phase 3.
- **2504.19872** Castan-Lopez 2025 — Cosmic Shoreline Revisited.
  g's position relative to the empirical M-dwarf atmospheric
  retention line: likely retains a thin atmosphere but not a
  thick one.
- **1810.05210** Moran 2018 — HST haze limits. Rejects cloud-free
  H₂-rich for inner 5 planets (including g indirectly). Already
  read for d Phase 3.
- **1706.02689** Unterborn 2018 — Inward-migration interpretation of
  TRAPPIST-1 densities. Argues g and f have ≥50 wt% water/ice — a
  much higher water-content upper bound than Bourgeois 2024's 0.24.
  Drives the upward revision of `water_mass_fraction` to 0.11–0.50.
- **1903.04501** Hay & Matsuyama 2019 — Tides between TRAPPIST-1
  planets. g uniquely receives 2–20% of its tidal heating from
  planet-planet interactions (mostly f); all other planets <1%.
  Drives the new Rotation section paragraph.
- **2401.16490** Van Looveren 2024 — Airy worlds or barren rocks?
  Quantitative atmospheric escape under Jeans escape. At g's ~120
  F_EUV,⊕, CO₂ atmospheres are lost at ~1 bar per 5 Myr. Drives the
  new "atmosphere retention caveat" paragraph and the alternative
  cfg variants.
- **2506.12140** Berardo 2025 — HST multi-year Ly-α monitoring of
  TRAPPIST-1. Revised L_XUV = 1.83×10²⁸ erg/s (30× higher than 2017
  estimates). Microflare cadence ~10²⁹ erg every 45 min. Drives
  the new XUV and microflare entries in the decisions table.
- **1912.05749** Hori & Ogihara 2020 — Hydrogen-rich atmosphere
  origin. g's maximum primordial H atmosphere ≤ 2 wt%, lost within
  several 100 Myr. Confirms the present-day atmosphere is secondary.
- **1707.06927** Turbet 2018 — Climate diversity modeling for
  TRAPPIST-1 planets. Drives the atmosphere equilibrium reference
  (150 mbar at 174 K for pure CO₂ on g) and confirms the snowball
  state at all plausible pressures.
- **2101.08172** Acuña 2021 — Hydrosphere characterization. Validates
  g's sub-glacial ocean architecture (ice Ih over high-pressure ices
  over rocky mantle). Identifies the WMF ≥ 0.14 habitability
  threshold (HPPs seal off rock-water interface).
- **1911.08596** Fauchez 2019 — Clouds and hazes modeling. Confirms
  g's snowball state even at 10 bar CO₂; only minimal substellar
  cloud formation.
- **1811.04877** Wakeford 2019 — HST transmission of g + 3-temperature
  stellar model. Provides the canonical spot-coverage values
  (64:35:1 at 2400/3000/5825 K). Refines stellar sky color predictions.
- **1706.04617** Garraffo 2017 — Threatening Magnetic and Plasma
  Environment of TRAPPIST-1. Outer-planet magnetopause geometry.
- **2203.01065** RM22 — Rocky-planet dynamo scaling for tidally-locked.
- **1910.09871** Atri 2019 — Surface-dose tables for g.

### Read (context / methodology, not decision-driving)

- **2508.12865** Empirical determination of the Cosmic Shoreline.
  Context for g's retention status.
- **2504.01182** Receding Cosmic Shoreline for mid-to-late M dwarfs.
  TRAPPIST-1 system-level context.
- **2210.02484** HZ catalog. Lists g as one of the wider-HZ candidates.
  Already read for d.
- **2006.11349** Wunderlich 2020 — Wet/dry e and f. g context only.
  Already read for f.
- **2506.16063** Mass-radius plane classification. Catalog context only.

### Read (instrument-only, not visual-informative)

(None specific to g.)

### Not read — no arXiv preprint or low-priority (~14 papers)

The g bibliography is large (66 papers, 52 with arXiv) but most
papers are SETI / technosignature surveys, mass-radius catalogs,
or works that mention g only in passing.

- **2509.06310** Deep SETI search with FAST. Not visual.
- **2208.02511** SETI drift rate context. Not visual.
- **Multiple cosmic-shoreline papers** — collectively read for the
  retention question; individual entries not visual-informative.
- **TESS / non-TRAPPIST-1 catalog papers** — irrelevant.

---

## Open items for follow-up

- No direct JWST observation of g exists yet; if a future
  transmission or emission spectrum is published, the atmosphere
  pressure / composition table should be revisited. Particularly
  if g shows any CO₂ feature in transmission, the 0.05 bar choice
  could be refined.
- Cryovolcanism is plausible but unconstrained for g. If a future
  cfg variant wants to emphasize the Europa-analog aspect (visible
  resurfaced ice patches, possible plume features at warm spots),
  it could be implemented as Phase 3.5.
- The 0.05 bar CO₂ choice is at the lower edge of "atmosphere
  present" — could be reduced to ~0.01 bar or set to zero for a
  fully airless cold-snowball variant.
- The wmf range (0.11–0.24) is high enough that g could plausibly
  host an habitable sub-glacial layer with hydrothermal activity at
  the seafloor (Europa-Enceladus astrobiology analog). Worth a
  Principia note even if not visually relevant.
- The 0.05 bar atmosphere is below the Turbet equilibrium 150 mbar.
  A cfg variant at 0.15 bar would be more thermodynamically natural.
  Choice depends on whether NearStars prefers "active outgassing
  equilibrium" (Turbet) or "atmosphere just hanging on against
  escape" (current).
- WMF upper-bound habitability constraint: at 0.14+, HPPs seal off
  mantle-ocean exchange. If the Principia-side astrobiology pass
  cares about habitability, flag g as marginal at the upper bound.
- JWST GO 2589 observed g for flare characterization (per Burdanov
  2025 / 2512.04265) but no atmosphere retrieval has been published.
  Worth re-checking arXiv periodically for follow-up papers.
- **Cfg variant: uniform smooth snowball.** Preserved as alternative
  — for users who prefer the no-active-features reading. The
  cryovolcanic-plumes canonical version was chosen per
  interesting-first rule.
- Surface radiation dose ~5 Sv/yr places g in Kerbalism's
  "moderate-to-high" radiation bracket. With substantial ice
  shielding (50 g/cm² atmospheric + ~30 m of ice), interior
  habitats (under the ice) would actually be among the safest in
  the system.
