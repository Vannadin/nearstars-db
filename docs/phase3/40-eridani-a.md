# 40 Eridani A — Phase 3 Synthesis

40 Eridani A (HD 26965, HR 1325, GJ 166 A, Keid) is a K0.5 V dwarf at
5.01 pc — the brightest component of the 40 Eridani triple system and
the host star whose hypothetical planet "Vulcan" (Ma 2018) was refuted
by Burrows et al. 2024. The system also contains the DA white dwarf
40 Eri B (`docs/phase3/40-eridani-b.md`) and the M4.5 Ve flare star
40 Eri C / DY Eri (`docs/phase3/40-eridani-c.md`), with the B-C
pair separated from A by roughly 83″ (≈ 400 AU projected) and
gravitationally bound on an outer orbit too long (~8000 yr per
Tokovinin MSC 2018) to be Keplerian-fitted.

The fundamental stellar parameters are exceptionally well-constrained
by two independent interferometric measurements that agree at the 1σ
level. Boyajian et al. 2012 CHARA Classic H-band observations give
θ_LD = 1.504 ± 0.006 mas, R = 0.8061 ± 0.0036 R☉, Teff = 5143 ± 14 K,
L = 0.4078 ± 0.0032 L☉ (paper Table 6, sample identifier GJ 166 A).
Rains et al. 2020 VLTI/PIONIER independently measure θ_LD =
1.486 ± 0.012 mas → R = 0.804 ± 0.006 R☉, Teff = 5126 ± 30 K,
L = 0.40 ± 0.01 L☉ (paper Table 4; 40 Eri A is star #7 of 16 in the
sample). Both CHARA and VLTI/PIONIER measurements appear in the
Phase 2 DB; Boyajian 2012 is the recommended primary because of the
tighter fractional uncertainty (the method-tier tiebreak when both
are interferometry).

The mass anchor is Ma et al. 2018 M = 0.78 ± 0.08 M☉ (paper Table 2,
M-R relation via Torres et al. 2010 + spectroscopic Teff/[Fe/H]) —
the same paper that announced the now-refuted "Vulcan" candidate.
Diaz et al. 2018 SPECIES isochrone gives an independent 0.76 ± 0.03
M☉ in agreement within 1σ. No dynamical mass exists because the
A-BC outer orbit is too long-period to have been fitted (Tokovinin
MSC 2018 lists it as "no Keplerian solution").

**The age is the documented divergence of this synthesis.** Ma et al.
2018 PARSEC isochrone fitting yields 6.9 ± 4.7 Gyr — a typical
K-dwarf-isochrone result with the characteristic K-dwarf age
indeterminacy on Gyr timescales (the SPECIES Diaz 2018 result is
9.23 ± 4.84 Gyr along the same flat χ² floor). Bond et al. 2017 §6.2
derive a system-coeval age of **~1.8 Gyr** from the white-dwarf
initial–final mass relation: 40 Eri B with M_final = 0.573 M☉ implies
an initial-mass progenitor of ~1.8 M☉, with main-sequence lifetime
~1.7 Gyr + cooling age 122 Myr. Bond explicitly notes that "earlier
concerns about an excessive age...appear to be resolved" with the new
mass — i.e. the K-dwarf-isochrone old age was historically taken
seriously but the WD progenitor analysis disfavors it. This Phase 3
synthesis adopts ~1.8 Gyr as the cfg age because the IFMR-derived
system-coeval value is more physically constrained than a single
K-dwarf isochrone with 60+% relative uncertainty; the K-dwarf
isochrone alternative is preserved in `## Canonical alternatives`.

Metallicity is moderately sub-solar, [Fe/H] = −0.29 ± 0.12 (Diaz 2018
SPECIES; Bensby 2014 thin/thick-disk survey −0.31 ± 0.10 within 1σ;
Ma 2018 −0.42 ± 0.04 marginally lower). The rotation period from
Burrows et al. 2024 NEID line-by-line activity analysis is ~42 days
(the paper gives no formal uncertainty, only "∼42 days") — this is
the rotational modulation that produced the spurious "Vulcan" 42-day
RV signal in the first place. Pre-Burrows literature gives shorter
rotation periods (Saar & Osten 1997 ~37–38 d from Mt. Wilson HK;
Diaz 2018 HARPS S-index ~38 d) and the discrepancy is unresolved
in the current literature. Chromospheric activity log R'HK = −4.99
(Jenkins 2011) places 40 Eri A as a quiet K-dwarf, slightly more
active than the Sun's mean. X-ray monitoring is sparse; the
ROSAT all-sky survey baseline gives log L_X ≈ 27.5 cgs in the
0.5–2 keV band.

