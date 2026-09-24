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
import mantle_flux as mf
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
          "h_core": ce.H_CORE, "h_m_present_w": rg.budget(0.675 * M)["mantle_w"],
          # ⚠ **픽스처도 표면온도를 명시로 적는다.** 레시피는 바디 선언을 요구하고 기본값을
          #   안 쓴다 — 손수 짠 `params` 만 모듈 값을 쓰면 두 경로가 다른 수로 돈다.
          "t_surface_k": mf.T_S}
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
# ⚠ **Mantle heating: Nimmo's printed present-day product, history ours (Nimmo does not print it).** Nimmo+ 2004
#   Table 4 (PDF p. 7) prints the present H_m M_m = 23.4 TW (Table 2: "Hm 5.3 pW kg−1", from the abundances of
#   Sun & McDonough 1989, PDF p. 6). M_m and whether "mantle" includes the crust are not printed (PDF pp. 6–7
#   searched), so the product is taken as printed. The decay history is `radiogenic.history_factor` of our
#   set — not Sun & McDonough 1989 ratios (not cached). Until 2026-09-24 this row carried `rg.budget`'s
#   mantle_w (15.22 TW, crust removed), so its old anchor (1525.46 · 4027.43) was «our set + Nimmo core
#   condition», not a reproduction of Nimmo's mantle.
H_M_M_NIMMO_W = 23.4e12               # W — Nimmo+ 2004 Table 4, present-day H_m M_m (printed product).
PARAMS_NIMMO = {**PARAMS, "h_core": H_NIMMO, "h_m_present_w": H_M_M_NIMMO_W}

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
    # ⚠ **2026-09-24 re-freeze (radiogenic landing, Ruedas 2017 mass-weighted).** Declared-H row 1517.34 → 1519.86 ·
    #   3911.29 → 3910.45. Nimmo row: mantle heating switched to Table 4's printed H_m M_m 23.4 TW (was our
    #   mantle_w 15.22 TW, crust removed), so 1525.46 → 1586.452 · 4027.43 → 4004.202;
    #   pinned to three decimals.
    row(fixed_n["n_steps"] == 1135 and abs(fx_n["t_m"] - 1586.452) < 0.005 and abs(fx_n["t_c"] - 4004.202) < 0.005,
        f"고정 4 Myr — Nimmo 현재 H_m M_m(Table 4) · 이력 우리 벌 · 핵 Table 4 조건 (H 1.5 pW/kg): {fixed_n['n_steps']} 걸음 (앵커 1135) · T_p {fx_n['t_m']:.2f} K (앵커 1586.452) · "
        f"T_c {fx_n['t_c']:.2f} K (앵커 4004.202)")
    fixed = ch.integrate(PARAMS, T_C0, T_M0, AGE, adaptive=False)
    row(fixed["n_steps"] == 1135 and abs(fixed["rows"][-1]["t_m"] - 1519.86) < 0.005 and abs(fixed["rows"][-1]["t_c"] - 3910.45) < 0.005
        and abs(fixed["rows"][-1]["t_m"] - hist["rows"][-1]["t_m"]) < 0.01,
        f"선언 H 0.088 pW/kg (오너 결정 ⑤ · 브리프 166 E 환산 정정): 1135 걸음 · T_p {fixed['rows'][-1]['t_m']:.2f} K (앵커 1519.86) · "
        f"T_c {fixed['rows'][-1]['t_c']:.2f} K (앵커 3910.45) · 적응과의 차 {hist['rows'][-1]['t_m'] - fixed['rows'][-1]['t_m']:+.4f} K")
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
# ⚠ 표면온도를 명시로 넘긴다 — 레시피는 선언을 요구하고 모듈 기본값을 안 쓴다 (결정 8).
res = ch.solve(1.0, 0.325, v["core_radius"], v["cmb_pressure"], v["cmb_temperature"], 1600.0, 1.0, AGE,
               T_C0, T_M0, surface_temperature_k=mf.T_S, run_sweep=False)
row(res.applicable and res.values["inner_core_case"] == "never" and res.values["history_converged"] is None,
    f"solve(): {res.regime} · {res.values['entropy_history_verdict'][:40]}… · 수렴 필드 None (스윕은 온디맨드)")
row(all(k in res.units for k in res.values), "모든 값에 단위")
r2 = ch.solve(1.0, 0.325, v["core_radius"], v["cmb_pressure"], v["cmb_temperature"], 1600.0, 1.0, AGE, None, None)
row(not r2.applicable and "initial" in r2.reason, "초기온도 미선언 → 이름 붙여 거절")
r3 = ch.solve(1.0, 0.325, v["core_radius"], v["cmb_pressure"], v["cmb_temperature"], 1600.0, 1.0, AGE, T_C0, T_M0,
              body_class="giant", surface_temperature_k=mf.T_S)
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
            "h_core": ce.H_CORE, "h_m_present_w": rg.budget(0.76 * MM)["mantle_w"],
            "t_surface_k": mf.T_S}
