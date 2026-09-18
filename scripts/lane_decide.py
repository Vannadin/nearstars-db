# 바뀐 파일만 보고 차선을 고른다 — 앵커 지문을 안 쓰고, 판정하려고 코드를 돌리지도 않는다 (차선 규칙)
"""Choose the gate's lane from a diff, and print the reason.

    python3 scripts/lane_decide.py <parent-sha> <target-sha> <gate-logs-dir>

⚠ **앵커의 입력 지문을 쓰지 않는다.** 그 33 개는 얼음거인 경로뿐이라 `engine/mantle_budget.py` 도
`engine/tools/c51_regimes.py` 도 그 목록에 없다 — 어젯밤 적분 방향을 뒤집은 커밋이 지문으로는
«같음» 이었고, quick 여덟에는 그 시험이 없다 (감사석 반례). 그래서 경계는 **diff** 다.

⚠ **import 하지 않는다.** 판정하려고 판정 대상 모듈을 실행하면 부작용을 사는 셈이고, `compile()`
만으로 충분하다 — 리터럴 기본값은 감싸는 코드 객체의 상수이고(`MAKE_FUNCTION` 앞의 `LOAD_CONST`),
리터럴이 아니면 그 계산식 자체가 코드다. 실측: `b=0.5 → 0.6` 은 해시를 움직이고 주석만 더한 사본은
안 움직인다.
"""
from __future__ import annotations

import datetime
import hashlib
import pathlib
import re
import subprocess
import sys
import types

#: 바뀌면 **무조건 full**. 게이트 자신·선언·엔진이 읽는 데이터다.
ALWAYS_FULL = re.compile(
    r"(^scripts/.*\.sh$)|(^engine/chain\.yaml$)|(^engine/requirements\.txt$)"
    r"|(^engine/ice_giant_anchor\.json$)|(^engine/bodies/.*\.(yaml|json)$)"
    r"|(^engine/.*\.(yaml|json|csv|tsv|txt)$)|(^scripts/.*\.py$)")
#: 산문·미러·생성 페이지. 계산에 안 들어간다.
PROSE = re.compile(r"(\.md$)|(^ko/)|(^docs/)|(^plans/)|(^phase4/.*\.md$)"
                   r"|(^engine/chain-explorer\.html$)")


def _sh(*args: str) -> str:
    return subprocess.run(args, capture_output=True, text=True, check=True).stdout


def code_digest(blob: bytes, name: str) -> str:
    """코드 객체의 정규 해시 — 주석·빈 줄·docstring 의 **위치**는 안 잡고, 상수·바이트코드는 잡는다.

    ⚠ **docstring 의 내용이 바뀌면 코드 객체가 움직인다** — docstring 은 `co_consts` 의 상수라
    `repr(k)` 에 그대로 들어간다 (감사석 픽스처 2026-09-18: `+주석` SAME · 빈 줄 SAME ·
    모듈 docstring 변경 MOVED · 함수 docstring 변경 MOVED). 이 레포는 산문을 docstring 에 쓰므로
    「산문만 고친 코드 커밋」의 대부분이 **full** 이다. 주석으로 옮겨 적으면 quick 을 탄다.
    """
    def walk(c: types.CodeType) -> str:
        parts = [c.co_name, c.co_argcount, c.co_kwonlyargcount, tuple(c.co_varnames)]
        for k in c.co_consts:
            parts.append(walk(k) if isinstance(k, types.CodeType) else repr(k))
        parts.append(c.co_code.hex())
        return "|".join(map(str, parts))
    return hashlib.sha256(walk(compile(blob, name, "exec")).encode()).hexdigest()[:16]


