# 출처 잇기 계산 — 교차 확인의 띠(선언 격자의 최대 |Δρ|/ρ)와 노드별 r = |Δρ|/σ_allow, σ 전파 (phase-2 impl notes 3–4)
"""Joining two sources inside one phase (rewrite/phase2-impl.frozen.md notes 3 A1–A3, A7 and 4).

`cross_check(view, phase_index, join)` walks the join's declared sampling grid inside its overlap box (the data-range
intersection, A1) and returns, per node, ρ of the preferred and the other source, |Δρ|/ρ, σ_allow and
r = |Δρ|/σ_allow (A3). The band is max |Δρ|/ρ over the grid (A2: «its mismatch goes into the band at every node»);
nodes with r > k are the ones the record must disclose by name and value.

σ of a source at a state (A3, c8's edits 3–4, note 4 item 4):
- propagated: ρ recomputed with each listed parameter moved by its σ, combined in quadrature (correlation not
  printed: independent, which the record discloses as overstating for K0–K′ fits);
- constant: the stated relative σ;
- not_printed: 0, never a stand-in;
- by_region: the printed values by (P, T) box (directing (a); c8: IAPWS-06 Table 7). Where several boxes hold
  the node, the smallest printed value: the finer statement, and never a looser gate. Outside every box, `else`
  (constant or not_printed).
sigma_kind converts to 1σ: ci90 ÷ 1.645, ci95 ÷ 1.960, ci68 and 1sigma ÷ 1. σ_allow = max(σ1, σ2) with shared data,
else √(σ1² + σ2²).
"""
from __future__ import annotations

import copy
import math
from types import MappingProxyType

from solver import stepper as st

TO_1SIGMA = MappingProxyType({"1sigma": 1.0, "ci68": 1.0, "ci90": 1.645, "ci95": 1.960, "not_applicable": 1.0})


def _src(view, pi, sid):
    return next(s for s in view.record["phases"][pi]["sources"] if s["id"] == sid)


def _box_holds(box, p, t) -> bool:
    """Closed box; an absent T bound is open."""
    return (float(box["p_min"]) <= p <= float(box["p_max"])
            and float(box.get("t_min", -math.inf)) <= t <= float(box.get("t_max", math.inf)))


def source_sigma(view, pi, sid, p, t) -> float:
    """Relative 1σ of ρ for source `sid` at (P, T)."""
    src = _src(view, pi, sid)
    sg = src["sigma"]
    if sg["kind"] == "by_region":
        held = [float(r["value"]) for r in sg["regions"] if _box_holds(r["box"], p, t)]
        sg = {"kind": "constant", "value": min(held)} if held else sg["else"]
    if sg["kind"] == "not_printed":
        return 0.0
    if sg["kind"] == "constant":
        return float(sg["value"]) / TO_1SIGMA[src["sigma_kind"]]
    from solver import material_view as mv
    base = view.source_density(pi, sid, p, t)
    if isinstance(base, st.Stop):
        return math.nan
    var = 0.0
    for name, s in sg["from"].items():
        rec = mv.thaw_plain(view.record)
        tgt = next(x for x in rec["phases"][pi]["sources"] if x["id"] == sid)
        block = tgt["eos"]["params"] if name in tgt.get("eos", {}).get("params", {}) else tgt.get("thermal_model", {})
        block[name]["value"] = float(block[name]["value"]) + float(s)
        moved = mv.RecordView(rec, view.t_pot).source_density(pi, sid, p, t)
        if isinstance(moved, st.Stop):
            return math.nan
        var += ((moved - base) / base) ** 2
    return math.sqrt(var) / TO_1SIGMA[src["sigma_kind"]]


