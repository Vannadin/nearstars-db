# 행성 J2 편평도 섭동을 rebound additional_forces 로 주입 (reboundx 미사용, rebound 5.x 호환).
from __future__ import annotations

import math

import rebound

R_JUP_KM = 71_492.0  # Jupiter equatorial radius (IAU nominal)


def _orbit_normal(inc: float, Omega: float) -> tuple[float, float, float]:
    """Unit angular-momentum (orbit-normal) vector for inclination/node (rad)."""
    return (
        math.sin(inc) * math.sin(Omega),
        -math.sin(inc) * math.cos(Omega),
        math.cos(inc),
    )


def _index_of(sim: rebound.Simulation, name: str) -> int:
    """Integer index of a named particle (order is fixed during these runs)."""
    return sim.particles[name].index


def add_j2(sim: rebound.Simulation, meta: dict, body_name: str, j2: float,
           r_eq_au: float, axis: tuple[float, float, float] | None = None,
           obliquity_deg: float = 0.0):
    """Register a J2 oblateness force for `body_name` acting on its moons.

    The J2 symmetry (spin) axis defaults to the body's orbit-normal — i.e. zero
    obliquity, the bulge plane coincides with the moons' reference plane (moons
    are added relative to the parent's orbital plane in load.add_hypotheticals).
    `obliquity_deg` tilts the spin axis by that angle about the body's orbital
    node line (so the equatorial plane = orbital plane inclined by the obliquity);
    a moon set to inclination_deg = obliquity_deg then sits exactly in the tilted
    equatorial plane (its natural Laplace plane if it is inside the Laplace radius).
    Pass `axis` to override with an explicit spin direction in the sim frame.

    Applied to real particles only; MEGNO's variational particles do not feel J2,
    so MEGNO reflects point-mass chaos — the moon verdict rests on Hill-fraction +
    a/e drift, which are measured from the real orbits and ARE J2-aware.
    """
    body_index = _index_of(sim, body_name)
    star = sim.particles[meta["star"]["name"]]
    if axis is None:
        o = sim.particles[body_name].orbit(primary=star)
        # tilt the spin axis by the obliquity about the orbital node = orbit normal
        # taken at inclination (o.inc + obliquity); zero obliquity → plain orbit normal.
        axis = _orbit_normal(o.inc + math.radians(obliquity_deg), o.Omega)
    norm = math.sqrt(sum(c * c for c in axis))
    ax, ay, az = (c / norm for c in axis)

    moon_idx = [
        _index_of(sim, h["name"])
        for h in meta.get("hypotheticals", [])
        if h.get("parent") == body_name and h.get("type") == "moon"
    ]
    if not moon_idx:
        raise ValueError(f"no moons parented to '{body_name}' — nothing for J2 to act on")

    G = sim.G

    def force(reb_sim):
        s = reb_sim.contents
        ps = s.particles
        pl = ps[body_index]
        mu = G * pl.m
        c0 = 1.5 * j2 * mu * r_eq_au * r_eq_au
        px, py, pz = pl.x, pl.y, pl.z
        rbx = rby = rbz = 0.0  # back-reaction force accumulator
        for i in moon_idx:
            m = ps[i]
            dx, dy, dz = m.x - px, m.y - py, m.z - pz
            r2 = dx * dx + dy * dy + dz * dz
            r = math.sqrt(r2)
            zeta = dx * ax + dy * ay + dz * az  # r·n̂
            zr = zeta / r
            common = c0 / (r2 * r2)
            f_rhat = 1.0 - 5.0 * zr * zr
            amx = -common * (f_rhat * dx / r + 2.0 * zr * ax)
            amy = -common * (f_rhat * dy / r + 2.0 * zr * ay)
            amz = -common * (f_rhat * dz / r + 2.0 * zr * az)
            m.ax += amx
            m.ay += amy
            m.az += amz
            rbx += m.m * amx
            rby += m.m * amy
            rbz += m.m * amz
        if pl.m > 0:
            pl.ax -= rbx / pl.m
            pl.ay -= rby / pl.m
            pl.az -= rbz / pl.m

    sim.additional_forces = force
    sim.force_is_velocity_dependent = 0
    meta["j2"] = {"body": body_name, "J2": j2, "r_eq_au": r_eq_au,
                  "axis": [ax, ay, az], "_force_ref": force}  # ref pins the closure
    return force
