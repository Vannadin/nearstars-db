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

import graph

CHAIN = Path(__file__).resolve().parent / "chain.yaml"


def load() -> dict:
    return yaml.safe_load(CHAIN.read_text(encoding="utf-8"))


_BANNER_TO_LAYER = {"클래스 표 상수 — 도출값이 아니라 조회값": "클래스 표 상수"}


def _banner_layers() -> dict[str, str]:
    """노드 이름 → 그 노드 위의 배너(층). YAML 은 주석을 버리므로 파일을 줄 단위로 읽는다."""
    import re
    out: dict[str, str] = {}
    banner = None
    in_nodes = False
    for line in CHAIN.read_text(encoding="utf-8").split("\n"):
        if line.startswith("nodes:"):
            in_nodes = True
        elif line.startswith("edges:"):
            break
        m = re.match(r"  # ── (.+?) ─", line)
        if in_nodes and m:
            b = m.group(1).strip()
            banner = _BANNER_TO_LAYER.get(b, b)
        m = re.match(r"  ([a-z_0-9]+):", line)
        if in_nodes and m and banner:
            out[m.group(1)] = banner
    return out


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

    # 브리프 61 — 노드 축 둘. 모든 노드가 layer 와 domain 을 선언하고, 값은 헤더 목록 안이며,
    # layer 는 노드가 놓인 배너와 같아야 한다 (주석과 필드가 어긋나면 주석은 거짓이 된다).
    layers, domains = set(g.get("layers", [])), set(g.get("domains", []))
    for name, n in nodes.items():
        for axis, allowed in (("layer", layers), ("domain", domains)):
            if axis not in n:
                errors.append(f"node {name}: {axis} 가 없다")
            elif n[axis] not in allowed:
                errors.append(f"node {name}: {axis} '{n[axis]}' 가 {sorted(allowed)} 밖")
    for name, banner in _banner_layers().items():
        if name in nodes and nodes[name].get("layer") != banner:
            errors.append(f"node {name}: layer '{nodes[name].get('layer')}' 가 배너 '{banner}' 와 다르다")

    declared = {m for c in g.get("cycles", []) for m in c["members"]}
    for c in g.get("cycles", []):
        for m in c["members"]:
            if m not in nodes:
                errors.append(f"cycle {c['id']}: '{m}' 는 nodes 에 없다")

    # 순환은 requires 와 selects 를 함께 따라가야 보인다. 예전에는 requires 만
    # 봤고, 그래서 selects 를 지나는 고리를 하나도 못 잡았다 — 러너를 만들자
    # 위상정렬이 막히면서 드러났다. 실제 모양은 선언된 여섯 개가 아니라
    # 15노드짜리 덩어리 하나였다. 규칙은 graph.py 에만 둔다.
    for comp in graph.undeclared(g):
        errors.append("선언되지 않은 순환군: " + ", ".join(comp))

    core = graph.declared_core(g)
    real = {n for c in graph.components(g) for n in c}
    antic = (g.get("coupled_core") or {}).get("anticipated") or []
    for n in sorted(core - real):
        if n not in antic:
            warnings.append(f"coupled_core '{n}' 는 실제 순환 안에 없다 "
                            "(엣지가 아직 gap 이면 anticipated 로 옮길 것)")

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
              f"(selects {n_sel}, influences {n_inf}) · 순환군 {len(graph.components(g))} "
              f"(코어 {len(graph.declared_core(g))}노드, 이름 붙인 부분 고리 {len(g.get('cycles', []))})")
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
        first = ((d.get("note") or "").strip().splitlines() or [""])[0]
        print(f"  [{d['status']}] {n}{' — ' + first if first else ''}")
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
