<!-- tau Cet e Phase 3 synthesis: refuted (False Positive) detection re-included as a documented divergence per project decision -->
# τ Ceti e — Phase 3 Synthesis (Refuted — included as documented divergence)

τ Ceti e was originally one of four RV planet candidates announced
by Feng et al. 2017 (`2017AJ....154..135F`, arXiv:1708.02051) around
the metal-poor G8V τ Ceti — a 3.93 M⊕ (M sin i) super-Earth on a
162.87-day orbit at 0.538 AU, sitting just inside the optimistic
habitable zone (Kopparapu et al. 2014). It was the most disputed of the four
Feng detections from the start, with the lowest amplitude-to-noise
ratio and a stellar-activity contamination concern flagged in
Feng 2017 §6.

**Now classified as False Positive (NEA 2026-04-09)**, following
Figueira et al. 2025 (`2025A&A...700A.174F`,
doi:10.1051/0004-6361/202553869) ESPRESSO sub-10 cm/s RV
non-detection of the 162-day signal. Cretignier et al. 2021
(`2021A&A...653A..43C`) had earlier reached the same negative
conclusion with the YARARA stellar-activity post-processing applied
to HARPS data; ESPRESSO is the instrument-level confirmation that
the original signal is stellar activity, not a planet. Per a project
decision, e is **re-included** in `db/systems/tau_cet.json::planets[]`
at its pre-retraction Feng 2017 values as a refuted-flagged documented
divergence (PHM Adrian cultural weight).

