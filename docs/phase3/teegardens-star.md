# Teegarden's Star — Phase 3 Synthesis

Teegarden's Star (GAT 1370, GJ J02530+1652) is an M7.0 V ultra-cool
dwarf at 3.832 ± 0.004 pc — the 24th-25th nearest star to the Sun
(Zechmeister 2019; Dreizler 2024 reference list). With M = 0.089 ±
0.009 M☉ and R = 0.107 ± 0.004 R☉ (Schweitzer 2019 CARMENES SED +
empirical mass-radius relation), it sits near the hydrogen-burning
limit but is still firmly a star. Effective temperature 2904 ± 51 K
and luminosity 7.32 × 10⁻⁴ L☉ (Cifuentes 2020 bolometric flux fit) make
it cooler and dimmer than Proxima Centauri (M5.5 Ve, 2980 K) and only
marginally warmer than TRAPPIST-1 (M8 V, 2566 K). Stefan-Boltzmann
gives R = 0.107 R☉ from these L and Teff — internally self-consistent
with Schweitzer's empirical value.

The star carries the kinematic signature of an evolved thick-disc
population (U, V, W = −69, −71, −59 km/s; Cortés-Contreras 2016 via
Zechmeister 2019), giving a kinematic age of 8 ± 3 Gyr. The
chromospheric activity is exceptionally low for spectral type M7 V:
log L(Hα) / L_bol = −5.25 to −5.37 (Zechmeister 2019 average and
Fuhrmeister 2024 update respectively) — Teegarden's Star sits among
the quietest one or two M7 V dwarfs known. Combined with the slow
rotation period of 96 ± 2 days (Lafarga 2021 spectroscopic indices,
confirmed by Terrien 2022 HPF and Shan 2024 CARMENES photometry, all
within ~5%), the picture is of a star that long ago shed its angular
momentum and entered a quiet senescence.

Teegarden's Star hosts three confirmed radial-velocity planets, all
near or below 1.2 M⊕ minimum mass: b (4.91 d, S ≈ 1.08 S⊕, inner edge
of the habitable zone), c (11.4 d, S ≈ 0.35 S⊕, cold outer edge), and
d (26.13 d, S ≈ 0.12 S⊕, beyond the habitable zone — discovered by
Dreizler 2024). None transit. The mutual Hill separations are
comfortably stable (>13 mutual Hill radii between adjacent planets),
making this dynamically a "loose" system more similar to GJ 1002 than
to TRAPPIST-1 — though Dreizler hints that the unresolved RV signal at
7.7 d could yet add a fourth body and tighten the architecture.

The Dreizler 2024 reanalysis of the stellar fundamental parameters
using the Marfil 2021 line list yields slightly different numbers (Teff
= 3034 K, R = 0.120 R☉, M = 0.097 M☉) that disagree with Schweitzer
2019's recommended values at the ~3σ level for the radius. Phase 2
adopted the Schweitzer 2019 numbers as recommended because they are
self-consistent under Stefan-Boltzmann with the directly measured
luminosity, whereas Dreizler's higher Teff combined with the same L
implies R ≈ 0.098 R☉ rather than the quoted 0.120. This stellar-parameter
ambiguity directly feeds the runaway-vs-habitable decision for planet b
and is flagged in Open items.

