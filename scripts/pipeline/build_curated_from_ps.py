#!/usr/bin/env python3
# Phase 1 큐레이션: db/planets_ps_default.json → planets_curated + stellar_props_curated 채우기
"""
ps 테이블 default_flag=1 row 기반으로 paper-attributed Phase 1 entry 작성.

DOI는 Crossref bibliographic search 로 best-effort 해석. 못 찾으면 null 유지.
α Cen A/B, Barnard's star 같은 기존 high-quality 큐레이션은 보존 (덮어쓰기 금지).

Usage:
    python3 scripts/pipeline/build_curated_from_ps.py            # 전체 호스트
    python3 scripts/pipeline/build_curated_from_ps.py --hosts "GJ 179,GJ 581,GJ 1132"
    python3 scripts/pipeline/build_curated_from_ps.py --dry-run  # 출력만, 파일 미수정
"""
import argparse, json, os, re, sys, time, urllib.parse, urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB   = f"{BASE}/db"
RETRIEVAL_DATE = "2026-05-19"

# 기존 high-quality 큐레이션 - 절대 덮어쓰지 않음
PRESERVED_HOSTS = {"Alpha Centauri A", "Alpha Centauri B", "Barnard's star"}

# bibcode journal abbreviation → Crossref container-title 검색어
JOURNAL_NAMES = {
    "ApJ":   "Astrophysical Journal",
    "ApJL":  "Astrophysical Journal Letters",
    "ApJS":  "Astrophysical Journal Supplement",
    "A&A":   "Astronomy and Astrophysics",
    "AJ":    "Astronomical Journal",
    "MNRAS": "Monthly Notices of the Royal Astronomical Society",
    "Natur": "Nature",
    "Sci":   "Science",
    "NatAs": "Nature Astronomy",
    "PASP":  "Publications of the Astronomical Society of the Pacific",
    "RAA":   "Research in Astronomy and Astrophysics",
}

BIBCODE_RE = re.compile(
    r"^(?P<year>\d{4})"
    r"(?P<journal>[A-Za-z&\.\+]+?)\.*"
    r"\s*(?P<vol>\d+|\.+)"
    r"(?P<sect>[A-Z\.])"
    r"(?P<page>[0-9\.]+)"
    r"(?P<init>[A-Z])$"
)


def parse_bibcode(bib):
    """ADS bibcode → (year, journal, volume, page_or_id, first_author_initial)."""
    if not bib:
        return None
    s = bib.strip()
    if len(s) < 19:
        return None
    year = s[0:4]
    journal = s[4:9].rstrip(".")
    vol = s[9:13].strip(".")
    sect = s[13]
    page = s[14:18].strip(".")
    init = s[18] if len(s) > 18 else None
    return {"year": year, "journal": journal, "volume": vol,
            "section": sect, "page": page, "first_author_init": init,
            "is_arxiv": journal.lower().startswith("arxiv"),
            "is_letter": sect == "L"}


def crossref_lookup_doi(bib, author_label, timeout=15):
    """Crossref bibliographic search 로 DOI 후보 검색. 검증 실패 시 None.

    A&A/ApJL 형식: article-id = section + page (예: "A112", "L8")
    그 외 (ApJ/AJ/MNRAS): page 그대로 (예: "1467")
    매칭 기준: container + year + volume + (page or article-id) + 첫 저자 initial.
    """
    if not bib:
        return None
    parsed = parse_bibcode(bib)
    if not parsed:
        return None
    if parsed["is_arxiv"]:
        return None
    container = JOURNAL_NAMES.get(parsed["journal"])
    if not container:
        return None

    # 목표 페이지/아티클 ID
    target_id = (parsed["section"] + parsed["page"]) if parsed["section"] in ("A", "L") else parsed["page"]

    params = {
        "query.container-title": container,
        "query.bibliographic": f"{parsed['volume']} {target_id}",
        "filter": f"from-pub-date:{parsed['year']}-01-01,until-pub-date:{parsed['year']}-12-31",
        "rows": "10",
    }
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "NearStars/0.1 (research; vannadin00@gmail.com)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.load(r)
    except Exception:
        return None

    init = parsed["first_author_init"]
    for item in data.get("message", {}).get("items", []):
        vol = str(item.get("volume", "")).strip()
        if vol != parsed["volume"]:
            continue
        # 페이지/아티클 ID 매칭
        page = str(item.get("page", "")).strip()
        article = str(item.get("article-number", "")).strip()
        candidates = []
        if page:
            candidates.append(page.split("-")[0])
        if article:
            candidates.append(article)
        if target_id not in candidates and not any(c.startswith(target_id) for c in candidates):
            continue
        # 첫 저자 initial 매칭. Crossref family 는 형태가 일관되지 않음 —
        #   "Howard" (마지막 단어)
        #   "W. Howard" (initial 포함)
        #   "von Stauffenberg" (소문자 particle 포함; ADS bibcode 는 'V' 부여)
        # 첫 단어 첫글자, 마지막 단어 첫글자, 전체 string 첫글자 중 init 매칭이 있으면 OK.
        authors = item.get("author", [])
        if init and authors:
            family = (authors[0].get("family") or "").strip()
            if family:
                tokens = family.split()
                cands = {family[0].upper()}
                if tokens:
                    cands.add(tokens[0][0].upper())
                    cands.add(tokens[-1][0].upper())
                # initial-prefix 토큰 ("W.", "J.-P.") 은 제거 후 다시 시도
                stripped = re.sub(r"^([A-Z]\.[-\s]*)+", "", family).strip()
                if stripped:
                    cands.add(stripped[0].upper())
                if init not in cands:
                    continue
        return item.get("DOI")
    return None


