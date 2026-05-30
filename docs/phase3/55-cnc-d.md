<!-- 55 Cnc d Phase 3 synthesis: cfg-ready decisions and reasoning -->
# 55 Cnc d — Phase 3 Synthesis

55 Cnc d is the system's cold outer giant: a ~3.8 M_Jup
(M sin i ≈ 1214 M⊕, Moutou 2025) gas giant on a long ~4799-day
(~13.1-year) eccentric (e ≈ 0.09) orbit at 5.6 AU around 55 Cnc A. It
was among the first long-period giant planets ever found (Marcy et al.
2002), with one of the longest known orbital periods at the time. Its
exact orbit remains the system's most contested signal because its
period is entangled with the star's ~10.5-year magnetic cycle —
Bourrier 2018 placed it at 5574 d / ~6 AU, Moutou 2025 at 4799 d /
5.6 AU, with other studies ranging 4825–5285 d. It does not transit, so
there is no measured radius; for a ~3.8 M_Jup giant a radius near
~1.1–1.2 R_Jup is the standard estimate (massive giants are slightly
compressed). With the host luminosity L = 0.582 L☉, its equilibrium
temperature derives to T_eq(A=0) ≈ 103 K — a genuinely **cold Jovian**,
colder than Jupiter, in the regime where ammonia clouds and a possible
ring/moon system would be stable.

