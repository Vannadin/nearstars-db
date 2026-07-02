---
title: "Principia interstellar-precision branch — design draft"
status: draft
created: 2026-07-02
audited_against: mockingbirdnest/Principia master @ 440310a9
supersedes_line_numbers_in: schultz-dev0/principia-docs/interstellar-audit.md (head cc6522fc9)
---

# Principia interstellar-precision branch — design draft

**One-line goal.** Let a single Principia simulation hold **Sol and one (or a
few) remote star systems at once**, with **full per-star orbital precision** —
so a vessel can fly a low orbit around a planet of Alpha Centauri while Sol's
system is co-simulated, and stars perturb each other physically.

This is a **design draft**, not a fork. It is grounded in a fresh read of the
current `master` (head `440310a9`) — the file:line citations below were
re-verified against that head, superseding the older audit written against
`cc6522fc9`. The deliverable is the architecture, the concrete change sites,
and a staged prototype plan that 슐츠 (or we) can implement from.

Sibling docs: `schultz-dev0/principia-docs/interstellar-audit.md` (the original
audit), `theoretical_implementation.md` (the data-only Option 1),
`../universe-sandbox-nbody-comparison.md` (the separate integrator/UX question —
**out of scope here**).

---

## 1. The problem, stated precisely

Principia stores every position as **three IEEE-754 `double`s in one flat
inertial frame**. The chain is exact and leaves no room for interpretation:

- `Position<Frame> = Point<Displacement<Frame>>` → `Vector<Length, Frame>` →
  `R3Element<Length>` → `Quantity<Length>` = a single `double magnitude_`
  (`quantities/quantities.hpp:83`, `geometry/point.hpp:66`,
  `geometry/grassmann.hpp:67`, `geometry/r3_element.hpp:75-91`).
- A `double` resolves ≈ `2⁻⁵² · |x|`. In metres:

| Distance from frame origin | ULP (position resolution) |
|---|---|
| 1 AU | ≈ 33 µm |
| Sol → Pluto | ≈ 1.6 mm |
| Sol → **Alpha Centauri** (4.0e16 m) | **≈ 9 m** |
| Sol → Barnard (5.6e16 m) | ≈ 12 m |
| Sol → Trappist-1 (3.8e17 m) | ≈ 84 m |

The moment one coordinate origin must span Sol → another star, positions near
that star lose metres-to-tens-of-metres of resolution — fine for cruise, fatal
for orbital mechanics (a low orbit needs sub-metre precision to integrate
stably over years).

**Where the loss actually bites — the cancellation site.** It is not the
storage alone; it is the gravity kernel. In
`physics/ephemeris_body.hpp:1366`:

```cpp
Displacement<Frame> const Δq = position_of_b1 - positions[b2];   // :1366
```

`positions` here is `q_stage`, which the integrator forms by **flattening the
`DoublePrecision` state to plain doubles** and discarding the error term
(`integrators/symplectic_runge_kutta_nyström_integrator_body.hpp:114`). So for
a planet and its star, both ≈ 4e16 m from a shared origin, `Δq` is a
difference of two nearly-equal large doubles → **catastrophic cancellation**,
leaving ~5 significant digits in a ~1e10 m orbital displacement. The same
`Δq = rᵢ − rⱼ` idiom recurs in the massless kernel (`:1433`), the Jacobian
(`:1184-1193`), jerk (`:1230-1232`), and the potential — one helper covers all.

**Why `DoublePrecision<T>` does not already save us.** It is compensated
summation (`{T value; Difference<T> error;}`, `numerics/double_precision.hpp:59-60`)
and *is* used inside the integrator state (`ordinary_differential_equations.hpp:167-171`)
— but it compensates the **step-vs-running-total** roundoff, not the
**value-minus-value** cancellation between two star systems, and the error term
is dropped both when forming `q_stage` (`:114`) and when appending to
trajectories (`ephemeris_body.hpp:1111`). Storage is single-double.

**Why the two obvious options fail** (`theoretical_implementation.md`):
- *Sol at origin, stars as perturbers (data-only).* Works for **stellar
  motion** (a star's pull on Sol's planets), needs zero code — but `r_planet −
  r_star` cancels as above, so **no remote-planet precision**.
