<!-- TRAPPIST-1 e Phase 3 synthesis: cfg-ready decisions and reasoning -->
# TRAPPIST-1 e — Phase 3 Synthesis

TRAPPIST-1 e is a 0.92 R⊕, 0.69 M⊕ rocky planet on a 6.10-day orbit
around an M8V ultra-cool dwarf. Fourth planet out, receiving 0.66×
Earth's insolation — squarely in the conservative habitable zone and
the **single most likely habitable world** in the TRAPPIST-1 system
(Wolf 2017, Turbet 2018, Lincowski 2018, Way 2025). Recent JWST NIRSpec
PRISM transmission spectra (Glidden et al. 2025 DREAMS, 4 visits)
suffer from significant stellar contamination but exclude H₂-rich
atmospheres and weakly disfavor Venus-analog CO₂-rich atmospheres at
2σ. N₂-rich atmospheres with trace CO₂ and CH₄ are fully permitted;
bare-rock interpretation is also consistent.

**Scenario choice for NearStars: temperate aqua-planet with a 1 bar
N₂/CO₂/H₂O atmosphere, ocean-bearing, tidally-locked "eyeball"
geometry with open water near the substellar point and ice at the
terminator and nightside.** This is the canonical "best habitable
candidate" cfg variant. It picks the Wolf 2017 / Turbet 2018 / Way
2025 aquaplanet scenario from among the (still observation-consistent)
options. The alternative bare-rock interpretation is preserved as
a backup cfg variant.

## Decisions

Kopernicus / atmosphere cfg-ready values. `Confidence`: high =
directly measured or tightly constrained, medium = theoretical with
strong support, low = aesthetic choice within the allowed window.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 6.10 d orbit, tidal damping; Agol 2021 |
| `obliquity_deg` | 0 | high | tidal damping; Agol 2021 |
| `eccentricity` | 0.00510 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 108 | medium | Agol 2021 (low ecc → weak constraint) |
| `sidereal_period_days` | 6.1010 | high | Agol 2021 |
| `semi_major_axis_au` | 0.02925 | high | Agol 2021 |
| `mass_mearth` | 0.692 | high | Agol 2021 TTV |
| `radius_rearth` | 0.920 | high | Agol 2021 |
| `surface_gravity_g_earth` | 0.818 | high | derived = 0.692 / 0.920² |
| `density_g_cc` | 4.92 | high | Agol 2021 (lower than Earth — water-rich interior) |
| `water_mass_fraction` | 0.05–0.10 | medium | Agol 2021 + Acuña 2021 — low-mass + lower-density consistent with several wt% H₂O |
| `insolation_s_earth` | 0.66 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 251 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.3) | 230 | high | derived; Earth-analog albedo |
| `bond_albedo` | 0.30 | medium | Earth + Hapi 2024 aqua-planet GCM range 0.25–0.35 |
| `surface_temp_substellar_k` | 290 | medium | Wolf 2017 GCM Aquaplanet; Turbet 2018 §4 |
| `surface_temp_nightside_k` | 230 | medium | Wolf 2017 GCM; ice-covered nightside |
| `surface_temp_global_mean_k` | 270 | medium | Wolf 2017 GCM Aquaplanet |
| `atmosphere_present` | true | high | adopted scenario; consistent with Glidden 2025 |
| `atmosphere_surface_pressure_pa` | 100 000 | medium | 1 bar canonical Earth-like; Glidden 2025 permits N₂-rich with trace CO₂ |
| `atmosphere_composition` | N₂ 78%, O₂ ~5% (low; abiotic), CO₂ ~1%, H₂O 0.1–1%, Ar 0.5% | medium | Wolf 2017, Lincowski 2018 aquaplanet equilibrium; CO₂ elevated vs. Earth for outer-HZ warming |
| `atmosphere_scale_height_km` | 9.5 | medium | derived: kT/μg with T≈270 K, μ=29, g=8.0 m/s² |
| `atmosphere_tint_rgb_hex` | `#5a7090` (muted blue with M-dwarf red shift) | medium | Rayleigh-blue under 2566 K illumination — heavily red-shifted toward dim cyan-gray |
| `cloud_cover_fraction` | 0.55 | medium | Wolf 2017 GCM Aquaplanet stratocumulus + cirrus |
| `cloud_tint_rgb_hex` | `#c0a890` (warm cream — red-shifted water clouds) | medium | water cloud + 2566 K illumination → warm cream-orange |
| `ocean_present` | true (substellar open-water disk; ice elsewhere) | medium | Turbet 2018 aquaplanet; Pierrehumbert 2011 "eyeball Earth" morphology |
| `ocean_extent_substellar_radius_deg` | 35 | medium | Wolf 2017 Aquaplanet — open ocean within ~35° of substellar point |
| `ocean_tint_rgb_hex` | `#1a2540` (dark navy under low M-dwarf insolation) | low | deep ocean + faint red star → dark blue-violet |
| `surface_ice_caps` | full coverage outside substellar open-water disk; ~60% of surface | medium | Wolf 2017 Aquaplanet ice line at ~35° from substellar |
| `surface_tint_rgb_hex_primary` | `#d8d0c4` (snow / sea ice under M-dwarf light) | medium | water ice albedo 0.6–0.8 + red-shifted illumination |
| `surface_tint_rgb_hex_accent` | `#7a6a58` (exposed bedrock at ridge tops on terminator) | low | thin atmosphere + ice flow geometry |
| `surface_morphology` | ocean within ~35° of substellar; sea-ice + glacial terrain elsewhere; submerged + emerged terrain at ice boundary | medium | Hu 2014 / Pierrehumbert 2011 tidally-locked aquaplanet templates |
| `magnetic_field_present` | true (modest, ~0.1× Earth) | low | small mass + slow rotation → weak intrinsic field; not directly constrained |
| `induction_heating_w_m2` | 0.01–0.1 | medium | Grayver 2022 — much lower at e than at b/c |
| `tidal_heating_w_m2` | 0.001–0.01 | medium | Bolmont 2020 — minimal at e |
| `star_apparent_angular_diameter_deg` | 2.17 | high | derived: 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## Surface synthesis

