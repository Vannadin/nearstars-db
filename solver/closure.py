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
WALL_TOL_COARSE = 1e-3       # phase-1 note 15 §1: first location; WALL_TOL only where the outcome reads the wall
SCREEN_K = 10.0              # note 15 §1: a root may hide beside a wall when |F| ≤ K·|s|·gap (2873.8 K's wall: 5.6)
WALL_SHOTS = 24
CLOSE_TOL = 1e-12
CLOSE_ITERS = 100            # Brent iterations per root (fixed by the S2 dated line)
# The noise stop (stage-A registration prereg-k8-stop, frozen 3ea24b5d; directing 10-18): F near a root is jagged at its
# walk's resolution σ_F, 10–10 000× above CLOSE_TOL·|x|, and below it Brent bisects noise. With s0 the secant of the
# bracket Brent is handed (only when that bracket is ≥ NOISE_STOP_MIN_WIDTH·|x| wide: a hair-wide pair's secant is
# itself noise, phase-1 note 10), Brent stops and returns b once |F_b| > NOISE_STOP_K·s0·|m|. On a smooth F that needs
# a local slope > K/2 = 4·s0 (measured 0.87–0.89); in the noise band it fires once |m| < σ_F/(K·s0).
NOISE_STOP_K = 8.0
NOISE_STOP_MIN_WIDTH = 1e-6
# the registration's curvature watch: a firing whose noise-free local slope (the narrowest bracket of the call still
# ≥ NOISE_STOP_MIN_WIDTH·|x| wide) is ≥ CURVATURE_WATCH·s0 is named in its log entry
CURVATURE_WATCH = 3.5
# A1 impl note 8 (directing, 2026-10-10): a refusing shot is a wall only when confirmed by a second shot a little
# further from the solved side (CONFIRM_FRAC of the gap, at least CONFIRM_MIN·|x|). If that shot solves, the refusal
# is isolated (e.g. one unlanded event at Earth 2064.76 K, x = 6437400.24 m): recorded as kind "isolated", never a
# wall, and the solved shot joins the search.
CONFIRM_FRAC = 0.01
CONFIRM_MIN = 1e-9
CONFIRM_MAX = 4              # confirming shots per refusal chain (r2 on d031605b: the reason must match)


#: A gap between two adjacent refusing scan points is shot when they refused in one material at P a factor GAP_RATIO
#: apart (opposite_walls):
#: one trial went too deep and the next too shallow for a material's range, so the x between them may solve (mars
#: O9 2350–2850 K: R 3584 km refused at the core fit's 350 GPa top and 3685 km under its 11.93 GPa turning point,
#: and every answer lies at 3599–3664 km between them; the 17-point scan had no solved point). Log-midpoints, keeping
#: the half whose ends are still GAP_RATIO apart, at most GAP_SHOTS per gap.
GAP_RATIO = 2.0
GAP_SHOTS = 6


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
    kind: str                    # "scan" | "wall" | "brent" | "confirm" | "isolated" | "gap"


@dataclass(frozen=True)
class Wall:
    x: float                     # the located wall (first refusing x next to a solved one)
    stop: st.Stop
    solved_side: float           # the nearest solved x
    located: bool = True         # False when WALL_SHOTS ran out before `tol` (NoAnswer budget WALL_SHOTS)
    tol: float = WALL_TOL        # note 15 §1 (r2 H1): the tolerance this wall was located to; `located` is judged on it


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


