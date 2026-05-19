#!/usr/bin/env python3
# NASA Archive ps 테이블(per-paper rows)에서 default_flag=1 행을 가져와 paper-attributed values 생성
"""
Phase 1 큐레이션용 helper. fetch_planets.py 는 pscomppars (composite) 사용 —
정책 [[feedback-planet-curation]] 위반. 이 스크립트는 ps 테이블에서 NASA가
지정한 default 논문 1편의 값과 bibcode 를 그대로 가져온다.

Usage:
    python3 scripts/pipeline/fetch_planets_ps.py              # 전체 호스트
    python3 scripts/pipeline/fetch_planets_ps.py GJ 179       # 단일 호스트
    python3 scripts/pipeline/fetch_planets_ps.py GJ 179 GJ 581

출력: db/planets_ps_default.json
"""
import json, os, re, sys, urllib.parse, urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TAP  = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

PL_REFNAME_BIBCODE = re.compile(r"abs/([0-9A-Za-z\.\&\+\-%]+)/abstract")
PL_REFNAME_LABEL   = re.compile(r"refstr=([A-Za-z_0-9]+)")


def archive_query(q, timeout=120):
    data = urllib.parse.urlencode({"query": q, "format": "json"}).encode()
    req = urllib.request.Request(TAP, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def parse_refname(refname):
    if not refname:
        return None, None
    bm = PL_REFNAME_BIBCODE.search(refname)
    lm = PL_REFNAME_LABEL.search(refname)
    bibcode = urllib.parse.unquote(bm.group(1)) if bm else None
    label = None
    if lm:
        raw = lm.group(1)
        # WANG_ET_AL__2024  →  Wang et al. 2024
        # PINEDA-AND-HALLINAN_2018 → Pineda And Hallinan 2018
        # 패턴: 1) _ET_AL_+ 처리, 2) 나머지 underscore → space, 3) 단어별 title case
        s = re.sub(r"_+ET_+AL_+", " et al. ", raw)
        s = s.replace("_", " ").strip()
        # 마지막에 et al. 뒤 연도가 ".2024" 같이 붙어 있을 수 있음 → 정리
        s = re.sub(r"\s+", " ", s)
        # 토큰별 처리: 영문 단어는 title case (하이픈도 분리해서), 연도는 그대로
        out = []
        for tok in s.split(" "):
            if not tok:
                continue
            if tok.lower() in ("et", "al.", "and", "the"):
                out.append(tok.lower())
            elif tok.isdigit():
                out.append(tok)
            else:
                # 하이픈 포함 가능
                out.append("-".join(p.capitalize() for p in tok.split("-")))
        label = " ".join(out)
    return bibcode, label


def fetch_hosts(hosts):
    q = f"""
SELECT
  hostname, pl_name, default_flag, soltype,
  pl_refname,
  pl_orbper, pl_orbpererr1, pl_orbpererr2,
  pl_orbsmax, pl_orbsmaxerr1, pl_orbsmaxerr2,
  pl_orbeccen,
  pl_orbincl, pl_orbinclerr1,
  pl_orblper,
  pl_orbtper, pl_orbtpererr1,
  pl_tranmid, pl_tranmiderr1,
  pl_bmasse, pl_bmasseerr1, pl_bmasseerr2, pl_bmassprov,
  pl_rade, pl_radeerr1, pl_radeerr2,
  discoverymethod, pl_pubdate,
  st_refname, st_mass, st_masserr1, st_rad, st_raderr1
FROM ps
WHERE hostname in ({','.join("'" + h.replace("'", "''") + "'" for h in hosts)})
"""
    print(f"NASA Archive ps 쿼리: {len(hosts)} 호스트 …")
    rows = archive_query(q, timeout=180)
    print(f"  {len(rows)} rows 반환")
    return rows


def select_defaults(rows):
    """planet 별 default_flag=1 row 1개씩, host별 dict 으로 묶기."""
    by_planet = {}
    for r in rows:
        if r.get("default_flag") != 1:
            continue
        pname = r["pl_name"]
        if pname in by_planet:
            continue
        by_planet[pname] = r

    by_host = {}
    for pname, r in by_planet.items():
        host = r["hostname"]
        by_host.setdefault(host, []).append(r)
    return by_host


def shape_entry(r):
    """ps row → 큐레이션-친화적 dict (단위 그대로, mass_type 정규화)."""
    pl_bib, pl_lab = parse_refname(r.get("pl_refname"))
    st_bib, st_lab = parse_refname(r.get("st_refname"))
    mp = r.get("pl_bmassprov")
    mass_type = {"Mass": "true mass", "Msini": "Msini",
                 "Msin(i)/sin(i)": "Msini",
                 "Mass*sin(i)/sin(i)": "Msini"}.get(mp, mp)
    return {
        "pl_name":              r["pl_name"],
        "period_days":          r.get("pl_orbper"),
        "period_err_days":      r.get("pl_orbpererr1"),
        "semi_major_axis_au":   r.get("pl_orbsmax"),
        "semi_major_axis_err_au": r.get("pl_orbsmaxerr1"),
        "eccentricity":         r.get("pl_orbeccen"),
        "inclination_deg":      r.get("pl_orbincl"),
        "inclination_err_deg":  r.get("pl_orbinclerr1"),
        "omega_deg":            r.get("pl_orblper"),
        "tperi_bjd":            r.get("pl_orbtper"),
        "tperi_err_bjd":        r.get("pl_orbtpererr1"),
        "tranmid_bjd":          r.get("pl_tranmid"),
        "tranmid_err_bjd":      r.get("pl_tranmiderr1"),
        "mass_mearth":          r.get("pl_bmasse"),
        "mass_err_mearth":      r.get("pl_bmasseerr1"),
        "mass_type":            mass_type,
        "radius_rearth":        r.get("pl_rade"),
        "radius_err_rearth":    r.get("pl_radeerr1"),
        "discoverymethod":      r.get("discoverymethod"),
        "pubdate":              r.get("pl_pubdate"),
        # source attribution
        "pl_bibcode":           pl_bib,
        "pl_reference":         pl_lab,
        # host stellar params from same row.
        # 정책: 출처 없는 값(st_refname=null)은 Phase 1 에서 사용 불가 → null 처리.
        # mass / radius 각각 독립적으로 bibcode 관리: fallback 시 다른 paper 가 들어올 수 있음.
        "host_mass_msun":          r.get("st_mass") if st_bib else None,
        "host_mass_err_msun":      r.get("st_masserr1") if st_bib else None,
        "host_mass_bibcode":       st_bib if r.get("st_mass") is not None else None,
        "host_mass_reference":     st_lab if r.get("st_mass") is not None else None,
        "host_radius_rsun":        r.get("st_rad") if st_bib else None,
        "host_radius_err_rsun":    r.get("st_raderr1") if st_bib else None,
        "host_radius_bibcode":     st_bib if r.get("st_rad") is not None else None,
        "host_radius_reference":   st_lab if r.get("st_rad") is not None else None,
    }


def fetch_host_stellar_fallback(host_names):
    """ps default 행에서 host_mass/host_radius 가 null 인 호스트용 fallback.
    같은 호스트의 다른(non-default) ps 행 중 st_mass + st_refname 이 모두 있는 row 를
    fractional uncertainty 가 작은 순으로 선택."""
    if not host_names:
        return {}
    where = " in (" + ",".join("'" + h.replace("'", "''") + "'" for h in host_names) + ")"
    q = f"""
SELECT hostname, st_refname, st_mass, st_masserr1, st_rad, st_raderr1
FROM ps
WHERE hostname {where}
  AND st_refname IS NOT NULL
  AND (st_mass IS NOT NULL OR st_rad IS NOT NULL)
"""
    rows = archive_query(q, timeout=120)
    by_host = {}
    for r in rows:
        h = r["hostname"]
        by_host.setdefault(h, []).append(r)

    def best(rows, val_key, err_key):
        def frac(r):
            v = r.get(val_key)
            e = r.get(err_key)
            if v is None or e is None or v == 0:
                return (float("inf"), 0)
            return (abs(e / v), 0)
        cands = [r for r in rows if r.get(val_key) is not None]
        if not cands:
            return None
        cands.sort(key=frac)
        return cands[0]

    out = {}
    for h, rs in by_host.items():
        mass_row = best(rs, "st_mass", "st_masserr1")
        rad_row  = best(rs, "st_rad",  "st_raderr1")
        if mass_row or rad_row:
            mb, mlb = (parse_refname(mass_row["st_refname"]) if mass_row else (None, None))
            rb, rlb = (parse_refname(rad_row["st_refname"]) if rad_row else (None, None))
            out[h] = {
                "host_mass_msun":       (mass_row or {}).get("st_mass"),
                "host_mass_err_msun":   (mass_row or {}).get("st_masserr1"),
                "host_mass_bibcode":    mb,
                "host_mass_reference":  mlb,
                "host_radius_rsun":     (rad_row or {}).get("st_rad"),
                "host_radius_err_rsun": (rad_row or {}).get("st_raderr1"),
                "host_radius_bibcode":  rb,
                "host_radius_reference":rlb,
            }
    return out


def main():
    args = sys.argv[1:]
    if args:
        # CLI 인자는 공백 포함될 수 있어 join 처리
        line = " ".join(args)
        hosts = [h.strip() for h in line.split(",")] if "," in line else [line]
    else:
        # 전체 호스트는 planets_raw.json 키 사용
        with open(f"{BASE}/db/planets_raw.json") as f:
            hosts = sorted(json.load(f).keys())

    rows = fetch_hosts(hosts)
    by_host = select_defaults(rows)
    result = {host: [shape_entry(r) for r in sorted(plist, key=lambda x: x["pl_name"])]
              for host, plist in by_host.items()}

    # default 행에 host stellar 가 비어 있는 호스트는 fallback 쿼리
    needs_fallback = []
    for h, plist in result.items():
        first = plist[0] if plist else {}
        if first.get("host_mass_msun") is None or first.get("host_radius_rsun") is None:
            needs_fallback.append(h)
    if needs_fallback:
        print(f"  host fallback 쿼리: {len(needs_fallback)} 호스트")
        fb = fetch_host_stellar_fallback(needs_fallback)
        for h, picks in fb.items():
            # 첫 행성에 fallback 값 병합 (없는 필드만)
            first = result[h][0]
            if first.get("host_mass_msun") is None and picks.get("host_mass_msun") is not None:
                first["host_mass_msun"]      = picks["host_mass_msun"]
                first["host_mass_err_msun"]  = picks["host_mass_err_msun"]
                first["host_mass_bibcode"]   = picks["host_mass_bibcode"]
                first["host_mass_reference"] = picks["host_mass_reference"]
            if first.get("host_radius_rsun") is None and picks.get("host_radius_rsun") is not None:
                first["host_radius_rsun"]      = picks["host_radius_rsun"]
                first["host_radius_err_rsun"]  = picks["host_radius_err_rsun"]
                first["host_radius_bibcode"]   = picks["host_radius_bibcode"]
                first["host_radius_reference"] = picks["host_radius_reference"]

    out = f"{BASE}/db/planets_ps_default.json"
    with open(out, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=str)
    print(f"저장: {out}")
    print(f"  hosts: {len(result)}, planets: {sum(len(v) for v in result.values())}")


if __name__ == "__main__":
    main()
