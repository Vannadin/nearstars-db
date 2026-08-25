# chain.yaml 의 노드 이름에 실제 함수를 붙인다 — 선언과 구현을 잇는 유일한 지점
"""Bind chain.yaml node names to the functions that compute them.

    from registry import recipe

    @recipe("dynamo_giant")
    def _(state):
        ...
        return Result(...)

레시피는 `state` 하나만 받는다. 무엇을 소비했는지는 `Result.inputs` 에 스스로
적으므로, 러너가 인자를 맞춰줄 필요가 없고 시그니처가 노드마다 달라지지도 않는다.

등록하지 않은 노드는 오류가 아니라 **아직 구현 안 된 상태**다. 28개 중 지금
구현된 것이 하나뿐이므로, 러너는 빠진 것을 세어 보고하고 계속 간다.
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable

import yaml

CHAIN = Path(__file__).resolve().parent / "chain.yaml"

_REGISTRY: dict[str, Callable] = {}


def recipe(node: str) -> Callable:
    """노드 하나를 계산하는 함수로 등록한다."""
    nodes = yaml.safe_load(CHAIN.read_text(encoding="utf-8"))["nodes"]
    if node not in nodes:
        raise KeyError(f"'{node}' 는 chain.yaml 에 없는 노드다")
    if nodes[node].get("kind") != "computed":
        raise ValueError(
            f"'{node}' 는 {nodes[node].get('kind')} 다. 계산 노드만 레시피를 가진다 — "
            "측정치는 입력, 오너 결정은 선언, 클래스 표는 조회다")
    if node in _REGISTRY:
        raise ValueError(f"'{node}' 에 이미 레시피가 등록돼 있다")

    def wrap(fn: Callable) -> Callable:
        _REGISTRY[node] = fn
        fn.node = node
        return fn
    return wrap


def get(node: str) -> Callable | None:
    return _REGISTRY.get(node)


def registered() -> set[str]:
    return set(_REGISTRY)


def load_all() -> None:
    """레시피 모듈을 전부 import 해서 등록을 채운다.

    지금은 하나뿐이라 명시 목록이 제일 정직하다. 늘어나면 여기만 늘린다 —
    디렉터리를 자동 스캔하면 등록 실패가 조용히 지나간다.
    """
    import dynamo        # noqa: F401
    import mass_radius   # noqa: F401
    import interior      # noqa: F401
