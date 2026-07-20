<!-- Barnard's Star d Phase 3 synthesis: cfg-ready decisions and reasoning -->
# Barnard's Star d — Phase 3 Synthesis

Barnard's Star d is the innermost of the four sub-Earth planets around
Barnard's Star, identified as a candidate by González Hernández et al.
2024 (ESPRESSO) and confirmed by Basant et al. 2025 (MAROON-X joint
analysis). On a 2.3402-day orbit at 0.0188 AU it receives ~10× Earth's
insolation from the 0.003558 L☉ M4 V host — the hottest of the four,
with an equilibrium temperature of 483 K (Basant 2025 Table 3, zero
albedo, full heat redistribution). The minimum mass is 0.263 ± 0.024 M⊕
from the MAROON-X + ESPRESSO joint RV fit; the planet does not transit
(Stefanov 2024 finds no TESS transit, i < 87.9°), so radius, density,
and composition are inferred from the mass-radius relation (DB radius
0.694 R⊕) and the broader hot-rocky / Mercury analog.

The orbit has a low best-fit eccentricity (e = 0.04, −0.03/+0.05, from
the Basant 2025 β-distribution prior), close to but not exactly
circular. SPOCK dynamical-stability tests in the Basant paper show the
four-planet configuration remains stable over 10⁹ orbits of d (the
shortest-period planet) for zero eccentricity and for inclinations from
20° to 90°, with e < 0.02 favored for long-term retention. The 2.34-d
period places tidal-locking timescales well under the 8.5–10 Gyr system
age (Walterová 2020 despinning physics), so d is locked into 1:1
synchronous rotation.

At ~10× Earth's insolation, d is comparable to Mercury — far inside any
habitable-zone definition (Basant confirms the HZ for this host is
P = 10–42 d; d's 2.34-d orbit is the innermost of the four). With
Barnard's old-but-detectable high-energy environment (González
Hernández 2024 reports log(L_X/L_bol) ≈ −5.8 from Chandra, citing France
2020), the inner-system XUV exposure at d's distance makes atmospheric
retention over Gyr timescales implausible. The cfg adopts a Mercury-analog
interpretation: a bare basaltic surface, a vestigial sodium-vapor
exosphere from stellar-wind sputtering, and no significant atmospheric
shielding.

