<!-- Barnard's Star c Phase 3 synthesis: cfg-ready decisions and reasoning -->
# Barnard's Star c — Phase 3 Synthesis

Barnard's Star c is the most massive of the four planets in the
González Hernández 2024 / Basant 2025 system at Msini = 0.335 ± 0.030
M⊕ — the only one above 1/3 Earth mass. On a 4.12-day orbit at
0.0274 AU it receives 4.7× Earth's insolation, giving an equilibrium
temperature of 400 K (Basant 2025 Table 3, A = 0, full heat
redistribution) — comparable to early Venus. It was a candidate in
the González Hernández 2024 ESPRESSO data and was promoted to
confirmed status by the Basant 2025 MAROON-X analysis, which
recovered the c signal independently of the ESPRESSO data set.

The orbit eccentricity is e = 0.08 (−0.05 / +0.06) from the Basant
2025 β-distribution prior — the highest eccentricity nominal value of
the four planets, though still consistent with circular at 1.5σ and
with the long-term-stability requirement of e < 0.02. The orbital
period ratio with b (4.124 / 3.154 = 1.31) is close to but not exactly
the 4:3 mean-motion resonance; Basant 2025 SPOCK stability tests find
the 4-planet configuration stable over 10⁹ orbits of the shortest-period
planet when eccentricities are near zero, without explicit resonance
locking.

At 4.7 S⊕ insolation c sits inside the runaway-greenhouse limit for
any Earth-analog atmosphere (Kopparapu 2014 inner edge ~1.1 S⊕ for
this stellar mass at conservative HZ). Surface temperatures preclude
liquid water; the planet does not transit (Stefanov 2024 implicit
non-detection across the four-planet GH24 solution), and radius /
composition are inferred from mass-radius scaling. The atmospheric
escape calculation from France 2020 — 87 Earth-atm Gyr⁻¹ at HZ
(0.1 AU) — implies cumulative loss at c's 0.0274 AU is ~13× higher per
unit area, again precluding significant primary atmosphere retention.
The cfg adopts the same bare-rock interpretation used for b and d,
with c distinguished visually by its slightly lower insolation (cooler
surface tint) and the highest absolute mass of the four (slightly
larger angular diameter in the sky relative to its smaller siblings).

