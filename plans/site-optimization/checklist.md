# Site optimization — checklist

Goal: make the 270-page published surface navigable as one site. Owner-approved
order (2026-08-07): A → structure 1–4 → B → D. C (page diet) is a separate
session. Wiki decision: nav points at the LOCAL render (`wiki/index.html`);
GitHub wiki demoted to a secondary link.

## A. Regression gate
- [x] check.sh gate 11 = `build_sitemap.py --audit-only` (new orphans fail loud) — commit 0cdef1e

## 1. Unified global nav — `DB · 3D Map · Reports · Phase 4 · Tools · Wiki`
- [x] Canonical nav module `scripts/pipeline/_nav.py` (single source)
- [x] `docs/index.html` (static, hand-edit)
- [x] `build_reports_index.py` (reports.html; `__NAV__` placeholder + Methodology contextual)
- [x] `build_docs.py` (wiki 58p sidebar: 6 surfaces + GitHub wiki ↗ secondary)
- [x] `render_color_visualizer.py` (`.format()` template — GLOBAL_NAV kwarg)
- [x] `starmap_template.html` (topbar buttons)
- [x] `build_phase4_html.py` (hub crumb = global nav; body pages keep contextual crumb)
- [x] `docs/ice-stability.html` (static, hand-edit)
- [x] `belt_viewer_template.html`
- [x] `BASELINE_ORPHANS` → empty set (orphans 0, dead ends 0)

## 2. Back-crumbs on orbit viewers + validation (16 dead ends)
- [x] `build_viewers.py` `inject_crumb()` at collect time (idempotent; implicit-<body>
      pages fall back to `</style>` injection)
- [x] validation 4 charts one-off injected (they are committed artifacts, not
      rebuilt by build_viewers); validation index got a header crumb + EN default

## 3. Tools index
- [x] `docs/tools.html`: starmap, colors, belt-viewer, ice-stability, orbit-viewer
      gallery, validation set; KO/EN toggle, EN default

## 4. reports.html viewer pill
- [x] `scan_viewers()` + host-slug prefix match → `3D` pill in the System cell

## B. CDN vendoring → `docs/assets/`
- [x] marked.min.js + github-markdown-light.css (wiki 58p)
- [x] plotly.min.js (interactive 6p + validation 4p) — localized in inject_crumb
- [x] ~~three.module.js + jsm~~ REVERTED to CDN: Chromium-family browsers
      (owner's Whale included) block file:// ES-module imports by CORS, so the
      local copy broke starmap/orbit3d for local viewing. Classic scripts
      (plotly/marked) are unaffected and stay vendored.
- [x] Geist/Geist Mono woff2 ×11 + geist.css (156 KB); Noto Sans KR dropped from
      the request — Korean falls to the system stack (Apple SD Gothic / Malgun)
- [x] remaining `src/href="https://…"` count: 0

## D. i18n stragglers
- [x] belt-viewer.html: full UI dictionary (header, presets, controls, readouts,
      canvas captions, footer EN translation); preset labels get label_en from the
      builder; toggle in the preset bar, EN default; cfg-export comments stay Korean
      (tool output, not prose)
- [x] orbit3d.html ×6: HUD/controls/frame labels bilingual (label_en carried in
      DATA.frames), toggle in the control bar, EN default; node --check clean on both

## Verify (every step)
- [ ] `python3 scripts/build_sitemap.py` regenerated after each structure change
- [ ] `./scripts/check.sh` green
- [ ] browser smoke on one page per changed generator

## E. UX/UI review pass (2026-08-10)
- [x] a11y floor: focus rings, prefers-reduced-motion, AA text contrast (.46), 11px
      type floor, lang/viewport on viewer pages, aria-sort + keyboard sort, alt text
- [x] DB browser works from `file://` — `data.js` / `reports-manifest.js` classic-script
      fallbacks emitted by the builders; error state now names the fix
- [x] stability-sim PNGs render dark (`nsplot.apply_dark`); validation thumbnails
      re-shot from their own dark plotly pages (no generator exists for those four)
- [x] orbit3d back-crumb no longer overlaps the HUD (HUD top 10px → 44px)
- [x] reports.html: sticky thead + system filter with live count
      (`html,body overflow-x: clip` — `hidden` was killing sticky)
- [x] phase3 decisions table: sticky thead + field filter
- [x] phase4 body boards: axis anchor TOC (>3 decisions)
- [x] wiki sidebar grouped (Methodology / Engine & mods / Pipeline & data / Reference / Plans)
- [x] belt viewer presets grouped by row (Stock / Physical / NearStars / Demo)

## F. Light / dark theme (2026-08-10)
- [x] `docs/style.css` + `docs/style.v2.css` carry paired light palettes; the v2
      override also targets `[data-ns="v2"]`, which re-declares the tokens locally
- [x] phase4 boards, wiki shell (+ github-markdown-light swap by media), gallery,
      validation index, DB browser: light blocks, hardcoded whites tokenised
- [x] every document surface opts in with `<html class="ns-light-ok">`;
      fullscreen apps (starmap, orbit3d) stay dark by design
- [x] phase2 pages got the same file:// data fallback as the DB browser

## G. Mobile support (2026-08-10)
- [x] audit harness: playwright iPhone 13 across all 16 page types — horizontal
      overflow, tap-target size, body/label font size, JS errors
- [x] global bar: was two wrapped rows of 13px links → one scrollable row,
      44px targets, separators dropped, brand sticky, current page underlined
- [x] segment controls (한/EN, filters): 24px → 40px min target
- [x] wiki: the only page that scrolled sideways (543px). Sidebar became a 42vh
      scroll region so 59 links stop blocking the article; wide tables scroll
      inside themselves
- [x] shared stylesheet mobile block: 15px body, 14px intro, 40px form controls
      (16px font so iOS doesn't zoom), 36px table links, cards scroll wide tables
- [x] per-surface controls: starmap layer buttons + zoom + tour, ice chips,
      belt presets/sliders/mode, phase4 axis chips + crumbs + prev/next,
      phase3 crumb/filter, gallery card links, orbit3d HUD, plotly modebar
- [x] DB header: help button + language toggle share one row instead of two
- [x] 100vh → dvh fallbacks (wiki shell, ice, plotly viewers)
- [x] starmap touch hint moved below the two-tier header
- Result: horizontal overflow 0/16 pages; every *control* ≥36px. What the audit
  still flags is inline links inside running prose (phase3 61, phase2 17,
  wiki 15) — exempt by WCAG 2.5.8, and the phase2 chart-label links are
  duplicated as normal-size links in the table beneath each plot.
