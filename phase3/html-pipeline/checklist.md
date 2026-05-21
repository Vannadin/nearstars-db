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

## Stage 2 — Korean mirror for synthesis ✓ (already exists upstream)

Policy: AGENTS.md §2.1 — English at canonical path, Korean at
`ko/<same-path>`. Supersedes earlier bilingual-in-one-file plan.

- [x] `ko/docs/phase3/trappist-1-d.md` exists upstream (created by
  user / parallel session). H2/H3 structure (12 headings) matches
  English source by position.
- [x] `scripts/check-mirrors.sh` reports all 17 mirrors OK.

## Stage 3 — Phase 3 HTML generator ✓

- [x] `scripts/phase3/build_html.py <planet_slug>` skeleton
- [x] Markdown parser — H2/H3 sections, paragraph blocks, tables, lists (incl. indented continuations), code fences
- [x] Pair English source with `ko/` mirror by block order; fail loudly on count/kind mismatch
- [x] Generate `T = {en: {...}, ko: {...}}` JS table from paired sections (198 keys for trappist-1-d)
- [x] Lang-toggle JS: `data-i18n` swap + localStorage persistence, mirror `index.html` UX
- [x] Emit `docs/phase3/<slug>.html` matching existing visual style (44.6 KB output)
- [x] Run on trappist-1-d — 41 paired blocks, no errors
- [x] Remove old `docs/phase3-trappist-1-d.html` flat-path file
- [x] Update `docs/index.html` howto link to new subdirectory path

## Stage 4 — Phase 2 generator ✓

- [x] `scripts/pipeline/build_phase2_html.py` scans
  `db/stellar_props_curated.json` for hosts with any of the 6 new
  measurement categories (= true Phase 2 curation, vs Phase 1 auto-fill)
- [x] For each such host, emit `docs/phase2/<host_slug>.html`
- [x] Reused the existing DB-fetching JS but generalized for all 8
  measurement categories + parameterized host name + json filename
- [x] Removed legacy `docs/phase2-trappist-1.html`
- [x] Run: emits `docs/phase2/trappist-1.html` for TRAPPIST-1 (only
  current Phase 2 host). Page loads with 200 OK, 15.2 KB.
- [x] Updated README.md, ko/README.md, and docs/index.html links to
  the new subdirectory path

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
