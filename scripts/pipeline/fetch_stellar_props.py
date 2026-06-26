# target_list.json → SIMBAD (스펙형, Teff, mesDiameter) → db/stellar_props_raw.json
import json, urllib.request, urllib.parse, os, math, time, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schema

BASE       = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SIMBAD_TAP = "https://simbad.u-strasbg.fr/simbad/sim-tap/sync"
PC_TO_KM   = 3.085677581491e13
R_SUN_KM   = 695700.0

METHOD_PRIORITY = {
    "interferometry": 1, "eclipsing_binary": 2, "binary_orbit": 2,
    "sed_fitting": 3, "spectroscopic": 4, "evolutionary_model": 5,
    "spectroscopic_calibration": 6,
    "unverified": 99,  # Phase 1 batch에서 method 검증 안 함 — 항상 최하위
}


def tap_post(query, timeout=60):
    data = urllib.parse.urlencode(
        {"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json", "QUERY": query}
    ).encode()
    req = urllib.request.Request(SIMBAD_TAP, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def tap_rows(resp):
    cols = [m["name"] for m in resp["metadata"]]
    return [dict(zip(cols, row)) for row in resp["data"]]

def diam_to_rsun(diam_mas, parallax_mas):
    try:
        dist_pc = 1000.0 / parallax_mas
        angular_radius_rad = (float(diam_mas) / 2) * (math.pi / 648_000_000)
        return round(angular_radius_rad * dist_pc * PC_TO_KM / R_SUN_KM, 4)
    except (ValueError, TypeError, ZeroDivisionError):
        return None

def name_list(names):
    return ", ".join(f"'{n.replace(chr(39), chr(39)+chr(39))}'" for n in names)

def oid_list(oids):
    return ", ".join(str(o) for o in oids)


# ── 입력 로드 ──────────────────────────────────────────────────────────────────


def main():
    with open(f"{BASE}/db/target_list.json") as f:
        target_list = json.load(f)

    all_stars = []
    for entry in target_list:
        all_stars.extend(entry["components"])

    with open(f"{BASE}/db/astrometry_raw.json") as f:
        astrometry = json.load(f)

    results = {name: {
        "teff_k": None,
        "teff_bibcode": None,
        "spectype": None,
        "mass_measurements": [],
        "radius_measurements": [],
    } for name in all_stars}


    # ── 0. 이름 → OID 매핑 ────────────────────────────────────────────────────────
    # SIMBAD는 쿼리 이름을 내부적으로 해석하므로 반환 id가 입력 이름과 다를 수 있음.
    # 개별 쿼리로 name → oidref를 확실하게 매핑한다.
    # target_list.json 이름으로 SIMBAD에서 찾을 수 없는 별의 별칭 매핑
    SIMBAD_ALIASES = {
        "40 Eridani A":               "GJ 166 A",
        "Chi-1 Orionis A":            "chi01 Ori",
        "Kapteyn":                    "Kapteyn's Star",
        "Mu Herculis A":              "mu Her A",
        "COCONUTS-2 A":               "COCONUTS-2A",
        "eps Ind A":                  "GJ 845 A",
        "WISEP J121756.91+162640.2 A":"WISE J121756.90+162640.8",
        # Brown-dwarf binaries: SIMBAD only catalogs the unresolved pair, so the
        # primary aliases to the system entry and the secondary (B/Bb) has no SIMBAD
        # record -> curated-only (expected WARN; teff/spectype/mass come from curated).
        "Luhman 16 A":                "Luhman 16",
        "eps Ind Ba":                 "eps Ind B",
        # 50ly 이내 유명 비-호스트
        "Arcturus":                   "alf Boo",
        "Capella":                    "alf Aur",
        "Procyon A":                  "alf CMi",
        "Procyon B":                  "alf CMi B",
        "70 Ophiuchi A":              "70 Oph A",
        "70 Ophiuchi B":              "70 Oph B",
        "Van Maanen's Star":          "Wolf 28",
    }

    name_to_oid = {}   # our_name → oid
    oid_to_name = {}   # oid → our_name

    # 별별 OID 조회. SIMBAD ident는 alias 정규화를 수행하므로 정확 매칭은
    # 단일 쿼리가 가장 안정적 (배치 IN/UNION ALL 모두 회귀 발생 확인).
    # sleep을 0.2 → 0.1로 줄여 ~14초 단축.
    print(f"SIMBAD OID 매핑 중 ({len(all_stars)}개 항성)...")
    for idx, star_name in enumerate(all_stars):
        lookup = SIMBAD_ALIASES.get(star_name, star_name)
        safe = lookup.replace("'", "''")
        q = f"SELECT oidref FROM ident WHERE id = '{safe}'"
        try:
            rows = tap_rows(tap_post(q))
            if rows:
                oid = rows[0]["oidref"]
                name_to_oid[star_name] = oid
                oid_to_name[oid] = star_name
        except Exception as e:
            print(f"  [{idx+1}] {star_name}: 오류 {e}")
        time.sleep(0.1)

    print(f"  → 매핑 완료: {len(name_to_oid)}/{len(all_stars)}개")
    not_found = [s for s in all_stars if s not in name_to_oid]
    if not_found:
        print(f"  → SIMBAD에 없음 ({len(not_found)}개): {not_found}")

    all_oids = list(oid_to_name.keys())
    OID_CHUNK = 50


    # ── 1. 스펙형 (basic 테이블) ──────────────────────────────────────────────────
    print(f"\nSIMBAD 스펙형 쿼리 중...")
    for i in range(0, len(all_oids), OID_CHUNK):
        chunk_oids = all_oids[i:i+OID_CHUNK]
        q = f"""
    SELECT oid, sp_type
    FROM basic
    WHERE oid IN ({oid_list(chunk_oids)})
    AND sp_type IS NOT NULL
    """.strip()
        try:
            rows = tap_rows(tap_post(q))
            found = 0
            for row in rows:
                our_name = oid_to_name.get(row["oid"])
                if our_name and our_name in results:
                    results[our_name]["spectype"] = row["sp_type"]
                    found += 1
            print(f"  스펙형 배치 {i//OID_CHUNK+1}: {found}개")
        except Exception as e:
            print(f"  스펙형 배치 {i//OID_CHUNK+1} 오류: {e}")
        time.sleep(0.5)


    # ── 2. Teff (mesFe_H 테이블) ─────────────────────────────────────────────────
    # 별마다 첫 번째 값만 사용 (curated에서 정밀값으로 덮어씌울 예정)
    print(f"\nSIMBAD Teff 쿼리 중...")
    for i in range(0, len(all_oids), OID_CHUNK):
        chunk_oids = all_oids[i:i+OID_CHUNK]
        q = f"""
    SELECT oidref, teff, bibcode
    FROM mesFe_H
    WHERE oidref IN ({oid_list(chunk_oids)})
    AND teff IS NOT NULL
    """.strip()
        try:
            rows = tap_rows(tap_post(q))
            found = set()
            for row in rows:
                our_name = oid_to_name.get(row["oidref"])
                if our_name and our_name in results and our_name not in found:
                    results[our_name]["teff_k"] = int(row["teff"]) if row["teff"] else None
                    results[our_name]["teff_bibcode"] = row.get("bibcode")
                    found.add(our_name)
            print(f"  Teff 배치 {i//OID_CHUNK+1}: {len(found)}개")
        except Exception as e:
            print(f"  Teff 배치 {i//OID_CHUNK+1} 오류: {e}")
        time.sleep(0.5)


    # ── 3. mesDiameter (간섭계 각지름 → R☉) ─────────────────────────────────────
    print(f"\nSIMBAD mesDiameter 쿼리 중...")
    for i in range(0, len(all_oids), OID_CHUNK):
        chunk_oids = all_oids[i:i+OID_CHUNK]
        q = f"""
    SELECT oidref, diameter, bibcode
    FROM mesDiameter
    WHERE oidref IN ({oid_list(chunk_oids)})
    AND diameter IS NOT NULL
    AND unit LIKE 'mas%'
    """.strip()
        try:
            rows = tap_rows(tap_post(q))
            count = 0
            for row in rows:
                our_name = oid_to_name.get(row["oidref"])
                if not our_name or our_name not in results:
                    continue
                plx = (astrometry.get(our_name) or {}).get("parallax_mas")
                if not plx:
                    continue
                r_rsun = diam_to_rsun(row["diameter"], plx)
                if not r_rsun or r_rsun <= 0:
                    continue
                bc = str(row.get("bibcode", "")).strip()
                results[our_name]["radius_measurements"].append({
                    "value_rsun":       r_rsun,
                    "uncertainty_rsun": None,
                    "method":           "interferometry",
                    "reference":        bc,
                    "doi":              None,
                    "bibcode":          bc,
                    "recommended":      False,
                })
                count += 1
            print(f"  mesDiameter 배치 {i//OID_CHUNK+1}: {count}개 측정값")
        except Exception as e:
            print(f"  mesDiameter 배치 {i//OID_CHUNK+1} 오류: {e}")
        time.sleep(0.5)

    # recommended 설정 (메서드 우선순위 기준 상위 1개)
    for props in results.values():
        meas = props["radius_measurements"]
        if not meas:
            continue
        for m in meas:
            m["recommended"] = False
        best = min(range(len(meas)),
                   key=lambda i: METHOD_PRIORITY.get(meas[i].get("method", ""), 9))
        meas[best]["recommended"] = True


    # ── 저장 ──────────────────────────────────────────────────────────────────────
    out_path = f"{BASE}/db/stellar_props_raw.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    n_teff   = sum(1 for v in results.values() if v["teff_k"])
    n_spec   = sum(1 for v in results.values() if v["spectype"])
    n_radius = sum(1 for v in results.values() if v["radius_measurements"])
    print(f"\n완료: {len(results)}개 항성")
    print(f"  Teff:    {n_teff}/{len(results)}")
    print(f"  스펙형:  {n_spec}/{len(results)}")
    print(f"  반지름:  {n_radius}/{len(results)} (mesDiameter)")
    print(f"  질량:    0/{len(results)} (stellar_props_curated.json에서 입력 필요)")
    print(f"→ {out_path}")

    errs = schema.validate(results, schema.STELLAR_PROPS_REQUIRED,
                           schema.STELLAR_PROPS_OPTIONAL, name="stellar_props",
                           measurement_keys=("mass_measurements", "radius_measurements"))
    schema.report_and_exit(errs, "stellar_props_raw")


if __name__ == "__main__":
    main()
