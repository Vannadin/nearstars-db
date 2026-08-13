# Wiki consolidation — one published surface (Pages), wiki reduced to a front door

Owner decision 2026-08-13: unify on Pages (`docs/`), keep the GitHub-repo wiki as a
front door of stubs so inbound links survive.

## Stage 1 — a home on Pages for the wiki's reader-facing pages
- [x] `docs/guide/*.md` (+ `ko/docs/guide/`) as a new source dir: overview, installation,
      faq, star-systems, viewers, showcase
- [x] `build_docs.py` gains the `guide` group (first in the sidebar), `guide__<slug>.html`
- [x] Freshness gate covers the new dir (it globs docs/guide via the same rule)

## Stage 2 — Radiation-Belts (the one substantial wiki page)
- [x] Cross-section PNGs → `docs/img/belts/`
- [x] Fold the gallery into `docs/reference/solar-system-radiation-belts.md` + ko mirror
      (same subject, same per-body structure, already carries the citations)

## Stage 3 — retire the third registration surface
- [x] Gate 12 (`check_methodology_coverage.py`) drops the wiki portal check → no network
      dependency, registration goes from three places to two
- [x] `nearstars-methodology` skill registration checklist updated. **Only the NearStars
      copy exists on this machine** — the warpfx duplicate is not on disk here, so it still
      carries the retired three-surface rule and must be synced wherever that repo lives
- [x] tools.md + ko mirror updated; CONVENTIONS carries no wiki-portal rule

## Stage 4 — the front door
- [x] Wiki `Home` + `_Sidebar` → link map into Pages
- [x] Every other wiki page → one-line "moved →" stub (EN + ko)
- [x] `README.md` + `ko/README.md` point at Pages first
- [x] Sidebar's cross-link now points at the repository, not the stubbed wiki

## Verification
- [x] `./scripts/check.sh` green (mirror parity, dead links, sitemap orphans, gate 12)
- [x] sitemap audit: 279 pages, 0 new orphans
- [x] Every wiki stub resolves to a live Pages URL (all 8 guide/reference targets plus the
      belt images return 200 after the 2026-08-13 deploy)
