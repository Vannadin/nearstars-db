# 광물 집합 기록 — SLB 집합 표를 읽는 물질 기록의 조성 지문과 뷰 (phase-2 규산염 기록 등록 §2–§3)
"""The assemblage-kind material record (rewrite/phase2-silicate-record-registration.frozen.md §2–§3).

`composition_key(oxides_wt)` is the composition fingerprint a record carries and the resolver matches (§2.1, §4):
the CFMASNa reduction of the declared oxide wt % (normalised to 100, as the builder's `cfmasna`, build declaration §2,
and legacy `mantle_composition.cfmasna`), each rounded to 1e-12, hashed as sorted JSON; the first 16 hex of its
sha256. The generator (rewrite/phase2-records/gen_silicate_records.py) writes the key with this function, so a
layer's declared oxides and a record's key cannot drift; one changed oxide misses (§7 item 10).
"""
from __future__ import annotations

import hashlib
import json
import math

#: the six oxides the build keeps (build declaration §2), in the builder's order
CFMASNA = ("CaO", "FeO", "MgO", "Al2O3", "SiO2", "Na2O")


def cfmasna(oxides_wt) -> dict:
    """The CFMASNa wt %, normalised to 100 (builder `cfmasna`; legacy mantle_composition.cfmasna)."""
    sub = {k: float(oxides_wt[k]) for k in CFMASNA}
    s = math.fsum(sub.values())
    return {k: v * 100.0 / s for k, v in sub.items()}


def composition_key(oxides_wt) -> str:
    """The fingerprint: sha256 of {"composition_cfmasna_wt": {oxide: round(wt, 12)}} as sorted JSON, first 16 hex."""
    body = {"composition_cfmasna_wt": {k: round(v, 12) for k, v in cfmasna(oxides_wt).items()}}
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]


# ── the compact table and its load checks (registration §2.2–§2.3; post-freeze note 3 §3) ────────────────────────────
WINDOW_CAUSES = ("grid_end", "bound_cut", "eos_edge", "solidus_cap")
CELL_KINDS = ("equilibrium", "extrapolated", "above_solidus", "frozen")


class TableStop(Exception):
    """A load check the compact table fails; the registry turns it into `material.assemblage_table`."""


def read_table(path, sha256: str) -> dict:
    """The compact table at `path`, after its sha256 matches the record's pin (§2.2: only the compact sha256 can be
    checked at engine load; a mismatch is a STOP, never a fallback)."""
    try:
        data = open(path, "rb").read()
    except OSError as e:
        raise TableStop(f"the compact table {path} cannot be read: {e}") from None
    got = hashlib.sha256(data).hexdigest()
    if got != sha256:
        raise TableStop(f"the compact table's sha256 is {got}, not the record's pinned {sha256}")
    try:
        return json.loads(data)
    except ValueError as e:
        raise TableStop(f"the compact table is not JSON: {e}") from None


def _one_state(a, b) -> bool:
    """r2 H6: the same label, and both non-frozen, or both frozen with the same freeze_t."""
    if a["assemblage"] != b["assemblage"]:
        return False
    fa, fb = a["kind"] == "frozen", b["kind"] == "frozen"
    return (not fa and not fb) or (fa and fb and a["freeze_t"] == b["freeze_t"])


#: the Maxwell scale's floor [1/K]: as the registry's ALPHA_FLOOR (68 N61), so a residual is not divided by a ∂v/∂T
#: passing through 0 (the plagioclase-out loop, where ∂(1/ρ)/∂T changes sign)
ALPHA_FLOOR = 1.0e-6


def _d3(xm, x0, xp, fm, f0, fp):
    """The second-order 3-point derivative at x0 on a non-uniform grid (the P grid is 1.5× per node below 0.1 GPa,
    then a 1.5 % step to 0.1 GPa, then 5 %; a two-point (hi − lo)/(x_hi − x_lo) is first order there)."""
    hm, hp = x0 - xm, xp - x0
    return (-hp / (hm * (hm + hp))) * fm + ((hp - hm) / (hm * hp)) * f0 + (hm / (hp * (hm + hp))) * fp


