# D2 읽기 변형 시험 실행기 — 등록 §10 의 변형마다 앵커 한 곳을 바꾼 임시 사본에서 지정 시험을 돌려 어느 시험이 잡는지 인쇄, 못 잡거나 앵커가 한 번이 아니면 실패(D2 읽기 등록 §10; 앵커는 조각마다 채움)
"""python3 -B -m solver.landing.d2_read_mutants [--python-wrapper SCRIPT] [ID …]      (D2-read rev 7 §10; from the tree root)

One row per §10 item (the item's text quoted). A row with anchors is applied to a temp copy of the tree (the tracked
files under COPY_DIRS, git-initialised so tools that list tracked files see the same tree), one mutant at a time:
each anchor must occur exactly once in its file (else STOP), the replacement is written, the row's test modules run
under this interpreter, and the failing tests are printed by name. The copy is restored before the next mutant.

Baseline control: each distinct module set is first run unmutated on the copy. A mutant is caught only by tests that
pass there and fail mutated; tests already red at baseline are printed once («baseline red») and never count. A class
or module fixture red at baseline (setUpClass, setUpModule and their tear-downs) masks every test under it, so it is a
STOP, never «caught by nothing» (68 on 337151ac). A mutant whose only new failures are such fixtures is caught by no
named test: printed «caught only by a fixture» and failed (68 n2 on 09e425c9).

--python-wrapper SCRIPT (c8 11-16): each module set runs as `python -B SCRIPT <modules>` instead of `python -B -m
unittest <modules>`, baseline and mutants alike; the script is a named double that ends in unittest.main (e.g. c8's
pinned_double4.py before A1's re-pin). It is printed with its git blob. Without it the run needs nothing. The copy's
git borrows the source repository's objects (objects/info/alternates), so `git rev-parse <commit>:<path>` answers
there as in the tree; the copy's own index and work tree are its own.

A row whose anchors are empty is pending: its slice fills them (S1–S4, or «writer» for ea's side in the artifacts
repo) and it is printed as pending, never as caught.

rc 0 when every applied mutant is caught by at least one test; 1 when any is caught by nothing; 2 on a STOP (an
anchor not found exactly once, an unknown ID). The shape is c8's agree_mutants.py (part2-c8)."""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

COPY_DIRS = ("solver", "engine", "derived", "scripts")
STORE_TEST = "solver.tests.test_d2_store"
REF_TEST = "solver.tests.test_d2_read_reference"
FIXTURES = frozenset({"setUpClass", "setUpModule", "tearDownClass", "tearDownModule"})

