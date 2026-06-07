<!-- Alpha Centauri A b Phase 3 synthesis: cfg-ready decisions and reasoning -->
# α Centauri A b — Phase 3 Synthesis

α Centauri A b ("S1") is a **JWST direct-imaging candidate** — a
Saturn-class giant point source detected once, in August 2024, with
JWST/MIRI's F1550C coronagraph (15.5 µm) at a projected separation of
1.51″ (~2 AU) from the nearest Sun-like star (Beichman et al. 2025,
"Worlds Next Door I"; Sanghi & Beichman et al. 2025, "II"). The detection
is faint — 3.5 ± 1.0 mJy, S/N 4–6 (≈4σ) — and was **not recovered** at
two 2025 follow-up epochs, though orbit-fitting shows ~52% of the
dynamically stable orbits are consistent with the planet simply having
moved into a low-sensitivity region. The authors link S1 to **C1**, the
2019 VLT/NEAR candidate (Wagner et al. 2021), as the same object, and
rule out detector, PSF, background, and Solar-System-object explanations.
It is a genuine, well-vetted **candidate**, included in NearStars as a
documented candidate (the tau Cet e / 40 Eri A b pattern) — the nearest
candidate gas giant around a solar twin.

Everything physical is **model-derived from two mid-IR photometric points
plus an orbit family**, not measured. The orbit splits into four stable
families — {prograde, retrograde} × {a < 2 AU, a > 2 AU} — with
eccentricity e ≈ 0.4 and periods of 2–3 yr; the authors favor the
**a < 2 AU family** (a ≈ 1.6 AU, T_eq ≈ 225 K) because the higher
temperature better fits the F1550C brightness. The mass is **Saturn-class,
90–150 M⊕**, set by atmosphere fits restricted to log g 2.5–3.0 to respect
the RV upper limits (Zhao et al. 2018). The favored atmosphere is a cool
(~225 K), metal-enriched ([M/H] +0.5 to +1.0) H₂/He giant with **water
clouds** — at this temperature ammonia has rained out and water is the
condensing species, putting α Cen A b near the Sudarsky Class I/II
water-cloud boundary.

