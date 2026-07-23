# Principia CFG Technical Reference

> Source: mockingbirdnest/Principia GitHub repo, wiki, and astronomy/*.cfg files  
> Purpose: Reference for generating Principia-compatible CFG files for KSP planet packs

> **Perspective.** This document is the **external Principia CFG API
> reference** — the full set of nodes/keys Principia accepts and their
> meanings, sourced from upstream code and docs. Independent of any
> particular planet pack.
>
> For **NearStars-specific implementation** — which subset of nodes the
> project actually emits, how `db/systems/*.json` fields map to CFG
> values, what variants (Sol Real / Sol Quarter / RSS) are MVP-supported,
> and the rationale for diverging from `:NEEDS:FOR[NearStarsSystem]` on
> Principia patches — see the
> [`principia-cfg` skill](../../.claude/skills/principia-cfg/SKILL.md).

---

## Overview

Principia replaces KSP's patched-conic (sphere-of-influence) gravity with full N-body physics. It reads configuration from KSP's GameDatabase (same system as Kopernicus). Config nodes are discovered via `GameDatabase.Instance.GetAtMostOneNode(name)` — ModuleManager merging applies, and there must be **at most one** instance of each top-level node after all patches resolve.

---

## Top-Level CFG Nodes

| Node name | Purpose |
|---|---|
| `principia_gravity_model` | Physical properties (mass, rotation, geopotential) |
| `principia_initial_state` | Cartesian positions and velocities at a reference epoch |
| `principia_numerics_blueprint` | Numerical integrator configuration |
| `principia_draw_styles` | Trajectory visualization colors and line styles |
| `principia_override_version_check` | Suppress KSP version mismatch fatal error |

**Rule**: Each node may appear **at most once** after ModuleManager processing. Two `principia_gravity_model` roots = crash.

---

## `principia_gravity_model`

Provides accurate rotational and gravitational parameters. Overrides values Principia would derive from `CelestialBody` fields. Optional — if absent, falls back to KSP's `gravParameter`, `angularV`, `initialRotation`.

### Structure

```cfg
principia_gravity_model[:NEEDS[SomeMod]] {
  body { ... }
  body { ... }
}
```

To patch from an addon:

```cfg
@principia_gravity_model:NEEDS[OPM] {
  body { ... }
}
```

### `body` node keys

| Key | Type | Required | Notes |
|---|---|---|---|
| `name` | string | Yes | Must match `CelestialBody.name` (Kopernicus `Body { name = X }`), not `displayName` |
| `gravitational_parameter` | quantity (m³/s²) | Conditional* | μ = GM. Required if `principia_initial_state` is present |
| `reference_instant` | instant | No | Epoch for rotation reference. Default: `JD2451545.000000000` (J2000) |
| `axis_right_ascension` | quantity (angle) | No | ICRF RA of north pole. Default: `-90 deg` |
| `axis_declination` | quantity (angle) | No | ICRF Dec of north pole. Default: `90 deg` |
| `reference_angle` | quantity (angle) | No | Prime meridian angle W₀ at `reference_instant`. Default: KSP's `initialRotation` |
| `angular_frequency` | quantity (angle/time) | No | Sidereal rotation rate. Default: KSP's `angularV` |
| `reference_radius` | quantity (length) | Conditional | Required if `j2` or `geopotential_row` is present |
| `j2` | float | No | Unnormalized J₂ zonal harmonic. Mutually exclusive with `geopotential_row` |
| `geopotential_row` | sub-node (repeating) | No | Full spherical harmonic geopotential. Mutually exclusive with `j2` |

*`gravitational_parameter` is required when `principia_initial_state` is present.

**Rotation model convention**: Follows IAU 2009 WG on Cartographic Coordinates. Default `-90 deg` / `90 deg` aligns pole with KSP's internal frame.

### J2 example

```cfg
body {
  name                    = Sun
  gravitational_parameter = 1.3271244004193938e+11 km^3/s^2
  reference_instant       = JD2451545.000000000
  axis_right_ascension    = 286.13 deg
  axis_declination        = 63.87 deg
  reference_angle         = 84.176 deg
  angular_frequency       = 14.1844000 deg / d
  reference_radius        = 696000.0 km
  j2                      = 2.11060885327268404e-07
}
```

### Geopotential example

```cfg
body {
  name             = Earth
  reference_radius = 6378.1363 km
  geopotential_row {
    degree = 2
    geopotential_column {
      order = 0
      cos   = -4.84169457320000017e-04
      sin   = 0.0
    }
    geopotential_column {
      order = 2
      cos   = 2.43937341593980011e-06
      sin   = -1.40029401183640008e-06
    }
  }
}
```

---

## `principia_initial_state`

Provides Cartesian initial conditions for every body in an inertial frame. If **absent**, Principia derives initial states from KSP's Keplerian orbital elements (Jacobi coordinates). If **present**, both this node and `principia_gravity_model` are required and must cover every body.

### Structure

```cfg
principia_initial_state[:NEEDS[RealSolarSystem]] {
  game_epoch         = JD2433647.5
  solar_system_epoch = JD2433282.500000000
  body { ... }
  body { ... }
}
```

### Top-level fields

| Key | Type | Notes |
|---|---|---|
| `game_epoch` | instant | KSP Universal Time 0 mapped to a real instant (in-game start date) |
| `solar_system_epoch` | instant | Epoch at which state vectors are valid. Must be ≤ `game_epoch`. Principia integrates forward from here. |

**Epoch note**: `solar_system_epoch` is the JPL data reference epoch; `game_epoch` is the RSS/Sol game start date. Principia pre-integrates the gap at load time.

### `body` node keys

| Key | Type | Required | Notes |
|---|---|---|---|
| `name` | string | Yes | Must match KSP body name |
| `x`, `y`, `z` | quantity (length) | Yes | Position in barycentric inertial frame |
| `vx`, `vy`, `vz` | quantity (length/time) | Yes | Velocity in barycentric inertial frame |

**Coordinate frame**: Barycentric inertial frame, axes aligned to Unity world frame, origin at solar system barycentre.

### Example

```cfg
principia_initial_state:NEEDS[RealSolarSystem] {
  game_epoch         = JD2433647.5
  solar_system_epoch = JD2433282.500000000
  body {
    name = Earth
    x    = -2.720318042296709e+07 km
    y    = +1.329407956490104e+08 km
    z    = +5.764165538717468e+07 km
    vx   = -2.975363625990147e+01 km/s
    vy   = -5.189341029926219e+00 km/s
    vz   = -2.251484908750744e+00 km/s
  }
}
```

---

## `principia_numerics_blueprint`

Controls numerical integration algorithms. Optional — Principia uses compiled-in defaults if absent.

### Structure

```cfg
principia_numerics_blueprint {
  downsampling {
    tolerance = 10 m
  }
  ephemeris {
    fixed_step_size_integrator = QUINLAN_TREMAINE_1990_ORDER_12
    integration_step_size      = 10 min
    fitting_tolerance          = 1 mm
    geopotential_tolerance     = 0x1.0p-24
  }
  history {
    fixed_step_size_integrator = QUINLAN_1999_ORDER_8A
    integration_step_size      = 10 s
  }
  psychohistory {
    adaptive_step_size_integrator = DORMAND_ELMIKKAWY_PRINCE_1986_RKN_434FM
    length_integration_tolerance  = 1 mm
    speed_integration_tolerance   = 1 mm/s
  }
}
```

### Sub-nodes

- **`downsampling`**: `tolerance` (length) — max positional error for trajectory downsampling
- **`ephemeris`**: Background celestial-body integration
  - `fixed_step_size_integrator` — integrator name (see below)
  - `integration_step_size` — step size (`10 min` standard for RSS/Sol)
  - `fitting_tolerance` — accuracy for polynomial fitting
  - `geopotential_tolerance` — threshold for dropping harmonics (e.g. `0x1.0p-24`)
- **`history`**: Vessel past trajectory integrator
- **`psychohistory`**: Vessel future/prediction integrator (adaptive step)

### Supported integrators

**Symmetric Linear Multistep (recommended for ephemeris):**
- `QUINLAN_TREMAINE_1990_ORDER_8/10/12/14`
- `QUINLAN_1999_ORDER_8A` / `QUINLAN_1999_ORDER_8B`

**Symplectic Runge-Kutta-Nyström (SRKN):**
- `BLANES_MOAN_2002_SRKN_6B` / `_11B` / `_14A`

**Symplectic Partitioned Runge-Kutta (SPRK):**
- `MCLACHLAN_1995_SB3A_4` / `_5`
- `MCLACHLAN_ATELA_1992_ORDER_4_OPTIMAL` / `ORDER_5_OPTIMAL`
- `OKUNBOR_SKEEL_1994_ORDER_6_METHOD_13`

**Adaptive (psychohistory only):**
- `DORMAND_ELMIKKAWY_PRINCE_1986_RKN_434FM`

---

## `principia_draw_styles`

```cfg
principia_draw_styles {
  history           { colour = #aa0000  style = solid  }
  prediction        { colour = #00ff00  style = dashed }
  flight_plan       { colour = #0000ff  style = faded  }
  burn              { colour = #ffff00  style = solid  }
  target_history    { colour = #ff8800  style = dashed }
  target_prediction { colour = #ff00ff  style = faded  }
}
```

- `colour`: HTML RGB hex (`#rrggbb`)
- `style`: `solid`, `dashed`, or `faded`

---

## `principia_override_version_check`

```cfg
principia_override_version_check {
  version = 1.12.5
  version = 1.12.4
}
```

Converts the fatal KSP version mismatch crash into a logged warning. Multiple `version` values allowed.

---

## Type Reference

### `quantity`

Format: `<number> <unit>` — number uses `strtod` syntax (supports scientific notation).

Examples: `3.986004e+14 m^3/s^2`, `-2.975 km/s`, `14.1844 deg / d`, `10 min`, `1 mm`, `0.5 au`

**ModuleManager math operators (`*=`, `+=`) do NOT work on quantity values.** Always supply the full computed value.

| Dimension | Supported units |
|---|---|
| Length | `μm`, `mm`, `cm`, `m`, `km`, `au` |
| Time | `ms`, `s`, `min`, `h`, `d` |
| Angle | `deg`, `°`, `rad` |
| Compound | `km^3/s^2`, `deg / d`, `km/s`, `m^3/s^2`, `m s^-1` |

### `instant` (Terrestrial Time)

| Format | Example |
|---|---|
| Julian Date | `JD2451545.000000000` |
| Modified Julian Date | `MJD51544.5` |
| ISO 8601 (TT) | `2000-01-01T12:00:00` |

J2000 = `JD2451545.0` = `2000-01-01T12:00:00` TT.

---

## Kopernicus Integration

### Body discovery

Principia discovers bodies from `FlightGlobals.Bodies` (populated by Kopernicus). It does **not** read Kopernicus `Body {}` nodes directly. The `name` in `body { name = X }` must match `CelestialBody.name` (= Kopernicus `Body { name = X }`), not `displayName`.

### Two initialization paths

**Path 1 — Cartesian (with `principia_initial_state`):**
- Uses `InsertCelestialAbsoluteCartesian()` for each body
- Both `principia_initial_state` and `principia_gravity_model` required
- Every body in `FlightGlobals.Bodies` must have entries in both nodes
- `gravitational_parameter` is required in every `body`
- Kopernicus Keplerian elements are ignored
- Mode: Sol-Configs, RealSolarSystem

**Path 2 — Keplerian fallback (no `principia_initial_state`):**
- Uses `InsertCelestialJacobiKeplerian()` for each body
- Uses KSP/Kopernicus orbital elements as osculating elements (Jacobi coordinates)
- `principia_gravity_model` is optional; supplements CelestialBody data
- `gravitational_parameter` optional (defaults to `body.gravParameter`)
- Mode: stock KSP, fictional planet packs
- **Interstellar bodies = Cartesian only — never Keplerian.** The adapter passes
  the orbit's *mean motion* (KSP period, computed with the stock parent-only μ),
  and Principia's Jacobi initialization re-derives the semimajor axis with
  μ_eff = Σ(inner chain) + own body. A body whose mass is not negligible next to
  its primary (a star around a star) silently inflates its orbit by
  (μ_eff/μ_parent)^(1/3) — measured ~6.3× for NearStars (2026-07-19, the "TS
  displacement" incident). The fork logs a warning when the inflation exceeds 1%
  (commit `9b2167ec7`); the fix is a `principia_initial_state` Cartesian patch
  for any system containing stellar-mass satellites.

### Stock KSP Jool system stabilization

Without `principia_initial_state`, Principia automatically applies `StabilizeKSP()` in Keplerian mode:
- Vall's and Tylo's mean motions shifted out of 1:2:4 resonance with Laythe
- Bop's orbit flipped retrograde

Applied in code, not CFG. Does not apply when `principia_initial_state` is present.

### Tidal locking

Principia forcibly sets `body.tidallyLocked = false` for all bodies. Tidally locked bodies must set `angular_frequency` to match their orbital period via `principia_gravity_model`.

---

## Practical Patterns

### Pattern 1: Fictional planet pack (Keplerian mode)

Only `principia_gravity_model` needed. No `principia_initial_state`. Principia derives positions from Kopernicus orbits.

```cfg
principia_gravity_model:NEEDS[MyPack] {
  body {
    name                    = MyStar
    gravitational_parameter = 1.8e+18 m^3/s^2
    axis_right_ascension    = -90 deg
    axis_declination        = 89.5 deg
    reference_angle         = 0 deg
    angular_frequency       = 2.1e-05 rad/s
  }
  body {
    name                    = MyPlanet
    gravitational_parameter = 4.5e+12 m^3/s^2
    axis_right_ascension    = -90 deg
    axis_declination        = 75.0 deg
  }
}
```

### Pattern 2: Patching an existing gravity model

```cfg
@principia_gravity_model:FOR[MyPack]:NEEDS[MyPack] {
  body {
    name                    = NewMoon
    gravitational_parameter = 8.5e+10 m^3/s^2
    axis_right_ascension    = 120 deg
    axis_declination        = -15.0 deg
  }
}
```

### Pattern 3: NearStars — Sol-Configs + RSS dual support

NearStars runs on top of Sol-Configs (ballisticfox). RSS compatibility is a future target — the Cartesian state vectors below are valid for both variants since they share the same `solar_system_epoch` and `game_epoch`. Sol-Configs (and eventually RSS) ships its own `principia_gravity_model` and `principia_initial_state`, so NearStars only patches in its own bodies.

**Epoch reference:**

| Variant | `solar_system_epoch` | `game_epoch` | NEEDS tag |
|---|---|---|---|
| Sol real scale | JD2433282.5 (1950-Jan-01) | JD2433647.5 (1951-Jan-01) | `SolSystem,!SolQuarterScale` |
| Sol quarter scale | JD2433465.0 | — | `SolSystem,SolQuarterScale` |
| RSS | JD2433282.5 (1950-Jan-01) | JD2433647.5 (1951-Jan-01) | `RSSConfig` |

Sol real-scale and RSS share identical epochs → same Cartesian coords usable for both.  
Sol quarter-scale has a different `solar_system_epoch` → needs separate coords.

**gravity_model**: gravitational parameters are scale-independent → one patch per solar system mod (2 total).  
**initial_state**: epoch differs per scale → 3 patches total.

```cfg
// gravity model — Sol (all scales)
@principia_gravity_model:NEEDS[NearStarsSystem,SolSystem] {
  body { name = AlphaCentauriA  gravitational_parameter = ...  axis_right_ascension = ...  axis_declination = ... }
  // ... all NearStars bodies
}

// gravity model — RSS
@principia_gravity_model:NEEDS[NearStarsSystem,RSSConfig] {
  body { name = AlphaCentauriA  gravitational_parameter = ...  axis_right_ascension = ...  axis_declination = ... }
  // ... all NearStars bodies (same values — duplication unavoidable with MM)
}

// initial state — Sol real scale (solar_system_epoch = JD2433282.5)
@principia_initial_state:NEEDS[NearStarsSystem,SolSystem,!SolQuarterScale] {
  body { name = AlphaCentauriA  x = ...  y = ...  z = ...  vx = ...  vy = ...  vz = ... }
  // ... all NearStars bodies
}

// initial state — RSS (solar_system_epoch = JD2433282.5, same coords as Sol real)
@principia_initial_state:NEEDS[NearStarsSystem,RSSConfig] {
  body { name = AlphaCentauriA  x = ...  y = ...  z = ...  vx = ...  vy = ...  vz = ... }
  // ... all NearStars bodies
}

// initial state — Sol quarter scale (solar_system_epoch = JD2433465.0, different coords)
@principia_initial_state:NEEDS[NearStarsSystem,SolSystem,SolQuarterScale] {
  body { name = AlphaCentauriA  x = ...  y = ...  z = ...  vx = ...  vy = ...  vz = ... }
  // ... all NearStars bodies
}
```

**Coordinate values**: `x/y/z` = physical distance from Sol barycentre (parsecs → km). `vx/vy/vz` = proper motion + radial velocity in barycentric frame (km/s). At stellar distances, gravitational influence on the Sol system is negligible — the entries exist solely to satisfy Principia's consistency check.

---

## Key Constraints

1. At most one of each top-level node after ModuleManager processing.
2. If `principia_initial_state` is present → `principia_gravity_model` is mandatory and must cover every body in `FlightGlobals.Bodies`.
3. If `principia_initial_state` is present → `gravitational_parameter` is required in every `body` of `principia_gravity_model`.
4. `j2` and `geopotential_row` are mutually exclusive on the same body.
5. `reference_radius` is required if and only if `j2` or any `geopotential_row` is present.
6. ModuleManager math operators (`*=`, `+=`) do not work on `quantity` values.
7. Body `name` must match `CelestialBody.name`, not `displayName`.
8. `solar_system_epoch` ≤ `game_epoch`.

---

## IAU Nominal Unit Constants

Used in Principia's TRAPPIST configs as unit shorthand:

| Symbol | Value |
|---|---|
| `GM☉` | 1.327124400419394e+20 m³/s² |
| `GM🜨` | 3.986004e+14 m³/s² |

---

## Shipped File Locations (Principia repo)

| Source path | Loaded when |
|---|---|
| `astronomy/sol_gravity_model.cfg` | `:NEEDS[RealSolarSystem]` |
| `astronomy/sol_initial_state_jd_2433282_500000000.cfg` | `:NEEDS[RealSolarSystem]` |
| `astronomy/sol_numerics_blueprint.cfg` | `:NEEDS[RealSolarSystem]` |

Sol-Configs ships its own `Real_Sol-GravityModel.cfg`, `Real_Sol-InitialState.cfg`, `Quarter_Sol-GravityModel.cfg`, `Quarter_Sol-InitialState.cfg` with `:FOR[SolSystem]`.

## Related

- [principia-geopotential-data](principia-geopotential-data.md) — the **real geopotential values** Principia ships for each Solar System body (Sun, giants, Earth/Mars/Moon), verbatim, with the proto↔cfg mapping + how to write a gas giant like Polyphemus
- [methodology](methodology.md) — DB-side schema that feeds gravitational_parameter, mass, radius into Principia
- [binary-epoch-pipeline](binary-epoch-pipeline.md) — the Cartesian state vectors produced by §9–11 of that doc feed `principia_initial_state` body blocks here
- [mod-reference](mod-reference.md) — Principia install and dependency tier
- [mod-release-layout](mod-release-layout.md) — §2.1 covers how Principia patches are placed in `Patches/Principia/`
- [alpha-centauri-a](../phase3/alpha-centauri-a.md), [alpha-centauri-b](../phase3/alpha-centauri-b.md) — the canonical worked example downstream of Principia's per-body gravity model
