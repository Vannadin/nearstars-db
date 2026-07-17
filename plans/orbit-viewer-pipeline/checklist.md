# Orbit-viewer pipeline — checklist

Framing: finalization of Phase 4 orbit-related axes. Rollout: αCen skeleton first.

## Phase A — αCen skeleton (prove the pattern on one system)
- [x] Frame normalization + toggle in animate_orbits.py (invariable / orbital / sky), default invariable
  - [x] generator computes the 3 sim-frame up-vectors from masses + initial elements
  - [x] viewer wraps content in a Group, switches frame via one quaternion; grid = chosen plane
  - [x] verify: invariable ↔ spin = 8.87° (moons ~aligned); embedded frames sane — 2026-07-17
- [x] Hierarchy generalization: center auto-detected (moon parent / star), children rendered, auto-scale (AU vs R_p) — animate_orbits.py + plot_moons.py, 2026-07-18
- [x] Static + 3D both driven purely from summary + timeseries (no per-system code)
- [x] αCen viewer reviewed & accepted by owner (moon system, frame toggles)

## Phase B — pipeline plumbing
- [x] `viewer-manifest.yaml` — per-system sim params (Principia-equivalent leapfrog dt=10min, years, snapshots, hypotheticals, overrides)
- [x] batch driver `build_viewers.py`: manifest → sim (skip-if-fresh) → static + 3D → gallery
- [x] bilingual gallery index (docs/phase4/orbit-viewers/index.html, ko/en toggle)
- [ ] register build_viewers.py + manifest in docs/reference/tools.md (+ko)

## Phase C — roll out to remaining Phase 4 orbit-axis systems
- Owner note: existing WHFast/TRACE summaries NOT reused — every system re-run
  the Principia way (leapfrog dt=10min, 2000 yr) via the manifest.
- Scope (in manifest): alpha_centauri (moons), proxima_cen, 40_eridani, tau_cet,
  barnards_star + trappist_1 (bonus). fomalhaut omitted (1 planet, trivial).
- [ ] full 2000 yr build running → spot-check each verdict + frame alignment
- [ ] wire results back as the "orbit axes finalized" evidence in the Phase 4 boards

## Deferred / decisions pending
- [x] single-planet systems: skip (fomalhaut omitted from manifest)
- [ ] commit cadence: per-phase semantic commits

## Done
- [x] Owner decisions captured (frame toggles / Phase 4 scope / αCen-first) — 2026-07-17
- [x] Principia-equivalent 2000 yr αCen run (STABLE) + dense 8000-snapshot run
- [x] plot_moons.py (static 4-panel) + animate_orbits.py (3D, bin-averaged)
- [x] spin-axis / oblateness orientation fix in animate_orbits.py