- *Galactic-centre origin.* Sol itself lands at ~55 km resolution — unplayable
  before a single planet is placed.

Neither lets you *play* at the remote star. That is the gap this branch closes.

---

## 2. What already protects us (this narrows the branch a lot)

A key finding from the plugin audit: **rendering and in-bubble vessel physics
are already floating-origin-safe.** We do *not* have to solve display.

- **Vessel World is re-anchored every frame.** `Plugin::BarycentricToWorld`
  places Unity's `World::origin` at the reference (root) part
  (`ksp_plugin/plugin.cpp:702-752`); the adapter drives it each
  `FixedUpdate` and shifts every celestial by the offset
  (`ksp_plugin_adapter.cs:1596-1670`). Near-vessel coordinates stay small
  regardless of barycentric magnitude.
- **The P/Invoke boundary is all `double`** (`XYZ`/`QP` = `double`,
  `serialization/journal.proto:24-29`, `interface.cs:52-67`).
- **The KSP hand-off is parent-relative** `AliceSun`
  (`VesselFromParent`/`CelestialFromParent` → `RelativeDegreesOfFreedom<AliceSun>`,
  `ksp_plugin/plugin.hpp:334-345`), mirroring KSP's own hierarchical `Orbit`.
  Parent-relative quantities are intrinsically scale-free — **this is the
  natural seam** a per-star design leans on.

So the breakage is **concentrated in three places**, not spread everywhere:

1. **The single `Ephemeris<Barycentric>`** — integration + Chebyshev fitting
   run at 1 mm tolerance (`ksp_plugin/integrators.cpp:34,41,80`) against a ~4 m
   ULP at a remote star: the fit cannot converge and inter-body dynamics carry
   metre-level noise. *This is the real work.*
2. **Single-sun assumptions** — `Plugin::sun_` (`plugin.hpp:588`, uniqueness
   CHECK at `plugin.cpp:250-256`) and the Sun-anchored map view
   (`renderer.cpp:197-205`, fed `Planetarium.fetch.Sun.position`).
3. **The map-view float boundary** — `ScaledSpacePoint {float x,y,z}`
   (`planetarium.hpp:44-46`) collapses when viewing a system 1e16 m from the
   anchor; needs re-centring on the local star (adapter-side).

---

## 3. The architecture — a per-star *subsystem* ephemeris

The three subsystem audits (geometry, dynamic frames, ephemeris) converge on
one answer. The offset that carries interstellar distance **must be split out
of the stored `Position` before it is ever written down** — not injected at the
transform layer, where the operands are already lossy
(`geometry/affine_map_body.hpp:42`). Concretely:

### 3.1 State representation

Partition the ephemeris bodies into **subsystems** `S(i)` (Sol = subsystem 0,
each remote star = its own subsystem). Then:

- Each subsystem `S` has an **origin** `O_S` (its barycentre), carried in the
  global inertial `Barycentric` frame as a **`DoublePrecision<Position<Barycentric>>`**
  — this is the only place interstellar magnitude lives, and double-double gives
  it ~32-digit headroom.
- Each body's **stored position is local**: `q̃ᵢ = qᵢ − O_{S(i)}`, magnitude
  ≤ system size (~1e13 m for a wide binary, ~1e11 m for planets) → **sub-mm in
  plain `double`**. No storage-format change to `Position` itself; it is still
  `{double x,y,z}`, just measured from a near origin.
- Inter-origin offsets `Δ_{AB} = O_B − O_A` are obtained by
  `DoublePrecision` subtraction (`TwoDifference`, Point−Point→Vector overload,
  `numerics/double_precision.hpp:104-119`) — exact, no cancellation surprises.

The `Frame::is_inertial` static_assert (`ephemeris.hpp:69`, `reference_frame.hpp:47`)
**stays** — subsystem origins are *translations*; the axes remain the shared
inertial `Barycentric` orientation. We do **not** rotate per star.

### 3.2 Gravity kernel — the same/cross-subsystem split

The pairwise kernel (`ephemeris_body.hpp:1346-1410`, dispatcher `:1505-1552`)
gets a single new helper `Displacement Δq(b1, b2)`:

- **Same subsystem** (`S(b1) == S(b2)`): `Δq = q̃[b1] − q̃[b2]` — *identical to
  today's `:1366`*, now cancellation-free because both operands are small.
  **The hot Sol-internal loop is unchanged and zero-cost.**
