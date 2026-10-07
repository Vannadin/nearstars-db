# C143 가드 — fsum 자리를 건드리는 게이트 단계만 골라, 보통 sum() 과 3.9 식(왼쪽부터) sum() 훅으로 두 번 돌려 판정 줄이 하나도 안 뒤집히는지 본다
"""python3 scripts/c143_guard.py [--list] [--rule direct|closure]

prereg-c143-compensated-sum-boundaries (b17dcb5c) §1.8: the naive-`sum()` hook (`scripts/c143_naive_sum/sitecustomize.py`,
3.9's left-to-right `builtins.sum`) runs only on gate steps whose declared inputs or code touch an `fsum` site.
- `direct` (default): the step's own script is a C143 site, or C136's declarations (`scripts/gate_step_inputs.yaml`) list
  a site file among the step's inputs.
- `closure`: as `direct`, plus every step whose script imports (transitively, engine-local modules) a site module.
Without `--list`, each selected step runs twice (as shipped, and under the hook); the [PASS]/[FAIL] lines must match
one for one (0 flips). Differing non-verdict lines are counted and printed, not judged.

Post-freeze note 2 (bit-identity rows), with audit e2's condition: rows are classified by an explicit list (`ROWS`,
step + row text, the note's §3 census as data). A listed «frozen» row (bit identity against a frozen anchor, table or
pin) that flips is class (b): recorded with both outcomes, not a flip. A listed «same-run» row stays a verdict. A row
that carries a bit-identity form (`BIT`) but is not on the list FAILs, so a new one cannot pass unclassified.
`--controls` runs the note's §4 fixture: a plain row whose compensated ≠ left-to-right sum must count as 1 flip, the
same row in a listed «앵커와 비트 동일» form must be class (b), and an unlisted bit-identity row must FAIL. On 3.9
(`sum()` already left to right) the fixture cannot differ and the controls print «vacuous on 3.9».
"""
from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
#: the C143 sites: engine modules with an fsum, and the tests that carry a C143 check themselves
SITE_MODULES = {"mantle_composition", "samuel_lid"}
SITE_TESTS = {"test_mantle_composition.py", "test_interior.py", "test_radiogenic.py", "test_mixture.py",
              "test_samuel_lid.py"}
STEP = re.compile(r"""^step "([^"]+\.py)" bash -c 'cd engine && exec python3 \1'""", re.M)
VERDICT = re.compile(r"^\s*\[(PASS|FAIL)\]")
#: bit-identity text forms (note 2 §2)
BIT = re.compile(r"비트까지 같다|비트 동일|비트까지 동일")
#: note 2 §3 census — (step, regex on the row text after [PASS]/[FAIL], class). «frozen» flips are class (b).
ROWS = [
    ("test_ice_giant.py", r"^\S+ — 수렴점에서 적분 한 번 ", "frozen"),
    ("test_ice_giant.py", r"^\S+ — 전체 풀이 \d+ s", "frozen"),
    ("test_ice_giant.py", r"^교란-불변 \(", "frozen"),
    ("test_interior.py", r"^전선 1\.0 = 지각 없음: 기본 풀이와 비트까지 같다", "same-run"),
    ("test_mixture.py", r"^목성 envelope_z=0 이 기본 호출과 비트까지 같다", "same-run"),
    ("test_mantle_composition.py", r"^선언 없는 지구 — 입구 대 몸통 값 비트 동일", "same-run"),
    ("test_structure_grid.py", r"^덧붙임 60 후속 — 이력 무관: 고정 풀이 한 번 뒤에도 지구 2062 K ", "same-run"),   # _hA 대 _hB, 한 실행 안의 두 풀이
    # --controls 의 픽스처 (note 2 §4)
    ("<controls>", r"^c143 control — 앵커와 비트 동일", "frozen"),
]


def engine_steps() -> list[str]:
    return STEP.findall((ROOT / "scripts" / "check.sh").read_text(encoding="utf-8"))


def declared_inputs() -> dict[str, list[str]]:
    out, cur = {}, None
    for line in (ROOT / "scripts" / "gate_step_inputs.yaml").read_text(encoding="utf-8").splitlines():
        m = re.match(r'^"([^"]+)":', line)
        if m:
            cur = m.group(1)
        elif cur and line.strip().startswith("globs:"):
            out[cur] = re.findall(r'"([^"]+)"', line)
    return out


def imports(module: str, seen: set[str]) -> set[str]:
    path = ENGINE / f"{module}.py"
    if module in seen or not path.exists():
        return seen
    seen.add(module)
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        names = ([a.name for a in node.names] if isinstance(node, ast.Import) else
                 [node.module] if isinstance(node, ast.ImportFrom) and node.module and not node.level else [])
        for n in names:
            imports(n.split(".")[0], seen)
    return seen


