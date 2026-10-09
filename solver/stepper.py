# 적분 걸음 — Dormand–Prince 5(4) 내장 쌍, 적응 걸음, 사건 착지와 사건 폭주 방지 (phase-1 설계 §A1.3 · §A1.8)
"""Embedded Dormand–Prince 5(4) stepper with step control, event location and an event guard.

Frozen design: rewrite/phase1-design.frozen.md §A1.3 (events, landing), §A1.8 (stepper, event guard).
Implementation registration: rewrite/phase1-a1-impl.md, step S1.

The stepper knows nothing about planets. It integrates dy/dx = f(x, y) for a tuple y, in either direction of x,
and stops at the end point, at an event, or with a typed stop record. It never raises for a physical reason:
- `f` may return a `Stop` (e.g. a material refusal from the adapter) instead of a derivative tuple. The step is
  then rejected and h shrinks; if it still refuses at h_min, the run stops with that record (kind "refused").
- Exceptions mean bugs only (design A3).

Coefficients: Dormand & Prince 1980, J. Comput. Appl. Math. 6, 19–26, Table 2 «RK5(4)7M», as carried by
engine/interior.py:161–172 at 097a8aa3 (checked 2026-09-28 against the paper and scipy 1.13.1 RK45; the test
re-checks against scipy). B5 = b̂ (5th order, propagated), B4 = b (4th order, error pair).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction as Fr
from typing import Callable, Sequence

C = (Fr(0), Fr(1, 5), Fr(3, 10), Fr(4, 5), Fr(8, 9), Fr(1), Fr(1))
A = ((),
     (Fr(1, 5),),
     (Fr(3, 40), Fr(9, 40)),
     (Fr(44, 45), Fr(-56, 15), Fr(32, 9)),
     (Fr(19372, 6561), Fr(-25360, 2187), Fr(64448, 6561), Fr(-212, 729)),
     (Fr(9017, 3168), Fr(-355, 33), Fr(46732, 5247), Fr(49, 176), Fr(-5103, 18656)),
     (Fr(35, 384), Fr(0), Fr(500, 1113), Fr(125, 192), Fr(-2187, 6784), Fr(11, 84)))
B5 = (Fr(35, 384), Fr(0), Fr(500, 1113), Fr(125, 192), Fr(-2187, 6784), Fr(11, 84), Fr(0))
B4 = (Fr(5179, 57600), Fr(0), Fr(7571, 16695), Fr(393, 640), Fr(-92097, 339200), Fr(187, 2100), Fr(1, 40))

_C = tuple(float(c) for c in C)
_A = tuple(tuple(float(a) for a in row) for row in A)
_B5 = tuple(float(b) for b in B5)
_E = tuple(float(b5 - b4) for b5, b4 in zip(B5, B4))   # 5th − 4th order weights: err = h Σ E_i k_i

Vec = tuple


@dataclass(frozen=True)
class Stop:
    """A typed reason the integration (or one derivative evaluation) cannot go on. `kind` is a short tag;
    `record` carries the caller's payload (e.g. a refusal from the material adapter)."""
    kind: str
    record: object = None


@dataclass(frozen=True)
class Event:
    """g(x, y) = 0 is located and landed on. `scale` sets the landing tolerance |g| ≤ tol·scale.
    `terminal` events end the run; others are reported and the run continues on the new side."""
    name: str
    g: Callable[[float, Vec], float]
    scale: float = 1.0
    terminal: bool = True


@dataclass(frozen=True)
class Options:
    rtol: float
    floors: tuple                 # per-component absolute floors for the error scale
    h0: float                     # first step (signed by the run direction inside `run`)
    h_min: float                  # |h| below this at a refusing or rejected point is a stop
    h_max: float
    max_steps: int                # accepted + rejected steps per run
    event_tol: float = 1e-12      # landing: |g| ≤ event_tol · scale
    event_rewalks: int = 8        # secant re-steps per event
    event_min_progress: float = 0.0   # same event may not fire again before |x − x_event| ≥ this
    event_restarts_step: int = 4
    event_restarts_run: int = 2000


@dataclass
class Counters:
    accepted: int = 0
    rejected: int = 0
    refused_stage: int = 0
    events: int = 0
    rewalks: int = 0


