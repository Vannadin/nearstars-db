# target_list.json → Gaia DR3 TAP 배치 쿼리 + SIMBAD 폴백 → db/astrometry_raw.json
import json, math, urllib.request, urllib.parse, time, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schema

BASE      = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GAIA_TAP  = "https://gea.esac.esa.int/tap-server/tap/sync"
SIMBAD_TAP = "https://simbad.u-strasbg.fr/simbad/sim-tap/sync"

JD_GAIA   = 2457389.0   # J2016.0
JD_J2000  = 2451545.0   # J2000.0

# ── 수동 astrometry override ────────────────────────────────────────────────
# Gaia DR3 가 5-parameter 해를 못 주는 천체 (빠르고 흐린 갈색왜성 쌍, Gaia 미탐재
# 컴포넌트) 의 명시적 천체측정. HIPPARCOS_V(측광)·SIMBAD 폴백과 같은 패턴 —
# Gaia/SIMBAD 가 데이터를 못 줄 때의 출처-기반 보강. 형제 컴포넌트는 같은 거리/
# 고유운동을 공유하므로 시스템 값을 부여하고, AU 규모 상대 위치는 binary_orbit 가
# 결정한다 (build 의 kepler_thiele_innes 경로). results[name] 을 통째로 대체.
MANUAL_ASTROMETRY = {
    # Luhman 16 AB — Gaia DR3 5353626573555863424 는 2-param 해만 (parallax/PM null)
    # for this fast (~2.8"/yr), faint, ~1.5" blended pair. Position = Gaia DR3 ICRS;
    # parallax/PM = Lazorenko & Sahlmann 2018 (A&A 618 A111; arXiv 1808.07835).
    "Luhman 16 A": {
        "ra_deg": 162.3084022291181, "dec_deg": -53.3180447534979,
        "parallax_mas": 501.557, "pmra_mas_yr": -2767.502, "pmdec_mas_yr": 356.856,
        "radial_velocity_km_s": None,
        "ref": "Lazorenko & Sahlmann 2018 (parallax/PM) + Gaia DR3 (position)",
    },
    "Luhman 16 B": {
        "ra_deg": 162.3084022291181, "dec_deg": -53.3180447534979,
        "parallax_mas": 501.557, "pmra_mas_yr": -2767.502, "pmdec_mas_yr": 356.856,
        "radial_velocity_km_s": None,
        "ref": "sibling of Luhman 16 A (Lazorenko & Sahlmann 2018); relative position from binary_orbit",
    },
    # eps Ind Bb — Gaia 미탐재 (Ba+Bb ~0.7" 미분해). Ba 의 Gaia DR3 값을 형제로 공유.
    "eps Ind Bb": {
        "ra_deg": 331.07645259656397, "dec_deg": -56.79381206688221,
        "parallax_mas": 270.6580324694526, "pmra_mas_yr": 3981.97666296105,
        "pmdec_mas_yr": -2466.8318147663504, "radial_velocity_km_s": None,
        "ref": "sibling of eps Ind Ba (Gaia DR3 6412596012146801152); relative position from binary_orbit",
    },
}