# (id, slice, §10 item quoted, [(file, anchor, replacement)], [test modules])
MUTANTS = (
    ("M01", "S2", "precedence reordered (`d2` before `fallback`);", [], []),
    ("M02", "S2", "a `fallback` cell read as `d2`;",
     [("solver/d2_store.py", '    if cls in ("fallback", "limit"):\n        return {"read": "table", "why": cls, "notes": ()}\n    if cls in ("d2", "cut"):\n',
       '    if cls in ("limit",):\n        return {"read": "table", "why": cls, "notes": ()}\n    if cls in ("d2", "cut", "fallback"):\n')],
     [REF_TEST]),
    ("M03a", "view", "a chain link removed (one per link);",
     [("solver/d2_store.py", '    links = (("pins.compact_sha256", pins.get("compact_sha256"), compact_sha256),\n',
       '    links = (\n')], [STORE_TEST]),
    ("M03b", "view", "a chain link removed (one per link);",
     [("solver/d2_store.py", '             ("d2_store.sha256", (record_doc.get("d2_store") or {}).get("sha256"), store_sha256),\n',
       "")], [STORE_TEST]),
    ("M03c", "view", "a chain link removed (one per link);",
     [("solver/d2_store.py", '             ("builder_manifest_blob", strict, h.get("builder_manifest_blob")),\n', "")],
     [STORE_TEST]),
    ("M03d", "view", "a chain link removed (one per link);",
     [("solver/d2_store.py", '             ("record_id", record_doc.get("id"), h.get("record_id")),\n', "")], [STORE_TEST]),
    ("M03e", "view", "a chain link removed (one per link);",
     [("solver/d2_store.py", '             ("table_blob", (compact.get("source") or {}).get("table_blob"), h.get("table_blob")),\n',
       "")], [STORE_TEST]),
    ("M03f", "view", "a chain link removed (one per link);",
     [("solver/d2_store.py",
       '             ("interp_term_blob", interp_term_blob(compact), (h.get("inputs") or {}).get("interp_term_blob")))\n',
       "             )\n")], [STORE_TEST]),
    ("M04", "view", "the closed-key check removed;",
     [("solver/d2_store.py", "    if sorted(doc) != list(TOP_KEYS):\n", "    if False:\n")], [STORE_TEST]),
    ("M05", "S2", "the lower-cell tie switched to upper;",
     [("solver/d2_store.py", "    for i in range(len(xs) - 1):\n        if xs[i] <= x <= xs[i + 1]:",
       "    for i in reversed(range(len(xs) - 1)):\n        if xs[i] <= x <= xs[i + 1]:")],
     [STORE_TEST, REF_TEST]),
    ("M06", "S2", "the subgrid side 1 not reversed;",
     [("solver/d2_store.py", '    rev = s1["A"] != s0["A"]\n', "    rev = False\n")], [REF_TEST]),
    ("M07", "S2", "s_path on subgrid taking the blend's own derivative;",
     [("solver/d2_store.py", '        return ("sliver", v["s"], v["rho"], v["alpha"], v["c_p"])\n',
       '        return ("sliver", v["s"], v["rho"], -v["rho"] * (read_point(doc, p * (1 + 1e-6), t)["values"]["s"]\n'
       '                - read_point(doc, p * (1 - 1e-6), t)["values"]["s"]) / (2e-6 * p), v["c_p"])\n')],
     [STORE_TEST]),                       # the blend's own ∂s/∂P for α; the Q8 test holds the ruled ≤ 8 ulp (note 7 (1))
    ("M08", "S1", "d2_read off opening the store;",
     [("solver/d2_store.py", '    state, rel = check_keys(record_doc)\n    if state == "off":\n        return None\n',
       '    state, rel = check_keys(record_doc)\n    if state == "off":\n'
       '        [q.read_bytes() for q in sorted((Path(materials_dir) / "fields").glob("*"))]\n        return None\n')],
     [STORE_TEST]),                       # the planted unreadable store under fields/ (68 B4) raises when opened
    ("M09", "S1", "global off × eligible routed to D2;",
     [("solver/solve.py", "    if registry is not None and silicate:             # silicate registration §4",
       "    if registry is not None:             # silicate registration §4")],
     [STORE_TEST]),                       # the route itself; test_global_off_never_asks_for_a_store (Earth, 68 n4)
    ("M10a", "S3", "the table-regardless mode on by default, or ignored by the dispatch, or with its note dropped;",
     [("solver/material_assemblage.py", "def view(record, table, t_pot, p_stop=0.0, p_floor=0.0, handover=None, store=None, *, table_regardless=None):",
       "def view(record, table, t_pot, p_stop=0.0, p_floor=0.0, handover=None, store=None, *, table_regardless=\"on\"):")],
     [STORE_TEST]),                       # on by default
    ("M10b", "S3", "the table-regardless mode on by default, or ignored by the dispatch, or with its note dropped;",
     [("solver/material_assemblage.py", "self._d2 = None if (table_regardless or store is None) else",
       "self._d2 = None if (store is None) else")],
     [STORE_TEST]),                       # ignored by the dispatch
    ("M10c", "S3", "the table-regardless mode on by default, or ignored by the dispatch, or with its note dropped;",
     [("solver/material_assemblage.py", '''                self.notes.append(mv.DeclaredNote(self.material_id, PHASE_ID,
                                                  f"table-regardless read: {self.table_regardless}"))
''', "")],
     [STORE_TEST]),                       # the note dropped
    ("M11", "S1", "a `boundaries` reader left on the table's block (fall_sets' extension rows in particular);",
     [("solver/fall_sets.py", 'ma.boundary_block(None, table, getattr(v, "store", None), "position")',
       'ma.boundary_block(None, table, None, "position")')],
     [STORE_TEST]),
    ("M12", "view", "a v1 store accepted for positions;",
     [("solver/d2_store.py", '    if c.get("name") == CONTRACT_NAME and c.get("version") == 1:\n',
       "    if False:\n"),
      ("solver/d2_store.py", '    if c.get("name") != CONTRACT_NAME or c.get("version") != 2:\n',
       '    if c.get("name") != CONTRACT_NAME or c.get("version") not in (1, 2):\n')], [STORE_TEST]),
    ("M13", "view", "a «today» row through a `d2` cell accepted;",
     [("solver/d2_store.py", '                if cell["class"] in ("d2", "cut"):\n',
       '                if cell["class"] in ("cut",):\n')], [STORE_TEST]),
    ("M14", "view", "a swap taking a traced P_b;",
     [("solver/d2_store.py", "        point = kind in (\"accepted\", \"unmatched\")\n",
       "        point = kind in (\"accepted\", \"unmatched\", \"swap\")\n")], [STORE_TEST]),
    ("M15", "view", "`material.d2_store_coincident` removed: a fixture store whose coincident group took two different "
                    "points must be refused (rev 5);",
     [("solver/d2_store.py", "    if a != b:\n        diff = sorted(set(a) ^ set(b))[:3]\n",
       "    if False:\n        diff = sorted(set(a) ^ set(b))[:3]\n")], [STORE_TEST]),
    ("M16", "view", "`material.d2_store_edges_rows` loosened to compare `p_b` only: a fixture store with a changed "
                    "`delta_rho` must be refused;",
     [("solver/d2_store.py", '    return {k: v for k, v in d.items() if k not in NEW_KEYS and k != "p_b"}\n',
       "    return {}\n")], [STORE_TEST]),
    ("M17", "view", "the «traced» interval made inclusive: a fixture store with a traced p_b equal to p_lo must be "
                    "refused.",
     [("solver/d2_store.py", '            if not (ma._finite(pb) and r["p_lo"] < pb < r["p_hi"]):\n',
       '            if not (ma._finite(pb) and r["p_lo"] <= pb <= r["p_hi"]):\n')], [STORE_TEST]),
    ("M18", "writer", "rule 5/6 taking the first point in file order instead of the nearest", [], []),
    ("M19", "writer", "rule 4 removed must fail a fixture coincident group with each edge covered by its own point.",
     [], []),
)


