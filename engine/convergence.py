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
    substituted: dict[str, tuple[int, float]] = field(default_factory=dict)
    #: events counted, not judged — e.g. a Newton leaving its window before a safety net took over
    #: (prereg-fe-liquid-newton-fix ⓐ: the fact stays on record even when the site's state is `None`)
    counts: dict[str, int] = field(default_factory=dict)
    #: C138 — 다른 길로 간 자리(F): 대체 길이 제대로 된 답을 냈다. **AND 밖**, 셈만.
    fallbacks: dict[str, int] = field(default_factory=dict)
    #: C138 — 버린 시행 · 중간 패스의 False(P): 채택 답은 다른 시행일 수 있다. **AND 밖**, 따로 칸.
    trial_false: set[str] = field(default_factory=set)
    #: C139 — 버린 적분(시행)에서 진입 괄호가 깨진 자리. **AND 밖**, `bracket_invalid` 와 따로 칸.
    trial_invalid: set[str] = field(default_factory=set)
    #: C139 — 적분 한 번마다의 하위 기록 `[구조 id | None, 하위 Trace, "and" | "trial"]`. 끝나자마자 이 기록에
    #: AND 로 합쳐지므로(오늘과 같은 답), `settle` 을 부르지 않는 호출자는 한 비트도 달라지지 않는다.
    shots: list = field(default_factory=list)
    #: C139 — 적분 **밖에서** 직접 남긴 `note` 의 사본. `settle` 이 AND 를 다시 지을 때의 바탕이다.
    own: "Trace | None" = None
    #: C139 — 이 기록이 적분 한 번의 하위 기록인가(적분은 중첩되지 않는다 — `shot` 이 확인한다).
    in_shot: bool = False

    def note(self, site: str, converged: bool | None,
             bracket_checked: bool = True, bracket_valid: bool | None = None, trial: bool = False) -> None:
        """⚠ **한 자리가 여러 번 불리면 AND 다** — 한 번이라도 안 닫혔으면 안 닫힌 것이다.
        ``trial=True`` 면 버린 시행 · 중간 패스의 기록(C138 P 형) — False 는 `trial_false` 에만, AND 밖."""
        if self.own is not None:
            self.own.note(site, converged, bracket_checked, bracket_valid, trial)
        if trial:
            if converged is False:
                self.trial_false.add(site)
            if bracket_valid is False:
                self.invalid.add(site)
            return
        if converged is None:
            self.sites.setdefault(site, None)
        else:
            prev = self.sites.get(site)
            self.sites[site] = bool(converged) if prev in (None, True) else False
        if not bracket_checked:
            self.unchecked.add(site)
        if bracket_valid is False:
            self.invalid.add(site)

    def _merge_and(self, sub: "Trace") -> None:
        """하위 기록 하나를 `note` 를 다시 부른 것과 같은 규칙으로 합친다(자리별 AND · 합집합)."""
        for site, v in sub.sites.items():
            if v is None:
                self.sites.setdefault(site, None)
            else:
                prev = self.sites.get(site)
                self.sites[site] = v if prev in (None, True) else False
        self.unchecked |= sub.unchecked
        self.invalid |= sub.invalid
        self.trial_false |= sub.trial_false

    def add_shot(self, sid: int | None, sub: "Trace") -> None:
        """적분 한 번이 끝났다 — 하위 기록을 AND 로 합치고(오늘의 답), 판정 대기 목록에 둔다. AND 밖 칸
        (`counts` · `fallbacks` · `substituted`)은 그 자리에서 더하고 `settle` 이 다시 건드리지 않는다."""
        self._merge_and(sub)
        for k, n in sub.counts.items():
            self.counts[k] = self.counts.get(k, 0) + n
        for k, n in sub.fallbacks.items():
            self.fallbacks[k] = self.fallbacks.get(k, 0) + n
        self.substituted.update(sub.substituted)
        self.shots.append([sid, sub, "and"])

    def settle(self, accepted_sid: int, since: int = 0) -> bool:
        """C139 — `since` 부터의 적분 중 **받아들인 구조의 적분 하나만** AND 에 남기고, 나머지는 시행 칸으로
        보낸다(`trial_unconverged` · `trial_bracket_invalid`). AND 는 직접 기록(`own`) + 판정된 적분들로 다시 짓는다.

        ⚠ 구조 id 는 살아 있는 객체 사이에서만 유일하다 — 버려진 시행의 구조가 수거된 뒤 같은 id 가 다시
        나올 수 있다. 받아들인 구조는 `settle` 때 살아 있으므로 **같은 id 의 마지막 적분**이 그것이다.
        맞는 적분이 없으면 아무것도 옮기지 않고 `False` 를 돌려준다(오늘의 답 그대로)."""
        if self.own is None:
            return False
        hit = None
        for i in range(len(self.shots) - 1, since - 1, -1):
            if self.shots[i][0] == accepted_sid:
                hit = i
                break
        if hit is None:
            return False
        for i in range(since, len(self.shots)):
            self.shots[i][2] = "and" if i == hit else "trial"
        own = self.own
        self.sites, self.unchecked, self.invalid = dict(own.sites), set(own.unchecked), set(own.invalid)
        self.trial_false, self.trial_invalid = set(own.trial_false), set()
        for _sid, sub, status in self.shots:
            if status == "and":
                self._merge_and(sub)
            else:
                self.trial_false |= {n for n, v in sub.sites.items() if v is False} | sub.trial_false
                self.trial_invalid |= sub.invalid
        return True

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

    def note_substituted(self, site: str, attempt: int, last_deviation: float) -> None:
        """⚠ **이 자리는 `note` 가 아니다.** 예산을 다 쓰고 **앞선 시행**을 답으로 들고 나간
        것은 «수렴하지 않았다» 가 아니다 — 그 시행은 허용오차를 만족한다. `sites` 에 적으면
        `converged` 가 통째로 뒤집혀 사전등록 B 가 금지한 배지가 된다. 그래서 옆 칸이다.
        같은 자리가 두 번이면 **나중 것**이 남는다 (마지막 대체가 답을 정한다)."""
        self.substituted[site] = (attempt, last_deviation)

    @property
    def substituted_sites(self) -> list[str]:
        """예산 소진으로 앞선 시행을 답으로 삼은 자리 — `"자리@시행N"` 꼴."""
        return [f"{name}@시행{self.substituted[name][0]}" for name in sorted(self.substituted)]

    @property
    def bracket_invalid_sites(self) -> list[str]:
        """진입 부호 검사가 실패한 자리 — 상태와 무관하게 싣는다."""
        return sorted(self.invalid)

    @property
    def no_criterion_sites(self) -> list[str]:
        """기준 가지가 없어 상태를 비운 자리."""
        return sorted(n for n, v in self.sites.items() if v is None)


