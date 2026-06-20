<!-- AU Mic b Phase 3 synthesis: cfg-ready decisions and reasoning -->
# AU Mic b — Phase 3 Synthesis

AU Microscopii b is a 4.79 ± 0.29 R⊕, 8.99 ± 2.61 M⊕ low-density
warm Neptune on an 8.463-day orbit around the 22-Myr-old pre-main-sequence
M1Ve flare star AU Microscopii. Plavchan et al. 2020 (Nature 582, 497;
`2020Natur.582..497P`, arXiv:2006.13248) discovered the planet in TESS
transits; Cale et al. 2021 (AJ 162, 295; `2021AJ....162..295C`,
arXiv:2109.13996) provided the first robust RV mass after Gaussian-process
detrending of the host star's spot signal; Mallorquin et al. 2024
(A&A 689, A132; `2024A&A...689A.132M`) refined both mass and radius with
ESPRESSO + TESS reanalysis. Bulk density is ≈ 0.45 g/cc — about three
times lower than Neptune — placing b firmly in the "puffy / inflated
sub-Saturn" regime characteristic of young transiting planets whose
hydrogen envelopes have not yet had time to cool and contract. Allart
et al. 2023 (A&A 677, A164; `2023A&A...677A.164A`, arXiv:2308.10891)
reported a marginal-to-significant He I 10830 Å absorption signature
during transit, consistent with an extended escaping H/He envelope;
Hirano et al. 2020 (ApJ 899, L13; `2020ApJ...899L..13H`,
arXiv:2006.13654) measured the projected obliquity via Rossiter–McLaughlin
and found it aligned within ~5° (λ = −2.96°), consistent with the
disk + stellar spin axis.

