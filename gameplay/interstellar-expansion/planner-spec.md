---
title: Interstellar navigation planner — spec + Δv lead-intercept prototype
status: active
created: 2026-06-28
updated: 2026-06-29
---

# Interstellar navigation planner — spec

**Stage: exploratory.** Specifies the interstellar **Δv-based lead-intercept**
planner and records the math prototype. Engine-agnostic: the math here is portable
and is the half this side owns; the in-game C# (map-view hooks, UI, jump/warp
engage) is Schultz's ([[project-nearstars-mod-plugins-schultz]]). Context:
[`README`](README.md), [`warp-and-navigation-brainstorm.md`](warp/warp-and-navigation-brainstorm.md).

## Why it's needed (and why it's *light*, not heavy)

The original worry was that Principia's own flight planner couldn't carry an
interstellar trip — integrating a centuries-long trajectory in real time. That
worry is correct in practice (real-time Principia prediction over such spans
**lags the game hard**), but the root reason for a custom planner is sharper:

- The travel leg is **outside Principia entirely** — non-gravitational
  repositioning Principia has no maneuver primitive for and actively undoes
  (warp doc §2). It is detached; the flight plan is dropped.
- The destination star **moves** — you must aim where it will be on arrival, a
  lead-intercept Principia's planner does not do.

We design for the **worst case: no custom Principia branch available.** Without a
fork, continuous cruise is impossible (no-fork ⇒ jump only, warp doc §3). So the
floor mechanic is a **computed jump**: solve (heading, transit time `T`,
arrival point) closed-form, then **advance the clock by `T` and re-seed the
vessel at the lead point** — no per-step real-time integration (no lag), no fork
(stock re-seed). Continuous cruise becomes an *upgrade if a fork ever lands*.

This inverts the worry: because interstellar gravity ≈ 0, **there is nothing to
integrate** — the planner is a closed-form quadratic, not a trajectory solve.
It depends on **no Principia read API** (being removed anyway) and runs offline.

No Unity Editor required — a planner is a code-only C# plugin (IMGUI/stock UI +
map-view lines), precedent: Transfer Window Planner / Astrogator / MechJeb.

## 1. Inputs

- **Origin** — ship position `r0` (Sol-barycentric ICRF) + velocity `v0` (read
  from the actual vessel state at engage; whatever it coasted out at).
- **Destination star** — ICRF position `P0` + velocity `v_star`, built from
  `db/systems` astrometry (RA/Dec, parallax, pmRA, pmDec, RV → 3-D vector).
  Future position by **linear extrapolation** `P(t) = P0 + v_star·t` (interstellar
  gravity ≈ 0 ⇒ ~straight-line). Binary destination: **add the DB orbital term**
  (required, not optional — see §4.5).
- **Δv budget** — the ship's drive capability. This is the *speed input*: a
  brachistochrone (accel to midpoint, flip, decel-to-rest) converts Δv → transit
  time. Newtonian `T = 4d/Δv`; the relativistic form (below) is used near `c`.

## 2. Algorithm — Δv → transit time → lead-intercept

The average speed of a stop-at-end brachistochrone is `v_avg = Δv/4` (Newtonian).
The relativistic form (rapidity, per feasibility §2) is a single clean line that
**covers both regimes and never exceeds light**:

```
v_avg = c · tanh(Δv / 4c)          // → Δv/4 at low Δv; → c as Δv → ∞ (light floor automatic)
```

Then the lead-intercept is a closed-form quadratic — the ship covers `v_avg·T`
while the star drifts by `v_star·T`:

```
R0 = P0 − r0
(v_avg² − |v_star|²)·T² − 2(R0·v_star)·T − |R0|² = 0     →  positive root T
target    = P0 + v_star·T            // the future star position to lock as the aim point
heading   = normalize(target − r0)
arrivalRelV = v0 − v_star            // frame-(a); |·| = the braking Δv at arrival
```

`v_avg < c` always ⇒ a positive root always exists and `T > d/c` (light floor)
holds with **no separate FTL guard**. A binary destination makes `v_star`
position-dependent ⇒ one fixed-point pass (guess T → orbital position → T);
cheap and well-conditioned.

## 3. Outputs

`transit time T`, the **future `target` point** (what the player locks the aim
on), `heading`, and `arrivalRelV` (magnitude = the braking Δv at the destination).
The arrival *frame* (do you keep `v0`, or does the drive null it to the star) is
**not the planner's call** — it's a warp/drive-mechanic decision (warp doc §6);
the planner just *reports* the consequence.

## 4. Prototype results (real DB astrometry, ship at barycenter, v0 = 0)

`lead offset` = how far the future target sits from the star's *current* spot —
i.e. how far you'd miss aiming at "now". Light floor `d/c` shown for reference.

| Target (dist, \|v_star\|) | Δv | v_avg | T | lead offset | arrive rel-v |
|---------------------------|---:|------:|--:|------------:|-------------:|
| Alpha Cen (4.39 ly, 28 km/s) | 1c | 24.5%c | 17.9 yr | 107 AU | 28 km/s |
| | 4c | 76.2%c | 5.8 yr | 34 AU | 28 km/s |
| | 12c | 99.5%c | 4.4 yr | 26 AU | 28 km/s |
| Barnard (5.96 ly, 142 km/s) | 1c | 24.5%c | 24.3 yr | 731 AU | 142 km/s |
| | 4c | 76.2%c | 7.8 yr | 235 AU | 142 km/s |
| TRAPPIST-1 (40.7 ly, 84 km/s) | 1c | 24.5%c | 165.9 yr | 2927 AU | 84 km/s |
| | 4c | 76.2%c | 53.4 yr | 942 AU | 84 km/s |
| | 12c | 99.5%c | 40.9 yr | 721 AU | 84 km/s |

