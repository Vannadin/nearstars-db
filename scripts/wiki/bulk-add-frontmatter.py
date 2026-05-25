#!/usr/bin/env python3
# Workspace .md에 YAML frontmatter + minimal Related 추가 — 부트스트랩 1회용 + 영구 유틸
"""Bulk-add wiki frontmatter to workspace docs.

Used during Phase 2 bootstrap to backfill workspace files
(phase2/<topic>/, phase3/<system>/, docs/phase1-50ly/, etc.) that
were missed in the initial pass. Also reusable for future bulk ops.

Files with existing frontmatter are skipped. The script never rewrites
file body content — only prepends frontmatter and appends `## Related`.
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)

# Cluster assignment by parent directory prefix.
CLUSTER_MAP = {
    "phase3/trappist-1-system": "system-trappist-1",
    "phase3/alpha-cen-proxima-system": "system-alpha-cen",
    "phase3/html-pipeline": "phase3-procedure",
    "phase3/stability-sim": "phase3-procedure",
    "phase3/_audit": "comparisons",
    "phase2/alpha_centauri_proxima": "system-alpha-cen",
    "phase2/trappist_1": "system-trappist-1",
    "phase2/schema-expansion": "methodology",
    "phase2/skill-phase3-optimization": "phase3-procedure",
    "phase2/skill-policy-permanence": "methodology",
    "docs/phase1-50ly": "methodology",
    "docs/famous-20-non-hosts": "methodology",
}

# Files that are reports/audits, not workspace-tracking
SYNTHESIS_FILENAMES = {
    "STABILITY_REPORT.md",
    "audit-pass-2026-05-22.md",
    "paper-count-summary.md",
    "art-redundancy-2026-05-22.md",
}

WORKSPACE_FILES = [
    "phase3/trappist-1-system/checklist.md",
    "phase3/trappist-1-system/context-notes.md",
    "phase3/trappist-1-system/audit-pass-2026-05-22.md",
    "phase3/trappist-1-system/manual-paper-followup.md",
    "phase3/trappist-1-system/paper-count-summary.md",
    "phase3/alpha-cen-proxima-system/checklist.md",
    "phase3/alpha-cen-proxima-system/context-notes.md",
    "phase3/alpha-cen-proxima-system/manual-paper-followup.md",
    "phase3/html-pipeline/checklist.md",
    "phase3/html-pipeline/context-notes.md",
    "phase3/stability-sim/checklist.md",
    "phase3/stability-sim/context-notes.md",
    "phase3/stability-sim/plan.md",
    "phase3/stability-sim/STABILITY_REPORT.md",
    "phase3/_audit/art-redundancy-2026-05-22.md",
    "phase2/alpha_centauri_proxima/checklist.md",
    "phase2/alpha_centauri_proxima/context-notes.md",
    "phase2/schema-expansion/checklist.md",
    "phase2/schema-expansion/context-notes.md",
    "phase2/skill-phase3-optimization/checklist.md",
    "phase2/skill-phase3-optimization/context-notes.md",
    "phase2/skill-phase3-optimization/plan.md",
    "phase2/skill-policy-permanence/checklist.md",
    "phase2/skill-policy-permanence/context-notes.md",
    "phase2/skill-policy-permanence/plan.md",
    "phase2/trappist_1/checklist.md",
    "phase2/trappist_1/context-notes.md",
    "docs/phase1-50ly/checklist.md",
    "docs/phase1-50ly/context-notes.md",
    "docs/phase1-50ly/plan.md",
    "docs/famous-20-non-hosts/checklist.md",
    "docs/famous-20-non-hosts/plan.md",
]


def cluster_for(filepath: Path) -> str:
    path_str = str(filepath).replace("\\", "/")
    for prefix, cluster in CLUSTER_MAP.items():
        if path_str.startswith(prefix):
            return cluster
    return "workspaces-misc"


def get_title(content: str, default: str) -> str:
    for line in content.splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip()
        if s and not s.startswith("<!--") and not s.startswith("---"):
            break
    return default


def slug_from_path(path: Path) -> str:
    parent = path.parent.name.replace("_", "-")
    stem = path.stem
    return f"{parent}-{stem}"


def sibling_pages(filepath: Path):
    """Return list of (slug, filename_stem) for sibling .md files."""
    out = []
    for sib in sorted(filepath.parent.glob("*.md")):
        if sib.name == filepath.name:
            continue
        out.append((slug_from_path(sib), sib.stem))
    return out


def parent_topic_link(filepath: Path):
    """Return (label, relative_path) of a likely parent hub doc, or None."""
    path_str = str(filepath).replace("\\", "/")
    # Phase 3 system workspaces → docs/phase3/<system>/<body>.md likely exists
    if path_str.startswith("phase3/trappist-1-system"):
        return ("system-trappist-1 entity pages", "../../docs/phase3/trappist-1-e.md")
    if path_str.startswith("phase3/alpha-cen-proxima-system"):
        return ("system-alpha-cen entity pages", "../../docs/phase3/alpha-centauri-a.md")
    if path_str.startswith("phase2/alpha_centauri_proxima"):
        return ("system-alpha-cen entity pages", "../../docs/phase3/alpha-centauri-a.md")
    if path_str.startswith("phase2/trappist_1"):
        return ("system-trappist-1 entity pages", "../../docs/phase3/trappist-1-e.md")
    # Procedure clusters → methodology or phase3 skill
    if "phase3-procedure" in cluster_for(filepath):
        return ("phase3 procedure (skill)", "../../.agents/skills/nearstars-phase3/SKILL.md")
    if cluster_for(filepath) == "methodology":
        return ("methodology hub", "../../docs/reference/methodology.md")
    if cluster_for(filepath) == "comparisons":
        return ("comparisons cluster (REX, Stellarium)", "../../docs/reference/rex-data-comparison.md")
    return None


def make_frontmatter(filepath: Path, content: str) -> str:
    is_synthesis = filepath.name in SYNTHESIS_FILENAMES
    file_type = "synthesis" if is_synthesis else "workspace"
    title = get_title(content, slug_from_path(filepath))
    slug = slug_from_path(filepath)
    cluster = cluster_for(filepath)
    siblings = sibling_pages(filepath)
    related = ", ".join(f"[[{slug}]]" for slug, _ in siblings) if siblings else ""

    return "\n".join([
        "---",
        f"type: {file_type}",
        f'title: "{title}"',
        f"slug: {slug}",
        f"cluster: {cluster}",
        "cluster_role: member",
        "status: active",
        f"related: {related}",
        "created: 2026-05-21",
        "updated: 2026-05-25",
        "tier: public",
        "---",
        "",
    ])


def make_related(filepath: Path) -> str:
    siblings = sibling_pages(filepath)
    parent = parent_topic_link(filepath)
    parent_dir_name = filepath.parent.name
    lines = ["", "## Related", ""]

    for _, stem in siblings:
        lines.append(f"- [{stem}]({stem}.md) — sibling workspace doc in `{parent_dir_name}/`")

    if parent:
        label, path = parent
        lines.append(f"- [{label}]({path}) — parent topic this workspace contributes to")

    lines.append("")
    return "\n".join(lines)


def process(filepath: Path) -> str:
    content = filepath.read_text(encoding="utf-8")
    if content.startswith("---\n") or content.startswith("---\r\n"):
        return "skip_has_fm"

    body = content.lstrip()
    body = re.sub(r"^<!--.*?-->\s*", "", body, flags=re.DOTALL)
    body = body.lstrip()

    fm = make_frontmatter(filepath, content)
    related = make_related(filepath)

    final = fm + body
    if not final.endswith("\n"):
        final += "\n"
    final += related
    filepath.write_text(final, encoding="utf-8")
    return "ok"


def main():
    results = {}
    for f in WORKSPACE_FILES:
        p = Path(f)
        if not p.exists():
            results[f] = "missing"
            continue
        results[f] = process(p)

    ok = sum(1 for v in results.values() if v == "ok")
    skip = sum(1 for v in results.values() if v == "skip_has_fm")
    missing = sum(1 for v in results.values() if v == "missing")
    print(f"Processed: {ok} added, {skip} already had frontmatter, {missing} missing")
    for f, r in results.items():
        if r != "ok":
            print(f"  [{r}] {f}")


if __name__ == "__main__":
    main()
