<!-- Saha/Boltzmann 엔진 설계 결정과 유도 근거를 누적 기록 -->
# Context notes — Saha/Boltzmann LTE plasma color

Append-only log of decisions + derivations. See [plan](plan.md).

## Why a slab, not a weighted blend (2026-06-08)

The old builder modeled `combined = (1-w)·blackbody + w·emission` with `w(T)` a
hand-set linear ramp (3000→9000K, identical for every gas). Two dishonesties:
(a) the transition temperature is the same for H₂ (weak bond, ionizes early) and
N₂ (triple bond, very robust) — physically wrong; (b) the emission hue is a
single fixed curated value regardless of T.

The isothermal LTE slab `I_λ = B_λ(T)(1−e^{−τ_λ})` fixes both **for free**:
- It is a real radiative-transfer solution, not an interpolation invented for
  this table.
- `τ_λ(T)` carries the chemistry: line opacity only appears once Saha+Boltzmann
  populate the lower level, so each gas lights up its lines at its own T.
- Hue-normalizing `I_λ` means the absolute faintness of a thin cold gas does not
  matter — we read off whatever hue the (weak) spectrum has, which in the thin
  limit is `B_λ(T)·τ_λ` ≈ thermal-tinted, marching to line-dominated as T rises.

The one knob left is the column `L·n` (optical depth scale). That is honest: a
denser/longer plasma genuinely looks more blackbody-like. Fix it, document it,
maybe show tiers.

## State of existing DBs (what we can and cannot reuse)

`db/refs/{element,molecular}_plasma_colors.yaml` carry `emission_lines/bands`
with `{nm, intensity}` — but `intensity` is a **curated relative snapshot**, not
`A_ki`, and there is no `E_upper`, `g`, ionization energy, or partition fn. So
the wavelengths are reusable as a cross-check; the rest must be curated fresh
from NIST ASD (atoms) and band-spectroscopy literature (molecules).

Note: the element DB folded **molecular** bands into atomic entries (element "N"
lists N₂⁺/N₂ bands; "C" lists C₂ Swan / CN). For the engine these must be split:
atomic lines → `atomic_lines.yaml`, molecular band systems → `molecular_bands.yaml`.

## Decisions (defaults pending user veto)
- D1 P=1 atm reference; column tiers thin/medium/thick. Saha density from P.
- D2 Molecular bands kept (band-as-effective-line); weight = computed
  dissociation fraction. Keeps reentry C₂-Swan green + CN-violet.
- D3 Atom set {H,He,C,N,O}+first ions. Covers all 6 compositions. S deferred.
- D4 LTE only. Aurora (non-LTE) out of scope, stays curated.

## Derivations / formulas (fill as implemented)
- f_lu from A_ul:  f_lu = (g_u/g_l) · (m_e c / 8π²e²) · λ² · A_ul
- Saha:  n_{i+1} n_e / n_i = 2 (U_{i+1}/U_i) (2π m_e k T / h²)^{3/2} e^{−χ_i/kT}
- Boltzmann:  n_j = n · (g_j/U(T)) e^{−E_j/kT}
- (TODO) dissociation K_p(T), continuum κ_ff / κ_bf, line profile width

## Progress 2026-06-08

**Done + verified:**
- `cie_color.py` extracted; `blackbody_srgb` byte-matches the old builder at 8
  test temps; `spectrum_to_hex(planck)` == `blackbody_srgb`. CIE path solid.
- `build_atomic_lines.py` + `db/refs/atomic_lines.yaml` (8 species: H I, He I,
  C I/II, N I/II, O I/II). Pulled from NIST ASD (lines1.pl + energy1.pl,
  format=3 TSV). Anchors verified: Hα 656.28/A=6.47e7, He D3 587.56/7.07e7,
  C II 426.7/2.34e8, O I 777 triplet/3.69e7, ground terms + ionization energies.
  NIST fetch is via the MAIN thread (subagents are denied WebFetch/Bash); the
  builder is cache-first (`/tmp/nist`), `--refresh` forces live re-fetch.
  - `_num` bug fixed: scientific-notation `3.69e+07` was truncated at `+`, so
    only negative-exponent (forbidden) lines survived. Now regex-parsed.
- `saha_boltzmann.py` atomic engine — mechanically correct: self-test slab@1500K
  == blackbody exactly; isolated 550nm ⇒ green; ionization fractions physical
  (air 0.8% @9000K → 11% @12000K → 45% @15000K, n_e rising smoothly).

