# 측정·오너 노드의 공통 읽기 — DB 기록에서 권장 항목을 읽어 값·밴드·출처(record)를 내고, 관측이 아닌 기록은 이름 대고 거절한다 (계약 §4.2, prereg N8·N13)
"""Generic reader for measured and owner nodes (contract `node-contract.frozen.md` §4.2, §4.4).

The spec's `reads` block names the file, where the body's block sits, the record list, and per output the value
field, the printed-uncertainty field and the factor to SI.

measured: the block must be a list (the curated form). Exactly one entry is `recommended`; its `method` must be in
the spec's closed `methods` list, else `node.record_not_measured {file, key, method}` (N13), citation or not. The
point is the value, the band the printed ± (`input` source, «catalogue uncertainty as printed»), the source the
record `{file, key, sha256}` with the paper's bibcode in `cites`. Other entries of the same list whose value lies
outside that band are named in a `measurement_spread` note (D-5); they never widen the band. Grade `measured`,
method `read`.

owner: the block is the owner value file's entry for the body: `{value, decision}`. Grade `authored`, method
`chosen`, source `user_declared: <decision>`, no band.
"""
from __future__ import annotations

import json
from pathlib import Path

from solver import refusals as rf
from solver.result import Answer, Band, Note, Quantity, SolverInfo, Sources, SourceBand, Where

from nodes import run_id as rid
from nodes.types import NodeProvenance, SourceRef

REPO = Path(__file__).resolve().parent.parent
_CACHE = {}


def _load(file, db_root):
    path = Path(db_root or REPO) / file
    if path not in _CACHE:
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".json":
            _CACHE[path] = json.loads(text)
        else:
            from solver import yamlio
            _CACHE[path] = yamlio.parse(text)
    return _CACHE[path]


def _block(spec, body, db_root):
    """The body's record block and its key text, or (None, key)."""
    r = spec["reads"]
    data = _load(r["file"], db_root)
    if r["path"] == "{self}":
        key = f"{body['name']}.{r['field']}"
        entry = data.get(body["name"]) or {}
        return entry.get(r["field"]), key
    if r["path"] == "{host}[pl_name={self}]":
        hosts = body.get("hosts") or []
        if not hosts:
            return None, f"?[pl_name={body['name']}].{r['field']}"
        key = f"{hosts[0]}[pl_name={body['name']}].{r['field']}"
        for pl in data.get(hosts[0]) or []:
            if pl.get("pl_name") == body["name"]:
                return pl.get(r["field"]), key
        return None, key
    raise ValueError(f"unknown reads.path {r['path']!r}")


