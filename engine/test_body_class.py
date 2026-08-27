# body_class 검사 — 태양계 여덟 천체가 맞게 갈리는가, 경계 근처를 모호하다고 말하는가
"""Anchors for `body_class`.

    python3 engine/test_body_class.py
    python3 engine/test_body_class.py --table     # 문서 §Domain 의 태양계 표를 다시 낸다

**판정선은 태양계 여덟이다.** 이 노드는 다른 노드와 달리 앵커가 풍부하다 — 수성·금성·
지구·화성이 암석, 목성·토성이 가스거대행성, 천왕성·해왕성이 얼음거대행성이고, 전부
측정된 질량과 반지름이다. 못 맞히면 경계가 틀린 것이다.

질량과 반지름은 **발표된 값** 이다. 반지름은 Archinal+ 2011 (IAU/IAG WGCCRE) Table 4 의
평균반지름, 질량은 Luzum+ 2011 (IAU 2009 상수계) 의 GM 비다. 우리 출력으로 우리를
시험하지 않는다.

경계는 어느 것도 이 여덟에 맞춰 잡지 않았다. 한 번 그렇게 잡았다가 버렸다 — 천왕성과
토성으로 띠를 그어 놓고 여덟으로 검증하면 아무것도 증명하지 못한다.
"""
from __future__ import annotations

import sys

from body_class import (DEUTERIUM_BAND_MJ, GAS_DOMINATED_ME, HBMM_BAND_MSUN,
                        LADDER, M_EARTH_PER_MJ, M_EARTH_PER_MSUN,
                        SUB_NEPTUNE_R_MAX, solve)
from mass_radius import VALLEY_HI, VALLEY_LO

# (이름, 질량 M⊕, 평균반지름 R⊕, 발표된 클래스)
# 반지름은 Archinal+ 2011 Table 4 의 km 를 6371.00 km 로 나눈 값이다.
SOLAR_SYSTEM = [
    ("Mercury", 0.055274, 2439.7 / 6371.00, "rocky"),
    ("Venus",   0.814998, 6051.8 / 6371.00, "rocky"),
    ("Earth",   1.000000, 6371.0 / 6371.00, "rocky"),
    ("Mars",    0.107447, 3389.5 / 6371.00, "rocky"),
    ("Jupiter", 317.828,  69911. / 6371.00, "gas_giant"),
    ("Saturn",  95.1609,  58232. / 6371.00, "gas_giant"),
    ("Uranus",  14.5357,  25362. / 6371.00, "ice_giant"),
    ("Neptune", 17.1476,  24622. / 6371.00, "ice_giant"),
]

# 보드가 선언한 천체. 도출이 선언을 재현하는가 — 어긋나면 그것이 발견이다.
DECLARED = [
    ("Earth",              1.0,    1.0,    "rocky",   None),
    ("Pandora (A b III)",  0.6447, 0.8984, "rocky",   None),
    ("Alpha Centauri A b", 120.0,  11.209, "giant",   "gas_giant"),
]


def table() -> None:
    """문서의 태양계 표를 다시 낸다. 손으로 친 표는 어긋난다."""
    print("| body | M (M⊕) | R (R⊕) | derived | published | grade | decided by |")
    print("|---|---|---|---|---|---|---|")
    for name, m, r, want in SOLAR_SYSTEM:
        res = solve(mass_earth=m, radius_earth=r)
        got = res.values["classes"]
        mark = got if got == want else f"**{got}**"
        print(f"| {name} | {m:.4g} | {r:.3f} | {mark} | {want} | {res.grade} | "
              f"{res.values['decided_by']} |")


