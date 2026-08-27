# 페르미 적분 검사 — 굳혀 둔 표가 정의와 맞는가, 그리고 보간 오차가 적어둔 만큼인가
"""Anchors for `fermi.py`.

    python3 engine/test_fermi.py

**오라클이 둘이고 서로 독립이다.** 하나는 정의의 정적분(scipy.integrate.quad), 다른
하나는 폴리로그 항등식 F_j(η) = −Γ(j+1)·Li_{j+1}(−e^η) 를 mpmath 로 40자리에서 평가한
값이다. 방법이 다르므로 같은 실수를 같은 방향으로 하지 않는다. 둘 다 개발 venv 에만
있고, 없으면 그 절을 SKIP 한다 — scripts/check.sh 는 시스템 파이썬으로 돌아야 한다.

의존성 없이도 도는 절이 둘 있다. 급수 두 개의 이어붙임과 역함수의 왕복이고, 그 둘은
`fermi.py` 안에서 닫히므로 오라클이 필요 없다.
"""
from __future__ import annotations

import math
import sys

import fermi
from fermi import ETA_HI, ETA_LO, ETA_STEP, INTERP_WORST

# 굳힌 값이 정의와 어긋나도 되는 폭. 표를 만든 것과 같은 방법으로 다시 만드는 것이므로
# 사실상 0 이어야 한다 — 이건 "표가 표류했는가" 검사다.
TABLE_TOL = 1e-12
# 두 오라클이 서로 어긋나도 되는 폭. 오너가 잰 값이 최악 4e-10 이었다.
ORACLE_TOL = 1e-8
# 보간 오차가 적어둔 값에서 벗어나도 되는 폭 (상대).
INTERP_TOL = 0.25


def _oracles():
    """(quad, polylog) 두 오라클. 없으면 (None, None)."""
    try:
        from scipy.integrate import quad
    except ImportError:
        return None, None

    def by_quad(j: float, eta: float) -> float:
        hi = max(80.0, eta + 80.0)
        v, _err = quad(lambda x: x ** j / (math.exp(x - eta) + 1.0), 0.0, hi,
                       limit=800, epsabs=1e-14, epsrel=1e-13)
        return v

    try:
        from mpmath import exp as mexp, gamma as mgamma, mp, mpf, polylog, re
        mp.dps = 40

        def by_polylog(j: float, eta: float) -> float:
            return float(re(-mgamma(mpf(j) + 1) * polylog(mpf(j) + 1, -mexp(mpf(eta)))))
    except ImportError:
        by_polylog = None
    return by_quad, by_polylog


