# DB JSON → REBOUND Simulation 로더. 단위: AU / yr / Msun (G = 4π²).
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import rebound

KM_PER_AU = 149_597_870.7
SEC_PER_YR = 365.25 * 86400.0
MSUN_KG = 1.98892e30
MEARTH_KG = 5.9722e24
G_SI = 6.67430e-11
MU_SUN_KM3_S2 = G_SI * MSUN_KG / 1e9  # km^3 / s^2


def mu_km3s2_to_msun(mu: float) -> float:
    return mu / MU_SUN_KM3_S2


def mearth_to_msun(m_earth: float) -> float:
    return m_earth * MEARTH_KG / MSUN_KG


def hill_radius(a: float, m: float, M: float) -> float:
    """Hill radius in same length units as `a`. m, M same mass units."""
    return a * (m / (3.0 * M)) ** (1.0 / 3.0)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open() as f:
        return json.load(f)


def _planet_mass_msun(planet: dict) -> tuple[float, str]:
    """Return (mass_msun, mass_kind). mass_kind ∈ {true, msini}."""
    # physical may be a list of measurements or a single collapsed dict in
    # db/systems (mirror _planet_orbital's list/dict handling below).
    phys = planet.get("curated", {}).get("physical")
    if isinstance(phys, list):
        rec = next((p for p in phys if p.get("recommended")), phys[-1] if phys else None)
    elif isinstance(phys, dict):
        rec = phys
    else:
        rec = None
    if rec is None:
        raise ValueError(f"No physical entry for {planet['name']}")
    if rec.get("true_mass_mearth") is not None:
        return mearth_to_msun(rec["true_mass_mearth"]), "true"
    if rec.get("mass_mearth") is not None:
        return mearth_to_msun(rec["mass_mearth"]), rec.get("mass_type", "msini").lower()
    raise ValueError(f"No mass on recommended physical for {planet['name']}")


def _planet_orbital(planet: dict, star_m_msun: float | None = None,
                    rng: "random.Random | None" = None,
                    ecc_override: float | None = None) -> dict[str, float]:
    """Return semi-major axis (AU), eccentricity, inclination (rad), omega, Omega, M (rad).

    Phases that are null in the DB get a deterministic random fill — required because
    REBOUND's default-0 would line every planet up at the same heliocentric longitude,
    creating an unphysical initial conjunction that spawns spurious chaos.
    """
    import random
    rng = rng or random.Random(0)

    curated = planet.get("curated", {}).get("orbital")
    raw = planet.get("raw", {})

    if isinstance(curated, list):
        rec = next((o for o in curated if o.get("recommended")), curated[-1])
    elif isinstance(curated, dict):
        rec = curated
    else:
        rec = {}

    a_au = rec.get("semi_major_axis_au") or raw.get("semi_major_axis_au")
    if a_au is None:
        # TTV/RV planets may record only a period (e.g. AU Mic d, e). Derive a
        # exactly via Kepler III in (AU, yr, Msun) units: a³ = M · P_yr².
        period_days = rec.get("period_days") or raw.get("period_days")
        if period_days is not None and star_m_msun is not None:
            p_yr = period_days / 365.25
            a_au = (star_m_msun * p_yr * p_yr) ** (1.0 / 3.0)
        else:
            raise ValueError(f"No semi-major axis or period for {planet['name']}")

    e = rec.get("eccentricity")
    if e is None:
        e = raw.get("eccentricity", 0.0) or 0.0
    if ecc_override is not None:
        e = ecc_override   # downstream adopted-config override (DB keeps the measured value)

    inc = rec.get("inclination_deg") or raw.get("inclination_deg")
    inc_rad = 0.0 if inc is None else math.radians(inc - 90.0)
    # Most transit-fit inclinations are ~89.7°. For stability we only care
    # about MUTUAL inclinations; subtract 90° so transiting coplanar set ≈ 0.

    omega_deg = raw.get("omega_deg")
    omega_rad = math.radians(omega_deg) if omega_deg is not None else rng.uniform(0, 2 * math.pi)

    M_deg = rec.get("mean_anomaly_at_epoch_deg")
    M_rad = math.radians(M_deg) if M_deg is not None else rng.uniform(0, 2 * math.pi)

    Omega_rad = rng.uniform(0, 2 * math.pi)  # node not constrained for transiting set

    return {
        "a": float(a_au),
        "e": float(e),
        "inc": inc_rad,
        "omega": omega_rad,
        "Omega": Omega_rad,
        "M": M_rad,
    }


