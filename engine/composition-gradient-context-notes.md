# Composition gradient Z(x) — context notes (Brief 26)

2026-09-01. Checklist: `composition-gradient-checklist.md` (pre-registered, six
branches). Premise as updated by the ice-axis landing: uniform Z cannot measure the
axis (h_he cold floor), so the gradient is the only remaining path and the wall probe
comes before any grid.

## §1 The three sourced ingredients (all verified against typeset page images)

1. **Profile form — Howard+ 2023 (2302.09082), Eq. 2, the one transcribable closed
   form C5 names:**
       Z(m) = Z₁ + (Z_dilute − Z₁)/2 · [1 − erf((m − m_dilute)/δm_dil)]
   m = normalized mass coordinate; δm_dil = 0.075 in their Jupiter fit (our grid's one
   sourced interior point, provenance caveat: Jupiter/Juno, not an ice giant); Z₁ =
   outer-envelope Z; Z_dilute = the dilute core's maximum Z; the compact core stays
   separate below. Verified against the typeset page (pdftotext drops the erf argument).

2. **Position — Gupta+ 2025 (2407.04685 · 2025ApJ...982L..35G): the H₂–H₂O critical
   curve as a closed form** (Methods Eqs. 4–10, Table 1's six parameters, validity
   750–6000 K × 0.25–2000 GPa; spot check P_c(3000 K) = 27.0 GPa vs the paper's
   "near 30 GPa"). Location only, never width (miscibility-pairs.md rule). Binary-curve
   caveat: bulk x = 0.6 shifts it ~+10 GPa at 3000 K.

3. **Width cap, route A — Vazan & Helled 2020 (1908.10682) §3.3, a printed common
   property of all valid Uranus models:** "the outer 20 % of the planetary radius
   develop a large-scale convection on top of a stratified inner region", the
   convective shell itself metal-rich (Z ≈ 0.6–0.7, all models except two-layer U-1).
   Declared knobs carried with it: a₀ = 0.1, α ∈ [5×10⁻³, 0.5] (their §2.3; the Ledoux
   criterion ∇R > ∇A + ∇X is theirs to evaluate, not ours — see §2).

## §2 What our recipe can and cannot judge (the route-B refusal, stated up front)

Full Ledoux needs ∇R (radiative/conductive gradient). This recipe carries an adiabatic
profile and no heat-transport model, so a self-computed stability verdict would
degenerate (∇_actual = ∇_A makes any ∇X > 0 marginally stable) — route B therefore
refuses by name wherever it would need ∇R, exactly as the radiative–convective boundary
closed in survey ②. What we CAN do without inventing physics: per grid point, report
the gradient region's radial extent and mark whether it respects the Vazan-stable
geometry (stratified region below ~0.8 R, homogeneous convective shell above). The cap
is transcribed geometry, not a stability computation of ours.

## §3 Implementation design (minimal, declared–integrated–reported)

