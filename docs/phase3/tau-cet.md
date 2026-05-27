<!-- tau Ceti Phase 3 synthesis: cfg-ready decisions and reasoning -->
# τ Ceti — Phase 3 Synthesis

τ Ceti (HD 10700, HIP 8102, GJ 71) is the nearest single G-type
star to the Sun at 3.652 ± 0.002 pc / 11.91 ly — Gaia DR3 parallax
273.81 ± 0.17 mas (DB Phase 2). Spectral type G8V (Gray 2006), it
sits at the cool, faint end of the solar analog locus with M =
0.783 ± 0.012 M☉ (Feng 2017), R = 0.793 ± 0.004 R☉ (Teixeira 2009
asteroseismology + Di Folco 2007 interferometry), and Teff =
5344 ± 50 K (Pavlenko 2012). Its defining property among nearby
G dwarfs is an unusually low metallicity, [Fe/H] = −0.55 ± 0.05
(Pavlenko 2012; Santos 2013 reports −0.49 ± 0.05 in good
agreement) — exceptionally iron-poor for a planet host and roughly
0.8 dex below the α Cen A reference.

τ Ceti's other distinguishing features are an old, kinematically
quiet history and a prominent cold debris disk. Pavlenko 2012
places τ Ceti in the Eggen 1971 super-population of old disk
stars; combined with the 34-day rotation period (Baliunas 1996 Mt
Wilson Ca II H&K monitoring) and the gyrochronological calibration
of Mamajek & Hillenbrand 2008, this gives an age of 7 ± 1.5 Gyr.
Chromospheric activity is extreme in the *quiet* direction:
log R'HK = −4.95 (Pavlenko 2012) places τ Ceti among the most
inactive G dwarfs in the HK survey, with X-ray emission below the
EXOSAT detection threshold (Schmitt 1985, log L_X ≤ 26.5).
Surrounding the star is a cold, broad debris disk first detected
in SCUBA submillimeter excess by Greaves 2004 and resolved by ALMA
Band 6 imaging in MacGregor 2016 as a single ring spanning roughly
6 to 55 AU with a total dust mass ~10–20× that of the solar
Kuiper Belt — the closest resolved debris-disk analog to our own
outer Solar System.

The Phase 2 DB records four confirmed planets from Feng 2017
(e, f, g, h), but τ Ceti e is absent from `db/systems/tau_cet.json`
while f, g, and h are present; the rex-data-comparison reference
flags this as a curation question (Feng 2017 lists the same dispute
flag for all four). This stellar synthesis therefore covers only
the host; planet f / g / h Phase 3 work is deferred to a follow-up
workspace, and the τ Cet e curation question is logged as an Open
item.