# ── 수동 RV override ────────────────────────────────────────────────────────
# Gaia DR3 가 RV 를 안 주는 (밝거나·흐리거나·변광·축퇴성) 별의 시선속도를 출처-기반으로
# 보강. position/PM/parallax 는 Gaia 그대로 두고 RV 만 채운다 (MANUAL_ASTROMETRY 와 달리
# 전체 교체가 아님). RV 누락이면 공간속도가 접선 성분만 되어 운동·heliosphere 방향이
# 틀어지므로 보강. {name: {"rv": km/s, "err": km/s|None, "source": "..."}}.
MANUAL_RV = {
    "eps Eri":           {"rv": 16.376,  "err": 0.1,  "source": "Soubiran et al. 2018 (2018A&A...616A...7S)"},
    "tau Cet":           {"rv": -16.597, "err": 0.1,  "source": "Soubiran et al. 2018 (2018A&A...616A...7S)"},
    "Delta Pavonis":     {"rv": -21.543, "err": 0.1,  "source": "Soubiran et al. 2018 (2018A&A...616A...7S)"},
    "Beta Hydri":        {"rv": 23.085,  "err": 0.1,  "source": "Soubiran et al. 2018 (2018A&A...616A...7S)"},
    "gam Cep":           {"rv": -43.668, "err": 0.1,  "source": "Soubiran et al. 2018 (2018A&A...616A...7S); SB1 + planet host, systemic"},
    "Eta Cassiopeiae A": {"rv": 8.404,   "err": 0.1,  "source": "Soubiran et al. 2018 (2018A&A...616A...7S)"},
    "Mu Herculis A":     {"rv": -17.78,  "err": 0.03, "source": "Gaia DR2 RVS (2018A&A...615A..31D)"},
    "36 Ophiuchi B":     {"rv": 0.10,    "err": 0.13, "source": "Gaia DR2 (2018A&A...619A..81H)"},
    "Ross 128":          {"rv": -30.66,  "err": 0.5,  "source": "Fouque et al. 2018 SPIRou (2018MNRAS.475.1960F)"},
    "Wolf 359":          {"rv": 19.57,   "err": 1.0,  "source": "Fouque et al. 2018 SPIRou (2018MNRAS.475.1960F)"},
    "YZ Cet":            {"rv": 28.27,   "err": 0.5,  "source": "Fouque et al. 2018 SPIRou (2018MNRAS.475.1960F)"},
    "Teegarden's Star":  {"rv": 68.375,  "err": None, "source": "Zechmeister et al. 2019 CARMENES gamma (2019A&A...627A..49Z)"},
    "TRAPPIST-1":        {"rv": -56.3,   "err": None, "source": "Reiners & Basri 2009 (2009ApJ...705.1416R)"},
    "eps Ind Ba":        {"rv": -40.4,   "err": 0.9,  "source": "King et al. 2010 system RV (2010A&A...510A..99K)"},
    "eps Ind Bb":        {"rv": -40.4,   "err": 0.9,  "source": "King et al. 2010 system RV (2010A&A...510A..99K)"},
    "Luhman 16 A":       {"rv": 23.1,    "err": 1.1,  "source": "Kniazev et al. 2013 (2013ApJ...770..124K)"},
    "Luhman 16 B":       {"rv": 19.5,    "err": 1.2,  "source": "Kniazev et al. 2013 (2013ApJ...770..124K)"},
    "Sirius B":          {"rv": -5.50,   "err": 0.4,  "source": "Gontcharov 2006 PCRV, Sirius A system (2006AstL...32..759G)"},
    "40 Eridani B":      {"rv": -42.27,  "err": 0.1,  "source": "Gaia DR2, 40 Eri A system (2018A&A...616A...7S)"},
    "Van Maanen's Star": {"rv": -12.0,   "err": 7.0,  "source": "Lindegren & Dravins 2021 astrometric RV, grav-redshift-free (2021A&A...652A..45L)"},
    # PSR J0108-1431: pulsar — no spectroscopic RV exists; left null (stays 0).
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


def main():
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

    # ── 이진성 sibling backfill ────────────────────────────────────────────────────
    # 일부 SIMBAD 항목 (예: Procyon B) 은 primary 만 parallax 보유. 같은 시스템 사이의
    # 형제 컴포넌트는 같은 거리에 있으므로 missing parallax 를 primary 값으로 보완.
    for entry in target_list:
        comps = entry["components"]
        if len(comps) < 2:
            continue
        # primary (가장 정보 많은 컴포넌트) 식별
        best = None
        for c in comps:
            r = results.get(c, {})
            if r.get("parallax_mas") is not None:
                if best is None or r.get("parallax_mas") > best[1]:
                    best = (c, r.get("parallax_mas"))
        if not best:
            continue
        primary, plx = best
        for c in comps:
            r = results.get(c, {})
            if not r or r.get("parallax_mas") is not None:
                continue
            # backfill from primary
            pr = results[primary]
            r["parallax_mas"] = pr["parallax_mas"]
            r["parallax_error_mas"] = pr.get("parallax_error_mas")
            if r.get("radial_velocity_km_s") is None:
                r["radial_velocity_km_s"] = pr.get("radial_velocity_km_s")
                r["radial_velocity_source"] = pr.get("radial_velocity_source")
            # source 표기 명시
            r["sibling_backfill"] = f"parallax/rv from {primary}"
            print(f"  sibling backfill: {c} ← {primary} (plx={plx})")

    # ── 수동 override 적용 (Gaia/SIMBAD/backfill 보다 우선) ───────────────────────
    print("\n수동 astrometry override:")
    for name, m in MANUAL_ASTROMETRY.items():
        if name not in star_to_gaia:
            continue  # target_list 에 없는 이름은 무시
        results[name] = {
            "source":                "manual",
            "source_id":             None,
            "epoch_jd":              JD_GAIA,
            "epoch_label":           "J2016.0",
            "ra_deg":                m["ra_deg"],
            "ra_error_mas":          None,
            "dec_deg":               m["dec_deg"],
            "dec_error_mas":         None,
            "parallax_mas":          m["parallax_mas"],
            "parallax_error_mas":    None,
            "pmra_mas_yr":           m["pmra_mas_yr"],
            "pmra_error_mas_yr":     None,
            "pmdec_mas_yr":          m["pmdec_mas_yr"],
            "pmdec_error_mas_yr":    None,
            "radial_velocity_km_s":  m.get("radial_velocity_km_s"),
            "rv_error_km_s":         None,
            "manual_ref":            m["ref"],
        }
        print(f"  {name}: plx={m['parallax_mas']} mas ({m['ref']})")

    # ── 수동 RV override 적용 (Gaia/SIMBAD RV 가 없을 때만 보강) ──────────────────
    print("\n수동 RV override:")
    for name, m in MANUAL_RV.items():
        r = results.get(name)
        if not r:
            continue
        if r.get("radial_velocity_km_s") is None:
            r["radial_velocity_km_s"] = m["rv"]
            r["rv_error_km_s"] = m.get("err")
            r["radial_velocity_source"] = m["source"]
            print(f"  {name}: RV={m['rv']} km/s ({m['source']})")

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


if __name__ == "__main__":
    main()
