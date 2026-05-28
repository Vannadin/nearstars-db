# Barnard's Star d — Phase 3 Synthesis

Barnard's Star d is the innermost confirmed planet of the four-planet
sub-Earth family announced by González Hernández et al. 2024 (ESPRESSO)
and confirmed by Basant et al. 2025 (MAROON-X joint analysis). On a
2.34-day orbit at 0.0188 AU it receives ~10× Earth's insolation around
a 0.00356 L☉ M4 V host — the hottest of the four planets, with an
equilibrium temperature of 483 K (Basant 2025 Table 3, zero albedo,
full heat redistribution) or up to 496 K assuming no atmospheric
transport. The minimum mass is 0.263 ± 0.024 M⊕ from MAROON-X +
ESPRESSO joint RV; the planet does not transit (Stefanov 2024 TESS
non-detection), so radius, density, and composition are inferred from
mass-radius scaling and the broader Mercury / hot-rocky-USP analog.

The orbit is mildly eccentric (e = 0.04 ± 0.05 from the Basant 2025
β-distribution prior), close to but not exactly circular. SPOCK
dynamical stability tests in the Basant paper show the four-planet
configuration remains stable over 10⁹ orbits of d (the shortest-period
planet) for zero eccentricity and for inclinations from 20° to 90°,
with e < 0.02 favored for long-term retention. The 2.34-d period
places tidal-locking timescales well under 10⁵ years (Walterová 2020
scaling), so d is locked synchronously in the 1:1 spin-orbit
configuration.

At 10× Earth's insolation, d is comparable to early Venus or Mercury
— far inside any habitable-zone definition. The Kopparapu 2014 inner
edge for an M4 V host sits at ~0.1 AU (P = 10 d), and d's 0.0188 AU
orbit lies 5× closer to the star. With Barnard's flare environment
(France 2020: ~25% duty cycle, ~87 Earth-atm Gyr⁻¹ thermal escape at
0.1 AU), the inner-system XUV exposure at d's distance scales up by
~28× — atmospheric retention prospects for d are minimal. The cfg
adopts a Mercury-analog interpretation: bare basaltic surface with a
substellar partial-melt region, vestigial sodium-vapor exosphere from
stellar-wind sputtering, and no significant atmospheric shielding.

