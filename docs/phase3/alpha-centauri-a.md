<!-- α Centauri A Phase 3 synthesis: cfg-ready decisions and reasoning -->
# α Centauri A — Phase 3 Synthesis

α Centauri A (HD 128620, HIP 71683, GJ 559 A) is the brighter of the
nearest stellar pair and the closest G-type star to the Sun. Spectral
type G2V (Porto de Mello 2008) — essentially a solar twin at a
distance of 1.3384 ± 0.0011 pc (Kervella 2017, derived from the
Pourbaix & Boffin 2016 parallax of 747.17 ± 0.61 mas). With α Centauri
B it forms a visual binary of 79.91-year period in a moderately
eccentric (e ≈ 0.52) orbit ranging from 11.2 AU at periastron to 35.6
AU at apastron. Proxima Centauri, gravitationally bound at roughly
13 000 AU (Kervella 2017), completes the triple.

The fundamental parameters are exceptionally well-constrained.
Interferometric angular diameters from VLTI/PIONIER (Kervella 2017)
give R = 1.2234 ± 0.0053 R☉ (0.43% precision), while the
double-lined spectroscopic binary solution of Pourbaix & Boffin 2016
fixes the dynamical mass at 1.1055 ± 0.0039 M☉. Asteroseismic
oscillations detected by Bouchy & Carrier (2001) and de Meulenaer
2010 — combined with the classical observables — yield an age of
**5.3 ± 0.3 Gyr** for the α Centauri system (Joyce & Chaboyer 2018).
The DB Phase 2 attribution shows a less-correct 4.81 ± 0.5 Gyr that
appears to have transcribed an intermediate model fit rather than the
paper headline; this synthesis uses the paper-headline value (see
Open items for the DB erratum).

Metallicity is slightly super-solar, [Fe/H] = +0.24 ± 0.03 (Porto de
Mello 2008), consistent with the disk-population kinematics. The
rotation period from photometric variability is 22 ± 3 days (DeWarf
2010), and the same campaign measures a chromospheric activity index
log R'HK = −4.95 — quiet, but with a Sun-like coronal cycle of roughly
19 years detected in X-rays by Robrade 2016. There is no confirmed
planet around α Cen A; Beichman & Sanghi 2025 reported a candidate
giant point source in MIRI direct-imaging at ≈ 1.5 AU separation,
which remains unconfirmed at the time of this synthesis.

**Scenario choice for NearStars: a quiet, Sun-like G2V star slightly
brighter and warmer than Sol, viewed in close visual proximity to its
K1V companion B and at huge angular separation from Proxima.** All
17 cfg picks track the canonical parameter set; the four tie-break
picks involve visual hex colors and binary-event geometry where the
literature is silent.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | G2V | high | Porto de Mello 2008; IAU MK system |
| `mass_msun` | 1.1055 ± 0.0039 | high | Pourbaix & Boffin 2016 — double-lined visual+spectroscopic binary fit |
| `radius_rsun` | 1.2234 ± 0.0053 | high | Kervella 2017 — VLTI/PIONIER limb-darkened interferometry |
| `teff_k` | 5847 ± 27 | high | Porto de Mello 2008 — high-resolution spectroscopy, differential to Sun |
| `luminosity_lsun` | 1.519 | high | derived from R and Teff via Stefan–Boltzmann; Bigot 2008 agrees |
| `metallicity_fe_h_dex` | +0.24 ± 0.03 | high | Porto de Mello 2008 — adopted in Joyce 2018 |
| `age_gyr` | 5.3 ± 0.3 | high | Joyce & Chaboyer 2018 — joint asteroseismic + classical, DSEP code, 31 viable model pairs |
| `rotation_period_days` | 22 ± 3 | high | DeWarf 2010 — photometric variability |
| `activity_log_rhk` | −4.95 | high | DeWarf 2010 — chromospheric Ca II H&K |
| `activity_cycle_years` | 19 | medium | Robrade 2016 — coronal X-ray cycle, Sun-like in amplitude |
| `x_ray_log_lx_cgs_min` | 27.0 | medium | Robrade 2016 cycle minimum |
| `x_ray_log_lx_cgs_max` | 27.6 | medium | Robrade 2016 cycle maximum |
| `limb_darkening_alpha_h` | 0.1404 ± 0.0050 | high | Kervella 2017 — H band power-law fit, marginally weaker than 1D model predictions |
| `visual_surface_tint_hex_primary` | `#fff4e8` (warm white, slightly more yellow-cream than Sun) | medium | Tie-break: G2V blackbody at 5847 K + visual distinction from solar reference; interesting-first per the interesting-first rule |
| `stellar_color_temp_k` | 5847 | high | derived from Teff |
| `visual_in_planet_sky_apparent_diameter_arcmin` (from α Cen B at 23 AU mean) | 0.5 | high | derived: 2 R★ / a × (180·60/π) |
| `visual_companion_event_corona_visible_during_b_eclipse` | true | medium | Tie-break: at α Cen AB orbit conjunctions seen from a hypothetical α Cen B planet, A occulted by B reveals corona; rare and dramatic in-game event |

