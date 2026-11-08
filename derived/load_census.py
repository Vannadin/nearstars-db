# 로드 센서스 — 한 항목의 빌드·검사를 이 프로세스 안에서 돌린 뒤 실제로 올라온 프로젝트 모듈(sys.modules)이 그 항목의 계산된 닫힘 안에 있는지 보고, 밖이면 이름 댄 빨강(sg-gate prereg 1765b55c G1, 대조군 N18)
"""python3 derived/load_census.py --entry NAME [--allow PATH ...] -- TARGET

TARGET is one of
    path/to/script.py ARGS...            run as __main__, its directory first on sys.path (as `python3 script.py`)
    -m module ARGS...                    run as `python3 -m module`
    --call path/to/file.py:func JSON     import the file's module and call func(*JSON) (JSON a list; default [])

After the target finishes (normally, by SystemExit, or by an exception), every module in sys.modules whose file is under
engine/, solver/ or scripts/ of this tree must be in the entry's closure (derived/check.py closure(), the stamped
code), in the entry's listed derived .py files (stamped as derived), or be the target file itself (a check script that is
not the build; also --allow). A module outside is printed by name on a [LOAD-RED] line and the exit code is 3; otherwise
[LOAD] and the target's own exit code. Pools run in-process (GRID_POOL=1; multiprocessing pools and
concurrent.futures.ProcessPoolExecutor replaced by serial stand-ins). Every Python child process (subprocess) gets
derived/census_site/ first on PYTHONPATH: it reports its own loads, opens and children at exit, and they are judged by the
same rule; a child that writes no report (-I/-E, or killed) is a named red. Module files that are neither stdlib,
site-packages nor engine/solver/scripts are printed as unjudged; one that is not exactly a declared `out_of_tree` path
under the resolved NEARSTARS_ARTIFACTS or under the out-of-tree target's own checkout is a [LOAD-RED] (CENSUS-OOT-COVER).
With --restore, the entry's own files go back to their bytes before the run and untracked files the run created are removed (each named).
Every declared external input is traced: the files the run opens (and the paths handed to subprocesses) must include
the stamped path, with the stamp's bytes; a different path, other bytes, or no open is a [LOAD-RED] naming both.
"""
import json
import os
import runpy
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PROJECT = ("engine", "solver", "scripts")


TOOLING = {"derived/load_census.py", "derived/check.py", "derived/digest.py", "derived/census_site/sitecustomize.py"}


def _system_prefixes() -> list:
    """stdlib and site-packages directories of this interpreter: modules there are not the project's."""
    import site
    import sysconfig
    paths = sysconfig.get_paths()
    out = {paths.get(k) for k in ("stdlib", "platstdlib", "purelib", "platlib")}
    try:
        out |= set(site.getsitepackages()) | {site.getusersitepackages()}
    except AttributeError:
        pass
    return sorted(os.path.realpath(x) for x in out if x)


def classify(files, root: Path = REPO, prefixes=None) -> tuple[list, list]:
    """(project, unjudged): project = repo-relative files under engine/, solver/, scripts/ (judged against the closure);
    unjudged = every other module file that is not stdlib, site-packages or the census's own tooling (68 on db1a128b:
    printed per row, so a module from another directory or checkout is never silent)."""
    prefixes = _system_prefixes() if prefixes is None else prefixes
    project, unjudged = set(), set()
    for f in files:
        real = os.path.realpath(f)
        if real.endswith(".pyc"):                        # a sourceless load names its cache file; judge the source
            real = real.replace("/__pycache__/", "/").rsplit(".", 2)[0] + ".py"
        try:
            rel = Path(real).relative_to(root).as_posix()
        except ValueError:
            rel = None
        if rel is not None and rel.split("/")[0] in PROJECT:
            project.add(rel)
        elif rel is not None and rel in TOOLING:
            continue
        elif any(real == q or real.startswith(q + os.sep) for q in prefixes):
            continue
        else:
            unjudged.add(rel if rel is not None else real)
    return sorted(project), sorted(unjudged)


