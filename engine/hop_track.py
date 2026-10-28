# 도약을 막는 δ_u·δ_b 추적기(D2 §7 의 (D)) — fold_track 산술을 다시 구현하고 NaN 안전 이분법·잔차 확인·이웃 진입 막기·되돌리기를 담음, ALE 열역사 방식(thermal_ale)이 씀
"""The hop-safe tracker (D) of the D2 redesign note §7 (artifacts review2-fix-c8 c8c7472c), used by `thermal_ale`.

From the cleared prototype hoptrack.py (58d7dc3f; pre-run statement eb16d490 §2, amendment A1 on), plus 68's carry-over:
guard (a)'s neighbour bracket stays on the neighbour's side of the midpoint between the tracked root and the neighbour
(as fold_track's `_continue_neighbour`); OPT["guard_a_clip"] = False restores the old bracket for the plant only.

fold_track's continuation arithmetic is re-implemented here (fold_track supplies only its constants and its
Root / Track / Lost data classes), with three switches in `OPT`:
- `nan_safe`: a NaN met inside a bisection returns «no root», never a sign;
- `residual`: a root is accepted only if |f| ≤ EPS_ROOT_M at it;
- `guard`:    the neighbour-entry guard — (a) a carried neighbour inside the root's bracket, (b) the adopted root
  nearer the neighbour's prediction (nb + Δnb) than its own (x + Δx) — rejects the trial.
With all three off the arithmetic is fold_track's, call for call (NC0 checks that on T2's default run).
`install()` puts `continued` / `track_at` in place of thermal_stack's for the duration of a `with` block only."""
from __future__ import annotations

import contextlib
import copy
import math

import fold_track as ft
import samuel_model as sm
import thermal_stack as ts

EPS_ROOT_M = 1.0e-3        # §2: 1e-6 × FLOOR_M; T2 default max true residual 1.1e-7 m (resid.py), false root 1033 m
OPT = {"nan_safe": True, "residual": True, "guard": True, "scaled": True, "guard_a_clip": True}
#: amendment A1 (forced by NC4, cleared by 68 10-23, ON for every counted rung): the guard's predictions x + Δx·ρ,
#: ρ = h_trial / h_last
STEP = {"ratio": 1.0, "h_last": None, "c": 1.0}
#: f3 (10-24): the evaluated state's time fraction within the trial step (thermal_ale sets it per ARS stage: 0 at the
#: step start and at accept, γ at stage 2, 1 at the end). The guard predicts x + Δx·ρ·c; T2's paths leave c = 1.
STATS: dict = {}


def reset_stats() -> None:
    STATS.clear()
    STATS.update(bisections=0, nan_seen=0, nan_returned_none=0, residual_checked=0, residual_fail=0,
                 residual_max_accepted=0.0, guard_trips=0, guard_log=[], margin_min={"δ_u": None, "δ_b": None},
                 margin_at={"δ_u": None, "δ_b": None})


reset_stats()


def changes_sign(fa: float, fb: float) -> bool:
    return not (math.isnan(fa) or math.isnan(fb)) and (fa > 0) != (fb > 0)


def bisect(f, a: float, b: float, fa: float):
    """fold_track.bisect's arithmetic. With `nan_safe`, a NaN evaluation ends it with None."""
    STATS["bisections"] += 1
    seen = False
    for _ in range(ft.BISECT_ITERS):
        m = 0.5 * (a + b)
        fm = f(m)
        if math.isnan(fm):
            seen = True
            if OPT["nan_safe"]:
                STATS["nan_seen"] += 1
                STATS["nan_returned_none"] += 1
                return None
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
    if seen:
        STATS["nan_seen"] += 1
    return 0.5 * (a + b)


