# E-id 강화 시험 — id 키 표의 열린 틈(적분 뒤 붙잡기 전 예외)을 트리별로 심어 기준은 빨간불 · 수정은 초록으로, 깊이 · 구조 출처 · 물 캐시를 AST 로, 겹친 풀이 없음을 최대 깊이로 지킴
"""python3 engine/test_eid.py   (frozen prereg pc/ea-eid/eid-prereg.frozen.md, rev 4, artifacts 29b23943)

E-a  window (a), planted: `_note_loop_trial` raises once after a basal-layer integration has written `_BASAL_INFO`.
     Fix tree (the dropped structure is in `_ALIVE`): it is held and its entry still maps to it — green.
     Base tree (not held): bare same-size objects are made until one reuses the dropped id (bounded; never skips) and
     `_BASAL_INFO.get(id(it))` returns the dropped structure's entry — the defect, red.
E-b  (b) `_depth_counted` restores the depth after a raise; `_ALIVE.clear()` sits under `_SOLVE_DEPTH[0] <= 1`.
     (c) AST: `Structure(` is built only in `_integrate_raw`, and each construction is followed by `_ALIVE.append`
     before any `[id(…)] =` write.
E-c  AST: water_table's and water2_table's `_bilinear` are called only with RHO, DTDP_S or C_P.
E-f  guard: the maximum `_SOLVE_DEPTH` over one real solve (a Mars-mass solve) is 1; a planted nested solve raises it
     to 2 (the control). Red the day a nested caller appears (then the inner clears must become outermost-only).
"""
from __future__ import annotations

import ast
import gc
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import interior as I  # noqa: E402

FAILS = []