**Scenario choice for NearStars: a hot, tidally-locked, Mercury-like
sub-Earth-mass rocky planet with a partially molten substellar pond,
iron-oxidized basaltic regolith elsewhere, and a thin
sputtering-driven Na exosphere. The hottest of the four Barnard
planets — d is the visual benchmark for "scorched rocky" rendering
in this system.** 32 cfg picks; 16 canonical-aligned (orbital + bulk
+ derived thermal), 16 tie-break (surface visuals, composition,
exosphere, magnetic). No documented divergences — d is too newly
discovered for any canonical climate model to exist.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 2.34-d orbit → tidal lock < 10⁵ yr (Walterová 2020 scaling) |
| `obliquity_deg` | 0 | high | tidal damping |
| `eccentricity` | 0.04 | medium | Basant 2025 β-prior fit; consistent with circular within 1σ; stability favors e < 0.02 |
| `sidereal_period_days` | 2.3402 ± 0.0003 | high | Basant 2025 |
| `semi_major_axis_au` | 0.0188 ± 0.0003 | high | Basant 2025 |
| `argument_of_periapsis_deg` | −51.8 | medium | Basant 2025 (low ecc → weak constraint) |
| `epoch_jd` | 2460243.7 | high | Basant 2025 t_peri |
| `mass_mearth` | 0.263 ± 0.024 | high | Basant 2025 Msini |
| `radius_rearth` | 0.65 | medium | Tie-break: non-transiting; mass-radius for 0.26 M⊕ Earth-analog rocky → 0.60–0.70 R⊕; interesting-first picks 0.65 |
| `surface_gravity_g_earth` | 0.62 | medium | derived = 0.263 / 0.65² |
| `density_g_cc` | 5.3 | medium | Tie-break: Earth-analog rocky; Mercury-density 5.4 alternative within window |
| `insolation_s_earth` | 10.07 | high | derived from L = 0.00356 L☉ and a = 0.0188 AU |
| `equilibrium_temp_k` (A=0, full redistribution) | 483 | high | Basant 2025 Table 3 |
| `equilibrium_temp_k` (A=0, no redistribution) | 575 | high | derived dayside formula |
| `equilibrium_temp_k` (A=0.1) | 470 | high | derived |
| `bond_albedo` | 0.10 | medium | Tie-break: hot bare-rock range 0.06–0.15; Mercury 0.12; partial-melt darker — 0.10 mid-range |
| `surface_temp_substellar_k` | 800 | medium | Tie-break: airless dayside scaling → ~830 K; thin Na exosphere + thermal redistribution → ~800 K |
| `surface_temp_nightside_k` | 100 | medium | Tie-break: airless cold-trap analog of Mercury polar shadow; thermal inertia of basaltic regolith → ~100 K |
| `atmosphere_present` | false (vestigial Na exosphere only) | medium | Tie-break: 10 S⊕ + flare environment strongly favor stripping; Mercury-analog Na exosphere from sputtering |
| `atmosphere_surface_pressure_pa` | 10⁻⁹ | low | Tie-break: Mercury Na exosphere column ~10¹⁰ atoms cm⁻² ↔ 10⁻⁹ Pa equivalent (Killen 2007 analog) |
| `atmosphere_composition` | Na-dominated sputter exosphere; trace K, Ca, Mg | low | Tie-break: Mercury analog; sputtering by Barnard wind on basaltic regolith |
| `atmosphere_tint_rgb_hex` | n/a | high | derived (no visible atmosphere) |
| `cloud_cover_fraction` | 0 | high | no atmosphere |
| `ocean_present` | false | high | T > 600 K rules out surface water |
| `surface_tint_rgb_hex_primary` | `#6a3a26` (iron-oxidized basaltic regolith under deep red star) | medium | Tie-break: Mercury surface ferrous reduction × M-dwarf SED |
| `surface_tint_rgb_hex_accent` | `#9c5532` (substellar partial-melt magma glow + thermal emission peak) | medium | Tie-break: T_substellar ≥ 800 K → partial silicate melt visible; thermal emission contributes to dayside color |
| `surface_morphology` | impact-cratered basalt with substellar partial-melt pond; antistellar cold-trap regolith | medium | Tie-break: Mercury analog + 10 S⊕ partial-melt thermal forcing |
| `magnetic_field_present` | true (weak, induced) | low | Tie-break: small iron core + Barnard wind → induction-driven field; Mercury analog |
| `magnetic_dipole_moment_normalized_earth` | 0.0005 | low | Tie-break: Mercury-class very small core dipole |
| `radiation_belt_present` | false | high | no atmosphere + negligible B-field → no trapped population |
| `surface_radiation_dose_msv_yr` | 10000 | medium | Atri 2020 scaling: airless + 10 S⊕ XUV × France 2020 flare duty cycle; lower than Proxima d because Barnard's flare energies are 10⁴× smaller |
| `atmospheric_shielding_g_cm2` | 0 | high | airless |
| `aurora_present` | false | high | no atmosphere to excite |
| `star_apparent_angular_diameter_deg` | 5.3 | high | derived: 2 R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 3195 | high | Barnard Teff |

## Surface synthesis

Barnard d's surface is the hottest in the four-planet system —
substellar dayside temperatures of order 800 K are sustained by 10×
Earth's insolation under bare-rock conditions. The substellar
hemisphere hosts a partial-melt zone where iron-rich basalts soften
and pond: the cfg encodes this as a warmer accent tint (`#9c5532`)
that visually distinguishes d from the cooler bare-rock siblings.
This is a tie-break choice between (a) a fully solidified regolith
(more conservative, Mercury at lower insolation) and (b) a true magma
ocean (would require higher insolation than 10 S⊕ at this size).
Partial-melt ponds are consistent with both lava-world models from
Stamenković & Spohn for Earth-mass planets at 5–10 S⊕ and with the
sustained substellar thermal forcing under tidal lock.

The antistellar hemisphere is a deeply cold (~100 K) volatile
cold-trap, analog to Mercury's permanently shadowed polar craters
but spanning the full nightside hemisphere. Any volatiles delivered
by cometary or interstellar dust influx over 10 Gyr could be
sequestered here — water ice, sulfur compounds, sodium —though no
direct detection is possible for sub-Earth USP planets at 1.8 pc.
Bedrock at the terminator is iron-oxidized basalt (`#6a3a26` cfg
tint), consistent with the broader Mercury / hot-rocky regolith
template; the M-dwarf illumination tints the perceived color further
into warm red-brown.

Surface morphology is inferred entirely from the Mercury analog:
4 Gyr of accumulated impact cratering, overlain by substellar
partial-melt flows that may produce smoother volcanic plains in the
near-substellar zone. The cfg encodes this in the `surface_morphology`
field; specific in-game terrain generation should bias the substellar
patch toward smoother textures and the cold antistellar hemisphere
toward heavily cratered terrain.

