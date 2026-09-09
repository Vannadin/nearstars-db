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

import ast
import re
import sys
from pathlib import Path

import yaml

import graph
import registry
from state import BodyState

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent / "docs" / "reference"
BODIES = HERE / "bodies"

#: C45 (b)/C50 의 클래스 ③ 기준선 — (노드 수, 고유 키 수). 2026-09-09 첫 측정.
#: ⚠ FAIL 이 아니다. 수리 뒤 0 이 되면 그때 FAIL 로 승격한다 (D 와 같은 경로).
CLASS3_BASELINE = (8, 8, 13)          # (노드, 고유 키, (노드,키) 쌍) — 발생은 13곳이다

#: 클래스 ① (C37 의 서명) 의 **알려진 기존 사례** — 2026-09-09 첫 측정, C50 에 등재.
#: ⚠ **이 집합 밖의 사례는 FAIL 이다.** 기존 넷을 지금 고치는 것은 값을 움직일 수 있어 다음
#: 브리프의 몫이고, 그때 이 집합에서 지운다. 집합을 늘리는 것은 병을 늘리는 것이다.
CLASS1_KNOWN = {
    ("body_class", "gas_mass_fraction"),
    ("body_class", "semi_major_axis_au"),
    ("dynamo_rocky", "dynamo_regime"),
    ("interior_layers", "porosity_cap"),
}

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


def ast_lookup_literals(node: str) -> set[str]:
    """레시피 소스에서 `state.get("…")` · `state.get_optional("…")` · `state["…"]` 의 리터럴 키.

    C45 (b) 의 백스톱: 표본 천체가 밟지 않는 분기의 조회는 런타임 로그에 남지 않는다. `state`
    라는 이름에 대한 접근만 센다 — 다른 객체의 `.get("x")` 까지 긁으면 소음이 된다."""
    fn = registry.get(node)
    if fn is None:
        return set()
    src = Path(sys.modules[fn.__module__].__file__).read_text(encoding="utf-8")
    keys: set[str] = set()
    for n in ast.walk(ast.parse(src)):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr in ("get", "get_optional")
                and isinstance(n.func.value, ast.Name) and n.func.value.id == "state"
                and n.args and isinstance(n.args[0], ast.Constant)
                and isinstance(n.args[0].value, str)):
            keys.add(n.args[0].value)
        if (isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name)
                and n.value.id == "state" and isinstance(n.slice, ast.Constant)
                and isinstance(n.slice.value, str)):
            keys.add(n.slice.value)
    return keys