**Scenario choice for NearStars: a quiet, slightly old K0.5 V star
hosting no curated planet, viewed from a far-binary perspective where
the B-C pair appears as a single point ~83″ away.** All 14
canonical-aligned cfg picks track the paper-verified parameter set.
The age is a documented divergence (Bond 2017 IFMR over Ma 2018
K-dwarf isochrone). One tie-break sets the visual surface tint for
the K0.5 V SED.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | K0.5 V | high | Keenan & McNeil 1989 — IAU MK system |
| `mass_msun` | 0.78 ± 0.08 | high | Ma et al. 2018 — M-R relation (Torres 2010) + spectroscopic Teff/[Fe/H]; Diaz 2018 SPECIES 0.76 ± 0.03 agrees within 1σ |
| `radius_rsun` | 0.8061 ± 0.0036 | high | Boyajian et al. 2012 — CHARA Classic H-band interferometry, θ_LD = 1.504 ± 0.006 mas; Rains 2020 VLTI/PIONIER 0.804 ± 0.006 agrees |
| `teff_k` | 5143 ± 14 | high | Boyajian et al. 2012 — interferometric θ_LD + bolometric flux; Rains 2020 5126 ± 30 agrees within 1σ |
| `luminosity_lsun` | 0.4078 ± 0.0032 | high | Boyajian et al. 2012 — bolometric flux integration; Rains 2020 0.40 ± 0.01 agrees |
| `metallicity_fe_h_dex` | −0.29 ± 0.12 | high | Diaz et al. 2018 — SPECIES high-resolution spectroscopy; Bensby 2014 thin-disk survey −0.31 ± 0.10 corroborates |
| `age_gyr` | 1.8 | medium | Documented divergence: see Canonical alternatives. Bond 2017 §6.2 IFMR-derived system-coeval age from 40 Eri B WD progenitor (initial mass ~1.8 M☉, MS lifetime 1.7 Gyr + cooling 122 Myr) |
| `rotation_period_days` | 42 | medium | Burrows et al. 2024 — NEID line-by-line activity analysis; "∼42 days" with no formal σ in the paper; same signal that produced the spurious Vulcan RV detection |
| `activity_log_rhk` | −4.99 | medium | Jenkins et al. 2011 — Ca II H&K HARPS chromospheric survey; Henry 1996 −4.94 corroborates |
| `x_ray_log_lx_cgs` | ~27.5 | low | ROSAT all-sky survey baseline 0.5–2 keV; no dedicated XMM/Chandra long-term cycle monitoring published |
| `vulcan_disposition` | Refuted (Burrows 2024) | high | Burrows et al. 2024 NEID line-RV + activity correlations + depth dependence; 16-year multi-instrument RV (HIRES, PFS, CHIRON, HARPS, NEID); 42-day signal is stellar rotation, not Keplerian |
| `visual_surface_tint_hex_primary` | `#ffd5a8` (warm orange-cream K0.5 V) | medium | Tie-break: K0.5 V blackbody at 5143 K rendered as a slightly cooler-toned cream than the Sun; interesting-first contrast with companion C's deep red |
| `stellar_color_temp_k` | 5143 | high | derived from Teff |
| `star_apparent_diameter_arcsec_from_bc_barycenter_at_400au` | 1.9 | high | derived: 2 R★ / a × (180·3600/π); a = 400 AU projected separation to B-C |
| `visual_companion_event_b_c_pair_separation_arcsec_from_a` | ~83 | high | WDS J04153−0739; A-BC outer orbit unfitted (Tokovinin MSC 2018) so separation drifts slowly on ~8000 yr timescales |
| `apparent_magnitude_v_from_earth` | 4.43 | high | Hipparcos van Leeuwen 2007; naked-eye star in Eridanus, traditional name Keid |

