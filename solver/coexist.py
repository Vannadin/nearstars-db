# 공존 구간 훅 — swap 곡선에 착지한 걸음이 T_b(P) 를 따라 읽기 자신의 s 를 보존하며 건너가게 하는 일반 객체 (reg-coexistence §2–§3, 노트 3·4)
"""The coexistence segment's stepper hook (reg-coexistence §2–§3 with post-freeze notes 3–4; Q-P3 (a)).

A `Segment` is built per cut swap curve from side-read callables, so the view stays stateless and a planted analytic
pair of sides can drive it in tests:
    s_side(side, p, t) → s | Stop      the read's s with the curve's side forced (side −1: P < P_b, +1: P > P_b)
    rho_side(side, p, t) → ρ | Stop    the read's ρ with the side forced, the ρ repair bypassed (`side_rho`)
    p_b(t) → P_b | None, t_b(p) → T | None, dpb_dt(t) → dP_b/dT      the curve, as boundary_pressure reads it
    rows_t → the curve's row T (the segment lands each, mapped to P, as a seam)
    ds_model(t) → the rows' signed delta_s at t, or None              disclosed, never carried (note 3 §2)
On the segment T = T_b(P) (algebraic, 68 B2); the lever rule on s gives the new side's fraction
    φ = (s_L − s_old) / (s_new − s_old),   1/ρ = (1 − φ)/ρ_old + φ/ρ_new,
and the exit is s_new(P, T_b(P)) = s_L: the read's own s is conserved (note 3 §2, Δs_read carried, δ = 0)."""
from __future__ import annotations

import math

from solver import rhs as rh, stepper as st


