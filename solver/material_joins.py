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
- not_printed: 0, never a stand-in.
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


def source_sigma(view, pi, sid, p, t) -> float:
    """Relative 1σ of ρ for source `sid` at (P, T)."""
    src = _src(view, pi, sid)
    sg = src["sigma"]
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