def lookup_sets(node: str, bodies: list[BodyState]) -> dict[str, set[str]]:
    """이 노드가 **실제로** 조회한 키들을 표본 전체에서 모은다 (C45 (b)).

    `hit` 는 어느 표본에서든 값이 있었다는 뜻이고, `miss` 는 어느 표본에서도 없었다는 뜻이다.
    ⚠ 마지막에 다시 확인한다 — 초반 회차에서 못 찾고 나중 노드가 공급한 키는 미스가 아니다."""
    hit: set[str] = set()
    asked: set[str] = set()
    hard_asked: set[str] = set()          # get_optional / `in` 이 아닌 조회
    for body in bodies:
        for owner, key, kind in body.lookups:
            if owner != node:
                continue
            asked.add(key)
            if kind.endswith("hit"):
                hit.add(key)
            if kind == "miss":
                hard_asked.add(key)
    for body in bodies:                   # 회차 끝의 상태로 다시 판정
        for key in list(asked - hit):
            found, _ = body._find(key)
            if found:
                hit.add(key)
    return {"asked": asked, "hit": hit, "miss": asked - hit, "hard": hard_asked}


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
    import run
    for body in bodies:
        run.solve(body, g)
    fails: list[str] = []
    checked = 0
    #: C45 (b) 클래스 ③ — Needs 인데 로스터 어느 천체도 공급하지 않는 조회. **지금은 FAIL 이 아니다**:
    #: 계약이 틀렸는지 천체 선언이 빠졌는지가 아직 안 갈렸다(C50). 기준선보다 늘면 그 줄이 찍힌다.
    class3: dict[str, list[str]] = {}
    class1_seen: set[tuple[str, str]] = set()

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

        # ⚠ **두 `continue` 위에 있어야 한다** (B2, 2026-09-09): 조회 로그는 노드가 도메인
        # 밖이든 Result 를 못 내든 무관하게 쌓이는데, 아래의 `res is None` · `not res.applicable`
        # 조기 이탈 뒤에 두면 **조회 부재가 그 노드를 못 돌게 만드는 오타는 영원히 안 잡힌다.**
        # ── C45 (b): 문서 Needs · 실제 조회 · AST 리터럴, 세 집합 ────────────────────────
        look = lookup_sets(node, bodies)
        needs = declared.get("needs", set())
        literals = ast_lookup_literals(node)
        # ① C37 의 정확한 형태 — 조회가 어느 표본에서도 미스인데 그 `None` 이 **같은 이름으로
        # 증거에 기재**된다. C37 이 초록으로 남은 방식이 바로 이것이다: 값은 없고 이름은 있다.
        never = sorted((needs & look["asked"]) - look["hit"])
        filed = set()
        for body in bodies:
            res_b = body.results.get(node)
            if res_b is None:
                continue
            for key in never:
                if key in res_b.inputs and res_b.inputs[key] is None:
                    filed.add(key)
        new_filed = sorted(k for k in filed if (node, k) not in CLASS1_KNOWN)
        known_filed = sorted(k for k in filed if (node, k) in CLASS1_KNOWN)
        if new_filed:
            fails.append(f"{node}: 조회가 전부 미스인데 그 None 이 증거에 같은 이름으로 기재된다 — "
                         f"{', '.join(new_filed)} (C37 의 서명, 클래스 ①)")
        if known_filed:
            print(f"  [클래스 ① · 기존] {node}: {', '.join(known_filed)} — C50 에 등재된 사례")
        class1_seen.update((node, k) for k in filed)
        rest = sorted(set(never) - filed)
        if rest:
            class3[node] = rest
            print(f"  [클래스 ③] {node}: Needs 인데 어느 표본에서도 공급되지 않는다 — {', '.join(rest)}")
        # ② 철자 오류의 형태 — 선택적이라고 선언되지 않은 조회가 전부 미스이고 Needs 에도 없다.
        #    (클래스 나누기는 C45 (b) 정정 참조: 좁힌 것이 아니라 판정을 셋으로 나눈 것이다.)
        stray = sorted((look["miss"] & look["hard"]) - needs)
        if stray:
            fails.append(f"{node}: 아무도 공급하지 않는 조회이고 Needs 에도 없다 — {', '.join(stray)}")
        # ③ 보고만 — 소스에는 있는데 어느 표본도 밟지 않은 조회, 그리고 아무도 조회하지 않는 Needs.
        unexercised = sorted(literals - look["asked"])
        unread = sorted(needs - look["asked"])
        if unexercised:
            print(f"  [기록] {node}: 소스에 있으나 표본이 밟지 않은 조회 — {', '.join(unexercised)}")
        if unread:
            print(f"  [기록] {node}: Needs 인데 조회되지 않는다 — {', '.join(unread)} "
                  f"(다른 노드의 출력으로 들어올 수 있다)")

        res = None

        union_in = union_out = union_units = None
        for body in bodies:
            # 그래프를 통째로 돌린 뒤에 읽는다. 레시피를 하나만 불러서는 **다른 노드의
            # 출력을 먹는 노드** 의 계약을 확인할 수 없다 — core_state 가 그렇다.
            candidate = body.results.get(node)
            if candidate is None:
                continue
            res = res or candidate
            if candidate.applicable:
                # 가지가 여럿인 레시피는 표본 하나로는 Returns 를 다 못 본다 — 값을 내는
                # 표본 전부의 입력·출력을 합친다 (C19: dynamo_giant 의 갈색왜성 가지).
                if union_in is None:
                    res = candidate
                    union_in, union_out, union_units = set(candidate.inputs), set(candidate.values), dict(candidate.units)
                else:
                    union_in |= set(candidate.inputs); union_out |= set(candidate.values); union_units.update(candidate.units)
        if res is None:
            print(f"  [건너뜀] {node}: 어느 표본 천체도 입력을 갖추지 못했다")
            continue
        if not res.applicable:
            print(f"  [건너뜀] {node}: 표본 천체가 전부 도메인 밖이다 "
                  f"— Returns 를 확인할 수 없다")
            continue
        actual_in = union_in
        actual_out = union_out
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
            if name not in union_units:
                fails.append(f"{node}: 출력 '{name}' 에 단위가 없다")


    gone = sorted(CLASS1_KNOWN - class1_seen)
    if gone:
        print(f"  [클래스 ① · 사라짐] {', '.join(f'{n}.{k}' for n, k in gone)} — "
              f"고쳐졌으면 CLASS1_KNOWN 에서 지울 것")
    n3_nodes = len(class3)
    n3_keys = len({k for v in class3.values() for k in v})
    n3_pairs = sum(len(v) for v in class3.values())
    got3 = (n3_nodes, n3_keys, n3_pairs)
    print(f"  [클래스 ③ 합계] {n3_nodes} 노드 · 고유 키 {n3_keys} · 쌍 {n3_pairs} "
          f"(기준선 {CLASS3_BASELINE[0]} · {CLASS3_BASELINE[1]} · {CLASS3_BASELINE[2]}, C50) — "
          f"{'변화 없음' if got3 == CLASS3_BASELINE else '⚠ 기준선과 다르다'}")

    total = sum(1 for d in g["nodes"].values() if d.get("kind") == "computed")
    for f in fails:
        print(f"  [FAIL] {f}")
    if not fails:
        n_look = sum(len(b.lookups) for b in bodies)
        print(f"  [PASS] 계약 대조 {checked}건 — 문서와 코드가 일치 "
              f"(레시피 {len(registry.registered())} / 계산 노드 {total}); "
              f"조회 {n_look}건을 Needs·AST 와 대조 (C45 (b))")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
