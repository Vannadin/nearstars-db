# The iron-alloy melting depression — corrected premise, then a labelled bound (Brief 38)

Registered 2026-09-02, before work. Anchor for every number: `b6a525cc`. Read-first
done: brief-38.md **§0 before the grounding note**, core-melt-depression-context-notes,
paper-defects.md, SESSION-HANDOFF parked rows cross-checked against `git log`
(obligation done — two stale statements found, reported in the registration report:
the ② row's "≤54 K" superseded at `edf15772` → 16.1 K in-interval; the tidal row's
"Dante has no root" superseded at `086bad3b`/`3b8a9739` → unique root at the canonical
pair).

**The corrected premise (§0)**: Mori+ 2017 measures the Fe–Fe₃S **eutectic** — the
floor of the melting surface at the S-rich composition. Our 0.80 rides `fe_prem`,
Earth's actual (non-eutectic) composition; `0.63 (eutectic) < 0.81 (ours/Sinmyo) <
1.0 (pure Fe)` is a correct ordering, not an error. The Sinmyo+ 2019 ICB check
(5120 ± 390 K) decides it: ours ×0.80 = 5073.7 K at 330 GPa → −0.12 σ; Mori's
eutectic 3992.7 K → −2.56 σ. **The value stays; its provenance gets repaired.**

**Pre-registered branches, five (committed before any run)**
① Transcription reproduces Mori's four printed points; the eutectic stored as a bound;
  labels land; `iron_t_melt` returns unchanged values → adopt.
② Any `test_ice_giant.py` anchor moves → stop and trace. Never absorbed, never
  `--refresh`.
③ The Sinmyo check, **recomputed** rather than read from the prose literal, does not
  come back at ~19 % → the hardcoded number drifted; report the delta and the pressure
  it was computed at before changing anything.
④ The bracket (eutectic ≤ declared ≤ pure Fe) is unfireable for every roster body →
  **C5: do not build it**; report the measurement that killed it (Brief 34's B1 shape).
⑤ Outside the register → land it, record the kind.

**Items**
- [ ] **A (documentation repair, first)**: note §2 + the handoff banner's Brief-38
  line — correction beside the original, never instead of it; the FE_EPS denominator
  trap stays as written. (Plus the two stale handoff statements found by the
  cross-check, fixed with their SHAs.)
- [ ] **B (transcribe from the cached primary)**: Mori eq. (1) (1348 K @ 21 GPa,
  a 36.5(4), c 2.07(1); our exponent 1/c). Four printed checks in the gate test —
  the "~4100 at the ICB" row is a **label detail already adjudicated, not a defect**
  (it sits at ~350 GPa on the paper's own curve). A printed point that does not come
  back = stop; never adjust coefficients.
- [ ] **C (labels + three conditions at the constants)**: S-rich bound (Mori Fig. 6
  ordering; Si/O/C between 0.65 and 1.0) · no nickel · the whole curve hangs on the
  unobtained Fei+ 2000 anchor (the four checks confirm the fit, not the anchor).
  Coverage: measured 21→254 GPa, self-extrapolated ~350; **10–21 GPa covered by
  neither Mori nor Buono → named refusal, never a silent interpolation**.
- [ ] **D (provenance repair, value unmoved)**: eos.py:1427's "Stevenson+ 1983 관례" →
  the real pedigree (Stevenson 1981 ideal-mixing, Boehler 1996 p. 29's "crude
  assumptions" quote; Zhang & Rogers 2022's "artificial"/"fine tune") + what now
  stands under it (a 1981 estimate that a 2019 measurement independently lands on at
  Earth's ICB, −0.12 σ) + the negative finding (Boehler convergence unsupported;
  absolute depression grows, fractional flat — a constant factor is a defensible
  shape).
- [ ] **E (Sinmyo check computed, not asserted)**: core_state.py:209's literal
  "19.1 %" recomputed (directing seat gets 19.3 % at 330 GPa) — computed value +
  a gate test so it cannot drift silently.
- [ ] **F (the bound, only if it fires)**: measure whether any roster body can violate
  eutectic ≤ declared ≤ pure Fe; expected unfireable → branch ④ closes it; the curve
  stays a labelled constant with its conditions.
- [ ] **G (identity + gate)**: full anchor re-solve (not --fast), check.sh backgrounded
  under caffeinate -i, FAIL 0, delta vs 1213 s reported.

**Standing constraints**: do not fit the engine to the roster (Dante is invented; the
−12.5 % was already alloy-equivalent — this brief is not motivated by it); the FE_EPS
denominator; Buono eq. (5) used only as the corrected reading with defect #10 cited;
paper-defects read before transcribing; commits English, one logical change,
`git diff --stat` first.
