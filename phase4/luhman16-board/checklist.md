# Luhman 16 Phase 4 board — first authoring

Create `phase4/luhman_16.yaml` (schema v2) covering Luhman 16 A (L7.5) and
Luhman 16 B (T0.5). Phase 3 grounding: `docs/phase3/luhman-16-a.md` / `-b.md`.

## Tasks

- [ ] Owner facet-walk: rotation (A), color policy, B weather treatment,
      magnetism approach (dynamo methodology vs none).
- [ ] Board skeleton: `schema_version: 2`, `system: luhman_16`, `status: staged`.
- [ ] Per-body rows: identity / bulk / appearance / atmosphere-as-appearance /
      magnetism / environment / orbit (binary AB) / gameplay; silent-passthrough
      confirms for measurement-less axes (obliquity, spin axis).
- [ ] If dynamo route chosen: compute B-field via
      `docs/reference/planetary-dynamo-scaling.md` recipe, cite the methodology doc.
- [ ] `python3 scripts/check_phase4_gate.py` — 0 errors.
- [ ] `python3 scripts/phase4/build_phase4_html.py luhman_16` + eyeball.
- [ ] Commit per logical unit.

## Constraints

- Do NOT touch the uncommitted magnetopause-regate changes
  (`phase4/alpha_centauri.yaml`, `phase4/proxima_cen.yaml`,
  `scripts/viz/render_belts_bodies.py`) — another session owns them.
  Never `git add -A`; stage only `phase4/luhman_16.yaml`, this dir, and
  generated `docs/phase4/luhman_16/`.
