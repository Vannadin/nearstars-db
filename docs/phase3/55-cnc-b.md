<!-- 55 Cnc b Phase 3 synthesis: cfg-ready decisions and reasoning -->
# 55 Cnc b — Phase 3 Synthesis

55 Cnc b is the innermost giant of the system and the fourth exoplanet
ever discovered (Butler et al. 1997). It is a warm Jovian on a
14.65-day, nearly circular orbit at 0.118 AU around 55 Cnc A, with a
radial-velocity minimum mass M sin i ≈ 276 M⊕ ≈ 0.87 M_Jup (Moutou
2025). It does not transit (i ≈ 89.7° is poorly constrained, with a
24° error bar), so there is no measured radius — for a non-irradiated-to-
mildly-irradiated Jovian of this mass, a radius near ~1.0 R_Jup is the
standard estimate. With the host luminosity L = 0.582 L☉, its
equilibrium temperature derives to T_eq(A=0) ≈ 708 K — a warm Jupiter,
hot enough for a cloudless deep atmosphere but well below the
"hot Jupiter" inflation regime of the most extreme close-in giants.

**Scenario choice for NearStars: a warm Jovian — a roughly
Jupiter-mass, Jupiter-radius gas giant at ~700 K, rendered with warm
banded cloud decks (alkali-metal / silicate condensates) under the
yellow-orange light of its K0 host.** Mass is Msini (RV), radius is an
estimate-only standard Jovian value; the cfg flags both accordingly.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false (likely pseudo-synchronous) | medium | 14.65 d orbit at 0.118 AU; tidal locking timescale for a gas giant is long, but pseudo-synchronization plausible |
| `obliquity_deg` | 0 | low | Tie-break: assumed low for a close-in giant; unconstrained |
| `eccentricity` | 0.0029 | high | Moutou 2025 — essentially circular (Bourrier 2018 gives 0.0) |
| `argument_of_periastron_deg` | 23 | low | raw NASA Archive value (low ecc → weak constraint) |
| `sidereal_period_days` | 14.651552 | high | Moutou 2025 (Phase 2 recommended; Bourrier 2018 14.6516 agrees) |
| `semi_major_axis_au` | 0.118 | high | Moutou 2025 (Phase 2 recommended; Bourrier 2018 0.1134) |
| `inclination_deg` | ~89.7 (unconstrained, ±24°) | low | raw value; non-transiting, so true mass not pinned |
| `mass_mearth` | 276 (M sin i) | high | Moutou 2025 — RV minimum mass (Phase 2 recommended; Bourrier 2018 255.4) |
| `mass_type` | Msini | high | Moutou 2025 — radial-velocity minimum mass; non-transiting |
| `mass_mjup` | 0.87 (M sin i) | high | derived = 276 / 317.8 |
| `radius_rjup` | ~1.0 (estimate only) | low | No measured radius (non-transiting); standard warm-Jovian estimate at ~0.9 M_Jup, ~700 K |
| `equilibrium_temp_k` (A=0) | 708 | high | derived: 278.3·0.582^0.25/√0.118 |
| `equilibrium_temp_k` (A=0.3) | 647 | high | derived, Jovian-analog albedo |
| `insolation_s_earth` | 41.8 | high | derived = L / a² = 0.582 / 0.118² |
| `bond_albedo` | 0.3 | low | Tie-break: cloudy warm Jovian, Jupiter-like albedo |
| `atmosphere_present` | true | high | gas giant — H/He envelope |
| `atmosphere_composition` | H₂/He with alkali metals (Na, K), silicate/sulfide condensate clouds | medium | warm-Jovian chemistry at ~700 K; super-metal-rich host favors enriched metallicity |
| `cloud_cover_fraction` | 0.9 | medium | banded gas-giant cloud decks |
| `cloud_morphology` | zonal banding; warm silicate/alkali-sulfide cloud decks, deeper and warmer than Jupiter's ammonia clouds | medium | 700 K class — too warm for NH₃ ice, condensates are silicates/sulfides/alkali salts |
| `cloud_tint_rgb_hex` | `#d8a878` (warm tan-orange) | low | Tie-break: warm-Jovian condensate palette (alkali/silicate haze), warmer than Jupiter's ochre |
| `atmosphere_tint_rgb_hex` | `#e8b888` (warm orange limb haze) | low | Tie-break: ~700 K Jovian limb |
| `star_apparent_angular_diameter_deg` | 4.26 | high | derived: 2·R★/a = 2·0.943 R☉ / 0.118 AU |
| `stellar_illumination_color_temp_k` | 5196 | high | von Braun 2011 stellar Teff |

## Surface synthesis

55 Cnc b has no surface — it is a gas giant — so this section covers
the cloud-top "surface" the renderer presents. At T_eq ≈ 708 K it is a
**warm Jovian**: hot enough that the ammonia and water-ice clouds that
give Jupiter its familiar palette cannot condense at the visible cloud
deck, but cool enough that it is not an inflated, glowing hot Jupiter.
The condensates that form at this temperature are silicates,
alkali-metal salts, and sulfides, deeper and warmer than Jupiter's
cloud tops.

The visible cloud-top color is therefore warmer and more orange-tan
than Jupiter's — `#d8a878` for the banded decks, with a slightly
warmer `#e8b888` limb haze. The host star's super-solar metallicity
([Fe/H] ≈ +0.32) suggests an enriched atmospheric metallicity, which
would deepen the cloud colors and strengthen the alkali-metal
absorption features. Under the yellow-orange 5196 K light of 55 Cnc A,
the planet reads as a warm tan-orange banded giant.

