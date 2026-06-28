# KSP Science System — Reference for NearStars body authoring

> **Perspective.** What a planet pack must author, per new body, so science
> works under **both** stock KSP science **and** Kerbalism/ROKerbalism (RP-1).
> Grounded in upstream sources (cited inline). NearStars targets both player
> stacks: Sandbox/Science on Sol-Configs (stock science) and RP-1 on Sol V1.0
> (Kerbalism). See [`plans/rp1-integration/plan.md`](../../plans/rp1-integration/plan.md).

---

## 0. The one-paragraph answer

Author **biomes + a `ScienceValues` block** once, at the **Kopernicus body
level**. Both stock science and Kerbalism read them directly — Kerbalism has
**no per-body science config of its own**. The *only* divergence is flavor
text: stock `ScienceDefs RESULTS{}` strings are shown to stock players but are
**ignored by Kerbalism's completion flow** (Kerbalism auto-composes a title
from body + situation + biome names and uses generic result lines). The one
genuinely Kerbalism-specific per-body knob is the **radiation environment**
(belts/magnetosphere), which makes Kerbalism's radiation *virtual biomes*
resolve at the body — and that overlaps with RP-1 integration WS4.

| Body-side artifact | Stock | Kerbalism/RP-1 | Author once? |
|--------------------|:-----:|:--------------:|:------------:|
| `ScienceValues` (9 fields) | ✅ reads | ✅ reads (this *is* its per-body multiplier) | **Yes** |
| Biome map + `Biomes{}` | ✅ reads | ✅ reads (stock `Body.BiomeMap`) | **Yes** |
| `ScienceDefs RESULTS{}` flavor | ✅ shows | ❌ ignored in completion | stock-only |
| Radiation belts/magnetosphere | n/a | enables radiation *virtual biomes* — but **no RP-1 experiment uses them (§3.4)**: latent | Kerbalism-only (optional) |
| Experiment defs / parts | global | global (RP-1 content) | **never per-body** |

---

## 1. Stock science system

### 1.1 Experiments (12 base) + DLC

| `id` | Title | Carrier |
|------|-------|---------|
| `crewReport` | Crew Report | any crewed part |
| `evaReport` | EVA Report | Kerbal on EVA |
| `surfaceSample` | Surface Sample | EVA on surface |
| `asteroidSample` | Asteroid Sample | EVA at grappled asteroid |
| `cometSample` | Comet Sample | EVA at comet |
| `mysteryGoo` | Mystery Goo™ | Goo Containment Unit |
| `mobileMaterialsLab` | **Materials Study** (id ≠ MPL lab) | SC-9001 Science Jr. |
| `temperatureScan` | Temperature Scan | 2HOT Thermometer |
| `barometerScan` | Atmospheric Pressure Scan | PresMat Barometer |
| `gravityScan` | Gravity Scan | GRAVMAX |
| `seismicScan` | Seismic Scan | Double-C Accelerometer |
| `atmosphereAnalysis` | Atmosphere Analysis | Fluid Spectro-Variometer (atmo only) |

- **Breaking Ground:** surface features → `ROCScience_<Feature>` (~42 stock defs,
  e.g. `ROCScience_MunStone`); 4 deployed → `deployedSeismicSensor`,
  `deployedWeatherReport` (atmo only), `deployedGooObservation` (≠ `mysteryGoo`),
  `deployedIONCollector` (airless only).
- **Making History:** zero new experiments.
- Not experiments: `recovery` (banking mechanic), Mobile Processing Lab (data→science).

Source: stock ScienceDefs mirror `raw.githubusercontent.com/pjf/ksp-gamedata/master/Squad/Resources/ScienceDefs.cfg`; ROC scheme `github.com/Kerbalism/Kerbalism/issues/395`.

### 1.2 Situations & masks

`ExperimentSituations`: `SrfLanded`(landed/prelaunch), `SrfSplashed`(ocean bodies
only), `FlyingLow`/`FlyingHigh`(atmosphere bodies only), `InSpaceLow`/`InSpaceHigh`.

