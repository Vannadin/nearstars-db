<!-- YZ Cet c Phase 3 synthesis: cfg-ready decisions and reasoning -->
# YZ Cet c — Phase 3 Synthesis

YZ Cet c is the middle of three planets around the M4.5 V flare star
YZ Cet, on a 3.05989-day orbit at a = 0.0216 AU (Stock et al. 2020).
Like its siblings it is a non-transiting radial-velocity planet: its
minimum mass M sin i = 1.14 ± 0.11 M⊕ (Stock 2020) is measured — the
most massive of the three — but its radius is **not**, so the 1.05 R⊕
figure in the DB is a semi-empirical mass-radius estimate, not an
observation. With the host's L = 0.0022 L☉ the equilibrium temperature
is T_eq ≈ 410 K at zero albedo (computed here; T_eq = 278.3·L^0.25/√a),
making c a **warm rocky world** — cooler than the inner planet b
(471 K) but still well above Earth, at ~4.7× Earth's insolation.

**Scenario choice for NearStars: a warm, tidally-locked rocky planet
with a thin-to-absent secondary atmosphere.** YZ Cet c is not the SPI
driver — the confirmed star-planet magnetic interaction folds to
planet b's orbit, and the radio bursts show worse phase agreement with
c (Pineda & Villadsen 2023; Trigilio 2023). c is therefore rendered as
a "plain" warm rocky planet: the slightly more massive, slightly cooler
middle world. Surface and atmosphere sit at low confidence because no
transit, eclipse, or transmission spectrum exists.

## Decisions

Kopernicus / atmosphere cfg-ready values. `Confidence`: high =
directly measured or tightly constrained, medium = theoretical with
strong support, low = aesthetic choice within the allowed window.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 3.06 d orbit at 0.0216 AU; tidal locking time ≪ system age for a mid-M host |
| `obliquity_deg` | 0 | high | tidal damping at this orbit |
| `eccentricity` | 0.0 | medium | Stock et al. 2020 (Phase 2 recommended); circular orbit adopted |
| `argument_of_periastron_deg` | n/a | high | circular orbit (e = 0) — periastron undefined |
| `sidereal_period_days` | 3.05989 | high | Stock et al. 2020 (Phase 2 recommended) |
| `semi_major_axis_au` | 0.02156 | high | Stock et al. 2020 (Phase 2 recommended) |
| `mass_mearth` | ≥ 1.14 ± 0.11 (M sin i) | high | Stock et al. 2020 RV minimum mass (Phase 2 recommended); most massive of the three; true mass higher by 1/sin i |
| `radius_rearth` | ~1.05 (ESTIMATE) | low | NOT measured — no transit. Semi-empirical M-R estimate (Stock 2020); Pineda & Villadsen 2023 cite R_c = 1.05 R⊕ from the same relation |
| `surface_gravity_g_earth` | ~1.03 | low | derived = 1.14 / 1.05² from minimum mass + estimated radius; a lower bound (true mass higher) |
| `density_g_cc` | ~5 (assumed rocky) | low | No measured radius → no measured density; Earth-like rocky composition assumed |
| `insolation_s_earth` | 4.7 | high | derived = L / a² = 0.0022 / 0.02156² |
| `equilibrium_temp_k` (A=0) | 410 | high | derived = 278.3 · L^0.25 / √a (L = 0.0022 L☉, a = 0.02156 AU) |
| `equilibrium_temp_k` (A=0.3) | 376 | high | derived, Earth-analog Bond albedo |
| `bond_albedo` | 0.1 | low | Tie-break: assumed low for a warm rocky surface; no measurement |
| `atmosphere_present` | thin or absent | low | No transmission spectrum; warm rocky RV planet around an active flaring M dwarf — atmosphere retention is marginal. cfg renders a thin atmosphere as the interesting option |
| `atmosphere_surface_pressure_pa` | ~10000 (0.1 bar, tie-break) | low | No measurement; thin secondary atmosphere chosen as more interesting than airless. Airless variant preserved in Open items |
| `atmosphere_composition` | CO₂ / N₂ secondary (assumed) | low | No spectrum; outgassed rocky-planet composition assumed if any atmosphere survives |
| `atmosphere_tint_rgb_hex` | `#c2a07c` (thin warm haze) | low | Tie-break: faint warm limb haze under 3100 K illumination if a thin atmosphere is present |
| `dayside_surface_temp_k` | ~450 | medium | substellar bare-rock peak above the 410 K global T_eq (A=0, low redistribution) |
| `nightside_surface_temp_k` | depends on atmosphere | low | airless → very cold nightside; thin atmosphere → partial redistribution |
| `surface_tint_rgb_hex_primary` | `#5e4a3c` (warm basaltic rock) | low | Tie-break: warm-toned iron-bearing basalt under red M-dwarf light; slightly lighter than the warmer inner planet b |
| `surface_tint_rgb_hex_accent` | `#74402a` (oxidized iron patches) | low | Tie-break: photolytic / oxidized iron on an exposed warm rocky surface |
| `surface_morphology` | cratered rocky plains, tidally-locked | low | No data; generic warm rocky morphology under tidal lock |
| `spi_driver` | false | high | Pineda & Villadsen 2023; Trigilio 2023 — the SPI bursts fold to b's orbit, not c's (worse phase agreement for c); c is not the flux-tube driver |
| `planet_magnetic_field_g` | unconstrained | low | No SPI signal attributable to c → no field inference; left unconstrained |
| `star_apparent_angular_diameter_deg` | 3.88 | high | derived = 2 · R★ / a · (180/π), R★ = 0.1571 R☉ |
| `stellar_illumination_color_temp_k` | 3100 | high | Cifuentes et al. 2020 host Teff |

