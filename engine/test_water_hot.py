# 뜨거운 물 EOS 이식 검사 — 논문이 자기 적합에 대해 적어둔 값을 다시 내는가
"""Anchors for `water_hot.py`.

    python3 engine/test_water_hot.py

이 파일은 **이식이 맞는가** 를 묻는다. 상수 스무 개쯤을 저자들의 참조 구현에서 옮겼고,
포트란 컴파일러가 없어 원본을 오라클로 돌릴 수 없으므로, 대신 서로 다른 것을 짚는 검사
셋을 건다.

1. **논문이 자기 적합에 대해 적어둔 임계점.** Mazevet+ 2019 §3.2 가 "giving the critical
   point at 683 K and 0.331 g/cm³ (to be compared with the experimental values of 647 K and
   0.322 g/cm³)" 라고 적는다. 우리 출력이 아니라 그들의 수이고, 분자항·혼합함수·이상항을
   한꺼번에 짚는다.
2. **저밀도 극한.** 밀도를 낮추면 압력이 분자 이상기체로 가야 한다. 물리가 정하는 것이라
   적합이 어긋나면 드러난다.
3. **두 출처의 일치.** 유효전하 Z* 는 논문 eq. (9) 에도 인쇄돼 있고 참조 구현에도 있다.
   두 경로를 따로 적어 맞춰 보면 그 여섯 상수가 검산된다.
"""
from __future__ import annotations

import math
import sys

import water_hot as w

# Mazevet+ 2019 §3.2 — 그들의 적합이 내는 임계점. 실측(647 K, 0.322)이 아니라 적합의 값이다.
PAPER_CRITICAL = (683.0, 0.331e3)
CRITICAL_T_TOL = 5.0        # K
CRITICAL_RHO_TOL = 0.02     # 상대


def _dp_drho(rho: float, t: float, h: float = 1e-3) -> float:
    return (w.pressure(rho * (1 + h), t) - w.pressure(rho * (1 - h), t)) / (2 * h * rho)


def _min_slope(t: float) -> tuple[float, float]:
    best = (1e99, 0.0)
    for i in range(400):
        rho = (0.15 + (0.6 - 0.15) * i / 399.0) * 1e3
        v = _dp_drho(rho, t)
        if v < best[0]:
            best = (v, rho)
    return best


