<!-- tau Cet h Phase 3 synthesis: cfg-ready decisions and reasoning -->
# τ Ceti h — Phase 3 Synthesis

τ Ceti h is a 1.83 M⊕ (M sin i) RV candidate on a 49.41-day orbit at
0.243 AU around the metal-poor G8V τ Ceti (Feng 2017,
`2017AJ....154..135F`). It sits between g (0.133 AU) and f (1.334
AU) in `db/systems/tau_cet.json`. At 0.488 L☉ host luminosity, h
receives **8.26 S⊕** — Venus-class insolation but on a fainter,
cooler host. The equilibrium temperature is 472 K at zero albedo or
334 K with a Venus-like cloud albedo, comfortably above the H₂O
critical point and in the classic runaway-greenhouse regime. The
planet is **disputed** in NEA (`pl_controv_flag = 1`) — RV-only, no
transit, no direct imaging. Notably, h's eccentricity (0.23) is the
highest of the three Feng 2017 planets — it sits cleanly in the
3:2-spin-orbit-capture regime (Vinson 2017 / Makarov 2018) and the
elevated eccentricity contributes additional tidal heating at a
non-trivial level.

**Scenario choice for NearStars: a Venus-analog with a thick CO₂
runaway-greenhouse atmosphere, sulfate aerosol cloud deck obscuring
the surface, a hot dry rocky basement, and a featureless yellow-
cream cloud-top palette under quiet G8V illumination.** The host's
quiet XUV environment is the key physical lever: unlike Venus
analogs around active K/M dwarfs (which experience runaway
atmospheric loss), τ Ceti h's thick CO₂ envelope is *more* secure on
this metal-poor low-activity host. Bare-rock and intermediate-thick
alternatives are preserved as cfg variants.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false (3:2 spin-orbit; pseudo-synchronous) | medium | P=49.41 d on 0.78 M☉ host: τ_tidal lock timescale exceeds system age; e = 0.23 puts h cleanly in 3:2-capture regime (Vinson 2017 / Makarov 2018: 3:2 strongly preferred for e ≳ 0.10) |
| `obliquity_deg` | 0 | medium | Tidal damping over 7 Gyr drives obliquity to zero even for slow rotators |
| `eccentricity` | 0.23 | medium | Feng 2017 RV — uncertainty consistent with secular perturbations from f/g and possible orbital chaos |
| `argument_of_periastron_deg` | 7.45 | medium | Feng 2017 RV |
| `sidereal_period_days` | 49.41 | high | Feng 2017 RV — uncertainty ±0.08 d |
| `semi_major_axis_au` | 0.243 | high | Feng 2017 (±0.003 from Kepler's third law + host mass) |
| `inclination_deg` | 35 | low | Tie-break: τ Ceti debris disk inclination (Lawler et al. 2014, adopted by MacGregor et al. 2016; assumed coplanar) |
| `mass_mearth` | 1.83 (M sin i; true mass ≳ 2.3 M⊕ assuming sin i ≈ 0.7) | medium | Feng 2017 RV (±0.68 — the largest fractional uncertainty of the three) |
| `radius_rearth` | 1.19 | low | Feng 2017 catalogued radius from mass–radius relation (rocky); not directly measured |
| `surface_gravity_g_earth` | 1.29 | medium | derived = 1.83 / 1.19² |
| `density_g_cc` | 5.99 | medium | derived; Earth-like rocky composition consistent with the mass–radius relation pick |
| `water_mass_fraction` | < 0.001 | medium | Runaway-greenhouse history: any primordial water photolyzed and lost as H over Gyr timescales; surface absolutely dry |
| `insolation_s_earth` | 8.26 | high | derived L_bol/a²: 0.488 L☉ (Teixeira 2009, recommended) / 0.243² |
| `equilibrium_temp_k` (A=0) | 472 | high | derived 278 × (L/a²)^0.25 |
| `equilibrium_temp_k` (A=0.75, Venus-cloud) | 334 | high | derived with Venus-analog cloud-top bond albedo |
| `bond_albedo` | 0.75 | low | Venus-analog sulfate cloud deck (Venus analog; standard value) |
| `surface_temp_global_mean_k` | 720 | medium | Runaway-greenhouse with 50-bar CO₂ + H₂SO₄ clouds; ~Venus surface temperature |
| `surface_temp_substellar_k` | 730 | medium | Thick atmosphere homogenizes dayside vs. nightside; minimal substellar enhancement |
| `surface_temp_nightside_k` | 710 | medium | Same — thick atmosphere transports heat efficiently around the slow rotator |
| `atmosphere_present` | true (thick CO₂) | medium | Adopted Venus-analog scenario; quiet host XUV preserves heavy CO₂ over 7 Gyr |
| `atmosphere_surface_pressure_pa` | 5 000 000 | low | scenario choice — Venus analog; mixing ratios are template values, no atmospheric data for this planet |
| `atmosphere_composition` | CO₂ ~95%, N₂ ~3.5%, SO₂ + H₂SO₄ aerosols ~1%, trace H₂O <100 ppm | low | scenario choice — Venus analog; mixing ratios are template values, no atmospheric data for this planet |
| `atmosphere_scale_height_km` | 6.9 | medium | derived: kT/μg with T≈460 K (mid-atmosphere), μ=44, g=12.6 m/s² |
| `atmosphere_tint_rgb_hex` | `#d8c490` (warm yellow-cream from CO₂ + sulfate aerosol haze under G8V illumination) | medium | Venus-analog cloud-top reflectance; G8V illumination is cleaner-yellow than Sol's, giving a slightly cooler-yellow tone than Venus |
| `cloud_cover_fraction` | 1.00 | high | Venus-analog complete cloud cover; surface obscured at all wavelengths |
| `cloud_morphology` | global homogeneous sulfate haze with subtle banded thermal structure at low latitudes; possible polar "collar" feature analogous to Venus's | medium | Venus-analog cloud morphology (Venus analog; standard value); rotation rate similar enough for Hadley-cell structure |
| `cloud_tint_rgb_hex` | `#e0cba0` (yellow-cream cloud tops, G8V-illuminated) | medium | Same physics as `atmosphere_tint`; cloud-top reflectance is the dominant visual feature |
| `ocean_present` | false | high | Far above water critical point; surface absolutely dry |
| `ocean_extent_substellar_radius_deg` | 0 | high | No surface liquid |
| `ocean_tint_rgb_hex` | n/a | high | No ocean |
| `surface_ice_caps` | none | high | Far above water freezing point everywhere; no ice |
| `surface_tint_rgb_hex_primary` | `#5a4838` (dark basaltic surface, obscured by cloud deck — visible only in occasional cloud breaks at PQS gameplay resolution) | low | Tie-break: Venus surface is dark basalt at radar wavelengths (Magellan); for cfg the surface tint is mostly irrelevant because the cloud deck obscures it |
| `surface_tint_rgb_hex_accent` | `#7a3a20` (volcanic surface flows / iron-rich basalt patches) | low | Tie-break: Venus-analog volcanic geology; mostly invisible from orbit |
| `surface_morphology` | volcanic plains with shield volcanoes, tessera highlands, impact crater fields; mostly obscured by cloud deck | medium | Venus analog (Ivanov & Head 2011) |
| `magnetic_field_present` | false | medium | Slow rotation (3:2, ~98.8-d solar day) + tidally heated but probably mostly-solid mantle → likely no active dynamo; Venus-analog absence of global field |
| `magnetic_field_strength_microtesla_equator` | 0.1 | low | Tie-break: induced magnetic moment only from solar-wind interaction; Venus analog |
| `tidal_heating_w_m2` | 0.05–0.5 | medium | e = 0.23 at a = 0.243 AU is significant; Bolmont 2020 scaling gives elevated tidal flux but still well below Io (~2 W/m²) — possibly Venus-analog volcanic activity |
| `induction_heating_w_m2` | < 0.001 | medium | Quiet host magnetic field; negligible induction |
| `radiogenic_heat_w_m2` | 0.04 | low | Earth-analog bulk-silicate-Earth radiogenic flux (~0.04 W/m² present-day), mass-scaled. Method: Wang et al. 2020 (`2020A&A...644A..19W`) exoplanet radiogenic-heat framework; its Eu→Th/U host-abundance refinement is not applied because per-host abundances are not curated, so an Earth-analog abundance is assumed |
| `aurora_present` | false | high | No global magnetic field → induced-only solar-wind interaction; no auroral oval (Venus-analog) |
| `star_apparent_angular_diameter_deg` | 1.74 | high | derived: 2 × R★ / a × (180/π); 3.3× the Sun seen from Earth |
| `stellar_illumination_color_temp_k` | 5370 | high | host Teff (Pavlenko 2012) |

## Surface synthesis

τ Ceti h is the system's **Venus analog**. At 8.26 S⊕ insolation,
even moderate primordial atmospheric outgassing leads to a runaway
greenhouse: H₂O is photolyzed to H + O, the H escapes (via Jeans on
this low-XUV host, more slowly than on Venus around the active early
Sun, but still effective over 7 Gyr), and the O is locked into
oxidized regolith. What remains is a CO₂-dominated thick atmosphere
maintained by ongoing volcanic outgassing balanced against very slow
escape on this quiet host.

The surface is therefore **hot, dry, and obscured**. Surface
temperature is approximately 720 K (Venus's is 735 K), surface
pressure approximately 50 bar (Venus's is 92 bar — h's lower value
reflects the metal-poor host's reduced primordial volatile
inventory). The atmosphere is so thick that horizontal heat transport
homogenizes the dayside and nightside even for a slow 3:2 rotator;
surface temperature contrast across the planet is at most a few K.

**Surface composition.** Volcanic plains with shield volcanoes,
tessera-style highland blocks, and impact crater fields are the
expected morphology — Venus-analog geology from Ivanov & Head 2011's
Magellan-era reconstruction. The metal-poor host produces a more
olivine-rich (Mg/Si > 1) basalt than Venus's tholeiitic; visually
the surface basement is darker than terrestrial basalt
(`#5a4838`), with localized iron-rich red-brown patches
(`#7a3a20`) from regional volcanic flows. **Most of this is invisible
from orbit.** The cloud deck obscures the surface at all wavelengths
except radar.

**Tidal heating possibly drives volcanism.** With e = 0.23 at a =
0.243 AU, the tidal flux is estimated at 0.05–0.5 W/m² — well above
Earth's continental heat flow (0.065 W/m²) and comparable to Io's
total surface heat flux (~2 W/m²) at the upper bound. The metal-poor
mantle would have a slightly elevated melting point relative to Sol-
system Venus, partially offsetting the tidal heat, but the net effect
is probably active volcanism. Whether this manifests as Venus-like
shield volcanism or Io-like sulfur volcanism depends on the volatile
inventory; the cfg adopts the Venus-analog shield interpretation
because the metal-poor host should reduce both Fe and S in the
primordial budget.

**No water, no biosignatures.** Runaway-greenhouse history removes
any chance of surface or subsurface water. Photolytic H escape over
7 Gyr should have removed multiple Earth oceans worth of H₂O. The
remaining O is locked in the oxidized regolith and atmospheric CO₂.

## Atmosphere synthesis

The cfg adopts a **50-bar CO₂ runaway-greenhouse atmosphere with
sulfate aerosol clouds** — a Venus analog tuned slightly thinner to
reflect the metal-poor host's lower primordial volatile inventory.

**Pressure choice — 50 bar.** Venus is 92 bar; Earth is 1 bar; Mars
is 0.006 bar. For a 1.83 M⊕ body in the Venus-insolation regime on a
metal-poor host, the steady-state atmospheric pressure depends on
the integrated outgassing rate over Gyr timescales and the loss rate.
Outgassing should be similar to Venus per unit volcanism, but with
elevated tidal heat the volcanism rate may be higher. The cfg picks
50 bar as an intermediate value; defensible alternatives span 10 bar
(Venus-thin, more like primordial Venus) to 92 bar (full Venus
analog).

**Composition.** Venus-analog: CO₂ ~95%, N₂ ~3.5%, SO₂ ~150 ppm,
H₂SO₄ aerosols, trace H₂O <100 ppm. The H₂O concentration is
suppressed below Venus's 30 ppm because the metal-poor host produces
less primordial water in the volatile inventory. Sulfate aerosols
form from volcanic SO₂ + photolytic OH → H₂SO₄ at the cloud-top
temperature ~250 K.

**Cloud morphology.** A global homogeneous sulfate haze obscures the
surface at all wavelengths. Within the cloud deck, Venus-analog
banded thermal structure is expected at low latitudes (Hadley-cell
driven), with possible polar collar features as on Venus. Cloud-top
altitude is ~50–70 km above the surface; cloud-top temperature is
~250 K. The cloud deck is the dominant visual feature of h.

**Sky appearance from the surface.** Yellow-cream haze obscures the
star. Surface illumination is approximately 5% of incident flux —
nearly twilight conditions at the surface despite 8.26 S⊕ at the
cloud top. The view from the surface is a uniform yellow-brown
glow, with no visible stellar disk; Venus-analog conditions. From
orbit, h is a featureless yellow-cream pearl (`#e0cba0`) with subtle
banding.

**Loss mechanisms suppressed.** Unlike Venus around the active
early Sun, h's host is exceptionally quiet (log L_X ≤ 26.5,
log R'HK = −4.95). XUV-driven hydrodynamic escape is negligible.
H₂O photolysis happens slowly; the primordial water inventory has
been bleeding off via Jeans escape over 7 Gyr but the integrated
loss is much smaller than Venus's. h is consequently a *more secure*
Venus analog than Venus itself in terms of atmospheric retention —
the thick CO₂ envelope should persist over geological timescales
without active replenishment.

## Rotation & spin synthesis

τ Ceti h's eccentricity of 0.23 is the highest of the three Feng
2017 planets. At this eccentricity, the 3:2 spin-orbit resonance
capture probability is high (Vinson 2017 Figure 5: > 80% for e ≳
0.10) and the cfg adopts **3:2** as the canonical spin-orbit state.

**Pseudo-synchronous rotation.** For 3:2 at P_orb = 49.41 d, the
spin period is 49.41 × 2/3 ≈ 32.94 d. The solar day length is
P_orb × P_spin / (P_orb − P_spin) = 49.41 × 32.94 / 16.47 ≈ 98.8 d
(approximately 2 × P_orb). The slow rotation produces minimal
Coriolis effect; atmospheric circulation should be Venus-like with a
single Hadley cell per hemisphere.

**Tidal-lock timescale.** P = 49.41 d is far longer than g's 20 d;
τ_tidal scales as P^(13/3), so h's tidal damping is roughly
(49.41/20)^(13/3) ≈ 50× slower than g's. Whether g is locked over
7 Gyr or not, h almost certainly is not fully locked — the 3:2
resonance with stable libration is the most plausible state.

**KSP implementation note.** For 3:2: `rotationPeriod` = (2/3) ×
49.41 d × 86400 s/d ≈ 32.94 d ≈ 2.85 × 10⁶ s. Asynchronous
fast-rotator alternative (much less likely): 24 h Earth analog.

**Obliquity.** Tidal damping over 7 Gyr drives obliquity to zero;
libration-induced insolation variation from the e = 0.23 eccentric
orbit is ±20% over the orbital period, producing significant
"seasonal" forcing at the cloud-top level but smoothed by the thick
atmosphere at the surface.

**Magnetic dynamo expectation.** A 2 M⊕ body with 3:2 slow rotation
and a thick CO₂ atmosphere (which insulates the interior) is
unlikely to have a sustained dynamo — Venus's own field is induced-
only. The cfg adopts a Venus-analog absence of global magnetic
field, with possible weak induced magnetosphere from solar-wind
interaction.

## Visual styling

- **Global appearance.** A featureless yellow-cream pearl
  (`#e0cba0`) with subtle low-latitude banding visible at PQS
  resolution. The cloud deck obscures any surface features. Visual
  character is closest to Venus but with a slightly cooler-yellow
  tint due to the metal-poor G8V illumination (less of the warm
  ochre that Venus shows under solar illumination).
- **Cloud-top bands.** Subtle dark and bright bands at low
  latitudes from Hadley-cell circulation; polar collar feature
  may be visible at the level of the largest atmospheric
  structures.
- **Day–night terminator.** Faintly visible because the thick
  atmosphere transports heat efficiently, but cloud-top
  illumination drops sharply at the terminator; the planet has
  a sharply defined illuminated crescent in optical view.
- **Nightside appearance.** Dark with faint cyan glow from
  starlight reflecting off cloud tops; the lower atmosphere's
  thermal IR emission would dominate at infrared wavelengths
  (not visible at typical KSP rendering). KSP nightside ambient
  ≈ 0.5% dayside.
- **Atmosphere haze.** A broad warm yellow-cream haze
  (`#d8c490`) extends 60–80 km above the planet limb; visually
  much thicker than Venus because the cloud-top is higher
  relative to the planet radius. The haze is the most visually
  distinctive feature of h from orbit.
- **No aurora.** No global magnetic field → no auroral oval.
- **Star in sky from the cloud tops.** τ Ceti subtends 1.74° at
  h's distance — 3.3× the Sun seen from Earth. The host is a
  bright pale-yellow disk under metal-poor G8V illumination.
  From the *surface*, the host is not directly visible — the
  sulfate cloud deck diffuses all incoming light into a
  featureless yellow-brown sky.
- **Sister planets in sky.** g (innermost) at ~0.04° in conjunction,
  rarely visible against the bright sky background even from
  orbit; f at ~0.04°. The cold debris disk at ≥ 6 AU is far
  outside h's orbit and appears as a faint amber-grey band on
  the night side.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Feng F. et al. 2017** — *Color difference makes a difference:
  four planet candidates around τ Ceti*, AJ 154, 135
  (`2017AJ....154..135F`, arXiv:1708.02051). Discovery + best
  constraint on h's orbit (P = 49.41 ± 0.08 d), mass
  (Msini = 1.83 ± 0.68 M⊕), eccentricity (0.23 — highest of the
  three). Anchors every orbital and physical Decisions row.
- **Feng F. et al. 2018** — *Detection limits on τ Ceti's planet
  system*, A&A 613, A76 (`2018A&A...613A..76F`,
  arXiv:1801.05415). Confirms 49.4-d signal stability;
  controversial flag in NEA reflects amplitude-to-noise concerns.
- **Vinson A. M. & Hansen B. M. S. 2017** — *Spin-orbit dynamics
  of habitable-zone planets*. 3:2 capture probability > 80% for
  e ≳ 0.10; anchors the cfg's 3:2 spin-orbit pick for h.
- **Venus bond albedo + cloud morphology (standard value)** —
  Venus-analog bond albedo 0.75 + cloud structure template adopted
  for h. No single primary citation pinned; standard Venus
  reference value. Confidence low.
- **Ivanov M. A. & Head J. W. 2011** — *Venus geologic units
  from Magellan*. Surface morphology template for the obscured
  basement (volcanic plains, tessera highlands, impact craters).

### Read (context / methodology, not directly decision-driving)

- **Kopparapu R. K. et al. 2014** — *Habitable zones*. Inner-
  edge runaway-greenhouse limit for a G8V is ~1.0 S⊕; h at
  7.74 S⊕ is firmly in the runaway regime.
- **Lawler S. M. et al. 2014** — τ Ceti debris disk
  inclination ~35° (Herschel); adopted by MacGregor et al. 2016
  (ALMA) and used here as h's orbital plane default.
- **Bolmont E. et al. 2020** — Tidal evolution framework;
  h's e = 0.23 at 0.243 AU gives estimated 0.05–0.5 W/m² tidal
  flux.
- **Makarov V. V. 2018** — Tidal locking timescales + 3:2
  capture; confirms h cannot be 1:1 locked over 7 Gyr at
  P = 49.41 d.
- **Way M. J. et al. 2025** — *Venus-analog GCM and atmospheric
  retention on quiet G-dwarf hosts*. General framework for
  Venus-analog atmospheric stability on a metal-poor low-XUV
  host; supports the 50-bar pick.

### Read (instrument / non-cfg-decisive)

- **Pavlenko Y. V. et al. 2012** — host star context (Teff,
  [Fe/H], log R'HK).
- **Schmitt J. H. M. M. et al. 1985** — host X-ray
  log L_X ≤ 26.5 (no XUV-driven escape).

### Not read — no arXiv preprint or low-priority (~14 papers)

- **Tuomi 2013 + 2014 erratum** — superseded by Feng 2017.
- **Various SETI / technosignature papers** — h is firmly
  uninhabitable, mostly irrelevant for biosignature catalog
  papers.
- **Venus-specific atmospheric chemistry reviews** — generally
  applicable but not h-specific.

## Open items for follow-up

- **Controversial flag (`pl_controv_flag = 1`).** Largest
  uncertainty of the three planets — Msini fractional error 0.37
  is highest. Monitor for retraction or refinement.
- **True mass.** Msini = 1.83 ± 0.68 M⊕; true mass depends on
  unknown i. Cfg adopts i ≈ 35° from disk → true mass ≈ 3.2 M⊕.
- **User-input discrepancy.** The user request described a τ Cet h
  at P = 4562 d / a = 5.0 AU. The DB authoritative h is at
  P = 49.41 d / a = 0.243 AU. The 4562-d signal is plausibly a
  Feng 2018 §3.4 long-period candidate or a later RV-reanalysis
  candidate not yet ingested. This Phase 3 synthesis treats the
  DB h (49.4 d). If the long-period candidate is later promoted to
  Phase 2 / Phase 3, a separate cfg variant or a re-named entry
  (e.g., "tau Cet i") may be needed.
- **Bare-rock cfg variant.** If the user prefers a Mercury-analog
  reading for h instead of Venus-analog (less likely given the
  much lower insolation than g), the bare-rock cfg variant from
  τ Cet g could be adapted. Not the canonical pick.
- **Sulfur volcanism cfg variant.** If the elevated tidal heating
  is more aggressive (upper bound 0.5 W/m²) the planet may have
  Io-like sulfur volcanism rather than Venus-like shield
  volcanism. Visually this would produce a more vibrantly yellow-
  orange cloud deck. Preserved as cfg variant.
- **Cloud-top wind speeds.** Venus has super-rotating cloud-top
  winds ~100 m/s. For h's slower (49-d × 2/3 spin) rotation, the
  super-rotation could be even more extreme, potentially producing
  visible cloud-band motion at gameplay timescales. Logged for
  future cfg refinement.
- **Lower-pressure variant (10 bar primordial Venus).** A thinner
  atmosphere at 10 bar would still produce runaway greenhouse but
  with a slightly cooler surface (~600 K) and possibly visible
  surface features through occasional cloud breaks. Less visually
  distinctive than the canonical 50-bar pick.

## Related

- [tau-cet](tau-cet.md) — host star Phase 3 (G8V metal-poor;
  quiet, old, debris-disk-bearing)
- [tau-cet-g](tau-cet-g.md) — innermost sibling, hot bare-rock
  Mercury-analog
- [tau-cet-f](tau-cet-f.md) — outermost sibling, snowball
- [methodology](../reference/methodology.md) — Decisions schema
- [rex-data-comparison](../reference/rex-data-comparison.md) — §6
  τ Ceti e curation gap
