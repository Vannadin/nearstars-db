---
title: Universe Sandbox vs Principia n-body engine comparison
status: active
created: 2026-05-30
---
# Universe Sandbox vs Principia n-body engine comparison

**NearStars connection.** NearStars feeds **Principia** (the n-body KSP
mod) an ICRF Cartesian state `(x, y, z, vx, vy, vz)` per component at
`JD2433282.5`, and Principia forward-integrates the whole system. A
possible future direction is a **custom Principia branch** (with 슐츠).
This note therefore asks a different question than the Stellarium
comparison did: not "is our convention right" but **"what has Universe
Sandbox done for real-time interactive n-body that a Principia branch
could plausibly borrow — and what is downstream of US²'s goals and
should *not* be borrowed."** See
[`stellarium-binary-orbit-comparison.md`](stellarium-binary-orbit-comparison.md)
for the sibling note.

**⚠ Source-quality caveat (important).** The Stellarium note cited
**actual source lines** (`Star.hpp#L364-L373`) because Stellarium is
open source. **Universe Sandbox is closed-source commercial software.**
Everything here is from public developer statements (dev blog, FAQ,
Steam forum posts by team members) or the team-maintained wiki. Claims
are tagged:
- **[DEV]** — direct developer statement (blog / FAQ / forum quote).
- **[WIKI]** — team-maintained wiki, not a verbatim dev quote.
- **[INFER]** — inferred from observed behavior / design.
- **[NO SRC]** — could not be sourced; treat as unknown.

The Principia side is open source and high-confidence (wiki + shipped
`sol_numerics_blueprint.cfg` + source headers); divergence flags there
are minor wording gaps, not fidelity gaps.

**Scope.** Read-only research. No code changes in this repo.

**External references.**
- Universe Sandbox dev blog: https://universesandbox.com/blog/
- US² FAQ: https://universesandbox.com/faq/ (+ legacy /faq/original/)
- US² integrator forum thread (lead n-body dev "Greenleaf"):
  https://steamcommunity.com/app/230290/discussions/0/520518053429453785/
- Principia wiki: https://github.com/mockingbirdnest/Principia/wiki
- Principia Jool-stability note (the symplectic rationale):
  https://github.com/mockingbirdnest/Principia/wiki/On-the-dynamical-stability-of-Principia's-modified-Jool-system
- Our pipeline: [`../docs/reference/binary-epoch-pipeline.md`](../docs/reference/binary-epoch-pipeline.md),
  [`../docs/reference/principia-cfg-reference.md`](../docs/reference/principia-cfg-reference.md)

---

## 1. Executive summary

| Question | Answer |
|----------|--------|
| Same numerical goal? | **No.** US² optimizes for **real-time interactivity** (grab/throw bodies, collisions, fragmentation, responsive at any speed). Principia optimizes for **deterministic, long-term-stable forward integration** of a fixed initial state under time-warp. |
| Default integrator | US²: **PEFRL** (4th-order symplectic) [WIKI], from a *selectable suite* incl. velocity-Verlet, RK4, RKF, Adams, Hermite, Forest-Ruth [DEV]. Principia: **`QUINLAN_TREMAINE_1990_ORDER_12`** (12th-order symmetric linear multistep, conjugate-symplectic) — fixed for *all* celestials. |
| Timestep | US²: **adaptive**, controlled by a user-facing **tolerance in units of length** via step-doubling error estimate [DEV]. Principia: **fixed** (10 min ephemeris / 10 s vessel history); adaptive only for vessel *prediction*. |
| Accuracy/speed control | US²: **exposed to the user** — sim-speed slider is an auto-limited target, capped by the single worst-error body [DEV+WIKI]. Principia: not user-tuned at runtime; correctness is a property of the fixed step + symplecticity. |
| Relativity | US²: **Newtonian only**, no GR; speed-of-light gravity + PN corrections are *aspirational* [DEV]. Principia: Newtonian + geopotential spherical harmonics (J₂ / full C̄ₙₘ,S̄ₙₘ); no GR either. |
| Collisions / mergers / Roche | US²: **first-class** — overlap detection, momentum/energy-conserving merge, cratering, fragmentation, Roche tidal disruption [DEV+WIKI]. Principia: **none** — bodies are point masses on continuous trajectories. |
| Many-body scaling | US²: direct O(N²) default, **Barnes-Hut tree** opt-in for thousands of fragments [DEV]; CPU multicore via Unity DOTS/Burst, **not GPU** [DEV]. Principia: massive bodies n-body, vessels massless test particles; N is small (~planets+stars). |
| Determinism / reversibility | Principia: fixed-step **symmetric** methods → deterministic, time-reversible, no secular energy drift [DEV-rationale]. US²: adaptive + collisions + RNG fragments → **not** reproducible by design. |
| Should a Principia branch borrow from US²? | **A short list, mostly UX/ergonomics, not the core integrator.** See §6. Most US² choices follow from "interactive sandbox," which KSP/Principia is not. |

