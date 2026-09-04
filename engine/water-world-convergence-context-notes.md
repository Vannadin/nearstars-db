<!-- C24 — 물 많은 암석체가 interior 에서 수렴하지 않는다. 사전등록 → 진단 → 실행 기록 -->
# C24 — the water-rich rocky body does not converge — context notes

Opened by the owner 2026-09-04 (back to the stem; relayed by the directing seat). **§1 is the pre-registration,
committed before the first diagnostic run.**

## 1. Pre-registration

**Symptom (reproduced by the directing seat, `interior.solve(1.0, core_mass_fraction=0.325, ice_mass_fraction=X,
potential_temperature=1600)`):** X = 0 → 3 s, `calibrated`, R 1.0030, centre 358.5 GPa (positive control); X = 0.1 →
68 s, `analog`, R 1.1509, centre 353.8 GPa, `converged=False`. The 20× slowdown is itself a clue: a loop running to
its cap and giving up, not a hard computation.

**① Where does it fail — first, and by a per-iteration log, not by reading.** Log (centre temperature, centre
pressure, surface-condition residual) at every iteration of both loops.
- ①a the temperature loop — the centre-temperature update oscillates or exhausts its cap.
- ①b the pressure bracket — the centre-pressure bisection cannot narrow.
- ①c the two loops hand the failure to each other — `interior.py` documents *"what temperature blocked cannot be
  fixed by the pressure bracket … the outer temperature loop raises the centre temperature and re-brackets"*;
  the most likely, but read off the log, not assumed. The log decides oscillation vs drift in one look.