**Scenario choice for NearStars: a hot, tidally-locked, sub-Earth-mass
bare-rock planet with iron-oxidized basaltic regolith, a warmer
substellar zone (hot rock, not lava — T_eq 483 K is far below the
silicate solidus), and a thin sputtering-driven Na exosphere. The
hottest of the four Barnard planets, d is the visual benchmark for
"scorched rock" rendering in this system.** This is a canonical-aligned
synthesis: orbital and bulk parameters trace directly to Basant 2025,
and the surface/exosphere visuals are within-window tie-breaks. No
documented divergence — d is too newly discovered for any canonical
climate model to exist, and the tie-break choices have no
weight-advantaged canonical reading to diverge from.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 2.34-d orbit → tidal lock well under system age (Walterová 2020 despinning physics) |
| `obliquity_deg` | 0 | high | tidal damping |
| `eccentricity` | 0.04 | medium | Basant 2025 Table 3 (e = 0.04, −0.03/+0.05, β-prior); consistent with circular within 1σ; stability favors e < 0.02 |
| `sidereal_period_days` | 2.3402 ± 0.0003 | high | Basant 2025 Table 3 |
| `semi_major_axis_au` | 0.0188 ± 0.0003 | high | Basant 2025 Table 3 |
| `argument_of_periapsis_deg` | −51.8 | medium | Basant 2025 Table 3 (low ecc → weak constraint, −93.5/+190.8) |
| `epoch_jd` | 2460243.70 | high | Basant 2025 Table 3 t₀ (BJD−2450000 = 10243.70) |
| `mass_mearth` | 0.263 ± 0.024 | high | Basant 2025 Table 3 (M sin i) |
| `radius_rearth` | 0.694 | medium | DB mass-radius relation (non-transiting → no measured radius); innermost-of-four mass-radius scaling |
| `surface_gravity_g_earth` | 0.55 | medium | derived = 0.263 / 0.694² |
| `density_g_cc` | 4.34 | medium | derived = 5.513 · 0.263 / 0.694³ (follows from DB mass-radius radius; lower than Earth bulk because the M-R relation assigns a relatively large radius to a 0.26 M⊕ body) |
| `insolation_s_earth` | 10.07 | high | derived = L/a² = 0.003558 / 0.0188² |
| `equilibrium_temp_k` (A=0, full redistribution) | 483 | high | Basant 2025 Table 3 (footnote a: zero albedo, full heat redistribution) |
| `equilibrium_temp_k` (A=0.3) | 453 | high | derived = 278.3·(L·0.7)^0.25/√a, Earth-analog Bond albedo |
| `bond_albedo` | 0.10 | medium | Tie-break: hot bare-rock range 0.06–0.15; Mercury 0.12; darker iron-rich basalt → 0.10 mid-range |
| `surface_temp_substellar_k` | 700 | medium | Tie-break: airless substellar peak (no redistribution, A=0) = T_eq,full·√2 ≈ 700 K; below the silicate solidus (~1300 K) → hot solid rock, no melt |
| `surface_temp_nightside_k` | 100 | medium | Tie-break: airless cold-trap analog of Mercury's permanently shadowed polar craters; thermal inertia of basaltic regolith → ~100 K |
| `atmosphere_present` | false (vestigial Na exosphere only) | medium | Tie-break: 10 S⊕ + inner-system XUV strongly favor stripping; Mercury-analog Na exosphere from sputtering |
| `atmosphere_surface_pressure_pa` | 10⁻⁹ | low | Tie-break: Mercury Na exosphere column ~10¹⁰ atoms cm⁻² ↔ ~10⁻⁹ Pa equivalent (Mercury exosphere analog) |
| `atmosphere_composition` | Na-dominated sputter exosphere; trace K, Ca, Mg | low | Tie-break: Mercury analog; sputtering by Barnard wind on basaltic regolith |
| `atmosphere_tint_rgb_hex` | n/a | high | derived (no visible atmosphere) |
| `cloud_cover_fraction` | 0 | high | no atmosphere |
| `ocean_present` | false | high | T_eq 483 K rules out surface water |
| `surface_tint_rgb_hex_primary` | `#6a3a26` (iron-oxidized basaltic regolith under deep red star) | medium | Tie-break: Mercury-style ferrous surface × M-dwarf SED |
| `surface_tint_rgb_hex_accent` | `#9c5532` (warmer substellar regolith + slightly elevated thermal emission) | medium | Tie-break: hottest substellar zone reads warmer/oranger; bare hot rock, no magma at 483 K |
| `surface_morphology` | impact-cratered basalt, warmer bare-rock substellar zone; antistellar cold-trap regolith | medium | Tie-break: Mercury analog + 10 S⊕ thermal forcing (no melt at 483 K) |
| `magnetic_field_present` | true (weak, induced) | low | Tie-break: small iron core + Barnard wind → induction-driven field; Mercury analog |
| `magnetic_dipole_moment_normalized_earth` | 0.0005 | low | Tie-break: Mercury-class very small core dipole (Mercury analogy, not dynamo-modeled) |
| `radiation_belt_present` | false | high | no atmosphere + negligible B-field → no trapped population |
| `surface_radiation_dose_msv_yr` | 10000 | low | Context-cite scaling (Atri 2020-class airless dose + inner-system XUV); no Barnard-specific surface-dose paper in cache — order-of-magnitude only |
| `atmospheric_shielding_g_cm2` | 0 | high | airless |
| `aurora_present` | false | high | no atmosphere to excite |
| `star_apparent_angular_diameter_deg` | 5.3 | high | derived = 2 R★/a × (180/π), R★ = 0.187 R☉ |
| `stellar_illumination_color_temp_k` | 3195 | high | Barnard Teff (González Hernández 2024) |

## Surface synthesis

