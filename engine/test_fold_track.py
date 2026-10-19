# C145 추적기의 NaN 부류 시험 — 유한↔NaN 은 부호 변화가 아님, 미끄러진 안쪽 근을 이어 따라감, NaN 구멍은 접힘이 아님, 닫히지 않는 쌍은 제외하지 않음
"""Checks for `fold_track`'s NaN class (c1 4b26cbcd, items (1)–(4)) on analytic functions; no solve.

    python3 engine/test_fold_track.py

The gain-cap V2 refusal (0.747935 Gyr) and the base R2 refusal (0.749176 Gyr) had one cause: the outer function was
NaN wherever the inner root had slid out of its ±w bracket, and NaN was read as a sign — a neighbour planted on a
finite→NaN edge, a fold declared across a NaN hole, and the live root excluded by the branch switch. Each item is
planted here with a mutant that reproduces it (red against the old rule)."""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fold_track as ft                 # noqa: E402
import thermal_stack as ts              # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


NAN = math.nan


def holed(x):
    """+ above 117 km, NaN on [114.7, 117], − below: a root at 119 (live) and a NaN hole, as the V2 outer function."""
    if 114.7e3 <= x <= 117e3:
        return NAN
    return 119e3 - x if x > 117e3 else -(x - 100e3) - 1.0


# (2) a finite↔NaN edge is never a sign change
check("(2) changes_sign — finite → NaN is no sign change", not ft.changes_sign(1.0, NAN) and not ft.changes_sign(NAN, -1.0))
check("(2) changes_sign — a finite sign change still is", ft.changes_sign(1.0, -1.0) and not ft.changes_sign(1.0, 2.0))
roots = ft.scan(holed, 110e3, 125e3, 300)
check("(2) scan — only the live root, none on the NaN edges", len(roots) == 1 and abs(roots[0] - 119e3) < 1.0,
      f"{[round(r) for r in roots]}")
lo, hi = ft.neighbours(holed, 119e3, 0.0, 200e3)
check("(2) neighbours — no neighbour planted on the finite→NaN edge", lo is None or lo < 114.7e3 - 1.0,
      f"lo {lo}")
old_rule = (1.0 > 0) != (NAN > 0)          # the old test: finite-positive → NaN read as a sign change
check("(2) the old rule's mutant is red here", old_rule)

# (3) a fold is judged on finite values only
r = ft.Root(119.416e3, dx=-560.0, lo=114.734e3, g=1.0)
ev = ft.lost(holed, r, "δ_u")
check("(3) lost — a NaN hole in the pair's interval is not a fold", ev.fold is False, str(ev))


def closed(x):
    """The pair met: h < 0 everywhere between them (a real fold)."""
    return -1.0 - 1e-6 * abs(x - 117e3)


check("(3) lost — a real fold (the hump gone, finite) is still a fold", ft.lost(closed, r, "δ_u").fold is True)

# (1) the inner root carried past its ±w bracket
slid = lambda x: 112e3 - x                 # noqa: E731 — the root moved 1.7 km, w at FLOOR (1 km)
b = ft.Root(110.3e3, dx=10.0)
check("(1) local_root alone loses it (the old NaN)", ft.local_root(slid, b, 0.0, 300e3) is None)
got = ft.carried_root(slid, b, 0.0, 300e3)
check("(1) carried_root follows it", got is not None and abs(got - 112e3) < 1e-3, f"{got}")
b2 = ft.Root(110.3e3, dx=10.0, hi=112.5e3)  # a known neighbour above at 112.5: the midpoint 111.4 bounds the search
got2 = ft.carried_root(slid, b2, 0.0, 300e3)
check("(1) carried_root never goes past the midpoint toward a known neighbour", got2 is None, f"{got2}")

# (4) a neighbour that is not a closing partner is not a fold's pair
far = ft.Root(119.416e3, dx=-560.0, lo=114.734e3, g=1.0)        # 4.7 km apart, scale max(4·0.56, 1) km = 2.24 km
near = ft.Root(119.416e3, dx=-560.0, lo=119.0e3, g=1.0)
check("(4) pair_closing — a neighbour 4.7 km off is not closing", not ft.pair_closing(far))
check("(4) pair_closing — a neighbour within twice the bracket scale is", ft.pair_closing(near))

# the T_c − T_b sign log (directing 10-19, the gain-cap decision)
rows = [{"t": 0.1, "t_c": 2000.0, "t_b": 1990.0}, {"t": 0.2, "t_c": 1990.0, "t_b": 1995.0},
        {"t": 0.3, "t_c": 1980.0, "t_b": 1979.5}]
lg = ts.tc_tb_sign(rows)
check("tc_tb_sign — sign changes and the least |T_c − T_b|", lg["sign_changes"] == 2 and lg["min_abs_k"] == 0.5
      and lg["min_at_gyr"] == 0.3, str(lg))

print(f"  test_fold_track — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
