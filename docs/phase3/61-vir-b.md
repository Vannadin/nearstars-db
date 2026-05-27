<!-- 61 Vir b Phase 3 synthesis: cfg-ready decisions and reasoning -->
# 61 Vir b — Phase 3 Synthesis

61 Vir b is the innermost of three RV-detected planets around the
G6.5V solar twin 61 Virginis, reported by Vogt et al. 2010 (HIRES + AAT
joint solution). The detection is radial-velocity-only; the planet does
not transit, so the directly measured quantities are limited to orbital
period P = 4.215 ± 0.0006 d, semi-major axis a = 0.0502 AU, eccentricity
e = 0.12, argument of periastron ω = 105°, and minimum mass Msini =
5.1 ± 0.5 M⊕. The true mass is at least 5.1 M⊕ and most plausibly in
the 5–7 M⊕ range under the system's likely near-edge-on inclination
posterior. No radius has been measured; reflected-light direct
imaging is a future-class observation (HabEx / LUVOIR era), so the
ground-state atmosphere is currently unconstrained.

**Scenario choice for NearStars: a tidally-locked hot super-Earth with
a magma-ocean dayside, cooled nightside, vestigial silicate-vapor
exosphere, and no visible Rayleigh atmosphere.** This is the
CoRoT-7b / 55 Cnc e cosmochemical archetype applied to b's slightly
cooler insolation (S ≈ 326 S⊕, T_eq(A=0) ≈ 1180 K, T_eq(A=0.3) ≈
1080 K). The alternative — a retained steam-and-CO₂ runaway-Venus
atmosphere — is preserved as a cfg variant in Open items because b's
escape budget at 326 S⊕ does not unambiguously force the airless
reading.

## Decisions

