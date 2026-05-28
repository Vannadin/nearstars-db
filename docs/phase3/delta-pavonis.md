<!-- δ Pavonis Phase 3 synthesis: cfg-ready decisions and reasoning -->
# δ Pavonis — Phase 3 Synthesis

δ Pavonis (HD 190248, HIP 99240, GJ 780) is one of the closest
G-type subgiants to the Sun, at 6.10 ± 0.005 pc (Gaia DR3 parallax
163.95 ± 0.12 mas). The spectral classification G8IV (Gray 2006
NStars; Houk & Cowley 1975) places it just off the main sequence —
core hydrogen exhausted, hydrogen-shell burning beginning to inflate
the envelope. Effective temperature 5644 ± 30 K (Gomes da Silva
2021 AMBRE-HARPS) and V = 3.56 make it the brightest G subgiant in
the southern sky and a textbook target for nearby-subgiant studies.
No confirmed planets exist: extreme-precision RV (HARPS, Tinney
2005; Mawet 2017) and direct-imaging (Lannier 2017) campaigns rule
out anything more massive than ~3 M_Jup at 1 AU and Neptune-mass at
the habitable zone, and the ESPRESSO-era limits push deeper.

What δ Pav *does* host is a cold debris disk first detected as a
Spitzer/MIPS 70 µm excess (Beichman 2006) and resolved
photometrically by Herschel/PACS at 70, 100, and 160 µm (Eiroa 2013
DUNES; Lawler & Tanner 2014). Modified blackbody fits to the SED
give a single cold belt at roughly 30–80 AU with dust temperature
T_d ≈ 55 K and dust mass M_d ~ 0.01 M⊕ — small but unambiguous, and
moderately old (system age ~5 Gyr from Gomes da Silva 2021 PARSEC
isochrone, with literature spread 5–9 Gyr across pipelines), already
~5× the typical 50–500 Myr collisional cascade lifetime of µm-cm
dust at 50 AU, implying a collisionally replenished planetesimal
reservoir analogous to a thin Kuiper Belt.