Morphology: standard gas-giant zonal banding (alternating prograde
and retrograde jets), with the band contrast and number set by the
rotation rate and internal heat flux. Without a measured rotation
period the banding is a tie-break; the cfg renders Jupiter-analog
banding warmed to the planet's palette.

## Atmosphere synthesis

55 Cnc b has a deep H₂/He envelope with no surface. At ~700 K the
dominant visible-altitude condensates are silicates (forsterite,
enstatite), alkali-metal salts (Na₂S, KCl), and sulfides — not the
ammonia/water ices of the Solar System giants. Gaseous sodium and
potassium produce strong alkali absorption in the optical, which
combined with the enriched (super-solar) host metallicity would make
the atmosphere relatively opaque and warm-toned.

- **Pressure / structure.** The visible cloud deck sits at the level
  where these condensates form; below it the atmosphere is a hot,
  clear, increasingly dense H₂/He fluid. No discrete surface.
- **Composition.** H₂/He primary, with Na/K alkali metals, silicate
  and sulfide condensates, and (given the super-metal-rich host) likely
  enhanced heavy-element abundance.
- **Sky appearance.** From within the upper atmosphere the sky would
  be a warm tan-orange, hazed by alkali/silicate clouds, with the
  enormous host star (4.3° angular diameter) dominating one
  hemisphere.

## Rotation & spin synthesis

At 0.118 AU on a 14.65-day orbit, 55 Cnc b is not necessarily tidally
locked — gas-giant tidal locking timescales are long, and the planet
likely settles into a pseudo-synchronous rotation rather than a strict
1:1 lock. The orbit is essentially circular (e = 0.003; Moutou 2025),
so any pseudo-synchronization would be close to synchronous. No
rotation period has been measured.

**KSP implementation note.** Lacking a measured spin, the cfg adopts a
fast Jovian rotation (~10 h order, Jupiter-analog) for visual banding
rather than a synchronous lock — banding dynamics look more
gas-giant-like at fast rotation. This is a tie-break; flag as
unconstrained.

**No seasons.** Negligible obliquity and eccentricity → no seasonal
variation.

## Visual styling

- **Global appearance.** A warm tan-orange banded gas giant, roughly
  Jupiter-sized, at 0.118 AU — the innermost of the system's four
  giants and the brightest sibling in 55 Cnc e's sky.
- **Cloud decks.** Zonal banding in warm tans and oranges (`#d8a878`),
  with alternating light zones and darker belts. Deeper, warmer
  condensates than Jupiter; no white ammonia clouds.
- **Limb / haze.** A warm orange limb haze (`#e8b888`), with the
  alkali-metal absorption giving the limb a slightly deeper tone.
- **Star in sky.** 55 Cnc A subtends 4.26° — about 8× the Sun's
  angular size from Earth — a large warm-orange disk dominating the
  daytime hemisphere.
- **Sister planets in sky.** The lava super-Earth e (inward at
  0.0154 AU) appears as a bright point near the star; planet c (outward
  at 0.247 AU) is a fainter warm point. None rivals the host star.
- **No rings (default).** Unlike the cold giant d, b is too warm and
  too close for a stable ice ring; no ring is rendered.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Moutou C. et al. 2025/2026** — *Characterizing planetary systems
  with SPIRou…*, A&A 705, A190 (`2026A&A...705A.190M`,
  arXiv:2510.11523). Latest RV refit: planet b P = 14.651552 d,
  a = 0.118 AU, e = 0.0029, M sin i = 276 ± 9 M⊕. **Phase 2 recommended
  orbit + mass.** Postdates the model cutoff — values value-checked
  against the cached text.
- **von Braun K. et al. 2011** — `2011ApJ...740...49V`,
  arXiv:1107.1936. Host L = 0.582 L☉ → the T_eq derivation.

### Read (context / methodology, not decision-driving)

- **Bourrier V. et al. 2018** — `2018A&A...619A...1B`,
  arXiv:1807.04301. Homogeneous system refit: b at a = 0.1134 AU,
  e = 0.0, M sin i = 255.4 M⊕ — the documented-alternative orbit/mass
  (superseded by Moutou 2025 as recommended).
- **Butler R. P. et al. 1997** — `1997ApJ...474L.115B`. Discovery
  paper (the 4th exoplanet ever found); historical context.

### Read (instrument-only, not visual-informative)

- **Ehrenreich D. et al. 2012** — noted 55 Cnc b as a warm Jupiter
  "possibly at the limit of atmospheric stability" (via Bourrier 2018
  intro); context for the warm-Jovian classification.

### Not read — no arXiv preprint or low-priority (~15 papers)

Early RV-refinement papers (Marcy 2002, McArthur 2004, Fischer 2008 —
superseded by Bourrier 2018 / Moutou 2025) and dynamical-stability
proceedings. Full filtered bib in `docs/phase3/_bib/55-cnc.yaml`.

## Open items for follow-up

- **Radius.** No measured radius (non-transiting). If an astrometric or
  future direct-imaging constraint pins the inclination and true mass,
  the radius estimate can be replaced; for now ~1.0 R_Jup is an
  estimate-only standard value.
- **Atmospheric metallicity.** The super-metal-rich host suggests an
  enriched atmosphere; a future transmission/emission constraint would
  refine the cloud composition and color.
- **Rotation.** No measured spin; the cfg's fast-Jovian rotation is a
  tie-break. Any measured rotation (e.g. from Doppler-imaging) would
  set the banding dynamics.

## Related

- [55-cnc](55-cnc.md) — host star (K0 IV-V, L = 0.582 L☉)
- [55-cnc-e](55-cnc-e.md) — inner neighbor (USP lava super-Earth)
- [55-cnc-c](55-cnc-c.md) — outer neighbor (warm Saturn-class giant)
- [methodology](../reference/methodology.md) — Decisions schema and Msini convention