**This Phase 3 synthesis is a documented divergence — e is included
per project decision despite the False Positive disposition.** The cfg
adopts the pre-retraction Feng 2017 parameters; every row carries
Confidence=low because the underlying signal is now considered an
artifact, and the canonical reading is no planet. The synthesis preserves the
Feng 2017 picture for cultural cross-reference (the planet was the
real-world model for "Adrian" in Andy Weir's *Project Hail Mary*,
2021), for the rex-data-comparison §6 curation thread, and as a
worked example of how a once-confirmed detection looks under the
False Positive reclassification.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `disposition` | False Positive Planet (NEA 2026-04-09) | high | Figueira 2025 ESPRESSO refutation; Cretignier 2021 YARARA earlier non-detection. The only high-confidence row in this table |
| `tidally_locked` | false | low | At P = 162.87 d and a = 0.538 AU around 0.78 M☉, tidal-lock timescale exceeds 7 Gyr; would not be locked if it existed. Vinson 2017. Confidence low because the planet does not exist |
| `obliquity_deg` | 23 | low | Tie-break: Earth-like default for an asynchronous super-Earth; no observational constraint and no body to constrain |
| `eccentricity` | 0.18 (+0.18 / −0.14) | low | Feng 2017 RV fit; uncertainty bracket so wide that 0 is within the published 1σ — itself a hint the signal was marginal |
| `argument_of_periastron_deg` | 22 (+75 / −46) | low | Feng 2017 RV fit; poorly constrained, the worst of the four planets |
| `sidereal_period_days` | 162.87 (+1.08 / −0.46) | low | Feng 2017 RV; signal now attributed to stellar activity (Figueira 2025) |
| `semi_major_axis_au` | 0.538 | low | Feng 2017 from Kepler's third law + host mass; geometrically valid, physically vacuous |
| `inclination_deg` | 35 | low | Tie-break: would have inherited the τ Ceti debris disk inclination (MacGregor 2016) on the coplanar assumption; moot for a refuted signal |
| `mass_mearth` | 3.93 (M sin i) | low | Feng 2017 RV; ±0.4 from amplitude fit. With the signal refuted, this is a record of the original measurement, not a property of any body |
| `radius_rearth` | 1.81 | low | Feng 2017 catalogued radius from mass–radius relation (Weiss & Marcy 2014 sub-Neptune); never measured |
| `surface_gravity_g_earth` | 1.20 | low | derived = 3.93 / 1.81²; same caveat |
| `density_g_cc` | 3.66 | low | derived; sub-Neptune-class if it existed |
| `water_mass_fraction` | 0.10–0.30 | low | Theoretical: an inner-edge optimistic-HZ super-Earth at 0.538 AU around a metal-poor G8V would carry a modest volatile inventory in the Feng 2017 picture |
| `insolation_s_earth` | 1.69 | low | derived L_bol/a²: 0.488 L☉ (Teixeira 2009, recommended) / (0.538 AU)² — between Earth (1.0) and Venus (1.91); inside the conservative HZ inner edge for G8V (Kopparapu 2014: ~1.05 S⊕) |
| `equilibrium_temp_k` (A=0) | 317 | low | derived 278 × (L/a²)^0.25 — slightly above Earth's 255 K |
| `equilibrium_temp_k` (A=0.3) | 290 | low | derived with Earth-analog albedo — comfortably in the liquid-water range |
| `bond_albedo` | 0.30 | low | Tie-break: Earth-analog default for a temperate super-Earth in the original Feng 2017 picture |
| `surface_temp_global_mean_k` | 295 | low | Earth-analog moderate-greenhouse scenario from the historical reading — assumes thin N₂/CO₂ atmosphere with modest H₂O vapor |
| `surface_temp_substellar_k` | 310 | low | Asynchronous slow rotator — diurnal substellar peak modestly above mean |
| `surface_temp_nightside_k` | 280 | low | Thick-enough atmosphere to limit night-side cooling in the historical reading |
| `atmosphere_present` | true (Earth-analog) | low | Historical Feng 2017 picture assumed a temperate atmosphere; no observation ever attempted because the planet does not exist |
| `atmosphere_surface_pressure_pa` | 100 000 | low | 1 bar adopted as the canonical Earth-analog default for the historical scenario; never measured |
| `atmosphere_composition` | N₂ ~78%, CO₂ ~2–5%, H₂O variable, trace O₂ uncertain | low | Historical Earth-analog reading; metal-poor host slightly reduces primordial volatile inventory; no biosphere assumption |
| `atmosphere_scale_height_km` | 7.0 | low | derived: kT/μg with T≈290 K, μ=29, g=11.8 m/s² |
| `atmosphere_tint_rgb_hex` | `#8a99aa` (pale blue-grey under cleaner G8V SED) | low | Tie-break: Rayleigh scattering at 1 bar gives an Earth-like blue, slightly cooler-toned than the Sun's pale-blue because of the metal-poor SED |
| `cloud_cover_fraction` | 0.50 | low | Earth-analog default for the historical picture |
| `cloud_tint_rgb_hex` | `#ece6dc` (clean cream-white H₂O clouds under G8V light) | low | Tie-break: standard H₂O cloud-top reflectance under the cleaner-yellow G8V SED |
| `ocean_present` | true (partial coverage in historical reading) | low | Historical Feng 2017 picture supported surface liquid water; volatile inventory + insolation would have allowed it. Refuted. |
| `ocean_extent_substellar_radius_deg` | n/a (asynchronous rotator) | low | Not eyeball geometry — slow asynchronous rotation distributes any ocean coverage globally rather than in a substellar patch |
| `ocean_tint_rgb_hex` | `#2a4a68` (deep ocean under cleaner G8V SED) | low | Tie-break: Rayleigh-blue ocean, slightly cooler-toned than Earth's because of the metal-poor host SED |
| `surface_ice_caps` | seasonal polar caps possible | low | Mild eccentricity (0.18) + asynchronous spin give modest seasonal cycling; polar ice formation plausible in the historical picture |
| `surface_tint_rgb_hex_primary` | `#7a6a58` (continental basalt-and-sediment surface under G8V illumination) | low | Tie-break: Earth-like continental blend; metal-poor primordial dust is slightly less iron-stained than terrestrial soils |
| `surface_tint_rgb_hex_accent` | `#4a6840` (vegetation-analog or olivine-rich surface patches) | low | Tie-break: Project Hail Mary's "Adrian" was rendered as having vegetation-like surface features. Confidence low: no biosphere is implied by the data — this is fictional cross-reference only |
| `surface_morphology` | mixed continent/ocean Earth-analog in the historical reading | low | Feng 2017 picture; surface morphology was never observed |
| `magnetic_field_present` | true (modest) | low | A 4–5 M⊕ rocky body with multi-week asynchronous rotation could plausibly sustain a dynamo if it existed |
| `magnetic_field_strength_microtesla_equator` | 30 | low | Tie-break: RM22 scaling for the assumed parameters; comparable to Earth's |
| `tidal_heating_w_m2` | 0.001–0.01 | low | e = 0.18 at 0.538 AU; modest tidal flux in the historical scenario |
| `induction_heating_w_m2` | < 0.001 | low | Quiet host (log L_X ≤ 26.5); negligible induction |
| `radiogenic_heat_w_m2` | 0.04 | low | Earth-analog mantle radiogenics scaled by mass |
| `aurora_present` | true (modest) | low | Modest field + atmosphere in the historical scenario; faint diffuse aurora possible |
| `aurora_color_primary_hex` | `#4DFF4D` | low | Tie-break: [OI] 557.7 nm green if any O₂; N₂ Vegard-Kaplan blue-green otherwise |
| `aurora_intensity_kR_typical` | 1 | low | Quiet host — auroral excitation rate well below Earth's |
| `star_apparent_angular_diameter_deg` | 0.786 | low | derived: 2 × R★ / a × (180/π); roughly 1.5× the Sun seen from Earth |
| `stellar_illumination_color_temp_k` | 5370 | low | host Teff (Pavlenko 2012); applies to the historical scenario only |

