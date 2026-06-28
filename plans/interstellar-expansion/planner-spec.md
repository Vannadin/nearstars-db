---
title: Interstellar navigation planner — spec + lead-intercept prototype
status: exploratory
created: 2026-06-28
---

# Interstellar navigation planner — spec

**Stage: exploratory.** Specifies the interstellar lead-intercept planner and
records the math prototype. Engine-agnostic: the math here is portable and is the
half this side owns; the in-game C# (map-view hooks, UI, warp engage) is Schultz's
([[project-nearstars-mod-plugins-schultz]]). Context: [`README`](README.md),
[`warp-and-navigation-brainstorm.md`](warp-and-navigation-brainstorm.md).

**Why it's needed.** Under Principia the destination star *moves* (real space
velocity), so you must aim where it will be on arrival, not where it is now —
a lead-intercept. Principia's own flight planner can't do the warp leg (detached,
non-gravitational, flight-plan dropped). No Unity Editor required — a planner is a
code-only C# plugin (IMGUI/stock UI + map-view lines), precedent: Transfer Window
Planner / Astrogator / MechJeb.

## 1. Inputs

- **Origin** — ship position `r0` (Sol-barycentric ICRF) + velocity `v0`.
- **Destination star** — ICRF position `P0` + velocity `v_star` from `db/systems`.
  Future position by **linear extrapolation** `P(t) = P0 + v_star·t` (interstellar
  gravity ≈ 0 ⇒ ~straight-line; no Principia API needed). Binary destination: add
  the known orbital term from the DB elements.
- **Warp model** — speed `v_w` (constant for MVP; FTL allowed). Later: gravity-gated
  / tech-tiered ⇒ `v_w(distance)`.
- **Velocity-frame mode** — (a) barycentric-preserve / (b) destination-rest / (c) mid.

## 2. Algorithm — lead-intercept

Relative start `R0 = P0 − r0`. For **constant `v_w`** it's a closed-form quadratic
(ship covers `v_w·T` while the star drifts):

```
(v_w² − |v_star|²)·T² − 2(R0·v_star)·T − |R0|² = 0     →  positive root T
heading   = normalize(P0 + v_star·T − r0)
arrival   = P0 + v_star·T
arrivalRelV = (mode a: v0  |  mode b: v_star) − v_star   →  |·| = Δv-to-match
```

Variable `v_w(distance)` or a binary destination ⇒ fixed-point iterate (guess T →
distance/position → v_w → T → converge). Both are cheap and well-conditioned for
`v_w > v_star` (always true for warp).

## 3. Outputs

`heading` (unit), transit time `T`, `arrival` point, `arrivalRelV` (+ magnitude =
Δv to stop/match), and warnings (e.g. high arrival speed).

## 4. Prototype results (real DB data, ship at barycenter, v0 = 0)

`no-lead miss` = how far you'd miss if you aimed at the star's *current* spot.

| Target | warp | transit | no-lead miss | arrival rel v |
|--------|-----:|--------:|-------------:|--------------:|
| Alpha Cen A (4.40 ly, 28 km/s) | 1c | 4.40 yr | **26 AU** | 28 km/s |
| | 10c | 161 d | 2.6 AU | 28 km/s |
| | 1000c | 1.6 d | ~0 | 28 km/s |
| Barnard (5.99 ly, 142 km/s) | 1c | 5.99 yr | **180 AU** | 142 km/s |
| | 10c | 219 d | 18 AU | 142 km/s |
| | 1000c | 2.2 d | ~0 | 142 km/s |

**Findings.**
- **Lead is real and scales inversely with warp speed.** At 1c you'd miss by
  26 AU (αCen) / 180 AU (Barnard) — i.e. miss the whole inner system; even at 10c
  it's AU-scale. Negligible only above ~1000c. ⇒ the lead-intercept planner is
  necessary for any moderate warp, not a rounding error.
- **Arrival relative velocity is warp-speed-independent** — it equals the star's
  barycentric speed (28 / 142 km/s with v0 = 0). So the **velocity-frame decision
  has large consequences**: under (a) you arrive screaming past Barnard at
  142 km/s (a real arrival challenge / huge stop-Δv); under (b) the warp absorbs
  it and you arrive at rest. Barnard's proper motion makes this vivid.
- Constant-warp lead-intercept is a trivial closed-form quadratic — no convergence
  risk.

Prototype: `scratchpad/lead_intercept.py` (textbook intercept kinematics).

## 5. In-game UI surface (what the plugin shows)

- Map view: select a target star → show its **predicted arrival point** (the lead
  point, visibly offset from the star's current marker for slow warps), a heading
  line, transit time, and arrival relative velocity / Δv-to-stop.
- Engage warp toward the heading; (later) re-solve continuously as you steer.

## 6. Math ↔ C# boundary

- **Math (this spec + prototype — portable, done):** the intercept solver, star
  extrapolation, arrival-velocity computation. Schultz ports this verbatim.
- **C# (Schultz):** map-view hooks + line/marker rendering, feeding body states
  from Kopernicus/DB, warp engage, the cruise mechanic, and the UI.

## 7. Open decisions

- Warp speed model — constant (quadratic) vs gravity-gated/tiered (iterative).
- `v_w` value / tech tiers (tied to the expansion tech tree).
- Velocity-frame default (a / b / c) — §4 shows the stakes.
- Binary-destination orbital term (use DB elements vs barycenter-only approximation).
- `v0` source (the ship's launch velocity at engage).

## Related

- [warp-and-navigation-brainstorm](warp-and-navigation-brainstorm.md) — §6 frame decision, §7 planner
- [feasibility](feasibility.md) — gate 0