def check(label, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        FAILS.append(label)


SRC = (HERE / "interior.py").read_text()
TREE = ast.parse(SRC)
M, CMF, TP = 0.1074, 0.24, 1600.0                     # test_basal_layer's Mars inputs (not a fit)

# a real basal-layer state to integrate from
lay = I.solve(M, core_mass_fraction=CMF, potential_temperature=TP, basal_layer_thickness_km=150.0,
              basal_layer_density=4050.0)
p_c, t_c = lay.values["core_pressure"] * 1e9, lay.values["core_temperature"]

# E-a — window (a), planted
I._ALIVE.clear()
I._BASAL_INFO.clear()
real_note = I._note_loop_trial
calls = {"n": 0}


def raise_once(*a, **k):
    calls["n"] += 1
    raise RuntimeError("E-id planted raise after the raw integration")


I._note_loop_trial = raise_once
try:
    I.integrate(p_c, M * I.EARTH_MASS_KG, CMF, 0.0, "fe_prem", t_center=t_c, t_pot=TP,
                basal_layer={"thickness_m": 150e3, "density": 4050.0})
    raised = False
except RuntimeError:
    raised = True
finally:
    I._note_loop_trial = real_note
check("E-a plant — the raise happened after the raw integration wrote _BASAL_INFO", raised and len(I._BASAL_INFO) == 1,
      f"raised {raised} · entries {len(I._BASAL_INFO)}")
key = next(iter(I._BASAL_INFO), None)
gc.collect()
held = [s for s in I._ALIVE if id(s) == key]
if held:                                               # the fix tree
    check("E-a (fix) — the dropped structure is held in _ALIVE and its entry maps to it",
          len(held) == 1 and I._BASAL_INFO.get(id(held[0])) is not None)
else:                                                  # the base tree: show the reuse defect
    keep, reused = [], None
    for _ in range(200000):
        o = object.__new__(I.Structure)
        if id(o) == key:
            reused = o
            break
        keep.append(o)
    check("E-a (base) — a bare same-size object reused the dropped id (else the test cannot run)", reused is not None)
    check("E-a (base) — the reused id reads the dropped structure's entry (the window-(a) defect)",
          reused is not None and I._BASAL_INFO.get(id(reused)) is None,
          "the stale entry is returned" if reused is not None and I._BASAL_INFO.get(id(reused)) is not None else "")
    del keep
I._ALIVE.clear()
I._BASAL_INFO.clear()

# E-b — (b) depth restored after a raise; the clear sits under the outermost test
@I._depth_counted
def _boom():
    raise ValueError("planted")


d0 = I._SOLVE_DEPTH[0]
try:
    _boom()
except ValueError:
    pass
check("E-b (b) — _depth_counted restores _SOLVE_DEPTH after a raise", I._SOLVE_DEPTH[0] == d0)
under = False
for node in ast.walk(TREE):
    if isinstance(node, ast.If) and "_SOLVE_DEPTH" in ast.unparse(node.test) and "<= 1" in ast.unparse(node.test):
        under = under or any("_ALIVE.clear()" in ast.unparse(s) for s in node.body)
check("E-b (b) — _ALIVE.clear() sits under `_SOLVE_DEPTH[0] <= 1`", under)

# E-b — (c) Structure is built only in _integrate_raw, each held before any id-keyed write
sites = [(f.name, n) for f in ast.walk(TREE) if isinstance(f, ast.FunctionDef) for n in ast.walk(f)
         if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "Structure"]
check("E-b (c) — Structure( is built only inside _integrate_raw", sites and {name for name, _ in sites} == {"_integrate_raw"},
      str(sorted({name for name, _ in sites})))
raw = next(f for f in TREE.body if isinstance(f, ast.FunctionDef) and f.name == "_integrate_raw")
raw_lines = SRC.split("\n")[raw.lineno - 1:raw.end_lineno]
ok_c = True
for _name, call in sites:
    after = SRC.split("\n")[call.end_lineno:raw.end_lineno]
    nxt_append = next((i for i, ln in enumerate(after) if "_ALIVE.append(" in ln), None)
    nxt_write = next((i for i, ln in enumerate(after) if "[id(" in ln and "] =" in ln), None)
    ok_c = ok_c and nxt_append is not None and (nxt_write is None or nxt_append < nxt_write)
check("E-b (c) — each construction is followed by _ALIVE.append before any [id(…)] = write", ok_c)

# E-c — the water caches' keys are module constants
for mod in ("water_table.py", "water2_table.py"):
    t = ast.parse((HERE / mod).read_text())
    args = [ast.unparse(n.args[0]) for n in ast.walk(t)
            if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "_bilinear" and n.args]
    check(f"E-c — {mod}: _bilinear is called only with RHO, DTDP_S or C_P", args and set(args) <= {"RHO", "DTDP_S", "C_P"},
          str(args))

# E-f — the guard: no nested solve on a real path; a planted one is seen
class MaxDepth(list):
    def __init__(self, base):
        super().__init__(base)
        self.max = base[0]

    def __setitem__(self, i, v):
        super().__setitem__(i, v)
        self.max = max(self.max, v)


real_depth = I._SOLVE_DEPTH
I._SOLVE_DEPTH = MaxDepth(real_depth)
try:
    I.solve(M, core_mass_fraction=CMF, potential_temperature=TP)
    real_max = I._SOLVE_DEPTH.max
    I._SOLVE_DEPTH.max = 0
    once = {"done": False}

    def nested_once(*a, **k):
        if not once["done"]:
            once["done"] = True
            I.solve(M, core_mass_fraction=CMF)                        # the planted nested caller
        return real_note(*a, **k)

    I._note_loop_trial = nested_once
    try:
        I.solve(M, core_mass_fraction=CMF, potential_temperature=TP)
    finally:
        I._note_loop_trial = real_note
    planted_max = I._SOLVE_DEPTH.max
finally:
    I._SOLVE_DEPTH = real_depth
check("E-f guard — the maximum solve depth over a real solve is 1", real_max == 1, f"max {real_max}")
check("E-f control — a planted nested solve raises it to 2", planted_max == 2, f"max {planted_max}")

print("test_eid: " + ("ok" if not FAILS else f"FAIL ({len(FAILS)})"))
sys.exit(1 if FAILS else 0)
