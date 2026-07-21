# Luhman 16 A — Phase 3 Synthesis

Luhman 16 A (WISE J104915.57−531906.1 A) is the brighter, cooler-cloud
component of the nearest brown-dwarf binary — the third-closest system to
the Sun after α Centauri and Barnard's Star, at 1.9938 ± 0.0004 pc (501.557
mas absolute parallax, Lazorenko & Sahlmann 2018). It is an **L7.5 dwarf**
(Burgasser et al. 2013, adopted by Faherty 2014), sitting just on the L side
of the L/T transition where photospheric condensate clouds are at their
thickest. Its companion Luhman 16 B (T0.5) orbits it every 27.5 years on a
moderately eccentric (e = 0.34) 3.56-AU relative orbit (Lazorenko & Sahlmann
2018).

This is not a star. With a dynamical mass of 33.5 M_Jup = 0.0320 M☉
(Lazorenko & Sahlmann 2018) it is far below the ~0.075 M☉ hydrogen-burning
limit; the strong 6708 Å lithium line detected by Faherty 2014 (EW 8.0 Å) —
the lithium test — confirms the substellar, never-fused core. Luhman 16 A
shines only on residual gravitational/contraction heat, with a bolometric
luminosity of log L/L☉ = −4.67 (≈ 2.1 × 10⁻⁵ L☉) radiated almost entirely in
the infrared from an ~1310 K photosphere.

In NearStars terms it renders as a **dim, deep-red incandescent sphere
roughly the size of Jupiter** (≈ 0.090 R☉, the standard field-brown-dwarf
radius Faherty 2014 assumes), wrapped in thick, near-featureless silicate and
iron clouds. Unlike its restless companion B, A is photometrically quiet —
the calm member of the pair.

**Scenario choice for NearStars: a sub-stellar, Jupiter-sized "failed star"
glowing a dull ember-red, paired in a tight 27-year mutual orbit with the
more dramatic weather-world B.** All physical picks track the Phase 2
measurements; the single tie-break is the surface tint hex, computed from the
1310 K blackbody and reddened for the dusty photosphere.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | L7.5 | high | Burgasser et al. 2013 (NIR resolved spectroscopy), adopted by Faherty 2014 |
| `mass_msun` | 0.0320 ± 0.0003 | high | Lazorenko & Sahlmann 2018 — astrometric binary orbit (33.51 M_Jup); Bedin 2024 / Garcia 2017 alternates |
| `radius_rsun` | 0.090 | medium | Faherty 2014 — assumed 0.9 R_Jup (Vrba 2004 prescription); no measured radius exists for any L/T dwarf |
| `teff_k` | 1310 ± 30 | high | Faherty 2014 — derived from bolometric luminosity |
| `luminosity_lsun` | 2.1e-05 | high | Faherty 2014 — log L/L☉ = −4.67 ± 0.04 (bolometric flux) |
| `age_gyr` | 0.5 | medium | Luhman 16AB are kinematic members of the Oceanus moving group (age ~500 Myr, Gagné et al. 2023); de Regt et al. 2026 (`2602.03409`) corroborate via ¹²C/¹³C = 74 (matching the present-day ISM, below the Solar value → recent inheritance). Supersedes the Faherty 2014 field age (1.5 Gyr, range 0.1–3) |
| `rotation_period_days` | 0.289 (≈ 6.94 hr) | low | Apai 2021 — TESS periodogram, *tentatively* attributed to A; disputed (~5–8 hr) |
| `visual_surface_tint_hex_primary` | `#662400` | medium | Tie-break: 1310 K blackbody hue #FF5900 (cie_color.py) dimmed to ember + dusty-silicate/alkali reddening |
| `stellar_color_temp_k` | 1310 | high | = teff_k; drives Kopernicus emission/illumination color (deep red) |
| `variability_amplitude_pct` | < 4.5 (ground-based); wavelength-dependent in JWST | medium | Buenzli 2015 ground-based low-amplitude; Biller et al. 2025 (`2505.00794`) JWST reveals wavelength-dependent multi-layer variability in A (not featureless) — amplitude varies by pressure level |
| `cloud_morphology` | constant longitudinal (Jupiter-like) cloud bands of silicate + iron condensates, plus patchy structure + hot spots; multi-layer wavelength-dependent weather (subtler than B) | medium | Millar-Blanchaer et al. 2020 (`2020ApJ...894...42M`, H-band VLT/NaCo polarimetry p_A = 0.031% ± 0.004%) shows A's polarization requires CONSTANT LONGITUDINAL cloud bands — an oblate homogeneous atmosphere is ruled out, a two-banded morphology reproduces the signal. Biller et al. 2024/2025 (`2505.00794`) JWST adds patchy clouds (deep 1–2.5 µm) + high-altitude hot spots + small-grain silicates (8.5–11 µm). Both revise the earlier "near-uniform / quiet" reading (Crossfield 2014 left A unmapped) |

## Surface synthesis

There is no solid surface — the visible "surface" is the τ ≈ 1 photosphere at
~1310 K, deep inside a hydrogen/helium envelope laced with condensate clouds.
At this temperature the chemistry is dominated by neutral alkalis (the broad,
pressure-broadened Na and K resonance doublets that drink most of the optical
flux), water and CO/CH₄ in the near-IR, and FeH (Faherty 2014 detects the
0.9896 µm Wing–Ford band in both components). The condensates are silicate
and iron grains plus corundum — the same 1300–2000 K mineral dust that the
color-materials catalog ties to grey-to-reddened cloud decks. On the L7.5
primary these clouds are at their thickest and most uniform; little of the
deeper, hotter gas shows through.

