<!-- Barnard's Star e Phase 3 synthesis: cfg-ready decisions and reasoning -->
# Barnard's Star e — Phase 3 Synthesis

Barnard's Star e is the outermost and lowest-mass of the four
confirmed sub-Earth planets in the system, with Msini = 0.193 ± 0.033
M⊕ on a 6.74-day orbit at 0.0381 AU. It was the weakest candidate in
González Hernández 2024 ESPRESSO data and was promoted to confirmed
status only after Basant 2025 added 112 MAROON-X RVs to the joint
analysis — the joint-fit detection probability for an e analogue
rose from 59% (ESPRESSO alone) to 79% (joint), pushing the signal
above the formal confirmation threshold. At 0.19 M⊕ it ties Proxima d
as the lowest-mass planet ever detected by radial velocity.

At 2.45× Earth's insolation, e is the coolest of the four planets
with an equilibrium temperature of 340 K (Basant 2025 Table 3, A = 0,
full heat redistribution) — close to Venus's 232 K and far above any
liquid-water habitable threshold. The Kopparapu 2014 conservative
inner HZ edge for Barnard's M4 V host is at P ≈ 10 d (a ≈ 0.05 AU);
e at 6.74 d (0.0381 AU) sits just inside that boundary, the closest of
the four planets to the HZ but still firmly in the runaway-greenhouse
parameter space. The cfg interprets e as a borderline Venus-analog —
hot enough to lose any primary water atmosphere via XUV-driven escape
over 10 Gyr, but the only one of the four where a modest secondary
CO₂ atmosphere could plausibly be retained against the France 2020
loss rate.

The orbit eccentricity is e = 0.04 (−0.03/+0.04) (Basant 2025 β-prior),
consistent with circular; stability requires e < 0.02 for long-term
4-planet co-residence per the SPOCK analysis. The 6.74-d period
places the tidal despinning timescale far below the 10 Gyr system age
(10³–10⁶ yr for the bulk of plausible rocky rheologies; Walterová
2020), so a synchronous spin-orbit configuration is expected. The
orbital period ratio with c (6.739 / 4.124 = 1.634) is close to but
not exactly the 5:3 mean-motion resonance.

