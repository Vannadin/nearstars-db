# ρ 보수의 떨어짐 집합 적재기 — 출하 집합(materials/fall_sets/*.json.gz)을 읽고, 없거나 낡으면 이름 붙은 거절, 읽기의 가져오기 폐포·엔진 조사로 도장 (E24 등록 reg-e24-fallsets.md)
"""The ρ repair's fall-interval sets as shipped (registration rewrite/c1-read/reg-e24-fallsets.md, frozen ccb82429).

material_assemblage.py is byte-identical under this package (its blob is pinned by the records' closure_terms): the
loader lives here and replaces `AssemblageView._fall_set_load` when that module finishes executing (solver/__init__.py's
meta-path hook, rule 2). This module and solver/__init__.py are outside the read's closure by name: they decide which
sets load and whether a load refuses, never a read value.

- `directory()`: `material_assemblage.FALL_SETS_DIR` (NS_FALL_SETS, read at call time) if set, else DEFAULT_DIR.
- `load(view)` (installed as `_fall_set_load`): the record's sets, or a TableStop «fall sets» by name: a missing file
  for a shipped record (`is_shipped`: its id and its table pin are solver/materials/<id>.yaml's) with the repair on
  (rule 3); a file whose stamp differs from this tree's (rule 4). A record that only reuses a shipped id reads no
  shipped file and gets no refusal.
- `closure()`, `engine_static()`, `engine_census(records)`, `closure_stamp(records)`: the stamp (rule 1).
- `export(full, out, stamp)`: the compact, byte-stable shipped form.

Limits named (68 n5, n6; the registration's audits): the static half carries the engine modules on branches the census
sweep never visits and the literal data paths in their source; a data file opened only on an unswept branch through a
computed path is in neither half. The census sees one process and one thread (r2 n1): the audit hook and the profiler
are per process and per thread, so a read routed through parallel_points or a worker would be invisible; today's reads
are serial. The census sees Python-level opens (the «open» audit event: open, io.open,
Path.read_*); a C extension's own fopen is invisible to it. At 1868f06c no module of the read's closure opens engine data
through a C reader (np.load / fromfile / h5py / loadtxt: none), and seafreeze, which reads its own data in C, is out of
the repo and reported by version only."""
from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SOLVER = Path(__file__).resolve().parent
REPO = SOLVER.parent
ENGINE = REPO / "engine"
DEFAULT_DIR = SOLVER / "materials" / "fall_sets"
EXCLUDED = frozenset({"__init__", "fall_sets"})       # outside the closure by name (rule 1): they never change a value
DATA_SUFFIXES = (".json", ".npz", ".npy", ".csv", ".dat", ".txt", ".h5", ".yaml", ".yml", ".gz")
PACKAGES = ("numpy", "scipy", "yaml", "burnman", "seafreeze")
REGION_KINDS = ("body", "edge_window", "swap_extension", "melt_window", "frozen_cap")
STAMP_KEY = "read_closure"


def _ma():
    return sys.modules.get("solver.material_assemblage") or __import__("solver.material_assemblage",
                                                                       fromlist=["x"])


def _stop(why):
    return _ma().TableStop(why, check="fall sets")


def blob(path) -> str:
    """The git blob id of a file's bytes as they are on disk now (the module as loaded: the process reads the same)."""
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


# ── the stamp (rule 1) ────────────────────────────────────────────────────────────────────────────────────────────
_SOLVER_IMPORT = (re.compile(r"^\s*from solver import ([\w ,]+)", re.M),
                  re.compile(r"^\s*from solver\.(\w+) import", re.M),
                  re.compile(r"^\s*import solver\.(\w+)", re.M))
_BARE_IMPORT = (re.compile(r"^\s*import ([\w ,]+)", re.M), re.compile(r"^\s*from (\w+) import", re.M))
_DATA_LITERAL = re.compile(r"""["']([\w./-]+(?:%s))["']""" % "|".join(re.escape(s) for s in DATA_SUFFIXES))


def _names(text, pats):
    out = set()
    for pat in pats:
        for m in pat.findall(text):  # x3-ok: import lines of source files (the stamp's closure), never a refusal's text
            out |= {x.strip().split(" as ")[0].strip() for x in m.split(",") if x.strip()}
    return out


