# 한 풀이 안에서 유계 솔버가 닫혔는지를 모으는 기록기 — 값 경로는 건드리지 않는다 (C71, 브리프 189)
"""Per-solve convergence trace.

⚠ **왜 값이 아니라 기록기인가.** C71 의 내용은 «미수렴 값이 산문 한 줄과 함께 배달된다» 이고,
고치는 방법은 **소비처가 읽을 수 있는 값**으로 내는 것이다 (C61: 세지 않은 걸음은 통과한 걸음으로
읽힌다). 각 자리가 `(값, 수렴)` 을 돌려주게 바꾸면 호출부 스물셋이 함께 움직이고 그 diff 안에서
«값이 안 움직였다» 를 증명하기 어렵다. 그래서 **값은 그대로 두고** 각 자리가 여기에 한 줄을
남기며, 노드가 그 요약을 `values` 에 싣는다.

⚠ **`converged` 의 뜻** (브리프 189 Amendment 1): **진입 시 괄호가 유효했고**(f(lo)·f(hi) < 0,
또는 그 자리의 동치) **종료가 기준 가지였다**(예산 소진이 아니라). 고정 횟수 이분법에서 폭 검사는
`초기폭/2^N` 이라 **항상 참**이므로 아무것도 묻지 않는다 — 그 자리에서 묻는 것은 부호다.

⚠ **괄호를 싸게 확인할 수 없는 자리**(f(hi) 가 정의되지 않거나 거절 영역)는 참을 지어내지 않고
`bracket_checked=False` 를 남긴다.

⚠ **중첩된 풀이는 바깥 것에 합쳐진다** — `infer_composition` 이 `solve` 을 여러 번 부르므로,
가장 바깥 `start()` 가 하나의 기록을 들고 안쪽은 거기에 적는다.
"""
from __future__ import annotations

import contextlib
import contextvars
from dataclasses import dataclass, field

_TRACE: contextvars.ContextVar["Trace | None"] = contextvars.ContextVar(
    "convergence_trace", default=None)


@dataclass
class Trace:
    """한 풀이가 지나간 유계 솔버들의 기록.

    ⚠ **`converged` 는 세 값이다** (브리프 189 Amendment 2, 감사석 실측): `True` · `False` ·
    `None`. **`None` 은 «기준 가지가 없는 자리»** 다 — `core_state` :322 · `mantle_flux` :139 ·
    `stagnant_lid` :360 · `ammonia_table` :274 는 `break` 도 이른 `return` 도 없이 정해진 횟수를
    다 돌고 중점을 돌려준다. 거기에 «기준으로 나갔는가» 를 물으면 **항상 거짓**이고, 그것은
    항상 참인 깃발과 똑같이 나쁘다. 기준 가지를 새로 넣는 것은 돌려주는 중점을 바꾸므로
    §4 가 금지한다 — 그래서 상태를 비우고 그 이유를 이름으로 남긴다."""
    sites: dict[str, bool | None] = field(default_factory=dict)
    unchecked: set[str] = field(default_factory=set)
    invalid: set[str] = field(default_factory=set)

    def note(self, site: str, converged: bool | None,
             bracket_checked: bool = True, bracket_valid: bool | None = None) -> None:
        """⚠ **한 자리가 여러 번 불리면 AND 다** — 한 번이라도 안 닫혔으면 안 닫힌 것이다."""
        if converged is None:
            self.sites.setdefault(site, None)
        else:
            prev = self.sites.get(site)
            self.sites[site] = bool(converged) if prev in (None, True) else False
        if not bracket_checked:
            self.unchecked.add(site)
        if bracket_valid is False:
            self.invalid.add(site)

    @property
    def converged(self) -> bool | None:
        """이 풀이에서 **실제로 돌았고 기준 가지를 가진** 자리들에 대한 AND.

        ⚠ 전부 `None` 이면 노드도 `None` 이다 — «전부 통과» 가 아니라 «물을 것이 없었다» 이고,
        둘을 같은 `True` 로 인쇄하면 읽는 사람이 검사를 본 줄 안다."""
        judged = [v for v in self.sites.values() if v is not None]
        return None if not judged else all(judged)

    @property
    def unconverged_sites(self) -> list[str]:
        """`False` 를 돌려준 자리의 이름. 괄호를 확인 못 한 자리는 `?` 를 단다."""
        return [name + ("?" if name in self.unchecked else "")
                for name in sorted(self.sites) if self.sites[name] is False]

    @property
    def bracket_invalid_sites(self) -> list[str]:
        """진입 부호 검사가 실패한 자리 — 상태와 무관하게 싣는다."""
        return sorted(self.invalid)

    @property
    def no_criterion_sites(self) -> list[str]:
        """기준 가지가 없어 상태를 비운 자리."""
        return sorted(n for n, v in self.sites.items() if v is None)


def note(site: str, converged: bool | None, bracket_checked: bool = True,
         bracket_valid: bool | None = None) -> None:
    """현재 풀이의 기록에 한 줄. 기록이 없으면(모듈을 직접 부른 경우) 조용히 지나간다."""
    tr = _TRACE.get()
    if tr is not None:
        tr.note(site, converged, bracket_checked, bracket_valid)


@contextlib.contextmanager
def start():
    """한 풀이의 기록을 연다. **중첩되면 바깥 것을 그대로 쓴다.**"""
    tr = _TRACE.get()
    if tr is not None:
        yield tr
        return
    tr = Trace()
    token = _TRACE.set(tr)
    try:
        yield tr
    finally:
        _TRACE.reset(token)


def bracket_valid(f_lo: float, f_hi: float) -> bool:
    """괄호가 뿌리를 감쌌는가 — 부호가 갈리는가. 0 은 뿌리이므로 유효로 센다.

    ⚠ **이 검사를 넣으면 안 되는 자리가 있다** (감사석 실측, 브리프 189): 평가 경로에
    **따뜻한 출발 전역**이 있는 함수 — `water_hot._LAST_DENSITY` 는 :232–236 에서 직전 ρ 를
    같은 온도·열 배 안의 압력이면 출발점으로 읽고 매 종료마다 쓴다, `fermi._LAST_INVERSE` 도
    같다. 추가 평가 한 번이 **다음 호출의 답**을 바꾸므로, 실패가 호출 순서를 따라 움직여
    재현되지 않는다. 그런 자리는 `bracket_checked=False` 와 이유를 남긴다.
    ⚠ **순수 메모 캐시는 이 부류가 아니다** — `fe_liquid.thermal_at` 은 입력으로만 키를 만들어
    추가 호출이 메모리만 쓴다.""" 
    return f_lo == 0.0 or f_hi == 0.0 or (f_lo > 0.0) != (f_hi > 0.0)


def current() -> Trace | None:
    """지금 열린 기록. 없으면 `None`."""
    return _TRACE.get()


def traced(fn):
    """한 진입점을 기록으로 감싼다 — **중첩되면 바깥 기록에 합쳐진다**.

    ⚠ 데코레이터로 두는 이유는 «값 경로를 건드리지 않는다» 를 눈으로 확인할 수 있게 하기
    위해서다: 함수 본문은 한 줄도 바뀌지 않고, 들여쓰기도 움직이지 않는다."""
    import functools

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        with start():
            return fn(*args, **kwargs)

    return wrapper
