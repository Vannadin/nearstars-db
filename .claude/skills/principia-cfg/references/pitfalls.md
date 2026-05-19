# Pitfalls

Common Principia-cfg mistakes, ordered by how often they hit. Read this before debugging.

---

## 1. Body name mismatch with Kopernicus → silent skip

Principia matches by `CelestialBody.name`, not `displayName`. If Kopernicus declares `Body { name = AlphaCenA }` and Principia patches `body { name = AlphaCentauriA }`, Principia silently drops the entry. Then `principia_initial_state` is missing a body → crash at load.

**Detection**: check Principia log lines `Inserted ... at ...`. If a body you expect isn't there, the name is wrong.

**Project rule**: the same normalization (`stars[].name` → strip non-alphanum, keep case) is used by both Kopernicus and Principia emitters. Use `kopernicus_body_name` to override if needed.

---

## 2. Patching `solar_system_epoch` or `game_epoch`

Sol-Configs's root `principia_initial_state` already declares these. Re-declaring them inside `@principia_initial_state:NEEDS[...]` either overrides (bad — silently changes simulation epoch) or, in some MM versions, creates a parse error.

**Rule**: NearStars patches contain only `body { }` blocks. No `solar_system_epoch =`, no `game_epoch =`.

---

## 3. Wrong unit literal

| Wrong | Right | Why |
|---|---|---|
| `gravitational_parameter = 1.32e+20 m3/s2` | `1.32e+20 m^3/s^2` | Principia parses `^`; without it the value is rejected |
| `x = 1.5e+13` (no unit) | `x = 1.5e+13 km` | Principia requires a unit |
| `vx = 13.08 km s-1` | `vx = 13.08 km/s` or `13.08 m s^-1` | Use either compound form, but always include `/` for per-unit |

The script emits `km^3/s^2`, `km`, `km/s` consistently — do not hand-edit to "fix formatting."

---

## 4. ModuleManager math on quantities

`gravitational_parameter *= 1.5` does **not** work. Principia parses the value as a quantity; MM's `*=` operator doesn't dimension-check. Always emit the fully computed value.

This is why the DB stores `gravitational_parameter_km3_s2` as a pre-computed float, not a formula.

---

## 5. Missing body in `principia_gravity_model` when `initial_state` is present

If `principia_initial_state` is present, every body in `FlightGlobals.Bodies` (i.e., every Kopernicus body) must have:
- a `body { }` block in `principia_initial_state`, AND
- a `body { }` block in `principia_gravity_model` with a `gravitational_parameter`.

The script emits both files from the same body list, so they stay in sync. Do not hand-edit just one.

---

## 6. Epoch mismatch between DB and patch

The DB's `derived.icrs_*` are propagated to `solar_system_epoch = JD 2433282.5` (Sol real scale). If a system's `derived.epoch_jd` is anything else, the patch is inconsistent with Sol-Configs's root.

**Script guard**: aborts emit if `meta.solar_system_epoch_jd != 2433282.5` or any `stars[].derived.epoch_jd != 2433282.5`.

If a user manually re-runs the pipeline at a different epoch, this guard catches it.

---

## 7. `tidallyLocked` reset

Principia forcibly sets `body.tidallyLocked = false` for all bodies. Tidally locked moons rely on `angular_frequency` in `principia_gravity_model` to keep their face pointed at the parent.

Not relevant for the MVP (stars only), but flag this when planets land — Proxima b et al. are tidally locked in reality and KSP players will expect the visual to match.

---

## 8. Confusing `icrs_x_km` vs `icrs_x_j2000_km`

The DB has both:
- `derived.icrs_x_km` — propagated to `solar_system_epoch = JD 2433282.5` (B1950) — **this is what we emit**
- `derived.icrs_x_j2000_km` — at J2000 — for a different downstream consumer (e.g., visualization tooling)

Sourcing the wrong field shifts every body by tens of AU. The script only reads the non-J2000 set; the J2000 fields are documented but unused here.

---

## 9. Coordinate-frame mislabeling

Principia documents the frame as "Barycentric inertial, axes aligned to Unity world frame, origin at SSB." The project treats this as ICRF in practice — Sol-Configs and HORIZONS use ICRF Cartesian and Principia accepts them without rotation.

If a future contributor adds a "rotate from ICRF to KSP frame" step here, stop — that's almost certainly wrong. The convention is unrotated.

---

## 10. Bodies missing from one file but not the other

If `principia_gravity_model` lists `AlphaCentauriA` and `principia_initial_state` lists `AlphaCenA` (typo), Principia rejects the entry from `initial_state`, sees the body has Kopernicus data but no Cartesian state, and refuses to start.

**Script invariant**: both files iterate the same in-memory list of `(body_name, ...)` tuples, sorted by `body_name`. A diff between the two files should only differ in node syntax, never in body coverage.
