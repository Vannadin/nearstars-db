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

from dataclasses import dataclass, field, replace
from typing import Any

# chain.yaml 의 grades 와 같은 어휘를 쓴다.
# authored (2026-09-04, 오너 결정 — engine/AUTHORED-VALUES-POLICY.md): 이 프로젝트가 공급한 값. 어느 보유 출처도
# 주지 않으며, 근거 있는 것과 모순되지 않는다. judgment(발표된 선택지 사이의 판단)와 섞지 않는다.
GRADES = ("measured", "calibrated", "analog", "judgment", "authored")
# 등급 낱말 단일 목록 (prereg-grade-vocabulary §1, 오너 2026-09-25 «목록은 통일»). 결과(`GRADES`)와 입력
# (`INPUT_GRADES`)은 이 목록의 부분집합 둘이다 — calibrated 는 결과 전용, 입력 칸에 쓰면 거절.
GRADE_WORDS = ("measured", "literature", "analog", "derived", "judgment", "declared", "inherited", "authored",
               "calibrated")
INPUT_GRADES = tuple(g for g in GRADE_WORDS if g != "calibrated")
assert set(GRADES) <= set(GRADE_WORDS)
#: 세 칸 검사(`check_provenance`)를 받는 새 입력 칸 이름. 층 일반화 ⓐ–ⓓ 가 칸을 만들 때 한 줄씩 더한다.
NEW_PROVENANCE_FIELDS: tuple[str, ...] = ("lithosphere_thickness_km",      # ⓑ1 prereg-surface-lithosphere
                                         "core_light_elements")          # ⓒ1 prereg-core-light-elements


def check_provenance(field_name: str, entry: Any) -> None:
    """새 입력 칸 하나의 세 칸(grade · source · counter_evidence_searched)을 본다 — 오너 원칙 09-24.
    어긋나면 칸 이름을 대고 ValueError."""
    if not isinstance(entry, dict):
        raise ValueError(f"`{field_name}` 은 value · grade · source · counter_evidence_searched 블록이어야 한다")
    grade = entry.get("grade")
    if grade not in INPUT_GRADES:
        raise ValueError(f"`{field_name}.grade` «{grade}» 는 입력 등급이 아니다 — {' · '.join(INPUT_GRADES)}")
    for key in ("source", "counter_evidence_searched"):
        if not entry.get(key):
            raise ValueError(f"`{field_name}` 에 `{key}` 가 없다")

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
    #: 이 결과를 지으면서 읽은 값 가운데 **미수렴 결과에서 온 것들** — `"노드.키"` 꼴 (C71).
    #: 비어 있지 않으면 아래 `__post_init__` 이 등급에 상한을 씌운다.
    #: ⚠ **`converged` 와 다른 질문이다.** `converged` 는 «내가 수렴했나», 이쪽은 «내가 읽은
    #:   값이 수렴한 풀이에서 왔나» 다. 한 필드로 합치면 그 둘이 구별되지 않는다.
    unconverged_inputs: tuple[str, ...] = ()
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
        # ⚠ **미수렴 입력을 읽었으면 등급에 상한이 걸린다** (C71, 지휘 결정 2026-09-16).
        #   규칙은 **상한**이지 강등이 아니다 — `min(자기 등급, judgment)` 이므로 사다리에서
        #   `judgment` 위면 내려가고, 이미 그 아래(`authored`)면 그대로다. 새 등급은 안 만든다.
        #   ⚠ **병합은 단조 최소다**: 표지는 전부 `notes` 에 남고, 등급은 적용되는 상한들의
        #   최소다. 순서가 판정을 바꾸지 않는다 — 어느 상한이 «이긴다» 는 규칙이 없다.
        if self.unconverged_inputs:
            cap = GRADES.index("judgment")
            if GRADES.index(self.grade) < cap:
                object.__setattr__(self, "grade", GRADES[cap])
            marks = tuple(f"unconverged input: {s}" for s in self.unconverged_inputs
                          if f"unconverged input: {s}" not in self.notes)
            if marks:
                object.__setattr__(self, "notes", self.notes + marks)

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
        if self.unconverged_inputs:
            line += (" ⚠ 미수렴 입력에서 온 값 — 등급 상한 judgment ("
                     + " · ".join(self.unconverged_inputs) + ")")
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


def tagged_with_unconverged(result: "Result", state) -> "Result":
    """조회 창구가 본 미수렴 입력을 결과에 실어 돌려준다 (C71).

    ⚠ **레시피의 순수한 부분은 그대로 둔다.** 등급을 아는 것은 «무엇을 읽었는가» 이고, 그것을
    아는 것은 `state` 뿐이다. 그래서 `@recipe` 어댑터가 마지막에 이 함수를 통과시킨다.
    ⚠ **읽은 것이 없으면 같은 객체를 그대로 돌려준다** — 표지 없는 결과에는 필드가 안 붙고,
    골든 값도 안 움직인다."""
    marks = state.unconverged_reads()
    if not marks:
        return result
    return replace(result, unconverged_inputs=marks)


def _fmt(v: Any) -> str:
    if isinstance(v, float):
        if v == 0:
            return "0"
        if abs(v) >= 1e5 or abs(v) < 1e-3:
            return f"{v:.3g}"
        return f"{v:,.4g}"
    return str(v)