The discovery paper offers a striking alternative for the same brightness:
**a smaller (~1 R_Jup, ~120 M⊕) planet girdled by an optically thick
circumplanetary ring** (Beichman §5.3) — a ring of cross-section
~64 000 km (≈ 0.9 R_Jup, about half Saturn's ring extent), sitting in the
Roche zone (1.4–2.5 planetary radii) at ~209–257 K with an asteroid-like
dark albedo. Because this ring reading is **paper-grounded** (not an
invention), and because a ringed giant around the nearest Sun-like star is
the more distinctive render, the cfg adopts it.

**Scenario choice for NearStars: a temperate (~225 K) Saturn-class gas
giant on a stability-selected near-circular (e ≈ 0.1) ~1.6 AU orbit around
the G2V solar twin α Centauri A, girdled by a dark, optically thick rocky
ring — a single-roll JWST candidate, set in the close eccentric α Cen AB
binary at a mutual inclination of ~16° (the observed ~50° is
Kozai-unstable).** The mass, temperature, and water-cloud atmosphere are
the paper's favored solution and are canonical-aligned, while the orbit's
eccentricity and inclination are NearStars stability-selected (the observed
e ≈ 0.4 / i ≈ 50° orbit is Kozai-unstable, see `## Canonical
alternatives`); the ring (vs a ring-free 1.1 R_Jup inflated giant), the
pale cloud tint, rotation, and obliquity are tie-breaks. The ring-free
reading is preserved in `## Canonical alternatives`.

## Decisions

Kopernicus / atmosphere cfg-ready values. `Confidence`: high = directly
measured or tightly constrained, medium = theoretical with strong
support, low = aesthetic choice within the allowed window. Overall floor:
the planet is an **unconfirmed single-roll candidate**, so "high" rows are
conditional on its existence and on the favored orbit family.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | high | ~1.6 AU orbit around a 1.1 M☉ star — tidal timescale ≫ the 5.3 Gyr age; no spin–orbit coupling |
| `eccentricity` | 0.1 | medium | NearStars stability-selected (median of the HZ-stable range 0–0.18 from a REBOUND/IAS15 scan). The Beichman-observed e ≈ 0.4 (families 0.33–0.46) is Kozai-unstable at the observed inclination — see Canonical alternatives |
| `semi_major_axis_au` | 1.6 | medium | Beichman et al. 2025 §5.3 — the **a < 2 AU family is favored** (higher T_eq fits F1550C); a ≈ 1.58–1.68 AU. The Phase 2 DB representative was reconciled from 1.9 AU to 1.6 AU (P 705 d) to match this favored family, so the in-game orbit tracks the synthesis |
| `sidereal_period_yr` | ~2.0 | medium | Beichman et al. 2025 — 2–3 yr range; ~2 yr for the favored a ≈ 1.6 AU / 1.1 M☉ |
| `mutual_inclination_deg` | 16 | medium | NearStars stability-selected (median of the HZ-stable range 0–35° from a REBOUND/IAS15 scan). Beichman Table 4 gives the OBSERVED ≈50° (prograde) / ≈130° (retrograde) wrt the α Cen AB plane (i_AB = 79.24°), but ≳35° drives the orbit out of the HZ and ≳45° is Kozai-unstable — see Canonical alternatives |
| `inclination_deg` | unset | low | The constrained quantity is the mutual inclination to the AB plane (row above); the sky-plane inclination is bimodal/weak (Beichman Table 4). cfg-frame inclination left as an open item |
| `mass_mearth` | 120 | medium | Beichman et al. 2025 — Saturn-class, 90–150 M⊕ (Saturn = 95); ring-model solution ~120 M⊕. Atmosphere fits restricted to log g 2.5–3.0 to respect RV limits (Zhao 2018: M sin i < 100 M⊕ for P ≲ 1000 d) |
| `mass_mjup` | 0.38 | medium | = 120 M⊕ / 317.8 |
| `radius_rjup` | 1.0 | low | Tie-break: the **ring-model** radius (Beichman §5.3); the ring-free atmosphere fit gives ~1.1–1.15 R_Jup (inflated for a 5 Gyr giant). cfg adopts 1.0 R_Jup with the ring carrying the extra cross-section |
| `radius_rearth` | 11.2 | low | = 1.0 R_Jup |
| `surface_gravity_g_earth` | ~0.96 | low | derived: g = M/R² = 120/11.2² ≈ 0.96 g⊕ (log g ≈ 2.97 cgs) — consistent with the paper's assumed log g 2.75–3.0 |
| `density_g_cc` | ~0.5 | low | derived: 120 M⊕ in a 1.0 R_Jup sphere ≈ 0.47 g/cc — a low-density Saturn-class giant (cf. Saturn 0.69) |
| `insolation_s_earth` | 0.59 | medium | derived: S = L/a² = 1.521 L☉ / (1.6 AU)² ≈ 0.59 S⊕ (the disfavored a ≈ 2.1 AU family gives ≈ 0.34 S⊕). Beyond the outer HZ (EEID ≈ 1.23 AU) — a cold giant, not a temperate world |
| `equilibrium_temp_k` | 225 | medium | Beichman et al. 2025 — flux-averaged T_eq with A_B = 0.3, f = 1, for the favored a < 2 AU family (a > 2 AU gives ~195 K). Recompute: 278.3 × (L/a²)^0.25 × 0.7^0.25 ≈ 224 K at a = 1.6 AU — consistent |
| `effective_temp_k` | ~225 | medium | Beichman et al. 2025 — internal heat negligible (T_int < 110 K, Jupiter/Saturn analog); the radiating temperature ≈ the equilibrium temperature, unlike the self-luminous ε Indi A b |
| `bond_albedo` | 0.30 | medium | Beichman et al. 2025 — assumed intermediate between hot Jupiters and Solar-System giants for the T_eq derivation |
| `atmosphere_present` | true | high | gas giant; H₂/He bulk with metal enrichment and water clouds (Beichman model fits) |
| `atmosphere_reference_pressure_pa` | 100000 | medium | gas giant has no solid surface; 1 bar cfg reference for cloud-deck rendering |
| `atmosphere_composition` | H₂/He bulk; metal-enriched [M/H] +0.5 to +1.0; **H₂O the condensing cloud species** (NH₃ rained out at 225 K); CH₄/NH₃/H₂O in rainout chemistry | medium | Beichman et al. 2025 — C/O is fit-dependent: 2.5× solar in the §5.2 cloudy water-cloud fits (Sonora Flame Skimmer / PICASO, log g 2.75, K_zz 10⁹, f_sed 6), 1.5× in the §5.3 clear model paired with the adopted ring. Solar-metallicity & hotter (≥250 K) models failed the photometry. cfg renders water clouds as the physically expected deck at 225 K |
| `atmosphere_tint_rgb_hex` | `#dfe3e8` (pale cool-white water-cloud giant) | low | Tie-break: no visible-light data (two mid-IR points only). A ~225 K water-cloud giant near the Sudarsky Class I/II boundary reads as a bright, pale, high-albedo body — distinct from Jupiter's warm cream; faint warm bias from the G2V (5847 K) light |
| `cloud_cover_fraction` | 0.9 | low | Tie-break: a cool water-cloud deck (f_sed 6 ⇒ moderately compact clouds); high coverage typical of Class II giants. No measurement |
| `cloud_morphology` | near-global pale water-cloud deck with faint zonal banding; cool Class-I/II giant, more uniform and brighter than Jupiter | low | Tie-break: scaled from the Beichman water-cloud best fit; modest belt–zone contrast at 225 K with metal enrichment |
| `cloud_tint_rgb_hex` | `#eef1f4` (near-white water clouds) | low | Tie-break: water clouds are intrinsically near-white; under G2V light the deck reads bright pale-white, brighter than the limb |
| `rotation_period_hours` | 10 | low | Tie-break: no measurement. Saturn/Jupiter-analog ~10 h; Beichman §5.3 notes the 1.1 R_Jup atmosphere fit could imply rapid rotation viewed near pole-on, consistent with a fast spin |
| `obliquity_deg` | 27 | low | Tie-break: Saturn-analog 26.7° picked for a visually distinct tilt that reads naturally with the ring plane; no measurement |
| `ring_present` | true | low | **Documented divergence** (see Canonical alternatives): Beichman et al. 2025 §5.3 offers an optically thick circumplanetary ring as a co-equal explanation of the F1550C brightness. Paper-grounded (passes the ring guardrail); cfg picks it as the more distinctive render |
| `ring_inner_radius_bodyradii` | 1.4 | low | Beichman §5.3 — ring sits in the Roche zone, ~1.4–2.5 planetary radii. Kopernicus `Ring` innerRadius as a body-radius multiplier |
| `ring_outer_radius_bodyradii` | 2.5 | low | Beichman §5.3 — Roche-zone outer edge; cross-section ~64 000 km ≈ 0.9 R_Jup, about half Saturn's ring extent |
| `ring_color_hex` | `#6e6253` (dark warm grey — rocky/dusty, low albedo) | low | Tie-break: Beichman §5.3 assumes an asteroid-like Bond albedo A_B ≈ 0.1 for the ring → a **dark rocky/dusty ring**, not Saturn's bright ice. Ring T ≈ 209–257 K |
| `ring_opacity` | 0.85 | low | Beichman §5.3 — "optically thick" ring (the whole point is to add enough cross-section to match the brightness) |
| `ring_observed` | false | high | The ring is a **model interpretation** of the F1550C brightness, not resolved; S1 is an unresolved point source |
| `magnetic_field_strength_microtesla_equator` | 500 | low | Tie-break: Saturn-analog dynamo (~500 µT-class) for a Saturn-mass giant; no measurement |
| `aurora_present` | false | medium | The quiet G2V wind (log R'HK = −4.95) at 1.6 AU is a weak plasma driver; like the other quiet-host giants, no strong aurora expected. cfg renders none |
| `star_apparent_angular_diameter_deg` | 0.41 | high | derived: 2 R_star / a = 2 × 1.2234 R☉ / 1.6 AU ≈ 0.41° — slightly smaller than the Sun from Earth (0.53°). Varies over the orbit: ~0.45° at periastron (1.44 AU), ~0.37° at apastron (1.76 AU) |
| `stellar_illumination_color_temp_k` | 5847 | high | inherited from host Phase 3 (`docs/phase3/alpha-centauri-a.md`) — G2V, near-white warm sunlight |
| `companion_stars_in_sky` | α Cen B (K1V) at 11.2–35.6 AU; Proxima (M5.5Ve) at ~13 000 AU | high | Akeson et al. 2021 / Kervella 2017 — the eccentric K-dwarf companion is a brilliant second "sun"; Proxima a faint red point |

## Surface synthesis

α Centauri A b has no solid surface — it is a ~120 M⊕ Saturn-class H₂/He
giant. The "surface" for rendering is the cloud deck, and at ~225 K that
deck is set by water.

The temperature regime is the key to the palette. At 1.6 AU around the
1.521 L☉ G2V star, the equilibrium temperature is ~225 K for the favored
orbit family (Beichman 2025; recompute ≈ 224 K at A_B = 0.3). This is
warmer than Jupiter (~165 K) and Saturn (~134 K), warm enough that
**ammonia has rained out** and **water is the condensing cloud species** —
placing α Cen A b near the Sudarsky Class I/II boundary. Water-cloud
giants in this regime are bright, pale, and high-albedo, so the cfg
renders the body as a **pale cool-white world** (`#dfe3e8` atmosphere,
`#eef1f4` clouds) with only faint zonal banding — distinct from Jupiter's
warm cream-amber. The metal enrichment ([M/H] +0.5 to +1.0, C/O ~2.5×
solar; Beichman §5.2) and a moderate cloud compactness (f_sed 6) leave
modest belt–zone contrast, brighter and more uniform than Jupiter.

Because internal heat is negligible (T_int < 110 K; Beichman §5.1), the
appearance is **insolation-set** — unlike the self-luminous super-Jupiter
ε Indi A b, α Cen A b glows only as warm as its starlight makes it. The
e ≈ 0.1 orbit swings the planet from ~1.44 AU (periastron) to ~1.76 AU
(apastron), a mild ~1.5× insolation range, so the cloud deck likely
brightens and the banding sharpens slightly near periastron — a gentle
seasonal cycle on a ~2-yr period.

The defining visual is the **ring**. Adopting Beichman §5.3, α Cen A b
carries a dark, optically thick rocky ring in its Roche zone (1.4–2.5
planetary radii), of cross-section ~0.9 R_Jup — about half the extent of
Saturn's rings. With an asteroid-like albedo (A_B ≈ 0.1) and a temperature
of ~209–257 K, this is a **dark dusty ring** (`#6e6253`), not Saturn's
brilliant ice — a sombre, dust-coloured girdle around a pale giant.

## Atmosphere synthesis

**Pressure reference.** A gas giant has no solid surface; the cfg
reference pressure is 1 bar (100 000 Pa), anchoring the cloud-deck render.
The physically meaningful level is the water-cloud top.

**Composition.** Bulk H₂/He, as for any giant. The Beichman 2025
atmosphere fits that match the two mid-IR points require **metal
enrichment** ([M/H] +0.5 to +1.0) and a cool ~225 K profile in which
ammonia, methane, and water are in rainout chemistry — at 225 K ammonia
has condensed/rained out below the visible deck and **water is the
condensing cloud species**. The C/O ratio is fit-dependent: the §5.2
cloudy water-cloud fits use C/O ~2.5× solar, while the §5.3 model paired
with the adopted ring is a clear atmosphere with C/O 1.5× and [M/H] +1.0.
Solar-metallicity and hotter (≥250 K) models failed the photometry, so the
metal-rich reading is the paper's preferred fit; the cfg renders water
clouds as the physically expected deck at 225 K and encodes the
composition at medium confidence (model-constrained, exact mixing ratios
less so).

**Sky appearance from a cloud-top / moon observer.** From the cloud tops
the sky is a bright pale-white overcast, lit by a near-Sun-like star.
α Cen A subtends ~0.41° at 1.6 AU — a touch smaller than our Sun, swinging
from ~0.45° at periastron to ~0.37° at apastron — a warm-white G2V disk
(`#fff4e8`) delivering ~0.6 Earth's insolation. The dark ring would arc
across the sky as a dusty band, edge-lit by the star. The system's
spectacle is the **companion**: α Cen B, a K1V star, orbits the AB
barycentre on an e ≈ 0.52 path from 11.2 to 35.6 AU, so from α Cen A b it
is a brilliant orange second "sun" — at closest approach hundreds of times
brighter than the full Moon, never a true disk but an intense point. Far
beyond, Proxima hangs as a faint red speck at ~13 000 AU.

**Nightside.** With negligible internal heat the nightside is dark and
cool (~225 K, radiating in the mid-IR — the band JWST detected it in).
The quiet G2V stellar wind is a weak plasma driver, so no significant
aurora is rendered (`aurora_present = false`), unlike the flare-host
giants in the catalog.

## Rotation & spin synthesis

No rotation measurement of α Cen A b exists — it is a single-epoch
imaging candidate.

**Tidal damping argument.** At ~1.6 AU around a 1.1 M☉ star, the tidal
timescale for a Saturn-class giant vastly exceeds the 5.3 Gyr age, so
α Cen A b is **not** tidally locked (`tidally_locked = false`).

**Rotation period choice.** The cfg picks a Saturn/Jupiter-analog
`rotation_period_hours = 10`, a within-window tie-break. Beichman §5.3
notes that the 1.1 R_Jup atmosphere-only radius would be unusually
inflated for a mature giant unless it is **rapidly rotating and viewed
near pole-on** — which is one motivation for the smaller ringed model the
cfg adopts, and is consistent with a fast ~10 h spin.

**Obliquity.** Tie-break aesthetic: 27° (Saturn-analog) for a visually
distinct tilt that reads naturally with the ring plane. The ring is
rendered in the planet's equatorial plane at this obliquity.

**KSP implementation note.** Rotation period = 10 h = 36 000 s
(`rotationPeriod = 36000`); obliquity ≈ 27° from the orbital normal, with
the `Ring` block sharing the equatorial plane.

## Visual styling

Combining the surface (cloud-deck), atmosphere, and ring decisions, α Cen
A b renders as a pale, ringed, temperate Saturn-class giant — the nearest
candidate gas giant around a solar twin:

- **Global appearance.** From orbit, a pale cool-white disk (`#dfe3e8`)
  about 1.0 R_Jup (~71 000 km) across — a Saturn-mass world rendered
  bright and high-albedo (water clouds near the Class I/II boundary),
  deliberately distinct from Jupiter's warm cream-amber.
- **Cloud-deck detail.** A near-global pale water-cloud deck (~90% cover)
  with faint zonal banding (`#eef1f4` clouds) and modest belt–zone
  contrast — brighter and more uniform than Jupiter, sharpening near
  periastron as insolation peaks.
- **Ring.** A dark, dusty, optically thick rocky ring (`#6e6253`) in the
  Roche zone (1.4–2.5 planetary radii), cross-section ~0.9 R_Jup (~half
  Saturn's extent), at ~209–257 K with asteroid-like low albedo — a sombre
  girdle, not Saturn's brilliant ice. Inclined to the 27° obliquity.
- **Limb.** A pale, bright water-cloud limb; thin and near-white.
- **Nightside.** Dark and cool; no significant aurora (quiet G2V wind).
- **Star in sky.** α Cen A subtends ~0.41° (periastron ~0.45°, apastron
  ~0.37°) — a warm-white G2V (`#fff4e8`) near-Sun, ~0.6 Earth's insolation.
- **Companion suns.** α Cen B (K1V) sweeps from 11.2 to 35.6 AU on its
  e ≈ 0.52 orbit — a brilliant orange second sun, intense at periastron;
  far beyond, Proxima (M5.5Ve) is a faint red point at ~13 000 AU. The
  binary setting is the planet's signature: an eccentric S-type giant in a
  close, bright two-star (plus distant red) sky.

## Canonical alternatives

The cfg renders the **ringed** reading; Beichman et al. 2025 §5.3 offers a
co-equal ring-free interpretation of the same F1550C brightness.

| cfg pick | Canonical alternative | Why cfg diverges |
|---|---|---|
| `ring_present = true`, `radius_rjup = 1.0` (smaller planet + optically thick dark ring) | **Ring-free inflated giant: `radius_rjup ≈ 1.1–1.15`, no ring** — the atmosphere-only best fit (Beichman §5.2). The larger radius alone supplies the cross-section that produces the F1550C brightness | Both are explicitly offered by Beichman as fitting the data equally; §5.3 notes 1.1 R_Jup is "more commonly observed for hotter planets" and is only plausible for a mature giant if rapidly rotating / pole-on, which motivates the ring alternative. The cfg picks the ring for visual distinctiveness (interesting-first), since it is paper-grounded and the more striking render. Users preferring the conservative reading should set `ring_present = false` and `radius_rjup = 1.1` |
| `eccentricity = 0.1`, `mutual_inclination = 16°` (stability-selected) | **Observed (Beichman): e ≈ 0.4, mutual inclination ≈ 50°** — the favored imaging-fit orbit | The observed orbit is Kozai-Lidov **unstable**: eccentric KL pumps e past 0.95 within ~30 kyr, periastron then crashing below the stellar radius over ~10⁵ yr (tidal disruption; REBOUND/IAS15, see `STABILITY_REPORT.md`). NearStars takes the median of the HZ-stable range instead. The Avatar canon 1.2 AU is a separate reading — dynamically stable but interior to α Cen A's HZ (too warm), so 1.6 AU is the nearest robust HZ orbit |

A second within-paper fork is the **orbit family**: the cfg uses the
favored a < 2 AU family (a ≈ 1.6 AU, T_eq ≈ 225 K). The a > 2 AU family
(a ≈ 2.1 AU, T_eq ≈ 195 K) is allowed but disfavored (lower T_eq fits the
F1550C brightness less well). The Phase 2 DB orbital is now set to the
favored a ≈ 1.6 AU family (reconciled from an earlier 1.9 AU midpoint).

## Cultural context — Avatar's Polyphemus and Pandora

α Centauri A b is the real-world candidate that the science press and a
2025 follow-up identified with **Polyphemus**, the gas giant of James
Cameron's *Avatar*. In the films' canon Polyphemus is a Saturn-class gas
giant orbiting **Alpha Centauri A** in its habitable zone, with fourteen
moons — the fifth, **Pandora**, is the Na'vi homeworld. The match is close:
a Saturn-class (90–150 M⊕) gas giant, no measured ring, in α Cen A's HZ, at
the nearest Sun-like star. When Beichman et al. 2025 reported S1, NPR and
Live Science called it "a real-life Pandora," and a 2025 astrobiology paper
— *Seeking the Worlds of Avatar* — assessed the prospects for detecting
exactly such habitable-zone moons.

This is naming/lore context only, kept separate from the measured science
above. But the dynamical question it raises is real and is answered in
`phase3/stability-sim`: can a Pandora-class habitable moon survive here? A
REBOUND/IAS15 scan shows the observed eccentric/inclined orbit is
Kozai-unstable (see Canonical alternatives), while the stability-selected
orbit this synthesis uses (a = 1.6 AU, e = 0.1, mutual inclination ≈ 16°)
keeps Polyphemus in the HZ over 10⁵ yr and hosts a Hill-stable Pandora-mass
moon (0.45 M⊕) at ~225 000 km — a ~27 h tidally-locked day with Polyphemus
spanning ~36° of its sky. The Avatar setup is dynamically viable, just not
on the favored *observed* orbit. The Avatar canon places Polyphemus at
1.2 AU; that orbit is dynamically stable but sits interior to α Cen A's
habitable zone (too warm), so 1.6 AU is the nearest robust HZ orbit.

## Bibliography

### Read (drove decisions above)

- **Beichman C. et al. 2025** — *JWST Observations of the Nearest Sun-Like
  Stars: Worlds Next Door I* (`2025ApJ...989L..22B`,
  doi:10.3847/2041-8213/adf53f, arXiv:2508.03814). The discovery paper.
  S1 = F1550C (15.5 µm) detection, 3.5 ± 1.0 mJy, 1.51″ (~2 AU), Aug 2024;
  four stable orbit families (e ≈ 0.4, P 2–3 yr, mutual i ≈ 50°/130°),
  a < 2 AU favored; mass 90–150 M⊕; T_eq ≈ 225 K; metal-rich water-cloud
  atmosphere fits; **§5.3 the ring alternative** (~1 R_Jup + optically
  thick ring, Roche zone, A_B ≈ 0.1). Cornerstone — drives orbit, mass,
  temperature, atmosphere, and ring rows.
- **Sanghi & Beichman et al. 2025** — *Worlds Next Door II*
  (arXiv:2508.03812). The detection-vetting + orbit-dynamics paper.
  S/N 5.4 (≈4σ) PCA-KLIP detection; rules out detector / ε Mus PSF /
  α Cen B speckle / background / Solar-System-object explanations; links
  S1 to the 2019 VLT/NEAR **C1** (Wagner et al. 2021); ~52% of stable
  orbits consistent with the 2025 non-recoveries. Drives the
  detection-status framing and the candidate flag.

### Read (context / instrument-only, not decision-driving)

- **Wagner K. et al. 2021** (VLT/NEAR, cited) — the 2019 **C1** candidate
  (11.25 µm, 1.2 ± 0.4 mJy, ~1.1 AU), originally read as a ≳300 K planet
  (radius ≳ 3.3 R⊕) or a 60-zodi dust clump; the JWST exozodi non-detection
  favors the planet interpretation, and S1+C1 are treated as one object.
- **Zhao et al. 2018** (cited) — α Cen A RV upper limits (M sin i ≲ 100 M⊕
  for P ≲ 1000 d) that bound the mass; α Cen A b is built to respect them.
- **Akeson R. et al. 2021** (cited) — α Cen AB orbit (i_AB = 79.24°,
  Ω_AB = 205.07°) used to convert the mutual inclination to the sky plane.

### Not read — no arXiv full text / superseded

- The PICASO / Sonora Flame Skimmer / ATMO2020++ model grids underlying
  the atmosphere fits are read for the best-fit parameters already cited
  but contribute no further cfg number. Comparable-system references
  (HD 196885 Ab, γ Cep Ab — S-type planets in close eccentric binaries)
  frame the architecture but add no per-planet visual field.

## Open items for follow-up

- **Existence / recovery.** S1 is a single-roll detection not recovered in
  2025. Confirmation needs a JWST epoch catching it back in the
  detectable separation range (~52% of orbits predict recovery on the next
  favourable epoch) or an independent imaging detection. If refuted, the
  entry should be reclassified.
- **DB semi-major-axis (resolved).** The Phase 2 DB orbital originally used
  a = 1.9 AU (P = 2.5 yr), a midpoint that leaned toward the **disfavored**
  a > 2 AU family. It was reconciled to the authors' favored a ≈ 1.6 AU /
  P 705 d (T_eq ≈ 225 K) so the in-game orbit matches this synthesis; the
  a > 2 AU family (a ≈ 2.1 AU) is retained only in prose as the disfavored
  alternative.
- **Dynamical stability (Kozai-Lidov) — resolved.** The orbit is now
  **stability-selected** (e = 0.1, mutual i ≈ 16°), the median of the
  HZ-stable range from a REBOUND/IAS15 scan (`phase3/stability-sim`, see
  `STABILITY_REPORT.md`): it keeps the planet in α Cen A's habitable zone
  (orbit 1.345–1.854 AU, e_max 0.157, MEGNO 2.000) over 10⁵ yr and hosts a
  Hill-stable Pandora-mass moon. The Beichman-observed e ≈ 0.4 / mutual
  i ≈ 50° orbit is **Kozai-Lidov unstable** (eccentric KL pumps e past 0.95
  within ~30 kyr, periastron then crashing below the stellar radius over
  ~10⁵ yr — tidal disruption) and is retained only as the unstable canonical
  alternative. The one remaining open item is the cfg-frame inclination: the
  constrained quantity is the mutual inclination to the AB plane (≈16°), which
  still needs converting to the system-frame value for the cfg.
- **Ring vs inflated radius.** The ring (`ring_present = true`) and the
  ring-free 1.1 R_Jup giant are co-equal paper readings
  (`## Canonical alternatives`). A resolved image or a NIRCam 4–5 µm
  measurement (which would separate the clear vs cloudy/ringed models)
  would decide it.
- **Atmosphere ingest.** α Cen A b has no Phase 2 atmosphere block in the
  DB (orbital + physical only). When the schema is extended, the Beichman
  2025 metal-rich water-cloud best fit should be ingested as
  `atmosphere_measurements` matching the cfg picks here.
- **Rotation / obliquity.** Both are within-window tie-breaks (10 h, 27°),
  unconstrained by any measurement.

## Related

- [alpha-centauri-a](alpha-centauri-a.md) — host star Phase 3 synthesis;
  provides the G2V Teff / L / R / mass / age, the binary-event geometry,
  and the illumination-color-temperature reference. (Its intro notes the
  candidate as "unconfirmed" — predates this planet-level synthesis.)
- [alpha-centauri-b](alpha-centauri-b.md) — the K1V companion, the
  brilliant second sun in α Cen A b's sky
- [proxima-cen-c](proxima-cen-c.md) — the other new candidate in this
  triple; contrast Proxima c's cold ice giant against α Cen A b's
  temperate ringed Saturn-class giant
- [eps-ind-a-b](eps-ind-a-b.md) — comparison giant around a nearby dwarf;
  contrast ε Indi A b's massive, self-luminous super-Jupiter against
  α Cen A b's lower-mass, insolation-set, ringed temperate giant
- [methodology](../reference/methodology.md) — Decisions schema
- [mod-reference](../reference/mod-reference.md) — downstream Kopernicus /
  EVE / Scatterer cfg writers consuming this giant's atmosphere + ring
  decisions