def cross_check(view, pi, join) -> dict:
    """Walk the join's sampling grid; per node ρ_pref, ρ_other, |Δρ|/ρ, σ_allow, r. Returns {nodes, band, max_r, k}."""
    a, b = join["between"]
    smp = join["sampling"]
    box, dp, dt = smp["box"], float(smp["dp"]), float(smp["dt"])
    k = float(join.get("k", 2.0))
    shared = "shared_data" in join
    nodes = []
    p = float(box["p_min"])
    while p <= float(box["p_max"]) + 1e-9 * dp:
        t = float(box["t_min"])
        while t <= float(box["t_max"]) + 1e-9 * dt:
            ra, rb = view.source_density(pi, a, p, t), view.source_density(pi, b, p, t)
            if isinstance(ra, st.Stop) or isinstance(rb, st.Stop):
                nodes.append({"p": p, "t": t, "stop": True})
            else:
                rel = abs(rb - ra) / ra
                sa, sb = source_sigma(view, pi, a, p, t), source_sigma(view, pi, b, p, t)
                allow = max(sa, sb) if shared else math.sqrt(sa * sa + sb * sb)
                nodes.append({"p": p, "t": t, "rho_a": ra, "rho_b": rb, "rel": rel, "sigma_allow": allow,
                              "r": math.inf if allow == 0.0 else rel / allow})
            t += dt
        p += dp
    good = [n for n in nodes if "rel" in n]
    if not good:                                              # 68 N45: never a NaN band
        return st.Stop("refused", _refusal(view, float(box["p_min"]), float(box["t_min"]),
                                           f"cross-check {a}–{b} has no valid nodes on its grid"))
    return {"nodes": nodes, "band": max((n["rel"] for n in good), default=math.nan),
            "max_r": max((n["r"] for n in good), default=math.nan), "k": k,
            "over_k": [(n["p"], n["t"], n["r"]) for n in good if n["r"] > k]}


# ── the taper zone (impl note 4 item 1; note 3 A4) ─────────────────────────────────────────────────────────────────
DT_ALPHA = 0.5          # K: the centred step for α = (1/V)(∂V/∂T)_P of a source or of the blend


def source_cp(view, pi, sid, p, t):
    """c_P [J/kg/K] of a source: its own (library c_p; evaluator c_V + T(∂P/∂T)_V²/(ρK_T)), or the source it names in
    c_p_from. A Stop where none can be had."""
    from solver import material_library as ml
    from solver import material_view as mv
    src = _src(view, pi, sid)
    eos = src.get("eos")
    if eos is not None and eos["form"] == "library":
        try:
            return view.source_engine(pi, sid).at(p, t)["c_p"]
        except ml.LibraryOutOfRange as e:
            return st.Stop("refused", mv.RecordRefusal(view.material_id, p, t, "input.material_out_of_data", str(e)))
    if eos is not None and eos["form"] == "evaluator":
        try:
            x = view.source_engine(pi, sid).ev.at(p, t)
        except ValueError as e:
            return st.Stop("refused", mv.RecordRefusal(view.material_id, p, t, "input.material_out_of_data", str(e)))
        return x["c_v"] + t * x["dpdt_v"] ** 2 / (x["density"] * x["k_t"])
    if "c_p_from" in src:
        return source_cp(view, pi, src["c_p_from"], p, t)
    return st.Stop("refused", mv.RecordRefusal(view.material_id, p, t, "input.material_out_of_data",
                                               f"source {sid} has no c_P and names no c_p_from"))


def _smoothstep(s):
    s = min(max(s, 0.0), 1.0)
    return s * s * (3.0 - 2.0 * s)


def taper_zone(join, src_a) -> tuple:
    """(P_lo, P_hi, upper) of a taper: from P_e to 1.5·P_e (upper side) or P_e/1.5 to P_e (lower), or the declared
    width (impl note 4 item 1; lower side owner-direction after adfc584)."""
    pe = float(join["edge_p"])
    upper = join["side"] == "upper"
    if "width" in join:
        end = float(join["width"]["p_end"])
    else:
        end = 1.5 * pe if upper else pe / 1.5
    return (pe, end, True) if upper else (end, pe, False)