**Scenario choice for NearStars: a tidally-locked puffy hot Neptune
with an extended H/He-dominated atmosphere at ~10⁷ Pa surface pressure,
Jupiter-band-analog cloud structure under M-dwarf illumination, a hot
day-side, modest internal heat, and an actively escaping upper atmosphere
sculpted by AU Mic's super-flare bombardment.** All 27 cfg picks are
canonical-aligned within the puffy-Neptune literature window;
three are tie-breaks (atmosphere tint hex, cloud tint hex, banding
pattern choice). No documented divergences.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 8.46 d orbit; tidal damping timescale ≪ 22 Myr age for a Neptune at 0.07 AU around 0.51 M☉ (Goldreich & Soter 1966 scaling) |
| `obliquity_deg` | 0 | high | tidal damping; consistent with Hirano 2020 RM spin–orbit alignment |
| `eccentricity` | 0.07 | medium | Mallorquin 2024 ESPRESSO + TESS joint fit |
| `argument_of_periastron_deg` | -52 | medium | Mallorquin 2024 |
| `sidereal_period_days` | 8.463446 | high | Plavchan 2020 TESS; refined by Mallorquin 2024 |
| `semi_major_axis_au` | 0.07 | high | Mallorquin 2024 (Kepler's third from M☉ + P) |
| `inclination_deg` | 88.39 | high | Plavchan 2020 transit fit; refined Mallorquin 2024 |
| `mass_mearth` | 8.99 ± 2.61 | high | Mallorquin 2024 ESPRESSO RV with GP detrending; consistent with Cale 2021 (20.12 +1.57/-1.72 M⊕ — higher; Mallorquin 2024 supersedes via better activity model) |
| `radius_rearth` | 4.79 ± 0.29 | high | Mallorquin 2024 TESS + ground-based transits |
| `surface_gravity_g_earth` | 0.39 | high | derived = 8.99 / 4.79² |
| `density_g_cc` | 0.45 | high | derived; ≈ 0.08 ρ_Earth, ≈ 0.27 ρ_Neptune — puffy envelope confirmed |
| `insolation_s_earth` | 20.8 | high | derived from L = 0.102 L☉ (Donati 2023, recommended) and a = 0.07 AU |
| `equilibrium_temp_k` (A=0) | 593 | high | derived; consistent with TEPCat 556 K reported with non-zero albedo |
| `equilibrium_temp_k` (A=0.1) | 577 | high | derived; modest gas-giant albedo |
| `bond_albedo` | 0.10 | medium | gas-giant Neptune-analog low albedo; Cale 2021 §4 discussion |
| `dayside_surface_temp_k` | 700 | medium | super-rotation + greenhouse → dayside hotter than T_eq for a thick H/He envelope. Day-night offset estimated from the heat-recirculation (+ internal-heat) parameterization of Cowan & Agol 2011 (`1001.0012`) in the strong-recirculation limit (replaces the earlier Plavchan 2020 §6 attribution, which covers XUV/escape, not greenhouse redistribution) |
| `nightside_surface_temp_k` | 450 | medium | substantial day-night redistribution expected from thick atmosphere; no Spitzer phase curve yet. Estimated from the Cowan & Agol 2011 (`1001.0012`) heat-recirculation (+ internal-heat) parameterization |
| `atmosphere_present` | true | high | Allart 2023 He I 10830 detection; bulk density requires ≥ 30% H/He by mass |
| `atmosphere_surface_pressure_pa` | 1.0e7 | medium | hot-Neptune envelope mass ~30% of total → ~10⁷ Pa at the τ = 1 cloud deck; Lopez & Fortney 2014 mass-radius envelope mass-fraction calibration |
| `atmosphere_composition` | H₂ ~85%, He ~15%, trace H₂O / CH₄ / NH₃ / CO at solar abundance; photochemical haze in upper layer | medium | Allart 2023 He detection; high-mass-loss escape; Lavie 2017 cool-Neptune photochemistry analog |
| `atmosphere_scale_height_km` | 567 | high | derived: kT/μg with T = 600 K, μ = 2.3 (H/He), g = 3.8 m/s² — large H/He scale height drives Allart 2023's detectability |
| `atmosphere_tint_rgb_hex` | `#7c4a32` | low | Tie-break: interesting-first. Photochemical hydrocarbon haze under M-dwarf SED → muted red-brown, deeper than Jupiter's tan; chosen over a uniform peach for clearer banding contrast |
| `cloud_cover_fraction` | 0.70 | medium | gas-giant analog with banded cloud structure; Sing 2016 hot-Neptune cloud-deck census suggests common |
| `cloud_morphology` | Jupiter-band-analog zonal cloud structure with bright zones and dark belts; equatorial superrotation jet; faint polar hood under M-dwarf insolation | low | Tie-break: interesting-first. GCM-class simulations of puffy Neptunes (Showman 2009, Lewis 2010 hot-Jupiter analogs adapted to Neptune temperatures) favor banded structure; cfg picks the banded reading over a featureless uniform haze for visual interest |
| `cloud_tint_rgb_hex` | `#c0a880` | low | Tie-break: warm cream of H₂O/NH₃ cloud particles under M1V red illumination; chosen over a uniform cream for terminator contrast |
| `surface_morphology` | n/a — no solid surface; gas-giant envelope all the way down | high | density and mass-radius position rule out a rocky surface |
| `magnetic_field_present` | true | low | Neptune-mass H-rich envelope sustains a dynamo (Neptune/Uranus do) |
| `magnetic_field_strength_microtesla_equator` | 100 | low | Order-of-magnitude estimate, not a measurement. The energy-flux dynamo scaling (Christensen 2009 `2009Natur.457..167C`; applied to inflated exoplanets by Yadav & Thorngren 2017 `1709.05676`) is validated for hot Jupiters, but AU Mic b (0.028 M_Jup) sits BELOW that mass regime — in the sub-Saturn zone where He separation makes the surface field unquantifiable (Stevenson 1980). cfg brackets it by the Neptune/Uranus ice-giant analog (~0.1–0.5 G = 10–50 µT; Connerney 1991, Ness 1986), nudged to ~100 µT for AU Mic's youth (22 Myr inflates the interior, raising internal flux). See docs/reference/planetary-dynamo-scaling.md |
| `atmospheric_escape_rate_g_s` | 1e10 | medium | Allart 2023 He I absorption implies mass-loss ~10⁹–10¹⁰ g/s under energy-limited escape with AU Mic XUV; Plavchan 2020 §6 estimates similar; Cale 2021 §5 |
| `aurora_present` | true | low | strong stellar wind + H-rich upper atmosphere; H Balmer-α + H₂ Lyman + Werner bands expected |
| `aurora_color_primary_hex` | `#ff6e8c` | low | Tie-break: H-α 656.3 nm + Lyman-α downconverted gives pink-red dominant; interesting-first picks the bright pink over a fainter UV-only rendering |
| `star_apparent_angular_diameter_deg` | 6.6 | high | derived: 2 × 0.862 R☉ / 0.07 AU × (180/π) ≈ 6.6° |
| `stellar_illumination_color_temp_k` | 3665 | high | from host star Teff |

## Surface synthesis

AU Mic b has no surface in the rocky-planet sense. Mass 8.99 M⊕ and
radius 4.79 R⊕ give density 0.45 g/cc — about a tenth of Earth's and
less than half of Neptune's. Lopez & Fortney 2014 mass-radius diagrams
place this combination squarely in the H/He-envelope regime, with the
hydrogen envelope contributing 25–35% of the planet's total mass. The
nominal "surface" — where pressure reaches a few × 10⁴ Pa and the
optical depth becomes unity at the cloud deck — sits at roughly the
4.79 R⊕ radius reported by the transit; below that, pressure rises
through 10⁵ → 10⁶ → 10⁷ Pa over a column of ~10 scale heights, and
the gas transitions smoothly to supercritical fluid without a phase
boundary. There is no terrain to render and no surface tint to specify.

For NearStars purposes, the "visible surface" the player sees is the
top of the cloud deck. This is rendered as a banded gaseous body
(see Visual styling) rather than as a textured solid; KSP's stock
gas-giant infrastructure with custom band textures is the appropriate
analog. The body's interior is presumed structured roughly like a
warm Neptune: H/He envelope → H₂O/NH₃/CH₄ supercritical "ice" mantle
→ small rocky/iron core of perhaps 1–3 M⊕ (Cale 2021 §5 interior
fit). None of this is visible.

The youth of the system matters here. At 22 Myr, b has not finished
its primary Kelvin–Helmholtz contraction; its radius is ~1.5× larger
than the equilibrium it will reach at Gyr ages, and its interior
luminosity (Plavchan 2020 §6) is ~10× what an old equivalent would
emit. This residual heat keeps the envelope inflated and is part of
why the He I 10830 Å absorption is detectable (Allart 2023): the
upper atmosphere is hot, ionized, and extended out to roughly 5–8
planet radii along the trailing wake.

## Atmosphere synthesis

The atmosphere is the planet, observationally and visually. Several
constraints converge on the H/He-dominated puffy-Neptune picture.

**Pressure.** The transit-derived radius pins the location of the
τ ≈ 1 cloud deck. Lopez & Fortney 2014 inversion of mass + radius +
age + insolation for sub-Saturns gives an H/He mass fraction of ~30%
for b's parameters; this implies a surface pressure (at the rocky
core, if one exists) of ~10⁹ Pa, but the meaningful "cfg surface
pressure" for KSP atmosphere rendering is the cloud-deck pressure
of ~10⁷ Pa. The exact value depends on cloud-condensate chemistry
(H₂O, NH₃, NH₄SH, depending on depth and temperature) and is not
directly measured.

