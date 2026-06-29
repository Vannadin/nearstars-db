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

## 1. Executive summary

| Question | Answer |
|----------|--------|
| Core mechanic | Effective thrust = nominal / γ³ (longitudinal relativistic mass). Light becomes an automatic asymptotic wall — no artificial speed cap. |
| Reward side | Proper-time resource burn = base / γ. Near-c cruise burns life support slowly. Opposite sign to the thrust penalty → a genuine trade. |
| Reference frame | Solar System **barycenter** inertial frame, fixed at departure. β measured against it. |
| Principia compatible? | **Yes** — we modulate the *input force* and *consumption rate*, never the integrator. Unlike warp, this does not bend spacetime. Principia even supplies barycentric velocity for free. |
| Display | Show both nominal and effective thrust, plus γ / β / resource-rate multiplier. The split readout *is* the mechanic's identity. |
| Visuals | Optional, decoupled, 3 tiers (color-only → full starbow). Tier 0 ships with zero visuals. |
| Implementation owner | Schultz (C# force hook + Kerbalism rate hook + post-process shader). This note is the brief. |

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
The one thing to confirm with Schultz is whether Principia exposes a clean hook
to modify the per-frame intrinsic force before integration.

### 2.5 Optional visual layer — 3 tiers

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

---

## 3. Implications for NearStars

- This is a **gameplay layer for the interstellar endgame**, not a physics
  integrator. It is consistent with the gate-0 "gameplay first" decision and,
  unlike warp, is Principia-safe.
- **Recommended build order**: Tier 0 mechanic first (thrust + resource +
  dashboard) → it is shippable and self-contained → visuals later, Tier 1 before
  Tier 2.
- **Hand-off**: this note is the brief for Schultz
  (`project_nearstars_mod_plugins_schultz`). Three plugin pieces: (a) per-frame
  intrinsic-force scaling by 1/γ³, (b) Kerbalism proper-time consumption scaling
  by 1/γ, (c) post-process shader (Tiers 1–2). No NearStars DB / cfg deltas are
  implied by this layer.

---

## 4. Open questions

- Does Principia expose a clean hook to modify the per-frame intrinsic force
  before integration? (Confirm before hand-off.)
- Stock profile: cheapest correct way to compute barycentric velocity each
  frame without Principia.
- Onset tuning: keep pure 1/γ³, or expose a β-scale / exponent tuner for earlier
  felt onset? Default = pure, tuner optional.
- Exact list of resources treated as proper-time-linked (life support / crew
  consumables / science sample decay) vs coordinate-time (propellant, reaction
  wheels, etc.).
- On arrival at another star, do we keep the departure Sol-barycenter frame
  (recommended) or rebase to the destination barycenter? Peculiar velocities are
  negligible either way.
- Does the visual post-process compose cleanly with Scatterer / Singularity if
  both are installed (shader pass ordering)?
