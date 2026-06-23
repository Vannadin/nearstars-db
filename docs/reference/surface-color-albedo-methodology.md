<!-- 고체 표면(암석·레골리스·얼음) 조성에서 가시광 색과 Bond/기하 알베도를 도출하는 방법론 레퍼런스 -->
# Surface Color & Albedo Methodology — Composition → Reflectance → sRGB + Bond Albedo

> Source: synthesis of the planetary-surface reflectance-spectroscopy literature
> (Burns 1993, Sherman 1985, Morris+ 1985/2000, Clark 1981, Hapke 1981/1993/2012,
> Hapke 2001, Pieters+ 2000, Kokaly+ 2017 / USGS Spectral Library v7, Warren 1984 /
> Warren & Brandt 2008, Grundy & Schmitt 1998, Grundy+ 1999, Cruikshank+ 1993/1998,
> Grundy+ 2016, Buratti+ 2017) plus the per-species optical-constant portal
> (Polyanskiy 2024 / refractiveindex.info, **solid/liquid-phase** entries) and the
> Bond/geometric-albedo definitions of standard planetary-science texts
> (de Pater & Lissauer, *Planetary Sciences*).
> Citations resolved against NASA ADS (the registered ADS_API_TOKEN), not ad-hoc
> web search; arXiv id where one exists, otherwise the authoritative ADS bibcode.
> Purpose: a reusable recipe for **choosing and justifying** the visible color of a
> solid planetary surface (rock, regolith, ice) and the **Bond albedo** that the
> equilibrium-temperature formula needs, from composition.
> This is a working reference, not a textbook — see §8 for the verified citations.

**Scope — what this doc is NOT.** This is about light a **solid surface**
(rock/regolith/ice) **reflects**: its disk hue and its bolometric Bond albedo. It
is the SURFACE sibling of the atmosphere reflected-color doc. It is **not** about:

- **Atmosphere reflected/scattered color** (sky, cloud deck, haze) — that is the
  sibling `atmosphere-reflected-color-methodology.md`. The two **compose**: the
  atmosphere's reflected color sits *on top of* the surface color. For a thick
  atmosphere or an optically thick cloud/haze deck the surface is **hidden** and
  this doc is moot (Venus, Titan, the giants); it matters for **thin- or
  no-atmosphere** bodies (Mars, the Moon, icy moons, airless rock).
- **Emission / plasma color** (reentry glow, airglow, aurora, lava thermal
  emission) — that lives in the `firefly-cfg` skill and `composition-color.md`.
  Different physics: *emission* from excited/hot matter, not reflection of starlight.

The two reflectance docs share one colorimetry engine (spectrum → sRGB with the host
star as illuminant); **this doc does not restate it** — see §5 and the atmosphere
doc §6.

## Table of Contents