def _maxwell_residual(by, ps, ts, i, k, d):
    """The signed Maxwell residual (∂(1/ρ)/∂T + ∂S/∂P) / max(|∂(1/ρ)/∂T|, |∂S/∂P|, ALPHA_FLOOR/ρ) at node (i, k),
    over ±d nodes; None where the stencil leaves the grid, leaves the cell's state, or meets a frozen cell."""
    if i - d < 0 or i + d >= len(ps) or k - d < 0 or k + d >= len(ts):
        return None
    c = by.get((ps[i], ts[k]))
    nb = [by.get(x) for x in ((ps[i - d], ts[k]), (ps[i + d], ts[k]), (ps[i], ts[k - d]), (ps[i], ts[k + d]))]
    if c is None or any(n is None or n["kind"] == "frozen" or not _one_state(n, c) for n in nb):
        return None
    lp, hp, lt, ht = nb
    dv_dt = _d3(lt["t"], c["t"], ht["t"], 1.0 / lt["rho"], 1.0 / c["rho"], 1.0 / ht["rho"])
    ds_dp = _d3(lp["p"], c["p"], hp["p"], lp["s"], c["s"], hp["s"])
    return (dv_dt + ds_dp) / max(abs(dv_dt), abs(ds_dp), ALPHA_FLOOR / c["rho"])


#: the stored-value gate (r2's ruling on the 1 % bump finding; registration note 3 §3): every stored field the engine
#: reads, on every cell, within this of the model's value from the dT/dP sidecar (non-frozen: the centre re-solve;
#: frozen: the fixed state re-evaluated), relative (s against max(|s|, 1)). Measured ≤ 1.4e-8 before it was set.
STORED_MODEL_REL = 1.0e-6
MODEL_FIELDS = ("rho", "s", "c_p", "c_v", "alpha_k_t", "gamma", "dtdp_s")
#: each field's declared scale floor in the gate's denominator max(|x|, floor) (r2 NB 3 on c1907476: no field divides
#: by a value that can approach 0). Each is far below the field's values in the tables (ρ ~3e3 kg/m³, c_P and c_V
#: ~1e3 J/kg/K, αK_T ~1e6 Pa/K, γ ~1, dtdp_s ~1e-8 K/Pa); s is the one that crosses 0, as before.
FIELD_SCALE = {"rho": 1.0, "s": 1.0, "c_p": 1.0, "c_v": 1.0, "alpha_k_t": 1.0, "gamma": 1e-3, "dtdp_s": 1e-12}


def _model_miss(c):
    """The worst relative stored-against-model difference at a cell, and its field; None without model values."""
    worst = (0.0, None)
    for f in MODEL_FIELDS:
        m = c.get(f"{f}_model")
        if m is None:
            return None
        d = abs(c[f] - m) / max(abs(c[f]), FIELD_SCALE[f])
        if d > worst[0]:
            worst = (d, f)
    return worst


def _exact_maxwell(c):
    """The model's own Maxwell residual at a cell, from the dT/dP sidecar's four ±δ solves; None without them."""
    dv, ds = c.get("dv_dt_model"), c.get("ds_dp_model")
    if dv is None or ds is None:
        return None
    return abs(dv + ds) / max(abs(dv), abs(ds), ALPHA_FLOOR / c["rho"])


def _fd_blind(by, ps, ts, i, k, d1, b3):
    """None when an FD Maxwell failure at node (i, k) is FD's (exact ≤ FD/10, and stored = model to 1e-6 at the cell
    and at every node of its ±1 and ±2 stencils); else why it is not excused."""
    c = by[(ps[i], ts[k])]
    e = _exact_maxwell(c)
    if e is None:
        return "no exact derivatives at the cell"
    if e > d1 / 10.0:
        return f"the model's exact Maxwell {e:.4g} is not ≤ FD/10"
    for d in (0, 1, 2):
        for a, b in (((0, 0),) if d == 0 else ((-d, 0), (d, 0), (0, -d), (0, d))):
            n = by[(ps[i + a], ts[k + b])]
            miss = _model_miss(n)
            if miss is None:
                return f"node ({n['p']:g}, {n['t']:g}) has no model value"
            if miss[0] > STORED_MODEL_REL:
                return f"node ({n['p']:g}, {n['t']:g}): stored {miss[1]} differs from the model's beyond {STORED_MODEL_REL:g}"
    return None


