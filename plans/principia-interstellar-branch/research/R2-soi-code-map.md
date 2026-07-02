# R2 — SOI cutoff + grouped interaction (code-mapping)

Research agent: opus. Source head 440310a9. Physics-correctness owned by R3.

## 0. No existing SOI machinery
Grep `sphere_of_influence|SOI|dominant|HillRadius|LagrangeEquipotential` in physics/, ksp_plugin/: only the **Lagrange equipotential plotting overlay** (`physics/lagrange_equipotentials*.hpp`, rendering only, does NOT feed the integrator). `subsystem` → only `hierarchical_system_body.hpp` (construction-time Jacobi helper, not runtime). **The per-star subsystem partition does not exist in code either — the `groups_` structure below IS that partition; SOI cutoff is a second filter layered on it.** (Reconcile with R1's `subsystem_of_body_`: same concept.)

## 1. Gravity path + cutoff insertion points
- Massive accel bound: `MakeMassiveBodiesNewtonianMotionEquation` (`ephemeris_body.hpp:1133-1147`) → `ComputeGravitationalAccelerationBetweenAllMassiveBodies`; integrator built at ctor `:166-170`.
- Massless bound: `:366-385`, `:422-436`, `:453-470` → `...OnMasslessBodies`.
- Dispatcher `:1503-1552`: oblate-oblate + oblate-spherical + spherical-spherical, exploiting oblate-low-index invariant (`:138-159`, `ephemeris.hpp:514-516`), each pair once with Newton-3rd-law dual update.
- Pairwise kernel `:1342-1410`. **Cutoff insertion: after `Δq²` at `:1368`, before Sqrt `:1369`**: `if (Δq² > cutoff²(b1,b2)) continue;` (squared, no Sqrt). Correct-zero but not the O(N²) win (still visits every b2).
- Massless kernel `:1412-1462`, loop `:1431-1460`; `Δq²` `:1435`. SOI test slots beside existing collision test `:1437-1441`: `if (Δq² > soi_cutoff²(b1)) continue;`. Vessel outside ALL SOIs → zero accel → coasts.
- **Sister kernels needing identical cutoff** (else energy/variational disagree): Jacobian `:1174-1208` (loop :1187), jerk `:1210-1247` (:1224), potential `:1464-1501` (:1477), single-body query `:1249-1340`.

## 2. Grouped iteration (the O(N²)→O(Σnₖ²) win)
- **Tier A** (per-pair skip §1): zero structural change, correctness only, keeps O(N²) Δq. Do first.
- **Tier B** (grouped): replace contiguous ranges (`:1514-1549`) with intra-group pairs. Groups are arbitrary index sets mixing oblate/spherical → per group keep two index lists (`oblate_members`, `spherical_members`), emit the 3 template kernels restricted to them. Generalize kernel to take `std::vector<std::size_t> const& b2_indices` instead of `[b2_begin,b2_end)` (mechanical loop-header change at `:1360`, body unchanged). Cross-group pairs never enumerated.

## 3. Data structures (= the subsystem partition)
On `Ephemeris` private, near `ephemeris.hpp:535`/`:548`:
```cpp
std::vector<int> group_ids_ ABSL_GUARDED_BY(lock_);        // == subsystem_of_body_ (R1)
struct BodyGroup { std::vector<std::size_t> oblate_members, spherical_members; };
std::vector<BodyGroup> groups_ ABSL_GUARDED_BY(lock_);
std::vector<Square<Length>> soi_cutoff_squared_;           // per-body, fixed at ctor (0 ⇒ no cutoff)
```
`group_ids_`/`groups_` mutable+lock-guarded (membership changes as bodies move); `soi_cutoff_squared_` immutable — recommend attaching a `sphere_of_influence()` accessor to `MassiveBody` (travels with serialization/identity). **Start with a STATIC partition** (assign at construction, never recompute) — sidesteps every integrator-contract hazard.

## 4. Vessel zero-accel path
`compute_acceleration` lambda → `...ByAllMassiveBodiesOnMasslessBodies` (`:1554-1591`) → per-b1 `...ByMassiveBodyOnMasslessBodies` with SOI test. All b1 skipped → zero accel → inertial coast. Intrinsic (engine) accel still added after (`:377-381,:432,:465`) → burning vessel in deep space still thrusts. Single-body wrapper `:623-642` inherits it.

## 5. Group-recompute hook (if dynamic)
Only at fixed-step boundaries: `Ephemeris::Prolong` (`:312-344`), insert `RecomputeGroups_locked()` immediately before `instance_->Solve` at `:338` (already holds `lock_` at :315). NEVER inside `compute_acceleration`. Static partition ⇒ no-op after construction.

## 6. Integrator-contract constraint (→ R3)
`compute_acceleration` signature frozen (`:1138-1144`) — group data read from `this`, not a param. SRKN/multistep evaluates accel at multiple stage points per step ⇒ (1) force law must be constant across a step (groups read-only in accel); (2) membership changes only between steps (Prolong hook); (3) a per-pair hard cutoff is itself a within-step force discontinuity as a body crosses cutoff² between stages. R3 decides: accept (cutoff in numerically-negligible tail) vs C¹/C² smooth taper. Static partition removes hazard for grouping; only the SOI tail cut remains. **[R3 verdict: smooth C² taper on the potential, symmetric per pair, + Verlet skin+hysteresis. See R3.]**

## Files
- `physics/ephemeris.hpp`: members near :535/:548; declare `RecomputeGroups_locked()`; index-list kernel overload.
- `physics/ephemeris_body.hpp`: cutoff at :1368/:1435 + mirrors :1235/:1195/:1481; restructure dispatcher :1514-1549; hook at :338; thread `soi_cutoff_squared_` through ctor :96-171.
- Schema (flag): `physics/massive_body.hpp` SOI radius source.
