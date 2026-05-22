<!-- Proxima Cen Phase 3 synthesis: cfg-ready stellar visual decisions -->
# Proxima Cen — Phase 3 Synthesis

Phase 3 stellar synthesis for the NearStars KSP mod (drafted 2026-05-22).

Proxima Cen is an M5.5 Ve fully convective dwarf at 1.302 pc — the
nearest known star to the Solar System and host to two confirmed
planets (b, d) plus a third candidate (c, contested). Mass
0.1221 ± 0.0022 M☉ (Suárez Mascareño et al. 2025 evolutionary
model, consistent with Mann et al. 2019 K-band calibration), radius
0.1410 ± 0.0070 R☉ (Boyajian et al. 2012 CHARA interferometry),
luminosity 0.00155 ± 0.00006 L☉ (Boyajian 2012 bolometric flux). At
this luminosity, the classical habitable zone falls at ~0.04–0.08 AU
and the orbital periods inside it are 5–20 days.

Proxima is gravitationally bound to Alpha Cen AB on a wide
hierarchical orbit (a ≈ 8700 AU, e ≈ 0.5, P ≈ 547 kyr; Kervella,
Thévenin & Lovis 2017), making the system a triple and Proxima a
shared-age companion (~5 Gyr; Joyce & Chaboyer 2018 for AB
applies). Despite this old age, Proxima is one of the most
magnetically active nearby M dwarfs — a property typical of fully
convective dwarfs with their dynamos in the saturated regime.

For NearStars the goal is a deep-red M5.5 Ve disk with prominent
flare activity, a high-contrast spot map, and a planetary system
that visualizes the "nearest neighbor" relationship to Alpha Cen AB.

**Scenario choice for NearStars: deep-red flare-active M dwarf
with starspot complexes covering up to 20% of disk surface and a
realistic flare schedule** — flares as occasional dramatic
brightening events for any orbiting planet, with rare superflares
(~10 yr cadence) as gameplay-relevant rad-storm events.

## Decisions

Kopernicus star cfg-ready values.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `mass_msun` | 0.1221 | high | Suárez Mascareño 2025; Mann 2019 K-band |
| `radius_rsun` | 0.1410 | high | Boyajian et al. 2012 CHARA interferometry |
| `teff_k` | 2904 | high | Passegger et al. 2019 CARMENES high-res |
| `luminosity_lsun` | 0.00155 | high | Boyajian et al. 2012 bolometric flux |
| `spectype` | M5.5 Ve | high | Bessell 1991, modern revision via Bidelman & MacConnell 1973 |
| `metallicity_fe_h_dex` | +0.05 | medium | Passegger et al. 2019 CARMENES; metallicity uncertainty large for M dwarfs |
| `age_gyr` | 4.85 ± 0.5 | medium | Kinematic (Kervella 2017 binding to AB) |
| `rotation_period_days` | 83.0 | high | Suárez Mascareño et al. 2016 long-baseline photometry |
| `obliquity_deg` | 0 | low | adopted |
| `surface_color_temp_k` | 2900 | high | weighted toward limb-darkened mean |
| `surface_tint_rgb_hex` | `#ff6028` | medium | blackbody 2900 K → CIE chromaticity, deep red-orange (visually ~580 nm dominant) |
| `corona_tint_rgb_hex` | `#ff8030` | low | brighter flare-loop tint |
| `limb_darkening_coeff_quadratic_a` | 0.55 | medium | strong M-dwarf limb darkening; Claret 2017 + TiO band opacity |
| `limb_darkening_coeff_quadratic_b` | 0.25 | medium | same |
| `granulation_cell_size_arcsec` | 0.4e-3 | medium | smaller than G/K dwarfs; M-dwarf grad-Brun convection |
| `convective_overshoot_pct` | 30 | medium | fully convective; no radiative core |
| `magnetic_cycle_period_yr` | 7 | medium | Wargelin et al. 2017 X-ray + Suárez Mascareño 2016 Hα cycle |
| `spot_coverage_max_pct` | 20 | medium | Reiners & Basri 2008 Bcoll constraint + Tregloan-Reed 2024 spectropolarimetric mapping |
| `spot_temperature_offset_k` | -500 | low | M-dwarf umbra T_spot/T_quiet ≈ 0.85; spot 2400 K vs photosphere 2900 K |
| `xray_log_lx_erg_s` | 27.2 | high | Wargelin et al. 2017 Chandra quiescent + flare-mean |
| `xray_cycle_factor` | 2.0 | medium | Wargelin 2017 cycle amplitude |
| `flare_rate_per_day_amplitude_log10` | -1.4 | high | Howard et al. 2018 + Vida et al. 2019 + MacGregor 2018 |
| `superflare_rate_per_yr_amplitude_log33_5_erg` | 0.1 | medium | Howard 2018 — 1 superflare/decade order |
| `wind_mass_loss_rate_msun_yr` | 1e-13 | medium | Wood et al. 2021 (revised) — 5–7× higher than Sun's |
| `wind_terminal_velocity_km_s` | 1500 | medium | Garraffo et al. 2017 MHD wind models |
| `chromosphere_h_alpha_ew_angstrom` | 4.5 | high | Newton et al. 2017 catalog mean |
| `chromosphere_log_rhk` | -5.55 | high | Suárez Mascareño et al. 2016 |
| `magnetic_field_strength_kg` | 0.6 | high | Reiners & Basri 2008 — Bcoll ≈ 600 G; Klein et al. 2021 ZDI |
| `apparent_diameter_arcsec_from_sol` | 0.0010 | high | derived |
| `apparent_magnitude_v_from_sol` | 11.29 | high | Gaia DR3 converted |
| `companion_alpha_ab_separation_au` | 8700 | medium | Kervella et al. 2017 |
| `interstellar_extinction_av_mag` | 0.0 | high | LIC, negligible reddening |

