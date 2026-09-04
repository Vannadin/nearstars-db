<!-- AQUA region-5 격자를 h2o_hot 1–100 GPa 에 치환해도 해왕성 열린-창 기둥의 PhaseGap 거절점이 비트 동일함을 잰 병렬석 기록 — 사전등록 + 결과 + 정정, 원문 무편집 -->
<!-- Landed 2026-09-04 from the parallel seat's scratch (files PRE-REGISTRATION.md 18:13:53 · REPORT.md 18:19:14 · correction section 18:26:53 KST), merged into one file, pre-registration first, body unedited. This is the report that superionic-ceiling-context-notes.md §5's addendum (dd40c301) says lives "in the parallel seat's scratch, not the repository" — it landed as this file. Line numbers quoted inside refer to the engine worktree's docs/ copies at 839b2c7c. -->

# Pre-registration — AQUA(region 5 = Brown 2018) grid substitution into h2o_hot, 1-100 GPa

Written BEFORE any measurement or any reading of a result. Parallel seat (Opus 5, 1M),
brief from nearstars-77, owner-approved 2026-09-04 afternoon.

## This is NOT a fill from AQUA
`superionic-ceiling-context-notes.md` §5 outcome Ⓡ instructs that nothing be filled from AQUA.
This measurement does not fill anything: it is a **sensitivity measurement of a grid choice**,
run entirely in a scratch copy. No engine value is adopted, nothing is committed, no anchor moves.
Whatever the result, it is not a decision to admit AQUA into the engine.

## Question (one sentence)
If `h2o_hot`'s (whole-region Mazevet 2019) 1-100 GPa interval is replaced by AQUA's corresponding
region (region 5 = Brown 2018), does the open-window Neptune column's FIRST CONTACT with ice_x's
1800 K ceiling change in depth/pressure?

## Distance between the substituted interval and the contact point
Substitution interval: 1-100 GPa. Printed contact point (§5): 923.6 GPa · 1800 K.
Three orders of magnitude apart. What is asked is an INDIRECT effect via the upstream column.
**"No change" is registered in advance as a valid result.**

## Thresholds (verdict is drawn from these alone)
- Ⓐ |ΔP_contact| < 1 % AND contact still occurs  -> downstream insensitive.
- Ⓑ contact still occurs but |ΔP_contact| >= 1 % -> indirect path real; report magnitude.
- Ⓒ contact disappears (1800 K ceiling not reached) OR a new refusal fires at a different wall
      -> report the wall's name and location.
- Ⓓ the substitution itself fails (outside grid domain / phase mismatch / a mask refusal keeps the
      column from traversing that interval) -> report the failure point; NO verdict.

Observations outside the thresholds are reported only as "printed facts placed side by side" —
no causal claims.

## Baseline gate
The baseline must reproduce 923.6 GPa · 1800 K first contact in the scratch copy before any
substitution is run. If it does not, stop and report. Time limit: if baseline reproduction does
not succeed within 10 minutes, report in whatever state it is in.

## Also to be printed
- Discontinuity at the seam: relative difference of the two densities at 100 GPa.
- Whether the substitution wrapper's column passes through the ~1514 K isotherm band
  (the non-converging oddity) — flag the fact only, no cause sought.

## Discipline
PYTHONDONTWRITEBYTECODE=1; worktree imports are read-only; no bibcode guessing; AQUA paper
sentences, if quoted, carry § / line numbers.

---

# Result — AQUA region 5 (Brown 2018) substitution into h2o_hot, 1-100 GPa

Parallel seat, 2026-09-04. Pre-registration: `PRE-REGISTRATION.md`, written **18:13:53 KST**
before any measurement. Scratch only; the engine worktree is clean (`git status --porcelain`
empty, HEAD 839b2c7c unchanged).

## Verdict: Ⓐ — downstream insensitive

First contact with ice_x's 1800 K ceiling is **bit-identical** in baseline and both
substitution variants:

    923611756890.3204 Pa  ·  1801.0133587468536 K   (printed rounded: 923.6118 GPa · 1800 K)

|ΔP_contact| = 0 exactly, contact still occurs, same refusal, same material (`h2o`), same
message. Threshold Ⓐ ( |ΔP| < 1 % and contact unchanged ) is met at the strongest possible
margin.

## What was run

