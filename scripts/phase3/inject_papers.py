# Phase 3 bibliography 에 ADS 키워드 검색이 놓친 핵심 paper 를 system.yaml 기반으로 일괄 inject
"""Inject ADS-missed papers into per-bibliography YAML files.

Reads `phase3/<system>/system.yaml`'s `injections:` block; for each entry
fetches the paper from ADS by bibcode and adds it to every target bib as
`status: pending` (deferred to triage in Step 7). Idempotent — papers
already in a target bib are skipped.

Replaces the per-system `phase3/<system>/add_missing_papers.py` pattern.

Usage:
    ADS_API_TOKEN=... python3 scripts/phase3/inject_papers.py <system>
    python3 scripts/phase3/inject_papers.py <system> --check
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

from _system_config import BIB_DIR, load


def fetch_ads_metadata(bibcode: str, token: str) -> dict | None:
    fl = "bibcode,title,author,year,pubdate,doi,abstract,identifier"
    q = urllib.parse.urlencode({"q": f'bibcode:"{bibcode}"', "fl": fl, "rows": 1})
    req = urllib.request.Request(
        f"https://api.adsabs.harvard.edu/v1/search/query?{q}",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    docs = data.get("response", {}).get("docs", [])
    if not docs:
        return None
    d = docs[0]
    arx = next(
        (i.split("arXiv:")[-1] for i in (d.get("identifier") or []) if "arXiv:" in i),
        None,
    )
    return {
        "arxiv_id": arx,
        "ads_bibcode": d.get("bibcode"),
        "title": (d.get("title") or [None])[0],
        "authors": d.get("author") or [],
        "year": str(d.get("year") or ""),
        "pubdate": d.get("pubdate"),
        "doi": ((d.get("doi") or [None])[0]
                if isinstance(d.get("doi"), list)
                else d.get("doi")),
        "abstract": d.get("abstract"),
        "status": "pending",
        "category": None,
        "skip_reason": None,
        "fetch_error": None,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("slug", help="phase3/<slug>/system.yaml")
    ap.add_argument("--check", action="store_true",
                    help="Report what would be injected; no writes, no ADS calls")
    args = ap.parse_args()

    cfg = load(args.slug)
    injections = cfg["injections"]
    if not injections:
        print(f"[OK] {args.slug}: no injections defined in system.yaml")
        return 0

    if args.check:
        # Inventory: which bibs would each injection touch, and is the paper
        # already there?
        missing = []
        for inj in injections:
            bib = inj["bibcode"]
            for slug in inj["targets"]:
                path = BIB_DIR / f"{slug}.yaml"
                if not path.exists():
                    missing.append((bib, slug, "bib-missing"))
                    continue
                with open(path, encoding="utf-8") as f:
                    bibd = yaml.safe_load(f) or {}
                papers = bibd.get("papers") or []
                if not any(p.get("ads_bibcode") == bib for p in papers):
                    missing.append((bib, slug, "would-inject"))
        if not missing:
            print(f"[CLEAN] {args.slug}: all {len(injections)} injections already present")
            return 0
        print(f"[DIFF] {args.slug}: {len(missing)} target-injections pending:")
        for bib, slug, reason in missing:
            print(f"  {reason:14s}  {slug:30s}  {bib}")
        return 1

    token = os.environ.get("ADS_API_TOKEN")
    if not token:
        print("[FAIL] ADS_API_TOKEN not set", file=sys.stderr)
        return 1

    cache = {}
    for inj in injections:
        bib = inj["bibcode"]
        if bib not in cache:
            md = fetch_ads_metadata(bib, token)
            if not md:
                print(f"  MISS  {bib}: not found on ADS")
                continue
            cache[bib] = md
        md = cache[bib]
        for slug in inj["targets"]:
            path = BIB_DIR / f"{slug}.yaml"
            if not path.exists():
                print(f"  SKIP  {slug}.yaml not found")
                continue
            with open(path, encoding="utf-8") as f:
                bibd = yaml.safe_load(f)
            papers = bibd.setdefault("papers", [])
            if any(p.get("ads_bibcode") == bib for p in papers):
                print(f"  HAVE  {slug:30s} {bib}")
                continue
            papers.append(dict(md))
            with open(path, "w", encoding="utf-8") as f:
                yaml.safe_dump(bibd, f, sort_keys=False, allow_unicode=True)
            title = (md.get("title") or "")[:60]
            print(f"  ADD   {slug:30s} {bib}  arx={md.get('arxiv_id')}  {title}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
