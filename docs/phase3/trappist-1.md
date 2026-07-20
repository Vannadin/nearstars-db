<!-- TRAPPIST-1 host star Phase 3 synthesis: M8V ultracool dwarf — cool H2-thermostat flares, low-contrast spots, fast rotation -->
# TRAPPIST-1 — Phase 3 Synthesis (host star)

TRAPPIST-1 is the ultracool anchor of the NearStars roster: an M8.0 V
dwarf at 12.467 pc, barely above the hydrogen-burning limit at
0.0898 M☉, with a radius of 0.1192 R☉ — a star the size of Jupiter
holding seven transiting rocky planets inside 0.07 AU. The Sun is
roughly 2000 times more luminous; at L = 5.22×10⁻⁴ L☉ and
Teff = 2566 K the photosphere sits at the temperature of a candle
flame's outer envelope, cool enough that molecular chemistry (TiO,
VO, H₂O — and crucially H₂) shapes both its spectrum and, as it
turns out, its flares.

The physical parameters are among the best measured of any M dwarf
because seven planets transit it: [Agol et al. 2021](https://arxiv.org/abs/2010.01074)
(transit-timing + photodynamics) pins mass, radius, and Teff;
[Van Grootel et al. 2018](https://arxiv.org/abs/1712.01911) anchors
the bolometric luminosity; [Burgasser & Mamajek 2017](https://arxiv.org/abs/1706.02018)
give the concordance age of 7.6 ± 2.2 Gyr — an *old* star, kinematics
and activity agreeing, yet still magnetically lively. The mean
density is ~51 ρ☉, the highest of any NearStars host.

Two recent results overturn the default art direction for this star,
and both go into cfg. **First, its flares are cool.**
[Shapiro et al. 2026](https://arxiv.org/abs/2601.00386) show that
molecular-hydrogen dissociation acts as a thermostat in the dense,
cool photosphere, capping white-light flares at ~3500–4000 K —
nearly three times cooler than the 9000–10000 K solar-flare
blackbody every generic renderer assumes. Flares on TRAPPIST-1 are
warm orange brightenings, not blue-white flashes.
**Second, its spots are low-contrast.**
[Vasilyev et al. 2025](https://arxiv.org/abs/2508.04793) measure
vanished magnetic features at 2350–2550 K — only a few hundred
kelvin below the 2566 K photosphere — so the surface is a subtle
mottle, not a black-spotted disk.

**Scenario choice for NearStars: a deep-orange, subtly mottled
ultracool dwarf (`#ffcc70` photospheric tint) with frequent warm
orange flares — an every-25-days superflare cadence at 3500–4000 K
flare color, low-contrast spot dappling, and a fast 3.295-day spin
that carries the mottle visibly around the disk.**

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M8.0 V (±0.5) | high | Gillon et al. 2016 classification, restated in [Van Grootel 2018](https://arxiv.org/abs/1712.01911) §1 |
| `mass_msun` | 0.0898 ± 0.0023 | high | [Agol et al. 2021](https://arxiv.org/abs/2010.01074) — photodynamical fit; Phase 2 recommended row |
| `radius_rsun` | 0.1192 ± 0.0013 | high | [Agol et al. 2021](https://arxiv.org/abs/2010.01074) — transit-derived stellar density + parallax |
| `teff_k` | 2566 ± 26 | high | [Agol et al. 2021](https://arxiv.org/abs/2010.01074); same value used as the literature prior in [Radica 2024](https://arxiv.org/abs/2409.19333) §3 |
| `luminosity_lsun` | 5.22×10⁻⁴ ± 0.19×10⁻⁴ | high | [Van Grootel 2018](https://arxiv.org/abs/1712.01911) — bolometric flux integration |
| `metallicity_fe_h_dex` | +0.04 ± 0.08 | medium | Gillon et al. 2016 low-res spectroscopy; CMD position slightly metal-rich per [Burgasser & Mamajek 2017](https://arxiv.org/abs/1706.02018) |
| `age_gyr` | 7.6 ± 2.2 | medium | [Burgasser & Mamajek 2017](https://arxiv.org/abs/1706.02018) — kinematic + activity concordance |
| `rotation_period_days` | 3.295 ± 0.003 | high | [Vida et al. 2017](https://arxiv.org/abs/1703.10130) K2 photometry; independently recovered at 3.27 ± 0.04 d by [Berardo 2025](https://arxiv.org/abs/2506.12140) |
| `activity_log_lhalpha_lbol` | −4.85 to −4.60 | medium | [Burgasser & Mamajek 2017](https://arxiv.org/abs/1706.02018) Table 1 — Hα, the M-dwarf activity proxy (no Ca II R'HK for an M8) |
| `x_ray_log_lx_lbol` | −3.52 ± 0.17 | medium | [Burgasser & Mamajek 2017](https://arxiv.org/abs/1706.02018) Table 1, from the [Wheatley 2017](https://arxiv.org/abs/1605.01564) XMM detection (Lx/Lbol 2–4×10⁻⁴) |
| `magnetic_field_kg` | 0.6 (+0.2/−0.4) | medium | Reiners & Basri 2010, restated in [Van Grootel 2018](https://arxiv.org/abs/1712.01911) §4.2 |
| `flare_ffd_cumulative_slope_beta` | 0.753 (+0.068/−0.050) | medium | [Vasilyev et al. 2026](https://arxiv.org/abs/2605.05468) — single power law over 10²⁹–10³³ erg; supersedes Vida β≈0.59 (see Atmosphere) |
| `flare_rate_e30_per_year` | ~1000 | medium | [Shapiro et al. 2026](https://arxiv.org/abs/2601.00386) §I; consistent with the Vasilyev 2026 normalization (0.240/day above 1.01×10³¹ erg) |
| `superflare_e32_interval_days` | 25 | medium | [Vasilyev et al. 2026](https://arxiv.org/abs/2605.05468) — an order of magnitude more frequent than pre-2026 estimates |
| `flare_color_temp_k` | 3500–4000 | medium | [Shapiro et al. 2026](https://arxiv.org/abs/2601.00386) — H₂-dissociation thermostat caps white-light flares; [Howard 2025](https://arxiv.org/abs/2512.04265) RADYN fits (2115–4010 K) corroborate. Render flares warm orange, not blue-white |
| `spot_temp_k` | 2350–2550 | medium | [Vasilyev et al. 2025](https://arxiv.org/abs/2508.04793) — vanished-feature Planck fits; "cooler than the photosphere, but by at most a few hundred kelvins" |
| `spot_feature_area_disk_pct` | 0.06–1.5 (per feature) | medium | [Vasilyev et al. 2025](https://arxiv.org/abs/2508.04793) §3.4 — black-spot to penumbra-like bracketing; contamination retrievals are spot-dominated ([Radica 2024](https://arxiv.org/abs/2409.19333)) |
| `stellar_color_temp_k` | 2566 | high | = Teff; input to the photospheric-color pipeline |
| `visual_surface_tint_hex_primary` | `#ffcc70` | medium | Pickles real-SED M-ladder via `stellar_photospheric_color.py`; 2566 K clamps at the coolest anchor — pale warm orange, NOT brick-red (see Visual styling) |
| `figure_j2` | 2.0×10⁻⁶ | medium | Radau–Darwin polytrope branch (NMoI 0.205, J₂/q = 0.084) at q = 2.33×10⁻⁵ from the fast 3.295-d spin; per the always-emit stellar-J₂ policy ([body-figure-methodology](../reference/body-figure-methodology.md)) |

## Surface synthesis

The photosphere is a 2566 K molecular atmosphere — TiO/VO bands
gate the optical flux and H₂O the near-IR, which is why the
photospheric color pipeline uses a real Pickles SED rather than a
blackbody (a 2566 K blackbody renders `#ffa94f`, noticeably redder
than the band-structured truth). The star is also measurably
*inflated*: [Burgasser & Mamajek 2017](https://arxiv.org/abs/1706.02018)
note the radius runs 8–14% above solar-metallicity evolutionary
models, the classic signature of magnetic suppression of convection
in active M dwarfs.

**Spots exist, but the contrast is subtle.** Kepler/K2 confirmed
cool, stable spots (Luger 2017; Vida 2017), and JWST transmission
spectra of the planets are contaminated at the 100–500 ppm level by
a spot-dominated heterogeneous photosphere
([Radica 2024](https://arxiv.org/abs/2409.19333)). The best direct
temperature measurement comes from
[Vasilyev et al. 2025](https://arxiv.org/abs/2508.04793), who
watched individual magnetic features vanish during flares: the
features fit 2350–2550 K — a few hundred kelvin of contrast at most,
with per-feature projected areas of 0.06% (if fully black) to 1.5%
(if penumbra-like) of the visible disk. The rendering consequence is
a *dappled* disk: slightly darker, slightly redder patches drifting
with the 3.295-day rotation, never the hard black naevi of a
classical spotted-star texture.

**No spot–flare geometry correlation.** Vida et al. 2017 found
flares at every rotational phase, only weakly favoring light-curve
minimum — so flare placement in the renderer need not track the spot
pattern.

## Atmosphere synthesis

The chromosphere and corona are active but modest by late-M flare
star standards — [Van Grootel 2018](https://arxiv.org/abs/1712.01911)
call it "a low-activity M8," and
[Burgasser & Mamajek 2017](https://arxiv.org/abs/1706.02018) place
it as less active than over half of nearby M7–M9 dwarfs, while
stressing it "remains an active star" at 7.6 Gyr. Hα emission sits
at log L_Hα/L_bol = −4.85 to −4.60; the XMM X-ray detection
([Wheatley 2017](https://arxiv.org/abs/1605.01564)) gives
Lx/Lbol = 2–4×10⁻⁴ (log −3.52 ± 0.17) with a soft two-temperature
corona (kT = 0.15 and 0.83 keV) — proportionally *solar-flare-level*
X-ray heating on a star 2000× fainter, which is why the planets'
radiation environment is severe even though the star is dim.

**The flare story is the load-bearing synthesis.** Three strands
reconcile as follows:

- **Rates.** K2 gave 42 flares in 74 days (median wait 28.1 h,
  [Vida 2017](https://arxiv.org/abs/1703.10130)). The 2026 joint
  JWST+K2 flare-frequency distribution
  ([Vasilyev 2026](https://arxiv.org/abs/2605.05468)) is a single
  power law (cumulative slope β = 0.753) across 10²⁹–10³³ erg:
  ~10³⁰-erg flares ~1000 times a year, and >10³² erg superflares
  every ~25 days — ten times more often than pre-2026 estimates.
  The cfg adopts the 2026 law; Vida's shallower β ≈ 0.59 and Paudel's
  0.6 were energy-range-limited fits now subsumed by it.
- **Temperature (the color).** The H₂ thermostat
  ([Shapiro 2026](https://arxiv.org/abs/2601.00386)): heating the
  cool dense photosphere dissociates H₂, which soaks energy and caps
  flare regions near 4000 K. White-light flares run 3500–4000 K,
  briefly ~5000 K in the impulsive phase, settling to 3000–3500 K
  for tens of minutes. [Howard 2025](https://arxiv.org/abs/2512.04265)
  independently fit JWST flares with RADYN models at 2115–4010 K
  effective temperatures (filling factors 0.03–0.51%). The classic
  9000–10000 K flare blackbody is a *solar* paradigm that does not
  operate below ~4000 K stellar Teff.
- **The UV exception.** In the far-UV,
  [Berardo 2025](https://arxiv.org/abs/2506.12140) find sub-hour
  ~10²⁹-erg microflares with ~11000 K color temperature over a tiny
  ~0.011% of the disk — 400% amplitude in Lyα versus ~3–4% in the
  optical. Hot flare *cores* exist, but they are FUV-bright pinpoints;
  the visible-band event remains the warm 3500–4000 K brightening.

**XUV budget spread (recorded, not resolved).**
[Wheatley 2017](https://arxiv.org/abs/1605.01564) bracket
L_XUV/L_bol = 6–9×10⁻⁴ (~1.2–1.8×10²⁷ erg/s);
[Berardo 2025](https://arxiv.org/abs/2506.12140) reconstruct
1.83×10²⁸ erg/s from Lyα — 30× the 2017-era value they quote
(6.28×10²⁶), and ~5× above Howard's adopted quiescent 3.75×10²⁷
(Wilson 2021). The Decisions table carries only the solid X-ray row;
the XUV spread is an open item for the radiation-environment layer.

## Rotation & spin synthesis

The 3.295 ± 0.003 d K2 period ([Vida 2017](https://arxiv.org/abs/1703.10130))
is secure and independently recovered in HST photometry at
3.27 ± 0.04 d ([Berardo 2025](https://arxiv.org/abs/2506.12140));
the older ground-based 1.40 d value (Gillon 2016, echoed in
Wheatley 2017) is superseded. An honest tension remains on the
spectroscopic side: v sin i = 6 ± 2 km/s (Reiners & Basri 2010)
would imply P_rot ≈ 0.99 d (0.74–1.48 d) at this radius — it was the
1.40 d value, not 3.295 d, that matched it — while the equatorial
velocity at 3.295 d is only ~1.8 km/s. Vida et al. note the K2
Fourier spectrum shows no significant ~1 d feature, so the cfg
adopts the twice-confirmed photometric period and leaves the v sin i
discrepancy to the literature.

**Figure.** Fast spin on a small dense star gives
q = Ω²R³/GM = 2.33×10⁻⁵; the fully convective Radau–Darwin branch
(polytropic NMoI 0.205, J₂/q = 0.084) yields **J₂ ≈ 2.0×10⁻⁶** —
~500× Proxima's (83.5-d spin) and edging out 40 Eri C's fast-spun
1.6×10⁻⁶ as the roster's largest M-dwarf J₂ (Fomalhaut A's 1.0×10⁻⁴
still dominates overall). Dynamically it stays
negligible even for planet b at 21 stellar radii (GR precession
dominates), but per the 2026-07-12 always-emit policy the term is
computed and Principia carries it. Visual oblateness
f ≈ 1.5×10⁻⁵ — unrenderable, the disk stays round.

At 7.6 Gyr with a ~4 Gyr saturation spin-down knee (Fleming 2020,
via [Howard 2025](https://arxiv.org/abs/2512.04265)), the star has
left saturation yet still spins in days — ultracool dwarfs brake
extraordinarily slowly, which is why an old star still delivers a
young star's flare schedule.

## Visual styling

- **Photospheric tint `#ffcc70`** — from the Pickles real-SED ladder
  (`scripts/refs/stellar_photospheric_color.py`); 2566 K lies below
  the coolest Pickles M anchor, so the chromaticity clamps at the
  ladder floor. Per the color methodology this is a pale warm
  orange: the "brick-red M dwarf" trope is a color-index artifact,
  not a chromaticity. The 2566 K blackbody hex `#ffa94f` is the
  lower bound if a redder art direction is ever wanted — the
  Pickles value is the data-grounded pick.
- **Low-contrast mottling, not black spots.** Spot dapples at
  ~2350–2550 K against 2566 K: darken the tint locally by a few
  percent and pull faintly redward; individual features sub-percent
  to ~1.5% of the disk. Drift them with the 3.295-d rotation.
- **Flares are warm orange, frequent, and small-area.** Render flare
  color at 3500–4000 K (≈ K-dwarf photosphere warmth — `#ffcc95`
  territory per the same ladder), filling factors well under 1% of
  the disk, amplitudes a few percent in the optical. A >10³²-erg
  superflare every ~25 game-days is the marquee event; ~daily lesser
  flares keep the star visibly alive. Never render blue-white
  solar-style flares on this star.
- **In-sky presence.** From planet e (0.029 AU) the star spans ~2.4°
  — four to five Suns wide — a huge dim amber disk whose mottle and
  flares are directly visible scenery, which is why the
  low-contrast-spot and warm-flare rows above are gameplay-facing,
  not trivia.
- **Firefly note.** Flare color here is *stellar surface* rendering,
  not reentry plasma — the Firefly composition-color policy
  (mod-original palette) is unaffected; this row feeds the star's
  own emissive layer.

## Bibliography

### Read (deep-read, drives Decisions rows)

- **[Agol et al. 2021](https://arxiv.org/abs/2010.01074)** —
  *Refining the transit timing and photometric analysis of
  TRAPPIST-1*. Mass/radius/Teff anchors (Phase 2 recommended rows).
  Cache note: local text is abstract-only; numeric rows rest on the
  Phase 2 curation (paper-verified) and the 2566 K prior restated in
  Radica 2024 §3.
- **[Van Grootel et al. 2018](https://arxiv.org/abs/1712.01911)** —
  *Stellar parameters for TRAPPIST-1*. Bolometric luminosity
  5.22×10⁻⁴ L☉; density 51.1 ρ☉; 600 G field restatement;
  "low-activity M8" characterization.
- **[Burgasser & Mamajek 2017](https://arxiv.org/abs/1706.02018)** —
  *On the Age of the TRAPPIST-1 System*. 7.6 ± 2.2 Gyr concordance
  age; Table 1 activity compendium (Hα, X-ray, v sin i); 8–14%
  radius inflation; "old but active" framing.
- **[Vida et al. 2017](https://arxiv.org/abs/1703.10130)** — K2
  flare survey: 42 flares/74 d, 3.295 d rotation, energy range
  1.26×10³⁰–1.24×10³³ erg, no spot-phase correlation.
- **[Wheatley et al. 2017](https://arxiv.org/abs/1605.01564)** —
  XMM-Newton X-ray detection: Lx/Lbol 2–4×10⁻⁴, two-temperature
  corona, XUV/bol 6–9×10⁻⁴.
- **[Vasilyev et al. 2025](https://arxiv.org/abs/2508.04793)** —
  flares reveal magnetic-feature spectra: vanished features at
  2350–2550 K, per-feature 0.06–1.5% of disk; MURaM M4 spot contrast.
- **[Shapiro et al. 2026](https://arxiv.org/abs/2601.00386)** — the
  H₂ flare thermostat: white-light flares capped at ~3500–4000 K,
  ~1000/yr above 10³⁰ erg; mechanism ceases above ~4000 K Teff.
- **[Vasilyev et al. 2026](https://arxiv.org/abs/2605.05468)** —
  single power-law FFD (β = 0.753) over four energy decades;
  superflares every 25 d; adopts 3500 K flare continuum.
- **[Berardo et al. 2025](https://arxiv.org/abs/2506.12140)** — HST
  Lyα: frequent FUV microflares (11000 K, 0.011% of disk), rotation
  confirmation, XUV reconstruction 1.83×10²⁸ erg/s.
- **[Radica et al. 2024](https://arxiv.org/abs/2409.19333)** — JWST
  NIRISS stellar contamination: spot-dominated retrievals, 100–500
  ppm signatures, 2566 ± 50 K photosphere prior, spot grid floor
  2300 K / faculae ≤ +1000 K.
- **[Howard et al. 2025](https://arxiv.org/abs/2512.04265)** — RADYN
  NIR flare modeling: fiducial flare Teff 2115–4010 K with 0.03–0.51%
  filling factors; flares contaminate 50–70% of JWST transits.

### Context (cited through the read set; not deep-read here)

- **[Gillon et al. 2016](https://ui.adsabs.harvard.edu/abs/2016Natur.533..221G)** /
  **[Gillon et al. 2017](https://ui.adsabs.harvard.edu/abs/2017Natur.542..456G)** —
  discovery papers; first stellar parameters and the superseded
  1.40 d rotation alias; [Fe/H] source.
- **[Luger et al. 2017](https://ui.adsabs.harvard.edu/abs/2017NatAs...1E.129L)** —
  K2 seven-planet paper; spot confirmation and the 3.3 d period the
  contamination literature cites.
- **Reiners & Basri 2010** — 600 G magnetic field and
  v sin i = 6 ± 2 km/s, quoted by Van Grootel 2018 and Wheatley 2017.
- **Wilson et al. 2021** — quiescent XUV 3.75×10²⁷ erg/s used by
  Howard 2025 (one leg of the XUV spread).
- **Fleming et al. 2020** — the ~4 Gyr saturation knee for ultracool
  spin-down.

### Not read — superseded or out of scope

- Stassun 2019 / Ducrot 2020 / Grimm 2018 stellar rows — earlier or
  wider-error parameter sets, superseded by Agol 2021 in Phase 2.
- Planet-focused atmosphere/escape papers in the system bibliography —
  consumed by the seven per-planet syntheses, not the host report.

## Open items for follow-up

- **Agol 2021 cache is abstract-only.** The recommended M/R/Teff rows
  are Phase 2-verified, but a full-text re-fetch of
  [2010.01074](https://arxiv.org/abs/2010.01074) would let this
  report's Step 10 trace land on the paper's own tables rather than
  the curation layer + Radica's restatement.
- **XUV budget spread (×10).** Wheatley-band ~1.2–1.8×10²⁷ vs
  Berardo Lyα-reconstructed 1.83×10²⁸ erg/s. If the Kerbalism
  radiation layer is ever re-anchored for TRAPPIST-1, resolve this
  spread first (definition differences — X-ray+EUV band vs
  Lyα-scaled total — likely explain most of it).
- **No stellar wind measurement.** The 2026-06-11 stellar-wind
  synthesis pass skipped TRAPPIST-1 for lack of mass-loss or
  astrosphere data — hence no wind/astrosphere section here. MHD
  wind-planet coupling papers exist in the system bib (simulation
  only); revisit if an observational constraint appears.
- **Spot covering fraction is per-feature, not global.** Vasilyev
  2025 measures individual vanished features (0.06–1.5% of disk);
  the global spot fraction remains retrieval-degenerate (Radica's
  0–50% prior). The low-contrast rendering rule is robust to this;
  a global fraction row is not currently supportable.
- **Activity cycle unknown.** No cycle period exists for TRAPPIST-1
  (flare monitoring baselines are too short); no `activity_cycle_years`
  row is emitted, unlike α Cen A/B.

## Related

- [trappist-1-b](trappist-1-b.md) … [trappist-1-h](trappist-1-h.md) —
  the seven planet syntheses this host report anchors
- [alpha-centauri-a](alpha-centauri-a.md) — stellar synthesis
  structural template (G2V counterpart)
- [stellar-photospheric-color-methodology](../reference/stellar-photospheric-color-methodology.md) —
  the `#ffcc70` derivation path (Pickles real-SED ladder)
- [body-figure-methodology](../reference/body-figure-methodology.md) —
  stellar J₂ always-emit policy + the polytrope branch used here
- [methodology](../reference/methodology.md) — Decisions schema
