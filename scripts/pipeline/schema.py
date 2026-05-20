# 파이프라인 raw 데이터의 필수 키를 검증하는 경량 스키마 모듈
"""Field-name validation for pipeline raw output files.

Each fetch script writes a dict-of-dicts JSON (`name → record`). The
schemas here declare the required and optional keys per record. Call
`validate(records, REQUIRED, OPTIONAL, name=...)` at the end of a fetch
script — it prints any missing required keys, unexpected keys, or naming
mismatches and exits non-zero on failure.

Goal: catch typos like `error_msun` vs `uncertainty_msun` at fetch time,
before they propagate to `db/systems/*.json`.
"""
import sys


ASTROMETRY_REQUIRED = {
    "source", "source_id", "epoch_jd", "epoch_label",
    "ra_deg", "dec_deg", "parallax_mas",
    "pmra_mas_yr", "pmdec_mas_yr", "radial_velocity_km_s",
}
ASTROMETRY_OPTIONAL = {
    "ra_error_mas", "dec_error_mas", "parallax_error_mas",
    "pmra_error_mas_yr", "pmdec_error_mas_yr", "rv_error_km_s",
    "radial_velocity_source", "sibling_backfill",
}

PHOTOMETRY_REQUIRED = {"vmag_v", "vmag_source"}
PHOTOMETRY_OPTIONAL = {"g_mag", "bp_rp"}

STELLAR_PROPS_REQUIRED = {
    "teff_k", "spectype", "mass_measurements", "radius_measurements",
}
STELLAR_PROPS_OPTIONAL = {"teff_bibcode"}

# measurement dict 내부 키 prefix 규약.
# value_msun/value_rsun처럼 단위 접미사가 있어야 하며, error_* prefix는 금지.
MEASUREMENT_VALUE_PREFIXES   = ("value_",)
MEASUREMENT_FORBIDDEN_PREFIX = ("error_",)  # uncertainty_*로 통일됨

PLANET_REQUIRED = {
    "pl_name", "period_days", "semi_major_axis_au", "mass_mearth",
}
PLANET_OPTIONAL = {
    "eccentricity", "mass_type", "reference", "retrieval_date",
    "period_err_days", "semi_major_axis_err_au", "inclination_deg",
    "inclination_err_deg", "omega_deg", "tperi_bjd", "tperi_err_bjd",
    "tranmid_bjd", "tranmid_err_bjd", "mass_err_mearth", "radius_rearth",
    "radius_err_rearth", "discoverymethod", "pl_controv_flag",
    "pubdate", "tepcat",
}


def validate(records, required, optional, name="records", measurement_keys=None):
    """records dict의 키 집합을 required/optional에 대해 검증.

    Args:
        records: name → record dict
        required: 필수 키 set
        optional: 허용되는 추가 키 set
        name: 에러 메시지에 출력할 식별자
        measurement_keys: ("mass_measurements", "radius_measurements") 같은
                          중첩 측정값 리스트 키. 각 항목을 별도 검증.
    Returns:
        에러 메시지 리스트. 빈 리스트면 통과.
    """
    errors = []
    allowed = required | optional
    for rec_name, rec in records.items():
        if not isinstance(rec, dict):
            errors.append(f"{name}[{rec_name}]: dict 아님 ({type(rec).__name__})")
            continue
        keys = set(rec.keys())
        missing = required - keys
        unknown = keys - allowed
        if missing:
            errors.append(f"{name}[{rec_name}]: 필수 키 누락 {sorted(missing)}")
        if unknown:
            errors.append(f"{name}[{rec_name}]: 알 수 없는 키 {sorted(unknown)}")

        for mk in (measurement_keys or []):
            for i, m in enumerate(rec.get(mk, []) or []):
                if not isinstance(m, dict):
                    errors.append(f"{name}[{rec_name}].{mk}[{i}]: dict 아님")
                    continue
                mkeys = set(m.keys())
                has_value = any(k.startswith(MEASUREMENT_VALUE_PREFIXES) for k in mkeys)
                if not has_value:
                    errors.append(f"{name}[{rec_name}].{mk}[{i}]: value_* 키 없음")
                forbidden = [k for k in mkeys if k.startswith(MEASUREMENT_FORBIDDEN_PREFIX)]
                if forbidden:
                    errors.append(
                        f"{name}[{rec_name}].{mk}[{i}]: 금지 prefix 사용 {forbidden} "
                        f"(uncertainty_*로 통일)"
                    )
                base_required = {"method", "reference", "recommended"}
                m_missing = base_required - mkeys
                if m_missing:
                    errors.append(f"{name}[{rec_name}].{mk}[{i}]: 필수 키 누락 {sorted(m_missing)}")
    return errors


