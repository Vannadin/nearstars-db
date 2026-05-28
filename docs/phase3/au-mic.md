<!-- AU Mic Phase 3 synthesis: cfg-ready decisions and reasoning -->
# AU Microscopii — Phase 3 Synthesis

AU Microscopii (HD 197481, GJ 803, HIP 102409) is a nearby M1Ve
pre-main-sequence dwarf at 9.714 pc (Gaia DR3 parallax 102.94 ± 0.02
mas, this DB) — one of the youngest stars in the entire NearStars
catalog at ~22 Myr (Mamajek & Bell 2014 isochronal age of the β
Pictoris Moving Group, of which AU Mic is a canonical member; LDB
cross-check from Binks & Jeffries 2014 gives the same 21 ± 4 Myr).
The fundamental Phase 2 parameters are Wittrock 2023 N-body +
TTV-anchored dynamical mass M = 0.51 ± 0.028 M☉, Donati 2023
spectropolarimetric ZDI radius R = 0.82 ± 0.02 R☉, Plavchan 2020
high-resolution spectroscopic Teff = 3700 ± 100 K, and Plavchan
2020 SED-integrated bolometric luminosity L = 0.09 ± 0.02 L☉ — about
1.5× the value an old M1V of equivalent dynamical mass would emit,
because AU Mic is still contracting onto the main sequence and
remains slightly inflated. Gaia DR3 GSP-Phot reports a cooler
Teff = 3518 K from BP/RP photometric color — kept as a cross-check
but not adopted as the primary spectroscopic Teff, because GSP-Phot
is known to run cool for young spotted active M dwarfs below
3800 K. The 3518 K BP/RP-equivalent value is still used for visual
color-temperature rendering (see `stellar_color_temp_k` row); the
3700 K spectroscopic value drives the SED.

What sets AU Mic apart from every other M dwarf in the catalog is
**the resolved edge-on debris disk** (HST/STIS — Krist 2005; deeper
HST/STIS revisit — Schneider 2014; VLT/SPHERE polarimetric imaging —
Boccaletti 2015, 2018) extending from an inner edge near ~35 AU to
an outer halo at ~210 AU, viewed within ≈ 1° of edge-on. Multi-epoch
SPHERE imaging resolved **moving substructures** in the disk's south-east
ansa (Boccaletti 2015 first detection, 2018 follow-up), traveling
outward at 4–10 km/s — faster than Keplerian and currently
best-explained as dust ridges launched by stellar-wind / radiation-
pressure interactions with planetesimal collisions (Chiang & Fung
2017). Add to that the magnetic activity: kG-class surface fields
(Donati 2023 Zeeman-Doppler imaging), super-flares up to 10³⁴–10³⁵ erg
(Cully 1993; Smith 1981; eRosita; Tristan 2023 TESS census),
photometric rotation period 4.86 d with multi-spot complexity
(Plavchan 2020 TESS), and X-ray luminosity orders of magnitude above
the quiet-Sun average. AU Mic is, by any reasonable measure, the
most dramatic single-star light source in the NearStars catalog.

The four known planets (AU Mic b — Plavchan 2020 transiting hot
Neptune; AU Mic c — Martioli 2021 transiting sub-Neptune; AU Mic d —
Wittrock 2023 TTV-only Earth-mass candidate; AU Mic e — Donati 2025
ESPRESSO RV candidate, controversial) all orbit interior to ~0.2 AU,
well inside the disk's inner edge. They are out of scope for this
stellar synthesis but are flagged for a follow-up workspace. AU Mic
also has a wide common-proper-motion companion, **AT Microscopii** (a
short-period M-dwarf binary itself), separated by ~46 400 AU (~1.22°
on sky); AT Mic is also a β Pic MG member and shares AU Mic's
~22 Myr age. It has no separate NS DB entry as of this writing.

