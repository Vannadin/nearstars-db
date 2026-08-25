# 출하된 확정값의 역류를 추적한다 — 노드를 바꾸면 이미 나간 값 중 무엇이 무효가 되는가
"""Trace what already-shipped Phase 4 values a methodology change invalidates.

    python3 engine/backflow.py check            바인딩 무결성 검사
    python3 engine/backflow.py impact <노드>     그 노드를 바꾸면 무효가 되는 출하값 전부
    python3 engine/backflow.py after <필드>      그 값을 고쳤을 때 함께 고쳐야 할 확정값
    python3 engine/backflow.py field <필드>      한 필드의 부모/자식/소비처
    python3 engine/backflow.py debt             벌크로 뭉쳐 재도출 불가능한 필드

`chain.yaml` 은 방법론끼리의 의존만 그린다. 값이 출하된 뒤에 벌어지는 일 — 시뮬의
입력이 되고, 다른 확정값의 부모가 되고, 앞으로 쓸 함수가 재현해야 할 제약이 되는 것
— 은 거기 없다. 지금까지 기록된 사고는 전부 그 안 그려진 층에서 났다.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CHAIN = ROOT / "engine" / "chain.yaml"
BINDINGS = ROOT / "engine" / "bindings.yaml"
BOARDS = sorted((ROOT / "phase4").glob("*.yaml"))

# 물리 도출값이 아닌 필드. 노드에 안 붙는 것이 정상이다.
NON_PHYSICAL = {"label", "gameplay", "art"}


def load():
    chain = yaml.safe_load(CHAIN.read_text(encoding="utf-8"))
    binds = yaml.safe_load(BINDINGS.read_text(encoding="utf-8"))
    return chain, binds


def instances() -> list[dict]:
    """보드에서 (천체, 축, 필드) 인스턴스를 전부 펼친다."""
    out = []
    for path in BOARDS:
        board = yaml.safe_load(path.read_text(encoding="utf-8"))
        for row in board.get("decisions") or []:
            for f in row.get("fields") or []:
                out.append({
                    "board": path.stem,
                    "body": row.get("body"),
                    "axis": row.get("axis"),
                    "name": f.get("name"),
                    "status": row.get("status"),
                })
    return out


def check(chain, binds) -> int:
    errors: list[str] = []
    warnings: list[str] = []
    nodes = set(chain["nodes"])
    fields = binds.get("fields") or {}
    seen = {i["name"] for i in instances()}

    for name in sorted(seen - set(fields)):
        errors.append(f"필드 '{name}' 이 보드에 있는데 bindings 에 없다")
    for name in sorted(set(fields) - seen):
        warnings.append(f"바인딩 '{name}' 이 어느 보드에도 없다 (필드가 사라졌나)")

    for name, b in fields.items():
        for n in b.get("produced_by") or []:
            if n not in nodes:
                errors.append(f"'{name}'.produced_by: '{n}' 는 chain.yaml 에 없는 노드")
        for p in b.get("derived_from") or []:
            if p not in fields:
                errors.append(f"'{name}'.derived_from: '{p}' 는 알려진 필드가 아니다")
        # 물리값인데 어느 노드도 안 낳는다면 그래프에 구멍이 있다는 뜻이다.
        if not (b.get("produced_by") or []) and b.get("kind") not in NON_PHYSICAL:
            warnings.append(f"'{name}': 물리값인데 produced_by 가 비었다 ({b.get('kind') or 'unmapped'})")

    for c in binds.get("consumers") or []:
        for name in c.get("consumes") or []:
            if name not in fields:
                errors.append(f"consumer '{c.get('id')}': '{name}' 는 알려진 필드가 아니다")

    # 확정값끼리의 순환은 계산 순서가 없다는 뜻이다. 다만 진짜 고정점인 경우가
    # 있으므로 — pause_smooth 는 문서가 명시적으로 고정점 반복으로 푼다고 적는다 —
    # chain.py 가 물리 순환을 다루는 것과 같은 규칙을 쓴다. 순환을 막는 게 아니라
    # *선언되지 않은* 순환을 막는다. 선언에는 근거가 붙어야 한다.
    declared = {frozenset(fp["members"]): fp for fp in (binds.get("fixed_points") or [])}
    for fp in (binds.get("fixed_points") or []):
        for m in fp["members"]:
            if m not in fields:
                errors.append(f"fixed_point '{fp.get('id')}': '{m}' 는 알려진 필드가 아니다")
        if not fp.get("ref"):
            errors.append(f"fixed_point '{fp.get('id')}': ref 가 없다")

    seen_c: set[str] = set()
    stack: list[str] = []

    def walk(n: str) -> None:
        if n in stack:
            loop = stack[stack.index(n):]
            if frozenset(loop) not in declared:
                errors.append("선언되지 않은 확정값 순환: " + " -> ".join(loop + [n]))
            return
        if n in seen_c:
            return
        seen_c.add(n)
        stack.append(n)
        for p in fields[n].get("derived_from") or []:
            if p in fields:
                walk(p)
        stack.pop()

    for name in fields:
        walk(name)

    n_dec = check_decisions(binds, errors)

    for w in warnings:
        print(f"  [WARN] {w}")
    for e in errors:
        print(f"  [FAIL] {e}")
    if not errors:
        phys = sum(1 for b in fields.values() if b.get("kind") not in NON_PHYSICAL)
        der = sum(1 for b in fields.values() if b.get("derived_from"))
        bun = sum(1 for b in fields.values() if b.get("bundled"))
        print(f"  [PASS] 필드 {len(fields)} (물리 {phys}) · 확정값끼리 의존 {der} "
              f"· 벌크 {bun} · 소비처 {len(binds.get('consumers') or [])} "
              f"· 근거-보드 대조 {n_dec}")
    return 1 if errors else 0


def board_values() -> dict[tuple[str, str], dict]:
    """보드에서 (천체, 필드) -> 필드 블록. decisions 대조에 쓴다."""
    out: dict[tuple[str, str], dict] = {}
    for path in BOARDS:
        board = yaml.safe_load(path.read_text(encoding="utf-8"))
        for row in board.get("decisions") or []:
            if row.get("status") == "superseded":
                continue
            for f in row.get("fields") or []:
                if f.get("name"):
                    out.setdefault((str(row.get("body")), f["name"]), f)
    return out


def check_decisions(binds: dict, errors: list[str]) -> int:
    """근거 문서가 고른 값을 보드가 실제로 들고 있는지 대조한다.

    consumers 와 방향이 반대다. 값이 어디로 흘러가는지가 아니라 **어디서
    정해졌는지** 를 보고, 보드가 그 답을 받았는지 확인한다. 결정이 나고도
    보드가 안 따라가는 것은 조용히 지나가던 실패였다.
    """
    board = board_values()
    checked = 0
    for d in binds.get("decisions") or []:
        key = (d["body"], d["field"])
        got = board.get(key)
        if got is None:
            errors.append(f"결정 {d['body']}.{d['field']}: 보드에 그 행이 없다")
            continue
        checked += 1
        try:
            a, b = float(got.get("value")), float(d["value"])
        except (TypeError, ValueError):
            if str(got.get("value")) != str(d["value"]):
                errors.append(f"결정 {d['body']}.{d['field']}: 보드 '{got.get('value')}' "
                              f"!= 근거 '{d['value']}' ({d['source']})")
            continue
        if b and abs(a - b) / abs(b) > 1e-6:
            errors.append(
                f"결정 {d['body']}.{d['field']}: 보드 {a:g} {got.get('unit','')} 인데 "
                f"근거 문서는 {b:g} {d.get('unit','')} 를 골랐다 — {d['source']}")
        elif got.get("unit") and d.get("unit") and got["unit"] != d["unit"]:
            errors.append(f"결정 {d['body']}.{d['field']}: 단위가 다르다 "
                          f"(보드 {got['unit']} vs 근거 {d['unit']})")
    return checked


def _downstream_nodes(chain, start: str) -> dict[str, int]:
    """chain.py 의 affects 와 같은 규칙 — requires/influences/selects 를 따라간다.

    거리를 함께 돌려준다. 이 그래프는 전이폐포가 거의 전체라서(노드 44개 중
    한 곳에서 30여 개가 닿는다) 거리를 안 재면 어느 노드를 물어도 "거의 전부"가
    나온다. 그건 사실이지만 쓸 수 없는 답이다.
    """
    adj = defaultdict(list)
    for e in chain["edges"]:
        if e["kind"] in ("requires", "influences", "selects"):
            adj[e["from"]].append(e["to"])
    dist = {start: 0}
    frontier = [start]
    while frontier:
        nxt_frontier = []
        for n in frontier:
            for m in adj[n]:
                if m not in dist:
                    dist[m] = dist[n] + 1
                    nxt_frontier.append(m)
        frontier = nxt_frontier
    return dist


def _derived_closure(fields: dict, roots: set[str]) -> set[str]:
    """확정값 → 확정값 의존을 닫는다. Proxima 사고가 살던 자리."""
    kids = defaultdict(list)
    for name, b in fields.items():
        for parent in b.get("derived_from") or []:
            kids[parent].append(name)
    out, stack = set(roots), list(roots)
    while stack:
        for k in kids[stack.pop()]:
            if k not in out:
                out.add(k)
                stack.append(k)
    return out


def impact(chain, binds, node: str) -> int:
    if node not in chain["nodes"]:
        print(f"'{node}' 는 chain.yaml 에 없다")
        return 2
    fields = binds["fields"]
    dist = _downstream_nodes(chain, node)
    insts = instances()

    # 1층: 이 노드가 직접 낳은 값. 반드시 다시 만들어야 한다.
    own = {n for n, b in fields.items() if node in (b.get("produced_by") or [])}
    # 그 값에서 계산된 다른 확정값 — 방법론을 거치지 않는 역류.
    own_closed = _derived_closure(fields, own)
    cascaded = own_closed - own
    # 2층 이후: 하류 노드가 낳은 값. 재검토 대상이지 자동 무효는 아니다.
    downstream = {n for n, b in fields.items()
                  if n not in own_closed
                  and any(dist.get(p, 99) > 0 for p in (b.get("produced_by") or []))}

    def rows_of(names):
        return [i for i in insts if i["name"] in names]

    r_own, r_cas, r_down = rows_of(own), rows_of(cascaded), rows_of(downstream)
    boards = sorted({i["board"] for i in r_own + r_cas})

    print(f"{node} 를 바꾸면\n")
    print(f"  ■ 반드시 다시 만들 값   {len(r_own)}행 / {len(own)}종"
          f"  (보드 {len(boards)}: {', '.join(boards) or '없음'})")
    if cascaded:
        print(f"  ■ 따라서 함께 무효      {len(r_cas)}행 / {len(cascaded)}종 — "
              f"{', '.join(sorted(cascaded))}")
        print(f"      ↑ 방법론을 안 거치고 확정값에서 확정값이 나온 자리. Proxima 사고가 여기서 났다.")
    print(f"  □ 재검토 대상(하류)     {len(r_down)}행 / {len(downstream)}종 "
          f"— 값이 바뀔 수도, 안 바뀔 수도")

    bundled = sorted(n for n in own_closed if fields[n].get("bundled"))
    if bundled:
        n_bun = sum(1 for i in r_own + r_cas if fields[i["name"]].get("bundled"))
        print(f"\n  벌크라 재도출 불가      {len(bundled)}종 / 행 {n_bun}개 — 쪼개기 전엔 다시 못 만든다")
        for n in bundled:
            note = (fields[n].get("note") or "").strip()
            print(f"      {n}{'  — ' + note if note else ''}")
    allf = own_closed

    hit = [c for c in (binds.get("consumers") or [])
           if allf & set(c.get("consumes") or [])]
    if hit:
        print(f"\n  다시 돌려야 할 것 {len(hit)}건")
        for c in hit:
            why = ", ".join(sorted(allf & set(c["consumes"])))
            print(f"      {c['id']}  [{c.get('cost', '비용 미상')}]  ← {why}")
            for line in (c.get("invalidates") or []):
                print(f"          그 결과 무효: {line}")

    docs = sorted({d for n in dist
                   for d in ([chain["nodes"][n].get("recipe")] if chain["nodes"][n].get("recipe") else [])})
    if docs:
        print(f"\n  손봐야 할 방법론 문서 {len(docs)}개 (+ ko 미러 같은 수)")
    return 0


def after(binds, name: str) -> int:
    """한 확정값을 손으로 고쳤다 — 그러면 뭘 따라가야 하나.

    Proxima 사고가 정확히 이 질문에 답이 없어서 났다. pause_nose 를 23.5 에서
    35.33 으로 고쳤는데, 그 함수인 outer_compression/outer_extension 이 그대로
    남았다. 관계가 어느 파일에도 없었으니 아무도 못 잡았다.
    """
    fields = binds["fields"]
    if name not in fields:
        print(f"'{name}' 는 bindings 에 없다")
        return 2
    kids = defaultdict(list)
    for n, b in fields.items():
        for p in b.get("derived_from") or []:
            kids[p].append(n)

    order: list[tuple[str, int]] = []
    seen = {name}
    frontier = [(name, 0)]
    while frontier:
        n, d = frontier.pop(0)
        for k in sorted(kids[n]):
            if k not in seen:
                seen.add(k)
                order.append((k, d + 1))
                frontier.append((k, d + 1))

    if not order:
        print(f"{name} 에서 계산되는 확정값은 없다. 이 값만 고치면 된다.")
        return 0
    insts = instances()
    n_rows = sum(1 for i in insts if i["name"] in seen and i["name"] != name)
    print(f"{name} 을 고쳤으면 함께 다시 계산해야 할 확정값 "
          f"{len(order)}종 / {n_rows}행\n")
    for n, d in order:
        b = fields[n]
        src = ", ".join(b.get("derived_from") or [])
        print(f"  {'  ' * (d - 1)}└ {n:30} ← {src}")
    print("\n  하나라도 빠뜨리면 그게 Proxima 사고다.")
    return 0


def field(binds, name: str) -> int:
    fields = binds["fields"]
    if name not in fields:
        print(f"'{name}' 는 bindings 에 없다")
        return 2
    b = fields[name]
    kids = sorted(n for n, o in fields.items() if name in (o.get("derived_from") or []))
    print(f"{name}")
    print(f"  낳은 노드      {', '.join(b.get('produced_by') or []) or '(없음 — ' + str(b.get('kind')) + ')'}")
    print(f"  재료로 쓴 값   {', '.join(b.get('derived_from') or []) or '(없음)'}")
    print(f"  이걸 쓰는 값   {', '.join(kids) or '(없음)'}")
    if b.get("bundled"):
        print(f"  ⚠ 벌크        {b.get('note') or '여러 노드 출력이 한 칸에'}")
    used = [c["id"] for c in (binds.get("consumers") or []) if name in (c.get("consumes") or [])]
    print(f"  소비처         {', '.join(used) or '(없음)'}")
    n = sum(1 for i in instances() if i["name"] == name)
    print(f"  출하된 인스턴스 {n}개")
    return 0


def debt(binds) -> int:
    fields = binds["fields"]
    bundled = {n: b for n, b in fields.items() if b.get("bundled")}
    counts = defaultdict(int)
    for i in instances():
        if i["name"] in bundled:
            counts[i["name"]] += 1
    print(f"벌크로 뭉쳐 재도출 불가능한 필드 {len(bundled)}종 / 행 {sum(counts.values())}개\n")
    for n, c in sorted(counts.items(), key=lambda kv: -kv[1]):
        owners = ", ".join(bundled[n].get("produced_by") or []) or "unmapped"
        print(f"  {c:3}행  {n:32} ← {owners}")
        note = (bundled[n].get("note") or "").strip()
        if note:
            print(f"         {note}")
    print("\n한꺼번에 쪼갤 필요는 없다. 레시피가 실제로 닿는 것부터 — `impact <노드>` 가 순서를 정해준다.")
    return 0


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    chain, binds = load()
    cmd = args[0]
    if cmd == "check":
        sys.exit(check(chain, binds))
    if cmd == "impact" and len(args) == 2:
        sys.exit(impact(chain, binds, args[1]))
    if cmd == "after" and len(args) == 2:
        sys.exit(after(binds, args[1]))
    if cmd == "field" and len(args) == 2:
        sys.exit(field(binds, args[1]))
    if cmd == "debt":
        sys.exit(debt(binds))
    print(__doc__)
    sys.exit(2)


if __name__ == "__main__":
    main()