def closure(root=REPO) -> list:
    """The read's solver/ import closure: every `from solver …` / `import solver.…` of material_assemblage.py,
    followed transitively, function-local imports included, minus EXCLUDED."""
    seen, todo = set(), ["material_assemblage"]
    while todo:
        m = todo.pop()
        f = Path(root) / "solver" / f"{m}.py"
        if m in seen or m in EXCLUDED or not f.exists():
            continue
        seen.add(m)
        todo += sorted(_names(f.read_text(encoding="utf-8"), _SOLVER_IMPORT))
    return sorted(seen)


def engine_static(root=REPO) -> dict:
    """The static engine half (68 guard i, n5): {"modules": the engine modules reached by following bare imports from
    the solver closure's modules into engine/ (legacy_materials puts engine/ on sys.path) and on within engine/,
    "data": the literal data paths in those modules' source that exist under engine/}."""
    eng = Path(root) / "engine"
    seen, todo = set(), []
    for m in closure(root):
        todo += sorted(_names((Path(root) / "solver" / f"{m}.py").read_text(encoding="utf-8"), _BARE_IMPORT))
    while todo:
        m = todo.pop()
        f = eng / f"{m}.py"
        if m in seen or not f.exists():
            continue
        seen.add(m)
        todo += sorted(_names(f.read_text(encoding="utf-8"), _BARE_IMPORT))
    data = set()
    for m in seen:
        for lit in _DATA_LITERAL.findall((eng / f"{m}.py").read_text(encoding="utf-8")):
            for cand in (eng / lit, eng / Path(lit).name):
                if cand.is_file():
                    data.add(cand.relative_to(root).as_posix())
    return {"modules": sorted(f"engine/{m}.py" for m in seen), "data": sorted(data)}


_CENSUS_MAIN = r"""
import json, os, sys
SEEN = {"open": set()}
ROOT = sys.argv[1]
def hook(event, args):
    if event == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
        p = os.fsdecode(args[0])
        if not os.path.isabs(p):
            p = os.path.join(os.getcwd(), p)
        p = os.path.realpath(p)
        if p.startswith(ROOT + os.sep):
            SEEN["open"].add((os.path.relpath(p, ROOT).replace(os.sep, "/"), SEEN.get("window", "load")))
sys.addaudithook(hook)
ENG = os.path.join(ROOT, "engine") + os.sep
CALLED, LOADCALLED = set(), set()
DEPTH = [0]                                            # inside an in-repo module's import: its own execution, not a call
def prof(frame, event, arg):
    code = frame.f_code
    if code.co_name == "<module>":
        if code.co_filename.startswith(ROOT + os.sep) and event in ("call", "return"):
            DEPTH[0] += 1 if event == "call" else -1
        return
    if event == "call" and not DEPTH[0]:
        f = code.co_filename
        if f.startswith(ENG):
            (CALLED if SEEN.get("window") == "read" else LOADCALLED).add(os.path.relpath(f, ROOT).replace(os.sep, "/"))
sys.path.insert(0, ROOT)
from solver import fall_sets as fs
if len(sys.argv) > 4 and sys.argv[4]:
    exec(sys.argv[4])                                  # a test's planted change inside the read (census mutants)
sys.setprofile(prof)
out = fs._sweep(json.loads(sys.argv[2]), sys.argv[3] or None, SEEN)
sys.setprofile(None)
mods = sorted({os.path.relpath(os.path.realpath(m.__file__), ROOT).replace(os.sep, "/")
               for m in list(sys.modules.values()) if getattr(m, "__file__", None)
               and os.path.realpath(m.__file__).startswith(ROOT + os.sep)})
print("CENSUS " + json.dumps({"modules": mods, "opens": sorted(SEEN["open"]), "called": sorted(CALLED),
                              "called_at_load": sorted(LOADCALLED), "points": out}))
"""


