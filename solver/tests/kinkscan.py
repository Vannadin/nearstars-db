# 광물 집합 읽기의 기울기 꺾임 조사 — 선 위 한쪽 1차 차분, 위치를 좁혀 진짜 꺾임만, 내부 상태로 부류, 이름 붙은 부류의 한도 (항목 5d998d40, 68 판정 4)
"""The slope-jump scan of an assemblage read (item 5d998d40, 68 ruling 4), used by test_assemblage_c1.

Lines: fixed T (ln P from the floor to p_dataset at N steps) and fixed P (along T at 20 steps per T cell).
- Candidate: a local max of J(h) = |D⁺(h) − D⁻(h)| (the one-sided first differences at the line step h) above CAND × the
  line's median J and above REL × the line's median |D|.
- Located: the bracket ±h is narrowed by 9-point scans of J at bracket/8 to 1e-5 in ln P (1e-3 K).
- Kink: J at step 1e-6 (1e-4 K) at the located point is ≥ ½·J(h) and ≥ REL × median |D| (a slope jump keeps its size as
  the step shrinks). The point is then located again to 2e-9 (2e-7 K) and J taken at 1e-7, 1e-8, 1e-9 (68 K1): where it
  falls below ½·J(1e-6) the point is a narrow-loop ramp (C¹, a phase loop narrower than about 1e-6 in ln P crossed by
  the empty-region smoothstep or the blend), its width the step ×10 at which J fell; otherwise a kink if the one-sided
  slopes over 1e-9 still differ by more than 1e-3 of their size. (The scan at v4 tested that last step at the first
  location, up to its bracket off the kink, and so took most clip kinks for ramps: one bse line held 2 kinks by it and
  17 by this scan, on the same read.)
- Excluded: within 2h of a cut swap's P_b at the read's T (a landed event, a step by design); refusals.
- Class, by the read's internal state 2e-6 (2e-4 K) either side (instrumented, no value change): refusal edge, T row line,
  row drop, region, clip (bridge), clip (T) (the per-field pattern of the T slope's clip, over the own and side reads in
  call order, differs), else unnamed.

The named classes and their bounds (2× the max measured on the three shipped records with the run-end rule, full scan
on the TIP 91be8043 + this scan; max slope jump / the line's median |D|):
- clip (T): the T-direction node slope's Fritsch–Carlson clip (_clip_fc in _slope_t) starts or stops binding where a T
  secant passes 0; the slope is then 0 on one side and about the secant on the other, C⁰ in the row values, so the read
  kinks in P there (68 ruling 3). In a blend's side reads too: dmm 23.961302 GPa, 1418.5 K, ρ, where row 25 holds its
  bounding curve's value (an empty region) and row 26 rises through it (68 K1 (iii)). Measured max: ρ 10812 / 2613 /
  16924, dT/dP 2650 / 1159 / 2700, c_P 275615 / 9933 / 3961 (bse / dmm / mars); 425 / 389 / 428 per record.
- T row line: at a T row line the stencil's rows, and so the set of curves partitioning them, change; an edge that
  partitions only the outgoing row leaves the blend there (its far and own reads agree, as it partitions none of the
  remaining rows), so the read is C⁰ with a slope change across the row line. Measured max: ρ 1.02, dT/dP 4.83,
  c_P 0.92. 25 / 16 / 13 per record.
- narrow-loop ramp: C¹, so no jump bound; bounded by count and width (RAMPS: 68 on K1, a ramp much narrower than the
  stepper's step acts as a kink for the integration): a full scan fails on more than twice the declared count, any scan
  on a ramp narrower than half the declared minimum width. Measured: 16 / 10 / 13, all of width 1e-6.
Any other class, or an unnamed kink above the noise floor, fails the scan.
"""
import contextlib
import math

from solver import material_assemblage as ma

REL, CAND = 1e-3, 20.0
FIELDS = ("rho", "dtdp", "c_p")
BOUNDS = {"clip (T)": {"rho": 2 * 16924.0, "dtdp": 2 * 2700.0, "c_p": 2 * 275615.0},
          "T row line": {"rho": 2 * 1.021, "dtdp": 2 * 4.829, "c_p": 2 * 0.915}}
#: per record: the full scan's narrow-loop ramp count and their least width (ln P)
RAMPS = {"silicate_slb_default_bse": (16, 1e-6), "silicate_slb_earth_dmm_wh2005": (10, 1e-6),
         "silicate_slb_mars_khan2022": (13, 1e-6)}


