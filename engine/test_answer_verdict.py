# interior.answer_verdict 두 칸(불수락 · 표지)을 아는 판 넷으로 가르는 시험 (prereg-melt-window-answers 덧붙임 4)
"""Four known cases, fixed before results (melt-window addendum 4): an outer converged=False is refused;
an inner-only False is accepted with a tag naming the solver sites; both True and an inner None pass clean."""
from __future__ import annotations

import sys
import types

import interior


def _r(outer, inner, sites=None):
    return types.SimpleNamespace(applicable=True, reason=None, notes=(), converged=outer,
                                 values={"converged": inner, "unconverged_solvers": sites or []})


def main() -> int:
    fails = 0
    for name, r, refuse, tag in (("① 겉 False", _r(False, True), True, []),
                                 ("② 겉 True · 속 False", _r(True, False, ["x.y"]), False, ["속 풀이 미수렴 — x.y"]),
                                 ("③ 둘 다 True", _r(True, True), False, []),
                                 ("④ 속 None", _r(True, None), False, [])):
        tags = []
        why = interior.answer_verdict(r, tags)
        ok = (why is not None) == refuse and tags == tag
        fails += not ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} — 불수락 {why is not None} · 표지 {tags}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
