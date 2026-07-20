<!-- Teegarden's Star c Phase 3 synthesis: cfg-ready decisions and reasoning -->
# Teegarden's Star c — Phase 3 Synthesis

Teegarden's Star c is a 1.05 M⊕ minimum-mass rocky planet on an
11.416-day orbit around the M7.0 V host, with semi-major axis 0.0455
AU and insolation 0.35 ± 0.02 S⊕ (Dreizler 2024). Equilibrium
temperature with Bond albedo 0.3 is 209 ± 4 K — 64 K below the freezing
point of water. The Earth Similarity Index, which uses a simple bulk-
parameter weighting, comes out high (ESI = 0.88, "closely resembling
Proxima b" per Dreizler 2024), but that is misleading: c sits at or
beyond the outer edge of the conservative habitable zone, and the most
recent dedicated 3D GCM study finds it locked in a global snowball
state for every atmospheric composition tested. The cfg therefore
renders c as a **cold, globally ice-covered world** — not as a
temperate Earth-analog.

The defining cfg-relevant result for c comes from Hammond 2025
([arXiv:2504.00978](https://arxiv.org/abs/2504.00978)), which runs an ExoCAM GCM suite over seven nearby
HZ targets including Teegarden c, with pCO₂ varied from 100 μbar to 2
bar. Of the seven targets, c is the **only one** that fails to support
liquid water anywhere on its surface even at the maximum 2-bar CO₂
greenhouse — the paper states explicitly that c "has a fully
ice-covered surface even at a CO₂ partial pressure of 2 bar." The
combination of low insolation (S = 0.37 in Hammond's parameter set),
high ice albedo feedback, and the M-dwarf SED's limited shortwave
heating efficiency drives c firmly into snowball regardless of how
much greenhouse gas is loaded.

Wandel 2019's older 1D analytic model gave a more optimistic
habitability range (H_atm = 1–12 at f = 0.5, with a narrow habitable
patch at the substellar point for H_atm = 1), but that model is
parametric in atmospheric heating and lacks ice-albedo feedback and
3D heat redistribution physics. The Hammond 2025 3D GCM is the more
recent, planet-specific, higher-weight reading; the cfg follows it.
Because the cfg's snowball pick *agrees with* the canonical reading
(it does not diverge from it), no Canonical-alternatives divergence is
required; the optimistic Wandel reading is preserved as a cfg variant
under Open items.

**Scenario choice for NearStars: globally ice-covered "snowball"
planet with a ~1 bar N₂ + 0.1 bar CO₂ atmosphere, tidally locked,
surface temperature below 273 K everywhere, no liquid water,
atmospheric circulation dominated by an equatorial superrotating jet.**
The cfg is structurally distinct from b's eyeball aquaplanet and from
d's bare rock — c is the system's archetypal snowball.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | Wandel 2019; Hammond 2025 GCM assumes 1:1 |
| `obliquity_deg` | 0 | high | tidal damping |
| `eccentricity` | 0.04 | high | Dreizler 2024 Table 4 (0.04 +0.07/−0.03) |
| `argument_of_periastron_deg` | 301 | low | Dreizler 2024 Table 4 (poorly constrained at low e: +165/−74) |
| `sidereal_period_days` | 11.416 | high | Dreizler 2024 Table 4 |
| `semi_major_axis_au` | 0.0455 | high | Dreizler 2024 Table 4 |
| `mass_mearth` | 1.05 (msini) | high | Dreizler 2024 Table 4 |
| `radius_rearth` | 1.02 | medium | DB (Earth-like MR); Hammond 2025 Table 1 uses 1.05 (Zeng-class) |
| `surface_gravity_g_earth` | 1.01 | medium | derived = 1.05 / 1.02² = 1.01 |
| `density_g_cc` | 5.45 | low | derived = 5.513 × 1.05 / 1.02³ = 5.45 (Earth-like assumption; no transit) |
| `insolation_s_earth` | 0.35 | high | Dreizler 2024 Table 4 (Hammond 2025 uses 0.37 with slightly different stellar params) |
| `equilibrium_temp_k` (A=0.3) | 209 | high | Dreizler 2024 Table 4 (load-bearing; not a bare-formula recompute) |
| `bond_albedo` | 0.55 | medium | Hammond 2025 — high ice albedo dominates the snowball regime (value inferred from ice-covered state, not a quoted figure) |
| `surface_temp_substellar_k` | 230 | medium | Hammond 2025 Fig. 1 — warmest dayside spot still below freezing at 2 bar CO₂ (read from map; not a quoted number) |
| `surface_temp_nightside_k` | 170 | medium | Hammond 2025 Fig. 1 — nightside cold-trap (read from map; not a quoted number) |
| `surface_temp_global_mean_k` | 200 | medium | Hammond 2025 — sub-freezing everywhere for all pCO₂ (text-stated; specific mean read from map) |
| `atmosphere_present` | true | high | Wandel 2019; Hammond 2025 — all 0.1–2 bar CO₂ cases sustain a stable climate |
| `atmosphere_surface_pressure_pa` | 110 000 | medium | Tie-break: Hammond 2025 0.1 bar CO₂ + 1 bar N₂ case (warm-edge snowball); even the 2 bar CO₂ case stays ice-covered |
| `atmosphere_composition` | N₂ ~91%, CO₂ ~9% (0.1 bar CO₂ over 1 bar N₂), trace H₂O, Ar | medium | Tie-break: adopts Hammond 2025's 0.1 bar CO₂ / 1 bar N₂ scenario (its 2 bar case is pure CO₂, 0 N₂) |
| `atmosphere_scale_height_km` | 5.8 | medium | derived: kT/μg with T=200 K, μ=29, g=9.86 m/s² |
| `atmosphere_tint_rgb_hex` | `#4a3a50` (thin Rayleigh + cold-sky dim violet) | low | Tie-break: Rayleigh under 2904 K + low pressure — dimmer than b's expected tone |
| `cloud_cover_fraction` | 0.35 | medium | Hammond 2025 — c is the cloud-water-path outlier (least cloud cover of the seven; lowest atmospheric water vapor because the surface is ice-covered) |
| `cloud_morphology` | Sparse clouds advected eastward of the substellar point by the superrotating jet; possible CO₂-ice clouds at the nightside cold-trap | medium | Hammond 2025 — cloud maximum sits east of substellar; c's total cloud water path is much smaller than the other six targets |
| `cloud_tint_rgb_hex` | `#a09080` (dim warm cream — very low moisture) | low | Tie-break: ice clouds + M7 V illumination |
| `ocean_present` | false | high | Hammond 2025 — ice everywhere even at 2 bar CO₂ |
| `surface_morphology` | Global ice sheet ~50–300 m thick over frozen ocean substrate; hummocky terrain at convergence zones; rare exposed dark bedrock at low-latitude impact craters or volcanic vents | medium | Snowball-Earth analog physics; no Teegarden-c-specific GCM surface-topology paper |
| `surface_tint_rgb_hex_primary` | `#d8d0c4` (ice surface under M-dwarf light) | low | Tie-break: water-ice albedo 0.6–0.8 + 2904 K illumination |
| `surface_tint_rgb_hex_accent` | `#4a3030` (exposed mafic bedrock at impact craters and volcanic features) | low | Tie-break: sparse exposure of darker sub-ice terrain |
| `magnetic_field_present` | true (modest) | low | Tie-break: Earth-mass active interior; no measurement |
| `magnetic_field_strength_microtesla_equator` | 20 | low | Tie-break: scaled to a low Earth-analog field; no measurement |
| `aurora_present` | true (weak) | low | Atm + B-field both modest; M-dwarf SEP environment |
| `aurora_color_primary_hex` | `#4DFF4D` | low | Tie-break: [OI] 557.7 nm — but very weak; CO₂⁺ accent `#FF4D4D` may dominate in CO₂-rich atm |
| `aurora_intensity_kR_typical` | 15 | low | Tie-break: weak — quiet M7 V flux side + thin atmosphere couples little SEP energy |
| `surface_radiation_dose_msv_yr` | 50 | low | Tie-break: low M7 V flare rate + Earth-like B-field + ~1 bar atmosphere |
| `star_apparent_angular_diameter_deg` | 1.25 | high | derived: 2 × 0.107 × 0.00465 / 0.0455 × 57.3 = 1.25° |
| `stellar_illumination_color_temp_k` | 2904 | high | Schweitzer 2019 (host Teff 2904 K; high-res spectroscopy) |

## Surface synthesis

Teegarden c sits at S = 0.35 S⊕ — about a third of Earth's insolation
and at or below the conservative outer-HZ limit (Kopparapu 2013
S_outer ≈ 0.36 for an M dwarf with full atmospheric circulation). The
cfg's snowball pick rests on Hammond 2025 ([arXiv:2504.00978](https://arxiv.org/abs/2504.00978)), the most
recent dedicated 3D GCM study of c.

Hammond's ExoCAM grid runs c at three CO₂ scenarios — 100 μbar CO₂
over 1 bar N₂, 0.1 bar CO₂ over 1 bar N₂, and 2 bar CO₂ with no N₂
background — and finds c ice-covered in all three. The paper states
plainly that "all planet cases except Teegarden's Star c have some
habitable surface area with temperatures above the freezing point of
water, while Teegarden's Star c is ice-covered for all pCO₂ values
considered," and that c "has a fully ice-covered surface even at a CO₂
partial pressure of 2 bar." The qualitative picture across the three
cases (warming with increasing pCO₂ but never crossing the freezing
point) is:

- **100 μbar CO₂**: the coldest case; surface temperatures fall to the
  nightside cold-trap minimum and the thin CO₂ reservoir is most
  vulnerable to freeze-out.
- **0.1 bar CO₂**: stable, warmer, but still ice-covered — adopted as
  the cfg's "warm-edge snowball."
- **2 bar CO₂**: the warmest case; the dayside warms but stays below
  freezing — the maximum greenhouse warming in the simulation does not
  lift the surface above the freezing point anywhere.

(Per-cell temperatures above are read from the surface-temperature
maps in the paper's Figure 1, not quoted numbers; the cached text does
not reproduce the Appendix A global-mean table, so the specific
substellar/nightside values in the Decisions table are figure-level
estimates with medium confidence.)

The reason c stays frozen even at extreme greenhouse loading is the
combination of low instellation (only 0.35 S⊕) and a high ice albedo
that the M-dwarf SED struggles to overcome. Late-M illumination peaks
in the near-IR, where water ice has surprisingly high absorptivity
(unlike at visible wavelengths where ice albedo is 0.7–0.9), but the
substellar dayside still requires the bulk of incident flux to be at
shorter wavelengths to break out of the ice-albedo feedback loop —
exactly what an M7 V host fails to provide.

The cfg therefore renders c as a **uniform ice-covered surface** with:

- **Substellar dayside**: warmest ice (~230 K at high pCO₂). Ice may be
  thin enough to be photically transparent in rare cases, but no melt
  pools form. Surface morphology is hummocky, with pressure ridges
  where atmospheric circulation drives ice convergence.
- **Mid-latitudes / longitudes**: glacial ice sheet ~50–300 m thick
  over the frozen ocean substrate (if any subsurface water exists from
  primordial accretion).
- **Nightside**: permanent CO₂-frost cold-trap (~170 K), possibly with
  CO₂ ice deposition reducing atmospheric pressure locally — a
  Martian-style polar-CO₂-frost analog but over the entire nightside
  hemisphere.

**Colour choice.** The surface is overwhelmingly water-ice with an
M-dwarf-illumination-shifted warm cream `#d8d0c4`. The accent `#4a3030`
(dark mafic bedrock) appears at sparse impact craters where ejecta has
temporarily exposed sub-ice material — these would be the most visually
distinctive features for a player flying over the surface.

## Atmosphere synthesis

The cfg adopts Hammond 2025's **0.1 bar CO₂ over 1 bar N₂** scenario
(~1.1 bar total, ~9% CO₂ by partial pressure) — the warm-edge member
of the snowball regime. It is the warmest of Hammond's two
N₂-background cases but explicitly does not lift the surface above
freezing. The composition is:

- **Pressure** ~1.1 bar (110 kPa) — 0.1 bar CO₂ on a 1 bar N₂
  background, per Hammond 2025's intermediate case.
- **Composition** N₂ ~91%, CO₂ ~9% (0.1 bar), H₂O trace (saturated at
  ~6×10⁻⁵ at 200 K), with minor Ar. Note that Hammond's *thickest*
  case is pure 2 bar CO₂ with no N₂; the cfg deliberately picks the
  N₂-background intermediate case rather than the pure-CO₂ end-member.
- **Clouds.** Hammond 2025 finds c to be the cloud-water-path outlier
  of the seven targets — the ice-covered surface keeps total
  atmospheric water vapor far below the other six. What little cloud
  forms is advected eastward of the substellar point by the
  superrotating jet (the general pattern Hammond reports for the
  low-pCO₂ cases), not concentrated at the terminator. Total cloud
  cover is therefore low (~35%). CO₂-ice clouds may form on the
  nightside if surface temperatures drop below the CO₂ frost point.

**Sky appearance.** The atmosphere has Rayleigh scattering at short
wavelengths, but with the 2904 K stellar SED there is very little
short-wavelength flux — the scattered sky is dim and shifted toward
red. Zenith sky `#3a2a35`, horizon `#7a5040`.

The host star angular size is 1.25° (about 2.3× the Sun's angular
size from Earth). Surface illumination at substellar is 0.35 ×
Earth's bolometric flux — comparable to twilight on Earth, with the
spectral peak firmly in the near-IR. Most of the incident energy is
absorbed by water-ice with high near-IR absorptivity, but most of the
upwelling thermal emission radiates back to space because the
atmosphere is optically thin in the 8–13 μm window.

**Atmospheric escape and stability.** The 7–8 Gyr old quiet host star
favors atmospheric retention as long as the planet built and kept a
secondary CO₂/N₂ atmosphere via outgassing. Hammond 2025 does not
include escape; Wandel 2019 reviewed retention and found old quiet
M dwarfs less hostile than younger active ones. The CO₂–N₂ atmosphere
is heavier than the H₂/He primordial atmosphere typical of pre-MS
escape and is less susceptible to thermal escape.

**Auroras.** Weak (15 kR typical — much fainter than a thick-atmosphere
HZ world). The low flare frequency at Teegarden combined with the
modest atmosphere produces a sparse auroral display. Visible emission
is dominated by [OI] 557.7 nm green (`#4DFF4D`) where O is present from
minor CO₂ photolysis, with a CO₂⁺ red-orange accent (`#FF4D4D`) in the
580–700 nm Fox-Duffendack-Barker bands becoming significant if the CO₂
fraction is high.

## Rotation & spin synthesis

c at P_orb = 11.4 d is firmly inside the tidal-locking timescale
(Griessmeier 2009) over 7–8 Gyr; the cfg assumes synchronous rotation,
consistent with the 1:1 spin-orbit state Hammond 2025 adopts for its
GCM and with Wandel 2019's locked-planet treatment. Obliquity damped
to zero. Eccentricity is 0.04 (Dreizler 2024, +0.07/−0.03) — low and
consistent with near-circular, so the cfg renders the spin as near-1:1
/ pseudo-synchronous rather than a captured 3:2 resonance.

**KSP implementation note.** Rotation period = orbital period =
11.416 days (986 342 s).

**Atmospheric circulation.** Hammond 2025 finds that all of its seven
tidally-locked cases (including c) develop an equatorial superrotating
jet (their Figure 3, zonal-mean zonal wind). Surface flow is weaker.
This is canonical for slowly-rotating tidally-locked planets and
matches the "thermal superrotation" regime (Pierrehumbert & Hammond
2019), which Hammond cites. c is in the Rhines-rotator dynamical
regime in Hammond's classification.

**No seasons.** Obliquity = 0; libration amplitude small.

**Magnetic dynamo.** Earth-mass c likely supports a modest dynamo from
core convection. The cfg picks a low Earth-analog field (20 μT) as a
tie-break. No measurement.

## Visual styling

Combining surface and atmosphere decisions, c renders as a uniform
white-cream snowball world:

- **Global appearance from orbit.** A nearly featureless ice sphere
  with subtle variations in surface roughness. Terminator features
  (pressure ridges, glacial flow lines) become visible only at
  oblique illumination. The thin atmosphere produces almost no limb
  haze.
- **Substellar zone**: slightly warmer ice (~230 K), possibly with
  rare thin transparent ice patches. Surface morphology shows
  convergence-driven pressure ridges where the superrotating jet
  drives ice convergence.
- **Mid-latitudes**: uniform glacial sheet, smooth on large scales,
  with occasional impact craters exposing dark `#4a3030` bedrock at
  the impact center.
- **Nightside**: dark, possibly with bright patches of CO₂-frost
  deposition where surface temperature drops below the CO₂ frost
  point. The cold trap reads as a uniformly dim region.
- **Atmosphere haze.** Very thin pale violet limb glow (`#4a3a50`),
  ~8–12 km thick.
- **Star in sky.** Teegarden's Star subtends 1.25° in c's sky (2.3×
  the Sun from Earth). Appears as a deep red-orange disk; illumination
  feels like deep twilight, never noon.
- **Sister planets in sky.** b (inner, ~4.91 d) and d (outer, ~26 d)
  pass through conjunctions; b is the brighter and closer of the two
  at inferior conjunction.

The overall visual impression should evoke a Hoth-like ice world but
with the perpetual red-orange illumination of an ultra-cool dwarf.
c is visually less striking than b (no ocean-pupil contrast) but
forms a distinct "frozen sibling" companion in the system view.

## Bibliography

### Read (visual-informative, drove decisions above)

- **[2402.00923](https://arxiv.org/abs/2402.00923)** Dreizler S. et al. 2024 — *Teegarden's Star revisited*
  (`2024A&A...684A.117D`). Table 4 refined c orbit
  (P = 11.416 d, e = 0.04, msini = 1.05 M⊕, T_eq = 209 K @ A=0.3,
  S = 0.35 S⊕, ESI = 0.88 "closely resembling Proxima b").
- **[2504.00978](https://arxiv.org/abs/2504.00978)** Hammond T. et al. 2025 — *The climates and thermal
  emission spectra of prime nearby temperate rocky exoplanet targets*
  (`2025ApJ...984..181H`). 3D ExoCAM GCM of c at 100 μbar / 0.1 bar /
  2 bar CO₂ — c is ice-covered everywhere for all pCO₂, the only one
  of seven targets that never reaches liquid water. Driver of the
  cfg's snowball choice.
- **[1906.07704](https://arxiv.org/abs/1906.07704)** Wandel A. & Tal-Or L. 2019 — *On the Habitability of
  Teegarden's Star planets* (`2019ApJ...880L..21W`). 1D analytic
  habitability range H_atm = 1–12 for c (f=0.5, T_max=340 K) — the
  older, more optimistic reading superseded for the cfg by Hammond
  2025.
- **[1906.07196](https://arxiv.org/abs/1906.07196)** Zechmeister M. et al. 2019 — discovery paper for b
  and c (`2019A&A...627A..49Z`). Original orbital parameters and host
  characterization.

### Read (context / methodology, not decision-driving)

- **[2007.15077](https://arxiv.org/abs/2007.15077)** Cifuentes C. et al. 2020 — CARMENES input catalogue
  of M dwarfs (`2020A&A...642A.115C`). M-dwarf Teff/spectral-type
  calibration context (M7.0 V bin); the adopted host Teff of 2904 K
  is from Schweitzer 2019, not this catalogue's bin median.
- **2512.16575** Fujii et al. — climate / habitability methodology
  context for M-dwarf HZ planets.
- **Schweitzer A. et al. 2019** — host stellar parameters (Teff 2904 K,
  L, M, R); used via the host synthesis.

### Read (instrument / non-cfg-decisive)

- General LIFE / MIRECLE mission concept papers (the PIE-detectability
  framing of Hammond 2025).

### Not read — no arXiv preprint or low-priority (~2 papers)

- Hill 2023 catalog (skipped — catalog, not cfg-decisive).
- Bibliography preserved in `docs/phase3/_bib/teegarden-s-star-c.yaml`.

## Open items for follow-up

- **Hammond 2025 vs Wandel 2019 (cfg variant)**: the cfg's snowball
  pick follows Hammond 2025's 3D ExoCAM result. Wandel 2019's older 1D
  analytic model gives a more optimistic H_atm = 1–12 habitability
  range for c, with a narrow habitable patch at the substellar point.
  The conservative-but-interesting **variant** the cfg writer can ship
  instead is a marginal "eyeball with a thin substellar warm spot."
  If a future independent 3D GCM (THAI-style intercomparison, or a
  ROCKE-3D study of c specifically) finds liquid water at substellar
  for high pCO₂, the cfg should shift to that variant. For now,
  snowball is canonical and the cfg agrees with it.
- **Surface temperatures are figure-read, not quoted**: the cached
  Hammond 2025 text does not reproduce the Appendix A global-mean
  table; the substellar/nightside/global-mean K values in the
  Decisions table are estimates read from the Figure 1 maps. Tighten
  these if the numerical table becomes available.
- **2-bar CO₂ end-member**: Hammond 2025 tested up to 2 bar CO₂ (pure,
  no N₂) with no surface melt. A higher CO₂ atmosphere (e.g., 10 bar
  Venus-like) was not tested and could in principle warm the surface
  above freezing — but at that pressure other effects (CO₂
  condensation onto the nightside, atmospheric collapse) become
  important.
- **No transit confirmation**: all parameters RV-derived; the system
  is non-transiting (TESS + SPECULOOS).
- **Subsurface ocean**: Hammond 2025 does not model interior structure.
  If c has a primordial water reservoir, a liquid subsurface ocean
  could exist beneath the global ice sheet (Europa-like). The cfg does
  not render it as visible from orbit but could add a Kerbalism
  subsurface-water flag.
- **Atmospheric escape over 7–8 Gyr**: not modeled. The cfg assumes
  retention based on the quiet present-day star and the old age. A
  Lammer-style escape calculation specifically for c would tighten the
  atmospheric column.

## Related

- [teegardens-star](teegardens-star.md) — M7 V host
- teegardens-star-b — inner sibling, temperate aquaplanet (not yet promoted)
- teegardens-star-d — outer sibling, cold bare-rock (not yet promoted)
- [trappist-1-f](trappist-1-f.md) — sister-system analog at the HZ outer edge (TRAPPIST-1 f sits nearer the snowball/eyeball boundary; c is fully snowball)
- [proxima-cen-b](proxima-cen-b.md) — Dreizler 2024 quotes c's ESI (0.88) as comparable
- [methodology](../reference/methodology.md) — Decisions schema
