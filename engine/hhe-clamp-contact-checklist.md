# Do our integrations read the clamped nodes? — checklist (Brief 30)

Registered 2026-09-01, before any instrumentation runs. Basis: Brief 29's finding —
70 pressed (0.1-clamp) grad_ad cells above the reach line, a coherent block at
≈18–112 GPa × 1585–3981 K; the hhe notes' own table puts a 60 K-start adiabat at
≈2371 K through 100 GPa, mid-block. Independent of the (closed) gradient axis: this
touches numbers already published — the anchors, C13's 26 %/41 %, Brief 26's grid.

**Order, registered**:
① **Contact count first.** Instrument (temporary hook, never committed) the baked
   table's grad_ad stencil: at the frozen convergence points, one standalone
   integration per body, count steps whose bicubic stencil contains ≥1 pressed node;
   report the fraction and the (P, T) range of contact steps. Zero → done, recorded.
② Only if nonzero: **propagation, not pointwise** (Brief 28's registered weakness) —
   re-solve with pressed nodes replaced by neighbour-interpolated values via an
   uncommitted hook, and report where radius/λ/T_c go, against the anchor jitter
   3.7–3.9e-4.
③ Not just anchors: the same contact count at the printed convergence points of
   Brief 26's 14 grid solves and C13's end-B four.

**Branches**: ① zero contact → the block never touches our answers; record and close.
② contact, contribution within anchor jitter → answers stand; the fact "we read
clamped values" is still recorded (the next body may differ). ③ contact and the answer
moves → **anchors are contaminated: report the shift and STOP — no quiet fixes, no
--refresh (refreezing on contaminated values is the worst move); owner decides.**
④ contact not instrumentable → legitimate ending; the structure itself is the record.
⑤ outside → name it.

**Hard constraints**: no committed code change (hooks only, in scratch runners);
anchors bit-identical (instrumentation must not perturb); gate in background at
landing; branch ③ freezes all anchor operations pending the owner.

**Verdict (2026-09-01)**: branch ② — contact is real everywhere (anchors 12.1/18.5 %,
rock end B 20.7/26.2 %, ice end B and all 14 grid points 13–20 % of grad_ad reads),
but replacing all 72 clamped nodes with neighbour interpolation moves the re-solved
anchors by Δλ ≤ 4.3e-5 · ΔR ≤ 2.9e-5 (10–40× below the 3.7–3.9e-4 jitter) and
ΔT_c ≤ 3.41e-4 (0.87–0.92× of it — within, flush against the boundary). Answers
stand; the fact that clamped values are read is recorded; no --refresh ran.
Details: hhe-clamp-contact-context-notes.md.