def checked(f, x):
    """The residual check: x, or None when |f(x)| > EPS_ROOT_M (or NaN). Off: x unchanged."""
    if x is None or not OPT["residual"]:
        return x
    v = f(x)
    STATS["residual_checked"] += 1
    if math.isnan(v) or abs(v) > EPS_ROOT_M:
        STATS["residual_fail"] += 1
        return None
    STATS["residual_max_accepted"] = max(STATS["residual_max_accepted"], abs(v))
    return x


def root_in(f, a, b, fa):
    return checked(f, bisect(f, a, b, fa))


def half_width(r: ft.Root) -> float:
    w = max(ft.K_BRACKET * abs(r.dx), ft.FLOOR_M)
    gaps = [r.x - r.lo] if r.lo is not None else []
    if r.hi is not None:
        gaps.append(r.hi - r.x)
    if gaps:
        w = min(w, 0.5 * min(gaps))
    return w


def local_root(h, r: ft.Root, lo: float, hi: float):
    w = half_width(r)
    a, b = max(lo, r.x - w), min(hi, r.x + w)
    if not a < b:
        return None
    fa, fb = h(a), h(b)
    if not changes_sign(fa, fb):
        return None
    return root_in(h, a, b, fa)


def scan(h, lo: float, hi: float, n: int) -> list:
    roots, a, fa = [], lo, h(lo)
    for k in range(1, n + 1):
        b = lo + (hi - lo) * k / n
        fb = h(b)
        if changes_sign(fa, fb):
            x = root_in(h, a, b, fa)
            if x is not None:
                roots.append(x)
        a, fa = b, fb
    return roots


def _move_scale() -> float:
    """The predicted-move factor for a continuation: ρ·c in the ALE mode (thermal_ale sets STEP['ale']), 1 on T2's
    paths, whose arithmetic stays fold_track's (r2 h2: T2 + (D) keeps c = 1 — not fixed there, recorded only)."""
    return STEP["ratio"] * STEP.get("c", 1.0) if (STEP.get("ale") and OPT["scaled"]) else 1.0


def carried_root(h, r: ft.Root, lo: float, hi: float, reach: int = ft.NEIGHBOUR_CELLS, log: list | None = None):
    got = local_root(h, r, lo, hi)
    if got is not None:
        return got
    cell = (hi - lo) / ft.FULL_SCAN
    a_lim = max(lo, r.x - (0.5 * (r.x - r.lo) if r.lo is not None else reach * cell))
    b_lim = min(hi, r.x + (0.5 * (r.hi - r.x) if r.hi is not None else reach * cell))
    w = half_width(r)
    while True:
        w *= 2.0
        a, b = max(a_lim, r.x - w), min(b_lim, r.x + w)
        if not a < b:
            return None
        fa, fb = h(a), h(b)
        if changes_sign(fa, fb):
            roots = scan(h, a, b, ft.FULL_SCAN)
            if not roots:
                return None
            want = r.x + r.dx * _move_scale()      # 68 (l.141): the prediction at this evaluation's time fraction
            got = min(roots, key=lambda z: (abs(z - want), -z))
            if log is not None:
                log.append((r.x, want, got, len(roots)))
            return got
        if a <= a_lim and b >= b_lim:
            return None


def hump(h, a: float, b: float, sign: float) -> tuple:
    lo, hi = min(a, b), max(a, b)
    c, d = hi - ft._PHI * (hi - lo), lo + ft._PHI * (hi - lo)
    fc, fd = sign * h(c), sign * h(d)
    for _ in range(ft.GOLDEN_ITERS):
        if fc > fd:
            hi, d, fd = d, c, fc
            c = hi - ft._PHI * (hi - lo)
            fc = sign * h(c)
        else:
            lo, c, fc = c, d, fd
            d = lo + ft._PHI * (hi - lo)
            fd = sign * h(d)
    x = 0.5 * (lo + hi)
    return x, h(x)


def hump_sign(h, r: ft.Root) -> float:
    nb = r.ahead()
    if nb is None:
        return 0.0
    return 1.0 if h(0.5 * (r.x + nb)) > 0 else -1.0


