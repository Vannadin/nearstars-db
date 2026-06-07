# alpha Cen A b 경계 재도출 스캔 — dt 버그 수정 후 IAS15로 q/Q·e_max·MEGNO 재계산.
"""Re-derive the alpha Cen A b stability boundaries with IAS15 (post dt-fix).

The audit found the prior boundary numbers came from TRACE runs corrupted by the
configure_integrator dt bug AND TRACE's own inaccuracy on this secular (not
close-encounter) problem; the inclination range was also read off the wrong
e=0.4 case. This re-runs every boundary case with IAS15 (adaptive, dt-independent,
|dE/E|~1e-13 here) and computes periastron q / apastron Q from the orbit so the
HZ-confinement and survival verdicts are exact.

Each case integrates in chunks and early-stops once e>=0.95 (disruption is then
inevitable and the deep-periastron plunge would crawl IAS15) — the break time is
recorded as the disruption onset. Output flushes per line so a kill keeps it.

HZ (conservative, alpha Cen A): 1.18 <= a*(1+-e) <= 2.05 AU.
Star A radius (disruption floor): 0.00569 AU (1.2234 R_sun).
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from run import build, configure_integrator  # noqa: E402

HZ_INNER, HZ_OUTER = 1.18, 2.05
STAR_A_RADIUS_AU = 0.00569
PLANET = "Alpha Centauri A b"


def scan(label, a, e, i_mut, years=100_000, n_chunks=400):
    sim, meta = build("alpha_centauri", None, acen_incl=i_mut, acen_a=a, acen_e=e)
    configure_integrator(sim, meta, "ias15")
    star = sim.particles[0]
    planet = sim.particles[PLANET]

    q_min, Q_max, e_max, a_min, a_max = float("inf"), 0.0, 0.0, float("inf"), 0.0
    disrupt_t = None
    for k in range(1, n_chunks + 1):
        t = years * k / n_chunks
        sim.integrate(t, exact_finish_time=0)
        orb = planet.orbit(primary=star)
        av, ev = orb.a, orb.e
        q, Q = av * (1 - ev), av * (1 + ev)
        q_min = min(q_min, q); Q_max = max(Q_max, Q)
        e_max = max(e_max, ev); a_min = min(a_min, av); a_max = max(a_max, av)
        if ev >= 0.95 or av <= 0 or q < STAR_A_RADIUS_AU:
            disrupt_t = t
            break

    hz_confined = (q_min >= HZ_INNER) and (Q_max <= HZ_OUTER) and disrupt_t is None
    survives = (e_max < 0.9) and disrupt_t is None
    megno = sim.megno() if disrupt_t is None else float("nan")
    print(f"{label:30s} a={a:.3f} e={e:.3f} i={i_mut:4.0f}  "
          f"e_max={e_max:6.3f} q={q_min:6.3f} Q={Q_max:6.3f} "
          f"MEGNO={megno:6.3f} HZ={'Y' if hz_confined else 'n'} "
          f"surv={'Y' if survives else 'N'}"
          + (f" DISRUPT@{disrupt_t:.0f}yr" if disrupt_t else ""),
          flush=True)
    return dict(label=label, a=a, e=e, i=i_mut, e_max=e_max, q_min=q_min,
                Q_max=Q_max, megno=megno, hz=hz_confined, survives=survives,
                disrupt_t=disrupt_t)


def main():
    print("=== ADOPTED + reference ===", flush=True)
    scan("adopted a1.6 e0.1 i16", 1.6, 0.1, 16)

    print("\n=== INNER EDGE (e=0.1, i=16) ===", flush=True)
    for a in [1.20, 1.30, 1.34, 1.36, 1.38, 1.40, 1.45, 1.50]:
        scan(f"a={a:.2f}", a, 0.1, 16)

    print("\n=== OUTER EDGE (e=0.1, i=16) ===", flush=True)
    for a in [2.00, 2.50, 3.00, 3.10, 3.20, 3.30, 3.50]:
        scan(f"a={a:.2f}", a, 0.1, 16)

    print("\n=== ECCENTRICITY BOUND (a=1.6, i=16) ===", flush=True)
    for e in [0.15, 0.18, 0.20, 0.22, 0.25]:
        scan(f"e={e:.2f}", 1.6, e, 16)

    print("\n=== INCLINATION BOUND at adopted e=0.1 (a=1.6) ===", flush=True)
    for i in [25, 30, 33, 35, 40, 42, 45, 50]:
        scan(f"i={i}", 1.6, 0.1, i)

    print("\n=== CANON a=1.2 with PINNED i (e=0.1) ===", flush=True)
    for i in [0, 16, 30]:
        scan(f"canon a1.2 i={i}", 1.2, 0.1, i)

    print("\n=== OBSERVED ORBIT (e=0.4, i=50) disruption timescale, to 3e5 yr ===", flush=True)
    scan("observed e0.4 i50", 1.6, 0.4, 50, years=300_000, n_chunks=1500)


if __name__ == "__main__":
    main()