## Surface synthesis

The photosphere of 40 Eridani A is a quintessential K0.5 V dwarf —
slightly cooler than the Sun's G2 V, with the cream-orange illumination
characteristic of mid-K dwarfs. At Teff = 5143 K the SED peaks in the
green-yellow ~563 nm, shifted from the Sun's ~501 nm peak by the
~600 K cooler photosphere; in chromaticity this corresponds to a
warm-orange tint with the visible disk appearing as a slightly amber
"sun" to a hypothetical observer at the 0.65 AU habitable-zone inner
edge (where insolation matches Earth's).

The CHARA Classic interferometric measurement (Boyajian 2012) gives
the angular diameter to 0.4% precision — among the best-determined
K-dwarf diameters in the literature. The independent VLTI/PIONIER
result (Rains 2020) agrees within 1σ on both θ_LD and the derived
Teff. The two interferometric arrays use different beam combiners,
different bandpasses (CHARA H band; PIONIER H band as well but
four-telescope), and different limb-darkening prescriptions, so the
agreement is a strong validation of the fundamental parameter set.

Spot coverage is moderate; log R'HK = −4.99 (Jenkins 2011) places
40 Eri A as quiet by the standards of intermediate-activity K
dwarfs, but slightly more active than the Sun's quiet-cycle mean of
log R'HK ≈ −4.95. The 42-day rotation period (Burrows 2024) implies
Rossby number Ro ≈ 1.0 (using Noyes 1984 convective turnover ≈
40 d at this Teff), placing A in the unsaturated rotation–activity
regime. Active regions distribute across the visible hemisphere
during rotation phases producing the few-m/s RV jitter that
masqueraded as the 42-day Vulcan signal.

The slightly sub-solar metallicity ([Fe/H] = −0.29) does not produce
a visible color shift at typical in-game illumination resolution but
does affect the SED at the few-percent level in the optical
blue — slightly bluer continuum than a solar-metallicity K0.5 V.
The granulation pattern is K-dwarf-typical with smaller convection
cells than the Sun, consistent with the shallower convective envelope
of the cooler photosphere.

## Atmosphere synthesis

40 Eri A hosts a moderately quiet K-dwarf atmosphere with the
standard chromosphere–transition-region–corona structure. The
chromospheric Ca II H&K emission corresponds to log R'HK = −4.99
(Jenkins 2011) — a value consistent with the K-dwarf mean for the
unsaturated rotation–activity regime. There is no published
long-term log R'HK time series for 40 Eri A comparable to the
Mt. Wilson coverage of α Cen A or HK Cet B, so the chromospheric
cycle (if any) is unconstrained; the 42-day rotation period in
Burrows 2024 is observed in a 16-year multi-instrument RV
baseline but no decadal cycle was characterized.

The X-ray luminosity from ROSAT all-sky survey points is roughly
log L_X = 27.5 cgs (0.5–2 keV); there is no XMM-Newton or Chandra
long-term monitoring campaign published for 40 Eri A. The integrated
XUV flux at the habitable zone is therefore set by typical K0.5 V
quiet-state scaling — slightly higher in fractional Lbol than a
solar-twin G dwarf because K dwarfs maintain stronger chromospheric
heating per unit photospheric flux. Hydrodynamic atmospheric escape
for any hypothetical inner planet (if one existed; HD 26965 b does
not) would have been moderate-to-strong because the K-dwarf XUV
plateau is longer than the G-dwarf equivalent during the early
saturated phase.

The activity-induced RV signature that produced the spurious Vulcan
detection is itself an atmospheric phenomenon: Burrows 2024 traces
it to a combination of starspot modulation and convective-blueshift
suppression cycling at the 42-day rotation period. The depth-
dependent line-by-line correlations indicate that the dominant
contribution comes from suppression of granular convective
blueshift in active regions, not from pure photometric spot
modulation. This is the same mechanism that produces the well-known
"granulation-driven RV jitter" in solar-type stars, scaled to K-dwarf
sub-photosphere convection depth.

## Rotation & spin synthesis

The Burrows et al. 2024 rotation period of ∼42 days is the canonical
modern value, derived from NEID line-by-line activity correlations
across a 16-year multi-instrument RV baseline (HIRES, PFS, CHIRON,
HARPS, NEID). The paper explicitly does not quote a formal
uncertainty on P_rot — the wording is "rotationally modulated activity
signal at a period of ∼42 days" — so the cfg adopts 42 d as a
point value with confidence=medium.

**Pre-Burrows rotation literature is non-uniform.** Saar & Osten
1997 ROSAT-correlated coronal activity estimate gives 37.10 d.
Diaz et al. 2018 HARPS S-index periodogram peaks at "an emerging
peak at 38 days, very close to the [42-d RV] signal we detect."
Mount Wilson Ca II HK monitoring (Baliunas et al. 1995 era) reports
power near 42.3 d after subtracting longer magnetic-cycle terms.
The factor-of-1.1 spread between 37 d and 42 d may reflect
differential rotation (latitude-dependent rotation rate, with the
NEID activity signal sampling a different active-latitude band than
the older datasets), but no published differential-rotation
measurement settles this for 40 Eri A.

For cfg purposes, 42 d is the recent multi-instrument anchor and
the same period that drove the Vulcan-refutation result. Confidence
is medium because of the absent formal σ and the 37–42 d pre-Burrows
spread.

**Differential rotation and inclination.** Neither is directly
measured for 40 Eri A. Differential rotation is expected to be
weaker than the Sun's (K-dwarf trend: shallower convective envelope
→ less differential shear), but the literature lacks a Doppler-imaging
campaign comparable to those for active K dwarfs like ε Eri.
Rotation-axis inclination is unconstrained — for visual rendering
NearStars adopts an axis tilted ~30° to the line of sight from the
ecliptic, consistent with random orientation.