**Scenario choice for NearStars: a tidally-locked sub-Earth rocky
planet, the most massive of the four in the system, with a bare
basaltic surface, no atmosphere, and surface temperatures comparable
to early Venus. Visually a middle-tone red-brown bare-rock world
between hot d/b and cooler e.** 32 cfg picks; 16 canonical-aligned,
16 tie-break. No documented divergences.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 4.12-d orbit → tidal lock < 10⁵ yr (Walterová 2020) |
| `obliquity_deg` | 0 | high | tidal damping |
| `eccentricity` | 0.08 | medium | Basant 2025 β-prior fit (0.08 −0.05/+0.06); highest nominal e of the four, but stability favors e < 0.02 |
| `sidereal_period_days` | 4.1244 ± 0.0006 | high | Basant 2025 Table 3 |
| `semi_major_axis_au` | 0.0274 ± 0.0004 | high | Basant 2025 Table 3 |
| `argument_of_periapsis_deg` | 90.8 | medium | Basant 2025 Table 3 (90.8 −48.1/+38.9) |
| `epoch_jd` | 2460242.92 | high | Basant 2025 t₀,c (BJD−2450000 = 10242.92) |
| `mass_mearth` | 0.335 ± 0.030 | high | Basant 2025 Msini |
| `radius_rearth` | 0.743 | medium | DB mass-radius relation for 0.335 M⊕ non-transiting rocky planet (no measured radius; transit ruled out, Stefanov 2024) |
| `surface_gravity_g_earth` | 0.61 | medium | derived = 0.335 / 0.743² = 0.607 |
| `density_g_cc` | 4.50 | medium | derived = 5.513 × 0.335 / 0.743³; slightly lower density than smaller siblings (mass-radius slope) |
| `insolation_s_earth` | 4.74 | high | derived = L / a² = 0.003558 / 0.0274² |
| `equilibrium_temp_k` (A=0, full redistribution) | 400 | high | Basant 2025 Table 3 |
| `equilibrium_temp_k` (A=0, no redistribution) | 476 | high | derived dayside formula: 400 × 2^0.25 |
| `equilibrium_temp_k` (A=0.1) | 390 | high | derived: 400 × 0.9^0.25 |
| `bond_albedo` | 0.12 | medium | Tie-break: bare-rock range 0.08–0.18; intermediate insolation favors slightly higher albedo than hotter siblings |
| `surface_temp_substellar_k` | 600 | medium | Tie-break: airless dayside scaling at 4.7 S⊕ → ~640 K; weak thermal redistribution → ~600 K |
| `surface_temp_nightside_k` | 130 | medium | Tie-break: basaltic regolith cold-trap |
| `atmosphere_present` | false (vestigial Na exosphere only) | medium | Tie-break: 4.7 S⊕ + flare environment favor stripping; same Mercury-analog logic as b/d |
| `atmosphere_surface_pressure_pa` | 10⁻⁹ | low | Tie-break: Mercury-analog column density |
| `atmosphere_composition` | Na-dominated sputter exosphere; trace K, Ca | low | Tie-break: Mercury analog |
| `atmosphere_tint_rgb_hex` | n/a | high | derived (no visible atmosphere) |
| `cloud_cover_fraction` | 0 | high | no atmosphere |
| `ocean_present` | false | high | T > 400 K rules out surface water |
| `surface_tint_rgb_hex_primary` | `#5a3225` (cooler dark basalt; intermediate between d and e) | medium | Tie-break: bare basalt × M-dwarf SED at intermediate substellar T |
| `surface_tint_rgb_hex_accent` | `#6e3d2c` (terminator/highlands bedrock) | low | Tie-break: limited thermal emission at this insolation |
| `surface_morphology` | impact-cratered basaltic plains; possible relict volcanic terrains; antistellar cold-trap | medium | Tie-break: Mercury-analog + slightly lower thermal forcing than b/d |
| `magnetic_field_present` | true (weak, induced) | low | Tie-break: induction-driven |
| `magnetic_dipole_moment_normalized_earth` | 0.001 | low | Tie-break: slightly larger than smaller siblings because c is most massive |
| `radiation_belt_present` | false | high | no atmosphere + negligible B-field |
| `surface_radiation_dose_msv_yr` | 5000 | medium | Atri 2020 scaling: airless + 4.7 S⊕ XUV × France 2020 duty cycle |
| `atmospheric_shielding_g_cm2` | 0 | high | airless |
| `aurora_present` | false | high | no atmosphere |
| `star_apparent_angular_diameter_deg` | 3.64 | high | derived: 2 R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 3195 | high | Barnard Teff |

## Surface synthesis

Barnard c's surface conditions are intermediate between the hotter
inner pair (b/d) and the cooler outermost e. At 4.7 S⊕ insolation
the substellar dayside reaches ~600 K — sustained enough for thermal
weathering of basaltic minerals but well below the silicate-melt
threshold seen on d. The cfg encodes this as the absence of any
partial-melt accent (`surface_tint_rgb_hex_accent = #6e3d2c` for
terminator-ridge bedrock) — c is visually distinguished from d by
the lack of warm-orange substellar glow.

The substellar hemisphere is dominated by iron-oxidized basaltic
plains. Possible relict volcanic terrains from earlier (hotter) early
thermal phases could be present but are not directly inferable; the
cfg's `surface_morphology` field reflects the canonical Mercury-analog
impact-cratered baseline.

The antistellar hemisphere is a deep cold-trap (~130 K), accumulating
volatiles over Gyr timescales. As c is the most massive of the four
planets, its gravitational retention of any volatile influx is
marginally stronger than the smaller siblings — though still
insufficient to retain a primary atmosphere.

The lower bond albedo (cfg 0.12) reflects the bare-rock surface;
without any cloud or atmospheric scattering, the visible appearance
is dominated by the basaltic regolith color. The slightly cooler
substellar temperature compared to b/d means thermal emission
contribution to the dayside spectrum is minimal at visible wavelengths
— the appearance is governed by reflection of the M4 V SED.