def band(a, g, dtdp_s, floor):
    """The model-consistency band (S-based against G-based isentrope from the same solver), r2's ruling (α); the same
    formula as the sidecar's (rewrite/phase2-records/slb2024/dtdp_eq.py `band`)."""
    return max(floor, abs(a - g) / max(abs(a), abs(dtdp_s)))


def _finite(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def check_table(asm, table) -> dict:
    """§2.3's B3 on a compact assemblage table, as post-freeze note 3 §3 amends it. Raises TableStop at the first gate
    a table fails; returns the report-only figures. `asm` is the record's `assemblage` block (its `b3` numbers were
    declared before the first load)."""
    b3 = asm["b3"]
    cells = table.get("cells")
    if not isinstance(cells, list) or not cells:
        raise TableStop("the compact table has no cells")
    by = {}
    for c in cells:
        if c.get("kind") not in CELL_KINDS:
            raise TableStop(f"cell ({c.get('p')}, {c.get('t')}): kind {c.get('kind')!r}")
        for f in ("rho", "s", "c_p", "c_v", "alpha_k_t", "gamma", "dtdp_s"):
            v = c.get(f)
            if not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v):
                raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): {f} is {v!r}, not a finite number")
        by[(c["p"], c["t"])] = c
    if len(by) != len(cells):
        raise TableStop("two cells share a node")
    # the stored-value gate: every stored field the engine reads, on every cell, against the model (r2; note 3 §3).
    # A cell with no model value (its sidecar re-solve failed) is not covered by it: a STOP for a ruling, never shipped
    # silently uncovered (r2 condition 2)
    misses, uncovered, stored = [], [], []
    for c in cells:
        m = _model_miss(c)
        if m is None:
            uncovered.append((c["p"], c["t"], c["kind"]))
        else:
            stored.append(m[0])
            if m[0] > STORED_MODEL_REL:
                misses.append((c["p"], c["t"], m[1], m[0]))
    if misses:
        raise TableStop(f"{len(misses)} cells' stored values differ from the model's beyond {STORED_MODEL_REL:g}: "
                        + "; ".join(f"({p:g}, {t:g}) {f} {d:.3g}" for p, t, f, d in misses[:20]))
    if uncovered:
        raise TableStop(f"{len(uncovered)} cells have no model values, so the stored-value gate cannot cover them "
                        "(a ruling is needed before the table ships): "
                        + "; ".join(f"({p:g}, {t:g}) {k}" for p, t, k in uncovered[:20]))
    ps = sorted({p for p, _ in by})
    ts = sorted({t for _, t in by})
    pi = {p: i for i, p in enumerate(ps)}
    cols = {c["p"]: c for c in table.get("columns", ())}
    if sorted(cols) != ps:
        raise TableStop("the column list does not match the cells' P nodes")
    # no holes: every node from the grid's first T up to the column's window top
    for p, col in cols.items():
        if col.get("window", {}).get("cause") not in WINDOW_CAUSES:
            raise TableStop(f"column {p:g}: window cause {col.get('window')!r}")
        top = col["t_window_top"]
        have = [t for t in ts if (p, t) in by]
        if not have or have[-1] != top:
            raise TableStop(f"column {p:g}: its last cell is not its window top {top}")
        for t in ts:
            if t <= top and (p, t) not in by:
                raise TableStop(f"a hole at ({p:g}, {t:g}), below the column's window top {top}")
    # positivity and the γ identity (interim internal check, note 3 §3)
    for c in cells:
        if not (c["c_p"] > 0.0 and c["c_v"] > 0.0 and c["alpha_k_t"] > 0.0 and c["dtdp_s"] > 0.0):
            raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): c_P, c_V, αK_T and dtdp_s must be > 0")
        g = c["alpha_k_t"] / (c["rho"] * c["c_v"])
        if abs(g - c["gamma"]) > b3["gamma_tolerance"] * abs(c["gamma"]):
            raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): γ {c['gamma']!r} against αK_T/(ρc_V) {g!r}")
    # ρ rises with P along every isotherm, for pairs in one state (r2 H6); cross-state frozen pairs are reported
    cross = []
    for t in ts:
        for a, b in zip(ps, ps[1:]):
            ca, cb = by.get((a, t)), by.get((b, t))
            if ca is None or cb is None or cb["rho"] > ca["rho"]:
                continue
            if _one_state(ca, cb):
                raise TableStop(f"ρ does not rise with P at {t:g} K between {a:g} and {b:g} Pa in one state "
                                f"({ca['assemblage']})")
            if ca["kind"] == "frozen" or cb["kind"] == "frozen":
                cross.append((a, b, t, cb["rho"] / ca["rho"] - 1.0))
    # frozen cells: the in-column identity α = −∂lnρ/∂T against dtdp_s·ρc_P/T (note 3 §3, gate)
    frozen_max = 0.0
    for c in cells:
        if c["kind"] != "frozen":
            continue
        k = ts.index(c["t"])
        lo = by.get((c["p"], ts[k - 1])) if k > 0 else None
        hi = by.get((c["p"], ts[k + 1])) if k + 1 < len(ts) else None
        if lo is None or hi is None or not (_one_state(lo, c) and _one_state(c, hi)):
            continue
        alpha = -(math.log(hi["rho"]) - math.log(lo["rho"])) / (hi["t"] - lo["t"])
        want = c["dtdp_s"] * c["rho"] * c["c_p"] / c["t"]
        r = abs(alpha - want) / abs(want)
        frozen_max = max(frozen_max, r)
        if r > b3["frozen_alpha_tolerance"]:
            raise TableStop(f"frozen cell ({c['p']:g}, {c['t']:g}): α {alpha:.6g} against dtdp_s·ρc_P/T {want:.6g}, "
                            f"beyond {b3['frozen_alpha_tolerance']:g}")
    # Maxwell, gated per cell on 5-point interior cells against the cell's own truncation estimate (note 3 §3). An FD
    # failure is excused («FD blind: kink inside the stencil») only if the model's exact Maxwell there is ≤ FD/10 and
    # the stored ρ and s equal the model's to 1e-6 at the cell and every node of its stencils (r2's rulings)
    gated, blind, worst, excused = 0, [], 0.0, []
    for c in cells:
        if c["kind"] == "frozen":
            continue
        i, k = pi[c["p"]], ts.index(c["t"])
        d1 = _maxwell_residual(by, ps, ts, i, k, 1)
        d2 = _maxwell_residual(by, ps, ts, i, k, 2)
        if d1 is None or d2 is None:
            continue
        tol = b3["maxwell_k"] * abs(d1 - d2) + b3["maxwell_floor"]
        d1 = abs(d1)
        gated += 1
        worst = max(worst, d1)
        if tol > 1e-2:
            blind.append((c["p"], c["t"], tol))
        if d1 <= tol:
            continue
        why = _fd_blind(by, ps, ts, i, k, d1, b3)
        if why is not None:
            raise TableStop(f"Maxwell at ({c['p']:g}, {c['t']:g}): residual {d1:.4g} beyond "
                            f"{b3['maxwell_k']:g}·|D_h − D_2h| + {b3['maxwell_floor']:g} = {tol:.4g}, not excused: {why}")
        excused.append((c["p"], c["t"], d1, _exact_maxwell(c)))
    # the dT/dP field: the equilibrium isentrope on non-frozen cells, dtdp_s on frozen ones (note 3 §2)
    refused = {(r["p"], r["t"]) for r in table.get("dtdp_eq_refused", ())}
    for c in cells:
        v = c.get("dtdp_eq")
        if c["kind"] == "frozen":
            if v != c["dtdp_s"] or c.get("dtdp_eq_from") != "frozen: dtdp_s":
                raise TableStop(f"frozen cell ({c['p']:g}, {c['t']:g}): its dT/dP field is not its dtdp_s")
        elif v is None:
            if (c["p"], c["t"]) not in refused:
                raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): no dT/dP and not listed as refused")
        elif not all(_finite(c.get(f)) for f in ("dtdp_eq_band", "dtdp_g", "envelope_gap_v", "envelope_gap_s")):
            raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): its band, G-based isentrope or envelope gap is missing")
        elif abs(c["dtdp_eq_band"] - band(c["dtdp_eq"], c["dtdp_g"], c["dtdp_s"], asm["dtdp"]["band_floor"])) \
                > 1e-12 * c["dtdp_eq_band"]:
            raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): dT/dP band {c['dtdp_eq_band']!r} is not its "
                            f"recomputation from A, G and the floor {asm['dtdp']['band_floor']:g}")
        elif not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v) \
                or c.get("dtdp_eq_from") != "model" or (c["p"], c["t"]) in refused:
            raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): dT/dP field {v!r} ({c.get('dtdp_eq_from')!r})")
    if len(refused) != sum(1 for c in cells if c["kind"] != "frozen" and c.get("dtdp_eq") is None):
        raise TableStop("the refused dT/dP list names a cell that has a value or is not in the table")
    if asm["dtdp"]["refused_count"] != len(refused):
        raise TableStop(f"the record says {asm['dtdp']['refused_count']} refused dT/dP cells, the table lists "
                        f"{len(refused)}")
    exact = sorted(e for e in (_exact_maxwell(c) for c in cells if c["kind"] != "frozen") if e is not None)
    q = (lambda f: exact[min(len(exact) - 1, int(f * (len(exact) - 1)))]) if exact else (lambda f: None)
    return {"stored_model": {"n": len(stored), "median": sorted(stored)[len(stored) // 2] if stored else None,
                             "max": max(stored) if stored else None},
            "maxwell_gated": gated, "maxwell_worst": worst, "maxwell_blind": blind, "maxwell_fd_blind": excused,
            "exact_maxwell": {"n": len(exact), "median": q(0.5), "p99": q(0.99), "max": q(1.0)},
            "frozen_alpha_max": frozen_max, "cross_state_inversions": cross, "dtdp_eq_refused": len(refused)}


#: the fields a planted single-field bump is tried on, per cell kind (r2 condition 3: coverage per field)
BUMP_FIELDS = MODEL_FIELDS + ("dtdp_eq", "dtdp_g", "dtdp_eq_band")


def _caught_by(why: str) -> str:
    for key, name in (("differ from the model", "stored-value gate"), ("recomputation", "band recompute"),
                      ("γ", "γ identity"), ("frozen cell", "frozen in-column identity"), ("Maxwell", "FD Maxwell"),
                      ("ρ does not rise", "ρ rises with P"), ("dT/dP field", "dT/dP field rule"),
                      ("must be > 0", "positivity")):
        if key in why:
            return name
    return why[:60]


def planted_coverage(asm, table, per=5, seed=0, rel=0.01):
    """r2 conditions 2–3: for every field the engine reads × cell kind, plant a single-field bump of `rel` at up to
    `per` seeded cells (and at every cell with no model values) and record which check catches it. Returns
    {(field, kind): {"tried": n, "caught": n, "by": {check: n}, "missed": [(p, t)]}}. Report-only: the load gate is
    check_table; this is the evidence that it covers each pair."""
    import copy
    import random
    rng = random.Random(seed)
    out = {}
    kinds = sorted({c["kind"] for c in table["cells"]})
    for f in BUMP_FIELDS:
        for k in kinds:
            pool = [i for i, c in enumerate(table["cells"]) if c["kind"] == k and _finite(c.get(f))]
            if f in ("dtdp_eq", "dtdp_g", "dtdp_eq_band") and k == "frozen" and f != "dtdp_eq":
                continue
            pick = sorted(rng.sample(pool, min(per, len(pool))))
            row = {"tried": 0, "caught": 0, "by": {}, "missed": []}
            for i in pick:
                t2 = copy.deepcopy(table)
                t2["cells"][i][f] *= 1.0 + rel
                row["tried"] += 1
                try:
                    check_table(asm, t2)
                    row["missed"].append((t2["cells"][i]["p"], t2["cells"][i]["t"]))
                except TableStop as e:
                    row["caught"] += 1
                    name = _caught_by(str(e))
                    row["by"][name] = row["by"].get(name, 0) + 1
            out[(f, k)] = row
    return out