**Scenario choice for NearStars: an old, quiet G8 subgiant —
slightly inflated, slightly redder than a G8V dwarf, viewed against
a faint, single cold debris ring at ~30–80 AU.** Stellar parameters
are canonical-aligned. The disk geometry rests on SED inversion only
(Herschel did not resolve the belt), so disk tint and opacity are
medium/low confidence and noted as such; the cfg ships the belt as
visually subtle until ALMA or JWST resolves it.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | G8IV | high | Gray 2006 NStars; Houk & Cowley 1975 MK catalog; subgiant classification confirmed by HR-diagram position |
| `mass_msun` | 1.064 ± 0.013 | high | Gomes da Silva 2021 PARSEC isochrone with Gaia DR2 parallax + AMBRE-HARPS Teff/[Fe/H]; supersedes earlier Bensby 2014 (1.03 ± 0.07) and Spada 2011 (~1.05) subgiant fits, all within 1σ |
| `radius_rsun` | 1.115 ± 0.025 | medium | Gomes da Silva 2021 PARSEC isochrone (same fit as mass). No direct interferometric diameter exists (δ Pav dec −66° too far south for CHARA; never observed by PAVO@SUSI or VLTI-PIONIER). Bruntt 2010 quoted R = 1.22 ± 0.02 from L+Teff Stefan-Boltzmann with older parallax; the 9% offset vs Gomes 2021 traces to (a) updated Gaia DR2 parallax and (b) PARSEC vs Stefan-Boltzmann method choice |
| `teff_k` | 5644 ± 30 | high | Gomes da Silva 2021 AMBRE-HARPS pipeline; Tsantaki 2013 high-res 5566 ± 36 K and Casagrande 2011 IRFM 5598 ± 80 K bracket within combined uncertainty |
| `luminosity_lsun` | 1.246 ± 0.05 | high | Eiroa 2013 DUNES bolometric flux from SED + Hipparcos parallax; supersedes Stefan-Boltzmann derivation from R + Teff (which gives ~1.17 with current Gomes 2021 values) |
| `metallicity_fe_h_dex` | +0.36 ± 0.02 | high | Gomes da Silva 2021 AMBRE-HARPS (smallest formal uncertainty); Tsantaki 2013 +0.32 ± 0.03, Ramirez 2013 +0.33 ± 0.07, Bensby 2014 +0.37 ± 0.20 all agree within combined errors |
| `age_gyr` | 5.04 ± 1.23 | low | Gomes da Silva 2021 PARSEC isochrone (newest paper, smallest stated uncertainty); Bensby 2014 also gives ~5 Gyr from Geneva-Copenhagen. Tsantaki 2013 isochrone (8.5 ± 1.3) and Eiroa 2013 Ca II age (8.3) both give ~8–9 Gyr — literature is split between ~5 and ~9 Gyr depending on pipeline. Tier-hierarchy pick goes to Gomes 2021 (newest, tightest), but Confidence kept low to reflect the unresolved spread |
| `rotation_period_days` | ≤175 (upper limit); best estimate ~30 from Skumanich | low | Ramirez 2013 v sin i = 0.32 ± 0.05 km/s (HARPS solar-twin precision, supersedes earlier 1–3 km/s upper limits) + R = 1.115 R☉ + sin i ≤ 1 ⇒ P_rot ≤ 175 d for any inclination. No photometric period detected. Skumanich-braking expectation at ~5 Gyr with Sun-like initial spin places P_rot near 30 d but is not directly measured |
| `activity_log_rhk` | −5.13 ± 0.003 | high | Gomes da Silva 2021 — weighted mean of 6002 HARPS spectra 2003–2016; well below solar minimum (log R'HK ≈ −4.96), one of the most inactive G subgiants known. Boro Saikia 2018 multi-survey median −4.99 / HARPS-only median −5.49 brackets this; Henry 1996 Mt Wilson −5.10 agrees |
| `activity_cycle_years` | unknown | low | No long-term Mt. Wilson program coverage; subgiants in this evolutionary phase often show weakened or irregular cycles |
| `x_ray_log_lx_cgs_max` | 26.6 | medium | ROSAT all-sky non-detection upper limit (Hünsch 1998); consistent with very weak corona |
| `limb_darkening_alpha_h` | 0.16 ± 0.02 | medium | Claret 2011 LD tables for G8IV at Teff ≈ 5640 K, log g ≈ 4.0; no direct interferometric LD measurement (no interferometry of δ Pav exists) |
| `visual_surface_tint_hex_primary` | `#ffe8c8` (amber-cream, redder than G2V Sol) | medium | Tie-break: G8IV blackbody at 5644 K + +0.36 dex metallicity reddening; subgiant envelope inflation shifts disk integrated color slightly redder than a G8V dwarf at same Teff |
| `stellar_color_temp_k` | 5644 | high | derived from Teff (Gomes da Silva 2021) |
| `visual_corona_extent_radii` | 1.6 | low | Tie-break: weak chromosphere + low log R'HK = -5.1 → muted corona band; rendered as a thin ring rather than the brighter Sun-like halo |
| `disk_present` | true | high | Beichman 2006 Spitzer/MIPS 70 µm excess; Eiroa 2013 Herschel/PACS confirmed at 70/100/160 µm |
| `disk_inner_radius_au` | 30 | medium | Lawler & Tanner 2014 single-belt fit r_in ≈ 30 AU from modified blackbody at T_d = 55 K; Eiroa 2013 finds r_in 23–35 AU depending on grain size |
| `disk_outer_radius_au` | 80 | medium | Lawler & Tanner 2014 r_out ≈ 80 AU; SED-only, unresolved |
| `disk_dust_temperature_k` | 55 ± 5 | high | Eiroa 2013 + Lawler & Tanner 2014 SED fit both converge on T_d ≈ 55 K, modified-blackbody emissivity index β ≈ 0.8 |
| `disk_tint_rgb_hex` | `#3a2a18` (faint warm-grey, low opacity) | low | Tie-break: 55 K dust radiates in far-IR; visible-light tint is the scattered-light dust albedo guess (~0.1 grey-brown silicate/ice mix) since no resolved imaging exists |
| `disk_opacity` | 0.02 | low | Tie-break: optical depth τ ≈ 10⁻⁵ from L_d/L_★ ≈ 2×10⁻⁵ (Eiroa 2013); rendered as a very faint visual feature, just barely detectable in long exposures |
| `disk_morphology` | "single cold belt, modest dust mass, no asymmetries detected (unresolved)" | medium | Lawler & Tanner 2014 — one belt fits the SED; no second-belt component needed; spatially unresolved so morphological detail is inferred |
| `disk_resolved_imaging` | false | high | Eiroa 2013 / Lawler 2014 both note Herschel PSF (~5″ at 70 µm) does not resolve the belt at 6.1 pc (expected angular extent ~5–13″); no ALMA / JWST resolved imaging as of 2026 |
| `disk_imaging_observatory` | "Herschel-PACS (SED only)" | high | Eiroa 2013 DUNES survey + Lawler 2014 follow-up; Spitzer/MIPS for original detection |
| `disk_mass_mearth` | 0.012 | medium | Lawler & Tanner 2014 dust mass (mm-cm grains); planetesimal parent body mass not directly constrained but inferred ≫ dust mass |
| `disk_planetesimal_belt_inferred` | true | high | Age ~7 Gyr ≫ collisional cascade lifetime of µm-cm dust at 50 AU; replenishment requires a planetesimal reservoir (Wyatt 2008 framework, applied in Lawler & Tanner 2014) |

## Surface synthesis

δ Pavonis sits in the brief but visually consequential subgiant
phase: core hydrogen has been exhausted, a thin hydrogen-burning
shell is beginning to inflate the envelope, and the star is climbing
the subgiant branch toward the base of the red-giant branch. The
result is a photosphere ~20% larger and ~200 K cooler than a G8V
dwarf would be at the same mass. The Stefan–Boltzmann luminosity of
1.20 L☉ — slightly higher than its G8V analogs because the radius
gain outpaces the temperature drop — gives the star a paradoxical
character: redder than the Sun in color, but still slightly brighter.

The integrated disk color shifts noticeably toward amber-cream
compared to a G2V Sun. At Teff = 5604 K the blackbody peak sits near
518 nm — yellow-green still, but the slope across visible
wavelengths is shallower than a G2V, with more red and less blue
than Sol. Compounded by the +0.33 dex super-solar metallicity (which
reddens the visible continuum by ~30 K equivalent via line
blanketing), the cfg tint `#ffe8c8` captures the warmer cream of an
evolved G8 star. The contrast with α Cen A's `#fff4e8` (a G2V at
5847 K) is real and visible in side-by-side renders.