def build_planetary_system(db_path: Path, phase_seed: int = 0,
                           ecc_override: float | None = None) -> tuple[rebound.Simulation, dict]:
    """Build a single-star + N-planet REBOUND simulation."""
    import random
    rng = random.Random(phase_seed)

    d = _load_json(db_path)
    star = d["stars"][0]
    star_name = star["name"]
    star_mu = star["principia"]["gravitational_parameter_km3_s2"]
    star_m_msun = mu_km3s2_to_msun(star_mu)

    sim = rebound.Simulation()
    sim.units = ("AU", "yr", "Msun")
    sim.add(m=star_m_msun, name=star_name)

    meta = {
        "system": d["system_name"],
        "star": {"name": star_name, "mass_msun": star_m_msun},
        "planets": [],
        "phase_seed": phase_seed,
    }

    primary = sim.particles[star_name]
    for p in d.get("planets", []):
        m_msun, kind = _planet_mass_msun(p)
        orb = _planet_orbital(p, star_m_msun=star_m_msun, rng=rng, ecc_override=ecc_override)
        sim.add(
            primary=primary,
            m=m_msun,
            a=orb["a"],
            e=orb["e"],
            inc=orb["inc"],
            omega=orb["omega"],
            Omega=orb["Omega"],
            M=orb["M"],
            name=p["name"],
        )
        meta["planets"].append(
            {
                "name": p["name"],
                "mass_msun": m_msun,
                "mass_kind": kind,
                "a_au": orb["a"],
                "e": orb["e"],
                "inc_rad": orb["inc"],
                "omega_rad": orb["omega"],
                "Omega_rad": orb["Omega"],
                "M_rad": orb["M"],
            }
        )

    return sim, meta


# Solar System — full J2000 ecliptic elements + real masses (M_sun). Names match
# the viewer's hard-coded Sol cluster so the stability data attaches. Inclinations
# are kept as-is (ecliptic, already near-coplanar) — NOT the -90 deg transit hack.
_SOLAR_SYSTEM = [
    # name, mass_msun, a(AU), e, i(deg), Omega(deg), omega(deg), M0(deg, J2000)
    ("Mercury", 1.66012e-7, 0.38710, 0.2056, 7.005, 48.331, 29.125, 174.796),
    ("Venus",   2.44781e-6, 0.72333, 0.0068, 3.395, 76.680, 54.853, 50.115),
    ("Earth",   3.04043e-6, 1.00000, 0.0167, 0.000, 348.739, 114.208, 357.517),  # Earth+Moon
    ("Mars",    3.22716e-7, 1.52371, 0.0934, 1.850, 49.558, 286.502, 19.373),
    ("Jupiter", 9.54792e-4, 5.20288, 0.0489, 1.303, 100.464, 273.867, 20.020),
    ("Saturn",  2.85886e-4, 9.53667, 0.0565, 2.485, 113.665, 339.392, 317.020),
    ("Uranus",  4.36624e-5, 19.18916, 0.0457, 0.773, 74.006, 96.999, 142.239),
    ("Neptune", 5.15139e-5, 30.06992, 0.0113, 1.770, 131.784, 276.336, 256.228),
]


