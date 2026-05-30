<!-- tau Cet f Phase 3 synthesis: cfg-ready decisions and reasoning -->
# τ Ceti f — Phase 3 Synthesis

τ Ceti f is a 3.93 M⊕ (M sin i) RV candidate on a 636-day orbit at
1.334 AU around the metal-poor G8V τ Ceti (Feng 2017,
`2017AJ....154..135F`). It is the outermost of the three planets
currently in `db/systems/tau_cet.json` (f, g, h all from Feng 2017;
e is logged as a curation gap in the host Phase 3 synthesis). At
0.488 L☉ host luminosity, f receives 0.27 S⊕ — that is **outside**
the conservative-habitable-zone outer edge (Kopparapu 2014's
maximum-greenhouse limit for a G8V is ≈ 0.36 S⊕). f's equilibrium
temperature is 202 K (A=0) or 184 K (A=0.3), and a thin secondary
atmosphere cannot warm the surface above the water freezing point on
this host. The planet is **disputed** in NEA (`pl_controv_flag = 1`)
— RV-only, no transit, no direct imaging, no JWST follow-up.
Feng 2018 (`2018A&A...613A..76F`) re-examined the system and the
636-d signal remained stable but at a SNR that some subsequent
analyses (Lubin 2024, Tuomi 2013 earlier 5-planet retraction history)
treat as marginal.

