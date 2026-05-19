# target_list.json → NASA Exoplanet Archive + TEPCat → db/planets_raw.json
import json, urllib.request, urllib.parse, os, csv, io, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import schema

BASE        = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARCHIVE_TAP = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
TEPCAT_URL  = "https://www.astro.keele.ac.uk/jkt/tepcat/allplanets-csv.csv"
RETRIEVAL_DATE = __import__("datetime").date.today().isoformat()

MJUP_TO_MEARTH = 317.8284
RJUP_TO_REARTH = 11.2089


def archive_query(query, timeout=120):
    data = urllib.parse.urlencode(
        {"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json", "QUERY": query}
    ).encode()
    req = urllib.request.Request(ARCHIVE_TAP, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


# ── target_list 로드 ───────────────────────────────────────────────────────────
with open(f"{BASE}/db/target_list.json") as f:
    target_list = json.load(f)

target_systems = {e["system"] for e in target_list}


# ── 1. NASA Exoplanet Archive ─────────────────────────────────────────────────
# 거리 사전 필터 없음 — target_list에 들어있는 모든 호스트의 행성을 가져옴.
# 50 ly 너머 별도 DB에 포함 가능 (downstream cfg writer가 거리 limit 결정).
q = """
SELECT
  hostname, pl_name, disc_refname,
  pl_orbper, pl_orbpererr1, pl_orbpererr2,
  pl_orbsmax, pl_orbsmaxerr1, pl_orbsmaxerr2,
  pl_orbeccen,
  pl_orbincl, pl_orbinclerr1,
  pl_orblper,
  pl_orbtper, pl_orbtpererr1,
  pl_tranmid, pl_tranmiderr1,
  pl_bmasse, pl_bmasseerr1, pl_bmasseerr2, pl_bmassprov,
  pl_rade, pl_radeerr1, pl_radeerr2,
  discoverymethod, pl_controv_flag, pl_pubdate
FROM pscomppars
""".strip()

print("NASA Exoplanet Archive 쿼리 중...")
try:
    rows = archive_query(q, timeout=120)
    rows = [r for r in rows if r.get("hostname") in target_systems]
    print(f"  {len(rows)}개 행성 반환")
except Exception as e:
    print(f"  Archive 쿼리 오류: {e}")
    rows = []

results = {}
for row in rows:
    host = row["hostname"]
    if host not in results:
        results[host] = []
    results[host].append({
        "pl_name":              row["pl_name"],
        "reference":            row.get("disc_refname"),
        "retrieval_date":       RETRIEVAL_DATE,
        "period_days":          row["pl_orbper"],
        "period_err_days":      row.get("pl_orbpererr1"),
        "semi_major_axis_au":   row["pl_orbsmax"],
        "semi_major_axis_err_au": row.get("pl_orbsmaxerr1"),
        "eccentricity":         row["pl_orbeccen"],
        "inclination_deg":      row["pl_orbincl"],
        "inclination_err_deg":  row.get("pl_orbinclerr1"),
        "omega_deg":            row.get("pl_orblper"),
        "tperi_bjd":            row.get("pl_orbtper"),
        "tperi_err_bjd":        row.get("pl_orbtpererr1"),
        "tranmid_bjd":          row.get("pl_tranmid"),
        "tranmid_err_bjd":      row.get("pl_tranmiderr1"),
        "mass_mearth":          row["pl_bmasse"],
        "mass_err_mearth":      row.get("pl_bmasseerr1"),
        "mass_type":            row.get("pl_bmassprov"),
        "radius_rearth":        row["pl_rade"],
        "radius_err_rearth":    row.get("pl_radeerr1"),
        "discoverymethod":      row.get("discoverymethod"),
        "pl_controv_flag":      row.get("pl_controv_flag", 0),
        "pubdate":              row.get("pl_pubdate"),
    })

for host in results:
    results[host].sort(key=lambda p: p["semi_major_axis_au"] or 9999)


# ── 2. TEPCat (트랜짓 행성 질량·반지름 보완) ──────────────────────────────────
# TEPCat 이름 포맷이 일관되지 않음. 여러 변환 후보를 시도.
# "55 Cnc e"      → "55_Cnc_e"    (공백 → 밑줄)
# "GJ 1214 b"     → "GJ_1214b"    (호스트 밑줄, 행성 글자 직접 연결)
# "TRAPPIST-1 c"  → "TRAPPIST-1c" (공백 제거)
# "LTT 1445 A b"  → "LTT_1445Ab"  (컴포넌트 글자 + 행성 글자 직접 연결)
def tepcat_keys(pl_name):
    parts = pl_name.rsplit(" ", 1)
    if len(parts) != 2:
        return [pl_name.replace(" ", "_")]
    host, letter = parts
    candidates = [
        pl_name.replace(" ", "_"),          # 55_Cnc_e
        host.replace(" ", "_") + letter,    # GJ_1214b, LHS_1140b
        pl_name.replace(" ", ""),           # TRAPPIST-1c
    ]
    # 호스트에 대문자 컴포넌트 글자가 있는 경우: "LTT 1445 A" → "LTT_1445A" + letter
    host_parts = host.split()
    if len(host_parts) >= 2 and host_parts[-1].isupper() and len(host_parts[-1]) == 1:
        candidates.append("_".join(host_parts[:-1]) + host_parts[-1] + letter)
    return list(dict.fromkeys(candidates))  # 중복 제거, 순서 유지

print("\nTEPCat 로드 중...")
tepcat = {}  # tepcat_key → dict
try:
    req = urllib.request.Request(TEPCAT_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        content = r.read().decode("utf-8", errors="replace")

    reader = csv.reader(io.StringIO(content))
    header = next(reader)
    # 컬럼 인덱스: System(0) Period(19) e(20) a_AU(23) M_b_Mjup(26) R_b_Rjup(29) Teq(38) Recent_ref(42)
    IDX = {
        "system": 0, "teff": 1,
        "period": 19, "ecc": 20, "ecc_err_up": 21, "ecc_err_dn": 22,
        "sma": 23, "sma_err_up": 24,
        "mass_mjup": 26, "mass_err_up": 27, "mass_err_dn": 28,
        "radius_rjup": 29, "radius_err_up": 30, "radius_err_dn": 31,
        "teq": 38,
        "recent_ref": 42,
    }
    for cols in reader:
        if len(cols) <= max(IDX.values()):
            continue
        key = cols[IDX["system"]].strip()
        if not key:
            continue

        def fval(idx):
            try: return float(cols[idx].strip()) if cols[idx].strip() else None
            except: return None

        mass_mj  = fval(IDX["mass_mjup"])
        rad_rj   = fval(IDX["radius_rjup"])
        if mass_mj is not None and mass_mj <= 0:
            mass_mj = None
        if rad_rj is not None and rad_rj <= 0:
            rad_rj = None
        mass_err = fval(IDX["mass_err_up"])
        rad_err  = fval(IDX["radius_err_up"])
        if mass_err is not None and mass_err <= 0:
            mass_err = None
        if rad_err is not None and rad_err <= 0:
            rad_err = None
        tepcat[key] = {
            "mass_mjup":       mass_mj,
            "mass_mearth":     round(mass_mj * MJUP_TO_MEARTH, 4) if mass_mj else None,
            "mass_err_mearth": round(mass_err * MJUP_TO_MEARTH, 4) if mass_err else None,
            "radius_rjup":     rad_rj,
            "radius_rearth":   round(rad_rj * RJUP_TO_REARTH, 4) if rad_rj else None,
            "radius_err_rearth": round(rad_err * RJUP_TO_REARTH, 4) if rad_err else None,
            "period_days":     fval(IDX["period"]),
            "eccentricity":    fval(IDX["ecc"]),
            "semi_major_axis_au": fval(IDX["sma"]),
            "teq_k":           fval(IDX["teq"]),
            "bibcode":         cols[IDX["recent_ref"]].strip() if len(cols) > IDX["recent_ref"] else None,
        }
    print(f"  {len(tepcat)}개 행성 로드")
except Exception as e:
    print(f"  TEPCat 로드 오류: {e}")

# TEPCat 데이터를 해당 행성에 주입
n_matched = 0
for host_planets in results.values():
    for pl in host_planets:
        for key in tepcat_keys(pl["pl_name"]):
            if key in tepcat:
                pl["tepcat"] = tepcat[key]
                n_matched += 1
                break
print(f"  → {n_matched}개 행성에 TEPCat 데이터 연결")


# ── 저장 ──────────────────────────────────────────────────────────────────────
out_path = f"{BASE}/db/planets_raw.json"
with open(out_path, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

n_planets = sum(len(v) for v in results.values())
n_omega   = sum(1 for ps in results.values() for p in ps if p.get("omega_deg") is not None)
n_tperi   = sum(1 for ps in results.values() for p in ps if p.get("tperi_bjd") is not None)
n_tepcat  = sum(1 for ps in results.values() for p in ps if p.get("tepcat"))
print(f"\n완료: {len(results)}개 항성계, {n_planets}개 행성")
print(f"  ω 있음:    {n_omega}/{n_planets}")
print(f"  T_peri 있음: {n_tperi}/{n_planets}")
print(f"  TEPCat 있음: {n_tepcat}/{n_planets}")
print(f"→ {out_path}")

planets_flat = {pl["pl_name"]: pl for pls in results.values() for pl in pls}
errs = schema.validate(planets_flat, schema.PLANET_REQUIRED,
                       schema.PLANET_OPTIONAL, name="planets")
schema.report_and_exit(errs, "planets_raw")
