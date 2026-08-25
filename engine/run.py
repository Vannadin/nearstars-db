# 선언된 그래프를 실제로 실행한다 — 순서·순환·부모 규칙을 chain.yaml 에서 읽어서
"""Execute the declared graph over a body.

    python3 engine/run.py bodies/alpha_centauri_a_b.yaml

`chain.py` 는 순서를 알고 `dynamo.py` 는 계산을 안다. 둘을 잇는 것이 없어서
그래프가 그림으로만 있었다. 이 파일이 그 자리다.

순서는 어디서 오나
------------------
`chain.yaml` 의 `requires` 와 `selects` 를 위상정렬한다. 다만 그래프에 순환이
여섯 개 선언돼 있어서 그대로는 정렬이 안 된다. 선언된 순환은 하나의 덩어리로
접어 정렬하고, 덩어리 안에서는 `resolution` 이 말하는 대로 **시드 후 반복**한다.
전부 "두 번 반복" 이라 기본 2회로 두되, 값이 안 움직이면 일찍 멈춘다.

`scope: parent` 엣지는 순서에서 뺀다. 다른 천체를 거쳐가므로 한 천체 안의
순서가 아니다. 대신 천체를 풀 때 부모를 먼저 푼다 (`ordering_rules`).

없는 레시피
-----------
28개 계산 노드 중 지금 구현된 것은 하나다. 없는 노드는 오류가 아니라 아직
안 만든 것이므로, 세어서 보고하고 계속 간다. 그래야 첫 레시피부터 러너를 쓸 수
있고, 스물여덟 번째까지 기다리지 않아도 된다.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

import graph
import registry
from payload import Result
from state import BodyState, Missing

HERE = Path(__file__).resolve().parent
CHAIN = HERE / "chain.yaml"
MAX_PASSES = 4          # resolution 은 전부 "두 번" 이다. 여유를 두되 무한은 아니다.


def load_chain() -> dict:
    return graph.load()


# ── 순서 ────────────────────────────────────────────────────────────────
# 순서와 순환 규칙은 graph.py 하나에만 있다. 검증기와 러너가 다른 규칙을 쓰면
# 검증을 통과한 그래프가 실행되지 않는다 — 실제로 그랬다.
order = graph.order


# ── 실행 ────────────────────────────────────────────────────────────────
def solve(body: BodyState, g: dict, verbose: bool = False) -> dict[str, int]:
    nodes = g["nodes"]
    stats = {"computed": 0, "declined": 0, "no_recipe": 0, "not_ready": 0}
    missing: list[str] = []

    for unit in order(g):
        computable = [n for n in unit if nodes[n].get("kind") == "computed"]
        if not computable:
            continue
        passes = MAX_PASSES if len(unit) > 1 else 1
        for p in range(passes):
            before = dict(body.resolved)
            stalled: dict[str, str] = {}
            for node in computable:
                fn = registry.get(node)
                if fn is None:
                    if p == 0 and node not in missing:
                        missing.append(node)
                    continue
                try:
                    res: Result = fn(body)
                except Missing as exc:
                    # 입력이 아직 없다. 반복하면 생길 수도 있으므로 이번 회차만
                    # 기록하고, 마지막 회차의 것만 최종 집계한다. 예전에는
                    # `p == passes - 1` 로 셌는데 일찍 수렴하면 거기 도달하지 않아
                    # 영영 세지 않았다.
                    stalled[node] = str(exc)
                    continue
                body.record(node, res)
            if body.resolved == before:
                break                      # 값이 안 움직인다. 수렴했다.
        stats["not_ready"] += len(stalled)
        if verbose:
            for node, why in stalled.items():
                print(f"    [대기] {node}: {why}")
        if len(unit) > 1 and verbose:
            print(f"    [순환] {', '.join(unit)} — {p + 1}회")

    for node, r in body.results.items():
        stats["declined" if not r.applicable else "computed"] += 1
    stats["no_recipe"] = len(missing)
    return stats


# ── 입력 ────────────────────────────────────────────────────────────────
def load_body(path: Path) -> tuple[BodyState, dict]:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    body = BodyState(
        name=doc["name"], kind=doc["kind"], parent=doc.get("parent"),
        inputs=doc.get("inputs") or {}, units=doc.get("units") or {})
    return body, doc.get("expected") or {}


def compare(body: BodyState, expected: dict, default_tol: float = 0.02) -> int:
    """엔진이 낸 값과 이미 출하된 값을 대조한다.

    출하값은 엔진의 입력이 아니라 **재현해야 할 제약**이다. 어긋나면 엔진이
    틀렸거나 보드가 틀렸다는 뜻이고, 어느 쪽이든 찾을 가치가 있다.

    허용오차를 항목마다 둘 수 있다. 어떤 기대값은 *다른 기대값의 함수*라서
    전파 오차를 그대로 안기 때문이다 — 밀도는 반지름의 세제곱에 반비례하므로
    반지름이 1 % 어긋나면 밀도는 3 % 어긋난다. 그건 불일치가 아니라 산술이다.
    그런 항목은 `tol:` 과 함께 *왜* 느슨한지를 적는다.
    """
    if not expected:
        return 0
    bad = 0
    print("\n  이미 출하된 값과 대조")
    for key, spec in sorted(expected.items()):
        got = body.get(key)
        want = spec["value"]
        if got is None:
            print(f"    [건너뜀] {key:14} 엔진이 아직 이 값을 안 낸다")
            continue
        tol = spec.get("tol", default_tol)
        off = abs(got - want) / abs(want) if want else abs(got)
        ok = off <= tol
        bad += 0 if ok else 1
        mark = "일치" if ok else "어긋남"
        print(f"    [{mark}] {key:14} 엔진 {got:>9.4g} · 보드 {want:>8} "
              f"{spec.get('unit','')}  ({off * 100:.1f}% / 허용 {tol * 100:.0f}%)")
        if ok and spec.get("tol_reason"):
            print(f"             허용 사유: {spec['tol_reason']}")
        if not ok:
            print(f"             출처: {spec.get('source','?')}")
    return bad


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    registry.load_all()
    g = load_chain()

    body, expected = load_body(
        Path(args[0]) if Path(args[0]).is_absolute() else HERE / args[0])
    stats = solve(body, g, verbose="-v" in args)
    print(body.report())
    total = sum(1 for d in g["nodes"].values() if d.get("kind") == "computed")
    print(f"\n  계산 노드 {total} 중 — 값 냄 {stats['computed']} · "
          f"범위 밖 {stats['declined']} · 입력 부족 {stats['not_ready']} · "
          f"레시피 없음 {stats['no_recipe']}")
    sys.exit(1 if compare(body, expected) else 0)


if __name__ == "__main__":
    main()
