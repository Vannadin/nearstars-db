# Chaos가 외곽 먼지 고리(test particles)에 실제로 비우는 간극을 N-body로 측정 (E고리 두-ringlet 검증)
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rebound  # noqa: E402
from run import build  # noqa: E402
from load import KM_PER_AU  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
HYP = ROOT / "hypotheticals" / "_ring_sim_moons.json"   # Cassandra + Chaos only

YEARS = 2000.0        # ~38,000 Chaos orbits — long enough for a tiny moon (μ≈7.5e-7) to act
N_TP = 300            # ring test particles
A_MIN_KM = 1_000_000  # ring span to resolve the Chaos gap (1.5M) and its edges
A_MAX_KM = 2_000_000
GOLDEN = math.pi * (3.0 - math.sqrt(5.0))  # deterministic phase spread (no RNG)


def main():
    sim, meta = build("alpha_centauri", HYP, acen_incl=16.0, acen_a=1.6, acen_e=0.1)
    sim.integrator = "trace"

    star = sim.particles[meta["star"]["name"]]
    planet = sim.particles["Alpha Centauri A b"]
    po = planet.orbit(primary=star)
    base_inc, base_Omega = po.inc, po.Omega

    n_massive = sim.N
    a_init = []
    for i in range(N_TP):
        a_km = A_MIN_KM + (A_MAX_KM - A_MIN_KM) * i / (N_TP - 1)
        a_au = a_km / KM_PER_AU
        # re-fetch planet each add: rebound reallocs the particle array on add(),
        # invalidating any held Particle reference (would read m=0 → "Primary has no mass").
        sim.add(primary=sim.particles["Alpha Centauri A b"], a=a_au, e=0.001,
                inc=base_inc, Omega=base_Omega, omega=0.0,
                M=(i * GOLDEN) % (2 * math.pi), m=0.0)
        a_init.append(a_km)
    sim.N_active = n_massive   # test particles feel the moons but perturb nothing
    planet = sim.particles["Alpha Centauri A b"]   # refresh after the add loop

    # innermost massive = Cassandra (P ≈ 4.9 d); 27 steps/orbit
    sim.dt = 5e-4  # yr  (≈ 0.18 d)

    chaos = sim.particles["Chaos"]
    co = chaos.orbit(primary=planet)
    print(f"system: star+planet+Cassandra+Chaos + {N_TP} ring test particles "
          f"({A_MIN_KM/1e3:.0f}k–{A_MAX_KM/1e3:.0f}k km)")
    print(f"Chaos: a={co.a*KM_PER_AU/1e3:.0f}k km e={co.e:.3f}  "
          f"peri={co.a*(1-co.e)*KM_PER_AU/1e3:.0f}k apo={co.a*(1+co.e)*KM_PER_AU/1e3:.0f}k")
    print(f"integrating {YEARS:g} yr (TRACE, dt={sim.dt} yr)…")

    sim.integrate(YEARS)
    planet = sim.particles["Alpha Centauri A b"]   # refresh reference post-integration

    # classify: survivor = still bound to planet AND a within ±15% of start
    bins = 34
    edges = [A_MIN_KM + (A_MAX_KM - A_MIN_KM) * k / bins for k in range(bins + 1)]
    total = [0] * bins
    surv = [0] * bins
    for j in range(N_TP):
        p = sim.particles[n_massive + j]
        a0 = a_init[j]
        b = min(bins - 1, int((a0 - A_MIN_KM) / (A_MAX_KM - A_MIN_KM) * bins))
        total[b] += 1
        try:
            o = p.orbit(primary=planet)
            af = o.a * KM_PER_AU
            ok = (af > 0) and (abs(af - a0) < 0.15 * a0)
        except Exception:
            ok = False
        if ok:
            surv[b] += 1

    print("\n a_init (k km) | survival            | frac")
    cleared_lo = cleared_hi = None
    for k in range(bins):
        c = (edges[k] + edges[k + 1]) / 2 / 1e3
        frac = surv[k] / total[k] if total[k] else 0.0
        bar = "#" * int(round(frac * 20))
        print(f"  {c:7.0f}     | {bar:<20} | {frac:4.2f}")
        if frac < 0.25:
            if cleared_lo is None:
                cleared_lo = edges[k]
            cleared_hi = edges[k + 1]

    K = 2.5
    rh = co.a * (5.4e20 / (3 * 120 * 5.972e24)) ** (1 / 3) * KM_PER_AU
    an_lo = co.a * (1 - co.e) * KM_PER_AU - K * rh
    an_hi = co.a * (1 + co.e) * KM_PER_AU + K * rh
    print(f"\nanalytic gap (swept ± {K}·R_Hill, R_Hill={rh/1e3:.0f}k): "
          f"[{an_lo/1e3:.0f}k, {an_hi/1e3:.0f}k]  width {(an_hi-an_lo)/1e3:.0f}k km")
    if cleared_lo is not None:
        print(f"measured cleared gap (survival<25%): "
              f"[{cleared_lo/1e3:.0f}k, {cleared_hi/1e3:.0f}k]  width {(cleared_hi-cleared_lo)/1e3:.0f}k km")
    else:
        print("measured cleared gap: none (ring not cleared)")


if __name__ == "__main__":
    main()