@dataclass(frozen=True)
class Result:
    x: float
    y: Vec
    stop: Stop                    # kind: "end" | "event" | "refused" | "h_min" | "max_steps" | "chatter"
    event: str | None = None
    h_last: float = 0.0
    path: tuple = ()              # accepted (x, y, f(x, y)) nodes, including the start and the end point
    events: tuple = ()            # non-terminal events landed: (name, x, y)
    counters: Counters = field(default_factory=Counters)


def _axpy(y: Vec, h: float, ks: Sequence[Vec], w: Sequence[float]) -> Vec:
    n = len(y)
    return tuple(y[j] + h * sum(w[i] * ks[i][j] for i in range(len(w)) if w[i] != 0.0) for j in range(n))


def step(f, x: float, y: Vec, h: float, k1: Vec):
    """One DP5(4) step from (x, y) with first stage k1 = f(x, y). Returns (y_new, err, k7) or a Stop from f.
    k7 = f(x + h, y_new) (FSAL), reused as the next step's k1."""
    ks = [k1]
    for i in range(1, 7):
        yi = _axpy(y, h, ks, _A[i])
        k = f(x + _C[i] * h, yi)
        if isinstance(k, Stop):
            return k
        ks.append(k)
    y_new = _axpy(y, h, ks, _B5)            # equals stage 7's argument (row 7 of A = B5)
    err = tuple(h * sum(_E[i] * ks[i][j] for i in range(7)) for j in range(len(y)))
    return y_new, err, ks[6]


def err_norm(err: Vec, y0: Vec, y1: Vec, rtol: float, floors: tuple) -> float:
    return max(abs(e) / (rtol * max(abs(a), abs(b), fl)) for e, a, b, fl in zip(err, y0, y1, floors))


def next_h(h: float, en: float, accepted: bool) -> float:
    """Step-size update of the old engine (R-RK-3's form): accept → h·min(5, 0.9 en^(−1/5)),
    reject → h·max(0.2, 0.9 en^(−1/4))."""
    if en <= 0.0:
        return h * 5.0
    if accepted:
        return h * min(5.0, 0.9 * en ** -0.2)
    return h * max(0.2, 0.9 * en ** -0.25)


def _land(f, ev: Event, x: float, y: Vec, k1: Vec, s_hi: float, g0: float, opt: Options, cnt: Counters):
    """Locate g = 0 inside a step of signed length s_hi from (x, y), g(x, y) = g0, and land just past it.
    Secant/Illinois on real DP steps of length s (no interpolant), at most `event_rewalks` re-steps.
    Returns (x_e, y_e, k_e) on the new side, or a Stop."""
    lo, g_lo = 0.0, g0
    hi = s_hi
    out = step(f, x, y, hi, k1)
    if isinstance(out, Stop):
        return out
    g_hi = ev.g(x + hi, out[0])
    best = (hi, out)
    side = 0
    tol = opt.event_tol * ev.scale
    for _ in range(opt.event_rewalks):
        if abs(g_hi) <= tol and g_hi * g0 <= 0.0:
            break
        s = hi - g_hi * (hi - lo) / (g_hi - g_lo)
        if not (min(lo, hi) < s < max(lo, hi)):
            s = 0.5 * (lo + hi)
        cnt.rewalks += 1
        o = step(f, x, y, s, k1)
        if isinstance(o, Stop):
            return o
        gs = ev.g(x + s, o[0])
        if gs * g0 > 0.0:                     # still on the old side
            lo, g_lo = s, gs
            if side == -1:
                g_hi *= 0.5                    # Illinois
            side = -1
        else:
            hi, g_hi = s, gs
            best = (s, o)
            if side == 1:
                g_lo *= 0.5
            side = 1
    s, (y_e, _err, k_e) = best
    return x + s, y_e, k_e