---

## 2. What Universe Sandbox actually does

Confidence is lower than the Stellarium note — no source to read. Tags
as defined above.

### 2.1 Integrator suite, not one integrator

**[DEV]** The lead n-body dev ("Greenleaf" on Steam, identified as
Thomas Grønneløv / "Naml") listed the historical set: explicit &
semi-implicit Euler, RK2, RK4, RKF (Runge-Kutta-Fehlberg), Adams-
Bashforth 6th, Adams-Moulton 6th, Hermite 5th, **PEFRL**, and
**Forest-Ruth**. A "large NBody rewrite" temporarily cut most; they
were being re-added. The currently exposed default is **PEFRL** (a
4th-order symplectic position-extended Forest-Ruth-like method) [WIKI];
velocity-Verlet is the explicitly documented Verlet variant [DEV]:
> `x(t+dt)=x(t)+v(t)·dt+0.5·a(t)·dt²`, `v(t+dt)=v(t)+0.5·(a(t)+a(t+dt))·dt`

Stated philosophy [DEV]: *"let the user pick the right integrator for
the job, and set a sensible default … fast chaotic sim → speed matters;
long-running stability analysis → accuracy matters."*

### 2.2 Adaptive timestep with a user-facing length tolerance

**[DEV]** This is the most interesting design point. The user sets a
**tolerance in units of length** = max positional error per step. Each
step the engine takes one full `dt` and two `½dt` steps, compares them
(standard step-doubling), and shrinks the step to stay under tolerance:
> *"the integration step length will be adjusted to not generate a
> position error larger than this tolerance."*

**[DEV]** The sim-speed slider is therefore a **target, auto-limited**
to preserve accuracy. **[WIKI]** The UI even names *which single body*
is currently the worst-error offender capping your speed. **[DEV]**
Raise tolerance → faster but orbits may "fall apart" as error
accumulates.

### 2.3 Newtonian only

**[DEV]** *"the physics in Universe Sandbox is currently only
Newtonian."* No GR. Gravitational waves explicitly out of scope of an
n-body method. Aspirational future: gravity propagating at `c` instead
of instantaneously, and possible post-Newtonian corrections. No GR
toggle exists [NO SRC for any implemented GR effect].

### 2.4 Collisions, mergers, fragmentation, Roche

**[DEV+WIKI]** First-class, and the product's signature feature:
- Collision = overlap detection; resolve by **merge** ("Combine") or
  fictional elastic **bounce**, conserving momentum/energy, with impact
  heating.
- Cratering: impact energy melts a mass fraction of the larger body;
  melted mass → fragments with random mass/position/velocity drawn to
  conserve mass/momentum/energy.
- Three fragmentation types: **collision**, **Roche** (tidal — computed
  from the same per-step gravity/tidal-force evaluation), **spin**.
- Fragment count auto-capped for performance.

**[INFER]** Tidal (Roche) evaluation and overlap detection both ride on
the per-step gravity computation; fragments become new gravitating
bodies. Exact ordering within a step not sourced.

### 2.5 Scaling: O(N²) → Barnes-Hut, CPU not GPU

