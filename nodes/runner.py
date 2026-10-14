# 노드 실행기 — 천체 맥락에서 그래프 순서로 노드를 돌리고, 선언된 입력만 읽게 막고(F4), 결과마다 run id 를 붙인다 (계약 §3·§6·§8)
"""Run node specs over one body (contract `node-contract.frozen.md`).

A body context is `{name, kind, hosts, parent, companions}` (`companions`: other stars of the system, named in a
`companion_hosts_not_combined` note by nodes with host inputs, not summed; prereg §1). A node with a `scope: host` input runs its producer on every host
body and receives a list. `Runner.result(node, body)` returns `(outcome, run_id)`, memoised; the outcome is a
`solver.result.Answer` or `Refusal`.

Two kinds of node implementation:
- measured and owner nodes are generic: `nodes/records.py` reads their `reads` block;
- computed nodes are a module `nodes/<id>.py` with `compute(ctx) -> (values, notes)`, where `ctx.read(name)` is the
  only way to get an input and refuses a name the spec does not declare (`node.undeclared_read`, prereg N7).
"""
from __future__ import annotations

import importlib

from solver import refusals as rf
from solver.result import Answer, Band, Note, Quantity, SolverInfo, Sources, SourceBand, Where, GRADES

from nodes import graph, records, run_id as rid, spec as sp
from nodes.types import NodeProvenance, RESULT_TO_INPUT_GRADE, SourceRef, CONTRACT_NOTE_KINDS


class UndeclaredRead(Exception):
    def __init__(self, key):
        super().__init__(key)
        self.key = key


class Context:
    """What a computed node sees: its declared inputs, nothing else."""

    def __init__(self, spec, inputs):
        self.spec, self._inputs, self.read_log = spec, inputs, []

    def read(self, name):
        if name not in (self.spec.get("inputs") or {}):
            raise UndeclaredRead(name)
        self.read_log.append(name)
        return self._inputs[name]


def worst(grades) -> str:
    return GRADES[max(GRADES.index(g) for g in grades)]


def body_key(body: dict) -> str:
    return f"{body['kind']}:{body['name']}"


