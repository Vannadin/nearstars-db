# Luhman 16 B — Phase 3 Synthesis

Luhman 16 B (WISE J104915.57−531906.1 B) is the famous one: the first brown
dwarf — indeed the first object outside the Solar System — to have its
cloud weather mapped across its surface (Crossfield et al. 2014). It is the
**T0.5** secondary of the nearest brown-dwarf binary, 1.9938 ± 0.0004 pc away
(Lazorenko & Sahlmann 2018), sitting just on the T side of the L/T transition
where the thick silicate clouds of the L dwarfs begin to break up and clear.

Like its primary it is deeply substellar — 28.5 M_Jup = 0.0273 M☉ (Lazorenko &
Sahlmann 2018), with the lithium test passed (Faherty 2014 detect the 6708 Å
Li line at EW 3.8 Å, the first such detection in a T dwarf). Its bolometric
luminosity log L/L☉ = −4.71 (≈ 1.9 × 10⁻⁵ L☉) and ~1280 K photosphere are
within a whisker of A's; the two differ not in brightness but in **behaviour**.
Faherty 2014 find B runs ~50 K warmer in the grain-scattering near-IR windows,
which they read as thinner clouds or patchy holes letting us see down to
deeper, hotter gas.

That patchiness is the whole story. As B rotates every ~4.9 hours its
brightness swings by up to ~11% peak-to-peak (Gillon 2013) as bright cloud
holes and dark thick-cloud regions rotate in and out of view. Crossfield 2014's
Doppler map resolved "a large, dark, mid-latitude region, a brighter near-polar
area, and equatorial mottling"; Apai 2021's 100-rotation TESS light curve
showed the period drifting and splitting, the signature of high-speed zonal
jets and planetary-scale waves rather than fixed spots.

**Scenario choice for NearStars: a Jupiter-sized, deep-red substellar globe
whose defining feature is dynamic, banded, fast-evolving cloud weather — the
restless companion to the quiet ember A, the pair locked in a 27-year mutual
orbit.** Physical picks track the Phase 2 measurements; the surface-tint hex is
a tie-break computed from the 1280 K blackbody, and the cloud morphology is the
distinctive, observation-grounded visual.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | T0.5 | high | Burgasser et al. 2013 (NIR resolved spectroscopy), adopted by Faherty 2014 |
| `mass_msun` | 0.0273 ± 0.0003 | high | Lazorenko & Sahlmann 2018 — astrometric binary orbit (28.55 M_Jup); Bedin 2024 / Garcia 2017 alternates |
| `radius_rsun` | 0.090 | medium | Faherty 2014 — assumed 0.9 R_Jup (Vrba 2004 prescription); no measured radius exists for any L/T dwarf |
| `teff_k` | 1280 ± 75 | high | Faherty 2014 — derived from bolometric luminosity |
| `luminosity_lsun` | 1.9e-05 | high | Faherty 2014 — log L/L☉ = −4.71 ± 0.10 (bolometric flux) |
| `age_gyr` | 0.5 | medium | Shared system age — Luhman 16AB are kinematic members of the Oceanus moving group (~500 Myr, Gagné et al. 2023); de Regt et al. 2026 (`2602.03409`) corroborate via ¹²C/¹³C = 74 (present-day ISM, recent inheritance). Supersedes the Faherty 2014 field age (1.5 Gyr, range 0.1–3) |
| `rotation_period_days` | 0.203 (= 4.87 hr) | high | Gillon 2013 — photometric variability; first BD weather detection |
| `visual_surface_tint_hex_primary` | `#662200` | medium | Tie-break: 1280 K blackbody hue #FF5600 (cie_color.py) dimmed to ember + dusty-silicate/alkali reddening |
| `stellar_color_temp_k` | 1280 | high | = teff_k; drives Kopernicus emission/illumination color (deep red) |
| `variability_amplitude_pct` | ~11 | high | Gillon 2013 — peak-to-peak in I+z′ (~0.9 µm), strong night-to-night evolution |
| `cloud_morphology` | dynamic banded / patchy condensate clouds; dark thick-cloud regions + bright clearings, zonal jets | high | Crossfield 2014 (Doppler map); Apai 2021 (jets / planetary waves); Faherty 2014 (patchy holes) |

## Surface synthesis

As with A there is no solid surface — the visible globe is the ~1280 K
photosphere within an H/He envelope. The chemistry is that of an early T dwarf:
broad Na and K resonance absorption still dominating the optical, but with
methane now strengthening in the near-IR (Faherty 2014 note stronger CH₄ at
1.15 and 2.2 µm in B than in A) as the atmosphere cools past the transition.
The defining difference from A is the cloud state: B's silicate/iron decks are
fragmenting. Where A is a smooth, uniformly clouded ball, B has thick-cloud
regions interleaved with cleared holes that expose deeper, ~50 K hotter gas
(Faherty 2014) — the cloud-fragmentation mechanism thought to drive the entire
L→T transition.

## Atmosphere / cloud layer

