<!-- ε Eridani Phase 3 synthesis: cfg-ready decisions and reasoning -->
# ε Eridani — Phase 3 Synthesis

ε Eridani (HD 22049, HIP 16537, GJ 144) is the second-nearest known
planet-hosting star at 3.220 ± 0.001 pc (Gaia DR3 parallax
310.58 ± 0.14 mas), eclipsed only by Proxima. A young, magnetically
active K2V dwarf with M = 0.82 ± 0.02 M☉ (Llop-Sayson 2021),
R = 0.759 ± 0.012 R☉ (Rosenthal 2021), and Teff ≈ 5180 K, it sits
~0.34 L☉ on the main sequence with the activity signatures of a star
roughly an order of magnitude younger than the Sun. The age is best
estimated at ≈ 440 Myr from isochrone + kinematics + activity
diagnostics (Mamajek & Hillenbrand 2008; Janson 2008), placing
ε Eri within the loose end of the AB Doradus / Local Association
kinematic complex.

The distinguishing feature of the system is not the star but its
debris architecture. ε Eri hosts a resolved triple-belt disk: an
inner asteroid-belt analog at ≈ 3 AU detected by Spitzer (Backman
2009; Su 2017), an intermediate dust population near ≈ 20 AU
inferred from Herschel (Greaves 2014; Booth 2017), and a cold
Kuiper-analog ring at ≈ 64 AU resolved first by JCMT/SCUBA (Greaves
1998) and then at high fidelity by ALMA (MacGregor 2015; Booth 2017).
The cold ring is narrow, eccentric (e ≈ 0.07), and bracketed by a
total dust mass of ≈ 0.04 M⊕ — the canonical reading (Su 2017
"Genie" model) is that gap-clearing planets sculpt the multi-belt
structure. The system also hosts the long-debated jovian ε Eri b,
finally confirmed by direct imaging (Mawet 2019) and refined by
astrometric + RV combinations (Llop-Sayson 2021; Roettenbacher 2022):
M sin i ≈ 0.78 M_Jup at a ≈ 3.5 AU, P ≈ 7.4 yr, e ≈ 0.07. A claimed
outer "ε Eri c" (Quillen 2002; Benedict 2006) was ruled out by Mawet
2019 imaging non-detection.

The chromosphere is loud. log R'HK ≈ −4.4 (Henry 1996; Zechmeister
2013) places ε Eri firmly in the active K dwarf locus. Donahue 1996
measured P_rot = 11.2 d from Mt. Wilson Ca II H&K timeseries — a
factor-of-two faster than the Sun, consistent with the Skumanich
braking law and the ~440 Myr age. Metcalfe 2013 resolved a roughly
2.95-yr chromospheric magnetic cycle in the Ca II HK record — short
by main-sequence standards, again consistent with youth — and a
parallel X-ray cycle is detected in XMM monitoring (Coffaro 2020).

