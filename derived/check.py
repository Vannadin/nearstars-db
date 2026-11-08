# 파생 파일 관문 도구 — derived/files.yaml 의 항목마다 입력 전부(코드 닫힘·데이터·파생 입력·저장소 밖 빌더·패키지·외부 데이터)의 스탬프를 짓고 대조하며, 움직였으면 그 항목의 값·재빌드 검사를 돌리고, 기본 거부 조사와 G6 재스탬프를 맡음
"""Derived-file gate, prereg pc/sg-gate/prereg-sg-gate.frozen.md (1765b55c), artifacts sg-gate-c8.

    python3 derived/check.py --entry NAME          one entry: stamp check, then its value/rebuild check if it moved (rc)
    python3 derived/check.py --all                 every entry, in DAG order (rc = number of red entries, capped at 1)
    python3 derived/check.py --census              the default-deny census (G1)
    python3 derived/check.py --steps               the landing steps generated from the list (one per entry + census)
    python3 derived/check.py --restamp NAME --why REASON   G6: rebuild:<blob> | check:<log blob> | ruling:<path>@<blob>
    python3 derived/check.py --show NAME           print the tip's stamp for NAME (no write)
    python3 derived/check.py --first-stamps        §3: every entry's first stamp from the tip (refused if any stamp exists)
    python3 derived/check.py --moved NAME          the stamp comparison alone, no check run (rc 1 when moved)

The stamp of an entry is everything its bytes depend on (G1): the §2 digest of every module in the static import closure
of its build entry points (computed here as solver/fall_sets.engine_static computes it), the git blob of every in-tree
data input and of every listed derived input, the out-of-tree builder blobs at artifacts origin/main (NEARSTARS_ARTIFACTS),
package versions, external data sha256s, the Python version and stamp_rule. Stamps live in derived/stamps/<entry>.json,
outside engine/ and solver/ (§1.1), and are rewritten only by --restamp (G6). An entry is green when its stamp is
unchanged; when it moved, an entry with a check runs it and takes its verdict, and an entry without one is red (G2)."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))
import digest as dg                                    # noqa: E402
from solver import fall_sets as fs                    # noqa: E402  (stdlib only; the closure is computed as it computes)

LIST = HERE / "files.yaml"
STAMPS = HERE / "stamps"
REASONS = ("rebuild", "check", "ruling")
ARTIFACTS_REFS = ("refs/remotes/origin-all/remotes/origin/main", "refs/remotes/origin/main")   # PC first (68 rev-4 n1)


class NotRun(LookupError):
    """An input's env var is unset and no checked default exists (directing B2 ruling on 68 HOLD 0415aff69): outside the
    gate lane the entry prints «NOT RUN <entry>: <VAR> unset», neither red nor green; inside it, it is red."""


def in_gate() -> bool:
    return os.environ.get("GATE_RUNNING") == "1"


def _default_dir(var: str):
    """A checked default beside the repo: NEARSTARS_ARTIFACTS must be the artifacts repo (tools/freeze.py and rewrite/),
    NEARSTARS_EXTERNAL the external-data dir (MANIFEST.md). Anything else is no default."""
    cand = {"NEARSTARS_ARTIFACTS": REPO.parent / "NearStars-artifacts",
            "NEARSTARS_EXTERNAL": REPO.parent / "NearStars-external"}.get(var)
    if cand is None:
        return None
    ok = ((cand / "tools" / "freeze.py").is_file() and (cand / "rewrite").is_dir() if var == "NEARSTARS_ARTIFACTS"
          else (cand / "MANIFEST.md").is_file())
    return str(cand) if ok else None


def env_dir(var: str, given=None) -> str:
    """The directory an env var names, else its checked default; NotRun when neither exists."""
    # literal reads, so the env census (solver/tests/test_env_tiers, which scans derived/) sees each name
    read = {"NEARSTARS_ARTIFACTS": os.environ.get("NEARSTARS_ARTIFACTS"),
            "NEARSTARS_EXTERNAL": os.environ.get("NEARSTARS_EXTERNAL"),
            "NEARSTARS_PAPERS": os.environ.get("NEARSTARS_PAPERS")}
    v = read[var] if given is None else given
    if v:
        return v
    d = _default_dir(var)
    if d:
        return d
    raise NotRun(f"{var} unset")


# ── the list ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def load_list(path=LIST) -> dict:
    import yaml
    doc = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return doc


def entries(doc) -> dict:
    return doc["entries"]


def file_owner(doc) -> dict:
    """derived file path → entry name."""
    own = {}
    for name, e in entries(doc).items():
        for f in e["files"]:
            if f in own:
                raise SystemExit(f"STOP: {f} is listed in both {own[f]} and {name}")
            own[f] = name
    return own


def dag_order(doc) -> list:
    """Entries ordered by their derived inputs; a cycle, an unknown derived input or derived/ as an input is refused."""
    own = file_owner(doc)
    es = entries(doc)
    deps = {}
    for name, e in es.items():
        for p in list(e.get("data", [])) + list(e.get("derived", [])):
            if p.startswith("derived/"):
                raise SystemExit(f"STOP: {name} names {p} as an input; derived/ is no entry's input (G6)")
        ups = set()
        for p in e.get("derived", []):
            if p not in own:
                raise SystemExit(f"STOP: {name}'s derived input {p} is not a listed derived file")
            ups.add(own[p])
        files = tracked_all() if any("*" in p or "?" in p for p in e.get("data", [])) else None
        for p in expand(e.get("data", []), files):        # after expansion (68 n2): a glob match counts too
            if p in own and p not in e.get("derived", []):
                raise SystemExit(f"STOP: {name}'s data {'glob matches' if p not in e.get('data', []) else 'lists'} the "
                                 f"derived file {p}; name it under derived")
        if e.get("code"):                              # a listed derived .py in the code closure is an upstream too
            ups |= {own[m] for m in closure(e["code"]) if m in own}
        ups.discard(name)
        deps[name] = ups
    order, state = [], {}

    def visit(n, path):
        if state.get(n) == 2:
            return
        if state.get(n) == 1:
            raise SystemExit(f"STOP: cycle in derived inputs: {' → '.join(path + [n])}")
        state[n] = 1
        for u in sorted(deps[n]):
            visit(u, path + [n])
        state[n] = 2
        order.append(n)

    for n in sorted(es):
        visit(n, [])
    return order


# ── the closure (G1, M5) ─────────────────────────────────────────────────────────────────────────────────────────────
def _module_file(spec: str) -> Path:
    """«engine/tools/reference_adiabats.py:main» → the file."""
    return REPO / spec.split(":", 1)[0]


def closure(code_specs, root=REPO) -> list:
    """The static import closure of the entry points, as fall_sets.engine_static follows imports: bare imports resolved in
    engine/ (and in the entry file's own directory), `from solver …` / `import solver.…` resolved in solver/, followed
    transitively within engine/ and solver/. Returns repo-relative paths, sorted."""
    root = Path(root)
    eng, sol = root / "engine", root / "solver"
    seen, todo = set(), []
    for spec in code_specs:
        f = root / spec.split(":", 1)[0]
        if not f.is_file():
            raise SystemExit(f"STOP: code entry point {spec} does not exist")
        todo.append(f)
    while todo:
        f = todo.pop()
        rel = f.relative_to(root).as_posix()
        if rel in seen:
            continue
        seen.add(rel)
        text = f.read_text(encoding="utf-8")
        for m in sorted(fs._names(text, fs._BARE_IMPORT)):
            for cand in (eng / f"{m}.py", f.parent / f"{m}.py"):
                if cand.is_file() and (eng in cand.parents or sol in cand.parents):
                    todo.append(cand)
                    break
        for m in sorted(fs._names(text, fs._SOLVER_IMPORT)):
            cand = sol / f"{m}.py"
            if cand.is_file() and m not in fs.EXCLUDED:
                todo.append(cand)
        for m in sorted(_dynamic_names(rel, text, root)):  # 68 B1 class: imports by name at run time (measured, rows 4, 7)
            top, _, sub = m.partition(".")
            cands = ([sol / f"{sub}.py"] if top == "solver" and sub else []) + [eng / f"{m}.py", f.parent / f"{m}.py"]
            for cand in cands:
                if cand.is_file() and (eng in cand.parents or sol in cand.parents):
                    todo.append(cand)
                    break
        if rel.startswith("solver/") and (sol / "__init__.py").is_file():
            todo.append(sol / "__init__.py")             # the package init runs on every solver import (measured, row 7)
    return sorted(seen)


#: a literal module name passed to the import machinery: import_module("x"), __import__("x")
_LITERAL_IMPORT = re.compile(r"""(?:import_module|__import__)\(\s*["']([\w.]+)["']""")
#: modules that import every process_state.REGISTRY module by name (process_state.reset, legacy_materials'
#: _registry_entries); transfers.check_code_defaults imports each CODE_DEFAULTS record's module="x"
_REGISTRY_WALKERS = ("engine/process_state.py", "solver/legacy_materials.py")
_REGISTRY_KEY = re.compile(r"""^\s*\(\s*["'](\w+)["']\s*,\s*["']\w+["']\s*\)\s*:""", re.M)
_TRANSFER_MODULE = re.compile(r"""\bmodule\s*=\s*["'](\w+)["']""")


def _dynamic_names(rel: str, text: str, root: Path) -> set:
    names = set(_LITERAL_IMPORT.findall(text))
    if rel in _REGISTRY_WALKERS:
        names |= set(_REGISTRY_KEY.findall((Path(root) / "engine" / "process_state.py").read_text(encoding="utf-8")))
    if rel == "engine/transfers.py":
        names |= set(_TRANSFER_MODULE.findall(text))
    return names


# ── the stamp (G1) ───────────────────────────────────────────────────────────────────────────────────────────────────
def git_blob(path: Path) -> str:
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def artifacts_ref(art: Path) -> tuple[str, str]:
    """(ref, sha) of artifacts origin/main as fetched now; the suite run fetches it itself (68 n2, rev-4 n1)."""
    f = subprocess.run(["git", "-C", str(art), "fetch", "-q", "origin", "+refs/*:refs/remotes/origin-all/*"],
                       capture_output=True, text=True)
    if f.returncode != 0:                                   # frozen §1: a failed fetch is red, never a stale main (68 B1)
        raise LookupError(f"the artifacts fetch failed (rc {f.returncode}: {(f.stderr or '').strip()[-160:]}); "
                          "main is not compared stale")
    for ref in ARTIFACTS_REFS:
        r = subprocess.run(["git", "-C", str(art), "rev-parse", "--verify", "-q", ref], capture_output=True, text=True)
        if r.returncode == 0:
            return ref, r.stdout.strip()
    raise LookupError(f"no artifacts main ref in {art} ({', '.join(ARTIFACTS_REFS)})")


def out_of_tree_blobs(specs, art_env=None) -> dict:
    """{path: blob} of artifacts builder files at artifacts origin/main; a missing checkout or file raises LookupError."""
    if not specs:
        return {}
    art = env_dir("NEARSTARS_ARTIFACTS", art_env)
    if not Path(art).is_dir():
        raise LookupError(f"NEARSTARS_ARTIFACTS={art!r} is not a checkout (out-of-tree builders are red, not skipped)")
    ref, sha = artifacts_ref(Path(art))
    out = {"_ref": f"{ref} {sha}"}
    for p in specs:
        r = subprocess.run(["git", "-C", str(art), "rev-parse", "--verify", "-q", f"{sha}:{p}"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise LookupError(f"builder {p} is not in artifacts {sha[:12]} ({ref})")
        out[p] = r.stdout.strip()
    return out


def external_sha(specs) -> dict:
    """{name: sha256} of external data; a path is absolute, or relative to the directory its env var names."""
    out = {}
    for name, s in (specs or {}).items():
        base = env_dir(s["env"]) if s.get("env") else None
        p = Path(base) / s["path"] if base else Path(s["path"])
        if not p.is_file():
            raise LookupError(f"external {name}: {p} is not a file")
        out[name] = sha256(p)
    return out


def glob_re(pat: str):
    """A data glob as a regex over repo-relative paths: `**/` is zero or more directories, `*` and `?` stay in one."""
    out, i = "", 0
    while i < len(pat):
        if pat.startswith("**/", i):
            out, i = out + "(?:[^/]+/)*", i + 3
        elif pat.startswith("**", i):
            out, i = out + ".*", i + 2
        elif pat[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif pat[i] == "?":
            out, i = out + "[^/]", i + 1
        else:
            out, i = out + re.escape(pat[i]), i + 1
    return re.compile(out + r"\Z")


def expand(paths, files=None) -> list:
    """Data paths with a glob expanded at check time over TRACKED files only (68 n1 on 2be90e97: an untracked stray on
    one machine is no input, and engine/.venv* is never swept); sorted, repo-relative. A new tracked match is a new input."""
    out = []
    for p in paths:
        if "*" not in p and "?" not in p:
            out.append(p)
            continue
        if files is None:
            files = tracked_all()
        rx = glob_re(p)
        out += sorted(f for f in files if rx.match(f) and not any(s.startswith(".venv") for s in f.split("/")))
    return out


def tracked_all(root=REPO) -> list:
    r = subprocess.run(["git", "-C", str(root), "ls-files"], capture_output=True, text=True, check=True)
    return [ln for ln in r.stdout.splitlines() if ln]


def data_inputs(e: dict, files=None) -> list:
    """The entry's data after expansion, without the listed derived files a glob also matches (they are stamped, and
    ordered in the DAG, as `derived`; dag_order refuses a glob match that is a derived file not listed there)."""
    der = set(e.get("derived", []))
    return [p for p in expand(e.get("data", []), files) if p not in der]


def stamp(name: str, e: dict, art_env=None) -> dict:
    """The stamp of one entry at this tree. Raises LookupError for an input it cannot read (the entry is then red)."""
    mods = closure(e["code"]) if e.get("code") else []
    st = {
        "entry": name,
        "stamp_rule": dg.STAMP_RULE,
        "python": platform.python_version(),
        "files": {f: git_blob(REPO / f) for f in e["files"]},
        "code": {m: dg.digest(REPO / m) for m in mods},
        "data": {p: git_blob(REPO / p) for p in data_inputs(e)},
        "derived": {p: git_blob(REPO / p) for p in e.get("derived", [])},
        "out_of_tree": out_of_tree_blobs(e.get("out_of_tree", []), art_env),
        "packages": {p: importlib.metadata.version(p) for p in e.get("packages", [])},
        "external": external_sha(e.get("external")),
    }
    return st


def moved(then: dict | None, now: dict) -> list[str]:
    """The moved parts, named. A stamp with no stamp_rule, or another rule, reads as moved (N5), never matched.
    `files` (the entry's own bytes) and `python` are not inputs: a file rebuilt in this landing is restamped (G6)."""
    if not then:
        return ["no stamp"]
    if then.get("stamp_rule") != dg.STAMP_RULE:
        return [f"stamp_rule {then.get('stamp_rule')!r} is not {dg.STAMP_RULE!r}"]
    out = []
    for part in ("code", "data", "derived", "out_of_tree", "packages", "external"):
        a, b = then.get(part, {}), now.get(part, {})
        for k in sorted(set(a) | set(b)):
            if k == "_ref":
                continue
            if a.get(k) != b.get(k):
                tag = {"derived": "input"}.get(part, part)
                out.append(f"{tag} {k} " + ("added" if k not in a else "dropped" if k not in b else "moved"))
    return out


def own_bytes_moved(then: dict | None, now: dict) -> list[str]:
    """The entry's own files whose bytes differ from the stamp's: a rebuild not restamped, or a hand edit."""
    if not then:
        return []
    return [f for f in now["files"] if then.get("files", {}).get(f) != now["files"][f]]


def read_stamp(name: str) -> dict | None:
    p = STAMPS / f"{name}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


# ── value / rebuild checks (G2) ──────────────────────────────────────────────────────────────────────────────────────
def check_structure_table(table: str, recheck: bool = True) -> tuple[bool, str, list | None]:
    """Row 1: structure_grid's own read rules for one table (quick mode, refusal cap, data triggers by _moved), and, when
    `recheck`, its `_recheck` within ε — run because the sidecar's closure moved (the in-file code digest is not read,
    §1.1). The read rules run on every call, stamp moved or not: a first stamp asserts nothing about values (§3), so a
    table already stale on its data (mars under the E18 hold) is red at once, never green by its first stamp."""
    sys.path.insert(0, str(REPO / "engine"))
    import run
    import structure_grid as sg
    path = REPO / table
    doc = json.loads(path.read_text(encoding="utf-8"))
    if doc.get("mode") == "quick":
        return False, "a quick table (mode quick) sits in the reference place (C161)", None
    over = sg.refusal_over_cap(doc.get("no_answer", []))
    if over:
        return False, f"refusal span over the cap ({over}, C162)", None
    body, _ = run.load_body(sg.BODIES_DIR / f"{doc['body'].lower()}.yaml")
    data, _code_in_file = sg._moved(doc["triggers"], sg.triggers(body.inputs))
    if data:
        return False, f"data triggers moved {data}", sorted(data)
    if not recheck:
        return True, "read rules hold (quick mode, refusal cap, data triggers)", None
    before = sg.GUARD_RUNS[0]
    worst, where = sg._recheck(doc, body)
    sg.GUARD_RUNS[0] += 1
    ok = worst <= sg.EPS
    return ok, (f"_recheck {'within' if ok else 'beyond'} ε: largest relative difference {worst:.3e} at {where} "
                f"(ε {sg.EPS:.4e}, {len(doc['t_pot'])} points; GUARD_RUNS {before} → {sg.GUARD_RUNS[0]})"), None


def check_command(argv: list, env_extra=None) -> tuple[bool, str]:
    env = dict(os.environ, **(env_extra or {}))
    env.setdefault("PYTHONPATH", str(REPO))
    r = subprocess.run([sys.executable if a == "{python}" else a for a in argv], cwd=REPO, env=env,
                       capture_output=True, text=True)
    tail = (r.stdout + r.stderr).strip().splitlines()[-3:]
    return r.returncode == 0, f"rc {r.returncode} · " + " | ".join(t[:160] for t in tail)


def run_check(e: dict, name: str | None = None) -> tuple[bool, str, list | None] | None:
    """The entry's check. With `name`, the G1 load census rides on it (68 HOLD on 4e58f8a6, directing): a command check
    runs inside derived/load_census.py, so the modules it loads are judged against the closure; row 1's in-process
    check adds the one-point census build. A census red fails the check, named."""
    c = e.get("check")
    if not c:
        return None
    if c["kind"] == "structure_table":
        ok, why, data = check_structure_table(c["table"])
        if name is not None:
            cok, cline = run_census(name, e)
            ok, why = ok and cok, f"{why}; {cline}"
        return ok, why, data
    if c["kind"] == "command":
        if name is not None and not e.get("census"):
            return census_command(name, c["argv"][1:], c.get("env")) + (None,)
        if name is not None:                         # the check's own loads (and its children's) are judged too
            ok, why = census_command(name, c["argv"][1:], c.get("env"))
            cok, cline = run_census(name, e)
            ok, why = ok and cok, f"{why}; {cline}"
        else:
            ok, why = check_command(c["argv"], c.get("env"))
        return ok, why, None
    raise SystemExit(f"STOP: unknown check kind {c['kind']!r}")


# ── the load census (G1, N18) ────────────────────────────────────────────────────────────────────────────────────────
def census_target(e: dict):
    """(target argv for derived/load_census.py, its flags, the env its declared externals name), or None when this
    entry's census runs in the PC block."""
    c = e.get("census")
    if c is None:
        chk = e.get("check") or {}
        return (list(chk["argv"][1:]), [], {}) if chk.get("kind") == "command" else None
    if c.get("where") == "pc":
        return None
    dirs = {}
    for var, key in (("NEARSTARS_EXTERNAL", "{external}"), ("NEARSTARS_PAPERS", "{papers}"),
                     ("NEARSTARS_ARTIFACTS", "{artifacts}")):
        if any(key in str(a) for a in c.get("argv", []) + c.get("args", [])):
            dirs[key] = env_dir(var)                     # NotRun when unset (B2), as for the stamp
    sub = [str(a) for a in c.get("argv", [])]
    for k, v in dirs.items():
        sub = [a.replace(k, v) for a in sub]
    args = [a for a in c.get("args", [])]
    for k, v in dirs.items():
        args = [a.replace(k, v) if isinstance(a, str) else a for a in args]
    target = ["--call", c["call"], json.dumps(args)] if "call" in c else sub
    env = {x["env"]: env_dir(x["env"]) for x in (e.get("external") or {}).values() if x.get("env")}   # the build's inputs
    return target, (["--restore"] if c.get("restore") else []), env


def census_command(name: str, target: list, env_extra=None, flags=(), report=None) -> tuple[bool, str]:
    """Run TARGET under derived/load_census.py for entry NAME. ok only when the census holds AND the target exit is 0
    (a build that failed is no census). The line names the [LOAD]/[LOAD-RED] verdict. REPORT, a list, gets every line
    the census itself printed (restore, externals, outside-tree reads, children, unjudged files, mirrors, verdict),
    not only the tail: `--load-census` prints them whole, the A-time evidence.
    LOAD-CENSUS-TIME (1) (go-live s4r, 11-08): a flushed `[CENSUS-START]` line before the run — not `[LOAD…`, which the
    verdict finder and the taggers match — and `· start HH:MM:SS · wall N s` at the END of the line (census_tag reads
    the verdict as field 1), so a slow entry can be told from a hung one. No budget yet: that is (2)–(3)."""
    env = dict(os.environ, **(env_extra or {}))
    env.setdefault("PYTHONPATH", str(REPO))
    start, t0 = time.strftime("%H:%M:%S"), time.monotonic()
    print(f"[CENSUS-START] {name} — {start} · {' '.join(str(x) for x in target[:2])[:160]}", flush=True)
    r = subprocess.run([sys.executable, "-B", str(HERE / "load_census.py"), "--entry", name, *flags, "--", *target],
                       cwd=REPO, env=env, capture_output=True, text=True)
    lines = (r.stdout + r.stderr).strip().splitlines()
    verdict = next((ln for ln in lines if ln.startswith("[LOAD")), f"[LOAD-RED] {name} — no census line (rc {r.returncode})")
    tail = " | ".join(t[:160] for t in lines[-3:])
    said = target_said(name, lines) if r.returncode != 0 else []
    if said:       # 68 n3 on ba56bcf0d: a non-zero target names its own failure in the line, not only the census's
        tail += " · target said: " + " | ".join(t[:200] for t in said)
    if report is not None:
        report += [ln for ln in lines if ln.startswith((f"  {name}: ", "[LOAD"))] or lines[-3:]
        report += [f"  {name}: target said: {t}" for t in said]
    clock = f" · start {start} · wall {time.monotonic() - t0:.0f} s"
    return r.returncode == 0 and verdict.startswith("[LOAD]"), f"rc {r.returncode} · {verdict[:400]} · {tail}{clock}"


SAID = re.compile(r"^\s*\[?(FAIL|STOP|NOT OK)\b|^Traceback|^\s*\w*(Error|Exception)\b|:\s*(FAIL|RED)\s*$")


def target_said(name: str, lines: list) -> list:
    """The target's own lines from a census run (the census's lines removed): those that open with a failure (FAIL,
    [FAIL], STOP, NOT OK, Traceback, …Error) or end in «: FAIL»/«: RED», else its last three; at most six either way.
    A line that only mentions FAIL mid-text (a [PASS] control quoting «판정 FAIL») is not one."""
    own = [ln for ln in lines if not ln.startswith((f"  {name}: ", "[LOAD")) and ln.strip()]
    hit = [ln for ln in own if SAID.search(ln)]
    return (hit or own[-3:])[-6:]


def census_tag(ok: bool, line: str) -> str:
    """One census's tag from its own verdict (68 HOLD B2 on 5db3db7f): [LOAD-RED] when its loads are red;
    [LOAD-INCOMPLETE] only when its loads are inside but its target exited non-zero (row 3's Mac drift); else [LOAD]."""
    verdict = line.split(" · ", 2)[1] if line.count(" · ") >= 1 else line
    if not verdict.startswith("[LOAD] "):
        return "[LOAD-RED]"
    return "[LOAD]" if ok else "[LOAD-INCOMPLETE]"


def row_tag(tags: list) -> str:
    """A row is red when any of its censuses is red, whatever the others say; INCOMPLETE only when none is red."""
    return "[LOAD-RED]" if "[LOAD-RED]" in tags else "[LOAD-INCOMPLETE]" if "[LOAD-INCOMPLETE]" in tags else "[LOAD]"


def run_census(name: str, e: dict) -> tuple[bool, str]:
    t = census_target(e)
    if t is None:
        return True, f"load census of {name} runs in the PC block ({(e.get('census') or {}).get('how', 'where: pc')})"
    return census_command(name, t[0], {**((e.get("check") or {}).get("env") or {}), **t[2]}, t[1])


def expected_red(name: str) -> dict | None:
    """A gate_expected_red.yaml item naming this entry (`derived_entry: <name>`), with its ruling: named, never silent."""
    import yaml
    p = REPO / "scripts" / "gate_expected_red.yaml"
    for item in yaml.safe_load(p.read_text(encoding="utf-8")) or []:
        if item.get("derived_entry") == name:
            return item
    return None


def judge_entry(name: str, e: dict, art_env=None, out=print) -> int:
    """One entry, G2/G3: 0 green, 1 red. Every line names the entry; a red names its expected-red item if one exists."""
    then = read_stamp(name)
    try:
        now = stamp(name, e, art_env)
    except NotRun as err:                                  # directing B2: named, not red, outside the gate lane
        if not in_gate():
            out(f"NOT RUN {name}: {err}")
            return 0
        out(f"[RED] {name} — an input cannot be read in the gate lane: {err}")
        return 1
    except LookupError as err:
        out(f"[RED] {name} — an input cannot be read: {err}")
        return _named(name, out)
    if "_ref" in now["out_of_tree"]:
        out(f"  {name}: artifacts main read at {now['out_of_tree']['_ref']}")
    mv = moved(then, now)
    own = own_bytes_moved(then, now)
    if own:
        out(f"[RED] {name} — its own bytes differ from the stamp's ({own}): rebuilt without --restamp, or edited")
        return _named(name, out)
    if not mv and (e.get("check") or {}).get("kind") == "structure_table":
        ok, why, data = check_structure_table(e["check"]["table"], recheck=False)
        if not ok:
            out(f"[RED] {name} — stamp unchanged, but the table's own read rules fail: {why}")
            return _named(name, out, data)
    if not mv:
        out(f"[GREEN] {name} — stamp unchanged ({len(now['code'])} closure modules, {len(now['data'])} data, "
            f"{len(now['derived'])} derived, {len(now['out_of_tree']) - ('_ref' in now['out_of_tree'])} out-of-tree)")
        return 0
    res = run_check(e, name)
    if res is None:
        out(f"[RED] {name} — stamp moved ({'; '.join(mv[:8])}{' …' if len(mv) > 8 else ''}); no value check: rebuild "
            f"in this landing, or a ruling (G2, G6)")
        return _named(name, out)
    ok, why, data = res
    out(f"[{'GREEN' if ok else 'RED'}] {name} — stamp moved ({'; '.join(mv[:8])}{' …' if len(mv) > 8 else ''}); "
        f"check: {why}")
    return 0 if ok else _named(name, out, data)


def _named(name, out, data=None) -> int:
    """68 B4: an item names the exact read-rule failure it expects (`triggers`, the moved data triggers); only a red that
    is that failure, and nothing else, prints EXPECTED. Any other red on the entry stays a plain red."""
    item = expected_red(name)
    if item and data is not None and sorted(item.get("triggers") or []) == sorted(data):
        out(f"  {name}: EXPECTED RED, gate_expected_red.yaml id {item.get('id')} — {item.get('registered', '')}")
    elif item:
        out(f"  {name}: not the red gate_expected_red.yaml id {item.get('id')} expects (its triggers "
            f"{sorted(item.get('triggers') or [])}; this red {data if data is not None else 'is no data-trigger failure'})")
    return 1


# ── G6: restamp ──────────────────────────────────────────────────────────────────────────────────────────────────────
def restamp(name: str, why: str, art_env=None) -> Path:
    kind, _, ev = why.partition(":")
    if kind not in REASONS or not ev:
        raise SystemExit(f"STOP: --why must be one of {', '.join(r + ':<evidence>' for r in REASONS)} (G6); got {why!r}")
    e = entries(load_list())[name]
    if kind == "ruling" and e.get("check"):
        raise SystemExit(f"STOP: {name} has a value check; a ruling restamps only stamp-only entries (G6)")
    if kind == "rebuild" and not e.get("check"):     # G1: a stamp-only entry's load census runs at each rebuild
        ok, line = run_census(name, e)
        print(f"{'[LOAD]' if ok else '[LOAD-RED]'} {name} — {line}", flush=True)
        if not ok:
            raise SystemExit(f"STOP: {name}'s load census at this rebuild is not clean; no restamp (G1)")
    now = stamp(name, e, art_env)
    now["why"] = why
    STAMPS.mkdir(exist_ok=True)
    p = STAMPS / f"{name}.json"
    p.write_text(json.dumps(now, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return p


# ── the census (G1, default deny) ────────────────────────────────────────────────────────────────────────────────────
GENERATED_MARK = "생성된 파일이다. 손으로 고치지 말 것"


def tracked(root=REPO) -> list:
    r = subprocess.run(["git", "-C", str(root), "ls-files", "engine", "solver"], capture_output=True, text=True, check=True)
    return [ln for ln in r.stdout.splitlines() if ln]


def census(doc, files=None, root=REPO) -> list[str]:
    """Reds: a tracked file under engine/ or solver/ in no class; a .py with the generated header not listed; a make_*.py
    output neither listed nor named not-tracked; a listed or exempt path that is not tracked; a check without its
    tolerance or reference machine; an entry with no load census (G1)."""
    files = tracked(root) if files is None else files
    listed = set(file_owner(doc))
    ex = doc.get("exempt", {})
    exempt_pats = [(re.compile(p), why) for p, why in ex.items()]
    reds = []
    for f in files:
        p = Path(root) / f
        if f in listed:
            continue
        if f.endswith(".py") or f.endswith(".sh"):
            if f.endswith(".py") and p.is_file() and GENERATED_MARK in p.read_text(encoding="utf-8", errors="replace")[:400]:
                reds.append(f"{f}: carries the generated header and is not listed")
            continue
        if f.endswith(".md"):
            continue
        if any(rx.fullmatch(f) for rx, _ in exempt_pats):
            continue
        reds.append(f"{f}: in no class (hand-written source, document, listed derived file, or exempt with a reason)")
    tset = set(files)
    for f in sorted(listed):
        if f not in tset:
            reds.append(f"{f}: listed but not tracked")
    for name, e in entries(doc).items():             # G1: a check names its tolerance and reference machine
        c = e.get("check")
        for k in ("tolerance", "reference_machine"):
            if c and not str(c.get(k) or "").strip():
                reds.append(f"{name}: its check names no {k} (G1)")
        if not e.get("census") and (c or {}).get("kind") != "command":
            reds.append(f"{name}: no load census (G1): neither a census field nor a command check it rides on")
    not_tracked = set(doc.get("not_tracked", {}))
    for mk in sorted(Path(root, "engine", "tools").glob("make_*.py")):
        target = f"engine/{mk.stem.removeprefix('make_')}.py"
        if target not in listed and target not in not_tracked:
            reds.append(f"{mk.relative_to(root).as_posix()}: its output {target} is neither listed nor named not tracked")
    return reds


# ── CLI ──────────────────────────────────────────────────────────────────────────────────────────────────────────────
def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--entry")
    g.add_argument("--all", action="store_true")
    g.add_argument("--census", action="store_true")
    g.add_argument("--steps", action="store_true")
    g.add_argument("--restamp")
    g.add_argument("--show")
    g.add_argument("--first-stamps", action="store_true")
    g.add_argument("--moved")
    g.add_argument("--load-census", metavar="NAME|all")
    ap.add_argument("--why")
    a = ap.parse_args(argv)
    doc = load_list()
    order = dag_order(doc)
    print(f"# derived · list {git_blob(LIST)[:12]} · this {git_blob(Path(__file__))[:12]} · python "
          f"{platform.python_version()} · {platform.system()}-{platform.machine()}")
    if a.census:
        reds = census(doc)
        for r in reds:
            print(f"[RED] census — {r}")
        print(f"census: {'PASS' if not reds else f'RED ({len(reds)})'} · {len(file_owner(doc))} listed files")
        return 1 if reds else 0
    if a.steps:
        for n in order:
            print(f"{n}\t{{python}} derived/check.py --entry {n}")
        print("census\t{python} derived/check.py --census")
        return 0
    if a.restamp:
        if not a.why:
            raise SystemExit("STOP: --restamp needs --why (G6)")
        print(f"restamped {restamp(a.restamp, a.why).relative_to(REPO)} ({a.why})")
        return 0
    if a.first_stamps:
        # §3 «the first stamps»: written once from the tip's code and inputs at this prereg's landing; not a G6 rewrite,
        #   so it is refused when any stamp exists (a later write is --restamp with a reason)
        if any(STAMPS.glob("*.json")):
            raise SystemExit("STOP: stamps exist; a stamp is rewritten only by --restamp with a reason (G6)")
        STAMPS.mkdir(exist_ok=True)
        bad = 0
        for n in order:
            try:
                st = stamp(n, entries(doc)[n])
            except LookupError as err:
                print(f"[RED] {n} — no first stamp: an input cannot be read: {err}")
                bad += 1
                continue
            st["why"] = "first stamp (§3)"
            (STAMPS / f"{n}.json").write_text(json.dumps(st, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
                                              encoding="utf-8")
            print(f"first stamp {n}")
        return 1 if bad else 0
    if a.moved:                                    # the stamp comparison alone, no check run (the plant controls)
        mv = moved(read_stamp(a.moved), stamp(a.moved, entries(doc)[a.moved]))
        print(f"{'[MOVED]' if mv else '[UNMOVED]'} {a.moved} — {'; '.join(mv) if mv else 'stamp unchanged'}")
        return 1 if mv else 0
    if a.load_census:                              # G1 load census now: every Mac-runnable entry, or one (A-time)
        names = order if a.load_census == "all" else [a.load_census]
        bad = 0
        for n in names:
            e = entries(doc)[n]
            try:
                t = census_target(e)
            except NotRun as err:
                print(f"NOT RUN {n}: {err}" if not in_gate() else f"[LOAD-RED] {n} — census input unset: {err}")
                bad += in_gate()
                continue
            if t is None:
                print(f"PC {n} — {(e.get('census') or {}).get('how', 'where: pc')}")
                continue
            rep, crep = [], []
            ok, line = census_command(n, t[0], {**((e.get("check") or {}).get("env") or {}), **t[2]}, t[1], rep)
            tags = [census_tag(ok, line)]
            chk = e.get("check") or {}
            if e.get("census") and chk.get("kind") == "command":   # the check's own loads too, as at the landing
                cok, cline = census_command(n, chk["argv"][1:], chk.get("env"), report=crep)
                tags.append(census_tag(cok, cline))
                ok, line = ok and cok, f"{line}; check: {cline}"
            tag = row_tag(tags)
            print(f"{tag} {n} — {line}", flush=True)     # INCOMPLETE: loads inside, but the target exited non-zero
            for label, r_ in (("build", rep), ("check", crep)):
                for ln in r_:
                    print(f"    {label}| {ln.strip()}", flush=True)
            bad += not ok
        return 1 if bad else 0
    if a.show:
        print(json.dumps(stamp(a.show, entries(doc)[a.show]), indent=1, sort_keys=True))
        return 0
    names = order if a.all else [a.entry]
    bad = sum(judge_entry(n, entries(doc)[n]) for n in names)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
