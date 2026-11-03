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
[LOAD] and the target's own exit code. Child processes are not seen, so a census run keeps one process: GRID_POOL=1, and
every multiprocessing Pool (multiprocessing.Pool, a context's .Pool) is replaced by an in-process serial stand-in.
With --restore, the entry's own files go back to HEAD and untracked files the run created are removed (each named).
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


def loaded(root: Path = REPO) -> list:
    """Repo-relative files of the project modules now in sys.modules (sorted)."""
    out = set()
    for m in list(sys.modules.values()):
        f = getattr(m, "__file__", None)
        if not f:
            continue
        try:
            rel = Path(f).resolve().relative_to(root).as_posix()
        except ValueError:
            continue
        if rel.endswith(".pyc"):                         # a sourceless load names its cache file; judge the source
            rel = rel.replace("__pycache__/", "").rsplit(".", 2)[0] + ".py"
        if rel.split("/")[0] in PROJECT:
            out.add(rel)
    return sorted(out)


def outside(name: str, mods: list, allow=()) -> list:
    sys.path.insert(0, str(HERE))
    import check as ck
    e = ck.entries(ck.load_list())[name]
    inside = set(ck.closure(e["code"])) if e.get("code") else set()
    inside |= {p for p in e.get("derived", []) if p.endswith(".py")} | set(e["files"]) | set(allow)
    return [m for m in mods if m not in inside]


def restore_own(name: str) -> str:
    """After a build census in the working tree: the entry's own files back to HEAD; says whether the rebuild matched."""
    import subprocess
    sys.path.insert(0, str(HERE))
    import check as ck
    files = ck.entries(ck.load_list())[name]["files"]
    diff = subprocess.run(["git", "-C", str(REPO), "diff", "--name-only", "--", *files], capture_output=True,
                          text=True, check=True).stdout.split()
    if diff:
        subprocess.run(["git", "-C", str(REPO), "checkout", "-q", "--", *diff], check=True)
    return (f"  {name}: the census build rewrote its files byte-identical" if not diff else
            f"  {name}: the census build's bytes differ in {diff} (restored from HEAD; a load census judges loads, "
            f"not bytes: read this beside the entry's check)")


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
    import multiprocessing
    import multiprocessing.context
    import multiprocessing.pool
    multiprocessing.Pool = SerialPool
    multiprocessing.pool.Pool = SerialPool
    multiprocessing.context.BaseContext.Pool = lambda self, *a, **k: SerialPool()


def untracked(root: Path = REPO) -> set:
    import subprocess
    out = subprocess.run(["git", "-C", str(root), "ls-files", "--others", "--exclude-standard", "-z"],
                         capture_output=True, text=True, check=True).stdout
    return {x for x in out.split("\0") if x}


def remove_new(before: set, root: Path = REPO) -> list:
    """Untracked files the census run created (not there before it): removed, returned by name."""
    new = sorted(untracked(root) - before)
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
    try:
        return [(p if p.is_absolute() else REPO / p).resolve().relative_to(REPO).as_posix()]
    except ValueError:
        return []                                        # an out-of-tree builder (8a–8d)


def main(argv) -> int:
    if "--" not in argv:
        raise SystemExit(__doc__)
    head, target = argv[:argv.index("--")], argv[argv.index("--") + 1:]
    name = head[head.index("--entry") + 1]
    allow = [head[i + 1] for i, a in enumerate(head) if a == "--allow"]
    restore = "--restore" in head
    own = target_files(target)
    before = untracked() if restore else set()
    rc = run_target(target)
    mods = loaded()
    out = outside(name, mods, allow + own)
    sys.stdout.flush()
    if restore:                                          # a build census writes the entry's own files: put HEAD back
        print(restore_own(name), flush=True)
        new = remove_new(before)
        if new:
            print(f"  {name}: removed the untracked files the census run created: {', '.join(new)}", flush=True)
    if out:
        print(f"[LOAD-RED] {name} — loaded outside the static closure ({len(out)} of {len(mods)} project modules): "
              f"{', '.join(out)}", flush=True)
        return 3
    print(f"[LOAD] {name} — {len(mods)} project modules loaded, all inside the static closure (target rc {rc})",
          flush=True)
    return rc


if __name__ == "__main__":
    os.environ["GRID_POOL"] = "1"                        # one process: a pool child's imports are not seen
    serial_pools()
    sys.exit(main(sys.argv[1:]))
