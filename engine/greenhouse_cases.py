# 환원 대기 온실 — 발표된 사례 둘을 사례째로 싣는다. 둘은 두 축이 아니라 한 축의 두 선택지다 (C32)
"""The two published reducing-atmosphere cases, kept whole.

    python3 engine/greenhouse_cases.py

`greenhouse-warming-methodology` prints two runs under one sentence — *"For reducing thick
atmospheres the published grid is already good"* — and it is tempting to read them as one grid with
four widths in it. They are not one grid. They are **two runs, on two different bodies, by two
different papers**:

- **Ramirez 2014**, early Mars, above 273 K on `1.3–4 bar CO₂` **plus** `5–20 % H₂`.
- **Wordsworth & Pierrehumbert 2013**, early Earth, above 0 °C at 75 % of present solar flux, on
  `2–3×` the present N₂ mass, `2–25×` present CO₂, and a H₂ mixing ratio of **0.1 — a point, not a
  range**.

Two things follow, and both are refusals:

1. **The cases do not multiply.** Ramirez's CO₂ width against Wordsworth's N₂ width is not a wider
   band, it is a body that neither paper modelled. So the cases are `Choice` candidates — one axis
   with two options — and not two bundles that a corner grid would happily cross.
2. **Neither case can be walked inside, either.** Raising CO₂ lets a run reach the same temperature on
   less H₂, so the low ends do not belong together any more than the crossed corners do. Our document
   prints the extent of each published region and not which combinations inside it clear freezing, so
   both members declare `pairing="unknown"` and `corners()` refuses them by name. Walking a bundle in
   step looks like the cautious option and is a second assumption.

What is left is what the document itself recommends: *"find a published run whose composition,
pressure and host spectrum bracket the body"* — borrow a case whole, and record which one.

Anchors (C33):
  greenhouse-warming-methodology.md@«For reducing thick atmospheres the published grid is already good:»
  greenhouse-warming-methodology.md@«reaches >273 K on early Mars with 1.3–4 bar CO₂ **plus 5–20 % H₂**»
  greenhouse-warming-methodology.md@«warm the early Earth above 0 °C at 75 % solar flux with 2–3× the present N₂ mass and a H₂ mixing ratio of 0.1, needing CO₂ only 2–25× present.»
  greenhouse-warming-methodology.md@«Note what those numbers require: **percent-level H₂, not traces.**»
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bands import Band, Choice, corners  # noqa: E402

DOC = "greenhouse-warming-methodology"
_RAMIREZ = f"{DOC} §borrow: Ramirez 2014 (2014NatGe...7...59R), early Mars above 273 K"
_WORDSWORTH = f"{DOC} §borrow: Wordsworth & Pierrehumbert 2013 (2013Sci...339...64W), early Earth above 0 °C"

#: 사례 안의 값들. 짝짓기가 인쇄돼 있지 않으므로 `pairing="unknown"` 이고, 그래서 걸을 수 없다.
CASES = {
    "early Mars (Ramirez 2014)": {
        "co2_bar": Band(None, 1.3, 4.0, _RAMIREZ, "calibrated", bundle="early-mars", pairing="unknown"),
        "h2_fraction": Band(None, 0.05, 0.20, _RAMIREZ, "calibrated", bundle="early-mars", pairing="unknown"),
    },
    "early Earth (Wordsworth & Pierrehumbert 2013)": {
        "n2_present": Band(None, 2.0, 3.0, _WORDSWORTH, "calibrated", bundle="early-earth", pairing="unknown"),
        "co2_present": Band(None, 2.0, 25.0, _WORDSWORTH, "calibrated", bundle="early-earth", pairing="unknown"),
        # 밴드가 아니다 — 문서가 혼합비 0.1 을 점으로 인쇄한다. 폭을 지어 붙이지 않는다.
        "h2_mixing_ratio": Band(0.1, None, None, "", "calibrated"),
    },
}

#: 두 사례는 한 축의 두 선택지다. 후보의 값이 스칼라가 아니라 **사례 이름**인 첫 자리다.
CASE_CHOICE = Choice(
    at="atmosphere_choice",
    quantity="which published reducing-atmosphere run to borrow",
    candidates=({"value": "early Mars (Ramirez 2014)", "end": "case", "grade": "calibrated",
                 "source": _RAMIREZ},
                {"value": "early Earth (Wordsworth & Pierrehumbert 2013)", "end": "case",
                 "grade": "calibrated", "source": _WORDSWORTH}),
    consequences={
        "what the atmosphere is made of": "the Mars case is CO₂-dominated with H₂ at percent level and "
                                          "no N₂ statement; the Earth case carries 2–3× present N₂ with "
                                          "CO₂ as the minor term. Borrowing one and quoting the other's "
                                          "numbers describes no published atmosphere.",
        "what counts as warm": "the Mars case clears 273 K on early Mars' insolation; the Earth case "
                               "clears 0 °C at 75 % of present solar flux. The two thresholds are not "
                               "the same statement about a third body.",
        "what stays true in both": "percent-level H₂, not traces — the document says so in its own "
                                   "sentence, and sustaining it needs a reducing mantle outgassing "
                                   "faster than escape.",
    },
    default=None,   # 기본값 없음: 어느 사례가 바디를 감싸는지는 바디를 봐야 안다
    note="the document's own instruction is to borrow a run that brackets the body, so there is no "
         "default case — picking one without looking at the body is the error this record exists to "
         "stop")


def main() -> int:
    print("발표된 환원 대기 사례 둘 — 두 축이 아니라 한 축의 두 선택지")
    for case, members in CASES.items():
        print(f"\n  {case}")
        for name, b in members.items():
            span = f"{b.low}–{b.high}" if b.kind == "interval" else f"{b.value} (점)"
            print(f"    {name:<18}{span:>14}   {'짝짓기 미상' if b.pairing == 'unknown' else ''}")
        try:
            corners(members)
            print("    ⚠ 걸어졌다 — 그러면 안 된다")
            return 1
        except ValueError as e:
            print(f"    → corners() 거절: {str(e).split(':')[1].strip().split('.')[0]}")
    print(f"\n기본 사례 없음 — {CASE_CHOICE.note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