PARAMS_M_NIMMO = {**PARAMS_M, "h_core": H_NIMMO}
try:
    ch.integrate(PARAMS_M_NIMMO, 4800.0, 4800.0 / R_BM, AGE, adaptive=False)
    row(False, "고정 4 Myr 화성이 발산하지 않았다 — C48 의 기록(T_m −6244 K)과 어긋남")
except ValueError as e:
    row("표면온도" in str(e), f"고정 4 Myr 화성 → 발산 (ValueError: {str(e)[:60]}…)")
t0 = time.perf_counter()
hm = ch.integrate(PARAMS_M_NIMMO, 4800.0, 4800.0 / R_BM, AGE)
lastm = hm["rows"][-1]
nearm_t_m = ch.t_at_gyr(hm["rows"], -3.7)       # 보간 — 격자 무관 (사전등록 ec974a1d)
# ⚠ **앵커 셋이 180 C 에서 움직였다** (`61374a86`, 재고정은 180 D). 원인은 ① **압력 분할**이다 —
# 이 노드는 구조 적분기를 지나지 않고 `cmb_flux`·`core_energy` 를 부르는데, 그 둘이
# `core_gamma(mat, p_cmb, t_c)` 를 묻고 **화성의 p_cmb 20.649 GPa 가 Huang 실측 구간(19–35 GPa) 안**
# 이라 γ 가 **1.5 → 2.8718** 로 바뀌었다. 전/후: T_p 1382.90 → 1383.78 · **T_c 3893.07 → 3905.34**
# (+12.27) · T_p@3.7Ga 1669.12 → 1669.99. 허용오차는 그대로 두고 앵커만 옮긴다.
row(abs(lastm["t_m"] - 1383.78) < 5.0 and abs(lastm["t_c"] - 3905.34) < 5.0 and abs(nearm_t_m - 1669.88) < 5.0,
    f"적응 화성 (H 1.5) → T_p {lastm['t_m']:.2f} · T_c {lastm['t_c']:.2f} · T_p@3.7Ga {nearm_t_m:.2f} K · {hm['n_steps']} 걸음 · 최소 h {hm['h_min_myr']:.4f} Myr "
    f"(180 C 전 대비 {lastm['t_m']-1382.90:+.2f} / {lastm['t_c']-3893.07:+.2f} / {nearm_t_m-1669.12:+.2f} K, {time.perf_counter()-t0:.0f} s)")