def classify(parent: str, target: str) -> tuple[str, list[str], int]:
    # ⚠ **상태까지 읽는다** — 더해지거나 지워지거나 이름이 바뀐 `.py` 는 비교할 짝이 없다.
    rows = [l for l in _sh("git", "diff", "--name-status", f"{parent}..{target}").split("\n") if l]
    if not rows:
        # ⚠ 이유 줄이 아니라 **바뀐 파일 수**가 0 이다 — 이유 목록 길이로 세면 여기서 1 이 찍힌다.
        return "quick", [], 0
    reasons: list[str] = []
    verdict = "quick"
    for row in rows:
        cols = row.split("\t")
        status, path = cols[0], cols[-1]
        if status[:1] in ("A", "D", "R") and path.endswith(".py"):
            reasons.append(f"{path} {status} — 새/지워진/이름바뀐 코드는 잰 적이 없다 → **full**")
            verdict = "full"
            continue
        if PROSE.search(path):
            reasons.append(f"{path} 산문/미러/생성물 → 통과")
            continue
        if ALWAYS_FULL.search(path):
            reasons.append(f"{path} 게이트·선언·데이터 → **full**")
            verdict = "full"
            continue
        if path.endswith(".py"):
            try:
                a = _sh("git", "show", f"{parent}:{path}")
                b = _sh("git", "show", f"{target}:{path}")
            except subprocess.CalledProcessError:
                reasons.append(f"{path} 한쪽에만 있음 → **full**")
                verdict = "full"
                continue
            if code_digest(a.encode(), path) == code_digest(b.encode(), path):
                reasons.append(f"{path} 코드 객체 동일(주석 전용) → 통과")
            else:
                reasons.append(f"{path} 코드 객체 다름(docstring 내용 포함) → **full**")
                verdict = "full"
            continue
        reasons.append(f"{path} 분류 없음 → **full**")
        verdict = "full"
    return verdict, reasons, len(rows)


def full_ran_today(logs_dir: pathlib.Path, day: str) -> tuple[bool, list[str]]:
    """오늘 **끝난** full 게이트가 있었나 — 별도 상태 파일 없이 로그 디렉터리를 훑는다.

    세는 조건을 문장으로 (감사석 개정 1): **오늘(+0900)** · **END 줄이 있고** · **`rc=0`** ·
    **`lane=full`** · **이 레포**(END 줄의 `isolated=` 경로나 sha 로 판별). ⚠ **END 가 없는 판은
    «미완 full 진행 중» 으로 따로 세고 «오늘 full 있었음» 으로 안 친다.**
    ⚠ **못 찾으면 full 쪽으로 실패한다** — 디렉터리가 없거나 사본이 안 옮겨졌을 때 조용히 quick
    으로 넘어가면, 안전망이 꺼진 것을 아무도 못 본다."""
    notes: list[str] = []
    if not logs_dir.is_dir():
        return False, [f"로그 디렉터리 없음 ({logs_dir}) → 안전망은 full 쪽으로 실패한다"]
    done = running = undated = 0
    for log in sorted(logs_dir.glob("gate-*.log")):
        text = log.read_text(encoding="utf-8", errors="ignore")
        end = [l for l in text.split("\n") if l.startswith("GATE END")]
        if not end:
            # ⚠ 파일 시각으로 «오늘» 을 정하지 않는다 — mtime 은 사본을 옮긴 때이기도 하다.
            start = [l for l in text.split("\n") if l.startswith("GATE START")]
            if start and f"date={day}" in start[-1]:
                running += 1
                notes.append(f"{log.name} — END 없음, **오늘 미완 full 진행 중**으로 셈")
            continue
        line = end[-1]
        m = re.search(r"\bdate=(\d{4}-\d\d-\d\d)\b", line)
        if m is None:
            undated += 1
            continue
        if m.group(1) != day:
            continue
        sha = re.search(r"\bsha=([0-9a-f]+)\b", line)
        if sha is None or subprocess.run(
                ["git", "merge-base", "--is-ancestor", sha.group(1), "HEAD"],
                capture_output=True).returncode != 0:
            notes.append(f"{log.name} — 이 레포의 조상이 아니다 → 안 셈")
            continue
        if "lane=full" in line and "rc=0" in line:
            done += 1
            notes.append(f"{log.name} — 오늘 끝난 full (rc=0, sha={sha.group(1)})")
    notes.append(f"오늘({day}) 끝난 full {done} · 미완 {running} · 날짜 없는 옛 로그 {undated}(안 셈)")
    return done > 0, notes


def main() -> int:
    parent, target, logs = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3]).expanduser()
    today = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %z")
    day = today.split()[0]
    had_full, notes = full_ran_today(logs, day)
    for n in notes:
        print(f"  · {n}")
    if not had_full:
        print(f"lane=full 이유=오늘({today}) 끝난 full 이 없다 — 안전망, diff 안 봄")
        return 0
    verdict, reasons, n_files = classify(parent, target)
    print(f"lane={verdict} 이유={'모든 변경이 통과' if verdict == 'quick' else '아래 중 하나가 full 을 부름'}"
          f" · 오늘({today}) full 있었음 · 바뀐 파일 {n_files}")
    for r in reasons:
        print(f"  · {r}")
    if verdict == "quick":
        print("  ⚠ quick 은 여덟 단계뿐이다 — **66 단계는 안 돈다**. 안 돈 것은 «통과» 가 아니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