## Stellar disk synthesis

Proxima Cen is the closest example of an old fully convective M
dwarf. At 0.1410 R☉ its physical disk is 7× smaller than the Sun's,
but Boyajian et al. 2012's CHARA Array interferometry measured the
angular diameter at 1.044 ± 0.080 mas from Earth — still resolved by
present-day baseline interferometers (CHARA, VLTI). Among the
nearest stars this is the smallest physical and angular diameter.

**Color choice.** Teff = 2904 K (Passegger 2019, the recommended
high-resolution spectroscopic value; the existing raw teff = 3498 K
from the Suárez Mascareño 2025 entry is anomalous compared to most
M5.5Ve determinations and was reconciled in Phase 2 curation). At
2904 K the blackbody peaks near 1.0 μm (deep near-infrared), and
the visible spectrum is heavily depressed below 600 nm. The
disk-integrated chromaticity is dominated by long-wavelength
emission — RGB ≈ `#ff6028` (deep red-orange). Compared to a G2 V
star this is unambiguously red, far past the K1 V `#ffe9c4` warm
yellow of Alpha B. Visually this is the "Mars-like" red commonly
associated with M dwarfs.

**Limb darkening.** Strong M-dwarf limb darkening (a ≈ 0.55,
b ≈ 0.25) driven by TiO band opacity in the upper photosphere.
Edge brightness ~25% of disk-center, with appreciable additional
redward shift near the limb. The TiO bands also produce
characteristic broadband absorption that gives M dwarfs their
distinctive spectral shape.

**Granulation.** M dwarfs have smaller granulation cells than
G/K dwarfs (Brun & Browning 2017 fully-convective dynamo theory).
Cell scale ~0.4e-3 arcsec from Earth — unresolved by present
instruments but detectable in time-resolved photometric noise.
Convective velocities ~1.5 km/s in upper photosphere.

**Starspots.** Reiners & Basri 2008 detect Bcoll ≈ 600 G in
Stokes I + V; Klein et al. 2021 ZDI maps confirm a complex
multipolar geometry with dominant ~kG spot regions. Photometric
variability amplitude (~1.5% in V) at cycle max implies ~20% disk
surface covered by spots, consistent with Tregloan-Reed et al.
2024 spectropolarimetric mapping. Spot temperatures ~2400 K
(umbra) vs 2900 K (quiet photosphere) — a smaller relative
temperature difference than G/K dwarfs (500 K vs ~1500 K).

The spot pattern is dynamic — multiple complexes wax and wane on
~30–60 day timescales, with the dominant complex shifting
longitudes (consistent with strong differential rotation; equator-
to-pole period ratio ~1.4 from Klein 2021 ZDI).