# The declared-H row. Same trajectory shape (1197 steps, h_min 0.0053 Myr, inner-core branch 'never'); the answer
# moves by −5.87 / −129.91 K. ⚠ The 3.7 Ga column's **rule is part of the number**: `min(rows, key=|t_gyr + 3.7|)`
# — the nearest *sampled* row, never an interpolation. ⚠ **That rule was replaced on 2026-09-19**
# by `core_history.t_at_gyr`, a linear interpolation between the two neighbouring rows; the sentences
# below describe the generation before that, and the numbers they quote are that generation's. Here that row is unique (t = −3.700566 Gyr, |Δ| 0.000566 Gyr
# against the next row's 0.003434) and reads 1668.0021 K at the declared H, so the anchor is 1668.00. ⚠ Brief 166 E moved the declared H from the
# mis-converted 0.14 to 0.088 pW/kg, which moved this column by −0.04 K; at 0.14 it read 1668.0452, and the audit
# seat's run of that condition reported 1668.043744 from a row at −3.700558 Gyr — same trajectory, different row
# grid. Neither deserves its last digits —
# the local step is ~4 Myr, so "nearest row" is ±2 Myr, worth ≈0.19 K, against 5.1 K of criterion-B headroom.
t0 = time.perf_counter()
hmd = ch.integrate(PARAMS_M, 4800.0, 4800.0 / R_BM, AGE)
lastd = hmd["rows"][-1]
neard_t_m = ch.t_at_gyr(hmd["rows"], -3.7)
# ⚠ **같은 원인으로 이 갈래도 움직였다** (180 C → 180 D 재고정): T_p 1377.03 → 1377.96 ·
# **T_c 3763.10 → 3780.60**(+17.50) · T_p@3.7Ga **1668.00 → 1668.79**. 걸음 수 1197 은 불변이다.
# ⚠ **그리고 마지막 수가 기준 B 의 여유를 먹는다** — Herzberg 상한 1673.15 K 까지 **5.15 → 4.36 K**.
# 판정은 여전히 통과지만 C20 이 «5 K 오차면 뒤집힌다» 고 적어 둔 자리라, 방향이 크기보다 중요하다.
# ⚠ **2026-09-19: 3.7 Ga 칸의 규칙이 바뀌어 그 수가 다시 움직였다** — 최근접 표본 행 **1668.79 K** →
# 보간 **1668.68 K**(`core_history.t_at_gyr`). **궤적이 아니라 읽는 규칙이 바뀐 것**이고, 여유는
# 4.36 → **4.47 K** 가 된다. 위 두 줄의 수는 그 전 세대의 것이다.
# ⚠ **2026-09-24 re-freeze (radiogenic landing):** 1377.96 → 1380.65 · 3780.60 → 3779.52 · 1668.68 → 1670.60 — Herzberg headroom 4.47 → 2.55 K.
row(hmd["n_steps"] == 1197 and abs(lastd["t_m"] - 1380.65) < 0.05 and abs(lastd["t_c"] - 3779.52) < 0.05
    and abs(neard_t_m - 1670.60) < 0.05,
    f"선언 H 0.088 화성 → T_p {lastd['t_m']:.2f} · T_c {lastd['t_c']:.2f} · T_p@3.7Ga {neard_t_m:.2f} K · {hmd['n_steps']} 걸음 "
    f"(H 1.5 대비 {lastd['t_m']-lastm['t_m']:+.2f} / {lastd['t_c']-lastm['t_c']:+.2f} / {neard_t_m-nearm_t_m:+.2f} K, {time.perf_counter()-t0:.0f} s) "
    f"— 기준 B: Herzberg [1553.15, 1673.15] K 안 (위끝 여유 {1673.15-neard_t_m:.2f} K)")

# ── 증인 줄 — 측정 장치이고 판정이 아니다 (2026-09-19) ─────────────────────────────
# ⚠ **왜 `repr` 인가.** 이 파일의 판정 줄은 `:.2f` 로 찍고 허용오차가 5 K 다. 그래서 손실 법칙
# 분기(결정 8) 같은 변경이 이 갈래의 수를 **1 K 움직여도 통과한다**. 아래 여섯 칸은 전정밀
# 문자열로 찍히므로, 전후 두 로그에서 **문자열이 같으면 그 갈래는 비트 동일**이고 다르면 어느
# 칸이 움직였는지가 바로 보인다. ⚠ **`row()` 가 아니라 맨 `print()`** — 판정 수를 안 늘린다.
# ⚠ 이 파일이 적분하는 것은 지구와 화성 둘이다. 판도라는 여기 없고 `run.py` 쪽에서 돈다.
def _witness(label, hist_, near_t_m):
    last_ = hist_["rows"][-1]
    print(f"  [증인] {label} — t_m {last_['t_m']!r} · t_c {last_['t_c']!r} · n_steps {hist_['n_steps']!r} · "
          f"h_min_myr {hist_['h_min_myr']!r} · max_h_over_tau {hist_['max_h_over_tau']!r} · "
          f"t_m@3.7Ga {near_t_m!r}")


# ⚠ **어느 갈래에서 나온 수인지 라벨에 박는다.** 지구의 `hist` 는 `--sweep` 이면 고정걸음
# (`sw["h/4"]["hist"]`), 아니면 적응 1152 걸음이다 — 그러면 여섯 칸 중 `n_steps` 와
# `max_h_over_tau`(고정이면 `None`) 가 달라진다. 라벨이 없으면 다른 갈래의 두 로그를 맞대 놓고
# **허수 경보**가 난다. 게이트는 앞 갈래로만 돈다.
_earth_path = "게이트 경로(적응)" if hist.get("adaptive") else "--sweep 경로(고정걸음)"
print("\n증인 — 전정밀 여섯 칸 (판정 아님; 전후 로그에서 문자열로 대조한다)")
_witness(f"지구 (H 선언 · {_earth_path})", hist, ch.t_at_gyr(hist["rows"], -3.7))
_witness("화성 (H 1.5, Brief 166 D 조건)", hm, nearm_t_m)
_witness("화성 (H 선언 0.088)", hmd, neard_t_m)

# ── 결정 8 — 영역이 법칙을 고른다 ────────────────────────────────────────────────
# ⚠ **수를 손으로 다시 치지 않는다.** 바디 선언을 읽어 같은 입력에서 법칙만 갈리게 한다.
# ⚠ **음성 대조가 같이 있어야 한다** — 화성만 보면 «foley 라고 찍혔다» 는 하드코딩 경로에서도
# 똑같이 나온다. 지구(mobile)가 같은 판에서 `nimmo` 를 찍어야 그 줄이 뜻을 가진다.
import yaml                              # noqa: E402

