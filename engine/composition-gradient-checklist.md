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

- [x] wall probe: steepest + shallowest width, conv or the wall (owner reported 09-01
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
- [x] width-0 anchor identity — BIT-IDENTICAL twice (anchor ± Z≡0 profile; rock-free
      toy layers vs zero-width step), 872c44ae
- [x] fetch-and-pin Gupta+ 2025 (2407.04685 · 2025ApJ...982L..35G) — **transcribable,
      closed form**: critical curve Eqs. 5–10 with Table 1's six printed parameters
      (validity 750–6000 K × 0.25–2000 GPa). Table verified against the typeset page
      images (the IF97 corrupted-channel rule) — all six match the text layer; spot
      check P_c(3000 K) = 27.0 GPa vs the paper's own "near 30 GPa at 3000 K".
      Caveats pinned in the PROVENANCE: binary-system curve (x=0.6 shifts +~10 GPa at
      3000 K); location only, never width
- [x] Ledoux cap route A: Vazan §3.3's printed geometry (stratified below ~0.8 R)
      transcribed and measured per point — conformal only at w ≤ 0.025; every moving
      width excluded (context notes §5, with the z_shallow=0 family limitation named).
      Route B refused by name (no ∇R in the recipe)
- [x] grid complete 14/14 conv=True + shell sensitivity (renorm digit-stable at 64
      shells) + extent pass — full table in context notes §5; span U 39.7 % / N 60.0 %
      of the deficit, radius residual U +5.44→+0.12 %; **no width adopted**
- [x] landing gate: **FAIL 0, exit 0, 1205 s measured** (detached run). The first full
      gate FAILED 1: code uses `envelope_z_profile` but the methodology doc's Needs
      lacked it — the prose-lags-code class this list keeps meeting (Brief 23 hit the
      same check); fixed in en + ko docs, rerun clean. Two rerun attempts in between
      died at ~600 s on the tool harness's own timeout (SIGTERM — neither the owner nor
      the directing seat; the attribution sub-kind gains the branch "the sender
      candidates include the execution harness itself"); the completing run was
      detached from the harness. Anchor `seconds` unchanged class (21.9→22.2→21.9-grade
      jitter), values bit-identical throughout
- [ ] C13 row hand-off to directing seat (report sent)

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

# Brief 27 — widen the family to z_shallow > 0 (owner chose (b)) — REGISTERED BEFORE RUNS

Basis: `728f6f5d` — route A's cap is a **family resemblance** (the shape of Vazan &
Helled 2020's successful models), not a stability calculation. This brief puts that
shape into the declared family and measures again.

**Design — no engine edit needed, and that is the identity argument**: Brief 26's erf
already produces the three-part shape when z_shallow > 0 (deep Z → gradient → a
homogeneous outer plateau at Z = z_shallow), the validations already admit
0 ≤ shallow ≤ deep ≤ 1, and the dispatch already mixes the outer shells. z_shallow = 0
declarations are therefore **the same calls byte-for-byte** — identity by
call-equality, plus one measured rerun (U w=0.20, must be bit-identical to the grid
log) so the claim is measured, not argued.

**z_shallow is a declaration with a citable bracket**: Vazan & Helled 2020 §3.3, the
metal-rich convective outer layer of all successful models except two-layer U-1 carries
**Z = 0.6–0.7** (the T_int pattern: declare inside a published bracket, never invent).
Source cited beside every value.

**Mass conservation, forced by the declaration mapping**: total heavy mass is fixed
(rock layer + envelope Z-mass = the end-B budget), so raising z_shallow pushes the
transition deeper: m_mid = (imf0 + base − s·1)/(1 − s) from
(m_mid − base) + s·(1 − m_mid) = imf0 (symmetric erf). Shells conserve the integral
exactly (mass-averaged erf), but the erf tail clipped at the envelope base is NOT
negligible at wide widths — the runner prints the actual integrated Z mass next to the
declared imf0 and the difference is reported per point.

**Conformity criterion, redefined for this family** (registered here): the *gradient*
(heterogeneous) region m_mid ± 2δm must sit below 0.8 R (r_grad_top ≤ 0.8 R); above it
the profile is homogeneous at z_shallow by construction and convective by the recipe's
adiabatic assumption — i.e. Vazan's actual description (outer ~20 % homogeneous
convective, stratified below), not just "gradient below 0.8 R with a clean top".

**Probes before any grid** (2-D grid would be 42 solves): Uranus, three points —
(z_shallow 0.6, w 0.20) · (0.7, 0.20) · (0.65, 0.30), serial. Two questions each:
① conforms (r_grad_top ≤ 0.8 R)? ② renorm moves off the layered end A (0.1937)?

**Branches, five**: ① conforms AND moves → grid; reachable coverage exists for the
first time. ② conforms, doesn't move → the homogeneous top kills the moment gain;
trace why; that is the result. ③ moves, doesn't conform → the family widening lands in
the same place; the cap itself becomes the question → (a). ④ neither → the gradient
axis closes in this recipe; C13's next item changes. ⑤ outside the register → name it.

**Hard constraints**: z_shallow=0 reproduces Brief 26 bit-for-bit (call-equality + one
measured rerun; stop before any grid if it fails); anchors bit-identical (no fingerprint
move expected — no code edit); gate in background/detached ONLY (the 600 s foreground
harness limit killed two runs yesterday); **no value adopted — neither width nor
z_shallow**; observations beside.

**Out of scope**: (a) re-grounding the cap; Howard+ 2025; the silicate melting curve.

**Brief 27 probe verdict (2026-09-01)**: branch ⑤ — all three probes conv=False,
surface pinned 120.6–123.2 K vs 76 K; wall = deep h_he window floor (~1055 GPa ·
2309–2340 K, spy 35 refusals; mechanism and the 10⁻⁵-weight evidence-gate observation
in context notes §6). Identity rerun matched the Brief 26 grid in every printed digit;
mass conservation within 0.0008. Grid NOT run; nothing adopted.
