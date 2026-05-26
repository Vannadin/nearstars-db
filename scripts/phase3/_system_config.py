# phase3/<system>/system.yaml 로딩 + 검증 공통 유틸 (run_phase3 / inject_papers / verify_* 가 공유)
"""Shared loader for `phase3/<system>/system.yaml`.

Schema:
    system_slug: <str>          # must match the dir name
    display_name: <str>         # for log lines
    planets: [ "<Name 1>", ... ] # passed to build_bibliography.py
    system_query: "<str>"       # for build_bibliography.py --system
    score:
      keep_threshold: <int>     # default 8
      mark_skipped_below: <int> # default 14
    expand:
      max_per_seed: <int>       # default 60
      since_year: <int>         # default 2000
    injections:                 # optional
      - bibcode: "<str>"
        targets: [ <bib-slug>, ... ]   # without _bib/ prefix or .yaml suffix
        note: "<str>"                  # human-readable
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
BIB_DIR = ROOT / "docs" / "phase3" / "_bib"


def system_yaml_path(slug: str) -> Path:
    return ROOT / "phase3" / slug / "system.yaml"


def load(slug: str) -> dict:
    path = system_yaml_path(slug)
    if not path.exists():
        raise SystemExit(f"[FAIL] {path.relative_to(ROOT)} not found")
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    # mandatory
    for k in ("system_slug", "planets"):
        if k not in data:
            raise SystemExit(f"[FAIL] {path.relative_to(ROOT)}: missing required key '{k}'")
    if data["system_slug"] != slug:
        raise SystemExit(
            f"[FAIL] system_slug='{data['system_slug']}' does not match dir name '{slug}'"
        )

    # defaults
    data.setdefault("display_name", slug.replace("_", " ").title())
    data.setdefault("system_query", None)
    score = data.setdefault("score", {})
    score.setdefault("keep_threshold", 8)
    score.setdefault("mark_skipped_below", 14)
    expand = data.setdefault("expand", {})
    expand.setdefault("max_per_seed", 60)
    expand.setdefault("since_year", 2000)
    data.setdefault("injections", [])

    return data


def slugify(name: str) -> str:
    """Match scripts/phase3/build_bibliography.py:slugify exactly."""
    import re
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")