class Segment:
    """One cut swap curve's hook (stepper.Event.coexist)."""

    def __init__(self, name, s_side, rho_side, p_b, t_b, dpb_dt, rows_t=(), ds_model=None, entry_tol=1e-12):
        self.name, self.s_side, self.rho_side = name, s_side, rho_side
        self.p_b, self.t_b, self.dpb_dt = p_b, t_b, dpb_dt
        self.rows_t, self.ds_model, self.entry_tol = tuple(rows_t), ds_model, entry_tol

    # ── entry ────────────────────────────────────────────────────────────────────────────────────────────────────
    def enter(self, m, y):
        """At the landed new-side node: a CoexistToken, or a «sharp» CoexistRecord where no segment exists in the read
        (§2.2: the read's Δs and the curve's slope disagree; a zero-length segment, 68 n2) (note 4 B2″)."""
        p, t = y[1], y[3]
        pb = self.p_b(t)
        if pb is None:
            return st.CoexistRecord("sharp", {"reason": "no_curve"})
        new = 1 if p >= pb else -1
        old = -new
        s_l, s_n = self.s_side(old, p, t), self.s_side(new, p, t)
        if isinstance(s_l, st.Stop) or isinstance(s_n, st.Stop):
            return st.CoexistRecord("sharp", {"reason": "side_read_refused"})
        g0 = s_n - s_l
        if abs(g0) <= self.entry_tol * max(abs(s_l), 1.0):
            return st.CoexistRecord("sharp", {"reason": "zero_length", "ds_read": g0})
        # the exit exists along the walk (P moving away from the old side) only if g moves toward 0 there (§2.2)
        dp = new * 1e-6 * abs(p)
        t2 = self.t_b(p + dp)
        s2 = None if t2 is None else self.s_side(new, p + dp, t2)
        if s2 is None or isinstance(s2, st.Stop) or abs(s2 - s_l) >= abs(g0):
            return st.CoexistRecord("sharp", {"reason": "clapeyron_read", "ds_read": g0})
        dm = self.ds_model(t) if self.ds_model is not None else None
        tok = st.CoexistToken({"curve": self.name, "old": old, "new": new, "s_L": s_l, "ds_read": g0, "ds_model": dm,
               "delta": None if dm is None else g0 - dm, "entry": (m, p, t), "phi_range": [math.inf, -math.inf],
               "rho_jump_entry": None, "exit": None, "rho_jump_exit": None, "projection": None})
        ro = self.rho_side(old, p, t)
        if not isinstance(ro, st.Stop):
            tok["rho_old_entry"] = ro
        return tok

    # ── the segment ──────────────────────────────────────────────────────────────────────────────────────────────
    def _phi_rho(self, tok, p, t):
        s_o, s_n = self.s_side(tok["old"], p, t), self.s_side(tok["new"], p, t)
        if isinstance(s_o, st.Stop):
            return s_o
        if isinstance(s_n, st.Stop):
            return s_n
        phi = 1.0 if s_n == s_o else min(max((tok["s_L"] - s_o) / (s_n - s_o), 0.0), 1.0)
        r_o, r_n = self.rho_side(tok["old"], p, t), self.rho_side(tok["new"], p, t)
        if isinstance(r_o, st.Stop):
            return r_o
        if isinstance(r_n, st.Stop):
            return r_n
        return phi, 1.0 / ((1.0 - phi) / r_o + phi / r_n)

    def rhs(self, tok, f_mat):
        """dy/dm on the segment: make_rhs's shape at the lever-rule ρ, T = T_b(P), dT/dm = dP/dm / (dP_b/dT)."""
        def f(m, y):
            r, p = y[0], y[1]
            if r <= 0.0:
                return st.Stop("centre_crossed", {"m": m, "r": r})
            t = self.t_b(p)
            if t is None:
                return st.Stop("coexist_unfinished", {"curve": self.name, "m": m, "P": p, "T": y[3]})
            got = self._phi_rho(tok, p, t)
            if isinstance(got, st.Stop):
                return got
            phi, rho = got
            pr = tok["phi_range"]
            pr[0], pr[1] = min(pr[0], phi), max(pr[1], phi)
            drdm = 1.0 / (rh.FOUR_PI * r * r * rho)
            dpdm = -rh.G * m / (rh.FOUR_PI * r ** 4)
            dtdm = dpdm / self.dpb_dt(t)
            k = f_mat(m, (r, p, t, t) + tuple(y[4:]))       # the quadratures' own terms (I, V_p) at the segment's state
            if isinstance(k, st.Stop):
                vp = 0.0
                di = -2.0 / 3.0 * r * r
            else:
                di = k[4]
                vp = k[5] * (drdm / k[0]) if k[0] else 0.0
            return (drdm, dpdm, dtdm, dtdm, di, vp) + tuple(0.0 for _ in y[6:])
        return f

    def exit_g(self, tok):
        """g = s_new(P, T_b(P)) − s_L (the read's own new-side s back at the entry s), landed as an event."""
        def g(m, y):
            t = self.t_b(y[1])
            if t is None:
                return None
            s_n = self.s_side(tok["new"], y[1], t)
            return None if isinstance(s_n, st.Stop) else s_n - tok["s_L"]
        return g

    def exit_scale(self, tok):
        """s's own magnitude: the landing tolerance event_tol·|s_L| (~2.5e-9 J/kg/K, ~3e-9 K) sits above s's rounding
        at T_b(P); |Δs| alone (~6e-12) is below it, and Mars's first declared solve chattered at the exit."""
        return max(abs(tok["ds_read"]), abs(tok["s_L"]), 1.0)

    def row_events(self, tok):
        """The curve's row T, mapped to P, ahead of the entry: seams of the segment (dP_b/dT jumps there; §3.2)."""
        _m, p0, _t = tok["entry"]
        out = []
        for k, t_k in enumerate(self.rows_t):
            pk = self.p_b(t_k)
            if pk is not None and tok["new"] * (pk - p0) > 0.0:
                out.append(st.Event(f"coexist-row:{self.name}:{k}", (lambda m, y, pk=pk: y[1] - pk), scale=abs(pk),
                                    terminal=False, seam=True, component=1))
        return out

    def project(self, tok, y):
        """At the exit: T and T_ad onto T_b(P), one recorded projection (≤ the step tolerance)."""
        t = self.t_b(y[1])
        if t is None:
            return y
        tok["projection"] = (y[3] - t, y[2] - t)
        tok["exit"] = (y[1], t)
        rn = self.rho_side(tok["new"], y[1], t)
        if not isinstance(rn, st.Stop):
            tok["rho_new_exit"] = rn
        return (y[0], y[1], t, t) + tuple(y[4:])


class SharpOnly:
    """A cut swap with no single-valued T_b(P) (one row, or P_b not monotone in T): the sharp step, named (§2.2's
    fallback), never a silent None."""

    def __init__(self, name, reason):
        self.name, self.reason = name, reason

    def enter(self, m, y):
        return st.CoexistRecord("sharp", {"reason": self.reason})