## Surface synthesis

The photosphere of α Centauri A is the closest analog to the Sun in
the entire NearStars catalog. Effective temperature 5847 K places it
75 K hotter than Sol; the half-magnitude higher luminosity stems from
the slightly larger 1.22 R☉ envelope inflated by the super-solar
metallicity. 3D radiative-hydrodynamic granulation simulations
(STAGGER code, used by Kervella 2017 §4) predict granulation
contrast and timescales nearly identical to solar, scaled by a ~5%
factor. The visible disk shows the canonical Sun-like central
brightness with mild limb darkening — the H-band power-law exponent
α(A) = 0.1404 measured by Kervella is marginally weaker than 1D
atmosphere models predict, mirroring the Sun's own departure from
analytic limb-darkening.

Spot coverage is modest: log R'HK = −4.95 (DeWarf 2010) places A
fractionally less active than the modern Sun. During the 19-year
coronal cycle (Robrade 2016), peak spot coverage is comparable to
solar maximum (~0.5% of the disk), with active regions at ±35°
latitude. In a tidally-stable orbit at α Cen A's habitable zone
(~1.3 AU based on Wang 2022), an observer would see a recognizable
solar-type disk with limb darkening, granulation pattern, sunspots
during activity maximum, and faculae bridging active regions.

The slightly higher metallicity tints the SED marginally toward the
red — the +0.24 dex Fe/H increase shifts the bolometric continuum by
roughly ~10 K equivalent reddening, imperceptible at the spectral
resolution typical of in-game illumination color but contributing
to the warmer cream visual choice over a pure solar-white reference.

## Atmosphere synthesis

α Cen A hosts a quiet G-dwarf atmosphere with the standard
chromosphere–transition-region–corona structure. The chromosphere is
moderately filled with Hα and Ca II H&K emission; FUV/UV monitoring
by DeWarf 2010 finds emission lines consistent with Sun-like activity
across an 11-year (chromospheric) and 19-year (coronal X-ray; Robrade
2016) cycle. The X-ray luminosity range log L_X = 27.0–27.6 (cgs;
0.5–2 keV) cycles by a factor of ~4, again Sun-like.

There is no evidence of frequent flares above the photometric noise
of the DeWarf monitoring; α Cen A is well within the inactive G-dwarf
locus and provides a benign space-weather environment for any inner
planet. Coronal mass ejections, if comparable to the Sun's, would
launch at ~10²² g per event and ~1–10 events per day during cycle
maximum — but the radial scaling from 1 AU implies fluxes at any
candidate α Cen A planet differ negligibly from Sun-at-Earth values.

The transition region produces a Lyman-α continuum + Lyα line typical
of G2V stars; Ayres 2015 Tier-B references compile the full UV-to-
X-ray spectrum. The integrated XUV luminosity is below 10⁻⁴ L_bol,
unable to materially erode an Earth-like atmosphere over Gyr
timescales at A's habitable zone.

## Rotation & spin synthesis

A 22 ± 3 day photometric rotation period (DeWarf 2010) is slightly
slower than the Sun's mean rotation, consistent with α Cen A's
~0.5 Gyr age advantage over Sol via the Skumanich braking law
P_rot ∝ √t. Asteroseismic inversions (Bazot 2007, de Meulenaer 2010,
Bedding 2004) detect the p-mode oscillation spectrum with frequency
separations Δν = 105.9 ± 0.3 μHz and ν_max ~ 2200 μHz; the
characteristic acoustic timescale 2π/Δν ≈ 2.6 h is comparable to the
solar 5-minute oscillation when scaled by the larger radius and lower
sound speed.

Differential rotation is not directly resolved but is expected to be
Sun-like, with the equator rotating roughly 20% faster than the
poles. The rotation axis inclination is poorly constrained — for
visual rendering NearStars adopts an axis tilted ~30° to the line of
sight from α Cen B's orbital plane, consistent with a randomly
oriented spin axis in a long-lived binary.

