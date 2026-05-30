<!-- YZ Cet b Phase 3 synthesis: cfg-ready decisions and reasoning -->
# YZ Cet b — Phase 3 Synthesis

YZ Cet b is the innermost of three planets around the M4.5 V flare
star YZ Cet, on a 2.02087-day orbit at a = 0.0163 AU (Stock et al.
2020). It is a non-transiting radial-velocity planet, so its minimum
mass M sin i = 0.70 ± 0.09 M⊕ (Stock 2020) is measured but its radius
is **not** — the 0.913 R⊕ figure carried in the DB is a semi-empirical
mass-radius estimate (Stock 2020 / Astudillo-Defru 2017), not an
observation. With the host's L = 0.0022 L☉ the equilibrium temperature
is T_eq ≈ 471 K at zero albedo (computed here; T_eq = 278.3·L^0.25/√a),
making b a **warm rocky world** — hot, but far from a lava planet,
because the M dwarf is dim and b only receives ~8.2× Earth's
insolation despite its tiny orbit.

**Scenario choice for NearStars: a warm, tidally-locked rocky planet
with a thin-to-absent secondary atmosphere — and, uniquely, a
magnetosphere.** YZ Cet b is the driver of the system's confirmed
star-planet magnetic interaction: Trigilio et al. 2023 infer a
**planetary polar magnetic field of at least 0.4 G** from the auroral
radio emission, the first (indirect) measurement of an exoplanet
magnetic field, and Pineda & Villadsen 2023 detect the SPI radio bursts
that fold to b's orbit. The magnetosphere is the headline feature of
this planet; the surface and atmosphere sit at low confidence because
no transit, eclipse, or transmission spectrum exists.

## Decisions

Kopernicus / atmosphere cfg-ready values. `Confidence`: high =
directly measured or tightly constrained, medium = theoretical with
strong support, low = aesthetic choice within the allowed window.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 2.02 d orbit at 0.0163 AU; tidal locking time ≪ system age for a mid-M host |
| `obliquity_deg` | 0 | high | tidal damping at this orbit |
| `eccentricity` | 0.06 | medium | Stock et al. 2020 (Phase 2 recommended); poorly constrained (σ ≈ 0.06), consistent with circular |
| `argument_of_periastron_deg` | 197 | low | Stock et al. 2020 (weak constraint at low ecc) |
| `sidereal_period_days` | 2.02087 | high | Stock et al. 2020 (Phase 2 recommended); supersedes 1.96876 d Astudillo-Defru 2017 |
| `semi_major_axis_au` | 0.01634 | high | Stock et al. 2020 (Phase 2 recommended) |
| `mass_mearth` | ≥ 0.70 ± 0.09 (M sin i) | high | Stock et al. 2020 RV minimum mass (Phase 2 recommended); true mass higher by 1/sin i (no inclination from RV) |
| `radius_rearth` | ~0.913 (ESTIMATE) | low | NOT measured — no transit. Semi-empirical M-R estimate (Stock 2020); Pineda & Villadsen 2023 bracket 0.89–1.0 R⊕ for an Earth-like density |
| `surface_gravity_g_earth` | ~0.84 | low | derived = 0.70 / 0.913² from minimum mass + estimated radius; a lower bound (true mass higher) |
| `density_g_cc` | ~5 (assumed rocky) | low | No measured radius → no measured density; Earth-like rocky composition assumed |
| `insolation_s_earth` | 8.2 | high | derived = L / a² = 0.0022 / 0.01634² |
| `equilibrium_temp_k` (A=0) | 471 | high | derived = 278.3 · L^0.25 / √a (L = 0.0022 L☉, a = 0.01634 AU) |
| `equilibrium_temp_k` (A=0.3) | 431 | high | derived, Earth-analog Bond albedo |
| `bond_albedo` | 0.1 | low | Tie-break: assumed low for a warm rocky surface; no measurement |
| `atmosphere_present` | thin or absent | low | No transmission spectrum; warm rocky RV planet around an active flaring M dwarf — atmosphere retention is marginal. cfg renders a thin atmosphere as the visually interesting option |
| `atmosphere_surface_pressure_pa` | ~10000 (0.1 bar, tie-break) | low | No measurement; thin secondary atmosphere chosen as the more interesting option vs airless. Conservative airless variant preserved in Open items |
| `atmosphere_composition` | CO₂ / N₂ secondary (assumed) | low | No spectrum; outgassed rocky-planet composition assumed if any atmosphere survives |
| `atmosphere_tint_rgb_hex` | `#caa37a` (thin warm haze) | low | Tie-break: faint warm limb haze under 3100 K illumination if a thin atmosphere is present |
| `dayside_surface_temp_k` | ~520 | medium | substellar bare-rock peak above the 471 K global T_eq (A=0, low redistribution) |
| `nightside_surface_temp_k` | depends on atmosphere | low | airless → very cold nightside; thin atmosphere → partial redistribution |
| `surface_tint_rgb_hex_primary` | `#5a4438` (warm basaltic rock) | low | Tie-break: warm-toned iron-bearing basalt under red M-dwarf light; warmer than the airless-black inner TRAPPIST worlds because b is not a confirmed lava world |
| `surface_tint_rgb_hex_accent` | `#7a3a22` (oxidized iron patches) | low | Tie-break: photolytic / oxidized iron on an exposed warm rocky surface |
| `surface_morphology` | cratered rocky plains, tidally-locked | low | No data; generic warm rocky morphology under tidal lock |
| `planet_magnetic_field_polar_g` | ≥ 0.4 | medium | Trigilio et al. 2023 — lower limit from ARE power balance (R_MP ≥ 1.6–2.0 R_planet); first indirect exoplanet B-field measurement. Pineda & Villadsen 2023 Alfvén-Wing scenario needs ≳ a few G |
| `magnetosphere_present` | true | medium | Trigilio 2023 — the radiated SPI power requires a magnetopause R_MP ≥ 1.6 R_planet, i.e. b must have a real magnetosphere, not just an ionospheric obstacle |
| `magnetosphere_standoff_planet_radii` | 1.6–2.0 | medium | Trigilio et al. 2023 — R_MP ≥ 1.6–2.0 R_planet from the ARE cross-section requirement |
| `spi_flux_tube_to_star` | true | high | Pineda & Villadsen 2023; Trigilio 2023 — b sits in the sub-Alfvénic regime (a/R★ ≈ 21.9, R_Alf ≈ 100 R★) and drives a Jupiter-Io-style flux tube to the stellar poles |
| `aurora_present` | true (radio; optical if atmosphere) | medium | The confirmed SPI implies energetic particle precipitation; radio ARE is at the stellar pole, but b's own magnetosphere channels particles to its poles |
| `star_apparent_angular_diameter_deg` | 5.12 | high | derived = 2 · R★ / a · (180/π), R★ = 0.1571 R☉ |
| `stellar_illumination_color_temp_k` | 3100 | high | Cifuentes et al. 2020 host Teff |