**Scenario choice for NearStars: a quiet, old, metal-poor G8V
roughly 80% of the Sun's mass and 46% of its luminosity, with a
slightly cooler-yellow visual tint than Sol, viewed against the
backdrop of a broad ALMA-resolved cold debris belt at 6–55 AU
and the f / g / h planet system as faint inner points.** 22 cfg
picks: 18 canonical-aligned, 4 tie-break (visual hex, disk hex,
disk opacity, disk morphology compositional inference).

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | G8V | high | Gray 2006; SIMBAD; DB |
| `mass_msun` | 0.783 ± 0.012 | high | Feng 2017 — M–K relation with Mann 2015 calibration; Teixeira 2009 asteroseismic 0.783 ± 0.012 agrees |
| `radius_rsun` | 0.793 ± 0.004 | high | Teixeira 2009 asteroseismic + Di Folco 2007 VLTI/VINCI interferometry |
| `teff_k` | 5344 ± 50 | high | Pavlenko 2012 — high-resolution spectroscopy, differential to Sun; Santos 2013 = 5333 ± 20 K within 1σ |
| `luminosity_lsun` | 0.457 | high | derived from R and Teff via Stefan–Boltzmann |
| `metallicity_fe_h_dex` | −0.55 ± 0.05 | high | Pavlenko 2012 — differential LTE analysis vs Sun; Santos 2013 = −0.49 ± 0.05 within 1σ |
| `age_gyr` | 7.0 ± 1.5 | medium | Pavlenko 2012 — Eggen 1971 super-population kinematics + chromospheric activity proxy; Mamajek & Hillenbrand 2008 gyrochronology from 34-d rotation agrees on 6–8 Gyr |
| `rotation_period_days` | 34 | high | Baliunas 1996 — Mt Wilson Ca II H&K timeseries; Pavlenko 2012 confirms |
| `activity_log_rhk` | −4.95 | high | Pavlenko 2012 — among the most inactive G dwarfs in the HK survey |
| `x_ray_log_lx_cgs_max` | 26.5 | medium | Schmitt 1985 — EXOSAT non-detection upper limit; Judge 2004 confirms quiescent FUV emission |
| `visual_surface_tint_hex_primary` | `#ffe9c8` (cream-yellow, slightly less yellow than Sol) | medium | Tie-break: G8V blackbody at 5344 K + metal-poor SED is marginally bluer than solar-metallicity equivalent (less line blanketing in the blue at [Fe/H] = −0.55); interesting-first per the interesting-first rule for visual distinction from α Cen A's metal-rich cream |
| `stellar_color_temp_k` | 5344 | high | derived from Teff |
| `disk_present` | true | high | Greaves 2004 SCUBA 850 μm excess; MacGregor 2016 ALMA Band 6 resolved imaging |
| `disk_inner_radius_au` | 6 | high | MacGregor 2016 — ALMA resolved fit, inner edge ~6 AU |
| `disk_outer_radius_au` | 55 | high | MacGregor 2016 — ALMA resolved fit, outer edge ~55 AU |
| `disk_dust_temperature_k` | 60 | high | MacGregor 2016 SED + Greaves 2004 60–80 K consistent |
| `disk_tint_rgb_hex` | `#b8aa9c` (warm grey-brown, metal-poor analog of Kuiper Belt) | low | Tie-break: composition not directly measured; cfg adopts a slightly less reddened tint than the Sol KBO reference to reflect the metal-poor parent star (less iron in primordial grain population); interesting-first per the interesting-first rule |
| `disk_opacity` | 0.15 | low | Tie-break: physical optical depth is ~10⁻³ from MacGregor 2016 dust mass + ring geometry, but cfg uses 0.15 for in-game visibility against deep-space background; documented as a render-visibility tradeoff |
| `disk_morphology` | "broad single ring, metal-poor analog of Kuiper Belt" | high | MacGregor 2016 §3 — single broad ring explicitly favored over multi-belt; no resolved inner gap |
| `disk_resolved_imaging` | true | high | MacGregor 2016 — ALMA Band 6 resolved |
| `disk_imaging_observatory` | ALMA | high | MacGregor 2016 |
| `disk_mass_mearth` | 1.2 | medium | MacGregor 2016 fit — ~10–20× Sol KBO dust mass (Sol KBO ≈ 0.01 M⊕ dust) |
| `disk_planetesimal_belt_inferred` | true | high | MacGregor 2016 §5 — collisional cascade requires a parent planetesimal body belt to replenish the dust |

## Surface synthesis

τ Ceti's photosphere is a colder, older, and substantially more
iron-poor cousin of the Sun. The effective temperature of 5344 K
sits 433 K below Sol's 5777 K; combined with R = 0.793 R☉, the
Stefan–Boltzmann bolometric luminosity is 0.457 L☉, a little under
half the solar reference. The G8V classification (Gray 2006) places
τ Ceti at the cool faint end of the solar analog band, comparable
in temperature to ε Eridani's K2V but with the lower-gravity
envelope of a true G dwarf rather than a young K star.

The metallicity [Fe/H] = −0.55 (Pavlenko 2012) is the headline
distinguishing feature. At nearly four times less iron than the
Sun, line blanketing in the blue continuum is correspondingly
weaker, and the integrated visible SED is marginally bluer than a
solar-metallicity G8V would be at the same Teff — the difference is
small (~10–20 K equivalent blue-shift) but enough to push the
cfg surface tint away from the warm-cream of α Cen A's +0.24 dex
metallicity toward a cleaner pale-yellow. Santos 2013's
[Fe/H] = −0.49 ± 0.05 measurement is statistically consistent and
reinforces the picture, with the two analyses differing primarily
in the model atmosphere grid used; Pavlenko 2012's differential
analysis against the Sun is preferred as the cleaner observable.