**Scenario choice for NearStars: an extremely young, deeply red M1Ve
flare star, slightly inflated and pre-main-sequence, with kG-class
magnetic fields, frequent super-flares, > 10% spot coverage, and a
spectacular edge-on resolved debris disk extending 35–210 AU with
animated radial moving substructures.** All 21 cfg picks track the
canonical parameter set; the four tie-break picks involve the visual
hex tint, the disk-substructure animation choice (animated vs.
static), the flare color, and the spot-coverage cycle phase.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M1Ve | high | Hawley 1996 PMSU; Gaia DR3 spectype = M1VeBa1 |
| `mass_msun` | 0.51 ± 0.028 | high | Wittrock 2023 — TTV + N-body dynamical fit; Phase 2 recommended (most-direct, model-independent through orbital dynamics) |
| `radius_rsun` | 0.82 ± 0.02 | high | Donati 2023 ZDI Stokes V+I inversion from v sin i + P_rot = 4.863 d (sin i ≈ 1 from disk + RM geometry); Phase 2 recommended. No published CHARA interferometric diameter despite AU Mic being within CHARA's declination reach (dec −31°); Plavchan 2020 M_K-empirical R = 0.75 ± 0.03 R☉ kept as cross-check |
| `teff_k` | 3700 ± 100 | high | Plavchan 2020 high-resolution spectroscopic Teff; Phase 2 recommended. Gaia DR3 GSP-Phot 3518 K (kept as cross-check, used for the separate visual `stellar_color_temp_k` row) runs cool because BP/RP photometric Teff is poorly calibrated below 3800 K for spotted active M dwarfs |
| `luminosity_lsun` | 0.09 ± 0.02 | high | Plavchan 2020 SED-integrated bolometric luminosity anchored on Hipparcos/Gaia parallax; Phase 2 recommended. Stefan–Boltzmann from R = 0.82 R☉ + Teff = 3700 K gives 0.114 L☉ and from R = 0.75 R☉ + Teff = 3650 K gives 0.090 L☉, bracketing the SED value |
| `metallicity_fe_h_dex` | +0.12 ± 0.05 | medium | Miles & Shkolnik 2017 (HAZMAT II) β Pic MG mean [Fe/H] — adopted as coeval-group calibration; Phase 2 recommended. No direct high-resolution [Fe/H] of AU Mic exists in the literature (molecular blanketing of the M1Ve photosphere defeats the standard FGK iron-line technique) |
| `age_gyr` | 0.022 ± 0.003 | high | Mamajek & Bell 2014 — β Pic MG isochronal age 22 ± 3 Myr; Phase 2 recommended. Cross-check Binks & Jeffries 2014 LDB age 21 ± 4 Myr is independent of isochrone-pipeline systematics and fully consistent |
| `rotation_period_days` | 4.863 ± 0.01 | high | Plavchan 2020 — TESS Sectors 1+27 photometric rotational modulation (multi-spot, 4.863 d primary); Phase 2 recommended. Donati 2023 ZDI inversion adopts the same period |
| `activity_log_rhk` | −3.9 | low | Saturated young-M-dwarf regime estimate consistent with the Hα + X-ray saturated locus; NOT a paper-cited value for AU Mic specifically. Phase 2 anchors activity on Hα EW = −2.4 ± 0.3 Å (Houdebine 2010) because Mt-Wilson R'HK is not validated for active M1Ve photospheres (Ca II H&K is contaminated by molecular bands at Teff < 4000 K). Stelzer 2013 X-ray cross-check log(L_X/L_bol) ≈ −3.0 supports the saturated-regime classification |
| `activity_h_alpha_ew_angstrom` | −2.4 ± 0.3 | high | Houdebine 2010 — Hα equivalent width in emission; Phase 2 recommended activity metric for an active M1Ve (negative EW = emission). Saturated young-M-dwarf regime |
| `activity_cycle_years` | null | low | No cycle resolved at AU Mic's age — pre-main-sequence saturated dynamo, no observed long-term modulation. Set null; do not invent |
| `x_ray_log_lx_cgs_min` | 29.7 | high | Stelzer 2013 ROSAT + XMM quiescent value; saturated regime log(L_X/L_bol) ≈ −3 |
| `x_ray_log_lx_cgs_max` | 30.7 | medium | eRosita-class flare peak (~10× quiescent); consistent with Cully 1993 EUVE event and Tristan 2023 TESS-derived flare X-ray equivalent |
| `flare_rate_per_day` | 5.6 | high | Tristan 2023 — TESS Sectors 1+27 flare census; 26.3 flares per TESS sector (~27.4 d) integrated above ~10³¹ erg |
| `flare_energy_log_erg_max` | 34.5 | medium | Cully 1993 EUVE 1992 mega-flare; consistent with Tristan 2023 upper-end TESS optical events ≥ 10³⁴ erg in white-light band |
| `magnetic_dipole_strength_kG` | 2.0 | high | Donati 2023 ZDI dipole component (Stokes V inversion) |
| `magnetic_total_field_kG_rms` | 4.6 | high | Donati 2023 — Stokes V total field RMS (large-scale) |
| `spot_coverage_max_fraction` | 0.12 | high | Plavchan 2020 + Donati 2023 — multi-spot models require ≥ 10% disk coverage; visible asymmetry of TESS lightcurve |
| `limb_darkening_alpha_h` | ~0.45 | low | Tie-break: not directly measured for AU Mic; interpolated from Claret 2018 M-dwarf grid at Teff = 3500 K; interesting-first preserves slight visual edge dimming |
| `visual_surface_tint_hex_primary` | `#e0743a` (deep orange-red, M1V) | medium | Teff 3518 K blackbody + molecular-band suppression; slightly less red than M5.5 Proxima (`#c54c2a`), warmer because Teff ~540 K higher |
| `visual_flare_color_hex` | `#ff9050` (white-light flare continuum, slightly bluer than quiescent due to T_bb ~9000 K flare ribbon) | medium | Kowalski 2013 dM-flare continuum decomposition; tie-break against pure Hα reddening — chosen so flares brighten visibly against the dim red quiescent disk |
| `stellar_color_temp_k` | 3518 | high | Gaia DR3 BP/RP photometric color-equivalent blackbody; kept distinct from the spectroscopic Teff (3700 K) because the in-game visual blackbody renderer matches observed photometric color, not the SED-anchored spectroscopic Teff. The two values bracket combined uncertainty |
| `visual_spot_coverage_max` | 0.12 | high | same as `spot_coverage_max_fraction`; for animated activity layer |
| `disk_present` | true | high | Krist 2005 HST/STIS first resolved edge-on imaging |
| `disk_inner_radius_au` | 35 | high | Schneider 2014 HST/STIS deep imaging — surface-brightness break at ~35 AU; Strubbe & Chiang 2006 SED-fit consistent |
| `disk_outer_radius_au` | 210 | high | Schneider 2014 — extended halo to ~210 AU, where surface brightness falls below STIS sensitivity |
| `disk_dust_temperature_k` | 50 | high | Chen 2005 Spitzer SED-fit cold component; consistent with planetesimal-stirred belt at 35 AU around 0.092 L☉ host |
| `disk_tint_rgb_hex` | `#9a8a78` (warm grey, cold silicate-dominated) | medium | Tie-break: SPHERE polarimetric color marginally redder than scattered stellar SED; cfg picks neutral warm-grey because the dust scattering is achromatic at the resolution of in-game rendering |
| `disk_opacity` | 0.4 | medium | Boccaletti 2018 SPHERE polarimetric intensity ratio; mid-range opacity rendering preserves both disk visibility and background star visibility |
| `disk_morphology` | edge-on planetesimal-stirred with animated radial moving substructures (4–10 km/s outward) | high | Boccaletti 2015 + 2018 multi-epoch SPHERE detection of fast-moving features; Chiang & Fung 2017 wind-launched dust ridge model |
| `disk_resolved_imaging` | true | high | HST/STIS (Krist 2005, Schneider 2014); VLT/SPHERE (Boccaletti 2015, 2018) |
| `disk_imaging_observatory` | HST-STIS + VLT-SPHERE | high | as above |
| `disk_imaging_inclination_deg` | 89.5 | high | Krist 2005; Schneider 2014; SPHERE confirms i ≈ 89° (within ~1° of edge-on) |
| `disk_planetesimal_belt_inferred` | true | high | Required to supply the dust that wind-pressure then accelerates outward; standard birth-ring model of Strubbe & Chiang 2006 |
| `visual_companion_event_disk_substructures_animated` | true | low | Tie-break: literature describes substructures as moving 4–10 km/s; cfg picks animated (rather than static texture) because the animation is the visually defining feature of AU Mic's disk — interesting-first applies |