TRAPPIST-1 e is the system's most likely habitable world. Three lines
of evidence converge:

1. **Insolation** (0.66 S⊕) places it inside the conservative
   habitable zone (Kopparapu 2013 / 2014) for any reasonable
   atmosphere with greenhouse warming. Without an atmosphere, e
   freezes; with 1 bar N₂/CO₂, it supports surface liquid water
   (Wolf 2017, Turbet 2018 §4).

2. **Density** (4.92 g/cc from Agol 2021) is lower than Earth's
   5.51 g/cc, consistent with a non-trivial water mass fraction.
   Magma-Ocean modeling (Bourgeois et al. 2024 — 2008.09599) gives
   a water mass fraction of 0–0.23 for e, with central estimates
   around 0.05–0.10 (several percent by mass = several Earth oceans
   worth of water).

3. **Observational consistency.** Glidden 2025 (DREAMS) rules out
   H₂-rich and weakly disfavors Venus-analog atmospheres, but
   explicitly permits N₂-rich atmospheres with trace CO₂ and CH₄ —
   exactly the canonical Earth-analog secondary atmosphere.

For the surface morphology, the tidally-locked aquaplanet template
(Pierrehumbert 2011, Hu & Yang 2014, Wolf 2017) gives a distinctive
"eyeball Earth" pattern:

- **Substellar disk** (≲35° from substellar point): open ocean, warm
  enough for liquid water (substellar surface temperature ~290 K in
  Wolf 2017 Aquaplanet scenario), possible cirrus clouds.
- **Mid-latitudes / mid-longitudes** (35–90° from substellar): sea
  ice with thickness varying from a few meters at the ice line to
  hundreds of meters near the terminator.
- **Terminator and nightside** (>90° from substellar): thick glacial
  ice (>1 km) over a frozen ocean; possible emerged terrain at ridge
  tops where ice has fractured around tectonic features.

