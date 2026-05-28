# Teegarden's Star c — Phase 3 Synthesis

Teegarden's Star c is a 1.05 M⊕ minimum-mass rocky planet on an
11.416-day orbit around the M7.0 V host, with semi-major axis 0.0455
AU and insolation 0.35 ± 0.02 S⊕ (Dreizler 2024). Equilibrium
temperature with Bond albedo 0.3 is 209 ± 4 K — 70 K below the freezing
point of water. The Earth Similarity Index, which uses a simple bulk-
parameter weighting, comes out high (ESI = 0.88, comparable to Proxima
b per Dreizler 2024), but that is misleading: c sits at or beyond the
outer edge of the conservative habitable zone, and recent 3D GCM
modelling finds it locked in a global snowball state for every
atmospheric composition tested. The cfg therefore renders c as a
**cold, globally ice-covered world** — not as a temperate Earth-analog.

The defining cfg-relevant result for c comes from Hammond 2025
(arXiv:2504.00978), which runs an ExoCAM GCM suite over seven nearby
HZ targets including Teegarden c, with pCO₂ varied from 100 μbar to 2
bar. Of the seven targets, c is the **only one** that fails to support
liquid water anywhere on its surface even with the maximum 2-bar CO₂
greenhouse. The combination of low insolation (S = 0.37 in Hammond's
parameter set), high ice albedo feedback, and the M-dwarf SED's
limited shortwave heating efficiency drives c firmly into snowball
regardless of how much greenhouse gas is loaded.

Wandel 2019's older 1D analytic model gave a more optimistic
habitability range (H_atm = 1-12 at f = 0.5), but that model lacks
ice-albedo feedback and 3D heat redistribution physics. The Hammond
2025 3D GCM is the canonical reading; cfg follows it.

