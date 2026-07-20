<!-- 40 Eridani A c Phase 3 synthesis: fully synthetic NS system-completion body (Mercury-analog filler) — no real detection -->
# 40 Eridani A c — Phase 3 Synthesis (Synthetic — NS system-completion body)

40 Eridani A c is a **fully invented planet**. There is no detection,
no candidate signal, and no literature claim behind it — it exists
because the NearStars Phase 4 board wanted a dynamically plausible
filler between the culturally-mandated b ("Vulcan"/"Erid", itself a
refuted detection kept as a documented divergence) and the *Project
Hail Mary* Threeworld analog at d. Every physical row below is a
design value, not a measurement, and the entire body is flagged
`method: theoretical` in `db/planets_curated.json`.

What *is* grounded is the dynamics. The orbit (a = 0.4 AU,
e = 0.04, P = 104.62 d) was chosen and then validated with a REBOUND
stability integration of the full three-planet system around the
0.78 M☉ K0.5 V primary: 10⁵ yr with WHFast, relative energy error
4.6×10⁻¹¹, MEGNO = 2.00 (regular, non-chaotic), all three bodies
judged stable with calm eccentricity evolution
(`phase3/stability-sim/results/40_eridani_summary.json`). The orbit
sits near a 3:1 period ratio outside b and near 2:1 interior to d —
close to, but deliberately not inside, the resonances.

The physical design is a **Mercury analog**: 0.055 M⊕ and 0.38 R⊕
are Mercury's own mass and radius to two digits, which makes the
derived density (~5.5 g/cc), surface gravity (0.38 g), and escape
velocity (4.3 km/s) land on Mercury's values automatically. At
0.4 AU around the 0.408 L☉ primary the insolation is 2.5 S⊕ —
warmer than Mercury-at-aphelion, cooler than Mercury-at-perihelion —
so the Mercury reading is self-consistent: an airless, baked,
cratered bare-rock world. Per the physical-plausibility gate this is
**not** a lava world (equilibrium temperature ~352 K is nowhere near
the silicate solidus, and no interior-heating mechanism applies).

**Scenario choice for NearStars: a Mercury-analog airless rock in a
3:2 spin–orbit resonance — heavily cratered basalt-gray regolith
with a faint sodium exosphere, baked on the dayside and frozen on
the night side, under the orange light of the K0.5 V primary.**

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `disposition` | Synthetic (NS system-completion filler; no detection) | high | The one high-confidence row: this body is invented. DB entry is `method: theoretical` with the design rationale in the reference string |
| `mass_mearth` | 0.055 | low | design value — Mercury's mass, chosen so all derived quantities inherit Mercury's tested self-consistency |
| `radius_rearth` | 0.38 | low | design value — Mercury's radius, paired with the mass above |
| `density_g_cc` | ~5.5 | low | derived M/R³ — Mercury-like iron-rich rock |
| `surface_gravity_g_earth` | ~0.38 | low | derived 0.055/0.38² |
| `equilibrium_temp_k` (A=0.3) | 322 | low | derived; (A=0) 352, (A=0.088 Mercury albedo) 344 |
| `insolation_s_earth` | ~2.55 | low | derived 0.4078 L☉ / (0.4 AU)² |
| `surface_temp_k` | ~490 dayside peak / ~100 night | low | airless slow-rotator regime: substellar ≈ √2 × Teq at Mercury albedo; Mercury-analog day–night contrast |
| `bond_albedo` | 0.088 | low | Mercury's Bond albedo — dark space-weathered basaltic regolith |
| `tidally_locked` | false (3:2 spin–orbit resonance) | low | tie-break: at e = 0.04 tidal despinning favors resonance capture over pure 1:1; Mercury precedent adopted whole |
| `rotation_period_h` | 1674 (= 2/3 × 104.62 d) | low | follows from the 3:2 resonance pick |
| `atmosphere_composition` | none (trace Na exosphere) | low | v_esc 4.3 km/s at ~350 K retains nothing; sodium exosphere is the Mercury-analog flourish |
| `atmosphere_surface_pressure_pa` | 0 | low | airless |
| `surface_tint_rgb_hex` | `#8d8781` (space-weathered basalt gray) | low | tie-break: Mercury regolith tone, warmed slightly under the K0.5 V (5143 K) illuminant |
| `sky_tint_rgb_hex` | `#000000` (airless black) | low | no atmosphere, no sky color |

## Surface synthesis

The surface is designed, not observed, so the synthesis job here is
self-consistency rather than literature reconciliation. Adopting
Mercury's mass and radius wholesale buys a physically tested package:
an iron-rich ~5.5 g/cc interior, 0.38 g surface gravity, and a
4.3 km/s escape velocity that guarantees airlessness at this
temperature. The design deliberately avoids inventing novel physical
parameters that would each need separate justification.

**Thermal regime — baked rock, not lava.** At 2.55 S⊕ the
equilibrium temperature is ~352 K (zero albedo) and the substellar
dayside peak in the slow-rotation airless regime is ~490 K — hot
enough to bake, two full regimes short of the ~1300 K silicate
solidus. The physical-plausibility gate therefore forces the bare-rock
reading; a lava or magma-pond rendering would be indefensible for
this body and is explicitly excluded.

