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

LLM Wiki bootstrap Phase 2 (incremental cluster ingest). system-trappist-1
done (7 entity pages, 2026-05-24). Next cluster candidates:
system-alpha-cen (5 entities), docs/reference concept hubs (10+
pages), then docs/phase3/* outside trappist-1.

### Open questions

- Next cluster to ingest: system-alpha-cen, methodology concept
  cluster, or scan-all-and-batch? User direction pending.
- Trigger channel for `/wiki lint` schedule (A/B/C from skill §8) —
  user confirmation pending.
- Host star entity page for TRAPPIST-1 (M8V) does not exist yet —
  flagged in log as ingest follow-up.

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

### Last 3 log entries

1. **2026-05-24** ingest | system-trappist-1 cluster — 7 entity pages
   (frontmatter + `## Related`), confidence range high→low.
2. **2026-05-24** initialize | wiki scaffold created — skill +
   `docs/wiki/{index,log,hot,overview}.md`.

### Active pages

- `.agents/skills/llm-wiki/SKILL.md`
- `docs/wiki/{index,log,hot,overview}.md`
- `docs/phase3/trappist-1-{b,c,d,e,f,g,h}.md` (7 entity pages,
  frontmatter + Related added 2026-05-24)
