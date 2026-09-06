# 임시값 가드레일 다섯 자기검증 — 특히 ⑤ 가 "언젠가" 가 아니라 지금 발화하는지
"""Hold the provisional-value pattern to its five guardrails.

    python3 engine/test_provisional.py

⚠ The interesting one is **⑤**. Its promise is "the gate fails the moment the real recipe lands", and
that day is tomorrow, not today — so left alone it would be code that first executes when it matters
most, which is how three checks were written correctly and found wrong when finally run. Here it is
handed a set containing the node's name and required to fire. The claim is tested on the day it is
made, against the case it is supposed to **fail**, not the case it is supposed to pass.

The wiring test and the answer test are named apart, per the owner's rule: running on a real body
means the plumbing carries a value, never that the value is right. Nothing here claims a body is or
is not tidally locked.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bands import Band  # noqa: E402
from payload import GRADES  # noqa: E402
from provisional import (PROVISIONAL, Placeholder, REGISTRY, recipe_arrived,  # noqa: E402
                         refuse_emit, register, standing_on, supply)
from state import BodyState  # noqa: E402


def main() -> int:
    fails: list[str] = []

    def ok(cond, msg):
        if not cond:
            fails.append(msg)

    # ① its own word, colliding with nothing
    picks = {Band(1.0, 0.9, 1.1, "d", "measured").pick,
             Band(1.0, 0.9, 1.1, "d", "measured", value_origin="printed").pick,
             Band(None, 0.9, 1.1, "d", "measured").pick}
    ok(PROVISIONAL not in picks, f"1: 'provisional' must not collide with bands.py's words {picks}")
    ok(PROVISIONAL not in GRADES,
       "1: a placeholder is not a grade — grades say how well a value is known, and this is not a value yet")
    probe = Placeholder(node="not_a_node", output="x", value=1, why="a synthetic stand-in: the real "
                        "one, tidal_locking.locked, was deleted when C36 landed on 2026-09-06")
    register(probe)
    ok(probe.pick == PROVISIONAL, "1: a placeholder reports its own word")
    try:
        Placeholder(node="x", output="y", value=1, why="")
        fails.append("1: a placeholder with no stated debt is a silent default and must be refused")
    except ValueError:
        pass

    # ② counted by value, not by node
    ok(len(REGISTRY) == 1, f"2: the count is by value; got {len(REGISTRY)}")
    try:
        register(Placeholder(node="not_a_node", output="x", value=2, why="again"))
        fails.append("2: two stand-ins for one value must be refused")
    except ValueError:
        pass

    # ③ may not be emitted, ④ and both ends know
    st = BodyState(name="probe", kind="planet", inputs={"mass_earth": 1.0})
    ok(refuse_emit(st) is None, "3: a clean state emits freely")
    supply(st, probe)
    why = refuse_emit(st)
    ok(why is not None and "x" in why, f"3: a state standing on a placeholder must refuse emit: {why}")
    ok(standing_on(st, "x", "mass_earth") == ("x",),
       "4: a consumer must be able to ask which of its inputs are provisional")
    ok(st["x"] == 1, "4: and the chain still reads the value, or nothing downstream runs")

    # ⑤ fires today, against the case it must fail
    ok(recipe_arrived(set()) == [], "5: with no recipe registered, nothing fires")
    fired = recipe_arrived({"not_a_node"})
    ok(len(fired) == 1 and "not_a_node" in fired[0] and "recipe" in fired[0],
       f"5: the moment that node has a recipe this must fire, got {fired}")
    ok(recipe_arrived({"dynamo_rocky"}) == [],
       "5: and it must not fire on some other node acquiring a recipe")

    # ⚠ 5b. and it must be pointed at the LIVE registry, or the promise is untested where it matters.
    # Handing it a made-up set proves the function works; it does not make the gate red on the day a
    # recipe actually lands. This is the check that does.
    import registry  # noqa: E402
    registry.load_all()
    live = recipe_arrived(registry.registered())
    ok(live == [],
       "5b: a placeholder is standing for a node that now has a registered recipe — "
       + " ".join(live))

    # ⚠ The wiring tests that stood here are gone with the placeholder. What they measured is kept
    # as the control table in `regime-gate-context-notes.md` §7, which is the other half of C36's A/B:
    # the wiring was frozen and stipulated first, so when the physics landed only the answer moved.

    # 6. the first real instance: `orbit_elements.eccentricity` (owner decision (b), 2026-09-06).
    # ⚠ It is tested here rather than only in the recipe's own file because the thing worth pinning is
    # not what tidal_locking does with it — it is that ONE value classifies EVERY body. No body
    # supplies its own eccentricity, so unlike ω₀ (which is at least multiplied by per-body data)
    # this placeholder is not a default that data can outvote. If that ever stops being true, this
    # test should be the thing that notices.
    import tidal_locking  # noqa: E402
    ph = REGISTRY[("orbit_elements", "eccentricity")]
    ok(ph.value == 0.10, f"6: the placeholder's value lives in one place; got {ph.value}")
    roster = [("Pandora", 0.6447, 0.8984, 252393.0, 120.0),
              ("Dante", 1.552e21 / tidal_locking.M_EARTH_KG, 521e3 / tidal_locking.R_EARTH_M,
               110000.0, 120.0),
              ("Hades", 5.0e21 / tidal_locking.M_EARTH_KG, 750e3 / tidal_locking.R_EARTH_M,
               148000.0, 120.0)]
    states = {tidal_locking.solve(m, r, a, mp, 5.3).values["rotation_state"] for _n, m, r, a, mp in roster}
    ok(len(states) == 1 and states.pop().startswith("unclassified"),
       "6: one provisional decides all three bodies identically, and the state it decides is the one "
       "that declines to classify — that uniformity IS the finding, not a side effect")
    res = tidal_locking.solve(*roster[0][1:], 5.3)
    ok(res.values.get("eccentricity_pick") == PROVISIONAL,
       "6: a result standing on the placeholder must say so in its own values (guardrail 4)")
    ok(tidal_locking.solve(*roster[0][1:], 5.3, 0.0).values.get("eccentricity_pick") is None,
       "6: and a body that supplies its own eccentricity must carry no such mark")

    # ⚠ 6b. the value is not neutral, and the note must not claim it is. What was chosen is the
    # INTERVAL (0.055, 0.206) — §4's unprinted gap — not the number: every value in it gives the same
    # answer, and 0.10 has no standing of its own. The input still asserts "this body's eccentricity
    # is middling", exactly as 0.0 asserts "circular".
    for alt in (0.06, 0.15, 0.205):
        ok(tidal_locking.rotation_state(alt, False) == tidal_locking.rotation_state(0.10, False),
           f"6b: any value in the gap gives the same state, so the number is not the choice; {alt}")
    ok(tidal_locking.rotation_state(0.0, False) != tidal_locking.rotation_state(0.10, False),
       "6b: and it is not the same as zero — the placeholder is a different assertion, not the absence "
       "of one")
    # ⚠ 6c. the interval deliberately stops below 0.206. Between our pseudo threshold and Barnes's CPL
    # threshold √(1/19) = 0.2294 there is an 11 % gap where this engine says pseudo-synchronous and
    # the CPL model says 1:1 — C38's seam, still live. A placeholder must not be parked inside it.
    import math  # noqa: E402
    cpl = math.sqrt(1.0 / 19.0)
    ok(tidal_locking.E_MERCURY_RESONANT < ph.value < cpl or ph.value < tidal_locking.E_MERCURY_RESONANT,
       "6c: the placeholder must not sit between our threshold and the CPL threshold")
    ok(ph.value < tidal_locking.E_MERCURY_RESONANT,
       f"6c: and specifically below ours, {ph.value} vs {tidal_locking.E_MERCURY_RESONANT}")

    for f in fails:
        print(f"  [FAIL] {f}")
    if fails:
        return 1
    print(f"  [PASS] 임시값 가드레일 — ①넷째 단어(등급 아님) · ②값 단위 {len(REGISTRY)}개(중복 등록 거절) · "
          f"③emit 거절 · ④양쪽 기록 · ⑤레시피 도착 시 발화(오늘 증명) · "
          f"실물 인스턴스 1개(orbit_elements.eccentricity) — ⚠ 값 하나가 로스터 전원을 동일하게 "
          f"분류한다(천체별 데이터가 뒤집지 못함) · 고른 것은 수가 아니라 구간 · 우리 문턱과 CPL "
          f"문턱 사이 틈은 피함")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
