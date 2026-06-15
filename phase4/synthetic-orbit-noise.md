<!-- Phase 4 정책: '완벽한' 기본/가정 궤도값(0·90·정수·e=0)에 물리적 가드레일 안에서 seeded 노이즈를 줘 현실성·다양성을 부여. 측정값 불변, DB 불변, 안정성 게이트. -->
# Phase 4 — Synthetic Orbital Noise (de-perfecting default elements)

**Status:** spec / backlog. Phase 4 not yet built. Generalizes the earlier
synthetic-eccentricity idea to all suspiciously-perfect orbital elements.

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
2. **DB invariant.** Noise is applied in the Phase-4 / cfg-emit layer, never written
   back to `db/`. The measured DB stays the source of truth; the build is reproducible.
3. **Re-rollable, never baked.** The noise is a re-rollable *realization*, not a single
   fixed value frozen into the spec or DB. It's drawn from a seed: a given seed
   reproduces a given build (a committed release stays deterministic, so diffs/freshness
   checks still hold), but **the seed is a free knob** — bump / re-roll it and every
   noised element lands on a *different* valid value inside the same guardrails (and must
   re-pass the stability gate). So the values vary roll-to-roll; they are never locked to
   one set. (The seed is recorded with the build for reproducibility; re-rolling = change
   the recorded seed. If a future build wants fresh noise every run instead, the
   build-freshness check must exempt the noised emit — tradeoff noted.)
4. **Physically bounded** (below). Noise must stay inside the Phase-3 defensible
   window AND inside any observational constraint the body still has to satisfy.
5. **Stability-gated.** After perturbing a multi-body system, run the stability sim
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
- Ties into [[project_nearstars_phase4]] (the art-direction → 고증-gate → emit flow):
  synthetic noise is one of the deterministic transforms the Phase-4 emit applies, and
  the stability sim is its 고증 gate.
