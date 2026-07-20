<!-- tau Ceti Phase 3 synthesis: cfg-ready decisions and reasoning -->
# τ Ceti — Phase 3 Synthesis

τ Ceti (HD 10700, HIP 8102, GJ 71) is the nearest single G-type
star to the Sun at 3.652 ± 0.002 pc / 11.91 ly — Gaia DR3 parallax
273.81 ± 0.17 mas (DB Phase 2). Spectral type G8.5 V (Gray et al.
2006 NStars), it sits at the cool, faint end of the solar analog
locus with M = 0.783 ± 0.012 M☉ (Teixeira 2009 asteroseismology),
R = 0.793 ± 0.004 R☉ (Korolik 2023 CHARA/MIRC-X interferometry,
θ_LD 2.019 mas), and Teff = 5370 ± 20 K (Korolik 2023 interferometric
θ_LD + Boyajian 2013 bolometric flux). Its defining property among
nearby G dwarfs is an unusually low metallicity, [Fe/H] = −0.52 ± 0.01
(Santos 2013) — exceptionally iron-poor for a planet host and roughly
0.8 dex below the α Cen A reference.

τ Ceti's other distinguishing features are an old, kinematically
quiet history and a prominent cold debris disk. The age is a
documented divergence (see Canonical alternatives): the cfg adopts
the Di Folco 2004 isochrone value ~10 Gyr (adopted by Korolik 2023),
consistent with the very low activity and slow rotation, against the
Mamajek & Hillenbrand 2008 activity-age of 5.8 Gyr, within a literature
range of 4.4–12.4 Gyr. No direct photometric rotation period exists —
τ Ceti is nearly pole-on (i = 7 ± 7°, v sin i ~0.1 km/s), so the cfg
carries the Korolik 2023 gyrochronological 46 ± 4 d (against the
Baliunas 1996 Ca II HK ~34 d). Chromospheric activity is extreme in
the *quiet* direction: log R'HK = −4.977 (Gomes da Silva 2021) places
τ Ceti among the most inactive G dwarfs — though Gomes da Silva caution
that it is NOT a flat standard, showing ~11 yr cyclic variability plus
a long-term declining trend. X-ray emission is below the historical
EXOSAT threshold (Schmitt 1985, log L_X ≤ 26.5; no measurement in the
Phase 2 layer).
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
and the f / g / h planet system as faint inner points.** ~24 cfg
picks; the stellar layer is re-anchored on the frozen Phase 2 sources
(Korolik 2023 interferometry, Teixeira 2009 asteroseismology, Santos
2013, Gomes da Silva 2021) with documented age + rotation divergences.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | G8.5 V | high | Gray et al. 2006 (NStars); DB |
| `mass_msun` | 0.783 ± 0.012 | high | Teixeira 2009 — asteroseismic mean density + interferometric radius (Phase 2 recommended); Korolik 2023 g·R² mass 0.69 ± 0.09 is the alternative |
| `radius_rsun` | 0.793 ± 0.004 | high | Korolik 2023 — CHARA/MIRC-X interferometry, θ_LD 2.019 ± 0.012 mas (Phase 2 recommended; supersedes Teixeira 2009 / Di Folco 2007, same 0.793) |
| `teff_k` | 5370 ± 20 | high | Korolik 2023 — interferometric θ_LD + Boyajian 2013 bolometric flux (Phase 2 recommended; spectroscopic Korolik 5320 / Santos 2013 5310 are alternatives; supersedes the Pavlenko 2012 5344) |
| `luminosity_lsun` | 0.488 ± 0.010 | high | Teixeira 2009 — M_V + bolometric correction (Phase 2 recommended; consistent with R 0.793, Teff 5370 via Stefan–Boltzmann) |
| `metallicity_fe_h_dex` | −0.52 ± 0.01 | high | Santos 2013 (SWEET-Cat; Phase 2 recommended) — very metal-poor; Bruntt 2010 −0.18 is the rejected α-enhanced outlier |
| `age_gyr` | 10 | medium | Di Folco 2004 isochrone (Phase 2 recommended, adopted by Korolik 2023), consistent with the very low activity + slow rotation. DOCUMENTED DIVERGENCE vs Mamajek 2008 activity-age 5.8 Gyr; literature range 4.4–12.4 Gyr (see Canonical alternatives) |
| `rotation_period_days` | 46 ± 4 | medium | Korolik 2023 gyrochronology (Phase 2 recommended; method=unverified — NO direct photometric period, the star is pole-on). DOCUMENTED DIVERGENCE vs Baliunas 1996 Ca II HK ~34 d (see Canonical alternatives) |
| `activity_log_rhk` | −4.977 | high | Gomes da Silva 2021 — AMBRE-HARPS (Phase 2 recommended; Mamajek 2008 −4.958 corroborates; supersedes Pavlenko 2012 −4.95) |
| `activity_cycle_years` | ~11 | low | Gomes da Silva 2021 — a ~11 yr cyclic variability with a superimposed long-term declining trend (GdS explicitly warn τ Cet is NOT a flat activity standard) |
| `limb_darkening_alpha_h` | 0.14 ± 0.03 | medium | Korolik 2023 — H-band linear limb-darkening fit from the CHARA/MIRC-X visibilities |
| `spin_axis_inclination_deg` | 7 ± 7 | medium | Korolik 2023 — nearly pole-on (v sin i ~0.1 km/s vs v_eq from R + P_gyro); the disk axis (i ~35°, Lawler 2014) is misaligned |
| `visual_surface_tint_hex_primary` | `#ffe9c8` (cream-yellow, slightly less yellow than Sol) | medium | Tie-break: G8.5 V blackbody at 5370 K + metal-poor SED is marginally bluer than a solar-metallicity equivalent (less blue line blanketing at [Fe/H] = −0.52); distinguished from α Cen A's metal-rich cream |
| `stellar_color_temp_k` | 5370 | high | derived from Teff (Korolik 2023) |
| `disk_present` | true | high | Greaves 2004 SCUBA 850 μm excess; MacGregor 2016 ALMA Band 6 resolved imaging |
| `disk_inner_radius_au` | 6 | high | MacGregor 2016 — ALMA resolved fit, inner edge ~6 AU |
| `disk_outer_radius_au` | 55 | high | Greaves 2004 (55 AU, SCUBA); MacGregor 2016 adopts it as a fixed prior upper bound — ALMA does not constrain the outer edge |
| `disk_dust_temperature_k` | 60 | high | Greaves 2004 / Lawler 2014 (~60–80 K); MacGregor 2016 assumes a T proportional to r^-0.5 profile and fits no dust temperature |
| `disk_tint_rgb_hex` | `#ffe2bb` (warm; vivid `#ffbc00`) | low | No measured optical color (thermal/mm only). Mie reflectance synthesis: amorphous silicate + organics (Lawler 2014; a_min ~0.31 µm), the silicate+organic optical constants mixed with Maxwell-Garnett effective-medium theory — organics absorb blue → distinctly warm reflectance (B/I 0.39, the warmest belt); renderer applies the G8.5 V light. Vivid pack: `#ffbc00` (amber) |
| `disk_opacity` | 0.15 | low | Tie-break: physical optical depth is ~10⁻³ from MacGregor 2016 dust mass + ring geometry, but cfg uses 0.15 for in-game visibility against deep-space background; documented as a render-visibility tradeoff |
| `disk_morphology` | "broad single ring, metal-poor analog of Kuiper Belt" | high | MacGregor 2016 §3 — single broad ring explicitly favored over multi-belt; no resolved inner gap |
| `disk_resolved_imaging` | true | high | MacGregor 2016 — ALMA Band 6 resolved |
| `disk_imaging_observatory` | ALMA | high | MacGregor 2016 |
| `disk_mass_mearth` | 1.2 | medium | Greaves 2004 (1.2 M⊕); MacGregor 2016 measures a belt flux density of 1.0 mJy, not a dust mass |
| `disk_planetesimal_belt_inferred` | true | high | MacGregor 2016 §5 — collisional cascade requires a parent planetesimal body belt to replenish the dust |