**Scenario choice for NearStars: globally ice-covered "snowball"
planet with thin CO₂-enhanced N₂ atmosphere, tidally locked, surface
temperature below 273 K everywhere, no liquid water, atmospheric
circulation dominated by an equatorial superrotating jet.** The cfg
is structurally distinct from b's eyeball aquaplanet and from d's bare
rock — c is the system's archetypal snowball.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | Wandel 2019; Hammond 2025 GCM assumes 1:1 |
| `obliquity_deg` | 0 | high | tidal damping |
| `eccentricity` | 0.06 | high | Dreizler 2024 |
| `argument_of_periastron_deg` | 301 | low | Dreizler 2024 (poorly constrained at low e: +165/−74) |
| `sidereal_period_days` | 11.416 | high | Dreizler 2024 |
| `semi_major_axis_au` | 0.0455 | high | Dreizler 2024 |
| `mass_mearth` | 1.05 (msini) | high | Dreizler 2024 table 4 |
| `radius_rearth` | 1.02 | medium | Hammond 2025 (Zeng 2016 Earth-like MR) |
| `surface_gravity_g_earth` | 1.01 | medium | derived = 1.05 / 1.02² |
| `density_g_cc` | 5.4 (Earth-like assumption) | low | no transit |
| `insolation_s_earth` | 0.35 | high | Dreizler 2024 (Hammond 2025 uses 0.37 with slightly different stellar params) |
| `equilibrium_temp_k` (A=0.3) | 209 | high | Dreizler 2024 |
| `bond_albedo` | 0.55 | medium | Hammond 2025 — high ice albedo dominates snowball regime |
| `surface_temp_substellar_k` | 230 | medium | Hammond 2025 ExoCAM Fig. 2 — warmest dayside spot still below freezing |
| `surface_temp_nightside_k` | 170 | medium | Hammond 2025 nightside cold-trap, also CO₂ frost regime |
| `surface_temp_global_mean_k` | 200 | medium | Hammond 2025 — sub-freezing everywhere for all pCO₂ |
| `atmosphere_present` | true | high | Wandel 2019; Hammond 2025 default 0.1-2 bar CO₂ all sustain |
| `atmosphere_surface_pressure_pa` | 100 000 | medium | Tie-break: Hammond 2025 1-bar Earth-analog default; even 2 bar CO₂ doesn't melt the ice |
| `atmosphere_composition` | N₂ 99%, CO₂ 1%, trace H₂O, Ar 0.5% | medium | Tie-break: Hammond pCO₂=0.1 bar case bracketed for the "warm-edge" snowball |
| `atmosphere_scale_height_km` | 5.5 | medium | derived: kT/μg with T=200 K, μ=29, g=9.9 m/s² |
| `atmosphere_tint_rgb_hex` | `#4a3a50` (thin Rayleigh + cold-sky dim violet) | low | Tie-break: Rayleigh under 2904 K + low pressure — dimmer than b's `#5a3a40` |
| `cloud_cover_fraction` | 0.35 | medium | Hammond 2025 — patchy clouds at terminator cold-traps; less than Earth-analog |
| `cloud_morphology` | Patchy water-ice / CO₂-ice clouds at terminator cold-traps; sparse high cirrus over substellar | medium | Hammond 2025 — wind quivers show terminator convergence; snowball atmosphere has limited moisture |
| `cloud_tint_rgb_hex` | `#a09080` (dim warm cream — even less moisture than b) | low | Tie-break: ice clouds + M7 V illumination |
| `ocean_present` | false | high | Hammond 2025 — ice everywhere even at 2 bar CO₂ |
| `surface_morphology` | Global ice sheet ~50-300 m thick over frozen ocean substrate; hummocky terrain at convergence zones; rare exposed dark bedrock at low-latitude impact craters or volcanic vents | medium | Snowball-Earth analog physics; no Teegarden-c-specific GCM topology paper |
| `surface_tint_rgb_hex_primary` | `#d8d0c4` (ice surface under M-dwarf light) | medium | Tie-break: water ice albedo 0.6-0.8 + 2904 K illumination; matches b ice tone for system consistency |
| `surface_tint_rgb_hex_accent` | `#4a3030` (exposed mafic bedrock at impact craters and volcanic features) | low | Tie-break: sparse exposure suggests darker terrain than b |
| `magnetic_field_present` | true (modest) | low | Tie-break: Earth-mass active interior; no measurement |
| `magnetic_field_strength_microtesla_equator` | 20 | low | Tie-break: scaled slightly lower than b because c is colder (slower core convection); no measurement |
| `aurora_present` | true (weak) | low | Atm + B-field both modest; M-dwarf SEP environment |
| `aurora_color_primary_hex` | `#4DFF4D` | low | Tie-break: [OI] 557.7 nm — but very weak; CO₂⁺ accent `#FF4D4D` may dominate in CO₂-rich atm |
| `aurora_intensity_kR_typical` | 15 | low | Tie-break: half of b's 30 kR because c is dimmer-flux side, thinner atmosphere couples less of SEP energy |
| `surface_radiation_dose_msv_yr` | 50 | low | Tie-break: low M7 V flare rate + Earth-like B-field + 1 bar atmosphere |
| `star_apparent_angular_diameter_deg` | 1.25 | high | derived: 2 × 0.107×0.00465 / 0.0455 × 57.3 = 1.25° |
| `stellar_illumination_color_temp_k` | 2904 | high | Cifuentes 2020 |

## Surface synthesis

Teegarden c sits at S = 0.35 S⊕ — about a third of Earth's insolation
and below the conservative outer-HZ limit (Kopparapu 2013 S_outer ≈
0.36 for an M dwarf with full atmospheric circulation). The cfg's
snowball pick rests on Hammond 2025 (arXiv:2504.00978), which is the
most recent dedicated 3D GCM study of c.

Hammond's ExoCAM grid runs c at three pCO₂ values (100 μbar, 0.1 bar,
2 bar) all with 1 bar N₂ background, and finds:

- **100 μbar CO₂**: Surface temperatures fall to ~140 K at the
  nightside cold-trap, ~190 K at substellar. Total CO₂ atmospheric
  reservoir would freeze out — atmospheric collapse imminent.
- **0.1 bar CO₂**: Surface 170-220 K, nightside ~170 K, substellar
  ~220 K. Stable atmosphere but still ice-covered.