**[DEV]** Default gravity is direct all-pairs **O(N²)**. For thousands
of fragments/ring/galaxy particles, a **Barnes-Hut tree** is the
scaling answer (slightly reduced accuracy, tunable "gravity tree
ratio") — shippable as an experimental opt-in [WIKI]. The 2025 rewrite
moved the engine to **Unity DOTS / ECS / Burst / Job System** —
cache-friendly, multithreaded **CPU**. **[NO SRC]** that the gravity
step runs on GPU (a search snippet claiming GPU appears to conflate it
with unrelated academic papers).

### 2.6 Precision / frame

**[NO SRC]** No primary statement confirming float64 positions or any
floating-origin / origin-rebasing scheme. Tolerance being "in units of
length" is the only adjacent fact. Galaxy-scale sims are self-described
as "only representative and not very accurate" — a *physics* caveat,
not a floating-point one.

---

## 3. What Principia does (high-confidence, open source)

### 3.1 Fixed-step symplectic for celestials

Default ephemeris integrator: **`QUINLAN_TREMAINE_1990_ORDER_12`** — a
12th-order **symmetric linear multistep** method, **fixed step 10 min**.
Conjugate-symplectic → **no secular energy drift**, only bounded
oscillation (shrinkable by reducing the step). Stated rationale (Jool
note):
> *"being conjugate-symplectic, it does not exhibit energy drift … our
> observer cannot measure the energy at various times and notice an
> unphysical systematic drift."*

Other shipped fixed-step families: Blanes-Moan SRKN, McLachlan /
McLachlan-Atela / Okunbor-Skeel SPRK, Quinlan-1999 SLMS.

### 3.2 Adaptive only for the vessel future

Vessel **prediction / flight-plan** uses **`DORMAND_ELMIKKAWY_PRINCE_1986_RKN_434FM`**
(embedded RKN 4(3)4, adaptive, tolerances 1 mm / 1 mm·s⁻¹) — **not
symplectic**. Vessel *history* is fixed-step Quinlan-1999 order 8A at
10 s. So Principia already runs an **adaptive embedded-RKN** internally;
it just confines it to test-particle futures, not the celestial
backbone.

### 3.3 Geopotential, precision, epoch, determinism

- **Geopotential:** IERS-2010 normalized spherical harmonics, or single
  unnormalized J₂ (`J₂ = −C̄₂₀·√5`). `geopotential_tolerance` prunes
  small terms for speed.
- **Precision:** binary64 doubles, SI units, native C++14 via P/Invoke.
- **Frame/epoch:** Cartesian state at `solar_system_epoch` (TT),
  pre-integrated to `game_epoch`; IAU-2009 pole/rotation convention.
  Matches NearStars's `JD2433282.5`.
- **Determinism:** fixed-step *symmetric* methods are deterministic and
  time-reversible (the property they are chosen for). The adaptive
  vessel-prediction segment is not bit-reversible.
- **Warp:** step stays **fixed** under time-warp; warp just runs more
  steps per wall-clock second. Smooth to 6,000,000× with no vessels;
  janky past ~1,000,000× with vessels.

---

## 4. The core philosophical split

| | Universe Sandbox | Principia |
|---|---|---|
| **Goal** | Real-time *interactive* sandbox — grab, throw, smash, watch | Deterministic forward integration of a *fixed* system for gameplay |
| **Default integrator order** | 4th (PEFRL) | 12th (Quinlan-Tremaine) |
| **Step control** | Adaptive, user-facing length tolerance | Fixed step, no runtime knob |
| **What gives when you go fast** | Accuracy degrades gracefully; orbits may "fall apart" | Nothing — same step, just more wall-clock; correctness preserved |
| **Editing the system live** | Central feature | Not a use case; state comes from the initial-state cfg |
| **Collisions/mergers/Roche** | First-class | Absent (point masses) |
| **Reproducibility** | Not a goal (RNG fragments, adaptive) | Deterministic & reversible by construction |

The single sentence: **US² makes the integrator adapt to keep an
interactive sim alive; Principia fixes the integrator so a long sim
stays physically honest.** Almost every other difference falls out of
that.

Note the *inversion* of the usual "game = less accurate" intuition for
the **celestial backbone**: Principia's default is a 12th-order
symplectic method — *higher* order and stronger long-term guarantees
than US²'s 4th-order default — because Principia integrates a *known,
relatively stable hierarchy*. US² must survive *arbitrary
user-constructed chaos plus collisions in real time*, so it picks a
lower-order adaptive scheme with graceful degradation. Different
problems, not "one is better."

---

## 5. Where they agree

Less than the Stellarium case, but real:
1. **Newtonian gravity, no GR.** Both treat GR as out of scope for an
   n-body engine (US² aspirationally; Principia ships geopotential
   harmonics but no relativity). For NearStars's stellar/planetary
   scales this is the right call in both.
2. **Symplectic-by-default for the stable case.** US²'s default PEFRL
   and Principia's Quinlan-Tremaine are both **symplectic/energy-
   conserving** families. Both teams independently concluded that for
   long-running gravitational systems you want a symplectic method, not
   a naive RK4 that drifts. (US² even keeps Euler around "primarily to
   show how bad it is" [DEV].)
3. **Adaptive embedded methods for the hard/uncertain part.** US² uses
   adaptive step-doubling everywhere; Principia uses adaptive embedded
   RKN for vessel prediction. Both reach for adaptive control where the
   trajectory is sensitive — they just draw the boundary differently.

---

## 6. Implications for a custom Principia branch

The honest headline: **most of what makes US² impressive is downstream
of "interactive sandbox," which KSP/Principia is not.** You don't throw
stars around in KSP; you fly vessels through a deterministic,
warp-stable system. So the borrow list is short and mostly ergonomic.
What is actually worth considering, in rough priority:

**Worth seriously considering**
1. **User-facing accuracy/speed tolerance + "worst-offender body"
   readout.** US²'s best UX idea. Principia's correctness is invisible
   to the player (fixed step, no dial). A branch could expose a single
   "max positional error" tolerance and surface *which body* is
   currently the binding constraint on smooth warp. This is portable
   *without* touching the symplectic celestial integrator — it would
   live in the diagnostic/UX layer. **Caveat:** Principia's whole
   stability argument rests on the *fixed* step; a naive "make the
   celestial step adaptive" would break conjugate-symplecticity and the
   no-drift guarantee. The borrow is the *readout and a step-size
   chooser*, not adaptive celestial stepping.

**Conditional — only if the branch's goal includes it**
2. **Collisions / mergers / Roche disruption.** If the branch wants
   bodies to *collide and merge* (US²'s signature), there is no
   Principia machinery for it — US² is the reference design (overlap
   detection, momentum/energy-conserving merge, fragment spawning,
   per-step tidal Roche). This is a large feature, fundamentally at
   odds with Principia's "continuous trajectory of point masses" model,
   and would need its own design. Flag, don't assume.
3. **Barnes-Hut tree for many-body.** Only relevant if the branch
   simulates *thousands* of bodies (debris rings, captured swarms).
   NearStars's footprint is ~tens of stars/planets, where direct O(N²)
   is trivially fine. Defer unless the branch's scope explicitly grows
   N by orders of magnitude.

**Probably not worth borrowing**
4. **Lower-order adaptive celestial integrator.** US²'s adaptive PEFRL
   approach exists to survive arbitrary chaos in real time. For a fixed,
   curated NearStars system, Principia's fixed 12th-order symplectic is
   *strictly better* for the long-term-stability goal. Adopting US²'s
   approach here would be a regression.
5. **GPU offload.** US² explicitly didn't do this (CPU/DOTS/Burst). No
   reason for a Principia branch to either at NearStars's N.

**Open design question for the branch:** the genuinely hard,
interesting tension is #1 + #4 together — *can you keep Principia's
fixed-step symplectic guarantee for the celestial backbone while giving
the player a US²-style accuracy/speed dial?* The clean answer is
probably: expose **step-size selection** (e.g. 10 min ↔ 2.5 min, the
Richardson pair Principia already validates against) plus the
worst-offender diagnostic, rather than per-step adaptivity. That keeps
the symplectic property while delivering the UX. This is the thing to
prototype first with 슐츠.

---

## 7. Open questions

- **US² float precision & floating-origin.** [NO SRC]. If the branch
  ever needs to interoperate or cross-check against US² numerically,
  we'd need to confirm float64 and any origin-rebasing — currently
  unknown and unsourced.
- **US² collision-step ordering.** [INFER only]. Whether overlap
  resolution runs before/after the integrator advance within a step is
  not sourced; matters only if we ever design Principia-side collisions.
- **PEFRL exact coefficients in current US² build.** [WIKI] says PEFRL
  default; the precise method/order in the shipped build isn't
  dev-confirmed post-rewrite.
- **Does the branch want collisions/mergers at all?** This single
  decision determines whether §6 #2 (a large US²-derived feature) is in
  or out of scope. Needs a product call before any engine work.

## Related

- [stellarium-binary-orbit-comparison](stellarium-binary-orbit-comparison.md) — the sibling note; that one *could* cite source lines (open source), this one cannot (US² is closed)
- [binary-epoch-pipeline](../docs/reference/binary-epoch-pipeline.md) — how NearStars produces the Cartesian state Principia integrates
- [principia-cfg-reference](../docs/reference/principia-cfg-reference.md) — the Principia cfg/numerics layer this compares against