Kopernicus / atmosphere cfg-ready values. `Confidence`: high =
directly measured or tightly constrained, medium = theoretical with
strong support, low = aesthetic choice within the allowed window.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 4.215 d orbit at 0.050 AU; tidal-locking timescale ~10⁵–10⁶ yr (Vinson 2017 scaling for 5 M⊕, G-dwarf host) ≪ 6 Gyr system age |
| `obliquity_deg` | 0 | high | tidal damping |
| `eccentricity` | 0.12 | high | Vogt 2010 RV fit |
| `argument_of_periastron_deg` | 105 | high | Vogt 2010 |
| `sidereal_period_days` | 4.215 | high | Vogt 2010 |
| `semi_major_axis_au` | 0.0502 | high | Vogt 2010 |
| `mass_mearth` | 5.1 | high | Vogt 2010 Msini; lower bound only (RV-only) |
| `radius_rearth` | 1.65 | medium | Tie-break: no transit; mass–radius scaling Zeng 2016 for a 5–7 M⊕ rocky-Earth-composition core gives R ≈ 1.5–1.8 R⊕; cfg picks 1.65 R⊕ as the Earth-composition mid-range |
| `surface_gravity_g_earth` | 1.87 | medium | derived = 5.1 / 1.65² (Earth-composition core) |
| `density_g_cc` | 6.27 | medium | derived; consistent with Earth-like rocky-iron mix |
| `insolation_s_earth` | 326 | high | derived from L = 0.82 L☉ and a = 0.0502 AU |
| `equilibrium_temp_k` (A=0) | 1180 | high | derived |
| `equilibrium_temp_k` (A=0.3) | 1080 | high | derived |
| `bond_albedo` | 0.1 | medium | Tie-break: range 0.05–0.2 for hot dark silicate / partial-melt surface; cfg picks 0.1 (CoRoT-7b / 55 Cnc e analog) |
| `dayside_surface_temp_k` | 1450 | medium | Tie-break: airless extreme (no redistribution) gives substellar T_substellar = T_eq × √2 × (1−A)^0.25 ≈ 1450 K; matches Léger 2009 CoRoT-7b template — above silicate solidus (~1500 K for basalt but partial melt at 1300+ K) |
| `nightside_surface_temp_k` | 200 | medium | Tie-break: airless cold-trap with thermal inertia for a partially molten dayside; cfg picks 200 K — colder than Mercury's nightside ~100 K because b has a longer 4.2 d night |
| `atmosphere_present` | false (vestigial silicate vapor only) | medium | Tie-break: primary H/He envelope photoevaporated long ago (Owen & Wu 2017 valley physics for 5 M⊕ at 0.05 AU around G-star: ≲ 50 Myr loss); secondary steam atmosphere would require continuous outgassing exceeding the ~10⁹ g/s XUV-driven loss rate, which is not guaranteed; cfg picks airless with a Mercury-analog mineral vapor exosphere |
| `atmosphere_surface_pressure_pa` | 10⁻⁷ | medium | Tie-break: silicate-vapor exosphere from substellar mantle / magma sublimation; column density ~10¹² atoms/cm² → equivalent surface pressure ~10⁻⁷ Pa (Schaefer & Fegley 2009 hot-rocky outgassing scaling) |
| `atmosphere_composition` | Na, K, SiO, O₂ silicate-vapor exosphere (sputter + thermal) | low | Tie-break: hot-rocky outgassing chemistry (Schaefer & Fegley 2009 for CoRoT-7b class); Na/K dominate by vapor pressure, SiO/O₂ secondary |
| `atmosphere_scale_height_km` | n/a | high | exospheric, no hydrostatic atmosphere |
| `atmosphere_tint_rgb_hex` | n/a (no visible atmosphere) | high | exospheric column too low for visible scattering or absorption |
| `cloud_cover_fraction` | 0 | high | no atmosphere |
| `cloud_morphology` | n/a | high | no atmosphere |
| `cloud_tint_rgb_hex` | n/a | high | no atmosphere |
| `ocean_present` | false | high | T_dayside > 1400 K rules out surface water; nightside too cold but no atmospheric transport to deliver volatiles |
| `surface_tint_rgb_hex_primary` | `#3a2a22` (dark partial-melt basaltic crust) | medium | Tie-break: dayside magma + cooled basaltic plains under solar G-dwarf illumination; cfg picks dark brown-black tone consistent with CoRoT-7b / 55 Cnc e expectations |
| `surface_tint_rgb_hex_accent` | `#c84a18` (substellar magma ocean glow) | low | Tie-break: substellar partial-melt region at ~1450 K radiates in red-orange (Wien peak at 2 μm but visible tail prominent); interesting-first picks a visible lava-glow accent over a uniformly dark surface |
| `surface_morphology` | substellar magma ocean ~1500 km radius; basaltic cooled plains in mid-latitudes; volatile-stripped nightside regolith | medium | Tie-break: Léger 2009 CoRoT-7b magma-ocean template; substellar isotherm at silicate solidus gives ~30° magma-pond radius |
| `tidal_heating_w_m2` | 0.1–1 | medium | Bolmont 2020 scaling for e=0.12 at 4.2 d period; eccentricity contribution is non-trivial but modest at this mass; supplements but does not dominate the insolation budget |
| `radiogenic_heat_w_m2` | 0.05 | medium | Earth-analog at 5 M⊕ × 6 Gyr decay; consistent with a partially molten interior |
| `star_apparent_angular_diameter_deg` | 1.02 | high | derived: 2 × R★ / a × (180/π); 0.963 R☉ at 0.0502 AU |
| `stellar_illumination_color_temp_k` | 5552 | high | host Teff |

## Surface synthesis

61 Vir b is the RV-only super-Earth archetype of a hot inner planet
around a solar-twin host. Three observational anchors pin the
synthesis:

1. **Insolation 326 S⊕** is the canonical "lava world" regime. Léger
   2009 introduced this regime with CoRoT-7b (4.8 M⊕, S ≈ 2500 S⊕, T_eq
   ≈ 1810 K), and 55 Cnc e (8 M⊕, S ≈ 2400 S⊕, T_eq ≈ 2000 K) extended
   it; b sits at the cooler end of the lava-world family with T_eq
   ≈ 1180 K. At this temperature, a basaltic surface is solid in the
   bulk and partial-melt in the substellar hemisphere only, rather
   than fully molten across the dayside.

2. **No transit and no JWST follow-up.** The planet's true mass and
   radius are unconstrained; b will not be transit-characterized
   without a future astrometric inclination or direct-imaging campaign.
   The cfg adopts Zeng 2016 mass–radius scaling for an Earth-composition
   rocky core: R ≈ 1.65 R⊕ for Msini = 5.1 M⊕, with surface gravity
   1.87 g⊕ and bulk density 6.27 g/cc.

