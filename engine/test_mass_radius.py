# 질량-반지름 레시피 앵커 — 문서의 worked example 과 발표된 천체를 재현하는가
"""Anchor mass_radius on published bodies and the document's own worked examples.

    python3 engine/test_mass_radius.py

앵커는 우리 출력이 아니라 남이 발표한 값이다. 여기서는 두 종류를 쓴다 —
태양계·외계행성의 실측 (M, R) 쌍과, 문서 §7 이 직접 계산해 적어둔 예제.
후자가 어긋나면 코드와 문서 중 하나가 틀렸다는 뜻이고, 둘 다 찾을 가치가 있다.
"""
from __future__ import annotations

import sys

from mass_radius import assign, density_gate

TOL = 0.06        # 6 %. Zeng 근사 자체가 "good to a few percent" 라 그보다 빡빡할 수 없다.

# (이름, 질량 M⊕, 조성, 기대 반지름 R⊕, 출처)
ANCHORS = [
    ("Earth",       1.000, "earth_like", 1.000, "정의상 기준점 — 격자 정규화가 맞는지"),
    ("Proxima b",   1.220, "earth_like", 1.070, "문서 §7 worked example (1.22^0.27 ≈ 1.055)"),
    ("TRAPPIST-1e", 0.692, "earth_like", 0.910, "Gillon+ 2017 실측 R = 0.92 R⊕"),
    ("TRAPPIST-1b", 1.374, "earth_like", 1.116, "Agol+ 2021 실측 R = 1.12 R⊕"),
    # 수성은 순철이 **아니다**. 규산염 맨틀이 있어서 핵질량분율이 0.70 이고, 그래서
    # 순철 곡선보다 커야 한다. 층을 풀기 전에는 'iron' 배율이 손으로 맞춘 값이라
    # 수성이 그 위에 얹혀 있었는데, 곡선이 실물이 되면서 자리가 갈렸다. 수성 자체의
    # 앵커는 test_interior.py 가 핵질량분율 0.70 으로 잡는다 (반지름 오차 0.2 %).
]

# 값을 내면 안 되는 것들. 거절 자체가 답이다.
DECLINES = [
    ("sub-Neptune 2.5 R⊕", dict(mass_earth=12.0), "밸리 위 — 확률 관계로 가야 한다"),
    ("Jupiter",            dict(mass_earth=317.8), "전자축퇴 — 거듭제곱 금지"),
    ("Saturn",             dict(mass_earth=95.2),  "전자축퇴"),
    ("super-Earth 9 M⊕",   dict(mass_earth=9.0),   "Zeng 근사 상한 위"),
    ("모르는 조성",         dict(mass_earth=1.0, composition="cheese"), "조성 밖"),
]


