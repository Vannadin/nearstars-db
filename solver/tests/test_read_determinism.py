# 기록 읽기·풀이의 결정성 시험 — 객체 주소가 다른 프로세스들에서 같은 읽기·같은 답 (곡선 집합의 순회 순서)
"""The assemblage read and a records-on solve give bit-identical results in processes whose object addresses differ.

_read sums the (c′) edge corrections over the curves near the read; iterated as a set of _Curve objects (hashed by
address), the order, and so the sum's last bits, differed between processes, and the answers with them (every repeat of
the four declared states on 0691efdb gave a different answer sha). Read in curve id order now.

Run from the worktree root:  <solver venv>/python -m unittest solver.tests.test_read_determinism
"""
import os
import subprocess
import sys
import unittest

from solver import material_registry as mr

RECORDS = ("silicate_slb_default_bse", "silicate_slb_earth_dmm_wh2005", "silicate_slb_mars_khan2022")
HEAVY = os.environ.get("NEARSTARS_HEAVY") == "1"

#: reads on both sides of every third row of every cut edge, after a process-specific number of allocations (so the
#: curves land at other addresses); prints the sha of the reads' reprs and their count
READS = """
import hashlib, sys
pad = [object() for _ in range(int(sys.argv[1]) * 997)]
from solver import material_registry as mr, material_assemblage as ma
from solver.from_v1 import thaw
reg = mr.load()
h, n = hashlib.sha256(), 0
for rid in %r:
    v = ma.view(thaw(reg.get(rid)), reg.tables[rid], 1600.0)
    junk = [object() for _ in range(int(sys.argv[1]) * 13)]
    for c in v._cut:
        if c.kind != "edge":
            continue
        for r in c.rows[::3]:
            for f in (0.999, 1.001):
                h.update(repr(v.state(r["p_b"] * f, r["t"] + 17.0)).encode())
                n += 1
print(h.hexdigest(), n)
""" % (RECORDS,)

#: a declared state solved with the records on; prints the sha of the whole answer
SOLVE = """
import hashlib, json, sys
from solver import context, from_v1, material_registry as mr, result, solve as sv
reg = mr.load()
got = from_v1.load_v1(f"engine/bodies/{sys.argv[1]}.yaml", registry=reg)
body = got[0] if isinstance(got, tuple) else got
a = sv.solve(body, context.Options(sensitivity_dt=0.0, silicate_records=True), registry=reg)[0]
d = {"type": type(a).__name__, "repr": repr(a)}
print(hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest())
"""


def _shipped():
    reg = mr.load()
    return all(reg.get(r) is not None and r in reg.tables for r in RECORDS)


def _run(code, arg):
    return subprocess.run([sys.executable, "-c", code, str(arg)], capture_output=True, text=True, check=True,
                          env={**os.environ, "OPENBLAS_NUM_THREADS": "1"}).stdout.split()


class Determinism(unittest.TestCase):
    @unittest.skipUnless(_shipped(), "no shipped assemblage records with their tables")
    def test_reads_do_not_depend_on_addresses(self):
        """Four processes, each with its curves at other addresses, read the same 2072-odd points bit for bit
        (with rel as a set they gave four different shas)."""
        outs = [_run(READS, i) for i in (1, 2, 3, 4)]
        self.assertGreater(int(outs[0][1]), 1000)               # the reads ran, on every record
        self.assertEqual(len({o[0] for o in outs}), 1, outs)

    @unittest.skipUnless(HEAVY and _shipped(), "NEARSTARS_HEAVY=1 (two venus solves with the records on, minutes)")
    def test_solve_answer_sha(self):
        """Two processes solve venus's declared state with the records on and give the same answer."""
        outs = [_run(SOLVE, "venus")[0] for _ in range(2)]
        self.assertEqual(outs[0], outs[1])


if __name__ == "__main__":
    unittest.main()
