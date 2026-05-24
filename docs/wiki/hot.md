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

LLM Wiki bootstrap Phase 2 in progress. Two entity clusters ingested
(system-trappist-1 + system-alpha-cen = 12 pages). Remaining
candidates: docs/reference concept hub (~10 pages, different
workflow — type=concept instead of type=entity), `plans/*` syntheses,
and the per-system workspaces in phase3/.

### Open questions

- Next ingest: docs/reference concept cluster (methodology hub + 8
  members), or remaining phase3 systems (none with `.md` entity
  pages exist yet beyond TRAPPIST-1 + α Cen — synthesis hasn't
  reached other systems)? Likely concept cluster next.
- Trigger channel for `/wiki lint` schedule (A/B/C from skill §8) —
  user confirmation still pending.
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

1. **2026-05-24** ingest | system-alpha-cen cluster — 5 entity pages
   (3 stars + 2 planets), cross-cluster link to TRAPPIST-1 e added.
2. **2026-05-24** ingest | system-trappist-1 cluster — 7 entity pages.
3. **2026-05-24** initialize | wiki scaffold created.

### Active pages

- `.agents/skills/llm-wiki/SKILL.md`
- `docs/wiki/{index,log,hot,overview}.md`
- `docs/phase3/trappist-1-{b,c,d,e,f,g,h}.md` (frontmatter + Related)
- `docs/phase3/{alpha-centauri-a,alpha-centauri-b,proxima-cen,proxima-cen-b,proxima-cen-d}.md` (frontmatter + Related)
