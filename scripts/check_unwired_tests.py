# 게이트(check.sh)가 안 부르는 test_*.py 를 잡는다 — 추적 시험 − (엮임 ∪ 이름 박힌 제외) 가 비어야 PASS (C129)
"""Fail when a tracked test_*.py is neither run by scripts/check.sh nor excluded here with a reason.

엮임 = check.sh 의 주석 아닌 줄에 그 파일의 basename 이 글자 그대로 나옴 (C129 §1.1).
엮임으로 센 줄은 전부 인쇄한다 — echo 문구 같은 데서 잘못 세는지 눈으로 보려고 (C129 §4-1).
"""
from __future__ import annotations

import collections
import pathlib
import subprocess
import sys

#: 게이트가 안 돌리는 시험 — {레포 경로: 까닭}. 칸을 더하거나 빼는 것은 등록.
EXCLUDED = {
    "scripts/pipeline/test_hierarchical.py":
        "게이트 venv 에 PyAstronomy 없음 — DB 파이프라인 환경 시험(build_systems.py 가 import; "
        "시스템 파이썬으로는 PASS, 2026-09-29). 게이트 venv 에 의존성을 넣을지는 열린 결정",
}


def tracked_tests(root: pathlib.Path) -> list[str]:
    out = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True).stdout
    return sorted(p for p in out.split("\n") if p and p.rsplit("/", 1)[-1].startswith("test_") and p.endswith(".py"))


def audit(tests: list[str], check_sh: str, excluded: dict[str, str]) -> tuple[list[str], list[str]]:
    """(FAIL 줄들, 인쇄 줄들)."""
    lines = [(i, l) for i, l in enumerate(check_sh.split("\n"), 1) if not l.lstrip().startswith("#")]
    fails: list[str] = []
    shown: list[str] = []
    dup = [b for b, n in collections.Counter(t.rsplit("/", 1)[-1] for t in tests).items() if n > 1]
    for b in dup:
        fails.append(f"[FAIL] basename 겹침 {b} — 글자 일치로 엮임을 못 가름")
    wired = 0
    for t in tests:
        base = t.rsplit("/", 1)[-1]
        hits = [(i, l) for i, l in lines if base in l]
        if hits:
            wired += 1
            for i, l in hits:
                shown.append(f"  엮임 {t} ← check.sh {i} 행: {l.strip()[:120]}")
            if t in excluded:
                fails.append(f"[FAIL] 엮여 있는데 제외 목록에도 있음 {t}")
        elif t in excluded:
            if not excluded[t].strip():
                fails.append(f"[FAIL] 제외 까닭 빈 칸 {t}")
            else:
                shown.append(f"  제외 {t} — {excluded[t]}")
        else:
            fails.append(f"[FAIL] 안 엮인 시험 {t}")
    for t in excluded:
        if t not in tests:
            fails.append(f"[FAIL] 낡은 제외 {t} — 추적 파일 없음")
    shown.append(f"대상 {len(tests)} · 엮임 {wired} · 제외 {sum(t in excluded for t in tests)}")
    return fails, shown


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent.parent
    fails, shown = audit(tracked_tests(root), (root / "scripts/check.sh").read_text(encoding="utf-8"), EXCLUDED)
    print("\n".join(shown))
    print("\n".join(fails))
    if not fails:
        print("  [PASS] 안 엮인 test_*.py 없음")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
