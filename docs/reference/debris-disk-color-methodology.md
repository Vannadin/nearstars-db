<!-- Phase 3 디스크색 합성: Mie 산란광 reflectance로 disk_tint_rgb_hex 도출, 고증/vivid 변종 + B/I 검증 -->
# Debris-Disk Color Methodology: Composition + Grain Size → Mie Scattering → Reflectance → sRGB

> Source: synthesis of the debris-disk scattered-light and grain-optics literature
> (Bohren & Huffman 1983 for the Mie kernel; Dohnanyi 1969 for the collisional
> size distribution; the per-composition optical-constant papers Draine 2003,
> Rouleau & Martin 1991, Warren & Brandt 2008, Jäger+ 2003, Khare+ 1984; the
> measured scattered-light colors Krist 2005 / Fitzgerald 2007 / Graham 2007 for
> AU Mic and Kalas 2005 / Acke 2012 for Fomalhaut) plus the per-species
> optical-constant portal (Polyanskiy 2024 / refractiveindex.info, **solid/ice-phase**
> entries) and the engineering colorimetry standards (CIE 1931; IEC 61966-2-1 sRGB)
> reused from the atmosphere doc.
> Citations resolved against NASA ADS (the registered ADS_API_TOKEN), not ad-hoc
> web search; arXiv id where one exists, otherwise the authoritative ADS bibcode.
> Purpose: a reusable recipe for **synthesizing and justifying** the visible color of
> a circumstellar **debris disk** (`disk_tint_rgb_hex`) from grain composition and
> grain-size distribution, when no resolved scattered-light color exists.
> This is a working reference, not a textbook. See §8 for the verified citations.
> Tool: `scripts/phase3/disk_color_mie.py`.

**Scope: what this doc is NOT.** This is about light that **circumstellar dust
grains scatter** from their host star: the disk's intrinsic visible hue, stored as
`disk_tint_rgb_hex`. It is the **dust-in-scattered-light** sibling of the atmosphere
and surface reflectance docs, the THIRD reflectance sibling. It is **not** about:

- **Thermal / mm disk emission**: the far-IR/sub-mm/mm flux that Spitzer, Herschel
  and ALMA actually detect for most belts is a **different observable** (grain
  *thermal* emission, set by temperature and emissivity, not scattering of starlight).
  Most NearStars belts have only that, which is precisely why their *color* must be
  synthesized here (§6 measure-vs-synthesize rule).
- **Atmosphere reflected/scattered color** (sky, cloud, haze): sibling
  `atmosphere-reflected-color-methodology.md`. Same colorimetry engine, gas-phase
  optical constants.
- **Solid-surface color** (rock, regolith, ice): sibling
  `surface-color-albedo-methodology.md`. Same engine, **solid/ice-phase** optical
  constants that overlap with the grain materials here (water ice, silicate, tholin).
- **Planetary-ring color per se**: a circum*planetary* ring (Saturn-like) is also
  scattered-light off particles and shares this physics, but its grains are cm–m
  boulders, not µm dust, so the Mie size regime is irrelevant (geometric optics, ring
  color ≈ surface color of the constituent ice/rock). Treat a ring with the surface
  doc; this doc is for the µm-grain *debris* regime where `x = 2πa/λ ~ 1`.

The three reflectance docs share one colorimetry engine (spectrum → sRGB with the
host star as illuminant); **this doc does not restate it**: see §5 and the atmosphere
doc §6.

## Table of Contents

