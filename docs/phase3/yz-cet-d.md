<!-- YZ Cet d Phase 3 synthesis: cfg-ready decisions and reasoning -->
# YZ Cet d — Phase 3 Synthesis

YZ Cet d is the outermost of three planets around the M4.5 V flare
star YZ Cet, on a 4.65626-day orbit at a = 0.0285 AU (Stock et al.
2020). Like its siblings it is a non-transiting radial-velocity planet:
its minimum mass M sin i = 1.09 ± 0.12 M⊕ (Stock 2020) is measured, but
its radius is **not**, so the 1.03 R⊕ figure in the DB is a
semi-empirical mass-radius estimate, not an observation. With the host's
L = 0.0022 L☉ the equilibrium temperature is T_eq ≈ 357 K at zero
albedo (computed here; T_eq = 278.3·L^0.25/√a), making d the
**coolest of the three warm rocky worlds** — still above Earth at
~2.7× Earth's insolation, but the closest of the trio to temperate.

**Scenario choice for NearStars: a warm, tidally-locked rocky planet
with a thin-to-absent secondary atmosphere — the coolest, outermost
member of the compact system.** Like c, d is not the SPI driver: the
confirmed star-planet magnetic interaction folds to planet b's orbit,
and d shows the worst radio phase agreement of the three (Pineda &
Villadsen 2023; Trigilio 2023). d is rendered as the outermost, coolest
plain rocky world. Surface and atmosphere sit at low confidence because
no transit, eclipse, or transmission spectrum exists.

## Decisions

Kopernicus / atmosphere cfg-ready values. `Confidence`: high =
directly measured or tightly constrained, medium = theoretical with
strong support, low = aesthetic choice within the allowed window.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 4.66 d orbit at 0.0285 AU; tidal locking time ≪ system age for a mid-M host |
| `obliquity_deg` | 0 | high | tidal damping at this orbit |
| `eccentricity` | 0.07 | medium | Stock et al. 2020 (Phase 2 recommended); poorly constrained (σ ≈ 0.05), consistent with near-circular |
| `argument_of_periastron_deg` | 200 | low | Stock et al. 2020 (weak constraint at low ecc) |
| `sidereal_period_days` | 4.65626 | high | Stock et al. 2020 (Phase 2 recommended) |
| `semi_major_axis_au` | 0.02851 | high | Stock et al. 2020 (Phase 2 recommended) |
| `mass_mearth` | ≥ 1.09 ± 0.12 (M sin i) | high | Stock et al. 2020 RV minimum mass (Phase 2 recommended); true mass higher by 1/sin i |
| `radius_rearth` | ~1.03 (ESTIMATE) | low | NOT measured — no transit. Semi-empirical M-R estimate (Stock 2020); Trigilio 2023 cites R_d = 1.04 R⊕ from the same relation |
| `surface_gravity_g_earth` | ~1.03 | low | derived = 1.09 / 1.03² from minimum mass + estimated radius; a lower bound (true mass higher) |
| `density_g_cc` | ~5 (assumed rocky) | low | No measured radius → no measured density; Earth-like rocky composition assumed |
| `insolation_s_earth` | 2.7 | high | derived = L / a² = 0.0022 / 0.02851² |
| `equilibrium_temp_k` (A=0) | 357 | high | derived = 278.3 · L^0.25 / √a (L = 0.0022 L☉, a = 0.02851 AU) |
| `equilibrium_temp_k` (A=0.3) | 327 | high | derived, Earth-analog Bond albedo |
| `bond_albedo` | 0.1 | low | Tie-break: assumed low for a warm rocky surface; no measurement |
| `atmosphere_present` | thin or absent | low | No transmission spectrum; warm rocky RV planet around an active flaring M dwarf — atmosphere retention is marginal. cfg renders a thin atmosphere as the interesting option |
| `atmosphere_surface_pressure_pa` | ~10000 (0.1 bar, tie-break) | low | No measurement; thin secondary atmosphere chosen as more interesting than airless. Airless variant preserved in Open items |
| `atmosphere_composition` | CO₂ / N₂ secondary (assumed) | low | No spectrum; outgassed rocky-planet composition assumed if any atmosphere survives |
| `atmosphere_tint_rgb_hex` | `#bca088` (thin warm haze) | low | Tie-break: faint warm limb haze under 3100 K illumination if a thin atmosphere is present |
| `dayside_surface_temp_k` | ~395 | medium | substellar bare-rock peak above the 357 K global T_eq (A=0, low redistribution) |
| `nightside_surface_temp_k` | depends on atmosphere | low | airless → very cold nightside; thin atmosphere → partial redistribution |
| `surface_tint_rgb_hex_primary` | `#62503f` (warm basaltic rock) | low | Tie-break: warm-toned iron-bearing basalt under red M-dwarf light; lightest of the three, reinforcing the inside-out gradient |
| `surface_tint_rgb_hex_accent` | `#6e3e2a` (oxidized iron patches) | low | Tie-break: photolytic / oxidized iron on an exposed warm rocky surface |
| `surface_morphology` | cratered rocky plains, tidally-locked | low | No data; generic warm rocky morphology under tidal lock |
| `spi_driver` | false | high | Pineda & Villadsen 2023; Trigilio 2023 — the SPI bursts fold to b's orbit, not d's (worst phase agreement of the three); d is not the flux-tube driver |
| `planet_magnetic_field_g` | unconstrained | low | No SPI signal attributable to d → no field inference; left unconstrained |
| `star_apparent_angular_diameter_deg` | 2.94 | high | derived = 2 · R★ / a · (180/π), R★ = 0.1571 R☉ |
| `stellar_illumination_color_temp_k` | 3100 | high | Cifuentes et al. 2020 host Teff |

