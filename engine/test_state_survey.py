# 상태 조사 동결 시험(ES-f6 (a) §4.6) — 모듈 상태가 바뀌는 모든 꼴의 조사 결과가 동결 요약 줄과 꼴마다의 동결 목록(줄 번호 없이)과 같은지, 심은 새 자리와 같은 꼴 안의 바꿔치기가 빨갛게 잡히는지
"""ES-f6 (a) frozen §3 and §4.6 (artifacts pc/ea-esf6/prereg-a.frozen.md, blob 2ceec161). The survey is the frozen
registration's `state_survey.py` (blob 7117cb5d) made a function here: it reads engine source by AST or text only and
never imports an engine module. Its SUMMARY line must equal the registration's quoted line; each blind-spot row's hit list, keyed by file,
enclosing def and source phrase (no line numbers), must equal FROZEN_LISTS (r2 B1 on db4eab30); one planted hit per
row that can have one must raise that row's count, and a same-row swap (counts kept) must turn its list red."""
import ast
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FROZEN = ("SUMMARY census 76 (counter 31, flag 12, memo 30, start 3) · setattr 2 · other_module_attr 21 · class_attr 0 · "
          "object_attr 0 · contextvars 1 · mutable_default 0 · c_extension 0 · functools_cache 0 · imported_name 4 · "
          "closure_cells 9 · instance_state 30 (method, attribute) pairs in 5 classes (BodyState, LayerGrid, LidGrid, "
          "Table, Trace)")
fails = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        fails.append(name)


