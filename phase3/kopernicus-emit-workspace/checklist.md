# Kopernicus emitter — checklist

Concrete next-session steps. Each block is one commit's worth.

## Stage 1 — Schema + fixtures

- [ ] Design `phase3/<system>/kopernicus_extras.yaml` schema. Minimum
  shape (see context-notes for field list):
  - `<planet_slug>:`
    - `terrain_class:` enum (smooth | rocky | cratered | volcanic | icy | desert | gas_giant | ocean_world)
    - `pqs_color_low_hex:` optional
    - `pqs_color_high_hex:` optional
    - `ring_present:` bool, default false
    - `ring_inner_au:` float (if ring_present)
    - `ring_outer_au:` float (if ring_present)
    - `ring_color_hex:` string (if ring_present)
    - `biome_count:` int, default 1
    - `ocean_color_hex:` string (when Phase 3 declares ocean)
  - All fields optional except `terrain_class` (which defaults to `smooth`)
- [ ] Define enum mappings inline in the emitter — `terrain_class` →
  PQS preset dict (deformity, mountainAmplitude, craterCount, etc.)
- [ ] Write stub `phase3/trappist_1/kopernicus_extras.yaml` with
  realistic values for d/e/f/g/h based on existing Phase 3 syntheses

## Stage 2 — emit_kopernicus_cfg.py

- [ ] Write `.claude/skills/kopernicus-cfg/scripts/emit_kopernicus_cfg.py`
  - CLI: `python3 .../emit_kopernicus_cfg.py [<system_slug>] [--dry-run]`
  - Load db/systems/<slug>.json
  - Load docs/phase3/<planet>.md Decisions (reuse extract_decisions
    from Firefly emitter, factor out to common module if needed)
  - Load kopernicus_extras.yaml if present
  - Emit per-body cfg blocks:
    - Star: Properties + ScaledVersion (type=Star, Light, Coronas)
    - Rocky planet: Properties + Orbit + ScaledVersion + optional Atmosphere + PQS reference
    - Gas giant: similar but with ScaledVersion type=Atmospheric + Atmosphere
  - Output: `dist/NearStars-Configs/Patches/Kopernicus/<system_slug>.cfg`
- [ ] Strict validation: missing required fields → abort with batched
  error report (principia-cfg pattern)

## Stage 3 — Migration / verification

- [ ] Run against alpha_centauri_proxima → inspect cfg
- [ ] Run against trappist_1 (with extras yaml) → inspect cfg
- [ ] Verify Module Manager syntax via static check (regex for
  `@Kopernicus:FOR[NearStarsSystem]` header, node bracket balance)
- [ ] Skim 2-3 emitted bodies against the equivalent
  `RSS-Reborn/Sol-Configs/Configs/` reference cfg — sanity-check
  field types/ranges

## Stage 4 — Wire + integrate

- [ ] Update `.claude/skills/kopernicus-cfg/SKILL.md` — add §3
  "Bulk emission" section pointing at the emitter. Manual procedure
  in §1-§2 stays for edge cases not yet automated.
- [ ] Register emitter + extras yaml in `docs/reference/tools.md` (en + ko)
- [ ] Update `phase3/<system>/system.yaml` schema docs if needed
  (e.g. add `kopernicus_extras_present: true` flag for run_phase3.py
  validation)
- [ ] `./scripts/check.sh` clean

## Out of scope (subsequent sessions)

- PQS texture asset generation (heightmap + colormap PNG files)
- Detailed biome region map authoring
- Ring texture/material authoring
- Hazardous surface specifics (lava, radiation)
- ScaledVersion mesh export (uses Parallax cacheFile path; mesh generation deferred)

## Related

- [plan](plan.md)
- [context-notes](context-notes.md)
