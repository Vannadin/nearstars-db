# chain.yaml 검증기 + 질의 도구 — 엣지 무결성 확인과 "X 를 바꾸면 뭘 다시 봐야 하나"
"""Validate engine/chain.yaml and answer cascade questions against it.

    python3 engine/chain.py check          그래프 무결성 검사
    python3 engine/chain.py affects <노드>  X 가 바뀌면 다시 봐야 할 것 전부
    python3 engine/chain.py needs <노드>    X 를 계산하려면 먼저 있어야 할 것 전부
    python3 engine/chain.py gaps           빠진 노드·엣지만

`affects` 는 requires 와 influences 를 모두 따라간다. cascade 를 기억으로
추적하던 자리를 대신하는 것이 이 명령의 목적이다.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

CHAIN = Path(__file__).resolve().parent / "chain.yaml"


def load() -> dict:
    return yaml.safe_load(CHAIN.read_text(encoding="utf-8"))


def check(g: dict) -> int:
    nodes, edges = g["nodes"], g["edges"]
    kinds = set(g["kinds"])
    errors: list[str] = []
    warnings: list[str] = []

    for i, e in enumerate(edges):
        where = f"edge[{i}] {e.get('from')} -> {e.get('to')}"
        for end in ("from", "to"):
            if e.get(end) not in nodes:
                errors.append(f"{where}: '{e.get(end)}' 는 nodes 에 없다")
        if e.get("kind") not in kinds:
            errors.append(f"{where}: kind '{e.get('kind')}' 가 {sorted(kinds)} 밖")
        # selects 와 influences 는 근거 없이 존재할 수 없다. 교과서 관계식과
        # 아직 문서화되지 않은 gap 만 예외이고, 둘 다 명시적으로 표시해야 한다.
        if e.get("kind") in ("selects", "influences") and not e.get("ref"):
            if not e.get("textbook") and e.get("status") != "gap":
                errors.append(f"{where}: {e['kind']} 엣지에 ref 가 없다")

    declared = {m for c in g.get("cycles", []) for m in c["members"]}
    for c in g.get("cycles", []):
        for m in c["members"]:
            if m not in nodes:
                errors.append(f"cycle {c['id']}: '{m}' 는 nodes 에 없다")

    # requires 만으로 이루어진 순환은 선언돼 있어야 한다.
    req: dict[str, set[str]] = {n: set() for n in nodes}
    for e in edges:
        if e.get("kind") == "requires" and e["from"] in nodes and e["to"] in nodes:
            req[e["to"]].add(e["from"])

    seen: set[str] = set()
    stack: list[str] = []

    def walk(n: str) -> None:
        if n in stack:
            loop = stack[stack.index(n):] + [n]
            if not set(loop) <= declared:
                errors.append("선언되지 않은 requires 순환: " + " -> ".join(loop))
            return
        if n in seen:
            return
        seen.add(n)
        stack.append(n)
        for p in req[n]:
            walk(p)
        stack.pop()

    for n in nodes:
        walk(n)

    for name, nd in nodes.items():
        if nd.get("kind") == "computed" and not nd.get("recipe"):
            if nd.get("status") not in ("missing", "gap"):
                warnings.append(f"node '{name}': computed 인데 recipe 가 없다")

    for w in warnings:
        print(f"  [WARN] {w}")
    for x in errors:
        print(f"  [FAIL] {x}")
    if not errors:
        n_sel = sum(1 for e in edges if e["kind"] == "selects")
        n_inf = sum(1 for e in edges if e["kind"] == "influences")
        print(f"  [PASS] 노드 {len(nodes)} · 엣지 {len(edges)} "
              f"(selects {n_sel}, influences {n_inf}) · 순환 {len(g.get('cycles', []))} 선언됨")
    return 1 if errors else 0


def _adj(g: dict, forward: bool, kinds: set[str]) -> dict[str, list[tuple[str, str]]]:
    out: dict[str, list[tuple[str, str]]] = {n: [] for n in g["nodes"]}
    for e in g["edges"]:
        if e["kind"] not in kinds:
            continue
        a, b = (e["from"], e["to"]) if forward else (e["to"], e["from"])
        if a in out:
            out[a].append((b, e["kind"]))
    return out


def _reach(adj, start: str) -> list[tuple[str, int, str]]:
    seen = {start}
    frontier = [(start, 0, "")]
    order: list[tuple[str, int, str]] = []
    while frontier:
        node, depth, kind = frontier.pop(0)
        if depth:
            order.append((node, depth, kind))
        for nxt, k in adj.get(node, []):
            if nxt not in seen:
                seen.add(nxt)
                frontier.append((nxt, depth + 1, k))
    return order


def affects(g: dict, start: str) -> int:
    if start not in g["nodes"]:
        print(f"'{start}' 는 nodes 에 없다"); return 2
    adj = _adj(g, True, {"requires", "influences", "selects"})
    hits = _reach(adj, start)
    print(f"{start} 가 바뀌면 다시 봐야 할 것 {len(hits)}개\n")
    for n, d, k in hits:
        print(f"  {'  ' * (d - 1)}└ {n}  ({k})")
    return 0


def needs(g: dict, start: str) -> int:
    if start not in g["nodes"]:
        print(f"'{start}' 는 nodes 에 없다"); return 2
    adj = _adj(g, False, {"requires", "selects"})
    hits = _reach(adj, start)
    print(f"{start} 를 계산하려면 먼저 있어야 할 것 {len(hits)}개\n")
    for n, d, k in hits:
        nd = g["nodes"][n]
        flag = f"  ⚠ {nd['status']}" if nd.get("status") else ""
        print(f"  {'  ' * (d - 1)}└ {n}  ({k}){flag}")
    return 0


def gaps(g: dict) -> int:
    ns = [(n, d) for n, d in g["nodes"].items() if d.get("status")]
    es = [e for e in g["edges"] if e.get("status")]
    print(f"빠진 노드 {len(ns)}개")
    for n, d in ns:
        print(f"  [{d['status']}] {n} — {(d.get('note') or '').strip().splitlines()[0]}")
    print(f"\n빠진 엣지 {len(es)}개")
    for e in es:
        print(f"  [{e['status']}] {e['from']} -> {e['to']} ({e['kind']})")
    return 0


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    g = load()
    cmd = args[0]
    if cmd == "check":
        sys.exit(check(g))
    if cmd in ("affects", "needs") and len(args) == 2:
        sys.exit(affects(g, args[1]) if cmd == "affects" else needs(g, args[1]))
    if cmd == "gaps":
        sys.exit(gaps(g))
    print(__doc__)
    sys.exit(2)


if __name__ == "__main__":
    main()