## Surface synthesis

YZ Cet d has no transit, eclipse, or transmission measurement, so its
surface is inferred entirely from its minimum mass, orbit, and host
illumination. The radius (1.03 R⊕) is a semi-empirical mass-radius
estimate — Trigilio 2023 cite R_d = 1.04 R⊕ from the same Stock 2020
relation. The minimum mass M sin i = 1.09 M⊕ (Stock 2020) is a genuine
lower bound; the true mass is higher by 1/sin i. For cfg purposes d is
treated as an Earth-mass-class rocky planet.

d is the **coolest of the three, but still warm**. The equilibrium
temperature at zero albedo is T_eq ≈ 357 K (computed here from
L = 0.0022 L☉ and a = 0.02851 AU), about 50 K cooler than the middle
planet c and 110 K cooler than the inner planet b, at ~2.7× Earth's
insolation. This is the closest of the trio to temperate, though still
above the boiling point of water at 1 bar — a warm rocky world, not a
habitable-zone analog. The substellar bare-rock peak is ~395 K.

**Color choice.** Under the host's 3100 K red-orange illumination, d is
rendered as a warm iron-bearing basaltic surface (`#62503f` primary)
with oxidized iron-patch accents (`#6e3e2a`) — the lightest of the
three planet tints, completing the inside-out warm-to-cooler gradient
(b darkest/warmest, d lightest/coolest) so the compact system reads as a
graded sequence in orbit view. The tint is low-confidence: with no
eclipse or reflectance data the mineralogy is unconstrained, and the
warm-rock reading is the interesting-first tie-break.

**Morphology.** Tidally locked (the 4.66-day orbit damps spin to
synchronous within the system age), so the substellar point is fixed.
Default texture is cratered rocky plains with a warm dayside and a cold
nightside; no resurfacing mechanism is confirmed, so there are no forced
volcanic features.

## Atmosphere synthesis

No transmission spectrum exists for YZ Cet d, so its atmosphere is a
synthesis choice within the allowed window, bracketed by the same two
considerations as its siblings: a thin secondary atmosphere is
thermally plausible — indeed most plausible of the three at d's lower
T_eq ≈ 357 K and ~2.7× Earth insolation — but the moderately active
flaring M-dwarf host with its kG field, strong wind, and the planets
orbiting deep inside the stellar magnetosphere (sub-Alfvénic; Trigilio
2023) still makes retention marginal.

Like c, d carries **no SPI signal of its own** — the radio bursts do
not fold to d's orbit (Pineda & Villadsen 2023; Trigilio 2023 find the
worst agreement of the three for d) — so there is no inferred magnetic
field to argue for extra atmospheric shielding. Being the outermost and
coolest, d is nonetheless the best atmosphere-retention candidate of the
trio on thermal grounds alone.

For NearStars the cfg adopts a **thin secondary atmosphere
(~0.1 bar, CO₂/N₂)** as the interesting-first tie-break, with the
airless variant preserved in Open items. This is a low-confidence
aesthetic choice giving d a faint warm limb haze (`#bca088`) and some
day-night heat redistribution.

**Sky appearance.** With the thin atmosphere, the daytime sky under the
3100 K star is a dim red-orange with weak Rayleigh blue near the zenith;
airless, it is black with a sharp-edged stellar disk. The host star
dominates the sky at ~2.9° angular diameter (about 6× the Sun from
Earth), deep red-orange; the inner siblings b and c appear as bright
moving points.

## Rotation & spin synthesis

YZ Cet d is tidally locked. At a = 0.0285 AU around a 0.137 M☉ star the
tidal-locking timescale is far shorter than the system age, so the
planet rotates synchronously with its 4.65626-day orbit. The
eccentricity (0.07 ± 0.05; Stock 2020) is poorly constrained and
consistent with near-circular; at e ≲ 0.07 the 1:1 spin-orbit resonance
is favoured over 3:2 (3:2 requires e ≳ 0.01 with significant
triaxiality, not supported by the low-e RV solution; Vinson 2017 /
Makarov 2018). Obliquity is damped to zero.