def main() -> int:
    fails: list[str] = []

    print("앵커 — 발표된 값과 문서 예제를 재현하는가")
    for name, mass, comp, want, note in ANCHORS:
        r = assign(mass, comp)
        if not r.applicable:
            fails.append(f"{name}: 값이 나와야 하는데 거절했다 — {r.reason[:70]}")
            print(f"  [FAIL] {name:14} 거절됨")
            continue
        got = r.values["radius"]
        off = abs(got - want) / want
        ok = off <= TOL
        if not ok:
            fails.append(f"{name}: {got:.3f} R⊕, 기대 {want} ({off * 100:.1f}%)")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:14} R {got:6.3f} R⊕  "
              f"기대 {want:5.3f}  ({off * 100:4.1f}%)  {note}")

    print("\n순철 곡선 — 실제 천체보다 작은가 (순철보다 밀한 것은 없다)")
    for name, mass, r_real, note in (
            ("Mercury", 0.055, 0.383, "규산염 맨틀이 있으니 순철보다 커야 한다"),
            ("Earth", 1.000, 1.000, "핵질량분율 0.325 이니 더 커야 한다")):
        iron_r = assign(mass, "iron").values["radius"]
        ok = iron_r < r_real
        if not ok:
            fails.append(f"순철 곡선이 {name} 보다 크다 — {iron_r:.3f} vs {r_real}")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:9} 순철 {iron_r:.3f} R⊕ < "
              f"실측 {r_real:.3f} R⊕   {note}")

    print("\n거절 — 레짐 밖은 값이 아니라 이유를 돌려주는가")
    for name, kwargs, why in DECLINES:
        r = assign(**kwargs)
        ok = not r.applicable
        if not ok:
            fails.append(f"{name}: 거절해야 하는데 값을 냈다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:20} {why}")

    print("\n밸리 — 하나로 고르지 않고 애매하다고 말하는가")
    valley = assign(4.0)          # 4 M⊕ → 1.44 R⊕ 근처, 밸리 하단
    for mass in (4.0, 5.0, 6.0):
        r = assign(mass)
        if r.applicable and r.regime == "radius_valley":
            valley = r
            break
    ok = valley.applicable and valley.regime == "radius_valley" and valley.grade == "judgment"
    if not ok:
        fails.append("밸리 거주자를 judgment 등급으로 표시하지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] regime={valley.regime} grade={valley.grade}")
    if ok:
        print(f"         {valley.notes[0]}")

    print("\n밀도 게이트 — 초수성을 기각하는가 (문서 §6)")
    # 채택된 값은 보드에서 그대로 읽는다: Pandora 0.6447 M⊕ · 0.8984 R⊕ · 0.889 ρ⊕.
    # 문서 §7 이 적은 Option B 와 일치한다.
    accepted = density_gate(mass_earth=0.6447, radius_earth=0.8984)
    # 명백한 초수성: 같은 반지름에 순철보다 밀한 질량. 순철 곡선이 층 적분으로
    # 바뀌면서 문턱이 1.53 → 2.4 ρ⊕ 근처로 올라갔다. 1.60 M⊕ 는 순철 곡선
    # (0.880 R⊕) 보다 오히려 **크므로** 이제 통과가 맞다. 2.50 M⊕ 는 순철이
    # 0.992 R⊕ 라 0.8984 R⊕ 로는 담기지 않는다.
    rejected = density_gate(mass_earth=2.50, radius_earth=0.8984)
    for label, res, want_ok in (("Pandora Option B", accepted, True),
                                ("명백한 초수성", rejected, False)):
        ok = res.applicable is want_ok
        if not ok:
            fails.append(f"밀도 게이트 {label}: 기대와 다르다")
        detail = (f"ρ {res.values['density'] / 5.513:.3f} ρ⊕" if res.applicable
                  else res.reason[:56])
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:16} {detail}")

    # 문서 §7 이 기각 근거로 적은 "1.2 ρ⊕ 는 순철보다 밀하다" 는 재현되지 않고,
    # 이제는 **왜 재현되지 않는지도 근거가 있다**. 순철 곡선이 유도된 배율이 아니라
    # Fe(ε) 상태방정식의 적분이 되면서 그 질량대의 한계가 1.53 → 2.04 ρ⊕ 로 올라갔다.
    # 1.2 ρ⊕ 는 그물 한참 안쪽이므로 "초수성이라 기각" 은 틀린 이유였다. 기각이라는
    # 결론 자체는 다른 근거(표면중력 목표)로 여전히 설 수 있다.
    doc_claim = density_gate(mass_earth=1.2 * 0.8984 ** 3, radius_earth=0.8984)
    iron_limit = assign(1.2 * 0.8984 ** 3, "iron").values["radius"]
    limit_rho = (1.2 * 0.8984 ** 3) / iron_limit ** 3
    print(f"  [알림] 문서 §7 의 1.2 ρ⊕ 기각 근거: 이 게이트는 "
          f"{'기각' if not doc_claim.applicable else '통과'}시킨다 "
          f"(그 질량의 순철 한계는 {limit_rho:.2f} ρ⊕)")

    print("\n계약 — 페이로드가 제 몫을 하는가")
    r = assign(1.22)
    for label, cond in (("inputs 기록", set(r.inputs) >= {"mass_earth", "composition"}),
                        ("모든 값에 단위", set(r.values) <= set(r.units)),
                        ("근거 동반", bool(r.refs)),
                        ("evidence 생성", bool(r.evidence()))):
        if not cond:
            fails.append(f"계약: {label}")
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")

    print(f"\n  {r.evidence()[:150]}")
    if fails:
        print(f"\n실패 {len(fails)}건")
        for f in fails:
            print(f"  · {f}")
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
