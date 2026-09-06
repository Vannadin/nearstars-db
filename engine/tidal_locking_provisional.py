# tidal_locking.locked 의 임시값 — 레시피가 아니라 자리표다. C36 이 이 자리를 가져간다
"""The one placeholder standing today: `tidal_locking.locked`.

    python3 engine/tidal_locking_provisional.py

`tidal_locking` is declared in `chain.yaml` with `recipe: tidal-locking-timescale-methodology` and no
registered recipe, so `locked` never reaches anybody and every body takes `dynamo_rocky`'s
`cannot-say (no tidal_locking)` branch. The C16 regime gate has therefore never run on a real body —
its refusal has never been reached, only stepped around.

⚠ **This is not a recipe and must not become one.** Working out whether a body is tidally locked means
solving the locking timescale, and that is C36, released by the owner as the next item. Registering
this through `registry.recipe` would claim the node computes, take the seat C36 needs, and leave
guardrail 5 with nothing to fire on. So the value is supplied and the node stays unbuilt.

**Which output.** The node owes three — `locked`, `t_lock`, `rotation_period` — and exactly one is
stood in for. `t_lock` has no consumer yet. `rotation_period` is a separate defect and is left alone:
`dynamo_rocky` asks `state.get("rotation_period")` while bodies declare `rotation_period_h`, so it has
been reading `None` all along (C37).

**Pre-registered, before running it.** Two outcomes are expected, and anything else is the finding:

- a body whose `locked` is False → **dipolar by the paper's rule** (RM22 §5.2, eq. 20; `Ro_ℓ` is not
  evaluated on that path), and
- a body whose `locked` is True → the locked branch, **refused by the two remaining names** (`ν` has
  no value; the printed `Ro_ℓ` misses RM22's own Table 8 by 4–5×).

Reaching the refusal **at all** is the measurement. It has never happened on a real body.

**And this is a controlled A/B for C36.** The wiring is being frozen now, with the answer stipulated;
when the real recipe lands, the answer changes and the wiring does not. Whatever moves then, moved
because of the physics — the two are not being changed together. That is why the placeholder is worth
building rather than waiting a day for the recipe.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provisional import Placeholder, refuse_emit, register, standing_on, supply  # noqa: E402

#: 값은 False 다 — "잠기지 않았다"가 참이라서가 아니라, **어느 값이든 사슬이 돌기만 하면 되고**
#: 그 자리가 임시라는 사실이 라벨에 있기 때문이다. 참으로 주장하는 값이 아니다.
LOCKED = register(Placeholder(
    node="tidal_locking",
    output="locked",
    value=False,
    why=("C36 must solve the tidal-locking timescale and return this. Until then the value is a "
         "stand-in: False was chosen so the chain runs, not because these bodies are known to rotate "
         "freely."),
    consumers=("body_figure", "cassini_state", "tidal_heating", "day_night_contrast", "dynamo_giant",
               "dynamo_rocky", "atmospheric_escape", "t_eq_stellar"),
))


def main() -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import dynamo_rocky as dr
    from state import BodyState

    print(LOCKED.line(), "\n")
    print(f"소비처 {len(LOCKED.consumers)}곳: {', '.join(LOCKED.consumers)}")
    print("→ 임시값 하나가 여덟 갈래로 퍼진다. 그래서 emit 금지와 양쪽 기록이 이 자리의 핵심이다.\n")

    for label, locked in (("without the placeholder", None), ("with it (False)", False),
                          ("with it flipped (True)", True)):
        res = dr.ladder(1.0, 1.0, "liquid_outer_solid_inner", False, 4.54, locked=locked,
                        rotation_period_h=32.0)
        print(f"  {label:<24} regime={res.values['regime']:<26} {res.values['rossby_verdict'][:56]}")

    st = BodyState(name="probe", kind="planet", inputs={"mass_earth": 1.0})
    supply(st, LOCKED)
    print(f"\n  standing_on → {standing_on(st, 'locked', 'mass_earth')}")
    print(f"  emit         → {refuse_emit(st)[:96]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