## Surface synthesis

YZ Cet c has no transit, eclipse, or transmission measurement, so its
surface is inferred entirely from its minimum mass, orbit, and host
illumination. The radius (1.05 R⊕) is a semi-empirical mass-radius
estimate, not an observation — the same value Pineda & Villadsen 2023
cite (R_c = 1.05 R⊕) from the Stock 2020 relation. The minimum mass
M sin i = 1.14 M⊕ (Stock 2020) is a genuine lower bound and makes c the
most massive of the three planets; the true mass is higher by 1/sin i.
For cfg purposes c is treated as an Earth-mass-class rocky planet.

c is **warm, not molten**. The equilibrium temperature at zero albedo
is T_eq ≈ 410 K (computed here from L = 0.0022 L☉ and a = 0.02156 AU),
about 60 K cooler than the inner planet b, at ~4.7× Earth's insolation.
This is hotter than Earth but cooler than Venus's equilibrium
temperature — a genuinely warm, but not lava, world. The substellar
bare-rock peak is ~450 K.

**Color choice.** Under the host's 3100 K red-orange illumination, c is
rendered as a warm iron-bearing basaltic surface (`#5e4a3c` primary)
with oxidized iron-patch accents (`#74402a`) — slightly lighter than the
inner, warmer planet b, to give the compact system a perceptible
inside-out temperature gradient in orbit view. The tint is
low-confidence: with no eclipse or reflectance data the mineralogy is
unconstrained, and the warm-rock reading is the interesting-first
tie-break over a featureless grey sphere.

**Morphology.** Tidally locked (the 3.06-day orbit damps spin to
synchronous within the system age), so the substellar point is fixed.
Default texture is cratered rocky plains with a warm dayside and a cold
nightside; no resurfacing mechanism is confirmed, so there are no forced
volcanic features.

## Atmosphere synthesis

No transmission spectrum exists for YZ Cet c, so its atmosphere is a
synthesis choice within the allowed window, bracketed by the same two
considerations as the other planets: a thin secondary atmosphere is
thermally plausible at T_eq ≈ 410 K and ~4.7× Earth insolation, but the
moderately active flaring M-dwarf host with its kG field, strong wind,
and the planets orbiting deep inside the stellar magnetosphere
(sub-Alfvénic; Trigilio 2023) makes retention marginal.

Unlike planet b, c carries **no SPI signal of its own** — the radio
bursts do not fold cleanly to c's orbit (Pineda & Villadsen 2023;
Trigilio 2023 find worse agreement for c and d) — so there is no
inferred magnetic field to argue for extra atmospheric shielding. c is
therefore the more conservative case: a thin atmosphere is possible but
less defended than on b.

For NearStars the cfg adopts a **thin secondary atmosphere
(~0.1 bar, CO₂/N₂)** as the interesting-first tie-break, with the
airless variant preserved in Open items. This is a low-confidence
aesthetic choice giving c a faint warm limb haze (`#c2a07c`) and some
day-night heat redistribution.

**Sky appearance.** With the thin atmosphere, the daytime sky under the
3100 K star is a dim red-orange with weak Rayleigh blue near the zenith;
airless, it is black with a sharp-edged stellar disk. The host star
dominates the sky at ~3.9° angular diameter (about 8× the Sun from
Earth), deep red-orange; the inner sibling b and outer sibling d appear
as bright moving points.

## Rotation & spin synthesis

YZ Cet c is tidally locked. At a = 0.0216 AU around a 0.137 M☉ star the
tidal-locking timescale is far shorter than the system age, so the
planet rotates synchronously with its 3.05989-day orbit. The
eccentricity is adopted as circular (e = 0; Stock 2020), which makes the
1:1 spin-orbit resonance unambiguous (3:2 requires e ≳ 0.01 with
triaxiality; Vinson 2017 / Makarov 2018). Obliquity is damped to zero.

