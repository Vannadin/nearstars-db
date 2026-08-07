# Site optimization — context notes

- 2026-08-07: Owner approved the 3-tier IA (home → 5 hubs → leaves) with two
  flow axes (per-body pipeline via reports.html; per-topic via Tools/Wiki),
  order A → 1–4 → B → D, C deferred to its own session. Wiki decision: local
  render becomes the nav target, GitHub wiki secondary.
- CDN dependency headcount corrected mid-plan: "68 pages" is NOT the orbit
  viewers — it is wiki 58 (marked.js + github-markdown-css) + orbit viewers 16
  (plotly) + starmap (three.js). Vendoring priority reordered accordingly:
  marked first, plotly second, three third. Fonts: phase4 boards 30p + starmap.
- Prior art: `plans/doc-flow-linking/` already wired the vertical spine
  (P2↔P3↔P4 crumbs, reports P4 column). This pass adds the GLOBAL nav layer +
  lateral Tools hub on top; don't duplicate its per-page contextual crumbs.
- `docs/index.html` and `docs/ice-stability.html` are hand-maintained statics;
  everything else nav-bearing is generator-emitted.
- Orbit viewers are built by `phase3/stability-sim/scripts/build_viewers.py`
  (commit 9f288c3, manifest + batch driver + gallery).
- Close-out 2026-08-07: four commits — 0cdef1e (gate 11), 2c084b2 (IA rewire),
  6996003 (CDN vendoring), 5440f10 (viewer i18n). End state: 272 pages,
  orphans 0, dead ends 0, published CDN references 0, every toggle EN-default.
- Gotchas for future passes: viewer pages use implicit <head>/<body> markup, so
  crumb/asset injection falls back to `</style>`; `build_viewers` re-runs the SIM
  when the manifest is newer than a summary (run.py fails under system Python 3.9
  — re-render with animate_orbits/plot_interactive directly instead); the
  validation set (alpha-centauri-validation) is hand-maintained, not rebuilt.
- Deferred to their own sessions: C (page diet — plans/viewer-optimization.md
  remaining items + orbit-viewer payload rounding), full EN pass over the belt
  viewer's exported cfg comments if ever wanted.
