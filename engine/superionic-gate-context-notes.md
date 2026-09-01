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
| V2 refuse at >355 GPa | **1** (first touch kills the trial) | exactly 0 |
| V3 refuse at >520 GPa | **1** | exactly 0 |

The zero was validated by the fire counters (a null result must prove the instrument
fired). Mechanism read off the counters: the region-walking trials are value-insensitive
(1,754 perturbed evaluations change nothing) and dispensable (killing them at first
touch changes nothing — first-touch death and full-walk death are the same signal to
the controller). **The converged solution is independent of the region in both the
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