Barnard d's surface is the hottest in the four-planet system. Its
substellar dayside peaks near 700 K — the airless no-redistribution
limit for 10× Earth's insolation at zero albedo (T_eq,full · √2) — while
the planet-wide equilibrium temperature is 483 K under full heat
redistribution (Basant 2025 Table 3). Critically, 700 K is far below the
silicate solidus (~1300 K): d is hot *solid* rock, not a lava world. The
substellar hemisphere is therefore rendered as a warmer, oranger
regolith zone (accent tint `#9c5532`) rather than a magma pond. This is a
deliberate physical gate — the cfg does not place a molten surface on a
483 K body, and no cited interior-heating mechanism (tidal, induction)
reaches melt temperatures for a 0.26 M⊕ planet on a near-circular orbit.

The antistellar hemisphere is a deeply cold (~100 K) volatile cold-trap,
analogous to Mercury's permanently shadowed polar craters but spanning
the full nightside hemisphere. Any volatiles delivered by cometary or
interstellar dust influx over ~9 Gyr could be sequestered here — water
ice, sulfur compounds, sodium — though no direct detection is possible
for a sub-Earth USP planet at 1.8 pc. Bedrock at the terminator is
iron-oxidized basalt (`#6a3a26` cfg tint), consistent with a broad
Mercury / hot-rocky regolith template; the M-dwarf illumination shifts
the perceived color further into warm red-brown.

Surface morphology is inferred entirely from the Mercury analog: ~9 Gyr
of accumulated impact cratering across both hemispheres. The cfg encodes
this in the `surface_morphology` field; specific in-game terrain
generation should bias the warm substellar patch toward smoother,
oranger-toned regolith and the cold antistellar hemisphere toward heavily
cratered terrain.

## Atmosphere synthesis

d has no atmosphere in the conventional sense. At 0.55 g surface gravity
and ~700 K substellar temperature, the Jeans escape parameter for any
plausible secondary atmosphere is favorable to loss over Gyr timescales:
H₂ escapes thermally, H₂O dissociates and the H escapes, and CO₂ is
XUV-photolyzed with the lighter products lost. González Hernández 2024,
citing France 2020, reports a still-detectable high-energy environment
for this old M dwarf (log(L_X/L_bol) ≈ −5.8 from Chandra); at d's
0.0188 AU orbit — five times closer than the habitable zone — the
inner-system XUV makes cumulative atmospheric retention over the system
lifetime implausible.

What survives is a vestigial sputter-driven exosphere analogous to
Mercury's. Stellar-wind ions striking the basaltic surface dislodge Na
(and to lesser extents K, Ca, Mg) atoms from feldspar / pyroxene
lattices; the resulting cloud is gravitationally unbound at d's
temperature but maintained by continuous sputtering. Column densities are
of order 10¹⁰ atoms cm⁻², equivalent to a surface pressure of ~10⁻⁹ Pa —
well below any visible Rayleigh-scattering signature, so the cfg sets
`atmosphere_tint_rgb_hex = n/a`.

Episodic enhancement during Barnard's modest flares is expected but is
much weaker than the Proxima analog (Barnard is a very quiet, old M
dwarf, log R'HK = −5.82; Toledo-Padrón 2019). The EUV environment of
Barnard's Star has been reconstructed by Duvvuri 2021 (DEM technique on
HST + Chandra data), which underpins the radiation-environment context;
transient sputtering spikes during flares do not produce visible
exospheric plumes at the cfg's scalar tint resolution.

## Rotation & spin synthesis

d is tidally locked at 1:1 (synchronous) with the substellar point fixed
at the planetary-frame 0° meridian. Tidal-despinning timescales for a
0.26 M⊕ rocky planet at 0.0188 AU around a 0.162 M☉ M dwarf are far
shorter than the 8.5–10 Gyr system age (Walterová 2020 despinning
physics), so obliquity is damped to 0° and the spin is synchronized.

The Basant 2025 best-fit eccentricity (e = 0.04 from a β-prior) is
nominally non-zero but stability constraints favor e < 0.02. At this low
eccentricity the synchronous 1:1 resonance dominates over higher-order
(e.g. 3:2 Mercury-style) configurations; if the true eccentricity sits at
the high end of the posterior, a small pseudo-synchronous libration
(amplitude < 1°) would be expected, but the substellar point remains
effectively fixed in the planetary frame.

