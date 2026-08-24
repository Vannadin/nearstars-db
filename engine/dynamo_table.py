# 방법론 문서의 워크드 예제 표를 레시피에서 재생성하고, 문서에 실린 값과 대조
"""Regenerate the giant-dynamo worked-example table from the recipe.

The table in `docs/reference/planetary-dynamo-scaling.md` was hand-keyed. This
prints what the function actually returns for the same bodies and flags any
cell that disagrees, so the document stops being a second source of truth.

Body inputs are the curated Phase 2 anchors, transcribed here for the pilot;
wiring this to `db/systems/` is the next step, not this one.

    python3 engine/dynamo_table.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dynamo import dipole_field  # noqa: E402

# (라벨, M_J, R_J, age_Gyr, 문서에 실린 B_eq [µT], 문서에 실린 모멘트 [×Earth])
BODIES = [
    ("eps Eri b",    0.66, 1.05, 0.44, 660,  34000),
    ("GJ 896 A b",   2.26, 1.10, 0.50, 1980, 117000),
    ("eps Ind A b",  7.60, 1.12, 3.50, 3220, 201000),
]

print(f"{'body':<14}{'M_J':>6}{'R_J':>6}{'age':>6}"
      f"{'B_eq µT':>10}{'문서':>9}{'모멘트 ×E':>12}{'문서':>11}  판정")
print("-" * 82)

mismatch = 0
for label, m, r, age, doc_beq, doc_mom in BODIES:
    res = dipole_field(m, r, age)
    if not res.applicable:
        print(f"{label:<14} 적용 불가 — {res.reason[:50]}")
        continue

    beq = res.values["b_eq"]
    mom = res.values["dipole_moment"]

    beq_ok = doc_beq is not None and abs(beq - doc_beq) / doc_beq <= 0.03
    if doc_mom is None:
        verdict = "◀ 문서 셀 깨짐"
        mismatch += 1
        doc_mom_s = "—"
    else:
        mom_ok = abs(mom - doc_mom) / doc_mom <= 0.03
        verdict = "일치" if (beq_ok and mom_ok) else "◀ 불일치"
        mismatch += 0 if (beq_ok and mom_ok) else 1
        doc_mom_s = f"{doc_mom:,}"

    print(f"{label:<14}{m:>6.2f}{r:>6.2f}{age:>6.2f}"
          f"{beq:>10,.0f}{doc_beq:>9,}{mom:>12,.0f}{doc_mom_s:>11}  {verdict}")

print()
if mismatch:
    print(f"문서와 어긋난 행 {mismatch}개. 문서 표를 이 출력으로 교체해야 한다.")
else:
    print("문서 표와 전부 일치.")
sys.exit(1 if mismatch else 0)
