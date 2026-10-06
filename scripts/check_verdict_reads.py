# 결과의 `.applicable` 을 판정(답인가)으로 읽는 자리를 잡는다 — 탈출구 `# verdict-ok: 까닭`, 지금 있는 자리는 줄기만 하는 기준표 (착지 3)
"""Flag reads of `applicable` that decide whether a result is used (landing 3 verdict_of draft 7f2d8d2e §2).

An AST scan, not a grep: a grep cannot tell a refusal check from an answer claim, and both polarities are
flagged anyway (`if not r.applicable: break` then `best = r` is the same claim as `if r.applicable`).

Flagged (strict pass):
- attribute loads `x.applicable`, and `getattr(x, "applicable", …)` with the string constant;
- calls, within the same file, of a function whose `return` value holds an unescaped flagged read
  (one level of interprocedural flow).
Not flagged: the bodies of `answer_verdict`, `verdict_of` and `is_answer`.
Escape hatch: a `# verdict-ok: <why>` comment on the read's line. An empty reason is itself a FAIL.
Listed only (loose pass, hand-reviewed): subscript reads `x["applicable"]` and `x.get("applicable")`.

Gate mode (default, engine repo): the strict count per (file, enclosing function) must equal
`scripts/verdict_reads_baseline.json`. A rise is a new verdict read; a fall means the baseline is stale and is
lowered in the same commit (`--write-baseline`). The baseline only shrinks as reads migrate to `verdict_of` /
`is_answer` or get a `# verdict-ok:` reason.
Report mode (`--root DIR --report`): print the counts for any tree (the artifacts repo's kits), rc 0.
"""
from __future__ import annotations

import argparse
import ast
import io
import json
import pathlib
import re
import subprocess
import sys
import tokenize

EXEMPT_FUNCS = {"answer_verdict", "verdict_of", "is_answer"}
OK_RE = re.compile(r"#\s*verdict-ok\b(:?)(.*)$")
ENGINE_SCOPE = (re.compile(r"^engine/[^/]+\.py$"), re.compile(r"^engine/tools/[^/]+\.py$"),
                re.compile(r"^scripts/[^/]+\.py$"))
BASELINE = "scripts/verdict_reads_baseline.json"


def _comments(src: str) -> dict[int, str]:
    out: dict[int, str] = {}
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type == tokenize.COMMENT:
                out[tok.start[0]] = tok.string
    except (tokenize.TokenError, IndentationError):
        pass
    return out


def _is_read(node: ast.AST) -> bool:
    if isinstance(node, ast.Attribute) and node.attr == "applicable" and isinstance(node.ctx, ast.Load):
        return True
    return (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "getattr"
            and len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and node.args[1].value == "applicable")


def _is_loose(node: ast.AST) -> bool:
    if isinstance(node, ast.Subscript):
        sl = node.slice
        sl = getattr(sl, "value", sl) if type(sl).__name__ == "Index" else sl     # Python 3.8 Index
        return isinstance(sl, ast.Constant) and sl.value == "applicable"
    return (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "get"
            and node.args and isinstance(node.args[0], ast.Constant) and node.args[0].value == "applicable")


class _Scan(ast.NodeVisitor):
    def __init__(self, comments: dict[int, str]):
        self.comments = comments
        self.stack: list[str] = []
        self.reads: list[tuple[int, str, str]] = []      # (line, qualname, what) — unescaped strict reads
        self.escaped: list[tuple[int, str, str]] = []    # (line, qualname, reason)
        self.loose: list[tuple[int, str]] = []
        self.sources: set[str] = set()                   # functions whose return holds an unescaped read
        self.calls: list[tuple[int, str, str]] = []      # (line, qualname, callee) — every call by name

    def _qual(self) -> str:
        return ".".join(self.stack) or "<module>"

    def _exempt(self) -> bool:
        return any(n in EXEMPT_FUNCS for n in self.stack)

    def _escape(self, line: int) -> str | None:
        m = OK_RE.search(self.comments.get(line, ""))
        return m.group(2).strip() if m and m.group(1) else None

    def _func(self, node):
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    visit_FunctionDef = visit_AsyncFunctionDef = visit_ClassDef = _func

    def visit_Return(self, node: ast.Return):
        if node.value is not None and not self._exempt() and self.stack:
            for sub in ast.walk(node.value):
                if _is_read(sub) and not self._escape(sub.lineno):
                    self.sources.add(self.stack[-1])
                    break
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        f = node.func
        name = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else None
        if name and not self._exempt():
            self.calls.append((node.lineno, self._qual(), name))
        self._check(node)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        self._check(node)
        self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript):
        self._check(node)
        self.generic_visit(node)

    def _check(self, node):
        if self._exempt():
            return
        if _is_read(node):
            why = self._escape(node.lineno)
            if why:
                self.escaped.append((node.lineno, self._qual(), why))
            else:
                self.reads.append((node.lineno, self._qual(), "getattr" if isinstance(node, ast.Call) else ".applicable"))
        elif _is_loose(node):
            self.loose.append((node.lineno, self._qual()))


