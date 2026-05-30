<!-- 55 Cnc e Phase 3 synthesis: cfg-ready decisions and reasoning -->
# 55 Cnc e — Phase 3 Synthesis

55 Cnc e is a 1.88 R⊕, 8.0 M⊕ ultra-short-period (USP) super-Earth on
a 0.737-day (17.7 h) orbit around the bright K0 IV-V star 55 Cnc A, at
a semi-major axis of just 0.0154 AU. It receives ~2450× Earth's
insolation, giving an equilibrium temperature T_eq(A=0) ≈ 1959 K
(derived from the host L = 0.582 L☉ via T_eq = 278.3·L^0.25/√a). It
transits — the brightest star known to host a transiting planet —
which fixes its radius (Bourrier 2018 HST/STIS: 1.88 ± 0.03 R⊕ over
530–750 nm) and, with the RV mass (8.0 ± 0.3 M⊕), its bulk density
(6.7 ± 0.4 g/cc, consistent with a rocky / silicate composition with
at most a thin volatile envelope). Spitzer 4.5 μm dayside thermal
emission is strongly **variable** — Demory 2016 measured the dayside
brightness temperature swinging between ~1365 K and ~2528 K over a
single year (4σ), with the full range spanning ~1300–2800 K. JWST
MIRI/NIRCam secondary-eclipse observations (Hu et al. 2024, Nature)
favor a volatile-rich **outgassed secondary atmosphere** (CO/CO₂)
over a bare lava surface or a primordial envelope.

