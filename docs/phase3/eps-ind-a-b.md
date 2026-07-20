<!-- eps Ind A b Phase 3 synthesis: cfg-ready decisions and reasoning -->
# ε Indi A b — Phase 3 Synthesis

ε Indi A b is **the nearest directly-imaged cold giant exoplanet to the
Sun** — a ~7.6 M_Jup super-Jupiter orbiting the quiet K5 V dwarf ε Indi A
(11.9 ly) at a = 20.9 (+5.8/−3.3) AU with an eccentricity
e = 0.244 (+0.11/−0.083) and an orbital period P ≈ 108 (+49/−25) yr
(Matthews et al. 2026, JWST/MIRI imaging + Hipparcos–Gaia astrometry +
three decades of RV). It was first imaged by JWST/MIRI at 10.6 and
15.5 µm (Matthews 2024), re-detected at 11.3 µm in a second epoch
(Matthews 2026), and confirmed by common proper motion. The planet is a
cold, solar-age (~3.5 Gyr) giant with an atmospheric temperature near
~275 K — and crucially, that temperature is set by its own internal heat,
not by starlight: the insolation at 20.9 AU around a 0.239 L☉ star is
only S ≈ 5.5 × 10⁻⁴ S⊕, giving a radiative-equilibrium temperature of
just ~43 K. ε Indi A b therefore radiates as a self-luminous, contracting
super-Jupiter, ~230 K hotter than its surroundings.

The atmosphere is the headline. Matthews 2026 measured an F1065C–F1140C
color of 0.88 ± 0.08 mag — an 11σ brightness difference across the
10–11 µm ammonia band — **confirming ammonia (NH₃)**, making ε Indi A b
the coldest planet with an ammonia detection to date. The feature is
shallower than cloud-free solar-metallicity models predict; the authors'
**preferred explanation is thick water-ice clouds** that suppress both
the ammonia feature and the near-IR (3–5 µm) emission (consistent with
archival ground-based non-detections). The best-fit cloudy model is a
275 K, log g ≈ 4.5, ~3× solar metallicity, ~2.5× solar C/O atmosphere
with a highly optically thick H₂O cloud (column optical depth ~416,
reaching τ = 1 near 0.7 bar).

**Scenario choice for NearStars: a cold (~275 K, internally heated)
super-Jupiter on a wide ~20.9 AU eccentric orbit, rendered as a muted,
pale methane/ammonia-class giant — NOT a warm Jovian amber — with thick
water-ice clouds suppressing the bands, confirmed ammonia, and an
optional artistic Saturn-like icy ring (flagged: not observed).** The
orbit and the ammonia + water-ice-cloud atmosphere are measured (Matthews
2026), so the core Decisions rows are canonical-aligned; the exact tint,
band morphology, rotation, obliquity, and the ring are within-window
tie-breaks defaulting to the cold-giant interesting-first reading. No
ring is observed; the cfg default is `ring_present = false`, with the
icy ring preserved as a cfg variant in Open items.

## Decisions

