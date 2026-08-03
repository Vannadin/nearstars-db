<!-- Phase 4 정책: '완벽한' 기본/가정 궤도값(0·90·정수·e=0)에 물리적 가드레일 안에서 seeded 노이즈를 줘 현실성·다양성을 부여. 측정값 불변, DB 불변, 안정성 게이트. -->
# Phase 4 — Synthetic Orbital Noise (de-perfecting default elements)

**Status:** spec / backlog. Phase 4 not yet built. Generalizes the earlier
synthetic-eccentricity idea to all suspiciously-perfect orbital elements.

**Scope, widened 2026-08-04 (owner):** the intent is that *every* defaulted value
eventually carries noise, not only orbital elements. The rules below are written per
element because the orbital guardrails are the ones already worked out, but they read
as the general contract: never a measurement, emit-stage only, physically bounded,
and one-sided at a threshold (rule 5). A derived physical value whose cascade other
rows depend on (pressure feeding temperature feeding albedo) is the case rule 5
exists for.

## Why
Where an element was never measured, the pipeline fills a **default**: inclination
0° (face-on) or 90° (edge-on), eccentricity 0, Ω 0, ω 0/90, round integers. Those
exact values look artificial in-game (every RV planet a perfect circle in a perfect
plane). Phase 4 perturbs them with small **seeded** noise so the built systems read
as natural — **without ever touching a real measurement**.

## Hard rules (apply to every element)
1. **Never noise a measurement.** Only perturb a value whose curation method is a
   default/assumption (`predicted`, `assumed_canonical`, null-filled, or an exact
   0/90/0.0 with no source). Measured transit i, RV e, interferometric i★, etc. are
   frozen. (The DB already records method/source — that is the gate.)
2. **DB invariant + emit-stage.** Noise is applied at the **cfg-emit stage** (one of the
   deterministic emit transforms), **NOT at the facet-decision / board stage**, and never
   written back to `db/`. The Phase-4 board records only the *intent* — "this element is a
   default/free value → de-perfect it at emit" — never a concrete noised number. The measured
   DB stays the source of truth; the build is reproducible (`cfg = f(db, phase3, phase4,
   per-system seed)`).
3. **Re-rollable per star system, never baked.** The noise is a re-rollable
   *realization*, not a single fixed value frozen into the spec or DB. It's drawn from a
   **per-system seed** — the seed key is the star system, so each system is an
   independent roll (systems differ from one another) and **re-rolling is scoped to one
   system**: bumping a system's seed gives that system a different valid realization
   (inside the same guardrails, re-passing the stability gate) while every other system
   stays untouched. A given set of per-system seeds reproduces a given build (releases
   stay deterministic / diffs + freshness hold); re-rolling = bump that one system's
   seed. So values vary system-to-system and roll-to-roll, never locked to one set.
   (If a future build wants fresh noise every run, the build-freshness check must exempt
   the noised emit — tradeoff noted.)
4. **Physically bounded** (below). Noise must stay inside the Phase-3 defensible
   window AND inside any observational constraint the body still has to satisfy.
5. **One-sided at a threshold.** A value that sits *on* a physical threshold gets
   noise only in the direction that moves it **away** from that threshold, or is
   excluded from noise entirely. Two-sided jitter on a threshold value does not blur
   a round number, it flips a verdict. This rule generalizes past orbital elements:
   the owner's intent (2026-08-04) is that eventually **every** defaulted value
   carries noise, so the threshold check has to be part of picking any bound, not a
   special case for `i` and `e`.

   Known threshold-adjacent values, first cases:
   - **Proxima Cen b `atmosphere.pressure` = 0.3 bar** sits exactly at the upper edge
     of Joshi 1997's 0.1–0.3 bar night-side collapse band, and the value is itself
     pinned by the CO₂ frost point that buffers the partial pressure. Any jitter is
     **upward only**; downward crosses into atmospheric collapse.
   - **`eccentricity` = 0 (measured)** is not noised at all: Kopernicus'
     `temperatureEccentricityBiasCurve` divides by zero there, and the fix is to
     suppress the curve at emit rather than to jitter a measurement off the trap
     (rule 1 forbids the jitter anyway).

6. **Stability-gated.** After perturbing a multi-body system, run the stability sim
   ([[project_nearstars_stability_sim]]); if it goes unstable (ejection / Hill breach
   / MEGNO chaotic beyond baseline), shrink the amplitude or reseed. **This is the
   "orbit verification before Phase 4" step.** Single isolated planets skip it.

## Per-element guardrails
| element | candidate (when defaulted) | noise bound |
|---|---|---|
| **inclination i** | i = 0 / 90 / null-fill | **transiting system → must keep the transit**: \|i−90°\| ≤ arcsin(R★/a) (impact parameter b<1). e.g. TRAPPIST-1 → ±2.75° (b) … ±0.51° (h); use the per-planet bound. **RV-only (i unconstrained)** → free, BUT in a multi-planet system keep **mutual** inclinations small (σ ≈ 1–3°, near-coplanar) for stability/realism. **Has a disk** → stay near the disk plane (small tilt). |
| **eccentricity e** | e = 0 | small seeded **e ≲ 0.05**, stability-checked; exclude measured e. (the original synthetic-e concept) |
| **arg. of periapsis ω** | ω = 0 / 90 | free 0–360° (orientation; benign while e is small) |
| **long. of ascending node Ω** | Ω = 0 | single planet → free 0–360°. **Multi-planet near-coplanar** → keep ΔΩ small (a common Ω + a few-degree jitter) so mutual inclination stays low. |
| **mean anomaly / phase M** | any default phase | free 0–360° (just where the body is "now"); pure visual variety, no dynamical constraint. |

## Notes
- The inclination bound is the headline: in a transiting system the planet is *known*
  to transit, so any inclination noise must preserve b<1 (a hard, body-specific cap),
  not a flat "±X°". Compute it per planet from R★ and a (and Rp/R★, e, ω for the
  grazing limit b<1+k).
- "Small mutual inclination" for compact multis is both a stability requirement and an
  observational one (they were detected *because* they are flat).
- Amplitude philosophy: large enough to break the perfect-value look, small enough to
  stay inside the Phase-3 window and pass the stability gate.
- **Stage & gate (decided 2026-06-22).** Apply the noise at **emit**, not at the per-facet
  decision stage. The board flags a value as *de-perfect-at-emit*; the emitter realizes the
  concrete value from the per-system seed. The stability gate is satisfied at the **bound**
  level: the per-element guardrails above are set *inside the already-validated stability
  envelope*, so any seeded value within them is safe **without a per-roll re-sim**. Only a
  *new* system (bounds not yet validated) or a re-roll that widens beyond a validated bound
  reruns the stability sim. Rationale: keeps the deterministic-emit invariant + a clean
  decision record + one-place generalized noise logic.
- Ties into [[project_nearstars_phase4]] (the art-direction → 고증-gate → emit flow):
  synthetic noise is one of the deterministic transforms the Phase-4 emit applies, and
  the stability sim is its 고증 gate.
