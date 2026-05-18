# raw 파일들을 조합해 db/systems/*.json 재생성. B1950+J2000 전파, vmag_v 포함.
import json, math, re, os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB   = os.path.join(BASE, "db")

# ── 상수 ──────────────────────────────────────────────────────────────────────
PC_TO_KM      = 3.085677581491e13
AU_TO_M       = 1.495978707e11
GM_SUN        = 1.32712440018e11   # km³/s²
R_SUN_KM      = 695700.0
M_EARTH_KG    = 5.9722e24
R_EARTH_M     = 6.371e6
DEG_TO_RAD    = math.pi / 180.0
YR_TO_S       = 365.25 * 86400.0
ULP           = 2.0 ** -52

JD_GAIA       = 2457389.0   # J2016.0
JD_J2000      = 2451545.0   # J2000.0
JD_B1950      = 2433282.5   # B1950.0 (Sol/RSS 에포크)
RETRIEVAL_DATE = __import__("datetime").date.today().isoformat()

# 고정 소스 항목
SRC_BUTKEVICH = {
    "title": "Butkevich & Lindegren (2014): Relativistic aspects of stellar kinematics",
    "doi": "10.1051/0004-6361/201424483", "bibcode": "2014A&A...570A..62B",
    "accessed": RETRIEVAL_DATE, "used_for": ["epoch propagation method"],
}
SRC_GAIA = {
    "title": "Gaia Data Release 3",
    "doi": "10.1051/0004-6361/202243940", "bibcode": "2023A&A...674A...1G",
    "accessed": RETRIEVAL_DATE,
    "used_for": ["astrometry (ra, dec, parallax, pmra, pmdec, radial_velocity)"],
}
SRC_SIMBAD = {
    "title": "SIMBAD Astronomical Database (Wenger et al. 2000)",
    "doi": "10.1051/aas:2000332", "bibcode": "2000A&AS..143....9W",
    "accessed": RETRIEVAL_DATE,
    "used_for": ["astrometry (ra, dec, parallax, pmra, pmdec, rv)"],
}
SRC_ARCHIVE = {
    "title": "NASA Exoplanet Archive",
    "doi": None, "bibcode": None,
    "url": "https://exoplanetarchive.ipac.caltech.edu",
    "accessed": RETRIEVAL_DATE, "used_for": ["planet parameters"],
}


# ── 물리 함수 ─────────────────────────────────────────────────────────────────

def to_icrf(ra_deg, dec_deg, parallax_mas, pmra_mas_yr, pmdec_mas_yr, rv_km_s):
    """아스트로메트리 관측값 → SSB-ICRF Cartesian (km, km/s)."""
    ra  = ra_deg  * DEG_TO_RAD
    dec = dec_deg * DEG_TO_RAD
    dist_km = (1000.0 / parallax_mas) * PC_TO_KM
    cr, sr = math.cos(ra), math.sin(ra)
    cd, sd = math.cos(dec), math.sin(dec)
    x = dist_km * cd * cr
    y = dist_km * cd * sr
    z = dist_km * sd
    pmra_rs  = (pmra_mas_yr  / 3.6e6) * DEG_TO_RAD / YR_TO_S
    pmdec_rs = (pmdec_mas_yr / 3.6e6) * DEG_TO_RAD / YR_TO_S
    e_ra  = [-sr,       cr,     0.0]
    e_dec = [-sd*cr,   -sd*sr,  cd ]
    e_r   = [ cd*cr,    cd*sr,  sd ]
    vx = dist_km*(pmra_rs*e_ra[0] + pmdec_rs*e_dec[0]) + rv_km_s*e_r[0]
    vy = dist_km*(pmra_rs*e_ra[1] + pmdec_rs*e_dec[1]) + rv_km_s*e_r[1]
    vz = dist_km*(pmra_rs*e_ra[2] + pmdec_rs*e_dec[2]) + rv_km_s*e_r[2]
    return (x, y, z), (vx, vy, vz)


def propagate(pos, vel, dt_s):
    """선형 전파: pos(t0 + dt)."""
    return tuple(p + v*dt_s for p, v in zip(pos, vel))


def ulp_km(pos):
    return abs(max(pos, key=abs)) * ULP


def to_filename(name):
    s = name.lower()
    s = s.replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_") + ".json"


# 컴포넌트 글자 추출용 패턴 (예: "Alpha Centauri A" → "A")
COMPONENT_RE = re.compile(r"^.+\s+([A-Z])$")