Limb darkening is stronger than for a G2V because the cooler, more
extended atmosphere has a longer photon mean-free-path near the
limb. The H-band α exponent of ≈0.16 (Claret 2011 LD tables
interpolated to G8IV) is ~15% higher than α Cen A's measured 0.14 —
a subtle but real visual effect in fly-by renders, with the limb
appearing distinctly more shadowed than for a G2V dwarf.

Spot coverage is modest. Without a measured rotation period or
cycle, photometric variability constraints are loose (Hipparcos
H_p amplitude < 0.005 mag), but log R'HK = -5.10 (Henry 1996)
places δ Pav firmly in the inactive G subgiant locus — quieter than
α Cen A, comparable to the most magnetically dead stars in the
Mt. Wilson sample. For the cfg renderer, spot density is set to
half the solar-maximum value and randomly distributed, with no
strong cycle modulation.

## Atmosphere synthesis

δ Pav's chromosphere and corona are correspondingly weak. The
chromospheric Ca II H&K core flux of log R'HK = -5.10 (Henry 1996;
Gray 2006 NStars) lies near the chromospheric "basal flux floor"
where no further activity decline is observed — δ Pav is essentially
at the magnetic-quiescence asymptote for its evolutionary stage.
The ROSAT non-detection (Hünsch 1998) places log L_X < 26.6 (cgs,
0.5–2 keV) — an order of magnitude weaker than Sol at activity
minimum, and consistent with the gravitational and convective
weakening expected as a star expands off the main sequence.

