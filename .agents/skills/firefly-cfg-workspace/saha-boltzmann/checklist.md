<!-- Saha/Boltzmann LTE 발광색 엔진 작업 체크리스트 -->
# Checklist — Saha/Boltzmann LTE plasma-emission color

Started 2026-06-08. See [plan](plan.md).

## Stage 1 — Engine + CIE refactor
- [x] Extract `scripts/refs/cie_color.py` — Planck, CMF, xyz→srgb_hue,
  blackbody_srgb, spectrum_to_hex. Verified == old builder (8 temps).
- [~] Repoint `build_plasma_temperature_colors.py` — DEFERRED to Stage 4 rewrite
  (it gets replaced there; editing now is churn). cie_color verified independently.
- [x] `scripts/refs/saha_boltzmann.py`: partition_fn, saha (n_e bisection),
  boltzmann pops, line opacity (f from A_ki), gray continuum, slab I(λ).
  [ ] dissociation equilibrium + molecular bands → Stage 3
- [x] Self-tests: slab@1500K == blackbody hex; isolated 550nm ⇒ green;
  ionization fractions physical

## Stage 2 — Atomic data (DONE — fetched in main thread, subagents denied net)
- [x] `db/refs/atomic_lines.yaml` schema + 8 species from NIST ASD
- [x] H I, He I, C I/II, N I/II, O I/II — strong visible lines, A_ki, E levels
- [x] Anchors verified: Hα 6.47e7, O I 777 triplet 3.69e7, He D3 587.6/7.07e7,
  C II 426.7/2.34e8, ionization energies, ground terms

## Stage 3 — Molecular band data (delegate → verify)
- [ ] `db/refs/molecular_bands.yaml` schema: system → {species, band_heads_nm,
  T_e_cm, eff_strength, dissociation_eV, note}
- [ ] N₂ 1P + 2P, N₂⁺ 1NG, CN violet, C₂ Swan, CH (431nm), NH (336nm), OH (306nm), H₂
- [ ] Verify: CN violet head 388.3; C₂ Swan 516.5; N₂⁺ 1NG 391.4;
  D(N₂)=9.79eV, D(O₂)=5.12eV, D(H₂)=4.48eV, D(CO)=11.16eV

## Stage 4 — Wire compositions
- [ ] Composition → constituent species map (air→N,O; co2→C,O(+CO,CN,C2);
  h2_he→H,He; ch4→C,H(+CH,C2,CN); h2o→H,O(+OH); nh3→N,H(+NH))
- [ ] Replace `build()` per-composition loop to call `slab_spectrum(T)`
- [ ] YAML: keep `combined_hex`/`rgb`/`temp_k`; add `ionization_fraction`,
  `molecular_fraction`, `tau_peak`, `dominant_species`; drop `emission_weight`
- [ ] `_blackbody` table unchanged (still exact)
- [ ] `--sanity` prints physically sensible march per composition

## Stage 5 — Render + validate + verify
- [ ] `render_color_visualizer.py`: tooltip uses new diagnostics; caption +
  i18n (en/ko) state the LTE-slab assumption list (drop "not ab-initio")
- [ ] `scripts/refs/validate_plasma_temp.py`: hex format, grid completeness,
  build reproducibility, fractions ∈ [0,1]
- [ ] Wire validate into `scripts/check.sh`
- [ ] Regenerate `docs/firefly-colors.html`
- [ ] Verify rendered colors vs anchors + existing curated reentry hexes
  (air→blue-violet, co2→green/violet, h2_he→pink-red; sanity, not equality)
- [ ] `./scripts/check.sh` clean

## Stage 6 — Docs + commit
- [ ] YAML header + script docstrings rewritten (assumption list)
- [ ] `docs/reference/tools.md` (+ ko) — register new scripts/DBs
- [ ] context-notes appended with all derivations + decisions
- [ ] Semantic commit per stage

## Related
- [plan](plan.md) · [context-notes](context-notes.md)
