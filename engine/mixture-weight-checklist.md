# Mixture evidence gate vs component weight — checklist (Brief 28)

Registered 2026-09-01, BEFORE any measurement. Owner cleared both tracks; survey ⑦
(the h_he table itself) runs in a parallel session, independent.

**The question** (from Brief 27's hand-off): the mixture's evidence gate
(`eos.py` `Mixture.p_max` = min over parts with w > 0) lets a ~10⁻⁵-mass-fraction
component veto a state. Is that veto one that could change the answer? Measured as:
*the ungrounded component's actual contribution to the reported quantities, compared
against the anchor's own reproduction jitter* (grid 1500→6000 moved the radius by
3.7–3.9e-4 relative — C13's record). The threshold, if any ever exists, comes from our
own precision, not from a declared number. **The gate's design sentence is not under
attack** ("가장 높은 상한을 쓰면 근거 없는 외삽을 근거 있는 성분 뒤에 숨기게 된다") —
this brief measures, it does not weaken.

**Method, registered**:
- Locus: Brief 27's fatal point — the deepest envelope shell of the (z_shallow 0.6,
  w 0.20) probe; its exact h_he weight computed from `_erf_mean_z` on the bottom shell.
- Grounded spot: same pressure (~1055 GPa), temperature ABOVE the h_he floor
  (3130 K at 1050 GPa, directing-seat measurement) so both mixtures are evaluable —
  T = 3300 K, h_he.in_domain checked before use.
- Quantities, each measured separately (a density-only conclusion is the named failure
  mode): **ρ** (additive volume), **c_p** (mass-weighted), **∇_ad** (c_P-weighted).
  Contribution = relative difference between the mixture with the h_he part at weight w
  and the same mixture with that part removed, remainder renormalized to 1.
- Weight sweep: the actual bottom-shell weight, then 10⁻⁵, 10⁻⁴, 10⁻³ —
  proportionality in w is itself a result.
- Scale reference: the anchor jitter 3.7–3.9e-4 (relative radius). Units caveat stated
  with it: pointwise EOS contributions and end-to-end radius jitter are different
  quantities; the comparison is a scale reference, not a propagation.

**Explicitly NOT measured, named up front**: ① the veto's effect on the solver's
*search trajectory* — a refusal reroutes trials regardless of how small the component's
numeric contribution is, and a pointwise contribution cannot capture that; ② phase-name
/ cold_phases / in_domain effects (equally weight-blind gates); ③ any threshold's
interaction with dispatch switching inside `_EnvelopeWater`.

**Branches, five (directing seat's register)**:
1. contribution < anchor jitter → the veto cannot change the answer; a policy proposal
   gains grounds (adoption is the owner's).
2. contribution > anchor jitter → the current gate is right; brief closes as-is.
3. contribution not ∝ w → additive volume with nonlinear contribution is itself a
   finding; trace why.
4. not measurable (no grounded spot where both mixtures evaluate) → legitimate ending;
   policy can only be declared, and that goes to the owner as such.
5. outside the register → name it.

**Hard constraints**: NO code change (measurement only); anchors bit-identical
(trivially — nothing runs but EOS calls); gate in background/detached at landing.
