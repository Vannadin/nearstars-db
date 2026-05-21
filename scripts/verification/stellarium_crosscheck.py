# Stellarium 의 visual binary sky-offset 알고리즘을 Python 으로 재구현하고
# NearStars binary_orbits.json 데이터로도 같은 계산을 돌려 두 파이프라인의
# 컨벤션 일치 여부를 확인하는 검증 스크립트

import json
import math
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
NS_BINARY_ORBITS = REPO_ROOT / "db" / "binary_orbits.json"
STELLARIUM_DATA = pathlib.Path("/tmp/stellarium_binary_orbitparam.dat")

# Target epoch for the comparison. J2024.0 = JD 2460310.5 (TT).
TARGET_JD = 2460310.5
TARGET_LABEL = "J2024.0"


def solve_kepler_newton(M, e, tol=1e-12, max_iter=100):
    """Stellarium Star.hpp #L332-L353 의 Newton-Raphson Kepler solver."""
    M = M % (2 * math.pi)
    E = M
    for _ in range(max_iter):
        dE = (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
        E -= dE
        if abs(dE) < tol:
            break
    return E


def stellarium_style(elements, target_jd):
    """Stellarium Star.hpp 의 'r * rotation' 형태 직접 평가.
    Returns (Δα·cosδ, Δδ) in arcsec, secondary relative to primary.
    """
    P_d = elements["P_d"]
    e = elements["e"]
    i = elements["i_rad"]
    Omega = elements["Omega_rad"]
    omega = elements["omega_rad"]
    T = elements["T_jd"]
    a = elements["a_arcsec"]

    n = 2 * math.pi / P_d
    M = n * (target_jd - T)
    E = solve_kepler_newton(M, e)

    nu = 2 * math.atan2(
        math.sqrt(1 + e) * math.sin(E / 2),
        math.sqrt(1 - e) * math.cos(E / 2),
    )
    r = a * (1 - e * math.cos(E))

    # Hilditch (2001) projection onto sky plane.
    # Δδ (North) and Δα·cosδ (East), both in arcsec.
    cos_O, sin_O = math.cos(Omega), math.sin(Omega)
    cos_i = math.cos(i)
    cos_nu_w, sin_nu_w = math.cos(nu + omega), math.sin(nu + omega)

    d_dec = r * (cos_O * cos_nu_w - sin_O * sin_nu_w * cos_i)
    d_ra_cosdec = r * (sin_O * cos_nu_w + cos_O * sin_nu_w * cos_i)
    return d_ra_cosdec, d_dec


def thiele_innes(elements, target_jd):
    """Thiele-Innes 상수 + (x, y) 표현. Stellarium 의 r·rotation 과
    수학적으로 등가지만 다른 표현 경로 — 알고리즘 독립 sanity check 용.
    """
    P_d = elements["P_d"]
    e = elements["e"]
    i = elements["i_rad"]
    Omega = elements["Omega_rad"]
    omega = elements["omega_rad"]
    T = elements["T_jd"]
    a = elements["a_arcsec"]

    n = 2 * math.pi / P_d
    M = n * (target_jd - T)
    # 동일 M 으로 풀어서 두 표현이 수학적으로 동치임을 확인.
    E = solve_kepler_newton(M, e, tol=1e-14)

    cos_O, sin_O = math.cos(Omega), math.sin(Omega)
    cos_w, sin_w = math.cos(omega), math.sin(omega)
    cos_i = math.cos(i)

    A = a * (cos_O * cos_w - sin_O * sin_w * cos_i)
    B = a * (sin_O * cos_w + cos_O * sin_w * cos_i)
    F = a * (-cos_O * sin_w - sin_O * cos_w * cos_i)
    G = a * (-sin_O * sin_w + cos_O * cos_w * cos_i)

    x = math.cos(E) - e
    y = math.sqrt(1 - e * e) * math.sin(E)

    d_dec = A * x + F * y
    d_ra_cosdec = B * x + G * y
    return d_ra_cosdec, d_dec


def load_stellarium_elements():
    """Stellarium binary_orbitparam.dat 의 3개 비교 대상 시스템 추출."""
    lookup = {
        "Alpha Centauri": ("71683", "71681"),
        "Sirius": ("32349", "2947050466531873024"),
        "61 Cygni": ("1872046609345556480", "1872046574983497216"),
    }
    by_pair = {}
    with STELLARIUM_DATA.open() as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            cols = line.split("\t")
            by_pair[(cols[0], cols[1])] = cols

    result = {}
    for label, key in lookup.items():
        if key not in by_pair:
            print(f"WARN: {label} {key} not found in Stellarium data", file=sys.stderr)
            continue
        c = by_pair[key]
        result[label] = {
            "source": "Stellarium binary_orbitparam.dat",
            "P_d": float(c[2]),
            "e": float(c[3]),
            "i_rad": float(c[4]),
            "Omega_rad": float(c[5]),
            "omega_rad": float(c[6]),
            "T_jd": float(c[7]),
            "a_arcsec": float(c[8]),
        }
    return result


def load_ns_elements():
    """NearStars db/binary_orbits.json 의 AB 궤도 3개."""
    with NS_BINARY_ORBITS.open() as f:
        data = json.load(f)
    result = {}
    for sys_name in ["Alpha Centauri", "Sirius", "61 Cygni"]:
        sys_data = data[sys_name]
        ab = next(o for o in sys_data["orbits"] if o["orbit_id"] == "AB")
        # NS 는 P 를 year, T 를 JD_TT, 각도를 도, a 를 arcsec 로 저장.
        result[sys_name] = {
            "source": ab.get("source", "NearStars binary_orbits.json"),
            "equinox": ab.get("equinox", "?"),
            "P_d": ab["P_yr"] * 365.25,
            "e": ab["e"],
            "i_rad": math.radians(ab["i_deg"]),
            "Omega_rad": math.radians(ab["Omega_deg"]),
            "omega_rad": math.radians(ab["omega_deg"]),
            "T_jd": ab["T_jd_tt"],
            "a_arcsec": ab["a_arcsec"],
        }
    return result


def vec_mag(dx, dy):
    return math.sqrt(dx * dx + dy * dy)


def fmt_offset(dra, ddec):
    sep = vec_mag(dra, ddec)
    # Position angle measured from N through E.
    pa = math.degrees(math.atan2(dra, ddec)) % 360
    return f"Δα·cosδ={dra*1000:+9.1f} mas  Δδ={ddec*1000:+9.1f} mas  (sep={sep:.4f}″, PA={pa:.2f}°)"


def compare_system(label, ns_elem, stl_elem):
    print(f"\n{'='*72}")
    print(f"{label}  @  {TARGET_LABEL}  (JD {TARGET_JD})")
    print(f"{'='*72}")

    print("\nOrbital element comparison.")
    keys = [
        ("P (yr)", "P_d", lambda v: v / 365.25),
        ("e", "e", lambda v: v),
        ("a (arcsec)", "a_arcsec", lambda v: v),
        ("i (deg)", "i_rad", lambda v: math.degrees(v)),
        ("Ω (deg)", "Omega_rad", lambda v: math.degrees(v)),
        ("ω (deg)", "omega_rad", lambda v: math.degrees(v)),
        ("T (JD)", "T_jd", lambda v: v),
    ]
    for name, key, conv in keys:
        n_val = conv(ns_elem[key])
        s_val = conv(stl_elem[key])
        diff = s_val - n_val
        print(f"  {name:14s}  NS={n_val:14.5f}   Stellarium={s_val:14.5f}   Δ={diff:+.5f}")
    print(f"  source         NS: {ns_elem['source'][:60]}")
    print(f"                  Stellarium: {stl_elem['source'][:60]}")
    if ns_elem.get("equinox") and ns_elem["equinox"] != "J2000":
        print(f"  *** NS equinox = {ns_elem['equinox']} (Stellarium implicitly J2000) ***")

    # Test 1 — Algorithm equivalence on the SAME elements.
    print("\nTest 1. 같은 원소를 두 알고리즘에 통과 → 수학적 등가성.")
    for src_label, elem in [("Stellarium-data", stl_elem), ("NS-data", ns_elem)]:
        stl_result = stellarium_style(elem, TARGET_JD)
        ti_result = thiele_innes(elem, TARGET_JD)
        diff_dra = abs(stl_result[0] - ti_result[0]) * 1000
        diff_ddec = abs(stl_result[1] - ti_result[1]) * 1000
        status = "✓" if max(diff_dra, diff_ddec) < 0.001 else "✗"
        print(f"  [{src_label}]  Stellarium-style: {fmt_offset(*stl_result)}")
        print(f"  {' ' * (len(src_label)+4)}  Thiele-Innes:    {fmt_offset(*ti_result)}")
        print(f"  {' ' * (len(src_label)+4)}  algorithm diff:   {diff_dra:.6f} mas, {diff_ddec:.6f} mas  {status}")

    # Test 2 — Data drift via the SAME algorithm.
    print("\nTest 2. 같은 알고리즘(Stellarium-style) 에 두 데이터 → 데이터 drift.")
    stl_pos = stellarium_style(stl_elem, TARGET_JD)
    ns_pos = stellarium_style(ns_elem, TARGET_JD)
    d_dra = (stl_pos[0] - ns_pos[0]) * 1000
    d_ddec = (stl_pos[1] - ns_pos[1]) * 1000
    d_mag = vec_mag(d_dra, d_ddec)
    if d_mag < 10:
        verdict = "✓ < 10 mas — 데이터 일치 양호"
    elif d_mag < 100:
        verdict = "~ < 100 mas — 데이터 drift 존재 (출처 revision 차이일 가능성)"
    else:
        verdict = "✗ > 100 mas — sign 또는 frame 차이 의심"
    print(f"  Stellarium data: {fmt_offset(*stl_pos)}")
    print(f"  NS data:         {fmt_offset(*ns_pos)}")
    print(f"  vector diff:     {d_dra:+.1f} mas, {d_ddec:+.1f} mas  (|Δ|={d_mag:.1f} mas)")
    print(f"  {verdict}")


def main():
    if not STELLARIUM_DATA.exists():
        print(f"missing {STELLARIUM_DATA}", file=sys.stderr)
        print(f"fetch via curl from Stellarium repo first", file=sys.stderr)
        sys.exit(1)

    ns = load_ns_elements()
    stl = load_stellarium_elements()

    print(f"Stellarium ↔ NearStars binary-orbit cross-check  @  {TARGET_LABEL} (JD {TARGET_JD})")

    for sys_name in ["Alpha Centauri", "Sirius", "61 Cygni"]:
        if sys_name in ns and sys_name in stl:
            compare_system(sys_name, ns[sys_name], stl[sys_name])

    print()


if __name__ == "__main__":
    main()
