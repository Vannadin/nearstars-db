# 페이로드 등급 계약 테스트 — authored 등급은 두 표지(gap:, consistent-with:) 없이는 생성되지 않는다
"""Grade-vocabulary contract of `payload.Result` (engine/AUTHORED-VALUES-POLICY.md, 2026-09-04).

    python3 engine/test_payload.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from payload import GRADES, AUTHORED_MARKERS, Result  # noqa: E402

fails = 0


def row(ok, text):
    global fails
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


def make(grade, notes=()):
    return Result(recipe="test", version="0", regime="test", reason="test", grade=grade,
                  inputs={}, values={"x": 1.0}, units={"x": "—"}, notes=notes)


print("등급 어휘 — chain.yaml 의 grades 와 같은 다섯")
row(GRADES == ("measured", "calibrated", "analog", "judgment", "authored"), f"GRADES = {GRADES}")
row(AUTHORED_MARKERS == ("gap:", "consistent-with:"), f"표지 = {AUTHORED_MARKERS}")

print("\nauthored — 두 표지가 다 있어야 생성된다")
ok = True
try:
    make("authored", ("gap: no held source gives it (cache + ADS searched 2026-09-04)",
                      "consistent-with: sits inside the published bound X"))
except ValueError:
    ok = False
row(ok, "gap: + consistent-with: → 생성")
for label, notes in (("표지 없음", ()), ("gap 만", ("gap: …",)), ("consistent-with 만", ("consistent-with: …",))):
    try:
        make("authored", notes); ok = False
    except ValueError as e:
        ok = "authored" in str(e)
    row(ok, f"{label} → 거절")

print("\njudgment 는 그대로 — 표지 없이 생성된다 (발표된 선택지 사이의 판단)")
ok = True
try:
    make("judgment")
except ValueError:
    ok = False
row(ok, "judgment, notes 없음 → 생성")
try:
    make("invented"); ok = False
except ValueError:
    ok = True
row(ok, "어휘 밖 등급 → 거절")

print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
