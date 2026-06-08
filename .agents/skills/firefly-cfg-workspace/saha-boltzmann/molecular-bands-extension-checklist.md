<!-- Task checklist: molecular band-DB extension + temperature-slider viewer -->
# Molecular band-DB extension — checklist

## Phase A — band systems, no new atoms (Tier 1)
- [x] CN: X2Σ constants + violet B2Σ-X2Σ band system → molecular_bands.yaml
- [x] CO: X1Σ constants + Ångström B1Σ-A1Π (verified system; Cameron is UV not green)
- [~] S2 / SO: SKIPPED — S2 B-X is mostly UV (visible edge violet only); exact heads
      uncertain → no fabrication. Sulfur species (SO2/H2S/H2SO4) → atomic S/O, honest.
- [~] O2, NO: SKIPPED — Schumann-Runge/β/γ are UV-dominant; → atomic O/N, honest.
- [~] H2 Fulcher-α: SKIPPED for now (H2 → atomic H Balmer dominates anyway).
- [x] bulk plasma_temperature_colors.yaml unchanged (uses composition_bands, not select_bands)
- [x] commit

## Phase B — metal atoms via NIST (main thread; subagents can't fetch)
- [x] Ti, V, Fe, Mg: fetched NIST lines1/energy1 (neutral + first ion), cache /tmp/nist
      (Fe_I had a STALE truncated cache from 15:17 — only 360-362nm; deleted + refetched
       → 80 of 1543 visible. Lesson: verify cache freshness, not just line count.)
- [x] added to atomic_lines.yaml (build_atomic_lines.py SPECIES) → 18 species
- [x] saha_boltzmann ELEMENTS + chi (NIST recommended ionization energies)
- [x] element_temperature_colors.yaml UNCHANGED (it has its own 75-element NIST coverage,
      independent of the engine's atomic_lines.yaml set — no regression)
- [x] commit

## Phase C — metal-oxide band systems (Tier 2)
- [x] TiO γ A3Φ-X3Δ (705.4/708.9 nm red), VO C4Σ-X4Σ (574 nm yellow-green),
      FeO orange D5Δ-X5Δ (611 nm), MgO B1Σ-X1Σ (500 nm green) → molecular_bands.yaml
      Sources: TiO heads — Ti-isotope/MNRAS (arXiv 2110.01908, 1612.08298); VO C-X 0-0
      ~17400 cm-1 — ExoMol XVIII (arXiv 1609.06120); FeO orange D-X 580-626 nm —
      Odin/OSIRIS airglow (Evans 2010 GRL) + Fe LIBS; MgO B1Σ ~20000 cm-1 — ExoMol XXXII
      (arXiv 1904.12155). Ground-state constants D0/ωe/Be: Huber & Herzberg.
- [x] verified march: TiO orange-red→Ti cyan→ion; VO yellow→V violet; FeO orange→Fe violet;
      MgO green (500nm band + Mg b 518 atomic)→ion. Bulk plasma_temperature unchanged.
- [x] commit

## Phase D — molecular temperature table
- [ ] build_molecular_temperature_colors.py (each molecule = 1.0 composition over grid)
- [ ] db/refs/molecular_temperature_colors.yaml (mirror element_temperature_colors shape)
- [ ] wire reproducibility into validate_plasma_temp.py
- [ ] commit

## Phase E — viewer temperature slider
- [ ] render_color_visualizer: regime-bar → temperature slider
- [ ] applyRegime() → applyTemp(T): color .el-cell AND .mol-cell from temp tables
- [ ] cells without temp data → dimmed "no data"
- [ ] i18n: drop regime_* keys, add slider label; update intro
- [ ] rebuild docs/firefly-colors.html
- [ ] commit

## Phase F — register + verify
- [ ] tools.md (+ ko mirror): new script + YAML
- [ ] methodology-review: note molecular band extension + sources
- [ ] ./scripts/check.sh green
- [ ] commit
