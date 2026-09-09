# 판구조 영역 선언을 읽고 옛 `stagnant_lid` 불리언을 파생한다 — 두 값이 아니라 밴드 + contested (C53)
"""Tectonic regime as a band with named end-members, and the old boolean derived from it.

    from tectonic_regime import derived_stagnant_lid
    derived_stagnant_lid({"value": "mobile", "grade": "declared", "source": "…"}).value   -> False

⚠ **Why this file exists (C53).** Our bodies declared `stagnant_lid: true|false`, and Foley &
Bercovici 2014's abstract (`2014GeoJI.199..580F`) names that shape as the thing it argues against —
*"as opposed to the bimodal distribution of fully mobile lid planets and stagnant lid planets that is
typically assumed"*. The parallel seat's P9 surveyed the classification literature and found **no
scheme that is binary**: the oldest (Solomatov 1995) already had three regimes with *transitional* in
the middle, the yield-stress schemes have mobile/episodic/stagnant, the grain-damage scheme makes the
middle continuous and puts plate tectonics *inside* it, and the review (Lenardic 2018) says tectonic
potential is *"far from binary"* and may be a history rather than a state.

⚠ **The boolean stays, as a derived value, so that no consumer changed shape.** `dynamo_rocky`'s
survival gate is the only place a value reaches an output, and it still reads a three-valued
`True/False/None`. What changed is where that value comes from.

⚠ **And the derived boolean erases what the enum was built to carry — on purpose.** `stagnant` and
`contested` both derive `True`, which is exactly the distinction P9 measured. A consumer that needs
to know a body is contested reads `tectonic_regime`; the derived boolean cannot tell it (C53).

**Grades, and what each one claims**

* `measured` — a source we hold prints this classification *for this body*.
* `analog` — carried from a body classified elsewhere, with that body named.
* `declared` — the owner elected a statement; the schemes disagree, or there is nothing to measure.
* `contested` — the sources disagree in print. ⚠ Travels with `value: contested` and only with it.
"""
from __future__ import annotations

from typing import Any, NamedTuple

#: 이 어휘 밖의 값은 거절된다 (derivation-discipline §7).
REGIMES = ("stagnant", "mobile", "transitional", "episodic", "heat_pipe", "contested")
GRADES = ("measured", "analog", "declared", "contested")

#: 파생 규칙. ⚠ **`contested` → `True` 는 오너 결정 (a), 2026-09-09** — 그 바디에서 다이나모는 실제로
#: 0 이고, 금성형 행성이 실제로 가지는 장은 대기 상층부 이온화가 만드는 **유도 자기권**, 즉 다른
#: 기전이다. `transitional` → `None` 은 기존 cannot-say 경로를 그대로 탄다.
DERIVED: dict[str, bool | None] = {
    "stagnant": True,
    "mobile": False,
    "contested": True,
    "transitional": None,
}

#: ⚠ **매핑이 없다 — 오너 대기.** 로스터의 어느 바디도 이 값을 갖지 않고, 추측은 «주기적으로
#: 판이 움직이는 행성에 다이나모를 줄지» 를 좌석이 결정하는 것이 된다. 후보는 C53 에 적혀 있다.
UNMAPPED = ("episodic", "heat_pipe")

#: `contested` 가 생존 게이트의 라벨에 덧붙이는 한 줄. 유도 자기권은 다른 브랜치이고 이 노드의
#: 몫이 아니라는 사실이 판정과 함께 이동해야 한다 (C53, 오너 결정 (a) 의 라벨 요건).
CONTESTED_NOTE = ("contested → declared-dead; induced magnetosphere is a separate branch "
                  "(magnetosphere_geometry)")


class Derived(NamedTuple):
    """파생 결과. ⚠ `value` 는 `bool` 또는 `None` 이고 `1`/`0` 이 아니다 — 소비처가 동일성으로
    비교하는 자리가 있어서, `int` 는 모든 참·거짓 분기를 통과한 뒤 다른 곳에서 틀린다."""

    value: bool | None
    note: str
    refusal: str | None = None      # 이름 붙은 거절 문구. 있으면 `value` 는 읽지 않는다.
    label: str | None = None        # 생존 게이트의 라벨에 **덧붙는** 한 줄. contested 만 갖는다.


def _refuse(text: str) -> Derived:
    return Derived(None, text, text)


def derived_stagnant_lid(regime: Any, legacy: Any = None) -> Derived:
    """`tectonic_regime` 선언에서 옛 불리언을 파생한다. 거절은 예외가 아니라 반환값이다 (§2).

    `legacy` 는 같은 바디에 남아 있는 옛 `stagnant_lid` 선언이다 (`state.get_optional` 로 읽어
    미스가 설계임을 호출부가 선언한다). ⚠ **둘 다 선언되어 있으면 어느 쪽도 고르지 않는다** —
    한 양을 두 곳에서 선언하는 것이 C49 가 열려 있는 모양이고, 여기서 네 번째 사례를 만들지 않는다.
    """
    if regime is not None and legacy is not None:
        return _refuse("`tectonic_regime` 과 옛 `stagnant_lid` 가 같은 바디에 둘 다 선언되어 있다 "
                       f"(regime {regime!r} · stagnant_lid {legacy!r}) — 어느 쪽도 고르지 않는다. "
                       "옛 키를 지우고 `tectonic_regime` 만 남겨라 (C53)")
    if regime is None:
        if legacy is not None:
            return _refuse("옛 `stagnant_lid` 만 선언되어 있다 — 이 노드는 `tectonic_regime` 을 읽는다. "
                           "옛 키를 새 키로 바꿔라 (C53)")
        return Derived(None, "tectonic_regime 선언이 없다 — 판정 불가는 기본값이 아니다")

    if not isinstance(regime, dict):
        return _refuse(f"`tectonic_regime` 은 값·등급·출처를 담은 블록이어야 한다 — {type(regime).__name__} "
                       f"({regime!r}) 이 왔다. 문자열 하나는 등급과 출처를 말하지 않는다 (C53)")

    value = regime.get("value")
    grade = regime.get("grade")
    source = regime.get("source")
    if value not in REGIMES:
        return _refuse(f"`tectonic_regime.value` «{value}» 는 이 어휘에 없다 — {' · '.join(REGIMES)}")
    if grade not in GRADES:
        return _refuse(f"`tectonic_regime.grade` «{grade}» 는 이 어휘에 없다 — {' · '.join(GRADES)}")
    if not source:
        return _refuse(f"«{value}» 선언에 `source` 가 없다 — 누가 그렇게 말하는지 없이는 등급이 뜻이 없다")
    if (value == "contested") != (grade == "contested"):
        return _refuse(f"`value` «{value}» 와 `grade` «{grade}» 가 어긋난다 — 등급 contested 는 "
                       "값 contested 와만 함께 이동한다 (출처들이 인쇄물에서 서로 다르다는 뜻)")

    if value in UNMAPPED:
        return _refuse(f"no derived-boolean mapping is declared for regime «{value}» — owner pending "
                       "(후보는 C53 에 기록되어 있고 이 노드가 고르지 않는다)")

    note = f"derived from tectonic_regime «{value}» (grade {grade}, {source})"
    # ⚠ 라벨에 한 줄이 덧붙는 것은 `contested` 뿐이다 (C53 의 등록된 요건). 다른 값에 덧붙이면
    #   오늘의 출력이 문구까지 바뀌고, 그러면 «소비처는 안 움직였다» 를 회귀로 증명할 수 없다.
    label = CONTESTED_NOTE if value == "contested" else None
    return Derived(DERIVED[value], note, None, label)
