# raw 파일들을 조합해 db/systems/*.json 재생성. B1950+J2000 전파, vmag_v 포함.
import json, math, re, os
from PyAstronomy.pyasl import MarkleyKESolver
from _naming import to_filename

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB   = os.path.join(BASE, "db")

# ── 상수 ──────────────────────────────────────────────────────────────────────
PC_TO_KM      = 3.085677581491e13
AU_TO_KM      = 1.495978707e8
AU_TO_M       = 1.495978707e11
GM_SUN        = 1.32712440018e11   # km³/s²
R_SUN_KM      = 695700.0
M_EARTH_KG    = 5.9722e24
R_EARTH_M     = 6.371e6
DEG_TO_RAD    = math.pi / 180.0
YR_TO_S       = 365.25 * 86400.0
AU_PER_YR_TO_KM_PER_S = AU_TO_KM / YR_TO_S      # ≈ 4.7404705 km/s per AU/yr
ULP           = 2.0 ** -52

JD_GAIA       = 2457389.0   # J2016.0
JD_J2000      = 2451545.0   # J2000.0
JD_B1950      = 2433282.5   # B1950.0 (Sol/RSS 에포크)
RETRIEVAL_DATE = __import__("datetime").date.today().isoformat()

# 매 실행마다 today() 가 retrieval_date/accessed 에 박혀 151개 systems 파일이
# 통째로 churn 나는 것을 막는다. 내용(날짜 제외)이 같으면 기존 파일을 그대로 두어
# 날짜가 "마지막으로 데이터가 실제 바뀐 날" 을 가리키게 한다.
_VOLATILE_DATE_KEYS = {"retrieval_date", "accessed"}


def _strip_dates(obj):
    if isinstance(obj, dict):
        return {k: ("" if k in _VOLATILE_DATE_KEYS else _strip_dates(v))
                for k, v in obj.items()}
    if isinstance(obj, list):
        return [_strip_dates(x) for x in obj]
    return obj


def write_system_doc(out_path, doc):
    """Write doc unless ONLY volatile date fields would change.
    Returns 'wrote' or 'skipped'."""
    if os.path.exists(out_path):
        try:
            with open(out_path, encoding="utf-8") as f:
                old = json.load(f)
            if _strip_dates(old) == _strip_dates(doc):
                return "skipped"
        except (json.JSONDecodeError, OSError):
            pass
    with open(out_path, "w") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    return "wrote"


_KEPLER_SOLVER = MarkleyKESolver()

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


# 컴포넌트 글자 추출용 패턴 (예: "Alpha Centauri A" → "A")
COMPONENT_RE = re.compile(r"^.+\s+([A-Z])$")

# 알려진 선형 전파 한계 노트 (Barnard's Star perspective acceleration 등)
# meta.notes 의 소스는 stellar_props_curated[<star>].meta_notes (top-level 자유
# 서술 필드). build 가 이를 그대로 흘려 보내고, phase_reliable=false 인 다성계
# 라면 자동 warning 을 append. 과거 PROPAGATION_NOTES 하드코드 dict 는 제거.


def coalesce(*candidates):
    """첫 번째 non-None 값을 반환. 키 부재와 명시적 None 구분 안 함."""
    for v in candidates:
        if v is not None:
            return v
    return None


# ── 다성계 Kepler/Thiele-Innes 파이프라인 ─────────────────────────────────────

def _icrs_basis(ra_deg, dec_deg):
    """무게중심 (α, δ)에서의 (r̂_los, N̂, Ê) 단위벡터 (ICRS Cartesian)."""
    ra  = ra_deg  * DEG_TO_RAD
    dec = dec_deg * DEG_TO_RAD
    cr, sr = math.cos(ra), math.sin(ra)
    cd, sd = math.cos(dec), math.sin(dec)
    r_hat = (cd*cr,  cd*sr,  sd)
    N_hat = (-sd*cr, -sd*sr, cd)
    E_hat = (-sr,    cr,     0.0)
    return r_hat, N_hat, E_hat


def _thiele_innes_per_unit_a(omega_deg, Omega_deg, i_deg):
    """ω,Ω,i (deg) → 차원 없는 A,B,F,G,C,H/a. 부호 규약은 pipeline doc §2 step 5."""
    co, so = math.cos(omega_deg*DEG_TO_RAD), math.sin(omega_deg*DEG_TO_RAD)
    cO, sO = math.cos(Omega_deg*DEG_TO_RAD), math.sin(Omega_deg*DEG_TO_RAD)
    ci, si = math.cos(i_deg*DEG_TO_RAD),     math.sin(i_deg*DEG_TO_RAD)
    A =  co*cO - so*sO*ci
    B =  co*sO + so*cO*ci
    F = -so*cO - co*sO*ci
    G = -so*sO + co*cO*ci
    C =  so*si
    H =  co*si
    return A, B, F, G, C, H


