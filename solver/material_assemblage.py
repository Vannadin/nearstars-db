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


class _NoNode(Exception):
    """A corner row of a cut read has no read-side node at all (scope note §3 (b)): the T row's index."""


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
NO_NODE_WHY = "no read-side node in row {t:g} K across the exported boundary"


def _labels(label) -> frozenset:
    return frozenset(label.split("+"))


class _Curve:
    """One exported boundary curve: a run of rows adjacent in T of one group (scope note §3 (a)). `kind` is «swap» (a
    step), «edge» (a converged edge of an edge class: no step, the c′ correction) or «node» (a node-resolved row, read
    as an edge). P_b(T) is piecewise-linear in T between its rows and absent outside them."""

    def __init__(self, cid, kind, phase, rows):
        self.id, self.kind, self.phase = cid, kind, phase
        self.rows = sorted(rows, key=lambda r: r["t"])            # dicts: t, p_b, left, right (label sets), band
        self.t0, self.t1 = self.rows[0]["t"], self.rows[-1]["t"]
        self.p_range = (min(r["p_b"] for r in self.rows), max(r["p_b"] for r in self.rows))

    def p_b(self, t):
        if t < self.t0 or t > self.t1:
            return None
        rs = self.rows
        for a, b in zip(rs, rs[1:]):
            if a["t"] <= t <= b["t"]:
                w = (t - a["t"]) / (b["t"] - a["t"])
                return a["p_b"] + w * (b["p_b"] - a["p_b"])
        return rs[0]["p_b"]

    def nearest(self, t):
        return min(self.rows, key=lambda r: abs(r["t"] - t))

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
                "left_label": r["left"], "right_label": r["right"], "band": r.get("band")}
        if r.get("node_resolved"):
            groups.setdefault(("node", left, right, None), []).append({**base, "p_b": r["p_b"]})
        elif r["class"] == "swap":
            groups.setdefault(("swap", left, right, None), []).append({**base, "p_b": r["p_b"]})
        else:
            for e in r["edges"]:
                groups.setdefault(("edge", left, right, e["phase"]), []).append({**base, "p_b": e["p_b"]})
    return groups


def build_curves(boundaries, ts):
    """The curves of an exported block: each group split into runs of rows adjacent on the table's T grid. A group
    with two rows at one T is not a function of T: TableStop (68 M6)."""
    idx = {t: k for k, t in enumerate(ts)}
    out = []
    for key, rows in sorted(curve_groups(boundaries).items(), key=lambda kv: repr(kv[0])):
        seen = {}
        for r in rows:
            if r["t"] in seen:
                raise TableStop(f"exported boundary group {key[0]} {sorted(key[1])}→{sorted(key[2])}"
                                f"{'' if key[3] is None else ' (' + key[3] + ')'} has two rows at {r['t']:g} K: P_b(T) "
                                "is not single-valued", check="boundaries")
            seen[r["t"]] = r
        run = []
        for r in sorted(rows, key=lambda r: r["t"]):
            if run and idx[r["t"]] != idx[run[-1]["t"]] + 1:
                out.append(_Curve(len(out), key[0], key[3], run))
                run = []
            run.append(r)
        if run:
            out.append(_Curve(len(out), key[0], key[3], run))
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


