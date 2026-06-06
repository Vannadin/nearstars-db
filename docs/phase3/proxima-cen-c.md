<!-- Proxima Cen c Phase 3 synthesis: cfg-ready decisions and reasoning -->
# Proxima Centauri c — Phase 3 Synthesis

Proxima Centauri c is a **contested radial-velocity candidate** — a
long-period, low-mass companion to the nearest star, reported by Damasso
et al. 2020 (Sci. Adv. 6, eaax7467) as a ~1900-day signal with a minimum
mass of 5.8 ± 1.9 M⊕ at a = 1.48 ± 0.08 AU. If real, it would be a
strikingly cold world: at 1.48 AU around the 0.001567 L☉ flare star
Proxima, the equilibrium temperature is only **T_eq ≈ 39 (+16/−18) K**
(Damasso 2020) — colder than Neptune — and the insolation is just
S ≈ 7.2 × 10⁻⁴ that of Earth. The signal has **never been independently
confirmed**: an Artigau et al. 2022 re-extraction of the HARPS data
found no evidence of it, and the 2025 NIRPS campaign (Suárez Mascareño
et al.) recovered only "inconclusive" hints of a lower-amplitude
long-period signal. Proxima c is included in NearStars as a **documented
candidate**, the same way tau Cet e and 40 Eri A b are — a real entry in
the public record, flagged as unconfirmed.

The science headline of Damasso 2020 is the planet's location: at
1.48 AU it sits far beyond the protoplanetary snow line, which around a
star this faint was within ~0.15 AU. A super-Earth (or larger) so far
out is a challenge for in-situ formation and points to type-II migration
from a few times its current distance. The mass is the second fork. The
RV minimum mass is 5.8 M⊕, but Damasso 2020 notes the Gaia–Hipparcos
proper-motion anomaly (Kervella et al. 2020) is compatible with a **true
mass of ~10–20 M⊕** at 1–2 AU — squarely Neptune-class. A 10–20 M⊕ core
forming in the cold outer disk is the textbook ice-giant channel (Uranus
and Neptune are ~14.5 and ~17 M⊕), so the synthesis adopts the true-mass
reading and renders Proxima c as a **cold ice giant**.

**Scenario choice for NearStars: a deep-blue, ~40 K Neptune-class ice
giant on a wide 1.48 AU circular orbit around Proxima — the cold,
envelope-bearing counterpart to the rocky inner planets b and d, lit by
a dim red pinpoint star and exposed to its giant flares.** The orbit and
the ~39 K temperature are the only measured/derived anchors and are
canonical-aligned; everything visual — the ice-giant nature itself, the
methane-blue tint, the rotation, the offset magnetic field, and the
flare-driven aurora — is a within-window tie-break defaulting to the
Neptune-analog interesting-first reading. The rocky super-Earth
alternative (the 5.8 M⊕ minimum-mass reading) is preserved in
`## Canonical alternatives`. **No ring**: the popular "Proxima c may have
rings" line traces to Gratton et al. 2020's disputed SPHERE counterpart
and to a debated circumstellar dust ring (Anglada 2017 / MacGregor
2018), neither of which is planet-specific ring evidence — `ring_present
= false` per the ring guardrail.

## Decisions

