# D2 읽기 독자 조사 도구 — 엔진 저장소의 .py 를 ast 로 훑어 silicate_records·d2_read 키·view 생성·_solid/s_path·boundaries·boundary_block(use)·table_regardless 자리를 한 줄씩 적고 종류별 규칙을 검사(D2 읽기 등록 §7)
"""python3 -B -m solver.landing.d2_read_census [write|check]      (D2-read rev 7 §7; run from the engine tree root)

Walks every `.py` git tracks in the engine repo (`git ls-files '*.py'`), outside `solver/tests/` and the tool's own
test, with `ast`. Writes solver/landing/d2_read_census.json:
{"sites": [{path, line, kind, function, use}, …], "schema_keys": [...]}, one site per row, sorted by (path, line, kind,
function, use). `function` is the enclosing function's qualified name (classes and functions joined by «.»), or «<module>».
`schema_keys` are the record keys of solver/materials/schema.yaml (its `record:` mapping), sorted.

Kinds (§7):
- `option`: a read or pass of `silicate_records`, or a `requires_switch` read: a name, an attribute, a parameter or a
  keyword argument so named, or the string as a subscript, a `.get` / `.pop` / `.setdefault` key or a comparison operand;
- `record_key`: a subscript or `.get` of `d2_read`, `d2_read_basis` or `d2_store`;
- `view`: a call of `material_assemblage.view` (through any import alias, or bare `view` inside material_assemblage
  itself) or of `AssemblageView(`;
- `solid`: an attribute call `._solid(` or `.s_path(`;
- `boundaries`: a subscript or `.get` of "boundaries";
- `table_regardless`: a keyword `table_regardless=` at a call;
- `switch` (c8, 11-16, extending S0's keys with §5b's «the census checks each site's `use`»): a call of
  `material_assemblage.boundary_block` (through any import alias, or bare inside material_assemblage), with its `use`
  (the fourth argument or `use=`) when that is a string literal, else None. `use` is None on every other kind.

`write` writes the JSON; `check` (the default) regenerates it, compares with the committed file and applies each kind's
rule (`violations`); it prints every difference and every violation and exits 1 on any, else 0."""
import ast
import json
import subprocess
import sys
from pathlib import Path
from types import MappingProxyType

SITE_KEYS = ("path", "line", "kind", "function", "use")
KINDS = ("option", "record_key", "view", "solid", "boundaries", "table_regardless", "switch")
OUT = "solver/landing/d2_read_census.json"
TOP_KEYS = ("sites", "schema_keys")

SCHEMA = "solver/materials/schema.yaml"
OWN_TEST = "solver/landing/test_d2_read_census.py"
EXCLUDED_DIRS = ("solver/tests/",)
MA_MODULE = "material_assemblage"
MA_PATH = "solver/material_assemblage.py"

OPTION_NAMES = frozenset({"silicate_records", "requires_switch"})
RECORD_KEYS = frozenset({"d2_read", "d2_read_basis", "d2_store"})
SOLID_ATTRS = frozenset({"_solid", "s_path"})
GET_LIKE = frozenset({"get", "pop", "setdefault"})