**Findings.**
- **`v_avg = c·tanh(Δv/4)` retires the FTL guard.** Even at Δv = 12c the speed is
  99.5%c and `T > d/c` everywhere — the light floor falls out of the formula.
- **The lead is large at *every* realistic speed.** Even at near-light Δv = 12c,
  TRAPPIST-1's target is **721 AU** off its current marker; at 1c it's thousands.
  The system is ~AU-scale ⇒ **you cannot hit it without the planner.** Existence
  fully justified.
- **"TRAPPIST-1 in 30–50 yr" sits at Δv ≈ 4–5c** (`v_avg` ~0.76–0.81c) — a
  reaction-drive-impossible Δv, confirming a warp-equivalent drive fills that slot.
- **Arrival rel-v is the star's own speed** (frame-(a), v0 = 0): Fomalhaut 15 km/s
  vs Barnard 142 km/s. Proper motion survives as arrival difficulty.

Prototype: [`prototypes/lead_intercept_dv.py`](prototypes/lead_intercept_dv.py)
(Δv → T → future target, real DB vectors).

## 4.5 The trip is three legs (deeper analysis, 2026-06-29)

Warp/jump can only engage where stellar gravity is negligible (clean detach /
re-seed). That boundary `r_g` (where `GM/r² < ~1e-10 m/s²`) is **~0.12 ly for a
Sun-like star** (`r_g ≈ 0.12·√(M/M☉) ly`; TRAPPIST-1 ≈ 0.037 ly). So a real trip
is: **leg 1** sublight climb to `r_g` → **leg 2** the jump/warp lead-intercept →
**leg 3** sublight descent + braking burn at the far `r_g`.

- **Leg 2 dominates distance** — the sublight legs are 0.6 % (TRAPPIST) to 5.5 %
  (αCen) of the trip ⇒ modelling the intercept as a single Δv-brachistochrone is
  justified. But the boundaries set `v0` (entry) and the arrival braking.
- **`r_g` = the warp engage/disengage boundary** — it lines up with the
  Blueshift-style gravity-gated speed model (slow in wells, fast in the flat).
- **Braking is cheap, not a wall.** Killing even Barnard's 142 km/s with a torch
  drive (Isp 1e6 s) = **1.4 % propellant**, a ~4 h burn over 0.007 AU. So
  frame-(a) "arrive fast" is a short braking beat, not a Δv gate — which is why
  the frame choice is flavor, not a blocker (the warp doc owns that call).
  *Caveat — two different brakings.* This cheap one is the **non-relativistic**
  arrival case (the star's km/s peculiar velocity, γ≈1). Shedding a relativistic
  **cruise** speed (a realist torch run, or a fork'd continuous warp that carries
  real β) is the hard case, governed by the relativity layer's `1/γ³` brake
  authority and surfaced as the dashboard's `⚠ decel now` cue
  ([relativity-ux §4](relativity/relativity-ux.md)). It is **dormant in the
  computed-jump floor** (the jump is instantaneous — no cruise speed to shed) and
  matters only in a sublight / continuous-cruise profile.
- **Binary orbital term is required, not optional.** Over a 1c transit to Alpha
  Cen, component A swings **6.1 AU** along its barycentric orbit — larger than the
  inner system. Aiming at the barycenter lead alone still misses A by ~6 AU. αCen
  is our #1 target ⇒ the DB orbital term is mandatory for binary destinations.

Numbers reproducible via [`prototypes/planner_deep.py`](prototypes/planner_deep.py).

## 5. In-game UI surface (what the plugin shows)

- Map view: select a target star → enter/read **Δv** → show **transit time T**,
  the **future target marker** (visibly offset from the star's current marker),
  a heading line, and arrival rel-v / braking Δv.
- Lock the future target → engage (computed jump: clock-advance `T` + re-seed; or,
  with a fork, fly the cruise and re-solve continuously as you steer).

## 6. Math ↔ C# boundary

- **Math (this spec + prototypes — portable, done):** Δv→v_avg, star vector from
  astrometry, the intercept solver, arrival-velocity. Schultz ports verbatim.
- **C# (Schultz):** map-view hooks + marker/line rendering, body states from
  Kopernicus/DB, the jump (clock-advance + re-seed) or cruise mechanic, the UI.

## 7. Decisions

**Resolved by the analysis:**
- Speed model — **Δv-driven**, `v_avg = c·tanh(Δv/4)`; one formula, light-floor-safe.
- Binary orbital term — **required** (αCen swings 6 AU; §4.5).
- Re-solve — single-star constant-Δv is one-shot exact; **binary targets need the
  fixed-point pass** (orbital curvature).
- `v0` source — **read from vessel state** at engage.

**Remaining (mostly outside the planner):**
- Δv values / tech tiers — tied to the expansion tech tree (gameplay design).
- Velocity-frame default (keep v0 vs null to star) — **warp/drive-mechanic call**,
  warp doc §6; the planner only reports the resulting arrival rel-v.

## Related

- [warp-and-navigation-brainstorm](warp/warp-and-navigation-brainstorm.md) — §6 frame decision, §3 jump-vs-cruise
- [feasibility](feasibility.md) — gate 0 (Δv math, light floor, relativity)
- [relativity-ux](relativity/relativity-ux.md) — §4 consumes this planner's leg-3 braking as the dashboard `⚠ decel now` cue
