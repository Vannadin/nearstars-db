# C53 테스트 — 영역 밴드가 옛 불리언을 파생하고, 세 로스터 바디의 출력이 비트 동일함을 증명한다
"""The registered regressions for `tectonic_regime.py` (C53, Brief 168 B).

    python3 engine/test_tectonic_regime.py      # the gate; ~12 s, of which Pandora's solve is ~8.5 s

⚠ **These three assertions were written before the code** and are registered at
`engine/interior-core.md@«**Three assertions, written before the code:**»`:

1. the three roster bodies' derived booleans equal today's values bit for bit — Earth `False`,
   Mars `True`, Pandora `False`;
2. `contested` → `True` → the gate's `DEAD_LID`, `dipole_moment == 0.0`; `transitional` → `None` →
   the gate's `UNDECIDED_LID`, **not** dead;
3. `episodic` and `heat_pipe` raise the named refusal rather than defaulting to anything.

⚠ **Assertion 2 is hung on identity with `dynamo_rocky.DEAD_LID` / `UNDECIDED_LID`, never on the
literal text** (amendment to the pre-registration). A test that retypes the sentence keeps passing
while the label drifts underneath it, and the label strings do not change in Brief 168.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yaml                            # noqa: E402
import dynamo_rocky as dr              # noqa: E402
import tectonic_regime as tect         # noqa: E402

fails = 0


def row(ok, text):
    global fails
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


def declared(body: str):
    """바디 파일이 선언한 `tectonic_regime` 블록. 파일이 원전이고 이 시험은 그것을 읽는다."""
    doc = yaml.safe_load((Path(__file__).resolve().parent / "bodies" / f"{body}.yaml").read_text(encoding="utf-8"))
    return doc["inputs"].get("tectonic_regime"), doc["inputs"].get("stagnant_lid")


print("① 등록된 단정 1 — 세 로스터 바디의 파생 불리언이 오늘의 값과 비트 동일하다")
# ⚠ 오늘의 값은 이 파일이 기억하는 수가 아니라 **브리프 168 B 전에 측정된 것**이다: 지구 False ·
#   화성 True · 판도라 False (2026-09-09, 커밋 3c5ede48 위에서 세 바디를 실제로 풀어 읽었다).
BEFORE = {"earth": False, "mars": True, "pandora": False}
for body, was in BEFORE.items():
    regime, legacy = declared(body)
    got = tect.derived_stagnant_lid(regime, legacy)
    row(got.refusal is None and got.value is was,
        f"{body}: tectonic_regime «{(regime or {}).get('value')}» → 파생 {got.value!r} · 168 B 전 {was!r} "
        f"— {'같다' if got.value is was else '다르다'} (`is` 로 비교: 타입까지 같다)")
    row(type(got.value) is bool,
        f"{body}: 파생값의 타입이 `bool` 이다 ({type(got.value).__name__}) — `1`/`0` 은 모든 참·거짓 "
        "분기를 통과한 뒤 동일성 비교에서만 틀린다")
    row(legacy is None,
        f"{body}: 옛 `stagnant_lid` 키가 바디 파일에서 사라졌다 — 파생값은 노드 안에서만 살고 "
        "바디 파일에 되쓰이지 않는다")

print("\n② 등록된 단정 2 — contested 는 dead, transitional 은 cannot-say (문자열이 아니라 상수 동일성으로)")
LADDER = dict(mass_earth=1.0, radius_earth=1.0, conductor_phase="liquid_outer_solid_inner",
              age_gyr=4.54)
cont = tect.derived_stagnant_lid({"value": "contested", "grade": "contested", "source": "P9 (다섯 인쇄 분류)"})
row(cont.value is True, f"contested → 파생 {cont.value!r} (오너 결정 (a))")
r = dr.ladder(stagnant_lid=cont.value, lid_note=cont.label, **LADDER)
row(r.values["regime"] == dr.DEAD_LID,
    f"contested → 게이트가 `dynamo_rocky.DEAD_LID` 를 돌려준다 (동일성, 축자 아님): «{r.values['regime']}»")
row(r.values["dipole_moment"] == 0.0 and r.values["b_eq"] == 0.0 and r.values["b_pol"] == 0.0,
    f"contested → 세 필드가 0 이다 (ℳ {r.values['dipole_moment']} · B_eq {r.values['b_eq']} · "
    f"B_pol {r.values['b_pol']}) — 오너 사유: 그 바디의 다이나모는 실제로 0 이다")
row(any(tect.CONTESTED_NOTE in n for n in r.notes),
    "contested → 라벨에 한 줄이 덧붙는다: 유도 자기권은 다른 브랜치(`magnetosphere_geometry`)이고 "
    "이 노드의 몫이 아니다 (결정 (a) 의 라벨 요건)")

trans = tect.derived_stagnant_lid({"value": "transitional", "grade": "declared", "source": "F&B 2014 체계"})
row(trans.value is None, f"transitional → 파생 {trans.value!r}")
rt = dr.ladder(stagnant_lid=trans.value, lid_note=trans.label, **LADDER)
row(rt.values["regime"] == dr.UNDECIDED_LID,
    f"transitional → 게이트가 `dynamo_rocky.UNDECIDED_LID` 를 돌려준다, **dead 가 아니다**: «{rt.values['regime']}»")
row(rt.values["dipole_moment"] is None and not rt.values["regime"].startswith("dead"),
    f"transitional → ℳ 은 0 이 아니라 None 이다 ({rt.values['dipole_moment']!r}) — 판정 불가는 기본값이 아니다")
row(trans.label is None and cont.label is not None,
    "덧붙는 라벨은 contested 만 갖는다 — 다른 값에 붙이면 오늘의 출력이 문구까지 바뀐다")

print("\n③ 등록된 단정 3 — episodic·heat_pipe 는 이름을 대며 거절한다 (기본값으로 떨어지지 않는다)")
for value in tect.UNMAPPED:
    got = tect.derived_stagnant_lid({"value": value, "grade": "declared", "source": "P9"})
    row(got.refusal is not None and value in got.refusal and "owner pending" in got.refusal,
        f"«{value}» → 거절, 이름이 문구에 있다: «{got.refusal[:78]}…»")
    row(got.value is None and value not in tect.DERIVED,
        f"«{value}» 는 파생표에 아예 없다 — 후보는 C53 에 적혀 있고 이 코드가 고르지 않는다")

print("\n④ 어휘가 실재한다 — 밖의 값·등급·모양을 거절한다 (derivation-discipline §7)")
CASES = (
    ({"value": "plate_tectonics", "grade": "measured", "source": "x"}, "value"),
    ({"value": "mobile", "grade": "guessed", "source": "x"}, "grade"),
    ({"value": "mobile", "grade": "declared"}, "source"),
    ({"value": "contested", "grade": "declared", "source": "x"}, "어긋난다"),
    ({"value": "mobile", "grade": "contested", "source": "x"}, "어긋난다"),
    ("stagnant", "블록이어야"),
)
for payload, needle in CASES:
    got = tect.derived_stagnant_lid(payload)
    row(got.refusal is not None and needle in got.refusal,
        f"{payload if isinstance(payload, str) else payload.get('value')}"
        f"{'' if isinstance(payload, str) else '/' + str(payload.get('grade'))} → 거절 «{needle}»")

print("\n⑤ 한 양을 두 곳에서 선언하는 것 — 어느 쪽도 고르지 않는다 (C49 의 모양을 늘리지 않는다)")
both = tect.derived_stagnant_lid({"value": "mobile", "grade": "declared", "source": "x"}, False)
row(both.refusal is not None and "둘 다 선언" in both.refusal,
    f"둘 다 선언 → 거절: «{both.refusal[:88]}…»")
old_only = tect.derived_stagnant_lid(None, True)
row(old_only.refusal is not None and "옛 `stagnant_lid` 만" in old_only.refusal,
    f"옛 키만 선언 → 거절: «{old_only.refusal[:78]}…»")
absent = tect.derived_stagnant_lid(None, None)
row(absent.refusal is None and absent.value is None,
    f"둘 다 없음 → 거절이 아니라 판정 불가 ({absent.value!r}) — 오늘 미선언 바디가 받던 처분 그대로")

print("\n⑥ 사다리의 도메인 게이트가 먼저다 (C28 의 불변식, 168 C)")
# ⚠ 순서가 뒤집히면 300 M⊕ 거대행성이 나쁜 판구조 블록을 들었을 때 «암석 사다리 밖이다» 대신 C53
#   문구를 받는다 — 이 사다리가 판정하지도 않는 바디에 대해 뚜껑 이야기를 하는 것이다.
from state import BodyState as _BS                                          # noqa: E402
BAD = {"value": "nope", "grade": "declared", "source": "probe"}
giant = dr._from_state(_BS(name="probe-giant", kind="planet", inputs={
    "mass_earth": 300.0, "radius_earth": 11.2, "body_class": "giant", "age_gyr": 5.0,
    "tectonic_regime": BAD}))
row(not giant.applicable and "암석 사다리 밖이다" in giant.reason and "tectonic_regime" not in giant.reason,
    f"거대행성 300 M⊕ + 나쁜 판구조 블록 → 사다리 밖 문구를 지킨다: «{giant.reason[:60]}…»")
rocky = dr._from_state(_BS(name="probe-rocky", kind="planet", inputs={
    "mass_earth": 1.0, "radius_earth": 1.0, "body_class": "rocky", "age_gyr": 4.5,
    "composition_intent": "earth_like", "tectonic_regime": BAD}))
row(not rocky.applicable and "이 어휘에 없다" in rocky.reason,
    f"암석체 + 나쁜 블록 → 그때는 C53 이 말한다: «{rocky.reason[:60]}…»")

print("\n⑦ 판정 불가에 이유가 붙는다 — «선언 없음» 과 «transitional» 이 출력에서 갈린다 (168 C)")
un_declared = dr._from_state(_BS(name="probe-none", kind="planet", inputs={
    "mass_earth": 1.0, "radius_earth": 1.0, "body_class": "rocky", "age_gyr": 4.5,
    "conductor_phase": "liquid", "composition_intent": "earth_like"}))
un_trans = dr._from_state(_BS(name="probe-trans", kind="planet", inputs={
    "mass_earth": 1.0, "radius_earth": 1.0, "body_class": "rocky", "age_gyr": 4.5,
    "conductor_phase": "liquid", "composition_intent": "earth_like",
    "tectonic_regime": {"value": "transitional", "grade": "declared", "source": "F&B 2014 체계"}}))
row(un_declared.values["regime"] == dr.UNDECIDED_LID and un_trans.values["regime"] == dr.UNDECIDED_LID,
    "둘 다 `UNDECIDED_LID` 로 나온다 — 판정 문자열은 168 에서 바뀌지 않는다")
row(any("선언이 없다" in n for n in un_declared.notes)
    and any("transitional" in n for n in un_trans.notes),
    "그러나 이유는 노트에서 갈린다: «tectonic_regime 선언이 없다» 대 «derived … «transitional»»")

print("\n⑧ 바디 회귀 — 판도라를 실제로 풀어 두 필드를 자릿수까지 대조한다 (~8.5 s)")
# ⚠ 지구는 넣지 않는다: 같은 검사를 71 초에 산다. 판도라가 8.5 초이고 이 두 수는 168 B 전에 측정된 것이다.
import registry                                                             # noqa: E402
import run as _run                                                          # noqa: E402
registry.load_all()
_g = _run.load_chain()
_st, _ = _run.load_body(Path(__file__).resolve().parent / "bodies" / "pandora.yaml")
_run.solve(_st, _g)
_res = _st.results["dynamo_rocky"]
row(_res.values["b_eq"] == 41.37252479971432 and _res.values["b_pol"] == 82.74504959942864,
    f"판도라 B_eq {_res.values['b_eq']!r} · B_pol {_res.values['b_pol']!r} — 168 B 전 값과 자릿수까지 같다")
row(_res.values["dipole_moment"] == 1.0 and _res.values["regime"] == "undeclared (both emitted)",
    f"판도라 ℳ {_res.values['dipole_moment']!r} · 판정 «{_res.values['regime']}» — 그대로다")

print("\n기록 — 화성의 True 는 오늘 판정을 지지하지 않는다 (판정 아님, 168 B 측정)")
print("      화성의 생존 게이트는 `conductor_phase 'undecided'` 에서 먼저 멈춘다 — 뚜껑 분기 앞이다.")
print("      그래서 화성의 답은 `cannot-say (conductor_phase undecided)` 이고 `DEAD_LID` 가 아니며,")
print("      선언이 stagnant 든 contested 든 오늘의 화성 출력은 같다. 위 ② 는 그래서 게이트 함수를")
print("      고정 입력으로 시험하고, 바디로 시험하지 않는다.")

print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
