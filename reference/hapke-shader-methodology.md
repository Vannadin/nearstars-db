<!-- Sol의 Hapke 셰이더 값(_Hapke 지형/스케일드)을 앵커 보간 + 광도 문헌으로 처방하는 방법 -->
# Hapke shader value grounding: Sol anchor families + photometric regimes

Method reference for assigning the two **`_Hapke` shader values** every NearStars
body needs for the Sol (RSS-Reborn) rendering stack: the **Parallax terrain**
material's `_Hapke` (ground-level look) and the **`Custom/HapkeScaled`** scaled-space
material's `_Hapke` (orbit/map-view disk look). These are engine look-knobs named
after the Hapke reflectance framework, so the recipe has two layers: an **empirical
anchor table** read from Sol-Configs itself (the canonical cfg source), and a
**photometric literature layer** that grounds *why* the anchors cluster the way they
do and how to place a new body between them.

**What `_Hapke` actually is (source-confirmed).** The terrain shader is open
source (Gameslinx/Parallax-Continued,
`Assets/Shaders/Includes/ParallaxGlobalFunctions.cginc`): the scalar is simply a
**diffuse-cosine exponent**, `NdotL = pow(NdotL, _Hapke)`. Below 1 the lighting
stays flat and bright up to the terminator (the icy look), 1.0 is pure Lambert,
above 1 the falloff steepens into dramatic shading. The *real* Hapke BRDF lives in
the scaled shader's per-pixel parameter maps and global scalars (next section);
that shader ships compiled, so its channel semantics below are characterized
forensically from the shipped textures, not read from HLSL.

## The canonical source (non-ADS exception, pinned)

