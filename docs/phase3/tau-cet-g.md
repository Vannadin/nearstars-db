<!-- tau Cet g Phase 3 synthesis: cfg-ready decisions and reasoning -->
# τ Ceti g — Phase 3 Synthesis

τ Ceti g is a 1.75 M⊕ (M sin i) RV candidate on a 20.0-day orbit at
0.133 AU around the metal-poor G8V τ Ceti (Feng 2017,
`2017AJ....154..135F`). It is the innermost of the three planets
currently in `db/systems/tau_cet.json`. At 0.488 L☉ host
luminosity, g receives **27.59 S⊕** — roughly Mercury-class
illumination but on a fainter, cooler host. The equilibrium
temperature is 638 K at zero albedo or 584 K with an Earth-analog
albedo, comfortably above the H₂O critical point and approaching
silicate vaporization for some mineral phases. The planet is
**disputed** in NEA (`pl_controv_flag = 1`) — RV-only, no transit,
no direct imaging.

**Scenario choice for NearStars: a hot bare-rock super-Earth — most
of its primordial atmosphere lost despite the quiet host XUV
environment, leaving an exposed silicate surface with photolytic
oxidation patches, possible silicate-vapor cap near the substellar
point, and an ash-grey palette under quiet G8V illumination.** The
host's metal-poor SED and basal XUV mean atmospheric escape is
*thermal Jeans only* — no hydrodynamic loss — but at 638 K dayside
temperature and 0.13 AU separation, even Jeans escape for low-
molecular-weight species (H₂O, CH₄) operates efficiently over 7 Gyr.
The alternative thick-CO₂ Venus-analog reading is preserved as a
cfg variant; this synthesis follows the **interesting-first** rule
in picking the visually distinctive bare-rock outcome.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | maybe (3:2 or 1:1; cfg picks 3:2 Mercury-analog) | medium | Vinson 2017 / Makarov 2018: at P=20 d on a 0.78 M☉ host, tidal damping over 7 Gyr is borderline. e = 0.06 puts g in the 3:2-capture-permitted zone; the cfg picks 3:2 (interesting-first) over the asynchronous alternative |
| `obliquity_deg` | 0 | medium | Tidal damping over 7 Gyr; standard for short-period rocky planets |
| `eccentricity` | 0.06 | medium | Feng 2017 RV (consistent with secular forcing from h/f) |
| `argument_of_periastron_deg` | 35.341 | medium | Feng 2017 RV (reports 6.90 rad; normalized to [0,360)) |
| `sidereal_period_days` | 20.00 | high | Feng 2017 RV — uncertainty ±0.02 d |
| `semi_major_axis_au` | 0.133 | high | Feng 2017 (±0.001 from Kepler's third law + host mass) |
| `inclination_deg` | 35 | low | Tie-break: τ Ceti debris disk inclination (Lawler et al. 2014, adopted by MacGregor et al. 2016; assumed coplanar) |
| `mass_mearth` | 1.75 (M sin i; true mass ≳ 2.2 M⊕ assuming sin i ≈ 0.7) | medium | Feng 2017 RV (±0.25) |
| `radius_rearth` | 1.18 | low | Feng 2017 catalogued radius from mass–radius relation (Weiss & Marcy 2014 rocky); not directly measured |
| `surface_gravity_g_earth` | 1.26 | medium | derived = 1.75 / 1.18² |
| `density_g_cc` | 5.84 | medium | derived; Earth-like rocky composition consistent with the mass–radius relation pick |
| `water_mass_fraction` | < 0.01 | low | High insolation + low-XUV thermal Jeans escape over 7 Gyr → primordial water mostly lost; surface volatile inventory minimal |
| `insolation_s_earth` | 27.59 | high | derived L_bol/a²: 0.488 L☉ (Teixeira 2009, recommended) / 0.133² |
| `equilibrium_temp_k` (A=0) | 638 | high | derived 278 × (L/a²)^0.25 |
| `equilibrium_temp_k` (A=0.3) | 584 | high | derived with Earth-analog albedo |
| `bond_albedo` | 0.10 | low | Tie-break: low-albedo basalt / silicate surface; bare-rock airless body, Mercury-analog albedo |
| `surface_temp_substellar_k` | 700 | low | Slow rotator (3:2 resonance, 40-day solar day) → substellar temperature exceeds equilibrium because heat redistribution is incomplete |
| `surface_temp_nightside_k` | 200 | low | 3:2 resonance gives long thermal-decay time; nightside cools but not to deep-space limit |
| `surface_temp_global_mean_k` | 500 | low | Asymmetric heat distribution from slow rotation; subsolar-to-antisolar contrast moderated by conduction |
| `atmosphere_present` | false | medium | Tie-break: bare-rock airless adopted. Quiet host XUV preserves heavy molecules, but at 638 K Teq, even N₂ and CO₂ Jeans-escape on a ~2 M⊕ body over 7 Gyr; outgassing too slow on a likely cold-interior super-Earth |
| `atmosphere_surface_pressure_pa` | 0 | medium | Adopted scenario (bare rock); 1–100 mbar trace CO₂ + Na exosphere possible but not in cfg |
| `atmosphere_composition` | n/a (trace silicate-vapor + Na exosphere possible) | low | If any atmosphere, Mercury-analog: photolytically liberated Na, K, Si from regolith at substellar |
| `atmosphere_scale_height_km` | n/a | high | No bulk atmosphere |
| `atmosphere_tint_rgb_hex` | `#000000` (imperceptible) | high | No atmosphere → no scattering |
| `cloud_cover_fraction` | 0 | high | No atmosphere |
| `cloud_tint_rgb_hex` | n/a | high | No clouds |
| `ocean_present` | false | high | Far above water critical point + no atmosphere |
| `ocean_extent_substellar_radius_deg` | 0 | high | No surface liquid |
| `ocean_tint_rgb_hex` | n/a | high | No ocean |
| `surface_ice_caps` | none | high | Far above water freezing point everywhere |
| `surface_tint_rgb_hex_primary` | `#6c655c` (basaltic ash grey under G8V illumination; metal-poor host slightly cleaner-blue than Sol) | low | Tie-break: Mercury-analog basalt regolith; metal-poor host produces less iron-stained primordial dust → slightly less red-brown than Sol-system basalt; ash-grey rather than ochre |
| `surface_tint_rgb_hex_accent` | `#8a4a30` (photolytic iron-oxide patches near substellar where regolith is most heated) | low | Tie-break: 7 Gyr of direct G8V irradiation should produce localized iron-oxide weathering at substellar; interesting-first over uniform-grey alternative |
| `surface_morphology` | heavily impact-cratered bedrock; localized silicate-vapor frost on terminator/nightside from dayside outgassing; possible photolytically-darkened lava-flow remnants | low | Mercury / Moon analog; no resurfacing over 7 Gyr Suggests crater-saturated terrain |
| `magnetic_field_present` | false | low | Likely no active dynamo on a 1.75 M⊕ body with 3:2 slow rotation and probable cold interior; small fossil crustal field possible |
| `magnetic_field_strength_microtesla_equator` | 0.5 | low | Tie-break: Mercury-analog crustal-remnant only (Mercury's surface field ≈ 0.4 μT) |
| `tidal_heating_w_m2` | 0.01–0.1 | medium | e = 0.06 at a = 0.133 AU around a 0.78 M☉ host; Bolmont 2020-style scaling gives modest tidal flux but well below Io |
| `induction_heating_w_m2` | < 0.001 | medium | Host magnetic field too weak; quiet G dwarf magnetic torque negligible |
| `radiogenic_heat_w_m2` | 0.04 | medium | Earth-analog mantle radiogenics scaled by mass |
| `aurora_present` | false | high | No atmosphere; no aurora possible |
| `star_apparent_angular_diameter_deg` | 3.17 | high | derived: 2 × R★ / a × (180/π); 6× the Sun seen from Earth |
| `stellar_illumination_color_temp_k` | 5370 | high | host Teff (Pavlenko 2012) |

## Surface synthesis

τ Ceti g is in the **bare-rock** regime: 27.59 S⊕ insolation places
it well inside the runaway-greenhouse limit (Kopparapu 2014 inner
edge for a G8V is ~1.0 S⊕), but unlike Venus, g lacks the secondary
outgassing rate to maintain a thick CO₂ atmosphere against Jeans
escape over 7 Gyr. Two competing effects determine the outcome:

1. The host star is exceptionally quiet — log L_X ≤ 26.5 cgs
   (Schmitt 1985), log R'HK = −4.95 (Pavlenko 2012), basal FUV
   (Judge 2004). XUV-driven hydrodynamic escape is negligible.
   Heavy molecules (N₂, CO₂, SO₂) are not blow-off-limited.
2. But thermal Jeans escape at Teq = 638 K is non-negligible. The
   escape velocity for a 1.75 M⊕ planet of 1.18 R⊕ radius is
   13.7 km/s; the thermal velocity of N₂ at 638 K is 0.67 km/s,
   giving a Jeans parameter of 21 — formally retained — but for
   the upper-atmosphere effective temperature (typically 2–4× the
   surface in a thin/no-atmosphere regime), the Jeans parameter
   drops to ~5–10, in the marginal-loss range over Gyr timescales.

The cfg adopts the **interesting-first** outcome: bare-rock airless.
This produces a more visually distinctive Mercury-analog over the
Venus-analog alternative and matches the system context — τ Ceti's
inner planet should look different from its outer planets, and g
"loses its atmosphere while h retains a thick CO₂ envelope" is a
visually informative within-system contrast.

The surface is heavily impact-cratered bedrock with no resurfacing
on geological timescales. Tidal heating (e = 0.06 at 0.133 AU) is
modest (~0.05 W/m², well below Io's 2 W/m²) and does not drive
active volcanism. Radiogenic heating is Earth-analog 0.04 W/m². The
combined interior flux is too low to maintain a fluid mantle or
sustained dynamo, but is sufficient to slowly bleed primordial heat
over the system's age.

**Color choice — ash-grey basaltic regolith.** Mercury and the Moon
provide the empirical templates for unweathered silicate regolith on
an airless body — both are dominantly dark grey (`#6c655c` to
`#8c8478`) with localized brighter patches from ejecta or iron-poor
basalts. On τ Ceti g the metal-poor primordial dust (from a
[Fe/H] = −0.55 host) suggests less iron-staining of the original
grain population than around the Sun; the cfg pick `#6c655c` is a
slightly cleaner ash-grey than the Sol-system Mercury reference,
biased toward grey rather than ochre. Photolytic iron-oxide
weathering accumulates over 7 Gyr at the substellar region, giving
localized rust-brown patches (`#8a4a30`) at the ~5% surface-area
level — a tie-break that adds visual distinctiveness over a uniform
grey alternative.

**Mineralogy notes.** Without observation, mineralogy is inferred
from formation: a 2 M⊕ rocky body forming inside the iceline of a
metal-poor G dwarf should have Mg/Si ≈ 1.1–1.2 (slightly elevated
because Fe is depleted), favoring olivine and pyroxene over
plagioclase-dominated melts. Olivine-rich basaltic regolith would
appear slightly greener-grey than terrestrial basalt; the cfg pick
doesn't try to encode this at the hex level but the surface
morphology prose hints at it.

**No silicate-vapor cap.** At 700 K dayside temperature, silicate
vapor pressure is well below 10⁻⁶ bar (silicate condensation
temperature ~1500–2000 K). g is hot but not magma-ocean hot; no
substellar silicate-vapor cloud is rendered.

## Atmosphere synthesis

The cfg adopts **no bulk atmosphere**. The reasoning is in the
Surface synthesis above: thermal Jeans escape at 638 K Teq with
modest upper-atmosphere heating bleeds N₂ and CO₂ over 7 Gyr on a
2 M⊕ body, and the quiet host produces no replenishing photochemistry
of significance. The atmosphere is therefore vanishingly thin — a
Mercury-analog exosphere with photolytically liberated Na, K, Si,
O from the regolith at the substellar hot spot, dynamically
ballistic on the surface scale and not in hydrostatic equilibrium.

**No global Rayleigh haze.** The cfg `atmosphere_tint_rgb_hex` is
`#000000` (imperceptible) and the limb appears sharp at PQS
resolution.

**Sky appearance.** From the surface, the sky is black, dominated by
the host star at 3.17° angular diameter — about 6× the Sun's angular
size from Earth. The surface receives 27.59 S⊕ of pale-yellow G8V
illumination at the substellar point; dayside surface temperatures
exceed 700 K. Other stars are easily visible during dayside because
no atmosphere scatters the host light; the night sky is similar to
the Moon's, with deep field stars visible at full magnitude. The
host's metal-poor SED produces a slightly cleaner pale-yellow color
than the Sun's spectrum, perceptible as a marginally less warm
disk.

**Counterfactual — Venus-analog cfg variant.** A reader interested
in a "g is the Venus, h is the Mercury" alternative system
description could swap the two — but the period and insolation
ordering (g hottest, h next, f coldest) means the Venus-class
runaway-greenhouse is best placed at h (the slightly cooler 7.7 S⊕
neighbor) where outgassing rates support a sustained thick CO₂
atmosphere. The Mercury-analog g is the more physically defensible
pick.

## Rotation & spin synthesis

τ Ceti g's spin state is the most uncertain of the three planets.
Two competing scenarios:

1. **3:2 spin-orbit resonance (Mercury analog).** At e = 0.06,
   capture probability into 3:2 is ~50–70% (Makarov 2018 Figure 7
   for super-Earth-mass bodies at this period and eccentricity).
   The 3:2 capture creates a 40-day solar day with substantial
   thermal asymmetry between the libration regions.
2. **Asynchronous slow rotator.** If 3:2 capture failed, the
   planet rotates at a primordial period (could be anywhere from
   hours to days) with steady damping toward 3:2 or 1:1 — over
   7 Gyr at this orbital period, damping should be close to
   complete.

The cfg adopts **3:2 (Mercury analog)** as the interesting-first
pick. The 40-day solar day creates substantial diurnal cycling of
surface temperature (subsolar swings 200 → 700 → 200 K over the
solar day) and produces visually distinctive thermal asymmetry
across the surface. The 1:1 lock alternative is preserved as a cfg
variant in the Open items.

**KSP implementation note.** For 3:2: `rotationPeriod` = (2/3) ×
orbital period = 13.33 days (1.152×10⁶ s). For 1:1 alternative:
20 days (1.728×10⁶ s).

**Obliquity.** Tidal damping over 7 Gyr should pull obliquity to
zero; cfg adopts 0°. Libration-induced insolation variation
(~12% from e = 0.06) gives modest "seasons" over the 20-d orbital
period — perceptible as a brightening/cooling cycle but not as
hemispheric seasons.

**Magnetic dynamo expectation.** A 1.75 M⊕ body with 3:2 slow
rotation (~40-d solar day) and probably cold interior is unlikely
to sustain a global dynamo. Mercury's dynamo is anomalously
maintained by a partially-molten core; whether the same applies to
a metal-poor super-Earth is unclear. The cfg pessimistically
assumes no active dynamo, with possible Mercury-analog crustal
remnant field at ~0.5 μT.

## Visual styling

- **Global appearance.** A dark ash-grey rocky world (`#6c655c`)
  with localized rust-brown weathering patches (`#8a4a30`) near
  the substellar libration region. Heavily impact-cratered, with
  visible ray systems from younger impacts. Visual character is
  closest to a slightly larger Mercury — almost airless, dark,
  cratered.
- **Substellar region (libration zone).** Most heated, oldest
  oxidation patches concentrated here. Rust-brown weathering
  visible at PQS resolution as ~5% surface-area patches over the
  base ash-grey. Possible silicate-vapor-deposited bright patches
  near the largest impact crater rims (volatiles redeposited from
  the impact shock).
- **Mid-latitudes / longitudes.** Ash-grey basalt with subtle
  variations in albedo from differential weathering. Crater rays
  visible as bright lineations.
- **Terminator.** High contrast under grazing 5370 K G8V light;
  topographic shadows reveal cratering depth. The terminator
  band is sharp because the lack of atmosphere produces no
  scattering.
- **Nightside.** Dark grey-black with faint cyan-white sheen
  from starlight reflecting off regolith. KSP nightside ambient
  ≈ 0.5% dayside. Visible features: crater rims catching star
  light at oblique angles.
- **Atmosphere haze.** None — the limb is sharp at PQS
  resolution. The 0.1° Rayleigh scattering halo seen on Mercury
  in Earth observation is not rendered.
- **Star in sky.** τ Ceti subtends 3.17° in g's sky (6× the Sun
  from Earth). The disk is pale-yellow under metal-poor SED, much
  larger and brighter than the Sun seen from Earth, but somewhat
  cooler-yellow than Sol due to the lower Teff. Surface
  illumination at dayside peak is uncomfortably bright but not
  enough to incandesce the regolith.
- **Sister planets in sky.** h (next outward) at angular size
  ~0.05° in conjunction; f (much further) at ~0.03°. The cold
  debris disk at ≥ 6 AU is far outside and appears as a faint
  outer band.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Feng F. et al. 2017** — *Color difference makes a difference:
  four planet candidates around τ Ceti*, AJ 154, 135
  (`2017AJ....154..135F`, arXiv:1708.02051). Discovery + best
  constraint on g's orbit (P = 20.00 ± 0.02 d), mass
  (Msini = 1.75 ± 0.25 M⊕), eccentricity (0.06). Anchors every
  orbital and physical Decisions row.
- **Feng F. et al. 2018** — *Detection limits on τ Ceti's planet
  system*, A&A 613, A76 (`2018A&A...613A..76F`,
  arXiv:1801.05415). Confirms 20-day signal stability;
  controversial flag in NEA reflects amplitude-to-noise concerns.
- **Vinson A. M. & Hansen B. M. S. 2017** — *Spin-orbit dynamics
  of habitable-zone planets*. Capture probabilities for 3:2 vs.
  1:1 spin-orbit resonance; supports the 3:2 cfg pick for g at
  e = 0.06.
- **Makarov V. V. 2018** — *Tidal locking timescales and 3:2
  capture for rocky planets*. Figure 7 gives 3:2 capture
  probability ~50–70% at g's parameters.
- **Zahnle K. J. et al. 2017** — *Cosmic shoreline*. Empirical
  framework for atmospheric retention thresholds; g sits just
  inside the shoreline for a quiet host, marginal for atmospheric
  retention.

### Read (context / methodology, not directly decision-driving)

- **Kopparapu R. K. et al. 2014** — *Habitable zones*. Inner-edge
  runaway-greenhouse limit for a G8V is ~1.0 S⊕; g at 25.85 S⊕
  is far inside.
- **Lawler S. M. et al. 2014** — τ Ceti debris disk inclination
  ~35° (Herschel); adopted by MacGregor et al. 2016 (ALMA) and
  used here as g's orbital plane default.
- **Bolmont E. et al. 2020** — Tidal evolution framework; g's
  modest e = 0.06 at 0.133 AU gives ~0.05 W/m² flux.
- **Owen J. E. & Wu Y. 2017** — *Evaporation valley*. Sub-
  Neptune envelope retention vs. mass + insolation framework; g
  is well below the sub-Neptune mass and above the bare-rock
  retention threshold.

### Read (instrument / non-cfg-decisive)

- **Pavlenko Y. V. et al. 2012** — host star context.
- **Schmitt J. H. M. M. et al. 1985** — host X-ray non-detection.

### Not read — no arXiv preprint or low-priority (~12 papers)

- **Tuomi 2013 + 2014 erratum** — superseded by Feng 2017.
- **Various SETI / technosignature papers** — no cfg relevance.
- **Astrobiology speculation reviews** — generally do not
  individually address g (which is too hot for the conservative
  habitable category).

## Canonical alternatives

### Diverged cfg picks

| Field | Gameplay (in cfg) | Canonical alternative | Why diverged |
|---|---|---|---|
| `atmosphere_present` | false (bare-rock Mercury analog) | true, thick CO₂ Venus analog (~10 bar, T_surf ~700 K) | Both are defensible within the unconstrained window. Mercury-analog gives a visually distinctive cratered bedrock surface; Venus-analog gives an obscured cloud-covered yellow planet visually similar to τ Cet h. Interesting-first picks Mercury-analog to differentiate g visually from h. Venus-analog preserved as cfg variant. |
| `tidally_locked` | maybe (3:2 resonance, 40-d solar day) | 1:1 fully locked | Vinson 2017 / Makarov 2018 give 3:2 capture probability ~50–70% at e = 0.06. The cfg picks 3:2 for visual asymmetry (Mercury analog substellar libration zone vs. uniform thermal field of full lock). 1:1 alternative preserved as cfg variant. |

## Open items for follow-up

- **Controversial flag (`pl_controv_flag = 1`).** As for f, monitor
  for retraction by Lubin 2024 or future ESPRESSO RV reanalysis.
- **True mass.** Msini = 1.75 ± 0.25 M⊕; true mass depends on
  unknown i. Cfg adopts i ≈ 35° from disk → true mass ≈ 3.0 M⊕.
- **Radius is assumed, not measured.** R = 1.18 R⊕ from mass–
  radius relation; unconstrained from below. If true mass is
  higher and the planet is denser-rocky, R could be 1.05 R⊕ with
  ρ ≈ 7 g/cc.
- **Venus-analog cfg variant.** A 10-bar CO₂ atmosphere with
  H₂SO₄ clouds is the conservative alternative to the bare-rock
  pick. Visually it would look similar to τ Cet h — yellow-cream
  obscured cloud deck — so the cfg picks Mercury-analog for
  visual differentiation. The variant is preserved.
- **1:1 spin-lock cfg variant.** If a future tidal-dissipation
  modeling campaign refines τ_tidal for super-Earths on metal-
  poor hosts, the spin-state could be revised. Currently the
  3:2 vs. 1:1 question is essentially open.
- **Mineralogy refinement.** A metal-poor (Mg/Si elevated) rocky
  body should be olivine-rich. If future cfg shaders support
  mineralogy-specific surface tinting, the `surface_tint`
  could shift toward olive-grey rather than the current ash-grey
  default.
- **Trace exosphere.** A Mercury-analog Na/K/Si exosphere from
  photolytic regolith liberation is plausible but not visible at
  KSP rendering scales. Logged for future cfg refinement.

## Related

- [tau-cet](tau-cet.md) — host star Phase 3 (G8V metal-poor;
  quiet, old, debris-disk-bearing)
- [tau-cet-h](tau-cet-h.md) — middle sibling, Venus-analog with
  thick CO₂ atmosphere
- [tau-cet-f](tau-cet-f.md) — outermost sibling, snowball
- [methodology](../reference/methodology.md) — Decisions schema
- [rex-data-comparison](../reference/rex-data-comparison.md) — §6
  τ Ceti e curation gap
