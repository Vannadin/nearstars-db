# Barnard's Star b — Phase 3 Synthesis

Barnard's Star b is the original "headline" planet of the four-planet
ESPRESSO/MAROON-X system around the second-closest stellar host. It
is the only one of the four declared a bona-fide confirmed planet by
González Hernández et al. 2024 in the discovery paper; candidates
c, d, and e were promoted to confirmed status in the follow-up
Basant et al. 2025 MAROON-X analysis. Importantly, the current
Barnard b is a *different* object than the historical Ribas et al.
2018 candidate super-Earth at 0.4 AU — Lubin et al. 2021 refuted that
detection as a stellar-activity one-year alias, and González
Hernández 2024 explicitly recovered no signal at the Ribas period in
156 ESPRESSO observations. The b designation in NearStars and in
current literature refers exclusively to the P = 3.154-d planet.

The planet has Msini = 0.299 ± 0.026 M⊕ (Basant 2025; ESPRESSO-only
González Hernández 2024 reported 0.37 M⊕, refined by the joint
MAROON-X fit) on a near-circular 3.1542-day orbit at 0.0229 AU. It
receives 6.8× Earth's insolation, giving an equilibrium temperature
of 438 K (Basant 2025 Table 3, A = 0, full heat redistribution) — far
inside the Kopparapu 2014 conservative habitable zone for the M4 V
host (HZ inner edge at ~0.1 AU, P ≈ 10 d). The planet does not
transit (González Hernández 2024 + Stefanov 2024 TESS non-detection),
so radius and composition are inferred from the Msini and the broader
hot rocky USP analog.

The 3.15-d orbit means tidal locking is essentially certain
(Walterová 2020 timescale < 10⁵ yr for this mass and host), with the
substellar point fixed in the planetary frame. The Basant 2025
β-distribution-prior eccentricity is e = 0.03 ± 0.03 — consistent with
circular, and SPOCK stability tests favor e < 0.02 for long-term
4-planet co-residence. At 6.8 S⊕ insolation and the same France 2020
atmospheric loss environment that affects the inner sibling d, b is
expected to have stripped most of any primary atmosphere over 10 Gyr;
the cfg adopts a bare-rock scenario with a vestigial sodium-vapor
exosphere as the canonical visual baseline.