Kopernicus / atmosphere cfg-ready values. `Confidence`: high = directly
measured or tightly constrained, medium = theoretical with strong
support, low = aesthetic choice within the allowed window. Note the
overall low confidence floor: the planet itself is an **unconfirmed,
contested candidate**, so even the "high" rows are conditional on its
existence.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | high | 1.48 AU / 1900-day orbit around a 0.122 M☉ star — tidal-damping timescale ≫ the 4.85 Gyr age; no spin–orbit coupling |
| `eccentricity` | 0.0 | medium | Damasso et al. 2020 — adopted circular (e fixed 0); the free-eccentricity run gave e = 0.41 (+0.34/−0.26) but below the significance threshold, and Bayesian evidence did not favor an eccentric model. Genuinely unconstrained — see Open items |
| `semi_major_axis_au` | 1.48 (±0.08) | high | Damasso et al. 2020 — Table 1 derived parameter (RV + GLS period analysis) |
| `sidereal_period_days` | 1900 (+96/−82) | high | Damasso et al. 2020 — GLS peak ~1907 d, FAP 0.01%; P = 5.21 (+0.26/−0.22) yr |
| `inclination_deg` | unconstrained | low | Damasso et al. 2020 attempted an i/Ω fit to the Hipparcos–Gaia proper-motion anomaly but could not state whether the Δμ is due to Proxima c. A coplanar-with-disk solution (i ≈ 45°, m = 8.2 M⊕) is one literature option; cfg leaves orbit inclination a low-confidence pick |
| `mass_mearth` | ~14 | low | Tie-break: the Gaia–Hipparcos PMa true mass ~10–20 M⊕ (Kervella et al. 2020, as cited by Damasso 2020); midpoint ~14 M⊕ adopted for the ice-giant reading. RV minimum mass is 5.8 ± 1.9 M⊕ — see Canonical alternatives |
| `mass_mjup` | ~0.044 | low | = ~14 M⊕ / 317.8 |
| `radius_rearth` | ~3.8 | low | Tie-break: no transit (TESS/ground searches find none). Mass–radius inference for a ~14 M⊕ ice giant ≈ Neptune (3.88 R⊕); cfg picks ~3.8 R⊕ |
| `surface_gravity_g_earth` | ~1.0 | low | derived: g = M/R² = 14/3.8² ≈ 0.97 g⊕ (cf. Neptune 1.14) |
| `density_g_cc` | ~1.4 | low | derived: 14 M⊕ in a 3.8 R⊕ sphere ≈ 1.4 g/cc — ice-giant range (cf. Neptune 1.64) |
| `insolation_s_earth` | 0.00072 | high | derived: S = L/a² = 0.001567 L☉ / (1.48 AU)² ≈ 7.2 × 10⁻⁴ S⊕ — negligible; a deep-cold world |
| `equilibrium_temp_k` | 39 (+16/−18) | high | Damasso et al. 2020 (Table 1 derived). Independent recompute: T_eq = 278.3 × (L/a²)^0.25 ≈ 45 K (A = 0), ≈ 42 K (A = 0.3) — consistent |
| `bond_albedo` | 0.30 | low | Tie-break: Neptune-analog (Neptune ≈ 0.29); high-cloud/haze albedo for a cold methane atmosphere. Aesthetic within the no-measurement window |
| `atmosphere_present` | true | low | Tie-break: a ~10–20 M⊕ core forming in the cold outer disk retains an H₂/He envelope (ice-giant channel). If the true mass is the 5.8 M⊕ minimum, a thinner volatile envelope is possible — see Canonical alternatives |
| `atmosphere_reference_pressure_pa` | 100000 | low | ice giant has no solid surface; 1 bar cfg reference for cloud-deck rendering |
| `atmosphere_composition` | H₂/He bulk with CH₄ (methane), Neptune-class; condensed CH₄/N₂ haze likely at ~40 K | low | Tie-break: no measurement. Modeled on Neptune/Uranus ice-giant chemistry; at ~40 K methane largely condenses out of the upper layers, leaving residual gas-phase CH₄ absorption + ice haze |
| `atmosphere_tint_rgb_hex` | `#2f5fb0` (deep methane blue, dimmer/cooler than Neptune) | low | Tie-break: gas-phase CH₄ absorbs red light → the Neptune blue; at ~40 K with more CH₄ condensation the cast is slightly muted/hazier than Neptune's vivid `#4170d0`. Interesting-first vivid ice-giant blue |
| `cloud_cover_fraction` | 0.6 | low | Tie-break: a cold ice giant with patchy methane-ice/haze cloud bands (Neptune-like) rather than a uniform deck; no measurement |
| `cloud_morphology` | faint zonal banding with patchy bright methane-ice clouds over a deep blue methane atmosphere; Neptune-analog, muted by the cold | low | Tie-break: Neptune/Uranus morphology scaled to a colder, dimmer-lit world; minimal storm activity expected at 7 × 10⁻⁴ S⊕ |
| `cloud_tint_rgb_hex` | `#cfe0ec` (pale icy-white methane clouds) | low | Tie-break: methane-ice clouds are near-white with a faint cold-blue cast against the deep-blue gas; Neptune's bright cloud streaks analog |
| `rotation_period_hours` | 16 | low | Tie-break: no measurement. Neptune-analog (~16 h) picked — an ice giant inherits a large angular-momentum budget; rapid rotation drives the faint zonal banding |
| `obliquity_deg` | 28 | low | Tie-break: Neptune-analog 28.3° picked for a visually distinct tilt; no measurement. Negligible seasonal effect at this insolation |
| `magnetic_field_strength_microtesla_equator` | 1.4 | low | Tie-break: ice-giant offset/tilted dynamo scaled to Neptune's surface field (~1.4 µT equatorial mean); offset dipole assumed for asymmetric aurorae. No measurement |
| `magnetic_dipole_tilt_deg` | 47 | low | Tie-break: Neptune's strongly tilted (47°) offset dipole picked over a Jupiter-like aligned field — characteristic of ice giants and visually interesting for off-axis aurorae |
| `aurora_present` | true | low | Tie-break (physically gated): Proxima is a superflare star (Howard 2018; Vida 2019); an ice-giant magnetosphere at 1.48 AU would channel flare-driven plasma into aurorae. Faint (the planet is far and the field weak), flagged low-confidence |
| `aurora_color_primary_hex` | `#e0507a` (H Balmer / H₂ pink-red) | low | Tie-break: an H₂/CH₄ atmosphere aurora emits in hydrogen Balmer + H₂ bands (pink-red), distinct from Earth's green [O I] — Jupiter/ice-giant H₂ aurora analog |
| `aurora_emission_species_primary` | H Balmer (Hα 656 nm) + H₂ Lyman/Werner bands | low | Tie-break: hydrogen-dominated atmosphere; no measurement |
| `ring_present` | false | high | No planet-specific ring evidence. The "Proxima c rings" story traces to Gratton et al. 2020's disputed SPHERE direct-imaging counterpart and to a debated circumstellar inner dust ring (Anglada et al. 2017; debated by MacGregor et al. 2018) — neither is a circumplanetary ring. Ring guardrail: omit |
| `ring_observed` | false | high | Damasso 2020 is an RV detection; no imaging resolves a ring, and the candidate itself is unconfirmed |
| `star_apparent_angular_diameter_deg` | 0.051 | high | derived: 2 R_star / a = 2 × 0.141 R☉ / 1.48 AU ≈ 0.051° — about 1/10 the Sun's angular size from Earth; Proxima is a small, dim red pinpoint |
| `stellar_illumination_color_temp_k` | 2904 | high | inherited from host Phase 3 (`docs/phase3/proxima-cen.md`) — Teff 2904 K, deep-red M5.5Ve |