# ── binary_orbits.json 스키마 ────────────────────────────────────────────────
# 신규 components[]+orbits[] 스키마 (2026-05-18). legacy raw 형식은 더 이상 허용 안 함.

BINARY_COMPONENT_REQUIRED = {
    "name", "mass_msun", "astrometry_source", "astrometry_quality",
}
BINARY_COMPONENT_OPTIONAL = {
    "mass_source", "astrometry_note",
}
BINARY_ASTROMETRY_SOURCES = {
    "gaia_dr3", "simbad",
    "mass_weighted_average",
    "gaia_dr3_nss_barycenter", "hipparcos_barycenter",
}
# single_component:<name> 패턴은 별도 검증

BINARY_ORBIT_REQUIRED = {
    "orbit_id", "relates", "secondary",
    "P_yr", "e",
    "i_deg", "omega_deg", "Omega_deg",
    "grade", "phase_reliable",
}
# 다음 키들은 궤도 종류에 따라 조건부 필수.
# 자세한 규칙은 validate_binary_orbits 의 per-orbit 조건 분기 참조.
BINARY_ORBIT_OPTIONAL = {
    # 조건부 필수: primary 또는 primary_is_barycenter_of 중 정확히 하나
    "primary", "primary_is_barycenter_of",
    # 조건부 필수: a_arcsec 또는 a_au 중 정확히 하나
    "a_arcsec", "a_au",
    # 조건부 필수: phase_reliable=true 면 T_jd_tt 필수, false 면 옵션 (위상 미사용)
    "T_jd_tt",
    # 그 외 옵션
    "source", "doi", "bibcode", "equinox", "node_resolved",
    "P_yr_err", "T_yr", "e_err", "a_arcsec_err",
    "i_err_deg", "omega_err_deg", "Omega_err_deg",
    "orbit_type", "note",
}

BINARY_SYSTEM_REQUIRED = {"system_id", "hierarchy", "components", "orbits"}
BINARY_SYSTEM_OPTIONAL = {"wds_id", "barycenter_astrometry"}


