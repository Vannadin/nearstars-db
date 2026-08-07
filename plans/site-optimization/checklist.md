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
- [ ] marked.min.js + github-markdown-light.css (wiki 58p) — best ratio
- [ ] plotly.min.js (orbit viewers 16p)
- [ ] three.js module + OrbitControls (starmap)
- [ ] Google fonts (phase4 30p + starmap) → vendored woff2 or system fallback

## D. i18n stragglers
- [ ] belt-viewer.html toggle (generator)
- [ ] orbit3d.html ×6 toggle (build_viewers.py)

## Verify (every step)
- [ ] `python3 scripts/build_sitemap.py` regenerated after each structure change
- [ ] `./scripts/check.sh` green
- [ ] browser smoke on one page per changed generator