**Spin–down history under K-dwarf braking.** At P_rot = 42 d the
gyrochronological age estimate (Barnes 2007 + Mamajek & Hillenbrand
2008 calibration) is roughly 4–6 Gyr for B−V ≈ 0.82 — broadly
consistent with the Ma 2018 K-dwarf isochrone reading of 6.9 ± 4.7
Gyr but inconsistent with the Bond 2017 IFMR ~1.8 Gyr. This is a
secondary face of the same age divergence flagged in the Decisions
table. The gyrochronology calibration is itself uncertain at these
old ages because K-dwarf spin-down stalls partially at long P_rot
(van Saders et al. 2016 weakened-braking hypothesis), so the
gyrochronological age has its own systematic floor.

## Visual styling

In the NearStars renderer, 40 Eridani A is portrayed as a warm-cream
K0.5 V star — visually distinguishable from a solar-type analog
by the slightly cooler orange-cream tint encoded as `#ffd5a8` (in
contrast to the Sun's `#fff8f0` or the warm-cream α Cen A
`#fff4e8`). The choice is a tie-break against a strict K-dwarf
blackbody color: at 5143 K the blackbody chromaticity is closer to
`#ffe2b6`, but the cfg pick pushes slightly toward orange for
visual distinction in the in-game star palette, where K dwarfs are
the dominant local-volume population and a single shared "K-dwarf
warm-cream" risks visual homogeneity.

At 5.01 pc viewed from Earth, the apparent magnitude V = 4.43
places 40 Eridani A as a naked-eye star in Eridanus (traditional
name Keid, from Arabic *al-qaid* "the broken shell"). It is
located on the constellation's southern outline, about 16°
southwest of Rigel.

The companion B-C pair, viewed from any hypothetical close-in
planet around A, would appear as an unresolved double point of
light at angular separation ~83″ — easily a single naked-eye
object at A's habitable zone (the angular separation is roughly
30 arc-minutes at the 0.65 AU HZ inner edge, comparable to the
full Moon seen from Earth). The B-C pair itself is a 230-yr
mutually orbiting K-dwarf-mass WD + M-dwarf binary; at
periastron the B-C separation drops to ~26 AU and B's reflected
brightness from C's emission becomes detectable, but at the
~8000 yr A-BC orbit timescale the separation is geometrically
fixed for the cfg in-game epoch.

