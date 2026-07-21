# Proxima Centauri d — Phase 3 Synthesis

Proxima Centauri d is a sub-Earth-mass ultra-short-period (USP)
planet candidate first reported as a 0.26 M⊕ object at 5.122 d period
by Faria et al. 2022 (`2022A&A...658A.115F`, [arXiv:2202.05188](https://arxiv.org/abs/2202.05188)), and
confirmed at high significance in the NIRPS + ESPRESSO joint analysis
of Suárez Mascareño et al. 2025 (`2025A&A...700A..11S`,
[arXiv:2507.21751](https://arxiv.org/abs/2507.21751)). At a semi-major axis of 0.029 AU it sits inside
the inner edge of any habitable-zone interpretation; even so, with
Proxima's faint M5.5V illumination (L = 0.00155 L☉) the insolation
is only ~1.9× Earth's, giving an equilibrium temperature of 326 K
(A = 0.3) — comparable to Mercury and above any liquid-water threshold.

The planet has not been seen in transit; Suárez Mascareño 2025 §4
confirms a high orbital inclination that places transit geometry
outside the photometric monitoring envelope. As a result, only the
minimum mass and orbital period are observationally constrained.
Almost every other Decisions row is inferred from comparison with
the best-studied USP analog — Mercury — combined with the constraints
of M-dwarf irradiation and Proxima's flare environment.

**Scenario choice for NearStars: a hot, tidally-locked, Mercury-like
sub-Earth-mass rocky planet with an airless, sun-baked basaltic
surface (substellar peaks ~460 K, far below the silicate solidus →
no melt), a vestigial sodium-vapor exosphere, and no atmospheric
shielding from Proxima's flare output.** 32 cfg picks; 17 canonical-aligned (orbital + bulk
parameters), 15 tie-break (surface visuals, weak atmosphere/exosphere
choice, magnetic field inference) where the literature is silent on
specific values. No documented divergences — Proxima d is too newly
discovered for a canonical climate model to exist.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | USP at 5.12 d → tidal lock < 10⁵ yr (Walterová 2020 scaling) |
| `obliquity_deg` | 0 | high | tidal damping |
| `eccentricity` | 0 | high | SM25 — fit consistent with circular at USP |
| `sidereal_period_days` | 5.122 ± 0.001 | high | Faria 2022; SM25 confirms |
| `semi_major_axis_au` | 0.029 | high | derived from Kepler's 3rd law |
| `mass_mearth` | 0.26 | high | Faria 2022 Msini; SM25 refines slightly |
| `radius_rearth` | 0.65 | medium | Tie-break: non-transiting; mass-radius for ~0.3 M⊕ rocky → 0.6–0.7 R⊕; interesting-first selects 0.65 for visual distinction from Earth |
| `surface_gravity_g_earth` | 0.62 | medium | derived = 0.26 / 0.65² |
| `density_g_cc` | 5.2 | medium | Tie-break: assumed Earth-like rocky; Mercury-density 5.4 alternative within window |
| `insolation_s_earth` | 1.9 | high | derived from L = 0.00155 L☉ and a = 0.029 AU |
| `equilibrium_temp_k` (A=0) | 357 | high | derived |
| `equilibrium_temp_k` (A=0.3) | 326 | high | derived; rocky bond albedo |
| `bond_albedo` | 0.15 | medium | Tie-break: hot rocky range 0.06–0.2; Mercury analog 0.12; interesting-first picks 0.15 between dark basalt and brighter regolith |
| `surface_temp_substellar_k` | 460 | medium | airless substellar peak (no redistribution) at ~1.9 S⊕ ≈ 460 K; far below the silicate solidus (~1300 K) → solid rock, no melt |
| `surface_temp_nightside_k` | 80 | medium | Tie-break: airless cold trap (Mercury nightside ~100 K); slight thermal inertia → ~80 K |
| `atmosphere_present` | false (vestigial Na vapor only) | medium | Tie-break: escape ratio strongly favors loss at ~1.9 S⊕ + Proxima flare environment; interesting-first picks Mercury-analog vestigial exosphere over fully airless |
| `atmosphere_surface_pressure_pa` | 10⁻⁹ | medium | Tie-break: Mercury Na exosphere column density 10¹⁰ /cm² ≈ 10⁻⁹ Pa equivalent (Killen 2007 Mercury exosphere review for analogy) |
| `atmosphere_composition` | sodium-dominated vapor (sputter-produced) | low | Tie-break: Mercury analog; sputtering by Proxima stellar wind on basaltic surface |
| `atmosphere_tint_rgb_hex` | n/a (no visible atmosphere) | high | derived |
| `cloud_cover_fraction` | 0 | high | no atmosphere |
| `ocean_present` | false | high | airless, no stable surface liquid; dayside ~460 K rules out persistent water |
| `surface_tint_rgb_hex_primary` | `#5a3a2a` (iron-oxidized basaltic regolith under red star) | medium | Tie-break: Mercury surface tint × M-dwarf SED; interesting-first selects warm earthy tone over neutral gray |
| `surface_tint_rgb_hex_accent` | `#6a4632` (substellar sun-baked basalt) | low | Mercury-analog substellar regolith reddening; NO melt (substellar ~460 K ≪ silicate solidus ~1300 K) |
| `surface_morphology` | impact-cratered basaltic terrain; substellar sun-baked basalt; antistellar volatile cold-trap regolith | medium | Tie-break: Mercury analog + dayside thermal gradient driven by ~1.9 S⊕ insolation (no melt) |
| `magnetic_field_present` | true (intrinsic, SPI-indicated) | medium | Zapatero Osorio et al. 2026 (`2605.22925`) detect flares phase-locked to Proxima d at ≥99.8% significance — the FIRST star–planet-interaction field estimate for a terrestrial exoplanet. Supersedes the prior unconstrained Mercury-analog guess. Still airless → no rendered aurora |
| `magnetic_dipole_moment_normalized_earth` | 4 | low | From the SPI-derived polar field ~16 G (median, Mars-size) of Zapatero Osorio 2026 (`2605.22925`): M ∝ B_pol·R³ vs Earth (0.6 G polar) → ~4× Earth for a Mars radius. **Order-of-magnitude only** — the paper's 3–280 G range × radius uncertainty spans ~0.5–70× Earth, and it self-labels the field "reliable only at the order-of-magnitude level". Supersedes the prior Mercury-analog 0.001. **Tension with the derived scaling:** the rocky-dynamo ladder ([rocky-planet-dynamo-methodology.md](../reference/rocky-planet-dynamo-methodology.md), RM22) predicts the *opposite* — a small 0.26-M⊕ core at 4.85 Gyr is likely dynamo-dead-to-weak (ℳ ≲ 0.01). The SPI *observation* supersedes the *derivation* (measurement beats scaling), but the mismatch is itself notable: either d retains an unexpectedly strong dynamo, or the phase-locked-flare attribution needs scrutiny |
| `radiation_belt_present` | false | high | no atmosphere + negligible B-field → no trapped particle population |
| `surface_radiation_dose_msv_yr` | 10⁵ | low | Order-of-magnitude estimate, not a measured rate. Atri 2020 ([1910.09871](https://arxiv.org/abs/1910.09871)) provides the SEP→dose *framework* but reports Gray-per-event + dimensionless enhancement-over-GCR factors, NOT annual mSv/yr; the yearly figure here is a conversion (airless dose × flare frequency), so confidence is low despite the strong physical driver. NOTE the SPI-indicated ~16 G field (Zapatero Osorio 2026) could partially deflect SEPs → this no-magnetic-shield value is an upper bound |
| `atmospheric_shielding_g_cm2` | 0 | high | airless |
| `aurora_present` | false | high | no atmosphere to excite |
| `flare_dose_event_msv` | 10⁴ | high | Atri 2020 + Vida 2019 superflare integrated proton dose at d's distance |
| `star_apparent_angular_diameter_deg` | 2.5 | high | derived: 2 R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2980 | high | Proxima Teff |

## Surface synthesis

Proxima d's surface is governed by two competing thermal regimes: a
hot but airless dayside and a deeply cold nightside, with sharp
terminator gradients. At ~1.9× Earth's insolation and an albedo of
0.15, the equilibrium temperature (326 K) is a global mean — the
airless substellar point (no day-night redistribution) peaks only
around 460 K.

That ~460 K substellar peak is far below the basalt/silicate solidus
of ~1200–1300 K, so the dayside is a solid, sun-baked basaltic
surface — there is no melt and no magma pond. An Io-style silicate
volcanism would require a tidal-heating engine, but Proxima d has no
significant tidal heat, so that pathway is ruled out as well. The
substellar accent is therefore a dry regolith-reddening tone rather
than a glow: warm baked basalt visible from a hypothetical spacecraft
as the planet approaches mid-day terminator (`surface_tint_rgb_hex_accent
= #6a4632`).

The antistellar hemisphere is a volatile cold-trap analog of
Mercury's permanently-shadowed polar craters — temperatures near 80 K
can sequester water ice, methane, and sodium volatiles brought in by
the few interstellar / cometary deliveries. The Ipatov 2023 dust /
icy planetesimal delivery models (cited via the system bibliography)
suggest persistent low-flux volatile flux at the inner Proxima
system; volatile retention in the antistellar cold-trap is plausible
but not directly measurable.

Surface morphology — impact craters from 4 Gyr of bombardment, with
the sun-baked substellar regolith overprinting older terrain — is
inferred entirely from the Mercury analog. The cfg `surface_morphology`
field captures this with the standard Mercury-style hummocky basaltic
texture, biased toward the brown-red end of the silicate palette by
the M-dwarf illumination spectrum.

## Atmosphere synthesis

Proxima d has effectively no atmosphere in the conventional sense.
At the surface gravity of 0.62 g_⊕ and a substellar peak ~460 K,
the Jeans-escape parameter for any plausible secondary atmosphere is
favorable for H₂ and H₂O over Gyr timescales. Proxima's intense XUV
output also drives strong hydrodynamic escape; Lee 2021 ([2109.06963](https://arxiv.org/abs/2109.06963)) found that
even Proxima b at 0.05 AU experiences Venus-analog escape rates,
and at d's much closer 0.029 AU the loss rates scale up by another
order of magnitude.

What remains is a vestigial sodium-vapor exosphere — the cfg
tie-break choice over a fully airless model. Sputtering by Proxima's
stellar wind on basaltic surfaces continuously liberates Na atoms
from feldspar / pyroxene lattices, producing a thin, gravitationally
unbound exosphere with column densities ~10¹⁰ atoms/cm² (by analogy
to Mercury, Killen 2007). The associated pressure equivalent (10⁻⁹ Pa)
is well below any visible Rayleigh-scattering or absorption signature,
so the cfg `atmosphere_tint_rgb_hex` is set to "n/a" — the visible
appearance is dominated entirely by the surface tint.

Episodic enhancements of the Na exosphere can be expected during
Proxima superflares (~3 of 10³³ erg per year, Vida 2019) when
increased XUV and particle flux dramatically increase the sputtering
yield. These
events do not produce visible plumes at the cfg's scalar tint
resolution but are flagged in Open items as a future cfg variant.

## Rotation & spin synthesis

Proxima d is tidally locked, with the substellar point fixed at the
0° meridian and a sidereal rotation period equal to its 5.122-day
orbit. Tidal damping timescales for a 0.26-M⊕ rocky planet at
0.029 AU around a 0.12-M☉ M dwarf are < 10⁵ years (Walterová 2020
scaling from Proxima b's longer-period calculation), well within the
~4.85 Gyr system age. Obliquity is similarly damped to 0°.

The spin-orbit resonance is presumed to be 1:1 (synchronous) rather
than the 3:2 resonance held by Mercury, because the orbital
eccentricity is effectively zero (SM25 fit) and only modest e is
required to drive a higher-order resonance trap (Makarov 2012). The
cfg `tidally_locked: true` and `obliquity_deg: 0` capture this
synchronous state.

Libration amplitude around the synchronous state is small (< 1°),
limited by the negligible orbital eccentricity. The substellar point
is fixed in the planetary frame; the daily diurnal cycle disappears
entirely, replaced by the much slower 7-year stellar activity cycle
modulation of substellar temperature.

## Visual styling

Proxima d is the most visually muted of the five entries in this
synthesis. The deep red M5.5V illumination (`stellar_color_temp_k = 2980`)
combined with the iron-oxidized basaltic surface produces a warm,
saturated red-brown global tint (`#5a3a2a`), with a subtle warmer
accent (`#6a4632`) at the sun-baked substellar region. Cratering
and ridge geometry follow the Mercury-analog template.

From orbit, the planet shows the classic hot-Mercury phase curve:
sharp terminator with no atmospheric haze, near-zero limb darkening
beyond the photometric noise, and a fully-illuminated dayside that
fades rapidly into the dark nightside. Proxima fills 2.5° angular
diameter in d's sky — 5× the apparent diameter of the Sun seen from
Earth — and its deep red light dominates the visual scene.

During a Proxima superflare, the planet's dayside experiences a
brief brightening as the increased UV / optical flux scatters off
the surface; the cfg encodes this as a temporary tint modifier on
the visible side. The cumulative flare dose for any object on the
surface reaches lethal levels (10⁴ mSv per ≥ 10³³-erg superflare
per the Atri 2020 scaling), making in-game habitability impossible. The planet is
purely a hot-rocky visual destination for player exploration.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Faria J. P. et al. 2022** — *A candidate short-period sub-Earth
  orbiting Proxima Centauri*, A&A 658, A115
  (`2022A&A...658A.115F`, [arXiv:2202.05188](https://arxiv.org/abs/2202.05188)). The discovery paper.
  Reports P = 5.122 d, Msini = 0.26 M⊕. Orbital eccentricity is
  consistent with circular at the precision of the fit.
- **Suárez Mascareño A. et al. 2025** — *Diving into the planetary
  system of Proxima with NIRPS: Breaking the m/s barrier*, A&A 700,
  A11 ([arXiv:2507.21751](https://arxiv.org/abs/2507.21751)). Confirms Proxima d at high significance;
  refines orbital fit; constrains inclination to high values
  precluding transits in the photometric monitoring envelope.
- **Suárez Mascareño A. et al. 2020** — *Revisiting Proxima with
  ESPRESSO* ([arXiv:2005.12114](https://arxiv.org/abs/2005.12114)). Pre-discovery upper limits
  consistent with a 0.3-M⊕ planet at 5 d.
- **Anglada-Escudé G. et al. 2016** — *A terrestrial planet candidate
  in a temperate orbit around Proxima Centauri*, Nature 536, 437
  ([arXiv:1609.03449](https://arxiv.org/abs/1609.03449)). Host star context — Proxima b discovery used
  the same data baseline that constrained d's eventual identification.
- **Boyajian T. S. et al. 2012** — *Stellar Diameters and Temperatures
  II*, ApJ 757, 112 ([arXiv:1208.2431](https://arxiv.org/abs/1208.2431)). Proxima R = 0.1542 R☉; sets
  the insolation calculation.
- **Atri D. et al. 2020** — *Stellar Proton Event-induced surface
  radiation dose as a constraint on the habitability of terrestrial
  exoplanets* ([arXiv:1910.09871](https://arxiv.org/abs/1910.09871)). Used for the radiation-dose
  Decisions row.
- **Walterová M. & Běhounková M. 2020** — *Thermal and Orbital
  Evolution of Low-mass Exoplanets*, ApJ 900, 24 ([arXiv:2007.12459](https://arxiv.org/abs/2007.12459)).
  Tidal-locking timescale scaling.
- **Vida K. et al. 2019** — *Flaring Activity of Proxima Centauri
  from TESS Observations* ([arXiv:1907.12580](https://arxiv.org/abs/1907.12580)). Superflare rate +
  energy distribution for the dose scaling.

### Read (context / methodology, not decision-driving)

- **Lee Y. et al. 2021** — *Exosphere Modeling of Proxima b*
  ([arXiv:2109.06963](https://arxiv.org/abs/2109.06963)). Order-of-magnitude scaling for d's escape rate.
- **Kossakowski D. et al. 2023** — *The CARMENES search for
  exoplanets around M dwarfs: Wolf 1069 b* ([arXiv:2301.02477](https://arxiv.org/abs/2301.02477)).
  Sister-system analog; useful for cross-checking USP rocky planet
  scenarios.

### Read (instrument / non-cfg-decisive)

- (none; the deep_read set is small for d).

### Not read — no arXiv preprint or low-priority (~10 papers)

- Mostly Wolf 1069 b and TOI-2095 sister-system papers from the
  expanded bibliography; preserved in
  `docs/phase3/_bib/proxima-cen-d.yaml` with `status: skipped`.

## Open items for follow-up

- **Direct radius measurement**: SM25 confirms no transit detection
  in the current monitoring envelope. A future direct-imaging or
  high-precision astrometric campaign could yield true mass + radius
  (currently only Msini is constrained). The cfg `radius_rearth = 0.65`
  is a placeholder tie-break.
- **Composition by mass–radius relation**: with only Msini, the
  composition (rocky vs. ice-rich) is unconstrained. The cfg
  defaults to a rocky Earth-analog density (5.2 g/cc); a confirmed
  smaller radius would push toward higher density (Mercury-like
  iron-enriched).
- **Volatile cold-trap signature**: the antistellar cold-trap could
  retain water ice and other volatiles delivered by cometary
  flux. A future cfg variant could add a small `subsurface_ice`
  patch at the antistellar pole.
- **Stellar wind sputtering yield**: the cfg adopts a Mercury-analog
  Na exosphere as a tie-break, but no direct modeling exists for
  Proxima d's stellar wind environment. A future Garraffo-style
  3D MHD wind simulation tailored to d could refine the exosphere
  column density and species composition.
- **Superflare albedo modulation**: the cfg currently encodes only
  the time-averaged Bond albedo. The ~3-superflare-per-year cadence
  (Vida 2019) produces transient albedo enhancements during XUV-bright phases.

## Related

- [proxima-cen](proxima-cen.md) — host star; flare environment drives the atmosphere-stripped scenario
- [proxima-cen-b](proxima-cen-b.md) — outer sibling at HZ; contrast — d sits inside the inner edge of any HZ interpretation at ~1.9× Earth's insolation
- [methodology](../reference/methodology.md) — Decisions schema
- [mod-reference](../reference/mod-reference.md) — downstream mods