class Stop(Exception):
    pass


def copy_tree(root, dest, dirs=COPY_DIRS):
    """the tracked files under `dirs`, from the working tree, into a git-initialised `dest`"""
    out = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--", *dirs], capture_output=True, check=True)
    names = [n for n in out.stdout.decode().split("\0") if n and (Path(root) / n).is_file()]
    for n in names:
        (dest / n).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(Path(root) / n, dest / n)
    subprocess.run(["git", "-C", str(dest), "init", "-q"], check=True)
    src = subprocess.run(["git", "-C", str(root), "rev-parse", "--path-format=absolute", "--git-common-dir"],
                         capture_output=True, text=True, check=True).stdout.strip()
    (dest / ".git/objects/info/alternates").write_text(str(Path(src) / "objects") + "\n")
    for i in range(0, len(names), 500):
        subprocess.run(["git", "-C", str(dest), "add", "--", *names[i:i + 500]], check=True)


def apply(work, edits):
    """write each edit into `work`; return {file: original text}; Stop unless every anchor occurs exactly once"""
    saved = {}
    for f, a, b in edits:
        p = work / f
        text = p.read_text(encoding="utf-8")
        n = text.count(a)
        if n != 1:
            raise Stop(f"anchor in {f} found {n} times: {a[:80]!r}")
        saved.setdefault(f, text)
        p.write_text(text.replace(a, b), encoding="utf-8")
    return saved


def run_tests(work, modules, py=sys.executable, wrapper=None):
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    cmd = [py, "-B", str(wrapper), *modules] if wrapper else [py, "-B", "-m", "unittest", *modules]
    r = subprocess.run(cmd, cwd=work, capture_output=True, text=True, env=env)
    failed = sorted(set(re.findall(r"^(?:FAIL|ERROR): (\w+)", r.stderr, re.M)))
    return r.returncode, failed


def _blob(path):
    import hashlib
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main(argv, root=".", mutants=MUTANTS, out=print):
    argv, wrapper = list(argv), None
    if "--python-wrapper" in argv:
        i = argv.index("--python-wrapper")
        if i + 1 >= len(argv) or not Path(argv[i + 1]).is_file():
            out("STOP: --python-wrapper needs an existing script")
            return 2
        wrapper = Path(argv[i + 1]).resolve()
        del argv[i:i + 2]
        out(f"launcher: python -B {wrapper} (blob {_blob(wrapper)[:8]})")
    ids = {m[0] for m in mutants}
    unknown = [a for a in argv if a not in ids]
    if unknown:
        out(f"STOP: unknown mutant id(s) {unknown}")
        return 2
    chosen = [m for m in mutants if not argv or m[0] in argv]
    caught = missed = pending = 0
    with tempfile.TemporaryDirectory(prefix="d2-mutants-") as tmp:
        work = Path(tmp)
        copy_tree(Path(root), work)
        base = {}
        for mods in sorted({tuple(m[4]) for m in chosen if m[3]}):
            base[mods] = set(run_tests(work, list(mods), wrapper=wrapper)[1])
            out(f"baseline {' '.join(mods)}: " + (f"red {', '.join(sorted(base[mods]))}" if base[mods] else "green"))
            masked = sorted(base[mods] & FIXTURES)
            if masked:
                out(f"STOP: baseline {' '.join(mods)}: {', '.join(masked)} red, which masks every test under it")
                return 2
        for mid, slice_, item, edits, modules in chosen:
            if not edits:
                pending += 1
                out(f"{mid} pending ({slice_}): {item}")
                continue
            try:
                saved = apply(work, edits)
            except Stop as e:
                out(f"STOP: {mid}: {e}")
                return 2
            try:
                rc, failed = run_tests(work, modules, wrapper=wrapper)
            finally:
                for f, text in saved.items():
                    (work / f).write_text(text, encoding="utf-8")
            new = [t for t in failed if t not in base[tuple(modules)]]
            named = [t for t in new if t not in FIXTURES]
            if named:
                caught += 1
                out(f"{mid} ({slice_}): rc {rc} · caught by {', '.join(named)} — {item}")
            elif new:
                missed += 1
                out(f"{mid} ({slice_}): rc {rc} · caught only by a fixture: {', '.join(new)} — {item}")
            else:
                missed += 1
                out(f"{mid} ({slice_}): rc {rc} · caught by NOTHING — {item}")
    out(f"d2-read mutants: {caught} caught, {missed} caught by nothing, {pending} pending — "
        f"{'PASS' if not missed else 'FAIL'}")
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