def build_orbital(pl, doi):
    """ps row → curated 'orbital' dict."""
    orb = {}
    # 단순 매핑
    if pl.get("semi_major_axis_au") is not None:
        orb["semi_major_axis_au"] = pl["semi_major_axis_au"]
    if pl.get("eccentricity") is not None:
        orb["eccentricity"] = pl["eccentricity"]
    if pl.get("inclination_deg") is not None:
        orb["inclination_deg"] = pl["inclination_deg"]
    orb["longitude_of_ascending_node_deg"] = None  # RV/transit 데이터로는 미결정
    if pl.get("omega_deg") is not None:
        orb["argument_of_periapsis_deg"] = pl["omega_deg"]
    # tperi → epoch_jd + mean_anomaly_at_epoch=0 변환
    if pl.get("tperi_bjd") is not None:
        orb["epoch_jd"] = pl["tperi_bjd"]
        orb["mean_anomaly_at_epoch_deg"] = 0.0
    elif pl.get("tranmid_bjd") is not None:
        # 트랜짓-only: tranmid 시점에서 mean_anomaly 계산은 omega/ecc 필요. ecc<<1 가정 시
        # M ≈ 90° - omega (primary transit at f=90°-omega 위치). omega 없으면 null.
        if pl.get("omega_deg") is not None:
            orb["epoch_jd"] = pl["tranmid_bjd"]
            # M = E - e sin E; for circular orbit, M = 90° - omega at primary transit
            # 일반 ecc일 땐 정확하진 않으나 ecc<0.1 행성에선 충분
            f_transit = 90.0 - pl["omega_deg"]  # true anomaly at mid-transit
            # 정확한 M 계산은 ecc 필요 - Phase 1 에서는 ecc<0.1 가정으로 M≈f
            orb["mean_anomaly_at_epoch_deg"] = f_transit % 360.0
        else:
            orb["epoch_jd"] = None
            orb["mean_anomaly_at_epoch_deg"] = None
    else:
        orb["epoch_jd"] = None
        orb["mean_anomaly_at_epoch_deg"] = None

    orb["source"]    = pl.get("pl_reference")
    orb["bibcode"]   = pl.get("pl_bibcode")
    orb["doi"]       = doi
    return orb


def build_physical(pl, doi):
    """ps row → curated 'physical' dict."""
    phy = {}
    mtype = pl.get("mass_type")
    if pl.get("mass_mearth") is not None:
        # Msini vs true mass 구분
        if mtype == "true mass":
            phy["true_mass_mearth"] = pl["mass_mearth"]
        else:
            phy["mass_mearth"] = pl["mass_mearth"]
        if pl.get("mass_err_mearth") is not None:
            phy["uncertainty_mearth"] = pl["mass_err_mearth"]
        phy["mass_type"] = mtype
    if pl.get("radius_rearth") is not None:
        phy["radius_rearth"] = pl["radius_rearth"]
        if pl.get("radius_err_rearth") is not None:
            phy["uncertainty_rearth"] = pl["radius_err_rearth"]
    phy["source"]    = pl.get("pl_reference")
    phy["bibcode"]   = pl.get("pl_bibcode")
    phy["doi"]       = doi
    return phy


