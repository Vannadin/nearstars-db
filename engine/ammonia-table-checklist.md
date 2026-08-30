# Checklist: the ammonia table (C4 reopened for ammonia)

- [x] Bethkenhagen, French & Redmer 2013 read from the cached PDF; first page "J. Chem. Phys. 138, 234504 (2013)"; bibcode checked by title; labels say *2013* wherever the 2017 paper could be confused with it
- [x] Appendix B Table I is the distribution — no repository, no data-availability statement, no fit (grep of the full text)
- [x] `tools/make_ammonia_table.py` parses the text layer (`pdftotext -layout`): 93 rows, 11 isotherms, 9 densities, the six absent cold-dense cells absent, ten asterisks — each a hard stop
- [x] `test_ammonia.py` re-checks eight rows read from the rendered page by eye, the five flagged rows, counts, ragged edge, monotonicity
- [x] convention chosen and stated: u includes the vibrational correction (2013 Appendix B / Fig. 7) — the set 2017 §II.4 removed it from; `U_INCLUDES_VIBRATIONAL_CORRECTION` asserted; p_vc caveat quoted
- [x] flags carried: per-row flag, `uncertainty()` 5 % / 2 %, exposed on the material
- [x] ragged grid honoured: domain = intersection of bracketing isotherms; no interpolation across absent cells; refusals name the table (T both sides, ragged P edge)
- [x] interpolation error measured leave-one-out (whole grid 17.3 %, mantle region 6.4 %, at doubled spacing) and written into the module; log-log in T tried and rejected
- [x] `eos.Ammonia` (`nh3`) in the `HotWater` shape, registered; c_P / ∇_ad finite and positive at the mantle points
- [x] the check: water (Mazevet+ 2019) + ammonia at the same (P, T), additive volume at w_NH₃ = 0.1159 — water overestimates the pair's density by 2.9–3.5 % (composition tier, ammonia share; above the propagated noise); thermal columns reported without a sign
- [x] C4 row: reopened for ammonia, dated, reason recorded; closed again for that half; methane text untouched; three-tier statement unchanged, tier numbers added for the ammonia share only
- [x] `eos.py` AVL comment ("no consumer — no ammonia") rewritten to the current condition
- [x] materials table row, mixing section, hot-water tiers paragraph, citation — EN and KO
- [x] methane half re-stated from Sherman+ 2012 (PDF + LaTeX source in the cache; 79 rows counted; coverage table in the row): a table exists and is distributed, methane does not persist as a species in the region (Sherman; Bethkenhagen+ 2017 §III), grid does not cover it (2017 §II.3) — **not baked**
- [x] `tools/methane_thresholds.py`: the solved Uranus/Neptune mantles measured against the C–C (1100 K · 10 GPa), diamond (3000 K) and polymeric (4000–5000 K) thresholds — all crossed; numbers in the row and notes, no judgment
- [x] no new runtime dependency; `check.sh` gains `test_ammonia.py` (< 1 s)
- [x] anchors bit-identical (no path function touched; `test_ice_giant.py --fast` and the full gate in the log); gate FAIL 0; report to nearstars-cb
