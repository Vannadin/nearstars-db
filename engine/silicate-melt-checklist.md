# A silicate melting curve, regime-switched and differentiation-seeded — checklist (Brief 36)

Registered 2026-09-02, before work. Read-first done: brief-36.md, survey ⑫
(H12-silicate-melting-curve.md), survey ⑬ (H13-six-paper-grid.md), eos.py melt
machinery (Phase.melt/melt_scale/melt_ref, t_melt dispatch, c_p identity, grad_ad),
Monteux+ 2016 §2.2 read in the cached primary (eqs 6, 10–13, 14–17, Table 1).

**Hard line**: anchors bit-identical expected — adding a melt curve makes previously
silent phases answerable, so identity is MEASURED (full anchor re-solve, not --fast),
never assumed. Any movement = branch ④, stop and trace.

**Item 0 (OPEN — design question sent to the directing seat before wiring the >20 GPa
window).** The brief's regime table gives 20–500 GPa to the pure-MgSiO₃ single-point
chain (Deng bdg → ppv → Fei upper), while the composition section seeds Monteux's A/F
curves from `differentiated` and validates their +879 K split at 140 GPa — but A/F
differ only ABOVE 20 GPa (eq 13), and below 20 GPa Monteux prints one composition
(HZ96). Read (A): >20 GPa is single-point (window collapses; A/F used only in the seam
measurement; the differentiation link is wired but latent above 20). Read (B): the
rock solidus/liquidus pair (eqs 10–13, A/F seeded) runs to Monteux's fitted range with
Deng/Fei beyond. These give 300–1300 K different curves in 20–160 GPa. Building (A) as
default unless corrected; the >20 GPa wiring lands after the answer.

**Order and items**
- [x] **A (transcribe, from cached primaries only)**: Monteux+ 2016 eqs (6), (10)–(13),
  (15)–(17), ΔH = 4×10⁵ J/kg (Table 1, Ghosh & McSween 1998) — the solidus scale is
  **1.336×10⁹ Pa** (confirmed at its own line in the primary; the 1336×10⁹ secondary
  rendering is the 750-K trap, do not import it). Deng+ 2023 two Simon fits; Fei+ 2021
  upper bound. Labels: quantity, printed location, condition, paper name; Monteux as
  printing source only (survey ⑬ retracted "re-fit for continuity" — the word is not
  in the primary); Herzberg & Zhang 1996 / Andrault+ 2011 / Fiquet+ 2010 as the
  experimental sources.
- [x] **B (transcription checks in the gate test)**: Deng — Table I rows + the printed
  "9376 ± 656 K at 500 GPa" (fit gives 9376.6); Monteux — the three liquidus branches
  meet at 20 GPa within 0.040 K and the solidus join is ~1.0 K with the correct scale
  (745.6 K with the trap scale — pinned as the decimal-point tripwire); Fei evaluated
  at its 140 GPa anchor. **A printed point that does not come back out of its own
  equation = stop and report; never adjust coefficients.**
- [x] **C (the chain)**: regime switch per the owner's table; every seam step measured
  and pinned (20 GPa both compositions; bdg→ppv at the printed triple point 180 GPa,
  +18 K expected, carrying the paper's own inconsistency that the fits cross at
  173.6 GPa; ppv→Fei at 200 GPa measured, plus the 500 GPa +48 K comparison); steps
  labelled as composition/material declarations, never smoothed. Named refusals: above
  500 GPa (nothing transcribable with data), and Deng bdg's arithmetic floor at
  11.89 GPa (a range limit living in the coefficients, not prose — survey ⑬'s (f)).
- [x] **D (the window machinery)**: melt fraction φ = (T−T_sol)/(T_liq−T_sol)
  (Monteux eq. 6, printed — the shape is not our declaration) as the single source of
  truth; apparent heat capacity C′_p = C_p + ΔH/(T_liq−T_sol) (Monteux eq. 17, after
  Solomatov 2007) hooked into the silicate c_p/grad_ad inside the window; nominal
  width for single-point melters (declared, labelled filled-in) so the integrator
  never sees a knife edge. Width from measurement where sol/liq are printed
  separately — state that in the label.
- [x] **E (seeding + verdicts)**: composition variant from `differentiated`
  (peridotitic = melted-and-differentiated residue, chondritic = primitive) — labelled
  as OUR declaration, not the papers' instruction; antigorite `melt` stays empty **as a
  verdict** (dehydration/breakdown, not congruent melting — say so in its comment);
  mgsio3 phases get melt="silicate" + melt_ref labels.
- [ ] **F (measure identity)**: full anchor re-solve (not --fast) + gate FAIL 0
  backgrounded under caffeinate -i, delta vs 1221 s reported. Landing: notes closed,
  report SHAs, residuals, every seam, seeding map, refusals, anchor bits, gate delta.

**Pre-registered outcomes, five (as issued)**: ① all transcribe, chain assembles with
measured steps → report every seam. ② a transcription check fails → stop, report, no
coefficient adjustment. ③ the 20 GPa step differs materially from 306–464 K → trace
which end moved. ④ an anchor moves → UNEXPECTED, stop and trace. ⑤ outside → name it,
record the kind.

**Constraints**: no new runtime dependency; identifiers read not made, checked by
title; no WebSearch; commits English, one logical change, VaNnadin
<vannadin00@gmail.com>; `git diff --stat <file>` before `git add <file>`.


**Amendment (2026-09-02, directing seat's answer to item 0 — original registration
above preserved as the record of what was expected).** The answer is read (B), and the
brief's own regime table violated the brief's own principle (a width-less single point
across 20–160 GPa would have made the whole width a declaration). Corrected chain, as
built: rock (Monteux eqs 10–13, A/F seeded by `differentiated`) to **140 GPa**; the
seam moves from 20 to ~140 GPa and is a **material-kind change** (rock → pure MgSiO₃),
not a composition step; Deng bdg 140–180 (printed triple point; 160–180 is
extrapolation past Table I), ppv 180–200, Fei upper 200–500, refuse above. The 140
boundary is labelled range-unconfirmed (Andrault+ 2011 unobtained; Monteux prints no
number, but its own model exercises the curves at 140 GPa — chosen over Earth-CMB 136
for that reason). The pure-mineral chain above 140 is read as an **upper bound on the
rock solidus** (above it: definitely molten; below it: indeterminate, and the verdict
labels say so). The brief's "+48 K at 500 GPa" was the directing seat's misplaced
quote of the closure comparison; the real 200 GPa seam step is +297 K (their own
reproduction agrees).

**Verdict (2026-09-02, landed)**: chain built and gated (test_silicate_melt.py):
transcription checks all pass (Deng Table I ≤ ±50 K, printed 500 GPa point 9376.6,
Monteux 20 GPa joins 0.040/1.002 K with the 1336e9 trap pinned at 745.6 K); seams
measured on the implemented-curve basis (audit correction 2026-09-02, notes §3):
liquidus +1275.7 (A) / +396.7 (F), solidus +1732.1, then +17.98 / +296.7 / closure
+47.6; refusals named
(500 GPa ceiling, bdg 11.89 GPa arithmetic floor, unknown variant); φ (eq 6) single
source; C′_p (eq 17) + ∇_ad damping in-window (eq 16 printed-but-unadopted, reason in
eos.py); seeding differentiated→peridotitic / undifferentiated & primitive crust→
chondritic (labelled OUR declaration); antigorite's empty melt commented as a verdict.
Earth at 1600 K stays solid-with-61-K-margin (guarded in the test); solve() now
returns silicate_melt_state / silicate_melt_fraction_max.
