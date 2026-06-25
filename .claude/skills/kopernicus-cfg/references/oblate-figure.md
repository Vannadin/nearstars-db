# Oblate / Triaxial Figure (VertexHeightOblateAdvanced)

Reference: `github.com/jamespglaze/VertexHeightOblateAdvanced` (MIT, KSP 1.12.x)
Kopernicus source: standard `ModLoader<PQSMod>` (inherits `order`, `enabled`, `name`)

Renders a body as an oblate or triaxial ellipsoid instead of a sphere — the **visual** counterpart to the gravity figure (J2/C22). Drop-in PQSMod; adds two extra in-flight camera modes inside the SOI of any body that uses it.

## Node placement

Inside `Body { PQS { Mods { VertexHeightOblateAdvanced { ... } } } }`. Like every PQSMod it also accepts `order`, `enabled`, and `name`.

## Fields

| field | type | meaning | range/units | default |
|-------|------|---------|-------------|---------|
| `oblateMode` | enum | figure model: `PointEquipotential` \| `UniformEquipotential` \| `Blend` \| `CustomEllipsoid` \| `ContactBinary` | — | `PointEquipotential` |
| `energyMode` | enum | `Low` \| `High` — only used by `UniformEquipotential` | — | `Low` |
| `mass` | double | body mass; if 0, computed from `geeASL` | kg | `0` |
| `geeASL` | double | surface gravity; ignored if `mass` given | g (Earth = 1) | `0` |
| `period` | double | **rotation** period | seconds | `0` |
| `a` | double | primary equatorial axis as **ratio** of reference radius, ≥1 | ratio | `1` |
| `b` | double | secondary equatorial axis as ratio of reference radius, ≥1 | ratio | `1` |
| `c` | double | polar axis as ratio of reference radius, ≥1 | ratio | `1` |
| `primaryRadius` | double | `ContactBinary` only — primary lobe radius as ratio of neck radius | ratio | — |
| `secondaryRadius` | double | `ContactBinary` only — secondary lobe radius as ratio of neck radius | ratio | — |

There are **no** oblateness/flattening scalar, blend-weight, or curve fields — only the above plus the inherited `order`/`enabled`/`name`.

### Field usage by mode

| field | used by |
|-------|---------|
| `mass` / `geeASL` / `period` | `PointEquipotential`, `UniformEquipotential`, `Blend` |
| `a` / `b` / `c` | `Blend`, `CustomEllipsoid` |
| `energyMode` | `UniformEquipotential` only |
| `primaryRadius` / `secondaryRadius` | `ContactBinary` only |

### energyMode physics (UniformEquipotential)

- `Low` — Maclaurin spheroid up to polar:equatorial = 1.42.
- `High` — Maclaurin spheroid for 1.42–1.716, then Jacobi ellipsoid for 1.716–2.850.

`ContactBinary` is real but experimental, used by no known pack and omitted from the README — treat as experimental/inferred.

## Verbatim examples

CustomEllipsoid, oblate (`QuackPack/Subon.cfg`):

```cfg
VertexHeightOblateAdvanced
{
    oblateMode = CustomEllipsoid
    a = 1.375
    b = 1.375
    c = 1
}
```

CustomEllipsoid, triaxial (`Edge-Of-Eternity/Isathe.cfg`):

```cfg
VertexHeightOblateAdvanced
{
    oblateMode = CustomEllipsoid
    a = 2.10755681818
    b = 1.48621744318
    c = 1
}
```

UniformEquipotential Low (`Celestial-Harmony/Etnas.cfg`):

```cfg
VertexHeightOblateAdvanced
{
    oblateMode = UniformEquipotential
    energyMode = Low
    geeASL = 0.01
    period = 7000
}
```

UniformEquipotential High (`Whirligig-World/YawerTriaxialVHOA.cfg`):

```cfg
VertexHeightOblateAdvanced
{
    oblateMode = UniformEquipotential
    energyMode = High
    period = 6100
    mass = 6.2776078e19
}
```

## License & dependency

- MIT (Copyright 2024 James Glaze) — bundling and a hard dependency are both permitted, compatible with NearStars' CC-BY-NC-SA.
- A **hard dependency** for any body whose PQS uses the node — there is no cfg fallback if the plugin is absent.
- Requires ModuleManager + Kopernicus. Packs ship it under `GameData/001_DuckweedUtils/`; CKAN installs it via `.*DuckweedUtils`.

## NearStars mapping

Our figure pass (`docs/reference/body-figure-methodology.md`, tool `scripts/refs/body_figure.py`) produces each body's degree-2 figure (J2/C22). The **gravity** emit is Principia (separate); **this mod is the visual emit**, and the two come from the same figure so they stay consistent.

- Use **`oblateMode = CustomEllipsoid`** for all NearStars bodies — deterministic, exactly matches our computed J2/C22. `body_figure.py::ellipsoid_ratios()` already outputs a:b:c in this mod's convention (`c=1` smallest, `a`/`b` ≥ 1).
- `UniformEquipotential` is the physics alternative for fluid bodies (gas giants, fast free rotators): it self-computes the Maclaurin/Jacobi figure from `mass`+`period`. It may differ slightly from our Radau–Darwin J2, so prefer `CustomEllipsoid` for consistency.
- Emit only above a visible threshold (`a/c ≳ 1.02`); below that, skip the visual (gravity C22 may still emit).
- **Writer-stage caveat:** `a`/`b`/`c` are ratios on the PQS reference radius. Either set reference radius = polar radius (`c=1`, body grows) or volume-normalize so `a·b·c = 1` (mean radius preserved). Pack examples use `c=1` (non-volume-normalized). Flag this as a writer decision.

Example NearStars values (from the figure pass):

| body | a:b:c | figure |
|------|-------|--------|
| Polyphemus | 1.149 : 1.149 : 1.0 | oblate giant |
| Dante | 1.167 : 1.042 : 1.0 | triaxial |
| Chaos | 1.075 : 1.075 : 1.0 | oblate |
| Hades | 1.053 : 1.013 : 1.0 | triaxial |
| Pandora / Cassandra | below threshold | skip visual |