def taper_state(view, pi, join, p, t):
    """ρ and (dT/dP)_S across a taper join at (P, T): the measured source (between[0]) on its side of the zone, the
    other beyond it, and in the zone the V-direct blend with a P-only C¹ weight: V = (1 − w)V_a + w·V_b, α from the
    blended V by a centred T difference, c_P blended directly, (dT/dP)_S = αT/(ρ c_P) (note 3 A4). Returns
    (ρ, dtdp, note) where note carries the full |Δρ|/ρ in the zone (the band, note 4 item 1), or a Stop."""
    a, b = join["between"]
    lo, hi, upper = taper_zone(join, _src(view, pi, a))
    s = (p - lo) / (hi - lo)
    w = _smoothstep(s if upper else 1.0 - s)            # weight of the other source b
    t_note = None
    if w < 1.0:                                         # the measured source is read here: is T inside its data range?
        dr = _src(view, pi, a)["data_range"]
        t_lo, t_hi = dr.get("t_min", -math.inf), dr.get("t_max", math.inf)
        if not (t_lo <= t <= t_hi):
            t_note = t_extrapolation(view, pi, a, b, p, t)
            if isinstance(t_note, st.Stop):
                return t_note
    def vol(sid, tt):
        r = view.source_density(pi, sid, p, tt)
        return r if isinstance(r, st.Stop) else 1.0 / r
    parts = [(a, 1.0 - w), (b, w)]
    v = vt_hi = vt_lo = 0.0
    cp = 0.0
    for sid, wt in parts:
        if wt == 0.0:
            continue
        v0, vh, vl = vol(sid, t), vol(sid, t + DT_ALPHA), vol(sid, t - DT_ALPHA)
        c = source_cp(view, pi, sid, p, t)
        for x in (v0, vh, vl, c):
            if isinstance(x, st.Stop):
                return x
        v, vt_hi, vt_lo, cp = v + wt * v0, vt_hi + wt * vh, vt_lo + wt * vl, cp + wt * c
    alpha = (vt_hi - vt_lo) / (2.0 * DT_ALPHA * v)
    rho = 1.0 / v
    note = None
    if 0.0 < w < 1.0:
        ra, rb = view.source_density(pi, a, p, t), view.source_density(pi, b, p, t)
        note = {"grade": f"blended ({a} extrapolated, {b})", "band": abs(rb - ra) / ra}
    if t_note is not None:                                    # 68 N49: both facts ride; the band is the larger
        note = t_note if note is None else {"grade": f"{note['grade']}; {t_note['grade']}",
                                            "band": max(note["band"], t_note["band"])}
    if not (cp > 0.0) or not math.isfinite(alpha):
        return st.Stop("refused", _refusal(view, p, t, f"taper state fails the physical checks (c_P {cp}, α {alpha})"))
    return rho, alpha * t / (rho * cp), note


def _refusal(view, p, t, why):
    from solver import material_view as mv
    return mv.RecordRefusal(view.material_id, p, t, "input.material_out_of_data", why)


