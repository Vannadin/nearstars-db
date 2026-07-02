# Context notes — Principia interstellar branch draft

Append-only. Decisions + reasoning as the work proceeds.

## 2026-07-02 — kickoff
- Trigger: owner wants to leverage `fable` model (available until 2026-07-07) to
  dig max on the Principia custom branch (memory `project_principia_custom_branch`)
  and produce a branch draft.
- Confirmed the branch's real technical content = **frame nesting** for
  interstellar precision, per `schultz-dev0/principia-docs/interstellar-audit.md §7`
  and `theoretical_implementation.md`. NOT the US²-style integrator/UX borrow
  (that's the separate `universe-sandbox-nbody-comparison.md` note).
- Source state on disk:
  - `principia-docs` (schultz) cloned to scratchpad — audit + theoretical_impl read.
    NOTE: my earlier PR draft `nbody-engine-comparison.md` DID land in his repo.
  - Principia source shallow-cloned to scratchpad, master head `440310a9`
    (audit was written against old head `cc6522fc9` → line numbers drifted, must
    re-verify).
  - The `docs/nbody-engine-comparison` local branch from memory is GONE from this
    checkout (was another session/machine). Not needed; content is in schultz repo.

## Problem restated (from the two docs)
- Positions bottom out in one IEEE-754 `double`/axis. ULP ≈ 2^-52·|x|.
  At Proxima (4e16 m) → ~9 m; Trappist-1 (3.8e17 m) → ~84 m.
- `DoublePrecision<T>` (numerics/double_precision.hpp) fixes *integration* error
  (compensated summation of step vs running total), NOT *storage* error —
  positions are stored as plain `Position`, not `DoublePrecision<Position>`.
- `Frame<Tag,...>` is a flat compile-time tag; no nesting (geometry/frame.hpp).
- Single `Ephemeris<Barycentric>` per session (ksp_plugin/plugin.hpp).
- Two rejected options: Option 1 (Sol origin, stars as perturbers) works for
  stellar motion but `r_planet - r_star` cancels 6-7 digits → no remote-planet
  precision. Option 2 (galactic origin) → Sol itself at 55 km. Neither plays.
- Real fix (audit §7.2): 2-level frame nest Galactic→StarBarycentric→Vessel,
  DoublePrecision only across top level, plain Position near each star.

## Key hypothesis to test in synthesis
- Principia ALREADY has runtime dynamic reference frames
  (ReferenceFrame<InertialFrame, ThisFrame>, RigidMotion) for the plotting frame.
  Q: can the per-star local frame reuse this instead of a new compile-time nest?
- KSP itself floats the origin near the active vessel (Krakensbane). So rendering
  may already tolerate 1e16 m; the problem is likely confined to ephemeris
  STORAGE + prediction, not display. Agent 4 checks this.

## 2026-07-02 — 4 fable ground-truth reports in, architecture converged
All against master 440310a9 (audit was cc6522fc9; lines drifted, re-verified).

### Converged findings
- **Frame** = pure compile-time empty tag; encoding parentage buys nothing (frame.hpp:52-79). Nesting is a physics-layer concept.
- **Position<F>** = {double x,y,z} confirmed (grassmann→r3_element→quantities.hpp:83). No DoublePrecision in stored positions.
- **Cancellation site** = ephemeris_body.hpp:1366 `Δq = position_of_b1 - positions[b2]`; integrator flattens DoublePrecision→plain in q_stage (symplectic_rkn_body.hpp:114, drops .error). Repeated in massless(1433)/Jacobian(1193)/jerk(1230)/potential.
- **Dynamic reference frames already exist**: ReferenceFrame<InertialFrame,ThisFrame> (reference_frame.hpp:45-47), RigidMotion composes (rigid_motion_body.hpp:173). BUT offset can't be injected at AffineMap layer (affine_map_body.hpp:42) — operands already lossy. Must split origin out of Position *before storage*.
- **Plugin already floating-origin-safe**: World re-anchored at root part per frame (plugin.cpp:702-752); P/Invoke all double; KSP hand-off parent-relative AliceSun (plugin.hpp:334-345) = the natural seam. Float only at ScaledSpace map view (planetarium.hpp:44-46).
- **Breakage concentrated**: (a) single Ephemeris<Barycentric> integration+Chebyshev fit at 1mm tol vs ~4m ULP (integrators.cpp:34,41,80); (b) single-sun assumptions (plugin.hpp:588 sun_, renderer sun-anchored world renderer.cpp:197-205); (c) Sun-anchored map World + float ScaledSpace.

### DECISION — architecture = per-star SUBSYSTEM ephemeris
- Bodies partitioned by subsystem S(i); positions stored LOCAL to subsystem origin (≤~1e13 m → sub-mm in double).
- Inter-origin offsets O_B−O_A as DoublePrecision<Displacement<Barycentric>>.
- Gravity kernel: same-subsystem = today's exact small Δq (zero cost, hot Sol loop unchanged); cross-subsystem = local diff + wide offset, low precision demand (accel ~1e-14 of intra terms).
- Reuse dynamic-reference-frame machinery for plotting, anchored to LOCAL star.
- Remove single-sun assumptions; map World + ScaledSpace re-anchor on local star (adapter).
- Origin MOTION is the hard sub-decision: (i) integrate each origin as extra DoublePrecision ODE var (needs .error plumbed through q_stage), or (ii) kinematic/periodic re-anchoring ("rebasing" fold between fixed steps).

### Rejected
- Compile-time frame nest (Frame tag can't carry offset usefully; ripples through all templates).
- Galactic origin (Sol itself → 55 km).
- Wide floats everywhere (DoublePrecision<Position> stored globally) — heavy, and dynamic-range not the issue, cancellation is.

## 2026-07-02 (b) — owner scoped 3 workstreams; model reallocation
Owner defined the actual branch scope as 3 features, and directed: RESEARCH via
general agents (not fable — wasteful), reserve FABLE for the actual branch code edits.
Working branch created: scratchpad Principia clone, branch `nearstars-interstellar`.

Three workstreams:
1. **Long-distance FP** — owner: Schultz overcomplicated it (galactic centre etc.).
   MINIMAL form only: per-star local origin + DoublePrecision inter-origin offset,
   NO galactic frame. (Refines existing design-draft §3; drop the Galactic level.)
2. **SOI separation** — beyond where gravity →0, treat gravity as LITERALLY ZERO
   (not Principia n-body, not stock patched-conic); keep inertia only. Body-body
   interaction only within an SOI group → big O(N²) cut. Composes with subsystem
   partition. HARD question = hard-zero discontinuity vs symplectic no-drift.
3. **Thrust under timewarp** — sustained low-thrust over long durations during warp,
   for interstellar cruise. Gap = real-time physical thrust under warp vs planned
   flight-plan burn.

Research agents launched (R1 sonnet=FP, R2 sonnet=SOI code, R3 opus=SOI numerics,
R4 sonnet+web=thrust). Next: synthesize → implementation spec → fable implements
on `nearstars-interstellar`.
Opened ko mirror in browser for owner review (preview-md.sh).

## 2026-07-02 (c) — division of labor finalized
- All 4 research agents now on OPUS (R1 FP, R2 SOI-code, R3 SOI-numerics, R4 thrust).
- FABLE implementation will be driven by the owner DIRECTLY in a separate session
  (better context locality for editing the branch). This session's job ends at:
  4 opus reports → synthesize into ONE clean implementation spec (impl-spec.md)
  that the owner hands to fable.
- Working branch for fable: scratchpad Principia clone, branch `nearstars-interstellar`
  (head 440310a9). Note: scratchpad is session-local — the owner's fable session
  may need its own clone/branch; flag this in the handoff.

## 2026-07-02 (d) — 4 opus research reports in; hand-off spec written
Deliverables in plans/principia-interstellar-branch/:
- research/R1-R4.md (raw opus specs), impl-spec.md (master synthesis), + ko mirror.

Two synthesis decisions that override the individual reports:
1. **WS1 subsystem partition == WS2 groups_** — build ONE partition
   (subsystem_of_body_ + subsystem_origin_offset_ + subsystem_members_ +
   soi_cutoff_squared_). STATIC to start (avoids within-step membership-change
   hazard). WS1→WS2 sequential; WS3 independent.
2. **SOI cutoff = smooth C² quintic taper on the POTENTIAL, NOT hard-zero.**
   R3 correction: QT12 is a SYMMETRIC LINEAR MULTISTEP method (methods.hpp:1041),
   not symplectic; no-drift comes from reversibility + smoothness. Hard-zero →
   energy step μ/r_c per crossing → random-walk drift, 8-12 orders > tolerance.
   Compact-support taper = exactly 0 beyond r_c (delivers owner's force-free
   coasting intent) but smooth → no drift. Vessel path first (low risk, main
   payoff, one-way coupled); backbone block-diagonal only between star systems,
   symmetric per pair. + Verlet neighbor list/skin for the O(N²)→O(N·k) speedup.

Owner drives fable in a SEPARATE session from impl-spec.md (self-contained: has
clone+branch setup). This session = research + spec only; no fable implementation
here (owner's call).

## 2026-07-02 (e) — published
- Schultz PR: https://github.com/schultz-dev0/principia-docs/pull/2
  (branch nearstars-interstellar-branch-spec on Vannadin/principia-docs fork;
  files under interstellar-branch-spec/).
- Principia fork = code+spec home: Vannadin/Principia, branch `nearstars-interstellar`,
  spec under docs/nearstars/. fable + Schultz clone THIS fork/branch to work.
- NearStars repo (Vannadin/nearstars-db) is PUBLIC — the earlier auto-mode
  "private repo" exfil assumption was wrong; no confidentiality delta.
- Durable local backup: ~/Desktop/NearStars-local-backups/principia-interstellar-branch_2026-07-02/
- NearStars-repo copy (plans/principia-interstellar-branch/ + ko mirror) still
  UNCOMMITTED — owner deciding whether to keep it here as the design/decision record.