def validate_binary_orbits(binary_orbits):
    """db/binary_orbits.json 전체 검증.

    Returns:
        에러 메시지 리스트. 빈 리스트면 통과.
    """
    errors = []
    for sys_name, entry in binary_orbits.items():
        if sys_name.startswith("_"):
            continue   # _principia_notes 등 메타 키 스킵
        if not isinstance(entry, dict):
            errors.append(f"binary_orbits[{sys_name}]: dict 아님")
            continue

        keys = set(entry.keys())
        missing = BINARY_SYSTEM_REQUIRED - keys
        if missing:
            errors.append(f"binary_orbits[{sys_name}]: 필수 키 누락 {sorted(missing)}")
            continue
        unknown = keys - (BINARY_SYSTEM_REQUIRED | BINARY_SYSTEM_OPTIONAL)
        if unknown:
            errors.append(f"binary_orbits[{sys_name}]: 알 수 없는 키 {sorted(unknown)}")

        # components
        comp_names = []
        needs_bary_block = False
        for i, comp in enumerate(entry["components"]):
            if not isinstance(comp, dict):
                errors.append(f"binary_orbits[{sys_name}].components[{i}]: dict 아님")
                continue
            ck = set(comp.keys())
            cmiss = BINARY_COMPONENT_REQUIRED - ck
            if cmiss:
                errors.append(f"binary_orbits[{sys_name}].components[{i}]: 필수 키 누락 {sorted(cmiss)}")
            cunknown = ck - (BINARY_COMPONENT_REQUIRED | BINARY_COMPONENT_OPTIONAL)
            if cunknown:
                errors.append(f"binary_orbits[{sys_name}].components[{i}]: 알 수 없는 키 {sorted(cunknown)}")
            src = comp.get("astrometry_source")
            if src:
                if src.startswith("single_component:"):
                    pass   # 자유 형식 (단일 컴포넌트 이름 참조)
                elif src not in BINARY_ASTROMETRY_SOURCES:
                    errors.append(f"binary_orbits[{sys_name}].components[{i}]: "
                                  f"astrometry_source '{src}' 미지원 "
                                  f"(허용: {sorted(BINARY_ASTROMETRY_SOURCES)} 또는 'single_component:<name>')")
                if src in ("gaia_dr3_nss_barycenter", "hipparcos_barycenter"):
                    needs_bary_block = True
            comp_names.append(comp.get("name"))

        if needs_bary_block and "barycenter_astrometry" not in entry:
            errors.append(f"binary_orbits[{sys_name}]: astrometry_source가 "
                          f"NSS/Hipparcos barycenter인데 'barycenter_astrometry' 블록 없음")

        # orbits
        for j, orbit in enumerate(entry["orbits"]):
            if not isinstance(orbit, dict):
                errors.append(f"binary_orbits[{sys_name}].orbits[{j}]: dict 아님")
                continue
            ok = set(orbit.keys())
            omiss = BINARY_ORBIT_REQUIRED - ok
            if omiss:
                errors.append(f"binary_orbits[{sys_name}].orbits[{j}]: 필수 키 누락 {sorted(omiss)}")
            ounknown = ok - (BINARY_ORBIT_REQUIRED | BINARY_ORBIT_OPTIONAL)
            if ounknown:
                errors.append(f"binary_orbits[{sys_name}].orbits[{j}]: 알 수 없는 키 {sorted(ounknown)}")

            # 조건부 필수 1: primary 또는 primary_is_barycenter_of 중 정확히 하나
            has_primary  = "primary" in ok
            has_pri_bary = "primary_is_barycenter_of" in ok
            if has_primary == has_pri_bary:   # 둘 다 있거나 둘 다 없음
                errors.append(f"binary_orbits[{sys_name}].orbits[{j}]: "
                              f"'primary' 또는 'primary_is_barycenter_of' 중 정확히 하나 필요")

            # 조건부 필수 2: a_arcsec 또는 a_au 중 정확히 하나
            has_a_arcsec = "a_arcsec" in ok
            has_a_au     = "a_au" in ok
            if has_a_arcsec == has_a_au:
                errors.append(f"binary_orbits[{sys_name}].orbits[{j}]: "
                              f"'a_arcsec' 또는 'a_au' 중 정확히 하나 필요")

            # 조건부 필수 3: phase_reliable=true 면 T_jd_tt 필수 (위상 계산에 필요)
            #                phase_reliable=false 면 T_jd_tt 옵션 (위상 미사용 폴백)
            if orbit.get("phase_reliable", True) and "T_jd_tt" not in ok:
                errors.append(f"binary_orbits[{sys_name}].orbits[{j}]: "
                              f"phase_reliable=true 인 궤도는 'T_jd_tt' 필수")

            # relates 의 모든 항목이 components[] 에 있는지.
            # 단 primary_is_barycenter_of 가 있으면 barycenter pseudo-name (예: "X AB (barycenter)") 허용.
            allowed_rel_names = set(comp_names)
            if has_pri_bary:
                allowed_rel_names.add("(barycenter)")   # 마커: substring 매치
            for rname in orbit.get("relates", []) or []:
                if rname in comp_names:
                    continue
                if has_pri_bary and "(barycenter)" in rname:
                    continue   # 외곽 궤도의 barycenter pseudo-name
                errors.append(f"binary_orbits[{sys_name}].orbits[{j}]: "
                              f"relates '{rname}' 가 components[] 에 없음")

            # primary_is_barycenter_of 의 멤버들이 components[]에 있는지
            for bname in orbit.get("primary_is_barycenter_of", []) or []:
                if bname not in comp_names:
                    errors.append(f"binary_orbits[{sys_name}].orbits[{j}]: "
                                  f"primary_is_barycenter_of '{bname}' 가 components[] 에 없음")

    return errors


# ── stellar_props_curated.json 스키마 ────────────────────────────────────────
# raw 와 달리 curated 는 부분 오버라이드를 허용하므로 top-level 필수 키 없음.
# 각 measurement 의 method 라벨은 화이트리스트로 제한 (오타 방지).

