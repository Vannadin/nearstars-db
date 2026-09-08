# C20 열진화 적분기 테스트 — 사전등록 분기(⑤ 수렴 · ① 지구 보정 · ② 내핵 · ④ 냉각률 · ③ ΔE_min)를 그 순서로 읽는다
"""Pre-registered checks for the C20 integrator (engine/core-thermal-history-context-notes.md §2–§3).

    python3 engine/test_core_history.py            # the gate: one converged history at Nimmo's 4 Myr step (~60 s)
    python3 engine/test_core_history.py --sweep    # on demand: h, h/2, h/4 (~7 min) — the pre-registered ⑤ test

The sweep is on demand because it costs ~400 s (each time step builds four core profiles for RK4); the gate
carries the single run and the recorded sweep result (2026-09-04: width 0.001 %, same inner-core case at
1135 / 2270 / 4540 steps). ③ is read last, and only because ⑤ passed on record.
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
    print("      (온디맨드 — `--sweep`. 기록 2026-09-04: 폭 0.001 %, 1135/2270/4540 걸음 모두 '내핵 없음' — 통과)")
    t0 = time.perf_counter()
    hist = ch.integrate(PARAMS, T_C0, T_M0, AGE)
    # Brief 157: the step is adaptive (h = min(4 Myr, 0.1·τ)); Earth takes 1152 steps (fixed: 1135 — the 17 extra are the hot
    # first ~50 Myr) and its anchors do not move at two decimals (T_p 1525.46, T_c 4027.43). Recorded, not absorbed (rule 1).
    row(hist["n_steps"] == 1152 and abs(hist["step_myr"] - 4.0) < 0.01 and abs(hist["max_h_over_tau"] - 0.1) < 1e-9,
        f"단일 실행 h ≤ {hist['step_myr']:.2f} Myr (적응, 최대 h/τ {hist['max_h_over_tau']:.3f}) · {hist['n_steps']} 걸음 · 최소 h {hist['h_min_myr']:.3f} Myr ({time.perf_counter()-t0:.0f} s)")
    fixed = ch.integrate(PARAMS, T_C0, T_M0, AGE, adaptive=False)
    row(fixed["n_steps"] == 1135 and abs(fixed["rows"][-1]["t_m"] - 1525.46) < 0.005 and abs(fixed["rows"][-1]["t_m"] - hist["rows"][-1]["t_m"]) < 0.01,
        f"고정 4 Myr 재현: 1135 걸음 · T_p {fixed['rows'][-1]['t_m']:.2f} K (앵커 1525.46) · 적응과의 차 {hist['rows'][-1]['t_m'] - fixed['rows'][-1]['t_m']:+.4f} K")
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
print("⑥ C48 — 화성: 고정 4 Myr 이면 발산, 적응이면 0.25 Myr 스윕값(1382.90 · 3893.07 · 1669.12) 5 K 안")
vm = interior_solve(0.1074, core_mass_fraction=0.24, potential_temperature=1600.0).values
MM = 0.1074 * M
RPM = 0.5320 * RP
R_BM = vm["cmb_temperature"] / 1600.0
PARAMS_M = {"material": "fe_prem", "p_cmb": vm["cmb_pressure"] * 1e9, "r_cmb": vm["core_radius"] * RP,
            "m_core": 0.24 * MM, "m_mantle": 0.76 * MM, "r_b": R_BM, "g": cf.G_NEWTON * MM / RPM ** 2, "r_p": RPM,
            "h_core": ce.H_CORE, "h_m_present_w": rg.budget(0.76 * MM)["mantle_w"]}
try:
    ch.integrate(PARAMS_M, 4800.0, 4800.0 / R_BM, AGE, adaptive=False)
    row(False, "고정 4 Myr 화성이 발산하지 않았다 — C48 의 기록(T_m −6244 K)과 어긋남")
except ValueError as e:
    row("표면온도" in str(e), f"고정 4 Myr 화성 → 발산 (ValueError: {str(e)[:60]}…)")
t0 = time.perf_counter()
hm = ch.integrate(PARAMS_M, 4800.0, 4800.0 / R_BM, AGE)
lastm = hm["rows"][-1]
nearm = min(hm["rows"], key=lambda r: abs(r["t_gyr"] + 3.7))
row(abs(lastm["t_m"] - 1382.90) < 5.0 and abs(lastm["t_c"] - 3893.07) < 5.0 and abs(nearm["t_m"] - 1669.12) < 5.0,
    f"적응 화성 → T_p {lastm['t_m']:.2f} · T_c {lastm['t_c']:.2f} · T_p@3.7Ga {nearm['t_m']:.2f} K · {hm['n_steps']} 걸음 · 최소 h {hm['h_min_myr']:.4f} Myr "
    f"(스윕 0.25 Myr 대비 {lastm['t_m']-1382.90:+.2f} / {lastm['t_c']-3893.07:+.2f} / {nearm['t_m']-1669.12:+.2f} K, {time.perf_counter()-t0:.0f} s)")

print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