def build_host_mass_radius(host_planets, doi_cache):
    """host_*_msun/rsun 값 중 가장 정밀한 1개씩 선택해서 measurement 객체 생성.

    같은 host 의 여러 planet 이 같은 bibcode 를 공유하면 1개 paper. 다르면
    가장 작은 uncertainty 가진 paper 선택. mass 와 radius 는 독립적인 bibcode 보유 가능.
    """
    mass_candidates = []
    rad_candidates  = []
    for p in host_planets:
        m_bib = p.get("host_mass_bibcode")
        r_bib = p.get("host_radius_bibcode")
        if p.get("host_mass_msun") is not None and m_bib:
            mass_candidates.append((p["host_mass_msun"], p.get("host_mass_err_msun"),
                                    m_bib, p.get("host_mass_reference")))
        if p.get("host_radius_rsun") is not None and r_bib:
            rad_candidates.append((p["host_radius_rsun"], p.get("host_radius_err_rsun"),
                                   r_bib, p.get("host_radius_reference")))

    def pick_best(cands):
        if not cands:
            return None
        # 가장 작은 fractional uncertainty 우선; null 은 후순위
        def key(t):
            val, err, _, _ = t
            if err is None or val in (0, None):
                return float("inf")
            return abs(err / val)
        return sorted(cands, key=key)[0]

    out = {"mass": None, "radius": None}
    best_m = pick_best(mass_candidates)
    if best_m:
        val, err, bib, ref = best_m
        doi = doi_cache.get(bib)
        out["mass"] = {
            "value_msun": val,
            "uncertainty_msun": err,
            "method": "spectroscopic_calibration",  # ps default 는 paper 마다 다르지만
            # method 식별이 어렵다. 보수적으로 가장 흔한 카테고리 사용.
            "reference": ref, "bibcode": bib, "doi": doi,
            "recommended": True,
        }
    best_r = pick_best(rad_candidates)
    if best_r:
        val, err, bib, ref = best_r
        doi = doi_cache.get(bib)
        out["radius"] = {
            "value_rsun": val,
            "uncertainty_rsun": err,
            "method": "evolutionary_model",
            "reference": ref, "bibcode": bib, "doi": doi,
            "recommended": True,
        }
    return out


def load_existing(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hosts", help="comma-separated host names; default = all")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--input", default=f"{DB}/planets_ps_default.json")
    ap.add_argument("--no-doi", action="store_true",
                    help="skip Crossref DOI lookup (faster, leaves doi=null)")
    args = ap.parse_args()

    with open(args.input) as f:
        ps_data = json.load(f)

    host_filter = None
    if args.hosts:
        host_filter = {h.strip() for h in args.hosts.split(",")}

    planets_curated  = load_existing(f"{DB}/planets_curated.json")
    stellar_curated  = load_existing(f"{DB}/stellar_props_curated.json")

    doi_cache = {}  # bibcode → doi (or None if lookup failed)

    new_planet_hosts = 0
    new_planet_entries = 0
    new_stellar_entries = 0

    for host, plist in ps_data.items():
        if host_filter and host not in host_filter:
            continue

        # ── 행성 curated ──
        planet_entries = []
        for p in plist:
            bib = p.get("pl_bibcode")
            ref = p.get("pl_reference")
            if bib and bib not in doi_cache:
                doi_cache[bib] = None if args.no_doi else crossref_lookup_doi(bib, ref)
                time.sleep(0.05)  # be polite to Crossref
            doi = doi_cache.get(bib)
            planet_entries.append({
                "pl_name":  p["pl_name"],
                "orbital":  build_orbital(p, doi),
                "physical": build_physical(p, doi),
            })

        if planet_entries:
            if host in planets_curated:
                print(f"  [SKIP] {host}: planets_curated 기존 entry 보존")
            else:
                planets_curated[host] = planet_entries
                new_planet_hosts += 1
                new_planet_entries += len(planet_entries)

        # ── 호스트 stellar curated ──
        if host in PRESERVED_HOSTS:
            print(f"  [PRESERVE] {host}: stellar_props_curated 기존 high-quality 보존")
            continue
        if host in stellar_curated:
            existing = stellar_curated[host]
            if existing.get("mass_measurements") or existing.get("radius_measurements"):
                # 이미 큐레이션 있으면 보존
                print(f"  [SKIP] {host}: stellar_props_curated 기존 entry 보존")
                continue

        host_pkg = build_host_mass_radius(plist, doi_cache)
        m = host_pkg["mass"]
        r = host_pkg["radius"]
        if not m and not r:
            continue
        entry = stellar_curated.get(host, {})
        if m:
            entry.setdefault("mass_measurements", []).append(m)
        if r:
            entry.setdefault("radius_measurements", []).append(r)
        stellar_curated[host] = entry
        new_stellar_entries += 1

    print(f"\n새 행성 호스트: {new_planet_hosts}, 행성 entry: {new_planet_entries}")
    print(f"새 stellar host: {new_stellar_entries}")
    print(f"DOI cache: {sum(1 for v in doi_cache.values() if v)} resolved / {len(doi_cache)} bibcodes")

    if args.dry_run:
        print("[DRY RUN] 파일 미수정")
        return

    with open(f"{DB}/planets_curated.json", "w") as f:
        json.dump(planets_curated, f, indent=2, ensure_ascii=False)
    with open(f"{DB}/stellar_props_curated.json", "w") as f:
        json.dump(stellar_curated, f, indent=2, ensure_ascii=False)
    print(f"저장: {DB}/planets_curated.json, {DB}/stellar_props_curated.json")


if __name__ == "__main__":
    main()
