# 궤적을 순방향 스윕해 행성 하늘 투영 PA가 관측값(83.5°)에 최근접인 시점 t*를 찾고, 그 상태를 1950 게임 에포크로 되감아 emit 궤도요소 산출 — orbit 방향 정합용
"""Find the epoch t* whose SKY-projected position angle of the planet best matches the
JWST/MIRI Aug-2024 detection (PA = 83.5 deg E of N; Beichman et al. 2025, arXiv:2508.03814
Table 2 S1), then quote the matched orbit at the game solar-system epoch (JD 2433282.5 =
1950.0) by rewinding the mean anomaly. Output = planet + 5 moons osculating elements in
the board frame (same conventions as snapshot_elements.py).

Sky frame: the alpha_centauri build() is sky-anchored (load.py feeds the binary
i/Omega/omega verbatim from the J2000 visual-binary solution), so REBOUND's reference
x-y plane = plane of the sky, z = Earth line of sight. Convention: +x = North, +y = East,
PA = atan2(East, North).

Only DIRECTION is matched: along PA 83.5 the adopted 1.6 AU / e=0.1 orbit reaches only
~0.8 AU projected (< observed ~2.0 AU) because that PA is near the minor axis of the
projected ellipse (major axis lies along the real binary node, Omega=204.85). Accepted
by design (owner decision) and documented.

Integration is FORWARD-ONLY (TRACE + J2 is symplectic; non-monotonic integrate() calls
corrupt the state). The emit state is read from a FRESH build integrated once to t*.
"""
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import numpy as np
import rebound
from run import build, configure_integrator, KM_PER_AU
from j2 import add_j2, R_JUP_KM

HYP = Path(__file__).parent.parent / "results/_snapshot500/alpha_centauri_massB_input.json"

OBS_PA_DEG = 83.5
DIST_PC = 1.3474909718104888
DT_SCAN = 0.005            # yr, forward-only fine scan
T_END = 8.0               # yr — crossing near the epoch (least precession drift)

OBS_JD = 2460532.5        # 2024-08-10 (JWST/MIRI detection)
EPOCH_JD = 2433282.5      # game solar-system epoch = 1950.0
DELTA_YR = (OBS_JD - EPOCH_JD) / 365.25   # 74.60 yr


def make_sim():
    res = build("alpha_centauri", HYP, acen_incl=16.0, acen_a=1.6, acen_e=0.1)
    sim, meta = (res if isinstance(res, tuple) else (res, None))
    if meta is None:
        raise SystemExit("build() did not return (sim, meta)")
    add_j2(sim, meta, "Alpha Centauri A b", 0.023, 1.0 * R_JUP_KM / KM_PER_AU, obliquity_deg=0.0)
    meta["megno_enabled"] = False
    configure_integrator(sim, meta, "trace")
    return sim


def vec(p):
    return np.array([p.x, p.y, p.z]), np.array([p.vx, p.vy, p.vz])


def sky_pa_sep(r_rel):
    north, east = r_rel[0], r_rel[1]
    return math.degrees(math.atan2(east, north)) % 360.0, math.hypot(north, east)


def pa_diff(a, b):
    d = abs((a - b) % 360.0)
    return min(d, 360.0 - d)


# --- Phase 1: forward-only scan for the best PA match near the epoch ---
sim = make_sim()
A = sim.particles["Alpha Centauri A"]; P = sim.particles["Alpha Centauri A b"]
best = None  # (err, t, pa, sep)
t0 = time.time()
nstep = int(round(T_END / DT_SCAN))
for k in range(1, nstep + 1):
    t = DT_SCAN * k
    sim.integrate(t)
    pa, sep = sky_pa_sep(vec(P)[0] - vec(A)[0])
    err = pa_diff(pa, OBS_PA_DEG)
    if best is None or err < best[0] - 1e-9:
        best = (err, t, pa, sep)
t_star = best[1]
print(f"# scan {T_END:g} yr @ dt={DT_SCAN}  ({time.time()-t0:.0f}s)")
print(f"# BEST MATCH  t* = {t_star:.4f} yr   sky PA = {best[2]:.3f} deg  (obs 83.5, err {best[0]:.3f})")
print(f"#   projected sep = {best[3]:.4f} AU = {best[3]/DIST_PC:.4f} arcsec"
      f"   (obs 2.03 AU / 1.51 arcsec — direction-only; sep short by design)")

# --- Phase 2: fresh build, single forward integrate to t*, read emit state ---
sim = make_sim()
sim.integrate(t_star)
A = sim.particles["Alpha Centauri A"]; B = sim.particles["Alpha Centauri B"]
P = sim.particles["Alpha Centauri A b"]
rA, vA = vec(A); rB, vB = vec(B); rP, vP = vec(P)

# self-check at t*: recompute sky PA matches Phase 1
pa_chk, sep_chk = sky_pa_sep(rP - rA)
print(f"# self-check sky PA at t* (fresh build) = {pa_chk:.3f} deg, sep = {sep_chk:.4f} AU")

r_ba, v_ba = rB - rA, vB - vA
n_ab = np.cross(r_ba, v_ba); n_ab /= np.linalg.norm(n_ab)
x_ab = r_ba - np.dot(r_ba, n_ab) * n_ab; x_ab /= np.linalg.norm(x_ab)
r_pa, v_pa = rP - rA, vP - vA
n_p = np.cross(r_pa, v_pa); n_p /= np.linalg.norm(n_p)
node = np.cross(n_ab, n_p)
if np.linalg.norm(node) < 1e-12:
    node = x_ab
node /= np.linalg.norm(node)
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


el = elements(r_pa, v_pa, A.m, P.m, n_ab, x_ab)
P_yr = 2 * math.pi / P.orbit(primary=A).n          # sidereal period about A
ma_obs = el['ma_deg']
ma_1950 = (ma_obs - 360.0 * DELTA_YR / P_yr) % 360.0

print(f"\n# t* snapshot  (mutual inc Polyphemus vs AB plane: {mutual_inc:.3f} deg)")
print(f"# epoch rewind: period about A = {P_yr:.5f} yr; rewind {DELTA_YR:.3f} yr "
      f"= {DELTA_YR/P_yr:.3f} orbits (obs 2024 -> game epoch 1950)")
print(f"# ma_obs (2024) = {ma_obs:.2f} deg  ->  ma_1950 (EMIT) = {ma_1950:.2f} deg")
print("# Polyphemus (frame: AB plane, x = A->B direction at t*)")
print(f"Polyphemus  a_au={el['a_km']/KM_PER_AU:.6f} e={el['e']:.5f} inc={el['inc_deg']:.3f} "
      f"lan={el['lan_deg']:.2f} argp={el['argp_deg']:.2f} ma_2024={ma_obs:.2f} ma_1950={ma_1950:.2f}")

print("# Moons (frame: Polyphemus orbital plane, x = mutual node line on AB plane)")
for name in ["Dante", "Hades", "Pandora", "Cassandra", "Chaos"]:
    M = sim.particles[name]
    rM, vM = vec(M)
    el = elements(rM - rP, vM - vP, P.m, M.m, n_p, node)
    print(f"{name:<10} a_km={el['a_km']:.1f} e={el['e']:.5f} inc={el['inc_deg']:.3f} "
          f"lan={el['lan_deg']:.2f} argp={el['argp_deg']:.2f} ma={el['ma_deg']:.2f}")
