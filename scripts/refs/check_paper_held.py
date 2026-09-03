# 논문이 캐시에 있는지 두 이름 규칙(bibcode / arXiv id)과 하위폴더까지 보고 판정하는 도구
"""Answer "is this paper in the cache?" without producing a false absence.

    python3 scripts/refs/check_paper_held.py 2004GeoJI.156..363N 2022A&A...661A.101R
    python3 scripts/refs/check_paper_held.py --scan docs/reference/*.md engine/*.md

Why this exists: `docs/phase3/_papers/` files are named EITHER by bibcode
(2013JChPh.138w4504B.pdf) OR by bare arXiv number (2203.01065.md), and some live in
subdirectories (militzer2024_zenodo/). A glob on the bibcode prefix alone reported
RM22, Reiners & Christensen, Yadav & Thorngren, Garraffo and Zhang & Rogers as absent
when all five are held. Three separate sessions hit this on 2026-09-03/04.

The arXiv id is READ from the ADS `identifier` field, never constructed.
Needs ADS_API_TOKEN. Exit status 1 if any queried paper is absent.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.parse
import urllib.request

# 리포 루트를 스크립트 위치에서 되짚는다 — 어느 디렉터리에서 실행해도 같은 캐시를 본다.
CACHE = os.environ.get("NEARSTARS_PAPERS") or os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "docs", "phase3", "_papers")
BIBCODE = re.compile(r"\b\d{4}[A-Za-z&][A-Za-z&.]{1,6}[0-9A-Za-z.]{0,8}\.{1,4}[0-9]{1,4}[A-Z]\b")
ARXIV = re.compile(r"\b\d{4}\.\d{4,5}\b")
STRIP = re.compile(r"\.(pdf|txt|src|md|json|html|xml|ps|eps|zip)$")


def cache_names(root: str = CACHE) -> set[str]:
    """Every base name the cache holds — files and directories, all levels."""
    if not os.path.isdir(root):
        sys.exit(f"paper cache not found at {root} — set NEARSTARS_PAPERS if it lives elsewhere.")
    names = set()
    for dirpath, dirnames, filenames in os.walk(root):
        for name in list(filenames) + list(dirnames):
            names.add(STRIP.sub("", name).removesuffix(".PROVENANCE"))
    return names


def ads_identifiers(bibcodes: list[str]) -> dict[str, list[str]]:
    """bibcode -> the arXiv ids ADS lists for it. Read, not constructed."""
    token = os.environ.get("ADS_API_TOKEN")
    if not token:
        sys.exit("ADS_API_TOKEN is not set — cannot resolve arXiv ids, and guessing them is the bug this tool exists to prevent.")
    out: dict[str, list[str]] = {}
    for i in range(0, len(bibcodes), 20):
        chunk = bibcodes[i:i + 20]
        url = "https://api.adsabs.harvard.edu/v1/search/query?" + urllib.parse.urlencode(
            {"q": " OR ".join(f'bibcode:"{b}"' for b in chunk), "fl": "bibcode,identifier", "rows": len(chunk)})
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        for doc in json.load(urllib.request.urlopen(req))["response"]["docs"]:
            found = [m.group(0) for ident in doc.get("identifier", [])
                     if (m := ARXIV.search(ident))]
            out[doc["bibcode"]] = sorted(set(found))
    return out


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] == "--scan":
        wanted: set[str] = set()
        for path in argv[2:]:
            wanted |= set(BIBCODE.findall(open(path, encoding="utf-8", errors="replace").read()))
        bibcodes = sorted(wanted)
    else:
        bibcodes = argv[1:]
    if not bibcodes:
        return int(bool(sys.stderr.write(__doc__ or "")))

    names = cache_names()
    arxiv = ads_identifiers(bibcodes)
    missing = 0
    for b in bibcodes:
        candidates = [b] + arxiv.get(b, [])
        held = [c for c in candidates if c in names]
        if held:
            how = "bibcode" if held[0] == b else f"arXiv {held[0]}"
            print(f"HELD    {b}  (as {how})")
        else:
            missing += 1
            print(f"ABSENT  {b}  (checked {', '.join(candidates)})")
    print(f"\n{len(bibcodes) - missing}/{len(bibcodes)} held, {missing} absent — cache index {len(names)} names.")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