@contextlib.contextmanager
def _instrumented(v, probe):
    """Records, while probe["on"], per field the pattern of the T slope's clip over the read's T interpolations (which
    bind, in call order), whether a bridge clip binds, and which rows' regions a read used."""
    clip, slope_t, bridge, rvr = ma._clip_fc, ma._slope_t, ma._bridge, ma.AssemblageView._row_value_raw
    value, blend = ma.AssemblageView._value, ma.AssemblageView._blend_sides

    def slope_t_(d0, d1):                     # the T slope's clip only (a run's gap-end clip is shared, so C¹)
        r = slope_t(d0, d1)
        if probe["on"]:
            q = d0 * d0 + d1 * d1
            probe["clip_t"].setdefault(probe["f"], []).append(r != (0.0 if q == 0.0 else d0 * d1 * (d0 + d1) / q))
        return r

    def value_(self, f, *a, **k):
        probe["f"] = f
        return value(self, f, *a, **k)

    def blend_(self, f, *a, **k):
        probe["f"] = f
        return blend(self, f, *a, **k)

    def bridge_(x, a, b):
        s = (b[1][0] - a[1][-1]) / (b[0][0] - a[0][-1])
        if probe["on"] and (clip(a.m_hi, s, s) != a.m_hi or clip(b.m_lo, s, s) != b.m_lo):
            probe["clip_b"].add((a[2][-1], b[2][0]))
        return bridge(x, a, b)

    def row_value_raw(self, f, k, r, x, corner):
        if probe["on"]:
            probe["regions"].add((f, k, r))
        return rvr(self, f, k, r, x, corner)
    saved = (ma._slope_t, ma._bridge, ma.AssemblageView._row_value_raw, ma.AssemblageView._value,
             ma.AssemblageView._blend_sides)
    (ma._slope_t, ma._bridge, ma.AssemblageView._row_value_raw, ma.AssemblageView._value,
     ma.AssemblageView._blend_sides) = slope_t_, bridge_, row_value_raw, value_, blend_
    try:
        yield
    finally:
        (ma._slope_t, ma._bridge, ma.AssemblageView._row_value_raw, ma.AssemblageView._value,
         ma.AssemblageView._blend_sides) = saved


