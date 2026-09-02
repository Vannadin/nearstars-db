# The superionic gate — context notes (Brief 34)

2026-09-01. Registration: `superionic-gate-checklist.md` (2fbbfffd); resolution:
tolerance + labels, solver untouched, anchors unmoved.

## §1 Item A — the trial corridor walks the region (branch ③, then refined)

Instrumented every `ice_x` evaluation across all seven anchors' FULL solves (spy on the
ladder material's density, phase-checked; caffeinate-wrapped; total 1474 s):

| anchor | ice_x evals | max P | in region (>355 GPa · 0<T<1800 K) | >520 GPa |
|---|---|---|---|---|
| five moons | **0** (deepest call 8 GPa-grade) | — | 0 | 0 |
| Uranus | 21,829 | **535 GPa** | **1,854** | **153** |
| Neptune | 22,024 | 235 GPa | 0 | 0 |

Distribution (full re-record of the U solve): P spreads continuously 355→535 GPa
(261/315/308/308/306/203/153 per bin), T rises 1643→1800 K with P — an adiabat-shaped
single deep walk, NOT a ceiling-pin (≥1799 K only 0.8 %; the directing seat's
wall-riding reading was rejected by this histogram, and the first report's "all at
535 GPa" was a first-6-samples collection artifact, stated as such). Zero isothermal
(t=0) evaluations in the region.

## §2 Item A2 — the answer does not depend on the region (branch ①, strongest form)

Pre-registered variants (copy fixed before running: scratch A2-PREREG.md), run in a
throwaway detached worktree (HEAD 1c824a90, removed after): criteria = "same solution"
within the anchor reproducibility 3.9e-4 — the result beat the criterion:

| variant | hook fired | Δλ / ΔR / ΔT_c |
|---|---|---|
| base control | — | exactly 0 |
| V1 ±5 % density in region | **1,754** | exactly 0 (bit-identical) |
| V2 refuse at >355 GPa | **1–2** (instrument-dependent; all touches bracket-steered — 2026-09-01 amendment below) | exactly 0 |
| V3 refuse at >520 GPa | **1** | exactly 0 |

> *Audit seat's line, landed verbatim (2026-09-02; audit-measured,
> directing-seat-unreproduced):* The V2 fire count is sensitive to the refusal's flavour — an audit replication using too_cold=True counted 2 fires (the steered bracket grazes the region once more), not 1; either way Δ = 0, and the discriminator between "first-contact kill" and a dead instrument is to call the hooked density on a region point **after** the solve and confirm it still raises (audit, 2026-09-02).

The zero was validated by the fire counters (a null result must prove the instrument
fired). Mechanism read off the counters: the region-walking trials are value-insensitive
(1,754 perturbed evaluations change nothing) and dispensable (refusing them changes
nothing — the refusal is caught and steered by the temperature bracket, and the steered
solve converges to the same bits as the full walk; 1–2 region touches depending on the
instrument, amendment below). **The converged solution is independent of the region in both the
value axis and the traversal axis.**

## §3 What the gate asserts now, and the two discarded approaches

**Discarded, with reasons (for whoever reads after a /clear):**
- **B2 as drafted** ("ice_x is never evaluated in the region") — item A refuted the
  premise: it IS evaluated, 1,854 times, in Uranus's trial corridor.
- **B1** (named refusal at the conservative edge ≈375 GPa + cold-flank steering) — A2
  refuted the need: refusing the region changes nothing, so a refusal would add
  machinery whose only consumer provably does not affect the answer (C5).

**Adopted**: the old flat-floor check (`ICE_VII_X_T_MAX < 2000 K` vs MILLOT_SUPERIONIC)
is REMOVED — it asserted a false premise (the published boundary is not flat and
crosses 1800 K in 305–375 GPa) on a falsely attributed number (Millot's abstract
restating refs 6–12). Its replacement is **the perturbation-invariance regression**
(`test_ice_giant._clamp_invariance`, A2's V1+ promoted to the gate: +5 % on the
region's ice_x density, full Uranus re-solve, bit-compare to the frozen anchor).
Promotion chosen over a documented-procedure-only note because it costs +22 s on a
~1205 s gate (2 %) and fails loudly the day a solver change couples the trial
corridor's region values to the answer. **Scope limitation carried at both sites
(eos comment + the check's docstring): this invariance is a measurement about the
current roster's Uranus, not a general guarantee — it reopens if any body's CONVERGED
column enters the region (why C6 stays a standing watch).** `ICE_X_P_MAX` stays
1000 GPa; A2 weakened the case for narrowing (the only consumer is a trial corridor
that does not feed the answer).

## §4 Items C·D

The dead, falsely-labelled constant pair (`SUPERIONIC_MIN_T/_P`) and the live tuple
(`MILLOT_SUPERIONIC`) are all removed; the story lives as prose at `ICE_VII_X_T_MAX`
(attribution corrected: the 100 GPa/2000 K figure is refs 6–12's prediction restated in
Millot's abstract; the paper's 100–400 GPa × 2000–3000 K is its experimental window).
The three ceilings (data ≈355 / stability ≈520 / printed 1000 GPa) stand as one
notation at `ICE_X_P_MAX`, pointing at C6 and the survey notes, with the closure that
the stability boundary's ice-side potential IS what `ice_x` is fitted to.

## §5 Amendment (2026-09-01, Brief 35 follow-up ⑥) — V2's count and its flavor, measured

The audit's own instrumentation counted V2's region touches as **2** against this
file's original **1** ("first touch kills the trial"), and validated its instrument by
throwing region points at the hook post-solve. Replicated here to find the flavor:

- **The `too_cold` flavor is load-bearing.** Re-running V2 (PhaseGap raised from the
  h2o cold-curve density hook in the region) with `too_cold=True`: the temperature
  bracket catches it, raises the trial center temperature ×1.6, and Uranus converges
  **bit-identical to the anchor** — 1 fire at (535.1 GPa, T → 1800⁻ K). With
  `too_cold=False` the same touch escalates to a **whole-body refusal** (Uranus
  inapplicable). A2's V2 completed bit-identical, so its refusal was too_cold-steered;
  the flavor is confirmed, not assumed.
- **The count is a property of the hook point, not the physics.** Under this session's
  hook (cold-curve `density` of h2o) the count is 1 with either region predicate
  (with or without the T < 1800 K bound): the ×1.6-hotter retry re-enters the corridor
  through the **hot-water dispatch**, which the cold-curve hook cannot see. The audit's
  instrument sits where it counts a second, also-steered touch. Both instruments agree
  on Δ = 0.

So the sentence to carry: **1–2 touches, all steered by the too_cold-flavored bracket,
answer unchanged to the bit.** "First-touch death" was one instrument's view of a
steered retry, not a property of the solve.
