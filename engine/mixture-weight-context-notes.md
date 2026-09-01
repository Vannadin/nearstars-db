# Mixture evidence gate vs component weight — context notes (Brief 28)

2026-09-01. Registration: `mixture-weight-checklist.md` (method, branches, and the
not-measured list fixed before the run). Measurement only — no code moved (anchors
--fast pass untouched).

## §1 The measurement

Locus, computed not assumed: the fatal shell of Brief 27's (z_shallow 0.6, w 0.20)
probe is the envelope's bottom shell [0.0543, 0.0839] with z = 0.99999313…, i.e. the
vetoing h_he component carries **w = 6.870×10⁻⁶** of the shell's mass. Grounded spot:
the same pressure as the fatal refusals (1055 GPa) at T = 3300 K — above the h_he
floor (3130 K at 1050 GPa, directing-seat measurement), `in_domain` verified True.
Contribution = relative change in each reported quantity when the h_he part is removed
and the remainder renormalized.

| w (h_he) | Δρ/ρ | Δc_p/c_p | Δ∇_ad/∇_ad |
|---|---|---|---|
| **6.870e-6 (actual)** | −1.18e-5 | +1.46e-5 | −8.9e-6 |
| 1e-5 | −1.72e-5 | +2.12e-5 | −1.30e-5 |
| 1e-4 | −1.72e-4 | +2.12e-4 | −1.30e-4 |
| 1e-3 | −1.71e-3 | +2.12e-3 | −1.30e-3 |

Scale reference: the anchor's own reproduction jitter, 3.7–3.9e-4 (relative radius
under grid doubling 1500→6000, C13's record). Units caveat carried from the register:
pointwise EOS contributions and end-to-end radius jitter are different quantities; the
comparison is a scale reference, not a propagation.

## §2 The verdict — branch ①, with the proportionality as the policy's shape

**At the weight that actually vetoed Brief 27's probes (6.9e-6), every measured
contribution sits 25–30× below the anchor's own jitter** — a veto fired by a component
that cannot move any reported quantity beyond our own reproducibility. Branch ① fires:
the policy proposal gains measured grounds. **Adoption is the owner's**; the gate's
design sentence stands untouched for components that DO contribute.

**The contribution is linear in w to 3–4 digits** (contribution/w constant: −1.716 ρ,
+2.118 c_p, −1.299 ∇_ad — branch ③ does not fire), so the crossover is computable
rather than declared: the largest slope (c_p) meets the anchor jitter at
**w ≈ 3.7e-4 / 2.118 ≈ 1.7e-4**. Below that weight, at this locus, a component's
contribution is smaller than the noise of our own answers; at w = 1e-3 it already
exceeds it (2.1e-3). A threshold, if the owner wants one, therefore has a measured
origin — "components below our own reproducibility" — not an arbitrary exponent.
Slopes are locus-dependent (they are density/heat-capacity contrasts at (P,T)); a
policy would need either the conservative envelope of the slopes or a per-locus check.

## §3 Not measured, restated (from the register)

① The veto's effect on the solver's **search trajectory** — a refusal reroutes trials
regardless of the component's numeric weight; this pointwise measurement cannot see
that, and Brief 27's conv=False is exactly such a trajectory effect. ② The other
weight-blind gates (cold_phases, in_domain, phase names). ③ Interaction with
`_EnvelopeWater`'s internal dispatch. A policy that only softens `p_max` would leave
those untouched — stated so nobody reads §2 as covering them.