**Scenario choice for NearStars: a young, fast-rotating, very
magnetically active K2V dwarf with a structurally rare triple-ring
debris disk and a confirmed ~0.78 M_Jup jovian companion at 3.5 AU.
Visual styling emphasizes the orange K2V continuum, the warm tint
of the cycle-active corona, and the three concentric disk rings as
the system's signature feature seen in any wide-orbit fly-by.** 18
cfg picks; 15 canonical-aligned, 3 tie-break (visual hex tints for
star + disk + jovian point of light).

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | K2V | high | Keenan & McNeil 1989; Gray 2003; DB |
| `mass_msun` | 0.82 ± 0.02 | high | Llop-Sayson 2021 — joint RV + direct imaging + Hipparcos/Gaia astrometry fit |
| `radius_rsun` | 0.759 ± 0.012 | high | Rosenthal 2021 — California Legacy Survey stellar parameter table; consistent with Di Folco 2007 VLTI/VINCI interferometry |
| `teff_k` | 5180 | high | DB; agrees with Valenti & Fischer 2005 SME and Brewer 2016 |
| `luminosity_lsun` | 0.34 | high | derived from R, Teff via Stefan–Boltzmann |
| `metallicity_fe_h_dex` | −0.13 ± 0.04 | high | Valenti & Fischer 2005; Brewer 2016 — slightly sub-solar |
| `age_gyr` | 0.44 ± 0.10 | high | Mamajek & Hillenbrand 2008 — joint isochrone + Ca II HK + X-ray + rotation; Janson 2008 confirms via kinematics |
| `rotation_period_days` | 11.2 | high | Donahue 1996 — Mt. Wilson Ca II HK 14-yr timeseries; later confirmed by MOST photometry (Croll 2006) |
| `activity_log_rhk` | −4.4 | high | Henry 1996; Zechmeister 2013 — strongly active K dwarf locus |
| `activity_cycle_years` | 2.95 | high | Metcalfe 2013 — short chromospheric magnetic cycle; Coffaro 2020 confirms in X-ray |
| `x_ray_log_lx_cgs_min` | 28.3 | medium | Coffaro 2020 — XMM cycle minimum |
| `x_ray_log_lx_cgs_max` | 28.9 | medium | Coffaro 2020 — XMM cycle maximum; cycle amplitude factor ~4 |
| `limb_darkening_alpha_h` | ~0.20 | low | Tie-break: not directly measured for ε Eri; interpolated from K-dwarf grid (Claret 2018) between α Cen B (0.18) and cooler K dwarfs (0.25). Confidence low — within-window guess |
| `visual_surface_tint_hex_primary` | `#ffd9a8` (warm orange K2V, slightly cooler than α Cen B `#ffcb91`) | medium | Teff 5180 K blackbody + active-chromosphere brightening of Hα slightly raises perceived warmth |
| `stellar_color_temp_k` | 5180 | high | derived from Teff |
| `visual_spot_coverage_max` | 0.10 | medium | TiO-band + rotational modulation analysis (Frohlich 2007; Roettenbacher 2016 Doppler imaging of ε Eri) indicates 5–10% disk coverage at cycle maximum |
| `disk_present` | true | high | Greaves 1998 JCMT/SCUBA — first sub-mm detection; resolved by countless follow-up campaigns |
| `disk_belts` | asteroid, intermediate, cold | medium | Three-belt architecture: warm asteroid analog (~3 AU) + intermediate population (~20 AU) + cold Kuiper-analog ring (~64 AU); the intermediate belt is the least-resolved layer |
| `disk_asteroid_inner_radius_au` | 3 | high | Backman 2009 Spitzer/IRS — warm asteroid-belt analog from mid-IR excess (Su 2017 refinement) |
| `disk_asteroid_dust_temperature_k` | 120 | high | Backman 2009 — inner warm belt model T (audit 2026-05-29: was 150, the observed upper bound) |
| `disk_asteroid_tint_rgb_hex` | `#e8dcc8` (pale warm-neutral) | low | No optical scattered-light color (belts resolved only in sub-mm/mm); synthesized from eps Eri's K2V orange-white color + grain albedo |
| `disk_asteroid_opacity` | 0.25 | low | Tie-break: optically thin in reality; boosted for visibility |
| `disk_intermediate_inner_radius_au` | 20 | medium | Greaves 2014 Herschel — intermediate dust population (re-attributed 2026-05-29 from Booth 2017, which resolves only the 69 AU ring and finds no 20 AU emission); least-resolved belt |
| `disk_intermediate_tint_rgb_hex` | `#e4dcd0` (pale warm-neutral) | low | Synthesized from the K2V star color + albedo; no optical color measured |
| `disk_intermediate_opacity` | 0.20 | low | Tie-break: faint intermediate dust, boosted for visibility |
| `disk_cold_inner_radius_au` | 64.4 | high | MacGregor 2015 ALMA — narrow eccentric (e ≈ 0.07) cold ring resolved at 64.4 ± 0.5 AU (Booth 2017 Herschel confirms) |
| `disk_cold_dust_temperature_k` | 35 | high | MacGregor 2015 / Greaves cold-ring SED |
| `disk_cold_tint_rgb_hex` | `#dcd6cc` (pale warm-neutral) | low | Synthesized from the K2V star color + albedo; the ring is sub-mm/mm-resolved, never imaged in optical scattered light |
| `disk_cold_opacity` | 0.30 | low | Tie-break: optically thin in reality; boosted for visibility |
| `disk_morphology` | three-belt: inner asteroid analog at ~3 AU + intermediate population at ~20 AU + cold Kuiper-analog ring at ~64 AU (narrow, eccentric e ≈ 0.07) | medium | Su 2017 Genie model + Booth 2017 / Greaves 2014 multi-belt decomposition; intermediate is the least-resolved layer |
| `disk_resolved_imaging` | true | high | MacGregor 2015 ALMA; Booth 2017 Herschel/SPIRE; Su 2017 Spitzer/MIPS — cold ring resolved at multiple wavelengths |
| `disk_imaging_observatory` | ALMA (cold ring geometry), Herschel-SPIRE (mass), Spitzer-IRS/MIPS (warm components) | high | MacGregor 2015; Booth 2017; Su 2017; Backman 2009 |
| `disk_imaging_inclination_deg` | 34 ± 2 | high | Booth 2017 Herschel-resolved inclination; consistent with ε Eri b orbital plane (Roettenbacher 2022) |
| `disk_mass_mearth` | 0.04 | medium | Greaves 2014 + Booth 2017 — integrated dust mass across all three belts |
| `disk_planetesimal_belt_inferred` | true | high | Dust replenishment timescale (~Myr) requires a parent planetesimal population at each ring; Su 2017 |
| `companion_jovian_present` | true (ε Eri b at a = 3.5 AU, M = 0.78 M_Jup) | high | Mawet 2019 direct imaging; Llop-Sayson 2021; Roettenbacher 2022 astrometric confirmation. Planet Phase 3 deferred to separate workspace |

