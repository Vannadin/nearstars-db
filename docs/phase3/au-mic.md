<!-- AU Mic Phase 3 synthesis: cfg-ready decisions and reasoning -->
# AU Microscopii — Phase 3 Synthesis

AU Microscopii (HD 197481, GJ 803, HIP 102409) is a nearby M1Ve
pre-main-sequence dwarf at 9.714 pc (Gaia DR3 parallax 102.94 ± 0.02
mas, this DB) — one of the youngest stars in the entire NearStars
catalog at ~22 Myr (Mamajek & Bell 2014 isochronal age of the β
Pictoris Moving Group, of which AU Mic is a canonical member).
The fundamental parameters come from the frozen Phase 2 layer:
R = 0.862 ± 0.052 R☉ (Gallenne 2022 VLTI/PIONIER, the only refereed
interferometric radius — the widely-cited 0.75 R☉ traces to an
unrefereed White 2019 AAS abstract; see Canonical alternatives),
M = 0.50 ± 0.03 M☉ (Plavchan 2020 PMS isochrone), and Teff = 3665 ± 31 K
(Cristofari 2023 SPIRou atmospheric fit). The luminosity is
L = 0.102 L☉ (Donati 2023, log L/L☉ = −0.99 ± 0.01) — elevated for an
M1V because AU Mic is still contracting onto the main sequence and
remains slightly inflated.

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
animated radial moving substructures.** The stellar layer is
re-anchored on the frozen Phase 2 sources (Gallenne 2022 interferometry,
Plavchan 2020, Cristofari 2023, Donati 2023, Mamajek & Bell 2014) with
documented radius / mass / luminosity divergences; tie-break picks
involve the visual hex tint, the disk-substructure animation choice,
the flare color, and the spot-coverage cycle phase.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M1Ve | high | Hawley 1996; Gaia DR3 spectype = M1VeBa1 |
| `mass_msun` | 0.50 ± 0.03 | high | Plavchan 2020 — PMS isochrone (Phase 2 recommended, community standard). DOCUMENTED DIVERGENCE vs Donati 2023 Dartmouth 0.60 (see Canonical alternatives) |
| `radius_rsun` | 0.862 ± 0.052 | high | Gallenne 2022 — VLTI/PIONIER interferometry, θ_LD 0.825 mas (Phase 2 recommended; only refereed interferometric radius). DOCUMENTED DIVERGENCE vs the unrefereed White 2019 AAS-abstract 0.75 (see Canonical alternatives) |
| `teff_k` | 3665 ± 31 | high | Cristofari 2023 — SPIRou atmospheric fit with magnetic fields (Phase 2 recommended; supersedes the Gaia 3518); Donati 2023 V−I color gives 3700 ± 70 |
| `luminosity_lsun` | 0.102 ± 0.002 | high | Donati 2023 — log(L/L☉) = −0.99 ± 0.01 (M_bol + BC + distance; Phase 2 recommended). Plavchan 2009 SED gives 0.09 (see Canonical alternatives) |
| `metallicity_fe_h_dex` | +0.12 ± 0.10 | medium | Cristofari 2023 — direct SPIRou spectroscopy [M/H] (Phase 2 recommended; [α/Fe] = 0 so [M/H] ≈ [Fe/H]; supersedes the β Pic MG mean) |
| `age_gyr` | 0.023 ± 0.003 | high | Mamajek & Bell 2014 — β Pic MG isochronal 22 ± 3 Myr reconciled with the Li-depletion-boundary age; the ~12 Myr kinematic age is explicitly rejected |
| `rotation_period_days` | 4.86 | high | Plavchan 2020 — TESS photometric rotational modulation (multi-spot, 4.863 d primary) |
| `activity_cycle_years` | null | low | No cycle resolved at AU Mic's age — pre-main-sequence saturated dynamo, no observed long-term modulation. Set null; do not invent |
| `x_ray_log_lx_cgs` | 29.35 | high | Tsikoudi & Kellett 2000 — ROSAT quiescent Lx = 2.24e29 erg/s, log(Lx/Lbol) ≈ −3.24, saturated regime (Phase 2 recommended activity proxy). NOTE: there is NO chromospheric log R'HK in the frozen Phase 2 layer for AU Mic — the X-ray index is the activity proxy (the earlier −3.9 log R'HK row was an unsourced placeholder, removed) |
| `flare_rate_per_day` | 5.6 | high | Tristan 2023 — TESS Sectors 1+27 flare census; 26.3 flares per TESS sector (~27.4 d) integrated above ~10³¹ erg |
| `flare_energy_log_erg_max` | 34.5 | medium | Cully 1993 EUVE 1992 mega-flare; consistent with Tristan 2023 upper-end TESS optical events ≥ 10³⁴ erg in white-light band |
| `magnetic_dipole_strength_kG` | 0.55 | high | Donati 2023 — large-scale field 550 ± 30 G (ZDI, mostly poloidal/axisymmetric) |
| `magnetic_total_field_kG_rms` | 2.61 ± 0.05 | high | Donati 2023 — small-scale mean field ⟨B⟩ from Zeeman broadening (Phase 2 DB meta_notes) |
| `spot_coverage_max_fraction` | 0.12 | high | Plavchan 2020 + Donati 2023 — multi-spot models require ≥ 10% disk coverage; visible asymmetry of TESS lightcurve |
| `limb_darkening_alpha_h` | ~0.45 | low | Tie-break: not directly measured for AU Mic; interpolated from Claret 2018 M-dwarf grid at Teff = 3500 K; interesting-first preserves slight visual edge dimming |
| `visual_surface_tint_hex_primary` | `#e0743a` (deep orange-red, M1V) | medium | Teff 3665 K blackbody + molecular-band suppression (hex retained; the 3518→3665 K shift is within rendering tolerance, slightly warmer/less red than M5.5 Proxima `#c54c2a` since Teff ~620 K higher) |
| `visual_flare_color_hex` | `#ff9050` (white-light flare continuum, slightly bluer than quiescent due to T_bb ~9000 K flare ribbon) | medium | Kowalski 2013 dM-flare continuum decomposition; tie-break against pure Hα reddening — chosen so flares brighten visibly against the dim red quiescent disk |
| `v_sin_i_km_s` | ~9.0 | medium | Derived from R = 0.862 R☉ and P_rot = 4.86 d (edge-on, sin i ≈ 1); consistent with Kochukhov & Reiners; supersedes the ~8.5 keyed to the old 0.82 R☉ |
| `stellar_color_temp_k` | 3665 | high | derived from Teff (Cristofari 2023) |
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
catalog — but warmer than Proxima or the TRAPPIST-1 host. At
Teff = 3665 K (Cristofari 2023) and R = 0.862 R☉ (Gallenne 2022),
the luminosity is 0.102 L☉ (Donati 2023; about 1/10 of the Sun),
with most flux emerging between 0.7 and 2.0 μm. TiO bands suppress
the visible continuum below 6500 Å sharply; VO and water bands shape
the near-infrared. Because AU Mic is pre-main-sequence (~22 Myr), the
radius is inflated relative to a settled M1V — the Gallenne 2022
interferometric radius 0.862 R☉ is consistent with PARSEC and Baraffe
pre-MS evolutionary tracks at 22 Myr / 0.50 M☉.

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