def solve_orbit_relative(orbit, dist_pc, t_jd):
    """주어진 orbit 요소로 t_jd 시점의 상대(B−A) 위치/속도를 ICRS Cartesian으로 반환.
    Returns ((rx, ry, rz) km, (vx, vy, vz) km/s).
    a 입력은 a_arcsec (각도) 또는 a_au (직접 AU) 중 하나. 외곽(hierarchical) 궤도는
    분리각이 너무 커서 a_au가 더 자연스러움.
    """
    P_yr     = orbit["P_yr"]
    T_jd     = orbit["T_jd_tt"]
    e        = orbit["e"]
    if "a_au" in orbit:
        a_au = orbit["a_au"]
    elif "a_arcsec" in orbit:
        a_au = orbit["a_arcsec"] * dist_pc    # parsec 정의: 1″×1pc = 1AU
    else:
        raise ValueError(f"orbit {orbit.get('orbit_id')}: a_arcsec 또는 a_au 필요")
    i_deg    = orbit["i_deg"]
    om_deg   = orbit["omega_deg"]
    Om_deg   = orbit["Omega_deg"]

    # Mean anomaly
    n_rad_yr = 2.0 * math.pi / P_yr
    dt_yr    = (t_jd - T_jd) / 365.25
    M        = (n_rad_yr * dt_yr) % (2.0 * math.pi)

    # Kepler → eccentric anomaly
    E = _KEPLER_SOLVER.getE(M, e)

    # Perifocal state (AU, AU/yr)
    sqrt1me2 = math.sqrt(1.0 - e*e)
    nu = 2.0 * math.atan2(math.sqrt(1+e)*math.sin(E/2),
                          math.sqrt(1-e)*math.cos(E/2))
    r  = a_au * (1.0 - e*math.cos(E))
    x_p = r * math.cos(nu)
    y_p = r * math.sin(nu)
    n_a_factor = n_rad_yr * a_au / sqrt1me2     # AU/yr
    vx_p = -n_a_factor * math.sin(E)
    vy_p =  n_a_factor * sqrt1me2 * math.cos(E)

    # Thiele-Innes (per unit a, dimensionless) → sky-frame (N, E, W) AU.
    # Hilditch / Pourbaix convention: A·x_p + F·y_p → North; B·x_p + G·y_p → East;
    # C·x_p + H·y_p → away from observer (radial). Pipeline doc §2 step 5 prose
    # transposes A↔B (and H↔C) — the worked-example numerics in §10 confirm
    # Hilditch is the intended formula. See docs/work/binary-epoch-context-notes.md.
    tA, tB, tF, tG, tC, tH = _thiele_innes_per_unit_a(om_deg, Om_deg, i_deg)
    dN_au = tA*x_p + tF*y_p
    dE_au = tB*x_p + tG*y_p
    dW_au = tC*x_p + tH*y_p
    vN_auyr = tA*vx_p + tF*vy_p
    vE_auyr = tB*vx_p + tG*vy_p
    vW_auyr = tC*vx_p + tH*vy_p

    return ((dN_au, dE_au, dW_au), (vN_auyr, vE_auyr, vW_auyr))


def sky_offset_to_icrs(deltas_au, ra_deg, dec_deg):
    """(ΔN, ΔE, ΔW) AU at sky direction (α, δ) → ICRS Cartesian (km)."""
    dN, dE, dW = deltas_au
    r_hat, N_hat, E_hat = _icrs_basis(ra_deg, dec_deg)
    x_au = dN*N_hat[0] + dE*E_hat[0] + dW*r_hat[0]
    y_au = dN*N_hat[1] + dE*E_hat[1] + dW*r_hat[1]
    z_au = dN*N_hat[2] + dE*E_hat[2] + dW*r_hat[2]
    return (x_au*AU_TO_KM, y_au*AU_TO_KM, z_au*AU_TO_KM)


def _mass_weighted_average(records, masses):
    """ICRF Cartesian (km, km/s) mass-weighted average of component astrometries.
    Assumes all records share the same epoch_jd. Caller checks epoch consistency.
    """
    positions, velocities = [], []
    for rec in records:
        rv = rec.get("radial_velocity_km_s") or 0.0
        pos, vel = to_icrf(rec["ra_deg"], rec["dec_deg"], rec["parallax_mas"],
                           rec["pmra_mas_yr"], rec["pmdec_mas_yr"], rv)
        positions.append(pos)
        velocities.append(vel)
    total = float(sum(masses))
    pos_avg = tuple(sum(m*p[i] for m,p in zip(masses, positions))/total for i in range(3))
    vel_avg = tuple(sum(m*v[i] for m,v in zip(masses, velocities))/total for i in range(3))
    return pos_avg, vel_avg