def _region_points(v, table=None):
    """{kind: [(P, T)]} for one view (registration rev 5 rule 1, 68 guard ii): body = every T row × every P cell
    centre; edge window = every edge run row's P_b ± 1e-6, 1e-3, 1e-2 (relative); swap extension = each swap run's
    P_b_ext one T row past each end, ± 1e-6, where it extends, and every extension row of the table at its T around its
    swap curve's end P (± 1e-6, 1e-3); melt window = each P cell centre at T past the last row in 150 K steps
    until φ ≥ 1 (six at most) and every row T where φ > 0; frozen cap = each frozen cell and the P midpoint to its
    non-frozen neighbour."""
    import math
    ma = _ma()
    ps, ts = list(v.ps), list(v.ts)
    cen = [math.sqrt(a * b) for a, b in zip(ps, ps[1:])]
    out = {k: [] for k in REGION_KINDS}
    out["body"] = [(p, t) for t in ts for p in cen]
    for c in v._events:
        if c.kind == "edge":
            for r in c.rows:
                out["edge_window"] += [(r["p_b"] * (1 + s * e), r["t"]) for e in (1e-6, 1e-3, 1e-2) for s in (-1, 1)]
        elif c.kind == "swap":
            for t in [x for x in ts if x < c.t0][-1:] + [x for x in ts if x > c.t1][:1]:
                pe = c.p_b_ext(t, v._reach)
                if pe is not None:
                    out["swap_extension"] += [(pe * (1 - 1e-6), t), (pe * (1 + 1e-6), t)]
    # the swap-extension registration's rows (frozen 8402255e): past a swap curve's true end the read settles each side
    # at the extension row's T; read there around the curve's end P (and the row's own P_b where it has one)
    ends = {}
    for c in v._curves:
        if c.kind == "swap":
            ends.setdefault(c.t0, []).append(c.rows[0]["p_b"])
            ends.setdefault(c.t1, []).append(c.rows[-1]["p_b"])
    for r in ((table or {}).get("boundaries") or {}).get("extension", {}).get("rows", ()):
        for pb in ends.get(r.get("curve_end_t"), []) + ([r["p_b"]] if r.get("p_b") else []):
            out["swap_extension"] += [(pb * (1 + s * e), r["t"]) for e in (1e-6, 1e-3) for s in (-1, 1)]
    lm = ma._lm()
    for p in cen:
        for t in ts:
            if lm.silicate_melt_phi(p, t, v.variant) > 0.0:
                out["melt_window"].append((p, t))
        t = ts[-1]
        for _ in range(6):
            t += 150.0
            out["melt_window"].append((p, t))
            if lm.silicate_melt_phi(p, t, v.variant) >= 1.0:
                break
    for (ia, ib), c in ((k, v._cell(*k)) for k in ((ia, ib) for ia in range(len(ps)) for ib in range(len(ts)))):
        if c is not None and c.get("kind") == "frozen":
            out["frozen_cap"].append((ps[ia], ts[ib]))
            for ja in (ia - 1, ia + 1):
                n = v._cell(ja, ib) if 0 <= ja < len(ps) else None
                if n is not None and n.get("kind") != "frozen":
                    out["frozen_cap"].append((math.sqrt(ps[ia] * ps[ja]), ts[ib]))
    return out


def _sweep(records, sets_dir, seen):
    """The census sweep, inside its own process (engine_census): every record × every region kind, each point read
    through the view's whole point interface (state, dtdp, s_path, phase_read, onset_curves, and thermal where the view has it), with the repair on and
    the sets from `sets_dir` loaded unchecked (the export's census runs before the stamp exists). Solver-side opens are
    recorded only while reading (the «read» window); engine-side opens from process start (r2 n1)."""
    from solver import material_registry as mr
    ma = _ma()
    raw = {}
    if sets_dir:
        for rid in records:
            f = find(Path(sets_dir), rid)
            raw[rid] = parse_sets(_read(f)) if f else {}

    def unchecked(self):
        if self._fall_sets is None:
            self._fall_sets = raw.get(self.material_id, {})
        return self._fall_sets
    ma.AssemblageView._fall_set_load = unchecked          # before the registry's eager check reads it
    reg = mr.load()
    if not isinstance(reg, mr.Registry):
        raise SystemExit(f"STOP: the registry does not load: {reg!r}")
    counts = {}
    for rid in records:
        v = ma.view(ma.mv.thaw_plain(reg.records[rid]), reg.tables[rid], 1600.0)
        pts = _region_points(v, reg.tables[rid])
        counts[rid] = {k: (len(x) if x else "none in this record") for k, x in pts.items()}
        reads = [getattr(v, n) for n in ("state", "dtdp", "s_path", "phase_read", "thermal", "onset_curves")
                 if callable(getattr(v, n, None))]
        seen["window"] = "read"
        for x in (v.seams, v.transitions, v.source_seams, v.s_open_ends):
            try:
                x()
            except Exception:
                pass
        for c in v._curves:
            try:
                v.curve_slope_points(c)
            except Exception:
                pass
        for kind, xs in pts.items():
            for p, t in xs:
                for f in reads:
                    try:
                        f(p, t)
                    except Exception:                    # a refusal is a read too: what it loaded is recorded
                        pass
        seen["window"] = "load"
    return counts


