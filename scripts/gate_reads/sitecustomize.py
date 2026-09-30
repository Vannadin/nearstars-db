# 게이트 단계가 데이터로 읽은 파일을 기록하는 감사 후크 — GATE_READS_LOG 가 있을 때만 켜진다 (C136)
"""Record the files a gate step reads *as data* (C136 §1.2).

Active only when `GATE_READS_LOG` is set; `check.sh` puts this directory on `PYTHONPATH` for the
full lane, so every Python process a step starts (children included) loads it at start-up.

One JSON line per read, appended to `$GATE_READS_LOG`:
    {"step": $GATE_STEP, "kind": "open" | "git" | "list" | "gitlist", "path": <repo-relative>}

`gitlist` is a `git ls-files` / `git grep` / `git ls-tree` pathspec, as written (`*` for none);
`glob` is a `glob.glob` pattern, repo-relative (glob's own directory walk is not logged again).

⚠ **Import reads are dropped by the calling frame, not by the path.** CPython raises the same
`open` audit event from `io.open_code`, which the import system calls for every module it loads.
The event is dropped only when the **innermost** Python frame — `sys._getframe(1)` here, the one
that called `open` / `open_code` — is the frozen import machinery (`SourceLoader.get_data`, or
zipimport probing the main script), or when there is no Python frame (the interpreter loading the
main script).
Ancestors are not looked at: a module whose top-level code opens a table while it is being
imported has import frames *below* it, and that read is data (audit HOLD 2). A step that `open()`s
an imported module's source as text is recorded; its import of the same file is not.

`GATE_READS_RAW=1` also writes the dropped events, with `"dropped": true` (fixture D-import).
At exit, recorded `.py` paths that are also some loaded module's `__file__` are written as
`"kind": "leak"` — printed by the census, never dropped.
"""
import atexit
import json
import os
import sys

_LOG = os.environ.get("GATE_READS_LOG")
_ROOT = os.path.realpath(os.environ.get("GATE_READS_ROOT") or os.getcwd())
_STEP = os.environ.get("GATE_STEP", "?")
_RAW = os.environ.get("GATE_READS_RAW") == "1"
# ⚠ the import machinery is importlib **and** zipimport — `python3 x.py` first asks zipimport whether
#   x.py is a zip archive (`_read_directory` opens it), then the interpreter opens it with no Python
#   frame at all. Both are the step's own code being loaded, not data.
_IMPORT_FRAMES = ("<frozen importlib", "<frozen zipimport>", "<interpreter>")


def _rel(path):
    try:
        p = os.path.realpath(os.fsdecode(path))
    except (TypeError, ValueError):
        return None
    if p != _ROOT and not p.startswith(_ROOT + os.sep):
        return None
    return os.path.relpath(p, _ROOT)


def _install():
    seen = set()
    recorded_py = set()
    busy = [False]
    write = open(_LOG, "a", encoding="utf-8", buffering=1).write   # opened before the hook exists

    def emit(kind, rel, dropped=False):
        key = (kind, rel, dropped)
        if key in seen:
            return
        seen.add(key)
        rec = {"step": _STEP, "kind": kind, "path": rel}
        if dropped:
            rec["dropped"] = True
        write(json.dumps(rec, ensure_ascii=False) + "\n")

    def hook(event, args):
        if busy[0]:
            return
        busy[0] = True
        try:
            if event == "open":
                path, mode, flags = args
                if isinstance(path, int):
                    return
                if mode is None:                        # os.open: read unless WRONLY / RDWR+CREAT
                    if flags & (os.O_WRONLY | os.O_CREAT | os.O_TRUNC):
                        return
                elif not ("r" in mode or "+" in mode):
                    return
                rel = _rel(path)
                if rel is None:
                    return
                try:
                    caller = sys._getframe(1).f_code.co_filename
                except ValueError:                      # no Python frame: the interpreter itself
                    caller = "<interpreter>"            #   opening the main script to run it
                if caller.startswith(_IMPORT_FRAMES):
                    if _RAW:
                        emit("open", rel, dropped=True)
                    return
                if rel.endswith(".py"):
                    recorded_py.add(rel)
                emit("open", rel)
            elif event in ("os.listdir", "os.scandir"):
                # ⚠ the import system's `FileFinder` lists every directory on `sys.path` — the same
                #   innermost-frame rule drops those listings
                caller = sys._getframe(1).f_code.co_filename
                if caller.startswith(_IMPORT_FRAMES):
                    return
                if caller.endswith(os.sep + "glob.py"):     # glob's own walk — its pattern is logged below
                    return
                rel = _rel(args[0] if args[0] is not None else ".")
                if rel is not None:
                    emit("list", rel)
            elif event == "glob.glob":
                pat = os.fsdecode(args[0])
                full = pat if os.path.isabs(pat) else os.path.join(os.getcwd(), pat)
                head, tail = os.path.split(full)
                while any(c in head for c in "*?["):     # the literal directory part only
                    head, t2 = os.path.split(head)
                    tail = os.path.join(t2, tail)
                rel = _rel(head)
                if rel is not None:
                    emit("glob", tail if rel == "." else os.path.join(rel, tail))
            elif event == "subprocess.Popen":
                argv = args[1]
                if isinstance(argv, (str, bytes)):
                    argv = [argv]
                argv = [os.fsdecode(a) for a in (argv or []) if isinstance(a, (str, bytes, os.PathLike))]
                sub = next((a for a in argv[1:] if a in ("ls-files", "grep", "ls-tree")), None)
                if len(argv) >= 2 and os.path.basename(argv[0]) == "git" and sub:
                    # a path enumeration: a file added under the pathspec changes what the step sees.
                    # The pathspecs after `--` (or none = the whole tree) become globs as written.
                    specs = argv[argv.index("--") + 1:] if "--" in argv else []
                    if sub == "ls-files" and "--" not in argv:
                        specs = [a for a in argv[argv.index(sub) + 1:] if not a.startswith("-")]
                    specs = [s for s in specs if not s.startswith(":!")] or ["*"]
                    for s in specs:
                        emit("gitlist", s)
                elif len(argv) >= 2 and os.path.basename(argv[0]) == "git" and "show" in argv:
                    cwd = args[2] or os.getcwd()
                    for a in argv:
                        if ":" in a and not a.startswith("-"):
                            path = a.split(":", 1)[1]
                            if path:
                                # `git show <rev>:<path>` is repo-root relative unless it starts with ./
                                full = os.path.join(cwd, path) if path.startswith("./") else os.path.join(_ROOT, path)
                                rel = _rel(full)
                                if rel is not None:
                                    emit("git", rel)
        except Exception:
            pass
        finally:
            busy[0] = False

    def at_exit():
        busy[0] = True
        loaded = set()
        for m in list(sys.modules.values()):
            f = getattr(m, "__file__", None)
            if f:
                r = _rel(f)
                if r:
                    loaded.add(r)
        for rel in sorted(recorded_py & loaded):
            emit("leak", rel)

    sys.addaudithook(hook)
    atexit.register(at_exit)


if _LOG:
    _install()
