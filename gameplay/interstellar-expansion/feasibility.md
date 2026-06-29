---
title: Interstellar travel feasibility — gate 0
status: active
created: 2026-06-28
---

# Interstellar travel feasibility — gate 0

**NearStars connection.** Reaching the NearStars systems is meant to be a
**post-RP-1 end-game expansion** — content that exists *after* the player has
completed the real-world RP-1 tech tree. Before designing that expansion's tech
tree, propulsion, and per-system science values, one question gates everything:
**is interstellar travel actually buildable and playable** in the
RSS + Principia + RP-1 stack at NearStars' real (uncompressed) distances? This
note records that gate-0 analysis and the architecture decision it produced.

**Scope.** In: the Δv / time / propulsion trade space, the relativistic limits,
the warp-mod survey, and the resulting build decision. Out: the actual tech-tree
design, propulsion-mod RO configs, and per-system science values (downstream,
gated on this). No cfg is shipped here — emit stays deferred to project end, and
the travel plugin itself is C# (Schultz, per [[project-nearstars-mod-plugins-schultz]]).

**Interactive companion.** Relativistic Δv map (live slider):
https://claude.ai/code/artifact/43636b83-6e8d-48e3-ae63-025cc89c6c57

---

## 1. Executive summary

| Question | Finding |
|----------|---------|
| Can reaction drives reach the stars fast? | **No.** Chem/NTR/nuclear-ion/adv-electric are impossible at every interstellar setting. Only torch (Isp 10⁶ s) and antimatter (10⁷ s) close — and only over **100–500 yr**. |
| Is there a hard speed limit? | Yes — **the light-speed floor.** Min Earth-frame travel time = distance in ly (Proxima 4.2 yr … TRAPPIST-1 40.7 yr). Faster = FTL = warp-only. |
| Does relativity matter? | Only when pushing toward the floor (>0.3c). There the relativistic rocket Δv (rapidity) explodes — even a photon rocket struggles, antimatter becomes impossible. Below ~0.1c it's negligible. |
| Do the warp mods work with Principia? | **No — both KSPIE and Blueshift are Principia-incompatible** (they reposition vessels without thrust; Principia undoes it). Any warp here is a custom build. |
| Build decision | **Build the interstellar gameplay on the premise of Principia-incompatibility** → two install profiles. May let us skip the custom Principia plugin entirely. |

---

## 2. The Δv trade space (real distances)

Distances are real, from `db/systems/*.json` (uncompressed; pc → ly ×3.261564).
Continuous-thrust **brachistochrone** (accelerate to midpoint, flip, decelerate).
Textbook relations only (rocket equation; relativistic-rocket / rapidity):

- Average Earth-frame speed `β = d / (c·T)` — **requires β < 1**.
- Rapidity `φ = 2·atanh(β)`; Δv `= 2φ·c` (stop) or `φ·c` (flyby).
- Peak speed `β_peak = tanh φ`, `γ = 1/√(1−β_peak²)`.
- Crew (proper) time `τ = T·φ/sinh φ` — diverges from Earth time T at high β.
- Mass ratio `MR = exp(Δv / v_e)`, `v_e = Isp·g₀`.

Propulsion exhaust velocities (engineering reference): Fusion (Daedalus) 10⁵ s
= 0.0033c · Torch 10⁶ s = 0.033c · Antimatter 10⁷ s = 0.33c · Photon rocket = c.

| System | dist | light floor | feasible reaction-drive route |
|--------|------|-------------|-------------------------------|
| Proxima Cen | 4.2 ly | 4.2 yr | Torch ~200 yr · Antimatter ~50–100 yr |
| Alpha Cen | 4.4 ly | 4.4 yr | as Proxima |
| Barnard | 6.0 ly | 6.0 yr | Torch ~300 yr · Antimatter ~100 yr |
| Luhman 16 | 6.5 ly | 6.5 yr | Antimatter ~100 yr |
| Tau Ceti | 11.9 ly | 11.9 yr | Antimatter ~150–200 yr |
| 40 Eridani | 16.3 ly | 16.3 yr | Antimatter ~200 yr |
| Fomalhaut | 25.1 ly | 25.1 yr | Antimatter ~200–300 yr |
| TRAPPIST-1 | 40.7 ly | 40.7 yr | Antimatter only, multi-century; <100 yr needs photon-class |

**Verdict.** Interstellar travel demands torch/antimatter-class propulsion
(Isp 10⁶–10⁷ s) — far beyond RP-1's chemical/NTR/early-nuclear. This confirms it
must be a far-future extension, and that **propulsion is the real bottleneck**.
"Go fast to far stars" with reaction drives is physically out: e.g. TRAPPIST-1 in
50 yr = 0.81c average → Δv ≈ 4.5c → antimatter MR ~10⁶ (impossible), photon ~94.

---

## 3. The light-speed floor & the two clocks

- **Floor.** Earth-frame travel time can never beat light: `T_min = d/c`. So
  TRAPPIST-1 (40.7 ly) is unreachable under ~41 yr by any reaction drive;
  **30 yr is flat impossible** (FTL). This is the hard wall a realist path hits.