def survey(ENG):
    # Rule (directing 11-03): this survey reads engine source by AST or text only and never imports an engine module (some run
    # code at import). The census's own `mutated_names` is taken from test_process_state.py's source (its METHODS, _root and
    # mutated_names definitions, executed alone), and REGISTRY's keys and kinds from process_state.py's AST.
    _tsrc = ast.parse((ENG / "test_process_state.py").read_text())
    _keep = [n for n in _tsrc.body if (isinstance(n, ast.FunctionDef) and n.name in ("_root", "mutated_names"))
             or (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "METHODS" for t in n.targets))]
    _ns = {"ast": ast}
    exec(compile(ast.fix_missing_locations(ast.Module(body=_keep, type_ignores=[])), "test_process_state.py (definitions only)",
                 "exec"), _ns)


    class _TP:
        mutated_names = staticmethod(_ns["mutated_names"])


    tp = _TP()
    _kinds = {"START": "start", "MEMO": "memo", "COUNTER": "counter", "FLAG": "flag"}
    _reg = {}
    for n in ast.parse((ENG / "process_state.py").read_text()).body:
        tgt = n.target if isinstance(n, ast.AnnAssign) else (n.targets[0] if isinstance(n, ast.Assign) else None)
        if isinstance(tgt, ast.Name) and tgt.id == "REGISTRY" and isinstance(n.value, ast.Dict):
            for k, v in zip(n.value.keys, n.value.values):
                _reg[tuple(e.value for e in k.elts)] = (_kinds[v.elts[0].id],)


    class _PS:
        REGISTRY = _reg


    ps = _PS()

    files = sorted(p for p in ENG.glob("*.py") if not p.name.startswith("test_"))
    mods = {p.stem for p in ENG.glob("*.py")}
    METH = {"update", "setdefault", "pop", "popitem", "clear", "append", "extend", "insert", "remove", "add", "discard"}
    rows = {k: [] for k in ("census", "setattr", "other_module_attr", "class_attr", "object_attr", "contextvars",
                            "mutable_default", "c_extension", "functools_cache", "imported_name", "instance_state",
                            "closure_cells")}
    for p in files:
        src = p.read_text()
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        for n in sorted(tp.mutated_names(src)):
            rows["census"].append([p.stem, n, ps.REGISTRY.get((p.stem, n), ("UNLISTED",))[0]])
        for m in re.finditer(r"\bsetattr\(", src):
            rows["setattr"].append(f"{p.name}:{src.count(chr(10), 0, m.start()) + 1}")
        for m in re.finditer(r"ContextVar\(", src):
            rows["contextvars"].append(f"{p.name}:{src.count(chr(10), 0, m.start()) + 1}")
        for m in re.finditer(r"\bnp\.random\.|\brandom\.(seed|random|uniform|choice|shuffle)\(|numba\.|@njit|@jit", src):
            rows["c_extension"].append(f"{p.name}:{src.count(chr(10), 0, m.start()) + 1} {m.group(0)}")
        for m in re.finditer(r"lru_cache|functools\.cache|@cache\b", src):
            rows["functools_cache"].append(f"{p.name}:{src.count(chr(10), 0, m.start()) + 1}")
        top_names, classes = set(), set()
        for n in tree.body:
            if isinstance(n, ast.ClassDef):
                classes.add(n.name)
            elif isinstance(n, (ast.Assign, ast.AnnAssign)):
                for t in (n.targets if isinstance(n, ast.Assign) else [n.target]):
                    if isinstance(t, ast.Name):
                        top_names.add(t.id)
        alias = {}                                 # local name → engine module (import M / import M as A / from M import X)
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                for a in n.names:
                    alias[a.asname or a.name.split(".")[0]] = a.name.split(".")[0]
            elif isinstance(n, ast.ImportFrom):
                for a in n.names:
                    alias[a.asname or a.name] = a.name if n.module is None else (a.name if a.name in mods else n.module)
        imported = set(alias)
        for fn in ast.walk(tree):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for d in fn.args.defaults + fn.args.kw_defaults:
                if isinstance(d, (ast.List, ast.Dict, ast.Set)):
                    rows["mutable_default"].append(f"{p.name}:{fn.lineno} {fn.name}")
            for n in ast.walk(fn):
                tgts = []
                if isinstance(n, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                    tgts = n.targets if isinstance(n, ast.Assign) else [n.target]
                elif isinstance(n, ast.Delete):
                    tgts = n.targets
                elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in METH:
                    tgts = [n.func.value]
                for t in tgts:
                    node = t
                    while isinstance(node, ast.Subscript):
                        node = node.value
                    if not (isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name)):
                        continue
                    base = node.value.id
                    where = f"{p.name}:{n.lineno} {base}.{node.attr}"
                    real = alias.get(base)
                    if real in mods and real != p.stem:
                        if where + f" ({real})" not in rows["other_module_attr"]:
                            rows["other_module_attr"].append(where + f" ({real})")
                    elif (base in classes or base == "cls") and where not in rows["class_attr"]:
                        rows["class_attr"].append(where)
                    elif base in top_names and base not in imported and where not in rows["object_attr"]:
                        rows["object_attr"].append(where)
        from_imp = {}
        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom) and n.module in mods and n.module != p.stem:
                for a in n.names:
                    from_imp[a.asname or a.name] = f"{n.module}.{a.name}"
        for fn in ast.walk(tree):
            if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for n in ast.walk(fn):
                    tgts = []
                    if isinstance(n, (ast.Assign, ast.AugAssign)):
                        tgts = n.targets if isinstance(n, ast.Assign) else [n.target]
                    elif isinstance(n, ast.Delete):
                        tgts = n.targets
                    elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in METH:
                        tgts = [n.func.value]
                    for t in tgts:
                        node, sub = t, False
                        while isinstance(node, ast.Subscript):
                            node, sub = node.value, True
                        if isinstance(node, ast.Name) and node.id in from_imp and (sub or t is not node or isinstance(n, ast.Call)):
                            w = f"{p.name}:{n.lineno} {node.id} ({from_imp[node.id]})"
                            if w not in rows["imported_name"]:
                                rows["imported_name"].append(w)
        for cl in ast.walk(tree):
            if not isinstance(cl, ast.ClassDef):
                continue
            for fn in cl.body:
                if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) or fn.name in ("__init__", "__post_init__"):
                    continue
                for n in ast.walk(fn):
                    tgts = []
                    if isinstance(n, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                        tgts = n.targets if isinstance(n, ast.Assign) else [n.target]
                    elif isinstance(n, ast.Delete):
                        tgts = n.targets
                    elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in METH:
                        tgts = [n.func.value]
                    for t in tgts:
                        node = t
                        while isinstance(node, ast.Subscript):
                            node = node.value
                        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "self":
                            w = f"{p.name} {cl.name}.{fn.name} self.{node.attr}"
                            if w not in rows["instance_state"]:
                                rows["instance_state"].append(w)
        for n in ast.walk(tree):
            if isinstance(n, ast.Nonlocal):
                rows["closure_cells"].append(f"{p.name}:{n.lineno} nonlocal {','.join(n.names)}")
    kinds = {}
    for r in rows["census"]:
        kinds[r[2]] = kinds.get(r[2], 0) + 1
    classes = sorted({e.split()[1].split(".")[0] for e in rows["instance_state"]})
    summary = ("SUMMARY " + " · ".join([f"census {len(rows['census'])} ({', '.join(f'{k} {v}' for k, v in sorted(kinds.items()))})"]
          + [f"{k} {len(v)}" for k, v in rows.items() if k not in ("census", "instance_state")]
          + [f"instance_state {len(rows['instance_state'])} (method, attribute) pairs in {len(classes)} classes ({', '.join(classes)})"]))
    return rows, summary


LISTED_ROWS = ("other_module_attr", "setattr", "contextvars", "imported_name", "closure_cells", "instance_state",
               "class_attr", "object_attr", "mutable_default", "functools_cache", "c_extension")


def keyed(rows, ENG):
    """Each blind-spot row's hits without line numbers (r2 B1 on db4eab30): «file · enclosing def · source phrase», the
    phrase being the hit line's stripped text (plus the survey's own tail: the name and the resolved module), so a
    hit is anchored by file and phrase and an edit elsewhere in the file moves nothing. instance_state entries carry
    no line and are kept as they are."""
    encl, lines = {}, {}

    def where(fname, ln):
        if fname not in encl:
            src = (ENG / fname).read_text()
            lines[fname] = src.split("\n")
            spans = []
            for n in ast.walk(ast.parse(src)):
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    spans.append((n.lineno, n.end_lineno, n.name))
            encl[fname] = spans
        inner = [s for s in encl[fname] if s[0] <= ln <= s[1]]
        name = min(inner, key=lambda s: s[1] - s[0])[2] if inner else "<module>"
        return name, re.split(r"\s+#", lines[fname][ln - 1])[0].strip()        # a trailing comment is not the phrase

    out = {}
    for row in LISTED_ROWS:
        ks = []
        for e in rows[row]:
            m = re.match(r"^(\S+\.py):(\d+)(.*)$", e)
            if m:
                fn, phrase = where(m.group(1), int(m.group(2)))
                ks.append(f"{m.group(1)} · {fn} · {phrase} ·{m.group(3)}")
            else:
                ks.append(e)
        out[row] = sorted(ks)
    return out



FROZEN_LISTS = {  # 42f28876's survey, keyed (no line numbers), plus ES-f6's two TABLE_POINT sites and E-steps note 6's two VALUE_BOUND_MIXED sites
    'other_module_attr': [
        'ammonia_table.py · _iso_smooth · smooth_table.EXTRAPOLATED_READS[0] += 1 · smooth_table.EXTRAPOLATED_READS (smooth_table)',
        'interior.py · integrate · eos.VALUE_BOUND_MIXED["first"] = None · eos.VALUE_BOUND_MIXED (eos)',
        'interior.py · integrate · eos.VALUE_BOUND_MIXED["first"] = vb_saved if vb_saved is not None else vb_first · eos.VALUE_BOUND_MIXED (eos)',
        'interior.py · integrate · water_hot.CLAMPED["first"] = None · water_hot.CLAMPED (water_hot)',
        'interior.py · integrate · water_hot.CLAMPED["first"] = hw_saved if hw_saved is not None else hw_first · water_hot.CLAMPED (water_hot)',
        'mantle_composition.py · swap · eos.MATERIALS.update(saved) · eos.MATERIALS (eos)',
        'mantle_composition.py · swap · eos.MATERIALS[n] = table_material(m, tab.key) · eos.MATERIALS (eos)',
        'samuel_structure.py · mars_profile · interior.integrate = plain · interior.integrate (interior)',
        'samuel_structure.py · mars_profile · interior.integrate = recording · interior.integrate (interior)',
        'structure_grid.py · _pinned_solve · interior._PIN[0] = (float(s0_values["core_temperature"]), float(s0_values["core_pressure"]) * 1e9) · interior._PIN (interior)',
        'structure_grid.py · _pinned_solve · interior._PIN[0] = saved · interior._PIN (interior)',
        'structure_grid.py · one · interior.TABLE_POINT[0] = False · interior.TABLE_POINT (interior)',
        'structure_grid.py · one · interior.TABLE_POINT[0] = True · interior.TABLE_POINT (interior)',
        'structure_grid.py · one · interior._ENTRY[0] = None · interior._ENTRY (interior)',
        'structure_grid.py · one · interior._ENTRY[0] = entry · interior._ENTRY (interior)',
        'thermal_ale.py · _land · hp.STEP["ratio"] = mid / hp.STEP["h_last"] if hp.STEP["h_last"] else 1.0 · hp.STEP (hop_track)',
        'thermal_ale.py · _run · hp.STEP["ale"] = True · hp.STEP (hop_track)',
        'thermal_ale.py · _run · hp.STEP["c"] = 1.0 if moved else 0.0 · hp.STEP (hop_track)',
        'thermal_ale.py · _run · hp.STEP["h_last"] = h · hp.STEP (hop_track)',
        'thermal_ale.py · _run · hp.STEP["ratio"] = (h_used / hp.STEP["h_last"]) if hp.STEP["h_last"] else 1.0 · hp.STEP (hop_track)',
        'thermal_ale.py · _run · hp.STEP["ratio"] = h_used / hp.STEP["h_last"] if hp.STEP["h_last"] else 1.0 · hp.STEP (hop_track)',
        'thermal_ale.py · _run · hp.STEP["ratio"] = ratio_in · hp.STEP (hop_track)',
        'thermal_ale.py · _step · hp.STEP["c"] = 1.0 · hp.STEP (hop_track)',
        'thermal_ale.py · _step · hp.STEP["c"] = G · hp.STEP (hop_track)',
        'thermal_ale.py · event_signs · hp.STEP["c"] = c · hp.STEP (hop_track)',
    ],
    'setattr': [
        'process_state.py · reset · setattr(importlib.import_module(mod), name, initial) ·',
        'samuel_structure.py · load · setattr(p, k, d[k]) ·',
    ],
    'contextvars': [
        'convergence.py · <module> · _TRACE: contextvars.ContextVar["Trace | None"] = contextvars.ContextVar( ·',
    ],
    'imported_name': [
        'interior.py · _declared_light_core · MATERIALS.pop(name, None) · MATERIALS (eos.MATERIALS)',
        'interior.py · _declared_light_core · MATERIALS[name] = Material( · MATERIALS (eos.MATERIALS)',
        'interior.py · _sulphur_core · MATERIALS.pop(name, None) · MATERIALS (eos.MATERIALS)',
        'interior.py · _sulphur_core · MATERIALS[name] = Material( · MATERIALS (eos.MATERIALS)',
    ],
    'closure_cells': [
        'interior.py · apply_jump · nonlocal t · nonlocal t',
        'interior.py · contract_close · nonlocal st, converged, t_c · nonlocal st,converged,t_c',
        'interior.py · locate_wall · nonlocal wall, wall_why · nonlocal wall,wall_why',
        'interior.py · lower_point · nonlocal lo · nonlocal lo',
        'interior.py · material_for · nonlocal layer · nonlocal layer',
        'interior.py · note · nonlocal lo, hi, dlo, dhi, dlo_tau, dhi_tau · nonlocal lo,hi,dlo,dhi,dlo_tau,dhi_tau',
        'interior.py · note_switch · nonlocal core_radius, p_cmb, t_cmb, p_ice_base, r_crust_base, p_crust_base · nonlocal core_radius,p_cmb,t_cmb,p_ice_base,r_crust_base,p_crust_base',
        'interior.py · remember · nonlocal best, best_attempt, attempts · nonlocal best,best_attempt,attempts',
        'tidal_transport.py · _walk · nonlocal M_h, R_h · nonlocal M_h,R_h',
    ],
    'instance_state': [
        'convergence.py Trace._merge_and self.invalid',
        'convergence.py Trace._merge_and self.sites',
        'convergence.py Trace._merge_and self.trial_false',
        'convergence.py Trace._merge_and self.unchecked',
        'convergence.py Trace.add_shot self.counts',
        'convergence.py Trace.add_shot self.fallbacks',
        'convergence.py Trace.add_shot self.shots',
        'convergence.py Trace.add_shot self.substituted',
        'convergence.py Trace.note self.invalid',
        'convergence.py Trace.note self.sites',
        'convergence.py Trace.note self.trial_false',
        'convergence.py Trace.note self.unchecked',
        'convergence.py Trace.note_substituted self.substituted',
        'convergence.py Trace.settle self.shots',
        'convergence.py Trace.settle self.trial_false',
        'convergence.py Trace.settle self.trial_invalid',
        'mantle_composition.py Table.at self._st_cache',
        'samuel_layer.py LayerGrid._melt_step self.iterations_max',
        'samuel_layer.py LayerGrid._melt_step self.phi',
        'samuel_layer.py LayerGrid._melt_step self.t',
        'samuel_layer.py LayerGrid._track_margin self.history',
        'samuel_layer.py LayerGrid._track_margin self.margin',
        'samuel_layer.py LayerGrid.start self.phi',
        'samuel_layer.py LayerGrid.start self.t',
        'samuel_layer.py LayerGrid.step self.t',
        'samuel_lid.py LidGrid.start self.r',
        'samuel_lid.py LidGrid.start self.t',
        'samuel_lid.py LidGrid.step self._r_crust',
        'state.py BodyState._note self.lookups',
        'state.py BodyState.record self.results',
    ],
    'class_attr': [
    ],
    'object_attr': [
    ],
    'mutable_default': [
    ],
    'functools_cache': [
    ],
    'c_extension': [
    ],
}

rows, summary = survey(HERE)
# ES-f6 (a.1) adds interior.TABLE_POINT, written only from structure_grid._solve_raw (two sites, set and cleared): the
# «another module's attribute» row grows by exactly those two, named below; every other row is the frozen survey.
# E-steps note 6 (rev 4) adds the counter eos.VALUE_BOUND_MIXED (census and counter +1, registered in test_process_state)
# and its two save/restore sites in interior.integrate, the same pair water_hot.CLAMPED has there (+2, named below)
expect = FROZEN.replace("other_module_attr 21", "other_module_attr 25").replace("census 76 (counter 31,", "census 77 (counter 32,")
check("the survey's SUMMARY equals the frozen line, with ES-f6's two named TABLE_POINT sites and note 6's VALUE_BOUND_MIXED",
      summary == expect, summary)
vb_sites = sorted(e for e in rows["other_module_attr"] if "VALUE_BOUND_MIXED" in e)
check("note 6's two added sites are interior.integrate's VALUE_BOUND_MIXED save and restore", len(vb_sites) == 2
      and all(e.split(":", 1)[0] == "interior.py" and "eos.VALUE_BOUND_MIXED (eos)" in e for e in vb_sites), str(vb_sites))
new_sites = sorted(e for e in rows["other_module_attr"] if "TABLE_POINT" in e)
check("the two added sites are structure_grid's TABLE_POINT set and clear", len(new_sites) == 2
      and all(e.split(":", 1)[0] == "structure_grid.py" and "interior.TABLE_POINT (interior)" in e for e in new_sites), str(new_sites))
kd = keyed(rows, HERE)
for row in LISTED_ROWS:              # r2 B1 on db4eab30: §4.6's «each blind-spot row's hit list equal», not the counts
    check(f"the «{row}» hit list equals the frozen list ({len(FROZEN_LISTS[row])})", kd[row] == FROZEN_LISTS[row],
          f"new {sorted(set(kd[row]) - set(FROZEN_LISTS[row]))[:3]} · gone {sorted(set(FROZEN_LISTS[row]) - set(kd[row]))[:3]}")
check("unlisted 0", not [r for r in rows["census"] if r[2] == "UNLISTED"])
check("START is the three", sorted((r[0], r[1]) for r in rows["census"] if r[2] == "start")
      == [("fermi", "_LAST_INVERSE"), ("hop_track", "STEP"), ("water_hot", "_LAST_DENSITY")])
PLANTS = {
    "contextvars": "import contextvars\nV = contextvars.ContextVar('v', default=None)\n",
    "other_module_attr": "import eos\ndef f():\n    eos.PLANTED[1] = 2\n",
    "imported_name": "from eos import MATERIALS\ndef f():\n    MATERIALS['x'] = 1\n",
    "instance_state": "class C:\n    def go(self):\n        self.cache[1] = 2\n",
    "closure_cells": "def f():\n    x = 0\n    def g():\n        nonlocal x\n        x += 1\n    return g\n",
    "setattr": "import eos\ndef f():\n    setattr(eos, 'X', 1)\n",
    "class_attr": "class D:\n    N = 0\n    @classmethod\n    def bump(cls):\n        cls.N = 1\n",
    "object_attr": "class E:\n    pass\nOBJ = E()\ndef f():\n    OBJ.n = 1\n",
    "mutable_default": "def f(x=[]):\n    return x\n",
    "functools_cache": "import functools\n@functools.lru_cache\ndef f(x):\n    return x\n",
    "c_extension": "import numpy as np\ndef f():\n    return np.random.random()\n",
    "census": "X = {}\ndef f():\n    X[1] = 2\n",
}
with tempfile.TemporaryDirectory() as d:
    for p in HERE.glob("*.py"):
        shutil.copy(p, Path(d) / p.name)
    for row, code in PLANTS.items():
        f = Path(d) / "zz_planted.py"
        f.write_text(code)
        got, _s = survey(Path(d))
        f.unlink()
        check(f"a planted hit raises the «{row}» row", len(got[row]) > len(rows[row]), f"{len(rows[row])} → {len(got[row])}")
# the swap control (r2 B1): one listed site renamed to an unlisted one in the same row keeps every count, and must read red
with tempfile.TemporaryDirectory() as d:
    for p in HERE.glob("*.py"):
        shutil.copy(p, Path(d) / p.name)
    sg = Path(d) / "structure_grid.py"
    txt = sg.read_text()
    assert txt.count("interior._PIN[0] = saved") == 1
    sg.write_text(txt.replace("interior._PIN[0] = saved", "interior._PLANTED_SWAP[0] = saved"))
    got, s2 = survey(Path(d))
    kg = keyed(got, Path(d))
    check("swap control: the counts are unchanged", s2 == summary, s2)
    check("swap control: the «other_module_attr» list reads red", kg["other_module_attr"] != FROZEN_LISTS["other_module_attr"])
print(f"test_state_survey: {'모두 통과' if not fails else f'FAIL {fails}'}")
sys.exit(1 if fails else 0)
