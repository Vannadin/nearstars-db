# NaN 은 부호가 아니다 — 이분이 NaN 끝으로 수렴하지 않고 각 자리의 거절 경로로 가는지, 괄호·부호 검사가 NaN 을 괄호로 안 받는지 (유한↔NaN 경계 심기)
"""Checks for the NaN sign/bracket/bisect class (directing / c8 7335778d fold-b1; artifacts ea-jobA
pc/ea-f13b/nanbisect/plan.md; 68 pc/audit68-nanbisect 4911b80e) on planted functions; no solve.

    python3 engine/test_nanbisect.py

Each plant is a function that is finite on one side and NaN past an edge that is no root. The old rule — `(fm > 0) ==
(fa > 0)`, or `fa * fb > 0` for a bracket — read NaN as «not > 0» and converged onto that edge, which it accepted as a
root. Each plant also runs that old rule inline (the mutant) and shows it converging onto the edge (red against it);
the fixed code refuses through the site's own path."""
from __future__ import annotations

import math
import sys
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import convergence                      # noqa: E402
import fold_track as ft                 # noqa: E402
import interior                         # noqa: E402
import rootfind as rf                   # noqa: E402
import rtpress                          # noqa: E402
import eos                              # noqa: E402

fails = 0
NAN = float("nan")


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += not ok


def old_bisect(f, a, b, fa, n=50):
    """The rule before the fix: NaN > 0 is False, so b moves onto every NaN midpoint."""
    for _ in range(n):
        m = 0.5 * (a + b)
        fm = f(m)
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
    return 0.5 * (a + b)


# (1) a sign change between finite ends with a NaN band inside: no root exists, the edge at 0.2 is not one
def hole(x):
    return -1.0 if x < 0.2 else (NAN if x < 0.7 else 1.0)


old = old_bisect(hole, 0.0, 1.0, -1.0)
check("(1) mutant: the old rule converges onto a finite↔NaN edge (0.2 or 0.7; with fa < 0 a NaN midpoint reads as "
      "«same side» and a moves onto it)", min(abs(old - 0.2), abs(old - 0.7)) < 1e-9, f"old → {old:.12g}")
check("(1) fold_track.bisect refuses (None)", ft.bisect(hole, 0.0, 1.0, -1.0) is None)
check("(1) fold_track.scan takes no root from the hole", ft.scan(hole, 0.0, 1.0, 1) == [])


# (2) a finite-positive side and NaN past 0.6: changes_sign already refused the end pair; the bisection itself refuses
def edge(x):
    return 1.0 if x < 0.6 else NAN


check("(2) mutant: old rule on (1 | NaN) converges onto 0.6", abs(old_bisect(edge, 0.0, 1.0, 1.0) - 0.6) < 1e-9)
check("(2) fold_track.bisect refuses", ft.bisect(edge, 0.0, 1.0, 1.0) is None)

# (3) a genuine root is unchanged (bit-identical to the old rule where no NaN occurs)
lin = lambda x: x - 0.3                                       # noqa: E731
check("(3) a finite root: new == old, bit for bit", ft.bisect(lin, 0.0, 1.0, -0.3) == old_bisect(lin, 0.0, 1.0, -0.3))

# (4) rootfind.brent: a NaN end is no bracket; a NaN trial ends the generator on its last finite best
try:
    rf.brent(0.0, NAN, 1.0, 1.0, 1e-12)
    check("(4) brent with a NaN end raises", False)
except ValueError:
    check("(4) brent with a NaN end raises", True)
g = rf.brent(0.0, -1.0, 1.0, 1.0, 1e-12)
x1 = next(g)
try:
    g.send(NAN)
    check("(4) brent ends on a NaN trial", False)
except StopIteration as stop:
    best = stop.value
    check("(4) brent ends on a NaN trial with a finite best", best is not None and best[1] == best[1], f"{best}")

# (5) bracket and sign tests: a NaN end is no bracket, and no sign change
check("(5) convergence.bracket_valid(NaN, 1) is False", convergence.bracket_valid(NAN, 1.0) is False)
check("(5) convergence.bracket_valid(−1, 1) is True", convergence.bracket_valid(-1.0, 1.0) is True)
check("(5) mutant: old product form passes NaN as a bracket", not (NAN * 1.0 > 0.0))
check("(5) rf.nan_free", rf.nan_free(1.0, -1.0) and not rf.nan_free(1.0, NAN))


# (6) rtpress.volume_full: P(V) NaN on part of the bracket — PhaseGap, never a root at the NaN edge; and the
#     product-form bracket with a NaN end (P(0.2 V0) NaN) — PhaseGap, where the old `g_lo * g_hi > 0` let it through
def p_hole(v, t):
    x = v / rtpress.V0
    return NAN if 0.5 < x < 0.8 else 100.0 * (1.0 / x) ** 3


with mock.patch.object(rtpress, "pressure", p_hole):
    try:
        v = rtpress.volume_full(100.0 / 0.6 ** 3, 3000.0)
        check("(6) volume_full refuses a root inside a NaN band", False, f"returned V/V0 {v / rtpress.V0:.6g}")
    except eos.PhaseGap:
        check("(6) volume_full refuses a root inside a NaN band (PhaseGap)", True)


def p_nan_end(v, t):
    x = v / rtpress.V0
    return NAN if x < 0.25 else 100.0 * (1.0 / x) ** 3


with mock.patch.object(rtpress, "pressure", p_nan_end):
    try:
        rtpress.volume_full(100.0 / 0.6 ** 3, 3000.0)
        check("(6) a NaN bracket end is no bracket (product form)", False)
    except eos.PhaseGap:
        check("(6) a NaN bracket end is no bracket (product form)", True)

# (7) interior._litho_bracket: g changes sign between iterates, the bisection's midpoint is NaN — refused by name
pts = [100.0, 110.0, 105.0]                  # g = +10, −5: a sign change on the last pair
r, why = interior._litho_bracket(pts, lambda r_: NAN, 1e-3)
check("(7) _litho_bracket refuses a NaN midpoint", r is None and "NaN" in str(why), str(why))

print(f"  test_nanbisect — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