- **Two clocks.** The crew's proper time is dilated below Earth time. TRAPPIST-1
  in 50 Earth-yr → crew experiences ~24 yr (γ≈5). A realist cruise plugin would
  have to book-keep this: the calendar jumps by Earth years; crew, life-support,
  and part aging advance by crew years. This is the one place relativity touches
  gameplay — and it is plugin bookkeeping, not a physics-engine change.
- **Relativity scope.** Negligible below ~0.1c (the comfortable antimatter
  missions); decisive only when pushing toward the floor. We do not simulate
  relativity in the engine (impossible in KSP — float32 near c, single UT clock,
  Principia desync); it lives as formulas in whatever computes the transit.

---

## 4. Warp-mod survey

Both candidate warp mods were compared (full cites below). Bottom line:

| | KSPIE — Alcubierre Drive | Blueshift (Angel-125) |
|---|---|---|
| Mechanic | Alcubierre bubble, 78 warp factors; moves via orbit state-vector rewrite + rail-warp | FTL cruise + jump-gate; moves via per-frame `SetPosition()` |
| Energy | ExoticMatter + MegaJoules, mass-scaled, reactor-driven | Graviolium → GravityWaves (mined, arcade-themed) |
| Gravity well | gravity caps max speed; no atmo warp | SOI speed curve; ×1000 interstellar boost; location classes |
| RP-1 tone | "hard-adjacent" reactor progression | explicit Star-Trek arcade (worst RP-1 fit) |
| Maintenance | dormant (Nov 2021), community fork exists | **active (v1.16, Mar 2026)** |
| License | custom non-OSI | **code GPL-3.0** (forkable), art ARR |
| Principia | incompatible (inferred, near-certain) | **incompatible — named in Principia FAQ** |

**Both are Principia-incompatible for the same root cause** — they reposition
vessels without thrust, which Principia undoes every tick. Reference choice:
**Blueshift** — GPL-3.0 (legally adaptable), actively maintained, and its
gravity-well-gated + location-aware speed model is the right gameplay shape
(sublight in wells, huge boost in flat interstellar space). Borrow **KSPIE's
mass-scaled reactor/ExoticMatter economy** for RP-1 tone. Reuse the *model*,
never the *propagation*.

---

## 5. Decision — build Principia-incompatible first (two profiles)

Because every warp option (and the realist torch-cruise) needs custom
Principia-aware engineering, we **build the interstellar gameplay on the premise
of Principia-incompatibility first.** This naturally splits NearStars into two
self-consistent install profiles:

| | Principia profile | Non-Principia profile (interstellar) |
|---|---|---|
| Orbits | true n-body, real multi-star dynamics | stock patched-conics + **SigmaBinary** |
| Interstellar travel | effectively none (warp incompatible) | **warp works** |

- **Key upside.** In the non-Principia profile, **SigmaBinary and warp are
  mutually compatible** (both non-Principia). So a Blueshift-derived warp can be
  used near-as-is, and the expensive "custom Principia-aware propagation" may be
  **skipped entirely** (or deferred indefinitely as a future "unify" item).
  Gates (b) Principia-integrates-the-cruise and (c) time-warp-under-thrust become
  moot in this profile.
- **Trade.** Interstellar players give up Principia's n-body — binaries revert to
  SigmaBinary/conics. Accepted as reasonable: hard-n-body realism and warp-
  interstellar fantasy are largely different audiences.
- **Role boundary.** Design / spec / cfg (parts, tech placement, science values,
  warp model) = this side; the warp/cruise C# (incl. any Blueshift fork) =
  Schultz, per [[project-nearstars-mod-plugins-schultz]].

---

## 6. Open questions / next

- **Gameplay loop design** (non-Principia profile): warp model details, drive
  parts, the interstellar mission arc, arrival experience.
- **Propulsion / drive choice**: Blueshift-fork warp vs a realist torch option —
  and whether to offer both (warp = primary; torch = hard-mode realist alt).
- **Tech-tree placement & balance**: where the interstellar branch attaches past
  the RP-1 tree (ties to the broader expansion plan).
- **Per-system science values**: set last, using `docs/reference/science-system.md`
  and the extended tree's node costs.
- **Distance compression** is now a *tuner*, not a blocker — optional, to shorten
  trips / lighten any future Principia integration. Decide only if needed.

---

## Sources

- Principia FAQ (warp/SigmaBinary incompatibility): https://github.com/mockingbirdnest/Principia/wiki/Installing,-reporting-bugs,-and-frequently-asked-questions
- KSPIE Alcubierre: https://github.com/sswelm/KSP-Interstellar-Extended/blob/master/FNPlugin/Propulsion/AlcubierreDrive.cs · https://github.com/sswelm/KSP-Interstellar-Extended/wiki/Warp-Drives
- Blueshift: https://github.com/Angel-125/Blueshift · https://raw.githubusercontent.com/Angel-125/Blueshift/master/Source/Blueshift/WarpTech/WBIWarpEngine.cs
- RP-1 supported configs: https://github.com/KSP-RO/RP-1/wiki/Which-mods-have-RP1-Configurations%3F
- Distances: `db/systems/*.json`. Δv math: standard rocket / relativistic-rocket equations (textbook).

## Related

- [rp1-integration](../rp1-integration/plan.md) — the RP-1 career-layer integration this expansion sits on top of
- [science-system](../../docs/reference/science-system.md) — per-body science values (feeds the expansion's payoff)