Mineralogically the photosphere is supersolar [Fe/H] ≈ +0.12 (β Pic
MG mean — Shkolnik 2017; no direct AU Mic measurement is on file
in the DB), slightly reddening the SED toward the long-wavelength
end relative to a solar-metallicity M1V. This is invisible at the
spectral resolution of the in-game illumination color but justifies
the deeper-red `#e0743a` over a pure 3665 K Planckian.

## Atmosphere synthesis

AU Mic is one of the most chromospherically and coronally active
stars in the solar neighborhood — its outer atmosphere drives most
of the spaceweather-relevant physics for planet b/c/d/e and for the
debris disk. The quiescent X-ray luminosity is log L_X ≈ 29.35 cgs
(Tsikoudi & Kellett 2000 ROSAT, Lx = 2.24e29 erg/s), placing AU Mic in
the **saturated regime**: log(L_X/L_bol) ≈ −3.24, near the empirical
upper limit for rapid
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

The chromosphere is filled with Hα emission (EW ≈ 1 Å in
quiescence, several Å during flares), He I 10830 Å absorption-to-
emission cycling, and broad Mg II h&k. UV flux at Lyman-α is
elevated by factors of 10²–10³ over Sol's. The transition region is
extremely bright: Loyd et al. 2018 measure FUV fluxes consistent
with the saturated activity locus. Without an activity cycle to
modulate it — AU Mic is too young and too saturated to show one —
the high-energy output is approximately constant over decades, with
quasi-stochastic super-flare punctuation.

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
is consistent with edge-on (v sin i ≈ 9 km/s implies sin i ≈ 1 given
R = 0.862 R☉ and P = 4.86 d), aligning the rotation
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