**Scenario choice for NearStars: a quiet, deeply red M7 V dwarf with
an 8 Gyr kinematic age, ~96 d rotation, low chromospheric Hα and X-ray
output, and rare large flares (≥ 10³⁵ erg only every ~2.4 years).
Visual styling emphasises the very deep red continuum, the long-period
modulation, and the rarity of dramatic flares compared to Proxima.**
19 cfg picks; 16 canonical-aligned, 3 tie-break (limb darkening
interpolation, surface tint hex, flare tint hex).

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M7.0 V | high | Alonso-Floriano 2015; DB |
| `mass_msun` | 0.089 ± 0.009 | high | Schweitzer 2019 — CARMENES empirical M–R relation; DB recommended |
| `radius_rsun` | 0.107 ± 0.004 | high | Schweitzer 2019 — Stefan–Boltzmann from L and Teff; self-consistent |
| `teff_k` | 2904 ± 51 | high | Cifuentes 2020 SED fit; DB recommended |
| `luminosity_lsun` | 7.32e-4 ± 4e-5 | high | Cifuentes 2020 bolometric flux |
| `metallicity_fe_h_dex` | −0.19 ± 0.16 | medium | Passegger 2019 high-res spectroscopy; DB recommended |
| `age_gyr` | 8.0 ± 3.0 | medium | Zechmeister 2019 kinematic + Hα-activity age; thick-disc UVW |
| `rotation_period_days` | 96 ± 2 | high | Lafarga 2021 spectroscopic indices; Dreizler 2024 recommended |
| `activity_log_lhalpha_lbol` | −5.25 to −5.37 | high | Zechmeister 2019 (−5.25 average), Fuhrmeister 2024 (−5.37 updated); quiet for M7 V |
| `activity_log_rhk` | not measured | n/a | Ca II H&K only in ESPRESSO; published L_Hα/L_bol used instead |
| `x_ray_log_lx_cgs_quiescent` | 25.55 | high | Fuhrmeister 2024 — L_X ≈ 3.7×10²⁵ erg/s (Chandra + XMM agree) |
| `x_ray_log_lx_lbol_quiescent` | −4.9 | high | Fuhrmeister 2024; "minimum flux law" obeyed at low-mass end |
| `activity_cycle_years` | ~7 | low | Dreizler 2024 — coherent ~2500 d trend in RV + activity indices; weak detection |
| `flare_rate_per_day_total` | 0.026 | high | Fuhrmeister 2024 TESS — 2 flares of ~10³² erg in 80 d active sector; 0 in 56 d quiet sectors |
| `flare_largest_observed_erg` | 1.3e32 | high | Fuhrmeister 2024 — TESS Flares I, II both ≈ 1.3×10³² erg total |
| `flare_rate_superflare_per_year` | 0.4 | medium | Dreizler 2024 §5.4 SPECULOOS — ≥ 10³⁵ erg every 2.4 yr from FFD extrapolation (α=1.84±0.05) |
| `flare_power_law_alpha` | 1.84 ± 0.05 | high | Dreizler 2024 §5.4 — SPECULOOS U-band FFD fit |
| `limb_darkening_alpha_h` | ~0.5 | low | Tie-break: not directly measured for Teegarden's Star; interpolated from M-dwarf model grid (Claret 2018) at Teff 2904 K; interesting-first per the interesting-first rule |
| `visual_surface_tint_hex_primary` | `#b03020` (deeper red than M5.5V; M7.0 V with strong TiO/VO/H₂O band depression) | medium | Tie-break: Teff 2904 K blackbody + late-M molecular bands; chose tint visually distinct from Proxima's `#c54c2a` to convey "even cooler and redder" |
| `visual_flare_color_hex` | `#ff5e2a` (Hα + Balmer-dominated optical flare) | medium | Tie-break: no published Teegarden-specific flare spectrum; adopt the Proxima/M-dwarf flare-tint convention for game continuity |
| `stellar_color_temp_k` | 2904 | high | derived from Teff |

## Surface synthesis

Teegarden's Star is one of the dimmest objects in the NearStars
catalog, with only TRAPPIST-1 cooler. At 2904 K and 0.107 R☉ the
photospheric SED is heavily depressed below ~7000 Å by overlapping
TiO, VO, FeH, and H₂O absorption bands, leaving most of the integrated
bolometric flux in the near- and mid-infrared. The Cifuentes 2020 SED
fit (the CARMENES input catalogue paper) integrates broad-band
photometry across optical-NIR to yield L = 7.32 × 10⁻⁴ L☉ — about
1/1370 of the Sun's luminosity and roughly half of Proxima's. Stefan-
Boltzmann combining this L with the Cifuentes Teff = 2904 K produces
R = 0.107 R☉, which agrees within uncertainty with Schweitzer 2019's
empirical mass-radius value of 0.107 ± 0.004 R☉; this self-consistency
is what motivates Phase 2's recommendation of the Schweitzer parameter
set.

