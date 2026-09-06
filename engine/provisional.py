# 아직 만들지 않은 노드의 값을 임시로 세워 사슬을 굴린다 — 다섯 가드레일이 이 모듈의 전부다
"""A value nobody has computed yet, standing in so the chain downstream can run.

    from provisional import Placeholder, standing_on, refuse_emit, recipe_arrived

The owner set the pattern on 2026-09-06: *if a value must come from a node nobody has built, write
down that the node will owe it, put any value in for now so the thing runs, test on real bodies, and
test again when the wiring lands.* Without guardrails that is precisely the silent default this
engine spent two days removing, so the guardrails are not decoration — they are the pattern.

1. **Its own word.** `bands.py` already refuses to let three origins share a name — `printed`,
   `chosen`, `unchosen`. **`provisional` is the fourth**, and it means *nobody has computed this and
   nobody has chosen it either*. It is deliberately not a grade: `payload.GRADES` describes how well a
   value is known, and a placeholder is not badly-known, it is **not-yet-a-value**.
2. **It is counted, by value and not by node.** A node with three outputs of which one is a
   placeholder is one placeholder, not one node's worth. `tidal_locking` is exactly that case.
3. **It may not be emitted.** Run the chain on it, publish nothing from it.
4. **Both ends carry the record.** The owing node is named here; and anything computed downstream can
   ask `standing_on(...)` and say so in its own output.
5. **The gate tightens the moment the real recipe lands.** `recipe_arrived()` reports any placeholder
   whose node now has a registered recipe. That is the check people forget to run, so it runs itself.

⚠ **A placeholder is not a quick calculation.** If a value can be derived, derive it; if it can be
declared from a source, declare it. Both were tried before this module was written and both worked —
`stellar_wind` needed none of it. A placeholder is only for a node that must genuinely be built.
"""
from __future__ import annotations

from dataclasses import dataclass, field

#: bands.py 의 세 단어와 절대 겹치지 않는 넷째 단어.
PROVISIONAL = "provisional"


@dataclass(frozen=True)
class Placeholder:
    """One output of one unbuilt node, standing in until that node exists."""

    node: str                 # the node that will owe this value
    output: str               # which of its outputs — a node may owe several and have only one stood in
    value: object             # whatever lets the chain run; its truth is not claimed
    why: str                  # what the real node will have to do instead
    consumers: tuple[str, ...] = ()   # who reads it, so the blast radius is on the record

    def __post_init__(self) -> None:
        for name in ("node", "output", "why"):
            if not getattr(self, name):
                raise ValueError(f"a placeholder needs {name}: a value with no owner is a silent default")

    @property
    def pick(self) -> str:
        return PROVISIONAL

    def line(self) -> str:
        return (f"{self.node}.{self.output} = {self.value!r} — provisional, nobody computed it. "
                f"{self.why}")


#: 등록된 임시값 전부. 세는 단위는 **값**이다 (가드레일 2).
REGISTRY: dict[tuple[str, str], Placeholder] = {}


def register(ph: Placeholder) -> Placeholder:
    key = (ph.node, ph.output)
    if key in REGISTRY:
        raise ValueError(f"{key} already has a placeholder; two stand-ins for one value is one too many")
    REGISTRY[key] = ph
    return ph


def supply(state, ph: Placeholder) -> None:
    """Put the value where the chain reads it, and leave a mark that says what it is.

    `BodyState` deliberately does not distinguish declared inputs from derived ones — recipes read
    `state[k]` and do not care. That is the right design and it is exactly why a placeholder cannot
    simply be written into `inputs` and left: it would become indistinguishable from a measurement.
    The mark is what keeps them apart."""
    state.inputs[ph.output] = ph.value
    marks = state.inputs.setdefault("_provisional", [])
    if ph.output not in marks:
        marks.append(ph.output)


def standing_on(state, *keys: str) -> tuple[str, ...]:
    """Which of these values a result is standing on. Empty means the result is clean."""
    marks = state.inputs.get("_provisional", ())
    return tuple(k for k in keys if k in marks)


def refuse_emit(state) -> str | None:
    """The reason an emit must not happen, or None. Guardrail 3."""
    marks = tuple(state.inputs.get("_provisional", ()))
    if not marks:
        return None
    return (f"cannot emit: {', '.join(marks)} " +
            ("is" if len(marks) == 1 else "are") +
            " provisional — nobody has computed " +
            ("it" if len(marks) == 1 else "them") +
            ". The chain may run on this; the board and the game may not.")


def recipe_arrived(registered: set[str]) -> list[str]:
    """Placeholders whose node now has a real recipe. Guardrail 5 — the gate reads this.

    `registered` is `registry.registered()`. Kept as an argument rather than imported so that the
    check can be pointed at a hypothetical set: the test proves this fires by handing it a node name,
    instead of waiting for the day it happens."""
    return [f"{ph.node}.{ph.output} is still provisional, but `{ph.node}` now has a recipe — "
            f"delete the placeholder and re-run the tests that were written against it"
            for (node, _out), ph in sorted(REGISTRY.items()) if node in registered]


def report() -> str:
    if not REGISTRY:
        return "임시값 위에 선 값 0개."
    lines = [f"임시값 위에 선 값 {len(REGISTRY)}개 (노드가 아니라 **값** 단위로 센다):"]
    lines += [f"  {ph.line()}" for _k, ph in sorted(REGISTRY.items())]
    return "\n".join(lines)
