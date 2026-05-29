# 영문 source-of-truth 영역의 .md 파일 중 한글 비율이 임계값을 넘는 것을 검출하는 진단 도구
"""Scan English-source-of-truth markdown files for Korean-dominant content.

The repo's policy (AGENTS.md §2.1, feedback_md_language) says every
.md outside `ko/` should be written in English. This catches accidental
Korean-first drafting in workspaces / plans / docs / skills.

Usage:
    python3 scripts/check_language.py [--quiet]

Scope: every tracked .md file EXCEPT:
    - ko/**/*.md           (Korean mirror tree, intentionally Korean)
    - **/_papers/**        (external paper cache)
    - **/_archive/**       (archived snapshots)

Allowlist (intentionally Korean, won't trigger):
    - phase3/_audit/*.md   (one-off audit notes, user-approved)

Heuristic:
    For each file with ≥ 50 letter characters total, compute
    hangul / (hangul + ASCII_alpha). Flag if ratio ≥ 0.25.

Output:
    For each violation: <path>: <hangul%> hangul (<hangul>/<ascii_alpha>)
    Exit code 0 if clean, 1 otherwise.
"""
from __future__ import annotations

import fnmatch
import subprocess
import sys
from pathlib import Path


THRESHOLD = 0.25
MIN_LETTERS = 50

# 검출 제외 (ko 미러, paper/archive 캐시) — 정책상 한글이거나 외부 출처
EXCLUDE_PREFIXES = ("ko/",)
EXCLUDE_GLOBS = ("**/_papers/**", "**/_archive/**")

# 의도된 한글 영역 (사용자 명시 allowlist)
ALLOWLIST_GLOBS = (
    "phase3/_audit/*.md",
    # Korean-by-intent recovery/handoff notes (preserved as written).
    "phase2/2026-05-28-tier1-postmortem.md",
    "phase2/2026-05-29-next-session-prompt.md",
)


def excluded(path: str) -> bool:
    if any(path.startswith(p) for p in EXCLUDE_PREFIXES):
        return True
    for glob in EXCLUDE_GLOBS:
        if fnmatch.fnmatch(path, glob):
            return True
    return False


def allowlisted(path: str) -> bool:
    return any(fnmatch.fnmatch(path, g) for g in ALLOWLIST_GLOBS)


def hangul_ratio(text: str) -> tuple[int, int, float]:
    hangul = sum(1 for c in text if 0xAC00 <= ord(c) <= 0xD7A3)
    ascii_alpha = sum(1 for c in text if c.isascii() and c.isalpha())
    total = hangul + ascii_alpha
    return hangul, ascii_alpha, (hangul / total if total else 0.0)


def main() -> int:
    quiet = "--quiet" in sys.argv
    repo_root = Path(
        subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    )
    files = subprocess.check_output(
        ["git", "ls-files", "*.md"], cwd=repo_root, text=True,
    ).strip().splitlines()

    violations = []
    scanned = 0
    for rel in files:
        if excluded(rel) or allowlisted(rel):
            continue
        try:
            text = (repo_root / rel).read_text(encoding="utf-8")
        except Exception:
            continue
        hangul, ascii_alpha, ratio = hangul_ratio(text)
        if hangul + ascii_alpha < MIN_LETTERS:
            continue
        scanned += 1
        if ratio >= THRESHOLD:
            violations.append((rel, hangul, ascii_alpha, ratio))

    if violations:
        print(f"[FAIL] {len(violations)} file(s) over {THRESHOLD*100:.0f}% hangul threshold "
              f"(scanned {scanned} English-source .md):")
        for rel, h, a, r in sorted(violations, key=lambda x: -x[3]):
            print(f"  {rel}: {r*100:.1f}% hangul ({h}/{a})")
        return 1

    if not quiet:
        print(f"[PASS] scanned {scanned} English-source .md file(s), "
              f"no Korean-dominant content.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
