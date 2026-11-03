# 파생 파일 관문 도구 — derived/files.yaml 의 항목마다 입력 전부(코드 닫힘·데이터·파생 입력·저장소 밖 빌더·패키지·외부 데이터)의 스탬프를 짓고 대조하며, 움직였으면 그 항목의 값·재빌드 검사를 돌리고, 기본 거부 조사와 G6 재스탬프를 맡음
"""Derived-file gate, prereg pc/sg-gate/prereg-sg-gate.frozen.md (1765b55c), artifacts sg-gate-c8.

    python3 derived/check.py --entry NAME          one entry: stamp check, then its value/rebuild check if it moved (rc)
    python3 derived/check.py --all                 every entry, in DAG order (rc = number of red entries, capped at 1)
    python3 derived/check.py --census              the default-deny census (G1)
    python3 derived/check.py --steps               the landing steps generated from the list (one per entry + census)
    python3 derived/check.py --restamp NAME --why REASON   G6: rebuild:<blob> | check:<log blob> | ruling:<path>@<blob>
    python3 derived/check.py --show NAME           print the tip's stamp for NAME (no write)
    python3 derived/check.py --first-stamps        §3: every entry's first stamp from the tip (refused if any stamp exists)

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
        for p in e.get("data", []):
            if p in own:
                raise SystemExit(f"STOP: {name} lists the derived file {p} under data; name it under derived")
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
    return sorted(seen)


# ── the stamp (G1) ───────────────────────────────────────────────────────────────────────────────────────────────────
def git_blob(path: Path) -> str:
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def artifacts_ref(art: Path) -> tuple[str, str]:
    """(ref, sha) of artifacts origin/main as fetched now; the suite run fetches it itself (68 n2, rev-4 n1)."""
    subprocess.run(["git", "-C", str(art), "fetch", "-q", "origin", "+refs/*:refs/remotes/origin-all/*"],
                   capture_output=True, text=True)
    for ref in ARTIFACTS_REFS:
        r = subprocess.run(["git", "-C", str(art), "rev-parse", "--verify", "-q", ref], capture_output=True, text=True)
        if r.returncode == 0:
            return ref, r.stdout.strip()
    raise LookupError(f"no artifacts main ref in {art} ({', '.join(ARTIFACTS_REFS)})")


def out_of_tree_blobs(specs, art_env=None) -> dict:
    """{path: blob} of artifacts builder files at artifacts origin/main; a missing checkout or file raises LookupError."""
    if not specs:
        return {}
    art = art_env if art_env is not None else os.environ.get("NEARSTARS_ARTIFACTS")
    if not art or not Path(art).is_dir():
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
        base = os.environ.get(s["env"]) if s.get("env") else None
        if s.get("env") and not base:
            raise LookupError(f"external {name}: {s['env']} is unset")
        p = Path(base) / s["path"] if base else Path(s["path"])
        if not p.is_file():
            raise LookupError(f"external {name}: {p} is not a file")
        out[name] = sha256(p)
    return out


def stamp(name: str, e: dict, art_env=None) -> dict:
    """The stamp of one entry at this tree. Raises LookupError for an input it cannot read (the entry is then red)."""
    mods = closure(e["code"]) if e.get("code") else []
    st = {
        "entry": name,
        "stamp_rule": dg.STAMP_RULE,
        "python": platform.python_version(),
        "files": {f: git_blob(REPO / f) for f in e["files"]},
        "code": {m: dg.digest(REPO / m) for m in mods},
        "data": {p: git_blob(REPO / p) for p in e.get("data", [])},
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
def check_structure_table(table: str) -> tuple[bool, str]:
    """Row 1: structure_grid's own read rules for one table (quick mode, refusal cap, data triggers by _moved), and its
    `_recheck` within ε — called because the sidecar's closure moved (the in-file code digest is not read, §1.1)."""
    sys.path.insert(0, str(REPO / "engine"))
    import run
    import structure_grid as sg
    path = REPO / table
    doc = json.loads(path.read_text(encoding="utf-8"))
    if doc.get("mode") == "quick":
        return False, "a quick table (mode quick) sits in the reference place (C161)"
    over = sg.refusal_over_cap(doc.get("no_answer", []))
    if over:
        return False, f"refusal span over the cap ({over}, C162)"
    body, _ = run.load_body(sg.BODIES_DIR / f"{doc['body'].lower()}.yaml")
    data, _code_in_file = sg._moved(doc["triggers"], sg.triggers(body.inputs))
    if data:
        return False, f"data triggers moved {data}"
    before = sg.GUARD_RUNS[0]
    worst, where = sg._recheck(doc, body)
    sg.GUARD_RUNS[0] += 1
    ok = worst <= sg.EPS
    return ok, (f"_recheck {'within' if ok else 'beyond'} ε: largest relative difference {worst:.3e} at {where} "
                f"(ε {sg.EPS:.4e}, {len(doc['t_pot'])} points; GUARD_RUNS {before} → {sg.GUARD_RUNS[0]})")