Granulation is not directly imaged but is predicted to be Sun-like
in pattern and somewhat slower in timescale because of the lower
photospheric temperature (acoustic cut-off scales as √g/√T_eff,
giving τ Ceti's p-mode oscillations a slightly longer characteristic
period than the Sun's 5-minute oscillation). Teixeira 2009 detected
the p-mode spectrum with HARPS, finding Δν = 169.0 ± 0.5 μHz and
ν_max ≈ 4490 μHz, consistent with the asteroseismic radius and mass
adopted above. Limb darkening is not directly measured in H band
(no VLTI interferometric campaign of τ Ceti at the precision of
Kervella 2017 on α Cen A); the cfg leaves `limb_darkening_alpha_h`
unfilled and adopts the Sun-like default in the downstream renderer.

Sunspot coverage is essentially undetectable at the photometric
precision of long-term ground-based monitoring. With log R'HK =
−4.95, τ Ceti is fractionally less active than α Cen A and well
below the modern Sun — chromospheric Ca II H&K emission shows no
detectable cycle in the Baliunas 1996 record, consistent with a
saturated-quiet regime expected for old, slowly rotating, low-
metallicity G dwarfs.

## Atmosphere synthesis

The chromosphere–transition-region–corona structure of τ Ceti is
the canonical quiet G-dwarf reference. Pavlenko 2012's
log R'HK = −4.95 places the chromospheric Ca II H&K emission near
the basal flux floor — the minimum expected from acoustic heating
alone, with no detectable magnetic-cycle modulation. Hα is in
absorption with no measurable variability.

X-ray emission is below the EXOSAT detection threshold: Schmitt
1985 reports an upper limit log L_X ≤ 26.5 cgs (0.1–2.4 keV).
Subsequent XMM-Newton and Chandra pointings (catalogued in Judge
2004 and subsequent compilations) have not produced a clean
detection, and the quiescent corona is fainter than that of α Cen A
during cycle minimum. There is no evidence of any X-ray activity
cycle. FUV continuum emission (Judge 2004) is correspondingly weak,
implying a transition region thinner and cooler than the modern
Sun's.

Flares are not detected. Long-term photometric monitoring (HIPPARCOS,
Mt Wilson) shows no impulsive brightening events above the noise
floor, and the surface magnetic field is below the Zeeman-broadening
detection limit of ~50 G in the available high-resolution
spectroscopy. The integrated XUV luminosity is well below 10⁻⁵ L_bol
and would not materially erode an Earth-like atmosphere over Gyr
timescales at any of the f / g / h planet orbits.

The implication for the planet roster is an exceptionally benign
space-weather environment, distinctly milder than even the quiet
α Cen A. Any inner-planet atmospheric escape calculation defaults
to thermal Jeans loss without the augmented hydrodynamic loss
driven by stellar XUV that is the rule for K and M dwarfs.

## Rotation & spin synthesis

τ Ceti rotates with a period of 34 days (Baliunas 1996 Mt Wilson
Ca II H&K monitoring, confirmed by Pavlenko 2012 from combined HK
and photometric data). Some recent zeeman-doppler imaging (Boro
Saikia 2018) prefers a 46 d period, but the HK-traced 34 d value
remains the canonical reference and matches the Skumanich braking
expectation for a 7 Gyr old G8V — P_rot ∝ √t, anchored to the
solar 25-day rotation at 4.6 Gyr, predicts ~31 days at 7 Gyr,
within the measurement scatter of 34 d.

The slow rotation is consistent with the old age inferred from
Pavlenko 2012's Eggen 1971 super-population kinematic membership
and Mamajek & Hillenbrand 2008's gyrochronological calibration
applied to the 34-d period (which yields 6.5 Gyr from the
Skumanich law with their B–V color). The combined age estimate of
7.0 ± 1.5 Gyr is the cfg adoption, with the uncertainty range
spanning both gyrochronology and kinematic estimates.

Asteroseismic p-mode oscillations were detected by Teixeira 2009
in 8 nights of HARPS RV monitoring: Δν = 169.0 ± 0.5 μHz, ν_max ≈
4490 μHz. The acoustic timescale 2π/Δν ≈ 1.6 h is shorter than the
solar 5-minute oscillation when scaled correctly by the smaller
radius and higher mean sound speed; this constrains the mass to
0.783 ± 0.012 M☉ and the radius to 0.793 ± 0.004 R☉ with
percent-level precision, the values adopted in the Decisions table.

Differential rotation is not resolved. The rotation axis
inclination is poorly constrained; for visual rendering NearStars
adopts a default ~30° tilt to the line of sight consistent with a
randomly oriented spin axis.

## Visual styling

In the NearStars renderer, τ Ceti is portrayed as a slightly cooler
and visibly more pale-yellow star than α Cen A. The surface tint
hex `#ffe9c8` encodes a cream-yellow with marginally less warmth
than the canonical solar `#fff8f0` or α Cen A's metal-rich
`#fff4e8` — the metal-poor SED is the physical reason, captured by
the tie-break rule. The chosen tint sits between Sol-yellow and a
hypothetical pure G8V blackbody, biased toward visual
distinguishability from the catalog's other yellow dwarfs in
side-by-side comparison.

At 11.91 ly (3.65 pc) viewed from Earth, the apparent magnitude
V = 3.5 makes τ Ceti easily visible to the naked eye as a faint
naked-eye solitary star in Cetus — culturally the nearest single
Sun-like star and a long-standing SETI target since Drake's
Project Ozma in 1960. From a candidate planet in the τ Ceti
habitable zone (planet f at 1.334 AU is the relevant case), the
star would fill ≈ 0.34° angular diameter, smaller than the Sun
seen from Earth (0.53°) because of f's larger orbital radius. The
illumination color seen from f's surface is the same warm cream
tint shifted toward a slightly cleaner pale-yellow by the
combination of metal-poor SED and cooler Teff.

Sunspots and faculae are not rendered as animated features —
τ Ceti is too quiet to show resolved activity at the precision
of the NearStars renderer. The X-ray and chromospheric output are
encoded as a flat baseline with no cycle modulation, contrasting
sharply with α Cen A's 19-year Sun-like cycle.

The defining visual element of the system is the cold debris
disk. ALMA Band 6 imaging (MacGregor 2016) resolves a single broad
ring extending from ~6 AU (inner edge) to ~55 AU (outer edge),
with a peak surface density around 30 AU and a total dust mass of
roughly 1.2 M⊕ — about 10–20× the dust inventory of our own
Kuiper Belt. NearStars renders this as a faint, broad, dimly
amber-grey annulus around τ Ceti, encoded with hex `#b8aa9c` and
in-game opacity 0.15 (physical optical depth is ~10⁻³, but the
cfg uses a higher visibility setting so the belt is recognizable
against the deep-space background). The belt has no inner gap or
shepherding structure resolved at ALMA precision, so the cfg ring
is uniform across its 6–55 AU width. The metal-poor parent star
likely formed grains slightly less iron-reddened than the Sol KBO
analog, justifying a more achromatic grey-brown rather than the
warmer ochre of a solar-metallicity Kuiper Belt — this is a
tie-break documented in Basis.

Planet f / g / h are rendered as faint inner points all interior
to the disk's inner edge (f at 1.33 AU, h at 0.24 AU, g at 0.13 AU
— all well within the 6 AU disk inner edge). The visual contrast
of the inner planet system against the broad outer dust belt is
the system's signature framing in the NearStars renderer, distinct
from the planet-only inner systems (TRAPPIST-1, Proxima) and the
binary-pair framings (α Cen A/B).

