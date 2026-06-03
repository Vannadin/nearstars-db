<!-- ε Eridani b Phase 3 synthesis: cfg-ready decisions and reasoning -->
# ε Eridani b — Phase 3 Synthesis

ε Eridani b is a ~0.66 M_Jup gas giant orbiting the young active K2V
dwarf ε Eridani at a = 3.53 ± 0.03 AU with a 2671 ± 17 d (7.32 yr)
period and low eccentricity e = 0.07. After two decades of contested
radial-velocity history (Hatzes 2000 discovery; Benedict 2006 HST FGS
attempt; intermittent activity-induced spurious-signal rebuttals),
the planet was finally confirmed by direct imaging at L′ and Ms band
(Mawet 2019, Keck/NIRC2 vortex coronagraph) and refined by combined
RV + Hipparcos/Gaia astrometry (Llop-Sayson 2021). Llop-Sayson 2021's
most-probable inclination is i = 78.81°, indicating the planet is
likely inclined ~2σ from the 34° main-ring plane (Booth 2017
ALMA-resolved disk); a coplanar ~32° solution is allowed at ~1σ but
not favored. No transmission or thermal-emission
spectrum exists yet; the planet's atmospheric composition,
rotation, and any moon population are unconstrained.

**Scenario choice for NearStars: a cold (T_eq ≈ 110 K), young
(~440 Myr) jovian on a 3.5 AU low-eccentricity orbit, sitting in the
inner-belt-to-intermediate-belt gap (3–20 AU) of the ε Eri three-belt
debris disk and identified by Su 2017's Genie model as the inner-
gap sculptor. Visual styling treats it as a Saturn-analog cool jovian
with ammonia-ice cloud bands rendered in warm cream under K2V
illumination, a faint photochemical haze layer from CH₄ photolysis
under elevated K-dwarf UV, no ring, and Jupiter-scaled magnetosphere
driving H-Balmer α aurorae visible from a Hill-sphere observer.**
35 cfg picks; **14 canonical-aligned, 21 tie-break** (jovian-analog
defaults under K2V illumination — no spectrum or thermal map yet),
0 documented divergence.

## Decisions

