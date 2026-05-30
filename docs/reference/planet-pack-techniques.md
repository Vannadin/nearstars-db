# Planet-Pack Visual Techniques — Reference Mining

> **Sources** (read-only analysis, 2026-05-30):
> - **SPVE** — SpacePotato's Volumetric Enhancements,
>   [`TheSpacePotato/...-Volumetric-Enhancements`](https://github.com/TheSpacePotato/SpacePotato-s-Volumetric-Enhancements)
>   @ `c33fefd8d7` (release 1.1, builds V3 + V5).
> - **Cosmic Serenity** —
>   [`ProximaCentauri-star/Cosmic-Serenity`](https://github.com/ProximaCentauri-star/Cosmic-Serenity)
>   @ `6f81ac01cf`.
> - **Promised Worlds** —
>   [`PromisedWorlds/PromisedWorlds`](https://github.com/PromisedWorlds/PromisedWorlds)
>   @ `b6484d1078`.
>
> **Purpose.** Mine reusable visual *techniques* and config *conventions*
> from three reference planet/visual packs, for use in NearStars'
> Kopernicus + Principia + Scatterer + EVE + Firefly + Parallax stack.
> **Techniques only — no config text or assets are copied into this repo.**
> See [§1 Licensing](#1-licensing--attribution) for why that distinction
> matters and what NearStars may/may not reuse.
>
> **Local-only companion.** Paid-Early-Access (blackrack release-5
> volumetric) schema specifics are NOT in this file; they live in
> `~/Desktop/ksp-mod-refs/_notes/` per [[feedback_patreon_assets]].

---

## TL;DR

> **Star rendering is the highest-value find.** The full Kopernicus
> `ScaledVersion` (sunspot/rim Material + Coronas), `Light` (4 intensity
> curves), photosphere-as-`Atmosphere`, and `HazardousBody` recipe is
> entirely free/publishable and can be *generated* from NearStars'
> curated Teff / L / R / mass instead of hand-tuned. See [§2](#2-star--stellar-object-rendering).

> **There are four debris-disk techniques**, not one. The best new one
> is PW's stock-Kopernicus **Asteroid spawner** (free, real spawnable
> belt). See [§3](#3-debris-disks--rings--four-techniques).

> **Licensing splits the three packs cleanly:** PW configs are
> CC-BY-NC-SA (compatible — adaptable with attribution); SPVE is
> CC-BY-NC (compatible, credit required); **Cosmic Serenity configs are
> GPLv3 (incompatible — learn the technique, never copy the text), and
> its textures/meshes are All-Rights-Reserved.** See [§1](#1-licensing--attribution).

---

## 1. Licensing & attribution

**The governing principle:** *techniques, methods, and ideas are not
copyrightable — only their concrete expression (config text, textures,
meshes, compiled code) is.* Everything in this document describes
**methods**, which NearStars may freely re-implement from understanding.
The constraints below apply only to **copying the actual files**.

### 1.1 Per-pack license

| Pack | Configs / "everything else" | Textures / meshes | Compatible with NearStars (CC-BY-NC-SA 4.0)? |
|------|------------------------------|-------------------|----------------------------------------------|
| **SPVE** | CC BY-NC 4.0 | CC BY-NC 4.0 | **Yes** — BY-NC content may enter a BY-NC-SA work; attribution required. |
| **Cosmic Serenity** | **GPL-3.0** | **All Rights Reserved** (ProximaCentauri) | **No (configs)** — GPL-3.0 ⇄ CC-BY-NC-SA are mutually incompatible for copied text. **No (assets)** — ARR. |
| **Promised Worlds** | CC-BY-NC-SA | CC-BY-NC-SA (some sub-licensed, see 1.3) | **Yes** — same license; adaptation allowed with attribution + ShareAlike. |

### 1.2 What NearStars may / may not do

- **All three:** read, learn, and **re-implement techniques** → always OK
  (ideas aren't copyrighted). This doc is that.
- **SPVE (CC BY-NC):** may adapt config text / reference snippets **with
  credit to SpacePotato**; non-commercial only (NearStars already is).
  Laythe cloud textures are by **StarCrusher96** — credit if ever used.
- **Promised Worlds (CC-BY-NC-SA):** may adapt config text **with
  attribution to Emu / "Constructalor" + Promised Worlds Contributors,
  under ShareAlike** (NearStars' own CC-BY-NC-SA satisfies this). Do **not**
  touch `PromisedWorlds.dll` (proprietary, see 1.3).
- **Cosmic Serenity:** **do not copy any config text** (GPL-3.0 would
  force NearStars configs to GPL — incompatible with CC-BY-NC-SA) and
  **do not use any texture/mesh** (All Rights Reserved). Re-implementing
  a technique you understood from reading CS is fine; pasting its cfg is not.
- **blackrack volumetric clouds:** the current paid release (V5) is
  Patreon Early-Access — never redistribute, and keep V5 schema facts
  local-only ([[feedback_patreon_assets]], [[reference_volumetric_clouds_naming]]).
  The free release-3 schema (`layerRaymarchedVolume`) is public.

### 1.3 Bundled third-party plugins (their own licenses)

These ship *inside* CS/PW but are separate projects. The MIT ones are
the realistic candidates for NearStars to actually **use/bundle** (keep
the MIT notice + add to `NOTICE`):

| Plugin | License | Author | Relevance |
|--------|---------|--------|-----------|
| **VertexHeightOblateAdvanced** (DuckweedUtils) | **MIT** | © 2024 James Glaze | ★ Oblate fast-rotator shapes — usable for real oblate stars/planets. |
| **VertexColorMapEmissive** (DuckweedUtils) | **MIT** | © 2024 Lt_Duckweed | Per-channel emissive terrain (Parallax-incompatible — scaled-space only). |
| **MitchellNetravali heightmap** (NiakoUtils) | **MIT** | © 2022 Niako | Smoother low-res heightmaps; drop-in for `VertexHeightMap`. |
| **ScaledDecorator** | **GPL-3.0** | (KSP forum) | Loads `.unity3d` prefabs into scaled space (comet tails / jets / disks). |
| **KopernicusExpansion Continued-er** | **GPL-3.0** | — | Wormholes etc. (out of NearStars scope). |
| **Sigma LoadingScreens** | ARR (cond. redistribution) | Sigma88 | Loading screens only. |
| **PromisedWorlds.dll** (settings menu) | **Proprietary, ARR** | © 2026 averageksp | Do not copy/modify/reverse-engineer. |

> **If NearStars ever bundles a plugin:** add it to `NOTICE` and
> `docs/reference/data-sources.md` with its license. MIT → include the
> copyright + permission notice. GPL-3.0 → ship as mere aggregation
> (separate plugin, not merged into NearStars' own licensed content).

---

## 2. Star & stellar-object rendering

The single most valuable area: NearStars ships **real stars** and already
curates Teff / L / R / mass, so every value these packs hand-tuned can be
**computed and generated**. All of this is free/publishable Kopernicus.

### 2.1 ScaledVersion Material (the visible star surface)

Under `ScaledVersion { type = Star … Material { … } }`:

- `sunspotTex` — greyscale photosphere granulation/spot map; `sunspotPower`
  (sharper at higher Teff — observed ~10 for a cool star vs ~40 for a
  hot one), `sunspotColor` (tint of the dark spots).
- `rimColor` / `rimPower` / `rimBlend` — limb glow. Hotter stars use a
  **tighter** rim (lower `rimPower`/higher `rimBlend`).
- `emitColor0` / `emitColor1` — intrinsic emission. For normal stars these
  can be near-black (lit externally); for **dim stars (brown/white dwarf)**
  set a faint colored emission so the body self-glows like an ember even
  when it casts almost no light.
- `noiseMap` — extra photosphere noise (exotic stars use it).

**NearStars rule:** drive every color (`sunspotColor`, `rimColor`,
`*SunlightColor`, `sunLensFlareColor`) from a **blackbody→sRGB conversion
of Teff** — reuse the existing disk-color/Mie synthesis. Keep `rimPower`
inversely related to Teff. Generate, don't copy magic numbers.

### 2.2 Coronas

`ScaledVersion { Coronas { <Value|Corona> { scaleSpeed, scaleLimitX/Y,
speed, rotation, updateInterval, Material { texture, invFade,
mainTexScale, mainTexOffset } } } }`. The child-node name (`Value` vs
`Corona`) is **not** load-bearing — both parse. `mainTexScale = 0,0`
effectively suppresses the corona (used for a dwarf with no bright halo).

### 2.3 Light block + intensity curves

`Body { … Light { … } }` fields and how they vary by type:

- Colors: `sunlightColor`, `scaledSunlightColor`, `IVASunColor`,
  `sunLensFlareColor`, `ambientLightColor` — the dominant per-type knob
  (warm/orange for M/K, white for G/F, blue-white for A, magenta/near-IR
  for L/brown dwarf, blue for a neutron star).
- `luminosity`, `insolation`, `sunAU` — **gameplay anchors**: set
  `insolation` so a planet at its real orbit receives ≈1.0; `sunAU` is the
  1-AU-equivalent reference distance (m) for thermal/solar-panel scaling.
- `sunFlare` — points at an AssetBundle (`…unity3d:flareName`). The packs
  ship **one shared flare** and recolor it per star via `sunLensFlareColor`
  rather than authoring N flares. Adopt this — single flare asset, tinted
  from Teff.
- `radiationFactor` — present on exotic high-radiation stars (pulsar 0.8).
- **Four curves** drive brightness vs camera distance:
  `IntensityCurve` (in-flight light), `ScaledIntensityCurve` (map/far),
  `IVAIntensityCurve` (cockpit, ≈0.9× of flight), `brightnessCurve`
  (lens-flare bloom). In the reference packs these are ~20-key analytic
  `1/r²`-style falloffs with exact derivative tangents — **clearly
  tool-generated, then pasted.**

> **NearStars action:** write one generator — given `luminosity` and a
> distance grid, emit all four curves. Near-field intensity scales with
> √L (observed: the brighter reference star's near value was ≈2.2× the
> dimmer one's, tracking its higher luminosity). Never hand-edit curves.

### 2.4 Photosphere as an `Atmosphere` envelope

Wrap the star body in a thin atmosphere to make the photosphere physical:
`enabled = true`, `oxygen = false`, `altitude ∝ stellar radius`,
`adiabaticIndex = 1.667` (monatomic), high `staticPressureASL` (~10–100,
a hard wall), and **`temperatureSeaLevel = Teff`**. The `temperatureCurve`
can rise again near the top to fake a **chromospheric temperature
inversion**. Generate the temperature/pressure curves from a simple
scale-height model.

### 2.5 HazardousBody — "you fry near the star"

`HazardousBody { Item { ambientTemp = <≈Teff or a death threshold>;
AltitudeCurve { … } } }` maps radial distance → fraction of `ambientTemp`,
keyed to part-destruction temperatures (the reference comments map keys to
"4000 K = all stock parts destroyed", "800 K = max EVA", etc.). Generate
the curve from stellar radius/luminosity so each star's lethal radius
scales correctly. Gives real close-approach danger without an atmosphere.

### 2.6 Exotic stars

- **Pulsar / neutron star** (composite of 4 layers on one body): true
  small `radius` (~12 km), short `rotationPeriod` (~2.4 s), near-black
  `Material` with blue tint, blue `Light` + `radiationFactor`, a
  **ScaledDecorator** twin-cone jet prefab (`rotatesWithParent`, axis
  tilted off spin), and the **Singularity** lensing shader layered on with
  `hideCelestialBody = False` so the star stays visible (see §7).
- **Brown / L-dwarf**: dim `luminosity` (~1–2), dark `ambientLightColor`,
  magenta/near-IR `emitColor0/1` (intrinsic ember glow), suppressed corona
  (`mainTexScale = 0,0`), steep `brightnessCurve` so the flare only blooms
  up close.
- **White dwarf** (synthesis, not seen directly): combine the brown-dwarf
  self-emission trick with a tiny radius + hot blue-white color, and
  optionally the Singularity-on-visible-body trick for faint lensing.

### 2.7 Appearance toggles

- **RealisticStarSize** — `@radius *= <factor>` gated on a settings flag;
  NearStars should compute the factor per star from real radius vs the
  oversized gameplay default (rather than one global constant).
- **TUFX dual-tuning** — material doubled with `:NEEDS[TUFX]` vs
  `:NEEDS[!TUFX]`: when TUFX bloom is present, *lower* `sunspotPower` /
  `rimBlend` / `rimPower` so the star doesn't blow out. Worth replicating
  only for dim stars where bloom dominates the read.
- **DistanceFactor** — `@semiMajorAxis *= <factor>` to compress/expand
  inter-system distance.

---

## 3. Debris disks & rings — four techniques

NearStars has real debris-disk hosts (Vega/Fomalhaut/ε Eri class). Four
distinct mechanisms exist across the packs; pick per case:

| # | Technique | Source | Thickness? | Cost / dependency | NearStars fit |
|---|-----------|--------|-----------|-------------------|---------------|
| 1 | **Raymarched EVE volume, annular band** | SPVE `rings.cfg` | **Yes** (3D, `min/maxAltitude` band) | EVE only; free V3 schema works | ★★★ Best config-only thick dusty disk. |
| 2 | **Stock Kopernicus Asteroid spawner** | PW `Asteroids.cfg` | n/a (real spawned bodies) | Stock Kopernicus, free | ★★★ Real, harvestable/visitable belt; tie radii to DB. |
| 3 | **ScaledDecorator `.unity3d` prefab** | CS comet tail / pulsar jets; PW protoplanetary disk | Yes (in the asset) | ScaledDecorator (GPL-3.0) + custom Unity bundle | ★★ Most cinematic; requires asset authoring. |
| 4 | **Stock Kopernicus Ring** (`useNewShader`) | SPVE/PW gas giants | No (flat plane) | Stock Kopernicus | ★ Ordinary flat rings only. |

**Technique 1 mechanism (free V3, publishable):** a dedicated
`EVE_CLOUDS / OBJECT` (in SPVE's `rings.cfg`, named `Jool-rings` /
`Dres-rings` — a real ring object, distinct from the aurora objects in
`Planets/*.cfg`) with a raymarched volume whose cloud-type `Item` sets
`minAltitude` and `maxAltitude` — the gap between them *is* the disk's 3-D
thickness, raymarched as an annular slab (e.g. Jool ≈ 2.95 Mm → 4.67 Mm).
A red-channel **coverage map** carves the annulus + gaps; very low
`density` + dark `color` make it dusty rather than opaque; an optional
**particle field** sprinkles discrete grains, and an `ambientSound` can
play inside the volume. (Same node as the free EVE release-3 layer — the
only paid-V5 difference is the node *name* and minor tuning; author
against `layerRaymarchedVolume`.)

> **Note:** SPVE demonstrates this on **planetary rings** (Jool, Dres),
> not a stellar/circumstellar ring — there is no star-ring example in
> SPVE. The technique transfers to circumstellar debris disks, but that
> application is ours, not a copied config. (Jool also carries a separate
> flat Kopernicus `Ring`; the EVE volume is what supplies the 3-D
> thickness/haze. SPVE itself uses no DLL — these effects are pure config
> exploiting existing EVE rendering, no engine modification.)

**Technique 2 mechanism (free):** a Kopernicus `Asteroid` definition named
e.g. `ProtoplanetaryDisk-*` with `Locations { Around { Body {
semiMajorAxis = min/max; inclination; eccentricity } } }` and multiple
radial zones — spawns real asteroids in a belt. Drive `semiMajorAxis` /
`inclination` from real disk radii.

> **SpaceDust is *not* a disk-visual option here:** both packs use
> `SPACEDUST_RESOURCE` (harvestable bands) only — zero `SPACEDUST_CLOUD`
> visual rendering. The mod *can* render visible dust, but neither pack
> demonstrates it, so there's no example to lift.

---

## 4. Aurorae & emissive volumetric FX

All three packs render aurorae the same way, and **SPVE proves it works in
the free release-3 schema** → publishable.

- Mechanism: an `EVE_CLOUDS / OBJECT` combining a **`layer2D`**
  (`macroCloudMaterial` with high `_MinLight` → self-illuminated 2D sheet)
  **+ a raymarched volume** configured to ignore external light:
  `lightMarchSteps = 0`, `lightMarchDistance = 0`,
  `receivedShadowsDensity = 0`, `skylightMultiplier = 0`. With no light
  marching the volume renders its own flat `color` regardless of sun
  direction → reads as **self-emissive glow**, visible on the night side.
  (Raymarched volumetric clouds have no real emission channel; this is the
  standard workaround.)
- An `AuroraCurtain`-style cloud type with a tall, thin altitude band and
  hand-shaped `coverageCurve` / `densityCurve` gives the curtain form.
- **Free vs paid:** author against `layerRaymarchedVolume` (release-3).
  CS/PW auroras mostly use the paid `…V5` node — keep those specifics local.

The same `fxOnlyLayer = True`, `density = 0` invisible-volume pattern is
reused for **localized ambience** (geographic sound/particle triggers via
an SDF coverage map) and **decal effects** (rainbows, shore/forest
ambience) — a clean, general "you are inside region X" mechanism.

---

## 5. Atmospheres, oceans, Scatterer

- **Scatterer atmosphere** (`Scatterer_atmosphere { Atmo { … } }`):
  Rayleigh/Mie betas, `useOzone` + `ozoneAbsorption/Height/Falloff` (a
  **generic stratospheric absorber** slot — see
  [[project_phase3_stratospheric_absorbers]]), `multipleScattering`,
  `godrayStrength` (~0.7 is a safe default), `averageGroundReflectance`.
- **Patch, don't redefine:** use `@Atmo:HAS[#name[X]] { … }` with
  `:LAST`/`:AFTER` to re-tune an existing atmosphere instead of
  redeclaring it — minimizes conflicts.
- **Cloud integration on airless bodies:** registering a body in the
  Scatterer `planetsList` with `flatScaledSpaceModel = True` +
  `usesCloudIntegration = True` gives a nominally airless body just enough
  fake atmosphere for EVE aurorae/disks to pick up correct **star colors**.
- **Multi-star Scatterer (mandatory):** each `planetsList` Item sets
  `mainSunCelestialBody = <local star>` and per-body `eclipseCasters`.
  NearStars' Scatterer writer must emit these per system.
- **Oceans** (`Scatterer_ocean { Ocean { … } }`): `AMP`, `m_windSpeed`,
  `m_omega`, **`m_gravity` = the body's real surface gravity**,
  `m_whiteCapStr` / `shoreFoam`, `m_oceanUpwellingColor` +
  `m_UnderwaterColor` (tint these for non-water look — lava/ammonia are
  done purely by color, not a special shader), `transparencyDepth` /
  `darknessDepth`, `refractionIndex = 1.33`, and a full `caustics*` block.
  Turnkey for any NearStars ocean world.
- **Sunflare override conflict guard:** when overriding the host-star
  flare, gate with `:NEEDS[!BetterKerbol,…]` so it doesn't fight other
  star mods.

---

## 6. PQS terrain recipes (procedural, no real heightmap)

For exoplanets with no real DEM, these stacks generate plausible relief:

- **VoronoiCraters** (multi-pass: big/medium/tiny, each with `CraterCurve`
  + `JitterCurve` Béziers, `voronoiFrequency`, `jitterHeight`) — realistic
  cratering for airless moons.
- **VertexHeightNoiseVertHeightCurve2** (Low/High ridged modes, distinct
  seeds, per-layer `simplexCurve`) + **VertexRidgedAltitudeCurve** +
  **LandControl** (a `_LandClassOcean` with `createScatter = true,
  createColors = false` seeds scatters from height without recoloring) — a
  complete "no-heightmap" relief recipe.
- **VertexHeightOblateAdvanced** (MIT plugin): `oblateMode`
  (`PointEquipotential` | `UniformEquipotential` | …), `energyMode`,
  `period`, `geeASL`/`mass` — analytic Maclaurin/Jacobi oblateness for
  fast rotators. ★ Correct tool for real oblate stars/planets; verify it
  can drive a star's ScaledVersion mesh (it's a PQS mod).
- **MitchellNetravali heightmap** (MIT plugin): bicubic-filtered drop-in
  for `VertexHeightMap` — smoother terrain from low-res maps.

---

## 7. Parallax conventions (fills the pending Parallax reference)

(Addresses the "Parallax still unwritten" item in
[[project_nearstars_mod_refs_pending]].)

- **ParallaxScaled / `Terrain.cfg`** (`@ParallaxTerrain … :FINAL`):
  `ParallaxScaledProperties { mode = FromTerrain; Material {
  _ColorMap / _BumpMap / _HeightMap }; TerrainMaterialOverride { … } }`
  with per-altitude texture banding (`_LowMidBlendStart/End`,
  `_MidHighBlendStart/End`), regolith `_Hapke`, and
  `_SteepPower/Contrast/Midpoint`. This is the real surface+scaled material
  schema, beyond the generic subdivision node.
- **Subdivision injection:** a `:NEEDS[ParallaxContinued]` patch adding
  `PQS { Mods { Parallax { subdivisionLevel, subdivisionRadius,
  order = 999999 } } }` per body.
- **ParallaxScatters** (the surface-scatter system):
  `collisionLevel` (0–4, collidable rocks for landing),
  `BiomeBlacklist { name = … }` (biome-gated placement),
  `DistributionNoise { noiseType, inverted, frequency, octaves, seed }`
  (clustering), `Distribution { spawnChance, populationMultiplier,
  min/maxScale, steepPower/Contrast, min/maxAltitude, alignToTerrainNormal,
  coloredByTerrain }`, `LODs { LOD { model, range } }`, and crystal
  scatters via `Keywords { REFRACTION; SUBSURFACE_SCATTERING }` +
  `_RefractionEta` / `_SubsurfaceColor`. Stock Parallax model atlases can
  be reused so no custom meshes are needed.

---

## 8. EVE weather / particle / effect library

A reusable, named-effect pattern worth adopting as house style. Effects
are defined once and referenced **by string name** from any cloud volume,
decoupling "what happens" from "where/when":

- `EVE_PARTICLE_FIELD_CONFIG` — rain, snow, hail, ash, dust, meteor
  showers, ring grains (`fallSpeed`, `tangentialSpeed`, `fieldParticleCount`,
  `particleSheetCount`, optional `splashes {}`).
- `EVE_DROPLETS_CONFIG` — lens/canopy wet effect.
- `EVE_LIGHTNING_CONFIG` — bolts (`spawnChancePerSecond`, `boltHeight`,
  sound lists), hooked from a cloud type via `lightningFrequency`.
- `EVE_WET_SURFACES_CONFIG` — terrain wetting under precipitation.
- **Episodic scheduler:** `timeSettings { unit; duration; repeatInterval;
  offset; fadeTime }` gates a whole feature on a clock — e.g. periodic dust
  storms, seasonal aurora, meteor showers.
- **Coherent storms from one mask:** a single cloud-type coverage gradient
  simultaneously scales clouds + rain + lightning + ground-wetness via
  `particleFieldDensity` / `lightningFrequency` / `dropletsDensity` /
  `wetSurfacesIntensity`.

These config *node types* exist in the free release-3 EVE; the all-free
particle/droplet/lightning/wetSurface libraries are directly reusable.

---

## 9. Scene-level visuals

- **TUFX post-processing** (`TUFX_PROFILE { Antialiasing; EFFECT
  ColorGrading{ Tonemapper = ACES }; EFFECT Bloom{ Intensity, Threshold,
  Diffusion }; EFFECT AutoExposure }`) — defines the pack's visual identity
  (ACES + heavy bloom for star glow). Profiles are named; scene binding is
  in TUFX's own UI, not cfg.
- **PlanetShine** (`PlanetshineCelestialBody { color (0–255), intensity,
  isSun }`) — per-body bounce light; derive colors from Phase 3 body colors.
- **DistantObjectEnhancement** (`CelestialBodyColor { name, color }`) —
  distant flare/dot tint; also derivable from Phase 3 colors.
- **Rescale fades:** real-scale builds need `@fadeStart *= f` /
  `@fadeEnd *= f` on scaledSpace fades (the packs do this in their rescale
  patches — relevant since NearStars is Sol-real-scale).

---

## 10. Config organization & ModuleManager patterns

The strongest *structural* lessons (both multi-system packs converge here):

- **Per-system self-contained folder tree:**
  `_Systems/<Star>/{Configs, EVE, Scatterer, Parallax, Firefly,
  ScaledDecorator}` + shared `_Core/` (base textures, sounds) + `Miscs/`.
- **Per-system sentinel + deletability** (PW): define
  `SYS_DUMMY { name = System<Star> }` in a `00SystemExists.cfg`; gate every
  downstream patch with `:NEEDS[…&System<Star>]`. Deleting a system's
  folder makes everything (EVE, resources, Scatterer) silently no-op.
  Excellent for a many-star pack.
- **Central settings node + flag toggles:** `:HAS[@<Settings>:HAS[
  #Flag[?rue]]]` (the `?rue`/`?alse` single-char wildcard matches
  True/true casing) to switch optional features without forking files.
- **Tag-based bulk selection:** classify bodies with a `Tag`
  (`NS_Star`, `NS_Planet`, …) and patch via `@Body:HAS[#Tag[NS_Star]]`
  instead of enumerating names.
- **Multi-install adaptation (directly relevant to NearStars' Sol-real-
  scale MVP):** `@…:AFTER[SolSystem]:HAS[@Sol_Configuration:HAS[
  #SystemScale[Real|Quarter|Stock]]] { … }` with a Sun-orbit
  `:NEEDS[!SolSystem]` fallback — one config adapts to RSS/Sol scale or
  stock.
- **`:HAS[#name[X]]` + `:LAST`/`:AFTER`** for surgical patches to existing
  Scatterer/EVE nodes; **`:NEEDS[!OtherPack]`** guards for graceful
  degradation; numeric folder prefixes (`000_`, `001_`) for plugin load
  order.
- **Invisible barycenter recipe** (PW, for the Kopernicus/Keplerian layer):
  a `Template { name = Jool; removeAtmosphere = true }` body shrunk to a
  tiny `radius`, `ScaledVersion { invisible = true; Material color =
  0,0,0,0 }`, `hiddenRnD = true`, `mode = OFF` (hide orbit line); the
  visible components set `referenceBody` to it. (Confirms NearStars' visual-
  binary approach — but NearStars resolves real binaries with Principia
  n-body, not Keplerian.)

Other notable bits: SCANsat `requireLight = false` patch (for dim
interstellar systems); biome-keyed localized crew reports with the
`displayName = …^N` localizer marker; 5-language localization layout.

---

## 11. Quality cautions / what NOT to copy

- **Everything is stock-scale.** All radii, altitudes, SOIs, luminosity /
  intensity / temperature curves, `HazardousBody` thresholds, raymarching
  `baseStepSize`/`maxStepSize`/`scaledFadeAltitude`, and ring bands are
  tuned to **stock Kerbin radii and Kerbol** (or compressed ~100× inter-
  system distances). **Copy the structure, never the numbers** — NearStars
  is Sol-real-scale.
- **Stars orbit `Sun` directly (no barycenter) in both packs.** That model
  does **not** transfer to NearStars' Principia n-body real-binary systems.
- **Copy-paste artifacts** abound (a corona texture path with the wrong
  star name; duplicated `…V5`/`LayerRaymarchedVolumeV5` nodes; verbatim
  sound lists; stray V5 nodes inside SPVE's "free" V3 build). If mining a
  V3 cfg as a template, **scrub for `…V5`** before publishing.
- **VertexColorMapEmissive is incompatible per-surface, not per-install.**
  It injects emissive in three places (ScaledVersion / PQS terrain / Ocean).
  Per its README, the **PQS-terrain** layer is nullified by Parallax
  Continued (which owns terrain shading) and the **Ocean** layer doesn't
  function on Scatterer oceans (stock oceans only). The mods still coexist
  fine in one install — but on a NearStars body (Parallax + Scatterer) only
  VCME's **ScaledSpace / orbital-view** emissive works; close-up terrain and
  Scatterer-ocean emissive do not. So its NearStars use is limited to
  orbital-view glow (e.g. a lava world seen from map/space).
- **No single source of truth** in these packs (editing one body touches
  several files) — the opposite of NearStars' derived-from-DB pipeline.
  Keep NearStars' generation model; borrow only the output conventions.

---

## 12. Priority adoption list for NearStars

1. **Star-rendering generator** — Material/Light/Coronas/Atmosphere/
   HazardousBody + 4 intensity curves, all computed from curated
   Teff / L / R / mass. Highest value; entirely free/publishable. (§2)
2. **Debris disk** — raymarched EVE annular volume (free V3, config-only)
   and/or stock Asteroid spawner; pick per host, drive from real disk
   radii. (§3)
3. **Parallax Terrain + Scatters schema** into the Parallax skill. (§7)
4. **`VertexHeightOblateAdvanced` (MIT)** for real oblate fast rotators. (§6)
5. **Multi-system folder + sentinel `:NEEDS[&SystemX]` isolation** as the
   asset-layer organization for many star systems. (§10)
6. **Scatterer multi-star** (`mainSunCelestialBody` + `eclipseCasters`)
   and **ocean** templates. (§5)
7. **Free-schema aurora** + named EVE effect-library house style. (§4, §8)
8. **TUFX / PlanetShine / DOE color tables** from Phase 3 colors;
   **rescale fade** scaling. (§9)
9. **Multi-install `:HAS[#SystemScale[…]]` adaptation** pattern. (§10)

---

## Sources

- SPVE — <https://github.com/TheSpacePotato/SpacePotato-s-Volumetric-Enhancements> (CC BY-NC 4.0)
- Cosmic Serenity — <https://github.com/ProximaCentauri-star/Cosmic-Serenity> (configs GPL-3.0; assets ARR)
- Promised Worlds — <https://github.com/PromisedWorlds/PromisedWorlds> (CC-BY-NC-SA; bundled plugins MIT/GPL-3.0; settings DLL proprietary)
- blackrack True Volumetric Clouds / EVE-Redux — Patreon (paid EA; see [[reference_volumetric_clouds_naming]])
