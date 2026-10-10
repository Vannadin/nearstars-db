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
# A1 impl note 8 (directing, 2026-10-10): a refusing shot is a wall only when confirmed by a second shot a little
# further from the solved side (CONFIRM_FRAC of the gap, at least CONFIRM_MIN·|x|). If that shot solves, the refusal
# is isolated (e.g. one unlanded event at Earth 2064.76 K, x = 6437400.24 m): recorded as kind "isolated", never a
# wall, and the solved shot joins the search.
CONFIRM_FRAC = 0.01
CONFIRM_MIN = 1e-9
CONFIRM_MAX = 4              # confirming shots per refusal chain (r2 on d031605b: the reason must match)


def reason(stop: st.Stop) -> tuple:
    """A refusal's reason, as fine as the registry id or finer: the stop kind, the cap for event_chatter, and for a
    refused stage the inner refusal's kind and material."""
    r = stop.record
    if stop.kind == "chatter" and isinstance(r, dict):
        return ("chatter", r.get("cap_name"))
    if stop.kind == "refused":
        inner = r.record if isinstance(r, st.Stop) else r
        if isinstance(inner, st.Stop):
            return ("refused", inner.kind)
        return ("refused", type(inner).__name__, getattr(inner, "kind", None), getattr(inner, "material_id", None))
    return (stop.kind,)


@dataclass(frozen=True)
class Trial:
    x: float
    F: float | None              # None for a wall
    stop: st.Stop | None
    kind: str                    # "scan" | "wall" | "brent" | "confirm" | "isolated"


@dataclass(frozen=True)
class Wall:
    x: float                     # the located wall (first refusing x next to a solved one)
    stop: st.Stop
    solved_side: float           # the nearest solved x
    located: bool = True         # False when WALL_SHOTS ran out before WALL_TOL (NoAnswer budget WALL_SHOTS)


@dataclass
class Outcome:
    kind: str                    # "root" | "two_roots" | "no_bracket" | "no_solved" | "unconverged"
    roots: list = field(default_factory=list)
    walls: list = field(default_factory=list)
    trials: list = field(default_factory=list)
    detail: dict = field(default_factory=dict)


def scan_points(lo: float, hi: float, n: int = N_SCAN) -> list:
    """Log-spaced for lo > 0 (R, boundary masses); linear when lo = 0 (a composition axis such as Dante's φ₀ ∈
    [0, 0.60], r2 S7 B3)."""
    if lo > 0.0:
        return [lo * (hi / lo) ** (i / (n - 1)) for i in range(n)]
    return [lo + (hi - lo) * i / (n - 1) for i in range(n)]


def _brent(F, a: float, fa: float, b: float, fb: float, trials: list):
    """Brent's method (zeroin) on a bracket with fa·fb < 0, to |Δx| ≤ CLOSE_TOL·|x|. Bisection fallback guarantees
    shrink. A refusing evaluation inside a solved bracket is reported (it splits the bracket). Returns (root, None,
    final bracket (x_b, F_b, x_c, F_c)) or (None, problem, None); the final bracket names where a jump would sit
    (phase-1 design note 8)."""
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
            return b, None, (b, fb, c, fc)
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
        v = _value(F, b)
        if isinstance(v, st.Stop):
            trials.append(Trial(b, None, v, "brent"))
            return None, ("refused_inside", b, v), None
        trials.append(Trial(b, v, None, "brent"))
        fb = v
    return None, ("unconverged", b, fb), None


def _value(F, x: float):
    """F(x) as a finite float, or a Stop. A non-finite or missing residual (e.g. a stopped pass's F = None) is a
    refusal of that trial, never a solved value (r2 N5)."""
    v = F(x)
    if isinstance(v, st.Stop):
        return v
    if v is None or not math.isfinite(v):
        return st.Stop("no_residual", {"x": x, "value": v})
    return float(v)


def _confirm(F, x_bad: float, x_ok: float, lo: float, hi: float, trials: list):
    """The confirming shot for a refusal at x_bad, further from the solved side x_ok (inside [lo, hi]; toward x_ok
    when x_bad is at the range end). Returns (x_c, value)."""
    step = max(CONFIRM_FRAC * abs(x_bad - x_ok), CONFIRM_MIN * abs(x_bad))
    d = 1.0 if x_bad >= x_ok else -1.0
    xc = x_bad + d * step
    if not (lo <= xc <= hi):
        xc = x_bad - d * step
    v = _value(F, xc)
    trials.append(Trial(xc, None, v, "confirm") if isinstance(v, st.Stop) else Trial(xc, v, None, "confirm"))
    return xc, v


def _confirm_chain(F, x_bad: float, stop_bad: st.Stop, x_ok: float, lo: float, hi: float, trials: list):
    """A wall only when a confirming shot refuses for the same reason (r2): a solved shot isolates x_bad
    (→ ("solved", x_c, value)); a shot refusing for another reason isolates x_bad and becomes the candidate, confirmed
    again (at most CONFIRM_MAX shots); a matching reason confirms the candidate (→ ("wall", x, stop))."""
    for _ in range(CONFIRM_MAX):
        xc, vc = _confirm(F, x_bad, x_ok, lo, hi, trials)
        if not isinstance(vc, st.Stop):
            _isolate(trials, x_bad, stop_bad)
            return "solved", xc, vc
        if reason(vc) == reason(stop_bad):
            return "wall", x_bad, stop_bad
        _isolate(trials, x_bad, stop_bad)
        x_bad, stop_bad = xc, vc
    return "wall", x_bad, stop_bad                    # budget spent: the last candidate stands, unconfirmed