**Scenario choice for NearStars: a tidally-locked sub-Earth-mass
rocky planet at the inner edge of any potential atmosphere-retention
window — the coolest of the four siblings (T_eq = 340 K) with a
plausible thin CO₂-dominated secondary atmosphere as a tie-break
upgrade over the bare-rock baseline used for b/c/d. Visually a darker,
cooler-toned bare rocky world with subtle Rayleigh haze.** 34 cfg
picks; 16 canonical-aligned, 18 tie-break. The atmosphere-thin choice
over bare-rock is the most interesting tie-break of the four planets.
No documented divergences.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 6.74-d orbit → despin ≪ 10 Gyr age (Walterová 2020) |
| `obliquity_deg` | 0 | high | tidal damping |
| `eccentricity` | 0.04 | medium | Basant 2025 β-prior fit (−0.03/+0.04); consistent with circular |
| `sidereal_period_days` | 6.7392 ± 0.0028 | high | Basant 2025 |
| `semi_major_axis_au` | 0.0381 ± 0.0005 | high | Basant 2025 |
| `argument_of_periapsis_deg` | −27.5 | low | Basant 2025 (low ecc → weak constraint, −96.1/+137.5) |
| `epoch_jd` | 2460245.3 | high | Basant 2025 t_peri |
| `mass_mearth` | 0.193 ± 0.033 | high | Basant 2025 Msini; ties Proxima d as lowest-mass RV planet |
| `radius_rearth` | 0.64 | medium | Tie-break: non-transiting; mass-radius for 0.19 M⊕ Earth-analog rocky → 0.58–0.69 R⊕; interesting-first picks 0.64 (DB mass-radius = 0.637) |
| `surface_gravity_g_earth` | 0.47 | medium | derived = 0.193 / 0.64² = 0.471 |
| `density_g_cc` | 4.0 | medium | Tie-break: lowest density of the four (mass-radius slope, 5.513·0.193/0.64³ ≈ 4.06); could be slightly volatile-enriched |
| `insolation_s_earth` | 2.45 | high | derived from L = 0.003558 L☉ and a = 0.0381 AU (L/a² = 2.451) |
| `equilibrium_temp_k` (A=0, full redistribution) | 340 | high | Basant 2025 Table 3 |
| `equilibrium_temp_k` (A=0, no redistribution) | 405 | high | derived dayside-hemisphere formula (340 × 2^¼ = 404) |
| `equilibrium_temp_k` (A=0.3) | 311 | high | derived (340 × 0.7^¼ = 311) |
| `bond_albedo` | 0.20 | medium | Tie-break: bare-rock or thin-atmosphere range 0.10–0.35; thin CO₂ scenario favors slightly higher albedo via Rayleigh scattering |
| `surface_temp_substellar_k` | 470 | medium | Tie-break: with thin CO₂ atmosphere + modest greenhouse → ~470 K; bare-rock airless ~400 K |
| `surface_temp_nightside_k` | 250 | medium | Tie-break: thin atmosphere allows minor nightside heat transport; bare-rock would give ~150 K |
| `atmosphere_present` | true (thin CO₂-dominated; Venus-analog secondary) | medium | Tie-break: cooler T_eq + larger orbital distance reduce loss rates ~5× vs b/c/d; interesting-first picks atmosphere-thin scenario over fully bare-rock |
| `atmosphere_surface_pressure_pa` | 1000 (0.01 bar) | low | Tie-break: well below Venus's 92 bar (heavy atmosphere implausible for this size); thin secondary CO₂ scaled from Mars analog at higher insolation |
| `atmosphere_composition` | CO₂ 90%, N₂ 7%, trace H₂O / SO₂ / Ar | low | Tie-break: Venus / hot-Mars analog; CO₂-dominated outgassed secondary |
| `atmosphere_scale_height_km` | 14 | medium | derived: kT/μg with T = 340 K, μ = 44, g = 4.6 m/s² → 14 km |
| `atmosphere_tint_rgb_hex` | `#6a3a3a` (faint Rayleigh-reddened thin CO₂ under M-dwarf SED) | medium | Tie-break: Rayleigh-blue heavily reddened by M-dwarf SED + low atmosphere thickness → muted red-violet haze |
| `cloud_cover_fraction` | 0.05 | low | Tie-break: dry thin atmosphere → minimal water clouds; no SO₂ photochemistry intense enough for Venus-style clouds |
| `cloud_morphology` | sparse high cirrus only (if any) | low | Tie-break: thin atmosphere |
| `cloud_tint_rgb_hex` | `#8a6050` (warm taupe — minimal contribution) | low | Tie-break: M-dwarf-illuminated thin clouds |
| `ocean_present` | false | high | T > 350 K dayside rules out liquid water (no surface water cycle even with thin CO₂) |
| `surface_tint_rgb_hex_primary` | `#503020` (cooler dark basalt; coolest of the four planets) | medium | Tie-break: bare basalt × M-dwarf SED at the lowest substellar T of the four |
| `surface_tint_rgb_hex_accent` | `#6a4030` (terminator/highlands; subtle warmer accent) | low | Tie-break: bedrock tones |
| `surface_morphology` | basaltic plains; possible relict aqueous-weathering features from earlier wet phase; antistellar cold-trap | medium | Tie-break: Venus / hot-Mars analog with possibility of aqueous geomorphology from earlier (cooler) phase |
| `magnetic_field_present` | true (weak) | low | Tie-break: smaller core → weaker dynamo; magnetic shielding limited |
| `magnetic_dipole_moment_normalized_earth` | 0.0003 | low | Tie-break: smallest of the four planets (Mercury analogy, not dynamo-modeled) |
| `radiation_belt_present` | false | medium | thin atmosphere + weak B-field → marginal trapped population at most |
| `surface_radiation_dose_msv_yr` | 3000 | low | Atri 2020 scaling (context-cite, not in cache): thin atmospheric shielding (~10 g/cm²) + 2.45 S⊕ XUV × France 2020 duty cycle |
| `atmospheric_shielding_g_cm2` | 10 | medium | derived: 0.01 bar column on 0.47 g surface |
| `aurora_present` | true (faint) | medium | Tie-break: thin atmosphere + weak B-field permits modest aurora during flares |
| `aurora_color_primary_hex` | `#88ff88` (CO₂⁺ Fox–Duffendack–Barker green-yellow plus minor O I emission) | low | Tie-break: CO₂-dominated photochemistry; visible only during flare-peak XUV |
| `aurora_intensity_kR_typical` | 5 | low | Tie-break: weak B-field + thin atmosphere + modest Barnard XUV → 0.5× Earth's typical 10 kR |
| `star_apparent_angular_diameter_deg` | 2.61 | high | derived: 2 R★ / a × (180/π) = 2.62 |
| `stellar_illumination_color_temp_k` | 3195 | high | Barnard Teff |

