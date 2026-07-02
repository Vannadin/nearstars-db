# R1 — Long-distance FP precision fix (per-star local origin + DoublePrecision offset)

Research agent: opus. Source: mockingbirdnest/Principia branch `nearstars-interstellar`, head 440310a9. Owner axiom: NO galactic frame; `Barycentric` stays the sole integration frame; subsystems (0 = Sol at local origin, each remote star = one subsystem) carry a `DoublePrecision<Displacement<Barycentric>>` offset relative to Sol.

## 0. Root cause (verified)
- `Position<Barycentric>` = one `double`/axis (`quantities.hpp:83` → r3_element → grassmann → space.hpp).
- Cancellation site `ephemeris_body.hpp:1366` `Δq = position_of_b1 - positions[b2]`; both ~4e16 m → ULP ≈ 9 m; small in-system separation lost.
- Integrator `symplectic_runge_kutta_nyström_integrator_body.hpp:114,133` keeps DoublePrecision per body but only compensates the *increment*; absolute magnitude fixes resolution. Localizing origin shrinks |q.value| to ~1e13 m → ULP ~2e-3 m. Relocation is the fix.

## 1. Data structures
Store per subsystem `DoublePrecision<Displacement<Barycentric>> origin_offset` (Displacement, NOT Position — never materialize a 4e16 Position double). Difference of two offsets is again DoublePrecision<Displacement> (`double_precision.hpp:149-151`). Offset is a constant (never integrated).

Members on `Ephemeris<Frame>` near `ephemeris.hpp:534-535`:
```cpp
std::vector<int> subsystem_of_body_;                                    // parallel to bodies_; 0 == Sol
std::vector<DoublePrecision<Displacement<Frame>>> subsystem_origin_offset_;  // index == subsystem id; [0] zero
```
Ctor gets trailing `std::vector<int> const& subsystems = {}` (default ⇒ single subsystem 0 ⇒ byte-identical legacy).

## 2. Ingest global→local (Ephemeris ctor `ephemeris_body.hpp:122-159`)
After `CHECK_EQ(bodies.size(), initial_state.size())` (:114): normalize subsystem vector; each subsystem's anchor = global position of its first input body; `subsystem_origin_offset_[s] = TwoDifference(anchor[s], anchor[0])` (Point×Point overload `double_precision.hpp:104-119`). In the per-body loop replace global DoF with local: `local_position = Frame::origin + (dof.position() - anchor[s])`; feed `local_dof` to `trajectory->Append` (:136) and `state.positions` (:146-147,:155). Velocities unchanged (translation-invariant). Fill `subsystem_of_body_` in the index post-loop (:161-163), mapping by body pointer (oblate reorder at :144-150).

## 3. Gravity kernel (`ComputeGravitationalAccelerationByMassiveBodyOnMassiveBodies`, static, decl `ephemeris.hpp:426`, body `ephemeris_body.hpp:1342-1410`)
Being static, add params `subsystem_of_body`, `subsystem_origin_offset`; thread through call sites (`:1516-1548`, `:1274-1311`). Replace `:1366`:
```cpp
int s1 = subsystem_of_body[b1], s2 = subsystem_of_body[b2];
Displacement<Frame> Δq;
if (s1 == s2) {
  Δq = position_of_b1 - positions[b2];             // unchanged, full precision
} else {
  DoublePrecision<Displacement<Frame>> inter = subsystem_origin_offset[s1] - subsystem_origin_offset[s2];
  Displacement<Frame> local_diff = position_of_b1 - positions[b2];
  Δq = inter.value + (inter.error + local_diff);   // cross-system 1/r² negligible; collapse safe
}
```
Downstream (`Δq²`, geopotential `:1386,:1399`) unchanged. Apply identical split to Jacobian (`:1193`) and jerk kernels or energy/variational machinery disagrees (may defer for commit 1 if not on Prolong path — grep-verify).

## 4. Trajectory storage
`AppendMassiveBodiesStateToTrajectories` (`:1101-1116`) already appends `.value`, now local ⇒ UNCHANGED. ContinuousTrajectory stays local (Chebyshev fit on ~1e13 not ~4e16 reclaims ~5 digits). Add `subsystem_origin_offset(body)` accessor; `EvaluateAllPositions` default LOCAL, add `EvaluateGlobalPosition` (adds offset) only for rendering path — never silently globalize.

## 5. Serialization
`serialization::DoublePrecision` exists (`numerics.proto:26-44`, Multivector value). Extend `message Ephemeris` (`physics.proto:181-210`, last tag 13): add `repeated int32 body_subsystem = 14;` `repeated DoublePrecision subsystem_origin_offset = 15;`. Empty ⇒ legacy single-subsystem ⇒ old saves load unchanged. Do NOT reuse existing `Subsystem` message (`:231`, Kepler hierarchy — unrelated).

## 6. Validation test (`astronomy/interstellar_precision_test.cpp`, mirror `trappist_dynamics_test.cpp:985-1153`)
Two identical star+planet subsystems, subsystem 1 at +4.0e16 m x̂; `subsystems={0,0,1,1}`. Control = `subsystems={}` (legacy). Prolong 100 yr. Assert: fixed branch `max_t |‖r1‖−‖r0‖| < 1 mm`; control `> 1 m`. Optional energy: after <1e-11, control ~1e-6. Numbers: ULP(4e16)=9 m, ULP(1.5e11)=3.3e-5 m, ~2.7e5× improvement.

## 7. Commit order
1. **Prove precision headless (3 files)**: members + ctor param + kernel split + call sites + test. Fully back-compat.
2. Jacobian/jerk cross split.
3. Serialization + round-trip test.
4. Global accessor + plugin wiring (`plugin.cpp:128-138` InsertCelestialAbsoluteCartesian → thread subsystems; route only rendering through globalizing accessor).
