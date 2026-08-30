# Lighter rock — context notes

## The derivation, from the PDF

`docs/phase3/_papers/2006GeoRL..33.2302H.pdf`, text extracted with `pdftotext -layout`.
Located by paragraph number:

- §2 [6]: sample Cu12 (Escambray massif, Central Cuba), structural formula
  (Mg₂.₆₂Fe₀.₁₆Al₀.₁₅)Σ=2.93(Si₁.₉₆Al₀.₀₄)Σ=2O₅(OH)₃.₅₇, a one-layer polytype, average m = 14.
- §3 [13]: "The best fit is obtained with a second order EoS, yielding V₀ = 2926.23(50) Å³ and
  K₀ = 67.27(123) GPa (K₀′ = 4). A fit to the third order yielded V₀ = 2926.65(47) Å³, K₀ =
  62.03(223) GPa and K₀′ = 6.39(98). A F-f plot confirms a second order EoS."
- §4 [15]: "The V₀ value corresponding to m = 1 for antigorite is 172 Å³".
- §4: "at 5.7 GPa and 470°C, antigorite density calculated with our new bulk modulus is
  2765 kg·m⁻³ approximately 1.6 % lower than values obtained from Holland and Powell [1998]".
- Abstract: "determined at ambient temperature up to 10 GPa … No amorphization, phase
  transition or hysteresis were detected during compression or decompression."

ρ₀: one m = 1 unit weighs Mg 2.62×24.305 + Fe 0.16×55.845 + Al 0.19×26.982 + Si 1.96×28.086 +
O 5×15.999 + OH 3.57×17.007 = **273.50 u**; at 172 Å³ that is 273.50 × 1.66054×10⁻²⁷ kg /
1.72×10⁻²⁸ m³ = **2640.4 kg/m³**. Two earlier independent readings gave 2638–2640; the survey's
"2639" and this session's 2640.5 differ in the atomic masses used and the rounding of the
formula, not in the method. Checks: 2926.23 / 172 = 17.013, the m = 17 polysome (Capitani &
Mellini 2004) the paper indexes its m = 14 sample with ("negligible effect on refined m = 1
volumes"); and the BM2 at 5.7 GPa gives 2841 kg/m³ at room temperature against the printed
2765 at 470 °C, +2.7 %, which is the size and the sign of 450 K of thermal expansion.

Not read into the engine: the third-order fit (comparison only), the P–T stability field,
the seismic velocities.

## What the material is allowed to do

BM2 to 10 GPa. *(Interim, superseded 2026-08-30 by F2: the paragraph below described the
state at C10's landing.)* At landing the phase had no thermal term — `alpha_k = 0`, isothermal,
named by `cold_phases()` — and the grade followed from that deficiency. Since F2 the term is
borrowed from Holland & Powell 1998 (the source Hilairet's §4 borrows from), flattened at
298 K, and the grade follows from the borrowing and flattening instead; see
`engine/antigorite-thermal-context-notes.md`. Above 10 GPa the material still declines by
name: the paper's range ends there and serpentine above it is a dehydration problem, not the
same phase.

## The mixture, and the one rule extended

`serpentinisation` = mass fraction of antigorite in the rock layer, mixed by additive volume
with the enstatite/PREM silicate — two solids as grains, which is what a partially
serpentinised rock physically is, and the same rule the recipe carries for rock and metal.
Not the mixture C7 forbade: that was water *into* silicate, a reaction.

`Mixture.grad_ad` used to raise when any component returned no c_P. antigorite has no thermal
constants at all, so with a declared temperature the rock layer would have declined
everywhere. The rule extended: a component with `has_thermal == False` is skipped in the
c_P weighting, exactly as a pure cold phase carries dT/dP = 0 — temperature passes through
that fraction. A component that *has* thermal constants but returns c_P ≤ 0 still raises.
`h_he_z` and the ice-mantle rock mixture (C5) have all-thermal parts and are untouched.

## The sweep

`infer_three_layer` on Callisto, Titan and Enceladus with the icy roster's 270 K, at f = 0,
0.25, 0.5, 0.75, 1 (`test_interior.py --serpentine`; 35–400 s per run, 15 runs in parallel):

| moon | published | f = 0 | 0.25 | 0.5 | 0.75 | 1.0 | closes in [0, 1]? |
|---|---|---|---|---|---|---|---|
| Callisto | 0.3549 | 0.2856–0.3119 | 0.3165 | 0.3213 | 0.3265 | 0.3321 | no (0.023 short) |
| Titan | 0.3414 | 0.2853–0.3126 | 0.3172 | 0.3222 | 0.3276 | 0.3334 | no (0.008 short) |
| Enceladus | 0.3350 | 0.2682–0.3008 | 0.2682–0.3058 | 0.2683–0.3109 | 0.2683–0.3162 | 0.2684–0.3216 | no (0.013 short) |

The band top rises ~0.005 per 0.25 of fraction on all three and never reaches the published
value. On Callisto and Titan the band collapses to its zero-core member for f > 0: with a
lighter rock no core fraction on the grid (0.15–0.45) reproduces the radius, which is the
same statement from the other side. Pure antigorite closes 40–75 % of each gap.

**No fraction was chosen.** Extrapolating the grid past f = 1 would ask for rock lighter than
antigorite, which is not a composition this recipe has a source for; the honest reading is
that what remains is void space (C9's branch) or the partial differentiation C7 declined.

## Layers kept apart

- C9's statement is rheology: a core dominated by antigorite would not keep its pores.
- Hilairet's statement is density: antigorite's ρ₀ and its compression.
- This item's statement is geometry: even pure antigorite does not lift the band far enough.
Together on Enceladus: the missing lightness is pores, and the pores live in rock that is
not mostly antigorite. None of the three refutes another.

## What moved

Anchors: nothing — the f = 0 path returns the silicate object itself, and the Ganymede-class
icy solve reproduces HEAD to the last digit; giants and ice giants do not touch the rock
mixture; `--refresh` for the touched signatures, values identical. Gate: the transcription
checks are milliseconds; the band sweep is a flag, not a gate step.

Dante / Hades: not touched. The row records that the axis is the one that question turns on.