**KSP implementation note.** Rotation period = orbital period =
4.65626 days = 402 301 s. In Kopernicus the body's `rotationPeriod`
equals the orbital `period` in seconds.

**No seasons.** With obliquity = 0 and a near-circular orbit, the
substellar point is fixed in the surface frame.

As the outermost member of the compact near-coplanar system, d's only
spin consequence for the cfg is the fixed substellar point and the
absence of seasons; its longer 4.66-day day-length is still far shorter
than any gameplay-relevant timescale.

## Visual styling

Combining the surface and atmosphere decisions:

- **Global color palette.** A warm iron-toned rocky world (`#62503f`
  primary, `#6e3e2a` oxidized accent) under deep red-orange 3100 K
  light — the lightest of the three planet tints, completing the
  inside-out warm-to-cooler gradient of the compact system.
- **Dayside.** Warm substellar hemisphere (~395 K peak) with textured
  rocky plains; a faint warm limb haze if the thin atmosphere is
  present.
- **Terminator band.** Sharp and high-contrast if airless; softened by
  thin-atmosphere scattering in the adopted scenario.
- **Nightside.** Cold; partially warmed by atmospheric redistribution in
  the thin-atmosphere reading, near-black if airless. Reflected light
  from siblings b and c at conjunction is the main nightside source.
- **No SPI aurora.** Like c, d is not the flux-tube driver, so it carries
  no inferred magnetosphere and no star-planet aurora; rendered as a
  plain warm rocky world.
- **Star in sky.** YZ Cet subtends ~2.9° in d's sky (≈ 6× the Sun from
  Earth), a pale warm orange (3100 K → `#ffd081`), flooding the surface
  with ~2.7× Earth's insolation. Frequent flares from the
  eruptive-variable host punctuate the illumination.
- **Sister planets in sky.** b and c (both inner) appear as bright
  moving points; near-coplanar compact system with frequent
  conjunctions.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2020A&A...636A.119S** Stock et al. 2020 — Phase 2 recommended
  source for d's orbit (P = 4.65626 d, a = 0.02851 AU, e = 0.07) and
  minimum mass (1.09 M⊕), plus the semi-empirical radius estimate
  (1.03 R⊕).
- **[2304.00031](https://arxiv.org/abs/2304.00031)** Pineda & Villadsen 2023 — VLA SPI study; establishes
  that the radio bursts fold to b's orbit, **not** d's (worst phase
  agreement of the three for d), so d is not the SPI driver.
- **[2305.00809](https://arxiv.org/abs/2305.00809)** Trigilio et al. 2023 — uGMRT SPI confirmation; same
  conclusion (d's detections randomly mixed around the orbit, no folding
  → no SPI attribution to d). Cites R_d = 1.04 R⊕. Source for the
  d-is-not-driver decision.

### Read (context / methodology, not decision-driving)

- **2017A&A...605L..11A** Astudillo-Defru et al. 2017 — discovery paper;
  earlier d orbit/mass solution (P = 4.65627 d, e = 0.129,
  M sin i = 1.14 M⊕) retained as `recommended:false`.
- Host stellar synthesis (`yz-cet.md`) — the Teff/L/R/M values that set
  d's illumination.

### Read (instrument-only, not visual-informative)

- The radio-interferometry methodology of the two SPI papers is read for
  the d-not-driver conclusion but yields no additional d-specific visual
  field.

### Not read — no arXiv preprint or low-priority (~handful)

No JWST, transit, or transmission-spectroscopy paper exists for d (it
does not transit), so there is no eclipse/atmosphere literature to read.
The generic SPI-theory references inside the two radio papers are read
for context but contribute no d-specific cfg number.

## Open items for follow-up

- **Cfg variant: airless d.** The adopted thin-atmosphere reading is an
  interesting-first tie-break; the conservative airless variant is
  preserved here as an alternative cfg. d is the best atmosphere-retention
  candidate of the three on thermal grounds, so the thin-atmosphere
  variant is most defensible here.
- **Radius is an estimate, not a measurement.** d does not transit; the
  1.03 R⊕ figure is semi-empirical. A future mass/radius measurement
  would update the surface gravity and density.
- **Atmosphere detection.** Only a future emission/phase-curve campaign
  could confirm or exclude the thin atmosphere; until then the pressure
  stays low-confidence.

## Related

- [yz-cet](yz-cet.md) — host star; the M4.5 V flare star with the confirmed SPI radio aurora
- [yz-cet-b](yz-cet-b.md) — innermost sibling and the SPI driver (≥ 0.4 G magnetic field)
- [yz-cet-c](yz-cet-c.md) — middle sibling
- [methodology](../reference/methodology.md) — schema for the Decisions table and confidence tags
