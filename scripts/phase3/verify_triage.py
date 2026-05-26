# Phase 3 bibliography 의 score >= 14 paper 가 triage 분류 (deep_read/skim/skip/manual_followup) 받았는지 검사
"""Check that every must-read paper in a system's bibs is triaged.

Step 7 of the nearstars-phase3 workflow requires explicit classification
of every `combined_score >= 14` paper. This script flags any that are
still `status: pending` (or missing a category) — the gate before Step 8
deep-read.

A paper counts as triaged if it satisfies any of:
  - status == "skipped" (with skip_reason)
  - status == "fetched" AND category in {deep_read, skim, manual_followup}
  - status == "failed"  (manual_followup will be inferred from log)

Usage:
    python3 scripts/phase3/verify_triage.py <system>
    python3 scripts/phase3/verify_triage.py <system> --min-score 14
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from _system_config import BIB_DIR, load, slugify  # noqa: E402

TRIAGED_CATEGORIES = {"deep_read", "skim", "skip", "manual_followup"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("slug", help="phase3/<slug>/system.yaml")
    ap.add_argument("--min-score", type=int, default=14,
                    help="combined_score threshold for must-read (default 14)")
    args = ap.parse_args()

    cfg = load(args.slug)
    bib_paths = [BIB_DIR / f"{slugify(p)}.yaml" for p in cfg["planets"]]
    if cfg.get("system_query"):
        bib_paths.append(BIB_DIR / f"_system-{slugify(cfg['system_query'])}.yaml")

    untriaged = []
    n_total = 0
    n_must_read = 0
    for path in bib_paths:
        if not path.exists():
            print(f"[SKIP] {path.name}: not built yet")
            continue
        with open(path, encoding="utf-8") as f:
            bibd = yaml.safe_load(f) or {}
        for p in bibd.get("papers", []) or []:
            n_total += 1
            if (p.get("combined_score") or 0) < args.min_score:
                continue
            n_must_read += 1
            cat = p.get("category")
            status = p.get("status")
            if cat in TRIAGED_CATEGORIES:
                continue
            if status == "skipped" and p.get("skip_reason"):
                continue
            untriaged.append((path.name, p.get("ads_bibcode") or p.get("arxiv_id"),
                              (p.get("title") or "")[:60], status, cat))

    print(f"scanned {n_total} papers across {len(bib_paths)} bibs; "
          f"must-read (score >= {args.min_score}): {n_must_read}")

    if not untriaged:
        print(f"[OK] {args.slug}: all must-read papers triaged")
        return 0
    print(f"[FAIL] {args.slug}: {len(untriaged)} must-read paper(s) lack triage:")
    for bib, ident, title, status, cat in untriaged:
        print(f"  {bib:30s} {ident or '<no-id>':25s} status={status} cat={cat}  {title}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