## Surface synthesis

Proxima c has no solid surface to render under the adopted ice-giant
reading — it is a ~14 M⊕ H₂/He envelope over an icy/rocky core, a
Neptune-class world. The "surface" for rendering purposes is the cloud
deck, and at ~39 K that deck is dominated by methane.

The temperature is the controlling fact. At 1.48 AU around a 0.001567 L☉
star the equilibrium temperature is only ~39–45 K (Damasso 2020;
recompute), colder than Neptune's ~47 K. At this temperature methane
largely condenses out of the upper atmosphere into ice clouds and haze,
while residual gas-phase CH₄ below the condensation level still absorbs
red light and produces the characteristic ice-giant blue. The cfg
renders Proxima c as a **deep methane-blue world** (`#2f5fb0`) — slightly
muted and hazier than Neptune's vivid blue because the extra cold drives
more methane condensation. Bright methane-ice cloud streaks
(`#cfe0ec`) sit over the deep-blue gas, in faint zonal bands, with the
band contrast suppressed by the weak insolation: at 7 × 10⁻⁴ Earth's
sunlight there is almost no stellar drive for storms, so the deck is
calmer and more uniform than Neptune's.

This is deliberately the **cold, envelope-bearing counterpart** to
Proxima's inner planets. Proxima b is a temperate, possibly-ocean-bearing
rocky world at 0.0485 AU and Proxima d is a hot Mercury-analog at
0.029 AU; Proxima c, far out at 1.48 AU, is the system's ice giant — a
single dim blue disk a tenth the size of the inner pair's rocky bodies in
mass terms but visually the largest body in the system after the star.