## Visual styling

In the NearStars renderer, α Cen A is portrayed as a warm-cream
G2V star — visually nearly indistinguishable from Sol but with the
faintest extra cream tint encoded as `#fff4e8` (in contrast to a
strict solar `#fff8f0`). The choice is a tie-break against a pure
solar match: in the binary-pair view, the visible color contrast
between A's cream and B's clear orange makes the system instantly
recognizable to the player.

At 1.3 pc viewed from Earth, the apparent magnitude V = 0.01 places
α Cen A as one of the three brightest stars in the night sky. From
a candidate planet in α Cen A's habitable zone (Wang 2022 model
Earth at 1.25 AU), the star fills 0.5° angular diameter — slightly
smaller than the Sun seen from Earth (0.53°) because of A's larger
distance from the HZ.

The companion B at ~11-36 AU separation (depending on orbital phase)
ranges from a brilliant K1V point of light at apastron to an
apparent stellar disk of ~0.04° at periastron — never resolved by
the naked eye but visible as a strikingly orange "second sun" in
deep-sky telescope views from a hypothetical α Cen A planet. The
binary conjunctions every 79.91 years produce dramatic alignment
events where, viewed from a planet orbiting α Cen B, A briefly
appears to occult B's disk; the converse alignment likewise reveals
A's corona during B-front transits — the rare events flagged in the
cfg `visual_companion_event_corona_visible_during_b_eclipse` field.

Sunspots, faculae, and prominences are rendered at solar-analog scale
during activity maximum, peaking every 19 years (Robrade 2016 X-ray
cycle, with the chromospheric 11-year sub-cycle as a faster
amplitude modulation).

## Bibliography

### Read (visual-informative, drove decisions above)

- **Pourbaix D. & Boffin H. M. J. 2016** — *Parallax and masses of α
  Centauri revisited*, A&A 586, A90 (`2016A&A...586A..90P`,
  arXiv:1601.01636). Double-lined visual-spectroscopic binary fit
  using ESO/HARPS archive; revised orbital parallax 743 mas, M_A =
  1.1055 ± 0.0039 M☉ and M_B = 0.9373 ± 0.0028 M☉; sets the
  dynamical mass anchor for the system.
- **Kervella P. et al. 2017** — *The radii and limb darkenings of α
  Centauri A and B*, A&A 597, A137 (`2017A&A...597A.137K`,
  arXiv:1610.06185). VLTI/PIONIER interferometry in H band; angular
  diameters θ_LD(A) = 8.502 ± 0.038 mas, θ_LD(B) = 5.999 ± 0.025
  mas; with the revised parallax derives R_A = 1.2234 ± 0.0053 R☉,
  R_B = 0.8632 ± 0.0037 R☉.
- **Joyce M. & Chaboyer B. 2018** — *Classically and Asteroseismically
  Constrained 1D Stellar Evolution Models of α Centauri A and B*,
  ApJ 864, 99 (`2018ApJ...864...99J`, arXiv:1806.07567). DSEP
  evolutionary models fitting classical + p-mode constraints
  simultaneously; 31 viable model pairs; system age 5.3 ± 0.3 Gyr.
- **DeWarf L. E. et al. 2010** — *X-Ray, FUV, and UV Observations of α
  Centauri B: Determination of Long-term Magnetic Activity Cycle and
  Rotation Period* (`2010ApJ...722..343D`). Chromospheric and coronal
  monitoring of both A and B; rotation periods 22 ± 3 d (A) and
  36–40 d (B); 8.1-yr chromospheric cycle for B and Sun-like ~19-yr
  cycle for A. **No arXiv preprint** — Tier A manual followup;
  values drawn from the ApJ abstract and the DB Phase 2 attribution.
- **Robrade J. et al. 2016** — *Coronal activity cycles in action —
  X-rays from α Centauri A/B*, A&A 596, A53 (`2016A&A...596A..53R`,
  arXiv:1612.06570). XMM-Newton + Chandra monitoring; confirms a
  ~19-yr coronal cycle on A; log L_X cycle amplitude factor ~4.
