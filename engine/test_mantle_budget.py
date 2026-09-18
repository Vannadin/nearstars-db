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
print(f"      ⚠ 용융 항의 간극은 가정하지 않고 찍는다: dT_p/dt 를 {sc['probe_fraction']:.0%} 움직이려면 "
      f"용융 열손실 {sc['probe_melt_w']/1e12:.2f} TW — 표면 손실의 {sc['probe_melt_as_fraction_of_surface']:.1%} 다.")
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

print("\n⑦ 2단계 — 시간 적분 (C51 Stage 2, 사전등록 1f907a63 + 개정 1)")
import time                                                        # noqa: E402

# ⚠ **수락선 A — 현재 시점은 비트까지 그대로여야 한다.** 적분기는 1단계를 감쌀 뿐이므로
#   t0 == t1 이면 걸음을 한 번도 안 밟고 같은 수를 돌려줘야 한다. 「거의 같다」가 아니라 **같다**.
still = mb.integrate_tp(1623.0, mb.DELTA_TYPICAL_M, lambda _t: q_man_w, 0.0, 0.0, steps=1)
row(still["steps"] == 0
    and still["t_p_end_k"] == 1623.0
    and still["end_state"]["f_man_w_m2"] == z["f_man_w_m2"]
    and still["end_state"]["dtp_dt_k_s"] == z["dtp_dt_k_s"]
    and still["end_state"]["urey"] == z["urey"],
    f"t0 = t1 이면 걸음 {still['steps']} · F_man {still['end_state']['f_man_w_m2']*1e3:.10f} mW/m² · "
    f"dT_p/dt {still['end_state']['dtp_dt_k_gyr']:+.7f} K/Gyr — 1단계와 **비트 동일**")

# Q_man(t) 는 이 파일이 안 고른다 — `radiogenic` 이 답한다. t_gyr 은 **오늘을 0** 으로 두는 축이라
# 과거는 음수이고, 그때 붕괴 인자 2^(−t/t_half) 가 1 보다 커진다 (과거가 더 뜨겁다).
SIL_EARTH_KG = 0.675 * cf.M_EARTH_KG


def q_man_at(t_gyr):
    return rg.budget(SIL_EARTH_KG, t_gyr=t_gyr)["mantle_w"]


# ⚠ **출발점은 시점이 붙은 쪽이다** — 오늘 값을 과거에 놓지 않는다. 초기 T_p 의 인쇄 출처를 못
#   찾았고(보유 논문 셋, ADS 질의 안 돌림), Korenaga 2008 §[76] 은 그 부재를 «poorly known initial
#   condition» 으로 적는다. 그래서 **오늘에서 뒤로** 적분해 초기값을 도출한다.
t_start = time.perf_counter()
run = mb.integrate_tp(1623.0, mb.DELTA_TYPICAL_M, q_man_at, 0.0, -4.5, steps=450)
elapsed = time.perf_counter() - t_start
# ⚠ **수락선 E — 걸음 예산을 인쇄한다.** 단계 수가 74 로 그대로여도 이 비용은 기존 단계 **안**에
#   숨는다. 그래서 수를 찍는다.
# ⚠ **이 줄이 거는 것은 걸음 예산뿐이다.** 끝 온도에는 등록된 폭이 없으므로 **판정 안 한다** —
#   「어떤 값이어도 통과하는 단언」을 PASS 로 찍으면 검사가 있는 척만 한다 (감사석 ㉠).
row(run["steps"] == 450 and run["h_gyr"] == (-4.5 - 0.0) / 450,
    f"4.5 Gyr 뒤로 적분 — 걸음 {run['steps']} · 걸음 크기 {run['h_gyr']:+.4f} Gyr (요청과 일치) · "
    f"벽시계 {elapsed*1e3:.0f} ms")
print(f"      [인쇄, 판정 아님] 오늘 T_p 1623.0 K (t = 0) → −4.5 Gyr 의 T_p {run['t_p_end_k']:.1f} K (도출)")
print(f"      과거 쪽 Q_man {q_man_at(-4.5)/1e12:.1f} TW · 오늘 {q_man_at(0.0)/1e12:.1f} TW "
      f"(비 {q_man_at(-4.5)/q_man_at(0.0):.2f}) — 붕괴는 `radiogenic` 이 답하고 이 파일이 안 고른다")