## Surface synthesis

In the Feng 2017 picture, τ Ceti e sat at 1.69 S⊕ — comparable to
or slightly inside the conservative habitable zone inner edge for a
G8V host (Kopparapu 2014: ~1.05 S⊕). At this insolation, e was the
"interesting" planet of the four — warmer than Earth but not in
the Venus-class runaway regime, with an equilibrium temperature of
317 K at zero albedo or 290 K under an Earth-analog 0.3 bond
albedo, comfortably in the liquid-water range. Kopparapu et al.
2014's optimistic inner edge (which extends inward to ~0.75 S⊕)
was the framework most often cited when e was
discussed as a habitability target between 2017 and 2025.

**The historical scenario assumed a partially-ocean-covered super-
Earth.** With 3.93 M⊕ (M sin i) and a sub-Neptune-relation radius of
1.81 R⊕, the Feng 2017 picture supported a temperate world with a
modest 1-bar N₂/CO₂ atmosphere, surface oceans covering perhaps
30–60% of the planet, and seasonal polar ice caps modulated by the
0.18 eccentricity. Surface temperature in this reading was ~295 K
globally, with the substellar diurnal peak ~310 K and the
nightside ~280 K — Earth-temperate with a stronger pole-to-equator
gradient than Earth because of the slow asynchronous rotation.

**Color choice — Earth-analog with metal-poor host correction.** If
e existed and were rendered, the primary surface tint `#7a6a58`
encodes a continental blend (basalt + sediment) under the cleaner-
yellow G8V SED. The accent `#4a6840` is reserved for vegetation-
analog or olivine-rich patches — a tie-break that explicitly nods to
the Andy Weir "Adrian" fictional rendering, which depicted vegetation-
like features. *This is a fiction cross-reference, not a physical
prediction.* No data ever supported a biosphere on e, and with the
False Positive disposition the question is moot.

**Refutation context.** The Feng 2017 signal at 162 d turned out to
be a stellar-activity artifact correlated with τ Ceti's slow
magnetic cycle — the 162-d period is roughly P_rot / 4 to 5 (the
host rotates at 34 d in the Baliunas 1996 frame, or 46 d per Boro
Saikia 2018 ZDI), placing the false signal in the harmonic regime
typical of activity-induced RV noise on quiet G dwarfs. Cretignier
2021 first identified this with the YARARA post-processing technique;
Figueira 2025 confirmed it with ESPRESSO's sub-10 cm/s precision,
where the 162-d signal failed to appear in the cleaner instrument's
data.

## Atmosphere synthesis

The atmosphere synthesis is the most thoroughly historical part of
this document. No atmosphere was ever observed; the Feng 2017
picture assumed Earth-analog conditions because the inferred
insolation placed e in the optimistic HZ, but the underlying signal
is now considered an artifact.

