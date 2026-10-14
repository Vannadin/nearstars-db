# 노드 명세 로더 — schema.yaml 의 닫힌 키로 명세를 읽고, 모르는 키·빠진 키·계약 위반을 이름 대며 멈춘다 (계약 §2·§4.3).
"""Load and check a node spec against `nodes/schema.yaml` (contract `rewrite/nodes/node-contract.frozen.md` §2).

A spec that breaks a rule does not load: `SpecError(kind, detail, path)` names the rule. Kinds:
- `spec.unknown_key`, `spec.missing_key`, `spec.bad_value`: the closed schema (F12);
- `spec.id_mismatch`: `id` differs from the file stem;
- `spec.counter_evidence_missing`: a computed node's output with `method_grade: authored` and no
  `counter_evidence_searched` (§4.3; the owner route is exempt);
- `spec.host_combine_missing`: an input with `scope: host` and no `host_combine` for some output (§2, D-7);
- `spec.reads_missing` / `spec.methods_missing`: a measured or owner node without `reads`, a measured one without
  its closed `methods` list (§4.2, prereg N13);
- `spec.unknown_quantity`: an output's `quantity` not in `nodes/quantities.yaml`, or a unit differing from it;
- `spec.refusal_unregistered`: a refusal id not in the solver's one registry;
- `spec.checks_missing`: no hand check for an output, no negative control for a declared refusal (§7).
"""
from __future__ import annotations

from pathlib import Path

from solver import yamlio

HERE = Path(__file__).resolve().parent
_SCHEMA = None
_QUANTITIES = None


class SpecError(Exception):
    def __init__(self, kind: str, detail: str, path: str = ""):
        super().__init__(f"{kind}: {detail}" + (f" ({path})" if path else ""))
        self.kind, self.detail, self.path = kind, detail, path


def schema() -> dict:
    global _SCHEMA
    if _SCHEMA is None:
        _SCHEMA = yamlio.load_data(HERE / "schema.yaml")
    return _SCHEMA


def quantities() -> dict:
    global _QUANTITIES
    if _QUANTITIES is None:
        _QUANTITIES = yamlio.load_data(HERE / "quantities.yaml")["quantities"]
    return _QUANTITIES


def _check_record(obj, rec_name: str, path: str) -> None:
    sch = schema()[rec_name]
    if not isinstance(obj, dict):
        raise SpecError("spec.bad_value", f"expected a mapping for {rec_name}", path)
    for k in obj:
        if k not in sch:
            raise SpecError("spec.unknown_key", f"'{k}' is not a {rec_name} key", f"{path}.{k}")
    for k, rule in sch.items():
        if rule.get("required") and k not in obj:
            raise SpecError("spec.missing_key", f"'{k}' is required in {rec_name}", path)
        if k in obj:
            _check_value(obj[k], rule, f"{path}.{k}")


def _check_value(v, rule: dict, path: str) -> None:
    shape = rule["shape"]
    if shape == "any":
        return
    if shape == "text" and not isinstance(v, str):
        raise SpecError("spec.bad_value", "expected text", path)
    if shape == "bool" and not isinstance(v, bool):
        raise SpecError("spec.bad_value", "expected true/false", path)
    if shape == "enum" and v not in rule["values"]:
        raise SpecError("spec.bad_value", f"{v!r} not in {list(rule['values'])}", path)
    if shape == "list":
        if not isinstance(v, (list, tuple)):
            raise SpecError("spec.bad_value", "expected a list", path)
        for i, item in enumerate(v):
            if "values" in rule and item not in rule["values"]:
                raise SpecError("spec.bad_value", f"{item!r} not in {list(rule['values'])}", f"{path}[{i}]")
            if "of" in rule:
                _check_record(item, rule["of"], f"{path}[{i}]")
    if shape == "mapping":
        if not isinstance(v, dict):
            raise SpecError("spec.bad_value", "expected a mapping", path)
        if "of" in rule:
            for k, item in v.items():
                _check_record(item, rule["of"], f"{path}.{k}")
    if shape == "record":
        _check_record(v, rule["of"], path)