class CutFinding:
    """A non-swap cut (a cut edge run; note 3 §3, 68 B1): no segment, T continuous; the read's δs at the crossing is
    reported as a FINDING for BA. Also a curve end (a row-step seam; note 4 S5, r2 v2) with kind «restart»."""

    def __init__(self, name, s_side, p_b, kind="finding"):
        self.name, self.s_side, self.p_b, self.kind = name, s_side, p_b, kind

    def enter(self, m, y):
        p, t = y[1], y[3]
        pb = self.p_b(t)
        side = 1 if pb is None or p >= pb else -1
        a, b = self.s_side(-side, p, t), self.s_side(side, p, t)
        if isinstance(a, st.Stop) or isinstance(b, st.Stop):
            return st.CoexistRecord(self.kind, {"ds": None, "reason": "unread"})
        return st.CoexistRecord(self.kind, {"ds": b - a})


# ── the assemblage view's side (note 4 S4), outside material_assemblage.py ─────────────────────────────────────────
# material_assemblage.py's git blob is pinned by the records' closure_terms (s-read §3.4's build-time check) and by the
# fall sets' stamp (read_blob), so these readers sit here and use the view's existing reads (s_path with `force`, and
# _read with the ρ repair bypassed as _edge_read does). Every read leaves no note, count, mark or memo on the view.

def _restore(v, n, counts, marks, memo):
    del v.notes[n:]
    v.cut_counts.clear()
    v.cut_counts.update(counts)
    v._marks, v._read_memo = marks, memo


def side_rho(v, p, t, force):
    """ρ of the read at (p, t) with `force` {curve: side}, the ρ repair bypassed (r2 B3: the fall sets were built on the
    unforced read); a Stop when the read refuses."""
    import bisect
    from solver import material_assemblage as ma
    pr = max(p, v.ps[0])
    ia = min(max(bisect.bisect_left(v.ps, pr, 1) - 1, 0), len(v.ps) - 2)
    ib = min(max(bisect.bisect_right(v.ts, t) - 1, 0), len(v.ts) - 2)
    n, counts, marks, memo = len(v.notes), dict(v.cut_counts), v._marks, v._read_memo
    v._in_bridge = True
    try:
        got = v._read(p, t, pr, ma._log(pr), ia, ib, fields=("rho",), force=force)
    except (ma._NoRead, ma.CellMissing):
        got = None
    finally:
        v._in_bridge = False
        _restore(v, n, counts, marks, memo)
    if got is None:
        return st.Stop("coexist_side_read", {"p": p, "t": t, "field": "rho"})
    if isinstance(got, st.Stop):
        return got
    r = got["rho"]
    return float(getattr(r, "v", r))


def side_s(v, p, t, force):
    """s of the read at (p, t) with `force` (the s path's value); a Stop when it refuses or its stencil is frozen."""
    n, counts, marks, memo = len(v.notes), dict(v.cut_counts), v._marks, v._read_memo
    try:
        got = v.s_path(p, t, force)
    finally:
        _restore(v, n, counts, marks, memo)
    if got is None:
        return st.Stop("coexist_side_read", {"p": p, "t": t, "field": "s", "reason": "frozen stencil"})
    if isinstance(got, st.Stop):
        return got
    return float(getattr(got, "v", got))


def curve_inverse(v, c):
    """(p_b, t_b, dpb_dt) of a cut curve as boundary_pressure reads it (P_b_ext over its rows and reach), T_b(P) by
    bisection over the curve's T domain; None where P_b is not monotone in T there (no single T_b)."""
    lo, hi = c.t0 - v._reach, c.t1 + v._reach
    ts = [lo + (hi - lo) * k / 64.0 for k in range(65)]
    good = [(t, p) for t, p in ((t, c.p_b_ext(t, v._reach)) for t in ts) if p is not None]
    if len(good) < 2:
        return None
    if len({1 if b[1] > a[1] else -1 if b[1] < a[1] else 0 for a, b in zip(good, good[1:])} - {0}) != 1:
        return None
    t_lo, t_hi = good[0][0], good[-1][0]

    def p_b(t):
        return c.p_b_ext(t, v._reach)

    def t_b(p):
        a, b = t_lo, t_hi
        pa, pb_ = p_b(a), p_b(b)
        if pa is None or pb_ is None or (pa - p) * (pb_ - p) > 0.0:
            return None
        for _ in range(200):
            mid = 0.5 * (a + b)
            pm = p_b(mid)
            if pm is None:
                return None
            if (pm - p) * (pa - p) > 0.0:
                a, pa = mid, pm
            else:
                b = mid
            if not a < 0.5 * (a + b) < b:              # to machine resolution: the exit's g reads s at T_b(P), so a
                break                                   # looser T_b would put noise above the landing tolerance
        return 0.5 * (a + b)

    def dpb_dt(t):
        h = 1e-4
        pa, pb_ = p_b(t - h), p_b(t + h)
        if pa is None or pb_ is None:
            pa, pb_ = p_b(t), p_b(t + h)
            return (pb_ - pa) / h if pa is not None and pb_ is not None else math.nan
        return (pb_ - pa) / (2.0 * h)
    return p_b, t_b, dpb_dt


