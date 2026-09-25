# 새 입력 칸의 세 칸 검사(grade · source · counter_evidence_searched) 시험 — prereg-grade-vocabulary §3
"""`payload.check_provenance` 와 `run.load_body` 의 새 칸 목록(`NEW_PROVENANCE_FIELDS`).

    python3 engine/test_provenance.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import payload                         # noqa: E402
import run                             # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


def refused(entry) -> str:
    try:
        payload.check_provenance("probe_field", entry)
    except ValueError as exc:
        return str(exc)
    return ""


good = {"value": 1.0, "grade": "derived", "source": "x", "counter_evidence_searched": "cache, 2026-09-25"}
check("세 칸 다 있고 입력 등급이면 통과", refused(good) == "")
for name, entry, needle in (
        ("목록 밖 낱말", dict(good, grade="guessed"), "grade"),
        ("결과 전용 calibrated", dict(good, grade="calibrated"), "calibrated"),
        ("옛 낱말 owner-override", dict(good, grade="owner-override"), "owner-override"),
        ("빈 source", dict(good, source=""), "source"),
        ("counter_evidence_searched 없음", {k: v for k, v in good.items() if k != "counter_evidence_searched"},
         "counter_evidence_searched"),
        ("블록이 아님", 1.0, "블록")):
    why = refused(entry)
    check(f"{name} → 칸 이름 대고 거절", bool(why) and needle in why and "probe_field" in why, why[:90])

check("INPUT_GRADES 에 calibrated 없음 · 나머지 여덟", payload.INPUT_GRADES == (
    "measured", "literature", "analog", "derived", "judgment", "declared", "inherited", "authored"))

calls = 0
orig = payload.check_provenance


def counting(name, entry):
    global calls
    calls += 1
    orig(name, entry)


payload.check_provenance = counting
bodies = sorted((Path(__file__).resolve().parent / "bodies").glob("*.yaml"))
for path in bodies:
    run.load_body(path)
payload.check_provenance = orig
print(f"  [보고] 몸 파일 {len(bodies)} 개 로드 — 실패는 위에서 예외로 멈춤")
print(f"  [보고] 새 칸 목록 {payload.NEW_PROVENANCE_FIELDS!r} · check_provenance 호출 {calls} 회")
import yaml                            # noqa: E402
declared = sum(1 for path in bodies for name in payload.NEW_PROVENANCE_FIELDS
               if name in ((yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("inputs") or {}))
check("새 칸을 선언한 수만큼 검사 (9f #34)", calls == declared, f"선언 {declared} · 호출 {calls}")

print(f"  test_provenance — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
