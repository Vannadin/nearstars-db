# 파생 파일 관문의 판 무관 코드 해시(§2) — 주석·docstring 을 토큰 자리로 지우고 줄 끝 공백·빈 줄을 버린 원문의 sha256 앞 16자
"""Version-stable source digest, prereg pc/sg-gate/prereg-sg-gate.frozen.md (1765b55c) §2.

digest(path) = sha256 of the source text with every COMMENT token removed by its token span (tokenize), every docstring
removed by its STRING token span (a docstring is the first statement of a module, class or function body when it is a
string constant, found with ast and matched to its token by start position), trailing whitespace stripped on each line,
lines left empty dropped, joined with «\\n»; the first 16 hex. Inputs are token positions in the text, not a printed tree,
so the value does not depend on the Python version (A2 measures it on 3.11, 3.12 and 3.14)."""
import ast
import hashlib
import io
import tokenize
from pathlib import Path

STAMP_RULE = "source-v1"


def _docstring_starts(tree):
    starts = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if (body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                starts.add((body[0].lineno, body[0].col_offset))
    return starts


def stripped(text: str) -> str:
    """The source with comments and docstrings cut by token span, trailing blanks stripped, empty lines dropped."""
    docs = _docstring_starts(ast.parse(text))
    lines = text.splitlines(keepends=True)
    offs = [0]
    for ln in lines:
        offs.append(offs[-1] + len(ln))
    cuts = []
    for tok in tokenize.generate_tokens(io.StringIO(text).readline):
        if tok.type == tokenize.COMMENT or (tok.type == tokenize.STRING and tok.start in docs):
            (r0, c0), (r1, c1) = tok.start, tok.end
            cuts.append((offs[r0 - 1] + c0, offs[r1 - 1] + c1))
    out, pos = [], 0
    for a, b in sorted(cuts):
        out.append(text[pos:a])
        pos = b
    out.append(text[pos:])
    kept = [ln.rstrip() for ln in "".join(out).splitlines()]
    return "\n".join(ln for ln in kept if ln)


def digest_text(text: str) -> str:
    return hashlib.sha256(stripped(text).encode("utf-8")).hexdigest()[:16]


def digest(path) -> str:
    return digest_text(Path(path).read_text(encoding="utf-8"))