**Color choice.** Two competing effects: (a) intrinsic ice/snow
albedo is high (0.6–0.8) and bluish-white, (b) the 2566 K M-dwarf
illumination shifts perceived hue strongly to red-orange. The
combination produces a warm cream-white for ice cover (`#d8d0c4`) and
a dark navy-violet for deep ocean (`#1a2540`). Hu 2014 explicitly
notes that aquaplanets around M-dwarfs appear "less blue" than Earth
because the stellar SED has minimal short-wavelength flux to
Rayleigh-scatter.

**Iron oxide / bedrock.** Limited exposure — most surface area is
ice-covered. Bedrock appearance limited to ridge tops near the
terminator where glacial flow has thinned ice. The accent `#7a6a58`
is a muted weathered-basalt tone under M-dwarf light.

**Morphology under tidal lock.** The substellar disk hosts active
hydrological circulation — surface heating drives evaporation,
condensation in the polar / nightside cold-traps creates persistent
glaciers, glacial flow returns water toward the substellar disk.
This pattern is stable on geological timescales (Wolf 2017 §6),
producing a planet with permanent climatic zones rather than
seasonal cycles.

## Atmosphere synthesis

Glidden 2025 (DREAMS NIRSpec PRISM, 4 transits) presents the first
JWST transmission spectra of e. Significant stellar contamination
across 0.6–5 μm complicates the inference, but after marginalizing
over stellar features with Gaussian processes they find:

- H₂-rich (≳80% by volume) cloudy atmospheres excluded at >3σ
- Venus-analog CO₂-rich atmospheres weakly disfavored at 2σ
- N₂-rich atmospheres with trace CO₂ and CH₄ are **fully permitted**
- Bare-rock interpretation also adequate but with unexplained features

This is consistent with — and rather supports — the Earth-analog
secondary atmosphere expected from Wolf 2017 / Lincowski 2018 / Way
2025 modeling.

For NearStars we adopt the **1 bar N₂-rich aquaplanet atmosphere**:

- **Pressure** 1 bar (100 kPa) — Earth-analog, comfortably within
  the Glidden 2025 N₂-rich consistency window.
- **Composition** N₂ 78% (Earth-like background), Ar 0.5%, CO₂ 1%
  (elevated vs. Earth's 0.04% to provide outer-HZ greenhouse
  warming; Wolf 2017 finds 1–10× CO₂ enhancement needed for habitable
  surface), H₂O 0.1–1% (saturated near substellar surface, much
  less elsewhere), O₂ ~5% (abiotic photolysis-driven O₂; below
  current Earth's 21% because no oxygenic biosphere is assumed in
  the cfg).
- **Clouds.** Wolf 2017 GCM produces ~55% global cloud cover, mostly
  stratocumulus over the open-water disk and high cirrus elsewhere.
  Cirrus contributes 5–10% greenhouse warming.

**Sky appearance.** The 1 bar N₂ atmosphere has Earth-like Rayleigh
scattering at short wavelengths, but the 2566 K stellar SED has
minimal flux below 0.5 μm — so the scattered sky color is much
dimmer and shifted toward orange compared to Earth's blue. The
zenith sky is a dim red-blue mix (~`#3a4060`), transitioning to a
warm orange near the horizon (`#a07050`). Water cloud features
appear as warm cream patches (`#c0a890`) catching the red stellar
light.

