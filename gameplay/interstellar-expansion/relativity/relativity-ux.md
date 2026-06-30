---
title: Relativity layer — dashboard UX / UI spec
status: draft
created: 2026-06-30
---

# Relativity layer — dashboard UX / UI

**What this is.** The display spec for the sub-light relativity mechanic
([relativity-mod.md](relativity-mod.md)). The mechanic's identity *is* its readout
("the player sees nominal vs effective thrust diverge as β climbs", §1), so the
dashboard is a first-class design surface, not chrome. This note is the brief for
extending the draft [`RelativityDashboard.cs`](../../../plugins/NearStarsRelativity/RelativityDashboard.cs)
stub. Scope: the in-flight HUD only — no shader/visual layer (§2.5 of the spec, out
of our lane).

**Design tension it resolves.** relativity-mod §0 says the *felt* mechanic needs no
math; §1 says the split readout is the identity. The answer is a **two-mode
dashboard**: a math-free Simple mode and a full Expert mode.

---

## 1. The readout set

| Row | Shows | Source | Mode |
|-----|-------|--------|------|
| **Speed** | `β` as a fraction of `c`, with a light-wall gauge | `RelativityState.Beta` | both |
| **Thrust** | effective / nominal kN and % (`1/γ³`) | `ThrustFactor(γ)` | both |
| **Brake authority** | retrograde effective thrust % + a "⚠ decel now" cue | `1/γ³` (direction-blind) + planner | both |
| **Mission clock** | coordinate (UT) elapsed | game UT | both |
| **Crew clock** | proper time elapsed + Δ vs mission | per-vessel `∫dt/γ` accumulator | both |
| **γ** | the Lorentz factor | `RelativityState.Gamma` | Expert |
| **Life support** | consumption rate `×1/γ` | `ResourceFactor(γ)` | Expert |
| **Radiation dose** | `×1.00 (not dilated)` — the contrast row | constant 1.0 | Expert |

The **radiation contrast row** is deliberate: placing `dose ×1.00` directly beside
`life support ×0.39` teaches the spec's §4 conclusion — a fast crew ages less but
soaks the same dose, so **radiation, not starvation, is the binding constraint**.
Absolute dose stays in Kerbalism's own UI; we only show the multiplier contrast.

---

## 2. The light-wall speed gauge (§ decision ③)

A **linear bar from 0 to 1 c with a hard wall marker at 1.0**, plus the numeric
`0.923 c`. Above ~0.9c the last segment fills with a **non-linear tail** so the
final approach to `c` visibly never completes — the "asymptote you can't fill"
reads at a glance without needing rapidity. (Rapidity scaling was considered and
rejected as less intuitive.)

---

## 3. The two clocks (§ decision ④)

- **Crew (proper) clock** integrates `τ = ∫ dt/γ` **from vessel launch**, so it is a
  true crew-age odometer, displayed next to the coordinate (UT) mission clock with
  their difference.
- The gap is **permanent** — slowing down never catches it back up (the twin-paradox
  outcome). The accumulator never resets.
- Stored **per vessel** in the save. Display tracks the active vessel.
- **Display-only / bookkeeping.** This integrates and shows proper time; it does
  **not** manipulate the game's UT or time-warp. The deferred "time element"
  (relativity-mod scope) is *clock manipulation*; a passive odometer is compatible
  and safe to ship now.
- During warp, `γ = 1`, so the accumulator advances **1:1** with UT (no new gap); it
  keeps running in the background but is hidden from the warp-mode panel (§5).

---

## 4. Brake-authority cue (§ decision ⑤)

