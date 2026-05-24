---
type: hot
title: "Wiki Hot Cache"
slug: wiki-hot
updated: 2026-05-24
tier: public
---

# Wiki Hot Cache

~500-word session context cache. Read silently at session start when
wiki context is relevant. Updated by `/wiki refresh`, `/wiki lint`,
and any large ingest batch.

---

### Current focus

LLM Wiki bootstrap Phase 2 substantially complete. 23 wiki pages
across 4 clusters now have frontmatter + `## Related`:
- system-trappist-1: 7 entity pages
- system-alpha-cen: 5 entity pages (3 stars + 2 planets)
- methodology: 9 concept pages (1 hub + 8 members)
- comparisons: 2 synthesis pages

Outstanding clusters not yet ingested:
- mod-principia (principia-cfg-reference.md + skill)
- mod-kopernicus, mod-firefly (SKILL.md files for live skills)
- attribution (overlaps with methodology via data-sources; minimal new work)
- phase3-procedure (nearstars-phase3 skill — internal, may not need ingest)

Remaining bootstrap is small. Phase 3 (trigger automation) is the next
real decision.

### Open questions

- Trigger channel for `/wiki lint` schedule (A/B/C from skill §8) —
  user confirmation still pending.
- Should principia-cfg-reference + skill SKILL.md files be ingested
  next, or is bootstrap considered done?
- Host star entity page for TRAPPIST-1 (M8V dwarf) does not exist —
  flagged as ingest follow-up.
- Proxima c candidate (unconfirmed sub-Neptune at 5.2 AU) — entity
  page may be created if discovery confirmed.

### Recent decisions

- Wiki agent CAN read+write inside local-only skill workspaces
  (`scatterer-cfg`, future `eve-cfg`, `volumetrics-cfg`,
  `raymarched-*`). Output stays in those gitignored paths.
- Public wiki may reference local-only skills by *existence* (path),
  not by *content* (EA-derived field names).
- Lint enforces public-tier EA-identifier blocklist (see skill §9).
- `_papers/`, `db/`, `phase2/`, `phase3/` are raw tier — wiki never
  writes there.
- Entity frontmatter uses paper-name strings for `sources:` in this
  pass; conversion to wikilinks deferred until `_papers/*.md` get
  their own frontmatter (`type: source`).
- Cross-cluster links are encouraged where physically motivated
  (e.g., proxima-cen-b ↔ trappist-1-e — both M-dwarf HZ aquaplanets).

### Last 3 log entries

1. **2026-05-24** ingest | methodology + comparisons clusters — 11 pages
   (9 concept + 2 synthesis); first test of `cluster_role: hub`,
   `secondary_cluster`, `type: synthesis`.
2. **2026-05-24** ingest | system-alpha-cen cluster — 5 entity pages.
3. **2026-05-24** ingest | system-trappist-1 cluster — 7 entity pages.

### Active pages

- `.agents/skills/llm-wiki/SKILL.md`
- `docs/wiki/{index,log,hot,overview}.md`
- `docs/phase3/trappist-1-{b,c,d,e,f,g,h}.md` (entity)
- `docs/phase3/{alpha-centauri-a,alpha-centauri-b,proxima-cen,proxima-cen-b,proxima-cen-d}.md` (entity)
- `docs/reference/{methodology,adding_stars,binary-epoch-pipeline,data-sources,archive_issues,tools,mod-reference,mod-release-layout,guideline,rex-data-comparison}.md` (concept + synthesis)
- `plans/stellarium-binary-orbit-comparison.md` (synthesis)
