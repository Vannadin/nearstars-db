# Composition gradient Z(x) — checklist (Brief 26, pre-registration draft)

Drafted 2026-09-01, before work starts. **Work does NOT start until the owner's morning
report** — the h_he cold-floor wall surfaced after the owner approved the method, and the
directing seat holds the final brief until then. This draft is the compute-free share.

## Premise, updated by the ice-axis landing

The original brief left open "if the ice axis covers much of the deficit, the gradient
relaxes". The measured result is the opposite: **the ice axis cannot be measured with
uniform Z at all** (all four end-B solves conv=False; the surface pins at 355–363 K vs
t_pot = 76 K because trial adiabats die at the h_he table's cold floor — 1830 K at
130 GPa, 1945 K at 164 GPa, 3130 K at 1050 GPa, directing-seat measurement; reproduction = probe the h_he window floor at fixed
pressure by bisecting temperature against the too_cold refusal, milliseconds). So the
gradient is **the only remaining path**, and whether it clears that wall is the first
question, not the last.

## Pre-registered plan

**First work item — the wall probe, before any grid.** Two points only: the steepest
width and the shallowest width the grid would contain. If either yields conv=True, the
grid proceeds. If neither does, **that is the product** (branch ⑥) and the grid is not
run.

**Anchor check.** Width 0 must reproduce the current layered answers **bit-identically**
(renorm 0.1937 / 0.2135) — the same identity style as every prior axis.

**The grid (method 나+가, owner-approved).** Width axis narrowed by Ledoux, not chosen:
- **Ledoux cap, route A (default): transcribe, don't derive.** Vazan & Helled 2020
  (cached 1908.10682) publish Ledoux-stable Uranus models with declared knobs
  (a₀ = 0.1; α ∈ [5e-3, 0.5]; criterion ∇R > ∇A + ∇X, their §2.3) and adopted-model
  profiles fitting MoI 0.222–0.230 directly. The cap = the widest gradient their stable
  models sustain, taken from the paper with the knobs stated. This is a transcription.
- **Route B (check, only where computable): our own ∇X** via the mixture EOS
  (∂lnT/∂Z at fixed ρ,p by finite difference on additive volume; dZ/dlnp from the trial
  profile). Full Ledoux needs ∇R, which this recipe does not carry — if the check
  requires it, the check refuses by name rather than inventing a radiative model.
- **Howard+ 2023 δm_dil = 0.075** enters as one sourced point on the grid, with its
  provenance caveat attached (Jupiter/Juno, not an ice giant).
- **Position axis**: the H–H₂O miscibility boundary gives the transition's location and
  **never its width** (miscibility-pairs.md, first cell). Gupta+ 2025 (ApJL 982 L35,
  arXiv 2407.04685) is **NOT in the paper cache** — fetch-and-pin is the first read at
  start; the transcribability question is asked before any number moves.

**Reporting.** Per grid point: renorm I/(M·R_pub²) and radius residual. Observations
(N13 P_Voy targets) are **reported beside, never fitted**; no point is adopted.

**Out of scope** (from the original brief): Howard+ 2025, the luminosity axis, the
silicate melting curve.

## Outcome branches, six

1. Grid runs, some widths converge → the measured span vs the deficit, beside the rock
   axis's 26 %/41 % table.
2. Grid runs, no width converges but for varied, named reasons → coordinates per width.
3. Ledoux cap not transcribable from the paper (route A fails) → route B where
   computable; if neither, the width axis is unmeasurable and says so.
4. Gupta+ 2025 not transcribable → position axis falls back to what the miscibility
   table already grounds; recorded, not invented.
5. Outside the register → name it.
6. **The gradient hits the same h_he cold floor** (wall probe: both ends conv=False on
   that wall) → the next item is not the gradient but **the material ceiling itself**:
   does a published H/He table extend below that floor — the same shape of question
   answered for water with IF97/AQUA.

## Work items

- [ ] wall probe: steepest + shallowest width, conv or the wall (owner reported 09-01
      morning; directing seat cleared start — minimal Z(x) first, probe before grid)
- [ ] width-0 anchor identity (bit-identical to layered)
- [x] fetch-and-pin Gupta+ 2025 (2407.04685 · 2025ApJ...982L..35G) — **transcribable,
      closed form**: critical curve Eqs. 5–10 with Table 1's six printed parameters
      (validity 750–6000 K × 0.25–2000 GPa). Table verified against the typeset page
      images (the IF97 corrupted-channel rule) — all six match the text layer; spot
      check P_c(3000 K) = 27.0 GPa vs the paper's own "near 30 GPa at 3000 K".
      Caveats pinned in the PROVENANCE: binary-system curve (x=0.6 shifts +~10 GPa at
      3000 K); location only, never width
- [ ] Ledoux cap route A transcription (knobs stated), route B check where computable
- [ ] grid + per-point report (renorm, radius residual; observations beside, not fitted)
- [ ] landing: notes, C13 row hand-off to directing seat
