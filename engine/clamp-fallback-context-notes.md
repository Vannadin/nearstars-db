# Assembled fallback at the clamped nodes — context notes (Brief 31)

2026-09-01. Registration: `clamp-fallback-checklist.md`. Landed per the directing
seat's terms: **the default path is unchanged** — `hhe_repair.py` is an OPT-IN
instrument (nothing in the engine imports it; unarmed, every answer is bit-identical
to the clamped table). No `--refresh` ran; the anchors stay frozen on the clamped
table. Which table becomes the default is the owner's decision, pending.

## §1 The instrument

`hhe_repair.py`: importing it rebinds `hhe_table.GRAD_AD` with the 66 assemblable
clamped nodes replaced by ∇_ad = −(∂lnρ/∂lnT)_P·P/(T·ρ·c_p) from the same table's
density derivative and C_P (assembled range 0.0012–0.4306, median 0.087 vs the 0.1
clamp). The 6 cells where the density table itself is unphysical
((∂lnρ/∂lnT)_P ≥ 0: 63–89 GPa × 1585 K, 100–112 GPa × 1778 K) stay unrepaired in
`CLAMP_UNREPAIRED`; armed consumers ask `clamp_bad_stencil()` — no grounded route
exists there on either path. Identity proof: exactly the 66 nodes differ from the
published table; LOGRHO/C_P byte-identical; interpolation code untouched.

## §2 What the repaired table does to the published numbers

**The headline sentence, ahead of the tables: 26 %/41 % (C13's rock-axis bracket) and
39.7 %/60.0 % (Brief 26's spans) were measurements of a table choice, not of the
planets.** A number that exists on one grounded route and does not even converge on
the other was never robust to that choice. That — not which table is right — is this
experiment's product.

Measured, original beside repaired (controls first: with the repair OFF, the corrected
declarations reproduce their bases exactly — rockB_U λ 0.20972908…, grid_U_0.3
λ 0.20763726…, both conv=True — so every flip below is the repair's doing, not
declaration drift):

- **Anchors (branch ①)**: U Δλ −3.6e-6 · ΔT_c −1.3e-4; N Δλ +2.9e-5 · ΔT_c −1.1e-4 —
  within the 3.7–3.9e-4 jitter. The clamp was conservative where the anchors read it.
- **C13 rock end B — both ends flip conv=False** (λ 0.209729→0.195350 (−6.9 %),
  0.219617→0.207624 (−5.5 %)). *Condition now attached to the published bracket: the
  26 %/41 % gap coverage was measured on the clamped table; on the repaired table the
  bracket's outer ends do not meet the boundary condition and the bracket is
  unmeasured.*
- **Brief 26 grid — the wide half flips** (U w≥0.2, N w≥0.125 conv=False; narrow
  half moves ≤1e-4-grade and keeps converging). *Condition attached: the 39.7/60.0 %
  spans exist only on the clamped table; the repaired-table measurable span collapses
  to the narrow half (U ≈3.6 %, N ≈1.5 % of the deficit).*
- Ice end B: still conv=False on both tables; diagnostic renorms move percent-level
  (0.2356–0.2736 → 0.2437–0.2830).

Mechanism, recorded not asserted: the repaired values are mostly below 0.1 in the
contact band, flattening that stretch of the adiabat; the same t_center then leaves a
hotter 1-bar level, and the walk toward 76 K fails the same way the z_shallow family
did. **Still carried: this test says which route the numbers depended on, never which
route is closer to the authors' unpublished truth.**

## §3 Runner hygiene (two recurrences, one fix)

The rock-end-B declaration mistake (ice layer dropped) recurred twice in this brief —
caught the second time by the directing seat because the first recurrence was written
down. The corrected declaration is now fixed in the suite runner, and the runner
gained a **base auto-check**: run without `--repaired` it must reproduce each point's
published base on the unrepaired table (mismatch auto-invalidates the point); with
`--repaired` it arms the opt-in module and prints deltas. Declarations in runners are
anchor-grade assets.