def engine_census(records, sets_dir=None, root=REPO, plant=None) -> dict:
    """The run-time census (rule 1, as directing ruled 10-25 on the census's first run, post-registration note 1): a
    fresh process with an audit hook installed before any solver import sweeps `records` (_sweep) under a profiler
    limited to the read window, and returns {"engine": {path: blob} of the engine files whose code is called during the
    reads and of every engine data file opened at any time in the process, "imported_not_read": the engine modules
    imported but never called during the reads (process_state's snapshot imports: listed, not compared),
    "solver_data": {path: blob} of the solver/ data files opened while reading (minus the stamped record yaml and table
    and the set files), "modules": the in-repo modules loaded (for the drift test), "points": per record and kind}."""
    root = Path(root).resolve()
    env = dict(os.environ, PYTHONPATH=str(root), PYTHONDONTWRITEBYTECODE="1", NS_RHO_BRIDGE="1")
    got = subprocess.run([sys.executable, "-B", "-c", _CENSUS_MAIN, str(root), json.dumps(list(records)),
                          str(sets_dir or ""), plant or ""], capture_output=True, text=True, env=env, cwd=str(root))
    line = [x for x in got.stdout.splitlines() if x.startswith("CENSUS ")]
    if got.returncode != 0 or not line:
        raise RuntimeError(f"census sweep failed (rc {got.returncode}): {got.stderr[-2000:]}")
    d = json.loads(line[-1][7:])
    stamped = set()
    for rid in records:
        stamped.add(f"solver/materials/{rid}.yaml")
        a = _record_file(rid, root)
        if a:
            stamped.add(a)
    eng, sol = {}, {}
    for path, window in d["opens"]:
        if path.endswith((".py", ".pyc")) or "/__pycache__/" in path:
            continue
        if path.startswith("engine/"):
            eng[path] = blob(root / path)
        elif path.startswith("solver/") and window == "read" and path not in stamped \
                and not path.startswith("solver/materials/fall_sets/"):
            sol[path] = blob(root / path)
    for m in d["called"]:
        eng[m] = blob(root / m)
    imported = sorted(m for m in d["modules"] if m.startswith("engine/") and m.count("/") == 1 and m not in eng)
    return {"engine": dict(sorted(eng.items())), "imported_not_read": imported, "solver_data": dict(sorted(sol.items())),
            "called_at_load": d["called_at_load"], "modules": d["modules"], "points": d["points"]}


_SIDE_MAIN = r'''
import importlib, json, os, sys
ROOT = sys.argv[1]
sys.path.insert(0, os.path.join(ROOT, "engine"))
read, only = json.loads(sys.argv[2]), json.loads(sys.argv[3])
def snap(names):
    out = {}
    for n in names:
        m = sys.modules[n]
        for k, v in vars(m).items():
            if k.startswith("__"):
                continue
            r = repr(v)
            out[f"{n}.{k}"] = r if len(r) < 4000 else str(hash(r))
    return out
pre = sorted(n for n in only if n in sys.modules)
for n in read:
    importlib.import_module(n)
pre += sorted(n for n in only if n in sys.modules and n not in pre)
a = snap(read)
for n in only:
    importlib.import_module(n)
b = snap(read)
print("SIDE " + json.dumps({"changed": sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k)), "preimported": pre}))
'''


