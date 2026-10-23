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
  row drop, region, clip (bridge), side structure (the per-field count of T-slope calls, over the own and side reads,
  differs: a side read gains or loses a row; 68 z1, unnamed), clip (T) (the per-field pattern of the T slope's clip,
  over the own and side reads in call order, differs), else unnamed.

The named classes and their bounds (2× the max measured on the three shipped records with the run-end rule, full scan
on the TIP 6570d848 (the run-end rule, BLEND_SHARP, the bump bridge and END_CAPPED) + this scan; max slope jump / the
line's median |D|):
- clip (T): the T-direction node slope's Fritsch–Carlson clip (_clip_fc in _slope_t) starts or stops binding where a T
  secant passes 0; the slope is then 0 on one side and about the secant on the other, C⁰ in the row values, so the read
  kinks in P there (68 ruling 3). In a blend's side reads too: dmm 23.961302 GPa, 1418.5 K, ρ, where row 25 holds its
  bounding curve's value (an empty region) and row 26 rises through it (68 K1 (iii)). Measured max: ρ 10812 / 2613 /
  16924, dT/dP 64120 / 1412 / 2693, c_P 488360 / 88548 / 5192 (bse / dmm / mars); 410 / 377 / 440 per record, and a
  full scan fails on more than twice that count (CLIPS, 68 z2). bse's dT/dP and c_P maxima sit on the 14.24 GPa line
  (1068–1218 K), where the line's median |D| is small; uncapped dT/dP and c_P run ends (END_CAPPED) raised its dT/dP
  jumps from 2670 to 64120. (Before: dT/dP 2670 / 1408 / 4283, c_P 288808 / 98934 / 5191, 413 / 370 / 436 with
  BLEND_SHARP; 2650 / 1159 / 2700, 275615 / 9933 / 3961, 425 / 389 / 428 before it.)
- T row line: at a T row line the stencil's rows, and so the set of curves partitioning them, change; an edge that
  partitions only the outgoing row leaves the blend there (its far and own reads agree, as it partitions none of the
  remaining rows), so the read is C⁰ with a slope change across the row line. Measured max: ρ 1.02, dT/dP 7.69,
  c_P 1.68. 15 / 17 / 10 per record.
- narrow-loop ramp: C¹, so no jump bound; bounded by count and width (RAMPS: 68 on K1, a ramp much narrower than the
  stepper's step acts as a kink for the integration): a full scan fails on more than twice the declared count, any scan
  on a ramp narrower than half the declared minimum width. Measured: 14 / 8 / 14, all of width 1e-6.
- interior-end hold (b′) (note 8 delta 1 addendum 1; r2 c8a2fab3; 68 README §14–§18): a «T row line» kink on a fixed-P
  line at an interior run end's row t_e within the end's (c′) window, its run ≥ 2 rows and not flat-ended, absent from
  AF af12d75b's scan (shipped as data/kinkscan_af_*.json), accepted when held on the open side and C⁰ at t_e in every
  field (hold, c0_test); counted apart from violations() (violations_with_hold) with its own bound HOLD_BOUND, 2× the
  max over stage 5c's line set at s on; a candidate without an AF lookup is a violation; the x_r mutant (xr_mutant)
  accepts none. A member failing C⁰ at t_e is an edge T-end step: on the full scan every failing field must be in
  E26's census (data/e26_census.json, e26_census_match, §9 with amendment 1), else a violation.
Any other class, or an unnamed kink above the noise floor, fails the scan.
"""
import contextlib
import math

from solver import material_assemblage as ma

REL, CAND = 1e-3, 20.0
FIELDS = ("rho", "dtdp", "c_p")
BOUNDS = {"clip (T)": {"rho": 2 * 16924.0, "dtdp": 2 * 64120.0, "c_p": 2 * 488361.0},
          "T row line": {"rho": 2 * 1.021, "dtdp": 2 * 7.686, "c_p": 2 * 1.683},
          # swap extension note 1 (r2 addendum 4 (3)): a reach-0 end's holding row stepping at its own P_b, weighted by its
          # T weight, a landed event (assemblage_row_step); a value step, so the slope ratio is large; 2× the max over
          # P lines at 10/50/90 % of both cells past each of the 26 ends (bse / dmm / mars 3.2e5 / 1.35e7 / 4.17e7 ρ,
          # 2.29e5 / 4.73e7 / 1.99e8 dT/dP, 1.06e7 / 5.98e8 / 4.96e7 c_P; engine ea-swap-ext, scratch rowstep_scan.py)
          "reach-0 weighted row step": {"rho": 2 * 4.172e7, "dtdp": 2 * 1.990e8, "c_p": 2 * 5.976e8}}
#: per record: the count of «reach-0 weighted row step» kinks on those lines (a scan over them fails above twice it)
ROWSTEPS = {"silicate_slb_default_bse": 45, "silicate_slb_earth_dmm_wh2005": 64, "silicate_slb_mars_khan2022": 108}
#: per record: the full scan's narrow-loop ramp count and their least width (ln P)
RAMPS = {"silicate_slb_default_bse": (14, 1e-6), "silicate_slb_earth_dmm_wh2005": (8, 1e-6),
         "silicate_slb_mars_khan2022": (14, 1e-6)}
#: per record: the full scan's clip (T) count (68 z2: the jump bound alone barely constrains)
CLIPS = {"silicate_slb_default_bse": 410, "silicate_slb_earth_dmm_wh2005": 377, "silicate_slb_mars_khan2022": 440}


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
        if len(a["clip_t"]) != len(b["clip_t"]):         # 68 z1: a side read gains or loses a T call, not a binding
            return "side structure"
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
            rs = [math.log(q) for i in range(len(getattr(v, "_row_steps", ())))
                  if (q := v._row_step_p(i, t)) is not None]   # swap extension note 1: holding rows' own P_b, landed
            h = (x_hi - x_lo) / n
            for x, fi, r, cl, w in line(lambda x: read(math.exp(x), t), lambda x, fi: state(math.exp(x), t, fi),
                                        x_lo, x_hi, n, 1e-6, 1e-5):
                if not any(abs(x - s) < 2 * h for s in sw):
                    if any(abs(x - s) < 2 * h for s in rs):
                        cl = "reach-0 weighted row step"
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
    n_row = sum(k["class"] == "reach-0 weighted row step" for k in kinks)
    if full and rid in ROWSTEPS and n_row > 2 * ROWSTEPS[rid]:
        out.append({"class": "reach-0 weighted row step", "count": n_row, "declared": ROWSTEPS[rid]})
    n_clip = sum(k["class"] == "clip (T)" for k in kinks)
    if full and n_clip > 2 * CLIPS[rid]:
        out.append({"class": "clip (T)", "count": n_clip, "declared": CLIPS[rid]})
    return out + [k for k in kinks if k["class"] != "narrow-loop ramp"
                  and (k["class"] not in BOUNDS or k["jump_rel"] > BOUNDS[k["class"]][k["field"]])]


# «interior-end hold (b′)» (silicate note 8 delta 1 addendum 1 §2–§3, blob 8f38338d; r2 c8a2fab3; 68 README §14): a
# «T row line» kink on a fixed-P line at an interior run end's row, relabelled by mechanism, counted apart from
# violations(). The test is pc/ea-rev3d/jb_kink.py's _hold (c2ed694b) as cleared; AF af12d75b's scan is shipped data.
HOLD = "interior-end hold (b′)"
#: its bound per table and field: 2× the max jump_rel of accepted members over stage 5c's line set at s on (68 §14 (ii),
#: §17; TIP 8d3f4aae, the edge-end and full_lines sets with AF's scan, artifacts ea-jobA 7f55c311 kmeas; max ρ / dT/dP /
#: c_P: bse 1.795 / 117.96 / 15.43, dmm 7.624 / 95.25 / 12.19, khan 2.290 / 25.96 / 26.49). These sit above the generic
#: «T row line» bound (dT/dP 2 × 7.686) by design: jump_rel is a ratio to the line's median |D| and the held side's
#: slope is about 0 (addendum 1 §1), so the read does not step; the generic bound is not raised
HOLD_BOUND = {"silicate_slb_default_bse": {"rho": 2 * 1.7946097684392608, "dtdp": 2 * 117.96097252566203,
                                           "c_p": 2 * 15.43052040590948},
              "silicate_slb_earth_dmm_wh2005": {"rho": 2 * 7.623794533679736, "dtdp": 2 * 95.25493671059657,
                                                "c_p": 2 * 12.187386379907778},
              "silicate_slb_mars_khan2022": {"rho": 2 * 2.2902302346066112, "dtdp": 2 * 25.955932871556712,
                                             "c_p": 2 * 26.494264628830322}}
DATA = __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "data")
#: the C⁰ test's round-off floor multiplier on ε·|v| (r2 32cf0efe: J₃'s weights (|8| + |6| + |1|)/3 = 5, two reads per
#: difference at ≲ 1.6 ε|v| each) and its smallest step in K (r2 db668a80: reads at ±h/8)
FLOOR_K, H_FLOOR, EPS = 16.0, 1.25e-4, 2.220446049250313e-16
_SHIPPED = {}


def shipped(name):
    """A shipped data file's payload, checked on load: present, its provenance header there, its sha256 over the
    canonical payload as recorded. Anything else raises (68 §14 (i): red, never a silent «no lookup»)."""
    if name not in _SHIPPED:
        import hashlib
        import json
        import os
        path = os.path.join(DATA, name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"kinkscan: shipped data {name} is missing")
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        if not d.get("provenance") or "data" not in d:
            raise ValueError(f"kinkscan: {name} has no provenance header or no data")
        sha = hashlib.sha256(json.dumps(d["data"], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if sha != d.get("sha256"):
            raise ValueError(f"kinkscan: {name}'s payload is not its recorded sha256")
        _SHIPPED[name] = d["data"]
    return _SHIPPED[name]


def _j3(s, h):
    return (8.0 * s(h / 4.0) - 6.0 * s(h / 2.0) + s(h)) / 3.0


def c0_test(s, v_abs, h=1e-3):
    """The C⁰ acceptance at one field (r2 32cf0efe; B1 on ac9af31a; addendum db668a80), s(h) the value step across t_e at
    ±h: J = J₃(h/2) + (J₃(h/2) − J₃(h))/7, allowance |J₃(h) − J₃(h/2)|/7 + FLOOR_K·ε·|v|, tol 1e-9·|v|; resolved when
    allowance ≤ tol/2, then ok when |J| ≤ tol + allowance; else h halves down to H_FLOOR, unresolved there is not ok."""
    tol = 1e-9 * v_abs
    while True:
        a, b = _j3(s, h), _j3(s, h / 2.0)
        est, allow = b + (b - a) / 7.0, abs(a - b) / 7.0 + FLOOR_K * EPS * v_abs
        out = {"J": est, "allowance": allow, "tol": tol, "h": h}
        if allow <= tol / 2.0:
            return {**out, "resolved": True, "ok": abs(est) <= tol + allow}
        if h / 2.0 < H_FLOOR * (1.0 - 1e-12):
            return {**out, "resolved": False, "ok": False}
        h /= 2.0


@contextlib.contextmanager
def xr_mutant():
    """68's mutant «x_r throughout»: an interior end's position follows its parent's real P_b(T) through the reach;
    under it no kink may be accepted as (b′)."""
    cls = next(c for c in vars(ma).values() if isinstance(c, type) and hasattr(c, "_edge_ext"))
    real = cls._edge_ext

    def ext(self, t, hi, e, o, reach):
        if (self.interior_hi if hi else self.interior_lo) and getattr(self, "parent", None) is not None:
            q = self.parent.p_b(t)
            if q is not None:
                return q
        return real(self, t, hi, e, o, reach)
    cls._edge_ext = ext
    try:
        yield
    finally:
        cls._edge_ext = real


def _af_match(v, k, tol):
    """r2 c8a2fab3: AF's kink matching k (same field, |ΔT| ≤ the scan step, same table P cell), the nearest in T; False
    when AF scanned k's line and has none; None when k's line (its fixed P, to 1e-9) is not among AF's lines."""
    import bisect
    if not any(abs(q / k["P"] - 1.0) <= 1e-9 for q in shipped("kinkscan_af_lines.json").get(v.material_id, {}).get("p", [])):
        return None
    cell = lambda p: min(max(bisect.bisect_right(v.ps, p) - 1, 0), len(v.ps) - 2)
    ia = cell(k["P"])
    got = [x for x in shipped("kinkscan_af_kinks.json").get(v.material_id, [])
           if x["field"] == k["field"] and abs(x["T"] - k["T"]) <= tol and cell(x["P"]) == ia]
    return min(got, key=lambda x: abs(x["T"] - k["T"])) if got else False


def hold(v, k):
    """The (b′) test on one kink (jb_kink._hold, c2ed694b). None when k is no candidate; {"member": False, "excluded":
    [...]} when its nearest end is one-row or flat-ended, or AF has the kink, or AF has no scan of its line («no AF
    lookup»); else the member record with «accepted» = held on the open side and a run of > 1 row and C⁰ at t_e in
    every field (c0_test at h = 1e-3 K)."""
    if k.get("class") != "T row line" or k.get("line") != "T":
        return None
    p, t = k["P"], k["T"]
    x = math.log(p)
    step = (v.ts[1] - v.ts[0]) / 20.0
    ib = min(max(sum(1 for q in v.ts if q <= t) - 1, 0), len(v.ts) - 2)
    rows = range(max(ib - 1, 0), min(ib + 2, len(v.ts) - 1) + 1)
    rel = {c for r in rows for _pb, c in v._partition(r)}
    ends, excl = [], []
    for c in v._cut:
        if c.kind != "edge" or c not in rel:
            continue
        for hi in (True, False):
            te = c.t1 if hi else c.t0
            if not getattr(c, "interior_hi" if hi else "interior_lo", False) or abs(t - te) > step:
                continue
            pb = c.p_b(te)
            if pb is None:
                continue
            xb, w = math.log(pb), v._width(math.log(pb))
            if abs(x - xb) <= w:
                rs = c.rows
                o = (rs[-2] if hi else rs[1]) if len(rs) > 1 else None
                why = "one row" if o is None else ("flat end" if o["p_b"] == (rs[-1] if hi else rs[0])["p_b"] else None)
                (excl if why else ends).append((abs(x - xb), x - xb, w, c, hi, te, pb) + ((why,) if why else ()))
    allx = sorted(ends + excl, key=lambda e: e[0])
    if ends:
        af = _af_match(v, k, step)
        if af is not False:
            return {"member": False, "af": None if af is None else {"T": af["T"], "P": af["P"], "jump_rel": af["jump_rel"]},
                    "excluded": [{"curve": e[3].id, "side": "hi" if e[4] else "lo", "t_e": e[5], "dx": e[1],
                                  "window": e[2], "why": ("AF has it" if af else "no AF lookup")} for e in allx[:1]]}
    if not ends:
        if excl:
            return {"member": False, "excluded": [{"curve": e[3].id, "side": "hi" if e[4] else "lo", "t_e": e[5],
                                                   "dx": e[1], "window": e[2], "why": e[7]} for e in sorted(excl, key=lambda e: e[0])]}
        return None
    ends.sort(key=lambda e: e[0])
    _a, _d, _w, c, hi, te, pb = ends[0]
    q = c.p_b_ext(te + (1e-3 if hi else -1e-3), v._reach)
    held = q is not None and abs(q / pb - 1.0) <= 1e-12
    cache = {}

    def read(t_):
        if t_ not in cache:
            cache[t_] = v._solid(p, t_)
        return cache[t_]
    fields = []
    for i, f in enumerate(FIELDS):
        def s(h_, i=i):
            a, b = read(te - h_), read(te + h_)
            if not (isinstance(a, tuple) and isinstance(b, tuple)):
                raise ValueError("refused")
            return b[i] - a[i]
        try:
            ref = read(te)
            if not isinstance(ref, tuple):
                raise ValueError("refused at t_e")
            fields.append({"field": f, **c0_test(s, abs(ref[i]))})
        except ValueError:
            fields = []
            break
    c0 = bool(fields) and all(q_["ok"] for q_ in fields)
    return {"member": True, "t_e": te, "p_b": pb, "curve": c.id, "side": "hi" if hi else "lo", "run_rows": len(c.rows),
            "held": held, "c0": {"fields": fields, "ok": c0}, "accepted": held and len(c.rows) > 1 and c0}


def holds(v, kinks):
    """(members, no_af): each kink's (b′) record where it is a member, [(kink, record)], and the count of candidates left
    generic for want of an AF lookup (68 f7d964cc §6: > 0 is a FINDING)."""
    members, no_af = [], 0
    for k in kinks:
        h = hold(v, k)
        if h is None:
            continue
        if h.get("member"):
            members.append((k, h))
        elif any(e.get("why") == "no AF lookup" for e in h.get("excluded", ())):
            no_af += 1
    return members, no_af


def violations_with_hold(v, kinks, rid, full=False, members=None, apart=()):
    """violations() with the (b′) class counted apart (addendum 1 §2): accepted members leave the generic count and are
    violations themselves above HOLD_BOUND, and candidates left for want of an AF lookup are one count violation.
    `members`, (members, no_af) from holds() when the caller has them; `apart`, further kinks the caller has counted
    apart (the landing scan's E26 census matches), also left out of the generic count. Returns (violations, members)."""
    members, no_af = holds(v, kinks) if members is None else members
    acc = [k for k, h in members if h["accepted"]]
    rest = [k for k in kinks if not any(k is a for a in acc) and not any(k is a for a in apart)]
    out = violations(rest, rid, full=full)
    for k in acc:
        if k["jump_rel"] > HOLD_BOUND[rid][k["field"]]:
            out.append({**k, "class": HOLD, "bound": HOLD_BOUND[rid]})
    if no_af:
        out.append({"class": HOLD, "no_af_lookup": no_af})
    return out, members


def e26_census_match(v, k, end=None):
    """68 README §9 with amendment 1 (§18, r2 concurring): the census row a C⁰-failing kink belongs to, or None. E26 iff
    its field is dT/dP or c_P; its T is within one fixed-P scan step of an edge end T_e in the census
    (data/e26_census.json); (3′) that end is the kink's own curve end (`end` = (curve id, "hi" | "lo"), a (b′) member's;
    without it, any census edge end at T) and the kink's ln P lies inside its window, |x − ln P_b_ext(T_e)| ≤ w; and
    (4), an upper bound only, its step |Δ|/max(|l|,|r|) across T_e ∓ 1e-6 K at its own P is ≤ 2× the row's recorded
    value for the field."""
    if k.get("line") != "T" or k.get("field") not in ("dtdp", "c_p"):
        return None
    i = FIELDS.index(k["field"])
    h = (v.ts[-1] - v.ts[0]) / max(len(v.ts) * 20, 400)
    x = math.log(k["P"])
    curves = {c.id: c for c in v._cut}
    for r in shipped("e26_census.json").get(v.material_id, []):
        if r["kind"] != "edge" or abs(r["T_e"] - k["T"]) > h:
            continue
        if end is not None and (r["curve"] != end[0] or r["end"] != ("t1" if end[1] == "hi" else "t0")):
            continue
        c = curves.get(r["curve"])
        pe = None if c is None else c.p_b_ext(r["T_e"], v._reach)
        if pe is None or abs(x - math.log(pe)) > v._width(math.log(pe)):
            continue
        a, b = v._solid(k["P"], r["T_e"] - 1e-6), v._solid(k["P"], r["T_e"] + 1e-6)
        if not (isinstance(a, tuple) and isinstance(b, tuple)):
            continue
        ref = r["jump_dtdp" if k["field"] == "dtdp" else "jump_cp"]
        if abs(b[i] - a[i]) / max(abs(a[i]), abs(b[i]), 1e-12) <= 2.0 * ref:
            return r
    return None
