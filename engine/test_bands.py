# 밴드 규칙 자기검증 — 세 상태 · 묶음 불가분 · 선택지 요건 (C32)
"""Hold the band rules to what they claim.

    python3 engine/test_bands.py

The rules exist because each of them was broken somewhere before it was written down:

1. **Three shapes, not two.** A width needs both ends printed to be an interval; one end printed is a
   *floored point*, which is real information and must not be flattened. The heat-pipe row is the
   live case — 2.5 W/m² with "no firm upper bound" — and its floor carries its own grade, because
   that 2.5 is one body's computed flux rather than a published boundary.
2. **A width without a source is not a band.** Two numbers with nothing behind them look exactly like
   a measurement to whoever reads the value next.
3. **A bundle moves in step.** `A_Bond = q · p` ties two widths together, and the greenhouse forcing
   is a published combination grid; crossing bundle members produces combinations nobody published,
   with a spread neither source supports.
4. **A choice needs at least two candidates and a measured consequence.** One candidate is a default
   wearing a costume; a consequence-free choice is a question, not a choice.
5. **Consequences are plural**, because a pick can improve one axis and cost another — the bright end
   of an albedo band moves temperature most, the dark end moves visual contrast most, in opposite
   directions. A single summary line would hide exactly that.
"""
from __future__ import annotations

import sys

from bands import Band, Choice, Collapse, corners, floored, point


def main() -> int:
    fails: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # 1. three shapes
    interval = Band(1.0, 0.9, 1.1, "OC06 prints both 0.05 and 0.10", "measured")
    heat_pipe = floored(2.5, 2.5, "the document prints a floor and says no upper bound is published",
                        grade="analog", floor_grade="analog")
    plate = point(0.135, "authored")
    ok(interval.kind == "interval", f"1: both ends printed → interval, got {interval.kind}")
    ok(heat_pipe.kind == "floored point", f"1: one end printed → floored point, got {heat_pipe.kind}")
    ok(plate.kind == "point", f"1: nothing printed → point, got {plate.kind}")
    ok(heat_pipe.floor_grade == "analog",
       "1: a floor keeps its own grade — the heat-pipe floor is one body's computed flux")

    # the emitted shape is the one the recipes already use
    ok(interval.emit("b_eq") == {"b_eq": 1.0, "b_eq_min": 0.9, "b_eq_max": 1.1},
       f"1: emit must match dynamo.py's existing *_min/*_max shape, got {interval.emit('b_eq')}")
    ok(set(plate.emit("x")) == {"x"}, "1: a point emits no band keys")

    # 1b. a band may have ends and no point inside them — the eight albedo rows are all like this
    unchosen = Band(None, 0.5, 0.85, "the albedo table prints the row and no point in it", "analog")
    ok(unchosen.kind == "interval" and not unchosen.chosen,
       "1b: ends printed with no pick is still an interval, and says so")
    ok(interval.chosen, "1b: a band given a working point says so")
    ok(unchosen.ends() == (0.5, 0.85), f"1b: an unchosen band walks its ends, got {unchosen.ends()}")
    try:
        unchosen.emit("albedo")
        fails.append("1b: emitting a band nobody picked a point in must be refused — that pick is a Collapse")
    except ValueError:
        pass
    try:
        Band(None, None, None, "", "analog")
        fails.append("1b: a band with neither a value nor an end must be refused")
    except ValueError:
        pass

    # 2. a width must say where its ends are printed
    try:
        Band(1.0, 0.9, 1.1, "", "measured")
        fails.append("2: a width with no source must be refused")
    except ValueError:
        pass
    try:
        Band(1.0, 1.2, 1.4, "doc", "measured")
        fails.append("2: a value outside its own band must be refused")
    except ValueError:
        pass

    # 3. bundles move in step; independents cross
    q = Band(0.5, 0.3, 0.8, "albedo table, eight rows", "measured", bundle="albedo")
    p = Band(1.0, 0.8, 1.2, "phase-integral table", "measured", bundle="albedo")
    grid = corners({"q": q, "p": p, "x": interval})
    ok(len(grid) == 9, f"3: 3 bundle steps × 3 independent ends = 9 combinations, got {len(grid)}")
    allowed = {(0.3, 0.8), (0.5, 1.0), (0.8, 1.2)}
    ok(all((c["q"], c["p"]) in allowed for c in grid),
       "3: a bundle's members must never be crossed against each other")
    try:
        corners({"a": Band(1, 0, 2, "doc", "measured", bundle="b"),
                 "c": Band(1, None, None, "", "authored", bundle="b")})
        fails.append("3: bundle members with different end counts must be refused")
    except ValueError:
        pass

    # 4/5. a choice needs candidates and consequences
    cands = ({"value": 0.010, "end": "low", "source": "Venus 10–20 mW/m²", "grade": "measured"},
             {"value": 0.030, "end": "high", "source": "Mars 15–30 mW/m²", "grade": "measured"})
    good = Choice(at="heat_transport_mode", quantity="stagnant-lid ceiling", candidates=cands,
                  consequences={"roster labels": "how many bodies read stagnant lid rather than plate",
                                "solar-system control": "agreement with the four measured bodies"},
                  default=0.030)
    ok(len(good.consequences) == 2, "5: consequences are a mapping so two axes can disagree")
    for kw, why in (({"candidates": cands[:1], "consequences": {"a": "b"}},
                     "4: one candidate is not a choice"),
                    ({"candidates": cands, "consequences": {}},
                     "4: a choice with no measured consequence is a question")):
        try:
            Choice(at="x", quantity="y", **kw)
            fails.append(why)
        except ValueError:
            pass

    # a collapse says what, which end, and why
    line = Collapse("A_Bond", 0.30, "value", "board pick, 2026-06", "owner").line()
    ok("low" not in line and "0.3" in line and "owner" in line,
       f"collapse must record the value, the end and who chose: {line}")

    for f in fails:
        print(f"  [FAIL] {f}")
    if fails:
        return 1
    print("  [PASS] 밴드 규칙 — 세 상태(구간·바닥 있는 점·점) · 출처 없는 폭 거절 · 값이 밴드 밖이면 거절 · "
          "값 없는 구간 emit 거절 · 묶음 불가분(9조합, 교차 없음) · 후보 2개 미만 거절 · 귀결 없는 선택지 거절 · 귀결 복수 · 붕괴 기록")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    raise SystemExit(main())