**KSP implementation note.** Rotation period = orbital period =
3.05989 days = 264 374 s. In Kopernicus the body's `rotationPeriod`
equals the orbital `period` in seconds.

**No seasons.** With obliquity = 0 and a circular orbit, the substellar
point is fixed in the surface frame.

The compact, near-coplanar architecture means c sits between b and d in
a tightly packed resonant-adjacent chain; for the cfg the only spin
consequence is the fixed substellar point and the absence of seasons.

## Visual styling

Combining the surface and atmosphere decisions:

- **Global color palette.** A warm iron-toned rocky world (`#5e4a3c`
  primary, `#74402a` oxidized accent) under deep red-orange 3100 K
  light — slightly lighter than the inner planet b, reinforcing the
  inside-out temperature gradient of the compact system.
- **Dayside.** Warm substellar hemisphere (~450 K peak) with textured
  rocky plains; a faint warm limb haze if the thin atmosphere is
  present.
- **Terminator band.** Sharp and high-contrast if airless; softened by
  thin-atmosphere scattering in the adopted scenario.
- **Nightside.** Cold; partially warmed by atmospheric redistribution in
  the thin-atmosphere reading, near-black if airless. Reflected light
  from siblings b and d at conjunction is the main nightside source.
- **No SPI aurora.** Unlike b, c is not the flux-tube driver, so it
  carries no inferred magnetosphere and no star-planet aurora; rendered
  as a plain warm rocky world.
- **Star in sky.** YZ Cet subtends ~3.9° in c's sky (≈ 8× the Sun from
  Earth), a pale warm orange (3100 K → `#ffd081`), flooding the surface
  with ~4.7× Earth's insolation. Frequent flares from the
  eruptive-variable host punctuate the illumination.
- **Sister planets in sky.** b (inner) and d (outer) appear as bright
  moving points; near-coplanar compact system with frequent
  conjunctions.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2020A&A...636A.119S** Stock et al. 2020 — Phase 2 recommended
  source for c's orbit (P = 3.05989 d, a = 0.02156 AU, e = 0) and
  minimum mass (1.14 M⊕), plus the semi-empirical radius estimate
  (1.05 R⊕).
- **[2304.00031](https://arxiv.org/abs/2304.00031)** Pineda & Villadsen 2023 — VLA SPI study; establishes
  that the radio bursts fold to b's orbit, **not** c's (worse phase
  agreement for c), so c is not the SPI driver. Cites R_c = 1.05 R⊕.
- **[2305.00809](https://arxiv.org/abs/2305.00809)** Trigilio et al. 2023 — uGMRT SPI confirmation; same
  conclusion (c and d show randomly mixed detections, no orbital folding
  → no SPI attribution to c). Source for the c-is-not-driver decision.

### Read (context / methodology, not decision-driving)

- **2017A&A...605L..11A** Astudillo-Defru et al. 2017 — discovery paper;
  earlier c orbit/mass solution (P = 3.06008 d, M sin i = 0.98 M⊕)
  retained as `recommended:false`.
- Host stellar synthesis (`yz-cet.md`) — the Teff/L/R/M values that set
  c's illumination.

### Read (instrument-only, not visual-informative)

- The radio-interferometry methodology of the two SPI papers is read for
  the c-not-driver conclusion but yields no additional c-specific visual
  field.

### Not read — no arXiv preprint or low-priority (~handful)

No JWST, transit, or transmission-spectroscopy paper exists for c (it
does not transit), so there is no eclipse/atmosphere literature to read.
The generic SPI-theory references inside the two radio papers are read
for context but contribute no c-specific cfg number.

## Open items for follow-up

- **Cfg variant: airless c.** The adopted thin-atmosphere reading is an
  interesting-first tie-break; the conservative airless variant is
  preserved here as an alternative cfg.
- **Radius is an estimate, not a measurement.** c does not transit; the
  1.05 R⊕ figure is semi-empirical. A future mass/radius measurement
  would update the surface gravity and density.
- **Atmosphere detection.** Only a future emission/phase-curve campaign
  could confirm or exclude the thin atmosphere; until then the pressure
  stays low-confidence.

## Related

- [yz-cet](yz-cet.md) — host star; the M4.5 V flare star with the confirmed SPI radio aurora
- [yz-cet-b](yz-cet-b.md) — inner sibling and the SPI driver (≥ 0.4 G magnetic field)
- [yz-cet-d](yz-cet-d.md) — outermost sibling
- [methodology](../reference/methodology.md) — schema for the Decisions table and confidence tags
