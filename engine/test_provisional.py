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
import dynamo_rocky as dr  # noqa: E402
from bands import Band  # noqa: E402
from payload import GRADES  # noqa: E402
from provisional import (PROVISIONAL, Placeholder, REGISTRY, recipe_arrived,  # noqa: E402
                         refuse_emit, register, standing_on, supply)
from state import BodyState  # noqa: E402
from tidal_locking_provisional import LOCKED  # noqa: E402


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
    ok(LOCKED.pick == PROVISIONAL, "1: a placeholder reports its own word")
    try:
        Placeholder(node="x", output="y", value=1, why="")
        fails.append("1: a placeholder with no stated debt is a silent default and must be refused")
    except ValueError:
        pass

    # ② counted by value, not by node
    ok(len(REGISTRY) == 1, f"2: one value stands in today, got {len(REGISTRY)}")
    ok(("tidal_locking", "locked") in REGISTRY,
       "2: the count is keyed by (node, output) — tidal_locking owes three outputs and one is stood in")
    try:
        register(Placeholder(node="tidal_locking", output="locked", value=True, why="again"))
        fails.append("2: two stand-ins for one value must be refused")
    except ValueError:
        pass

    # ③ may not be emitted, ④ and both ends know
    st = BodyState(name="probe", kind="planet", inputs={"mass_earth": 1.0})
    ok(refuse_emit(st) is None, "3: a clean state emits freely")
    supply(st, LOCKED)
    why = refuse_emit(st)
    ok(why is not None and "locked" in why, f"3: a state standing on a placeholder must refuse emit: {why}")
    ok(standing_on(st, "locked", "mass_earth") == ("locked",),
       "4: a consumer must be able to ask which of its inputs are provisional")
    ok(st["locked"] is False, "4: and the chain still reads the value, or nothing downstream runs")

    # ⑤ fires today, against the case it must fail
    ok(recipe_arrived(set()) == [], "5: with no recipe registered, nothing fires")
    fired = recipe_arrived({"tidal_locking"})
    ok(len(fired) == 1 and "tidal_locking" in fired[0] and "recipe" in fired[0],
       f"5: the moment tidal_locking has a recipe this must fire, got {fired}")
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

    # wiring: the placeholder carries a value into the gate that never received one
    without = dr.ladder(1.0, 1.0, "liquid_outer_solid_inner", False, 4.54, locked=None,
                        rotation_period_h=32.0)
    ok(without.values["rossby_verdict"] == dr.NO_LOCK,
       "wiring: without the placeholder every body stops at cannot-say (no tidal_locking)")
    free = dr.ladder(1.0, 1.0, "liquid_outer_solid_inner", False, 4.54, locked=False,
                     rotation_period_h=32.0)
    ok(free.values["regime"] == "dipolar" and free.values["rossby_verdict"].startswith("dipolar by rule"),
       "wiring: locked False reaches the free-rotation branch, dipolar by the paper's rule")
    lock = dr.ladder(1.0, 1.0, "liquid_outer_solid_inner", False, 4.54, locked=True,
                     rotation_period_h=32.0)
    ok(lock.values["rossby_verdict"] == dr.ROSSBY_REFUSAL,
       "wiring: locked True reaches the C16 refusal — the first time anything reaches it at all")

    # ⚠ and no answer test exists, on purpose
    ok(LOCKED.value is False and "not because these bodies are known" in LOCKED.why,
       "answer: there is none — the value is a stand-in and the module must say so, or someone will "
       "read a passing wiring test as evidence that these bodies rotate freely")

    for f in fails:
        print(f"  [FAIL] {f}")
    if fails:
        return 1
    print(f"  [PASS] 임시값 가드레일 — ①넷째 단어(등급 아님) · ②값 단위 {len(REGISTRY)}개(중복 등록 거절) · "
          f"③emit 거절 · ④양쪽 기록 · ⑤레시피 도착 시 발화(오늘 증명) · "
          f"wiring: 없음→cannot-say / False→dipolar / True→C16 거절 최초 도달 · answer 시험 없음(의도)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
