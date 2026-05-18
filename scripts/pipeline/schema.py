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