The ~10-year stellar activity cycle (Toledo-Padrón 2019: 3800 ± 600 d)
modulates substellar XUV exposure by factors of a few; this affects
exospheric column density but not surface tint at the cfg's resolution.

## Visual styling

Barnard d is the visual "hot scorched rock" of the system.

- **Global appearance:** a warm red-brown disk (`#6a3a26`) under deep red
  M4 V illumination (`stellar_color_temp_k = 3195`), with a brighter,
  oranger substellar accent (`#9c5532`) where the hottest bare rock and
  slightly elevated thermal emission combine.
- **Dayside detail:** the classic hot-Mercury phase curve — a fully
  illuminated, near-uniformly cratered dayside with near-zero limb
  darkening and no atmospheric haze.
- **Terminator band:** a sharp terminator with no haze ring; bare-rock
  bedrock tones throughout.
- **Nightside:** fades rapidly into a near-black, ~100 K cold-trap
  hemisphere.
- **Atmosphere haze:** none — the Na exosphere is far below any visible
  scattering signature.
- **Star in sky:** Barnard subtends 5.3° in d's sky — about 10× the
  apparent diameter of the Sun from Earth — and dominates the scene as a
  constant dim red disk.
- **Sister planets in sky:** b, c, and e (all on similarly compact
  orbits) appear as bright moving points; at conjunction the nearest
  sibling subtends a small but resolvable disk.
- **Flare modulation:** Barnard's flares are weak compared to an active
  M dwarf; in-game rendering can encode brief, infrequent ambient
  brightening events, but they are subtle.

The aurora cfg fields are all `false` / `n/a` since there is no
atmosphere to excite. The cumulative surface dose (cfg
`surface_radiation_dose_msv_yr = 10000`, order-of-magnitude only) reaches
lethal levels under normal play, making in-game habitability impossible;
d is purely a hot-rocky visual destination for player exploration.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2503.08095** — Basant R. et al. 2025, *Four Sub-Earth Planets
  Orbiting Barnard's Star from MAROON-X and ESPRESSO*
  (`2025ApJ...982L...1B`). The MAROON-X confirmation paper and the source
  of every load-bearing orbital/bulk value: P = 2.3402 ± 0.0003 d,
  M sin i = 0.263 ± 0.024 M⊕, a = 0.0188 ± 0.0003 AU, e = 0.04
  (−0.03/+0.05), ω = −51.8°, T_eq = 483 K (A=0, full redistribution);
  SPOCK stability over 10⁹ orbits with e < 0.02 favored, HZ at P = 10–42 d.