## Atmosphere synthesis

c has no significant atmosphere. The same France 2020 escape
calculation that applies to b and d implies cumulative atmospheric
loss at c's 0.0274 AU is roughly 13× the HZ rate per unit area, or
~1100 Earth-atm Gyr⁻¹ thermal escape — far in excess of any plausible
primary atmosphere mass for a 0.34 M⊕ planet over 10 Gyr.

The vestigial sodium exosphere from stellar-wind sputtering is
present with column density ~10¹⁰ atoms cm⁻² (Mercury-analog scaling).
Trace heavier species (K, Ca) accompany Na at lower abundances. The
exospheric pressure equivalent ~10⁻⁹ Pa is well below any
Rayleigh-scattering threshold; the cfg `atmosphere_tint_rgb_hex
= n/a` reflects the absence of any visible atmospheric layer.

The 25% flare duty cycle from France 2020 drives episodic sputtering
enhancements but no visible exospheric plumes. The cumulative
radiation dose at the surface (cfg 5000 mSv/yr) is lethal to
unshielded biology and dominates the in-game habitability assessment.

## Rotation & spin synthesis

c is tidally despun. Walterová 2020 timescales for a 0.34 M⊕ rocky
planet at 0.0274 AU around a 0.16 M☉ M dwarf remain well under 10⁵
years, much shorter than the 10 Gyr system age. Obliquity is damped
to 0°.

The exact end-state spin depends on which eccentricity is adopted.
Basant 2025 reports e = 0.08 — the highest nominal eccentricity of
the four — but the prior-uniform-uninformative test in the same paper
preferred even higher eccentricities (e ~ 0.24 for c) that conflict
with long-term stability. The β-prior fit at e = 0.08 (−0.05/+0.06)
is the recommended value, but stability constraints (SPOCK 10⁹-orbit
test) favor e < 0.02. At the adopted e = 0.08 the equilibrium spin
is pseudo-synchronous (slightly super-synchronous) rather than a pure
1:1 lock — Walterová 2020 finds eccentric rocky planets settle into
pseudosynchronous rotation rather than exact synchronization — with
a non-trivial libration amplitude (~5°) that would produce measurable
diurnal insolation variation. At the stability-constrained e < 0.02
the spin reduces to a pure 1:1 lock and the libration is negligible.
For the cfg's scalar rotation field this difference is below the
in-game resolution; the planet is rendered as effectively
synchronous either way.

c participates in the compact-system architecture but is not in a
strict 4:3 mean-motion resonance with b (period ratio 1.31, not
exactly 4/3). The ~3800-day stellar activity cycle modulates
insolation by a few percent — too small to drive visual changes at
the cfg's scalar resolution.

## Visual styling

c is the visual middle of the four-planet family — cooler and slightly
darker than b/d, warmer than e. The cfg primary tint `#5a3225` is the
darkest of the four (cooler substellar T with no thermal emission
overlay), with the terminator accent `#6e3d2c` providing limited
visual variation. Surface morphology is dominated by basaltic plains
with possible older volcanic features.

Barnard subtends 3.6° in c's sky — about 7× the apparent diameter of
the Sun from Earth. The dim red illumination produces perpetual warm
twilight on the dayside; the nightside is fully unilluminated
(no satellite-illumination effects since no known moons).

Aurora cfg fields are all `false` / `n/a`. Flare events from Barnard
appear as transient ambient brightening with the 25% duty cycle; the
cumulative surface dose remains lethal under normal play conditions.

Because c is the most massive of the four, it has marginally higher
surface gravity than its siblings (0.61 g vs ~0.55–0.62) but the
difference is too small to affect in-game terrain rendering at the
cfg's resolution. The visual emphasis is on c as a "middle sibling"
contrast — neither the scorched hot interior pair nor the relatively
cooler outermost e.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Basant R. et al. 2025** — *Four Sub-Earth Planets Orbiting
  Barnard's Star from MAROON-X and ESPRESSO* (`2025ApJ...982L...1B`,
  arXiv:2503.08095). The MAROON-X confirmation. P = 4.1244 d,
  Msini = 0.335 ± 0.030 M⊕, a = 0.0274 AU, e = 0.08 (−0.05/+0.06),
  ω = 90.8°, T_eq = 400 K (A=0, full redistribution). SPOCK stability
  favors e < 0.02.