def check(spec: dict, stem: str | None = None) -> dict:
    """Check one parsed spec; return it unchanged or raise `SpecError`."""
    _check_record(spec, "top", spec.get("id", "?") if isinstance(spec, dict) else "?")
    sid = spec["id"]
    if stem is not None and stem != sid:
        raise SpecError("spec.id_mismatch", f"id {sid!r} in file {stem!r}", sid)
    q = quantities()
    for key, out in spec["outputs"].items():
        p = f"{sid}.outputs.{key}"
        if out["quantity"] not in q:
            raise SpecError("spec.unknown_quantity", f"{out['quantity']!r} is not in quantities.yaml", p)
        if q[out["quantity"]]["unit"] != out["unit"]:
            raise SpecError("spec.unknown_quantity",
                            f"unit {out['unit']!r} differs from quantities.yaml {q[out['quantity']]['unit']!r}", p)
        if spec["kind"] == "computed" and out["method_grade"] == "authored" \
                and not out.get("counter_evidence_searched"):
            raise SpecError("spec.counter_evidence_missing",
                            "method_grade authored needs counter_evidence_searched (contract §4.3)", p)
    inputs = spec.get("inputs") or {}
    if any(i["scope"] == "host" for i in inputs.values()):
        hc = spec.get("host_combine") or {}
        missing = [k for k in spec["outputs"] if k not in hc]
        if missing:
            raise SpecError("spec.host_combine_missing", f"host inputs but no host_combine for {missing}", sid)
    if spec["kind"] in ("measured", "owner"):
        if inputs:
            raise SpecError("spec.bad_value", "a measured or owner node reads records, not other nodes", sid)
        if not spec.get("reads"):
            raise SpecError("spec.reads_missing", f"a {spec['kind']} node needs `reads`", sid)
        if spec["kind"] == "measured" and not spec["reads"].get("methods"):
            raise SpecError("spec.methods_missing", "a measured node needs its closed `methods` list (N13)", sid)
        overlap = set(spec["reads"].get("methods") or ()) & set(spec["reads"].get("adopted_methods") or ())
        if overlap:
            raise SpecError("spec.bad_value", f"adopted_methods overlaps methods: {sorted(overlap)}", sid)
    from solver import refusals as rf
    for rid in spec["refusals"]:
        if rid not in rf.REGISTRY:
            raise SpecError("spec.refusal_unregistered", f"{rid!r} is not in solver.refusals.REGISTRY", sid)
    checked = {h["output"] for h in spec["hand_checks"]}
    if spec["kind"] == "computed":
        missing = [k for k in spec["outputs"] if k not in checked]
        if missing:
            raise SpecError("spec.checks_missing", f"no hand check for {missing} (contract §7)", sid)
        identity_only = all(s.get("identity") for s in spec["sources"] if "formula" in s) and \
            all("formula" in s or "to_fetch" in s or "user_declared" in s for s in spec["sources"])
        if not identity_only and not spec["formula_checks"]:
            raise SpecError("spec.checks_missing", "a fitted or empirical law needs formula_checks (contract §7)", sid)
    controlled = {n["refusal"] for n in spec["negative_controls"]}
    missing = [r for r in spec["refusals"] if r not in controlled]
    if missing:
        raise SpecError("spec.checks_missing", f"no negative control for {missing} (contract §7)", sid)
    return spec


def load(path) -> dict:
    path = Path(path)
    try:
        data = yamlio.load_data(path)
    except yamlio.LoadError as e:
        raise SpecError("spec.unreadable", e.detail, str(path)) from None
    return check(_thaw(data), path.stem)


def load_all(directory=HERE) -> dict:
    """Every `*.yaml` spec in `directory` except schema.yaml and quantities.yaml, by id."""
    out = {}
    for p in sorted(Path(directory).glob("*.yaml")):
        if p.name in ("schema.yaml", "quantities.yaml"):
            continue
        s = load(p)
        out[s["id"]] = s
    return out


def _thaw(x):
    """yamlio returns read-only mappings; specs are plain dicts and lists."""
    if hasattr(x, "items"):
        return {k: _thaw(v) for k, v in x.items()}
    if isinstance(x, tuple):
        return [_thaw(v) for v in x]
    return x