Declaration: `envelope_z_profile` — (z_deep, z_shallow, m_dilute, delta_m_dil, shells).
The envelope's mass span is discretized into `shells` sub-layers at stack build; each
shell gets z_i = Z(m̄_i) by Eq. 2 and becomes the same h_he+H₂O(+rock) mixture part the
uniform envelope already uses. No new EOS, no new material — only the stack's shape.
- **Width-0 identity (the anchor check):** at δm_dil = 0 the erf degenerates to a step
  at m_dilute; shell edges are chosen to include m_dilute exactly, so the built stack
  is layer-for-layer the current layered structure. The check demands bit-identity
  with the layered answer (renorm 0.1937 / 0.2135), through the shell machinery — not
  by short-circuiting around it (the c13 1-ULP lesson: the corridor's boundary must be
  the answer's own path).
- **Shell count** is a resolution knob to report (staircase lesson: boundaries between
  shells are interpolated by the existing layer-boundary interpolation, C13 fix).
- The wall probe (steepest = δm_dil → small, shallowest = Vazan-cap geometry) runs
  before any grid; both conv=False on the h_he floor → branch ⑥, grid not run.


## §4 Measurements so far (probe + the grid's narrow half; compute stopped mid-grid)

**Width-0 identity, both bit-identical** (2026-09-01): the Uranus anchor with a Z≡0
profile equals the anchor in every digit (λ, R, P_c, T_c; 44 s), and a rock-free
ice+H/He body declared as layers vs as a zero-width step profile equals itself the same
way (98 s). The corridor's boundary is the answer's own path (the c13 1-ULP lesson,
honored by construction this time).

**Wall probe — the gradient clears the h_he floor** (registered verdict rule: either
end conv=True → grid proceeds): U w=0.01 → λ 0.174208, renorm 0.1937 (the layered end A
exactly — continuity), conv=True; U w=0.30 → λ 0.207637, renorm 0.2081, radius residual
+0.12 %, T_c 4294 K, conv=True. Why: uniform Z carried heavy material to the surface
and dragged the adiabat under the h_he window's floor; the gradient's shallow envelope
tapers to clean H/He, whose adiabat stays inside — the anchor's own surviving shape.
Brief 23's §4 observation ("a graded profile crosses the wedge with far less water")
was a testable prediction and it held.

**Grid, narrow half done before the compute stop** (6 of 14; values in the checklist):
U/N × {0.01, 0.025, 0.05} all sit at the layered end A's renorm (0.1937/0.2135 to the
fourth digit) — narrow gradients are the layered structure, as continuity demands. The
movement lives in the wide half {0.075, 0.125, 0.20, 0.30}, unmeasured except the
probe's U 0.30. No adoption; observations (N13 P_Voy 0.2300/0.2410) sit beside.

