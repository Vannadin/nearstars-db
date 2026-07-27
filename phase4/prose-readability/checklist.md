# Phase 4 prose-readability pass — checklist

Applying the SPEC §3.1 prose readability contract to every decision row in
`phase4/alpha_centauri.yaml`, one body at a time, one row at a time.

## Bodies

- [x] Pandora (committed)
- [x] Polyphemus / Alpha Centauri A b (committed)
- [x] Dante (committed)
- [x] Hades (committed)
- [x] Cassandra (committed)
- [ ] Chaos
- [ ] Alpha Cen A (star)
- [ ] Alpha Cen B (star)

## Hades rows — all 9 done

- [x] identity
- [x] bulk
- [x] magnetism.magnetic_field
- [x] bulk.tidal_heating (nominal-vs-realized nuance adopted)
- [x] surface
- [x] appearance
- [x] atmosphere
- [x] environment.radiation (now quotes ~7,200 rem/day)
- [x] gameplay

Next body: **Chaos**.

## Per-body closeout (do NOT skip)

1. Rewrite each row; show before→after (Korean version alone is fine); wait for user OK.
2. NEVER commit before showing the user the diffs.
3. When all rows of a body are confirmed:
   - `python phase4/check_phase4_gate.py` (expect 0 errors; "no refs[]" warnings are OK)
   - `python phase4/build_phase4_html.py alpha_centauri`
   - commit (English subject+body, identity VaNnadin <vannadin00@gmail.com>)
