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

# B1 (r2 5cee6df2): the carried bracket holds three roots; the one carried is the middle (the predicted x + Δx)
X0 = 100e3
three = lambda x: (x - X0 - 1.7e3) * (x - X0 - 2.2e3) * (x - X0 - 2.7e3)  # noqa: E731
b3 = ft.Root(X0, dx=2.2e3, lo=X0 - 3e3)    # w = min(4·2.2, ½·3) km = 1.5 km: local_root fails, doubled to 3 km
check("B1 local_root alone finds none", ft.local_root(three, b3, 0.0, 300e3) is None)
carries = []
got3 = ft.carried_root(three, b3, 0.0, 300e3, log=carries)
check("B1 carried_root takes the root nearest x + Δx (the middle of three)", got3 is not None
      and abs(got3 - (X0 + 2.2e3)) < 1e-3, f"{got3}")
check("B1 the carry is logged with the roots seen", len(carries) == 1 and carries[0][3] == 3, str(carries))
first = ft.bisect(three, X0 - 1.5e3, X0 + 3e3, three(X0 - 1.5e3))   # the old rule: bisect the first sign change
check("B1 the «first sign change» mutant is red here (lands on another root)", abs(first - (X0 + 2.2e3)) > 100.0,
      f"{first}")
sm_ = ft.carry_summary(carries)
check("B1 carry_summary", sm_["n"] == 1 and sm_["multi_root"] == 1 and sm_["max_roots"] == 3
      and abs(sm_["max_carry_m"] - 2.2e3) < 1e-3, str(sm_))

# (4) a neighbour that is not a closing partner is not a fold's pair
far = ft.Root(119.416e3, dx=-560.0, lo=114.734e3, g=1.0)        # 4.7 km apart, scale max(4·0.56, 1) km = 2.24 km
near = ft.Root(119.416e3, dx=-560.0, lo=119.0e3, g=1.0)
check("(4) pair_closing — a neighbour 4.7 km off is not closing", not ft.pair_closing(far))
check("(4) pair_closing — a neighbour within twice the bracket scale is", ft.pair_closing(near))

# B2 (r2 5cee6df2): a rejected fold keeps the branch only if the full scan returns the continued root
from types import SimpleNamespace          # noqa: E402
from unittest import mock                  # noqa: E402
import samuel_run as sr                    # noqa: E402


def switch(mod, scan_root):
    """mod.switch_branch on stubs: the continuation holds (119.2, 110.1) km, the full scan returns `scan_root`."""
    u = ft.Root(119.416e3, dx=-560.0, lo=114.734e3, g=1.0)                # its neighbour 4.7 km off: not closing
    b = ft.Root(110.283e3, dx=-130.0)
    s = SimpleNamespace(r_p=3389.5e3, r_base=1830e3, e_star=3e5, opt={"a_rh": 2.21, "r_gas": 8.314},
                        track=ft.Track(u, b), fold_rejected=[], fold_events=[])
    ev = SimpleNamespace(equation="δ_u", tol_s=1.0)
    with mock.patch.object(mod.sm, "lid_base_temperature", lambda *a: 1000.0), \
            mock.patch.object(mod, "_layers_fn", lambda *a: None), \
            mock.patch.object(mod, "_continued", lambda *a: (119.2e3, 110.1e3)), \
            mock.patch.object(mod, "solve_boundary_layers" if mod is ts else "solve_layers",
                              lambda *a, **k: (*scan_root, None, None, None, 1900.0)), \
            mock.patch.object(mod, "track_at", lambda *a: "restarted"):
        try:
            mod.switch_branch(s, [2000.0, 1700.0, 100e3], 0.75, ev)
            return s, None
        except mod.sm.Refused as e:
            return s, str(e)


for mod in (ts, sr):
    name = mod.__name__
    s_, err = switch(mod, (119.25e3, 110.12e3))
    check(f"B2 {name}: the scan's root is the continued one → the branch is kept, the rejection recorded",
          err is None and s_.track == "restarted" and len(s_.fold_rejected) == 1 and s_.fold_events == [], str(err))
    s_, err = switch(mod, (131.0e3, 110.1e3))                             # another branch, 11.8 km off
    check(f"B2 {name}: another branch → refused by name", err is not None
          and err.startswith("fold rejected, but the continued root is gone at t = 0.750000 Gyr"), str(err))
    with mock.patch.object(ft, "FLOOR_M", 1e9):                          # the mutant: no distance check
        s_, err = switch(mod, (131.0e3, 110.1e3))
    check(f"B2 {name}: the no-check mutant is red here (takes the other branch silently)", err is None, str(err))

# the T_c − T_b sign log (directing 10-19, the gain-cap decision)
rows = [{"t": 0.1, "t_c": 2000.0, "t_b": 1990.0}, {"t": 0.2, "t_c": 1990.0, "t_b": 1995.0},
        {"t": 0.3, "t_c": 1980.0, "t_b": 1979.5}]
lg = ts.tc_tb_sign(rows)
check("tc_tb_sign — sign changes and the least |T_c − T_b|", lg["sign_changes"] == 2 and lg["min_abs_k"] == 0.5
      and lg["min_at_gyr"] == 0.3, str(lg))

# the pole (directing 10-20): a T_c − T_b sign change between accepted rows is a named refusal in both runners
for mod in (ts, sr):
    name = mod.__name__
    crossing = [{"t": 0.1, "t_c": 2000.0, "t_b": 1999.0}, {"t": 0.2, "t_c": 1990.0, "t_b": 1990.5}]
    try:
        mod.pole_check(crossing)
        err = None
    except mod.sm.Refused as e:
        err = str(e)
    check(f"pole {name}: a crossing refuses by name", err is not None and err.startswith(
        "T_c − T_b changed sign between t = 0.100000 and 0.200000 Gyr (+1.000 → -0.500 K)"), str(err))
    try:
        mod.pole_check([crossing[0], {"t": 0.2, "t_c": 1990.0, "t_b": 1989.0}])
        mod.pole_check([crossing[0], {"t": 0.2, "t_c": 1990.0, "t_b": None}])
        mod.pole_check(crossing[:1])
        ok = True
    except mod.sm.Refused:
        ok = False
    check(f"pole {name}: one sign, a row without T_b, a single row — no refusal", ok)
    lg = mod.tc_tb_sign(crossing)
    check(f"pole {name}: the mutant (the sign log alone) only counts it — silent", lg["sign_changes"] == 1, str(lg))

print(f"  test_fold_track — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
