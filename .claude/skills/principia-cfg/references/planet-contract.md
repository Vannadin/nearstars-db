# Planet Support — Forward Contract

The MVP emits star bodies only. This file describes what needs to land in the DB before planet bodies can be added to `principia_initial_state`, and the chain of decisions that follow.

---

## Why planets are not emitted today

Principia's rule (`docs/reference/principia-cfg-reference.md`, Key Constraints §2):

> If `principia_initial_state` is present → `principia_gravity_model` is mandatory and must cover **every body** in `FlightGlobals.Bodies`.

If NearStars ships planets via Kopernicus but its `principia_initial_state` patch only lists stars, Principia will reject the configuration at load: the planet body exists in `FlightGlobals.Bodies` but has no entry in `principia_initial_state`. KSP crashes during Principia init.

**Status update (2026-07-20).** The MVP-era claim "`planets[]` is empty in every
system file" is obsolete: 123 of 157 system files now carry a top-level
`planets[]` array (siblings to `stars[]`, 229 planets, names like
`Proxima Cen b`), but each planet's `kopernicus`/`principia` blocks are still
empty — so the emit-script guard below now fires silently on every planet-bearing
system while the data to satisfy this contract is absent. Populating
`planets[].derived.icrs_*` + `planets[].principia.*` (the plan in "Implementation
order" below) is a prerequisite of emit wiring; the flow-level accounting lives in
[`docs/reference/pipeline-contract.md`](../../../../docs/reference/pipeline-contract.md).

**Guard**: the emit script warns (does not abort) when a planet lacks the
required blocks, so the operator is reminded that this contract is active.

---

## What the DB needs to provide

For every planet that will be added to a `principia_initial_state` patch, the DB must provide an ICRF Cartesian state at the matching `solar_system_epoch`. Proposed schema additions:

```json
{
  "planets": [
    {
      "name": "Proxima b",
      "raw": { ... existing fields ... },
      "kopernicus": { ... existing fields ... },
      "derived": {
        "epoch_jd": 2433282.5,
        "icrs_x_km": -1.5527351e+13,
        "icrs_y_km": -1.3030087e+13,
        "icrs_z_km": -3.6336848e+13,
        "icrs_vx_km_s": -1.30864e+01,
        "icrs_vy_km_s": +2.01465e+01,
        "icrs_vz_km_s": +1.48518e+01
      },
      "principia": {
        "gravitational_parameter_km3_s2": 3.986e+05
      }
    }
  ]
}
```

Required fields (mirrors the star contract):

| Path | Notes |
|---|---|
| `planets[].derived.epoch_jd` | must equal `meta.solar_system_epoch_jd` (`2433282.5` for Sol real) |
| `planets[].derived.icrs_{x,y,z}_km` | barycentric (SSB), ICRF axes |
| `planets[].derived.icrs_v{x,y,z}_km_s` | same frame |
| `planets[].principia.gravitational_parameter_km3_s2` | required because `principia_initial_state` is present |

`kopernicus_body_name` resolution is identical to stars.

---

## Computation outline (for the pipeline extension when it lands)

Per planet:

1. Resolve the parent star (`planets[].parent_star` or Kopernicus `referenceBody`) and read its `derived.icrs_*` state at `solar_system_epoch`.
2. From `planets[].kopernicus.{semi_major_axis_m, eccentricity, inclination_deg, mean_anomaly_deg, longitude_of_ascending_node_deg, argument_of_periapsis_deg}`, solve Kepler at the epoch to get the relative perifocal state (`x_p, y_p, vx_p, vy_p`). Markley's method (PyAstronomy MarkleyKESolver) — same solver the binary-orbit pipeline already uses.
3. Rotate perifocal → some inertial frame. **This is the open question**: Kopernicus orbital elements are referenced to KSP's reference plane, which is **not** ICRF. Three options to evaluate when a real planet system reaches Phase 2:

   | Option | Description | Trade-off |
   |---|---|---|
   | A. Treat KSP frame ≡ ICRF for stars at ~LY distance | The star's orbital plane convention is irrelevant when its ICRF location is what matters. Use Kopernicus elements directly in the star's local ICRF frame. | Simple. Loses any star-axis-orientation realism, but stars at LY distance look like points anyway. |
   | B. Use catalog (RA/Dec of pole, system orientation) to build a per-star rotation matrix from KSP frame to ICRF | Physically correct. | Need pole RA/Dec per star — currently not in DB. |
   | C. Define a synthetic KSP-frame ↔ ICRF rotation that minimizes user-visible weirdness | Hand-tuned per system. | Maintenance burden grows with system count. |

   Default until decided: **option A**, with a documented caveat in the system file.
4. Translate by the star's `derived.icrs_*` to convert relative state to barycentric ICRF.
5. Write to `planets[].derived.icrs_*` in the DB.

---

## When to revisit this contract

Trigger conditions:
- A user starts Phase 2 (Policy C) curation for any system in `db/systems/` that has planets — see `feedback_planet_curation.md` in user memory.
- The user explicitly asks for a planet to appear in n-body simulation.

When triggered:
1. Decide between options A/B/C above.
2. Extend `scripts/pipeline/build_systems.py` (or a new pipeline stage) to compute and write `planets[].derived.icrs_*` and `planets[].principia.gravitational_parameter_km3_s2`.
3. Drop the script's planet-warn guard, replace it with the same hard-abort treatment stars get.
4. Update `db-mapping.md` with a planets section.
