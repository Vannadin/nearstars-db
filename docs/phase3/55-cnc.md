<!-- 55 Cnc A Phase 3 synthesis: cfg-ready decisions and reasoning -->
# 55 Cancri A — Phase 3 Synthesis

55 Cancri A (ρ¹ Cnc, HD 75732, HIP 43587, HR 3522, Gaia DR3
704967037090946688) is a bright, nearby K0 IV-V dwarf at the
G–K boundary, 12.59 ± 0.01 pc (41.0 ly) from the Sun via Gaia DR3
parallax 79.448 ± 0.043 mas. At V = 5.95 it sits just at the
naked-eye threshold in Cancer, and is one of the three brightest
stars known to host a transiting exoplanet. The fundamental
parameters are anchored on von Braun et al. 2011, a dedicated
stellar-parameters paper that directly resolved the star with CHARA
interferometry: θ_LD = 0.711 ± 0.004 mas → R = 0.943 ± 0.010 R☉,
with a direct Teff = 5196 ± 24 K and a bolometric luminosity
L = 0.582 ± 0.014 L☉. The star is mildly evolved off the
zero-age main sequence — hence the IV-V luminosity class — but is
otherwise a slightly cooler, slightly less luminous near-solar
analog. It is famously super-metal-rich ([Fe/H] ≈ +0.31 to +0.42,
not curated here per project policy).

The star is old and very quiet. Bourrier et al. 2018 measured a
rotation period of 38.8 ± 0.05 d (from a sine fit to the Hα
activity-index residuals, corroborated by Season-9 APT photometry
at 40.4 d and the ~39 d Ca II period of Henry 2000), a chromospheric
index log R'HK = −5.03, and a solar-like magnetic activity cycle of
≈ 10.5 ± 0.3 yr (KECK HIRES S-index; ~11.8 yr in Hα), confirming
55 Cnc A is an old (~10 Gyr) inactive star. Moutou et al. 2025
independently recovered P_rot = 38.7 ± 0.8 d (quasi-periodic GPR)
and a large-scale magnetic field of only ~0.3 G at cycle minimum
rising to ~3 G at maximum — about ten times weaker than the Sun's
field. The system hosts five planets (e, b, c, f, d in period order)
spanning a USP lava super-Earth to a cold ~3.8 M_Jup giant, plus a
possible sixth long-period candidate entangled with the magnetic
cycle (Moutou 2025).

A second sun shares the system. 55 Cnc B is a mid-M red dwarf
(M4.5V; Teff ≈ 3200 K, M ≈ 0.26 M☉) at a projected separation of
~1065 AU (84″ visual; Eggenberger 2004 / Mugrauer 2006), with an
estimated orbital period of ~30 000 yr (Moutou 2025). It is already
in the NearStars DB as a separate body (`55_cnc_b`, hosting its own
two planets) and has **no published Keplerian orbit** — the A–B pair
is left unmodeled (note only), so no binary-orbit is synthesized
here. From a planet around A, B would appear as a faint, distant
orange-red second sun.

