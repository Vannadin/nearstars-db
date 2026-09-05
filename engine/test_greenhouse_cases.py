# 온실 사례 자기검증 — 숫자가 문서의 것인가 · 사례가 곱해지지 않는가 · 사례 안도 걸을 수 없는가
"""Hold the two published greenhouse cases to the document, and to the two refusals they exist for.

    python3 engine/test_greenhouse_cases.py

1. **The numbers are the document's.** Each printed form is looked up in
   `greenhouse-warming-methodology.md` itself, and the one unit conversion (a percent to a fraction)
   is written out here rather than done silently.
2. **The two cases do not multiply.** They are two options on one axis. Merging their members into one
   dictionary and walking it would produce an atmosphere neither paper modelled; the co_groups refuse.
3. **Neither case can be walked inside.** The pairing is not published, so in step is as much an
   invention as crossing.
4. **The H₂ mixing ratio is a point.** The document prints 0.1, not a range, and no width was added.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bands import corners  # noqa: E402
from greenhouse_cases import CASE_CHOICE, CASES  # noqa: E402

DOC = Path(__file__).resolve().parents[1] / "docs" / "reference" / "greenhouse-warming-methodology.md"

# 문서가 인쇄한 형태 → (사례, 필드, 기대 양끝). 퍼센트→분율 환산을 여기 드러낸다.
PRINTED = (
    ("1.3–4 bar CO₂", "early Mars (Ramirez 2014)", "co2_bar", (1.3, 4.0)),
    ("5–20 % H₂", "early Mars (Ramirez 2014)", "h2_fraction", (0.05, 0.20)),          # % → 분율
    ("2–3× the present N₂ mass", "early Earth (Wordsworth & Pierrehumbert 2013)", "n2_present", (2.0, 3.0)),
    ("CO₂ only 2–25× present", "early Earth (Wordsworth & Pierrehumbert 2013)", "co2_present", (2.0, 25.0)),
)


def main() -> int:
    fails: list[str] = []
    text = re.sub(r"\n[ \t]*(?=\S)", " ", DOC.read_text(encoding="utf-8"))

    # 1. every number came from the document
    for printed, case, field, (lo, hi) in PRINTED:
        # 여기서 묻는 것은 유일성이 아니라 출처다 — 앞의 둘은 본문과 참고문헌에 각각 한 번씩 실린다.
        if printed not in text:
            fails.append(f"1: {printed!r} is not printed in the document")
        band = CASES[case][field]
        if (band.low, band.high) != (lo, hi):
            fails.append(f"1: {case}/{field} is {(band.low, band.high)}, the document prints {printed}")

    # 4. the mixing ratio is a point the document prints as a point
    h2 = CASES["early Earth (Wordsworth & Pierrehumbert 2013)"]["h2_mixing_ratio"]
    if not (h2.kind == "point" and h2.value == 0.1):
        fails.append(f"4: the H₂ mixing ratio is printed as 0.1, a point; got {h2.kind} {h2.value}")
    if "H₂ mixing ratio of 0.1" not in text:
        fails.append("4: the document no longer prints the mixing ratio as 0.1")

    # 3. neither case can be walked inside
    for case, members in CASES.items():
        try:
            corners(members)
            fails.append(f"3: {case} was walked, but its pairing is not published")
        except ValueError as e:
            if "pairing unknown" not in str(e):
                fails.append(f"3: {case} refused for the wrong reason: {e}")

    # 2. and the two cases do not cross with each other
    merged = {f"{c[:4]}.{k}": v for c, m in CASES.items() for k, v in m.items()}
    try:
        corners(merged)
        fails.append("2: two published cases were crossed into an atmosphere neither paper modelled")
    except ValueError:
        pass
    if len(CASE_CHOICE.candidates) != 2 or CASE_CHOICE.default is not None:
        fails.append("2: the cases are two options on one axis, and neither is a default")

    for f in fails:
        print(f"  [FAIL] {f}")
    if fails:
        return 1
    print("  [PASS] 온실 사례 — 네 값 전부 문서 인쇄형과 일치(5–20 % → 0.05–0.20 환산 명시) · "
          "H₂ 혼합비는 점 0.1 · 사례 안 걸음 거절(짝짓기 미상) · 사례끼리 교차 거절 · 기본 사례 없음")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
