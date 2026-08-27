# 거대행성 앵커 — n=1 폴리트로프가 해석해와 발표값을 재현하는가, 그리고 문서 표를 다시 만든다
"""Anchor the giant-planet branch on the analytic polytrope and on published planets.

    python3 engine/test_giant.py
    python3 engine/test_giant.py --table     문서 §Validation 의 거대행성 표를 다시 낸다

폴리트로프는 **새 노드가 아니라 상태방정식의 네 번째 함수형** 이다. 그래서 이 파일이
검사하는 것은 새 레시피가 아니라, 같은 적분기가 층 하나를 더 받고도 옳은 답을 내는가다.

세 가지를 대조한다. 전부 남이 발표하거나 손으로 풀 수 있는 값이다.

1. **해석해.** n = 1 의 Lane-Emden 해는 닫힌 형태다. 반지름이 질량과 무관하게
   R = √(πK/2G) 이고, 관성모멘트가 C/MR² = (2/3)(1 − 6/π²) 다. 수치 적분이 그 둘을
   재현하지 못하면 적분기가 틀린 것이다.
2. **발표된 숫자.** Helled+ 2022 §2 가 같은 K 에서 R = 70,300 km 가 나온다고 적는다.
   그 문장이 **단위 함정을 걸러내는 자리** 이기도 하다 — 논문이 K 를 cgs 값으로 적고
   SI 단위를 달아 놓았고, SI 로 읽으면 반지름이 1.5 AU 가 된다.
3. **측정된 행성.** 목성과 토성의 IAU 평균반지름, 그리고 목성의 NMoI.

**반지름 정의를 섞으면 안 된다.** 이 모형은 비회전 구형이므로 대조 상대는 적도
1-bar 반지름(목성 71,492 km)이 아니라 **부피 평균반지름**(69,911 km)이다. 회전이
목성의 적도를 2.3 % 부풀리는데, 그건 이 레시피가 계산하지 않는 효과다.
"""
from __future__ import annotations

import math
import sys

from eos import (DEUTERIUM_LIMIT_MJ, JUPITER_MASS_EARTH, POLYTROPE_K_HHE,
                 POLYTROPE_N_HHE, polytrope_radius_n1)
from interior import EARTH_MASS_KG, EARTH_RADIUS_M, shoot, solve

# ── 발표값 ──────────────────────────────────────────────────────────────
#
# 반지름은 IAU/IAG 실무그룹 보고의 값이다 (Archinal+ 2011, CeMDA 109, 101; 같은 값이
# Seidelmann+ 2007 에도 있다). **평균반지름과 적도 1-bar 반지름을 둘 다 적어 둔다** —
# 어느 쪽과 대조하는지가 결과를 2 % 움직이므로 고르는 게 아니라 밝히는 문제다.
PLANETS = [
    # (이름, 질량 M⊕, 평균반지름 km, 적도 1-bar km, 중원소 총량 M⊕ (Guillot 1999))
    ("Jupiter", JUPITER_MASS_EARTH, 69911, 71492, (11, 42)),
    ("Saturn", 95.159, 58232, 60268, (19, 31)),
]

# Helled+ 2022 §2 (arXiv:2202.10046) 가 자기 K 에서 낸다고 적는 반지름.
HELLED_POLYTROPE_R_KM = 70300.0

