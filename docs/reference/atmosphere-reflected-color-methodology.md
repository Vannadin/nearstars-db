<!-- 대기 조성에서 반사·산란 가시광 색(스펙트럼→sRGB)을 도출하는 방법론 레퍼런스 -->
# Atmosphere Reflected-Color Methodology — Composition → Spectrum → sRGB

> Source: synthesis of the planetary reflected-light / albedo-spectrum literature
> (Sudarsky+ 2000/2003, Marley+ 1999, Cahoy+ 2010, Karkoschka 1994, Irwin+ 2024,
> Khare+ 1984, Tomasko+ 2008, Carlson+ 2016, Gao+ 2021, Sneep & Ubachs 2005,
> Sagan+ 1993, Krissansen-Totton+ 2016) plus the per-species optical-constant portal
> (Polyanskiy 2024 / refractiveindex.info) and the engineering colorimetry standards
> (CIE 1931 color-matching functions; IEC 61966-2-1 sRGB).
> Citations resolved against NASA ADS (the registered ADS_API_TOKEN), not ad-hoc
> web search; arXiv id where one exists, otherwise the authoritative ADS bibcode.
> Purpose: a reusable recipe for **choosing and justifying** the visible
> reflected/scattered color of a planet's atmosphere, sky, and cloud deck from its
> composition + cloud/haze state + host-star illumination, as the prerequisite for
> a later tool that emits Scatterer atmosphere-color cfg.
> This is a working reference, not a textbook — see §8 for the verified citations.

**Scope — what this doc is NOT.** This is about light the atmosphere
**reflects/scatters** (sky color, cloud-deck color, the disk-integrated hue of the
planet). It is **not** about:

- **Emission / plasma color** (reentry glow, airglow, aurora) — that lives in the
  `firefly-cfg` skill and `composition-color.md`. Different physics: line/band
  *emission* from excited species, not scattering of starlight.
- **Solid surface / mineral color** (regolith, ice, ocean reflectance) — a separate
  future doc. The atmosphere's reflected color sits *on top of* whatever the surface
  contributes; for a thick cloud deck the surface is irrelevant, for a thin clear
  atmosphere over bright terrain the surface dominates and this doc only adds a tint.

## Table of Contents