Bitmask (same layout for `situationMask` and `biomeMask`):

| Situation | SrfLanded | SrfSplashed | FlyingLow | FlyingHigh | InSpaceLow | InSpaceHigh |
|-----------|:---------:|:-----------:|:---------:|:----------:|:----------:|:-----------:|
| value | 1 | 2 | 4 | 8 | 16 | 32 |

`situationMask` = where the experiment runs. `biomeMask` = which of those
situations give biome-specific results (subset of situationMask; `0` = never).
`63` = all six. Most atmosphere/ocean gating is done by *which bits are set*,
not separate flags (`requireNoAtmosphere`/`requireSurface` are **unverified**
for stock 1.12.x; `requireAtmosphere` is real).

### 1.3 Body values — `Body { Properties { ScienceValues {} } }`

Exactly **9 fields** (per-situation multipliers + thresholds):

| Field | Role | Kerbin | Mun | Duna | Sun |
|-------|------|:------:|:---:|:----:|:---:|
| `landedDataValue` | × SrfLanded | 0.3 | 4 | 8 | 1 |
| `splashedDataValue` | × SrfSplashed | 0.4 | 1 | 1 | 1 |
| `flyingLowDataValue` | × FlyingLow | 0.7 | 1 | 5 | 1 |
| `flyingHighDataValue` | × FlyingHigh | 0.9 | 1 | 5 | 1 |
| `inSpaceLowDataValue` | × InSpaceLow | 1.0 | 3 | 7 | 11 |
| `inSpaceHighDataValue` | × InSpaceHigh | 1.5 | 2 | 5 | 2 |
| `recoveryValue` | × on recovery | 1.0 | 2 | 5 | 4 |
| `flyingAltitudeThreshold` | m, FlyingLow↔High | 18000 | 18000 | 12000 | 18000 |
| `spaceAltitudeThreshold` | m, InSpaceLow↔High | 250000 | 60000 | 140000 | 1E+09 |

- Both thresholds are **per-body** and drive situation resolution.
- Pattern: home body lowest; farther/harder bodies scale up; airless bodies keep
  `flyingLow/High = 1` placeholders.
- **The Sun is the template for NearStars star bodies**: no `Biomes`,
  `spaceAltitudeThreshold = 1E+09`, modest multipliers.
- Not in this node: `RnDNormalRate`, `sciSpaceLowMultiplier` (do not exist here).

Source: Kopernicus kittopia-dumps; `github.com/Kopernicus/Kopernicus/wiki/Properties`.

### 1.4 Biomes

In `Body { Properties { } }` alongside ScienceValues:

```
biomeMap = NearStars-Textures/PluginData/<Body>/<Body>_Biomes.dds   // path sans GameData, with extension
Biomes {
    Biome { name = Lowlands ; value = 1 ; color = RGBA(0,255,255,255) }
    Biome { name = Highlands; value = 1 ; color = RGBA(51,255,255,255) }
}
```

- One **solid flat color = one biome**; Kopernicus matches on the **full RGB(A)
  color** of each pixel. Two color syntaxes exist in the wild: float `0–1`
  (`color = 0.2,0.5,0.1,1`) and 0–255 `RGBA(...)`. NearStars/Sol-Configs use the
  `RGBA(...)` form.
- `value` = per-biome **science multiplier** (not an index/color).
- Texture rules: uncompressed (DDS in `PluginData/` so DDSLoader skips DXT;
  DXT corrupts flat colors), **no mipmaps**, hard edges (no AA/gradients), ~1K is plenty.
