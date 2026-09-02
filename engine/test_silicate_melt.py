# 규산염 녹는곡선 사슬을 전사 검산·이음매 계단·거절·시딩으로 고정한다 (브리프 36)
"""Anchor the silicate melting chain: transcription, seams, refusals, seeding.

    python3 engine/test_silicate_melt.py

앵커는 인쇄된 수다 — Deng+ 2023 은 자기 Table I 과 자기 인쇄 외삽점(9376 K @ 500 GPa)
으로, Monteux+ 2016 은 자기 20 GPa 조인(리퀴더스 셋이 0.040 K 안에서 만나고 솔리더스가
1.0 K 로 잇는다)으로 검산한다. 인쇄된 점이 자기 식에서 안 나오면 계수를 맞추지 말고
멈춘다. 이음매 계단은 측정된 선언이다 — 움직이면 물질 배정이 바뀐 것이니 크게 울린다.
"""
from __future__ import annotations

import sys

import eos
from eos import (silicate_solidus, silicate_liquidus, silicate_melt_fraction,
                 silicate_melt_refusal, _silicate_melt_point, _simon_pa,
                 MONTEUX_SOL_LOW, MONTEUX_LIQ_LOW, MONTEUX_SOL_HIGH,
                 MONTEUX_LIQ_A, MONTEUX_LIQ_F, DENG_BDG, DENG_PPV, FEI_UPPER,
                 SILICATE_MELT_DH, SILICATE_MELT_POINT_WIDTH, MATERIALS, GPA)


