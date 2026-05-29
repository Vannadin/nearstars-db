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
# 각 measurement category 의 value_* 키와 method 라벨을 화이트리스트로 제한.
#
# Phase 2 expansion (2026-05-21): mass/radius 외에 teff/luminosity/age/
# metallicity/rotation/activity 6개 카테고리 추가. tier 우선순위는 코드 외부
# (phase2/schema-expansion/context-notes.md) 에 문서화됨 — 코드는 whitelist
# 만 강제하고 recommended:true 선택은 사용자가 manual 로 함.

# build-control 필드 — mass/radius 의 자동 sources[] 항목 생성을 제어한다.
# build_systems.py 의 sources[] 루프만 이 필드들을 읽고, raw block 으로 가기
# 직전에 strip 된다. mass/radius 외 측정 종류 (teff/lum/age/...) 에는 자동
# source 생성이 없으므로 적용되지 않는다.
_SOURCE_CONTROL_FIELDS = {"source_title", "source_used_for", "emit_source"}

STELLAR_MEASUREMENT_KINDS = {
    "mass_measurements": {
        # methodology.md tier: binary_orbit > asteroseismology > evolutionary_model
        #                      > spectroscopic / spectroscopic_calibration
        # empirical_relation = Torres et al. 2010 M-R-Teff / mass-luminosity relations.
        "value_keys": {"value_msun"},
        "methods": {
            "binary_orbit", "asteroseismology", "evolutionary_model",
            "spectroscopic", "spectroscopic_calibration",
            "empirical_relation",
            "unverified",
        },
        "extra_keys": set(_SOURCE_CONTROL_FIELDS),
    },
    "radius_measurements": {
        # methodology.md tier: interferometry > eclipsing_binary > sed_fitting > evolutionary_model
        # spectroscopic_calibration 은 methodology 에 미문서화이나 실 사용 중 (M dwarf
        # radius-color calibration: Wolf 359, Eta Cas B, Kapteyn). 추가.
        "value_keys": {"value_rsun"},
        "methods": {
            "interferometry", "eclipsing_binary", "sed_fitting",
            "evolutionary_model", "spectroscopic_calibration",
            "asteroseismology",
            "unverified",
        },
        # interferometric measurements often carry paper-level metadata
        # (instrument, angular_diameter_mas, arxiv id, narrative notes).
        # tau Cet / Korolik 2023 is the canonical example.
        "extra_keys": _SOURCE_CONTROL_FIELDS | {
            "instrument",
            "angular_diameter_mas", "angular_diameter_uncertainty_mas",
            "arxiv", "notes",
        },
    },
    "teff_measurements": {
        "value_keys": {"value_k"},
        "methods": {
            "high_res_spectroscopy", "low_res_spectroscopy",
            "sed_fitting", "photometric_color", "interferometry",
            "unverified",
        },
    },
    "luminosity_measurements": {
        "value_keys": {"value_lsun"},
        "methods": {
            "bolometric_flux", "sed_fitting", "photometric",
            "unverified",
        },
    },
    "age_measurements": {
        "value_keys": {"value_gyr"},
        "methods": {
            "asteroseismology", "isochrone", "gyrochronology",
            "activity_age", "kinematic",
            "unverified",
        },
    },
    "metallicity_measurements": {
        "value_keys": {"value_dex"},   # [Fe/H] in dex
        "methods": {
            "high_res_spectroscopy", "low_res_spectroscopy",
            "photometric_calibration",
            "unverified",
        },
    },
    "rotation_measurements": {
        "value_keys": {"value_days"},   # P_rot
        "methods": {
            "photometric_variability", "v_sin_i",
            "zeeman_doppler", "asteroseismology",
            "unverified",
        },
    },
    "activity_measurements": {
        # 여러 지표 중 하나만 있으면 됨 (paper 마다 다름)
        "value_keys": {
            "value_log_rhk",
            "value_h_alpha_ew_angstrom",
            "value_x_ray_log_lx_lbol",
            "value_ca_ii_log_lhk",
        },
        "methods": {
            "log_rhk", "h_alpha", "x_ray", "ca_ii_h_k",
            "unverified",
        },
    },
    "disk_measurements": {
        # 한 entry = (paper × belt). Multi-belt 별 (Vega/Fomalhaut/eps Eri) 은
        # 같은 bibcode 로 여러 entry. 일부 paper (Aumann 1984 IRAS) 는 detection
        # 만 — 대부분 value_keys 가 null.
        "value_keys": {
            "inner_radius_au",
            "outer_radius_au",
            "dust_temperature_k",
            "dust_mass_mearth",
            "inclination_deg",
        },
        "methods": {
            "sed_fit",            # Spitzer/Herschel SED 두 성분 fit
            "resolved_imaging",   # ALMA/Herschel/HST/SPHERE/JWST imaging
            "photometric_excess", # IRAS/WISE/Spitzer-MIPS 단순 초과
            "unverified",
        },
        # disk-specific 보조 필드 (value 도 uncertainty 도 아닌 descriptor 들)
        "extra_keys": {"belt", "morphology", "resolved", "observatory", "notes"},
    },
}