**Scenario choice for NearStars: a glowing lava super-Earth with a
molten dayside (~2000–2700 K) radiating in the visible, an outgassed
secondary atmosphere of CO₂/CO sourced from the magma ocean, and a
dramatic day-night terminator separating the incandescent dayside from
a much darker, partly-solidified nightside.** This matches the
Hu 2024 outgassed-atmosphere interpretation and the Demory 2016
magma-ocean / volcanic-variability hint; the bare-airless-rock
alternative is preserved as a cfg variant.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 0.737 d orbit, tidal damping at 0.0154 AU; circularized (Bourrier 2018) |
| `obliquity_deg` | 0 | high | tidal damping; circularized orbit |
| `eccentricity` | 0.05 | medium | Bourrier 2018 (consistent with 0 at 2σ; 3σ upper limit 0.19, Demory 2016) |
| `argument_of_periastron_deg` | 86 | low | Bourrier 2018 (low ecc → weak constraint) |
| `sidereal_period_days` | 0.7365474 | high | Bourrier 2018 transit ephemeris |
| `semi_major_axis_au` | 0.0154 | high | Bourrier 2018 |
| `inclination_deg` | 83.59 | high | Bourrier 2018 transit fit |
| `mass_mearth` | 8.0 | high | Bourrier 2018 — RV (Phase 2 recommended; 7.99 ± 0.32; Moutou 2025 Msini 9.35) |
| `radius_rearth` | 1.88 | high | Bourrier 2018 — HST/STIS optical transit, 530–750 nm (Phase 2 recommended) |
| `surface_gravity_g_earth` | 2.26 | high | derived = 8.0 / 1.88² |
| `density_g_cc` | 6.7 | high | Bourrier 2018 — from M, R (rocky/silicate; derived 6.63 agrees) |
| `insolation_s_earth` | 2454 | high | derived = L / a² = 0.582 / 0.0154² |
| `equilibrium_temp_k` (A=0) | 1959 | high | derived: 278.3·0.582^0.25/√0.0154 (TEPCat lists 2349 K with different albedo/redistribution assumptions) |
| `equilibrium_temp_k` (A=0.3) | 1792 | high | derived, Earth-analog albedo |
| `dayside_brightness_temp_k_min` | 1365 | high | Demory 2016 — Spitzer 4.5 μm season minimum (1365 +219/−257 K) |
| `dayside_brightness_temp_k_max` | 2528 | high | Demory 2016 — Spitzer 4.5 μm season maximum (2528 +224/−229 K); full toy-model range ~1273–2816 K |
| `bond_albedo` | 0.1 | medium | low albedo for a molten/dark silicate dayside; within the Demory 2016 emission constraints |
| `atmosphere_present` | true | medium | Hu 2024 — JWST favors a volatile (CO/CO₂) secondary atmosphere over bare rock; Bourrier 2018 interior fit also favors a "heavyweight" few-percent-radius envelope |
| `atmosphere_surface_pressure_pa` | 100000 | low | Tie-break: ~1 bar order-of-magnitude outgassed secondary atmosphere; not directly measured. No H/He (lost in ~80 000 yr; Bourrier 2018), no extended H₂O/H exosphere (Ehrenreich 2012, Esteves 2017) |
| `atmosphere_composition` | CO₂ + CO (outgassed from magma ocean), high mean molecular weight | medium | Hu 2024 — JWST emission favors CO/CO₂; Bourrier 2018 dry-scenario μ = 13.5 +17.9/−7.7 g/mol |
| `atmosphere_scale_height_km` | ~25 | low | derived from T~2000 K, μ~20 g/mol, g = 2.26 g⊕ (high-T inflates scale height; Demory 2016) |
| `atmosphere_tint_rgb_hex` | `#d9c4a0` (hazy warm-grey CO₂/silicate-vapor limb) | low | Tie-break: silicate-vapor + CO₂ outgassed haze; thin and warm-toned |
| `cloud_cover_fraction` | 0.3 | low | Tie-break: silicate/metal-vapor clouds possible on the cooler terminator; Madhusudhan 2015 notes clouds less likely on the hottest daysides |
| `cloud_morphology` | patchy silicate / metal-oxide clouds condensing near the terminator and on the nightside | low | Tie-break: high-T condensate physics; clouds suppressed over the molten substellar point |
| `cloud_tint_rgb_hex` | `#b0a088` (silicate/forsterite grey) | low | Tie-break: enstatite/forsterite condensate grey |
| `dayside_surface_temp_k` | 2400 | high | Demory 2016 — T_eq ~2400 K cited; magma-ocean dayside; matches the variable brightness-temp envelope |
| `substellar_peak_temp_k` | 2700 | medium | derived bare-rock subsolar peak (A=0.1, no redistribution) ≈ T_eq·(8/3)^0.25; matches Demory 2016 ~2816 K upper bound |
| `nightside_surface_temp_k` | 1300 | medium | Demory 2016 — low end of the brightness-temp range; partial nightside re-radiation / atmosphere transport |
| `surface_tint_rgb_hex_primary` | `#2a1c14` (dark solidified silicate, nightside / cool terminator) | medium | Dark ultramafic / quenched silicate where solidified; Demory 2016 magma-ocean interior |
| `surface_tint_rgb_hex_accent` | `#ff5a18` (glowing magma, substellar dayside) | high | Incandescent ~2400–2700 K silicate melt radiating in the visible-orange; matches Demory 2016 dayside temps |
| `surface_morphology` | molten substellar magma ocean grading to a solidified, fractured nightside crust; possible Io-like volcanic resurfacing | medium | Demory 2016 — variability attributed to large-scale surface/volcanic activity (Io analogy) |
| `surface_ice_caps` | none | high | dayside ~2400 K; no surface volatiles survive |
| `ocean_present` | magma ocean (silicate melt) on the dayside, not water | high | Demory 2016 — molten dayside lithosphere at T ≳ 2000 K |
| `tidal_heating_w_m2` | high (Io-like, exact value unconstrained) | low | Demory 2016 — strong tidal interaction invoked to explain the variability; Bolmont 2013 cited |
| `star_apparent_angular_diameter_deg` | 32.6 | high | derived: 2·R★/a = 2·0.943 R☉ / 0.0154 AU — the star fills ~⅓ of the sky |
| `stellar_illumination_color_temp_k` | 5196 | high | von Braun 2011 stellar Teff |

## Surface synthesis

55 Cnc e is the headline body of the system: a transiting USP
super-Earth whose 0.737-day orbit at 0.0154 AU bathes it in ~2450×
Earth's insolation. The measured bulk density of 6.7 ± 0.4 g/cc
(Bourrier 2018) is consistent with a rocky / silicate-dominated
interior — denser than a pure-water world, lighter than an
iron-rich Mercury-analog — with at most a thin volatile envelope
contributing a few percent of the radius. At T_eq ≈ 1959 K and
substellar peak temperatures reaching ~2700 K, the dayside
lithosphere is at or above the silicate solidus for most plausible
mineral compositions: **the substellar hemisphere is a magma
ocean.**

