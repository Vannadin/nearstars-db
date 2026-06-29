---
title: Relativity mod — sub-light special-relativity gameplay layer
status: active   # active | promoted | archived
created: 2026-06-29
---

# Relativity mod — sub-light special-relativity gameplay layer

**NearStars connection.** Interstellar travel is the post-RP-1 endgame
expansion (see `project_nearstars_interstellar_expansion`). Gate-0
feasibility concluded that reaction propulsion cannot reach relativistic
cruise quickly, and warp mods are Principia-incompatible — so the chosen
direction is *gameplay first*. This note scopes a special-relativity
**gameplay layer** that makes the light barrier *felt* without faster-than-light
cheating: as a vessel approaches `c`, the thrust that actually accelerates it
falls away, while the crew's proper-time resource burn slows. It is the
sub-light companion to (deferred) time-dilation clock mechanics.

**Scope.**
- **In** — design of the core mechanic (thrust scaling, resource scaling,
  dashboard) and an optional 3-tier visual layer. Reference frame choice.
  Principia/SigmaBinary compatibility reasoning. Physics grounding.
- **Out** — actual clock time dilation / time-warp manipulation (deferred
  to a later "time" element). Energy/fuel mass-ratio blow-up economics.
  General-relativistic effects (this is special relativity only).
- **No code changes from this note.** It is a scoping document. Implementation
  is a C# / shader plugin and falls to Schultz
  (see `project_nearstars_mod_plugins_schultz`).

**External references.**
- Principia (Newtonian n-body integrator, barycentric inertial frame):
  https://github.com/mockingbirdnest/Principia
- Singularity (KSP black-hole gravitational-lensing screen-space
  post-process — proves the relativistic-aberration shader pipeline is
  viable in KSP). Repo URL to be confirmed before hand-off.
- Kerbalism (time-based resource/life-support consumption — the hook for
  proper-time resource scaling).

---

## 0. What the player experiences (no math)

You never see γ or a formula. The whole layer is **two opposing effects near
light speed**, plus one twist:

