<!-- 55 Cnc c Phase 3 synthesis: cfg-ready decisions and reasoning -->
# 55 Cnc c — Phase 3 Synthesis

55 Cnc c is a Saturn-class giant on a 44.4-day, mildly eccentric orbit
at 0.247 AU around 55 Cnc A, discovered by McArthur et al. 2004. Its
radial-velocity minimum mass is M sin i ≈ 56.6 M⊕ ≈ 0.18 M_Jup (Moutou
2025) — about Saturn-mass. It does not transit, so there is no measured
radius; for a Saturn-mass giant a radius near ~0.8 R_Jup is the
standard estimate. With the host luminosity L = 0.582 L☉, its
equilibrium temperature derives to T_eq(A=0) ≈ 489 K — a warm
Saturn-class giant, cooler than the inner hot Jupiter b but still well
above the temperate regime.

**Scenario choice for NearStars: a warm Saturn-class gas giant
(~0.18 M_Jup, ~490 K), rendered with banded cloud decks in warm
muted tones under the yellow-orange light of its K0 host.** Mass is
Msini (RV), radius is an estimate-only Saturn-class value; the cfg
flags both accordingly.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | medium | 44.4 d orbit; gas-giant tidal locking timescale far exceeds the system age at 0.247 AU |
| `obliquity_deg` | 0 | low | Tie-break: assumed low; unconstrained |
| `eccentricity` | 0.088 | medium | Moutou 2025 (Bourrier 2018 gives 0.03; large uncertainty ±0.23) |
| `argument_of_periastron_deg` | 31 | low | raw NASA Archive value |
| `sidereal_period_days` | 44.3936 | high | Moutou 2025 (Phase 2 recommended; Bourrier 2018 44.3989 agrees) |
| `semi_major_axis_au` | 0.247 | high | Moutou 2025 (Phase 2 recommended; Bourrier 2018 0.2373) |
| `inclination_deg` | ~89.7 (unconstrained, ±24°) | low | raw value; non-transiting |
| `mass_mearth` | 56.6 (M sin i) | high | Moutou 2025 — RV minimum mass (Phase 2 recommended; Bourrier 2018 51.2) |
| `mass_type` | Msini | high | Moutou 2025 — radial-velocity minimum mass; non-transiting |
| `mass_mjup` | 0.18 (M sin i) | high | derived = 56.6 / 317.8 |
| `radius_rjup` | ~0.8 (estimate only) | low | No measured radius (non-transiting); Saturn-class estimate at ~0.18 M_Jup, ~490 K, read off the warm-giant mass-radius-insolation tracks of Fortney, Marley & Barnes 2007 (`astro-ph/0612671`) |
| `equilibrium_temp_k` (A=0) | 489 | high | derived: 278.3·0.582^0.25/√0.247 |
| `equilibrium_temp_k` (A=0.3) | 447 | high | derived, Jovian-analog albedo |
| `insolation_s_earth` | 9.5 | high | derived = L / a² = 0.582 / 0.247² |
| `bond_albedo` | 0.3 | low | Tie-break: cloudy warm Saturn-class, Jupiter/Saturn-like albedo |
| `atmosphere_present` | true | high | gas giant — H/He envelope |
| `atmosphere_reference_pressure_pa` | 100000 | medium | gas giant — no solid surface; 1 bar cfg reference for cloud-deck rendering |
| `atmosphere_composition` | H₂/He with alkali metals, sulfide/silicate condensate clouds | medium | warm-Saturn chemistry at ~490 K; super-metal-rich host favors enriched metallicity |
| `cloud_cover_fraction` | 0.9 | medium | banded gas-giant cloud decks |
| `cloud_morphology` | zonal banding; sulfide/alkali-salt cloud decks, warmer than Saturn's ammonia clouds but cooler than 55 Cnc b's silicates | medium | ~490 K — between the silicate clouds of b and the NH₃ clouds of Solar System giants |
| `cloud_tint_rgb_hex` | `#d4b890` (warm muted tan) | low | Tie-break: warm-Saturn condensate palette, softer/paler than b's hotter silicate tan |
| `atmosphere_tint_rgb_hex` | `#e0c8a0` (pale warm limb haze) | low | Tie-break: ~490 K Saturn-class limb |
| `star_apparent_angular_diameter_deg` | 2.04 | high | derived: 2·R★/a = 2·0.943 R☉ / 0.247 AU |
| `stellar_illumination_color_temp_k` | 5196 | high | von Braun 2011 stellar Teff |

## Surface synthesis

55 Cnc c is a Saturn-mass gas giant with no surface; this section
covers the cloud-top "surface". At T_eq ≈ 489 K it is a **warm
Saturn-class** world — cooler than the inner hot Jupiter b (708 K) but
still far too warm for ammonia/water-ice clouds. The visible
condensates at this temperature are alkali-metal salts (Na₂S, KCl) and
sulfides, sitting deeper and at higher temperatures than the ammonia
clouds of the Solar System giants.

The cloud-top palette is a warm muted tan (`#d4b890`) — softer and
paler than the hotter silicate-tan of 55 Cnc b, reflecting the
cooler condensate chemistry. The super-solar host metallicity
([Fe/H] ≈ +0.32) again argues for an enriched atmosphere with stronger
alkali absorption and deeper cloud colors. Under the 5196 K
yellow-orange host light, the planet reads as a warm, gently banded
tan giant.