# 알려진 선형 전파 한계 노트 (Barnard's Star perspective acceleration 등)
PROPAGATION_NOTES = {
    "Barnard's star": (
        "Linear propagation accumulates ~0.5 AU position error over "
        "66 years from perspective acceleration (μ≈10,300 mas/yr, "
        "ϖ≈548 mas, RV≈−110 km/s). Within perturber tolerance for "
        "KSP. For sub-AU accuracy, override with JPL Horizons state "
        "vector at JD2433282.5."
    ),
}


def coalesce(*candidates):
    """첫 번째 non-None 값을 반환. 키 부재와 명시적 None 구분 안 함."""
    for v in candidates:
        if v is not None:
            return v
    return None


def build_planet_derived(pl, curated=None):
    """행성 raw + curated → 단위 변환된 derived 블록.
    우선순위: curated > tepcat > nasa_archive (raw).
    측정 없는 값은 null 유지 (기본값 가정은 Kopernicus 작성 단계의 책임)."""
    c_orb = (curated or {}).get("orbital") or {}
    c_phy = (curated or {}).get("physical") or {}
    tep   = pl.get("tepcat") or {}

    sma_au  = coalesce(c_orb.get("semi_major_axis_au"),
                       tep.get("semi_major_axis_au"),
                       pl.get("semi_major_axis_au"))
    ecc     = coalesce(c_orb.get("eccentricity"),
                       tep.get("eccentricity"),
                       pl.get("eccentricity"))
    incl    = coalesce(c_orb.get("inclination_deg"),
                       pl.get("inclination_deg"))
    mass_me = coalesce(c_phy.get("true_mass_mearth"),
                       c_phy.get("mass_mearth"),
                       tep.get("mass_mearth"),
                       pl.get("mass_mearth"))
    rad_re  = coalesce(c_phy.get("radius_rearth"),
                       tep.get("radius_rearth"),
                       pl.get("radius_rearth"))

    return {
        "semi_major_axis_m":               sma_au * AU_TO_M if sma_au is not None else None,
        "eccentricity":                    ecc,
        "inclination_deg":                 incl,
        "longitude_of_ascending_node_deg": c_orb.get("longitude_of_ascending_node_deg"),
        "argument_of_periapsis_deg":       c_orb.get("argument_of_periapsis_deg"),
        "mean_anomaly_at_epoch_deg":       c_orb.get("mean_anomaly_at_epoch_deg"),
        "orbital_epoch_jd":                c_orb.get("epoch_jd"),
        "mass_kg":                         mass_me * M_EARTH_KG if mass_me is not None else None,
        "mass_type":                       c_phy.get("mass_type") or pl.get("mass_type"),
        "radius_m":                        rad_re * R_EARTH_M if rad_re is not None else None,
    }


# ── 데이터 로드 ───────────────────────────────────────────────────────────────
def load_json(path):
    with open(path) as f:
        return json.load(f)

astrometry    = load_json(f"{DB}/astrometry_raw.json")
photometry    = load_json(f"{DB}/photometry_raw.json")
stellar_props = load_json(f"{DB}/stellar_props_raw.json")
planets_raw   = load_json(f"{DB}/planets_raw.json")

_sc_path = f"{DB}/stellar_props_curated.json"
stellar_curated = load_json(_sc_path) if os.path.exists(_sc_path) else {}
binary_orbits = load_json(f"{DB}/binary_orbits.json")

_curated_path = f"{DB}/planets_curated.json"
planets_curated = load_json(_curated_path) if os.path.exists(_curated_path) else {}

os.makedirs(f"{DB}/systems", exist_ok=True)

errors   = []
written  = 0

# ── 항성별 시스템 JSON 생성 ───────────────────────────────────────────────────
with open(f"{BASE}/db/target_list.json") as f:
    target_list = json.load(f)

