---
type: workspace
title: "TRAPPIST-1 system Phase 3 — checklist"
slug: trappist-1-system-checklist
cluster: system-trappist-1
cluster_role: member
status: active
related: [[trappist-1-system-audit-pass-2026-05-22]], [[trappist-1-system-context-notes]], [[trappist-1-system-manual-paper-followup]], [[trappist-1-system-paper-count-summary]]
created: 2026-05-21
updated: 2026-05-25
tier: public
---
# TRAPPIST-1 system Phase 3 — checklist

Started 2026-05-21. d is already done as the pilot
(`docs/phase3/trappist-1-d.md`). Goal: extend full d-level synthesis
to the remaining six planets b, c, e, f, g, h.

## Stage 1 — bibliography builds (parallel)

- [x] `python3 scripts/phase3/build_bibliography.py "TRAPPIST-1 b"` — 66 papers, 35 arxiv
- [x] `python3 scripts/phase3/build_bibliography.py "TRAPPIST-1 c"` — 32 papers, 12 arxiv
- [x] `python3 scripts/phase3/build_bibliography.py "TRAPPIST-1 e"` — 64 papers, 30 arxiv
- [x] `python3 scripts/phase3/build_bibliography.py "TRAPPIST-1 f"` — 15 papers, 6 arxiv
- [x] `python3 scripts/phase3/build_bibliography.py "TRAPPIST-1 g"` — 66 papers, 52 arxiv
- [x] `python3 scripts/phase3/build_bibliography.py "TRAPPIST-1 h"` — 53 papers, 43 arxiv

## Stage 2 — arXiv text fetches (sequential per arXiv rate limit)

- [x] All 6 fetched, 0 failures (cached in docs/phase3/_papers/, gitignored)

## Stage 3 — synthesis (English markdown)

Each follows the d template: intro, Decisions table, Surface synthesis,
Atmosphere synthesis, Rotation & spin, Visual styling, Bibliography
(Read / Read — context / Read — instrument / Not read — no arXiv),
Open items.

- [x] `docs/phase3/trappist-1-b.md` — airless ultramafic bare rock (Greene 2023, Ducrot 2024/2025)
- [x] `docs/phase3/trappist-1-c.md` — thin O₂-dominated fossil atmo (Zieba 2023, Lincowski 2023)
- [x] `docs/phase3/trappist-1-e.md` — temperate aquaplanet (Glidden 2025 DREAMS, Wolf 2017)
- [x] `docs/phase3/trappist-1-f.md` — frozen ocean world (Acuña 2025, Wolf 2017)
- [x] `docs/phase3/trappist-1-g.md` — full snowball + sub-glacial ocean (Bourgeois 2024)
- [x] `docs/phase3/trappist-1-h.md` — Mars-Pluto hybrid frozen rocky (Luger 2017, Gressier 2022)

## Stage 4 — Korean mirrors

H2/H3 structure must match English source by position (build_html.py
will fail loudly otherwise).

- [x] `ko/docs/phase3/trappist-1-b.md`
- [x] `ko/docs/phase3/trappist-1-c.md`
- [x] `ko/docs/phase3/trappist-1-e.md`
- [x] `ko/docs/phase3/trappist-1-f.md`
- [x] `ko/docs/phase3/trappist-1-g.md`
- [x] `ko/docs/phase3/trappist-1-h.md`

## Stage 5 — HTML + report index

- [x] `python3 scripts/phase3/build_html.py trappist-1-{b,c,e,f,g,h}` ×6 — all built clean
- [x] `python3 scripts/pipeline/build_reports_index.py` — 7 P3 reports listed
- [x] `bash scripts/check-mirrors.sh` — 23/23 mirrors OK
- [x] `docs/reports-manifest.json` shows P3 chips for all 7 TRAPPIST-1 planets

## Stage 6 — commit

- [ ] `git add` the 6 .md, 6 ko/.md, 6 _bib/.yaml, 6 .html, docs/reports*.html docs/reports*.json
- [ ] Commit: "Phase 3 synthesis for TRAPPIST-1 b/c/e/f/g/h"

## Related

- [audit-pass-2026-05-22](audit-pass-2026-05-22.md) — sibling workspace doc in `trappist-1-system/`
- [context-notes](context-notes.md) — sibling workspace doc in `trappist-1-system/`
- [manual-paper-followup](manual-paper-followup.md) — sibling workspace doc in `trappist-1-system/`
- [paper-count-summary](paper-count-summary.md) — sibling workspace doc in `trappist-1-system/`
- [system-trappist-1 entity pages](../../docs/phase3/trappist-1-e.md) — parent topic this workspace contributes to