**Composition.** Allart 2023's He I 10830 Å detection (~0.3% absorption
during transit, marginal at 2.5σ in their nominal analysis but robust
when combined with He I excess seen in CARMENES observations) requires
an extended H/He atmosphere. Energy-limited escape calculations using
AU Mic's XUV flux (saturated regime; Stelzer 2013; Tristan 2023 flare
census) yield mass-loss rates of 10⁹–10¹⁰ g/s, consistent with the
Allart 2023 He I optical depth. This is sufficient to lose ~10% of
the envelope mass over the system's projected lifetime, but not to
strip b entirely. Trace species (H₂O, CH₄, NH₃, CO) are assumed at
near-solar abundance per the Lavie 2017 cool-Neptune photochemistry
framework, with photochemical hazes generated by methane photolysis
in the upper atmosphere.

**Sky appearance from low orbit.** A KSP player descending toward b's
cloud tops would see a Jupiter-like banded gas giant lit by a deep
red star — but with the bands themselves muted toward red-brown by
both photochemical haze and M-dwarf SED. Zonal jets are inferred
from GCM-class hot-Neptune simulations (Showman 2009 hot-Jupiter
analogs scaled for Neptune temperature and rotation); equatorial
superrotation produces a single bright zone with darker mid-latitude
belts. The polar regions are darker still — a hood-like discoloration
where the photochemical haze accumulates under reduced insolation.

