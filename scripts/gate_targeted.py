# 게이트의 표적 층이 돌 시험 목록을 바뀐 경로에서 도출한다 — import 그래프의 추이 폐포로 (브리프 169 B)
"""Derive the targeted lane's test list from a commit range, and say when it cannot.

    python3 scripts/gate_targeted.py <base-sha> <head-sha>

Three lines on stdout, in this order, each possibly empty after the first:

    1. the number of changed paths
    2. the changed code paths this mapping cannot explain (space-separated) — **non-empty means the
       caller must fall back to the full lane**
    3. the derived work items (space-separated): `test_*.py`, `tools/<tool>.py`, `run:bodies/<b>.yaml`,
       and `gate:<step>` for the three gate steps that are not tests (backflow, chain, dynamo_table)

⚠ **Why this is not a hand-written table.** Brief 169's first mapping followed imports **one hop**, and
a static census of `engine/` (52 modules, 43 tests) found that the transitive test set is much wider for
low-level modules — `fermi` derived 1 test where its transitive dependents hold 32, `eos` 10 against 30,
`registry` 1 against 24 (audit seat, 2026-09-09). A one-hop list is a *plausible* list, and a plausible
list is what the lane exists to stop. So the graph is computed from the AST on every run and the closure
is taken; nobody types the pairs.

⚠ **The answer runs are unconditional whenever code changed.** `check.sh`'s own recorded decision is
that *"the answer tests are never skipped on a commit that changed code"*, and those live in
`run.py bodies/…`, not in a `test_*.py`. So any changed `engine/**.py` or `engine/bodies/*.yaml` adds
**every** body in `engine/bodies/` (169 E — the list used to be three names typed twice, and Mars fell
out of both), regardless of what the import graph says.

⚠ **A changed path outside the mapping is a veto, not a guess.** `scripts/`, `engine/chain.yaml`,
`check.sh` itself: nothing here can say what depends on them, so the lane is abandoned rather than
narrowed. That is the same veto `--wiring` already had.
"""
from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGINE = ROOT / "engine"
CHECK_SH = ROOT / "scripts" / "check.sh"

def answer_bodies() -> list[str]:
    """코드가 바뀌면 언제나 함께 도는 answer 실행 — **디렉토리가 목록이다** (169 E).

    ⚠ 예전에는 `("alpha_centauri_a_b", "pandora", "earth")` 리터럴이었고, `check.sh` 에도 같은 셋이
    손으로 적혀 있었다. 그래서 `bodies/mars.yaml` 이 두 곳 모두에서 빠진 채 **한 달 가까이 아무
    게이트도 화성의 출하값 대조를 안 돌렸다**(C59). 리터럴을 고치는 대신 글롭으로 바꾸는 이유는
    여덟 번째 바디에서 같은 누락이 반복되기 때문이고, `check.sh` 도 같은 글롭을 쓰므로 두 파일이
    갈릴 수 없다."""
    return [p.name for p in sorted((ENGINE / "bodies").glob("*.yaml"))]

#: ⚠ **12b 는 어느 층에서도 좁혀지지 않는다** — 이 둘은 그래서 «시험이 없다» 가 구멍이 아니다.
#: 이것들을 빼기 전에는 `engine/check_contracts.py` 를 고친 커밋이 매번 «매핑이 설명 못 하는 경로»
#: 로 잡혀 full 로 떨어졌다 (169 C, 실측). ⚠ 이 목록은 `scripts/check.sh` 의 12b 블록과 **손으로
#: 묶여 있다**: 거기서 무엇이 항상 도는지가 바뀌면 여기도 바뀌어야 한다.
#: ⚠ **169 C 는 다섯을 적었고 셋은 필요 없었다** (170 E, 실측): `check_refs` 는 `test_check_refs`
#: 가 덮고, `test_check_refs` 는 그 자신이 시험이며, `check_citations` 는 `tools/` 항목이라 도구
#: 규칙이 잡는다. 면제는 **다른 규칙이 못 잡는 것에만** 준다 — 넓은 면제는 조용한 면제다.
ALWAYS_RUN = ("check_via", "check_contracts")

#: ⚠ **13 블록의 «시험이 아닌» 게이트 단계** — 모듈 이름 → check.sh 가 아는 항목 어휘 (169 D ②).
#: 이것들이 없으면 `engine/backflow.py` 를 고친 커밋이 **자기를 검사하는 단계 없이** 초록으로 지나간다:
#: `backflow.py check` 는 bindings 정합성을, `chain.py check` 는 그래프를, `dynamo_table.py --check` 는
#: 문서 표를 검사하는데 셋 다 `test_*.py` 가 아니라 어떤 시험 폐포에도 안 잡힌다.
#: ⚠ 감사석은 `backflow` 하나를 지적했고, 같은 모양인 나머지 둘도 함께 닫았다 — 하나만 닫으면
#: 다음 사람이 같은 자리에서 같은 것을 다시 발견한다.
GATE_STEPS = {"backflow": "gate:backflow", "chain": "gate:chain", "dynamo_table": "gate:dynamo_table"}


def modules() -> dict[str, Path]:
    """`engine/` 아래의 로컬 모듈 — 키는 import 될 이름, 값은 파일."""
    out: dict[str, Path] = {}
    for p in sorted(ENGINE.glob("*.py")):
        out[p.stem] = p
    for p in sorted((ENGINE / "tools").glob("*.py")):
        out.setdefault(p.stem, p)          # ⚠ 평평한 이름공간: tools 는 sys.path 로 부모를 잡는다
    return out