def select(rule: str) -> list[str]:
    decl = declared_inputs()
    picked = []
    for step in engine_steps():
        globs = decl.get(step, [])
        direct = step in SITE_TESTS or any(f"engine/{m}.py" in globs for m in SITE_MODULES)
        closure = bool(imports(step[:-3], set()) & SITE_MODULES)
        if direct or (rule == "closure" and closure):
            picked.append(step)
    return picked


def run(step: str, hook: bool, argv: list[str] | None = None) -> list[str]:
    env = dict(os.environ)
    if hook:
        env["PYTHONPATH"] = str(ROOT / "scripts" / "c143_naive_sum") + os.pathsep + env.get("PYTHONPATH", "")
    r = subprocess.run(argv or [sys.executable, step], cwd=ENGINE, env=env, capture_output=True, text=True)
    return (r.stdout + r.stderr).splitlines()


def row_class(step: str, line: str) -> str | None:
    """«frozen» · «same-run» from `ROWS`, «unlisted» for a bit-identity row not on the list, None otherwise."""
    text = VERDICT.sub("", line, count=1).strip()
    for s, pat, cls in ROWS:
        if s == step and re.search(pat, text):
            return cls
    return "unlisted" if BIT.search(text) else None


def compare(step: str, a: list[str], b: list[str]) -> tuple[int, list[str], list[str], int]:
    """(flips, class-(b) rows, unlisted bit-identity rows, differing lines) for one step's two runs."""
    va, vb = [l.strip() for l in a if VERDICT.match(l)], [l.strip() for l in b if VERDICT.match(l)]
    flips, class_b, unlisted = abs(len(va) - len(vb)), [], []
    for x, y in zip(va, vb):
        cls = row_class(step, x) or row_class(step, y)
        if cls == "unlisted":
            unlisted.append(x)
        flipped = VERDICT.match(x).group(1) != VERDICT.match(y).group(1)
        if flipped and cls == "frozen":
            class_b.append(f"{x}  ⇄  {y}")
        elif flipped:
            flips += 1
    n_diff = sum(1 for x, y in zip(a, b) if x != y) + abs(len(a) - len(b))
    return flips, class_b, unlisted, n_diff


#: note 2 §4 — compensated sum([1e16, 1.0, -1e16]) is 1.0, left to right 0.0
CONTROL = ("s = sum([1e16, 1.0, -1e16]); ok = s == 1.0\n"
           "print(f\"  [{'PASS' if ok else 'FAIL'}] c143 control — plain row, sum = {s}\")\n"
           "print(f\"  [{'PASS' if ok else 'FAIL'}] c143 control — 앵커와 비트 동일, sum = {s}\")\n"
           "print(f\"  [PASS] c143 control — unlisted row 비트 동일\")\n")


def controls() -> int:
    argv = [sys.executable, "-c", CONTROL]
    flips, class_b, unlisted, _ = compare("<controls>", run("", False, argv), run("", True, argv))
    if sum([1e16, 1.0, -1e16]) == 0.0:
        print(f"[c143-guard] controls vacuous on {sys.version.split()[0]} (sum() is already left to right) — "
              f"flips {flips} · class (b) {len(class_b)} · unlisted {len(unlisted)}")
        return 0
    good = flips == 1 and len(class_b) == 1 and len(unlisted) == 1
    print(f"  [{'PASS' if good else 'FAIL'}] c143 controls: plain row flips {flips} (want 1) · listed bit row class (b) "
          f"{len(class_b)} (want 1) · unlisted bit row caught {len(unlisted)} (want 1)")
    return 0 if good else 1


def main() -> int:
    rule = sys.argv[sys.argv.index("--rule") + 1] if "--rule" in sys.argv else "direct"
    steps = select(rule)
    print(f"[c143-guard] rule {rule} · {len(steps)} step(s): {', '.join(steps)}")
    if "--list" in sys.argv:
        return 0
    if "--controls" in sys.argv:
        return controls()
    flips = unl = 0
    for step in steps:
        a, b = run(step, False), run(step, True)
        n_flip, class_b, unlisted, n_diff = compare(step, a, b)
        flips += n_flip
        unl += len(unlisted)
        bad = n_flip or unlisted
        print(f"  [{'FAIL' if bad else 'PASS'}] {step}: verdict lines {sum(1 for l in a if VERDICT.match(l))} · "
              f"flips {n_flip} · class (b) {len(class_b)} · unlisted bit-identity {len(unlisted)} · "
              f"differing lines {n_diff} (recorded)")
        for row in class_b:
            print(f"      class (b): {row}")
        for row in unlisted:
            print(f"      unlisted bit-identity row: {row}")
    rc = controls()
    ok = flips == 0 and unl == 0 and rc == 0
    print(f"[c143-guard] {'PASS' if ok else 'FAIL'} · flips {flips} · unlisted bit-identity rows {unl}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