def _brent(F, a: float, fa: float, b: float, fb: float, trials: list, lo: float = -math.inf, hi: float = math.inf,
           confirm: bool = True, noise_log: list | None = None):
    """Brent's method (zeroin) on a bracket with fa·fb < 0, to |Δx| ≤ CLOSE_TOL·|x|, or to F's noise (the noise stop,
    NOISE_STOP_K above). Bisection fallback guarantees shrink. A refusing evaluation inside a solved bracket is
    reported (it splits the bracket). Returns (root, None, final bracket (x_b, F_b, x_c, F_c)) or (None, problem, None);
    the final bracket names where a jump would sit (phase-1 design note 8). A noise stop appends its entry to
    `noise_log` when one is given."""
    width0 = abs(b - a)
    s0 = abs(fb - fa) / width0 if width0 >= NOISE_STOP_MIN_WIDTH * max(abs(a), abs(b)) and width0 > 0.0 else None
    s_loc = s0                   # the secant of the narrowest bracket still ≥ NOISE_STOP_MIN_WIDTH·|x| (noise-free)
    c, fc = a, fa
    d = e = b - a
    isolated = set()             # G2-C-01: x where a landing failed and its confirming shot solved
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
        if s0 is not None:
            if abs(c - b) >= NOISE_STOP_MIN_WIDTH * abs(b):
                s_loc = abs(fc - fb) / abs(c - b)
            if abs(fb) > NOISE_STOP_K * s0 * abs(m):          # the noise stop
                if noise_log is not None:
                    ratio = s_loc / s0 if s0 > 0.0 else float("inf")
                    noise_log.append({"x": b, "F_b": fb, "m": m, "s0": s0, "s_loc": s_loc, "ratio": ratio,
                                      "named": ratio >= CURVATURE_WATCH})
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
        if b in isolated:
            # Brent came back to an isolated point: it sits at the bracket's resolution, so the better end is the
            # root; the closure guard (note 8 (a)) judges its residual like any other root
            x_best, f_best = (a, fa) if abs(fa) <= abs(fc) else (c, fc)
            return x_best, None, (a, fa, c, fc)
        v = _value(F, b)
        if isinstance(v, st.Stop):
            trials.append(Trial(b, None, v, "brent"))
            if not confirm:              # refine (note 15a): any refusal falls back to the full procedure
                return None, ("refused_inside", b, v), None
            # G2-C-01: confirm here (impl note 8). A solved confirming shot isolates b, and Brent goes on from that shot
            # (kept as a Brent trial, out of the sign search); only a confirmed refusal splits the bracket
            what, xc, vc = _confirm_chain(F, b, v, a, lo, hi, trials)
            if what == "wall":
                return None, ("refused_inside", xc, vc), None
            isolated.add(b)
            for n in range(len(trials) - 1, -1, -1):
                if trials[n].x == xc and trials[n].kind == "confirm":
                    trials[n] = Trial(xc, vc, None, "brent")
                    break
            b, v = xc, vc
        else:
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


def _locate_wall(F, x_ok: float, x_bad: float, stop_bad: st.Stop, trials: list, lo: float, hi: float,
                 tol: float = WALL_TOL) -> Wall:
    for _ in range(WALL_SHOTS):
        if abs(x_bad - x_ok) <= tol * max(abs(x_ok), abs(x_bad)):
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
    return Wall(x_bad, stop_bad, x_ok, abs(x_bad - x_ok) <= tol * max(abs(x_ok), abs(x_bad)), tol)


