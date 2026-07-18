# Phase 3 무결성 감사용 결정론적 정적 체크 (행성 커버리지/디스크 중첩/인용 갭/파생값 재계산/블록 parity)
import json, os, re, glob, sys, math, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
sys.path.insert(0, "scripts/pipeline")
from importlib import import_module
to_slug = import_module("_naming").to_url_slug

REPORTS = {os.path.basename(p)[:-3]: p for p in glob.glob("docs/phase3/*.md")}
CACHE = set(os.path.splitext(os.path.basename(f))[0] for f in glob.glob("docs/phase3/_papers/*"))
PLANETS = json.load(open("db/planets_curated.json"))
STELLAR = json.load(open("db/stellar_props_curated.json"))

bibcode_re = re.compile(r'\b(\d{4}[A-Za-z&.][\w&.]{13,15}[A-Z])\b')
arxiv_re = re.compile(r'\b(\d{4}\.\d{4,5})\b')


def recommended(arr, key):
    if not isinstance(arr, list):
        return None
    rec = [m for m in arr if isinstance(m, dict) and m.get("recommended")]
    pool = rec or arr
    for m in pool:
        if isinstance(m, dict) and m.get(key) is not None:
            return m.get(key)
    return None


# host display-name -> slug
host_by_slug = {}
for host in set(list(PLANETS.keys()) + list(STELLAR.keys())):
    host_by_slug[to_slug(host)] = host

out = {"check_B_missing_planet_reports": [], "check_C_disk_overlap": [],
       "check_A_untracked_citations": {}, "derived_recompute": [],
       "block_parity": {}}

# ---- Check B: roster coverage ----
for host, planets in PLANETS.items():
    if not isinstance(planets, list):
        continue
    hs = to_slug(host)
    if hs not in REPORTS:
        continue  # not in Phase 3 scope
    for p in planets:
        nm = p.get("pl_name")
        if not nm:
            continue
        letter = nm.split()[-1].lower()
        cand = f"{hs}-{letter}"
        if cand not in REPORTS and cand != hs:
            out["check_B_missing_planet_reports"].append(
                {"host": host, "planet": nm, "expected_report": f"{cand}.md"})

# ---- Check C: disk belt overlap ----
for slug, md in REPORTS.items():
    txt = open(md, encoding="utf-8").read()
    belts = {}
    for m in re.finditer(r'`disk_(\w+?)_(inner|outer)_radius_au`\s*\|\s*([\d.]+)', txt):
        belts.setdefault(m.group(1), {})[m.group(2)] = float(m.group(3))
    full = [(b, v["inner"], v["outer"]) for b, v in belts.items() if "inner" in v and "outer" in v]
    full.sort(key=lambda x: x[1])
    for i in range(len(full) - 1):
        b1, i1, o1 = full[i]
        b2, i2, o2 = full[i + 1]
        if o1 > i2:
            out["check_C_disk_overlap"].append(
                {"report": slug, "belt_inner": b1, "belt_outer": b2,
                 "overlap_au": round(o1 - i2, 2), "detail": f"{b1}({i1}-{o1}) overlaps {b2}({i2}-{o2})"})

# ---- Check A: Bibliography/Decisions citations absent from bib + cache ----
for slug, md in REPORTS.items():
    txt = open(md, encoding="utf-8").read()
    codes = set(bibcode_re.findall(txt))
    axs = set(arxiv_re.findall(txt))
    bibtxt = ""
    for c in (slug, re.sub(r'-[a-z]$', '', slug)):
        p = f"docs/phase3/_bib/{c}.yaml"
        if os.path.exists(p):
            bibtxt += open(p, encoding="utf-8").read()
    mc = sorted(c for c in codes if c not in bibtxt)
    ma = sorted(a for a in axs if a not in bibtxt and a not in CACHE)
    if mc or ma:
        out["check_A_untracked_citations"][slug] = {
            "untracked_bibcodes": mc, "untracked_arxiv": ma,
            "n": len(mc) + len(ma)}