def view_hook(v, curve, name):
    """The stepper hook of one transitions() curve of an assemblage view (note 4 S4–S5):
    - a cut swap run → Segment (the read's own Δs carried, note 3 §2);
    - a cut edge run → CutFinding «finding» (T continuous, the read's δs for BA; note 3 §3, 68 B1);
    - a row step (a curve end) → CutFinding «restart» (its Δs; r2 v2; the curve dict stays {form, id});
    - a run read across (i ≥ len(_cut)) or any other form → None."""
    form = curve.get("form")
    if not hasattr(v, "_cut"):
        # a view that forwards another's curves (BasalView, review 2 R-M-03): its dT/dP is the overlying read but its ρ
        # is its own, and neither the registration nor note 4 covers a segment there — a cut swap takes the named sharp
        # step; edges and row steps record nothing (reported as a departure with the code)
        ov = getattr(v, "overlying", None)
        if ov is not None and hasattr(ov, "_cut") and form == "assemblage_curve" and curve["id"] < len(ov._cut) \
                and ov._events[curve["id"]].kind == "swap":
            return SharpOnly(name, "basal layer: coexistence segment not built here")
        return None
    if form == "assemblage_row_step":
        c, _k = v._row_steps[curve["id"]]
        return CutFinding(name, (lambda side, p, t: side_s(v, p, t, {c: side})),
                          (lambda t: v._row_step_p(curve["id"], t)), kind="restart")
    if form != "assemblage_curve" or curve["id"] >= len(v._cut):
        return None
    c = v._events[curve["id"]]

    def s_side(side, p, t):
        return side_s(v, p, t, {c: side})
    if c.kind == "edge":
        return CutFinding(name, s_side, lambda t: c.p_b_ext(t, v._reach), kind="finding")
    if c.kind != "swap":
        return None
    inv = curve_inverse(v, c)
    if inv is None:                                   # a single-row run or a P_b not monotone in T: no T_b(P), so no
        return SharpOnly(name, "no T_b: single row or P_b not monotone in T")    # segment — a named sharp step
    p_b, t_b, dpb_dt = inv
    rows = sorted((r["t"], r.get("delta_s")) for r in c.rows)
    ds_rows = [(tt, d) for tt, d in rows if d is not None]

    def ds_model(t):
        if not ds_rows:
            return None
        if t <= ds_rows[0][0]:
            return ds_rows[0][1]
        for (t0, d0), (t1, d1) in zip(ds_rows, ds_rows[1:]):
            if t0 <= t <= t1:
                return d0 + (d1 - d0) * (t - t0) / (t1 - t0)
        return ds_rows[-1][1]
    return Segment(name, s_side, (lambda side, p, t: side_rho(v, p, t, {c: side})), p_b, t_b, dpb_dt,
                   rows_t=[tt for tt, _d in rows], ds_model=ds_model)