# disk_measurements 는 별도 db/disks_curated.json 으로 분리 (validate_disks_curated).
# 키 이름이 rename 되더라도 stellar_props_curated 에서 자동으로 빠지도록 상수화.
DISK_KIND = "disk_measurements"
assert DISK_KIND in STELLAR_MEASUREMENT_KINDS, (
    f"DISK_KIND constant out of sync with STELLAR_MEASUREMENT_KINDS keys"
)

STELLAR_CURATED_TOPLEVEL_ALLOWED = {
    "teff_k", "teff_bibcode", "spectype",
    "spectype_bibcode", "spectype_reference",
    "meta_notes",   # 자유 서술 노트 — db/systems/<star>.json::meta.notes 로 흘러감
    # 측정값에 묶이지 않는 추가 참고 논문 (supporting reference, 각주 등).
    # 형식: [{"title", "doi", "bibcode", "used_for": [str, ...]}, ...]
    # tau Cet 의 Di Folco 2007 (angular diameter source for Teixeira radius) 가 사례.
    "sources_extra",
} | (set(STELLAR_MEASUREMENT_KINDS.keys()) - {DISK_KIND})

STELLAR_MEASUREMENT_BASE_REQUIRED = {"method", "recommended"}
STELLAR_MEASUREMENT_COMMON_OPTIONAL = {"reference", "bibcode", "doi"}
# 참고: source_title / source_used_for / emit_source 는 mass/radius 의 extra_keys
# 로 제한됨 (자동 sources[] 생성이 mass/radius 에만 있기 때문). 다른 카테고리에
# 적용해도 빌드가 무시하므로 schema 단계에서 거부한다.

# Backward-compat union (methodology.md 등 외부 문서 참조용).
# 캐노니컬 소스는 STELLAR_MEASUREMENT_KINDS[*]["methods"].
STELLAR_ALLOWED_METHODS = set().union(
    *(kind["methods"] for kind in STELLAR_MEASUREMENT_KINDS.values())
)


