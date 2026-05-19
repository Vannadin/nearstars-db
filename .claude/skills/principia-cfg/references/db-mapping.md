# DB → Principia cfg Field Mapping

DB layout reference: `db/systems/<system>.json` produced by `scripts/pipeline/build_systems.py`. Each system file has a `stars[]` array; this skill emits one Principia `body { }` per element.

---

## `body.name`

Resolution order:
1. `stars[].kopernicus_body_name` — if present and non-null, use verbatim.
2. Fallback: normalize `stars[].name`:
   - split on whitespace into tokens
   - within each token, drop characters that are not `[A-Za-z0-9]`
   - if a token contains **any** uppercase letter, keep it as-is
   - if a token is entirely lowercase, capitalize the first letter only
   - concatenate the tokens

   This rule preserves all-uppercase catalog prefixes (`GJ`, `HD`, `HIP`, `TOI`, `TRAPPIST`) and recovers from sloppy DB casing (`Barnard's star` → `BarnardsStar`, `eps Eri` → `EpsEri`).

Examples (fallback rule):

| DB `stars[].name` | Emitted `body.name` |
|---|---|
| `Alpha Centauri A` | `AlphaCentauriA` |
| `Proxima Centauri` | `ProximaCentauri` |
| `Barnard's star` | `BarnardsStar` |
| `AU Mic` | `AUMic` |
| `eps Eri` | `EpsEri` |
| `tau Cet` | `TauCet` |
| `GJ 1002` | `GJ1002` |
| `HD 219134` | `HD219134` |
| `TRAPPIST-1` | `TRAPPIST1` |
| `Chi-1 Orionis A` | `Chi1OrionisA` |
| `Van Maanen's Star` | `VanMaanensStar` |
| `61 Cygni A` | `61CygniA` |
| `40 Eridani C` | `40EridaniC` |
| `L 363-38` | `L36338` |

Limits of the fallback:

- `eps Eri` → `EpsEri`. If a Kopernicus body uses `EpsilonEridani` instead, set `kopernicus_body_name = "EpsilonEridani"` on the star.
- `L 363-38` → `L36338`. Hyphen drop merges `363` + `38`. Disambiguate via override if another DB star would normalize the same.

**Hard rule**: this name must equal the body's Kopernicus `Body { name = X }`. Mismatch = Principia silently ignores the entry. If a system's Kopernicus name diverges from the fallback rule, add `kopernicus_body_name` to the star entry.

Leading-digit names (`61CygniA`, `40EridaniC`) are legal both in Kopernicus and Principia; the parsers don't tokenize identifiers as code symbols.

---

## `body.gravitational_parameter`

| Source | Target | Conversion | Unit literal |
|---|---|---|---|
| `stars[].principia.gravitational_parameter_km3_s2` | `body.gravitational_parameter` | none (DB is already in km³/s²) | ` km^3/s^2` (note the caret, Principia syntax) |

Format: scientific notation, 15 significant digits (Python `repr(float)` defaults are fine). Example: `1.46713602439899e+11 km^3/s^2`.

**Abort condition**: if `principia.gravitational_parameter_km3_s2` is `null` or missing, the script aborts the entire emit (not just that body) — gravity_model coverage must be 100% when `principia_initial_state` is present.

---

## `body.x`, `body.y`, `body.z`

| Source | Target | Conversion |
|---|---|---|
| `stars[].derived.icrs_x_km` | `body.x` | append ` km` |
| `stars[].derived.icrs_y_km` | `body.y` | append ` km` |
| `stars[].derived.icrs_z_km` | `body.z` | append ` km` |

Note the **non-J2000** fields are used. `derived.icrs_x_j2000_km` etc. exist for a different downstream consumer; for Sol-real-scale `solar_system_epoch = JD 2433282.5`, the matching set is `icrs_x_km` (no `_j2000` suffix), which the pipeline has already propagated to that epoch.

---

## `body.vx`, `body.vy`, `body.vz`

| Source | Target | Conversion |
|---|---|---|
| `stars[].derived.icrs_vx_km_s` | `body.vx` | append ` km/s` |
| `stars[].derived.icrs_vy_km_s` | `body.vy` | append ` km/s` |
| `stars[].derived.icrs_vz_km_s` | `body.vz` | append ` km/s` |

Same epoch as position. Includes proper motion + radial velocity + Kepler/Thiele-Innes orbital contribution (for binaries).

---

## Pre-emit validation (script must enforce)

For every system file:

| Check | Action on failure |
|---|---|
| `meta.solar_system_epoch_jd == 2433282.5` | abort |
| every `stars[].derived.epoch_jd == 2433282.5` | abort |
| every `stars[].principia.gravitational_parameter_km3_s2` is finite | abort |
| every `stars[].derived.icrs_{x,y,z}_km` is finite | abort |
| every `stars[].derived.icrs_v{x,y,z}_km_s` is finite | abort |
| `planets` array is empty | warn; continue (MVP scope — see planet-contract.md) |

"Abort" means: write nothing, exit non-zero, name the offending file and field. Partial emits are worse than no emit, because users won't notice the gap until KSP load.

---

## Ordering

Within each top-level patch, sort `body { }` blocks alphabetically by emitted `body.name`. Reasons:

- Deterministic diffs across pipeline runs.
- Easy visual cross-check between `gravity_model` and `initial_state` (same order, same names).
- Stable git blame.

Do NOT group by system — alphabetical-by-body-name is the only sort key.
