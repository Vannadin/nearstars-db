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
import types
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

print("(6) a continuation without a state (note 3)")
orig = ValueError("표면온도 잔차가 뛴다 — 중심 온도 [3135.2, 3135.25] K 사이에서 0 을 건너뛴다 (C152).")
w0 = rf.fold_walk(plant(v_star=5.0), (0.05, 0.05 ** 3 - 0.05), TOL)                 # (b): the whole curve, no crossing
base = {"seed_bracket": (3135.2, 39.6e9, 3135.25, 39.3e9), "cpu": 1.0}
fa = interior._fold_failure(orig, dict(base, kind="no_seed", why="neither end of the bracket closes at SHOOT_TOL (W2)",
                                       walk=None), 1745.0)
check("(a) no walk: the original C152 refusal stands, first, with only the no-seed tail",
      str(fa).startswith(str(orig)) and str(fa).endswith("(core-tc-fold: no seed — neither end of the bracket closes at "
                                                         "SHOOT_TOL (W2))"), str(fa)[:80])
check("(b) the planted walk ran edge to edge without a crossing", w0.status == "done" and not w0.crossings
      and [e[0] for e in w0.leg_ends] == ["edge", "edge"])
fb = interior._fold_failure(orig, dict(base, kind="off_domain", why="no crossing", walk=w0), 1745.0)
check("(b) core_fold_off_domain heads it and carries the original refusal verbatim",
      str(fb).startswith(interior.FOLD_OFF_DOMAIN + " — ") and f"원래 거절: {orig}" in str(fb), str(fb)[:60])
wb = rf.fold_walk(plant(), (0.05, 0.05 ** 3 - 0.05), TOL, budget=5)
fc = interior._fold_failure(orig, dict(base, kind="budget", why="budget", walk=wb), 1745.0)
check("(c) core_fold_budget heads it and carries the original refusal verbatim",
      str(fc).startswith(interior.FOLD_BUDGET_ID + " — ") and f"원래 거절: {orig}" in str(fc), str(fc)[:60])


def renames(exc, att, t_pot):        # mutant «(a) renames»: no seed reported as core_fold_off_domain
    return interior._fold_refusal(interior.FOLD_OFF_DOMAIN, att, t_pot, f"; 원래 거절: {exc}")


check("control: the mutant «(a) renames» puts core_fold_off_domain first, so the (a) check above kills it",
      not str(renames(orig, dict(base, kind="no_seed", why="x", walk=None), 1745.0)).startswith(str(orig)))

print("(7) 68 B1: a step never steps over an S-turn (slope- and turn-limited steps, H_MAX 5e-3)")


def _sig(x):
    return 1.0 / (1.0 + math.exp(-x)) if x > -700.0 else 0.0


def s_feature(c):
    """dm = v − u; g a two-step S-feature of width 1e-3, crossings at c and c + 6e-3, excursion 0.05 between."""
    def F(u, v):
        if abs(u) > 1.0:
            raise rf.FoldOutside
        return v - u, 0.05 - 0.1 * (_sig((u - c) / 1e-3) - _sig((u - c - 6e-3) / 1e-3))
    return F


centres = [0.40 + 0.01 * i for i in range(21)]
found = [len(rf.fold_walk(s_feature(c), (0.0, 0.0), 1e-12, direction=1.0).crossings) for c in centres]
check("every one of 21 planted S-features is resolved: two crossings each", found == [2] * 21, f"{found}")
old = [len(rf.fold_walk(s_feature(c), (0.0, 0.0), 1e-12, direction=1.0, h_max=2e-2, dg_max=float("inf"),
                        turn_max=float("inf")).crossings) for c in centres]
check("control (mutant: 1b2fc17e's H_MAX 2e-2 without the limits) steps over some of them", min(old) == 0,
      f"missed {sum(1 for n in old if n == 0)} of 21")

print("(8) 68 B2: a PhaseGap in the F12 sweep ends as core_fold_states")
import eos  # noqa: E402