def main() -> int:
    fails: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # ── 1. 전사 검산 — 인쇄된 점이 자기 식에서 도로 나오는가 ────────────────
    # Deng+ 2023: 자기 Table I (용융점을 적합이 ±50 K 안에서 재현한다고 논문이 스스로
    # 말한다) + 인쇄된 외삽 "9376 ± 656 K at 500 GPa".
    bdg = lambda g: DENG_BDG[0] * ((g - DENG_BDG[1]) / DENG_BDG[2] + 1) ** (1 / DENG_BDG[3])
    ppv = lambda g: DENG_PPV[0] * ((g - DENG_PPV[1]) / DENG_PPV[2] + 1) ** (1 / DENG_PPV[3])
    fei = lambda g: FEI_UPPER[0] * (g / FEI_UPPER[1]) ** FEI_UPPER[2]
    for g, tab in [(20, 2875), (40, 4000), (75, 5000), (120, 5750), (160, 6250)]:
        ok(abs(bdg(g) - tab) <= 50.0,
           f"1: Deng bdg {g} GPa — 적합 {bdg(g):.1f} 이 Table I {tab} 에서 ±50 K 밖")
    for g, tab in [(120, 5600), (140, 5950), (180, 6450), (200, 6750)]:
        ok(abs(ppv(g) - tab) <= 50.0,
           f"1: Deng ppv {g} GPa — 적합 {ppv(g):.1f} 이 Table I {tab} 에서 ±50 K 밖")
    ok(abs(ppv(500.0) - 9376.0) < 1.0,
       f"1: Deng 인쇄 외삽점 재현 실패 — {ppv(500.0):.1f} ≠ 9376 (전사가 틀어졌다)")
    ok(abs(fei(140.0) - 6295.0) < 1e-9, "1: Fei 상계가 자기 앵커(140 GPa, 6295 K)를 안 낸다")
    # Monteux 20 GPa 조인: 리퀴더스 셋 0.040 K, 솔리더스 1.002 K — 그리고 오식 스케일
    # (1336e9)이면 745.6 K 로 벌어진다. 이 잔차 셋이 소수점 함정의 삼중 고정핀이다.
    l3 = [_simon_pa(20e9, *c) for c in (MONTEUX_LIQ_LOW, MONTEUX_LIQ_A, MONTEUX_LIQ_F)]
    ok(max(l3) - min(l3) < 0.05,
       f"1: Monteux 리퀴더스 셋의 20 GPa 스프레드 {max(l3)-min(l3):.3f} K — 0.040 이었다")
    d_sol = _simon_pa(20e9, *MONTEUX_SOL_LOW) - _simon_pa(20e9, *MONTEUX_SOL_HIGH)
    ok(abs(d_sol - 1.002) < 0.05,
       f"1: Monteux 솔리더스 조인 {d_sol:+.3f} K — +1.002 였다 (스케일이 움직였다)")
    trap = 1661.2 * (20e9 / 1336e9 + 1) ** (1 / 7.437)
    ok(_simon_pa(20e9, *MONTEUX_SOL_HIGH) - trap > 700.0,
       "1: 오식 스케일(1336e9)의 조인 격차가 사라졌다 — 함정 고정핀이 뜻을 잃었다")

    # ── 2. 이음매 계단 — 측정된 선언, 뭉개지지 않았는가 ─────────────────────
    # 140 GPa 계단의 기준은 **구현 곡선**이다 (감사 정정 2026-09-02): 암석 리퀴더스 →
    # 구현 리퀴더스(tm + 75). 솔리더스 계단(+1732.1, 노트)과 같은 기준이라 독자가 코드로
    # 재현할 수 있다. 기준이 문제가 되는 이유 — 명목 폭 150 K 가 **선언값**이라, tm(중심)
    # 기준(+1200.7/+321.7)과 이 값은 정확히 폭/2 = 75 K 차이가 나고 눈으로 구별이 안 된다.
    # 계단 수치는 그 선언에 의존한다.
    for got, want, name in [
            (silicate_liquidus(140e9) - _simon_pa(140e9, *MONTEUX_LIQ_A), 1275.67,
             "140 GPa 암석(A-liq)→구현 리퀴더스"),
            (silicate_liquidus(140e9) - _simon_pa(140e9, *MONTEUX_LIQ_F), 396.72,
             "140 GPa 암석(F-liq)→구현 리퀴더스"),
            (ppv(180) - bdg(180), 17.98, "180 GPa bdg→ppv (인쇄 삼중점)"),
            (fei(200) - ppv(200), 296.65, "200 GPa ppv→Fei 상계"),
            (fei(500) - ppv(500), 47.62, "500 GPa 사슬 폐합 비교 (Deng 외삽 vs Fei)")]:
        ok(abs(got - want) < 0.5, f"2: 계단 {name} = {got:+.2f} K, 기록 {want:+.2f}")

    # ── 3. 거절 — 이름을 대는가 ─────────────────────────────────────────────
    ok(silicate_solidus(501e9) is None and silicate_liquidus(501e9) is None,
       "3: 500 GPa 위에서 None 이 아니다")
    ok("500 GPa" in silicate_melt_refusal(501e9), "3: 거절문이 상한을 이름 대지 않는다")
    try:
        _silicate_melt_point(5e9)
        fails.append("3: bdg 산술 바닥(11.89 GPa) 아래가 조용히 지나갔다")
    except ValueError as e:
        ok("11.89" in str(e), "3: bdg 바닥 거절이 11.89 를 이름 대지 않는다")
    try:
        silicate_solidus(1e9, "basaltic")
        fails.append("3: 미등록 조성이 조용히 통과했다")
    except ValueError:
        pass

    # ── 4. 용융분율 — 단일 진리원의 성질 ────────────────────────────────────
    p = 1e9
    sol, liq = silicate_solidus(p), silicate_liquidus(p)
    ok(silicate_melt_fraction(p, sol - 1.0) == 0.0, "4: 솔리더스 아래에서 φ ≠ 0")
    ok(silicate_melt_fraction(p, liq + 1.0) == 1.0, "4: 리퀴더스 위에서 φ ≠ 1")
    mid = silicate_melt_fraction(p, 0.5 * (sol + liq))
    ok(abs(mid - 0.5) < 1e-9, "4: 창 중앙에서 φ ≠ 0.5 (식 (6) 선형 지렛대가 아니다)")
    ok(silicate_melt_fraction(p, 1000.0, ) == 0.0 and silicate_melt_fraction(501e9, 5000.0) is None,
       "4: 곡선 밖 처리(500 GPa 위 None)가 틀렸다")
    ok(MATERIALS["silicate"].phases[0].t_melt(p) == sol,
       "4: Phase.t_melt(silicate) 가 솔리더스(첫 용융)와 다른 수를 낸다 — 진리원이 둘이 됐다")
    # 조성이 곡선을 바꾸는 곳은 20 GPa 위 리퀴더스뿐이다
    ok(silicate_liquidus(10e9, "peridotitic") == silicate_liquidus(10e9, "chondritic"),
       "4: 20 GPa 아래에서 조성이 곡선을 바꾼다 — 인쇄된 조성은 하나다")
    dl = silicate_liquidus(140e9 - 1, "peridotitic") - silicate_liquidus(140e9 - 1, "chondritic")
    ok(abs(dl - 878.96) < 1.0,
       f"4: 140 GPa 의 F−A 리퀴더스 차 {dl:.1f} K — 인쇄값 검산 +879 K 이었다")

    # ── 5. 겉보기 비열 (식 17) 과 단열선 평탄화 ─────────────────────────────
    m = MATERIALS["silicate"]
    t_in = 0.5 * (sol + liq)
    lat = SILICATE_MELT_DH / (liq - sol)
    cp_out = m.c_p(p, sol - 50.0)
    cp_in = m.c_p(p, t_in)
    ok(abs((cp_in - cp_out) - lat) < 0.1 * lat + 50.0,
       f"5: 창 안 c_p 증가 {cp_in - cp_out:.0f} ≠ ΔH/(T_liq−T_sol) = {lat:.0f} J/kg/K")
    g_out = m.grad_ad(p, sol - 50.0)
    g_in = m.grad_ad(p, t_in)
    ok(g_in < g_out, "5: 창 안에서 단열선이 평평해지지 않는다 (∇_ad 미감쇠)")
    # 단일점 구간(>140 GPa)의 명목 폭 — 선언값 그대로 창이 있다
    w = silicate_liquidus(300e9) - silicate_solidus(300e9)
    ok(abs(w - SILICATE_MELT_POINT_WIDTH) < 1e-9,
       f"5: 단일점 명목 폭 {w:.0f} ≠ 선언 {SILICATE_MELT_POINT_WIDTH:.0f} K")

    # ── 6. 시딩 — differentiated 가 조성을 고른다 (우리 선언, 라벨 확인) ──────
    ok(MATERIALS["silicate_chondritic"].phases[0].melt_variant == "chondritic"
       and MATERIALS["silicate"].phases[0].melt_variant == "peridotitic",
       "6: 조성 가지 기본값이 틀렸다")
    import interior
    stack = interior._stack(0.3, 0.0, "fe_prem", differentiated=False)
    names = [mm.name for mm, w_ in stack[0][1].parts]
    ok("silicate_chondritic" in names,
       "6: 미분화 천체의 암석이 콘드라이트 가지를 안 쓴다 — 시딩이 끊겼다")

    # ── 7. 지구 가드 — 기준 포텐셜 온도의 지구는 창 밖(고체)이다 ─────────────
    # 새 창이 앵커를 침범하면 여기가 게이트보다 먼저 운다. 1600 K 지구의 최소 여유는
    # 표면(0 GPa)에서 61 K 다 (T_sol(0) = 1661.2).
    r = interior.solve(1.0, core_mass_fraction=0.325, potential_temperature=1600.0)
    ok(r.values["silicate_melt_state"] == "solid",
       f"7: 기준 지구의 암석 판정이 {r.values['silicate_melt_state']} — solid 여야 한다")
    r2 = interior.solve(1.0, core_mass_fraction=0.325)
    ok(r2.values["silicate_melt_state"] == "undecided",
       "7: 온도 미선언인데 판정이 나왔다 — 0 인 척하지 말아야 한다")

    if fails:
        print(f"test_silicate_melt: FAIL {len(fails)}")
        for f in fails:
            print("  -", f)
        return 1
    print("test_silicate_melt: OK (전사 검산·이음매 계단·거절·φ 단일원·식17·시딩·지구 가드)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
