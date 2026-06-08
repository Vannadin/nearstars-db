<!-- 플라스마 발광색 방법론의 이론적 타당성을 문헌(ADS+web)으로 적대 검증한 리뷰 -->
# Plasma-color methodology review

An independent, literature-grounded adversarial review of the NearStars
plasma-color engine (the LTE Saha–Boltzmann emission → CIE pipeline behind
`plasma_temperature_colors.yaml`, `element_temperature_colors.yaml`,
`lte_plasma_colors.yaml`). Six dimensions were each checked by a separate
reviewer against the literature; sources are ADS (astrophysics/planetary) plus
web for color-science and analytical-chemistry topics that ADS under-indexes.

## Bottom line

**The backbone is sound and standard.** Computing a plasma's emission spectrum
from Saha (ionization) + Boltzmann (excitation) + Σ nᵤ·A·hν line emission and
folding it through CIE 1931 is exactly the method used in calibration-free LIBS
and astrophysical synthetic spectra. The documented non-LTE caveats (reentry
blue, auroral forbidden lines) are all **correct**. The real weaknesses are
known omissions — continuum emission, the additive-vs-slab combination, and the
band-as-head molecular approximation — none of which invalidate the approach,
all of which have clear fixes.

## Verdicts by dimension

| # | Dimension | Verdict |
|---|---|---|
| 1 | LTE Saha–Boltzmann optically-thin emission | **Sound** w/ caveats |
| 2 | Spectrum → CIE 1931 → sRGB, max-channel hue | **Sound** w/ caveats |
| 3 | Molecular band-as-effective-line + dissociation eq. | **Sound** w/ caveats |
| 4 | Non-LTE caveat (reentry / aurora) | **Correct** (all 3 claims) |
| 5 | Combination model (density·Planck + GAIN·emission) | **Sound for hue**, questionable physics |
| 6 | Approximations & reference choices | Mostly **defensible** |

## What is confirmed correct

- **The core method is mainstream.** LTE is "the essential requisite for applying
  Boltzmann–Maxwell and Saha–Eggert expressions" (Cristoforetti 2010,
  `2010AcSpB..65...86C`, 322 cites); CF-LIBS quantification *is* this calculation
  run in reverse (`2023ApPhB.129..136L`); LTE synthetic spectra with Saha across
  many ionization stages + 105 molecules are standard in stellar atmospheres
  (Allard & Hauschildt 1995, `1995ApJ...445..433A`, 482 cites).
- **LTE holds in our core regime.** McWhirter's criterion (nₑ ≳ 1.6×10¹²·√T·ΔE³)
  gives ~10¹⁵–10¹⁶ cm⁻³ for optical ΔE at 10⁴ K; an atmospheric-pressure thermal
  plasma at 4000–15000 K sits above this. Independent Thomson-scattering work
  confirms local Saha–Boltzmann equilibrium in dense laser plasma
  (`2014AcSpB..96...61M`).
- **The colorimetry is the textbook path** and correctly treats the emission
  spectrum directly as the SPD (no illuminant division — the most common
  spectrum-to-color bug, which we avoided). Wyman–Sloan–Shirley (2013) CMF fit is
  accurate to a few % — ample for hue.
- **Dissociation K(T) is textbook-correct** — (2πμkT/h²)³ᐟ² · (U_A U_B/U_AB) ·
  exp(−D₀/kT), right sign, right prefactor, σ symmetry number.
- **The non-LTE caveats are right.** Reentry shock-layer radiation is modeled as
  thermochemical/radiative *non-equilibrium* (`1994ntrs.rept23568C` et al.);
  N₂⁺(B) (391 nm) is electron-impact populated (Te-driven, Park two-temperature),
  not thermal. Auroral O I 557.7/630 nm are forbidden metastable lines excited by
  electron precipitation / dissociative recombination and quenched at high
  density (`1989RSPSA.424....1S`, `1990AdSpR..10e..31F`, `1960JChPh..32..607Y`).
  C₂ Swan (upper state ~2.5 eV) **is** thermally accessible — so the carbon-plasma
  green is a legitimate LTE result while the N₂ blue is not. Confirmed.

## Key actionable findings (ranked)

1. **Missing continuum + the "thermal term" is a stand-in (moderate→major for hue).**
   A genuinely optically-thin gas emits lines/bands plus *continuum* (free-free
   bremsstrahlung, free-bound recombination, H⁻); it does **not** emit a Planck
   continuum. Our `(n_heavy/N_REF)·Planck` term is a phenomenological incandescence
   stand-in, defensible as art-direction but it should be **labeled as such**, not
   called the gas's thermal continuum. At 1000–3000 K a thin neutral gas has
   essentially no visible continuum (the "ember glow" is an optically-thick /
   condensed-body property). Omitting the real continuum biases hues toward
   over-saturation. → done: caption/headers now say "incandescence stand-in".
2. **The slab was abandoned for a units bug, not a physics failure (moderate).**
   The earlier `I=B(1−e^{−τ})` with κ=j/B blew up only because of bad unit
   bookkeeping — B cancels analytically (I=B(1−exp(−(Σj·L)/B))). Computing
   τ_λ=(Σj·L)/B in log space is stable. The slab is the correct physics: it
   unifies thermal+emission **without GAIN**, caps strong resonance lines at B_λ
   (fixing self-absorption hue bias), reduces to the additive sum in the thin
   limit, and replaces GAIN with a physical path length L. **Recommended highest-
   value upgrade.**