two = {"kind": "states", "states": [((0.0, math.log(39.6e9), math.log(3134.0), 0.0), []),
                                    ((0.1, math.log(39.2e9), math.log(3136.0), 0.0), [])],
       "seed_bracket": None, "cpu": 0.0}
saved = (interior._fold_attempt, interior._shoot_body)
interior._fold_attempt = lambda exc, a: two


def gap_body(*a, **k):
    raise eos.PhaseGap("fake_core", 51e9, "가짜 천장", temperature_k=None, too_cold=False)


interior._shoot_body = gap_body
try:
    try:
        interior._fold_continue(ValueError("x"), (6.4e23, 0.21, 0.0, "fe_prem"), {"potential_temperature": 1800.0})
        got = "answered"
    except ValueError as e:
        got = str(e)
    except eos.PhaseGap as e:
        got = f"PhaseGap escaped: {e}"
finally:
    interior._fold_attempt, interior._shoot_body = saved
check("the sweep's PhaseGap at T_pot + 10 K ends core_fold_states, not a foreign PhaseGap",
      got.startswith(interior.FOLD_STATES_ID + " — "), got[:90])

print("(9) 68 B3: R1 from converged curve points only; a failure keeps the state with a named note")
att = {"walk": types.SimpleNamespace(points=[(0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0)]), "e_ts": 2.0}
a_ = {"mass_kg": 1.0, "potential_temperature": 1800.0}


def st_at(u, v, mass=1.0):
    return types.SimpleNamespace(mass_kg=mass, t_surface=1800.0 * (1.0 + u), t_center=math.exp(v), p_center=math.exp(u),
                                 radius_m=3.4e6 * (1.0 + u), core_radius_m=1.7e6, p_cmb=19e9, t_cmb=2300.0, nmoi=0.36)


saved_i = interior._fold_integrate
try:
    interior._fold_integrate = lambda a, p, t: st_at(math.log(p), math.log(t))
    ok_band = interior._fold_band(att, (0.0, 0.0, 0.0, 0.0), a_)
    interior._fold_integrate = lambda a, p, t: st_at(math.log(p), math.log(t), mass=1.0 + 1e-3)   # never closes
    off_band = interior._fold_band(att, (0.0, 0.0, 0.0, 0.0), a_)

    def raising(a, p, t):
        raise ValueError("적분이 실패했다 — 가짜")
    interior._fold_integrate = raising
    raise_band = interior._fold_band(att, (0.0, 0.0, 0.0, 0.0), a_)
finally:
    interior._fold_integrate = saved_i
check("on-curve neighbours: b_y measured for every output", "not_measured" not in ok_band and len(ok_band) == 7,
      str(ok_band)[:80])
check("neighbours that never close: «not_measured», no band from off-curve points",
      "did not close" in off_band.get("not_measured", ""), str(off_band)[:80])
check("a neighbour that refuses: «not_measured», not a refusal", "refused" in raise_band.get("not_measured", ""),
      str(raise_band)[:80])
info = {"turning": [], "length": 0.0, "evals": 0, "cpu": 0.0, "crossings": 1, "states": 1, "band": raise_band,
        "e_ts": 2.0, "seed": (3134.0, 39.6e9), "extra": ""}
check("the note names the band failure", any("R1 not measured" in n for n in interior.fold_note(info)))

print("(10) 68 B4 and n3: the grade drops one step; the doubled solve restores its state when it raises")
check("one step down: analog → judgment, calibrated → analog", (interior._fold_grade_down("analog"),
      interior._fold_grade_down("calibrated")) == ("judgment", "analog"))
before = (interior.STEPS, interior._FOLD_DEPTH[0], interior.FOLD_DOUBLED[0], repr(interior._FAMILY_TRAIL))
saved_s = interior.shoot


def bad_shoot(**k):
    interior._FAMILY_TRAIL["trials"].append("planted")
    raise RuntimeError("planted")


interior.shoot = bad_shoot
try:
    try:
        interior._fold_doubled({})
    except RuntimeError:
        pass