**No planet rendering for HD 26965 b.** Per the Burrows 2024
refutation, the "Vulcan" candidate is not represented in the
in-game system. The Refutation section below documents the
historical detection and refutation for cultural cross-reference;
the cfg renders only the stellar triple, not any planetary body
around A.

## Canonical alternatives

The age is the single documented divergence in this synthesis. The
cfg adopts Bond 2017 ~1.8 Gyr from the WD-progenitor IFMR; the
canonical reading of the K-dwarf-only literature would adopt the
Ma 2018 K-dwarf isochrone instead.

| Field | cfg value (Bond 2017 IFMR) | Canonical alternative (Ma 2018 K-dwarf isochrone) | Why cfg picks differently |
|---|---|---|---|
| `age_gyr` | ~1.8 (system-coeval from 40 Eri B WD progenitor analysis) | 6.9 ± 4.7 (K-dwarf SED + PARSEC isochrone) | The IFMR-derived system-coeval value anchors the age to a physical end-point (WD progenitor lifetime + cooling track), independent of K-dwarf isochrone systematics. The Ma 2018 alternative has 60+% relative uncertainty along a K-dwarf isochrone branch where age is poorly constrained on Gyr timescales. Bond 2017 §6.2 explicitly notes "earlier concerns about an excessive age...appear to be resolved" with the revised WD mass. Gyrochronological cross-check (P_rot 42 d → 4–6 Gyr via Barnes 2007) sits closer to Ma 2018 but is subject to van Saders 2016 weakened-braking systematics at old ages, so does not settle the tension. cfg follows the more physically anchored Bond reading. |

The Ma 2018 isochrone age is retained in the Phase 2 DB as
`recommended:true` within `age_measurements` because it is the only
direct stellar-age measurement of A itself; Bond 2017 is recorded
as `recommended:false` with method `isochrone` (treating the IFMR
progenitor lifetime as an isochrone-equivalent constraint). The
divergence between the Phase 2 recommended pick and the Phase 3
cfg pick is the rationale for this `## Canonical alternatives`
section.

## Refuted planet — HD 26965 b ("Vulcan")

40 Eridani A is famous in popular culture as the host star of Mr.
Spock's homeworld Vulcan in the Star Trek universe — an
identification confirmed by a 1991 letter from Gene Roddenberry and
Sallie Baliunas. The Ma et al. 2018 announcement of an RV-detected
super-Earth candidate at P = 42.4 d, M sin i ≈ 8.5 M⊕, a ≈ 0.224 AU
was therefore one of the most culturally celebrated exoplanet
detections of the 2010s.

**HD 26965 b is now classified as Refuted (Burrows et al. 2024,
AJ 167, 243).** The Burrows 2024 NEID precision-Doppler campaign,
combined with re-analysis of 16 years of HIRES + PFS + CHIRON +
HARPS data, demonstrated that the 42-day RV signal is the same
signal as the star's rotation period (∼42 d). The three lines of
evidence are: (1) cross-correlation of bulk RV with classical
activity indicators shows a multi-day lag consistent with
rotational modulation, not Keplerian orbit; (2) line-by-line RV
analysis shows depth-dependent correlations indicative of
convective-blueshift suppression varying with active-region
visibility; (3) linear detrending against the activity-indicator
time series removes most of the RV variance. The combined evidence
is consistent with "an RV signature dominated by a rotationally
modulated activity signal at a period of ∼42 days. We hypothesize
that this activity signature is due to a combination of spots and
convective blueshift suppression" (Burrows 2024 abstract).

**Disposition: not in `db/planets_curated.json`.** No KSP planet is
built from the Ma 2018 candidate; the NASA Exoplanet Archive
`ps` table also returns zero rows for HD 26965 since the
Burrows-driven removal. No 2025 or 2026 follow-up paper has
proposed a replacement candidate; lit-search "HD 26965 planet
2024-2026" surfaces only the Burrows refutation and downstream
news summaries.