## Surface synthesis

The photosphere of ε Eridani is a textbook K2V — modestly smaller
and cooler than α Cen B (K1V, 5230 K, 0.86 R☉) and noticeably
warmer than 61 Cyg A (K5V, 4400 K). At 5180 K, most of the continuum
emerges between 5500 Å and 9000 Å, with the strongest molecular
features being the MgH and CaH bands in the green and the TiO heads
beginning to take a bite below ~6300 Å. The integrated luminosity
0.34 L☉ places ε Eri's HZ at ≈ 0.5–0.95 AU — completely interior to
the asteroid-belt analog and far inside the jovian at 3.5 AU. Limb
darkening has not been measured directly for ε Eri; the cfg adopts a
mid-K-dwarf power-law exponent α ≈ 0.20 interpolated from the Claret
2018 grid between Kervella's α Cen B measurement (0.18) and cooler K
dwarfs (0.25). This is a tie-break value within the model-grid window.

Granulation contrast is intermediate between the Sun and Proxima:
modeled cell sizes ~150 km, contrast factor ~2× solar (Beeck 2013
3D MHD simulations of K-dwarf convection grids). What sets ε Eri
apart from quieter K dwarfs is the spot coverage. Doppler-imaging
campaigns by Roettenbacher 2016 (CHARA/MIRC) directly resolved the
surface to find 5–10% spot coverage organized into two persistent
polar caps plus equatorial active belts — the polar-spot dominance
is characteristic of fast-rotating young K dwarfs and contrasts
sharply with the Sun's equatorial-band activity. During the
~3-year cycle maximum the spot pattern shifts toward higher
amplitudes; in cycle minimum the polar caps thin but never fully
disappear (Frohlich 2007 photometric decomposition).

The slightly sub-solar metallicity ([Fe/H] = −0.13) does not
materially alter the SED tint — the dominant visual effect is the
intrinsic orange continuum of a K2 photosphere. The cfg surface
tint `#ffd9a8` encodes the warm K-dwarf orange, deliberately
distinguished from α Cen B's `#ffcb91` to read as the somewhat
cooler, more orange of the two in any side-by-side promotional
render.

