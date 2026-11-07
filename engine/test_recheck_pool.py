# 풀 재검산 시험 — RECHECK_POOL 로 `_recheck` 를 풀에 돌려도 직렬과 비트 같고(값·동점·첫 거절), 일꾼의 읽기가 가드에 보이며, 폭과 자리 셈이 맞는지
"""python3 engine/test_recheck_pool.py — prereg pc/recheck-pool (frozen 3e484a0c) T1–T7b. T1 solves three real Earth
points twice (minutes); the rest use a planted solver (seconds). Each mutant must turn its compare red."""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import tempfile
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import structure_grid as sg  # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    fails += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


def bits(x: float) -> str:
    return float.hex(float(x))


# ── a planted solver: values per T, refusals by T, an optional read and an optional per-worker perturbation ──
class Planted:
    def __init__(self, vals, refuse=(), read_at=None, read_path=None, perturb_at=None):
        self.vals, self.refuse, self.read_at, self.read_path, self.perturb_at = vals, set(refuse), read_at, read_path, perturb_at
        self.parent = os.getpid()

    def __call__(self, t):
        if self.read_at is not None and t == self.read_at:
            with open(self.read_path, "rb") as fh:
                fh.read(1)
        if t in self.refuse:
            return types.SimpleNamespace(applicable=False, reason=f"planted refusal at {t}", regime=None, converged=False,
                                         notes=(), inputs={"core_mass_fraction": 0.3}, values={})
        v = dict(self.vals[t])
        if self.perturb_at == t and os.getpid() != self.parent:      # a mutant worker: one ulp off in one field
            v["p_cmb"] = math.nextafter(v["p_cmb"], math.inf)
        return types.SimpleNamespace(applicable=True, reason="", regime="planted", converged=True, notes=(),
                                     inputs={"core_mass_fraction": 0.3}, values=v)


def planted_doc(ts, stored):
    return {"t_pot": list(ts), "points": [dict(stored[t], core_mass_fraction=0.3) for t in ts]}


BODY = types.SimpleNamespace(inputs={"mass_earth": 1.0})


def run_planted(solver, doc, pool):
    saved = (sg._solver, sg._params, sg.RECHECK_POOL)
    sg._solver = lambda body, s0: (solver, None, None)
    sg._params = lambda v, t, m: dict(v)
    sg.RECHECK_POOL = pool
    try:
        return sg._recheck(doc, BODY)
    finally:
        sg._solver, sg._params, sg.RECHECK_POOL = saved


TS = [1000.0, 1100.0, 1200.0, 1300.0, 1400.0, 1500.0]
STORED = {t: {k: 1.0 + i * 0.1 + j * 0.01 for j, k in enumerate(sg.FIELDS)} for i, t in enumerate(TS)}

# ── T2: scan order and the tie on `where` ──────────────────────────────────────────────────────────────────────────
TIE_AT = ((1200.0, "r_b"), (1200.0, "g"), (1400.0, "p_cmb"))      # stored 1.0 → solved 1.5: d = 0.5 exactly at all three
stored_t = {t: dict(STORED[t]) for t in TS}
tie = {t: dict(STORED[t]) for t in TS}
for t, k in TIE_AT:
    stored_t[t][k], tie[t][k] = 1.0, 1.5
doc_t = planted_doc(TS, stored_t)
s1 = run_planted(Planted(tie), doc_t, 1)
s3 = run_planted(Planted(tie), doc_t, 3)
check("T2 — 세 자리가 정확히 같은 차 0.5", s1[0] == 0.5, repr(s1))
check("T2 — 동점: 직렬은 T 먼저, FIELDS 순서 먼저인 자리를 이름 댄다", s1[1] == "r_b @ 1200.00 K", repr(s1))
check("T2 — 풀 3 이 직렬과 비트 같음(차와 자리)", (bits(s3[0]), s3[1]) == (bits(s1[0]), s1[1]), f"{s1!r} · {s3!r}")


