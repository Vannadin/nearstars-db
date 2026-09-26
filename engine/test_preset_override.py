# 조성 프리셋 칸이 선언에 덮일 때 결과에 이름 댄 한 줄이 서는지 · 안 서야 할 곳엔 안 서는지 묻는 시험 (C121)
"""Checks for C121 (pre-registration `prereg-preset-override-note.md`, frozen e198d4ca).

    python3 engine/test_preset_override.py

PO-줄    — an override line appears once per overridden preset field when a composition is named, and never when
           the declaration equals the preset, when no composition is passed, or inside an inversion.
PO-안쪽   — the inner `solve` calls an inversion makes (trial fractions, no composition named) carry no override line.
PO-반지름 — with a declared radius, the note says it is a comparison, not a solver input.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import interior                        # noqa: E402

fails = 0
MARK = "을 선언"          # the override line's verb phrase («… 0.50 을 선언 0 이 덮음»)


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


def lines(res) -> list[str]:
    return [n for n in (res.notes or []) if "덮음" in n and "composition_intent" in n]


M_SMALL = 0.0015          # a small rocky body — quick to solve; the notes are what is asked, not the numbers

r = interior.solve(M_SMALL, composition="water", ice_mass_fraction=0.0)
got = lines(r)
check("PO-줄 ① water + ice 0.0 → one line naming ice_mass_fraction, preset 0.5, declared 0",
      r.applicable and len(got) == 1 and "ice_mass_fraction" in got[0] and "0.5" in got[0] and "선언 0 " in got[0],
      got[0] if got else "none")
r = interior.solve(M_SMALL, composition="water", ice_mass_fraction=0.50)
check("PO-줄 ② declaration equal to the preset → no line", r.applicable and not lines(r))
r = interior.solve(M_SMALL, core_mass_fraction=0.3)
check("PO-줄 ③/⑤ no composition passed, only a fraction → no line", r.applicable and not lines(r))
r = interior.solve(M_SMALL, composition="earth_like", core_mass_fraction=0.4)
got = lines(r)
check("PO-줄 ④ earth_like + cmf 0.4 → one core_mass_fraction line",
      r.applicable and len(got) == 1 and "core_mass_fraction" in got[0], got[0] if got else "none")
r = interior.solve(M_SMALL, composition="water", core_mass_fraction=0.2, ice_mass_fraction=0.3)
check("PO-줄 ④ two fields overridden → two lines", r.applicable and len(lines(r)) == 2, str(len(lines(r))))
r = interior.solve(M_SMALL, composition=None, core_mass_fraction=0.3)
check("an explicit None is still refused by name, as before", not r.applicable and "'None'" in (r.reason or ""),
      (r.reason or "")[:80])

# PO-반지름
r = interior.solve(M_SMALL, composition="earth_like", radius_earth=0.12)
check("PO-반지름 — the declared-radius note says it is a comparison, not a solver input",
      r.applicable and any("대조값" in n and "선언된 반지름" in n for n in r.notes))

# PO-안쪽 · PO-줄 ⑥ — an inversion: its inner solve calls and its own result carry no override line
inner: list = []
plain = interior.solve


def spy(*a, **k):
    res = plain(*a, **k)
    inner.append(res)
    return res


interior.solve = spy
try:
    inv = interior.infer_composition(M_SMALL, 0.12, ice_allowed=False)
finally:
    interior.solve = plain
n_inner = sum(len(lines(x)) for x in inner if getattr(x, "notes", None))
check("PO-안쪽 — the inversion's inner solve calls carry no override line", n_inner == 0,
      f"{len(inner)} inner calls · {n_inner} lines")
check("PO-줄 ⑥ — the inversion's own result carries no override line", not lines(inv))

print(f"\n  test_preset_override — {'모두 통과' if fails == 0 else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