Kopernicus / atmosphere cfg-ready values. `Confidence`: high = directly
measured or tightly constrained, medium = theoretical with strong
support, low = aesthetic choice within the allowed window.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | high | 20.9 AU orbit around a 0.78 M☉ star — tidal-damping timescale ≫ age of the system; no spin–orbit coupling possible |
| `obliquity_deg` | 27 | low | Tie-break: no measurement. Saturn-analog 26.7° picked over Jupiter's 3.1° for a visually distinct axis tilt; consistent with the optional icy-ring axis. Within the dynamical window for a wide-orbit giant |
| `eccentricity` | 0.244 (+0.11/−0.083) | high | Matthews et al. 2026 — orvara joint fit (imaging + Hipparcos–Gaia acceleration + RV); ~1.9σ lower than Feng 2025; correlated with a (incomplete phase coverage) |
| `argument_of_periapsis_deg` | 62 (+48/−27) | high | Matthews et al. 2026 (DB curated, recommended) |
| `inclination_deg` | 102.3 (+1.9/−1.7) | high | Matthews et al. 2026 — two JWST epochs double the inclination precision |
| `longitude_of_ascending_node_deg` | 44.6 ± 1.3 | high | Matthews et al. 2026 |
| `sidereal_period_yr` | ~108 (+49/−25) | high | Matthews et al. 2026 derived (DB period_days 39447); near-circular solutions with a ≈ 19 AU also allowed. Supersedes the Feng 2019 ~45 yr |
| `semi_major_axis_au` | 20.9 (+5.8/−3.3) | high | Matthews et al. 2026 (Phase 2 recommended); supersedes Feng 2019 (11.6 AU) and Feng 2018 (12.8 AU). a–e degeneracy from ~30 yr RV over a ~108 yr orbit |
| `mass_mjup` | 7.6 ± 0.7 | high | Matthews et al. 2026 — orvara dynamical (true) mass, 7.63 (+0.73/−0.70) M_Jup; supersedes Feng 2019 (~3.25 M_Jup astrometric) and Feng 2018 (M sin i ~2.7 M_Jup) |
| `mass_mearth` | 2425 ± 232 | high | DB curated (= 7.63 M_Jup × 317.8); Matthews et al. 2026 |
| `radius_rjup` | 1.12 | medium | DB radius 12.6 R⊕ = 1.12 R_Jup; typical for a ~7.6 M_Jup, ~3.5 Gyr giant (massive cold giants are near 1 R_Jup; e.g. Matthews 2026 best-fit log g 4.5 implies ~1.1 R_Jup). Not transit-measured |
| `surface_gravity_g_earth` | ~15 | medium | derived from DB M (7.63 M_Jup) and R (12.6 R⊕): g = GM/R² ≈ 1.5 × 10³ cm/s² ≈ 15 g⊕ (log g ≈ 4.18 cgs); Matthews best-fit log g 4.5 is for a smaller-radius model |
| `density_g_cc` | ~5.3 | medium | derived: 7.63 M_Jup in a 1.12 R_Jup sphere ≈ 5.3 g/cc — a massive, compact, mature giant (cf. Jupiter 1.33 g/cc); reflects the high mass at near-Jupiter radius |
| `insolation_s_earth` | 0.00055 | high | derived: S = L_star / a² = 0.239 L☉ (Feng 2019) / (20.9 AU)² ≈ 5.5 × 10⁻⁴ S⊕ — negligible; the planet is not insolation-heated |
| `equilibrium_temp_k_a0` | ~43 | high | derived: T_eq = 278.3 × (L/a²)^0.25 = 278.3 × 0.239^0.25 / √20.9 ≈ 43 K (A = 0); ~39 K at A = 0.3. At periastron (15.8 AU) ~49 K, apastron (26 AU) ~38 K |
| `effective_temp_k` | ~275 | high | Matthews et al. 2024, 2026 — JWST photometry + cloudy atmosphere fit (~250–300 K); the planet's actual radiating temperature, dominated by internal heat (a 7.6 M_Jup giant contracting at ~3.5 Gyr), ~230 K above its ~43 K equilibrium |
| `bond_albedo` | 0.35 | low | Tie-break: at ~275 K with thick water-ice + ammonia clouds, a high cloud albedo near Saturn's (0.34) is appropriate; aesthetic within the no-direct-measurement window |
| `atmosphere_present` | true | high | gas giant; H₂/He bulk with measured NH₃ and inferred H₂O-ice clouds (Matthews 2026) |
| `atmosphere_reference_pressure_pa` | 100000 | medium | gas giant has no solid surface; 1 bar cfg reference for cloud-deck rendering. Note the water-ice cloud τ = 1 sits near 0.7 bar (Matthews 2026 best-fit) |
| `atmosphere_composition` | H₂/He bulk; **confirmed NH₃** (shallower than cloud-free models); thick H₂O-ice clouds; elevated metallicity (~3× solar) and C/O (~2.5× solar) in the best-fit cloudy model | high (NH₃, clouds) / medium (mixing ratios) | Matthews et al. 2026 — NH₃ from F1065C–F1140C = 0.88 mag (11σ); H₂O-ice clouds the preferred explanation for the shallow feature + 3–5 µm faintness; [M/H] and C/O from the PICASO/Virga best fit |
| `atmosphere_scale_height_km` | ~25 | medium | derived: H = kT/(μ m_H g) with T = 275 K, μ = 2.3, g ≈ 15 m/s²-equivalent (≈ 150 m/s²) → ~25 km |
| `atmosphere_tint_rgb_hex` | `#b8bcb0` (muted pale grey-green limb, cold methane/ammonia class) | low | Tie-break: cold (~275 K) water-ice + ammonia clouds give a pale, desaturated cast — NOT warm Jovian amber. Modeled on the WISE 0855 analog (Matthews 2026: near-identical mid-IR color); K5 V illumination adds a faint warm bias |
| `cloud_cover_fraction` | 0.95 | medium | Matthews et al. 2026 — thick, optically very deep (τ ~416) water-ice clouds; near-complete coverage best matches the suppressed ammonia feature + 3–5 µm faintness (uniform cover, vs WISE 0855's possible patchy holes) |
| `cloud_morphology` | thick, near-global water-ice cloud deck (τ = 1 near 0.7 bar) over a confirmed-ammonia atmosphere; faint zonal banding at most; suppresses the NH₃ feature and the near-IR emission | medium | Matthews et al. 2026 — PICASO/Virga best fit: 275 K, log g 4.5, 3× solar [M/H], 2.5× solar C/O, f_sed 6, H₂O column optical depth ~416 |
| `cloud_tint_rgb_hex` | `#dfe2dc` (pale icy off-white — H₂O-ice + NH₃ under K5 V light) | low | Tie-break: water-ice + ammonia clouds are intrinsically near-white with a faint cold-blue cast; the warm K5 V (4700 K) illumination shifts the perceived hue to a neutral pale off-white, distinct from Jupiter's cream-amber |
| `planet_disk_tint_rgb_hex_primary` | `#dfe2dc` (pale off-white deck — dominant appearance) | low | downstream of `cloud_tint_rgb_hex`; a muted, pale cold giant |
| `planet_disk_tint_rgb_hex_accent` | `#b8bcb0` (faint grey-green band shadows where the deck thins) | low | Tie-break: minimal belt–zone contrast under weak convective drive at 275 K; the cold giant reads nearly featureless, far more uniform than Jupiter |
| `rotation_period_hours` | 10 | low | Tie-break: no rotation measurement. Jupiter-analog ~10 h picked over slower Saturn/Uranus values; a massive giant's angular-momentum budget favors rapid rotation. Within-window, not constrained |
| `ring_present` | false | medium | No ring observed in any JWST/MIRI epoch (Matthews 2024, 2026); cfg default is no ring. An icy ring is preserved as an optional cfg variant — see Open items |
| `ring_observed` | false | high | Matthews et al. 2024/2026 JWST/MIRI imaging shows the planet as a bright point source with no resolved ring component |
| `magnetic_field_strength_microtesla_equator` | 3200 | low | Energy-flux dynamo scaling (Christensen et al. 2009 `2009Natur.457..167C`; Reiners & Christensen 2010 `1007.1514`): B_dip^pol = 9 G·(age/4.5 Gyr)^−0.33·(M/M_Jup)^0.93 → for 7.6 M_Jup at ~3.5 Gyr, B_eq ≈ 3200 µT (range 2600–3700). Near the brown-dwarf boundary, so the field stays strong despite the older age (the mass exponent is extrapolated above its 1–5 M_J calibration → extra ~25% systematic). Supersedes the prior ad-hoc "2× Jupiter". See docs/reference/planetary-dynamo-scaling.md |
| `magnetic_dipole_moment_normalized_earth` | 200000 | low | 3200 µT × (1.12 R_Jup)³ vs Jupiter (4.5 G equatorial, 20 000× Earth) → ≈ 2×10⁵ × Earth via energy-flux scaling (`1007.1514`); R³-sensitive → low conf |
| `aurora_present` | false | medium | The host's quiet stellar wind (log R'HK = −4.72) at 20.9 AU delivers a very weak plasma driver; unlike the active-host jovians, no strong aurora is expected. cfg renders none |
| `companion_to_brown_dwarf_pair` | ε Indi B (Ba T1–1.5 66.9 M_Jup + Bb T6 53.3 M_Jup) at ~1459 AU | high | Chen et al. 2022 — the wide brown-dwarf-pair component of the hierarchical triple; not the planet's host but part of its sky |
| `star_apparent_angular_diameter_deg` | 0.018 | high | derived: 2 R_star / a = 2 × 0.713 R☉ / 20.9 AU × (180/π) ≈ 1.1 arcmin ≈ 0.018°; about 1/30 the Sun's angular size from Earth |
| `stellar_illumination_color_temp_k` | 4700 | high | inherited from host Phase 3 (`docs/phase3/eps-ind-a.md`) |