def check_table(table):
    """Load checks of an exported assemblage table for the coexistence hooks (note 4 S4, r2 v1 and 68 n; run by the
    registry after material_assemblage.check_table, raising its TableStop, check «coexist»):
    - every cut edge row (an edge-class row not read across) lies in a cut run, so no non-swap cut is left without a
      hook (the FINDING rule and G1's restarts cannot be silently vacuous);
    - on every cut swap run of two or more rows, each row's signed delta_s agrees with Clapeyron for Δv < 0:
      sign(delta_s) = −sign(dP_b/dT) on its segment (r2 B1′).
    A table without an exported block has no curves and passes."""
    from solver import material_assemblage as ma
    b = table.get("boundaries") or {}
    if b.get("status") != "exported":
        return
    ts = sorted({c["t"] for c in table["cells"]})
    curves = ma.build_curves(b, ts)
    runs = ma._cut_runs(curves)
    in_runs = {id(r) for c in runs for r in c.rows}
    lost = [(c.kind, r["t"], r["p_b"]) for c in curves if c.kind == "edge" for r in c.rows
            if not r["across"] and id(r) not in in_runs]
    if lost:
        raise ma.TableStop(f"coexist_cut_rows: {len(lost)} cut edge row(s) in no cut run, first {lost[0]!r}",
                           check="coexist")
    for c in runs:
        if c.kind != "swap" or len(c.rows) < 2:
            continue
        for a, b2 in zip(c.rows, c.rows[1:]):
            if b2["t"] == a["t"]:
                continue
            slope = (b2["p_b"] - a["p_b"]) / (b2["t"] - a["t"])
            for r in (a, b2):
                d = r.get("delta_s")
                if d is not None and slope != 0.0 and d != 0.0 and (d > 0.0) == (slope > 0.0):
                    raise ma.TableStop(f"coexist_clapeyron: swap run at T {r['t']!r} K has delta_s {d!r} of the "
                                       f"curve's slope sign ({slope!r} Pa/K); Clapeyron with Δv < 0 wants the opposite",
                                       check="coexist")


def notes(records, views, body_layers=()):
    """solve's notes from Result.coexist (note 4 S6), and the SWAP_NOTE texts to drop (68 B4, keyed by curve: m2).
    Returns (notes, drop) — drop is a set of (layer id, SWAP_NOTE text prefix) for every curve walked as a segment;
    solve removes a material_declared_note whose (layer, text) starts with one (its own «; latent heat …» tail too)."""
    from solver import material_assemblage as ma, result
    out, drop = [], set()
    for rc in records:
        kind, layer = rc.get("kind"), rc.get("layer")
        if kind == "segment":
            (_m, p_in, t_in), ex = rc["entry"], rc.get("exit")
            p_out, t_out = (ex if ex else (None, None))
            text = (f"coexistence segment (Q-P3 (a)): {rc['curve']}, P {p_in / 1e9:.6g} → "
                    f"{(p_out or float('nan')) / 1e9:.6g} GPa, T {t_in:.6g} → {t_out if t_out is not None else float('nan'):.6g} K")
            out.append(result.Note("coexistence_segment", text, {
                "layer": layer, "curve": rc["curve"], "entry_p": p_in, "entry_t": t_in, "exit_p": p_out,
                "exit_t": t_out, "ds_read": rc.get("ds_read"), "ds_model": rc.get("ds_model"),
                "delta": rc.get("delta"), "phi_min": rc["phi_range"][0], "phi_max": rc["phi_range"][1],
                "rho_old_entry": rc.get("rho_old_entry"), "rho_new_exit": rc.get("rho_new_exit"),
                "projection": rc.get("projection")}))
            v = views.get(layer) if hasattr(views, "get") else None
            i = _run_id(rc["curve"])
            if v is not None and hasattr(v, "_events") and i is not None and i < len(v._events):
                a, b = v._events[i].p_range
                drop.add((layer, f"{ma.SWAP_NOTE}; P {a / 1e9:.4g}–{b / 1e9:.4g} GPa"))
        elif kind == "finding":
            out.append(result.Note("coexistence_cut_finding", f"non-swap cut {rc['curve']}: the read's s steps by "
                                   f"{rc.get('ds')!r} J/kg/K at P {rc['P'] / 1e9:.6g} GPa, T {rc['T']:.6g} K; T kept "
                                   "continuous (a read defect for BA; coexistence note 3 §3)", dict(rc)))
        elif kind == "restart":
            out.append(result.Note("coexistence_restart", f"curve end {rc['curve']}: restart, the read's s steps by "
                                   f"{rc.get('ds')!r} J/kg/K at P {rc['P'] / 1e9:.6g} GPa (no segment)", dict(rc)))
        elif kind == "sharp":
            out.append(result.Note("coexistence_sharp_step", f"{rc['curve']}: sharp step, no coexistence segment "
                                   f"({rc.get('reason')}) at P {rc['P'] / 1e9:.6g} GPa", dict(rc)))
    return out, drop


def _run_id(event_name):
    """The run index i from an event name «phase:swap<i>:<labels>|…» (events.record_events' naming), else None."""
    import re
    m = re.match(r"phase:(?:swap|edge|node)(\d+):", event_name)
    return int(m.group(1)) if m else None