**Key physics finding (drove the next step):** atomic-only is NOT enough.
- Hot-air atomic emission is dominated by O I 777 nm (red) + N I 746/821 nm
  (red/IR) — verified by ranking n_upper·A·hν. That is physically correct but it
  is RED, not the iconic reentry blue-violet. The blue-violet is MOLECULAR:
  N₂⁺ 1NG 391 nm + N₂ bands. So molecular bands (D2) are mandatory, not optional.
- Real visible-line optical depth in a thin layer is tiny (κ_center ~3e-4 cm⁻¹
  for a strong O I line at 8000K ⇒ τ~1 needs L~30 m). So the slab needs a
  calibrated reference column; line-vs-continuum contrast is a documented knob.
  The slab's LTE B·κ identity was checked: B_λ·κ_line ∝ n_upper·A (emission),
  so the thin-limit emission color is correct — only the magnitude is tuned.

**Next:** `db/refs/molecular_bands.yaml` (N₂ 1P/2P, N₂⁺ 1NG, CN, C₂ Swan, CH, NH)
+ dissociation equilibrium (law of mass action, bond energy) → band-as-effective-
line in the engine. Then joint calibration of the 2 slab knobs against anchors
(low-T ember, mid-T reentry bands, high-T ionic), wire into the builder.

## Final model + calibration (2026-06-08)

Abandoned the strict slab `I=B(1−e^{−τ})` with Kirchhoff κ=j/B — `planck_rel`'s
tiny absolute scale (~1e-14 in nm^-5) made j/B blow up (τ~1e26). Switched to an
**optically-thin LTE emission** model, which gives correct hues in both limits
after max-channel normalization and is numerically robust:

    j(λ) = (n_heavy/N_REF)·Planck_shape(λ,T)  +  GAIN · Σ emission(λ)
    color = CIE(j)

- thermal term ∝ density·Planck = incandescent glow of the bulk gas; ∝1/T at
  fixed P, so it fades as the gas heats/rarefies. Low-T ⇒ blackbody hue. ✓
- emission = atomic lines (n_upper·A·hν) + molecular bands; grows with excitation.
- ONE tuned constant: `GAIN=3e-6` (thermal:emission balance). `N_REF=2e18`,
  P=1 atm, line width 1.2 nm, band width 5 nm. Everything else first-principles.

Self-tests: slab@1500K == blackbody exactly; isolated 550nm ⇒ green.

**Result colors (validated against physical expectation):**
- co2: ember→ #00ffe1 C₂ Swan green @4000K (mol=0.59, emis=0.79) → blue/white →
  ionic. ch4 similar (CH+C₂). H Balmer pink-magenta for h2_he @≥12000K.
- N₂ dissociation curve correct: air mol 1.0 @≤3000K → 0.82 @6000K → 0.13 @8000K.

**Key documented divergence — air reentry blue is NON-LTE.** N₂ 1P (B³Πg, 7.4 eV)
and 2P (C³Πu, 11 eV) upper states are far too high to populate thermally
(exp(−7.4eV/kT)~1e-17 at 5000K), so LTE air glows thermal→atomic(O I 777 red,
N I red/IR)→ionic(pale violet/pink), NOT the iconic blue-violet. That blue is
electron-impact (non-LTE) excitation of N₂⁺ 1NG — correctly absent here. C₂ Swan
(d³Πg, 2.5 eV) IS thermally accessible, so the carbon-plasma green is real LTE.
Firefly reentry cfg keeps the observation-based curated blue for air (cite this
divergence); this table is the first-principles reference.

**co2 CN-violet caveat:** pure C+O has no nitrogen → C₂ Swan only. The Mars-EDL
CN-violet needs trace N₂ — documented in molecular_bands.yaml, not modeled.

State: engine + atomic_lines.yaml + molecular_bands.yaml + rebuilt
plasma_temperature_colors.yaml + visualizer caption/tooltip all done; check.sh
green. Remaining: tools.md registration (+ko), optional validate script.

## Open questions
- Continuum: is free-free alone enough for hue, or is bound-free needed below
  the Balmer/Paschen edges? Decide empirically vs curated hexes.
- Column tiers: render all 3 in the grid, or pick one "reentry-representative"
  value and note the others? Lean: one value in the grid, sensitivity in caption.
