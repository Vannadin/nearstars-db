# 레시피 반환 계약 — 값만이 아니라 입력·regime·판정이유·신뢰등급·근거를 함께 들고 다닌다
"""The return contract every recipe honours.

A recipe does not return a number. It returns a `Result` carrying, alongside
the values, the exact inputs it consumed, the regime it took, a machine-written
reason for that regime, a confidence grade, and its grounding refs.

Three things follow from that, and they are the whole point:

1. **Staleness is detectable.** `inputs` records what the value was computed
   from, so a change upstream can be compared against it instead of remembered.
2. **The explanation cannot drift.** `reason` is written at the branch that
   made the decision, so it can never describe a different calculation than the
   one that ran. Hand-written evidence prose drifts; this cannot.
3. **Out of domain is a result, not a crash.** A recipe asked about a body it
   does not cover returns a Result with no values, the regime `out-of-domain`,
   and a reason naming the recipe that does cover it. Misapplication is the
   failure mode we most need to make loud, so it gets a first-class return.

`Result.evidence()` renders the one-line sentence a Phase 4 board row carries,
generated rather than typed.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# chain.yaml 의 grades 와 같은 어휘를 쓴다.
# authored (2026-09-04, 오너 결정 — engine/AUTHORED-VALUES-POLICY.md): 이 프로젝트가 공급한 값. 어느 보유 출처도
# 주지 않으며, 근거 있는 것과 모순되지 않는다. judgment(발표된 선택지 사이의 판단)와 섞지 않는다.
GRADES = ("measured", "calibrated", "analog", "judgment", "authored")
# authored 결과가 notes 에 반드시 달아야 하는 두 표지. 없으면 생성 시점에 거절한다.
AUTHORED_MARKERS = ("gap:", "consistent-with:")

OUT_OF_DOMAIN = "out-of-domain"


@dataclass(frozen=True)
class Result:
    recipe: str                       # 방법론 문서 slug
    version: str                      # 레시피 버전. 바뀌면 캐시된 값이 낡은 것
    regime: str                       # 어느 분기를 탔는가
    reason: str                       # 그 분기를 고른 이유 (분기 자리에서 생성)
    grade: str                        # measured | calibrated | analog | judgment | authored
    inputs: dict[str, Any]            # 소비한 입력 전부
    values: dict[str, Any] = field(default_factory=dict)
    units: dict[str, str] = field(default_factory=dict)
    refs: tuple[str, ...] = ()
    cycles: tuple[int, ...] = ()      # chain.yaml 에 선언된 순환 id
    converged: bool | None = None     # 순환 위에 있을 때만 의미가 있다
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.grade not in GRADES:
            raise ValueError(f"grade '{self.grade}' 는 {GRADES} 밖")
        if self.grade == "authored":
            joined = " ".join(self.notes)
            missing = [m for m in AUTHORED_MARKERS if m not in joined]
            if missing:
                raise ValueError(f"{self.recipe}: authored 값에는 notes 에 {AUTHORED_MARKERS} 가 다 있어야 한다 — 없는 것 {missing}")
        if self.regime != OUT_OF_DOMAIN and not self.values:
            raise ValueError(f"{self.recipe}: 도메인 안인데 값이 비었다")
        for k in self.values:
            if k not in self.units:
                raise ValueError(f"{self.recipe}: '{k}' 에 단위가 없다")
        if self.cycles and self.converged is None:
            raise ValueError(f"{self.recipe}: 순환 위에 있는데 converged 가 없다")

    @property
    def applicable(self) -> bool:
        return self.regime != OUT_OF_DOMAIN

    def evidence(self) -> str:
        """Phase 4 보드 행이 싣는 한 줄. 손으로 쓰지 않고 생성한다."""
        if not self.applicable:
            return f"{self.recipe} 적용 불가 — {self.reason}"
        vals = " · ".join(
            f"{k} {_fmt(v)} {self.units[k]}".strip() for k, v in self.values.items()
        )
        line = f"{vals} ({self.recipe} v{self.version}, {self.regime}; {self.reason})"
        if self.cycles and not self.converged:
            line += " ⚠ 미수렴 1차 통과값"
        return line

    def stale_against(self, current: dict[str, Any], tol: float = 1e-9) -> list[str]:
        """기록된 입력과 현재 값을 대조해 어긋난 입력 이름을 돌려준다.

        비어 있으면 이 결과는 여전히 유효하다. 이게 cascade 추적을 기억이
        아니라 대조로 바꾸는 자리다."""
        drifted = []
        for k, was in self.inputs.items():
            if k not in current:
                continue
            now = current[k]
            if isinstance(was, (int, float)) and isinstance(now, (int, float)):
                scale = max(abs(was), abs(now), 1e-30)
                if abs(was - now) / scale > tol:
                    drifted.append(k)
            elif was != now:
                drifted.append(k)
        return drifted


def out_of_domain(recipe: str, version: str, reason: str,
                  inputs: dict[str, Any], refs: tuple[str, ...] = (),
                  notes: tuple[str, ...] = ()) -> Result:
    """도메인 밖 결과. 예외가 아니라 값이다 — 오적용은 조용히 넘어가면 안 된다."""
    return Result(recipe=recipe, version=version, regime=OUT_OF_DOMAIN,
                  reason=reason, grade="judgment", inputs=inputs,
                  refs=refs, notes=notes)


def _fmt(v: Any) -> str:
    if isinstance(v, float):
        if v == 0:
            return "0"
        if abs(v) >= 1e5 or abs(v) < 1e-3:
            return f"{v:.3g}"
        return f"{v:,.4g}"
    return str(v)