- **2 bar CO₂**: Substellar warms to ~230 K, nightside ~190 K. Still
  ice-covered everywhere — the maximum greenhouse warming achievable
  in the simulation does not lift the dayside above the freezing
  point.

The reason c stays frozen even at extreme greenhouse loading is the
combination of low instellation (only 0.35 S⊕) and a high ice albedo
that the M-dwarf SED struggles to overcome. Late-M illumination peaks
in the near-IR, where water ice has surprisingly high absorptivity
(unlike at visible wavelengths where ice albedo is 0.7-0.9), but the
substellar dayside still requires the bulk of incident flux to be at
shorter wavelengths to break out of the ice-albedo feedback loop —
exactly what an M7 V host fails to provide.

The cfg therefore renders c as a **uniform ice-covered surface** with:

- **Substellar dayside**: Surface temperature ~220-230 K. Ice may be
  thin enough (a few meters at most) to be photically transparent in
  rare cases, but no melt pools form. Surface morphology is hummocky,
  with pressure ridges where atmospheric circulation drives ice
  convergence.
- **Mid-latitudes / longitudes**: Glacial ice sheet ~50-300 m thick
  over the frozen ocean substrate (if any subsurface water exists from
  primordial accretion). Surface temperature 180-210 K.
- **Nightside**: Permanent CO₂-frost cold-trap. Surface temperature
  ~170 K, possibly with CO₂ ice deposition reducing atmospheric
  pressure locally — a Martian-style polar-CO₂-frost analog but at
  the entire nightside hemisphere.

**Colour choice.** The surface is overwhelmingly water-ice with the
same M-dwarf-illumination-shifted warm cream `#d8d0c4` as on b. The
accent `#4a3030` (dark mafic bedrock) appears at sparse impact craters
where ejecta has temporarily exposed sub-ice material — these would be
the most visually distinctive features for a player flying over the
surface.

## Atmosphere synthesis

The cfg adopts the **1 bar N₂ + 1% CO₂** composition — a compromise
between Hammond 2025's 0.1 bar and 2 bar CO₂ scenarios. This is at
the warmer end of the snowball regime (about 220-230 K substellar) but
explicitly does not lift the surface above freezing. The composition is:

- **Pressure** 1 bar (100 kPa) — Hammond 2025 N₂ background default.
- **Composition** N₂ 99%, CO₂ 1% (10 mbar — between Earth's 400 ppm
  and Hammond's 0.1 bar), H₂O trace (saturated at ~6×10⁻⁵ at 200 K),
  Ar 0.5%.
- **Clouds.** Hammond 2025 wind-vector maps (Fig. 2) show
  terminator-convergent flow zones where atmospheric water vapor
  (already extremely sparse) condenses into thin clouds. Total cloud
  cover ~35% — much less than b's 55% because there is minimal
  liquid-phase water cycling. CO₂-ice clouds may form on the
  nightside if surface temperatures drop below the CO₂ frost point
  (~165 K at 1 bar), giving rise to occasional bright cloud features
  on the nightside.

**Sky appearance.** The 1 bar atmosphere has Rayleigh scattering at
short wavelengths, but with the 2904 K stellar SED there is even less
short-wavelength flux than on b — the scattered sky is dim and
shifted toward red. Zenith sky `#3a2a35`, horizon `#7a5040`.

The host star angular size is 1.25° (about 2.3× the Sun's angular
size from Earth). Surface illumination at substellar is 0.35 ×
Earth's bolometric flux — comparable to twilight on Earth, with the
spectral peak firmly in the near-IR. Most of the incident energy is
absorbed by water-ice with high near-IR absorptivity but most of the
upwelling thermal emission radiates back to space because the thin
atmosphere is optically thin in the 8-13 μm window.

**Atmospheric escape and stability.** The 8 Gyr old quiet host star
favors atmospheric retention as long as the planet built and kept a
secondary CO₂/N₂ atmosphere via outgassing. Hammond 2025 does not
include escape; Wandel 2019 §3.1 reviewed retention and found old quiet
M dwarfs less hostile than younger active ones. The CO₂-N₂ atmosphere
is heavier than the H₂/He primordial atmosphere typical of pre-MS
escape and is less susceptible to thermal escape.

**Auroras.** Weak (15 kR typical, vs 30 kR for b and 150 kR for
TRAPPIST-1 e). The lower flare frequency at Teegarden's distance
combined with the thinner atmosphere produces a sparse auroral
display. Visible emission is dominated by [OI] 557.7 nm green
(`#4DFF4D`) where O is present from minor CO₂ photolysis, with a CO₂⁺
red-orange accent (`#FF4D4D`) in the 580-700 nm Fox-Duffendack-Barker
bands becoming significant if CO₂ fraction exceeds a few percent.

## Rotation & spin synthesis

c at P_orb = 11.4 d is firmly inside the tidal-locking timescale
(Griessmeier 2009) over 8 Gyr; the cfg assumes synchronous rotation.
Obliquity damped to zero. Eccentricity is 0.06 (Dreizler 2024) —
close enough to circular that 3:2 spin-orbit resonance is unstable.

**KSP implementation note.** Rotation period = orbital period =
11.416 days (986 342 s).

**Atmospheric circulation.** Hammond 2025 ExoCAM gives c an equatorial
superrotating jet (their Figure 3 zonal-mean zonal wind shows positive
flow ~20 m/s at the equator at low pressures). Surface flow is weaker.
This is canonical for slowly-rotating tidally-locked planets and
matches the "thermal superrotation" regime (Pierrehumbert & Hammond
2019).

**No seasons.** Obliquity = 0; libration amplitude small.

**Magnetic dynamo.** Earth-mass c likely supports a modest dynamo from
core convection. The cfg picks a low Earth-analog field (20 μT,
slightly less than b's 25 μT) as a tie-break — the colder interior
might have slightly less vigorous core convection. No measurement.

## Visual styling

Combining surface and atmosphere decisions, c renders as a uniform
white-cream snowball world:

- **Global appearance from orbit.** A nearly featureless ice sphere
  with subtle variations in surface roughness. Terminator features
  (pressure ridges, glacial flow lines) become visible only at
  oblique illumination. The thin atmosphere produces almost no limb
  haze.
- **Substellar zone**: Slightly warmer ice (~230 K), possibly with
  rare melt-puddle-equivalent thin transparent ice patches. Surface
  morphology shows convergence-driven pressure ridges as the
  atmospheric superrotating jet drives ice convergence.
- **Mid-latitudes**: Uniform glacial sheet, smooth on large scales,
  occasional impact craters with exposed dark `#4a3030` bedrock at
  the impact center where ice has been ejected.
- **Nightside**: Dark, possibly with bright patches of CO₂-frost
  deposition where surface temperature drops below 165 K. Cold trap
  visible as a uniformly dim region.
- **Atmosphere haze.** Very thin pale violet limb glow (`#4a3a50`)
  ~8-12 km thick.
- **Star in sky.** Teegarden's Star subtends 1.25° in c's sky (2.3×
  the Sun from Earth). Appears as a deep red-orange disk much smaller
  than from b — illumination feels like deep twilight, never noon.
- **Sister planets in sky.** b at inferior conjunction (~0.3°
  angular diameter, m_v ≈ −6); d at superior conjunction (~0.2°,
  m_v ≈ −4). Inferior conjunctions with b happen every ~8 days at the
  beat period.

The overall visual impression should evoke a Hoth-like ice world but
with the perpetual red-orange illumination of an ultra-cool dwarf.
c is visually less striking than b (no ocean-pupil contrast) but
forms a distinct "frozen sibling" companion in the system view.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Dreizler S. et al. 2024** — *Teegarden's Star revisited*
  (`2024A&A...684A.117D`, arXiv:2402.00923). Refined c orbit
  (P = 11.416 d, e = 0.06, msini = 1.05 M⊕, T_eq = 209 K, S = 0.35 S⊕).
- **Hammond T. et al. 2025** — *The climates and thermal emission
  spectra of prime nearby temperate rocky exoplanet targets* (`2025ApJ...
  984..181H`, arXiv:2504.00978). 3D ExoCAM GCM of c at 100 μbar / 0.1
  bar / 2 bar CO₂ — c is ice-covered everywhere for all pCO₂. Driver
  of the cfg's snowball choice.
- **Wandel A. & Tal-Or L. 2019** — *On the Habitability of Teegarden's
  Star planets* (`2019ApJ...880L..21W`, arXiv:1906.07704). 1D analytic
  habitability range H_atm = 1-12 for c — the older, more optimistic
  reading superseded by Hammond 2025.
- **Zechmeister M. et al. 2019** — Discovery paper for b and c
  (arXiv:1906.07196). Original orbital parameters.

### Read (context / methodology, not decision-driving)

- **Kossakowski D. et al. 2023** — *The CARMENES search for exoplanets
  around M dwarfs. Wolf 1069 b: Earth-mass planet in the habitable
  zone of a nearby, very low-mass star* (`2023A&A...670A..84K`,
  arXiv:2301.02477). Comparison rocky planet at S = 0.65 S⊕ around a
  warmer M5 V; helps frame why c (at S = 0.35) is the colder edge.
- **Schweitzer A. et al. 2019** — Stellar params; used via host star.
- **Boukrouche R. et al. 2024** — Water clouds emission spectrum
  (arXiv:2411.07922). For b but methodology context for c.

### Read (instrument / non-cfg-decisive)

- General LIFE / MIRECLE mission concept papers (Hammond context).

### Not read — no arXiv preprint or low-priority

c's bibliography is small (7 papers, 5 with arXiv). Only one was
marked `skipped` — Hill 2023 catalog. All others were deep-read or
skim. Preserved in `docs/phase3/_bib/teegarden-s-star-c.yaml`.

## Open items for follow-up

- **Hammond 2025 vs Wandel 2019**: The cfg's snowball pick relies on
  Hammond 2025's 3D ExoCAM result. Wandel 2019's older 1D analytic
  model gives a more optimistic H_atm = 1-12 habitability range for c.
  If a future independent 3D GCM (THAI-style intercomparison, or a
  ROCKE-3D study of c specifically) finds liquid water at substellar
  for high pCO₂, the cfg would shift to a marginal "eyeball with thin
  substellar warm spot" variant. For now, snowball is canonical.
- **2-bar CO₂ scenario**: Hammond 2025 tested up to 2 bar CO₂ with no
  surface melt. A higher CO₂ atmosphere (e.g., 10 bar Venus-like) was
  not tested and could in principle produce surface temperatures
  above freezing — but at that pressure other effects (CO₂
  condensation onto the nightside, atmospheric collapse) become
  important.
- **No transit confirmation**: All parameters RV-derived. Transit
  detection extremely unlikely given non-transiting geometry.
- **Subsurface ocean**: Hammond 2025 does not model interior structure.
  If c has a primordial water reservoir, a liquid subsurface ocean
  could exist beneath the global ice sheet — analogous to Europa.
  Cfg currently does not render a subsurface ocean as visible from
  orbit but could add one as a Kerbalism subsurface-water flag.
- **CO₂ frost cycling**: The nightside cold-trap may have a seasonal-
  scale (orbit-period) CO₂ frost deposition cycle. With P_orb = 11 d
  the cycle is fast; no published study explicitly models it for c.
- **Atmospheric escape over 8 Gyr**: Not modeled. The cfg assumes
  retention based on the quiet present-day star and the old age. A
  Lammer-style escape calculation specifically for c would tighten
  the atmospheric column.

## Related

- [teegardens-star](teegardens-star.md) — M7 V host
- [teegardens-star-b](teegardens-star-b.md) — inner sibling, temperate aquaplanet
- [teegardens-star-d](teegardens-star-d.md) — outer sibling, cold bare-rock
- [trappist-1-f](trappist-1-f.md) — sister-system analog at HZ outer edge (TRAPPIST-1 f is closer to snowball/eyeball boundary; c is fully snowball)
- [proxima-cen-b](proxima-cen-b.md) — Dreizler 2024 quotes ESI of c (0.88) as comparable
- [methodology](../reference/methodology.md) — Decisions schema