**Flare rate.** Howard et al. 2018 used MOST + ASAS-SN long-baseline
data to derive flare cumulative distribution:
- M-class flares (~10³² erg): ~1 per day
- Larger flares (~10³³ erg): ~1 per week
- X-class superflares (~10³⁴ erg): ~1 per month
- Superflares (>10³⁵ erg): ~1 per decade (MacGregor et al. 2018
  detected one at amplitude 14,000× quiescent in March 2016)

The most violent superflares reach ~1000× quiescent brightness for
minutes. For an orbiting planet, this is biologically/electrically
catastrophic — radiation doses can spike to 10⁵× normal levels.

**No pulsations or oscillations detected.** Fully convective M
dwarfs are not expected to show p-mode oscillations in the same way
as G/K dwarfs. Suárez Mascareño 2025's RV residuals show only
activity and rotational modulation, no oscillation signal.

## Activity and variability synthesis

**Rotation period: 83.0 ± 0.8 days** (Suárez Mascareño et al. 2016
from long-baseline ASAS + HARPS photometry; confirmed by Benedict
et al. 1998 at 83.5 d). This is *slow* for an M dwarf — most M5.5
dwarfs at this age would rotate in 10–30 d. Proxima's slow rotation
is consistent with magnetic braking and old age, but combined with
the fully convective interior it does not predict the strong
activity observed. The explanation: fully convective dwarfs have
saturated dynamos where activity decouples from rotation rate
beyond the saturation threshold.

**Magnetic cycle: ~7 years** (Wargelin et al. 2017 Chandra X-ray
monitoring; Suárez Mascareño 2016 Hα). Notably shorter than the
Sun's 11-yr cycle despite the slower rotation. Cycle amplitude is
factor ~2 in X-rays — modest compared to the Sun's factor ~10.