## Surface synthesis

YZ Cet b has no transit, eclipse, or transmission measurement, so
everything about its surface is inferred from its minimum mass, orbit,
and host illumination. The radius (0.913 R⊕) is a semi-empirical
mass-radius estimate, not an observation; Pineda & Villadsen 2023, who
needed a radius for their SPI cross-section, bracketed it at 0.89–1.0 R⊕
assuming Earth-like density. The minimum mass M sin i = 0.70 M⊕
(Stock 2020) is a genuine lower bound; the true mass is higher by
1/sin i. For cfg purposes b is treated as a sub-Earth-to-Earth-mass
rocky planet.

The key thermal fact is that b is **warm, not molten**. The equilibrium
temperature at zero albedo is T_eq ≈ 471 K (computed here from
L = 0.0022 L☉ and a = 0.01634 AU), and the insolation is ~8.2× Earth's
— elevated, but the M dwarf is so dim that even at 0.0163 AU b is far
cooler than its tiny orbit alone would suggest. This is the same lesson
as the inner TRAPPIST worlds: a planet hugging a faint red dwarf is not
automatically a lava world. The substellar bare-rock peak temperature is
~520 K, comparable to Venus's surface, not to a magma ocean.

**Color choice.** Under the host's 3100 K red-orange illumination, b is
rendered as a warm-toned iron-bearing basaltic surface
(`#5a4438` primary) with oxidized iron-patch accents (`#7a3a22`). This
is deliberately warmer and lighter than the very-dark airless ultramafic
black of the JWST-confirmed lava-rock TRAPPIST-1 b (`#1a1612`), because
YZ Cet b has no JWST eclipse forcing a fresh-ultramafic, near-zero-albedo
surface — the interesting-first tie-break here favours a visibly
textured, iron-toned warm rock over a featureless black sphere. The
surface tint is low-confidence: with no eclipse or reflectance data, the
mineralogy is unconstrained and the choice is aesthetic within the
allowed window.

**Morphology.** Tidally locked (the 2.02-day orbit damps spin to
synchronous rotation well within the system age), so the substellar
point is fixed. Default texture is cratered rocky plains with a warm
dayside and a cold nightside; no resurfacing mechanism is confirmed, so
unlike TRAPPIST-1 b there are no forced fresh-lava features — though a
thin substellar warm-spot brightening is a permissible visual touch.