The transition region UV emission is correspondingly faint, but δ
Pav has been observed by IUE and HST/STIS, with Mg II h&k and Si IV
emission lines detected at weak but non-zero intensity. No measured
flares — δ Pav is among the most flare-quiet stars in the local
sample, with no events reported in any monitoring campaign.
Integrated XUV luminosity is ≲ 10⁻⁵ L_bol, well below thresholds
that would erode atmospheres on candidate inner planets even over
the full 7 Gyr age of the system.

The benign space-weather state has interesting implications for any
hypothetical (currently unconfirmed) planet: at δ Pav's habitable
zone — roughly 1.0–1.7 AU based on Kopparapu 2013 conservative
limits scaled to 1.20 L☉ — XUV-driven atmospheric escape would be
negligible across the system's full lifetime. The cfg encodes a
benign stellar-wind environment with no significant CME flux for
in-game atmospheric retention modeling.

The stellar atmosphere itself, at the photosphere, shows the
canonical G8IV temperature inversion at the chromospheric onset:
T drops from 5604 K at τ=1 to a temperature minimum near 4200 K
around τ ≈ 10⁻⁴, then rises through the chromosphere to ~10⁴ K and
the transition region to ~10⁵ K. The cool temperature minimum is
deeper and broader than in G2V Sol, characteristic of the lower
acoustic flux from the larger, slower-convecting envelope.

## Rotation & spin synthesis

δ Pavonis rotates slowly — exactly how slowly is poorly determined.
The projected rotational velocity v sin i ≈ 1.7 km/s (Bensby 2014;
Valenti & Fischer 2005 give similar values from HARPS / Keck spectra)
combined with R = 1.22 R☉ gives an *upper limit* on rotational
velocity of 2π·R/P_rot ≥ 1.7 km/s, implying P_rot · sin i ≤ 36 d.
Without an inclination constraint the period is bounded only from
above; for i = 90° (equator-on) P_rot ≤ 36 d, and for typical random
inclinations the most probable period is ~30 d.

Skumanich braking applied from a G8V zero-age main-sequence
rotation of ~5 d, scaled to 7 Gyr by P ∝ √t, predicts ~50 d — but
the subgiant expansion further slows the surface rotation by angular
momentum conservation as the envelope inflates. The Spada & Lanzafame
2020 subgiant rotation models predict 30–45 d at this evolutionary
stage for an initial main-sequence rotation period of 25–35 d. The
cfg adopts 30 d as a within-window estimate, flagged Confidence=low,
and notes the open item for future photometric monitoring.

No direct asteroseismic detection of rotation splitting exists; the
Bruntt 2010 ground-based campaign detected p-mode oscillations
(ν_max ≈ 2300 µHz, Δν ≈ 110 µHz, consistent with M ≈ 1.05 M☉ and
R ≈ 1.22 R☉) but the data quality was insufficient to resolve
rotational splittings of the modes. A future TESS or PLATO campaign
would tighten this; the cfg open items log the dependency.

Obliquity is unconstrained observationally. For an isolated single
star with no companion to torque the spin axis, default to obliquity
= 0° relative to the spin angular momentum reference frame; the cfg
encodes 0° as a within-window default with no special tilt for
visual flair.

## Visual styling

In the NearStars renderer, δ Pavonis is portrayed as an old,
quiet G8 subgiant viewed against a faint cold debris ring. Key
visual choices:

- **Global appearance** — a warm amber-cream stellar disk
  (`#ffe8c8`), distinctly redder than the cream-white of α Cen A
  but warmer in tint than a K-dwarf orange. Side-by-side with G2V
  Sol the contrast is subtle but real; alone in a planet sky δ Pav
  reads as "a tired Sun, slightly redder, slightly larger."
- **Disk detail** — at a hypothetical close-fly-by render, the
  photospheric granulation is rendered with ~5% lower contrast than
  G2V because the larger, slower-convecting envelope produces
  shallower temperature differentials between hot rising plumes and
  cool intergranular lanes. Granulation cells are ~30% larger in
  angular size (scaled by R*).
- **Limb appearance** — visibly more darkened toward the limb than
  α Cen A, due to the cooler photosphere and stronger H⁻ opacity at
  oblique viewing angles. The limb appears noticeably shadowed in
  fly-by renders.