def main() -> int:
    fails: list[str] = []

    print("임계점 — 논문이 자기 적합에 대해 적어둔 값을 다시 내는가")
    lo, hi = 600.0, 760.0
    for _ in range(45):
        mid = 0.5 * (lo + hi)
        if _min_slope(mid)[0] < 0.0:
            lo = mid
        else:
            hi = mid
    t_c = 0.5 * (lo + hi)
    rho_c = _min_slope(t_c)[1]
    want_t, want_rho = PAPER_CRITICAL
    ok_t = abs(t_c - want_t) <= CRITICAL_T_TOL
    ok_r = abs(rho_c / want_rho - 1.0) <= CRITICAL_RHO_TOL
    if not (ok_t and ok_r):
        fails.append(f"임계점이 {t_c:.1f} K · {rho_c / 1e3:.4f} g/cc, 논문은 "
                     f"{want_t:.0f} K · {want_rho / 1e3:.3f} g/cc")
    print(f"  [{'PASS' if ok_t and ok_r else 'FAIL'}] 이식 {t_c:.1f} K · "
          f"{rho_c / 1e3:.4f} g/cc · 논문 {want_t:.0f} K · {want_rho / 1e3:.3f} g/cc "
          f"({t_c - want_t:+.1f} K, {(rho_c / want_rho - 1) * 100:+.2f} %)")
    print(f"         실측은 647 K · 0.322 g/cc 다. 여기서 재는 것은 물리가 아니라 "
          f"**이식** 이므로, 대는 상대가 실측이 아니라 그들의 적합이어야 한다.")

    print("\n저밀도 극한 — 압력이 분자 이상기체로 가는가")
    k_b, m_h2o = 1.380649e-23, 2.99e-26
    worst = 0.0
    for rho, t in ((1.0, 30000.0), (0.1, 30000.0), (0.01, 40000.0)):
        got = w.pressure(rho, t)
        want = (rho / m_h2o) * k_b * t
        worst = max(worst, abs(got / want - 1.0))
        print(f"         ρ {rho:6.2f} kg/m³, T {t:6.0f} K → {got / want:.4f} × 이상기체")
    ok = worst < 0.05
    if not ok:
        fails.append(f"저밀도 극한이 이상기체에서 {worst * 100:.1f} % 벗어난다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 밀도를 낮출수록 1 로 간다 (최악 "
          f"{worst * 100:.1f} % — 가장 성긴 점에서)")

    print("\n두 출처 — 논문 eq. (9) 와 참조 구현이 같은 Z* 를 주는가")
    # 논문 eq. (9): Z* = (10/3)·[1 + 2.35 r_s/(1 + 0.09/(r_s√Γ)) + 5.9 r_s^3.78/(1+17/Γ)^1.5]^-1
    def z_from_paper(rs: float, game: float) -> float:
        return (10.0 / 3.0) / (1.0 + 2.35 * rs / (1.0 + 0.09 / (rs * math.sqrt(game)))
                               + 5.9 * rs ** 3.78 / (1.0 + 17.0 / game) ** 1.5)
    worst, where = 0.0, None
    for rs in (0.2, 0.5, 1.0, 2.0):
        for game in (0.5, 2.0, 10.0, 60.0):
            a = z_from_paper(rs, game)
            b = w._z_effective(rs, game)[0]
            d = abs(a - b) / a
            if d > worst:
                worst, where = d, (rs, game)
    ok = worst < 1e-12
    if not ok:
        fails.append(f"논문 eq. (9) 와 참조 구현의 Z* 가 {worst:.2e} 다르다 {where}")
    print(f"  [{'PASS' if ok else 'FAIL'}] 최악 {worst:.2e} (r_s, Γ = {where}) — 여섯 "
          f"상수가 두 출처에서 같다")

    print("\n혼합함수 — 논문 eq. (5) 와 참조 구현이 같은 무게를 주는가")
    # 논문 eq. (5): w(ρ,T) = 1/(1 + (ρ/2.5 g/cc + T/3509 K)^4)
    worst, where = 0.0, None
    for rho_cgs in (0.3, 1.0, 3.0, 8.0):
        for t in (1000.0, 5000.0, 20000.0):
            paper = 1.0 / (1.0 + (rho_cgs / 2.5 + t / 3509.0) ** 4)
            x = w.Q4 * math.log(w.Q1 * rho_cgs + w.Q2 * (t / 1.0e6 / w.UN_T6))
            impl = 1.0 / (1.0 + math.exp(x))
            d = abs(paper - impl) / paper
            if d > worst:
                worst, where = d, (rho_cgs, t)
    # 남는 차이는 논문이 인쇄한 반올림 그 자체다. 그러니 무게를 대충 재는 대신
    # **함축된 상수** 를 직접 꺼내 인쇄된 자릿수와 맞춘다. 그쪽이 날카롭다.
    implied = 1.0e6 * w.UN_T6 / w.Q2          # 참조의 90·T_au 가 함축하는 온도 눈금 [K]
    ok_const = abs(implied - 3509.0) < 0.5
    ok = worst < 1e-3 and ok_const
    if not ok:
        fails.append(f"논문 eq. (5) 와 참조 구현이 안 맞는다 — 무게 {worst:.2e} {where}, "
                     f"함축 상수 {implied:.1f} K 대 인쇄된 3509 K")
    print(f"  [{'PASS' if ok else 'FAIL'}] 함축된 온도 눈금 {implied:.1f} K · 논문이 "
          f"인쇄한 3509 K — 같은 수를 반올림한 것이다")
    print(f"         무게 자체의 최악 차이 {worst:.2e} (ρ, T = {where}) 는 그 반올림이 "
          f"네제곱을 타고 커진 몫이고, 다른 상수의 불일치가 아니다. 같은 자리에서 ρ 쪽 "
          f"눈금 2.5 g/cc 는 참조의 Q1 = 0.4 와 정확히 역수다.")

    print("\n단조 — P(ρ) 가 쓰는 구간에서 증가하는가 (밀도 뒤집기의 뿌리가 하나인 근거)")
    bad = None
    for t in (2000.0, 5000.0, 10000.0, 30000.0):
        prev = None
        for i in range(200):
            rho = w.RHO_MIN * (w.RHO_MAX / w.RHO_MIN) ** (i / 199.0)
            v = w.pressure(rho, t)
            if prev is not None and v <= prev:
                bad = (t, rho)
                break
            prev = v
    if bad:
        fails.append(f"P(ρ) 가 T={bad[0]} K, ρ={bad[1]:.3g} 에서 단조가 아니다")
    print(f"  [{'PASS' if not bad else 'FAIL'}] {w.RHO_MIN / 1e3:.1f}–"
          f"{w.RHO_MAX / 1e3:.0f} g/cc · 2000–30000 K 에서 단조증가")

    print("\n뒤집기 — 밀도에서 압력으로 돌아오는가")
    worst, where = 0.0, None
    for t in (2000.0, 5000.0, 12000.0):
        for p in (10e9, 100e9, 500e9, 2000e9):
            rho = w.density(p, t)
            d = abs(w.pressure(rho, t) / p - 1.0)
            if d > worst:
                worst, where = d, (t, p)
    ok = worst < 1e-8
    if not ok:
        fails.append(f"密度 뒤집기 왕복이 {worst:.2e} 어긋난다 {where}")
    print(f"  [{'PASS' if ok else 'FAIL'}] 왕복 최악 {worst:.2e} (T, P = {where})")

    print("\n그뤼나이젠 — 뜨거운 물의 값이 발표된 자릿수인가")
    for rho, t in ((2.0e3, 3000.0), (3.0e3, 5000.0), (4.0e3, 5700.0)):
        g = w.gruneisen(rho, t)
        ok = 0.2 < g < 2.0
        if not ok:
            fails.append(f"γ 가 {g:.3f} — 뜨거운 물의 자릿수가 아니다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {rho / 1e3:.1f} g/cc {t:5.0f} K → "
              f"γ = {g:.4f}")

    if fails:
        print(f"\n실패 {len(fails)}건")
        for f in fails:
            print(f"  · {f}")
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
