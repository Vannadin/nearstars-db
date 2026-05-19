# Principia Node Reference (subset used by NearStars)

Full reference: [`docs/reference/principia-cfg-reference.md`](../../../../docs/reference/principia-cfg-reference.md).
This file only covers the nodes the NearStars MVP emits.

---

## `principia_gravity_model`

Patch shape NearStars emits (one big patch, all stars inside):

```cfg
@principia_gravity_model:NEEDS[NearStarsSystem,SolSystem]
{
    body { name = ...  gravitational_parameter = ... }
    body { name = ...  gravitational_parameter = ... }
    ...
}
```

### `body { }` keys actually used

| Key | Type | Required for NearStars stars |
|---|---|---|
| `name` | string | yes — must match Kopernicus `Body { name = X }` |
| `gravitational_parameter` | `<num> km^3/s^2` | yes — `principia_initial_state` is present, so every body must declare it |

### Keys we deliberately **omit** (defaults are fine)

| Omitted key | Default Principia applies | Why we don't override |
|---|---|---|
| `reference_instant` | `JD2451545.000000000` (J2000) | rotational pole is omitted too — instant is moot |
| `axis_right_ascension` | `-90 deg` | aligns pole with KSP world frame; cosmetic only for stars at LY distance |
| `axis_declination` | `90 deg` | same |
| `reference_angle` | KSP `initialRotation` | no measured W₀ data |
| `angular_frequency` | KSP `angularV` | Kopernicus body already declares this |
| `reference_radius` | — | NOT set ⇒ must not set `j2` / `geopotential_row` either |
| `j2`, `geopotential_row` | — | DB has no zonal-harmonics measurements for nearby stars |

If anyone later adds rotation pole or J₂ measurements, extend `references/db-mapping.md` first, then this table.

---

## `principia_initial_state`

```cfg
@principia_initial_state:NEEDS[NearStarsSystem,SolSystem,!SolQuarterScale]
{
    body
    {
        name = AlphaCentauriA
        x    = -1.5527351120891346e+13 km
        y    = -1.3030087085895514e+13 km
        z    = -3.6336848257786305e+13 km
        vx   = -1.3086466445996077e+01 km/s
        vy   = +2.0146595841415063e+01 km/s
        vz   = +1.4851844455108127e+01 km/s
    }
    ...
}
```

### `body { }` keys

| Key | Type | Required |
|---|---|---|
| `name` | string | yes |
| `x`, `y`, `z` | `<num> km` | yes — barycentric inertial frame, axes ≡ ICRF |
| `vx`, `vy`, `vz` | `<num> km/s` | yes |

### Frame & epoch

- **Frame**: Principia calls it "Barycentric inertial frame, axes aligned to Unity world frame, origin at solar-system barycentre." In practice the project treats this as ICRF — Sol-Configs and HORIZONS use the same convention.
- **Epoch**: implicit. Comes from the root `principia_initial_state.solar_system_epoch` Sol-Configs ships (= `JD 2433282.5` at Sol real scale). Every body in the patch must be valid at that epoch.
- DB field `stars[].derived.epoch_jd` MUST equal `2433282.5` before we emit. The pipeline already ensures this; the script asserts as a guard.

### Why we do NOT set `solar_system_epoch` / `game_epoch` in the patch

The root node already declares them. `principia_initial_state` is constrained to **at most one** instance after ModuleManager processing — re-declaring `solar_system_epoch` inside an `@` patch overwrites it, which is dangerous and unnecessary.

---

## Top-level nodes we do NOT emit

| Node | Why omitted |
|---|---|
| `principia_numerics_blueprint` | Sol-Configs / RSS provide their own |
| `principia_draw_styles` | UX preference, not body-pack concern |
| `principia_override_version_check` | Not the planet pack's responsibility |