def lost(h, r: ft.Root, equation: str) -> ft.Lost:
    """A fold only on a hump flip toward the neighbour ahead, judged on finite values; anything else left the bracket."""
    nb = r.ahead()
    if nb is None or r.g == 0.0:
        return ft.Lost(equation, False)
    seen = []

    def hn(x):
        v = h(x)
        if math.isnan(v):
            seen.append(x)
        return v
    _, g_now = hump(hn, r.x, nb, r.g)
    if seen or math.isnan(g_now):
        return ft.Lost(equation, False)
    return ft.Lost(equation, r.g * g_now <= 0.0)


def neighbours(h, x: float, lo: float, hi: float, reach: int = ft.NEIGHBOUR_CELLS) -> tuple:
    cell = (hi - lo) / ft.FULL_SCAN
    out = []
    for step in (-cell, cell):
        found = None
        a = x + 0.5 * step
        if lo <= a <= hi:
            fa = h(a)
            for _ in range(reach):
                b = a + step
                if not lo <= b <= hi:
                    break
                fb = h(b)
                if changes_sign(fa, fb):
                    found = root_in(h, min(a, b), max(a, b), fa if a < b else fb)
                    break
                a, fa = b, fb
        out.append(found)
    return out[0], out[1]


def _continue_neighbour(h, nb, dnb: float, x: float, side: float, lo: float, hi: float):
    if nb is None:
        return None
    w = min(max(ft.K_BRACKET * abs(dnb), ft.FLOOR_M), 0.5 * abs(nb - x))
    a, b = nb - w, nb + w
    if side > 0:
        a = max(a, x + 0.5 * abs(nb - x))
    else:
        b = min(b, x - 0.5 * abs(nb - x))
    a, b = max(a, lo), min(b, hi)
    if not a < b:
        return None
    fa, fb = h(a), h(b)
    if not changes_sign(fa, fb):
        return None
    return root_in(h, a, b, fa)


def accept(h, prev: ft.Root | None, x: float, lo: float, hi: float, reach: int = ft.NEIGHBOUR_CELLS) -> ft.Root:
    if prev is None:
        r = ft.Root(x)
        r.lo, r.hi = neighbours(h, x, lo, hi, reach)
    else:
        r = ft.Root(x, x - prev.x)
        r.lo = _continue_neighbour(h, prev.lo, prev.dlo, x, -1.0, lo, hi)
        r.hi = _continue_neighbour(h, prev.hi, prev.dhi, x, 1.0, lo, hi)
        if r.lo is None or r.hi is None:
            nlo, nhi = neighbours(h, x, lo, hi, reach)
            r.lo = r.lo if r.lo is not None else nlo
            r.hi = r.hi if r.hi is not None else nhi
        r.dlo = r.lo - prev.lo if (r.lo is not None and prev.lo is not None) else 0.0
        r.dhi = r.hi - prev.hi if (r.hi is not None and prev.hi is not None) else 0.0
    r.g = hump_sign(h, r)
    return r


def pair_closing(r: ft.Root) -> bool:
    nb = r.ahead()
    return nb is not None and abs(nb - r.x) <= 2.0 * max(ft.K_BRACKET * abs(r.dx), ft.FLOOR_M)