STELLAR_CURATED_TOPLEVEL_ALLOWED = {
    "teff_k", "teff_bibcode", "spectype",
    "spectype_bibcode", "spectype_reference",
    "mass_measurements", "radius_measurements",
}
STELLAR_MEASUREMENT_BASE_REQUIRED = {"method", "recommended"}
STELLAR_MEASUREMENT_OPTIONAL = {
    "uncertainty_msun", "uncertainty_rsun",
    "reference", "bibcode", "doi",
    "value_msun", "value_rsun",  # value_* 는 별도 검증
}
# fetch_stellar_props.py 의 METHOD_PRIORITY 와 동기화 필요.
STELLAR_ALLOWED_METHODS = {
    "interferometry", "eclipsing_binary", "binary_orbit",
    "sed_fitting", "spectroscopic", "evolutionary_model",
    "spectroscopic_calibration", "asteroseismology",
    "unverified",
}


def validate_stellar_props_curated(records):
    """db/stellar_props_curated.json 검증."""
    errors = []
    for star, rec in records.items():
        if not isinstance(rec, dict):
            errors.append(f"stellar_props_curated[{star}]: dict 아님")
            continue
        unknown = set(rec.keys()) - STELLAR_CURATED_TOPLEVEL_ALLOWED
        if unknown:
            errors.append(f"stellar_props_curated[{star}]: 알 수 없는 키 {sorted(unknown)}")

        for mk in ("mass_measurements", "radius_measurements"):
            arr = rec.get(mk) or []
            if not isinstance(arr, list):
                errors.append(f"stellar_props_curated[{star}].{mk}: list 아님")
                continue
            n_recommended = 0
            for i, m in enumerate(arr):
                if not isinstance(m, dict):
                    errors.append(f"stellar_props_curated[{star}].{mk}[{i}]: dict 아님")
                    continue
                mkeys = set(m.keys())
                has_value = any(k.startswith(MEASUREMENT_VALUE_PREFIXES) for k in mkeys)
                if not has_value:
                    errors.append(f"stellar_props_curated[{star}].{mk}[{i}]: value_* 키 없음")
                forbidden = [k for k in mkeys if k.startswith(MEASUREMENT_FORBIDDEN_PREFIX)]
                if forbidden:
                    errors.append(
                        f"stellar_props_curated[{star}].{mk}[{i}]: 금지 prefix {forbidden} "
                        f"(uncertainty_* 사용)"
                    )
                miss = STELLAR_MEASUREMENT_BASE_REQUIRED - mkeys
                if miss:
                    errors.append(f"stellar_props_curated[{star}].{mk}[{i}]: 필수 키 누락 {sorted(miss)}")
                method = m.get("method")
                if method and method not in STELLAR_ALLOWED_METHODS:
                    errors.append(
                        f"stellar_props_curated[{star}].{mk}[{i}]: method '{method}' 미지원 "
                        f"(허용: {sorted(STELLAR_ALLOWED_METHODS)})"
                    )
                if m.get("recommended") is True:
                    n_recommended += 1
                unk = mkeys - (STELLAR_MEASUREMENT_BASE_REQUIRED | STELLAR_MEASUREMENT_OPTIONAL)
                if unk:
                    errors.append(f"stellar_props_curated[{star}].{mk}[{i}]: 알 수 없는 키 {sorted(unk)}")
            if n_recommended > 1:
                errors.append(
                    f"stellar_props_curated[{star}].{mk}: recommended:true 가 {n_recommended}개 "
                    f"(정확히 0 또는 1개)"
                )
    return errors


# ── planets_curated.json 스키마 ──────────────────────────────────────────────
# host_name → list of {pl_name, orbital{}, physical{}}. orbital/physical 은
# 단일 dict (Phase 1). Phase 2 의 array 형식은 빌드 코드 확장 후 별도 처리.

PLANET_CURATED_REQUIRED = {"pl_name"}
PLANET_CURATED_OPTIONAL = {"orbital", "physical"}
PLANET_ORBITAL_ALLOWED = {
    "semi_major_axis_au", "eccentricity", "inclination_deg",
    "argument_of_periapsis_deg", "longitude_of_ascending_node_deg",
    "mean_anomaly_at_epoch_deg", "epoch_jd",
    "source", "bibcode", "doi",
    # Phase 2 array element fields:
    "method", "recommended",
}
PLANET_PHYSICAL_ALLOWED = {
    "mass_mearth", "true_mass_mearth", "uncertainty_mearth", "mass_type",
    "radius_rearth", "uncertainty_rearth",
    "source", "bibcode", "doi",
    # Phase 2 array element fields:
    "method", "recommended",
}
PLANET_PROVENANCE_KEYS = {"source", "bibcode", "doi"}