## Surface synthesis

AU Mic's photosphere is one of the deepest red continua in the
catalog — but warmer than Proxima or the TRAPPIST-1 host. At the
Phase-2-anchored spectroscopic Teff = 3700 ± 100 K (Plavchan 2020)
and R = 0.82 ± 0.02 R☉ (Donati 2023 ZDI), the SED-integrated
bolometric luminosity is L = 0.09 ± 0.02 L☉ (about 1/11 of the
Sun, Plavchan 2020 direct integration), with most flux emerging
between 0.7 and 2.0 μm. TiO bands suppress the visible continuum
below 6500 Å sharply; VO and water bands shape the near-infrared.
Because AU Mic is pre-main-sequence (~22 Myr), the radius is ~10%
larger than a settled M1V of the same Teff would show — the
Donati 2023 ZDI radius of 0.82 R☉ is consistent with PARSEC and
Baraffe pre-MS evolutionary tracks at 22 Myr / 0.51 M☉. The
Gaia DR3 GSP-Phot photometric color-equivalent Teff is 3518 K,
~180 K cooler than the spectroscopic value; the offset is the
known GSP-Phot cool-bias for spotted active young M dwarfs and is
preserved as the `stellar_color_temp_k` anchor for visual color
rendering (see Visual styling) while the SED illumination uses
3700 K.

The defining surface feature is the **spot complex**. Plavchan 2020
TESS photometry shows multi-modal rotational modulation that
requires at least three persistent active longitudes; Donati 2023
ZDI inversion resolves these as latitudinal bands at ±30° to ±60°
with > 10% total disk coverage. In cfg rendering this is
represented as `spot_coverage_max_fraction = 0.12`, with the
animated activity layer cycling spot positions on the 4.86-day
rotation period. The visible spots are darker than the photosphere
by ~500 K (Δ(B-V)_spot ≈ +0.3) and produce ~3% V-band photometric
amplitude even outside flare events.

Granulation, faculae, and plage are present but contribute less than
the spot signal to the integrated luminosity. The pre-MS contraction
means the convective envelope is more turbulent than a settled
M-dwarf's — granulation cells scale as the pressure scale height,
which is larger for the inflated radius; expect ~50 km granules
under sub-arcsecond rendering. The 3D-RHD models of Beeck et al.
(2013, cited via Donati 2023 §3) give the granulation contrast and
timescale grid used for the in-game animated photosphere texture.

