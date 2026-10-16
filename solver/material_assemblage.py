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
import dataclasses
import hashlib
import json
import bisect
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
    if Path(path).suffix == ".gz":                  # the shipped form: gzip, pinned on the packed bytes (directing)
        import gzip
        try:
            data = gzip.decompress(data)
        except (OSError, EOFError) as e:
            raise TableStop(f"the compact table is not readable gzip: {e}", check="read") from None
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


def _fd_blind(by, ps, ts, i, k, d1, b3, tol):
    """None when an FD Maxwell failure at node (i, k) is FD's («FD blind: exact Maxwell within tol»: the model's exact
    Maxwell at the cell ≤ the gate's own tol there, and stored = model to 1e-6 at the cell and at every node of its ±1
    and ±2 stencils); else why it is not excused. POST-RESULT (registration note 5, r2's ruling (iii) on the final
    earth_dmm record, 2026-10-16): the test was «exact ≤ FD/10», which refused three cells consistent at the gate's own
    tol, inside the plg+ol+opx+cpx field along its plg ≈ 1.1–1.2 % contour (no label change in their stencils)."""
    c = by[(ps[i], ts[k])]
    e = _exact_maxwell(c)
    if e is None:
        return "no exact derivatives at the cell"
    if e > tol:
        return f"the model's exact Maxwell {e:.4g} is over the gate's tol {tol:.4g} at the cell"
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
        for f in ("dtdp_eq", "dtdp_g", "dtdp_eq_band", "envelope_gap_v", "envelope_gap_s", "c_p_eq"):
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
    curves = check_boundaries(table, by, ps)          # exported boundaries: rows on their pairs, P_b inside, single-valued
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
        if c.get("c_p_eq") is not None and not c["c_p_eq"] > 0.0:     # stability: c_P,eq > 0 (68 B1 on 9582a67b)
            raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): c_p_eq {c['c_p_eq']!r} must be > 0", check="positivity")
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
    # failure is excused («FD blind: exact Maxwell within tol», note 5) only if the model's exact Maxwell there is ≤ tol and
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
        why = _fd_blind(by, ps, ts, i, k, d1, b3, tol)
        if why is not None:
            raise TableStop(f"Maxwell at ({c['p']:g}, {c['t']:g}): residual {d1:.4g} beyond "
                            f"{b3['maxwell_k']:g}·|D_h − D_2h| + {b3['maxwell_floor']:g} = {tol:.4g}, not excused: {why}", check="FD Maxwell")
        excused.append((c["p"], c["t"], d1, _exact_maxwell(c), tol))       # per cell: FD, exact, tol (r2)
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
        elif not all(_finite(c.get(f)) for f in ("dtdp_eq_band", "dtdp_g", "envelope_gap_v", "envelope_gap_s",
                                                  "c_p_eq", "ds_dp_model")):
            raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): its band, G-based isentrope or envelope gap is missing", check="dT/dP field rule")
        elif abs(v + c["ds_dp_model"] * c["t"] / c["c_p_eq"]) > 1e-12 * max(abs(v), abs(c["dtdp_s"])):
            raise TableStop(f"cell ({c['p']:g}, {c['t']:g}): dtdp_eq {v!r} is not −ds_dp·T/c_p_eq (r2 B1 on note 3: "
                            "c_p_eq on dtdp_eq's basis)", check="c_p_eq recompute")
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
            "frozen_alpha_max": frozen_max, "cross_state_inversions": cross, "dtdp_eq_refused": len(refused),
            "boundary_curves": None if curves is None else len(curves)}


#: the fields a planted single-field bump is tried on, per cell kind (r2 condition 3: coverage per field)
BUMP_FIELDS = MODEL_FIELDS + ("dtdp_eq", "dtdp_g", "dtdp_eq_band", "c_p_eq")


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
            if f in ("dtdp_g", "dtdp_eq_band", "c_p_eq") and k == "frozen":
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


# ── exported boundaries (registration §3.2–§3.3; scope note b0057863, r2's and 68's rulings) ────────────────────────
#: §3.3's declared note on an answer that lands a swap seam (frozen text), and the scope note's declared notes
SWAP_NOTE = ("phase-set change landed as a sharp step, T continuous: coexistence segment not built (D-P3; owner Q-P3 "
             "(a) pending its registration)")
MULTI_NOTE = ("two or more exported boundaries inside one grid cell: read linear in ln P between the outermost curves' "
              "one-sided values (scope note Q1, r2)")
#: the declared note of a read whose cell holds a node-resolved row, read across (frozen §3.3 «never forced into a
#: step»; (A″), owner f43dac2a)
NODE_NOTE = ("node-resolved phase change read across: C¹ over its grid cell, never forced into a step (registration "
             "§3.3; read rule (A″), owner f43dac2a)")


def _labels(label) -> frozenset:
    return frozenset(label.split("+"))


#: (A″) S1 (r2 on 68 B2): a corner row reads a run past its end node only within this many P columns
CORNER_REACH = 4
#: (R1) §4 (68 (a)): a cut curve's P_b is extended this many T rows past each end, for sides and events only
EXT_ROWS = 2
#: the refusals of an (R1) read, by class (68: each located at its declared place)
NO_READ_WHY = MappingProxyType({"cap": "no read-side node within 4 P columns in row {t:g} K across the exported boundary",
                                "run": "no read-side node in row {t:g} K across the exported boundary"})


class _NoRead(Exception):
    """(R1): a corner row with no usable value — kind «cap» or «run», and the row."""


def row_across(r) -> bool:
    """(A″) (r2's per-edge criterion, owner f43dac2a): a row is read across, not cut, iff it is node-resolved, or it is
    an edge class (edge_in, edge_out, swap_two_edges) whose every edge is converged with both sides solved and within
    the pass's tolerance: delta_rho present and the pass's own over_tolerance flag False. A swap is always cut; an edge
    over tolerance, with delta_rho None (a side unsolved at P_b) or not converged cuts its row. The engine reads the
    pass's flag, never re-derives it from the value."""
    if r.get("node_resolved"):
        return True
    if r["class"] == "swap":
        return False
    es = r.get("edges") or ()
    return bool(es) and all(e.get("converged") and e.get("delta_rho") is not None and e.get("over_tolerance") is False
                            for e in es)


class _Curve:
    """One exported boundary curve: a run of rows adjacent in T of one group (scope note §3 (a)). `kind` is «swap» (a
    step), «edge» (a converged edge of an edge class: no step, the c′ correction) or «node» (a node-resolved row, read
    as an edge). P_b(T) is piecewise-linear in T between its rows and absent outside them."""

    def __init__(self, cid, kind, phase, rows):
        self.id, self.kind, self.phase = cid, kind, phase
        self.rows = sorted(rows, key=lambda r: r["t"])            # dicts: t, p_b, left, right (label sets), band
        self.t0, self.t1 = self.rows[0]["t"], self.rows[-1]["t"]
        self.p_range = (min(r["p_b"] for r in self.rows), max(r["p_b"] for r in self.rows))
        self._ts = [r["t"] for r in self.rows]                      # the rows' T, for p_b's bisection

    def p_b(self, t):
        if t < self.t0 or t > self.t1:
            return None
        rs = self.rows
        if len(rs) == 1:
            return rs[0]["p_b"]
        i = bisect.bisect_left(self._ts, t, 1) - 1      # the first pair (i, i+1) with T_i <= t <= T_i+1, as a scan finds it
        a, b = rs[i], rs[i + 1]
        w = (t - a["t"]) / (b["t"] - a["t"])
        return a["p_b"] + w * (b["p_b"] - a["p_b"])

    def nearest(self, t):
        return min(self.rows, key=lambda r: abs(r["t"] - t))

    def p_b_ext(self, t, reach):
        """P_b(t), extended past each end by `reach` in T for side decisions and events only ((R1), 68 (a)): ln P_b
        linear in T from the two end rows, constant for a one-row curve; None farther out. Not a located boundary: §3 (d)'s
        [p_lo, p_hi] check does not apply to the extension."""
        pb = self.p_b(t)
        if pb is not None:
            return pb
        rs = self.rows
        if t > self.t1:
            if t - self.t1 > reach:
                return None
            e, o = rs[-1], (rs[-2] if len(rs) > 1 else None)
        else:
            if self.t0 - t > reach:
                return None
            e, o = rs[0], (rs[1] if len(rs) > 1 else None)
        if o is None or o["p_b"] == e["p_b"]:
            return e["p_b"]
        # ln P linear past the end, from the end row's exact value: never reaches 0 (linear in P did, on default_bse's
        # steep cpx edge at 2250 K, and a clamp there flipped the read's side off any event), and a constant curve
        # extends to its own value bit for bit (an exp-log round trip left a 2e-8 Pa sliver that named no region)
        return e["p_b"] * math.exp((t - e["t"]) * (math.log(e["p_b"]) - math.log(o["p_b"])) / (e["t"] - o["t"]))

    def side_of(self, p, t):
        """The side of (p, t): −1 left, +1 right, by P_b at t, or at the nearest row's T past the curve's ends."""
        pb = self.p_b(t)
        if pb is None:
            pb = self.nearest(t)["p_b"]
        return -1 if p < pb else 1