finally:
    interior.shoot = saved_s
after = (interior.STEPS, interior._FOLD_DEPTH[0], interior.FOLD_DOUBLED[0], repr(interior._FAMILY_TRAIL))
check("STEPS, _FOLD_DEPTH, FOLD_DOUBLED and _FAMILY_TRAIL are restored after a raising doubled shoot", before == after)

print("(11) every walk limit is read at call time (directing 10-19, r2 B1)")
saved_l = (rf.FOLD_BUDGET, rf.FOLD_H0, rf.FOLD_H_MAX, rf.FOLD_DG_MAX, rf.FOLD_TURN_MAX)
try:
    rf.FOLD_BUDGET, rf.FOLD_H0 = 7, 1.25e-4
    rf.FOLD_H_MAX, rf.FOLD_DG_MAX, rf.FOLD_TURN_MAX = 6.25e-4, 1.25e-3, 0.025
    wp = rf.fold_walk(plant(), (0.05, 0.05 ** 3 - 0.05), TOL)
finally:
    rf.FOLD_BUDGET, rf.FOLD_H0, rf.FOLD_H_MAX, rf.FOLD_DG_MAX, rf.FOLD_TURN_MAX = saved_l
check("patched FOLD_BUDGET and FOLD_H0 take effect: the walk records them and stops at budget 7",
      wp.limits == {"budget": 7, "h0": 1.25e-4, "h_max": 6.25e-4, "dg_max": 1.25e-3, "turn_max": 0.025}
      and wp.status == "budget" and wp.attempts == 7, f"{wp.limits} {wp.status} {wp.attempts}")
check("unpatched, the walk records the shipped limits", rf.fold_walk(plant(), (0.05, 0.05 ** 3 - 0.05), TOL).limits
      == {"budget": rf.FOLD_BUDGET, "h0": rf.FOLD_H0, "h_max": rf.FOLD_H_MAX, "dg_max": rf.FOLD_DG_MAX,
          "turn_max": rf.FOLD_TURN_MAX})

print("(12) 68 R1: the guards themselves — a feature H_MAX 5e-3 alone steps over")


def s_narrow(c):
    """width 3e-4, crossings 2e-3 apart: H_MAX 5e-3 without the guards resolves 22/41 positions; each guard alone off
    loses some (post-check off 40/41, predictive cap off 37/41, measured at ba7bcf70)."""
    def F(u, v):
        if abs(u) > 1.0:
            raise rf.FoldOutside
        return v - u, 0.05 - 0.1 * (_sig((u - c) / 3e-4) - _sig((u - c - 2e-3) / 3e-4))
    return F


cs41 = [0.40 + 0.0037 * i for i in range(41)]
got41 = sum(1 for c in cs41 if len(rf.fold_walk(s_narrow(c), (0.0, 0.0), 1e-12, direction=1.0).crossings) == 2)
check("the guards resolve all 41 narrow S-features", got41 == 41, f"{got41}/41")
off41 = sum(1 for c in cs41 if len(rf.fold_walk(s_narrow(c), (0.0, 0.0), 1e-12, direction=1.0, dg_max=float("inf"),
                                                turn_max=float("inf")).crossings) == 2)
check("control (guards off, H_MAX 5e-3 kept) misses some of them", off41 < 41, f"{off41}/41")

print("(13) 68 R2: solve's grade goes through _answer_grade")
check("_answer_grade: a fold answer one step down, any other unchanged",
      (interior._answer_grade("analog", {}), interior._answer_grade("analog", None),
       interior._answer_grade("calibrated", {"band": {}})) == ("judgment", "analog", "analog"))
import inspect  # noqa: E402
src_solve = inspect.getsource(interior.solve)
check("solve's Result grade is _answer_grade(grade0, fold_info) (the wiring, not only the helper)",
      "grade=_answer_grade(grade0, fold_info)" in src_solve)

print(f"test_core_fold: {'모두 통과' if not fails else f'FAIL {fails}'}")
sys.exit(1 if fails else 0)