## Bibliography

### Read (visual-informative, drove decisions above)

- **Greaves J. S. et al. 2004** — *The debris disk around τ Ceti:
  a massive analogue to the Kuiper Belt*, MNRAS 351, L54
  (`2004MNRAS.351L..54G`). JCMT/SCUBA 850 μm detection of cold
  dust excess; first identification of τ Ceti's debris disk as a
  KBO analog ~10× more massive than the Sun's.
- **MacGregor M. A. et al. 2016** — *Constraints on planetesimal
  collision models in debris disks*, ApJ 828, 113
  (`2016ApJ...828..113M`, arXiv:1607.06900). ALMA Band 6 resolved
  imaging of τ Ceti's disk; single broad ring 6–55 AU; dust mass
  ~1.2 M⊕; collisional cascade requires a parent planetesimal
  body belt. Anchors all `disk_*` Decisions rows.
- **Pavlenko Y. V. et al. 2012** — *Spectral analysis of τ Ceti:
  abundances and age*, MNRAS 422, 542 (`2012MNRAS.422..542P`,
  arXiv:1112.1709). Differential LTE analysis vs Sun;
  [Fe/H] = −0.55 ± 0.05; log R'HK = −4.95; Eggen 1971
  super-population age 7 ± 1 Gyr. Anchors metallicity, activity,
  age Decisions rows.