def mirror_copies(files, root: Path = REPO) -> tuple[dict, list]:
    """({copy: rel}, rest): an unjudged file whose path ends in engine/…, solver/… or scripts/… and whose bytes equal
    that tree file's is judged as that module (check_graph_page runs the generator in a mirror). Anything else stays
    unjudged."""
    out, rest = {}, []
    for f in files:
        parts = Path(f).parts
        hit = None
        for i in range(len(parts) - 1, -1, -1):
            if parts[i] in PROJECT:
                rel = Path(*parts[i:])
                t = root / rel
                got = CHILD_SHA.get(f) or (_sha256(Path(f)) if os.path.isabs(f) and Path(f).is_file() else None)
                if got and t.is_file() and got == _sha256(t):
                    hit = rel.as_posix()
                break
        if hit:
            out[f] = hit
        else:
            rest.append(f)
    return out, rest


def module_files() -> list:
    return [f for m in list(sys.modules.values()) for f in [getattr(m, "__file__", None)] if isinstance(f, str)]


def loaded(root: Path = REPO) -> list:
    """Repo-relative files of the project modules now in sys.modules (sorted)."""
    return classify(module_files(), root)[0]


_INFO_CODE = r"""
import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import check as ck
name = sys.argv[2]
e = ck.entries(ck.load_list())[name]
inside = set(ck.closure(e["code"])) if e.get("code") else set()
inside |= {p for p in e.get("derived", []) if p.endswith(".py")} | set(e["files"])
ext = {}
for x, s in (e.get("external") or {}).items():
    base = ck.env_dir(s["env"]) if s.get("env") else None
    ext[x] = [str(Path(base) / s["path"]) if base else s["path"], s["path"]]
st = ck.read_stamp(name) or {}
try:
    art = str(Path(ck.env_dir("NEARSTARS_ARTIFACTS")).resolve())
except ck.NotRun:
    art = None
print(json.dumps({"files": e["files"], "inside": sorted(inside), "ext": ext, "ext_sha": dict(st.get("external") or {}),
                  "oot": list(e.get("out_of_tree") or []), "art": art}))
"""
_INFO: dict = {}


def entry_info(name: str) -> dict:
    """The entry's files, its closure (∪ listed derived .py ∪ its files), declared externals and stamped external sha256,
    read by check.py in a **separate interpreter** (68 HOLD B1 on 5db3db7f): check.py imports solver.fall_sets, and a
    project module the census tooling loads into the judged process would be masked as «loaded before the run»."""
    if name not in _INFO:
        import subprocess
        r = subprocess.run([sys.executable, "-B", "-c", _INFO_CODE, str(HERE), name], cwd=REPO,
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"load census: reading entry {name} from derived/files.yaml failed: {r.stderr.strip()[-400:]}")
        _INFO[name] = json.loads(r.stdout.strip().splitlines()[-1])
    return _INFO[name]


def oot_roots(info: dict, own) -> list:
    """The checkout roots an out_of_tree path is anchored at: the resolved NEARSTARS_ARTIFACTS, and the out-of-tree
    target's own checkout (the target is itself a declared path: its resolved path minus that path) — the go-live
    row8.py runs each generator from a worktree of the artifacts checkout, not from NEARSTARS_ARTIFACTS itself."""
    oot = info.get("oot") or []
    roots = [info["art"]] if info.get("art") else []
    for t in own:
        for o in oot:
            if os.path.isabs(str(t)) and str(t).endswith("/" + o):
                roots.append(str(t)[: -len(o) - 1])
    return sorted(set(roots))


def oot_uncovered(name: str, unjudged: list, own=()) -> list:
    """CENSUS-OOT-COVER (go-live s4r, directing 11-08): the unjudged module files no `out_of_tree` path of the entry
    declares. Covered means the file's resolved path equals resolve(root / path) for a declared path and an anchor root
    (oot_roots): a same-named file in any other checkout stays red. Undeclared foreign code reaching the build was
    printed and passed; it is red now."""
    info = entry_info(name)
    oot, roots = info.get("oot") or [], oot_roots(info, own)
    covered = {os.path.realpath(os.path.join(r, o)) for r in roots for o in oot}
    return [u for u in unjudged if os.path.realpath(str(u)) not in covered or not os.path.isabs(str(u))]


