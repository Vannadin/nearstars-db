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
      morning; directing seat cleared start — minimal Z(x) first, probe before grid).
      **Probe declarations, registered before the runs**: Uranus end-B-ice geometry
      (cmf 0, silicate layer 0.79 M⊕ intact, envelope = H/He + ice = gmf+imf0), profile
      z 1.0→0.0, m_dilute = envelope base + imf0 (so the integrated Z mass equals the
      declared ice mass automatically — the erf is symmetric about m_dilute; tail
      clipping at the edges is exponentially small at the steep width and reported at
      the shallow one), 32 shells, zr = 0, t_pot 76 K. Widths: **0.01** (steepest —
      near-step, the layered limit's neighbour) and **0.30** (shallowest — transition
      smeared over most of the envelope; Vazan-geometry conformity reported post-hoc,
      not enforced). Verdict rule (directing seat): either conv=True → grid proceeds;
      both conv=False on the h_he floor → branch ⑥, grid NOT run.
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

## Grid registration (after the probe passed — both widths conv=True)

Probe verdict (2026-09-01): w=0.01 → λ 0.174208, renorm 0.1937 (= the layered end A,
continuity confirmed), conv=True; w=0.30 → λ 0.207637, renorm 0.2081, radius residual
+0.12 %, conv=True. The gradient clears the h_he floor that killed uniform Z — the
shallow envelope tapers to clean H/He, whose adiabat stays inside the window (the
anchor's own surviving configuration). Grid proceeds.

**Width grid, registered before the runs**: δm_dil ∈ {0.01, 0.025, 0.05, **0.075
(Howard+ 2023, the one sourced point)**, 0.125, 0.20, 0.30}, both planets (Uranus and
Neptune end-B-ice geometry, z 1→0, m_dilute = envelope base + ice mass, 32 shells,
zr = 0, t_pot 76/72 K). Per point: λ, radius residual, renorm I/(M·R_pub²), P_c, T_c,
conv, and the gradient region's radial extent (Vazan-geometry conformity reported, not
enforced). Observations (N13 P_Voy 0.2300/0.2410) reported beside; **no point adopted**.
Shell-count sensitivity: rerun one mid point at 64 shells, report the digit drift.

## COMPUTE STOP (2026-09-01, owner going out — directing-seat relay)

Grid interrupted cleanly, remaining python 0 verified. **6 of 14 points done** (values
kept below — deterministic, resume continues from the rest). **Resume on the owner's
signal ONLY**: run `scratchpad/zprofile_grid.py <U|N> <w>` for the 8 missing points
{U,N} × {0.075, 0.125, 0.20, 0.30} (4-way parallel), then the shell-sensitivity point
`U 0.075 64`, then the landing gate.

Done (32 shells, conv=True all):
| pt | λ | R resid | renorm | P_c | T_c |
|---|---|---|---|---|---|
| U w=0.01 | 0.174208 | +5.44 % | 0.1937 | 1220 | 6149 |
| U w=0.025 | 0.174607 | +5.32 % | 0.1937 | 1219 | 6120 |
| U w=0.05 | 0.175925 | +4.97 % | 0.1938 | 1217 | 6044 |
| N w=0.01 | 0.180034 | +8.90 % | 0.2135 | 1533 | 6285 |
| N w=0.025 | 0.180482 | +8.78 % | 0.2136 | 1532 | 6255 |
| N w=0.05 | 0.181987 | +8.37 % | 0.2137 | 1529 | 6168 |

(Probe values already registered above: U w=0.30 → renorm 0.2081, R +0.12 %; the narrow
widths sit at the layered end A as continuity predicts — renorm starts moving in the
wide half of the grid.)

## SECOND INTERRUPT (2026-09-01 ~11:11, SIGTERM from outside this session)

The wide-half workers died on signal 15 mid-chain — not sent by this seat; same shape
as the battery-stop kill wave. Remaining python verified 0. **13 of 14 grid points are
now done** (values below); missing: **N w=0.20** (~100 s) and the shell-sensitivity
point **U w=0.075 @64 shells** (~60 s), then anchors --refresh (the gradient-radius
marks moved the fingerprint) and the landing gate. RESUME ON THE OWNER'S SIGNAL ONLY.

Wide half done (32 shells, conv=True all):
| pt | λ | R resid | renorm | P_c | T_c |
|---|---|---|---|---|---|
| U w=0.075 | 0.178521 | +4.27 % | 0.1941 | 1213 | 5909 |
| U w=0.125 | 0.186833 | +2.19 % | 0.1951 | 1202 | 5445 |
| U w=0.20 | 0.197789 | +0.33 % | 0.1991 | 1178 | 4816 |
| U w=0.30 | 0.207637 | +0.12 % | 0.2081 | 1131 | 4294 |
| N w=0.075 | 0.184934 | +7.58 % | 0.2140 | 1524 | 6014 |
| N w=0.125 | 0.193415 | +5.50 % | 0.2153 | 1510 | 5509 |
| N w=0.30 | 0.212117 | +4.14 % | 0.2300 | 1421 | 4395 |

(Not judged, recorded: N w=0.30's renorm 0.2300 sits at Uranus's target by coincidence
of digits; N's own target is 0.2410. U's radius residual nearly vanishes at wide
widths — +0.12 % at w=0.30 — while renorm covers 0.0144/0.0363 ≈ 40 % of U's deficit.)
