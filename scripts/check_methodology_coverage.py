# 방법론 문서가 영문 인덱스·한글 인덱스·GitHub 위키 포털 세 곳에 모두 등재됐는지 대조하는 게이트
"""Methodology registration gate.

A new recipe has to land in three places, and nothing so far noticed when it
did not:

1. `docs/reference/methodology-index.md`   (English index, canonical)
2. `ko/docs/reference/methodology-index.md` (Korean mirror)
3. the GitHub wiki's `Methodology-Library` / `-ko` portal

The mirror gate only checks that a *file* exists, so a mirror that silently
lists three fewer recipes than its English source passes it (found 2026-08-11:
KO listed 20 against EN's 23). The wiki lives in its own git repository
(`nearstars-db.wiki.git`) and sits outside every gate in this repo, so it had
stalled at 18 entries while the library grew to 28.

This compares the actual entry sets. The wiki half needs the network; when the
clone fails it warns and passes, so an offline `check.sh` still runs clean.
Use --no-wiki to skip that half deliberately.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EN_INDEX = REPO / "docs/reference/methodology-index.md"
KO_INDEX = REPO / "ko/docs/reference/methodology-index.md"
WIKI_URL = "https://github.com/Vannadin/nearstars-db.wiki.git"

ROW_LINK = re.compile(r"^\|\s*\[[^\]]+\]\(([a-z0-9-]+)\.md\)", re.M)
BULLET_LINK = re.compile(r"^-\s*\[[^\]]+\]\(([a-z0-9-]+)\.md\)", re.M)
WIKI_LINK = re.compile(r"blob/main/(?:ko/)?docs/reference/([a-z0-9-]+)\.md")


def sections(text):
    """Split a markdown doc into {h2 title: body}."""
    out, title, buf = {}, "", []
    for line in text.splitlines():
        if line.startswith("## "):
            out[title] = "\n".join(buf)
            title, buf = line[3:].strip(), []
        else:
            buf.append(line)
    out[title] = "\n".join(buf)
    return out


def index_entries(path):
    """Recipe slugs (table rows) and validation slugs (bullets), per index."""
    text = path.read_text(encoding="utf-8")
    recipes, validation = set(), set()
    for title, body in sections(text).items():
        low = title.lower()
        if low.startswith(("related", "관련")):
            continue
        if "validation" in low or "검증" in title:
            validation |= set(BULLET_LINK.findall(body))
        else:
            recipes |= set(ROW_LINK.findall(body))
    return recipes, validation


def fetch_wiki():
    """Shallow-clone the wiki; None when the network is unavailable."""
    tmp = tempfile.mkdtemp(prefix="nswiki-")
    r = subprocess.run(["git", "clone", "--depth", "1", "-q", WIKI_URL, tmp],
                       capture_output=True, text=True, timeout=90)
    if r.returncode != 0:
        return None
    return Path(tmp)


def main():
    errors, warnings = [], []

    en_recipes, en_validation = index_entries(EN_INDEX)
    ko_recipes, ko_validation = index_entries(KO_INDEX)

    # 1. index parity, in both directions
    for label, en, ko in (("recipe", en_recipes, ko_recipes),
                          ("validation", en_validation, ko_validation)):
        for slug in sorted(en - ko):
            errors.append(f"KO index is missing the {label} entry '{slug}' "
                          f"(ko/docs/reference/methodology-index.md)")
        for slug in sorted(ko - en):
            errors.append(f"KO index lists '{slug}' as a {label}, which the EN index does not")

    # 2. every methodology doc on disk is registered
    for f in sorted((REPO / "docs/reference").glob("*-methodology.md")):
        slug = f.stem
        if slug not in en_recipes | en_validation:
            errors.append(f"docs/reference/{slug}.md exists but no index row points at it")

    # 3. the wiki portal covers every recipe (extras there are fine)
    if "--no-wiki" in sys.argv:
        warnings.append("wiki portal check skipped (--no-wiki)")
    else:
        wiki = fetch_wiki()
        if wiki is None:
            warnings.append("wiki portal check skipped: cannot reach "
                            "nearstars-db.wiki.git (offline?)")
        else:
            for page in ("Methodology-Library.md", "Methodology-Library-ko.md"):
                p = wiki / page
                if not p.exists():
                    errors.append(f"wiki page {page} is gone")
                    continue
                listed = set(WIKI_LINK.findall(p.read_text(encoding="utf-8")))
                for slug in sorted(en_recipes - listed):
                    errors.append(f"wiki {page} does not link '{slug}'")

    n = len(en_recipes) + len(en_validation)
    for w in warnings:
        print(f"  [WARN] {w}")
    if errors:
        print(f"  [FAIL] methodology coverage: {len(errors)} gap(s) across {n} document(s):")
        for e in errors:
            print(f"    · {e}")
        return 1
    print(f"  [PASS] methodology coverage: {n} document(s) registered in EN index, "
          f"KO mirror, and the wiki portal")
    return 0


if __name__ == "__main__":
    sys.exit(main())