# 목성 NMoI. **고르지 않고 조사했다.** 돌아다니는 값이 셋인데 근거가 같지 않다.
#
#   0.254   NASA 팩트시트(D. R. Williams) 계열. ADS 색인 전문 하나가 그 값을 두고
#           "whereas it actually translates into λ = 0.243 when it is normalised using
#           R_eq" 라고 적는다 — 정규화 반지름이 모호하다는 뜻이다.
#   0.2756  Ni 2018 (2018A&A...613A..32N) 에 나오고, 뒤 논문들이 "Jupiter-like value
#           determined from the Juno probe" 로 재인용한다. 그 논문 전문을 구하지 못해
#           그 값이 그 논문에서 **입력으로 훑은 값인지 추론된 값인지 확인하지 못했다.**
#           확인한 것은 하나뿐이다 — 전문을 읽은 어느 내부구조 모형 연구도 이 값을
#           내지 않고, 아래 두 범위보다 4.5 % 높다.
#   0.2634-0.2644  Neuenschwander+ 2021 (arXiv:2101.12508) 이 Juno 중력장에 맞춘
#           조각별 폴리트로프 모형에서 0.2634 < MoI < 0.2639 를 얻고, 같은 논문이
#           Wahl+ 2017 의 0.2640 < MoI < 0.2644 를 나란히 적는다. 둘의 합집합이
#           Helled+ 2011 (arXiv:1109.1627) 의 독립적인 0.2629-0.2645 안에 든다.
#
# **셋 중 마지막을 앵커로 쓴다.** Juno 이후이고, 측정된 중력장에 맞춘 모형에서 나오고,
# 전문을 읽은 두 연구가 서로 겹치며, 세 번째 독립 연구의 범위 안에 있다.
JUPITER_NMOI_BAND = (0.2634, 0.2644)      # Neuenschwander+ 2021 ∪ Wahl+ 2017
JUPITER_NMOI_WIDE = (0.2629, 0.2645)      # Helled+ 2011, 독립 확인용
JUPITER_NMOI_REJECTED = {"NASA 팩트시트": 0.254, "Ni 2018 재인용": 0.2756}

# 보드가 지금 싣고 있는 클래스 상수. 이 파일은 보드를 바꾸지 않고 **대조만** 한다.
AB_MASS_EARTH = 120.0
AB_RADIUS_RJ = 1.0
AB_CLASS_TABLE_NMOI = 0.23
R_JUP_EQ_KM = 71492.0

RADIUS_TOL = 0.03        # 3 %. 목성 평균반지름에 대한 허용치
NMOI_TOL = 0.02          # 2 %. 앵커 밴드 대비
SATURN_BAND = (0.10, 0.30)   # 토성 초과분이 떨어져야 하는 구간. **한계를 고정한다**


def analytic_nmoi_n1() -> float:
    """n = 1 Lane-Emden 해의 C/MR². θ = sin ξ/ξ, ξ₁ = π 를 손으로 적분한 값.

        ∫₀^π ξ sin ξ dξ = π,   ∫₀^π ξ³ sin ξ dξ = π³ − 6π
        C/MR² = (2/3)(π³ − 6π)/(π² · π) = (2/3)(1 − 6/π²)

    교과서 적분이라 인용이 필요 없다 — Lane-Emden 방정식 자체는 Chandrasekhar 1939 다."""
    return (2.0 / 3.0) * (1.0 - 6.0 / math.pi ** 2)


def _giant(mass_earth: float, core_earth: float = 0.0):
    """가스 외피만 있는(또는 규산염 핵을 얹은) 거대행성 하나를 푼다."""
    cmf = core_earth / mass_earth
    return solve(mass_earth, core_mass_fraction=0.0, ice_mass_fraction=0.0,
                 gas_mass_fraction=1.0 - cmf, body_class="giant")


def _km(res) -> float:
    return res.values["radius"] * EARTH_RADIUS_M / 1e3


def _integrator_km(mass_earth: float) -> float:
    """적분기를 **레시피의 영역 정책을 거치지 않고** 직접 돌려 반지름[km]을 낸다.

    해석해 대조는 "이 천체를 믿는가" 가 아니라 "적분기가 Lane-Emden 을 재현하는가"
    를 묻는다. 두 질문에 같은 문을 쓰면, 검증 범위를 좁히는 순간 적분기 검사가 같이
    막힌다 — 실제로 그렇게 됐다. 정책은 solve() 에 두고, 이 검사만 아래를 본다."""
    st, _ = shoot(mass_earth * EARTH_MASS_KG, 0.0, 0.0, "fe_prem", gmf=1.0)
    return st.radius_m / 1e3


def table() -> None:
    """문서 §Validation 의 거대행성 표를 다시 낸다. 손으로 친 표는 어긋난다."""
    print("| body | M (M⊕) | R derived | R mean (IAU) | ΔR vs mean | R eq 1 bar | "
          "C/MR² derived | P_c (GPa) |")
    print("|---|---|---|---|---|---|---|---|")
    for name, m, r_mean, r_eq, _z in PLANETS:
        res = _giant(m)
        if not res.applicable:
            print(f"| {name} | {m:.1f} | declined | {r_mean} | – | {r_eq} | – | – |")
            continue
        rk = _km(res)
        print(f"| {name} | {m:.1f} | {rk:.0f} km | {r_mean} km | "
              f"{(rk / r_mean - 1) * 100:+.1f} % | {r_eq} km | "
              f"{res.values['nmoi']:.4f} | {res.values['core_pressure']:.0f} |")
    res = _giant(AB_MASS_EARTH)
    rk = _km(res)
    print(f"| Alpha Centauri A b | {AB_MASS_EARTH:.1f} | {rk:.0f} km | – | – | "
          f"{AB_RADIUS_RJ * R_JUP_EQ_KM:.0f} km (declared) | "
          f"{res.values['nmoi']:.4f} | {res.values['core_pressure']:.0f} |")


