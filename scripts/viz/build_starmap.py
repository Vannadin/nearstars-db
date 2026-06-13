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
import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from _naming import to_file_slug  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
SYS_DIR = os.path.join(ROOT, "db", "systems")
OUT_HTML = os.path.join(ROOT, "docs", "starmap.html")

KM_PER_LY = 9.460730472580800e12
PC_TO_LY = 3.2615637769
CLUSTER_LY = 0.4  # validated: sits in the empty 0.22–1.08 ly gap

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

    return {
        "name": p.get("name"),
        "host_star": p.get("host_star"),
        "semi_major_axis_au": pick(orb.get("semi_major_axis_au"),
                                    raw.get("semi_major_axis_au")),
        "eccentricity": ecc,
        "inclination_deg": pick(orb.get("inclination_deg"),
                                raw.get("inclination_deg"),
                                der.get("inclination_deg")),
        "period_days": pick(orb.get("period_days"), raw.get("period_days")),
        "radius_rearth": pick(phys.get("radius_rearth"), raw.get("radius_rearth")),
        "mass_mearth": pick(phys.get("mass_mearth"), raw.get("mass_mearth")),
        "teq_k": der.get("equilibrium_temperature_k"),
    }


# ── load + per-star record ─────────────────────────────────────────────────
def load_records():
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
        x = der.get("icrs_x_km")
        y = der.get("icrs_y_km")
        z = der.get("icrs_z_km")
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
            "distance_pc": der.get("distance_pc"),
            "pos_ly": [None if v is None else v / KM_PER_LY for v in (x, y, z)],
            "has_full_orbit": "binary_orbit" in d,
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

    components = []
    planets = []
    for m in sorted(members, key=keyfn):
        components.append({
            "name": m["name"], "spectype": m["spectype"],
            "spec_class": m["spec_class"], "teff_k": m["teff_k"],
            "rgb": m["rgb"], "vmag_v": m["vmag_v"],
            "luminosity_lsun": m["luminosity_lsun"],
            "radius_rsun": m["radius_rsun"],
            "distance_pc": round(dist_pc, 4) if dist_pc else None,
            "is_primary": m["file"] == rep["file"],
        })
        for p in m["planets"]:
            pp = dict(p)
            pp["rgb"] = (teff_to_rgb(p["teq_k"]) if p.get("teq_k")
                         else "#ccd2de")
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
        "n_planets": len(planets),
        "components": components,
        "planets": planets,
    }


# ── Solar System (canonical hardcoded elements; not DB-derived) ────────────
def solar_system_cluster():
    # a(AU), e, i(deg to ecliptic), period(d), radius(R_earth), Teq(K)
    P = [
        ("Mercury", 0.387, 0.2056, 7.00, 87.97, 0.383, 440, "#9c9088"),
        ("Venus", 0.723, 0.0068, 3.39, 224.70, 0.949, 737, "#d9b38c"),
        ("Earth", 1.000, 0.0167, 0.00, 365.26, 1.000, 255, "#5b8fd6"),
        ("Mars", 1.524, 0.0934, 1.85, 686.98, 0.532, 210, "#c1502e"),
        ("Jupiter", 5.203, 0.0484, 1.30, 4332.59, 11.21, 110, "#d8b89a"),
        ("Saturn", 9.537, 0.0539, 2.49, 10759.22, 9.45, 81, "#e3d9b0"),
        ("Uranus", 19.191, 0.0473, 0.77, 30688.5, 4.01, 58, "#b5e3e0"),
        ("Neptune", 30.069, 0.0086, 1.77, 60182.0, 3.88, 47, "#5b7fd6"),
    ]
    planets = [{
        "name": n, "host_star": "Sun",
        "semi_major_axis_au": a, "eccentricity": e, "inclination_deg": inc,
        "period_days": per, "radius_rearth": rad, "mass_mearth": None,
        "teq_k": teq, "rgb": col,
    } for (n, a, e, inc, per, rad, teq, col) in P]
    return {
        "id": "sol", "label": "Solar System", "label_ko": "태양계",
        "pos": [0.0, 0.0, 0.0],
        "distance_pc": 0.0, "distance_ly": 0.0,
        "is_confirmed_set": False, "is_sol": True, "beyond_50ly": False,
        "rep_rgb": teff_to_rgb(5772), "rep_radius": marker_radius(1.0, "G"),
        "n_planets": len(planets),
        "components": [{
            "name": "Sun", "spectype": "G2 V", "spec_class": "G",
            "teff_k": 5772, "rgb": teff_to_rgb(5772), "vmag_v": -26.74,
            "luminosity_lsun": 1.0, "radius_rsun": 1.0,
            "distance_pc": 0.0, "is_primary": True,
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
            a = p.get("semi_major_axis_au")
            e = p.get("eccentricity")
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
