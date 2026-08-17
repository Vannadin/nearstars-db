# Luhman 16 Phase 4 board — first authoring

Create `phase4/luhman_16.yaml` (schema v2) covering Luhman 16 A (L7.5) and
Luhman 16 B (T0.5). Phase 3 grounding: `docs/phase3/luhman-16-a.md` / `-b.md`.

## Tasks

- [x] Owner facet-walk: rotation (A 6.94 h), color policy (soft R-dominant
      magenta), B weather treatment (Crossfield skeleton + Apai motion),
      magnetism approach (dynamo methodology).
- [x] Board skeleton: `schema_version: 2`, `system: luhman_16`, `status: staged`.
- [x] **Luhman 16 A: all 11 axis groups dispositioned (13 rows)** — identity,
      orbit (validated 1950.0 phase, MEGNO 1e6 yr), bulk anchor, spin axis
      (methodology), J2/figure, atmosphere (photosphere-as-surface, 2.6 bar),
      surface (absence), appearance + aurora (documented-divergence), magnetism
      (ISM-ram geometry + CRAND belt), environment, satellites (absence),
      gameplay (3 latitude biomes).
- [ ] Luhman 16 B: same walk (inputs already gathered: P 4.87 h high-conf,
      i* ~ 90 deg, B_dyn 1177 G, figure q 8.7e-3, Crossfield+Apai weather).
- [x] Dynamo B-field computed via planetary-dynamo-scaling BD branch (A 1250 G,
      B 1177 G), methodology doc cited.
- [ ] `python3 scripts/check_phase4_gate.py` — 0 errors.
- [ ] `python3 scripts/phase4/build_phase4_html.py luhman_16` + eyeball.
- [ ] Commit per logical unit.

## Constraints

- Do NOT touch the uncommitted magnetopause-regate changes
  (`phase4/alpha_centauri.yaml`, `phase4/proxima_cen.yaml`,
  `scripts/viz/render_belts_bodies.py`) — another session owns them.
  Never `git add -A`; stage only `phase4/luhman_16.yaml`, this dir, and
  generated `docs/phase4/luhman_16/`.
