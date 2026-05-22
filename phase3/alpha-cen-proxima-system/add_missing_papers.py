# α Cen + Proxima 시스템 Phase 3 bib 에 핵심 디스커버리 페이퍼 보강 (ADS 키워드 매치 실패분)
"""Inject critical discovery / atmosphere papers that the ADS keyword search
missed (their titles don't contain the system+letter compound, so
build_bibliography.py never found them).

Run once after build_bibliography.py + score_papers.py. Re-runs are
idempotent — papers already in a bib are skipped.
"""
import os
import sys
import urllib.parse
import urllib.request
import json
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BIB_DIR = ROOT / "docs/phase3/_bib"
TOKEN = os.environ.get("ADS_API_TOKEN")
if not TOKEN:
    print("ADS_API_TOKEN not set", file=sys.stderr)
    sys.exit(1)

# (bibcode, target_bibs) — target_bibs is a list of bib slugs to inject into.
# arxiv_id is fetched from ADS to avoid manual maintenance.
INJECTIONS = [
    ("2016Natur.536..437A", ["proxima-cen-b", "proxima-cen"]),                # Anglada-Escudé 2016 Proxima b discovery
    ("2022A&A...658A.115F", ["proxima-cen-d", "proxima-cen-b", "proxima-cen"]),# Faria 2022 Proxima d candidate
    ("2025A&A...700A..11S", ["proxima-cen-b", "proxima-cen-d", "proxima-cen"]),# Suárez Mascareño 2025 NIRPS — SM25
    ("2020A&A...639A..77S", ["proxima-cen-b", "proxima-cen"]),                # Suárez Mascareño 2020 Revisiting Proxima
    ("2016A&A...586A..90P", ["alpha-centauri-a", "alpha-centauri-b", "_system-alpha-centauri"]),  # Pourbaix & Boffin 2016 masses
    ("2017A&A...601A.120B", ["proxima-cen-b", "proxima-cen"]),                # Boutle 2017 Proxima GCM
    ("2016A&A...596A.112T", ["proxima-cen-b", "proxima-cen"]),                # Turbet 2016 Proxima 1D climate
    ("2012ApJ...757..112B", ["proxima-cen", "proxima-cen-b"]),                # Boyajian 2012 Proxima R
    ("2018A&A...612A..49R", ["proxima-cen", "proxima-cen-b"]),                # Reiners 2018 CARMENES Proxima high-energy
]


def fetch_ads_metadata(bibcode):
    """Pull title, authors, year, doi, abstract, arxiv_id from ADS."""
    fl = "bibcode,title,author,year,pubdate,doi,abstract,identifier"
    q = urllib.parse.urlencode({"q": f'bibcode:"{bibcode}"', "fl": fl, "rows": 1})
    req = urllib.request.Request(
        f"https://api.adsabs.harvard.edu/v1/search/query?{q}",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    docs = data.get("response", {}).get("docs", [])
    if not docs:
        return None
    d = docs[0]
    arx = next((i.split("arXiv:")[-1] for i in (d.get("identifier") or []) if "arXiv:" in i), None)
    return {
        "arxiv_id": arx,
        "ads_bibcode": d.get("bibcode"),
        "title": (d.get("title") or [None])[0],
        "authors": d.get("author") or [],
        "year": str(d.get("year") or ""),
        "pubdate": d.get("pubdate"),
        "doi": (d.get("doi") or [None])[0] if isinstance(d.get("doi"), list) else d.get("doi"),
        "abstract": d.get("abstract"),
        "status": "pending",
        "category": None,
        "skip_reason": None,
        "fetch_error": None,
    }


def main():
    cache = {}
    for bibcode, targets in INJECTIONS:
        if bibcode not in cache:
            md = fetch_ads_metadata(bibcode)
            if not md:
                print(f"  MISS  {bibcode}: not found on ADS")
                continue
            cache[bibcode] = md
        md = cache[bibcode]
        for slug in targets:
            path = BIB_DIR / f"{slug}.yaml"
            if not path.exists():
                print(f"  SKIP  {slug}.yaml not found")
                continue
            with open(path) as f:
                bib = yaml.safe_load(f)
            papers = bib.setdefault("papers", [])
            if any(p.get("ads_bibcode") == bibcode for p in papers):
                print(f"  HAVE  {slug:25s} {bibcode}")
                continue
            papers.append(dict(md))
            with open(path, "w") as f:
                yaml.safe_dump(bib, f, sort_keys=False, allow_unicode=True)
            print(f"  ADD   {slug:25s} {bibcode}  arx={md['arxiv_id']}  {md['title'][:60]}")


if __name__ == "__main__":
    main()