def build_solar_system() -> tuple[rebound.Simulation, dict]:
    """Sun + 8 planets REBOUND sim from J2000 ecliptic elements (real masses).
    The Solar System is the benchmark: real (non-zero) eccentricities so the run
    shows genuine secular/Milankovitch oscillation, not a circular-init flat line."""
    sim = rebound.Simulation()
    sim.units = ("AU", "yr", "Msun")
    sim.add(m=1.0, name="Sun")
    meta = {"system": "Solar System",
            "star": {"name": "Sun", "mass_msun": 1.0},
            "planets": [], "phase_seed": 0}
    primary = sim.particles["Sun"]
    for name, m, a, e, i, Om, om, M in _SOLAR_SYSTEM:
        sim.add(primary=primary, m=m, a=a, e=e,
                inc=math.radians(i), Omega=math.radians(Om),
                omega=math.radians(om), M=math.radians(M), name=name)
        meta["planets"].append({"name": name, "mass_msun": m, "mass_kind": "known",
                                "a_au": a, "e": e, "inc_rad": math.radians(i),
                                "omega_rad": math.radians(om), "Omega_rad": math.radians(Om),
                                "M_rad": math.radians(M)})
    return sim, meta


def build_alpha_cen_ab(db_root: Path, mutual_incl_deg: float = 50.0,
                       a_override: float | None = None,
                       e_override: float | None = None) -> tuple[rebound.Simulation, dict]:
    """α Cen AB binary, plus the S-type candidate α Cen A b around A if curated.

    `mutual_incl_deg` / `a_override` / `e_override` parameterize the planet for
    the Beichman orbit-family scan and the mutual-inclination sweep (default =
    the favored prograde a<2 representative: a/e from the DB, i_mut = 50°).

    The AB binary itself (Proxima outer orbit ignored — irrelevant on 10⁴ yr)
    is trivially stable; the interesting case is the inner planet, which sits
    at a mutual inclination ~50° to the AB plane (Beichman 2025) — inside the
    Kozai-Lidov window, so its eccentricity is expected to oscillate. The
    near-equal binary masses break WHFast's small-perturber assumption, so run
    this system with --integrator trace (or ias15).
    """
    a_path = db_root / "alpha_centauri_a.json"
    d_a = _load_json(a_path)
    binary = d_a["binary_orbit"]
    orbit_ab = next(o for o in binary["orbits"] if o["orbit_id"] == "AB")

    m_a = next(c["mass_msun"] for c in binary["components"] if c["name"] == "Alpha Centauri A")
    m_b = next(c["mass_msun"] for c in binary["components"] if c["name"] == "Alpha Centauri B")

    plx_mas = d_a["stars"][0]["raw"]["parallax_mas"]
    dist_pc = 1000.0 / plx_mas
    a_au = orbit_ab["a_arcsec"] * dist_pc

    i_ab = math.radians(orbit_ab["i_deg"])
    Omega_ab = math.radians(orbit_ab["Omega_deg"])

    sim = rebound.Simulation()
    sim.units = ("AU", "yr", "Msun")
    sim.add(m=m_a, name="Alpha Centauri A")
    sim.add(
        primary=sim.particles[0],
        m=m_b,
        a=a_au,
        e=orbit_ab["e"],
        inc=i_ab,
        Omega=Omega_ab,
        omega=math.radians(orbit_ab["omega_deg"]),
        M=0.0,
        name="Alpha Centauri B",
    )

    planets_meta = [
        {
            "name": "Alpha Centauri B",
            "mass_msun": m_b,
            "mass_kind": "true",
            "a_au": a_au,
            "e": orbit_ab["e"],
            "inc_rad": i_ab,
        }
    ]

    # S-type candidate around A. Place it at the same node as B so the mutual
    # inclination is exactly |i_B - i_planet| = 50° (Beichman 2025, prograde) —
    # inside the Kozai-Lidov window (39.2°–140.8°) → expect e oscillations.
    planet = next((p for p in d_a.get("planets", [])
                   if p.get("name") == "Alpha Centauri A b"), None)
    if planet is not None:
        m_p, kind = _planet_mass_msun(planet)
        orb = _planet_orbital(planet, star_m_msun=m_a)
        a_p = a_override if a_override is not None else orb["a"]
        e_p = e_override if e_override is not None else orb["e"]
        i_mut_deg = mutual_incl_deg
        i_planet = i_ab - math.radians(i_mut_deg)
        sim.add(
            primary=sim.particles[0],
            m=m_p,
            a=a_p,
            e=e_p,
            inc=i_planet,
            Omega=Omega_ab,
            omega=orb["omega"],
            M=orb["M"],
            name="Alpha Centauri A b",
        )
        planets_meta.append({
            "name": "Alpha Centauri A b",
            "mass_msun": m_p,
            "mass_kind": kind,
            "a_au": a_p,
            "e": e_p,
            "inc_rad": i_planet,
            "mutual_incl_deg": i_mut_deg,
        })

    meta = {
        "system": "Alpha Centauri AB" + (" + A b" if planet is not None else ""),
        "star": {"name": "Alpha Centauri A", "mass_msun": m_a},
        "planets": planets_meta,
    }
    return sim, meta


