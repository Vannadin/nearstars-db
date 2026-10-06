# verdict_of 의 네 판정 행 — 답 · 답(속 미수렴) · 불수락 · 거절, interior 결과와 payload.Result 둘 다 (착지 3, 초안 7f2d8d2e §3.1)
"""python3 engine/test_verdict_of.py — one row per verdict kind, plus is_answer and the str form.

Real result: one Earth solve at its default T_pot (답). The other kinds are planted on copies of it or on small
payload.Results, said so in each row:
- 불수락: the draft named Mars 1782.0 K, but C152 note 8 (849874e3) makes that point answer through the continuation,
  so the row plants `converged=False` on the Earth copy, which is what 1782.0 was before note 8;
- 답(속 미수렴): planted `values["converged"] = False` with a solver name (the draft's fallback);
- 거절: an out_of_domain payload.Result (no solve).
"""
from __future__ import annotations

import contextlib
import dataclasses
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import interior  # noqa: E402
from payload import Result, out_of_domain  # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    fails += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


with contextlib.redirect_stdout(io.StringIO()):
    earth = interior.solve(1.0, core_mass_fraction=0.325)

v = interior.verdict_of(earth)
check("답 — 지구 기본 T_pot 풀이(진짜)", v.kind == "답" and v.text == "" and str(v) == "답" and interior.is_answer(earth),
      str(v))
inner = (earth.values or {}).get("converged")
check("지구 풀이의 속 기록이 False 가 아니다(답 행의 전제)", inner is not False, repr(inner))

planted_inner = dataclasses.replace(earth, values={**earth.values, "converged": False, "unconverged_solvers": ["심은_자리"]})
v = interior.verdict_of(planted_inner)
check("답(속 미수렴) — 속 기록 False 를 심은 사본: 답으로 센다, 자리 이름을 든다",
      v.kind == "답(속 미수렴)" and "심은_자리" in v.text and interior.is_answer(planted_inner), str(v))

planted_outer = dataclasses.replace(earth, converged=False)
v = interior.verdict_of(planted_outer)
check("불수락 — 겉 수렴 표지 False 를 심은 사본(옛 1782.0 의 꼴): 답이 아니다, answer_verdict 의 까닭을 든다",
      v.kind == "불수락" and v.text == interior.answer_verdict(planted_outer) and not interior.is_answer(planted_outer)
      and planted_outer.applicable, str(v))  # verdict-ok: 불수락이 거절이 아님을(applicable 은 참) 시험이 확인한다

wall = out_of_domain("test", "1", "벽 — 심은 도메인 밖", {})
v = interior.verdict_of(wall)
check("거절 — 도메인 밖 결과: 답이 아니다, 까닭이 text", v.kind == "거절" and v.text == "벽 — 심은 도메인 밖"
      and str(v) == "거절 — 벽 — 심은 도메인 밖" and not interior.is_answer(wall), str(v))

_kw = dict(recipe="test", version="1", regime="r", reason="까닭", grade="measured", inputs={},
           values={"x": 1.0}, units={"x": ""})
plain = Result(**_kw)
check("순환 밖 payload.Result(converged None) — applicable 만이 가른다: 답", interior.verdict_of(plain).kind == "답",
      str(interior.verdict_of(plain)))
cyc = Result(**_kw, cycles=(1,), converged=False)
v = interior.verdict_of(cyc)
check("순환 위 미수렴 payload.Result — 불수락, «미수렴 1차 통과값»(Result.evidence 의 말)",
      v.kind == "불수락" and v.text == "미수렴 1차 통과값" and not interior.is_answer(cyc), str(v))
tagged = Result(**_kw, unconverged_inputs=("노드.키",))
v = interior.verdict_of(tagged)
check("미수렴 입력을 읽은 payload.Result(C71) — 답(속 미수렴), 그 입력 이름을 든다",
      v.kind == "답(속 미수렴)" and "노드.키" in v.text and interior.is_answer(tagged), str(v))
check("판정 종류는 넷 — VERDICT_KINDS", interior.VERDICT_KINDS == ("답", "답(속 미수렴)", "불수락", "거절"),
      str(interior.VERDICT_KINDS))

print(f"  test_verdict_of — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