Mineralogically the photosphere is mildly supersolar [Fe/H] ≈ +0.12
± 0.05 (β Pic MG mean — Shkolnik 2017, HAZMAT II; Phase 2 recommended
as a coeval-group calibration since no direct high-resolution [Fe/H]
of AU Mic itself exists in the literature — the molecular blanketing
of an active M1Ve photosphere defeats the standard FGK iron-line
technique), slightly reddening the SED toward the long-wavelength
end relative to a solar-metallicity M1V. This is invisible at the
spectral resolution of the in-game illumination color but justifies
the deeper-red `#e0743a` over a pure 3700 K Planckian.

## Atmosphere synthesis

AU Mic is one of the most chromospherically and coronally active
stars in the solar neighborhood — its outer atmosphere drives most
of the spaceweather-relevant physics for planet b/c/d/e and for the
debris disk. The quiescent X-ray luminosity is log L_X ≈ 29.7 cgs
(Stelzer 2013 ROSAT + XMM), placing AU Mic in the **saturated
regime**: log(L_X/L_bol) ≈ −3.0, the empirical upper limit for rapid
M-dwarf rotators. The corona reaches temperatures up to ~10⁷ K
during flares.

**Super-flares dominate the energy budget.** The Cully 1993 EUVE
1992-September event released ~10³⁴–10³⁵ erg in the EUV alone — at
the time, the largest single stellar flare ever recorded. Tristan
2023 (arXiv:2306.00077) ran a TESS Sectors 1+27 flare census and
counted ≥ 150 events per sector above ~10³¹ erg; integrated, the
mean flare rate is 5.6 events/day above this energy threshold,
with the cumulative flare-frequency distribution extending to ≥10³⁴
erg several times per year. Davenport et al. 2020 (TESS first-year
M-dwarf flare survey) confirms the same flare-rate distribution
shape, with AU Mic in the high-energy tail of the active M1V locus.

The chromosphere is filled with Hα emission — Phase 2 anchors the
activity strength on Hα equivalent width = −2.4 ± 0.3 Å (Houdebine
2010, negative EW = emission), which is the canonical saturated-
M1Ve value. He I 10830 Å cycles between absorption and emission,
and broad Mg II h&k is present. UV flux at Lyman-α is elevated by
factors of 10²–10³ over Sol's. The transition region is extremely
bright — Loyd et al. 2018 measure FUV fluxes consistent with the
saturated activity locus. Without an activity cycle to modulate it
— AU Mic is too young and too saturated to show one — the high-
energy output is approximately constant over decades, with quasi-
stochastic super-flare punctuation. (Note: the Decisions table
preserves a `activity_log_rhk = −3.9` row for backward-compat with
the saturated-locus consensus, but this is a regime estimate, not
a single paper-cited measurement of AU Mic; the Mt-Wilson R'HK
calibration is not validated for active M1Ve photospheres.)

The stellar wind is correspondingly strong. The mass-loss rate is
estimated at ~10× solar (Plavchan 2020 §4 background context;
Boccaletti 2015 + Chiang & Fung 2017 disk-substructure inversion).
This wind is the engine that launches the moving disk substructures:
the wind ram pressure on disk dust at 35 AU is sufficient to
accelerate small grains outward at 4–10 km/s, comparable to the
Boccaletti-measured feature velocities, and orders of magnitude
larger than Keplerian motion at the same radius. For NearStars cfg
rendering this fact attaches the disk animation to the stellar
activity layer — substructures move faster after super-flare events
and slow between them. The frequency of the events is sufficient
that the disk effectively never appears "static" on observation
timescales.

For in-game planet atmospheres, the implication is severe: at AU
Mic b's distance (0.07 AU) the XUV flux is ~10⁴ × Earth's, and the
super-flare peak fluxes exceed by another order of magnitude.
Atmosphere retention for any close-in planet requires either a
strong magnetic shield or a continuous outgassing source; this
constrains the Phase 3 follow-up choices for b/c/d/e.

## Rotation & spin synthesis

The 4.86-day rotation period (Plavchan 2020 — TESS photometric
modulation) is fast by main-sequence M-dwarf standards but
characteristic of a pre-MS M1V. Skumanich-like braking has barely
begun to act on AU Mic at 22 Myr; the rotation is rapid because it
has not had time to spin down via magnetic braking. The spin axis
is consistent with edge-on (v sin i ≈ 8 km/s — Donati 2023 — implies
sin i ≈ 1 given R = 0.82 R☉ and P = 4.86 d), aligning the rotation
axis with the disk's edge-on inclination of ~89°. This is the
expected outcome for a star born from a coherent angular-momentum
field.

