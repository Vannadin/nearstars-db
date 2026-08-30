# antigorite's thermal term — context notes (F2)

## The first question: is antigorite in the data set — yes

Holland & Powell 1998 (1998JMetG..16..309H; the cached file is Wiley's 2004 re-hosting, first
line "J. metamorphic Geol., 1998, 16, 309–343"), read with `pdftotext -layout`. Table 1a lists
**antigorite, atg, Mg₄₈Si₃₄O₈₅(OH)₆₂** among "Other sheet silicates", and Table 5 carries its
row:

| ΔfG (kJ) | ΔfH (kJ) | σ_H | S (J/K) | V (J/bar) | a (kJ/K) | b (10⁵ kJ/K²) | c (kJ·K) | d (kJ·K^½) | a° (K⁻¹) | κ (kbar) |
|---|---|---|---|---|---|---|---|---|---|---|
| −70622.39 | −71417.98 | 19.91 | 3591.00 | 175.480 | 9.6210 | −9.1183 | −35941.6 | −83.0342 | 4.70 | 525 |

The a° column is printed in units of 10⁻⁵ K⁻¹ (forsterite reads 6.13, the familiar
6.13×10⁻⁵; periclase 6.20; quartz 0.65). The functional forms, from the text:
V(1,T) = V°[1 + a°(T − 298) − 20a°(√T − √298)], i.e. α(T) = a°(1 − 10/√T); the Murnaghan EOS with
k∞ = 4; and κ_T = κ₂₉₈(1 − 1.5×10⁻⁴(T − 298)).

**The chain is real.** Hilairet+ 2006 §4 write that their stability field was computed "using
… thermal expansivity of Holland and Powell [1998]" and compare their K₀ with "Holland and
Powell's [1998] database value". So the recipe borrows where Hilairet borrows: recipe →
Hilairet → Holland & Powell 1998, the same edition.

The fourth pre-registered branch ("the source does not reach the deciding region") is
checked and **not taken**: antigorite is in the set, and the expansivity form is the
dataset's global one, valid at the 1 bar–few GPa, 250–400 K the three moons' rock occupies.

## What was carried, and how it was flattened

This recipe's thermal term is αK_T·ΔT with a constant αK_T (Anderson & Goto, Seager's form),
so Holland & Powell's temperature-dependent α cannot enter as a function. It is evaluated at
the reference isotherm:

- α(298.15) = 4.70×10⁻⁵ × (1 − 10/√298.15) = **1.978×10⁻⁵ K⁻¹**, against 2.78×10⁻⁵ at 600 K and
  3.21×10⁻⁵ at 1000 K — the flattening is 40 % low by 600 K and that is stated where the
  constant lives;
- αK_T = α(298) × K₀(Hilairet, 67.27 GPa) = **1.331 MPa/K**. Hilairet's K₀ rather than Holland &
  Powell's 52.5 GPa, because the compression curve the term rides on is Hilairet's (a
  consistency choice, stated);
- κ(T) has no slot in this form and is not carried;
- c_V = C_p(298.15) from the polynomial, 4380.7 J/K/mol, over 4535.9 g/mol → **966 J/kg/K**,
  taken as c_V for a solid;
- reference: 298.15 K, isotherm.

**Composition differs.** Holland & Powell's antigorite is the pure Mg end-member
(V = 175.480 J/bar → ρ 2585 kg/m³); Hilairet's sample carries Fe and Al (ρ₀ 2640.5). The
thermal term of one is placed on the compression curve of the other. That is the grade's
reason now — a borrowed, flattened term from a different composition — where before it was
the term's absence. The C10 sentence "the grade is set by the missing thermal term" is
therefore false and was rewritten in the same commit (row, domain row, EOS table, note in
`solve`, EN and KO).

## Two defects the term exposed

Giving antigorite thermal constants made `Mixture.grad_ad` evaluate its c_P, and with it
`Material.k_t`'s finite difference — which pokes half a step *above* the pressure it is
asked at. The shooting's bracket puts a trial exactly on the material's ceiling (10 GPa for
antigorite), and there the derivative's upper point fell outside the phase and raised. Pure
antigorite (f = 1) met the same through the integrator's own `_adiabatic_dtdp`. Both
differences are now clipped at the material's ceiling (one-sided there, central elsewhere).
Nothing that solved before touches the clipped branch — a state that previously raised is the
only one that changes — and Earth and the Ganymede-class icy solve reproduce to the last
digit.

## The sweep, re-run on the same grid — nothing moves

Three moons, `infer_three_layer` at 270 K, f = 0, 0.25, 0.5, 0.75, 1, with the thermal
antigorite. Band top (zero-core end) against the C10 sweep:

| moon | published | f = 0 | 0.25 | 0.5 | 0.75 | 1.0 |
|---|---|---|---|---|---|---|
| Callisto | 0.3549 | 0.3119 (=) | 0.3165 (=) | 0.3213 (=) | see below | 0.3321 (=) |
| Titan | 0.3414 | 0.3126 (=) | 0.3172 (=) | 0.3222 (=) | see below | 0.3334 (=) |
| Enceladus | 0.3350 | 0.3008 (=) | 0.3058 (=) | 0.3109 (=) | 0.3161 (−0.0001) | 0.3215 (−0.0001) |