**② The directing seat's hypothesis — a thing to test, not a premise:** with a water layer, the silicate mantle's
top starts at the water layer's *bottom* temperature instead of the declared potential temperature, which would
put the CMB hotter at lower pressure (as C17's unconverged rows showed).
- ②a true → the source of the silicate-top temperature under a water layer is corrected.
- ②b false → written as the hypothesis's retraction.

**③ Neither ① nor ② explains it → stop and report.** No third candidate is invented on the spot.

**④ Positive control, fixed:** ice 0.0 must stay 3 s · `calibrated` · R 1.0030 · centre 358.5. If it moves, the
change broke something rather than fixed it.

**⑤ Anchors — the most dangerous part:** the temperature loop is a path function; touching it changes the
fingerprint. `test_ice_giant.py --refresh` goes in the same commit, **and the refreshed values must be
bit-identical to the old ones** (the ice-0 path must not change). A difference means dry bodies were touched
too: stop and trace.

**⑥ Success:** ice 0.1 *and* 0.3 converge · grade back to `calibrated` · positive control unchanged · anchors
bit-identical. Anything less is reported as partial and not adopted.

**Scope:** C17 is not opened with this (it becomes measurable when C24 closes; separate start). No fix is
attempted before ①–③ are read.

## 2. ① read off the log (2026-09-04 14:5x, compute-only wrapper on `_shoot_pressure`, no worktree change)

    ice 0.1 — 26 calls, 56 s, converged False:
      T_c 3200 → PhaseGap (water, 0.09 GPa · 672 K: outside the dense-liquid table's window)  → ×1.6
      T_c 5120 → shoot ok, T_surf/T_pot − 1 = +0.78                                          → proportional step asks ~2870
      T_c 2870 → PhaseGap (water, 20.6 GPa · 1055 K: inside the melting-curve dispute band, Queyroux+ 2020) → ×1.6 → 4591 → +0.58
      T_c 2914 → PhaseGap (water, 0.09 GPa · 560 K: dense-liquid window)                      → ×1.6 → 4663 → +0.60
      … from call 10 on the pair is frozen: T_c 2907.5 → PhaseGap at 20.6 GPa · 1058 K → 4652.1 → +0.6000, twelve times identical.
    ice 0.0 — 6 calls, 3 s: 3200 → 2655 → 2671.6 → 2671.1 → converged at 5.7e-9 (positive control as recorded).

**Reading (①, before any fix):** it is neither an oscillating temperature update (①a) nor a pressure bracket that
cannot narrow (①b — every completed shot lands P_c 353.8 GPa at once). It is a **wall in the water column**: the
surface condition wants T_c ≈ 2 900 K, but at that centre temperature the adiabat crosses the water layer at
temperatures the water EOS refuses — the disputed ice-VII melting band at ~20.6 GPa / ~1 055 K (Queyroux+ 2020
vs the other fit) and the dense-liquid table's window at ~0.09 GPa / ~560 K. Each refusal is a `PhaseGap` with
`too_cold=True`, so `attempt` multiplies T_c by 1.6, lands at 4 652 K where the whole water column is hot enough
to dispatch, and the surface comes out 60 % too hot. The loop then asks 2 907.5 again and is refused again — a
**fixed two-cycle between a table wall and a too-hot surface**, not a convergence failure of the update. That is
①c's shape ("the two loops hand the failure to each other") with the wall named: **the water EOS's validity
windows, not physics.** The `analog` grade and the hot CMB (4 397 K in C17) are the stuck-hot state's values.

**② (the silicate-top hypothesis):** not the mechanism of the non-convergence — the shot at the needed T_c never
completes, so where the silicate top starts is never reached. ②b as far as convergence is concerned; retracted
as a *cause*. Whether the silicate-top temperature source is right is a separate question that becomes
askable only after the wall is understood.

**Next diagnostic, not a fix:** name the two windows exactly (which table, which bound, and whether `too_cold`
is the correct flag for the disputed band — a *disputed* band is not a cold flank).

### Registered before the scan (2026-09-04 14:53:37)
The two refusals are of different kinds and are not one "wall": **0.09 GPa · 560 K** is the dense-liquid table's
**pressure floor** (P_MIN 2.3 GPa; the 500–1000 K low-pressure liquid was "close to vapour, grid not honest, not
frozen" — a coverage gap between `h2o_liquid` and Mazevet's ≥ 1000 K), a physical/data limit; **20.6 GPa · 1055 K** is
the ice-VII melting-curve **dispute band** (Brief 33: sources agree numerically, disagree on phase assignment; we
chose to refuse inside the candidate envelope) — a policy. Both raise `too_cold=True` on purpose ("hotter → the
next representation takes it").
- **(a) the flag steers the wrong way** → fixing the direction lets the loop through (the ammonia cold-flank class).
- **(b) the answer lies inside a hole** → the only T_c that meets the surface (~2 900 K) crosses a region we refuse
  to evaluate; no flag fix passes; the outcome is a *named refusal* ("the solution lies in a refused region") or a
  narrowing of the hole by data/declaration — a legitimate ending (C13, C18), not a failure.
- **③** whether the dispute band is a two-sided strip in T (then a one-way `too_cold` cannot represent it — a
  third fact) or a one-sided wall.
Scan: T_c from 2 907 to 4 652 K; if a passing interval exists that the update never reaches → (a); if ~2 900 is
blocked throughout → (b).

## 3. The scan — (b): the answer lies inside a hole (2026-09-04 14:55, compute-only)

    T_c (K)    outcome
    2700–2800  REFUSED — dispute band: 20.6 GPa · 966–1017 K inside the candidate envelope 715–1073 K (too_cold=True)
    2907–4000  REFUSED — dense-liquid table's PRESSURE FLOOR: 0.086–0.100 GPa · 557–873 K, below P_MIN 0.1 GPa
               ("500–1000 K low-pressure water is close to vapour; the bilinear grid was not honest, so not frozen"; too_cold=True)
    4200       PASS — T_surf/T_pot − 1 = +0.42 (surface 42 % too hot)
    4400       PASS — +0.50
    4652       PASS — +0.60

Every centre temperature below ≈ 4 100 K is refused, and the lowest passing one already leaves the surface 42 %
too hot with the residual rising with T_c, so the T_c that would meet the surface (≈ 2 900 K by the proportional
update) lies **entirely inside the refused region**. There is no passing interval the update fails to reach:
**(b)**, not (a). The flag directions are not the cause.

**What the hole is.** Not the dispute band (it bites only at T_c ≤ 2 800 K, below the answer) but the near-surface
water column: on a 10 % water body at a declared potential temperature of 1 600 K, the water just under the
surface sits at ~0.09 GPa and 560–870 K — a **supercritical fluid below 0.1 GPa between 500 and 1 000 K that no
held representation covers** (`h2o_liquid` is the cold liquid; `water2` starts at 0.1 GPa; Mazevet takes over at
1 000 K). This is the coverage gap the dense table's own comment names. So the honest ending is a **named
refusal**: *"the solution lies in a refused region — near-surface water between 500 and 1 000 K below 0.1 GPa"* —
the C13/C18 kind of closure, not a bug in the loop.

**And a declaration question beside it, not decided here:** 1 600 K is Earth's *mantle* potential temperature;
applying it to a body whose outer 10 % is water puts a ~600–900 K fluid ocean/steam layer at the surface. A water
world's potential temperature is the water's, not the rock's, and at ~300 K the column would be solid ices on a
different path. C17's instrument used the rock's declaration on a water world; the non-convergence is partly the
declaration's, and the refusal should say so.

**③** The dispute band is a **two-sided strip in T** (715–1 073 K at 20.6 GPa; below → all solid, above → all
liquid, inside → refuse) carried by a **one-way** `too_cold=True` flag — a third fact: the flag system cannot
express a strip. Not on this failure's critical path (the answer is above the strip), recorded for the flag
design. Queyroux+ 2020 and Prakapenka+ 2021 are both held (`check_paper_held.py`); nothing to request.

**Nothing fixed; nothing to fix in the loop.** Next, if the owner wants the body solved: either a representation for
500–1 000 K water below 0.1 GPa (IAPWS-95 covers it — a data question), or the declaration corrected for water
worlds, or the named refusal emitted by `interior` as its answer for this input class. Owner's choice.

## 4. The hole is already covered by a table the water column never consults (directing seat's catch; read 2026-09-04 14:57)

**1. Reachable?** No — not from the water column. `interior.liquid_material` (line 585, the water column's liquid
dispatch) considers, in order: the ocean table water1 (≤ 2.3 GPa · ≤ 500 K), then `h2o_hot` at ≥ 1 000 K, then
water2 if `in_domain`, then **raises** (`too_cold=True`). It never names `STEAM` / `h2o_if97`. Its own docstring
states the hole: *"0.1 GPa 아래의 뜨거운 저압 물은 여전히 표현이 없고 이름 대며 거절한다"*.
**2. Why not chosen?** Not applicable — it is not a candidate there.
**3. Why envelope-only?** `_EnvelopeWater._rep` (line 1684) *does* consult it, and says why: *"IAPWS-IF97 r1·2
(Brief 25) — Brief 23's wall (p ≲ 0.1 GPa × 500–1000 K) was closed by this line."* So the same wall was closed on
2026-08-3x **for water dissolved in an envelope** and never for the water column of a water-rich rocky body.
`_Steam`'s docstring ("used only as `_EnvelopeWater`'s delegate; `p_max` not stated so a mixture's ceiling is not
set by this component") is a scoping note of Brief 25, not a prohibition — the `p_max = inf` design is about
mixture ceilings, not about the column. No document says the column must not use it.
**Physics**: 0.09 GPa · 560–870 K is supercritical water; IF97 region 2 is exactly that region; the table is
appropriate, and the gate verifies it every run against the standard's own check values (worst 2.9e-9).

**So C24 is not "data missing" but "a held table is not consulted in that window" — a one-place dispatch.**
The owner's decision shrinks from an IAPWS-95 transcription to one candidate line.

**Design if released (not done):** add `STEAM` to `liquid_material` **after** water1 / hot / water2 have all
declined — i.e. only inside the window that is refused today — then raise as before if IF97 is also out of
domain. Placing it *last* keeps every anchor bit-identical by construction: an anchor that had entered that
window would have refused, so none did, and no existing path changes. ⑤ still runs formally (`integrate` is a
path function): `--refresh` in the same commit and the refreshed values must be byte-identical; the ice-0
positive control must stay 3 s · calibrated · R 1.0030 · centre 358.5. The envelope puts IF97 *first* among the
liquids; the column must not copy that order (it would move ocean anchors inside water1's overlap with IF97).
Then ⑥ is re-measured: ice 0.1 and 0.3 converge or the next wall names itself.

**Kept, independently**: the potential-temperature remark (1 600 K is the rock's declaration, not a water world's)
is right on its own and is **not** tied causally to this hole — with the dispatch fixed, a correct declaration
can still land in the same window. ③ (a two-sided strip on a one-way flag) stays recorded, off the critical path.

## 5. Fix released (directing seat, owner opened C24) — seam pre-registered before it is built (2026-09-04 14:59:59)

Placing STEAM last among the column's liquid candidates creates two seams: **IF97 ↔ water2 at 0.1 GPa** (the
dense table's floor) for 500–1 000 K, and **IF97 ↔ water1 at 500 K** (the ocean table's ceiling) below 0.1 GPa.
Measured now, before the line is written, the way the melting-curve seam (+26 % at 20.6 GPa, C3) and the iron
seam (6.8–7.5 %, eos.py) were:
- **Ⓐ |Δρ/ρ| ≤ 5 %** at every sampled seam point → proceed; the size is written into the result. Why 5 %: the
  width two fits of one material disagree by in this engine's own record (iron 6.8–7.5 % was recorded as "narrower
  than two static-compression experiments"); a same-fluid density seam should be narrower than that.
- **Ⓑ > 5 %** → proceed anyway, the seam carried by name in the result (the 26 % precedent); STEAM is **not**
  removed for being large — removal returns "no representation", which is worse.
- **Ⓒ wrong sign or order (e.g. the supercritical side far denser than the liquid side)** → stop and report: a
  table-reading error, not a wiring problem.

**Seam result (measured before the line was written): Ⓐ, and far inside it.**

    IF97 ↔ water2 at 0.1 GPa:  560 K +0.00 % · 600 +0.00 · 700 +0.01 · 800 −0.02 · 870 +0.00 · 1000 −0.02 %
    IF97 ↔ water1 at 500 K:    0.02 GPa +0.04 % · 0.05 −0.00 · 0.09 +0.01 · 0.10 −0.00 %

Both neighbours are IAPWS-lineage tables (water2 is SeaFreeze's Gibbs surface, water1 Bollengier's), so the seam
is at the 1e-4 level — the IF97 candidate joins continuously on both sides. Recorded, and pinned by a test row
(≤ 0.05 % at these ten points) so a future table swap cannot open the seam silently.

**What C24 was (the lesson, written before the fix).** The seam being ~0 says it: water1 (Bollengier), water2
(SeaFreeze Gibbs surface) and IF97 are all IAPWS-lineage and agree at their edges to 1e-4 — they were never
tables asserting different physics. So the hole was neither a physical boundary nor a disagreement between
sources: **a coverage gap between three compatible tables, closed on one code path (the envelope) and not on
the other (the water column).** Not a data problem — a "did not join what we already hold" problem, and that
kind recurs. Observation, not a task: *our water representations' coverage map — which table covers which
(P, T), and where the gaps are — lives in no single place; this gap surfaced by chance on one code path.*