## Atmosphere synthesis

**Pressure reference.** An ice giant has no solid surface; the cfg
reference pressure is 1 bar (100 000 Pa), used only to anchor the
cloud-deck rendering. The physically meaningful level is the methane
condensation layer in the upper troposphere.

**Composition.** No atmosphere of Proxima c has been measured — it is an
RV candidate with no transit, no spectrum, and no confirmed existence.
The composition is inferred entirely from the adopted ~14 M⊕ ice-giant
mass: an H₂/He bulk envelope with methane as the dominant minor species,
exactly as for Neptune and Uranus. At ~40 K the methane is near or below
its condensation point, so the upper atmosphere is depleted in gas-phase
CH₄ (forming ice haze) while deeper layers retain enough to colour the
planet blue. The cfg encodes this at low confidence — it is the
Neptune-analog default, not a measurement.

**Sky appearance from a cloud-top / moon observer.** From the cloud tops
the sky is a deep methane blue overcast, lit by a small, dim, deep-red
star. Proxima subtends only ~0.051° at 1.48 AU — about a tenth the Sun's
angular size from Earth — a faint red pinpoint delivering ~7 × 10⁻⁴
Earth's insolation, so the dayside is extremely dim, more a deep twilight
than a day. Across the sky, far brighter than Proxima would be the
distant pair α Centauri A and B (Proxima orbits the AB pair at
~13 000 AU), appearing as a brilliant close double "evening star."

**Nightside and flares.** With negligible insolation the planet is cold
and dark, but Proxima is a superflare star: its giant flares (Howard
2018; the 2019 ASAS-SN/Evryscope superflare, Vida 2019) flood the system
with energetic particles. An ice-giant magnetosphere at 1.48 AU — modeled
on Neptune's strongly tilted, offset dipole — would channel that plasma
into **faint, off-axis aurorae** glowing pink-red in hydrogen Balmer and
H₂ emission (`#e0507a`), distinct from Earth's green oxygen aurora. The
flux is diluted by the 1.48 AU distance and the weak field, so the cfg
flags the aurora as faint and low-confidence — a tie-break, not a
measurement, but a physically motivated one given the flare host.

## Rotation & spin synthesis

No rotation measurement of Proxima c exists — it is an unconfirmed RV
candidate with no resolved disk.

**Tidal damping argument.** At 1.48 AU around a 0.122 M☉ star, the tidal
timescale for a Neptune-class planet vastly exceeds the 4.85 Gyr age, so
Proxima c is **not** tidally locked (`tidally_locked = false`) — unlike
its tidally-locked inner siblings b and d.

**Rotation period choice.** Ice giants inherit large angular-momentum
budgets from disk accretion and rotate quickly; the cfg picks a
Neptune-analog `rotation_period_hours = 16` as a within-window tie-break.
Rapid rotation drives the faint zonal banding, though the band contrast
is muted by the very weak insolation.

**Obliquity.** Tie-break aesthetic: 28° (Neptune-analog 28.3°) for a
visually distinct tilt. At 7 × 10⁻⁴ Earth's insolation the obliquity
drives no observable seasonal effect — the planet is uniformly cold.

**KSP implementation note.** Rotation period = 16 h = 57 600 s
(`rotationPeriod = 57600`); obliquity ≈ 28° from the orbital normal.

## Visual styling

Combining the surface (cloud-deck) and atmosphere decisions, Proxima c
renders as a cold, deep-blue ice giant — the system's outermost and
largest body after the star:

