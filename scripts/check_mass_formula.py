# 선언 질량 대 화학식 질량(M1, S3 D2 등록 §2.0) — 엔진이 만드는 BurnMan 광물의 끝성분마다 molar_mass 대 formula_mass 를 동결 허용 목록과 대조하고, 별칭·getattr 생성자까지 AST 묶음으로 훑음
"""python3 scripts/check_mass_formula.py [--root DIR] [--recorded GATE_MASS_LOG]      (the gate venv: BurnMan 2.1.0)

S3 D2 registration §2.0 (frozen d65eb6c8), M1 «declared mass vs formula», engine side (directing ruling 11-04 on r2
B4: wired in check.sh now, against the frozen allow-list; MARS-mass (b) empties the list in its own commit).

**The objects** (what the engine tree creates):
- `engine/mantle_composition.py`'s `SLB_NAMES`, each built through the engine's own `_phase(key)` (so a fix inside
  `_phase` is seen). The module must name exactly one `minerals.<dataset>` (else STOP, r2 n1).
- Every other BurnMan mineral constructor in the tracked .py of engine/, solver/ and scripts/, found by **binding**,
  not by text (r2 B2): names bound by `import burnman[.minerals[.<DS>]] [as X]`, `from burnman import minerals [as X]`,
  `from burnman.minerals import <DS> [as X]` and `from burnman.minerals.<DS> import <cls> [as X]`, then
  `<DS-binding>.<cls>(…)`, `getattr(<DS-binding>, "<cls>")(…)` and a bound class called.
  - Any other use of a dataset binding (a `getattr` with a non-constant name, `inspect.getmembers`, a bare
    reference) is a **dynamic** site. It STOPs unless its file's routes are enumerated here: only
    engine/mantle_composition.py, whose route is SLB_NAMES → `_phase`.
**The rule.** r = |params molar_mass − formula_mass(formula)| / formula_mass(formula) per end-member (BurnMan
atomic_masses). Every end-member with r > 1e-9 must be in `scripts/mass_allowlist.json` with the same r (to 1e-12
relative); one that is not STOPs, a listed one whose r changed STOPs, a listed one not found STOPs. If
mantle_composition sets `MASS_FROM_FORMULA = True`, the list must be empty.
**Runtime cross-check** (§2.0 «during the engine suite»; r2 B1 on b2a6d1c3, directing ruling (a)).
- In this check's own process, `Mineral.__init__` is wrapped while every key goes through `_phase`, every candidate
  through `_rock` and Mars's bulk through `select_all` at one node.
- Over the suite: in the full lane check.sh sets `GATE_MASS_LOG`, and `scripts/gate_reads/gate_mass_record.py` (loaded
  by the gate's sitecustomize) appends every (module, class) any step's Python process constructs after BurnMan's own
  import. `--recorded FILE` reads it after the pool barrier.
- Either way, a class that is neither a listed object nor one of its end-members is red: those under
  `burnman.minerals.*`, and any class outside `burnman.*` (a project subclass). BurnMan's machinery classes
  (`burnman.classes.*`) are not objects of the list.
**Stated limits** (r2 n1 on b2a6d1c3). The binding scan does not follow `from burnman.minerals import *`,
`importlib.import_module`, or `Mineral(params)` / `Solution(...)` built from a parameter dict. The runtime record sees
the first two (they construct dataset classes), and the third only if its class is outside `burnman.classes.*`. None
is in the tree at this commit. solver/ is parsed by the 3.9 gate python here, so a 3.10+-only file there makes this
step fail loudly (a SyntaxError), never silently (r2 n3).

scripts/mass_allowlist.json is a byte copy of artifacts ea-d2 a6fca1801 `rewrite/phase2-records/mass_allowlist.json`
(blob 29b0e33d), the frozen list. Last line «M1: PASS» (rc 0) or «M1: FAIL» (rc 1)."""
import ast
import json
import os
import subprocess
import sys
from pathlib import Path

TOL = 1e-9
R_MATCH = 1e-12
SCAN_DIRS = ("engine", "solver", "scripts")
ENUMERATED = {"engine/mantle_composition.py"}


