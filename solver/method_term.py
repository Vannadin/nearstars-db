# T2 적분법 항 측정 — (천체, 상태)마다 적응 DP45 와 옛 격자 고정 RK4 를 같은 프로세스에서 풀어 키별 상대차 d 와 (천체, 키) 항을 냄
"""The T2 integration-method term (rewrite/oracle/t2-method-term-registration.md).

    solver/.venv/bin/python -m solver.method_term run BODY_YAML POINTS_JSON OUT_JSONL [--steps N]
    solver/.venv/bin/python -m solver.method_term terms OUT_JSONL... > terms.json
    solver/.venv/bin/python -m solver.method_term controls BODY_YAML > controls.json
    solver/.venv/bin/python -m solver.method_term crosscheck CAP_O1_DIR OUT_JSONL... > crosscheck.json

run: one JSON line per (body, state), appended to OUT_JSONL as each state finishes; states already in the file are
skipped (resume). The declared state runs run_oracle.one in both modes (interior quantities and the legacy nodes, with
the run_oracle default options); every T_pot state of POINTS_JSON (the O9 points) runs the solve only (O9 compares
interior_layers values). For each state the adaptive solve comes first; its accepted profile gives the centre density
ρ_c = 3 m_end / (4π r_end³), and the fixed mode's grid is dr = (3M / (4π ρ_c))^(1/3) / N (interior.py's r_scale / STEPS).
d = (y_fixed − y_adaptive) / |y_adaptive| per numeric key; null with flag `zero_reference` where y_adaptive = 0.
terms: per (body, key), max |d| over the states whose two outcome kinds are both «answer», with count and argmax.
"""
from __future__ import annotations

import dataclasses
import json
import math
import sys
import time
from pathlib import Path

from solver import context, from_v1, result, run_oracle as ro, solve as sv

STEPS = 1500                       # interior.STEPS at 097a8aa3


def grid_dr(body, answer, steps: int = STEPS):
    """(dr, ρ_c) from the adaptive answer's innermost profile node."""
    prof = answer.profiles[body.layers[0].id]
    m, r = prof["m"][-1], prof["r"][-1]
    rho_c = 3.0 * m / (4.0 * math.pi * r ** 3)
    return (3.0 * body.mass / (4.0 * math.pi * rho_c)) ** (1.0 / 3.0) / steps, rho_c


def _num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _flat(rec: dict) -> dict:
    """Numeric values of a run_oracle record: interior quantities by key, legacy node values as «node.key»."""
    out = {q["key"]: q["point"] for q in rec["quantities"]}
    for node, r in rec["legacy_nodes"].items():
        for k, v in r["values"].items():
            if _num(v):
                out[f"{node}.{k}"] = v
    return out


def _kind(out) -> str:
    return {"Answer": "answer", "Refusal": "refusal", "NoAnswer": "no_answer"}[type(out).__name__]


def _diff(a: dict, f: dict) -> tuple:
    d, flags = {}, {}
    for k, va in a.items():
        vf = f.get(k)
        if not (_num(va) and _num(vf)):
            continue
        if va == 0.0:
            d[k] = None
            if vf != 0.0:
                flags[k] = "zero_reference"
            continue
        d[k] = (vf - va) / abs(va)
    return d, flags


def _body_at(body_yaml, t_pot):
    got = from_v1.load_v1(body_yaml)
    body = got[0] if isinstance(got, tuple) else got
    if t_pot is not None and not isinstance(body, result.Refusal):
        body = dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=t_pot))
    return body