_BODIES = Path(__file__).resolve().parent / "bodies"


def _decl(name):
    return yaml.safe_load((_BODIES / f"{name}.yaml").read_text())["inputs"]


#: ⑦ 절이 바디 선언에 요구하는 키. ⚠ **`.get` 으로 눅이지 않는다** — 빠진 키가 `None` 으로
#: 흘러가면 `ch.solve` 가 `NO_CORE` 로 거절하고, 아래 세 판정은 **조용히 딴 뜻**이 되거나
#: `values` 가 없어 이름 없는 `AttributeError` 로 죽는다. 없으면 **이름 대며 멈춘다**.
#: ⚠ `core_mass_fraction` 은 **여기 없다** — C57 뒤로 그 값은 선언이 아니라 **풀이의 출력**일 수
#: 있고(역산 갈래), 아래 `_cmf()` 가 두 자리를 다 본다. 선언을 요구하면 C57 판에서 멈춘다.
_NEEDS = ("mass_earth", "potential_temperature", "age_gyr",
          "core_initial_temperature", "mantle_initial_potential_temperature")


def _decl_or_stop(decl, body):
    missing = [k for k in _NEEDS if k not in decl]
    if missing:
        raise SystemExit(f"  [STOP] {body}.yaml 에 {' · '.join(missing)} 가 없다 — 결정 8 ⑦ 절은 "
                         f"그 선언을 전제한다. 값이 다른 이름으로 옮겨졌으면 이 자리를 그 이름으로 "
                         f"고쳐라; 느슨하게 읽으면 거절이 판정으로 둔갑한다")
    return decl


def _cmf(res, body):
    """핵질량분율을 **풀린 상태에서** 읽는다 — 선언 판과 역산 판 둘 다.

    ⚠ **두 자리를 다 본다** (병렬석 실측, 2026-09-20): 선언이 남아 있는 트리에서는
    `values` 에 그 키가 **없고** `inputs` 이 0.24 를 든다. 선언을 지우면 역산이 돌아
    **둘 다** 0.23958333333333331 이 된다. `values` 만 읽으면 앞 판에서 `None`,
    `decl[...]` 로 읽으면 뒤 판에서 `KeyError` 다.
    ⚠ **`.get` 으로 눅여서 `None` 을 흘리지 않는다** — 그러면 `ch.solve` 가 `NO_CORE` 로
    거절하고 아래 판정들이 **조용히 딴 뜻**이 된다. 없으면 이름 대며 멈춘다."""
    cmf = res.values.get("core_mass_fraction", res.inputs.get("core_mass_fraction"))
    if cmf is None:
        raise SystemExit(f"  [STOP] {body} 의 핵질량분율을 선언에서도 풀이에서도 못 읽었다 — "
                         f"결정 8 ⑦ 절은 그 값을 전제한다 (느슨하게 읽으면 거절이 판정으로 둔갑한다)")
    return cmf


def _run(decl, age_gyr=None, **over):
    # ⚠ 선언이 없으면 `None` 을 넘겨 **역산 갈래를 연다** — 그 값을 `_cmf()` 가 되읽는다.
    _res = interior_solve(decl["mass_earth"], core_mass_fraction=decl.get("core_mass_fraction"),
                          potential_temperature=decl["potential_temperature"])
    st, _cm = _res.values, _cmf(_res, "화성/지구 중 한 바디")
    kw = {"tectonic_regime": decl.get("tectonic_regime"),
          "lid_thickness_km": decl.get("lid_thickness_km"),
          "surface_temperature_k": decl.get("surface_temperature_k"), **over}
    return ch.solve(mass_earth=decl["mass_earth"], core_mass_fraction=_cm,
                    core_radius_earth=st["core_radius"], cmb_pressure_gpa=st["cmb_pressure"],
                    cmb_temperature=st["cmb_temperature"],
                    potential_temperature=decl["potential_temperature"],
                    radius_earth=st["radius"], age_gyr=age_gyr or decl["age_gyr"],
                    core_initial_temperature=decl["core_initial_temperature"],
                    mantle_initial_potential_temperature=decl["mantle_initial_potential_temperature"],
                    **kw)


def _block(value, grade="measured", source="fixture"):
    return {"value": value, "grade": grade, "source": source}


