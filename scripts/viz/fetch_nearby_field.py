# 50광년 이내 모든 별 → db/nearby_field.json (뷰어 "모든 별" 밀도 레이어용)
# SIMBAD basic(plx>65.24mas) 을 척추로: 완전·이름·분광형·밝은 별 포함. Gaia DR3 는
# source_id(SIMBAD ident)로 정확 매칭해 Teff/색 보강(고유운동 무관). 큐레이션 별
# (db/astrometry_raw.json)은 source_id + 위치 이중 디둡. 자전축·항성풍·운동·행성 없는 마커.
import json, math, os, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GAIA_TAP   = "https://gea.esac.esa.int/tap-server/tap/sync"
SIMBAD_TAP = "https://simbad.u-strasbg.fr/simbad/sim-tap/sync"
PLX_MIN = 65.24       # mas → 50 ly
MATCH_ARCSEC = 25.0   # curated dedup radius (loose; high-PM stars caught by source_id)


def tap(endpoint, query, timeout=180):
    data = urllib.parse.urlencode(
        {"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json", "QUERY": query}).encode()
    req = urllib.request.Request(endpoint, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        resp = json.loads(r.read().decode())
    cols = [m["name"] for m in resp["metadata"]]
    return [dict(zip(cols, row)) for row in resp["data"]]


_BPRP_TEFF = [(-0.1, 10000), (0.3, 7500), (0.6, 6500), (0.82, 5800), (1.0, 5300),
              (1.3, 4600), (1.8, 3900), (2.5, 3300), (3.5, 2900), (5.0, 2400)]
_SPTYPE_TEFF = {"O": 35000, "B": 18000, "A": 8500, "F": 6500, "G": 5600,
                "K": 4400, "M": 3300, "L": 1800, "T": 1100, "Y": 600, "D": 12000}


def _interp(x, t):
    if x <= t[0][0]:
        return t[0][1]
    if x >= t[-1][0]:
        return t[-1][1]
    for (x0, y0), (x1, y1) in zip(t, t[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return t[-1][1]


def teff_bprp(b):
    return None if b is None else round(_interp(b, _BPRP_TEFF))


def teff_sptype(sp):
    if not sp:
        return None
    for ch in sp.strip():
        if ch.upper() in _SPTYPE_TEFF:
            return _SPTYPE_TEFF[ch.upper()]
    return None


def angsep(ra1, de1, ra2, de2):
    r1, d1, r2, d2 = map(math.radians, (ra1, de1, ra2, de2))
    s = (math.sin((d2 - d1) / 2) ** 2
         + math.cos(d1) * math.cos(d2) * math.sin((r2 - r1) / 2) ** 2)
    return math.degrees(2 * math.asin(min(1, math.sqrt(s)))) * 3600


def clean_name(main_id):
    # SIMBAD main_id → readable: drop a leading "* ", "V* ", "NAME "
    n = (main_id or "").strip()
    for p in ("NAME ", "V* ", "* "):
        if n.startswith(p):
            n = n[len(p):]
    return n.strip()


def main():
    print(f"SIMBAD basic: plx > {PLX_MIN} mas (≤50 ly) — spine…")
    spine = tap(SIMBAD_TAP, f"""
SELECT oid, main_id, ra, dec, plx_value, sp_type
FROM basic WHERE plx_value > {PLX_MIN} AND ra IS NOT NULL
  AND otype != 'Pl' AND otype != 'Pl?'""".strip())   # drop exoplanets (host-parallax entries)
    print(f"  {len(spine)} SIMBAD stars")

    print("SIMBAD ident: Gaia DR3 source_id per star…")
    idrows = tap(SIMBAD_TAP, f"""
SELECT id.oidref, id.id FROM ident AS id JOIN basic AS b ON b.oid = id.oidref
WHERE b.plx_value > {PLX_MIN} AND id.id LIKE 'Gaia DR3 %'""".strip())
    oid_to_sid = {r["oidref"]: r["id"].split()[-1] for r in idrows}
    print(f"  {len(oid_to_sid)} matched to Gaia DR3")

    print("Gaia DR3: Teff/colour enrichment…")
    grows = tap(GAIA_TAP, f"""
SELECT source_id, teff_gspphot, bp_rp, phot_g_mean_mag
FROM gaiadr3.gaia_source WHERE parallax > {PLX_MIN} AND parallax_over_error > 5""".strip())
    genrich = {str(r["source_id"]): r for r in grows}
    print(f"  {len(genrich)} Gaia rows")

    # curated dedup keys
    cur = json.load(open(f"{BASE}/db/astrometry_raw.json", encoding="utf-8"))
    cur_sids = {r.get("source_id") for r in cur.values() if r.get("source_id")}
    cur_pos = [(r["ra_deg"], r["dec_deg"], r.get("parallax_mas"))
               for r in cur.values() if r.get("ra_deg") is not None]

    def is_curated(ra, dec, plx, sid):
        if sid and sid in cur_sids:
            return True
        for cra, cde, cplx in cur_pos:
            if abs(cra - ra) > 0.05 and abs(cra - ra) < 359.95:
                continue
            if angsep(ra, dec, cra, cde) < MATCH_ARCSEC and (
                    not cplx or abs(cplx - plx) / plx < 0.2):
                return True
        return False

    field, skipped, n_gaia = [], 0, 0
    for s in spine:
        ra, dec, plx = s["ra"], s["dec"], s["plx_value"]
        sid = oid_to_sid.get(s["oid"])
        if is_curated(ra, dec, plx, sid):
            skipped += 1
            continue
        g = genrich.get(sid) if sid else None
        if g:
            teff = g.get("teff_gspphot") or teff_bprp(g.get("bp_rp"))
            gmag = g.get("phot_g_mean_mag"); src = "gaia_dr3"
            n_gaia += 1
        else:
            teff = teff_sptype(s.get("sp_type")); gmag = None; src = "simbad"
        field.append({
            "name": clean_name(s["main_id"]),
            "ra": round(ra, 6), "dec": round(dec, 6), "parallax_mas": round(plx, 3),
            "teff_k": round(teff) if teff else None,
            "spectype": (s.get("sp_type") or "").strip() or None,
            "gmag": round(gmag, 2) if gmag is not None else None, "source": src,
        })
    field.sort(key=lambda f: -f["parallax_mas"])
    print(f"  field: {len(field)} stars ({n_gaia} Gaia-enriched, "
          f"{len(field) - n_gaia} SIMBAD-only) · {skipped} curated dupes removed")
    path = f"{BASE}/db/nearby_field.json"
    json.dump({"plx_min_mas": PLX_MIN, "count": len(field), "stars": field},
              open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"→ {path}")


if __name__ == "__main__":
    main()