def t_extrapolation(view, pi, a, b, p, t):
    """Note 4 item 1.4: the measured source a read outside its data T range. Graded «extrapolated in T»; the band is
    its relative ρ difference from source b at the same state (b must answer there, else refuse); the B3 checks at
    the point (ρ rising with P) refuse on failure. Error method: owner-direction (directing, 2026-10-11, c8's
    proposal)."""
    ra, rb = view.source_density(pi, a, p, t), view.source_density(pi, b, p, t)
    if isinstance(ra, st.Stop):
        return ra
    if isinstance(rb, st.Stop):
        return st.Stop("refused", _refusal(view, p, t, f"{a} extrapolated in T has no band here: {b} cannot answer"))
    up = view.source_density(pi, a, p * (1.0 + 1e-4), t)
    if isinstance(up, st.Stop) or not up > ra:
        return st.Stop("refused", _refusal(view, p, t, f"{a} extrapolated in T fails ρ rising with P"))
    rng = _src(view, pi, a).get("alpha_range")                # r2 XB1: α inside the declared range, not merely finite
    vh, vl = view.source_density(pi, a, p, t + DT_ALPHA), view.source_density(pi, a, p, t - DT_ALPHA)
    if rng is None or isinstance(vh, st.Stop) or isinstance(vl, st.Stop):
        return st.Stop("refused", _refusal(view, p, t, f"{a} extrapolated in T: no declared α range to check against"))
    alpha = (1.0 / vh - 1.0 / vl) / (2.0 * DT_ALPHA) * ra
    if not float(rng["min"]) <= alpha <= float(rng["max"]):
        return st.Stop("refused", _refusal(view, p, t, f"{a} extrapolated in T: α {alpha:.3e} outside its declared "
                                                       f"range [{rng['min']}, {rng['max']}]"))
    band = abs(rb - ra) / ra
    dr = _src(view, pi, a)["data_range"]                      # r2: floor by the disagreement at a's nearest T edge
    t_edge = float(dr["t_max"]) if t > float(dr.get("t_max", math.inf)) else float(dr["t_min"])
    ea, eb = view.source_density(pi, a, p, t_edge), view.source_density(pi, b, p, t_edge)
    if not isinstance(ea, st.Stop) and not isinstance(eb, st.Stop):
        band = max(band, abs(eb - ea) / ea)
    return {"grade": f"{a} extrapolated in T", "band": band}


def taper_zone_checks(view, pi, join, temps, n=21) -> dict:
    """r2 on 48770cb0 (1): the B3 checks on the blended zone itself. At each T in `temps`, walk n P nodes across the
    zone (ends included): ρ must rise with P (which gives K_T > 0), and the zone's effective K_T is compared with the
    sources' own, recorded as the max distortion factor. Returns {failures: [(P, T, why)], max_kt_factor}."""
    a, b = join["between"]
    lo, hi, _up = taper_zone(join, _src(view, pi, a))
    fails, worst = [], 1.0
    for t in temps:
        ps = [lo + (hi - lo) * i / (n - 1) for i in range(n)]
        rho = []
        for p in ps:
            got = taper_state(view, pi, join, p, t)
            if isinstance(got, st.Stop):
                fails.append((p, t, got.record.why))
                rho.append(None)
                continue
            rho.append(got[0])
        for i in range(1, n):
            if rho[i] is None or rho[i - 1] is None:
                continue
            if not rho[i] > rho[i - 1]:
                fails.append((ps[i], t, "ρ does not rise with P across the taper zone"))
                continue
            kt_zone = rho[i] * (ps[i] - ps[i - 1]) / (rho[i] - rho[i - 1])
            ka = [view.source_density(pi, s, ps[i], t) for s in (a, b)]
            kb = [view.source_density(pi, s, ps[i - 1], t) for s in (a, b)]
            if any(isinstance(x, st.Stop) for x in ka + kb):
                continue
            kts = [ka[j] * (ps[i] - ps[i - 1]) / (ka[j] - kb[j]) for j in (0, 1) if ka[j] > kb[j]]
            if kts:
                worst = max(worst, max(kt_zone / k for k in kts), max(k / kt_zone for k in kts))
    return {"failures": fails, "max_kt_factor": worst}