def import_side_effects(called, imported, root=REPO) -> dict:
    """Directing 10-25's check on the import-only modules: in a fresh process, import the engine modules the read
    calls, snapshot their module globals (repr), import the import-only modules, snapshot again. {"changed": globals
    that differ, "preimported": import-only modules already imported by the read modules themselves (their import
    side effects precede the snapshot and are not checked here: named)}."""
    stem = lambda ps: [Path(p).stem for p in ps]
    got = subprocess.run([sys.executable, "-B", "-c", _SIDE_MAIN, str(Path(root).resolve()),
                          json.dumps(stem(called)), json.dumps(stem(imported))], capture_output=True, text=True,
                         env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), cwd=str(root))
    line = [x for x in got.stdout.splitlines() if x.startswith("SIDE ")]
    if got.returncode != 0 or not line:
        raise RuntimeError(f"side-effect check failed (rc {got.returncode}): {got.stderr[-2000:]}")
    return json.loads(line[-1][5:])


def _record_file(rid, root=REPO):
    """The record's compact table path (solver/materials/<assemblage.file>), from its yaml, or None."""
    import yaml
    f = Path(root) / "solver" / "materials" / f"{rid}.yaml"
    if not f.exists():
        return None
    a = (yaml.safe_load(f.read_text(encoding="utf-8")) or {}).get("assemblage") or {}
    return f"solver/materials/{a['file']}" if a.get("file") else None


def _switches():
    from solver import legacy_materials as lm
    return lm._switch_bytes().hex()


def _packages():
    out = {}
    for name in PACKAGES:
        try:
            out[name] = getattr(__import__(name), "__version__", "unversioned")
        except ImportError:
            out[name] = "absent"
    return out


def tree_stamp(census, root=REPO) -> dict:
    """The stamp this tree has for a given census: the solver closure's blobs, the engine half (static ∪ census), the
    solver data the census opened, the engine switches, and the packages (reported only)."""
    root = Path(root)
    st = engine_static(root)
    eng = {p: blob(root / p) for p in st["modules"] + st["data"]}
    eng.update({p: blob(root / p) for p in census["engine"] if (root / p).exists()})
    return {"solver": {m: blob(root / "solver" / f"{m}.py") for m in closure(root)},
            "engine": dict(sorted(eng.items())),
            "engine_static": st,
            "solver_data": {p: blob(root / p) for p in census.get("solver_data", {}) if (root / p).exists()},
            "switches": _switches(), "packages": _packages()}


def closure_stamp(records, sets_dir=None, root=REPO) -> dict:
    """The full stamp an export writes: tree_stamp over a fresh census of `records`, plus the census's lists."""
    cen = engine_census(records, sets_dir, root)
    out = tree_stamp(cen, root)
    out["census"] = {"engine": sorted(cen["engine"]), "imported_not_read": cen["imported_not_read"],
                     "called_at_load": cen["called_at_load"],
                     "solver_data": sorted(cen["solver_data"]), "points": cen["points"]}
    return out


def drift(stamp, cen, root=REPO, closure_list=None) -> list:
    """Rule 6's drift test on a fresh census `cen` against a shipped stamp: every engine load inside the stamp, every
    census entry still loaded, every solver data open stamped, the static engine half unchanged, and every solver/
    module the read loaded inside the closure or excluded. [] when none drifts."""
    out = []
    eng, listed = set(stamp.get("engine") or ()), set((stamp.get("census") or {}).get("engine") or ())
    out += [f"engine load outside the stamp: {p}" for p in sorted(set(cen["engine"]) - eng)]
    out += [f"census entry no longer loaded: {p}" for p in sorted(listed - set(cen["engine"]))]
    out += [f"solver data outside the stamp: {p}" for p in sorted(set(cen["solver_data"]) - set(stamp.get("solver_data") or ()))]
    st = engine_static(root)
    if st != stamp.get("engine_static"):
        out.append("static engine closure changed")
    out += [f"engine call at load outside the stamp and the static half: {p}" for p in cen.get("called_at_load", ())
            if p not in eng and p not in st["modules"]]                     # 68 n7: expected none
    names = set(closure_list if closure_list is not None else closure(root)) | EXCLUDED
    out += [f"solver module outside the closure: {m}" for m in cen["modules"]
            if m.startswith("solver/") and m.count("/") == 1 and Path(m).stem not in names]
    return out


