# R3 — SOI cutoff numerical/physics correctness

Research agent: opus. Source head 440310a9 + numerical-methods literature.

## 0. Two reframing facts (change the whole risk calculus)
1. **QT12 is NOT symplectic — it is a symmetric linear multistep method** (`integrators/methods.hpp:1041` `struct QuinlanTremaine1990Order12 : SymmetricLinearMultistep`; integrated by `symmetric_linear_multistep_integrator_body.hpp`, not the symplectic RKN path). The no-drift guarantee comes from **time-reversibility** (force = f(q) only) + symmetric coefficients, not symplecticity. Principia's "conjugate-symplectic" = behaves symplectic via backward-error analysis, but the load-bearing property is reversibility + smoothness of f. **A cutoff must preserve (a) reversibility [position-only force] and (b) smoothness that the order-12 error constant assumes. A cutoff can keep (a) and still destroy (b).**
2. **Two integration paths, one-way coupled**: massive backbone (fixed-step QT12, O(N²), symmetric dual update `ephemeris_body.hpp:1372-1378`, conserves momentum) — dozens of bodies, cheap. Massless vessels (adaptive `FlowWithAdaptiveStep` `ephemeris.hpp:64`, one-way `:1415+`, no feedback to backbone) — cost scales with star count per vessel per substep. **Real payoff is on the vessel path; real risk is on the backbone.**

## 1. Hard-zero energy damage
Truncated potential Φ̃ = −μ/r (r<r_c), 0 (r>r_c) has a step of height **μ/r_c = a_c·r_c** at r_c. Each crossing injects |ΔH̃| = μ/r_c, sign by direction. Backward-error analysis needs smooth f — void across the discontinuity (method has NO order at the shell). M crossings → energy **random walk** √M·μ/r_c = secular drift, the exact pathology QT12 exists to prevent. Per-crossing jump vs QT12's bounded ~1e-12…1e-14 oscillation: even r_c=100·a_sma gives ~2e-2 (2%) step — 8-12 orders larger AND wrong kind (drift not oscillation). **Hard zero disqualifying on the backbone / for bound orbits.**

## 2. Softening
- (i) Hard cutoff: reversible but C⁻¹, error bound void. Rejected.
- (ii) **C¹/C² smooth taper** on the POTENTIAL: Φ̃(r)=Φ(r)·S(r), S=1 for r≤r₀, 0 for r≥r_c. Quintic C² switch `S(x)=1−10x³+15x⁴−6x⁵`, x=(r−r₀)/(r_c−r₀). Φ̃ is a genuine position-only function ⇒ **reversibility + time-symmetry exactly preserved, smooth backward-error Hamiltonian ⇒ no-drift restored** (for the modified system). Compact support ⇒ exactly 0 beyond r_c ⇒ genuinely force-free coasting (the owner's "keep only inertia" intent, achieved cleanly). Residual = static modelling bias (truncated real tail), NOT drift. Cost: a few flops in the shell.
- (iii) **Verlet neighbor list + skin**: orthogonal optimization (which pairs, not the potential). Pair with (ii). Skin+hysteresis (add at r_c, drop at r_c+δ) kills membership chatter.
Ranking: taper > list+skin (neutral, speed) > hard cutoff (worst). **Recommend (ii)⊕(iii).**

## 3. Is the property even needed here?
- **Backbone: protect absolutely.** Drift corrupts every planet's orbit. Payoff of cutoff ~zero (N_celestial dozens). Never hard-zero; if decoupling light-year-apart systems, smooth taper sited absurdly far out only.
- **Vessel/coast: barely matters.** One-way coupling (error non-contagious), path already adaptive (no no-drift claim anyway), interstellar tail genuinely negligible (a_local ~1e-12 m/s² at 0.5 ly). Concern reduces to "no visible kink/velocity glitch" → taper handles it.

## 4. Cutoff placement (principled)
Reject "Hill-sphere multiple" as primary (Hill = satellite stability, not force-negligibility). **Rule: site r₀ where neglected a_cut < the integrator's own error floor at that point.**
- Backbone (fixed h, order p=12): tail ≤ a_local·C(ωh)^p ⇒ r_c pushes VERY far out ⇒ effectively never truncate within a bound system; only between star-system blocks (below round-off) ⇒ **block-diagonal force matrix**. Within a block: full N².
- Vessel: r₀ where a_cut/a_dominant = 10⁻k, **k ≥ 6** (ppm tail); or where tail < adaptive abs-tolerance. + skin δ≈0.05–0.1·r_c + hysteresis.

## 5. Recommendation (concrete)
**No hard zero anywhere feeding the reversible backbone. Smooth compactly-supported potential taper via a skinned neighbor list.**
- **A. Vessel path (primary, low risk)**: neighbor list per vessel (rebuild every few steps), C² quintic switch on potential for shell bodies, exactly 0 beyond r_c. Site r₀ at a_cut/a_dominant=1e-6. Delivers clean coasting + dominant speedup, ~zero risk.
- **B. Backbone (secondary, careful)**: full N² within each bound system; between systems taper inter-block terms to 0 (block-diagonal). **Apply same S(r) symmetrically to both sides** (`ephemeris_body.hpp:1372-1378`) to keep force antisymmetric ⇒ momentum exact. If in doubt skip B — backbone isn't the bottleneck.
- **C. Non-negotiables**: taper the POTENTIAL (derive force from it, don't truncate force independently → non-conservative); symmetric per-pair on backbone; skin+hysteresis; **C² quintic minimum**; validate against `physics/ephemeris_test.cpp` + `astronomy/ksp_system_test.cpp`/`ksp_resonance_test.cpp` for **bounded, non-drifting** energy (acceptance gate).

Owner gives up: ppm static bias on far-field forces (physically negligible). Gains: O(N·k) vessel scaling, block-diagonal backbone, force-free interstellar coasting — keeping the bounded-energy reversible behaviour. A hard zero would forfeit that for a speedup the taper delivers anyway.

## Grounding
QT12 symmetric-multistep `methods.hpp:1041`; symmetric backbone kernel `ephemeris_body.hpp:1347-1410` (dual :1372-1378); massless one-way `:1415+`; fixed vs adaptive `ephemeris.hpp:64`; Jool "stability" = setup patch `stabilize_ksp_body.hpp:33-44`. Lit: Quinlan & Tremaine 1990; Hairer-Lubich-Wanner *Geometric Numerical Integration* ch. XV (symmetric, bounded energy) + ch. IX (backward error needs smooth f); Allen & Tildesley (switching functions, Verlet skin).
