# Phase 3 ko/en 마크다운 블록 구조 일치 검사 (build_html.py 가 빌드 중간에 fail 하기 전 pre-flight 용)
"""Verify ko/en block parity for one or more Phase 3 syntheses.

`build_html.py` enforces parity internally but fails mid-build. This
script runs the same check standalone so Step 11 → 12 can fail fast.

Usage:
    python3 scripts/phase3/check_block_parity.py <slug> [<slug>...]
    python3 scripts/phase3/check_block_parity.py --all
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_html import pair_blocks, parse_md  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
EN_DIR = ROOT / "docs" / "phase3"
KO_DIR = ROOT / "ko" / "docs" / "phase3"


def check(slug: str) -> int:
    en_path = EN_DIR / f"{slug}.md"
    ko_path = KO_DIR / f"{slug}.md"
    if not en_path.exists():
        print(f"[FAIL] {slug}: en source missing ({en_path.relative_to(ROOT)})")
        return 1
    if not ko_path.exists():
        print(f"[FAIL] {slug}: ko mirror missing ({ko_path.relative_to(ROOT)})")
        return 1
    en = parse_md(en_path)
    ko = parse_md(ko_path)
    try:
        pair_blocks(en, ko, slug)
    except SystemExit as e:
        print(f"[FAIL] {e}")
        return 1
    print(f"[OK] {slug}: {len(en)} blocks paired")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("slugs", nargs="*", help="planet slugs e.g. trappist-1-d")
    ap.add_argument("--all", action="store_true",
                    help="Check every docs/phase3/*.md against its ko mirror")
    args = ap.parse_args()

    if args.all:
        slugs = sorted(p.stem for p in EN_DIR.glob("*.md"))
    elif args.slugs:
        slugs = args.slugs
    else:
        ap.error("provide slug(s) or --all")

    fail = 0
    for slug in slugs:
        fail |= check(slug)
    return fail


if __name__ == "__main__":
    sys.exit(main())