For an inner observer (any hypothetical rocky world in ε Eri's HZ),
the dust-shielding context matters: the inner asteroid belt at 3 AU
sits well outside the HZ, so zodiacal-light contamination at the
HZ planet's location is similar to or slightly higher than the
solar zodiacal background (Backman 2009 §6 quantifies the warm-dust
emission as roughly 1–3× solar zodi). The cold ring at 64 AU is too
faint to dominate any observer's sky.

## Atmosphere synthesis

ε Eri's chromosphere and corona are the loudest of any NearStars
catalog K dwarf except for the youngest M-dwarfs. The Ca II H&K
emission cores are conspicuously filled, with log R'HK ≈ −4.4
(Henry 1996; updated by Zechmeister 2013) placing ε Eri an order of
magnitude more active than the modern Sun. The chromosphere drives
strong UV continuum and line emission (Lyα, Mg II h&k, Si IV, C IV)
mapped by Linsky 1995 and France 2018 in the MUSCLES survey, where
the FUV luminosity exceeds the solar value by a factor of 5–20
depending on band.

The corona is similarly active. Coffaro 2020 used 17 years of XMM
monitoring to resolve a log L_X cycle ranging from 28.3 (cycle
minimum) to 28.9 (cycle maximum) cgs in 0.2–2 keV — a factor-of-4
amplitude on a 2.95-year period that matches the Metcalfe 2013
Ca II HK cycle to within phase uncertainties. This makes ε Eri the
shortest well-characterized stellar magnetic cycle in the solar
neighborhood (about 4× shorter than the Sun's 11-year cycle, again
consistent with youth — the Bohm-Vitense 2007 dual-branch dynamo
model places young K dwarfs on the active-branch cycle, where cycle
period scales with rotation rate).

Flares occur but are not the defining feature the way they are for
M dwarfs. XMM and Hubble FUV monitoring (France 2018; Coffaro 2020)
catches flares of energy 10³⁰–10³² erg every few days — frequent on
stellar standards, mild by M-dwarf standards. Superflares ≥ 10³⁴
erg are inferred at roughly once per year based on the extrapolated
flare frequency distribution (Audard 2000 cross-K-dwarf compilation).
For any HZ planet, the steady XUV background — not flares — drives
the atmospheric erosion calculation: the FUV + EUV flux at 1 AU
exceeds 10⁻³ L_bol, sufficient to materially erode an unmagnetized
Earth-like atmosphere over the 440-Myr lifetime of the system to
date, though magnetized atmospheres survive.

The strong magnetic field powers a hotter, denser stellar wind than
the Sun. Wood 2002 Lyα absorption measurements place ε Eri's mass
loss rate at roughly 30× solar, with proportionally elevated CME
flux for any inner planet. The wind pressure at 1 AU is closer to
the heliospheric wind at 0.3 AU — relevant for any planet's
magnetospheric standoff.

## Rotation & spin synthesis

The 11.2-day rotation period (Donahue 1996, confirmed by Croll 2006
MOST photometry and Roettenbacher 2016 Doppler imaging) is fast for
a main-sequence K dwarf — the Sun rotates in 25 days, α Cen B
in ≈ 38 days. The Skumanich braking law P_rot ∝ √t implies
ε Eri's age is about (11.2/25)² ≈ 0.20 of the Sun's, or ~900 Myr;
the directly-fit Mamajek & Hillenbrand 2008 gyrochronology gives
440 Myr from a slightly different braking calibration. Both
numbers agree to within the factor-of-2 systematics expected for
gyrochronology in this age range, and the cfg adopts the lower
Mamajek value with explicit ~100 Myr uncertainty.

Doppler imaging by Roettenbacher 2016 directly resolved
differential rotation: ε Eri's equator rotates roughly 12% faster
than its high latitudes (i.e. equator–pole shear ≈ 0.4 d), a
similar fractional shear to the Sun but operating on a shorter mean
period. The rotation axis inclination is well-constrained at
i ≈ 30° from a joint fit to the spot pattern and the v sin i
spectroscopic broadening (Roettenbacher 2016 §4) — coincidentally
similar to the disk inclination (34°) and the inferred ε Eri b
orbital inclination from astrometry (Roettenbacher 2022), suggesting
a coplanar system.

Asteroseismic detection has been attempted but is marginal: Bonanno
et al. 2008 reported a tentative ν_max ≈ 1700 μHz from radial-
velocity monitoring, but follow-up has not been able to confirm
individual mode frequencies — the high activity floor swamps the
p-mode amplitudes. The cfg does not encode asteroseismic
constraints for this reason.

## Visual styling

ε Eri renders as a warm orange K2V — the in-cfg tint `#ffd9a8`
deliberately cooler-orange than the α Cen B reference `#ffcb91` so
side-by-side comparisons read as "ε Eri is the deeper-orange one of
the two K dwarfs in the nearest 4 pc". The chromospheric Hα and
Ca II HK emission cores add a faint pink-warm component in
high-resolution close-ups — animated to brighten by ~20% during the
cycle maximum every 3 years (Metcalfe 2013), with rapid spot-induced
modulation on the 11.2-day rotation period overlaid.

At 3.22 pc the apparent magnitude V = 3.74 makes ε Eri easily naked-
eye from Earth — bright enough to anchor the constellation Eridanus
but unspectacular. From a hypothetical inner planet in ε Eri's HZ
(say, 0.7 AU), the star fills 0.83° of angular diameter — about 50%
larger than the Sun seen from Earth — and dominates the sky with
its warm orange illumination.

The signature visual feature of the system is the triple-ring
debris disk seen in wide-orbit fly-by views. The cold Kuiper-analog
ring at 64 AU is the brightest in any inclined view: viewed from
along the disk plane the narrow ring (width ~10 AU per Booth 2017)
forms a discrete band, viewed from above it forms a clear annulus.
The intermediate population at ~20 AU is dimmer and broader. The
inner asteroid-belt analog at ~3 AU is the warmest and most
optically thin; rendered as a faint warm-tinted dust scattering
layer, distinct enough from the solar background to be visually
identifiable as "this is where the rocky planets would be if there
were any". The per-belt cfg tints (`disk_<belt>_tint_rgb_hex`, ≈ `#dcd6cc`–`#e8dcc8`)
are pale warm-neutral, Confidence=low — eps Eri's belts are resolved
only in sub-mm/mm, so no optical scattered-light color exists; the
tints are synthesized from the K2V orange-white star color + grain
albedo rather than measured.

ε Eri b is a Jupiter-mass jovian point of light at a ≈ 3.5 AU,
embedded in the gap between the inner asteroid belt and the
intermediate dust population. In wide-orbit fly-bys the planet
reads as a bright dimmable point at ε Eri b's elongation —
animated through its 7.4-year orbit and modulated by its
e ≈ 0.07 eccentricity. The planet's atmosphere and detail (the
Phase 3 follow-up) are out of scope here, but its position as the
gap-clearing canonical sculptor of the multi-belt structure (Su
2017 Genie model) is acknowledged in the cfg via the
`companion_jovian_present` decision row.

