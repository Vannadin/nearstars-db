<!-- Barnard's Star Phase 3 synthesis: cfg-ready decisions and reasoning -->
# Barnard's Star — Phase 3 Synthesis

Barnard's Star (GJ 699, HIP 87937, V2500 Oph) is an M4.0 Ve red dwarf
at 1.83 pc — the nearest single star to the Sun (only the α Centauri
triple lies closer) and the star with the highest known proper motion
of any object in the sky, μ ≈ 10.3 arcsec/yr (Barnard 1916). At that
rate it crosses a full lunar diameter on the sky in about 175 years.
It is an old, metal-poor, intermediate-Population-II / high-velocity
disk star (space velocity ~140 km/s relative to the Sun), and
correspondingly one of the most magnetically quiet M dwarfs known:
the chromospheric index log R'HK = −5.82 (Toledo-Padrón et al. 2019)
sits near the floor of M-dwarf activity, an order of magnitude below
the active flare stars that dominate the M-dwarf census.

The fundamental parameters come from the frozen Phase 2 layer.
The mass M = 0.162 ± 0.007 M☉ and the luminosity
L = 0.003558 ± 0.000072 L☉ are both from Schweitzer et al. 2019
(CARMENES), as is the radius R = 0.187 ± 0.001 R☉. That radius is
**interferometric in origin**: Boyajian et al. 2012b measured the
limb-darkened angular diameter θ_LD = 0.952 mas with the CHARA array,
and Schweitzer 2019 recomputed R = 0.187 R☉ by combining that θ_LD
with the Gaia DR2 distance. The effective temperature Teff = 3195 ± 28 K
is from González Hernández et al. 2024 (ESPRESSO master spectrum,
SteParSyn), the most recent high-resolution determination and the
Phase 2 recommended value; it sits at the cool end of an ~80 K spread
across spectroscopic analyses (see Canonical alternatives). The
metallicity is sub-solar, [Fe/H] = −0.39 ± 0.03 from Jahandar et al.
2023 (SPIRou near-infrared), the recommended value — but the
metallicity spread across instruments is large (~0.4 dex) and is the
second documented divergence of this synthesis.

What characterizes Barnard's Star for NearStars is not drama but
extreme quiescence and antiquity. The age is ~8.5 ± 1.5 Gyr (Ribas
et al. 2018, kinematic), consistent with the broader 7–10 Gyr range
inferred from its thick-disk / halo-grazing kinematics; it is one of
the oldest stars in the catalog. The rotation period is very long,
P_rot = 145 ± 15 d (Toledo-Padrón et al. 2019, photometric), the
signature of several Gyr of magnetic braking having spun the star
down almost completely (v sin i is unmeasurably small, ~0.07 km/s
implied by R and P). The same monitoring campaign reports a long-term
activity cycle of order ~10 yr — a slow, Sun-like cyclic modulation
superimposed on a chromosphere that is otherwise near its activity
floor. Despite its quiescence the star does produce rare flares: a
strong far-UV flare was caught in 2019 (HST), confirming that even
this inactive an old M dwarf retains an episodic flaring corona.

Barnard's Star hosts a **compact system of four confirmed
sub-Earths**: "Barnard b" (P ≈ 3.15 d, M sin i ≈ 0.30 M⊕) and
siblings c, d, and e (P ≈ 4.12, 2.34, 6.74 d; M sin i 0.19–0.34 M⊕),
all rocky sub-Earths well inside the habitable zone. They were
detected by the ESPRESSO campaign (González Hernández et al. 2024)
and confirmed with independent MAROON-X data by Basant et al. 2025,
which promoted candidates c, d, and e to bona-fide planets. (The
earlier Ribas et al. 2018 "Barnard b" super-Earth at P ≈ 233 d was
subsequently retracted — Lubin et al. 2021 — and is not the same
object.) Each is characterized in its own per-planet Phase 3
synthesis (`barnards-star-b/c/d/e`).

