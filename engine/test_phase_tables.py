# 상 곁표 계약 테스트 — 키 집합은 eos 가 내는 상과 같고, 채운 칸은 등급·출처, authored 는 두 표지, 빈 칸 수를 출력한다
"""Contract of the phase side tables (engine/phase-tables-context-notes.md ①–⑨).

    python3 engine/test_phase_tables.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phase_tables as pt              # noqa: E402
from payload import AUTHORED_MARKERS, GRADES  # noqa: E402

fails = 0


def row(ok, text):
    global fails
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


print("키 — 표의 키 집합은 eos 가 실제로 내는 상과 같다 (상을 추가하면 행이 없어 실패, 안 내는 상의 행도 실패)")
emitted = set(pt.emitted_phase_keys())
row(len(emitted) == 17, f"방출 상 {len(emitted)}개: {' · '.join(pt.PHASE_KEYS)}")
for axis, table in pt.AXES.items():
    row(set(table) == emitted, f"{axis}: 키 집합 == 방출 상 ({len(table)})")

print("\n칸 — 채운 칸은 등급·출처, authored 는 두 표지; 빈 칸은 합법")
for axis, table in pt.AXES.items():
    for k, c in table.items():
        if c is None:
            continue
        ok = c.grade in GRADES and bool(c.source) and (c.grade != "authored" or all(m in c.note for m in AUTHORED_MARKERS))
        row(ok, f"{axis}.{k}: {c.value} {c.unit} · {c.grade} · {c.source[:60]}…")
try:
    pt.Cell(value=1.0, unit="—", grade="authored", source="x", note="gap: y"); row(False, "authored without consistent-with accepted")
except ValueError:
    row(True, "authored 셀에 consistent-with 없음 → 거절")

print("\n빈 칸 — 소비자가 그 상에서 거절한다 (정상 경로)")
row(pt.lookup("conductivity", "ice_vii") is None, "conductivity.ice_vii → None")
try:
    pt.lookup("conductivity", "not_a_phase"); row(False, "unknown phase accepted")
except KeyError:
    row(True, "엔진이 안 내는 상 → KeyError")

print("\n교차검사 — fe_prem σ 1.36e6 S/m ↔ λ_m = 1/(μ₀σ)")
lam = pt.magnetic_diffusivity("fe_prem")
row(lam is not None and abs(lam - 0.585) < 0.01, f"λ_m {lam:.3f} m²/s (RM22 prints 1.32 — paper-defects row 14, kept as a printed inconsistency)")

print("\n채움 현황 — 게이트 출력 (다음 조사 대상 목록)")
for axis, s in pt.summary().items():
    print(f"  {axis:13s} filled {s['filled']:2d} / {s['total']:2d} · authored {s['authored']}")
    row(s["authored"] == 0, f"{axis}: authored 0 (2026-09-04 — 빈 칸을 authored 로 채우지 않았다)")

print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