def resolve_barycenter_state(system_name, binary_data, astrometry_raw):
    """astrometry_source 규칙으로 무게중심 (pos, vel, ra_at_epoch, dec_at_epoch, dist_pc, epoch_jd)
    를 source 에포크에서 계산. 반환 dist_pc는 source 에포크의 parallax 기반.
    """
    comps_by_name = {c["name"]: c for c in binary_data["components"]}
    orbit = binary_data["orbits"][0]   # 첫 궤도의 primary 규칙 사용 (단순화: 다중 궤도는 비계층 처리)
    primary_name = orbit.get("primary") or orbit["relates"][0]
    src = comps_by_name[primary_name]["astrometry_source"]

    if src.startswith("single_component:"):
        ref_name = src.split(":", 1)[1].strip()
        rec = astrometry_raw[ref_name]
        rv = rec.get("radial_velocity_km_s") or 0.0
        pos, vel = to_icrf(rec["ra_deg"], rec["dec_deg"], rec["parallax_mas"],
                           rec["pmra_mas_yr"], rec["pmdec_mas_yr"], rv)
        return {
            "pos_km":      pos,
            "vel_km_s":    vel,
            "ra_deg":      rec["ra_deg"],
            "dec_deg":     rec["dec_deg"],
            "dist_pc":     1000.0 / rec["parallax_mas"],
            "epoch_jd":    rec.get("epoch_jd", JD_GAIA),
            "method":      f"single_component({ref_name})",
        }

    if src == "mass_weighted_average":
        related = list(orbit["relates"])
        recs    = [astrometry_raw[c] for c in related]
        masses  = [comps_by_name[c]["mass_msun"] for c in related]
        epochs  = {r.get("epoch_jd", JD_GAIA) for r in recs}
        if len(epochs) > 1:
            raise ValueError(f"{system_name}: mass_weighted_average requires "
                             f"matched epoch_jd across components; got {sorted(epochs)}")
        pos_avg, vel_avg = _mass_weighted_average(recs, masses)
        total = float(sum(masses))
        ra_avg  = sum(m*r["ra_deg"]       for m,r in zip(masses,recs)) / total
        dec_avg = sum(m*r["dec_deg"]      for m,r in zip(masses,recs)) / total
        plx_avg = sum(m*r["parallax_mas"] for m,r in zip(masses,recs)) / total
        return {
            "pos_km":      pos_avg,
            "vel_km_s":    vel_avg,
            "ra_deg":      ra_avg,
            "dec_deg":     dec_avg,
            "dist_pc":     1000.0 / plx_avg,
            "epoch_jd":    recs[0].get("epoch_jd", JD_GAIA),
            "method":      f"mass_weighted_average({','.join(related)})",
        }

    if src in ("gaia_dr3_nss_barycenter", "hipparcos_barycenter"):
        bary = binary_data.get("barycenter_astrometry")
        if bary is None:
            raise ValueError(f"{system_name}: astrometry_source={src} "
                             "requires top-level 'barycenter_astrometry' block")
        rv = bary.get("radial_velocity_km_s") or 0.0
        pos, vel = to_icrf(bary["ra_deg"], bary["dec_deg"], bary["parallax_mas"],
                           bary["pmra_mas_yr"], bary["pmdec_mas_yr"], rv)
        return {
            "pos_km":      pos,
            "vel_km_s":    vel,
            "ra_deg":      bary["ra_deg"],
            "dec_deg":     bary["dec_deg"],
            "dist_pc":     1000.0 / bary["parallax_mas"],
            "epoch_jd":    bary.get("epoch_jd", JD_GAIA),
            "method":      src,
        }

    raise ValueError(f"{system_name}: unsupported astrometry_source '{src}'")


