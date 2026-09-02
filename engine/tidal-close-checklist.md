# Close the tidal axis with its mechanism named — checklist (Brief 37)

Registered 2026-09-02, before work. **Documentation only — no code behaviour, no
anchors (untouched by construction), gate delta 0 (nothing new executes).** Read-first
done: brief-37.md, H14-tidal-axis-verification.md, tidal-interior-context-notes.md §4,
methodology citation block.

The notes record a symptom (the printed system cannot reproduce its own Io result);
this brief writes the **mechanism**, so no later seat re-digs the same paper.

- [x] **A (notes §7 — the three causes, quotes at their place, verifier named)**:
  ① the model is dimensionless by construction (thesis Table 2.1, §5.5, H "dimensionless
  value of 10") and Table 5 is a write-up-time re-dimensionalisation — predicting the
  audit's "no admissible constants"; ② the 2019 paper contradicts itself on T₀
  (§2 "T₀ (= 1)" vs Table 5 "1400 K") and its own eq. (2) misses its own ~8 criterion
  by six orders in both readings; ③ A=15 resolved dimensionless (F-K, ΔT_rh = A⁻¹),
  α recoverable as 3×10⁻⁵ (thesis quoting K&M's own named source + Spencer Table 1 —
  chain stated honestly: read 0 times in the 2019 paper itself) and contradicting the
  audit's unique-root ≈9×10⁻⁷; H's precision and a_u unrecoverable (dimensionless-only /
  figure-only). ③b: the third leg swaps — mountain heights are unsettled
  (Carr+ 1998 "at least 7.6 km"; White+ 2014 albedo caveat; Turtle+ 2001 compression)
  and Khurana+ 2011's induction (≥50 km, ≥20 % melt global layer) + Spencer+ 2020
  (80 % intrusion) say **the model resolves a different structure than the
  observations indicate**.
- [x] **B (methodology doc correction, EN + KO both)**: the citation block's "the
  transport half meets the validation standard" claim is now known unsupported by the
  printed system — corrected in place, old sentence kept and dated (prose carrying a
  number carries the duty).
- [x] **C (label mechanism line)**: tidal_transport.py's failed-io-reproduction label
  comment gains one line naming the cause — comment-only, zero behaviour.
- [x] **D (traps + reopeners + prerequisites)**: Spencer 2021 Table 1's diffusivity
  printed 10⁶ m²/s (dropped minus, same family as the 1336e9 scale); K&M "~1 TW"
  carried; what reopens the axis (a model built for Khurana's structure, or a paper
  that predicts rather than calibrates Io's lid); author-contact question recorded,
  NOT initiated (owner's call): which T₀ entered §6 — dimensionless 1 or 1400 K;
  thermal conductivity named as the first property gap (K&M's constant 4 W/m/K was
  borrowed; Spencer/Moore print none; thesis is dimensionless).

Constraints: labels with location+condition, identifiers read not made, no WebSearch,
commits English, one logical change, `git diff --stat` before add (directing seat
edits interior-core.md / SESSION-HANDOFF.md).

**Verdict (2026-09-02, landed)**: notes §7 carries the three causes with quotes at
their place and verifiers named; the methodology citation block corrected in place
(EN + KO, old reading kept and dated — the KO mirror had never received the ⑧b block,
so it gained a dated summary + the correction together); the runtime label now names
the mechanism in one line; traps (Spencer 10⁶ m²/s, K&M ~1 TW), reopeners, the single
author-contact question (recorded, not initiated), and the conductivity prerequisite
all in §7. Anchors untouched by construction (prose + one label string; the only code
file touched is a note string whose test pins status, not text — test_tidal_transport
re-run green). Gate delta 0: nothing new executes.