def outside(name: str, mods: list, allow=()) -> list:
    inside = set(entry_info(name)["inside"]) | set(allow)
    return [m for m in mods if m not in inside]


def snapshot_own(name: str, root: Path = REPO) -> dict:
    """The entry's own files as they are before the run (bytes, or None when absent): what --restore writes back. Not
    HEAD: a seat's uncommitted rebuild of an entry file must survive a census (68 on db1a128b)."""
    return {f: ((root / f).read_bytes() if (root / f).is_file() else None) for f in entry_info(name)["files"]}


def restore_own(name: str, snap: dict, root: Path = REPO) -> str:
    """After a build census: each of the entry's files back to its bytes before the run; says which the run changed."""
    changed = []
    for f, data in snap.items():
        p = root / f
        now = p.read_bytes() if p.is_file() else None
        if now != data:
            changed.append(f)
            if data is None:
                p.unlink()
            else:
                p.write_bytes(data)
    return (f"  {name}: the census build left its files as they were before the run" if not changed else
            f"  {name}: the census build changed {changed} (put back to the bytes before the run; a load census judges "
            f"loads, not bytes: read this beside the entry's check)")


class SerialPool:
    """In-process stand-in for multiprocessing.pool.Pool: the work runs here, so its imports land in sys.modules."""
    def __init__(self, *a, **k):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def map(self, f, it, chunksize=None):
        return [f(x) for x in it]

    def imap(self, f, it, chunksize=1):
        return (f(x) for x in it)

    imap_unordered = imap

    def starmap(self, f, it, chunksize=None):
        return [f(*x) for x in it]

    def close(self):
        pass

    def join(self):
        pass

    def terminate(self):
        pass


def serial_pools():
    """Every process pool runs in this process: multiprocessing pools and concurrent.futures.ProcessPoolExecutor
    (68 on db1a128b; a thread pool of one shares sys.modules)."""
    import concurrent.futures
    import concurrent.futures.process
    import concurrent.futures.thread
    import multiprocessing
    import multiprocessing.context
    import multiprocessing.pool
    multiprocessing.Pool = SerialPool
    multiprocessing.pool.Pool = SerialPool
    multiprocessing.context.BaseContext.Pool = lambda self, *a, **k: SerialPool()

    class SerialExecutor(concurrent.futures.thread.ThreadPoolExecutor):
        def __init__(self, max_workers=None, mp_context=None, initializer=None, initargs=(), **_):
            super().__init__(max_workers=1, initializer=initializer, initargs=initargs)

    concurrent.futures.ProcessPoolExecutor = SerialExecutor
    concurrent.futures.process.ProcessPoolExecutor = SerialExecutor


SITE = HERE / "census_site"
SPAWNED: list = []                                      # argv of every Python child this process started


def _is_python(argv) -> bool:
    exe = os.path.realpath(sys.executable)
    for a in list(argv)[:6]:                             # also behind /usr/bin/time, perf stat --, env
        a = os.fsdecode(a) if isinstance(a, (str, bytes, os.PathLike)) else ""
        base = os.path.basename(a)
        if a and (os.path.realpath(a) == exe or base.startswith("python") or base == "Python"):
            return True
    return False


def patch_popen(report_dir: str):
    """Every Python child gets the census site (first on its PYTHONPATH, whatever env the caller passed) and the report
    dir; the site chains to the next sitecustomize on the path (gate_reads, c143_naive_sum). A child started with -I or
    -E ignores PYTHONPATH and writes no report: the count below makes that a named red, never a silent pass."""
    import subprocess
    orig = subprocess.Popen.__init__
    if getattr(orig, "_census", False):
        return

    def init(self, args, *a, **k):
        argv = [args] if isinstance(args, (str, bytes, os.PathLike)) else list(args)
        if _is_python(argv):
            env = dict(k.get("env") if k.get("env") is not None else os.environ)
            env["PYTHONPATH"] = str(SITE) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
            env["LOAD_CENSUS_REPORT"] = report_dir
            env["GRID_POOL"] = "1"
            k["env"] = env
            SPAWNED.append([os.fsdecode(x) if isinstance(x, (str, bytes, os.PathLike)) else str(x) for x in argv][:4])
        return orig(self, args, *a, **k)

    init._census = True
    subprocess.Popen.__init__ = init


