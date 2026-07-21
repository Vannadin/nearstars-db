# Doc-flow linking - checklist

Goal: make the document set navigable as one pipeline. Three link axes:
vertical spine (DB -> Phase 2 -> Phase 3 -> Phase 4, both ways), lateral
(body <-> body, methodology <-> methodology), cross-domain (phase <-> methodology,
phase <-> wiki, colors <-> phase). Most links are builder-generated (deterministic
by slug match), so the 80 phase-3 docs are not hand-edited.

## Builders (vertical spine)
- [ ] build_html.py (Phase 3 render): fix `.md`->`.html` href rewrite
      (siblings -> `X.html`; reference -> `../wiki/reference__X.html`;
      plans -> `../wiki/plans__X.html`). Keep anchors.
- [ ] build_html.py: crumb gains Methodology + forward "Phase 4 board" link
      (emit only when `docs/phase4/*/<slug>.html` exists).
- [ ] build_phase4_html.py: body crumb gains back-link to Phase 3 synthesis
      (emit only when `docs/phase3/<body_slug>.md` exists) + Methodology link.
- [ ] build_phase4_html.py: index crumb -> full spine (DB · Reports · Methodology).
- [ ] build_reports_index.py: add Phase 4 column (scan `docs/phase4/*/`, skip
      orbit-viewers); crumb gains Methodology (methodology-index) link.

## Lateral (body-to-body) - backfill only
- [ ] `## Related` in the 4 phase-3 docs missing it (en + ko):
      luhman-16-a, luhman-16-b, psr-j0108-1431, v1400-centauri.

## Cross-domain
- [ ] methodology docs `## Related`: make sibling links clickable + add a
      clickable back-link to methodology-index. Fix the inconsistent ones
      (rocky-dynamo plain-text index, tidal-heating backtick+no index,
      surface-color backtick+no index; audit the rest).
- [ ] color-materials.md: add a `## Related` section (+ ko).
- [ ] element-plasma-colors.md: `## Related` -> link the live firefly-colors viewer (+ ko).
- [ ] (DEFERRED) firefly-colors.html <- element-plasma doc: needs
      render_color_visualizer.py, which has uncommitted parallel-session work
      (copy-hex feature). Do NOT touch this turn.

## Verify
- [ ] rebuild all three surfaces; `./scripts/check.sh` green (dead-link gate).
- [ ] spot-check a rendered Phase 3 page: sibling + reference links resolve to
      `.html`, Phase 4 forward link present where a board exists.
- [ ] spot-check a Phase 4 body page: Phase 3 back-link present where a synthesis exists.
- [ ] reports.html shows P2 -> P3 -> P4 chain.
- [ ] check-mirrors.sh: ko parity for the edited .md docs.