## Surface synthesis

ε Indi A b has no solid surface — it is a ~7.6 M_Jup H₂/He super-Jupiter.
The "surface" relevant for rendering is the cloud deck, and ε Indi A b's
deck is the defining science result: a thick water-ice cloud layer
reaching τ = 1 near 0.7 bar (Matthews 2026 best fit), sitting over an
atmosphere with confirmed ammonia.

The temperature regime is the key to the palette. The planet radiates at
~275 K (Matthews 2024/2026), but this is **not** an insolation
temperature — at 20.9 AU around a 0.239 L☉ star the radiative-equilibrium
temperature is only ~43 K (derived), and the insolation is ~5.5 × 10⁻⁴
that of Earth. The ~275 K is set by the planet's own internal heat: a
7.6 M_Jup giant at ~3.5 Gyr is still slowly contracting and radiating its
formation energy, so it glows ~230 K hotter than its surroundings. This
makes ε Indi A b a **self-luminous cold giant**, in the same regime as
the cold brown dwarf WISE 0855 (~285 K), which Matthews 2026 found has a
near-identical mid-IR color.

At ~275 K the condensation chemistry is dominated by water ice and
ammonia rather than the silicate/iron clouds of hot giants. Ammonia is
confirmed in the gas phase (Matthews 2026), and the preferred
explanation for its anomalously shallow feature is that thick water-ice
clouds blanket the atmosphere and suppress it. The cfg therefore renders
ε Indi A b as a **muted, pale methane/ammonia-class giant** — water-ice
and ammonia clouds are intrinsically near-white with a faint cold-blue
cast, and under the warm K5 V (4700 K) illumination the perceived hue
settles to a neutral pale off-white (`#dfe2dc` cloud, `#b8bcb0` limb).
This is deliberately distinct from the warm cream-amber of a
solar-illuminated Jupiter or of a younger/warmer jovian: ε Indi A b is a
cold, desaturated world.