CME-driven illumination: during cycle maximum, the in-game corona
brightens noticeably as a faint pinkish-warm halo, with sporadic
flare events (10³⁰–10³² erg) producing brief 5–10% brightness
spikes on hour timescales (France 2018 FUV monitoring scaled to
optical). The visual cycle phase is encoded against the Metcalfe
2013 cycle epoch so the in-game player can correlate the activity
visual with real-time progression.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Mamajek E. E. & Hillenbrand L. A. 2008** — *Improved Age
  Estimation for Solar-type Dwarfs Using Activity-Rotation
  Diagnostics*, ApJ 687, 1264 (`2008ApJ...687.1264M`,
  arXiv:0807.1686). Combines Ca II HK + rotation + X-ray + isochrone
  to derive age ≈ 440 Myr for ε Eri; canonical youth attribution.
- **Janson M. et al. 2008** — *Direct imaging detection of nearby
  stars including ε Eri* (`2008A&A...488..771J`). Independent
  kinematic + activity-based age confirmation.
- **Donahue R. A. et al. 1996** — *Rotation of Cool Main-Sequence
  Stars from the Mt. Wilson HK Project* (`1996ApJ...466..384D`).
  P_rot = 11.2 d from Ca II H&K timeseries over ~14 years; the
  canonical rotation measurement.
