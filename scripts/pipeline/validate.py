# build_systems.py 출력 검증 — 필수 필드, 에포크 일관성, vmag_v 존재 여부 확인
import json, math, glob, os, sys

BASE    = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SYSTEMS = os.path.join(BASE, "db", "systems")
DB      = os.path.join(BASE, "db")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schema import validate_binary_orbits

JD_B1950 = 2433282.5
JD_J2000 = 2451545.0
DT_B1950_TO_J2000_S = (JD_J2000 - JD_B1950) * 86400.0  # ~1.66e9 s

errors   = []
warnings = []

def fail(fname, msg):
    errors.append(f"{fname}: {msg}")
    print(f"  [FAIL] {msg}")

def warn(fname, msg):
    warnings.append(f"{fname}: {msg}")
    print(f"  [WARN] {msg}")

def ok(msg):
    print(f"  [PASS] {msg}")


files = sorted(glob.glob(f"{SYSTEMS}/*.json"))
print(f"검증 대상: {len(files)}개 파일\n")

if not files:
    print("파일 없음. build_systems.py를 먼저 실행하세요.")
    exit(1)

docs = {}
for path in files:
    fname = os.path.basename(path)
    with open(path) as f:
        docs[fname] = json.load(f)

ok(f"{len(docs)}개 파일 로드 완료")


# ── 1. 필수 최상위 키 ─────────────────────────────────────────────────────────
print("\n── 1. 최상위 구조 ───────────────────────────────────────────────────────")
for fname, doc in docs.items():
    for key in ("stars", "planets", "sources", "meta"):
        if key not in doc:
            fail(fname, f"최상위 키 누락: '{key}'")
    if not doc.get("stars"):
        fail(fname, "stars[] 비어있음")
ok("최상위 키 확인 완료")


# ── 2. raw 필드 ───────────────────────────────────────────────────────────────
print("\n── 2. raw 필드 ──────────────────────────────────────────────────────────")
required_raw = ("ra_deg", "dec_deg", "parallax_mas", "pmra_mas_yr", "pmdec_mas_yr",
                "radial_velocity_km_s", "teff_k", "spectype")
missing_vmag = []
for fname, doc in docs.items():
    for star in doc.get("stars", []):
        raw = star.get("raw", {})
        for field in required_raw:
            if raw.get(field) is None:
                warn(fname, f"raw.{field} 없음")
        if raw.get("vmag_v") is None:
            missing_vmag.append(fname)
        if not raw.get("mass_measurements"):
            warn(fname, "mass_measurements 비어있음")
        if not raw.get("radius_measurements"):
            warn(fname, "radius_measurements 비어있음")

if missing_vmag:
    warn("(전체)", f"vmag_v 없는 파일 {len(missing_vmag)}개: {missing_vmag[:5]}{'...' if len(missing_vmag)>5 else ''}")
else:
    ok("모든 항성에 vmag_v 있음")
ok("raw 필드 확인 완료")


# ── 3. derived 필드 및 에포크 일관성 ─────────────────────────────────────────
print("\n── 3. derived 좌표 ──────────────────────────────────────────────────────")
required_derived = ("icrs_x_km", "icrs_y_km", "icrs_z_km",
                    "icrs_vx_km_s", "icrs_vy_km_s", "icrs_vz_km_s",
                    "icrs_x_j2000_km", "icrs_y_j2000_km", "icrs_z_j2000_km")
bad_epoch = []
bad_j2000 = []

for fname, doc in docs.items():
    for star in doc.get("stars", []):
        der = star.get("derived", {})
        for field in required_derived:
            if der.get(field) is None:
                fail(fname, f"derived.{field} 없음")

        # B1950 에포크 레이블 확인
        if der.get("epoch_jd") != JD_B1950:
            bad_epoch.append(fname)

        # B1950과 J2000 차이가 속도 × 시간과 대략 일치하는지 확인.
        # 단, Kepler+T-I 컴포넌트는 비선형 — 이 체크 스킵.
        if der.get("propagation_method") == "kepler_thiele_innes":
            continue
        x_b = der.get("icrs_x_km")
        x_j = der.get("icrs_x_j2000_km")
        vx  = der.get("icrs_vx_km_s")
        if x_b is not None and x_j is not None and vx is not None:
            expected_dx = vx * DT_B1950_TO_J2000_S
            actual_dx   = x_j - x_b
            # 오차가 기대값의 1% 이상이면 경고
            if abs(expected_dx) > 1e6 and abs(actual_dx - expected_dx) / abs(expected_dx) > 0.01:
                bad_j2000.append(fname)

if bad_epoch:
    fail("(전체)", f"epoch_jd ≠ {JD_B1950}인 파일: {bad_epoch}")