## Atmosphere synthesis

No transmission spectrum exists for YZ Cet b, so its atmosphere is
entirely a synthesis choice within the allowed window. Two physical
considerations bracket it: (1) at T_eq ≈ 471 K and ~8.2× Earth
insolation, a thin secondary atmosphere is thermally plausible but
under constant erosion; (2) the host is a moderately active flaring M
dwarf with a kG field and a strong stellar wind, and b orbits deep
inside the stellar magnetosphere in the sub-Alfvénic regime — an XUV
and particle environment hostile to atmosphere retention.

The decisive twist for b specifically is its **own magnetosphere**.
Trigilio 2023's SPI power balance requires b to present a magnetopause
of R_MP ≥ 1.6–2.0 R_planet to the stellar wind, which means b must carry
a real magnetic field (≥ 0.4 G at the pole) rather than just an
ionospheric obstacle. A magnetosphere of that strength would partially
shield a thin atmosphere from direct stellar-wind stripping — so the
"thin atmosphere" reading is more defensible for b than for an
unmagnetized close-in M-dwarf planet.

For NearStars the cfg adopts a **thin secondary atmosphere
(~0.1 bar, CO₂/N₂)** as the interesting-first tie-break, with the
conservative airless variant preserved in Open items. This is a
low-confidence aesthetic choice: the atmosphere gives b a faint warm
limb haze (`#caa37a`) and some day-night heat redistribution, which is
visually more distinctive than a bare airless sphere and is consistent
with — though not required by — the magnetosphere inference.

**Sky appearance.** If the thin atmosphere is present, the daytime sky
under the 3100 K star is a dim red-orange with weak Rayleigh blue near
the zenith. If b is airless instead, the sky is black and the star's
disk is sharp-edged. Either way the host star dominates the sky at
~5.1° angular diameter (about 10× the Sun from Earth), deep red-orange,
and the two outer siblings (c, d) appear as bright moving "stars."

## Rotation & spin synthesis

YZ Cet b is tidally locked. At a = 0.0163 AU around a 0.137 M☉ star the
tidal-locking timescale is far shorter than the system age (a few Gyr),
so the planet rotates synchronously with its 2.02087-day orbit. The
eccentricity (0.06 ± 0.06; Stock 2020) is poorly constrained and
consistent with circular; at e ≲ 0.06 the 1:1 spin-orbit resonance is
strongly favoured over 3:2 (Vinson 2017 / Makarov 2018: 3:2 is stable
only above e ≈ 0.01 with significant triaxiality, and the low-e RV
solution does not support that). Obliquity is damped to zero.

**KSP implementation note.** Rotation period = orbital period =
2.02087 days = 174 603 s. In Kopernicus the body's `rotationPeriod`
equals the orbital `period` in seconds.

**No seasons.** With obliquity = 0 and near-zero eccentricity, the
substellar point is fixed in the surface frame.

**SPI synodic geometry.** The radio aurora's visibility is governed by
the synodic period between b's orbit and the stellar rotation:
P_syn = [P_orb⁻¹ − P_rot⁻¹]⁻¹ ≈ 2.082 d (Pineda & Villadsen 2023, using
P_rot = 68.46 d). This is the cadence at which b returns to the same
position relative to the tilted stellar dipole, and it is why the SPI
bursts recur near — but not exactly at — b's orbital phase. For the cfg
the flux-tube footpoint animation is keyed to the 2.02-day orbit with a
slow 68-day modulation.

## Visual styling

Combining the surface, atmosphere, and magnetosphere decisions:

- **Global color palette.** A warm iron-toned rocky world (`#5a4438`
  primary, `#7a3a22` oxidized accent) under deep red-orange 3100 K
  light — lighter and warmer than the black airless lava-rock inner
  TRAPPIST worlds, reflecting b's lack of a confirmed molten surface.
- **Dayside.** Warm substellar hemisphere (~520 K peak) with textured
  rocky plains; a faint warm limb haze if the thin atmosphere is
  present.
- **Terminator band.** Sharp and high-contrast if airless; softened by
  thin-atmosphere scattering in the adopted scenario.
- **Nightside.** Cold; partially warmed by atmospheric redistribution in
  the thin-atmosphere reading, near-black if airless. Reflected light
  from siblings c and d at conjunction is the main nightside source.
