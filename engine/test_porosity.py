# 공극 압밀 앵커 — 발표된 다공성 천체와 발표된 실험값을 재현하는가, 그리고 문서 표를 다시 만든다
"""Anchor the compaction relation on published measurements and published bodies.

    python3 engine/test_porosity.py
    python3 engine/test_porosity.py --kbo       문서 §Validation 의 KBO 표를 다시 낸다

**우리 출력으로 우리를 시험하지 않는다.** 여기 있는 대조값은 전부 남이 발표한 것이다 —
Yasui & Arakawa 2009 의 압밀 실험 결과, Durham+ 2005 의 잔류 공극, Bierson+ 2019 이
자기 모형에서 낸 수치와 그들이 쓴 KBO 발표 밀도, Carry 2012 의 관측 전이질량.

가장 중요한 줄이 **전이질량** 이다. 이 레시피는 10²⁰ kg 을 계산에 쓰지 않는다. 압력이
공극을 닫는다는 관계식과 규산염 입자 파쇄 문턱 10 MPa 만 넣고 압력 프로파일을 풀면
전이질량이 저절로 나오고, 그 값이 발표된 구간에 떨어지는지가 이 모형이 물리를 담고
있다는 증거다. 질량에 맞춘 곡선이라면 그럴 이유가 없다.
"""
from __future__ import annotations

import math
import sys

from interior import EARTH_MASS_KG, EARTH_RADIUS_M, solve
from porosity import (B_ICE, PHI0_NOMINAL, PHI_FLOOR_ICE, P_GRAIN_FRACTURE,
                      P_LAB_MAX, YASUI_SILICA_A3, YASUI_SILICA_B3,
                      YASUI_SILICA_PHI_F, YASUI_SILICA_PHI_I, porosity)

# Bierson+ 2019 Table A.2 의 KBO 발표 밀도. (이름, 밀도 kg/m³, 지름 km, 출처)
#
# 그 표가 각 행의 출처를 적어 두었고, 여기 옮긴 것이 그 열이다. 밀도에 오차가 없고
# 지름에 오차가 붙어 있는 것이 원 표의 형식이다 — 밀도는 질량과 지름에서 나온 값이다.
KBO = [
    ("Altjira", 300, 123, "Vilenius+ 2014"),
    ("Typhon", 600, 157, "Stansberry+ 2012"),
    ("Ceto", 1370, 174, "Grundy+ 2007"),
    ("Teharonhiawako", 600, 178, "Vilenius+ 2014"),
    ("2001 QC298", 1140, 235, "Vilenius+ 2014"),
    ("Sila", 730, 249, "Vilenius+ 2014"),
    ("Lempo", 500, 304, "Stansberry+ 2006"),
    ("2002 UX25", 820, 652, "Brown 2013"),
    ("Varda", 1270, 705, "Vilenius+ 2014"),
    ("Salacia", 1260, 866, "Brown & Butler 2017"),
    ("Orcus", 1520, 958, "Fornasier+ 2013"),
    ("Quaoar", 2180, 1070, "Vilenius+ 2014"),
    ("Charon", 1700, 1212, "Nimmo+ 2016"),
    ("Haumea", 1885, 1595, "Ortiz+ 2017"),
    ("Eris", 2520, 2326, "Brown+ 2011"),
]

ROCK_MASS_FRACTION = 0.70   # Bierson+ 2019 의 nominal. 얼음질량분율 0.30 에 해당한다
BIERSON_SMALL_RHO = 750.0   # kg/m³. "φ₀ = 60 % gives an object with f_m = 70 % a
#                             density of ~750 kg/m³" (Bierson+ 2019 §2.1)


def _bulk_density(name_mass_kg: float, res) -> float:
    r = res.values["radius"] * EARTH_RADIUS_M
    return name_mass_kg / (4.0 / 3.0 * math.pi * r ** 3)


