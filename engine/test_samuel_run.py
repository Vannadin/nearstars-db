# 판 2 적분의 시험 — 불변식 셋(핵 에너지 수지 · 식 20 부호 · 천장)과 Λ 20 한 점 일곱 값 회귀 대조
"""Checks for `samuel_run` (pre-registration v2-9 ④). Solves the engine's Mars structure once (~65 s).

    python3 engine/test_samuel_run.py

Invariants, which a wrong wiring breaks whatever the target says:
* the core's energy closes — ∫ q_c A_c dt equals ρ_c C_pc V_c ϵ_c (T_c0 − T_c) (2021 eq. (11)), to 1 %.
  ⚠ The residual is not the trapezoid's step error: shortening the step moves it within ±0.5 % either way
  (audit seat, six runs). It was melt-shell noise leaking into q_c — 1.00392 at 120 shells, 0.99991 at 1 920;
* dD_l/dt has the sign of (k_m-conducted outflow at the lid base − q_m + the crust term) at every step —
  2019 SI eq. (20) wired with the v2 `−`;
* Λ 20 stays below its ceiling for the whole run.

Regression: the A0 values that need no source data at Λ 20, cap 10 Myr, re-frozen at 1 920 melt shells (v2-9 records A0
failing there). A move is not a failure of physics — it is a change to explain, then re-freeze with the reason.
The A0 verdict itself is **not** asserted: the gate stays green on a recorded failure.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import samuel_run as sr                # noqa: E402
import samuel_structure as ss          # noqa: E402
import samuel_thermal as st            # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


# The A0 values that need no source data, at Λ 20 and cap 10 Myr, frozen from this run's own output on
# 2026-09-24: 1 920 melt shells (v2-10), the δ_b guard at ½ shell (v2-14), and the δ_u/δ_b bracket solve
# with the nearest inner root (v2-17 and supplements; v2-18). Before the bracket solve they read
# 2101.59 / 1941.69 (a fixed point stopping silently at 60 iterations, noise ~1 K). The two RMS conditions
# need the 2023 source data, which is outside the repo, so the gate cannot hold them.
FROZEN_L20 = {"T_c today": 2101.64, "T_m today": 1942.02, "T_c(1) − T_c0": -48.90, "T_m(1) − T_m0": 286.63,
              "T_m peak": 2044.64, "T_m peak time": 1.2726}
FROZEN_TOL = {"T_m peak time": 0.0005}  # Gyr; every other value K, to the frozen decimal


prof = ss.mars_profile(Path(__file__).resolve().parent / "bodies" / "mars.yaml")
print(f"  구조 — {prof.source}")
s = sr.Setup(lam=20.0, profile=prof, g=prof.gravity(prof.radius_m), g_c=prof.gravity(st.R_CORE_NO_BML_M),
             path_check_every=100)
out = sr.run(s, 10.0)
check("Λ 20 runs to 4.5 Gyr without a refusal", "refused" not in out, out.get("refused", "")[:80])
rows = out["rows"]

# ① core energy — trapezoid of q_c A_c against the core's heat content change
r_c = st.R_CORE_NO_BML_M
a_c, v_c = 4 * math.pi * r_c ** 2, 4 / 3 * math.pi * r_c ** 3
e_out = sum(0.5 * (a["q_c"] + b["q_c"]) * a_c * (b["t"] - a["t"]) * sr.GYR_S for a, b in zip(rows, rows[1:]))
e_lost = st.RHO_CORE_KG_M3 * st.CP_CORE_J_PER_KG_K * v_c * st.EPSILON_CORE * (rows[0]["t_c"] - rows[-1]["t_c"])
check("2021 eq. (11) — the core's energy closes to 1 %", abs(e_out / e_lost - 1) < 0.01,
      f"∫q_c A_c dt {e_out:.4e} J · ΔE_core {e_lost:.4e} J · ratio {e_out / e_lost:.5f}")

# ② the lid equation's sign at every step
live = [r for r in rows if r["ddl"] != 0.0]
bad = [r for r in live if (r["ddl"] > 0) != (r["lid_net"] + r["crust_term"] > 0)]
check("2019 SI eq. (20) — dD_l/dt has the sign of (outflow − q_m + crust term) at every step", not bad,
      f"{len(bad)} of {len(live)} steps differ")

# ③ the ceiling
worst, when = out["max_lambda_over_ceiling"]
check("v2-4 ③ — Λ 20 stays under its ceiling", worst < 1.0, f"largest Λ/ceiling {worst:.3f} at {when:.3f} Gyr")

# v2-17 supplements — the bracket solve: no failure, cold starts agree where the inner root is single,
# and every root jump is printed.
check("v2-17 — the δ_u/δ_b bracket solve never fails", not out["fixed_point_limit_hits"],
      f"{len(out['fixed_point_limit_hits'])} failures")
single = [p for p in out["path_checks"] if p[1] == 1]
worst = max((max(abs(p[2] - p[4]), abs(p[3] - p[5])) for p in single), default=math.nan)
check("v2-17 — a cold start gives the same δ_u, δ_b where the inner root is single (≤ 1e-6 m)",
      single and worst <= 1e-6, f"{len(single)} samples, largest difference {worst:.3g} m")
for j in out["root_jumps"]:
    print(f"      뜀 @ {j[0]:.4f} Gyr: δ_b {j[1] / 1e3:.1f} → {j[2] / 1e3:.1f} km, T_c − T_b {j[3]:+.3f} K")
print(f"      근 여럿 평가 {out['multi_root_evals']} · 뜀 {len(out['root_jumps'])}")

# regression — the six data-free values
c = sr.curve_values(rows)
for key, frozen in FROZEN_L20.items():
    tol = FROZEN_TOL.get(key, 0.006)
    check(f"regression — Λ 20 {key} = {frozen}", abs(c[key] - frozen) <= tol, f"now {c[key]:.4f}")

print(f"  test_samuel_run — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
