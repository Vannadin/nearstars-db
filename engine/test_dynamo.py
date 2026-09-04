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
    ("brown dwarf, no inputs", dict(mass_mj=30.0, radius_rj=1.0, age_gyr=1.0), "없는 입력"),
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
    ("inputs 기록", set(jup.inputs) == {"mass_mj", "radius_rj", "age_gyr", "body_class",
                                         "luminosity_lsun", "rotation_period_h", "radius_rj_min",
                                         "radius_rj_max", "isolated"}),   # 갈색왜성 가지 입력은 None 으로 기록된다
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

# ── 갈색왜성 가지 (C19, 2026-09-04) — 순서: 소비자 → 가드 → 밴드 → 계산 → 크기 대조 맨 마지막 ──
print("\n갈색왜성 가지 — 가드가 먼저 서는가")
BD = dict(mass_mj=33.5, radius_rj=0.876, age_gyr=0.5, body_class="brown_dwarf",
          luminosity_lsun=2.14e-05, rotation_period_h=6.94,
          radius_rj_min=0.778, radius_rj_max=0.973, isolated=True)   # Luhman 16 A, DB 2026-09-04
GUARDS = [
    ("no luminosity", {**BD, "luminosity_lsun": None}, "luminosity_lsun"),
    ("no rotation", {**BD, "rotation_period_h": None}, "rotation_period_h"),
    ("no radius band", {**BD, "radius_rj_min": None, "radius_rj_max": None}, "radius_rj_min"),
    ("isolated undeclared", {**BD, "isolated": None}, "isolated"),
    ("irradiated (hot Jupiter route)", {**BD, "isolated": False}, "고립 갈색왜성에만"),
    ("slow rotator 5 d", {**BD, "rotation_period_h": 120.0}, "4 d"),
    ("stellar mass", {**BD, "mass_mj": 80.0}, "항성 영역"),
]
for label, kw, expect in GUARDS:
    res = dipole_field(**kw)
    ok = res.regime == OUT_OF_DOMAIN and expect in res.reason
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {label:<32} {res.regime}")
    if not ok:
        print(f"         reason={res.reason[:120]}")

print("\n갈색왜성 가지 — 밴드와 소비자 계약")
bd = dipole_field(**BD)
ok = bd.applicable and bd.regime == "brown_dwarf"
fails += 0 if ok else 1
print(f"  [{'PASS' if ok else 'FAIL'}] Luhman 16 A 가 가지를 탄다: {bd.regime}")
if bd.applicable:
    v = bd.values
    # 식 1 을 손으로: M 0.032 M☉, L 2.14e-5, R 0.09 R☉ → 4.8 (0.032·(2.14e-5)²/0.09⁷)^(1/6) kG
    by_hand_kg = 4.8 * (0.032 * (2.14e-5) ** 2 / 0.09 ** 7) ** (1 / 6)
    off = abs(v["b_dyn"] / 1e5 - by_hand_kg) / by_hand_kg
    ok = off < 0.01
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] B_dyn {v['b_dyn']/1e5:.3f} kG · 손계산 {by_hand_kg:.3f} kG ({off*100:.2f} %)")
    ok = v["b_dyn_min"] < v["b_dyn"] < v["b_dyn_max"] and v["b_eq_min"] < v["b_eq"] < v["b_eq_max"]
    fails += 0 if ok else 1
    width = (v["b_dyn_max"] - v["b_dyn_min"]) / v["b_dyn"]
    # 사전등록 ②: R 0.08–0.10 R☉ (±11 %) → R^(-7/6) 으로 ±13 % 안팎. 폭이 그 자릿수인가.
    ok2 = 0.15 < width < 0.40
    fails += 0 if ok2 else 1
    print(f"  [{'PASS' if ok and ok2 else 'FAIL'}] 밴드 {v['b_dyn_min']/1e5:.2f}–{v['b_dyn_max']/1e5:.2f} kG, 폭 {width*100:.0f} % (사전등록: 반지름 ±11 % → ~±13 %)")
    ok = abs(v["b_eq"] - v["b_dyn"] / (2 * 2 ** 0.5)) < 1e-6 * v["b_dyn"] and abs(v["b_pol"] - 2 * v["b_eq"]) < 1e-6 * v["b_pol"]
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] 소비자 계약: b_eq = B_dyn/(2√2) (깊이 감쇠 없음), b_pol = 2 b_eq → b_eq {v['b_eq']/1e5:.3f} kG")
    ok = all(k in bd.units for k in v) and "radius" in " ".join(bd.notes)
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] 단위 전부 · 밴드가 반지름에서 온다는 라벨")

    print("\n갈색왜성 가지 — 크기 대조 (맨 마지막, 사전등록 ①)")
    # RC10 §4.1 인쇄: 갈색왜성 장은 "a few kG and a hundred G" 사이. Christensen+ 2009: 1 Gyr·0.05 M☉·1500 K → ~0.1 T = 1 kG.
    b_kg = v["b_dyn"] / 1e5
    in_rc10 = 0.1 <= b_kg <= 5.0
    near_c09 = 1 / 3 <= b_kg / 1.0 <= 3
    fails += 0 if in_rc10 else 1
    print(f"  [{'PASS' if in_rc10 else 'FAIL'}] B_dyn {b_kg:.2f} kG 는 RC10 §4.1 의 인쇄 범위 0.1–5 kG 안인가")
    print(f"  [{'①a' if near_c09 else '①b'}] Christensen+ 2009 의 1 kG(1 Gyr · 0.05 M☉ · 1500 K) 대비 {b_kg:.2f}× — Luhman 16 은 더 가볍고 어두우니 1 kG 이하 언저리가 기대")
    b_res = dipole_field(**{**BD, "mass_mj": 28.6, "luminosity_lsun": 1.95e-05, "rotation_period_h": 4.87})
    print(f"  Luhman 16 B: B_dyn {b_res.values['b_dyn']/1e5:.2f} kG ({b_res.values['b_dyn_min']/1e5:.2f}–{b_res.values['b_dyn_max']/1e5:.2f}), b_eq {b_res.values['b_eq']/1e5:.3f} kG")

print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
