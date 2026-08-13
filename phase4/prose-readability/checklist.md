# Phase 4 prose-readability pass — checklist

Applying the SPEC §3.1 prose readability contract to every decision row in
`phase4/alpha_centauri.yaml`, one body at a time, one row at a time.

## Bodies

- [x] Pandora (committed)
- [x] Polyphemus / Alpha Centauri A b (committed)
- [x] Dante (committed)
- [x] Hades (committed)
- [x] Cassandra (committed)
- [x] Chaos (committed)
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

Next body: **Alpha Cen A** (star), then **Alpha Cen B**.

## Chaos rows — all 9 done

identity / bulk / atmosphere / surface / appearance / magnetism / environment.radiation /
satellites / gameplay. Two axes with nothing to say (magnetism, satellites) are just `없음.`

Value fixes that fell out: albedo 0.7 → 0.91 with surface_temperature 200 → 134 K (ice
stability), the magnetopause misrecorded as Chaos's own 21 R_p instead of 23.5 R_p, canon's
15–30 km cliffs restored, and the 먹이다 calque cleared board-wide.

## Gameplay rows realigned (all 5 surfaced bodies)

New three-part shape, owner 2026-07-27 — see context-notes. Dante, Hades, Pandora,
Cassandra rewritten to match Chaos; Polyphemus was exempted then for having no surface,
and was brought into the same shape on 2026-08-13 (the belt structure replaced the
class-definitional "no ground to land on" opening, evidence to the 3-part form).
The old "no biome lists in prose" rule is superseded in SPEC §3.1, the skill, context-notes
and memory.

## Per-body closeout (do NOT skip)

1. Rewrite each row; show before→after (Korean version alone is fine); wait for user OK.
2. NEVER commit before showing the user the diffs.
3. When all rows of a body are confirmed:
   - `python phase4/check_phase4_gate.py` (expect 0 errors; "no refs[]" warnings are OK)
   - `python phase4/build_phase4_html.py alpha_centauri`
   - commit (English subject+body, identity VaNnadin <vannadin00@gmail.com>)
