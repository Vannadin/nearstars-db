# 게이트 인터프리터 3.12 이상 거절 시험 — check.sh 머리(핀 검사와 판 검사)를 심은 가짜 python3 으로 돌려 3.9·3.10 은 이름 붙은 거절, 3.12·3.13 은 통과
"""python3 scripts/test_gate_python_version.py

check.sh's head, from its first line through the version check's `esac`, is run with GATE_PY set to a planted stub
`python3` that reports a chosen version (owner 2026-11-13, f075fa770: the gate runs on 3.12 or newer only). The stub
is machine-independent, so the PC (no 3.9) runs the same cases. A head without the version check passes 3.9: this
test then fails (the mutant)."""
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARK = "_gate_ver=$("


def head():
    lines = (ROOT / "scripts" / "check.sh").read_text(encoding="utf-8").splitlines(keepends=True)
    start = next(i for i, x in enumerate(lines) if x.startswith(MARK))
    end = next(i for i in range(start, len(lines)) if lines[i].strip() == "esac")
    return "".join(lines[:end + 1]) + 'echo "HEAD-OK"\n'


def run(version):
    with tempfile.TemporaryDirectory() as d:
        stub = Path(d) / "bin" / "python3"
        stub.parent.mkdir()
        stub.write_text(f'#!/bin/sh\necho "{version}"\n')
        stub.chmod(stub.stat().st_mode | stat.S_IXUSR)
        script = Path(d) / "head.sh"
        script.write_text(head(), encoding="utf-8")
        env = {**os.environ, "GATE_PY": str(stub)}
        return subprocess.run(["bash", str(script)], cwd=ROOT, env=env, capture_output=True, text=True)


def main():
    bad = 0
    for ver, ok in (("3.9", False), ("3.10", False), ("3.11", False), ("3.12", True), ("3.13", True)):
        r = run(ver)
        passed = (r.returncode == 0 and "HEAD-OK" in r.stdout) if ok else \
            (r.returncode == 2 and f"gate interpreter {ver} is older than 3.12" in r.stdout and "HEAD-OK" not in r.stdout)
        bad += not passed
        print(f"  [{'PASS' if passed else 'FAIL'}] GATE_PY reporting {ver} → rc {r.returncode}"
              f" · {(r.stdout.strip().splitlines() or [''])[-1][:120]}")
    print("모두 통과" if not bad else f"{bad} 실패")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
