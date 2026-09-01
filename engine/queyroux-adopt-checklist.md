# Adopt Queyroux+ 2020's melting curve — checklist (Brief 33)

Registered 2026-09-01, before any computation beyond what prior notes already hold.
Brief: directing seat's brief-33 (new cb session). Read-first done: queyroux-flip /
queyroux-seam / prakapenka notes, survey ③, C3.

**What this is**: a NAMED CHOICE OF LINEAGE, not an error repair. Queyroux+ 2020
(2020PhRvL.125s5501Q) = the discontinuous/kinked lineage (triple point 14.6(5) GPa ·
850(20) K, two Simon–Glatzel branches, VII′/VII″ structure). Rescigno+ 2025 (Nature
640, 662) defends the continuous lineage, and Datchi stands on both sides of the
record. **Every landed number carries: "adopted from the discontinuous lineage; the
continuous lineage is defended in 2025 and named in the record."**

**Source, verified against the typeset page** (Table I, p. 195501-3):
T_m(P) = T_t·[(P − P_t)/a + 1]^(1/b);
lower (P ≤ 14.6): a 1.555(14) · b 2.557(14) · P_t 2.17 · T_t 354.8 (VI–VII–fluid
triple point from Ref. [21] = Datchi+ 2000 — the anchor is printed IN the table, so
the fit's construction reaches 2.17 GPa);
upper (P ≥ 14.6): a 3.44(216) · b 4.33(200) · P_t 14.6 · T_t 850.
Melting DATA = Table S1's twelve rows (already transcribed in test_interior.py — reuse).
**Banned numbers**: 782 K @20 GPa and 2188 K @44 GPa are corner-run artifacts of
correlated coefficients and are NEVER quoted as Queyroux's uncertainty. **Isostructural
trap**: 15.6(2) GPa·905 K and 18.4(9) GPa·944 K are the VII″→VII′ solid transition,
not melting points. **eq. (2) is Kimura 2023's fit** anchored on Queyroux's triple
point — every equation label carries its paper's name.

**Fit-selection criterion, written before the residuals are seen**: the printed fit is
adoptable over a range iff its residual against every Table S1 measured point in that
range is within **2× the printed σ_T** of that point; otherwise the fit fails there
and only branch handovers at measured edges remain.

**Joining principle, chosen before any seam value is computed**: hand over from IAPWS
to Queyroux at **the ice VI–VII phase boundary** (our dispatch's IAPWS VI–VII–liquid
triple point) — the phase changes there anyway and Queyroux's lower branch is pinned
to Datchi's VI–VII–fluid triple point printed in Table I. The mismatch between our
IAPWS triple point and Datchi's (2.17 GPa · 354.8 K) is measured and recorded as the
handover step, not tuned away. Fallbacks stay as briefed (measured window edges with
the step recorded; declared blend). Any step any principle yields is recorded — three
items in a row declined to write the value that would close their gap; this one too.

**Order**: ① seam table at 20.6 GPa EXACTLY under all three combinations
(neither / lower-only / both), plus the 44.7 GPa edge for "both" — BEFORE electing.
② residual table of the printed fits vs the twelve points (criterion above).
③ two separately-labelled elections (declining one half with the four-voice spread as
its reason is a legitimate ending and does not block the other). ④ implement; identity
per the flip test — **five moons bit-identical, Uranus solution bit-identical (only
column-top margin words may move), Neptune converged**; any solution movement STOPS
the brief and is traced. ⑤ downstream prose: C3's grade reason rewritten (not just
re-graded), F4's park line closed, every moved prose number fixed or dated
*superseded*, phase-label changes stated explicitly. ⑥ gate backgrounded, log-tail
watched, measured delta reported.

**Outcomes, five**: ① both elected → success with dissenting voices named beside each
(Kimura, Prakapenka, Rescigno). ② lower elected, upper declined (expected) → upper
closes as a named refusal with the spread as reason; the seam table says what that
costs. ③ an anchor or verdict moves → UNEXPECTED, trace and stop. ④ joining rule
cannot be declared without tuning → park with the step measured. ⑤ outside → name it,
extend the register, record the kind.

**Hard constraints**: gate FAIL 0 backgrounded; no new runtime dependency; commits
English, one logical change; `git diff --stat` before `git add`; --refresh only if a
fingerprinted function/constant changes, same commit, cause stated.