def check_stamp(stamp, root=REPO, name="?"):
    """Rule 4: the file's stamp against this tree, a TableStop «fall sets» naming the first difference. The loader
    re-hashes the stamped files (it does not re-run the sweep; the drift test does). Packages are reported, never
    compared."""
    root = Path(root)
    have = closure(root)
    want = stamp.get("solver") or {}
    if sorted(want) != have:
        raise _stop(f"fall-set file {name}: the read's solver closure changed (stamped {sorted(set(want) - set(have))} "
                    f"gone, {sorted(set(have) - set(want))} new); rebuild the sets on this read")
    for m, b in want.items():
        if blob(root / "solver" / f"{m}.py") != b:
            raise _stop(f"fall-set file {name} was built on solver/{m}.py blob {b}, not this tree's; rebuild")
    st = engine_static(root)
    if st != stamp.get("engine_static"):
        raise _stop(f"fall-set file {name}: the static engine closure changed; rebuild the sets on this read")
    for part in ("engine", "solver_data"):
        for p, b in (stamp.get(part) or {}).items():
            f = root / p
            if not f.exists() or blob(f) != b:
                raise _stop(f"fall-set file {name} was built on {p} blob {b}, not this tree's "
                            f"{blob(f) if f.exists() else 'absent'}; rebuild")
    if stamp.get("switches") != _switches():
        raise _stop(f"fall-set file {name} was built with engine switches {stamp.get('switches')!r}, not this "
                    f"process's {_switches()!r}")


# ── files ─────────────────────────────────────────────────────────────────────────────────────────────────────
def directory() -> Path:
    d = _ma().FALL_SETS_DIR
    return Path(d) if d else DEFAULT_DIR


def find(d: Path, rid):
    for name in (f"{rid}.json.gz", f"{rid}.json"):
        if (Path(d) / name).is_file():
            return Path(d) / name
    return None


def _read(path: Path) -> dict:
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.name.endswith(".gz") else raw)


def parse_sets(d) -> dict:
    """{T node index: [(a′, b′), …]} from a full or compact file's «sets»."""
    return {int(k): [tuple(iv) for iv in v] for k, v in d["sets"].items()}


def build_tree(root=REPO) -> dict:
    """The tree a build ran on (68 B2): the solver closure's blobs, the static engine half and the engine switches —
    tree_stamp without a census (the census is the export's). rho_fall_build writes it into its document's stamp."""
    st = tree_stamp({"engine": {}, "solver_data": {}}, root)
    return {k: st[k] for k in ("solver", "engine", "engine_static", "switches")}


def export(full: Path, out_dir: Path, stamp: dict, stale_test_only=False) -> Path:
    """The compact shipped file from a full build file: record, ps, ts, stamp, sets, stops, gzip -n with sorted keys
    (byte-stable). The build's own stamp fields (record and yaml sha256, tool blobs, read_blob, build_tree) are kept
    under «build»; `stamp` is the tree's closure stamp (closure_stamp), written as «read_closure».
    68 B2: the export refuses unless the build's `build_tree` equals this tree's: an old build never gets a fresh
    stamp. `stale_test_only` lets a test (or the Mac's stand-in sets) export an old build, and is refused for
    DEFAULT_DIR, so such a file can never become the shipped one."""
    d = _read(Path(full))
    if d.get("stops"):
        raise _stop(f"build {Path(full).name} carries {len(d['stops'])} STOP(s): no shipped sets")
    b = d.get("stamp") or {}
    if stale_test_only:
        if Path(out_dir).resolve() == DEFAULT_DIR.resolve():
            raise _stop("a stale-allowed export never writes the shipped directory")
    elif b.get("build_tree") != build_tree():
        raise _stop(f"build {Path(full).name} ran on another tree than this one "
                    f"({'no build_tree in its stamp' if 'build_tree' not in b else 'build_tree differs'}): rebuild here")
    doc = {"record": d["record"], "ps": d["ps"], "ts": d["ts"], "sets": d["sets"], "stops": [],
           "stamp": {"record_sha256": b.get("record_sha256"), "record_yaml_sha256": b.get("record_yaml_sha256"),
                     STAMP_KEY: stamp, "build": b}}
    text = json.dumps(doc, sort_keys=True, separators=(",", ":")).encode()
    out = Path(out_dir) / f"{d['record']}.json.gz"
    out.write_bytes(gzip_stable(text))
    return out


