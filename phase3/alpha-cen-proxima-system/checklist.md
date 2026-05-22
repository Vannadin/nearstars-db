<!-- Alpha Cen A/B + Proxima Cen + planets Phase 3 synthesis — task tracker -->
# Alpha Centauri (A, B) + Proxima Cen + planets — Phase 3 Checklist

Started 2026-05-22. Five synthesis documents:
- Alpha Cen A (G2V star) — focus: stellar disk visual, color temp, surface granulation, activity
- Alpha Cen B (K1V star) — focus: stellar disk visual, color temp, AB pair geometry from each star's frame
- Proxima Cen (M5.5V flare star) — focus: stellar disk, flare visuals, B-field structure
- Proxima Cen b (HZ-edge terrestrial) — focus: surface + atmosphere visual, polar regions, JWST constraints
- Proxima Cen d (sub-Earth-mass hot rock) — focus: surface visual, magma plausibility, weak atmo

Follows TRAPPIST-1 d template depth: ~350-400 lines each + Korean mirror.

## Stage 1 — bibliography builds (parallel)

- [x] `python3 scripts/phase3/build_bibliography.py "Alpha Centauri A"` — bg bf5fdzq2o
- [x] `python3 scripts/phase3/build_bibliography.py "Alpha Centauri B"` — bg bplf755ah
- [x] `python3 scripts/phase3/build_bibliography.py "Proxima Cen"` — bg be54jux4s
- [x] `python3 scripts/phase3/build_bibliography.py "Proxima Cen b"` — bg bp66r2bf9
- [x] `python3 scripts/phase3/build_bibliography.py "Proxima Cen d"` — bg b2x0igm16

## Stage 2 — arXiv text fetches (sequential per arXiv rate limit)

- [ ] alpha-centauri-a
- [ ] alpha-centauri-b
- [ ] proxima-cen
- [ ] proxima-cen-b
- [ ] proxima-cen-d

## Stage 3 — synthesis (English markdown)

- [ ] `docs/phase3/alpha-centauri-a.md`
- [ ] `docs/phase3/alpha-centauri-b.md`
- [ ] `docs/phase3/proxima-cen.md`
- [ ] `docs/phase3/proxima-cen-b.md`
- [ ] `docs/phase3/proxima-cen-d.md`

## Stage 4 — Korean mirrors

H2/H3 structure must match English source by position.

- [ ] `ko/docs/phase3/alpha-centauri-a.md`
- [ ] `ko/docs/phase3/alpha-centauri-b.md`
- [ ] `ko/docs/phase3/proxima-cen.md`
- [ ] `ko/docs/phase3/proxima-cen-b.md`
- [ ] `ko/docs/phase3/proxima-cen-d.md`

## Stage 5 — HTML + report index

- [ ] `python3 scripts/phase3/build_html.py alpha-centauri-{a,b}`
- [ ] `python3 scripts/phase3/build_html.py proxima-cen{,-b,-d}`
- [ ] `python3 scripts/pipeline/build_reports_index.py`
- [ ] `bash scripts/check-mirrors.sh`
- [ ] Visual browser check

## Stage 6 — commit

- [ ] `git add` synthesis files + bibs + HTML
- [ ] Commit: "Phase 3 synthesis for Alpha Cen A/B + Proxima Cen system"