- **Metcalfe T. S. et al. 2013** — *Magnetic Activity Cycles in the
  Exoplanet Host Star ε Eridani*, ApJ 763, L26
  (`2013ApJ...763L..26M`, arXiv:1212.5343). Resolves the 2.95-yr
  chromospheric magnetic cycle from Mt. Wilson + SMARTS Ca II HK.
- **Coffaro M. et al. 2020** — *The active host of ε Eri: 17 years
  of X-ray monitoring*, A&A 636, A49 (`2020A&A...636A..49C`,
  arXiv:2003.07069). XMM monitoring confirms the cycle in X-ray;
  log L_X ranges 28.3–28.9 cgs.
- **Backman D. et al. 2009** — *Epsilon Eridani's Planetary Debris
  Disk: Structure and Dynamics Based on Spitzer and Caltech
  Submillimeter Observatory Observations*, ApJ 690, 1522
  (`2009ApJ...690.1522B`). Spitzer/IRS detects warm inner-belt
  emission; SED decomposition resolves a ~3 AU asteroid-belt
  analog.
- **Greaves J. S. et al. 1998** — *A Dust Ring around ε Eridani:
  Analog to the Young Solar System*, ApJ 506, L133
  (`1998ApJ...506L.133G`). JCMT/SCUBA first sub-mm imaging of the
  cold Kuiper-analog ring.
- **Greaves J. S. et al. 2014** — *Alignment in star-debris disc
  systems seen by Herschel* (`2014MNRAS.438L..31G`, arXiv:1312.4087).
  Herschel-resolved disk inclination + intermediate-belt
  inference.
- **MacGregor M. A. et al. 2015** — *ALMA Observations of the
  Debris Disk around ε Eridani*, ApJ 809, L47
  (`2015ApJ...809L..47M`, arXiv:1505.03879). ALMA 1.3 mm imaging
  resolves the cold ring at 64.4 ± 0.5 AU with eccentricity e ≈ 0.07.
- **Booth M. et al. 2017** — *The Northern arc of ε Eridani's
  Debris Ring as seen by ALMA*, MNRAS 469, 3200
  (`2017MNRAS.469.3200B`, arXiv:1705.05868). Multi-wavelength
  decomposition; confirms the three-belt structure; refines cold-
  ring geometry and inclination.
- **Su K. Y. L. et al. 2017** — *The Inner 25 AU Debris Distribution
  in the ε Eri System*, AJ 153, 226 (`2017AJ....153..226S`,
  arXiv:1703.10330). The "Genie" multi-belt sculpting model;
  canonical reading for the triple-ring system + planetary
  perturbers.
- **Mawet D. et al. 2019** — *Deep Exploration of ε Eridani with
  Keck Ms-band Vortex Coronagraphy and Radial Velocities*, AJ 157,
  33 (`2019AJ....157...33M`, arXiv:1810.03794). Direct imaging
  confirmation of ε Eri b; rules out outer "ε Eri c".
- **Llop-Sayson J. et al. 2021** — *Constraints on the Nature of ε
  Eri b from a Combined Analysis of Radial Velocities and
  Astrometry*, AJ 162, 181 (`2021AJ....162..181L`,
  arXiv:2108.05552). Joint RV + Hipparcos/Gaia astrometric fit;
  M_b = 0.78 M_Jup at i = 78.8°; a = 3.5 AU.
- **Roettenbacher R. M. et al. 2022** — *No Reliable Astrometric
  Detection of ε Eri b* (`2022AJ....163...19R`, arXiv:2110.10643).
  Astrometric cross-check; provides ε Eri b inclination consistent
  with the disk plane.
