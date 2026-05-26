# Kopernicus emitter — plan

Started 2026-05-26 (handoff workspace). Build the Phase 3 → Kopernicus
cfg emitter following the pattern established by emit_principia_cfg.py
and emit_firefly_cfg.py.

## Goal

Generate `dist/NearStars-Configs/Patches/Kopernicus/<system>.cfg` for
every system in `db/systems/` whose body has a Phase 3 synthesis. The
emitter is deterministic and idempotent — same inputs → byte-identical
output. New systems require no Python.

## Why now

After Firefly, Kopernicus is the next major cfg layer needed to ship
NearStars. Currently the `kopernicus-cfg` skill teaches manual cfg
authoring via 1845 lines of `references/*.md` prose templates. With
223 planets in the DB, hand-writing each is unmaintainable. The emitter
replaces that with template strings + structured Phase 3 inputs.

## Architecture decision: sidecar yaml, not prose extraction

(See context-notes.md for the full reasoning.)

The hard part of Kopernicus cfg is that some fields (PQS terrain
parameters, biome layout, ring system, ScaledVersion material specifics)
aren't in the Phase 3 Decisions table — they're either prose
description in `## Surface` / `## Visual` sections, or not in Phase 3
at all (cfg-internal aesthetic decisions).

**Strategy:**
- **Mechanical fields** (Properties, Orbit, base ScaledVersion, Atmosphere
  pressure/temperature curves, AmbientColor) — derived from
  `db/systems/<system>.json` (mass, radius, orbital elements) +
  `docs/phase3/<slug>.md` Decisions table fields directly.
- **Cfg-only structured fields** (terrain class, ring system, biome
  count, etc.) — `phase3/<system>/kopernicus_extras.yaml` sidecar.
  Empty/absent → sensible defaults. Override only when Phase 3 prose
  intent diverges from defaults.
- **No LLM at emit time.** The emitter is pure Python. Prose
  interpretation, if needed, happens during Phase 3 curation (writer
  decides terrain_class, fills sidecar) — not at cfg emit time.

## Inputs / outputs

```
emit_kopernicus_cfg.py <system_slug>   (or all systems if no arg)

inputs:
  db/systems/<system>.json              ← mass/radius/orbital/distance
  docs/phase3/<planet_slug>.md          ← Decisions table per planet
  phase3/<system>/kopernicus_extras.yaml  ← optional cfg-only overrides

outputs:
  dist/NearStars-Configs/Patches/Kopernicus/<system>.cfg
```

## Scope

**In-scope:**
- Star bodies (Sun template) — currently MVP for principia, extend here
- Rocky planet bodies (Mun / Kerbin templates)
- Gas giant bodies (Jool template + ScaledVersion.type=Atmospheric)
- Atmosphere node generation from Phase 3 pressure/temperature
- ScaledVersion material color from Phase 3 `atmosphere_tint_rgb_hex` /
  surface synthesis
- AtmosphereFromGround color from bulk_gas (reuses Firefly palette)
- Orbit node from db/systems orbital block

**Out-of-scope MVP:**
- PQS terrain heightmap generation — `vertexHeightMapBicubic` requires
  external image assets; emitter just emits the cfg reference, asset
  generation is separate work
- VertexColorMap detailed authoring — needs per-body texture art
- Ring textures — only emit ring node skeleton if `ring_present: true`
- Biome map — emit a single default biome unless sidecar specifies
- Ocean detail (FallbackMaterial, HazardousOcean) — emit if Phase 3
  `ocean_extent_substellar_radius_deg > 0`, defaults otherwise
- Hazardous surface (lava, radiation belts) — defer

## Acceptance criteria (MVP)

- emit_kopernicus_cfg.py runs against alpha_centauri_proxima + trappist_1
  without erroring
- Output cfg passes Module Manager syntax (`@Kopernicus:FOR[NearStarsSystem]`
  header + node structure)
- Star bodies emit Properties.gravParameter + Properties.radius +
  ScaledVersion.material.color
- Planet bodies emit Properties + Orbit + ScaledVersion.type matching
  atmosphere_present + Atmosphere node (if present) + bare PQS reference
- Stub `kopernicus_extras.yaml` for trappist_1 demonstrates the sidecar
  schema in action

## Dependencies

- The Phase 3 → Firefly emitter for `pick_palette()` reuse (atmosphere
  → bulk-gas palette mapping is identical for AtmosphereFromGround)
- `db/refs/element_plasma_colors.yaml` for trace-species accents in
  ScaledVersion material (where applicable)
- `kopernicus-cfg` skill's `references/*.md` templates as base text

## Related

- [checklist](checklist.md) — concrete next-session steps
- [context-notes](context-notes.md) — design decisions + open questions
- [kopernicus-cfg skill](../../.claude/skills/kopernicus-cfg/SKILL.md) — current manual-authoring procedure (will be augmented, not replaced — emitter handles common case, skill handles edge cases)
- [emit_principia_cfg.py](../../.claude/skills/principia-cfg/scripts/emit_principia_cfg.py) — reference implementation
- [emit_firefly_cfg.py](../../.claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py) — reference implementation