class Runner:
    def __init__(self, specs: dict | None = None, db_root=None):
        self.specs = specs if specs is not None else sp.load_all()
        graph.check(self.specs)
        self.db_root = db_root
        self._memo = {}

    def result(self, node: str, body: dict):
        k = (node, body_key(body))
        if k not in self._memo:
            self._memo[k] = self._run(node, body)
        return self._memo[k]

    # ── one run ────────────────────────────────────────────────────────
    def _run(self, node, body):
        spec = self.specs[node]
        where = f"{node}@{body['name']}"
        if body["kind"] not in spec["applies_to"] and "any" not in spec["applies_to"]:
            return rf.make("node.out_of_domain", where, input="body.kind", value=body["kind"],
                           bound=list(spec["applies_to"]), bound_kind="applies_to"), None
        if spec["kind"] in ("measured", "owner"):
            return records.run(spec, body, where, self.db_root)
        return self._run_computed(spec, body, where)

    def _resolve_input(self, inp, body):
        node, _, key = inp["from"].partition(".")
        if inp["scope"] == "self":
            targets = [body]
        elif inp["scope"] == "host":
            targets = [{"name": h, "kind": "star", "hosts": [], "parent": None} for h in body.get("hosts", [])]
        elif inp["scope"] == "parent":
            targets = [body["parent"]] if body.get("parent") else []
        else:
            raise NotImplementedError("scope system is not used by any node yet")
        got = []
        for t in targets:
            out, run = self.result(node, t)
            q = None
            if isinstance(out, Answer):
                q = next((x for x in out.quantities if x.key == f"{node}.{key}"), None)
            got.append((q, run))
        return got

    def _run_computed(self, spec, body, where):
        node = spec["id"]
        inputs, upstream, read_grades = {}, {}, []
        for name, inp in (spec.get("inputs") or {}).items():
            got = self._resolve_input(inp, body)
            if not got or any(q is None for q, _ in got):
                if inp.get("required", True):
                    return rf.make("node.input_missing", where, input=name, **{"from": inp["from"]}), None
                continue
            upstream[name] = [r for _, r in got]
            inputs[name] = [q for q, _ in got] if inp["scope"] == "host" else got[0][0]
            for q, _ in got:
                read_grades.append((inp["from"], q.provenance.grade))
        for b in spec.get("domain") or []:
            if b["input"] not in inputs:
                continue
            vals = inputs[b["input"]]
            for q in (vals if isinstance(vals, list) else [vals]):
                for op, test in (("ge", lambda v, x: v >= x), ("gt", lambda v, x: v > x),
                                 ("le", lambda v, x: v <= x), ("lt", lambda v, x: v < x)):
                    if op in b and not test(q.point, b[op]):
                        return rf.make(b["refusal"], where, input=b["input"], value=q.point, bound=b[op],
                                       bound_kind=op), None
        run = rid.run_id(spec, upstream=upstream, records={}, body=body)
        mod = importlib.import_module(f"nodes.{node}")
        ctx = Context(spec, inputs)
        try:
            values, notes = mod.compute(ctx)
        except UndeclaredRead as e:
            return rf.make("node.undeclared_read", where, key=e.key), run
        sources = tuple(_source_ref(s) for s in spec["sources"] if "to_fetch" not in s)
        quantities = []
        for key, (point, lo, hi) in values.items():
            out = spec["outputs"][key]
            grade = worst([g for _, g in read_grades] + [out["method_grade"]])
            band, reason = _band(point, lo, hi, "inputs' printed bands propagated through the closed form")
            quantities.append(Quantity(
                key=f"{node}.{key}", unit=out["unit"], point=point, kind=out["kind"], method="derived",
                where=Where("body"), band=band, band_reason=reason,
                provenance=NodeProvenance(
                    grade=grade, solver=SolverInfo(solve_id=run),
                    inputs_read=tuple((f, RESULT_TO_INPUT_GRADE[g]) for f, g in read_grades),
                    sources=sources,
                    counter_evidence_searched=tuple(out.get("counter_evidence_searched") or ()))))
        notes = list(notes)
        has_host = any(i["scope"] == "host" for i in (spec.get("inputs") or {}).values())
        if has_host and body.get("companions"):
            notes.append(Note(kind="companion_hosts_not_combined",
                              text=f"other stars in the system are not summed: {', '.join(body['companions'])}",
                              fields={"hosts": tuple(body.get("hosts", [])), "companions": tuple(body["companions"])}))
        for n in notes:
            if n.kind not in spec["note_kinds"] and n.kind not in CONTRACT_NOTE_KINDS:
                raise ValueError(f"{node}: undeclared note kind {n.kind!r}")
        return Answer(quantities=tuple(quantities), notes=tuple(notes)), run


def _source_ref(s: dict) -> SourceRef:
    for kind in ("cache", "library", "doi", "formula", "user_declared"):
        if kind in s:
            return SourceRef(kind=kind, ref=s[kind], page=s.get("page"), where=s.get("where"),
                             sha256=s.get("sha256"), cites=s.get("cites"), identity=bool(s.get("identity")))
    raise ValueError(f"source entry {s!r} names no kind")


def _band(point, lo, hi, contrib):
    """A Band from absolute input-propagated limits, or (None, reason) when no input carried a band."""
    if lo is None or hi is None or (lo == point == hi):
        return None, "no input carried a printed band"
    return Band(lo=lo, hi=hi, method="corner evaluation over the inputs' printed bands",
                sources=Sources(input=SourceBand(lo - point, hi - point, contrib), model=None, solver=None,
                                model_reason="exact identity: no model scatter",
                                solver_reason="closed form: no numerical error")), None