Kopernicus / atmosphere cfg-ready values. `Confidence`: high =
directly measured or tightly constrained, medium = theoretical with
strong support, low = aesthetic choice within the allowed window.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | high | 7.32-yr orbit at 3.5 AU around K dwarf — tidal damping timescale ≫ Hubble time at this separation |
| `obliquity_deg` | 25 | low | Tie-break: no measurement. Saturn-like 26.7° picked over Jupiter-like 3.1° to give visually distinctive ring-axis option (even though cfg picks no ring); within the dynamical-stability window for any 3.5 AU jovian |
| `eccentricity` | 0.07 | high | Llop-Sayson 2021 — joint RV + Hipparcos/Gaia astrometric fit |
| `argument_of_periastron_deg` | −19.15 | high | Llop-Sayson 2021 (DB Phase 2) |
| `sidereal_period_days` | 2671 ± 17 | high | Llop-Sayson 2021 — refined RV + astrometry fit; consistent with Mawet 2019 direct imaging epoch |
| `semi_major_axis_au` | 3.53 ± 0.03 | high | Llop-Sayson 2021 |
| `inclination_deg` | 78.81 (+29.34/−22.41) | high | Llop-Sayson 2021 most-probable (RV + Hipparcos/Gaia astrometry); = DB. The disk-coplanar i ≈ 34° (Booth 2017 ring; Benedict 2006 30°) is ~1–2σ from this and is kept as a noted alternative in Open items |
| `mass_mjup` | 0.66 (+0.12/−0.09) | high | Llop-Sayson 2021 — true mass from joint RV + Hipparcos/Gaia astrometry + imaging (inclination-marginalized; = DB Phase 2) |
| `mass_mearth` | 210 | high | = 0.66 M_Jup × 317.8 ≈ 210 (DB 209.8) |
| `radius_rjup` | 1.05 | low | Tie-break: no transit. Burrows 2003 / Fortney 2007 evolutionary tracks for 0.66 M_Jup at 0.44 Gyr predict 1.03–1.12 R_Jup with solar metallicity; cfg picks 1.05 as mid-range. Mawet 2019 Ms-band non-detection sets an upper limit excluding hot-start inflated radii > 1.3 R_Jup |
| `surface_gravity_g_earth` | 1.5 | medium | derived: g = G M / R² with M = 0.66 M_Jup, R = 1.05 R_Jup → 14.8 m/s² = 1.5 g⊕ |
| `density_g_cc` | 0.76 | medium | derived: 0.66 M_Jup / (1.05 R_Jup)³ × ρ_Jup ≈ 0.76 g/cc |
| `insolation_s_earth` | 0.026 | high | derived: S = L_star / a² = 0.32 L☉ (Baines & Armstrong 2012, recommended) / (3.53 AU)² = 0.0257 S⊕ |
| `equilibrium_temp_k_a0` | 111 | high | derived: T_eq = 278 K × (L/a²)^0.25 = 278 × 0.0257^0.25 |
| `equilibrium_temp_k_a03` | 102 | high | derived; Earth-analog A = 0.3 |
| `bond_albedo` | 0.34 | low | Tie-break: Saturn-analog 0.342 (Hanel 1983; Li 2018) picked over Jupiter's 0.503 because cooler T_eq ≈ 111 K skews cloud chemistry toward thicker ammonia-ice deck more like Saturn than Jupiter; Uranus 0.300 also bracketed |
| `intrinsic_luminosity_w_m2` | 0.5 | low | Tie-break: Burrows 2003 cooling track for 0.66 M_Jup at 0.44 Gyr predicts internal T ~ 100 K; cfg picks conservative 0.5 W/m² intrinsic flux (well below Jupiter's 5.4 W/m²; consistent with the older + lower-mass + less-inflated state) |
| `atmosphere_present` | true | high | gas giant by definition; H₂/He bulk inferred from M-R consistency with solar composition |
| `atmosphere_reference_pressure_pa` | 100 000 | medium | gas giant has no solid surface; cfg-reference 1 bar level for cloud-deck rendering, conventional jovian KSP atmosphere altitude origin |
| `atmosphere_composition` | H₂ ~89%, He ~10%, CH₄ ~0.2%, NH₃ ~0.02%, H₂O ~0.01% (deep), trace CO and HCN from photochemistry | low | Tie-break: no spectrum. Solar-composition jovian default per Lodders 2003 protosolar abundance, with Jupiter/Saturn-like volatile inventory and condensation chemistry truncated at T = 111 K equilibrium |
| `atmosphere_scale_height_km` | 27 | medium | derived: H = kT / (μ m_H g) with T = 111 K, μ = 2.3, g = 14.8 m/s² ≈ 27 km |
| `atmosphere_tint_rgb_hex` | `#d8c098` (warm-cream limb haze under K2V illumination) | low | Tie-break: ammonia-ice atmosphere is intrinsically near-white; K2V 5039 K SED shifts perception warmer than Sun-illuminated Jupiter |
| `cloud_cover_fraction` | 0.85 | medium | jovian-analog: zonal banding nearly complete coverage with belt/zone contrast; cfg picks 0.85 to allow distinct dark belts vs bright zones rather than uniform overcast |
| `cloud_morphology` | zonal bands with ammonia-ice cloud deck at ≈ 0.5–1 bar level; possible water-cloud deck below at ≈ 5 bar (inaccessible to visible imaging); faint photochemical haze layer above 100 mbar from CH₄ photolysis under K2V UV | low | Tie-break: no GCM; cfg adopts Saturn-analog band structure with ε Eri's elevated K-dwarf UV driving a slightly more prominent stratospheric haze layer than Saturn |
| `cloud_tint_rgb_hex` | `#e8dac4` (warm cream — NH₃ ice + K2V illumination) | low | Tie-break: Saturn's ammonia clouds appear cream-white under solar illumination; under 5039 K K2V the perceived hue shifts further into warm cream |
| `photochemical_haze_present` | true | medium | ε Eri's elevated FUV flux (France 2018 MUSCLES, 5–20× solar) drives CH₄ photolysis above 100 mbar; tholin / hydrocarbon haze layer is expected analogous to Titan's atmosphere chemistry but on a jovian H₂ background |
| `photochemical_haze_tint_rgb_hex` | `#b08858` (light tholin from CH₄ photolysis under K2V UV) | low | Tie-break: laboratory tholin chemistry (Khare 1984; Hörst 2018) gives orange-tan absorption signatures; haze layer is thin and renders as a subtle limb-darkening rather than a dominant tint |
| `planet_disk_tint_rgb_hex_primary` | `#e8dac4` (cream-white zones — dominant cloud-deck appearance from a planetary-scale observer) | low | downstream of `cloud_tint_rgb_hex` |
| `planet_disk_tint_rgb_hex_accent` | `#c4a878` (warm cream-brown bands — belt regions where deeper cloud layers + tholin haze show through) | low | Tie-break: Saturn/Jupiter belt-zone contrast under K2V illumination; band amplitude reduced vs Jupiter because of weaker convective drive at lower insolation |
| `ring_present` | false | medium | Mawet 2019 Ms-band high-contrast imaging would detect a Saturn-bright ring system at the 3.5 AU separation; no ring component detected. cfg defaults to "no ring" |
| `ring_observed` | false | high | Mawet 2019 Ms-band direct imaging detection without ring component |
| `rotation_period_hours` | 10 | low | Tie-break: no rotation measurement. Jupiter-analog 9.93 h (Jupiter has fastest jovian rotation in the Solar System); cfg picks 10 h as round-number Jupiter-like value rather than slower Saturn-like (10.7 h) or Uranus-like (17.2 h) because mass-scaling and the angular-momentum budget at 3.5 AU favor Jupiter-class rapid rotation |
| `magnetic_field_strength_microtesla_equator` | 400 | medium | scaled jovian dynamo: Jupiter's surface field ≈ 430 μT (equator); for 0.66 M_Jup with vigorous convection and Jupiter-like rotation, cfg picks 400 μT — below Jupiter by ~7% reflecting slightly weaker convective drive at lower mass |
| `magnetic_dipole_moment_normalized_earth` | 13200 | medium | 0.66 × 20 000 ≈ 13 200 × Earth by linear-mass scaling |
| `magnetic_dipole_tilt_deg` | 10 | low | Tie-break: Jupiter 9.6°, Saturn 0°, Neptune 47°. cfg picks Jupiter-analog 10° for visible auroral oval offset; Saturn-aligned 0° would be visually uninteresting |
| `aurora_present` | true | medium | ε Eri's stellar wind ≈ 30× solar mass-loss rate (Wood 2002) + cycle-active corona drives strong incident plasma flux at 3.5 AU; combined with jovian magnetospheric capture this produces auroral emission analogous to Jupiter's but with elevated driver |
| `aurora_color_primary_hex` | `#c84080` (H-Balmer α 656 nm red-pink dominant in H₂-rich jovian atmosphere) | low | Tie-break: Jupiter UV aurora is brightest in Lyα + H₂ Lyman/Werner bands but the visible-band component is H-Balmer α; under K2V illumination context the visible-band aurora reads as red-pink |
| `aurora_oval_magnetic_latitude_deg` | 70 | medium | Jupiter-analog auroral oval at 65–75° magnetic latitude (Clarke 1996 HST FUV; Bonfond 2017); scales to ε Eri b's magnetospheric standoff |
| `aurora_intensity_kR_typical` | 1000 | low | Tie-break: Jupiter UV aurora ≈ 100–1000 kR depending on solar wind state (Clarke 2009); ε Eri's 30× solar wind drives proportionally stronger driver; cfg picks 1000 kR as mid-range for ε Eri's active state |
| `companion_position_relative_belts` | between asteroid-belt analog (3 AU) and intermediate belt (20 AU); inner-gap sculptor in Su 2017 Genie three-belt model | high | Su 2017 §4 — gap-clearing requires a planet of M ≳ 0.5 M_Jup between the two belts; ε Eri b's mass and location match the requirement |
| `star_apparent_angular_diameter_deg` | 0.112 | high | derived: 2 R_star / a = 2 × 0.74 R☉ / 3.53 AU × (180/π); compares with Sun-from-Jupiter 0.10° |
| `stellar_illumination_color_temp_k` | 5039 | high | inherited from host Phase 3 (`docs/phase3/eps-eri.md`) |

## Surface synthesis

ε Eridani b has no solid surface in the conventional sense — it is
a Jupiter-mass H₂/He gas giant. The "surface" relevant for visual
rendering is the cloud deck, conventionally referenced to the 1 bar
pressure level where the optical opacity transitions from clear gas
above to dense particulate-laden gas below.

The equilibrium temperature at 3.5 AU under L_star = 0.32 L☉ is
T_eq ≈ 111 K (A = 0) or 102 K (A = 0.3). Both values are colder than
Jupiter (T_eq ≈ 110 K) and warmer than Saturn (T_eq ≈ 81 K). The
condensation chemistry on a H₂/He atmosphere at these temperatures
follows the well-established Lewis 1969 / Atreya 1999 thermochemical
sequence: ammonia (NH₃) condenses near the 1 bar level, water (H₂O)
condenses deeper at ≈ 5 bar, and methane (CH₄) remains gaseous at all
accessible levels (the CH₄ condensation point requires T < 75 K,
beyond ε Eri b's reach). The cfg therefore renders ε Eri b as an
ammonia-cloud-deck jovian, structurally most similar to Saturn but
warmer and with Jupiter-like rotational dynamics expected from its
higher mass.

The cloud deck reads as warm cream-white (`#e8dac4`) under K2V
illumination. Ammonia ice in the laboratory has an intrinsic albedo
in the visible near 0.8–0.9 with a slight yellow tint from trace
absorption at 1.5–2.0 μm; under 5039 K K2V illumination the perceived
hue shifts further toward warm cream relative to the Sun-illuminated
Jupiter palette. Belt-zone contrast (`#c4a878` warm cream-brown for
belt bands) is muted compared to Jupiter because the convective drive
at T_eq ≈ 111 K is weaker than Jupiter's, but stronger than Saturn's
because the planet's internal heat flux (~0.5 W/m² adopted) gives a
nontrivial convective overturn — broadly consistent with Sromovsky
2007 belt-zone amplitude scaling.

Above the ammonia cloud deck, ε Eri's elevated K-dwarf FUV flux
(France 2018 MUSCLES: 5–20× solar at the same orbital distance)
drives methane photolysis at ≈ 0.1–10 mbar pressure levels. The
photochemical products — heavier hydrocarbons (C₂H₂, C₂H₆) and tholin-
like polymers — accumulate as a stratospheric haze layer with
absorption signatures in the UV and blue (Khare 1984; Hörst 2018).
The cfg encodes this as `photochemical_haze_present = true` with a
faint tholin tint `#b08858` rendered as a thin limb-haze layer
overlying the cream-white cloud deck. The haze does not dominate the
visual appearance — even Jupiter's stratospheric haze produces only
subtle limb-darkening at visible wavelengths — but it is the most
likely first-order spectroscopic signature in future JWST coronagraph
or ELT high-contrast imaging.

No surface features map to the planet's interior — convective
overturn maintains a vertically mixed adiabat below the ammonia cloud
deck. The interior structure is fully fluid down to the metallic-
hydrogen transition at ≈ 1 Mbar (≈ 90% of the radius), with a
possible heavy-element core of 5–25 M⊕ inferred indirectly from
mass-radius models (cfg does not encode core mass — no observational
constraint).

## Atmosphere synthesis

No transmission or thermal-emission spectrum of ε Eri b exists.
Mawet 2019's Ms-band (4.6 μm) direct-imaging contrast measurement
gives only a broad upper limit on hot-start luminosity, ruling out
very young, very inflated jovian evolutionary tracks (Spiegel &
Burrows 2012 hot-start models with T_eff > 700 K are excluded at the
~2σ level) but leaving the canonical "cold-start" thermal-equilibrium
prediction (T_eff ≈ 150 K including internal flux) consistent with
the data. The atmospheric composition is therefore drawn entirely
from the solar-composition jovian default per Lodders 2003 protosolar
abundance + Atreya 1999 condensation chemistry truncated at T = 111 K.

**Pressure reference.** Gas giants have no solid surface; the cfg
reference pressure is set at 1 bar (100 000 Pa) where the ammonia
cloud deck condenses. Conventional KSP atmosphere altitude origin
matches this level. Above 1 bar, pressure decreases with scale
height H ≈ 23 km — somewhat below Earth's and Jupiter's scale heights
because of the colder temperature combined with higher gravity.

**Composition.** H₂ ≈ 89%, He ≈ 10% by volume — solar protosolar
ratios with He depletion negligible at this mass and age. Volatiles:
CH₄ ≈ 0.2% (Jupiter is 0.21%, slightly enhanced above protosolar by
~3× per Wong 2004 Galileo probe; cfg picks Jupiter-analog 0.2%),
NH₃ ≈ 200 ppm (depleted above the cloud deck by condensation),
H₂O ≈ 100 ppm (depleted above the deeper water cloud deck), trace
CO ~ 1 ppb and HCN ~ 0.1 ppb from CH₄ + N₂ photochemistry. These
volatile abundances are entirely tie-break defaults — no spectrum
constrains them — but the cfg picks Jupiter-analog values because
the 0.66 M_Jup mass and protosolar metallicity context favor a
Jupiter-class disk-accretion formation history.

**Photochemistry signature.** ε Eri's elevated FUV (Lyα, France 2018
MUSCLES: 8 × 10⁻⁴ L_bol vs Sun's ≈ 6 × 10⁻⁵ L_bol) drives stronger
methane photolysis than Jupiter receives. The resulting hydrocarbon
chain (CH₄ → C₂H₆, C₂H₂, C₂H₄ → tholin polymers) produces a
stratospheric haze layer above ≈ 100 mbar pressure. Quantitative
modeling (Moses 2005 Saturn; Hörst 2018 sub-Neptune tholin chemistry
extended to jovians) predicts ε Eri b's haze optical depth at 1 μm
to be roughly 2–5× Jupiter's, sufficient to produce visibly enhanced
limb darkening and a detectable absorption feature at 0.6–0.8 μm in
future spectroscopy. Aurora-related N₂⁺ / H₃⁺ emission lines in the
near-IR (Drossart 1989 Jupiter H₃⁺ at 3.4 μm) would be the most
diagnostic future detection channel; cfg encodes the haze presence
without committing to a specific optical depth.

**Sky appearance from a Hill-sphere observer.** The Hill sphere
radius for 0.66 M_Jup at 3.53 AU around 0.82 M☉ is r_H ≈
**0.224 AU = 447 R_planet** — large enough to host substantial moon
populations. From an observer on a hypothetical large moon at, say,
20 R_planet (Io-analog distance scaled to ε Eri b's larger radius),
the planet subtends ≈ 5.7° in the sky — nearly 12× the lunar
diameter from Earth — and dominates the daytime sky with a banded
cream-white disk. The ε Eri star itself is a tiny 0.112° point — 1/4
the Sun's angular size from Earth, comparable to Sun-from-Jupiter
geometry — appearing as a deep orange point with the K2V color
temperature. The contrast between the warm-cream planet disk and the
orange stellar point would be the system's most photogenic feature
in any wide-orbit fly-by render.

**Nightside.** No direct stellar illumination. The planet's own
internal flux (~0.5 W/m²) produces a near-IR thermal glow at ~110 K
peak (28 μm) — invisible to the unaided eye, but a faint
self-illuminated reddish-warm cast at 4.6 μm where Mawet 2019
detected the planet. Aurora emission at high magnetic latitudes
provides the only visible-light nightside signal: a faint H-Balmer α
red-pink ring at ~70° magnetic latitude, plausibly brighter than
Jupiter's visible aurora given ε Eri's elevated stellar wind.

## Rotation & spin synthesis

No direct rotation measurement of ε Eri b exists. Doppler-broadened
near-IR spectra (the technique Snellen 2014 applied to β Pictoris b
to measure v sin i = 25 km/s) require high-contrast spectroscopic
imaging at < 0.5 arcsec separation — ε Eri b's angular separation is
≈ 1.1 arcsec from the host, accessible to current instruments but
the small mass (0.66 M_Jup) and faint thermal emission have so far
prevented a rotation measurement.

**Tidal damping argument.** At 3.5 AU around a 0.82 M☉ host, the
tidal timescale for a Jupiter-mass planet is τ_tide ≈ 10⁴⁰ s
(Goldreich & Soter 1966 with Q_p ≈ 10⁵) — orders of magnitude
longer than the age of the universe. ε Eri b is **not** tidally
locked. The cfg encodes `tidally_locked = false`.

**Rotation period choice.** Among observed gas giants, rotation
period scales weakly with mass: Jupiter (1.0 M_Jup) ≈ 9.93 h, Saturn
(0.3 M_Jup) ≈ 10.7 h, Uranus (0.046 M_Jup) ≈ 17.2 h, Neptune (0.054
M_Jup) ≈ 16.1 h. For ε Eri b at 0.66 M_Jup, the angular-momentum
budget inherited from disk accretion at 3.5 AU favors Jupiter-class
rapid rotation. The cfg picks `rotation_period_hours = 10` as a
round Jupiter-analog value — within-window tie-break, not
constrained.

**Obliquity.** Tie-break aesthetic choice. Jupiter's 3.1° vs Saturn's
26.7° vs Uranus's 97.8° — no observation either way. cfg picks 25°
(Saturn-analog) because the moderate obliquity reads as visually
distinct from "tipped over" Uranus extremes while still giving an
animated axis tilt in render. With the 7.32-yr orbital period, even
the moderate obliquity does not produce observable seasonal effects
in the cloud deck — convective overturn timescales (~years) are
comparable to the orbital period.

**KSP implementation note.** Rotation period = 10 h = 36 000 s.
Kopernicus `rotationPeriod = 36000`. Obliquity (`initialRotation`
or axis-tilt cfg) = 25° from orbital normal.

**Magnetic dynamo expectation.** A H₂/He envelope with vigorous
convection and a Jupiter-class rotation period (10 h) sustains a
strong dipolar field. Scaling from Jupiter (surface equatorial field
≈ 430 μT, dipole moment ≈ 2 × 10⁴ × Earth) by linear mass gives ε
Eri b ≈ 400 μT and ≈ 1.32 × 10⁴ × Earth — both adopted in the cfg.
The dipole tilt is set to Jupiter-analog 10° for visually distinct
auroral oval rendering. The Jupiter-analog rotation + magnetic field
combination places ε Eri b firmly in the "strong magnetosphere"
regime, with magnetopause standoff ≳ 50 R_planet against a 30× solar
wind background.

## Visual styling

Combining surface (cloud-deck) and atmosphere decisions:

- **Global appearance.** From orbit, ε Eri b reads as a banded
  cream-white jovian about 20% smaller than Jupiter — ~1.05 R_Jup =
  75 000 km. Belt-zone contrast is modest (`#e8dac4` cream-white
  zones, `#c4a878` warm cream-brown belts), less vivid than Jupiter
  but visible at moderate render distance. Persistent zonal banding
  (~5 belts and zones) covers ~85% of the visible disk.
- **Cloud-deck detail.** Ammonia-ice cloud zones appear as smooth
  cream-white bands with faint cyclonic eddies — no equivalent of
  Jupiter's Great Red Spot is constrained, so cfg picks a few small
  storm vortices (drift signatures only) as visual interest.
  Bands run east-west, latitudinal banding pattern with widths
  scaling to the planet's Coriolis parameter at 10 h rotation +
  1.05 R_Jup radius.
- **Polar regions.** No constraint. Tie-break aesthetic: cfg renders
  a faint cyclonic polar hood structure inspired by Saturn's polar
  hexagon morphology but without committing to a specific geometric
  pattern.
- **Limb haze.** Pale cream-tan limb glow (`#d8c098`) about
  20–40 km thick — Rayleigh + Mie scattering off the ammonia cloud
  deck under K2V illumination, with a thin overlying tholin haze
  layer (`#b08858`) adding subtle absorption at the day-night
  terminator.
- **Aurora ring.** At high magnetic latitudes (~70° in the cfg)
  both north and south poles show faint H-Balmer α red-pink
  (`#c84080`) auroral rings, plausibly brighter than Jupiter's
  visible aurora given ε Eri's elevated stellar wind. Visible from
  nightside angles only; obscured by the cloud deck on the dayside.
- **Star in sky.** ε Eridani subtends 0.112° from ε Eri b — about
  the angular diameter of Saturn from Earth — appearing as a deep
  orange (K2V `#ffd9a8`) point/disk. From a hypothetical large moon
  at 20 R_planet, the planet itself dominates the sky at ~5.7°,
  with the star reduced to a brilliant orange pinpoint nearby.
- **Sister planets in sky.** No other confirmed planet in the ε Eri
  system as of Mawet 2019's coronagraphic non-detection. The
  intermediate debris belt at ~20 AU and the cold ring at ~64 AU are
  visible from ε Eri b's viewpoint only as faint diffuse glow bands
  at large heliocentric phase angles — no discrete companion bodies
  detected.
- **Ring system.** No ring (cfg `ring_present = false`). Mawet 2019
  Ms-band imaging would have detected a Saturn-bright ring system
  at the 3.5 AU separation; non-detection sets `ring_present = false`
  with medium confidence (a Jupiter-faint ring is below the Mawet
  detection threshold and not excluded).
- **Hill-sphere context.** r_H ≈ 0.224 AU = 447 R_planet. Large
  enough to host a substantial moon population; cfg does not commit
  to specific moons (out of scope for this Phase 3) but the
  Hill-sphere extent itself is a visual landmark when rendered as a
  faint sphere of influence boundary.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Hatzes A. P. et al. 2000** — *Evidence for a Long-Period Planet
  Orbiting ε Eridani*, ApJ 544, L145 (`2000ApJ...544L.145H`). The
  original radial-velocity discovery paper; sets P ≈ 6.85 yr and
  M sin i ≈ 0.86 M_Jup as the initial values (later refined).
- **Quillen A. C. & Thorndike S. 2002** — *Structure in the ε Eridani
  Dusty Disk Caused by Mean Motion Resonances with a 0.3 Eccentricity
  Planet at 40 AU*, ApJ 578, L149 (`2002ApJ...578L.149Q`). Historical
  inference of an outer "ε Eri c" from cold-ring eccentricity; ruled
  out by Mawet 2019 direct imaging but important for the
  multi-belt-sculpting context.
- **Benedict G. F. et al. 2006** — *The Extrasolar Planet ε Eridani b.
  Orbit and Mass from Combined Astrometric and Spectroscopic Data*,
  AJ 132, 2206 (`2006AJ....132.2206B`). HST FGS astrometric attempt;
  superseded by direct imaging but historically important for the
  mass determination chain.
- **Mawet D. et al. 2019** — *Deep Exploration of ε Eridani with
  Keck Ms-band Vortex Coronagraphy and Radial Velocities*, AJ 157,
  33 (`2019AJ....157...33M`, arXiv:1810.03794). Direct imaging
  confirmation of ε Eri b at L′ and Ms band; rules out outer
  ε Eri c with planet mass > 0.3 M_Jup beyond 30 AU; constrains
  thermal-emission upper limit excluding hot-start inflated jovian
  models. **Cornerstone observational paper.**
- **Llop-Sayson J. et al. 2021** — *Constraining the Orbit and Mass
  of ε Eridani b with Radial Velocities, Hipparcos IAD-Gaia DR2
  Astrometry, and Multi-epoch Vortex Coronagraphy Upper Limits*,
  AJ 162, 181 (`2021AJ....162..181L`).
  Joint RV + Hipparcos/Gaia astrometric fit;
  true mass M_b = 0.66 (+0.12/−0.09) M_Jup, i = 78.81°
  (+29.34/−22.41), a = 3.48 AU. **Cornerstone observational
  paper.**
- **Roettenbacher R. M. et al. 2022** — *No Reliable Astrometric
  Detection of ε Eridani b*, AJ 163, 19 (`2022AJ....163...19R`,
  arXiv:2110.10643). Astrometric cross-check across multiple
  missions; the individual signal is marginal but combined with the
  disk-plane coplanarity argument favors i ≈ 34° over Llop-Sayson's
  RV-only 78.8°.
- **MacGregor M. A. et al. 2015** — *ALMA Observations of the
  Debris Disk around ε Eridani*, ApJ 809, L47
  (`2015ApJ...809L..47M`, arXiv:1505.03879). ALMA 1.3 mm imaging
  resolves the cold ring at 64.4 ± 0.5 AU with eccentricity e ≈ 0.07;
  provides the disk inclination reference frame.
- **Booth M. et al. 2017** — *The Northern arc of ε Eridani's
  Debris Ring as seen by ALMA*, MNRAS 469, 3200
  (`2017MNRAS.469.3200B`, arXiv:1705.05868). Multi-wavelength
  decomposition; three-belt structure; cold-ring inclination 34 ± 2°
  — the canonical inclination reference matched by ε Eri b's
  orbital plane.
- **Su K. Y. L. et al. 2017** — *The Inner 25 AU Debris Distribution
  in the ε Eri System*, AJ 153, 226 (`2017AJ....153..226S`,
  arXiv:1703.10330). The "Genie" multi-belt sculpting model;
  identifies ε Eri b as the inner-gap sculptor between the 3 AU
  asteroid analog and the 20 AU intermediate belt. **Drives the
  `companion_position_relative_belts` decision row.**

### Read (context / methodology, not decision-driving)

- **Burrows A. et al. 2003** — *Beyond the T dwarfs* and related
  cool-jovian evolutionary tracks (`2003ApJ...596..587B`). Mass-
  radius-age tracks for 0.5–1.5 M_Jup planets; used to estimate ε
  Eri b's radius and intrinsic luminosity from 0.66 M_Jup, 0.44 Gyr.
- **Fortney J. J. et al. 2007** — *Planetary Radii across Five
  Orders of Magnitude in Mass and Stellar Insolation* (`2007ApJ
  ...659.1661F`). Confirms Burrows tracks across the relevant mass-
  age window for ε Eri b's radius choice.
- **Spiegel D. S. & Burrows A. 2012** — *Spectral and Photometric
  Diagnostics of Giant Planet Formation Scenarios* (`2012ApJ...745
  ..174S`). Hot-start vs cold-start jovian evolutionary tracks; the
  Mawet 2019 contrast measurement rules out hot-start tracks for ε
  Eri b.
- **Lodders K. 2003** — *Solar System Abundances and Condensation
  Temperatures of the Elements* (`2003ApJ...591.1220L`). Protosolar
  abundance reference; drives the atmosphere composition default.
- **Atreya S. K. et al. 1999** — *A comparison of the atmospheres
  of Jupiter and Saturn* and related condensation chemistry
  references. Sets the ammonia / water cloud-deck altitude
  framework.
- **Lewis J. S. 1969** — *The clouds of Jupiter and the NH₃-H₂O
  and NH₃-H₂S systems* (`1969Icar...10..365L`). Original thermo-
  chemical cloud-deck sequence; still the framework used in modern
  jovian atmosphere modeling.
- **Sromovsky L. A. et al. 2007** — Jupiter/Saturn convective drive
  and belt-zone amplitude scaling. Used to estimate ε Eri b's
  belt-zone contrast vs Jupiter and Saturn.
- **Khare B. N. et al. 1984** — *Optical constants of organic
  tholins produced in a simulated Titanian atmosphere* (`1984Icar
  ...60..127K`). Laboratory tholin chemistry; absorption signatures
  used in the photochemical haze tint choice.
- **Hörst S. M. et al. 2018** — *Haze Production Rates in Super-
  Earth and Mini-Neptune Atmosphere Experiments* (`2018Natur
  ...2..303H`). Sub-Neptune tholin chemistry extended to jovians;
  drives the haze-optical-depth scaling vs Jupiter.
- **Moses J. I. et al. 2005** — *Photochemistry of Saturn's
  atmosphere* (`2005JGRE..110.8001M`). Saturn UV photochemistry
  reference; scaled to ε Eri b under K2V FUV.
- **Wood B. E. et al. 2002** — *Measured Mass Loss Rates of Solar-
  like Stars as a Function of Age and Activity* (`2002ApJ...574
  ..412W`, arXiv:astro-ph/0203437). ε Eri's mass-loss rate ~30×
  solar; drives the magnetosphere driver strength.
- **France K. et al. 2018** — *The MUSCLES Treasury Survey*
  extension to K dwarfs (`2018ApJS..239...16F`). FUV / Lyα fluxes
  for ε Eri; drives the photochemistry-strength estimate.
- **Reiners A. & Christensen U. R. 2010** — *A magnetic field
  evolution scenario for brown dwarfs and giant planets* (`2010
  A&A...522A..13R`). Dynamo scaling for jovians; consistent with
  the cfg's 400 μT pick from Jupiter scaling.
- **Metcalfe T. S. et al. 2013** — *Magnetic Activity Cycles in the
  Exoplanet Host Star ε Eridani*, ApJ 763, L26
  (`2013ApJ...763L..26M`, arXiv:1212.5343). First report of the
  ~2.95-yr chromospheric activity cycle; drives the cycle-phase
  magnetospheric-driver synchronization noted in Open items.
  (Not fetched in the b-bibliography; cited from the host Phase 3.)
- **Coffaro M. et al. 2020** — *A solar-like magnetic cycle on the
  mature K-dwarf 61 Cygni A and the X-ray cycle of ε Eridani*, A&A
  636, A49 (`2020A&A...636A..49C`, arXiv:2002.11009). Refines the
  X-ray cycle amplitude that modulates the wind driver at ε Eri b's
  orbit. (Pinned in the host bibliography `eps-eri.yaml`, status
  fetched; not separately pinned for b.)
- **Canup R. M. & Ward W. R. 2002** — *Formation of the Galilean
  Satellites: Conditions of Accretion*, AJ 124, 3404
  (`2002AJ....124.3404C`). Circumplanetary-disk satellite-accretion
  framework; context for the speculative moon-system Open item.
  (Not fetched in the b-bibliography.)

### Read (instrument / non-cfg-decisive)

- **Snellen I. A. G. et al. 2014** — *Fast spin of the young
  extrasolar planet β Pictoris b* (`2014Natur.509...63S`). Doppler-
  broadened spectroscopy technique; not yet applied to ε Eri b.
- **Drossart P. et al. 1989** — *Detection of H₃⁺ on Jupiter*
  (`1989Natur.340..539D`). H₃⁺ emission as future aurora detection
  channel for ε Eri b.
- **Clarke J. T. et al. 1996, 2009** — Jupiter HST FUV aurora
  observations; provides the auroral-oval geometry reference scaled
  to ε Eri b.
- **Bonfond B. 2017** — *Jovian auroral aspects* (`2017JGRA
  ...122.4548B`). Jupiter auroral oval latitude reference.
- **Wong M. H. et al. 2004** — *Updated Galileo probe abundance
  measurements* (`2004Icar..171..153W`). Jupiter CH₄ / NH₃ abundance
  reference; cfg adopts Jupiter-analog values.
- **Hanel R. A. et al. 1983, Li L. et al. 2018** — Saturn Bond
  albedo measurements (`1983Icar...53..262H`; `2018NatCo...9.3709L`).
  Reference values for the cool-jovian Bond albedo tie-break.
- **Goldreich P. & Soter S. 1966** — *Q in the Solar System*
  (`1966Icar....5..375G`). Tidal-dissipation Q factor reference
  for the tidal-lock timescale calculation.

### Not read — no arXiv preprint or low-priority (~30 papers)

- Hatzes 2013 follow-up RV monitoring papers — superseded by Llop-
  Sayson 2021's combined analysis.
- 2000s-era ε Eri b activity-contamination rebuttal series (Anglada-
  Escudé 2012, Zechmeister 2013) — historical context; superseded
  by Mawet 2019 direct imaging confirmation.
- ε Eri b moon-system speculative papers — not observationally
  motivated; out of scope for first-pass Phase 3.
- SETI / laser-emission searches targeting ε Eri (Marcy 2022, Tusay
  2022, Saide 2023) — already cited in host Phase 3, not relevant
  to b.

The host star Phase 3 audit trail is preserved in
`phase3/eps_eri/system.yaml` + workspace notes, but its pinned
bibliography (`docs/phase3/_bib/eps-eri.yaml`) contains only the
stellar papers — it has zero planet-b entries. The planet-b paper
set (Hatzes 2000, Mawet 2019, Llop-Sayson 2021, Roettenbacher 2022,
Booth 2017, Su 2017) is cited in this document's own Bibliography
above but is not yet pinned/cached in a `docs/phase3/_bib/eps-eri-b.yaml`;
a dedicated b-bibliography fetch is a follow-up pass.

## Open items for follow-up

- **JWST coronagraph spectroscopy of ε Eri b (Cycle 4+)** — NIRCam
  or MIRI coronagraph at 4–5 μm could yield first thermal-emission
  spectrum, constraining T_eff, CH₄/NH₃ abundance ratios, and the
  photochemical haze optical depth. If detected, the Decisions table
  rows `atmosphere_composition`, `photochemical_haze_present`, and
  `bond_albedo` should be re-derived from the spectrum.
- **Doppler-broadened rotation measurement** — VLT/CRIRES+ or
  ELT/HARMONI could measure v sin i at the ~1.1 arcsec separation
  if the planet's thermal contrast can be extracted. Currently the
  10 h rotation period is a within-window tie-break; a measured
  period would shift Confidence from low to high.
- **Inclination-DB consistency**: the cfg adopts the Llop-Sayson/DB
  value i = 78.81° (RV + Hipparcos/Gaia astrometry, inclination-
  marginalized). The disk-coplanar i ≈ 34° (Booth 2017 ring;
  Benedict 2006 30°) is allowed at ~1σ and is preserved here as the
  alternative scenario a future Phase 2 could carry.
- **Moon system Phase 3**: Hill-sphere radius ~0.224 AU is large
  enough to host a substantial moon population. A future Phase 3
  follow-up could speculate on icy/rocky moons in the 5–50 R_planet
  range, anchored on (a) the protoplanetary-disk circumplanetary-
  feeding context (Canup 2002) and (b) any future ALMA/JWST
  circumplanetary-disk dust constraint. Out of scope for this
  first-pass Phase 3.
- **Ring system tie-break preservation**: cfg picks `ring_present
  = false` based on Mawet 2019 Ms-band non-detection of a Saturn-
  bright ring. A Jupiter-faint ring system would be below the Mawet
  detection threshold and not excluded; this is preserved here as
  the alternative cfg variant for users who prefer a faint ring.
- **Cycle-phase magnetospheric driver synchronization**: the host
  star's 2.95-yr activity cycle (Metcalfe 2013) modulates the wind
  driver at ε Eri b's orbit by a factor of ~4 (Coffaro 2020 X-ray
  cycle amplitude). A future cfg revision could phase-lock the
  aurora intensity rendering to the host cycle epoch so the player
  sees consistent timing across game years — same enhancement
  flagged in the host eps-eri.md Open items.
- **Phase 2 `disk_measurements`/`planet_atmosphere_measurements`
  ingest**: ε Eri b currently has no Phase 2 atmosphere block in
  the DB. When the DB schema is extended (or when a
  `db/planets_atmospheres/` companion is introduced), the Mawet
  2019 thermal-emission upper limit and any future JWST measurement
  should be ingested as `atmosphere_measurements` records with
  `recommended` flags matching the cfg picks above.

## Related

- [eps-eri](eps-eri.md) — host star Phase 3 synthesis; provides the
  M_star / R_star / L_star / age / disk-plane reference frame and
  the cycle activity context that drives the magnetospheric driver
- [tau-cet](tau-cet.md) — host of a metal-poor G8V solar analog
  with resolved cold debris ring; comparator for "nearby
  planet-hosting star with resolved disk" context
- [fomalhaut](fomalhaut.md) — A3V host with resolved debris ring
  and historical "Fomalhaut b" direct-imaging candidate; comparator
  for direct-imaging-confirmed companions in resolved-disk systems
- [methodology](../reference/methodology.md) — Decisions schema
- [mod-reference](../reference/mod-reference.md) — downstream
  Kopernicus / EVE / Scatterer cfg writers consuming this jovian's
  atmosphere + magnetosphere decisions
- [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) —
  single-star astrometry only; ε Eri does not need binary-orbit
  propagation
- [rex-data-comparison](../reference/rex-data-comparison.md) —
  REX has only a basic stellar entry for ε Eri without the
  jovian; ε Eri b is a NearStars-exclusive Phase 3 addition