def add_hypotheticals(sim: rebound.Simulation, meta: dict, hyp_path: Path) -> list[dict]:
    """Add moons / extra planets from a hypotheticals JSON. Returns list of body metadata."""
    if not hyp_path.exists():
        return []
    spec = _load_json(hyp_path)
    added = []
    star_mass = meta["star"]["mass_msun"]

    for body in spec.get("bodies", []):
        parent_name = body["parent"]
        try:
            parent = sim.particles[parent_name]
        except rebound.ParticleNotFound as exc:
            raise ValueError(f"Hypothetical parent '{parent_name}' not found in sim") from exc

        a_km = body["semi_major_axis_km"]
        a_au = a_km / KM_PER_AU
        m_kg = body["mass_kg"]
        m_msun = m_kg / MSUN_KG

        # Hill sphere preflight check for moons
        if body.get("type") == "moon":
            parent_meta = next((p for p in meta["planets"] if p["name"] == parent_name), None)
            if parent_meta is None:
                raise ValueError(f"Moon's parent planet '{parent_name}' not in meta")
            r_hill_au = hill_radius(parent_meta["a_au"], parent_meta["mass_msun"], star_mass)
            hill_frac = a_au / r_hill_au
            if hill_frac > 1.0:
                raise ValueError(
                    f"{body['name']}: a = {hill_frac:.2f} R_Hill — definitely unbound. "
                    f"R_Hill = {r_hill_au * KM_PER_AU:,.0f} km."
                )
            body["_hill_fraction_initial"] = hill_frac
            body["_r_hill_km"] = r_hill_au * KM_PER_AU
        else:
            body["_hill_fraction_initial"] = None
            body["_r_hill_km"] = None

        # Moons are specified relative to their PARENT's orbital plane, not the
        # sim reference frame. Offset by the parent's orbital inc/Omega so an
        # inclination_deg=0 moon is coplanar with its planet's orbit. This
        # matters when the planet's orbit is itself inclined (e.g. the alpha Cen
        # binary plane sits ~79 deg from the sim reference) — otherwise a "flat"
        # moon would be wildly inclined to its planet's orbit and spuriously
        # Kozai-pumped by the star. (Planetary-loader planets sit near the
        # reference plane, so this is a no-op there.)
        base_inc, base_Omega = 0.0, 0.0
        if body.get("type") == "moon":
            po = parent.orbit(primary=sim.particles[meta["star"]["name"]])
            base_inc, base_Omega = po.inc, po.Omega
        sim.add(
            primary=parent,
            m=m_msun,
            a=a_au,
            e=body.get("eccentricity", 0.0),
            inc=base_inc + math.radians(body.get("inclination_deg", 0.0)),
            Omega=base_Omega,
            name=body["name"],
        )
        added.append(
            {
                "name": body["name"],
                "parent": parent_name,
                "type": body.get("type", "planet"),
                "mass_msun": m_msun,
                "a_au": a_au,
                "a_km": a_km,
                "e": body.get("eccentricity", 0.0),
                "hill_fraction_initial": body["_hill_fraction_initial"],
                "r_hill_km": body["_r_hill_km"],
            }
        )
    return added
