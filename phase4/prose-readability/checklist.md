# Phase 4 prose-readability pass — checklist

Applying the SPEC §3.1 prose readability contract to every decision row in
`phase4/alpha_centauri.yaml`, one body at a time, one row at a time.

## Bodies

- [x] Pandora (committed)
- [x] Polyphemus / Alpha Centauri A b (committed)
- [x] Dante (committed)
- [ ] Hades — IN PROGRESS, uncommitted. 4/9 rows rewritten, 5 rows pending.
- [ ] Cassandra
- [ ] Chaos
- [ ] Alpha Cen A (star)
- [ ] Alpha Cen B (star)

## Hades rows (line numbers as of last edit)

- [x] identity (1620)
- [x] bulk (1644)
- [x] magnetism.magnetic_field (1674)
- [x] bulk.tidal_heating (1691) — DONE, but one open question (see context-notes)
- [ ] surface (1711)
- [ ] appearance (1743)
- [ ] atmosphere (1757)
- [ ] environment.radiation (1766)
- [ ] gameplay (1780)

## Per-body closeout (do NOT skip)

1. Rewrite each row; show before→after (Korean version alone is fine); wait for user OK.
2. NEVER commit before showing the user the diffs.
3. When all rows of a body are confirmed:
   - `python phase4/check_phase4_gate.py` (expect 0 errors; "no refs[]" warnings are OK)
   - `python phase4/build_phase4_html.py alpha_centauri`
   - commit (English subject+body, identity VaNnadin <vannadin00@gmail.com>)