else:
    ok("모든 파일 B1950 에포크 JD 정확")

if bad_j2000:
    warn("(전체)", f"B1950↔J2000 불일치 의심: {bad_j2000[:5]}")
else:
    ok("B1950↔J2000 전파 일관성 확인")


# ── 4. principia 블록 ────────────────────────────────────────────────────────
print("\n── 4. principia ─────────────────────────────────────────────────────────")
missing_principia = []
for fname, doc in docs.items():
    for star in doc.get("stars", []):
        prin = star.get("principia", {})
        if not prin.get("gravitational_parameter_km3_s2"):
            missing_principia.append(fname)
        if not prin.get("mean_radius_km"):
            missing_principia.append(fname)

if missing_principia:
    warn("(전체)", f"principia 누락 파일 {len(set(missing_principia))}개")
else:
    ok("모든 파일 principia 블록 완전")


# ── 4b. binary_orbits.json 스키마 ────────────────────────────────────────────
print("\n── 4b. binary_orbits 스키마 ────────────────────────────────────────────")
try:
    with open(f"{DB}/binary_orbits.json") as f:
        binary_data = json.load(f)
    bin_errs = validate_binary_orbits(binary_data)
    for e in bin_errs:
        fail("(binary_orbits.json)", e)
    if not bin_errs:
        ok("binary_orbits.json 스키마 통과")
except FileNotFoundError:
    warn("(binary_orbits.json)", "파일 없음 — 다성계 데이터 미보유로 간주")
    binary_data = {}


# ── 4c. 다성계 컴포넌트 derived 일관성 ───────────────────────────────────────
print("\n── 4c. 다성계 컴포넌트 ────────────────────────────────────────────────")
multi_component_count = 0
for sys_name, entry in (binary_data or {}).items():
    if sys_name.startswith("_"):
        continue
    if not isinstance(entry, dict) or "components" not in entry:
        continue
    in_orbit_names = set()
    for orbit in entry.get("orbits", []):
        in_orbit_names.update(orbit.get("relates", []))
    for comp in entry.get("components", []):
        cname = comp.get("name")
        if cname not in in_orbit_names:
            continue   # 궤도 없는 컴포넌트 (예: 40 Eri A) 는 선형 전파 — 별도 체크 없음
        if comp.get("mass_msun") is None:
            fail("(binary)", f"{cname}: orbit-bound 컴포넌트인데 mass_msun=null")
        if not comp.get("astrometry_source"):
            fail("(binary)", f"{cname}: astrometry_source unset (FAIL)")

        # db/systems 파일에서 propagation_method=kepler_thiele_innes 확인
        from_path = None
        for fname, doc in docs.items():
            if doc.get("system_name") == cname:
                from_path = fname; break
        if from_path is None:
            warn("(binary)", f"{cname}: db/systems 파일 없음")
            continue
        der = docs[from_path]["stars"][0].get("derived", {})
        if der.get("propagation_method") != "kepler_thiele_innes":
            fail(from_path, f"{cname}: orbit-bound 컴포넌트인데 "
                            f"propagation_method='{der.get('propagation_method')}' "
                            f"(kepler_thiele_innes 이어야 함)")
        # phase_reliable=false 면 meta.notes 에 경고가 박혀 있어야 함
        if der.get("phase_reliable") is False:
            notes = docs[from_path].get("meta", {}).get("notes", "") or ""
            if "phase_reliable=false" not in notes:
                warn(from_path, f"{cname}: phase_reliable=false 인데 meta.notes 에 경고 없음")
        multi_component_count += 1

if multi_component_count:
    ok(f"다성계 orbit-bound 컴포넌트 {multi_component_count}개 확인")


# ── 5. 행성 호스트 확인 ───────────────────────────────────────────────────────
print("\n── 5. 행성 데이터 ───────────────────────────────────────────────────────")
planet_hosts = [f for f, d in docs.items() if d.get("planets")]
ok(f"행성 포함 파일: {len(planet_hosts)}개")

for fname in planet_hosts:
    for pl in docs[fname]["planets"]:
        der = pl.get("derived", {})
        if not der.get("semi_major_axis_m"):
            warn(fname, f"행성 {pl['name']}: semi_major_axis_m 없음")
        if not der.get("mass_kg"):
            warn(fname, f"행성 {pl['name']}: mass_kg 없음")


# ── 결과 요약 ─────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"파일 수:  {len(docs)}")
print(f"FAIL:    {len(errors)}")
print(f"WARN:    {len(warnings)}")
if errors:
    print("\n오류 목록:")
    for e in errors:
        print(f"  {e}")
if not errors:
    print("\n검증 통과.")