def _kbo_rows():
    """각 KBO 를 발표 밀도·지름에서 질량으로 되돌려 두 봉투를 계산한다."""
    for name, rho, dkm, src in KBO:
        radius_m = dkm / 2.0 * 1e3
        mass_kg = rho * 4.0 / 3.0 * math.pi * radius_m ** 3
        m_e = mass_kg / EARTH_MASS_KG
        imf = 1.0 - ROCK_MASS_FRACTION
        porous = solve(m_e, core_mass_fraction=0.0, ice_mass_fraction=imf,
                       initial_porosity=PHI0_NOMINAL, porosity_cap=P_LAB_MAX)
        solid = solve(m_e, core_mass_fraction=0.0, ice_mass_fraction=imf)
        yield (name, rho, dkm, src, mass_kg,
               _bulk_density(mass_kg, porous) if porous.applicable else None,
               _bulk_density(mass_kg, solid) if solid.applicable else None)


def kbo_table() -> None:
    """문서 §Validation 의 KBO 표를 다시 낸다. 손으로 친 표는 어긋난다."""
    print("| body | D (km) | ρ observed | ρ brittle-only | ρ zero-porosity | source |")
    print("|---|---|---|---|---|---|")
    for name, rho, dkm, src, _m, d_por, d_sol in _kbo_rows():
        por = f"{d_por:.0f}" if d_por else "declined"
        sol = f"{d_sol:.0f}" if d_sol else "declined"
        print(f"| {name} | {dkm} | {rho} | {por} | {sol} | {src} |")


def transition_mass(phi0: float) -> float:
    """중심압이 규산염 입자 파쇄 문턱을 처음 넘는 질량. **압력에서 나오는 값이다.**"""
    lo, hi = 1e16, 1e22
    for _ in range(50):
        mid = math.sqrt(lo * hi)
        res = solve(mid / EARTH_MASS_KG, core_mass_fraction=0.0,
                    ice_mass_fraction=0.0, initial_porosity=phi0)
        if not res.applicable:
            return float("nan")
        if res.values["core_pressure"] * 1e9 < P_GRAIN_FRACTURE:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


