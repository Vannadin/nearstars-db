# The cold-flank general fix — context notes

Brief 22, 2026-08-31. Pre-registration is in `cold-flank-checklist.md` (written before any
code beyond the brief's three pointers was read).

## §1 The mechanisms, traced not guessed

The directing session handed three readings labeled as readings; each was checked against
the code, and one death was re-traced live before any design was fixed.

1. **C13 end B — two killers, both static.** (i) `integrate`'s **centre seed**: `rho_c =
   mat.density(p_center, t, t_pot)` with `mat = stack[0][1]` — the static innermost
   material, taken before the fluid/solid dispatch exists. With the water column innermost,
   the solid ladder is asked at the centre regardless of temperature: at P_c > 1 TPa it
   throws its knot-cap refusal (traceback: `integrate` → `Material.density` →
   `check_temperature` → `phase_at`), and at P_c ≤ 1 TPa with T > 1800 K it throws the
   superionic t_over refusal — both were observed (the 1 s deaths of the first bracket
   attempt). (ii) `_shoot_pressure`'s bracket ceiling `p_ceiling = stack[0][1].p_max` caps
   the centre pressure at the **solid** ladder's 1 TPa even when the centre dispatches
   fluid.
2. **Queyroux–Neptune route death — the availability seam.** Instrumented in a throwaway
   worktree (`coldflank-trace`, Queyroux window patch + a dispatch spy): the trial walks
   outward as fluid above the cap (1000.4996 GPa · 1102.4 K, liquid=True), the in-step
   phase-boundary finder reads the **fluid↔solid availability handoff at exactly the
   ladder's knot cap** (1 TPa — a spline-box edge, not the data ceiling, which C6 places
   at ~355 GPa, 2026-08-31) as a phase boundary, bisects it, and lands the next step **solid at
   1000.0000 GPa** (`forced=False`) — a rounding hair above the cap, where `phase_at`
   throws the cap refusal **without a temperature**, which the shoot then treats as
   geometry and narrows the pressure bracket; the narrowed bracket cannot carry the mass
   and the solve dies quoting the trial's state. The seam is not physics: at ≥ 1000 K the
   same site is Mazevet's.
3. **C11's over-broad refusal** — a different genus (a refusal *predicate* wider than its
   evidence, fixed at its site on 2026-08-30). Named per branch 2: the general route below
   neither covers nor disturbs it.

## §2 The fix — three edits, one principle

**Evidence caps and availability seams are statements about representations, not about the
body; a trial that hits one steers, it does not die.**

- **The centre seed dispatches like a step** (`integrate`): the seed computation moves
  below the dispatch closures and asks `liquid_at(p_center, t)` when the innermost layer
  is the water column; fluid centres seed from the fluid representation. Bodies without
  dispatch (t = 0, or a non-water innermost layer) fall through with the identical
  arithmetic in the identical order — anchors are bit-identical by construction and by
  the gate.
- **The bracket ceiling respects the dispatch** (`_shoot_pressure`): with the water column
  innermost and t_center ≥ 1000 K the centre is the hot fluid's, whose fit states no
  pressure ceiling; `p_ceiling` is uncapped there. Cold centres (< 1000 K) keep the
  ladder's knot cap — a genuinely cold, very watery body still stops where the
  representation ends, by name (C6's 2026-08-31 refinement: that end is the knot box at
  1 TPa; the data ceiling beneath it is ~355 GPa).
- **The seam steers** (`integrate`, step body): a step dispatched solid **above** the
  ladder's cap — the availability seam the boundary finder can land on — raises
  `PhaseGap(..., too_cold=True)` with the local temperature attached, so the temperature
  loop lifts the trial instead of the shoot mis-narrowing on a temperatureless refusal.

## §3 Measurements

**Acceptance ① and ② — end B solves without the stub, and 1 ULP no longer gates.**
Both planets, both `imf` expressions (residuals: Uranus exactly 0.0 under *both*
expressions — the configuration that died; Neptune ±5.6e-17):

| run | residual | λ | R (vs pub) | I/(M·R_pub²) | P_c | T_c | conv |
|---|---|---|---|---|---|---|---|
| Uranus, 1−gmf−rockf | 0.0 | 0.209729 | 3.9185 (−1.57 %) | 0.2032 | 784 GPa | 4950 K | yes |
| Uranus, 1−(rock+hhe)/m | 0.0 | 0.209729 | 3.9185 (−1.57 %) | 0.2032 | 784 GPa | 4950 K | yes |
| Neptune, 1−gmf−rockf | −5.6e-17 | 0.219577 | 3.9104 (+1.19 %) | 0.2248 | 984 GPa | 4915 K | yes |
| Neptune, 1−(rock+hhe)/m | +5.6e-17 | 0.219617 | 3.9101 (+1.18 %) | 0.2248 | 984 GPa | 4916 K | yes |

The residual's sign still decides whether a ghost stub layer exists, and that moves λ by
1.8e-4 relative — inside the ε-ladder's stability envelope (3e-4 across nine orders) and
consistent with the pre-registered ε→0 reading; what it no longer decides is
**solvability**. And the C13 bracket survives stub-free: renorm 0.2032 / 0.2248 are the
same numbers the stub measured, so **branch 4 does not fire** — 26 % / 41 % were not
stub-dependent.

**Coverage.** Case C13: above. Case Queyroux–Neptune: in the trace worktree (Queyroux
window patch + this fix) Neptune **converges in 79 s to the anchor's own solution** —
R 4.210086 R⊕ · λ 0.179916 · T_c 6296 K · P_c 1533 GPa — repairing the route death and
re-confirming that the converged answer never depended on the curve. Case C11: a different
genus (an over-broad refusal *predicate*, fixed at its site 2026-08-30); the general route
neither covers nor disturbs it — branch 2's naming, with the C11 gate section still
passing. So the registered outcome is **branch 1 for the two corridor cases + branch 2's
naming for C11**.

**Anchors.** `--fast`: both planets' convergence-point integrations bit-identical; the
path fingerprint moved (integrate and _shoot_pressure changed) → `--refresh` in the
landing commit, and the anchor diff shows **only** `path_fingerprint`, `frozen_at` and
the timing fields — every solved value bit-identical. Full solves in the refresh: 24 s /
58 s (was 23 s / 56 s at freeze — the seed-dispatch branch costs nothing measurable).

**Gate additions**: the new test section (two end-B convergence-point integrations + one
cold-ceiling refusal check) adds ~3–4 s to `test_interior.py`; the knot cap for cold
water bodies is asserted to survive by name (C6: the printed 1 TPa is the spline's
knot box; the data ceiling is ~355 GPa).

**Reproduction, for the directing seat's leg** (the three judgment-changing items):
① the four stub-free λ — session scratchpad `coldflank_accept.py` (both planets × both
`imf` expressions, ~5 min); against the stub values in `fuzzy-core-context-notes.md` §6.
② branch 4's non-firing — the same run's renorm columns: 0.2032 / 0.2248 equal the stub
run's to the printed digit, so the bracket's 26 % / 41 % never depended on the device.
③ the Queyroux coverage — a throwaway worktree with the window patch (reconstruction in
`queyroux-flip-context-notes.md` §1, Pa units) plus this fix, then the Neptune solve;
compare R 4.210086 · λ 0.179916 · T_c 6296 · P_c 1533 against
`ice_giant_anchor.json`'s Neptune values.