Anchor values are read from **RSS-Reborn/Sol-Configs**, commit
[`f9e6fdf`](https://github.com/RSS-Reborn/Sol-Configs/tree/f9e6fdf4e26c4a5ba1364ba93babfa2ada3e5a5c)
(`*-ParallaxTerrain.cfg`, 44 real-scale bodies; the `Quarter_`/`Stock_` variants are
rescale shells with no own values). This is a curated authoritative database in the
sense of the ADS-discipline fallback: verified by direct file read at the pinned
commit, not by web summary.

## The anchor table (Sol-Configs, condensed to families)

| Family | Bodies (examples) | terrain `_Hapke` | scaled `_Hapke` |
|---|---|---|---|
| Mature lunar regolith | Luna, Mimas, (Earth land) | **1.0** | **2.2** |
| Dark rocky regolith | Mercury, Ceres, Vesta, Phoebe, Styx/Nix/Hydra/Kerberos | **0.88** | **2.2** |
| Ejecta-blanketed small moons | Phobos, Deimos | 0.88 | **1.6** |
| Icy / dark-grain surfaces | Ganymede, Callisto, icy moons, Pluto, Charon, Triton, asteroids (Ida, Eros, Psyche, Ryugu, Pallas) | **0.38–0.45** | **2.2** |
| Bright glazed ice / volcanic frost | Europa, Io | 0.44–0.45 | **2.0** |
| Haze-veiled solid (odd pair) | Titan, Proteus | 0.56 | 2.2 |
| Dusty thin-atmosphere terrestrial | Mars | **1.56** | **1.0** |
| Thick-atmosphere terrestrial | Earth, Venus | 1.0 / 1.15 | ~1.0–1.15 (Earth: ocean shader path) |
| Gas / ice giants | Jupiter, Saturn, Uranus, Neptune | (0.44 template) | **1.6** |

Reading of the two knobs (rendering regimes, not one physical constant):

- **scaled `_Hapke`** controls the full-disk phase behavior — how flat the disk stays
  toward the limb and how hard the brightness surges near full phase (the "lunar
  look"). Sol's convention is tight: **airless regolith/ice = 2.2**, bright glazed
  ice = 2.0, gas giants and compacted-ejecta moonlets = 1.6, atmospheres ≈ 1.0.
- **terrain `_Hapke`** is the diffuse-cosine exponent above: the icy family
  (0.38–0.45) keeps ground lighting flat to the terminator, 1.0 is Lambert
  (Luna), 1.56 gives Mars its contrasty falloff. Sol assigns it in **discrete
  family presets** ({0.38–0.45, 0.56, 0.88, 1.0, 1.15, 1.56}), i.e. by surface
  analog, then per-body look tuning inside the family.

## The physical layer: why the families order this way

The knob is named for the Hapke bidirectional-reflectance framework
(Hapke 1981, [`1981JGR....86.3039H`](https://ui.adsabs.harvard.edu/abs/1981JGR....86.3039H)),
whose phase behavior is driven by two opposition mechanisms plus the particle
phase function:

- **Shadow-hiding opposition effect (SHOE)** — pores and grain shadows vanish at
  zero phase; strongest in dark, porous, mature regolith
  (Hapke 1986, [`1986Icar...67..264H`](https://ui.adsabs.harvard.edu/abs/1986Icar...67..264H)).
  This is what makes the Moon's disk flat-bright to the limb: the resolved global
  Hapke-parameter maps are Sato et al. 2014
  ([`2014JGRE..119.1775S`](https://ui.adsabs.harvard.edu/abs/2014JGRE..119.1775S)),
  and Mercury's regolith photometry is Moon-like with a comparably strong surge
  (Warell 2004, [`2004Icar..167..271W`](https://ui.adsabs.harvard.edu/abs/2004Icar..167..271W)).
  → the airless-regolith scaled family (2.2).
- **Coherent-backscatter opposition effect (CBOE)** — a narrow interference spike
  that grows with albedo and multiple scattering
  (Hapke 2002, [`2002Icar..157..523H`](https://ui.adsabs.harvard.edu/abs/2002Icar..157..523H));
  the archetype measurement is Enceladus' surge (Verbiscer et al. 2005,
  [`2005Icar..173...66V`](https://ui.adsabs.harvard.edu/abs/2005Icar..173...66V)).
  Bright icy surfaces keep a strong (narrower) surge — Sol keeps them at 2.0–2.2 —
  while their ground-level response reads smoother than regolith (terrain 0.38–0.45).
- **Opposition amplitude vs albedo is non-monotonic** across asteroid classes
  (largest at moderate albedo, smaller at the dark and bright ends: Belskaya &
  Shevchenko 2000, [`2000Icar..147...94B`](https://ui.adsabs.harvard.edu/abs/2000Icar..147...94B)),
  which is why the terrain knob is a family preset, not a single albedo formula.
  Disk-resolved photometry of the mid-albedo icy satellites is anchored by
  Buratti & Veverka 1984
  ([`1984Icar...59..392B`](https://ui.adsabs.harvard.edu/abs/1984Icar...59..392B)).
- **An atmosphere washes the disk phase curve** toward smooth scattering (Mars at
  1.0 scaled; Earth/Venus off the airless path entirely) — the disk look is then
  clouds/haze, not ground photometry.

## What the scaled shader actually consumes (texture forensics)

The `Custom/HapkeScaled` material takes, besides the ordinary `_ColorMap` /
`_BumpMap` / `_HeightMap`, **two Hapke-specific parameter maps** plus per-body
global scalars (verified across all 50 real-scale Sol bodies; channel statistics
from a BC7 decode of the shipped Mercury 4k pack):

- **`_ScatteringTex`** and **`_SurgeTex`** are **512×256 equirect parameter maps**
  (1/8 the color-map resolution — the parameters vary at geologic-unit scale).
  They assign Hapke optical parameters per coordinate, heightmap-style; they are
  neither color nor normal data. Measured channel structure (Mercury):
  - Scatter: R ≈ single-scattering-albedo class (mean 0.40, +0.92 correlation
    with surface brightness), G ≈ phase-function asymmetry class (0.22, −0.82),
    B a third parameter (0.72); alpha unused.
  - Surge: R ≈ opposition-surge amplitude B₀ (mean 0.82, **−0.92** vs
    brightness — darker regolith surges harder, exactly the SHOE physics), G ≈
    surge width h (0.09, matching the literature's h_S ~0.05–0.1); B/A unused.
  - Channel-to-parameter naming is inferred from value statistics (the scaled
    shader is compiled); the ranges and correlations match the canonical Hapke
    parameter families.
- **`_porosityCoeffient`** — the Hapke porosity coefficient K, global per body:
  1.86 for nearly everything (lunar-like fill factor), with physical variations
  (Europa 1.2, Phobos 1.19, Deimos 1.34, Enceladus 1.73, Mars 2.02).
- **`_Theta`** — macroscopic roughness θ̄ in degrees: Moon/Mercury 18, smooth
  frost (Enceladus, Titan) 6, fractured icy moons 30–31.
- `_GammaBoost` / `_LightBoost` — pure look trims.

Art-pass consequence: a finished NearStars body eventually ships the two low-res
parameter maps (or flat defaults) plus K and θ̄, alongside the color/normal/height
set. The board records the scalars; the maps are emit-end texture work.

### Can K and θ̄ be derived rather than copied?

**K: yes — it is a closed-form function of packing.** Hapke 2008
([`2008Icar..195..918H`](https://ui.adsabs.harvard.edu/abs/2008Icar..195..918H),
series paper 6, *Effects of porosity*) gives the porosity coefficient explicitly in
terms of the filling factor φ of the optical (top-millimetre) layer:

    K = −ln(1 − 1.209 φ^(2/3)) / (1.209 φ^(2/3))

so the derivation chain is **surface type → φ → K**, one step, no analog copying.
Inverting Sol's own assignments confirms they sit on this curve at sensible
packings:

| Sol K | implied φ | porosity | reading |
|---|---|---|---|
| 2.02 (Mars) | 0.54 | 46 % | wind-compacted dust |
| 1.86 (default) | 0.49 | 51 % | lunar-like regolith (real lunar φ ≈ 0.4–0.5 ✓) |
| 1.73 (Enceladus) | 0.45 | 56 % | fresh frost |
| 1.34 / 1.20 / 1.19 (Deimos, Europa, Phobos) | 0.24 / 0.13 / 0.12 | 76–88 % | fairy-castle fluff |

Pick φ from the surface state we already derive (mature regolith 0.45–0.50,
fresh frost ~0.45, uncompacted fluff 0.1–0.25), then compute K. Note φ is the
**near-surface optical packing, not the body's bulk porosity** — bulk density
from mass and radius says nothing about it.

Tested and rejected: **K does not track surface gravity**. Across 16 Sol bodies
corr(K, log g) is only +0.58 and is carried by outliers (Europa at g = 1.31 gets
1.20 while Miranda at g = 0.08 gets 1.86). Sol assigns K by *surface type*, not
by compaction under weight; do the same.

**θ̄: no — it is a fitted parameter, not a predicted one.** The roughness
correction (Hapke 1984,
[`1984Icar...59...41H`](https://ui.adsabs.harvard.edu/abs/1984Icar...59...41H))
defines θ̄ as the mean slope angle of sub-resolution topography, and it is obtained
by *fitting* a measured phase curve or by measuring a high-resolution DEM — neither
exists for an exoplanet. So θ̄ stays anchored on the nearest Solar-System analog,
informed by the terrain character we do derive (crater-degradation methodology):
saturated cratered regolith ≈ 18°, smooth frost-mantled ≈ 6°, fractured/ridged ice
≈ 30°. Record it as an analog choice, never as a derivation.

## Practical recipe (per body class)

1. **Pick the scaled value by class** — this is the firm half:
   - airless rock or ice with regolith → **2.2**
   - bright glazed/frost-renewed ice (Europa/Io class) → **2.0**
   - compacted ejecta-blanket moonlet (Phobos class) → **1.6**
   - gas / ice giant → **1.6**
   - solid body with a real atmosphere → **1.0** (haze-veiled Titan is Sol's 2.2
     outlier; follow the art call, note it)
2. **Pick the terrain family by nearest surface analog**, then tune inside it:
   mature lunar-like regolith 1.0 · dark rocky regolith 0.88 · icy/dark-grain
   0.38–0.45 · dusty desert 1.56. Our space-weathering state (color methodology §4)
   moves a body *within* its family: fresher/shielded regolith sits above the dark
   mature preset (toward Luna 1.0), saturated-weathered terrain at or below it.
3. **Mean visual albedo rides the existing color methodology** — the appearance
   `albedo_mean` field is the area-weighted **geometric** (visual) albedo of the
   final palette; the Bond value for the energy budget stays on the surface row.
   Conversion and definitions: surface-color-albedo methodology §6.
4. **Compute K from φ** with the Hapke 2008 formula above (pick φ from the
   surface state: mature regolith 0.45–0.50, fresh frost ~0.45, uncompacted
   fluff 0.1–0.25), and **pick θ̄ by analog** (18° cratered regolith, ~6° smooth
   frost, ~30° fractured ice) — it is a fitted parameter with no predictor.
5. Record the values in the body's Phase 4 appearance row as typed fields
   (`hapke_terrain`, `hapke_scaled`, `hapke_porosity_k`, `hapke_theta`),
   refs = this doc. The Scatter/Surge parameter maps are deferred to the
   emit-end art pass.

### Validation: the recipe reproduces Sol's own assignments

Applying rules 1–2 blind to held-out Sol bodies: Vesta/Ceres (dark rocky regolith)
→ 0.88 / 2.2 ✓; the Uranian moons (icy dark grains) → 0.43 / 2.2 ✓; Phobos
(ejecta blanket) → 1.6 scaled ✓; Neptune (giant) → 1.6 ✓; Mars (dusty, thin
atmosphere) → 1.0 scaled ✓. The one Sol outlier the rules do not predict is
Titan's scaled 2.2 (rule 1 would say 1.0) — flagged above as an art call.

## Worked examples (NearStars)

| Body | Class read | terrain | scaled | Note |
|---|---|---|---|---|
| Proxima d | airless basaltic regolith, mid-latitudes magnetically shielded (fresher than Mercury), weathered polar caps | **0.95** | **2.2** | between Mercury 0.88 and Luna 1.0: less npFe⁰-mature than unshielded Mercury |
| Proxima c I | tholin-stained water-ice bedrock (Charon analog) | **0.43** | **2.2** | straight from the icy family; Charon itself is 0.43/2.2 in Sol |
| Proxima b | rocky world, 0.3 bar atmosphere, lakes + night ice | **1.0** | **1.0** | terrain lunar-family land; scaled on the atmosphere path |
| Proxima c | cold mini-Neptune | (n/a) | **1.6** | giant family; no terrain shader |

## Citations

- **Hapke, B. 1981**, JGR 86, 3039 ([`1981JGR....86.3039H`](https://ui.adsabs.harvard.edu/abs/1981JGR....86.3039H)).
  The bidirectional-reflectance framework the shader is named for. No arXiv (1981);
  bibcode-verified. Shared with the surface-color methodology.
- **Hapke, B. 1986**, Icarus 67, 264 ([`1986Icar...67..264H`](https://ui.adsabs.harvard.edu/abs/1986Icar...67..264H)).
  Shadow-hiding opposition effect (series paper 4). Bibcode-verified, no preprint.
- **Hapke, B. 2008**, Icarus 195, 918 ([`2008Icar..195..918H`](https://ui.adsabs.harvard.edu/abs/2008Icar..195..918H)).
  Porosity effects (series paper 6): the closed-form K(φ) this doc computes the
  porosity coefficient with. Bibcode-verified.
- **Hapke, B. 1984**, Icarus 59, 41 ([`1984Icar...59...41H`](https://ui.adsabs.harvard.edu/abs/1984Icar...59...41H)).
  Macroscopic-roughness correction (series paper 3): defines θ̄ as a *fitted* mean
  slope angle, which is why θ̄ is anchored, not derived. Bibcode-verified.
- **Hapke, B. 2002**, Icarus 157, 523 ([`2002Icar..157..523H`](https://ui.adsabs.harvard.edu/abs/2002Icar..157..523H)).
  Coherent-backscatter opposition effect (series paper 5). Bibcode-verified.
- **Sato, H. et al. 2014**, JGR Planets 119, 1775 ([`2014JGRE..119.1775S`](https://ui.adsabs.harvard.edu/abs/2014JGRE..119.1775S)).
  Resolved Hapke-parameter maps of the Moon (LROC WAC) — the lunar anchor.
- **Warell, J. 2004**, Icarus 167, 271 ([`2004Icar..167..271W`](https://ui.adsabs.harvard.edu/abs/2004Icar..167..271W)).
  Mercury regolith photometric parameters vs the Moon — the dark-regolith anchor.
- **Verbiscer, A. et al. 2005**, Icarus 173, 66 ([`2005Icar..173...66V`](https://ui.adsabs.harvard.edu/abs/2005Icar..173...66V)).
  Enceladus opposition surge (HST) — the bright-ice CBOE anchor.
- **Belskaya & Shevchenko 2000**, Icarus 147, 94 ([`2000Icar..147...94B`](https://ui.adsabs.harvard.edu/abs/2000Icar..147...94B)).
  Opposition-effect amplitude vs albedo across asteroid classes (non-monotonic).
- **Buratti & Veverka 1984**, Icarus 59, 392 ([`1984Icar...59..392B`](https://ui.adsabs.harvard.edu/abs/1984Icar...59..392B)).
  Voyager disk-resolved photometry of the Saturnian satellites.
- **RSS-Reborn/Sol-Configs @ f9e6fdf** — the engine-side canonical source (non-ADS
  exception; verified by direct file read at the pinned commit).

## Related

- [`surface-color-albedo-methodology.md`](surface-color-albedo-methodology.md) —
  palette, space-weathering state (§4) and the Bond/geometric albedo engine (§6)
  this recipe's terrain tuning and `albedo_mean` ride on.
- [`planet-pack-techniques.md`](planet-pack-techniques.md) — neighboring visual
  techniques mined from planet packs.
- [methodology-index](methodology-index.md) — the living index of derived-value recipes.
