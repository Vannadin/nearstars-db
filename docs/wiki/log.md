---
type: log
title: "Wiki Activity Log"
slug: wiki-log
updated: 2026-05-24
tier: public
---

# Wiki Activity Log

Append-only record of `/wiki ingest`, `/wiki lint`, `/wiki query`
operations performed by the [llm-wiki](../../.agents/skills/llm-wiki/SKILL.md)
skill. Newest entry on top.

Format per skill §6: heading `## [YYYY-MM-DD] {operation} | <title>`
followed by structured body.

---

## [2026-05-25] ingest | workspace cluster backfill (32 files, bulk script)

Source: `phase2/<topic>/`, `phase3/<system>/`, `docs/phase1-50ly/`,
`docs/famous-20-non-hosts/` workspace dirs
Pages updated: 32 (plan / checklist / context-notes / audit / report /
manual-followup / paper-count-summary across 12 workspace dirs)
Method: `scripts/wiki/bulk-add-frontmatter.py` — newly-written
permanent utility for workspace ingestion. YAML frontmatter
(type=workspace, cluster, status, related to trio companions) +
`## Related` section linking to trio companions + parent cluster hub.
Contradictions flagged: none
Tier: public

Notes:
- First version of the bulk script had a slug-stem bug producing broken
  link labels (`[22](22.md)` etc.). Reverted, fixed (use file stem
  instead of slug-derived stem), re-ran. Final output verified on
  random sample.
- Cluster assignments (CLUSTER_MAP in script):
  - `phase3/trappist-1-system/*` + `phase2/trappist_1/*` → system-trappist-1
  - `phase3/alpha-cen-proxima-system/*` + `phase2/alpha_centauri_proxima/*` → system-alpha-cen
  - `phase3/html-pipeline/*` + `phase3/stability-sim/*` + `phase2/skill-phase3-optimization/*` → phase3-procedure
  - `phase2/schema-expansion/*` + `phase2/skill-policy-permanence/*` + `docs/phase1-50ly/*` + `docs/famous-20-non-hosts/*` → methodology
  - `phase3/_audit/*` → comparisons
- Report-type files (STABILITY_REPORT, audit-pass-*, paper-count-summary,
  art-redundancy-*) → `type: synthesis`. Others → `type: workspace`.
- The bulk script is now reusable for future workspace dirs — add the
  path to WORKSPACE_FILES list and re-run.

This closes the workspace-docs disconnect the user surfaced 2026-05-25.

## [2026-05-25] lint | Phase 2 bootstrap health check

Frontmatter coverage: 26 / 27 wiki pages (plans/README.md intentionally
excluded as a folder meta-doc).
Orphans: 0
EA-identifier leaks (public tier): 0
Stale claims: not assessed (would require LLM read-through)
Cross-tier link integrity: all `[name](.agents/skills/...)` paths verified
to exist on disk (broken-on-public, working locally — by design).

Conclusion: Phase 2 bootstrap effectively complete. Wiki layer is
healthy across 4 clusters (system-trappist-1, system-alpha-cen,
methodology, comparisons) + 1 partial cluster (mod-principia).

