# 핵 사격 접힘 이어 걷기 시험 — 심은 접힘 곡선에서 교차·꺾임·상태 묶기·F12 고르기가 등록 규칙대로인가 (rootfind 순수 함수)
"""python3 engine/test_core_fold.py — core-tc-fold registration (frozen fbbce52e) §2 items 2–4, 8, 10 and §4 A4, on
planted callables (no engine solve).

Plant: dm(u, v) = u³ − u − v, so {dm = 0} is v = u³ − u — at fixed v it has up to three zeros in u (the fold of §1),
and v(s) turns at u = ±1/√3 (v = ∓0.3849). g(u, v) = v − v*: with v* = 0 the walk crosses g = 0 at u = −1, 0, 1, and
between neighbouring crossings |g| reaches 0.3849 (the excursion). Domain |u| ≤ 1.5 (FoldOutside outside).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rootfind as rf  # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    fails += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


def plant(v_star=0.0, edge=1.5):
    def F(u, v):
        if abs(u) > edge:
            raise rf.FoldOutside
        return u ** 3 - u - v, v - v_star
    return F


TOL = 1e-10
U_TURN = 1.0 / math.sqrt(3.0)
V_TURN = U_TURN ** 3 - U_TURN

print("(1) the walk on the planted fold")
w = rf.fold_walk(plant(), (0.05, 0.05 ** 3 - 0.05 + 1e-3), TOL, direction=-1.0)
us = sorted(c[1] for c in w.crossings)
check("ends at both domain edges, within budget", w.status == "done" and [e[0] for e in w.leg_ends] == ["edge", "edge"],
      f"{w.status} {w.leg_ends}")
check("every point is on {dm = 0} to the corrector tolerance", all(abs(p[3]) <= TOL for p in w.points))
check("three crossings, at u = −1, 0, 1", len(us) == 3 and all(abs(a - b) < 1e-6 for a, b in zip(us, (-1.0, 0.0, 1.0))),
      f"{[round(x, 9) for x in us]}")
check("crossings have |g| ≤ 1e-9", all(abs(c[3]) <= 1e-9 for c in w.crossings))
tu = sorted(t[1] for t in w.turning)
check("two turning points of v(s), near u = ∓1/√3", len(tu) == 2 and all(abs(abs(x) - U_TURN) < 2e-2 for x in tu),
      f"{[round(x, 4) for x in tu]}")
s_order = [c[0] for c in sorted(w.crossings, key=lambda c: c[1])]
check("one arc-length coordinate through the seed (s increases with u here)", s_order == sorted(s_order))
check("the first leg went toward the shallow end (smaller u)", w.leg_ends[0][1] < 0.0 < w.leg_ends[1][1])

print("(2) states by the excursion test (item 8)")
e_hi = abs(V_TURN) * 1.01
st1 = rf.fold_states(w, e_hi)
check("excursion ≤ e_g: one state, reported at the crossing nearest the seed (u = 0)",
      len(st1) == 1 and abs(st1[0][0][1]) < 1e-6 and len(st1[0][1]) == 3, f"{len(st1)}")
st3 = rf.fold_states(w, abs(V_TURN) * 0.99)
check("excursion > e_g: three states", len(st3) == 3)
# the mutant «stop at the first crossing toward the shallow end»: a walk cut at its first crossing sees one state
cut = rf.FoldWalk()
first = min((c for c in w.crossings if c[0] < 0.0), key=lambda c: -c[0])
cut.points = [p for p in w.points if first[0] <= p[0] <= 0.0]
cut.crossings = [first]
check("control (mutant: stop at the first crossing toward the shallow end) — one state, so A4 would fail",
      len(rf.fold_states(cut, abs(V_TURN) * 0.99)) == 1)

print("(3) seed off the curve, budget, outside")
wb = rf.fold_walk(plant(), (0.05, 0.0), TOL, budget=5)
check("budget: status «budget» with the attempts at the budget", wb.status == "budget" and wb.attempts == 5,
      f"{wb.status} {wb.attempts}")


def outside(u, v):
    raise rf.FoldOutside


check("a seed outside the domain: status «seed»", rf.fold_walk(outside, (0.0, 0.0), TOL).status == "seed")

print("(4) F12 on the core chain (item 10)")


def _read_solve():
    """solver/solve.py's pair, read from its source (the engine does not import the solver)."""
    import re
    s = (Path(__file__).resolve().parent.parent / "solver" / "solve.py").read_text(encoding="utf-8")
    return (float(re.search(r"^WARM_STEP_K = ([\d.]+)$", s, re.M).group(1)),
            int(re.search(r"^WARM_STEPS_MAX = (\d+)$", s, re.M).group(1)))