def _guard(h, r: ft.Root, x_new: float, lo: float, hi: float, equation: str) -> None:
    """(a) a neighbour continued in its own bracket lands inside [x − w, x + w]; (b) x_new nearer a neighbour's
    prediction than the root's own. Either rejects the trial as «left the bracket»."""
    if not OPT["guard"]:
        return
    w = half_width(r)
    rho = (STEP["ratio"] if OPT["scaled"] else 1.0) * STEP.get("c", 1.0)
    own = abs(x_new - (r.x + r.dx * rho))
    for nb, dnb in ((r.lo, r.dlo), (r.hi, r.dhi)):
        if nb is None:
            continue
        why = None
        if abs(x_new - (nb + dnb * rho)) < own:
            why = "b"
        else:
            wn = min(max(ft.K_BRACKET * abs(dnb), ft.FLOOR_M), 0.5 * abs(nb - r.x))
            c = nb + dnb * rho
            a, b = max(lo, c - wn), min(hi, c + wn)
            if OPT["guard_a_clip"]:                      # 68: the neighbour's bracket stays on its side of the midpoint
                mid = 0.5 * (r.x + nb)
                if nb < r.x:
                    b = min(b, mid)
                else:
                    a = max(a, mid)
            if a < b:
                fa, fb = h(a), h(b)
                if changes_sign(fa, fb):
                    z = bisect(h, a, b, fa)
                    if z is not None and r.x - w <= z <= r.x + w:
                        why = "a"
        if why:
            STATS["guard_trips"] += 1
            if len(STATS["guard_log"]) < 200:
                STATS["guard_log"].append((equation, why, r.x, r.dx, nb, dnb, x_new))
            raise ft.Lost(equation, False)


def continued(s, layers, r_l: float, r_c: float, tr: ft.Track):
    """thermal_stack._continued with this module's arithmetic and the guard on both adopted roots."""
    def hb(du):
        return lambda db: layers(du, db)[1]["delta_b"] - db

    def inner(du):
        return carried_root(hb(du), tr.b, 0.0, max(r_l - du - r_c, 1.0), log=s.carries)

    def outer(du):
        db = inner(du)
        return math.nan if db is None else layers(du, db)[0]["delta_u"] - du

    d_u = local_root(outer, tr.u, 0.0, r_l - r_c)
    if d_u is None:
        if inner(tr.u.x) is None:
            raise lost(hb(tr.u.x), tr.b, "δ_b")
        raise lost(outer, tr.u, "δ_u")
    d_b = inner(d_u)
    if d_b is None:
        raise lost(hb(d_u), tr.b, "δ_b")
    if OPT["residual"]:
        if checked(hb(d_u), d_b) is None:
            raise ft.Lost("δ_b", False)
    _guard(hb(d_u), tr.b, d_b, 0.0, max(r_l - d_u - r_c, 1.0), "δ_b")
    _guard(outer, tr.u, d_u, 0.0, r_l - r_c, "δ_u")
    return d_u, d_b


def _margin(prev: ft.Root, r: ft.Root, equation: str, t_gyr) -> None:
    """(w − max(|Δ tracked|, neighbour move toward)) / w over the step that ends at this accepted state."""
    if prev is None or (prev.lo is None and prev.hi is None):
        return
    w = half_width(prev)
    moves = [abs(r.x - prev.x)]
    if prev.lo is not None and r.lo is not None:
        moves.append(r.lo - prev.lo)
    if prev.hi is not None and r.hi is not None:
        moves.append(prev.hi - r.hi)
    m = (w - max(moves)) / w
    if STATS["margin_min"][equation] is None or m < STATS["margin_min"][equation]:
        STATS["margin_min"][equation] = m
        STATS["margin_at"][equation] = t_gyr


def track_at(s, t_c: float, t_m: float, d_l: float, t_l: float, prev: ft.Track | None, d_u: float, d_b: float):
    """thermal_stack.track_at with this module's accept, plus the bracket margins."""
    layers = ts._layers_fn(s, t_c, t_m, d_l, t_l)
    r_l, r_c = s.r_p - d_l, s.r_base
    hb = lambda db: layers(d_u, db)[1]["delta_b"] - db  # noqa: E731
    b = accept(hb, None if prev is None else prev.b, d_b, 0.0, max(r_l - d_u - r_c, 1.0))

    def outer(du):
        db = carried_root(lambda x: layers(du, x)[1]["delta_b"] - x, b, 0.0, max(r_l - du - r_c, 1.0),
                          log=s.carries)
        return math.nan if db is None else layers(du, db)[0]["delta_u"] - du
    c_in = STEP.get("c", 1.0)
    STEP["c"] = 0.0                               # r2 aa2b6ec6: b is this state's own root (no predicted move)
    try:
        u = accept(outer, None if prev is None else prev.u, d_u, 0.0, r_l - r_c, reach=ft.OUTER_NEIGHBOUR_CELLS)
    finally:
        STEP["c"] = c_in
    t_now = s._rows[-1]["t"] if getattr(s, "_rows", None) else None
    if prev is not None:
        _margin(prev.b, b, "δ_b", t_now)
        _margin(prev.u, u, "δ_u", t_now)
    return ft.Track(u, b)


