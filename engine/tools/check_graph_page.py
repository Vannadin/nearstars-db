# 커밋된 의존 사슬 페이지가 그 커밋의 chain.yaml 과 같은지 다시 만들어 대조한다.
"""Regenerate `engine/chain-explorer.html` and compare it with the committed file.

    python3 engine/tools/check_graph_page.py

⚠ **C86 의 두 반 중 둘째다** (2026-09-14). 첫째는 페이지를 다시 만든 것이고, 이 검사는
«아무도 그것을 대조하지 않는다» 를 없앤다 — 기존 검사 셋은 `.html` 을 구조적으로 건너뛴다
(`check_refs` 의 live 집합은 `{.py, .yaml, .md}`, `check_contracts` 는 `chain.yaml`·`bindings.yaml`
을 읽지 페이지를 안 읽고, `check_build_freshness` 는 `docs/phase2`·`docs/phase3` 와 `db/systems`
를 본다).

⚠ **아무 일도 안 한 실행이 통과하면 안 된다** (감사석, 2026-09-14). 그래서 **먼저 지우고**,
생성기의 **rc 를 판정에 넣고**, 그다음 `git diff` 를 본다 — 생성기가 한 글자도 안 쓰면 파일이
없는 채로 남아 **삭제가 diff 에 뜬다**.

⚠ **수는 «무엇이 다른가» 를 부르는 데 쓰고, 판정은 바이트가 한다.** 낡은 페이지와 새 페이지는
**노드 수가 같을 수 있다** — `0c494b05` 의 페이지는 노드 51 · 간선 205 이고 오늘 것은 51 · 210
이다. 수만 보는 검사는 그것을 통과시킨다.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PAGE = ROOT / "engine" / "chain-explorer.html"
BUILDER = ROOT / "engine" / "build_graph_page.py"


def declared_inputs() -> list[Path]:
    """생성기가 선언한 입력을 **구체 파일로** 받아 온다 — 모듈에 물어보고, 소스는 안 읽는다.

    ⚠ **`cwd` 는 `engine/` 이어야 한다** — 레포 뿌리에서 부르면 `ModuleNotFoundError` 다.
    ⚠ **임포트에 부수효과가 없다는 것이 전제**이고, 그 전제는 생성기가 쓰기를
    `if __name__ == "__main__": build()` 뒤에 둔다는 사실이다. 그 가드가 사라지면 이 줄은 임포트만으로
    페이지를 쓰게 된다 — 그래서 여기 적어 둔다.
    ⚠ **펼치는 것도 모듈이 한다** (`input_paths()`): 패턴을 받아 셸이나 이 파일이 펼치면 주인은
    하나인데 **해석하는 쪽이 둘**이 된다."""
    run = subprocess.run(
        [sys.executable, "-c",
         'import build_graph_page as b; print("\\n".join(str(p) for p in b.input_paths()))'],
        capture_output=True, text=True, cwd=str(ROOT / "engine"))
    if run.returncode != 0:
        raise SystemExit("거절: 생성기에서 `input_paths()` 를 못 읽었다 — "
                         + (run.stderr.strip().splitlines() or ["출력 없음"])[-1])
    return [Path(x) for x in run.stdout.split("\n") if x.strip()]


def _counts(text: str) -> tuple[int, int]:
    m = re.search(r"const D\s*=\s*(\{.*?\});", text, re.S)
    if not m:
        return -1, -1
    d = json.loads(m.group(1))
    return len(d.get("nodes", ())), len(d.get("edges", ()))


def _judge(before: str) -> int:
    """임시 나무에서 다시 만들어 **커밋본과 바이트로 견준다**. 추적 파일은 안 건드린다.

    ⚠ **되쓰기가 아니라 구조로 푼다** (지휘석, 2026-09-14). 앞선 판은 페이지를 **지우고** 다시
    만들었고, 격리(`--from <sha>`) 밖에서 부르면 그 둘이 **실행 중인 워크트리**에 났다 — 생성기가
    거절하면 페이지가 지워진 채 남고, 낡은 페이지를 커밋한 나무에서는 덮어쓴 채 「다시 만들어
    커밋하라」고 말했다. 이제 생성기는 **임시 디렉터리의 거울**에서 돌고, 이 검사는 **읽기만** 한다 —
    `--from` 이 있든 없든 `git status` 가 **구조적으로** 깨끗하다.

    거울에는 생성기가 이름으로 여는 것만 넣는다 — `engine/build_graph_page.py` ·
    `engine/chain.yaml` · `engine/bindings.yaml` · `phase4/*.yaml`. **그 목록이 곧 선언된 입력이고,
    빠지면 생성기가 거절한다** (그것이 주입 시험이다)."""
    import shutil
    import tempfile

    import yaml
    graph = yaml.safe_load((ROOT / "engine" / "chain.yaml").read_text(encoding="utf-8"))
    nodes, edges = set(graph["nodes"]), graph["edges"]
    dropped = [e for e in edges if e["from"] not in nodes or e["to"] not in nodes]

    tmp = Path(tempfile.mkdtemp(prefix="c86-2-"))
    try:
        (tmp / "engine").mkdir()
        # ⚠ **목록의 주인은 하나다** — `build_graph_page.py` 의 `INPUTS` 다. 여기서 다시
        #   적으면 생성기가 입력을 하나 더 읽는 날 이 목록이 **조용히 낡고**, 검사는 «다르다» 가
        #   아니라 «맞다» 를 찍는다 (감사석, 2026-09-14 — C90 의 손 목록이 낡은 그 층이다).
        shutil.copy2(BUILDER, tmp / "engine" / BUILDER.name)
        copied = 0
        for src in declared_inputs():
            dest = tmp / src.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            copied += 1
        print(f"  거울에 복사한 입력 {copied} 개 + 생성기 자신 1 개")
        run = subprocess.run([sys.executable, str(tmp / "engine" / "build_graph_page.py")],
                             capture_output=True, text=True, cwd=str(tmp))
        made = tmp / "engine" / "chain-explorer.html"
        if run.returncode != 0:
            # ⚠ **마지막 줄을 자르지 않는다** (감사석, 2026-09-14). 120 자에서 끊었더니 거절이 이름을
            #   댄 **바로 그 경로**가 잘려 나갔다 — 이름을 대라는 수락선을 인쇄 폭이 막았다.
            tail = (run.stderr or run.stdout).strip().splitlines()
            print(f"  [FAIL] 생성기가 rc={run.returncode} 로 끝났다 — "
                  + (tail[-1] if tail else "출력 없음"))
            # ⚠ 생성기가 대는 경로는 **거울의 것**이다. 사람이 고쳐야 하는 것은 원본이므로 그 자리도
            #   함께 적는다 — 안 적으면 「임시 디렉터리에 파일이 없다」로 읽힌다.
            # ⚠ 힌트도 **선언에서 읽는다** — 손으로 적으면 거절과 힌트가 서로 다른 말을 한다
            #   (감사석, 2026-09-14: ⑦e 에서 빠진 것은 `engine/nonexistent.yaml` 인데 힌트는
            #   `phase4/*.yaml` 을 찍고 있었다).
            try:
                have = declared_inputs()
                names = " · ".join(str(x.relative_to(ROOT)) for x in have) or "없음"
            except SystemExit:
                names = "(선언을 못 읽었다)"
            print(f"         거울은 {tmp} · 선언에서 실제로 펼쳐진 입력 {names}")
            return 1
        if not made.exists():
            print("  [FAIL] 생성기가 rc=0 인데 페이지를 안 썼다")
            return 1
        after = made.read_text(encoding="utf-8")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    n_now, e_now = _counts(after)
    n_old, e_old = _counts(before)
    # ⚠ **원본 간선과 남은 간선을 둘 다 찍는다** (감사석). 생성기는 **남은 수**만 인쇄한다 — 한 수만
    #   보면 「0 개 버렸다」와 「5 개 버렸는데 5 개는 애초에 없던 변이다」가 같은 모양이다.
    kept = len(edges) - len(dropped)
    print(f"  chain.yaml 노드 {len(nodes)} · 간선 원본 {len(edges)} · 버리는 간선 {len(dropped)} "
          f"· 남는 간선 {kept}")
    print(f"  다시 만든 페이지 노드 {n_now} · 간선 {e_now} | 커밋된 페이지 노드 {n_old} · 간선 {e_old}")
    if dropped:
        print(f"  [FAIL] 끝점이 노드가 아닌 간선 {len(dropped)} 개 — "
              + " · ".join(f"{e['from']}→{e['to']}" for e in dropped[:3]))
        return 1
    if e_now != kept:
        print(f"  [FAIL] 페이지의 간선 {e_now} 이 «원본 {len(edges)} − 버린 것 {len(dropped)} = "
              f"{kept}» 과 다르다 — 생성기가 세는 것과 그래프가 다르다")
        return 1
    if after == before:
        # ⚠ 바이트와 문자를 갈라 적는다 — 두 좌석이 같은 파일을 105 902 와 92 567 로 읽고 한 바퀴를
        #   썼다. 하나는 `wc -c`, 하나는 문자였고 **둘 다 맞았다.**
        print(f"  [PASS] 커밋된 페이지가 이 sha 의 chain.yaml 과 같다 — 차이 0 · "
              f"{len(after.encode('utf-8'))} 바이트 · 문자 {len(after)}")
        return 0
    first = next((i + 1 for i, (a, b) in enumerate(zip(after.splitlines(), before.splitlines()))
                  if a != b), min(len(after.splitlines()), len(before.splitlines())) + 1)
    print(f"  [FAIL] 커밋된 페이지가 이 sha 의 chain.yaml 과 다르다 — "
          f"노드 {n_old} → {n_now} · 간선 {e_old} → {e_now} · 첫 다른 줄 {first} · "
          f"바이트 {len(before.encode('utf-8'))} → {len(after.encode('utf-8'))} "
          f"(문자 {len(before)} → {len(after)})")
    print("         다시 만든 것이 답이다. `python3 engine/build_graph_page.py` 를 이 커밋에서 "
          "돌리고 그 페이지를 커밋하라 (C86).")
    return 1


def main() -> int:
    """⚠ **이 검사는 나무를 안 바꾼다.** 판정을 내려면 페이지를 **지우고 다시 만들어야** 하는데
    (아무것도 안 쓴 실행이 통과하지 않게), 그 둘은 **격리 클론 안에서만** 무해하다. 격리는
    `--from <sha>` 일 때만 일어나므로, 인자 없이 부르면 이 단계가 **실행 중인 워크트리**에서 돈다 —
    감사석이 그 자리를 찾아냈다 (2026-09-14): 생성기가 거절하면 페이지가 **지워진 채** 남고,
    낡은 페이지를 커밋한 나무에서는 **덮어쓴 채** 「다시 만들어 커밋하라」고 말했다.

    그래서 **PASS 가 아닌 모든 출구에서 원본을 되쓴다.** 읽기 전용 계약을 다른 단계들과 맞춘다."""
    if not PAGE.exists():
        print("  [FAIL] 커밋된 페이지가 없다 — 대조할 대상이 없다")
        return 1
    return _judge(PAGE.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
