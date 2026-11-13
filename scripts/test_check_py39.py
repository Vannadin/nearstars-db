# check_py39 의 픽스처 시험 — 3.9 에서 깨지는 꼴은 빨강, 깨지지 않는 꼴은 초록 (VR-base 7)
"""python3 scripts/test_check_py39.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_py39 as c  # noqa: E402

RED = {
    "arg union": "def f(x: dict | None = None):\n    pass\n",
    "return union": "def f() -> int | None:\n    pass\n",
    "nested def": "def f():\n    def g(y: str | None):\n        pass\n",
    "method": "class A:\n    def m(self, y: int | None):\n        pass\n",
    "module AnnAssign": "x: int | None = None\n",
    "class AnnAssign": "class A:\n    x: int | None = None\n",
    "inside if": "if True:\n    def f(x: int | None):\n        pass\n",
    "isinstance union": "isinstance(1, int | None)\n",
    "isinstance union with future": "from __future__ import annotations\nisinstance(1, int | str)\n",
    "match statement": "match x:\n    case 1:\n        pass\n",
}
GREEN = {
    "future import": "from __future__ import annotations\ndef f(x: dict | None = None) -> int | None:\n    pass\n",
    "string annotation": "def f(x: 'dict | None' = None):\n    pass\n",
    "function-local AnnAssign": "def f():\n    y: int | None = None\n",
    "Optional": "from typing import Optional\ndef f(x: Optional[dict] = None):\n    pass\n",
    "bit-or on values": "a = 1 | 2\n",
    "isinstance tuple": "isinstance(1, (int, str))\n",
}


def main() -> int:
    bad = 0
    for name, src in RED.items():
        got = c.check_source(src, f"<{name}>")
        ok = len(got) >= 1
        bad += not ok
        print(f"  [{'PASS' if ok else 'FAIL'}] red fixture «{name}» → {got[:1]}")
    for name, src in GREEN.items():
        got = c.check_source(src, f"<{name}>")
        ok = got == []
        bad += not ok
        print(f"  [{'PASS' if ok else 'FAIL'}] green fixture «{name}» → {got}")
    # 11-13 (owner f075fa770): the scope is the system-python tools only; engine/ and solver/ gate under 3.12
    ok = set(c.DIRS) == {"scripts/pipeline/", "scripts/phase4/", "scripts/refs/", "scripts/viz/"}
    bad += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] scope is the system-python tools → {c.DIRS}")
    print("모두 통과" if not bad else f"{bad} 실패")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