def run(f, x0: float, y0: Vec, x1: float, opt: Options, events: Sequence[Event] = (),
        disabled_until: dict | None = None) -> Result:
    """Integrate from x0 to x1 (either direction). Stops at x1, at the first terminal event, or with a Stop."""
    cnt = Counters()
    direction = 1.0 if x1 >= x0 else -1.0
    x, y = x0, tuple(y0)
    k1 = f(x, y)
    if isinstance(k1, Stop):
        return Result(x, y, Stop("refused", k1), counters=cnt)
    h = direction * min(abs(opt.h0), opt.h_max)
    path = [(x, y, k1)]
    landed = []
    last_fire = dict(disabled_until or {})          # event name → x of its last landing
    run_events = 0
    g_prev = {ev.name: ev.g(x, y) for ev in events}

    def armed(ev, xx):
        xe = last_fire.get(ev.name)
        return xe is None or abs(xx - xe) >= opt.event_min_progress

    while True:
        if cnt.accepted + cnt.rejected >= opt.max_steps:
            return Result(x, y, Stop("max_steps", opt.max_steps), h_last=h, path=tuple(path),
                          events=tuple(landed), counters=cnt)
        if direction * (x + h - x1) > 0.0:
            h = x1 - x
        out = step(f, x, y, h, k1)
        if isinstance(out, Stop):
            cnt.refused_stage += 1
            if abs(h) <= opt.h_min:
                return Result(x, y, Stop("refused", out), h_last=h, path=tuple(path),
                              events=tuple(landed), counters=cnt)
            h = direction * max(abs(h) * 0.25, opt.h_min)
            continue
        y_new, err, k7 = out
        en = err_norm(err, y, y_new, opt.rtol, opt.floors)
        if en > 1.0:
            cnt.rejected += 1
            if abs(h) <= opt.h_min:
                return Result(x, y, Stop("h_min", {"h": h, "err_norm": en}), h_last=h, path=tuple(path),
                              events=tuple(landed), counters=cnt)
            h = direction * max(abs(next_h(h, en, False)), opt.h_min)
            continue
        # accepted unless an armed event changes sign inside the step
        x_new = x + h
        fired = None
        restarts = 0
        for ev in events:
            if not armed(ev, x_new):
                continue
            g1 = ev.g(x_new, y_new)
            if g_prev[ev.name] * g1 < 0.0 or (g1 == 0.0 and g_prev[ev.name] != 0.0):
                fired = ev
                break
        if fired is not None:
            restarts += 1
            run_events += 1
            if restarts > opt.event_restarts_step or run_events > opt.event_restarts_run:
                return Result(x, y, Stop("chatter", {"event": fired.name, "count": run_events}), h_last=h,
                              path=tuple(path), events=tuple(landed), counters=cnt)
            got = _land(f, fired, x, y, k1, h, g_prev[fired.name], opt, cnt)
            if isinstance(got, Stop):
                return Result(x, y, Stop("refused", got), h_last=h, path=tuple(path),
                              events=tuple(landed), counters=cnt)
            x_e, y_e, k_e = got
            cnt.accepted += 1
            cnt.events += 1
            path.append((x_e, y_e, k_e))
            last_fire[fired.name] = x_e
            if fired.terminal:
                return Result(x_e, y_e, Stop("event"), event=fired.name, h_last=h, path=tuple(path),
                              events=tuple(landed), counters=cnt)
            landed.append((fired.name, x_e, y_e))
            x, y, k1 = x_e, y_e, k_e
            g_prev = {ev.name: ev.g(x, y) for ev in events}
            h = direction * min(abs(h), opt.h_max)      # controller restarts from the event with the last h
            continue
        cnt.accepted += 1
        x, y, k1 = x_new, y_new, k7
        path.append((x, y, k1))
        g_prev = {ev.name: ev.g(x, y) for ev in events}
        if direction * (x - x1) >= 0.0:
            return Result(x, y, Stop("end"), h_last=h, path=tuple(path), events=tuple(landed), counters=cnt)
        h = direction * min(max(abs(next_h(h, en, True)), opt.h_min), opt.h_max)


def dense(path: Sequence[tuple], x: float) -> Vec:
    """Dense output: cubic Hermite through the bracketing accepted nodes (y and f at both ends; 3rd order).
    Used only to report values between nodes (e.g. a merged internal boundary, design §A1.3); events are landed
    by real re-steps (`_land`), never on this interpolant."""
    lo, hi = path[0][0], path[-1][0]
    if not (min(lo, hi) <= x <= max(lo, hi)):
        raise ValueError(f"dense({x}) outside the path [{lo}, {hi}]")
    for (xa, ya, fa), (xb, yb, fb) in zip(path, path[1:]):
        if min(xa, xb) <= x <= max(xa, xb):
            h = xb - xa
            if h == 0.0:
                return ya
            t = (x - xa) / h
            h00 = (1 + 2 * t) * (1 - t) ** 2
            h10 = t * (1 - t) ** 2
            h01 = t * t * (3 - 2 * t)
            h11 = t * t * (t - 1)
            return tuple(h00 * a + h10 * h * da + h01 * b + h11 * h * db
                         for a, b, da, db in zip(ya, yb, fa, fb))
    return path[-1][1]
