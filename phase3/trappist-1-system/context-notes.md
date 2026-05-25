---
type: workspace
title: "TRAPPIST-1 system Phase 3 — context notes"
slug: trappist-1-system-context-notes
cluster: system-trappist-1
cluster_role: member
status: active
related: [[trappist-1-system-audit-pass-2026-05-22]], [[trappist-1-system-checklist]], [[trappist-1-system-manual-paper-followup]], [[trappist-1-system-paper-count-summary]]
created: 2026-05-21
updated: 2026-05-25
tier: public
---
# TRAPPIST-1 system Phase 3 — context notes

Append-only log of decisions made while extending Phase 3 synthesis to
the remaining six TRAPPIST-1 planets (b, c, e, f, g, h). d is the
already-completed pilot.

## 2026-05-21 — Scope and depth

User confirmed: full d-level depth for all 6, parallelized fetches.
Each planet gets ~300 lines of synthesis: decisions table (~30 rows),
Surface / Atmosphere / Rotation / Visual sections, full bibliography
with Read / context / instrument / not-read categories.

## 2026-05-21 — Per-planet observational state going in

This drives how heavily synthesis vs. measurement each planet leans:

- **b** — innermost. JWST MIRI 12.8 μm emission (Greene 2023):
  Tday ≈ 503 K, A_B = 0.0 ± 0.1, atmosphere-free or trace. The
  cleanest "definitely bare rock" case. Lava world potential at
  3.4 S⊕ insolation.
- **c** — JWST MIRI 15 μm emission (Zieba 2023): Tday ≈ 380 K
  consistent with bare rock + low albedo OR very thin (≲10 bar) CO₂.
  Also constrained, slightly more atmosphere room than b.
- **d** — DONE. JWST NIRSpec transmission (Piaulet 2025) flat,
  most-atmospheres-excluded. Adopted thin-atmosphere + terminator
  H₂O ice cloud scenario.
- **e** — habitable zone center. No JWST transmission yet published
  in the same depth. Way 2025 ROCKE-3D GCM explores
  Venus/Earth/Dead variants. Best HZ candidate. Will rely heavily on
  Wolf 2017, Turbet 2018, Way 2025, Lustig-Yaeger 2024 (if available)
  GCM predictions.
- **f** — outer HZ edge. Cooler than e, ~Teq 215 K. Turbet 2018 places
  it in the "Snowball Earth or thin CO₂" branch. Lim 2023 JWST/NIRISS
  transmission excludes H₂-rich (per the d paper's reference list).
- **g** — outer HZ. ~Teq 195 K. Even more snowball-prone than f. Less
  observational follow-up; relies on outgassing/escape models.
- **h** — outermost. ~Teq 169 K. Sub-Mars mass (0.33 M⊕). Permanently
  frozen analog; possible subsurface ocean if internally heated.

## 2026-05-21 — Methodology reuse from d

Constants reused for all 7 (host star is the same):

- Host: TRAPPIST-1 M8V, 2566 K, 0.1192 R☉, 0.0898 M☉, 0.000522 L☉
- Age: 7.6 ± 2.2 Gyr (Burgasser 2017)
- Stellar SED color tint: red-orange `~#ff7a1a` for visual sections
- Tidal lock baseline 1:1, obliquity 0
- Eccentricity: from Agol 2021 TTV (per planet)
- Mass / radius / a / P: Agol 2021 TTV
- "Sister planets in sky" geometry: near-coplanar (Agol 2021)
- ~8 Gyr age implies heavy impact accumulation on all surfaces

## 2026-05-21 — Per-planet expected scenario choices

Working hypothesis before reading papers (will revise as needed):

- **b** — bare hot rock (basaltic/melt-resurfaced). No atmosphere.
  Strong substellar magma-ocean residual? Way 2024 calls it "exo-Io"
  candidate from induction heating. Visual: dark basalt + iron oxide
  patches under fierce red glare, possibly fresh lava in patches.
- **c** — bare warm rock. No detectable CO₂ atmosphere down to thin
  limit. Similar palette to b but cooler, less melt.
- **e** — adopt habitable-temperate scenario: 1 bar N₂+CO₂+H₂O
  atmosphere, ocean-bearing, blue-tint with cloud cover. The classic
  "best habitable candidate" cfg variant.
- **f** — outer HZ, snowball/cold thin-CO₂ branch. Mostly icy
  surface, thin atmosphere. Possible subglacial liquid water but
  surface frozen.
- **g** — fully frozen, slightly thicker CO₂ to stave off complete
  collapse (Wordsworth 2017 cold-trap idea). Snowy surface.
- **h** — Mars/Pluto analog. Either fully frozen N₂/CO₂ ice with bare
  surface in places, or volatile-stripped bedrock. Tend toward icy
  given outer location.

## 2026-05-21 — Heading structure (frozen for ko mirror parity)

All six syntheses use the same H2 structure as d:
- (intro paragraphs, no H2)
- ## Decisions
- ## Surface synthesis
- ## Atmosphere synthesis
- ## Rotation & spin synthesis
- ## Visual styling
- ## Bibliography
- ### Read (visual-informative, drove decisions above)
- ### Read (context / methodology, not decision-driving)
- ### Read (instrument-only, not visual-informative)
- ### Not read — no arXiv preprint available (N papers)
- ## Open items for follow-up

If a category is empty for a given planet, the H3 heading is still
kept (with a brief "none for this planet" note) so the ko mirror
parses cleanly.

## Related

- [audit-pass-2026-05-22](audit-pass-2026-05-22.md) — sibling workspace doc in `trappist-1-system/`
- [checklist](checklist.md) — sibling workspace doc in `trappist-1-system/`
- [manual-paper-followup](manual-paper-followup.md) — sibling workspace doc in `trappist-1-system/`
- [paper-count-summary](paper-count-summary.md) — sibling workspace doc in `trappist-1-system/`
- [system-trappist-1 entity pages](../../docs/phase3/trappist-1-e.md) — parent topic this workspace contributes to
