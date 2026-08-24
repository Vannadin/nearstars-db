# 역류 층이 실제로 일어난 두 사고를 잡는지 고정한다 — 통과하면 그 사고는 다시 안 난다
"""Anchor the backflow layer on the two failures it exists to prevent.

    python3 engine/test_backflow.py

앵커는 우리가 만든 출력이 아니라 **실제로 일어난 사고**다. 하나는 Proxima 의
pause_nose 갱신 누락, 하나는 J₂ 가 21시간 위성 시뮬의 입력이라는 사실이다.
"""
from __future__ import annotations

import sys

import backflow


def main() -> int:
    chain, binds = backflow.load()
    fields = binds["fields"]
    fails: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # ── 사고 1: Proxima. pause_nose 가 23.5 → 35.33 으로 바뀌었는데 그 함수인
    # outer_compression / outer_extension 이 재계산되지 않았다. 그 관계가 어느
    # 파일에도 없었기 때문이다. 이제 있어야 한다.
    kids = {n for n, b in fields.items() if "pause_nose" in (b.get("derived_from") or [])}
    for child in ("outer_compression", "outer_extension"):
        ok(child in kids, f"사고 1: {child} 가 pause_nose 의 자식으로 안 적혀 있다")
    ok(len(kids) >= 4, f"사고 1: pause_nose 의 직접 자식이 {len(kids)}개뿐 — 문서상 더 많다")

    # ── 사고 2: J₂ 는 방법론의 결론이 아니라 21시간 위성 시뮬의 입력이다.
    # 내부구조가 NMoI 를 바꾸면 그 런과 결과가 함께 열린다.
    j2 = fields.get("geopotential_j2") or {}
    ok("body_figure" in (j2.get("produced_by") or []),
       "사고 2: geopotential_j2 가 body_figure 소생으로 안 적혀 있다")
    sims = [c for c in (binds.get("consumers") or [])
            if "geopotential_j2" in (c.get("consumes") or [])]
    ok(bool(sims), "사고 2: J₂ 를 먹는 소비처가 하나도 없다 — 21시간 런이 안 보인다")
    for c in sims:
        ok(bool(c.get("cost")), f"사고 2: 소비처 '{c.get('id')}' 에 비용이 없다")
        ok(bool(c.get("invalidates")), f"사고 2: 소비처 '{c.get('id')}' 가 무엇을 무효화하는지 안 적혀 있다")

    # ── 되열림 질의가 실제로 답을 내는지. body_figure 는 J₂ 를 낳으므로
    # 반드시 시뮬을 걸어야 한다.
    dist = backflow._downstream_nodes(chain, "body_figure")
    ok(dist.get("body_figure") == 0, "그래프 질의: 시작 노드의 거리가 0 이 아니다")
    own = {n for n, b in fields.items() if "body_figure" in (b.get("produced_by") or [])}
    ok("geopotential_j2" in own, "그래프 질의: body_figure 가 J₂ 를 안 낳는 것으로 나온다")

    # ── 거리를 재는 이유. 안 재면 어느 노드를 물어도 "거의 전부" 가 나온다.
    ok(len(dist) < len(chain["nodes"]),
       "그래프 질의: 한 노드에서 전체 노드가 닿는다 — 거리 구분이 무의미해진다")

    # ── 계약: 바인딩은 값을 다시 적지 않는다. 값이 사는 곳은 보드 하나여야 한다.
    for name, b in fields.items():
        ok("value" not in b, f"계약 위반: '{name}' 바인딩이 값을 들고 있다")

    if fails:
        for f in fails:
            print(f"  [FAIL] {f}")
        return 1
    n_kids = len(backflow._derived_closure(fields, {"pause_nose"})) - 1
    print(f"  [PASS] 사고 1 — pause_nose 뒤로 {n_kids}종이 추적된다 "
          f"(outer_compression·outer_extension 포함)")
    print(f"  [PASS] 사고 2 — J₂ 가 {sims[0]['id']} [{sims[0]['cost']}] 의 입력으로 잡힌다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
