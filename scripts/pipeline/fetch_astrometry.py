# target_list.json → Gaia DR3 TAP 배치 쿼리 + SIMBAD 폴백 → db/astrometry_raw.json
import json, math, urllib.request, urllib.parse, time, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schema

BASE      = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GAIA_TAP  = "https://gea.esac.esa.int/tap-server/tap/sync"
SIMBAD_TAP = "https://simbad.u-strasbg.fr/simbad/sim-tap/sync"

JD_GAIA   = 2457389.0   # J2016.0
JD_J2000  = 2451545.0   # J2000.0


def tap_post(endpoint, query, timeout=60):
    data = urllib.parse.urlencode(
        {"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json", "QUERY": query}
    ).encode()
    req = urllib.request.Request(endpoint, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def tap_rows(resp):
    cols = [m["name"] for m in resp["metadata"]]
    return [dict(zip(cols, row)) for row in resp["data"]]


def fetch_gaia_batch(source_ids):
    """Gaia DR3에서 여러 source_id를 배치 쿼리."""
    id_list = ", ".join(source_ids)
    q = f"""
SELECT source_id, ra, ra_error, dec, dec_error,
       parallax, parallax_error,
       pmra, pmra_error, pmdec, pmdec_error,
       radial_velocity, radial_velocity_error
FROM gaiadr3.gaia_source
WHERE source_id IN ({id_list})
""".strip()
    resp = tap_post(GAIA_TAP, q, timeout=90)
    return {str(row["source_id"]): row for row in tap_rows(resp)}


def fetch_simbad_star(star_name):
    """SIMBAD TAP에서 단일 항성 아스트로메트리 조회 (Gaia 미탐재 밝은 별 대상)."""
    safe = star_name.replace("'", "''")
    q = f"""
SELECT b.ra, b.dec, b.plx_value, b.pmra, b.pmdec, b.rvz_radvel
FROM basic b
JOIN ident i ON i.oidref = b.oid
WHERE i.id = '{safe}'
""".strip()
    try:
        rows = tap_rows(tap_post(SIMBAD_TAP, q, timeout=30))
        if not rows:
            return None
        r = rows[0]
        return {
            "ra": r["ra"], "ra_error": None,
            "dec": r["dec"], "dec_error": None,
            "parallax": r["plx_value"], "parallax_error": None,
            "pmra": r["pmra"], "pmra_error": None,
            "pmdec": r["pmdec"], "pmdec_error": None,
            "radial_velocity": r["rvz_radvel"], "radial_velocity_error": None,
        }
    except Exception as e:
        print(f"  SIMBAD 오류 ({star_name}): {e}")
        return None


# ── 입력 로드 ──────────────────────────────────────────────────────────────────
with open(f"{BASE}/db/target_list.json") as f:
    target_list = json.load(f)

# 항성별 Gaia ID 매핑 구성 (Gaia ID 없는 별도 포함해야 SIMBAD 폴백 처리됨)
star_to_gaia = {}   # star_name → gaia_source_id (str) or None
for entry in target_list:
    comps = entry["components"]
    gids  = entry.get("gaia_source_ids", [])
    for i, comp in enumerate(comps):
        star_to_gaia[comp] = gids[i] if i < len(gids) else None

# 카테고리 분리
gaia_stars    = {name: gid for name, gid in star_to_gaia.items() if gid}
simbad_stars  = [name for name, gid in star_to_gaia.items() if not gid]

print(f"Gaia DR3 쿼리 대상: {len(gaia_stars)}개 항성")
print(f"SIMBAD 폴백 대상: {len(simbad_stars)}개 항성")

results = {}  # star_name → astrometry dict

# ── Gaia DR3 배치 쿼리 (1000개씩 분할) ────────────────────────────────────────
gaia_ids = list(gaia_stars.values())
gaia_names_by_id = {gid: name for name, gid in gaia_stars.items()}

CHUNK = 1000
for i in range(0, len(gaia_ids), CHUNK):
    chunk = gaia_ids[i:i+CHUNK]
    print(f"\nGaia 배치 {i//CHUNK+1}: {len(chunk)}개 쿼리 중...", end=" ", flush=True)
    try:
        rows = fetch_gaia_batch(chunk)
        print(f"{len(rows)}개 반환")
        for sid, row in rows.items():
            name = gaia_names_by_id.get(sid)
            if name:
                results[name] = {
                    "source":                "gaia_dr3",
                    "source_id":             sid,
                    "epoch_jd":              JD_GAIA,
                    "epoch_label":           "J2016.0",
                    "ra_deg":                row["ra"],
                    "ra_error_mas":          row["ra_error"],
                    "dec_deg":               row["dec"],
                    "dec_error_mas":         row["dec_error"],
                    "parallax_mas":          row["parallax"],
                    "parallax_error_mas":    row["parallax_error"],
                    "pmra_mas_yr":           row["pmra"],
                    "pmra_error_mas_yr":     row["pmra_error"],
                    "pmdec_mas_yr":          row["pmdec"],
                    "pmdec_error_mas_yr":    row["pmdec_error"],
                    "radial_velocity_km_s":  row["radial_velocity"],
                    "rv_error_km_s":         row["radial_velocity_error"],
                }
        # 누락 항성 확인
        missing = [gaia_names_by_id[sid] for sid in chunk if sid not in rows]
        if missing:
            print(f"  Gaia 미반환: {missing}")
    except Exception as e:
        print(f"GAIA 배치 오류: {e}")

# ── SIMBAD 폴백 ────────────────────────────────────────────────────────────────
print(f"\nSIMBAD 쿼리:")
for name in simbad_stars:
    print(f"  {name}...", end=" ", flush=True)
    astro = fetch_simbad_star(name)
    time.sleep(0.3)
    if astro:
        results[name] = {
            "source":                "simbad",
            "source_id":             None,
            "epoch_jd":              JD_J2000,
            "epoch_label":           "J2000.0",
            "ra_deg":                astro["ra"],
            "ra_error_mas":          None,
            "dec_deg":               astro["dec"],
            "dec_error_mas":         None,
            "parallax_mas":          astro["parallax"],
            "parallax_error_mas":    None,
            "pmra_mas_yr":           astro["pmra"],
            "pmra_error_mas_yr":     None,
            "pmdec_mas_yr":          astro["pmdec"],
            "pmdec_error_mas_yr":    None,
            "radial_velocity_km_s":  astro["radial_velocity"],
            "rv_error_km_s":         None,
        }
        print("OK")
    else:
        print("FAILED")

# ── 저장 ──────────────────────────────────────────────────────────────────────
missing_total = [n for n in star_to_gaia if n not in results]
out_path = f"{BASE}/db/astrometry_raw.json"
with open(out_path, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n완료: {len(results)}/{len(star_to_gaia)}개 항성 저장")
if missing_total:
    print(f"누락: {missing_total}")
print(f"→ {out_path}")

errs = schema.validate(results, schema.ASTROMETRY_REQUIRED,
                       schema.ASTROMETRY_OPTIONAL, name="astrometry")
schema.report_and_exit(errs, "astrometry_raw")