# ⚠ **초기조건은 선택이다** (함정 2). 하나로 끝내면 이력이 적분기의 것인지 출발점의 것인지 못 가른다.
alt = mb.integrate_tp(1823.0, mb.DELTA_TYPICAL_M, q_man_at, 0.0, -4.5, steps=450)
# ⚠ **두 번째 출발값은 아예 답이 없다** — 그리고 그것이 이 방향의 성질이다. 앞으로 가는 적분이
#   초기조건의 기억을 지우므로(위 문단), 그 역은 오늘의 작은 차를 **키운다**. 한쪽은 차게, 다른
#   쪽은 뜨겁게 달아난다. 둘 다 «거절» 이고, 죽는 것이 아니라 이름이 붙는다.
row("refused" in alt and "도메인" in alt["refused"],
    f"오늘 값 둘로 뒤로 — 1623 K → −4.5 Gyr 의 {run['t_p_end_k']:.1f} K (도출) · "
    f"1823 K → **거절** (t = {alt['t_end_gyr']:+.3f} Gyr, 걸음 {alt['steps']}/450). "
    "오늘 200 K 차가 뒤로 가면 한쪽은 도메인 밖으로 나간다 — **이 방향은 불안정**하고, "
    "거절이 그 사실을 값으로 말한다")
print(f"      [인쇄, 판정 아님] 거절문: «{alt['refused'][:92]}…»")

end = run["end_state"]
print(f"      −4.5 Gyr 상태 — F_man {end['f_man_w_m2']*1e3:.3f} mW/m² · Urey {end['urey']:.3f} · "
      f"dT_p/dt {end['dtp_dt_k_gyr']:+.1f} K/Gyr (⚠ 오늘 값은 위 ⑤ 가 찍은 1단계 수 그대로다)")
# ⚠ **수락선 B — 인쇄된 궤적과 대조하거나, 못 찾았다면 어디를 찾았는지 적는다.**
print("      ⚠ 인쇄된 `T_p(t)` 궤적과의 대조 **없음**. 찾은 곳: 보유 논문 "
      "`2018AsBio..18..873F`(Foley 2018, 이 수지의 원전) · `2014GeoJI.199..580F`(F&B 2014) · "
      "`2008RvGeo..46.2007K`(Korenaga 2008, Urey 비). ⚠ ADS 질의는 **안 돌렸다** — "
      "«안 찾았다» 와 «찾았는데 없다» 를 가르기 위해 여기 그대로 적는다. 셋에서 우리 초기조건·뚜껑 "
      "고정과 같은 조건의 인쇄 궤적을 못 봤다는 것이 지금 말할 수 있는 전부다.")
print("      ⚠ **뚜껑 δ 는 이 적분에서 고정이다** — eq. (2) 의 기울기가 eq. (5) 의 출력이고 그것이 "
      "안 지어졌다. 그래서 이 이력은 «뚜껑이 그대로일 때의 온도 이력» 이지 «뚜껑까지 함께 푼 이력» 이 아니다.")

# ── ⑦ 뚜껑 정의역 — 양끝과 **위끝 바로 그 점** (사전등록 08ca4f62) ─────────────────────────
# ⚠ 기하를 **명시로** 넘긴다. 안 넘기면 모듈 기본값이 지구(R_P_M 6378.1 km · R_C_M 3488.1 km,
#   d_m 2890 km)라 화성의 1559.5 km 가 평범한 내부 값으로 **통과**하고 경계를 안 밟는다.
#   ⚠ 여기 쓰는 기하는 `:240` 주석의 것(3389.5 · 1830.0 km)이고, 엔진 정본(0.5320 R⊕ =
#   3389.372 km · r_c 1666.53 → d_m 1722.84 km)과 다르다. 이 시험은 **건네받은 기하의 경계**를
#   재고, 가드의 부등호는 기하와 무관하다. 두 기하 통일은 별 항목이다.
print("⑦ 뚜껑 정의역 — 0 ≤ δ < d_m 의 **양끝과 위끝 그 점**")
_RP_M, _RC_M = 3389.5e3, 1830.0e3
_DM = _RP_M - _RC_M
_q = lambda t_gyr: 1.0e13          # 자리표시자 열원 — 이 시험이 보는 것은 거절이지 온도가 아니다
for _delta, _want in ((2000.0e3, True), (_DM, True), (350.0e3, False), (-1.0e3, True)):
    _r = mb.integrate_tp(1600.0, _delta, _q, 0.0, -0.1, 5, r_p_m=_RP_M, r_c_m=_RC_M)
    _txt = _r.get("refused", "")
    # ⚠ 기대는 **이름 붙은 거절 문구**다. 「예외가 안 났다」가 아니다 — 죽던 것이 안 죽는 것과
    #   거절이 말하는 것은 다르다.
    _ok = ("(0 ≤ δ < d_m)" in _txt) if _want else ("refused" not in _r)
    row(_ok, f"δ {_delta/1e3:>7.1f} km (d_m {_DM/1e3:.1f} km) → "
             + (f"거절: «{_txt[:58]}…»" if _txt else "통과 (거절 없음)"))

