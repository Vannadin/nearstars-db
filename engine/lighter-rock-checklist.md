# Checklist: lighter rock (C10)

Plan in one line: bake Hilairet+ 2006's antigorite from the PDF (ρ₀ derived, since it is not
printed), declare one axis — how serpentinised the rock is — as a volume-additive mixture with
the silicate, re-run the three-layer band on Callisto, Titan and Enceladus across the axis, and
report the fraction that closes each or that none does.

- [x] 2006GeoRL..33.2302H (+ Capitani & Mellini 2004, Vance+ 2018) checked by title on ADS; constants read from the cached PDF
- [x] ρ₀ derived from the structural formula and the m = 1 volume (2640.5); the m = 17 and 2765-kg/m³ checks pass in `test_interior`
- [x] `antigorite` material (BM2, 10 GPa, no thermal term); `serpentinisation` on solve/shoot/integrate/_stack and `infer_three_layer`
- [x] Mixture: a part with no thermal constants passes temperature through (the pure-material rule), stated in the note
- [x] band sweep at f = 0, 0.25, 0.5, 0.75, 1 on the three moons — declared grid, no fraction chosen to close anything
- [x] result: no fraction in [0, 1] closes any of the three; recorded as pointing at C9's porosity branch
- [x] C9 discriminator kept on the rheology layer; Dante / Hades noted as owner's, tool only
- [x] anchors bit-identical at f = 0 (icy solve re-run against HEAD to the last digit); `--refresh` for the touched signatures
- [x] EOS table row, domain row, three-moon prose and cells, citations, chain.yaml, Needs — EN and KO
- [x] C10 row closed; gate FAIL 0; report