## Surface synthesis

τ Ceti's photosphere is a colder, older, and substantially more
iron-poor cousin of the Sun. The effective temperature of 5370 K
(Korolik 2023 interferometric) sits ~400 K below Sol's 5772 K;
combined with R = 0.793 R☉, the measured bolometric luminosity is
0.488 L☉ (Teixeira 2009, M_V + bolometric correction; consistent
with R and Teff via Stefan–Boltzmann), a little under half the solar
reference. The G8.5 V classification (Gray et al. 2006) places
τ Ceti at the cool faint end of the solar analog band, comparable
in temperature to ε Eridani's K2V but with the lower-gravity
envelope of a true G dwarf rather than a young K star.

The metallicity [Fe/H] = −0.52 (Santos 2013, the Phase 2 recommended
value) is the headline distinguishing feature. At roughly three times
less iron than the Sun, line blanketing in the blue continuum is
correspondingly weaker, and the integrated visible SED is marginally
bluer than a solar-metallicity G8.5 V would be at the same Teff — the
difference is small (~10–20 K equivalent blue-shift) but enough to push
the cfg surface tint away from the warm-cream of α Cen A's +0.24 dex
metallicity toward a cleaner pale-yellow. Bruntt 2010's [Fe/H] = −0.18
is a known α-enhanced outlier and is rejected; the Santos 2013
SWEET-Cat value anchors the DB.