check("WARM_STEP_K and WARM_STEPS_MAX equal solver/solve.py's", (rf.WARM_STEP_K, rf.WARM_STEPS_MAX) == _read_solve(),
      f"{(rf.WARM_STEP_K, rf.WARM_STEPS_MAX)} vs {_read_solve()}")


def plant_states(n_two: int, persist=False):
    """Two states (T_c 3000 and 3100) up to T_pot t0 + n_two·10, then one state near 3010 (or two forever)."""
    def states_at(t):
        k = round((t - 1800.0) / 10.0)
        if persist or k <= n_two:
            return "states", (3000.0 + k, 3100.0 + k)
        return "states", (3010.0 + k,)
    return states_at


tc, trace, why = rf.core_warm_choice(plant_states(3), 1800.0, (3000.0, 3100.0))
check("one state at a warmer T_pot: the walked-back choice is the nearer branch (3000)", tc == 3000.0 and why is None,
      f"{tc} {why} steps {len(trace) - 1}")
tc, trace, why = rf.core_warm_choice(plant_states(0, persist=True), 1800.0, (3000.0, 3100.0))
check("two states over 20 steps: undecided (core_fold_states)", tc is None and "persist over 20" in why and len(trace) == 21)
tc, trace, why = rf.core_warm_choice(lambda t: ("other", "core_fold_budget"), 1800.0, (3000.0, 3100.0))
check("the sweep meets a non-state: undecided, naming it", tc is None and "core_fold_budget" in why)
# 998c37d2's hint perturbation on the first plant: the choice does not depend on which state the caller lists first
tc2, _t, _w = rf.core_warm_choice(plant_states(3), 1800.0, (3100.0, 3000.0))
check("hint perturbation (states listed in the other order): the same F12 outcome", tc2 == 3000.0)

print("(5) the trigger predicate (note 1: any C152 refusal holding a sign-changing bracket, any width)")
import interior  # noqa: E402


def planted(site, y_lo, y_hi, t_lo=3117.2, t_hi=3136.82, p=39.3e9):
    return interior._fold_tagged(ValueError("planted"), (t_lo, p, y_lo, t_hi, p, y_hi), site)


check("a budget end with a straddling 19.6 K bracket triggers (1735.449's shape)",
      interior.fold_trigger(planted("budget", -1e-2, 6e-3)))
check("a zero-width straddling bracket triggers (frozen (b), the 1990 K stall)",
      interior.fold_trigger(planted("stall", -1e-3, 1e-3, 3135.15, 3135.15)))
check("the jump site triggers (frozen (a))", interior.fold_trigger(planted("jump", -9e-3, 5.8e-2, 3135.2, 3135.25)))
check("a budget end with a same-sign bracket does not trigger", not interior.fold_trigger(planted("budget", 1e-2, 6e-3)))
check("a zero-width bracket without a sign change does not trigger",
      not interior.fold_trigger(planted("stall", 1e-3, 2e-3, 3135.15, 3135.15)))
check("an untagged ValueError does not trigger", not interior.fold_trigger(ValueError("x")))
check("a bracket end without its P_c does not trigger", not interior.fold_trigger(
    interior._fold_tagged(ValueError("x"), (3117.2, None, -1e-2, 3136.82, 39.3e9, 6e-3), "budget")))


def width_zero_only(exc):          # mutant: frozen (b) read literally, «width == 0 only» (68 note-1 condition 2)
    sd = getattr(exc, "fold_seed", None)
    return getattr(exc, "fold_site", None) == "jump" or (sd is not None and sd[0] == sd[3] and sd[2] * sd[5] < 0.0)


check("control: the mutant «width == 0 only» misses the 19.6 K straddle (so the plant above kills it)",
      not width_zero_only(planted("budget", -1e-2, 6e-3)))
check("the switch defaults on", interior.FOLD_CONTINUATION is True)

print(f"test_core_fold: {'모두 통과' if not fails else f'FAIL {fails}'}")
sys.exit(1 if fails else 0)