- **Santos N. C. et al. 2013** — *SWEET-Cat: A catalogue of
  parameters for stars with exoplanets*, A&A 556, A150
  (`2013A&A...556A.150S`, arXiv:1307.0354). Independent
  spectroscopic [Fe/H] = −0.49 ± 0.05 and Teff = 5333 ± 20 K,
  confirming Pavlenko 2012 within 1σ.
- **Feng F. et al. 2017** — *Color difference makes a difference:
  four planet candidates around τ Ceti*, AJ 154, 135
  (`2017AJ....154..135F`, arXiv:1708.02051). Four-planet RV
  discovery (e, f, g, h); host mass M = 0.783 ± 0.012 M☉ adopted
  for the Decisions table. The DB Phase 2 stores planets f, g, h
  but omits e (see Open items).
- **Mamajek E. E. & Hillenbrand L. A. 2008** — *Improved age
  estimation for solar-type dwarfs using activity-rotation
  diagnostics*, ApJ 687, 1264 (`2008ApJ...687.1264M`,
  arXiv:0807.1686). Gyrochronological calibration applied to
  τ Ceti's 34-d rotation yields ~6.5 Gyr, agreeing with Pavlenko
  2012's kinematic age.
- **Baliunas S. L. et al. 1996** — *Chromospheric variations in
  main-sequence stars II*, ApJ 438, 269 (`1995ApJ...438..269B`).
  Mt Wilson Ca II H&K survey; τ Ceti rotation period 34 d;
  exceptionally flat HK record without resolved cycle.

### Read (context / methodology, not directly decision-driving)

- **Teixeira T. C. et al. 2009** — *Solar-like oscillations in
  τ Ceti*, A&A 494, 237 (`2009A&A...494..237T`, arXiv:0811.3989).
  HARPS p-mode detection; Δν = 169.0 ± 0.5 μHz, ν_max ≈ 4490 μHz;
  asteroseismic mass and radius cross-check.
- **Di Folco E. et al. 2007** — *VLTI/VINCI interferometric
  diameters of nearby exoplanet host stars*, A&A 475, 243
  (`2007A&A...475..243D`, arXiv:0710.1731). VINCI K-band angular
  diameter; consistent with Teixeira 2009 asteroseismic radius.
- **Schmitt J. H. M. M. et al. 1985** — *EXOSAT observations of
  nearby stars: τ Ceti upper limit*. log L_X ≤ 26.5 non-detection;
  quiescent corona reference.
- **Judge P. G. et al. 2004** — *FUV spectroscopy of τ Ceti from
  FUSE: chromospheric basal flux*, ApJ 613, 1306. Quiescent
  chromosphere reference; basal flux floor.
- **Gray R. O. et al. 2006** — *Contributions to the Nearby Stars
  (NStars) Project: spectroscopy of stars within 40 pc — south*.
  G8V spectral classification.