- **Cross subsystem**: `Δq = (q̃[b1] − q̃[b2]) + Δ_{S(b2)S(b1)}`. Note the
  precision demand here is *low*: at 4e16 m separation the cross-term
  acceleration is ~1e-14 of intra-system terms, so magnitude — not digits — is
  what matters. Compute in `DoublePrecision` and take `.value`; the win is
  entirely in keeping the *intra*-subsystem `Δq` exact.

Because subsystem membership is a property of the body index, the dispatcher
loops (`:1514-1548`) iterate **subsystem-blocked pair ranges**, so same-vs-cross
is a **loop-level branch, not a per-pair test** — no hot-path cost. The
oblateness/geopotential branch (`:1381-1407`) consumes the same `Δq`, so it is
fixed for free.

### 3.3 Origin motion — the hard sub-decision (flagged, not yet chosen)

Subsystem origins are not fixed: stars accelerate each other. Two options,
to be decided with 슐츠 by prototype:

- **(A) Integrate each origin as an extra ODE variable** of type
  `DoublePrecision<Position<Barycentric>>`, kept in full double-double through
  the RHS. Cleanest physically; requires plumbing the `error` term into
  `q_stage` (today dropped at `symplectic_..._body.hpp:114`) for the origin
  variables only.
- **(B) Kinematic / periodic re-anchoring.** Advect origins by their measured
  space velocity (interstellar tides are ~1e-15 of local gravity, negligible
  over KSP timescales — `interstellar-audit.md §7.4`), and periodically **fold**
  accumulated origin drift back into local coordinates via `QuickTwoSum` — a
  "rebasing" step between fixed integration steps in `Prolong`. Simpler; exact
  enough because the coupling is negligible.

**Leaning (B)** for the first prototype: interstellar gravitational coupling is
physically negligible, so integrating origins to full precision (A) is
over-engineering until proven necessary. (B) keeps the integrator loop
untouched. Revisit only if a tight stellar binary (α Cen A–B, 80 yr) shows the
origin-drift fold introducing visible error.

### 3.4 Trajectory storage

`AppendMassiveBodiesStateToTrajectories` (`ephemeris_body.hpp:1101-1116`) today
appends the global `positions[i].value` (`:1111`). It must instead append the
**local** `q̃ᵢ` to each body's `ContinuousTrajectory`, plus maintain a
**per-subsystem origin trajectory** (`O_S(t)` — a small `ContinuousTrajectory`
or, under option B, an analytic `O_S₀ + v·t` plus fold points). Newhall/Chebyshev
fitting (`continuous_trajectory.hpp:186-201`) is **translation-invariant**, so it
fits the local series unchanged — and its 1 mm `tolerance_` finally becomes
*achievable* at a remote star. `EvaluatePosition` callers that need a global
position compose `q̃ + O_S`; callers that feed a star-local plotting frame
consume `q̃` directly (preferred).

### 3.5 Frame / plotting layer — reuse what exists

No new frame *algebra*. Principia already re-expresses trajectories in runtime
frames via `ReferenceFrame<InertialFrame, ThisFrame>`
(`physics/reference_frame.hpp:45-47`) and composes `RigidMotion`s
(`physics/rigid_motion_body.hpp:173`). A **star-local plotting frame** is a new
`RigidReferenceFrame` subclass built exactly like
`BodyCentredNonRotatingReferenceFrame`
(`body_centred_non_rotating_reference_frame_body.hpp:25-79`) — except its
`ToThisFrameAtTime` builds the transform from **star-local** ephemeris
coordinates (`q̃`), never round-tripping vessel positions through absolute
`Barycentric` doubles. `GravitationalAcceleration(t, q)`
(`rigid_reference_frame.hpp:183-185`) gets a star-local overload so accelerations
near the remote star are computed from small local displacements.

We need **a handful of new compile-time frame tags** (one inertial-quality tag
per star, exactly as `Barycentric` is declared, `ksp_plugin/frames.hpp:39-43`),
each paired with a **runtime `DoublePrecision` anchor** — *not* a rewrite of the
frame templates.

### 3.6 Plugin layer

