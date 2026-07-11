# 전 바디 J2(폴리페무스+위성 5 각자 축) 500yr 스냅샷 — 위성 지오이드 감도 + 적분기 교차확인용
"""Same 500-yr snapshot recipe, but EVERY figure body carries its ledgered J2
(figure/values.md): Polyphemus 0.023 + per-moon phi-scaled J2, each about its own
spin axis (locked moons = own orbit normal; Chaos tilted 15 deg per the board).
argv: [integrator] [dt_minutes] — e.g. `trace` or `leapfrog 10`.
"""
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, "/Users/vana/Desktop/NearStars/phase3/stability-sim/scripts")
import numpy as np
import rebound
from run import build, configure_integrator, KM_PER_AU
from j2 import _orbit_normal

HYP = Path("/Users/vana/Desktop/NearStars/phase3/stability-sim/results/_snapshot500/alpha_centauri_massB_input.json")

# (name, J2 phi-scaled, R_eq km, obliquity deg about own node) — figure/values.md ledger
FIGURES = [
    ("Alpha Centauri A b", 0.023,   71492.0, 0.0),
    ("Dante",              0.039,     900.0, 0.0),
    ("Hades",              0.013,     750.0, 0.0),
    ("Pandora",            2.06e-3,  5724.0, 0.0),
    ("Cassandra",          4.1e-4,   3400.0, 0.0),
    ("Chaos",              0.026,     400.0, 15.0),
]
SUBSYSTEM = [n for n, *_ in FIGURES]

sim, meta = build("alpha_centauri", HYP, acen_incl=16.0, acen_a=1.6, acen_e=0.1)
meta["megno_enabled"] = False

# spin axes at t=0: Polyphemus about A, moons about Polyphemus (locked -> orbit normal)
A0 = sim.particles["Alpha Centauri A"]
P0 = sim.particles["Alpha Centauri A b"]
sources = []
for name, j2v, r_km, obl in FIGURES:
    p = sim.particles[name]
    o = p.orbit(primary=(A0 if name == "Alpha Centauri A b" else P0))
    ax = _orbit_normal(o.inc + math.radians(obl), o.Omega)
    n = math.sqrt(sum(c * c for c in ax))
    sources.append((p.index, j2v, (r_km / KM_PER_AU) ** 2, tuple(c / n for c in ax)))
idx = [sim.particles[n].index for n in SUBSYSTEM]
G = sim.G

def force(reb_sim):
    s = reb_sim.contents
    ps = s.particles
    for si, j2v, r2eq, (ax, ay, az) in sources:
        src = ps[si]
        c0 = 1.5 * j2v * G * src.m * r2eq
        px, py, pz = src.x, src.y, src.z
        rbx = rby = rbz = 0.0
        for ti in idx:
            if ti == si:
                continue
            t = ps[ti]
            dx, dy, dz = t.x - px, t.y - py, t.z - pz
            r2 = dx * dx + dy * dy + dz * dz
            r = math.sqrt(r2)
            zr = (dx * ax + dy * ay + dz * az) / r
            common = c0 / (r2 * r2)
            f_rhat = 1.0 - 5.0 * zr * zr
            amx = -common * (f_rhat * dx / r + 2.0 * zr * ax)
            amy = -common * (f_rhat * dy / r + 2.0 * zr * ay)
            amz = -common * (f_rhat * dz / r + 2.0 * zr * az)
            t.ax += amx; t.ay += amy; t.az += amz
            rbx += t.m * amx; rby += t.m * amy; rbz += t.m * amz
        if src.m > 0:
            src.ax -= rbx / src.m; src.ay -= rby / src.m; src.az -= rbz / src.m

sim.additional_forces = force
sim.force_is_velocity_dependent = 0

integrator = sys.argv[1] if len(sys.argv) > 1 else "trace"
dt_minutes = float(sys.argv[2]) if len(sys.argv) > 2 else None
print(f"# integrator = {integrator}" + (f" (fixed dt {dt_minutes} min)" if dt_minutes else "")
      + " | J2 sources: all 6 figure bodies", flush=True)
configure_integrator(sim, meta, integrator, dt_minutes=dt_minutes)

t0 = time.time()
for chunk in range(1, 21):
    sim.integrate(500.0 * chunk / 20)
    print(f"  ... {500*chunk/20:.0f} yr  elapsed {time.time()-t0:.0f}s", flush=True)

def vec(p):
    return np.array([p.x, p.y, p.z]), np.array([p.vx, p.vy, p.vz])

A = sim.particles["Alpha Centauri A"]
B = sim.particles["Alpha Centauri B"]
P = sim.particles["Alpha Centauri A b"]
rA, vA = vec(A); rB, vB = vec(B); rP, vP = vec(P)

r_ba, v_ba = rB - rA, vB - vA
n_ab = np.cross(r_ba, v_ba); n_ab /= np.linalg.norm(n_ab)
x_ab = r_ba - np.dot(r_ba, n_ab) * n_ab; x_ab /= np.linalg.norm(x_ab)

r_pa, v_pa = rP - rA, vP - vA
n_p = np.cross(r_pa, v_pa); n_p /= np.linalg.norm(n_p)
node = np.cross(n_ab, n_p)
node = node / np.linalg.norm(node) if np.linalg.norm(node) > 1e-12 else x_ab
mutual_inc = math.degrees(math.acos(np.clip(np.dot(n_ab, n_p), -1, 1)))

def elements(r_rel, v_rel, m_primary, m_body, zhat, xhat):
    yhat = np.cross(zhat, xhat)
    R = np.vstack([xhat, yhat, zhat])
    r = R @ r_rel; v = R @ v_rel
    tmp = rebound.Simulation()
    tmp.G = sim.G
    tmp.add(m=m_primary)
    tmp.add(m=m_body, x=r[0], y=r[1], z=r[2], vx=v[0], vy=v[1], vz=v[2])
    o = tmp.particles[1].orbit(primary=tmp.particles[0])
    deg = lambda x: (math.degrees(x) % 360.0)
    return dict(a_km=o.a * KM_PER_AU, e=o.e, inc_deg=math.degrees(o.inc),
                lan_deg=deg(o.Omega), argp_deg=deg(o.omega), ma_deg=deg(o.M))

print(f"\n# t = {sim.t:.3f} yr snapshot  (mutual inc: {mutual_inc:.3f} deg)")
el = elements(r_pa, v_pa, A.m, P.m, n_ab, x_ab)
print(f"Polyphemus  a_au={el['a_km']/KM_PER_AU:.6f} e={el['e']:.5f} inc={el['inc_deg']:.3f} "
      f"lan={el['lan_deg']:.2f} argp={el['argp_deg']:.2f} ma={el['ma_deg']:.2f}")
for name in ["Dante", "Hades", "Pandora", "Cassandra", "Chaos"]:
    M = sim.particles[name]
    rM, vM = vec(M)
    el = elements(rM - rP, vM - vP, P.m, M.m, n_p, node)
    print(f"{name:<10} a_km={el['a_km']:.1f} e={el['e']:.5f} inc={el['inc_deg']:.3f} "
          f"lan={el['lan_deg']:.2f} argp={el['argp_deg']:.2f} ma={el['ma_deg']:.2f}")
