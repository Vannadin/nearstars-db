# 광물 집합 기록 — SLB 집합 표를 읽는 물질 기록의 조성 지문과 뷰 (phase-2 규산염 기록 등록 §2–§3)
"""The assemblage-kind material record (rewrite/phase2-silicate-record-registration.frozen.md §2–§3).

`composition_key(oxides_wt)` is the composition fingerprint a record carries and the resolver matches (§2.1, §4):
the CFMASNa reduction of the declared oxide wt % (normalised to 100, as the builder's `cfmasna`, build declaration §2,
and legacy `mantle_composition.cfmasna`), each rounded to 1e-12, hashed as sorted JSON; the first 16 hex of its
sha256. The generator (rewrite/phase2-records/gen_silicate_records.py) writes the key with this function, so a
layer's declared oxides and a record's key cannot drift; one changed oxide misses (§7 item 10).
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
from collections.abc import Sequence
from types import MappingProxyType

from solver import material_view as mv
from solver import stepper as st
from solver.result import freeze

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
#: the boundary export's states (registration §3.3): pending until the boundary pass lands, then exported
BOUNDARY_STATUS = ("pending", "exported")
CELL_KINDS = ("equilibrium", "extrapolated", "above_solidus", "frozen")


class TableStop(Exception):
    """A load check the compact table fails; the registry turns it into `material.assemblage_table`. `check` names
    the check (read by planted_coverage; control flow never reads the text, X3)."""

    def __init__(self, why: str, check: str = "table"):
        super().__init__(why)
        self.check = check


def read_table(path, sha256: str) -> dict:
    """The compact table at `path`, after its sha256 matches the record's pin (§2.2: only the compact sha256 can be
    checked at engine load; a mismatch is a STOP, never a fallback)."""
    from pathlib import Path
    try:
        data = Path(path).read_bytes()
    except OSError as e:
        raise TableStop(f"the compact table {path} cannot be read: {e}", check="read") from None
    got = hashlib.sha256(data).hexdigest()
    if got != sha256:
        raise TableStop(f"the compact table's sha256 is {got}, not the record's pinned {sha256}", check="sha pin")
    try:
        return json.loads(data)
    except ValueError as e:
        raise TableStop(f"the compact table is not JSON: {e}", check="read") from None


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
FIELD_SCALE = MappingProxyType({"rho": 1.0, "s": 1.0, "c_p": 1.0, "c_v": 1.0, "alpha_k_t": 1.0, "gamma": 1e-3,
                                "dtdp_s": 1e-12})        # read-only (phase1-design §A6: no mutable module state)


def _model_miss(c):
    """The worst relative stored-against-model difference at a cell, and its field; None without model values. The
    model group is all None or all finite numbers: anything else is a STOP (68 B1 on 2a5af2db: a NaN made every
    comparison False and so turned the gate off)."""
    ms = [c.get(f"{f}_model") for f in MODEL_FIELDS]
    if all(m is None for m in ms):
        return None
    if not all(_finite(m) for m in ms):
        raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): its model values are neither all absent nor all finite "
                        f"numbers: {ms!r}", check="finite fields")
    worst = (0.0, None)
    for f, m in zip(MODEL_FIELDS, ms):
        d = abs(c[f] - m) / max(abs(c[f]), FIELD_SCALE[f])
        if d > worst[0]:
            worst = (d, f)
    return worst


def _exact_maxwell(c):
    """The model's own Maxwell residual at a cell, from the dT/dP sidecar's four ±δ solves; None without them."""
    dv, ds = c.get("dv_dt_model"), c.get("ds_dp_model")
    if dv is None and ds is None:
        return None
    if not (_finite(dv) and _finite(ds)):                 # 68 B1: a NaN must never excuse a cell
        raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): its exact derivatives are neither both absent nor both "
                        f"finite numbers: {dv!r}, {ds!r}", check="finite fields")
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
    # a belt behind the global stored-value gate, which already STOPs on any miss (68 N1 on 2a5af2db): kept so the
    # excuse states its own condition (r2) even if that gate is ever moved after this check
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
    if isinstance(cells, (str, bytes)) or not isinstance(cells, Sequence) or not cells:   # a list, or the registry's
        raise TableStop("the compact table has no cells", check="structure")                                  # frozen tuple (68)
    by = {}
    for c in cells:
        if not (_finite(c.get("p")) and _finite(c.get("t"))):          # 68 N2: numbers before any arithmetic
            raise TableStop(f"a cell's node is not a pair of finite numbers: ({c.get('p')!r}, {c.get('t')!r})", check="finite fields")
        for f in ("dtdp_eq", "dtdp_g", "dtdp_eq_band", "envelope_gap_v", "envelope_gap_s"):
            if c.get(f) is not None and not _finite(c[f]):
                raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): {f} is {c[f]!r}, not a finite number or absent", check="finite fields")
        if c.get("kind") not in CELL_KINDS:
            raise TableStop(f"cell ({c.get('p')}, {c.get('t')}): kind {c.get('kind')!r}", check="structure")
        for f in ("rho", "s", "c_p", "c_v", "alpha_k_t", "gamma", "dtdp_s"):
            v = c.get(f)
            if not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v):
                raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): {f} is {v!r}, not a finite number", check="finite fields")
        by[(c["p"], c["t"])] = c
    if len(by) != len(cells):
        raise TableStop("two cells share a node", check="structure")
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
                        + "; ".join(f"({p:g}, {t:g}) {f} {d:.3g}" for p, t, f, d in misses[:20]), check="stored-value gate")
    if uncovered:
        raise TableStop(f"{len(uncovered)} cells have no model values, so the stored-value gate cannot cover them "
                        "(a ruling is needed before the table ships): "
                        + "; ".join(f"({p:g}, {t:g}) {k}" for p, t, k in uncovered[:20]), check="stored-value gate")
    ps = sorted({p for p, _ in by})
    ts = sorted({t for _, t in by})
    pi = {p: i for i, p in enumerate(ps)}
    # the grid assumptions the view relies on (68 B1 on 2390a7e2): every column starts at the T floor; p_dataset is a
    # P node, so the one-sided cut falls on a node and a read below it never extrapolates past the grid
    if ts[0] != T_FLOOR:
        raise TableStop(f"the grid's first T node is {ts[0]:g} K, not the view's floor {T_FLOOR:g} K", check="structure")
    if (table.get("boundaries") or {}).get("status") not in BOUNDARY_STATUS:     # read by the resolver (68 S3)
        raise TableStop(f"boundaries.status is {(table.get('boundaries') or {}).get('status')!r}, not one of "
                        f"{BOUNDARY_STATUS}", check="structure")
    if table.get("p_dataset") not in ps:
        raise TableStop(f"p_dataset {table.get('p_dataset')!r} is not a P node of the table", check="structure")
    cols = {c["p"]: c for c in table.get("columns", ())}
    if len(cols) != len(table.get("columns", ())):                   # 68 N3: duplicates would collapse unseen
        raise TableStop("two columns share a P node", check="structure")
    if sorted(cols) != ps:
        raise TableStop("the column list does not match the cells' P nodes", check="structure")
    # no holes: every node from the grid's first T up to the column's window top
    for p, col in cols.items():
        if col.get("window", {}).get("cause") not in WINDOW_CAUSES:
            raise TableStop(f"column {p:g}: window cause {col.get('window')!r}", check="structure")
        top = col["t_window_top"]
        have = [t for t in ts if (p, t) in by]
        if not have or have[-1] != top:
            raise TableStop(f"column {p:g}: its last cell is not its window top {top}", check="structure")
        for t in ts:
            if t <= top and (p, t) not in by:
                raise TableStop(f"a hole at ({p:g}, {t:g}), below the column's window top {top}", check="structure")
    # positivity and the γ identity (interim internal check, note 3 §3)
    for c in cells:
        if not (c["c_p"] > 0.0 and c["c_v"] > 0.0 and c["alpha_k_t"] > 0.0 and c["dtdp_s"] > 0.0):
            raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): c_P, c_V, αK_T and dtdp_s must be > 0", check="positivity")
        g = c["alpha_k_t"] / (c["rho"] * c["c_v"])
        if abs(g - c["gamma"]) > b3["gamma_tolerance"] * abs(c["gamma"]):
            raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): γ {c['gamma']!r} against αK_T/(ρc_V) {g!r}", check="γ identity")
    # ρ rises with P along every isotherm, for pairs in one state (r2 H6); cross-state frozen pairs are reported
    cross = []
    for t in ts:
        for a, b in zip(ps, ps[1:]):
            ca, cb = by.get((a, t)), by.get((b, t))
            if ca is None or cb is None or cb["rho"] > ca["rho"]:
                continue
            if _one_state(ca, cb):
                raise TableStop(f"ρ does not rise with P at {t:g} K between {a:g} and {b:g} Pa in one state "
                                f"({ca['assemblage']})", check="ρ rises with P")
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
                            f"beyond {b3['frozen_alpha_tolerance']:g}", check="frozen in-column identity")
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
                            f"{b3['maxwell_k']:g}·|D_h − D_2h| + {b3['maxwell_floor']:g} = {tol:.4g}, not excused: {why}", check="FD Maxwell")
        excused.append((c["p"], c["t"], d1, _exact_maxwell(c)))
    # the dT/dP field: the equilibrium isentrope on non-frozen cells, dtdp_s on frozen ones (note 3 §2)
    refused = {(r["p"], r["t"]) for r in table.get("dtdp_eq_refused", ())}
    for k in refused:                                    # each refused entry names a non-frozen cell of the table
        if k not in by or by[k]["kind"] == "frozen" or by[k].get("dtdp_eq") is not None:
            raise TableStop(f"the refused dT/dP list names {k}, which is not a non-frozen cell without a value", check="dT/dP field rule")
    for c in cells:
        v = c.get("dtdp_eq")
        if c["kind"] == "frozen":
            if v != c["dtdp_s"] or c.get("dtdp_eq_from") != "frozen: dtdp_s":
                raise TableStop(f"frozen cell ({c['p']:g}, {c['t']:g}): its dT/dP field is not its dtdp_s", check="dT/dP field rule")
        elif v is None:
            if (c["p"], c["t"]) not in refused:
                raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): no dT/dP and not listed as refused", check="dT/dP field rule")
        elif not all(_finite(c.get(f)) for f in ("dtdp_eq_band", "dtdp_g", "envelope_gap_v", "envelope_gap_s")):
            raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): its band, G-based isentrope or envelope gap is missing", check="dT/dP field rule")
        elif abs(c["dtdp_eq_band"] - band(c["dtdp_eq"], c["dtdp_g"], c["dtdp_s"], asm["dtdp"]["band_floor"])) \
                > 1e-12 * c["dtdp_eq_band"]:
            raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): dT/dP band {c['dtdp_eq_band']!r} is not its "
                            f"recomputation from A, G and the floor {asm['dtdp']['band_floor']:g}", check="band recompute")
        elif not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v) \
                or c.get("dtdp_eq_from") != "model" or (c["p"], c["t"]) in refused:
            raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): dT/dP field {v!r} ({c.get('dtdp_eq_from')!r})", check="dT/dP field rule")
    if asm["dtdp"]["refused_count"] != len(refused):
        raise TableStop(f"the record says {asm['dtdp']['refused_count']} refused dT/dP cells, the table lists "
                        f"{len(refused)}", check="dT/dP field rule")
    exact = sorted(e for e in (_exact_maxwell(c) for c in cells if c["kind"] != "frozen") if e is not None)
    q = (lambda f: exact[min(len(exact) - 1, int(f * (len(exact) - 1)))]) if exact else (lambda f: None)
    return {"stored_model": {"n": len(stored), "median": sorted(stored)[len(stored) // 2] if stored else None,
                             "max": max(stored) if stored else None},
            "maxwell_gated": gated, "maxwell_worst": worst, "maxwell_blind": blind, "maxwell_fd_blind": excused,
            "exact_maxwell": {"n": len(exact), "median": q(0.5), "p99": q(0.99), "max": q(1.0)},
            "frozen_alpha_max": frozen_max, "cross_state_inversions": cross, "dtdp_eq_refused": len(refused)}


#: the fields a planted single-field bump is tried on, per cell kind (r2 condition 3: coverage per field)
BUMP_FIELDS = MODEL_FIELDS + ("dtdp_eq", "dtdp_g", "dtdp_eq_band")


def planted_coverage(asm, table, per=5, seed=0, rel=0.01):
    """r2 conditions 2–3: for every field the engine reads × cell kind, plant a single-field bump of `rel` at up to
    `per` seeded cells (and at every cell with no model values) and record which check catches it. Returns
    {(field, kind): {"tried": n, "caught": n, "by": {check: n}, "missed": [(p, t)]}}. Report-only: the load gate is
    check_table; this is the evidence that it covers each pair."""
    import random
    table = mv.thaw_plain(table)                     # the registry hands the table out frozen (68 on 2922f022)
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
                    name = e.check
                    row["by"][name] = row["by"].get(name, 0) + 1
            out[(f, k)] = row
    return out


# ── C¹ interpolation: a port of legacy engine/smooth_table.py (prereg-c157 note 10) ─────────────────────────────────
# Monotone piecewise-cubic Hermite (Fritsch & Carlson 1980; PCHIP slopes) on non-uniform grids, tensor product in
# (ln P, T): along T on each of the stencil's P rows, then along ln P through those values. A missing node *outside*
# the query cell is replaced, for slope estimation only, by linear extrapolation from its row's nearest real node along
# that row's PCHIP end slope (audit e2: the stencil shape never changes, so C¹ holds next to ragged column tops); a
# missing corner of the query cell is a CellMissing, never a value. On a grid line a zero-weight end is not read
# (smooth_table's rule). Ported, not imported: the solver imports engine/ only through legacy_materials (design §L).
class CellMissing(Exception):
    """A corner of the query cell has no value: (axis-a index, axis-b index) of the corner."""


def _end_slope(h0, h1, d0, d1):
    s = ((2.0 * h0 + h1) * d0 - h0 * d1) / (h0 + h1)
    if s * d0 <= 0.0:
        return 0.0
    if d0 * d1 < 0.0 and abs(s) > 3.0 * abs(d0):
        return 3.0 * d0
    return s


def _inner_slope(h0, h1, d0, d1):
    if d0 * d1 <= 0.0:
        return 0.0
    w1, w2 = 2.0 * h1 + h0, h1 + 2.0 * h0
    return (w1 + w2) / (w1 / d0 + w2 / d1)


def _coeffs(xs, ys, i):
    y0, y1 = ys[i], ys[i + 1]
    if y0 is None or y1 is None:
        raise CellMissing(i)
    x0, x1 = xs[i], xs[i + 1]
    h = x1 - x0
    d = (y1 - y0) / h
    has_l = i - 1 >= 0 and ys[i - 1] is not None
    has_r = i + 2 < len(xs) and ys[i + 2] is not None
    if has_l:
        hl = x0 - xs[i - 1]
        m0 = _inner_slope(hl, h, (y0 - ys[i - 1]) / hl, d)
    elif has_r:
        hr = xs[i + 2] - x1
        m0 = _end_slope(h, hr, d, (ys[i + 2] - y1) / hr)
    else:
        m0 = d
    if has_r:
        hr = xs[i + 2] - x1
        m1 = _inner_slope(h, hr, d, (ys[i + 2] - y1) / hr)
    elif has_l:
        hl = x0 - xs[i - 1]
        m1 = _end_slope(h, hl, d, (y0 - ys[i - 1]) / hl)
    else:
        m1 = d
    return x0, h, y0, y1, m0, m1


def _hermite(x, c):
    x0, h, y0, y1, m0, m1 = c
    u = (x - x0) / h
    u2, u3 = u * u, u * u * u
    return ((2.0 * u3 - 3.0 * u2 + 1.0) * y0 + (u3 - 2.0 * u2 + u) * h * m0
            + (-2.0 * u3 + 3.0 * u2) * y1 + (u3 - u2) * h * m1)


def _cubic1(x, xs, ys, i):
    y0, y1 = ys[i], ys[i + 1]
    u = (x - xs[i]) / (xs[i + 1] - xs[i])
    if u == 0.0 and y0 is not None:
        return y0
    if u == 1.0 and y1 is not None:
        return y1
    if y0 is None or y1 is None:
        raise CellMissing(i)
    return _hermite(x, _coeffs(xs, ys, i))


class _Seq:
    """Index → value or None (absent keys and out-of-range read None)."""
    __slots__ = ("d", "n")

    def __init__(self, d, n):
        self.d, self.n = d, n

    def __len__(self):
        return self.n

    def __getitem__(self, k):
        return self.d.get(k)


def _extrapolate(val, ka, kb, ib, n):
    """smooth_table `_extrapolate`: a missing outer node (ka, kb) from its row's nearest real node along the row's
    PCHIP end slope, the slope taken per index."""
    k = None
    for dist in range(1, n):
        cands = [kb + dist, kb - dist] if kb <= ib else [kb - dist, kb + dist]
        for c in cands:
            if 0 <= c < n and val(ka, c) is not None:
                k = c
                break
        if k is not None:
            break
    if k is None:
        return None
    step = 1 if k > kb else -1
    y0 = val(ka, k)
    y1 = val(ka, k + step) if 0 <= k + step < n else None
    y2 = val(ka, k + 2 * step) if 0 <= k + 2 * step < n else None
    if y1 is None:
        return y0
    d0 = (y1 - y0) / step
    d1 = (y2 - y1) / step if y2 is not None else d0
    m = -_end_slope(1.0, 1.0, -d0, -d1) if step > 0 else _end_slope(1.0, 1.0, d0, d1)
    return y0 + m * (kb - k)


def cubic2(xa, xb, xs_a, xs_b, val, ia, ib, rows_allowed=None):
    """Value at (xa, xb) in cell [ia, ia+1] × [ib, ib+1]; `val(ka, kb)` gives a node value or None. `rows_allowed(ka)`
    False drops a first-axis row from the stencil entirely (the one-sided cut at p_dataset): the first-axis
    interpolation then goes one-sided there, as at a table end. A missing corner raises CellMissing((ka, kb))."""
    na, nb = len(xs_a), len(xs_b)
    rows = {}
    for ka in range(ia - 1, ia + 3):
        if not 0 <= ka < na or (rows_allowed is not None and not rows_allowed(ka)):
            continue
        need = ka in (ia, ia + 1)
        col = {}
        for kb in range(ib - 1, ib + 3):
            if not 0 <= kb < nb:
                continue
            v = val(ka, kb)
            if v is None and not (need and kb in (ib, ib + 1)):
                v = _extrapolate(val, ka, kb, ib, nb)
            col[kb] = v
        seq = _Seq(col, nb)
        try:
            rows[ka] = _cubic1(xb, xs_b, seq, ib)
        except CellMissing:
            if need:
                u = (xa - xs_a[ia]) / (xs_a[ia + 1] - xs_a[ia])
                if (ka == ia and u == 1.0) or (ka == ia + 1 and u == 0.0):
                    continue                        # a zero-weight row is not read (smooth_table's grid-line rule)
                missing = next(kb for kb in (ib, ib + 1) if col.get(kb) is None)
                raise CellMissing((ka, missing)) from None
    try:
        return _cubic1(xa, xs_a, _Seq(rows, na), ia)
    except CellMissing as e:
        raise CellMissing((e.args[0], ib)) from None


# ── the view (registration §3; post-freeze note 3 §1, §4) ───────────────────────────────────────────────────────────
#: the T floor of every column (registration §3.1: below 200 K a refusal; Mars's surface is 216 K)
T_FLOOR = 200.0
PHASE_ID = "slb_assemblage"


def _lm():
    """legacy_materials, imported on first use: the generator imports this module for `composition_key` alone, with
    no engine/ on its path (design §L: only legacy_materials imports engine/)."""
    from solver import legacy_materials
    return legacy_materials


class AssemblageView(mv.RecordView):
    """An assemblage record as the integrator reads it (registration §3). A RecordView subclass so the notes
    collector reads it (68 S2), answering every attribute the solver reads (§3.1's class sweep): density, dtdp and
    state through the C¹ table read and phase 1's melt window (`_lm().silicate_melt_mix`); onset curves and their
    names as legacy silicate's; the record id as `name`; `.record` with the compact sha, so solve_id binds the
    table (68 S1). RecordView's own branches (sets, γ windows, joins, the K_T stencil) are never entered."""

    def __init__(self, record, table, t_pot: float, p_stop: float = 0.0, p_floor: float = 0.0):
        self.material_id = record["id"]
        self.name = record["id"]                 # solve._pass keys its GrazeMonitor on this (68)
        self.t_pot = float(t_pot)
        self.p_stop = float(p_stop)
        self.p_floor = float(p_floor)            # legacy's, by the declared name (§3.1): _p_stop unchanged
        self.kind = "assemblage"
        self.record = freeze(copy.deepcopy(mv.thaw_plain(record)))
        self.boundaries = ()
        self.phases = []
        self.notes: list = []
        asm = self.record["assemblage"]
        self.variant = asm["melt_variant"]
        self.p_dataset = float(asm["p_dataset"])
        self.band_origin = asm["dtdp"]["band_origin"]
        self.onset_curve_names = ["고상선"]
        self._cells = {(c["p"], c["t"]): c for c in table["cells"]}
        self.ps = sorted({c["p"] for c in table["cells"]})
        self.ts = sorted({c["t"] for c in table["cells"]})
        self.lnps = [math.log(p) for p in self.ps]
        self.columns = {c["p"]: c for c in table["columns"]}

    # the table read ──────────────────────────────────────────────────────────────────────────────────────────
    def _refuse(self, p, t, rid, why):
        return st.Stop("refused", mv.RecordRefusal(self.material_id, p, t, rid, why))

    def _cell(self, ia, kb):
        return self._cells.get((self.ps[ia], self.ts[kb]))

    def _solid(self, p, t):
        """(ρ_s, dT/dP_s, c_P,s, the corner cells) from the C¹ read at (P, T), or a Stop (§3.1–§3.2)."""
        if t < T_FLOOR:
            return self._refuse(p, t, "input.material_out_of_data",
                                f"below the table's {T_FLOOR:g} K floor (registration §3.1)")
        if p > self.p_dataset:
            return self._refuse(p, t, "input.material_out_of_data",
                                f"above the SLB dataset top {self.p_dataset / 1e9:g} GPa (declaration §4); the "
                                "taper to the hand-over is not built yet (registration §3.4, note 2)")
        if t > self.ts[-1]:
            return self._refuse(p, t, "input.material_above_solid_window",
                                f"above the table's last T node {self.ts[-1]:g} K (grid_end)")
        pr = max(p, self.ps[0])                  # below 1 bar: read at the floor node (§3.1's floor band)
        x = math.log(pr)
        ia = min(max(next(i for i in range(len(self.ps)) if i + 1 == len(self.ps) or self.ps[i + 1] >= pr), 0),
                 len(self.ps) - 2)
        ib = min(max(int((t - self.ts[0]) // (self.ts[1] - self.ts[0])), 0), len(self.ts) - 2)
        while self.ts[ib] > t:
            ib -= 1
        while self.ts[ib + 1] < t:
            ib += 1
        cut = (lambda ka: self.ps[ka] <= self.p_dataset)
        out = {}
        for f in ("rho", "dtdp_eq", "c_p"):
            def val(ka, kb, f=f):
                c = self._cell(ka, kb)
                return None if c is None else c.get(f)
            try:
                out[f] = cubic2(x, t, self.lnps, self.ts, val, ia, ib, cut)
            except CellMissing as e:
                ka, kb = e.args[0]
                c = self._cell(ka, kb)
                if c is None:
                    col = self.columns[self.ps[ka]]
                    return self._refuse(p, t, "input.material_above_solid_window",
                                        f"above the solid window of the {self.ps[ka]:g} Pa column (top "
                                        f"{col['t_window_top']:g} K, cause {col['window'].get('cause')}: "
                                        f"{ {k: v for k, v in col['window'].items() if k != 'cause'} })")
                return self._refuse(p, t, "input.material_out_of_data",
                                    f"no equilibrium isentrope at node ({c['p']:g} Pa, {c['t']:g} K): its "
                                    "re-solves did not converge (registration note 3 §2 condition 4)")
        corners = [self._cell(a, b) for a in (ia, ia + 1) for b in (ib, ib + 1)]
        return out["rho"], out["dtdp_eq"], out["c_p"], [c for c in corners if c is not None]

    def _cell_notes(self, cells, p, t):
        for c in cells:
            if c["kind"] == "frozen":
                self.notes.append(mv.DeclaredNote(self.material_id, PHASE_ID,
                                                  f"frozen assemblage below its freeze temperature "
                                                  f"(class: {c.get('freeze_class')}); one fixed state re-evaluated"))
            elif c["kind"] == "above_solidus":
                self.notes.append(mv.DeclaredNote(self.material_id, PHASE_ID,
                                                  "solid above the solidus cap: SLB extrapolated in T (metastable "
                                                  "solid); melt mixed by the phase-1 rule (C120)"))
        bands = [c["dtdp_eq_band"] for c in cells if c.get("dtdp_eq_band") is not None]
        if bands:
            self.notes.append(mv.BandNote(self.material_id, "dT/dP model consistency", "relative", None, None,
                                          "equilibrium isentrope (route A)", self.band_origin, max(bands),
                                          self.band_origin))
        if p < self.ps[0]:
            k_t = self._floor_k_t(t)
            if k_t:
                self.notes.append(mv.BandNote(self.material_id, "p_min floor", "relative",
                                              (self.ps[0] - max(p, 0.0)) / k_t, None,
                                              "extrapolated in P below the grid floor",
                                              self.record["assemblage"]["floor_band"]["origin"]))

    def _floor_k_t(self, t):
        """K_T at the floor node on the read's T, ρ·∂P/∂ρ over the first two P nodes (r2 N2), at the nearest node T."""
        kb = min(range(len(self.ts)), key=lambda k: abs(self.ts[k] - t))
        a, b = self._cell(0, kb), self._cell(1, kb)
        if a is None or b is None or not b["rho"] > a["rho"]:
            return None
        return a["rho"] * (self.ps[1] - self.ps[0]) / (b["rho"] - a["rho"])

    # the interface the solver reads ─────────────────────────────────────────────────────────────────────────
    def state(self, p: float, t: float, guess_rho=None):
        self.notes.clear()
        pe = max(p, self.p_stop) if p > 0.0 else max(1.0e5, self.p_stop)
        phi = _lm().silicate_melt_phi(pe, t, self.variant)
        try:
            if phi >= 1.0:                       # the liquid alone: no solid cell is read (note 3 §1)
                rho, g, _ = _lm().silicate_melt_mix(pe, t, self.variant, None, None, None)
                return (rho, g, tuple(self.notes))
            got = self._solid(pe, t)
            if isinstance(got, st.Stop):
                return got
            rho_s, g_s, cp_s, cells = got
            self._cell_notes(cells, p, t)
            rho, g, _ = _lm().silicate_melt_mix(pe, t, self.variant, rho_s, g_s, cp_s)
        except _lm().eos.PhaseGap as e:             # RTpress's own refusal
            return self._refuse(pe, t, "input.material_out_of_data", f"RTpress liquid: {e}")
        return (rho, g, tuple(self.notes))

    def density(self, p: float, t: float):
        got = self.state(p, t)
        return got if isinstance(got, st.Stop) else got[0]

    def dtdp(self, p: float, t: float):
        got = self.state(p, t)
        return got if isinstance(got, st.Stop) else got[1]

    def phase_read(self, p: float, t: float):
        pe = max(p, self.p_stop) if p > 0.0 else max(1.0e5, self.p_stop)
        if _lm().silicate_melt_phi(pe, t, self.variant) >= 1.0:
            return PHASE_ID
        got = self._solid(pe, t)
        return got if isinstance(got, st.Stop) else PHASE_ID

    def porosity(self, p: float) -> float:
        return 0.0

    def seams(self) -> tuple:
        return ()

    def transitions(self) -> tuple:
        return ()                                # boundaries pending (§3.3): every label change is read across

    def source_seams(self) -> tuple:
        return ()

    def onset_curves(self, p: float, t: float) -> list:
        return _lm().silicate_solidus_onset(p, t, self.variant)



def view(record, table, t_pot, p_stop=0.0, p_floor=0.0):
    """An AssemblageView of a loaded record and its compact table (registry.tables[id])."""
    return AssemblageView(record, table, t_pot, p_stop, p_floor)