# ── the scan by binding ───────────────────────────────────────────────────────────────────────────────────
def _bindings(tree):
    """name → ("root",) | ("minerals",) | ("ds", DS) | ("cls", DS, name)."""
    b = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                parts = a.name.split(".")
                if parts[0] != "burnman":
                    continue
                if a.asname is None:
                    b["burnman"] = ("root",)
                elif parts == ["burnman"]:
                    b[a.asname] = ("root",)
                elif parts[:2] == ["burnman", "minerals"]:
                    b[a.asname] = ("minerals",) if len(parts) == 2 else ("ds", parts[2])
        elif isinstance(n, ast.ImportFrom) and n.module:
            parts = n.module.split(".")
            for a in n.names:
                nm = a.asname or a.name
                if parts == ["burnman"] and a.name == "minerals":
                    b[nm] = ("minerals",)
                elif parts == ["burnman", "minerals"]:
                    b[nm] = ("ds", a.name)
                elif parts[:2] == ["burnman", "minerals"] and len(parts) == 3:
                    b[nm] = ("cls", parts[2], a.name)
    return b


def _kind(expr, b):
    if isinstance(expr, ast.Name):
        return b.get(expr.id)
    if isinstance(expr, ast.Attribute):
        k = _kind(expr.value, b)
        if k == ("root",) and expr.attr == "minerals":
            return ("minerals",)
        if k == ("minerals",):
            return ("ds", expr.attr)
        if k and k[0] == "ds":
            return ("cls", k[1], expr.attr)
    return None


def scan_source(src, name):
    """(static constructors [(DS, cls, line)], datasets named [DS], dynamic sites [(DS, line, text)])."""
    tree = ast.parse(src, filename=name)
    b = _bindings(tree)
    if not b:
        return [], [], []
    par = {c: p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}
    static, dyn, dss = [], [], []
    for n in ast.walk(tree):
        if not isinstance(n, (ast.Name, ast.Attribute)) or isinstance(par.get(n), ast.Attribute) and par[n].value is n:
            continue                                   # only the outermost expression of a chain
        k = _kind(n, b)
        if not k or k[0] not in ("ds", "cls"):
            continue
        p = par.get(n)
        if k[0] == "ds":
            dss.append(k[1])
            if (isinstance(p, ast.Call) and isinstance(p.func, ast.Name) and p.func.id == "getattr" and p.args
                    and p.args[0] is n and len(p.args) >= 2 and isinstance(p.args[1], ast.Constant)
                    and isinstance(par.get(p), ast.Call) and par[p].func is p):
                static.append((k[1], p.args[1].value, n.lineno))
            else:
                dyn.append((k[1], n.lineno, ast.unparse(p if p is not None else n)[:80]))
        elif k[0] == "cls":
            dss.append(k[1])
            if isinstance(p, ast.Call) and p.func is n:
                static.append((k[1], k[2], n.lineno))
            elif not (isinstance(n, ast.Name) and isinstance(p, (ast.alias,))):
                dyn.append((k[1], n.lineno, ast.unparse(p if p is not None else n)[:80]))
    # a name bound to a class by `from … import cls` and only ever called is static; any other use is dynamic
    return static, sorted(set(dss)), dyn


