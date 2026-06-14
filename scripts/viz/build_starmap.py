# db/systems/*.json을 3D 성도 뷰어(docs/starmap.html)로 빌드
"""Build an interactive 3D star-map viewer from db/systems/*.json.

Reads every system file, clusters components into one marker per
gravitationally-distinct location, bakes blackbody colours / marker sizes /
light-year coordinates, injects the Solar System (canonical hardcoded
elements) at the origin, and emits a self-contained, GitHub-Pages-hostable
HTML file with the data embedded as JSON and Three.js loaded from a CDN.

Colour model: Helland piecewise blackbody-chromaticity approximation —
perceptual, NOT a calibrated stellar SED. Marker sizes are luminosity proxies
(billboard markers), NOT physical radii.

Usage:
    python3 scripts/viz/build_starmap.py            # build
    python3 scripts/viz/build_starmap.py --self-check
"""
import json
import glob
import math
import os
import sys
import csv
import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from _naming import to_file_slug  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
SYS_DIR = os.path.join(ROOT, "db", "systems")
OUT_HTML = os.path.join(ROOT, "docs", "starmap.html")

KM_PER_LY = 9.460730472580800e12
PC_TO_LY = 3.2615637769
AU_PER_LY = 63241.077
M_PER_AU = 1.495978707e11
CLUSTER_LY = 0.4  # validated: sits in the empty 0.22–1.08 ly gap

# nominal main-sequence radius (R_sun) by spectral class — fallback when the
# DB has no measured radius (used only for the real-size render proxy).
_MS_RADIUS_PROXY = {
    "O": 8.0, "B": 3.5, "A": 1.7, "F": 1.3, "G": 1.0,
    "K": 0.7, "M": 0.3, "X": 0.1,  # X folds WD(~0.01)/BD(~0.1)/pulsar
}

CONFIRMED_SLUGS = {
    "alpha_centauri", "barnards_star", "tau_cet", "40_eridani",
    "fomalhaut", "trappist_1", "luhman_16",
}

# ── Teff → RGB (Helland blackbody-chromaticity approximation) ──────────────
def _clamp(v, lo=0.0, hi=255.0):
    return max(lo, min(hi, v))


def teff_to_rgb(teff):
    """Perceptual blackbody colour. Returns '#rrggbb'. None → neutral grey."""
    if teff is None:
        return "#a3b0c8"  # v2 spec-X grey (pulsar / unknown)
    t = max(1000.0, min(40000.0, float(teff))) / 100.0
    # red
    if t <= 66:
        r = 255.0
    else:
        r = _clamp(329.698727446 * (t - 60) ** -0.1332047592)
    # green
    if t <= 66:
        g = _clamp(99.4708025861 * math.log(t) - 161.1195681661)
    else:
        g = _clamp(288.1221695283 * (t - 60) ** -0.0755148492)
    # blue
    if t >= 66:
        b = 255.0
    elif t <= 19:
        b = 0.0
    else:
        b = _clamp(138.5177312231 * math.log(t - 10) - 305.0447927307)
    # slight white-blend at the core for render friendliness
    r = r + (255 - r) * 0.18
    g = g + (255 - g) * 0.18
    b = b + (255 - b) * 0.18
    return "#%02x%02x%02x" % (round(r), round(g), round(b))


# ── spectral class parse (O/B/A/F/G/K/M/X) ─────────────────────────────────
_MS_LUM_PROXY = {  # nominal main-sequence L_sun by class (size fallback)
    "O": 50000, "B": 800, "A": 20, "F": 3.5, "G": 1.0,
    "K": 0.3, "M": 0.02, "X": 0.005,
}


def spec_class(spectype):
    if not spectype:
        return "X"
    s = spectype.strip()
    if s and s[0] == "d" and len(s) > 1:  # dM4.5 → dwarf M
        s = s[1:]
    c = s[0].upper() if s else "X"
    if c in ("O", "B", "A", "F", "G", "K", "M"):
        return c
    return "X"  # white dwarfs (D*), L/T/Y brown dwarfs, pulsar (n...)


def marker_radius(luminosity, sclass):
    """Baked marker scale. luminosity^0.2 when measured, else class proxy."""
    L = luminosity if luminosity is not None else _MS_LUM_PROXY.get(sclass, 0.02)
    if L <= 0:
        L = 0.005
    return round(0.55 * max(0.4, min(4.0, L ** 0.2)), 4)


# ── measurement helpers ────────────────────────────────────────────────────
def _recommended(measurements, value_key):
    """Pick recommended row's value from a *_measurements list, else first."""
    if not measurements:
        return None
    for m in measurements:
        if m.get("recommended") and m.get(value_key) is not None:
            return m[value_key]
    for m in measurements:
        if m.get(value_key) is not None:
            return m[value_key]
    return None