def scan(doc_, rows, order, ge=False):
    """The scan over solved rows, in a given order of indices; `ge` is the `>=` mutant."""
    worst, where = 0.0, ""
    for i in order:
        t, row, r = doc_["t_pot"][i], doc_["points"][i], rows[i]
        for k in sg.FIELDS:
            d = abs(r[k] - row[k]) / abs(row[k])
            if (d >= worst) if ge else (d > worst):
                worst, where = d, f"{k} @ {t:.2f} K"
    return worst, where


rows = [tie[t] for t in TS]
check("T2 — 같은 훑기를 T 순서로 다시 하면 직렬과 같다", scan(doc_t, rows, range(len(TS))) == s1)
check("T2 대조 — `>=` 훑기는 다른 자리를 낸다(빨강이어야 함)", scan(doc_t, rows, range(len(TS)), ge=True)[1] != s1[1])
check("T2 대조 — 끝난 순서(여기선 역순)로 훑으면 다른 자리를 낸다", scan(doc_t, rows, reversed(range(len(TS))))[1] != s1[1])

doc = planted_doc(TS, STORED)

# ── T3: the first refusal in T order, and the guard on both paths ───────────────────────────────────────────────────
ref = Planted(STORED, refuse=(1200.0, 1400.0))
r1 = run_planted(ref, doc, 1)
r3 = run_planted(ref, doc, 3)
check("T3 — 첫 거절(1200 K)의 문장, 직렬", r1[0] == math.inf and r1[1].startswith("1200.0 K 에서 거절"), repr(r1))
check("T3 — 풀 3 이 같은 첫 거절을 낸다", (r3[0], r3[1]) == (r1[0], r1[1]), repr(r3))
check("T3 대조 — 마지막 거절(1400 K)을 고르면 다르다", not r1[1].startswith("1400.0"))

# ── reads: install the audit hook as `--check` does (it cannot be removed; this process is the test's own) ─────────
sys.addaudithook(sg._reads_hook)
td = tempfile.TemporaryDirectory()
probe = Path(td.name) / "undeclared.dat"
probe.write_bytes(b"x")
probe_s = str(probe.resolve())


def reads_after(solver, pool, union=True):
    sg._READS.clear()
    saved = sg._recheck_pooled
    if not union:                                   # mutant: drop the worker reads
        def no_union(doc_, solve, m_kg):
            import parallel_points
            out = parallel_points.solve_points(lambda t: (sg._light(solve(t)), []), [(t,) for t in doc_["t_pot"]],
                                               sg.RECHECK_POOL)
            return 0.0, ""
        sg._recheck_pooled = no_union
    try:
        run_planted(solver, doc, pool)
    finally:
        sg._recheck_pooled = saved
    return [f for f in sg.guard_reads(set(sg._READS)) if probe_s in f]


# T5: a worker's undeclared read reaches the parent's guard
check("T5 — 풀 3: 일꾼이 연 신고 안 된 파일이 부모의 가드에 보인다(빨강)",
      bool(reads_after(Planted(STORED, read_at=1300.0, read_path=probe), 3)))
check("T5 — 풀 1(오늘의 길)도 같은 파일을 본다", bool(reads_after(Planted(STORED, read_at=1300.0, read_path=probe), 1)))
check("T5 대조 — 읽기 합치기를 뺀 풀은 못 본다(합치기가 빨강을 만든다)",
      not reads_after(Planted(STORED, read_at=1300.0, read_path=probe), 3, union=False))
# T3's guard verdicts: a read before the refusal reds both; one only after it reds pool 3 alone (superset, stated)
before = Planted(STORED, refuse=(1200.0, 1400.0), read_at=1100.0, read_path=probe)
after = Planted(STORED, refuse=(1200.0, 1400.0), read_at=1300.0, read_path=probe)
check("T3 가드 — 거절 앞의 읽기: 직렬과 풀 둘 다 빨강", bool(reads_after(before, 1)) and bool(reads_after(before, 3)))
check("T3 가드 — 거절 뒤에만 있는 읽기: 풀 3 만 빨강(상위 집합, 의도)",
      not reads_after(after, 1) and bool(reads_after(after, 3)))

