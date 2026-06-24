<!-- 항성 Teff(+금속함량, M왜성 TiO/VO 분자밴드)에서 광구 가시색(sRGB)을 도출하는 방법론 레퍼런스 -->
# Stellar Photospheric-Color Methodology — Teff (+ [Fe/H], M-dwarf molecular bands) → sRGB

> Source: synthesis of the stellar effective-temperature / synthetic-photometry
> literature (Bessell+ 1998, Husser+ 2013 PHOENIX, Castelli & Kurucz 2003 ATLAS9,
> Allard+ 2011 BT-Settl, Rajpurohit+ 2013, Mann+ 2015, Ramírez & Meléndez 2005,
> Casagrande+ 2010, Worthey & Lee 2011, Pecaut & Mamajek 2013) plus the engineering
> colorimetry standards (CIE 1931 color-matching functions; IEC 61966-2-1 sRGB).
> Citations resolved against NASA ADS (the registered ADS_API_TOKEN), not ad-hoc
> web search; arXiv id where one exists, otherwise the authoritative ADS bibcode.
> Purpose: a reusable, grounded recipe for the **visible incandescent color of a
> star's photosphere** — the `visual_surface_tint_hex` assigned to every NearStars
> star — from its effective temperature, with the small metallicity correction and
> (the load-bearing part) the molecular-band breakdown of the blackbody for M dwarfs.
> This is a working reference, not a textbook — see §8 for the verified citations.

**Scope — what this doc is NOT, and what it supersedes.** This is the star's own
**emitted (incandescent) photospheric color** — light the star *makes*, set by its
temperature and emergent SED. It is **not**:

- **Reflected / scattered planetary color** (sky, cloud-deck, disk-integrated hue) —
  that is `atmosphere-reflected-color-methodology.md` (atmosphere), the
  surface/disk reflectance docs. There the star is the *illuminant*; here the star
  *is the source*.
- **Emission-line / plasma color** (reentry glow, airglow, aurora, stellar
  chromospheric lines) — that is line/band emission from discrete excited species
  and lives in `firefly-cfg` / `element-plasma-colors.md`. A star's *continuum*
  photospheric color is a different mechanism: thermal continuum shaped by opacity.

It **supersedes** the heuristic stellar-tint guidance scattered in
`color-materials.md` (the "incandescence is set by temperature" line and the
"cool stars are red" intuition). `color-materials.md` stays as the general
material-color justification tool for **planetary** surfaces/atmospheres; this doc
is the grounded method for the **stellar** tint specifically.

## Table of Contents