- **Global appearance.** From orbit, a deep methane-blue disk
  (`#2f5fb0`) about 3.8 R⊕ (~48 000 km) across — a Neptune-class world,
  muted and slightly hazier than Neptune itself because the extra cold
  (~40 K vs Neptune's ~47 K) drives more methane condensation.
- **Cloud-deck detail.** Faint zonal bands with patchy bright methane-ice
  cloud streaks (`#cfe0ec`) over the deep-blue gas. Storm activity is
  minimal at 7 × 10⁻⁴ Earth's insolation — calmer and more uniform than
  Neptune's banded disk.
- **Limb haze.** A pale, cold-blue methane-ice haze at the limb, a thin
  bright halo over the deep-blue body.
- **Nightside and aurora.** Dark and cold on the nightside, with faint
  pink-red (`#e0507a`) hydrogen aurorae in off-axis ovals where Proxima's
  flare plasma reaches the strongly tilted ice-giant field. Faint and
  intermittent, tied to flare events.
- **Star in sky.** Proxima subtends only ~0.051° — about 1/10 the Sun's
  angular size from Earth — a dim deep-red (M5.5Ve, `#c54c2a`) pinpoint
  delivering ~7 × 10⁻⁴ Earth's insolation. The dayside is a deep red
  twilight, not a true day.
- **α Cen AB in sky.** The bright G2V + K1V pair α Centauri A and B, at
  ~13 000 AU, appears as a brilliant close double — the most prominent
  "star" in Proxima c's sky after Proxima itself.
- **No ring.** `ring_present = false` — there is no planet-specific ring
  evidence (see Canonical alternatives / Open items for the disputed
  imaging story).

## Canonical alternatives

The cfg renders the **ice-giant (true-mass) reading**; a co-existing
literature reading is the rocky/icy super-Earth at the RV minimum mass.

| cfg pick | Canonical alternative | Why cfg diverges |
|---|---|---|
| `mass_mearth ≈ 14` (Neptune-class ice giant, H₂/He envelope) | **`mass_mearth = 5.8 ± 1.9` (RV minimum mass, Damasso 2020)** — a rocky/icy super-Earth with at most a thin volatile envelope; `radius ≈ 1.8–2.2 R⊕`, no significant gas envelope, an airless or thin-atmosphere frozen body at ~40 K | The 5.8 M⊕ value is a **minimum** (m sin i); the Gaia–Hipparcos PMa true mass is ~10–20 M⊕ (Kervella 2020), which lands in the ice-giant regime. The cfg adopts the true-mass reading because it is (a) the physically expected outcome of a 10–20 M⊕ core in the cold outer disk and (b) far more visually distinctive than a small frozen rock. Users wanting the minimum-mass reading should render a ~2 R⊕ frozen super-Earth instead |

A second alternative noted by Damasso 2020: if Proxima c is **coplanar
with the candidate ALMA cold dust belt** (i ≈ 45°), its true mass is
~8.2 M⊕ — still a super-Earth/sub-Neptune, between the two readings
above. The cfg's ~14 M⊕ sits within the PMa range; 8.2 M⊕ is the
lower-inclination edge.

## Bibliography

### Read (drove decisions above)

- **Damasso M. et al. 2020** — *A low-mass planet candidate orbiting
  Proxima Centauri at a distance of 1.5 AU*, Sci. Adv. 6, eaax7467
  (`2020SciA....6.7467D`, doi:10.1126/sciadv.aax7467). **The only primary
  source.** RV candidate: P = 1900 (+96/−82) d, a = 1.48 ± 0.08 AU,
  m sin i = 5.8 ± 1.9 M⊕, T_eq ≈ 39 (+16/−18) K, e fixed 0 (free run
  e = 0.41, not significant). Gaia–Hipparcos PMa compatible with a true
  mass ~10–20 M⊕ (citing Kervella 2020). Forms beyond the snow line →
  type-II migration. Explicitly a candidate requiring follow-up. **Has no
  arXiv preprint**; full text cached from open-access PMC6962037. Drives
  every orbit/mass/temperature row.

### Read (context — dispute / non-recovery)

- **Suárez Mascareño A. et al. 2025** — NIRPS Proxima campaign
  (`2507.21751`). Reports **inconclusive evidence** for the 1900-d signal:
  a low-amplitude (58 ± 28 cm/s, < 1.4 m/s at 99.7%) long-period hint at
  ~1800 d, "not fully compatible" with Damasso's amplitude. "No conclusive
  evidence was found for Proxima c." The most recent test; lowers the
  confidence floor.
- **Faria J. P. et al. 2022** — ESPRESSO Proxima d discovery
  (`2202.05188`). Notes Proxima c "has so far eluded a clear detection
  with direct imaging or astrometry (Gratton 2020; Kervella 2020;
  Benedict & McArthur 2020)"; ESPRESSO's ~815-d baseline is too short
  (~2.3× shorter than P_c) to test the 1900-d signal — a non-test, not a
  refutation.
- **Suárez Mascareño A. et al. 2020** — "Revisiting Proxima with
  ESPRESSO" (`2005.12114`). States re-testing Proxima c is beyond the
  paper's (short-baseline) scope. Non-test.
- **Artigau É. et al. 2022** (not in cache; via NIRPS 2025) — a HARPS
  re-extraction with a different RV method **could not find evidence** of
  Proxima c. The principal dispute.

### Not read — cited only, no full text in cache

- **Kervella P. et al. 2020** (Gaia–Hipparcos PMa true masses) — the
  source of the ~10–20 M⊕ true-mass range, quoted via Damasso 2020;
  full text not cached.
- **Gratton R. et al. 2020** (SPHERE direct-imaging counterpart) and
  **Benedict & McArthur 2020** (HST astrometry) — both cited as having
  Proxima c "elude a clear detection"; the disputed Gratton SPHERE
  candidate is the origin of the popular "rings" story but is not
  cache-verifiable and is characterised as a non-detection.
- **Anglada G. et al. 2017** / **MacGregor M. et al. 2018** — the
  candidate ALMA inner dust ring at 1–4 AU and its rebuttal (attributing
  the ALMA point source to a stellar flare); a circumstellar feature,
  debated, not a planetary ring.

## Open items for follow-up

- **Existence.** Proxima c is the catalog's most contested planet entry.
  Confirmation requires the longer RV baseline now accumulating (ESPRESSO
  + NIRPS) or a Gaia DR4 astrometric detection. If it is refuted outright,
  it should be reclassified (like a hardened tau Cet e); if confirmed and
  its true mass pinned, the mass/radius/nature rows should be re-derived.
- **Mass and nature.** The ice-giant vs rocky-super-Earth fork
  (`## Canonical alternatives`) turns entirely on the true mass. Gaia DR4
  astrometry should resolve it; the cfg should switch to the rocky reading
  if the true mass comes in near the 5.8 M⊕ minimum.
- **Eccentricity.** Adopted circular (Damasso fixed e = 0), but the
  free-eccentricity run gave e = 0.41 (+0.34/−0.26) — genuinely
  unconstrained. A future cfg could adopt a moderate eccentricity if
  follow-up favors it; the synthetic-eccentricity layer (project policy)
  is **not** applied here because e is a (loosely) measured quantity.
- **Inclination.** Unconstrained; the coplanar-with-disk i ≈ 45° / m =
  8.2 M⊕ option is one literature anchor. A measured astrometric
  inclination would fix both the orbit and the true mass.
- **Atmosphere.** Entirely inferred (no transit, no spectrum). The
  methane-blue ice-giant composition is a Neptune-analog default; it
  cannot be measured for a non-transiting RV candidate at 1.48 AU with
  current instruments.

## Related

- [proxima-cen](proxima-cen.md) — host star Phase 3 synthesis; provides
  the M5.5Ve Teff / L / mass / radius, the superflare context, and the
  illumination-color-temperature reference
- [proxima-cen-b](proxima-cen-b.md) — the temperate inner rocky planet;
  contrast b's possible-ocean eyeball world against c's cold ice giant
- [proxima-cen-d](proxima-cen-d.md) — the hot inner Mercury-analog;
  the third member of the Proxima system
- [eps-ind-a-b](eps-ind-a-b.md) — comparison cold giant around a nearby
  dwarf; contrast ε Indi A b's massive, internal-heat-dominated
  super-Jupiter against Proxima c's small, insolation-cold ice giant
- [methodology](../reference/methodology.md) — Decisions schema
- [mod-reference](../reference/mod-reference.md) — downstream Kopernicus /
  EVE cfg writers consuming this ice giant's atmosphere + aurora decisions