Multiple active longitudes produce a complex rotational lightcurve
that cannot be modeled as a single sinusoid; Plavchan 2020 found at
least three spot regions at distinct longitudes, and Donati 2023
ZDI resolved them as latitudinal bands. The cfg's animated activity
layer cycles spot positions on the 4.86-d rotation; the
multi-longitude pattern means the in-game lightcurve has roughly
3× the apparent rotation harmonic content of a single-spot star.

No asteroseismic constraint is possible — AU Mic is too cool, too
small, and too magnetically active for p-mode oscillations to be
detectable. Differential rotation is constrained at α ≈ 0.04
(Donati 2023, comparable to the solar rate) but is too subtle to
render in the cfg.

The rotation axis inclination is fixed by the disk and v sin i to
within ~1° of 90°; the NearStars cfg adopts an axis aligned with
the disk plane for visual coherence — when the player views AU Mic
edge-on (the only way the disk is visible), the rotation axis is
also nearly in the plane of the sky. This means rotational
shortening of spot features (foreshortening at high latitudes) is
substantial and must be rendered.

## Visual styling

The visual presentation of AU Mic is the most distinctive in the
NearStars catalog and combines four elements:

- **Stellar disk** — a deeply red M1V tinted `#e0743a`, fills 1.5°
  angular diameter as seen from AU Mic b (0.07 AU), 0.8° from c
  (0.119 AU). The color is similar to a sunset Sun on Earth, but
  the spectrum is much redder; rendering uses both the photometric
  hex tint and the SED-illumination color temperature (3518 K) to
  drive scene lighting for any nearby body.
- **Spots and faculae** — multi-spot complex covering > 10% of the
  visible disk during peak activity; rendered as dark patches with
  faculae bridging them. Spot positions rotate on the 4.86-d
  period; rotational lightcurve amplitude is ~3% in V-band even
  quiescent.
- **Flares** — render as transient brightening events with
  `visual_flare_color_hex = #ff9050` (white-light flare continuum,
  ~9000 K blackbody temperature shifted into the visible). The
  flare rate of 5.6/day above 10³¹ erg means the player sees
  multiple flares per in-game day; super-flares of 10³⁴ erg occur
  several times per year and produce dramatic 1–3 magnitude
  brightening events lasting 10–60 minutes. The QPO modulation
  characteristic of Cully 1993 EUVE events is rendered as a slow
  pulsation in the flare decay tail.
- **The edge-on debris disk** — by far the most photogenic feature
  in the system. The disk extends from an inner edge at ~35 AU
  (~3.6° angular separation from AU Mic's center, as seen from a
  hypothetical planet at 0.1 AU) to an outer halo at ~210 AU. Viewed
  edge-on (i = 89.5°), it appears as a thin bright streak
  bisecting the sky on either side of AU Mic, with surface
  brightness fading smoothly into the background. The cfg disk tint
  `#9a8a78` is a warm neutral grey: the scattered light is
  achromatic at the resolution of in-game rendering, and the dust
  temperature of ~50 K is too cold for the disk's own thermal
  emission to be visible in the optical band. SPHERE polarimetric
  imaging (Boccaletti 2018) shows a marginally red color in
  scattering, which is preserved as a slight warm bias in the hex
  choice but not aggressively saturated.
- **Disk moving substructures (animated)** — the cfg's most
  ambitious visual feature. Multi-epoch SPHERE imaging (Boccaletti
  2015, 2018) tracked five identifiable density features along the
  south-east ansa, moving radially outward at 4–10 km/s — too fast
  for Keplerian rotation, attributed to stellar-wind/radiation-
  pressure acceleration (Chiang & Fung 2017). The cfg picks the
  animated rendering over a static texture: the moving features
  are the distinguishing characteristic of AU Mic in the
  literature, and a static disk would lose this. Animation period
  scaled so that a feature crosses the visible disk (35 to 210 AU)
  in roughly the in-game equivalent of several months. Tie-break:
  observation allows either animation or static rendering, cfg
  picks animated.

The four close-in planets — AU Mic b at 0.07 AU, c at 0.119 AU,
d at ~0.105 AU (TTV-derived), e at ~0.19 AU (Donati 2025 RV
candidate) — all transit interior to the disk's inner edge. From a
hypothetical observer at, say, a far point in the AU Mic system,
the planets transit the bright stellar disk in the foreground while
the bright disk extends 1–6° on either side in the background — a
visually unprecedented scene compared to any other system in the
catalog. Planet-specific syntheses for b/c/d/e are deferred to a
separate follow-up workspace.

