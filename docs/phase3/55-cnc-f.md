<!-- 55 Cnc f Phase 3 synthesis: cfg-ready decisions and reasoning -->
# 55 Cnc f — Phase 3 Synthesis

55 Cnc f is the system's temperate giant: a ~0.15 M_Jup
(M sin i ≈ 48.5 M⊕, Moutou 2025) gas/ice giant on a 260.6-day,
eccentric (e ≈ 0.063) orbit at 0.802 AU around 55 Cnc A. Discovered by
Fischer et al. 2008, it is the planet von Braun et al. 2011 singled out
as the system's **habitable-zone planet**: it "spends the majority of
the duration of its elliptical orbit in the circumstellar habitable
zone (0.67–1.32 AU) where, with moderate greenhouse heating, it could
harbor liquid water." It does not transit, so there is no measured
radius; for a sub-Saturn-mass giant a radius near ~0.7 R_Jup is the
standard estimate. With the host luminosity L = 0.582 L☉, its
equilibrium temperature derives to T_eq(A=0) ≈ 271 K — genuinely
temperate, swinging from ~263 K at apastron to ~280 K at periastron
across the eccentric orbit.

**Scenario choice for NearStars: a temperate gas/ice giant
(~0.15 M_Jup, ~270 K) that grazes the habitable zone, rendered as a
cool banded giant with the possibility of water-ice cloud decks (the
coldest banded condensates of the system's inner giants), under the
yellow-orange light of its K0 host.** Mass is Msini (RV), radius is an
estimate-only sub-Saturn value; the cfg flags both. f is itself a gas
giant, so its HZ residence is of interest only for hypothetical
moons.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | high | 260.6 d orbit at 0.802 AU; far outside any tidal-locking regime |
| `obliquity_deg` | 0 | low | Tie-break: assumed low; unconstrained |
| `eccentricity` | 0.063 | medium | Moutou 2025 (Bourrier 2018 gives 0.08; ±0.048) |
| `argument_of_periastron_deg` | 100 | low | raw NASA Archive value |
| `sidereal_period_days` | 260.58 | high | Moutou 2025 (Phase 2 recommended; Bourrier 2018 259.88 agrees) |
| `semi_major_axis_au` | 0.802 | high | Moutou 2025 (Phase 2 recommended; Bourrier 2018 0.7708) |
| `inclination_deg` | ~89.7 (unconstrained, ±24°) | low | raw value; non-transiting |
| `mass_mearth` | 48.5 (M sin i) | high | Moutou 2025 — RV minimum mass (Phase 2 recommended; Bourrier 2018 47.8) |
| `mass_type` | Msini | high | Moutou 2025 — radial-velocity minimum mass; non-transiting |
| `mass_mjup` | 0.15 (M sin i) | high | derived = 48.5 / 317.8 |
| `radius_rjup` | ~0.7 (estimate only) | low | No measured radius (non-transiting); sub-Saturn estimate at ~0.15 M_Jup, ~270 K, read off the warm-giant mass-radius-insolation tracks of Fortney, Marley & Barnes 2007 (`astro-ph/0612671`) |
| `equilibrium_temp_k` (A=0) | 271 | high | derived: 278.3·0.582^0.25/√0.802 |
| `equilibrium_temp_k` (A=0.3) | 248 | high | derived, Jovian-analog albedo |
| `equilibrium_temp_k_periastron` (A=0) | 280 | high | derived at a(1−e) = 0.752 AU |
| `equilibrium_temp_k_apastron` (A=0) | 263 | high | derived at a(1+e) = 0.853 AU |
| `insolation_s_earth` | 0.9 | high | derived = L / a² = 0.582 / 0.802² (≈ Earth-like) |
| `bond_albedo` | 0.3 | low | Tie-break: cloudy temperate giant, Jupiter/Saturn-like albedo |
| `atmosphere_present` | true | high | gas/ice giant — H/He envelope |
| `atmosphere_reference_pressure_pa` | 100000 | medium | gas giant — no solid surface; 1 bar cfg reference for cloud-deck rendering |
| `atmosphere_composition` | H₂/He with NH₃ / NH₄SH / possible H₂O-ice cloud decks | medium | ~270 K — cold enough for ammonia and (deeper) water-ice condensates, like the Solar System giants |
| `cloud_cover_fraction` | 0.9 | medium | banded gas-giant cloud decks |
| `cloud_morphology` | zonal banding; ammonia + ammonium-hydrosulfide cloud decks (Jupiter/Saturn-analog) with possible deeper water clouds | medium | ~270 K is in the NH₃-cloud regime — the only inner 55 Cnc giant cold enough for white ammonia clouds |
| `cloud_tint_rgb_hex` | `#e8e0d0` (pale cream, NH₃-cloud Jovian) | low | Tie-break: cool temperate-Jovian palette — paler and whiter than the warm inner giants |
| `atmosphere_tint_rgb_hex` | `#dde4ec` (pale cool-blue limb haze) | low | Tie-break: cool ~270 K limb, Rayleigh-tinged |
| `star_apparent_angular_diameter_deg` | 0.63 | high | derived: 2·R★/a = 2·0.943 R☉ / 0.802 AU |
| `stellar_illumination_color_temp_k` | 5196 | high | von Braun 2011 stellar Teff |

## Surface synthesis

55 Cnc f is a sub-Saturn-mass gas/ice giant with no surface; this
section covers the cloud-top "surface". At T_eq ≈ 271 K it is
**genuinely temperate** — the coldest of the four inner giants and the
only one in the regime where ammonia clouds (Jupiter's signature white
clouds) can condense at the visible deck. Its eccentric orbit
(e ≈ 0.063) carries the equilibrium temperature from ~263 K at apastron
to ~280 K at periastron — straddling the water freezing point and
spending most of the orbit inside the von Braun 2011 habitable zone
(0.67–1.32 AU).

The cloud-top palette is therefore pale and cream-white (`#e8e0d0`) —
ammonia-cloud Jovian colors, distinctly cooler and whiter than the warm
tans of b and c. Where ammonium-hydrosulfide (NH₄SH) clouds form they
add tan/orange tints in the belts, as on Jupiter. The cool limb takes
a pale blue Rayleigh tinge (`#dde4ec`). Under the 5196 K yellow-orange
host light the planet reads as a cool, cream-and-tan banded giant —
the most "Jupiter-like" looking world of the inner system.

Morphology: Jupiter/Saturn-analog zonal banding with white ammonia
zones and tan NH₄SH belts. As a temperate giant its banding contrast
and storm activity (great-spot-like vortices, optional) are within the
Solar-System-giant range.

## Atmosphere synthesis

55 Cnc f has a deep H₂/He envelope. At ~270 K the visible condensates
are ammonia ice (NH₃) and, deeper, ammonium hydrosulfide (NH₄SH) and
water — the same cloud chemistry that colors Jupiter and Saturn. This
makes f the one inner 55 Cnc giant with a genuinely Solar-System-like
cloud palette.

- **Pressure / structure.** A continuous H₂/He atmosphere with an
  NH₃-ice cloud deck at the top, NH₄SH below, and deeper water clouds;
  no discrete surface.
- **Composition.** H₂/He primary with NH₃, NH₄SH, and H₂O condensates;
  the super-metal-rich host suggests enhanced heavy-element abundance.
- **Sky appearance.** From the upper atmosphere the sky would be a pale
  cream-blue, with the host star a modest 0.63° disk — only slightly
  larger than the Sun seen from Earth, the most "Sun-like sky" of the
  system's giants.

**Habitable-zone note.** von Braun 2011 highlighted f as the
HZ planet, but f is itself a gas giant — it cannot host surface liquid
water. Its HZ residence matters only for hypothetical large moons,
which could in principle be temperate. No such moon is observed; none
is synthesized here (no fabricated bodies). The HZ residence is
recorded as context, not as a habitability claim for f itself.

## Rotation & spin synthesis

At 0.802 AU on a 260.6-day orbit, 55 Cnc f is far outside any
tidal-locking regime and rotates freely. The orbit is mildly eccentric
(e ≈ 0.063; Moutou 2025). No rotation period has been measured.

**KSP implementation note.** The cfg adopts a fast Jovian rotation
(~10 h order, Jupiter/Saturn-analog) for visual banding. This is a
tie-break; flag as unconstrained.

**Mild seasons.** The e ≈ 0.063 eccentricity gives a periastron-to-
apastron insolation swing (T_eq ~280 K → ~263 K), a real ~6%
temperature variation over the 260-day orbit, but with negligible
obliquity there are no axial seasons.

## Visual styling

- **Global appearance.** A cool, cream-and-tan banded giant at 0.802 AU
  — the most Jupiter-like-looking world of the inner system, grazing
  the habitable zone on its eccentric orbit.
- **Cloud decks.** Jupiter-analog zonal banding: white ammonia zones
  (`#e8e0d0`) and tan NH₄SH belts, with optional great-spot vortices.
- **Limb / haze.** A pale cool-blue Rayleigh-tinged limb (`#dde4ec`),
  cooler-toned than the warm inner giants.
- **Star in sky.** 55 Cnc A subtends only 0.63° — barely larger than
  the Sun seen from Earth — the most Sun-like sky of any 55 Cnc giant.
- **Sister planets in sky.** Planet c (inward at 0.247 AU) appears as a
  warm point; the cold giant d (outward at 5.6 AU) is a faint distant
  point. The distant M-dwarf companion 55 Cnc B (~1065 AU) is a faint
  orange-red second sun far beyond d.
- **Seasonal brightness flicker (optional).** The ~6% insolation swing
  over the eccentric orbit could subtly modulate the cloud brightness
  on the 260-day period — a faithful but minor touch.
- **No rings (default).** f is not the system's ring-candidate body; no
  ring is rendered (the cold giant d carries the optional artistic
  ring).

## Bibliography

### Read (visual-informative, drove decisions above)

- **Moutou C. et al. 2025/2026** — *Characterizing planetary systems
  with SPIRou…*, A&A 705, A190 (`2026A&A...705A.190M`,
  [arXiv:2510.11523](https://arxiv.org/abs/2510.11523)). Latest RV refit: planet f P = 260.58 d,
  a = 0.802 AU, e = 0.063, M sin i = 48.5 ± 2.8 M⊕; confirms f sits in
  the habitable zone between the runaway and maximum-greenhouse limits
  (Hill 2022) and that a temperate Earth-mass planet at 1–2 AU would be
  dynamically stable. **Phase 2 recommended orbit + mass.** Postdates
  the model cutoff — value-checked against the cached text.
- **von Braun K. et al. 2011** — *The 55 Cancri System… Habitable Zone
  Planet…*, ApJ 740, 49 (`2011ApJ...740...49V`, [arXiv:1107.1936](https://arxiv.org/abs/1107.1936)). Host
  L = 0.582 L☉ → the T_eq derivation; identifies f as spending most of
  its eccentric orbit in the HZ (0.67–1.32 AU). **The HZ-residence
  anchor.**

### Read (context / methodology, not decision-driving)

- **Bourrier V. et al. 2018** — `2018A&A...619A...1B`,
  [arXiv:1807.04301](https://arxiv.org/abs/1807.04301). Refit: f at a = 0.7708 AU, e = 0.08,
  M sin i = 47.8 M⊕ — documented-alternative orbit/mass (superseded by
  Moutou 2025).
- **Fischer D. A. et al. 2008** — `2008ApJ...675..790F`. Discovery
  paper for f (0.15 M_Jup at 260 d); historical context.

### Read (instrument-only, not visual-informative)

- **Hill M. L. et al. 2022** — places f within the runaway/maximum-
  greenhouse HZ limits (via Moutou 2025); HZ-geometry context.

### Not read — no arXiv preprint or low-priority (~15 papers)

Dynamical-stability proceedings (Satyal & Cuntz 2019 on the
temperate-planet stability between 1–2 AU) and early RV-refinement
papers. Full filtered bib in `docs/phase3/_bib/55-cnc.yaml`.

## Open items for follow-up

- **Radius.** No measured radius (non-transiting); ~0.7 R_Jup is
  estimate-only. An inclination/true-mass constraint would allow a
  radius refinement.
- **Hypothetical moon.** f's HZ residence is of interest for a large
  moon, but none is observed; per policy no body is fabricated. If a
  moon is ever detected, a temperate-moon Phase 3 follow-up would be
  warranted.
- **Cloud chemistry.** The NH₃/NH₄SH cloud assignment is a temperature-
  based inference; the super-metal-rich host could shift the cloud
  colors. A future emission/transmission constraint would refine the
  palette.

## Related

- [55-cnc](55-cnc.md) — host star (K0 IV-V, L = 0.582 L☉, HZ 0.67–1.32 AU)
- [55-cnc-c](55-cnc-c.md) — inner neighbor (warm Saturn-class giant)
- [55-cnc-d](55-cnc-d.md) — outer neighbor (cold gas giant, ring candidate)
- [methodology](../reference/methodology.md) — Decisions schema and Msini convention