def count(event: str) -> None:
    """현재 풀이의 기록에 사건 하나를 센다(판정 아님). 기록이 없으면 조용히 지나간다."""
    tr = _TRACE.get()
    if tr is not None:
        tr.counts[event] = tr.counts.get(event, 0) + 1


def note_substituted(site: str, attempt: int, last_deviation: float) -> None:
    """현재 풀이의 기록에 대체 한 줄. 기록이 없으면 조용히 지나간다."""
    tr = _TRACE.get()
    if tr is not None:
        tr.note_substituted(site, attempt, last_deviation)


def note(site: str, converged: bool | None, bracket_checked: bool = True,
         bracket_valid: bool | None = None, trial: bool = False) -> None:
    """현재 풀이의 기록에 한 줄. 기록이 없으면(모듈을 직접 부른 경우) 조용히 지나간다."""
    tr = _TRACE.get()
    if tr is not None:
        tr.note(site, converged, bracket_checked, bracket_valid, trial)


def note_fallback(site: str) -> None:
    """C138 F 형 — 대체 길로 가서 제대로 된 답이 났다. «미수렴» 이 아니다: AND 밖, 셈만(`fallback_solvers`)."""
    tr = _TRACE.get()
    if tr is not None:
        tr.fallbacks[site] = tr.fallbacks.get(site, 0) + 1


@contextlib.contextmanager
def start():
    """한 풀이의 기록을 연다. **중첩되면 바깥 것을 그대로 쓴다.**"""
    tr = _TRACE.get()
    if tr is not None:
        yield tr
        return
    tr = Trace(own=Trace())
    token = _TRACE.set(tr)
    try:
        yield tr
    finally:
        _TRACE.reset(token)


@contextlib.contextmanager
def shot():
    """C139 — 적분 한 번의 기록을 하위 기록으로 연다. 들고 나가는 칸 `holder[0]` 에 호출자가 구조 id 를
    적는다(던지면 `None` — 시행이다). 열린 기록이 없으면 `None` 을 내고 아무것도 안 한다."""
    outer = _TRACE.get()
    if outer is None:
        yield None
        return
    assert not outer.in_shot, "C139: an integration ran inside another integration"
    sub = Trace(in_shot=True)
    token = _TRACE.set(sub)
    holder = [None]
    try:
        yield holder
    finally:
        _TRACE.reset(token)
        outer.add_shot(holder[0], sub)


def shot_count() -> int:
    """지금 열린 기록에 쌓인 적분 수(풀이 시작점을 잡는 데 쓴다). 기록이 없으면 0."""
    tr = _TRACE.get()
    return 0 if tr is None else len(tr.shots)


def settle(accepted_sid: int, since: int = 0) -> bool:
    """지금 열린 기록에서 받아들인 적분을 정한다 (`Trace.settle`). 기록이 없으면 `False`."""
    tr = _TRACE.get()
    return False if tr is None else tr.settle(accepted_sid, since)


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
