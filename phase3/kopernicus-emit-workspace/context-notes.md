# Kopernicus emitter — context notes

## Why sidecar yaml instead of prose extraction at emit time

This was discussed in the session that handed off this workspace. The
core decision:

**emit is pure Python. Prose interpretation happens during Phase 3
curation, captured in structured form, then read mechanically.**

Three options were considered:

1. **Pure mechanical emitter, manual prose fields.** Emit ~70% of cfg
   automatically; hand-finish ~30% per body. Rejected — still requires
   per-body manual work.
2. **Structured intermediate (sidecar yaml).** Add a small set of
   structured fields to capture cfg-only decisions (terrain class,
   ring params, biome count, etc.) — emit becomes fully mechanical.
   **Selected.**
3. **LLM at emit time.** Have Claude read Phase 3 prose + Kopernicus
   references + DB data at emit time and generate cfg. Rejected —
   non-deterministic; defeats the "no new code per system" goal;
   curation intent invisible in emitter output.

The sidecar pattern preserves three properties:

- **Determinism** — same inputs always produce same cfg.
- **Curation visibility** — the structured override sits next to the
  Phase 3 markdown in the same `phase3/<system>/` directory, so a
  reviewer sees both the science synthesis and the cfg-specific call.
- **No new code per system** — the original goal. Adding a new system
  means: write `system.yaml` (Phase 3 driver) + measurements.yaml
  (Phase 2) + kopernicus_extras.yaml (cfg overrides). Zero Python.

## Field categorization

For each Kopernicus cfg field, ask "where does this value come from?":

| Source | Kopernicus fields |
|---|---|
| `db/systems/*.json` mechanical | gravParameter (mass), radius, Orbit elements |
| `docs/phase3/*.md` Decisions mechanical | atmosphere_present (→ ScaledVersion.type), atmosphere_pressure_pa + temperature_K (→ pressureCurve, temperatureCurve), atmosphere_tint_rgb_hex (→ ScaledVersion material color), ocean_extent_substellar_radius_deg (→ Ocean node trigger) |
| `kopernicus_extras.yaml` sidecar | terrain_class (→ PQS preset), ring_present + ring_*_au + ring_color_hex (→ Ring node), biome_count, pqs_color_low/high_hex, ocean_color_hex |
| Hardcoded NearStars conventions | MM header tag, texture path prefix, flightGlobalsIndex range, cacheFile path, epoch |
| Templated from references/*.md | The boilerplate skeleton (Properties block layout, Atmosphere ramp, PQS subnode structure) |

This list is the design target. Any Kopernicus field that doesn't fit
one of these rows means we have a gap — either it should be in the
sidecar schema or it's an indication that Phase 3 needs to grow that
field.

## Terrain class — proposed enum

Maps to PQS preset values inside the emitter. The Phase 3 curator
picks the closest match to the planet's intended look.

| terrain_class | deformity | mountainAmplitude | craterCount | base_color | Example |
|---|---|---|---|---|---|
| smooth | 0.2 | 50 | 0 | gray | sub-Saturnian moons |
| rocky | 0.6 | 1500 | 20 | brown | Mars-like |
| cratered | 0.4 | 800 | 200 | gray | Mun-like |
| volcanic | 0.7 | 2500 | 30 | red-orange | Io-like, hot rocky |
| icy | 0.3 | 500 | 50 | white-blue | Europa-like |
| desert | 0.4 | 600 | 10 | tan | Mars analog with active surface |
| gas_giant | 0 | 0 | 0 | striped | Jupiter/Saturn |
| ocean_world | 0.1 | 100 | 0 | blue | Earth/Kerbin |

Defaults are starting points; sidecar can override individual values
(e.g., `mountainAmplitude_override: 1800`) for fine-tuning.

## Open questions for next session

- **PQS texture path convention.** Kopernicus expects heightmap/colormap
  PNG paths under `GameData/NearStarsSystem/PluginData/<body>/`. These
  files don't exist yet (texture art is separate work). Emitter should
  write the path strings deterministically but the assets are TODO.
  Decision: emit cfg with placeholder paths + log missing-asset list
  per body. Module Manager won't fail to load the cfg; planet just
  uses fallback render until textures are added.
- **flightGlobalsIndex allocation.** NearStars rule: 1000+, 100 per
  system. The emitter needs a mapping from system_slug → base index.
  Where does this state live? Options:
  - Hardcoded dict in emit script
  - In `db/systems/<system>.json` as a `kopernicus_fgi_base` field
  - In `kopernicus_extras.yaml` as a top-level
  Probably (b) since it's a per-system fact tied to DB ordering.
- **Atmosphere temperature curve generation.** Phase 3 only gives
  surface temperature; Kopernicus needs a curve over altitude. Need a
  parametric model: `T(h) = T_surface * exp(-h/scale_height_for_temperature)`
  with sensible defaults. Use Phase 3 `atmosphere_scale_height_km` if
  available.
- **AtmosphereFromGround color**. Currently Firefly emitter computes
  bulk-gas palette per body. Kopernicus AtmosphereFromGround needs a
  similar color but slightly different (Rayleigh scattering, not
  plasma). Two-layer mapping:
  - `kopernicus_atm_color = lerp(bulk_gas_palette.trail_primary, surface_tint_rgb_hex, 0.3)`
  - Or read from Phase 3 `atmosphere_tint_rgb_hex` if present
- **Star body Light + Coronas + sun-flare**. NearStars stars need
  Kopernicus `ScaledVersion.Light` + `Coronas` subnodes. Color comes
  from Teff (blackbody mapping). Cf. `Properties → spectral type →
  blackbody RGB`. Reusable from existing kopernicus-cfg skill prose.

## Texture asset workflow (deferred)

Once cfg emitter is working, the next layer is texture asset generation.
That's a separate workstream (could be Phase 3.5 or a new mod
side-project). The cfg emitter writing placeholder paths is the
contract — texture pipeline fills the actual PNGs later.

## Reference implementations

When starting next session, read these in order:

1. `.claude/skills/principia-cfg/scripts/emit_principia_cfg.py` —
   simplest pattern, DB → cfg, validation, MVP scope handling
2. `.claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py` —
   intermediate, reads Phase 3 markdown + DB + element DB
3. `phase3/firefly-cfg-workspace/emitter/context-notes.md` — design
   journal of the Firefly emitter build
4. `.claude/skills/kopernicus-cfg/references/*.md` — 14 files of cfg
   template prose, source of skeleton strings for the emitter

## Related

- [plan](plan.md)
- [checklist](checklist.md)
- [kopernicus-cfg skill](../../.claude/skills/kopernicus-cfg/SKILL.md)
- [emit_principia_cfg.py](../../.claude/skills/principia-cfg/scripts/emit_principia_cfg.py) — pattern reference
- [emit_firefly_cfg.py](../../.claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py) — pattern reference