- **Boro Saikia S. et al. 2018** — *Solar-type magnetic activity
  on τ Ceti from ZDI*, A&A 620, L11. Zeeman-Doppler-imaging
  prefers 46 d rotation; cfg retains 34 d Baliunas 1996 canonical
  value (see Decisions Basis).

### Read (instrument / non-cfg-decisive)

- **Lawler S. M. et al. 2014** — *Debris disks of τ Ceti and
  ε Eridani: SED modeling* (arXiv:1409.0023). SED-fit dust
  temperature and inferred grain size; superseded by MacGregor
  2016 resolved imaging.

### Not read — no arXiv preprint or low-priority (~40 papers)

SETI / laser-emission searches (Tarter 1981 Project Ozma followup,
Tellis 2017, Margot 2018), conference abstracts (EPSC/AGU/DPS), and
astrobiological habitability speculation papers contribute no
cfg-decisive content for the host star. The full filtered bib is
preserved in `docs/phase3/_bib/tau-cet.yaml` with `status: skipped`
annotations.

## Open items for follow-up

- **Phase 2 disk_measurements + planet measurements re-ingest.**
  The DB Phase 2 currently has no `disk_measurements` block for
  τ Ceti — Greaves 2004 and MacGregor 2016 are cited only via this
  Phase 3 synthesis. A future DB schema migration should add a
  `disk_measurements: []` array under each star with appropriate
  entries from MacGregor 2016 (inner/outer radius, dust mass,
  resolved imaging flag). Similarly, the planet f / g / h
  curated entries currently lack physical parameters beyond
  Msini — radius columns from Feng 2017 should be re-verified
  against the original paper.
- **τ Ceti e curation revisit.** The
  [rex-data-comparison](../reference/rex-data-comparison.md) §6
  documents that NearStars stores planets f, g, h from Feng 2017
  but omits e, despite all four having the same `pl_controv_flag`
  in the source. Either deliberately dropped (e was the most
  disputed of the four detections — Feng 2017 §6 cautions about
  its inferior amplitude-to-noise ratio) or an oversight in the
  Phase 2 ingest. Should be documented in
  `db/systems/tau_cet.json::meta.notes` either way, and the
  follow-up Phase 3 planet workspace should decide whether to
  include e or formally drop it with cited justification.
- **Planet f / g / h Phase 3 follow-up workspace.** This
  stellar-only synthesis defers the planet system to a separate
  Phase 3 workspace. Required inputs: Feng 2017 mass / period /
  semi-major axis (already in DB), plus literature-direct
  radius and equilibrium-temperature estimates that the DB does
  not yet carry. Once Phase 2 planet measurements are
  re-ingested per the first item, the planet workspace can
  proceed.
- **τ Ceti age precision.** The adopted 7.0 ± 1.5 Gyr spans both
  Pavlenko 2012's super-population kinematic estimate and
  Mamajek 2008's gyrochronological estimate. A future Gaia DR4
  or future asteroseismic-evolutionary modeling campaign (Joyce
  & Chaboyer 2018 methodology applied to τ Ceti's HARPS p-modes)
  could tighten this to ±0.5 Gyr, which would affect the
  habitability-history modeling for any planet f / g / h
  follow-up.
- **Disk inner-edge fine structure.** MacGregor 2016 ALMA
  imaging is consistent with a clean inner edge at ~6 AU but
  does not rule out a faint inner extension or a shepherding
  feature beyond the noise floor. A future deeper ALMA campaign
  or JWST/MIRI direct imaging could detect inner-belt dust that
  the current cfg ignores; a subsequent Phase 3 revision could
  add a second inner-belt Decisions row if needed.

## Related

- [alpha-centauri-a](alpha-centauri-a.md) — nearest single G2V (metal-rich, +0.24 dex); structural template for this synthesis
- [proxima-cen](proxima-cen.md) — nearest M dwarf, sharp contrast in activity and visual styling
- [methodology](../reference/methodology.md) — schema source for the Decisions table
- [rex-data-comparison](../reference/rex-data-comparison.md) — §6 documents the τ Ceti e curation gap that this synthesis logs as an Open item
- entity pages in `docs/phase3/*.md` — sibling Phase 3 syntheses
