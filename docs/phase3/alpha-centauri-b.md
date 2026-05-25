# α Centauri B — Phase 3 Synthesis

α Centauri B (HD 128621, HIP 71681, GJ 559 B) is the K1V secondary of
the nearest stellar binary. Roughly two-thirds the mass and luminosity
of its G2V companion α Cen A, B is a quiet, slightly metal-rich
K-dwarf with the longest baseline of high-precision radial-velocity
monitoring of any K star — a legacy of the planet hunt that
culminated in the retracted Dumusque 2012 claim and the subsequent
Rajpaul 2016 ruling-out.

The fundamental parameters from Pourbaix & Boffin 2016 and Kervella
2017 are exceptionally tight: M_B = 0.9373 ± 0.0028 M☉, R_B = 0.8632
± 0.0037 R☉, both shared in the same double-lined orbital and
interferometric solution as the primary. Effective temperature
5236 ± 51 K from Porto de Mello 2008 places B at the warm end of the
K1V locus; surface metallicity is +0.25 ± 0.04 (essentially identical
to A, consistent with formation from a common protostellar cloud).
System age 5.3 ± 0.3 Gyr is set by the joint asteroseismic + classical
fit of Joyce & Chaboyer 2018 — the same value as A by construction,
since both stars must satisfy their respective observational
constraints simultaneously.

α Cen B is more active than A despite being older as a fraction of
its main-sequence lifetime: log R'HK = −5.0 (Henry 1996 / DeWarf 2010)
straddles the K-dwarf quiescent–active boundary, with a 36–40 day
rotation period (DeWarf 2010) consistent with a slow but persistent
8.1-year chromospheric activity cycle. X-ray luminosity cycles with
this period (Robrade 2016), reaching log L_X ≈ 27.5 cgs at maximum.