- **Multi-sun.** Remove the `sun_` uniqueness assumption (`plugin.hpp:588`,
  CHECK `plugin.cpp:250-256`); the plugin holds a **set of stars**, and the
  active one is chosen by the vessel's current subsystem.
- **Map-view anchoring.** `Renderer::BarycentricToWorld` (`renderer.cpp:197-205`)
  switches World anchoring from Sol's Sun to the **local star**; the adapter
  supplies that star's `ScaledSpace` position instead of
  `Planetarium.fetch.Sun.position`.
- **ScaledSpace float boundary.** `plotting_to_scaled_space`
  (`interface_planetarium.cpp:100-109`) must subtract a **local** scaled-space
  origin before the `float` cast (`planetarium.hpp:44-46`) — re-centre on the
  local system, adapter-side.
- **The seam stays put.** The parent-relative `AliceSun` APIs
  (`plugin.hpp:334-345`) need **no change** — they are already hierarchical and
  scale-free.
- **Serialization / save-compat.** `Plugin::WriteToMessage` (`plugin.cpp:1512`)
  persists one ephemeris + `Barycentric` trajectories; the save format grows a
  subsystem partition + per-subsystem `DoublePrecision` origins.
  `serialization::DoublePrecision` already exists
  (`double_precision.hpp:55-57`), so the wire format extension is small; new
  star-frame enum values go in `serialization/geometry.pb`'s `Frame` enum.

---

## 4. Why not the alternatives

| Alternative | Verdict |
|---|---|
| **Compile-time frame nest** (`Frame<Parent, …>`) | Rejected. `Frame` is an empty tag (`frame.hpp:52-79`); it cannot usefully carry an offset, and parameterizing it ripples through every template in the codebase for zero gain. Nesting belongs in the physics layer. |
| **Galactic-centre origin** | Rejected. Sol itself resolves to ~55 km (`theoretical_implementation.md`). Unplayable. |
| **`DoublePrecision<Position>` stored everywhere** | Rejected as the primary mechanism. Doubles storage/bandwidth of all trajectories, and the problem is **cancellation**, not dynamic range — a local origin removes the large operands entirely, so plain double suffices intra-subsystem. `DoublePrecision` is used *only* for the few inter-origin offsets. |
| **Data-only perturber (Option 1)** | Kept as a **separate, shippable milestone** — see §5 stage 0. It gives stellar-motion coupling with zero code, just not remote-planet play. |

---

## 5. Staged prototype plan

Ordered so each stage is independently testable and de-risks the next.

- **Stage 0 — data-only perturber (no code).** Add Alpha Centauri A/B to
  `sol_gravity_model.proto.txt` + initial state, per `theoretical_implementation.md`.
  Verifies the Gaia→ICRS→Cartesian pipeline and that the ephemeris ingests a
  second star at all. Ships today; establishes the baseline error (the ~9 m we
  are removing).
- **Stage 1 — subsystem partition + local storage (headless).** In
  `physics/ephemeris*`, add the subsystem id, local-origin state, the `Δq`
  helper (§3.2), and origin handling option B (§3.3). Validate in a C++ test
  (mirror `trappist_dynamics_test.cpp`): integrate Sol + α Cen for 100 yr and
  confirm intra-α-Cen orbital elements are now sub-mm-stable where the flat
  frame gave metre-level noise. **No KSP yet.** This is the core proof.
- **Stage 2 — star-local plotting frame.** Add the `RigidReferenceFrame`
  subclass (§3.5) + frame tags; verify a vessel state near α Cen b round-trips
  through the local frame without precision loss.
- **Stage 3 — plugin multi-sun + map anchoring** (§3.6). The KSP-facing work:
  multi-star plugin state, local-star World/ScaledSpace anchoring, save format.
  Needs a real KSP build — 슐츠's domain (C#/adapter + Principia build chain).
- **Stage 4 — vessel system-crossing.** Hand a vessel's `DiscreteTrajectory`
  from one subsystem frame to another mid-flight. Downstream of everything else;
  the interstellar-cruise use case (may be gated behind the warp/relativity
  profile per `project_nearstars_interstellar_expansion`).

Stages 0–2 are buildable/testable **without a KSP install** (Principia's test
suite is standalone C++), which is what makes a meaningful draft achievable on a
short horizon; stages 3–4 are the heavier KSP-integration lift for 슐츠.

