# 적분기 기록 인자(record)가 계산을 바꾸지 않는다는 시험 — 켬/끔 두 판의 구조 스칼라 비트 동일
"""`interior.integrate(..., record=[...])` records the profile and changes nothing else (pre-registration
v2-7, directing seat's condition 2). Every `Structure` slot is compared bit for bit between the two runs,
on configurations that take different branches of the stepping loop.

    python3 engine/test_interior_record.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import interior                        # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


def same(a, b) -> bool:
    """Bit-identical, recursing into tuples; NaN equals NaN only by its bits."""
    if isinstance(a, float) and isinstance(b, float):
        return a == b or (math.isnan(a) and math.isnan(b))
    if isinstance(a, (tuple, list)) and isinstance(b, (tuple, list)):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


ME = interior.EARTH_MASS_KG
CASES = [
    ("rocky, cold (Earth mass, core 0.325)", (360e9, ME, 0.325, 0.0, "fe_prem"), {}),
    ("rocky, adiabatic (t_center 5000 K, t_pot 1600 K)", (360e9, ME, 0.325, 0.0, "fe_prem"),
     {"t_center": 5000.0, "t_pot": 1600.0}),
    ("water-rich (Ganymede-like, imf 0.45)", (5e9, 0.0248 * ME, 0.1, 0.45, "fe_prem"), {}),
]
for name, args, kw in CASES:
    off = interior.integrate(*args, **kw)
    rec: list = []
    on = interior.integrate(*args, record=rec, **kw)
    diff = [s for s in interior.Structure.__slots__ if not same(getattr(off, s), getattr(on, s))]
    check(f"record on = off, every Structure slot — {name}", not diff, f"differs: {diff}" if diff else
          f"{len(interior.Structure.__slots__)} slots, {len(rec)} rows recorded")
    ok = bool(rec) and rec[-1][1] <= rec[0][1] and all(b[0] > a[0] for a, b in zip(rec, rec[1:]))
    check(f"the record runs outward, pressure falling to the surface — {name}", ok,
          f"r {rec[0][0] / 1e3:.1f} → {rec[-1][0] / 1e3:.1f} km, P {rec[0][1] / 1e9:.3g} → {rec[-1][1] / 1e9:.3g} GPa")
    check(f"the last row is the returned surface — {name}",
          rec[-1][0] == on.radius_m and rec[-1][2] == on.mass_kg)

print(f"  test_interior_record — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