**The planet that wasn't.** Dumusque et al. 2012 announced a candidate
α Cen Bb with M sin i ≈ 1.13 M⊕ in a 3.236-day orbit, which would
have been the lowest-mass planet detected via RV at the time. Plavchan
2015 independently re-analyzed the data and could not reproduce a
significant signal at the claimed period. Rajpaul et al. 2016 ("Ghost
in the time series") demonstrated that the Dumusque signal is a
window-function artifact of the irregular HARPS sampling cadence;
neither Demory 2015 (HST transit photometry) nor Krishnamurthy 2021
(ASTERIA transit search) found any planetary signature. The current
consensus is no confirmed planet around α Cen B, leaving the visual
HZ in B (~0.5–0.9 AU; Wang 2022, Heller 2014) as an empty but
dynamically stable basin for future searches.

**Scenario choice for NearStars: a quiet, slightly metal-rich K1V
star with a longer activity cycle than A, no confirmed planets, and
a recognizable warm-orange visual signature distinct from A's
cream.** All 16 cfg picks are canonical-aligned; the Dumusque 2012
history is captured in the `has_planet_b: false` decision row and in
the Open items.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | K1V | high | Porto de Mello 2008; IAU MK |
| `mass_msun` | 0.9373 ± 0.0028 | high | Pourbaix & Boffin 2016 |
| `radius_rsun` | 0.8632 ± 0.0037 | high | Kervella 2017 VLTI/PIONIER |
| `teff_k` | 5236 ± 51 | high | Porto de Mello 2008 |
| `luminosity_lsun` | 0.500 | high | derived from R and Teff |
| `metallicity_fe_h_dex` | +0.25 ± 0.04 | high | Porto de Mello 2008 |
| `age_gyr` | 5.3 ± 0.3 | high | Joyce & Chaboyer 2018 (joint with A) |
| `rotation_period_days` | 38 ± 2 | high | DeWarf 2010 (range 36–40) |
| `activity_log_rhk` | −5.0 | high | Henry 1996; DeWarf 2010 |
| `activity_cycle_years` | 8.1 | high | DeWarf 2010 chromospheric cycle |
| `x_ray_log_lx_cgs_min` | 26.5 | medium | Robrade 2016 cycle minimum |
| `x_ray_log_lx_cgs_max` | 27.5 | medium | Robrade 2016 cycle maximum |
| `has_planet_b` | false | high | Rajpaul 2016 retraction of Dumusque 2012; Plavchan 2015 independent re-analysis; Demory 2015 transit non-detection; Krishnamurthy 2021 ASTERIA non-detection |
| `limb_darkening_alpha_h` | 0.1545 ± 0.0044 | high | Kervella 2017 — H band power-law fit |
| `visual_surface_tint_hex_primary` | `#ffcfa0` (warm orange K1V) | high | K1V blackbody at 5236 K |
| `stellar_color_temp_k` | 5236 | high | derived |
| `visual_in_planet_sky_apparent_diameter_arcmin` (from a hypothetical HZ planet at 0.7 AU) | 1.1 | high | derived: 2 R★/a |

## Surface synthesis

The photosphere of α Centauri B is a textbook quiet K1V — moderately
metal-rich (Δ[Fe/H] = +0.25 vs. solar), 5236 K Teff, with 3D
hydrodynamic granulation simulations (Bigot 2006, used by Kervella
2017) reproducing the VLTI/PIONIER visibility data better than 1D
atmosphere models. The H-band power-law limb-darkening exponent
α(B) = 0.1545 ± 0.0044 is slightly stronger than A's, consistent
with the cooler photosphere and steeper temperature gradient at the
surface.

Spot coverage during the 8.1-year activity cycle (DeWarf 2010) is
larger than on A — log R'HK = −5.0 places B in the moderately active
K-dwarf regime, with active region coverage estimated at ~1–2% of
the visible disk during cycle maximum. The Thompson 2017
(arXiv:1702.01647) plage modeling using disk-integrated HARPS spectra
finds asymmetric latitudinal spot distribution consistent with a
~30° tilt of the rotation axis, comparable to but distinct from the
Sun's ~7° solar inclination.

Surface granulation is slightly redder and finer-grained than A's:
the granulation cell size scales with pressure scale height,
~140 km for B against ~180 km for A (Bigot 2006 STAGGER simulations).
The visual disk, viewed from a hypothetical inner-HZ planet at 0.7
AU, presents a slightly more saturated orange limb-darkened sphere
with intermittent dark sunspots and bright faculae during cycle
maximum.

## Atmosphere synthesis

The chromosphere is moderately filled, with Ca II H&K emission cycles
mapped by DeWarf 2010 across 12 years of spectroscopic monitoring.
The transition region and corona produce X-ray emission cycling by a
factor of 10 (log L_X = 26.5–27.5 cgs over the 8.1-yr cycle, Robrade
2016) — somewhat more variable than A's factor-of-4 modulation, and
phase-shifted from B's chromospheric cycle by roughly π/2 (Robrade
2016 §4).

Lisogorskyi 2019 (arXiv:1902.10711) characterized α Cen B's
activity-induced RV jitter in HARPS spectra at ~1.5 m/s amplitude on
the rotation period — the residual signal that initially appeared as
the Dumusque 2012 planetary signal. Modern RV teams treat α Cen B as
a benchmark for activity decorrelation methods (Cretignier 2020;
Wise 2018; Dumusque 2018), making B the most-monitored K1V star in
the world for the purpose of distinguishing astrophysical jitter from
genuine Doppler shifts.

Stellar wind mass loss is roughly 0.6× the solar rate, scaling with
the X-ray luminosity (Wood 2002 relation). Coronal mass ejections are
detected at modest rate in the X-ray monitoring, but no superflare
events have been recorded in any optical photometry campaign.

## Rotation & spin synthesis

The 38-day rotation period (DeWarf 2010, range 36–40 d) is slow for
a K1V but consistent with the 5.3 Gyr age via Skumanich braking. The
rotation axis inclination remains uncertain — Lisogorskyi 2019 places
i ~ 30°–70° based on jitter-amplitude modulation, while DeWarf 2010
spot-modulation envelope is consistent with the same range. NearStars
adopts an axis tilted ~45° to the line of sight from α Cen A's
direction, which fits the upper-mid range of the constraints.