**Scenario choice for NearStars: an ancient, deeply red, extremely
quiet M4 V dwarf — the nearest single star — slowly rotating on a
145-day period with a faint ~10 yr activity cycle and only rare
flares.** The stellar layer is anchored on the frozen Phase 2 sources
(Schweitzer 2019 mass/radius/luminosity, González Hernández 2024
Teff, Jahandar 2023 metallicity, Toledo-Padrón 2019 rotation/activity,
Ribas 2018 age, Boyajian 2012b interferometric diameter). Two
parameters carry documented divergences across the literature —
metallicity (~0.4 dex spread) and Teff (~80 K spread) — handled in
`## Canonical alternatives`. One tie-break sets the visual surface
tint for the M4 V SED.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M4.0 Ve | high | Phase 2 DB spectype; the "e" denotes the historical Hα-emission/flare designation (variable-star name V2500 Oph) even though the star is now extremely quiet |
| `mass_msun` | 0.162 ± 0.007 | high | Schweitzer et al. 2019 — CARMENES spectroscopic_calibration (Phase 2 recommended); Mann et al. 2015 M_K empirical relation gives 0.161 ± 0.006, agreeing within 1σ |
| `radius_rsun` | 0.187 ± 0.001 | high | Schweitzer et al. 2019 — interferometric: Boyajian 2012b limb-darkened θ_LD = 0.952 mas (CHARA) combined with the Gaia DR2 distance (Phase 2 recommended) |
| `teff_k` | 3195 ± 28 | high | González Hernández et al. 2024 — ESPRESSO master spectrum, SteParSyn (Phase 2 recommended). Documented divergence: ~80 K spread vs Jahandar/Marfil/Schweitzer — see Canonical alternatives |
| `luminosity_lsun` | 0.003558 ± 0.000072 | high | Schweitzer et al. 2019 — bolometric flux (Phase 2 recommended); ~1/280 of the Sun's luminosity |
| `metallicity_fe_h_dex` | −0.39 ± 0.03 | medium | Jahandar et al. 2023 — SPIRou near-infrared spectroscopy (Phase 2 recommended). DOCUMENTED DIVERGENCE: ~0.4 dex spread vs Schweitzer 2019 VIS (−0.15) and Marfil 2021 (−0.57) — see Canonical alternatives |
| `age_gyr` | 8.5 ± 1.5 | medium | Ribas et al. 2018 — kinematic age from thick-disk / high-velocity membership (Phase 2 recommended); consistent with the broader 7–10 Gyr range for intermediate Pop-II disk stars |
| `rotation_period_days` | 145 ± 15 | high | Toledo-Padrón et al. 2019 — photometric rotational modulation; the long period reflects several Gyr of magnetic braking |
| `activity_log_rhk` | −5.82 ± 0.08 | high | Toledo-Padrón et al. 2019 — Ca II H&K chromospheric index; near the M-dwarf activity floor, one of the quietest M dwarfs known |
| `activity_cycle_years` | ~10 | medium | Toledo-Padrón et al. 2019 — long-term cyclic modulation in the activity-index time series; order ~10 yr, Sun-like in character |
| `v_sin_i_km_s` | ~0.07 | low | Derived from R = 0.187 R☉ and P_rot = 145 d (equatorial velocity ~0.065 km/s); below the resolution of any spectroscopic v sin i measurement — the star is effectively a non-rotator for line-broadening purposes |
| `visual_surface_tint_hex_primary` | `#cf5a30` (deep orange-red, M4 V) | medium | Tie-break: 3195 K blackbody + TiO/VO molecular-band suppression; redder than the M1V AU Mic `#e0743a` (Teff ~470 K hotter), slightly warmer than the M5.5 Proxima `#c54c2a` (Teff ~145 K cooler) |
| `stellar_color_temp_k` | 3195 | high | derived from Teff (González Hernández 2024) |
| `apparent_magnitude_v_from_earth` | 9.51 | high | Hipparcos / standard photometry; far below naked-eye visibility despite the 1.83 pc distance, because of the low luminosity (M_V ≈ 13.2) |
| `proper_motion_arcsec_per_yr` | 10.36 | high | Barnard 1916 / Gaia; the highest proper motion of any known star ("Barnard's Runaway Star") |