def _uncertainty_keys_for(value_keys):
    """value_msun → uncertainty_msun 패턴으로 변환.

    Stellar 측정값은 value_msun/value_rsun 형태로 `value_` prefix 가 있어 그대로
    치환. disk_measurements 처럼 prefix 없는 value 키 (inner_radius_au 등) 는
    `uncertainty_` 를 prepend.
    """
    return {
        k.replace("value_", "uncertainty_", 1) if k.startswith("value_")
        else f"uncertainty_{k}"
        for k in value_keys
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

        for mk, kind in STELLAR_MEASUREMENT_KINDS.items():
            arr = rec.get(mk) or []
            if not isinstance(arr, list):
                errors.append(f"stellar_props_curated[{star}].{mk}: list 아님")
                continue

            allowed_value_keys = kind["value_keys"]
            allowed_uncertainty_keys = _uncertainty_keys_for(allowed_value_keys)
            allowed_methods = kind["methods"]
            extra_keys = kind.get("extra_keys", set())
            allowed_all = (
                STELLAR_MEASUREMENT_BASE_REQUIRED
                | STELLAR_MEASUREMENT_COMMON_OPTIONAL
                | allowed_value_keys
                | allowed_uncertainty_keys
                | extra_keys
            )

            n_recommended = 0
            for i, m in enumerate(arr):
                if not isinstance(m, dict):
                    errors.append(f"stellar_props_curated[{star}].{mk}[{i}]: dict 아님")
                    continue
                mkeys = set(m.keys())
                if not (mkeys & allowed_value_keys):
                    errors.append(
                        f"stellar_props_curated[{star}].{mk}[{i}]: "
                        f"value 키 누락 (허용: {sorted(allowed_value_keys)})"
                    )
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
                if method and method not in allowed_methods:
                    errors.append(
                        f"stellar_props_curated[{star}].{mk}[{i}]: method '{method}' 미지원 "
                        f"(허용: {sorted(allowed_methods)})"
                    )
                if m.get("recommended") is True:
                    n_recommended += 1
                    # recommended 측정값은 derived value 의 출처가 되므로 sources[] 에서
                    # 빠질 수 없음. emit_source=false 와 양립 불가.
                    if m.get("emit_source") is False:
                        errors.append(
                            f"stellar_props_curated[{star}].{mk}[{i}]: recommended:true 와 "
                            f"emit_source:false 양립 불가 (derived 값의 attribution 누락)"
                        )
                unk = mkeys - allowed_all
                if unk:
                    errors.append(f"stellar_props_curated[{star}].{mk}[{i}]: 알 수 없는 키 {sorted(unk)}")
            if n_recommended > 1:
                errors.append(
                    f"stellar_props_curated[{star}].{mk}: recommended:true 가 {n_recommended}개 "
                    f"(정확히 0 또는 1개)"
                )
    return errors


# ── disks_curated.json 스키마 ───────────────────────────────────────────────
# debris/circumstellar disk 측정값은 star 와 1:N 관계지만 (한 별이 다수의 belt
# entry 보유), stellar_props 와 의미가 분리되어 별도 파일로 관리.
# 구조: {star_name: {"disk_measurements": [entry, ...], "meta_notes": str?}}
# entry 는 STELLAR_MEASUREMENT_KINDS["disk_measurements"] 스키마 재사용.

DISKS_CURATED_TOPLEVEL_ALLOWED = {"disk_measurements", "meta_notes"}

def validate_disks_curated(records, known_components=None):
    """db/disks_curated.json 검증.

    Args:
        records: parsed JSON.
        known_components: target_list.json 의 components 합집합 (set). 주어지면
            disks_curated 의 host key 가 active target 이 아닌 경우 에러로 보고
            (typo/orphan 방지). None 이면 cross-check 생략.
    """
    errors = []
    kind = STELLAR_MEASUREMENT_KINDS[DISK_KIND]
    allowed_value_keys = kind["value_keys"]
    allowed_uncertainty_keys = _uncertainty_keys_for(allowed_value_keys)
    allowed_methods = kind["methods"]
    extra_keys = kind.get("extra_keys", set())
    allowed_all = (
        STELLAR_MEASUREMENT_BASE_REQUIRED
        | STELLAR_MEASUREMENT_COMMON_OPTIONAL
        | allowed_value_keys
        | allowed_uncertainty_keys
        | extra_keys
    )

    for star, rec in records.items():
        if not isinstance(rec, dict):
            errors.append(f"disks_curated[{star}]: dict 아님")
            continue
        if known_components is not None and star not in known_components:
            errors.append(
                f"disks_curated[{star}]: target_list 의 components 에 없음 "
                f"(typo 또는 orphan — 캐노니컬 이름 확인 필요)"
            )
        unknown = set(rec.keys()) - DISKS_CURATED_TOPLEVEL_ALLOWED
        if unknown:
            errors.append(f"disks_curated[{star}]: 알 수 없는 키 {sorted(unknown)}")

        arr = rec.get("disk_measurements") or []
        if not isinstance(arr, list):
            errors.append(f"disks_curated[{star}].disk_measurements: list 아님")
            continue

        for i, m in enumerate(arr):
            if not isinstance(m, dict):
                errors.append(f"disks_curated[{star}].disk_measurements[{i}]: dict 아님")
                continue
            mkeys = set(m.keys())
            # value_keys 중 적어도 하나의 키가 *존재* 해야 함 (값 자체는 null 가능 —
            # IRAS 등 detection-only paper 도 belt/morphology 만 남는 경우 허용).
            if not (mkeys & allowed_value_keys):
                errors.append(
                    f"disks_curated[{star}].disk_measurements[{i}]: "
                    f"value 키 누락 (허용: {sorted(allowed_value_keys)} 중 하나 이상 키 존재)"
                )
            forbidden = [k for k in mkeys if k.startswith(MEASUREMENT_FORBIDDEN_PREFIX)]
            if forbidden:
                errors.append(
                    f"disks_curated[{star}].disk_measurements[{i}]: 금지 prefix {forbidden} "
                    f"(uncertainty_* 사용)"
                )
            miss = STELLAR_MEASUREMENT_BASE_REQUIRED - mkeys
            if miss:
                errors.append(
                    f"disks_curated[{star}].disk_measurements[{i}]: 필수 키 누락 {sorted(miss)}"
                )
            method = m.get("method")
            if method and method not in allowed_methods:
                errors.append(
                    f"disks_curated[{star}].disk_measurements[{i}]: method '{method}' 미지원 "
                    f"(허용: {sorted(allowed_methods)})"
                )
            unk = mkeys - allowed_all
            if unk:
                errors.append(
                    f"disks_curated[{star}].disk_measurements[{i}]: 알 수 없는 키 {sorted(unk)}"
                )
    return errors


# ── planets_curated.json 스키마 ──────────────────────────────────────────────
# host_name → list of {pl_name, orbital, physical, environment, atmosphere}.
# 각 블록은 단일 dict (Phase 1) 또는 list-of-dict (Phase 2 다중 paper) 허용.
#
# Phase 2 expansion (2026-05-21): orbital 에 period_days/tperi_bjd/tranmid_bjd
# 추가, environment (Teq/density/brightness temp 등 모든 행성에 적용) 와
# atmosphere (분광 검출/retrieval — 일부 행성에만) 블록 신설.

PLANET_CURATED_REQUIRED = {"pl_name"}
PLANET_PROVENANCE_KEYS = {"source", "reference", "bibcode", "doi"}

# 공통 provenance/메타 키 — 모든 planet 블록이 받음.
PLANET_BLOCK_COMMON = {
    "source", "reference", "bibcode", "doi",   # provenance (source/reference 동의어)
    "method", "recommended",                    # Phase 2 array element fields
}

PLANET_ORBITAL_ALLOWED = PLANET_BLOCK_COMMON | {
    "period_days", "uncertainty_period_days",
    "semi_major_axis_au", "uncertainty_semi_major_axis_au",
    "eccentricity", "uncertainty_eccentricity",
    "inclination_deg", "uncertainty_inclination_deg",
    "argument_of_periapsis_deg", "uncertainty_argument_of_periapsis_deg",
    "longitude_of_ascending_node_deg", "uncertainty_longitude_of_ascending_node_deg",
    "mean_anomaly_at_epoch_deg", "uncertainty_mean_anomaly_at_epoch_deg",
    "epoch_jd",
    "tperi_bjd", "uncertainty_tperi_bjd",
    "tranmid_bjd", "uncertainty_tranmid_bjd",
}
PLANET_PHYSICAL_ALLOWED = PLANET_BLOCK_COMMON | {
    "mass_mearth", "true_mass_mearth", "uncertainty_mearth", "mass_type",
    "radius_rearth", "uncertainty_rearth",
}
PLANET_ENVIRONMENT_ALLOWED = PLANET_BLOCK_COMMON | {
    "equilibrium_temperature_k", "uncertainty_equilibrium_temperature_k",
    "bond_albedo", "uncertainty_bond_albedo",
    "irradiation_flux_sun", "uncertainty_irradiation_flux_sun",
    "density_g_cc", "uncertainty_density_g_cc",
    "dayside_brightness_temperature_k", "uncertainty_dayside_brightness_temperature_k",
    "nightside_brightness_temperature_k", "uncertainty_nightside_brightness_temperature_k",
}
PLANET_ATMOSPHERE_ALLOWED = PLANET_BLOCK_COMMON | {
    "detection",                   # bool
    "species_detected",            # list[str]
    "species_excluded",            # list[str]
    "significance_sigma",
    "pressure_pa", "uncertainty_pressure_pa",
    "scale_height_km", "uncertainty_scale_height_km",
    "temperature_isothermal_k", "uncertainty_temperature_isothermal_k",
    "mean_molecular_weight_amu", "uncertainty_mean_molecular_weight_amu",
}

# Phase 2 method 화이트리스트 — 블록별로 다른 검출/관측 방식.

# orbital / physical: 발견 method tier 순:
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

PLANET_ENVIRONMENT_METHODS = {
    "derived_from_a_l_albedo",     # Teq = T_star * sqrt(R_star/2a) * (1-A)^0.25 등 표준 공식
    "phase_curve",                  # full-orbit photometry → Tday/Tnight
    "emission_spectrum",            # secondary eclipse / direct emission detection
    "transit_radiometry",
    "secondary_eclipse",
    "discovery",
    "unverified",
}

PLANET_ATMOSPHERE_METHODS = {
    "transmission_spectrum",        # 1차 transit 분광
    "emission_spectrum",            # 2차 식 분광
    "phase_curve",
    "high_res_cross_correlation",   # HARPS/ESPRESSO 분자선 검출
    "secondary_eclipse",
    "non_detection",                # 상한선만 보고
    "unverified",
}

# 블록 검증 메타데이터 — validate_planets_curated 가 iterate.
PLANET_BLOCKS = {
    "orbital":     {"allowed": PLANET_ORBITAL_ALLOWED,     "methods": PLANET_ALLOWED_METHODS},
    "physical":    {"allowed": PLANET_PHYSICAL_ALLOWED,    "methods": PLANET_ALLOWED_METHODS},
    "environment": {"allowed": PLANET_ENVIRONMENT_ALLOWED, "methods": PLANET_ENVIRONMENT_METHODS},
    "atmosphere":  {"allowed": PLANET_ATMOSPHERE_ALLOWED,  "methods": PLANET_ATMOSPHERE_METHODS},
}
PLANET_CURATED_OPTIONAL = set(PLANET_BLOCKS.keys())


def validate_planets_curated(records):
    """db/planets_curated.json 검증.

    각 행성의 orbital / physical / environment / atmosphere 블록이 존재하면
    최소 하나의 provenance 필드(source/bibcode/doi)를 요구.
    array 형식은 method 필수 + 카테고리별 whitelist + 최대 1개 recommended:true.
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

            for block_name, spec in PLANET_BLOCKS.items():
                block = pl.get(block_name)
                if block is None:
                    continue
                allowed = spec["allowed"]
                allowed_methods = spec["methods"]

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
                    loc = f"planets_curated[{host}][{i}].{block_name}" + (f"[{j}]" if is_array else "")
                    if not isinstance(elem, dict):
                        errors.append(f"{loc}: dict 아님")
                        continue
                    bunk = set(elem.keys()) - allowed
                    if bunk:
                        errors.append(f"{loc}: 알 수 없는 키 {sorted(bunk)}")
                    if not (PLANET_PROVENANCE_KEYS & set(elem.keys())):
                        errors.append(f"{loc}: source/bibcode/doi 중 하나 필요")
                    if is_array:
                        method = elem.get("method")
                        if not method:
                            errors.append(f"{loc}: array 형식은 'method' 필수")
                        elif method not in allowed_methods:
                            errors.append(
                                f"{loc}: method '{method}' 미지원 "
                                f"(허용: {sorted(allowed_methods)})"
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
