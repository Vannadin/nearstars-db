# Phase 3 큐레이션용 paper bibliography 빌더 — ADS + arXiv 검색을 합쳐 YAML로 출력
"""Build Phase 3 bibliography for a single planet.

Sources (in priority):
  1. ADS API — comprehensive, requires ADS_API_TOKEN env var.
     `object:` query is most precise for named exoplanets.
  2. arXiv API — free, no auth. `abs:` + `ti:` combined.

Output: docs/phase3/_bib/<slug>.yaml — per-paper records with arxiv_id,
ADS bibcode, title, authors, abstract, year, doi, plus `status: pending`
and `category: null` for the curator (Claude) to fill in during triage.

Usage:
  python3 scripts/phase3/build_bibliography.py "TRAPPIST-1 d"
  python3 scripts/phase3/build_bibliography.py "TRAPPIST-1 d" --max 200
  ADS_API_TOKEN=... python3 scripts/phase3/build_bibliography.py "Proxima Cen b"

The script is idempotent at the per-paper level: re-running merges new
papers without overwriting existing status/category annotations.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import yaml


BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BIB_DIR = os.path.join(BASE, "docs", "phase3", "_bib")

ADS_API = "https://api.adsabs.harvard.edu/v1/search/query"
ARXIV_API = "http://export.arxiv.org/api/query"

# arXiv API etiquette: at least 3 seconds between requests.
ARXIV_SLEEP_S = 3.0


def slugify(name: str) -> str:
    """'TRAPPIST-1 d' → 'trappist-1d'. Conservative — strip non-alphanumeric, lowercase."""
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s


def http_get_json(url: str, headers: dict | None = None, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return __import__("json").loads(r.read().decode())


def http_get_text(url: str, headers: dict | None = None, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode()


# ── ADS ─────────────────────────────────────────────────────────────────────

def ads_search(planet_name: str, token: str, max_results: int) -> list[dict]:
    """ADS API 로 행성명 검색. 제목/abstract 우선, 부족하면 본문 검색 보충.

    `object:` 는 SIMBAD-resolved 별 카탈로그명만 받아서 행성 designation
    ("TRAPPIST-1 d" 등) 에는 Solr SyntaxError. 대신 abs+title 정밀 검색을
    1차로, 결과 부족 (<15) 시 full-text 검색으로 보충.
    """
    fields = "bibcode,title,author,abstract,year,pubdate,doi,identifier"

    def _query(q: str) -> list[dict]:
        params = {
            "q": q,
            "fl": fields,
            "rows": min(max_results, 200),
            "sort": "date desc",
        }
        url = f"{ADS_API}?{urllib.parse.urlencode(params)}"
        resp = http_get_json(url, headers={"Authorization": f"Bearer {token}"})
        return resp.get("response", {}).get("docs", []) or []

    safe = planet_name.replace('"', '\\"')
    docs = _query(f'abs:"{safe}" OR title:"{safe}"')
    if len(docs) < 15:
        more = _query(f'full:"{safe}"')
        seen = {d.get("bibcode") for d in docs}
        for d in more:
            if d.get("bibcode") not in seen:
                docs.append(d)

    return docs[:max_results]


def ads_to_paper(doc: dict) -> dict:
    """ADS doc → Phase 3 paper record. arXiv id 추출 포함."""
    arxiv_id = None
    for ident in doc.get("identifier", []) or []:
        # 형식: "arXiv:2301.12345" 또는 "2301.12345" 또는 "astro-ph/0501123"
        if isinstance(ident, str) and ident.lower().startswith("arxiv:"):
            arxiv_id = ident.split(":", 1)[1].strip()
            break

    doi = None
    doi_list = doc.get("doi") or []
    if isinstance(doi_list, list) and doi_list:
        doi = doi_list[0]
    elif isinstance(doi_list, str):
        doi = doi_list

    return {
        "arxiv_id":    arxiv_id,
        "ads_bibcode": doc.get("bibcode"),
        "title":       (doc.get("title") or [None])[0],
        "authors":     doc.get("author") or [],
        "year":        doc.get("year"),
        "pubdate":     doc.get("pubdate"),
        "doi":         doi,
        "abstract":    doc.get("abstract"),
    }


# ── arXiv ───────────────────────────────────────────────────────────────────

_ATOM_NS = {"atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom"}


def arxiv_search(planet_name: str, max_results: int) -> list[dict]:
    """arXiv API 로 행성명 검색. abs: + ti: 양쪽."""
    # 따옴표로 묶어 phrase 검색
    safe = planet_name.replace('"', '\\"')
    query = f'abs:"{safe}" OR ti:"{safe}"'
    params = {
        "search_query": query,
        "start": 0,
        "max_results": min(max_results, 300),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    xml_text = http_get_text(url)
    root = ET.fromstring(xml_text)

    papers = []
    for entry in root.findall("atom:entry", _ATOM_NS):
        eid = (entry.findtext("atom:id", "", _ATOM_NS) or "").strip()
        # eid 형식: http://arxiv.org/abs/2301.12345v1
        m = re.search(r"arxiv\.org/abs/(.+?)(?:v\d+)?$", eid)
        arxiv_id = m.group(1) if m else None

        authors = [a.findtext("atom:name", "", _ATOM_NS).strip()
                   for a in entry.findall("atom:author", _ATOM_NS)]
        title = (entry.findtext("atom:title", "", _ATOM_NS) or "").strip()
        title = re.sub(r"\s+", " ", title)
        abstract = (entry.findtext("atom:summary", "", _ATOM_NS) or "").strip()
        abstract = re.sub(r"\s+", " ", abstract)
        published = (entry.findtext("atom:published", "", _ATOM_NS) or "").strip()
        # DOI element: arxiv:doi
        doi_elem = entry.find("arxiv:doi", _ATOM_NS)
        doi = doi_elem.text.strip() if doi_elem is not None else None

        papers.append({
            "arxiv_id":    arxiv_id,
            "ads_bibcode": None,
            "title":       title,
            "authors":     authors,
            "year":        published[:4] if published else None,
            "pubdate":     published[:10] if published else None,
            "doi":         doi,
            "abstract":    abstract,
        })
    return papers


# ── merge & persist ─────────────────────────────────────────────────────────

def merge_papers(existing: list[dict], new: list[dict]) -> list[dict]:
    """기존 paper 리스트에 새 검색 결과 병합.
    기존 entry 의 status/category/skip_reason/fetch_error 는 보존.
    중복 식별: arxiv_id > doi > ads_bibcode > 제목."""
    def key(p):
        return p.get("arxiv_id") or p.get("doi") or p.get("ads_bibcode") or (p.get("title") or "").lower()

    by_key = {key(p): p for p in existing}
    for np_ in new:
        k = key(np_)
        if k in by_key:
            # 기존 entry 의 ADS 보충 (예: arXiv 검색이 ads_bibcode 채워줌)
            ex = by_key[k]
            for field in ("ads_bibcode", "doi", "abstract", "authors", "title", "year", "pubdate"):
                if not ex.get(field) and np_.get(field):
                    ex[field] = np_[field]
        else:
            np_.setdefault("status", "pending")
            np_.setdefault("category", None)
            np_.setdefault("skip_reason", None)
            np_.setdefault("fetch_error", None)
            by_key[k] = np_
    return list(by_key.values())


def load_existing(path: str) -> dict | None:
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def save_bibliography(path: str, data: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True, width=120)


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Build Phase 3 bibliography for a planet.")
    parser.add_argument("planet", help='Planet name, e.g. "TRAPPIST-1 d"')
    parser.add_argument("--max", type=int, default=150,
                        help="Max papers per source (default 150)")
    parser.add_argument("--no-arxiv", action="store_true", help="Skip arXiv API")
    parser.add_argument("--no-ads", action="store_true",
                        help="Skip ADS API (always skipped if ADS_API_TOKEN not set)")
    args = parser.parse_args()

    slug = slugify(args.planet)
    out_path = os.path.join(BIB_DIR, f"{slug}.yaml")
    existing = load_existing(out_path)

    print(f"[Phase 3] Building bibliography for: {args.planet}  → {out_path}")

    papers = (existing or {}).get("papers", []) or []
    n_before = len(papers)
    sources_used = (existing or {}).get("sources", {}) or {}

    # ADS
    token = os.environ.get("ADS_API_TOKEN")
    if not args.no_ads and token:
        print(f"  ADS: querying (abs+title, full: fallback, max {args.max})…")
        try:
            ads_docs = ads_search(args.planet, token, args.max)
            ads_papers = [ads_to_paper(d) for d in ads_docs]
            papers = merge_papers(papers, ads_papers)
            sources_used["ads"] = f"queried ({len(ads_papers)} hits)"
            print(f"  ADS: {len(ads_papers)} papers")
        except Exception as e:
            sources_used["ads"] = f"error: {e}"
            print(f"  [WARN] ADS query failed: {e}", file=sys.stderr)
    elif not token:
        sources_used.setdefault("ads", "skipped (ADS_API_TOKEN not set)")
        print("  ADS: skipped (ADS_API_TOKEN env var not set)")

    # arXiv
    if not args.no_arxiv:
        print(f"  arXiv: querying (max {args.max})…")
        time.sleep(ARXIV_SLEEP_S)   # arXiv 가이드라인 준수 (3s 간격)
        try:
            ax_papers = arxiv_search(args.planet, args.max)
            papers = merge_papers(papers, ax_papers)
            sources_used["arxiv"] = f"queried ({len(ax_papers)} hits)"
            print(f"  arXiv: {len(ax_papers)} papers")
        except Exception as e:
            sources_used["arxiv"] = f"error: {e}"
            print(f"  [WARN] arXiv query failed: {e}", file=sys.stderr)

    # 최신순 정렬 (pubdate desc; null은 뒤로)
    papers.sort(key=lambda p: (p.get("pubdate") or ""), reverse=True)

    data = {
        "planet":        args.planet,
        "slug":          slug,
        "generated_at":  dt.datetime.utcnow().isoformat() + "Z",
        "sources":       sources_used,
        "papers":        papers,
    }
    save_bibliography(out_path, data)

    n_after = len(papers)
    n_new = n_after - n_before
    n_with_arxiv = sum(1 for p in papers if p.get("arxiv_id"))
    print(f"\n[Phase 3] Saved {out_path}")
    print(f"  Total papers: {n_after}  (new this run: {n_new})")
    print(f"  With arxiv_id: {n_with_arxiv}  (fetchable via ar5iv)")
    print(f"  Without arxiv_id: {n_after - n_with_arxiv}  (paywall fallback path)")


if __name__ == "__main__":
    main()
