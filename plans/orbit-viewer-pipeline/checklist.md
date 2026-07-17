# Orbit-viewer pipeline — checklist

Framing: finalization of Phase 4 orbit-related axes. Rollout: αCen skeleton first.

## Phase A — αCen skeleton (prove the pattern on one system)
- [x] Frame normalization + toggle in animate_orbits.py (invariable / orbital / sky), default invariable
  - [x] generator computes the 3 sim-frame up-vectors from masses + initial elements
  - [x] viewer wraps content in a Group, switches frame via one quaternion; grid = chosen plane
  - [x] verify: invariable ↔ spin = 8.87° (moons ~aligned); embedded frames sane — 2026-07-17
- [ ] Hierarchy generalization: primary auto-detected (child.parent), children rendered, auto-scale (AU vs R_p)
- [ ] Static + 3D both driven purely from summary + timeseries (no per-system code)
- [ ] αCen viewer reviewed & accepted by owner

## Phase B — pipeline plumbing
- [ ] `viewer-manifest.yaml` — per-system sim params (years, integrator, snapshots, hypotheticals, overrides)
- [ ] batch driver: iterate manifest → sim (skip-if-fresh) → static + 3D → per-system viewer HTML
- [ ] bilingual gallery index (en + ko mirror) linking all system viewers
- [ ] register tools in docs/reference/tools.md (+ko)

## Phase C — roll out to remaining Phase 4 orbit-axis systems
- [ ] enumerate systems with Phase 4 boards = the scope list
- [ ] run each through the manifest; spot-check verdict + frame alignment
- [ ] wire results back as the "orbit axes finalized" evidence in the Phase 4 boards

## Deferred / decisions pending
- [ ] single-planet systems: static-only vs skip
- [ ] commit cadence: per-phase semantic commits

## Done
- [x] Owner decisions captured (frame toggles / Phase 4 scope / αCen-first) — 2026-07-17
- [x] Principia-equivalent 2000 yr αCen run (STABLE) + dense 8000-snapshot run
- [x] plot_moons.py (static 4-panel) + animate_orbits.py (3D, bin-averaged)
- [x] spin-axis / oblateness orientation fix in animate_orbits.py