for target in target_list:
    sys_name  = target["system"]
    comps     = target["components"]
    is_binary = target["binary"]

    # 다성계: 대표 컴포넌트(첫 번째)에 binary_orbit 전체 임베드,
    # 다른 컴포넌트는 ref만 저장
    binary_data = binary_orbits.get(sys_name) if is_binary else None
    if is_binary and binary_data is None:
        errors.append(f"{sys_name}: binary=true이나 binary_orbits.json에 항목 없음")
        print(f"  [WARN] {sys_name}: binary_orbits.json 항목 없음")
    primary_comp  = comps[0] if is_binary else None
    primary_fname = to_filename(primary_comp) if primary_comp else None

    # 단일 항성 시스템: 항성 1개씩 개별 파일
    # 다성계도 현재 구조 유지 (컴포넌트별 개별 파일)
    for star_name in comps:
        fname = to_filename(star_name)
        astro = astrometry.get(star_name)
        phot  = photometry.get(star_name, {})
        props   = stellar_props.get(star_name, {})
        curated = stellar_curated.get(star_name, {})
        # curated 값이 있으면 raw보다 우선 적용
        teff_k      = curated.get("teff_k")      or props.get("teff_k")
        spectype    = curated.get("spectype")    or props.get("spectype")
        mass_meas   = curated.get("mass_measurements")   or props.get("mass_measurements", [])
        radius_meas = curated.get("radius_measurements") or props.get("radius_measurements", [])
        planet_list = planets_raw.get(star_name, []) or planets_raw.get(sys_name, [])

        if not astro:
            errors.append(f"{star_name}: astrometry_raw에 없음 — 건너뜀")
            print(f"  [SKIP] {star_name}: 아스트로메트리 없음")
            continue

        plx = astro.get("parallax_mas")
        if not plx or plx <= 0:
            errors.append(f"{star_name}: parallax ≤ 0 — 건너뜀")
            print(f"  [SKIP] {star_name}: parallax 이상")
            continue

        # RV 결정
        rv = astro.get("radial_velocity_km_s")
        rv_source = astro.get("source", "unknown")
        if rv is None:
            rv = 0.0
            rv_source += " (RV 없음 → 0으로 처리)"

        # ── 에포크 전파 ──
        source_epoch_jd = astro.get("epoch_jd", JD_GAIA)
        try:
            pos0, vel = to_icrf(
                astro["ra_deg"], astro["dec_deg"],
                plx,
                astro["pmra_mas_yr"], astro["pmdec_mas_yr"],
                rv
            )
        except (ZeroDivisionError, ValueError) as e:
            errors.append(f"{star_name}: ICRF 변환 오류 — {e}")
            continue

        # source → B1950
        dt_b1950 = (JD_B1950 - source_epoch_jd) * 86400.0
        pos_b1950 = propagate(pos0, vel, dt_b1950)

        # source → J2000
        dt_j2000 = (JD_J2000 - source_epoch_jd) * 86400.0
        pos_j2000 = propagate(pos0, vel, dt_j2000)

        dist_pc = 1000.0 / plx

        # ── raw 블록 ──
        raw_block = {
            "source":                  astro.get("source", "unknown"),
            "source_id":               astro.get("source_id"),
            "epoch_jd":                source_epoch_jd,
            "epoch_label":             astro.get("epoch_label", "J2016.0"),
            "ra_deg":                  astro["ra_deg"],
            "dec_deg":                 astro["dec_deg"],
            "parallax_mas":            plx,
            "parallax_error_mas":      astro.get("parallax_error_mas"),
            "pmra_mas_yr":             astro["pmra_mas_yr"],
            "pmdec_mas_yr":            astro["pmdec_mas_yr"],
            "radial_velocity_km_s":    rv,
            "radial_velocity_source":  rv_source,
            "vmag_v":                  phot.get("vmag_v"),
            "vmag_source":             phot.get("vmag_source"),
            "teff_k":                  teff_k,
            "spectype":                spectype,
            "mass_measurements":       mass_meas,
            "radius_measurements":     radius_meas,
        }

        # ── derived 블록 (B1950, J2000 모두 포함) ──
        derived_block = {
            "epoch_jd":           JD_B1950,
            "epoch_label":        "B1950.0",
            "propagation_method": "linear",
            "distance_pc":        dist_pc,
            "distance_km":        dist_pc * PC_TO_KM,
            # B1950 좌표 (Kopernicus/Principia용)
            "icrs_x_km":          pos_b1950[0],
            "icrs_y_km":          pos_b1950[1],
            "icrs_z_km":          pos_b1950[2],
            "icrs_vx_km_s":       vel[0],
            "icrs_vy_km_s":       vel[1],
            "icrs_vz_km_s":       vel[2],
            "position_ulp_km":    ulp_km(pos_b1950),
            # J2000 좌표 (참조용)
            "icrs_x_j2000_km":    pos_j2000[0],
            "icrs_y_j2000_km":    pos_j2000[1],
            "icrs_z_j2000_km":    pos_j2000[2],
            "icrs_vx_j2000_km_s": vel[0],
            "icrs_vy_j2000_km_s": vel[1],
            "icrs_vz_j2000_km_s": vel[2],
        }

        # ── principia 블록 ──
        rec_mass = next(
            (m.get("value_msun") for m in mass_meas if m.get("recommended")),
            None
        )
        rec_radius = next(
            (r.get("value_rsun") for r in radius_meas if r.get("recommended")),
            None
        )
        principia_block = {
            "gravitational_parameter_km3_s2": round(rec_mass * GM_SUN, 3) if rec_mass else None,
            "mean_radius_km":                 round(rec_radius * R_SUN_KM, 1) if rec_radius else None,
        }

        # ── 행성 블록 ──
        curated_list = planets_curated.get(star_name, []) or planets_curated.get(sys_name, [])
        curated_by_name = {c["pl_name"].strip(): c for c in curated_list}

        planets_block = []
        for pl in planet_list:
            pl_curated = curated_by_name.get(pl["pl_name"].strip())
            planet_entry = {
                "name":      pl["pl_name"],
                "host_star": star_name,
                "raw":       pl,
                "derived":   build_planet_derived(pl, curated=pl_curated),
            }
            if pl_curated:
                planet_entry["curated"] = pl_curated
            planets_block.append(planet_entry)

        # ── 소스 목록 ──
        astro_src = SRC_GAIA if astro.get("source") == "gaia_dr3" else SRC_SIMBAD
        sources = [SRC_BUTKEVICH, astro_src]
        if planets_block:
            sources.append(SRC_ARCHIVE)
        existing_dois    = {s.get("doi")     for s in sources if s.get("doi")}
        existing_bibcodes = {s.get("bibcode") for s in sources if s.get("bibcode")}

        # 질량·반지름 측정값의 DOI/bibcode 자동 추가
        for kind, meas_list in (("mass", mass_meas), ("radius", radius_meas)):
            for m in meas_list:
                doi = m.get("doi")
                bc  = m.get("bibcode")
                if doi in existing_dois or (not doi and bc in existing_bibcodes):
                    continue
                if not doi and not bc:
                    continue
                sources.append({
                    "title":    m.get("reference") or doi or bc,
                    "doi":      doi,
                    "bibcode":  bc,
                    "accessed": RETRIEVAL_DATE,
                    "used_for": [f"{star_name} {kind} ({m.get('method', 'unspecified')})"],
                })
                if doi:
                    existing_dois.add(doi)
                if bc:
                    existing_bibcodes.add(bc)

        # curated 행성 출처 추가
        for planet_entry in planets_block:
            c = planet_entry.get("curated") or {}
            for section in ("orbital", "physical", "environment", "atmosphere"):
                sec = c.get(section) or {}
                doi = sec.get("doi")
                if doi and doi not in existing_dois:
                    sources.append({
                        "title":    sec.get("source") or doi,
                        "doi":      doi,
                        "bibcode":  None,
                        "accessed": RETRIEVAL_DATE,
                        "used_for": [f"planet {planet_entry['name']} {section}"],
                    })
                    existing_dois.add(doi)

        # ── 컴포넌트 추출 ──
        cm = COMPONENT_RE.match(star_name)
        component = cm.group(1) if cm else None

        doc = {
            "system_name": star_name,
            "stars": [{
                "name":      star_name,
                "component": component,
                "raw":       raw_block,
                "derived":   derived_block,
                "principia": principia_block,
            }],
            "planets": planets_block,
            "sources": sources,
            "meta": {
                "retrieval_date":           RETRIEVAL_DATE,
                "solar_system_epoch_jd":    JD_B1950,
                "solar_system_epoch_label": "B1950.0",
                "game_epoch_jd_sol":        2433647.5,
                "game_epoch_jd_rss":        JD_B1950,
                "coordinate_origin":        "SSB",
                "coordinate_frame":         "ICRF",
                "coordinate_units":         "km, km/s",
                "notes":                    PROPAGATION_NOTES.get(star_name, ""),
            },
        }

        # 다성계 정보 임베드 / 참조
        if binary_data:
            if star_name == primary_comp:
                doc["binary_orbit"] = binary_data
            else:
                doc["binary_orbit_ref"] = primary_fname

        out_path = f"{DB}/systems/{fname}"
        with open(out_path, "w") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
        written += 1

# ── 결과 요약 ──────────────────────────────────────────────────────────────────
print(f"\n완료: {written}개 파일 작성")
if errors:
    print(f"오류 ({len(errors)}개):")
    for e in errors:
        print(f"  {e}")
else:
    print("오류 없음.")