## Canonical alternatives

**Radius — refereed interferometry vs the community-standard value.**
The cfg adopts R = 0.862 ± 0.052 R☉ from Gallenne 2022 (VLTI/PIONIER,
θ_LD 0.825 mas), the only *refereed* interferometric radius. The
widely-quoted 0.75 R☉ traces to White et al. 2019, which exists only
as an unrefereed AAS conference abstract (no journal paper, no arXiv);
Donati 2023 infers 0.78–0.82 R☉ from L + Teff, sitting between the two
and supporting the larger value. A future cfg could expose the 0.75
community value as an alternate scenario, but the refereed
interferometric radius is the principled default.

**Mass — Plavchan vs Donati.** The cfg uses M = 0.50 ± 0.03 M☉
(Plavchan 2020 PMS isochrone, the community standard propagated to all
the planet papers); Donati 2023 derives a higher 0.60 ± 0.04 M☉ from
Dartmouth tracks.

**Luminosity — Donati vs Plavchan.** The cfg uses L = 0.102 L☉
(Donati 2023, log L = −0.99); Plavchan 2009's SED gives 0.09 L☉. The
two agree to ~10%.

**Activity index.** AU Mic is an M dwarf with a convective dynamo, so
log R'HK is physically definable in principle, but there is NO
chromospheric log R'HK in the frozen Phase 2 layer — the cfg activity
proxy is the X-ray log(Lx/Lbol) ≈ −3.24 (Tsikoudi & Kellett 2000),
near the saturation ceiling. (The earlier −3.9 log R'HK figure was an
unsourced placeholder.)

## Visual styling

The visual presentation of AU Mic is the most distinctive in the
NearStars catalog and combines four elements:

- **Stellar disk** — a deeply red M1V tinted `#e0743a`, fills 1.5°
  angular diameter as seen from AU Mic b (0.07 AU), 0.8° from c
  (0.119 AU). The color is similar to a sunset Sun on Earth, but
  the spectrum is much redder; rendering uses both the photometric
  hex tint and the SED-illumination color temperature (3665 K) to
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

- **Gallenne A. et al. 2022** — *The radius and effective temperature
  of the pre-main-sequence M dwarf AU Mic via VLTI/PIONIER*, A&A 665,
  A41 (`2022A&A...665A..41G`, arXiv:2207.04116). The only *refereed*
  interferometric radius: θ_LD = 0.825 ± 0.033 ± 0.038 mas →
  R = 0.862 ± 0.052 R☉. Phase 2 recommended radius.