**Cratered Mercury-analog terrain.** With no atmosphere and no
interior heating mechanism, the surface record is impact-dominated:
heavy cratering, lobate scarps from global thermal contraction
(Mercury's signature tectonic form at this mass), and space-weathered
regolith darkened to a Bond albedo of ~0.09. The 1.8 Gyr system age
(Bond 2017 IFMR, adopted in the host synthesis) means somewhat fewer
craters than 4.5-Gyr Mercury, a note for the texture pass rather than
a cfg field.

**Day–night contrast.** The 3:2 resonance gives a solar day of two
orbital periods (~209 d), so each hemisphere bakes for months and
then freezes for months — Mercury's extreme thermal cycling,
reproduced at slightly higher insolation.

## Atmosphere synthesis

There is nothing to synthesize: at 4.3 km/s escape velocity and
~350–490 K dayside temperatures, thermal (Jeans) escape strips any
degassed volatile inventory on geologically short timescales, exactly
as on Mercury. The cfg sets zero surface pressure.

**Sodium exosphere as the one flourish.** Mercury maintains a
tenuous, optically negligible sodium exosphere sputtered off the
regolith by solar wind and micrometeorites; the same mechanism works
here under the K-dwarf wind. It is recorded in the composition row as
flavor — it has no pressure, no visual thickness, and no cfg
rendering beyond a possible faint emission note in a future art pass.

## Rotation & spin synthesis

At a = 0.4 AU around 0.78 M☉ the tidal despinning timescale is short
enough (small body, close orbit) that the primordial spin is gone —
unlike b at 0.224 AU whose synthesis picked a free rotator on
lock-timescale grounds, c's smaller mass and the 1.8 Gyr age put it
in the despun regime. The end state at e = 0.04 is then either
synchronous 1:1 or a spin–orbit resonance.

**Interesting-first pick: Mercury's 3:2.** With a nonzero design
eccentricity, capture into the 3:2 spin–orbit resonance is the
Mercury-precedent outcome, and it is the more visually interesting
one — every point on the surface gets both day and night, the
terminator migrates, and the thermal cycling drives the
baked/frozen contrast above. The rotation period is exactly 2/3 of
the 104.62-d orbital period (~69.7 d, 1674 h).

## Visual styling

- **Global appearance.** A gray, heavily cratered Mercury-analog
  (`#8d8781` base tint) with sharp airless shadows and a crisp
  terminator, lit noticeably orange by the 5143 K K0.5 V primary —
  the same illuminant shift that warms the whole 40 Eri A system
  palette relative to Sol.
- **No atmosphere effects.** Black sky (`#000000`), no limb haze, no
  scattering — the rendering contrast to its two neighbors is the
  point: b is a thick-hazed hot super-Earth, d is a thin-atmosphere
  frost world, c is the airless control between them.
- **Sky companions.** As everywhere in the 40 Eri system, the
  white-dwarf B / red-dwarf C pair (~400 AU out) appear as brilliant
  point companions in the black sky.
- **Texture-pass notes.** Lobate scarps, ray craters, and slightly
  reduced crater density vs Mercury (1.8 Gyr vs 4.5 Gyr surface age).

## Canonical alternatives

**The canonical reading is no planet.** Unlike b (a real, refuted
detection) there has never been any observational claim at this
period — c is pure system-completion design. The canonical 40
Eridani A system in current catalogs contains zero confirmed planets;
NearStars renders b, c, and d as a documented-divergence ensemble for
gameplay variety and the *Star Trek* / *Project Hail Mary* cultural
anchors.

| Reading | System content | Status |
|---|---|---|
| Canonical catalogs (2026) | no confirmed planets around 40 Eri A | observation |
| **cfg pick** | b (refuted, cultural) + c (synthetic filler) + d (PHM Threeworld) | documented divergence (design) |

## Bibliography

There is no discovery or characterization literature for an invented
body; the bibliography records the grounding used for the host
parameters, the dynamics validation, and the design method.

### Read (host + dynamics grounding)

- **[Boyajian et al. 2012](https://arxiv.org/abs/1208.2431)** —
  CHARA interferometric radius/Teff/luminosity of 40 Eridani A; the
  0.4078 L☉ that sets c's insolation and temperature rows.
- **[Bond et al. 2017](https://arxiv.org/abs/1709.00478)** —
  IFMR-derived system-coeval age (~1.8 Gyr) used in the surface-age
  and despinning arguments.
- **NearStars stability run** —
  `phase3/stability-sim/results/40_eridani_summary.json`: REBOUND
  WHFast, 10⁵ yr, energy error 4.6×10⁻¹¹, MEGNO 2.00, all bodies
  stable/calm (c's eccentricity oscillates 0.040–0.095, bounded).

### Method references

- Mercury-analog package (mass, radius, albedo, 3:2 resonance) —
  standard solar-system values adopted wholesale as the design
  baseline; textbook-level, no paper citation required per the
  derived-value grounding policy's textbook exception.
- Airless dayside/nightside temperature regime — same slow-rotator
  substellar formula used across NearStars airless bodies
  (`docs/reference/methodology.md`).

## Open items for follow-up

- **Everything is design.** No future observation is expected to
  constrain this body (it does not exist); rows will only change if
  the Phase 4 board revises the design intent.
- **Resonance proximity is deliberate but worth re-checking on
  touch.** The near-3:1 (with b) and near-2:1 (with d) spacings were
  validated at 10⁵ yr; if any neighbor's orbit is redesigned, re-run
  the stability sim before accepting new elements.
- **Eccentricity bound note.** The DB reference string says
  "e ≤ 0.05"; the 10⁵-yr integration shows c's eccentricity cycling
  up to ~0.095 under secular forcing (still calm/stable). The
  osculating design value stays 0.04; the wider secular envelope is
  recorded here for honesty.

## Related

- [40-eridani-a](40-eridani-a.md) — host star Phase 3 (K0.5 V)
- [40-eridani-a-b](40-eridani-a-b.md) — inner neighbor ("Vulcan"/
  "Erid", refuted detection kept as documented divergence)
- [40-eridani-a-d](40-eridani-a-d.md) — outer neighbor (*Project Hail
  Mary* Threeworld analog)
- [methodology](../reference/methodology.md) — Decisions schema +
  airless thermal regime