Identical to four decimals at every finished point; Enceladus drifts by one unit in the
fourth place at f ≥ 0.75. **Callisto and Titan at f = 0.75 did not finish inside the sweep's
budget** — both ran past forty CPU-minutes where C10's runs took 70 s — and the reason was
traced rather than waited out (its row is filled in below when the run ends). The band
member that stalls is the ice-rich one: a trial path whose water column passes 2.3–5 GPa at
500–1000 K enters the band C3 left without an equation of state and throws *too cold*, the
temperature bracket raises the centre past 2000 K, the ice mantle is then on Mazevet's
fit (an expensive integration), and every downward step re-enters the band and is thrown up
again — thirty pressure shoots in 45 s, each on hot-water integrations, until the passes are
exhausted and the member returns `converged=False`. It is the C3 band-direction trade-off
(recorded there as a trade-off) biting a warm water world, **an open defect that F2 exposed
and did not fix**: the fix belongs to the band (an equation of state for dense liquid water
between 500 and 1000 K — SeaFreeze `water2`, the shelf named in C3), not to this item. A
bracket-collapse guard was added to the pressure shoot during the investigation; it is
separate and, on this case, not the cause. The reason is arithmetic, not a surprise: the moons' rock sits at 250–400 K,
within ~100 K of the 298 K reference, so αK_T·ΔT is ≲ 0.1 GPa against 2–3 GPa of pressure —
the thermal term is real and it is negligible here. **No moon reaches its published C/MR² at
any fraction in [0, 1]**; the pre-registered overturn condition is not met, and C10 stays
closed with a revisited line.

## The nesting corner moved, and the comment moved with it

`c0c15b35`'s warning was about a cold component inside a nested mixture flattening the
thermal parts around it. With antigorite thermal, **no material in this repository is cold
any more**, so the pass-through branch in `Mixture.grad_ad` is not reached by any mixture at
all — including serpentinised rock. The branch stays for the day a material without thermal
constants returns, and its comment now says so.

## What moved when antigorite left `cold_phases`

- `Material.cold_phases()` for antigorite is now `()`, so a serpentinised body's note no
  longer lists it as a phase temperature passes through, and `Mixture.grad_ad` now weights
  **both** parts of the rock mixture by c_P (before, only the silicate part carried the
  adiabat). At the moons' 250–400 K the difference is the ≲ 0.1 GPa thermal pressure noted
  above — invisible at four decimals in C/MR².
- `test_interior`'s antigorite block changed from "cold phase, 10 GPa" to a re-derivation of
  αK_T and c_P from Holland & Powell's row.
- Two finite differences were clipped at the phase ceiling (`eos.Material.k_t`,
  `interior._adiabatic_dtdp`) because the thermal term made them run at the shooting's
  ceiling trial for the first time; a bracket-collapse guard went into `_shoot_pressure`.
  None of the three touches a state that solved before.

## A number that moved because the derivative stopped poking: Jupiter's core cap

The gate caught it: `test_giant` measured the largest silicate core a Jupiter-mass giant
holds at **16.69 M⊕**, against the 11.46 M⊕ recorded in C1. The mechanism is the same clip.
On HEAD a 14 M⊕ core refused with "the silicate layer's base at **13501 GPa** is above the
13500 GPa ceiling" — the shooting had placed a trial exactly on the ceiling and the
isothermal-bulk-modulus finite difference reached 0.01 % past it; with the difference
clipped, the same trial integrates and the 14 M⊕ core solves at P_c 11.36 TPa, under the
ceiling. So the 2026-08-29 cap was half a defect too: the envelope-base bug it replaced was
real, but the number it left was the derivative's wall, not the silicate's. Updated in the
same commit: `test_giant`'s expectation and comment, the domain row (EN, KO), the C1 row and
the sub-Neptune notes (both marked interim, superseded). The giant anchors themselves
(Jupiter, Saturn Z = 0 and 0.0825) are unchanged — they never sat on a ceiling.

## Anchors and the re-freeze

No anchor carries serpentinised rock, and the f = 0 path returns the silicate object itself,
so no anchor value moves: Earth (1.0029682364205592 R⊕, T_CMB 2526.2085475146446 K) and the
Ganymede-class icy solve (0.3570574293277166 R⊕) reproduce to the last digit after every
edit, and `--fast` reports the ice giants' convergence-point integrations bit-identical.
`ice_giant_anchor.json` was re-frozen for the **fingerprint only** — three path functions
changed their text or their unreachable branches: the note string in `solve`, the guard in
`_shoot_pressure`, the ceiling clip in `_adiabatic_dtdp`. Movement: none.

## Rejected on the way

- Carrying Holland & Powell's α(T) as a function: this recipe's thermal pressure is
  αK_T·ΔT with one constant per phase (Anderson & Goto), and every other phase is carried
  that way; a temperature-dependent α would need a different thermal-pressure form for one
  phase. Flattened at 298 K and the 40 %-by-600 K width stated instead.
- Using Holland & Powell's κ₂₉₈ (52.5 GPa) in αK_T: the compression curve is Hilairet's, so
  its K₀ multiplies the borrowed α; the product with κ₂₉₈ (1.04 MPa/K) is recorded here for
  the difference.
- Waiting out the two f = 0.75 runs before landing: traced instead (above), the mechanism is
  a C3 band defect, and the rows are filled in when the runs end.

Gate: the antigorite transcription check gains the thermal re-derivation; milliseconds. The
sweep is a flag.
