# 층 적분기가 화성 값을 칸에서만 읽는지 묻는 시험 — st. 0 · 바꿔 넣기 · 가짜 상수 모듈 · 기본값 0 (ⓐ2)
"""Checks for ⓐ2 (pre-registration `prereg-a2-stack-params.md`, frozen 7ff5d844): the layer integrator reads every
Mars value from its stack's slots.

    python3 engine/test_stack_params.py

A2-census   — no `st.` in `thermal_stack.py`, and each moved slot moves the output when changed (swap-in).
A2-가짜      — a child process puts a fake `samuel_thermal` (every upper-case number ×1.37) in `sys.modules` before
              anything imports it, scales `samuel_layer`'s upper-case numbers the same way (not its solver
              tolerances `MELT_TOL_K` · `MELT_MAX_ITER` — they change the iteration count, not a body value), and
              evaluates stacks built from slot values alone: the output must be bit-identical to the real module's.
A2-기본값    — in those evaluations no `samuel_model` default was used (`sm.DEFAULT_USES` stays empty).
"""
from __future__ import annotations

import copy
import pickle
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import samuel_structure as sst         # noqa: E402
import samuel_thermal as st            # noqa: E402
import thermal_stack as ts             # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


# ── A2-census, the grep half
src = (HERE / "thermal_stack.py").read_text(encoding="utf-8")
refs = re.findall(r"\bst\.[A-Za-z_0-9]+", src)
check("A2-census — no `st.` reference left in thermal_stack.py", not refs, f"{len(refs)} found")

# ── the fixture: slot values copied from the reproduction builder, as data (no `st.` in the child)
prof = sst.mars_profile(HERE / "bodies" / "mars.yaml")
G = prof.gravity(prof.radius_m)
LAYER = dict(d_d=st.D_D_M, k_d=4.0, lambda_d=14.373, fe_mean=96.97, fe_top=94.1306, nodes=41, melting=True)
STATE = (2158.1024424461625, 1815.5593199821958, 80e3, 20e3, 1.0)
CASES = {
    "plate 2": dict(lam=20.0),
    "plate 4 (layer, melting)": dict(lam=10.0, model="bml", layer=LAYER),
    "plate 4, hydrostatic melt pressure · total Stefan": dict(lam=10.0, model="bml", layer=LAYER,
                                                            melt_pressure="hydrostatic", stefan_mode="total"),
}


def as_data(s: ts.Stack) -> dict:
    return {"layers": [(x.role, x.kind, x.r_bot, x.r_top, copy.deepcopy(x.params)) for x in s.layers],
            "opt": copy.deepcopy(s.opt), "body": copy.deepcopy(s.body), "g": s.g}


FIX = {name: as_data(ts.samuel_stack(profile=prof, g=G, **kw)) for name, kw in CASES.items()}
# a short full run exercises `run` (start time, age, lid grid, radiogenic heat each step) at little cost
FIX_RUN = copy.deepcopy(FIX["plate 4 (layer, melting)"])
FIX_RUN["body"]["age_gyr"] = 0.02


def build(d: dict) -> ts.Stack:
    layers = [ts.Layer(role, kind, rb, rt, copy.deepcopy(p)) for role, kind, rb, rt, p in d["layers"]]
    return ts.Stack(layers, profile=prof, g=d["g"], options=copy.deepcopy(d["opt"]), body=copy.deepcopy(d["body"]))


def evaluate(d: dict):
    return ts.state_terms(build(d), *STATE, -0.02)


def short_run(d: dict):
    out = ts.run(build(d), 10.0)
    return [(r["t"], r["t_c"], r["t_m"], r["d_l"], r["d_cr"]) for r in out["rows"]]


# ── A2-census, the swap-in half: each moved slot, changed alone, moves the output
base = {n: evaluate(d) for n, d in FIX.items()}
base_run = short_run(FIX_RUN)


def _swap(d: dict, where: str, key: str, fn) -> dict:
    d = copy.deepcopy(d)
    if where == "body":
        d["body"][key] = fn(d["body"][key])
    elif where == "opt":
        d["opt"][key] = fn(d["opt"][key])
    elif where == "g":
        d["g"] = fn(d["g"])
    else:
        for i, lyr in enumerate(d["layers"]):
            if lyr[0] == where:
                lyr[4][key] = fn(lyr[4][key])
    return d


def swapped(case: str, where: str, key: str, fn) -> bool:
    """One evaluation first; slots that act only once a grid steps (basal grid, lid grid) or only where melt
    reaches them show on the short run (plate 4, layer and melting) instead."""
    if evaluate(_swap(FIX[case], where, key, fn)) != base[case]:
        return True
    return short_run(_swap(FIX_RUN, where, key, fn)) != base_run