This is the showpiece. B's atmosphere is the best-characterised "weather" of
any brown dwarf. The picture from a decade of monitoring: patchy condensate
clouds organised into zonal bands by fast atmospheric jets, evolving on a
rotation-to-rotation timescale (Gillon 2013's light curves change shape from
one night to the next). Crossfield 2014's Doppler image — the first surface map
of a brown dwarf — shows a large dark mid-latitude patch, a brighter near-polar
region, and equatorial mottling. Apai 2021 reinterpret the multi-peaked,
drifting periodicity as planetary-scale waves and high-speed jets, with a slow
~91 hr modulation possibly from vortex-dominated poles. For an EVE-style
treatment B wants two or more cloud layers of differing opacity, organised into
latitudinal bands, with bright clearings over a hotter (slightly more orange)
deep layer and visible evolution over a few-hour rotation.

## Rotation & spin

B's rotation is well determined, and it is fast: Gillon 2013 measured P =
4.87 ± 0.01 hr from TRAPPIST photometry — the value the cfg adopts. Because the
light curve is multi-peaked and epoch-dependent (the jets shift the dominant
feature), later campaigns recover slightly different "periods": Mancini 2015
got 5.1 hr, and Apai 2021's TESS analysis a dominant 5.28 hr over ~100
rotations. The true rotation is ~4.9–5.3 hr; 4.87 hr is the canonical precise
value. Crossfield 2014's v sin i = 26.1 ± 0.2 km/s is consistent with this
short period viewed close to equator-on. The fast spin is what makes the
weather observable on a single night and is integral to the body's character.

## Visual styling

The base color is blackbody incandescence at 1280 K — a deep red-orange (sRGB
hue #FF5600 from `cie_color.py`), essentially identical to A's 1310 K hue. As
with A the body is extremely dim, so the rendered tint `#662200` is that hue
scaled to a dark ember. The visual distinction between the two is therefore
**not** color but texture: B should carry obvious, evolving banded cloud
structure — dark thick-cloud lanes and brighter, slightly warmer (more orange)
clearings where the hotter deep gas shows through — turning over on its ~4.9 hr
spin. As with A, magenta is not used (a late-T/Y effect, not early-T; see Open
items). Illumination color is set to the 1280 K temperature.

## Bibliography

**Read (drive Decisions rows):**
- Gillon et al. 2013, A&A 555, L5 (arXiv [1304.0481](https://arxiv.org/abs/1304.0481)) — P_rot = 4.87 hr, ~11% variability, first BD weather.
- Crossfield et al. 2014, Nature 505, 654 (arXiv [1401.8145](https://arxiv.org/abs/1401.8145)) — first Doppler surface map of a brown dwarf.
- Apai et al. 2021, ApJ 906, 64 (arXiv [2101.02253](https://arxiv.org/abs/2101.02253)) — TESS 5.28 hr, zonal jets / planetary-scale waves.
- Faherty et al. 2014, ApJ 790, 90 (arXiv [1406.1518](https://arxiv.org/abs/1406.1518)) — Li, CH₄/FeH, bolometric luminosity, Teff, patchy clouds.
- Lazorenko & Sahlmann 2018, A&A 618, A111 (arXiv [1808.07835](https://arxiv.org/abs/1808.07835)) — dynamical mass, parallax.

**Context:**
- Burgasser et al. 2013 — L7.5/T0.5 classification.
- Mancini et al. 2015 (arXiv [1510.08099](https://arxiv.org/abs/1510.08099)) — 5.1 hr rotation cross-check.
- Bedin et al. 2024 (arXiv [2403.08865](https://arxiv.org/abs/2403.08865)), Garcia et al. 2017 (arXiv [1708.02714](https://arxiv.org/abs/1708.02714)) — alternate masses.

## Open items for follow-up

- **Magenta question.** As for A, the "brown dwarfs are magenta" reconstruction
  is a late-T/Y effect (deep CH₄ + Na/K carving out the green-yellow); T0.5 B is
  only just past the transition and stays red. Flagged, not adopted.
- **Radius is assumed, not measured** (0.9 R_Jup) — same caveat as A.
- **Cloud map is a snapshot.** B's weather genuinely evolves; any fixed cloud
  texture is a time-average. The dynamic, banded, fast-evolving character is the
  faithful choice over a static map.

## Related

- [luhman-16-a](luhman-16-a.md) — the L7.5 primary; the pair shares a ~3.5 AU orbit and is curated as a resolved brown-dwarf binary.
- [eps-ind-a](eps-ind-a.md) — the other curated substellar host in the roster (T-dwarf companion eps Ind B), for cross-comparing field brown-dwarf rendering.
- [stellar-photospheric-color-methodology](../reference/stellar-photospheric-color-methodology.md) — grounds the photospheric tint across the L/T transition.
- [methodology-index](../reference/methodology-index.md) — the derived-value recipe index (color, internal heat, rotation) behind these decisions.
- [methodology](../reference/methodology.md) — schema source for the Decisions table.
