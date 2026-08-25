# 천체 하나의 물리 상태 — 선언된 입력과 도출된 값을 한 자리에 모은다
"""The physical state of one body: declared inputs plus derived Results.

이것이 엔진의 산출물이다. KSP cfg 가 아니라 물리 상태이고, cfg 로 옮기는 일은
어댑터가 한다. 그래서 여기에는 게임 개념이 없다 — 양과 단위와 출처만 있다.

값은 두 갈래로 들어온다.

* **선언된 입력** — 측정치(mass, radius, orbit …)와 오너 결정(조성 의도, 바다
  비율, 고리 …). 도출되지 않는다. 사람이 정하거나 논문이 준다.
* **도출값** — 레시피가 돌려준 `Result`. 값 자체가 아니라 상태 전체를 들고
  있으므로, 나중에 무엇을 먹고 어느 분기를 탔는지 되짚을 수 있다.

읽을 때는 둘을 구분하지 않는다. 레시피는 `state["nmoi"]` 라고만 쓰고, 그게
입력에서 왔는지 다른 레시피에서 왔는지는 신경 쓰지 않는다.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from payload import Result


class Missing(KeyError):
    """아직 없는 값을 읽으려 했다. 레시피가 이걸 받으면 자기 차례가 아니다."""


@dataclass
class BodyState:
    name: str
    kind: str                                   # star | planet | moon
    parent: str | None = None
    inputs: dict[str, Any] = field(default_factory=dict)
    units: dict[str, str] = field(default_factory=dict)
    results: dict[str, Result] = field(default_factory=dict)   # 노드 이름 -> Result
    parent_state: "BodyState | None" = None

    # ── 읽기 ────────────────────────────────────────────────────────────
    def __contains__(self, key: str) -> bool:
        try:
            self[key]
            return True
        except Missing:
            return False

    def __getitem__(self, key: str) -> Any:
        if key in self.inputs:
            return self.inputs[key]
        for r in self.results.values():
            if r.applicable and key in r.values:
                return r.values[key]
        raise Missing(f"{self.name}: '{key}' 가 아직 없다")

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except Missing:
            return default

    def of_parent(self, key: str) -> Any:
        """부모의 값을 읽는다. scope=parent 엣지가 이 경로를 쓴다."""
        if self.parent_state is None:
            raise Missing(f"{self.name}: 부모가 없다 ('{key}' 요청)")
        return self.parent_state[key]

    def unit(self, key: str) -> str | None:
        if key in self.units:
            return self.units[key]
        for r in self.results.values():
            if key in r.units:
                return r.units[key]
        return None

    # ── 쓰기 ────────────────────────────────────────────────────────────
    def record(self, node: str, result: Result) -> None:
        self.results[node] = result

    # ── 요약 ────────────────────────────────────────────────────────────
    @property
    def resolved(self) -> dict[str, Any]:
        """도출된 값 전부. 범위 밖 판정은 값을 내지 않으므로 빠진다."""
        out: dict[str, Any] = {}
        for r in self.results.values():
            if r.applicable:
                out.update(r.values)
        return out

    @property
    def declined(self) -> dict[str, str]:
        """범위 밖이라 계산하지 않은 노드와 그 이유. 실패가 아니라 답이다."""
        return {n: r.reason for n, r in self.results.items() if not r.applicable}

    def report(self) -> str:
        lines = [f"{self.name} ({self.kind})"]
        lines.append(f"  선언된 입력 {len(self.inputs)} · 도출값 {len(self.resolved)} "
                     f"· 범위 밖 {len(self.declined)}")
        for node, r in sorted(self.results.items()):
            mark = "  " if r.applicable else "· "
            vals = ", ".join(f"{k}={_short(v)}{_u(r.units.get(k))}"
                             for k, v in r.values.items()) or r.reason[:72]
            lines.append(f"    {mark}{node:24} {vals}")
        return "\n".join(lines)


def _short(v: Any) -> str:
    if isinstance(v, float):
        return f"{v:.4g}"
    return str(v)[:40]


def _u(unit: str | None) -> str:
    return f" {unit}" if unit else ""