- **Corona / chromosphere** — rendered as a thin, faint ring at
  1.6 R★ (`visual_corona_extent_radii`), reflecting the very weak
  chromospheric and coronal emission. No active prominence
  rendering; no flare visual.
- **Spots / faculae** — set to half the solar-minimum amplitude,
  randomly distributed at low latitudes, with no cycle modulation
  in the current cfg.
- **Cold debris ring** — at 30–80 AU from the star, the cfg
  attaches a Kopernicus ring with very low opacity (0.02) and a
  faint warm-grey tint (`#3a2a18`). The ring is just barely visible
  in long-exposure renders from the inner system; from a candidate
  planet at 1.3 AU the ring would appear as a thin band of dust
  reflected sunlight, far fainter than the Zodiacal light at Earth.
  The morphology is rendered as a single uniform belt because
  Herschel did not resolve the belt and the SED supports a single
  cold component; if future ALMA / JWST imaging reveals
  asymmetries or multiple components, this picks would be revisited
  (see Open items).
- **Apparent diameter from candidate HZ** — a hypothetical 1 M⊕
  planet at 1.3 AU would see δ Pav fill ~0.50° angular diameter,
  comparable to Sol from Earth (0.53°).
- **Sky from disk** — a hypothetical observer at the inner edge of
  the debris belt (~30 AU) would see δ Pav as a brilliant
  amber-cream point of 1.2/(30)² = 1.3×10⁻³ L☉/AU² illumination,
  i.e. about 1/770 of Sol-at-Earth — clearly star-like, casting
  long shadows but not solar-bright. The inner zodiacal-dust
  scattering plus the outer belt would create a faint band of
  light along the ecliptic.
- **Isolation cue** — unlike the α Cen system's binary-pair
  rendering, δ Pav stands alone. No second sun, no orbital
  conjunction events. The visual styling leans on the disk and the
  subgiant color to give the star personality.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Eiroa C. et al. 2013** — *DUNES: Disc Around NEarby Stars with
  Herschel*, A&A 555, A11 (`2013A&A...555A..11E`, arXiv:1305.0155).
  Herschel/PACS survey of 133 nearby FGK stars; δ Pavonis detected
  at 70/100/160 µm; SED fit gives single cold belt at T_d ≈ 55 K
  with L_d/L_★ ≈ 2×10⁻⁵.
- **Lawler S. M. & Tanner A. M. 2014** — *Tracing planet formation
  with detailed analysis of debris disk SEDs* (`2014ApJ...780...28L`,
  arXiv:1310.3559). Modified-blackbody analysis of Eiroa 2013 data
  including δ Pav; refined belt geometry r ≈ 30–80 AU, dust mass
  ~0.012 M⊕, planetesimal-replenishment requirement from age
  argument.
- **Beichman C. A. et al. 2006** — *New Debris Disks around Nearby
  Main-Sequence Stars: Impact on the Direct Detection of Planets*
  (`2006ApJ...652.1674B`). Spitzer/MIPS 70 µm detection of δ Pav
  excess; first announcement of the disk.
- **Gomes da Silva J. et al. 2021** — *Chromospheric activity of FGK
  stars observed with HARPS* (`2021A&A...646A..77G`,
  doi:10.1051/0004-6361/202039765). AMBRE-HARPS Teff = 5644 ± 30 K,
  [Fe/H] = +0.36 ± 0.02, log R'HK = −5.13 (weighted mean of 6002
  HARPS spectra), PARSEC isochrone mass = 1.064 ± 0.013 M☉, radius =
  1.115 ± 0.025 R☉, age = 5.04 ± 1.23 Gyr. **Primary Phase 2 anchor
  for δ Pav** (newest paper, smallest uncertainties, homogeneous
  treatment); supersedes the older Bensby 2014 / Bruntt 2010 picks
  used in an earlier draft of this synthesis.
- **Eiroa C. et al. 2013** — *DUNES: DUst around NEarby Stars*
  (`2013A&A...555A..11E`, doi:10.1051/0004-6361/201321050).
  Herschel/PACS 70/100/160 µm photometry of δ Pav and 132 nearby FGK
  stars; bolometric L = 1.246 L☉, Ca II activity age 8.3 Gyr (the
  older end of the literature spread), v sin i upper limit 3.2 km/s
  (superseded by Ramirez 2013). Also the primary disk-detection
  source — see `disks_curated`.