| run | contact (P, T) | h2o_hot density calls | of those replaced by AQUA |
|---|---|---|---|
| baseline (window open, no substitution) | 923.6118 GPa · 1800 K | 8837 | 0 |
| `region5` (replace only where AQUA's phase flag = 5) | 923.6118 GPa · 1800 K | — | 2425 ρ, 346 γ |
| `wholeband` (replace across all 1-100 GPa) | 923.6118 GPa · 1800 K | 8308 | 2937 ρ, 419 γ |

Baseline reproduced the recorded 923.6 GPa · 1800 K in 1 s, first attempt.

## The substitution demonstrably moved the column, and the contact still did not move

This is the load-bearing check — an unchanged answer from an inert wrapper would prove nothing.

- The h2o_hot call sequence **diverges at call index 1533**: baseline `(99.8999 GPa, 1978.1929 K)`
  vs substituted `(99.8967 GPa, 1978.1831 K)` — relative ΔP = −3.14e−5, ΔT = −4.93e−6, and the
  returned density there differs by +6.4 % (2870.25 → 3052.92 kg/m³).
- The **total number of solver calls changes**: 8837 → 8308. The search took a different path.
- The **final call is byte-for-byte the same triple** in both runs.

## The substitution's own facts

- **The interval matches the source's stated validity.** AQUA §2.3.5: *"we use the EoS by Brown
  (2018) for region 5 … appropriate for liquid and supercritical H2O from 1 GPa to 100 GPa and up
  to 10^4 K"*; Table 1 (line 272) lists region 5 = Brown (2018), "liquid & supercritical fluid".
  The column's calls in the band sit at **1.02-99.91 GPa × 1052.53-1979.11 K** — inside that.
- **AQUA does not hand the whole band to region 5.** The grid publishes a *phase* flag, not a
  region id, so region membership is read off the paper's boundaries plus that flag. Of the 3437
  baseline calls in the band, AQUA labels **2578 as flag 5** (1.02-66.5 GPa × 1053-1867 K) and
  **859 as flag −10, ice-X** (66.6-99.9 GPa × 1867-1979 K) — i.e. region 3, French & Redmer 2015,
  not Brown. Hence the two variants; both give the same contact.
- **The 100 GPa seam is not continuous.** AQUA is denser than Mazevet there by **+6.33 %** at
  1800 K and +6.36 % at 1979 K (at 1 GPa: +5.46 % / +4.96 %). γ likewise: at 100 GPa · 1800 K,
  0.46908 (Mazevet) vs 0.68355 (AQUA, from its published ∇_ad · ρw²/P).
- ⚠ **Printed-fact correction to the brief.** The brief said "above 100 GPa the two are identical
  to printed digits". Measured along the T = 1995.26 K grid isotherm, they are **not**: +6.33 % at
  100 GPa, crossing zero at ≈228 GPa, −2.1 % at 317 GPa, and only from **≈722 GPa** onward do they
  agree to ≈1e−5 (0.0009 %). That threshold is the paper's own: §2.3.3 — *"for pressures above 700
  GPa we use the M19-EoS"*. The contact point (923.6 GPa) lies inside the identical zone, so
  `superionic-ceiling-context-notes.md` §5's "its region is M19, the same source as h2o_hot" holds
  for the contact; it is the 100-700 GPa stretch that is a different source.

## Bonus — the 1514 K isotherm

Both columns pass through it, at different pressures: baseline 28 calls at 11.49-12.06 GPa ·
1510.3-1517.4 K; substituted 28 calls at 26.31-27.09 GPa · 1511.1-1517.4 K. Fact only; no cause
sought.

## Scope note (as pre-registered)

This was a sensitivity measurement of a grid choice, not a fill from AQUA (§5 Ⓡ). Nothing was
adopted, no anchor moved, no commit made. What is substituted is `HotWater.density` and
`HotWater.gruneisen`; `_thermal` / `grad_ad` / `c_p` stay Mazevet (their own docstring says the
integrator's adiabatic slope is assembled from `gruneisen` and a numeric K_S, and `c_p` is used
only by `Mixture`).

## Files

`PRE-REGISTRATION.md`, `engine_copy/` (worktree copy at 839b2c7c + one added line
`column_steam_allowed = True` after `interior.py:521`), `neptune_open.py` (from the previous
seat's scratch), `baseline.log`, `spy.py`/`spy.log`, `extract_aqua.py`/`aqua_band.npz`,
`aqua_grid.py`, `phase_census.py`, `seam.py`, `above100.py`, `substitute.py`/`subst.log`,
`traj.py`/`traj_base.json`/`traj_sub.json`.

---

# ⚠ Dated correction — 2026-09-04, added after the audit seat's catch

**Nothing above is deleted.** What changes is a *label*, and the verdict Ⓐ survives.

**What was wrong.** Every "first contact `923611756890.3204 Pa · 1801.0133587468536 K`" in the
report above is `traj_base.json[-1]` — the **last `h2o_hot` density call**, not the ice_x
`PhaseGap` refusal point. They are different objects and differ by 366 Pa in pressure and
1.01 K in temperature. The audit seat caught it; §5:127 of
`superionic-ceiling-context-notes.md` had already printed the constraint ("t > 1800 by less
than 0.5 K"), which the 1801.01 K number violates — that sentence is what makes the mislabel
visible.

**The actual refusal point**, read by hooking `eos.PhaseGap.__init__` (so the numbers are the
constructor's own arguments, not a formatted message):

| run | material | P [Pa] | T [K] | too_cold |
|---|---|---|---|---|
| baseline | `h2o` | `923611757256.9896` | `1800.0000005870497` | False |
| region5 | `h2o` | `923611757256.9896` | `1800.0000005870497` | False |
| wholeband | `h2o` | `923611757256.9896` | `1800.0000005870497` | False |

These reproduce the audit seat's values exactly, and they satisfy §5:127 (`t − 1800 =
5.87e−7 K`, far under 0.5 K).

**All three runs construct exactly 7 `PhaseGap`s, and all 7 are byte-identical across the
three modes** (`json.dumps` comparison) — five `too_cold` walls at 1494–1507 GPa · 138–905 K,
one `too_cold` wall at 20.59 GPa · 745.6 K, and the ceiling refusal above. So the
substitution changes the h2o_hot call path (index-1533 divergence, 8837 → 8308 calls, both
still true) without moving any refusal the solve produces.

**Verdict unchanged: Ⓐ.** |ΔP_refusal| = 0 exactly, on the correctly-identified object.

**Terminology fix for the report above:** read every "first contact (P, T)" as "**last
`h2o_hot` density call (P, T)**". The refusal point is only the table in this section.

Correction section written 2026-09-04; hook script `refusal_hook.py`, logs `refusal.log`,
raw constructor arguments `gaps_baseline.json` / `gaps_region5.json` / `gaps_wholeband.json`.
