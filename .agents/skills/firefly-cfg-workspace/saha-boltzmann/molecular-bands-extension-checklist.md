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
- [ ] Ti, V, Fe, Mg: fetch NIST lines1/energy1 (neutral + first ion), cache /tmp/nist
- [ ] add to atomic_lines.yaml (build_atomic_lines.py species list)
- [ ] saha_boltzmann ELEMENTS + ionization energies (chi)
- [ ] commit

## Phase C — metal-oxide band systems (Tier 2)
- [ ] TiO (red), VO (orange-red), FeO (orange), MgO (green) → molecular_bands.yaml
- [ ] verify low-T molecular color → high-T dissociation→atomic march per oxide
- [ ] commit

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