def planet_orbital(p):
    """Prefer curated recommended orbital/physical, fall back to raw/derived."""
    raw = p.get("raw", {})
    der = p.get("derived", {})
    cur = p.get("curated", {})
    orb = {}
    if isinstance(cur.get("orbital"), list):
        for row in cur["orbital"]:
            if row.get("recommended"):
                orb = row
                break
        if not orb and cur["orbital"]:
            orb = cur["orbital"][0]
    phys = {}
    if isinstance(cur.get("physical"), list):
        for row in cur["physical"]:
            if row.get("recommended"):
                phys = row
                break
        if not phys and cur["physical"]:
            phys = cur["physical"][0]

    def pick(*vals):
        for v in vals:
            if v is not None:
                return v
        return None

    ecc = pick(orb.get("eccentricity"), raw.get("eccentricity"),
               der.get("eccentricity"))
    if ecc is not None and not (0 <= ecc < 1):  # -1 sentinel = unknown
        ecc = None

    a_au = pick(orb.get("semi_major_axis_au"), raw.get("semi_major_axis_au"))
    if a_au is None and der.get("semi_major_axis_m"):
        a_au = der["semi_major_axis_m"] / M_PER_AU

    def ang(*vals):
        v = pick(*vals)
        return None if v in (None, -1.0) else v

    return {
        "name": p.get("name"),
        "host_star": p.get("host_star"),
        "a_au": a_au,
        "e": ecc,
        # full Keplerian orientation — used where present, defaulted in the viewer
        "i_deg": ang(orb.get("inclination_deg"), raw.get("inclination_deg"),
                     der.get("inclination_deg")),
        "Omega_deg": ang(der.get("longitude_of_ascending_node_deg")),
        "omega_deg": ang(der.get("argument_of_periapsis_deg"),
                         raw.get("argument_of_periapsis_deg")),
        "M_deg": ang(der.get("mean_anomaly_at_epoch_deg")),
        "period_days": pick(orb.get("period_days"), raw.get("period_days")),
        "radius_rearth": pick(phys.get("radius_rearth"), raw.get("radius_rearth")),
        "mass_mearth": pick(phys.get("mass_mearth"), raw.get("mass_mearth")),
        "teq_k": der.get("equilibrium_temperature_k"),
    }


# ── load + per-star record ─────────────────────────────────────────────────
_MANIFEST_RAW = None


def manifest_raw():
    """Raw docs/reports-manifest.json: star name → {phase2, phase3:{'★':url, 'b':url…}}."""
    global _MANIFEST_RAW
    if _MANIFEST_RAW is None:
        path = os.path.join(ROOT, "docs", "reports-manifest.json")
        _MANIFEST_RAW = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    return _MANIFEST_RAW


def load_manifest():
    """Map system_name → curation phase (3 if phase3, 2 if phase2, else 1)."""
    phase = {}
    for name, rec in manifest_raw().items():
        phase[name] = 3 if rec.get("phase3") else (2 if rec.get("phase2") else 1)
    return phase


_STABILITY = None