# Phase 2 method 화이트리스트 (planet measurements).
# discovery method tier 순:
#   astrometric/direct > ttv/dynamical > rv > transit > predicted
PLANET_ALLOWED_METHODS = {
    "astrometric", "direct_imaging",
    "ttv", "dynamical",
    "rv",
    "transit", "transit_timing",
    "predicted", "theoretical",
    "discovery",          # 발견 paper의 종합값 (method 미세분류 곤란할 때)
    "unverified",         # Phase 1 batch auto-fill
}


def validate_planets_curated(records):
    """db/planets_curated.json 검증.

    각 행성의 orbital / physical 블록이 존재하면 최소 하나의 provenance
    필드(source/bibcode/doi)를 요구. curated 엔트리의 출처 추적성 강제.
    """
    errors = []
    for host, planets in records.items():
        if not isinstance(planets, list):
            errors.append(f"planets_curated[{host}]: list 아님 ({type(planets).__name__})")
            continue
        for i, pl in enumerate(planets):
            if not isinstance(pl, dict):
                errors.append(f"planets_curated[{host}][{i}]: dict 아님")
                continue
            pkeys = set(pl.keys())
            miss = PLANET_CURATED_REQUIRED - pkeys
            if miss:
                errors.append(f"planets_curated[{host}][{i}]: 필수 키 누락 {sorted(miss)}")
            unk = pkeys - (PLANET_CURATED_REQUIRED | PLANET_CURATED_OPTIONAL)
            if unk:
                errors.append(f"planets_curated[{host}][{i}]: 알 수 없는 키 {sorted(unk)}")

            for block_name, allowed in (
                ("orbital", PLANET_ORBITAL_ALLOWED),
                ("physical", PLANET_PHYSICAL_ALLOWED),
            ):
                block = pl.get(block_name)
                if block is None:
                    continue
                # Phase 1 dict 또는 Phase 2 list-of-dict 둘 다 허용.
                if isinstance(block, dict):
                    elems = [block]
                    is_array = False
                elif isinstance(block, list):
                    elems = block
                    is_array = True
                else:
                    errors.append(
                        f"planets_curated[{host}][{i}].{block_name}: dict 또는 list 아님"
                    )
                    continue

                n_recommended = 0
                for j, elem in enumerate(elems):
                    if not isinstance(elem, dict):
                        errors.append(
                            f"planets_curated[{host}][{i}].{block_name}"
                            f"{f'[{j}]' if is_array else ''}: dict 아님"
                        )
                        continue
                    bunk = set(elem.keys()) - allowed
                    if bunk:
                        errors.append(
                            f"planets_curated[{host}][{i}].{block_name}"
                            f"{f'[{j}]' if is_array else ''}: 알 수 없는 키 {sorted(bunk)}"
                        )
                    if not (PLANET_PROVENANCE_KEYS & set(elem.keys())):
                        errors.append(
                            f"planets_curated[{host}][{i}].{block_name}"
                            f"{f'[{j}]' if is_array else ''}: source/bibcode/doi 중 하나 필요"
                        )
                    if is_array:
                        method = elem.get("method")
                        if not method:
                            errors.append(
                                f"planets_curated[{host}][{i}].{block_name}[{j}]: "
                                f"array 형식은 'method' 필수"
                            )
                        elif method not in PLANET_ALLOWED_METHODS:
                            errors.append(
                                f"planets_curated[{host}][{i}].{block_name}[{j}]: "
                                f"method '{method}' 미지원 "
                                f"(허용: {sorted(PLANET_ALLOWED_METHODS)})"
                            )
                        if elem.get("recommended") is True:
                            n_recommended += 1
                if is_array and n_recommended > 1:
                    errors.append(
                        f"planets_curated[{host}][{i}].{block_name}: "
                        f"recommended:true 가 {n_recommended}개 (정확히 0 또는 1개)"
                    )
    return errors


def report_and_exit(errors, label):
    """에러가 있으면 stderr로 출력하고 비0 종료."""
    if not errors:
        print(f"  [OK] {label} 스키마 검증 통과")
        return
    print(f"\n  [FAIL] {label} 스키마 검증 실패 ({len(errors)}건):", file=sys.stderr)
    for e in errors[:20]:
        print(f"    {e}", file=sys.stderr)
    if len(errors) > 20:
        print(f"    ... 외 {len(errors)-20}건", file=sys.stderr)
    sys.exit(1)
