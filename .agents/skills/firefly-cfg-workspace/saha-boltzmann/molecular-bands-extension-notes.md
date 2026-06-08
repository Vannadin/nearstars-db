<!-- Design log: extending the engine's molecular band DB to color the full molecular panel vs temperature -->
# Molecular band-DB extension — context notes

## Why
The viewer's periodic table is being switched from a regime toggle to a
**temperature slider** (element_temperature_colors.yaml). The molecular panel
must join the same slider. But the engine (`molecular_bands.yaml`) only models
5 parents (N2, N2+, C2, CH, NH, OH) — enough for 6 bulk reentry compositions,
NOT the 30-molecule panel. CN is explicitly excluded; metal oxides need metal
atoms not in the atomic set (H/He/C/N/O/S). So "run each molecule through the
engine" gives correct color for ~10, trivial/wrong for ~20.

Decision (user): do it **properly** — research each panel molecule's dominant
visible electronic band system (Pearse & Gaydon / Huber-Herzberg constants),
add to `molecular_bands.yaml`, add the metal atoms via NIST, then the engine
produces temperature-resolved color for all, consistent with the element table.

## Sourcing discipline (no fabrication)
Every band constant cites a source. Two trusted layers:
- **Which molecule emits where** — already sourced in our own
  `db/refs/molecular_plasma_colors.yaml` (basis + source per molecule). hex set
  = real visible emitter; hex=None = UV/IR/dissociates. Use as the inventory.
- **The constants** (T_e, ω_e, B_e, D0, band heads) — Huber & Herzberg
  *Constants of Diatomic Molecules* / NIST diatomic constants; band-head
  wavelengths + appearance from Pearse & Gaydon *Identification of Molecular
  Spectra*. Verify uncertain visible-system assignments (e.g. CO) via search/ADS.

## Key physics note — regime vs temperature
curated hex=None for TiO/VO/MgO was a **reentry-regime** call (high T → these
dissociate). On a 1000–15000K axis the molecule is alive at LOW T (M-dwarf /
red-giant regime) → shows its band color → dissociates → atomic → ionic. So the
metal oxides DO matter at low T; that low-T molecular color is the payoff.

## Inventory (from curated DB + Huber-Herzberg)
Tier 1 — add band systems, NO new atoms (C/H/N/O/S):
  CN (violet B2Σ-X2Σ 388/421 nm) ★ ; CO (visible system — VERIFY Ångström
  B1Σ-A1Π blue-green vs 3rd-positive; Cameron is UV, not the visible green) ;
  O2 (Schumann-Runge UV; weak visible — minor) ; NO (β/γ mostly UV — minor) ;
  S2 / SO (sulfur species: S2 B-X green-yellow visible) ; H2 (Fulcher-α red
  ~600 nm — optional).
Tier 2 — metal oxides, NEED new metal atoms via NIST:
  TiO (red α/γ — Ti) ; VO (orange-red C-X 574 — V) ; FeO (orange B-X 580-612 —
  Fe) ; MgO (green B-X ~500 — Mg). SiO → SKIP (IR/UV, visible-dark).
Tier 3 — polyatomics: no own visible band; resolve to fragments once CN/CO/S2
  exist. CO2→C2/CO, CH4→CH/C2, HCN→CN, C2H2→C2, H2O→OH, NH3→NH, SO2/H2S→S2/SO.
Visible-dark (leave thermal/fragment, correct): OH(UV), HCl, HF, O3, SiO,
  NH2, H2SO4.

## Decisions log
- (date 2026-06-08) Scope = Tier 1 + Tier 2 (incl. 4 metal atoms Ti/V/Fe/Mg),
  Tier 3 via fragments, visible-dark left thermal. SiO/Si skipped (UV).