# ---- Derived recompute: T_eq(A=0) and S vs report ----
def report_value(txt, field, qualifier=None):
    for line in txt.splitlines():
        if f"`{field}`" in line and (qualifier is None or qualifier in line):
            m = re.search(r'\|\s*`%s`[^|]*\|\s*~?([\d.]+)' % re.escape(field), line)
            if m:
                return float(m.group(1))
    return None

for slug, md in REPORTS.items():
    hs = re.sub(r'-[a-z]$', '', slug)
    if hs == slug:
        continue  # stellar report, no a
    host = host_by_slug.get(hs)
    if not host:
        continue
    L = recommended(STELLAR.get(host, {}).get("luminosity_measurements"), "luminosity_lsun")
    letter = slug[len(hs) + 1:]
    a = None
    for p in PLANETS.get(host, []):
        if p.get("pl_name", "").split()[-1].lower() == letter:
            a = recommended(p.get("orbital"), "semi_major_axis_au")
            break
    if not (L and a):
        continue
    teq0 = 278.3 * (L ** 0.25) / math.sqrt(a)
    s = L / (a * a)
    txt = open(md, encoding="utf-8").read()
    rep_teq = report_value(txt, "equilibrium_temp_k", "A=0")
    rep_s = report_value(txt, "insolation_s_earth")
    rec = {"report": slug, "L_lsun": L, "a_au": a,
           "recomputed_teq_A0_k": round(teq0, 1), "recomputed_S_searth": round(s, 3)}
    flag = False
    if rep_teq:
        rec["report_teq_A0_k"] = rep_teq
        if abs(rep_teq - teq0) / teq0 > 0.20:
            rec["TEQ_MISMATCH"] = True; flag = True
    if rep_s:
        rec["report_S_searth"] = rep_s
        if abs(rep_s - s) / s > 0.25:
            rec["S_MISMATCH"] = True; flag = True
    if flag:
        out["derived_recompute"].append(rec)

# ---- Block parity ----
for slug in REPORTS:
    try:
        r = subprocess.run(["python3", "scripts/phase3/check_block_parity.py", slug],
                           capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            out["block_parity"][slug] = (r.stdout + r.stderr).strip()[-300:]
    except Exception as e:
        out["block_parity"][slug] = f"error: {e}"

with open("phase3/_audit/_scratch/static-flags-2026-06-03.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("=== Phase 0 static-check summary ===")
print(f"Reports scanned: {len(REPORTS)}")
print(f"B  missing planet reports : {len(out['check_B_missing_planet_reports'])}")
for x in out["check_B_missing_planet_reports"]:
    print(f"     {x['host']:20s} -> {x['expected_report']}")
print(f"C  disk-belt overlaps     : {len(out['check_C_disk_overlap'])}")
for x in out["check_C_disk_overlap"]:
    print(f"     {x['report']}: {x['detail']}")
print(f"A  reports w/ untracked cite: {len(out['check_A_untracked_citations'])} (detail in JSON)")
print(f"   top offenders: " + ", ".join(
    f"{k}({v['n']})" for k, v in sorted(out['check_A_untracked_citations'].items(),
                                        key=lambda kv: -kv[1]['n'])[:6]))
print(f"D  derived-value mismatches: {len(out['derived_recompute'])}")
for x in out["derived_recompute"]:
    print(f"     {x['report']}: {', '.join(k for k in x if k.endswith('MISMATCH'))} "
          f"(teq rep={x.get('report_teq_A0_k')} calc={x['recomputed_teq_A0_k']}; "
          f"S rep={x.get('report_S_searth')} calc={x['recomputed_S_searth']})")
print(f"P  block-parity failures   : {len(out['block_parity'])}")
for k, v in out["block_parity"].items():
    print(f"     {k}: {v[:120]}")