Asteroseismic detection of p-modes in B is more challenging than in
A due to the lower surface luminosity, but Kjeldsen 2005 detected
37 modes with frequency separation Δν = 160.1 ± 0.1 μHz and ν_max
near 4000 μHz, both consistent with the larger frequency density of
a K1V envelope (Joyce 2018 §2.3). Differential rotation has not been
directly resolved.

## Visual styling

In NearStars, α Cen B renders as a warm-orange K1V with the
`#ffcfa0` photospheric tint — clearly distinct from A's cream and
visually similar to other K-dwarfs in the catalog (e.g., ε Eri).
The 5236 K stellar SED feeds the in-game illumination engine for any
hypothetical planet at B's habitable zone, producing a sunset-orange
ambient lighting rather than the solar white of A.

Viewed from a candidate inner-HZ planet at 0.7 AU, B fills 1.1
arcmin angular diameter (roughly twice the Sun seen from Earth) and
casts a noticeably warmer light. The companion A at ~11-36 AU
separation appears as a brilliant point source ranging from V = −5.0
at apastron (still unresolved) to V = −7.0 at periastron — about
twice the brightness of Venus seen from Earth at greatest
elongation, casting visible shadows on a planetary surface.

Sunspots, faculae, and Ca II plages are rendered at modest scale
during cycle maximum (every 8.1 years), with phase offsets in the
X-ray cycle handled by the cfg `activity_cycle_years` field as the
chromospheric phase reference. The Robrade 2016 X-ray cycle phase
offset (90° from chromosphere) is a separate cfg variant in Open
items.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Kervella P. et al. 2017** — arXiv:1610.06185 (shared with A
  bibliography). R_B = 0.8632 ± 0.0037 R☉; α(B) = 0.1545 ± 0.0044.
- **Pourbaix D. & Boffin H. M. J. 2016** — arXiv:1601.01636. M_B =
  0.9373 ± 0.0028 M☉ from the binary orbital fit.
- **Joyce M. & Chaboyer B. 2018** — arXiv:1806.07567. System age
  5.3 ± 0.3 Gyr.
- **DeWarf L. E. et al. 2010** — (`2010ApJ...722..343D`,
  no arXiv preprint, Tier A manual followup). Defines B's 36–40 d
  rotation, log R'HK = −5.0, and 8.1-yr chromospheric cycle.
- **Henry T. J. et al. 1996** — (`1996AJ....111..439H`, no arXiv).
  Original log R'HK = −5.00 measurement for B.
- **Rajpaul V. et al. 2016** — *Ghost in the time series: no planet
  for Alpha Cen B*, MNRAS 456, L6 (arXiv:1510.05598). Window-function
  reanalysis of Dumusque 2012; rules out the claimed 3.236-d planet.
- **Plavchan P. et al. 2015** — *What is the Mass of α Cen B b?*
  (arXiv:1503.01772). Independent re-analysis of Dumusque 2012;
  reaches the same conclusion.
- **Demory B.-O. et al. 2015** — *HST search for the transit of the
  Earth-mass exoplanet α Centauri B b*, MNRAS 450, 2043
  (arXiv:1503.07528). HST/STIS photometry rules out a transiting
  Earth-mass planet at the claimed 3.236-d period.
- **Thompson A. P. G. et al. 2017** — *The changing face of α Centauri
  B: probing plage and stellar activity in K dwarfs*, A&A 596, A21
  (arXiv:1702.01647). Plage / spot latitudinal distribution and
  rotation-axis inclination constraint.
- **Lisogorskyi M. et al. 2019** — *Activity and telluric
  contamination in HARPS observations of α Centauri B*, MNRAS 485,
  4804 (arXiv:1902.10711). Characterizes the 1.5 m/s activity-driven
  RV jitter that gave rise to the Dumusque 2012 false claim.