def write_child_report(report_dir: str):
    """atexit in a child: its module files, opened paths and Python children, one JSON file per pid."""
    main = [MAIN_FILE] if MAIN_FILE else []          # CPython drops __main__.__file__ once a script finishes
    files, pre = module_files() + main, _system_prefixes()
    sha = {}
    for f in files:                                       # a mirror dir may be gone before the parent reads this
        r = os.path.realpath(f)
        if not any(r == q or r.startswith(q + os.sep) for q in pre) and os.path.isfile(r):
            sha[r] = _sha256(Path(r))
    d = {"pid": os.getpid(), "argv": sys.argv[:3], "files": files, "prefixes": pre, "sha": sha,
         "opened": list(OPENED), "spawned": SPAWNED}
    Path(report_dir, f"{os.getpid()}.json").write_text(json.dumps(d), encoding="utf-8")


MAIN_FILE = None


def child_setup():
    """Called by census_site/sitecustomize.py in every Python child of a census run."""
    global MAIN_FILE
    report = os.environ["LOAD_CENSUS_REPORT"]
    a0 = (sys.argv or [""])[0]
    MAIN_FILE = os.path.abspath(a0) if a0.endswith(".py") and os.path.isfile(a0) else None
    import atexit
    sys.addaudithook(_audit)
    serial_pools()
    patch_popen(report)
    atexit.register(write_child_report, report)


CHILD_SHA: dict = {}                                    # sha256 of each non-system module file a child loaded


