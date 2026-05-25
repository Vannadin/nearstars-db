# Phase 3 citation graph 1-hop expander — bibliography YAML 안의 핵심 논문들이 인용하는 reference 를 ADS 로 가져와 머지
"""Walk the 1-hop citation graph of a Phase 3 bibliography.

Why: per-planet ADS / arXiv keyword search misses papers cited by the
primary references (e.g., Piaulet 2025 cites Greene 2023 — both should
end up in the d bibliography for cross-reference, but a search for
"TRAPPIST-1 d" may pull only one of them if the other's abstract
doesn't repeat the planet name).

This script:
  1. Opens a bibliography YAML produced by build_bibliography.py
  2. Selects a "seed" subset of papers (default: all status=fetched
     AND has ads_bibcode) — these are the ones whose references we expand
  3. For each seed, calls ADS Solr `references(bibcode:X)` to get the
     papers they cite
  4. Deduplicates against the existing bibliography
  5. Looks up the new bibcodes via ADS for title/abstract/arxiv_id/doi
  6. Merges into the bibliography YAML with `status: pending` and
     a new `source: citation_of=<seed_bibcode>` annotation

Usage:
  python3 scripts/phase3/expand_citations.py docs/phase3/_bib/trappist-1-b.yaml
  python3 scripts/phase3/expand_citations.py docs/phase3/_bib/trappist-1-b.yaml \
      --triage phase3/trappist_1/_triage-result.json \
      --max-per-seed 80

Filtering:
  --triage <json>       Use a triage result JSON to seed only deep_read papers
                        (the JSON is the format produced by the triage logic in
                        phase3/<system>/_triage-result.json).
  --seed-bibcode <bib>  Manually seed a specific bibcode (can repeat)
  --max-per-seed N      Cap references per seed (default 80)
  --since-year YYYY     Only keep references published in this year or later
                        (default 1995 — paper-discussion timescale for
                        TRAPPIST-1-era work)

Idempotent: re-running merges new entries; existing status/category/
skip_reason are preserved by merge_papers().
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
import urllib.parse
import urllib.request

import yaml

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(__file__))

# Reuse helpers from build_bibliography
from build_bibliography import (
    ADS_API, ads_to_paper, merge_papers, save_bibliography, load_existing,
)

ADS_SLEEP_S = 0.2  # ADS rate limit: 5000/day, way more than we need; small sleep for politeness


def ads_references(seed_bibcode: str, token: str, max_results: int) -> list[dict]:
    """ADS Solr: references(bibcode:X) → list of doc dicts that X cites."""
    fields = "bibcode,title,author,abstract,year,pubdate,doi,identifier"
    params = {
        "q": f"references(bibcode:{seed_bibcode})",
        "fl": fields,
        "rows": min(max_results, 200),
        "sort": "date desc",
    }
    url = f"{ADS_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.loads(r.read().decode())
    return resp.get("response", {}).get("docs", []) or []


def select_seeds(bib: dict, triage_path: str | None, manual_seeds: list[str]) -> list[str]:
    """Return a list of seed ads_bibcodes."""
    papers = bib.get("papers", []) or []
    seeds: set[str] = set()

    if manual_seeds:
        seeds.update(manual_seeds)

    if triage_path:
        with open(triage_path) as f:
            triage = json.load(f)
        # triage format: {"arxiv": {"deep_read": [...], ...}, "no_arxiv": {...}}
        deep = (triage.get("arxiv") or {}).get("deep_read", []) + \
               (triage.get("no_arxiv") or {}).get("deep_read", [])
        # Match by ads_bibcode for arxiv-set papers, by ads_bibcode for no_arxiv set
        for p in deep:
            bib_id = p.get("ads_bibcode")
            if bib_id:
                seeds.add(bib_id)

    # Default: every paper with ads_bibcode AND status=fetched (it loaded successfully)
    if not seeds:
        for p in papers:
            if p.get("ads_bibcode") and p.get("status") == "fetched":
                seeds.add(p["ads_bibcode"])

    # But restrict to bibcodes that are actually in our bibliography (sanity check)
    biblio_bibcodes = {p.get("ads_bibcode") for p in papers if p.get("ads_bibcode")}
    seeds = seeds & biblio_bibcodes if (manual_seeds or triage_path) else seeds
    # If manual seeds or triage are given but produced an empty intersection,
    # warn but still allow expansion from those raw bibcodes (user knows best)
    if (manual_seeds or triage_path) and not seeds:
        seeds = set(manual_seeds) | {p.get("ads_bibcode") for p in deep if p.get("ads_bibcode")}
    return sorted(seeds)


def main():
    parser = argparse.ArgumentParser(description="Expand a Phase 3 bibliography by walking 1-hop citations.")
    parser.add_argument("bibliography", help="Path to YAML produced by build_bibliography.py")
    parser.add_argument("--triage", default=None,
                        help="Optional triage JSON (with arxiv.deep_read / no_arxiv.deep_read keys)")
    parser.add_argument("--seed-bibcode", action="append", default=[],
                        help="Manually add a seed bibcode (repeatable)")
    parser.add_argument("--max-per-seed", type=int, default=80,
                        help="Max references per seed paper (default 80)")
    parser.add_argument("--since-year", type=int, default=1995,
                        help="Keep references from this year or later (default 1995)")
    parser.add_argument("--limit-seeds", type=int, default=None,
                        help="Stop after N seeds (debug)")
    args = parser.parse_args()

    bib = load_existing(args.bibliography)
    if bib is None:
        print(f"[Phase 3] Bibliography not found: {args.bibliography}", file=sys.stderr)
        sys.exit(1)

    token = os.environ.get("ADS_API_TOKEN")
    if not token:
        print("[Phase 3] ADS_API_TOKEN env var required for citation expansion.", file=sys.stderr)
        sys.exit(1)

    seeds = select_seeds(bib, args.triage, args.seed_bibcode)
    if not seeds:
        print("[Phase 3] No seed papers to expand. Use --triage or --seed-bibcode.")
        return

    if args.limit_seeds:
        seeds = seeds[:args.limit_seeds]

    print(f"[Phase 3] Expanding from {len(seeds)} seed papers, --max-per-seed {args.max_per_seed}")

    n_before = len(bib.get("papers", []) or [])
    total_refs_fetched = 0
    total_skipped_year = 0

    # Walk each seed
    for i, seed in enumerate(seeds):
        try:
            docs = ads_references(seed, token, args.max_per_seed)
        except Exception as e:
            print(f"  [{i+1}/{len(seeds)}] {seed}  ERROR: {e}", file=sys.stderr)
            continue

        # Year filter
        kept = []
        for d in docs:
            yr = d.get("year")
            try:
                yr_int = int(yr) if yr else 0
            except Exception:
                yr_int = 0
            if yr_int >= args.since_year:
                kept.append(d)
            else:
                total_skipped_year += 1

        new_papers = [ads_to_paper(d) for d in kept]
        # Annotate provenance
        for np_ in new_papers:
            np_["source"] = f"citation_of={seed}"

        bib["papers"] = merge_papers(bib.get("papers", []) or [], new_papers)
        total_refs_fetched += len(kept)
        print(f"  [{i+1}/{len(seeds)}] {seed}  +{len(kept)} refs (post-year-filter)")
        time.sleep(ADS_SLEEP_S)

    # Re-sort by pubdate desc
    bib["papers"].sort(key=lambda p: (p.get("pubdate") or ""), reverse=True)

    n_after = len(bib["papers"])
    n_new = n_after - n_before
    bib.setdefault("sources", {})["citation_expansion"] = (
        f"{len(seeds)} seeds, +{n_new} new, {total_refs_fetched} refs fetched"
    )

    save_bibliography(args.bibliography, bib)

    print(f"\n[Phase 3] Done.")
    print(f"  Seed papers walked:    {len(seeds)}")
    print(f"  References fetched:    {total_refs_fetched}  (skipped pre-{args.since_year}: {total_skipped_year})")
    print(f"  Bibliography papers:   {n_before} → {n_after}  (+{n_new} new)")
    print(f"  Saved: {args.bibliography}")


if __name__ == "__main__":
    main()
