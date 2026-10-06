# 결과의 `.applicable` 을 판정(답인가)으로 읽는 자리를 잡는다 — 탈출구 `# verdict-ok: 까닭`, 지금 있는 자리는 줄기만 하는 기준표 (착지 3)
"""Flag reads of `applicable` that decide whether a result is used (landing 3 verdict_of draft 7f2d8d2e §2).

An AST scan, not a grep: a grep cannot tell a refusal check from an answer claim, and both polarities are
flagged anyway (`if not r.applicable: break` then `best = r` is the same claim as `if r.applicable`).

Flagged (strict pass):
- attribute loads `x.applicable`, and `getattr(x, "applicable", …)` with the string constant;
- calls, within the same file, of a function whose `return` value holds an unescaped flagged read
  (one level of interprocedural flow).
Not flagged: the bodies of `answer_verdict`, `verdict_of` and `is_answer` in `engine/interior.py` only.
Escape hatch: a `# verdict-ok: <why>` comment on the read's line. An empty reason is itself a FAIL.
Listed only (loose pass, hand-reviewed): subscript reads `x["applicable"]` and `x.get("applicable")`.

Gate mode (default, engine repo): every read is keyed by its **site**, (file, enclosing function, the
statement it sits in), and the count per site must equal `scripts/verdict_reads_baseline.json`. The statement is
the read's simple statement, or for a compound one (if / while / for / with) its header expression, as
`ast.unparse` with parentheses and whitespace dropped, so a moved line still matches and a 3.9 / 3.12
formatting difference does not. A rise is a new verdict read, including one swapped in for a removed one; a fall
means the baseline is stale and is lowered in the same commit.
`--write-baseline` writes the current sites but **refuses any site that rises** against the baseline committed at
HEAD (audit 89): the baseline only shrinks, as reads migrate to `verdict_of` / `is_answer` or get a reason.
Report mode (`--root DIR --report`): print the counts for any tree (the artifacts repo's kits), rc 0.

**Raising the baseline is a registration** (as with `gate_expected_red.yaml`: «칸을 더하거나 빼는 것은 등록»). The gate
compares only to the committed file, and an isolated archive has no HEAD to diff, so a hand-raised baseline would pass.
Every diff of `verdict_reads_baseline.json` goes to audit. A fall is written by `--write-baseline` in the commit that
removes the read.

Stated limit: a swap between textually identical sites in one function passes. Removing one `if r.applicable:` and
adding another `if r.applicable:` in the same function leaves the key «r.applicable» at the same count. The key is
text, not position, so that a moved line still matches.
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
EXEMPT_FILE = "engine/interior.py"     # 면제는 이 파일의 그 셋뿐 — 다른 곳의 같은 이름 도우미는 읽기를 숨기지 못한다(감사 89)
OK_RE = re.compile(r"#\s*verdict-ok\b(:?)(.*)$")
ENGINE_SCOPE = (re.compile(r"^engine/[^/]+\.py$"), re.compile(r"^engine/tools/[^/]+\.py$"),
                re.compile(r"^scripts/[^/]+\.py$"))
BASELINE = "scripts/verdict_reads_baseline.json"
FORMAT = 2


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


def _norm(text: str) -> str:
    return re.sub(r"[()\s]", "", text)


def _site(node: ast.AST, parents: dict) -> str:
    """읽기가 앉은 문장 — 단순 문장이면 그 문장, 복합 문장(if · while · for · with …)이면 읽기를 품은 머리 식."""
    child, up = node, parents.get(node)
    while up is not None and not isinstance(up, ast.stmt):
        child, up = up, parents.get(up)
    if up is None:
        return _norm(ast.unparse(child))
    if any(isinstance(getattr(up, f, None), list) and getattr(up, f) and isinstance(getattr(up, f)[0], ast.stmt)
           for f in ("body", "orelse", "finalbody", "handlers")):
        return _norm(ast.unparse(child))       # 복합 문장 — 몸통이 바뀌어도 자리 열쇠는 머리 식
    return _norm(ast.unparse(up))


class _Scan(ast.NodeVisitor):
    def __init__(self, comments: dict[int, str], parents: dict, exempt_ok: bool):
        self.comments = comments
        self.parents = parents
        self.exempt_ok = exempt_ok
        self.stack: list[str] = []
        self.reads: list[tuple[int, str, str, str]] = []     # (line, qualname, what, site) — unescaped strict reads
        self.escaped: list[tuple[int, str, str]] = []        # (line, qualname, reason)
        self.loose: list[tuple[int, str]] = []
        self.sources: set[str] = set()                       # functions whose return holds an unescaped read
        self.calls: list[tuple[int, str, str, str]] = []     # (line, qualname, callee, site) — every call by name

    def _qual(self) -> str:
        return ".".join(self.stack) or "<module>"

    def _exempt(self) -> bool:
        return self.exempt_ok and any(n in EXEMPT_FUNCS for n in self.stack)

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
            self.calls.append((node.lineno, self._qual(), name, _site(node, self.parents)))
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
                self.reads.append((node.lineno, self._qual(), "getattr" if isinstance(node, ast.Call) else ".applicable",
                                   _site(node, self.parents)))
        elif _is_loose(node):
            self.loose.append((node.lineno, self._qual()))


def scan_source(src: str, path: str = "<src>") -> dict:
    """한 파일의 판정 읽기 — {"reads", "escaped", "loose", "empty_ok"}. reads 의 칸은 (줄, 함수, 무엇, 자리)."""
    comments = _comments(src)
    tree = ast.parse(src, path)
    parents = {c: n for n in ast.walk(tree) for c in ast.iter_child_nodes(n)}
    sc = _Scan(comments, parents, exempt_ok=(path == EXEMPT_FILE))
    sc.visit(tree)
    reads = list(sc.reads)
    for line, qual, callee, site in sc.calls:
        if callee in sc.sources and qual.split(".")[-1] != callee:
            why = sc._escape(line)
            if why:
                sc.escaped.append((line, qual, why))
            else:
                reads.append((line, qual, f"{callee}() — 판정 원천", site))
    empty = [ln for ln, c in comments.items() if (m := OK_RE.search(c)) and not (m.group(1) and m.group(2).strip())]
    return {"reads": sorted(reads), "escaped": sorted(sc.escaped), "loose": sorted(sc.loose), "empty_ok": sorted(empty)}


def sites(per_file: dict[str, dict]) -> dict[str, dict[str, dict[str, int]]]:
    """{파일: {함수: {자리: 셈}}}."""
    out: dict = {}
    for path, res in per_file.items():
        for _line, qual, _what, site in res["reads"]:
            d = out.setdefault(path, {}).setdefault(qual, {})
            d[site] = d.get(site, 0) + 1
    return out


def _flat(s: dict) -> dict[tuple[str, str, str], int]:
    return {(p, q, st): n for p, qs in s.items() for q, ss in qs.items() for st, n in ss.items()}


def rises(now: dict, base: dict) -> list[tuple[tuple[str, str, str], int, int]]:
    a, b = _flat(now), _flat(base)
    return [(k, a[k], b.get(k, 0)) for k in sorted(a) if a[k] > b.get(k, 0)]


def compare(now: dict, base: dict) -> list[str]:
    """기준표와 자리마다 정확히 같아야 한다 — 늘면 새 판정 읽기(빠진 것과 바꿔 들어온 것 포함), 줄면 기준표가 낡음."""
    a, b = _flat(now), _flat(base)
    fails = []
    for k in sorted(set(a) | set(b)):
        n, e = a.get(k, 0), b.get(k, 0)
        path, qual, site = k
        if n > e:
            fails.append(f"[FAIL] 새 판정 읽기 {path} · {qual} · {site[:90]}: {n} (기준 {e}) — verdict_of / is_answer 로 읽거나 "
                         "`# verdict-ok: 까닭`")
        elif n < e:
            fails.append(f"[FAIL] 기준표가 낡음 {path} · {qual} · {site[:90]}: {n} (기준 {e}) — 같은 커밋에서 --write-baseline")
    return fails


def committed_baseline(root: pathlib.Path) -> dict | None:
    try:
        out = subprocess.run(["git", "show", f"HEAD:{BASELINE}"], cwd=root, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return json.loads(out)


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


def write_baseline(engine_root: pathlib.Path, now: dict, reformat: bool) -> int:
    """지금 자리들을 쓴다 — HEAD 의 기준표보다 느는 자리가 하나라도 있으면 거절(톱니는 내려가기만)."""
    old = committed_baseline(engine_root)
    total_now = 0
    for n in _flat(now).values():
        total_now += n
    if old is None:
        print(f"  [거절] HEAD 에 {BASELINE} 가 없다 — 처음 쓰기는 등록으로(이 검사기를 들이는 커밋)")
        return 1
    if old.get("format") != FORMAT:
        if not reformat:
            print(f"  [거절] HEAD 의 기준표가 형식 {old.get('format', 1)} — 형식을 바꾸려면 --reformat (총수가 늘면 거절)")
            return 1
        total_old = 0
        for qs in old.values():
            for n in qs.values():
                total_old += n
        if total_now > total_old:
            print(f"  [거절] 형식 바꾸기에서 총수가 늘었다 {total_old} → {total_now}")
            return 1
        print(f"  형식 {old.get('format', 1)} → {FORMAT}, 총수 {total_old} → {total_now}")
    else:
        up = rises(now, old["sites"])
        if up:
            for (path, qual, site), n, e in up:
                print(f"  [거절] 느는 자리 {path} · {qual} · {site[:90]}: {e} → {n}")
            print("  기준표를 안 썼다 — 새 판정 읽기는 verdict_of / is_answer 로 읽거나 `# verdict-ok: 까닭` 을 단다")
            return 1
    with open(engine_root / BASELINE, "w", encoding="utf-8", newline="\n") as fh:     # 3.9 의 write_text 엔 newline 이 없다
        fh.write(json.dumps({"format": FORMAT, "sites": now}, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
    print(f"  기준표를 썼다 {BASELINE} (자리 {len(_flat(now))} · 읽기 {total_now})")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", type=pathlib.Path, default=None, help="훑을 트리(기본: 이 엔진 레포)")
    ap.add_argument("--report", action="store_true", help="기준표 없이 셈만 인쇄, rc 0 (아티팩트 레포 등)")
    ap.add_argument("--write-baseline", action="store_true", help="지금 자리들로 기준표를 다시 쓴다 — HEAD 보다 느는 자리가 있으면 거절")
    ap.add_argument("--reformat", action="store_true", help="--write-baseline 과 함께: HEAD 의 옛 형식 기준표를 새 형식으로(총수가 늘면 거절)")
    ap.add_argument("-v", "--verbose", action="store_true", help="읽기 자리 하나하나 · 느슨한 목록 인쇄")
    a = ap.parse_args(argv)
    engine_root = pathlib.Path(__file__).resolve().parent.parent
    root = (a.root or engine_root).resolve()
    engine_scope = a.root is None
    per_file, fails = run(root, engine_scope)
    now = sites(per_file)
    n_reads = n_esc = n_loose = 0          # 정수 셈 — C143 의 sum() 목록(3.12 에서 쓴 문자열)에 안 걸리게 sum() 을 안 쓴다
    for path, r in sorted(per_file.items()):
        n_reads += len(r["reads"])
        n_esc += len(r["escaped"])
        n_loose += len(r["loose"])
        if r["reads"]:
            print(f"  {path}: {len(r['reads'])}")
        if a.verbose:
            for line, qual, what, site in r["reads"]:
                print(f"    {line} {qual} {what} · {site[:100]}")
            for line, qual in r["loose"]:
                print(f"    [느슨] {line} {qual}")
    print(f"파일 {len(per_file)} · 판정 읽기 {n_reads} · 까닭 단 탈출 {n_esc} · 느슨한 목록 {n_loose}")
    if a.write_baseline:
        return write_baseline(engine_root, now, a.reformat) or (1 if fails else 0)
    if a.report:
        print("\n".join(fails))
        return 0
    base = json.loads((engine_root / BASELINE).read_text(encoding="utf-8"))
    if base.get("format") != FORMAT:
        fails.append(f"[FAIL] 기준표 형식 {base.get('format', 1)} ≠ {FORMAT} — --write-baseline --reformat")
    else:
        fails += compare(now, base["sites"])
    print("\n".join(fails))
    if not fails:
        print("  [PASS] 판정 읽기가 기준표와 자리마다 같다(새 `.applicable` 판정 읽기 없음)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
