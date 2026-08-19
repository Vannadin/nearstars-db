# J2 C 힘(j2c)과 파이썬 콜백(j2.py)의 궤적 비트-동일성 교차검증.
"""Cross-check the compiled J2 force against the Python callback.

Builds the α Cen moon system twice with the exact manifest-cell parameters
(a=1.6, e=0.1, incl=16°, hypotheticals, J2=0.023, obliquity 5°), integrates one
with the Python force and one with the C force, and compares every particle's
full state (x y z vx vy vz) bitwise at each checkpoint. The C source is compiled
with -ffp-contract=off and mirrors the Python expression line for line, so the
expected result is EXACT equality — any nonzero difference is a fail.

Two passes:
  1. leapfrog, dt = 10 min (the cell this speedup is for; no MEGNO)
  2. ias15 + MEGNO (exercises the particles-array realloc after install —
     init_megno adds variational particles after the force is bound)

Exits nonzero on any mismatch. Also reports the measured speedup.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from run import build, R_JUP_KM  # noqa: E402
from j2 import add_j2  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
KM_PER_AU = 149_597_870.7


def make_sim(use_c: bool):
    os.environ["STAB_J2_C"] = "1" if use_c else "0"
    sim, meta = build("alpha_centauri", ROOT / "hypotheticals" / "alpha_centauri.json",
                      acen_incl=16.0, acen_a=1.6, acen_e=0.1)
    add_j2(sim, meta, "Alpha Centauri A b", 0.023, R_JUP_KM / KM_PER_AU,
           obliquity_deg=5.0)
    assert meta["j2"]["impl"] == ("c" if use_c else "python"), \
        f"wanted {'c' if use_c else 'python'} force, got {meta['j2']['impl']}"
    return sim, meta


def compare_states(sa, sb, label):
    """Bitwise compare every particle's position+velocity. Returns worst |Δ|."""
    worst = 0.0
    for i, (pa, pb) in enumerate(zip(sa.particles, sb.particles)):
        for f in ("x", "y", "z", "vx", "vy", "vz"):
            a, b = getattr(pa, f), getattr(pb, f)
            if a != b:
                worst = max(worst, abs(a - b))
                print(f"  MISMATCH {label} p{i}.{f}: {a!r} != {b!r}")
    return worst


def run_pass(integrator, dt_minutes, years, checkpoints, use_megno):
    print(f"\n== {integrator} dt={dt_minutes} min, {years} yr, "
          f"megno={'on' if use_megno else 'off'} ==")
    sims = {}
    elapsed = {}
    for kind, use_c in (("python", False), ("c", True)):
        sim, meta = make_sim(use_c)
        sim.integrator = integrator
        if dt_minutes:
            sim.dt = dt_minutes / (60.0 * 24.0 * 365.25)
        if use_megno:
            sim.init_megno(seed=42)
        t0 = time.perf_counter()
        for tc in [years * (k + 1) / checkpoints for k in range(checkpoints)]:
            sim.integrate(tc, exact_finish_time=0)  # sim.units = (AU, yr, Msun)
        elapsed[kind] = time.perf_counter() - t0
        sims[kind] = (sim, meta)

    sa, ma = sims["python"]
    sb, mb = sims["c"]
    worst = compare_states(sa, sb, integrator)
    if use_megno:
        mg_a, mg_b = sa.megno(), sb.megno()
        print(f"  MEGNO python={mg_a:.12f} c={mg_b:.12f}")
        if mg_a != mg_b:
            worst = max(worst, abs(mg_a - mg_b))

    # per-moon elements, from the python sim (identical if worst==0)
    for h in ma.get("hypotheticals", []):
        if h.get("type") != "moon":
            continue
        oa = sa.particles[h["name"]].orbit(primary=sa.particles[h["parent"]])
        ob = sb.particles[h["name"]].orbit(primary=sb.particles[h["parent"]])
        print(f"  {h['name']:>24}: a={oa.a:.9f} e={oa.e:.6f} inc={oa.inc:.6f}"
              f"   Δa={ob.a - oa.a:.3e} Δe={ob.e - oa.e:.3e} Δinc={ob.inc - oa.inc:.3e}")

    print(f"  time: python {elapsed['python']:.2f} s, c {elapsed['c']:.2f} s"
          f"  ({elapsed['python'] / max(elapsed['c'], 1e-9):.1f}x)")
    if worst == 0.0:
        print("  PASS — states bitwise identical")
        return True
    print(f"  FAIL — worst |Δ| = {worst:.3e}")
    return False


def main():
    ok = True
    ok &= run_pass("leapfrog", 10.0, 5.0, 5, use_megno=False)
    ok &= run_pass("ias15", None, 2.0, 2, use_megno=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