- **Ramirez I. et al. 2013** — *The dissimilar chemical composition
  of the planet-hosting stars of the XO-2 binary system*
  (`2013ApJ...764...78R`, doi:10.1088/0004-637X/764/1/78).
  HARPS solar-twin-precision v sin i = 0.32 ± 0.05 km/s for δ Pav at
  the instrumental floor; sets the modern P_rot upper-bound
  derivation in the Rotation row. Also high-res Teff = 5517 ± 60 K,
  [Fe/H] = +0.33 ± 0.07, evolutionary-model mass 0.98 ± 0.02 M☉
  (all kept as cross-check alternates).
- **Tsantaki M. et al. 2013** — *Deriving precise parameters for
  cool solar-type stars: optimizing the iron line list*
  (`2013A&A...555A.150T`, doi:10.1051/0004-6361/201321103).
  Homogeneous high-res spectroscopy: Teff = 5566 ± 36 K, [Fe/H] =
  +0.32 ± 0.03, mass 0.967 ± 0.016 M☉, age 8.48 ± 1.27 Gyr — the
  ~9 Gyr end of the age literature spread.
- **Bensby T. et al. 2014** — *Exploring the Milky Way stellar disk:
  A detailed elemental abundance study of 714 F and G dwarf stars*
  (`2014A&A...562A..71B`, arXiv:1309.2631). FEROS high-resolution
  spectroscopy gives Teff = 5635 ± 122 K, log g = 4.05, [Fe/H] =
  +0.37 ± 0.20, mass 1.03 ± 0.07 M☉ (evolutionary), age 4.9 Gyr —
  cross-check alternate; Gomes da Silva 2021 supersedes for primary
  pick (tighter formal uncertainties on the same quantities).

### Read (context / methodology, not directly decision-driving)

- **Mawet D. et al. 2017** — *Characterization of Exoplanets from
  Their Formation. I.* (`2017AJ....153...44M`, arXiv:1609.06163).
  NIRC2 vortex coronagraph deep imaging of δ Pav and other nearby
  FGK stars; companion mass limits ~3 M_Jup at >1 AU; confirms no
  giant planets in the cold disk inner region.
- **Lannier J. et al. 2017** — *Combining direct imaging and radial
  velocity data toward a full exploration of the giant planet
  population* (`2017A&A...603A..54L`, arXiv:1705.03477). δ Pav
  included in SPHERE direct-imaging survey; no companions
  detected.
- **Tinney C. G. et al. 2005** — *The Anglo-Australian Planet
  Search. XI. Five Planets and a Brown Dwarf* (`2005ApJ...623L.121T`).
  HARPS / AAPS RV monitoring of δ Pav; no planet detection above
  m sin i ~ 10 M⊕ at <2 AU; sets the RV non-detection baseline.
- **Bruntt H. et al. 2010** — *Accurate fundamental parameters for
  23 bright solar-type stars* (`2010MNRAS.405.1907B`,
  arXiv:1002.4268). Quotes R ≈ 1.22 R☉ for δ Pav derived from
  bolometric L + Teff via Stefan-Boltzmann with the Hipparcos-era
  parallax — **not** an interferometric or asteroseismic measurement
  (δ Pav has no published asteroseismology, and the southern
  declination keeps it out of CHARA). Cited here for historical
  context; the value diverges by ~9% from the modern Gomes da Silva
  2021 PARSEC R = 1.115 R☉ recommended in the Decisions table above.
  Earlier drafts of this synthesis attributed Bruntt 2010 as
  "interferometric + asteroseismic" — that attribution was incorrect
  and is corrected here.
- **Henry T. J. et al. 1996** — *Chromospheric Activity Survey* in
  the southern hemisphere (`1996AJ....111..439H`). Log R'HK =
  -5.10 for δ Pav, one of the most chromospherically quiet G
  subgiants in the local sample.
- **Hünsch M. et al. 1998** — *ROSAT All-Sky Survey of nearby
  stars* (`1998A&AS..132..155H`). δ Pav X-ray non-detection with
  upper limit log L_X < 26.6 cgs.