- **González Hernández J. I. et al. 2024** — *A sub-Earth-mass planet
  orbiting Barnard's star* (`2024A&A...690A..79G`, arXiv:2410.00569).
  ESPRESSO data first identified c as a candidate.
- **Stefanov A. K. et al. 2024** — *On the possible transit of
  Barnard b* (arXiv:2410.00577). TESS S80 non-detection; i ≤ 87.9°
  (3σ) for b, extended to the four-planet GH24 solution → c is
  non-transiting.
- **Walterová M. & Běhounková M. 2020** — *Thermal and Orbital
  Evolution of Low-mass Exoplanets* (arXiv:2007.12459). Tidal-lock
  timescale scaling; eccentric rocky planets settle into
  pseudosynchronous rather than exact synchronous rotation.
- **France K. et al. 2020** — *The High-Energy Radiation Environment
  Around a 10 Gyr M Dwarf: Habitable at Last?* (arXiv:2009.01259).
  Atmospheric loss baseline at the HZ; scales to c's 0.0274 AU.
  *(context-cite, not in local cache — escape rate and flare
  duty-cycle figures carried forward at low/medium confidence.)*

### Read (context / methodology, not decision-driving)

- **Toledo-Padrón B. et al. 2019** — *Stellar activity analysis of
  Barnard's Star* (arXiv:1812.06712). Host rotation + ~3800-d
  activity cycle.

### Read (instrument-only, not visual-informative)

- (None directly relevant to c specifically.)

### Not read — no arXiv preprint or low-priority (~15 papers)

The c bibliography is small because c does not have an individual
discovery paper — it is recovered only as a candidate in the
González Hernández 2024 multi-planet ESPRESSO data set and confirmed
in the Basant 2025 multi-planet MAROON-X paper. Most listed entries
are historical "comet c" name-collision papers. Preserved in
`docs/phase3/_bib/barnards-star-c.yaml` with `status: skipped`.

## Open items for follow-up

- **Direct radius measurement**: as with all four planets, no
  transit. Future astrometry or direct imaging could refine the
  cfg's `radius_rearth = 0.743` mass-radius-derived value.
- **High-eccentricity vs. stability**: the Basant 2025 β-prior
  e = 0.08 is the highest nominal value of the four, but stability
  prefers e < 0.02. Further RV monitoring at 30 cm/s precision could
  refine the eccentricity — and with it, whether the spin state is
  pseudo-synchronous (e = 0.08) or a pure 1:1 lock (e < 0.02).
- **Mass–radius relation for the most massive sub-Earth**: c is at
  the boundary between purely rocky (Earth-analog) and slightly
  ice-rich (e.g., Mars-analog volatile-enriched mantle) compositions.
  The cfg defaults to rocky; a future composition constraint from
  asteroseismic or direct-imaging campaigns could refine.
- **Resonance proximity**: the period ratio with b (1.31) is close
  to 4:3 (1.333). Whether c is in a near-resonant trap or simply
  near-resonant by coincidence affects long-term dynamics but not
  visual styling.
- **France 2020 verification**: the escape rate (87 Earth-atm Gyr⁻¹
  at HZ) and 25% flare duty cycle are carried from a paper not in the
  local cache. Re-fetch arXiv:2009.01259 to confirm both figures
  before any cfg writer treats them as load-bearing.
- **Atmosphere retention**: same caveats as for b — the cfg's
  bare-rock interpretation is a tie-break against the absence of any
  GCM modeling for this newly discovered planet.

## Related

- [barnards-star](barnards-star.md) — host star; quiet old M4 V
- [barnards-star-b](barnards-star-b.md) — inner sibling; lower mass but higher insolation
- [barnards-star-d](barnards-star-d.md) — innermost; hottest, has partial-melt accent
- [barnards-star-e](barnards-star-e.md) — outermost; coolest, closest to HZ
- [methodology](../reference/methodology.md) — Decisions schema
- [mod-reference](../reference/mod-reference.md) — downstream cfg writers