Belt–zone contrast is rendered as minimal. The convective drive at
~275 K with a near-global thick cloud deck is weak, and the suppressed
ammonia feature and 3–5 µm faintness both point to a uniform, optically
deep cover rather than a banded, gappy one (Matthews 2026 contrast ε Indi
A b's likely uniform cover with WISE 0855's possible patchy holes). The
cfg picks a near-featureless deck (`cloud_cover_fraction ≈ 0.95`) with
only faint grey-green band shadows (`#b8bcb0`) where the deck thins — far
more uniform than Jupiter's vivid belts.

## Atmosphere synthesis

**Pressure reference.** A gas giant has no solid surface; the cfg
reference pressure is 1 bar (100 000 Pa). The physically meaningful level
is the water-ice cloud top: Matthews 2026's best-fit cloudy model reaches
optical depth τ = 1 near 0.7 bar, so the visible "surface" of ε Indi A b
is the cloud deck a little above the 1 bar level.

**Composition.** The bulk is H₂/He, as for any giant. The measured
components are: **ammonia (NH₃), confirmed at 11σ** from the
F1065C–F1140C = 0.88 ± 0.08 mag color (Matthews 2026) — making this the
coldest planet with an ammonia detection — and **thick water-ice
clouds**, the preferred explanation for the shallower-than-expected
ammonia feature and the faint 3–5 µm emission. The best-fit cloudy
atmosphere has elevated metallicity (~3× solar) and an elevated C/O ratio
(~2.5× solar), which Matthews 2026 note remains a challenge for formation
models for a planet this massive. Two alternative explanations for the
shallow ammonia feature were considered and disfavored: a low-metallicity
atmosphere (rejected because it would brighten the 3–5 µm flux above the
ground-based upper limits) and an 85–95% nitrogen depletion (possible but
more extreme than formation models predict). The cfg encodes the
confirmed ammonia and the water-ice clouds with high confidence and the
exact mixing ratios at medium confidence.