1. [Why the Stellar Tint Is a Derived Value, Not a Measurement](#1-why-the-stellar-tint-is-a-derived-value-not-a-measurement)
2. [The Teff → Color Baseline (Blackbody)](#2-the-teff--color-baseline-blackbody)
3. [Synthetic Photometry — the Proper Way (Model Atmosphere → CIE)](#3-synthetic-photometry--the-proper-way-model-atmosphere--cie)
4. [The Metallicity Correction — Line Blanketing](#4-the-metallicity-correction--line-blanketing)
5. [M Dwarfs Break the Blackbody — TiO/VO Molecular Bands](#5-m-dwarfs-break-the-blackbody--tiovo-molecular-bands)
6. [Domain of Validity — Three Regimes](#6-domain-of-validity--three-regimes)
7. [The Colorimetry Engine](#7-the-colorimetry-engine)
8. [Worked Examples](#8-worked-examples)
9. [Honesty — What These Hexes Are](#9-honesty--what-these-hexes-are)
10. [Annotated Bibliography](#10-annotated-bibliography)
11. [Related](#related)

---

## 1. Why the Stellar Tint Is a Derived Value, Not a Measurement

We do not measure a NearStars star's color as a hex. What we have (Phase 2) is a
**curated effective temperature** `Teff`, a surface gravity `log g`, and usually a
metallicity `[Fe/H]`. The displayed photospheric tint is *derived* from those, the
same "physics sets the band, a documented choice picks the value" posture as the
sibling color docs. The chain is one-directional and short:

```
Teff (+ log g, [Fe/H])  ─►  emergent SED  S(λ)  ─►  CIE 1931 XYZ  ─►  sRGB  ─►  hex
```

The only modelling decision is **how good an approximation `S(λ)` needs to be**, and
that is set entirely by the spectral regime (§6). For most NearStars hosts (FGK,
the white dwarf) a Planck blackbody at `Teff` is good enough; for the M-dwarf ladder
it is **not**, and that is the whole point of this doc.

---

## 2. The Teff → Color Baseline (Blackbody)

A star's color is set, to first order, by its effective temperature. The photosphere
radiates an approximately thermal continuum, so the zeroth-order SED is the Planck
function

```
B_λ(Teff) = (2 h c² / λ⁵) · 1 / (exp(h c / λ k Teff) − 1)
```

Running `B_λ(Teff)` through the colorimetry engine (§7) traces the **Planckian locus**
in chromaticity space — the familiar "color temperature" curve: hot stars sit blue,
the Sun near white, cool stars orange-red. This is exactly the CIE color-temperature
relation used in lighting engineering, and for a **smooth-continuum** photosphere it
is a genuinely good approximation, because the real SED *is* close to a reddened
blackbody once line opacity is mild.

Two properties of the blackbody approximation matter:

- **Monotonic and smooth.** Color is a single-valued function of `Teff` along the
  locus — there are no surprises in the FGK/WD range. This is why the FGK tints below
  differ only subtly and why they are all near-white with a faint warm cast.
- **It only knows temperature.** A blackbody has no metals and no molecules, so it
  carries *neither* the metallicity nudge (§4) *nor* the M-dwarf molecular
  suppression (§5). Those are precisely the two corrections that the blackbody omits,
  and the regime (§6) decides whether omitting them is acceptable.

For grounding "where does a given Teff sit on the locus" against real stars rather
than pure Planck theory, the empirical **Teff↔color tables of Pecaut & Mamajek 2013**
(dwarf sequence O→M) and the **Worthey & Lee 2011** color-temperature calibration are
the reference anchors — they confirm the blackbody locus is a fair description for
FGK and quantify where it starts to fail toward late types.

---

## 3. Synthetic Photometry — the Proper Way (Model Atmosphere → CIE)

The blackbody is an approximation; the *correct* way to get a real stellar color is
**synthetic photometry**: take a model-atmosphere SED computed at the star's
`(Teff, log g, [Fe/H])`, and integrate it against the CIE color-matching functions
(§7) instead of integrating a Planck function. The model SED carries the real line
and molecular opacity that the blackbody lacks, so it reproduces both the
metallicity nudge and the molecular-band carving for free.

The canonical model-atmosphere libraries, in order of where each is the right tool:

- **Castelli & Kurucz 2003 (ATLAS9)** — LTE plane-parallel grids for **FGK and
  hotter**. The workhorse for solar-type and earlier stars; the metallicity
  line-blanketing of §4 is built in.
- **Husser+ 2013 (PHOENIX)** — a large, high-resolution synthetic-spectrum library
  spanning FGKM. The modern default for going from `(Teff, log g, [Fe/H])` to a real
  optical SED, and it resolves the molecular bands that matter for M dwarfs.
- **Allard+ 2011 (BT-Settl)** — the reference grid for **cool dwarfs, brown dwarfs,
  and giant planets**, with the molecular line lists (TiO, VO, H₂O, …) and the dust/
  cloud treatment that the M/L/T sequence requires. This is the grid that makes §5
  quantitative.

The classic precedent that ties model atmospheres to **broadband colors and
temperature calibrations** across the whole O→M range is **Bessell, Castelli & Plez
1998** — the standard reference for "model atmosphere → synthetic color." NearStars
does not currently run a live PHOENIX/BT-Settl→CIE integration; the M-dwarf ladder
(§5) is a *calibrated estimate* of what such an integration yields (see §9). When an
exact value is needed, the proper route is a real BT-Settl/PHOENIX SED through §7.

---

## 4. The Metallicity Correction — Line Blanketing

At **fixed Teff**, metals change the color through **line blanketing**: the dense
forest of metal absorption lines (overwhelmingly Fe, plus the other iron-peak
elements) is concentrated in the **blue/UV**, where it removes flux and
back-warms the redistributed flux toward longer wavelengths. The direction:

> **Metal-rich → redder; metal-poor → bluer**, at the same Teff.

The magnitude is **small** for mild metallicities — sub-perceptual for |[Fe/H]| ≲ 0.5
once converted to a displayed hex, which is why for FGK stars it is a *nudge* on top
of the blackbody, not a regime change. The canonical quantitative grounding is the
Teff–color–[Fe/H] calibration family:

- **Ramírez & Meléndez 2005 (II)** — the explicit `Teff : color : [Fe/H]` calibration
  for FGK stars; the reference for "how many Kelvin / how much color does a dex of
  [Fe/H] move." 
- **Casagrande+ 2010** — the absolutely-calibrated infrared-flux-method Teff scale for
  dwarfs and subgiants, the modern anchor for the FGK Teff–color zero point.
- **Worthey & Lee 2011** — a broadband color-temperature calibration carrying the
  metallicity term across UBVRIJHK.

Practical rule for NearStars FGK hosts: take the blackbody color at `Teff`, then apply
a **small** warm (metal-rich) or cool/blue (metal-poor) shift per the sign above, and
**record it as a sub-perceptual nudge** — never as a value that survives rounding to a
visibly different hex. (Consistent with the project's "skip metallicity curation as
low-impact" stance: the term is real but rarely changes the displayed tint.)

---

## 5. M Dwarfs Break the Blackbody — TiO/VO Molecular Bands

This is the load-bearing correction. Below `Teff ≈ 4000 K` the photosphere is cool
enough for **molecules to form**, and their broad absorption bands carve large chunks
out of the **optical** — far more than the smooth blackbody continuum suggests:

- **TiO** (titanium oxide) — the defining absorber of M dwarfs. Strong band systems
  blanket the **green and blue-green** (and the red), and TiO band strength deepening
  with later subtype *is* the M spectral-classification sequence (Kirkpatrick-type
  TiO/VO band ratios).
- **VO** (vanadium oxide) — strengthens in the **late M / early L** range, adding
  more red/near-IR absorption on top of TiO.
- **H₂O** — water bands remove flux in the red and (dominantly) the near-IR.

Net effect on the visible color: a real M dwarf is **much redder AND much darker** in
the optical than its blackbody Teff implies, because the molecular bands preferentially
**eat the short-wavelength (green/blue) flux** the eye is most sensitive to. This is a
**large, NOT sub-perceptual** effect — it changes the hue family, not just a nudge —
and it **cannot** be captured by a blackbody. It requires a molecular-line model
atmosphere (BT-Settl / PHOENIX, §3). The Teff scale these grids produce for M dwarfs
is the **Rajpurohit+ 2013** (BT-Settl M-dwarf Teff scale) and **Mann+ 2015** (the
empirical M-dwarf Teff/radius/luminosity calibration, which uses BT-Settl
synthetic spectra) references.

### The NearStars M-dwarf color ladder

Presented as the **worked output** of "blackbody at Teff, then TiO/VO/H₂O suppression
of the blue/green," it is **monotonic**: later M subtype / cooler Teff → more molecular
absorption → deeper, darker red.

| Star | Type | Teff (K) | tint hex | reading |
|---|---|---|---|---|
| AU Mic | M1 | 3665 | `#e0743a` | warm orange — early M, modest TiO |
| Barnard | M4 | 3195 | `#cf5a30` | deeper orange-red — strong TiO |
| Proxima | M5.5 | 2904 | `#c54c2a` | brick red — TiO + VO |
| Teegarden | M7 | ~2900 | `#c23a1c` | darkest red — heavy TiO/VO/H₂O |

**The rule behind the ladder:** start from the blackbody at `Teff` (which alone would
give an over-bright, *too-orange* color), then push the hue **redder and the value
darker** in proportion to the molecular band strength, which grows with later M
subtype. The ladder is the project's calibrated stand-in for a per-star BT-Settl→CIE
integration (§9).

---

## 6. Domain of Validity — Three Regimes

The body's spectral type decides which method is valid. Be explicit: the blackbody is
the project's **working approximation for FGK + white dwarfs**, and the M-dwarf ladder
is the **molecular-band-corrected output** that replaces it for cool dwarfs.

1. **FGK dwarfs + white dwarfs → blackbody Teff is a good approximation.**
   Smooth-continuum photospheres; color ≈ Planckian locus at `Teff`. Apply the small
   metallicity nudge (§4) for FGK. White dwarfs are *especially* clean: a hot DA has a
   pure-H atmosphere with no metals and no molecules, so the blackbody is excellent and
   there is **no metallicity term at all**. (NearStars: Sun, α Cen A, τ Ceti, 40 Eri A;
   40 Eri B = DA white dwarf.)
2. **M dwarfs → the blackbody FAILS; use a model atmosphere.** TiO/VO/H₂O bands make
   the star much redder and darker than `Teff` blackbody implies (§5). This is a hue-
   family change, not a nudge. Use BT-Settl/PHOENIX, or the calibrated ladder above.
   (NearStars: AU Mic, Barnard, Proxima, Teegarden, 40 Eri C; the M-dwarf field stars.)
3. **Special cases → model atmospheres also required, flag explicitly.**
   - **Carbon stars** — C/O > 1 swaps TiO for C₂/CN bands, reddening the star and
     adding a distinct character a blackbody cannot reproduce.
   - **Very hot O/B stars** — the optical sits far out on the Rayleigh-Jeans tail; the
     blackbody hue (blue-white) is roughly right, but strong UV line blanketing and
     non-LTE effects mean a proper color needs a hot model atmosphere. The *displayed*
     tint is robustly blue-white regardless.
   - **Strong-lined / chemically peculiar stars** (Ap/Bp, strong-CN giants, etc.) —
     heavy line blanketing shifts the color away from the blackbody; not blackbody-
     valid. None are in the current NearStars roster, but flag if added.

---

## 7. The Colorimetry Engine

The spectrum → sRGB conversion (integrate the SED against the CIE 1931 2°
color-matching functions → XYZ → IEC 61966-2-1 linear-sRGB matrix → sRGB gamma) is
**owned by `atmosphere-reflected-color-methodology.md` §6** and is **not restated
here** — including the 3×3 XYZ→linear-sRGB matrix and the gamma transfer function.
Use that engine. There is **no canonical ADS paper for the colorimetry math itself**;
it is the CIE/IEC engineering standard, cited as such.

The one physics difference for this doc — the star is its **own illuminant**:

- In the reflected-color doc, the input is a *reflected* spectrum `R(λ) = S(λ)·A(λ)`
  (host SED × albedo) and the normalization uses the host star as illuminant.
- **Here the input is the STAR'S OWN emergent SED** — a Planck `B_λ(Teff)` for FGK/WD
  (the working approximation), or a model-atmosphere spectrum for M dwarfs. There is
  **no external illuminant and no albedo**: the star *is* the light source, so we
  integrate `S(λ)` directly. The normalization `k` is then just a brightness scaling
  (the chromaticity — the *color* — is normalization-independent); pick `k` so the
  result is a representative value rather than crushed or clipped.

**Saturation / normalization caveat (important).** Physically-normalized true star
colors are **very pale** — near-white with only a faint tint, because the eye's
adaptation and the broad thermal continuum both wash out saturation. The Sun is
*white*, not yellow; even an M dwarf, normalized honestly, is a desaturated orange,
not a vivid red. Catalogs and renderers (and the NearStars viewer) commonly
**saturate** these colors for side-by-side distinguishability — that is a deliberate
**render choice**, separate from the physical chromaticity this doc derives. The hexes
here lean toward the *render* convention (perceptibly tinted) so the M-dwarf ladder is
legible; the underlying chromaticity is paler. State which convention a given value is
in when it matters.

---

## 8. Worked Examples

Each states regime → method → color.

**The Sun (G2V, 5772 K) → `#fff1ea`.** FGK blackbody regime (§2). The Planckian locus
at 5772 K is essentially the white point; the tiny offset from pure white is the faint
warm cast of a sun-temperature blackbody. Honestly normalized, the Sun is **near-white
with a barely-warm tint** — the popular "yellow Sun" is a render/atmosphere artifact,
not the photospheric color.

**α Cen A (G2V, ~5790 K, metal-rich [Fe/H] ≈ +0.2) and τ Ceti (G8.5V, 5370 K,
[Fe/H] ≈ −0.52) → `#ffecdd` physical.** Both FGK blackbody + metallicity (§2, §4).
α Cen A is a near-solar-twin temperature but **metal-rich**, so the line-blanketing
nudge pushes it very slightly **redder/warmer** than the Sun — sub-perceptual. τ Ceti
is cooler (warmer-toned base color) **and metal-poor**, so the metallicity term nudges
it slightly **bluer**, partly offsetting its cooler Teff; the residual displayed tint
is a warm cream `#ffecdd` with a sub-perceptual blue metallicity correction. Both
nudges are recorded but neither changes the hue family.

**40 Eridani A (K0.5V, 5143 K) → `#ffe9d5`.** FGK blackbody regime, cooler than the
Sun → a **warm orange-cream**. Still a smooth-continuum photosphere, so the blackbody
locus at 5143 K is the right tool; the metallicity term is a minor nudge.

**40 Eridani B (DA white dwarf, 17,200 K) → `#b0c5ff`.** Hot blackbody-valid regime
(§6.1). A hot pure-hydrogen DA atmosphere: **no metals, no molecules → no metallicity
term**, and the blackbody is an excellent approximation. At 17,200 K the locus sits
firmly **blue-white**. The cleanest blackbody case in the roster.

**The M-dwarf ladder (AU Mic / Barnard / Proxima / Teegarden, §5).** M-dwarf regime
(§6.2): the blackbody fails. Computed as "blackbody Teff + TiO/VO/H₂O suppression of
the blue/green," giving the monotonic deepening-red ladder `#e0743a → #cf5a30 →
#c54c2a → #c23a1c`.

**40 Eridani C (M4.5Ve, 3167 K) → `#cf5a30` — the diagnostic example.** 40 Eri C sits
at essentially **Barnard's temperature** (3167 K vs 3195 K). This is the clean test of
the whole method:

- **Blackbody at 3167 K → ~`#ffbe78`** — a bright, *too-orange* color. This is
  **WRONG**: it ignores that at this temperature TiO and VO have carved most of the
  green/blue out of the optical.
- **TiO/VO-corrected (the ladder) → ~`#cf5a30`** — the same deep orange-red as Barnard,
  which is **right**, because two stars at the same Teff and same (M4–M4.5) molecular
  band strength must land at the same color.

40 Eri C is therefore the worked proof that the blackbody is the wrong tool for M
dwarfs and the molecular-band-corrected ladder is the right one — and a built-in
**consistency check**: equal Teff + equal subtype ⇒ equal color (Barnard ≈ 40 Eri C).

---

## 9. Honesty — What These Hexes Are

- **The per-star hexes are tie-breaks, not measurements.** No NearStars star has a
  measured visible-color hex. The exact value depends on (a) which **model grid**
  (BT-Settl vs PHOENIX vs blackbody) and (b) the **saturation/normalization render
  choice** (§7). Two defensible pipelines can differ by a perceptible amount,
  especially for M dwarfs. Treat each hex as **medium/low confidence**.
- **The metallicity nudge is sub-perceptual** for the NearStars roster (|[Fe/H]| ≲ 0.5).
  It is recorded for correctness and direction, but it does not, by itself, move a
  star to a visibly different hex. (Hence the project's "skip metallicity curation"
  stance is harmless for the *tint*.)
- **An exact M-dwarf color needs a real BT-Settl/PHOENIX→CIE integration.** The ladder
  in §5 is the project's **calibrated estimate** of that integration, not the
  integration itself — monotonic, physically-signed (redder/darker with later type),
  and internally consistent (Barnard ≈ 40 Eri C), but a *grounded approximation*. If a
  value ever needs to be defended beyond "tie-break," run the model SED through §7.
- **The blackbody is explicitly an approximation for FGK/WD** — adopted because it is
  good there (smooth continuum) and because the displayed tints are near-white anyway,
  so the residual error is sub-perceptual. It is **not** adopted for M dwarfs.

---

## 10. Annotated Bibliography

Each entry: authors, year, journal, **verified** arXiv id (or a flag where none
exists, with the ADS bibcode), and one line on what it contributes. Citation counts
(ADS, at survey time) given for spot-checking.

- **Bessell, M. S., Castelli, F. & Plez, B. (1998)** — *A&A* 333, 231. **No arXiv**
  (bibcode `1998A&A...333..231B`). *Model atmospheres broad-band colors, bolometric
  corrections and temperature calibrations for O–M stars* — the standard precedent for
  turning a model-atmosphere SED into synthetic broadband colors and a Teff scale
  across the full O→M range. §2, §3. (1356 cites.)

- **Husser, T.-O. et al. (2013)** — *A&A* 553, A6. **arXiv:1303.5632.** *A new
  extensive library of PHOENIX stellar atmospheres and synthetic spectra* — the modern
  high-resolution synthetic-spectrum library spanning FGKM; the default `(Teff, log g,
  [Fe/H])` → real optical SED for synthetic photometry. §3. (1801 cites.)

- **Castelli, F. & Kurucz, R. L. (2003)** — IAU Symp. 210, A20. **arXiv:astro-ph/
  0405087** (bibcode `2003IAUS..210P.A20C`). *New Grids of ATLAS9 Model Atmospheres* —
  the LTE plane-parallel grids (with metal line blanketing) for FGK and hotter stars,
  the workhorse for solar-type colors. §3, §4. (1177 cites.)

- **Allard, F., Homeier, D. & Freytag, B. (2011)** — ASP Conf. 448, 91.
  **arXiv:1011.5405** (bibcode `2011ASPC..448...91A`). *Model Atmospheres From Very Low
  Mass Stars to Brown Dwarfs* (BT-Settl) — the reference cool-dwarf/BD grid with the
  TiO/VO/H₂O molecular line lists and dust treatment that make the M-dwarf color
  correction quantitative. §3, §5. (481 cites.)

- **Rajpurohit, A. S. et al. (2013)** — *A&A* 556, A15. **arXiv:1304.4072.** *The
  effective temperature scale of M dwarfs* — BT-Settl fits to M-dwarf optical spectra;
  the Teff scale and the demonstration that TiO/VO bands govern M-dwarf optical SEDs.
  §5. (222 cites.)

- **Mann, A. W. et al. (2015)** — *ApJ* 804, 64. **arXiv:1501.01635** (cached in
  `docs/phase3/_papers/1501.01635.md`). *How to Constrain Your M Dwarf: Measuring
  Effective Temperature, Bolometric Luminosity, Mass, and Radius* — the empirical
  M-dwarf Teff/radius/luminosity calibration (using BT-Settl synthetic spectra); the
  practical anchor for M-dwarf Teff used in the ladder. §5. (659 cites.)

- **Ramírez, I. & Meléndez, J. (2005)** — *ApJ* 626, 465. **arXiv:astro-ph/0503110.**
  *The Effective Temperature Scale of FGK Stars. II. Teff:Color:[Fe/H] Calibrations* —
  the explicit Teff–color–[Fe/H] calibration; the quantitative grounding for the
  metallicity-color nudge (sign and magnitude). §4. (496 cites.)

- **Casagrande, L. et al. (2010)** — *A&A* 512, A54. **arXiv:1001.3142.** *An
  absolutely calibrated Teff scale from the infrared flux method. Dwarfs and
  subgiants* — the modern absolutely-calibrated FGK Teff–color zero point. §4.
  (655 cites.)

- **Worthey, G. & Lee, H.-C. (2011)** — *ApJS* 193, 1. **arXiv:astro-ph/0604590.** *An
  Empirical UBVRIJHK Color-Temperature Calibration for Stars* — broadband color-
  temperature calibration carrying the metallicity term; anchors where the blackbody
  locus is fair and where it deviates. §2, §4. (224 cites.)

- **Pecaut, M. J. & Mamajek, E. E. (2013)** — *ApJS* 208, 9. **arXiv:1307.2657.**
  *Intrinsic Colors, Temperatures, and Bolometric Corrections of Pre-main-sequence
  Stars* — the widely-used empirical dwarf Teff↔color↔spectral-type sequence (O→M);
  the table that grounds "what color is a star of this Teff." §2. (2310 cites.)

- **CIE 1931 2° standard observer color-matching functions** — engineering standard
  (CIE 15; not an ADS work). The integration kernels of §7 (owned by the reflected-
  color doc).

- **IEC 61966-2-1:1999 (sRGB)** — engineering standard (not an ADS work). The XYZ→
  linear-sRGB matrix and sRGB gamma of §7 (owned by the reflected-color doc).

**No canonical ADS paper for**: the spectrum→sRGB colorimetry math itself (CIE/IEC
standard, owned by `atmosphere-reflected-color-methodology.md` §6). Every astrophysics
topic here (Teff scales, model atmospheres, metallicity-color, M-dwarf molecular
bands) has a clear high-citation canonical work, listed above.

---

## Related

- `atmosphere-reflected-color-methodology.md` — **owns the CIE 1931 → XYZ → sRGB
  colorimetry engine** (its §6, including the matrix and gamma). This doc references
  that engine; the only difference is the input SED is the star's own emission, not a
  reflected spectrum, and the star is its own illuminant (no external white point).
- `color-materials.md` — the heuristic stellar-tint guidance this doc **grounds and
  supersedes** (for the stellar incandescent tint specifically); it remains the
  general justification tool for *planetary* surface/atmosphere material color.
- `internal-heat-luminosity-methodology.md` — the sibling recipe for Teff/luminosity
  of planets and brown dwarfs; the Teff that feeds *this* color method comes from the
  same Phase 2 curation discipline.
- `planetary-dynamo-scaling.md` — the gold-standard "relation + regimes + worked
  examples + citation-flagged bibliography" rigor model this doc follows.
- **Emission / plasma color** (stellar chromospheric lines, reentry glow, airglow,
  aurora) lives in the `firefly-cfg` skill and `element-plasma-colors.md` — line/band
  *emission* from discrete species, a different mechanism from the thermal-continuum
  photospheric color derived here.
