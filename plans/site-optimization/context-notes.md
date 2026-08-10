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
- Design phase (owner-driven, same day): every surface unified on the v2
  (Phase 4 board) palette; then a two-tier header — `_nav.global_bar()` emits a
  self-contained one-line site bar (brand + DB·3D Map·Reports·Phase 4·Tools·Wiki,
  light-scheme variant behind `html.ns-light-ok`) inserted right after <body> on
  255 document pages, while page headers keep only page-specific controls
  (title, lang toggle, filters, contextual crumbs like Methodology / ← board).
  Fullscreen apps (starmap topbar, orbit3d/interactive overlay crumb) stay compact.
  Light-theme rollout to document surfaces is a proposed next step (model:
  ice-stability's paired palettes); owner has not yet decided.

## 2026-08-10 — UX/UI review pass

Ran the ui-ux-pro-max rule tables (installed globally that day) over the 272-page
surface, then fixed everything the review found.

- **Static-text audits over-count.** Grepping HTML for `<h3>` before `<h2>` flagged
  82 heading-skip pages; the DOM had 3. The other 79 were heading tags inside JS
  template strings. Same for `aria-sort` (148 flagged → 1 real sortable table).
  Audit rendered DOM, not source text.
- **`overflow-x: hidden` kills `position: sticky`.** It makes the element a scroll
  container, so a sticky `<th>` sticks to that container instead of the viewport.
  `overflow-x: clip` gives the same clipping without the scroll container.
- **The DB browser never worked from `file://`.** `fetch()` is blocked there, so the
  catalogue silently rendered as one error row. Builders now emit a classic-script
  twin (`data.js`, `reports-manifest.js`) — classic scripts load over `file://`
  where fetch and ES modules do not (same boundary as the three.js CDN decision).
- **matplotlib was not installed anywhere**; added to `phase3/stability-sim/.venv`
  for the dark-figure regeneration. The four alpha-cen validation PNGs have no
  generator in the repo, so they were re-shot headless from their own dark plotly
  pages — if they ever need regenerating, do that again rather than hunting for a script.

## 2026-08-10 (later) — light colours, measured rather than guessed

The first light pass flipped tokens by hand and left the semantic/data colours
alone. Measuring every text node's contrast against its *composited* background
(playwright walks the DOM, composites ancestor backgrounds, applies the WCAG
formula) found ~40 failures in light: the phase pills, phase4 verdict pills,
DB modal and phase2 method tags were still wearing dark-theme colours (1.5-2.4:1),
and the values I had picked were 0.2-0.7 short (3.7-4.4:1).

Method that replaced the guessing: keep the hue, binary-search lightness until
the colour clears 5.0:1 **against the background it actually sits on** — a pill
sits on its own 12% tint over a card tint over the canvas, so solving against
the bare canvas overshoots by ~1 point. Solver lives in the session scratchpad;
the resulting palette is in the light blocks.

Two findings worth keeping:
- **Spectral pills can't be darkened, they must be re-hued.** In dark they were
  separated by lightness alone (#b2c4ff / #9eb8ff / #cfdcff for O/B/A); darkening
  collapses all three to the same blue. The light set spreads them along the real
  colour-temperature sequence by hue (253° violet → 8° red).
- **Threshold-based black/white text picking is wrong.** `luminance > 0.4 ? black
  : white` on the periodic table gave 2.5:1 on mid-tone tiles. Choosing whichever
  of black/white has the higher contrast guarantees ≥4.58:1 for any colour.