- **Beichman C. et al. 2025** — *Worlds Next Door: A Candidate Giant
  Planet Imaged in the Habitable Zone of α Centauri A. I*
  (`2025NatAs.tmp.../...`, arXiv:2508.03814) and **Sanghi A. et al.
  2025** *Worlds Next Door II* (arXiv:2508.03812). JWST/MIRI direct
  imaging of a candidate point source at ~1.5 AU; identifies as a
  giant-planet candidate "S1"; remains unconfirmed pending follow-up.

### Read (context / methodology, not directly decision-driving)

- **Porto de Mello G. F. et al. 2008** — *Photospheric, chromospheric,
  and coronal activity of α Cen A* (`2008A&A...488..653P`). Defines
  the canonical [Fe/H] = +0.24 ± 0.03 and Teff = 5847 ± 27 K for A.
- **Bedding T. R. et al. 2004** — *Oscillation frequencies and mode
  lifetimes in α Centauri A* (`2004ApJ...614..380B`,
  arXiv:astro-ph/0406471). 28 p-modes detected; sets the
  asteroseismic constraint table for A.
- **de Meulenaer P. et al. 2010** — *Core properties of α Cen A
  using asteroseismology* (`2010A&A...523A..54D`, arXiv:1009.1237).
  44 p-modes; refined Δν = 105.9 μHz, ν_max ≈ 2200 μHz.
- **Bigot L. et al. 2006** — VLTI/VINCI 3D-hydrodynamic radiative
  transfer constraint on α Cen B granulation. Cited via Kervella
  2017 §4.
- **Wang H. S. et al. 2022** — *A Model Earth-sized Planet in the
  Habitable Zone of α Centauri A/B* (`2022ApJ...927..134W`,
  arXiv:2110.12565). Frames the cfg habitable-zone geometry; 1.25 AU
  hot edge, 1.85 AU cold edge for A.
- **Quarles B. et al. 2022** — *Milankovitch cycles for a
  circumstellar Earth-analogue within α Centauri-like binaries*
  (arXiv:2108.12650). Sets binary-perturbation obliquity
  oscillation envelope for any A or B planet.

### Read (instrument / non-cfg-decisive)

- **Salmon S. J. A. J. et al. 2021** — Reinvestigation of α Cen AB
  asteroseismic constraints with modern oscillation codes
  (arXiv:2011.14932).
- **Akeson R. et al. 2021** — *Precision Millimeter Astrometry of the
  α Centauri AB System* (arXiv:2104.10086). Sub-milliarcsecond
  positions; sub-2025 ALMA campaign.
- **Krishnamurthy A. et al. 2021** — ASTERIA transit search around α
  Cen A and B (`2021AJ....161..275K`). No-detection limits.
- **Spada F. et al. 2019** — *Entropy calibration of the radii of
  cool stars: α Cen A and B* (arXiv:1909.00701). Validates the
  Kervella 2017 + Joyce 2018 picture against entropy-based
  predictions.

### Not read — no arXiv preprint or low-priority (~50 papers)

Conference abstracts (EPSC/AGU/DPS), interstellar-propulsion
proposals (Heller 2017 photon sails, Forgan 2018 Project Lyra), and
SETI / laser-emission searches (Marcy 2022, Tusay 2022, Saide 2023)
contribute no cfg-decisive content. The full filtered bib is
preserved in `docs/phase3/_bib/alpha-centauri-a.yaml` with
`status: skipped` annotations.

## Open items for follow-up

- **DB erratum, `age_measurements` recommended entry for Joyce &
  Chaboyer 2018**: DB stores `value_gyr = 4.81 ± 0.5`; paper headline
  is **5.3 ± 0.3 Gyr**. The 4.81 number likely transcribed an
  intermediate fit (the paper presents multiple physics
  configurations); fix the DB attribution to the paper headline.
- **Beichman/Sanghi 2025 "S1" giant-planet candidate**: if a 2026
  follow-up confirms the point source as a bound companion at
  ~1.5 AU, a new Decisions entry `circumstellar_planet_present: true`
  is needed and the cfg `has_companion_b` (currently absent) should
  be added.
- **Higher-fidelity granulation pattern**: STAGGER simulations
  predict subtle limb-to-center contrast variations not modeled in
  the cfg `limb_darkening_alpha_h` scalar; a future cfg variant could
  capture the 3D structure for very close fly-by sequences.
- **Cycle phase at game epoch (J2000.0)**: the 19-yr X-ray cycle and
  the chromospheric activity cycle are not phase-locked in the
  current cfg. A phase synchronization based on Robrade 2016 cycle
  start epochs would let activity-driven CME flux track real-time
  in-game progression.