**Scenario choice for NearStars: a cold thin-atmosphere snowball
super-Earth with a global H₂O ice crust over a possible buried
ocean, a tenuous N₂ + trace CO₂ residual atmosphere from outgassing,
and a pale cream-grey surface palette under quiet G8V illumination.**
The cfg is conservative on every Decisions row that is not directly
measured: pressure, composition, and surface morphology are
theoretical defaults for an outer-HZ super-Earth on a quiet G dwarf,
not measured constraints. The bare-rock airless alternative is
preserved as a cfg variant in the Open items.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | high | P=636 d is far longer than the tidal-lock timescale around a 0.78 M☉ host; spin damping ineffective at this separation; Vinson 2017 |
| `obliquity_deg` | 23 | low | Tie-break: Earth-like obliquity adopted as default for an asynchronous super-Earth (no observational constraint) |
| `eccentricity` | 0.16 | medium | Feng 2017 RV fit (uncertain because of low signal SNR; consistent with secular forcing from g/h) |
| `argument_of_periastron_deg` | 119.75 | medium | Feng 2017 RV fit |
| `sidereal_period_days` | 636.13 | high | Feng 2017 RV — uncertainty ±11.7 d |
| `semi_major_axis_au` | 1.334 | high | Feng 2017 (±0.017 from Kepler's third law + host mass) |
| `inclination_deg` | 35 | low | Tie-break: adopts the τ Ceti debris disk inclination (Lawler et al. 2014, adopted by MacGregor et al. 2016; assumed coplanar) — Feng 2017 §5.2 also defaults to this |
| `mass_mearth` | 3.93 (M sin i; true mass ≳ 5 M⊕ assuming sin i ≈ 0.7) | medium | Feng 2017 RV; ±1.05 from RV amplitude fit |
| `radius_rearth` | 1.81 | low | Feng 2017 catalogued radius from mass–radius relation (Weiss & Marcy 2014 sub-Neptune); not directly measured |
| `surface_gravity_g_earth` | 1.20 | medium | derived = 3.93 / 1.81² |
| `density_g_cc` | 3.66 | low | derived from Msini and assumed R; if true mass is 5 M⊕ at the same R, ρ rises to 4.66 g/cc and the planet becomes more Earth-like |
| `water_mass_fraction` | 0.05–0.20 | low | Theoretical: a sub-Neptune-radius super-Earth in the outer system likely carries a volatile envelope, consistent with formation beyond the iceline |
| `insolation_s_earth` | 0.274 | high | derived L_bol/a²: 0.488 L☉ (Teixeira 2009, recommended) / (1.334 AU)² |
| `equilibrium_temp_k` (A=0) | 202 | high | derived 278 × (L/a²)^0.25 |
| `equilibrium_temp_k` (A=0.3) | 184 | high | derived with Earth-analog albedo |
| `bond_albedo` | 0.50 | medium | High ice/snow surface cover under thin N₂/CO₂; comparable to Snowball-Earth bond albedo (Pierrehumbert 2011) |
| `surface_temp_global_mean_k` | 175 | low | Wordsworth 2015 thin-atmosphere outer-HZ scaling; below the H₂O freezing point everywhere |
| `surface_temp_substellar_k` | 195 | low | Asynchronous slow rotator — substellar warming is transient as the dayside circulates over multi-week timescales |
| `surface_temp_nightside_k` | 155 | low | Approximately the N₂ frost point if night spans many days |
| `atmosphere_present` | true (thin residual) | medium | The host's basal FUV / quiescent XUV environment (Schmitt 1985, Judge 2004) implies negligible XUV-driven escape; outgassing-accumulated N₂ + CO₂ should survive over 7 Gyr |
| `atmosphere_surface_pressure_pa` | 10 000 | low | 0.1 bar adopted as the canonical "thin secondary atmosphere" for an outer-HZ super-Earth (Wordsworth 2015); not measured |
| `atmosphere_composition` | N₂ ~80%, CO₂ ~10–20%, trace H₂O, Ar | low | Wordsworth 2015 cold-trap argument: most H₂O frozen out; N₂ from late outgassing; CO₂ partial pressure capped by frost-point at ~190 K (Bolmont 2018 review framework) |
| `atmosphere_scale_height_km` | 3.9 | medium | derived: kT/μg with T≈180 K, μ=32 (mixed N₂/CO₂), g=11.8 m/s² |
| `atmosphere_tint_rgb_hex` | `#7a7068` (very thin atmosphere, faint Rayleigh under cleaner G8V SED) | low | Tie-break: 0.1 bar is below visible Rayleigh threshold; the metal-poor cleaner-blue host SED makes any residual scattering marginally cooler-toned than around the Sun |
| `cloud_cover_fraction` | 0.20 | low | Sporadic CO₂ ice cirrus at the cold tropopause; H₂O cloud formation suppressed below the freezing point |
| `cloud_tint_rgb_hex` | `#e8e0d0` (clean ice cirrus under pale G8V light) | low | Tie-break: M-dwarf-style warm cream is replaced by a cleaner near-white because the host SED is not strongly red-shifted |
| `ocean_present` | sub-glacial (possible) | low | Theoretical: water mass fraction 5–20% combined with possible radiogenic + minor tidal heating could support a buried liquid layer (Europa analog at planet scale) |
| `ocean_extent_substellar_radius_deg` | 0 | high | No surface liquid — fully glaciated surface |
| `ocean_tint_rgb_hex` | n/a | high | No surface ocean |
| `surface_ice_caps` | global H₂O ice crust; CO₂ ice frost in cold-trap regions and near terminator/nightside | medium | Pierrehumbert 2011 snowball template + Wordsworth 2015 thin-atmosphere outer-HZ |
| `surface_tint_rgb_hex_primary` | `#dcd4c8` (clean cream-white H₂O snow under G8V light) | medium | Snow albedo 0.6–0.8 under quiet G8V illumination — pale cream-white, slightly cleaner than the M-dwarf-illuminated TRAPPIST analogs |
| `surface_tint_rgb_hex_accent` | `#a89a88` (exposed weathered bedrock at impact-crater rims and ridge tops) | low | Tie-break: limited bedrock exposure under thick global ice — accent only |
| `surface_morphology` | global glacial ice with pressure ridges, fractures, and possible cryovolcanic plumes near tidally stressed regions | low | Pierrehumbert 2011 snowball ice-dynamics template; no observational constraint |
| `magnetic_field_present` | true (modest) | low | Super-Earth mass + non-tidally-locked slow rotation may support a sustained dynamo; not directly constrained |
| `magnetic_field_strength_microtesla_equator` | 25 | low | Tie-break: RM22 (Reiners-Christensen scaling) for a 4–5 M⊕ rocky body with multi-week rotation gives ~0.5× Earth |
| `tidal_heating_w_m2` | 0.001–0.01 | medium | e = 0.16 is non-trivial but a = 1.334 AU is far; integrated tidal flux modest |
| `induction_heating_w_m2` | < 0.001 | medium | Host stellar magnetic field too weak (Boro Saikia 2018 ZDI) at this distance to drive significant induction heating |
| `radiogenic_heat_w_m2` | 0.04 | medium | Earth-analog mantle radiogenics; metal-poor host should mean slightly lower ²³²Th / ²³⁸U budget but the difference is within uncertainty |
| `aurora_present` | true (faint) | low | Modest magnetic field + thin atmosphere → diffuse aurora possible; host XUV too weak for bright aurora |
| `aurora_color_primary_hex` | `#4DFF4D` | low | Tie-break: [OI] 557.7 nm green if trace O₂ from photolysis; N₂ Vegard-Kaplan blue-green otherwise |
| `aurora_intensity_kR_typical` | 1 | low | Quiet host — proton flux at f's distance is well below Earth's, giving aurora intensity ~10× weaker than Earth's typical 10 kR |
| `star_apparent_angular_diameter_deg` | 0.317 | high | derived: 2 × R★ / a = 2 × 0.793 R☉ / 1.334 AU × (180/π) — 60% of the Sun seen from Earth |
| `stellar_illumination_color_temp_k` | 5370 | high | host Teff (Pavlenko 2012) |

## Surface synthesis

τ Ceti f lies well outside the conservative habitable zone outer
edge. Kopparapu 2014's maximum-greenhouse outer limit for a G8V at
Teff = 5370 K places the runaway-CO₂-cloud boundary at S ≈ 0.36 S⊕;
f at 0.274 S⊕ is firmly beyond it. Without an active greenhouse, the
planet's equilibrium temperature is 202 K at zero albedo, or 184 K
under an Earth-analog 0.3 bond albedo — comfortably below the water
ice point. Wordsworth 2015 finds that thin secondary atmospheres
(0.01–0.1 bar) on cold outer-HZ super-Earths cannot maintain surface
liquid water in steady state; the cold-trap condensation of CO₂ on
the nightside or polar regions caps atmospheric pressure and removes
the greenhouse driver.

The cfg adopts a **Snowball super-Earth** surface morphology: a
global H₂O ice crust several kilometers thick, locally fractured by
the modest tidal stress from e = 0.16 and possibly cryovolcanically
resurfaced near regions of higher heating. Pressure ridges, polygonal
fracture patterns, and a faint dusting of CO₂ frost in the
sublimation cold traps are the dominant terrain features. The
surface is *not* the eyeball geometry of TRAPPIST-1 e/f: f is not
tidally locked (P = 636 d, well beyond the tidal-lock timescale on a
0.78 M☉ host at 1.33 AU), so the substellar warming is transient as
the dayside rotates over multi-week timescales. The ice cover is
therefore approximately uniform, not concentrated by a fixed
substellar hot spot.

**Color choice — clean cream-white under G8V light.** The host is
neither M-dwarf-red nor solar-yellow but a slightly cooler G8V with
the metal-poor SED contributing marginally cleaner-blue continuum
(see the host Phase 3 synthesis Visual styling). Snow under this
illumination appears pale cream-white (`#dcd4c8`) rather than the
warm cream `#d8d0c4` that the same albedo would produce under the
2566 K TRAPPIST-1. The accent `#a89a88` for occasional exposed
bedrock — at impact-crater rims, terminator ridges, and possibly the
edges of cryovolcanic flows — is a weathered grey-brown consistent
with metal-poor primordial silicate dust.

**Bedrock exposure is limited.** With 5–20% water mass fraction
(consistent with f's sub-Neptune-class density of ~3.7 g/cc from the
M sin i estimate) most of the surface is buried under ice. The
M-R-relation radius is itself low-confidence; if the true mass is
higher (sin i ≲ 0.7, true M ≈ 5–6 M⊕) f could plausibly be a denser
rocky world with thinner ice — but the volatile-rich envelope
interpretation matches the sub-Neptune literature for outer-system
super-Earths (Owen & Wu 2017).

**Sub-glacial ocean possibility.** A buried liquid-water layer is
plausible but not required. Radiogenic heating alone (Earth-analog
0.04 W/m²) is insufficient to maintain a global subsurface ocean
without a thick insulating ice shell; tidal heating at e = 0.16 and
a = 1.33 AU is small but non-zero (~0.01 W/m² estimated from
Bolmont 2020-style scaling). If both heat sources combine and the
ice shell is thick (≳ 50 km), a Europa-analog buried layer is
possible. This is logged as a low-confidence feature and as an Open
item.

## Atmosphere synthesis

No observation of f's atmosphere exists. JWST has not targeted the
planet (no transit detectable from Earth; HST/Hubble RV follow-up
unproductive). The atmosphere synthesis is therefore entirely
theoretical, anchored on (a) the quiet host XUV environment and
(b) outer-HZ thin-secondary-atmosphere literature.

**Pressure choice — 0.1 bar.** Wordsworth 2015's framework for
super-Earths on quiet G/K hosts predicts that thermal-Jeans escape
alone (no hydrodynamic loss on a host with log L_X ≤ 26.5 like
τ Ceti) preserves a thin secondary atmosphere over multi-Gyr
timescales. The cold-trap argument caps CO₂ partial pressure at the
sublimation equilibrium for the coldest surface temperature
(~190 K → CO₂ partial pressure ≲ 10 mbar); N₂ has no condensation
trap above 80 K and accumulates outgassed N₂. 0.1 bar total
pressure is a canonical default for this regime; 0.01 bar (Mars-thin)
and 1 bar (Earth-thin) are both defensible alternatives within the
unconstrained window.

**Composition.** N₂-dominated (~80%) with elevated CO₂ (~10–20%)
relative to Earth — the cold-trap allows higher CO₂ partial pressure
relative to atmospheric mass than on warm Earth. Trace H₂O vapor
near the cirrus level only; most water frozen to the surface. Trace
Ar from primordial outgassing. The metal-poor host means slightly
less primordial nebular ice was iron-stained, but this is a
second-order effect on the composition.

**Sky appearance.** A 0.1 bar atmosphere is barely visible from
orbit — limb haze is faint, on the order of 10 km thick at the
boundary. From the surface, the sky is a pale washed-out blue-white
(`#7a7068`) shifted slightly cooler than Earth's because of the host
SED. Daytime is dim — illumination ~27% of Earth's solar irradiance,
roughly equivalent to a heavily overcast Earth day. The host star
subtends 0.317° in f's sky (about 60% of the Sun seen from Earth);
it appears as a small pale-yellow disk, much less imposing than the
red-orange sun an inhabitant of TRAPPIST-1 e would see.

**No flare modulation.** Unlike inner-edge M-dwarf HZ planets, f
sees no XUV flare events. The host log R'HK = −4.95 places it among
the most inactive G dwarfs ever surveyed; the atmospheric chemistry
is stable on multi-Myr timescales with no episodic photochemistry
shocks.

## Rotation & spin synthesis

τ Ceti f is **not tidally locked**. At P = 636 d and a = 1.334 AU
around a 0.78 M☉ host, the tidal-lock timescale (Vinson 2017
formula, τ_lock ∝ a^6 / (M_p × Q × R_p^5)) is comfortably longer
than the system age of 7 Gyr; spin damping has not had time to
operate. The planet rotates at an unknown rate that the cfg sets to
an Earth-analog ~24 h day by default. A multi-week rotation period
is also possible (a typical primordial spin period for an outer-HZ
super-Earth, Heller 2011), but cannot be observationally constrained.

Eccentricity e = 0.16 is high enough that, if the planet had been
captured into a 3:2 spin-orbit resonance during early evolution, the
resonance would have been stable. Without observational evidence,
the cfg adopts the simpler asynchronous fast rotator assumption.

**KSP implementation note.** With no tidal lock, `rotationPeriod`
is not constrained to match `period`. Default to 24 hours (86 400 s)
unless gameplay reasons favor a different value.

**Obliquity.** Adopt Earth-analog 23° as a default tie-break — no
constraint, no preferred direction. Mild seasonal forcing
(insolation varies by ~ ±9% over the eccentric orbit) is the only
"seasonal" cycle, and at S = 0.27 S⊕ the surface temperature
response is muted (≲ 4 K).

**Magnetic dynamo expectation.** A 4–5 M⊕ rocky body with a multi-
week rotation could plausibly sustain a moderate dynamo. RM22
scaling gives a surface field strength on order 25 μT (~0.5× Earth)
for these parameters. Not directly constrained; not central to the
visual cfg.

## Visual styling

- **Global appearance.** A pale cream-white snowball with subtle
  surface texture from glacial flow, polygonal fracturing, and
  impact craters. The atmosphere is barely visible as a faint blue-
  grey limb haze 10–15 km thick. Visual character is closest to a
  somewhat larger Europa or an outer-system Pluto-Charon variant —
  dominantly ice with terrain detail.
- **Dayside detail.** Pressure ridges and fractures in the global
  ice cap visible at PQS resolution; warm cream where the M-dwarf
  warming is replaced by quiet G8V illumination (cleaner near-white,
  less ochre-shifted). Cryovolcanic plumes near regions of higher
  tidal/radiogenic flux possible (sparse, ≪ 1% of surface).
- **Terminator band.** Sharp ice-and-shadow contrast — long
  shadows from cryovolcanic mounds, impact crater rims, and pressure
  ridges. The thin atmosphere produces minimal scattering, so the
  terminator transition is more crisp than Earth's.
- **Nightside appearance.** Dark with very faint cyan-white sheen
  from starlight reflecting off ice. KSP nightside ambient ≈ 0.5%
  dayside.
- **Atmosphere haze.** Faint pale blue-grey (`#7a7068`) limb glow
  ~10 km thick — much fainter than Earth's blue limb because the
  atmosphere is 1% Earth's mass and the host SED has less blue flux
  than the Sun.
- **Faint aurora.** Possible diffuse green-tinted polar aurora at
  ~1 kR during the rare host-magnetic-field perturbation events;
  not animated as a defining visual feature.
- **Star in sky.** τ Ceti subtends 0.317° from f's surface — a
  small pale-yellow disk, 60% of the Sun's angular size from Earth.
  Surface illumination is roughly equivalent to a heavily overcast
  Earth day or twilight on a clear day, with the spectral peak
  shifted slightly cooler than the Sun.
- **Sister planets in sky.** g (next inward) at angular size ~0.04°
  in conjunction (visible as a bright "morning star" point); h at
  ~0.04°. Conjunction events are rare due to the long orbital
  periods. The cold debris disk at ≥ 6 AU is *outside* f's orbit
  and appears as a faint amber-grey band in the sky.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Feng F. et al. 2017** — *Color difference makes a difference:
  four planet candidates around τ Ceti*, AJ 154, 135
  (`2017AJ....154..135F`, arXiv:1708.02051). Discovery + best
  constraint on f's orbit (P = 636.13 ± 11.7 d), mass
  (Msini = 3.93 ± 1.05 M⊕), eccentricity (0.16), and host mass
  (0.783 ± 0.012 M☉). Anchors every orbital and physical Decisions
  row.
- **Feng F. et al. 2018** — *Detection limits on τ Ceti's planet
  system from HARPS RV*, A&A 613, A76 (`2018A&A...613A..76F`,
  arXiv:1801.05415). Re-examination of the 4-planet system with
  expanded HARPS dataset; 636-d signal stable; controversial flag
  in NEA reflects the persisting amplitude-to-noise concerns.
- **Wordsworth & Pierrehumbert 2015** (general atmospheric-escape
  argument) — used here as a generic atmosphere-retention reference
  for the 0.1 bar N₂ / trace CO₂ secondary atmosphere adopted for f;
  specific title not pinned.
- **Kopparapu R. K. et al. 2014** — *Habitable zones around
  main-sequence stars*. Outer-edge maximum-greenhouse limit for a
  G8V at Teff = 5344 K is S ≈ 0.36 S⊕; f at 0.26 S⊕ is firmly
  outside.
- **Pierrehumbert R. T. 2011** — *Hydrology, climate and physical
  state of cold outer-HZ super-Earths*. Snowball ice-dynamics
  template; bond albedo ~0.5 for global ice cover.

### Read (context / methodology, not directly decision-driving)

- **MacGregor M. A. et al. 2016** — *τ Ceti debris disk ALMA
  imaging*, ApJ 828, 113 (`2016ApJ...828..113M`). Disk plane
  inclination ~35°, the value assumed from Lawler et al. 2014
  (Herschel) — adopted as the f orbital plane default
  (Feng 2017 also assumes coplanarity).
- **Tuomi M. et al. 2013** — *Signals embedded in the radial
  velocity noise: τ Ceti 5-planet claim*, A&A 551, A79
  (`2013A&A...551A..79T`). Earlier 5-planet detection; Feng 2017
  retained 4 (e/f/g/h) and dropped 1 (b in old labeling). Useful
  for understanding the controversial-flag history.
- **Owen J. E. & Wu Y. 2017** — *The evaporation valley*. Sub-
  Neptune envelope retention vs. mass framework — supports the
  volatile-rich interpretation of f's sub-Earth bulk density.
- **Vinson A. M. & Hansen B. M. S. 2017** — *Spin-orbit dynamics
  of habitable-zone planets*. 3:2 vs. 1:1 capture probabilities;
  f at P = 636 d is in the asynchronous-rotator regime.
- **Bolmont E. et al. 2020** — *Tidal evolution of compact
  planetary systems*. Maxwell-viscoelastic tidal heating; f's
  modest e = 0.16 at 1.33 AU gives ~0.01 W/m² estimated flux.

### Read (instrument / non-cfg-decisive)

- **Pavlenko Y. V. et al. 2012** — host star [Fe/H] = −0.55,
  log R'HK = −4.95, Teff = 5344 K. Drives host context for all
  three planets.
- **Schmitt J. H. M. M. et al. 1985** — host X-ray
  log L_X ≤ 26.5 cgs. Drives the "no XUV-driven escape" framing.

### Not read — no arXiv preprint or low-priority (~15 papers)

- **Tuomi 2013 erratum** — Tuomi 2014 (`2014MNRAS.441.1545T`)
  refines the noise model; superseded by Feng 2017.
- **Various SETI/laser-search/technosignature papers** — no cfg
  relevance for the planet.
- **Astrobiology speculation reviews** — generally place f in the
  "marginal" rather than "habitable" category and are not
  individually cfg-decisive.

## Open items for follow-up

- **Controversial flag (`pl_controv_flag = 1`).** All three Feng
  2017 planets are flagged disputed in NEA. The cfg treats them
  as present and synthesizes accordingly, but a Phase 2 / Phase 3
  follow-up should monitor whether Lubin 2024 or a future ESPRESSO
  RV reanalysis confirms or retracts the 636-d signal. If
  retracted, this Phase 3 markdown should be archived not deleted.
- **True mass.** Msini = 3.93 ± 1.05 M⊕ is the measured quantity;
  the true mass depends on the unknown orbital inclination i. The
  cfg adopts i ≈ 35° from the τ Ceti debris disk plane (assumed
  coplanar), giving true mass ≈ 6.8 M⊕. A future astrometric
  detection (Gaia DR4 binary catalog) could constrain i and
  therefore the true mass, possibly shifting f from sub-Neptune
  toward super-Earth bulk classification.
- **Radius is assumed, not measured.** The DB stores radius
  1.81 R⊕ from a sub-Neptune mass–radius relation. f does not
  transit, so this is unconstrained from below. If true mass is
  higher (sin i < 0.7) and the planet is rocky-with-thin-ice
  rather than sub-Neptune-with-thick-envelope, R could be as low
  as 1.4 R⊕ with ρ ≈ 8 g/cc.
- **User input: a P=4562 d / 5 AU "h-candidate".** The user
  request for this synthesis described a τ Cet h at P = 4562 d
  and a ≈ 5.0 AU (near the asteroid-analog belt inner edge). The
  DB authoritative h is at P = 49.41 d / a = 0.243 AU. The 4562 d
  candidate is plausibly a Feng 2018 §3.4 long-period signal or a
  later (Lubin 2024) candidate that the DB has not ingested. The
  curation question is logged in `db/systems/tau_cet.json` Open
  items; this Phase 3 synthesis treats f as the *outermost*
  current-DB planet at 1.33 AU, consistent with the DB.
- **Bare-rock airless cfg variant.** An alternative reading: f
  has lost its volatile envelope completely (perhaps via giant
  impacts during the host's old age). The bare-rock variant would
  show exposed silicate basement with weathering patterns under
  G8V illumination, no atmosphere haze, and a sharper terminator.
  Preserved as a cfg variant in the Open items; not the canonical
  pick.
- **Sub-glacial ocean cfg detail.** If a future Europa-class
  interior model (extended to the super-Earth regime) confirms a
  buried liquid layer, the cfg could add a cryovolcanic plume
  Region pattern near regions of elevated heat flux. Currently
  treated as a Confidence=low feature, not animated.

## Related

- [tau-cet](tau-cet.md) — host star Phase 3 (G8V metal-poor;
  quiet, old, debris-disk-bearing)
- [tau-cet-g](tau-cet-g.md) — inner sibling, hot bare-rock
- [tau-cet-h](tau-cet-h.md) — inner-middle sibling, Venus-analog
- [methodology](../reference/methodology.md) — Decisions schema
- [rex-data-comparison](../reference/rex-data-comparison.md) — §6
  documents the τ Ceti e curation gap referenced in the host
  Phase 3