Dreizler 2024 reports an alternative parameter set using the Marfil
2021 spectroscopic grid: Teff = 3034 ± 45 K, R = 0.120 ± 0.012 R☉,
M = 0.097 ± 0.010 M☉. These values come from evolutionary model
matching rather than direct SED integration, and the higher Teff is
not internally consistent with the published bolometric luminosity —
Stefan-Boltzmann from L = 7.22 × 10⁻⁴ L☉ and Teff = 3034 K gives
R ≈ 0.098 R☉, not 0.120. Phase 2 noted this 3σ disagreement and stayed
with Schweitzer 2019. The cfg therefore renders Teegarden's Star at
R = 0.107 R☉, Teff = 2904 K. (See Open items for the Dreizler-variant
runaway scenario for planet b.)

The limb-darkening profile has not been directly measured; the cfg
adopts α(H) ≈ 0.5 by interpolating the Claret 2018 M-dwarf grid to
Teff 2904 K, marking it as a low-confidence tie-break. This is steeper
than for Proxima (0.4) and consistent with the trend toward stronger
limb darkening at cooler photospheric temperatures.

Sunspot coverage is expected to be very low given the chromospheric
quiet (log R'HK not published, but log L(Hα)/L_bol = −5.25 to −5.37 —
about an order of magnitude below Proxima). Photometric variability
in TESS sectors 43, 70, and 71 shows trends of only ~0.01 in
normalized flux over a 27-day sector (Dreizler 2024 §4.1) with no
clear rotational modulation, even though the 96-day rotation period
should be marginally detectable — supporting the conclusion that spot
contrast is small.

## Atmosphere synthesis

Teegarden's Star is exceptionally quiet by ultra-cool dwarf standards,
but it is not inactive. Fuhrmeister 2024 (arXiv:2504.02338) presents
the first dedicated multi-wavelength activity study, combining 298
CARMENES spectra, 11 ESPRESSO spectra, dedicated Chandra (50 ks) and
XMM-Newton (29 ks) X-ray pointings, and three TESS sectors. The
quiescent X-ray luminosity from both X-ray observatories agrees at
L_X ≈ 3.7 × 10²⁵ erg/s (log L_X = 25.57), giving log L_X / L_bol ≈
−4.9. This places Teegarden's Star among the weakest known stellar
X-ray sources in absolute terms, but its relative L_X / L_bol is still
much higher than solar — the dim photosphere lets a modest corona
dominate the energy ratio. The mean X-ray surface flux F_X obeys the
"minimum flux law" of Schmitt (1997) for cool main sequence stars, so
even the lowest-mass stars maintain a magnetically heated corona.

The chromospheric Hα line is filled in (not in emission) during quiet
phases — when an emission line does appear, it is double-horned with
the red horn slightly elevated, indicative of the mass motions seen in
hydrodynamic flare simulations. Zechmeister 2019 quoted log L(Hα) /
L_bol = −5.25 averaged over all CARMENES spectra; Fuhrmeister 2024
updates this to −5.37 with the larger dataset, with Hα varying from
−5.58 in deepest quiescence to −4.26 during the brightest observed
flares.

**Flares** are rare but real. Fuhrmeister 2024 identifies four flares
with detailed coverage:
- TESS Flare I (sector 43, 2021): total bolometric energy ≈ 1.3 ×
  10³² erg (T_flare = 15 000 K blackbody assumption), comparable to
  the largest solar flares.
- TESS Flare II (sector 43, 2021): also ≈ 1.3 × 10³² erg, longer
  decay time but smaller peak.
- XMM-Newton Flare III (2021): X-ray fluence 1.6 × 10²⁹ erg, peak
  L_X ≈ 9 × 10²⁶ erg/s. Shows the Neupert effect (X-ray rises after
  U-band).
- XMM-Newton Flare IV: weaker U-band only, no X-ray counterpart
  detectable.