**Sky appearance from a cloud-top / moon observer.** From the cloud tops
the sky is a thick, pale icy overcast — near-uniform off-white with
little banding, lit by a small, distant, warm orange-amber star. ε Indi A
subtends only ~1.1 arcmin (0.018°) at 20.9 AU, about 1/30 the Sun's
angular size from Earth — a brilliant orange-amber pinpoint, not a disk.
The light is weak (~5.5 × 10⁻⁴ Earth's insolation), so the dayside is
dim; most of the planet's energy comes from within. Far across the sky,
at ~1459 AU, the brown-dwarf pair ε Indi B (Ba + Bb) hangs as two faint
deep-red T-dwarf points — a striking, if dim, pair of "stars" unique to
this system.

**Nightside.** No meaningful stellar illumination. The planet's own
internal flux keeps the cloud tops at ~275 K, radiating in the
mid-infrared (peak ~10 µm) — invisible to the eye but exactly the band in
which JWST/MIRI detected it. There is no expected visible aurora: the
host's quiet stellar wind at 20.9 AU is a very weak plasma driver, unlike
the active-host jovians in the catalog.

## Rotation & spin synthesis

No rotation measurement of ε Indi A b exists. The angular separation from
the host (~3.65 arcsec, Matthews 2026) is wide and the planet is bright in
the mid-IR, so a future high-resolution Doppler-broadening measurement
(the Snellen 2014 β Pic b technique) is conceivable, but none has been
made.

**Tidal damping argument.** At 20.9 AU around a 0.78 M☉ star, the tidal
timescale for a Jupiter-class planet exceeds the age of the system by many
orders of magnitude. ε Indi A b is **not** tidally locked; the cfg sets
`tidally_locked = false`.

**Rotation period choice.** Among Solar System giants, rotation period
scales weakly with mass and a massive giant inherits a large
angular-momentum budget from disk accretion. The cfg picks a Jupiter-analog
`rotation_period_hours = 10` — a within-window tie-break, not constrained
by any measurement. A ~10 h rotation on a ~7.6 M_Jup giant produces strong
Coriolis banding in principle, but at ~275 K with a thick uniform cloud
deck the visible band contrast is suppressed (see Surface).

**Obliquity.** Tie-break aesthetic. The cfg picks 27° (Saturn-analog) for
a visually distinct axis tilt that also reads naturally with the optional
icy ring; Jupiter's near-zero 3.1° would be less interesting and Uranus's
extreme tip is unmotivated. With the ~108 yr orbital period and weak
insolation, obliquity drives no observable seasonal effect — the planet's
energy budget is internal.

**KSP implementation note.** Rotation period = 10 h = 36 000 s
(`rotationPeriod = 36000`); obliquity ≈ 27° from the orbital normal.

## Visual styling

Combining the surface (cloud-deck) and atmosphere decisions, ε Indi A b
renders as a cold, muted, pale super-Jupiter — the catalog's coldest and
most desaturated giant:

- **Global appearance.** From orbit, ε Indi A b is a pale off-white disk
  (`#dfe2dc`) about 1.12 R_Jup (~80 000 km) across — slightly larger than
  Jupiter in radius but ~7.6× its mass, hence a dense, compact world. The
  appearance is muted and near-featureless: a thick water-ice cloud deck
  with minimal belt–zone contrast, deliberately distinct from the warm
  cream-amber of a sunlit Jupiter. This is a methane/ammonia-class cold
  giant, modeled visually on the WISE 0855 analog.
- **Cloud-deck detail.** A near-global, optically very deep water-ice
  cloud cover (~95%) with only faint grey-green band shadows (`#b8bcb0`)
  where the deck thins. No vivid storms or Great-Red-Spot analog is
  constrained; cfg picks a calm, uniform deck for the cold,
  weakly-convective regime.
- **Limb haze.** A pale, muted grey-green limb (`#b8bcb0`) — cold
  water-ice + ammonia scattering under the warm K5 V illumination, a thin
  desaturated halo rather than a bright cream limb.
- **Nightside.** No stellar illumination to speak of; the cloud tops glow
  faintly in the mid-IR from internal heat (~275 K) — invisible to the
  eye, dark to a player's view, with no visible aurora.
- **Star in sky.** ε Indi A subtends only ~0.018° (1.1 arcmin) from the
  planet — about 1/30 the Sun's angular size from Earth — a brilliant
  warm orange-amber (K5 V, `#ffb870`) pinpoint, delivering only
  ~5.5 × 10⁻⁴ Earth's insolation. The dayside is dim and cold.
- **Brown-dwarf pair in sky.** At ~1459 AU, ε Indi Ba + Bb (Chen 2022)
  appear as two faint deep-red T-dwarf points — too dim to light the
  planet but a distinctive pair in any wide-field render, marking ε Indi
  A b as part of a hierarchical K-dwarf + super-Jupiter + brown-dwarf-pair
  system.
- **Optional icy ring (artistic — NOT observed).** A Saturn-like icy ring
  is offered as a cfg *variant*, not the default. **No ring has been
  observed** in any JWST/MIRI epoch (Matthews 2024, 2026), and the cfg
  default is `ring_present = false`. The variant is physically plausible —
  a cold (~275 K) giant readily retains a water-ice / ammonia-ice ring
  system — and would render as a pale, faintly bluish-white annulus,
  inclined to match the 27° obliquity. It is preserved in Open items as
  an opt-in, clearly flagged as artistic.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Matthews E. C. et al. 2026** — *A second visit to ε Ind Ab with
  JWST: new photometry confirms ammonia and suggests thick clouds in the
  exoplanet atmosphere of the closest super-Jupiter*, ApJL
  (doi:10.3847/2041-8213/ae5823, [arXiv:2603.08780](https://arxiv.org/abs/2603.08780)). Second JWST/MIRI
  coronagraphic epoch (F1140C, 11.3 µm) + archival data. **Confirms
  ammonia** (F1065C–F1140C = 0.88 ± 0.08 mag, 11σ); the shallow feature is
  best explained by **thick water-ice clouds** (best fit: 275 K, log g
  4.5, 3× solar [M/H], 2.5× solar C/O, H₂O cloud τ = 416, τ = 1 near
  0.7 bar). Re-fit orbit: M = 7.63 (+0.73/−0.70) M_Jup, a = 20.9
  (+5.8/−3.3) AU, e = 0.244 (+0.11/−0.083), i = 102.3°, Ω = 44.6°,
  ω = 62°, P ≈ 108 yr. **Cornerstone paper** — drives the orbit, mass,
  and atmosphere Decisions rows. Phase 2 recommended anchor.
- **Matthews E. C. et al. 2024** — JWST/MIRI direct-imaging discovery of
  ε Indi A b (`2024Natur.633..789M`, [arXiv:2503.01599](https://arxiv.org/abs/2503.01599)). First-epoch
  photometry at 10.6 and 15.5 µm; establishes the ~275 K cold giant, the
  3–5 µm faintness (NaCo non-detection) implying elevated metallicity, and
  the common-proper-motion case. **Cornerstone paper.** (ar5iv full text
  not available in the cache — HTML-only stub; numbers taken from the
  abstract and from Matthews 2026's recap.)
- **Feng F. et al. 2019** — *Detection of the nearest Jupiter analog in
  radial velocity and astrometry data*, MNRAS 490, 5002
  (`2019MNRAS.490.5002F`, doi:10.1093/mnras/stz2912, [arXiv:1910.06804](https://arxiv.org/abs/1910.06804)).
  RV + Hipparcos/Gaia astrometric detection; Phase 2 source for the host
  luminosity (0.239 L☉). The planet parameters here (a ≈ 11.6 AU,
  ~3.25 M_Jup, P ~45 yr) are the pre-JWST values, superseded by Matthews
  2026; retained in the DB as `recommended:false`.

### Read (context / methodology, not decision-driving)

- **Lundkvist M. S. et al. 2024** — *Low-amplitude solar-like
  oscillations in the K5 V star ε Indi A*, ApJ 964, 110
  (`2024ApJ...964..110L`, [arXiv:2403.04509](https://arxiv.org/abs/2403.04509)). Host-star asteroseismic
  mass (0.782 M☉), R (0.713 R☉), Teff (4700 K), and the ~7.1 yr activity
  cycle. Provides the host stellar parameters that set the insolation and
  illumination-color-temperature rows. Detailed in the host Phase 3
  (`docs/phase3/eps-ind-a.md`).
- **Chen M. et al. 2022** — *Precise Dynamical Masses of ε Indi Ba and
  Bb* (`2022AJ....163..288C`, [arXiv:2205.08077](https://arxiv.org/abs/2205.08077)). Dynamical masses of the
  wide brown-dwarf pair (Ba T1–1.5 66.9 M_Jup, Bb T6 53.3 M_Jup at
  ~1459 AU) and the system activity-age (~3.5 Gyr) that frames ε Indi A b
  as a "solar-age" giant. Drives the brown-dwarf-pair context row.
- **Feng F. et al. 2018** — *Detection of the closest Jovian exoplanet in
  the ε Indi triple system* (`2018arXiv180308163F`, [arXiv:1803.08163](https://arxiv.org/abs/1803.08163)).
  RV discovery preprint; earliest planet parameters (M sin i ~2.7 M_Jup,
  a ~12.8 AU), superseded by Feng 2019 / Matthews 2026; retained in the
  DB as `recommended:false`.

### Read (instrument-only, not visual-informative)

- The JWST/MIRI coronagraphic reduction (spaceKLIP / pyKLIP RDI,
  four-quadrant phase mask, glow-stick background subtraction) and the
  orvara orbit-fit machinery in Matthews 2026 are the instrument backbone
  of the photometry and the mass but contribute no direct visual field
  beyond the numbers used above. The PICASO/Virga cloudy-atmosphere
  modeling supplies the cloud τ and best-fit parameters already cited.

### Not read — no arXiv preprint or low-priority (~handful)

The Sonora Flame Skimmer / Elf Owl / Bobcat model grids and the WISE 0855
cooling-model references (Mukherjee 2024; Marley 2021; Kühnle 2025) cited
inside Matthews 2026 are read for context but contribute no ε-Indi-A-b
cfg number beyond the best-fit parameters already used. Upcoming JWST
3–20 µm spectroscopy (GO #8438, #8714) is not yet published. No further
papers were fetched for this planet beyond the pinned set.

## Open items for follow-up

- **JWST 3–20 µm spectroscopy (GO #8438, #8714).** Upcoming JWST
  observations should resolve whether the shallow ammonia feature is from
  water-ice clouds, low metallicity, or nitrogen depletion, and pin the
  metallicity, C/O, and cloud f_sed. If a spectrum arrives, re-derive
  `atmosphere_composition`, `cloud_morphology`, `bond_albedo`, and the
  tint hex codes.
- **Icy-ring cfg variant (artistic).** The default is `ring_present =
  false` — no ring is observed (Matthews 2024/2026). An optional pale
  icy-ring variant is preserved here for users who want it: physically
  plausible for a cold ~275 K giant, rendered as a faint bluish-white
  annulus inclined to the 27° obliquity. Clearly flagged as artistic,
  not data-driven.
- **a–e degeneracy.** With ~30 yr of RV over a ~108 yr orbit, the
  semi-major axis and eccentricity are strongly correlated (Matthews
  2026); near-circular solutions with a ≈ 19 AU are also allowed.
  Continued monitoring (Rajpoot et al. in prep.) will tighten both; the
  cfg should be updated if the orbit is refined.
- **Rotation and obliquity.** Both are within-window tie-breaks (10 h,
  27°). A future Doppler-broadening measurement at the ~3.65 arcsec
  separation would replace the rotation guess; obliquity is unlikely to be
  measured soon.
- **Effective vs equilibrium temperature.** The cfg encodes both the
  measured ~275 K effective temperature (internal-heat-dominated) and the
  derived ~43 K radiative-equilibrium temperature. A future cfg should
  drive the planet's thermal glow from the ~275 K internal value, not the
  insolation, to render the self-luminous cold giant faithfully.
- **Phase 2 atmosphere ingest.** ε Indi A b has no Phase 2 atmosphere
  block in the DB (only orbital + physical). When the schema is extended,
  the Matthews 2026 ammonia detection and water-ice-cloud best-fit should
  be ingested as `atmosphere_measurements` records matching the cfg picks
  above.

## Related

- [eps-ind-a](eps-ind-a.md) — host star Phase 3 synthesis; provides the
  K5 V M_star / R_star / L_star / age and the illumination-color-temperature
  reference, and the brown-dwarf-pair context
- [eps-eri-b](eps-eri-b.md) — comparison cold jovian around a nearby K
  dwarf (~0.78 M_Jup, 3.5 AU, ~110 K); contrast ε Eri b's lower-mass,
  insolation-set warm-cream Saturn-analog against ε Indi A b's massive,
  internal-heat-dominated, water-ice-cloud cold giant
- [methodology](../reference/methodology.md) — Decisions schema
- [mod-reference](../reference/mod-reference.md) — downstream Kopernicus /
  EVE / Scatterer cfg writers consuming this giant's atmosphere decisions
- [rex-data-comparison](../reference/rex-data-comparison.md) — REX has no
  entry for ε Indi A b; the nearest directly-imaged cold super-Jupiter is
  a NearStars-exclusive Phase 3 addition