def resolve_binary_component_states(system_name, binary_data, astrometry_raw):
    """주어진 binary entry의 모든 궤도-귀속 컴포넌트에 대해 B1950, J2000 ICRS Cartesian 상태 반환.
    Returns dict component_name → {b1950: {pos, vel}, j2000: {pos, vel}, meta: {...}}.
    Components not in any orbits[].relates 는 dict에 없음 (호출자가 단일 항성 경로로 처리).
    """
    out = {}
    bary = resolve_barycenter_state(system_name, binary_data, astrometry_raw)
    comps_by_name = {c["name"]: c for c in binary_data["components"]}

    # 각 궤도별 처리. 평탄 궤도(primary/secondary 둘 다 실제 컴포넌트)는 기존 로직.
    # 계층 궤도(primary_is_barycenter_of: 내부 쌍을 한 점으로 묶고 외곽 동반자와 짝지움)는
    # 별도 분기. phase_reliable=false 외곽 궤도는 단일 항성 폴백에 맡겨 회귀를 방지.
    for orbit in binary_data["orbits"]:
        if "primary_is_barycenter_of" in orbit:
            if not orbit.get("phase_reliable", True):
                # 외곽 궤도의 위상(T_periastron)이 불확실 → 요소만으로 위치 예측 불가.
                # out에 secondary를 추가하지 않으면 caller(main loop)가 binary_states에
                # 없는 컴포넌트를 단일 항성 경로(astrometry_raw 직접 + 선형 전파)로 처리함.
                # 결과: 외곽 동반자의 수치 출력은 기존 standalone 처리와 동일.
                continue
            # phase_reliable=true: Jacobi 합성.
            # 현재 데이터에서는 사용되지 않으나, 향후 신뢰성 있는 외곽 궤도(예: Gaia DR4 NSS
            # hierarchical)가 들어오면 자동으로 활성화됨.
            outer_secondary = orbit["secondary"]
            inner_members   = orbit["primary_is_barycenter_of"]
            m_inner_total = sum(comps_by_name[n]["mass_msun"] for n in inner_members)
            m_outer       = comps_by_name[outer_secondary]["mass_msun"]
            if m_outer is None or any(comps_by_name[n]["mass_msun"] is None for n in inner_members):
                raise ValueError(
                    f"{system_name} orbit {orbit['orbit_id']}: "
                    f"primary_is_barycenter_of requires mass_msun on inner members and secondary"
                )
            for epoch_label, t_jd in (("b1950", JD_B1950), ("j2000", JD_J2000)):
                dt_s = (t_jd - bary["epoch_jd"]) * 86400.0
                R_g = propagate(bary["pos_km"], bary["vel_km_s"], dt_s)
                V_g = bary["vel_km_s"]
                # 외곽 상대 오프셋 r_outer(t) = (outer_secondary − g) at t_jd
                (deltas_au, vels_auyr) = solve_orbit_relative(orbit, bary["dist_pc"], t_jd)
                r_outer_km   = sky_offset_to_icrs(deltas_au, bary["ra_deg"], bary["dec_deg"])
                v_outer_km_yr = sky_offset_to_icrs(vels_auyr, bary["ra_deg"], bary["dec_deg"])
                v_outer_km_s  = tuple(v / YR_TO_S for v in v_outer_km_yr)
                r_C = tuple(R_g[i] + r_outer_km[i]  for i in range(3))
                v_C = tuple(V_g[i] + v_outer_km_s[i] for i in range(3))
                out.setdefault(outer_secondary, {})[epoch_label] = {
                    "pos_km": r_C, "vel_km_s": v_C
                }
            out[outer_secondary].setdefault("meta", {}).update({
                "orbit_id":          orbit["orbit_id"],
                "role":              "outer_companion",
                "mass_ratio_q":      m_inner_total / (m_inner_total + m_outer),
                "barycenter_method": bary["method"],
                "phase_reliable":    orbit.get("phase_reliable", True),
            })
            continue

        primary, secondary = orbit["primary"], orbit["secondary"]
        m_p = comps_by_name[primary  ]["mass_msun"]
        m_s = comps_by_name[secondary]["mass_msun"]
        if m_p is None or m_s is None:
            raise ValueError(f"{system_name} orbit {orbit['orbit_id']}: "
                             f"mass_msun required for both components")
        m_total = m_p + m_s
        q_p = m_s / m_total   # primary는 무게중심 반대쪽: r_P = R_bary - q_p · r_rel
        q_s = m_p / m_total

        for epoch_label, t_jd in (("b1950", JD_B1950), ("j2000", JD_J2000)):
            # 무게중심: source 에포크 Cartesian → 선형 전파
            dt_s = (t_jd - bary["epoch_jd"]) * 86400.0
            R_bary = propagate(bary["pos_km"], bary["vel_km_s"], dt_s)
            V_bary = bary["vel_km_s"]    # 선형 → 속도 시간불변

            # 무게중심 (ra, dec)는 source 에포크 값 사용 (작은 시스템 영향 — context-notes 참조)
            ra_bary, dec_bary = bary["ra_deg"], bary["dec_deg"]

            # 상대 (B − A) 궤도 오프셋
            (deltas_au, vels_auyr) = solve_orbit_relative(orbit, bary["dist_pc"], t_jd)
            r_rel_km   = sky_offset_to_icrs(deltas_au, ra_bary, dec_bary)
            # 속도: sky basis는 동일 → AU/yr 입력으로 sky_offset_to_icrs 호출하면 km/yr 출력. /YR_TO_S.
            v_rel_km_yr = sky_offset_to_icrs(vels_auyr, ra_bary, dec_bary)
            v_rel_km_s  = tuple(v / YR_TO_S for v in v_rel_km_yr)

            r_p = tuple(R_bary[i] - q_p*r_rel_km[i]   for i in range(3))
            v_p = tuple(V_bary[i] - q_p*v_rel_km_s[i] for i in range(3))
            r_s = tuple(R_bary[i] + q_s*r_rel_km[i]   for i in range(3))
            v_s = tuple(V_bary[i] + q_s*v_rel_km_s[i] for i in range(3))

            out.setdefault(primary,   {})[epoch_label]   = {"pos_km": r_p, "vel_km_s": v_p}
            out.setdefault(secondary, {})[epoch_label]   = {"pos_km": r_s, "vel_km_s": v_s}

        out[primary  ].setdefault("meta", {}).update({
            "orbit_id": orbit["orbit_id"],
            "role": "primary",
            "mass_ratio_q": q_p,
            "barycenter_method": bary["method"],
            "phase_reliable": orbit.get("phase_reliable", True),
        })
        out[secondary].setdefault("meta", {}).update({
            "orbit_id": orbit["orbit_id"],
            "role": "secondary",
            "mass_ratio_q": q_s,
            "barycenter_method": bary["method"],
            "phase_reliable": orbit.get("phase_reliable", True),
        })

    return out


def _pick_recommended(block):
    """Phase 2 array 형식에서 recommended:true 항목 선택.
    dict이면 그대로, list이면 recommended:true 첫 항목.
    list인데 recommended가 없으면 [0]번 fallback."""
    if block is None:
        return {}
    if isinstance(block, dict):
        return block
    if isinstance(block, list):
        for m in block:
            if isinstance(m, dict) and m.get("recommended") is True:
                return m
        return block[0] if block and isinstance(block[0], dict) else {}
    return {}


def build_planet_derived(pl, curated=None):
    """행성 raw + curated → 단위 변환된 derived 블록.
    우선순위: curated > tepcat > nasa_archive (raw).
    curated.orbital/physical/environment 은 dict (Phase 1) 또는 list (Phase 2) 둘 다 허용.
    측정 없는 값은 null 유지 (기본값 가정은 Kopernicus 작성 단계의 책임)."""
    c_orb = _pick_recommended((curated or {}).get("orbital"))
    c_phy = _pick_recommended((curated or {}).get("physical"))
    c_env = _pick_recommended((curated or {}).get("environment"))
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
        # Phase 2 expansion (2026-05-21): environment 블록에서 Teq/density 추출
        "equilibrium_temperature_k":       c_env.get("equilibrium_temperature_k"),
        "density_g_cc":                    c_env.get("density_g_cc"),
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

# disk_measurements 는 stellar 와 의미 분리되어 별도 source 파일에 보관.
# 스키마: {star_name: {"disk_measurements": [...]}}. star_name 은
# stellar_props_curated 의 키와 동일 규칙. 누락 시 빈 배열로 처리.
_disks_path = f"{DB}/disks_curated.json"
disks_curated = load_json(_disks_path) if os.path.exists(_disks_path) else {}

os.makedirs(f"{DB}/systems", exist_ok=True)

errors   = []
written  = 0
skipped  = 0

