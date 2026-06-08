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

## Stage 3 — Molecular band data (DONE — curated from Huber-Herzberg myself)
- [x] `db/refs/molecular_bands.yaml`: molecules (D0, μ, ω_e, B_e, σ, g_elec) +
  band_systems (T_e, g_upper, A_eff, heads) + composition_bands map
- [x] N₂ 1P + 2P, N₂⁺ 1NG, C₂ Swan, CH A, NH A, OH A (CN deferred — needs trace N)
- [x] dissociation equilibrium (law of mass action) in engine; N₂ curve verified

## Stage 4 — Wire compositions (DONE)
- [x] Composition → element fractions in saha_boltzmann.COMPOSITIONS; bands via
  molecular_bands.composition_bands
- [x] `build()` calls `slab_spectrum(T)`; `_blackbody` unchanged (exact)
- [x] YAML: combined_hex/rgb/temp_k + ionization_fraction/molecular_fraction/
  emission_fraction/dominant; emission_weight/continuum_hex/emission_hex dropped
- [x] `--sanity` march physically sensible (C₂ green, Balmer pink, N₂ dissoc)

## Stage 5 — Render + validate + verify (DONE)
- [x] `render_color_visualizer.py`: tooltip uses new diagnostics; caption +
  i18n (en/ko) state the LTE model + non-LTE caveat (dropped "not ab-initio")
- [x] `scripts/refs/validate_plasma_temp.py`: hex, grid completeness, fractions
  ∈ [0,1], dominant enum, build reproducibility (rebuild == bytes)
- [x] Wired into `scripts/check.sh` gate 1
- [x] Regenerated `docs/firefly-colors.html`
- [x] Verified colors physically: co2 C₂-Swan green, h2_he Balmer pink, N₂
  dissociation curve, air thermal→atomic→ionic (blue is non-LTE, documented)
- [x] `./scripts/check.sh` clean (FAIL 0)

## Stage 6 — Docs + commit (DONE)
- [x] YAML header + script docstrings state the LTE model + caveat
- [x] `docs/reference/tools.md` (+ ko) — registered cie_color, build_atomic_lines,
  atomic_lines.yaml, molecular_bands.yaml, saha_boltzmann, validate
- [x] context-notes appended (final model, calibration, non-LTE finding)
- [x] Semantic commits per stage (7a0c413 data foundation, 8663305 engine)

## Outcome
Hand-tuned w(T) blend replaced by a first-principles LTE engine. The temperature
axis now means something different per composition (computed from ionization /
excitation / dissociation), not a uniform ramp. Honest finding surfaced: air's
reentry blue is non-LTE and absent in LTE — documented divergence, Firefly cfg
keeps the observation-based curated blue.

## Related
- [plan](plan.md) · [context-notes](context-notes.md)