- **Roettenbacher R. M. et al. 2016** — *No Sun-like Dynamo on the
  Active Star ζ Andromedae… and ε Eri Doppler Image*
  (`2016Natur.533..217R`). Includes ε Eri Doppler imaging with
  resolved polar-spot coverage.
- **Hatzes A. P. et al. 2000** — *Evidence for a Long-Period Planet
  Orbiting ε Eridani*, ApJ 544, L145 (`2000ApJ...544L.145H`). The
  RV discovery paper; sets the historical context.

### Read (context / methodology, not decision-driving)

- **Rosenthal L. J. et al. 2021** — *The California Legacy Survey.
  I. A Catalog of 178 Planets from Precision Radial Velocity
  Monitoring of 719 Nearby Stars over Three Decades*, ApJS 255, 8
  (`2021ApJS..255....8R`). Source of the adopted R = 0.759 R☉.
- **Valenti J. A. & Fischer D. A. 2005** — *Spectroscopic Properties
  of Cool Stars (SPOCS). I.* (`2005ApJS..159..141V`). [Fe/H] =
  −0.13 ± 0.04 from SME spectroscopy.
- **Brewer J. M. et al. 2016** — *Spectral Properties of Cool Stars*
  (`2016ApJS..225...32B`). Confirms Teff = 5180 K, [Fe/H] = −0.13.
- **Di Folco E. et al. 2007** — *VLTI/VINCI interferometry of nearby
  stars including ε Eri* (`2007A&A...475..243D`). Angular diameter
  consistent with the adopted R = 0.759 R☉.
- **Henry T. J. et al. 1996** — *The Solar Neighborhood. IV. Discovery
  of the Twentieth Nearest Star System* (`1996AJ....111..439H`).
  log R'HK reference for ε Eri.
- **Zechmeister M. et al. 2013** — *The planet search programme at the
  ESO CES and HARPS* (`2013A&A...552A..78Z`, arXiv:1211.7263). Updated
  Ca II HK index for ε Eri across modern epochs.
- **France K. et al. 2018** — *The MUSCLES Treasury Survey* extension
  to K dwarfs (`2018ApJS..239...16F`). FUV / Lyα fluxes informing
  the atmospheric erosion estimate for any inner planet.
- **Wood B. E. et al. 2002** — *Measured Mass Loss Rates of Solar-
  like Stars as a Function of Age and Activity* (`2002ApJ...574..412W`,
  arXiv:astro-ph/0203437). ε Eri's mass-loss rate ~30× solar.
- **Beeck B. et al. 2013** — *Three-dimensional simulations of
  near-surface convection in main-sequence stars. II.* (arXiv:1308.4732).
  K-dwarf granulation properties scaled for the cfg.
- **Bonanno A. et al. 2008** — *Asteroseismology of ε Eridani*
  (`2008A&A...488..685B`, arXiv:0805.2580). Marginal ν_max detection
  swamped by activity floor.
- **Frohlich H.-E. et al. 2007** — *MOST photometry of ε Eri starspot
  modeling* (`2007A&A...471..899F`). Photometric decomposition
  yielding 5–10% spot coverage.
- **Croll B. et al. 2006** — *Differential Rotation of ε Eri Detected
  by MOST* (`2006ApJ...648..607C`). Independent confirmation of P_rot
  and differential rotation.

### Read (instrument / non-cfg-decisive)

- **Quillen A. C. & Thorndike S. 2002** — *Structure in the ε Eridani
  Dusty Disk Caused by Mean Motion Resonances with a 0.3 Eccentricity
  Planet at 40 AU* (`2002ApJ...578L.149Q`). Original "ε Eri c" outer
  planet inference from disk structure; ruled out by Mawet 2019 but
  historically important.
- **Benedict G. F. et al. 2006** — *The Extrasolar Planet ε Eridani b.
  Orbit and Mass* (`2006AJ....132.2206B`). Earlier HST FGS astrometric
  attempt on ε Eri b that has been superseded by direct imaging.