def _load_stab_dir(directory):
    """body name → downsampled [[t,a,e,inc,Omega,omega,f]…] (deg) for every
    *_timeseries.csv in dir. Instantaneous elements let the viewer draw a smooth
    analytic ellipse per epoch (positions alone under-sample → polygon)."""
    out = {}
    for f in glob.glob(os.path.join(directory, "*_timeseries.csv")):
        rows = {}
        for r in csv.DictReader(open(f, encoding="utf-8")):
            g = lambda k: float(r.get(k, 0) or 0)
            rows.setdefault(r["body"], []).append((
                float(r["t_yr"]), float(r["a_au"]), float(r["e"]),
                g("inc_deg"), g("Omega_deg"), g("omega_deg"), g("f_deg")))
        for body, series in rows.items():
            series.sort()
            step = max(1, len(series) // 110)
            out[body] = [[int(t), round(a, 4), round(e, 4),
                          round(i, 3), round(Om, 3), round(om, 3), round(fa, 3)]
                         for (t, a, e, i, Om, om, fa) in series[::step]]
    return out


def load_stability():
    """Map planet body name → list of orbit *variants* for the in-viewer 3D
    orbit-evolution animation. Main results (results/) are the system's run; an
    optional results/_observed/ counterpart (e.g. α Cen A b's pre-adjustment
    observed orbit) becomes a second toggleable variant. Each variant is
    {id, data:[[t,a,e,x,y,z]…]}; id ∈ {adopted, observed, sim} drives the
    explanatory note in the viewer."""
    global _STABILITY
    if _STABILITY is not None:
        return _STABILITY
    res = os.path.join(ROOT, "phase3", "stability-sim", "results")
    main = _load_stab_dir(res)
    obs = _load_stab_dir(os.path.join(res, "_observed"))
    out = {}
    for body, data in main.items():
        # if there's an observed counterpart, the main run IS the adopted orbit
        out[body] = [{"id": "adopted" if body in obs else "sim", "data": data}]
        if body in obs:
            out[body].append({"id": "observed", "data": obs[body]})
    _STABILITY = out
    return out


_DISKS = None


def load_disks():
    """System name → list of debris-ring belts {inner_au, outer_au, inc_deg}
    (recommended belts with at least one radius) for the disk visualization."""
    global _DISKS
    if _DISKS is not None:
        return _DISKS
    path = os.path.join(ROOT, "db", "disks_curated.json")
    out = {}
    if os.path.exists(path):
        d = json.load(open(path, encoding="utf-8"))
        for sysname, rec in d.items():
            belts = []
            for b in rec.get("disk_measurements", []):
                if not b.get("recommended"):
                    continue
                ri, ro = b.get("inner_radius_au"), b.get("outer_radius_au")
                if ri is None and ro is None:
                    continue
                if ri is None:
                    ri = round(ro * 0.7, 2)
                if ro is None:
                    ro = round(ri * 1.3, 2)
                name = b.get("belt") or ""
                # render kind: broad inner disks fill, narrow belts/rings draw as
                # crisp outlines. width/name heuristic (Fomalhaut inner_warm is the
                # only genuinely broad component in the curated set).
                if name == "inner_warm" or (ro - ri) > 0.6 * ri:
                    kind = "disk"
                elif name == "main_cold":
                    kind = "ring"
                else:
                    kind = "belt"
                belts.append({"inner_au": ri, "outer_au": ro,
                              "inc_deg": b.get("inclination_deg") or 0,
                              "e": b.get("eccentricity") or 0,
                              "pa_deg": b.get("position_angle_deg") or 0,
                              "argp_deg": b.get("argument_of_periapsis_deg") or 0,
                              "belt": name, "kind": kind})
            # dedupe identical rings
            seen, uniq = set(), []
            for b in belts:
                k = (b["inner_au"], b["outer_au"])
                if k not in seen:
                    seen.add(k); uniq.append(b)
            if uniq:
                out[sysname] = uniq
    _DISKS = out
    return out


def load_records():
    manifest = load_manifest()
    recs = []
    for f in sorted(glob.glob(os.path.join(SYS_DIR, "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        base = os.path.basename(f)
        stars = d.get("stars", [])
        if not stars:
            continue
        star = stars[0]
        raw = star.get("raw", {})
        der = star.get("derived", {})
        teff = raw.get("teff_k")
        sclass = spec_class(raw.get("spectype"))
        lum = der.get("luminosity_lsun")
        radius_rsun = _recommended(raw.get("radius_measurements"), "value_rsun")
        mass_msun = _recommended(raw.get("mass_measurements"), "value_msun")
        x = der.get("icrs_x_km")
        y = der.get("icrs_y_km")
        z = der.get("icrs_z_km")
        vel_kms = (der.get("icrs_vx_km_s"), der.get("icrs_vy_km_s"),
                   der.get("icrs_vz_km_s"))
        recs.append({
            "file": base,
            "name": star.get("name"),
            "system_name": d.get("system_name"),
            "spectype": raw.get("spectype"),
            "spec_class": sclass,
            "teff_k": teff,
            "rgb": teff_to_rgb(teff),
            "vmag_v": raw.get("vmag_v"),
            "luminosity_lsun": lum,
            "radius_rsun": radius_rsun,
            "mass_msun": mass_msun,
            "vel_kms": vel_kms,
            "distance_pc": der.get("distance_pc"),
            "epoch_jd": der.get("epoch_jd"),
            "phase": manifest.get(star.get("name"),
                                  manifest.get(d.get("system_name"), 1)),
            "pos_ly": [None if v is None else v / KM_PER_LY for v in (x, y, z)],
            "has_full_orbit": "binary_orbit" in d,
            "binary_orbit": d.get("binary_orbit"),
            "ref": d.get("binary_orbit_ref"),
            "planets": [planet_orbital(p) for p in d.get("planets", [])],
        })
    return recs


# ── union-find clustering ──────────────────────────────────────────────────
def cluster(recs):
    n = len(recs)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        parent[find(i)] = find(j)

    thr2 = CLUSTER_LY ** 2
    for i in range(n):
        xi, yi, zi = recs[i]["pos_ly"]
        for j in range(i + 1, n):
            xj, yj, zj = recs[j]["pos_ly"]
            d2 = (xi - xj) ** 2 + (yi - yj) ** 2 + (zi - zj) ** 2
            if d2 < thr2:
                union(i, j)

    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)

    # guard: every binary_orbit_ref target must share its cluster
    by_file = {r["file"]: idx for idx, r in enumerate(recs)}
    for idx, r in enumerate(recs):
        if r["ref"]:
            tgt = r["ref"] if r["ref"].endswith(".json") else r["ref"] + ".json"
            if tgt in by_file and find(idx) != find(by_file[tgt]):
                raise SystemExit(
                    f"CLUSTER GUARD FAILED: {r['file']} and its "
                    f"binary_orbit_ref {tgt} fell into different clusters. "
                    f"Review CLUSTER_LY ({CLUSTER_LY} ly)."
                )
    return list(groups.values())


def _mean_to_true(M, e):
    E = M
    for _ in range(12):
        E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
    return 2 * math.atan2(math.sqrt(1 + e) * math.sin(E / 2),
                          math.sqrt(1 - e) * math.cos(E / 2))


def _v_cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def _v_norm(a):
    m = math.sqrt(sum(c * c for c in a))
    return [c / m for c in a] if m > 1e-12 else None


def _sky_triad(pos, i_deg, Om_deg, om_deg):
    """ICRS orbital triad (peri, q) for *sky-plane* elements at a star whose ICRS
    direction is `pos` (Sol = origin). Mirror of the viewer's skyBasis: i is the
    inclination from the plane of sky (0 face-on / 90 edge-on as seen from Sol),
    Omega = PA of the ascending node (North→East), omega = argument of periapsis.
    Built right-handed in ICRS; the viewer maps (x,y,z)→(x,z,y)."""
    s = _v_norm(pos) or [0.0, 0.0, 1.0]          # degenerate (Sol): no line of sight
    E = _v_norm(_v_cross([0, 0, 1], s)) or [1.0, 0.0, 0.0]   # east (incr RA)
    N = _v_cross(s, E)                                       # north (incr Dec)
    i = math.radians(i_deg or 0); Om = math.radians(Om_deg or 0); om = math.radians(om_deg or 0)
    node = [N[k] * math.cos(Om) + E[k] * math.sin(Om) for k in range(3)]
    ns = _v_cross(node, s)
    n = [s[k] * math.cos(i) + ns[k] * math.sin(i) for k in range(3)]   # orbit normal
    w = _v_cross(n, node)
    peri = [node[k] * math.cos(om) + w[k] * math.sin(om) for k in range(3)]
    q = _v_cross(n, peri)
    return peri, q


def _orbit_point(pos, a, e, i_deg, Om_deg, om_deg, nu):
    """Keplerian orbit point → ICRS (x,y,z) AU, oriented sky-true for a star at
    ICRS direction `pos` (so a binary's measured i/Omega/omega — Campbell elements
    relative to the plane of sky — land in the real ICRS orientation, not a generic
    grid frame). Output ordering matches the viewer's M:(x,y,z)→(x,z,y) mapping."""
    peri, q = _sky_triad(pos, i_deg, Om_deg, om_deg)
    r = a * (1 - e * e) / (1 + e * math.cos(nu))
    cx, sx = r * math.cos(nu), r * math.sin(nu)
    return tuple(peri[k] * cx + q[k] * sx for k in range(3))


def kepler_trajectory(orbit, epoch_jd, star_pos):
    """Two-body (= N-body for N=2) past trajectory of a secondary about its
    primary from published orbital elements. Used when the catalog 6D state
    doesn't give a bound pair but an orbital solution exists (e.g. 36 Oph A–B).
    star_pos = the system's ICRS direction (for sky-true orientation).
    Returns [[x,y,z]_AU…] ICRS, index 0 = now, going back ~0.9 of an orbit."""
    a = orbit.get("a_au")
    if not a:
        return None
    e = orbit.get("e") or 0.0
    P, T = orbit.get("P_yr"), orbit.get("T_jd")
    M0 = 0.0
    if T is not None and P and epoch_jd is not None:
        M0 = 2 * math.pi * ((epoch_jd - T) / 365.25) / P
    norm = lambda x: (x % (2 * math.pi) + 2 * math.pi) % (2 * math.pi)
    K, sweep = 150, 2 * math.pi * 0.9
    pts = []
    for k in range(K + 1):                    # k=0 now, increasing k = older
        nu = _mean_to_true(norm(M0 - sweep * (k / K)), e)
        x, y, z = _orbit_point(star_pos, a, e, orbit.get("i_deg"),
                               orbit.get("Omega_deg"), orbit.get("omega_deg"), nu)
        pts.append([round(x, 4), round(y, 4), round(z, 4)])
    return pts


def _accel(bs, G):
    a = [[0.0, 0.0, 0.0] for _ in bs]
    for i in range(len(bs)):
        for j in range(len(bs)):
            if i == j:
                continue
            dx = [bs[j]["p"][k] - bs[i]["p"][k] for k in range(3)]
            r = math.sqrt(sum(c * c for c in dx)) + 1e-6
            f = G * bs[j]["M"] / r ** 3
            for k in range(3):
                a[i][k] += f * dx[k]
    return a


def nbody_trajectories(members, rep):
    """Backward N-body trajectories for a multi-star system from its stored 6D
    state (real positions + velocities + masses). Components are split into
    gravitationally **bound subgroups** (pairwise specific energy < 0); each
    bound group of ≥2 is integrated in its own barycentric frame, so a loosely
    attached member whose catalog velocity is unbound (e.g. 40 Eri A vs the B–C
    pair) cannot contaminate the bound pair's orbit. Returns {name:[[x,y,z]_AU…]}
    in the ICRS frame relative to the rep's current position (index 0 = now);
    unbound singletons get no trajectory. Returns (traj_or_None, spans) where
    spans[name] is the integration time span (yr) — used for planet epicycles."""
    G = 4 * math.pi ** 2            # AU^3 / (Msun yr^2)
    KMS_TO_AUYR = 0.21094502
    spans = {}
    dyn = []
    for m in members:
        if m["mass_msun"] is None or any(v is None for v in m["vel_kms"]):
            continue
        dyn.append({
            "name": m["name"], "M": m["mass_msun"],
            "p": [c * AU_PER_LY for c in m["pos_ly"]],          # AU
            "v": [c * KMS_TO_AUYR for c in m["vel_kms"]],       # AU/yr
        })
    if len(dyn) < 2:
        return None, spans

    # bound graph via pairwise two-body specific energy
    n = len(dyn)
    par = list(range(n))

    def find(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i

    for i in range(n):
        for j in range(i + 1, n):
            dr = [dyn[i]["p"][k] - dyn[j]["p"][k] for k in range(3)]
            dv = [dyn[i]["v"][k] - dyn[j]["v"][k] for k in range(3)]
            r = math.sqrt(sum(c * c for c in dr))
            v2 = sum(c * c for c in dv)
            E = 0.5 * v2 - G * (dyn[i]["M"] + dyn[j]["M"]) / max(r, 1e-6)
            if E < 0:
                par[find(i)] = find(j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)

    repos = [c * AU_PER_LY for c in rep["pos_ly"]]   # rep current pos (AU)
    traj = {}
    for g in groups.values():
        if len(g) < 2:
            continue                                  # unbound singleton → static
        grp = [dyn[i] for i in g]
        Mtot = sum(b["M"] for b in grp)
        com = [sum(b["M"] * b["p"][k] for b in grp) / Mtot for k in range(3)]
        cov = [sum(b["M"] * b["v"][k] for b in grp) / Mtot for k in range(3)]
        P = [{"name": b["name"], "M": b["M"],
              "p": [b["p"][k] - com[k] for k in range(3)],
              "v": [b["v"][k] - cov[k] for k in range(3)]} for b in grp]
        const = [com[k] - repos[k] for k in range(3)]  # re-anchor to rep current
        sep_min = min(math.dist(P[a]["p"], P[b]["p"])
                      for a in range(len(P)) for b in range(a + 1, len(P)))
        P_est = math.sqrt(max(sep_min, 1e-3) ** 3 / max(Mtot, 1e-3))   # yr (Kepler)
        span = min(max(1.4 * P_est, 15.0), 20000.0)
        N = 4000
        dt = -span / N
        rec = max(1, N // 150)
        for b in P:
            traj[b["name"]] = []
            spans[b["name"]] = span
        acc = _accel(P, G)
        for step in range(N + 1):
            if step % rec == 0:
                for b in P:
                    traj[b["name"]].append([round(b["p"][k] + const[k], 4) for k in range(3)])
            for bi, b in enumerate(P):
                for k in range(3):
                    b["p"][k] += b["v"][k] * dt + 0.5 * acc[bi][k] * dt * dt
            acc2 = _accel(P, G)
            for bi, b in enumerate(P):
                for k in range(3):
                    b["v"][k] += 0.5 * (acc[bi][k] + acc2[bi][k]) * dt
            acc = acc2
        # light safety: drop a body that still wanders absurdly (chaotic triple)
        for b in P:
            p0 = traj[b["name"]][0]
            if any(math.dist(p, p0) > 8 * sep_min for p in traj[b["name"]]):
                del traj[b["name"]]
                spans.pop(b["name"], None)
    return (traj or None), spans


def planet_epicycle(planet, host_pts, span_host, star_pos):
    """Real-space path of a planet orbiting a *moving* host: host N-body position
    (interpolated from its trajectory) + the planet's Keplerian offset, sampled
    over ~8 planet periods → a drifting coil. star_pos = system ICRS direction
    (sky-true orientation). Returns [[x,y,z]_AU…] ICRS rel rep, index 0 = now.
    None if the planet lacks a/period."""
    a = planet.get("a_au")
    per_d = planet.get("period_days")
    if not a or not per_d or per_d <= 0:
        return None
    e = planet.get("e") or 0.0
    P_pl = per_d / 365.25
    nmot = 2 * math.pi / P_pl
    M0 = math.radians(planet.get("M_deg") or 0)
    window = min(span_host, 2.6 * P_pl)   # ~2-3 loops: shows host drift without tangling
    N = len(host_pts)
    norm = lambda x: (x % (2 * math.pi) + 2 * math.pi) % (2 * math.pi)
    K = max(160, min(2400, int(window / P_pl * 48)))
    out = []
    for j in range(K + 1):                       # j=0 now, increasing = older
        t = -window * (j / K)
        f = (-t / span_host) * (N - 1) if span_host > 0 else 0.0
        i0 = int(f); i1 = min(i0 + 1, N - 1); fr = f - i0
        h = [host_pts[i0][k] + (host_pts[i1][k] - host_pts[i0][k]) * fr for k in range(3)]
        nu = _mean_to_true(norm(M0 + nmot * t), e)
        ox, oy, oz = _orbit_point(star_pos, a, e, planet.get("i_deg"),
                                  planet.get("Omega_deg"), planet.get("omega_deg"), nu)
        out.append([round(h[0] + ox, 5), round(h[1] + oy, 5), round(h[2] + oz, 5)])
    return out


def _strip_component(name):
    """'Alpha Centauri A' → 'Alpha Centauri'; leave singletons intact."""
    if not name:
        return name
    toks = name.split()
    if len(toks) > 1 and toks[-1] in ("A", "B", "C", "AB", "Ba", "Bb"):
        return " ".join(toks[:-1])
    return name


def build_cluster_obj(members):
    # representative: full-orbit holder → brightest vmag → nearest
    def keyfn(r):
        v = r["vmag_v"] if r["vmag_v"] is not None else 99
        d = r["distance_pc"] if r["distance_pc"] is not None else 1e9
        return (not r["has_full_orbit"], v, d)
    rep = sorted(members, key=keyfn)[0]

    # label: common stripped system_name if all members agree, else rep
    stripped = {_strip_component(m["system_name"]) for m in members}
    label = stripped.pop() if len(stripped) == 1 else _strip_component(rep["system_name"])

    pos = [round(c, 4) for c in rep["pos_ly"]]
    dist_pc = rep["distance_pc"]
    dist_ly = round(dist_pc * PC_TO_LY, 3) if dist_pc else None

    # binary-orbit block (present on at most one member) for component placement
    bo = next((m["binary_orbit"] for m in members if m.get("binary_orbit")), None)

    def orbit_for(name):
        """Relative binary orbit with this star as secondary about the rep."""
        if not bo:
            return None
        for o in bo.get("orbits", []):
            if o.get("secondary") == name and o.get("primary") == rep["name"]:
                a_au = o.get("a_au")
                if a_au is None and o.get("a_arcsec") and dist_pc:
                    a_au = o["a_arcsec"] * dist_pc
                if a_au is None:
                    return None
                return {
                    "a_au": a_au, "e": o.get("e", 0.0),
                    "i_deg": o.get("i_deg"), "omega_deg": o.get("omega_deg"),
                    "Omega_deg": o.get("Omega_deg"),
                    "P_yr": o.get("P_yr"), "T_jd": o.get("T_jd_tt"),
                }
        return None

    # real N-body past trajectories for multi-star systems (from stored 6D state)
    traj, spans = (nbody_trajectories(members, rep) if len(members) > 1 else (None, {}))

    components = []
    planets = []
    for m in sorted(members, key=keyfn):
        is_primary = m["file"] == rep["file"]
        off_au = [round((m["pos_ly"][k] - rep["pos_ly"][k]) * AU_PER_LY, 5)
                  for k in range(3)]
        mag = math.sqrt(sum(c * c for c in off_au))
        orbit = None if is_primary else orbit_for(m["name"])
        if is_primary:
            kind = "primary"
        elif mag > 1.0:
            kind = "astrometric"          # real wide pair (e.g. Proxima)
        elif orbit:
            kind = "orbit"                # real relative orbit about the rep
        else:
            kind = "schematic"            # laid out by the viewer (not to scale)
        components.append({
            "name": m["name"], "spectype": m["spectype"],
            "spec_class": m["spec_class"], "teff_k": m["teff_k"],
            "rgb": m["rgb"], "vmag_v": m["vmag_v"],
            "luminosity_lsun": m["luminosity_lsun"],
            "radius_rsun": m["radius_rsun"] or _MS_RADIUS_PROXY.get(m["spec_class"], 0.3),
            "radius_measured": m["radius_rsun"] is not None,
            "distance_pc": round(dist_pc, 4) if dist_pc else None,
            # N-body trajectory where the catalog state gives a bound pair;
            # else a 2-body Keplerian path from published elements; else none.
            "is_primary": is_primary,
            "phase": m.get("phase", 1),
            # Phase 3 report page for this star (manifest '★' host entry), if any
            "phase3": (manifest_raw().get(m["name"], {}).get("phase3") or {}).get("★"),
            "offset_au": off_au, "placement": kind, "orbit": orbit,
            "trajectory": (traj or {}).get(m["name"])
            or (kepler_trajectory(orbit, rep.get("epoch_jd"), rep["pos_ly"]) if orbit else None),
        })
        _p3h = manifest_raw().get(m["name"], {}).get("phase3") or {}
        for p in m["planets"]:
            pp = dict(p)
            pp["rgb"] = (teff_to_rgb(p["teq_k"]) if p.get("teq_k")
                         else "#ccd2de")
            pp["phase3"] = _p3h.get(p["name"].split()[-1])   # planet-letter page, if any
            # planet around a moving host (binary N-body) → real-space epicycle
            if traj and m["name"] in traj:
                epi = planet_epicycle(p, traj[m["name"]], spans[m["name"]], rep["pos_ly"])
                if epi:
                    pp["epicycle"] = epi
            stab = load_stability().get(p["name"])
            if stab:
                pp["stability"] = stab
            planets.append(pp)

    return {
        "id": to_file_slug(label or rep["name"]),
        "label": label,
        "label_ko": None,
        "pos": pos,
        "distance_pc": round(dist_pc, 4) if dist_pc else None,
        "distance_ly": dist_ly,
        "is_confirmed_set": any(
            m["file"][:-5].startswith(s) for m in members for s in CONFIRMED_SLUGS
        ),
        "is_sol": False,
        "beyond_50ly": (dist_ly is not None and dist_ly > 50),
        "rep_rgb": rep["rgb"],
        "rep_radius": marker_radius(rep["luminosity_lsun"], rep["spec_class"]),
        "max_phase": max((m.get("phase", 1) for m in members), default=1),
        "epoch_jd": rep.get("epoch_jd"),
        "vel": [round(v, 4) if v is not None else None for v in rep["vel_kms"]],
        "disks": next((load_disks()[k] for k in load_disks()
                       if k == label or any(k == m["system_name"] or m["name"] == k
                                            for m in members)), None),
        "n_planets": len(planets),
        "components": components,
        "planets": planets,
    }


# ── Solar System (canonical hardcoded elements; not DB-derived) ────────────
def solar_system_cluster():
    # name, a(AU), e, i, Omega, omega, M0(J2000, deg), period(d), R_earth, Teq, colour
    # full J2000 elements (referenced to the ecliptic) so the orbits render
    # correctly inclined & oriented — a calibration showcase.
    P = [
        ("Mercury", 0.38710, 0.2056, 7.005, 48.331, 29.125, 174.796, 87.97, 0.383, 440, "#9c9088"),
        ("Venus", 0.72333, 0.0068, 3.395, 76.680, 54.853, 50.115, 224.70, 0.949, 737, "#d9b38c"),
        ("Earth", 1.00000, 0.0167, 0.000, 348.739, 114.208, 357.517, 365.26, 1.000, 255, "#5b8fd6"),
        ("Mars", 1.52371, 0.0934, 1.850, 49.558, 286.502, 19.373, 686.98, 0.532, 210, "#c1502e"),
        ("Jupiter", 5.20288, 0.0489, 1.303, 100.464, 273.867, 20.020, 4332.59, 11.21, 110, "#d8b89a"),
        ("Saturn", 9.53667, 0.0565, 2.485, 113.665, 339.392, 317.020, 10759.22, 9.45, 81, "#e3d9b0"),
        ("Uranus", 19.18916, 0.0457, 0.773, 74.006, 96.999, 142.239, 30688.5, 4.01, 58, "#b5e3e0"),
        ("Neptune", 30.06992, 0.0113, 1.770, 131.784, 276.336, 256.228, 60182.0, 3.88, 47, "#5b7fd6"),
    ]
    planets = [{
        "name": n, "host_star": "Sun", "a_au": a, "e": e, "i_deg": i,
        "Omega_deg": Om, "omega_deg": om, "M_deg": M, "period_days": per,
        "radius_rearth": rad, "mass_mearth": None, "teq_k": teq, "rgb": col,
        "phase3": (manifest_raw().get("Sun", {}).get("phase3") or {}).get(n),
        "stability": load_stability().get(n),   # solar_system REBOUND run, if present
    } for (n, a, e, i, Om, om, M, per, rad, teq, col) in P]
    return {
        "id": "sol", "label": "Solar System", "label_ko": "태양계",
        "pos": [0.0, 0.0, 0.0],
        "distance_pc": 0.0, "distance_ly": 0.0,
        "is_confirmed_set": False, "is_sol": True, "beyond_50ly": False,
        "rep_rgb": teff_to_rgb(5772), "rep_radius": marker_radius(1.0, "G"),
        "max_phase": 3, "epoch_jd": 2451545.0, "vel": [0.0, 0.0, 0.0],
        "n_planets": len(planets),
        "components": [{
            "name": "Sun", "spectype": "G2 V", "spec_class": "G",
            "teff_k": 5772, "rgb": teff_to_rgb(5772), "vmag_v": -26.74,
            "luminosity_lsun": 1.0, "radius_rsun": 1.0, "radius_measured": True,
            "distance_pc": 0.0, "is_primary": True, "phase": 3,
            "offset_au": [0.0, 0.0, 0.0], "placement": "primary", "orbit": None,
        }],
        "planets": planets,
    }


def build_payload():
    recs = load_records()
    groups = cluster(recs)
    clusters = [build_cluster_obj([recs[i] for i in g]) for g in groups]
    clusters.sort(key=lambda c: (c["distance_ly"] is None, c["distance_ly"] or 0))
    sol = solar_system_cluster()
    clusters.insert(0, sol)

    n_planets_db = sum(len(r["planets"]) for r in recs)
    meta = {
        "generated": datetime.date.today().isoformat(),
        "n_files": len(recs),
        "n_clusters": len(clusters),
        "n_clusters_db": len(groups),
        "n_planets": n_planets_db + len(sol["planets"]),
        "n_planets_db": n_planets_db,
        "color_model": "Helland blackbody-chromaticity approx (perceptual, not a calibrated SED)",
        "coordinate_frame": "ICRS Cartesian, origin = SSB (Sol≈0,0,0), units = light-years",
        "marker_size_model": "luminosity^0.2 when measured (24/157), else spectral-class MS proxy; billboard proxy, not physical radius",
        "sol_data": "Solar System = canonical textbook elements, hardcoded (not db-derived)",
    }
    return {"meta": meta, "clusters": clusters}


# ── self-check ─────────────────────────────────────────────────────────────
EXPECTED_MULTI = {
    "Alpha Centauri": 3, "40 Eridani": 3, "36 Ophiuchi": 3,
    "61 Cygni": 2, "70 Ophiuchi": 2, "Eta Cassiopeiae": 2,
    "Luhman 16": 2, "55 Cnc": 2,
}


def self_check(payload):
    m = payload["meta"]
    errs = []
    if m["n_files"] != 157:
        errs.append(f"n_files {m['n_files']} != 157")
    if m["n_clusters_db"] != 142:
        errs.append(f"n_clusters_db {m['n_clusters_db']} != 142")
    if m["n_planets_db"] != 227:
        errs.append(f"n_planets_db {m['n_planets_db']} != 227")
    comp_total = sum(len(c["components"]) for c in payload["clusters"] if not c["is_sol"])
    if comp_total != 157:
        errs.append(f"DB components {comp_total} != 157")

    by_label = {c["label"]: c for c in payload["clusters"]}
    for lbl, k in EXPECTED_MULTI.items():
        c = by_label.get(lbl)
        if not c:
            errs.append(f"missing multi-system '{lbl}'")
        elif len(c["components"]) != k:
            errs.append(f"'{lbl}' has {len(c['components'])} components, want {k}")

    sol = next((c for c in payload["clusters"] if c["is_sol"]), None)
    if not sol or len(sol["planets"]) != 8:
        errs.append("Solar System missing or != 8 planets")

    for c in payload["clusters"]:
        if not c["rep_rgb"]:
            errs.append(f"{c['label']} missing rep_rgb")
        if c["rep_radius"] <= 0:
            errs.append(f"{c['label']} rep_radius <= 0")
        for v in c["pos"]:
            if v is None or not math.isfinite(v) or abs(v) > 1000:
                errs.append(f"{c['label']} bad pos {c['pos']}")
                break
        for p in c["planets"]:
            a = p.get("a_au")
            e = p.get("e")
            if a is not None and a <= 0:
                errs.append(f"{p['name']} a<=0")
            if e is not None and not (0 <= e < 1):
                errs.append(f"{p['name']} e out of [0,1)")

    if errs:
        print("SELF-CHECK FAILED:")
        for e in errs:
            print("  -", e)
        return False
    print("SELF-CHECK PASSED:",
          f"{m['n_files']} files → {m['n_clusters_db']} DB clusters (+Sol = {m['n_clusters']}), "
          f"{m['n_planets']} planets")
    return True


# ── emit ───────────────────────────────────────────────────────────────────
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "starmap_template.html")


def emit_html(payload):
    data_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    data_json = data_json.replace("</", "<\\/")  # escape </script>
    with open(TEMPLATE_PATH, encoding="utf-8") as fh:
        template = fh.read()
    html = template.replace("/*__DATA__*/", data_json)
    os.makedirs(os.path.dirname(OUT_HTML), exist_ok=True)
    with open(OUT_HTML, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("wrote", os.path.relpath(OUT_HTML, ROOT),
          f"({len(html)//1024} KB)")


def main():
    payload = build_payload()
    ok = self_check(payload)
    if "--self-check" in sys.argv:
        sys.exit(0 if ok else 1)
    if not ok:
        sys.exit(1)
    emit_html(payload)
    print("serve:  python3 -m http.server  (run inside docs/, then open "
          "http://localhost:8000/starmap.html)")


if __name__ == "__main__":
    main()
