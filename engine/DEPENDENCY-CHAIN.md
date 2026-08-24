<!-- 무엇을 결정해야 무엇을 계산할 수 있는지 — NearStars 물리값 의존 사슬 (엔진화 순서의 근거) -->
# Dependency chain: what must be decided before what can be computed

This is the ordering document. Every other engine decision — which recipe to write
first, what a function's signature must be, where the seams are — falls out of it.

Three kinds of node:

| kind | meaning |
|---|---|
| **measured** | comes from a paper via Phase 2. Never computed by us. |
| **owner** | a choice no measurement constrains. Phase 4 gates it. |
| **computed** | a recipe turns upstream nodes into it. This is what the engine owns. |

Status marks what we have today: **✓** recipe exists · **~** partial or assumed ·
**✗** missing (the value is currently asserted, not derived).

---

## Level 0 — the floor

Nothing computes these. If they are wrong, everything below is wrong.

| node | kind | notes |
|---|---|---|
| star: M, R, T_eff, L, age, spin period, v sin i | measured | Phase 2 |
| body: orbit a, e, i, Ω, ω | measured / owner | measured where detected; owner where we place a synthetic body |
| body: M **or** R | measured | usually only one of the two is measured |
| **bulk composition intent** | **owner** | rocky / icy / H–He / mixed. Nothing measures this for our bodies. |

> **First gate.** When only one of M/R is measured, the other comes from
> `mass-radius-relation` **✓**. Which one is the anchor and which is derived is a
> decision, and it must be recorded — otherwise the pair silently becomes circular.

---

## Level 1 — the dispatch key

| node | needs | kind | status |
|---|---|---|---|
| **body class** | M, R, ρ, composition intent | computed | **✗** |

Everything below branches on this. It decides *which* dynamo recipe, *which* thermal
model, *which* figure relation applies. We do not currently have it: `body_class` in
Phase 4 is `star / tidally_locked / free_rotator`, which is a rotation axis, and
`body_type` is free prose, unique per body.

Because the key is missing, each downstream recipe re-invents its own admission test
in prose, and nothing can check that the right recipe was applied to the right body.

---

## Level 2 — interior structure (the missing root)