The overall observed flare rate of ~2 events per 80 days with energy
~10³² erg gives 2.6 ± 1.8 flares per 100 days — somewhat higher than
Seli 2021 FFD predictions for very late-type M dwarfs, hinting that
sector 43 may have caught Teegarden in a more active phase. Dreizler
2024's complementary SPECULOOS photometric survey (142 h over 35
nights between 2021 and 2022) found 13 lower-energy flares with a
power-law FFD of α = 1.84 ± 0.05, consistent with typical mid-to-late M
dwarfs. Extrapolating, large prebiotic-relevant flares of ≥ 10³⁵ erg
should occur at most once every 2.4 years.

A long-period sinusoidal trend on a timescale of ~2500 days (≈ 7
years) in both RV and spectroscopic activity indices (Dreizler 2024
§4.1, Fig. 12) is suggestive of an activity cycle, though the
detection is at the edge of the data baseline and could equally be
secular drift. The cfg adopts 7 yr with low confidence.

The combined picture is a star whose mean energy output is dominated
by quiet thermal emission, with rare but proportionally significant
flare excursions — much rarer than Proxima's roughly daily flare rate.
For exoplanet atmospheric retention, this is a far gentler environment
than the typical M dwarf, and is one of the reasons Wandel 2019 finds
both Teegarden b and c retain habitability ranges across a wide
atmospheric-heating parameter space.

## Rotation & spin synthesis

The 96-day rotation period is exceptionally slow even for an old M
dwarf. Lafarga 2021 first identified it from CARMENES spectroscopic
indices (CRX, dLW), and the same period has since been recovered by
Terrien 2022 from HPF Zeeman signatures (100 d), Kemmer 2023 from
clustered activity-index analysis (98 d), and Shan 2024 from CARMENES
photometric monitoring (97.56 d). Dreizler 2024 adopts 96 d as the
recommended value, with the noted caveat that an alternative 172-day
signal in the RV residuals is also coherent over the dataset duration —
its activity-indicator correlation makes a stellar origin more likely
than a planetary one, but the case is not closed.

The slow rotation matches the expectation from gyrochronological
spin-down (Newton 2018 MEarth South sample places only ~6 of 281 low-
mass M stars at rotation periods > 150 d; Shan 2024 finds similarly
few). It also matches the prediction from a Rossby number of order
unity (Wright 2011), since the empirical convective turnover time
calibration of Wright 2011 Eq. 11 gives τ_c ≈ 130 days for M = 0.089
M☉ — close to the observed 97 d rotation, implying Teegarden's Star is
near saturation of the rotation-activity relation but with very weak
absolute activity, consistent with the deep saturation regime for old
fully convective stars.

The line-of-sight rotational broadening is unresolved in CARMENES
(v sin i < 2 km/s, Reiners 2018), implying the rotation axis
inclination is consistent with the planetary orbital inclinations
(near-edge-on) given R = 0.107 R☉ and P_rot = 96 d (equatorial
velocity ≈ 0.06 km/s).

Asteroseismic p-modes are inaccessible for an M7 V due to the high
surface gravity and tiny amplitudes; rotation is constrained entirely
from photometric and spectroscopic modulation.

## Visual styling

Teegarden's Star renders as a very deep red M7 V — even more red and
dim than Proxima Centauri, with the integrated SED firmly in the
near-infrared. The photospheric tint `#b03020` is chosen slightly
darker and redder than Proxima's `#c54c2a` to convey the cooler
(2904 K vs 2980 K) and dimmer (7.3 × 10⁻⁴ vs 1.6 × 10⁻³ L☉) star.
Viewed from Teegarden b at 0.0259 AU, the star fills 2.20° angular
diameter (about 4× the apparent diameter of the Sun seen from Earth);
from c at 0.046 AU it fills 1.25°; from d at 0.079 AU it fills 0.72°.
On all three planets the host star is a large, dim, distinctly red
disk dominating the daytime sky.