1. [Why Surface Color & Albedo Are a Principled Choice](#1-why-surface-color--albedo-are-a-principled-choice)
2. [Why Minerals Have Color — Electronic Transitions](#2-why-minerals-have-color--electronic-transitions)
3. [From Composition to a Reflectance Spectrum — Libraries & the Hapke Model](#3-from-composition-to-a-reflectance-spectrum--libraries--the-hapke-model)
4. [Modifiers — Space Weathering, Grain Size, Ices & Organics](#4-modifiers--space-weathering-grain-size-ices--organics)
5. [Reflectance Spectrum → sRGB (Use the Atmosphere Doc's Engine)](#5-reflectance-spectrum--srgb-use-the-atmosphere-docs-engine)
6. [Bond & Geometric Albedo — the `A` for the Energy Budget](#6-bond--geometric-albedo--the-a-for-the-energy-budget)
7. [Worked Examples](#7-worked-examples)
8. [Annotated Bibliography](#8-annotated-bibliography)
9. [Related](#related)

---

## 1. Why Surface Color & Albedo Are a Principled Choice

For **no** NearStars exo-target do we measure the visible color or the Bond albedo
of its surface — those quantities are essentially never resolved even for nearby
exoplanets (a broadband geometric albedo at one phase is the best case, and only for
a handful of hot transiting worlds). So both the surface color we put in a cfg and
the `A` we feed the temperature formula are a **principled, analog-grounded choice
within physical bounds**, exactly in the spirit of the atmosphere doc's §1 and the
surface-pressure doc's §1 — composition sets the band, a documented tie-break picks
the value.

What actually constrains the answer, in decreasing order of how often we have it:

- **Composition** (from Phase 2/3): which minerals/ices/organics are present sets
  the diagnostic absorption bands (hence the hue) and the baseline brightness. This
  is the firmest input, and it is the one thing the analog libraries (§3) turn into
  a spectrum.
- **Surface state — grain size and weathering**: the *same* composition can be
  bright or dark, neutral or reddened, by large factors depending on grain size and
  exposure age (§4). This is the link that moves the **albedo** most, and it is
  rarely constrained for an exo-body.
- **Texture / mixing geometry**: intimate vs areal mixtures, fresh exposures vs
  mantled regolith. Least constrained; usually a deliberate art choice (the α Cen
  "half sulfur, half basalt" example, §7).

The honest position (echoed in §6's uncertainty note): **mineral identity sets the
hue family** (Fe³⁺ → red, mafic → dark with a 1 µm band, water ice → bright neutral,
tholin → red-brown), which is solid physics (§2); but the **brightness/albedo and
the degree of reddening are the soft links**, driven by weathering and grain size,
which can swing the Bond albedo by 2–5×. Record the assumed surface state the same
way the atmosphere doc records the assumed chromophore.

**Posture — surface appearance is an interesting-first axis.** Because the
composition→appearance mapping is so degenerate (Earth alone is wildly varied), the
*look* of a surface — hue, pattern, texture, the mixing geometry — is a deliberate
**interesting-first art choice**, not a derivation: pick the compelling reading and
note the canonical alternative, per the project's interesting-first cascade. This doc
is the **gate, not the dictator** of that look — it supplies (a) the physically
plausible **albedo band** and (b) the grounded **hue family** (§2) the art choice
must stay inside. The **one hard tie** is the **area-weighted Bond albedo**: it is not
aesthetic, it propagates into temperature through `T_eq ∝ (1−A)^¼` (§6). So the rule
is *look = interesting-first, but cascade the chosen skin's `A` into the temperature*
— a bright icy reskin and a dark basaltic one at the same insolation must carry
different `T_eq`.

---

## 2. Why Minerals Have Color — Electronic Transitions

A rock's visible color comes almost entirely from the **electronic transitions of
transition-metal ions** (overwhelmingly iron) in its minerals — not from molecular
vibrations (those sit in the IR). Two mechanisms dominate:

- **Crystal-field (d–d) transitions.** A transition-metal cation (Fe²⁺, Fe³⁺, also
  Cr³⁺, Ti) sits in a coordination site whose surrounding anions split its 3d
  orbitals; electrons absorb specific visible/near-IR wavelengths jumping between the
  split levels. The canonical, exhaustive treatment is **Burns 1993** (*Mineralogical
  Applications of Crystal Field Theory*, 2nd ed.) — the textbook that explains, ion
  by ion and site by site, which band falls where. The most important planetary case:
  **Fe²⁺ in mafic silicates** (olivine, pyroxene) produces the broad **~1 µm
  absorption band** (with pyroxene adding a ~2 µm band), the diagnostic that makes
  basaltic surfaces dark and gives the band-depth/position mineralogy of the Moon,
  Mars and asteroids.
- **Charge-transfer (and the red of oxidized iron).** Far stronger than d–d, the
  **O²⁻ → Fe³⁺ ligand-to-metal charge-transfer** band sits in the **blue/UV** and
  has a wing that climbs steeply toward the blue. In a **ferric (oxidized) iron**
  mineral — hematite, goethite, nanophase ferric oxides — this band eats the blue end
  and leaves a strong **red visible slope**: this is *why Mars is red* and why any
  oxidized-dust surface is rusty. The electronic-structure basis is **Sherman 1985**
  (Fe³⁺ coordination-site electronic structure) and **Sherman & Waite / Sherman 1985–87**
  (charge-transfer in iron oxides); the laboratory reflectance demonstration tying it
  to the Mars color is **Morris+ 1985** (submicron ferric-oxide powders) with the
  in-situ Mars confirmation in **Morris+ 2000** (Pathfinder rocks and soils).

The takeaway for color: **reduced/ferrous mafic rock → dark, neutral-to-greenish
with a 1 µm band; oxidized ferric dust → red with a steep blue-absorbing slope.**
Fe oxidation state is the single biggest lever on rock hue.

---

## 3. From Composition to a Reflectance Spectrum — Libraries & the Hapke Model

The input the colorimetry engine (§5) needs is a **bidirectional reflectance
spectrum** `r(λ)` over ~380–780 nm. There are two grounded routes from composition
to that spectrum, and we use them in this order:

**(a) Look it up in a spectral library — the lab-data backbone.** Measured
reflectance spectra of real minerals, rocks and ices are the firmest possible input.
The canonical, openly citable database is the **USGS Spectral Library Version 7**
(**Kokaly+ 2017**), a few thousand laboratory reflectance spectra of minerals, rocks,
soils, ices and vegetation at known grain size — the descendant of the splib06
(Clark+ 2007) and earlier releases. The **RELAB** facility at Brown University (the
PDS "RELAB Spectral Library Bundle") is the complementary planetary-analog database
(meteorites, lunar/asteroid analogs, ices). For a body whose Phase 3 composition
names specific phases, pull their library spectra, mix them (see (b)), and feed the
result to §5. Diagnostic absorption bands map to mineralogy per the spectroscopy
foundations of **Clark 1981** (water frost/ice 0.65–2.5 µm) and the crystal-field
band assignments of §2.

**(b) Radiative transfer in a particulate surface — the Hapke model.** A library
spectrum is for one grain size and one geometry; a real surface is a packed mixture
of grains and you often need to (i) **mix** end-members and (ii) **rescale** for grain
size and viewing geometry. The canonical framework is **Hapke 1981** (*Bidirectional
Reflectance Spectroscopy I — Theory*) and its sequels (roughness 1984, opposition/
coherent backscatter 2002, porosity 2008), collected in the textbook **Hapke 1993/2012**
(*Theory of Reflectance and Emittance Spectroscopy*). Two facts from Hapke theory that
drive **brightness/albedo** directly:

- **Single-scattering albedo `w` is the per-grain property**; the bidirectional and
  the hemispheric reflectance both rise monotonically with `w`. Composition sets `w(λ)`
  through the imaginary index `k(λ)` and the grain size (absorption path = grain size
  × `k`).
- **Finer grains → brighter, weaker bands.** Smaller grains mean shorter absorption
  paths per grain and more scattering surfaces, so a finely comminuted version of the
  *same* mineral is brighter and its absorption bands are shallower. This is the
  mechanism behind "fresh = bright" and is the dominant grain-size lever on albedo (§4).

For mixing in practice you either combine library spectra (areal mixing = linear,
intimate mixing = nonlinear in `w`-space via Hapke) or convert per-species optical
constants `n(λ)+ik(λ)` to single-scattering albedo and run Hapke forward. The optical
constants come from the **refractiveindex.info** portal (**Polyanskiy 2024**) — and
**here we use the solid/liquid-phase entries** (crystalline minerals, water ice, N₂/
CH₄/CO₂ ices, tholins), the opposite of the atmosphere doc, which uses the gas-phase
pages of the same portal. Pin each row to its own primary lab source (e.g. Warren
1984 / Warren & Brandt 2008 for water ice).

---

## 4. Modifiers — Space Weathering, Grain Size, Ices & Organics

Composition fixes the hue family; these three processes move the **brightness, the
saturation, and the reddening** — often by more than the composition itself.

- **Space weathering — airless bodies darken and redden with age.** On a body with no
  atmosphere, micrometeorite impacts and solar-wind sputtering coat grains in
  **nanophase metallic iron (npFe⁰)**, which **darkens** the surface (lowers albedo),
  **reddens** the continuum slope, and **subdues the absorption bands** over time. The
  canonical reviews are **Hapke 2001** (*Space Weathering from Mercury to the Asteroid
  Belt* — the npFe⁰ mechanism) and **Pieters+ 2000** (*Space Weathering on Airless
  Bodies* — resolved with returned lunar samples, with the optical role of the finest
  fraction in Pieters+ 1993 / Noble+). Practical rule: a **young/fresh** airless
  surface (recent impact crater, fresh ice) is **brighter and bluer/less-red** than
  the **mature** regolith of the same composition. This single process is why the
  freshly exposed crater rays on the Moon are bright and the surrounding mare is dark.

- **Grain size.** Independent of weathering, **finer grains are brighter and have
  shallower bands** (§3, Hapke). A frost of fine ice grains reads near-white; the
  same ice as a clear slab or coarse blocks is darker and bluer-translucent. Grain
  size and weathering together set the albedo "knob" that composition cannot.

- **Ices and organics — the outer-solar-system surfaces.** Volatile-ice surfaces have
  their own color logic:
  - **Water ice** is **bright and slightly blue** in the visible (its absorption is
    weak in the visible and rises into the near-IR), with strong diagnostic NIR bands;
    the optical constants are **Warren 1984 / Warren & Brandt 2008**, and the
    temperature-dependent NIR spectrum is **Grundy & Schmitt 1998**, with the
    icy-outer-surface remote-sensing recipe in **Grundy+ 1999**. Fresh water-ice/snow
    is the brightest common natural surface (§6).
  - **N₂, CH₄, CO₂ ices** are bright and largely neutral/white; they dominate the
    high-albedo terrains of Pluto and Triton (**Cruikshank+ 1993**, *Ices on the
    Surface of Triton*; Owen+ 1993 for Pluto).
  - **Tholins / refractory organics redden and darken icy surfaces.** Radiation
    processing of CH₄/N₂ ices builds reddish organic residues; small amounts turn a
    neutral ice **orange-red** and lower its albedo. The archetype is **Cruikshank+
    1998** (*The Composition of Centaur 5145 Pholus* — the reddest known solar-system
    surface), the same tholin chemistry (Khare-type optical constants) that the
    atmosphere doc uses for haze, but here as a **surface** coating. This is what
    paints the dark-red "Cthulhu"/tholin terrains of Pluto against its pale N₂-ice
    plains.

The honest consequence: weathering + grain size + a trace organic coating can move a
surface's **albedo by a factor of 2–5 and its hue from neutral to deep red** without
changing the bulk composition at all. Treat the surface *state* as a recorded choice.

---

## 5. Reflectance Spectrum → sRGB (Use the Atmosphere Doc's Engine)

The conversion from a reflectance spectrum to an sRGB color is **identical** to the
atmosphere case and is **fully documented in
`atmosphere-reflected-color-methodology.md` §6** — do not restate it here. The one
difference is the **input spectrum**:

- Atmosphere doc: the input is the atmospheric **geometric albedo** `A(λ)` (Rayleigh
  + Mie + chromophore absorption).
- This doc: the input is the **surface bidirectional reflectance** `r(λ)` from §3–4
  (library spectrum, grain-size/weathering-adjusted via Hapke).

Everything downstream is the same: multiply by the **host-star SED** `S(λ)` (the
illuminant — an M-dwarf surface reads warm, an A-star surface reads cool), integrate
against the CIE 1931 color-matching functions to XYZ, apply the IEC 61966-2-1 sRGB
matrix, gamma-encode, clip to gamut. Reflected spectrum `R(λ) = S(λ)·r(λ)`; the rest
is the atmosphere doc's §6 verbatim. As there, there is **no canonical ADS paper for
the colorimetry math** — it is the CIE/IEC engineering standard, cited as such in the
atmosphere doc.

For a **thin-atmosphere** body the two docs **compose**: render the surface color
here, then let the atmosphere doc's reflected/scattered contribution tint it (a thin
clear atmosphere over bright terrain → the surface dominates with a slight Rayleigh
tint; a thick deck → the surface is hidden and only the atmosphere doc applies).

---

## 6. Bond & Geometric Albedo — the `A` for the Energy Budget

The color (§5) is the *spectral* reflectance integrated against the eye; the energy
budget needs a *bolometric* scalar. Two albedos, one relation:

- **Geometric albedo `p`** — the disk-integrated brightness at zero phase (full
  illumination, back-scatter) relative to a perfectly diffuse (Lambert) disk of the
  same size. It is what you measure photometrically at opposition. Spectrally
  resolved, `p(λ)`, it is essentially the §5 input.
- **Bond albedo `A`** — the fraction of **all** incident stellar power (integrated
  over wavelength **and** over all scattering angles) that the body reflects. This is
  the energy-budget albedo.

They are linked by the **phase integral `q`** (the angular integral of the body's
phase function):

```
A_Bond = q · p_geometric        (per wavelength: A(λ) = q(λ)·p(λ);  bolometric: weight by the stellar SED)
```

The phase integral `q` (≈ 1 for a Lambert surface; ~0.3–0.5 for dark back-scattering
regolith like the Moon, ~0.7–1.3 for bright icy/cloud bodies with forward scattering)
encodes how light is distributed with phase angle. Definitions and the `A = q·p`
relation are standard planetary-science text material (**de Pater & Lissauer,
*Planetary Sciences***); the historical roots are Russell's reflecting-planet
photometry and Bond's energy balance. In practice we estimate `p` from §5 and adopt a
`q` appropriate to the surface type (analog-grounded), or take the Bond albedo
directly from a solar-system analog.

**Typical Bond albedos by surface type** (analog anchors — pick by composition+state):

| Surface type | Bond albedo `A` | Notes / analog |
|---|---|---|
| Fresh water-ice / snow | ~0.6–0.8 | brightest natural surface (Europa, Enceladus, fresh frost) |
| N₂/CH₄/CO₂ volatile-ice plains | ~0.5–0.85 | Pluto Sputnik / Triton bright terrain |
| Bright icy moon (mature) | ~0.3–0.6 | Europa ~0.6, mixed/old ice lower |
| Oxidized (ferric) dust / rust | ~0.2–0.3 | **Mars ~0.25** — bright but red |
| Tholin / dark-red organic ice | ~0.05–0.15 | Pholus-like; weathered icy terrain |
| Basalt / mare regolith, space-weathered | ~0.06–0.12 | **the Moon ~0.11** (very dark) |
| Anorthosite / fresh rock | ~0.15–0.25 | lunar highlands, fresh exposures |
| Carbonaceous / C-type regolith | ~0.02–0.06 | darkest common surfaces |

**This `A` is exactly the albedo consumed by the equilibrium-temperature formula in
the sibling temperature doc:**

```
T_eq = [ S (1 − A) / (4 σ) ]^(1/4)
```

(`S` = stellar flux at the body, `σ` = Stefan–Boltzmann). A surface choice therefore
**propagates into temperature**: a basaltic α Cen body (`A`~0.1) runs hotter than the
same body re-skinned as ice (`A`~0.6) at the same insolation. See
`tidally-locked-temperature-methodology.md`, which takes this `A` as input.

**Uncertainty.** The surface color and albedo of an exo-body are **never measured** —
they are an analog-grounded choice. Composition fixes the hue *family* (§2), but
**space weathering and grain size move the Bond albedo by large factors** (2–5×, §4),
which then moves `T_eq` (∝ (1−A)^¼, a milder but real dependence). Always record the
assumed surface state and the analog the albedo was taken from; treat `A` as a range,
not a number, when it feeds the temperature doc.

---

## 7. Worked Examples

Each grounds composition → process → (color, Bond albedo).

**Mars — oxidized-iron red, dark.** Basaltic substrate mantled in **ferric (oxidized)
nanophase iron-oxide dust**. The O²⁻→Fe³⁺ charge-transfer band (§2; Sherman 1985)
eats the blue and gives the steep **red visible slope** demonstrated in the lab by
**Morris+ 1985** and confirmed in situ by **Morris+ 2000**. Despite being "bright
rust," the Bond albedo is **only ~0.25** (§6) — red, not bright-white. This is the
charge-transfer archetype.

**Europa — water-ice, bright and bluish.** A nearly pure **water-ice** crust. Water
ice is bright and slightly blue in the visible with strong NIR bands (§4; Warren 1984,
Grundy & Schmitt 1998), giving a **high Bond albedo (~0.6+)** and a bright neutral-to-
bluish disk. The icy-moon archetype: composition → bright neutral, the opposite end
of the albedo table from the Moon.

**Pluto / Triton — N₂/CH₄/CO₂ ices + tholin reddening.** Volatile **N₂/CH₄/CO₂ ices**
(Cruikshank+ 1993 for Triton; Owen+ 1993 for Pluto) make **bright, pale, high-albedo**
plains — Pluto's Sputnik Planitia reads near-white, with hemispheric Bond/geometric
albedos mapped by **Buratti+ 2017** and compositions by **Grundy+ 2016**. *Alongside*
them, **radiation-processed tholins** (Cruikshank+ 1998, Pholus chemistry, §4) paint
the **dark-red** terrains (Cthulhu). So a single body is **spatially bimodal**: pale
high-albedo ice next to dark-red low-albedo organics — high but very variable albedo.

**The Moon — basalt/anorthosite + space weathering → grey, very dark.** Mafic mare
basalt and anorthositic highlands, both with the Fe²⁺ 1 µm band (§2), heavily
**space-weathered**: nanophase iron (Hapke 2001; Pieters+ 2000) **darkens and reddens
and subdues the bands**, leaving a **grey** surface at a very low Bond albedo (**~0.11**).
The space-weathering archetype — and the demonstration that the *same* fresh material
(bright crater rays) and mature regolith (dark mare) differ in albedo by the weathering
state alone (§4).

**NearStars α Cen application (qualitative).** A basaltic **volcanic body with sulfur
deposits** is a decided Dante-style surface: **half sulfur-yellow, half basalt-grey**.
Composition picks both axes — the basalt half is mafic-Fe²⁺ dark grey at a low Bond
albedo (~0.1, Moon-like, §6), while the **elemental-sulfur** deposits give the bright
sulfur-yellow band (sulfur's electronic absorption cuts the blue → yellow) at a higher
local albedo; the disk-integrated `A` is a low-ish weighted blend. Its **icy moon**
reads as a bright neutral water-ice body (Europa-like, `A`~0.6, §6, bluish). A
**continental rocky "lake world"** mixes fresh silicate rock (anorthosite-like, mid
albedo) with liquid-water lakes (low albedo, dark) → a moderate, spatially varied `A`.
In each case the composition picks the **color** (§5) and the **Bond albedo** (§6),
and that `A` is what then feeds the equilibrium-temperature calculation
(`tidally-locked-temperature-methodology.md`) — a darker basaltic skin runs hotter
than an icy one at the same α Cen insolation.

---

## 8. Annotated Bibliography

Each entry: authors, year, journal/book, **verified** arXiv id (or a flag where none
exists, with the ADS bibcode), and one line on what it contributes. Citation counts
(ADS, at survey time) given for spot-checking.

- **Burns, R. G. (1993)** — *Mineralogical Applications of Crystal Field Theory*, 2nd
  ed., Cambridge Univ. Press. **Book, no arXiv** (bibcode `1993macf.book.....B`). The
  canonical text on how transition-metal (Fe²⁺/Fe³⁺/Cr/Ti) crystal-field transitions
  set mineral color and the diagnostic ~1 µm mafic band. §2. (591 cites.)

- **Sherman, D. M. (1985)** — *Physics and Chemistry of Minerals* 12, 161. **No
  arXiv** (bibcode `1985PCM....12..161S`). Electronic structure of Fe³⁺ coordination
  sites in iron oxides — the basis for the blue/UV charge-transfer band that reddens
  oxidized iron. §2. (149 cites.)

- **Morris, R. V. et al. (1985)** — *JGR* 90, 3126. **No arXiv** (bibcode
  `1985JGR....90.3126M`). Spectral/physicochemical properties of submicron ferric-oxide
  powders — the lab demonstration of the Mars-red ferric slope. §2, §7. (371 cites.)

- **Morris, R. V. et al. (2000)** — *JGR Planets* 105, 1757. **No arXiv** (bibcode
  `2000JGR...105.1757M`). Mineralogy/alteration of Mars Pathfinder rocks and soils —
  in-situ confirmation of the oxidized-iron Mars color. §2, §7. (267 cites.)

- **Clark, R. N. (1981)** — *JGR* 86, 3087. **No arXiv** (bibcode `1981JGR....86.3087C`).
  Water frost and ice near-IR reflectance 0.65–2.5 µm — foundational ice-spectroscopy
  reference and band assignments. §3. (146 cites.)

- **Kokaly, R. F. et al. (2017)** — *USGS Data Series 1035*. **USGS report, no arXiv**
  (bibcode `2017usgs.rept...14K`, DOI 10.3133/ds1035). **USGS Spectral Library Version
  7** — the canonical openly citable laboratory reflectance library of minerals, rocks,
  soils and ices (successor to splib06, Clark+ 2007 `2007usgs.rept...16C`). §3. (352
  cites.)

- **Hapke, B. (1981)** — *JGR* 86, 3039. **No arXiv** (bibcode `1981JGR....86.3039H`).
  *Bidirectional Reflectance Spectroscopy I — Theory* — the canonical particulate-
  surface radiative-transfer model linking single-scattering albedo, grain size and
  geometry to reflectance. §3. (1519 cites — the field's most-cited surface paper.)

- **Hapke, B. (2012)** — *Theory of Reflectance and Emittance Spectroscopy*, 2nd ed.,
  Cambridge Univ. Press. **Book, no arXiv** (bibcode `2012tres.book.....H`, DOI
  10.1017/CBO9781139025683; 1st ed. 1993 `1993tres.book.....H`, 507/682 cites). The
  textbook collecting the Hapke model and its grain-size/porosity/roughness
  corrections. §3. (507 cites, 2012 ed.)

- **Hapke, B. (2001)** — *JGR Planets* 106, 10039. **No arXiv** (bibcode
  `2001JGR...10610039H`). *Space Weathering from Mercury to the Asteroid Belt* — the
  nanophase-iron darkening/reddening mechanism on airless bodies. §4, §7. (815 cites.)

- **Pieters, C. M. et al. (2000)** — *Meteoritics & Planetary Science* 35, 1101. **No
  arXiv** (bibcode `2000M&PS...35.1101P`). *Space Weathering on Airless Bodies* —
  resolved with returned lunar samples; the optical effects of the finest fraction.
  §4, §7. (611 cites.)

- **Warren, S. G. (1984)** — *Applied Optics* 23, 1206. **No arXiv** (bibcode
  `1984ApOpt..23.1206W`). Optical constants of water ice from the UV to the microwave —
  the canonical ice `n+ik` (revised compilation Warren & Brandt 2008,
  `2008JGRD..11314220W`, 820 cites). §3, §4, §7. (1319 cites.)

- **Grundy, W. M. & Schmitt, B. (1998)** — *JGR Planets* 103, 25809. **No arXiv**
  (bibcode `1998JGR...10325809G`). Temperature-dependent near-IR absorption spectrum
  of hexagonal H₂O ice — the lab basis for cold-surface water-ice modeling. §4, §7.
  (298 cites.)

- **Grundy, W. M. et al. (1999)** — *Icarus* 142, 536. **No arXiv** (bibcode
  `1999Icar..142..536G`). Near-IR spectra of icy outer-solar-system surfaces — the
  remote-determination recipe for ice on distant bodies. §4. (121 cites.)

- **Cruikshank, D. P. et al. (1993)** — *Science* 261, 742. **No arXiv** (bibcode
  `1993Sci...261..742C`). *Ices on the Surface of Triton* — N₂/CH₄/CO₂/H₂O/CO ices on
  a bright high-albedo surface. §4, §7. (256 cites.)

- **Cruikshank, D. P. et al. (1998)** — *Icarus* 135, 389. **No arXiv** (bibcode
  `1998Icar..135..389C`). *The Composition of Centaur 5145 Pholus* — the tholin/organic
  reddening archetype (reddest known solar-system surface). §4, §7. (239 cites.)

- **Grundy, W. M. et al. (2016)** — *Science* 351, aad9189. **arXiv:1604.05368.**
  *Surface compositions across Pluto and Charon* (New Horizons) — maps the N₂/CH₄/CO/
  H₂O ices vs the dark-red tholin terrains. §7. (211 cites.)

- **Buratti, B. J. et al. (2017)** — *Icarus* 287, 207. **arXiv:1604.06129.** Global
  albedos of Pluto and Charon from New Horizons LORRI — the resolved geometric/Bond
  albedo maps for the Pluto example. §6, §7. (77 cites.)

- **de Pater, I. & Lissauer, J. J.** — *Planetary Sciences*, Cambridge Univ. Press
  (2001 1st / 2010 2nd / 2015 3rd ed.). **Book, no arXiv** (bibcode
  `2010plsc.book.....D`). Standard text for the geometric-albedo, phase-integral and
  Bond-albedo definitions and the `A = q·p` relation. §6. (63/33 cites by ed.)

- **Polyanskiy, M. N. (2024)** — *Scientific Data* 11, 94. **No arXiv** (bibcode
  `2024NatSD..11...94P`). The **refractiveindex.info** database — the optical-constant
  portal; **here the solid/liquid-phase entries** (minerals, water/N₂/CH₄/CO₂ ices,
  tholins) for the Hapke `n+ik` step (§3), vs the gas-phase entries used by the
  atmosphere doc. Cite each dataset's own primary source per row. (335 cites.)

- **RELAB Spectral Library Bundle** — PDS Geosciences Node / Brown University (bibcode
  `2020pds..data...98M`, DOI 10.17189/1519032). **Database, no journal-paper
  descriptor.** Complementary planetary-analog reflectance library (meteorites, lunar/
  asteroid analogs, ices). §3. (23 cites on the PDS bundle record.)

- **CIE 1931 / IEC 61966-2-1 (sRGB)** — engineering standards (not ADS works); the
  colorimetry kernel is **not restated here** — see `atmosphere-reflected-color-
  methodology.md` §8. §5.

**No clean canonical ADS paper for**: (a) the spectrum→sRGB colorimetry math (CIE/IEC
standard, owned by the atmosphere doc §6); (b) a single definitive journal paper for
"Bond albedo / phase integral" — it is textbook material (de Pater & Lissauer above),
with historical roots in Russell's and Bond's photometry rather than one citable modern
paper. (c) RELAB has no peer-reviewed descriptor paper of record; cite the PDS bundle.

---

## Related

- `docs/reference/atmosphere-reflected-color-methodology.md` — the **sibling** that
  owns the **colorimetry engine** (§6: spectrum → XYZ → sRGB with the host-star SED)
  reused here, and the **refractiveindex.info portal** (Polyanskiy 2024; gas-phase
  there, solid/liquid-phase here). The atmosphere's reflected color sits **on top of**
  the surface color this doc derives; for thick decks the surface is hidden.
- `docs/reference/tidally-locked-temperature-methodology.md` — **consumes the Bond
  albedo `A`** from §6 in `T_eq = [S(1−A)/4σ]^¼`. A surface choice propagates into
  temperature through `(1−A)^¼`.
- `docs/reference/tidal-heating-methodology.md` — the other side of a body's energy
  budget (internal heating), which together with the absorbed-stellar term (this `A`)
  sets the surface temperature.
- `docs/reference/planetary-dynamo-scaling.md` — the gold-standard sibling for citation
  rigor and domain-of-validity honesty (no-arXiv flagging, regime caveats).
- **Emission color** (reentry plasma, airglow, aurora, lava thermal glow) lives in the
  `firefly-cfg` skill and `composition-color.md` — a different mechanism (emission, not
  reflection). Don't confuse it with the reflected surface color here.
- Phase 3 synthesis skill (`nearstars-phase3`) — where the chosen surface color, the
  assumed surface state, and the Bond albedo are recorded per body before they feed the
  cfg writer (Kopernicus surface color / Scatterer) and the temperature calc downstream.
