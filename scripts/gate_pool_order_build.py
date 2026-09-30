# 같은 기계의 정상 full 게이트 로그들에서 풀 단계의 `[TIME]` 벽시계 평균 내림차순으로 풀 순서 파일을 짓는 생성기 (C135, 손으로 돌림)
"""Build `scripts/gate_pool_order.<gate_machine>.txt` from gate logs of one machine.

    python3 scripts/gate_pool_order_build.py <gate log> [<gate log> ...] > scripts/gate_pool_order.<gate_machine>.txt

Rule (C135): pool steps are ordered by the **mean `[TIME]` wall seconds** over normal full runs on the **same
`gate_machine`**, longest first. `[COST] instr` is not read — its counting domain differs by machine (C134
decision 1: the Mac counts the direct task, Linux counts children), and after C135 split steps it no longer
tracks wall time on either machine.

Run by hand, not by the gate. Commit the output file separately so the order change is reviewable.
A log is refused **by name** when it has no `[기록] gate_machine:` line (older than C134), when its machine
differs from the others, or when it is not a completed full run (`GATE START … lane=full` and `GATE END`).
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

TIME = re.compile(r"^  \[TIME\] (.+?) — \d\d:\d\d:\d\d → \d\d:\d\d:\d\d · (\d+) s · RSS ")
START = re.compile(r"^GATE START sha=(\S+) .* lane=(\S+)")
MACHINE = re.compile(r"^  \[기록\] gate_machine: (\S+)")


def pool_eligible(name: str) -> bool:
    """`check.sh` 의 `_pool_eligible` 과 같은 규칙 — `test_…` 와 `run.py …` 만 풀에 든다."""
    return name.startswith("test_") or name.startswith("run.py")


def read(path: Path) -> tuple[str | None, str | None, str | None, bool, dict[str, int]]:
    machine = sha = lane = None
    ended = False
    times: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if (m := START.match(line)) and sha is None:
            sha, lane = m.group(1), m.group(2)
        elif (m := MACHINE.match(line)) and machine is None:
            machine = m.group(1)
        elif line.startswith("GATE END "):
            ended = True
        elif (m := TIME.match(line)) and pool_eligible(m.group(1)):
            times[m.group(1)] = int(m.group(2))
    return machine, sha, lane, ended, times


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__, file=sys.stderr)
        return 2
    runs, refused = [], []
    for arg in argv:
        path = Path(arg)
        machine, sha, lane, ended, times = read(path)
        if machine is None:
            refused.append(f"{path.name}: `[기록] gate_machine:` 줄이 없다 (C134 이전 로그)")
        elif lane != "full" or not ended:
            refused.append(f"{path.name}: 끝난 full 판이 아니다 (lane={lane}, GATE END {'있음' if ended else '없음'})")
        elif not times:
            refused.append(f"{path.name}: 풀 단계의 `[TIME]` 줄이 없다")
        else:
            runs.append((path, machine, sha, times))
    machines = sorted({r[1] for r in runs})
    if len(machines) > 1:
        refused.append(f"기계가 섞였다 — {', '.join(machines)}. 한 기계의 로그만 준다")
    if refused or not runs:
        for why in refused or ["쓸 로그가 없다"]:
            print(f"[FAIL] {why}", file=sys.stderr)
        return 1
    total: dict[str, list[int]] = defaultdict(list)
    for _p, _m, _s, times in runs:
        for name, secs in times.items():
            total[name].append(secs)
    mean = {name: sum(v) / len(v) for name, v in total.items()}
    order = sorted(mean, key=lambda n: (-mean[n], n))
    shas = " ".join(sorted(s or "?" for _p, _m, s, _t in runs))
    print(f"# 게이트 풀 단계의 시작 순서 — 같은 기계 정상 full 판들의 [TIME] 벽시계 평균 내림차순 (C135, 긴 단계 먼저)")
    print(f"# gate_machine {machines[0]} · 판 {len(runs)}: {shas} · 한 줄에 단계 이름 하나 · 없는 이름은 **앞에** 선다")
    for name in order:
        print(name)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