# ── T4: a perturbed worker turns the bitwise compare red ────────────────────────────────────────────────────────────
captured = []


def run_capture(solver, pool):
    saved = (sg._solver, sg._params, sg.RECHECK_POOL)
    sg._solver = lambda body, s0: (solver, None, None)
    sg._params = lambda v, t, mm: (captured.append((t, {k: bits(x) for k, x in v.items()})), dict(v))[1]
    sg.RECHECK_POOL = pool
    try:
        captured.clear()
        out = sg._recheck(doc, BODY)
        return out, list(captured)
    finally:
        sg._solver, sg._params, sg.RECHECK_POOL = saved


base = run_capture(Planted(STORED), 1)
good = run_capture(Planted(STORED, perturb_at=1300.0), 1)      # in-process: no worker, so no perturbation
bad = run_capture(Planted(STORED, perturb_at=1300.0), 3)
check("T4 — 같은 풀이는 직렬끼리 비트 같음", base[1] == good[1])
check("T4 대조 — 일꾼 하나가 한 ulp 흔들면 비트 대조가 빨강", bad[1] != base[1])

# ── T6: GUARD_RUNS rises by exactly one through check_all, pool 1 and pool 3 ────────────────────────────────────────
def guard_runs_through_check_all(pool):
    """check_all on a temp grid holding one table whose code trigger is moved and whose solve is planted."""
    import run
    with tempfile.TemporaryDirectory() as d:
        body, _ = run.load_body(sg.BODIES_DIR / "earth.yaml")
        trig = sg.triggers(body.inputs)
        trig = json.loads(json.dumps(trig))
        code = trig.setdefault("code", {})
        k0 = sorted(code)[0] if code else "interior.py"
        code[k0] = "0" * 16                                       # a moved code trigger: recheck runs
        t2 = [1500.0, 1600.0]
        stored = {t: {k: 1.0 for k in sg.FIELDS} for t in t2}
        tab = {"body": "Earth", "t_pot": t2, "points": [dict(stored[t], core_mass_fraction=0.3) for t in t2],
               "triggers": trig, "no_answer": []}
        Path(d, "earth.json").write_text(json.dumps(tab), encoding="utf-8")
        saved = (sg.GRID_DIR, sg._solver, sg._params, sg.RECHECK_POOL, sg.history_bodies)
        sg.GRID_DIR, sg.RECHECK_POOL = Path(d), pool
        sg._solver = lambda b, s0: (Planted(stored), None, None)
        sg._params = lambda v, t, mm: dict(v)
        sg.history_bodies = lambda: []
        sg._READS.clear()                                  # each run's own reads (an earlier run's temp table is not this one's)
        n0 = sg.GUARD_RUNS[0]
        try:
            import contextlib
            import io
            with contextlib.redirect_stdout(io.StringIO()) as buf:
                bad_ = sg.check_all()
        finally:
            sg.GRID_DIR, sg._solver, sg._params, sg.RECHECK_POOL, sg.history_bodies = saved
        return sg.GUARD_RUNS[0] - n0, bad_, buf.getvalue()


for pool in (1, 3):
    n, bad_, out = guard_runs_through_check_all(pool)
    check(f"T6 — check_all 한 번에 GUARD_RUNS +1, 가드 깨끗(풀 {pool})", n == 1 and bad_ == 0, f"+{n} · bad {bad_} · {out.strip()[:300]}")