## Surface synthesis

Barnard's Star has one of the deepest red photospheres in the
catalog. At Teff = 3195 K (González Hernández 2024) the SED peaks far
into the near-infrared near ~0.91 μm, with the optical continuum
heavily suppressed by TiO and VO molecular bands below ~0.7 μm and
shaped by water bands in the NIR. With R = 0.187 R☉ (Schweitzer 2019,
interferometric) the luminosity is only 0.003558 L☉ — about 1/280 of
the Sun — so the star is intrinsically faint despite being the
nearest single star: from Earth it shines at only V ≈ 9.5, invisible
to the naked eye.

Unlike the inflated pre-main-sequence radii of young M dwarfs, the
0.187 R☉ here is a fully-settled main-sequence radius for a ~0.16 M☉
star of several-Gyr age, and the interferometric anchor (Boyajian
2012b θ_LD = 0.952 mas, the limb-darkened diameter measured directly
with the CHARA array) makes it one of the better-determined M-dwarf
radii. The sub-solar metallicity [Fe/H] = −0.39 (Jahandar 2023)
slightly reduces the molecular-band line blanketing relative to a
solar-metallicity M4 V, nudging the SED marginally toward the blue,
but this is invisible at the spectral resolution of the in-game
illumination color and only weakly justifies the chosen tint.

The defining surface property is **quiescence**, not activity. With
log R'HK = −5.82 (Toledo-Padrón 2019) Barnard's Star sits near the
empirical floor of M-dwarf chromospheric activity — its spot
coverage is low and its photometric rotational amplitude small,
which is precisely why resolving the 145-day rotation period required
a dedicated long-baseline monitoring campaign. For cfg rendering this
means a near-uniform red disk with only faint, slowly-drifting spot
features, in deliberate contrast to the high-spot-coverage active M
dwarfs (AU Mic, Proxima) elsewhere in the catalog. Granulation is
M-dwarf-typical with small convection cells set by the shallow
photospheric pressure scale height.

## Atmosphere synthesis

Barnard's Star's outer atmosphere is dominated by its extreme
quiescence. The chromospheric Ca II H&K index log R'HK = −5.82
(Toledo-Padrón 2019) places it among the least active M dwarfs ever
measured — roughly an order of magnitude below the saturated young
flare stars and below even the field-M-dwarf median. The 145-day
rotation period and the resulting very large Rossby number put the
star deep in the unsaturated, magnetically-braked regime where
activity scales steeply with rotation: slow rotation begets weak
dynamo action begets a quiet corona and chromosphere.

The Toledo-Padrón 2019 campaign nonetheless resolved a **long-term
activity cycle of order ~10 yr** in the chromospheric-index time
series — a slow, Sun-like cyclic modulation riding on top of the
otherwise floor-level activity. This is the cfg `activity_cycle_years`
anchor; in rendering it modulates the (already faint) spot pattern
and chromospheric emission on a decadal timescale rather than driving
dramatic outbursts.

Quiescent does not mean inert. A strong far-ultraviolet **flare** was
caught on Barnard's Star in 2019 (HST observations), demonstrating
that even an 8–10 Gyr-old, near-floor-activity M dwarf retains an
episodic flaring corona capable of significant transient XUV output.
For cfg purposes flares are rare-event punctuation — not the
near-continuous flaring of AU Mic — and the quiescent XUV background
is low. The implication for any of the close-in sub-Earth planet
candidates is that the time-averaged high-energy irradiation is far
gentler than around an active M dwarf, though the rare flares and the
proximity of the candidate orbits (P ≈ 3 d) still impose a
non-negligible cumulative XUV dose over the star's long lifetime.