def files(root):
    root = Path(root)
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--", *[f"{d}/*.py" for d in SCAN_DIRS]],
                             capture_output=True, check=True).stdout.decode().split("\0")
        got = [f for f in out if f]
        if got:
            return got
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return sorted(str(p.relative_to(root)) for d in SCAN_DIRS for p in (root / d).rglob("*.py"))


# ── the objects ───────────────────────────────────────────────────────────────────────────────────────────
def r_of(m):
    from burnman.tools.chemistry import formula_mass
    fm = formula_mass(m.params["formula"])
    return abs(m.params["molar_mass"] - fm) / fm


def endmembers(o):
    from burnman import Solution
    return [m for m, _ in o.endmembers] if isinstance(o, Solution) else [o]


def check(root, recorded=None):
    root = Path(root).resolve()
    fails, objects = [], []
    sys.path.insert(0, str(root / "engine"))
    from burnman import minerals
    from burnman.classes.mineral import Mineral
    seen_classes = set()
    init = Mineral.__init__

    def wrapped(self, *a, **kw):
        init(self, *a, **kw)
        seen_classes.add((type(self).__module__, type(self).__name__))
    Mineral.__init__ = wrapped
    try:
        import mantle_composition as mc
        _static, dss, _dyn = scan_source((root / "engine" / "mantle_composition.py").read_text(encoding="utf-8"),
                                         "engine/mantle_composition.py")
        if len(dss) != 1:
            fails.append(f"engine/mantle_composition.py names {len(dss)} minerals datasets {dss}: exactly one expected")
        ds = dss[0] if dss else "?"
        for key, cls in sorted(mc.SLB_NAMES.items()):
            o = mc._phase(key)
            objects.append({"source": "engine", "dataset": ds, "class": cls, "obj": o})
        for cand in mc.CANDIDATES:
            mc._rock(cand, None)
        mc.select_all(mc.atomic_bulk(mc._body_wt("mars")), 1.0e9, 1500.0)
        marker = getattr(mc, "MASS_FROM_FORMULA", False) is True
    finally:
        Mineral.__init__ = init
    for f in files(root):
        if f in ENUMERATED:
            continue
        static, _dss, dyn = scan_source((root / f).read_text(encoding="utf-8", errors="replace"), f)
        for d, line, text in dyn:
            fails.append(f"dynamic BurnMan constructor site {f}:{line} ({d}: {text}) — not enumerable; list its route here")
        for d, cls, line in static:
            if not any(o["dataset"] == d and o["class"] == cls for o in objects):
                objects.append({"source": f"scan {f}:{line}", "dataset": d, "class": cls,
                                "obj": getattr(getattr(minerals, d), cls)()})
    al = json.loads((root / "scripts" / "mass_allowlist.json").read_text(encoding="utf-8"))
    listed = {(e["dataset"], e["class"], e["endmember"]): e["r"] for e in al["entries"]}
    found = set()
    for o in objects:
        for m in endmembers(o["obj"]):
            k = (o["dataset"], o["class"], type(m).__name__)
            r = r_of(m)
            if r <= TOL:
                if k in listed:
                    fails.append(f"listed {k} now has r = {r:.3e}: the allow-list must drop it")
                continue
            found.add(k)
            if k not in listed:
                fails.append(f"unlisted mismatch {k}: r = {r:.3e} ({o['source']})")
            elif abs(r - listed[k]) > R_MATCH * listed[k]:
                fails.append(f"listed {k}: r = {r:.6e}, list {listed[k]:.6e}")
    for k in sorted(set(listed) - found):
        if not any(str(k) in x for x in fails):
            fails.append(f"listed {k} not found among the objects the engine creates")
    if marker and listed:
        fails.append(f"MASS_FROM_FORMULA is True but the allow-list holds {len(listed)} entries (MARS-mass must empty it)")
    known = {o["class"] for o in objects} | {type(m).__name__ for o in objects for m in endmembers(o["obj"])}
    for mod, c in sorted(seen_classes):
        if c not in known and not mod.startswith("burnman.classes."):
            fails.append(f"runtime: class {mod}.{c} created on the engine's routes is not on the list")
    if recorded is not None:
        rows = [json.loads(ln) for ln in Path(recorded).read_text(encoding="utf-8").splitlines() if ln.strip()] \
            if Path(recorded).exists() else []
        for mod, c in sorted({(r["module"], r["class"]) for r in rows}):
            if c not in known and (mod.startswith("burnman.minerals.") or not mod.startswith("burnman.")):
                steps = sorted({r["step"] for r in rows if (r["module"], r["class"]) == (mod, c)})
                fails.append(f"runtime (suite record): class {mod}.{c} constructed by {steps} is not on the list")
        print(f"  [기록] M1 suite record: {len(rows)} lines, {len({(r['module'], r['class']) for r in rows})} classes")
    return fails, len(objects)


def main(argv):
    root = argv[argv.index("--root") + 1] if "--root" in argv else str(Path(__file__).resolve().parents[1])
    fails, n = check(root, argv[argv.index("--recorded") + 1] if "--recorded" in argv else None)
    for f in fails:
        print(f"  [FAIL] M1 {f}")
    print(f"M1: {'FAIL' if fails else 'PASS'} — {n} objects")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
