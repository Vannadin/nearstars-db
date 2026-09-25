# 페이로드 등급 계약 테스트 — authored 등급은 두 표지(gap:, consistent-with:) 없이는 생성되지 않는다
"""Grade-vocabulary contract of `payload.Result` (engine/AUTHORED-VALUES-POLICY.md, 2026-09-04).

    python3 engine/test_payload.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from payload import GRADES, GRADE_WORDS, INPUT_GRADES, AUTHORED_MARKERS, Result  # noqa: E402

fails = 0


def row(ok, text):
    global fails
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


def make(grade, notes=()):
    return Result(recipe="test", version="0", regime="test", reason="test", grade=grade,
                  inputs={}, values={"x": 1.0}, units={"x": "—"}, notes=notes)


print("등급 어휘 — chain.yaml 의 grades 와 같은 다섯")
row(GRADES == ("measured", "calibrated", "analog", "judgment", "authored"), f"GRADES = {GRADES}")
row(AUTHORED_MARKERS == ("gap:", "consistent-with:"), f"표지 = {AUTHORED_MARKERS}")
row(GRADE_WORDS == ("measured", "literature", "analog", "derived", "judgment", "declared", "inherited", "authored",
                    "calibrated"), f"GRADE_WORDS = {GRADE_WORDS} (prereg-grade-vocabulary §1 ①)")
row(INPUT_GRADES == tuple(g for g in GRADE_WORDS if g != "calibrated") and set(GRADES) <= set(GRADE_WORDS),
    f"INPUT_GRADES = {INPUT_GRADES} · GRADES ⊂ GRADE_WORDS")

print("\nauthored — 두 표지가 다 있어야 생성된다")
ok = True
try:
    make("authored", ("gap: no held source gives it (cache + ADS searched 2026-09-04)",
                      "consistent-with: sits inside the published bound X"))
except ValueError:
    ok = False
row(ok, "gap: + consistent-with: → 생성")
for label, notes in (("표지 없음", ()), ("gap 만", ("gap: …",)), ("consistent-with 만", ("consistent-with: …",))):
    try:
        make("authored", notes); ok = False
    except ValueError as e:
        ok = "authored" in str(e)
    row(ok, f"{label} → 거절")

print("\njudgment 는 그대로 — 표지 없이 생성된다 (발표된 선택지 사이의 판단)")
ok = True
try:
    make("judgment")
except ValueError:
    ok = False
row(ok, "judgment, notes 없음 → 생성")
try:
    make("invented"); ok = False
except ValueError:
    ok = True
row(ok, "어휘 밖 등급 → 거절")

# ── C71 — 미수렴 입력은 등급에 상한을 씌운다 ──────────────────────────────────
#
# ⚠ **상한이지 강등이 아니다.** `min(자기 등급, judgment)` 이므로 사다리에서 judgment 위면
#   내려가고, 이미 아래(authored)면 그대로다. 그 둘을 한 시험에서 같이 본다 — 하나만 보면
#   «내려간다» 와 «judgment 로 덮어쓴다» 가 구별되지 않는다.
print("\nC71 — 미수렴 입력의 등급 상한")


def tagged(grade, notes=(), marks=("interior_layers.radius",)):
    return Result(recipe="test", version="0", regime="test", reason="test", grade=grade,
                  inputs={}, values={"x": 1.0}, units={"x": "—"}, notes=notes,
                  unconverged_inputs=marks)


row(make("measured").grade == "measured" and make("measured").unconverged_inputs == (),
    "표지 없음 → 등급 그대로, 필드는 빈 튜플 (대조)")
row(tagged("measured").grade == "judgment", "measured + 미수렴 입력 → judgment 로 상한")
row(tagged("calibrated").grade == "judgment", "calibrated + 미수렴 입력 → judgment 로 상한")
row(tagged("judgment").grade == "judgment", "judgment 는 제자리")
_auth = tagged("authored", ("gap: …", "consistent-with: …"))
row(_auth.grade == "authored", "authored 는 judgment 아래라 그대로 — 상한은 올리지 않는다")
row(any("unconverged input: interior_layers.radius" in n for n in _auth.notes),
    "표지가 notes 에 남는다 (병합: 기존 표지 둘과 함께 셋)")
row(len(_auth.notes) == 3, "병합은 단조 — 기존 표지를 지우지 않는다")
_two = tagged("measured", marks=("interior_layers.radius", "interior_layers.core_radius"))
row(len([n for n in _two.notes if n.startswith("unconverged input: ")]) == 2,
    "입력 둘이면 표지 둘")
row("등급 상한 judgment" in tagged("measured").evidence(),
    "증거 한 줄이 그 사실을 인쇄한다 — 등급이 내려가고 아무 데도 안 보이면 배선이 죽은 것")
row("등급 상한 judgment" not in make("measured").evidence(),
    "표지 없는 결과의 증거 줄은 안 바뀐다 (대조)")

# ── C71 — 조회 창구에서 표지까지, 끝에서 끝까지 ─────────────────────────────
#
# ⚠ 위 시험들은 표지를 **손으로** 넣었다. 그것만으로는 「조회 창구가 미수렴 결과를 알아본다」 가
#   안 걸린다 — 배선이 죽어 있어도 전부 통과한다. 그래서 여기서는 상태를 짓고 **실제로 읽는다**.
print("\nC71 — 조회에서 표지까지")

from state import BodyState                                          # noqa: E402
from payload import tagged_with_unconverged                          # noqa: E402


def _state(converged):
    st = BodyState(name="fixture", kind="planet")
    st.record("interior_layers", Result(
        recipe="interior-structure", version="0", regime="solved", reason="fixture",
        grade="calibrated", inputs={}, values={"radius": 1.13}, units={"radius": "R_earth"},
        cycles=(1,), converged=converged))
    return st


def _consumer_result(st):
    st.current_node = "tidal_heating"
    st["radius"]                       # 실제 조회 — 이 한 줄이 생산자를 기록하게 한다
    return tagged_with_unconverged(
        Result(recipe="tidal-heating", version="0", regime="fixed_q", reason="fixture",
               grade="measured", inputs={}, values={"power": 1.0}, units={"power": "W"}), st)


_un = _consumer_result(_state(False))
row(_un.unconverged_inputs == ("interior_layers.radius",),
    "미수렴 결과에서 읽은 값 → 표지가 «노드.키» 로 붙는다")
row(_un.grade == "judgment", "그 소비자의 등급에 상한이 걸린다")
_ok = _consumer_result(_state(True))
row(_ok.unconverged_inputs == () and _ok.grade == "measured",
    "수렴한 결과에서 읽으면 표지도 상한도 없다 (음성 대조)")
_never = _state(False)
_never.current_node = "tidal_heating"
row(tagged_with_unconverged(
        Result(recipe="t", version="0", regime="r", reason="f", grade="measured",
               inputs={}, values={"power": 1.0}, units={"power": "W"}), _never
    ).unconverged_inputs == (),
    "읽지 않은 소비자는 표지를 안 받는다 — 표지는 조회를 따라간다")
row(BodyState.log_enabled(),
    "조회 로그가 켜져 있다 — 꺼져 있으면 위 빈 튜플들이 «미수렴 없음» 과 구별되지 않는다")

print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