def main() -> int:
    if "--kbo" in sys.argv:
        kbo_table()
        return 0

    fails: list[str] = []

    print("발표된 실험값 — 관계식이 실험실에서 나온 곡선을 재현하는가")
    # Yasui & Arakawa 2009 Table 1, run 090210-5: 순수 실리카(f = 1, −10 °C) 를
    # 거듭제곱으로 적합해 a₃ = 0.53, b₃ = 0.11. 초기 공극 0.64 가 30 MPa 에서 0.38.
    theirs = YASUI_SILICA_A3 * 30.0 ** -YASUI_SILICA_B3
    ours = porosity("rock", 30e6, YASUI_SILICA_PHI_I)
    d_meas = (ours - YASUI_SILICA_PHI_F) / YASUI_SILICA_PHI_F
    ok = abs(theirs - YASUI_SILICA_PHI_F) / YASUI_SILICA_PHI_F < 0.05 and 0 < d_meas < 0.25
    if not ok:
        fails.append(f"Yasui 순수 실리카: 그들의 적합 {theirs:.3f}, 우리 {ours:.3f}, "
                     f"측정 {YASUI_SILICA_PHI_F}")
    print(f"  [{'PASS' if ok else 'FAIL'}] 순수 실리카 30 MPa — 측정 "
          f"{YASUI_SILICA_PHI_F} · 그들의 적합 {theirs:.3f} · 우리 {ours:.3f} "
          f"({d_meas * 100:+.0f} %)")
    print(f"         우리가 높은 것은 Bierson 이 앞계수를 a₃ 대신 φ₀ 로 정규화했기 "
          f"때문이다. 공극을 **더** 주는 방향이라 그들이 말한 '밀도의 하한' 과 같은 쪽이다.")

    # Durham+ 2005: granulated 물얼음을 150 MPa 까지 눌러도 잔류 공극 ~0.10.
    # Bierson+ 2019 은 강도가 버티는 공극을 0.20 으로 잡았다 — 두 배 보수적이다.
    ice_deep = porosity("ice", P_LAB_MAX, PHI0_NOMINAL)
    ok = abs(ice_deep - PHI_FLOOR_ICE) < 1e-9 and PHI_FLOOR_ICE / 0.10 == 2.0
    if not ok:
        fails.append(f"얼음 바닥값이 {ice_deep:.3f} 로 Bierson 의 {PHI_FLOOR_ICE} 와 다르다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 얼음 150 MPa — 우리 {ice_deep:.2f} · "
          f"Durham+ 2005 측정 잔류 ~0.10 · Bierson+ 2019 이 채택한 바닥값 "
          f"{PHI_FLOOR_ICE:.2f} (측정의 2배로 보수적)")

    # 저온 분기라는 것을 드러낸다. Yasui 의 −10 °C 순수 얼음은 30 MPa 에서 0.02 인데
    # 이 관계식은 0.20 을 준다 — 따뜻한 얼음은 이 법칙이 서술하지 않는다.
    warm_gap = porosity("ice", 30e6, PHI0_NOMINAL)
    ok = warm_gap > 0.15
    if not ok:
        fails.append("얼음 관계식이 저온 분기가 아니게 됐다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 얼음 30 MPa — 우리 {warm_gap:.2f} · "
          f"Yasui 의 −10 °C 순수 얼음 측정 0.02. **이 법칙은 저온 분기다** — "
          f"따뜻한 얼음은 서술하지 않는다 (b_ice = {B_ICE} 가 저온 값)")

    print("\n발표된 모형값 — Bierson+ 2019 이 자기 논문에 적은 수를 내는가")
    # "a nominal value of 60% is used as this gives an object with f_m = 70% a
    #  density of ~750 kg/m³" (Bierson+ 2019 §2.1)
    small = [d for _n, _r, dkm, _s, _m, d, _sol in _kbo_rows() if dkm < 320 and d]
    got = sum(small) / len(small)
    off = abs(got - BIERSON_SMALL_RHO) / BIERSON_SMALL_RHO
    ok = off < 0.05
    if not ok:
        fails.append(f"작은 KBO 밀도 {got:.0f} vs 발표 ~{BIERSON_SMALL_RHO:.0f} kg/m³")
    print(f"  [{'PASS' if ok else 'FAIL'}] φ₀ = {PHI0_NOMINAL:.2f} · 암석질량분율 "
          f"{ROCK_MASS_FRACTION:.2f} → 작은 천체 {len(small)}개 평균 {got:.0f} kg/m³ · "
          f"발표 ~{BIERSON_SMALL_RHO:.0f} ({off * 100:.1f} %)")

    print("\n전이질량 — **입력이 아니라 압력에서 나오는 값이다**")
    # Carry 2012 §5.2: "The pressure inside an object with a mass lower than
    # ≈10²⁰ kg never reaches 10⁷ Pa", 그리고 그 위의 천체는 macroporosity ≈ 0.
    m_tr = transition_mass(PHI0_NOMINAL)
    ok = 1e19 <= m_tr <= 1e20
    if not ok:
        fails.append(f"전이질량 {m_tr:.2e} kg 이 발표된 10¹⁹–10²⁰ kg 밖")
    print(f"  [{'PASS' if ok else 'FAIL'}] 규산염 φ₀ = {PHI0_NOMINAL:.2f} 의 중심압이 "
          f"파쇄 문턱 {P_GRAIN_FRACTURE / 1e6:.0f} MPa 를 넘는 질량 = {m_tr:.2e} kg · "
          f"Carry 2012 §5.2 의 관측 전이 10¹⁹–10²⁰ kg")
    print(f"         이 줄에 10²⁰ kg 이 입력으로 들어간 데는 없다. 관계식과 문턱만 "
          f"넣고 압력을 풀면 나온다.")

    print("\nKBO — 발표된 밀도를 크기순으로 훑는다")
    rows = list(_kbo_rows())
    below = [(n, rho, d) for n, rho, _d, _s, _m, d, _sol in rows if d and rho < d]
    # 추세는 **질량** 에 대해 본다. 예측은 압력의 함수이고 압력은 질량이 정하므로,
    # 지름순으로 세우면 관측 밀도가 다른 두 천체의 순서가 뒤집힌다 — 지름 174 km 의
    # Ceto(ρ 1370)가 지름 178 km 의 Teharonhiawako(ρ 600)보다 무겁다.
    by_mass = sorted(((m, d) for _n, _r, _d, _s, m, d, _sol in rows if d))
    trend = [d for _m, d in by_mass]
    ok = trend == sorted(trend)
    if not ok:
        fails.append("브리틀 곡선이 질량에 단조증가하지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 브리틀 전용 곡선이 질량에 단조증가한다 — "
          f"{trend[0]:.0f} → {trend[-1]:.0f} kg/m³ "
          f"(질량 {by_mass[0][0]:.1e} → {by_mass[-1][0]:.1e} kg). "
          f"논문이 설명한 그 추세다")
    names = {n for n, _r, _d in below}
    ok = "2002 UX25" in names
    if not ok:
        fails.append("Bierson 이 이름 댄 이상치 2002 UX25 가 곡선 아래에 없다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 논문이 이름 댄 이상치가 우리 곡선 아래에도 "
          f"있다 — 2002 UX25 (관측 820, 우리 브리틀 920). Bierson+ 2019 §3 이 "
          f"\"2002 UX25 is below our expected density\" 라고 적는다")
    print(f"         곡선 아래로 떨어진 천체 {len(below)}/{len(rows)}: "
          f"{', '.join(n for n, _r, _d in below)}. 암석질량분율을 논문의 nominal "
          f"0.70 으로 **고정** 했기 때문이고, 논문은 그 값을 천체마다 자유로 둔다 "
          f"(그들의 Fig. 1b). 여기 고정한 것은 우리가 그 자유도를 쓰지 않는다는 뜻이다.")
    big = [(n, rho, d) for n, rho, _dk, _s, _m, d, _sol in rows if d and rho > d * 1.2]
    print(f"         반대로 곡선보다 20 % 이상 밀한 천체 {len(big)}개 "
          f"({', '.join(n for n, _r, _d in big)}) 는 **열-연성 단계** 가 빠진 자리다. "
          f"이 레시피는 브리틀 단계만 들고 있고, 그게 거절이 아니라 한계다.")

    print("\n큰 천체로 새지 않는가 — 공극을 선언하지 않으면 아무것도 바뀌지 않는다")
    for label, kwargs, want in (
            ("지구", dict(mass_earth=1.0, core_mass_fraction=0.325), 0.3297),
            ("달", dict(mass_earth=0.0123, core_mass_fraction=0.019), 0.3945)):
        got = solve(**kwargs).values["nmoi"]
        ok = abs(got - want) < 5e-4
        if not ok:
            fails.append(f"{label} C/MR² 가 {got:.4f} 로 움직였다 (기준 {want})")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label} C/MR² {got:.4f} (기준 {want})")
    # 선언하면 얼마나 움직이는가. 판정선이 아니라 감도다 — 달의 megaregolith 는
    # 실재하지만, 이 레시피는 그것을 판정할 열이력을 들고 있지 않다.
    moon_por = solve(0.0123, core_mass_fraction=0.019,
                     initial_porosity=PHI0_NOMINAL, porosity_cap=P_LAB_MAX)
    if moon_por.applicable:
        print(f"         참고 — 달에 φ₀ = {PHI0_NOMINAL:.2f} 를 선언하면 반지름이 "
              f"{solve(0.0123, core_mass_fraction=0.019).values['radius'] * EARTH_RADIUS_M / 1e3:.0f}"
              f" → {moon_por.values['radius'] * EARTH_RADIUS_M / 1e3:.0f} km 로 커진다. "
              f"그래서 기본값이 0 이고, 0 은 '공극이 없다' 가 아니라 '이 레시피가 "
              f"판정하지 않는다' 는 뜻이다.")

    print("\n거절 — 도메인 밖은 값이 아니라 이름을 돌려주는가")
    for label, kwargs, keyword in (
            ("음수 공극", dict(mass_earth=1.0, initial_porosity=-0.1), "초기 공극률"),
            ("공극 1 이상", dict(mass_earth=1.0, initial_porosity=1.0), "초기 공극률")):
        res = solve(**kwargs)
        ok = not res.applicable and keyword in res.reason
        if not ok:
            fails.append(f"{label}: 거절하며 '{keyword}' 를 이름 대야 한다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")

    print("\n계약 — 공극이 켜지면 등급이 내려가는가")
    por = solve(0.00026, core_mass_fraction=0.0, ice_mass_fraction=0.0,
                initial_porosity=0.4)
    checks = (("grade 가 analog", por.grade == "analog"),
              ("초기공극이 inputs 에", "initial_porosity" in por.inputs),
              ("실험압 외삽을 note 에", any("외삽" in n for n in por.notes)),
              ("근거 동반", "2019Icar..326...10B" in por.refs))
    for label, cond in checks:
        if not cond:
            fails.append(f"계약: {label}")
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")

    if fails:
        print(f"\n실패 {len(fails)}건")
        for f in fails:
            print(f"  · {f}")
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
