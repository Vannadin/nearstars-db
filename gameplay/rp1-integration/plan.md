---
title: RP-1 / RealSolarSystem compatibility integration
status: active
created: 2026-06-26
---

# RP-1 compatibility integration

**NearStars connection.** NearStars is built on Sol-Configs
(ballisticfox / RSS-Reborn lineage, `FOR[SolSystem]`). RP-1 (Realistic
Progression One) is a realistic-career mod on RealismOverhaul + Principia +
ROKerbalism that **officially requires classic `KSP-RO/RealSolarSystem`, not
Sol-Configs**. However, the Sol-Configs side (ballisticfox) is **planning its
own RP-1 compatibility** (awaited, upstream). So NearStars does **not** build a
classic-RSS branch; it **stays Sol-based and rides on Sol-Configs' upcoming
RP-1 bridge**, adding only the **base-independent RP-1 career-layer patches**
NearStars itself must own. This note captures those layers, grounded in the
upstream mod sources, so they are ready when Sol-Configs' RP-1 compat lands.

**Scope.** Target = **RP-1 on Sol V1.0 only** (owner decision 2026-06-26).
RP-1 on classic RealSolarSystem (today's standard install) is **explicitly out
of scope** — NearStars bodies are `SolSystem`-gated and will not appear on a
classic-RSS base, and we are choosing not to build a `:NEEDS[RealSolarSystem]`
body variant. In: the RP-1 career-layer patches NearStars owns (ResearchBodies,
ROKerbalism radiation, Principia body append, RealAntennas note) + their MM
tags/node names/reseat targets. **Out (collapsed):** any classic-RSS Kopernicus
variant or RSS-specific Principia coordinate variant. Out: shipping tested cfgs
now (emit deferred to project end); in-game validation (waits on Sol V1.0 RP-1
compat + owner's Windows install). C#/Harmony work is Schultz's per
[[project-nearstars-mod-plugins-schultz]].

**External references.**
- https://github.com/KSP-RO/RP-1 (career mod; MM token `RP-0`)
- https://github.com/KSP-RO/RealismOverhaul (tag `RealismOverhaul`)
- https://github.com/KSP-RO/ROKerbalism (profile `RealismOverhaul` → tag `ProfileRealismOverhaul`)
- https://github.com/mockingbirdnest/Principia
- https://github.com/JPLRepo/ResearchBodies
- https://github.com/KSP-RO/RealAntennas
- https://github.com/RSS-Reborn/Sol-Configs (our base; RP-1 compat upstream-planned)

---

## 1. Strategy (the pivot)

The key fact: **RP-1 and Sol-Configs are mutually exclusive bases, and an
RP-1 player's base is whatever Sol-Configs ships once it's RP-1-compatible —
NearStars never needs to target classic RSS itself.**

- **Bodies stay `FOR[SolSystem]`.** When Sol-Configs becomes RP-1-compatible,
  NearStars bodies load in the RP-1 game automatically (they attach to the
  same Sol base). No RSS tag, no coordinate fork, no dual-base gating.
- **NearStars owns only the base-independent career layers.** These gate on
  RP-1 / RO / ROKerbalism / Principia being present — **never on the
  base-system tag** — so they are robust to *however* Sol-Configs implements
  its RP-1 bridge, and can be authored now.
- **Dependency:** final in-game validation waits on Sol-Configs' RP-1 compat
  landing (upstream, awaited). Our side is built "ready" in the meantime.

| Decisive convention | Value | Source |
|----------------------|-------|--------|
| RP-1 detection tag | `RP-0` (not `RP-1`) | `:FOR[RP-0]` throughout `RP-1/GameData/RP-1/` |
| RealismOverhaul tag | `RealismOverhaul` | `:FOR[RealismOverhaul]` in RO cfgs |
| ROKerbalism profile tag | `ProfileRealismOverhaul` (profile name `RealismOverhaul`) | `ROKerbalism/.../Profiles/ROKerbalism.cfg` |
| Principia epoch | `JD2433282.5` — already our convention | Principia `astronomy/sol_initial_state_*.cfg` |
| flightGlobalsIndex | 1000+ avoids RO 0–99 — already safe | `guideline.md §7` |

---

## 2. Career layers NearStars owns (base-independent)

### WS3 — ResearchBodies under RP-1  *(primary; supersedes old rp1-compat.md sketch)*

- **No observatory mechanic exists in RP-1.** The stock TrackingStation is a
  DSN/comms facility, not an astronomy host. Discovery is **part-based**.
- RB telescope parts sit on `TechRequired = spaceExploration`, which RP-1
  routes to its unbuildable `orphanParts` sink. **Reseat to `scienceSatellite`**
  (where RP-1 puts its own `spaceExploration`-tagged film cameras; alt
  `deepSpaceScience` for a later gate). Gate `:NEEDS[ResearchBodies&RP-0]`.
- RB's `CC_RB_*` contracts pollute RP-1's tuned progression (RP-1 doesn't
  suppress third-party packs). **Ship them `:NEEDS[!RP-0]`** — RP-1 careers
  never see them; non-RP-1 installs keep telescope-discovery contracts.
- Re-verify RB's widened `observatorylvl*range` covers our distances at the
  chosen TS level.

### WS4 — ROKerbalism radiation

Our DB radiation/stellar-wind fields are already anchored to the ROKerbalism
Sun baseline (`radiation_surface = 46.5`), so the model is RO-aligned.

- Author per-body radiation as `RadiationModel` (belt/pause geometry) +
  `RadiationBody` (binds CelestialBody → model) in the style of ROKerbalism's
  `GameData/KerbalismConfig/System/Radiation.cfg`, with its **underscored**
  field names. `name` = Kopernicus internal body name. Storm magnitudes are
  global — leave alone.
- Gate `:NEEDS[ProfileRealismOverhaul]`. Becomes the RO-profile output mode of
  the (future) kerbalism-cfg writer. See [[project-nearstars-stellar-wind-kerbalism]].

### WS2′ — Principia (stays Sol, no RSS variant)

NearStars already appends body blocks to the single Principia root via
`@principia_gravity_model` / `@principia_initial_state` (no second root —
crashes). Under RP-1-on-Sol-Configs the same Sol patch applies; epoch already
matches (`JD2433282.5`). **No RSS coordinate variant needed.** One latent
constraint: if the base ships a *full* `principia_initial_state`, Principia
requires it to cover every body, so NearStars must supply Cartesian states for
all its bodies (we store `derived.icrs_*_km`) — not rely on Keplerian fallback.

### WS5 — RealAntennas (document-only)

No hard range cap; at our real distances (~10¹³–10¹⁴ km) the link budget
degrades cleanly to data-rate 0 (fails safe, no crash). Interstellar comms
won't establish under RP-1 — expected behaviour. No cfg; document the limit.

### WS6 — flightGlobalsIndex / RO body realism (no work)

Index already avoids RO's 0–99. Bodies are real-data based ⇒ naturally
RO/FAR/RealHeat-consistent. No patch expected.

---

## 3. Implications for NearStars

1. **Stay Sol-based.** No classic-RSS Kopernicus or Principia variant. The
   earlier dual-base / RSS-coordinate workstreams are dropped.
2. **Build the career layers now, gated on RP-0 / RealismOverhaul /
   ProfileRealismOverhaul / Principia** — independent of Sol-Configs' bridge
   mechanism, so upstream's design choices can't break them.
3. **Emit stays deferred to project end.** This note + skill updates make the
   conventions canonical now.
4. **Validation is gated on upstream.** Sol-Configs' RP-1 compat must land
   before end-to-end testing; until then our side is "ready, unvalidated."
5. **Skills to update:** `researchbodies-cfg/references/rp1-compat.md`
   (rewrite per grounded reseat + contract findings — actively wrong today),
   and the kerbalism-cfg writer spec (RO-profile mode). principia-cfg and
   kopernicus-cfg need no RSS-variant work after the pivot.

---

## 4. Open questions

- **[upstream] Sol V1.0 RP-1 compat shape + timeline.** Grounded mechanism:
  MM derives `:NEEDS[X]`/`:FOR[X]` from **loaded DLL assembly names**, not cfg.
  Classic RSS ships `RealSolarSystem.dll` → registers the `RealSolarSystem`
  tag that RP-1/RO patches gate on. **Sol-Configs is config-only (no DLL)** and
  registers only `SolSystem`, so today RP-1/RO patches do not fire on it.
  ballisticfox (Patreon 2025-05-29) declares Sol **V1.0 will be "100% RP-1
  balanced and compatible"** with a "seamless transition between RSS and Sol",
  replacing RSS (RSS-Reborn overlay support being dropped); Sol already ships
  `Patches/Sol-RP1.cfg`. So V1.0 is expected to provide the `RealSolarSystem`
  tag bridge itself. This is a **declared, not-yet-shipped** goal. It does NOT
  block our career-layer authoring (we gate on `RP-0`/`RealismOverhaul`/
  `ProfileRealismOverhaul`/`Principia`, all present once RP-1/RO load), only
  final validation. Body naming + launch sites already line up (Sol's Moon
  internal `name = Moon`; Sol replicates `us_cape_canaveral` under `SolSystem`).
- **[pre-existing] Real distance in Principia.** We emit stars at real
  ~10¹³–10¹⁴ km. Confirm Principia integrates them stably (REBOUND sim
  cross-check). Inherited from the Sol path, not introduced by RP-1.