**Scenario choice for NearStars: a hot, tidally-locked sub-Earth-mass
rocky planet with a bare basaltic surface, sub-Mercury exosphere, and
no atmospheric shielding from Barnard's flare activity. Cooler than
sibling d but still well above any water-stability threshold;
visually a darker red-brown bare-rock world.** 32 cfg picks; 16
canonical-aligned, 16 tie-break. No documented divergences.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 3.15-d orbit → tidal lock < 10⁵ yr (Walterová 2020) |
| `obliquity_deg` | 0 | high | tidal damping |
| `eccentricity` | 0.03 | medium | Basant 2025 β-prior fit; consistent with circular |
| `sidereal_period_days` | 3.1542 ± 0.0004 | high | Basant 2025 |
| `semi_major_axis_au` | 0.0229 ± 0.0003 | high | Basant 2025 |
| `argument_of_periapsis_deg` | 3.8 | medium | Basant 2025 (low ecc → weak constraint) |
| `epoch_jd` | 2460243.38 | high | Basant 2025 t_peri |
| `mass_mearth` | 0.299 ± 0.026 | high | Basant 2025 Msini |
| `radius_rearth` | 0.72 | medium | Tie-break: non-transiting; mass-radius for 0.3 M⊕ Earth-analog rocky → 0.66–0.76 R⊕; interesting-first picks 0.72 |
| `surface_gravity_g_earth` | 0.58 | medium | derived = 0.299 / 0.72² |
| `density_g_cc` | 5.0 | medium | Tie-break: slightly lower than d (Earth-analog rocky vs. Mercury-density iron-enriched) |
| `insolation_s_earth` | 6.79 | high | derived from L = 0.00356 L☉ and a = 0.0229 AU |
| `equilibrium_temp_k` (A=0, full redistribution) | 438 | high | Basant 2025 Table 3 |
| `equilibrium_temp_k` (A=0, no redistribution) | 521 | high | derived dayside formula |
| `equilibrium_temp_k` (A=0.1) | 426 | high | derived |
| `bond_albedo` | 0.10 | medium | Tie-break: bare-rock dark-basalt range 0.06–0.15 |
| `surface_temp_substellar_k` | 700 | medium | Tie-break: airless dayside scaling at 6.8 S⊕ → ~720 K; thin Na exosphere → ~700 K |
| `surface_temp_nightside_k` | 130 | medium | Tie-break: airless cold-trap with basaltic thermal inertia → ~130 K |
| `atmosphere_present` | false (vestigial Na exosphere only) | medium | Tie-break: 6.8 S⊕ + flare environment favor stripping; Mercury-analog Na exosphere |
| `atmosphere_surface_pressure_pa` | 10⁻⁹ | low | Tie-break: Mercury-analog column density × scale equivalent |
| `atmosphere_composition` | Na-dominated sputter exosphere; trace K, Ca | low | Tie-break: Mercury analog |
| `atmosphere_tint_rgb_hex` | n/a | high | derived (no visible atmosphere) |
| `cloud_cover_fraction` | 0 | high | no atmosphere |
| `ocean_present` | false | high | T > 500 K rules out surface water |
| `surface_tint_rgb_hex_primary` | `#5e3526` (cooler iron-oxidized basalt; slightly darker than d) | medium | Tie-break: bare basalt × M-dwarf SED; lower substellar T than d (700 K vs 800 K) → less thermal emission overlay |
| `surface_tint_rgb_hex_accent` | `#7a4530` (terminator ridge basalt) | low | Tie-break: limited thermal emission; bedrock tones at the terminator |
| `surface_morphology` | impact-cratered basaltic terrain; no substellar partial-melt; antistellar cold-trap | medium | Tie-break: Mercury-analog at slightly lower equilibrium temperature than d |
| `magnetic_field_present` | true (weak, induced) | low | Tie-break: induction-driven field; small core |
| `magnetic_dipole_moment_normalized_earth` | 0.0005 | low | Tie-break: Mercury-class very small dipole |
| `radiation_belt_present` | false | high | no atmosphere + negligible B-field |
| `surface_radiation_dose_msv_yr` | 7000 | medium | Atri 2020 scaling: airless + 6.8 S⊕ XUV × France 2020 flare duty cycle |
| `atmospheric_shielding_g_cm2` | 0 | high | airless |
| `aurora_present` | false | high | no atmosphere |
| `star_apparent_angular_diameter_deg` | 4.34 | high | derived: 2 R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 3195 | high | Barnard Teff |

## Surface synthesis

Barnard b's surface is the cooler counterpart to sibling d: substellar
temperatures of ~700 K stop short of widespread silicate partial-melt
seen on d, so the cfg distinguishes b from d by *absence* of a
partial-melt accent. The dominant tint is iron-oxidized basaltic
regolith (`#5e3526`) — slightly darker and cooler in color than d
because of the lower thermal-emission contribution at the same
M-dwarf illumination. Terminator-ridge bedrock (`#7a4530`) provides
modest visual variation.

The antistellar hemisphere is a deep cold-trap (~130 K — slightly
warmer than d's 100 K because of larger heat-flux retention in the
slightly thicker thermal regolith), accumulating volatiles over Gyr
timescales. As with d, volatile sequestration in the antistellar
cold-trap is plausible but not directly observable.

Surface morphology follows the Mercury / hot-rocky template: 4 Gyr
of impact cratering, no plate tectonics, and possible smooth
sub-substellar zones if any past partial-melt mobilization occurred.
The cfg's `surface_morphology` field captures the heavily cratered
basaltic baseline with the substellar zone slightly smoother in
texture than the terminator and antistellar regions.

The Stefanov 2024 TESS non-detection of transits provides an
indirect constraint on b's radius — if the planet were larger than
about 1.5 R⊕, transits would have been detected in the existing
photometric monitoring window. The cfg's R = 0.72 R⊕ is well below
this threshold; mass-radius scaling for 0.3 M⊕ Earth-analog rocky
material gives 0.66–0.76 R⊕, with the 0.72 value chosen as the
mid-range for visual distinction.

## Atmosphere synthesis

