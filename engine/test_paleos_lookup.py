# PALEOS 조회기가 표에 있는 줄을 빠짐없이 찾는지 · 없는 줄은 여전히 «없음» 인지 묻는 시험 (C125)
"""Checks for C125 (pre-registration `prereg-c125-paleos-lookup.md`, frozen a5ddce09).

    python3 engine/test_paleos_lookup.py

LK-적중 — per table: 300 random existing rows under each of two seeds (20260927, 314159), plus the first and last
          data rows, plus 63 rows whose line start sits right after a depth-1..6 halving midpoint of the data
          region: `_seek_line_start(fh, s, floor) == s` for each such start s (the bug's own shape), and each row
          looked up is found and returned verbatim.
LK-없음 — MgSiO₃: random grid cells with no row in the file answer «PALEOS 없음».
LK-밖   — a request outside the grid's own ends answers «PALEOS 범위 밖».
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paleos                          # noqa: E402

SEEDS = (20260927, 314159)
N = 300
fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


def rows_with_offsets(f) -> list[tuple[int, str]]:
    out = []
    with f.path.open("rb") as fh:
        fh.seek(f.data_start)
        pos = f.data_start
        for raw in fh:
            if raw.strip():
                out.append((pos, raw.decode("utf-8")))
            pos += len(raw)
    return out


def found(table: str, line: str) -> bool:
    """A hit whose density is that row's own density column — the row itself came back, not a neighbour."""
    parts = line.split()
    r = paleos.lookup(table, float(parts[0]), float(parts[1]))
    return r.get("grade") == paleos.GRADE_HIT and r.get("density") == float(parts[2])


for table in ("MgSiO3", "Fe", "H2O"):
    f = paleos.facts(table)
    rows = rows_with_offsets(f)
    # random existing rows, two seeds
    for seed in SEEDS:
        pick = random.Random(seed).sample(rows, N)
        miss = [ln for _, ln in pick if not found(table, ln)]
        check(f"LK-적중 {table} — {N} random rows, seed {seed}, all found", not miss, f"{len(miss)} missed")
    # first and last data rows
    check(f"LK-적중 {table} — first and last data rows found",
          found(table, rows[0][1]) and found(table, rows[-1][1]))
    # the bug's shape: line starts right after halving midpoints
    starts = [p for p, _ in rows]
    size = f.path.stat().st_size
    mids = []
    for depth in range(1, 7):
        k = 2 ** depth
        mids += [f.data_start + (size - f.data_start) * i // k for i in range(1, k, 2)]
    import bisect
    edge = sorted({starts[min(bisect.bisect_left(starts, m), len(starts) - 1)] for m in mids})
    by_start = dict(rows)
    with f.path.open("r", encoding="utf-8") as fh:
        keep = [s for s in edge if paleos._seek_line_start(fh, s, f.data_start) == s]
    miss = [s for s in edge if not found(table, by_start[s])]
    check(f"LK-적중 {table} — _seek_line_start keeps a line that starts exactly at the offset ({len(edge)} starts)",
          len(keep) == len(edge), f"{len(edge) - len(keep)} dropped")
    check(f"LK-적중 {table} — those {len(edge)} rows are found", not miss, f"{len(miss)} missed")
    # LK-밖
    r = paleos.lookup(table, f.p_hi * 10.0, f.t_lo)
    check(f"LK-밖 {table} — beyond the pressure end answers «범위 밖»", r.get("grade") == paleos.GRADE_OUT, str(r.get("grade")))
    if table == "MgSiO3":
        present = {paleos._row_key(ln, f) for _, ln in rows}
        absent = [(i, j) for i in range(f.n_p) for j in range(f.n_t) if (i, j) not in present]
        pick = random.Random(SEEDS[0]).sample(absent, N)
        wrong = []
        for i, j in pick:
            p = 10 ** (__import__("math").log10(f.p_lo) + i * f.dlog_p)
            t = 10 ** (__import__("math").log10(f.t_lo) + j * f.dlog_t)
            if paleos.lookup(table, p, t).get("grade") != paleos.GRADE_ABSENT:
                wrong.append((i, j))
        check(f"LK-없음 MgSiO3 — {N} absent grid cells answer «없음» ({len(absent)} absent in all)", not wrong,
              f"{len(wrong)} answered otherwise")

print(f"\n  test_paleos_lookup — {'모두 통과' if fails == 0 else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