The host star dominates the daytime sky at angular size 2.17° (about
4× the Sun's angular size from Earth). Surface illumination at the
substellar point is about 0.66 × Earth's, similar to a heavily
overcast Earth day — but with the spectral peak shifted firmly into
the red/near-IR.

**Nightside.** No direct stellar illumination; the only light sources
are (a) scattered light from the dayside transported via atmospheric
circulation (negligible), (b) reflected light from sister planets
(f and d at conjunction, ~0.4–0.5° angular diameter, mv ≈ −10 to
−13), and (c) starlight from distant stars (visible because there
is no atmospheric scattering from the absent sun). Nightside sky
is dramatically dark — KSP nightside ambient should be ~1% of
dayside.

## Rotation & spin synthesis

Tidal damping for e at 6.10-day period over 7.6 Gyr establishes the
synchronous (1:1) configuration unambiguously. Obliquity damped to
zero (Agol 2021 §6.2). Eccentricity is 0.00510 (Agol 2021), too low
for 3:2 spin-orbit (Vinson 2017).

**KSP implementation note.** Rotation period = orbital period =
6.1010 days (527 127 s). Kopernicus `rotationPeriod` should match the
orbital `period` in seconds.

**Slow rotation effects.** With a 6.1-day rotation period, Coriolis
effects are weaker than on Earth (Rossby number elevated). Wolf 2017
GCM shows this produces a slow, broad east-to-west zonal circulation
in the substellar disk rather than Earth's narrow jet streams. The
visual implication for cloud patterns: smoother, larger-scale cloud
bands; less cyclonic activity.

**No seasons.** Obliquity = 0; libration-induced insolation variation
< 0.4%. The substellar point and its open-water disk are fixed in
the surface frame.

## Visual styling

Combining surface and atmosphere decisions:

- **Global appearance.** From orbit, e looks like a snowball with a
  warm-cream open-water "pupil" near the substellar point, ringed
  by a fractal sea-ice transition zone, and entirely white-cream
  glacial ice beyond. Persistent cloud cover (~55% global) softens
  the appearance, with stratocumulus over the substellar ocean and
  high cirrus over the ice zones.
- **Substellar disk (open water).** Dark navy ocean (`#1a2540`)
  under intense red-orange illumination, dotted with warm cream
  clouds (`#c0a890`). Most visually striking feature of the planet.
- **Ice transition band.** Fractal pattern of warm cream
  (`#d8d0c4`) ice and dark ocean (`#1a2540`) — broken sea ice with
  open leads. The transition radius is about 35° from substellar
  (Wolf 2017); KSP terrain should show this as a roughly circular
  ice line.
- **Glacial ice zone.** Smooth warm cream (`#d8d0c4`) with subtle
  topographic relief where glacial flow encounters bedrock. The
  terminator is the brightest zone in oblique illumination — long
  shadows reveal pressure ridges and crevasses.
- **Nightside.** Dark with a faint cyan-white sheen from
  starlight-reflecting ice. Visible features: pressure ridges,
  fractures, and the occasional refrozen lead. KSP nightside ambient
  ≈ 1% dayside; rendering should show ice-features only.
- **Atmosphere haze.** Pale gray-blue limb glow (`#5a7090`) about
  15–25 km thick — Rayleigh-scattered M-dwarf light. Significantly
  fainter than Earth's blue limb because of the M-dwarf SED.
- **Star in sky.** TRAPPIST-1 subtends 2.17° in e's sky (4× the Sun
  from Earth) — appears as a deep red-orange disk (`#ff7a1a`) about
  the size of a large dinner plate held at arm's length. The
  illumination on the surface feels like "perpetual sunset" at the
  substellar point, fading to dusk and full night moving away.
- **Sister planets in sky.** d (next inward) at angular size ~0.3°
  in conjunction; f (next outward) at ~0.4°. Conjunctions every few
  days due to the resonant chain. The full system is near-coplanar.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2509.05414** Glidden 2025 (DREAMS NIRSpec PRISM) — first JWST
  transmission spectra of e (4 visits). Excludes cloudy H₂-rich
  atmospheres at >3σ; constrains stellar contamination methods.
  Cornerstone observational paper.
- **2509.05407** Glidden 2025 (DREAMS Secondary Atmospheres) —
  companion paper. **N₂-rich atmospheres with trace CO₂ and CH₄
  fully permitted; weak disfavor of Venus-analog at 2σ.** Drives the
  scenario choice.