## Atmosphere synthesis

d has no atmosphere in the conventional sense. At 0.62 g surface
gravity and 800 K substellar temperature, the Jeans escape parameter
for any plausible secondary atmosphere is favorable to loss over Gyr
timescales: H₂ escapes thermally, H₂O dissociates and the H escapes
hydrodynamically, and CO₂ is XUV-photolyzed and the lighter products
lost. France 2020 (arXiv:2009.01259) modeled the cumulative atmospheric
loss at Barnard's HZ (0.1 AU) at ~87 Earth-atm Gyr⁻¹ for an unmagnetized
1 M⊕ planet — extrapolated to d's 0.0188 AU and 0.26 M⊕ mass, the
effective rate is roughly 25× higher per unit area, making cumulative
atmospheric retention over 10 Gyr implausible.

What survives is a vestigial sputter-driven exosphere analog to
Mercury's. Stellar wind ions striking the basaltic surface dislodge
Na (and to lesser extents K, Ca, Mg) atoms from feldspar / pyroxene
lattices; the resulting cloud is gravitationally unbound at d's
temperature but maintained by continuous sputtering. Column densities
are of order 10¹⁰ atoms cm⁻², equivalent to a surface pressure of
~10⁻⁹ Pa — well below any visible Rayleigh scattering signature, so
the cfg sets `atmosphere_tint_rgb_hex = n/a`.

Episodic enhancement during Barnard's modest flares is expected but
much less dramatic than the Proxima analog: France 2020 detected
individual events of ~10²⁹·²–10²⁹·⁵ erg, orders of magnitude below
Proxima's ~10³³-erg superflares. The enhanced XUV during the flaring
state (Duvvuri 2021: ~8× quiescent EUV) drives transient sputtering
spikes but does not produce visible exospheric plumes at the cfg's
scalar tint resolution.

## Rotation & spin synthesis

d is tidally locked at 1:1 (synchronous) with substellar point fixed
at the planetary-frame 0° meridian. Tidal damping timescales for a
0.26 M⊕ rocky planet at 0.0188 AU around a 0.16 M☉ M dwarf are well
under 10⁵ years (Walterová 2020 scaling), much shorter than the 10
Gyr system age. Obliquity is similarly damped to 0°.

The Basant 2025 best-fit eccentricity (e = 0.04 from a β-prior) is
nominally non-zero but stability constraints favor e < 0.02. At low
eccentricity the synchronous resonance dominates over higher-order
(e.g., 3:2 Mercury-style) configurations (Makarov 2012 framework).
Libration amplitude is small (< 1°), and the substellar point is
fixed in the planetary frame.

The 10-year stellar activity cycle (Toledo-Padrón 2019) modulates
substellar XUV exposure by factors of a few; this affects exospheric
column density but not surface tint at the cfg's resolution.

## Visual styling

Barnard d is the visual "hot scorched rock" of the system. The deep
red M4 V illumination (`stellar_color_temp_k = 3195`) combined with
iron-oxidized basaltic surface produces a warm red-brown global tint
(`#6a3a26`), with a brighter substellar accent (`#9c5532`) where
partial-melt flows and slightly elevated thermal emission combine to
shift color toward orange.

From orbit, the planet shows the classic hot-Mercury phase curve: a
sharp terminator with no atmospheric haze, near-zero limb darkening,
and a fully illuminated dayside fading rapidly into a near-black
nightside. Barnard subtends 5.3° in d's sky — about 10× the apparent
diameter of the Sun from Earth — and dominates the visual scene as
a constant dim red disk.

Flare events from Barnard produce only modest brightness modulation
on d (France 2020 events are weak compared to Proxima's), but the
~25% duty cycle means flare-state illumination is a frequent
occurrence: in-game rendering should encode brief (~5000 s) ambient
brightening events 1–2 times per Earth-week of game time. The aurora
cfg fields are all `false` / `n/a` since there is no atmosphere to
excite.

The cumulative surface dose for any object on d's surface (cfg
`surface_radiation_dose_msv_yr = 10000`) reaches lethal levels under
normal play conditions, making in-game habitability impossible; the
planet is purely a hot-rocky visual destination for player
exploration.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Basant R. et al. 2025** — *Four Sub-Earth Planets Orbiting
  Barnard's Star from MAROON-X and ESPRESSO* (`2025ApJ...982L...1B`,
  arXiv:2503.08095). The MAROON-X confirmation paper. Reports
  P = 2.3402 ± 0.0003 d, Msini = 0.263 ± 0.024 M⊕, a = 0.0188 ±
  0.0003 AU, T_eq = 483 K (A=0, full redistribution); SPOCK
  stability over 10⁹ orbits for e < 0.02.