def refine(F, x0: float, lo: float, hi: float, h_rel: float = 1e-4, tries: int = 6):
    """Phase-1 note 15 §2 (as amended by note 15a): the root of a small shift of a function already solved at x0.
    F(x0) and F(x0 + h_rel·|x0|) give the slope (one extra pass: the first solve's own pairs can sit inside F's
    jitter, 4 µm wide on Earth); a pair that already brackets goes to Brent, else a Newton-sized step (×1.5) from x0
    and ×4 widenings until F changes sign, then Brent. Trials: x0, x1 and the widenings as «scan», Brent's as «brent»;
    brackets[root]["scan"] is the sign-change pair, so the closure guard reads s, the δ cap and its references from
    this run (r2 H2). None when anything refuses or no sign change comes within `tries`: the caller falls back."""
    trials: list = []
    f0 = _value(F, x0)
    if isinstance(f0, st.Stop):
        return None
    trials.append(Trial(x0, f0, None, "scan"))
    x1 = min(max(x0 + h_rel * abs(x0), lo), hi)
    if x1 == x0:
        return None
    f1 = _value(F, x1)
    if isinstance(f1, st.Stop):
        return None
    trials.append(Trial(x1, f1, None, "scan"))

    def root_at(a, fa, b, fb):
        if a > b:
            a, fa, b, fb = b, fb, a, fa
        noise: list = []
        x, prob, final = (a, None, None) if fa == 0.0 else (b, None, None) if fb == 0.0 else \
            _brent(F, a, fa, b, fb, trials, confirm=False, noise_log=noise)
        if x is None:
            return None
        return Outcome("root", roots=[x], walls=[], trials=trials,
                       detail={"problems": [], "lo": lo, "hi": hi, "n_scan": len(trials),
                               "brackets": {x: {"scan": (a, fa, b, fb), "final": final}}, "noise_stops": noise})
    if f0 * f1 <= 0.0:
        return root_at(x0, f0, x1, f1)
    s = (f1 - f0) / (x1 - x0)
    if s == 0.0:
        return None
    dx = -1.5 * f0 / s
    for _ in range(tries):
        xk = min(max(x0 + dx, lo), hi)
        fk = _value(F, xk)
        if isinstance(fk, st.Stop):
            return None
        trials.append(Trial(xk, fk, None, "scan"))
        if f0 * fk <= 0.0:
            return root_at(x0, f0, xk, fk)
        dx *= 4.0
    return None


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
    _gap_shots(F, trials, lo, hi)
    walls: list = []
    done_pairs: set = set()
    closed: dict = {}            # (a.x, b.x) → root or problem
    brackets: dict = {}          # root → {"scan": (x_a, F_a, x_b, F_b), "final": Brent's last bracket or None}
    # phase-1 note 15 §1: walls are located coarse first; a wall is refined to WALL_TOL (and the search run again with
    # the new trials, N4) when the outcome reads it (any outcome but one root) or a root may hide beside it
    noise: list = []             # the noise stop's log (prereg-k8-stop): one entry per firing Brent call
    out = _rounds(F, lo, hi, n_scan, trials, walls, done_pairs, closed, brackets, use_wall_trials, WALL_TOL_COARSE,
                  noise)
    hide = [w for w in walls if out.kind != "root" or _root_may_hide(w, trials)]
    if not hide:
        return out
    walls[:] = [_locate_wall(F, w.solved_side, w.x, w.stop, trials, lo, hi) if w in hide else w for w in walls]
    order = sorted((t for t in trials if t.kind != "isolated"), key=lambda t: t.x)
    for a, b in zip(order, order[1:]):                   # the refined walls' own pairs: not new walls
        if (a.F is None) != (b.F is None):
            done_pairs.add((a.x, b.x))
    return _rounds(F, lo, hi, n_scan, trials, walls, done_pairs, closed, brackets, use_wall_trials, WALL_TOL, noise)


def _refusal_p(stop) -> float | None:
    """The pressure a refusing trial refused at (the innermost record carrying one), or None."""
    r = stop
    for _ in range(6):
        p = r.get("p") if isinstance(r, dict) else getattr(r, "p", None)
        if isinstance(p, (int, float)) and not isinstance(p, bool) and p > 0.0:
            return float(p)
        r = r.get("record") if isinstance(r, dict) else getattr(r, "record", None)
        if r is None:
            return None
    return None


def _refusal_material(stop):
    """The material a refusing trial refused in (the innermost record naming one), or None."""
    r = stop
    for _ in range(6):
        mid = r.get("material_id") if isinstance(r, dict) else getattr(r, "material_id", None)
        if mid is not None:
            return mid
        r = r.get("record") if isinstance(r, dict) else getattr(r, "record", None)
        if r is None:
            return None
    return None


def opposite_walls(sa, sb) -> bool:
    """Two refusals on opposite sides of one material's range: the same material (or none named in either), refusing
    P a factor GAP_RATIO apart. Two materials refusing at different P are both one side's (mars 2850 K: the basal
    layer at 131 GPa and the core at 350 GPa, both too deep)."""
    pa, pb = _refusal_p(sa), _refusal_p(sb)
    return (pa is not None and pb is not None and max(pa, pb) >= GAP_RATIO * min(pa, pb)
            and _refusal_material(sa) == _refusal_material(sb))