def run(spec, body, where, db_root=None):
    r = spec["reads"]
    node = spec["id"]
    block, key = _block(spec, body, db_root)
    if block is None:
        return rf.make("node.input_missing", where, input=r["field"], **{"from": f"{r['file']}:{key}"}), None
    if spec["kind"] == "owner":
        return _owner(spec, body, block, key, where)
    if not isinstance(block, list):
        return rf.make("node.record_not_measured", where, file=r["file"], key=key, method=None), None
    rec = [i for i, e in enumerate(block) if e.get("recommended")]
    if len(rec) != 1:
        return rf.make("node.input_missing", where, input=f"{r['field']} (recommended)",
                       **{"from": f"{r['file']}:{key} has {len(rec)} recommended entries"}), None
    i = rec[0]
    entry = block[i]
    ekey = f"{key}[{i}]"
    method = entry.get("method")
    adopted = method is not None and method in (r.get("adopted_methods") or ())
    if method not in r["methods"] and not adopted:
        return rf.make("node.record_not_measured", where, file=r["file"], key=ekey, method=method), None
    records = {ekey: rid.entry_sha256(entry)}
    for j, other in enumerate(block):            # the spread / window checks read the others, so they bind the run id
        if j != i:
            records[f"{key}[{j}]"] = rid.entry_sha256(other)
    run_body = body
    if adopted:                                  # prereg-orbit-adopted §1: the body-context rule, adopted route only
        census = fictional_census(db_root)
        fictional = body["fictional"] if "fictional" in body else body["name"] in census
        run_body = dict(body, fictional=fictional)
        records["phase4 fictional census"] = rid.entry_sha256(sorted(census))
    else:
        fictional = body.get("fictional") is True   # the measured route reads only an explicit flag (M5c guards data)
    if fictional:
        return rf.make("node.fiction_in_measured_db", where, file=r["file"], key=ekey), None
    run = rid.run_id(spec, upstream={}, records=records, body=run_body)
    src = SourceRef(kind="record", ref={"file": r["file"], "key": ekey, "sha256": records[ekey]},
                    cites=entry.get("bibcode") or entry.get("doi"))
    grade, how_read = ("authored", "chosen") if adopted else ("measured", "read")
    quantities, notes = [], []
    if adopted:
        notes.append(Note(kind="stability_adopted",
                          text=f"{ekey} (method {method}) is adopted in place of an observation; read as authored",
                          fields={"record": ekey, "method": method}))
    for out_key, how in r["outputs"].items():
        out = spec["outputs"][out_key]
        if entry.get(how["value"]) is None:
            continue
        f = float(how["to_si"])
        point = float(entry[how["value"]]) * f
        u = entry.get(how["uncertainty"]) if how.get("uncertainty") else None
        if u is not None:
            u = float(u) * f
            band = Band(lo=point - u, hi=point + u, method="catalogue uncertainty as printed",
                        sources=Sources(input=SourceBand(-u, u, "catalogue uncertainty as printed"), model=None,
                                        solver=None, model_reason="a measurement: no model",
                                        solver_reason="a measurement: no solver"))
            reason = None
        else:
            band, reason = None, "the recommended record prints no uncertainty"
        for j, other in enumerate(block):
            if j == i or other.get(how["value"]) is None or other.get("method") not in r["methods"]:
                continue
            v = float(other[how["value"]]) * f
            if adopted:                          # shown, not graded (owner 00:25)
                ou = other.get(how["uncertainty"]) if how.get("uncertainty") else None
                lo = hi = inside = None
                if ou is not None:
                    lo, hi = v - float(ou) * f, v + float(ou) * f
                    inside = lo <= point <= hi
                notes.append(Note(kind="adopted_vs_observed",
                                  text=f"{out_key}: adopted {point!r} vs observed {key}[{j}] = {v!r}; inside {inside}",
                                  fields={"output": out_key, "observed_record": f"{key}[{j}]", "observed_value": v,
                                          "lo": lo, "hi": hi, "inside": inside}))
            elif band is not None and not band.lo <= v <= band.hi:
                notes.append(Note(kind="measurement_spread",
                                  text=f"{out_key}: {key}[{j}] = {v!r} lies outside the recommended band",
                                  fields={"output": out_key, "record": f"{key}[{j}]", "value": v,
                                          "reference": other.get("reference") or other.get("source")}))
        quantities.append(Quantity(
            key=f"{node}.{out_key}", unit=out["unit"], point=point, kind=out["kind"], method=how_read,
            where=Where("body"), band=band, band_reason=reason,
            provenance=NodeProvenance(grade=grade, solver=SolverInfo(solve_id=run), sources=(src,))))
    if not quantities:
        return rf.make("node.input_missing", where, input=",".join(r["outputs"]), **{"from": f"{r['file']}:{ekey}"}), run
    return Answer(quantities=tuple(quantities), notes=tuple(notes)), run


def fictional_census(db_root=None) -> frozenset:
    """Bodies a phase4 identity row marks `fictional: true` (contract note 1 A0: the only typed marker today)."""
    root = Path(db_root or REPO)
    k = ("census", root)
    if k not in _CACHE:
        import yaml                              # legacy boards carry duplicate keys the strict project loader refuses;
        names = set()                            # read them as scripts/check_pipeline_flow.py does (safe_load)
        for p in sorted((root / "phase4").glob("*.yaml")):
            data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
            for row in data.get("decisions") or ():
                if row.get("fictional") is True:
                    names.add(row.get("body"))
        _CACHE[k] = frozenset(names)
    return _CACHE[k]


def _owner(spec, body, block, key, where):
    r = spec["reads"]
    node = spec["id"]
    records = {key: rid.entry_sha256(block)}
    run = rid.run_id(spec, upstream={}, records=records, body=body)
    src = SourceRef(kind="user_declared", ref=block["decision"])
    quantities = []
    for out_key, how in r["outputs"].items():
        out = spec["outputs"][out_key]
        point = float(block[how["value"]]) * float(how["to_si"])
        quantities.append(Quantity(
            key=f"{node}.{out_key}", unit=out["unit"], point=point, kind=out["kind"], method="chosen",
            where=Where("body"), band=None, band_reason="an owner value: no band declared",
            provenance=NodeProvenance(grade="authored", solver=SolverInfo(solve_id=run), sources=(src,))))
    return Answer(quantities=tuple(quantities)), run
