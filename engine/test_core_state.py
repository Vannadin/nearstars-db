# core_state 검사 — 지구 핵의 두 층이 나오는가, 그리고 못 하는 것을 못 한다고 말하는가
"""Anchors for `core_state`.

    python3 engine/test_core_state.py
    python3 engine/test_core_state.py --table     # 문서 §Domain 의 지구 표를 다시 낸다

**판정선은 하나다.** 지구는 외핵이 액체이고 내핵이 고체다. 둘 다 측정된 사실이고,
융해곡선과 핵의 단열선이 둘 다 맞아야 둘 다 맞는다. 여기 쓰는 온도 앵커는 전부 발표된
값이다 — Sinmyo+ 2019 의 핵 쪽 경계 3760 ± 290 K 와 내핵 경계 5120 ± 390 K, 그리고
PREM 의 내핵 경계 압력 328.85 GPa. 우리 출력으로 우리를 시험하지 않는다.
"""
from __future__ import annotations

import sys

import core_state as cs
from core_state import (GAMMA_CORE, PREM_ICB_GPA, SINMYO_EARTH_CMB_K,
                        SINMYO_EARTH_ICB_K, solve)
from eos import MATERIALS
from interior import solve as interior_solve

EARTH = dict(mass_earth=1.0, core_mass_fraction=0.325, potential_temperature=1600.0)
ICB_PRESSURE_TOL = 0.10     # 내핵 경계 압력. 아래 표가 실제 잔차를 낸다
ADIABAT_TOL = 0.05          # γ 검산. Sinmyo 의 두 점을 잇는다


def earth_interior():
    return interior_solve(**EARTH).values


def earth_core(**kw):
    v = earth_interior()
    return solve(core_pressure=v["core_pressure"], cmb_pressure=v["cmb_pressure"],
                 core_temperature=v["core_temperature"],
                 cmb_temperature=v["cmb_temperature"], **kw)


def table() -> None:
    """문서의 지구 표를 다시 낸다. 손으로 친 표는 어긋난다."""
    v = earth_interior()
    r = earth_core(core_cmb_temperature=SINMYO_EARTH_CMB_K[0])
    m = MATERIALS["fe_prem"]
    p_cmb = v["cmb_pressure"] * 1e9
    rho_cmb = m.density(p_cmb, SINMYO_EARTH_CMB_K[0], 0.0)
    t_at_prem_icb = cs._adiabat(m, PREM_ICB_GPA * 1e9, p_cmb,
                                SINMYO_EARTH_CMB_K[0], rho_cmb)
    print("| quantity | derived | published | source | Δ |")
    print("|---|---|---|---|---|")
    print(f"| CMB pressure | {v['cmb_pressure']:.1f} GPa | 135.75 GPa | PREM | "
          f"{(v['cmb_pressure'] / 135.75 - 1) * 100:+.1f} % |")
    print(f"| core temperature at the PREM ICB | {t_at_prem_icb:.0f} K | "
          f"{SINMYO_EARTH_ICB_K[0]:.0f} ± {SINMYO_EARTH_ICB_K[1]:.0f} K | Sinmyo+ 2019 | "
          f"{(t_at_prem_icb / SINMYO_EARTH_ICB_K[0] - 1) * 100:+.1f} % |")
    print(f"| ICB pressure | {r.values['icb_pressure']:.0f} GPa | {PREM_ICB_GPA:.2f} GPa | "
          f"PREM | {(r.values['icb_pressure'] / PREM_ICB_GPA - 1) * 100:+.1f} % |")
    print(f"| conductor phase | {r.values['conductor_phase']} | "
          f"liquid outer core, solid inner core | seismology | – |")