## Rotation & spin synthesis

The 145-day rotation period (Toledo-Padrón 2019, photometric
modulation) is among the longest in the M-dwarf catalog and is the
direct fingerprint of age. Over its ~8.5 Gyr lifetime Barnard's Star
has shed nearly all of its initial angular momentum through magnetic
(Skumanich-type) braking, spinning down from a presumably rapid
zero-age-main-sequence rotation to the present near-stationary state.
The implied equatorial velocity is only ~0.065 km/s, so v sin i is
far below the detection threshold of any spectroscopic line-broadening
analysis — the cfg records it as ~0.07 km/s with low confidence
purely as a derived quantity, not a measurement.

This slow rotation is the engine of the star's quiescence: the
rotation–activity relation for M dwarfs predicts exactly the
floor-level log R'HK = −5.82 observed at this Rossby number. The
decadal activity cycle (~10 yr, Toledo-Padrón 2019) is the only
significant temporal variation; there is no fast rotational signal to
render, and the photometric modulation at the rotation period is
low-amplitude because the spot coverage is small.

No asteroseismic constraint is available — Barnard's Star is too cool
and too small for detectable p-mode oscillations. The rotation-axis
inclination is unconstrained by direct measurement; for visual
rendering NearStars adopts a generic axis orientation, since the
near-zero rotational velocity makes any spin-related foreshortening
visually negligible. The dominant kinematic fact about the star is
not its spin but its **translation**: at 10.3 arcsec/yr proper motion
and ~140 km/s space velocity, Barnard's Star is the fastest-moving
star on the sky, and over the next few millennia it will continue to
approach, reaching perihelion (~1.14 pc) around the year 11800 CE
before receding.

## Canonical alternatives

Two parameters carry documented divergences across the Phase 2
literature. In both cases the cfg adopts the Phase 2 recommended
value, but the spread between instruments is large enough to warrant
explicit documentation.

| Field | cfg value (recommended) | Canonical alternatives | Why cfg picks this value |
|---|---|---|---|
| `metallicity_fe_h_dex` | −0.39 ± 0.03 (Jahandar 2023, SPIRou NIR) | −0.15 ± 0.16 (Schweitzer 2019, CARMENES VIS); −0.57 ± 0.10 (Marfil 2021) | The three determinations span ~0.4 dex — a genuine systematic disagreement, not measurement scatter. For cool M dwarfs the near-infrared is favored for metallicity because the optical (VIS) continuum is so heavily blanketed by molecular bands that pseudo-continuum placement and line-list incompleteness bias VIS-based [Fe/H]; NIR analyses (Jahandar 2023, SPIRou) work in a cleaner spectral regime. The cfg therefore adopts the NIR value −0.39, intermediate between the optical Schweitzer (−0.15) and Marfil (−0.57) extremes. The metallicity only weakly affects the rendered SED color, so this divergence is documentary rather than visually decisive. |
| `teff_k` | 3195 ± 28 (González Hernández 2024, ESPRESSO) | 3231 ± 21 (Jahandar 2023); 3254 ± 32 (Marfil 2021); 3273 ± 51 (Schweitzer 2019) | The four spectroscopic determinations span only ~80 K (3195–3273 K), tight by M-dwarf standards. The cfg adopts the coolest, González Hernández 2024, as the most recent high-resolution ESPRESSO master-spectrum analysis and the Phase 2 recommended value. An 80 K shift at this Teff corresponds to a sub-perceptible change in rendered tint (well inside the M4 V `#cf5a30` rendering tolerance), so the choice among these values is not visually decisive; the divergence is documented for completeness of the parameter set. |

