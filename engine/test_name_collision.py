# 내보내는 이름이 바디 선언 이름과 겹치는가 — `state` 가 한 이름공간이라 겹치면 조용히 뒤집힌다
"""Names a recipe emits must not collide with names a body declares.

    python3 engine/test_name_collision.py

`State` resolves declarations and node outputs through one lookup (`State.get` 하나가 둘을 다 찾는다), and
`interior._declared_value` returns a bare scalar unchanged — so a value we emitted can be read
back as if a body had declared it. On 2026-09-22 that killed `run.py bodies/dante_fixture.yaml`:
`interior.solve` emitted `core_plus_layer_radius_km` as a named cannot-say sentence, the sulphur
path read it as a declaration and `float()` raised.

⚠ **The loud case is the narrow one.** On Mars the same key carried a number (1842 km), `float()`
accepted it, and nothing complained. The collision was there either way; only the string made it
visible.

The ruler: every key a contract declares under `Returns`, against every key any body declares
under `inputs`. The intersection must be empty apart from the four frozen below.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

#: `check_contracts` 가 계약 블록을 읽는 그 정규식 — 계약 블록을 두 자로 읽지 않는다.
LINE = re.compile(r"^\*\*(Returns|Needs|Declared-optional)\*\*\s*[—-]\s*(.+?)(?=\n\s*\n|\n\*\*|\Z)",
                  re.S | re.M)
KEY = re.compile(r"`([a-z_][a-z0-9_]*)`")

#: ⚠ **이미 겹치고 있던 넷** (2026-09-22 측정). 사유는 **두 종이고 섞지 않는다** — 아는 것과
#:   안 아는 것을 한 칸에 넣으면 목록이 줄어드는지 아무도 못 본다.
#: ⚠ **설계** 둘 — 계약 문서가 직접 적는다: *"The last two Returns keys are also Needs keys.
#:   Declared, they pass through unchanged; undeclared, this node infers them from mass and radius
#:   and returns what it solved, so a consumer reads one key either way."*
#:   (docs/reference/interior-structure-methodology.md@«Declared, they pass through unchanged»). 겹침이 결함이
#:   아니라 **계약**이고, 꼴도 한쪽으로 고정돼 있다.
#: ⚠ **미조사** 둘 — 이 항목이 만든 것이 아니라 여기서 판정하지 않는다. **이쪽이 줄어드는 것이
#:   보여야 한다.**
DESIGNED = "설계 — 선언이 그대로 통과하고, 없으면 이 노드가 풀어서 같은 키로 돌려준다 (계약 문서)"
UNEXAMINED = "조사 안 함 (2026-09-22)"
ALLOWED = {
    "core_mass_fraction": DESIGNED,
    "ice_mass_fraction": DESIGNED,
    "dynamo_alive": UNEXAMINED,
    "rotation_period_h": UNEXAMINED,
}


def declared_keys() -> set[str]:
    out: set[str] = set()
    for path in sorted((ROOT / "engine" / "bodies").glob("*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        out |= set(doc.get("inputs") or {})
    return out


def returned_keys() -> set[str]:
    out: set[str] = set()
    for path in sorted((ROOT / "docs" / "reference").glob("*.md")):
        for kind, body in LINE.findall(path.read_text(encoding="utf-8")):
            if kind == "Returns":
                out |= set(KEY.findall(body))
    return out


def main() -> int:
    declared, returned = declared_keys(), returned_keys()
    overlap = declared & returned
    new = sorted(overlap - set(ALLOWED))
    gone = sorted(set(ALLOWED) - overlap)

    fails = []
    for name in new:
        fails.append(f"1: `{name}` 를 레시피가 내보내고 바디가 선언한다 — `state` 는 한 "
                     "이름공간이라 우리 출력이 선언 자리에 앉는다. 이름을 갈라라")
    for name in gone:
        fails.append(f"2: `{name}` 가 허용 목록에 있는데 더는 안 겹친다 — 목록에서 빼라 "
                     "(허용은 기록이지 영구 면제가 아니다)")

    for f in fails:
        print(f"  [FAIL] {f}")
    if not fails:
        # ⚠ **두 종을 따로 센다.** 한 수로 합치면 «미조사가 줄었나» 를 아무도 못 본다.
        designed = sorted(k for k, v in ALLOWED.items() if v == DESIGNED)
        unexamined = sorted(k for k, v in ALLOWED.items() if v == UNEXAMINED)
        print(f"  [PASS] 이름 충돌 — 선언 {len(declared)} · Returns {len(returned)} · "
              f"겹침 {len(overlap)}: 설계 {len(designed)} ({' · '.join(designed)}) · "
              f"미조사 {len(unexamined)} ({' · '.join(unexamined)}, {UNEXAMINED})")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
