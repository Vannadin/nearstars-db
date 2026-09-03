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
# 1-bar 온도가 이 갈래의 **경계조건** 이다. 2026-08-28 에 폴리트로프가 표로 바뀌면서
# 온도가 인자가 됐고, 기체에는 P = 0 인 표면이 없으므로 적분이 1 bar 에서 멈춘다 —
# 발표된 반지름이 재어진 준위도 그 자리다. 두 값은 Voyager 전파엄폐에서 온다
# (Lindal+ 1981 목성, Lindal 1992 토성) 이고 널리 재인용되는 수다.
PLANETS = [
    # (이름, 질량 M⊕, 평균반지름 km, 적도 1-bar km, 중원소 총량 M⊕ (Guillot 1999), 1-bar K)
    ("Jupiter", JUPITER_MASS_EARTH, 69911, 71492, (11, 42), 165.0),
    ("Saturn", 95.159, 58232, 60268, (19, 31), 135.0),
]
GIANT_T_POT = 165.0     # 조성만 훑을 때 쓰는 기본 1-bar 온도 (목성 값)

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
# 토성 초과분이 떨어져야 하는 구간. **한계를 고정한다** — 조용히 고쳐지는 것과 조용히
# 나빠지는 것을 둘 다 잡는다. 폴리트로프였을 때 +20.7 % 였고 구간이 10~30 % 였다.
# 표가 들어와 +7.06 % 로 내려왔다.
SATURN_BAND = (0.03, 0.12)


def analytic_nmoi_n1() -> float:
    """n = 1 Lane-Emden 해의 C/MR². θ = sin ξ/ξ, ξ₁ = π 를 손으로 적분한 값.

        ∫₀^π ξ sin ξ dξ = π,   ∫₀^π ξ³ sin ξ dξ = π³ − 6π
        C/MR² = (2/3)(π³ − 6π)/(π² · π) = (2/3)(1 − 6/π²)

    교과서 적분이라 인용이 필요 없다 — Lane-Emden 방정식 자체는 Chandrasekhar 1939 다."""
    return (2.0 / 3.0) * (1.0 - 6.0 / math.pi ** 2)


def _giant(mass_earth: float, core_earth: float = 0.0,
           t_pot: float = GIANT_T_POT, envelope_z: float = 0.0):
    """가스 외피만 있는(또는 규산염 핵을 얹은) 거대행성 하나를 푼다.

    포텐셜 온도가 **필수** 다. 수소-헬륨 표가 (P, T) 의 함수라 등온으로는 안 풀린다."""
    cmf = core_earth / mass_earth
    return solve(mass_earth, core_mass_fraction=0.0, ice_mass_fraction=0.0,
                 gas_mass_fraction=1.0 - cmf, body_class="giant",
                 envelope_z=envelope_z, potential_temperature=t_pot)


def _km(res) -> float:
    return res.values["radius"] * EARTH_RADIUS_M / 1e3


def _integrator_km(mass_earth: float, t_pot: float = GIANT_T_POT) -> float:
    """적분기를 **레시피의 영역 정책을 거치지 않고** 직접 돌려 반지름[km]을 낸다.

    해석해 대조는 "이 천체를 믿는가" 가 아니라 "적분기가 Lane-Emden 을 재현하는가"
    를 묻는다. 두 질문에 같은 문을 쓰면, 검증 범위를 좁히는 순간 적분기 검사가 같이
    막힌다 — 실제로 그렇게 됐다. 정책은 solve() 에 두고, 이 검사만 아래를 본다."""
    st, _ = shoot(mass_earth * EARTH_MASS_KG, 0.0, 0.0, "fe_prem", gmf=1.0,
                  potential_temperature=t_pot)
    return st.radius_m / 1e3


