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
