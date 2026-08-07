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