b has no significant atmosphere. The atmospheric loss calculation
from France 2020 at the HZ (0.1 AU) gives ~87 Earth-atm Gyr⁻¹ of
thermal escape under the 25% flare duty cycle. At b's 0.0229 AU,
the inner-system enhancement factor is roughly 19× (radial XUV
scaling), so the cumulative loss over 10 Gyr is several orders of
magnitude greater than any plausible primary atmosphere mass for a
0.3-M⊕ planet.

The surviving atmospheric signature is a sputter-driven sodium
exosphere analog to Mercury's. Barnard's stellar wind impacting the
basaltic surface continuously dislodges Na (and K, Ca trace) atoms,
producing a gravitationally unbound exosphere with column density
~10¹⁰ atoms cm⁻². Surface pressure equivalent is ~10⁻⁹ Pa — far
below any Rayleigh-scattering signature, so the visible appearance
is dominated entirely by the surface tint (cfg `atmosphere_tint_rgb_hex
= n/a`).

Episodic enhancement during Barnard's modest flares (~25% duty cycle,
individual energies ~10²⁹·² – 10²⁹·⁵ erg, France 2020) drives transient
sputtering increases. These are much smaller than the analogous
Proxima superflare events but contribute the bulk of the cumulative
atmospheric loss over 10 Gyr. In-game effects are limited to
sub-resolution rendering — no visible exospheric plumes.

## Rotation & spin synthesis

b is tidally locked at 1:1 (synchronous) with substellar point fixed
at the planetary-frame 0° meridian. Walterová 2020 tidal-locking
timescales for a 0.3-M⊕ rocky planet at 0.0229 AU around a 0.16-M☉
M dwarf are well under 10⁵ years, far shorter than the 10 Gyr system
age. Obliquity is similarly damped to 0°.

Basant 2025 e = 0.03 is consistent with circular at 1σ; SPOCK
stability favors e < 0.02. At this low eccentricity the 1:1
synchronous configuration dominates (no 3:2 trap), and libration
amplitude is small (< 1°).

Coupled with the other three planets, b participates in the compact
near-resonant chain (period ratios 3.15:4.12 ≈ 4:5; 2.34:3.15 ≈ 3:4)
but the system is *not* in a strict mean-motion resonance per Basant
2025 SPOCK analysis — the planets are well-spaced enough for long-term
stability without resonance locking.

## Visual styling

Barnard b is the cooler dark-red sibling of d: the cfg's `#5e3526`
primary tint is darker and slightly browner than d's `#6a3a26`,
reflecting both the lower substellar temperature (700 K vs 800 K)
and the absence of partial-melt thermal emission. From orbit b
displays the same sharp-terminator hot-rocky phase curve as d, with
no atmospheric haze and minimal limb darkening.

Barnard subtends 4.3° in b's sky — about 8× the apparent diameter of
the Sun from Earth. The dim red illumination produces a perpetually
dim warm-orange surface lighting; cumulative surface dose remains
lethal under normal play (cfg `surface_radiation_dose_msv_yr = 7000`,
slightly lower than d's because of the cooler substellar T and
reduced XUV flux at the larger orbital radius).

Aurora cfg fields are all `false` / `n/a`. Flare events from Barnard
appear as transient ~5000-s ambient brightening at the cfg's
flare-duty-cycle rate (~25%), without exotic spectral features. The
in-game rendering should emphasize the cooler-tone basaltic surface
to visually distinguish b from the hotter, partial-melt-accented d.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Basant R. et al. 2025** — *Four Sub-Earth Planets Orbiting
  Barnard's Star from MAROON-X and ESPRESSO* (`2025ApJ...982L...1B`,
  arXiv:2503.08095). The MAROON-X confirmation. P = 3.1542 d,
  Msini = 0.299 ± 0.026 M⊕, a = 0.0229 AU, T_eq = 438 K (A=0, full
  redistribution).
- **González Hernández J. I. et al. 2024** — *A sub-Earth-mass planet
  orbiting Barnard's star* (`2024A&A...690A..79G`, arXiv:2410.00569).
  The ESPRESSO discovery; first confirmed planet of the modern Barnard
  system. T_eq = 400 K stated in the abstract from a slightly
  different stellar-parameter set.