def seam_delta(view, seam) -> dict:
    """Phase-2 design note 5: the step of a source seam in T, max |Δx|/x for ρ, α, c_P over its declared P grid at t,
    each side from its own eos. A Stop where either side cannot answer."""
    lo, hi = seam["between"]
    t = float(seam["t"]["value"])
    smp = seam["sampling"]
    out = {"rho": 0.0, "alpha": 0.0, "c_p": 0.0, "nodes": 0}
    p, p_max, dp = float(smp["p_min"]), float(smp["p_max"]), float(smp["dp"])
    while p <= p_max + 1e-9 * dp:
        a, b = view.phase_props(lo, p, t), view.phase_props(hi, p, t)
        for z in (a, b):
            if isinstance(z, st.Stop):
                return z
        for k in ("rho", "alpha", "c_p"):
            out[k] = max(out[k], abs(b[k] - a[k]) / abs(a[k]) if a[k] else abs(b[k] - a[k]))
        out["nodes"] += 1
        p += dp
    return out


def preferred_source(view, pi):
    """The source a phase answers from when its cross-check's preferred side (between[0]) declares its own eos
    (c8, IAPWS-06 Ih: the gibbs field stays SeaFreeze's, the values come from the preferred source). None otherwise."""
    own = view.record["phases"][pi]["eos"]
    for j in view.record["phases"][pi].get("joins_within", ()):
        if j["kind"] == "cross_check":
            src = _src(view, pi, j["between"][0])
            eos = src.get("eos")
            if eos is not None and not _same_eos(eos, own):    # the phase's own EOS answers as before (e.g. h2o VI)
                return src["id"]
    return None


def _same_eos(a, b):
    if a["form"] != b["form"]:
        return False
    if a["form"] == "library":
        return a["library"]["submodel"] == b.get("library", {}).get("submodel")
    if a["form"] == "evaluator":
        return a["evaluator"]["name"] == b.get("evaluator", {}).get("name")
    return False


def source_state(view, pi, sid, p, t):
    """ρ and (dT/dP)_S = αT/(ρc_P) of one source, inside its data_range only (68 N57: outside it the phase refuses by
    name; a preferred source is never extrapolated bare). An evaluator that returns α and c_P gives them analytically
    (68 N58: no T difference reaching below 0 K); otherwise α by a centred T difference of ρ, c_P from source_cp."""
    src = _src(view, pi, sid)
    if not _box_holds(src["data_range"], p, t):
        return st.Stop("refused", _refusal(view, p, t, f"source {sid} answers only inside its data_range "
                                                       f"{dict(src['data_range'])} ({src['data_range_where']})"))
    eos = src.get("eos") or {}
    if eos.get("form") == "evaluator":
        try:
            x = view.source_engine(pi, sid).ev.at(p, t)
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            return st.Stop("refused", _refusal(view, p, t, f"source {sid}: {e}"))
        if "alpha" in x and "c_p" in x and "c_p_from" not in src:
            rho, alpha, cp = x["density"], x["alpha"], x["c_p"]
            if t == 0.0 and cp == 0.0 and alpha == 0.0:            # the T → 0 limit: αT/c_P → 0
                return rho, 0.0
            if not (cp > 0.0) or not math.isfinite(alpha):
                return st.Stop("refused", _refusal(view, p, t, f"source {sid} fails the physical checks "
                                                               f"(c_P {cp}, α {alpha})"))
            return rho, alpha * t / (rho * cp)
    rho = view.source_density(pi, sid, p, t)
    if t - DT_ALPHA < 0.0:
        return st.Stop("refused", _refusal(view, p, t, f"source {sid}: α by a T difference needs T ≥ {DT_ALPHA} K"))
    vh, vl = view.source_density(pi, sid, p, t + DT_ALPHA), view.source_density(pi, sid, p, t - DT_ALPHA)
    cp = source_cp(view, pi, sid, p, t)
    for x in (rho, vh, vl, cp):
        if isinstance(x, st.Stop):
            return x
    alpha = (1.0 / vh - 1.0 / vl) / (2.0 * DT_ALPHA) * rho
    if not (cp > 0.0) or not math.isfinite(alpha):
        return st.Stop("refused", _refusal(view, p, t, f"source {sid} fails the physical checks (c_P {cp}, α {alpha})"))
    return rho, alpha * t / (rho * cp)
