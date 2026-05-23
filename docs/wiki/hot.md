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

LLM Wiki bootstrap (Phase 1 of 3). Skill defined; `docs/wiki/` scaffold
created; Phase 2 bootstrap (frontmatter + `## Related` sections) and
Phase 3 trigger automation pending.

### Open questions

- Trigger channel for `/wiki lint` schedule: on-demand only, weekly cron,
  or weekly + pre-commit hook? User confirmation pending.
- First Phase 2 dry-run cluster: TRAPPIST-1 system (8 entity pages) is
  the proposed start.

### Recent decisions

- Wiki agent CAN read+write inside local-only skill workspaces
  (`scatterer-cfg`, future `eve-cfg`, `volumetrics-cfg`,
  `raymarched-*`). Output stays in those gitignored paths.
- Public wiki may reference local-only skills by *existence* (path),
  not by *content* (EA-derived field names).
- Lint enforces public-tier EA-identifier blocklist (see skill §9).
- `_papers/`, `db/`, `phase2/`, `phase3/` are raw tier — wiki never
  writes there.

### Last 3 log entries

1. **2026-05-24** initialize | wiki scaffold created — skill +
   `docs/wiki/{index,log,hot,overview}.md`. Bootstrap pending.

### Active pages

- `.agents/skills/llm-wiki/SKILL.md` (created)
- `docs/wiki/index.md` (created, bootstrap partial)
- `docs/wiki/log.md` (created, 1 entry)
- `docs/wiki/hot.md` (this file)
- `docs/wiki/overview.md` (created, sketch)