def _pchip_1d(x, xs, ys):
    """A row's branch at x from its read-side nodes (sorted xs, 1–4 of them): PCHIP inside, and past the ends the end
    node's PCHIP end slope, as at a table end (smooth_table's rule, in x units)."""
    n = len(xs)
    if n == 1:
        return ys[0]
    if xs[0] <= x <= xs[-1]:
        i = min(max(next(k for k in range(n - 1) if xs[k + 1] >= x), 0), n - 2)
        return _cubic1(x, xs, ys, i)
    if x > xs[-1]:
        h0, d0 = xs[-1] - xs[-2], (ys[-1] - ys[-2]) / (xs[-1] - xs[-2])
        if n >= 3:
            h1, d1 = xs[-2] - xs[-3], (ys[-2] - ys[-3]) / (xs[-2] - xs[-3])
            m = _end_slope(h0, h1, d0, d1)
        else:
            m = d0
        return ys[-1] + m * (x - xs[-1])
    h0, d0 = xs[1] - xs[0], (ys[1] - ys[0]) / (xs[1] - xs[0])
    if n >= 3:
        h1, d1 = xs[2] - xs[1], (ys[2] - ys[1]) / (xs[2] - xs[1])
        m = _end_slope(h0, h1, d0, d1)
    else:
        m = d0
    return ys[0] + m * (x - xs[0])


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
        b = table.get("boundaries") or {}
        self._curves = build_curves(b, self.ts) if b.get("status") == "exported" else []
        #: the cut-read counts of this view (scope note §3 (b), 68 S1): reads cut, corner rows extrapolated past the
        #: stencil span with their largest reach in cells, rows refused with no read-side node, rows classified by label
        self.cut_counts = {"cut_reads": 0, "corner_extrapolations": 0, "corner_max_reach": 0, "corner_max_nodes": 0,
                           "no_node_refusals": 0, "label_rule_rows": 0, "side_fallbacks": 0}
        self._marks = {"corner_rows": set(), "label_rows": set(), "reach": 0, "corner_nodes": 0}

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
        cuts = self._crossing(pr, t, ia, ib)
        if cuts:
            return self._solid_cut(p, t, pr, x, ia, ib, cuts)
        cut = (lambda ka: self.ps[ka] <= self.p_dataset)
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
        corners = [self._cell(a, b) for a in (ia, ia + 1) for b in (ib, ib + 1)]
        return out["rho"], out["dtdp_eq"], out["c_p"], [c for c in corners if c is not None]

    # exported boundaries (scope note §3 (b)–(c″)) ─────────────────────────────────────────────────────────────
    def _val(self, f, j, k):
        c = self._cell(j, k)
        if c is None:
            return None
        if f == "c_p" and c["kind"] != "frozen":
            return c.get("c_p_eq")
        return c.get(f)

    def _crossing(self, pr, t, ia, ib):
        """The curves crossing the read's stencil P span (columns ia−1 … ia+2) at the read's T or at any stencil row's
        T (68 M3). Empty: the read is uncut, cubic2 unchanged."""
        if not self._curves:
            return []
        c0, c1 = max(ia - 1, 0), min(ia + 2, len(self.ps) - 1)
        ta, tb = self.ts[max(ib - 1, 0)], self.ts[min(ib + 2, len(self.ts) - 1)]
        lo, hi = self.ps[c0], self.ps[c1]
        out = []
        for c in self._curves:
            # anywhere on [t_{ib−1}, t_{ib+2}] (68 B1): P_b is piecewise linear, so its range over each segment between
            # consecutive samples (the stencil rows, t, the curve's own rows inside) is its two ends'
            tts = sorted({t, ta, tb, *(self.ts[k] for k in range(max(ib - 1, 0), min(ib + 2, len(self.ts) - 1) + 1)),
                          *(r["t"] for r in c.rows if ta <= r["t"] <= tb)})
            pbs = [c.p_b(tt) for tt in tts]
            hit = any(pb is not None and lo < pb < hi for pb in pbs) or any(
                a is not None and b is not None and min(a, b) < hi and max(a, b) > lo for a, b in zip(pbs, pbs[1:]))
            if hit:
                out.append(c)
        return out

    def _node_ok(self, j, k, side, cuts):
        """A node is on the read's side of every crossing curve, judged at its own T (r2 M1); past a curve's ends by
        its label against the read side's label at the curve's nearest row (68 M2)."""
        tk = self.ts[k]
        for c in cuts:
            pb = c.p_b(tk)
            if pb is not None:
                if (-1 if self.ps[j] < pb else 1) != side[c]:
                    return False
            else:
                r = c.nearest(tk)
                cell = self._cell(j, k)
                self._marks["label_rows"].add(k)
                if cell is None or _labels(cell["assemblage"]) != (r["left"] if side[c] < 0 else r["right"]):
                    return False
        return True

    def _cut_value(self, f, x, t, ia, ib, side, cuts):
        """P first per T row from that row's read-side nodes, then T (68 M1). An outer row with no read-side node in
        the span drops; a corner row extrapolates from the nearest read-side nodes further out (4-node reach), or
        raises _NoNode; a read-side corner of the read cell with no cell or no value is CellMissing, as uncut."""
        n_p, n_t = len(self.ps), len(self.ts)
        c0, c1 = max(ia - 1, 0), min(ia + 2, n_p - 1)
        rows = {}
        for k in range(max(ib - 1, 0), min(ib + 2, n_t - 1) + 1):
            corner = k in (ib, ib + 1)
            if corner:
                for j in (ia, ia + 1):
                    if self._node_ok(j, k, side, cuts) and self._val(f, j, k) is None:
                        raise CellMissing((j, k))
            ok = [j for j in range(n_p)                                       # the p_dataset cut stays (68 B2)
                  if self.ps[j] <= self.p_dataset and self._node_ok(j, k, side, cuts) and self._val(f, j, k) is not None]
            use = [j for j in ok if c0 <= j <= c1]
            if not use:
                if not corner:
                    continue
                near = sorted(ok, key=lambda j: abs(self.lnps[j] - x))
                if not near or (c0 - near[0] if near[0] < c0 else near[0] - c1) > 4:   # the nearest within 4 columns
                    raise _NoNode(k)
                use = sorted(near[:4])
                reach = min(abs(j - ia) if j < ia else abs(j - ia - 1) for j in use)
                self._marks["corner_rows"].add(k)
                self._marks["reach"] = max(self._marks["reach"], reach)
                self._marks["corner_nodes"] = max(self._marks["corner_nodes"], len(use))
            rows[k] = _pchip_1d(x, [self.lnps[j] for j in use], [self._val(f, j, k) for j in use])
        return _cubic1(t, self.ts, _Seq(rows, n_t), ib)

    def _read_side(self, c, p, t, ia, ib):
        """The read's side of one curve. Inside the curve's T range, by P_b(t). Past either end (r2's R1 ruling, 68's
        three points): by the labels of the read cell's two corner nodes on its row nearest the curve that lies past the
        end — past the last row t1, row ib if the read cell lies wholly past (t_ib > t1), else ib+1 (the first row past);
        before the first row t0, row ib+1 if t_{ib+1} < t0, else ib (the last row below). A corner matching the
        curve's left (right) label puts the read left (right); one matching corner and one third label still decide
        (the third-label node drops by the label rule); corners matching opposite sides, or none, fall back to the
        nearest row's P_b, counted («side_fallbacks», with the Q3/M2 disclosure)."""
        pb = c.p_b(t)
        if pb is not None:
            return -1 if p < pb else 1
        if t > c.t1:
            k = ib if self.ts[ib] > c.t1 else ib + 1
        else:
            k = ib + 1 if self.ts[ib + 1] < c.t0 else ib
        r = c.nearest(t)
        hits = set()
        for j in (ia, ia + 1):
            cell = self._cell(j, k)
            if cell is None:
                continue
            lab = _labels(cell["assemblage"])
            if lab == r["left"]:
                hits.add(-1)
            elif lab == r["right"]:
                hits.add(1)
        if len(hits) == 1:
            return hits.pop()
        self.cut_counts["side_fallbacks"] += 1
        return -1 if p < r["p_b"] else 1

    def _close_marks(self):
        """One count per read, and per (read, row) for corner and label rows, whatever the field and δ calls (68 N1)."""
        m = self._marks
        self.cut_counts["corner_extrapolations"] += len(m["corner_rows"])
        self.cut_counts["label_rule_rows"] += len(m["label_rows"])
        self.cut_counts["corner_max_reach"] = max(self.cut_counts["corner_max_reach"], m["reach"])
        self.cut_counts["corner_max_nodes"] = max(self.cut_counts["corner_max_nodes"], m["corner_nodes"])

    def _solid_cut(self, p, t, pr, x, ia, ib, cuts):
        """The cut read (scope note §3 (b)–(c″)): one-sided per side; a swap in the read cell steps (with §3.3's
        note); a single edge or node-resolved curve in the read cell is corrected linearly in ln P across the cell, 0 at
        the nodes and ±δ/2 at P_b with the equal split (r2 Q2, T1); two or more curves in the cell are read linear in
        ln P between the outermost curves' one-sided values (r2 Q1), with no edge correction there (r2 N1)."""
        self.cut_counts["cut_reads"] += 1
        self._marks = {"corner_rows": set(), "label_rows": set(), "reach": 0, "corner_nodes": 0}   # per read (68 N1)
        side = {c: self._read_side(c, pr, t, ia, ib) for c in cuts}
        lo, hi = self.ps[ia], self.ps[ia + 1]
        cell = sorted((c for c in cuts if (pb := c.p_b(t)) is not None and lo <= pb <= hi), key=lambda c: c.p_b(t))
        xl, xh = self.lnps[ia], self.lnps[ia + 1]
        out = {}
        try:
            for f in ("rho", "dtdp_eq", "c_p"):
                if len(cell) >= 2 and math.log(cell[0].p_b(t)) <= x <= math.log(cell[-1].p_b(t)):
                    xa, xb = math.log(cell[0].p_b(t)), math.log(cell[-1].p_b(t))
                    left = {**side, **{c: -1 for c in cell}}
                    right = {**side, **{c: 1 for c in cell}}
                    va = self._cut_value(f, xa, t, ia, ib, left, cuts)
                    vb = self._cut_value(f, xb, t, ia, ib, right, cuts)
                    out[f] = va + (vb - va) * (x - xa) / (xb - xa)
                    continue
                v = self._cut_value(f, x, t, ia, ib, side, cuts)
                if len(cell) == 1 and cell[0].kind in ("edge", "node"):
                    c = cell[0]
                    xbd = math.log(c.p_b(t))
                    d = (self._cut_value(f, xbd, t, ia, ib, {**side, c: -1}, cuts)
                         - self._cut_value(f, xbd, t, ia, ib, {**side, c: 1}, cuts))
                    if side[c] < 0:
                        v -= 0.5 * d * (x - xl) / (xbd - xl)
                    else:
                        v += 0.5 * d * (xh - x) / (xh - xbd)
                out[f] = v
        except _NoNode as e:
            self._close_marks()
            self.cut_counts["no_node_refusals"] += 1
            return self._refuse(p, t, "input.material_out_of_data", NO_NODE_WHY.format(t=self.ts[e.args[0]]))
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
        if len(cell) >= 2:
            self.notes.append(mv.DeclaredNote(self.material_id, PHASE_ID, MULTI_NOTE))
        elif len(cell) == 1 and cell[0].kind == "swap":
            a, b = cell[0].p_range
            self.notes.append(mv.DeclaredNote(self.material_id, PHASE_ID,
                                              f"{SWAP_NOTE}; P {a / 1e9:.4g}–{b / 1e9:.4g} GPa"))
        corners = [self._cell(a, b) for a in (ia, ia + 1) for b in (ib, ib + 1)
                   if self._node_ok(a, b, side, cuts)]
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
        """Exported curves as solid_solid seams (§3.3): a swap steps, an edge or node-resolved curve does not; pending
        boundaries give none (every label change is read across)."""
        return tuple(((f"{c.kind}{c.id}:{c.rows[0]['left_label']}", f"{c.rows[0]['right_label']}"), "solid_solid",
                      {"form": "assemblage_curve", "id": c.id}) for c in self._curves)

    def boundary_pressure(self, curve, t):
        if curve.get("form") == "assemblage_curve":
            return self._curves[curve["id"]].p_b(t)
        return super().boundary_pressure(curve, t)

    def source_seams(self) -> tuple:
        return ()

    def onset_curves(self, p: float, t: float) -> list:
        return _lm().silicate_solidus_onset(p, t, self.variant)