def gzip_stable(text: bytes) -> bytes:
    """gzip -n, the same bytes on every platform: mtime 0, and the header's OS byte (offset 9) set to 255, RFC 1952's
    «unknown». zlib writes its own platform's code there (3 on Linux, 19 on macOS), which made the stage-A block's PC
    export differ from the Mac fixture by that one byte; the deflate stream itself was identical."""
    data = gzip.compress(text, mtime=0)
    return data[:9] + b"\xff" + data[10:]


def _shipped_pin(rid):
    """The table pin (assemblage.sha256) of the shipped record solver/materials/<rid>.yaml, or None."""
    import yaml
    f = SOLVER / "materials" / f"{rid}.yaml"
    if not f.is_file():
        return None
    return ((yaml.safe_load(f.read_text(encoding="utf-8")) or {}).get("assemblage") or {}).get("sha256")


def is_shipped(view) -> bool:
    """A shipped record: its id names solver/materials/<id>.yaml and its table pin is that file's. A record that only
    reuses a shipped id (a test registry's synthetic record in another directory) is not one: the shipped set file
    under that id is another record's, so it neither loads nor refuses there."""
    pin = _shipped_pin(view.material_id)
    return pin is not None and pin == ((view.record or {}).get("assemblage") or {}).get("sha256")


def load(self):
    """AssemblageView._fall_set_load, installed (rule 2). Rules 3 and 4. Only a load that passes every check is cached
    on the view (68 B1): a refusal re-raises on every access, so a caught refusal never leaves the view inert; a
    registry record's file missing with the repair off reads nothing and is not cached either."""
    if self._fall_sets is not None:
        return self._fall_sets
    ma = _ma()
    d = directory()
    path = find(d, self.material_id)
    shipped = is_shipped(self)
    if path is None:
        if shipped:
            if ma.RHO_BRIDGE:
                raise _stop(f"fall sets: no file for {self.material_id} in {d}")
            return {}
        self._fall_sets = {}
        return self._fall_sets
    doc = _read(path)
    if not shipped and (doc.get("stamp") or {}).get("record_sha256") != self.record["assemblage"]["sha256"]:
        self._fall_sets = {}                              # another record's file under a reused id: not this record's
        return self._fall_sets
    if doc.get("record") != self.material_id or doc.get("ps") != list(self.ps) or doc.get("ts") != list(self.ts):
        raise _stop(f"fall-set file {path.name} does not match this record's table")
    if doc.get("stops"):
        raise _stop(f"fall-set file {path.name} carries {len(doc['stops'])} build STOP(s)")
    stamp = doc.get("stamp") or {}
    if stamp.get("record_sha256") != self.record["assemblage"]["sha256"]:
        raise _stop(f"fall-set file {path.name} was built on record sha256 {stamp.get('record_sha256')!r}, not this "
                    f"record's {self.record['assemblage']['sha256']}")
    if stamp.get("record_yaml_sha256") != ma.record_yaml_sha256(self.material_id):
        raise _stop(f"fall-set file {path.name} was built on record yaml sha256 {stamp.get('record_yaml_sha256')!r}, "
                    f"not this record's {ma.record_yaml_sha256(self.material_id)}")
    if STAMP_KEY not in stamp:
        raise _stop(f"fall-set file {path.name} was built on a read_blob stamp; rebuild")
    check_stamp(stamp[STAMP_KEY], REPO, path.name)
    sets = parse_sets(doc)
    self._fall_sets = sets
    return sets


def install(module):
    """Set the loader on the module's AssemblageView (called by solver/__init__.py's hook at the module's end)."""
    module.AssemblageView._fall_set_load = load


def check_record(rec, table):
    """Rule 5, the eager half: at registry load, a registry record's sets load through the installed loader, or the
    TableStop propagates (the registry turns it into material.assemblage_table for that record). With the repair off,
    nothing is read."""
    ma = _ma()
    if not ma.RHO_BRIDGE:
        return
    v = ma.AssemblageView({"id": rec["id"], "assemblage": rec["assemblage"]}, table, 1600.0)
    v._fall_set_load()