## Atmosphere / cloud layer

For a self-luminous brown dwarf the "atmosphere" *is* the visible body. Faherty
2014 finds A's clouds are thicker and more homogeneous than B's — the strong,
similar FeH in both components argues for comparably cloudy photospheres, but
A shows the weaker alkali continuum, consistent with looking only into the
upper, cooler cloud tops. The result is a smooth, slightly hazy globe with no
strong banding. This is the visual opposite of B: where B is a fast-changing
weather map, A is a near-static dusty ball. For an EVE-style treatment A wants
a single thick, low-contrast cloud layer with very slow evolution.

## Rotation & spin

Brown dwarfs are fast rotators (a few hours). A's period is genuinely
uncertain: Gillon 2013 detected **no** periodic signal from A in 12 nights of
TRAPPIST photometry (all the ~4.87 hr variability came from B); Crossfield 2014
measured v sin i = 17.6 ± 0.1 km/s — slower than B's 26.1 km/s — but did not
recover a period, calling A's rotation "the best way" to advance the system.
Apai 2021 *speculates* that a weak 6.94 hr peak in the TESS periodogram belongs
to A, while Mancini 2015 favored ~8 hr and Millar-Blanchaer 2020 simply assumed
5 or 8 hr. The cfg adopts 6.94 hr at low confidence; the spin axis is plausibly
near-equator-on (Apai 2021 reconciles the periods with the v sin i values under
near-edge-on viewing).

## Visual styling

The defensible base color is blackbody incandescence at 1310 K — a deep
red-orange (sRGB hue #FF5900 from `cie_color.py`, Planck + CIE 1931). But
Luhman 16 A is extraordinarily dim (L ≈ 2 × 10⁻⁵ L☉, most of it infrared), so
the *perceived* color is a dark ember rather than a bright orange — the cfg
tint `#662400` is the 1310 K hue scaled to ~40% value. Dusty silicate cloud
tops and the broad alkali absorption push it a touch redder and muddier still.
In-engine A should read as a quietly glowing dull-red sphere, Jupiter-sized,
its illumination color set to the same deep-red 1310 K temperature so any
nearby body (its companion B) is lit in that ember light. Magenta — sometimes
quoted as "the color of a brown dwarf" — is deliberately **not** used here: it
is a non-spectral hue requiring a green-notch absorber and only emerges in the
much cooler late-T/Y dwarfs, not at L7.5 (see Open items).

## Bibliography

**Read (drive Decisions rows):**
- Lazorenko & Sahlmann 2018, A&A 618, A111 (arXiv [1808.07835](https://arxiv.org/abs/1808.07835)) — astrometric orbit, dynamical masses, parallax.
- Faherty et al. 2014, ApJ 790, 90 (arXiv [1406.1518](https://arxiv.org/abs/1406.1518)) — Li, FeH, bolometric luminosity, Teff, age, assumed radius.
- Apai et al. 2021, ApJ 906, 64 (arXiv [2101.02253](https://arxiv.org/abs/2101.02253)) — TESS rotation; tentative 6.94 hr for A.
- Crossfield et al. 2014, Nature 505, 654 (arXiv [1401.8145](https://arxiv.org/abs/1401.8145)) — Doppler v sin i; A unmapped.

**Context:**
- Gillon et al. 2013, A&A 555, L5 (arXiv [1304.0481](https://arxiv.org/abs/1304.0481)) — no periodic signal from A.
- Burgasser et al. 2013 — L7.5/T0.5 spectral classification.
- Bedin et al. 2024 (arXiv [2403.08865](https://arxiv.org/abs/2403.08865)), Garcia et al. 2017 (arXiv [1708.02714](https://arxiv.org/abs/1708.02714)) — alternate dynamical masses.

## Open items for follow-up

- **Magenta question.** Integrated-light reconstructions sometimes render brown
  dwarfs magenta/violet (deep CH₄ + Na/K carving the green-yellow). This is a
  late-T/Y effect; at L7.5 A is firmly red. If a future art pass wants the
  magenta cast, it belongs on a cooler body, not A — flagged, not adopted.
- **Radius is assumed, not measured.** 0.9 R_Jup is the standard field-BD value;
  no L/T dwarf has a directly measured radius. JWST/interferometric constraints
  would refine the rendered size.
- **A's rotation is unconfirmed** (~5–8 hr). A dedicated period would let the
  spin be set at higher confidence.

## Related

- [luhman-16-b](luhman-16-b.md) — the T0.5 companion; the pair shares a ~3.5 AU orbit and is curated as a resolved brown-dwarf binary.
- [eps-ind-a](eps-ind-a.md) — the other curated substellar host in the roster (T-dwarf companion eps Ind B), for cross-comparing field brown-dwarf rendering.
- [stellar-photospheric-color-methodology](../reference/stellar-photospheric-color-methodology.md) — grounds the photospheric tint used for this L dwarf.
- [methodology-index](../reference/methodology-index.md) — the derived-value recipe index (color, internal heat, rotation) behind these decisions.
- [methodology](../reference/methodology.md) — schema source for the Decisions table.