def boundary_disclosures(record, table) -> dict:
    """The per-table disclosures of an exported block (scope note §3 (c′), (c″), §5; 68 M5, S1), report-only:
    - edge_delta: per edge or node-resolved curve row, |δ|/ρ = |L(P_b) − R(P_b)|/L of the one-sided ρ reads at the row's
      T, with the rows over 1e-2 listed for directing (r2 Q2);
    - over_tolerance: the pass's own over-tolerance edges;
    - multi_curve_cells: (T row, P cell) pairs holding two or more curves (r2 Q1);
    - t_changes: label changes along T inside a column, split «on curve <id>» (a sloped curve's P_b crosses the column
      between the rows) from unlocated ones (68 M5), with curve ends counted (r2 M2);
    - sweep: the cut-read counts of one read at the centre of every cell (68 S1)."""
    v = view(record, table, 1600.0)
    if not v._curves:
        return {"status": (table.get("boundaries") or {}).get("status")}
    ts, ps = v.ts, v.ps
    deltas, over, unreadable = [], [], []
    for r in table["boundaries"]["rows"]:
        for e in r.get("edges") or ():
            if e.get("over_tolerance"):
                over.append({"t": r["t"], "p_b": e["p_b"], "phase": e["phase"], "delta_rho": e["delta_rho"]})
    for c in v._curves:
        if c.kind == "swap":
            continue
        for row in c.rows:
            t, pb = row["t"], row["p_b"]
            ia = max(i for i in range(len(ps) - 1) if ps[i] <= pb)
            ib = min(ts.index(t), len(ts) - 2)
            cuts = v._crossing(pb, t, ia, ib)
            side = {cc: cc.side_of(pb, t) for cc in cuts}
            try:
                left = v._cut_value("rho", math.log(pb), t, ia, ib, {**side, c: -1}, cuts)
                right = v._cut_value("rho", math.log(pb), t, ia, ib, {**side, c: 1}, cuts)
            except (CellMissing, _NoNode) as e:          # named, never silently dropped
                unreadable.append({"curve": c.id, "t": t, "p_b": pb, "why": type(e).__name__})
                continue
            deltas.append({"curve": c.id, "t": t, "p_b": pb, "rel": abs(left - right) / left})
    rels = sorted(d["rel"] for d in deltas)
    multi = 0
    for t in ts:
        cells = {}
        for c in v._curves:
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
            if v._crossing(p, t, ia, ib):
                v._solid(p, t)
    return {"status": "exported", "curves": {k: sum(1 for c in v._curves if c.kind == k) for k in ("swap", "edge", "node")},
            "edge_delta": {"n": len(rels), "median": rels[len(rels) // 2] if rels else None,
                           "max": rels[-1] if rels else None,
                           "over_1e-2": [d for d in deltas if d["rel"] > 1e-2], "unreadable": unreadable},
            "over_tolerance": over, "multi_curve_cells": multi,
            "t_changes": {"located": located, "unlocated": unlocated, "unlocated_count": len(unlocated)},
            "curve_ends": ends, "sweep": dict(v.cut_counts)}


def view(record, table, t_pot, p_stop=0.0, p_floor=0.0):
    """An AssemblageView of a loaded record and its compact table (registry.tables[id])."""
    return AssemblageView(record, table, t_pot, p_stop, p_floor)


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