3. **Cosmochemical context.** 61 Vir's [Fe/H] ≈ 0.0 dex (Pavlenko
   2012) and ~6 Gyr age give b an Earth-analog initial volatile
   inventory but a much harsher atmospheric loss history. Owen & Wu
   2017's photoevaporation-valley physics places b firmly in the
   "core-only" regime: any initial H/He envelope of a 5 M⊕ core at
   0.05 AU around a G-dwarf is lost on a timescale ≲ 50 Myr, far
   shorter than the 6 Gyr system age. Secondary atmospheric retention
   depends on the balance between outgassing and XUV-driven loss; for
   b's parameters, the equilibrium is marginal.

The cfg adopts the **partial-melt substellar magma ocean** scenario:
the substellar hemisphere within ~30° of the substellar point hosts a
shallow magma-ocean structure where surface temperatures exceed the
silicate solidus (T ≈ 1500 K for tholeiitic basalts, lower for
volatile-rich melts). This is a tie-break choice over the fully
solidified "Mercury-with-stronger-insolation" interpretation;
interesting-first picks the magma ocean because it gives b a visually
distinctive feature absent in the rest of the system.

**Color choice.** Under the solar-twin illumination (Teff 5552 K,
near-Sol SED), surface tints are perceived essentially as they would
be from Earth — no significant M-dwarf red-shift correction needed.
The primary surface tint `#3a2a22` is a dark partial-melt basaltic
crust tone, between fresh ultramafic black (~`#1a1612`) and weathered
Mercury regolith (~`#5a4a3a`). The accent `#c84a18` encodes the
substellar magma-ocean glow as a visible red-orange patch — the Wien
peak of 1450 K thermal emission is at λ ≈ 2 μm (near-IR) but the
visible tail is bright enough to be perceptible against the cooler
mid-latitude crust.

**Morphology under tidal lock.** The substellar magma pond is a
permanent feature, fixed in the surface frame. Convective heat flow
within the magma pond, sustained by stellar insolation rather than
internal heating, drives partial silicate vapor outgassing into the
exosphere. Mid-latitudes are crusted basaltic plains; the nightside
is cold, dark, and volatile-stripped over the system's 6 Gyr — Mercury-
analog impact-cratered regolith covers the antistellar hemisphere
with no detectable volatile cold-trap because there is no atmospheric
transport from the dayside to deliver fresh volatiles.

## Atmosphere synthesis

The atmospheric inference for b is entirely theoretical. There is no
JWST transit or eclipse measurement, and the planet is too faint in
contrast for current-generation direct imaging. The cfg adopts a
**vestigial silicate-vapor exosphere** with no visible Rayleigh
atmosphere — the airless interpretation modified by ongoing magma-pond
outgassing.

**Pressure choice.** Surface pressure 10⁻⁷ Pa is the equivalent
column-density expression of a silicate-vapor exosphere produced by
substellar magma sublimation (Schaefer & Fegley 2009 scaling for hot
rocky planets). This is well below any Rayleigh-scattering threshold
and gives no visible limb haze. The full hydrostatic atmosphere is
absent — the column density of ~10¹² atoms/cm² corresponds to a few
Mercury exospheres in mass, biased to the substellar hemisphere where
the magma pond actively sublimes silicates.

**Composition.** Schaefer & Fegley 2009 give Na, K, SiO, O₂, and
Fe-vapor as the dominant outgassing species over a partial-melt
silicate magma ocean at 1400–1500 K. Na and K dominate by vapor
pressure at these temperatures; SiO and O₂ are secondary; Fe-vapor
condenses out before reaching exospheric altitudes. The cfg encodes
"Na, K, SiO, O₂ silicate-vapor" as the composition string — this is
the canonical Léger 2009 / Schaefer & Fegley 2009 composition for the
lava-world regime.

The XUV-driven loss budget runs at ~10⁹ g/s for b's parameters (Owen
& Wu 2017 scaling; ~10⁻⁵ M⊕/Gyr). Continuous outgassing from the
magma pond keeps the exosphere replenished at steady-state column
density. There is no significant secondary atmospheric buildup
because the loss rate exceeds the outgassing rate for any plausible
mantle composition; the planet is **escaping** rather than accumulating.

**Sky appearance from the surface.** No atmosphere means no Rayleigh
scattering — the sky is black at every elevation. 61 Vir dominates
the dayside sky at angular diameter 1.02° (about 2× the Sun's apparent
size from Earth), and its solar-yellow disk is unblurred and
unscattered. Surface brightness at the substellar point is ~326×
Earth-noon-equivalent. The star's spectrum is essentially Sol-like —
a player standing on b's dayside would see a yellow disk significantly
larger and brighter than Sol-from-Earth, casting sharp shadows over
the partial-melt landscape.