Both Jahandar 2023 and Schweitzer 2019 (and Marfil 2021) remain in
the Phase 2 DB as `recommended:false` alternatives within their
respective measurement arrays, preserving the audit trail; the
recommended picks are González Hernández 2024 (Teff) and Jahandar
2023 ([Fe/H]).

## Visual styling

In the NearStars renderer, Barnard's Star is portrayed as a deeply
red, very faint M4 V dwarf — the nearest single star, but visually
unremarkable in brightness. The surface tint is encoded as `#cf5a30`,
a tie-break choice: the 3195 K blackbody continuum, after TiO/VO
molecular-band suppression of the blue, renders as a deep orange-red,
positioned in the catalog's M-dwarf palette between the warmer M1 V
AU Mic (`#e0743a`, Teff ~470 K hotter) and the cooler M5.5 Proxima
(`#c54c2a`, Teff ~145 K cooler). The illumination color temperature
for scene lighting of any nearby body is driven directly by the
3195 K SED.

The disk is rendered near-uniform with only faint, slowly-drifting
spot features — the visual expression of the floor-level activity
(log R'HK = −5.82) and the very slow 145-day rotation. There is no
dramatic flaring layer: flares are rare-event punctuation (the 2019
HST far-UV flare being the documented example), rendered as
occasional transient brightenings rather than the near-continuous
flare activity of AU Mic. The decadal ~10 yr activity cycle modulates
the already-subtle spot pattern slowly over the in-game equivalent of
years.

From Earth, Barnard's Star is a V ≈ 9.5 object (absolute magnitude
M_V ≈ 13.2) — far below naked-eye visibility despite its 1.83 pc
proximity, because of the tiny 0.003558 L☉ luminosity. Its visual
signature in the real sky is not brightness but **motion**: at
10.3 arcsec/yr it is the fastest-moving star known, and a NearStars
sky-rendering that spans centuries of in-game time would show it
visibly creeping across the background field of Ophiuchus. From the
viewpoint of any of its close-in sub-Earth planet candidates, the
red disk would subtend a modest angular diameter and bathe the
landscape in deep-red, infrared-dominated light, with the faint
~10 yr brightening cycle the only slow temporal change and rare
flares the only sudden ones.

## Bibliography

### Read (drove Decisions above)

- **Schweitzer A. et al. 2019** — *The CARMENES search for exoplanets
  around M dwarfs. Different roads to radii and masses of the target
  stars*, A&A 625, A68 (`2019A&A...625A..68S`,
  doi:10.1051/0004-6361/201834965, arXiv:1904.03231). CARMENES
  fundamental-parameter compilation. Source for the Phase 2
  recommended mass (0.162 ± 0.007 M☉, spectroscopic calibration),
  luminosity (0.003558 ± 0.000072 L☉, bolometric flux), and radius
  (0.187 ± 0.001 R☉, interferometric — from Boyajian 2012b θ_LD plus
  Gaia DR2 distance). Also the alternative Teff (3273 ± 51 K) and
  alternative VIS metallicity (−0.15 ± 0.16).
- **González Hernández J. I. et al. 2024** — *A sub-Earth-mass planet
  orbiting Barnard's star*, A&A 690, A79 (`2024A&A...690A..79G`,
  doi:10.1051/0004-6361/202451311, arXiv:2410.00569). ESPRESSO
  master-spectrum SteParSyn analysis: Teff = 3195 ± 28 K (Phase 2
  recommended). Also the discovery paper for the sub-Earth planet
  candidate Barnard b (P ≈ 3.15 d, M sin i ≈ 0.37 M⊕) and three
  lower-significance candidates — out of scope here, flagged for the
  planet follow-up.
- **Jahandar F. et al. 2023** — SPIRou near-infrared high-resolution
  abundance analysis of Barnard's Star (arXiv:2310.12125). Source for
  the Phase 2 recommended metallicity [Fe/H] = −0.39 ± 0.03 (NIR,
  favored for cool M dwarfs) and an alternative Teff = 3231 ± 21 K.
  The documented metallicity divergence (vs Schweitzer VIS −0.15 and
  Marfil −0.57) is anchored on this paper.