def read_children(report_dir: str, root: Path = REPO) -> tuple:
    """(project, unjudged, opened, Python children started in all, reports written) over every child report."""
    project, unjudged, opened, reports = set(), set(), [], []
    CHILD_SHA.clear()
    for f in sorted(Path(report_dir).glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        reports.append(d)
        p, u = classify(d["files"], root, d["prefixes"])
        project |= set(p)
        unjudged |= set(u)
        opened += d["opened"]
        CHILD_SHA.update(d.get("sha") or {})
    spawned = len(SPAWNED) + sum(len(d["spawned"]) for d in reports)
    return sorted(project), sorted(unjudged), opened, spawned, len(reports)


def output_specs(name: str) -> list:
    """The directories of the entry's own files: the only places --restore looks for, and removes, untracked files."""
    return sorted({os.path.dirname(f) or "." for f in entry_info(name)["files"]})


def untracked(root: Path = REPO, specs=None) -> set:
    """Untracked files under the git pathspecs SPECS (s4r GATE-INPUTS-DERIVED l.5734, directing 11-08 (a)): scoped to the
    entry's output directories, so the read trace records those, not the whole tree, and --restore can neither see nor
    touch a file outside them. SPECS None lists the whole tree (callers outside a census)."""
    import subprocess
    out = subprocess.run(["git", "-C", str(root), "ls-files", "--others", "--exclude-standard", "-z",
                          *(["--", *specs] if specs else [])], capture_output=True, text=True, check=True).stdout
    return {x for x in out.split("\0") if x}


def remove_new(before: set, root: Path = REPO, specs=None) -> list:
    """Untracked files under SPECS the census run created (not there before it): removed, returned by name."""
    new = sorted(untracked(root, specs) - before)
    for f in new:
        (root / f).unlink()
    return new


def run_target(target: list) -> int:
    """Run TARGET in this process; its exit code (an exception is 1, printed)."""
    try:
        if target[0] == "-m":
            sys.argv = [target[1]] + target[2:]
            sys.path.insert(0, os.getcwd())
            runpy.run_module(target[1], run_name="__main__", alter_sys=True)
        elif target[0] == "--call":
            spec, args = target[1], json.loads(target[2]) if len(target) > 2 else []
            path, func = spec.rsplit(":", 1)
            p = (REPO / path).resolve()
            sys.path.insert(0, str(p.parent))
            mod = __import__(p.stem)
            getattr(mod, func)(*args)
        else:
            p = Path(target[0]).resolve()
            sys.argv = [str(p)] + target[1:]
            sys.path.insert(0, str(p.parent))
            runpy.run_path(str(p), run_name="__main__")
        return 0
    except SystemExit as err:
        code = err.code
        return int(code) if isinstance(code, int) else (0 if code is None else 1)   # unittest exits with a bool
    except BaseException:                                # the census still runs on what was loaded
        traceback.print_exc()
        return 1


def target_files(target: list) -> list:
    """The check's own file(s): the script, the called file, or the test modules `-m unittest` names. A check script
    that is not the build is not in the closure; it is the thing run, not something the build loaded."""
    if target[0] == "-m":
        if target[1] == "unittest":                      # the test modules and their packages' __init__
            out = []
            for a in (a for a in target[2:] if not a.startswith("-")):
                parts = a.split(".")
                out += ["/".join(parts[:i]) + "/__init__.py" for i in range(1, len(parts))] + ["/".join(parts) + ".py"]
            return out
        return []
    p = Path(target[1].rsplit(":", 1)[0] if target[0] == "--call" else target[0])
    real = (p if p.is_absolute() else REPO / p).resolve()
    try:
        return [real.relative_to(REPO).as_posix()]
    except ValueError:
        # an out-of-tree builder (8a–8d) or a scratch target: its resolved path, the form `classify` gives an unjudged
        # file, so the thing run is not listed as a module the build loaded (CENSUS-OOT-COVER; it was, as [] here)
        return [str(real)]


OPENED: list = []                                       # every path the run opened or handed to a subprocess


def _audit(event, args):
    """Audit hook: Python file opens, and the path-like arguments of every subprocess (pdftotext reads its PDF there)."""
    try:
        if event == "open" and isinstance(args[0], (str, bytes)):
            OPENED.append(os.fsdecode(args[0]))
        elif event == "subprocess.Popen":
            argv = args[1] if isinstance(args[1], (list, tuple)) else [args[1]]
            OPENED.extend(os.fsdecode(a) for a in argv if isinstance(a, (str, bytes, os.PathLike)))
    except Exception:                                    # an audit hook must never break the run it watches
        pass


def _sha256(p: Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def external_reads(externals: dict, stamped_sha: dict, opened, cwd=None) -> tuple[list, list]:
    """(reds, notes) for the declared external inputs (note 1 §10, directing's AMMONIA-path ruling).
    externals: {name: (stamped path, declared relative path)}; stamped_sha: {name: sha256 the stamp holds} (may lack a
    name: no stamp yet). For each name, the files the run opened whose path ends in the declared relative path (or has
    its basename) are compared with the stamped path: a different path is red naming both (and the bytes of each); the
    same path is red when its bytes now differ from the stamp's; no such open at all is red (the build did not read
    the declared input where the stamp says)."""
    reds, notes = [], []
    cwd = Path(cwd or os.getcwd())
    seen = []
    for o in opened:
        q = Path(o) if os.path.isabs(o) else cwd / o
        seen.append(Path(os.path.normpath(q)))
    for name, (stamped, rel) in externals.items():
        st = Path(os.path.realpath(stamped))
        rel_parts = Path(rel).parts
        hits = sorted({q for q in seen if q.parts[-len(rel_parts):] == rel_parts or q.name == Path(rel).name})
        if not hits:
            reds.append(f"external {name}: the run opened no file at {rel!r}; the stamp hashes {stamped}")
            continue
        for q in hits:
            real = Path(os.path.realpath(q))
            got = _sha256(real) if real.is_file() else "absent"
            if real != st:
                want = _sha256(st) if st.is_file() else "absent"
                reds.append(f"external {name}: the build opened {q} (sha256 {got[:16]}) but the stamp hashes {stamped} "
                            f"(sha256 {want[:16]}): a different path")
            elif name in stamped_sha and got != stamped_sha[name]:
                reds.append(f"external {name}: the build opened the stamped path {q}, but its bytes (sha256 {got[:16]}) "
                            f"differ from the stamp's ({stamped_sha[name][:16]})")
            else:
                notes.append(f"external {name}: opened the stamped path {q}, sha256 {got[:16]} "
                             f"{'= the stamp' if name in stamped_sha else '(no stamp yet: bytes not compared)'}")
    return reds, notes


def reads_outside(opened, declared: set, root: Path = REPO) -> list:
    """Existing files the run (or a child) opened outside the repo, the interpreter's stdlib/site-packages and the temp
    dir: the survey of external reads (AMMONIA-path generalised). A declared external input is marked «*»."""
    import tempfile
    skip = _system_prefixes() + [os.path.realpath(tempfile.gettempdir()), os.path.realpath(sys.prefix),
                                 os.path.realpath(sys.base_prefix), os.path.realpath(str(root)), "/dev", "/etc",
                                 "/usr", "/System", "/Library", "/opt/homebrew", "/private/etc", "/private/var"]
    out = set()
    for o in opened:
        if not os.path.isabs(o):
            continue
        r = os.path.realpath(o)
        if not os.path.isfile(r) or any(r == q or r.startswith(q.rstrip(os.sep) + os.sep) for q in skip):
            continue
        out.add(r + (" *" if r in declared else ""))
    return sorted(out)


#: path overrides read by closure modules (note 1 §10 survey): set, the build reads another directory than the tree
#: files its stamp hashes (the AMMONIA-path split, generalised). Literal reads, so the env census sees each name.
def path_overrides() -> list:
    read = {"MANTLE_TABLE_DIR": os.environ.get("MANTLE_TABLE_DIR"),           # mantle_composition.TABLE_DIR
            "STRUCTURE_GRID_DIR": os.environ.get("STRUCTURE_GRID_DIR"),       # structure_grid.GRID_DIR
            "NS_FALL_SETS": os.environ.get("NS_FALL_SETS"),                   # material_assemblage.FALL_SETS_DIR
            "NS_BUILD_ASSEMBLAGE": os.environ.get("NS_BUILD_ASSEMBLAGE")}     # rho_fall_build's out-of-tree builder
    return [f"path override {k}={v} is set: the build reads that directory, the stamp hashes the tree's files"
            for k, v in read.items() if v]


def entry_externals(name: str) -> tuple[dict, dict]:
    info = entry_info(name)
    return {x: tuple(v) for x, v in info["ext"].items()}, dict(info["ext_sha"])


def main(argv) -> int:
    if "--" not in argv:
        raise SystemExit(__doc__)
    import tempfile
    pre_tool = set(module_files())                       # before the census reads anything: what startup loaded
    head, target = argv[:argv.index("--")], argv[argv.index("--") + 1:]
    name = head[head.index("--entry") + 1]
    allow = [head[i + 1] for i, a in enumerate(head) if a == "--allow"]
    restore = "--restore" in head
    own = target_files(target)
    entry_info(name)                                     # check.py runs in its own interpreter, never in this one
    before = untracked(specs=output_specs(name)) if restore else set()
    snap = snapshot_own(name) if restore else {}
    reports = tempfile.mkdtemp(prefix="load-census-")
    pre = set(module_files())                            # the census's own imports, before the run
    early = [m for m in classify(sorted(pre))[0] if m.split("/", 1)[0] in ("engine", "solver")]
    tool_loaded = [m for m in classify(sorted(pre - pre_tool))[0]]   # project modules the tooling itself loaded
    sys.addaudithook(_audit)
    patch_popen(reports)
    rc = run_target(target)
    opened = list(OPENED)                                # the run's opens only, before the census reads its own files
    mods, unjudged = classify([f for f in module_files() if f not in pre])
    c_mods, c_unjudged, c_opened, spawned_n, reports_n = (*read_children(reports), )
    import shutil
    shutil.rmtree(reports, ignore_errors=True)
    mirrored, unjudged = mirror_copies(sorted((set(unjudged) | set(c_unjudged)) - set(own)))
    mods = sorted(set(mods) | set(c_mods) | set(mirrored.values()))
    for src, rel in sorted(mirrored.items()):
        print(f"  {name}: {src} is a byte-identical copy of {rel} (a mirror run): judged as {rel}", flush=True)
    out = outside(name, mods, allow + own)
    ext, ext_sha = entry_externals(name)
    ext_red, ext_notes = external_reads(ext, ext_sha, opened + c_opened, REPO)
    sys.stdout.flush()
    if restore:                                          # a build census writes the entry's own files: put the pre-run bytes back
        print(restore_own(name, snap), flush=True)
        new = remove_new(before, specs=output_specs(name))
        if new:
            print(f"  {name}: removed the untracked files the census run created: {', '.join(new)}", flush=True)
    for n in ext_notes:
        print(f"  {name}: {n}", flush=True)
    outer = reads_outside(opened + c_opened, {os.path.realpath(v[0]) for v in ext.values()})
    print(f"  {name}: files read outside the tree, stdlib, site-packages and temp (declared external marked *): "
          f"{', '.join(outer) if outer else 'none'}", flush=True)
    print(f"  {name}: {len(SPAWNED)} Python child process(es) started by the target, {reports_n} child report(s) "
          f"over {spawned_n} started in all", flush=True)
    print(f"  {name}: unjudged module files (not stdlib, site-packages or engine/solver/scripts): "
          f"{', '.join(unjudged) if unjudged else 'none'}", flush=True)
    undeclared = oot_uncovered(name, unjudged, own)
    if unjudged:
        print(f"  {name}: of those, not declared in the entry's out_of_tree: {', '.join(undeclared) or 'none'}",
              flush=True)
    oot_red = [f"unjudged module file(s) not declared in out_of_tree ({len(undeclared)}): {', '.join(undeclared)}"] \
        if undeclared else []
    miss = [] if reports_n >= spawned_n else [f"{spawned_n - reports_n} of {spawned_n} Python child processes wrote no "
                                             f"census report (started with -I/-E, or killed): their loads are unseen"]
    over = path_overrides()
    before = sorted(set(early) | set(tool_loaded))
    # s4r item (1): the line names the judged set (`before`); other project modules the interpreter loaded at start
    # (the gate's PYTHONPATH puts scripts/gate_reads/sitecustomize.py there) are allowed and listed apart, not as «none»'s
    # replacement
    startup = [m for m in classify(sorted(pre))[0] if m not in before]
    # no «): » in this clause: pc-golive.sh's S5 summary cuts the line at its last «): »
    allowed = f" · also loaded at interpreter start, allowed — {', '.join(startup)}" if startup else ""
    print(f"  {name}: project modules loaded before the target (not judged; must be none from engine/ or solver/, and "
          f"none the census tooling loaded): {', '.join(before) or 'none'}{allowed}", flush=True)
    masked = [f"loaded into the census process before the target, so not judged (68 B1): {', '.join(before)}"] \
        if before else []
    if out or ext_red or miss or over or masked or oot_red:
        why = ([f"loaded outside the static closure ({len(out)} of {len(mods)} project modules): {', '.join(out)}"]
               if out else []) + ext_red + miss + over + masked + oot_red
        print(f"[LOAD-RED] {name} — {'; '.join(why)} (target rc {rc})", flush=True)
        return 3
    print(f"[LOAD] {name} — {len(mods)} project modules loaded (children included), all inside the static closure"
          f"{f'; {len(ext)} external input(s) read at the stamped path' if ext else ''} (target rc {rc})",
          flush=True)
    return rc


if __name__ == "__main__":
    os.environ["GRID_POOL"] = "1"                        # one process: a pool child's imports are not seen
    serial_pools()
    sys.exit(main(sys.argv[1:]))