def one_state(body_yaml: str, state, tag: str, steps: int = STEPS) -> dict:
    t_pot = None if state == "declared" else float(state)
    body = _body_at(body_yaml, t_pot)
    rec = {"body": Path(body_yaml).stem, "state": state, "tag": tag, "steps": steps}
    if isinstance(body, result.Refusal):
        return {**rec, "kind_adaptive": "refusal", "kind_fixed": None, "flag": "input_refusal"}
    c0 = time.process_time()
    a, _ = sv.solve(body, context.Options(sensitivity_dt=0.0))
    rec["cpu_adaptive_s"] = time.process_time() - c0
    rec["kind_adaptive"] = _kind(a)
    if not isinstance(a, result.Answer):
        rec.update(kind_fixed=None, flag="adaptive_not_answer",
                   adaptive_outcome=getattr(a, "id", None) or getattr(a, "reason", None))
        return rec
    dr, rho_c = grid_dr(body, a, steps)
    rec.update(dr=dr, rho_c=rho_c)
    if state == "declared":
        base = context.Options()
        c0 = time.process_time()
        ra = ro.one(body_yaml, "declared", base)
        rf = ro.one(body_yaml, "declared", dataclasses.replace(base, fixed_dr=dr))
        rec["cpu_records_s"] = time.process_time() - c0
        rec["kind_adaptive"], rec["kind_fixed"] = ra["outcome_kind"], rf["outcome_kind"]
        va, vf = _flat(ra), _flat(rf)
        rec["options"] = result.plain(dataclasses.asdict(base))
    else:
        c0 = time.process_time()
        f, _ = sv.solve(body, context.Options(sensitivity_dt=0.0, fixed_dr=dr))
        rec["cpu_fixed_s"] = time.process_time() - c0
        rec["kind_fixed"] = _kind(f)
        va = {q.key: q.point for q in a.quantities}
        vf = {q.key: q.point for q in f.quantities} if isinstance(f, result.Answer) else {}
        if not isinstance(f, result.Answer):
            rec["fixed_outcome"] = getattr(f, "id", None) or getattr(f, "reason", None)
    rec["adaptive"], rec["fixed"] = va, vf
    if rec["kind_adaptive"] != rec["kind_fixed"]:
        rec["flag"] = "outcome_differs"
        return rec
    rec["d"], rec["flags"] = _diff(va, vf)
    return rec


def _states(stem: str, points_json: str) -> list:
    out = [("declared", "O1")]
    if points_json != "-":
        for b, t, tag in json.loads(Path(points_json).read_text(encoding="utf-8")):
            if b == stem and all(s != float(t) for s, _ in out):
                out.append((float(t), tag))
    return out


def run(body_yaml: str, points_json: str, out_jsonl: str, steps: int = STEPS) -> int:
    out = Path(out_jsonl)
    done = set()
    if out.exists():
        text = out.read_text(encoding="utf-8")
        lines = text.splitlines(keepends=True)
        if lines and not lines[-1].endswith("\n"):            # a kill mid-write: drop the partial last line
            out.write_text("".join(lines[:-1]), encoding="utf-8")
            lines = lines[:-1]
        for line in lines:
            r = json.loads(line)
            done.add((r["body"], repr(r["state"])))
    header = ro._header(context.Options(sensitivity_dt=0.0), "")
    stem = Path(body_yaml).stem
    with out.open("a", encoding="utf-8") as fh:
        for state, tag in _states(stem, points_json):
            if (stem, repr(state)) in done:
                continue
            rec = one_state(body_yaml, state, tag, steps)
            rec["header"] = header
            fh.write(json.dumps(result.plain(rec), ensure_ascii=True, allow_nan=False) + "\n")
            fh.flush()
    return 0


#: recorded, never a band (r2 N1): marked in terms.json so a table quoting it cannot pick them up
EVIDENCE_ONLY_BODIES = {"mars": "note 5: Mars has no T2 band"}
CLASS_R_KEYS = {("earth", "core_energy_balance.balance_residual"): "class R (tolerance-classes note 2)",
                ("earth", "core_energy_balance.core_profile_mass_residual"): "class R (tolerance-classes note 2)"}


def _use(body: str, key: str):
    why = EVIDENCE_ONLY_BODIES.get(body) or CLASS_R_KEYS.get((body, key))
    return (False, why) if why else (True, None)


def terms(paths) -> dict:
    per: dict = {}
    flagged: list = []
    for p in paths:
        for line in Path(p).read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            if r.get("flag"):
                flagged.append([r["body"], r["state"], r["flag"]])
                continue
            for k, d in r["d"].items():
                if d is None:
                    continue
                use, why = _use(r["body"], k)
                e = per.setdefault(r["body"], {}).setdefault(k, {"term": 0.0, "count": 0, "at": None, "use": use,
                                                                 **({"why": why} if why else {})})
                e["count"] += 1
                if abs(d) > e["term"] or e["at"] is None:
                    e["term"], e["at"] = max(abs(d), e["term"]), r["state"]
            for k, why in r.get("flags", {}).items():
                flagged.append([r["body"], r["state"], f"{k}:{why}"])
    return {"terms": per, "flagged": flagged}


ORDER_KEYS = ("cmb_temperature", "core_temperature")
ORDER_RANGE = (1.6, 2.4)