L4, HY = "plate 4 (layer, melting)", "plate 4, hydrostatic melt pressure · total Stefan"
for label, case, where, key, fn in (
        ("radiogenic concentrations", L4, "body", "concentration", lambda c: {**c, "U": c["U"] * 1.1}),
        ("melting curves — melt integrals", "plate 2", "body", "curves",
         lambda c: {**c, "low": (c["low"][0] - 50.0,) + tuple(c["low"][1:])}),
        ("melting curves — Stefan path", HY, "body", "curves",
         lambda c: {**c, "low": (c["low"][0] - 50.0,) + tuple(c["low"][1:])}),
        ("melting curves — basal grid", L4, "body", "curves",
         lambda c: {**c, "high": (c["high"][0] - 50.0,) + tuple(c["high"][1:])}),
        ("surface temperature", L4, "body", "t_surface", lambda v: v + 10.0),
        ("crust reference fraction", L4, "body", "crust_reference_fraction", lambda v: 0.25),
        ("solidus depletion ΔT_sol", L4, "body", "delta_t_sol", lambda v: v * 1.1),
        # shallower, not deeper: at this state all melt lies above 7.4 GPa, so a deeper threshold only adds
        # shells that do not melt; cutting into the melt zone is what shows the slot is read
        ("melt-extraction depth", "plate 2", "body", "melt_extraction_below_pa", lambda v: v * 0.5),
        ("δ_b law", L4, "opt", "ra_delta_b", lambda v: (v[0] * 1.1, v[1])),
        ("hydrostatic g of the printed form", HY, "opt", "hydrostatic_g", lambda v: v * 1.1),
        ("gravity", L4, "g", None, lambda v: v * 1.01),
        ("basal Fe_m", L4, "basal", "fe_m", lambda v: v + 1.0),
        ("basal iron shift", L4, "basal", "shift_k", lambda v: v + 1.0),
        ("basal density", L4, "basal", "rho_d", lambda v: v * 1.01),
        ("mantle density", L4, "mantle", "rho", lambda v: v * 1.01),
        ("crust conductivity", "plate 2", "lid", "k_crust", lambda v: v * 1.1),
        ("core heat capacity", L4, "core", "cp", lambda v: v * 1.1)):
    check(f"A2-census swap-in — {label} moves the output", swapped(case, where, key, fn))

for label, key, fn in (("age", "age_gyr", lambda v: v * 1.5), ("start time", "t_initial_gyr", lambda v: v * 2.0)):
    d = copy.deepcopy(FIX_RUN)
    d["body"][key] = fn(d["body"][key])
    check(f"A2-census swap-in — {label} moves the short run", short_run(d) != base_run)

# ── A2-가짜 · A2-기본값 — the child sees a fake samuel_thermal before anything imports it
CHILD = r'''
import pickle, sys, types
from pathlib import Path
here = Path(sys.argv[1]); sys.path.insert(0, str(here))
fake = sys.argv[3] == "fake"
import importlib.util
spec = importlib.util.spec_from_file_location("samuel_thermal", here / "samuel_thermal.py")
real = importlib.util.module_from_spec(spec); spec.loader.exec_module(real)
def scale(v):
    if isinstance(v, bool): return v
    if isinstance(v, (int, float)): return v * 1.37
    if isinstance(v, tuple): return tuple(scale(x) for x in v)
    return v
if fake:
    for k in dir(real):
        if k.isupper(): setattr(real, k, scale(getattr(real, k)))
sys.modules["samuel_thermal"] = real
import samuel_layer
if fake:
    for k in dir(samuel_layer):
        if k.isupper() and k not in ("MELT_TOL_K", "MELT_MAX_ITER"):
            setattr(samuel_layer, k, scale(getattr(samuel_layer, k)))
import samuel_model as sm
import thermal_stack as ts
job = pickle.loads(Path(sys.argv[2]).read_bytes())
prof = job["prof"]
def build(d):
    layers = [ts.Layer(r, k, rb, rt, p) for r, k, rb, rt, p in d["layers"]]
    return ts.Stack(layers, profile=prof, g=d["g"], options=d["opt"], body=d["body"])
out = {n: ts.state_terms(build(d), *job["state"], -0.02) for n, d in job["fix"].items()}
run = ts.run(build(job["fix_run"]), 10.0)
out["short run"] = [(r["t"], r["t_c"], r["t_m"], r["d_l"], r["d_cr"]) for r in run["rows"]]
sys.stdout.buffer.write(pickle.dumps({"out": out, "defaults": dict(sm.DEFAULT_USES)}))
'''
with tempfile.TemporaryDirectory() as tmp:
    jobf = Path(tmp) / "job.pkl"
    jobf.write_bytes(pickle.dumps({"prof": prof, "state": STATE, "fix": FIX, "fix_run": FIX_RUN}))
    res = {}
    for mode in ("real", "fake"):
        p = subprocess.run([sys.executable, "-c", CHILD, str(HERE), str(jobf), mode], capture_output=True)
        if p.returncode != 0:
            print(p.stderr.decode(errors="replace")[-2000:])
        res[mode] = pickle.loads(p.stdout) if p.returncode == 0 else None
ok = res["real"] is not None and res["fake"] is not None
check("A2-가짜 — both child processes ran", ok)
if ok:
    same_as_parent = all(res["real"]["out"][n] == base[n] for n in FIX) and res["real"]["out"]["short run"] == base_run
    check("A2-가짜 — the real-module child reproduces this process bit for bit", same_as_parent)
    for n in list(FIX) + ["short run"]:
        check(f"A2-가짜 — {n}: fake samuel_thermal/samuel_layer constants move nothing",
              res["fake"]["out"][n] == res["real"]["out"][n])
    for mode in ("real", "fake"):
        check(f"A2-기본값 — no samuel_model default used ({mode} child)", res[mode]["defaults"] == {},
              str(res[mode]["defaults"]))

print(f"\n  test_stack_params — {'모두 통과' if fails == 0 else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
