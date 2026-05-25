# 레포 전반의 마크다운 dead-link 를 스캔하는 진단 도구 (수동 실행)
"""Scan markdown inline links in tracked .md files for missing targets.

Usage:
    python3 scripts/check_dead_links.py [--quiet]

Scope:
    Root .md files (AGENTS.md, README.md, CLAUDE.md, NOTICE, etc.),
    docs/, ko/docs/, plans/, ko/plans/, phase2/, phase3/,
    .claude/skills/, .agents/skills/

Skips:
    - external URLs (http://, https://, mailto:)
    - same-page anchors (#section)
    - image embeds (![alt](path)) — covered, just like text links
    - code-fence blocks (links inside ``` ``` are ignored)

Output:
    For each broken link:  <source path>:<line>: broken link → <target>
    Exit code 0 if clean, 1 otherwise.

Resolution rule:
    Targets are resolved relative to the source file. Trailing #anchors
    are stripped before checking existence (Obsidian/CommonMark style).
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path


LINK_RE = re.compile(r'(?<!\\)\[([^\]\n]*)\]\(([^)\s]+?)\)')
CODE_FENCE_RE = re.compile(r'^```')


def tracked_md_files(repo_root: Path) -> list[Path]:
    """Return all repo-tracked .md files inside the relevant trees."""
    roots = [
        '*.md',
        'docs/**/*.md',
        'ko/**/*.md',
        'plans/**/*.md',
        'phase2/**/*.md',
        'phase3/**/*.md',
        '.claude/skills/**/*.md',
        '.agents/skills/**/*.md',
    ]
    out = subprocess.check_output(
        ['git', 'ls-files', '--', *roots],
        cwd=repo_root, text=True,
    )
    return [repo_root / p for p in out.strip().splitlines() if p.endswith('.md')]


def extract_links(path: Path) -> list[tuple[int, str]]:
    """Return (lineno, target) for each non-external, non-anchor link."""
    hits = []
    in_fence = False
    with path.open(encoding='utf-8') as f:
        for lineno, line in enumerate(f, 1):
            if CODE_FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for m in LINK_RE.finditer(line):
                # inline backtick code 안의 매치는 건너뜀
                if line[:m.start()].count('`') % 2 == 1:
                    continue
                target = m.group(2)
                if target.startswith(('http://', 'https://', 'mailto:', '#')):
                    continue
                hits.append((lineno, target))
    return hits


def resolve(source: Path, target: str, repo_root: Path) -> Path:
    """Resolve a relative link target against the source file's directory."""
    bare = target.split('#', 1)[0]
    if not bare:
        return source
    if bare.startswith('/'):
        return repo_root / bare.lstrip('/')
    return (source.parent / bare).resolve()


def main() -> int:
    quiet = '--quiet' in sys.argv
    repo_root = Path(
        subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip()
    )
    broken: list[str] = []
    files = tracked_md_files(repo_root)
    for path in files:
        for lineno, target in extract_links(path):
            resolved = resolve(path, target, repo_root)
            if not resolved.exists():
                rel = path.relative_to(repo_root)
                broken.append(f"{rel}:{lineno}: broken link → {target}")

    if broken:
        print(f"[FAIL] {len(broken)} broken link(s) across {len(files)} file(s):")
        for line in broken:
            print(f"  {line}")
        return 1

    if not quiet:
        print(f"[PASS] checked {len(files)} markdown file(s), no broken links.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
