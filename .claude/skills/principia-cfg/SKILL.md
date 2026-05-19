---
name: principia-cfg
description: >
  Write and review Principia .cfg files for the NearStars KSP planet pack.
  Use this skill when the user wants to generate, patch, or debug a Principia
  config for NearStars bodies — including requests like "Principia cfg
  만들어줘", "이 별 principia에 등록", "gravity_model 작성", "initial_state
  생성", "n-body cfg 빌드", "write a principia cfg", or "generate principia
  patches from the DB". Reads `db/systems/*.json` (no Keplerian-fallback
  guessing), emits combined per-variant patch files under `dist/Principia/`.
  NearStars-specific decisions (epoch, NEEDS tags, body-name convention,
  Sol-real-scale-only MVP) are pre-set — do not ask the user about them.
---

# Principia CFG Writing Guide

NearStars rides on top of **Sol-Configs (ballisticfox)** or **RSS**. Both
ship their own `principia_gravity_model` and `principia_initial_state`,
so NearStars only **patches** in its own bodies.

Source references:
- **Principia source**: `mockingbirdnest/Principia` — `astronomy/*.cfg`
- **Sol-Configs example**: `RSS-Reborn/Sol-Configs` — `Patches/Principia/`
- **Project-internal reference**: [`docs/reference/principia-cfg-reference.md`](../../../docs/reference/principia-cfg-reference.md)
- **Binary epoch math (already executed in pipeline)**: [`docs/reference/binary-epoch-pipeline.md`](../../../docs/reference/binary-epoch-pipeline.md)

---

## 1. When to Use vs. Defer

| Request | This skill? |
|---|---|
| "Generate Principia cfg from the DB" | ✅ yes |
| "Add this star to Principia" (after DB entry exists) | ✅ yes |
| "Add a new star to NearStars" (no DB entry yet) | ❌ run `nearstars-add-star` first, then this skill |
| "Write Kopernicus body for X" | ❌ that's `kopernicus-cfg` |
| "Compute ICRS state vector for a binary" | ❌ the pipeline already does this — `stars[].derived.icrs_*` |

---

## 2. MVP Scope (do not exceed without user approval)

| Setting | Decision |
|---|---|
| Variants covered | **Sol real scale only** (`:NEEDS[NearStarsSystem,SolSystem,!SolQuarterScale]`) |
| Bodies covered | **Stars only** — planets blocked with a clear message |
| Files emitted | `dist/Principia/Real_NearStars-GravityModel.cfg`, `dist/Principia/Real_NearStars-InitialState.cfg` |
| `solar_system_epoch` | `JD 2433282.5` (1950-Jan-01) — must equal `stars[].derived.epoch_jd` |
| `game_epoch` | `JD 2433647.5` (1951-Jan-01) |
| Body-name convention | CamelCase, alphanumerics only — matches Kopernicus (see [`references/db-mapping.md`](references/db-mapping.md)) |
| Rotational pole (RA/Dec) | omitted → Principia default `-90 / 90 deg` (aligned with KSP frame) |
| `reference_radius`, `j2`, `geopotential_row` | omitted — DB has no measured zonal harmonics |

Quarter-scale and RSS variants, planet bodies, and per-star rotation poles
are out of scope for the MVP. See [`references/planet-contract.md`](references/planet-contract.md) for the
forward path when a planet system is upgraded to Phase 2.

---

## 3. Default Workflow

```
1. Pre-flight     ← validate DB has icrs_* and gravitational_parameter_km3_s2
                    for every star in every system; abort early if not
2. Emit            ← scripts/emit_principia_cfg.py
                    reads db/systems/*.json → writes 2 cfg files
3. Eyeball         ← spot-check 1–2 body blocks for sane numbers
4. Report          ← list bodies emitted, files written, any skipped systems
```

The script is deterministic and idempotent. If the DB hasn't changed, the
output is byte-identical.

Run from project root:

```sh
python3 .claude/skills/principia-cfg/scripts/emit_principia_cfg.py
```

Flags:
- `--dry-run` — print to stdout, don't write files.
- `--system <stem>` — limit to the named DB file stems (repeatable, e.g. `--system alpha_centauri_a --system alpha_centauri_b`). Output is still in combined-file shape.

The script always errors out (exit 2) if any star in the selected set is missing required Principia fields (`gravitational_parameter_km3_s2`, `derived.icrs_*`). All errors are reported in one batch — fix everything the report lists, then re-run.

---

## 4. DB → cfg Field Mapping (Star Bodies)

Full table in [`references/db-mapping.md`](references/db-mapping.md). Summary:

| cfg field | JSON path | Conversion |
|---|---|---|
| `body.name` | `stars[].kopernicus_body_name` (if present) else normalized `stars[].name` | CamelCase, strip non-alphanum |
| `body.gravitational_parameter` | `stars[].principia.gravitational_parameter_km3_s2` | append ` km^3/s^2` |
| `body.x / y / z` | `stars[].derived.icrs_x_km / y / z` | append ` km` |
| `body.vx / vy / vz` | `stars[].derived.icrs_vx_km_s / vy / vz` | append ` km/s` |

Required preconditions (script aborts if any fail):
- `meta.solar_system_epoch_jd == 2433282.5`
- `stars[].derived.epoch_jd == 2433282.5`
- `stars[].derived.icrs_x_km` is not null (same for y, z, vx, vy, vz)
- `stars[].principia.gravitational_parameter_km3_s2` is not null

---

## 5. NearStars-Specific cfg Pattern

```cfg
@principia_gravity_model:NEEDS[NearStarsSystem,SolSystem]
{
    body
    {
        name                    = AlphaCentauriA
        gravitational_parameter = 1.46713602439899e+11 km^3/s^2
    }
    // ... one body per star, sorted by system then component
}

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
    // ... one body per star, same order as gravity_model
}
```

- No `@` author tag (`:FOR[NearStarsSystem]`) — Sol-Configs is the author of
  the root node; we only patch.
- No `solar_system_epoch` / `game_epoch` in the patch — those live on the
  root node Sol-Configs ships. Patching them would create a duplicate.
- Body ordering: alphabetical by Kopernicus body name. Stable diffs.

Pitfalls (always read before debugging): [`references/pitfalls.md`](references/pitfalls.md)

Node-by-node syntax: [`references/nodes.md`](references/nodes.md)

Output file layout & NEEDS-tag rationale: [`references/file-layout.md`](references/file-layout.md)