Outstanding follow-ups (not blocking):
- Host star entity page for TRAPPIST-1 (M8V dwarf, host_star: Trappist1)
- Proxima c entity page if/when discovery is confirmed at 3σ
- _papers/*.md source frontmatter (would let sources: lists become wikilinks)
- plans/README.md ingest if the wiki should formally cover it
- Trigger setup (cron / pre-commit hook / loop) — user decision pending

## [2026-05-25] ingest | mod-principia cluster + skill cross-refs (4 pages)

Source: `docs/reference/principia-cfg-reference.md` (concept ingest) +
`.agents/skills/{kopernicus-cfg,firefly-cfg,nearstars-phase3}/SKILL.md`
(Related-only ingest; skill frontmatter left untouched to avoid
disturbing the skill-system fields like `name`, `description`,
`mod_version`).

Pages updated:
  - `docs/reference/principia-cfg-reference.md` (full frontmatter +
    `## Related`; cluster_role: hub, secondary_cluster: physics-epoch)
  - `.agents/skills/kopernicus-cfg/SKILL.md` (Related section only)
  - `.agents/skills/firefly-cfg/SKILL.md` (Related section only)
  - `.agents/skills/nearstars-phase3/SKILL.md` (Related section only)
Contradictions flagged: none
Tier: public (none of these are local-only)

Notes:
- mod-principia is the first cluster spanning a reference doc + a skill
  (principia-cfg-reference + .agents/skills/principia-cfg/). The
  reference doc is the hub; skill is a member listed via Related.
- principia-cfg-reference declares dual cluster: mod-principia hub +
  physics-epoch member (mirroring binary-epoch-pipeline's pattern).
- Skill SKILL.md files use existing skill frontmatter
  (name, description, mod_version) — wiki added only the Related
  section near the end of each.

## [2026-05-24] ingest | methodology concept cluster + comparisons cluster (11 pages)

Source: `docs/reference/*.md` (9 concept pages) + `docs/reference/rex-data-comparison.md` + `plans/stellarium-binary-orbit-comparison.md` (2 synthesis pages)
Pages updated:
  - `docs/reference/methodology.md` (HUB; cluster_role: hub; type=concept)
  - `docs/reference/adding_stars.md` (member)
  - `docs/reference/binary-epoch-pipeline.md` (member of methodology; secondary_cluster: physics-epoch hub)
  - `docs/reference/data-sources.md` (member; replaces existing Korean HTML header)
  - `docs/reference/archive_issues.md` (member)
  - `docs/reference/tools.md` (member)
  - `docs/reference/mod-reference.md` (member)
  - `docs/reference/mod-release-layout.md` (member)
  - `docs/reference/guideline.md` (member)
  - `docs/reference/rex-data-comparison.md` (type=synthesis; cluster=comparisons; status: promoted)
  - `plans/stellarium-binary-orbit-comparison.md` (type=synthesis; cluster=comparisons; existing frontmatter extended)
Contradictions flagged: none
Tier: public

Notes:
- methodology.md gets `cluster_role: hub` and its `## Related` lists all 8 cluster members + cross-cluster pointers (principia-cfg-reference, rex-data-comparison).
- binary-epoch-pipeline.md declares dual cluster membership: `methodology` (member) + `physics-epoch` (hub for the multi-star Kepler→ICRS math). First test of secondary_cluster fields.
- Cross-cluster links materialized:
  - methodology cluster ↔ system-trappist-1, system-alpha-cen (entity clusters cite methodology/binary-epoch-pipeline)
  - comparisons cluster ↔ entity clusters (rex-data-comparison.related includes all 7 TRAPPIST + 2 α Cen + Proxima)
- Skipped: principia-cfg-reference (defer to mod-principia cluster batch), kopernicus-cfg/firefly-cfg SKILL.md (defer to skill-cluster batch), plans/_template.md (template, not content), plans/README.md (meta-doc), plans/rex-data-comparison.md (already a stub redirect to docs/reference/).

## [2026-05-24] ingest | system-alpha-cen cluster (5 entity pages)

Source: existing `docs/phase3/{alpha-centauri-a,alpha-centauri-b,proxima-cen,proxima-cen-b,proxima-cen-d}.md`
Pages created: none (frontmatter + `## Related` added to existing pages)
Pages updated:
  - `docs/phase3/alpha-centauri-a.md` (frontmatter + `## Related`, type=star, confidence: high, scenario: quiet G2V solar twin)
  - `docs/phase3/alpha-centauri-b.md` (frontmatter + `## Related`, type=star, confidence: high, scenario: K1V metal-rich, no confirmed planets)
  - `docs/phase3/proxima-cen.md` (frontmatter + `## Related`, type=star, confidence: high, scenario: M5.5Ve flare star with kG dipole + 7-yr cycle)
  - `docs/phase3/proxima-cen-b.md` (frontmatter + `## Related`, type=planet, confidence: medium, scenario: 1-bar N₂/CO₂ aquaplanet eyeball)
  - `docs/phase3/proxima-cen-d.md` (frontmatter + `## Related`, type=planet, confidence: medium, scenario: Mercury-like USP with Na exosphere)
Contradictions flagged: none
Tier: public

Notes:
- 3 stars + 2 planets in this cluster. star entities use new frontmatter fields: `binary_partner` (a↔b), `wide_companions` (proxima→AB), `hosted_planets` (proxima→[b,d]).
- Cross-cluster link: `proxima-cen-b.related` includes `trappist-1-e` (both are M-dwarf HZ aquaplanet analogs with eyeball geometry).
- α Cen AB is referenced as the canonical worked example in `binary-epoch-pipeline.md §9` and the cross-check target of `plans/stellarium-binary-orbit-comparison.md` — links added on both alpha-centauri-a and -b.
- Open follow-ups (logged for future ingest):
  - Host-star entity page for TRAPPIST-1 (still pending from earlier ingest)
  - Proxima c candidate (sub-Neptune at 5.2 AU, unconfirmed) — no entity page yet; may be created if discovery confirmed
  - `_papers/*.md` source frontmatter (would let us convert string `sources:` to wikilinks)

## [2026-05-24] ingest | system-trappist-1 cluster (Phase 2 dry-run, 7 entity pages)

Source: existing `docs/phase3/trappist-1-{b,c,d,e,f,g,h}.md`
Pages created: none (frontmatter + `## Related` added to existing pages)
Pages updated:
  - `docs/phase3/trappist-1-b.md` (frontmatter + `## Related`, confidence: high, scenario: airless ultramafic)
  - `docs/phase3/trappist-1-c.md` (frontmatter + `## Related`, confidence: medium, scenario: thin O₂ over basalt)
  - `docs/phase3/trappist-1-d.md` (frontmatter + `## Related`, confidence: low, scenario: thin atm + terminator H₂O ice)
  - `docs/phase3/trappist-1-e.md` (frontmatter + `## Related`, confidence: high, scenario: aquaplanet eyeball)
  - `docs/phase3/trappist-1-f.md` (frontmatter + `## Related`, confidence: medium, scenario: eyeball aquaplanet (1 bar CO₂))
  - `docs/phase3/trappist-1-g.md` (frontmatter + `## Related`, confidence: medium, scenario: full snowball)
  - `docs/phase3/trappist-1-h.md` (frontmatter + `## Related`, confidence: low, scenario: frozen sub-Mars with patchy frost)
Contradictions flagged: none
Tier: public

Notes:
- All 7 pages now have YAML frontmatter declaring type=entity, cluster=system-trappist-1, kopernicus_name, scenario, confidence
- `## Related` sections cross-link adjacent siblings + methodology + mod-reference + rex-data-comparison §10
- No host-star entity page exists yet for TRAPPIST-1 itself (M8V dwarf); will be created on first ingest of a star entity batch
- Source citations in frontmatter are paper-name strings; future pass can convert to wikilinks once `_papers/*.md` get their own `source` frontmatter
- Dry-run scope: this batch validates the ingest workflow before applying to docs/reference/ (concept pages) and docs/phase3/ alpha-cen + proxima cluster

## [2026-05-24] initialize | wiki scaffold created

Source: `.agents/skills/llm-wiki/SKILL.md`
Pages created: `docs/wiki/{index.md, log.md, hot.md, overview.md}`
Pages updated: none
Contradictions flagged: none
Tier: public

Notes: skill defined; bootstrap not yet started. Existing wiki pages
(`docs/reference/*`, `docs/phase3/*`, `plans/*`) lack frontmatter and
`## Related` sections — to be added in Phase 2 bootstrap. Smart
Connections chunk embeddings (`.smart-env/`) still present; will be
dropped once `## Related` sections supersede chunk-based discovery.