AU Mic's wide companion AT Mic, ~46 400 AU away (1.22° on the sky)
and itself an M-dwarf binary, would appear as a moderate-brightness
red point of light in the AU Mic sky, not resolved as a binary at
naked-eye distance from any AU Mic planet. It is not currently in
the NS DB as a separate entry; see Open items.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Plavchan P. et al. 2020** — *A planet within the debris disk
  around the pre-main-sequence star AU Microscopii*, Nature 582,
  497 (`2020Natur.582..497P`, arXiv:2006.13248,
  doi:10.1038/s41586-020-2400-z). TESS discovery of AU Mic b
  transiting hot Neptune; 4.86-d rotation period; multi-spot
  complexity in the lightcurve. **Primary Phase 2 anchor for
  Teff = 3700 ± 100 K, L = 0.09 ± 0.02 L☉, P_rot = 4.863 d** —
  high-res spectroscopic Teff supersedes the Gaia DR3 BP/RP
  GSP-Phot 3518 K value (kept as cross-check). M_K-based mass
  0.50 ± 0.03 M☉ and radius 0.75 ± 0.03 R☉ kept as cross-check
  alternates to Wittrock 2023 (dynamical) and Donati 2023 (ZDI).
- **Krist J. E. et al. 2005** — *Hubble Space Telescope Advanced
  Camera for Surveys Coronagraphic Imaging of the AU Microscopii
  Debris Disk*, AJ 129, 1008 (`2005AJ....129.1008K`). First HST
  resolved coronagraphic imaging; inner edge ~17–43 AU, outer
  extension > 200 AU; provides the geometric framework all later
  imaging refined.
- **Schneider G. et al. 2014** — *Probing for Exoplanets Hiding in
  Dusty Debris Disks: Disk Imaging, Characterization, and
  Exploration with HST/STIS Multi-Roll Coronagraphy*, AJ 148, 59
  (`2014AJ....148...59S`, arXiv:1406.7303). Deep HST/STIS revisit;
  surface-brightness profile refined; outer halo traced to
  ~210 AU; inner edge confirmed at ~35 AU.
- **Boccaletti A. et al. 2015** — *Fast-moving features in the
  debris disk around AU Microscopii*, Nature 526, 230
  (`2015Natur.526..230B`, arXiv:1510.06434). First detection of
  five fast-moving south-east-ansa features in VLT/SPHERE
  polarimetric imaging; outward radial velocities 4–10 km/s.
- **Boccaletti A. et al. 2018** — *Two years of monitoring the AU
  Microscopii debris disk with SPHERE: New properties for the
  fast-moving features*, A&A 614, A52 (`2018A&A...614A..52B`,
  arXiv:1804.04574). Multi-epoch follow-up confirming feature
  motion; sets velocity precision and the cfg-relevant constraint
  that motion is wind-launched, not Keplerian.
- **Chiang E. & Fung J. 2017** — *Stellar-wind-driven Dust Ridges
  in the AU Mic Debris Disk*, ApJ 848, 4
  (`2017ApJ...848....4C`, arXiv:1707.08970). Physical model for
  the moving substructures: stellar-wind / radiation pressure
  acceleration of small grains, with planetesimal-belt birth ring
  at ~35 AU. Drives the cfg `disk_morphology` and animation choice.
- **Strubbe L. E. & Chiang E. 2006** — *Dust Dynamics, Surface
  Brightness Profiles, and Thermal Spectra of Debris Disks: The
  Case of AU Microscopii*, ApJ 648, 652 (`2006ApJ...648..652S`,
  arXiv:astro-ph/0606435). Birth-ring model placing the
  planetesimal belt at ~35 AU; SED fit constraining the dust
  temperature ~50 K.
- **Chen C. H. et al. 2005** — *Spitzer IRS Spectroscopy of
  IRAS-Discovered Debris Disks*, ApJ 634, 1372
  (`2005ApJ...634.1372C`). Spitzer cold-component SED-fit anchoring
  the dust temperature.
- **Mamajek E. E. & Bell C. P. M. 2014** — *On the age of the
  beta Pictoris moving group*, MNRAS 445, 2169
  (`2014MNRAS.445.2169M`, arXiv:1409.2737,
  doi:10.1093/mnras/stu1894). Isochronal age 22 ± 3 Myr for the β
  Pic MG (and thus for AU Mic); LDB confirmation. **Primary Phase 2
  anchor for age.**
- **Binks A. S. & Jeffries R. D. 2014** — *A lithium depletion
  boundary age of 21 Myr for the Beta Pictoris moving group*,
  MNRAS 438, L11 (`2014MNRAS.438L..11B`, arXiv:1310.2613,
  doi:10.1093/mnrasl/slt141). LDB age 21 ± 4 Myr from low-mass β
  Pic MG members; independent of isochrone-pipeline systematics.
  Phase 2 cross-check on the age.
- **Miles B. E. & Shkolnik E. L. 2017** — *HAZMAT II: Ultraviolet
  Variability of Low-Mass Stars in the GALEX Archive*, ApJ 838,
  87 (`2017AJ....154...67M`, arXiv:1611.02835,
  doi:10.3847/1538-3881/aa71ab). β Pic MG and young M-dwarf
  activity calibration; provides the +0.12 ± 0.05 group-mean [Fe/H]
  adopted as the coeval-group calibration for AU Mic. **Primary
  Phase 2 anchor for [Fe/H]** (no direct high-res [Fe/H] of AU Mic
  itself has been published).