def _gap_shots(F, trials: list, lo: float, hi: float):
    """Shoot the gaps between adjacent refusing scan points that refused on opposite sides of a range (GAP_RATIO).
    Every shot joins the trials (kind "gap"): a solved one opens the stretch the rounds search, a refusing one is a
    wall like any scan point's."""
    order = sorted((t for t in trials if t.kind == "scan"), key=lambda t: t.x)
    for a, b in zip(order, order[1:]):
        if a.F is not None or b.F is not None:
            continue
        if not opposite_walls(a.stop, b.stop):
            continue
        xa, xb, sa, sb = a.x, b.x, a.stop, b.stop
        for _ in range(GAP_SHOTS):
            xm = math.sqrt(xa * xb) if xa > 0.0 else 0.5 * (xa + xb)
            v = _value(F, xm)
            if not isinstance(v, st.Stop):
                trials.append(Trial(xm, v, None, "gap"))
                break
            trials.append(Trial(xm, None, v, "gap"))
            if opposite_walls(sa, v):
                xb, sb = xm, v
            elif opposite_walls(v, sb):
                xa, sa = xm, v
            else:
                break


def _root_may_hide(w, trials) -> bool:
    """Note 15 §1's screen: at the solved trial nearest the wall (on its solved side), |F| ≤ SCREEN_K·|s|·gap, s the
    slope of the two nearest solved trials there, gap the distance to the wall's refusing x. Fewer than two solved
    trials on that side: refine."""
    side = 1.0 if w.x > w.solved_side else -1.0
    solved = sorted((t for t in trials if t.F is not None and (t.x - w.x) * side < 0.0), key=lambda t: abs(t.x - w.x))
    if len(solved) < 2:
        return True
    a, b = solved[0], solved[1]
    s = abs(a.F - b.F) / abs(a.x - b.x) if a.x != b.x else math.inf
    return abs(a.F) <= SCREEN_K * s * abs(w.x - a.x)


def _rounds(F, lo, hi, n_scan, trials, walls, done_pairs, closed, brackets, use_wall_trials, wall_tol,
            noise_log=None):
    for _round in range(MAX_SPLITS + 1):
        order = sorted((t for t in trials if t.kind != "isolated"), key=lambda t: t.x)
        for a, b in zip(order, order[1:]):
            if (a.F is None) != (b.F is None) and (a.x, b.x) not in done_pairs:
                done_pairs.add((a.x, b.x))
                ok, bad = (a, b) if a.F is not None else (b, a)
                wl = _locate_wall(F, ok.x, bad.x, bad.stop, trials, lo, hi, wall_tol)
                if all(w.x != wl.x for w in walls):       # P1R-G2-C-10: a located wall's own pair re-finds it
                    walls.append(wl)
        # G2-C-02: Brent's own trials sit inside F's jitter band near a root; they never open a new bracket
        pts = sorted((t for t in trials if t.F is not None and t.kind != "brent"
                      and (use_wall_trials or t.kind != "wall")), key=lambda t: t.x)
        refused = sorted(t.x for t in trials if t.F is None and t.kind != "isolated")
        roots, problems, split = [], [], False
        for a, b in zip(pts, pts[1:]):
            if a.F == 0.0:                                # P1R-G2-C-14: an exact zero is a root even beside a wall
                roots.append(a.x)
                brackets[a.x] = {"scan": (a.x, a.F, b.x, b.F), "final": None}
                continue
            if any(a.x < w < b.x for w in refused):
                continue                                  # not one solved stretch
            if a.F * b.F < 0.0:
                key = (a.x, b.x)
                if key not in closed:
                    closed[key] = _brent(F, a.x, a.F, b.x, b.F, trials, lo, hi, noise_log=noise_log)
                x, prob, final = closed[key]
                if x is not None:
                    roots.append(x)
                    brackets[x] = {"scan": (a.x, a.F, b.x, b.F), "final": final}
                elif prob[0] == "refused_inside":
                    split = True                          # confirmed inside _brent: a wall, located next round
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
    detail = {"problems": problems, "lo": lo, "hi": hi, "n_scan": n_scan, "brackets": brackets,
              "noise_stops": noise_log if noise_log is not None else []}
    if len(roots) == 1 and not problems:
        return Outcome("root", roots=roots, walls=walls, trials=trials, detail=detail)
    if len(roots) >= 2:
        return Outcome("two_roots", roots=roots, walls=walls, trials=trials, detail=detail)
    if problems:
        return Outcome("unconverged", roots=roots, walls=walls, trials=trials, detail=detail)
    return Outcome("no_bracket", roots=roots, walls=walls, trials=trials, detail=detail)
