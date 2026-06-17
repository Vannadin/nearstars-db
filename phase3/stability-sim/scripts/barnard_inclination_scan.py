# 바너드성 4행성계 Msini→진질량 경계 스캔 — 공면 경사각 i를 낮춰 질량 1/sin(i) 스케일, 불안정해지는 i_crit 도출.
"""Barnard's Star 4-planet (d, b, c, e) coplanar inclination → true-mass boundary scan.

All four planets are RV detections, so the DB carries M·sin i (minimum masses).
The loader feeds those straight in as the i=90° (edge-on) case. The true mass of
each planet is M = M_min / sin i, where i is the (unknown) orbital inclination to
the line of sight. Assuming the system is COPLANAR (a single i shared by all four),
lowering i scales every planet's mass by the same 1/sin(i). This walks the packed
system toward instability and locates the inclination — equivalently the true-mass
multiplier — at which it can no longer survive the 10^4 yr Principia play window.

That is a dynamical UPPER limit on the true masses / LOWER limit on i, the standard
packed-RV-system argument (cf. GJ 876, many Kepler multis).

First pass: single deterministic phase realization (phase_seed=0, matching the rest
of the suite) to LOCATE the boundary. A chaotic boundary is phase-sensitive, so a
multi-seed survival-fraction refinement near i_crit is a documented follow-up, not
done here.

Run: python3 scripts/barnard_inclination_scan.py   (writes results/barnards_star_inclination_scan.json)
"""
import json
import math
import sys
import time
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from run import build, configure_integrator  # noqa: E402

SYSTEM = "barnards_star"
YEARS = 10_000.0       # 10^4 yr Principia play window — matches the suite's canonical horizon
N_CHUNKS = 400
DISRUPT_E = 0.95       # early-stop: orbit crossing / near-unbound → disruption inevitable
RESULTS = SCRIPTS.parent / "results"


def scale_masses(sim, meta, incl_deg):
    """Multiply every planet mass by 1/sin(i) (coplanar true-mass assumption).

    Orbits were fixed at build time; changing m afterwards leaves a/e/phase intact
    and only strengthens the mutual perturbations — exactly the true-mass walk.
    """
    s = math.sin(math.radians(incl_deg))
    factor = 1.0 / s
    for pm in meta["planets"]:
        p = sim.particles[pm["name"]]
        p.m *= factor
    return factor


def scan(incl_deg, years=YEARS, n_chunks=N_CHUNKS, integrator="whfast"):
    sim, meta = build(SYSTEM, None)               # phase_seed=0 deterministic
    factor = scale_masses(sim, meta, incl_deg)
    configure_integrator(sim, meta, integrator)   # whfast=fast screen(+MEGNO); trace=close-encounter re-verify
    star = sim.particles[0]
    names = [pm["name"] for pm in meta["planets"]]

    e_max = {n: 0.0 for n in names}
    a_span = {n: [math.inf, 0.0] for n in names}
    disrupt_t, disrupt_body = None, None
    for k in range(1, n_chunks + 1):
        t = years * k / n_chunks
        sim.integrate(t, exact_finish_time=0)
        for n in names:
            orb = sim.particles[n].orbit(primary=star)
            av, ev = orb.a, orb.e
            e_max[n] = max(e_max[n], ev)
            a_span[n][0] = min(a_span[n][0], av)
            a_span[n][1] = max(a_span[n][1], av)
            if ev >= DISRUPT_E or av <= 0:
                disrupt_t, disrupt_body = t, n
                break
        if disrupt_t is not None:
            break

    sys_e_max = max(e_max.values())
    survives = (sys_e_max < 0.9) and disrupt_t is None
    # a_max/a_min ≥ 10× on any body is the suite's other instability flag
    a_blow = any(sp[0] > 0 and sp[1] / sp[0] >= 10.0 for sp in a_span.values())
    survives = survives and not a_blow
    megno = (sim.megno() if (meta.get("megno_enabled") and disrupt_t is None)
             else float("nan"))

    # heaviest true mass at this inclination (the most massive planet) in M_earth
    MEARTH_MSUN = 5.9722e24 / 1.98892e30
    masses_me = sorted((pm["mass_msun"] * factor / MEARTH_MSUN) for pm in meta["planets"])
    print(f"i={incl_deg:5.1f}deg  x{factor:5.2f}  Mmax={masses_me[-1]:.2f}Me  "
          f"e_max={sys_e_max:6.3f}  MEGNO={megno:8.3f}  surv={'Y' if survives else 'N'}"
          + (f"  DISRUPT {disrupt_body}@{disrupt_t:.0f}yr" if disrupt_t else ""),
          flush=True)
    return dict(incl_deg=incl_deg, mass_factor=factor, max_mass_mearth=masses_me[-1],
                sys_e_max=sys_e_max, per_body_e_max=e_max, megno=megno,
                survives=survives, disrupt_t=disrupt_t, disrupt_body=disrupt_body)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--integrator", choices=["whfast", "trace", "ias15"], default="whfast")
    ap.add_argument("--grid", default="90,60,40,30,20,15,12,10,8,6",
                    help="comma-separated inclinations (deg)")
    ap.add_argument("--out", default="barnards_star_inclination_scan.json")
    a = ap.parse_args()
    grid = [float(x) for x in a.grid.split(",")]

    t0 = time.time()
    print(f"=== Barnard's Star coplanar inclination → true-mass boundary scan "
          f"({YEARS:.0f} yr, {a.integrator}, phase_seed=0) ===", flush=True)
    rows = [scan(i, integrator=a.integrator) for i in grid]

    # locate the boundary: highest i that fails (largest survivable i below it)
    failed = [r for r in rows if not r["survives"]]
    i_crit = max((r["incl_deg"] for r in failed), default=None)
    payload = {
        "system": "Barnard's star",
        "method": f"coplanar inclination -> true-mass (M = Msini/sin i), {YEARS:.0f} yr {a.integrator}, phase_seed=0",
        "integrator": a.integrator,
        "years": YEARS, "disrupt_e": DISRUPT_E,
        "i_crit_deg": i_crit,
        "note": ("first failing inclination (highest i that does not survive); "
                 "true masses must lie ABOVE this i to keep the system stable"),
        "grid": rows,
        "elapsed_sec": time.time() - t0,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    out = RESULTS / a.out
    with out.open("w") as f:
        json.dump(payload, f, indent=2)
    print(f"\ni_crit (first failing) = {i_crit} deg   elapsed {payload['elapsed_sec']:.0f}s", flush=True)
    print(f"wrote {out}", flush=True)


if __name__ == "__main__":
    main()