Flares are rare events. Compared to Proxima's 1.49 flares per day with
multiple superflares per year, Teegarden produces only ~2-3 ~10³² erg
flares per 80 d, and ≥ 10³⁵ erg flares only once every couple of
years. In-game rendering should reflect this rarity — a flare on
Teegarden's Star should be a striking visual event, not a routine
nuisance. The flare colour `#ff5e2a` (Hα-dominated optical with broadband
brightening) follows the Proxima precedent for game continuity.

The corona is rendered as a faint cyan-white halo modulating slowly
with the ~7-year activity cycle; the modulation amplitude is much
smaller than Proxima's because Teegarden's mean L_X is ~25× lower in
absolute terms. Stellar wind streamers are not directly visible.

The most distinctive visual cue is the **slowness** of everything.
The 96-day rotation makes any visible spot or active region drift
across the disk on a timescale of weeks; the 7-year activity cycle
makes brightness modulation an in-game seasonal effect; flare events
are punctuations rather than weather. From a habitable-zone vantage
this is what an "old, settled" red dwarf looks like.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Zechmeister M. et al. 2019** — *The CARMENES search for exoplanets
  around M dwarfs. Two temperate Earth-mass planet candidates around
  Teegarden's Star*, A&A 627, A49 (`2019A&A...627A..49Z`,
  arXiv:1906.07196). Discovery paper for planets b and c; baseline
  stellar parameters (Schweitzer 2019 referenced), log L(Hα)/L_bol =
  −5.25, kinematic age > 8 Gyr, thick-disc UVW.
- **Dreizler S. et al. 2024** — *Teegarden's Star revisited. A nearby
  planetary system with at least three planets*, A&A 684, A117
  (`2024A&A...684A.117D`, arXiv:2402.00923). Planet d discovery,
  refined b/c orbits, rotation period 96 d (Lafarga reference), updated
  Marfil 2021 stellar parameters, SPECULOOS flare FFD.
- **Schweitzer A. et al. 2019** — *The CARMENES search for exoplanets
  around M dwarfs. Different roads to radii and masses of the target
  stars* (`2019A&A...625A..68S`, arXiv:1904.03231). Empirical M-R
  relation; recommended M = 0.089 M☉, R = 0.107 R☉.
- **Cifuentes C. et al. 2020** — *CARMENES input catalogue of M
  dwarfs. V. Luminosities, colours, and spectral energy distributions*
  (`2020A&A...642A.115C`, arXiv:2007.15077). SED-integrated bolometric
  L = 7.32 × 10⁻⁴ L☉; Teff = 2904 K; recommended luminosity and Teff.
- **Passegger V. M. et al. 2019** — *The CARMENES search for
  exoplanets around M dwarfs. Photospheric parameters of target stars
  from high-resolution spectroscopy* (`2019A&A...627A.161P`,
  arXiv:1907.00807). High-res [Fe/H] = −0.19 ± 0.16; recommended
  metallicity.
- **Fuhrmeister B. et al. 2024** — *Coronal and chromospheric activity
  of Teegarden's star*, A&A 691, A208 (`2024A&A...691A.208F`,
  arXiv:2504.02338). Comprehensive activity census — TESS flare
  energies ≈ 1.3 × 10³² erg, Chandra + XMM L_X ≈ 3.7 × 10²⁵ erg/s,
  Neupert effect detection, chromospheric Hα variability.

### Read (context / methodology, not decision-driving)

- **Marfil E. et al. 2021** — *Spectral synthesis of CARMENES M-type
  stars* (`2021A&A...656A.162M`). Line list used by Dreizler 2024 for
  the alternative stellar parameter set (Teff = 3034 K, R = 0.120
  R☉). Phase 2 did not adopt these because of internal Stefan-Boltzmann
  inconsistency.
- **Lafarga M. et al. 2021** — Spectroscopic-index rotation periods
  for CARMENES targets. Source of the 96 d rotation period.
- **Shan Y. et al. 2024** — *The PEPSI ultra-high resolution spectral
  library of M dwarfs* + CARMENES rotation period sample. Confirms
  P_rot = 97.56 d.