print("\n⑧ 같은 정의역, 세 입구 — 문구가 하나인가 (사전등록 B)")
# ⚠ **입구마다 한 행이다.** 한 행이 셋을 덮으면 하나만 고쳐져도 초록이 되고, 그건 이 항목이
#   막으려는 바로 그 모양이다. δ 는 `r_p_m − r_c_m` 으로 **건네받은 기하에서** 만든다 — 이
#   시험이 스스로 1559.5 를 타이핑하면 기하가 바뀌는 날 시험만 옛 수를 지키게 된다.
_DM_B = _RP_M - _RC_M
_WANT = "(0 ≤ δ < d_m)"

try:
    mb.dtp_dt_k_s(1600.0, _DM_B, 1.0e13, r_p_m=_RP_M, r_c_m=_RC_M)
    _got_a, _txt_a = False, "예외가 안 났다"
except mb.LidOutsideMantle as _e:
    _got_a, _txt_a = _WANT in str(_e), str(_e)
row(_got_a, f"`dtp_dt_k_s` δ = d_m → {mb.LidOutsideMantle.__name__}: «{_txt_a[:56]}…»")

try:
    mb.secular_cooling(1600.0, _DM_B, 1.0e13, r_p_m=_RP_M, r_c_m=_RC_M)
    _got_b, _txt_b = False, "예외가 안 났다"
except mb.LidOutsideMantle as _e:
    _got_b, _txt_b = _WANT in str(_e), str(_e)
row(_got_b, f"`secular_cooling` δ = d_m → 같은 예외가 **호출로 상속**: «{_txt_b[:44]}…»")

_r_c = mb.integrate_tp(1600.0, _DM_B, _q, 0.0, -0.1, 5, r_p_m=_RP_M, r_c_m=_RC_M)
row(_WANT in _r_c.get("refused", ""),
    f"`integrate_tp` δ = d_m → dict 규약 그대로: «{_r_c.get('refused', '')[:44]}…»")

# ⚠ 셋이 **같은 문자열**인지 — 함정 1 은 「셋 다 거절한다」가 아니라 「셋이 같은 말을 한다」다.
row(_txt_a == _txt_b == _r_c.get("refused"),
    "세 입구의 문구가 **글자까지 같다** (한 곳에서 지어 나눠 쓴다)")

# 대조 — 같은 실행에서 δ 350 km 는 세 입구 모두 통과한다. 통과가 없으면 「전부 거절」도 초록이다.
_pass_a = mb.dtp_dt_k_s(1600.0, 350.0e3, 1.0e13, r_p_m=_RP_M, r_c_m=_RC_M)
_pass_b = mb.secular_cooling(1600.0, 350.0e3, 1.0e13, r_p_m=_RP_M, r_c_m=_RC_M)
_pass_c = mb.integrate_tp(1600.0, 350.0e3, _q, 0.0, -0.1, 5, r_p_m=_RP_M, r_c_m=_RC_M)
row("dtp_dt_k_s" in _pass_a and "at_zero_melt" in _pass_b and "refused" not in _pass_c,
    "대조 — δ 350 km 는 세 입구 모두 **통과**한다 (거절만 세는 시험이 아님)")

print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
