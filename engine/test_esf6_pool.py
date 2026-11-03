# ES-f6 풀 시험 — 표 점 깃발이 포크된 일꾼 안에서만 켜지는지(a §4.2)와, 일꾼 줄이 점마다 시작·끝으로 바로 흘러나오는지(d1)
"""ES-f6 (a) frozen §4.2 (artifacts pc/ea-esf6/prereg-a.frozen.md, blob 2ceec161) and (d) frozen §3 (prereg-d.frozen.md,
blob 65a1eeb4):
- through structure_grid._solve_raw on a real forked pool of 2 (and in-process with pool 1), a fake solve sees
  interior.TABLE_POINT[0] true; after the call it is false in the parent and in a later direct call;
- a raising point solve leaves TABLE_POINT false (the finally);
- (d1): a child process running parallel_points.solve_points on a pool of 2 with sleeping jobs writes each job's
  «점 시작» line before its «점 끝» line, the first start line reaches the parent's pipe before the slowest job ends, and
  the results come back in input order."""
import os
import subprocess
import sys
import textwrap
import time
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
fails = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        fails.append(name)


import interior  # noqa: E402
import structure_grid as sg  # noqa: E402


def fake_solve(t, p_hint=None):
    if t < 0:
        raise RuntimeError("planted")
    return types.SimpleNamespace(applicable=False, reason=f"TABLE_POINT={interior.TABLE_POINT[0]}", regime=None,
                                 converged=True, notes=(), inputs={}, values={})


print("(a §4.2) the switch reaches the workers and is cleared after")
for pool in (2, 1):
    saved = sg.GRID_POOL
    sg.GRID_POOL = pool
    try:
        got = sg._solve_raw(fake_solve, [(1500.0, None, None), (1600.0, None, None), (1700.0, None, None)])
    finally:
        sg.GRID_POOL = saved
    check(f"pool {pool}: every point solve saw TABLE_POINT true", [g.reason for g in got] == ["TABLE_POINT=True"] * 3,
          str([g.reason for g in got]))
    check(f"pool {pool}: false in the parent after", interior.TABLE_POINT[0] is False)
check("a direct solve after a table build sees TABLE_POINT false", fake_solve(1.0).reason == "TABLE_POINT=False")
saved = sg.GRID_POOL
sg.GRID_POOL = 1
try:
    try:
        sg._solve_raw(fake_solve, [(-1.0, None, None)])
        raised = False
    except RuntimeError:
        raised = True
finally:
    sg.GRID_POOL = saved
check("a raising point solve leaves TABLE_POINT false", raised and interior.TABLE_POINT[0] is False)

print("(d1) worker lines reach the pipe per job, start before end, results in order")
child = textwrap.dedent(f"""
    import sys, time
    sys.path.insert(0, {str(HERE)!r})
    import parallel_points
    def fn(t, d):
        time.sleep(d)
        return t * 10
    out = parallel_points.solve_points(fn, [(1, 0.2), (2, 2.5), (3, 0.2), (4, 0.2)], 2)
    print("RESULT", out, flush=True)
""")
p = subprocess.Popen([sys.executable, "-B", "-c", child], stdout=subprocess.PIPE, text=True, env=dict(os.environ))
t0, lines = time.time(), []
for line in p.stdout:
    lines.append((time.time() - t0, line.rstrip("\n")))
p.wait()
starts = {ln.split("—")[1].split("·")[0].strip(): (i, ts) for i, (ts, ln) in enumerate(lines) if ln.startswith("점 시작")}
ends = {ln.split("—")[1].split("·")[0].strip(): (i, ts) for i, (ts, ln) in enumerate(lines) if ln.startswith("점 끝")}
check("a start and an end line for each of the 4 jobs", sorted(starts) == sorted(ends) == ["1", "2", "3", "4"],
      f"{sorted(starts)} {sorted(ends)}")
check("each job's start line comes before its end line", all(starts[k][0] < ends[k][0] for k in starts if k in ends))
first = min(ts for _i, ts in starts.values()) if starts else 99.0
check("the first start line reaches the parent before the slow job (2.5 s) ends", first < 2.0, f"{first:.2f} s")
check("results in input order", any(ln == "RESULT [10, 20, 30, 40]" for _t, ln in lines), str(lines[-1:]))
check("the child exits 0", p.returncode == 0, str(p.returncode))

print(f"test_esf6_pool: {'모두 통과' if not fails else f'FAIL {fails}'}")
sys.exit(1 if fails else 0)
