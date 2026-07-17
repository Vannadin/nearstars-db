# Orbit-viewer pipeline — context notes

Standardize the "sim → visualize → viewer" flow across NearStars systems, framed
as the **finalization of Phase 4 orbit-related axes** (obliquity, rotation, orbital
elements, moon orbits). The dynamics viewer is the verification/closure artifact
for those axes — complementary to the hand-crafted art viewers.

## Owner decisions (2026-07-17)
- **Reference frame: provide ALL toggles** in the viewer — invariable plane /
  parent-orbital plane / sky (observational). Default = invariable.
- **Scope: Phase 4 orbit-axis systems** — do this as the closure of the orbit-
  related Phase 4 decisions, i.e. the systems that carry Phase 4 boards.
- **Rollout: αCen skeleton first**, then extend to the rest via a manifest.

## Design decisions & why
- **Data contract already uniform.** run.py emits `{system}_summary.json` +
  `_timeseries.csv` for every `--system`. The viewer must consume ONLY that →
  zero per-system viewer code (generalize-over-hardcode).
- **Frame normalization = invariable plane** as the canonical default. Computed
  from masses + initial elements as the angular-momentum-weighted orbit normal;
  conserved, so fixed for the whole run; identical rule across systems → grids
  are comparable. For a moon system invariable ≈ equatorial(spin) plane, so the
  moons render near-horizontal (the alignment the owner wanted).
- **Why the sky frame looked tilted:** the sim reference plane = plane of sky
  toward the system (the frame the astrometric binary/planet elements are
  tabulated in; αCen AB `i=79.2°`). It is observational, not dynamical. Hence
  everything sits at large inclinations there. The toggle exposes all three.
- **Frame switch = one quaternion on a content Group.** Bodies are drawn in the
  sim frame (via orbitVec sim→three mapping x,y,z→x,z,y). Wrapping planet +
  orbits + spin axis in a Group and rotating so the chosen plane normal → +Y
  makes the +Y grid always represent the selected reference plane. Grid stays
  at +Y (not in the group).
- **Hierarchy generalization (pending):** one generator for "star+planets" and
  "planet+moons" — detect primary (child.parent), render children, auto-scale
  (AU vs R_p). Binaries (αCen, 40 Eri, Luhman 16) branch on a companion body.
- **Per-system manifest (pending):** `viewer-manifest.yaml` holds each system's
  sim params (years, integrator, snapshots, hypotheticals, overrides) — single
  reproducible source, replaces ad-hoc CLI.

## Established facts to reuse
- Principia-equivalent run = `--integrator leapfrog --dt-minutes 10`.
- Dense run for jitter-free animation = `--snapshots 8000` (bin-averaged down in
  animate_orbits.py; see its docstring). ~13 min/system.
- Frame math: orbit normal (sim frame) from (inc, Ω) = (sin i sin Ω, −sin i cos Ω, cos i).
- j2.axis in summary is the spin axis (sim frame); moons sit 3–9° from it (αCen).

## Open questions / risks
- Which exact systems have Phase 4 boards → that's the scope list (αCen has one;
  trappist_1 / luhman_16 boards do not yet exist per memory).
- Runtime: N systems × ~13 min dense. Manifest must cache/skip-if-fresh.
- Some systems are single-planet → dynamics dull; may warrant static-only.