- **Robrade J. et al. 2016** — arXiv:1612.06570. 8.1-yr coronal X-ray
  cycle on B, log L_X = 26.5–27.5 amplitude.
- **Heller R. & Armstrong J. 2014** — *Superhabitable Worlds*, AsBio
  14, 50 (arXiv:1401.2392). Frames the K1V HZ as physically more
  favorable than the solar HZ for surface life retention.

### Read (context / methodology, not decision-driving)

- **Kjeldsen H. et al. 2005** — Solar-like oscillations in α Cen B
  (arXiv:astro-ph/0508609). Asteroseismic p-mode detection.
- **Eggl S. et al. 2013** — *Circumstellar habitable zones of binary-
  star systems in the solar neighbourhood* (arXiv:1210.5411). Sets
  the binary-perturbation HZ edges.
- **Cretignier M. et al. 2020** — *Measuring precise radial velocities
  on individual spectral lines II* (arXiv:1912.05192). RV jitter
  decorrelation methodology.
- **Liseau R. et al. 2016** — *ALMA's view of the nearest neighbors to
  the Sun. The submm/mm SEDs of the α Centauri binary* (arXiv:
  1608.02384). Photospheric far-IR/sub-mm continuum.
- **Wiegert J. et al. 2014** — Dust around α Cen, infrared excess
  search (arXiv:1401.6896). No significant debris excess detected.

### Read (instrument / non-cfg-decisive)

- **Spada F. et al. 2019** — arXiv:1909.00701. Entropy calibration of
  K-dwarf radii, validates Kervella 2017.
- **Krishnamurthy A. et al. 2021** — ASTERIA transit search around α
  Cen A and B (`2021AJ....161..275K`). Non-detection limits.

### Not read — no arXiv preprint or low-priority (~40 papers)

- **Dumusque X. et al. 2012** — *An Earth-mass planet orbiting α
  Centauri B*, Nature 491, 207 (`2012Natur.491..207D`, no arXiv).
  Original RV-jitter-driven retracted detection; superseded by
  Rajpaul 2016 and Plavchan 2015.
- Conference proceedings, interstellar-propulsion proposals, and SETI
  searches contribute no cfg-decisive content; preserved in
  `docs/phase3/_bib/alpha-centauri-b.yaml` with `status: skipped`.

## Open items for follow-up

- **Independent inclination measurement**: Lisogorskyi 2019 and
  Thompson 2017 give overlapping but loose constraints (i = 30–70°).
  An asteroseismic rotational splitting analysis or interferometric
  spot mapping could tighten this.
- **Cycle phase relationship**: Robrade 2016 §4 shows that B's
  chromospheric and coronal cycles are ~π/2 out of phase. The cfg
  currently stores only the chromospheric cycle as the master phase;
  a coronal-cycle phase offset variant is a future cfg refinement.
- **Possible long-period planets**: Rajpaul 2016 rules out the
  Dumusque 2012 short-period claim but does not exhaustively
  constrain longer-period (months to years) planets in B's HZ. The
  Beichman & Sanghi 2025 MIRI direct-imaging campaign on α Cen A
  has parallel data on B; a confirmed companion at the 1+ AU range
  would require a new `has_planet_*` Decisions row.
- **High-spatial-resolution photosphere**: 3D STAGGER granulation
  patterns for B (Bigot 2006) are not in the cfg's scalar
  `limb_darkening_alpha_h`; a cfg variant capturing the 3D
  granulation could support extreme close-up flybys.

## Related

- [alpha-centauri-a](alpha-centauri-a.md) — binary partner; G2V primary, shares all dynamical solutions (Pourbaix & Boffin 2016)
- [proxima-cen](proxima-cen.md) — wide CPM companion at ~13,000 AU
- [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) — α Cen AB worked example (§9)
- [methodology](../reference/methodology.md) — Decisions schema
- [rex-data-comparison](../reference/rex-data-comparison.md) — α Cen B parameters comparison
- [stellarium-binary-orbit-comparison](../../plans/stellarium-binary-orbit-comparison.md) — visual-orbit cross-check
