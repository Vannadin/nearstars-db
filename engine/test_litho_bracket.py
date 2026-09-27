# 층 바닥 자리 괄호 풀이의 규칙 시험 — 오가는 반복은 닫힘 · 한쪽 부호는 이름 댄 거절 · 계단은 표지 (prereg-litho-fixed-point-bracket)
"""Checks for `interior._litho_bracket` (pre-registration `prereg-litho-fixed-point-bracket.md`, frozen 9cc09710).

    python3 engine/test_litho_bracket.py

The helper is driven with made-up R(r − D) maps, so each rule is asked alone:
  LB-닫힘   — an oscillating smooth map: the last sign-changing pair brackets the root and pure bisection lands within
              LITHO_R_TOL, in exactly ⌈log₂(W₀ / tol)⌉ halvings;
  LB-거절   — a map whose g keeps one sign over the iterated points: refused, «괄호 못 잡음» named;
  LB-계단   — a map with a jump across the root (g never crosses zero): not refused, flagged «계단 위의 뿌리».
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import interior                        # noqa: E402

TOL = interior.LITHO_R_TOL
fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


def iterate(radius_at, r0: float, n: int = interior.LITHO_ITERS) -> list:
    pts = [r0]
    for _ in range(n):
        pts.append(radius_at(pts[-1]))
    return pts


R_STAR = 6.371e6

# LB-닫힘 — slope −1.05 about the root: the fixed-point map overshoots and never contracts, g alternates sign
osc = lambda r: R_STAR - 1.05 * (r - R_STAR)
pts = iterate(osc, R_STAR + 300.0)
r, info = interior._litho_bracket(pts, osc, TOL)
g_end = abs(osc(r) - r) if r is not None else math.inf
check("LB-닫힘 — an oscillating map that plain iteration cannot close is bracketed and bisected",
      r is not None and abs(r - R_STAR) <= TOL and not info[2], f"r − R* {r - R_STAR if r else None!r} m · {info}")
if r is not None:
    check("LB-닫힘 — the halving count is ⌈log₂(W₀ / tol)⌉", info[1] == math.ceil(math.log2(info[0] / TOL)),
          f"width {info[0]:.4g} m · halvings {info[1]}")

# LB-거절 — slope +0.999: g keeps one sign over all points
slow = lambda r: R_STAR + 0.999 * (r - R_STAR)
r, why = interior._litho_bracket(iterate(slow, R_STAR + 5000.0), slow, TOL)
check("LB-거절 — one-signed g over the iterated points is refused by name", r is None and "괄호 못 잡음" in why, str(why))

# LB-계단 — a jump of 50 m at the root: g flips sign but never reaches zero
step = lambda r: R_STAR + (25.0 if r < R_STAR else -25.0)
r, info = interior._litho_bracket(iterate(step, R_STAR + 300.0), step, TOL)
check("LB-계단 — a step across the root is not refused; it is flagged as a root on a step",
      r is not None and info[2] and abs(r - R_STAR) <= info[0], f"r − R* {r - R_STAR if r else None!r} m · {info}")
check("LB-계단 — the leftover |R − r| at a step root is reported (half-jump 25 m + r's own offset from the jump)",
      r is not None and abs(info[3] - (25.0 + abs(r - R_STAR))) < 1e-9, f"|g| {info[3] if r else None!r}")

print(f"\n  test_litho_bracket — {'모두 통과' if fails == 0 else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
