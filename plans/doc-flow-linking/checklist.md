# Doc-flow linking - checklist

Goal: make the document set navigable as one pipeline. Three link axes:
vertical spine (DB -> Phase 2 -> Phase 3 -> Phase 4, both ways), lateral
(body <-> body, methodology <-> methodology), cross-domain (phase <-> methodology,
phase <-> wiki, colors <-> phase). Most links are builder-generated (deterministic
by slug match), so the 80 phase-3 docs are not hand-edited.

## Builders (vertical spine) — DONE (commit 29618f8)
- [x] build_html.py (Phase 3 render): fix `.md`->`.html` href rewrite
      (siblings -> `X.html`; reference -> `../wiki/reference__X.html`;
      plans -> `../wiki/plans__X.html`). Keep anchors.
- [x] build_html.py: crumb gains Methodology + forward "Phase 4 board" link
      (emit only when `docs/phase4/*/<slug>.html` exists).
- [x] build_phase4_html.py: body crumb gains back-link to Phase 3 synthesis
      (emit only when `docs/phase3/<body_slug>.md` exists) + Methodology link.
- [x] build_phase4_html.py: index crumb -> full spine (DB · Reports · Methodology).
- [x] build_reports_index.py: add Phase 4 column (scan `docs/phase4/*/`, skip
      orbit-viewers); crumb gains Methodology (methodology-index) link.
- [x] doc-hub was stale (missing rocky-planet-dynamo page) — rebuilt (commit 5f10973).

## Lateral (body-to-body) - backfill only — DONE (commit e56ae31)
- [x] `## Related` in the 4 phase-3 docs missing it (en + ko):
      luhman-16-a, luhman-16-b, psr-j0108-1431, v1400-centauri.

## Cross-domain — DONE (commit 3146679)
- [x] methodology docs `## Related`: sibling links clickable + clickable
      back-link to methodology-index (14 recipe docs + color-materials, en+ko).
- [x] color-materials.md: `## Related` added (+ ko).
- [x] element-plasma-colors.md: `## Related` -> live firefly-colors viewer (+ ko;
      ko path is repo-root-relative `../../../docs/firefly-colors.html` since the
      viewer has no ko mirror — matches AGENTS.md 2.1).
- [ ] (DEFERRED) firefly-colors.html <- element-plasma doc: render_color_visualizer.py
      is owned by the parallel color-viewer session (committed as 6c89884/d207768).
      One-directional link only this turn.
- [ ] (DEFERRED) planetary-magnetosphere-geometry-methodology.md Related: parallel
      session actively developing it on main (6c83894); left its source untouched,
      only committed its generated hub page. Normalize on a future clean pass.

## Verify — DONE
- [x] all three surfaces rebuilt; dead-link gate green (580 md files).
- [x] internal .html targets resolve: phase3 1074, phase4 201, wiki 2754, 0 missing.
- [x] Phase 3 page: sibling/reference links resolve to `.html`; Phase 4 forward
      link present where a board exists (alpha-centauri-a yes, trappist-1-e no).
- [x] Phase 4 body page: Phase 3 back-link present where synthesis exists
      (alpha-centauri-a yes, pandora/art-name no).
- [x] reports.html shows P2 -> P3 -> P4 chain (40 Eri A: P2 + P3 ★/b/c/d + P4 ★/b/c/d).
- [x] check-mirrors.sh: no edited doc flagged stale (ko parity holds).

## Not done (out of scope by owner choice)
- Full-roster sibling standardization across all 80 phase-3 docs (owner: backfill 4 only).
- In-content body-to-body prose flow (owner scoped body-to-body to Related backfill).
- gate-9 empty-dir FAIL (phase3/stability-sim/.venv/include) is a pre-existing venv
  artifact, unrelated to this work.