# Each kind's rule (§7 «Each kind has its rule»), as (path, function) allow-lists. The read piece fills them as it
# routes (S1–S3); a site outside its list is a violation, so a new reader cannot land unlisted.
_REASONS = MappingProxyType({
    # boundaries: raw reads of a `boundaries` block that stay off the switch, each with its reason (68 n2 on 54dd5042)
    ("boundaries", MA_PATH, "boundary_block"): "the switch itself",
    # a field record's own phase-boundary list (kind «field»), not an assemblage compact's block: outside §7's
    # boundaries rule, which is about the compact's block and its switch (c8 at S4; for 68's reading)
    ("boundaries", "solver/material_checks.py", "view_record_fns.curve"): "a field record's phase-boundary list",
    ("boundaries", "solver/material_registry.py", "_curve_ends"): "a field record's phase-boundary list",
    ("boundaries", "solver/material_registry.py", "_curves"): "a field record's phase-boundary list",
    ("boundaries", "solver/material_registry.py", "_field_record"): "a field record's phase-boundary list",
    ("boundaries", "solver/material_registry.py", "_kind"): "a field record's phase-boundary list",
    ("boundaries", "solver/material_registry.py", "triple_point_misses"): "a field record's phase-boundary list",
    ("boundaries", "solver/material_view.py", "RecordView.__init__"): "a field record's phase-boundary list",
    # record_key: the loader (§7 «every record_key site is in the loader»)
    ("record_key", "solver/d2_store.py", "state_of"): "the loader",
    ("record_key", "solver/d2_store.py", "check_keys"): "the loader (68 B1, B2 on 54dd5042)",
    ("record_key", "solver/d2_store.py", "chain"): "the loader's chain link (the record's pin against the store)",
    ("record_key", "solver/d2_store.py", "arbitration"): "the loader's chain link 7 (D2-read note 10 §2)",
    # view: the direct view builders, each correct as it is (§5a «Direct view builders that do not pass the argument
    # are listed and are correct as they are»)
    ("view", "solver/solve.py", "_assemblage_view"): "the solve route: passes the store only on silicate_records (§4)",
    ("view", MA_PATH, "view"): "the builder itself",
    ("view", "solver/fall_sets.py", "_sweep"): "the fall-set sweep: passes the registry's store on a D2 record (S1)",
    ("view", "solver/fall_sets.py", "check_record"): "the fall-set stamp check: a view of the table only, no read",
    ("view", "solver/rho_fall_build.py", "_view"): "the fall-set build's views: unrouted, disclosed (68 n on "
                                                   "96a9ec57; E1's owner question)",
    ("view", MA_PATH, "check_table"): "the compact's own validation at load: table reads only",
    ("view", MA_PATH, "boundary_disclosures"): "the compact's boundaries report: table reads only",
    ("view", MA_PATH, "s_monotone_build"): "the s-monotone build over the table: table reads only",
    ("view", "solver/d2_store.py", "check_edges"): "the store's load check over the compact's view (§5b)",
})
_allow = lambda kind: frozenset((p, fn) for (k, p, fn) in _REASONS if k == kind)  # noqa: E731
BOUNDARIES_ALLOW = _allow("boundaries")
RECORD_KEY_ALLOW = _allow("record_key")
VIEW_ALLOW = _allow("view")
TABLE_REGARDLESS_ALLOW = frozenset()                          # §5a: zero sites in the walk (the mode's own tests are
                                                              # under solver/tests/; the one real setter is in artifacts)
#: §5b's table, one entry per routed reader, {(path, function): frozenset({use, …})}; a non-literal use always fails
SWITCH_USES = MappingProxyType({
    ("solver/coexist.py", "check_table"): frozenset({"read"}),
    ("solver/coexist.py", "cut_census"): frozenset({"read"}),
    (MA_PATH, "AssemblageView.__init__"): frozenset({"read", "position"}),
    ("solver/rho_fall_build.py", "_edge_tol"): frozenset({"position"}),
    ("solver/solve.py", "_assemblage_view"): frozenset({"read"}),
    ("solver/fall_sets.py", "_region_points"): frozenset({"position"}),
    # the compact's own checks and report read the compact's block through the switch (§7: check_boundaries' callers
    # go through it; S4 routed boundary_disclosures and d2_store.check_edges' compact read the same way)
    (MA_PATH, "check_table"): frozenset({"read"}),
    (MA_PATH, "check_boundaries"): frozenset({"read"}),
    (MA_PATH, "boundary_disclosures"): frozenset({"read"}),
    ("solver/d2_store.py", "check_edges"): frozenset({"read"}),
})


def py_files(root):
    """repo-relative posix paths of the .py files git tracks, minus the exclusions"""
    out = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--", "*.py"],
                         capture_output=True, check=True).stdout.decode()
    paths = sorted({p for p in out.split("\0") if p})
    return [p for p in paths
            if not p.startswith(EXCLUDED_DIRS) and p != OWN_TEST and (Path(root) / p).is_file()]


