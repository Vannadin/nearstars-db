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
3. **A co-selected group moves in step.** `A_Bond = q · p` ties two widths together, and the greenhouse forcing
   is a published combination grid; crossing co-selected members produces combinations nobody published,
   with a spread neither source supports.
4. **A choice needs at least two candidates and a measured consequence.** One candidate is a default
   wearing a costume; a consequence-free choice is a question, not a choice.
5. **Consequences are plural**, because a pick can improve one axis and cost another — the bright end
   of an albedo band moves temperature most, the dark end moves visual contrast most, in opposite
   directions. A single summary line would hide exactly that.
"""
from __future__ import annotations

import sys

from bands import GRADES, Band, Choice, Collapse, corners, floored, point
from payload import GRADES as PAYLOAD_GRADES


def main() -> int:
    fails: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # 0. one grade vocabulary, not two — this file once held a `declared` that payload has never had
    ok(GRADES is PAYLOAD_GRADES, "0: the grade vocabulary must be payload's own tuple, not a copy")

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
    ok({"b_eq": 1.0, "b_eq_min": 0.9, "b_eq_max": 1.1}.items() <= interval.emit("b_eq").items(),
       f"1: emit must keep dynamo.py's existing *_min/*_max shape, got {interval.emit('b_eq')}")
    ok(not {"x_min", "x_max"} & set(plate.emit("x")), "1: a point emits no band ends")

    # 1b. a band may have ends and no point inside them — the eight albedo rows are all like this
    unchosen = Band(None, 0.5, 0.85, "the albedo table prints the row and no point in it", "analog")
    ok(unchosen.kind == "interval" and not unchosen.chosen,
       "1b: ends printed with no pick is still an interval, and says so")
    ok(interval.chosen, "1b: a band given a working point says so")
    ok(unchosen.ends() == (0.5, 0.85), f"1b: an unchosen band walks its ends, got {unchosen.ends()}")

    # 1c. an unchosen band still emits (the game needs a number), but never as a bare one:
    # the label says nobody picked it, and the ends travel with it. (Owner, 2026-09-05.)
    e = unchosen.emit("albedo")
    ok(e["albedo"] == 0.675, f"1c: an unchosen middle is filled, got {e['albedo']}")
    ok(e["albedo_pick"].startswith("unchosen"),
       f"1c: the filled point must be labelled unchosen, got {e['albedo_pick']!r}")
    ok({"albedo_min", "albedo_max", "albedo_width_source"} <= set(e),
       "1c: a filled point never travels without its ends and their source")
    ok(unchosen.pick == "unchosen" and interval.pick == "chosen",
       "1c: chosen and unchosen must not share a label")

    # 1d. Z-2: a printed centre is the default; computing a midpoint over it overwrites the document
    printed = Band(660.0, 540.0, 810.0, "the dynamo table prints 660 µT (540–810)", "calibrated",
                   value_origin="printed")
    ok(printed.emit("b_eq")["b_eq"] == 660.0 and printed.pick == "printed",
       "1d: a printed centre is emitted as printed, not replaced by the midpoint 675")
    ok(printed.middle() == 675.0, "1d: the midpoint is still computable, it is just not what is used")

    # 1e. Z-3: the mean is the band's to declare, because picking one for all bands invents a rate
    geo = Band(None, 0.05, 0.10, "OC06 prints both ends", "measured", mean="geometric")
    ok(abs(geo.emit("multipolar")["multipolar"] - 0.0707106781) < 1e-9,
       f"1e: a geometric band fills the geometric middle, got {geo.emit('multipolar')['multipolar']}")
    ok(abs(Band(None, 0.05, 0.10, "OC06", "measured").middle() - 0.075) < 1e-12,
       "1e: silence means arithmetic")
    for kw, why in ((dict(mean="geometric", low=-1.0, high=1.0), "1e: a geometric mean needs positive ends"),
                    (dict(mean="harmonic"), "1e: an undeclared mean must be refused, not guessed")):
        try:
            Band(None, kw.pop("low", 0.5), kw.pop("high", 0.85), "doc", "analog", **kw)
            fails.append(why)
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

    # 3. co_groups move in step; independents cross
    q = Band(0.5, 0.3, 0.8, "albedo table, eight rows", "measured", co_selected="albedo")
    p = Band(1.0, 0.8, 1.2, "phase-integral table", "measured", co_selected="albedo")
    grid = corners({"q": q, "p": p, "x": interval})
    ok(len(grid) == 9, f"3: 3 co-selected steps × 3 independent ends = 9 combinations, got {len(grid)}")
    allowed = {(0.3, 0.8), (0.5, 1.0), (0.8, 1.2)}
    ok(all((c["q"], c["p"]) in allowed for c in grid),
       "3: a co-selected group's members must never be crossed against each other")
    try:
        corners({"a": Band(1, 0, 2, "doc", "measured", co_selected="b"),
                 "c": Band(1, None, None, "", "authored", co_selected="b")})
        fails.append("3: co-selected members with different end counts must be refused")
    except ValueError:
        pass

    # 3b. in step is a claim too: a co_selected nobody published a pairing for refuses to be walked
    try:
        corners({"co2": Band(None, 1.3, 4.0, "Ramirez 2014", "calibrated", co_selected="early-mars",
                             pairing="unknown"),
                 "h2": Band(None, 0.05, 0.20, "Ramirez 2014", "calibrated", co_selected="early-mars",
                            pairing="unknown")})
        fails.append("3b: a co_selected with an unpublished pairing must refuse — the diagonal is a claim too")
    except ValueError as e:
        ok("unknown" in str(e) and "early-mars" in str(e),
           f"3b: the refusal must name the co_selected and why, got {e}")
    ok(corners({"q": q, "p": p}) and all(b.pairing == "in step" for b in (q, p)),
       "3b: a co_selected whose pairing IS published still walks")
    # and it has no middle of its own either: filling one per sibling rebuilds the refused combination
    try:
        Band(None, 1.3, 4.0, "Ramirez 2014", "calibrated", co_selected="early-mars",
             pairing="unknown").emit("co2_bar")
        fails.append("3b: a pairing-unknown member must not fill a middle of its own")
    except ValueError as e:
        ok("whole" in str(e), f"3b: the refusal must send the caller to the case, got {e}")
    try:
        Band(1.0, 0.9, 1.1, "doc", "measured", pairing="unknown")
        fails.append("3b: pairing on a band with no co_selected must be refused — nothing to pair with")
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
    # an adopted value that disagrees with its own printed band is not a pick from it
    outside = Collapse("A_Bond", 0.30, "outside", "the board adopts 0.3 beside a printed Class II "
                       "albedo of 0.5–0.8", "owner")
    ok("outside" in outside.line() or outside.end == "outside",
       "5b: a value outside its band gets its own word, so a filled middle cannot stand in for it")
    try:
        Collapse("x", 1.0, "middle", "y", "owner")
        fails.append("5b: an unknown end word must be refused")
    except ValueError:
        pass

    line = Collapse("A_Bond", 0.30, "value", "board pick, 2026-06", "owner").line()
    ok("low" not in line and "0.3" in line and "owner" in line,
       f"collapse must record the value, the end and who chose: {line}")

    for f in fails:
        print(f"  [FAIL] {f}")
    if fails:
        return 1
    print("  [PASS] 밴드 규칙 — 등급 어휘 단일 · 세 상태(구간·바닥 있는 점·점) · 출처 없는 폭 거절 · 값이 밴드 밖이면 거절 · "
          "미선택 emit=라벨+양끝 동반 · 인쇄된 중심 보존 · 평균 선언 · 묶음 불가분(9조합, 교차 없음) · 짝짓기 미상 묶음 거절(걸음·중간값 둘 다) · 후보 2개 미만 거절 · 귀결 없는 선택지 거절 · 귀결 복수 · 붕괴 기록")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    raise SystemExit(main())