- **Marfil E. et al. 2021** — *The CARMENES search for exoplanets
  around M dwarfs. Stellar atmospheric parameters of target stars
  with SteParSyn*, A&A 656, A162 (`2021A&A...656A.162M`,
  doi:10.1051/0004-6361/202141980, arXiv:2110.07329). CARMENES
  VIS+NIR parameter determination: Teff = 3254 ± 32 K and the
  most metal-poor reading [Fe/H] = −0.57 ± 0.10. Both enter the
  Canonical-alternatives table.
- **Toledo-Padrón B. et al. 2019** — *Stellar activity analysis of
  Barnard's Star: very slow rotation and evidence for long-term
  activity cycle*, MNRAS 488, 5145 (`2019MNRAS.488.5145T`,
  doi:10.1093/mnras/stz1647, arXiv:1812.06712). Source for the
  Phase 2 recommended rotation period (P_rot = 145 ± 15 d,
  photometric) and chromospheric activity (log R'HK = −5.82 ± 0.08),
  plus the ~10 yr long-term activity cycle. The defining quiescence /
  slow-rotation picture of this synthesis.
- **Ribas I. et al. 2018** — *A candidate super-Earth planet orbiting
  near the snow line of Barnard's star*, Nature 563, 365
  (`2018Natur.563..365R`). Source for the Phase 2 recommended
  kinematic age (~8.5 ± 1.5 Gyr) from thick-disk / high-velocity
  membership. NOTE: the super-Earth "Barnard b" candidate announced
  in this paper (P ≈ 233 d) was later retracted (Lubin et al. 2021)
  and is unrelated to the González Hernández 2024 short-period
  candidate.
- **Boyajian T. S. et al. 2012b** — *Stellar Diameters and
  Temperatures II. Main-Sequence K- and M-Stars*, ApJ 757, 112
  (`2012ApJ...757..112B`, doi:10.1088/0004-637X/757/2/112,
  arXiv:1208.2431). CHARA-array limb-darkened angular diameter
  θ_LD = 0.952 mas for Barnard's Star — the interferometric basis
  for the Schweitzer 2019 recommended radius R = 0.187 R☉.

### Read (context / methodology, not decision-driving)

- **Mann A. W. et al. 2015** — *How to Constrain Your M Dwarf:
  Measuring Effective Temperature, Bolometric Luminosity, Mass, and
  Radius*, ApJ 804, 64 (`2015ApJ...804...64M`,
  doi:10.1088/0004-637X/804/1/64, arXiv:1501.01635). M_K-based
  empirical mass relation giving M = 0.161 ± 0.006 M☉ — the
  Phase 2 alternative mass, agreeing with Schweitzer 2019 within 1σ.

### Read (instrument-only / methodological references)

- **Barnard E. E. 1916** — *A small star with large proper motion*,
  AJ 29, 181. The discovery of the 10.3 arcsec/yr proper motion that
  gives the star its name; source for the proper-motion Decisions row.

### Not read — superseded or low-priority

The retracted Ribas 2018 233-day super-Earth follow-up literature
(Lubin et al. 2021 retraction and downstream re-analyses), generic
nearby-M-dwarf rotation surveys without a dedicated Barnard's Star
entry, the 2019 HST far-UV flare paper (context only — not a
cfg-decisive measurement in the frozen Phase 2 layer), and
interstellar-precursor mission proposals (Barnard's Star is a
long-standing flyby target) contribute no cfg-decisive content for
the stellar synthesis. The planet-candidate papers (González
Hernández 2024 planet section, and any 2025+ follow-up) are deferred
to the planet Phase 3 follow-up workspace. The full filtered
bibliography is preserved in `docs/phase3/_bib/barnards-star.yaml`.

## Stellar wind / astrosphere

Barnard's Star has the **smallest astrosphere** of the set. As the
highest-proper-motion star known it plows through the local ISM at ~120 km/s, so
even though its wind is weak (Ṁ ≤ 0.2 Ṁ⊙, Wood 2021) the ram pressure compresses
the wind cavity to a standoff of only **≲11 AU**. It is an old, magnetically
quiet M4 dwarf with no detected activity cycle, and its quiescent corona is
now measured at just 3% of the Sun's X-ray output (France 2020, Chandra) —
though X-ray+UV flares still punch through several times a day.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `solar_cycle_yr` | none (not detected) | low | old, magnetically quiet M4 — no published cycle detection, no Phase 2 measurement |
| `stellar_wind_mass_loss_solar` | ≤ 0.2 (upper limit) | medium | Wood 2021 astrospheric Lyα |
| `local_ism_inflow_speed_kms` | ~120 | medium | 6D astrometry vs LIC (extreme space velocity) |
| `astrosphere_standoff_au` | ≲ 11 (upper bound) | medium | high V_ISM compresses the cavity |
| `stellar_radiation_surface_relative_sun` | ~0.1 | medium | measured: log L_X 25.3 (France 2020 Chandra) = 0.03× solar quiescent; ~6 X-ray+UV flares/day lift the time-averaged dose. Quiescent-only canonical alternative: ~0.03 |
| `astrosphere_apex_ra_deg` / `_dec_deg` | ~97 / +37 | low | 6D astrometry vs LIC; **plugin-only** |

## Open items for follow-up

- **Sub-Earth planet candidate Phase 3 follow-up workspace.** The
  González Hernández 2024 ESPRESSO campaign reports a sub-Earth
  candidate Barnard b (P ≈ 3.15 d, M sin i ≈ 0.37 M⊕) plus three
  lower-significance candidates. These are out of scope for the
  stellar synthesis; a dedicated follow-up should produce planet
  Phase 3 syntheses once the candidates' Phase 2 measurements are
  curated. The retracted Ribas 2018 233-day candidate should be
  recorded as refuted, mirroring the tau Cet e / 40 Eri A b
  treatment.
- **Metallicity divergence resolution.** The ~0.4 dex spread between
  the NIR (Jahandar −0.39), VIS (Schweitzer −0.15), and Marfil
  (−0.57) determinations is a genuine systematic. A future curation
  pass could ingest additional NIR abundance analyses (e.g. further
  SPIRou or CRIRES+ work) to tighten the cool-M-dwarf metallicity
  and confirm whether the NIR-favored value is converging.
- **Activity-cycle period refinement.** The ~10 yr cycle
  (Toledo-Padrón 2019) is resolved at order-of-magnitude precision
  from a single long-baseline campaign. Continued monitoring would
  refine the period and amplitude and confirm whether it is a stable
  Sun-like cycle or a quasi-periodic modulation, which would sharpen
  the cfg `activity_cycle_years` rendering.
- **Flare-rate characterization.** The 2019 HST far-UV flare confirms
  episodic flaring, but no quantitative flare-frequency distribution
  is in the frozen Phase 2 layer. A TESS / HST flare census would let
  a future cfg attach a `flare_rate_per_day` and
  `flare_energy_log_erg_max` to the otherwise quiescent rendering.
- **Rotation-axis inclination.** Unconstrained; the near-zero
  rotational velocity makes spin-related visual effects negligible,
  so this is low-priority, but a measured inclination would let the
  faint spot modulation be rendered with correct foreshortening.

## Related

- [methodology](../reference/methodology.md) — schema source for the Decisions table
- [proxima-cen](proxima-cen.md) — comparison M dwarf (M5.5 Ve, ~4.85 Gyr); contrast Proxima's higher activity with Barnard's near-floor quiescence
- [au-mic](au-mic.md) — comparison M dwarf (young, active M1 Ve); the activity/age opposite extreme to Barnard's old quiet M4 V