# ── 항성별 시스템 JSON 생성 ───────────────────────────────────────────────────
with open(f"{BASE}/db/target_list.json") as f:
    target_list = json.load(f)

for target in target_list:
    sys_name  = target["system"]
    comps     = target["components"]
    is_binary = target["binary"]
    stellarium_ids_map = target.get("stellarium_ids") or {}

    # 다성계: 대표 컴포넌트(첫 번째)에 binary_orbit 전체 임베드,
    # 다른 컴포넌트는 ref만 저장
    binary_data = binary_orbits.get(sys_name) if is_binary else None
    if is_binary and binary_data is None:
        errors.append(f"{sys_name}: binary=true이나 binary_orbits.json에 항목 없음")
        print(f"  [WARN] {sys_name}: binary_orbits.json 항목 없음")
    primary_comp  = comps[0] if is_binary else None
    primary_fname = to_filename(primary_comp) if primary_comp else None

    # 다성계: orbits[]에 fitted 궤도가 있는 컴포넌트는 Kepler+T-I로 ICRS 상태 산출.
    # 궤도 없는 컴포넌트(예: 40 Eri A, 36 Oph C)는 dict에 없음 → 단일 항성 경로로 폴백.
    binary_states = {}
    if binary_data and binary_data.get("orbits"):
        try:
            binary_states = resolve_binary_component_states(sys_name, binary_data, astrometry)
        except (ValueError, NotImplementedError, KeyError) as e:
            errors.append(f"{sys_name}: binary resolve 실패 — {e}")
            print(f"  [WARN] {sys_name}: binary 무시, 선형 전파 폴백 — {e}")

    # 단일 항성 시스템: 항성 1개씩 개별 파일
    # 다성계도 현재 구조 유지 (컴포넌트별 개별 파일)
    for star_name in comps:
        fname = to_filename(star_name)
        astro = astrometry.get(star_name)
        phot  = photometry.get(star_name, {})
        props   = stellar_props.get(star_name, {})
        curated = stellar_curated.get(star_name, {})
        # curated 에 키가 *존재* 하면 빈 리스트라도 그 의도를 존중 (raw 무시).
        # 키가 없으면 raw 로 fallback (mass/radius 만 raw 데이터 보유; 나머지 6
        # 카테고리는 raw 가 없어서 동일 결과).
        def _curated_or_raw(key):
            if key in curated:
                return curated[key]
            return props.get(key, [])
        mass_meas        = _curated_or_raw("mass_measurements")
        radius_meas      = _curated_or_raw("radius_measurements")
        # Phase 2 expansion (2026-05-21): 6 추가 카테고리 (raw 무관)
        teff_meas        = curated.get("teff_measurements", [])
        luminosity_meas  = curated.get("luminosity_measurements", [])
        age_meas         = curated.get("age_measurements", [])
        metallicity_meas = curated.get("metallicity_measurements", [])
        rotation_meas    = curated.get("rotation_measurements", [])
        activity_meas    = curated.get("activity_measurements", [])
        # 항성풍/자기장 (2026-06-10): sparse stellar 카테고리 — disk 처럼 데이터
        # 있는 별만 emit (conditional). [[project-nearstars-stellar-wind-kerbalism]].
        mass_loss_meas   = curated.get("mass_loss_measurements", [])
        bfield_meas      = curated.get("magnetic_field_measurements", [])
        cycle_meas       = curated.get("activity_cycle_measurements", [])
        xray_meas        = curated.get("xray_measurements", [])
        # disk_measurements 는 별도 source 파일 (db/disks_curated.json) 에서 로드.
        # 'present in disks_curated' 자체가 vetted 상태를 의미하므로 빈 리스트도
        # 가능. host_in_disks_curated 플래그로 emit 결정.
        _disk_rec = disks_curated.get(star_name) or {}
        host_in_disks_curated = star_name in disks_curated
        disk_meas        = _disk_rec.get("disk_measurements", [])

        # build-control 필드는 sources[] 생성에만 쓰이고 system 파일 output 에는
        # 노출하지 않음 (그 raw 인용은 curated.json 에 남음). 측정 dict 사본을
        # 만들어서 strip — 원본 curated 객체는 건드리지 않음.
        _BUILD_CONTROL_FIELDS = {"source_title", "source_used_for", "emit_source"}
        def _strip_build_control(arr):
            return [{k: v for k, v in m.items() if k not in _BUILD_CONTROL_FIELDS}
                    for m in (arr or [])]
        mass_meas_out        = _strip_build_control(mass_meas)
        radius_meas_out      = _strip_build_control(radius_meas)
        teff_meas_out        = _strip_build_control(teff_meas)
        luminosity_meas_out  = _strip_build_control(luminosity_meas)
        age_meas_out         = _strip_build_control(age_meas)
        metallicity_meas_out = _strip_build_control(metallicity_meas)
        rotation_meas_out    = _strip_build_control(rotation_meas)
        activity_meas_out    = _strip_build_control(activity_meas)
        mass_loss_meas_out   = _strip_build_control(mass_loss_meas)
        bfield_meas_out      = _strip_build_control(bfield_meas)
        cycle_meas_out       = _strip_build_control(cycle_meas)
        xray_meas_out        = _strip_build_control(xray_meas)
        disk_meas_out        = _strip_build_control(disk_meas)

        # Recommended resolved single values (array → recommended:true → value_*)
        rec_teff_arr = _pick_recommended(teff_meas)
        rec_lum_arr  = _pick_recommended(luminosity_meas)
        rec_age_arr  = _pick_recommended(age_meas)
        rec_met_arr  = _pick_recommended(metallicity_meas)
        rec_rot_arr  = _pick_recommended(rotation_meas)
        rec_act_arr  = _pick_recommended(activity_meas)
        rec_mdot_arr   = _pick_recommended(mass_loss_meas)
        rec_bfield_arr = _pick_recommended(bfield_meas)
        rec_cycle_arr  = _pick_recommended(cycle_meas)
        rec_xray_arr   = _pick_recommended(xray_meas)

        # teff_k: 우선순위 — Phase 2 array → curated 단일값 → raw stellar_props
        teff_k      = rec_teff_arr.get("value_k") or curated.get("teff_k") or props.get("teff_k")
        spectype    = curated.get("spectype") or props.get("spectype")
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
            "mass_measurements":       mass_meas_out,
            "radius_measurements":     radius_meas_out,
            "teff_measurements":       teff_meas_out,
            "luminosity_measurements": luminosity_meas_out,
            "age_measurements":        age_meas_out,
            "metallicity_measurements": metallicity_meas_out,
            "rotation_measurements":   rotation_meas_out,
            "activity_measurements":   activity_meas_out,
            "stellarium_id":           stellarium_ids_map.get(star_name),
        }
        # 항성풍/자기장: sparse → 데이터 있는 별만 raw 에 노출 (disk 패턴). 미제약
        # 별은 키 부재 → system 파일 churn 없음.
        if mass_loss_meas:
            raw_block["mass_loss_measurements"] = mass_loss_meas_out
        if bfield_meas:
            raw_block["magnetic_field_measurements"] = bfield_meas_out
        if cycle_meas:
            raw_block["activity_cycle_measurements"] = cycle_meas_out
        if xray_meas:
            raw_block["xray_measurements"] = xray_meas_out
        # disk_measurements 는 disks_curated 에 host entry 가 있는 별에만 emit
        # (빈 리스트도 'vetted no disk' 의미로 보존). 키 부재 = unvetted.
        # 위치는 stellarium_id 직전 — pop/reinsert 로 순서 유지.
        if host_in_disks_curated:
            si = raw_block.pop("stellarium_id", None)
            raw_block["disk_measurements"] = disk_meas_out
            raw_block["stellarium_id"] = si

        # Phase 2 expansion: curated array → recommended → 단일값 (derived 에 병합)
        stellar_props_resolved = {
            "luminosity_lsun":              rec_lum_arr.get("value_lsun"),
            "age_gyr":                      rec_age_arr.get("value_gyr"),
            "metallicity_fe_h_dex":         rec_met_arr.get("value_dex"),
            "rotation_period_days":         rec_rot_arr.get("value_days"),
            "activity_log_rhk":             rec_act_arr.get("value_log_rhk"),
            "activity_h_alpha_ew_angstrom": rec_act_arr.get("value_h_alpha_ew_angstrom"),
        }
        # 항성풍/자기장: 값 있을 때만 derived 에 추가 (대부분 별 미제약 → null churn 방지).
        _mdot = rec_mdot_arr.get("value_mdot_solar")
        if _mdot is not None:
            stellar_props_resolved["mass_loss_solar"] = _mdot
        _b_surf = rec_bfield_arr.get("value_b_surface_g")
        if _b_surf is not None:
            stellar_props_resolved["b_surface_g"] = _b_surf
        _b_large = rec_bfield_arr.get("value_b_largescale_g")
        if _b_large is not None:
            stellar_props_resolved["b_largescale_g"] = _b_large
        _cycle = rec_cycle_arr.get("value_cycle_period_yr")
        if _cycle is not None:
            stellar_props_resolved["activity_cycle_yr"] = _cycle
        _log_lx = rec_xray_arr.get("value_log_lx_ergs")
        if _log_lx is not None:
            stellar_props_resolved["xray_log_lx_ergs"] = _log_lx
        _log_rx = rec_xray_arr.get("value_log_rx")
        if _log_rx is not None:
            stellar_props_resolved["xray_log_rx"] = _log_rx

        # ── derived 블록 (B1950, J2000 모두 포함) ──
        # 다성계 컴포넌트가 fitted orbit에 포함되면 Kepler+T-I로 산출된 상태를 사용.
        bs = binary_states.get(star_name)
        if bs:
            b1950 = bs["b1950"]
            j2000 = bs["j2000"]
            bs_meta = bs.get("meta", {})
            derived_block = {
                "epoch_jd":           JD_B1950,
                "epoch_label":        "B1950.0",
                "propagation_method": "kepler_thiele_innes",
                "distance_pc":        dist_pc,
                "distance_km":        dist_pc * PC_TO_KM,
                "icrs_x_km":          b1950["pos_km"][0],
                "icrs_y_km":          b1950["pos_km"][1],
                "icrs_z_km":          b1950["pos_km"][2],
                "icrs_vx_km_s":       b1950["vel_km_s"][0],
                "icrs_vy_km_s":       b1950["vel_km_s"][1],
                "icrs_vz_km_s":       b1950["vel_km_s"][2],
                "position_ulp_km":    ulp_km(b1950["pos_km"]),
                "icrs_x_j2000_km":    j2000["pos_km"][0],
                "icrs_y_j2000_km":    j2000["pos_km"][1],
                "icrs_z_j2000_km":    j2000["pos_km"][2],
                "icrs_vx_j2000_km_s": j2000["vel_km_s"][0],
                "icrs_vy_j2000_km_s": j2000["vel_km_s"][1],
                "icrs_vz_j2000_km_s": j2000["vel_km_s"][2],
                "orbit_id":           bs_meta.get("orbit_id"),
                "orbit_role":         bs_meta.get("role"),
                "mass_ratio_q":       bs_meta.get("mass_ratio_q"),
                "barycenter_method":  bs_meta.get("barycenter_method"),
                "phase_reliable":     bs_meta.get("phase_reliable"),
                **stellar_props_resolved,
            }
        else:
            derived_block = {
                "epoch_jd":           JD_B1950,
                "epoch_label":        "B1950.0",
                "propagation_method": "linear",
                "distance_pc":        dist_pc,
                "distance_km":        dist_pc * PC_TO_KM,
                "icrs_x_km":          pos_b1950[0],
                "icrs_y_km":          pos_b1950[1],
                "icrs_z_km":          pos_b1950[2],
                "icrs_vx_km_s":       vel[0],
                "icrs_vy_km_s":       vel[1],
                "icrs_vz_km_s":       vel[2],
                "position_ulp_km":    ulp_km(pos_b1950),
                "icrs_x_j2000_km":    pos_j2000[0],
                "icrs_y_j2000_km":    pos_j2000[1],
                "icrs_z_j2000_km":    pos_j2000[2],
                "icrs_vx_j2000_km_s": vel[0],
                "icrs_vy_j2000_km_s": vel[1],
                "icrs_vz_j2000_km_s": vel[2],
                **stellar_props_resolved,
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
        seen_planet_names = set()
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
            seen_planet_names.add(pl["pl_name"].strip())

        # curated-only 행성 (NASA Archive raw 에 없는) 도 emit — J1407b·40 Eri A b·
        # tau Cet e 처럼 Archive 미등재 (잠정/비표준/철회) 천체. raw 는 fetch 된 게
        # 없으므로, 뷰어 행성 표(raw 값을 읽음)가 빈 칸으로 보이지 않도록 curated
        # 의 recommended 값으로 raw 를 합성한다 (provenance 는 reference 에 보존).
        for cname, c in curated_by_name.items():
            if cname in seen_planet_names:
                continue
            c_orb = _pick_recommended(c.get("orbital"))
            c_phy = _pick_recommended(c.get("physical"))
            synth_raw = {
                "pl_name":            c["pl_name"],
                "discoverymethod":    c_orb.get("method") or c_phy.get("method"),
                "period_days":        c_orb.get("period_days"),
                "semi_major_axis_au": c_orb.get("semi_major_axis_au"),
                "eccentricity":       c_orb.get("eccentricity"),
                "inclination_deg":    c_orb.get("inclination_deg"),
                "mass_mearth":        c_phy.get("true_mass_mearth") or c_phy.get("mass_mearth"),
                "radius_rearth":      c_phy.get("radius_rearth"),
                "reference":          (c_orb.get("reference") or c_phy.get("reference")
                                       or c_orb.get("source") or c_phy.get("source")),
            }
            planets_block.append({
                "name":      c["pl_name"],
                "host_star": star_name,
                "raw":       synth_raw,
                "derived":   build_planet_derived({}, curated=c),
                "curated":   c,
            })

        # ── 소스 목록 ──
        astro_src = SRC_GAIA if astro.get("source") == "gaia_dr3" else SRC_SIMBAD
        sources = [SRC_BUTKEVICH, astro_src]
        # 행성 entry에 per-paper bibcode가 하나라도 있으면 SRC_ARCHIVE 생략
        # (generic NASA Archive 출처는 paper-sourced attribution 있을 때 중복 잡음)
        # Phase 2 array form (list-of-dict) 도 검사.
        def _section_has_paper(sec):
            if isinstance(sec, dict):
                return bool(sec.get("bibcode") or sec.get("doi"))
            if isinstance(sec, list):
                return any(
                    isinstance(e, dict) and (e.get("bibcode") or e.get("doi"))
                    for e in sec
                )
            return False

        has_paper_source = any(
            _section_has_paper((pe.get("curated") or {}).get("orbital"))
            or _section_has_paper((pe.get("curated") or {}).get("physical"))
            for pe in planets_block
        )
        if planets_block and not has_paper_source:
            sources.append(SRC_ARCHIVE)
        existing_dois    = {s.get("doi")     for s in sources if s.get("doi")}
        existing_bibcodes = {s.get("bibcode") for s in sources if s.get("bibcode")}

        # 질량·반지름·disk 측정값의 DOI/bibcode 자동 추가.
        # disk 는 한 별이 여러 belt × paper entries 를 가질 수 있어서
        # belt label 을 used_for 에 포함시킨다 (e.g. "eps Eri disk main_cold").
        for kind, meas_list in (("mass", mass_meas), ("radius", radius_meas),
                                 ("disk", disk_meas)):
            for m in meas_list:
                # emit_source=false 면 sources[] 자동 생성 건너뜀
                # (cross-reference 목적의 superseded entry 등).
                if m.get("emit_source") is False:
                    continue
                doi = m.get("doi")
                bc  = m.get("bibcode")
                if doi in existing_dois or (not doi and bc in existing_bibcodes):
                    continue
                if not doi and not bc:
                    continue
                # source_title / source_used_for: per-measurement override 필드.
                # 큐레이션 시 풍부한 title (논문 부제 포함) 이나 다중 used_for 라벨
                # 을 묶고 싶을 때 사용. 키가 *존재* 하면 그 값을 우선 (빈 문자열·
                # 빈 리스트도 큐레이터 의도). 키 부재 시에만 reference + 기본 한 줄.
                if "source_title" in m:
                    src_title = m["source_title"]
                else:
                    src_title = m.get("reference") or doi or bc
                if "source_used_for" in m:
                    src_used = m["source_used_for"]
                else:
                    label = f"{star_name} {kind}"
                    if kind == "disk" and m.get("belt"):
                        label = f"{label} {m['belt']}"
                    src_used = [f"{label} ({m.get('method', 'unspecified')})"]
                sources.append({
                    "title":    src_title,
                    "doi":      doi,
                    "bibcode":  bc,
                    "accessed": RETRIEVAL_DATE,
                    "used_for": src_used,
                })
                if doi:
                    existing_dois.add(doi)
                if bc:
                    existing_bibcodes.add(bc)

        # 측정값에 묶이지 않는 supporting reference (curated.sources_extra) 병합.
        # title-only entry (doi=null, bibcode=null) 는 title 자체로 dedup 해서
        # 같은 빌드 내 중복 emit 방지.
        existing_title_only = {
            s.get("title") for s in sources
            if not s.get("doi") and not s.get("bibcode")
        }
        for extra in (curated.get("sources_extra") or []):
            if not isinstance(extra, dict):
                continue
            doi = extra.get("doi")
            bc  = extra.get("bibcode")
            title = extra.get("title") or extra.get("reference") or doi or bc
            if doi and doi in existing_dois:
                continue
            if bc and not doi and bc in existing_bibcodes:
                continue
            if not doi and not bc:
                # title-only — title 빈 값은 거부 (식별 불가).
                if not title:
                    continue
                if title in existing_title_only:
                    continue
            sources.append({
                "title":    title,
                "doi":      doi,
                "bibcode":  bc,
                "accessed": RETRIEVAL_DATE,
                "used_for": extra.get("used_for") or [],
            })
            if doi:
                existing_dois.add(doi)
            if bc:
                existing_bibcodes.add(bc)
            if not doi and not bc:
                existing_title_only.add(title)

        # curated 행성 출처 추가 (bibcode-or-doi dedup; bibcode propagation)
        # Phase 2 array form은 각 element를 별도 source로 추가.
        for planet_entry in planets_block:
            c = planet_entry.get("curated") or {}
            for section in ("orbital", "physical", "environment", "atmosphere"):
                sec = c.get(section)
                if sec is None:
                    continue
                # dict (Phase 1) → 단일 entry, list (Phase 2) → 모든 entry
                entries = sec if isinstance(sec, list) else [sec]
                for e in entries:
                    if not isinstance(e, dict):
                        continue
                    doi = e.get("doi")
                    bc  = e.get("bibcode")
                    if not doi and not bc:
                        continue
                    if doi and doi in existing_dois:
                        continue
                    if bc and not doi and bc in existing_bibcodes:
                        continue
                    sources.append({
                        "title":    e.get("source") or e.get("reference") or doi or bc,
                        "doi":      doi,
                        "bibcode":  bc,
                        "accessed": RETRIEVAL_DATE,
                        "used_for": [f"planet {planet_entry['name']} {section}"],
                    })
                    if doi:
                        existing_dois.add(doi)
                    if bc:
                        existing_bibcodes.add(bc)

        # ── 컴포넌트 추출 ──
        cm = COMPONENT_RE.match(star_name)
        component = cm.group(1) if cm else None

        notes = (curated.get("meta_notes") or "").strip()
        if bs and bs.get("meta", {}).get("phase_reliable") is False:
            warn = (f"Binary orbit {bs['meta'].get('orbit_id')} flagged "
                    f"phase_reliable=false — relative geometry of components "
                    f"may differ from real configuration at JD2433282.5. "
                    f"Principia N-body simulation will correct dynamically.")
            notes = (notes + " " + warn).strip()

        star_obj = {
            "name":      star_name,
            "component": component,
            "raw":       raw_block,
            "derived":   derived_block,
            "principia": principia_block,
        }
        # 컴팩트 천체 고유 물리 (compact_object) 는 일반 stellar 측정으로 표현 불가 —
        # curated 에 있으면 그대로 실어 보냄 (PSR J0108−1431).
        co = curated.get("compact_object")
        if co:
            star_obj["compact_object"] = co

        doc = {
            "system_name": star_name,
            "stars": [star_obj],
            "planets": planets_block,
            "sources": sources,
            "meta": {
                "retrieval_date":           RETRIEVAL_DATE,
                "solar_system_epoch_jd":    JD_B1950,
                "solar_system_epoch_label": "B1950.0",
                "game_epoch_jd_sol":        2433647.5,
                "game_epoch_jd_rss":        2433647.5,
                "coordinate_origin":        "SSB",
                "coordinate_frame":         "ICRF",
                "coordinate_units":         "km, km/s",
                "notes":                    notes,
            },
        }

        # 다성계 정보 임베드 / 참조
        if binary_data:
            if star_name == primary_comp:
                doc["binary_orbit"] = binary_data
            else:
                doc["binary_orbit_ref"] = primary_fname

        out_path = f"{DB}/systems/{fname}"
        if write_system_doc(out_path, doc) == "wrote":
            written += 1
        else:
            skipped += 1

# ── 결과 요약 ──────────────────────────────────────────────────────────────────
print(f"\n완료: {written}개 파일 작성, {skipped}개 변경 없음(날짜만) 건너뜀")
if errors:
    print(f"오류 ({len(errors)}개):")
    for e in errors:
        print(f"  {e}")
else:
    print("오류 없음.")
