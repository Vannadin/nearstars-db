# The ice giants' C/MR² against publication — context notes

2026-08-31. Directing-session task (no core-list number assigned; feeds C5(a)'s
consumer question). The gate reproduced 0.1741 / 0.1799 daily without ever asking whether
those are the right numbers — only the radius had a `published` column.

## §1 What "published" means here, and why choosing a source is itself a judgment

No spacecraft has measured the ice giants' moment of inertia. Every published C/MR² is a
**derived value**: an interior model fitted to the measured gravity field (J₂, J₄ from
Voyager 2 + satellite/ring astrometry, Jacobson 2007/2009) under an **assumed rotation
period**, integrating I from the fitted density profile. Two rotation hypotheses circulate:

- **P_Voy** — Voyager 2 radio periods: Uranus 17.24 h (Desch+ 1986), Neptune 16.11 h
  (Warwick+ 1989). The IAU baseline.
- **P_HAS** — Helled+ 2010's modified periods (16.57 h / 17.46 h), minimizing dynamical
  heights and wind speeds. Both source papers below state that P_Voy is inconsistent with
  the measured shapes, so neither hypothesis is safely "the" answer.

The rotation period moves the published λ by −3.3 % (Uranus, faster) / +6.0 % (Neptune,
slower). That spread is part of the answer and is recorded beside the headline value.

## §2 The two sources, and the normalization trap between them

- **Nettelmann+ 2013** ([2013P&SS...77..143N](https://ui.adsabs.harvard.edu/abs/2013P%26SS...77..143N),
  arXiv:1207.2309), three-layer physical-EOS (LM-R) models. **Footnote 2 prints
  λ = I/(M_p R_mean²) — mean-radius normalization, the same convention as our `nmoi`.**
  P_Voy: Uranus **0.230(1)**, Neptune **0.2410(8)**. P_HAS: 0.2224(1), 0.2555(2).
  (Parenthesis = uncertainty in the last digit; Table 2 representative models print
  0.2296 / 0.2224 / 0.2405 / 0.2555 / 0.2557.)
- **Neuenschwander & Helled 2022** ([2022MNRAS.512.3124N](https://ui.adsabs.harvard.edu/abs/2022MNRAS.512.3124N),
  arXiv:2203.02233), empirical piecewise-polytrope models on ToF 4th order, Table 2
  solution ranges, **normalized to the equatorial radius** (§3.6: MoI = I/(M·a²)):
  P_Voy: Uranus 0.22594–0.22670, Neptune 0.23727–0.23900; P_HAS ("Uranus–"/"Neptune+"):
  0.21919–0.21964, 0.25248–0.25431. Equatorial radii from their Table 1: Uranus 25559 km,
  Neptune 24766 km (P_Voy) / 24787 km (P_HAS).

The two normalizations differ by (a/R_mean)² ≈ 1.6 % (Uranus) / 1.2 % (Neptune) — larger
than either paper's internal band, so quoting the two papers side by side without the
conversion would manufacture a fake disagreement. This is the same trap the Jupiter block
already documents (the fact sheet's 0.254 vs 0.243 at R_eq). After conversion the papers
meet within 0.15 % (worst case Neptune P_HAS, where NH22's converted band starts 0.2559
against N13's 0.2555 — NH22 themselves call the agreement excellent and note their local
optimizer does not cover the whole solution space). The gate recomputes this conversion on
every run as its transcription check; Δ itself carries **no tolerance** — writing it down
is the deliverable.

**Headline column: Nettelmann+ 2013, P_Voy, mean-radius normalization.** Reasons: same
normalizing radius convention as the engine's sphere (we have no equatorial radius),
values with printed uncertainties rather than solution-space edges, and P_Voy is the same
baseline assumption the IAU rotation constants carry. NH22 stands beside it as the
independent empirical check.

## §3 What the comparison measures (frozen 2026-08-30 anchor)

| body | C/MR² derived | published (N13 P_Voy) | Δ | I/(M·R_pub²) | Δ after | vs P_HAS |
|---|---|---|---|---|---|---|
| Uranus | 0.17408 | 0.230(1) | **−24.3 %** | 0.19367 | −15.8 % | −21.7 % |
| Neptune | 0.17992 | 0.2410(8) | **−25.3 %** | 0.21352 | −11.4 % | −29.6 % |

Reading, measured not judged: the R² in the denominator uses the derived radius, which is
+5.48 % / +8.94 % too large, so part of the deficit is the radius error squared
(×1.113 / ×1.187). Renormalizing to the published mean radius (middle columns) removes
that share and leaves **−15.8 % / −11.4 %** that the radius does not explain: at matched
mass and radius the engine's mass distribution is more centrally condensed than the
gravity-fitted profiles. Where that remainder lives (the silicate/ice/envelope split, the
envelope drawn too thick, the missing rotation — every published λ comes from a rotating
figure while the engine's sphere does not spin) is **not analysed here**; the number is
measured and written down.

Consumer note: `body_figure` turns C/MR² into J₂ through Radau–Darwin, so a −24 % C/MR²
enters the figure chain directly. That is the consumer C5(a)'s grading-Z question was
missing — the directing session owns that linkage.

## §4 What was changed, and what was not

Changed: `test_ice_giant.py` (constants block with the investigation, `_published_nmoi`
comparison in both gate paths, `--table` columns), methodology doc en+ko (new block after
the Jupiter MoI block + two citations). Not changed: `interior.py`, the anchor file
(bit-identical; the comparison reads frozen values), the core list (the directing session
decides whether this becomes a row).