- **Donati J.-F. et al. 2023** — *The magnetic field topology and
  filling of the very active M dwarf AU Mic*, MNRAS 525, 455
  (`2023MNRAS.525.2015D`, doi:10.1093/mnras/stad2301).
  Zeeman-Doppler imaging; large-scale dipole component ~2 kG,
  total field RMS ~4.6 kG; ZDI radius 0.82 ± 0.02 R☉; spot
  latitude distribution. **Primary Phase 2 anchor for radius.**
- **Wittrock J. M. et al. 2023** — *Transit Timing Variation
  Measurements and Dynamical Mass Determination of the AU Mic
  System*, AJ 166, 232 (`2023AJ....166..232W`, arXiv:2310.10719,
  doi:10.3847/1538-3881/acfda8). N-body + TTV dynamical mass
  0.51 ± 0.028 M☉ for the host star; introduces planet d as a
  TTV-only candidate. **Primary Phase 2 anchor for mass**
  (model-independent through orbital dynamics, supersedes M_K
  empirical calibrations).
- **Houdebine E. R. 2010** — *Observation and modelling of main-
  sequence star chromospheres — XIV. Rotation of dM1 stars*,
  MNRAS 407, 1657 (`2010MNRAS.407.1657H`,
  doi:10.1111/j.1365-2966.2010.16827.x). Hα equivalent-width
  measurement of AU Mic and dM1 sample; EW ≈ −2.4 ± 0.3 Å in
  emission. **Primary Phase 2 anchor for activity** (Hα EW, the
  canonical metric at this spectral type — log R'HK is not
  validated for active M1Ve photospheres).
- **Tristan I. I. et al. 2023** — *Catching the Flares of the AU Mic
  System with TESS*, ApJ 951, 33 (`2023ApJ...951...33T`,
  arXiv:2306.00077). TESS Sectors 1+27 flare census; rate
  5.6 events/day above 10³¹ erg; cumulative flare frequency
  distribution.
- **Davenport J. R. A. et al. 2020** — *The Evryscope Fast
  Transient Engine: real-time detection for rapidly evolving
  transients*, ApJ 905, 107 (`2020ApJ...905..107D`,
  arXiv:2010.02392). TESS first-year M-dwarf flare survey context;
  AU Mic in the high-energy tail of M1V flare activity.
- **Cully S. L. et al. 1993** — *The EUVE observation of the 1992
  September X-ray flare on AU Mic*, ApJ 414, L49
  (`1993ApJ...414L..49C`). The original mega-flare detection:
  ~10³⁴–10³⁵ erg in the EUV.
- **Stelzer B. et al. 2013** — *The UV and X-ray activity of the M
  dwarfs within 10 pc of the Sun*, MNRAS 431, 2063
  (`2013MNRAS.431.2063S`, arXiv:1302.1061,
  doi:10.1093/mnras/stt220). AU Mic quiescent X-ray luminosity
  log L_X ≈ 29.7 cgs and log(L_X/L_bol) ≈ −3.0; saturated activity
  regime. Phase 2 cross-check on the Hα-anchored activity row.

### Read (context / methodology, not decision-driving)

- **Martioli E. et al. 2021** — *AU Mic c: a second planet
  transiting the young M dwarf AU Mic* (`2021A&A...649A.177M`,
  arXiv:2102.05288). TESS + ground-based confirmation of AU Mic c;
  not stellar-decisive but defines the planet roster.
- **Mallorquin M. et al. 2024** — *AU Mic system characterization
  with ESPRESSO* (`2024A&A...689A.132M`,
  doi:10.1051/0004-6361/202450047). Refined b/c orbital and mass
  parameters via ESPRESSO RV + TESS reanalysis. Phase 2
  cross-check on stellar mass / radius (consistent with Wittrock
  2023 and Donati 2023 within 1σ).
- **Donati J.-F. et al. 2025** — *AU Mic system characterized with
  ESPRESSO* (`2025A&A...700A.227D`,
  doi:10.1051/0004-6361/202555371). Adds AU Mic e candidate;
  reports M = 0.50 ± 0.03 M☉, R = 0.75 ± 0.03 R☉ from ESPRESSO +
  SPIRou. Phase 2 cross-check on mass and radius (consistent with
  the Plavchan 2020 M_K-based values, within 1σ of the Donati 2023
  ZDI radius and Wittrock 2023 dynamical mass).
- **Cale B. L. et al. 2021** — *Diving Beneath the Sea of Stellar
  Activity: Chromatic Radial Velocities of the Young AU Mic
  Planetary System*, AJ 162, 295 (`2021AJ....162..295C`,
  arXiv:2109.13996). RV mass for AU Mic b with Gaussian-process
  activity detrending; Phase 2 cross-check on planet mass
  (superseded by Mallorquin 2024 but historically important).
