# TRAPPIST-1 b — Firefly cfg decision: SKIP

Per SKILL.md Step 0 (Confirm Firefly cfg is appropriate), no
`ATMOFX_BODY` is emitted for `Trappist1b`.

## Phase 3 inputs (from `docs/phase3/trappist-1-b.md` Decisions table)

| Field | Value | Confidence |
|---|---|---|
| `atmosphere_present` | false | high |
| `atmosphere_surface_pressure_pa` | 0 | high |
| `atmosphere_composition` | n/a (airless) | high |
| `atmosphere_scale_height_km` | n/a | high |
| `aurora_present` | false | high |

## Rule applied

SKILL.md §3 Step 0:

> Skip Firefly cfg entirely if:
> - `atmosphere_present = false` → no `ATMOFX_BODY` written.

The first bullet fires unambiguously. The second bullet
(`atmosphere_pressure_pa < 100 Pa`) would also fire (pressure = 0 Pa),
but the first criterion already terminates the workflow.

## Override check

The Phase 3 synthesis does not declare any `atmofx_*_hex_intensity`
override fields (SKILL.md Step 1 / phase3-mapping §2), and explicitly
states under Visual styling:

> **No atmosphere haze.** Limb is sharp — no scattering, no
> refraction, no glow. The transition from disk to space is a clean
> edge.

No "thin reentry plasma desired" flag is present. No override path
applies.

## Pack-membership consequence

Because `Trappist1b` has no `ATMOFX_BODY`, it must NOT be listed in
the NearStars `ATMOFX_PLANET_PACK:NEEDS[NearStarsSystem]` node's
`affected_bodies` list. (Pack membership only covers atmosphere-
bearing bodies — SKILL.md §3 Step 7.)

## References consulted

- `draft/SKILL.md` §3 Step 0 (skip criteria) and §2 (NearStars-fixed
  decisions).
- No `references/*.md` files were needed; the Step 0 decision is
  resolved entirely from the Phase 3 Decisions table.