1. [Why Atmosphere Color Is a Principled Choice](#1-why-atmosphere-color-is-a-principled-choice)
2. [The Three Color-Setting Processes](#2-the-three-color-setting-processes)
3. [Rayleigh Scattering — the Blue Baseline](#3-rayleigh-scattering--the-blue-baseline)
4. [Aerosols & Clouds — Mie Scattering and the Grey/White Veil](#4-aerosols--clouds--mie-scattering-and-the-greywhite-veil)
5. [Chromophores — Absorption That Sets the Hue](#5-chromophores--absorption-that-sets-the-hue)
6. [Spectrum → sRGB With the Host Star as Illuminant](#6-spectrum--srgb-with-the-host-star-as-illuminant)
7. [Worked Examples](#7-worked-examples)
8. [Annotated Bibliography](#8-annotated-bibliography)
9. [Related](#related)

---

## 1. Why Atmosphere Color Is a Principled Choice

For essentially no NearStars target do we **measure** the visible color of the
atmosphere. Even for the solar-system planets the "true color" is a reconstruction;
for exoplanets we have, at best, a broadband geometric albedo at one or two phases.
So the color we put in a Scatterer cfg is a **principled choice within physical
bounds**, exactly in the spirit of the surface-pressure doc's §1 — physics sets the
band, a documented tie-break picks the value.

What actually constrains the color, in decreasing order of how often we have it:

- **Composition** (from Phase 2/3): which gases are present sets the Rayleigh
  baseline and which molecular absorbers can cut into the reflected spectrum. This
  is the firmest input.
- **Cloud/haze state**: whether a condensate or photochemical-haze deck exists, how
  deep it sits, and its particle size. Usually inferred from temperature + chemistry,
  rarely observed directly for exoplanets.
- **Chromophore identity**: the specific colored minority species (sulfur allotropes,
  tholins, NH₄SH photoproducts). This is the **least constrained** link — even for
  Jupiter the red chromophore was contested for decades (Carlson+ 2016). For an
  exoplanet it is essentially always a choice.

The honest position (echoed in §5): the **blue/grey/white axis is physics**
(Rayleigh vs Mie, §3–4), but the **warm-hue axis is a chromophore choice** bounded
by what photochemistry plausibly produces. Record which chromophore you assumed and
why, the same way pressure is recorded on the Phase 4 board.

---

## 2. The Three Color-Setting Processes

Reflected atmosphere color is the outcome of three competing processes acting on the
host star's incident spectrum on the way down and back out:

1. **Rayleigh scattering** by gas molecules — strongly wavelength-dependent
   (σ ∝ λ⁻⁴), scatters blue far more than red. Dominant in a *thin, clear*
   atmosphere → blue sky (§3).
2. **Mie / aerosol scattering** by cloud and haze particles — wavelength-flat when
   particles are large (→ grey/white deck), wavelength-dependent when particles are
   small and absorbing (→ colored haze). Dominant whenever a cloud or haze deck is
   optically thick (§4).
3. **Molecular / particulate absorption** — removes specific wavelengths from the
   reflected beam. Gas bands (CH₄ eating red, ozone Chappuis eating green-orange) and
   chromophore aerosols (sulfur, tholins eating blue) set the **hue** that survives
   (§5).

The recipe is: build the wavelength-dependent reflectance (geometric albedo)
`A(λ)` from these three, multiply by the host-star SED, integrate against the CIE
color-matching functions, convert to sRGB (§6). The whole pipeline is

```
host SED  S(λ)  ─┐
                 ├─► reflected spectrum  R(λ) = S(λ)·A(λ)  ─► XYZ ─► linear sRGB ─► gamma ─► hex
albedo A(λ) ─────┘
```

---

## 3. Rayleigh Scattering — the Blue Baseline

A clear gas column scatters light with cross-section

```
σ_R(λ) = (24 π³ / N² λ⁴) · ((n²−1)/(n²+2))² · F_K(λ)
```

where `n(λ)` is the gas refractive index, `N` the number density at which `n` is
referenced, and `F_K` the **King depolarization factor** correcting for molecular
anisotropy (≈ 1.02 for N₂, ≈ 1.0 for the noble gases; CH₄ and CO₂ have their own
values). The λ⁻⁴ dependence is the reason a thin clear atmosphere looks **blue** —
short wavelengths scatter ~(700/450)⁴ ≈ 6× more strongly than long ones, so the
diffuse sky light is blue while the directly transmitted beam reddens.

Two practical grounding points:

- **Per-gas refractivity.** σ_R scales with `((n²−1)/(n²+2))²`, so a gas's
  refractivity sets how blue its sky is. CO₂ scatters ~2.5× more than air per
  molecule; H₂/He far less. Measured Rayleigh cross-sections for the common
  atmospheric gases (N₂, O₂, CO₂, CH₄, Ar) are tabulated by **Sneep & Ubachs 2005**
  — the canonical lab reference for σ_R, including the King-factor corrections. For a
  gas outside that set (H₂/He, H₂O, NH₃, SO₂, …) pull the real index `n(λ)` from the
  **refractiveindex.info** database (Polyanskiy 2024), and **use the gas-phase entry**
  — the same site's liquid/solid pages (e.g. liquid CH₄ at 90 K) are surface data for
  the surface-color doc, not for atmospheric Rayleigh. Pin each value to the dataset's
  own primary source (the site exposes it) — the database is the portal, not the
  citation of record.
- **Optical depth gates the effect.** Rayleigh blue is only visible when the column
  is optically thin enough that scattered photons escape rather than being absorbed
  or scattered again by aerosol. A thick cloud deck (§4) sits *above* the Rayleigh
  column and hides it; the blue only shows in **cloud clearings**, and a deeper
  clearing means a longer clear-gas path and therefore a **bluer** patch.

In exoplanet transmission spectra the same physics shows up as a **Rayleigh slope**
(transit depth rising toward the blue as α ≈ −4 in `d ln δ / d ln λ`); a shallower
slope flags an aerosol/haze layer flattening the spectrum. This is the diagnostic
that ties a *transmission* observation to the *reflected* color we want — the same
aerosols that flatten the slope grey out the reflected sky.

---

## 4. Aerosols & Clouds — Mie Scattering and the Grey/White Veil

When condensate clouds or photochemical haze are present, scattering off the
particles dominates and the governing parameter is the **size parameter**

```
x = 2 π r / λ
```

(`r` = particle radius). Three regimes:

- **x ≪ 1** (particles much smaller than λ): Rayleigh-like, σ ∝ λ⁻⁴ — small *and
  absorbing* haze particles therefore impose a wavelength-dependent color (§5,
  tholins).
- **x ~ 1**: full **Mie** regime, resonant, with a strong forward-scattering lobe.
- **x ≫ 1** (cloud droplets/ice grains ≫ λ, e.g. µm-scale water or ammonia
  particles): scattering is nearly **wavelength-flat** → a **grey/white** deck. A
  thick water- or ammonia-ice cloud with no chromophore is white; this is why a
  high, fresh cloud deck reads as a bright neutral veil that *raises the albedo and
  washes out hue*.

The canonical modern review of how aerosols form and what they do to spectra across
the planetary range is **Gao+ 2021** (*Aerosols in Exoplanet Atmospheres*). For the
specific link from cloud microphysics to **reflected** spectra and albedos of
giant planets, the foundational works are **Marley+ 1999** (clear vs cloudy giant
albedos — clouds raise the albedo and flatten it) and the composition-class
framework of **Sudarsky+ 2000 / 2003** (§7). The key takeaway for color: **clouds
push toward neutral/white and high albedo; the hue has to come from a chromophore
mixed into or above the deck.**

---

## 5. Chromophores — Absorption That Sets the Hue

The neutral blue (Rayleigh) / white (thick cloud) baseline is tinted by absorbers
that remove part of the reflected spectrum. The major ones:

- **CH₄ — the red eater → blue-green giants.** Methane has strong absorption bands
  across the red and near-IR; a deep clear methane column absorbs long wavelengths
  and leaves the reflected light **blue-green**. This is *why Uranus and Neptune are
  cyan*, and the canonical reflected-spectrum reference is the **Karkoschka 1994**
  geometric-albedo atlas of the Jovian planets and Titan (300–1000 nm). The subtle
  part — *why Uranus is paler / greener than Neptune despite similar CH₄* — is a
  difference in their **aerosol** layers: **Irwin+ 2024** show a thicker, more
  reflective haze layer over Uranus mutes the deep-blue methane signature, so the
  Uranus/Neptune color split is set by aerosols, not composition (§7).

- **Tholins / organic haze → orange.** Small, absorbing organic photochemical-haze
  particles (CH₄/N₂ photolysis products) absorb strongly in the blue and scatter the
  rest, giving a **yellow-orange-brown** color. The optical-constants standard is
  **Khare+ 1984** (Titan tholins, 0.02–920 µm); the *in-situ* Titan aerosol model
  pinning the orange is **Tomasko+ 2008** (Huygens DISR). Tholin haze is the
  archetype for any reduced-CH₄ atmosphere going orange (§7, Titan).

- **Sulfur species → yellow/brown/red.** Elemental sulfur allotropes (S₈ and
  polysulfides), ammonium hydrosulfide (NH₄SH) photoproducts, and SO₂ are the leading
  candidates for the warm bands of Jupiter and Saturn. The identity is genuinely
  uncertain: **Carlson+ 2016** argue Jupiter's red chromophore is a **photolyzed-NH₃
  + acetylene** product rather than pure sulfur, after decades of the sulfur
  hypothesis. The honest rule: warm jovian deck color is "sulfur-or-tholin-like
  chromophore" — a bounded choice, not an identified compound.

- **Ozone (Chappuis band) → adds blue to Earth's sky.** O₃ has a broad weak
  absorption across ~500–700 nm (the Chappuis band) that removes green-orange and
  deepens the blue/violet of a thick O₂-O₃ atmosphere at twilight. Cross-sections:
  **Serdyuchenko/Orphal+ 2016**. Minor next to Rayleigh for Earth's daytime sky, but
  the canonical example of a *gas-phase visible* absorber that is neither CH₄ nor a
  cloud.

For absorbers and aerosols the input is the **complex** index `n(λ) + i·k(λ)` (the
`k` extinction part carries the absorption); the same **refractiveindex.info**
portal (Polyanskiy 2024) holds the tholin, water-ice, ammonia-ice, sulfur and
mineral optical constants for the Mie/absorption step — again citing each dataset's
own primary source per row (Khare+ 1984 for tholins, etc.).

**Honesty section.** The blue↔grey↔white axis (§3–4) is solid physics tied to
composition and particle size. The **warm hue (yellow/orange/red/brown) is the
soft link**: it depends on a minority chromophore whose identity is often unknown
even in the solar system. For a NearStars body, pick a chromophore that
photochemistry plausibly produces from the Phase 3 composition (reduced/CH₄-rich →
tholin orange; NH₃/sulfur present and warm → jovian yellow-brown), state it, and
treat the exact hue as a documented choice within that family — never as a derived
fact.

---

## 6. Spectrum → sRGB With the Host Star as Illuminant

This is the colorimetry engine. The one physics subtlety that distinguishes "doing
it right" from a naive conversion: **the illuminant is the host star's spectral
energy distribution, not the D65 daylight white point.** A planet around an M dwarf
is lit by a red sun, so even a perfectly grey (wavelength-flat) cloud deck reflects
*warm* light; a planet around an A star reflects bluer. The reflected spectrum is

```
R(λ) = S(λ) · A(λ)
```

with `S(λ)` the host SED (a stellar model — e.g. a PHOENIX/Kurucz spectrum at the
star's Teff/logg, or a blackbody as a coarse stand-in) and `A(λ)` the geometric
albedo built in §3–5. Then the standard CIE pipeline:

1. **Integrate against the CIE 1931 2° color-matching functions** `x̄(λ), ȳ(λ),
   z̄(λ)` over ~380–780 nm:

   ```
   X = k ∫ R(λ) x̄(λ) dλ,   Y = k ∫ R(λ) ȳ(λ) dλ,   Z = k ∫ R(λ) z̄(λ) dλ
   ```

   `k` is a normalization. For a **surface/material color** (what we want — the
   color of the planet *as lit by its star*) normalize so the chosen illuminant's
   own white maps to neutral: `k = 1 / ∫ S(λ) ȳ(λ) dλ`. Using the host SED (not
   D65) in *both* `R(λ)` and the normalization is the correct treatment — it bakes
   the star's color temperature into the result.

2. **XYZ → linear sRGB** via the IEC 61966-2-1 matrix (D65 primaries):

   ```
   [ R_lin ]   [  3.2406  −1.5372  −0.4986 ] [ X ]
   [ G_lin ] = [ −0.9689   1.8758   0.0415 ] [ Y ]
   [ B_lin ]   [  0.0557  −0.2040   1.0570 ] [ Z ]
   ```

3. **Gamma (sRGB transfer function)** to get display values: for each channel
   `c_lin`, `c = 1.055·c_lin^(1/2.4) − 0.055` for `c_lin > 0.0031308`, else
   `c = 12.92·c_lin`; clip to [0,1] and ×255.

Notes:
- **Gamut clipping**: saturated single-band results (deep CH₄ cyan) can fall outside
  sRGB; clip to the gamut boundary rather than letting channels go negative.
- **D65 vs host-star white point**: if you instead want "how the planet would look
  to a human eye adapted to *that* sky" you'd chromatically adapt to the host white;
  for cfg we want the color *as the star lights it*, so step 1's host-SED
  normalization is the right default. State which you used.
- There is **no canonical ADS paper for the colorimetry math itself** — it is the
  CIE/IEC engineering standard. The closest astronomy precedents for doing
  spectrum→true-color on planetary albedos are Karkoschka 1994 (which reports the
  Jovian colors) and the disk-integrated-color classification of
  **Krissansen-Totton+ 2016** (which color-classifies solar-system bodies in a
  photometric color space), but neither is the source of the matrix — cite the
  standards for that.

---

## 7. Worked Examples

Each example is grounded in the surveyed papers and states composition → process →
color.

**Earth — Rayleigh-blue sky.** N₂/O₂, thin and clear in the visible. Rayleigh λ⁻⁴
scattering (§3, Sneep & Ubachs 2005) dominates → blue sky; the disk-integrated
planet reads as a **pale blue** body, the "pale blue dot," confirmed by the Galileo
flyby spectrum of **Sagan+ 1993**. The ozone Chappuis band (§5) deepens the blue at
twilight but is secondary. Surface (ocean) and clouds modulate brightness, but the
*hue* is Rayleigh.

**Uranus / Neptune — CH₄ blue-green, split by aerosols.** Both have H₂/He + a few %
CH₄. Deep clear methane absorbs the red (§5) → **cyan** in the Karkoschka 1994
albedo spectra. The two differ not in composition but in **aerosol**: Irwin+ 2024
show Uranus carries a thicker, more reflective high haze that whitens and pales its
color, while Neptune's thinner haze lets the deep methane blue show → Neptune is the
**deeper, richer blue**, Uranus the **paler green-cyan**. This is the textbook case
that *the same gas gives different colors depending on the aerosol deck above it*
(§4 vs §5).

**Titan — tholin orange.** N₂ + CH₄ with a thick organic photochemical haze. Small,
blue-absorbing tholin particles (§5; Khare+ 1984 optical constants, Tomasko+ 2008
Huygens in-situ model) make the haze **orange-brown** and optically thick enough to
hide the surface entirely. The hue is set by the haze absorbing blue, not by any
Rayleigh signature — the opposite limit from Earth.

**Gas-giant warm cloud deck — the α Cen "Polyphemus" appearance.** A temperate
(~225 K) jovian-class giant lands in **Sudarsky Class II** ("water cloud" class;
Sudarsky+ 2000/2003): high water + NH₄SH condensate decks, optically thick µm-scale
particles → a bright, largely **neutral/white** Mie deck (§4) raising the albedo.
The **warm Jupiter-like tone** comes from chromophores mixed into the upper deck —
sulfur species (S₈/NH₄SH polysulfides) and CH₄/PH₃-photolysis tholins (§5), the same
"sulfur-or-tholin" bounded choice that colors Jupiter (Carlson+ 2016 caveat). In
**deep cloud-clearings** the line of sight reaches the clear H₂/He+CH₄ column below,
so those patches go **Rayleigh-blue** (§3) — and a *deeper* clearing means a longer
clear-gas path, hence a **bluer** patch. The deck therefore reads as a warm
cream/tan banded body with blue belts in the clearings.

For the illuminant (§6): **α Cen A is a G2V essentially a solar twin**, so its SED
white point is **near-solar** — the cloud deck's intrinsic chromophore color is
rendered almost exactly as it would appear under our Sun (no M-dwarf reddening, no
A-star bluing). This makes α Cen A b/Polyphemus an unusually "honest" color target:
the composition→albedo color and the displayed color nearly coincide.

---

## 8. Annotated Bibliography

Each entry: authors, year, journal, **verified** arXiv id (or a flag where none
exists, with the ADS bibcode), and one line on what it contributes. Citation counts
(ADS, at survey time) given for spot-checking.

- **Sneep, M. & Ubachs, W. (2005)** — *JQSRT* 92, 293. **No arXiv** (bibcode
  `2005JQSRT..92..293S`). Direct lab measurement of Rayleigh scattering
  cross-sections + King depolarization for the common atmospheric gases. The σ_R(λ)
  ground truth for §3. (275 cites.)

- **Gao, P. et al. (2021)** — *JGR Planets* 126, e06655. **arXiv:2102.03480.**
  *Aerosols in Exoplanet Atmospheres* — the canonical modern review of aerosol
  formation, microphysics, and their effect on spectra across the planetary range.
  §4. (125 cites.)

- **Marley, M. S. et al. (1999)** — *ApJ* 513, 879. **arXiv:astro-ph/9810073.**
  *Reflected Spectra and Albedos of Extrasolar Giant Planets I* — clear vs cloudy
  giant albedos; clouds raise and flatten the albedo. Foundational reflected-light
  model. §4. (277 cites.)

- **Sudarsky, D., Burrows, A. & Pinto, P. (2000)** — *ApJ* 538, 885.
  **arXiv:astro-ph/9910504.** *Albedo and Reflection Spectra of Extrasolar Giant
  Planets* — introduces the giant-planet composition/albedo classes. §4, §7. (314
  cites.)

- **Sudarsky, D., Burrows, A. & Hubeny, I. (2003)** — *ApJ* 588, 1121.
  **arXiv:astro-ph/0210216.** *Theoretical Spectra and Atmospheres of Extrasolar
  Giant Planets* — the **five composition classes** (Class I/II water clouds, …);
  Class II is the temperate-giant case for the Polyphemus example. §7. (273 cites.)

- **Cahoy, K. L., Marley, M. S. & Fortney, J. J. (2010)** — *ApJ* 724, 189.
  **arXiv:1009.3071.** Exoplanet albedo spectra and colors as a function of phase,
  separation, and metallicity — how reflected color shifts with system parameters.
  §6 context. (135 cites.)

- **Karkoschka, E. (1994)** — *Icarus* 111, 174. **No arXiv** (bibcode
  `1994Icar..111..174K`). Spectrophotometry of the Jovian planets and Titan,
  300–1000 nm — the geometric-albedo atlas that grounds the CH₄ blue-green of Uranus
  / Neptune and the colors of Jupiter/Saturn/Titan. §5, §7. (332 cites.)

- **Irwin, P. G. J. et al. (2024)** — *MNRAS* 527, 11521. **No arXiv** (bibcode
  `2024MNRAS.52711521I`, DOI 10.1093/mnras/stad3761). Models Uranus's seasonal
  color and compares to Neptune; the **aerosol** difference (thicker reflective haze
  on Uranus) explains why Uranus is paler/greener despite similar CH₄. §5, §7. (13
  cites — recent.)

- **Khare, B. N. et al. (1984)** — *Icarus* 60, 127. **No arXiv** (bibcode
  `1984Icar...60..127K`). Optical constants of Titan tholins, 0.02–920 µm — the
  standard refractive indices for organic photochemical haze. §5, §7. (612 cites.)

- **Tomasko, M. G. et al. (2008)** — *Planet. Space Sci.* 56, 669. **No arXiv**
  (bibcode `2008P&SS...56..669T`). In-situ Titan aerosol model from Huygens DISR —
  pins the orange tholin haze from inside the atmosphere. §5, §7. (242 cites.)

- **Carlson, R. W. et al. (2016)** — *Icarus* 274, 106. **No arXiv** (bibcode
  `2016Icar..274..106C`). Jupiter's red chromophore as a photolyzed-NH₃ + acetylene
  product — the cautionary tale that warm jovian color chromophores are uncertain.
  §5, §7. (56 cites.)

- **Orphal, J., Staehelin, J., Tamminen, J. … Serdyuchenko, A. et al. (2016)** —
  *J. Mol. Spectrosc.* 327, 105. **No arXiv** (bibcode `2016JMoSp.327..105O`).
  "Absorption cross-sections of ozone … Status report 2015" — the recommended ozone
  UV–visible cross-sections including the Chappuis band (consolidates the
  Serdyuchenko & Gorshelev 2014 laboratory dataset). §5. (72 cites.)

- **Sagan, C. et al. (1993)** — *Nature* 365, 715. **No arXiv** (bibcode
  `1993Natur.365..715S`). *A Search for Life on Earth from the Galileo Spacecraft* —
  Earth's disk-integrated spectrum, the canonical pale-blue-dot Rayleigh reference.
  §7. (316 cites.)

- **Krissansen-Totton, J., Schwieterman, E. W. et al. (2016)** — *ApJ* 817, 31.
  **arXiv:1512.00502.** *Is the Pale Blue Dot Unique?* — disk-integrated photometric
  color classification of solar-system bodies; closest astronomy precedent for color
  space placement (not the colorimetry matrix). §6. (31 cites.)

- **Polyanskiy, M. N. (2024)** — *Scientific Data* 11, 94. **No arXiv** (bibcode
  `2024NatSD..11...94P`). The **refractiveindex.info** database of optical constants:
  the data portal for per-species real index `n(λ)` (Rayleigh, §3) and complex index
  `n+ik` (aerosols/absorbers, §5). A curated **aggregator** — each dataset cites its
  own primary lab source, which is the per-row citation of record; cite this paper for
  the database itself. Match the phase to the use (gas-phase for atmosphere; liquid/
  solid for the surface-color doc). (335 cites.)

- **CIE 1931 2° standard observer color-matching functions** — engineering standard
  (CIE 15; not an ADS work). The `x̄/ȳ/z̄(λ)` integration kernels of §6.

- **IEC 61966-2-1:1999 (sRGB)** — engineering standard (not an ADS work). The XYZ→
  linear-sRGB matrix and the sRGB gamma transfer function of §6.

**No canonical ADS paper for**: the spectrum→sRGB colorimetry math itself (it is the
CIE/IEC standard, cited as such above). Everything else has a clear high-citation
canonical work.

---

## Related

- `docs/reference/tidally-locked-temperature-methodology.md` — the sibling recipe
  for the temperature that decides which Sudarsky class / condensate deck a giant
  falls into (the ~225 K Class-II anchor for the Polyphemus example).
- `docs/reference/exoplanet-atmosphere-methodology.md` — the sibling recipe for the
  *composition* (pressure, μ, redox) that feeds the Rayleigh baseline and the set of
  available chromophores here.
- **Emission color** (reentry plasma, airglow, aurora) lives in the `firefly-cfg`
  skill and `composition-color.md` — a different mechanism (line/band emission, not
  scattering of starlight). Don't confuse it with reflected color.
- **Surface / mineral color** (regolith, ice, ocean reflectance) is a **future
  sibling doc**; the atmosphere's reflected color sits on top of the surface
  contribution, and for thin clear atmospheres the surface dominates.
- Phase 3 synthesis skill (`nearstars-phase3`) — where the chosen atmosphere color
  (and the assumed chromophore) is recorded per body before it feeds the Scatterer
  cfg writer downstream.