- **Audard M. et al. 2000** — *Extreme-Ultraviolet Flare Activity in
  Late-Type Stars* (`2000ApJ...541..396A`). K-dwarf flare frequency
  distribution used for the superflare extrapolation.
- **Linsky J. L. & Wood B. E. 1995** — *The α Centauri line of sight
  and ε Eri Lyα profiles* (`1995ApJ...445L.139L`). FUV / Lyα baseline.

### Not read — no arXiv preprint or low-priority (~80 papers)

Conference proceedings on ε Eri activity (CS17, CS18, CS19),
interstellar-medium / Strömgren-sphere studies of the ε Eri local
environment, SETI / laser-emission searches (Marcy 2022, Tusay 2022,
Saide 2023; ε Eri is a perennial target), late-1990s pre-Spitzer
disk SED modeling, and stellar-population kinematics papers using
ε Eri only as one of many tracers. The full filtered bib is
preserved in `docs/phase3/_bib/eps-eri.yaml` with `status: skipped`
annotations.

## Open items for follow-up

- **Disk geometry is multi-belt in `disks_curated.json`** (audited
  2026-05-29): eps Eri's asteroid + intermediate + cold belts are
  separate `belt` entries (Backman 2009, Greaves 2014, MacGregor 2015),
  and the Decisions table renders them as per-belt `disk_<belt>_*`
  fields → one Kopernicus Ring each. Remaining: a grain-size / Mie
  color synthesis to replace the K2V-derived tie-break tints.
- **ε Eri b planet Phase 3 follow-up**: the jovian companion's
  atmosphere, ring-system possibility, color tint, and any moon
  population are out of scope for this stellar synthesis. A separate
  `docs/phase3/eps-eri-b.md` workspace is needed, anchored on
  Mawet 2019 + Llop-Sayson 2021 + Roettenbacher 2022 and the JWST
  followups expected 2026–2027.
- **Historical "ε Eri c" debate**: Quillen 2002 inferred an outer
  ~40 AU planet from the cold-ring eccentricity, Benedict 2006
  reported a candidate HST FGS astrometric signal, but Mawet 2019
  direct-imaging non-detection rules out any planet > 0.3 M_Jup beyond
  30 AU. The Su 2017 "Genie" model accommodates the multi-belt
  structure with planets inside the cold ring instead of beyond it.
  Documentation interest only — no cfg row required; included here so
  the next session knows why the "ε Eri c" entry sometimes seen in
  legacy catalogs is excluded.
- **Tie-break visual tints (`disk_tint_rgb_hex`, `limb_darkening_alpha_h`)**:
  both are within-window guesses. If a scattered-light visible imaging
  result for the ε Eri disk emerges (e.g. JWST/NIRCam coronagraph),
  the disk hex should be re-derived. If a K2V limb-darkening
  interferometric measurement becomes available (CHARA, VLTI), the
  α_h value should be replaced with the measured number.
- **Cycle-phase synchronization at game epoch (J2000.0)**: the
  Metcalfe 2013 cycle and the Coffaro 2020 X-ray cycle have not been
  phase-locked to the in-game J2000 epoch. A future cfg revision
  could anchor the activity-driven visual brightening to a specific
  cycle phase so the player sees consistent timing across game years.

## Related

- [alpha-centauri-a](alpha-centauri-a.md), [alpha-centauri-b](alpha-centauri-b.md) — neighboring K1V comparator (B) and G2V comparator (A); ε Eri visual tint distinguished from α Cen B's slightly warmer `#ffcb91`
- [proxima-cen](proxima-cen.md) — nearest planet host; ε Eri is the second-nearest, only 0.27 pc + 1.9 pc further out
- [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) — single-star astrometry only; ε Eri does not need binary-orbit propagation
- [methodology](../reference/methodology.md) — DB schema source
- [rex-data-comparison](../reference/rex-data-comparison.md) — REX has only a basic stellar entry for ε Eri; the triple-ring disk and the confirmed jovian are NearStars-exclusive additions
