# ResearchBodies cfg skill — Context Notes

Append-only log of decisions + reasoning during the build.

## 2026-06-22 — kickoff

- User asked to build a ResearchBodies cfg-emit skill. Direction was
  pre-decided (2026-06-22 discoverability = optional RB layer); this is
  the "추후 RB cfg-emit 스킬" promised in
  `project_nearstars_discoverability_researchbodies`.
- Following the firefly-cfg/principia workspace pattern: build under
  `.agents/skills/researchbodies-cfg-workspace/`, graduate the live skill
  to `.claude/skills/researchbodies-cfg/`.
- RB license per memory = MIT / CC-BY-NC-SA. License-compatible to ship a
  cfg-authoring skill (no Patreon-EA boundary, unlike scatterer/eve).
  → so this skill IS git-tracked (lives in .claude/skills/), like
  firefly/kopernicus/principia, not local-only like scatterer.
- Cloned source: `researchbodies-repo/`. Key files spotted at top level:
  Database.cs, BodyIgnoreData.cs, CelestialBodyInfo.cs, RBGameSettings.cs,
  SettingsParms.cs, RBEnums.cs, CCContractExtensions*.cs, Distribution/,
  ProgressiveCBMaps/.
- DB detection data lives at `planet.raw.discoverymethod` (NASA Exoplanet
  Archive: "Radial Velocity", "Transit", "Imaging", "Astrometry"…).
  Need to also locate candidate-vs-confirmed status + the discovery-paper
  bibcode for ONDISCOVERY citations. TBD which DB layer holds those.