def controls(body_yaml: str) -> dict:
    """Registration controls 1 and 2 at the declared state: the fixed solve twice gives identical values (null), and
    STEPS 2N halves the temperature keys' d (ratio d(N)/d(2N) within ORDER_RANGE: Euler in P, first order)."""
    body = _body_at(body_yaml, None)
    opt = context.Options(sensitivity_dt=0.0)
    a, _ = sv.solve(body, opt)
    va = {q.key: q.point for q in a.quantities}
    dr, rho_c = grid_dr(body, a, STEPS)
    outs = [sv.solve(body, dataclasses.replace(opt, fixed_dr=d))[0] for d in (dr, dr, dr / 2.0)]
    if not all(isinstance(o, result.Answer) for o in outs):
        return {"body": Path(body_yaml).stem, "dr": dr, "rho_c": rho_c, "fixed_not_answer": [_kind(o) for o in outs],
                "null_identical": False, "order_holds": False, "holds": False}
    runs = [{q.key: q.point for q in o.quantities} for o in outs]
    null = runs[0] == runs[1]
    ratios = {k: (runs[0][k] - va[k]) / (runs[2][k] - va[k]) for k in ORDER_KEYS
              if k in va and runs[2][k] != va[k]}
    order = bool(ratios) and all(ORDER_RANGE[0] <= v <= ORDER_RANGE[1] for v in ratios.values())
    return {"body": Path(body_yaml).stem, "dr": dr, "rho_c": rho_c, "null_identical": null, "order_ratios": ratios,
            "order_range": list(ORDER_RANGE), "order_holds": order, "holds": null and order}


RHO_RANGE = (0.5, 2.0)               # r2 on the registration, (2): outside it the term is not representative
# old interior_layers units → the rewrite's SI. No «km»: the rewrite emits its km keys (basal_layer_thickness_km,
# core_plus_layer_radius_solved_km) in km, so km ↔ km is factor 1 (r2 N3; compare_map's km → m row is for other keys)
OLD_UNIT_SCALE = {"R_earth": 6.371e6, "GPa": 1e9}


def _old_flat(cap: dict) -> dict:
    """Numeric values of an O1 capture, in the keys of `_flat`: interior_layers by key (converted to SI), the other
    nodes as «node.key» (old units on both sides: the rewrite's legacy nodes are the old code)."""
    out = {}
    for node, r in cap["results"].items():
        vals, units = r.get("values") or {}, r.get("units") or {}
        for k, v in vals.items():
            if not _num(v):
                continue
            if node == "interior_layers":
                out[k] = v * OLD_UNIT_SCALE.get(units.get(k), 1.0)
            else:
                out[f"{node}.{k}"] = v
    return out


def crosscheck(cap_dir: str, paths) -> dict:
    """Control 3 as a classifier (r2): at each O1 declared state, per key, ρ = |old − adaptive| / |fixed − adaptive|.
    A key with ρ outside RHO_RANGE (or fixed = adaptive ≠ old) is «term not representative»: listed for directing, so
    a later T2 verdict on it is not read as evidence about the method. The term itself never uses old − adaptive."""
    rows, odd = [], []
    for p in paths:
        for line in Path(p).read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            if r["state"] != "declared" or r.get("flag"):
                continue
            capf = Path(cap_dir) / f"{r['body']}.json"
            if not capf.exists():
                continue
            old = _old_flat(json.loads(capf.read_text(encoding="utf-8")))
            for k, va in sorted(r["adaptive"].items()):
                vf, vo = r["fixed"].get(k), old.get(k)
                if not (_num(va) and _num(vf) and _num(vo)):
                    continue
                go, gf = abs(vo - va), abs(vf - va)
                rho = (go / gf) if gf else (None if go == 0.0 else math.inf)
                ok = rho is None or RHO_RANGE[0] <= rho <= RHO_RANGE[1]
                row = {"body": r["body"], "key": k, "old_minus_adaptive": vo - va, "fixed_minus_adaptive": vf - va,
                       "rho": rho if rho is None or math.isfinite(rho) else "inf", "representative": ok}
                rows.append(row)
                if not ok:
                    odd.append([r["body"], k, row["rho"]])
    return {"rho_range": list(RHO_RANGE), "rows": rows, "not_representative": odd}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    steps = STEPS
    if "--steps" in argv:
        i = argv.index("--steps")
        steps = int(argv[i + 1])
        del argv[i:i + 2]
    if argv[:1] == ["run"] and len(argv) == 4:
        return run(argv[1], argv[2], argv[3], steps)
    if argv[:1] == ["controls"] and len(argv) == 2:
        c = controls(argv[1])
        print(json.dumps(c, indent=1, ensure_ascii=True, allow_nan=False))
        return 0 if c["holds"] else 1
    if argv[:1] == ["crosscheck"] and len(argv) >= 3:
        print(json.dumps(crosscheck(argv[1], argv[2:]), indent=1, ensure_ascii=True, allow_nan=False))
        return 0
    if argv[:1] == ["terms"] and len(argv) >= 2:
        print(json.dumps(terms(argv[1:]), indent=1, ensure_ascii=True, allow_nan=False))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