def _const_str(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


class _Walker(ast.NodeVisitor):
    def __init__(self, path, getters=frozenset()):
        self.path = path
        self.stack = []
        self.getters = set(getters)      # this file's functions that return the material_assemblage module (_ma())
        self.ma_aliases = {"<material_assemblage>"}   # names bound to the material_assemblage module (and a getter call)
        self.view_names = set()          # names bound to material_assemblage.view
        self.switch_names = set()        # names bound to material_assemblage.boundary_block
        if path == MA_PATH:
            self.view_names.add("view")
            self.switch_names.add("boundary_block")
        self.sites = set()

    def add(self, node, kind, use=None):
        self.sites.add((self.path, node.lineno, kind, ".".join(self.stack) or "<module>", use))

    # scopes
    def _scoped(self, node):
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    visit_FunctionDef = visit_AsyncFunctionDef = visit_ClassDef = _scoped

    # imports: track material_assemblage and its view
    def visit_Import(self, node):
        for a in node.names:
            if a.name.split(".")[-1] == MA_MODULE:
                self.ma_aliases.add(a.asname or a.name)    # «import solver.material_assemblage» binds the dotted name
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        mod = (node.module or "").split(".")[-1]
        for a in node.names:
            if a.name == MA_MODULE:
                self.ma_aliases.add(a.asname or a.name)
            elif mod == MA_MODULE and a.name == "view":
                self.view_names.add(a.asname or a.name)
            elif mod == MA_MODULE and a.name == "boundary_block":
                self.switch_names.add(a.asname or a.name)
        self.generic_visit(node)

    # names, attributes, parameters
    def visit_Name(self, node):
        if node.id in OPTION_NAMES:
            self.add(node, "option")

    def visit_Attribute(self, node):
        if node.attr in OPTION_NAMES:
            self.add(node, "option")
        self.generic_visit(node)

    def visit_arg(self, node):
        if node.arg in OPTION_NAMES:
            self.add(node, "option")
        self.generic_visit(node)

    def _key(self, node, key):
        if key in OPTION_NAMES:
            self.add(node, "option")
        if key in RECORD_KEYS:
            self.add(node, "record_key")
        if key == "boundaries":
            self.add(node, "boundaries")

    def visit_Subscript(self, node):
        self._key(node, _const_str(node.slice))
        self.generic_visit(node)

    def visit_Compare(self, node):
        for operand in [node.left, *node.comparators]:
            if _const_str(operand) in OPTION_NAMES:
                self.add(node, "option")
        self.generic_visit(node)

    def visit_Assign(self, node):
        # «ma = _ma()»: a name bound to a getter's answer is the module (c8 at S4: fall_sets' and rho_fall_build's
        # _ma() aliases hid fall_sets' boundary_block and view calls)
        if self._getter_call(node.value):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    self.ma_aliases.add(t.id)
        self.generic_visit(node)

    def _getter_call(self, node):
        return isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in self.getters

    def _dotted(self, node):
        if self._getter_call(node):                  # «_ma().view(...)»: the getter's answer is the module
            return "<material_assemblage>"
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            head = self._dotted(node.value)
            return None if head is None else f"{head}.{node.attr}"
        return None

    def visit_Call(self, node):
        f = node.func
        if isinstance(f, ast.Attribute):
            if f.attr in GET_LIKE and node.args:
                self._key(node, _const_str(node.args[0]))
            if f.attr in SOLID_ATTRS:
                self.add(node, "solid")
            if f.attr == "view" and self._dotted(f.value) in self.ma_aliases:
                self.add(node, "view")
            if f.attr == "AssemblageView":
                self.add(node, "view")
            if f.attr == "boundary_block" and self._dotted(f.value) in self.ma_aliases:
                self._switch(node)
        elif isinstance(f, ast.Name):
            if f.id in self.view_names or f.id == "AssemblageView":
                self.add(node, "view")
            if f.id in self.switch_names:
                self._switch(node)
        for kw in node.keywords:
            if kw.arg in OPTION_NAMES:
                self.add(kw.value, "option")
            if kw.arg == "table_regardless":
                self.add(kw.value, "table_regardless")
        self.generic_visit(node)


    def _switch(self, node):
        use = [kw.value for kw in node.keywords if kw.arg == "use"] or node.args[3:4]
        self.add(node, "switch", _const_str(use[0]) if use else None)


def ma_getters(tree):
    """the module-level functions of a file that hand back the material_assemblage module: a body that names the module
    (an import of it, or its dotted name as a string, as fall_sets' sys.modules / __import__ lookup) and returns"""
    out = set()
    for fn in tree.body:
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        names = any((isinstance(n, ast.ImportFrom) and any(a.name == MA_MODULE for a in n.names))
                    or (isinstance(n, ast.Import) and any(a.name.split(".")[-1] == MA_MODULE for a in n.names))
                    or (_const_str(n) or "").split(".")[-1] == MA_MODULE for n in ast.walk(fn))
        if names and any(isinstance(n, ast.Return) and n.value is not None for n in ast.walk(fn)):
            out.add(fn.name)
    return out


def sites_of(path, source):
    """the census rows of one file's source text, as tuples (path, line, kind, function, use)"""
    tree = ast.parse(source, filename=path)
    w = _Walker(path, ma_getters(tree))
    w.visit(tree)
    return w.sites


def schema_keys(root):
    import yaml
    return sorted((yaml.safe_load((Path(root) / SCHEMA).read_text(encoding="utf-8")) or {}).get("record") or {})


def census(root):
    root = Path(root)
    rows = set()
    for p in py_files(root):
        rows |= sites_of(p, (root / p).read_text(encoding="utf-8"))
    sites = [dict(zip(SITE_KEYS, r)) for r in sorted(rows, key=lambda r: r[:4] + (r[4] or "",))]
    return {"sites": sites, "schema_keys": schema_keys(root)}


#: §7 «Each kind has its rule» on the real tree (68 B2 on e59a6739; directing 11-16: routed, or named as the finding):
#: the (kind, path, function) of every site outside its allow-list before the read piece routes it. The real tree must
#: equal this list exactly: a new unrouted site fails, and a routed one must leave the list (it only shrinks). Empty at
#: the final pass, when the real-tree test's expectedFailure marker goes.
UNROUTED_KNOWN = frozenset()                                 # S4 (c8): every site routed or listed with its reason

RULES = (
    ("boundaries", BOUNDARIES_ALLOW, "a boundaries read outside boundary_block and the switch's allow-list (§7, §5b)"),
    ("record_key", RECORD_KEY_ALLOW, "a d2_read / d2_read_basis / d2_store key read outside the loader (§7)"),
    ("view", VIEW_ALLOW, "a direct view builder not in the list (§7)"),
    ("table_regardless", TABLE_REGARDLESS_ALLOW, "a table_regardless= site outside the mode's own tests (§5a, §7)"),
)


SWITCH_TEXT = "a boundary_block call whose use is not a literal in §5b's table for its reader (§5b, §7)"


def violations(data, rules=RULES, switch_uses=None):
    """[(rule text, site)] for every site outside its kind's allow-list, and every switch site whose `use` is not a
    literal listed for its (path, function)"""
    switch_uses = SWITCH_USES if switch_uses is None else switch_uses
    out = []
    for kind, allow, text in rules:
        for s in data["sites"]:
            if s["kind"] == kind and (s["path"], s["function"]) not in allow:
                out.append((text, s))
    for s in data["sites"]:
        if s["kind"] == "switch" and (s["use"] is None or s["use"] not in switch_uses.get((s["path"], s["function"]), ())):
            out.append((SWITCH_TEXT, s))
    return out


def dump(data):
    return json.dumps(data, indent=1, sort_keys=False, ensure_ascii=False) + "\n"


def diff(committed, regenerated):
    """the site rows and schema keys in one and not the other, as printable lines"""
    lines = []
    for key in TOP_KEYS:
        a = {json.dumps(x, sort_keys=True) for x in committed.get(key, [])}
        b = {json.dumps(x, sort_keys=True) for x in regenerated.get(key, [])}
        lines += [f"- {key}: {x}" for x in sorted(a - b)] + [f"+ {key}: {x}" for x in sorted(b - a)]
    if list(committed) != list(TOP_KEYS):
        lines.append(f"top keys {list(committed)} ≠ {list(TOP_KEYS)}")
    return lines


def main(argv, root="."):
    mode = argv[0] if argv else "check"
    if mode not in ("write", "check") or len(argv) > 1:
        print(__doc__)
        return 2
    data = census(root)
    out = Path(root) / OUT
    if mode == "write":
        out.write_text(dump(data), encoding="utf-8")
        print(f"census: {len(data['sites'])} sites, {len(data['schema_keys'])} schema keys → {OUT}")
        return 0
    bad = []
    if not out.is_file():
        bad.append(f"no committed {OUT}")
    else:
        bad += [f"regenerated ≠ committed: {ln}" for ln in diff(json.loads(out.read_text(encoding="utf-8")), data)]
    bad += [f"{text}: {s['path']}:{s['line']} {s['function']}" + (f" use={s['use']!r}" if s["kind"] == "switch" else "")
            for text, s in violations(data)]
    for ln in bad:
        print(ln)
    print(f"census check: {'PASS' if not bad else 'FAIL'} — {len(data['sites'])} sites, {len(bad)} finding(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