def _ft_advance(step, y, t_gyr, h_s, gyr_s):
    """For thermal_stack.run under install(): fold_track.advance's own control, each trial setting the step ratio,
    the kept step recorded as h_last."""
    def st(y0, t0, hh):
        STEP["ratio"] = hh / STEP["h_last"] if STEP["h_last"] else 1.0
        return step(y0, t0, hh)
    out = _REAL_ADVANCE(st, y, t_gyr, h_s, gyr_s)
    if out[1] > 0.0:
        STEP["h_last"] = out[1]
    return out


_REAL_ADVANCE = ft.advance


@contextlib.contextmanager
def install():
    """thermal_stack's `_continued` / `track_at` → this module's (and fold_track.advance wrapped for the step ratio),
    for the `with` block only."""
    saved = ts._continued, ts.track_at, ft.advance
    saved_step = dict(STEP)
    ts._continued, ts.track_at, ft.advance = continued, track_at, _ft_advance
    STEP.update(ratio=1.0, h_last=None, c=1.0)
    try:
        yield
    finally:
        ts._continued, ts.track_at, ft.advance = saved
        STEP.clear()
        STEP.update(saved_step)                   # r2 n1: the step state is restored on exit too


def snapshot(s) -> tuple:
    """The run state a trial can touch (the rollback of §2)."""
    return (copy.deepcopy(s.track), s.fixed_point_start, s.layer_t_i, s.layer_q, s.last_root_count, len(s.carries),
            dict(STEP), copy.deepcopy(getattr(s, "_ale_state", None)))


def restore(s, snap: tuple) -> None:
    s.track = copy.deepcopy(snap[0])
    s.fixed_point_start, s.layer_t_i, s.layer_q, s.last_root_count = snap[1], snap[2], snap[3], snap[4]
    del s.carries[snap[5]:]
    STEP.clear()
    STEP.update(snap[6])                          # 68 condition 2: the step ratio and h_last roll back too
    if snap[7] is not None:                       # §7.3 NC5′: the ALE mode's lid / basal profiles and gradient
        s._ale_state = copy.deepcopy(snap[7])


TRACKED = ("δ_u", "δ_b")                          # the equations whose loss can mark a fold


def advance(step, y: list, t_gyr: float, h_s: float, gyr_s: float, s):
    """fold_track.advance with the run state restored before every trial."""
    snap = snapshot(s)

    def trial(hh):
        restore(s, snap)
        STEP["ratio"] = hh / STEP["h_last"] if STEP["h_last"] else 1.0
        return step(list(y), t_gyr, hh)              # each trial gets its own copy of the state (D_l included)
    h = h_s
    while True:
        try:
            return trial(h), h, None
        except ft.Lost as e:
            if not e.fold:
                h *= 0.5
                if h < ft.MIN_STEP_FRACTION * h_s:
                    restore(s, snap)
                    raise
                continue
            tol = ft.event_tolerance_s(h, gyr_s)
            lo, hi, y_lo = 0.0, h, y
            while hi - lo > tol:
                mid = 0.5 * (lo + hi)
                try:
                    y_mid = trial(mid)
                except ft.Lost as e2:
                    if e2.equation not in TRACKED:        # fix A2: a stage loss (Ḋ_l) is not the fold's side
                        restore(s, snap)
                        raise sm.Refused(f"a trial inside the {e.equation} fold bisection lost {e2.equation} "
                                         f"at t = {t_gyr + mid / gyr_s:.6f} Gyr") from e2
                    hi = mid
                else:
                    lo, y_lo = mid, y_mid
            restore(s, snap)
            e.tol_s = tol
            return y_lo, lo, e