- **Stefanov A. K. et al. 2024** — *A sub-Earth-mass planet orbiting
  Barnard's star: No evidence of transits in TESS photometry*
  (arXiv:2410.00577). TESS non-detection ruling out transits;
  constrains R indirectly to < 1.5 R⊕.
- **France K. et al. 2020** — *The High-Energy Radiation Environment
  Around a 10 Gyr M Dwarf: Habitable at Last?* (arXiv:2009.01259).
  Mega-MUSCLES HST + Chandra; 25% flare duty cycle; atmospheric loss
  rates underpinning b's atmosphere-stripped scenario.
- **Lubin J. et al. 2021** — *Stellar Activity Manifesting at a
  One-year Alias Explains Barnard b as a False Positive*
  (`2021AJ....162...61L`; no arXiv preprint). The refutation of
  Ribas 2018 — establishes that the current Barnard b is a different
  planet from the 2018 candidate.
- **Walterová M. & Běhounková M. 2020** — *Thermal and Orbital
  Evolution of Low-mass Exoplanets* (arXiv:2007.12459). Tidal-lock
  timescale scaling.

### Read (context / methodology, not decision-driving)

- **Ribas I. et al. 2018** — *A candidate super-Earth planet orbiting
  near the snow line of Barnard's star* (`2018Natur.563..365R`,
  arXiv:1811.05955). Historical claim, refuted; preserved as
  historical literature context for the b designation.
- **Toledo-Padrón B. et al. 2019** — *Stellar activity analysis of
  Barnard's Star* (arXiv:1812.06712). Host rotation + activity
  underlying the planet's irradiation environment.

### Read (instrument-only, not visual-informative)

- **Choi J. et al. 2013** — *Precise Doppler Monitoring of Barnard's
  Star* (arXiv:1208.2273). Pre-discovery RV upper limits.

### Not read — no arXiv preprint or low-priority (~140 papers)

Mostly historical pre-2024 papers on Ribas 2018 candidate (now
refuted), generic M-dwarf planet-formation theory, and
instrumentation-development papers that mention Barnard as an RV
standard. Preserved in `docs/phase3/_bib/barnards-star-b.yaml` with
`status: skipped`.

## Open items for follow-up

- **Direct radius measurement**: no transit. A future astrometric
  detection (Gaia DR4 or direct imaging) could constrain true mass
  and radius. The cfg's `radius_rearth = 0.72` is a tie-break.
- **Composition by mass–radius**: rocky vs. ice-rich is degenerate
  without radius. The cfg defaults to Earth-analog rocky; a
  Mercury-like iron-enriched alternative is within the window.
- **Lubin 2021 retraction detail**: the refutation paper has no
  arXiv preprint. A future user-pasted abstract or full text would
  let us deep-read the refutation methodology rather than relying
  on the cited summary.
- **Eccentricity vs. stability**: Basant 2025 e = 0.03 ± 0.03 leaves
  open whether b is exactly circular or weakly eccentric. Long-term
  monitoring at 30 cm/s precision could refine this.
- **Atmosphere retention re-modeling**: France 2020 assumed an
  unmagnetized 1 M⊕ planet at 0.1 AU. A dedicated model for b's
  0.299 M⊕ at 0.0229 AU with M-dwarf wind ram-pressure scaling
  would refine the cfg's `atmosphere_present` decision; current
  tie-break leans bare-rock.

## Related

- [barnards-star](barnards-star.md) — host star; quiet old M4 V
- [barnards-star-c](barnards-star-c.md) — next outward; comparable surface conditions at lower insolation
- [barnards-star-d](barnards-star-d.md) — inner sibling; hotter (substellar partial-melt visible)
- [barnards-star-e](barnards-star-e.md) — outermost; closest to HZ inner edge
- [proxima-cen-b](proxima-cen-b.md) — different "b" letter, different host activity environment; useful comparison for atmosphere retention logic
- [methodology](../reference/methodology.md) — Decisions schema
- [mod-reference](../reference/mod-reference.md) — downstream cfg writers
- [rex-data-comparison](../reference/rex-data-comparison.md) — REX lists Ribas-2018-style super-Earth b; NS reflects the post-2024 sub-Earth b
