# 계층(Jacobi) 외곽 궤도 분기의 단위 검증. 실제 시스템 데이터는 모두 외곽 phase_reliable=false 라
# 이 코드 경로가 운영 데이터로 실행되지 않으므로, 합성 fixture로 sanity check.
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_systems import (
    resolve_binary_component_states,
    JD_B1950, JD_J2000, JD_GAIA, AU_TO_KM, YR_TO_S,
)


def _make_fixture():
    """face-on (i=0), ω=Ω=0, T=JD_B1950 인 단순 외곽 궤도 + 평탄 내부 궤도.
    내부는 같은 face-on 단순 형태로 설정해 caller가 거치는 평탄 경로도 한 번 거치게 함.
    """
    # Components at J2016 (Gaia epoch). RA/Dec 작은 값 → ICRF 변환 안정.
    # A, B는 mass_weighted_average → astrometry_raw에 두 항목 필요.
    # C는 single_component:C 로 자체 단일 항성 분기 사용.
    astrometry_raw = {
        "A": dict(ra_deg=100.0,         dec_deg=10.0, parallax_mas=100.0,
                  pmra_mas_yr=0.0, pmdec_mas_yr=0.0, radial_velocity_km_s=0.0,
                  epoch_jd=JD_GAIA),
        "B": dict(ra_deg=100.000001,    dec_deg=10.0, parallax_mas=100.0,
                  pmra_mas_yr=0.0, pmdec_mas_yr=0.0, radial_velocity_km_s=0.0,
                  epoch_jd=JD_GAIA),
        "C": dict(ra_deg=100.0,         dec_deg=10.001, parallax_mas=100.0,
                  pmra_mas_yr=0.0, pmdec_mas_yr=0.0, radial_velocity_km_s=0.0,
                  epoch_jd=JD_GAIA),
    }
    binary_data = {
        "system_id": "synthetic_triple",
        "hierarchy": "triple",
        "components": [
            dict(name="A", mass_msun=1.0,  astrometry_source="mass_weighted_average"),
            dict(name="B", mass_msun=1.0,  astrometry_source="mass_weighted_average"),
            dict(name="C", mass_msun=0.5,  astrometry_source="single_component:C"),
        ],
        "orbits": [
            dict(orbit_id="AB", relates=["A","B"], primary="A", secondary="B",
                 equinox="J2000", P_yr=10.0, T_jd_tt=JD_B1950,
                 e=0.0, a_arcsec=1.0, i_deg=0.0, omega_deg=0.0, Omega_deg=0.0,
                 grade=1, node_resolved=True, phase_reliable=True),
            dict(orbit_id="AB-C", relates=["AB","C"],
                 primary_is_barycenter_of=["A","B"], secondary="C",
                 equinox="J2000", P_yr=1000.0, T_jd_tt=JD_B1950,
                 e=0.0, a_au=1000.0, i_deg=0.0, omega_deg=0.0, Omega_deg=0.0,
                 grade=2, node_resolved=True, phase_reliable=True),
        ],
    }
    return binary_data, astrometry_raw


def _vec_sub(u, v): return tuple(u[i]-v[i] for i in range(3))
def _vec_norm(u):   return math.sqrt(sum(x*x for x in u))


def test_outer_jacobi_branch():
    """T_periastron=JD_B1950, e=0, face-on → C at B1950 is exactly a_au * (1-e) North of g.
    The relative magnitude |r_C - r_g| should equal a_au (in km).
    """
    binary_data, astrometry_raw = _make_fixture()
    out = resolve_binary_component_states("synthetic_triple", binary_data, astrometry_raw)

    assert set(out.keys()) >= {"A", "B", "C"}, f"missing components in out: {out.keys()}"
    assert out["C"]["meta"]["role"] == "outer_companion", out["C"]["meta"]
    assert out["C"]["meta"]["orbit_id"] == "AB-C"
    # mass_ratio_q for outer: m_inner_total / (m_inner_total + m_outer) = 2.0 / 2.5 = 0.8
    assert abs(out["C"]["meta"]["mass_ratio_q"] - 0.8) < 1e-12, out["C"]["meta"]["mass_ratio_q"]

    # 내부 쌍(A, B)의 중심은 무게중심(g)을 통과해야 함.
    # m_A = m_B = 1 → g = (A+B)/2 at B1950.
    r_A = out["A"]["b1950"]["pos_km"]
    r_B = out["B"]["b1950"]["pos_km"]
    r_C = out["C"]["b1950"]["pos_km"]
    g    = tuple((r_A[i] + r_B[i]) / 2.0 for i in range(3))

    # |r_C - g|: outer offset magnitude. a_au=1000 → 1000 * AU_TO_KM 이어야 함.
    expected_outer_km = 1000.0 * AU_TO_KM
    actual_outer_km   = _vec_norm(_vec_sub(r_C, g))
    rel_err = abs(actual_outer_km - expected_outer_km) / expected_outer_km
    assert rel_err < 1e-6, f"outer offset mismatch: expected {expected_outer_km:.6e}, got {actual_outer_km:.6e}, rel_err={rel_err:.2e}"

    # 내부 쌍의 분리도 a_arcsec=1.0 at distance 10 pc (plx=100 mas) → 10 AU.
    expected_inner_km = 10.0 * AU_TO_KM
    actual_inner_km   = _vec_norm(_vec_sub(r_B, r_A))
    rel_err_inner = abs(actual_inner_km - expected_inner_km) / expected_inner_km
    assert rel_err_inner < 1e-6, f"inner separation mismatch: expected {expected_inner_km:.6e}, got {actual_inner_km:.6e}, rel_err={rel_err_inner:.2e}"

    print("PASS test_outer_jacobi_branch:")
    print(f"  outer |r_C - g| = {actual_outer_km:.6e} km (expected {expected_outer_km:.6e}, rel_err {rel_err:.2e})")
    print(f"  inner |r_B - r_A| = {actual_inner_km:.6e} km (expected {expected_inner_km:.6e}, rel_err {rel_err_inner:.2e})")
    print(f"  C meta: {out['C']['meta']}")


def test_outer_phase_unreliable_skipped():
    """phase_reliable=false 외곽 궤도는 secondary를 out에 추가하지 않아야 함 (caller가 폴백 처리)."""
    binary_data, astrometry_raw = _make_fixture()
    binary_data["orbits"][1]["phase_reliable"] = False
    out = resolve_binary_component_states("synthetic_triple_unreliable", binary_data, astrometry_raw)
    assert "A" in out and "B" in out, "inner pair must still be processed"
    assert "C" not in out, "C should be skipped when outer phase_reliable=false (caller falls back)"
    print("PASS test_outer_phase_unreliable_skipped: C correctly skipped for caller fallback")


if __name__ == "__main__":
    test_outer_jacobi_branch()
    test_outer_phase_unreliable_skipped()
    print("\n전체 통과")