**Pressure choice — 1 bar (historical).** The Feng 2017 picture's
Earth-analog default is 1 bar surface pressure. This was the
working assumption in habitability discussions and in popular-
science treatments (including *Project Hail Mary*'s Adrian
rendering). Under Wordsworth 2015's framework, an inner-HZ super-
Earth at 1.69 S⊕ on a metal-poor quiet G dwarf could maintain a
1-bar N₂-dominated atmosphere over multi-Gyr timescales — XUV-
driven hydrodynamic loss is negligible (log L_X ≤ 26.5; Schmitt
1985), Jeans escape for N₂ at Teq = 290 K is ineffective.

**Composition (historical).** Earth-analog with metal-poor host
correction: N₂ ~78%, CO₂ ~2–5% (slightly elevated relative to Earth
to maintain temperate Teff under the lower G8V insolation), H₂O
vapor variable, trace O₂ uncertain (no biosphere assumed without
evidence). The metal-poor host implies marginally less primordial
volatile inventory than Earth had at the same orbital regime.

**Sky appearance (historical).** Pale blue-grey (`#8a99aa`) Rayleigh
scattering under the cleaner G8V SED — slightly cooler-toned than
Earth's sky because the host emits less blue continuum. The host
star subtends 0.786° from e's surface (about 1.5× the Sun's angular
size from Earth) — a bright pale-yellow disk under the metal-poor
SED. Clouds would have appeared cleaner cream-white (`#ece6dc`)
rather than Earth's warmer-toned clouds. Surface illumination
would have been roughly 1.6× Earth's irradiance — a bright Earth-
like day with a marginally cooler color temperature.

**Loss mechanisms (historical context).** The host's quiet XUV
environment is the most important factor: e at 0.538 AU around a
log R'HK = −4.95 quiet G dwarf would have experienced essentially no
hydrodynamic escape over 7 Gyr. The atmosphere in the Feng 2017
picture was therefore an exceptionally secure 1-bar envelope —
arguably more secure than Earth's own (which experiences modest
solar-wind erosion). This was part of the case for Adrian being a
plausible long-term habitable world in the Andy Weir narrative.

## Rotation & spin synthesis

If τ Ceti e existed, it would **not be tidally locked**. At P =
162.87 d and a = 0.538 AU around a 0.78 M☉ host, the tidal-lock
timescale (Vinson 2017 formula, τ_lock ∝ a^6 / (M_p × Q × R_p^5))
is approximately 30 Gyr — well beyond the system age. Spin damping
has not had time to operate.

**Pseudo-synchronous spin candidate.** With eccentricity 0.18,
e would be a strong candidate for capture into a high-order spin-
orbit resonance (Hut 1981 pseudo-synchronous rotation, ω_spin ≈
ω_orb × f(e)). At e = 0.18, Hut's f(e) ≈ 1.4, giving a pseudo-
synchronous spin period of ~116 d — a long but non-locked rotation.
The 3:2 resonance is also possible at this eccentricity (Vinson
2017 capture probability ~30–50%), giving a spin period of ~109 d.

**Asynchronous fast rotator alternative.** If neither pseudo-
synchronous nor 3:2 capture occurred, e could rotate at a primordial
period of hours to days, with slow tidal damping over 7 Gyr
incomplete because of the long orbital period. The cfg-historical
default in this synthesis adopts a generic "multi-week asynchronous
slow rotator" without specifying a precise value, because the
question is moot for a refuted body.

**Obliquity.** Adopt Earth-analog 23° as a default tie-break. The
0.18 eccentricity gives orbital insolation variation of ±36% peak-
to-trough — significantly stronger than Earth's ±3.4% — producing
substantial "eccentricity seasons" over the 162-day orbit. In the
historical picture this would have driven polar ice-cap formation
and seasonal hemispheric weather patterns.

