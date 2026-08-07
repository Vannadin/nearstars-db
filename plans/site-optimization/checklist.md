# Site optimization — checklist

Goal: make the 270-page published surface navigable as one site. Owner-approved
order (2026-08-07): A → structure 1–4 → B → D. C (page diet) is a separate
session. Wiki decision: nav points at the LOCAL render (`wiki/index.html`);
GitHub wiki demoted to a secondary link.

## A. Regression gate
- [ ] check.sh gate 11 = `build_sitemap.py --audit-only` (new orphans fail loud)

## 1. Unified global nav — `DB · 3D Map · Reports · Phase 4 · Tools · Wiki`
- [ ] Canonical nav module (single source; generators render it with a prefix)
- [ ] `docs/index.html` (static, hand-edit)
- [ ] `build_reports_index.py` (reports.html)
- [ ] `build_docs.py` (wiki 58p)
- [ ] `render_color_visualizer.py` (firefly-colors)
- [ ] `starmap_template.html`
- [ ] `build_phase4_html.py` (system index + body pages keep contextual crumb, gain global nav on index)
- [ ] `docs/ice-stability.html` (static, hand-edit)
- [ ] `build_belt_viewer.py`
- [ ] Tighten `BASELINE_ORPHANS` after wiring

## 2. Back-crumbs on orbit viewers + validation (16 dead ends)
- [ ] `phase3/stability-sim/scripts/build_viewers.py` injects `← board · system · home`
- [ ] validation 4 pages (moon/planets leapfrog/megno) get the same crumb

## 3. Tools index
- [ ] `docs/tools.html`: belt-viewer, ice-stability, firefly-colors, starmap,
      alpha-cen validation set; KO/EN toggle, EN default

## 4. reports.html viewer pill
- [ ] `build_reports_index.py`: `3D` pill when `docs/phase4/orbit-viewers/<slug>/` exists

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