print("\n⑦ 결정 8 — 선언된 영역이 손실 법칙을 고른다 (법칙 이름은 실행이 낸 값이다)")
_mars_decl = _decl_or_stop(_decl("mars"), "mars")
_earth_decl = _decl_or_stop(_decl("earth"), "earth")
# ⚠ **쌍은 같은 바디에서 법칙만 갈아 끼운 두 판이다.** 지구와 화성을 비교하면 바디가 달라서
# 차이가 법칙의 것이 아니다. 화성을 두 번 돌린다 — 선언대로(foley) 와 영역을 뺀 판(nimmo).
_mars = _run(_mars_decl)
_mars_nimmo = _run(_mars_decl, tectonic_regime=None)
# ⚠ 지구는 **음성 대조**라 법칙 이름만 필요하다. 나이를 0.05 Gyr 로 줄여 부른다 — 법칙 선택은
# 적분 전에 끝나므로 4.54 Gyr 를 더 도는 값이 아무 칸도 안 채운다.
_earth = _run(_earth_decl, age_gyr=0.05)
# ⚠ **줄이 자기 조건을 말하게 한다.** 지구 줄은 `age_gyr 0.05` 픽스처라 오늘값(1517.34)이 아니고,
# 화성 nimmo 는 이 레시피 경로(바디 선언 읽음)라 위 `[증인]` 의 손수 짠 경로와 다른 수다.
# 라벨이 없으면 두 수를 맞대고 「움직였다」로 읽는다.
for _lab, _res in ((f"지구 (mobile · 음성 대조 · age_gyr 0.05 픽스처)", _earth),
                   ("화성 (stagnant · δ 선언 · 레시피 경로)", _mars),
                   ("화성 (영역 뺀 판 · 레시피 경로, 위 [증인] 은 손수 짠 params)", _mars_nimmo)):
    _v = getattr(_res, "values", None) or {}
    print(f"  [증인·법칙] {_lab} — law {_v.get('loss_law')!r} · "
          f"t_m {_v.get('mantle_potential_temperature_present')!r}")
row(_earth.values["loss_law"] == "nimmo" and _mars.values["loss_law"] == "foley"
    and _mars_nimmo.values["loss_law"] == "nimmo",
    f"법칙 선택 — 지구 {_earth.values['loss_law']} · 화성 {_mars.values['loss_law']} · "
    f"화성(영역 뺌) {_mars_nimmo.values['loss_law']} (음성 대조 둘, 같은 줄에서 나온다)")
_dt = (_mars.values["mantle_potential_temperature_present"]
       - _mars_nimmo.values["mantle_potential_temperature_present"])
row(_dt > 0.0,
    f"방향 — 같은 바디·같은 입력에서 foley 가 nimmo 위다 ({_dt:+.2f} K). "
    f"⚠ 크기는 등록 안 했다 — 1739 K 근접은 다른 적분기의 수라 우연이다")

# 갈래 넷 — 오늘 로스터가 안 밟는 자리라 픽스처로만 발화한다. 거절 문구는 `tectonic_regime` 의 것이다.
# ⚠ **`contested` 는 등급도 `contested` 여야 한다** — `tect` 가 값과 등급의 어긋남을 이름 대며 거절한다.
for _name, _over, _want in (
        ("contested → foley (오너 결정 (a) 를 물려받음)",
         {"tectonic_regime": _block("contested", grade="contested")}, "foley"),
        ("transitional → 판단 불가, 이름 대는 거절",
         {"tectonic_regime": _block("transitional")}, "transitional"),
        ("episodic → 매핑 없음, 이름 대는 거절",
         {"tectonic_regime": _block("episodic")}, "no derived-boolean mapping"),
        ("영역 미선언 → Nimmo (사전등록 §1; 거절 아님)",
         {"tectonic_regime": None}, "nimmo")):
    # ⚠ **나이를 0.05 Gyr 로 줄여 부른다.** 이 넷이 재는 것은 **어느 법칙이 골라졌나**이지
    # 오늘 온도가 아니다. 4.54 Gyr 를 네 번 더 적분하면 이 단계가 몇 분 늘어나는데, 그 시간은
    # 아무 칸도 안 채운다 — 법칙 선택은 적분 **전에** 끝난다.
    _r = _run(_mars_decl, age_gyr=0.05, **_over)
    _got = (_r.values or {}).get("loss_law", "") if getattr(_r, "values", None) else ""
    _hit = _want in f"{_got} {_r.reason or ''}"
    row(_hit, f"{_name} — {(_got or _r.regime)!r}"
        + (f" · «{(_r.reason or '')[:64]}…»" if _r.reason else "")
        + ("" if _hit else f" · 기대 문구 «{_want}» 못 찾음"))


print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