def main() -> int:
    fails: list[str] = []
    by_quad, by_polylog = _oracles()

    print("두 오라클 — 정적분과 폴리로그 항등식이 서로 맞는가")
    if by_quad is None or by_polylog is None:
        print("  [SKIP] scipy 또는 mpmath 가 없다 — engine/.venv 에서만 도는 절이다")
    else:
        worst, where = 0.0, None
        for j in (0.5, 1.5):
            for eta in (-5, -2, -1, 0, 1, 2, 5, 10, 20, 50, 100, 300, 1000):
                a, b = by_quad(j, float(eta)), by_polylog(j, float(eta))
                d = abs(a - b) / abs(b)
                if d > worst:
                    worst, where = d, (j, eta)
        ok = worst <= ORACLE_TOL
        if not ok:
            fails.append(f"두 오라클이 {worst:.2e} 어긋난다 (j, η = {where})")
        print(f"  [{'PASS' if ok else 'FAIL'}] 최악 {worst:.2e} (j, η = {where}) — "
              f"허용 {ORACLE_TOL:.0e}. 방법이 달라도 같은 함수를 낸다")

    print("\n굳혀 둔 표 — 정의로 다시 만들면 같은 값이 나오는가")
    if by_quad is None:
        print("  [SKIP] scipy 가 없다")
    else:
        n = len(fermi.FD_P12)
        for name, table, j in (("F_-1/2", fermi.FD_M12, -0.5),
                               ("F_+1/2", fermi.FD_P12, 0.5),
                               ("F_+3/2", fermi.FD_P32, 1.5)):
            worst, where = 0.0, None
            for i in range(n):
                eta = ETA_LO + i * ETA_STEP
                want = by_quad(j, eta)
                d = abs(table[i] - want) / want
                if d > worst:
                    worst, where = d, eta
            ok = worst <= TABLE_TOL
            if not ok:
                fails.append(f"{name} 표가 정의에서 {worst:.2e} 표류했다 (η={where})")
            print(f"  [{'PASS' if ok else 'FAIL'}] {name:7} {n}점 최악 {worst:.2e} "
                  f"(η={where})")

    print("\n보간 오차 — 이 작업이 새로 들여온 오차원이다. 재서 적었는가")
    # 얼음 III·V·VI 은 상수 셋이라 굳힌 값이 맞으면 끝이었다. 여기는 함수의 표라서
    # 격자 사이가 새 오차이고, 그 수를 주장이 아니라 측정으로 둔다.
    if by_polylog is None:
        print("  [SKIP] mpmath 가 없다")
    else:
        worst, where = 0.0, None
        for k in range(401):
            eta = ETA_LO + (ETA_HI - ETA_LO) * k / 400.0
            for fn, j in ((fermi.f_half, 0.5), (fermi.f_three_half, 1.5)):
                want = by_polylog(j, eta)
                d = abs(fn(eta) - want) / want
                if d > worst:
                    worst, where = d, (j, eta)
        ok = abs(worst / INTERP_WORST - 1.0) <= INTERP_TOL
        if not ok:
            fails.append(f"보간 오차가 {worst:.3e}, 파일이 적어둔 값은 {INTERP_WORST:.3e}")
        print(f"  [{'PASS' if ok else 'FAIL'}] 격자 사이 최악 {worst:.3e} "
              f"(j, η = {where[0]}, {where[1]:.3f}) · 파일이 적어둔 {INTERP_WORST:.1e}")
        print(f"         같은 자리에서 Sommerfeld 가 1.3e-7 이므로 이 구성 전체의 정직한 "
              f"폭이 ~5e-7 이다. 이 파일을 먹는 상태방정식 자체가 몇 % 이므로 자릿수가 "
              f"넷 남는다.")

    print("\n이어붙임 — 급수와 표와 축퇴 전개가 경계에서 만나는가")
    for eta, label in ((ETA_LO, "급수 → 표"), (ETA_HI, "표 → Sommerfeld")):
        for fn, name in ((fermi.f_half, "F_1/2"), (fermi.f_three_half, "F_3/2")):
            lo_side, hi_side = fn(eta - 1e-9), fn(eta + 1e-9)
            d = abs(hi_side - lo_side) / lo_side
            ok = d < 5e-7
            if not ok:
                fails.append(f"{label} 이음매에서 {name} 가 {d:.2e} 튄다")
            print(f"  [{'PASS' if ok else 'FAIL'}] {label:16} η={eta:6.2f} {name} "
                  f"{d:.2e} 튄다")

    print("\n역함수 — 왕복이 제자리로 오는가 (표가 따로 없다)")
    worst, where = 0.0, None
    for k in range(121):
        eta = -20.0 + 40.0 * k / 120.0
        back = fermi.inverse_f_half(fermi.f_half(eta))
        d = abs(back - eta) / max(abs(eta), 1.0)
        if d > worst:
            worst, where = d, eta
    ok = worst < 1e-10
    if not ok:
        fails.append(f"역함수 왕복이 {worst:.2e} 어긋난다 (η={where})")
    print(f"  [{'PASS' if ok else 'FAIL'}] η ∈ [−20, 20] 왕복 최악 {worst:.2e} "
          f"(η={where:.2f}) — Padé 없이 Newton 만으로 닫힌다")

    print("\n단조 — F_1/2 가 증가하는가 (역함수의 뿌리가 하나인 근거)")
    prev = None
    mono = True
    for k in range(801):
        eta = -30.0 + 60.0 * k / 800.0
        v = fermi.f_half(eta)
        if prev is not None and v <= prev:
            mono = False
            break
        prev = v
    if not mono:
        fails.append("F_1/2 가 단조증가가 아니다")
    print(f"  [{'PASS' if mono else 'FAIL'}] η ∈ [−30, 30] 에서 단조증가")

    if fails:
        print(f"\n실패 {len(fails)}건")
        for f in fails:
            print(f"  · {f}")
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