- **[2410.00569](https://arxiv.org/abs/2410.00569)** — González Hernández J. I. et al. 2024, *A sub-Earth-mass
  planet orbiting Barnard's star* (`2024A&A...690A..79G`). The ESPRESSO
  discovery paper; first identification of the d candidate. Activity cycle
  3200 d, rotation 140 d; reports log(L_X/L_bol) ≈ −5.8 (Chandra, citing
  France 2020).
- **2102.08493** — Duvvuri G. et al. 2021, *Reconstructing the EUV
  Emission of Cool Dwarfs*. DEM reconstruction of Barnard's Star EUV from
  HST + Chandra; informs the radiation-environment context.
- **[2007.12459](https://arxiv.org/abs/2007.12459)** — Walterová M. & Běhounková M. 2020, *Thermal and
  Orbital Evolution of Low-mass Exoplanets*. Tidal despinning into
  synchronous / pseudo-synchronous rotation for close-in rocky planets;
  basis for the tidal-lock decision.

### Read (context / methodology, not decision-driving)

- **2410.00577** — Stefanov A. K. et al. 2024, *A sub-Earth-mass planet
  orbiting Barnard's star: No evidence of transits in TESS photometry*.
  Rules out transits ("no evidence of transiting Barnard b, or any other
  body"); 3σ upper bound i < 87.9°.
- **[1812.06712](https://arxiv.org/abs/1812.06712)** — Toledo-Padrón B. et al. 2019, *Stellar activity
  analysis of Barnard's Star*. P_rot = 145 ± 15 d, long-term activity
  cycle 3800 ± 600 d (~10 yr), log R'HK ≈ −5.86; underlies the quiet-host
  and activity-cycle reasoning.

### Read (instrument-only, not visual-informative)

- (Limited; the d-specific deep_read set is small.)

### Not read — context-cites NOT in the paper cache (flagged for audit)

These were cited in the prior draft for physical context but are **not in
`docs/phase3/_papers/`** and could not be verified directly. Their
specific numbers are not used as Decisions headline values:

- **France K. et al. 2020** ([arXiv:2009.01259](https://arxiv.org/abs/2009.01259)) — *The High-Energy
  Radiation Environment Around a 10 Gyr M Dwarf*. NOT in cache. The prior
  draft's specific figures (25% flare duty cycle, 87 Earth-atm Gyr⁻¹ loss
  at 0.1 AU, ×25–28 scaling, 10²⁹·²–10²⁹·⁵ erg flare energies) could not be
  verified and were removed from the prose; only the existence + X-ray
  context corroborated by González Hernández 2024 is retained.
- **Atri D. 2020** — surface-radiation-dose scaling. NOT in cache; the
  `surface_radiation_dose_msv_yr` row is order-of-magnitude only,
  Confidence low.
- **Killen 2007 / Stamenković & Spohn / Makarov 2012 / Kopparapu 2014** —
  analog/context cites (Mercury exosphere, lava-world thermal models,
  spin-orbit framework, HZ inner edge). Not standalone in the cache; used
  only as qualitative analogs, not as headline values.

### Not read — no arXiv preprint or low-priority

The bib for d is dominated by name-collision noise (Barnard the comet
observer + comet "d" coincidences) and shared multi-planet papers cited
above. Notable skipped items:

- Multi-author M-dwarf planet-occurrence-rate papers that mention Barnard
  but do not constrain individual planet parameters.
- TESS standard-candle photometric papers using Barnard as an RV standard.

## Open items for follow-up

- **Direct mass / radius measurement**: d does not transit (Stefanov
  2024). A future astrometric or direct-imaging campaign (Gaia DR4,
  JWST-MIRI) could yield a true mass and radius. The cfg `radius_rearth =
  0.694` is the DB mass-radius value, not a measurement.
- **Composition by mass-radius relation**: with only M sin i, the
  composition (rocky vs. iron-enriched) is unconstrained. The DB radius
  implies ρ ≈ 4.34 g/cc; a Mercury-like iron-enriched (denser, smaller)
  interior is also viable as a cfg variant.
- **France 2020 ([2009.01259](https://arxiv.org/abs/2009.01259)) re-fetch**: re-cache the high-energy-environment
  paper to restore the duty-cycle and atmospheric-loss figures with direct
  verification. Until then, the atmosphere-loss prose is qualitative.
- **Surface-dose paper (Atri-class)**: cache a primary radiation-dose
  scaling reference to firm up `surface_radiation_dose_msv_yr` beyond an
  order-of-magnitude estimate.
- **Volatile cold-trap signature**: the antistellar cold-trap could retain
  ices delivered over Gyr timescales. A future cfg variant could add a
  `subsurface_ice` patch.
- **Eccentricity vs. stability**: Basant 2025 reports e = 0.04 but
  stability favors e < 0.02. A future joint-fit with tighter priors could
  refine the orbital eccentricity (and the pseudo-sync libration note).

## Related

- [barnards-star](barnards-star.md) — host star; quiet old M4 V; weak flare environment
- [barnards-star-b](barnards-star-b.md) — next-out sibling (still hot rocky)
- [barnards-star-c](barnards-star-c.md) — middle sibling
- [barnards-star-e](barnards-star-e.md) — outermost; closest to the HZ inner edge of the four
- [proxima-cen-d](proxima-cen-d.md) — analog comparison: similar M sin i sub-Earth USP rocky planet around a different M dwarf, but with a much stronger flare environment
- [methodology](../reference/methodology.md) — Decisions schema
- [mod-reference](../reference/mod-reference.md) — downstream cfg writers
