# 방법론 문서의 계약 블록을 코드와 대조한다 — 문서가 읽히기만 하지 않고 검사받게
"""Check each recipe's documented contract against what the code actually does.

    python3 engine/check_contracts.py

문서에 `Returns` / `Needs` 를 적는 것만으로는 부족하다. 적어놓고 코드가 달라지면
문서가 조용히 거짓말이 된다 — 손으로 친 표가 54배 어긋났던 것과 같은 병이다.

`payload.Result` 는 레시피가 무엇을 먹었고 무엇을 냈는지 이미 들고 있다. 그래서
문서의 선언과 실행 결과를 맞춰볼 수 있고, 어긋나면 실패한다. 계약 블록이 서명이
되려면 이 검사가 있어야 한다.

계약 블록 형식 (방법론 문서 안)
--------------------------------
    ## Contract — `<노드 이름>`

    **Returns** — `a` [단위] · `b` [단위]
    **Needs** — `x` [단위] · `y` [단위]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

import graph
import registry
from state import BodyState, Missing

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent / "docs" / "reference"
BODIES = HERE / "bodies"

FIELD = re.compile(r"`([a-z0-9_]+)`")
# 항목이 많으면 줄이 넘어간다. 다음 **항목** 이나 빈 줄까지 이어 읽는다 —
# 문서를 한 줄에 욱여넣게 만들면 읽기 나빠지고, 그건 이 작업의 목적에 반한다.
LINE = re.compile(r"^\*\*(Returns|Needs)\*\*\s*[—-]\s*(.+?)(?=\n\s*\n|\n\*\*|\Z)",
                  re.M | re.S)


def parse_contract(doc: Path, node: str) -> dict[str, set[str]] | None:
    """문서에서 그 노드의 계약 블록을 뽑는다. 없으면 None."""
    text = doc.read_text(encoding="utf-8")
    head = re.search(rf"^##\s*Contract\s*[—-]\s*`{re.escape(node)}`\s*$", text, re.M)
    if not head:
        return None
    rest = text[head.end():]
    nxt = re.search(r"^##\s", rest, re.M)
    block = rest[:nxt.start()] if nxt else rest
    out: dict[str, set[str]] = {}
    for kind, body in LINE.findall(block):
        out[kind.lower()] = set(FIELD.findall(body))
    return out


def sample_bodies() -> list[BodyState]:
    """계약을 확인할 표본들.

    하나로는 부족하다. 레시피는 도메인 밖에서 값을 내지 않으므로, 거절하는
    천체만 보면 Returns 를 확인할 수 없다 — 거대행성 하나만 두었더니 암석
    레시피의 출력을 못 봤다. 천체를 훑어 그 레시피가 실제로 값을 내는 것을 쓴다.
    """
    out = []
    for path in sorted(BODIES.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        out.append(BodyState(name=doc["name"], kind=doc["kind"], parent=doc.get("parent"),
                             inputs=doc.get("inputs") or {}, units=doc.get("units") or {}))
    return out


def main() -> int:
    registry.load_all()
    g = graph.load()
    bodies = sample_bodies()
    fails: list[str] = []
    checked = 0

    for node in sorted(registry.registered()):
        nd = g["nodes"][node]
        slug = nd.get("recipe")
        if not slug:
            fails.append(f"{node}: chain.yaml 에 recipe 문서가 없다")
            continue
        doc = DOCS / f"{slug}.md"
        if not doc.exists():
            fails.append(f"{node}: 문서 {doc.name} 가 없다")
            continue
        declared = parse_contract(doc, node)
        if declared is None:
            fails.append(f"{node}: {doc.name} 에 '## Contract — `{node}`' 블록이 없다")
            continue

        fn = registry.get(node)
        res = None
        for body in bodies:
            try:
                candidate = fn(body)
            except Missing:
                continue
            res = res or candidate
            if candidate.applicable:
                res = candidate
                break
        if res is None:
            print(f"  [건너뜀] {node}: 어느 표본 천체도 입력을 갖추지 못했다")
            continue
        if not res.applicable:
            print(f"  [건너뜀] {node}: 표본 천체가 전부 도메인 밖이다 "
                  f"— Returns 를 확인할 수 없다")
            continue
        actual_in = set(res.inputs)
        actual_out = set(res.values)
        checked += 1

        for label, want, got in (("Needs", declared.get("needs", set()), actual_in),
                                 ("Returns", declared.get("returns", set()), actual_out)):
            if want - got:
                fails.append(f"{node}: 문서가 {label} 에 적었는데 코드가 안 쓴다 — "
                             f"{', '.join(sorted(want - got))}")
            if got - want:
                fails.append(f"{node}: 코드가 쓰는데 문서 {label} 에 없다 — "
                             f"{', '.join(sorted(got - want))}")

        # 선언된 출력에는 전부 단위가 붙어야 한다. 무차원이면 그렇게 적어야 한다.
        for name in sorted(actual_out):
            if name not in res.units:
                fails.append(f"{node}: 출력 '{name}' 에 단위가 없다")

    total = sum(1 for d in g["nodes"].values() if d.get("kind") == "computed")
    for f in fails:
        print(f"  [FAIL] {f}")
    if not fails:
        print(f"  [PASS] 계약 대조 {checked}건 — 문서와 코드가 일치 "
              f"(레시피 {len(registry.registered())} / 계산 노드 {total})")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