def curve_groups(boundaries):
    """{group key: [row dicts]} from an exported block's rows (scope note §2's read rule): a converged swap → its row
    p_b; a converged edge class → one group per edge phase at edges[i].p_b; a node-resolved row → its row p_b."""
    groups = {}
    for r in boundaries.get("rows", ()):
        left, right = _labels(r["left"]), _labels(r["right"])
        base = {"t": r["t"], "p_lo": r["p_lo"], "p_hi": r["p_hi"], "left": left, "right": right,
                "left_label": r["left"], "right_label": r["right"], "band": r.get("band"), "across": row_across(r)}
        if r.get("node_resolved"):
            groups.setdefault(("node", left, right, None), []).append({**base, "p_b": r["p_b"]})
        elif r["class"] == "swap":
            groups.setdefault(("swap", left, right, None), []).append({**base, "p_b": r["p_b"]})
        else:
            for e in r["edges"]:
                groups.setdefault(("edge", left, right, e["phase"]), []).append({**base, "p_b": e["p_b"]})
    return groups


def build_curves(boundaries, ts):
    """The curves of an exported block. A group (§3 (a)'s key) can hold two branches at one T: a phase that goes out,
    comes back and goes out again (real data: opx edge_out near 4 and 12 GPa at 2050–2500 K, ea on 76c0016f). So each
    group is chained in T by rank: at each T row its rows sorted by P_b; a branch continues to the next T row (adjacent
    on the grid) only when both rows hold the same number of rows, the k-th lowest to the k-th lowest; otherwise every
    branch ends there and new ones start (the ends are counted with Q3/M2). Each curve is then single-valued in T.
    Two rows of one group on the same pair at one T are a data error: TableStop (68 M6)."""
    idx = {t: k for k, t in enumerate(ts)}
    out = []
    for key, rows in sorted(curve_groups(boundaries).items(),     # a key of sorted names, never a frozenset's repr
                            key=lambda kv: (kv[0][0], sorted(kv[0][1]), sorted(kv[0][2]), kv[0][3] or "")):
        by_t = {}
        for r in rows:
            if any(o["p_lo"] == r["p_lo"] for o in by_t.get(r["t"], ())):
                raise TableStop(f"exported boundary group {key[0]} {sorted(key[1])}→{sorted(key[2])}"
                                f"{'' if key[3] is None else ' (' + key[3] + ')'} has two rows on one pair at "
                                f"{r['t']:g} K: P_b(T) is not single-valued", check="boundaries")
            by_t.setdefault(r["t"], []).append(r)
        open_, prev_t = [], None
        for t in sorted(by_t):
            now = sorted(by_t[t], key=lambda r: r["p_b"])
            if open_ and prev_t is not None and idx[t] == idx[prev_t] + 1 and len(now) == len(open_):
                for run, r in zip(open_, now):
                    run.append(r)
            else:
                out += [_Curve(len(out) + i, key[0], key[3], run) for i, run in enumerate(open_)]
                open_ = [[r] for r in now]
            prev_t = t
        out += [_Curve(len(out) + i, key[0], key[3], run) for i, run in enumerate(open_)]
    for i, c in enumerate(out):
        c.id = i
    return out


def _cut_runs(curves, across=False):
    """Each curve's maximal runs of consecutive cut rows (row["across"] False; with `across`, of rows read across), as
    curves of their own; never re-chained, so no two rows are linked that the full set does not link (68 B1:
    re-chaining the cut subset by rank joined opx edge_out at 4.28 GPa, 2500 K to 11.93 GPa, 2550 K on earth_dmm)."""
    out, run = [], []
    for c in curves:
        for r in c.rows + [None]:
            if r is not None and r["across"] == across:
                run.append(r)
                continue
            if run:
                out.append(_Curve(len(out), c.kind, c.phase, run))
                run = []
    return out


def check_boundaries(table, by, ps):
    """The load checks of an exported block (scope note §3 (d)): every row is an adjacent non-frozen column pair of
    the table with exactly its labels (the label/geometry agreement on the row's own pair, 68 M2), every P_b lies
    strictly inside its pair's P interval, and each curve group is single-valued in T (via build_curves). ρ rising
    with P on each side is the existing one-state check (r2 H6): a pair across a boundary is never one state."""
    b = table.get("boundaries") or {}
    if b.get("status") != "exported":
        return None
    nxt = {a: c for a, c in zip(ps, ps[1:])}
    for r in b.get("rows", ()):
        where = f"exported boundary row ({r.get('t')!r} K, {r.get('p_lo')!r}–{r.get('p_hi')!r} Pa)"
        lo, hi = by.get((r["p_lo"], r["t"])), by.get((r["p_hi"], r["t"]))
        if nxt.get(r["p_lo"]) != r["p_hi"] or lo is None or hi is None:
            raise TableStop(f"{where}: not a pair of adjacent columns of the table at that T", check="boundaries")
        if lo["assemblage"] != r["left"] or hi["assemblage"] != r["right"]:
            raise TableStop(f"{where}: labels {r['left']!r}/{r['right']!r} are not the cells' "
                            f"{lo['assemblage']!r}/{hi['assemblage']!r}", check="boundaries")
        if lo["kind"] == "frozen" or hi["kind"] == "frozen":
            raise TableStop(f"{where}: a frozen cell is not a boundary side (r2 H6)", check="boundaries")
        pbs = [r["p_b"]] if r.get("node_resolved") or r["class"] == "swap" else [e["p_b"] for e in r["edges"]]
        for pb in pbs:
            if not (_finite(pb) and r["p_lo"] < pb < r["p_hi"]):
                raise TableStop(f"{where}: P_b {pb!r} is not strictly inside its pair", check="boundaries")
    ts = sorted({c["t"] for c in by.values()})
    return build_curves(b, ts)


class _Part(list):
    """A row's partition [(P_b, curve)] sorted by P_b, with its P_b list, its curves, and _region's memo (by the
    curves' sides), so that resetting a view's _parts resets all of them."""
    __slots__ = ("pbs", "cs", "regions")

    def __init__(self, items):
        super().__init__(items)
        self.pbs = [pb for pb, _ in self]
        self.cs = [c for _, c in self]
        self.regions = {}


class _Run(tuple):
    """A run (xs, ys, js, region) of one row and field, with _pchip_1d's extrapolation slope and its segments' PCHIP
    coefficients found once: run.value(x) is _pchip_1d(x, xs, ys) bit for bit."""

    def __new__(cls, xs, ys, js, r):
        self = super().__new__(cls, (xs, ys, js, r))
        n = len(xs)
        if n > 1:
            secs = [(ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]) for i in range(n - 1)]
            self.m = 0.0 if (min(secs) < 0.0 < max(secs)) else min(secs, key=abs)
        self.coeffs = [None] * max(n - 1, 0)
        return self

    def value(self, x):
        xs, ys = self[0], self[1]
        n = len(xs)
        if n == 1:
            return ys[0]
        if xs[0] <= x <= xs[-1]:
            i = min(max(bisect.bisect_left(xs, x) - 1, 0), n - 2)
            u = (x - xs[i]) / (xs[i + 1] - xs[i])           # _cubic1's node returns, then its Hermite segment
            if u == 0.0:
                return ys[i]
            if u == 1.0:
                return ys[i + 1]
            c = self.coeffs[i]
            if c is None:
                c = self.coeffs[i] = _coeffs(xs, ys, i)
            return _hermite(x, c)
        return (ys[-1] + self.m * (x - xs[-1])) if x > xs[-1] else (ys[0] + self.m * (x - xs[0]))