def imports_of(path: Path, known: set[str]) -> set[str]:
    """그 파일이 import 하는 **로컬** 모듈 이름. 표준 라이브러리와 서드파티는 버린다."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return set()
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                head = a.name.split(".")[0]
                if head in known:
                    found.add(head)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            head = node.module.split(".")[0]
            if head in known:
                found.add(head)
    return found


def dependents_closure(seeds: set[str], mods: dict[str, Path]) -> set[str]:
    """씨앗 모듈들을 (직접·간접으로) import 하는 모든 모듈. 씨앗 자신도 포함한다."""
    known = set(mods)
    rev: dict[str, set[str]] = {name: set() for name in known}
    for name, path in mods.items():
        for dep in imports_of(path, known):
            rev.setdefault(dep, set()).add(name)
    seen = set(seeds)
    stack = list(seeds)
    while stack:
        cur = stack.pop()
        for user in rev.get(cur, ()):
            if user not in seen:
                seen.add(user)
                stack.append(user)
    return seen


def rel_name(mods: dict[str, Path], name: str) -> str:
    """`engine/` 기준 상대 이름 — tools 아래면 `tools/x.py`, 아니면 `x.py`."""
    p = mods[name]
    return str(p.relative_to(ENGINE))


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    base, head = sys.argv[1], sys.argv[2]
    diff = subprocess.run(["git", "diff", "--name-only", base, head],
                          cwd=ROOT, capture_output=True, text=True)
    if diff.returncode != 0:
        print("0"); print(f"git-diff-failed:{base}..{head}"); print("")
        return 0
    changed = [ln for ln in diff.stdout.splitlines() if ln.strip()]

    mods = modules()
    check_text = CHECK_SH.read_text(encoding="utf-8") if CHECK_SH.exists() else ""
    tests = {name for name in mods if name.startswith("test_")}

    seeds: set[str] = set()
    items: set[str] = set()
    gap: list[str] = []
    code_changed = False

    for p in changed:
        if p.endswith(".md"):
            continue
        if p.startswith("engine/bodies/") and p.endswith(".yaml"):
            code_changed = True
            body = Path(p).name
            items.add(f"run:bodies/{body}")
            for name in sorted(tests):
                if body in mods[name].read_text(encoding="utf-8"):
                    items.add(rel_name(mods, name))
            continue
        if p.startswith("engine/") and p.endswith(".json"):
            # **굳힌 앵커 파일** — 그것을 읽는 시험이 그것의 시험이다 (브리프 169 G). 파일 이름을
            # 본문에 들고 있는 `test_*.py` 를 찾는다: `ice_giant_anchor.json` 은 `test_ice_giant.py`
            # 가 열고 굳힌다. ⚠ 앵커가 바뀌는 커밋은 **코드가 바뀐 커밋이 아니다** — 그래서
            # answer 실행을 켜지 않는다. 앵커만 바뀌었으면 그 앵커를 읽는 시험 하나면 된다.
            # ⚠ 아무 시험도 그 이름을 안 들고 있으면 구멍이다. 데이터 파일이 무엇의 앵커인지
            #   말할 수 없으면 좁히지 않는다.
            base_name = Path(p).name
            readers = [name for name in sorted(tests)
                       if base_name in mods[name].read_text(encoding="utf-8")]
            if not readers:
                gap.append(p)
                continue
            for name in readers:
                items.add(rel_name(mods, name))
            continue
        if p.endswith(".py") and (p.startswith("engine/") or p.startswith("engine/tools/")):
            stem = Path(p).stem
            if stem not in mods:                 # 지워진 파일 — 무엇이 그것에 기대는지 말할 수 없다
                gap.append(p)
                continue
            code_changed = True
            seeds.add(stem)
            continue
        gap.append(p)

    if seeds:
        closure = dependents_closure(seeds, mods)
        for name in sorted(closure):
            rel = rel_name(mods, name)
            if name.startswith("test_"):
                items.add(rel)
            elif name in GATE_STEPS:
                items.add(GATE_STEPS[name])      # 시험이 아닌 게이트 단계 — 어휘로 부른다
            elif rel.startswith("tools/") and rel in check_text:
                items.add(rel)                   # check.sh 가 부르는 도구는 그 자체가 게이트 항목이다
        # ⚠ 씨앗 중 시험이 하나도 안 딸린 것이 있으면 그것은 매핑 구멍이다 — 좁히지 않는다.
        for s in sorted(seeds):
            if s in ALWAYS_RUN:
                continue                     # 12b 가 층과 무관하게 돌린다 — 시험이 없는 것이 구멍이 아니다
            own = dependents_closure({s}, mods)
            covered = any(n.startswith("test_") for n in own) or any(n in GATE_STEPS for n in own) or \
                any(rel_name(mods, n).startswith("tools/") and rel_name(mods, n) in check_text for n in own)
            if not covered:
                gap.append(rel_name(mods, s))

    if code_changed:
        for body in answer_bodies():
            items.add(f"run:bodies/{body}")

    print(len(changed))
    print(" ".join(sorted(set(gap))))
    print(" ".join(sorted(items)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
