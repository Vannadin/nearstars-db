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
# ⚠ **17 → 19, 브리프 178 C (2026-09-10).** 황 밴드의 양끝이 재질로 등록되면서 상이 둘 늘었다 —
# `fe_s_19GPa_c0.2065`(13 wt%)와 `fe_s_19GPa_c0.2901`(19 wt%). 이 수는 «새 상이 조용히 들어오지
# 못하게» 있는 것이고, 실제로 그 일을 했다: 게이트가 rc=1 로 멈추고 **어느 단계인지 이름을 찍었다**
# (169 E 의 표식이 처음으로 값을 한 자리다). 두 상의 표 칸은 비어 있고, 그건 «발표된 값이 없다» 로
# 합법이다 — 값을 지어 채우지 않는다.
row(len(emitted) == 19, f"방출 상 {len(emitted)}개: {' · '.join(pt.PHASE_KEYS)}")
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