- **González Hernández J. I. et al. 2024** — *A sub-Earth-mass planet
  orbiting Barnard's star* (`2024A&A...690A..79G`, arXiv:2410.00569).
  The ESPRESSO discovery paper; first identification of d as a
  candidate. Activity cycle 3200 d; rotation 140 d.
- **France K. et al. 2020** — *The High-Energy Radiation Environment
  Around a 10 Gyr M Dwarf: Habitable at Last?* (arXiv:2009.01259).
  Mega-MUSCLES HST + Chandra; 25% flare duty cycle; 87 Earth-atm/Gyr
  thermal loss at 0.1 AU (scales up at d's 0.0188 AU).
- **Duvvuri G. et al. 2021** — *Reconstructing the EUV Emission of
  Cool Dwarfs* (arXiv:2102.08493). Quiescent + flaring EUV flux
  reconstruction; informs the radiation-environment cfg.
- **Walterová M. & Běhounková M. 2020** — *Thermal and Orbital
  Evolution of Low-mass Exoplanets* (arXiv:2007.12459). Tidal-lock
  timescale scaling.

### Read (context / methodology, not decision-driving)

- **Stefanov A. K. et al. 2024** — *A sub-Earth-mass planet orbiting
  Barnard's star: No evidence of transits in TESS photometry*
  (arXiv:2410.00577). Rules out d transits in TESS data.
- **Toledo-Padrón B. et al. 2019** — *Stellar activity analysis of
  Barnard's Star* (arXiv:1812.06712). Host activity cycle + rotation;
  underlies atmospheric escape calculation.

### Read (instrument-only, not visual-informative)

- (Limited; the d-specific deep_read set is small.)

### Not read — no arXiv preprint or low-priority (~150 papers)

The bib for d is dominated by name-collision noise (Barnard the
comet observer + comet d-letter coincidences) and shared multi-planet
papers cited above. Preserved in `docs/phase3/_bib/barnards-star-d.yaml`
with `status: skipped`. Notable items:

- Multi-author papers on M-dwarf planet occurrence rates that mention
  Barnard but do not constrain individual planet parameters
- TESS standard-candle photometric papers using Barnard as RV
  standard

## Open items for follow-up

- **Direct mass / radius measurement**: d does not transit (Stefanov
  2024). A future astrometric or direct-imaging campaign with
  Gaia DR4 or JWST-MIRI could yield true mass + radius. The cfg
  `radius_rearth = 0.65` is a tie-break placeholder.
- **Composition by mass–radius relation**: with only Msini, the
  composition (rocky vs. ice-rich) is unconstrained. The cfg
  defaults to rocky Earth-analog density (5.3 g/cc); a Mercury-like
  iron-enriched (~6.5 g/cc) interior is also viable.
- **Partial-melt geometry**: the substellar partial-melt zone is a
  tie-break choice. Stamenković-style thermal models for 0.26 M⊕
  rocky planets at 10 S⊕ would refine the substellar-vs-deep
  thermal gradient.
- **Volatile cold-trap signature**: the antistellar cold-trap could
  retain water ice and other volatiles delivered by interstellar
  dust over 10 Gyr. A future cfg variant could add a
  `subsurface_ice` patch.
- **Stellar wind sputtering yield**: the cfg adopts a Mercury-analog
  Na exosphere as a tie-break. No direct MHD wind simulation tailored
  to Barnard exists; a Garraffo-style 3D wind model for an old quiet
  M dwarf would refine the exospheric column density.
- **Eccentricity vs. stability**: Basant 2025 reports e = 0.04 but
  stability favors e < 0.02. A future joint-fit with tighter priors
  could refine the orbital eccentricity.

## Related

- [barnards-star](barnards-star.md) — host star; quiet old M4 V; flare environment less aggressive than Proxima
- [barnards-star-b](barnards-star-b.md) — outer sibling (still hot rocky); the canonical "b" letter post-Ribas-retraction
- [barnards-star-c](barnards-star-c.md) — middle sibling; T_eq comparable to Venus
- [barnards-star-e](barnards-star-e.md) — outermost; closest to HZ inner edge of the four
- [proxima-cen-d](proxima-cen-d.md) — analog comparison: similar Msini sub-Earth USP rocky planet around a different M dwarf, but with much stronger flare environment
- [methodology](../reference/methodology.md) — Decisions schema
- [mod-reference](../reference/mod-reference.md) — downstream cfg writers