1. **The faster you go, the less your engine accelerates you.** Like a cart that
   gets heavier the faster it rolls. Light speed becomes a natural wall — no
   artificial speed cap needed; the engine just stops biting near `c`. This is
   **direction-blind**: braking is also an engine burn, so slowing down near `c`
   is just as feeble as speeding up. ⇒ you must begin arrival deceleration
   absurdly early (ties to the planner's leg-3 braking) — the brakes only start
   biting once you've bled off enough speed for the penalty to relax.
2. **The faster you go, the slower your crew's clock runs → supplies last
   longer.** A 50-year cruise (outside time) might cost only ~24 years of food
   and air. (This layer shows it as *slower supply burn*, not a separate calendar
   clock — real clock dilation is a deferred "time" element.)

→ **The trade:** getting fast is hard, but once you *are* fast your crew survives
far longer. The player picks a cruise speed around that tension.

**Time-rate is about current speed, not a debt.** Slow down and the burn rate
returns to normal — but the gap already built up while fast is permanent (the
twin-paradox outcome: the traveller comes back younger, for good; decelerating
never "catches up").

**The twist (radiation).** Radiation comes from *outside*, so it does **not**
slow with the crew clock — a fast crew ages less but soaks the same dose. So the
real danger on a relativistic run is **radiation, not starvation.**

---

## 1. Executive summary

| Question | Answer |
|----------|--------|
| Core mechanic | Effective thrust = nominal / γ³ (longitudinal relativistic mass). Light becomes an automatic asymptotic wall — no artificial speed cap. |
| Reward side | Proper-time resource burn = base / γ. Near-c cruise burns life support slowly. Opposite sign to the thrust penalty → a genuine trade. |
| Reference frame | Solar System **barycenter** inertial frame, fixed at departure. β measured against it. |
| Principia compatible? | **Yes** — we modulate the *input force* and *consumption rate*, never the integrator. Unlike warp, this does not bend spacetime. Principia even supplies barycentric velocity for free. |
| Display | Show both nominal and effective thrust, plus γ / β / resource-rate multiplier. The split readout *is* the mechanic's identity. |
| Visuals | **Out of scope** — the starbow shader layer is not our lane (§2.5). We ship Tier 0 (mechanic) only. |
| Implementation owner | Schultz (C# corrective-force hook + Kerbalism rate hook; no shader). This note is the brief. |

---

## 2. Findings

### 2.1 Core mechanic — thrust / γ³

For a force applied along the direction of motion, special relativity gives

```
a = F / (γ³ · m)        γ = 1 / √(1 − β²),   β = v/c
```

so the thrust that actually accelerates the vessel is **F_eff = F_nominal / γ³**.
This is the "longitudinal mass" γ³m. Applying it makes `c` an automatic
asymptotic wall: as β → 1, γ³ explodes and acceleration → 0 no matter the
nominal thrust. No artificial maximum-speed cap is needed.

Equivalence note for the integrator: `a = F/(γ³m)` is identical whether
modelled as "weak force on normal mass" or "normal force on γ³-heavy mass".
Feeding a Newtonian integrator the *reduced* force reproduces the longitudinal
relativistic-mass effect exactly.

| β | γ³ | effective thrust |
|---|----|------------------|
| 0.1 | 1.015 | 98.5% |
| 0.5 | 1.54 | 65% |
| 0.9 | 12.1 | 8% |
| 0.99 | 356 | 0.3% |

The curve is gentle below ~0.5c and steepens hard near `c` — the desired
"pushing the light barrier" feel. Keep pure 1/γ³ as the default; expose a
tuner if earlier onset is wanted for game feel.

### 2.2 Reward mechanic — resource burn / γ

Proper time runs as `dτ = dt / γ`. Scaling proper-time-linked consumption by
**1/γ** is physically exact and touches no clock or time-warp (keeps the time
element deferred). It is the opposite sign to the thrust penalty, which is what
makes the mechanic a real trade rather than a flat tax.

| β | γ | effective thrust (×1/γ³) | resource burn (×1/γ) |
|---|---|--------------------------|----------------------|
| 0.5 | 1.15 | 65% | 87% |
| 0.9 | 2.29 | 8% | 44% |
| 0.99 | 7.09 | 0.3% | 14% |

→ acceleration gets crushed, but a vessel that *is* already fast keeps its crew
alive far longer. This gives the player a strategic reason to deliberately aim
for a 0.9c cruise. Kerbalism's time-based consumption model is the natural hook.

**Only proper-time-linked consumption scales** — life support, crew food/oxygen,
sample degradation. **Engine propellant is excluded**: it burns in coordinate
time to produce the force. Scaling it too would double-reward ("going slow on
fuel *and* going fast").

### 2.3 Reference frame — Solar System barycenter

KSP velocity is reference-body-relative (orbit/surface), which is ambiguous for
interstellar flight. Use the **Solar System barycenter inertial frame, fixed at
departure**, for the whole journey. Inside any planetary system β is negligible,
so the mechanic effectively only switches on in interstellar cruise.

Interstellar nuance: other stars have peculiar velocities relative to the Sol
barycenter (α Cen ≈ 22 km/s ≈ 7×10⁻⁵ c) — negligible, so "at rest at the
destination" still reads β ≈ 0. A single fixed inertial frame for the whole trip
is the most consistent choice.

This dovetails with Principia, which already integrates in a barycentric
inertial frame and can hand us the barycentric velocity directly. Under the
stock profile we must compute barycentric velocity ourselves (stock gives only
SOI-relative velocity).

### 2.4 Principia / SigmaBinary compatibility

The earlier "Principia-incompatible" verdict was about **warp/FTL**, not this.
This mechanic is the opposite case:

- Principia integrates Newtonian n-body gravity and takes non-gravitational
  forces (engines) from the game. We reduce the engine force *before it is
  applied* (× 1/γ³). To Principia this just looks like a weaker burn — the
  integrator is untouched.
- Resource scaling is a Kerbalism consumption-rate change — also outside the
  integrator.
- There is a small philosophical inconsistency (Principia treats momentum as
  Newtonian), but every SR effect here is a **force / rate modulation layer**,
  so it does not fight the integrator. No spacetime is bent.

Net: this layer rides on **both** profiles (Principia n-body *and* SigmaBinary).
The force-hook question is now **resolved** (§4): Principia reads the accumulated
`part.force` census at stage-7 `FashionablyLate`, so writing that channel before
stage 7 suffices — no fork. The integrator is never touched.

### 2.5 Optional visual layer — 3 tiers (OUT OF SCOPE — not our lane)

> **Scope (2026-06-29):** the visual/shader layer (Tier 1–2 starbow) is **out of
> scope for this team, Schultz included** — relativistic post-process shaders are
> not our lane (cf. the Scatterer/EVE handoff: visual-mod shader work belongs to
> the visual-mod authors). **Our deliverable is Tier 0 only** (the mechanic +
> dashboard). The tiers below are retained as a reference/offer for whoever owns
> visuals, not as our work item.

Singularity proves a relativistic screen-space post-process is viable in KSP
(it already does black-hole lensing this way). The relativistic look decomposes
into three physically exact components:

| Component | Transform | On-screen |
|-----------|-----------|-----------|
| Aberration | cos θ′ = (cos θ − β)/(1 − β cos θ) | stars bunch toward the travel direction (forward headlight) |
| Doppler | D = 1/[γ(1 − β cos θ)] | forward blueshift, aft redshift (per-angle color) |
| Beaming | intensity ∝ D⁴ (bolometric; specific I_ν ∝ D³) | forward brightens, aft dims |

Together these are the "starbow". Every pixel needs only its line-of-sight angle
θ and β, so it is a single shader pass.

**Decouple visuals from the mechanic** so the shader can lag or be optional
without affecting gameplay:

- **Tier 0 — core, no visuals.** Thrust/γ³ + resource/γ + dashboard.
  Gameplay-complete on its own.
- **Tier 1 — cheap visual.** Doppler color grade + beaming brightness only,
  no geometry warp. Best value-for-effort; sells "I'm moving fast" past ~0.5c.
- **Tier 2 — full starbow.** Adds the aberration geometry warp. Singularity-class
  difficulty, but a proven path.

This layer is screen-space post-process — the same family as Scatterer — so it
sits adjacent to the existing visual pipeline.

### 2.6 Implementation guards / edge cases (must-handle for hand-off)

Three guards the C# must implement. All three are cheap and fail-safe.

**(i) Activation gate — don't compute when β is insignificant.**
The mechanic is negligible below ~0.1c (98.5 % thrust, γ−1 ~ 0.5 % at 0.1c), so
gate the whole thing on a `β_min` threshold (~0.01–0.05c); below it everything is
identity (no force correction, no resource scaling, dashboard shows "off"). The
gate is free: computing β is one `vessel.obt_velocity.magnitude` + one compare,
and in-system orbital speeds (~km/s ≈ 10⁻⁵ c) are always below threshold — so the
gate makes the layer "interstellar-cruise-only" for free. Two sub-gates:
- **Force correction** runs only when `β > β_min` AND an engine is producing
  thrust (coasting ⇒ no engine force to correct ⇒ natural no-op).
- **Resource scaling** runs whenever `β > β_min` (it must apply during high-β
  coast too — life support still burns slow while gliding fast).

**(ii) Warp-drive exemption — warp speed is NOT β.**
Warp is a bubble/metric translation, not real motion through space: the vessel's
proper velocity is ~0, so there is no dilation and no relativistic mass. If the
relativity layer ran during warp it would read apparent β > 1 (FTL) → NaN, and
would wrongly crush warp "thrust" and slow resource burn. So the layer reads a
shared **"under warp/jump" flag** and treats those vessels as identity. The warp
plugin and this layer are both Schultz's lane ⇒ one shared flag. (Also covers the
planner's computed-jump, though a jump is instantaneous.) **Rule: β counts only
physical speed-through-space; warp/jump motion is excluded.**

**(iii) Superluminal glitch (kraken) — fail safe.**
KSP physics bugs can fling parts at absurd / superluminal velocity; β ≥ 1 makes
γ = 1/√(1−β²) go NaN. Guard it:
- The force correction is **inherently bounded** — it is `−(1 − 1/γ³)·F_engine`,
  so as γ → ∞ it tends to `−F_engine` (full thrust cancellation), never an
  infinite force. So the relativity hook **cannot amplify a kraken.** Good.
- Still **NaN-guard the γ computation** (used by resource scaling + dashboard):
  `if (!IsFinite(β) || β ≥ β_sane) → identity` — skip correction and scaling for
  that vessel/frame. `β_sane` sits just above any legitimate drive (e.g. 0.995c);
  anything past it is treated as a glitch. **Do not try to "fix" the glitch** —
  the kraken is a collision/joint bug, not this layer's job; hand it back to
  KSP/Principia. Log a one-liner ("implausible β, relativity disabled").

---

## 3. Implications for NearStars

- This is a **gameplay layer for the interstellar endgame**, not a physics
  integrator. It is consistent with the gate-0 "gameplay first" decision and,
  unlike warp, is Principia-safe.
- **Recommended build order**: Tier 0 mechanic only (thrust + resource +
  dashboard) — shippable and self-contained. Visuals (Tier 1–2) are out of scope
  for this team (§2.5).
- **Hand-off**: this note is the brief for Schultz
  (`project_nearstars_mod_plugins_schultz`). Two plugin pieces: (a) a per-frame
  corrective force into the part-force channel so the *net* integrated force is
  ×1/γ³ (NOT an engine-thrust patch — that would also cut fuel; keep propellant
  at its nominal coordinate-time rate), applied **before** Principia's stage-7
  `FashionablyLate` force census; (b) Kerbalism proper-time consumption scaling
  by 1/γ. Both pieces must implement the §2.6 guards (activation gate, warp
  exemption, kraken fail-safe). The shader (former piece c) is out of scope. No
  NearStars DB / cfg deltas are implied by this layer.

---

## 4. Resolved (2026-06-29)

- **Principia force hook — RESOLVED, no fork needed.** Source recon
  (`ksp_plugin_adapter.cs` `FashionablyLate`, stage 7) confirms Principia reads
  the part's *accumulated* `part.force`/`part.forces` census — not re-derived
  engine thrust — **after** normal FixedUpdate force deposits and **before** the
  stock FlightIntegrator clears them. So a mod that writes the part-force channel
  before stage 7 has its force integrated. Implement as the corrective force in
  §3 hand-off. Works identically on the stock profile (same census feeds the
  stock integrator).
- **Stock barycentric velocity — RESOLVED.** KSP's root body (Sun) is the fixed
  inertial origin, so "barycentric" = Sun-fixed inertial. In the activation
  regime (interstellar cruise, SOI = Sun) `vessel.obt_velocity.magnitude` *is*
  the barycentric speed — no extra work. General fallback (still inside a planet
  SOI, where β is negligible anyway): walk the orbit parent chain summing
  `Orbit.GetFrameVel()`. Principia profile supplies barycentric velocity directly.
- **Onset tuning — RESOLVED: pure 1/γ³.** Keep the physically exact curve
  (project ethos). The *felt* onset is governed not by the exponent but by the
  **achievable cruise β** (drive tier) — tune it in the tech tree, not via an
  exponent fudge. Expose an optional tuner for modpacks, default off.
- **Proper-time vs coordinate-time resources — RESOLVED.** Scale ×1/γ (onboard
  biological/chemical rates): life-support O₂/Food/Water, CO₂/Waste/WasteWater,
  greenhouse growth, sample/specimen decay, time-based part wear. Do **not**
  scale (coordinate-time / external / avoids double-reward): engine
  propellant+oxidizer, ElectricCharge (external solar capture), reaction-wheel /
  RCS authority, and **radiation dose**. The dose split is deliberate: dose is an
  external coordinate-time flux integral, so a fast crew ages less but soaks the
  same dose ⇒ **radiation, not starvation, is the binding constraint on a
  relativistic run** (an emergent third axis, free from the two resource rules;
  optional ISM head-wind enhancement deferred to Kerbalism's ambient model).
- **Arrival frame — RESOLVED: keep the departure Sol-barycentric frame.** A
  single fixed inertial frame for the whole trip. Peculiar velocities (αCen
  7×10⁻⁵ c … Barnard 5×10⁻⁴ c) make "at rest at the destination" read β ≈ 0
  either way (γ−1 ~ 10⁻⁷⁻⁸) ⇒ rebasing has zero mechanical effect, only added
  complexity. (Arrival *relative velocity* for navigation/braking is the
  planner's concern, separate from this mechanic's β.)

**Out of scope (dropped):** shader-pass ordering with Scatterer/Singularity —
the whole visual layer is not our lane (§2.5).