**Scenario choice for NearStars: a quiet, mildly evolved,
yellow-orange K0 IV-V near-solar star — slightly cooler and dimmer
than Sol, super-metal-rich, with a Sun-like ~10.5 yr activity cycle
— anchored on the von Braun 2011 CHARA interferometry, hosting a
five-planet retinue and a distant M4.5V red-dwarf companion (55 Cnc B)
at ~1065 AU as a faint second sun.** All physical/activity rows track
the canonical parameter set; the visual hex tint and the
companion-event geometry are the only tie-breaks.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | K0 IV-V | high | DB (Gaia / SIMBAD); mildly evolved subgiant-dwarf at the G–K boundary, often quoted G8 V (Bourrier 2018) |
| `mass_msun` | 0.905 ± 0.015 | high | von Braun 2011 — evolutionary model (Phase 2 recommended; Crida 2018 transit-density 1.015 ± 0.051 is the documented alternative) |
| `radius_rsun` | 0.943 ± 0.010 | high | von Braun 2011 — CHARA interferometry, θ_LD 0.711 ± 0.004 mas (Phase 2 recommended; re-anchors the DB radius previously mis-attributed to Bourrier 2018) |
| `teff_k` | 5196 ± 24 | high | von Braun 2011 — interferometric θ_LD + bolometric flux (Phase 2 recommended; Yee 2017 spectroscopic 5172 ± 18 and Moutou 2025 SPIRou 5198 ± 31 agree within errors) |
| `luminosity_lsun` | 0.582 ± 0.014 | high | von Braun 2011 — bolometric flux (Phase 2 recommended) |
| `metallicity_fe_h_dex` | null (lit. ~+0.31 to +0.42) | low | Skipped per [[feedback-skip-metallicity]]; super-metal-rich (Soubiran 2024 +0.32 ± 0.02; Houdebine 2016 +0.42). Sub-perception color effect; not curated |
| `age_gyr` | ~10 (old) | medium | Bourrier 2018 — old quiet star inferred from log R'HK + slow rotation; Moutou 2025 adopts the >10 Gyr branch over the Ligi 2016 31 Myr interferometric-radius alternative |
| `rotation_period_days` | 38.8 ± 0.05 | high | Bourrier 2018 — Hα activity-index residual sine fit (Phase 2 recommended); Moutou 2025 GPR 38.7 ± 0.8, Folsom 2020 ZDI 39 d, Henry 2000 Ca II ~39 d corroborate |
| `activity_log_rhk` | −5.03 | high | Bourrier 2018 (Phase 2 recommended); Moutou 2025 21-yr mean −5.01 (Isaacson 2024 data) corroborates — very inactive |
| `activity_cycle_years` | 10.5 ± 0.3 | high | Bourrier 2018 — KECK HIRES S-index solar-like cycle (~11.8 yr in Hα; Baluev 2015 RV 12.6 yr consistent) |
| `large_scale_field_g_min` | 0.3 | medium | Moutou 2025 — SPIRou ZDI unsigned field at cycle minimum (subsets #1/#2) |
| `large_scale_field_g_max` | 3.0 | medium | Moutou 2025 — field near cycle maximum (Folsom 2020 measured ~3 G in 2017); ~10× weaker than the Sun's 7–15 G |
| `x_ray_log_lx_cgs_min` | 26.8 | low | Tie-break: no published long-baseline X-ray cycle; scaled from a quiet K0 V analog (HD 69830 / α Cen B locus) at log R'HK = −5.0 |
| `x_ray_log_lx_cgs_max` | 27.3 | low | Tie-break: assumed Sun-like cycle amplitude factor ~3 over the 10.5 yr cycle |
| `limb_darkening_alpha_h` | 0.16 | medium | Power-law H-band estimate from a 1D model atmosphere at 5196 K (Claret–Bloemen 2011 scaling); not measured directly for 55 Cnc A |
| `visual_surface_tint_hex_primary` | `#ffeccf` (warm yellow-orange, between Sol's `#fff8f0` and HD 69830's `#ffe8c8`) | medium | Tie-break: K0 IV-V blackbody at 5196 K; ~200 K cooler than HD 69830's 5394 K, so a touch warmer/oranger. Super-solar [Fe/H] adds mild line-blanketing reddening, below the perception threshold |
| `stellar_color_temp_k` | 5196 | high | derived from Teff (von Braun 2011) |
| `visual_spot_coverage_max` | 0.005 | low | Synthesis: very inactive (log R'HK −5.03), ~0.5% disk spot coverage at cycle maximum (Bourrier 2018 ~2 mmag photometric amplitude) |
| `visual_corona_extent_radii` | 3.0 | low | Synthesis: quiet-Sun-like corona for an old inactive K0 dwarf |
| `companion_present` | true (55 Cnc B, M4.5V, ~1065 AU projected) | high | Eggenberger 2004 / Mugrauer 2006 — 84″ visual; Moutou 2025 P ≈ 30 000 yr. Already in DB as `55_cnc_b`; A–B has NO published Keplerian orbit (left unmodeled) |
| `visual_companion_event_distant_red_second_sun` | true | low | Tie-break: from any A planet, B is a faint orange-red point of light (M4.5V) — a distant second sun rather than a binary disk |

## Surface synthesis

The photosphere of 55 Cnc A sits at the G–K boundary, ~580 K cooler
than Sol. von Braun 2011 resolved it directly with the CHARA Array
(θ_LD = 0.711 ± 0.004 mas), yielding R = 0.943 ± 0.010 R☉ and a
bolometric Teff = 5196 ± 24 K — values that agree to within their
errors with the Yee 2017 high-resolution spectroscopic 5172 ± 18 K
and the Moutou 2025 SPIRou Zeeturbo 5198 ± 31 K. The IV-V luminosity
class flags a star that has begun to evolve off the zero-age main
sequence; combined with the 0.943 R☉ envelope this gives the modest
0.582 L☉ bolometric luminosity. The cfg `limb_darkening_alpha_h` is
a 1D-atmosphere power-law estimate at α(H) ≈ 0.16, slightly stronger
than Sol's 0.14 at the cooler photosphere, consistent with the
Claret–Bloemen 2011 grid for log g ≈ 4.4, Teff ≈ 5200 K. No direct
interferometric limb-darkening profile has been published for the
star.

The defining chemical feature is the extreme metal enrichment.
55 Cnc A is one of the most metal-rich stars in the solar
neighborhood, [Fe/H] ≈ +0.31 to +0.42 (Soubiran 2024 +0.32 ± 0.02;
Houdebine 2016 +0.42; literature spread +0.25 to +0.45). Per project
policy this is not curated as a Phase 2 measurement — the line-blanketing
reddening it produces is below the rendering perception threshold —
but it is worth noting as the physical reason 55 Cnc A formed such a
rich and massive planet retinue. Granulation patterns are expected to
be Sun-like but ~10% smaller in linear scale at the cooler convective
overturn.

Spot coverage is very low. log R'HK = −5.03 (Bourrier 2018) places
55 Cnc A in the lower decile of the local G/K activity distribution,
quieter than the modern Sun, with peak-to-peak photometric variability
of only ~2 mmag over the activity cycle. The cfg adopts a
quiet-Sun spot envelope (~0.5% of disk at cycle maximum) and renders
no prominent active-region structure. Moutou 2025's SPIRou ZDI maps
show a poloidal, mostly non-axisymmetric large-scale field of only
0.3 G at minimum — about ten times weaker than the Sun's mean field.

The visual cream-orange tint `#ffeccf` is interpolated from the K0 IV-V
blackbody at 5196 K — ~200 K cooler than HD 69830 (5394 K, `#ffe8c8`),
so a half-step warmer and oranger, but still well short of the deep
orange of α Cen B (K1V). The super-solar metallicity nudges the SED
marginally toward the red, but imperceptibly at rendering resolution.

## Atmosphere synthesis

55 Cnc A hosts a quiet K0 chromosphere–transition-region–corona
structure typical of an old inactive late-G/early-K dwarf. The Ca II
H&K chromospheric index log R'HK = −5.03 (Bourrier 2018), confirmed
by Moutou 2025's 21-year mean of −5.01, sits at the inactive floor.
Unlike most quiet field stars, 55 Cnc A has a **well-characterized
activity cycle**: Bourrier 2018 detected a solar-like ≈ 10.5 ± 0.3 yr
cycle in the KECK HIRES S-index (amplitude 0.024, nearly twice the
Sun's), with consistent ~11.8 yr in Hα and ~12.6 yr in archival RV
(Baluev 2015). The cycle's anti-correlation between Hα and S-index
mirrors the behavior seen in a handful of other slow-rotating stars.

The large-scale magnetic field is unusually feeble. Moutou 2025's
SPIRou spectropolarimetric campaign caught the star at activity
minimum and measured an unsigned field of just 0.3 G, rising to
~0.9 G as it left minimum, and ~3 G near the 2017 maximum (Folsom
2020) — about ten times weaker than the Sun's 7–15 G range. This is
consistent with the very low log R'HK and the old age.

No published long-baseline X-ray cycle exists for 55 Cnc A. The cfg
adopts a log L_X range 26.8–27.3 cgs spanning Sun-quiet to
Sun-cycle-max analog levels — a tie-break in the absence of a
measured X-ray cycle amplitude, scaled from the quiet K0 V locus.
The integrated XUV luminosity stays well below 10⁻⁴ L_bol, far too
feeble to materially erode an Earth-equivalent atmosphere over Gyr
timescales at the star's habitable zone (~0.67–1.32 AU; von Braun
2011) — though planet f, which spends part of its eccentric orbit
in that zone, is itself a gas giant.

The corona/chromosphere visual extent is rendered at the quiet-Sun
reference — a thin chromospheric layer and a faint corona to ~3 R★,
brightening by ~20% over the 10.5 yr cycle.

## Rotation & spin synthesis

55 Cnc A has a robustly measured rotation period of P_rot = 38.8 ±
0.05 d (Bourrier 2018), derived from a sine fit to the Hα
activity-index residuals after removing the magnetic cycle. It is
corroborated from multiple independent channels: Season-9 APT
photometry gives 40.4 ± 0.8 d (weighted-mean of all photometric
seasons 40.04 ± 0.39 d), Henry 2000's Ca II emission monitoring gives
~39 d, and Fischer 2008's earlier APT photometry 42.7 ± 2.5 d. Moutou
2025 independently recovers 38.7 ± 0.8 d from a quasi-periodic GPR fit
and adopts the 39 d ZDI value of Folsom 2020. The 34–43 d spread
across methods is consistent with a modest level of differential
rotation (Folsom 2020 places an upper limit of 0.065 rad/day).

The slow ~39 d rotation is itself the cleanest argument for the old
age: Moutou 2025 notes that a rotation period > 30 d is not expected
for a 30 Myr solar-type star, which rules out the young (31 Myr)
interferometric-radius branch of the Ligi 2016 stellar-evolution
solution in favor of the >10 Gyr branch — the configuration adopted
here. The slow rotation is the product of ~10 Gyr of magnetic
braking via the Skumanich law.

No asteroseismic mode detection drives the cfg; the predicted ν_max
sits too high for the survey cadences deployed to date and the very
low activity floor offers no help. The cfg adopts no oscillation-driven
brightness modulation. Differential rotation is expected Sun-like but
not directly resolved; the rotation-axis inclination is poorly
constrained (ZDI assumed i ≈ 70–90°). For visual rendering NearStars
adopts an axis tilted modestly to the mean orbital plane of the
five-planet system.

In KSP units the cfg sets the stellar `rotationPeriod` to the measured
38.8 d (Bourrier 2018) — informational; Kopernicus does not animate
stellar rotation directly, but Principia reads `rotationPeriod` for
spin-axis bookkeeping.

## Visual styling

- **Orbit view (system-overview render).** A warm yellow-orange K0
  point hosting a tightly packed inner trio (e at 0.015 AU, lost in
  the glare; b at 0.118 AU; c at 0.247 AU), the eccentric f at
  0.80 AU sweeping the inner edge of the habitable zone, and the cold
  giant d far out at 5.6 AU. The ~4 AU gap between f and d is the
  system's defining architectural feature.
- **Stellar disk (close-up).** Quiet K0 IV-V with the textbook H-band
  power-law limb darkening; granulation cells slightly smaller than
  Sol's; no prominent active regions except a faint cycle-averaged
  spot brightness modulation (~0.5% peak-to-peak) at cfg cycle
  maximum.
- **Stellar color.** Warm yellow-orange `#ffeccf` — between Sol's
  `#fff8f0` and HD 69830's `#ffe8c8`, a touch warmer than the latter
  at its ~200 K cooler Teff. 55 Cnc A is a "redder, mildly evolved
  near-solar" entry in the NS catalog.
- **Activity cycle animation.** Over the 10.5 yr cycle (Bourrier 2018)
  the corona brightens by ~20% and the spot coverage peaks at ~0.5%;
  the large-scale field swings from 0.3 G (minimum) to ~3 G (maximum,
  Moutou 2025). Faint and slow by M-dwarf standards.
- **The distant red second sun (55 Cnc B).** From any planet around A,
  the M4.5V companion at ~1065 AU is an unresolved orange-red point of
  light — far too distant to show a disk (angular diameter ≪ 1″), but
  a recognizably warm second star many magnitudes brighter than any
  background field star. Flagged in the cfg
  `visual_companion_event_distant_red_second_sun`. The A–B orbit is
  unmodeled (~30 000 yr period, no published Keplerian), so B's
  position is treated as fixed on gameplay timescales.
- **Star in sky from Earth.** V = 5.95 places 55 Cnc A at the
  naked-eye threshold in Cancer; in dark-sky conditions it is just
  visible, otherwise one of many 6th-magnitude field stars —
  distinguished only by the in-game telescope view that resolves the
  five-planet system.

## Bibliography

### Read (visual-informative, drove decisions above)

- **von Braun K. et al. 2011** — *The 55 Cancri System: Fundamental
  Stellar Parameters, Habitable Zone Planet, and Super-Earth
  Diameter*, ApJ 740, 49 (`2011ApJ...740...49V`, arXiv:1107.1936).
  CHARA interferometry: θ_LD = 0.711 ± 0.004 mas → R = 0.943 ± 0.010
  R☉, direct Teff = 5196 ± 24 K, bolometric L = 0.582 ± 0.014 L☉,
  evolutionary mass 0.905 ± 0.015 M☉, HZ 0.67–1.32 AU. **Phase 2
  anchor for the entire stellar layer (R, Teff, L, M).**
- **Bourrier V. et al. 2018** — *The 55 Cnc system reassessed*, A&A
  619, A1 (`2018A&A...619A...1B`, arXiv:1807.04301). Two decades of
  photometry + spectroscopy: P_rot = 38.8 ± 0.05 d, log R'HK = −5.03,
  solar-like magnetic cycle P_mag ≈ 10.5 ± 0.3 yr (S-index;
  ~11.8 yr Hα), confirming an old (~10 Gyr) quiet star. Homogeneous
  system refit including the magnetic-cycle Keplerian. **Phase 2
  recommended mass / rotation / activity / planet-e anchor.**
- **Moutou C. et al. 2025/2026** — *Characterizing planetary systems
  with SPIRou: questions about the magnetic cycle of 55 Cnc A and two
  new planets around B*, A&A 705, A190 (`2026A&A...705A.190M`,
  arXiv:2510.11523). SPIRou spectropolarimetry of both A and B;
  P_rot = 38.7 ± 0.8 d (GPR), ZDI field 0.3 G (min) – 3 G (max),
  ~10× weaker than the Sun; adopts age > 10 Gyr; revised outer planet
  d (P 4799 d) and a possible 6th candidate / 13.15 yr 3.8 M_Jup
  signal; discovers two planets around 55 Cnc B. **Postdates the
  model knowledge cutoff — all values value-checked against the
  cached text.**

### Read (context / methodology, not directly decision-driving)

- **Demory B.-O. et al. 2016** — *Variability in the super-Earth
  55 Cnc e*, Nature 532, 207 (`2016Natur.532..207D`,
  arXiv:1505.00269). Spitzer 4.5 μm dayside thermal-emission
  variability; informs planet e's surface/atmosphere synthesis, not
  the stellar layer.
- **Soubiran C. et al. 2024** — Gaia FGK benchmark-star [Fe/H]
  update +0.32 ± 0.02 for 55 Cnc A. Metallicity context (not curated).
- **Folsom C. P. et al. 2020** — ZDI of 55 Cnc A; P_rot = 39 d,
  large-scale field ~3 G near the 2017 maximum; differential-rotation
  upper limit. Corroborates the rotation period.
- **Henry G. W. et al. 2000** — Ca II emission monitoring giving the
  ~39 d rotation period; long-baseline activity context.

### Read (instrument-only, not visual-informative)

- **Ligi R. et al. 2016** — Interferometric stellar-evolution fit
  giving the two-solution (31 Myr young / 13.2 Gyr old) age
  degeneracy; the old branch is adopted on rotation grounds.
- **Crida A. et al. 2018** — Transit-density + interferometry mass
  1.015 ± 0.051 M☉ / R 0.98 R☉ (via Moutou 2025 Table 1); documented
  alternative to the von Braun 2011 mass/radius.

### Not read — no arXiv preprint or low-priority (~30 papers)

Conference proceedings on 55 Cnc dynamical stability, the
historical RV discovery papers (Butler 1997, Marcy 2002, McArthur
2004, Fischer 2008 — superseded for parameters by Bourrier 2018 /
Moutou 2025), and stellar-population metallicity catalogs that use
55 Cnc only as one tracer. The full filtered bib is preserved in
`docs/phase3/_bib/55-cnc.yaml` with `status` annotations.

## Open items for follow-up

- **Sixth-planet candidate.** Moutou 2025 proposes a long-period (~13 yr
  or half) candidate entangled with the magnetic cycle, and a
  separate 13.15 yr / 3.8 M_Jup outer signal (possibly the same body
  as planet d under a different decomposition, possibly a distinct
  outer giant). If a future homogeneous nIR+optical RV campaign
  disentangles the cycle from the planets, a sixth-planet Decisions
  row may be needed.
- **A–B binary orbit.** No published Keplerian (only ~1065 AU
  projected separation, ~30 000 yr estimated period). If astrometric
  acceleration from Gaia DR4 constrains the orbit, the A–B pair could
  be promoted from "note only" to a modeled wide binary.
- **X-ray cycle detection.** No long-baseline X-ray monitoring; the
  cfg `x_ray_log_lx_cgs_min/max` are tie-break scalings. A Chandra /
  XMM campaign could pin the cycle amplitude.
- **Metallicity escalation.** [Fe/H] is skipped per policy; if a
  future renderer becomes sensitive enough to show line-blanketing
  reddening, the +0.32 to +0.42 dex enrichment should be curated and
  the visual tint re-derived.

## Related

- [hd-69830](hd-69830.md) — comparison K0 V quiet star; 55 Cnc A is ~200 K cooler, the "redder near-solar" of the two
- [alpha-centauri-b](alpha-centauri-b.md) — comparison K1V quiet star (55 Cnc A sits warmer than B on the color sequence)
- [55-cnc-e](55-cnc-e.md) — the headline USP lava super-Earth; uses this star's L = 0.582 for its T_eq derivation
- [methodology](../reference/methodology.md) — Decisions schema source for the stellar fields
- [data-sources](../reference/data-sources.md) — paper citation policy inherited by this synthesis