- **Cristofari P. I. et al. 2023** — *Atmospheric parameters and
  magnetic fields of M dwarfs from SPIRou*, MNRAS 522, 1342
  (`2023MNRAS.522.1342C`, arXiv:2303.11241). SPIRou atmospheric fit
  (with magnetic fields): Teff = 3665 ± 31 K, [M/H] = +0.12 ± 0.10,
  log g = 4.52. Phase 2 recommended Teff + metallicity.
- **Tsikoudi V. & Kellett B. J. 2000** — *ROSAT all-sky survey X-ray
  emission from late-type stars*, MNRAS 319, 1147 (`2000MNRAS.319.1147T`).
  AU Mic quiescent Lx = 2.24 × 10²⁹ erg/s (log Lx 29.35, log Lx/Lbol
  ≈ −3.24). Phase 2 recommended X-ray activity proxy. (Supersedes the
  earlier Stelzer 2013 citation; the NEXXUS 2.51e29 value cited online
  is WRONG for AU Mic — NEXXUS is a G/K sample.)
- **Plavchan P. et al. 2020** — *A planet within the debris disk
  around the pre-main-sequence star AU Microscopii*, Nature 582,
  497 (`2020Natur.582..497P`, arXiv:2006.13248). TESS discovery of
  AU Mic b transiting hot Neptune; 4.86-d rotation period; PMS-isochrone
  mass 0.50 ± 0.03 M☉ (Phase 2 recommended mass); multi-spot complexity.
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
  (`2014MNRAS.445.2169M`, arXiv:1409.2737). Isochronal age 22 ± 3
  Myr for the β Pic MG (and thus for AU Mic); LDB confirmation.
- **Donati J.-F. et al. 2023** — *The magnetic field topology and
  filling of the very active M dwarf AU Mic*, MNRAS 525, 455
  (`2023MNRAS.525..455D`, arXiv:2304.09642). SPIRou ZDI: small-scale
  mean field ⟨B⟩ = 2.61 ± 0.05 kG, large-scale field 550 ± 30 G
  (Phase 2 recommended magnetic values); log L/L☉ = −0.99 ± 0.01 →
  L 0.102 (Phase 2 recommended luminosity); V−I Teff 3700 ± 70 and
  Dartmouth mass 0.60 (divergence alternatives).
- **Wittrock J. M. et al. 2023** — *Transit Timing Variation
  Measurements and Dynamical Mass Determination of the AU Mic
  System*, AJ 166, 232 (`2023AJ....166..232W`, arXiv:2310.10719).
  N-body + TTV dynamical mass 0.51 ± 0.028 M☉ — consistent with, but
  superseded as the cfg value by, the Plavchan 2020 0.50 ± 0.03;
  introduces planet d as a TTV-only candidate.
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
  (`2013MNRAS.431.2063S`, arXiv:1302.1061). AU Mic quiescent X-ray;
  context only — NOT in the frozen Phase 2 bib (the cfg X-ray proxy is
  Tsikoudi & Kellett 2000, log Lx 29.35).

### Read (context / methodology, not decision-driving)

- **Martioli E. et al. 2021** — *AU Mic c: a second planet
  transiting the young M dwarf AU Mic* (`2021A&A...649A.177M`,
  arXiv:2102.05288). TESS + ground-based confirmation of AU Mic c;
  not stellar-decisive but defines the planet roster.
- **Mallorquin M. et al. 2024** — *AU Mic system characterization
  with ESPRESSO* (`2024A&A...689A.132M`). Refined b/c orbital and
  mass parameters; not stellar-decisive.
- **Donati J.-F. et al. 2025** — *AU Mic system characterized with
  ESPRESSO* (`2025A&A...700A.227D`). Adds AU Mic e candidate;
  context only for stellar synthesis.
- **Shkolnik E. L. et al. 2017** — *HAZMAT II: Ultraviolet
  Variability of Low-Mass Stars in the GALEX Archive*, ApJ 838,
  87 (`2017ApJ...838...87S`, arXiv:1611.02835). β Pic MG and young
  M-dwarf activity calibration; context for AU Mic's saturated
  state.
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