The `1/γ³` penalty is **direction-blind** — braking near `c` is as feeble as
accelerating, so arrival deceleration must begin absurdly early (relativity-mod §0,
ties to the planner's leg-3 braking).

- **Brake authority %** = retrograde effective/nominal thrust = `1/γ³` (same factor).
- **`⚠ decel now`** fires when deceleration must begin to make the arrival. Ideal
  source: the lead-intercept **planner** (leg-3 braking). MVP fallback without the
  planner: a heuristic on remaining distance vs current decel capability.

This single cue prevents the "why can't I stop?" soft-lock that the mechanic would
otherwise cause.

---

## 5. States & layout

Visibility follows the spec's §2.6 guards. The dashboard **auto-appears** when the
layer activates (`β > β_min`) and is otherwise hidden; an ApplicationLauncher toggle
can force-show it (for planning) or pin/hide. The window is draggable.

The stub currently hides the window whenever `st.Active` is false — which lumps
"sub-relativistic" together with "under warp". The extension must **split** these:

| Condition | Panel |
|-----------|-------|
| `β > β_min`, not warping/glitched | **full dashboard** (Simple or Expert) |
| **under warp/jump** (WarpFlag up) | **collapsed WARP panel** — speed in `c`-multiples only |
| `β ≤ β_min` (sub-relativistic) | hidden (or `off (sub-relativistic)` if pinned) |
| implausible β (kraken, §2.6 iii) | `disabled — implausible β` |

### Active (sub-light cruise) — Simple
```
┌─ RELATIVITY ───────────── ● ACTIVE ─┐
│ Speed   0.923 c  ▓▓▓▓▓▓▓▓░│1c         │
│ Thrust  8.9 / 154 kN  ( 5.8% )       │
│ Brake authority  5.8%   ⚠ decel now  │
│ Mission   12.4 yr                    │
│ Crew       4.8 yr   (−7.6)           │
└───────────────────────────────────────┘
```
**Expert** adds: `γ = 2.59`, `life support ×0.39`, `dose ×1.00 (not dilated)`.

### Warp detected (WarpFlag up) — collapsed
```
┌─ WARP ───────────── ◆ ─┐
│ Speed   23.4 c        │
└───────────────────────┘
```
All relativity-mechanic rows vanish (γ/thrust/supplies/dose/brake are identity or
NaN under warp). Only the warp speed in `c`-multiples remains. **The speed here is
the warp `β_s` read from the warp plugin (`WarpCruise`), not the relativity layer's
physical β** — the bridge between the two plugins (`WarpFlagBridge`) already exists.

---

## 6. Implementation brief — `RelativityDashboard.cs` extension

The stub computes `st = RelativityState.Evaluate(v, WarpFlag.IsWarpingOrJumping(v))`
and draws β/γ/thrust%/supply% when `st.Active`. Extend it:

1. **Route on warp first.** If `WarpFlag.IsWarpingOrJumping(v)`, draw the collapsed
   WARP panel using the warp speed from the warp plugin — **VERIFY** the read path
   (e.g. `WarpCruise.State.WarpBeta` of the active vessel's `WarpDriveModule`, via the
   same channel `WarpFlagBridge` uses). Do **not** read `st` for speed here (it's
   identity under warp by design).
2. **Two modes.** A Simple/Expert toggle (button in the window header or the launcher
   menu). Simple = Speed, Thrust, Brake, two clocks. Expert adds γ, life-support
   `×1/γ`, dose `×1.00`.
3. **Light-wall gauge.** Replace the plain `β` label with the 0→1 bar + wall marker +
   non-linear tail (§2).
4. **Two-clock accumulator.** A per-vessel `τ += dt/γ` integrator (advance 1:1 when
   γ≈1, including warp). Persist in the vessel's save node — **VERIFY** the
   `ProtoVessel`/`VesselModule` persistence hook. Display UT, crew, and Δ.
5. **Brake row.** Show `1/γ³` as brake authority %; wire `⚠ decel now` to the planner
   when present, heuristic otherwise (§4).
6. **Kraken/inactive text.** When pinned, show `off (sub-relativistic)` or
   `disabled — implausible β` instead of vanishing, so the player knows the layer is
   alive but idle.

No NearStars DB / cfg deltas. This is display + a proper-time accumulator on top of
the existing force/resource hooks.

## Related

- [relativity-mod.md](relativity-mod.md) — the mechanic this displays (§1 readout identity, §2.6 guards, §4 radiation-vs-starvation)
- [`plugins/NearStarsRelativity/RelativityDashboard.cs`](../../../plugins/NearStarsRelativity/RelativityDashboard.cs) — the stub this brief extends
- [warp/warp-patch-draft.md](../warp/warp-patch-draft.md) — the warp layer whose `β_s` and `WarpFlag` this reads under warp
- [planner-spec.md](../planner-spec.md) — the lead-intercept planner that feeds the `⚠ decel now` cue
