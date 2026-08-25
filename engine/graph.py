# 그래프를 읽고 순서·순환을 계산한다 — 검증기와 러너가 같은 규칙을 쓰게 하는 단일 지점
"""Ordering and cycle rules over chain.yaml, shared by the validator and the runner.

두 벌로 두면 어긋난다. 실제로 어긋나 있었다 — `chain.py` 는 순환을 `requires`
로만 찾았고, 그래서 `selects` 를 지나는 고리를 못 봤다. 러너를 만들자 위상정렬이
막히면서 드러났고, 진짜 모양은 선언된 여섯 개가 아니라 **15노드짜리 덩어리
하나**였다.

세 가지 규칙이 여기 있다.

* **순환은 `requires` 와 `selects` 를 함께 따라간다.** selects 는 어느 모델을
  쓸지를 고르는 엣지이고, 고른 결과가 돌아와 그 선택을 바꾼다면 그것도 고정점을
  돌려야 하는 진짜 순환이다.
* **`scope != self` 는 뺀다.** 다른 천체를 거쳐가므로 한 천체 안의 순서가 아니다.
* **클래스 표는 뺀다.** 조회는 순서를 요구하지 않는다 — 키만 있으면 즉시 나온다.
  계산 단계로 세면 없는 고리가 생긴다.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

CHAIN = Path(__file__).resolve().parent / "chain.yaml"
ORDERING_KINDS = ("requires", "selects")


def load() -> dict:
    return yaml.safe_load(CHAIN.read_text(encoding="utf-8"))


def tables(g: dict) -> set[str]:
    return {n for n, d in g["nodes"].items() if d.get("kind") == "class_table"}


def adjacency(g: dict) -> dict[str, list[str]]:
    skip = tables(g)
    adj: dict[str, list[str]] = defaultdict(list)
    for e in g["edges"]:
        if e["kind"] not in ORDERING_KINDS or e.get("scope", "self") != "self":
            continue
        if e["from"] in skip or e["to"] in skip:
            continue
        if e["from"] in g["nodes"] and e["to"] in g["nodes"]:
            adj[e["from"]].append(e["to"])
    return adj


def components(g: dict) -> list[list[str]]:
    """실제 순환군. 원소가 둘 이상인 강결합 성분만 돌려준다 (Tarjan)."""
    adj = adjacency(g)
    idx: dict[str, int] = {}
    low: dict[str, int] = {}
    on: set[str] = set()
    stack: list[str] = []
    out: list[list[str]] = []
    counter = [0]
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 10_000))

    def strong(v: str) -> None:
        idx[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on.add(v)
        for w in adj[v]:
            if w not in idx:
                strong(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            comp = []
            while True:
                w = stack.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            if len(comp) > 1:
                out.append(sorted(comp))

    for n in g["nodes"]:
        if n not in idx:
            strong(n)
    return out


def declared_core(g: dict) -> set[str]:
    return set((g.get("coupled_core") or {}).get("members") or [])


def undeclared(g: dict) -> list[list[str]]:
    """선언되지 않은 순환군. 비어 있어야 한다."""
    core = declared_core(g)
    return [c for c in components(g) if not set(c) <= core]


def order(g: dict) -> list[list[str]]:
    """실행 단위. 원소가 둘 이상이면 그 덩어리는 반복해서 푼다.

    클래스 표는 순서를 만들지 않으므로 계산이 끝난 뒤 아무 때나 조회하면 된다.
    여기서는 단위 목록에 넣되 의존은 걸지 않는다.
    """
    comps = components(g)
    of_group = {n: i for i, c in enumerate(comps) for n in c}

    def key(n: str) -> str:
        return f"#{of_group[n]}" if n in of_group else n

    skip = tables(g)
    deps: dict[str, set[str]] = defaultdict(set)
    units = {key(n) for n in g["nodes"] if n not in skip}
    for e in g["edges"]:
        if e["kind"] not in ORDERING_KINDS or e.get("scope", "self") != "self":
            continue
        if e["from"] in skip or e["to"] in skip:
            continue
        a, b = key(e["from"]), key(e["to"])
        if a != b:
            deps[b].add(a)

    out: list[list[str]] = []
    done: set[str] = set()
    while len(done) < len(units):
        ready = sorted(u for u in units if u not in done and deps[u] <= done)
        if not ready:
            raise SystemExit(
                "위상정렬이 막혔다 — 선언되지 않은 순환이 있다: "
                f"{sorted(units - done)[:6]}")
        for u in ready:
            out.append(comps[int(u[1:])] if u.startswith("#") else [u])
            done.add(u)
    out.append(sorted(skip))          # 조회표는 순서와 무관하다
    return out