- **Magnetosphere / aurora (the headline).** b is the only NearStars
  planet with an indirectly measured magnetic field (≥ 0.4 G; Trigilio
  2023). The cfg should render b's own magnetosphere and auroral ovals
  at its magnetic poles, plus the Jupiter-Io-style flux tube linking b
  to the stellar magnetic poles — the visible expression of the
  confirmed SPI. Auroral brightening keyed to the 2.02-day orbit.
- **Star in sky.** YZ Cet subtends ~5.1° in b's sky (≈ 10× the Sun from
  Earth), deep red-orange (3100 K → `#cf5630`), flooding the surface
  with ~8.2× Earth's insolation in infrared-rich light. Frequent flares
  from the eruptive-variable host punctuate the illumination.
- **Sister planets in sky.** c and d appear as bright moving points;
  near-coplanar compact system, so conjunctions are frequent.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2305.00809** Trigilio et al. 2023 — uGMRT 550–900 MHz confirmation
  of ARE from SPI at 4.37σ. Source for the **planet b magnetic field
  lower limit B ≥ 0.4 G** (R_MP ≥ 1.6–2.0 R_planet from the ARE power
  balance), the magnetosphere-present decision, and the sub-Alfvénic
  flux-tube geometry. The single most important paper for this planet.
- **2304.00031** Pineda & Villadsen 2023 — VLA 2–4 GHz coherent radio
  bursts folding to b's 2.02087 d orbit. Source for the SPI driver
  identification (b, not c/d), the radius bracket (0.89–1.0 R⊕ for
  Earth-like density), the synodic-period geometry, and the
  sub-Alfvénic regime that makes b the flux-tube driver.
- **2020A&A...636A.119S** Stock et al. 2020 — Phase 2 recommended
  source for b's orbit (P = 2.02087 d, a = 0.01634 AU, e = 0.06) and
  minimum mass (0.70 M⊕), plus the semi-empirical radius estimate
  (0.913 R⊕).

### Read (context / methodology, not decision-driving)

- **2017A&A...605L..11A** Astudillo-Defru et al. 2017 — discovery paper
  for b/c/d; earlier orbit/mass solution (P = 1.96876 d) retained as
  `recommended:false`. Context for the system architecture.
- Host stellar synthesis (`yz-cet.md`) — the Teff/L/R/M/activity/field
  values that set b's illumination and SPI environment.

### Read (instrument-only, not visual-informative)

- The radio-interferometry methodology of both SPI papers (CASA
  reduction, Stokes V dynamic spectra, hollow-cone ARE model) underpins
  the magnetic-field numbers but yields no additional visual field.

### Not read — no arXiv preprint or low-priority (~handful)

No JWST, transit, or transmission-spectroscopy paper exists for b (it
does not transit), so there is no eclipse/atmosphere literature to read.
The generic M-dwarf-wind and SPI-theory references (Saur 2013,
Lanza 2009, Turnpenney 2018, Vidotto 2019) cited inside the two SPI
papers are read for context but contribute no b-specific cfg number.

## Open items for follow-up

- **Cfg variant: airless b.** The adopted thin-atmosphere reading is an
  interesting-first tie-break; the conservative airless variant (0 Pa,
  black sky, sharp limb) is preserved here as an alternative cfg the
  writer can ship. The magnetosphere (≥ 0.4 G) is retained in both
  variants.
- **Radius is an estimate, not a measurement.** b does not transit; the
  0.913 R⊕ figure is semi-empirical. If a future astrometric or
  direct-imaging mass / radius appears, the surface gravity, density,
  and SPI cross-section should be updated.
- **Magnetic-field refinement.** The ≥ 0.4 G lower limit (Trigilio 2023)
  tightens if the full ARE high-frequency cutoff is measured or if the
  Alfvén-Wing scenario (which needs ≳ a few G; Pineda & Villadsen 2023)
  is favoured by future monitoring. Update the field strength and
  magnetopause standoff accordingly.
- **Atmosphere detection.** Only a future emission/phase-curve campaign
  (challenging for a non-transiting planet) could confirm or exclude
  the thin atmosphere; until then the pressure stays low-confidence.

## Related

- [yz-cet](yz-cet.md) — host star; the M4.5 V flare star whose kG field anchors the SPI to this planet
- [yz-cet-c](yz-cet-c.md) — next planet out (middle of the compact system)
- [yz-cet-d](yz-cet-d.md) — outermost planet
- [trappist-1-b](trappist-1-b.md) — comparison innermost M-dwarf rocky planet, but JWST-confirmed airless lava-rock; contrast with YZ Cet b's unmeasured surface and confirmed magnetosphere
- [methodology](../reference/methodology.md) — schema for the Decisions table and confidence tags