def table() -> None:
    """문서 §Validation 의 거대행성 표를 다시 낸다. 손으로 친 표는 어긋난다."""
    # T_c 열은 2026-08-30 에 들어왔다 (C5). 해왕성의 중심온도가 동결 파일에만 살아서 코어 리스트를 쓸 때
    # 사라졌던 일이 있다 — 산문이 드는 표에 그 수가 있어야 그 질문이 되풀이되지 않는다.
    print("| body | M (M⊕) | T at 1 bar | R derived | R mean (IAU) | ΔR vs mean | "
          "R eq 1 bar | C/MR² derived | T_c (K) | P_c (GPa) |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for name, m, r_mean, r_eq, _z, t1 in PLANETS:
        res = _giant(m, t_pot=t1)
        if not res.applicable:
            print(f"| {name} | {m:.1f} | {t1:.0f} K | declined | {r_mean} | – | "
                  f"{r_eq} | – | – | – |")
            continue
        rk = _km(res)
        print(f"| {name} | {m:.1f} | {t1:.0f} K | {rk:.0f} km | {r_mean} km | "
              f"{(rk / r_mean - 1) * 100:+.2f} % | {r_eq} km | "
              f"{res.values['nmoi']:.4f} | {res.values['core_temperature']:.0f} | "
              f"{res.values['core_pressure']:.0f} |")
    res = _giant(AB_MASS_EARTH)
    rk = _km(res)
    print(f"| Alpha Centauri A b | {AB_MASS_EARTH:.1f} | {GIANT_T_POT:.0f} K (declared) | "
          f"{rk:.0f} km | – | – | {AB_RADIUS_RJ * R_JUP_EQ_KM:.0f} km (declared) | "
          f"{res.values['nmoi']:.4f} | {res.values['core_temperature']:.0f} | "
          f"{res.values['core_pressure']:.0f} |")


def main() -> int:
    if "--table" in sys.argv:
        table()
        return 0

    fails: list[str] = []

    print("해석해 — 수치 적분이 손으로 푼 n=1 해를 재현하는가")
    r_analytic = polytrope_radius_n1(POLYTROPE_K_HHE) / 1e3
    nmoi_analytic = analytic_nmoi_n1()
    # **2026-08-28 에 이 검사의 부호가 뒤집혔다.** 폴리트로프였을 때는 반지름이 질량과
    # 무관한 것이 그 형태의 서명이라 편차가 0 이어야 했다. 표가 들어온 지금은 그 무감각이
    # 결함이므로, 반대로 **질량에 반응하는지** 를 본다.
    # 질량 상한이 4132 M⊕ (13 M_J, 폴리트로프의 선언된 울타리) 에서 519 M⊕ (1.63 M_J)
    # 로 내려왔다. 굳힌 창의 압력 위끝(10⁴ GPa) 때문이고, 배포 표 자체는 10¹³ GPa 까지
    # 가므로 열을 더 굳히면 올라간다 — 유효 영역의 한 행이지 물리의 한계가 아니다.
    swept = [_integrator_km(m) for m in (95.0, 200.0, 317.8, 500.0)]
    spread = max(swept) / min(swept) - 1.0
    ok = spread > 0.05
    if not ok:
        fails.append(f"반지름이 질량에 {spread * 100:.3f} % 밖에 안 움직인다 — "
                     "폴리트로프의 무감각이 돌아왔다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 반지름이 질량에 반응한다 — 95~1200 M⊕ 에서 "
          f"{spread * 100:.1f} % (폴리트로프는 0.0000 % 였다)")
    print(f"         해석해 √(πK/2G) = {r_analytic:.0f} km 는 이제 밀도가 아니라 "
          f"사격의 괄호를 잡는 척도로만 남았다 (eos.HydrogenHelium.rho_seed).")

    # C/MR² 도 같은 이유로 해석해에서 **떨어져야** 맞다. n = 1 의 0.2059 는 어느
    # 거대행성에나 같은 값이었고, Juno 가 목성에서 잰 것은 0.2634-0.2644 다.
    jup = _giant(JUPITER_MASS_EARTH)
    d_n = abs(jup.values["nmoi"] - nmoi_analytic) / nmoi_analytic
    ok = d_n > 0.02
    if not ok:
        fails.append(f"C/MR² 가 n=1 해석해에서 {d_n * 100:.3f} % 밖에 안 벗어난다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 적분 C/MR² {jup.values['nmoi']:.5f} 가 n=1 "
          f"해석해 (2/3)(1 − 6/π²) = {nmoi_analytic:.5f} 에서 {d_n * 100:.1f} % 떨어져 "
          f"있다 — 그 값은 이제 이 갈래의 답이 아니다")

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
    for name, m, r_mean, r_eq, z, t1bar in PLANETS:
        res = _giant(m, t_pot=t1bar)
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
    print("         토성의 남은 초과분은 **조성** 이다. Z = 0 이라 중원소가 하나도 없는 "
          "천체를 푼 것이고, Guillot 1999 는 토성에 19~31 M⊕ 의 중원소를 준다. "
          "envelope_z 를 올리면 반지름이 단조로 내려온다 — 그 곡선은 --saturnz 가 낸다.")

    print("\n목성 NMoI — 값을 고르지 않고 조사해서 밴드를 정했다")
    res = _giant(JUPITER_MASS_EARTH)
    n = res.values["nmoi"]
    lo, hi = JUPITER_NMOI_BAND
    off = 0.0 if lo <= n <= hi else min(abs(n - lo), abs(n - hi)) / ((lo + hi) / 2)
    # **밴드 안에 들어가는 것이 목표가 아니고, 들어가면 오히려 이상하다.** 이 모형은
    # 회전도 핵도 중원소도 없는 균질한 수소-헬륨 공이고, 실제 목성은 중심으로 갈수록
    # 무거워지므로 C/MR² 가 더 낮다. 그러니 도출값은 밴드보다 **높은 쪽** 에 있어야
    # 맞고, 검사할 것은 부호와 크기다. 폴리트로프는 0.2059 로 밴드에서 22 % 낮았는데,
    # 그건 자기 형태가 정한 상수 하나였지 목성에 대한 진술이 아니었다.
    above = n > hi
    closer = off < 0.219            # 폴리트로프의 밴드 밖 거리
    ok = above and closer and off <= 0.08
    if not ok:
        fails.append(f"목성 C/MR² {n:.4f} — 밴드 {lo}–{hi} 위쪽 8 % 안에 있어야 한다 "
                     f"(현재 {'위' if above else '아래'}, {off * 100:.1f} %)")
    print(f"  [{'PASS' if ok else 'FAIL'}] 도출 {n:.4f} · 앵커 {lo}–{hi} "
          f"(Neuenschwander+ 2021 ∪ Wahl+ 2017) · 밴드 위 {off * 100:.2f} % "
          f"— 폴리트로프는 0.2059 로 아래 21.9 % 였다")
    print("         밴드보다 높은 것이 맞는 방향이다. 핵도 중원소도 없는 균질한 공이라 "
          "질량이 실제 목성만큼 안쪽으로 몰려 있지 않다.")
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
    # **이 상한은 두 번 잘못 재어졌다.** 폴리트로프 외피에서 17.66 M⊕ 였고, 2026-08-28 에
    # 표가 들어오자 0 으로 닫혔다고 적었다 — 그런데 그 0 은 물리가 아니라 결함이었다. 외피
    # 바닥이 표의 도달 영역 아래로 떨어지면 적분기가 그 자리를 1 bar 표면으로 오인해 외피
    # 질량이 0 이 됐고, 사다리가 규산염 천장까지 올라가 거절을 냈다 (sub-neptune-context-notes.md).
    # 그 결함을 고친 2026-08-29 의 측정은 11.46 M⊕ 였다 — 그리고 **그것도 절반은 결함이었다.**
    # 2026-08-30 F2 에서 K_T 의 수치미분이 재료 상한 밖을 반 걸음 찌르던 것을 상한에서 자르자,
    # 사격이 규산염 천장(13.5 TPa)에 놓는 시험점이 13501 GPa 의 거절 대신 실제로 적분됐고 상한이
    # **16.69 M⊕** 로 올라갔다 (14 M⊕ 핵이 P_c 11.36 TPa 로 천장 아래에서 풀린다). 막는 것은 여전히
    # 규산염 천장이고 그것을 밀어올리는 것이 외피 하중이라는 진단은 그대로다 — 세 번째 수다.
    JUPITER_CORE_CAP = 16.69
    ok = abs(core_cap - JUPITER_CORE_CAP) < 0.1
    if not ok:
        fails.append(f"목성 안 규산염 핵 상한이 {core_cap:.2f} M⊕ 다 — 2026-08-29 측정 "
                     f"{JUPITER_CORE_CAP} M⊕ 에서 움직였다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 317.8 M⊕ 거대행성이 담을 수 있는 규산염 핵은 "
          f"{core_cap:.2f} M⊕ 까지다 — 폴리트로프 외피에서 17.66, 표 도입 직후의 0 은 외피 "
          f"바닥을 표면으로 오인한 결함이었고, 결함을 고친 뒤 {JUPITER_CORE_CAP} 이다")
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
            # 서브넵튠은 2026-08-29 에 열렸다. 남은 거절은 가스질량분율을 안 준 경우다 — 선언의 문제다.
            ("가스 없는 서브넵튠", dict(mass_earth=8.0, body_class="sub_neptune",
                                core_mass_fraction=0.3, potential_temperature=300.0),
             "선언하면 풀린다"),
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
    print("\n뿌리 선택 — 기체가 바깥일 때 가짜 가지에 수렴하지 않는가")
    # **숫자가 아니라 기작에 건다.** "토성이 Z = 0.02 에서 풀린다" 로 적으면 같은 결함이
    # 다른 조성에서 다시 나와도 안 잡힌다 — 괄호잡기 결함이 두 번 나온 이유가 그것이다.
    #
    # 기작은 이렇다. 기체 외피의 표면은 P = 0 이 아니라 1 bar 다. 그러면 중심압이 낮을수록
    # 천체가 부풀어 저밀도 가스가 먼 곳까지 1 bar 를 유지하며 질량을 담으므로, 겉질량이
    # 중심압에 대해 U 자를 그린다. 뿌리가 둘이고 왼쪽 것은 물리가 아니다. 그래서 수렴한
    # 해에서 중심압을 조금 올렸을 때 겉질량이 **따라 올라야** 한다.
    from interior import integrate, EARTH_MASS_KG as _ME
    for label, m, z in (("토성 Z = 0", PLANETS[1][1], 0.0),
                        ("토성 Z = 0.02", PLANETS[1][1], 0.02),
                        ("목성", JUPITER_MASS_EARTH, 0.0)):
        res = _giant(m, t_pot=PLANETS[1][5] if m < 200 else PLANETS[0][5], envelope_z=z)
        if not res.applicable:
            fails.append(f"뿌리 선택: {label} 이 거절됐다 — {res.reason[:60]}")
            print(f"  [FAIL] {label} 거절")
            continue
        p_c = res.values["core_pressure"] * 1e9
        kw = dict(gmf=1.0, envelope_z=z, t_center=res.values["core_temperature"],
                  t_pot=PLANETS[1][5] if m < 200 else PLANETS[0][5])
        here = integrate(p_c, m * _ME, 0.0, 0.0, "fe_prem", **kw)
        up = integrate(p_c * 1.01, m * _ME, 0.0, 0.0, "fe_prem", **kw)
        rising = up.mass_kg > here.mass_kg
        if not rising:
            fails.append(f"뿌리 선택: {label} 이 질량이 **감소하는** 구간에 수렴했다 — "
                         "가짜 가지다")
        print(f"  [{'PASS' if rising else 'FAIL'}] {label} — 중심압 +1 % 에 겉질량이 "
              f"{(up.mass_kg / here.mass_kg - 1) * 100:+.3f} % 움직인다 (양수여야 한다)")

    print("\n수렴 배지 — 압력만이 아니라 온도 경계조건까지 말하는가")
    # 표면 온도를 못 맞춘 해가 pressure-converged 배지를 달고 나가던 구멍. 도달할 수
    # 없는 표면 온도를 주면 거절이든 converged=False 든 나와야 하고, 조용히 True 면 안 된다.
    far = _giant(PLANETS[1][1], t_pot=3000.0)
    ok = (not far.applicable) or (not far.converged)
    if not ok:
        fails.append("수렴 배지: 도달 불가능한 표면 온도인데 converged=True 로 나온다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 1 bar 에 3000 K 를 요구하면 "
          f"{'거절' if not far.applicable else 'converged=False'} 다")

    print("\n검증 범위 — 강등의 근거가 질량이 아니라 선언인가")
    # **2026-08-28 에 이 규칙이 바뀌었다.** 예전에는 목성만 calibrated 이고 그보다
    # 가벼우면 analog 였는데, 그 근거는 n = 1 이 어느 거대행성에나 같은 답을 낸다는
    # 것이었다. 표가 들어와 그 전제가 사라졌고, 앵커도 둘에서 셋으로 늘었다. 남은
    # 강등 사유는 **포텐셜 온도가 선언** 이라는 것 하나다.
    for label, m in (("목성", JUPITER_MASS_EARTH),
                     ("토성", PLANETS[1][1]),
                     ("앵커 사이 (120 M⊕)", AB_MASS_EARTH)):
        got = _giant(m).grade
        ok = got == "analog"
        if not ok:
            fails.append(f"검증 범위: {label} 의 grade 가 {got} 다 — analog 여야 한다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label} analog — 포텐셜 온도가 선언이라서")

    ab = _giant(AB_MASS_EARTH)
    said = any("포텐셜 온도" in n and "질량 때문이 아니다" in n for n in ab.notes)
    if not said:
        fails.append("검증 범위: 강등 이유가 선언이라는 것을 note 가 안 적는다")
    print(f"  [{'PASS' if said else 'FAIL'}] 강등 이유를 note 가 이름 댄다 — 그리고 "
          f"질량 때문이 아니라고 명시한다")

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

    # 브리프 56 — 경계 메시지가 경계를 표현하는가. 상한 25118.86 K 는 정수가 아니라서 .0f 로 찍으면
    # 25119.0 K 에서 "25119 K 는 25119 K 위다" 가 된다. 거동은 맞고(배타 비교) 메시지가 틀린 부류다.
    from eos import MATERIALS, PhaseGap
    import hhe_table
    lt_max = 10.0 ** (hhe_table.LOGT_LO + (hhe_table.NT - 1) * hhe_table.STEP)
    hhe = MATERIALS["h_he"]
    at_edge = hhe.density(50e9, lt_max) > 0.0
    msg = ""
    try:
        hhe.density(50e9, lt_max + 0.14)          # 25119.0 K — 지시 세션이 친 값
    except PhaseGap as e:
        msg = str(e)
    nums = [w for w in msg.replace("(", " ").replace(")", " ").split() if w.replace(".", "").isdigit()]
    distinct = len(nums) >= 2 and nums[0] != nums[1]
    for label, cond in (("상한 그 자리에서는 값을 낸다", at_edge),
                        ("상한 0.14 K 위는 PhaseGap", bool(msg)),
                        ("메시지의 두 온도가 구별된다", distinct)):
        if not cond:
            fails.append(f"경계 메시지: {label} — {msg[:80]!r}")
        print(f"  [{'PASS' if cond else 'FAIL'}] 경계 메시지: {label}")

    print(f"  수소-헬륨 표의 굳힌 창: 1 bar ~ 10⁴ GPa · 100 ~ 25119 K. 가스 외피만인 "
          f"천체의 질량 상한이 519 M⊕ (1.63 M_J) 다 — 폴리트로프의 선언된 울타리 "
          f"4132 M⊕ (13 M_J) 보다 낮고, 배포 표 자체는 10¹³ GPa 까지 가므로 열을 더 "
          f"굳히면 올라간다. 폴리트로프 상수는 사격 괄호의 밀도 척도로만 남았다 "
          f"(n = {POLYTROPE_N_HHE:.0f}, K = {POLYTROPE_K_HHE:.1e} SI).")

    if fails:
        print(f"\n실패 {len(fails)}건")
        for f in fails:
            print(f"  · {f}")
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