**Nightside.** No atmospheric transport means the nightside is
genuinely dark, lit only by reflected light from sister planets at
conjunction (c is most prominent, with d further out) and by distant
starlight. Nightside surface temperatures of ~200 K and the absence
of any sublimable volatile means the antistellar hemisphere is a
darker analog of Mercury's nightside.

## Rotation & spin synthesis

The 4.215-day orbital period at 0.050 AU around a 0.94 M☉ host gives a
tidal-locking timescale of ~10⁵–10⁶ years (Vinson 2017 scaling for
5 M⊕ rocky planets at G-dwarf hosts), four to five orders of magnitude
shorter than the 6 Gyr system age. The 1:1 spin-orbit resonance is
fully established. Obliquity has damped to zero over the same
timescale.

**Higher-order resonances.** At eccentricity 0.12 (Vogt 2010 fit), the
Makarov 2012 / Vinson 2017 stability analysis allows for a 3:2
resonance trap as an alternative to 1:1, by analogy with Mercury's
3:2 lock at e = 0.205. The boundary is e ≈ 0.1–0.15 for a rocky
planet of b's mass at this orbital period; b sits **on** the boundary.
The cfg adopts 1:1 as the canonical choice (the most likely outcome
of slow eccentricity damping in a planetary chain) and notes the 3:2
alternative as a cfg variant in Open items.

**KSP implementation note.** Rotation period = orbital period =
4.215 days (364 176 s). Kopernicus `rotationPeriod` should match the
orbital `period` in seconds.

**No seasons.** Obliquity damped to zero; eccentricity-driven
insolation variation (e=0.12) gives a peri-to-apo S range of
S = (1 ± e)⁻² × 326 = 263 → 416 S⊕ over the orbit, but with a fixed
substellar point the variation manifests as a modulation of the magma
pond's depth and outgassing rate rather than seasonal weather. The
cfg's static magma-pond rendering is a time-averaged scenario;
variant rendering with periodic outgassing bursts could be added at
the Phase 3.5 visual-detail layer.

**Tidal heating.** Bolmont 2020 scaling for e=0.12 at a 4.2-day
period gives a tidal heating contribution of 0.1–1 W/m² for an
Earth-analog interior rheology. This is modest relative to the
326 S⊕ insolation flux (~4.4 × 10⁵ W/m² absorbed at substellar) but
non-trivial relative to Earth's ~0.1 W/m² internal heat flow. The
substellar magma pond is therefore **insolation-driven, not
tidal-driven** — unlike Io's tidal-heat-dominated volcanism.

## Visual styling

Combining the surface and atmosphere decisions for the orbital and
surface renderers:

- **Global appearance (orbit view).** A dark-bodied super-Earth with a
  glowing red-orange spot at the substellar point and dark
  near-uniform mid-latitude basaltic plains, fading to a black
  nightside. The substellar magma-ocean glow is the most visually
  distinctive feature in the entire 61 Vir inner system.
- **Substellar magma ocean.** A ~30° radius disk centred on the
  substellar point, surface tint `#c84a18` (lava red-orange), with
  thermal-emission glow at λ ≳ 1 μm contributing additional
  brightness in the IR cfg. The pond is permanent (insolation-driven)
  but its depth modulates slightly over the eccentric orbit.
- **Mid-latitude basaltic crust.** Tint `#3a2a22` (dark brown-black
  partial-melt basalt). Sparse impact craters from 6 Gyr of
  bombardment, partially resurfaced by past magma-pond expansion
  during high-e excursions. Smooth lava plains predominate.
- **Nightside.** Cold (~200 K) and dark; surface tint same as
  mid-latitudes but with no illumination. Visible only by sister-planet
  reflected light. Volatile-stripped Mercury-analog regolith.
- **Terminator band.** Sharp due to the absence of atmospheric
  scattering. Topographic features cast long shadows in the grazing
  solar-yellow light.
- **Atmosphere haze.** None visible; the silicate-vapor exosphere is
  ~10⁻⁷ Pa, well below any Rayleigh threshold. The limb is a clean
  edge from disk to space.
- **Star in sky.** 61 Vir subtends 1.02° at b — about 2× the Sun's
  angular size from Earth. Color essentially solar-yellow (Teff
  5552 K → `#fff2dc` cfg-encoded tint). At 326× Earth-noon brightness
  the surface is illuminated like a hot-Mercury dayside.