def _isolate(trials: list, x: float, stop: st.Stop):
    """Re-label the refusing trial at x as isolated (kept as a record, out of the wall and stretch logic)."""
    for n, t in enumerate(trials):
        if t.x == x and t.F is None and t.kind != "isolated":
            trials[n] = Trial(x, None, stop, "isolated")


def _locate_wall(F, x_ok: float, x_bad: float, stop_bad: st.Stop, trials: list, lo: float, hi: float) -> Wall:
    for _ in range(WALL_SHOTS):
        if abs(x_bad - x_ok) <= WALL_TOL * max(abs(x_ok), abs(x_bad)):
            break
        xm = 0.5 * (x_ok + x_bad)
        v = _value(F, xm)
        if isinstance(v, st.Stop):
            trials.append(Trial(xm, None, v, "wall"))
            what, xc, vc = _confirm_chain(F, xm, v, x_ok, lo, hi, trials)
            if what == "wall":
                x_bad, stop_bad = xc, vc
            else:                                        # isolated: the solved shot beyond it moves the ok side
                x_ok = xc if abs(xc - x_bad) < abs(x_ok - x_bad) else x_ok
        else:
            trials.append(Trial(xm, v, None, "wall"))
            x_ok = xm
    return Wall(x_bad, stop_bad, x_ok, abs(x_bad - x_ok) <= WALL_TOL * max(abs(x_ok), abs(x_bad)))


MAX_SPLITS = 16              # refusals met inside a Brent bracket, each splitting it (then re-searched)


def solve_scalar(F, lo: float, hi: float, n_scan: int = N_SCAN, use_wall_trials: bool = True) -> Outcome:
    """`use_wall_trials` exists only for N4's negative control (False drops the wall-location trials from the
    sign-change search, i.e. the behaviour N4 forbids). Not reachable from Body, options or the solve context.

    A refusal met by Brent inside a solved bracket is a wall like any other (r2 B3): it is located from both
    bracket ends with the wall budget, the solved trials join the search (N4) and the search is re-run."""
    assert 0.0 <= lo < hi, (lo, hi)
    trials: list = []
    xs = scan_points(lo, hi, n_scan)
    for x in xs:
        v = _value(F, x)
        trials.append(Trial(x, None, v, "scan") if isinstance(v, st.Stop) else Trial(x, v, None, "scan"))
    for n, t in enumerate(list(trials)):                 # a refusing scan point next to a solved one is confirmed
        if t.F is not None:
            continue
        nbr = [u for u in (trials[n - 1] if n > 0 else None, trials[n + 1] if n + 1 < len(xs) else None)
               if u is not None and u.F is not None]
        if nbr:
            _confirm_chain(F, t.x, t.stop, nbr[0].x, lo, hi, trials)
    walls: list = []
    done_pairs: set = set()
    closed: dict = {}            # (a.x, b.x) → root or problem
    brackets: dict = {}          # root → {"scan": (x_a, F_a, x_b, F_b), "final": Brent's last bracket or None}
    for _round in range(MAX_SPLITS + 1):
        order = sorted((t for t in trials if t.kind != "isolated"), key=lambda t: t.x)
        for a, b in zip(order, order[1:]):
            if (a.F is None) != (b.F is None) and (a.x, b.x) not in done_pairs:
                done_pairs.add((a.x, b.x))
                ok, bad = (a, b) if a.F is not None else (b, a)
                walls.append(_locate_wall(F, ok.x, bad.x, bad.stop, trials, lo, hi))
        pts = sorted((t for t in trials if t.F is not None and (use_wall_trials or t.kind != "wall")),
                     key=lambda t: t.x)
        refused = sorted(t.x for t in trials if t.F is None and t.kind != "isolated")
        roots, problems, split = [], [], False
        for a, b in zip(pts, pts[1:]):
            if any(a.x < w < b.x for w in refused):
                continue                                  # not one solved stretch
            if a.F == 0.0:
                roots.append(a.x)
                brackets[a.x] = {"scan": (a.x, a.F, b.x, b.F), "final": None}
                continue
            if a.F * b.F < 0.0:
                key = (a.x, b.x)
                if key not in closed:
                    closed[key] = _brent(F, a.x, a.F, b.x, b.F, trials)
                x, prob, final = closed[key]
                if x is not None:
                    roots.append(x)
                    brackets[x] = {"scan": (a.x, a.F, b.x, b.F), "final": final}
                elif prob[0] == "refused_inside":
                    split = True
                    _confirm_chain(F, prob[1], prob[2], a.x, lo, hi, trials)   # impl note 8
                else:
                    problems.append(prob)
        if pts and pts[-1].F == 0.0:
            roots.append(pts[-1].x)
            if len(pts) > 1:
                brackets[pts[-1].x] = {"scan": (pts[-2].x, pts[-2].F, pts[-1].x, pts[-1].F), "final": None}
        if not split:
            break
    else:
        return Outcome("unconverged", roots=roots, walls=walls, trials=trials,
                       detail={"budget": "MAX_SPLITS", "lo": lo, "hi": hi, "n_scan": n_scan})
    if not pts:
        return Outcome("no_solved", walls=walls, trials=trials)
    detail = {"problems": problems, "lo": lo, "hi": hi, "n_scan": n_scan, "brackets": brackets}
    if len(roots) == 1 and not problems:
        return Outcome("root", roots=roots, walls=walls, trials=trials, detail=detail)
    if len(roots) >= 2:
        return Outcome("two_roots", roots=roots, walls=walls, trials=trials, detail=detail)
    if problems:
        return Outcome("unconverged", roots=roots, walls=walls, trials=trials, detail=detail)
    return Outcome("no_bracket", roots=roots, walls=walls, trials=trials, detail=detail)