The cleanest observational anchor is the Demory 2016 Spitzer 4.5 μm
dayside thermal-emission campaign, which detected a 4σ **variability**:
the dayside brightness temperature swung from 1365 +219/−257 K in 2012
to 2528 +224/−229 K in 2013 — a factor-3.7 change in occultation depth
(47 → 176 ppm) over a single year, with a full toy-model envelope of
~1273–2816 K. This variability cannot be explained by stellar spots or
by slow compositional drift; Demory 2016 invokes either large-scale
surface activity (Io-like volcanic resurfacing driven by strong tidal
heating) or episodic circumstellar/circumplanetary material. For
NearStars this motivates a visually dynamic, volcanically resurfaced
dayside rather than a static lava plain.

**Color choice.** The dayside is dominated not by reflectance but by
**thermal emission**: silicate melt at 2400–2700 K radiates strongly
in the visible, peaking in the orange-red. The substellar accent
`#ff5a18` encodes this incandescence — a glowing magma surface, by far
the brightest feature on the planet. Where the surface has solidified
(the cooler terminator and nightside), the quenched ultramafic crust
is very dark, `#2a1c14`. The contrast between the glowing day and the
dark night is the planet's defining visual signature. The host star's
warm 5196 K K0 light is far less important here than the planet's own
glow on the dayside.

**Morphology.** Three contributing processes: (1) a substellar magma
ocean, convecting and possibly draining toward the terminator where it
quenches; (2) Io-like volcanic resurfacing driven by tidal heating
(Demory 2016) — episodic plumes and lava flows that produce the
observed brightness variability; (3) a solidified, fractured nightside
crust where re-radiated heat and any atmospheric transport keep
temperatures near ~1300 K. The default texture: a glowing orange
substellar lava pool grading through a narrow incandescent terminator
into a dark, cracked basaltic nightside.

## Atmosphere synthesis

The atmospheric nature of 55 Cnc e has been debated for over a decade,
and the JWST era has tilted the evidence toward an **outgassed
secondary atmosphere**. Bourrier 2018's interior modeling, combining
the 8.0 M⊕ mass and 1.88 R⊕ optical radius, favors a "heavyweight"
atmosphere contributing a few percent of the planet radius; a
primordial H/He envelope is excluded because it would be lost within
~80 000 years (and no hydrogen exosphere is detected; Ehrenreich 2012),
and an extended water-rich envelope is disfavored (Esteves 2017). The
dry-scenario mean molecular weight is high, μ = 13.5 +17.9/−7.7 g/mol.
Hu et al. 2024 (JWST MIRI/NIRCam secondary eclipse) found the emission
spectrum favors a volatile-rich atmosphere with **CO and CO₂** over
both a bare lava surface and a primordial envelope — an atmosphere
outgassed from the underlying magma ocean.

- **Pressure.** The cfg adopts ~1 bar (100 000 Pa) as an
  order-of-magnitude outgassed-atmosphere choice (Confidence=low —
  the absolute surface pressure is not directly measured). This is a
  tie-break: a thin, high-mean-molecular-weight CO₂/CO envelope in
  vapor-pressure equilibrium with the magma ocean, not a thick
  greenhouse.
- **Composition.** CO₂ + CO dominant (Hu 2024), with silicate-vapor
  species (SiO, Na, etc.) near the molten substellar point. High mean
  molecular weight (Bourrier 2018), consistent with no H/He and no
  extended water.
- **Sky appearance.** From the dayside surface, the sky would be a
  hazy, warm-toned veil of CO₂/silicate vapor (`#d9c4a0` limb tint),
  thin enough that the enormous host star dominates. Silicate/metal-oxide
  clouds (forsterite/enstatite grey, `#b0a088`) may condense near the
  cooler terminator and over the nightside, but are suppressed over
  the incandescent substellar magma where temperatures are too high
  for condensation (Madhusudhan 2015).

The variability (Demory 2016) plausibly reflects episodic injection of
silicate dust or volcanic opacity into this atmosphere — tens of scale
heights of optically thick material absorbing in the 4.5 μm band — so
the atmosphere is best rendered as dynamic and patchy rather than
uniform.

## Rotation & spin synthesis

At 0.0154 AU with a 0.737-day orbit, 55 Cnc e is firmly tidally locked
in a 1:1 spin-orbit resonance. The orbit is essentially circularized
(e = 0.05, consistent with 0 at 2σ; Bourrier 2018), which per the
Vinson 2017 / Makarov 2018 criterion (3:2 stable only for e ≳ 0.01,
1:1 favored below) puts e in the synchronous-rotation regime. Obliquity
is damped to zero. The substellar point is therefore fixed in the
surface frame — the magma ocean is permanently anchored under the star.

