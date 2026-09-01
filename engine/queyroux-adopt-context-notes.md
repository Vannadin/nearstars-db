# The melting curve below the kink — context notes (Brief 33)

2026-09-01. Registration `queyroux-adopt-checklist.md` (d14e665e); both registered
elections were superseded by the owner's resolution (e9343d5d), recorded there.

## §1 What the dispatch now is

- **[VI–VII boundary, 14.6 GPa]**: the unweighted mean of Queyroux+ 2020 (Table I lower
  Simon–Glatzel; typeset-verified) and Prakapenka+ 2021 (Supp. Table 3 ice-VII segment;
  P = P₀ + a[(T/T₀)ⁿ−1] inverted). NOT named "Queyroux adopted": *the mean of the two
  post-2020 melting measurements below the kink, both anchored on Datchi's
  VI–VII–fluid triple point.* Label conditions (all in `eos.py` at the constants):
  shared anchor → the 1.0 K at 8.2 GPa is never independent confirmation (the
  independent number is 8.7 K at 20.0 GPa); uncertainty = the curves' separation
  (≤54 K) beside each σ, never σ/√2; below 8.4 GPa = anchored interpolation, not
  measurement. Handover step at our IAPWS VI–VII triple point (2.216 GPa): **+4.1 K**,
  recorded not smoothed.
- **(14.6, 20.6] GPa**: named disputed refusal — the sources agree numerically but
  assign different phases (Queyroux on VII′ from 14.6; Prakapenka on VII to its own
  17.5 GPa break) and the dispatch consumes the phase. Verdicts are still given
  outside the candidates' temperature envelope (below IAPWS eq. (5) = all-solid; above
  Queyroux's upper fit = all-liquid); inside, PhaseGap(too_cold=True — hotter exits
  into agreed-liquid) naming the dispute. Zero roster reach, measured: ice-giant
  column tops 34.5/39.2 GPa, all moon calls < 8.4 GPa.
- **Above 20.6 GPa**: unchanged (Reinhardt+ 2022; the upper election was not taken —
  the four-voice spread is the recorded reason: Queyroux coldest, Kimura with
  Reinhardt, Prakapenka +336…+1234 K above Queyroux, upper coefficients ±63 %/±46 %).

## §2 The measurements that fed the resolution

Seam table at 20.6 GPa exactly: neither +188 K (old); lower-only −171 K (sign
inverted); both → seam moves to 44.7 GPa (+293 K fit / +239 K point). Printed-fit
residuals vs Table S1: lower branch all five points within 2σ (worst −1.5σ); upper
fit fails at 15.1 GPa (−2.8σ) — out of adopted scope, recorded as one reason 14.6 is
the boundary. Adopted-mean residuals vs the five kink-below points: +1.1σ, +0.2σ,
−0.7σ, −0.95σ, −2.3σ (at 14.6 GPa; |Δ| 23.4 K vs separation 16 K + 2σ 20 K — inside
the label's carried uncertainty, and the mean is not a fit). The banned corner numbers
(782/2188 K) were not used anywhere.

## §3 Identity and consumers

Anchors re-solved on the new dispatch: **U and N bit-identical** (λ, R, P_c, T_c all
equal to the frozen anchor; conv=True) — the strengthened expectation held. Moon-range
behaviour (< 8.4 GPa) changes only in curve VALUE (mean vs IAPWS, +69…+79 K at
8.4–8.8 GPa), far below any cold moon adiabat's crossing; the gate's moon checks are
the regression. Tests rewritten where they consumed the old dispatch: the IAPWS
eq. (5) transcription check now inverts eq. (5) directly (the standard's own
verification stays the standard's); the S1 residual record recomputes the historical
IAPWS/Reinhardt facts from the sources directly; new checks pin the adopted geometry
(mean(14.6)=829.6 K, disputed band refuses inside its envelope and verdicts outside,
Reinhardt(20.6)=903.3 K) and the mean-vs-S1 coverage under the label's uncertainty.
`water_phase_name` prose names the mean and the disputed band. C3 row: revisited
paragraph (grade reason rewritten, F4's park closed); methodology doc en+ko gained the
Brief-33 paragraph. VII′/VII″ phase labels: **unchanged** — the VII′–VII″ boundary
stays Reinhardt's line; no printed phase label changed except the disputed band's
undecided prose, which now names the dispute instead of "curve does not reach".
