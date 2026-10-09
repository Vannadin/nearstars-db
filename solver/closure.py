# 자유 변수 하나의 근 찾기 — 로그 간격 훑기, 거절 시행은 벽(위치 찾기), 부호 바뀜마다 Brent (설계 §A1.5)
"""The single free scalar: scan, wall location, Brent.

Frozen design: rewrite/phase1-design.frozen.md §A1.5; registration rewrite/phase1-a1-impl.frozen.md S2/S3 and N4.

`F(x)` returns a float residual, or a `stepper.Stop` (a refusing trial). A refusing trial is a wall of the scan,
never the outcome (r2 H1). Walls are located by bisection with their own budget; every solved trial made while
locating a wall joins the sign-change search (N4). Each sign change inside a solved stretch is closed by Brent.
The outcome is typed; mapping to the refusal registry is solve.py's job.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from solver import stepper as st

N_SCAN = 17
WALL_TOL = 1e-6
WALL_SHOTS = 24
CLOSE_TOL = 1e-12
CLOSE_ITERS = 100            # Brent iterations per root (fixed by the S2 dated line)


@dataclass(frozen=True)
class Trial:
    x: float
    F: float | None              # None for a wall
    stop: st.Stop | None
    kind: str                    # "scan" | "wall" | "brent"


@dataclass(frozen=True)
class Wall:
    x: float                     # the located wall (first refusing x next to a solved one)
    stop: st.Stop
    solved_side: float           # the nearest solved x


@dataclass
class Outcome:
    kind: str                    # "root" | "two_roots" | "no_bracket" | "no_solved" | "unconverged"
    roots: list = field(default_factory=list)
    walls: list = field(default_factory=list)
    trials: list = field(default_factory=list)
    detail: dict = field(default_factory=dict)


def scan_points(lo: float, hi: float, n: int = N_SCAN) -> list:
    return [lo * (hi / lo) ** (i / (n - 1)) for i in range(n)]


def _brent(F, a: float, fa: float, b: float, fb: float, trials: list):
    """Brent's method (zeroin) on a bracket with fa·fb < 0, to |Δx| ≤ CLOSE_TOL·|x|. Bisection fallback guarantees
    shrink. A refusing evaluation inside a solved bracket is reported (it splits the bracket)."""
    c, fc = a, fa
    d = e = b - a
    for _ in range(CLOSE_ITERS):
        if fb * fc > 0.0:
            c, fc = a, fa
            d = e = b - a
        if abs(fc) < abs(fb):
            a, b, c = b, c, b
            fa, fb, fc = fb, fc, fb
        tol = 2.0 * 2.2e-16 * abs(b) + 0.5 * CLOSE_TOL * abs(b)
        m = 0.5 * (c - b)
        if abs(m) <= tol or fb == 0.0:
            return b, None
        if abs(e) >= tol and abs(fa) > abs(fb):
            s = fb / fa
            if a == c:
                p, q = 2.0 * m * s, 1.0 - s
            else:
                q, r = fa / fc, fb / fc
                p = s * (2.0 * m * q * (q - r) - (b - a) * (r - 1.0))
                q = (q - 1.0) * (r - 1.0) * (s - 1.0)
            if p > 0.0:
                q = -q
            p = abs(p)
            if 2.0 * p < min(3.0 * m * q - abs(tol * q), abs(e * q)):
                e, d = d, p / q
            else:
                d = e = m
        else:
            d = e = m
        a, fa = b, fb
        b = b + (d if abs(d) > tol else math.copysign(tol, m))
        v = F(b)
        if isinstance(v, st.Stop):
            trials.append(Trial(b, None, v, "brent"))
            return None, ("refused_inside", b, v)
        trials.append(Trial(b, v, None, "brent"))
        fb = v
    return None, ("unconverged", b, fb)


def _locate_wall(F, x_ok: float, x_bad: float, stop_bad: st.Stop, trials: list) -> Wall:
    for _ in range(WALL_SHOTS):
        if abs(x_bad - x_ok) <= WALL_TOL * abs(x_ok):
            break
        xm = 0.5 * (x_ok + x_bad)
        v = F(xm)
        if isinstance(v, st.Stop):
            trials.append(Trial(xm, None, v, "wall"))
            x_bad, stop_bad = xm, v
        else:
            trials.append(Trial(xm, v, None, "wall"))
            x_ok = xm
    return Wall(x_bad, stop_bad, x_ok)


def solve_scalar(F, lo: float, hi: float, n_scan: int = N_SCAN, use_wall_trials: bool = True) -> Outcome:
    """`use_wall_trials` exists only for N4's negative control (False drops the wall-location trials from the
    sign-change search, i.e. the behaviour N4 forbids)."""
    trials: list = []
    for x in scan_points(lo, hi, n_scan):
        v = F(x)
        trials.append(Trial(x, None, v, "scan") if isinstance(v, st.Stop) else Trial(x, v, None, "scan"))
    walls = []
    scan = sorted(trials, key=lambda t: t.x)
    for a, b in zip(scan, scan[1:]):
        if (a.F is None) != (b.F is None):
            ok, bad = (a, b) if a.F is not None else (b, a)
            walls.append(_locate_wall(F, ok.x, bad.x, bad.stop, trials))
    pts = sorted((t for t in trials if t.F is not None and (use_wall_trials or t.kind != "wall")),
                 key=lambda t: t.x)
    if not pts:
        return Outcome("no_solved", walls=walls, trials=trials)
    wall_xs = sorted(w.x for w in walls) + sorted(t.x for t in trials if t.F is None)
    roots, problems = [], []
    for a, b in zip(pts, pts[1:]):
        if any(min(a.x, b.x) < w < max(a.x, b.x) for w in wall_xs):
            continue                                  # not one solved stretch
        if a.F == 0.0:
            roots.append(a.x)
            continue
        if a.F * b.F < 0.0:
            x, prob = _brent(F, a.x, a.F, b.x, b.F, trials)
            if x is not None:
                roots.append(x)
            else:
                problems.append(prob)
    if pts[-1].F == 0.0:
        roots.append(pts[-1].x)
    detail = {"problems": problems, "lo": lo, "hi": hi, "n_scan": n_scan}
    if len(roots) == 1 and not problems:
        return Outcome("root", roots=roots, walls=walls, trials=trials, detail=detail)
    if len(roots) >= 2:
        return Outcome("two_roots", roots=roots, walls=walls, trials=trials, detail=detail)
    if any(p[0] == "unconverged" for p in problems):
        return Outcome("unconverged", roots=roots, walls=walls, trials=trials, detail=detail)
    return Outcome("no_bracket", roots=roots, walls=walls, trials=trials, detail=detail)