- **Sister planets in sky.** c (next out at 0.22 AU) at angular size
  ~0.05° from b's perspective at inferior conjunction (every ~5 days
  by synodic period); d (at 0.48 AU) much smaller and not always
  visible.
- **Optional magma-pond animation.** A subtle thermal pulsation of
  the magma-pond accent tint (modulating from `#c84a18` to a brighter
  `#e85a28` over the eccentricity cycle) would faithfully render the
  insolation-driven heat-flow modulation. Low-priority visual easter
  egg.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Vogt S. S. et al. 2010** — *A Super-Earth and Two Neptunes
  Orbiting the Nearby Sun-Like Star 61 Virginis*, ApJ 708, 1366
  (`2010ApJ...708.1366V`). The discovery paper. Reports b's orbit
  (P=4.215 d, a=0.0502 AU, e=0.12, ω=105°) and minimum mass
  (Msini = 5.1 ± 0.5 M⊕). HIRES + AAT joint RV solution. All
  Decisions table orbital + mass values anchor here.
- **Léger A. et al. 2009** — *Transiting exoplanets from the CoRoT
  space mission VIII. CoRoT-7b: the first super-Earth with measured
  radius*, A&A 506, 287 (`2009A&A...506..287L`, arXiv:0908.0241).
  The lava-world template — establishes the magma-ocean dayside
  scenario for hot rocky super-Earths. b is a slightly cooler analog.
  Drives surface morphology + magma-pond visual decisions.
- **Schaefer L. & Fegley B. 2009** — *Chemistry of silicate
  atmospheres of evaporating super-Earths*, ApJ 703, L113
  (`2009ApJ...703L.113S`, arXiv:0905.4045). Outgassing chemistry of
  hot-rocky surfaces. Drives the `atmosphere_composition` choice (Na,
  K, SiO, O₂ silicate-vapor dominant at 1400–1500 K substellar).
- **Zeng L. et al. 2016** — *Mass-radius relation for rocky planets*,
  ApJ 819, 127 (`2016ApJ...819..127Z`, arXiv:1512.08827). Mass-radius
  scaling for Earth-composition rocky planets; gives R ≈ 1.65 R⊕ for
  5.1 M⊕. Drives the `radius_rearth` tie-break.
- **Owen J. E. & Wu Y. 2017** — *The evaporation valley in the
  Kepler planets*, ApJ 847, 29 (`2017ApJ...847...29O`,
  arXiv:1705.10810). Photoevaporation-valley physics. Places b firmly
  in the "core-only" regime — any initial H/He envelope is lost on
  ≲ 50 Myr. Drives the `atmosphere_present = false` choice.
- **Vinson A. M. & Hansen B. M. S. 2017** — *On the spin states of
  habitable zone exoplanets around M dwarfs: the effect of a planetary
  companion*, MNRAS 472, 3217 (`2017MNRAS.472.3217V`, arXiv:1708.00006).
  Tidal-locking timescales for rocky planets; b's parameters give
  ~10⁵–10⁶ yr. Anchors the `tidally_locked = true` choice.
- **Bolmont E. et al. 2020** — *Tidal dissipation and obliquity
  evolution of TRAPPIST-1 planets* (`2020A&A...644A.165B`, arXiv:
  2002.02015). Tidal heating scaling for rocky exoplanets; provides
  the 0.1–1 W/m² estimate at e=0.12, P=4.2 d.

### Read (context / methodology, not decision-driving)

- **Mamajek E. E. & Hillenbrand L. A. 2008** — *Improved Age
  Estimation for Solar-Type Dwarfs Using Activity-Rotation
  Diagnostics*, ApJ 687, 1264 (`2008ApJ...687.1264M`, arXiv:0807.1686).
  Inherited from the host-star synthesis. Gives 61 Vir age 6.1 ±
  1.7 Gyr; sets the system-evolution timescale for atmospheric loss.
- **Pavlenko Y. V. et al. 2012** — *Effective temperatures, gravities,
  metallicities, and ages of 18 solar twin candidates*
  (`2012MNRAS.422..542P`, arXiv:1112.0590). Inherited from host-star
  synthesis. Confirms 61 Vir solar-twin abundance pattern.
- **Wyatt M. C. et al. 2012** — *Herschel imaging of 61 Vir*, MNRAS
  424, 1206 (`2012MNRAS.424.1206W`, arXiv:1204.6063). Inherited from
  host-star synthesis. Cited briefly because the cold debris belt at
  ~30 AU does not interact dynamically with the inner planets at
  b's separation.