- **2510.18704** Bourgeois 2025 — Multimodel ensemble (photochemistry
  + 3D climate + transmission spectra) for e. Explores N₂/CO₂/CH₄/H₂O
  composition space, water clouds, and photochemical hazes. Informs
  the cloud cover fraction and atmospheric composition mix.
- **2502.00132** Way 2025 — ROCKE-3D GCM suite for TRAPPIST-1 d but
  with extensive comparison to e. Locates e in the habitable parameter
  space and discusses the Earth/Venus/Dead trichotomy. Already read
  for d Phase 3.
- **1809.07498** Lincowski 2018 — Evolved climates of all TRAPPIST-1
  planets. "Aqua planet e could maintain a temperate surface given
  Earth-like geological outgassing and CO₂." Directly motivates the
  aquaplanet cfg choice.
- **2006.11349** Wunderlich 2020 — Wet vs. dry atmospheres of e and
  f. Confirms e can be temperate with E-like geology + CO₂. Supports
  cfg composition decisions.
- **2008.09599** Bourgeois 2024 — Magma ocean evolution of e/f/g.
  Gives water mass fraction range 0–0.23 for e; sets the bedrock
  water budget. Used in surface synthesis.

### Read (context / methodology, not decision-driving)

- **2403.03403** How habitable are M dwarf exoplanets? Modeling
  surface conditions. General M-dwarf HZ context; not e-specific.
- **2412.10192** From CO₂- to H₂O-dominated atmospheres. Background
  on volatile cycling in habitable-zone planets; informs the CO₂
  fraction choice (1% rather than 0.04% for outer-HZ warming).
- **2206.00028** Felton 2022 — Atmospheric exchange biosignature
  false positives (O₂ from d transported to e). Already read for d
  Phase 3. Constrains the abiotic O₂ background but doesn't change
  the visual cfg.
- **2310.15992** New 2D Energy Balance Model for slowly-rotating
  tidally-locked planets. Methodology context for the substellar
  disk modeling.
- **2211.11887** Cohen 2022 — Traveling planetary-scale waves on
  tidally-locked aquaplanets. Predicts cloud variability that could
  add visual interest but is gameplay-irrelevant for KSP.
- **2305.08813** *(in d bibliography, not e)* Various contamination /
  characterization works — context only.

### Read (instrument-only, not visual-informative)

- **2203.04173** Rustamkulov 2022 — JWST NIRSpec lab time-series.
  Methodology only.
- **2407.19167** Machine-assisted biosignature classification. Not
  e-specific.

### Not read — no arXiv preprint or low-priority (~34 papers)

The e bibliography is the second-largest (64 papers, 30 with arXiv).
Most non-arXiv papers are conference abstracts on biosignatures or
ELT-specific characterization plans, not visual-informative.
Notable items skipped:

- **2024–2025 various** — biosignature feasibility studies and JWST
  proposal abstracts. Skip unless updating the cfg-relevant
  atmospheric composition.
- **Photochemistry program proposals** — methodology only.

---

## Open items for follow-up

- The Glidden 2025 DREAMS papers acknowledge "features which may be
  due to either uncorrected stellar contamination or planetary
  signal." If a future re-reduction or a new instrument (NIRISS,
  MIRI MRS) on e finds molecular features, the atmospheric
  composition table may need updating.
- The water mass fraction range (0.05–0.10 adopted) is the median
  of Bourgeois 2024's 0–0.23 — could narrow if Acuña 2025 or later
  interior fits improve.
- Cfg variant for the "Venus-analog" interpretation (1 bar CO₂ +
  H₂SO₄ clouds): visually distinctive yellow-cream world with no
  ocean. Weakly disfavored at 2σ by Glidden 2025 but not excluded.
- Cfg variant for the "bare-rock airless" interpretation: similar
  visuals to b/c but at e's much colder dayside temperatures (T_eq
  ≈ 250 K → mostly ice-coated bare rock).
- Cross-check the 5% abiotic O₂ choice — could be 10–20% in some
  Lincowski 2018 scenarios. Lower bound matches "minimum
  photolytic" expectation; upper bound is more "post-runaway".
