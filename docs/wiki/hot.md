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

**Phase 2 bootstrap complete (2026-05-25).** 27 wiki pages across
7 clusters now have frontmatter + `## Related`:
- system-trappist-1: 7 entity pages
- system-alpha-cen: 5 entity pages (3 stars + 2 planets)
- methodology: 9 concept pages (1 hub + 8 members)
- comparisons: 2 synthesis pages
- mod-principia: 1 reference + 1 skill cross-ref
- mod-kopernicus: 1 skill cross-ref
- mod-firefly: 1 skill cross-ref
- phase3-procedure: 1 skill cross-ref

First lint pass (2026-05-25): 0 orphans, 0 EA leaks, 26/27
frontmatter coverage (`plans/README.md` intentionally excluded).

**Phase 3 (trigger automation) is the next decision point** — see Open
questions. The bootstrap pattern is now stable; new docs added to the
repo can use `/wiki ingest <path>` to receive the same treatment.

### Open questions

- **Trigger channel for `/wiki lint` schedule** — user decision pending:
  A (on-demand only) / B (on-demand + weekly cron) / C (on-demand +
  weekly cron + git pre-commit hook). Skill §8 has the comparison.
- Host star entity page for TRAPPIST-1 (M8V dwarf) — needs creation
  to complete the system-trappist-1 cluster.
- Proxima c candidate (unconfirmed sub-Neptune at 5.2 AU) — entity
  page may be created if discovery confirmed (currently <3σ).
- `_papers/*.md` source frontmatter — would let `sources:` lists in
  entity pages become wikilinks. Currently they're paper-name strings.
- `plans/README.md` ingest — meta-doc, may not need wiki frontmatter.

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

1. **2026-05-25** lint | Phase 2 bootstrap health check — 0 orphans,
   0 EA leaks, 26/27 frontmatter coverage. Conclusion: bootstrap
   complete.
2. **2026-05-25** ingest | mod-principia + skill cross-refs — 4 pages
   (principia-cfg-reference frontmatter + Related; 3 skill SKILL.md
   files Related-only).
3. **2026-05-24** ingest | methodology + comparisons clusters — 11 pages.

### Active pages

- `.agents/skills/llm-wiki/SKILL.md`
- `docs/wiki/{index,log,hot,overview}.md`
- `docs/phase3/trappist-1-{b,c,d,e,f,g,h}.md` (entity)
- `docs/phase3/{alpha-centauri-a,alpha-centauri-b,proxima-cen,proxima-cen-b,proxima-cen-d}.md` (entity)
- `docs/reference/{methodology,adding_stars,binary-epoch-pipeline,data-sources,archive_issues,tools,mod-reference,mod-release-layout,guideline,rex-data-comparison}.md` (concept + synthesis)
- `plans/stellarium-binary-orbit-comparison.md` (synthesis)