def main() -> int:
    if "--table" in sys.argv:
        table()
        return 0

    fails: list[str] = []

    print("해석해 — 수치 적분이 손으로 푼 n=1 해를 재현하는가")
    r_analytic = polytrope_radius_n1(POLYTROPE_K_HHE) / 1e3
    nmoi_analytic = analytic_nmoi_n1()
    # n = 1 은 반지름이 질량과 무관하다. 그게 이 형태의 서명이므로 질량을 흩어 확인한다.
    got = [(m, _giant(m)) for m in (95.0, 317.8, 636.0, 1200.0)]
    swept = [_integrator_km(m) for m, _r in got]
    spread = max(swept) / min(swept) - 1.0
    ok = spread < 1e-4
    if not ok:
        fails.append(f"n=1 인데 반지름이 질량에 따라 {spread * 100:.3f} % 움직인다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 반지름이 질량과 무관하다 — 95~1200 M⊕ 에서 "
          f"편차 {spread * 100:.4f} % (해석해 {r_analytic:.0f} km)")

    d_r = abs(_km(got[1][1]) - r_analytic) / r_analytic
    ok = d_r < 1e-3
    if not ok:
        fails.append(f"적분 반지름이 해석해와 {d_r * 100:.3f} % 어긋난다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 적분 {_km(got[1][1]):.0f} km · 해석해 "
          f"√(πK/2G) = {r_analytic:.0f} km ({d_r * 100:.4f} %)")

    d_n = abs(got[1][1].values["nmoi"] - nmoi_analytic) / nmoi_analytic
    ok = d_n < 2e-3
    if not ok:
        fails.append(f"적분 C/MR² 가 해석해와 {d_n * 100:.3f} % 어긋난다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 적분 C/MR² {got[1][1].values['nmoi']:.5f} · "
          f"해석해 (2/3)(1 − 6/π²) = {nmoi_analytic:.5f} ({d_n * 100:.3f} %)")

    print("\n발표된 숫자 — 그리고 이 줄이 단위 함정을 걸러낸 자리다")
    d = abs(r_analytic - HELLED_POLYTROPE_R_KM) / HELLED_POLYTROPE_R_KM
    ok = d < 1e-3
    if not ok:
        fails.append(f"K 에서 나온 반지름이 발표값 {HELLED_POLYTROPE_R_KM} km 와 "
                     f"{d * 100:.2f} % 어긋난다")
    print(f"  [{'PASS' if ok else 'FAIL'}] K = {POLYTROPE_K_HHE:.1e} SI → "
          f"{r_analytic:.0f} km · Helled+ 2022 §2 가 적은 {HELLED_POLYTROPE_R_KM:.0f} km "
          f"({d * 100:.3f} %)")
    # 논문은 K 를 2.1e12 로 적고 단위를 SI 로 달았다. SI 로 읽으면 이렇게 된다.
    au = polytrope_radius_n1(2.1e12) / 1.495978707e11
    ok = au > 1.0
    if not ok:
        fails.append("단위 함정 검사가 뜻을 잃었다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 같은 수를 SI 로 읽으면 (K = 2.1e12) "
          f"R = {au:.2f} AU 다 — 그래서 적힌 값이 cgs 이고 SI 는 2.1e5 이다")

    print("\n측정된 행성 — 비회전 구형 모형이므로 **평균반지름** 과 대조한다")
    for name, m, r_mean, r_eq, z in PLANETS:
        res = _giant(m)
        if not res.applicable:
            fails.append(f"{name}: 풀려야 하는데 거절했다 — {res.reason[:70]}")
            print(f"  [FAIL] {name} 거절됨")
            continue
        rk = _km(res)
        off = rk / r_mean - 1.0
        if name == "Jupiter":
            ok = abs(off) <= RADIUS_TOL
            if not ok:
                fails.append(f"{name} 반지름 {rk:.0f} km vs 평균 {r_mean} "
                             f"({off * 100:+.1f} %)")
        else:
            # 토성은 **맞지 않는 것이 답** 이다. 그 초과분을 구간에 묶어 두어, 조용히
            # 고쳐지거나 조용히 나빠지는 것을 둘 다 잡는다.
            ok = SATURN_BAND[0] <= off <= SATURN_BAND[1]
            if not ok:
                fails.append(f"{name} 초과분 {off * 100:+.1f} % 가 기록된 구간 "
                             f"{SATURN_BAND[0] * 100:.0f}~{SATURN_BAND[1] * 100:.0f} % 밖")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:8} {rk:.0f} km · IAU 평균 "
              f"{r_mean} km ({off * 100:+5.1f} %) · 적도 1-bar {r_eq} km "
              f"({(rk / r_eq - 1) * 100:+5.1f} %) · 중원소 {z[0]}–{z[1]} M⊕")
    print("         토성이 20 % 초과하는 것은 **이 관계식의 한계이고 출처가 그것을 "
          "예고한다.** Helled+ 2022 §2 가 index-1 근사가 목성보다 토성에 덜 맞는 이유로 "
          "P∝ρ² 가 토성 외피에 덜 맞는 것과 토성이 중원소가 더 많은 것 둘을 든다. "
          "필요한 것은 외피에 금속을 실은 상태방정식이고, 이 파일에 없다.")

    print("\n목성 NMoI — 값을 고르지 않고 조사해서 밴드를 정했다")
    res = _giant(JUPITER_MASS_EARTH)
    n = res.values["nmoi"]
    lo, hi = JUPITER_NMOI_BAND
    off = 0.0 if lo <= n <= hi else min(abs(n - lo), abs(n - hi)) / ((lo + hi) / 2)
    ok = off <= NMOI_TOL
    if not ok:
        fails.append(f"목성 C/MR² {n:.4f} 가 앵커 밴드 {lo}–{hi} 에서 {off * 100:.1f} % 밖")
    print(f"  [{'PASS' if ok else 'FAIL'}] 도출 {n:.4f} · 앵커 {lo}–{hi} "
          f"(Neuenschwander+ 2021 ∪ Wahl+ 2017) · 밴드 밖 {off * 100:.2f} %")
    ok = JUPITER_NMOI_WIDE[0] <= lo and hi <= JUPITER_NMOI_WIDE[1]
    if not ok:
        fails.append("앵커 밴드가 Helled+ 2011 의 독립 범위 안에 없다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 그 밴드가 Helled+ 2011 의 독립 범위 "
          f"{JUPITER_NMOI_WIDE[0]}–{JUPITER_NMOI_WIDE[1]} 안에 든다")
    for label, v in JUPITER_NMOI_REJECTED.items():
        print(f"         쓰지 않은 값 — {label} {v} ({(v / ((lo + hi) / 2) - 1) * 100:+.1f} % "
              f"대비 앵커). 이유는 이 파일 머리의 주석에 있다.")

    print("\nAlpha Centauri A b — 이 작업이 무엇을 여는가")
    res = _giant(AB_MASS_EARTH)
    if not res.applicable:
        fails.append(f"A b: 풀려야 하는데 거절했다 — {res.reason[:70]}")
        print("  [FAIL] A b 거절됨")
    else:
        rk = _km(res)
        n = res.values["nmoi"]
        drift = n / AB_CLASS_TABLE_NMOI - 1.0
        ok = True
        print(f"  [PASS] 풀림 — R {rk:.0f} km = {rk / R_JUP_EQ_KM:.3f} R_J "
              f"(보드 선언 {AB_RADIUS_RJ:.1f} R_J, {(rk / (AB_RADIUS_RJ * R_JUP_EQ_KM) - 1) * 100:+.1f} %) · "
              f"C/MR² {n:.4f} · P_c {res.values['core_pressure']:.0f} GPa")
        print(f"  [보고] 클래스 표 상수는 {AB_CLASS_TABLE_NMOI} 다. 적분값이 "
              f"{n:.4f} 로 **{drift * 100:+.1f} %** 다. J₂ 가 Radau-Darwin 으로 이 값을 "
              f"먹고, 그 J₂ 가 21시간 위성 적분의 입력이다 — 보드를 바꿀지는 오너가 "
              f"정한다. `engine/backflow.py impact body_figure` 가 무엇이 열리는지 말한다.")
        if abs(drift) < 0.05:
            fails.append("클래스 상수와의 차이가 5 % 안이다 — 보고할 발견이 아니게 됐다")

    print("\n거대행성 안의 압축된 암석 핵 — 2026-08-27 에 어디까지 열렸나")
    # 직전 판까지 이 자리는 통째로 막혀 있었다. 19 M⊕ 규산염 핵이 **혼자서** 3.4 TPa 까지
    # 자기압축하고 PREM 적합이 3.5 TPa 에서 끝나서다. 규산염이 13.5 TPa 까지 이어지면서
    # 이 갈래가 열렸는데, **끝까지 열리지는 않았다** — 그 경계가 어디인지가 이 절의 내용이다.
    #
    # 그리고 막는 것이 바뀌었다. 이제는 핵의 자기압축이 아니라 **외피의 하중** 이다.
    # 같은 19 M⊕ 를 알몸으로 두면 3.43 TPa 로 새 천장 한참 아래인데, 목성 안에 넣으면
    # 그 위로 밀린다. 그래서 상한은 핵 질량 하나로 정해지지 않고 외피 질량에 달렸다.
    # 이분법 눈금은 24회면 60 M⊕ 폭에서 4e-6 M⊕ 다. 한 번이 사격 한 벌이라 비싸다.
    lo, hi = 0.0, 60.0
    for _ in range(24):
        mid = 0.5 * (lo + hi)
        if _giant(JUPITER_MASS_EARTH, mid).applicable:
            lo = mid
        else:
            hi = mid
    core_cap = lo
    bare, _ = shoot(19.0 * EARTH_MASS_KG, 0.0, 0.0, "fe_prem")
    ok = 0.0 < core_cap < 42.0
    if not ok:
        fails.append(f"목성 안 규산염 핵 상한이 {core_cap:.1f} M⊕ 로 뜻이 안 통한다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 317.8 M⊕ 거대행성이 담을 수 있는 규산염 핵은 "
          f"{core_cap:.2f} M⊕ 까지다")
    for core in (11.0, core_cap * 0.99, 19.0, 42.0):
        res = _giant(JUPITER_MASS_EARTH, core)
        if res.applicable:
            print(f"         핵 {core:5.2f} M⊕ → R {_km(res):.0f} km · C/MR² "
                  f"{res.values['nmoi']:.4f} · P_c "
                  f"{res.values['core_pressure'] / 1e3:.2f} TPa · {res.grade}")
        else:
            print(f"         핵 {core:5.2f} M⊕ → 거절 ({res.reason[:60]}…)")
    over = _giant(JUPITER_MASS_EARTH, 19.0)
    named = not over.applicable and "silicate" in over.reason and "13500" in over.reason
    if not named:
        fails.append("19 M⊕ 핵 거절이 규산염의 새 상한을 이름 대지 않는다")
    print(f"  [{'PASS' if named else 'FAIL'}] Guillot 의 19 M⊕ 는 **여전히 거절** 하고, "
          f"이제 3.5 가 아니라 13.5 TPa 를 이름 댄다")
    print(f"         막는 것이 바뀌었다는 것이 요점이다. 19 M⊕ 규산염을 알몸으로 두면 "
          f"중심압이 {bare.p_center / 1e12:.2f} TPa 로 새 천장 한참 아래다 — 목성 안에서 "
          f"넘기는 것은 자기압축이 아니라 외피의 하중이고, 그래서 이 상한은 핵 질량이 "
          f"아니라 **핵과 외피의 짝** 이 정한다. Guillot 의 목성 중원소 11–42 M⊕ 중 "
          f"아래쪽만 압축된 핵으로 들어간다.")

    print("\n거절 — 아직 밖인 것은 이름을 대며 거절하는가")
    for label, kwargs, keyword in (
            ("갈색왜성", dict(mass_earth=5000.0, body_class="brown_dwarf"), "중수소"),
            ("별", dict(mass_earth=3e5, body_class="star"), "n = 3/2"),
            # 얼음거대행성은 2026-08-27 에 열렸다. 남은 거절은 얼음층을 안 준 경우이고,
            # 그건 클래스가 아니라 선언의 문제다.
            ("얼음 없는 얼음 자이언트",
             dict(mass_earth=17.0, body_class="ice_giant", core_mass_fraction=0.0,
                  ice_mass_fraction=0.0, gas_mass_fraction=0.13,
                  potential_temperature=2500.0), "얼음거대행성이 아니다"),
            ("서브넵튠", dict(mass_earth=8.0, body_class="sub_neptune"), "광증발"),
            ("가스인데 암석 클래스",
             dict(mass_earth=120.0, core_mass_fraction=0.0, ice_mass_fraction=0.0,
                  gas_mass_fraction=0.9, body_class="rocky"), "어긋나면")):
        res = solve(**kwargs)
        ok = not res.applicable and keyword in res.reason
        if not ok:
            fails.append(f"{label}: 거절하며 '{keyword}' 를 이름 대야 한다 — "
                         f"{res.reason[:60] if not res.applicable else '풀렸다'}")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")

    print("\n응축체로 새지 않는가 — 폴리트로프가 암석·얼음 천체를 건드리면 안 된다")
    for label, kwargs, want in (
            ("지구", dict(mass_earth=1.0, core_mass_fraction=0.325), 0.3297),
            ("가니메데 조성", dict(mass_earth=0.0248, core_mass_fraction=0.0,
                              ice_mass_fraction=0.407), None)):
        res = solve(**kwargs)
        ok = res.applicable and "h_he" not in (res.notes[0] if res.notes else "")
        if want is not None:
            ok = ok and abs(res.values["nmoi"] - want) < 5e-4
        if not ok:
            fails.append(f"{label} 가 움직였다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label} C/MR² "
              f"{res.values['nmoi']:.4f}" + (f" (기준 {want})" if want else ""))

    # ── 검증 범위가 등급에 나타나는가 ──────────────────────────────────
    #
    # 이 갈래는 어느 거대행성에도 같은 반지름과 같은 C/MR² 를 돌려준다. 그러니
    # "얼마나 맞는가" 는 계산이 아니라 **어디서 시험됐는가** 가 정하고, 그 사실이
    # 값을 받는 쪽에 보여야 한다. 등급이 그 자리다.
    print("\n검증 범위 — 시험된 곳과 아닌 곳이 등급으로 갈리는가")
    for label, m, want in (
            ("목성은 calibrated — 이 갈래가 맞은 유일한 곳", JUPITER_MASS_EARTH, "calibrated"),
            ("토성은 analog — +20.7 % 로 측정된 곳", PLANETS[1][1], "analog"),
            ("두 앵커 사이는 analog — 시험된 적이 없다", AB_MASS_EARTH, "analog")):
        got = _giant(m).grade
        ok = got == want
        if not ok:
            fails.append(f"검증 범위: {label} — grade {got}")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")

    # 등급만 내리고 이유를 안 적으면 받는 쪽이 왜인지 모른다.
    ab = _giant(AB_MASS_EARTH)
    said = any("검증되지 않은 질량" in n for n in ab.notes)
    if not said:
        fails.append("검증 범위: 등급은 내렸는데 note 가 이유를 안 적는다")
    print(f"  [{'PASS' if said else 'FAIL'}] 강등 이유를 note 가 이름 댄다")

    print("\n계약 — 페이로드가 거대행성에서도 제 몫을 하는가")
    res = _giant(AB_MASS_EARTH)
    for label, cond in (
            ("가스질량분율이 inputs 에", "gas_mass_fraction" in res.inputs),
            ("모든 값에 단위", set(res.values) <= set(res.units)),
            ("근거 동반", "2022arXiv220210046H" in res.refs),
            ("regime 에 층이 보인다", "h_he" in res.regime)):
        if not cond:
            fails.append(f"계약: {label}")
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")

    print(f"\n  폴리트로프 유효 상한 {DEUTERIUM_LIMIT_MJ:.0f} M_J "
          f"(= {DEUTERIUM_LIMIT_MJ * JUPITER_MASS_EARTH:.0f} M⊕) 의 중심압까지. "
          f"지수 n = {POLYTROPE_N_HHE:.0f}, K = {POLYTROPE_K_HHE:.1e} SI.")

    if fails:
        print(f"\n실패 {len(fails)}건")
        for f in fails:
            print(f"  · {f}")
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
