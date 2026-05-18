# db/systems/*.json에서 target_list.json을 자동 생성하는 일회성 유틸리티
import json, glob, os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB   = os.path.join(BASE, "db")

with open(f"{DB}/binary_orbits.json") as f:
    binary_orbits = json.load(f)

# binary_orbits.json에 정의된 다성계 (system_name → [component_names])
binary_systems = {
    name: data["components"]
    for name, data in binary_orbits.items()
    if not name.startswith("_") and data.get("components")
}
binary_star_names = {name for comps in binary_systems.values() for name in comps}

# 모든 system/*.json에서 항성별 데이터 추출
star_data = {}  # star_name → gaia_source_id (or None)
for path in sorted(glob.glob(f"{DB}/systems/*.json")):
    with open(path) as f:
        doc = json.load(f)
    for star in doc.get("stars", []):
        name = star["name"]
        raw  = star.get("raw", {})
        sid  = raw.get("source_id")
        # Gaia DR3 ID는 숫자 문자열
        gaia_id = sid if (sid and str(sid).isdigit()) else None
        star_data[name] = gaia_id

entries = []

# 1. binary_orbits.json에 정의된 다성계 먼저 처리
for sys_name, comps in binary_systems.items():
    entries.append({
        "system":         sys_name,
        "components":     comps,
        "gaia_source_ids": [star_data.get(c) for c in comps],
        "hip_ids":        [],
        "binary":         True,
    })

# 2. 나머지는 단일 항성 시스템
for star_name in sorted(star_data):
    if star_name in binary_star_names:
        continue
    gaia_id = star_data[star_name]
    entries.append({
        "system":         star_name,
        "components":     [star_name],
        "gaia_source_ids": [gaia_id] if gaia_id else [],
        "hip_ids":        [],
        "binary":         False,
    })

# 다성계 먼저, 그 다음 알파벳순
entries.sort(key=lambda e: (not e["binary"], e["system"]))

out = os.path.join(BASE, "db", "target_list.json")
with open(out, "w") as f:
    json.dump(entries, f, indent=2, ensure_ascii=False)

n_binary = sum(e["binary"] for e in entries)
n_single = len(entries) - n_binary
n_stars  = sum(len(e["components"]) for e in entries)
print(f"target_list.json 생성 완료: {len(entries)}개 시스템 ({n_binary}개 다성계, {n_single}개 단일성계), 총 {n_stars}개 항성")
print(f"→ {out}")
