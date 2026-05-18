# target_list.json → Gaia G+BP-RP → V등급 변환 + 밝은 별 Hipparcos 하드코딩 → db/photometry_raw.json
import json, urllib.request, urllib.parse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schema

BASE      = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GAIA_TAP  = "https://gea.esac.esa.int/tap-server/tap/sync"

# Gaia가 포화(saturated)된 밝은 별의 Hipparcos V등급 하드코딩
# G < ~6 이면 Gaia 측광 불신뢰
HIPPARCOS_V = {
    "Sirius A":      -1.46,
    "Alpha Centauri A": -0.01,
    "Alpha Centauri B":  1.33,
    "Vega":           0.03,
    "Altair":         0.77,
    "Fomalhaut":      1.16,
    "Sirius B":       8.44,
    "Procyon A":      0.34,
    # Gaia DR3 미포함 적색왜성 — Hipparcos / 측광 카탈로그 문헌값
    "GJ 411":         7.47,   # Lalande 21185, HIP 54035
    "GJ 273":         9.87,   # Luyten's Star, HIP 36208
    "HD 62509":       1.14,   # Pollux, HIP 37826
}


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


def gaia_to_vmag(g, bp_rp):
    """Gaia G + (BP-RP) → Johnson V 변환 (Evans et al. 2018 Eq. A.1)."""
    c = bp_rp
    return g - (-0.02704 + 0.01424*c - 0.2156*c**2 + 0.01426*c**3)


# ── 입력 로드 ──────────────────────────────────────────────────────────────────
with open(f"{BASE}/db/target_list.json") as f:
    target_list = json.load(f)

star_to_gaia = {}
for entry in target_list:
    comps = entry["components"]
    gids  = entry.get("gaia_source_ids", [])
    for i, comp in enumerate(comps):
        star_to_gaia[comp] = gids[i] if i < len(gids) else None

gaia_stars = {name: gid for name, gid in star_to_gaia.items() if gid}

# ── Gaia 측광 배치 쿼리 ────────────────────────────────────────────────────────
print(f"Gaia 측광 쿼리: {len(gaia_stars)}개")

CHUNK = 1000
gaia_ids = list(gaia_stars.values())
gaia_names_by_id = {gid: name for name, gid in gaia_stars.items()}
gaia_phot = {}  # source_id → {g_mag, bp_rp}

for i in range(0, len(gaia_ids), CHUNK):
    chunk = gaia_ids[i:i+CHUNK]
    id_list = ", ".join(chunk)
    q = f"""
SELECT source_id, phot_g_mean_mag, bp_rp
FROM gaiadr3.gaia_source
WHERE source_id IN ({id_list})
""".strip()
    try:
        rows = tap_rows(tap_post(GAIA_TAP, q, timeout=90))
        for row in rows:
            gaia_phot[str(row["source_id"])] = {
                "g_mag":  row["phot_g_mean_mag"],
                "bp_rp":  row["bp_rp"],
            }
        print(f"  배치 {i//CHUNK+1}: {len(rows)}개 반환")
    except Exception as e:
        print(f"  Gaia 측광 오류 (배치 {i//CHUNK+1}): {e}")

# ── 결과 조립 ──────────────────────────────────────────────────────────────────
results = {}

for name, gid in star_to_gaia.items():
    # Hipparcos 하드코딩 우선 (Gaia 포화 별)
    if name in HIPPARCOS_V:
        results[name] = {
            "g_mag":       None,
            "bp_rp":       None,
            "vmag_v":      HIPPARCOS_V[name],
            "vmag_source": "hipparcos_hardcoded",
        }
        continue

    if gid and gid in gaia_phot:
        phot = gaia_phot[gid]
        g    = phot["g_mag"]
        bprp = phot["bp_rp"]
        if g is not None and bprp is not None:
            vmag = round(gaia_to_vmag(g, bprp), 4)
            results[name] = {
                "g_mag":       round(g, 4),
                "bp_rp":       round(bprp, 4),
                "vmag_v":      vmag,
                "vmag_source": "gaia_dr3_converted",
            }
        elif g is not None:
            # BP-RP 없으면 G ≈ V 근사 (M형 별 등)
            results[name] = {
                "g_mag":       round(g, 4),
                "bp_rp":       None,
                "vmag_v":      round(g, 4),
                "vmag_source": "gaia_g_approx",
            }
        else:
            results[name] = {
                "g_mag": None, "bp_rp": None,
                "vmag_v": None, "vmag_source": "unavailable",
            }
    else:
        results[name] = {
            "g_mag": None, "bp_rp": None,
            "vmag_v": None, "vmag_source": "no_gaia_id",
        }

# ── 저장 ──────────────────────────────────────────────────────────────────────
out_path = f"{BASE}/db/photometry_raw.json"
with open(out_path, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

n_ok = sum(1 for v in results.values() if v["vmag_v"] is not None)
print(f"\n완료: {n_ok}/{len(results)}개 항성 vmag_v 확보")
print(f"→ {out_path}")

errs = schema.validate(results, schema.PHOTOMETRY_REQUIRED,
                       schema.PHOTOMETRY_OPTIONAL, name="photometry")
schema.report_and_exit(errs, "photometry_raw")
