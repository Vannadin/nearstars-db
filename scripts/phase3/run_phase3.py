# Phase 3 Step 2~6 (bibliography 빌드 → system bib → citation 확장 → score → inject → fetch) 일괄 드라이버
"""Driver for Phase 3 Steps 2–6 from `phase3/<system>/system.yaml`.

Stages (numbered to match nearstars-phase3 SKILL.md):
  2 — build per-planet bibliographies (one run of build_bibliography.py per planet)
  3 — build system-level supplementary bibliography
  4 — expand 1-hop citations on every bib
  5 — score + filter every bib
  5b — inject ADS-missed papers from system.yaml
  6 — fetch arXiv full text for all pending+arxiv_id papers

Stages 2 and 3 require `ADS_API_TOKEN`. Stage 6 has a 2 s/paper rate.
Steps 7+ (triage, synthesis, ko mirror, build, commit) stay manual under
the skill runbook — they need judgment, not automation.

Usage:
    python3 scripts/phase3/run_phase3.py <system>                # all stages 2–6
    python3 scripts/phase3/run_phase3.py <system> --stage 2,3,4  # specific stages
    python3 scripts/phase3/run_phase3.py <system> --dry-run      # print commands, don't execute
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from _system_config import BIB_DIR, ROOT, load, slugify

ALL_STAGES = ["2", "3", "4", "5", "5b", "6"]


def stage_2_per_planet_bibs(cfg, *, dry_run: bool) -> None:
    """build_bibliography.py for each planet."""
    for planet in cfg["planets"]:
        cmd = [
            sys.executable,
            str(ROOT / "scripts/phase3/build_bibliography.py"),
            planet,
        ]
        run(cmd, dry_run=dry_run, label=f"build_bibliography {planet!r}")


def stage_3_system_bib(cfg, *, dry_run: bool) -> None:
    query = cfg.get("system_query")
    if not query:
        print("[SKIP] stage 3: system.yaml has no system_query")
        return
    cmd = [
        sys.executable,
        str(ROOT / "scripts/phase3/build_bibliography.py"),
        query,
        "--system",
        "--max", "200",
    ]
    run(cmd, dry_run=dry_run, label=f"build_bibliography --system {query!r}")


def _bib_paths_for(cfg) -> list[Path]:
    """All per-planet + system bib YAMLs that exist now."""
    paths = []
    for planet in cfg["planets"]:
        p = BIB_DIR / f"{slugify(planet)}.yaml"
        if p.exists():
            paths.append(p)
    if cfg.get("system_query"):
        p = BIB_DIR / f"_system-{slugify(cfg['system_query'])}.yaml"
        if p.exists():
            paths.append(p)
    return paths


def stage_4_expand(cfg, *, dry_run: bool) -> None:
    ex = cfg["expand"]
    for path in _bib_paths_for(cfg):
        cmd = [
            sys.executable,
            str(ROOT / "scripts/phase3/expand_citations.py"),
            str(path),
            "--max-per-seed", str(ex["max_per_seed"]),
            "--since-year", str(ex["since_year"]),
        ]
        run(cmd, dry_run=dry_run, label=f"expand_citations {path.name}")


def stage_5_score(cfg, *, dry_run: bool) -> None:
    sc = cfg["score"]
    for path in _bib_paths_for(cfg):
        cmd = [
            sys.executable,
            str(ROOT / "scripts/phase3/score_papers.py"),
            str(path),
            "--keep-threshold", str(sc["keep_threshold"]),
            "--mark-skipped-below", str(sc["mark_skipped_below"]),
        ]
        run(cmd, dry_run=dry_run, label=f"score_papers {path.name}")


def stage_5b_inject(cfg, slug, *, dry_run: bool) -> None:
    if not cfg.get("injections"):
        print("[SKIP] stage 5b: no injections in system.yaml")
        return
    cmd = [
        sys.executable,
        str(ROOT / "scripts/phase3/inject_papers.py"),
        slug,
    ]
    run(cmd, dry_run=dry_run, label=f"inject_papers {slug}")


def stage_6_fetch(cfg, *, dry_run: bool) -> None:
    for path in _bib_paths_for(cfg):
        cmd = [
            sys.executable,
            str(ROOT / "scripts/phase3/fetch_arxiv_texts.py"),
            str(path),
        ]
        run(cmd, dry_run=dry_run, label=f"fetch_arxiv_texts {path.name}")


def run(cmd: list[str], *, dry_run: bool, label: str) -> None:
    print(f"\n── {label}")
    print("   $ " + " ".join(cmd))
    if dry_run:
        return
    res = subprocess.run(cmd)
    if res.returncode != 0:
        sys.exit(f"[FAIL] {label} exited {res.returncode}")


STAGE_FUNCS = {
    "2":  lambda cfg, slug, dry: stage_2_per_planet_bibs(cfg, dry_run=dry),
    "3":  lambda cfg, slug, dry: stage_3_system_bib(cfg, dry_run=dry),
    "4":  lambda cfg, slug, dry: stage_4_expand(cfg, dry_run=dry),
    "5":  lambda cfg, slug, dry: stage_5_score(cfg, dry_run=dry),
    "5b": lambda cfg, slug, dry: stage_5b_inject(cfg, slug, dry_run=dry),
    "6":  lambda cfg, slug, dry: stage_6_fetch(cfg, dry_run=dry),
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("slug", help="phase3/<slug>/system.yaml")
    ap.add_argument("--stage", default=",".join(ALL_STAGES),
                    help=f"Comma-separated subset of {ALL_STAGES} (default: all)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print commands only; don't execute")
    args = ap.parse_args()

    requested = [s.strip() for s in args.stage.split(",") if s.strip()]
    unknown = set(requested) - set(ALL_STAGES)
    if unknown:
        sys.exit(f"[FAIL] unknown stage(s): {sorted(unknown)} (valid: {ALL_STAGES})")

    cfg = load(args.slug)
    print(f"=== Phase 3 driver: {cfg['display_name']} ({args.slug}) ===")
    print(f"   planets: {cfg['planets']}")
    print(f"   stages:  {requested}")

    for stage in requested:
        STAGE_FUNCS[stage](cfg, args.slug, args.dry_run)

    print("\n[OK] driver complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