- Launched research subagent to inventory the cfg schema with file:line
  citations (avoids me dumping the whole C# repo into context).

## 2026-06-22 — DB detection-data recon (non-overlapping with research agent)

- `planet.raw.discoverymethod` enum seen: "Radial Velocity", "Transit",
  "Imaging", "Astrometry", and **"predicted"** (Alpha Cen A b = predicted,
  i.e. stability-selected / not a clean confirmed detection).
- Candidate-vs-confirmed status is NOT a clean structured field — it lives
  in `raw.reference` prose + the `sources[]` list (each source has
  `title`/`doi`/`bibcode`/`used_for`). Alpha Cen A b prose: JWST/MIRI
  15.5µm direct-imaging **candidate** 'S1', Sanghi & Beichman 2025
  (arXiv:2508.03812 / 2508.03814).
- IMPLICATION for mapping: detection STATUS (candidate/confirmed/predicted/
  fictional-moon) is not fully machine-readable today. Options:
  (a) derive difficulty purely from `discoverymethod`; or
  (b) add a small curated `discovery` field (status + difficulty +
      detection-paper bibcode for the ONDISCOVERY message). 
  (b) fits feedback_phase4_facet_choices (discovery is an art-direction
  facet the owner picks per body) and gives a clean bibcode for the
  ONDISCOVERY citation. Lean (b); confirm with owner in mapping review.
- Body name in cfg must be the in-game name (e.g. "Polyphemus"), not the
  DB name ("Alpha Centauri A b"). Naming canonical = _naming.py — emitter
  must reuse it, not reinvent the slug/display-name conversion.

## 2026-06-22 — schema research landed + owner decisions

- Research subagent returned full source-cited schema → research-notes.md.
  Key corrections/confirmations vs memory:
  - ONE top node `RESEARCHBODIES`; ONDISCOVERY/IGNORELEVELS are SUBnodes.
  - Third-party pack MUST use `RESEARCHBODIES { loadAs = mod ... }` —
    `loadAs = mod` mandatory or data silently dropped.
  - IGNORELEVELS = exactly 4 booleans `true`/`false` (NOT 1/0), order
    Easy Normal Medium Hard; `true` = visible-at-start for that diff.
  - Default (no entry) = hidden at ALL difficulties. Silence = hidden.
  - ONDISCOVERY matched by substring `Contains`; IGNORELEVELS exact `==`.
    Use exact internal Kopernicus body names.
  - Barycenters (radius<100m) auto-dropped from UI — confirms memory; do
    not author for them.
  - LICENSE nuance: RB is MIT (simon56modder parts) + "ALL RIGHTS
    RESERVED" (other parts) per README. We author our OWN loadAs=mod
    patch + cite source lines (firefly-GPL posture). No code/cfg copying.

- OWNER DECISIONS (2026-06-22):
  1. Mapping INPUT = the **Phase 4 `identity > discoverability` facet**
     (phase4/*.yaml gate rows), NOT a new curated DB field. So the
     emitter reads Phase 4 discoverability decisions. Currently only
     alpha_centauri has it filled (✅); other 3 systems ⬜ (facet still
     being filled). Skill is built now regardless; emit deferred.
  2. SCOPE = skill body + emitter; do NOT run the project-wide emit
     (defer-emit decision stands). Dry-run validation only.

- DESIGN: Phase 4 gives the discoverability CATEGORY/intent per body
  (prose today: "candidate→observe", "star→always visible"). The SKILL
  defines the category → IGNORELEVELS 4-bool tuple + ONDISCOVERY message
  mapping. Proposed category vocabulary (real detection status driven):
  naked_eye / confirmed / candidate / predicted-disputed / fictional.
  See mapping-proposal.md — owner picks the tuple grading.

## 2026-06-22 — RO/RP-1 compatibility check (owner asked before judging)

VERIFIED FROM RB SOURCE:
- RB ships its own telescope PARTS (`TrackBodiesTelescope`,
  `InfraredTelescope`) with STOCK tech tree + stock funds:
  `TechRequired = spaceExploration`, `entryCost = 9530`
  (Distribution/.../Parts/telescope/telescope.cfg:11-12). RP-1 uses a
  custom tech tree + different economy → part mis-placed / unbuyable.
- RB ships its own Contract Configurator contracts
  (Distribution/.../Contracts/CC_RB_*.cfg) — not balanced for RP-1's
  progression; potential clash/duplication.
- RB's Kopernicus patch only bumps telescope range
  (ResearchBodiesMMKopernicus.cfg) — no RP-1/RO awareness.

WEB:
- RP-1 wiki "Extra Mods to Consider" does NOT list ResearchBodies
  (neither recommended nor blacklisted) — not a community-standard
  RP-1 combo.
- No authoritative "works/breaks with RP-1" report found.

RISK: our cfg uses only ONDISCOVERY + IGNORELEVELS (hide/show data), but
the DISCOVERY ACTION depends on RB's telescope/observatory. In RP-1 if
the telescope part is unreachable → NearStars bodies stay hidden forever
= soft-lock. This is a mechanic-integration issue, not just cfg.

WORKAROUND (verified option): global `allowTrackingStationLvl1 = true`
lets the player use the Tracking-Station-level observatory WITHOUT the
telescope part — sidesteps the tech-tree problem. Still need to address
RB-contract clash + economy in RP-1.

BEARING ON SKILL: discoverability is `:NEEDS[ResearchBodies&Kopernicus]`
optional — RB uninstalled → everything visible, so "RP-1 players just
omit RB" is a clean path. If we WANT RB to work under RP-1, the skill
will need an RP-1 integration patch (part tech-tree reseat OR
allowTrackingStationLvl1 + disable RB contracts). DECISION PENDING with
owner. Skill build (references + emitter) stands regardless.

## 2026-06-22 — "planets-only telescope" → plugin, delegated to Schultz

- Owner wants moons NOT telescope-discoverable (hidden, found by flyby
  only), planets telescope-discoverable. Native RB can't do this (telescope
  pools every hidden in-view body, random-picks one; hidden moon findable +
  cascades to parent). Verified `PartModule.cs:222-260` + `FoundBody`
  cascade (child→parent only).
- Resolution: a Harmony runtime patch (filter moons out of the telescope
  candidate list) — NOT a fork (RB partly ARR). Decided BACKLOG, and all
  mod-plugin (C#/Harmony) work delegated to Schultz. Brief written:
  plugin-brief-telescope-moon-filter.md.
- cfg skill unaffected: mapping stays `fictional → F F F F`; the plugin
  changes only HOW a hidden moon is found (flyby yes / telescope no). No
  emitter change. Interim (pre-plugin): native RB telescope can also find
  hidden moons — acceptable.

## Decisions log

- 2026-06-22: Grading REVISED from Scheme A. After the mod-mechanic
  explainer, owner realized the discovery action always works per-body
  (only cost/odds/range are global), so confirmed planets being always-
  visible wasted the discovery loop. New canonical: stars `T T T T`,
  all planets (confirmed/candidate/disputed) `T F F F` (Easy-visible,
  Normal+ discover), fictional `F F F F`. Emitter `SCHEME` dict + all
  docs updated. confirmed vs candidate now differ only in ONDISCOVERY
  message text.
