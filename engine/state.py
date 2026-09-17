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
    # ⚠ **반환 모양은 안 바꾼다** (C71). 꼬리표는 값에 붙지 않고 **결과 객체**에 남아 있다.
    #   바뀐 것은 «누가 답했는가» 를 `_producer` 가 따로 알려 준다는 것뿐이고, 이 함수의 다섯
    #   호출부(`__contains__`·`__getitem__`·`get`·`get_optional`·계약 검사)는 한 줄도 안 고친다.
    def _find(self, key: str) -> tuple[bool, Any]:
        """조회 한 번의 순수한 부분 — 기록하지 않는다. 선언된 입력이 먼저, 그 다음 도출값."""
        if key in self.inputs:
            return True, self.inputs[key]
        for r in self.results.values():
            if r.applicable and key in r.values:
                return True, r.values[key]
        return False, None

    def _producer(self, key: str) -> str | None:
        """그 키에 **실제로 답하는** 노드 이름. 선언된 입력이 이기면 `None`.

        ⚠ `_find` 와 **같은 순서로 돈다**. 두 함수가 다른 순서를 돌면 꼬리표가 다른 결과의
        것이 되고, 그 순간 등급이 남의 수렴 여부를 말하게 된다."""
        if key in self.inputs:
            return None
        for node, r in self.results.items():
            # ⚠ 위 `_find` 와 **같은 조건, 다른 철자**로 적는다 — 같은 문장을 두 번 쓰면
            #   원장의 구절 앵커가 두 곳에 매치해 애매해진다 (실제로 한 번 그랬다).
            if not r.applicable or key not in r.values:
                continue
            return node
        return None

    def unconverged_reads(self, node: str | None = None) -> tuple[str, ...]:
        """이 노드가 읽은 값 가운데 **미수렴 결과에서 온 것들** — `"노드.키"` 꼴 (C71).

        ⚠ **조회 로그를 읽는다.** 그래서 `NEARSTARS_LOOKUP_LOG=0` 이면 빈 튜플이 나오고, 그
        빈 튜플은 «미수렴 입력 없음» 과 똑같이 생겼다 — 호출부가 그 둘을 구별해야 한다면
        로그가 켜져 있는지를 먼저 물어야 한다 (`log_enabled`).
        ⚠ **순서를 보존하고 중복을 없앤다.** 같은 키를 두 번 읽어도 표지는 하나다."""
        who = self.current_node if node is None else node
        out: list[str] = []
        for reader, key, _kind in self.lookups:
            if reader != who:
                continue
            producer = self._producer(key)
            if producer is None:
                continue
            r = self.results.get(producer)
            if r is None:
                continue
            mark = None
            # ⚠ **`Result.converged` 가 아니라 그 풀이가 **기록한** 것을 읽는다** (C71 곁가지).
            #   필드 `converged` 는 자기 주석이 «순환 위에 있을 때만 의미가 있다» 라고 적는다 —
            #   `chain.yaml` 의 순환 일곱에 드는 노드는 **13** 개이고 나머지 **38** 개는 그 칸을
            #   아예 안 채운다. 그 필드로 거르면 네 노드 중 셋에게는 «안 붙었다» 를 말할 통로가
            #   없다. 기록기가 낸 `values["converged"]` 는 그 풀이 안 솔버 자리들의 AND 라서
            #   순환과 무관하게 답한다. 실측: earth·pandora 의 `interior_layers` 는 기록기가
            #   False 인데 필드는 True 였고, 표지가 한 소비처에도 안 갔다.
            #   ⚠ `None` 은 «물을 것이 없었다» 이므로 표지를 안 단다 — `is False` 로만 건다.
            if (r.values or {}).get("converged") is False:
                mark = f"{producer}.{key}"
            elif r.values.get("substituted_solvers"):
                # ⚠ **«미수렴» 이 아니다.** 예산이 끝나 앞선 시행이 답으로 나온 값이고, 그
                #   시행은 허용오차를 만족한다. 소비처가 알아야 할 것은 «값이 틀렸다» 가
                #   아니라 «이 값에 이르는 길이 안 보인다» 이고, 등급 상한은 그 사실에 건다.
                mark = f"best-of-budget:{producer}.{key}"
            if mark and mark not in out:
                out.append(mark)
        return tuple(out)

    @staticmethod
    def log_enabled() -> bool:
        """조회 로그가 켜져 있는가. `unconverged_reads` 의 빈 튜플을 읽을 때 같이 묻는다."""
        return BodyState._LOG

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
