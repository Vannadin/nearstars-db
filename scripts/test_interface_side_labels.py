# 경계 온도에 한쪽 이름을 단 키·문구가 관례 문장 없이 새로 생기지 못하게 하는 게이트 검사 (C153)
"""Interface-side labels guard (prereg-c153-interface-side-labels, with post-freeze note 1).

    python3 scripts/test_interface_side_labels.py

Hits, at the repo root:
  (i)  string keys of dict literals under `values` (the `values=` keyword or a `values = {…}` assignment) in
       engine/*.py that contain `temperature` and have `core` / `mantle` as a whole `_`-separated word;
  (ii) the exact texts «핵 쪽» «맨틀 쪽» «core side» «core-side» «mantle side» «mantle-side» anywhere in engine/*.py
       and engine/chain.yaml.
Each hit is fine if its module is on the real-side list (core_history.py, core_energy.py, cmb_flux.py) or if
scripts/interface_side_labels.txt carries a line `<path>:<hit> — <reason>` for that exact path and hit, whose reason
contains one of the three exact strings in REASONS. Anything else is a FAIL with its path and hit.
⚠ Text hits carry their occurrence count (audit e2): the line is `<path>:<text> ×N — <reason>`, and a different
count in the module FAILs, so a new side text in an already allow-listed module forces a reviewed line.
Stated non-reach (note 1): keys added by `v.update({…})` or `values[...] = …` are not dict literals under `values`.
"""
from __future__ import annotations

import ast
import pathlib
import re
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALLOW = pathlib.Path(__file__).resolve().with_name("interface_side_labels.txt")
SIDE = re.compile(r"(^|_)(core|mantle)(_|$)")
TEXTS = ("핵 쪽", "맨틀 쪽", "core side", "core-side", "mantle side", "mantle-side")
REAL_SIDE = ("engine/core_history.py", "engine/core_energy.py", "engine/cmb_flux.py")
REASONS = ("equals the other side unless a jump is declared", "is the physical side",
           "names a layer, not an interface side")


def _values_dicts(tree: ast.AST):
    for node in ast.walk(tree):
        if isinstance(node, ast.keyword) and node.arg == "values" and isinstance(node.value, ast.Dict):
            yield node.value
        elif (isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict)
              and any(isinstance(t, ast.Name) and t.id == "values" for t in node.targets)):
            yield node.value


def hits(root: pathlib.Path) -> list[tuple[str, str]]:
    out = []
    for f in sorted((root / "engine").glob("*.py")):
        rel = f.relative_to(root).as_posix()
        src = f.read_text(encoding="utf-8")
        try:
            tree = ast.parse(src)
        except SyntaxError:
            tree = None
        keys = set()
        for d in (_values_dicts(tree) if tree else ()):
            for k in d.keys:
                if (isinstance(k, ast.Constant) and isinstance(k.value, str)
                        and "temperature" in k.value and SIDE.search(k.value)):
                    keys.add(k.value)
        out += [(rel, k) for k in sorted(keys)]
        out += [(rel, f"{x} ×{src.count(x)}") for x in TEXTS if x in src]
    chain = root / "engine" / "chain.yaml"
    if chain.exists():
        src = chain.read_text(encoding="utf-8")
        out += [("engine/chain.yaml", f"{x} ×{src.count(x)}") for x in TEXTS if x in src]
    return out


def load_allow(path: pathlib.Path) -> dict[tuple[str, str], str]:
    allow = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or " — " not in line or ":" not in line.split(" — ", 1)[0]:
                continue
            head, reason = line.split(" — ", 1)
            p, h = head.split(":", 1)
            allow[(p.strip(), h.strip())] = reason.strip()
    return allow


def check(root: pathlib.Path, allow_path: pathlib.Path) -> tuple[list[str], list[tuple[str, str, str]]]:
    allow = load_allow(allow_path)
    fails, rows = [], []
    for p, h in hits(root):
        if p in REAL_SIDE:
            rows.append((p, h, "real-side list"))
            continue
        reason = allow.get((p, h))
        if reason is None and " ×" in h:
            text = h.rsplit(" ×", 1)[0]
            other = [k[1] for k in allow if k[0] == p and k[1].rsplit(" ×", 1)[0] == text]
            if other:
                fails.append(f"[FAIL] interface_side_labels — {p}: «{text}» count changed "
                             f"(allow-list {other[0].rsplit(' ', 1)[1]}, found {h.rsplit(' ', 1)[1]}) — review the new text")
                continue
        if reason is None:
            fails.append(f"[FAIL] interface_side_labels — {p}: {h} — no side rule")
        elif not any(r in reason for r in REASONS):
            fails.append(f"[FAIL] interface_side_labels — {p}: {h} — reason lacks the rule string")
        else:
            rows.append((p, h, next(r for r in REASONS if r in reason)))
    return fails, rows