def scan_source(src: str, path: str = "<src>") -> dict:
    """한 파일의 판정 읽기 — {"reads", "escaped", "loose", "empty_ok"}. reads 의 칸은 (줄, 함수, 무엇)."""
    comments = _comments(src)
    tree = ast.parse(src, path)
    sc = _Scan(comments)
    sc.visit(tree)
    reads = list(sc.reads)
    for line, qual, callee in sc.calls:
        if callee in sc.sources and qual.split(".")[-1] != callee:
            why = sc._escape(line)
            if why:
                sc.escaped.append((line, qual, why))
            else:
                reads.append((line, qual, f"{callee}() — 판정 원천"))
    empty = [ln for ln, c in comments.items() if (m := OK_RE.search(c)) and not (m.group(1) and m.group(2).strip())]
    return {"reads": sorted(reads), "escaped": sorted(sc.escaped), "loose": sorted(sc.loose), "empty_ok": sorted(empty)}


def counts(per_file: dict[str, dict]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for path, res in per_file.items():
        for _line, qual, _what in res["reads"]:
            out.setdefault(path, {}).setdefault(qual, 0)
            out[path][qual] += 1
    return out


def compare(now: dict[str, dict[str, int]], base: dict[str, dict[str, int]]) -> list[str]:
    """기준표와 정확히 같아야 한다 — 늘면 새 판정 읽기, 줄면 기준표가 낡음(같은 커밋에서 낮춘다)."""
    fails = []
    for path in sorted(set(now) | set(base)):
        n, b = now.get(path, {}), base.get(path, {})
        for qual in sorted(set(n) | set(b)):
            a, e = n.get(qual, 0), b.get(qual, 0)
            if a > e:
                fails.append(f"[FAIL] 새 판정 읽기 {path} · {qual}: {a} (기준 {e}) — verdict_of / is_answer 로 읽거나 `# verdict-ok: 까닭`")
            elif a < e:
                fails.append(f"[FAIL] 기준표가 낡음 {path} · {qual}: {a} (기준 {e}) — 줄었으면 같은 커밋에서 --write-baseline")
    return fails


def files(root: pathlib.Path, engine_scope: bool) -> list[str]:
    try:
        out = subprocess.run(["git", "ls-files", "*.py"], cwd=root, capture_output=True, text=True, check=True).stdout.split("\n")
    except (OSError, subprocess.CalledProcessError):
        out = [str(p.relative_to(root)) for p in root.rglob("*.py")]
    out = [p for p in out if p]
    if engine_scope:
        out = [p for p in out if any(r.match(p) for r in ENGINE_SCOPE)]
    return sorted(out)


def run(root: pathlib.Path, engine_scope: bool) -> tuple[dict[str, dict], list[str]]:
    per_file, fails = {}, []
    for p in files(root, engine_scope):
        try:
            src = (root / p).read_text(encoding="utf-8")
        except FileNotFoundError:
            fails.append(f"[FAIL] 추적 파일을 못 읽음 {p} — 작업 트리에서 지워졌나")
            continue
        try:
            per_file[p] = scan_source(src, p)
        except SyntaxError as e:
            fails.append(f"[FAIL] 구문 오류로 못 훑음 {p}: {e}")
            continue
        for ln in per_file[p]["empty_ok"]:
            fails.append(f"[FAIL] 까닭 빈 `# verdict-ok` {p}:{ln}")
    return per_file, fails


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", type=pathlib.Path, default=None, help="훑을 트리(기본: 이 엔진 레포)")
    ap.add_argument("--report", action="store_true", help="기준표 없이 셈만 인쇄, rc 0 (아티팩트 레포 등)")
    ap.add_argument("--write-baseline", action="store_true", help="지금 셈으로 기준표를 다시 쓴다 — 줄어든 이동만 커밋")
    ap.add_argument("-v", "--verbose", action="store_true", help="읽기 자리 하나하나 · 느슨한 목록 인쇄")
    a = ap.parse_args(argv)
    engine_root = pathlib.Path(__file__).resolve().parent.parent
    root = (a.root or engine_root).resolve()
    engine_scope = a.root is None
    per_file, fails = run(root, engine_scope)
    now = counts(per_file)
    n_reads = n_esc = n_loose = 0          # 정수 셈 — C143 의 sum() 목록(3.12 에서 쓴 문자열)에 안 걸리게 sum() 을 안 쓴다
    for r in per_file.values():
        n_reads += len(r["reads"])
        n_esc += len(r["escaped"])
        n_loose += len(r["loose"])
    for path in sorted(now):
        n_file = 0
        for n in now[path].values():
            n_file += n
        print(f"  {path}: {n_file}")
        if a.verbose:
            for line, qual, what in per_file[path]["reads"]:
                print(f"    {line} {qual} {what}")
    if a.verbose:
        for path, r in sorted(per_file.items()):
            for line, qual in r["loose"]:
                print(f"  [느슨] {path}:{line} {qual}")
    print(f"파일 {len(per_file)} · 판정 읽기 {n_reads} · 까닭 단 탈출 {n_esc} · 느슨한 목록 {n_loose}")
    if a.write_baseline:
        with open(engine_root / BASELINE, "w", encoding="utf-8", newline="\n") as fh:     # 3.9 의 write_text 엔 newline 이 없다
            fh.write(json.dumps(now, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
        print(f"  기준표를 썼다 {BASELINE}")
        return 0
    if a.report:
        print("\n".join(fails))
        return 0
    base = json.loads((engine_root / BASELINE).read_text(encoding="utf-8"))
    fails += compare(now, base)
    print("\n".join(fails))
    if not fails:
        print("  [PASS] 판정 읽기가 기준표와 같다(새 `.applicable` 판정 읽기 없음)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
