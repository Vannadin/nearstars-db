<!-- 40 Eridani A b Phase 3 synthesis: refuted ("Vulcan"/"Erid") detection re-included as a documented divergence per project decision -->
# 40 Eridani A b — Phase 3 Synthesis (Refuted — included as documented divergence)

40 Eridani A b is the most culturally famous refuted exoplanet ever
announced. It is **Vulcan**, the homeworld of Mr. Spock in *Star
Trek* — Gene Roddenberry's 1991 letter to *Sky & Telescope*
(co-signed by Sallie Baliunas and colleagues) settled the canon
debate in favor of 40 Eridani A over Epsilon Eridani — and it is
**Erid**, the homeworld of the alien Rocky in Andy Weir's *Project
Hail Mary* (2021). No other refuted detection carries this much
cultural weight, and that is the entire reason it survives in the
NearStars database at all.

The candidate was announced by Ma et al. 2018 (`2018AJ....155..117M`,
the Dharma Planet Survey RV program) as a super-Earth with
M sin i ≈ 8.47 M⊕ on a P = 42.245-day orbit at a = 0.224 AU around
the K0.5 V primary of the 40 Eridani triple, a real nearby catalog
system at 5.0 pc (this is **not** a beyond-50-ly target — 40 Eri is
one of the closest naked-eye stars). The host is a K0.5 V dwarf with
Teff 5143 K, L = 0.408 L☉, and M = 0.78 M☉, placing the candidate
well inside the habitable-zone inner edge — a *hot* super-Earth with
equilibrium temperature Teq(A=0.3) = 430 K, Teq(A=0) = 470 K.

**The detection was refuted by Burrows et al. 2024 and Lubin et al.
2024.** A 16-year multi-instrument RV baseline showed that the
42-day signal is the star's rotation period, not a Keplerian planet —
the same activity-driven periodicity that the 40 Eri A host synthesis
discusses as the spurious "Vulcan" signal. The canonical reading is
therefore *no planet*.

**Per a project decision, b is re-included** in
`db/systems/40_eridani.json::planets[]` at its pre-retraction Ma 2018
values as a refuted-flagged documented divergence, for the
exceptional cultural weight (Vulcan in *Star Trek* + Erid in *Project
Hail Mary*). Every row below carries Confidence=low except the
`disposition` row, because the underlying signal is now considered an
artifact; the refutation is kept prominent throughout rather than
hidden behind the synthesized world.