1. [Why a Disk Color Is a Principled Choice](#1-why-a-disk-color-is-a-principled-choice)
2. [Principle: Scattered Starlight and the Reflectance Convention](#2-principle-scattered-starlight-and-the-reflectance-convention)
3. [Method: Mie Q_sca, the Grain-Size Integral, Per-Composition n,k](#3-method-mie-q_sca-the-grain-size-integral-per-composition-nk)
4. [Q_sca(λ) → sRGB (Use the Atmosphere Doc's Engine)](#4-qscaλ--srgb-use-the-atmosphere-docs-engine)
5. [The Faithful / Vivid Two-Variant Convention](#5-the-faithful--vivid-two-variant-convention)
6. [Validation, and the Measure-vs-Synthesize Rule](#6-validation-and-the-measure-vs-synthesize-rule)
7. [Worked Examples](#7-worked-examples)
8. [Annotated Bibliography](#8-annotated-bibliography)
9. [Related](#related)

---

## 1. Why a Disk Color Is a Principled Choice

For **almost no** NearStars debris belt do we have a measured visible scattered-light
color. Resolved scattered-light imaging in the optical exists for only a handful of
the brightest, nearest disks; the rest are detected purely in **thermal/mm emission**
(an infrared/sub-mm excess or an ALMA map), which carries no visible-color information
at all. So the `disk_tint_rgb_hex` we put in a cfg is, for every belt except the two
imaged ones, a **principled, physics-grounded synthesis within bounds**, exactly in
the spirit of the atmosphere doc's §1 and the surface doc's §1: composition and grain
size set the hue, the Mie physics turns them into a spectrum, and a documented
white-balance convention (§2) fixes the chroma.

What constrains the answer, in decreasing order of how often we have it:

- **Grain size distribution** (small-end cutoff, slope): the **single biggest lever**
  on hue. Where the smallest grains sit relative to optical wavelengths sets whether
  the disk scatters blue (small grains, Rayleigh-like rise) or neutral-grey (large
  grains, geometric optics). The small-end is anchored by the **radiation-pressure
  blowout size** `a_blow` (§3), which is derived deterministically from the host's
  `L/M`, so even when nothing else is known, the host luminosity pins the cutoff.
- **Composition** (from Phase 2/3): silicate vs carbon vs ice vs organic sets the
  complex index `n+ik`, hence how strongly the grain absorbs the blue (an absorbing
  carbon/tholin grain reddens; a transparent ice/forsterite grain takes its color
  from size alone). The second-biggest lever.
- **Collisional slope `q`**: in a steady-state collisional cascade this is fixed near
  the canonical `q = 3.5` (Dohnanyi 1969), so it is rarely a free choice.

The honest position (echoed in §6's uncertainty note): **grain size + composition set
the hue family** (small grains → blue, large grains → grey, absorbing material →
redward), which is solid Mie physics; but the **exact `n,k` per composition class is a
representative literature value, not a belt-specific measurement**, and the absolute
chroma is a white-balance/saturation convention (§5), not an observable. Record the
assumed composition and the blowout-size input the same way the surface doc records
the assumed surface state.

---

## 2. Principle: Scattered Starlight and the Reflectance Convention

A debris disk's **visible** color is **scattered starlight**, not thermal emission.
The grains have an intrinsic wavelength-dependent scattering efficiency `Q_sca(λ)`;
the disk we see in the optical is

```
scattered_SED(λ) ∝ S(λ) · Q_sca(λ)
```

with `S(λ)` the host-star SED. `Q_sca(λ)` *is* the disk's reflectance spectrum.

**The stored convention is the intrinsic dust color (star removed).** The cfg tint
encodes `Q_sca(λ)` **grey-balanced**, i.e. the renderer re-applies the host star's
light, so the stored value must be **star-independent**. The white-balance is defined
so that **a wavelength-flat `Q_sca` maps to neutral grey**:

```
reflectance_color  =  whitebalance[ Q_sca(λ) ]  =  sRGB[ Q_sca(λ) / Q_flat(λ) ]
```

where the divisor is the sRGB color of a flat reflectance under the same colorimetry
(in the tool, `_lin_rgb(np.ones_like(WL))`). This is what keeps an **icy blue disk
blue even around a red M dwarf**: the blueness is a property of the *grains*, and
baking the star's redness into the stored tint would wrongly swamp it. The renderer
owns the illuminant; the DB owns the intrinsic dust color.

(The tool also exposes an **absolute** convention `color_absolute()`: `S(λ)·Q_sca(λ)`
white-balanced to the **Sun**, so a neutral grain under a Sun-like star → white, under
a K/M star → warm, under an A star → blue-white. That is the star-baked-in repo
convention upgraded from a crude "star color × albedo" to proper grain-size Mie
scattering. The **reflectance** convention above is the canonical one for
`disk_tint_rgb_hex`; the absolute one exists for the star-color-included slots.)

---

## 3. Method: Mie Q_sca, the Grain-Size Integral, Per-Composition n,k

The synthesis is fully deterministic from four inputs per belt: composition class,
grain-size range `[a_min, a_max]`, slope `q`, and host `L/M/Teff`. Steps (each maps
to a function in `scripts/phase3/disk_color_mie.py`):

**1. Mie scattering efficiency: Bohren & Huffman.** For a single sphere of size
parameter `x = 2πa/λ` and complex index `m = n − ik`, `Q_sca(x, m)` comes from the
**Bohren & Huffman (1983)** `bhmie` algorithm (downward recurrence for the logarithmic
derivative, then the Mie `a_n, b_n` coefficients). `mie_qsca()` is a dependency-free
numpy port of `bhmie`. The size parameter `x` (i.e. **grain radius vs optical
wavelength**) is the dominant color driver, and the algorithm captures it exactly.

**2. Grain-size integral over a collisional cascade.** A real belt is a power-law
distribution of sizes, not one grain. We integrate `Q_sca` weighted by the cross-
section-weighted **collisional size distribution**

```
dn/da ∝ a^(−q),   q ≈ 3.5   (Dohnanyi 1969 steady-state cascade)
```

from a small-end floor `a_min` to a large-end `a_max`, weighting each size by
`a^(−q) · a²` (number × geometric cross-section) and renormalizing. The small-end
floor is the **radiation-pressure blowout radius**: grains below it are ejected by
stellar radiation pressure, so they cannot accumulate:

```
a_blow ≈ 0.5 µm · (L/L☉)/(M/M☉) · (2.5 g cm⁻³ / ρ)
```

(`ρ = 2.5 g cm⁻³` is a representative grain-density assumption, not a measurement).
**Luminous hosts blow out bigger grains**, raising `a_min`, which pushes the disk's
color from blue toward grey: this is why the same icy composition reads blue around
AU Mic (M dwarf, tiny `a_blow`) and grey around Fomalhaut (A star, large `a_blow`).
Where Phase 2 reports an explicit minimum grain size (e.g. the ε Eri cold ring's
~15 µm grains), that overrides `a_blow`.

**3. Per-composition optical constants `n(λ), k(λ)`.** Sampled across the optical band
(400–800 nm) per composition class and interpolated onto the working grid. The
imaginary part `k` carries the **blue-absorption** that reddens absorbing materials;
transparent grains (ice, forsterite) get their color from grain size alone. The
classes the tool ships, each pinned to its primary lab source (§8):

| Class | Material | Optical constants |
|---|---|---|
| `astrosil` | astronomical silicate | Draine 2003 |
| `carbon` | amorphous carbon | Rouleau & Martin 1991 |
| `ice` | water ice | Warren & Brandt 2008 |
| `olivine` | Mg-rich crystalline forsterite | Jäger+ 2003 |
| `tholin` | Titan-type organic tholin | Khare+ 1984 |

Two-component grains (`ice_sil`, `sil_org`) are mixed with **Maxwell–Garnett
effective-medium theory**: spherical inclusions of volume fraction `f` in a host
matrix, mixing the dielectric function `ε = (n+ik)²` (not a linear `n,k` average,
which is unphysical). The inclusion volume fractions are derived from a 50/50 *mass*
split and bulk densities (ice 1.0, silicate 3.3, organic 1.3 g cm⁻³), with the
majority-volume component as the host; MG is valid for `f` below the percolation
threshold (~0.3), satisfied here.

**4. Composition is the second lever, size is the first.** The `n,k` values are
*representative optical-band values per class*, documented as a first-order
assumption: they are not belt-specific measurements, and the doc is honest that the
dominant color driver is the size parameter `x`, which the integral captures
correctly. Treat the composition class as setting the **hue family** and the blowout
size as setting **how far toward grey** it sits.

---

## 4. Q_sca(λ) → sRGB (Use the Atmosphere Doc's Engine)

The conversion from the reflectance spectrum `Q_sca(λ)` to an sRGB hex is **identical**
to the atmosphere and surface cases and is **fully documented in
`atmosphere-reflected-color-methodology.md` §6**. Do not restate the matrix here. The
pipeline: integrate the spectrum against the **CIE 1931 2° color-matching functions**
to XYZ, apply the **IEC 61966-2-1** linear-sRGB matrix, gamma-encode, clip to gamut.
There is **no canonical ADS paper for the colorimetry math**: it is the CIE/IEC
engineering standard, cited as such in the atmosphere doc §8.

Two disk-specific implementation notes:

- **CMF kernel.** The tool evaluates the CIE 1931 CMFs via the **multi-lobe analytic
  Gaussian fit of Wyman, Sloan & Shirley (2013)** rather than tabulated values, a
  closed-form approximation to `x̄/ȳ/z̄(λ)` accurate enough for color work and
  dependency-free. (This paper is a *Journal of Computer Graphics Techniques* article
  and is **not indexed in ADS**, see §8.) It is an implementation detail of the same
  CIE 1931 standard, not a different observer.
- **The reflectance white-balance (§2) is the input difference.** The atmosphere doc
  feeds the geometric albedo `A(λ)`, the surface doc the bidirectional reflectance
  `r(λ)`; here the input is `Q_sca(λ)`, and the canonical stored color is the
  **grey-balanced** version (flat `Q_sca` → neutral grey, star removed). That
  normalization, `Q_sca(λ)` divided by the sRGB color of a flat spectrum, is the one
  twist on top of the atmosphere doc's §6.

Optical constants `(n,k)` come from the **refractiveindex.info portal (Polyanskiy
2024)** introduced in the atmosphere doc, **solid/ice-phase** entries here (the same
phase as the surface doc), each row pinned to its own primary lab source (§3 table, §8).

---

## 5. The Faithful / Vivid Two-Variant Convention

Following the Sol-Configs model, the cfg writer emits **both** color variants for each
belt, distinguished only by **chroma** (saturation about the grey point), same hue:

- **faithful** (`SAT_FAITHFUL = 0.82`): mildly *de*-saturated, physically honest. Dust
  scattered-light colors are genuinely subtle, not neon; this is the grounded value.
- **vivid** (`SAT_VIVID = 2.6`): saturation-boosted so the disk's color is clearly
  visible in-game, the prettier pack.

Both are computed by scaling chroma about the white-balanced grey point
(`rgb = mean + sat·(rgb − mean)`), so they share the **same hue** and differ only in
how far off grey they sit. The user picks the pack; record both in the Phase 3 report.

---

## 6. Validation, and the Measure-vs-Synthesize Rule

**The synthesis is only trustworthy because the blowout/composition physics reproduces
the two belts that DO have measured scattered-light colors.** Use the `band_ratio()`
helper, the blue/near-IR reflectance ratio `B/I` (445 nm / 806 nm), to check any new
belt against the right measured analog before committing the tint:

| Belt | Measured | Synthesis | Verdict |
|---|---|---|---|
| **AU Mic** | **blue**, `B/I ~ 1.6` (Krist 2005) | `B/I ≈ 1.74` | ✓ blue reproduced |
| **Fomalhaut main ring** | **~neutral/grey**, `B/I ~ 1.0` (Kalas 2005) | `B/I ≈ 0.87` | ✓ grey reproduced |

AU Mic is an M dwarf: a tiny `a_blow` leaves sub-micron grains that scatter blue.
Fomalhaut is an A star: a large `a_blow` leaves only big, grey-scattering grains. The
model gets both ends right **from the host `L/M` alone**, which is what licenses
synthesizing the unmeasured belts in between.

**The measure-vs-synthesize rule:**

- **Belt imaged in scattered light** (Fomalhaut main ring = Kalas 2005; AU Mic =
  Krist 2005) → use the **MEASURED** color. Do **not** overwrite it with synthesis;
  the synthesis exists to *match* it, not replace it.
- **Thermal / mm-only belt** (no optical scattered-light image, the common case) →
  **synthesize** with this method. Flag `confidence: low` and note it in the host's
  Phase 3 Open items.

---

## 7. Worked Examples

Each grounds host + composition + grain size → reflectance color, via the `BELTS`
table in the tool.

**AU Mic (validation, measured blue).** M1V host, `L/L☉ ≈ 0.10`, so a sub-micron
`a_blow`. Sub-micron astrosilicate grains scatter strongly blueward → `B/I ≈ 1.74`,
matching the measured blue disk (Krist 2005; Fitzgerald 2007 multiwavelength; Graham
2007 traced the blue to primordial grain *growth*/porosity via polarimetry). The
small-grain archetype.

**Fomalhaut main ring (validation, measured grey).** A3V host, `L/L☉ ≈ 16.6`, so a
large `a_blow`: only big grains survive, scattering neutrally → `B/I ≈ 0.87`,
matching the measured ~grey ring (Kalas 2005; cometary fluffy aggregates, Acke 2012).
The large-grain archetype. The inner warm and intermediate Fomalhaut dust are PR-drag
fragments of the *same* outer belt (~50–80% water ice by volume, Sommer+ 2025), so the
tool gives them the same icy `ice_sil` composition and hence the same synthesized hue
as the cold ring.

**ε Eri (synthesized, thermal/mm only).** K2V host. Inner asteroidal silicate belt
(Backman 2009) and an icy/silicate cold ring at ~64 au with ~15 µm grains
(`ice_sil`, Su+ 2017). There is **no** optical scattered-light detection: HST/STIS
sets only a deep upper limit (Sai+ 2024), so the color is synthesized and flagged
low-confidence. The explicit 15 µm grain floor (not `a_blow`) pushes the cold ring
toward grey despite its icy composition.

**HD 69830 (synthesized, thermal/mm only).** K0V host with a warm ~1 au belt of
**crystalline olivine/forsterite** (Beichman 2005; Lisse 2007). Forsterite is
transparent in the optical (`k` ~ 1e-4), so its color comes from grain size alone, not
absorption. A near-neutral synthesized hue. The transparent-grain archetype.

**τ Ceti (synthesized, thermal/mm only).** G8V host with a broad belt of amorphous
silicate + organics (Lawler 2014), handled as a Maxwell–Garnett `sil_org` grain
(silicate inclusions in an organic host). The organic component's blue-absorbing `k`
gives a slightly reddened synthesized hue relative to a pure-silicate belt. The
absorbing-grain archetype.

---

## 8. Annotated Bibliography

Each entry: authors, year, journal/book, **verified** arXiv id (or a flag where none
exists, with the ADS bibcode), and one line on what it contributes. Citation counts
(ADS, at survey time) given for spot-checking.

**Mie kernel and size distribution.**

- **Bohren, C. F. & Huffman, D. R. (1983)**: *Absorption and Scattering of Light by
  Small Particles*, Wiley. **Book, no arXiv** (bibcode `1983asls.book.....B`). The
  canonical Mie-scattering text; its `bhmie` algorithm is the `Q_sca(x, m)` kernel
  ported in the tool. §3. (4180 cites, the field's standard reference.)

- **Dohnanyi, J. S. (1969)**: *JGR* 74, 2531. **No arXiv** (bibcode
  `1969JGR....74.2531D`). *Collisional Model of Asteroids and Their Debris*: the
  origin of the `dn/da ∝ a^(−3.5)` steady-state collisional-cascade size distribution.
  §3. (1033 cites.)

**Per-composition optical constants `n(λ)+ik(λ)`** (each pins one `_NK` class):

- **Draine, B. T. (2003)**: *ApJ* 598, 1017. **arXiv:astro-ph/0304060.** *Scattering
  by Interstellar Dust Grains. I. Optical and Ultraviolet*: the astronomical-silicate
  optical constants (`astrosil`). §3. (581 cites.) *(The script comment names "Draine
  2003"; ADS confirms this is the correct paper. Note the alternative canonical
  silicate reference Draine & Lee 1984 is the older compilation; the tool uses the 2003
  update, as cited.)*

- **Rouleau, F. & Martin, P. G. (1991)**: *ApJ* 377, 526. **No arXiv** (bibcode
  `1991ApJ...377..526R`). *Shape and Clustering Effects on the Optical Properties of
  Amorphous Carbon*: the amorphous-carbon constants (`carbon`). §3. (579 cites.)

- **Warren, S. G. & Brandt, R. E. (2008)**: *J. Geophys. Res. Atmos.* 113, D14220.
  **No arXiv** (bibcode `2008JGRD..11314220W`). *Optical constants of ice from the
  ultraviolet to the microwave: a revised compilation*, the water-ice constants
  (`ice`); the revised successor to Warren 1984 (`1984ApOpt..23.1206W`). The tool uses
  the 2008 revision, as cited. §3. (820 cites.)

- **Jäger, C., Dorschner, J., Mutschke, H., Posch, Th. & Henning, Th. (2003)**:
  *A&A* 408, 193. **No arXiv** (bibcode `2003A&A...408..193J`). *Steps toward
  interstellar silicate mineralogy VII*: sol-gel Mg-silicate (crystalline
  forsterite/olivine) constants (`olivine`). §3. (250 cites.)

- **Khare, B. N., Sagan, C., Arakawa, E. T., Suits, F., Callcott, T. A. & Williams,
  M. W. (1984)**: *Icarus* 60, 127. **No arXiv** (bibcode `1984Icar...60..127K`).
  *Optical constants of organic tholins produced in a simulated Titanian atmosphere*:
  the Titan-tholin constants (`tholin`); the same Khare-type optical constants the
  atmosphere doc uses for haze and the surface doc uses for tholin coatings. §3.
  (612 cites.)

**Colorimetry kernel.**

- **Wyman, C., Sloan, P.-P. & Shirley, P. (2013)**: *Journal of Computer Graphics
  Techniques* 2(2), 1. **NOT INDEXED IN ADS** (confirmed absent; it is a graphics-
  journal article, not an astronomy work). The multi-lobe analytic Gaussian fit to the
  CIE 1931 2° color-matching functions used by `cie_xyz()`. An implementation of the
  CIE 1931 standard, not a separate observer. §4.

- **CIE 1931 / IEC 61966-2-1 (sRGB)**: engineering standards (not ADS works); the
  colorimetry math is **not restated here**: see `atmosphere-reflected-color-
  methodology.md` §6/§8. §4.

**Validation disks (the two MEASURED scattered-light colors).**

- **Krist, J. E. et al. (2005)**: *AJ* 129, 1008. **No arXiv** (bibcode
  `2005AJ....129.1008K`). *HST ACS Coronagraphic Imaging of the AU Microscopii Debris
  Disk*: the measured **blue** color (`B/I ~ 1.6`) that the small-grain synthesis must
  reproduce. §6, §7. (119 cites.)

- **Kalas, P., Graham, J. R. & Clampin, M. (2005)**: *Nature* 435, 1067.
  **arXiv:astro-ph/0506574.** *A planetary system as the origin of structure in
  Fomalhaut's dust belt*: the measured ~**neutral/grey** main ring that the large-
  grain synthesis must reproduce. §6, §7. (357 cites.)

**Per-belt composition / grain-size provenance** (Phase 2 inputs to the `BELTS` table):

- **Fitzgerald, M. P. et al. (2007)**: *ApJ* 670, 536. **[arXiv:0705.4196](https://arxiv.org/abs/0705.4196).**
  *The AU Microscopii Debris Disk: Multiwavelength Imaging and Modeling.* §7.
  (70 cites.)

- **Graham, J. R. et al. (2007)**: *ApJ* 654, 595. **arXiv:astro-ph/0609332.**
  *The Signature of Primordial Grain Growth in the Polarized Light of the AU Mic Debris
  Disk*: porous-aggregate grains. §7. (137 cites.)

- **Acke, B. et al. (2012)**: *A&A* 540, A125. **[arXiv:1204.5037](https://arxiv.org/abs/1204.5037).** *Herschel images
  of Fomalhaut*: cometary fluffy-aggregate grains in the main ring. §7. (112 cites.)

- **Sommer, M. et al. (2025)**: *MNRAS* 539, 439. **[arXiv:2503.18127](https://arxiv.org/abs/2503.18127).** *A PR-drag
  origin for the Fomalhaut disc's pervasive inner dust*: the inner/intermediate dust
  is PR-drag debris of the outer belt, ~50–80% water ice by volume. §7. (11 cites.)

- **Backman, D. et al. (2009)**: *ApJ* 690, 1522. **[arXiv:0810.4564](https://arxiv.org/abs/0810.4564).** *Epsilon
  Eridani's Planetary Debris Disk: Structure and Dynamics*: silicate inner +
  icy/silicate cold ring. §7. (126 cites.)

- **Su, K. Y. L. et al. (2017)**: *AJ* 153, 226. **[arXiv:1703.10330](https://arxiv.org/abs/1703.10330).** *The Inner
  25 au Debris Distribution in the ε Eri System.* §7. (32 cites.)

- **Sai, K. P. M. et al. (2024)**: *AJ* 168, 169. **[arXiv:2408.06973](https://arxiv.org/abs/2408.06973).** *Deepest
  Limits on Scattered Light Emission from the Epsilon Eridani Debris Disk*: the
  HST/STIS optical **non-detection** (so ε Eri's color is synthesized, not measured).
  §7. (8 cites.)

- **Su, K. Y. L. et al. (2013)**: *ApJ* 763, 118. **[arXiv:1301.1331](https://arxiv.org/abs/1301.1331).** *Asteroid
  Belts in Debris Disk Twins: Vega and Fomalhaut*: featureless silicate, large blowout
  grains (Vega; thermal/mm only). (138 cites.)

- **Beichman, C. A. et al. (2005)**: *ApJ* 626, 1061. **arXiv:astro-ph/0504491.**
  *An Excess Due to Small Grains around the Nearby K0 V Star HD 69830*: crystalline
  silicate warm belt. §7. (168 cites.)

- **Lisse, C. M. et al. (2007)**: *ApJ* 658, 584. **arXiv:astro-ph/0611452.** *On
  the Nature of the Dust in the Debris Disk around HD 69830*: crystalline
  olivine/forsterite. §7. (95 cites.)

- **Wyatt, M. C. et al. (2012)**: *MNRAS* 424, 1206. **[arXiv:1206.2370](https://arxiv.org/abs/1206.2370).** *Herschel
  imaging of 61 Vir*: no spectral features (61 Vir; thermal/mm only). (107 cites.)

- **Lawler, S. M. et al. (2014)**: *MNRAS* 444, 2665. **[arXiv:1408.2791](https://arxiv.org/abs/1408.2791).** *The
  debris disc of solar analogue τ Ceti*: amorphous silicate + organics. §7. (40 cites.)

**Optical-constant portal.**

- **Polyanskiy, M. N. (2024)**: *Scientific Data* 11, 94. **No arXiv** (bibcode
  `2024NatSD..11...94P`). The **refractiveindex.info** database; **here the solid/ice-
  phase entries** (silicate, water ice, forsterite, tholin) for the per-composition
  `n+ik` step (§3), the same portal/phase as the surface doc and the gas-phase
  counterpart used by the atmosphere doc. Cite each material's own primary source per
  row (the five papers above). (335 cites.)

**No clean canonical ADS work for**: (a) the spectrum→sRGB colorimetry math (CIE/IEC
standards, owned by the atmosphere doc §6); (b) the **Wyman+ 2013** CMF fit: it is a
*Journal of Computer Graphics Techniques* article and is **not indexed in ADS** (verified
absent), so it is cited by journal reference only, as an implementation of the CIE 1931
standard. All astronomy citations above were confirmed by direct ADS bibcode/arXiv query.

---

## Related

- `docs/reference/atmosphere-reflected-color-methodology.md`: the **sibling** that
  owns the **colorimetry engine** (§6: spectrum → XYZ → sRGB with the host-star SED)
  reused here, and the **refractiveindex.info portal** (Polyanskiy 2024; gas-phase
  there, solid/ice-phase here). Atmosphere reflected color is a *different* observable
  from disk scattered light. Don't conflate them.
- `docs/reference/surface-color-albedo-methodology.md`: the **sibling** for solid
  surfaces; its grain optical constants **overlap** with the disk grain materials here
  (water ice = Warren & Brandt 2008, tholin = Khare-type, silicate). A circum*planetary*
  ring of cm–m boulders is closer to that doc (geometric optics) than to this one (µm
  Mie regime).
- `docs/reference/planetary-dynamo-scaling.md`: the **gold-standard sibling for
  citation rigor** and domain-of-validity honesty (no-arXiv flagging, regime caveats);
  this doc mirrors its bibliography discipline.
- **Tool:** `scripts/phase3/disk_color_mie.py`: the implementation (Mie `bhmie`,
  grain-size integral, Maxwell–Garnett blends, CIE→sRGB, faithful/vivid). The per-belt
  grain-size/composition/citation provenance lives in its `BELTS` table comments;
  those citations are pulled up into §8 here.
- **Skill:** `nearstars-phase3` consumes this method to choose a belt's
  `disk_tint_rgb_hex` decision and record the faithful/vivid variants in the per-host
  Phase 3 report.
- `db/disks_curated.json` stores disk **geometry only** (radius, width, inclination,
  aspect ratio), **not** the tint; the color provenance is in the tool/Phase 3 report,
  not the DB (the JSON round-trip was not clean). See `project-nearstars-ring-fabrication`.