- **Wandel A. & Tal-Or L. 2019** — *On the Habitability of Teegarden's
  Star planets*, ApJ 880, L21 (`2019ApJ...880L..21W`, arXiv:1906.07704).
  Stellar context for the habitability discussion of b and c.
- **Newton E. R. et al. 2018** — MEarth M-dwarf rotation period
  catalogue. Context for slow-rotation outlier statistics.

### Read (instrument / non-cfg-decisive)

- **Quirrenbach A. et al. 2014, 2020** — CARMENES instrument papers,
  cited but methodology only.
- **Ribas I. et al. 2023** — CARMENES legacy data release. Provides
  the spectra reanalysed by Fuhrmeister 2024.

### Not read — no arXiv preprint or low-priority (~25 papers in stellar bib, marked `skipped`)

The stellar bibliography has 40 papers. Most of the 25 marked
`skipped` are Sky & Telescope / amateur-astronomy retrospectives on the
star's discovery (Sinnott; Stafford; Astrobites), early-21st-century
parallax measurements superseded by Gaia (Gatewood 2009; West 2016),
and CARMENES survey-overview papers (Quirrenbach 2014, 2020) that
contribute methodology context but not new Teegarden-specific numbers.
All are preserved in `docs/phase3/_bib/teegarden-s-star.yaml` with
`status: skipped`.

## Open items for follow-up

- **Stellar parameter ambiguity (Schweitzer 2019 vs Dreizler 2024)**:
  The 3σ disagreement between R = 0.107 R☉ (Phase 2 recommended) and R
  = 0.120 R☉ (Dreizler 2024 Marfil-grid) propagates directly into the
  insolation at planet b (1481 vs 1565 W/m²) and so into the
  habitable-vs-runaway choice. A future independent radius
  determination from CHEOPS-like photometry, JWST occultation, or a
  ground-based interferometric attempt would close this.
- **172-day RV signal**: Dreizler 2024 cannot decisively distinguish
  whether this is stellar activity at twice the rotation period or a
  fourth planet at minimum mass ≈ 2.3 M⊕. The activity-indicator
  correlation suggests stellar origin, but a future ESPRESSO + MAROON-X
  baseline extension could settle it. If planetary, the cfg gains a
  "Teegarden's Star e".
- **Suggestive 7.7-day signal**: Dreizler 2024 finds a 0.5 m/s residual
  signal near a 3:2 commensurability with b and c. If confirmed (mass
  ~0.5 M⊕), it would tighten the system into a TRAPPIST-1-like
  resonant chain.
- **Activity cycle period**: ~2500 d trend is at the edge of the
  dataset baseline. Two-three more years of CARMENES monitoring would
  resolve whether the cycle exists and what its true period is.
- **No published flare-spectrum colour**: The cfg flare tint
  `#ff5e2a` is the Proxima convention by analogy. A Teegarden-specific
  flare spectrum from ESPRESSO during a Flare I-class event would
  refine this.
- **Long-term ZDI mapping**: Reiners 2018 inferred v sin i < 2 km/s
  but did not map the surface magnetic geometry. A future
  spectropolarimetric (CARMENES-pol or future) ZDI map of the slowly
  rotating disc could constrain whether Teegarden hosts a Proxima-like
  kG dipole or a much weaker organized field.

## Related

- [teegardens-star-b](teegardens-star-b.md) — inner-HZ Earth-mass planet, S ≈ 1.08 S⊕
- [teegardens-star-c](teegardens-star-c.md) — outer-HZ Earth-mass planet, snowball candidate
- [teegardens-star-d](teegardens-star-d.md) — cold sub-Earth, Dreizler 2024 discovery, outside HZ
- [proxima-cen](proxima-cen.md) — closest M-dwarf comparison; Proxima is more active by ~25×
- [trappist-1-b](trappist-1-b.md) — similar M-late host (M8 V vs M7 V)
- [methodology](../reference/methodology.md) — DB schema for stellar measurements
- [rex-data-comparison](../reference/rex-data-comparison.md) — Teegarden was a Phase 2 candidate; this is the Phase 3 escalation