**Scenario choice for NearStars: a cold, massive Jovian (~3.8 M_Jup,
~100 K) at 5.6 AU, rendered as a deep, ammonia-clouded gas giant in
cool muted tones — with an OPTIONAL artistic Saturn-like ring system
(flagged not observed) as the system's ring-candidate body, per the
disk-color / ring policy.** Mass is Msini (RV), radius is
estimate-only; the ring is an explicit artistic option, not an
observation.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | high | 4799 d orbit at 5.6 AU; far outside any tidal regime |
| `obliquity_deg` | 0 | low | Tie-break: assumed low; unconstrained |
| `eccentricity` | 0.0913 | medium | Moutou 2025 (Bourrier 2018 gives 0.13; the orbit is cycle-entangled and uncertain) |
| `argument_of_periastron_deg` | −90 | low | raw NASA Archive value |
| `sidereal_period_days` | 4799 | medium | Moutou 2025 (Phase 2 recommended; DOCUMENTED divergence vs Bourrier 2018's 5574 d — see Canonical alternatives) |
| `semi_major_axis_au` | 5.6 | medium | Moutou 2025 (Phase 2 recommended; Bourrier 2018 5.957) |
| `inclination_deg` | ~89.7 (unconstrained, ±24°) | low | raw value; non-transiting |
| `mass_mearth` | 1214 (M sin i) | high | Moutou 2025 — RV minimum mass (Phase 2 recommended; Bourrier 2018 991.6) |
| `mass_type` | Msini | high | Moutou 2025 — radial-velocity minimum mass; non-transiting |
| `mass_mjup` | 3.8 (M sin i) | high | derived = 1214 / 317.8 (Moutou 2025 abstract quotes 3.8 M_Jup) |
| `radius_rjup` | ~1.1 (estimate only) | low | No measured radius (non-transiting); massive-Jovian estimate at ~3.8 M_Jup, ~100 K (slight compression) |
| `equilibrium_temp_k` (A=0) | 103 | high | derived: 278.3·0.582^0.25/√5.6 |
| `equilibrium_temp_k` (A=0.3) | 94 | high | derived, Jovian-analog albedo |
| `insolation_s_earth` | 0.019 | high | derived = L / a² = 0.582 / 5.6² |
| `bond_albedo` | 0.3 | low | Tie-break: ammonia-clouded cold Jovian, Jupiter-like albedo |
| `atmosphere_present` | true | high | gas giant — H/He envelope |
| `atmosphere_composition` | H₂/He with NH₃ + deeper NH₄SH / H₂O cloud decks; possible CH₄ tint | medium | ~100 K — cold Jovian, ammonia-cloud regime; CH₄ absorption possible at this temperature |
| `cloud_cover_fraction` | 0.95 | medium | deep banded gas-giant cloud decks |
| `cloud_morphology` | zonal banding; deep NH₃ + NH₄SH cloud decks (Jupiter/Saturn-analog), high-contrast belts and zones | medium | ~100 K — fully in the ammonia-cloud regime of the cold Solar System giants |
| `cloud_tint_rgb_hex` | `#dcdcd0` (cool pale cream-grey, NH₃ clouds) | low | Tie-break: cold-Jovian ammonia palette, slightly grey-cool |
| `atmosphere_tint_rgb_hex` | `#cdd8e4` (cool pale-blue limb, Rayleigh + CH₄) | low | Tie-break: ~100 K cold limb, CH₄-tinged |
| `ring_present` | true (ARTISTIC OPTION — NOT observed) | low | Tie-break: no observed ring; a Saturn-like ice ring is plausible at ~100 K and allowed as an artistic option per the disk/ring policy — flagged `ring_observed = false` |
| `ring_inner_au` | 0.0012 | low | Tie-break: ~1.5 R_Jup inner edge for the artistic ring (≈ Saturn-relative geometry) |
| `ring_outer_au` | 0.0035 | low | Tie-break: ~4.5 R_Jup outer edge (Saturn-relative geometry) |
| `ring_color_hex` | `#e8e4d8` (icy cream-white) | low | Tie-break: cold water-ice ring at ~100 K, like Saturn's |
| `ring_opacity` | 0.6 | low | Tie-break: Saturn-like moderate opacity for visibility |
| `ring_morphology` | multi-ring icy system with a Cassini-like gap (artistic) | low | Tie-break: Saturn-analog; purely artistic |
| `ring_observed` | false | high | NO ring observed; flagged per the anti-fabrication policy — the ring is an explicit artistic option only |
| `star_apparent_angular_diameter_deg` | 0.090 | high | derived: 2·R★/a = 2·0.943 R☉ / 5.6 AU — the star is a small bright point |
| `stellar_illumination_color_temp_k` | 5196 | high | von Braun 2011 stellar Teff |

## Surface synthesis

55 Cnc d is a massive (~3.8 M_Jup) cold gas giant with no surface; this
section covers the cloud-top "surface". At T_eq ≈ 103 K it is the
system's only **cold Jovian** — colder than Jupiter (~110 K) — firmly
in the ammonia-cloud regime. Its great mass makes it the system's
dominant outer body, on a long ~13-year orbit far beyond the inner
four planets (the f–d gap is ~4 AU).

The cloud-top palette is a cool pale cream-grey (`#dcdcd0`) — deep
ammonia clouds with NH₄SH and water clouds beneath, like the Solar
System giants but cooler and slightly greyer. Methane absorption at
this temperature can add a faint cool-blue tint to the limb (`#cdd8e4`).
The super-metal-rich host suggests an enriched, high-contrast
atmosphere. Under the 5196 K host light — now a small, bright,
0.09°-diameter point in d's sky — the planet reads as a deep,
high-contrast, cool-toned banded giant: the most classically "gas
giant" world of the system.

Morphology: deep zonal banding with high belt/zone contrast (cold
giants show strong banding), optional long-lived storm vortices, and —
as an artistic option — a Saturn-like ring system (see below).

## Atmosphere synthesis

55 Cnc d has a deep, massive H₂/He envelope. At ~100 K the visible
condensates are ammonia ice (NH₃), with ammonium hydrosulfide (NH₄SH)
and water clouds deeper, plus possible gaseous methane producing a
cool-blue absorption tint — the classic cold-giant cloud chemistry.

- **Pressure / structure.** A deep H₂/He atmosphere with an NH₃-ice
  cloud deck, NH₄SH and water clouds below; no discrete surface. The
  great mass gives a deep, high-pressure interior.
- **Composition.** H₂/He primary with NH₃, NH₄SH, H₂O, and possible
  CH₄; the super-metal-rich host suggests enhanced heavy-element
  abundance.
- **Sky appearance.** From the upper atmosphere the sky would be a cool
  pale cream-blue, with the host star a small bright point (0.09°) —
  the dimmest stellar illumination of any 55 Cnc planet, plus the
  distant M-dwarf companion 55 Cnc B as a faint orange-red second sun
  far out at ~1065 AU.

## Rotation & spin synthesis

At 5.6 AU on a ~4799-day orbit, 55 Cnc d is far outside any
tidal-locking regime and rotates freely and fast, like the Solar
System giants. The orbit is mildly eccentric (e ≈ 0.09; Moutou 2025),
though both the eccentricity and the period are uncertain because the
~13-year orbit is entangled with the star's ~10.5-year magnetic cycle.
No rotation period has been measured.

**KSP implementation note.** The cfg adopts a fast Jovian rotation
(~10 h order, Jupiter-analog) for visual banding. This is a tie-break;
flag as unconstrained.

**No seasons.** Negligible obliquity → no axial seasons; the mild
eccentricity gives only a tiny insolation swing on an already very low
insolation (0.019 S⊕).

## Visual styling

- **Global appearance.** A massive, cool, high-contrast banded gas
  giant at 5.6 AU — the system's dominant outer body and most
  classically "gas giant" world, optionally crowned with a Saturn-like
  ring.
- **Cloud decks.** Deep zonal banding in cool pale cream-greys
  (`#dcdcd0`), with high belt/zone contrast and optional long-lived
  storm vortices.
- **Limb / haze.** A cool pale-blue, methane-tinged limb (`#cdd8e4`).
- **Ring system (optional, artistic).** As the system's
  ring-candidate body, d may be rendered with a Saturn-like icy ring
  (`#e8e4d8`, opacity 0.6, ~1.5–4.5 R_Jup, multi-ring with a
  Cassini-like gap). At ~100 K a water-ice ring is thermally stable.
  This is an **explicit artistic option, not an observation**
  (`ring_observed = false`) — included per the ring/disk policy as an
  allowed aesthetic choice for a cold giant, never presented as
  detected.
- **Star in sky.** 55 Cnc A subtends only 0.090° — about ⅙ the Sun's
  angular size from Earth — a small bright warm-orange point. The
  illumination is dim (0.019 S⊕, ~2% of Earth's).
- **Sister planets in sky.** The inner four planets are all close to
  the star from d's vantage; the temperate f (inward at 0.80 AU) is the
  nearest, a faint point. The M-dwarf companion 55 Cnc B (~1065 AU) is
  a faint orange-red second sun far beyond d's orbit.

## Canonical alternatives

55 Cnc d's orbit is the system's most contested signal, and the cfg
makes a documented choice between two literature periods. The ring is
handled separately as an explicit artistic option (flagged
`ring_observed = false`) rather than a divergence, since no observation
claims a ring either way.

### Diverged cfg picks

| Field | Gameplay (in cfg) | Canonical alternative | Why diverged |
|---|---|---|---|
| `sidereal_period_days` / `semi_major_axis_au` | 4799 d / 5.6 AU (Moutou 2025) | 5574 d / 5.96 AU (Bourrier 2018) | The two recommended-grade RV fits differ by 9σ in period because d's ~13-yr orbit is entangled with the star's ~10.5-yr magnetic cycle, and the result is sensitive to how the cycle is modeled (Keplerian vs GPR) and which instruments are combined. The cfg adopts the most recent value (Moutou 2025, 4799 d) as Phase 2 recommended; the Bourrier 2018 5574 d orbit is preserved as a cfg variant. Other studies span 4825–5285 d. This is a genuine measurement disagreement, not a gameplay choice — flagged so the cfg writer ships the recommended orbit but knows the alternative exists. |

## Bibliography

### Read (visual-informative, drove decisions above)

- **Moutou C. et al. 2025/2026** — *Characterizing planetary systems
  with SPIRou…*, A&A 705, A190 (`2026A&A...705A.190M`,
  arXiv:2510.11523). Latest RV refit: planet d P = 4799 d (9σ shorter
  than Bourrier 2018's 5574 d), a = 5.6 AU, e = 0.0913,
  M sin i = 1214 ± 41 M⊕ ≈ 3.8 M_Jup; notes the orbit is entangled with
  the ~10.5-yr magnetic cycle and a possible additional outer body
  (long-term RV trend, P > 24 yr). **Phase 2 recommended orbit + mass.**
  Postdates the model cutoff — value-checked against the cached text.
- **von Braun K. et al. 2011** — `2011ApJ...740...49V`,
  arXiv:1107.1936. Host L = 0.582 L☉ → the T_eq derivation.

### Read (context / methodology, not decision-driving)

- **Bourrier V. et al. 2018** — `2018A&A...619A...1B`,
  arXiv:1807.04301. Refit including the magnetic-cycle Keplerian: d at
  P = 5574 d, a = 5.957 AU, e = 0.13, M sin i = 991.6 M⊕ — the
  documented-alternative orbit (see Canonical alternatives).
- **Marcy G. W. et al. 2002** — `2002ApJ...581.1375M`. Discovery paper
  for d (one of the longest-period giants known at the time);
  historical context.

### Read (instrument-only, not visual-informative)

- (none specific to d beyond the system-level papers above.)

### Not read — no arXiv preprint or low-priority (~15 papers)

Long-period-signal decomposition papers (Endl 2012, Baluev 2015,
Rosenthal 2021, Laliotis 2023 — all give different d periods, captured
qualitatively in the Canonical alternatives) and dynamical-stability
proceedings. Full filtered bib in `docs/phase3/_bib/55-cnc.yaml`.

## Open items for follow-up

- **Orbit disambiguation.** d's period is contested (4799 d Moutou
  2025 vs 5574 d Bourrier 2018, range 4825–5285 d elsewhere) because of
  the magnetic-cycle entanglement. A homogeneous long-baseline nIR +
  optical RV campaign with a continuous activity indicator (Moutou 2025
  Open items) would settle it; the cfg should re-derive a, T_eq, and
  the angular diameters if the period is revised.
- **Possible additional outer body.** Moutou 2025 finds a long-term RV
  trend (0.84 m/s/yr) suggesting another body with P > 24 yr; if
  confirmed, a sixth/seventh planet Decisions entry may be needed.
- **Radius.** No measured radius (non-transiting); ~1.1 R_Jup is
  estimate-only. An inclination/true-mass or direct-imaging constraint
  would refine it.
- **Ring variants.** The Saturn-like ring is an artistic option
  (`ring_observed = false`). Ship both a no-ring and a ringed cfg
  variant; the ring is never to be presented as detected.

## Related

- [55-cnc](55-cnc.md) — host star (K0 IV-V, L = 0.582 L☉)
- [55-cnc-f](55-cnc-f.md) — inner neighbor (temperate HZ-grazing giant); the ~4 AU f–d gap is the system's largest
- [eps-eri](eps-eri.md) — comparison cold-Jovian host context (ε Eri b at 3.5 AU)
- [methodology](../reference/methodology.md) — Decisions schema, Msini convention, and ring fields
- [tools](../reference/tools.md) — disk/ring color synthesis policy (anti-fabrication)
