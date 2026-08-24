# 다이나모 레시피 앵커 테스트 — 논문이 발표한 천체를 재현하는지, 도메인 밖을 제대로 거절하는지
"""Known-answer anchors for the giant dynamo recipe.

Every anchor here is a body the *paper* published a field for, not a NearStars
body. A recipe validated only against our own outputs validates nothing.

    python3 engine/test_dynamo.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dynamo import dipole_field  # noqa: E402
from payload import OUT_OF_DOMAIN  # noqa: E402

# (라벨, M_J, R_J, age_Gyr, 기대 B_pol [G], 허용오차, 출처)
ANCHORS = [
    ("Jupiter", 1.00, 1.00, 4.5, 9.0, 0.05,
     "RC10 공표값 9 G; Connerney 실측 극지 8.4 G"),
    ("eps Eri b (paper M sin i)", 1.55, 1.00, 1.7, 19.0, 0.05,
     "RC10 Table 4.3"),
    ("1 M_J young end", 1.00, 1.00, 0.2, 25.6, 0.10,
     "RC10 냉각 트랙 상단 (보정 하한 나이)"),
    ("1 M_J old end", 1.00, 1.00, 10.0, 6.9, 0.05,
     "RC10 냉각 트랙 하단, <10 G"),
]

# 도메인 밖에서 조용히 답하면 안 되는 경우들
REFUSALS = [
    ("rocky planet", dict(mass_mj=0.003, radius_rj=0.09, age_gyr=4.5,
                          body_class="rocky"), "rocky-planet-dynamo"),
    ("brown dwarf", dict(mass_mj=30.0, radius_rj=1.0, age_gyr=1.0), "L(M, age)"),
    ("sub-Neptune", dict(mass_mj=0.05, radius_rj=0.35, age_gyr=4.5), "아날로그"),
    ("stellar", dict(mass_mj=120.0, radius_rj=1.2, age_gyr=1.0), "항성 영역"),
    ("pre-calibration age", dict(mass_mj=1.0, radius_rj=1.0, age_gyr=0.003),
     "보정 하한"),
]

fails = 0

print("앵커 — 논문이 공표한 천체를 재현하는가")
for label, m, r, age, want_g, tol, src in ANCHORS:
    res = dipole_field(m, r, age)
    if not res.applicable:
        print(f"  [FAIL] {label}: 도메인 밖으로 판정됨 — {res.reason}")
        fails += 1
        continue
    got_g = res.values["b_pol"] / 100.0
    off = abs(got_g - want_g) / want_g
    ok = off <= tol
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {label:<26} "
          f"B_pol {got_g:6.2f} G  기대 {want_g:5.1f} G  ({off*100:4.1f}%)  {src}")

print("\n적도 성분과 모멘트 정규화")
jup = dipole_field(1.0, 1.0, 4.5)
b_eq_g = jup.values["b_eq"] / 100.0
ok = abs(b_eq_g - 4.5) < 0.01 and abs(jup.values["dipole_moment"] - 20000) < 1
fails += 0 if ok else 1
print(f"  [{'PASS' if ok else 'FAIL'}] Jupiter B_eq {b_eq_g:.2f} G (실측 ~4.3 G) · "
      f"모멘트 {jup.values['dipole_moment']:,.0f} ×Earth")

print("\n거절 — 도메인 밖은 값이 아니라 이유를 돌려주는가")
for label, kw, expect_in_reason in REFUSALS:
    res = dipole_field(**kw)
    ok = res.regime == OUT_OF_DOMAIN and expect_in_reason in res.reason
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {label:<20} {res.regime}")
    if not ok:
        print(f"         reason={res.reason[:90]}")

print("\n계약 — 페이로드가 제 몫을 하는가")
checks = [
    ("inputs 기록", set(jup.inputs) == {"mass_mj", "radius_rj", "age_gyr", "body_class"}),
    ("모든 값에 단위", all(k in jup.units for k in jup.values)),
    ("근거 동반", len(jup.refs) >= 3),
    ("evidence 생성", "planetary-dynamo-scaling" in jup.evidence()),
    ("드리프트 감지", jup.stale_against({"age_gyr": 3.0}) == ["age_gyr"]),
    ("무드리프트 통과", jup.stale_against({"age_gyr": 4.5}) == []),
]
for label, ok in checks:
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")

print(f"\nevidence 예시:\n  {jup.evidence()}")
print(f"\n거절 예시:\n  {dipole_field(0.05, 0.35, 4.5).evidence()[:150]}")

print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