def check_command(argv: list, env_extra=None) -> tuple[bool, str]:
    env = dict(os.environ, **(env_extra or {}))
    env.setdefault("PYTHONPATH", str(REPO))
    r = subprocess.run([sys.executable if a == "{python}" else a for a in argv], cwd=REPO, env=env,
                       capture_output=True, text=True)
    tail = (r.stdout + r.stderr).strip().splitlines()[-3:]
    return r.returncode == 0, f"rc {r.returncode} · " + " | ".join(t[:160] for t in tail)


def run_check(e: dict) -> tuple[bool, str] | None:
    c = e.get("check")
    if not c:
        return None
    if c["kind"] == "structure_table":
        return check_structure_table(c["table"])
    if c["kind"] == "command":
        return check_command(c["argv"], c.get("env"))
    raise SystemExit(f"STOP: unknown check kind {c['kind']!r}")


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
    if not mv:
        out(f"[GREEN] {name} — stamp unchanged ({len(now['code'])} closure modules, {len(now['data'])} data, "
            f"{len(now['derived'])} derived, {len(now['out_of_tree']) - ('_ref' in now['out_of_tree'])} out-of-tree)")
        return 0
    res = run_check(e)
    if res is None:
        out(f"[RED] {name} — stamp moved ({'; '.join(mv[:8])}{' …' if len(mv) > 8 else ''}); no value check: rebuild "
            f"in this landing, or a ruling (G2, G6)")
        return _named(name, out)
    ok, why = res
    out(f"[{'GREEN' if ok else 'RED'}] {name} — stamp moved ({'; '.join(mv[:8])}{' …' if len(mv) > 8 else ''}); "
        f"check: {why}")
    return 0 if ok else _named(name, out)


def _named(name, out) -> int:
    item = expected_red(name)
    if item:
        out(f"  {name}: EXPECTED RED, gate_expected_red.yaml id {item.get('id')} — {item.get('registered', '')}")
    return 1


# ── G6: restamp ──────────────────────────────────────────────────────────────────────────────────────────────────────
def restamp(name: str, why: str, art_env=None) -> Path:
    kind, _, ev = why.partition(":")
    if kind not in REASONS or not ev:
        raise SystemExit(f"STOP: --why must be one of {', '.join(r + ':<evidence>' for r in REASONS)} (G6); got {why!r}")
    e = entries(load_list())[name]
    if kind == "ruling" and e.get("check"):
        raise SystemExit(f"STOP: {name} has a value check; a ruling restamps only stamp-only entries (G6)")
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
    output neither listed nor named not-tracked; a listed or exempt path that is not tracked."""
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
    if a.show:
        print(json.dumps(stamp(a.show, entries(doc)[a.show]), indent=1, sort_keys=True))
        return 0
    names = order if a.all else [a.entry]
    bad = sum(judge_entry(n, entries(doc)[n]) for n in names)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
