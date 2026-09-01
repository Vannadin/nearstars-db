# The superionic gate asserts something false — checklist (Brief 34)

Registered 2026-09-01, before work. Read-first done: superionic-ceiling notes
(83496754), C6's new entry (10aaa54a), French 2016 PROVENANCE. **Label-and-notation
repair, not a physics change. Hard line: `ICE_X_P_MAX` is NOT narrowed** (C5: item A is
the consumer test; narrowing first builds the machine first; C6's standing condition).

**Order and items**
- **A (first — decides the defect's kind; measurement only, no code)**: instrument
  every `ice_x` evaluation across the seven anchor solves (five icy moons + U/N),
  FULL solves, trial paths included — reusing Brief 33's spy shape, not a new tool.
  Record (P, T); ask: any evaluation at P > 355 GPa with T < 1800 K? at P > 520 GPa?
  Branches: ① none in either region → labelling defect; every fix below must be
  bit-identical. ② above 355 but not 520 → the data ceiling has a consumer; name the
  bodies and depth. ③ above 520 → stop the brief and report before touching anything.
  ④ the instrument cannot see trial paths → say so, legitimate ending. ⑤ outside →
  name it; record the kind after.
- **B (what the gate asserts)**: no transcribable boundary exists (French 2016 §IV =
  method only; legitimate not-found, settled) — **never encode a figure-read curve**.
  **B2 (recommended, if A=①)**: the gate asserts a claim about OUR CODE — `ice_x` is
  never evaluated where the published boundary passed below our ceiling — checkable to
  the bit, no coordinates, loud on future re-routing; figure readings ride as the
  documented reason for the region's bounds with their uncertainty. **B1 (only if
  A=②/③)**: named refusal at the conservative reading edge ≈375 GPa, chosen by the
  authors' own bias statement (quantum effects → lower crossing) BEFORE seeing anchor
  effects. **The 29 GPa disagreement is not adjudicated**: the crossing lies in
  305–375 GPa; the conclusion is the same either way; the strong confirmation is the
  maximum (0.7 % T, 5 % P).
- **C (one constant, correct label)**: consolidate the dead `eos.py` pair
  (`SUPERIONIC_MIN_T/_P`, defined never read) and the live test tuple
  (`MILLOT_SUPERIONIC`) into ONE definition living where the check does, labelled as
  what it is: refs 6–12's prediction restated in Millot's abstract, not Millot's
  result; the paper's 100–400 GPa × 2000–3000 K is its experimental window. Dead code
  removal is in scope HERE only (a dead constant with a false label is a trap).
- **D (three ceilings, one notation)**: data ≈355 / stability ≈520 / printed 1000 GPa
  in one place near the refusal path so a refusal can say WHICH ceiling it hit —
  pointing at C6 and the survey notes, not restating in a third voice; carrying the
  closure that the stability boundary's ice-side potential IS what `ice_x` is fitted
  to (French & Redmer 2015 = VII_X_French).

**Hard constraints**: anchors bit-identical expected (any movement stops and is
traced); --refresh only if a fingerprinted function/constant moves, same commit, cause
stated; gate FAIL 0 backgrounded, log-tail watch, **in-log timestamps this run**,
measured delta reported; no new runtime dependency; stage by filename (two seats in
the worktree); commits English, one logical change.

**Verdict (2026-09-01, landed)**: Item A → branch ③ (Uranus's trial corridor walks the
region to 535 GPa: 1,854 evaluations in >355 GPa·<1800 K, 153 above 520; moons 0,
Neptune caps 235 GPa; distribution = adiabat-shaped continuous walk, not a ceiling
pin). Item A2 (directing-seat addendum, throwaway worktree) → branch ①, strongest
form: base/V1±/V2/V3 all BIT-identical, fire counters validating the null (V1 1,754,
V2/V3 first-touch 1). Resolution: tolerance + labels — B1 and B2 both discarded with
reasons (notes §3); old flat check removed; A2's V1+ promoted to the gate as
_clamp_invariance (+22 s); constants consolidated to prose (all copies removed);
three ceilings as one notation; ICE_X_P_MAX untouched. Anchors bit-identical
throughout. Details: superionic-gate-context-notes.md.
