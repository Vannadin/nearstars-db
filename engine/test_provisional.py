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

    for f in fails:
        print(f"  [FAIL] {f}")
    if fails:
        return 1
    print(f"  [PASS] 임시값 가드레일 — ①넷째 단어(등급 아님) · ②값 단위 {len(REGISTRY)}개(중복 등록 거절) · "
          f"③emit 거절 · ④양쪽 기록 · ⑤레시피 도착 시 발화(오늘 증명) · "
          f"실물 인스턴스 0개 — C36 착지로 제거됨(대조표는 §7 에 남음)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