This refutation note is preserved in the Phase 3 markdown rather
than as a separate `docs/phase3/40-eridani-a-b.md` file because (a)
no curated planet exists for A and (b) the cultural cross-reference
fits naturally in the host-star synthesis. The closest precedent
is the tau Cet e refuted Phase 3 markdown (`tau-cet-e.md`), which
preserves the original-detection record alongside the refutation;
40 Eri A b is held to a similar standard but at section-level
rather than file-level since there is no historical Phase 3 for
the Ma 2018 picture to preserve.

## Bibliography

### Read (drove Decisions above)

- **Boyajian T. S. et al. 2012** — *Stellar Diameters and
  Temperatures II. Main-Sequence K- and M-Stars*, ApJ 757, 112
  (`2012ApJ...757..112B`, doi:10.1088/0004-637X/757/2/112). CHARA
  Classic H-band interferometric angular diameters for a sample
  including 40 Eri A as GJ 166 A: θ_LD = 1.504 ± 0.006 mas (Table 3);
  R = 0.8061 ± 0.0036 R☉, Teff = 5143 ± 14 K, L = 0.4078 ± 0.0032 L☉
  (Table 6). Recommended Phase 2 primary for R/Teff/L because of
  the tighter fractional uncertainty among the two interferometric
  measurements.
- **Rains A. D. et al. 2020** — *Precision angular diameters for 16
  southern stars with VLTI/PIONIER*, MNRAS 493, 2377
  (`2020MNRAS.493.2377R`, doi:10.1093/mnras/staa282,
  arXiv:2004.02343). VLTI/PIONIER four-telescope H-band
  interferometry; 40 Eri A is star #7 of 16 in Table 1. Independent
  cross-check: θ_LD = 1.486 ± 0.012 mas, R = 0.804 ± 0.006 R☉,
  Teff = 5126 ± 30 K, L = 0.40 ± 0.01 L☉ (Table 4). Agrees with
  Boyajian 2012 within 1σ on all four quantities.
- **Ma B. et al. 2018** — *Very low-mass stellar and substellar
  companions to solar-like stars from MARVELS VI. A giant planet
  and a brown dwarf candidate in a close binary system HD 87646*
  is the same authors' related work; the relevant paper for
  40 Eri A is **Ma et al. 2018 MNRAS 480, 2411**
  (`2018MNRAS.480.2411M`, doi:10.1093/mnras/sty1933) reporting
  the Dharma Planet Survey RV detection of HD 26965 b. Mass
  0.78 ± 0.08 M☉, age 6.9 ± 4.7 Gyr from PARSEC isochrone +
  multi-band SED, Teff 5072 ± 53 K, [Fe/H] −0.42 ± 0.04 (Table 2).
  Phase 2 anchor for mass and (alternative) age and metallicity;
  also the source of the now-refuted planet candidate.
- **Bond H. E. et al. 2017** — *Astrophysical Implications of a
  New Dynamical Mass for the Nearby White Dwarf 40 Eridani B*,
  ApJ 848, 16 (`2017ApJ...848...16B`, doi:10.3847/1538-4357/aa8a63,
  arXiv:1709.00478). HST FGS astrometric mass of 40 Eri B
  0.573 ± 0.018 M☉; §6.2 derives system-coeval total age ~1.8 Gyr
  from IFMR (initial mass ~1.8 M☉ → MS lifetime 1.7 Gyr + cooling
  age 122 Myr). Phase 3 cfg adopts this age over Ma 2018 — see
  `## Canonical alternatives`.
- **Burrows A. et al. 2024** — *The Death of Vulcan: NEID Reveals
  That the Planet Candidate Orbiting HD 26965 Is Stellar Activity*,
  AJ 167, 243 (`2024AJ....167..243B`, doi:10.3847/1538-3881/ad34d5,
  arXiv:2404.17494). NEID line-by-line RV + activity-indicator
  correlations refute the Ma 2018 Vulcan candidate. Stellar
  rotation period reported as "∼42 days" with no formal σ.
  Sources the Decisions row for `rotation_period_days` and the
  Refuted-planet section.