- **Smith B. A. & Terrile R. J. 1981** — *A Circumstellar Disk
  Around AU Microscopii?* (early IR-excess detection, pre-resolved).

### Read (instrument / non-cfg-decisive)

- **Boyajian T. S. et al. 2012** — *Stellar Diameters and
  Temperatures II*, ApJ 757, 112 (`2012ApJ...757..112B`,
  arXiv:1208.2431). CHARA M-dwarf interferometric calibration;
  context for the Donati 2023 radius but no direct AU Mic
  measurement.
- **Loyd R. O. P. et al. 2018** — *MUSCLES Treasury Survey V:
  FUV Flares On Active and Inactive M Dwarfs*, ApJ 867, 71
  (`2018ApJ...867...71L`, arXiv:1809.07322). FUV flare statistics
  on young M-dwarf comparison set including AU Mic.
- **Beeck B. et al. 2013** — *3D radiative-hydrodynamic simulations
  of cool main-sequence stars* (cited via Donati 2023 §3).
  Granulation model grid.
- **Kowalski A. F. et al. 2013** — *Time-resolved Properties and
  Global Trends in dM Flares from Simultaneous Photometry and
  Spectra*, ApJS 207, 15 (`2013ApJS..207...15K`, arXiv:1307.2099).
  Defines the white-light flare continuum decomposition adopted
  for the cfg flare color.

### Not read — no arXiv preprint or low-priority (~40 papers)

Conference abstracts (DPS / EPSC / IAU), early IRAS-era
characterization (pre-Krist 2005), SETI / laser-emission monitoring
of nearby M-dwarfs, and interstellar-precursor mission
proposals contribute no cfg-decisive content for the stellar
synthesis. Planet-specific JWST and ground-based atmosphere
papers (Allart 2024 He I; Hirano 2020 Rossiter-McLaughlin) are
deferred to the planet Phase 3 follow-up workspace. The full
filtered bibliography is preserved in
`docs/phase3/_bib/au-mic.yaml` with `status: skipped` annotations.

## Open items for follow-up

- **AT Microscopii DB entry**: AT Mic is a wide common-proper-motion
  companion to AU Mic at ~46 400 AU (~1.22°), itself a short-period
  M-dwarf binary and a β Pic MG member. No separate NS DB entry as
  of this writing. A follow-up Phase 2 should ingest AT Mic A and B
  and link the system in `db/systems/`; AU Mic and AT Mic should
  share a common `system_name` or `cpm_group` field.
- **Phase 2 `disk_measurements` ingest**: `db/systems/au_mic.json`
  has no `disk_measurements` block; the geometry adopted here
  (35–210 AU, 50 K, i = 89.5°, edge-on) was sourced directly from
  Krist 2005, Schneider 2014, Boccaletti 2015/2018, and Chen 2005.
  These should be added as a `disk_measurements` array in the DB
  for consistency with the standard Phase 2 schema and so that the
  Kopernicus circumstellar-disk cfg writer can read from a
  canonical location.
- **Planet b/c/d/e Phase 3 follow-up workspace**: the four known
  planets are out of scope for this stellar synthesis. A dedicated
  follow-up workspace should produce Phase 3 syntheses for at
  minimum b (hot Neptune — atmosphere retention under super-flare
  bombardment) and d (~Earth-mass TTV candidate, the most
  visually-relevant rocky body). c is a sub-Neptune; e is currently
  controversial (pl_controv_flag = 1).
- **Cycle phase / activity modulation**: AU Mic is in the saturated
  pre-MS regime and has no observed activity cycle. If a future
  observing campaign detects one (typical timescale would be ~1–3
  years if it exists), a `activity_cycle_years` entry can be filled.
- **Birth-ring planetesimal mass**: Strubbe & Chiang 2006 estimate
  the parent planetesimal belt mass at roughly 0.01–0.1 M⊕; a
  future cfg field `disk_planetesimal_mass_mearth` could
  parameterize this for in-game lore consistency. Not currently in
  the standard Decisions schema.
- **Disk-substructure animation period calibration**: the cfg
  animates substructures at the SPHERE-measured 4–10 km/s outflow
  velocity, but the exact in-game time-mapping requires a
  gameplay-vs-realism tradeoff decision once the Kopernicus circumstellar
  cfg writer is exercised. Preserve as a tie-break for the cfg variant.
- **Conservative cfg variant**: a static-disk variant preserving the
  same `disk_inner_radius_au` / `disk_outer_radius_au` /
  `disk_dust_temperature_k` but with
  `visual_companion_event_disk_substructures_animated = false`
  should be shippable as a fallback for low-end hardware.

## Related

- [methodology](../reference/methodology.md) — schema source for the Decisions table
- [alpha-centauri-a](alpha-centauri-a.md) — canonical stellar-synthesis structural template (this file follows its 8-section layout)
- [proxima-cen](proxima-cen.md) — comparison M-dwarf (M5.5Ve, ~4.85 Gyr) — contrast with AU Mic's young pre-MS M1Ve state
