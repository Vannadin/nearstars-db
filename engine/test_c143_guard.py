# C143 가드 (b) — 알려진 fsum 자리를 보통 sum() 과 3.9 식 sum() 으로 두 번 평가해 비트까지 같은지, 그리고 engine/ 의 sum() 호출 목록이 굳힌 목록과 같은지 본다 (매 게이트, 몇 초)
"""python3 engine/test_c143_guard.py [--write]   (prereg-c143-compensated-sum-boundaries b17dcb5c, post-freeze note 1)

1. Sites, bit for bit: each registered site is evaluated with the shipped `builtins.sum` and with a left-to-right `sum()`
   (Python ≤ 3.11 behaviour) patched into `builtins`. Outputs must be identical to the last bit, and every C143 verdict
   identical.
2. Inventory: an AST census of `sum(...)` calls over `engine/` (key: file · enclosing function · the call's source text,
   so line moves do not matter) must equal `c143_sum_inventory.json`. A new call fails this test: it forces a list
   update (`--write`) **and** a run of the naive-hook re-run (`scripts/c143_guard.py`, note 1 item 3).
"""
from __future__ import annotations

import ast
import builtins
import json
import math
import sys
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
INVENTORY = HERE / "c143_sum_inventory.json"
fails: list[str] = []


def census() -> list[list[str]]:
    out = []
    for f in sorted(HERE.rglob("*.py")):
        rel = f.relative_to(HERE)
        if any(part.startswith(".venv") for part in rel.parts):
            continue
        tree = ast.parse(f.read_text(encoding="utf-8"))
        parents = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parents[child] = node
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "sum":
                fn, up = "<module>", parents.get(node)
                while up is not None:
                    if isinstance(up, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        fn = up.name
                        break
                    up = parents.get(up)
                out.append([rel.as_posix(), fn, ast.unparse(node)])
    return sorted(out)


def naive_sum(iterable, /, start=0):
    items = list(iterable)
    r = _orig_sum(items, start)
    if not isinstance(r, float):
        return r
    acc = start
    for x in items:
        acc = acc + x
    return acc


_orig_sum = builtins.sum


def evaluate() -> dict:
    """Every registered site once; returns plain values (floats via repr, so bits compare exactly)."""
    import mantle_composition as mc
    import samuel_lid as sl
    import radiogenic as rg
    import eos
    mc._TABLES.clear()
    out = {}
    # the two compositions the shipped tables are built for — the printed tables of test_mantle_composition (W&H DMM for
    #   Earth, Khan+ 2022 for Mars), read through the engine's own reader
    for body, printed in _tables().items():
        wt, why = mc.read_mantle_composition({"value": printed, "grade": "literature", "source": "C143 guard",
                                              "counter_evidence_searched": "C143 guard"})   # read total (fsum)
        if wt is None:
            out[body] = {"why": why}
            continue
        cf = mc.cfmasna(wt)                                       # normalisation (fsum)
        key = mc.expected_key(wt)                                 # the fingerprint built on it
        table, why = mc.load(wt)
        out[body] = {"total": repr(math.fsum(wt.values())), "cfmasna": {k: repr(v) for k, v in cf.items()},
                     "key": key, "why": why}
        if table is not None:                                     # the bilinear sum (fsum)
            ps, ts = mc.grid_p(), mc.grid_t()
            p, t = 0.5 * (ps[3] + ps[4]), 0.5 * (ts[3] + ts[4])
            try:
                out[body]["at"] = [repr(x) for x in table.at(p, t)]
            except mc.TableMiss as e:
                out[body]["at"] = f"TableMiss {e}"
    kw = dict(r_p=3389.5e3, d_l=200e3, t_l=1500.0, t_s=220.0, k_m=4.0, k_cr=4.0, h_m=2e-8, h_cr=2e-8)
    two, one = sl.quasi_steady_gradient(d_cr=50e3, **kw), sl.quasi_steady_gradient(d_cr=0.0, **kw)
    out["samuel_lid"] = {"two": repr(two), "one": repr(one), "verdict": abs(two - one) < 1e-12 * abs(one)}
    out["R1"] = {el: repr(math.fsum(rg.ISOTOPES[n][1] * rg.ISOTOPES[n][2] for n in rg.ISOTOPES if rg.ELEMENT_OF[n] == el))
                 for el in ("U", "Th", "K")}
    ice = math.fsum(eos.SOLAR_ICE_MASS_FRACTIONS.values())
    out["solar_ice"] = {"sum": repr(ice), "verdict": abs(ice - 1.0) <= 4 * math.ulp(1.0)}
    return out


def _tables() -> dict:
    """The printed tables `DMM_WH2005` and `MARS_KHAN2022`, read from `test_mantle_composition.py` without running it."""
    tree = ast.parse((HERE / "test_mantle_composition.py").read_text(encoding="utf-8"))
    return {node.targets[0].id: ast.literal_eval(node.value) for node in tree.body
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id in ("DMM_WH2005", "MARS_KHAN2022")}


def printed_tables():
    """The Khan / W&H printed sums, as `test_mantle_composition` computes them (Decimal of the printed digits)."""
    return {k: str(sum(Decimal(repr(v)) for v in t.values())) for k, t in _tables().items()}


def main() -> int:
    if "--write" in sys.argv:
        INVENTORY.write_text(json.dumps(census(), indent=0, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {INVENTORY.name}: {len(census())} sum() calls")
        return 0
    # 2. inventory
    now, frozen = census(), json.loads(INVENTORY.read_text(encoding="utf-8"))
    new = [s for s in now if s not in frozen]
    gone = [s for s in frozen if s not in now]
    for s in new:
        fails.append(f"new sum() call not in the inventory: {s[0]} · {s[1]} · {s[2][:80]} — update the list "
                     "(--write) and run scripts/c143_guard.py (the naive-hook re-run)")
    for s in gone:
        fails.append(f"inventory lists a sum() call that is gone: {s[0]} · {s[1]} · {s[2][:80]} — update the list")
    print(f"  inventory: {len(now)} sum() calls in {len({s[0] for s in now})} files · new {len(new)} · gone {len(gone)}")
    # 1. sites, shipped sum() against left-to-right sum()
    a, pa = evaluate(), printed_tables()
    builtins.sum = naive_sum
    try:
        b, pb = evaluate(), printed_tables()
    finally:
        builtins.sum = _orig_sum
    for k in a:
        if a[k] != b[k]:
            fails.append(f"site {k} differs between the shipped and the left-to-right sum(): {a[k]} vs {b[k]}")
    if pa != pb:
        fails.append(f"printed-table sums differ: {pa} vs {pb}")
    khan_ok = abs(Decimal(pa["MARS_KHAN2022"]) - 100) <= Decimal("0.01")
    if not khan_ok:
        fails.append(f"Khan printed sum {pa['MARS_KHAN2022']} is outside 100 ± 0.01")
    print(f"  sites: {', '.join(a)} — bit-identical under both sum(): {all(a[k] == b[k] for k in a)} · "
          f"Khan {pa['MARS_KHAN2022']} · W&H {pa['DMM_WH2005']} · samuel_lid verdict {a['samuel_lid']['verdict']} · "
          f"solar ice {a['solar_ice']['sum']}")
    for f in fails:
        print("FAIL", f)
    print("test_c143_guard:", "FAIL" if fails else "ok")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