- **Gray R. O. et al. 2006** — *NStars: Spectral Classifications of
  Nearby Stars* (`2006AJ....132..161G`, arXiv:astro-ph/0603770).
  Confirms G8IV classification and log R'HK = -5.10.
- **Valenti J. A. & Fischer D. A. 2005** — *Spectroscopic
  Properties of Cool Stars (SPOCS)* (`2005ApJS..159..141V`). v sin
  i and chromospheric measurements; supports Bensby 2014.

### Read (instrument / non-cfg-decisive)

- **Trilling D. E. et al. 2008** — *Debris Disks around Sun-like
  Stars* (`2008ApJ...674.1086T`). Spitzer 24/70 µm survey
  including δ Pav; context for the disk detection census.
- **Spada F. & Lanzafame A. C. 2020** — *Asteroseismic rotation
  for subgiants* (`2020A&A...636A..76S`, arXiv:2003.06224). Sets
  the rotation-period model floor for δ Pav-class subgiants used
  in the Rotation & spin synthesis.
- **Kopparapu R. K. et al. 2013** — *Habitable Zones around
  Main-Sequence Stars: New Estimates* (`2013ApJ...765..131K`).
  HZ limits scaled to 1.20 L☉ give 1.0–1.7 AU conservative
  range — used in the Atmosphere synthesis prose.

### Not read — no arXiv preprint or low-priority (~25 papers)

Conference abstracts (DPS, EPSC, AAS), follow-up notes on the
disk SED with no new data (~12 follow-up references), and one-line
catalog mentions in survey papers contribute no cfg-decisive
content. Mt. Wilson HK survey notes (Wright 2004) confirm the
log R'HK floor but add no new constraint beyond Henry 1996. The
full filtered bib will be preserved in
`docs/phase3/_bib/delta-pavonis.yaml` with `status: skipped`
annotations once the bib retrieval pipeline runs for this star
(currently pending — see Open items).

## Open items for follow-up

- **Phase 2 `disk_measurements` ingest**. The DB `delta_pavonis.json`
  currently has no `disk_measurements` block; the Herschel/PACS
  fluxes (Eiroa 2013), Lawler & Tanner 2014 SED-fit geometry, and
  Spitzer 70 µm excess (Beichman 2006) should be ingested as
  paper-cited Phase 2 measurements before this synthesis is
  promoted from Confidence=medium on the disk geometry rows.
- **Resolved imaging (ALMA / JWST-MIRI)**. The 30–80 AU belt at
  6.1 pc spans ~5–13″ on the sky — well within ALMA's 1″
  angular resolution at Band 6, and just inside MIRI's coronagraph
  inner working angle. A resolved-imaging campaign would tighten
  inner/outer radius, detect any belt asymmetries or warps (which
  would imply unseen planetary perturbers), and constrain
  inclination. Confidence on disk geometry would rise to high.
- **Subgiant age refinement**. The 7.0 ± 0.5 Gyr age rests on
  isochrones (Holmberg 2009) and one-parameter subgiant models
  (Spada 2011). PLATO-class asteroseismology, when it observes δ
  Pav, would resolve the p-mode rotation splitting and tighten the
  age to ~5%. The cfg `age_gyr` Confidence would rise from medium
  to high.
- **Photometric rotation period**. TESS Cycle 4+ should observe δ
  Pav (declination favorable for the southern continuous viewing
  zone); a clean rotation-period detection would replace the
  current Confidence=low estimate.
- **`docs/phase3/_bib/delta-pavonis.yaml` bib retrieval**. The
  bibliography YAML has not been generated by the ADS+arXiv
  pipeline yet — run after the DB Phase 2 disk ingest is
  complete so the disk papers are included in the score-ranked
  output.

## Related

- [methodology](../reference/methodology.md) — schema source for the Decisions table
- [alpha-centauri-a](alpha-centauri-a.md) — G2V comparison anchor (cream-white at 5847 K vs δ Pav's amber-cream at 5604 K)
- [conflict-resolution](../../.claude/skills/nearstars-phase3/references/conflict-resolution.md) — tie-break policy used for visual tint and corona extent picks
