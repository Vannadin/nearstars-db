# C20 열진화 적분기 테스트 — 사전등록 분기(⑤ 수렴 · ① 지구 보정 · ② 내핵 · ④ 냉각률 · ③ ΔE_min)를 그 순서로 읽는다
"""Pre-registered checks for the C20 integrator (engine/core-thermal-history-context-notes.md §2–§3).

    python3 engine/test_core_history.py            # the gate: one converged history at h = min(4 Myr, 0.1·τ),
                                                   # plus the C48 Mars pair, each under both H conditions
                                                   # (~360 s measured 2026-09-09 after Brief 166 D; 235 s before it, ~60 s before Brief 157)
    python3 engine/test_core_history.py --sweep    # on demand: h, h/2, h/4 (~7 min) — the pre-registered ⑤ test

The sweep is on demand because it costs ~400 s (each time step builds four core profiles for RK4); the gate
carries the single run and the recorded sweep result (2026-09-04: width 0.001 %, same inner-core case at
1135 / 2270 / 4540 steps). ③ is read last, and only because ⑤ passed on record.
⚠ Those three counts are the **fixed-step** sweep of 2026-09-04, and between Briefs 157 and 161 `--sweep`
did not reproduce them: `sweep` had gone on varying the CAP in `h = min(cap, 0.1·τ)`, where halving changes
only the steps the cap binds. **Brief 161 restored ⑤'s registered meaning — `sweep` runs `adaptive=False`**,
because a branch registered before the adaptive step exists is not re-written afterwards to match the code.
An adaptive-cap sweep would be a different question and is deliberately not built (C47 (i)).
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cmb_flux as cf                  # noqa: E402
import core_energy as ce               # noqa: E402
import core_history as ch              # noqa: E402
import radiogenic as rg                # noqa: E402
from interior import solve as interior_solve  # noqa: E402

fails = 0


def row(ok, text):
    global fails
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


# Earth inputs, read from the interior solve (not typed in) — the same construction as C14/C15.
v = interior_solve(1.0, core_mass_fraction=0.325, potential_temperature=1600.0).values
M, RP = cf.M_EARTH_KG, cf.R_EARTH_M
R_B = v["cmb_temperature"] / 1600.0
PARAMS = {"material": "fe_prem", "p_cmb": v["cmb_pressure"] * 1e9, "r_cmb": v["core_radius"] * RP,
          "m_core": 0.325 * M, "m_mantle": 0.675 * M, "r_b": R_B, "g": cf.G_NEWTON * M / RP ** 2, "r_p": RP,
          "h_core": ce.H_CORE, "h_m_present_w": rg.budget(0.675 * M)["mantle_w"]}
T_C0, T_M0 = 4800.0, 4800.0 / R_B     # Nimmo Fig. 2 caption: "starting temperature of both mantle and core was 4800 K" (real)
AGE = 4.54

# ⚠ **Brief 166 D — the reproduction anchors carry their own H, the way the Table 4 anchors already do.**
# (⚠ Brief 166 E, the same day, corrected the declared H again — 0.14 was our textbook conversion, 0.088 is the
# paper's own; the declared-H anchors below are the 0.088 measurement and the mechanism is unchanged.)
# Owner decision ⑤ (2026-09-09) lowered the declared core heating from 1.5 to 0.14 pW/kg, and that moved this
# node's *reproduction* anchors: gate200 failed on 1517.62 K against 1525.46 and on Mars's 1377.23 · 3768.09.
# Nothing was wrong with the integrator — the anchors had been reading the nominal constant. So C48's anchors
# now name their condition (`H_NIMMO`, the same 1.5e-12 as `test_core_energy.H4`, Nimmo+ 2004 Table 4's 400 ppm K),
# and the engine's declared H gets rows of its own, measured 2026-09-09 and pinned here as anchors in turn.
H_NIMMO = 1.5e-12                     # W/kg — Nimmo Table 4; = test_core_energy.H4. NOT the engine's declared H.
PARAMS_NIMMO = {**PARAMS, "h_core": H_NIMMO}

print("⑤ 수렴 — 판정선은 종점 T_c 가 아니라 3.1 Gyr 창의 ΔE_min (h/4 대 h/2 < 10 %), 내핵 갈래 동일")
if "--sweep" in sys.argv:
    t0 = time.perf_counter()
    sw = ch.sweep(PARAMS, T_C0, T_M0, AGE)
    for lab in ("h", "h/2", "h/4"):
        o = sw[lab]
        print(f"      {lab:>4}: {o['hist']['n_steps']} 걸음 · T_c {o['t_c_present']:.1f} K · 내핵 {o['case']} · "
              f"ΔE_min 밴드 {o['delta_e_min_lo']/1e6:+.1f}…{o['delta_e_min_hi']/1e6:+.1f} MW/K")
    row(sw["converged"], f"수렴 폭 {sw['convergence_width']:.4%} · 같은 내핵 갈래 {sw['same_inner_core_case']} ({time.perf_counter()-t0:.0f} s)")
    hist = sw["h/4"]["hist"]
else:
    print("      (온디맨드 — `--sweep`. 기록 2026-09-04, 고정걸음: 폭 0.001 %, 1135/2270/4540 걸음 모두 '내핵 없음' — 통과)")
    print("      ⑤ 는 걸음을 반씩 줄이는 시험이므로 --sweep 은 고정걸음으로 돈다 (adaptive=False, 브리프 161) — 위 세 걸음 수가 그대로 재현된다")
    t0 = time.perf_counter()
    hist = ch.integrate(PARAMS, T_C0, T_M0, AGE)
    # Brief 157: the step is adaptive (h = min(4 Myr, 0.1·τ)); Earth takes 1152 steps (fixed: 1135 — the 17 extra are the hot
    # first ~50 Myr) and its anchors do not move at two decimals (T_p 1525.46, T_c 4027.43). Recorded, not absorbed (rule 1).
    row(hist["n_steps"] == 1152 and abs(hist["step_myr"] - 4.0) < 0.01 and abs(hist["max_h_over_tau"] - 0.1) < 1e-9,
        f"단일 실행 h ≤ {hist['step_myr']:.2f} Myr (적응, 최대 h/τ {hist['max_h_over_tau']:.3f}) · {hist['n_steps']} 걸음 · 최소 h {hist['h_min_myr']:.3f} Myr ({time.perf_counter()-t0:.0f} s)")
    fixed_n = ch.integrate(PARAMS_NIMMO, T_C0, T_M0, AGE, adaptive=False)
    fx_n = fixed_n["rows"][-1]
    row(fixed_n["n_steps"] == 1135 and abs(fx_n["t_m"] - 1525.46) < 0.005 and abs(fx_n["t_c"] - 4027.43) < 0.005,
        f"고정 4 Myr 재현 (H 1.5 pW/kg, Nimmo Table 4 조건): {fixed_n['n_steps']} 걸음 (앵커 1135) · T_p {fx_n['t_m']:.2f} K (앵커 1525.46) · "
        f"T_c {fx_n['t_c']:.2f} K (앵커 4027.43)")
    fixed = ch.integrate(PARAMS, T_C0, T_M0, AGE, adaptive=False)
    row(fixed["n_steps"] == 1135 and abs(fixed["rows"][-1]["t_m"] - 1517.34) < 0.005 and abs(fixed["rows"][-1]["t_c"] - 3911.29) < 0.005
        and abs(fixed["rows"][-1]["t_m"] - hist["rows"][-1]["t_m"]) < 0.01,
        f"선언 H 0.088 pW/kg (오너 결정 ⑤ · 브리프 166 E 환산 정정): 1135 걸음 · T_p {fixed['rows'][-1]['t_m']:.2f} K (앵커 1517.34) · "
        f"T_c {fixed['rows'][-1]['t_c']:.2f} K (앵커 3911.29) · 적응과의 차 {hist['rows'][-1]['t_m'] - fixed['rows'][-1]['t_m']:+.4f} K")
ws = ch.window_summary(hist["rows"])
last = hist["rows"][-1]

print("\n① 지구 보정 — 현재 T_c 가 C14 의 밴드 3750–4284 K 안인가 (사전등록 허용오차; 실패면 상수는 안 움직인다)")
row(3750.0 <= last["t_c"] <= 4284.0, f"T_c(0) {last['t_c']:.0f} K")
print(f"      보고 줄(게이트 아님): T_m(0) {last['t_m']:.0f} K 대 선언 1600 K ({last['t_m']-1600:+.0f} K) · "
      f"Q_M(0) {last['q_m_w']/1e12:.1f} TW 대 Nimmo·관측 42 TW · Q_C(0) {last['q_c_w']/1e12:.2f} TW (C14 4.91)")

print("\n② 내핵 — C14 는 '풀린 T_c 에서 내핵 없음'; 예상 갈래는 ②c (핵생성 없음)")
row(ws["inner_core_case"] == "never", f"갈래 {ws['inner_core_case']} · 현재 r_i {last['r_i_km']:.0f} km")

print("\n④ dT_c/dt — 선언(33–126 K/Gyr)이 계산이 되는가")
rate = -last["dtc_dt_k_gyr"]
row(33.0 <= rate <= 126.0, f"현재 −dT_c/dt {rate:.0f} K/Gyr (④a: 밴드 안 → C14 의 선언 밴드는 이 값으로 좁힐 수 있다)")

print("\n③ ΔE_min (3.1 Gyr, k × H 네 모서리) — 맨 마지막, ⑤ 통과 기록 위에서만")
lo, hi = ws["delta_e_min_band"]
n_pos = sum(1 for c in ws["per_corner"].values() if c["min"] > 0.0)
print(f"      밴드 {lo/1e6:+.0f}…{hi/1e6:+.0f} MW/K · 양수 모서리 {n_pos}/4 · 판정 '{ws['verdict'][:12]}…'")
for (k, hh), c in sorted(ws["per_corner"].items()):
    print(f"      k {k:.0f} · H {hh*1e12:.1f} pW/kg: min {c['min']/1e6:+.0f} (t {c['t_min_gyr']:+.2f} Gyr) · mean {c['mean']/1e6:+.0f} · present {c['present']/1e6:+.0f}")
row(ws["verdict"] == ch.CANNOT_SAY_HISTORY if lo < 0.0 < hi else ws["verdict"] in (ch.SUSTAINED, ch.FAILS),
    "판정 문자열이 밴드의 부호 구조와 맞는다 (③c 면 cannot-say, 좁히지 않는다)")

print("\n계약 — 레시피 출력과 거절")
res = ch.solve(1.0, 0.325, v["core_radius"], v["cmb_pressure"], v["cmb_temperature"], 1600.0, 1.0, AGE,
               T_C0, T_M0, run_sweep=False)
row(res.applicable and res.values["inner_core_case"] == "never" and res.values["history_converged"] is None,
    f"solve(): {res.regime} · {res.values['entropy_history_verdict'][:40]}… · 수렴 필드 None (스윕은 온디맨드)")
row(all(k in res.units for k in res.values), "모든 값에 단위")
r2 = ch.solve(1.0, 0.325, v["core_radius"], v["cmb_pressure"], v["cmb_temperature"], 1600.0, 1.0, AGE, None, None)
row(not r2.applicable and "initial" in r2.reason, "초기온도 미선언 → 이름 붙여 거절")
r3 = ch.solve(1.0, 0.325, v["core_radius"], v["cmb_pressure"], v["cmb_temperature"], 1600.0, 1.0, AGE, T_C0, T_M0,
              body_class="giant")
row(not r3.applicable, "거대행성 → 거절")

# ── Brief 157 / C48 — the Mars divergence was the step, both ways ─────────────────────────────────
print("⑥ C48 — 화성: 고정 4 Myr 이면 발산, 적응이면 0.25 Myr 스윕값(1382.90 · 3893.07 · 1669.12) 5 K 안 "
      "— 스윕도 재현도 H 1.5 pW/kg 조건이다 (Brief 166 D)")
vm = interior_solve(0.1074, core_mass_fraction=0.24, potential_temperature=1600.0).values
MM = 0.1074 * M
RPM = 0.5320 * RP
R_BM = vm["cmb_temperature"] / 1600.0
PARAMS_M = {"material": "fe_prem", "p_cmb": vm["cmb_pressure"] * 1e9, "r_cmb": vm["core_radius"] * RP,
            "m_core": 0.24 * MM, "m_mantle": 0.76 * MM, "r_b": R_BM, "g": cf.G_NEWTON * MM / RPM ** 2, "r_p": RPM,
            "h_core": ce.H_CORE, "h_m_present_w": rg.budget(0.76 * MM)["mantle_w"]}
PARAMS_M_NIMMO = {**PARAMS_M, "h_core": H_NIMMO}
try:
    ch.integrate(PARAMS_M_NIMMO, 4800.0, 4800.0 / R_BM, AGE, adaptive=False)
    row(False, "고정 4 Myr 화성이 발산하지 않았다 — C48 의 기록(T_m −6244 K)과 어긋남")
except ValueError as e:
    row("표면온도" in str(e), f"고정 4 Myr 화성 → 발산 (ValueError: {str(e)[:60]}…)")
t0 = time.perf_counter()
hm = ch.integrate(PARAMS_M_NIMMO, 4800.0, 4800.0 / R_BM, AGE)
lastm = hm["rows"][-1]
nearm = min(hm["rows"], key=lambda r: abs(r["t_gyr"] + 3.7))
# ⚠ **앵커 셋이 180 C 에서 움직였다** (`61374a86`, 재고정은 180 D). 원인은 ① **압력 분할**이다 —
# 이 노드는 구조 적분기를 지나지 않고 `cmb_flux`·`core_energy` 를 부르는데, 그 둘이
# `core_gamma(mat, p_cmb, t_c)` 를 묻고 **화성의 p_cmb 20.649 GPa 가 Huang 실측 구간(19–35 GPa) 안**
# 이라 γ 가 **1.5 → 2.8718** 로 바뀌었다. 전/후: T_p 1382.90 → 1383.78 · **T_c 3893.07 → 3905.34**
# (+12.27) · T_p@3.7Ga 1669.12 → 1669.99. 허용오차는 그대로 두고 앵커만 옮긴다.
row(abs(lastm["t_m"] - 1383.78) < 5.0 and abs(lastm["t_c"] - 3905.34) < 5.0 and abs(nearm["t_m"] - 1669.99) < 5.0,
    f"적응 화성 (H 1.5) → T_p {lastm['t_m']:.2f} · T_c {lastm['t_c']:.2f} · T_p@3.7Ga {nearm['t_m']:.2f} K · {hm['n_steps']} 걸음 · 최소 h {hm['h_min_myr']:.4f} Myr "
    f"(180 C 전 대비 {lastm['t_m']-1382.90:+.2f} / {lastm['t_c']-3893.07:+.2f} / {nearm['t_m']-1669.12:+.2f} K, {time.perf_counter()-t0:.0f} s)")
# The declared-H row. Same trajectory shape (1197 steps, h_min 0.0053 Myr, inner-core branch 'never'); the answer
# moves by −5.87 / −129.91 K. ⚠ The 3.7 Ga column's **rule is part of the number**: `min(rows, key=|t_gyr + 3.7|)`
# — the nearest *sampled* row, never an interpolation. Here that row is unique (t = −3.700566 Gyr, |Δ| 0.000566 Gyr
# against the next row's 0.003434) and reads 1668.0021 K at the declared H, so the anchor is 1668.00. ⚠ Brief 166 E moved the declared H from the
# mis-converted 0.14 to 0.088 pW/kg, which moved this column by −0.04 K; at 0.14 it read 1668.0452, and the audit
# seat's run of that condition reported 1668.043744 from a row at −3.700558 Gyr — same trajectory, different row
# grid. Neither deserves its last digits —
# the local step is ~4 Myr, so "nearest row" is ±2 Myr, worth ≈0.19 K, against 5.1 K of criterion-B headroom.
t0 = time.perf_counter()
hmd = ch.integrate(PARAMS_M, 4800.0, 4800.0 / R_BM, AGE)
lastd = hmd["rows"][-1]
neard = min(hmd["rows"], key=lambda r: abs(r["t_gyr"] + 3.7))
# ⚠ **같은 원인으로 이 갈래도 움직였다** (180 C → 180 D 재고정): T_p 1377.03 → 1377.96 ·
# **T_c 3763.10 → 3780.60**(+17.50) · T_p@3.7Ga **1668.00 → 1668.79**. 걸음 수 1197 은 불변이다.
# ⚠ **그리고 마지막 수가 기준 B 의 여유를 먹는다** — Herzberg 상한 1673.15 K 까지 **5.15 → 4.36 K**.
# 판정은 여전히 통과지만 C20 이 «5 K 오차면 뒤집힌다» 고 적어 둔 자리라, 방향이 크기보다 중요하다.
row(hmd["n_steps"] == 1197 and abs(lastd["t_m"] - 1377.96) < 0.05 and abs(lastd["t_c"] - 3780.60) < 0.05
    and abs(neard["t_m"] - 1668.79) < 0.05,
    f"선언 H 0.088 화성 → T_p {lastd['t_m']:.2f} · T_c {lastd['t_c']:.2f} · T_p@3.7Ga {neard['t_m']:.2f} K · {hmd['n_steps']} 걸음 "
    f"(H 1.5 대비 {lastd['t_m']-lastm['t_m']:+.2f} / {lastd['t_c']-lastm['t_c']:+.2f} / {neard['t_m']-nearm['t_m']:+.2f} K, {time.perf_counter()-t0:.0f} s) "
    f"— 기준 B: Herzberg [1553.15, 1673.15] K 안 (위끝 여유 {1673.15-neard['t_m']:.2f} K)")

print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
