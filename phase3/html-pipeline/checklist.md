<!-- Phase 3 web report pipeline — turning DB / synthesis markdown into a unified docs/ website -->
# Phase 3 web report pipeline — checklist

Started 2026-05-21. Goal: make `docs/` a coherent website where Phase 2
and Phase 3 reports are generated automatically from the DB / synthesis
markdown, with shared styling and a bilingual ko/en toggle.

## Stage 1 — common CSS extraction ✓

- [x] Inventory current `<style>` blocks in `docs/index.html`,
  `docs/phase2-trappist-1.html`, `docs/phase3-trappist-1-d.html`
- [x] Identify the shared subset (header, card, table, dark-theme tokens)
- [x] Write `docs/style.css` with the shared rules
- [x] Refactor each HTML page to `<link rel="stylesheet" href="style.css">` + keep page-specific rules inline
- [x] Verify localhost serves all 4 files with 200; visual eyeball check pending in browser

## Stage 2 — bilingual markdown retrofit

- [ ] Define grammar reference at `docs/reference/bilingual-markdown.md`
  (or in this checklist's context-notes)
- [ ] Retrofit `docs/phase3/trappist-1-d.md` to bilingual using the
  agreed syntax: heading `|`, paragraph `[en]/[ko]` blocks,
  table `(한국어)` columns, list `{{ko: ...}}` inline
- [ ] Verify the file still validates as markdown (renders in any standard viewer)

## Stage 3 — Phase 3 HTML generator

- [ ] `scripts/phase3/build_html.py <planet_slug>` skeleton
- [ ] Bilingual markdown parser — heading splitter, [en]/[ko] block splitter,
  table column pairing, list inline parser
- [ ] Generate `T = {ko: {...}, en: {...}}` JS table, embed in HTML
- [ ] Lang-toggle JS: `data-i18n="..."` swap on button click
- [ ] Emit `docs/phase3/<slug>.html` matching existing visual style
- [ ] Test: regenerate `phase3-trappist-1-d.html` and diff against current Korean page —
  output should preserve or improve coverage
- [ ] Replace current `docs/phase3-trappist-1-d.html` with the generated version
  (note: filename moves to `docs/phase3/trappist-1-d.html` per new layout)

## Stage 4 — Phase 2 generator

- [ ] `scripts/pipeline/build_phase2_html.py` scans
  `db/stellar_props_curated.json` + `db/planets_curated.json` for hosts
  with array-form measurements (= Phase 2 hosts)
- [ ] For each such host, emit `docs/phase2/<host_slug>.html`
- [ ] Reuse the same DB-fetching JS from the existing
  `phase2-trappist-1.html` but parameterize the host name
- [ ] Migrate existing `docs/phase2-trappist-1.html` to the new path
- [ ] Test: regenerate, verify no regression vs existing page

## Stage 5 — reports.html index

- [ ] `scripts/pipeline/build_reports_index.py` scans
  `docs/phase2/*.html` and `docs/phase3/*.html`
- [ ] Emit `docs/reports.html` — table of (system / planet, Phase 2 link,
  Phase 3 link, last-updated date)
- [ ] Bilingual (uses the same `T = {ko, en}` pattern)

## Stage 6 — index.html DB integration

- [ ] In the DB row detail panel, check existence of
  `phase2/<host_slug>.html` and `phase3/<planet_slug>.html`
- [ ] Render "Phase 2 보고서" / "Phase 3 보고서" buttons when files exist
- [ ] Mobile: same buttons in the card detail
- [ ] Test: TRAPPIST-1 row should show both Phase 2 and Phase 3 (planet d) buttons

## Verification across stages

- [ ] All four pages (`index.html`, `phase2/<host>.html`, `phase3/<planet>.html`,
  `reports.html`) share the same dark theme via `style.css`
- [ ] Lang toggle (한/EN) is consistent across all four pages
- [ ] Regenerating a Phase 3 page from updated markdown does not require
  HTML hand-editing
- [ ] Adding a new Phase 2 host (e.g. via `add-star` skill upgrade) does not
  require manual HTML

## Out of scope (future work)

- LLM-driven translation when only English markdown exists (deferred)
- Search across all Phase 2/3 reports
- Renderer for `_papers/*.md` (raw paper texts) — those stay as cache
- PR/changelog of Phase 3 syntheses (manual review still required)