def main() -> int:
    if "--table" in sys.argv:
        table()
        return 0
    fails: list[str] = []
    v = earth_interior()

    print("핵의 단열선 — 발표된 두 점을 잇는가 (γ 가 상수라는 것의 검산)")
    # Sinmyo+ 2019 은 지구 핵의 단열선 위 두 점을 준다. 하나에서 출발해 다른 하나가
    # 나오면 γ = 1.5 가 맞다는 뜻이고, 그건 우리 출력이 아니라 그 논문의 값이다.
    m = MATERIALS["fe_prem"]
    p_cmb = v["cmb_pressure"] * 1e9
    rho_cmb = m.density(p_cmb, SINMYO_EARTH_CMB_K[0], 0.0)
    got = cs._adiabat(m, PREM_ICB_GPA * 1e9, p_cmb, SINMYO_EARTH_CMB_K[0], rho_cmb)
    want, unc = SINMYO_EARTH_ICB_K
    d = abs(got / want - 1.0)
    ok = d <= ADIABAT_TOL
    if not ok:
        fails.append(f"γ = {GAMMA_CORE} 의 단열선이 {SINMYO_EARTH_CMB_K[0]:.0f} K 에서 "
                     f"{got:.0f} K 를 내는데 Sinmyo+ 2019 은 {want:.0f} K 다")
    print(f"  [{'PASS' if ok else 'FAIL'}] {SINMYO_EARTH_CMB_K[0]:.0f} K "
          f"({v['cmb_pressure']:.1f} GPa) → {got:.0f} K ({PREM_ICB_GPA:.2f} GPa) · "
          f"Sinmyo+ 2019 {want:.0f} ± {unc:.0f} K ({d * 100:.2f} %)")

    print("\n판정선 — 지구의 외핵이 액체이고 내핵이 고체로 나오는가")
    r = earth_core(core_cmb_temperature=SINMYO_EARTH_CMB_K[0])
    ok = r.applicable and r.values["conductor_phase"] == cs.CONDUCTOR_MIXED
    if not ok:
        fails.append(f"지구 핵이 '{r.values.get('conductor_phase')}' 로 나온다 — "
                     f"외핵 액체 + 내핵 고체여야 한다")
    print(f"  [{'PASS' if ok else 'FAIL'}] conductor_phase "
          f"{r.values.get('conductor_phase')}")
    icb = r.values["icb_pressure"]
    d = abs(icb / PREM_ICB_GPA - 1.0)
    ok = d <= ICB_PRESSURE_TOL
    if not ok:
        fails.append(f"내핵 경계가 {icb:.0f} GPa, PREM 은 {PREM_ICB_GPA:.2f} GPa "
                     f"({d * 100:.1f} % 차)")
    print(f"  [{'PASS' if ok else 'FAIL'}] 내핵 경계 {icb:.0f} GPa · PREM "
          f"{PREM_ICB_GPA:.2f} GPa ({(icb / PREM_ICB_GPA - 1) * 100:+.1f} %)")
    print(f"         융해온도가 경계 {r.values['cmb_melt_temperature']:.0f} K · 중심 "
          f"{r.values['center_melt_temperature']:.0f} K 이고, 단열선이 "
          f"{r.values['core_cmb_temperature_used']:.0f} → "
          f"{r.values['core_center_temperature_used']:.0f} K 다. 잔차가 압력으로 "
          f"{(icb / PREM_ICB_GPA - 1) * 100:+.0f} % 인 것은 중심 근처에서 두 곡선이 거의 "
          f"나란해서다 — 융해온도 1 % 가 경계를 수십 GPa 옮긴다.")

    print("\n선언이 없으면 — '액체' 는 말하고 '고체' 는 말하지 않는가")
    b = earth_core()
    ok = b.values["conductor_phase"] == cs.CONDUCTOR_UNDECIDED
    if not ok:
        fails.append(f"선언 없는 지구가 '{b.values['conductor_phase']}' 로 나온다 — "
                     f"하한만으로는 판정할 수 없다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 선언 없는 지구 → {b.values['conductor_phase']} "
          f"(하한 {v['cmb_temperature']:.0f} K < 융해 "
          f"{b.values['cmb_melt_temperature']:.0f} K)")
    ok = b.grade == "judgment" and r.grade == "analog"
    if not ok:
        fails.append(f"등급이 선언 의존도를 반영하지 않는다 — 하한 {b.grade}, 선언 {r.grade}")
    print(f"  [{'PASS' if ok else 'FAIL'}] 등급: 하한 갈래 {b.grade} · 선언 갈래 {r.grade} "
          f"(calibrated 는 어느 쪽도 아니다)")
    # 하한 갈래가 solid 를 낼 수 있는 입력이 있으면 안 된다. 아주 차가운 핵을 넣어 본다.
    cold = solve(core_pressure=v["core_pressure"], cmb_pressure=v["cmb_pressure"],
                 core_temperature=300.0, cmb_temperature=300.0)
    ok = cold.values["conductor_phase"] != cs.CONDUCTOR_SOLID
    if not ok:
        fails.append("하한 갈래가 'solid' 를 냈다 — 하한은 한쪽만 묶는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 아주 차가운 하한도 "
          f"'{cold.values['conductor_phase']}' 이지 'solid' 가 아니다")
    # 반대로 아주 뜨거우면 선언 없이도 '액체' 를 낸다.
    hot = solve(core_pressure=v["core_pressure"], cmb_pressure=v["cmb_pressure"],
                core_temperature=9000.0, cmb_temperature=8000.0)
    ok = hot.values["conductor_phase"] == cs.CONDUCTOR_LIQUID
    if not ok:
        fails.append("하한이 융해온도를 넘는데도 '액체' 라고 말하지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 하한이 융해온도를 넘으면 선언 없이도 "
          f"'{hot.values['conductor_phase']}' 다")

    print("\n판정의 여유 — 브리프 42: 얼마나 얇은가를 판정과 함께 내는가")
    # 밀도는 비로만 들어와 상쇄된다: ρ₀ 를 ±10 % 해도 중심 온도가 그대로다.
    from dataclasses import replace as _r
    ph = m.phases[0]
    p_c = v["core_pressure"] * 1e9
    t_base = cs._center_temperature(m, p_c, p_cmb, SINMYO_EARTH_CMB_K[0])
    moved = max(abs(cs._center_temperature(_r(m, phases=(_r(ph, rho0=ph.rho0 * s),)),
                                           p_c, p_cmb, SINMYO_EARTH_CMB_K[0]) - t_base)
                for s in (0.9, 1.1))
    ok = moved < 1e-6
    if not ok:
        fails.append(f"ρ₀ ±10 % 가 중심 온도를 {moved:.2e} K 움직인다 — 밀도가 상쇄되지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] ρ₀ ±10 % → 중심 온도 변화 {moved:.1e} K (비로만 들어와 상쇄)")
    mv = r.values
    ok = (mv["margin_condition"] == cs.MARGIN_THIN and -25.0 < mv["center_margin"] < -10.0
          and mv["gamma_flip_in_alfe_range"] is True
          and cs.GAMMA_SPAN[0] <= mv["gamma_flip"] <= cs.GAMMA_SPAN[1])
    if not ok:
        fails.append(f"지구 중심 여유 {mv['center_margin']:+.1f} K / {mv['margin_condition']} — "
                     f"−17.6 K, thin (γ_flip 이 Alfè 폭 {cs.GAMMA_SPAN} 안) 이어야 한다")
    # 액체 γ 의 양끝이 뒤집힘점을 끼고 있다 — 같은 논문의 액체 값이면 판정이 모호하다는 사실의 고정
    p_cc = v["core_pressure"] * 1e9
    rho_cmb_ = m.density(p_cmb, SINMYO_EARTH_CMB_K[0], 0.0); rho_c_ = m.density(p_cc, SINMYO_EARTH_CMB_K[0], 0.0)
    tm_c = m.t_melt(p_cc)
    mlo = SINMYO_EARTH_CMB_K[0] * (rho_c_ / rho_cmb_) ** cs.GAMMA_LIQUID_RANGE[0] - tm_c
    mhi = SINMYO_EARTH_CMB_K[0] * (rho_c_ / rho_cmb_) ** cs.GAMMA_LIQUID_RANGE[1] - tm_c
    ok2 = mlo < 0.0 < mhi
    if not ok2:
        fails.append(f"액체 γ 1.51/1.52 의 여유 {mlo:+.1f}/{mhi:+.1f} K 가 0 을 끼지 않는다 — 이야기가 바뀌었다")
    print(f"  [{'PASS' if ok2 else 'FAIL'}] 액체 γ {cs.GAMMA_LIQUID_RANGE}: 중심 여유 {mlo:+.1f} → {mhi:+.1f} K (부호가 바뀐다)")
    sd = mv["melt_splice_disagreement"]
    ok3 = sd is not None and 0.040 < sd < 0.045
    if not ok3:
        fails.append(f"중심압에서의 이음매 국소 불일치 {sd} — 4.0–4.5 % 이어야 한다 (358.5 GPa)")
    print(f"  [{'PASS' if ok3 else 'FAIL'}] 이음매 국소 불일치 @ 중심 {sd * 100 if sd else float('nan'):.2f} % "
          f"(300 GPa {cs.melt_splice_disagreement(300e9) * 100:.2f} % → 365 GPa {cs.melt_splice_disagreement(365e9) * 100:.2f} %)")
    kf = cs.k0_flip_gpa(MATERIALS["silicate"], p_cc, p_cmb, SINMYO_EARTH_CMB_K[0])
    ok4 = kf is None
    if not ok4:
        fails.append(f"다상 재료(silicate)에 k0_flip 이 {kf} 를 낸다 — None 으로 거절해야 한다")
    print(f"  [{'PASS' if ok4 else 'FAIL'}] 다상 재료 k0_flip → {kf} (이름 붙인 계산 불가)")
    print(f"  [{'PASS' if ok else 'FAIL'}] 지구 중심 여유 {mv['center_margin']:+.1f} K "
          f"({mv['center_margin_fraction'] * 100:+.2f} %) → {mv['margin_condition']}")
    ok = abs(mv["gamma_flip"] - 1.5145) < 0.002 and abs(mv["k0_flip"] - 194.0) < 1.0
    if not ok:
        fails.append(f"뒤집힘점이 움직였다 — γ {mv['gamma_flip']:.4f} (1.5145), "
                     f"K₀ {mv['k0_flip']:.1f} GPa (194.0)")
    print(f"  [{'PASS' if ok else 'FAIL'}] 중심 판정 뒤집힘: γ {mv['gamma_flip']:.4f} "
          f"(선언 {GAMMA_CORE}) · K₀ {mv['k0_flip']:.1f} GPa (fe_prem {ph.k0 / 1e9:.0f})")
    ok = (b.values["margin_condition"] == cs.MARGIN_NOT_COMPUTABLE
          and b.values["gamma_flip"] is None and b.values["k0_flip"] is None)
    if not ok:
        fails.append("하한 갈래가 뒤집힘점을 낸다 — 단열선이 없으니 못 한다고 말해야 한다 (④)")
    print(f"  [{'PASS' if ok else 'FAIL'}] 하한 갈래 → {b.values['margin_condition']}")

    print("\n온도를 바꾸면 판정이 뒤집히는가 (배선이 살아 있는가)")
    seq = []
    for t_cmb in (2500.0, 3760.0, 12000.0):
        seq.append((t_cmb, earth_core(core_cmb_temperature=t_cmb)
                    .values["conductor_phase"]))
    got = tuple(x[1] for x in seq)
    ok = got == (cs.CONDUCTOR_SOLID, cs.CONDUCTOR_MIXED, cs.CONDUCTOR_LIQUID)
    if not ok:
        fails.append(f"핵 쪽 경계 온도를 올려도 판정이 solid → 섞임 → liquid 로 가지 "
                     f"않는다: {got}")
    for t_cmb, phase in seq:
        print(f"  [{'PASS' if ok else 'FAIL'}] 핵 쪽 경계 {t_cmb:6.0f} K → {phase}")

    print("\n거절 — 못 하는 것을 이름 대며 거절하는가")
    cases = (
        ("거대행성", dict(body_class="giant"), "dynamo_giant"),
        ("핵이 없다", dict(cmb_pressure=0.0), "핵이 없다"),
        ("온도가 없다", dict(cmb_temperature=0.0, core_temperature=0.0), "등온"),
        ("융해곡선 밖", dict(core_pressure=6000.0), "상한"),
    )
    base = dict(core_pressure=v["core_pressure"], cmb_pressure=v["cmb_pressure"],
                core_temperature=v["core_temperature"],
                cmb_temperature=v["cmb_temperature"])
    for label, over, needle in cases:
        res = solve(**{**base, **over})
        ok = (not res.applicable) and needle in res.reason
        if not ok:
            fails.append(f"거절 '{label}': 이유가 '{needle}' 를 말하지 않는다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:10} → {res.reason[:66]}…")
    # 2026-09-02(브리프 36)까지 이 검사의 재료는 silicate 였다 — 규산염이 녹는곡선을
    # 얻으면서 그 재료로는 이 조건(곡선 없음)을 더는 시험할 수 없어 antigorite 로
    # 바꿨다 (빈 melt 가 판정인 재료). 규산염 핵은 아래에서 새 경로를 따로 고정한다.
    res = solve(**{**base, "core_material": "antigorite"})
    ok = (not res.applicable) and "융해곡선이 없다" in res.reason
    if not ok:
        fails.append("융해곡선 없는 재료를 이름 대며 거절하지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 사문석 핵 → {res.reason[:66]}…")
    # 규산염 핵은 이제 곡선이 있어 하한 갈래까지 가고, 거기서 원칙 있는 미판정을
    # 낸다 — 하한 지오섬이 융해온도 아래면 액체라 못 하고, 하한은 한쪽만 묶으므로
    # 고체라고도 못 한다. 상계 독법과 같은 결의 거절이고, 이 경로가 브리프 36 의
    # 의도된 변화다.
    res = solve(**{**base, "core_material": "silicate"})
    ok = (res.applicable and res.values.get("conductor_phase") == "undecided"
          and "하한" in res.reason)
    if not ok:
        fails.append(f"규산염 핵이 하한 갈래의 미판정에 닿지 않는다 — {res.reason[:60]}")
    print(f"  [{'PASS' if ok else 'FAIL'}] 규산염 핵 → {res.reason[:66]}…")

    print("\n계약 — 페이로드가 제 몫을 하는가")
    for label, cond in (
            ("inputs 기록", set(r.inputs) >= {"core_pressure", "cmb_temperature"}),
            ("모든 값에 단위", set(r.values) <= set(r.units)),
            ("conductor_phase 가 출력", "conductor_phase" in r.values),
            ("근거 동반", bool(r.refs)),
            ("선언을 note 가 이름 댐",
             any("선언이다" in n for n in r.notes)),
            ("등급이 calibrated 가 아님", r.grade != "calibrated")):
        if not cond:
            fails.append(f"계약: {label}")
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    print(f"  {r.evidence()[:150]}")


    print("\n공정 바운드 — Mori+ 2017 전사와 괄호 측정 (브리프 38)")
    from eos import iron_fes_eutectic_t_melt, iron_t_melt, IRON_LIGHT_ELEMENT_FACTOR
    # 전사 검산 넷 — 논문 자신이 인쇄한 값. 네 번째의 "~4100 at the ICB" 는 자기 곡선 위
    # ~350 GPa 의 값(라벨 세부, 결함 아님 — 판정 완료, paper-defects 에 넣지 말 것).
    for g, printed, tol, what in ((60.0, 1910.0, 6.0, "run #6"),
                                  (254.0, 3550.0, 10.0, "run #11"),
                                  (136.0, 2700.0, 20.0, "'~2700 K at the CMB'"),
                                  (350.0, 4100.0, 5.0, "'~4100 K at the ICB' (~350 GPa)")):
        got = iron_fes_eutectic_t_melt(g * 1e9)
        ok = got is not None and abs(got - printed) <= tol
        if not ok:
            fails.append(f"Mori 전사: {g} GPa 에서 {got} vs 인쇄 {printed} ({what}) — "
                         "인쇄점이 자기 식에서 안 나온다. 계수를 만지지 말고 멈춰라")
        print(f"  [{'PASS' if ok else 'FAIL'}] {g:5.0f} GPa → {got:6.1f} K (인쇄 ~{printed:.0f}, {what})")
    ok = (iron_fes_eutectic_t_melt(20e9) is None
          and iron_fes_eutectic_t_melt(351e9) is None)
    if not ok:
        fails.append("공정 곡선이 21–350 GPa 밖에서 값을 낸다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 21 GPa 아래·350 GPa 위는 None — "
          "10–21 GPa 공백은 IRON_FES_GAP_REASON 이 이름 댄다")
    # Sinmyo 검산의 재계산 (브리프 38 E) — 리터럴이던 19.1 이 계산값이 됐고, PREM ICB
    # 압력에서 ~19 % 로 돌아와야 한다. 갈래 ③ 감시.
    pct = (1.0 - SINMYO_EARTH_ICB_K[0] / iron_t_melt(PREM_ICB_GPA * 1e9)) * 100.0
    ok = 18.5 <= pct <= 19.5
    if not ok:
        fails.append(f"Sinmyo 내림 재계산이 {pct:.2f} % — ~19 에서 이탈 (갈래 ③): "
                     "iron_t_melt 나 앵커가 움직였다. 바꾸기 전에 델타와 압력을 보고하라")
    print(f"  [{'PASS' if ok else 'FAIL'}] Sinmyo 5120 K vs 순철 @ {PREM_ICB_GPA:.2f} GPa → "
          f"{pct:.2f} % (리터럴이 아니라 계산)")
    # 괄호 측정 (브리프 38 F, 갈래 ④): 로스터 전원이 0.80 상수이므로 선언 융해곡선이
    # 공정 바닥을 위반할 수 없다 — 21–350 GPa 최소 여유가 양수임을 재서 C5 로 닫는다.
    # 이 최소 여유(+407.5 K @ 48 GPa, 2026-09-02 측정)가 움직이면 곡선 중 하나가 움직인 것.
    margin = min(IRON_LIGHT_ELEMENT_FACTOR * iron_t_melt(p * 1e9)
                 - iron_fes_eutectic_t_melt(p * 1e9) for p in range(21, 351))
    ok = 400.0 < margin < 415.0
    if not ok:
        fails.append(f"괄호 최소 여유 {margin:.1f} K — 기록 +407.5 에서 이탈. "
                     "공정이나 순철 곡선이 움직였다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 선언(×0.80) − 공정 바닥의 21–350 GPa 최소 여유 "
          f"{margin:+.1f} K — 위반 가능 천체 0, 런타임 배선은 C5 로 안 지었다")

    if fails:
        print(f"\n실패 {len(fails)}건")
        for f in fails:
            print(f"  · {f}")
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
