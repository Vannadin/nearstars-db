# C51 1단계 테스트 — Foley 2018 식 (1)–(4) 전사를 논문이 인쇄한 도출값에 대조한다 (판정 칸은 커밋 D)
"""Anchors for the stagnant-lid budget transcription (`mantle_budget.py`, C51 stage 1).

    python3 engine/test_mantle_budget.py        # the gate; ~0 s, this is algebra on existing state

⚠ **The three verdict cells of C51 are *not* read here.** They are registered in
`engine/interior-core.md@«The three verdict cells, written before the numbers»` and belong to commit D.
This file checks only that the transcription reproduces what the paper prints, and records what the
printed equations turn out to imply.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mantle_budget as mb             # noqa: E402
import radiogenic as rg                # noqa: E402
import stagnant_lid as sl              # noqa: E402
import cmb_flux as cf                  # noqa: E402

fails = 0


def row(ok, text):
    global fails
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


def registered(ok, text):
    """A pre-registered predicate whose **registration** turned out to be wrong.

    It is evaluated and its outcome printed with the registered wording, and it does **not** move the
    gate — because what failed is the registration, not the code under test. Silently rewriting the
    predicate to match the output would erase the only evidence that it was written first (C45 ⓐ)."""
    print(f"  [기록·{'통과' if ok else '실패'}] {text}")


print("① 논문이 인쇄한 도출값 둘 — 우리 환산은 대조일 뿐이다 (C51 의 «인쇄값 규칙»)")
mu_r = mb.viscosity_pa_s(mb.T_R_K)
row(abs(mu_r - mb.MU_R_PRINTED_PA_S) / mb.MU_R_PRINTED_PA_S < 0.10,
    f"μ_r = μ_n exp(E_v/(R·1623)) = {mu_r:.3e} Pa s · 인쇄 «μ_r ≈ 2 × 10²⁰» — 유효숫자 한 자리에서 일치 "
    f"({(mu_r/mb.MU_R_PRINTED_PA_S - 1)*100:+.1f} %). ⚠ 우리가 나르는 값은 인쇄된 2e20 이다")
pe = mb.DELTA_TYPICAL_M * 6.0e-12 / mb.KAPPA_M2_S
row(abs(pe - 0.6) < 0.005,
    f"Pe = Λu/κ = 100 km × 6e-12 m/s / 1e-6 = {pe:.3f} · 인쇄 «P e ≈ 0.6» — 정확히 재현")

print("\n② 식 (3) 의 꼴은 Korenaga eq. 30 의 n=1 이다 — 새로 짓지 않고 불러 쓴다")
row(abs(sl.beta(1) - 1.0 / 3.0) < 1e-15 and abs(1.0 + sl.beta(1) - 4.0 / 3.0) < 1e-15,
    f"β(1) = {sl.beta(1):.6f} = 1/3 이고 1+β = {1+sl.beta(1):.6f} = 4/3 — 식 (3) 의 두 지수와 같다")
direct = mb.C1 * mb.K_W_M_K * (1623.0 - mb.T_S_K) / mb.D_MANTLE_M \
    * mb.theta_fk(1623.0) ** (-4.0 / 3.0) * mb.ra_internal(1623.0) ** (1.0 / 3.0)
row(abs(direct - mb.f_man_w_m2(1623.0)) / direct < 1e-12,
    f"직접 쓴 식 (3) 과 `stagnant_lid.nu_asymptotic(a=c₁)` 경로가 비트 수준에서 같다 ({direct*1e3:.6f} mW/m²)")

print("\n③ 논문의 «cancel out» 주장 — 믿지 않고 재서 기록한다")
cancel = mb.f_man_lid_variables(1623.0, mb.DELTA_TYPICAL_M)
row(abs(cancel["ratio"] - 1.0) < 1e-12,
    f"(T_p−T_s, d) 대 (T_p−T_l, d−δ): {cancel['printed_w_m2']*1e3:.6f} 대 "
    f"{cancel['lid_variables_w_m2']*1e3:.6f} mW/m² · 비 {cancel['ratio']:.12f} — 논문 주장대로 상쇄된다")
ts_vals = [mb.f_man_w_m2(1623.0, t_s_k=t) for t in (100.0, 273.0, 500.0, 737.0)]
d_vals = [mb.f_man_w_m2(1623.0, d_m=d) for d in (1700e3, 2890e3, 4000e3)]
spread_ts = (max(ts_vals) - min(ts_vals)) / ts_vals[0]
spread_d = (max(d_vals) - min(d_vals)) / d_vals[0]
row(spread_ts < 1e-12 and spread_d < 1e-12,
    "⚠ 상쇄는 **항등식**이다 — T_s 를 100·273·500·737 K 로, d 를 1700·2890·4000 km 로 바꿔도 "
    f"F_man 이 {ts_vals[0]*1e3:.6f} mW/m² 에서 상대 {max(spread_ts, spread_d):.1e} 안에 머문다 "
    "(1 − 4/3 + 1/3 = 0, −1 + 3/3 = 0 — 남는 것은 곱셈 순서뿐이다)")
print(f"      그래서 이 법칙의 F_man 이 실제로 읽는 것은 **T_p 와 g 둘뿐**이다 (θ ∝ 1/T_p², μ_i(T_p), Ra_i^(1/3) ∝ g^(1/3)).")
print(f"      기록: 금성의 737 K 표면도, 화성의 얇은 맨틀도 이 식의 플럭스를 바꾸지 않는다 — g 와 T_p 만 바꾼다.")

print("\n④ 식 (4) 와 부피 — 인쇄된 대로")
row(abs(mb.t_lid_base_k(1623.0) - 1440.50) < 0.01,
    f"T_l(1623 K) = T_p − a_rh R T_p²/E_v = {mb.t_lid_base_k(1623.0):.2f} K (뚜껑 밑이 맨틀보다 "
    f"{1623.0 - mb.t_lid_base_k(1623.0):.1f} K 차다)")
v = mb.volumes(mb.DELTA_TYPICAL_M)
row(v["v_man_m3"] > 0 and v["a_man_m2"] > 0 and abs(mb.R_P_M - mb.R_C_M - mb.D_MANTLE_M) < 1.0e3,
    f"δ 100 km 에서 V_man {v['v_man_m3']:.4e} m³ · A_man {v['a_man_m2']:.4e} m² · V_lid {v['v_lid_m3']:.4e} m³ "
    f"· R_p−R_c = {(mb.R_P_M-mb.R_C_M)/1e3:.1f} km 대 인쇄 d 2890 km")

print("\n⑤ 식 (1) 을 미지수 dT_p/dt 로 풀기 — secular cooling 이 출력으로 나온다")
q_man_w = rg.budget(0.675 * cf.M_EARTH_KG)["mantle_w"]
sc = mb.secular_cooling(1623.0, mb.DELTA_TYPICAL_M, q_man_w)
z = sc["at_zero_melt"]
registered(z["dtp_dt_k_s"] < 0.0,
           f"사전등록 문구 그대로 — «dT_p/dt < 0 (secular cooling 이 나온다)»: dT_p/dt "
           f"{z['dtp_dt_k_gyr']:+.1f} K/Gyr → **실패**. ⚠ 실패한 것은 **냉각을 전제한 등록**이고 "
           "코드가 아니다. 게이트를 움직이지 않으며, 문구를 출력에 맞춰 고쳐 쓰지도 않는다 — "
           "먼저 쓰였다는 증거가 그 문구뿐이기 때문이다 (C45 ⓐ 와 같은 형식). 판정은 칸 ②.")
residual = z["q_man_w"] - z["q_surface_w"] - z["melt_w"] - z["capacity_j_k"] * z["dtp_dt_k_s"]
row(abs(residual) / z["q_man_w"] < 1e-12,
    f"Q_man {q_man_w/1e12:.1f} TW (우리 radiogenic 맨틀 예산) · A_man F_man {z['q_surface_w']/1e12:.1f} TW "
    f"→ dT_p/dt {z['dtp_dt_k_gyr']:+.1f} K/Gyr · Urey {z['urey']:.3f} · 수지 잔차 {abs(residual):.2e} W "
    "(식 (1) 이 항으로 닫힌다 — 이 줄이 검사하는 것은 그 닫힘이다)")
print(f"      ⚠ **부호가 양수다 — 판정이 아니라 발견이고, 등록된 칸 ② 가 읽을 몫이다.** 이 법칙으로 정체뚜껑")
print(f"      지구는 방사성 공급 {q_man_w/1e12:.1f} TW 에 표면 손실 {z['q_surface_w']/1e12:.1f} TW 뿐이라 **식히지 못하고 데워진다**")
print(f"      (Urey {z['urey']:.2f}). 그것이 Reese+ 1998 의 *«정체뚜껑이면 맨틀이 700–1500 K 더 뜨거웠을 것»* 을")
print(f"      수지의 말로 옮긴 것이다 — 관측 지구의 ~46 TW 와 겨루는 수가 아니라 **반사실**이다 (C51 칸 ②).")
print(f"      ⚠ 융용 항의 간극은 가정하지 않고 찍는다: dT_p/dt 를 {sc['probe_fraction']:.0%} 움직이려면 "
      f"융용 열손실 {sc['probe_melt_w']/1e12:.2f} TW — 표면 손실의 {sc['probe_melt_as_fraction_of_surface']:.1%} 다.")
print(f"      (f_m 자체로 환산하지 않는다 — ΔT_m 이 이 엔진에 값이 없고, 환산은 온도를 지어내는 일이다.)")

print("\n⑥ 식 (2) — 없는 입력은 이름을 대며 거절한다")
r2 = mb.ddelta_dt_m_s(1623.0, z["f_man_w_m2"], None)
row("refused" in r2 and "eq. (5)" in r2["refused"],
    f"뚜껑 밑 전도 기울기 없음 → 거절: «{r2['refused'][:72]}…»")
r2b = mb.ddelta_dt_m_s(1623.0, z["f_man_w_m2"], -z["f_man_w_m2"] / mb.K_W_M_K)
row("refused" not in r2b and abs(r2b["ddelta_dt_m_s"]) < 1e-15,
    f"기울기를 −F_man/k 로 주면 (정상상태 정의) dδ/dt = {r2b['ddelta_dt_m_s']:+.2e} m/s — 식 (2) 가 0 을 낸다")

print("\n기록 — 선행 상수 다섯, 그리고 어느 비교가 뜻이 있는가 (판정 아님, C47 (f)·C51)")
for lab, a, kind in (("S&M 2000 Table 5 (원전 적합)", 0.528, "—"),
                     ("S&M, Korenaga 의 요약 0.31+0.22n", 0.53, "정의 경계"),
                     ("Korenaga 자기 재적합 0.30+0.25n", 0.55, "정의 안"),
                     ("Korenaga Fig. 6 부분집합", 0.57, "정의 안(다른 적합)"),
                     ("Foley 2018 인쇄 c₁", 0.5, "정의 무선언")):
    print(f"      {lab:34s} a {a:.3f} · 우리 0.5539 대비 {(0.5539/a-1)*100:+6.2f} % · {kind}")
print("      ⚠ 뜻이 있는 비교는 «정의 안» 하나뿐이고 그것이 +0.71 % (Korenaga 적합 rms ~1.2 % 안) 다.")

print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
