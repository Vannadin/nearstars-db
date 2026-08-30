# 암모니아 표 검사 — 굳힌 값이 인쇄된 표와 같은가, 보간이 제 오차 안인가, 물과 섞으면 얼마가 나오는가
"""Checks for `ammonia_table.py` and the `nh3` material.

    python3 engine/test_ammonia.py

1. **Transcription.** The baked constants are compared with rows read from the printed
   Table I of Bethkenhagen, French & Redmer 2013 by eye (the rendered page, not the text
   layer the generator parsed) — eight rows across both pages, the five asterisked rows,
   the ragged edge, and the counts.
2. **Interpolation.** Round trip density(pressure(ρ, T), T) = ρ on the grid; the
   leave-one-out error re-measured and compared with the constant the generator wrote.
3. **Refusals** name the table, on both temperature and the ragged pressure edge.
4. **The convention flag** is set, and the material's c_P and ∇_ad are finite and positive
   where an ice-giant mantle sits.
5. **The water–ammonia check (C4).** Water (Mazevet+ 2019) and ammonia (this table) read at
   the same (P, T) along points bracketing the ice-giant adiabat, mixed by additive volume
   at the solar-ratio water:ammonia mass fractions renormalised to two components. The
   numbers are printed and the deviation from pure water is reported — this is the first
   measured piece of the composition tier, for the ammonia share only.
"""
from __future__ import annotations

import math
import sys

import ammonia_table as a
import water_hot as w
from eos import MATERIALS, NH3, PhaseGap, Mixture, SOLAR_ICE_MASS_FRACTIONS

# 인쇄된 표에서 눈으로 읽은 행 (rho g/cm³, T K, p GPa, u kJ/g, 별표). 텍스트층 파싱과 별개의 경로다.
PRINTED = (
    (0.5, 500, 0.309, -105.69, False),
    (2.0, 700, 64.57, -95.843, False),
    (1.3, 2000, 20.25, -96.942, False),
    (1.0, 4000, 14.36, -85.86, True),
    (0.75, 5000, 9.00, -80.90, True),
    (2.5, 6000, 177.9, -50.496, False),
    (1.8, 8000, 82.81, -51.015, False),
    (3.0, 10000, 333.2, -18.953, False),
)
FLAGGED = ((0.5, 4000), (0.75, 4000), (1.0, 4000), (0.5, 5000), (0.75, 5000))

# 얼음거대행성 맨틀의 (P GPa, T K). 앞 넷은 엔진이 푼 천왕성 프로파일에서 읽은 점
# (tools/methane_thresholds.py: ~50 GPa 2829 K … ~250 GPa 3950 K 근방), 뒤 넷은 중심 온도
# 5500–6300 K 를 5000·7000 K 등온선 사이에서 감싸는 점. 압력은 표의 천장(그 온도에서
# ≈ 270–290 GPa) 아래로 잡는다.
MANTLE_POINTS = ((50.0, 2830.0), (100.0, 3190.0), (200.0, 3730.0), (250.0, 3950.0),
                 (50.0, 5000.0), (100.0, 5500.0), (200.0, 6000.0), (250.0, 6300.0))


def _row(rho, t):
    i = a.T_K.index(t)
    for r, p, u, f in a.ISOTHERMS[i]:
        if r == rho:
            return p, u, f
    return None