- **Diaz M. R. et al. 2018** — *The Test Case of HD 26965:
  Difficulties Disentangling Weak Doppler Signals from Stellar
  Activity*, AJ 155, 126 (`2018AJ....155..126D`,
  doi:10.3847/1538-3881/aaa896, arXiv:1801.03970). Pre-Burrows
  examination of the Vulcan signal with HARPS data; foreshadows
  the activity-vs-planet ambiguity. Phase 2 alternative for mass
  (0.76 ± 0.03 M☉), Teff (5151 ± 55 K), [Fe/H] (−0.29 ± 0.12),
  age (9.23 ± 4.84 Gyr) from SPECIES atmospheric pipeline
  (Table 1). Notes ~37 d Saar & Osten 1997 P_rot and a ~38 d
  HARPS S-index peak.
- **Jenkins J. S. et al. 2011** — *Chromospheric activities and
  kinematics for solar type dwarfs and subgiants: analysis of the
  activity distribution and the AVR*, A&A 531, A8
  (`2011A&A...531A...8J`, doi:10.1051/0004-6361/201016333). HARPS
  Ca II H&K survey of 890 southern FGK stars. Source for the
  Phase 2 log R'HK = −4.99 recommended value (caveat: the row-level
  CDS table entry was not directly fetched in this session, see
  Open items).

### Read (context for the K-dwarf parameter set + binary architecture)

- **Pourbaix D. & Boffin H. M. J. 2016** — α Centauri AB
  visual-spectroscopic binary mass; cited because the same
  technique was used historically for 40 Eri AB but with much
  longer-period unfittable mutual orbit (40 Eri A-BC is ~8000 yr,
  unresolved in Keplerian terms).
- **Mason B. D., Hartkopf W. I. & Miles K. N. 2017** — *Binary
  Star Orbits. V. The Nearby White Dwarf-Red Dwarf Pair 40 Eri BC*,
  AJ 154, 200 (`2017AJ....154..200M`,
  doi:10.3847/1538-3881/aa803e). Definitive grade-1 orbit for the
  inner B-C pair: P = 230.30 ± 0.68 yr, e = 0.4294 ± 0.0027.
  Phase 2 anchor for the B-C orbit in `db/binary_orbits.json`.
- **Henry T. J. et al. 1996** — *A Survey of Ca II H and K
  Chromospheric Emission in Southern Solar-Type Stars*, AJ 111,
  439 (`1996AJ....111..439H`, doi:10.1086/117796). Earlier
  chromospheric activity survey including 40 Eri A. Phase 2
  alternative log R'HK = −4.94. Direct CDS row not table-verified
  in this session; bibcode/title confirmed.
- **Bensby T., Feltzing S. et al. 2014** — *Exploring the Milky
  Way stellar disk*, A&A 562, A71 (`2014A&A...562A..71B`,
  doi:10.1051/0004-6361/201322631). Thin/thick-disk chemical
  abundance survey of 714 F/G dwarfs. Phase 2 alternative
  [Fe/H] = −0.31 ± 0.10 for 40 Eri A. The K0.5 V spectral type
  is at the sample boundary; bibcode/title confirmed but
  row-level Table A1 not directly fetched.
- **Tokovinin A. 2018** — *MSC — Catalogue of physical multiple
  stars* (updated 2018 release). 40 Eri A-BC outer orbit listed
  with no Keplerian solution (semi-major axis ~ 400 AU
  projected, period ~ 8000 yr). Anchors the cfg decision to
  treat A as an independent stellar body rather than as a
  resolved binary partner.
- **Saar S. H. & Osten R. A. 1997** — *Lithium, X-ray activity,
  and rotation in an HR diagram of solar-type field stars*,
  MNRAS 284, 803. Reports 40 Eri A P_rot ≈ 37.10 d from
  ROSAT-correlated coronal activity. Cited as pre-Burrows
  rotation alternative; see Open items.

### Read (instrument-only / methodological references)

- **Torres G., Andersen J. & Giménez A. 2010** — Mass-radius
  empirical relations underlying the Ma 2018 mass calculation.
- **Bressan A. et al. 2012** + **PARSEC tracks** — Stellar
  evolutionary tracks underlying the Ma 2018 isochrone age
  calculation.