- **Lopez E. D. & Fortney J. J. 2014** — *Understanding the
  mass-radius relation for sub-Neptunes*, ApJ 792, 1
  (`2014ApJ...792....1L`, arXiv:1311.0329). Sub-Neptune envelope
  mass-radius scaling; informs the bounds on b's potential
  unphotoevaporated H/He envelope (excluded as discussed).
- **Howe A. R. et al. 2014** — *Mass-radius relations and core-envelope
  decompositions of super-Earths and sub-Neptunes*, ApJ 787, 173
  (`2014ApJ...787..173H`, arXiv:1311.0329). Used briefly in the
  context of envelope-vs-rocky decision; b is rocky.

### Read (instrument-only, not visual-informative)

- **Marcy G. W. et al. 2014** — Kepler super-Earth statistics; b is
  not in the Kepler sample but used as a calibration anchor in
  follow-up studies.

### Not read — no arXiv preprint or low-priority (~10 papers)

The b-specific arXiv record is small (the planet was discovered in
2010 with no follow-up transit or atmospheric characterization). The
not-read set is predominantly:

- **Dynamical-stability follow-ups** — Vogt 2010 + extensions; b is
  stable inside the Vogt 2010 dynamical solution, no further refinement
  needed for cfg purposes.
- **Transit search non-detections** — confirmed b does not transit;
  no information beyond the inclination posterior already used.
- **Atmospheric escape rate calculations** — uses generic XUV scaling
  rather than 61 Vir specific stellar wind models.

## Open items for follow-up

- **True mass and radius.** b's mass is Msini-only and the radius is
  a mass–radius scaling estimate. A future direct-imaging campaign
  (HabEx / LUVOIR era) or precise astrometric inclination from Gaia
  DR5+ would convert Msini to true mass and constrain radius from a
  thermal-emission detection. Until then, all radius-dependent fields
  carry Confidence=medium.
- **Cfg variant: runaway-Venus retained atmosphere.** Even with the
  photoevaporation valley argument, a small fraction of secondary
  atmospheres (steam + CO₂ + N₂, ~1–10 bar) is consistent with the
  airless cfg's parameters. A cfg variant with a thick steam atmosphere
  would render b as a cloud-covered featureless white-yellow disk
  (Venus-analog), distinct from the magma-pond visual. Preserve as a
  cfg switch for users who prefer the "retained atmosphere" reading.
- **Cfg variant: 3:2 spin-orbit resonance.** At e=0.12, b sits on the
  1:1/3:2 boundary. A 3:2 cfg variant (Mercury-analog) would
  render with a slowly drifting substellar magma pond rather than a
  fixed one — visually distinctive but harder to animate at KSP
  scale. Document as Phase 3.5 alternative.
- **Surface mineralogy from future JWST or HabEx spectroscopy.** No
  current instrument can resolve b's surface composition. If a
  reflected-light direct-imaging campaign yields a thermal-emission
  spectrum, surface-tint hex codes could be refined from the
  inferred basalt composition (basalt vs. ultramafic vs. silica-rich).
- **Magma-pond outgassing rate.** Schaefer & Fegley 2009's outgassing
  scaling is well-established but planet-specific exospheric
  modeling is missing. A future Vidotto-style 3D MHD wind +
  outgassing model could refine the exosphere column density.
- **Sister-planet conjunction visibility.** The eccentric d (e=0.35)
  and modestly eccentric c (e=0.14) produce time-variable conjunction
  geometries. Sub-Neptune c at ~5 R⊕ would reach mv ≈ −4 at b's
  inferior-conjunction distance — bright enough to be a distinctive
  sky feature. Compute exact visibility for Phase 3.5 cfg.

## Related

- [61-vir](61-vir.md) — host star Phase 3 synthesis
- [61-vir-c](61-vir-c.md) — next-outward sibling sub-Neptune at 0.22 AU
- [61-vir-d](61-vir-d.md) — outermost sibling sub-Neptune at 0.48 AU
- [trappist-1-b](trappist-1-b.md) — adjacent hot-rocky analog around an M-dwarf (different host illumination but same surface category)
- [proxima-cen-d](proxima-cen-d.md) — sub-Earth USP RV-only analog (smaller, around M-dwarf)
- [methodology](../reference/methodology.md) — Decisions schema
