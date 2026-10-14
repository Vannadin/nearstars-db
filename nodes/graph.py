# 노드 그래프 — 명세의 입력·출력에서 간선을 만들고, 한쪽만 적힌 간선 · 물리량 중복 생산 · 단위 불일치 · 반복 없는 순환을 거절한다 (계약 §8)
"""Build the node graph from the specs (contract `node-contract.frozen.md` §8). Nothing is hand-kept.

Every edge must be declared at both ends: the consumer's `inputs.from` / `selects.from` and the producer's
`outputs.<key>.to`. `check(specs)` raises `GraphError(kind, detail)` on the first violation:
- `graph.no_such_output`: an input names a node or output that does not exist;
- `graph.one_ended`: a consumer reads an output whose producer does not list it in `to`, or a `to` names a node
  that does not read that output (F4);
- `graph.unit_mismatch`: an input's unit differs from the output's;
- `graph.duplicate_quantity`: two nodes produce one quantity for intersecting `applies_to` (F3);
- `graph.cycle_without_iterate`: a node on a cycle with no `iterate` (F5).
`order(specs)` gives a run order; `counts(specs)` the computed counts.
"""
from __future__ import annotations


class GraphError(Exception):
    def __init__(self, kind: str, detail: str):
        super().__init__(f"{kind}: {detail}")
        self.kind, self.detail = kind, detail


def edges(specs: dict) -> list:
    """(producer, output, consumer, kind) for every declared consumer end."""
    out = []
    for cid, s in specs.items():
        for _k, inp in (s.get("inputs") or {}).items():
            node, _, key = inp["from"].partition(".")
            out.append((node, key, cid, "requires"))
        for sel in s.get("selects") or []:
            node, _, key = sel["from"].partition(".")
            out.append((node, key, cid, "selects"))
    return out


def _intersects(a, b) -> bool:
    return "any" in a or "any" in b or bool(set(a) & set(b))


def check(specs: dict) -> None:
    consumer_ends = set()
    for cid, s in specs.items():
        for name, inp in (s.get("inputs") or {}).items():
            node, _, key = inp["from"].partition(".")
            if node not in specs or key not in specs[node]["outputs"]:
                raise GraphError("graph.no_such_output", f"{cid}.inputs.{name} reads {inp['from']}, which no spec emits")
            if specs[node]["outputs"][key]["unit"] != inp["unit"]:
                raise GraphError("graph.unit_mismatch", f"{cid}.inputs.{name} [{inp['unit']}] vs {inp['from']} "
                                                        f"[{specs[node]['outputs'][key]['unit']}]")
            consumer_ends.add((node, key, cid))
        for sel in s.get("selects") or []:
            node, _, key = sel["from"].partition(".")
            if node not in specs or key not in specs[node]["outputs"]:
                raise GraphError("graph.no_such_output", f"{cid}.selects reads {sel['from']}, which no spec emits")
            consumer_ends.add((node, key, cid))
    producer_ends = {(pid, key, c) for pid, s in specs.items() for key, o in s["outputs"].items() for c in o["to"]}
    for p, k, c in sorted(consumer_ends - producer_ends):
        raise GraphError("graph.one_ended", f"{c} reads {p}.{k}, but {p}.outputs.{k}.to does not list {c}")
    for p, k, c in sorted(producer_ends - consumer_ends):
        raise GraphError("graph.one_ended", f"{p}.outputs.{k}.to lists {c}, which does not read {p}.{k}")
    producers = []
    for pid, s in specs.items():
        for key, o in s["outputs"].items():
            producers.append((o["quantity"], pid, key, s["applies_to"]))
    for i, (q, pid, key, at) in enumerate(producers):
        for q2, pid2, key2, at2 in producers[i + 1:]:
            if q == q2 and pid != pid2 and _intersects(at, at2):
                raise GraphError("graph.duplicate_quantity",
                                 f"{pid}.{key} and {pid2}.{key2} both produce {q} for {sorted(set(at) | set(at2))}")
    for comp in cycles(specs):
        missing = [n for n in comp if not specs[n].get("iterate")]
        if missing:
            raise GraphError("graph.cycle_without_iterate", f"cycle {sorted(comp)}: no iterate on {sorted(missing)}")


def cycles(specs: dict) -> list:
    """Strongly-connected components with more than one node, or a self-loop (Tarjan)."""
    succ = {n: set() for n in specs}
    for p, _k, c, _kind in edges(specs):
        if p in succ:
            succ[p].add(c)
    index, low, stack, on, out, i = {}, {}, [], set(), [], [0]

    def visit(v):
        index[v] = low[v] = i[0]
        i[0] += 1
        stack.append(v)
        on.add(v)
        for w in sorted(succ[v]):
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            if len(comp) > 1 or v in succ[v]:
                out.append(comp)

    for v in sorted(specs):
        if v not in index:
            visit(v)
    return out


def order(specs: dict) -> list:
    """A run order: producers before consumers (nodes on a cycle are not ordered here; none exist yet)."""
    check(specs)
    deps = {n: {p for p, _k, c, _ in edges(specs) if c == n} for n in specs}
    done, out = set(), []
    while len(out) < len(specs):
        ready = sorted(n for n in specs if n not in done and deps[n] <= done)
        if not ready:
            raise GraphError("graph.cycle_without_iterate", f"cannot order {sorted(set(specs) - done)}")
        out.extend(ready)
        done.update(ready)
    return out


def counts(specs: dict) -> dict:
    sources = [s for sp in specs.values() for s in sp["sources"]]
    return {"nodes": len(specs), "edges": len(edges(specs)), "cycles": len(cycles(specs)),
            "to_fetch": sum(1 for s in sources if "to_fetch" in s),
            "user_declared": sum(1 for s in sources if "user_declared" in s)}