3. **Band-as-head should be band-as-centroid (moderate for hue).** A molecular
   band's hue lives in its *envelope* (rotational/vibrational spread, tens of nm),
   not its head. Placing effective lines at band heads biases each system toward
   its bluest/reddest extreme. Fix: place 2–3 effective lines at *sequence
   centroids*, weighted by g_e × band strength (not bare exp(−hc·T_e/kT)),
   cross-checked once against a LIFBASE/SPECAIR synthesis. Real diagnostics fit
   the full rotational envelope (`2002JAP....91.8955C`).
4. **Ion-line emission was missing (moderate at high T) — FIXED.** Added first-ion
   (X II) emission to the per-element table; high-T colors now show ion spectra
   (Ba II violet, etc.) instead of fading to continuum.
5. **Self-absorption (minor→moderate).** Optically-thin over-counts strong
   resonance lines (Na D, Ca II) that would saturate to B_λ; worst at high
   concentration / long path / low T (`2021AcAC.118539070T`, `2023RSCAd..1329613J`).
   Cheap guard: clamp any single line's contribution at its local B_λ(T).
6. **Single T_REF = 3500 K is a 1-D slice of a 2-D hue(T) surface.** Honest only
   if the temperature label travels with the value; flag the known flippers
   (Cu green↔violet; likely Ca/Sr/Fe/rare-earths) with alternate-T hues.
7. **Minor colorimetry:** replace per-channel clamp-to-0 with a hue-preserving
   gamut map for narrowband line spectra; add an epsilon guard before max-channel
   normalization (sub-threshold spectra → "undefined hue", not amplified noise);
   document the unadapted-D65 assumption.
8. **Minor / color-neutral:** partition-function truncation to ~25 levels cancels
   under per-channel normalization (no hue effect; only a 2nd-order Saha effect);
   fixed line width + top-80 cap are color-neutral. The intensity-mix fallback
   (A-less spectra) carries a green-yellow skew (eye/photographic intensity
   scale) — flag the *direction*, not just "low confidence".

## Sources

ADS: `2010AcSpB..65...86C`, `2014AcSpB..96...61M`, `2023ApPhB.129..136L`,
`2021AcAC.118539070T`, `2023RSCAd..1329613J`, `1995ApJ...445..433A`,
`2002JAP....91.8955C`, `1998PPCF...40..361D`, `1960JChPh..32..607Y`,
`1989RSPSA.424....1S`, `1990AdSpR..10e..31F`, `1994ntrs.rept23568C`,
`1990STIN...9025290H`. Web: CIE 1931 color space (Wikipedia); Wyman, Sloan &
Shirley 2013 (JCGT) analytic CMF; flame-test molecular bands CaO/SrO (RSC /
LibreTexts). ADS is astrophysics/planetary-centric — color science and analytical
chemistry are under-indexed there (use Semantic Scholar / Crossref for those).

## Further literature — non-LTE reentry & aurora (researched)

Beyond the LTE-verification sources above, the non-LTE work (the reentry blue,
the 2-temperature mode, and the aurora table) drew on:

**Non-LTE reentry / collisional-radiative implementation.** ADS:
`2025PhPl..32j3512A` (3-temperature collisional-radiative air plasma),
`2026arXiv260411856Z` (RAPRAL line-by-line + ray-tracing), `2011PhDT` (Monte
Carlo hypersonic radiation), `2001PhDT` (ionizational non-equilibrium recombining
air), `1994ntrs.rept23568C` (non-equilibrium reentry radiation). The N₂⁺ 1NG blue
is electron-impact (Park two-temperature) — the basis of saha_boltzmann's `t_elec`
mode.

**CR data availability** (verified, correcting an earlier overstatement — data
exists for major atmospheres): LXCat electron-scattering cross-section database
(Pitchford et al. 2017, *Plasma Processes & Polymers*) covers 42 species incl.
N₂/O₂/CO₂/CH₄/H₂/CO/NO/SO₂; CoRaM-AIR two-temperature CR (829 electronic states);
Mars/Titan/Jupiter entry CR models exist. Sparse only for exotic exoplanet
compositions. HITRAN/HITEMP for molecular line lists.

**Aurora (forbidden-line + quenching).** Mechanisms: `1960JChPh..32..607Y`
(auroral green OI 557.7 in N₂ afterglows), `1989RSPSA.424....1S` (O(¹S) airglow
mechanism), `1990AdSpR..10e..31F` (Venus nightglow O ¹D/¹S from dissociative
recombination + soft-electron precipitation). Lifetimes/quenching: Slanger &
Copeland (energetic-oxygen review), Sobral et al. 1993 JGR 98 (O(¹D)+O(³P)),
Rees 1989 (standard aeronomy). Quenching coefficients are standard textbook
values cross-checked against these, not freshly extracted.

## Related
- [tools.md](tools.md) — the build scripts + DBs
- engine: `scripts/refs/saha_boltzmann.py`, `build_element_temperature_colors.py`
- design log: `.agents/skills/firefly-cfg-workspace/saha-boltzmann/context-notes.md`