def main() -> int:
    fails: list[str] = []
    if "--table" in sys.argv:
        table()
        return 0

    print("판정선 — 태양계 여덟이 맞게 갈리는가")
    for name, m, r, want in SOLAR_SYSTEM:
        res = solve(mass_earth=m, radius_earth=r)
        ok = res.applicable and res.values["class"] == want
        if not ok:
            fails.append(f"{name}: '{res.values.get('classes')}' 가 나온다 — {want} 여야 한다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:9} {m:8.4g} M⊕ {r:6.3f} R⊕ → "
              f"{res.values['classes']:12} ({res.grade})")

    print("\n선언된 셋 — 도출이 선언을 재현하는가")
    for name, m, r, declared, canonical in DECLARED:
        res = solve(mass_earth=m, radius_earth=r, declared_class=declared)
        ok = res.values["agrees_with_declared"] is True
        if not ok:
            fails.append(f"{name}: 선언 '{declared}' 와 도출 "
                         f"'{res.values['classes']}' 가 어긋난다")
        note = f" (정본 철자 {canonical})" if canonical else ""
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:20} 선언 {declared:6} → "
              f"{res.values['classes']}{note}")

    print("\n모호 — 경계 근처를 한 칸에 우겨넣지 않는가")
    ambiguous = [
        ("밸리 한가운데", dict(mass_earth=4.0,
                          radius_earth=0.5 * (VALLEY_LO + VALLEY_HI)),
         ("rocky", "sub_neptune")),
        ("고립질량과 최대핵질량 사이",
         dict(mass_earth=0.5 * (20.0 + GAS_DOMINATED_ME), radius_earth=5.0),
         ("ice_giant", "gas_giant")),
        ("중수소 한계 한가운데",
         dict(mass_earth=0.5 * sum(DEUTERIUM_BAND_MJ) * M_EARTH_PER_MJ,
              radius_earth=12.0),
         ("gas_giant", "brown_dwarf")),
        ("수소연소 한계 한가운데",
         dict(mass_earth=0.5 * sum(HBMM_BAND_MSUN) * M_EARTH_PER_MSUN,
              radius_earth=12.0),
         ("brown_dwarf", "star")),
        # 반지름이 없으면 사다리의 아래쪽 절반이 통째로 열린 채로 남는다. 서브넵튠과
        # 얼음거대행성을 가르는 것도, 얼음과 가스를 가르는 것도(질량 띠 사이라) 없다.
        ("반지름이 없다 — 아래쪽 세 칸이 다 열린다",
         dict(mass_earth=30.0), ("sub_neptune", "ice_giant", "gas_giant")),
    ]
    for label, kw, want in ambiguous:
        res = solve(**kw)
        got = tuple(res.values["classes"].split(" | "))
        ok = got == want and res.values["class"] is None and res.grade == "judgment"
        if not ok:
            fails.append(f"모호 '{label}': {got} 가 나오고 등급이 {res.grade} 다 — "
                         f"{want} 를 judgment 로 내야 한다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:34} → "
              f"{res.values['classes']} ({res.grade})")

    print("\n선언과 도출이 어긋나면 말하는가")
    # 해왕성을 giant 로 선언한다. 지금 소비처가 이 문자열을 그대로 받으므로, 이것이
    # 막히지 않으면 H/He 폴리트로프가 얼음거대행성 위에서 돈다.
    res = solve(mass_earth=17.1476, radius_earth=24622. / 6371.0,
                declared_class="giant")
    ok = (res.values["agrees_with_declared"] is False
          and res.values["class"] == "ice_giant"
          and any("선언과 도출이 어긋난다" in n for n in res.notes))
    if not ok:
        fails.append("해왕성을 giant 로 선언했는데 어긋남을 말하지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 해왕성을 'giant' 로 선언 → "
          f"도출 {res.values['class']} · agrees {res.values['agrees_with_declared']}")

    res = solve(mass_earth=1.0, radius_earth=1.0, declared_class="ZZZ_bogus")
    ok = (res.values["agrees_with_declared"] is False
          and any("어휘 밖" in n for n in res.notes))
    if not ok:
        fails.append("어휘에 없는 선언을 어휘 밖이라고 말하지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 어휘 밖 선언 'ZZZ_bogus' → "
          f"agrees {res.values['agrees_with_declared']}")

    print("\n등급 — 근거가 강한 경계와 관례인 경계가 갈리는가")
    grades = [
        ("밸리로 갈린 암석 (실측 개체군)", dict(mass_earth=1.0, radius_earth=1.0),
         "calibrated"),
        ("최대 핵질량으로 갈린 가스거대행성", dict(mass_earth=317.8, radius_earth=10.97),
         "analog"),
        (f"{SUB_NEPTUNE_R_MAX} R⊕ 관례선으로 갈린 얼음거대행성",
         dict(mass_earth=14.54, radius_earth=3.981), "judgment"),
        ("반지름이 없어 질량으로 읽은 암석", dict(mass_earth=0.5), "judgment"),
    ]
    for label, kw, want in grades:
        res = solve(**kw)
        ok = res.grade == want
        if not ok:
            fails.append(f"등급 '{label}': {res.grade} 인데 {want} 여야 한다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:36} → {res.grade}")

    print("\n거절 — 못 하는 것을 이름 대며 거절하는가")
    for label, kw, needle in (
            ("질량이 없다", dict(mass_earth=0.0), "양수가 아니다"),
            ("감자 반지름 아래", dict(mass_earth=1e-5, radius_earth=150.0 / 6371.0),
             "감자-구 전이"),
    ):
        res = solve(**kw)
        ok = (not res.applicable) and needle in res.reason
        if not ok:
            fails.append(f"거절 '{label}': 이유가 '{needle}' 를 말하지 않는다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:16} → {res.reason[:62]}…")

    res = solve(mass_earth=3e-4, radius_earth=250.0 / 6371.0)
    ok = res.applicable and res.grade == "judgment" and any(
        "유체 평형이" in n for n in res.notes)
    if not ok:
        fails.append("감자-구 전이 구간 안에서 등급을 내리고 이유를 적지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 전이 구간 안 (250 km) → "
          f"{res.values['classes']} ({res.grade})")

    print("\n어휘 — 정본 여섯, 별칭 하나")
    res = solve(mass_earth=120.0, radius_earth=11.209, declared_class="giant")
    for label, cond in (
            ("사다리가 여섯", len(LADDER) == 6),
            ("'giant' 는 내보내지 않는다", res.values["class"] == "gas_giant"),
            ("별칭을 note 가 이름 댐",
             any("정본은 'gas_giant'" in n for n in res.notes)),
            ("사다리에 중복 없음", len(set(LADDER)) == 6)):
        if not cond:
            fails.append(f"어휘: {label}")
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")

    print("\n계약 — 페이로드가 제 몫을 하는가")
    res = solve(mass_earth=1.0, radius_earth=1.0, declared_class="rocky")
    for label, cond in (
            ("inputs 기록", set(res.inputs) >= {"mass_earth", "declared_class"}),
            ("모든 값에 단위", set(res.values) <= set(res.units)),
            ("class 가 출력", "class" in res.values),
            ("근거 동반", bool(res.refs)),
            ("선언이 계산에 안 쓰임",
             solve(mass_earth=1.0, radius_earth=1.0, declared_class="star")
             .values["class"] == "rocky")):
        if not cond:
            fails.append(f"계약: {label}")
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    print(f"  {res.evidence()[:150]}")

    if fails:
        print(f"\n실패 {len(fails)}건")
        for f in fails:
            print(f"  · {f}")
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