def _pchip_1d(x, xs, ys):
    """A run's value at x (sorted xs): PCHIP inside; past the ends, linear from the end node with the gentlest of the
    run's secants (0 where the secants change sign), so an extrapolation never steepens a run's trend and never turns
    it (directing 10-17: a run whose first segment is a steep transition, bse row 2100 K at 22.49 → 23.62 GPa, carried
    its slope a column back and inverted ρ by 1.2 % with the edge correction; the PCHIP end slope had done so)."""
    n = len(xs)
    if n == 1:
        return ys[0]
    if xs[0] <= x <= xs[-1]:
        i = min(max(bisect.bisect_left(xs, x) - 1, 0), n - 2)      # the first k with xs[k+1] >= x
        return _cubic1(x, xs, ys, i)
    secs = [(ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]) for i in range(n - 1)]
    m = 0.0 if (min(secs) < 0.0 < max(secs)) else min(secs, key=abs)
    return (ys[-1] + m * (x - xs[-1])) if x > xs[-1] else (ys[0] + m * (x - xs[0]))


# ── the view (registration §3; post-freeze note 3 §1, §4) ───────────────────────────────────────────────────────────
#: the T floor of every column (registration §3.1: below 200 K a refusal; Mars's surface is 216 K)
T_FLOOR = 200.0
PHASE_ID = "slb_assemblage"
#: the declared note of a read with φ ≥ 1 (no solid cell read, so no dT/dP band note): the round's B6 exemption keys on it
LIQUID_ALONE_NOTE = ("liquid alone (φ ≥ 1): RTpress liquid, as phase 1; no solid cell read (registration post-freeze "
                     "note 3 §1)")


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

    def __init__(self, record, table, t_pot: float, p_stop: float = 0.0, p_floor: float = 0.0, handover=None):
        self.material_id = record["id"]
        self.name = record["id"]                 # solve._pass keys its GrazeMonitor on this (68)
        #: the hand-over above p_dataset (a HandOver, note 7 §3), or None: then a read above p_dataset refuses (§3.4)
        self.handover = handover
        self._rise_rows = {}                     # note 7 §5: T row index → None (ρ rises across the zone) or the why
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
        b = table.get("boundaries") or {}
        exported = b.get("status") == "exported"
        #: every exported curve: the seam events (transitions) and the disclosures
        self._curves = build_curves(b, self.ts) if exported else []
        #: the curves that cut the stencil: each full curve split into its maximal runs of rows (A″) does not read
        #: across (row_across), so a cut curve's links are always links of the full set (68 B1 on 2453b935)
        self._cut = _cut_runs(self._curves)
        #: cut runs that coincide with another at every row (P_b equal to 1e-9; e.g. dmm's cpx and wa edges at
        #: 16.280025 GPa, 1450 K) are a step, not two edges: read as a swap, no (c′) correction, with SWAP_NOTE (68 N2,
        #: r2's Q1 degenerate limit); both land as events at one P, and the first landed leaves the other on its new side
        self.coincident = 0
        by_ts = {}
        for c in self._cut:
            by_ts.setdefault(tuple(r["t"] for r in c.rows), []).append(c)
        for group in by_ts.values():
            for a in group:
                if any(b is not a and all(abs(ra["p_b"] - rb["p_b"]) <= 1e-9 * ra["p_b"] for ra, rb in zip(a.rows, b.rows))
                       for b in group):
                    if a.kind == "edge":
                        self.coincident += 1
                    a.kind = "swap"
        #: the event curves (transitions): the cut runs, landed at their extended P_b ((R1) §4), then the runs read
        #: across, at their own P_b; indices are the ids the event names carry
        self._events = self._cut + _cut_runs(self._curves, across=True)
        #: (R1) §4: a cut curve's side reach past its ends, two T rows (the stencil's reach)
        self._reach = EXT_ROWS * (self.ts[1] - self.ts[0]) if len(self.ts) > 1 else 0.0
        self._parts, self._runcache = {}, {}
        self._read_memo = {}
        self._wn_of = None                               # _width's node widths and their max, for the lnps they came from
        #: the column cut of a read: p_dataset, lifted to the taper's end for the zone's SLB-extrapolated read (note 7 §2)
        self._top = self.p_dataset
        #: the read counts of this view ((R1), 68 S1): reads, corner rows read in an empty region, outer rows dropped
        #: (reads, most in one read), refusals by class, edge corrections applied, side fallbacks (0 by
        #: construction: the extension covers the stencil), and corner rows δ read from the nearest region with a run
        #: (_row_reach)
        self.cut_counts = {"reads": 0, "empty_region_reads": 0, "row_drop_reads": 0, "row_drop_max": 0,
                           "cap_refusals": 0, "no_run_refusals": 0, "by_count_reads": 0, "corrections": 0,
                           "side_fallbacks": 0, "reach_rows": 0}
        self._marks = {"dropped": set(), "empty": False, "by_count": False}

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
        if p > self.p_dataset and self.handover is None:
            return self._refuse(p, t, "input.material_out_of_data",
                                f"above the SLB dataset top {self.p_dataset / 1e9:g} GPa (declaration §4); the "
                                "taper to the hand-over is not built yet (registration §3.4, note 2)")
        if t > self.ts[-1]:
            return self._refuse(p, t, "input.material_above_solid_window",
                                f"above the table's last T node {self.ts[-1]:g} K (grid_end)")
        if p > self.p_dataset:
            return self._taper(p, t)
        return self._table_read(p, t)

    def _lifted(self, p, t):
        """The SLB-extrapolated read in the taper zone: the same read with the column cut lifted to the zone's end
        (note 7 §2)."""
        top = self._top
        self._top = 1.5 * self.p_dataset
        try:
            return self._table_read(p, t)
        finally:
            self._top = top

    def _blend(self, p, t):
        """(ρ, dT/dP, c_P, cells, w, ρ_SLB, ρ_HO, band_HO, shift) of the zone at (P, T), or a Stop (note 7 §1); shift is
        the 136 GPa match's relative size per field, (1 − w)·|X_cut − X_lift|/|X| (r2 D3 on delta 1)."""
        p_end = 1.5 * self.p_dataset
        w = _smoothstep((p - self.p_dataset) / (p_end - self.p_dataset))
        rho_h = self.handover.rho(p)
        th, why = self.handover.thermal(p, t)
        if th is None:
            return self._refuse(p, t, "input.material_out_of_data", f"{self.handover.material_id}: {why}")
        dtdp_h, cp_h, band_h = th
        if w >= 1.0:
            return rho_h, dtdp_h, cp_h, [], w, None, rho_h, band_h, (0.0, 0.0, 0.0)
        got = self._lifted(p, t)
        if isinstance(got, st.Stop):
            return got
        rho_s, dtdp_s, cp_s, cells = got
        # the 136 GPa match (note 7 delta): the lifted read and the read below differ at the dataset top off the T rows
        # (an outer row's end slope vs its run across, an edge's δ), so the lifted read is shifted by their difference
        # at 136 GPa on this T, faded with the zone's own weight: the answer is C⁰ at 136 GPa in every field
        cut0, lift0 = self._table_read(self.p_dataset, t), self._lifted(self.p_dataset, t)
        if not (isinstance(cut0, tuple) and isinstance(lift0, tuple)):
            # r2 D2 on delta 1: unshifted reads where one side refuses stepped the zone ×3 in T (bse 3600–3609 K); the
            # zone cannot be matched to a read that does not answer at the dataset top on this T, so it refuses there
            # by name (a refusal boundary in T, as the read below has at the same T)
            why = (cut0 if isinstance(cut0, st.Stop) else lift0).record.why
            return self._refuse(p, t, "input.material_out_of_data",
                                f"the taper zone cannot be matched at {self.p_dataset / 1e9:g} GPa on T {t:g} K: the "
                                f"read there refuses ({why}) (note 7 delta 1)")
        d = [(1.0 - w) * (cut0[i] - lift0[i]) for i in range(3)]
        rho_s, dtdp_s, cp_s = rho_s + d[0], dtdp_s + d[1], cp_s + d[2]
        shift = tuple(abs(d[i]) / abs(cut0[i]) if cut0[i] else 0.0 for i in range(3))
        rho = 1.0 / ((1.0 - w) / rho_s + w / rho_h)                 # A4's V-blend for ρ
        return (rho, (1.0 - w) * dtdp_s + w * dtdp_h, (1.0 - w) * cp_s + w * cp_h, cells, w, rho_s, rho_h,
                band_h, shift)                                       # dT/dP and c_P blended directly (note 7 §1)

    def _rise_ok(self, kb):
        """Note 7 §5: None if the zone's ρ rises with P along T row kb, else the refusal text; found once per row, at
        the zone's own P nodes and midpoints."""
        if kb not in self._rise_rows:
            t = self.ts[kb]
            nodes = [q for q in self.ps if self.p_dataset <= q <= 1.5 * self.p_dataset]
            xs = sorted(set(nodes) | {math.sqrt(a * b) for a, b in zip(nodes, nodes[1:])})
            why, last = None, None
            for q in xs[1:]:
                got = self._blend(q, t)
                if isinstance(got, st.Stop):
                    continue                                 # a refusal there is the read's own, met at the read
                if last is not None and not got[0] > last:
                    why = (f"ρ does not rise with P across the taper zone (§3.4's load check) at T row {t:g} K "
                           f"(note 7 §5)")
                    break
                last = got[0]
            self._rise_rows[kb] = why
        return self._rise_rows[kb]

    def _taper(self, p, t):
        """The read above p_dataset (§3.4, note 7): the zone 136–204 GPa blends the SLB-extrapolated read into the
        hand-over; above it, the hand-over alone. One band per field (note 7 §4); a T row where the zone's ρ does not
        rise refuses by name (§5)."""
        ib = min(max(bisect.bisect_right(self.ts, t) - 1, 0), len(self.ts) - 2)
        if p < 1.5 * self.p_dataset:
            for kb in (ib, ib + 1):
                why = self._rise_ok(kb)
                if why is not None:
                    return self._refuse(p, t, "input.material_out_of_data", why)
        got = self._blend(p, t)
        if isinstance(got, st.Stop):
            return got
        rho, dtdp, cp, cells, w, rho_s, rho_h, band_h, shift = got
        band_cell = max((c["dtdp_eq_band"] for c in cells if c.get("dtdp_eq_band") is not None), default=0.0)
        if rho_s is not None:
            rho_band = abs(rho_s - rho_h) / rho_s + shift[0]
            rho_origin = "the local |ρ_SLB − ρ_HO|/ρ_SLB (§3.4) + the 136 GPa match's (1 − w)·|Δρ|/ρ (delta 1)"
        else:                                    # above the zone: the composition's mismatch to PREM at 204 GPa (§6)
            rho_band, rho_origin = None, "beyond the zone: the composition's ρ mismatch to PREM at 204 GPa (note 7 §6)"
            r204 = self._lifted(1.5 * self.p_dataset, t)
            if not isinstance(r204, st.Stop):
                rho_band = abs(r204[0] - self.handover.rho(1.5 * self.p_dataset)) / self.handover.rho(1.5 * self.p_dataset)
        dt_band = max((1.0 - w) * band_cell, w * (band_h or 0.0)) + shift[1]
        self.notes.append(mv.BandNote(self.material_id, "taper to the hand-over", "relative", rho_band, None,
                                      TAPER_GRADE if w < 1.0 else self.handover.grade, rho_origin, dt_band,
                                      "max((1 − w)·the cell's dT/dP band, w·band_HO) (note 7 §4) + the 136 GPa "
                                      "match's (1 − w)·|Δ(dT/dP)|/(dT/dP) (delta 1)"))
        return rho, dtdp, cp, cells

    def _table_read(self, p, t):
        """The table's own C¹ read at (P, T) below the current column cut (self._top)."""
        pr = max(p, self.ps[0])                  # below 1 bar: read at the floor node (§3.1's floor band)
        x = math.log(pr)
        ia = min(max(bisect.bisect_left(self.ps, pr, 1) - 1, 0), len(self.ps) - 2)   # the first i with P_i+1 >= pr
        ib = min(max(int((t - self.ts[0]) // (self.ts[1] - self.ts[0])), 0), len(self.ts) - 2)
        while self.ts[ib] > t:
            ib -= 1
        while self.ts[ib + 1] < t:
            ib += 1
        if self._curves:                         # an exported-boundary record: every read through the row regions (R1)
            return self._read(p, t, pr, x, ia, ib)
        cut = (lambda ka: self.ps[ka] <= self._top)
        out = {}
        for f in ("rho", "dtdp_eq", "c_p"):
            def val(ka, kb, f=f):
                c = self._cell(ka, kb)
                if c is None:
                    return None
                if f == "c_p" and c["kind"] != "frozen":
                    return c.get("c_p_eq")          # the window's c_P,s on dtdp_eq's basis (r2 B1 on note 3)
                return c.get(f)
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
        self._node_note(t, ia)
        corners = [self._cell(a, b) for a in (ia, ia + 1) for b in (ib, ib + 1)]
        return out["rho"], out["dtdp_eq"], out["c_p"], [c for c in corners if c is not None]

    def _node_note(self, t, ia):
        """NODE_NOTE with the curve's P_b range and its ±half-cell band range, for each node-resolved curve whose P_b(t)
        lies in the read's P cell (scope note §4 «the midpoint and band are carried into the note»). Over the curve,
        not at the read's T, so the note's text does not depend on the integrator's T nodes (68 N1, as SWAP_NOTE)."""
        lo, hi = self.ps[ia], self.ps[ia + 1]
        for c in self._curves:
            if c.kind == "node" and (pb := c.p_b(t)) is not None and lo <= pb <= hi:
                a, b = c.p_range
                bands = [r["band"] for r in c.rows]
                self.notes.append(mv.DeclaredNote(self.material_id, PHASE_ID,
                                                  f"{NODE_NOTE}; P_b {a / 1e9:.4g}–{b / 1e9:.4g} GPa, band ± "
                                                  f"{min(bands) / 1e9:.3g}–{max(bands) / 1e9:.3g} GPa"))

    # exported boundaries (scope note §3 (b)–(c″)) ─────────────────────────────────────────────────────────────
    def _val(self, f, j, k):
        c = self._cell(j, k)
        if c is None:
            return None
        if f == "c_p" and c["kind"] != "frozen":
            return c.get("c_p_eq")
        return c.get(f)

    # (R1): fixed per-row region functions (owner e4cd7f01; 68 on the design note, H1–H3, (a)–(c)) ─────────────────
    def _partition(self, k):
        """Row k's cut curves defined at t_k, sorted by P_b(t_k): [(P_b, curve)]. Fixed per row."""
        got = self._parts.get(k)
        if got is None:
            tk = self.ts[k]
            got = _Part(sorted(((c.p_b(tk), c) for c in self._cut if c.p_b(tk) is not None), key=lambda e: e[0]))
            self._parts[k] = got
        return got

    def _region_of(self, j, k):
        return bisect.bisect_left(self._partition(k).pbs, self.ps[j])

    def _runs(self, f, k):
        """Row k's runs for field f: {region: [(xs, ys, js)]}, each a maximal run of consecutive present nodes at or
        below p_dataset inside one region (a missing node, the window's end, splits a region). Fixed per row."""
        key = (f, k, self._top)
        got = self._runcache.get(key)
        if got is None:
            pbs = self._partition(k).pbs
            got, cur = {}, None
            for j, p in enumerate(self.ps):
                if p > self._top:
                    break
                v = self._val(f, j, k)
                r = bisect.bisect_left(pbs, p)
                if v is None:
                    cur = None
                    continue
                if cur is None or cur[3] != r:
                    cur = ([], [], [], r)
                    got.setdefault(r, []).append(cur)
                cur[0].append(self.lnps[j])
                cur[1].append(v)
                cur[2].append(j)
            got = {r: [_Run(*q) for q in qs] for r, qs in got.items()}
            self._runcache[key] = got
        return got

    def _run_value(self, f, k, r, x, corner):
        """Region r of row k at x from its runs: PCHIP inside a run, the end slope past the region's outer runs, and
        linear in ln P between two runs across a gap inside the region (68 H1). A corner row reads past a run's end
        node only within CORNER_REACH columns, else _NoRead("cap") (r2 on 68 B2); an outer row has no cap (68 H2).
        None when the region has no run."""
        runs = self._runs(f, k).get(r)
        if not runs:
            return None
        n = len(self.ps)
        if len(runs) == 1:                               # one run: no gap, and every branch below picks it
            run = runs[0]
        else:
            for a, b in zip(runs, runs[1:]):
                if a[0][-1] < x < b[0][0]:                # a gap inside the region: linear between the two runs' ends
                    va, vb = a[1][-1], b[1][0]
                    return va + (vb - va) * (x - a[0][-1]) / (b[0][0] - a[0][-1])
            run = runs[0] if x < runs[0][0][0] else runs[-1] if x > runs[-1][0][-1] else next(
                q for q in runs if q[0][0] <= x <= q[0][-1])
        if corner and (x < self.lnps[max(run[2][0] - CORNER_REACH, 0)]
                       or x > self.lnps[min(run[2][-1] + CORNER_REACH, n - 1)]):
            raise _NoRead("cap", k)
        return run.value(x)

    def _row_value(self, f, k, r, x, corner):
        """Row k's value at x in region r: its runs (_run_value), or, for a region with no run for this field, linear in
        ln P between the nearest regions with a run on either side, each at its bounding curve toward r ((c″) per
        region; a block of empty regions, or a field missing at a node, reads through). None if a side has no run.
        Memoised per read on its arguments and the column cut (δ's two sides share the rows the edge is not in), with
        the empty-region mark it sets."""
        mk = ("row", f, k, r, x, corner, self._top)
        got = self._read_memo.get(mk)
        if got is not None:
            if got[1]:
                self._marks["empty"] = True
            return got[0]
        e0 = self._marks["empty"]
        self._marks["empty"] = False
        try:
            v = self._row_value_raw(f, k, r, x, corner)
            self._read_memo[mk] = (v, self._marks["empty"])
            return v
        finally:
            self._marks["empty"] = e0 or self._marks["empty"]

    def _row_value_raw(self, f, k, r, x, corner):
        runs = self._runs(f, k)
        part = self._partition(k)
        if runs.get(r):
            return self._run_value(f, k, r, x, corner)
        lo = next((q for q in range(r - 1, -1, -1) if runs.get(q)), None)      # the nearest regions with a run
        hi = next((q for q in range(r + 1, len(part) + 1) if runs.get(q)), None)
        if lo is None or hi is None:
            return None
        xl, xr = math.log(part[lo][0]), math.log(part[hi - 1][0])          # their bounding curves toward r
        vl = self._run_value(f, k, lo, xl, corner)
        vr = self._run_value(f, k, hi, xr, corner)
        if corner:
            self._marks["empty"] = True
        if xr <= xl:                                     # two curves at one P_b in this row: a zero-width region
            return 0.5 * (vl + vr)
        # 68 B1 on 652004f9: the read's region is named by its sides at its own T, so in a row whose curves sit elsewhere
        # x can lie outside [xl, xr]; the fraction is clamped, never extrapolated: the neighbours' difference is not
        # carried past their bounding curves (it gave c_P −0.38 at dmm 12.833 GPa, 3668.29 K). Beyond a curve the
        # region holds that curve's value, the nearest data it has, continuous in x; a refusal there would cut a
        # boundary inside valid space
        u = min(max((x - xl) / (xr - xl), 0.0), 1.0)
        return vl + (vr - vl) * u

    def _region(self, k, sides, x):
        """The region of row k named by the read's sides of row k's curves: right of the first r curves in P_b(t_k)
        order and left of the rest. When the sides name no such region (two curves crossed between t_k and the read's
        T; 68 H3), the region is still r = the count of curves the read is right of: it changes only where a side
        changes (a landed event), so the read stays continuous; counted. A curve with no side (none by construction)
        is taken by row k's own geometry, counted. Memoised per row on the sides of its curves, which alone decide r and
        the H3 mark when every curve has a side."""
        mk = (id(sides), k)                              # the read's memo holds `sides` itself, so its id is not reused
        got = self._read_memo.get(mk)
        if got is not None and got[0] is sides:
            if got[2]:
                self._marks["by_count"] = True
            return got[1]
        part = self._partition(k)
        key = tuple(map(sides.get, part.cs))
        got = part.regions.get(key)
        if got is not None:
            self._read_memo[mk] = (sides, got[0], got[1])
            if got[1]:
                self._marks["by_count"] = True
            return got[0]
        ss = []
        for pb, c in part:
            s_ = sides.get(c)
            if s_ is None:
                self.cut_counts["side_fallbacks"] += 1
                s_ = -1 if x < math.log(pb) else 1
            ss.append((pb, -s_))
        ss = [-s_ for _, s_ in sorted(ss)]               # curves at one P_b in this row: ordered by the read's side
        r = sum(1 for s_ in ss if s_ > 0)
        by_count = any(s_ < 0 for s_ in ss[:r])
        if by_count:
            self._marks["by_count"] = True                # 68 H3: curves crossed between t_k and t; by count
        if None not in key:                              # a fallback side is x's, so never memoised
            part.regions[key] = (r, by_count)
            self._read_memo[mk] = (sides, r, by_count)
        return r

    def _value(self, f, x, t, ia, ib, sides, check=True):
        """One field at (x, t) through the row regions, T last (_cubic1 as the uncut path). A corner row (ib, ib+1)
        that names no region, or has no usable run, raises _NoRead; an outer row then drops (its choice changes only
        with the sides). `check`: a read-side corner node of the read cell with no value is CellMissing (D-M2)."""
        n_t = len(self.ts)
        rows = {}
        for k in range(max(ib - 1, 0), min(ib + 2, n_t - 1) + 1):
            corner = k in (ib, ib + 1)
            r = self._region(k, sides, x)
            if corner and check:
                for j in (ia, ia + 1):
                    if self.ps[j] <= self._top and self._region_of(j, k) == r and self._val(f, j, k) is None:
                        raise CellMissing((j, k))
            v = self._row_value(f, k, r, x, corner)
            if v is None:
                if corner:
                    raise _NoRead("run", k)
                self._marks["dropped"].add(k)
                continue
            rows[k] = v
        return _cubic1(t, self.ts, _Seq(rows, n_t), ib)

    def _node_widths(self):
        """([node-centred ln-P cell width per node], their max), found once per lnps list (found again if lnps is
        replaced, as a test does)."""
        got = self._wn_of
        if got is None or got[0] is not self.lnps:
            xs, n = self.lnps, len(self.lnps)
            wn = [(xs[min(i + 1, n - 1)] - xs[max(i - 1, 0)]) / (2.0 if 0 < i < n - 1 else 1.0) for i in range(n)]
            got = self._wn_of = (xs, wn, max(wn))
        return got[1], got[2]

    def _width(self, x):
        """The (c′) window's half-width at x: node-centred ln-P cell widths, linear in ln P between nodes (68 (c))."""
        xs, n, wn = self.lnps, len(self.lnps), self._node_widths()[0]
        j = min(max(bisect.bisect_right(xs, x) - 1, 0), n - 2)
        u = min(max((x - xs[j]) / (xs[j + 1] - xs[j]), 0.0), 1.0)
        return wn[j] + u * (wn[j + 1] - wn[j])

    def _delta(self, f, c, xb, w, t, ia, ib, sides, pbs):
        """δ = L − R of edge c at x_b from the raw side reads (no correction inside, 68 (c)): every swap's side is the
        read's (its step is a landed event), every other edge's side is taken at (x_b, t) by geometry, so δ never
        depends on the read's own side of another edge. It changes in t where another cut edge's P_b crosses x_b."""
        two = self._read_memo.get(("sd", c.id, xb))       # the two sides do not depend on the field: once per read
        if two is None:
            sd = {cc: (sides[cc] if cc.kind == "swap" or q is None else (-1 if (xb, c.id) < (math.log(q), cc.id) else 1))
                  for cc, q in pbs.items()}              # at an exact tie, ordered by id: one order for both δ
            two = self._read_memo[("sd", c.id, xb)] = ({**sd, c: -1}, {**sd, c: 1})
        rl, rr = self._side_rows(f, xb, ib, two[0]), self._side_rows(f, xb, ib, two[1])
        if all(k in rl and k in rr for k in (ib, ib + 1)):
            return _cubic1(t, self.ts, _Seq(rl, len(self.ts)), ib) - _cubic1(t, self.ts, _Seq(rr, len(self.ts)), ib)
        # a corner row with no run for f at all: the read itself refuses there (its own corner row has no value), so
        # no δ is used (68 N4 on 652004f9: the row-difference form was reached only by reads that refuse)
        return 0.0

    def _row_reach(self, f, k, r):
        """A corner row's value for δ in region r where _row_value has none (r empty and no run on one side): the
        nearest region with a run, at its bounding curve toward r (constant). It depends on the row and the region
        alone, so a region shared by two edges' δ (two edges crossing at x_b) reads alike in both and their
        corrections telescope; None when the row has no run for f at all."""
        runs, part = self._runs(f, k), self._partition(k)
        lo = next((q for q in range(r - 1, -1, -1) if runs.get(q)), None)
        hi = next((q for q in range(r + 1, len(part) + 1) if runs.get(q)), None)
        if lo is None and hi is None:
            return None
        self.cut_counts["reach_rows"] += 1
        if lo is not None:
            return self._run_value(f, k, lo, math.log(part[lo][0]), False)
        return self._run_value(f, k, hi, math.log(part[hi - 1][0]), False)

    def _side_rows(self, f, x, ib, sides):
        """One side's stencil row values at x_b for δ (68 B1 on d7cc971d: a side never refuses the read): as _value's
        rows, but uncapped (x_b moves with t, so a cap would switch inside a T cell; the cap only refuses, it changes
        no value); a corner row with no value in its region reads the nearest region with a run (_row_reach), an outer
        row with none is left out, as _value drops it. {row: value}. Where both actual reads stand at x_b this is their
        value, so δ = L − R keeps the read continuous at P_b."""
        n_t = len(self.ts)
        rows = {}
        for k in range(max(ib - 1, 0), min(ib + 2, n_t - 1) + 1):
            r = self._region(k, sides, x)
            v = self._row_value(f, k, r, x, False)
            if v is None and k in (ib, ib + 1):
                v = self._row_reach(f, k, r)
            if v is None:
                continue
            rows[k] = v                     # no MULTI_NOTE from δ's side reads: the read's own regions decide the
                                            # notes (68 B2 (d) on 652004f9)
        return rows

    def _read(self, p, t, pr, x, ia, ib):
        """The read of an exported-boundary record (R1): every field P first through the row regions, T last; at each
        cut edge within w of the read, the (c′) correction ∓δ/2·(1 − |x − x_b|/w), δ = L − R from the raw side reads
        at x_b (_delta), continuous in t and changing in x only where the read crosses a swap (a landed step), so
        overlapping windows add continuously. Continuous except at P_b_ext(t) of
        cut swaps (landed events) and at refusal boundaries."""
        self.cut_counts["reads"] += 1
        self._marks = {"dropped": set(), "empty": False, "by_count": False}
        self._read_memo = {}                             # per read: δ's two side maps, and regions by side map
        n_t = len(self.ts)
        # in curve id order: a set of curves iterates by object address, which differs between processes, and the
        # corrections below are summed in this order, so a set made the answers differ in their last bits run to run
        rel = sorted({c for k in range(max(ib - 1, 0), min(ib + 2, n_t - 1) + 1) for _, c in self._partition(k)},
                     key=lambda c: c.id)
        pbs = {c: c.p_b_ext(t, self._reach) for c in rel}
        sides = {c: (None if pb is None else (-1 if pr < pb else 1)) for c, pb in pbs.items()}
        near = []                                        # the edges whose (c′) window holds x: (curve, x_b, w), per read
        for c in rel:
            if c.kind != "edge" or pbs[c] is None:
                continue
            xb = math.log(pbs[c])
            if abs(x - xb) >= self._node_widths()[1] * (1.0 + 1e-12):   # w is a convex mix of node widths: never wider (a
                continue                                          # rounding margin kept), so _width would skip it too
            w = self._width(xb)
            if abs(x - xb) < w:
                near.append((c, xb, w))
        out = {}
        try:
            for f in ("rho", "dtdp_eq", "c_p"):
                v = self._value(f, x, t, ia, ib, sides)
                for c, xb, w in near:
                    d = self._delta(f, c, xb, w, t, ia, ib, sides, pbs)
                    v += (-0.5 * d * (1.0 - (xb - x) / w)) if sides[c] < 0 else (0.5 * d * (1.0 - (x - xb) / w))
                    if f == "rho":
                        self.cut_counts["corrections"] += 1
                out[f] = v
        except _NoRead as e:
            self._close_marks()
            kind, k = e.args
            key = {"cap": "cap_refusals", "run": "no_run_refusals"}[kind]
            self.cut_counts[key] += 1
            return self._refuse(p, t, "input.material_out_of_data", NO_READ_WHY[kind].format(t=self.ts[k]))
        except CellMissing as e:
            ka, kb = e.args[0]
            c = self._cell(ka, kb)
            if c is None:
                col = self.columns[self.ps[ka]]
                return self._refuse(p, t, "input.material_above_solid_window",
                                    f"above the solid window of the {self.ps[ka]:g} Pa column (top "
                                    f"{col['t_window_top']:g} K, cause {col['window'].get('cause')})")
            return self._refuse(p, t, "input.material_out_of_data",
                                f"no equilibrium isentrope at node ({c['p']:g} Pa, {c['t']:g} K): its "
                                "re-solves did not converge (registration note 3 §2 condition 4)")
        self._close_marks()
        if self._marks["empty"]:
            self.notes.append(mv.DeclaredNote(self.material_id, PHASE_ID, MULTI_NOTE))
        lo, hi = self.ps[ia], self.ps[ia + 1]
        for c in rel:
            if c.kind == "swap" and pbs[c] is not None and lo <= pbs[c] <= hi:
                a, b = c.p_range
                self.notes.append(mv.DeclaredNote(self.material_id, PHASE_ID,
                                                  f"{SWAP_NOTE}; P {a / 1e9:.4g}–{b / 1e9:.4g} GPa"))
        self._node_note(t, ia)
        corners = []
        for kb in (ib, ib + 1):
            r = self._region(kb, sides, x)
            corners += [self._cell(ja, kb) for ja in (ia, ia + 1) if self._region_of(ja, kb) == r]
        return out["rho"], out["dtdp_eq"], out["c_p"], [c for c in corners if c is not None]

    def _close_marks(self):
        """One count per read, whatever the field and δ calls (68 N1)."""
        m = self._marks
        if m["dropped"]:
            self.cut_counts["row_drop_reads"] += 1
            self.cut_counts["row_drop_max"] = max(self.cut_counts["row_drop_max"], len(m["dropped"]))
        if m["empty"]:
            self.cut_counts["empty_region_reads"] += 1
        if m.get("by_count"):
            self.cut_counts["by_count_reads"] += 1

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
                self.notes.append(mv.DeclaredNote(self.material_id, PHASE_ID, LIQUID_ALONE_NOTE))
                return (rho, g, tuple(self.notes))
            got = self._solid(pe, t)
            if isinstance(got, st.Stop):            # the refusal names the solver's P, not the clamped read (ea F4)
                r = got.record
                return self._refuse(p, t, r.refusal, r.why if pe == p else f"{r.why} (read at {pe:g} Pa)")
            rho_s, g_s, cp_s, cells = got
            self._cell_notes(cells, p, t)
            rho, g, _ = _lm().silicate_melt_mix(pe, t, self.variant, rho_s, g_s, cp_s)
        except _lm().eos.PhaseGap as e:             # RTpress's own refusal
            return self._refuse(p, t, "input.material_out_of_data", f"RTpress liquid: {e}")
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
        """Exported curves as solid_solid seams (§3.3): the cut runs at their extended P_b ((R1) §4: a swap steps
        there, fading past its end with the partitioned rows' T weight, not monotonically), then the runs read across
        at their own P_b (no step); pending boundaries give none. Ids index self._events."""
        return tuple(((f"{c.kind}{i}:{c.rows[0]['left_label']}", f"{c.rows[0]['right_label']}"), "solid_solid",
                      {"form": "assemblage_curve", "id": i}) for i, c in enumerate(self._events))

    def boundary_pressure(self, curve, t):
        if curve.get("form") == "assemblage_curve":
            i = curve["id"]
            c = self._events[i]
            return c.p_b_ext(t, self._reach) if i < len(self._cut) else c.p_b(t)
        return super().boundary_pressure(curve, t)

    def source_seams(self) -> tuple:
        return ()

    def onset_curves(self, p: float, t: float) -> list:
        return _lm().silicate_solidus_onset(p, t, self.variant)



def _dist(items):
    """n, median, p99 and the largest item (value first) of a list of (value, …) tuples."""
    xs = sorted(items, key=lambda e: e[0])
    if not xs:
        return {"n": 0}
    return {"n": len(xs), "median": xs[len(xs) // 2][0], "p99": xs[int(0.99 * len(xs))][0], "max": list(xs[-1])}


def _across_smoothing(v, rows):
    """(A″)'s smoothing disclosures over the rows read across, at each row's T from its pair's outer nodes (columns
    ia−1 … ia+2): e_smooth = |m_L − m_R|·Δx/8, the C¹ read's largest ρ departure from the two sides' ln ρ secants
    over the cell (relative); the dT/dP bound |L − R|·ΔP/4 (K), L and R the two sides' secant extrapolations of
    dtdp_eq to P_b (the row's P_b, or its edges' mean); and the node-to-node |Δρ|/ρ across the cell. A bound, not a
    measured error. Rows whose stencil leaves the table or the dataset, or lacks a cell, are counted as skipped."""
    ps, ts = v.ps, v.ts
    es, dts, steps, skipped = {"edge": [], "node": []}, {"edge": [], "node": []}, [], 0
    for r in rows:
        ia, kb = ps.index(r["p_lo"]), ts.index(r["t"])
        cs = [v._cell(j, kb) for j in (ia - 1, ia, ia + 1, ia + 2)] if 1 <= ia and ia + 2 < len(ps) else None
        if cs is None or ps[ia + 1] > v.p_dataset or any(c is None for c in cs):
            skipped += 1
            continue
        kind = "node" if r.get("node_resolved") else "edge"
        pb = r["p_b"] if kind == "node" else sum(e["p_b"] for e in r["edges"]) / len(r["edges"])
        where = (pb / 1e9, r["t"], r["class"])
        x = [math.log(ps[j]) for j in (ia - 1, ia, ia + 1, ia + 2)]
        m_l = (math.log(cs[1]["rho"]) - math.log(cs[0]["rho"])) / (x[1] - x[0])
        m_r = (math.log(cs[3]["rho"]) - math.log(cs[2]["rho"])) / (x[3] - x[2])
        es[kind].append((abs(m_l - m_r) * (x[2] - x[1]) / 8.0, *where))
        steps.append((abs(cs[2]["rho"] / cs[1]["rho"] - 1.0), *where, kind))
        if all(c.get("dtdp_eq") is not None for c in cs):
            g_l = (cs[1]["dtdp_eq"] - cs[0]["dtdp_eq"]) / (ps[ia] - ps[ia - 1])
            g_r = (cs[3]["dtdp_eq"] - cs[2]["dtdp_eq"]) / (ps[ia + 2] - ps[ia + 1])
            lv, rv = cs[1]["dtdp_eq"] + g_l * (pb - ps[ia]), cs[2]["dtdp_eq"] - g_r * (ps[ia + 1] - pb)
            dts[kind].append((abs(lv - rv) * (ps[ia + 1] - ps[ia]) / 4.0, *where))
    return {"e_smooth": {k: {**_dist(e), "over_1e-2": [list(x) for x in e if x[0] > 1e-2]} for k, e in es.items()},
            "dtdp_bound_K": {k: _dist(e) for k, e in dts.items()},
            "node_to_node": {k: _dist([s_[:4] for s_ in steps if s_[4] == k]) for k in ("edge", "node")},
            "skipped": skipped}


def boundary_disclosures(record, table) -> dict:
    """The per-table disclosures of an exported block (scope note §3 (c′), (c″), §5; 68 M5, S1; (A″), owner f43dac2a),
    report-only:
    - read: each row's read mode («cut», «across», «node»: a node-resolved row read across) with its counts, so a
      boundary read differently along T (Earth's 660: stepped, ramped at node-resolved rows, read across) is listed;
    - across: (A″)'s smoothing over the rows read across (_across_smoothing): e_smooth, the dT/dP bound, node to node;
    - edge_delta: per cut edge curve row, |δ|/ρ = |L(P_b) − R(P_b)|/L of the one-sided ρ reads at the row's T, with the
      rows over 1e-2 listed for directing (r2 Q2);
    - over_tolerance: the pass's own over-tolerance edges, and the tolerance from the block's source when it carries it;
    - multi_curve_cells: (T row, P cell) pairs holding two or more cut curves (r2 Q1);
    - t_changes: label changes along T inside a column, split «on curve <id>» (a sloped curve's P_b crosses the column
      between the rows) from unlocated ones (68 M5), with curve ends counted (r2 M2);
    - sweep: the cut-read counts of one read at the centre of every cell (68 S1), with S1's row drops, and P0′'s past-end
      admissions across an edge-type label change (the |Δρ|/ρ each carries, _label_step) and swap-type rejections."""
    v = view(record, table, 1600.0)
    if not v._curves:
        return {"status": (table.get("boundaries") or {}).get("status")}
    ts, ps = v.ts, v.ps
    rows = table["boundaries"]["rows"]
    modes = [{"t": r["t"], "p_lo": r["p_lo"], "class": r["class"], "left": r["left"], "right": r["right"],
              "mode": ("node" if r.get("node_resolved") else "across") if row_across(r) else "cut"} for r in rows]
    deltas, over, unreadable = [], [], []
    for r in rows:
        for e in r.get("edges") or ():
            if e.get("over_tolerance"):
                over.append({"t": r["t"], "p_b": e["p_b"], "phase": e["phase"], "delta_rho": e["delta_rho"]})
    for c in v._cut:
        if c.kind == "swap":
            continue
        for row in c.rows:
            t, pb = row["t"], row["p_b"]
            ia = max(i for i in range(len(ps) - 1) if ps[i] <= pb)
            ib = min(ts.index(t), len(ts) - 2)
            rel = {cc for k in range(max(ib - 1, 0), min(ib + 2, len(ts) - 1) + 1) for _, cc in v._partition(k)}
            side = {cc: (None if (q := cc.p_b_ext(t, v._reach)) is None else (-1 if pb < q else 1)) for cc in rel}
            try:
                left = v._value("rho", math.log(pb), t, ia, ib, {**side, c: -1}, False)
                right = v._value("rho", math.log(pb), t, ia, ib, {**side, c: 1}, False)
            except (CellMissing, _NoRead) as e:          # named, never silently dropped
                unreadable.append({"curve": c.id, "t": t, "p_b": pb, "why": type(e).__name__})
                continue
            deltas.append({"curve": c.id, "t": t, "p_b": pb, "rel": abs(left - right) / left})
    rels = sorted(d["rel"] for d in deltas)
    multi = 0
    for t in ts:
        cells = {}
        for c in v._cut:
            pb = c.p_b(t)
            if pb is not None:
                ia = max(i for i in range(len(ps) - 1) if ps[i] <= pb)
                cells[ia] = cells.get(ia, 0) + 1
        multi += sum(1 for n in cells.values() if n >= 2)
    located, unlocated = [], []
    for j, p in enumerate(ps):
        for k in range(len(ts) - 1):
            a, b = v._cell(j, k), v._cell(j, k + 1)
            if a is None or b is None or "frozen" in (a["kind"], b["kind"]):
                continue
            la, lb = _labels(a["assemblage"]), _labels(b["assemblage"])
            if la == lb:
                continue
            on = next((c.id for c in v._curves if (pa := c.p_b(ts[k])) is not None and (pc := c.p_b(ts[k + 1])) is not None
                       and min(pa, pc) <= p <= max(pa, pc)), None)
            item = {"p": p, "t_pair": [ts[k], ts[k + 1]], "labels": [a["assemblage"], b["assemblage"]],
                    "class": "edge" if (la <= lb or lb <= la) else "swap"}
            (located if on is not None else unlocated).append({**item, "on_curve": on} if on is not None else item)
    ends = sum((c.t0 > ts[0]) + (c.t1 < ts[-1]) for c in v._curves)
    v.cut_counts = {k: 0 for k in v.cut_counts}          # the sweep's own counts, not the δ loop's (68 N1)
    for ia in range(len(ps) - 1):
        for ib in range(len(ts) - 1):
            p, t = math.sqrt(ps[ia] * ps[ia + 1]), 0.5 * (ts[ib] + ts[ib + 1])
            if p <= v.p_dataset:
                v._solid(p, t)
    # past-end crossings read across (R1 replaces P0′): in the rows within the extension past a cut run's ends, the
    # label changes within CORNER_REACH columns of its extended P_b that no curve of that row partitions, by type
    past = {"edge": {}, "swap": {}}
    for c in v._cut:
        for k, tk in enumerate(ts):
            if c.p_b(tk) is not None or (q := c.p_b_ext(tk, v._reach)) is None:
                continue
            pbs = [pb for pb, _ in v._partition(k)]
            jq = max(i for i in range(len(ps)) if i == 0 or ps[i] <= q)
            for j in range(max(jq - CORNER_REACH, 0), min(jq + CORNER_REACH, len(ps) - 2) + 1):
                a, b = v._cell(j, k), v._cell(j + 1, k)
                if (a is None or b is None or ps[j + 1] > v.p_dataset or a["assemblage"] == b["assemblage"]
                        or bisect.bisect_left(pbs, ps[j]) != bisect.bisect_left(pbs, ps[j + 1])):
                    continue
                la, lb = _labels(a["assemblage"]), _labels(b["assemblage"])
                past["edge" if (la <= lb or lb <= la) else "swap"][(j, k)] = (abs(b["rho"] / a["rho"] - 1.0),
                                                                              ps[j] / 1e9, tk)
    past = {kd: _dist(list(d.values())) for kd, d in past.items()}
    return {"status": "exported",
            "curves": {k: sum(1 for c in v._curves if c.kind == k) for k in ("swap", "edge", "node")},
            "read": {"counts": {m: sum(1 for x in modes if x["mode"] == m) for m in ("cut", "across", "node")},
                     "rows": modes},
            "across": _across_smoothing(v, [r for r in rows if row_across(r)]),
            "edge_delta": {"n": len(rels), "median": rels[len(rels) // 2] if rels else None,
                           "max": rels[-1] if rels else None,
                           "over_1e-2": [d for d in deltas if d["rel"] > 1e-2], "unreadable": unreadable},
            "over_tolerance": over,
            "edge_drho_tol": (table["boundaries"].get("source") or {}).get("edge_drho_tol"),
            "multi_curve_cells": multi,
            "t_changes": {"located": located, "unlocated": unlocated, "unlocated_count": len(unlocated)},
            "curve_ends": ends, "sweep": dict(v.cut_counts), "past_end_read_across": past}


def view(record, table, t_pot, p_stop=0.0, p_floor=0.0, handover=None):
    """An AssemblageView of a loaded record and its compact table (registry.tables[id]); `handover` is the record's
    HandOver above p_dataset (note 7), or None."""
    return AssemblageView(record, table, t_pot, p_stop, p_floor, handover)


class HandOver:
    """The hand-over above SLB's dataset top for one SLB record (silicate registration §3.4, notes 2, 3 §5 and 7 §3):
    ρ is Zeng 2016's lower-mantle BM2 on the PREM path, T-independent; dT/dP and c_P are the record's own block of the
    hand-over table (its 204 GPa column's fixed state carried in P), read C¹ in (ln P, T) over each T row's nodes up to
    its window p_max; band_HO(P) = band_1·|ln(P/204 GPa)|/ln(204 GPa/P_nb) + band_eq, per T row."""

    def __init__(self, record, table, slb_id, p_end=None):
        self.material_id = record["id"]
        self.p_end = float(p_end) if p_end is not None else P_HANDOVER_END   # the taper's end: 1.5·p_dataset
        prm = record["phases"][0]["eos"]["params"]
        self.rho0, self.k0 = float(prm["rho0"]["value"]), float(prm["k0"]["value"])
        win = record["phases"][0]["window"]
        self.p_max = float(win["p_max"])
        b = table["blocks"][slb_id]
        self.ps = list(b["p_nodes"])
        self.lnps = [math.log(p) for p in self.ps]
        self.p_nb = float(b["p_neighbour"])
        self.rows = sorted(b["rows"], key=lambda r: r["t"])
        self.ts = [r["t"] for r in self.rows]
        self.grade = record["phases"][0]["thermal"]["grade"]

    def rho(self, p):
        """BM2 on the PREM path: P = 1.5·K0·(x^(7/3) − x^(5/3)), x = ρ/ρ0, solved for x ≥ 1 by Newton from above."""
        x = max(1.0, (1.0 + 4.0 * p / (3.0 * self.k0)) ** 0.25 * 1.2)
        for _ in range(60):
            f = 1.5 * self.k0 * (x ** (7.0 / 3.0) - x ** (5.0 / 3.0)) - p
            d = 1.5 * self.k0 * ((7.0 / 3.0) * x ** (4.0 / 3.0) - (5.0 / 3.0) * x ** (2.0 / 3.0))
            step = f / d
            x -= step
            if abs(step) <= 1e-15 * x:
                break
        return self.rho0 * x

    def _val(self, f, ka, kb):
        r = self.rows[kb]
        if r.get("refused"):
            return None
        vals = r[f]
        return vals[ka] if ka < len(vals) else None

    def thermal(self, p, t):
        """(dT/dP, c_P, band_HO) at (P, T), or (None, why) where the block does not answer (a refused row, past a row's
        window p_max, outside its T rows)."""
        if not self.ts[0] <= t <= self.ts[-1]:
            return None, f"outside the hand-over's T rows {self.ts[0]:g}–{self.ts[-1]:g} K"
        top = min(self.ps[-1], self.p_max)
        if p > top:                              # r2 E1 / R1: never extrapolated past the last node or the window
            return None, (f"above the hand-over's last thermal node / window {top:g} Pa (note 2 item 5)")
        x = math.log(p)
        ia = min(max(bisect.bisect_left(self.lnps, x) - 1, 0), len(self.ps) - 2)
        ib = min(max(bisect.bisect_right(self.ts, t) - 1, 0), len(self.ts) - 2)
        out = {}
        try:
            for f in ("dtdp", "c_p"):
                out[f] = cubic2(x, t, self.lnps, self.ts, (lambda ka, kb, f=f: self._val(f, ka, kb)), ia, ib)
        except CellMissing as e:
            kb = e.args[0][1] if isinstance(e.args[0], tuple) else ib
            r = self.rows[min(max(kb, 0), len(self.rows) - 1)]
            if r.get("refused"):
                return None, f"hand-over row {r['t']:g} K refuses: {r['refused']}"
            cut = r.get("cut") or {}
            return None, (f"past the hand-over's thermal window at T row {r['t']:g} K (p_max {r['p_max']:g} Pa; "
                          f"{cut.get('bound', 'the block ends')}) (note 2 items 4–5)")
        bands = []
        for kb in (ib, ib + 1):
            r = self.rows[kb]
            if r.get("band_1") is None or r.get("band_eq") is None:
                continue
            bands.append(r["band_1"] * abs(math.log(p / self.p_end)) / math.log(self.p_end / self.p_nb)
                         + r["band_eq"])
        return (out["dtdp"], out["c_p"], max(bands) if bands else None), None


#: the taper zone's end, 1.5·P_e with P_e = the dataset top 136 GPa (impl note 4 item 1's default; §3.4)
P_HANDOVER_END = 204.0e9
#: note 7 §4: the zone's grade, as §3.4 names it
TAPER_GRADE = "blended (SLB extrapolated, PREM aggregate)"


def _smoothstep(s):
    s = min(max(s, 0.0), 1.0)
    return s * s * (3.0 - 2.0 * s)


class BasalView(mv.RecordView):
    """The basal record (silicate registration §4 Q6, §7.4a): ρ is the layer's declared density, graded «declared»;
    dT/dP, the onset curves and the melt window are the overlying assemblage view's at the same (P, T). A RecordView
    subclass, so the notes collector reads it."""

    def __init__(self, record, density: float, overlying, t_pot: float, p_stop: float = 0.0):
        self.material_id = record["id"]
        self.name = record["id"]                    # legacy BasalConstDensity's name: one GrazeMonitor, as today
        self.t_pot = float(t_pot)
        self.p_stop = float(p_stop)
        self.p_floor = 0.0
        self.kind = record["kind"]
        self.record = freeze(copy.deepcopy(mv.thaw_plain(record)))
        self.boundaries = ()
        self.phases = []
        self.notes: list = []
        self.density_declared = float(density)
        self.overlying = overlying
        self.onset_curve_names = list(getattr(overlying, "onset_curve_names", ()))
        self._phase_id = self.record["phases"][0]["id"]

    def state(self, p: float, t: float, guess_rho=None):
        self.notes.clear()
        got = self.overlying.state(p, t)
        if isinstance(got, st.Stop):
            rec = got.record
            if isinstance(rec, mv.RecordRefusal):
                return st.Stop("refused", mv.RecordRefusal(self.material_id, p, t, rec.refusal,
                                                           f"the overlying record {rec.material_id}: {rec.why}"))
            return got
        self.notes.append(mv.DeclaredNote(self.material_id, self._phase_id,
                                          "molten basal layer: density declared by the layer (graded «declared»; band "
                                          "origin «the declared layer density»); dT/dP from the overlying assemblage "
                                          f"record {self.overlying.material_id} at the same (P, T)"))
        # the overlying view's dT/dP band rides with the basal layer's answer, attributed to the basal record (68)
        self.notes.extend(dataclasses.replace(n, material_id=self.material_id)
                          for n in got[2] if isinstance(n, mv.BandNote) and n.dtdp_error is not None)
        return (self.density_declared, got[1], tuple(self.notes))

    def density(self, p: float, t: float):
        got = self.state(p, t)
        return got if isinstance(got, st.Stop) else got[0]

    def dtdp(self, p: float, t: float):
        got = self.state(p, t)
        return got if isinstance(got, st.Stop) else got[1]

    def phase_read(self, p: float, t: float):
        got = self.state(p, t)
        return got if isinstance(got, st.Stop) else self._phase_id

    def porosity(self, p: float) -> float:
        return 0.0

    def seams(self) -> tuple:
        return ()

    def transitions(self) -> tuple:
        return ()

    def source_seams(self) -> tuple:
        return ()

    def onset_curves(self, p: float, t: float) -> list:
        return self.overlying.onset_curves(p, t)
