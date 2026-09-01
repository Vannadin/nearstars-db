# Assembled fallback at the clamped nodes — checklist (Brief 31)

Registered 2026-09-01, before wiring. Owner approved; the weight gate stays as-is
(36125a7e — no trace component has ever blocked a legitimate answer). Scope: **grad_ad
only** (the sentinels all sit in trimmed columns; density is untouched).

**The argument**: the table-first rule ("발표된 수를 우리 조립으로 바꿔 적지 않는다")
does not apply at a clamped node — there is no published number there to overwrite,
only a clamp end (exactly 0.1) where a calculation failed. At those nodes only, the
assembled path is the honest alternative: not inventing, but using the other grounded
route we already hold.

**Design, registered**:
- **Node-level repair, bicubic untouched** (the step-level alternative changes more
  answers for no reason): the baked GRAD_AD gets, at import in `hhe_table.py`, a
  repaired copy where each clamped node (0.1 or 0.5 — 0.5 handling included though none
  exist today) is replaced by the assembly **from quantities the table itself
  publishes**: ∇_ad = −(∂lnρ/∂lnT)_P · P/(T·ρ·c_p), with (∂lnρ/∂lnT)_P from the
  density table's finite difference (`dlrho`) and c_p from the C_P table — no grad_ad
  circularity.
- **Pre-measured feasibility**: 66 of 72 nodes assemble (values 0.0012–0.4306, median
  0.087 vs the clamp's 0.1). **6 nodes cannot** — the density table itself has
  (∂lnρ/∂lnT)_P > 0 there (63–89 GPa × 1585 K; 100–112 GPa × 1778 K): no route is
  grounded at those cells, so per the register's own branch logic **they refuse by
  name** (PhaseGap, too_cold=True — it is the cold edge, the temperature machinery may
  steer) when a grad_ad stencil touches them.
- **Who touches the 6, measured before wiring**: nothing published except the two
  widest grid points (U w=0.3: 20 reads; N w=0.3: 175) — anchors, end-Bs, all other
  grid points: 0.

**Identity (the width-0 analogue)**: ① table-diff proof — the repaired table differs
from the published one at exactly the 66 nodes, byte-equal elsewhere, bicubic code
unchanged; ② a body whose stencils avoid all 72 original cells must be bit-identical
(checked via the contact runner + the gate's frozen expectations).

**Order**: wire → identity → re-solve anchors (branch 1/2 verdict; **--refresh only
after the deltas are reported, same commit, with reason**) → re-run the published
suite (rock end B ×2, ice end B ×4, grid ×14) so every printed number gets its
post-repair value beside it, originals kept → contact runner on the repaired table
(anchor contact with remaining clamped cells must be 0) → background gate (log-tail
watch) → land.

**Branches**: ① assembled ≈ clamp, answers barely move → the clamp was conservative;
that is itself an evaluation of it. ② assembled differs and anchors move → report the
shift and its cause, then --refresh in the same commit; the shift is the
reinterpretation width of everything published. ③ assembly fails at a cell → that cell
refuses (measured: 6 such). ④ split by coordinates → written per cell (it is: 66/6).
⑤ outside → name it.

**What this cannot say** (Brief 30's sentence, same kind): the assembled value is not
truth either — this measures how far two grounded routes diverge, not which is closer
to the authors' unpublished calculation.

**Verdict (2026-09-01, landed per directing-seat terms)**: anchors branch ① (within
jitter); the published derived numbers are NOT robust to the table choice — C13's rock
end B flips conv=False (λ −6.9/−5.5 %) and Brief 26's wide half flips too, so
26 %/41 % and 39.7/60.0 % carry the condition "measured on the clamped table".
Controls: repair-off reruns reproduce both bases exactly. Landed as OPT-IN
(`hhe_repair.py`, default path bit-identical, no --refresh); default-table choice is
the owner's, pending. Details: clamp-fallback-context-notes.md.