**KSP implementation note.** Rotation period = orbital period =
0.7365474 days (63 638 s). In Kopernicus the body's `rotationPeriod`
should equal the orbital `period` in seconds.

**No seasons.** With obliquity = 0 and near-zero eccentricity-driven
libration, there are no seasonal cycles; the only temporal variation
is the (real, observed) episodic volcanic/atmospheric variability of
Demory 2016, which the cfg can render as slow brightness flickering of
the substellar region on multi-year timescales.

## Visual styling

Combining the surface and atmosphere decisions:

- **Global appearance (orbit view).** A small, intensely glowing world
  hugging its star — the dayside an orange-incandescent magma hemisphere
  (`#ff5a18`), the nightside a dark fractured crust (`#2a1c14`), with a
  sharp, dramatic day-night terminator between them.
- **Dayside.** A molten substellar magma ocean radiating in the
  orange-red (~2400–2700 K). The substellar PQS/emissive map should
  peak at `#ff5a18`–`#ff8030` within ~30° of the substellar point,
  fading outward as the surface cools toward the terminator. This is
  the brightest single surface feature in the inner 55 Cnc system.
- **Terminator band.** Narrow and dramatic — the incandescent dayside
  drops sharply to the dark nightside over a thin band where the magma
  quenches and silicate clouds condense. High visual contrast; the
  signature look of the planet.
- **Nightside.** Much darker (~1300 K) — dark basaltic crust with only
  faint residual thermal-IR glow and occasional volcanic hotspots
  (Io-like, per Demory 2016). Not fully black like an airless rock,
  because re-radiation and atmospheric transport keep it warm.
- **Atmosphere haze.** A thin, hazy warm-grey CO₂/silicate-vapor veil
  (`#d9c4a0` limb), with patchy silicate/metal-oxide clouds (`#b0a088`)
  near the terminator and nightside. The limb shows a faint glowing rim
  where the hot dayside atmosphere catches the line of sight.
- **Star in sky.** 55 Cnc A is enormous: 32.6° angular diameter — the
  star fills roughly a third of the sky, a vast warm-orange (5196 K)
  dome rather than a point. Its surface brightness dominates everything;
  the dayside is in perpetual blinding daylight.
- **Sister planets in sky.** Planet b (next out at 0.118 AU) appears as
  a bright warm point; at conjunction it subtends only a small angle.
  None of the sibling planets rivals the host star's dominance.
- **Volcanic flicker (optional, faithful).** Per Demory 2016's
  observed factor-3.7 variability, the substellar glow can be animated
  to brighten and dim on multi-year timescales, with occasional
  Io-like plume/lava-flow events — a distinctive and physically
  motivated visual touch.

## Canonical alternatives

The atmosphere of 55 Cnc e is the one place where the cfg makes a
documented choice between two literature-supported readings. The cfg
adopts the **outgassed-secondary-atmosphere** scenario (Hu 2024) as
default but preserves the bare-lava-rock alternative.

### Diverged cfg picks

| Field | Gameplay (in cfg) | Canonical alternative | Why diverged |
|---|---|---|---|
| `atmosphere_present` / `atmosphere_surface_pressure_pa` | true / 100000 Pa (CO₂/CO outgassed secondary atmosphere, Hu 2024) | false / 0 Pa (bare lava surface with no atmosphere; the older Demory 2016a "no-atmosphere magmatic surface" reading and the long-standing airless-USP prior) | Both are within the observation window: the JWST emission spectrum (Hu 2024) favors a volatile atmosphere, but a bare incandescent lava surface remains a viable interpretation and is the default expectation for most USP planets. The cfg picks the atmosphere because the outgassed CO₂/CO veil + silicate clouds give a richer, more distinctive render (haze, terminator clouds, limb glow) than a bare rock, and because Hu 2024 is the most recent direct constraint. The airless-lava variant is preserved in Open items. |

## Bibliography

### Read (visual-informative, drove decisions above)

- **Bourrier V. et al. 2018** — *The 55 Cnc system reassessed*, A&A
  619, A1 (`2018A&A...619A...1B`, arXiv:1807.04301). Planet e
  mass 8.0 ± 0.3 M⊕, HST/STIS optical radius 1.88 ± 0.03 R⊕, density
  6.7 ± 0.4 g/cc; interior model favors a heavyweight few-percent-radius
  atmosphere, rules out H/He (lost in ~80 000 yr) and extended water.
  **Phase 2 anchor for orbit / mass / radius / density.**