*(landing: the wide half, the shell-sensitivity point, Vazan-geometry conformity per
point, and the gate — resume on the owner's signal only)*

## §5 The grid, complete — the cap's exclusion first, then the table

**The headline, before any number is read as coverage: the widths that move the moment
of inertia are all outside the transcribed stable geometry.** Vazan-geometry conformity
(gradient region m_mid ± 2δm below 0.8 R; measured per point by standalone integration
at the printed convergence point, closure ±1e-3) holds **only at w = 0.01 and 0.025 —
which sit at the layered end A**. Every wider width runs past 0.8 R (w ≥ 0.075 reaches
the surface). If Vazan & Helled's printed geometry is taken as the Ledoux cap (route A),
**the reachable coverage is ~0 % and the 39.7 %/60.0 % spans below are the values of
unreachable points.** Scope of that exclusion, named with it: it is a statement about
THIS declared family — a two-end erf with z_shallow = 0 — while their stable models pair
a wide gradient with a metal-rich homogeneous convective shell (Z ≈ 0.6–0.7) above
0.8 R, a shape this family cannot express. Route B (own Ledoux) stays refused by name
(§2, no ∇R).

All 14 points conv=True (widths registered in the checklist; 32 shells; the second
interrupt's kill was the directing seat's own, mis-aimed at reducing parallelism — their
register). **No width is adopted.** Observations sit beside; nothing was fitted.
Directing-seat integrity sweep over the interrupt-scarred logs: no .py change across the
grid, no duplicates from the kill, renorm recomputed from λ·R at all 14 points with zero
mismatch.

| δm_dil | U renorm | U R resid | N renorm | N R resid |
|---|---|---|---|---|
| 0.01  | 0.1937 | +5.44 % | 0.2135 | +8.90 % |
| 0.025 | 0.1937 | +5.32 % | 0.2136 | +8.78 % |
| 0.05  | 0.1938 | +4.97 % | 0.2137 | +8.37 % |
| 0.075 (Howard) | 0.1941 | +4.27 % | 0.2140 | +7.58 % |
| 0.125 | 0.1951 | +2.19 % | 0.2153 | +5.50 % |
| 0.20  | 0.1991 | +0.33 % | 0.2200 | +3.98 % |
| 0.30  | 0.2081 | +0.12 % | 0.2300 | +4.14 % |
| target (N13 P_Voy) | 0.2300 | — | 0.2410 | — |

**Span, from grid values**: U 0.1937 → 0.2081 = 0.0144 of the 0.0363 deficit = **39.7 %**;
N 0.2135 → 0.2300 = 0.0165 of 0.0275 = **60.0 %**. Monotone in width, no plateau reached
inside the registered grid. (N's 0.2300 at w=0.30 equals U's *target* by digit
coincidence only.)

**The second product — the radius residual collapses on the same axis**: Uranus
+5.44 % → **+0.12 %** (w=0.30), Neptune +8.90 % → +3.98 % (minimum at w=0.20). The
layered anchors carried +5.48/+8.94 % as a known systematic; a wide gradient removes
most of it *without being asked to* — the radius was never a fit target.

*Recorded, not judged (directing-seat observation)*: **Neptune's radius residual is
non-monotone** — it falls to 3.98 % at w=0.20 and rises back to 4.14 % at w=0.30, so its
minimum lies inside the grid, while Uranus falls monotonically to the grid's edge. The
renormalized moment is monotone for both, so the non-monotonicity lives on the radius
axis alone; the two planets behave differently there.

**Shell sensitivity** (U w=0.075, 32 → 64 shells): renorm 0.1941 → 0.1941 (stable at
the printed digit); λ 0.178521 → 0.178240 (−0.16 %). The staircase is not driving the
span.

(The cap's exclusion statement stands at the top of this section — the spans in the
table are read under it.)

## §6 Brief 27 — the family widened to z_shallow > 0, and the probes name a new wall

Registered in the checklist (47e34c7e): owner chose (b) after `728f6f5d` showed the cap
is a family resemblance. No engine edit was needed — Brief 26's erf already makes the
three-part shape — so identity is call-equality, confirmed by a measured rerun of
U w=0.20 (every printed digit equal to the grid log). Mass conservation held by the
declaration mapping (integrated Z mass within 0.0008 of the declared imf0, tail
clipping reported).

**Probe verdict — branch ⑤, named.** All three probes (z_shallow 0.6/0.7 × w 0.20,
0.65 × 0.30; Vazan bracket cited) end **conv=False**: the surface pins at
**120.6–123.2 K against the 76 K boundary condition**. The spy (35 refusals) puts the
wall almost entirely in the **deep h_he band, ~1055 GPa · 2309–2340 K** — the window
floor cb measured at 3130 K (1050 GPa) — with a single low-band sample (163.7 GPa ·
131 K). Reading, recorded with its mechanism: the metal-rich homogeneous top flattens
the upper envelope's mixture adiabat (heavier mean molecular weight), so the same
t_center yields a hotter 1-bar level; reaching 76 K then needs a t_center whose deep
adiabat falls below the h_he window's floor, and the trials die there. **The family
widening moved the failure from "shape outside the cap" (Brief 26) to "boundary
condition unreachable inside the recipe" — Vazan's successful shape, declared here,
cannot land on the declared 1-bar temperature.** Their models do reach it with the
same geometry, but with their own H/He EOS and a thermal-evolution model; ours refuses
at the table's printed floor. The unconverged renorms (0.2023–0.2095) are NOT
measurements (the ice-axis rule: an end that misses the boundary condition is not a
measured end). **No z_shallow adopted, no width adopted; the grid was not run.**

*Evidence-gate observation, recorded for whoever owns it next (C6 family)*: the fatal
refusals fire on the h_he **component of the deepest shells, whose mixture weight
there is ~10⁻⁵** — the mixture's evidence gate asks every part regardless of weight,
so a one-part-in-10⁵ component can veto the state. Whether a weight-thresholded gate
is honest is a materials-policy question, not this brief's.
