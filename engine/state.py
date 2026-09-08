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

import os
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
    #: 이 상태에 실제로 요청된 조회들 — `(노드, 키, 결과)`. C45 (b): 계약 검사가
    #: `Result.inputs`(저자가 타이핑한 이름) 대신 **코드가 실제로 조회한 문자열** 을 보게
    #: 하는 유일한 관측점이다. 런타임 비용은 append 하나이고 아무도 읽지 않으면 그냥 쌓인다.
    lookups: list[tuple[str | None, str, str]] = field(default_factory=list)
    #: 지금 돌고 있는 노드 — `run.solve` 가 레시피를 부르기 직전에 세운다.
    current_node: str | None = None

    # ── 읽기 ────────────────────────────────────────────────────────────
    def _find(self, key: str) -> tuple[bool, Any]:
        """조회 한 번의 순수한 부분 — 기록하지 않는다. 선언된 입력이 먼저, 그 다음 도출값."""
        if key in self.inputs:
            return True, self.inputs[key]
        for r in self.results.values():
            if r.applicable and key in r.values:
                return True, r.values[key]
        return False, None

    #: 조회 로그는 기본 켜짐 — 게이트가 이것으로 계약을 검사한다. `NEARSTARS_LOOKUP_LOG=0` 으로
    #: 끄면 append 조차 하지 않는다(측정과 대량 스윕용). C45 (b).
    _LOG = os.environ.get("NEARSTARS_LOOKUP_LOG", "1") != "0"

    def _note(self, key: str, found: bool, kind: str) -> None:
        if not BodyState._LOG:
            return
        self.lookups.append((self.current_node, key, f"{kind}{'hit' if found else 'miss'}"))

    def __contains__(self, key: str) -> bool:
        found, _ = self._find(key)
        # 존재 시험은 그 자체가 "없을 수도 있다" 는 선언이므로 발견 대상이 아니다.
        self._note(key, found, "contains-")
        return found

    def __getitem__(self, key: str) -> Any:
        found, value = self._find(key)
        self._note(key, found, "")
        if found:
            return value
        raise Missing(f"{self.name}: '{key}' 가 아직 없다")

    def get(self, key: str, default: Any = None) -> Any:
        found, value = self._find(key)
        self._note(key, found, "")
        return value if found else default

    def get_optional(self, key: str, default: Any = None) -> Any:
        """없어도 되는 조회 — 선호-대체 패턴(선언이 이기고 없으면 프리셋/다른 이름)용.

        ⚠ **`get` 과 동작은 같고 기록만 다르다.** C45 (b): 어떤 미스가 설계이고 어떤 미스가
        C37 인지는 도구의 판단이 아니라 **호출부의 선언** 이어야 한다. 그래서 계약 검사는
        여기로 들어온 미스를 발견으로 세지 않는다."""
        found, value = self._find(key)
        self._note(key, found, "optional-")
        return value if found else default

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