- **Demory B.-O. et al. 2016** — *Variability in the super-Earth
  55 Cnc e*, Nature 532, 207 (`2016Natur.532..207D`,
  arXiv:1505.00269). Spitzer 4.5 μm dayside brightness temperature
  variable from 1365 to 2528 K over a year (4σ; full range ~1273–2816 K);
  T_eq ~2400 K; attributes variability to Io-like surface/volcanic
  activity or circumstellar material. **The anchor for the dayside
  temperatures, magma-ocean surface, and the volcanic-variability
  visual.**
- **Hu R. et al. 2024** — *A secondary atmosphere on the rocky exoplanet
  55 Cnc e*, Nature 630, 609 (`2024Natur.630..609H`; no arXiv preprint —
  read via the Nature abstract / Phase 2 bib annotation). JWST
  MIRI/NIRCam secondary eclipse favors a volatile (CO/CO₂) outgassed
  secondary atmosphere over a bare lava surface or a primordial
  envelope. **Drives the atmosphere-present decision.** Tier-A manual
  followup — re-verify the exact CO/CO₂ mixing ratios when the full
  text is pasted.

### Read (context / methodology, not decision-driving)

- **von Braun K. et al. 2011** — `2011ApJ...740...49V`,
  arXiv:1107.1936. Stellar R/Teff/L anchor → the L = 0.582 L☉ used in
  the T_eq derivation; model-independent super-Earth diameter ~2.1 R⊕
  (superseded by Bourrier 2018's STIS 1.88 R⊕).
- **Madhusudhan N. & Redfield S. 2015** — clouds less likely on the
  hottest exoplanet daysides; informs the suppressed-substellar-cloud
  choice.

### Read (instrument-only, not visual-informative)

- **Ehrenreich D. et al. 2012** — no hydrogen exosphere detected on
  55 Cnc e; rules out a primordial H envelope.
- **Esteves L. et al. 2017** — no extended water-rich atmosphere;
  disfavors the wet-envelope scenario.

### Not read — no arXiv preprint or low-priority (~20 papers)

Early radius/phase-curve papers (Winn 2011, Gillon 2012, Dragomir 2014),
the disintegrating-exomercury comparison literature, and JWST
follow-up conference proceedings. The full filtered bib is preserved
in `docs/phase3/_bib/55-cnc.yaml`.

## Open items for follow-up

- **Hu 2024 full text.** The CO/CO₂ atmosphere decision rests on the
  Nature abstract; when the full text is pasted, re-verify the exact
  composition, mixing ratios, and dayside temperature retrieval, and
  refine `atmosphere_composition` / `atmosphere_surface_pressure_pa`
  from tie-break toward measured.
- **Airless-lava cfg variant.** Preserved per the Canonical
  alternatives: a bare incandescent lava surface with
  `atmosphere_present = false`, no haze, sharper limb, and a fully
  thermal-emission dayside. Ship as an alternate cfg.
- **Variability animation.** Demory 2016's factor-3.7 dayside
  variability is real and unique among super-Earths; a cfg that
  animates the substellar brightness on multi-year timescales (with
  occasional volcanic plume/lava events) would be the most faithful
  rendering. Refine the timescale if longer-baseline JWST monitoring
  publishes a period.
- **Refine albedo / temperatures.** The Bond albedo (0.1) and
  nightside temperature (1300 K) are medium/low confidence; a JWST
  phase curve (analogous to the TRAPPIST-1 b/c thermal phase curves)
  would pin the redistribution and tighten these.

## Related

- [55-cnc](55-cnc.md) — host star (K0 IV-V, L = 0.582 L☉) supplying the insolation and T_eq derivation
- [55-cnc-b](55-cnc-b.md) — next planet out (hot Jupiter at 0.118 AU), the brightest sibling in e's sky
- [trappist-1-b](trappist-1-b.md) — comparison hot rocky world (airless bare-rock interpretation contrasts with e's outgassed-atmosphere choice)
- [methodology](../reference/methodology.md) — Decisions schema and confidence tags
- [mod-reference](../reference/mod-reference.md) — downstream KSP mods consuming these values (emissive dayside, atmosphere haze)
