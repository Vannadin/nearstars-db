# 위성 궤도를 과거로 역적분하는 탐침 — "지금 궤도는 어디서 왔나"를 통계적으로만 묻는다.
"""Integrate the α Cen moon system BACKWARD and record when Hades dies.

REBOUND integrates backward simply by making the timestep negative; leapfrog and
IAS15 are both time-symmetric by construction, so this is a supported mode rather
than a trick. What it CANNOT do here is recover actual history: the system's
Lyapunov time is ~1.2e4 yr (moons_accurate summary), so over the 5e4 yr of
interest a trajectory's detail is unrecoverable in either direction — a backward
run explores the same chaotic ensemble rather than retracing the past. A 100-yr
forward-then-backward round trip already loses Hades' orbital PHASE entirely
(it completes ~1e5 orbits per century), while retracing the orbit's shape.

The question this probe CAN answer is statistical, and it is the one that matters
for the design: does Hades also die going backward? If it does, the shipped orbit
is not "a moon that arrived recently and is about to be lost" — it is an
improbable state in both time directions, i.e. simply the wrong orbit. If instead
it survives backward while dying forward, the recent-arrival narrative has legs.

Each realization varies only the initial mean anomaly, which re-rolls the chaotic
trajectory without changing the design. Writes results/backward_probe/summary.json
and prints a table.

  .venv/bin/python scripts/backward_probe.py [--years 1e5] [--phases 140,0,75,215]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from run import build, configure_integrator, R_JUP_KM, KM_PER_AU   # noqa: E402
from j2 import add_j2                                              # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "backward_probe"
HYP = ROOT / "hypotheticals" / "alpha_centauri.json"
R_P_KM = 71492.0            # Polyphemus equatorial radius = the impact surface
ROCHE_R_P = 1.31            # rocky-moon Roche limit, in R_p (design note)


def realization(args) -> dict:
    """One backward run at initial mean anomaly `ma`, `years` into the past."""
    ma, years, direction = args
    hyp = json.loads(HYP.read_text())
    for m in hyp["bodies"]:
        if m["name"] == "Hades":
            m["mean_anomaly_deg"] = ma
    tmp = OUT / f"hyp_ma{ma:g}.json"
    tmp.write_text(json.dumps(hyp, indent=1))

    sim, meta = build("alpha_centauri", tmp, acen_incl=16.0, acen_a=1.6, acen_e=0.1)
    add_j2(sim, meta, "Alpha Centauri A b", 0.023, R_JUP_KM / KM_PER_AU,
           obliquity_deg=5.0)
    configure_integrator(sim, meta, "leapfrog", dt_minutes=10.0)
    sim.dt = math.copysign(sim.dt, direction)      # negative dt = into the past

    planet = sim.particles["Alpha Centauri A b"]
    hades = sim.particles["Hades"]
    q_min = float("inf")
    death_t = None
    n = 2000
    for k in range(1, n + 1):
        t = direction * years * k / n
        sim.integrate(t, exact_finish_time=0)
        o = hades.orbit(primary=planet)
        if o.a <= 0 or o.e >= 1.0:                 # hyperbolic: the post-impact kick
            death_t = abs(sim.t)
            break
        q_rp = o.a * (1 - o.e) * KM_PER_AU / R_P_KM
        q_min = min(q_min, q_rp)
        if q_rp < 1.0:                             # periapsis inside the planet
            death_t = abs(sim.t)
            break
    return {"ma_deg": ma, "direction": "backward" if direction < 0 else "forward",
            "died_yr": death_t, "q_min_rp": None if q_min == float("inf") else q_min}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", type=float, default=1e5)
    ap.add_argument("--phases", default="140,0,75,215",
                    help="initial mean anomalies (deg); 140 is the shipped value")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--both", action="store_true",
                    help="also run the same phases forward, as the control")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    phases = [float(x) for x in a.phases.split(",")]
    jobs = [(ma, a.years, -1.0) for ma in phases]
    if a.both:
        jobs += [(ma, a.years, +1.0) for ma in phases]

    # PROCESSES, not threads: the compiled J2 force keeps its parameters in C
    # file-scope globals, so two simulations sharing one process clobber each
    # other's setup and the callback reads foreign memory (segfault). One
    # simulation per process is the contract — see j2c.py.
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        rows = list(ex.map(realization, jobs))

    (OUT / "summary.json").write_text(json.dumps(rows, indent=1))
    print(f"\n{'direction':10s} {'M0 (deg)':>9s} {'fate':>28s} {'min periapsis':>14s}")
    for r in sorted(rows, key=lambda r: (r["direction"], r["ma_deg"])):
        fate = (f"died at {r['died_yr']:,.0f} yr" if r["died_yr"]
                else f"survived {a.years:,.0f} yr")
        q = f"{r['q_min_rp']:.2f} R_p" if r["q_min_rp"] else "—"
        note = "  (< Roche)" if r["q_min_rp"] and r["q_min_rp"] < ROCHE_R_P else ""
        print(f"{r['direction']:10s} {r['ma_deg']:9.0f} {fate:>28s} {q:>14s}{note}")


if __name__ == "__main__":
    main()
