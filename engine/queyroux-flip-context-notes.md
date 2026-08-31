# Queyroux melting line — does any phase verdict actually flip? — context notes

2026-08-31. Directing-session task after F4; the owner chose "measure before adopting".
**An uncommitted experiment**: a detached worktree at `73cac7b2`
(`NearStars-wt/queyroux-melt-exp`), the patch applied only there, deleted after the
measurement. Measured, not judged — whether Queyroux becomes a melting-curve source is the
owner's decision, and this note is the input to it.

## §1 The temporary curve, declared

`water_t_melt` / `water_liquid_at` return, **only inside 8.4–44.7 GPa** (the span of
Queyroux+ 2020 Table S1's twelve measured points), a linear interpolation through those
points; the two points at 16.6 GPa (930 and 944 K) are averaged to 937 K. Outside the
window the dispatch is untouched (IAPWS branches below, Reinhardt's liquid line above).
The window edges therefore carry steps — **+69 K** at 8.4 GPa (ours 591.4 → 660 K) and
**−239 K** at 44.7 GPa (ours 1731.0 → 1492 K; an earlier draft wrote 1734, which was a
44.8 GPa evaluation transcribed as the boundary value — corrected after audit). An adopted
curve would need a joining rule, but for a flip test the steps only matter if a body's
column sits inside a step's span, and none does (§3). Units, for whoever reconstructs the
patch from this section: `water_t_melt` and `water_liquid_at` take pressure in **Pa** —
the window guard is `8.4e9 <= p <= 44.7e9` — and a GPa-valued argument lands every call on
the ice Ih branch (~273 K).

Curve fingerprint (from the runner, both runs):

| GPa | ours (baseline) | Queyroux window (experiment) |
|---|---|---|
| 8.4 | 591 K | 660 K |
| 12.5 | 641 K | 790 K |
| 17.3 | 681 K | 978 K |
| 20.0 | 705 K | 1032 K |
| 27.0 | 1159 K | 1172 K |
| 36.7 | 1470 K | 1310 K |
| 44.7 | 1731 K | 1492 K |

Direction, worth stating because it is not one-sided: inside 8.4–20.6 GPa (the IAPWS reach)
the Queyroux line is **hotter** by up to +297 K at 17.3 GPa (liquid → solid is the possible
flip); above ~30 GPa it is **colder** than Reinhardt's simulated line by up to −242 K
(solid → liquid would be the flip) — the same family split F4 recorded.

## §2 What was run

The runner (`exp_queyroux.py`, lives only in the worktree) solves the five icy anchors the
gate uses (two-layer inference + three-layer with the published C/MR², 270 K potential
temperature — the same calls as `test_interior.icy_table`) and the two ice giants (the same
solve as `test_ice_giant`), and records every phase-relevant output: regimes, bands,
narrowed compositions, ocean/shell thicknesses, ice-column notes with the (P, T) the phase
calls were made at, radius, C/MR², convergence. Once at HEAD, once with the patch; the two
JSONs are diffed.

## §3 Result: no *physical* verdict flips — but Neptune's solve does not survive the route

The diff of the two sweeps, in full:

- **The five moons: bit-identical.** Every field — regimes, two-layer C/MR², three-layer
  bands, narrowed compositions, ocean/shell thicknesses, ice-column notes with their (P, T)
  and margins — is unchanged to the last bit.
- **Uranus: solution bit-identical; only the margin words move.** Radius 4.198853465500676,
  C/MR² 0.1740800202106067 both unchanged. The column-top note changes from "melting point
  1395 K, +1268 K above" to "1278 K, +1385 K above" — the same `molten`, further from the
  line.
- **Neptune: converged → REFUSED.** Under the Queyroux window the full solve dies in 1.4 s:
  *"적분이 실패했다 — 이 질량을 담으려면 중심압을 1269 GPa 위로 올려야 하는데, 그러면
  바깥의 h2o 층이 근거 구간을 벗어난다 (그 층 바닥이 1000 GPa)"* — the **solid** ice
  ladder's French & Redmer 2015 evidence span (1000 GPa) exceeded.
- **The flip is the solver's route, not the physics.** A standalone integration at Neptune's
  frozen convergence point (P_c 1533.2 GPa · T_c 6295.5 K) under the patch reproduces the
  baseline structure **bit-identically** (radius, C/MR², surface temperature all repr-equal
  to the anchor). The converged column crosses the window at 39.2 GPa · 2553 K — +1186 K
  above even the Queyroux line — so the converged verdict cannot depend on the curve choice.
  What breaks is the shoot's *trial* path: a colder intermediate trial dips under the
  hotter Queyroux line inside the window, gets classified solid, walks the solid ladder to
  depths the ladder's evidence does not reach, and the mass shoot refuses before the
  temperature loop can climb out. Under our curve the same trial was liquid and passed
  through. (Same mechanism family as C11's over-broad refusal and the F2-era trial-path
  refusals: the trial corridor is narrower than the answer.)

The geometry that decides the physics side, from the baseline's own numbers:

- **The five moons never ask the question.** The deepest pressure any moon solve reaches is
  Ganymede's **central** 8.27 GPa (the three-layer inversion narrowed by the published
  C/MR², `core_pressure` 8.269; the two-layer inversion's centre is 6.83 GPa — either
  variant sits below 8.4) — 0.13 GPa below the window's floor, and that is rock/iron,
  not water; Ganymede's ice-column base is 1.62 GPa (ice VI, 308 K), Callisto's and Titan's
  centers are ≈5.5 GPa, Europa's ice base is 0.18 GPa, Enceladus is 0.03 GPa-scale. Every
  phase call the moon solves make lands below 8.4 GPa, where the patch changes nothing by
  construction.
- **The ice giants cross the window, but a kilokelvin above either curve.** Uranus's ice
  column tops out at 34.5 GPa · 2663 K — +1268 K above our curve (1395 K), +1385 K above
  the Queyroux line (1278 K; the engine-printed strings, same as §3's diff bullet). Neptune: 39.2 GPa · 2553 K — +999 K above ours (1554 K),
  +1186 K above Queyroux (1367 K). Both stay `molten` under either curve; below ~52 GPa the
  column leaves every curve's reach and the verdict ("fluid or superionic", undecided by
  name) never depended on the disputed band.

## §4 What this says for the adoption decision (measured; the decision is the owner's)

For the current roster the choice of melting curve in 8.4–44.7 GPa **selects no different
converged physics** — the moons live below the window and the ice giants' converged columns
pass through it ≥ 999 K on the liquid side of either curve. Where a physical flip would
start to matter, measured from the margins: a body whose water column crosses
~8.4–20.6 GPa within ≈300 K of our curve, or 30–45 GPa within ≈240 K — neither exists in
the roster today.

**But adopting the line as-is would break Neptune's solve.** *(Discharged 2026-08-31,
Brief 22: the cold-flank repair landed, and Neptune under the window patch + fix converges
to the anchor's own solution in 79 s — `cold-flank-context-notes.md` §3. The two remaining
costs below stand.)* The refusal above is a
prerequisite, not a verdict: before Queyroux (or any hotter in-band line) could be adopted,
the shoot's trial routing would need to survive a solid classification inside the window —
e.g. the solid-ladder over-depth refusal thrown as a too-cold PhaseGap so the temperature
loop raises the trial instead of the solve dying. That is solver work, measured here at one
body's cost; whether it is worth doing is part of the adoption decision. Two more items an
adoption would owe: a joining rule at the window edges (+69 K step at 8.4 GPa, −239 K at
44.7 GPa against Reinhardt), and F4's grade reasoning moving from "the check cannot see"
to a curve the measurements support. None of this is done here; nothing is committed from
the experiment worktree, which is deleted.
