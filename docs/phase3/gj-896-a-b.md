<!-- GJ 896 A b Phase 3 synthesis: cfg-ready decisions and reasoning -->
# GJ 896 A b — Phase 3 Synthesis

GJ 896 A b is a warm ~2.3 M_Jup gas giant orbiting the young active
M3.5 Ve flare star GJ 896 A at a = 0.63965 ± 0.00067 AU with a
284.39 ± 1.47 d period and a moderately eccentric orbit e = 0.35 ± 0.19
(Curiel et al. 2022). It was discovered by VLBA + optical/IR
astrometry, which yields a **true mass** rather than a minimum mass:
m_b = 2.26 ± 0.57 M_Jup (= 718.29 ± 181.16 M⊕), with an orbital
inclination i = 69.2°. This makes GJ 896 A b the first planetary
companion of a star in a binary system found by astrometry, and — at
6.26 pc — one of the nearest Jovian-mass planets known. No transmission
or thermal-emission spectrum exists; the planet's atmospheric
composition, radius, rotation, and any moon or ring population are
unconstrained, so those fields are jovian-analog tie-breaks under the
red-dwarf illumination.

**Scenario choice for NearStars: a warm (T_eq ≈ 130 K at the
semi-major axis, swinging ~110–165 K over the eccentric orbit), mature
~2.3 M_Jup jovian on a 0.64 AU orbit, lit by a deep-red M3.5 Ve flare
star.** It sits outside the host's narrow habitable zone (Curiel 2022:
0.18–0.26 AU) and oscillates around the snow line (~0.51 AU), so it is
a cold-to-warm Jovian whose orbit carries it from just inside to well
outside the water-ice line. Visual styling treats it as a Jupiter-mass
analog with ammonia-ice cloud bands rendered warm under M-dwarf
illumination, a faint photochemical haze from the active host's
elevated UV/flares, no ring, and a Jupiter-scaled magnetosphere. The
orbit and true mass are the high-confidence Phase 2 anchors; the
radius, atmosphere, clouds, rotation, and magnetosphere are
jovian-analog tie-breaks (no spectrum or thermal map yet).

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | high | 284-day orbit at 0.64 AU around a 0.44 M☉ star — tidal spin-down timescale ≫ system age at this separation; a Jovian retains a fast primordial spin |
| `obliquity_deg` | 25 | low | Tie-break: no measurement. Saturn-like ~26° picked over Jupiter-like 3° for a visually distinctive axis tilt; within the dynamical window for a 0.64 AU jovian. Note the large 148° mutual inclination of the planetary vs binary plane (Curiel 2022) makes a non-trivial obliquity plausible |
| `eccentricity` | 0.35 ± 0.19 | high | Curiel et al. 2022 — astrometric fit (Phase 2 recommended); perihelion 0.42 AU, aphelion 0.86 AU |
| `argument_of_periastron_deg` | 353.11 | high | Curiel et al. 2022 (Phase 2 recommended) |
| `sidereal_period_days` | 284.39 ± 1.47 | high | Curiel et al. 2022 — astrometric fit (Phase 2 recommended); single-companion fit gives 281.56 ± 1.67 d (`recommended:false`) |
| `semi_major_axis_au` | 0.63965 ± 0.00067 | high | Curiel et al. 2022 — full combined astrometric fit (Phase 2 recommended) |
| `inclination_deg` | 69.2 ± 25.61 | medium | Curiel et al. 2022 (Phase 2 recommended); the large uncertainty reflects the astrometric orbit solution |
| `longitude_of_ascending_node_deg` | 45.62 | medium | Curiel et al. 2022 (Phase 2 recommended); astrometry directly constrains Ω, rare for non-transiting planets |
| `mass_mjup` | 2.26 ± 0.57 | high | Curiel et al. 2022 — **true mass** from the full combined astrometric fit (Phase 2 recommended); not a minimum mass, since astrometry breaks the sin i degeneracy |
| `mass_mearth` | 718.29 ± 181.16 | high | Curiel et al. 2022 (= 2.26 M_Jup × 317.8); Phase 2 recommended true mass |
| `radius_rjup` | 1.1 | low | Tie-break: no transit. Mature 2.3 M_Jup jovians (Fortney 2007 / Burrows evolutionary tracks) sit near ~1.0–1.1 R_Jup; cfg picks 1.1 R_Jup. The DB `radius_rearth = 13.3` (≈ 1.19 R_Jup) is a NASA-archive model placeholder, not a measurement — consistent with this range |
| `surface_gravity_g_earth` | ~4.7 | medium | derived: g = G M / R² with M = 2.26 M_Jup, R = 1.1 R_Jup → ~46 m/s² ≈ 4.7 g⊕; a massive jovian (≈2× Jupiter surface gravity) |
| `density_g_cc` | ~2.1 | medium | derived: 2.26 M_Jup / (1.1 R_Jup)³ × ρ_Jup ≈ 2.1 g/cc; a compact, massive, mature gas giant denser than Jupiter (1.33 g/cc) |
| `insolation_s_earth` | ~0.05 | low | derived: S = L_star / a² with the synthesized L ≈ 0.02 L☉ (no Phase 2 luminosity) / (0.64 AU)² ≈ 0.05 S⊕; low-confidence because L is synthesized, not measured |
| `equilibrium_temp_k_a0` | ~130 | low | derived: T_eq = 278 K × (L/a²)^0.25 with synthesized L ≈ 0.02 L☉ at a = 0.64 AU; ranges ~110 K (aphelion 0.86 AU) to ~165 K (perihelion 0.42 AU). Low-confidence because no Phase 2 L; Curiel does not measure T_eq (`equilibrium_temperature_k` null in DB) |
| `equilibrium_temp_k_a03` | ~120 | low | derived; Earth-analog A = 0.3; same synthesized-L caveat |
| `bond_albedo` | 0.34 | low | Tie-break: Saturn-analog 0.34 picked over Jupiter's 0.50 because the cold T_eq ≈ 130 K skews cloud chemistry toward a thick ammonia-ice deck more Saturn-like than Jupiter-like |
| `atmosphere_present` | true | high | gas giant by definition; H₂/He bulk inferred from the 2.3 M_Jup mass at jovian radius |
| `atmosphere_reference_pressure_pa` | 100000 | medium | gas giant has no solid surface; cfg-reference 1 bar level for cloud-deck rendering, conventional jovian KSP atmosphere origin |
| `atmosphere_composition` | H₂ ~89%, He ~10%, CH₄ ~0.2%, NH₃ ~0.02%, H₂O (deep) ~0.01%, trace photochemical products | low | Tie-break: no spectrum. Solar-composition jovian default (Lodders 2003 protosolar), with condensation chemistry truncated at the ~130 K equilibrium and an ammonia-ice cloud deck |
| `atmosphere_scale_height_km` | ~10 | medium | derived: H = kT / (μ m_H g) with T ≈ 130 K, μ = 2.3, g ≈ 46 m/s² ≈ 10 km |
| `atmosphere_tint_rgb_hex` | `#d8b890` (warm-tan limb haze under M3.5 V illumination) | low | Tie-break: ammonia-ice atmosphere is intrinsically near-white; the deep-red ~3300 K SED shifts the perceived limb haze warm/tan, redder than a Sun-lit jovian limb |
| `cloud_cover_fraction` | 0.85 | medium | jovian-analog: near-complete zonal banding with belt/zone contrast; 0.85 leaves distinct dark belts vs bright zones rather than a uniform overcast |
| `cloud_morphology` | zonal bands; ammonia-ice cloud deck at ≈ 0.5–1 bar; possible water-cloud deck below; faint photochemical haze above 100 mbar from CH₄ photolysis under the active host's elevated UV/flares | low | Tie-break: no GCM; Saturn-analog band structure, with GJ 896 A's strong flare/UV activity driving a slightly more prominent stratospheric haze than a quiet-host jovian |
| `cloud_tint_rgb_hex` | `#e6d2b4` (warm cream — NH₃ ice under M-dwarf illumination) | low | Tie-break: Saturn's ammonia clouds read cream-white under solar light; under the ~3300 K deep-red SED the perceived hue shifts further into warm cream/tan |
| `planet_disk_tint_rgb_hex_primary` | `#e6d2b4` (cream-tan zones — dominant cloud-deck appearance) | low | downstream of `cloud_tint_rgb_hex` |
| `planet_disk_tint_rgb_hex_accent` | `#c0a070` (warm tan-brown belts — deeper cloud layers + haze showing through) | low | Tie-break: Jupiter/Saturn belt-zone contrast under M-dwarf illumination; band amplitude moderate given the low insolation and weak convective drive |
| `ring_present` | false | low | Tie-break: no detection (astrometry cannot see a ring). cfg defaults to "no ring" — no fabricated feature per the search-and-verify policy |
| `rotation_period_hours` | 10 | low | Tie-break: no rotation measurement. Jupiter-analog ~10 h fast rotation; a massive young jovian retains a large primordial spin angular momentum, favoring Jupiter-class rapid rotation over slower Saturn/Uranus-like values |
| `magnetic_field_strength_microtesla_equator` | 2000 | low | Energy-flux dynamo scaling (Christensen et al. 2009 `2009Natur.457..167C`; Reiners & Christensen 2010 `1007.1514`): B_dip^pol = 9 G·(age/4.5 Gyr)^−0.33·(M/M_Jup)^0.93 for 2.26 M_Jup. Host age is genuinely uncertain (≲100 Myr PMS vs ~950 Myr) → B_eq spans ~1600 (old) to ~3400 (young) µT; cfg picks ~2000 µT central, the young active host favoring the high end. (Field key normalized to the canonical `_strength_` spelling.) See docs/reference/planetary-dynamo-scaling.md |
| `magnetic_dipole_moment_normalized_earth` | 120000 | low | 2000 µT × (1.10 R_Jup)³ vs Jupiter (4.5 G equatorial, 20 000× Earth) → ≈ 1.2×10⁵ × Earth via energy-flux scaling (`1007.1514`); age- and R³-sensitive → low conf |
| `aurora_present` | true | medium | the host GJ 896 A is a very active flare star with a kG field and frequent radio/X-ray bursts (Curiel 2022); the elevated stellar wind + flare plasma flux at 0.64 AU, captured by the jovian magnetosphere, drives strong auroral emission |
| `aurora_color_primary_hex` | `#c84080` (H-Balmer α 656 nm red-pink in an H₂-rich jovian atmosphere) | low | Tie-break: visible-band jovian aurora is dominated by H-Balmer α; reads as red-pink, reinforced by the deep-red illumination context |
| `star_apparent_angular_diameter_deg` | ~0.29 (0.44 at perihelion) | medium | derived: R ≈ 0.35 R☉ at a = 0.64 AU → ~0.29°; at perihelion 0.42 AU → ~0.44° (near the Sun's apparent size from Earth) |
| `stellar_illumination_color_temp_k` | ~3300 (synthesized) | low | Synthesized from the host's M3.5 V spectral type (no Phase 2 Teff); deep-red M-dwarf illumination |

## Surface synthesis

GJ 896 A b is a gas giant with no solid surface; this section covers
the cloud-deck "surface" an observer would see and the bulk-structure
reasoning behind it. The one firmly measured physical quantity is the
mass: m_b = 2.26 ± 0.57 M_Jup (Curiel 2022), a **true mass** rather
than a minimum mass because the astrometric orbit breaks the sin i
degeneracy that radial velocity leaves open. At 2.3 M_Jup the planet is
a massive, mature jovian; evolutionary tracks for such a planet at any
plausible system age put the radius near ~1.0–1.1 R_Jup, so the cfg
adopts R ≈ 1.1 R_Jup. The DB stores `radius_rearth = 13.3` (≈ 1.19
R_Jup), which is a NASA-archive model placeholder rather than a
measurement, but it is consistent with this range. The implied bulk
density is high (~2 g/cc, denser than Jupiter) and the surface gravity
is large (~58 g⊕), so the visible atmosphere is compact with a small
~9 km scale height.

The thermal state is cold-to-warm. With the host's luminosity not
measured in Phase 2, the equilibrium temperature is synthesized from
L ≈ 0.02 L☉ (the Stefan-Boltzmann / mass-luminosity estimate from the
stellar synthesis) and is flagged low-confidence: T_eq ≈ 130 K at the
0.64 AU semi-major axis, swinging from ~110 K at aphelion (0.86 AU) to
~165 K at perihelion (0.42 AU) over the eccentric orbit. Curiel 2022
locates the host's habitable zone at 0.18–0.26 AU and the snow line at
~0.51 AU, so GJ 896 A b sits well outside the HZ and oscillates around
the snow line — inside it near perihelion, outside it for most of the
orbit. At ~130 K the dominant condensate is ammonia ice, so the
visible cloud-deck "surface" is an ammonia-ice deck near the 0.5–1 bar
level.

Under the deep-red M3.5 V illumination the rendered cloud deck is a
warm cream-tan (`#e6d2b4` zones, `#c0a070` belts): Saturn's ammonia
clouds appear cream-white under solar light, and the ~3300 K
synthesized SED shifts the perceived hue further into warm cream. The
belt/zone contrast is moderate — the low insolation gives a weaker
convective drive than Jupiter, so the bands are present but less
vivid. All of the surface/cloud color and morphology fields are
jovian-analog tie-breaks: no transmission or thermal-emission spectrum
of GJ 896 A b exists, so the cfg defaults to the most interesting
spectrally-plausible reading (banded ammonia-ice jovian) rather than a
featureless disk.

## Atmosphere synthesis

GJ 896 A b has a deep H₂/He envelope inferred from its 2.3 M_Jup mass
at a jovian radius; the atmosphere is the planet, so this section
covers composition, the cloud/haze structure, and the sky an observer
in the upper atmosphere would see.

**Composition.** With no spectrum, the cfg adopts a solar-composition
jovian default (Lodders 2003 protosolar abundances): H₂ ~89%, He ~10%,
with CH₄ (~0.2%), NH₃ (~0.02%), and deep H₂O as the principal
volatiles, plus trace photochemical products. The condensation
chemistry is truncated at the ~130 K equilibrium temperature, which
puts the ammonia cloud deck near 0.5–1 bar and a deeper water-cloud
deck below (inaccessible to visible imaging). This is the same
composition tie-break used for the other NearStars cool jovians; it
will be replaced if a spectrum is ever obtained.

**Photochemistry under an active host.** The headline atmospheric
modifier is the host star. GJ 896 A is a very active flare star with a
kG-scale field and frequent radio/X-ray bursts (Curiel 2022), so the
incident UV and flare-particle flux at 0.64 AU is elevated relative to
a quiet-host jovian. This drives CH₄ photolysis above the ~100 mbar
level and is expected to build a thin hydrocarbon/photochemical haze
layer, rendered as a faint warm-tan limb haze (`#d8b890`) above the
ammonia deck — slightly more prominent than the haze on a jovian around
a quiet star, but still a subtle limb effect rather than a dominant
tint. The flare-particle flux also feeds the auroral activity (below).

**Sky appearance.** From within the upper atmosphere the sky is a deep
ammonia-cloud haze lit warm cream-tan by the red host star. The
dominant light source is GJ 896 A's deep-red disk, subtending ~0.29° at
the semi-major axis (growing to ~0.44° near perihelion) — a little over
half the Sun's apparent size from Earth, deep red-orange, flooding the
cloud tops with infrared-rich light at a few percent of Earth's
insolation. The second sun, GJ 896 B, is a far smaller but distinct
bright red point on its wide retrograde orbit.

## Rotation & spin synthesis

GJ 896 A b is **not tidally locked**: at a = 0.64 AU around a 0.44 M☉
star the tidal spin-down timescale vastly exceeds the system age, so
the planet retains a fast primordial rotation like the Solar System's
giant planets. The cfg adopts a Jupiter-analog ~10-hour rotation
period — a massive young jovian carries a large primordial spin
angular momentum, favoring Jupiter-class rapid rotation over the slower
Saturn-like (10.7 h) or Uranus-like (17 h) values. This is a tie-break:
no rotation measurement exists.

**KSP implementation note.** Planet rotation period ≈ 10 h = 36 000 s,
set in seconds on the planet body in Kopernicus. The fast rotation
drives the zonal banding and the oblate figure typical of a rapidly
rotating gas giant.

**Obliquity and the binary architecture.** The cfg picks a Saturn-like
obliquity of ~25° (tie-break, no measurement) over a Jupiter-like ~3°,
for a visually distinctive axis tilt within the dynamical window for a
0.64 AU jovian. There is a physical hook for a non-trivial obliquity
here: Curiel 2022 finds a large mutual inclination Φ = 148° between the
planetary orbital plane and the wide binary orbital plane (a retrograde
configuration), the kind of misaligned architecture that can excite and
maintain a substantial planetary obliquity through secular forcing from
the stellar companion. The eccentric (e = 0.35) orbit gives the planet
a genuine seasonal/insolation cycle as it swings between 0.42 and
0.86 AU, on top of any obliquity seasons — distinct from the
near-circular orbits of most catalog jovians.

## Visual styling

In the NearStars renderer, GJ 896 A b is portrayed as a warm,
banded, red-dwarf-lit Jovian on a visibly eccentric orbit:

- **Global appearance (orbit view).** A massive ~1.1 R_Jup gas giant
  with warm cream-tan zonal bands (`#e6d2b4` zones, `#c0a070` belts),
  lit deep red by the M3.5 V host — the banding present but moderate in
  contrast given the weak convective drive at low insolation. An oblate
  figure from the fast ~10 h rotation.
- **Dayside detail.** Distinct Jupiter/Saturn-style belts and zones;
  the ammonia-ice cloud deck reads warm cream under the ~3300 K SED,
  with belt regions a deeper tan-brown where the cloud deck thins.
- **Terminator band.** A faint warm-tan photochemical haze layer
  (`#d8b890`) sits above the cloud deck along the limb — a touch more
  prominent than on a quiet-host jovian because of GJ 896 A's elevated
  UV and flare flux.
- **Nightside.** Dark, with possible auroral glow near the magnetic
  poles (below).
- **Aurorae.** GJ 896 A's strong flare/radio activity and elevated
  stellar wind drive a vigorous magnetosphere-fed aurora; rendered as
  red-pink H-Balmer-α auroral ovals (`#c84080`) at the magnetic poles,
  brightening in step with the host's frequent flares — a distinctive,
  scientifically-grounded effect given the unusually active host.
- **No ring.** No ring is rendered (tie-break: no detection, and no
  fabricated feature per the search-and-verify policy).
- **Host star in the sky.** GJ 896 A's deep-red disk subtends ~0.29° at
  the semi-major axis, growing to ~0.44° near perihelion — a little
  over half to nearly the full Sun's apparent size from Earth — and
  floods the cloud tops with infrared-rich red light. The eccentric
  orbit makes the star visibly swell and shrink over each 284-day year.
- **Second sun.** GJ 896 B, the M4.5 companion, appears as a smaller
  but distinct bright red point on its wide 229-year retrograde orbit
  (a = 31.6 AU) — a true two-sun sky, both suns deep red.

## Bibliography

### Read (drove Decisions above)

- **Curiel S. et al. 2022** — *3D orbital architecture of a dwarf
  binary system and its planetary companion*, AJ 164, 93
  (`2022AJ....164...93C`, doi:10.3847/1538-3881/ac7c66,
  [arXiv:2208.14553](https://arxiv.org/abs/2208.14553)). The VLBA + optical/IR astrometric discovery of
  GJ 896 A b. Phase 2 recommended source for the true mass
  (2.26 ± 0.57 M_Jup = 718.29 M⊕), the full orbital element set
  (a = 0.63965 AU, P = 284.39 d, e = 0.35, i = 69.2°, Ω = 45.62°,
  ω = 353.11°), the habitable-zone (0.18–0.26 AU) and snow-line
  (~0.51 AU) estimates that place the planet's thermal regime, and the
  large 148° planetary-vs-binary mutual inclination / retrograde
  architecture used in the obliquity reasoning. Also the host context
  (M3.5 Ve flare star, GJ 896 B companion) feeding the illumination and
  second-sun rendering.

### Read (context / methodology, not decision-driving)

- **Fortney J.J. et al. 2007** & **Burrows A. et al.** (evolutionary
  giant-planet mass-radius-age tracks) — the basis for the ~1.0–1.1
  R_Jup radius tie-break for a mature 2.3 M_Jup jovian. Read for the
  radius row only; no GJ-896-specific content.
- **Lodders K. 2003** — protosolar elemental abundances; the basis for
  the solar-composition atmosphere tie-break. Methodology context.

### Read (instrument-only, not visual-informative)

- The VLBA astrometric orbit-fitting methodology in Curiel 2022 (AIPS
  phase-referencing, AGA / least-squares + MCMC orbit solution) is the
  instrument backbone of the true-mass and orbital-element measurement
  but contributes no direct visual field beyond the parameters already
  used above.

### Not read — no arXiv preprint or low-priority (~handful)

No transmission, emission, or reflected-light spectrum of GJ 896 A b
exists, so the atmosphere/cloud composition and color fields are all
jovian-analog tie-breaks with no paper to read. Generic cool-jovian
atmosphere / photochemistry surveys (e.g. Sudarsky albedo classes,
Marley cloud models) inform the qualitative banded-ammonia-jovian
picture but supply no GJ-896-b-specific number to curate. The
single-companion orbit fit (Curiel 2022 Table 2 col 3:
a = 0.6352 AU, P = 281.56 d, e = 0.30) is retained in the DB as the
`recommended:false` alternative.

## Open items for follow-up

- **Direct imaging + spectroscopy.** Curiel 2022 notes GJ 896 A b is
  one of the nearest Jovians known and "well suited" for direct imaging
  and spectroscopy. A future spectrum would replace the tie-break
  atmosphere composition, cloud tints, and haze with measured values
  and upgrade those rows from low to high confidence.
- **Host Teff / luminosity.** The planet's insolation and equilibrium
  temperature are synthesized from a non-measured host luminosity
  (L ≈ 0.02 L☉). A curated Teff/L for GJ 896 A would sharpen T_eq
  (currently ~130 K, low confidence) and the insolation row.
- **Radius measurement.** No transit (the astrometric i = 69.2° is not
  edge-on, and the planet is not known to transit), so the radius stays
  a model-derived ~1.1 R_Jup tie-break; the DB `radius_rearth = 13.3`
  placeholder should be treated as such until a real measurement exists.
- **GJ 896 B as a DB body.** The second sun in the planet's sky is not
  yet a separate DB body; adding it (and the binary_orbit cfg for the
  229-year retrograde pair) would let the two-sun sky and the secular
  obliquity forcing be rendered faithfully.
- **Obliquity / spin.** The Saturn-like ~25° obliquity and ~10 h
  rotation are tie-breaks; the 148° mutual-inclination architecture
  motivates a non-trivial obliquity but does not pin it. Refine if a
  dynamical study of the misaligned system constrains the planet's
  spin state.

## Related

- [methodology](../reference/methodology.md) — schema source for the Decisions table
- [gj-896-a](gj-896-a.md) — the host M3.5 Ve flare star; source of the illumination color, insolation, and second-sun context
- [eps-eri-b](eps-eri-b.md) — comparison cool jovian (~0.78 M_Jup, 3.5 AU around a K2V); contrast its near-circular orbit and single-star system with GJ 896 A b's eccentric orbit and misaligned binary architecture
