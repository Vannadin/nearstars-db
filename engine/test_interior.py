# 내부 구조 앵커 — 실측된 관성모멘트를 재현하는가, 그리고 문서 표를 다시 만든다
"""Anchor interior_layers on measured moments of inertia, and regenerate the doc table.

    python3 engine/test_interior.py
    python3 engine/test_interior.py --table     문서 §Validation 표를 다시 낸다

앵커는 전부 **측정된** C/MR² 다 — 중력장이나 세차에서 나온 값이지 모형에서 나온
값이 아니다. 우리 출력으로 우리를 시험하면 아무것도 검증되지 않는다.
"""
from __future__ import annotations

import sys

from interior import layers, mean_density

# 층 밀도를 직접 넘긴다. 기본 표는 지구 근처에서만 유효하고, 나머지 셋은 그 밖이다 —
# 그래서 이 앵커들은 **기하와 관성모멘트 수식이 맞는지**를 시험하지, 밀도표를
# 시험하지 않는다. 두 질문은 다르고, 섞으면 어느 쪽이 틀렸는지 알 수 없다.
#
# (이름, 질량 M⊕, 반지름 R⊕, CMF, 핵밀도, 맨틀밀도, 발표 C/MR², 발표 f, 출처)
ANCHORS = [
    ("Earth",   1.0000, 1.0000, 0.325, 10900, 4500, 0.3307, 3480 / 6371,
     "PREM (Dziewonski & Anderson 1981)"),
    ("Mars",    0.1074, 0.5320, 0.24,   6500, 3500, 0.3644, 1830 / 3390,
     "Konopliv+ 2011 · InSight"),
    ("Mercury", 0.0553, 0.3829, 0.70,   7800, 3300, 0.3460, 2020 / 2440,
     "Margot+ 2012 (MESSENGER)"),
    ("Moon",    0.0123, 0.2727, 0.019,  7000, 3300, 0.3931, 350 / 1737,
     "Williams+ 2014 (LLR)"),
]

# 거절해야 하는 것들. 거절이 답이다.
DECLINES = [
    ("Ganymede", dict(mass_earth=0.0248, radius_earth=0.4135, core_mass_fraction=0.25),
     "3층 얼음 천체 — 2층으로 풀면 핵 경계가 0.46, 실측 0.27"),
    ("Callisto", dict(mass_earth=0.0180, radius_earth=0.3783, core_mass_fraction=0.25),
     "얼음이 두껍다 (1834 kg/m³)"),
    ("미분화",    dict(mass_earth=1.0, radius_earth=1.0, core_mass_fraction=0.0),
     "놓을 핵이 없다 — 균질구의 0.4"),
    ("맨틀 없음", dict(mass_earth=1.0, radius_earth=1.0, core_mass_fraction=1.0),
     "맨틀이 없다"),
    ("모르는 조성", dict(mass_earth=1.0, radius_earth=1.0, core_mass_fraction=0.3,
                     composition="cheese"), "층 밀도가 정의되지 않았다"),
]

TOL = 0.05      # 5 %. 지구가 4.8 % 이고 그게 최악값이다 — 그보다 빡빡할 수 없다.


def rows():
    for name, m, r, cmf, rc, rm, nmoi_pub, f_pub, src in ANCHORS:
        res = layers(m, r, cmf, core_density=rc, mantle_density=rm)
        yield name, res, nmoi_pub, f_pub, src


def table() -> None:
    """문서 §Validation 표를 다시 낸다. 손으로 친 표는 어긋난다."""
    print("| body | C/MR² derived | published | error | f derived | f published |")
    print("|---|---|---|---|---|---|")
    for name, res, nmoi_pub, f_pub, _ in rows():
        n, f = res.values["nmoi"], res.values["core_radius_fraction"]
        print(f"| {name} | {n:.4f} | {nmoi_pub:.4f} | "
              f"{abs(n - nmoi_pub) / nmoi_pub * 100:.1f} % | {f:.3f} | {f_pub:.3f} |")


def main() -> int:
    if "--table" in sys.argv:
        table()
        return 0

    fails: list[str] = []

    print("앵커 — 실측된 관성모멘트를 재현하는가")
    worst = 0.0
    for name, res, nmoi_pub, f_pub, src in rows():
        if not res.applicable:
            fails.append(f"{name}: 값이 나와야 하는데 거절했다 — {res.reason[:60]}")
            print(f"  [FAIL] {name:9} 거절됨")
            continue
        n, f = res.values["nmoi"], res.values["core_radius_fraction"]
        off = abs(n - nmoi_pub) / nmoi_pub
        worst = max(worst, off)
        ok = off <= TOL
        if not ok:
            fails.append(f"{name}: C/MR² {n:.4f}, 발표 {nmoi_pub} ({off * 100:.1f}%)")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:9} C/MR² {n:.4f} "
              f"발표 {nmoi_pub:.4f} ({off * 100:4.1f}%)  f {f:.3f} vs {f_pub:.3f}  {src}")

    # 부호. 균질층은 자기압축을 무시하므로 압축이 큰 천체에서 크게 나온다.
    # 다만 이건 층 밀도가 옳을 때의 이야기라 불변식으로 걸지 않는다 — 밀도가
    # 조금만 어긋나도 부호가 뒤집힌다. 관찰로만 적는다.
    print("\n오차의 부호 (불변식 아님 — 밀도가 옳을 때의 경향)")
    signs = [res.values["nmoi"] - pub for _, res, pub, _, _ in rows() if res.applicable]
    print(f"         {[f'{s:+.4f}' for s in signs]}")

    print("\n거절 — 도메인 밖은 값이 아니라 이유를 돌려주는가")
    for name, kwargs, why in DECLINES:
        res = layers(**kwargs)
        ok = not res.applicable
        if not ok:
            fails.append(f"{name}: 거절해야 하는데 값을 냈다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name:12} {why}")

    print("\n기본 밀도표 — 지구 근처에서만 쓰겠다고 말하는가")
    inside = layers(1.0, 1.0, 0.325)                       # 지구. 표를 써도 된다
    outside = layers(0.0553, 0.3829, 0.70, "iron_rich")    # 수성. 밖이다
    for label, res, want_ok in (("지구 (표 안)", inside, True),
                                ("수성 (표 밖)", outside, False)):
        ok = res.applicable is want_ok
        if not ok:
            fails.append(f"기본 밀도표 {label}: 기대와 다르다")
        detail = (f"C/MR² {res.values['nmoi']:.4f}" if res.applicable else res.reason[:54])
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:12} {detail}")

    print("\n계약 — 페이로드가 제 몫을 하는가")
    r = layers(1.0, 1.0, 0.325)
    for label, cond in (("inputs 기록", set(r.inputs) >= {"mass_earth", "core_mass_fraction"}),
                        ("모든 값에 단위", set(r.values) <= set(r.units)),
                        ("근거 동반", bool(r.refs)),
                        ("한계를 note 에 적음", bool(r.notes)),
                        ("grade 가 analog", r.grade == "analog")):
        if not cond:
            fails.append(f"계약: {label}")
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")

    print(f"\n  최악 오차 {worst * 100:.1f}% (허용 {TOL * 100:.0f}%)")
    print(f"  {r.evidence()[:140]}")

    if fails:
        print(f"\n실패 {len(fails)}건")
        for f in fails:
            print(f"  · {f}")
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