# ── T7b: RECHECK_POOL unset, empty, and check.sh's step line ────────────────────────────────────────────────────────
for label, env in (("없음", {}), ("빈 값", {"RECHECK_POOL": ""}), ("3", {"RECHECK_POOL": "3"})):
    e = {k: v for k, v in os.environ.items() if k not in ("RECHECK_POOL", "GATE_INNER_POOL")}
    e.update(env)
    p = subprocess.run([sys.executable, "-B", "-c", "import structure_grid as s; print(s.RECHECK_POOL)"], cwd=HERE,
                       env=e, capture_output=True, text=True)
    want = "3" if label == "3" else "1"
    check(f"T7b — RECHECK_POOL {label} (GATE_INNER_POOL 없음): import 가 {want} 를 읽는다",
          p.returncode == 0 and p.stdout.strip() == want, (p.stdout + p.stderr).strip()[-160:])
sh = (HERE.parent / "scripts" / "check.sh").read_text(encoding="utf-8")
check("T7b — check.sh 는 `${RECHECK_POOL:-1}` 을 받아 --check 단계에만 넘긴다",
      '_RECHECK_POOL="${RECHECK_POOL:-1}"' in sh and "unset RECHECK_POOL" in sh
      and 'exec env RECHECK_POOL=${_RECHECK_POOL} python3 structure_grid.py --check' in sh
      and "GATE_INNER_POOL" not in sh.split('_RECHECK_POOL="${RECHECK_POOL:-1}"')[1].split("\n")[0])
block = sh.split("# pooled _recheck (prereg pc/recheck-pool")[1]
block = "#" + block.split("\nfi\n", 1)[0] + "\nfi\n"     # the RECHECK_POOL read, its validation and the GATE_SLOTS check
for label, env, want_rc in (("GATE_SLOTS 21: 4×4+4+1 = 21", {"GATE_SLOTS": "21"}, 0),
                            ("GATE_SLOTS 20: 21 > 20 거절", {"GATE_SLOTS": "20"}, 2),
                            ("RECHECK_POOL 0 거절", {"RECHECK_POOL": "0"}, 2)):
    e = dict(os.environ, GATE_POOL="4", GATE_INNER_POOL="4", RECHECK_POOL="4")
    e.update(env)
    p = subprocess.run(["bash", "-c", "set -euo pipefail\n" + block + "\necho SLOTS-OK"], env=e, capture_output=True,
                       text=True)
    ok = p.returncode == want_rc and (("SLOTS-OK" in p.stdout) == (want_rc == 0))
    check(f"T7b — check.sh 의 자리 검사: {label}", ok, (p.stdout + p.stderr).strip()[-200:])

# ── T1: three real Earth points, pool 1 against pool 3, bit for bit ─────────────────────────────────────────────────
import run  # noqa: E402

earth = json.loads((sg.GRID_DIR / "earth.json").read_text(encoding="utf-8"))
pick = [0, len(earth["t_pot"]) // 2, len(earth["t_pot"]) - 1]
sub = {"t_pot": [earth["t_pot"][i] for i in pick], "points": [earth["points"][i] for i in pick]}
body, _ = run.load_body(sg.BODIES_DIR / "earth.yaml")
real = {}
for pool in (1, 3):
    saved = (sg._params, sg.RECHECK_POOL)
    orig = sg._params
    seen = []
    sg._params = lambda v, t, mm, _o=orig, _s=seen: (lambda out: (_s.append((t, {k: bits(x) for k, x in out.items()})), out)[1])(_o(v, t, mm))
    sg.RECHECK_POOL = pool
    try:
        w, where = sg._recheck(sub, body)
    finally:
        sg._params, sg.RECHECK_POOL = saved
    real[pool] = ((bits(w), where), seen)
    print(f"  [기록] T1 풀 {pool}: 최대 상대 차 {w:.3e} at {where}")
check("T1 — 실제 지구 세 점: 풀 3 의 (차, 자리)가 풀 1 과 비트 같음", real[1][0] == real[3][0], f"{real[1][0]} · {real[3][0]}")
check("T1 — 점마다 여섯 칸이 비트 같음(float.hex)", real[1][1] == real[3][1] and len(real[1][1]) == 3)

print(f"test_recheck_pool: {'통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