**Scenario choice for NearStars: a hot (~430–500 K), reddish,
high-gravity (~2.3 g) rocky-iron super-Earth — synthesized as a
documented divergence at the pre-retraction Ma 2018 mass and orbit,
rendered with a rusty basaltic Vulcan desert under the orange K0.5 V
primary.** The interesting-first reading is a dense rocky world with a
thick hazy atmosphere retained by its high gravity. The canonical
reading remains no planet.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `disposition` | Refuted (Burrows/Lubin 2024) | high | 42-day signal = stellar rotation, not Keplerian; multi-instrument 16-yr RV. The one high-confidence row |
| `mass_mearth` | 8.47 (M sin i; true mass ≥ this) | low | Ma 2018 RV; signal refuted |
| `radius_rearth` | ~1.9 | low | tie-break / interesting-first: mass–radius for a rocky-iron 8.5 M⊕ super-Earth (≈ Weir's Erid 2.01 R⊕); RV-only, never measured |
| `density_g_cc` | ~6.8 | low | derived M/R³ — rocky-metal, denser than Earth |
| `surface_gravity_g_earth` | ~2.35 | low | derived 8.47/1.9² (≈ Erid's 2.09 g) |
| `equilibrium_temp_k` (A=0.3) | 430 | low | derived; (A=0) 470 |
| `insolation_s_earth` | ~8.1 | low | derived 0.408 L☉ / (0.224 AU)² — hot, well inside the HZ inner edge |
| `surface_temp_k` | ~450–500 | low | Fiction-derived: this is not a physical estimate but an art-direction nod to Asimov's *Lucky Starr* "Erid" lore, which puts the surface at 210 °C ≈ 483 K, applied to an already-refuted body. No physical greenhouse calculation or paper backs this value; treated as flavor only |
| `bond_albedo` | 0.20 | low | tie-break: dark hazy / basaltic |
| `tidally_locked` | false | low | a = 0.224 AU around 0.78 M☉ → lock timescale long; interesting-first picks a rotator (Erid's fast spin) |
| `rotation_period_h` | ~5–10 (fast) | low | tie-break + Erid lore (5.1 h fast rotator → strong dynamo); moot for a refuted body |
| `atmosphere_composition` | thick CO₂/N₂ with high-altitude haze | low | tie-break: degenerate; interesting-first — high gravity retains a thick atmosphere at this Teq |
| `atmosphere_surface_pressure_pa` | ~1×10⁶ (≈10 bar) | low | tie-break: interesting-first thick atmosphere |
| `surface_tint_rgb_hex` | `#b5603a` (rusty basaltic-orange desert) | medium | tie-break: interesting-first + Vulcan's iconic reddish desert; iron-oxide / basalt on a hot rocky surface |
| `sky_tint_rgb_hex` | `#c98a5a` (dusty orange) | low | tie-break: thick hazy atmosphere under K0.5 V (5143 K) light |

## Surface synthesis

In the pre-retraction Ma 2018 picture, b sat at ~8.1 S⊕ — far inside
the habitable-zone inner edge for the K0.5 V host, giving an
equilibrium temperature of 430 K under an A = 0.3 bond albedo (470 K
at zero albedo). This is unambiguously a *hot* super-Earth, not a
temperate one; the Vulcan fiction predates the discovery and assumed
an Earth-like desert world, but the real orbital geometry places b in
the hot-rocky regime well above any water-stability threshold for a
thin atmosphere.

**The interesting-first reading is a dense rocky-iron super-Earth.**
With 8.47 M⊕ (M sin i) and a tie-break radius of ~1.9 R⊕ — closely
matching Weir's Erid at 2.01 R⊕ — the body is rocky-metal with a
derived density of ~6.8 g/cc and a surface gravity of ~2.35 g, very
close to Erid's quoted 2.09 g. None of these were ever measured: the
detection is RV-only and the signal is now refuted, so radius,
density, and gravity all cascade from the tie-break radius rather than
from any observation.

**Color choice — rusty basaltic Vulcan desert.** The primary surface
tint `#b5603a` encodes a hot, iron-oxide / basaltic desert, the
single highest-confidence visual row (medium) because it is
overdetermined: it is both the data-grounded reading for a hot rocky
surface and a direct nod to Vulcan's iconic reddish desert in *Star
Trek*. Surface temperature in this reading is ~450–500 K — base Teq
plus a modest greenhouse contribution from the thick atmosphere — which
lines up with Erid lore's stated 210 °C (≈ 483 K) surface.

**Refutation context.** The Ma 2018 signal at 42.245 d turned out to
be 40 Eridani A's stellar rotation period, not a Keplerian planet.
Burrows et al. 2024 used NEID line-by-line activity diagnostics and a
16-year multi-instrument RV baseline to show the periodicity tracks
the chromospheric activity rather than a reflex orbit; Lubin et al.
2024 reached the same conclusion independently. This is the same
~42-day rotational modulation documented in the 40 Eri A host
synthesis, and it settles the disposition as Refuted.

## Atmosphere synthesis

The atmosphere is entirely degenerate. The detection was RV-only —
no transit, no transmission spectrum, no direct imaging — so nothing
about an atmosphere was ever observed, and the body itself is refuted.
The synthesis adopts an interesting-first reading and lays the cultural
readings out as explicit alternatives.

**Pressure and composition — interesting-first thick atmosphere.** At
~2.35 g surface gravity, b retains a thick atmosphere far more easily
than a lower-mass world at the same Teq, so the cfg adopts a thick
CO₂/N₂ envelope with high-altitude haze at ~1×10⁶ Pa (≈10 bar). This
is a tie-break: high gravity favors retention, the haze darkens the
Bond albedo to 0.20, and a modest greenhouse lifts the surface above
the bare equilibrium temperature into the 450–500 K range.

**Cultural readings as alternatives.** The fiction diverges sharply
from the data and from itself. *Star Trek*'s Vulcan is a thin-atmosphere
world with a red desert sky — the classic hot-desert homeworld. Weir's
Erid in *Project Hail Mary* is the opposite extreme: a thick ~28 atm
NH₃ atmosphere at 210 °C, with the Eridians having evolved blind in
near-total darkness under that dense haze (the surface is essentially
lightless in the novel). The cfg's interesting-first pick sits between
them — a thick, hazy, hot atmosphere, but CO₂/N₂ rather than Erid's
NH₃, because the NH₃-specific value is a made-up worldbuilding choice
rather than a data-grounded one.

**The 2026 *Project Hail Mary* film's deep-blue atmosphere is
fiction.** The film depicts Erid with a deep-blue atmosphere — an
art-direction choice that contradicts both Weir's colourless NH₃
worldbuilding and the data-grounded hot-reddish reading. It is
explicitly **not** adopted in the cfg values; the dusty-orange
`sky_tint_rgb_hex` `#c98a5a` is the data-grounded sky color under the
K0.5 V (5143 K) primary, and the film's blue is recorded only in
`docs/reference/cultural-context.md § 40 Eridani A`.

**Loss context.** No loss calculation is meaningful for a refuted
body. The qualitative point is only that the high gravity makes a thick
atmosphere *plausible* in the interesting-first scenario — the actual
retention question is moot because there is no planet.

## Rotation & spin synthesis

If b existed, it would **not be tidally locked**. At a = 0.224 AU
around a 0.78 M☉ host the tidal-lock timescale is long — far longer
than for a close-in M-dwarf planet — so a primordial spin would
survive, and the body would be a free rotator rather than a
synchronous one. Spin damping has not had time to operate at this
orbital distance.

**Interesting-first fast rotator.** The cfg adopts a fast rotation
period of ~5–10 h, matching Erid's lore value of a 5.1-h sidereal day.
In Weir's worldbuilding the fast spin is what drives Erid's strong
dynamo (≈ 25× Earth's magnetic field), needed to retain the thick
ammonia atmosphere; the interesting-first pick borrows the fast
rotator without the NH₃-specific field strength.

**Moot for a refuted body.** The rotation period, the lock state, and
the dynamo are all unconstrained and ultimately moot, because the
42-day RV signal *is* the host's rotation — there is no planetary spin
to measure. The fast-rotator value is a cultural-flavor tie-break, not
a physical inference.

## Visual styling

This section frames the planet "as it would be rendered as a
documented divergence" rather than "as it exists" (because it does
not).

- **Global appearance (interesting-first).** A hot, reddish,
  high-gravity super-Earth — a rusty basaltic-orange desert
  (`#b5603a`) under a dusty-orange hazy sky (`#c98a5a`), lit by the
  orange K0.5 V primary. Visual character closest to a hotter, denser,
  more iron-stained Mars-tone world wrapped in a thick haze layer.
- **Atmosphere haze (interesting-first).** A thick ~10-bar hazy
  envelope gives a soft dusty-orange limb and muted surface contrast,
  rather than the crisp terminator of an airless world. The high
  gravity compresses the scale height, so the haze sits as a dense
  low layer.
- **Sky companions — the 40 Eri triple.** From b's surface the
  distant white-dwarf 40 Eri B and the red-dwarf flare star 40 Eri C
  appear as brilliant points in the sky (the B–C pair orbits the A
  primary at ~400 AU), a distinctive triple-system skyscape under the
  orange daylight of the K0.5 V primary.
- **Film fiction explicitly excluded.** The 2026 *Project Hail Mary*
  film's deep-blue atmosphere and ring system are **fiction** and are
  **not** rendered in cfg. The cfg uses the data-grounded hot reddish
  reading (rusty desert, dusty-orange hazy sky); the film's blue
  atmosphere and rings are recorded only in
  `docs/reference/cultural-context.md § 40 Eridani A`.
- **"Vulcan / Erid" cultural cross-reference.** This Phase 3 markdown
  is the synthesis + cultural cross-reference home, paired with
  `docs/reference/cultural-context.md § 40 Eridani A`. Per a project
  decision, NearStars includes b as a documented divergence — rendered
  using the interesting-first reading despite the refuted signal
  (canonical = no planet).

## Canonical alternatives

**The canonical reading is no planet.** The 42-day signal is 40
Eridani A's stellar rotation period (Burrows/Lubin 2024), not a
Keplerian orbit, and modern catalogs carry no confirmed planet at this
period. The cfg includes a synthesized world purely as a documented
divergence for the exceptional cultural weight; the table below lays
out the three cultural readings against the cfg's interesting-first
pick.

| Reading | Atmosphere | Surface / appearance | Status |
|---|---|---|---|
| *Star Trek* Vulcan | thin atmosphere | red desert sky, hot desert homeworld | fiction (predates discovery) |
| Weir's Erid (*Project Hail Mary*) | thick ~28 atm NH₃, 210 °C | dark — Eridians evolved blind in near-total darkness | fiction (worldbuilding) |
| *Project Hail Mary* 2026 film | deep-blue atmosphere | ring system | fiction (art direction — **not** in cfg) |
| **cfg interesting-first pick** | thick CO₂/N₂ + high-altitude haze (~10 bar) | hot reddish basaltic desert, dusty-orange hazy sky | documented divergence (canonical = no planet) |

## Bibliography

### Read (discovery + refutation)

- **Ma B. et al. 2018** — *The First Super-Earth Detection from the
  High Cadence and High Radial Velocity Precision Dharma Planet
  Survey* (`2018AJ....155..117M`). The discovery paper. Reports b at
  P = 42.245 d, M sin i ≈ 8.47 M⊕, a ≈ 0.224 AU around the K0.5 V
  primary. Anchors the pre-retraction Decisions rows above.
- **Burrows R. et al. 2024** — *The Death of Vulcan: NEID Reveals
  the Planet Candidate Orbiting HD 26965 Is Stellar Activity*
  (refutation). NEID line-by-line activity diagnostics over a
  multi-instrument 16-year RV baseline show the 42-day signal tracks
  40 Eridani A's stellar rotation, not a Keplerian reflex orbit.
  Drives the Refuted disposition.
- **Lubin J. et al. 2024** — *Stellar Activity and the 42-day Signal
  of HD 26965* (independent refutation). Reaches the same negative
  conclusion as Burrows 2024 — the signal is rotational activity, not
  a planet.

### Read (cultural cross-reference)

- **Roddenberry G. & Baliunas S. et al. 1991** — letter to *Sky &
  Telescope* confirming 40 Eridani A (over Epsilon Eridani) as the
  *Star Trek* canon location of Vulcan, Mr. Spock's homeworld. The
  most prominent cultural anchor for the system. Documented in
  `docs/reference/cultural-context.md § 40 Eridani A`.
- **Weir A. 2021** — *Project Hail Mary* (novel). Names 40 Eridani A's
  world as Erid, the homeworld of the alien Rocky. Weir's worldbuilding
  companion document gives Erid 28 atm NH₃, 210 °C, 2.09 g, a 5.1-h
  sidereal day, and ≈ 25× Earth's magnetic field at the Ma 2018
  measured mass of 8.47 M⊕. The novel pre-dates the 2024 refutation.

### Not read — superseded or low-priority

- **Various habitability / Vulcan-popular-science treatments
  (2018–2024)** — assessments of the Ma 2018 candidate written before
  the refutation. No cfg relevance under the Refuted disposition.
- **Dharma Planet Survey instrumentation papers** — describe the
  EXPRES/DPS RV pipeline; mention 40 Eri only as a survey target. No
  visual relevance.

## Open items for follow-up

- **Refuted — no real planet.** The disposition is settled: the 42-day
  signal is stellar rotation (Burrows/Lubin 2024). No future follow-up
  is expected to re-promote b. The synthesized world exists in cfg
  only as a documented divergence for cultural weight.
- **Radius / density / atmosphere / rotation are all tie-break.** The
  detection is RV-only — no transit ever constrained the radius, so the
  ~1.9 R⊕ radius and the derived `density_g_cc` and
  `surface_gravity_g_earth` all cascade from a single tie-break choice.
  A measured radius would update all three together, but no transit is
  geometrically expected and the signal is refuted.
- **True mass ≥ M sin i.** The Ma 2018 mass is a radial-velocity
  minimum; the true mass is bounded below by 8.47 M⊕ but unconstrained
  above, and is moot because the signal is not planetary.
- **Cultural-context cross-reference is the canonical home.** Any
  future "Vulcan / Erid" rendering should reference
  `docs/reference/cultural-context.md § 40 Eridani A` rather than
  treating the cfg body as a real detection. The film's deep-blue
  atmosphere + rings are fiction and live only in that document.

## Related

- [40-eridani-a](40-eridani-a.md) — host star Phase 3 (K0.5 V; the
  42-day rotation that masqueraded as Vulcan)
- [tau-cet-e](tau-cet-e.md) — sibling *Project Hail Mary* world
  (Adrian); the other refuted PHM-cultural documented divergence
- [cultural-context](../reference/cultural-context.md) — § 40
  Eridani A, Vulcan in *Star Trek* + Erid in *Project Hail Mary*
- [methodology](../reference/methodology.md) — Decisions schema
