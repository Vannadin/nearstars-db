<!-- C20 적분 스텝을 맨틀 시간상수에서 정하는 규칙의 사전등록 — 구현·실행 전에 커밋된 예상 결과와 근거 -->
# C20 adaptive step — pre-registration (Brief 157, 2026-09-08) — committed BEFORE the implementation runs

## The rule

    h = min(STEP_MYR, F · τ(state))        evaluated at the start of every RK4 step

* `STEP_MYR = 4 Myr` stays as the **upper bound** — Nimmo's constant step (their line 419) is the most the
  integrator may take, never less than the rule says.
* `τ(state)` is the linearised mantle relaxation time at the current (T_c, T_m):

      τ = C_eff / (dQ_m/dT_m),   C_eff = m_mantle · C_pm · √r_b   (the denominator of dT_m/dt, eq. 32 in eq. 29's form)
      dQ_m/dT_m = [Q_m(T_m + 1 K) − Q_m(T_m − 1 K)] / 2 K,   Q_m from `mantle_flux.implied_flux` (eqs 34–36)

  This is the mantle's own time constant because eq. 32 is C_eff · dT_m/dt = H_m − Q_m(T_m) + Q_c, and the
  stiff term is Q_m(T_m) ∝ exp(ζ T_m/3)·(T_m − T_s)^{4/3}; its linearisation about the current state
  relaxes on τ. Nimmo's §6 sentence about the *"short mantle time constant at high temperatures"*
  (`2004GeoJI.156..363N.txt@«is due to the short mantle time constant at high temperatures»`) names the same
  quantity in words.
* Measured before implementing (engine at 9c7b6796, central difference ±1 K):

  | body | state | τ |
  |---|---|---|
  | Earth | T_m 3040 K (its start) | 3.93 Myr |
  | Earth | T_m 1600 K | 1128 Myr |
  | Earth | T_m 1525 K (present) | 1545 Myr |
  | Mars | T_m 4021 K (its start) | 0.053 Myr |
  | Mars | T_m 1600 K | 579 Myr |
  | Mars | T_m 1383 K (present, 0.25 Myr sweep) | 1452 Myr |

  So the fixed 4 Myr step was h/τ = **1.02 on Earth's first step** and **75 on Mars's**. Earth survived at
  the edge; Mars did not. (⚠ The "τ ≈ 0.717 Myr, Earth 36.3" in yesterday's sweep comment has no
  derivation anywhere in the repo; 0.717 Myr is the ²⁶Al half-life at interior-core.md:2245. The directing
  seat relayed it into Briefs 156 and 157 as "h/τ Earth 0.1 · Mars 5.6". Both are withdrawn here.)

## F

`F = 0.1`. Basis: RK4's real-axis stability limit is h/τ ≈ 2.78, so 0.1 is 1/28 of it; and it is 1/10 of
the h/τ ≈ 1.02 Earth's first step already passed under the fixed step. Not a fit to any output.

## Expected results, registered before running

1. **Mars** integrates without divergence, and its three compared numbers land within 5 K of the 0.25 Myr
   sweep values: final T_p **1382.90 K** · final T_c **3893.07 K** · T_p at 3.7 Ga **1669.12 K**.
2. **Earth's anchor may move.** Its first steps shrink from 4 Myr to ≈ 0.39 Myr while τ is short, so the
   early hot phase is integrated more finely. If `mantle_potential_temperature_present` moves from
   **1525.46 K** (or T_c(0) from 4027–4028 K, or the step count from 1135), the move is reported with its
   cause and size, and the anchor is refreshed in the same commit (standing rule 1: a moved anchor is
   reported, never absorbed). A move is expected to be small: at h/τ ≈ 1 RK4 is still accurate to
   O((h/τ)⁵) per step, and the hot phase lasts a few tens of Myr.
3. **Step count and h/τ**: every result carries the number of steps taken, the smallest h, and the largest
   h/τ met. The largest h/τ must be ≤ F (0.1) by construction; a value above it is a bug, not a result.
4. An outcome outside 1–3 is written down as its own kind afterwards and registered then.

## What is not changed

`mars_step_sweep.py` stays as it is (its five fixed steps become an upper-bound sweep once the rule is in);
the Nimmo domain declarations (Brief 155) are untouched; `STEP_MYR` keeps its value and its role as the cap.