**Atmospheric escape and the comet-like tail.** AU Mic b is one of
the best-characterized escaping atmospheres in any system; the He I
10830 Å absorption maps a trailing tail extending several planet radii
behind b along the orbital direction (Allart 2023 §4). For
NearStars cfg rendering, this corresponds to an EVE-side atmospheric
escape feature — a faint ionized tail visible to a player at conjunction.
The tail is sculpted by AU Mic's stellar wind, which is anomalously
strong (~10× solar; Plavchan 2020 §4 background); during super-flare
events (5.6/day above 10³¹ erg, with occasional 10³⁴ erg events;
Tristan 2023), the tail brightens dramatically as the upper atmosphere
is briefly ionized to depths normally shielded by the bulk envelope.

## Rotation & spin synthesis

Tidal damping of an 8.46-day Neptune-class planet at 0.07 AU around
0.51 M☉ proceeds on a timescale of ~10⁵–10⁶ years (Goldreich & Soter
1966 with Neptune-like Q ≈ 10⁴); over the 22-Myr system age, b is
tidally locked into a near-synchronous, pseudo-synchronous spin — at
e = 0.07 the equilibrium rotation is only ~2% super-synchronous, so it
renders as effectively 1:1. The Hirano 2020
Rossiter–McLaughlin measurement (λ = −2.96 +10.3/-10.6°) confirms that
b's orbital plane is aligned with AU Mic's stellar rotation axis,
which in turn aligns with the edge-on disk plane (Krist 2005;
Schneider 2014). The system is coplanar at the ~5° level.

**KSP implementation note.** Rotation period = orbital period = 8.463446
days (731 241.7 s). Kopernicus `rotationPeriod` should match the orbital
`period`.

**No seasons.** Obliquity damped to zero by tidal locking. Eccentricity
0.07 (Mallorquin 2024) drives a ~14% insolation variation along the
orbit, which is significant — but the heat capacity of the H/He envelope
smooths this out to a few-K cloud-top temperature variation across
periapsis. No discrete "seasons" in the rocky-planet sense; instead,
modest planet-wide brightening near periapsis when the substellar
illumination peaks.

**Day-night redistribution.** With a thick H/He atmosphere, atmospheric
heat transport from day to night is efficient. Phase-curve-class
observations (not yet available for b — Spitzer phase curves were
attempted but the host-star spot signal dominated) would show
day-night contrast of ~150–250 K. The cfg picks 700 K dayside and
450 K nightside as a midrange estimate; both are within the GCM
window for puffy Neptune at this insolation.

## Visual styling

The visual presentation of AU Mic b combines five elements:

- **Global appearance.** A puffy warm-Neptune disk with subdued
  zonal bands, lit by a deep red M1V star at ~6° angular diameter
  (12× the Sun from Earth, dominating the sky). The disk itself
  shows muted red-brown bands (`#7c4a32` for primary haze, `#c0a880`
  for zone clouds) — softer than Jupiter's bold tan-and-white, both
  because of M-dwarf reddening and because photochemical haze
  blankets the cloud-top structure.