- A science **subject = experiment × body × situation × (biome if the
  experiment's `biomeMask` enables it for that situation)**.

> ⚠️ **Skill reconciliation flag.** `kopernicus-cfg/references/pitfalls.md`
> currently says biomes "use only the R channel". That is imprecise — Kopernicus
> matches the full color; our cyan convention happens to vary only R within
> G=B=255. Verify against Kopernicus source and fix the phrasing there.

### 1.5 Result text — `ScienceDefs RESULTS{}`

```
@EXPERIMENT_DEFINITION:HAS[#id[crewReport]] {
    @RESULTS {
        <Body>InSpaceLow            = ...
        <Body>SrfLanded<BiomeNoSpaces> = #LOC_NearStars_...
    }
}
```

- **Key form: concatenated `<Body><Situation><Biome>`, NO `@` separator** (the
  `@` only appears in the runtime subject ID, not in RESULTS keys). Body = the
  Kopernicus internal body name. No experiment prefix (the block's `id` identifies it).
- Biome spaces/punctuation stripped: `KerbinSrfLandedLaunchPad`.
- Fallback order: `<Body><Situation><Biome>` → `<Body><Situation>` → `default`
  (multiple `default =` allowed → random pick).
- Inject by id selector **`:HAS[#id[<exp>]]`** (not `:FOR[]`). `key =` adds a
  new key; `%key =` overwrites an existing one. RHS is usually a `#LOC_...` token.

Source: OPM `Patches/OPM_ScienceDefs.cfg`; GPP `GPP_Science_Defs.cfg`;
`github.com/Amorymeltzer/ksp/blob/main/parseScience.pl`.

---

## 2. Kerbalism / ROKerbalism science (RP-1)

### 2.1 Three-layer architecture

| Layer | Repo | Role |
|-------|------|------|
| Engine | `Kerbalism/Kerbalism` | the file-based science *mechanic* (C# `Experiment`/`HardDrive`/`Laboratory`, value math, virtual biomes) |
| Profile | `KSP-RO/ROKerbalism` | life-support/radiation profile — **defines no experiments** |
| Content | `KSP-RO/RP-1` (`GameData/RP-1/Science/`) | the experiment definitions + real-instrument parts (global, **not per-body**) |

Kerbalism **replaces the runner** (its `Experiment` PartModule supplants stock
`ModuleScienceExperiment`, auto-adds a `HardDrive` to pods) but **reuses the
stock `EXPERIMENT_DEFINITION` data node** (reads `id`, `baseValue`, `scienceCap`,
`dataScale`, `situationMask`, `biomeMask`) and extends it with a
`KERBALISM_EXPERIMENT{}` sub-node.

Source: `github.com/Kerbalism/Kerbalism/wiki/TechGuide-~-Supporting-Science-Mods`;
`kerbalism.readthedocs.io/en/latest/science.html`.

### 2.2 File-based model

Experiments **run over time** (background-capable on unloaded vessels), output
**files** (transmissible to DSN at a data rate; `sample_mass = 0`) or **samples**
(have mass, non-transmissible, recover or lab-analyze). RP-1's roster is
tiered real instruments (`crewReport`/`temperatureScan`/`evaReport`/`surfaceSample`
reused + custom `RP0<name><tier>` like `RP0magScan1/2/3`), ~34 parts, each
carrying a `totalScienceLevel` fraction so tech tiers return increasing % — **none
of the stock Goo/Science-Jr. paradigm**.

### 2.3 Conditions — situations, virtual biomes, `requires`

`KERBALISM_EXPERIMENT { Situation = Surface@Biomes; Situation = Space@VirtualBiomes; ... }`

- Builds on stock situations + composites (`Space`, `BodyGlobal`). Suffix
  `@Biomes` (stock biomes) or `@VirtualBiomes`.
- **Virtual biomes** (environment-based): `Storm` (solar storm), `Reentry`
  (>Mach 5 descending), **`Interstellar`** (in a sun SOI, outside the
  heliopause), `InnerBelt`/`OuterBelt`/`Magnetosphere` (radiation fields),
  `NoBiome`. **`Reentry`/`Storm` are virtual biomes, not situations** (common trap).
  This is a Kerbalism capability; **RP-1's shipped experiments do not use any
  virtual biome** (§3.4).
- Body gating: `BodyAllowed`/`BodyNotAllowed` = `HomeBody`, `Suns`, `Planets`, `Moons`, ...
- Module-level `requires` string (comma-separated, ALL must hold) — large token
  set incl. `Sunlight`/`Shadow`, `Atmosphere`/`Vacuum`, `Ocean`, `InnerBelt`,
  `Magnetosphere`, `InterPlanetary`, **`InterStellar`**, orbital/thermal/pressure mins-maxes.

Source: `kerbalism.readthedocs.io/en/latest/modders/modules.html`; `src/Kerbalism/Science/ScienceSituation.cs`.

### 2.4 Body values & text (what Kerbalism reads vs ignores)

- **Reads stock `ScienceValues` directly**: `ScienceSituation.BodyMultiplier`
  maps each situation to the stock field (`landedDataValue`, ...,
  `inSpaceHighDataValue`). The Kopernicus block **is** Kerbalism's per-body scaling.
- **Reads stock biome map** (`Body.BiomeMap`); above `minVirtualBiome` the index
  resolves to a virtual biome instead. Virtual biomes layer *on top of* stock biomes.
- **Ignores stock `RESULTS{}` flavor** in completion. Player sees: an
  auto-composed **title** (`BodyTitle + SituationTitle + BiomeTitle`) + generic
  random lines (`Sciencresult1..5`) + per-experiment static `experiment_desc`.
  Per-(body+situation+biome) custom result text is effectively **unsupported**
  (a `file.resultText` hook exists in code but its config path is untraced — treat as unsupported).
- Credit math: `DataSize = baseValue·dataScale`; `ScienceMaxValue = scienceCap·
  ScienceGainMultiplier · <situation>DataValue`; collected MB × (max/size),
  clamped to stock RnD subject cap. Diminishing returns = stock.

Source: `src/Kerbalism/Science/` (`ScienceSituation.cs`, `Situation.cs`, `SubjectData.cs`, `ExperimentInfo.cs`, `Science.cs`).

---

## 3. RP-1 experiment roster & durations

What a player can research/collect under RP-1, and how long each takes. RP-1
replaces stock instant-science: collection time is encoded as
`@data_rate /= N //comment`, where **N seconds is the dwell/transmit time** —
running for x% of N yields x% of the science (ROKerbalism partial credit). There
is almost no literal `duration` field, and `data_size` is absent (derived =
rate × time). "Science" below = `baseValue` (= `scienceCap`). Source:
`KSP-RO/RP-1` `GameData/RP-1/Science/Experiments/` @ master.

### 3.1 Instrument experiments (stock-style tiered)

| Discipline (id) | Studies | Situations | Science | Duration |
|-----------------|---------|------------|:-------:|----------|
| `crewReport` | crew situation report | all (63) | 4 | 5 min |
| `evaReport` | EVA observation | Srf+FlyHigh+SpaceHigh (51) | 24 | 2 min |
| `RP0telemetry1` | vessel telemetry | all (63) | 3 | 5 min |
| `temperatureScan` | ambient temperature | all (63) | 4 | 10 min |
| `barometerScan` | atmospheric pressure | no-splash (61) | 4 | 10 min |
| `surfaceSample` / `2` / `3` | surface scoop / core | SrfLanded (1) | 6 / 10 / 15 | 5 min / 20 min / 2.5 h |
| `surfaceAnalysis` | in-situ surface analysis | SrfLanded (1) | 4 | 30 min |
| `RP0magScan1/2/3` | magnetic field (early/He/fluxgate) | space + biome (49) | 6 / 12 / 40 | 1 mo / 1 mo / 3 mo |
| `RP0cosmicRay1/2` | cosmic-ray flux | space (48) | 10 / 30 | 3 mo |
| `RP0RPWS1/2/3` | radio & plasma wave | space (49) | 7 / 20 / 30 | 1 wk / 1 mo / 6 mo |
| `RP0massSpec1–4` | mass spectrometry | space + biome (57) | 8 / 12 / 20 / 30 | 2 h / 14 d / 3 mo / 3 mo |
| `RP0infraredRad1–4` | IR radiometry | space (48) | 2 / 3 / 4 / 6 | ~3 h / 4 h / ~11 h / 15 d |
| `RP0imageSpec1–4` | imaging spectrometry (Sun-angle gated) | space (48) | 3 / 3 / 4 / 6 | 10 d / 1 h / 96 h / ~78 h |
| `RP0visibleImaging1–5` | TV imaging (vidicon→HiRISE) | all (63) | 1.5–50 | 40 min → ~405 h |
| `micrometeoriteDetect` | micrometeorite tally | space (48) | 7 | 3 mo |
| `RP0orbitalPurturbation1` | orbit tracking → gravity field | space (48) | 200 | **10 yr** |
| `RP0bioScan1/2` 🏠 | biological specimen | FlyHigh+Space / Space | 22.5 / 40 | 20 min / 1 d |
| `RP0Cherenkov` 🏠 | high-energy particle | space (48) | 20 | 3 mo |
| `RP0photos1–4` 🏠 | Earth reconnaissance (V-2→HST) | space | 5 → **10000** | 10 min → **20 yr** |

🏠 = home-body only. (`Purturbation` misspelling is verbatim from source.)

### 3.2 SCANsat (optional, `:NEEDS[SCANSat]`)

RP-1 only **re-tunes the science value** of SCANsat's own experiments
(`SCANsatAltimetryLoRes`/`HiRes`, `SCANsatBiomeAnomaly`, `SCANsatResources`, all
InSpaceLow). The experiments + scan-coverage timing live in the SCANsat mod, not RP-1.

### 3.3 Crewed / station science (ROKerbalism timed)

A large separate family in `Science/Experiments/CrewScience/` (8 files, ~60
experiments) attached to capsules/stations/bases via boolean tier flags.
Durations span ~18 min → 2 years. Representative:

| id | studies | science | duration |
|----|---------|:-------:|----------|
| `RP0FlightControl` | yaw/pitch/roll response | 20 | 3 h |
| `RP0EarthPhotography` | handheld Earth imaging | 40 | 6 h |
| `RP0TelevisionBroadcast` | live TV en route to Moon | 80 | 4 h |
| `RP0ALFMED` | cosmic-ray light-flash | 20 | 4 d |
| `RP0longDurationHabit1/2` | long-duration habitation | 750 / 1500 | ~180 d / **2 yr** |
| `RP0LunarOrbitHabit` | lunar-orbit habitation | 400 | 720 d |
| `RP0lunarSeismicNetwork` | lunar seismic network | — | 365 d |

(`StationScienceEarly.cfg.disable` ships disabled — not collectable.)

### 3.4 Tiering, applicability, caveats

- **Tiering:** a discipline's total science splits across instrument tiers via the
  part's `totalScienceLevel` fraction (cosmic ray T1 `0.375` → T2 `1.0`; the top
  tier omits it = full cap). Higher tiers cost more, take longer, gate harder
  (eccentricity / Sun-angle / inclination). `GlobalExperimentPatches.cfg` is a
  `@dataScale /= baseValue` normalizer, **not** the tier engine.
- **Applicability:** most instruments are **body-agnostic** — they fire on any
  body once the situation mask is met. Home-only exceptions: **Photography (all
  tiers), Biological Sample, Cherenkov**.
- **No virtual biomes in RP-1.** **No RP-1 experiment references `InnerBelt`/
  `OuterBelt`/`Magnetosphere`/`Interstellar`/`Storm`** virtual biomes. That
  Kerbalism machinery exists but is **unused by RP-1 as shipped** — so
  radiation-belt / interstellar science is a *latent* hook, not active content.
- **Home-body surface ≈ 0 science** by explicit RP-1 design rule.

Source: roster pulled from `GameData/RP-1/Science/Experiments/` @ master
(durations quoted from `@data_rate /= N` lines; some lower-tier `data_rate` /
`totalScienceLevel` literals are summarizer-derived — verify before shipping cfg).

---

## 4. Per-body authoring checklist (NearStars, both systems)

For each new body `<X>` (Kopernicus internal name):

1. **`ScienceValues` (9 fields)** — *the* most important knob; read by both
   systems. Multipliers scale with distance/difficulty (Kerbin = 0.3–1.5 floor).
   Airless → flyingLow/High = 1 placeholders. **Stars → copy the Sun pattern**
   (large `spaceAltitudeThreshold`, no biomes).
2. **Biome map + `Biomes{}`** — read by both. Required for per-biome variety on
   surface/low situations. Flat colors, no mipmaps, in `PluginData/`. Stars: omit.
3. **Situation thresholds** — covered by the two threshold fields in step 1.
4. **`ScienceDefs RESULTS{}`** — `@EXPERIMENT_DEFINITION:HAS[#id[<exp>]]` per
   stock experiment, keys `<X><Situation>[<Biome>]`. **Stock players only** —
   skip if you only target Kerbalism. Include Breaking Ground ids if NearStars
   ships deployed/ROC content.
5. **(Radiation environment — gameplay, not RP-1 science)** — defining the
   body's radiation belts/magnetosphere (RP-1 integration WS4: ROKerbalism
   `RadiationBody`, gated `:NEEDS[ProfileRealismOverhaul]`,
   [`plans/rp1-integration/plan.md`](../../plans/rp1-integration/plan.md)) makes
   Kerbalism's `InnerBelt`/`OuterBelt`/`Magnetosphere`/`Interstellar` virtual
   biomes *resolvable* at the body. But **RP-1's shipped experiments don't
   reference virtual biomes (§3.4)**, so this yields **no science under RP-1
   today** — it's a radiation/life-support concern, plus a latent science hook
   NearStars could tap only with custom experiments.

**Minimum viable body:** ScienceValues only (generic text, one subject/situation).
**Full-flavor body:** ScienceValues + biome map + RESULTS text.

**Overlap summary:** under RP-1, per-body science authoring is **~100% stock
authoring** (biomes + ScienceValues) — there is no per-body Kerbalism science
cfg, and you never write experiments or situation gates (global RP-1 content,
§3). `RESULTS{}` flavor is the only stock-only investment; the radiation
environment is a gameplay/WS4 concern whose science payoff is latent.

---

## 5. NearStars status & notes

- **Existing scaffolding:** `kopernicus-cfg` skill already has biome patterns
  (`planet-body.md`, `gas-giant.md`); `mod-release-layout.md` defines
  `[Body]-Kopernicus.cfg` (biomes) + `[Body]-ScienceDefs.cfg` (result text) +
  `[Body]_Biomes.dds`. Phase 4 checklist has "Science experiment text for all bodies".
  The structure exists; **per-body science content is unwritten.**
- **The DB has no science fields** — science values/biomes/text are authored at
  cfg-emit time (project end), not stored in `db/systems/*.json`.
- **Interstellar virtual biome** exists in Kerbalism (a sun SOI, outside the
  heliopause) and is a thematic fit for NearStars — but **no RP-1 experiment
  references it (§3.4)**, so it yields no science under RP-1 as shipped. It's a
  latent hook NearStars could exploit only with a custom Kerbalism experiment.
- **Premise corrections** baked into this doc: RESULTS keys have no `@`; inject
  via `:HAS[#id[]]`; biome match is full-RGB; Kerbalism ignores RESULTS text;
  ScienceValues has exactly 9 fields; RP-1 experiments don't use virtual biomes.

## Related

- [guideline](guideline.md) — Phase 4 science-text checklist item
- [mod-release-layout](mod-release-layout.md) — `[Body]-ScienceDefs.cfg` / biome DDS conventions
- [plans/rp1-integration](../../plans/rp1-integration/plan.md) — radiation env / WS4 overlap