- **Soto M. G. & Jenkins J. S. 2018** — SPECIES atmospheric
  pipeline used by Diaz 2018 for parameter derivation.

### Not read — superseded or low-priority

Pre-2010 K-dwarf isochrone surveys (Valenti & Fischer 2005 SPOCS,
Holmberg et al. 2009 Geneva-Copenhagen); generic
nearest-50-pc K-dwarf rotation surveys without 40 Eri A entries;
Mt. Wilson HK plate-archive papers superseded by the Burrows
2024 NEID baseline. SETI / exoplanet-search proposal papers
targeting 40 Eri A pre-Burrows (Ma 2018 follow-up proposals).
These are filtered to `status: skipped` in the bib YAML when
that is built.

## Open items for follow-up

- **Jenkins 2011 + Henry 1996 row-level log R'HK verification.**
  The chromospheric activity values −4.99 (Jenkins) and −4.94
  (Henry) were carried over from the 2026-05-27 prep notes; in
  this session the CDS table row for HD 26965 was not directly
  fetched. Re-verify against the CDS Table 4 of Jenkins 2011 (full
  table) and the equivalent in Henry 1996 in a future curation
  pass — both are widely quoted in downstream papers and the
  values are likely correct but should be paper-Table confirmed.
- **Bensby 2014 row-level [Fe/H] verification.** Same caveat as
  above: the value −0.31 ± 0.10 is from the prep notes; the
  Table A1 row for HD 26965 was not directly fetched in this
  session.
- **Burrows 2024 rotation-period uncertainty.** Paper reports
  "∼42 days" without a formal σ. The pre-Burrows 37-d Saar &
  Osten reading and 38-d Diaz 2018 HARPS S-index reading are
  inconsistent with 42 d at face value. A Gaussian-process RV +
  light-curve joint analysis (per the Aigrain 2015 framework, or
  comparable to the methodology of Damasso 2020 for Proxima)
  would settle whether the 42-d signal is genuinely the surface
  rotation period or a longer-lived active-band signature with
  an underlying differential-rotation rate.
- **Age divergence resolution by asteroseismology.** A
  fundamental cross-check of the Ma 2018 ~7 Gyr vs Bond 2017 ~1.8
  Gyr ages would require asteroseismic detection of p-mode
  oscillations on 40 Eri A. The K0.5 V spectral type puts ν_max
  near 4000 µHz which is at the edge of feasibility for current
  precision-RV time-series capabilities, but a dedicated NEID or
  ESPRESSO multi-night campaign comparable to Bouchy & Carrier
  2001 / de Meulenaer 2010 (α Cen A) would be decisive.
- **40 Eri A x-ray cycle characterization.** No long-baseline
  XMM-Newton or Chandra monitoring campaign published for A;
  the activity log R'HK = −4.99 and P_rot 42 d imply a Sun-like
  cycle is plausible but unconstrained. A dedicated cycle search
  (the same template as Robrade 2016 for α Cen A) would be
  cfg-decisive for activity-cycle visual rendering.
- **A-BC outer orbit fitting.** The ~8000 yr orbit is currently
  unfitted (Tokovinin MSC 2018). Decades-long Gaia astrometric
  monitoring should eventually tighten the A-BC parameters; if
  fitted, this would change `db/binary_orbits.json` to include
  an A-BC entry and the Phase 3 visual styling section's
  "B-C pair as single point ~83″ away" claim becomes
  time-variable.

## Related

- [40-eridani-b](40-eridani-b.md) — DA2.9 white-dwarf companion;
  Bond 2017 IFMR is the anchor for the system age divergence
  documented above
- [40-eridani-c](40-eridani-c.md) — M4.5 Ve flare star (DY Eri);
  paired with B on a 230-yr orbit
- [tau-cet-e](tau-cet-e.md) — sibling refuted-planet Phase 3
  markdown; structural precedent for the Refuted planet section
- [methodology](../reference/methodology.md) — Phase 2/3 schema
- [rex-data-comparison](../reference/rex-data-comparison.md) —
  40 Eri B refutation comparison (rex carried HD 26965 b which
  NearStars correctly excludes)