| node | needs | kind | status |
|---|---|---|---|
| layer mass fractions | class, M, R | computed | **✗** |
| interior structure | layer fractions, M, R, T_surf | computed | **✗** |
| ↳ NMoI | interior | computed | **~** assumed 0.23 in `body-figure` |
| ↳ core radius + conductor phase | interior | computed | **~** assumed in `rocky-planet-dynamo` |
| ↳ strain-weighted k₂/Q | interior | computed | **~** hand-picked (Pandora's 0.0016 is fitted) |

Four downstream recipes currently each assume their own version of these. That is the
root cause of the seam drift found in review: no shared upstream node exists, so every
consumer invented one, and the inventions do not know about each other.

Note `T_surf` as an input — see **Cycle 1**.

---

## Level 3 — three branches off the interior

### 3a. Figure and spin

| node | needs | kind | status |
|---|---|---|---|
| tidal locking state | M_parent, a, e, age, k₂/Q | computed | **✓** |
| rotation period | locking state, or owner for free rotators | computed / owner | **✓** |
| J₂ | NMoI, rotation period, M, R | computed | **✓** |
| C₂₂ | J₂, locked | computed | **✓** |
| flattening | J₂ | computed | **✓** |
| obliquity | Cassini state (locked) / owner (free) | computed / owner | **✓** |
| spin-axis inclination i★ | v sin i, P, R | computed | **✓** |

### 3b. Magnetism

| node | needs | kind | status |
|---|---|---|---|
| B (giant / BD) | M, R, age | computed | **✓** |
| B (rocky) | core radius, conductor, rotation, age | computed | **~** needs Level 2 |
| stellar wind n, v | star age, activity | computed | **✓** |
| magnetopause R_mp | B, stellar wind | computed | **✓** |
| radiation belts | B, R_mp | computed | **✓** |

> The giant dynamo path does **not** need the interior — that is precisely why it works
> today while the rocky path is assumed. It is also why it is the cheapest pilot.

### 3c. Tidal energetics

| node | needs | kind | status |
|---|---|---|---|
| tidal power | e, a, M_parent, R, k₂/Q | computed | **✓** |
| tidal surface flux | tidal power, R | computed | **✓** |
| heat transport mode | flux | computed | **✓** |
| volcanism / ocean / plumes | mode | computed | **✓** |
| resurfacing rate | mode, flux | computed | **✓** |

---

## Level 4 — thermal and atmosphere

| node | needs | kind | status |
|---|---|---|---|
| T_eq (planet) | L, a, albedo | computed | **✓** |
| T_eq (moon, 4-term) | parent T + R + albedo, orbit, eclipse, tidal flux | computed | **✓** |
| atmosphere retention | XUV (star age), g, v_esc, B | computed | **✓** |
| atmosphere P + composition | retention window | **owner** | — |
| greenhouse ΔT | composition, P, S/S₀ | computed | **✓** |
| T_surf | T_eq + ΔT | computed | **✓** |
| internal heat / T_int | M, age | computed | **✓** |

> **Ordering rule.** A moon's 4-term budget consumes its parent's temperature, radius
> and albedo. **A parent must be fully resolved before any of its moons.** This is a
> hard topological constraint, not a preference.

---

## Level 5 — surface

| node | needs | kind | status |
|---|---|---|---|
| ice stability | T_surf, albedo, orbit | computed | **✓** |
| crater state | age, resurfacing rate, gravity | computed | **✓** |
| surface color + albedo | composition, ice, volcanism | computed | **~** |
| Hapke shader params | albedo, roughness | computed | **~** |
| atmosphere reflected color | composition, clouds, T | computed | **✓** |

---

## Level 6 — emit

| node | needs |
|---|---|
| Principia gravity model | J₂, C₂₂, reference radius |
| Kerbalism radiation | belts, surface dose |
| Kopernicus body | everything above |

---

## Cycles

These are real. They cannot be ordered away, only iterated or cut by decision.

**Cycle 1 — T_surf ↔ interior.**
The interior solver needs a surface boundary temperature; T_surf is produced four
levels below it. *Resolution:* first pass with T_eq as the boundary, then iterate.
Two passes is enough — the interior is insensitive to the surface at depth.

**Cycle 2 — albedo ↔ T_eq.**
Albedo sets T_eq; T_eq decides ice and cloud cover, which set albedo. *Resolution:*
seed with a class-default albedo, iterate twice, or cut it by making albedo an owner
decision and recording that the temperature followed it.

**Cycle 3 — tidal heating ↔ k₂/Q ↔ interior ↔ T_surf.**
The widest loop, and the one currently cut by hand-fitting k₂/Q to a desired answer.
*Resolution:* it closes once Level 2 exists. Until then, every k₂/Q we use is a free
parameter wearing a derivation's clothes, and should be labelled as such.

---

## What this implies for build order

1. **Class key (Level 1) before anything.** Without it no recipe can declare, or be
   checked against, its own domain.
2. **Interior (Level 2) before the rocky branch closes.** Four recipes stop assuming
   the moment it exists.
3. **The giant dynamo branch is independently reachable.** It needs only Level 0. That
   makes it the correct pilot: it exercises the payload contract, the class dispatch
   and the anchor-as-test pattern without waiting on Level 2.
4. **Parent before moon, star before planet.** Any per-system driver must walk the
   body tree in that order.
5. **Cycles are declared, not discovered.** Every recipe sitting on a cycle says so in
   its payload, so a value that came out of an un-converged first pass is never
   mistaken for a converged one.

---

## Related

- [`docs/reference/methodology-index.md`](../docs/reference/methodology-index.md) — the recipes named above
- [`phase4/SPEC.md`](../phase4/SPEC.md) — where owner decisions are gated
