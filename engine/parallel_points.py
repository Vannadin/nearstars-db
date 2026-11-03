# 독립 점 여러 개를 프로세스 풀로 풀어 돌려주는 엔진 공용 도우미 (structure-grid 덧붙임 44)
"""Solve independent points in a process pool and return the results in input order.

`solve_points(fn, jobs, pool)` calls ``fn(*job)`` for each job, after `process_state.reset()` — the same
rule in a worker and in this process, so the answer does not depend on which points a process solved
before. Workers are forked (the solver closure is inherited, not pickled); ``fn`` must return something
picklable. With one job or ``pool <= 1`` everything runs here under the same rule.
"""
from __future__ import annotations

import os
import sys
import time

import process_state

_FN = None


def _one(job):
    """ES-f6 (d1): a start and an end line per job, flushed — output only, no value or decision reads them."""
    process_state.reset()
    t0 = time.time()
    print(f"점 시작 — {job[0]!r} · pid {os.getpid()} · {time.strftime('%H:%M:%S')}", flush=True)
    try:
        return _FN(*job)
    finally:
        print(f"점 끝 — {job[0]!r} · {time.time() - t0:.1f} s", flush=True)


def _line_buffered():
    """ES-f6 (d1): each forked worker writes stdout line by line (block buffering hid a 5.7 h point until exit)."""
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except (AttributeError, ValueError):
        pass


def solve_points(fn, jobs, pool: int):
    global _FN
    _FN = fn
    jobs = list(jobs)
    if len(jobs) <= 1 or pool <= 1:
        return [_one(j) for j in jobs]
    import multiprocessing as mp
    with mp.get_context("fork").Pool(min(pool, len(jobs)), initializer=_line_buffered) as p:
        return p.map(_one, jobs, chunksize=1)