def scan(v, p_lines=(), t_lines=(), n=4000):
    """Kinks on the fixed-T lines `p_lines` (T values) and the fixed-P lines `t_lines` (P values): [{line, P, T, field,
    jump_rel, class}]."""
    probe = {"on": False, "f": None, "clip_t": {}, "clip_b": set(), "regions": set()}

    def read(p, t):
        v._read_memo = {}
        got = v._solid(p, t)
        return got[:3] if isinstance(got, tuple) else None

    def state(p, t, fi):
        probe.update(clip_t={}, clip_b=set(), regions=set(), on=True)
        v._marks = {"dropped": set(), "empty": False, "by_count": False}
        got = read(p, t)
        probe["on"] = False
        ib = min(max(sum(1 for q in v.ts if q <= t) - 1, 0), len(v.ts) - 2)
        f = ("rho", "dtdp_eq", "c_p")[fi]
        return {"refused": got is None, "ib": ib, "dropped": frozenset(v._marks["dropped"]),
                "regions": frozenset(e for e in probe["regions"] if e[0] == f), "clip_t": tuple(probe["clip_t"].get(f, ())),
                "clip_b": frozenset(probe["clip_b"])}

    def classify(a, b):
        if a["refused"] != b["refused"]:
            return "refusal edge"
        if a["ib"] != b["ib"]:
            return "T row line"
        if a["dropped"] != b["dropped"]:
            return "row drop"
        if a["regions"] != b["regions"]:
            return "region"
        if a["clip_b"] != b["clip_b"] or a["clip_b"]:
            return "clip (bridge)"
        if a["clip_t"] != b["clip_t"]:                   # 68 K1: a clip that starts or stops binding, this field
            return "clip (T)"
        return "unnamed"

    def jump(fx, x, h, fi):
        a, b, c = fx(x - h), fx(x), fx(x + h)
        return None if a is None or b is None or c is None else abs((c[fi] - b[fi]) / h - (b[fi] - a[fi]) / h)

    def locate(fx, x, h, fi, stop):
        lo, hi = x - h, x + h
        while hi - lo > stop:
            st = (hi - lo) / 8
            best = None
            for i in range(9):
                j = jump(fx, lo + i * st, st / 2, fi)
                if j is not None and (best is None or j > best[0]):
                    best = (j, lo + i * st)
            if best is None:
                return None
            lo, hi = best[1] - st, best[1] + st
        return 0.5 * (lo + hi)

    def line(fx, side, x0, x1, m, fine, stop):
        h = (x1 - x0) / m
        ys = [fx(x0 + i * h) for i in range(m + 1)]
        found = []
        for fi in range(3):
            D = [None if ys[i] is None or ys[i + 1] is None else (ys[i + 1][fi] - ys[i][fi]) / h for i in range(m)]
            Js = [None if D[i - 1] is None or D[i] is None else abs(D[i] - D[i - 1]) for i in range(1, m)]
            ok = sorted(j for j in Js if j is not None)
            dd = sorted(abs(d) for d in D if d is not None)
            if not ok or not dd:
                continue
            med_j, med_d = ok[len(ok) // 2] or 1e-300, dd[len(dd) // 2] or 1e-300
            for i in range(1, len(Js) - 1):
                j = Js[i]
                if j is None or j < CAND * med_j or j < REL * med_d or (Js[i - 1] or 0) > j or (Js[i + 1] or 0) >= j:
                    continue
                xl = locate(fx, x0 + (i + 1) * h, h, fi, stop)
                jf = None if xl is None else jump(fx, xl, fine, fi)
                if jf is None or jf < 0.5 * j or jf < REL * med_d:
                    continue
                # 68 K1: a slope jump keeps J as the step shrinks to fine/1000; a C¹ ramp of width w loses it once the
                # step is below w (J ∝ step/w): a narrow-loop ramp, named with the step where J fell below ½·J(fine)
                width, xr = None, locate(fx, xl, fine, fi, fine / 500)      # located again, to the finest step
                for hh in (fine / 10, fine / 100, fine / 1000):
                    jh = None if xr is None else jump(fx, xr, hh, fi)
                    if jh is not None and jh < 0.5 * jf:
                        width = hh * 10
                        break
                if width is not None:
                    found.append((xl, fi, jf / med_d, "narrow-loop ramp", width))
                    continue
                tiny = fine / 1000                           # and a kink only if the slopes differ by > 1e-3 there
                a, b, c = fx(xr - tiny), fx(xr), fx(xr + tiny)
                if a is not None and b is not None and c is not None:
                    sl, sr = (b[fi] - a[fi]) / tiny, (c[fi] - b[fi]) / tiny
                    if abs(sr - sl) <= 1e-3 * max(abs(sl), abs(sr)):
                        continue
                found.append((xl, fi, jf / med_d, classify(side(xl - 2 * fine, fi), side(xl + 2 * fine, fi)), None))
        return found

    out = []
    x_lo, x_hi = math.log(v.ps[0]), math.log(v.p_dataset)
    with _instrumented(v, probe):
        for t in p_lines:
            sw = [math.log(q) for c in v._cut if c.kind == "swap" and (q := c.p_b_ext(t, v._reach)) is not None]
            h = (x_hi - x_lo) / n
            for x, fi, r, cl, w in line(lambda x: read(math.exp(x), t), lambda x, fi: state(math.exp(x), t, fi),
                                        x_lo, x_hi, n, 1e-6, 1e-5):
                if not any(abs(x - s) < 2 * h for s in sw):
                    out.append({"line": "P", "P": math.exp(x), "T": t, "field": FIELDS[fi], "jump_rel": r, "class": cl,
                                "width": w})
        for p in t_lines:
            m = max(len(v.ts) * 20, 400)
            for tq, fi, r, cl, w in line(lambda t: read(p, t), lambda t, fi: state(p, t, fi), v.ts[0], v.ts[-1], m,
                                         1e-4, 1e-3):
                sw = [math.log(q) for c in v._cut if c.kind == "swap" and (q := c.p_b_ext(tq, v._reach)) is not None]
                if not any(abs(math.log(p) - s) < 1e-4 for s in sw):
                    out.append({"line": "T", "P": p, "T": tq, "field": FIELDS[fi], "jump_rel": r, "class": cl,
                                "width": w})
    return out


def full_lines(v):
    """Every line of the full scan: one fixed-T line 0.37 into each T cell, one fixed-P line 0.37 into each P cell up to
    p_dataset."""
    ts = [v.ts[k] + 0.37 * (v.ts[k + 1] - v.ts[k]) for k in range(len(v.ts) - 1)]
    ps = [math.exp(v.lnps[j] + 0.37 * (v.lnps[j + 1] - v.lnps[j])) for j in range(len(v.ps) - 1)
          if v.ps[j + 1] <= v.p_dataset]
    return ts, ps


def violations(kinks, rid, full=False):
    """The kinks outside the named classes or above their bounds; narrow-loop ramps (C¹, so no jump bound) narrower than
    half the record's declared minimum width, and on a full scan more than twice its declared count (68 on K1: a ramp
    much narrower than the stepper's step acts as a kink for the integration)."""
    n_ramp, w_min = RAMPS[rid]
    ramps = [k for k in kinks if k["class"] == "narrow-loop ramp"]
    out = [k for k in ramps if k["width"] < 0.5 * w_min]
    if full and len(ramps) > 2 * n_ramp:
        out.append({"class": "narrow-loop ramp", "count": len(ramps), "declared": n_ramp})
    return out + [k for k in kinks if k["class"] != "narrow-loop ramp"
                  and (k["class"] not in BOUNDS or k["jump_rel"] > BOUNDS[k["class"]][k["field"]])]
