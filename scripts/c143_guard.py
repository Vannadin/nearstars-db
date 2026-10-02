# C143 가드 — fsum 자리를 건드리는 게이트 단계만 골라, 보통 sum() 과 3.9 식(왼쪽부터) sum() 훅으로 두 번 돌려 판정 줄이 하나도 안 뒤집히는지 본다
"""python3 scripts/c143_guard.py [--list] [--rule direct|closure]

prereg-c143-compensated-sum-boundaries (b17dcb5c) §1.8: the naive-`sum()` hook (`scripts/c143_naive_sum/sitecustomize.py`,
3.9's left-to-right `builtins.sum`) runs only on gate steps whose declared inputs or code touch an `fsum` site.
- `direct` (default): the step's own script is a C143 site, or C136's declarations (`scripts/gate_step_inputs.yaml`) list
  a site file among the step's inputs.
- `closure`: as `direct`, plus every step whose script imports (transitively, engine-local modules) a site module.
Without `--list`, each selected step runs twice (as shipped, and under the hook); the [PASS]/[FAIL] lines must match
one for one (0 flips). Differing non-verdict lines are counted and printed, not judged.
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


def run(step: str, hook: bool) -> list[str]:
    env = dict(os.environ)
    if hook:
        env["PYTHONPATH"] = str(ROOT / "scripts" / "c143_naive_sum") + os.pathsep + env.get("PYTHONPATH", "")
    r = subprocess.run([sys.executable, step], cwd=ENGINE, env=env, capture_output=True, text=True)
    return (r.stdout + r.stderr).splitlines()


def main() -> int:
    rule = sys.argv[sys.argv.index("--rule") + 1] if "--rule" in sys.argv else "direct"
    steps = select(rule)
    print(f"[c143-guard] rule {rule} · {len(steps)} step(s): {', '.join(steps)}")
    if "--list" in sys.argv:
        return 0
    flips = 0
    for step in steps:
        a, b = run(step, False), run(step, True)
        va, vb = [l.strip() for l in a if VERDICT.match(l)], [l.strip() for l in b if VERDICT.match(l)]
        kinds_a = [VERDICT.match(l).group(1) for l in va]
        kinds_b = [VERDICT.match(l).group(1) for l in vb]
        n_flip = sum(1 for x, y in zip(kinds_a, kinds_b) if x != y) + abs(len(kinds_a) - len(kinds_b))
        n_diff = sum(1 for x, y in zip(a, b) if x != y) + abs(len(a) - len(b))
        flips += n_flip
        print(f"  [{'PASS' if n_flip == 0 else 'FAIL'}] {step}: verdict lines {len(kinds_a)} · flips {n_flip} · "
              f"differing lines {n_diff} (recorded)")
    print(f"[c143-guard] {'PASS' if flips == 0 else 'FAIL'} · flips {flips}")
    return 0 if flips == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
