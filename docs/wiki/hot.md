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

**Phase 2 bootstrap fully complete + automation installed (2026-05-25).**

- 59 wiki pages across 8 clusters now have frontmatter + `## Related`
  (was 27 → +32 from workspace backfill)
- C-full automation installed: 4 slash commands (`/wiki-ingest`, `-lint`,
  `-refresh`, `-query`) + git pre-commit hook (symlinked from
  `scripts/wiki/precommit-ingest.sh`) + weekly cron script (manual
  crontab install pending)
- New utility `scripts/wiki/bulk-add-frontmatter.py` available for
  future bulk operations (add path to WORKSPACE_FILES list, re-run)

### Open questions

- **Weekly cron entry still needs manual crontab edit** — user runs
  `crontab -e` and adds the line printed by `scripts/wiki/install.sh`.
  Hook is already symlinked.
- Host star entity page for TRAPPIST-1 (M8V dwarf) — needs creation
  to complete the system-trappist-1 cluster.
- Proxima c candidate (unconfirmed sub-Neptune at 5.2 AU) — entity
  page may be created if discovery confirmed (currently <3σ).
- `_papers/*.md` source frontmatter — would let `sources:` lists in
  entity pages become wikilinks. Currently they're paper-name strings.
- Skill `references/*.md` (29 files in firefly-cfg, kopernicus-cfg,
  nearstars-add-star, nearstars-phase3, principia-cfg) — intentionally
  deferred. They're internal-to-the-skill, accessed via SKILL.md, may
  not need separate wiki frontmatter.
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

1. **2026-05-25** ingest | workspace cluster backfill — 32 files via
   `scripts/wiki/bulk-add-frontmatter.py` (phase2/, phase3/,
   docs/phase1-50ly/, docs/famous-20-non-hosts/).
2. **2026-05-25** lint | Phase 2 bootstrap health check — 0 orphans,
   0 EA leaks, then 26/27 frontmatter coverage (now ~58/74 after
   workspace backfill).
3. **2026-05-25** ingest | mod-principia + skill cross-refs — 4 pages.

### Active pages

- `.agents/skills/llm-wiki/SKILL.md`
- `docs/wiki/{index,log,hot,overview}.md`
- `docs/phase3/trappist-1-{b,c,d,e,f,g,h}.md` (entity)
- `docs/phase3/{alpha-centauri-a,alpha-centauri-b,proxima-cen,proxima-cen-b,proxima-cen-d}.md` (entity)
- `docs/reference/{methodology,adding_stars,binary-epoch-pipeline,data-sources,archive_issues,tools,mod-reference,mod-release-layout,guideline,rex-data-comparison}.md` (concept + synthesis)
- `plans/stellarium-binary-orbit-comparison.md` (synthesis)
