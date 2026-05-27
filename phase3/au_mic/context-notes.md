# AU Mic Planets Phase 3 — Context Notes

## System background

- M1Ve pre-main-sequence (~22 Myr, β Pic MG) star at 9.71 pc.
- Super-flare host: flare rate 5.6/day above 10^31 erg (Tristan 2023); Cully 1993 EUVE 10^34-10^35 erg event.
- kG-class magnetic fields (Donati 2023 ZDI).
- Edge-on resolved debris disk 35-210 AU.
- L = 0.092 L☉; Teff = 3518 K.

## Planet inventory (DB-confirmed)

| Planet | P (d) | a (AU) | M (M⊕) | R (R⊕) | Status |
|---|---|---|---|---|---|
| b | 8.463 | 0.07 | 8.99 ± 2.61 | 4.79 ± 0.29 | Plavchan 2020 transit, hot Neptune, controv=0 |
| c | 18.859 | 0.119 | 14.46 ± 3.24 | 2.79 ± 0.18 | Martioli 2021 transit, sub-Neptune, controv=0 |
| d | 12.736 | ~0.105 | 1.053 ± 0.511 | 1.02 (NEA) | Wittrock 2023 TTV-only Earth-mass, controv=0 |
| e | 33.11 | ~0.171 (derived) | 21.1 ± 5.4 | 4.87 (NEA) | Donati 2025 ESPRESSO RV, controv=1 |

For e: NEA pl_controv_flag = 1 implies disputed status. Per task instructions,
write Confidence=low throughout for e if controversy persists. The candidate
status is from a single ESPRESSO RV paper; no transit detection.

Note on d: NEA radius 1.02 R⊕ is a placeholder; Wittrock 2023 is TTV-only
mass-determination, no transit so radius is inferred from a mass-radius
relation. Confidence on d radius/density must reflect this.

## Decisions-row classification — per planet

### AU Mic b — hot Neptune (puffy, atmospheric escape regime)

All rows canonical-aligned, three tie-break for visual hex choices.
No documented divergence (Cale 2021 + Mallorquin 2024 + Allart 2023 set
the canonical reading; cfg matches).

Key decisions:
- atmosphere_surface_pressure_pa = ~100 atmospheres (~10⁷ Pa) — H/He-dominated puffy envelope
- atmosphere_present = true (Allart 2023 He I 10830 detection; Hirano 2020 RM only)
- composition: H/He dominant + trace H₂O/CH₄
- bond_albedo ~0.05 (gas giant low albedo)
- surface_temp ~600 K (Teq) — no solid surface to render
- visual: deep brown-orange with cloud bands; H/He scale height huge
- tide-lock yes given P=8.46d and small a
- inflation: R/M ratio puts b at low density ~1.06 g/cc — puffy envelope confirmed

Tie-break rows (Confidence=low):
- atmosphere_tint_rgb_hex (within range — picked deeper red for visual interest)
- cloud_tint_rgb_hex
- visual_band_pattern (Jupiter-band-analog vs uniform — picked banded)

### AU Mic c — sub-Neptune (denser, possibly more rocky core)

All canonical-aligned, two tie-break.

Key decisions:
- 2.79 R⊕ + 14.5 M⊕ → density ~3.7 g/cc → sub-Neptune envelope retained
- atmosphere_present = true (no direct atmospheric detection but interior modeling supports H/He envelope)
- atmosphere_surface_pressure_pa ~10⁵-10⁶ Pa
- tide-lock yes
- visual: muted brown-orange, less inflated than b

Tie-break rows:
- atmosphere_tint
- cloud_tint

### AU Mic d — Earth-mass TTV candidate

All Confidence=medium or low because radius is inferred (1.02 R⊕ NEA
placeholder; Wittrock 2023 doesn't measure radius).

Key decisions:
- mass 1.053 ± 0.511 M⊕ — Earth-mass within 2σ
- radius: NEA placeholder 1.02 R⊕ — but no transit detection, so this
  is from a mass-radius relation (Chen & Kipping 2017 or similar)
- atmosphere: at d's insolation (~5-10 S_earth — interior to b at ~0.105 AU but
  HZ for AU Mic is ~0.3 AU), and given super-flare bombardment, atmosphere
  retention is highly questionable. Two scenarios:
  - Atmosphere-free rocky surface (canonical from XUV escape arguments)
  - Thin secondary CO₂/N₂ atmosphere (outgassing-replenished, low pressure)
- Cfg picks the secondary atmosphere variant (interesting-first) but documents
  the airless alternative
- visual: dark basaltic with possible iron-oxide reddening
- super-flare bombardment dominates the scene visually

Documented divergence:
- atmosphere_present = true (thin) vs canonical "likely airless given XUV"
  → Canonical alternatives section needed

### AU Mic e — Donati 2025 candidate (pl_controv_flag=1)

All Confidence=low per task spec. The candidate status from a single ESPRESSO
RV paper is the dominant uncertainty.

Key decisions:
- mass 21.1 ± 5.4 M⊕ (Donati 2025), radius unspecified
- 33.11 d period → a ~0.17 AU
- M_sin(i) but Donati 2025 reports as "Mass" (uncertain on this; need to read)
- Without radius, density is unknown — treat as "uncertain" between sub-Neptune
  and Neptune analog
- Cfg pick: medium-density Neptune analog (interesting visualization), but
  full caveat in Open items
- If e is later retracted, cfg variant must support removing the planet

This is a candidate; cfg ships e as a "tentative" planet with all values low.

## Step-9 row counts

Per planet:
- b: 27 rows; 24 canonical-aligned, 3 tie-break, 0 divergence
- c: 26 rows; 24 canonical-aligned, 2 tie-break, 0 divergence
- d: 27 rows; 22 canonical-aligned, 3 tie-break, 2 divergence (atmosphere_present + ocean_present)
- e: 22 rows; 0 canonical-aligned (all Confidence=low), all rows tie-break flavor

## Notes on sources

- Plavchan 2020 (2020Natur.582..497P) — AU Mic b discovery transit
- Martioli 2021 (2021A&A...649A.177M) — AU Mic c discovery transit  
- Wittrock 2023 (2023AJ....166..232W) — TTV; introduces d candidate
- Mallorquin 2024 (2024A&A...689A.132M) — ESPRESSO mass refinement b/c
- Donati 2025 (2025A&A...700A.227D) — ESPRESSO; e candidate
- Cale 2021 (2021AJ....162..295C) — RV mass/density for b, inflated puffy
- Allart 2023 (2023A&A...677A.164A) — JWST He I 10830 detection for b
- Hirano 2020 (2020ApJ...899L..13H) — Rossiter-McLaughlin for b
- Klein 2021 (2021MNRAS.502..188K) — ZDI/RV for AU Mic
- Tristan 2023 (2023ApJ...951...33T) — TESS flare census; bombardment context

Most planet-specific papers not in _papers/ as full text; bibcodes cited
based on published header conventions. For papers without verified full-text
fetch, mark Basis with paper+year and use the standard ADS bibcode format.