---

## 6. Change-site map (the code-level sketch)

| Layer | File:line (master 440310a9) | Change |
|---|---|---|
| Gravity kernel | `physics/ephemeris_body.hpp:1366,1433,1184-1193,1230-1232` | Replace `Δq = rᵢ − rⱼ` with subsystem-aware helper (§3.2) |
| Dispatcher | `physics/ephemeris_body.hpp:1505-1552` | Iterate subsystem-blocked pair ranges |
| State layout | `physics/ephemeris_body.hpp:95-171` | Partition bodies by subsystem; seed local positions; add per-subsystem origin |
| Trajectory append | `physics/ephemeris_body.hpp:1101-1116` | Append local `q̃`; maintain origin trajectory (§3.4) |
| Public accessors | `physics/ephemeris.hpp:154-159,253-285` | Local/global variants of `EvaluateAllPositions`, `ComputeGravitationalAcceleration…` |
| Origin motion | `integrators/symplectic_..._body.hpp:114` | (Only if option A) plumb `.error` through `q_stage` for origin vars |
| DoublePrecision offset | `numerics/double_precision.hpp:104-119` | (Use as-is) `TwoDifference` for exact inter-origin `Δ` |
| Star-local frame | new `physics/star_centred_inertial_reference_frame*.hpp` | Subclass of `RigidReferenceFrame`, pattern from `body_centred_non_rotating_…` |
| Frame tags | `ksp_plugin/frames.hpp:39-43` | One inertial tag per star + `DoublePrecision` anchor |
| Multi-sun | `ksp_plugin/plugin.hpp:588`, `plugin.cpp:250-256` | Set of stars; drop `sun_` uniqueness |
| Map anchoring | `ksp_plugin/renderer.cpp:197-205` | Anchor World on local star |
| ScaledSpace | `ksp_plugin/interface_planetarium.cpp:100-109`, `planetarium.hpp:44-46` | Local scaled-space origin before float cast |
| Save format | `ksp_plugin/plugin.cpp:1512,1572-1575`, `serialization/geometry.pb` | Subsystem partition + `DoublePrecision` origins + star frame enums |
| Untouched (seam) | `ksp_plugin/plugin.hpp:334-345` | Parent-relative `AliceSun` — no change |

---

## 7. Risks & open questions

1. **Origin-motion choice (A vs B, §3.3).** Prototype α Cen A–B (80 yr binary)
   under option B; if the rebasing fold shows visible secular error, escalate to
   A. *Decide by measurement, not up front.*
2. **Symplecticity across a rebasing fold.** Option B's periodic re-anchoring
   must not break the fixed-step symmetric method's no-drift guarantee. The fold
   is an exact `QuickTwoSum` translation of all coordinates by the same vector —
   it commutes with the integrator in principle, but this needs an explicit
   energy-drift test (mirror the Jool-stability methodology).
3. **Chebyshev fit degree at the subsystem boundary.** Confirm the local series
   degree/tolerance behaves once positions are small — expected to *improve*
   (§3.4), but verify.
4. **Serialization migration.** Old saves (single flat ephemeris) must still
   load — the subsystem partition needs a "everything is subsystem 0" default.
5. **KSP ScaledSpace / PQS float paths** (`ksp_plugin_adapter.cs:1663-1665`
   writes absolute doubles into KSP `CelestialBody.position`). The remote
   system's bodies become ~1e16 m in KSP's own float-laced code unless the
   adapter re-centres KSP's ScaledSpace too. This is the least-understood
   KSP-side risk; needs a spike in stage 3.
6. **Build chain.** Principia's build (bespoke MSVC/clang, large) is the
   practical gate on stages 3–4 — 슐츠's environment.

---

## 8. References

- `schultz-dev0/principia-docs/interstellar-audit.md` — original audit (§7 =
  frame-nesting requirement).
- `schultz-dev0/principia-docs/theoretical_implementation.md` — data-only
  Option 1 + the two rejected origins.
- `../universe-sandbox-nbody-comparison.md` — the separate integrator/UX
  borrow question (not this branch).
- File:line citations above verified against `mockingbirdnest/Principia`
  master `440310a9` (2026-07-02).
