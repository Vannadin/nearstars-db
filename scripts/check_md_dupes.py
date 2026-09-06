#!/usr/bin/env python3
# 한 파일 안에 같은 절이 통째로 두 번 들어갔는지 본다 — 게이트가 그런 파일을 초록으로 통과시킨 적이 있다
"""Find a section pasted twice into the same Markdown file.

    python3 scripts/check_md_dupes.py

On 2026-09-06 a commit put 53 identical lines into `engine/tools/README.md` — two whole entries, a
second time — and **gate129 passed it on the full lane.** Nothing here looked. A duplicated section
outlives a broken table: a reader sees plausible prose either way, and the next person to correct one
of the entries leaves the other standing.

**Detection is by the body, not by the heading.** The obvious test — "the same `##` twice in one
file" — was proposed first and measured before it was built: it fires on **11 files**, and every one
is legitimate structure. `phase2/alpha_centauri_proxima/checklist.md` has a `### mass_measurements`,
`### radius_measurements` and eight more per field; `phase3/61_vir/context-notes-planets.md` has
`### b`, `### c`, `### d` per planet; `engine/sub-neptune-checklist.md` repeats `## Reproduce` /
`## Diagnose` / `## Fix` per case. **Repeating a heading is how this repository is written.**

⚠ **The same shape of mistake as the table checker's, in the same place.** That file's header records
trying "a line starting with `|` after prose" and being wrong. Here the obvious test was the heading,
and it was wrong too. Both times **the obvious predicate matched the defect's appearance** — a line
beginning with a pipe, a heading occurring twice — **and the working one matches its substance**: no
delimiter row; a body identical byte for byte. Both times the shape came from one seat and was
measured by another before it was built; the step that cannot be dropped is the measuring, whoever
proposes.

**So: identical bodies, with a length floor.** Comparing whole sections gives 3 hits across the tree,
all in `engine/sub-neptune-checklist.md`, all 4–6 lines — the per-case template again. A floor of
`MIN_LINES` removes them and leaves **zero** false positives, while the real defect's two blocks (23
and 30 lines) are both caught. Prose does not match another section byte for byte over ten lines by
accident.

**Scope, stated because two seats measured it two ways and neither set contained the other.**

| scan | files | has | lacks |
|---|---|---|---|
| `Path.rglob("*.md")` (this checker) | 827 | dot-directories (`.claude/`, `.agents/`, 113 files) | `_papers`, not descended: it is a symlink |
| `glob.glob("**/*.md", recursive=True)` | 1455 | `_papers`, 741 generated paper sidecars | dot-directories — `**` skips them |

Their union is 1568 files, and **the ten-line floor returns zero hits on all of it**, the 741 generated
sidecars included. That is the number the floor rests on, not the 823 this checker actually walks.

⚠ **`SKIP_DIRS` contains an entry that has never excluded anything.** `_papers` is a symlink, and
`rglob` does not descend into one, so listing it changes nothing today — the symlink is doing the work
and the list is taking the credit. **A skip that fires and a skip that cannot look identical in the
source**, so this checker prints what each entry actually excluded and an inert one shows as `0`. The
entry stays: it becomes real the day someone replaces the symlink with a directory.

Exit code 1 on any unexempted hit.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "_papers", "node_modules", ".venv", ".archive"}

#: 이 아래 길이의 동일 절은 사례별 절차 틀이다. 재보고 정한 값이지 어림이 아니다 — 정상 반복의
#: 최댓값이 6줄, 실제 결함의 최솟값이 23줄이라 그 사이면 어디든 같은 답을 낸다.
MIN_LINES = 10

# 예외는 파일이 아니라 **이유**가 등록된다. 이유가 없으면 그건 미수리이지 예외가 아니다.
EXEMPT: dict[str, str] = {}


def duplicate_sections(path: Path) -> list[tuple[int, int, str]]:
    """(첫 번째 줄번호, 두 번째 줄번호, 제목) — 1-기준, 편집기가 세는 것과 같게."""
    lines = path.read_text(encoding="utf-8").splitlines()
    fence = False
    starts: list[int] = []
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence and line.startswith("#"):
            starts.append(i)
    starts.append(len(lines))

    seen: dict[str, int] = {}
    out: list[tuple[int, int, str]] = []
    for a, b in zip(starts, starts[1:]):
        if b - a < MIN_LINES:
            continue
        body = "\n".join(lines[a:b]).strip()
        if body in seen:
            out.append((seen[body] + 1, a + 1, lines[a].strip()[:70]))
        else:
            seen[body] = a
    return out


def _present_dirs() -> set[str]:
    """SKIP_DIRS 중 트리에 실제로 있는 이름. ⚠ 루트만 보면 안 된다 — 이 레포에서 스킵 대상은
    전부 중첩돼 있다(`engine/.venv`, `docs/phase3/_papers`). 첫 판이 `(ROOT / d).exists()` 였고,
    그래서 `_papers` 를 "트리에 없음" 이라고 보고했다. 심링크는 내려가지 않되 이름은 센다.

    ⚠ 그리고 **같은 코드가 체크아웃 종류에 따라 다른 답을 낸다.** git **워크트리**에서 `.git` 은
    디렉터리가 아니라 70바이트짜리 **파일**(`gitdir: …`)이라 여기 안 잡히고, 그래서 "트리에 없는
    항목" 으로 보고된다 — 사실이다, 스킵할 디렉터리가 없다. 보통 체크아웃에서 돌리면 같은 코드가
    `.git` 을 "있는데 못 내려감" 으로 낸다. **둘 다 맞다.** 이 문단이 없으면 다음 사람이 그 차이를
    결함으로 읽는다.
    """
    found: set[str] = set()
    for base, dirs, _files in os.walk(ROOT):
        for d in list(dirs):
            if d in SKIP_DIRS:
                found.add(d)
                dirs.remove(d)          # 안으로는 안 들어간다. 있다는 것만 안다.
    return found


def main() -> int:
    bad: list[str] = []
    exempted = scanned = 0
    #: 스킵이 실제로 무엇을 걷어냈는지 센다. 0 이면 그 항목은 오늘 아무 일도 안 하고 있다는 뜻이고,
    #: 그 사실이 보여야 한다 — 발화하는 스킵과 도달조차 못 하는 스킵은 소스에서 똑같이 생겼다.
    #: ⚠ 0 에도 두 뜻이 있어 갈라 센다. **부재**는 그 경로가 트리에 아예 없다는 것이고, **미도달**은
    #: 있는데 스캔이 안 내려갔다는 것이다(`_papers` 가 심링크라 그렇다). 둘을 한 칸에 넣으면, 나중에
    #: 누가 스킵 줄을 지워도 출력이 안 변해서 지워도 되는 줄 알게 된다 — 그러다 심링크가 실제
    #: 디렉터리로 바뀌는 날 741개가 쏟아진다.
    skipped: dict[str, int] = {d: 0 for d in SKIP_DIRS}
    present = _present_dirs()
    for path in sorted(ROOT.rglob("*.md")):
        hit = [p for p in path.parts if p in SKIP_DIRS]
        if hit:
            skipped[hit[0]] += 1
            continue
        scanned += 1
        rel = path.relative_to(ROOT).as_posix()
        for first, second, heading in duplicate_sections(path):
            if rel in EXEMPT:
                exempted += 1
                continue
            bad.append(f"{rel}:{second} — this section is byte-identical to the one at line {first}. "
                       f"Heading: {heading!r}")

    for b in bad:
        print(f"  [FAIL] 같은 절이 두 번 — {b}")
    if bad:
        print(f"\n  뒤 벌을 지우십시오. 두 벌이 정말 같은지 지우기 전에 확인하고, 다르면 그건 "
              f"중복이 아니라 편집 충돌입니다.")
        return 1
    fired = ", ".join(f"{d} {n}개" for d, n in sorted(skipped.items()) if n) or "없음"
    #: 0 인데 경로가 있다 = 스캔이 못 내려갔다. 0 이고 경로도 없다 = 걷어낼 것이 애초에 없다.
    unreached = sorted(d for d, n in skipped.items() if n == 0 and d in present)
    absent = sorted(d for d, n in skipped.items() if n == 0 and d not in present)
    print(f"  [PASS] 마크다운 절 중복 — {scanned}개 파일, {MIN_LINES}줄 이상 동일 절 0건 "
          f"(의도적 예외 {exempted}건: {', '.join(EXEMPT) if exempted else '없음'})")
    line = f"         스킵 발화: {fired}"
    if unreached:
        line += "  ·  ⚠ 있는데 스캔이 못 내려간 항목(스킵이 일한 게 아니다): " + ", ".join(unreached)
    if absent:
        line += "  ·  트리에 없는 항목: " + ", ".join(absent)
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