**log R'_HK = -5.55** (Suárez Mascareño 2016). Despite the
"inactive" Ca II H&K diagnostic value, Proxima's H-α emission
(EW ~4.5 Å, Newton 2017) and X-ray luminosity (log L_X ≈ 27.2,
~30× higher than the Sun's log L_X = 25.6) indicate strong
chromospheric and coronal heating. The discrepancy is because
log R'_HK has a saturation floor that depresses fully convective
dwarf measurements — Hα is the more sensitive activity diagnostic
for M dwarfs.

**Magnetic field: ~600 G longitudinal mean** (Reiners & Basri 2008).
The Zeeman Doppler images (Klein et al. 2021) show complex
multipolar topology with dominant high-latitude spot complexes and
a weak dipolar component. The geometry varies over the cycle but
is never as ordered as solar.

**Coronal mass ejections.** Direct detection of CMEs from Proxima
is challenging at 1.3 pc. MacGregor et al. 2018 reported indirect
evidence from the March 2016 superflare (millimeter-wave continuum)
suggesting an associated CME. ALMA observations during the
post-flare epoch (Howard 2018, follow-ups) constrain CME mass and
velocity to be comparable to large solar CMEs but much more
frequent — perhaps multiple events per day during cycle maxima.

**Stellar wind.** Wood et al. 2021 revised Ly-α absorption analysis
gives mass loss ~1e-13 M☉/yr — ~5× higher than solar mass loss in
units of mass-per-area, but lower in absolute units. The wind
velocity at planet b's orbit (~30 R★) reaches 1500 km/s
supersonically, depositing ~30× more particle flux on b's
magnetosphere than the solar wind on Earth's.

**Auroral diagnostics on the star.** Proxima's own chromospheric
Hα emission acts as an "auroral signature" of magnetic activity.
During flare events the line core fills in rapidly. Lyman-α
emission from the chromosphere similarly correlates with activity.

## System geometry synthesis

Proxima sits ~15,000 AU from Alpha AB barycenter at present epoch,
projected angular separation ~2°. The Kervella, Thévenin & Lovis
2017 hierarchical-orbit analysis finds:
- Semi-major axis: 8700 AU
- Eccentricity: 0.5
- Period: 547,000 years
- Periastron passage: in ~280 kyr (next time Proxima approaches AB)

The orbital phase at present epoch is far from periastron — Proxima
will continue to drift outward for ~270 kyr before returning.

**From Proxima's frame**, Alpha AB appears as a brilliant single
star (separation ~12" at apastron, easily resolvable by even modest
optical aid, but appearing as one point to the unaided eye). Joint
visual magnitude V ≈ -7 — about 100× brighter than Venus from Earth,
casting visible shadows on the surface of any Proxima planet at
night. Color: cream-yellow (dominated by Alpha A's higher
luminosity).

**From a Proxima planet** (b at 0.0485 AU, d at 0.0288 AU), Proxima
itself dominates the sky:
- From b: Proxima subtends 1.5° (3× the Sun's apparent diameter
  from Earth). The disk is deeply red, with visible starspot
  complexes (spots are large relative to disk).
- From d: Proxima subtends 2.4° (5× the Sun's apparent diameter
  from Earth). Even more dramatic.

During flares, the disk brightness can spike 10–100× within
seconds, producing temporary "second daylight" lasting minutes.
For superflares (every ~10 yr), the brightness can spike 1000×,
producing 30 seconds of solar-equivalent flux delivered as UV-blue
shifted light across the deep-red ambient disk.

## Visual styling

- **Global appearance.** Deep red-orange disk (~`#ff6028` chromaticity).
  Clearly distinct from the warm-yellow Alpha B and the white-yellow
  Alpha A. The "red M dwarf" archetype.
- **Dayside illumination of orbiting bodies.** Color temperature
  ~2900 K — atmospheric scattering on Proxima b would produce a
  reddish-orange sky (not blue), with surface illumination biased
  to long wavelengths. The visible-light photosynthesis envelope
  available to any biota is severely constrained; deep-red and
  near-infrared photons dominate.
- **Disk brightness profile.** Strong limb darkening (edge ~25% of
  center); limb additionally reddened due to TiO band onset. The
  disk appears more uniformly red across all sectors than the
  Sun's golden-edged disk.
- **Spot visibility.** At cycle max, several large dark spot
  complexes covering up to 20% of disk surface, each ~10–20°
  angular diameter. Spots are ~500 K cooler (not as deep contrast
  as G/K dwarf spots) but the *fractional* area is far larger.
  KSP-equivalent: procedural dark patches that visibly move across
  the disk on the 83-day rotation; pattern reconfigures every
  ~50 days.
- **Flares.** Bright flare brightening events at irregular
  intervals. Brightness ratio: M-class ~5×, X-class ~50×, superflare
  ~1000× quiescent. Duration: minutes to hours. KSP-equivalent:
  occasional UV-blue flash events with localized brightening; rare
  full-disk superflare events.
- **Companion Alpha AB.** Brilliant point source at V = -7, color
  cream-yellow, slow drift across the sky over centuries.
  Cardinal feature: the brightest non-Proxima light source visible
  from any Proxima planet.
- **Spectral lines.** TiO bands dominate (5448, 6159, 6651 Å);
  H-α emission (cycle-variable); strong CaH bands in red; K I,
  Na D, Mg I b at solar-equivalent wavelengths but with strongly
  saturated cores. Near-IR is bright (peak emission), with H₂O
  and CO bands at λ > 1.4 μm.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2012ApJ...757..112B** Boyajian et al. 2012 — CHARA interferometric
  angular diameter (1.044 ± 0.080 mas) and bolometric luminosity
  (0.00155 ± 0.00006 L☉). Definitive radius/luminosity source.
- **2019A&A...627A.161P** Passegger et al. 2019 — CARMENES high-
  resolution near-IR spectroscopy. Teff = 2904 ± 51 K and [Fe/H] =
  +0.05 ± 0.16. Recommended over older Anglada-Escudé 2016 SED-fit
  value.
- **2016MNRAS.459.3565S** Suárez Mascareño et al. 2016 — Long-
  baseline ASAS+HARPS photometric monitoring. Definitive rotation
  period 83.0 ± 0.8 d, partial 7-yr Hα cycle, log R'_HK = -5.55.
- **1607.05636** Anglada-Escudé et al. 2016 — Proxima b discovery
  (P=11.2 d, Msini=1.27 M⊕). Visual-informative for cfg of host
  star insolation environment.
- **2204.09270** Diamond-Lowe et al. 2022 — Simultaneous X-ray + FUV
  monitoring of Proxima. EUV/UV flux levels relevant for any planet
  atmospheric chemistry around the host.
- **1907.12580** Vida et al. 2019 — TESS observations of Proxima
  flare activity. Quasi-periodic oscillations during flares;
  superflare characterization.
- **1608.06672** Davenport et al. 2016 — MOST satellite monitoring;
  baseline flare rate measurement.
- **MacGregor et al. 2018 (1803.07581)** — ALMA detection of
  massive March-2016 superflare (14,000× quiescent at mm
  wavelengths). Indirect CME evidence.
- **2102.06318** Howard et al. 2018 — ASAS-SN long baseline flare
  cumulative distribution. Provides superflare rate ~1/decade.
- **2021MNRAS.500.1844K** Klein et al. 2021 — Zeeman Doppler
  Imaging of Proxima at multiple epochs. Magnetic geometry +
  starspot mapping.
- **2017A&A...598L...7K** Kervella, Thévenin & Lovis 2017 — Proxima
  is gravitationally bound to AB; system geometry for cfg.

### Read (context / methodology, not decision-driving)

- **2410.01621** Garraffo et al. 2024 — Magnetized stellar winds
  for M dwarfs. Provides 1500 km/s wind velocity used in cfg.
- **1706.04617** Garraffo et al. 2017 — MHD simulations of
  star-planet magnetic interaction at TRAPPIST-1; analog framework
  for Proxima b/d.
- **2402.12253** Schreyer et al. 2024 — Water vapour transit
  ambiguities for habitable M-Earths. Context for atmospheric
  retrieval of any Proxima planet.
- **2312.01893** Lichtenberg et al. 2024 — Water content of HZ
  rocky exoplanets. Phase 3 b reads.
- **2306.03004** Chen et al. 2023 — Stratospheric ozone on
  synchronously rotating exoplanets. Context for tidally locked
  Proxima planets.
- **2506.19779** Schmidt 2025 — Young M dwarf mm spectrum. Reference
  for Proxima's chromospheric/coronal contribution.
- **2410.19108** Way et al. 2024 — Earth-like exoplanets in
  spin-orbit resonance. Climate dynamics relevant to Proxima b.
- **2209.12502** Braam et al. 2023 — Lightning chemistry on
  tidally locked Earth-like worlds. Relevant for atmosphere visual.
- **2211.11887** Cohen et al. 2022 — Cloud variability on
  aquaplanets.

### Read (instrument-only, not visual-informative)

- **2503.18538** PIAA + nuller coronagraph paper. Methodology only.
- **2602.08929** RedDots GJ 887 paper. Different system,
  methodology cross-reference.
- **2310.07827** APRIO+RV solution for other systems. Methodology.

### Not read — no arXiv preprint available (90 papers)

Includes pre-2008 references and conference proceedings. Key
not-read examples:

- "Pre-WISE" surveys of M dwarf populations. Skipped.
- IAU symposium proceedings summarizing rotation/activity. Skipped.
- "TRAPPIST monitoring" multi-target compendium summaries (Gillon
  earlier work). Skipped — TRAPPIST-1 phase 3 covers those.

**User action requested.** If newer ZDI campaigns publish post-2024
magnetic geometry updates for Proxima, the spot map and field
strength may need refinement. The MacGregor 2018 ALMA detection is
particularly important — any follow-up at higher cadence on
superflare rates would refine the gameplay-relevant superflare
schedule.

---

## Open items for follow-up

- Reconcile the lingering ~600 K teff discrepancy across literature
  (Cifuentes 2020 at 3000 K, Passegger 2019 at 2904 K, Suárez
  Mascareño 2025 raw entry at 3498 K). Phase 2 recommended
  Passegger as the most reliable; Phase 4 could revisit if a
  consensus measurement appears.
- Cycle period (~7 yr) is constrained by partial-cycle data; the
  Wargelin 2017 X-ray dataset spans 14 years (1.5 cycles). Tighter
  determination needs continued ALMA/Chandra monitoring through
  2030.
- Superflare rate (1/decade for ~10³⁵ erg events) is based on
  ~30 yr of optical monitoring (one event observed: MacGregor 2018).
  The Poisson uncertainty is large; the rate could be 0.3–3 per
  decade.
- Differential rotation amplitude (~1.4 equator-to-pole ratio,
  Klein 2021) needs additional ZDI epochs to confirm.
- The wind mass loss rate revision from Wood et al. (2021 vs 2005)
  is significant for any Proxima-b atmosphere escape models; Phase 3
  planet docs should reference the newer value.