def main() -> int:
    fails: list[str] = []

    def check(ok: bool, label: str) -> None:
        if not ok:
            fails.append(label)
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")

    print("전사 — 굳힌 표가 인쇄된 Table I 과 같은가")
    for rho, t, p, u, f in PRINTED:
        got = _row(rho, t)
        check(got is not None and got[0] == p and got[1] == u and got[2] == f,
              f"rho {rho} T {t}: p {p} u {u}{' *' if f else ''}")
    n = sum(len(iso) for iso in a.ISOTHERMS)
    check(n == 93 == a.N_POINTS, f"{n} 점 (인쇄된 표 93 행)")
    flagged = {(r, t) for t, iso in zip(a.T_K, a.ISOTHERMS) for r, _p, _u, f in iso if f}
    check(flagged == set(FLAGGED) and len(flagged) == a.N_FLAGGED,
          f"5 % 표시 {len(flagged)} 점, 뜨겁고 성긴 모서리에 모여 있다")
    lens = [len(iso) for iso in a.ISOTHERMS]
    check(lens == [5, 7] + [9] * 9, f"들쭉날쭉한 격자 {lens} — 500 K 는 1.5, 700 K 는 2.0 g/cm³ 까지")
    check(a.T_K == (500, 700, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 10000),
          "등온선 11 개")
    check(abs(a.P_MAX_PA - 333.2e9) < 1.0, "천장 333.2 GPa = (3.0 g/cm³, 10 000 K)")
    mono = all(all(c[1] > b[1] for b, c in zip(iso, iso[1:])) for iso in a.ISOTHERMS)
    check(mono, "모든 등온선에서 p 가 ρ 에 단조")

    print("\n보간 — 격자 위에서 되돌아오는가, 오차가 적힌 만큼인가")
    worst = 0.0
    for t, iso in zip(a.T_K, a.ISOTHERMS):
        for r, p, _u, _f in iso:
            worst = max(worst, abs(a.density(p * 1e9, float(t)) / (r * 1e3) - 1.0))
    check(worst < 1e-9, f"density(pressure(ρ,T),T) 왕복 최악 {worst:.1e}")
    # leave-one-out 을 다시 잰다 (온도 방향, 전체 격자). 생성기가 적은 수와 같아야 한다.
    loo = 0.0
    for i in range(1, len(a.T_K) - 1):
        t0, t1, t2 = a.T_K[i - 1], a.T_K[i], a.T_K[i + 1]
        lo = {r: p for r, p, _u, _f in a.ISOTHERMS[i - 1]}
        hi = {r: p for r, p, _u, _f in a.ISOTHERMS[i + 1]}
        for r, p, _u, _f in a.ISOTHERMS[i]:
            if r in lo and r in hi:
                x = (t1 - t0) / (t2 - t0)
                loo = max(loo, abs((lo[r] + x * (hi[r] - lo[r])) / p - 1.0))
    check(loo <= a.INTERP_P_LOO_WORST + 1e-4,
          f"온도 방향 leave-one-out 최악 {loo * 100:.2f} % ≤ 적힌 {a.INTERP_P_LOO_WORST * 100:.2f} % "
          f"(맨틀 영역 {a.INTERP_P_LOO_MANTLE * 100:.2f} %, 격자 간격 두 배에서의 수)")

    print("\n거절 — 표 이름을 대는가")
    for p_gpa, t, why in ((10.0, 400.0, "500 K 아래"), (10.0, 12000.0, "10 000 K 위"),
                          (30.0, 600.0, "600 K 에서 1.5 g/cm³ 너머 (22.8 GPa 천장)"),
                          (300.0, 6300.0, "6300 K 에서 3.0 g/cm³ 너머 (293 GPa 천장)")):
        try:
            NH3.density(p_gpa * 1e9, t)
            check(False, f"{why}: 거절해야 한다")
        except PhaseGap as e:
            check("Bethkenhagen" in e.reason and "2013" in e.reason, f"{why}: '{e.reason[:60]}…'")
    check(not a.in_domain(30e9, 600.0) and a.in_domain(30e9, 4000.0), "in_domain 이 같은 가장자리를 안다")

    print("\n규약과 열 — 내부에너지에 진동 보정이 들어 있다고 말하는가")
    check(a.U_INCLUDES_VIBRATIONAL_CORRECTION is True,
          "U_INCLUDES_VIBRATIONAL_CORRECTION = True (2013 Appendix B; 2017 §II.4 가 뺀 그 보정)")
    check(MATERIALS["nh3"] is NH3, "MATERIALS['nh3'] 에 등록")
    for p_gpa, t in MANTLE_POINTS:
        p = p_gpa * 1e9
        cp, g = NH3.c_p(p, t), NH3.grad_ad(p, t)
        check(math.isfinite(cp) and cp > 0.0 and 0.0 < g < 1.0,
              f"{p_gpa:.0f} GPa · {t:.0f} K: c_P {cp:.0f} J/kg/K, ∇_ad {g:.3f}, 불확도 {NH3.uncertainty(p, t) * 100:.0f} %")

    print("\n물–암모니아 검사 (C4) — 물 하나로 두 성분을 대신하면 밀도가 얼마나 어긋나는가")
    w_nh3 = SOLAR_ICE_MASS_FRACTIONS["nh3"] / (SOLAR_ICE_MASS_FRACTIONS["nh3"] + SOLAR_ICE_MASS_FRACTIONS["h2o"])
    mix = Mixture("h2o_nh3_check", "물–암모니아 검사 혼합",
                  ((MATERIALS["h2o_hot"], 1.0 - w_nh3), (NH3, w_nh3)))
    mu_ratio = 17.031 / 18.015     # 같은 수밀도라면 이 비 — 조성 층위의 *도출* 가정
    print(f"  암모니아 질량분율 (물+암모니아 안에서) {w_nh3:.4f} — 태양비 0.08 : 0.61 (Bethkenhagen+ 2017 §V)")
    print(f"  {'P GPa':>6} {'T K':>6} {'ρ_H2O':>7} {'ρ_NH3':>7} {'NH3/H2O':>8} {'μ 비':>6} {'혼합/물':>8} {'불확도':>6}")
    ratios, devs = [], []
    for p_gpa, t in MANTLE_POINTS:
        p = p_gpa * 1e9
        rw, rn = w.density(p, t), NH3.density(p, t)
        rm = mix.density(p, t)
        ratios.append(rn / rw)
        devs.append(rm / rw - 1.0)
        print(f"  {p_gpa:6.0f} {t:6.0f} {rw:7.0f} {rn:7.0f} {rn / rw:8.4f} {mu_ratio:6.4f} "
              f"{rm / rw:8.4f} {NH3.uncertainty(p, t) * 100:5.0f} %")
    check(all(r < 1.0 for r in ratios),
          f"같은 (P, T) 에서 암모니아가 물보다 가볍다: ρ_NH3/ρ_H2O = {min(ratios):.3f}–{max(ratios):.3f} "
          f"(같은 수밀도 가정의 μ 비 {mu_ratio:.3f} 보다 훨씬 작다)")
    check(all(d < 0.0 for d in devs),
          f"물 하나가 물+암모니아 쌍의 밀도를 {-max(devs) * 100:.1f}–{-min(devs) * 100:.1f} % 과대평가한다 "
          "(조성 층위, 암모니아 몫만 — 방향 +, 잔차를 벌린다)")
    # 이 수가 잡음 위에 있는가. 암모니아 밀도의 오차(표 2 % + 보간, 맨틀 영역 LOO/4 ≈ 1.6 %)는
    # 혼합 밀도에 질량분율 × (ρ_mix/ρ_NH3) 만큼만 옮겨 간다 — 1/ρ_mix 가 1/ρ_i 의 가중합이라서.
    # 물 쪽(Mazevet+ 2019 적합)의 오차는 여기서 정량하지 않는다 — 표가 아니라 적합이고, 이 검사는
    # 그 적합을 기준으로 삼는다.
    err_nh3 = a.P_UNCERTAINTY + a.INTERP_P_LOO_MANTLE / 4.0
    err_mix = max(w_nh3 * (mix.density(p_gpa * 1e9, t) / NH3.density(p_gpa * 1e9, t)) * err_nh3
                  for p_gpa, t in MANTLE_POINTS)
    check(min(-d for d in devs) > err_mix,
          f"편차 최소 {min(-d for d in devs) * 100:.1f} % > 암모니아 오차 {err_nh3 * 100:.1f} % 가 혼합에 "
          f"옮겨 간 {err_mix * 100:.2f} % — 수가 잡음 위에 있다 (물 쪽 오차는 미정량)")

    print("\n열 층위, 암모니아 몫 — 같은 (P, T) 에서 c_P 와 ∇_ad 는 어느 쪽인가 (보고만, 판정 없음)")
    print(f"  {'P GPa':>6} {'T K':>6} {'c_P H2O':>8} {'c_P NH3':>8} {'∇ H2O':>7} {'∇ NH3':>7} {'∇ 혼합':>7}")
    hot = MATERIALS["h2o_hot"]
    for p_gpa, t in MANTLE_POINTS:
        p = p_gpa * 1e9
        print(f"  {p_gpa:6.0f} {t:6.0f} {hot.c_p(p, t):8.0f} {NH3.c_p(p, t):8.0f} "
              f"{hot.grad_ad(p, t):7.3f} {NH3.grad_ad(p, t):7.3f} {mix.grad_ad(p, t):7.3f}")
    print("  (암모니아의 c_P 는 진동 보정이 든 u 의 온도 도함수다 — 규약 노출은 이 두 열뿐이다)")

    print()
    if fails:
        print(f"FAIL: {len(fails)}")
        for f in fails:
            print(f"  - {f}")
        return 1
    print("모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