## Surface synthesis

Barnard e's surface conditions are the most "habitable-adjacent" of
the four planets — though still firmly outside any conservative HZ.
Substellar dayside temperatures of ~470 K under the cfg's thin-CO₂
atmosphere scenario allow basaltic regolith without partial melt;
the surface tint (`#503020`) is the darkest and coolest of the four
to reflect the lowest insolation. Terminator-ridge accent (`#6a4030`)
provides modest visual variation.

The thin-atmosphere scenario opens the possibility of subtle
geomorphic features absent on the airless siblings. If e ever
experienced a wetter early phase before the cumulative XUV escape
desiccated it, relict drainage networks or chemically weathered
basaltic terrains could be preserved. The cfg's `surface_morphology`
field includes "possible relict aqueous-weathering features" as a
visual nuance — a tie-break choice motivated by the cooler-end of
the four-planet ensemble.

The antistellar hemisphere remains a cold-trap, though at ~250 K
(considerably warmer than b/c/d's ~100–130 K) because the thin
atmosphere allows nightside heat transport. Substellar-to-antistellar
day-night temperature contrast is ~220 K — much smaller than the
airless 600 K contrast on the other planets.

Mass-radius for 0.19 M⊕ Earth-analog rocky gives 0.58–0.69 R⊕; the
cfg's 0.64 R⊕ choice is midpoint and matches the DB's mass-radius
value (0.637). The density 4.0 g/cc is the lowest of the four planets
— consistent with either (a) slight volatile enrichment (a few wt%
H₂O / CO₂ in the mantle) or (b) simply the mass-radius slope for small
rocky planets. A direct radius measurement would distinguish, but no
transit detection exists (Stefanov 2024, i < 87.9°).

## Atmosphere synthesis

The cfg adopts a thin CO₂-dominated secondary atmosphere for e as
the canonical tie-break upgrade over the bare-rock baseline used for
b/c/d. The motivating physics: at 2.45 S⊕ insolation and 0.0381 AU
orbital distance, the France 2020 atmospheric loss rate scales down
to roughly 1/5 the inner-system value per unit area. Cumulative loss
over 10 Gyr is still high — ~10²–10³ Earth-atm equivalent — but
plausibly within the budget of sustained volcanic outgassing for an
0.19 M⊕ planet over the same timescale. This produces a Venus-analog
secondary atmosphere at a fraction of Venus's column density: the
cfg's 0.01 bar surface pressure is ~10⁻⁴ of Venus's 92 bar. (France
2020 is cited here for the loss-rate framing but is not in the local
paper cache — the loss-rate scaling is the report's own order-of-
magnitude estimate, not a quoted figure.)

Composition: CO₂ 90%, N₂ 7%, trace H₂O / SO₂ / Ar. The CO₂ dominance
follows from photodissociation-resistant outgassing chemistry common
to Venus / hot-Mars analogs. Water vapor is locked at low abundance
because surface temperatures preclude liquid water and any H₂O that
outgasses is rapidly XUV-photolyzed with H escape. SO₂ trace is
included because basaltic volcanism delivers sulfur compounds; in
the thin-atmosphere regime, SO₂ photochemistry does not generate
sustained sulfuric-acid cloud decks (unlike Venus's thick atmosphere).

The cfg's `atmosphere_tint_rgb_hex = #6a3a3a` represents the heavily
red-shifted Rayleigh scattering under Barnard's M4 V SED — much
dimmer and redder than the blue sky of Earth, in line with the
M-dwarf habitable-zone-planet color modeling reviewed for Proxima b.
The atmosphere is too thin to produce strong scattering features
from orbit; the limb haze is faint and warm-toned.

Cloud cover is minimal (5%) given the dry composition. No Venus-style
sulfuric-acid clouds (the atmosphere is too thin and the SO₂
abundance too low); no water clouds (no surface water source). Sparse
high-altitude cirrus (cfg `cloud_morphology`) is possible from trace
water condensation in the upper atmosphere but provides only minor
visual variation.

Aurora rendering is the most subtle of any planet in this synthesis:
weak B-field + thin atmosphere + modest Barnard XUV produces ~5 kR
intensity (half of Earth's typical), visible only during peak flare
states (~25% duty cycle). The primary emission color `#88ff88` traces
CO₂⁺ Fox–Duffendack–Barker bands; this is a tie-break choice over a
red-orange N₂⁺ alternative, motivated by the CO₂-dominated atmosphere.

## Rotation & spin synthesis

e is tidally locked at 1:1 (synchronous). Tidal despinning timescales
for a 0.19 M⊕ rocky planet at 0.0381 AU around a 0.16 M☉ M dwarf fall
in the 10³–10⁶ yr range for the bulk of plausible rocky rheologies
(Walterová 2020 finds initial despinning "on the scale of thousands
or millions of years," with only the lowest-dissipation corners of
parameter space exceeding 1 Gyr) — in every case far shorter than the
10 Gyr age, so synchronous rotation is the expected end state.
Obliquity is damped to 0°.

Basant 2025 best-fit e = 0.04 (−0.03/+0.04) is consistent with
circular; SPOCK stability requires e < 0.02 for long-term 4-planet
residency. Libration amplitude at the recommended low eccentricity is
< 1° and does not produce measurable diurnal modulation.

e's 6.74-d orbit is the longest of the four planets, and its closeness
to the conservative HZ inner edge (10 d) makes it the most relevant
target for any future RV-based detection of an actual HZ planet at
~10-42 d. Basant 2025 explicitly rules out planets larger than
0.37–0.57 M⊕ in the 10–42 d window with 99% confidence; future
MAROON-X / ESPRESSO data could push this limit lower.

## Visual styling

e is the visual "cool sibling" of the family — the darkest primary
tint (`#503020`), the only one with a visible (if faint) atmosphere,
and the only one with even subtle aurora. From orbit it would appear
as a dark red-brown disk with a barely perceptible red-violet limb
haze (`#6a3a3a`) and occasional aurora bands during Barnard's flare
states.

Barnard subtends 2.6° in e's sky — about 5× the apparent diameter of
the Sun from Earth — the smallest angular size of the four-planet
family but still a dominant feature of the daylight sky. The thin
atmosphere produces a dim red-violet daytime sky color heavily
reddened by Barnard's SED, transitioning to near-black at the
terminator.

Surface morphology is the most varied of the four — beyond the
canonical basaltic regolith, possible relict aqueous-weathering
features from an earlier (cooler) atmospheric phase could be
preserved. In-game rendering should include the option for occasional
"riverbed" or "chemically-altered patch" terrain features at low
density.

Aurora bands during Barnard flares appear as faint greenish ribbons
(`#88ff88`) at high magnetic latitudes (~60°) during the 25% flare
duty cycle. Intensity is markedly lower than any Earth-analog
reference; in-game brightness should be sub-cinematic, more like
a subtle ambient glow than a dramatic light show. The cumulative
surface dose (cfg 3000 mSv/yr) is the lowest of the four planets but
still well above any habitable threshold.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Basant R. et al. 2025** — *Four Sub-Earth Planets Orbiting
  Barnard's Star from MAROON-X and ESPRESSO* (`2025ApJ...982L...1B`,
  arXiv:2503.08095). The MAROON-X paper that promoted e from
  candidate (59% detection probability from ESPRESSO alone) to
  confirmed (79% from joint MAROON-X + ESPRESSO). P = 6.7392 d,
  Msini = 0.193 ± 0.033 M⊕, a = 0.0381 AU, e = 0.04, ω = −27.5°,
  T_eq = 340 K (A=0, full redistribution); HZ = P 10–42 d; e < 0.02
  favored for stability.
- **González Hernández J. I. et al. 2024** — *A sub-Earth-mass planet
  orbiting Barnard's star* (`2024A&A...690A..79G`, arXiv:2410.00569).
  ESPRESSO data first identified e (6.74 d) as a candidate signal
  ("not within expectations" for detection sensitivity).
- **Stefanov A. K. et al. 2024** — *TESS photometry of Barnard's Star*
  (arXiv:2410.00577). i < 87.9° → the four planets are non-transiting;
  motivates the mass-radius-derived radius.
- **France K. et al. 2020** — *The High-Energy Radiation Environment
  Around a 10 Gyr M Dwarf: Habitable at Last?* (arXiv:2009.01259).
  Atmospheric loss baseline; scales to e's 0.0381 AU. The "habitable
  at last" framing motivates the thin-atmosphere tie-break for e
  over bare-rock alternative. *(Context-cite — not in local paper
  cache; used for framing, no quoted figure.)*
- **Duvvuri G. et al. 2021** — *Reconstructing the EUV Emission of
  Cool Dwarfs* (arXiv:2102.08493). Quiescent EUV reconstruction;
  atmospheric escape modeling input.
- **Walterová M. & Běhounková M. 2020** — *Thermal and Orbital
  Evolution of Low-mass Exoplanets* (arXiv:2007.12459). Tidal-despin
  timescale (thousands to millions of years; >1 Gyr only for the
  lowest-dissipation rheologies).

### Read (context / methodology, not decision-driving)

- **Toledo-Padrón B. et al. 2019** — *Stellar activity analysis of
  Barnard's Star* (arXiv:1812.06712). Host activity cycle + rotation
  (P_rot = 145 d).

### Read (instrument-only, not visual-informative)

- (None e-specific.)

### Not read — no arXiv preprint or low-priority (~15 papers)

The e bibliography is the smallest of the four — e has no individual
discovery paper and the bib is dominated by name-collision historical
papers (Comet Barnard e 1881, 1885, 1887). The radiation-dose Basis
cites Atri 2020 (cosmic-ray surface-dose scaling), which is not in the
local paper cache and is used only as an order-of-magnitude proxy.
Preserved in `docs/phase3/_bib/barnards-star-e.yaml` with
`status: skipped`.

## Open items for follow-up

- **Direct radius measurement**: as with all four planets, no
  transit. Future direct imaging or astrometry could refine the cfg's
  `radius_rearth = 0.64` placeholder. e is the smallest and would be
  hardest to constrain.
- **Bare-rock vs. thin-atmosphere variant**: the cfg's thin-CO₂
  scenario is a tie-break against bare-rock. If future atmospheric
  modeling for newly discovered cool sub-Earth USP planets (e.g.,
  TOI-700-class) excludes thin CO₂ retention, the cfg should revert
  e to bare-rock. The atmospheric mass loss calculation from France
  2020 is suggestive but not conclusive.
- **Wet earlier-phase morphology**: the cfg includes "relict
  aqueous-weathering features" as visual variation. This is purely
  speculative; no direct evidence supports an earlier wet phase for
  any of the four Barnard planets.
- **Aurora visibility**: the cfg encodes faint aurora during flares
  but the intensity is below the threshold of dramatic in-game
  rendering. The user may wish to dial this up for visual interest
  or down for realism.
- **HZ inner-edge planet candidate**: Basant 2025 explicitly searches
  for a hypothetical Barnard f at P > 10 d (in the HZ) and rules out
  planets > 0.37–0.57 M⊕. Future MAROON-X monitoring could detect
  a lower-mass HZ planet — if found, it would supersede e as the
  outermost in the system.
- **Resonance with c**: period ratio 1.634 ≈ 5/3 = 1.667. Whether
  e is in a near-resonant trap or simply near-resonant by coincidence
  affects long-term dynamics.
- **France 2020 / Atri 2020 re-fetch**: both are cited for atmosphere-
  loss and radiation-dose scaling but are not in the local paper
  cache. Re-fetch their arXiv preprints to replace the order-of-
  magnitude estimates with quoted figures before the cfg ships.

## Related

- [barnards-star](barnards-star.md) — host star; quiet old M4 V; "habitable at last?" framing per France 2020
- [barnards-star-b](barnards-star-b.md) — innermost (post-Ribas-retraction); bare rocky
- [barnards-star-c](barnards-star-c.md) — most massive; bare rocky
- [barnards-star-d](barnards-star-d.md) — hottest; substellar partial-melt
- [proxima-cen-b](proxima-cen-b.md) — analog comparison: another M-dwarf HZ-adjacent planet, but inside the conservative HZ at 0.65 S⊕ vs. e's 2.45 S⊕
- [methodology](../reference/methodology.md) — Decisions schema
- [mod-reference](../reference/mod-reference.md) — downstream cfg writers
