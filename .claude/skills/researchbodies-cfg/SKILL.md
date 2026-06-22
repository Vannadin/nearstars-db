---
name: researchbodies-cfg
description: >
  Write and review ResearchBodies .cfg files for the NearStars KSP planet
  pack — the optional **discoverability** layer that hides a body until the
  player discovers it with an observatory/telescope. Use this skill when the
  user wants to create, patch, or debug a ResearchBodies config — phrases
  like "ResearchBodies cfg 만들어줘", "discoverability 패치", "이 바디 숨김
  처리", "ONDISCOVERY 메시지 작성", "IGNORELEVELS 설정", "발견 난도 cfg",
  "write a researchbodies patch", or "generate the discovery cfg from Phase
  4". Maps each body's real detection status (Phase 4 `identity >
  discoverability`) to an `IGNORELEVELS` start-visibility tuple +
  `ONDISCOVERY` message, and emits one `RESEARCHBODIES { loadAs = mod ... }`
  MM patch. Grounded in `JPLRepo/ResearchBodies` v1.13.0.0 — every schema
  claim cites `<file>.cs:line`. NearStars conventions (NEEDS tag, Scheme-A
  difficulty grading, body-name = Kopernicus internal name, emit deferred
  to project end) are pre-set — do not ask the user about them.
mod_version: 1.13.0.0
---

# ResearchBodies CFG Writing Guide

> **Scope.** ResearchBodies (JPLRepo) hides celestial bodies until the
> player discovers them via an observatory research plan / telescope. This
> skill is the NearStars-specific implementation of its **discoverability**
> axis: which RB nodes the project uses (`RESEARCHBODIES` + `ONDISCOVERY` +
> `IGNORELEVELS`), how a body's real detection status maps to start-
> visibility, and the single `loadAs = mod` MM patch NearStars emits.
>
> ResearchBodies is an **optional** dependency. Uninstalled → NearStars is
> fully visible and works normally. The patch is guarded
> `:NEEDS[ResearchBodies&Kopernicus]`.

## Source references

- **ResearchBodies source**: `JPLRepo/ResearchBodies` v1.13.0.0 — the cfg
  loader is `Database.cs`; difficulty enum `RBEnums.cs`; per-body state
  `CelestialBodyInfo.cs` / `BodyIgnoreData.cs`.
- Full source-cited schema inventory: workspace `research-notes.md`.
- Reference docs in this skill:
  - [`references/global-settings.md`](references/global-settings.md) — the
    `RESEARCHBODIES` node, `loadAs = mod`, global knobs, patch skeleton.
  - [`references/ondiscovery.md`](references/ondiscovery.md) — discovery
    message subnode.
  - [`references/ignorelevels.md`](references/ignorelevels.md) — per-body
    start-visibility tuple.
  - [`references/db-mapping.md`](references/db-mapping.md) — Phase 4
    discoverability → cfg mapping (Scheme A) + input schema.
  - [`references/pitfalls.md`](references/pitfalls.md) — throws, surprises,
    dead/legacy nodes.
  - [`references/rp1-compat.md`](references/rp1-compat.md) — RO/RP-1
    compatibility analysis + the planned (deferred) RP-1 integration patch.

## NearStars conventions (pre-set — do not ask)

1. **One patch node:** `RESEARCHBODIES:NEEDS[ResearchBodies&Kopernicus] {
   loadAs = mod; name = NearStars; ONDISCOVERY {...} IGNORELEVELS {...} }`.
   `loadAs = mod` is mandatory or the data is silently ignored
   (`Database.cs:289`).
2. **Per-body only.** NearStars authors `ONDISCOVERY` + `IGNORELEVELS`.
   Globals (cost/odds/telescope range) stay at RB defaults — see
   `global-settings.md`.
3. **Difficulty grading** (canonical, revised 2026-06-22): `naked_eye` →
   `true true true true` (stars always visible); `confirmed`/`candidate`/
   `disputed` → `true false false false` (planets discover-by-observation,
   Easy shows them); `fictional` → `false false false false` (always
   discover). See `db-mapping.md`.
4. **Body name = exact Kopernicus internal name** (`Body { name }`), not
   `displayName`. Barycenter anchors (radius<100m) are omitted — RB
   auto-drops them (`Database.cs:91,164`).
5. **Real-detection identity.** `candidate`/`disputed` discovery messages
   cite the real detection paper (bibcode from DB `sources[]` / Phase 4
   note). Never invent a citation.
6. **Emit is deferred.** Per the project defer-emit decision, the bulk
   `RESEARCHBODIES` patch is generated at project end with the other cfg
   writers. Build/validate the emitter now; do not run a project-wide emit
   unless the user explicitly asks.
7. **Target = non-RP-1 (Sandbox / Science on RSS) for now.** RB works as
   shipped there. RP-1 career support needs an integration patch (telescope
   part / contract / economy) and is **deferred to a future update** — see
   `references/rp1-compat.md`. Until then, RP-1 players simply omit RB
   (discoverability is optional → all bodies visible).

## Workflow

1. **Read the body's discoverability** from `phase4/<system>.yaml`
   (`discoverability:` list — schema in `db-mapping.md`). Category is the
   real detection status: `naked_eye` / `confirmed` / `candidate` /
   `disputed` / `fictional`.
2. **Map** category → `IGNORELEVELS` tuple (Scheme A) and compose the
   `ONDISCOVERY` message (cite the paper for candidate/disputed).
3. **Emit** with `scripts/emit_researchbodies_cfg.py` (deterministic —
   reads Phase 4, writes the single MM patch). Or hand-write following the
   skeleton in `global-settings.md`.
4. **Verify** against `pitfalls.md`: `loadAs = mod` present; every
   `IGNORELEVELS` value is exactly 4 `true`/`false`; body names exact;
   no barycenters; candidates carry a real bibcode.

## Minimal example

```
RESEARCHBODIES:NEEDS[ResearchBodies&Kopernicus]
{
    loadAs = mod
    name = NearStars

    ONDISCOVERY
    {
        Polyphemus = JWST/MIRI 15.5 um direct imaging resolves a faint companion to Alpha Centauri A — the candidate "S1". (Sanghi & Beichman 2025)
    }
    IGNORELEVELS
    {
        // body = easy normal medium hard
        AlphaCentauriA = true true true true       // naked_eye
        Polyphemus     = true false false false    // candidate
        Pandora        = false false false false   // fictional
    }
}
```