**Magnetic dynamo expectation (historical).** A 4–5 M⊕ rocky body
with multi-week rotation could plausibly sustain a moderate dynamo.
RM22 (Reiners-Christensen) scaling gives a surface field of ~30 μT
(comparable to Earth's 25–65 μT). Not relevant to cfg because no
cfg body is built.

## Visual styling

This section is the most cultural part of the synthesis, framing
the planet "as it was depicted" rather than "as it exists" (because
it does not).

- **Global appearance (if it existed).** A blue-green-and-cream
  Earth-analog world with continental landmasses, partial ocean
  coverage, and seasonal polar ice. Visual character closest to a
  slightly larger, warmer Earth — the standard "habitable super-
  Earth" rendering that dominated the 2017–2025 popular-science
  treatments and Andy Weir's depiction of Adrian.
- **Dayside detail (historical reading).** Continents in mixed
  basalt-and-sediment `#7a6a58` tones with vegetation-analog or
  olivine-rich patches `#4a6840`. Ocean coverage 30–60% in
  `#2a4a68` Rayleigh-blue, slightly cooler-toned than Earth's
  oceans because of the metal-poor G8V SED. Cloud bands at low
  latitudes from Hadley-cell circulation.
- **Terminator band (historical).** Soft cloud-and-shadow gradient
  characteristic of a temperate atmosphere — much less crisp than
  the airless Mercury-analog sibling g, much more developed than
  the snowball outer sibling f.
- **Nightside appearance (historical).** Dark with cyan-white
  cloud highlights from starlight reflection. No urban lights
  because no biosphere was implied by the data — *Project Hail
  Mary*'s Adrian is depicted as uninhabited prior to the human
  expedition.
- **Atmosphere haze (historical).** Pale blue-grey (`#8a99aa`)
  Rayleigh limb glow ~30–50 km thick, similar in character to
  Earth's blue limb but with a marginally cooler tone.
- **Faint aurora (historical).** Possible diffuse green-tinted
  polar aurora at ~1 kR; not a defining feature of the rendering.
- **Star in sky (historical).** τ Ceti would subtend 0.786° from
  e's surface — about 1.5× the Sun's angular size from Earth. A
  bright pale-yellow disk under the metal-poor G8V illumination,
  delivering 1.69× Earth's irradiance at the substellar point.
- **"Adrian" cultural cross-reference.** Andy Weir's *Project
  Hail Mary* (2021) names e as Adrian and uses it as the
  protagonist's mission target. The novel adopts Feng 2017's
  orbital parameters (P ≈ 168 d, a ≈ 0.55 AU, M sin i = 3.93 M⊕)
  but constructs an environment that diverges from the
  habitable-Earth-analog framing — see the "Weir's Adrian" bullet
  below. The 2025 ESPRESSO refutation post-dates the novel by
  four years. NearStars does not render Adrian in-game because
  the underlying body does not exist; this Phase 3 markdown is
  the cultural cross-reference home, paired with
  `docs/reference/cultural-context.md § Tau Ceti`.
- **Weir's Adrian — diverges from the historical Earth-analog
  rendering above.** *Project Hail Mary* does not depict Adrian
  as an Earth-analog blue-green ocean world. The novel's stated
  parameters (compiled from Weir interviews + in-novel
  measurements) are: surface gravity 1.4 g, atmosphere 91% CO₂ /
  7% CH₄ / 1% Ar / trace (no significant N₂ — plot-critical
  because Taumoeba is nitrogen-intolerant), green appearance from
  space, sampling carried out at 91.2 km altitude where
  p = 0.02 bar and T = −51 °C. Weir's pressure structure implies
  a multi-bar CO₂-dominated surface atmosphere — closer to a
  temperate Venus-analog than to Earth. No ocean is described in
  the novel; the sampling mission targets upper-atmosphere clouds
  via a 10 km xenonite chain, never the surface. The vegetation-
  accent tone `#4a6840` in the Decisions table above is the
  closest match to Weir's "green planet" descriptor, but Weir's
  rendering is *photochemical-haze green* (CH₄ + CO₂ + airborne
  Taumoeba biology), not vegetation green. Surface gravity 1.4 g
  implies Weir adopted a rockier (smaller-radius) mass-radius
  relation than the popular-science sub-Neptune fit (1.81 R⊕,
  1.20 g) — closer to 1.68 R⊕ at the same 3.93 M⊕. Both the
  historical Earth-analog (table above) and Weir's CO₂-haze
  reading are fiction at this point; neither is observed.

## Bibliography

### Read (signal history + refutation)

- **Feng F. et al. 2017** — *Color difference makes a difference:
  four planet candidates around τ Ceti*, AJ 154, 135
  (`2017AJ....154..135F`, arXiv:1708.02051). Original discovery
  paper. Reports e at P = 162.87 d, M sin i = 3.93 M⊕, e = 0.18.
  Anchors the historical Decisions rows above. Feng 2017 §6
  itself cautions that e is the most amplitude-marginal of the
  four.
- **Cretignier M. et al. 2021** — *YARARA: stellar-activity
  post-processing for HARPS RV*, A&A 653, A43
  (`2021A&A...653A..43C`). First non-detection of the 162-d
  signal after stellar-activity decorrelation. Identifies the
  signal as activity-correlated rather than planetary.
- **Figueira P. et al. 2025** — *ESPRESSO RV monitoring of τ Ceti:
  refutation of e and tightened limits on f/g/h*, A&A 700, A174
  (`2025A&A...700A.174F`, doi:10.1051/0004-6361/202553869).
  Instrument-level confirmation that e is a stellar-activity
  artifact. ESPRESSO's sub-10 cm/s precision is below the original
  Feng 2017 amplitude; the 162-d signal is absent. Drives the
  False Positive disposition adopted by NEA 2026-04-09.

### Read (context for habitability framing)

- **Kopparapu R. K. et al. 2014** — *Habitable zones around
  main-sequence stars*, ApJL 787, L29 (arXiv:1404.5292, cache
  `_papers/1404.5292.md`). Conservative HZ inner edge at ~1.05 S⊕
  for a G8V; the optimistic inner edge extends inward to ~0.75 S⊕,
  placing Feng 2017's e at 1.58 S⊕ comfortably inside the
  optimistic HZ and driving the popular-science framing of e as
  "habitable." The gap between the conservative (~1.05 S⊕) and
  optimistic (~0.75 S⊕) inner edges was part of the debate over
  e's habitability classification before refutation.
- **Wordsworth & Pierrehumbert 2015** (general atmospheric-escape
  argument) — used here as a generic atmosphere-retention reference
  underlying the 1-bar Earth-analog atmosphere assumed in the
  historical reading; specific title not pinned.

### Read (host star context)

- **Pavlenko Y. V. et al. 2012** — host star [Fe/H] = −0.55,
  log R'HK = −4.95, Teff = 5344 K. Drove the historical
  metal-poor-host framing for the e atmosphere and color choices.
- **Mamajek E. E. & Hillenbrand L. A. 2008** — gyrochronological
  age 7 ± 1.5 Gyr; relevant to the historical atmospheric-retention
  argument over multi-Gyr timescales.
- **Schmitt J. H. M. M. et al. 1985** — host X-ray
  log L_X ≤ 26.5. The quiet XUV environment was central to the
  "secure atmosphere" framing in the historical reading.
- **Boro Saikia S. et al. 2018** — ZDI 46-d rotation; relevant
  because the refuted 162-d signal lies at a harmonic of the host
  rotation, consistent with activity-induced false-detection.

### Read (cultural cross-reference)

- **Weir A. 2021** — *Project Hail Mary* (novel). Names e as
  "Adrian" and uses it as the protagonist's mission target. The
  novel pre-dates the 2025 refutation by four years and is the
  most prominent cultural anchor for the e detection. Documented
  in `docs/reference/cultural-context.md § Tau Ceti`.

### Read (fiction worldbuilding reference — Weir's stated Adrian parameters)

- **Weir A. — Scientific American Science Quickly podcast, "The real science and the fun fiction behind Project Hail Mary"**. Weir walks through the gravity / atmosphere derivation. Adopted Feng 2017's M sin i = 3.93 M⊕ and back-calculated surface gravity ~1.4 g under a rocky mass-radius relation. Also explains why Tau Ceti: ~9 Gyr stellar age gives life a head start over Earth.
- **Weir A. — Astronomy.com, "Andy Weir on the science of Project Hail Mary"**. Sources the deliberate single-genesis panspermia design: Adrian is the origin of Astrophage and the *only* Astrophage-resistant biosphere (Taumoeba is endemic there).
- **Weir A. — Eridian worldbuilding companion document** (provided by user 2026-05-27 as `eridian.docx`). Authoritative Erid (40 Eri A b) parameters: **28 atm NH₃**, **210 °C** surface, **2.09 g**, **5.1-h sidereal day** (≈ 18 397 s), **25 × Earth** magnetic field, density 5 710 kg/m³, radius 12 835 km, mass 8.47 M⊕ (Ma 2018 measured). Also explicitly states the panspermia event seeded Earth + Erid from **Tau Ceti** — i.e. Adrian is the panspermia source, Erid + Earth the recipients. Cited here only to disambiguate Adrian-vs-Erid parameter conflation in popular summaries.
- **Sky & Telescope — "Explore the Worlds of Project Hail Mary" (2021)**. Confirms Weir wrote from the Feng 2017 detection picture pre-refutation. Frames Tau Cet e and 40 Eri A b as the two anchor real-exoplanet detections behind Adrian + Erid.
- **Project Hail Mary Fandom Wiki — Adrian / Taumoeba / Astrophage pages**. Fan-compiled index of in-novel measurements (1.4 g, 91% CO₂ / 7% CH₄ / 1% Ar atmosphere, green appearance; Taumoeba habitat at 91.2 km / 0.02 bar / −51 °C; nitrogen-intolerance). Citation pointer into the novel text, not a primary authority.
- **Wheeler D. — "Project Hail Mary Stellar Map" (dwheeler.com/essays/project-hail-mary-map.html)**. Third-party derivation showing Wheeler reconstructs Adrian's orbit from Feng 2017 directly (P = 168 d, a = 0.552 AU). The novel does not state these numbers explicitly; they are inferred from the e identification.

### Not read — superseded or low-priority (~10 papers)

- **Tuomi M. et al. 2013** + **Tuomi 2014 erratum** — earlier
  5-planet τ Ceti claim that included e at slightly different
  parameters. Superseded by Feng 2017; both are now historical
  given the refutation.
- **Various astrobiology speculation papers (2017–2024)** —
  habitability assessments of e under the Feng 2017 picture.
  No cfg relevance under the False Positive disposition; left
  unread for this synthesis.
- **SETI / technosignature papers targeting e** — historical
  observations made before the refutation; no cfg relevance.

## Open items for follow-up

- **Disposition is settled.** Unlike f / g / h (which remain
  `pl_controv_flag = 1` and are on retraction watch — see those
  Phase 3 syntheses for the open Lubin 2024 / future-ESPRESSO
  question), e's disposition is final: False Positive Planet
  per NEA 2026-04-09. No further follow-up is expected to
  re-promote e.
- **Cultural-context cross-reference is the canonical home.**
  Any future "Adrian" rendering — for example as a flavor-text
  Easter egg in a NearStars patch — should reference
  `docs/reference/cultural-context.md § Tau Ceti` rather than
  spawning a cfg body. The novel is fiction; the underlying
  planet is not.
- **Sibling retraction watch.** Figueira 2025 also reports
  tightened limits on f / g / h. While none of the three is
  formally refuted yet (NEA still carries them as disputed),
  the f / g / h Phase 3 syntheses' Open items track the
  retraction-watch question. If a future ESPRESSO reanalysis
  refutes any of them, this template (historical-only Phase 3
  with all-low Confidence) is the precedent.
- **`db/systems/tau_cet.json::meta.notes` should document the
  false-positive disposition for e.** Currently the DB simply
  omits e from `planets[]`; an explicit `meta.notes` entry
  citing Figueira 2025 + NEA 2026-04-09 would make the omission
  self-documenting rather than appearing as a curation gap to
  future readers.

## Related

- [tau-cet](tau-cet.md) — host star Phase 3 (G8V metal-poor;
  quiet, old, debris-disk-bearing)
- [tau-cet-f](tau-cet-f.md) — sibling, outermost, snowball
- [tau-cet-g](tau-cet-g.md) — sibling, innermost, hot bare-rock
- [tau-cet-h](tau-cet-h.md) — sibling, middle, Venus-analog
- [cultural-context](../reference/cultural-context.md) — §
  Tau Ceti, "Adrian" in *Project Hail Mary*
- [rex-data-comparison](../reference/rex-data-comparison.md) — §6
  τ Ceti e historical curation gap (now resolved by NEA 2026-04-09
  False Positive disposition)
- [methodology](../reference/methodology.md) — Decisions schema
