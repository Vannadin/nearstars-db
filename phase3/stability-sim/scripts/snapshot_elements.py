# 500년 적분 후 osculating 궤도요소 스냅샷 추출 — 보드 orbit emit-shaping용 (final32b+massB 구성; 결과 results/_snapshot500/elements.log)
"""Integrate the adopted alpha Cen A b moon system 500 yr (TRACE + J2, same recipe
as results/_final32b but with the gated Pandora mass 3.85e24) and print each body's
osculating elements at t=500 yr in the board's frame conventions:

  - moons:      z' = Polyphemus orbital-plane normal (t=500), x' = ascending-node
                line of Polyphemus's plane on the AB plane  -> inc/lan vs parent plane
  - Polyphemus: z  = AB orbital-plane normal, x = instantaneous A->B direction
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import numpy as np
import rebound
from run import build, configure_integrator, KM_PER_AU
from j2 import add_j2, R_JUP_KM

HYP = Path(__file__).parent.parent / "results/_snapshot500/alpha_centauri_massB_input.json"

sim, meta = None, None
res = build("alpha_centauri", HYP, acen_incl=16.0, acen_a=1.6, acen_e=0.1)
sim, meta = (res if isinstance(res, tuple) else (res, None))
if meta is None:
    raise SystemExit("build() did not return (sim, meta) — inspect run.py")

r_eq_au = 1.0 * R_JUP_KM / KM_PER_AU
add_j2(sim, meta, "Alpha Centauri A b", 0.023, r_eq_au, obliquity_deg=0.0)
meta["megno_enabled"] = False
configure_integrator(sim, meta, "trace")

import time
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

# AB plane normal + A->B in-plane x-axis
r_ba, v_ba = rB - rA, vB - vA
n_ab = np.cross(r_ba, v_ba); n_ab /= np.linalg.norm(n_ab)
x_ab = r_ba - np.dot(r_ba, n_ab) * n_ab; x_ab /= np.linalg.norm(x_ab)
y_ab = np.cross(n_ab, x_ab)

# Polyphemus plane normal (orbit about A) + mutual node line on the AB plane
r_pa, v_pa = rP - rA, vP - vA
n_p = np.cross(r_pa, v_pa); n_p /= np.linalg.norm(n_p)
node = np.cross(n_ab, n_p)
if np.linalg.norm(node) < 1e-12:
    node = x_ab
node /= np.linalg.norm(node)
mutual_inc = math.degrees(math.acos(np.clip(np.dot(n_ab, n_p), -1, 1)))

def elements(r_rel, v_rel, m_primary, m_body, zhat, xhat):
    """Osculating elements of (r_rel, v_rel) in the frame (xhat, yhat, zhat)."""
    yhat = np.cross(zhat, xhat)
    R = np.vstack([xhat, yhat, zhat])          # world -> frame
    r = R @ r_rel; v = R @ v_rel
    tmp = rebound.Simulation()
    tmp.G = sim.G
    tmp.add(m=m_primary)
    tmp.add(m=m_body, x=r[0], y=r[1], z=r[2], vx=v[0], vy=v[1], vz=v[2])
    o = tmp.particles[1].orbit(primary=tmp.particles[0])
    deg = lambda x: (math.degrees(x) % 360.0)
    return dict(a_km=o.a * KM_PER_AU, e=o.e, inc_deg=math.degrees(o.inc),
                lan_deg=deg(o.Omega), argp_deg=deg(o.omega), ma_deg=deg(o.M))

print(f"\n# t = {sim.t:.3f} yr snapshot  (mutual inc Polyphemus vs AB plane: {mutual_inc:.3f} deg)")
print("# Polyphemus (frame: AB plane, x = A->B direction at t=500)")
el = elements(r_pa, v_pa, A.m, P.m, n_ab, x_ab)
print(f"Polyphemus  a_au={el['a_km']/KM_PER_AU:.6f} e={el['e']:.5f} inc={el['inc_deg']:.3f} "
      f"lan={el['lan_deg']:.2f} argp={el['argp_deg']:.2f} ma={el['ma_deg']:.2f}")

print("# Moons (frame: Polyphemus orbital plane, x = mutual node line on AB plane)")
for name in ["Dante", "Hades", "Pandora", "Cassandra", "Chaos"]:
    M = sim.particles[name]
    rM, vM = vec(M)
    el = elements(rM - rP, vM - vP, P.m, M.m, n_p, node)
    print(f"{name:<10} a_km={el['a_km']:.1f} e={el['e']:.5f} inc={el['inc_deg']:.3f} "
          f"lan={el['lan_deg']:.2f} argp={el['argp_deg']:.2f} ma={el['ma_deg']:.2f}")