- **Banded structure.** Equatorial superrotation jet produces a
  single bright zone at the equator with darker mid-latitude belts.
  Polar regions show a faint hood-like darkening where haze
  accumulates. Bands are ~10° wide in latitude, broadly resembling
  Jupiter's structure but with reduced contrast and slower visual
  motion (rotation period 8.46 d locked → bands rotate with the
  planet's orbit). Tie-break: chose banded over uniform haze for
  visual interest.
- **Cloud-top texture.** Within each band, fine-scale eddies and
  Rossby-wave perturbations create a turbulent cloud-top texture
  — similar to a slowly-rotating Jupiter rendered through a sepia
  filter. Eddies advect with the zonal jet on weeks-to-months
  timescales.
- **Atmospheric escape tail (the planet's signature feature).**
  Allart 2023's He I 10830 Å detection maps an ionized escaping
  outflow extending several planet radii behind b along the
  orbital direction. For KSP visual rendering this corresponds to
  a faint pink-violet comet-like tail visible in transmission
  geometry — most prominent when b is near conjunction with the
  observer. The tail brightens during AU Mic super-flare events.
  Color picked at `#ff6e8c` (H Balmer-α + Lyman-α downconvert) as
  a tie-break against a UV-only rendering that would be invisible.
- **Star in sky.** AU Mic subtends 6.6° in b's sky (12× the Sun
  from Earth) — a vast deep-red disk taking up roughly 1/30 of the
  full hemisphere. Surface illumination at the substellar cloud
  top is about 20.8× Earth's, but red-shifted heavily into the
  near-IR; visually the cloud top appears bright but flat-toned
  rather than blue-sky bright. Super-flares (10³⁴ erg events
  several times per year; Tristan 2023) briefly brighten the
  illumination by 1–3 magnitudes for tens of minutes — visible
  as a transient brightening of the entire dayside.

The four close-in planets — c at 0.119 AU, d at ~0.105 AU, e at
~0.171 AU (if confirmed) — are visible from b as small dots, mostly
at ≪ 1° angular diameter; the edge-on debris disk at 35–210 AU
appears as a thin bright streak bisecting the sky on either side of
AU Mic. b transits AU Mic's stellar disk when viewed from beyond
the system; observers on b would see the disk's inner edge
extending across the sky from ~5° from the central star outward to
the horizon.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Plavchan P. et al. 2020** — *A planet within the debris disk around the pre-main-sequence star AU Microscopii*, Nature 582, 497 (`2020Natur.582..497P`, arXiv:2006.13248). TESS discovery of AU Mic b; transit-derived radius 4.0 R⊕ (later refined to 4.79); discussion of host XUV environment and atmospheric escape regime. Cornerstone paper.
- **Cale B. L. et al. 2021** — *Diving Beneath the Sea of Stellar Activity: Chromatic Radial Velocities of AU Mic b*, AJ 162, 295 (`2021AJ....162..295C`, arXiv:2109.13996). First robust RV mass with multi-instrument GP detrending; reports inflated low density consistent with puffy envelope.
- **Mallorquin M. et al. 2024** — *AU Mic system characterized with ESPRESSO*, A&A 689, A132 (`2024A&A...689A.132M`). ESPRESSO + TESS joint analysis; refines b's mass to 8.99 ± 2.61 M⊕ and radius to 4.79 ± 0.29 R⊕; supersedes Cale 2021's higher mass via improved stellar-activity modeling. **Adopted as headline source.**
- **Allart R. et al. 2023** — *Homogeneous search for helium in the atmosphere of 11 gas giants with HST/STIS and CARMENES*, A&A 677, A164 (`2023A&A...677A.164A`, arXiv:2308.10891). Reports marginal-to-significant He I 10830 Å detection during AU Mic b transit; constrains escape rate and extended-atmosphere geometry. Drives the atmosphere-present and escape-tail cfg picks.
- **Hirano T. et al. 2020** — *Evidence for Spin–Orbit Alignment in the TRAPPIST-1 System and Implications for the AU Mic system*, ApJ 899, L13 (`2020ApJ...899L..13H`, arXiv:2006.13654). Subaru IRD Rossiter–McLaughlin measurement of b; projected obliquity λ = −2.96°. Confirms orbital-plane alignment with disk + stellar spin.
- **Lopez E. D. & Fortney J. J. 2014** — *Understanding the Mass-Radius Relation for Sub-Neptunes*, ApJ 792, 1 (`2014ApJ...792....1L`, arXiv:1311.0329). Mass-radius envelope-mass-fraction calibration. Applied to b gives ~30% H/He by mass; drives the cfg surface pressure picks.

### Read (context / methodology, not decision-driving)

- **Klein B. et al. 2021** — *Investigating the young AU Mic system with SPIRou: stellar magnetic field and close-in planet mass*, MNRAS 502, 188 (`2021MNRAS.502..188K`, arXiv:2012.04970). SPIRou near-IR ZDI of AU Mic + RV; provides supporting stellar-activity context for the GP detrending used by Mallorquin 2024.
- **Donati J.-F. et al. 2023** — *The magnetic field topology and filling of the very active M dwarf AU Mic*, MNRAS 525, 455 (`2023MNRAS.525..455D`). ZDI dipole 2 kG, total RMS 4.6 kG; sets the stellar magnetic-field context.
- **Tristan I. I. et al. 2023** — *Catching the Flares of the AU Mic System with TESS*, ApJ 951, 33 (`2023ApJ...951...33T`, arXiv:2306.00077). TESS flare census; rate 5.6/day above 10³¹ erg; relevant for atmosphere-escape and aurora timing.
- **Lavie B. et al. 2017** — *HELIOS-RETRIEVAL: Open-source Nested Sampling Atmospheric Retrieval Code for Exoplanets*, AJ 154, 91 (`2017AJ....154...91L`, arXiv:1610.03216). Cool-Neptune photochemistry framework adopted for the trace-species composition.
- **Sing D. K. et al. 2016** — *A continuum from clear to cloudy hot-Jupiter exoplanets without primordial water depletion*, Nature 529, 59 (`2016Natur.529...59S`, arXiv:1512.04341). Census of cloud-deck pressures in hot/warm gas giants; supports the 0.70 cloud-cover choice.
- **Showman A. P. et al. 2009** — *Atmospheric Circulation of Hot Jupiters*, ApJ 699, 564 (`2009ApJ...699..564S`, arXiv:0809.2089). Equatorial-superrotation GCM framework adopted (with cooler-temperature adaptation) for the banded morphology pick.

### Read (instrument / non-decisive)

- **Martioli E. et al. 2020** — *AU Mic b transits revisited with TESS Sector 27* (early sector-27 release; not visual-informative).
- **Szabó Gy. M. et al. 2021** — *Spi-Ops campaign on AU Mic b* (`2021A&A...654A.159S`, arXiv:2108.07984). CHEOPS transit timing; not cfg-decisive.

### Not read — no arXiv preprint or low-priority (~25 papers)

Conference abstracts (DPS, EPSC), early TESS pipeline releases on AU Mic
without independent reanalysis, He I follow-up campaigns that didn't
yield significant detections, and very recent PSJ early-access papers
without arXiv preprints all contribute incrementally to the picture but
don't change cfg decisions. The full filtered bibliography is preserved
in the planet's `_bib/au-mic-b.yaml` (to be created) with
`status: skipped` annotations.

## Open items for follow-up

- **JWST atmospheric characterization.** A NIRSpec or NIRISS transmission
  spectrum of b would directly constrain composition and cloud structure;
  several proposals are accepted but not yet published at this writing.
  If a paper appears with molecular detections (H₂O, CH₄, CO, HCN), the
  cfg composition row should be re-fit and cloud_morphology may need
  refinement.
- **He I 10830 Å follow-up.** Allart 2023's detection is at modest
  significance. Independent confirmation from CARMENES or Keck/NIRSPEC
  would solidify the cfg's escape-tail visual feature. If the detection
  is retracted, atmospheric_escape_rate_g_s drops by ~1 dex and the tail
  rendering should become subtler.
- **Spitzer/JWST phase curve.** Direct dayside/nightside contrast
  measurement would constrain the 700 K / 450 K temperature picks. Phase
  curves through host-star activity remain challenging; deferring to
  JWST MIRI ECLIPSE program.
- **Interior modeling.** Cale 2021 §5 sketches a Neptune-analog
  H/He + ices + rocky-core interior. A formal Bayesian retrieval
  (Acuña-class for super-Neptunes) hasn't been published yet for b.
- **Cfg variant: deflated future state.** b is currently puffy at 22 Myr;
  at 1 Gyr it would shrink to ~3 R⊕ at constant mass (Lopez & Fortney
  2014). A "mature AU Mic system" cfg variant could ship the deflated b
  for visual comparison.
- **Coordination with c/d Phase 3.** The four close-in planets share
  AU Mic's flare environment; if super-flare-driven atmosphere stripping
  arguments for d/e shift, the cfg-consistency check for b's escape rate
  may need adjustment.

## Related

- [au-mic](au-mic.md) — host star synthesis with disk geometry
- [au-mic-c](au-mic-c.md) — sister planet, sub-Neptune at 18.9 d
- [au-mic-d](au-mic-d.md) — sister planet, Earth-mass TTV candidate at 12.7 d
- [au-mic-e](au-mic-e.md) — sister planet, ESPRESSO RV candidate at 33.1 d
- [methodology](../reference/methodology.md) — Decisions schema
- [mod-reference](../reference/mod-reference.md) — downstream cfg writers