def switch_branch(s, y: list, t_gyr: float, ev: ft.Lost, c: float = 0.0) -> None:
    """thermal_stack.switch_branch with this module's arithmetic; the full scan's result must pass the residual check.
    `c` is y's time fraction of the step that s.track's roots were carried from: 0 when y is the step start (a fold
    at h_used = 0), 1 when y is the accepted step's end (68 F1)."""
    STEP["c"] = c                                 # r2 h1 / 68 F1: the predictions move as far as y is from the track
    t_c, t_m, d_l = y[0], y[1], y[2]
    t_l = sm.lid_base_temperature(t_m, s.e_star, s.opt["a_rh"], s.opt["r_gas"])
    r_l, r_c = s.r_p - d_l, s.r_base
    layers = ts._layers_fn(s, t_c, t_m, d_l, t_l)
    tr = s.track
    d_u0, d_b0 = continued(s, layers, r_l, r_c, tr)
    dead = dead_u = None
    root = tr.b if ev.equation == "δ_b" else tr.u
    if not pair_closing(root):
        s.fold_rejected.append((t_gyr, ev.equation, root.x, root.ahead()))
    elif ev.equation == "δ_b":
        nb, cell = tr.b.ahead(), max(r_l - d_u0 - r_c, 1.0) / ft.FULL_SCAN
        dead = (min(d_b0, nb) - cell, max(d_b0, nb) + cell)
    else:
        nb, cell = tr.u.ahead(), (r_l - r_c) / ft.FULL_SCAN
        dead_u = (min(d_u0, nb) - cell, max(d_u0, nb) + cell)
    sol = ts.solve_boundary_layers(s, t_c, t_m, d_l, t_l, (d_u0, d_b0), "nearest", scan=ft.FULL_SCAN,
                                   dead=dead, dead_u=dead_u)
    if sol is None or sol[1] is None:
        raise sm.Refused(f"no branch after the fold of {ev.equation} at t = {t_gyr:.6f} Gyr")
    d_u1, d_b1, t_b1 = sol[0], sol[1], sol[5]
    if OPT["residual"]:
        fu = layers(d_u1, d_b1)[0]["delta_u"] - d_u1
        fb = layers(d_u1, d_b1)[1]["delta_b"] - d_b1
        if not (abs(fu) <= EPS_ROOT_M and abs(fb) <= EPS_ROOT_M):
            STATS["residual_fail"] += 1
            raise sm.Refused(f"branch after the fold fails the residual check at t = {t_gyr:.6f} Gyr "
                             f"(f_u {fu:.3g} m, f_b {fb:.3g} m)")
    if dead is None and dead_u is None:
        if (abs(d_u1 - d_u0) > max(ft.K_BRACKET * abs(tr.u.dx), ft.FLOOR_M)
                or abs(d_b1 - d_b0) > max(ft.K_BRACKET * abs(tr.b.dx), ft.FLOOR_M)):
            raise sm.Refused(f"fold rejected, but the continued root is gone at t = {t_gyr:.6f} Gyr")
    before, after = (d_b0, d_b1) if ev.equation == "δ_b" else (d_u0, d_u1)
    if dead is not None or dead_u is not None:
        s.fold_events.append((t_gyr, ev.equation, before, after, ev.tol_s / ts.GYR_S, t_c - t_b1))
    s.track = track_at(s, t_c, t_m, d_l, t_l, None, d_u1, d_b1)