def _scratch(files: dict[str, str], allow: str) -> tuple[pathlib.Path, pathlib.Path]:
    root = pathlib.Path(tempfile.mkdtemp())
    (root / "engine").mkdir()
    for name, body in files.items():
        (root / "engine" / name).write_text(body, encoding="utf-8")
    a = root / "allow.txt"
    a.write_text(allow, encoding="utf-8")
    return root, a


def _fixtures() -> list[str]:
    bad = []
    COLON = ":"   # 허용 목록 줄을 조립한다 — «경로.py:» 꼴이 원문에 있으면 인용 검사기가 인용으로 읽는다
    k = 'values={"foo_temperature_core": 1.0}\n'
    cases = [
        ("S-guard: no line", {"x.py": f"f({k})"}, "", "no side rule"),
        ("S-guard: reason lacks the string", {"x.py": f"f({k})"}, f"engine/x.py{COLON}foo_temperature_core — because\n",
         "reason lacks the rule string"),
        ("S-guard: valid line", {"x.py": f"f({k})"},
         f"engine/x.py{COLON}foo_temperature_core — equals the other side unless a jump is declared\n", None),
        ("S-guard: real-side module", {"core_energy.py": f"f({k})"}, "", None),
        ("S-guard-prefix", {"x.py": 'f(values={"core_foo_temperature_used": 1.0})\n'}, "", "no side rule"),
        ("S-guard-path", {"a.py": 'values = {"x_mantle_temperature_floor": 1}\n',
                          "b.py": 'values = {"x_mantle_temperature_floor": 1}\n'},
         f"engine/a.py{COLON}x_mantle_temperature_floor — names a layer, not an interface side\n", "engine/b.py"),
        ("S-guard-layer", {"x.py": 'values = {"mantle_temperature_width": 1}\n'},
         f"engine/x.py{COLON}mantle_temperature_width — names a layer, not an interface side\n", None),
        ("text rule", {"x.py": "# 핵 쪽 경계 온도\n"}, "", "no side rule"),
        ("text count", {"x.py": "# 핵 쪽 경계 온도\n# 핵 쪽 다시\n"},
         f"engine/x.py{COLON}핵 쪽 ×1 — is the physical side\n", "count changed"),
        ("text count ok", {"x.py": "# 핵 쪽 경계 온도\n"},
         f"engine/x.py{COLON}핵 쪽 ×1 — is the physical side\n", None),
    ]
    for name, files, allow, expect in cases:
        root, a = _scratch(files, allow)
        fails, _ = check(root, a)
        ok = (not fails) if expect is None else (len(fails) == 1 and expect in fails[0])
        print(f"  [{'PASS' if ok else 'FAIL'}] fixture {name} → {fails[0] if fails else 'clean'}")
        if not ok:
            bad.append(name)
    return bad


def main() -> int:
    bad = _fixtures()
    fails, rows = check(ROOT, ALLOW)
    print(f"  [S-census] hits {len(rows) + len(fails)} · real-side {sum(1 for r in rows if r[2] == 'real-side list')} · "
          f"allow-listed {sum(1 for r in rows if r[2] != 'real-side list')} · failing {len(fails)}")
    for p, h, why in rows:
        print(f"      {p}: {h} — {why}")
    for f in fails:
        print(f"  {f}")
    allow = load_allow(ALLOW)
    seen = {(p, h) for p, h in hits(ROOT)}
    stale = sorted(k for k in allow if k not in seen)
    for p, h in stale:
        print(f"  [FAIL] interface_side_labels — allow-list line {p}:{h} matches no hit (stale)")
    if bad or fails or stale:
        return 1
    print("  [PASS] interface_side_labels — every side-named temperature key and text has its rule")
    return 0


if __name__ == "__main__":
    sys.exit(main())
