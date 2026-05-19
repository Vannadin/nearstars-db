#!/usr/bin/env python3
# 별 이름 입력 → SIMBAD ident → Gaia DR3 source_id + 기본 정보 조회. 사전 조사 단계 자동화.
"""
Usage: lookup_gaia.py "<star name>"

Looks up a star by common name and returns information needed to add it
to the NearStars target_list.json:
- SIMBAD canonical name (in case alias is needed)
- Gaia DR3 source_id (if any)
- Distance (parsecs and light-years)
- V magnitude (if available)
- Spectral type
- Component flag (for binary identification)

Exits non-zero if the star can't be found in SIMBAD. Distance is reported
but never causes exit — DB collection is distance-agnostic.
"""
import sys
import json
import urllib.request
import urllib.parse

SIMBAD_TAP = "https://simbad.u-strasbg.fr/simbad/sim-tap/sync"
GAIA_TAP   = "https://gea.esac.esa.int/tap-server/tap/sync"
PC_TO_LY   = 3.26156


def tap_query(endpoint, query, timeout=30):
    data = urllib.parse.urlencode({
        "REQUEST": "doQuery",
        "LANG":    "ADQL",
        "FORMAT":  "json",
        "QUERY":   query,
    }).encode()
    req = urllib.request.Request(endpoint, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def tap_rows(resp):
    cols = [m["name"] for m in resp["metadata"]]
    return [dict(zip(cols, row)) for row in resp["data"]]


def find_simbad_oid(name):
    """별 이름 → SIMBAD oid + canonical main_id."""
    safe = name.replace("'", "''")
    q = f"""
SELECT b.oid, b.main_id, b.ra, b.dec, b.plx_value, b.sp_type
FROM basic b
JOIN ident i ON i.oidref = b.oid
WHERE i.id = '{safe}'
""".strip()
    rows = tap_rows(tap_query(SIMBAD_TAP, q))
    if not rows:
        return None
    return rows[0]


def find_v_mag(oid):
    """SIMBAD allfluxes 테이블에서 V mag 조회."""
    q = f"SELECT V FROM allfluxes WHERE oidref = {oid}"
    try:
        rows = tap_rows(tap_query(SIMBAD_TAP, q))
        if rows and rows[0]["V"] is not None:
            return rows[0]["V"]
    except Exception:
        pass
    return None


def find_gaia_source_id(oid):
    """SIMBAD oid → Gaia DR3 source_id via ident table."""
    q = f"""
SELECT id
FROM ident
WHERE oidref = {oid}
AND id LIKE 'Gaia DR3 %'
""".strip()
    rows = tap_rows(tap_query(SIMBAD_TAP, q))
    if not rows:
        return None
    # "Gaia DR3 <number>" → extract number
    full_id = rows[0]["id"]
    return full_id.replace("Gaia DR3 ", "").strip()


def find_components(main_id):
    """동일 시스템의 다른 컴포넌트 식별. WDS 정보로 단성/다성 추정."""
    # Strip trailing component letter to check for siblings
    base = main_id.rstrip(" ABCDEF").rstrip()
    if base == main_id:
        return None  # single, no component letter
    safe = base.replace("'", "''")
    q = f"""
SELECT DISTINCT i.id
FROM ident i
JOIN basic b ON i.oidref = b.oid
WHERE i.id LIKE '{safe}%'
AND (i.id LIKE '%A' OR i.id LIKE '%B' OR i.id LIKE '%C')
""".strip()
    rows = tap_rows(tap_query(SIMBAD_TAP, q))
    return [r["id"] for r in rows] or None


def main():
    if len(sys.argv) != 2:
        print("Usage: lookup_gaia.py \"<star name>\"", file=sys.stderr)
        sys.exit(2)

    name = sys.argv[1]
    print(f"Looking up: {name}\n")

    info = find_simbad_oid(name)
    if not info:
        print(f"  ERROR: SIMBAD has no record for '{name}'", file=sys.stderr)
        print(f"  Try alternate names or check spelling", file=sys.stderr)
        sys.exit(1)

    print(f"  SIMBAD canonical: {info['main_id']}")
    if info["main_id"] != name:
        print(f"  → SIMBAD canonical name differs from input.")
        print(f"     If `fetch_stellar_props.py` reports this star as 'SIMBAD에 없음',")
        print(f"     add to SIMBAD_ALIASES — but review the canonical first:")
        print(f"     some SIMBAD entries have quirks (extra spaces, '*' prefix, etc.)")
        print(f"     that you may want to normalize before adding as alias.")

    plx = info.get("plx_value")
    if plx and plx > 0:
        dist_pc = 1000.0 / plx
        dist_ly = dist_pc * PC_TO_LY
        print(f"  Distance:        {dist_pc:.2f} pc  ({dist_ly:.2f} ly)")
        if dist_ly > 50:
            print(f"  NOTE: > 50 ly — Kopernicus cfg writer will skip (out of range).")
            print(f"        Principia cfg writer may include as perturber if ≤ 80 ly.")
            print(f"        DB collection proceeds regardless — note distance in meta.notes.")
    else:
        print(f"  Distance:        unknown (no parallax)")

    v = find_v_mag(info["oid"])
    if v is not None:
        print(f"  V magnitude:     {v:.2f}")
        if v < 6:
            print(f"  → bright star — may be Gaia-saturated, check HIPPARCOS_V hardcode")
    else:
        print(f"  V magnitude:     unknown")

    sp = info.get("sp_type") or "unknown"
    print(f"  Spectral type:   {sp}")

    gaia_id = find_gaia_source_id(info["oid"])
    if gaia_id:
        print(f"  Gaia DR3 ID:     {gaia_id}")
    else:
        print(f"  Gaia DR3 ID:     not in SIMBAD ident table")
        print(f"  → try Gaia archive direct search, or use empty gaia_source_ids[] for SIMBAD fallback")

    siblings = find_components(info["main_id"])
    is_multi = bool(siblings and len(siblings) > 1)
    if is_multi:
        print(f"\n  Other components found in SIMBAD: {sorted(siblings)}")
        print(f"  → likely multiple system; confirm the full component list manually")

    print(f"\nReady for target_list.json (using your input name — adapt as needed):")
    # 입력 이름을 사용. 다성계라면 user가 직접 components 채울 것을 가정
    if is_multi:
        # try to derive A/B/C from input name; fallback to input + "?"
        last_token = name.strip().split()[-1] if name.strip().split() else ""
        if last_token in "ABCDEF":
            base = " ".join(name.strip().split()[:-1])
            comps = [f"{base} {c}" for c in sorted(set(s.strip()[-1] for s in siblings if s.strip()[-1] in "ABCDEF"))]
        else:
            comps = [name]  # user must fill in
        sys_name = " ".join(name.strip().split()[:-1]) if last_token in "ABCDEF" else name
    else:
        comps = [name]
        sys_name = name

    print(json.dumps({
        "system": sys_name,
        "components": comps,
        "gaia_source_ids": [gaia_id or None] + [None] * (len(comps) - 1),
        "hip_ids": [],
        "binary": is_multi,
    }, indent=2))


if __name__ == "__main__":
    main()