Morphology: zonal banding with somewhat lower contrast than the hotter
b (cooler atmospheres tend toward subtler banding). The cfg renders
Saturn-analog banding warmed and muted to the planet's palette.

## Atmosphere synthesis

55 Cnc c has a deep H₂/He envelope. At ~490 K the visible-altitude
condensates are alkali-metal salts and sulfides; gaseous Na/K produce
optical absorption. The super-metal-rich host suggests an enriched
metallicity, deepening the cloud colors.

- **Pressure / structure.** A continuous H₂/He atmosphere with a
  condensate cloud deck at the alkali/sulfide level; no discrete
  surface.
- **Composition.** H₂/He primary with Na/K and sulfide/silicate
  condensates; likely enhanced heavy-element abundance from the
  super-solar host.
- **Sky appearance.** From the upper atmosphere the sky would be a pale
  warm tan, hazed by alkali/sulfide clouds, with the host star (2.0°
  angular diameter) prominent but no longer overwhelmingly dominant as
  it is for the inner planets.

## Rotation & spin synthesis

At 0.247 AU on a 44.4-day orbit, 55 Cnc c is not tidally locked — the
gas-giant tidal-locking timescale at this distance far exceeds the
~10 Gyr system age. The orbit is mildly eccentric (e = 0.088, though
with a large uncertainty; Moutou 2025). No rotation period has been
measured.

**KSP implementation note.** The cfg adopts a fast Jovian rotation
(~10–11 h order, Saturn-analog) for visual banding. This is a tie-break;
flag as unconstrained.

**Mild seasons.** The e ≈ 0.088 eccentricity gives a modest
periastron-to-apastron insolation swing (T_eq from ~470 K at apastron
to ~510 K at periastron), but with negligible obliquity there are no
axial seasons.

## Visual styling

- **Global appearance.** A warm muted-tan Saturn-class banded giant at
  0.247 AU — the second of the system's four giants, between the hotter
  inner b and the temperate f.
- **Cloud decks.** Zonal banding in warm tans (`#d4b890`), softer and
  paler than b, with gentle light-zone / dark-belt alternation.
- **Limb / haze.** A pale warm limb haze (`#e0c8a0`).
- **Star in sky.** 55 Cnc A subtends 2.04° — about 4× the Sun's
  angular size from Earth — a prominent warm-orange disk.
- **Sister planets in sky.** Planet b (inward at 0.118 AU) and planet f
  (outward at 0.80 AU) appear as warm points; the lava super-Earth e is
  lost near the star.
- **No rings (default).** At ~490 K, c is too warm for a stable ice
  ring; no ring is rendered (the cold giant d is the system's
  ring-candidate body).

## Bibliography

### Read (visual-informative, drove decisions above)

- **Moutou C. et al. 2025/2026** — *Characterizing planetary systems
  with SPIRou…*, A&A 705, A190 (`2026A&A...705A.190M`,
  [arXiv:2510.11523](https://arxiv.org/abs/2510.11523)). Latest RV refit: planet c P = 44.3936 d,
  a = 0.247 AU, e = 0.088, M sin i = 56.6 ± 2.2 M⊕. **Phase 2
  recommended orbit + mass.** Postdates the model cutoff —
  value-checked against the cached text.
- **von Braun K. et al. 2011** — `2011ApJ...740...49V`,
  [arXiv:1107.1936](https://arxiv.org/abs/1107.1936). Host L = 0.582 L☉ → the T_eq derivation.

### Read (context / methodology, not decision-driving)

- **Bourrier V. et al. 2018** — `2018A&A...619A...1B`,
  [arXiv:1807.04301](https://arxiv.org/abs/1807.04301). Refit: c at a = 0.2373 AU, e = 0.03,
  M sin i = 51.2 M⊕ — documented-alternative orbit/mass (superseded by
  Moutou 2025).
- **McArthur B. E. et al. 2004** — `2004ApJ...614L..81M`. Discovery
  paper; historical context.

### Read (instrument-only, not visual-informative)

- (none specific to c beyond the system-level papers above.)

### Not read — no arXiv preprint or low-priority (~15 papers)

Early RV-refinement papers (Fischer 2008) and dynamical-stability
proceedings. Full filtered bib in `docs/phase3/_bib/55-cnc.yaml`.

## Open items for follow-up

- **Radius.** No measured radius (non-transiting); ~0.8 R_Jup is
  estimate-only. An inclination/true-mass constraint would allow a
  radius refinement.
- **Eccentricity.** e = 0.088 carries a large uncertainty (±0.23 in the
  curated entry); a tighter RV solution would firm up the mild-seasons
  treatment.
- **Atmospheric metallicity.** Enriched composition expected from the
  super-metal-rich host; a future emission/transmission constraint
  would refine the cloud color.

## Related

- [55-cnc](55-cnc.md) — host star (K0 IV-V, L = 0.582 L☉)
- [55-cnc-b](55-cnc-b.md) — inner neighbor (hotter Jovian)
- [55-cnc-f](55-cnc-f.md) — outer neighbor (temperate, HZ-grazing giant)
- [methodology](../reference/methodology.md) — Decisions schema and Msini convention