Granulation is not directly imaged but is predicted to be Sun-like
in pattern and somewhat slower in timescale because of the lower
photospheric temperature (acoustic cut-off scales as √g/√T_eff,
giving τ Ceti's p-mode oscillations a slightly longer characteristic
period than the Sun's 5-minute oscillation). Teixeira 2009 detected
the p-mode spectrum with HARPS, finding Δν = 169.0 ± 0.5 μHz and
ν_max ≈ 4490 μHz, consistent with the asteroseismic radius and mass
adopted above. Limb darkening IS now constrained: Korolik 2023 fit an
H-band linear limb-darkening coefficient α ≈ 0.14 ± 0.03 directly from
the CHARA/MIRC-X visibilities, which the cfg adopts.

Sunspot coverage is essentially undetectable at the photometric
precision of long-term ground-based monitoring. With log R'HK =
−4.977 (Gomes da Silva 2021), τ Ceti is fractionally less active than
α Cen A and well below the modern Sun. It is NOT, however, a flat
standard: Gomes da Silva 2021 explicitly find a ~11 yr cyclic
variability superimposed on a long-term declining activity trend, and
caution against using τ Ceti as a constant-activity reference —
consistent with a quiet-but-cycling regime for an old, slowly
rotating, low-metallicity G dwarf.

## Atmosphere synthesis

The chromosphere–transition-region–corona structure of τ Ceti is
the canonical quiet G-dwarf reference. Gomes da Silva 2021's
log R'HK = −4.977 places the chromospheric Ca II H&K emission near
the basal flux floor — close to the minimum expected from acoustic
heating — but with a real ~11 yr magnetic-cycle modulation and a
long-term declining trend (Gomes da Silva 2021), so it is low-amplitude
rather than truly flat. Hα is in absorption with only weak variability.

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

τ Ceti has NO directly measured photometric rotation period — it is
nearly pole-on (inclination i = 7 ± 7°, v sin i ~0.1 km/s, Korolik
2023), so rotational modulation is not observable and periodogram
peaks have false-alarm probabilities near unity. The cfg therefore
carries the Korolik 2023 gyrochronological estimate of 46 ± 4 days
(method recorded as unverified), against the older Baliunas 1996
Ca II H&K value of ~34 d — a documented divergence (see Canonical
alternatives). Both are slow, as expected for an old G dwarf.

The slow rotation is consistent with the old age. The cfg adopts the
Di Folco 2004 isochrone age of ~10 Gyr (adopted by Korolik 2023) as
the value most consistent with the very low activity and slow
rotation, against the Mamajek & Hillenbrand 2008 activity-age of
5.8 Gyr — a documented divergence within a literature range of
4.4–12.4 Gyr (Canonical alternatives). Gomes da Silva 2021's
isochrone fit of 0.028 Gyr is a metal-poor-star fit failure and is
rejected.

Asteroseismic p-mode oscillations were detected by Teixeira 2009
in 8 nights of HARPS RV monitoring: Δν = 169.0 ± 0.5 μHz, ν_max ≈
4490 μHz. The acoustic timescale 2π/Δν ≈ 1.6 h is shorter than the
solar 5-minute oscillation when scaled correctly by the smaller
radius and higher mean sound speed; this constrains the mass to
0.783 ± 0.012 M☉ and the radius to 0.793 ± 0.004 R☉ with
percent-level precision, the values adopted in the Decisions table.

Differential rotation is not resolved. The rotation axis is nearly
pole-on (i = 7 ± 7°, Korolik 2023), which NearStars reflects in the
rendered spin geometry; note this stellar spin axis is misaligned
with the debris-disk axis (i_disk ~35°, Lawler 2014), a misalignment
Korolik 2023 explicitly flags.

## Canonical alternatives

**Age — isochrone vs activity.** The cfg adopts the Di Folco 2004
isochrone age ~10 Gyr (adopted by Korolik 2023), the value most
consistent with τ Ceti's very low activity and slow rotation. The
documented alternative is the Mamajek & Hillenbrand 2008 activity-age
of 5.8 Gyr; the full literature spread is 4.4–12.4 Gyr (Korolik 2023).
The Gomes da Silva 2021 isochrone fit (0.028 Gyr) is a metal-poor-star
fit failure and is rejected. All credible methods agree τ Ceti is old;
the divergence is whether it is ~6 or ~10 Gyr.

**Rotation — gyrochronology vs Ca II HK.** τ Ceti has NO direct
photometric rotation period (it is pole-on, v sin i ~0.1 km/s). The cfg
carries the Korolik 2023 gyrochronological 46 ± 4 d (recorded
method=unverified, and tied to the ~10 Gyr age); the documented
alternative is the older Baliunas 1996 Ca II H&K ~34 d. Boro Saikia
2018 ZDI independently prefers ~46 d, supporting the cfg choice. The
two are coupled to the age divergence above.

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

Sunspots and faculae are rendered only as a very low-amplitude
feature — τ Ceti is quiet, but NOT flat: the chromospheric output is
encoded with a shallow ~11 yr cycle plus a slow long-term decline
(Gomes da Silva 2021), much milder than α Cen A's 19-year Sun-like
cycle. X-ray output stays near zero (below the historical EXOSAT
limit; no Phase 2 X-ray measurement).

The defining visual element of the system is the cold debris
disk. ALMA Band 6 imaging (MacGregor 2016) resolves a single broad
ring extending from ~6 AU (inner edge) to ~55 AU (outer edge),
with a peak surface density around 30 AU and a total dust mass of
roughly 1.2 M⊕ — about 10–20× the dust inventory of our own
Kuiper Belt. NearStars renders this as a faint, broad, dimly
warm annulus around τ Ceti, encoded with the reflectance hex `#ffe2bb`
(vivid pack `#ffc100` amber — its silicate+organic grains are the
warmest-reflectance belt in the catalog, B/I 0.40) and
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
  (`2016ApJ...828..113M`, [arXiv:1607.06900](https://arxiv.org/abs/1607.06900)). ALMA Band 6 resolved
  imaging of τ Ceti's disk; single broad ring 6–55 AU; dust mass
  ~1.2 M⊕; collisional cascade requires a parent planetesimal
  body belt. Anchors all `disk_*` Decisions rows.
- **Korolik M. et al. 2023** — *Refining the Stellar Parameters of
  τ Ceti: a Pole-on Solar Analog*, AJ 166, 123 (`2023AJ....166..123K`,
  [arXiv:2307.10394](https://arxiv.org/abs/2307.10394)). CHARA/MIRC-X interferometry: θ_LD 2.019 ± 0.012
  mas → R 0.793 ± 0.004 R☉; interferometric Teff 5370 ± 20 K (with
  Boyajian 2013 F_bol); H-band limb-darkening α ≈ 0.14; nearly pole-on
  (i = 7 ± 7°); gyrochronological P_rot 46 ± 4 d; adopts the Di Folco
  2004 ~10 Gyr age. Phase 2 anchor for radius/Teff/limb-darkening/spin/
  rotation.
- **Teixeira T. C. et al. 2009** — *Solar-like oscillations in τ Ceti*,
  A&A 494, 237 (`2009A&A...494..237T`, [arXiv:0811.3989](https://arxiv.org/abs/0811.3989)). HARPS p-mode
  detection; asteroseismic mass 0.783 ± 0.012 M☉ and luminosity
  0.488 ± 0.010 L☉ (M_V + bolometric correction). Phase 2 recommended
  mass + luminosity.
- **Santos N. C. et al. 2013** — *SWEET-Cat: A catalogue of parameters
  for stars with exoplanets*, A&A 556, A150 (`2013A&A...556A.150S`,
  [arXiv:1307.0354](https://arxiv.org/abs/1307.0354)). Spectroscopic [Fe/H] = −0.52 ± 0.01. Phase 2
  recommended metallicity (very iron-poor).
- **Gomes da Silva J. et al. 2021** — *Stellar chromospheric activity
  of the AMBRE-HARPS sample*, A&A 646, A77 (`2021A&A...646A..77G`,
  [arXiv:2012.10199](https://arxiv.org/abs/2012.10199)). log R'HK = −4.977; a ~11 yr cyclic variability
  with a long-term declining trend (NOT a flat activity standard).
  Phase 2 recommended activity.
- **Di Folco E. et al. 2004** — *VLTI near-IR interferometric radii of
  nearby stars*, A&A 426, 601 (`2004A&A...426..601D`). Isochrone age
  ~10 Gyr for τ Ceti, adopted by Korolik 2023; Phase 2 recommended age
  (see Canonical alternatives).
- **Feng F. et al. 2017** — *Color difference makes a difference:
  four planet candidates around τ Ceti*, AJ 154, 135
  (`2017AJ....154..135F`, [arXiv:1708.02051](https://arxiv.org/abs/1708.02051)). Four-planet RV
  discovery (e, f, g, h). The DB Phase 2 stores planets f, g, h
  but omits e (see Open items). (Mass now anchored on Teixeira 2009,
  not Feng's M–K relation.)
- **Mamajek E. E. & Hillenbrand L. A. 2008** — *Improved age
  estimation for solar-type dwarfs using activity-rotation
  diagnostics*, ApJ 687, 1264 (`2008ApJ...687.1264M`,
  [arXiv:0807.1686](https://arxiv.org/abs/0807.1686)). Activity-age 5.8 Gyr — the documented-divergence
  alternative to the Di Folco 2004 isochrone age (Canonical alternatives).
- **Pavlenko Y. V. et al. 2012** — *Spectral analysis of τ Ceti*,
  MNRAS 422, 542 (`2012MNRAS.422..542P`, [arXiv:1112.1709](https://arxiv.org/abs/1112.1709)). Earlier
  differential analysis ([Fe/H] −0.55, Teff 5344, log R'HK −4.95, age
  7 Gyr) — SUPERSEDED across the board by the Phase 2 layer above; not
  in the Phase 2 bib.
- **Baliunas S. L. et al. 1996** — *Chromospheric variations in
  main-sequence stars II*, ApJ 438, 269 (`1995ApJ...438..269B`).
  Mt Wilson Ca II H&K survey; τ Ceti ~34 d (the documented-divergence
  alternative to the Korolik 2023 gyrochronological 46 d).

### Read (context / methodology, not directly decision-driving)

- **Di Folco E. et al. 2007** — *VLTI/VINCI interferometric
  diameters of nearby exoplanet host stars*, A&A 475, 243
  (`2007A&A...475..243D`, [arXiv:0710.1731](https://arxiv.org/abs/0710.1731)). VINCI K-band angular
  diameter; the earlier interferometric radius, consistent with and
  superseded by Korolik 2023 CHARA/MIRC-X.
- **Schmitt J. H. M. M. et al. 1985** — *EXOSAT observations of
  nearby stars: τ Ceti upper limit*. log L_X ≤ 26.5 non-detection;
  historical X-ray context only — NOT in the Phase 2 layer, no cfg row.
- **Judge P. G. et al. 2004** — *FUV spectroscopy of τ Ceti from
  FUSE: chromospheric basal flux*, ApJ 613, 1306. Quiescent
  chromosphere reference; basal flux floor.
- **Gray R. O. et al. 2006** — *Contributions to the Nearby Stars
  (NStars) Project: spectroscopy of stars within 40 pc — south*
  (`2006AJ....132..161G`). G8.5 V spectral classification.
- **Boro Saikia S. et al. 2018** — *Solar-type magnetic activity
  on τ Ceti from ZDI*, A&A 620, L11. Zeeman-Doppler-imaging prefers
  a 46 d rotation — consistent with the Korolik 2023 gyrochronological
  46 ± 4 d now carried by the cfg.

### Read (instrument / non-cfg-decisive)

- **Lawler S. M. et al. 2014** — *Debris disks of τ Ceti and
  ε Eridani: SED modeling* ([arXiv:1409.0023](https://arxiv.org/abs/1409.0023)). SED-fit dust
  temperature and inferred grain size; superseded by MacGregor
  2016 resolved imaging.

### Not read — no arXiv preprint or low-priority (~40 papers)

SETI / laser-emission searches (Tarter 1981 Project Ozma followup,
Tellis 2017, Margot 2018), conference abstracts (EPSC/AGU/DPS), and
astrobiological habitability speculation papers contribute no
cfg-decisive content for the host star. The full filtered bib is
preserved in `docs/phase3/_bib/tau-cet.yaml` with `status: skipped`
annotations.

## Stellar wind / astrosphere

τ Cet has a weak wind (Ṁ ≤ 0.1 Ṁ⊙, Wood 2021) and sees a moderate ~50 km/s ISM
inflow, giving a small astrosphere standing off at **≲19 AU**. It is among the
most magnetically quiet Sun-like stars known — **definitively flat, with no
activity cycle** over ~50 yr of monitoring (Baum 2022). The result is a steady
(uncycled) particle environment somewhat below solar.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `solar_cycle_yr` | none (flat) | high | Baum 2022 — no cycle over ~50 yr; steady, uncycled wind |
| `stellar_wind_mass_loss_solar` | ≤ 0.1 (upper limit) | medium | Wood 2021 astrospheric Lyα |
| `local_ism_inflow_speed_kms` | ~50 | medium | 6D astrometry vs LIC |
| `astrosphere_standoff_au` | ≲ 19 (upper bound) | medium | 120·√(Ṁ_rel)·(V_⊙/V_ISM) from the Ṁ upper limit + V_ISM. Assumes a Sun-like wind speed (V_⊙ ≈ 400 km/s, fixed-velocity assumption of Wood et al. 2002/2005); only Ṁ and V_ISM vary per star |
| `stellar_radiation_surface_relative_sun` | ~0.6 | medium | measured: log L_X 26.69 (S&L 2004 NEXXUS) vs solar cycle-mean 26.9; flat star, no cycle modulation |
| `astrosphere_apex_ra_deg` / `_dec_deg` | ~282 / +8 | low | 6D astrometry vs LIC; **plugin-only** |

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
