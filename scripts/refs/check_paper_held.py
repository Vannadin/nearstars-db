# 논문이 캐시에 있는지 두 이름 규칙(bibcode / arXiv id)과 하위폴더까지 보고 판정하는 도구
"""Answer "is this paper in the cache?" without producing a false absence.

    python3 scripts/refs/check_paper_held.py 2004GeoJI.156..363N 2022A&A...661A.101R
    python3 scripts/refs/check_paper_held.py --scan docs/reference/*.md engine/*.md
    python3 scripts/refs/check_paper_held.py --contradictions docs/reference/*.md engine/*.md

Why this exists: `docs/phase3/_papers/` files are named EITHER by bibcode
(2013JChPh.138w4504B.pdf) OR by bare arXiv number (2203.01065.md), and some live in
subdirectories (militzer2024_zenodo/). A glob on the bibcode prefix alone reported
RM22, Reiners & Christensen, Yadav & Thorngren, Garraffo and Zhang & Rogers as absent
when all five are held. Three separate sessions hit this on 2026-09-03/04.

The arXiv id is READ from the ADS `identifier` field, never constructed.
Needs ADS_API_TOKEN. Exit status 1 if any queried paper is absent or abstract-only.

Two defects of its own, found 2026-09-04 within hours of installation (recorded, not hidden):
- The first arXiv regex matched only new-style ids (2203.01065) and missed old-style ones
  (astro-ph/0103383, cached as astro-ph_0103383 — 52 such names). The tool built to stop
  false absences produced a false absence of its own, for the one paper needed that night
  (Burrows+ 2001). It was caught in thirty seconds ONLY because the ABSENT line prints what
  was checked ("checked 2001RvMP...73..719B" — one candidate, no arXiv id, was the clue).
  DO NOT change that output format; it is what makes this tool self-checking.
- "Held" meant "a file of that name exists". Three cached names (1004.1091, 1209.5323,
  1401.8145) are arXiv abstract pages (50-byte .md, .html without ltx_document), and a
  name whose only file is .PROVENANCE.txt would also have counted. A held paper must have a
  body: a .pdf, an .html carrying ltx_document, or an .md above BODY_MIN_BYTES. Otherwise
  the verdict is ABSTRACT-ONLY — a different state from ABSENT, calling for a different fix.
- Third naming trap (2026-09-04, later that day): bibcodes carrying '&' (2001E&PSL.185...49A)
  are cached with '&' -> '_' (2001E_PSL.185...49A.pdf, four such names), and the tool did not
  know that rule either. Generalised: DOUBT THAT THIS TOOL KNOWS EVERY CACHE NAMING RULE.
  Three rules surfaced in one day; when a paper you can see on disk comes back ABSENT, the
  "checked ..." list says which names were tried - compare it with `ls` before believing it.
  Seen but not folded in: 2020SciA_6_7467D uses '_' where a dot run would be - a different
  variant, recorded here, not guessed at.
- Fourth and fifth naming classes (2026-09-04 evening, parallel seat's sweep of 21 ABSENT verdicts,
  engine/paper-cache-sweep-2026-09-04.md): DESCRIPTIVE names (mauk_fox_2010_electron_belts.pdf,
  summers_2014_limiting_spectrum.pdf, mauk_fox_KP_run.pdf) and UNDERSCORE + AUTHOR-YEAR names
  (_shue1997.pdf, _shue1998.pdf). Six of the 21 ABSENT papers were on disk under such names. There
  is no regex from summers_2014_limiting_spectrum to 2014JGRA..119.6313S, so the fix is not a
  smarter pattern but a RECORDED MAPPING: the cache's existing *.PROVENANCE.txt sidecars carry a
  "bibcode  <id>" line (and an "arXiv  <id>" line), and this tool now reads them into an id -> base
  name index consulted after the name rules fail. Rule that follows: WHOEVER CACHES A PAPER UNDER A
  DESCRIPTIVE NAME LEAVES A <base>.PROVENANCE.txt BESIDE IT WITH A bibcode LINE - the sidecar is the
  mapping. HELD still requires a body under that base (a sidecar alone is SIDECAR-ONLY, the
  "name whose only file is .PROVENANCE.txt" case above, kept as its own state).
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
# 구형 arXiv id (astro-ph/0103383) — 캐시는 '/' 를 '_' 로 바꿔 저장한다.
ARXIV_OLD = re.compile(r"\b([a-z-]+(?:\.[A-Z]{2})?)/(\d{7})\b")
BODY_MIN_BYTES = 2000  # an arXiv abstract page saved as .md is ~50 bytes; a full text is tens of KB
STRIP = re.compile(r"\.(pdf|txt|src|md|json|html|xml|ps|eps|zip)$")
# 사이드카의 "bibcode  2009P&SS...57.2053F ..." / "arXiv    1908.10682 ..." 줄. NONE 은 매핑이 아니다.
SIDECAR_LINE = re.compile(r"^(bibcode|arxiv)\s+(\S+)", re.IGNORECASE)


def _has_body(path: str) -> bool:
    """A file counts as a body if it is a pdf, an html with LaTeXML's ltx_document, or an md above BODY_MIN_BYTES."""
    if path.endswith(".pdf"):
        return True
    if path.endswith(".html"):
        with open(path, "rb") as fh:
            return b"ltx_document" in fh.read()
    if path.endswith(".md"):
        return os.path.getsize(path) > BODY_MIN_BYTES
    return False


def cache_names(root: str = CACHE) -> dict[str, bool]:
    """Every base name the cache holds (files and directories, all levels) -> whether a body was found.

    A directory counts as a body (the zenodo bundles). A name whose only file is .PROVENANCE.txt
    is listed with False, never True."""
    if not os.path.isdir(root):
        sys.exit(f"paper cache not found at {root} — set NEARSTARS_PAPERS if it lives elsewhere.")
    names: dict[str, bool] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for name in dirnames:
            names[name] = True
        for name in filenames:
            if name.endswith(".PROVENANCE.txt"):
                base = name.removesuffix(".PROVENANCE.txt")
                names.setdefault(base, False)
                continue
            base = STRIP.sub("", name)
            names[base] = names.get(base, False) or _has_body(os.path.join(dirpath, name))
    return names


def sidecar_index(root: str = CACHE) -> dict[str, str]:
    """id (bibcode or arXiv, as written in a *.PROVENANCE.txt) -> the sidecar's base name.

    The recorded mapping for cache names that carry no bibcode. Read, never derived from the file name."""
    index: dict[str, str] = {}
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if not name.endswith(".PROVENANCE.txt"):
                continue
            base = name.removesuffix(".PROVENANCE.txt")
            with open(os.path.join(dirpath, name), encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    m = SIDECAR_LINE.match(line)
                    if not m or m.group(2).upper().startswith("NONE"):
                        continue
                    ident = m.group(2)
                    if m.group(1).lower() == "arxiv":
                        ident = ident.removeprefix("arXiv:").removeprefix("arxiv:")
                        if (n := ARXIV.search(ident)):
                            ident = n.group(0)
                        elif (n := ARXIV_OLD.search(ident)):
                            ident = f"{n.group(1)}_{n.group(2)}"
                        else:
                            continue
                    index.setdefault(ident, base)
    return index


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
            found = []
            for ident in doc.get("identifier", []):
                if (m := ARXIV.search(ident)):
                    found.append(m.group(0))
                elif (m := ARXIV_OLD.search(ident)):
                    found.append(f"{m.group(1)}_{m.group(2)}")
            out[doc["bibcode"]] = sorted(set(found))
    return out


# Words a document uses to say a paper cannot be read. If one of these sits within three lines of a
# bibcode the cache HOLDS, the document is telling its next reader not to look — which is worse than a
# wrong value, because a wrong value eventually fails a reproduction and "we do not have it" simply
# stops anyone checking. Twice in one day (2026-09-05) a batch of papers arrived and the sentences
# calling them unobtainable stayed behind, so the rule is now the tool's rather than a habit's.
DENIES = re.compile(r"paywall|no preprint|unobtained|not obtained|미보유|받지 못|구하지 못|blocked|"
                    r"cannot be obtained|second-hand only", re.I)


def contradictions(paths: list[str]) -> int:
    names, sidecars = cache_names(), sidecar_index()
    found = 0
    for path in paths:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
        for i, line in enumerate(lines):
            for b in BIBCODE.findall(line):
                cands = [b, b.replace("&", "_")] + ([sidecars.get(b)] if sidecars.get(b) else [])
                if not any(names.get(c) for c in cands if c):
                    continue
                near = "\n".join(lines[max(0, i - 3):i + 4])
                m = DENIES.search(near)
                if m:
                    found += 1
                    print(f"[HELD but called unobtainable] {path}:{i + 1}: {b} — "
                          f"the text says {m.group(0)!r} within three lines")
    print(f"{found} place(s) where a document calls a held paper unobtainable")
    return 1 if found else 0


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] == "--contradictions":
        return contradictions(argv[2:])
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
    sidecars = sidecar_index()
    arxiv = ads_identifiers(bibcodes)
    missing = 0
    for b in bibcodes:
        candidates = [b] + arxiv.get(b, [])
        if "&" in b:
            candidates.append(b.replace("&", "_"))  # cache convention: '&' in a file name is written '_' 
        held = [c for c in candidates if names.get(c)]
        shells = [c for c in candidates if c in names and not names[c]]
        if held:
            if held[0] == b:
                how = "bibcode"
            elif held[0] == b.replace("&", "_"):
                how = f"bibcode with & as _: {held[0]}"
            else:
                how = f"arXiv {held[0]}"
            print(f"HELD    {b}  (as {how})")
        elif shells:
            missing += 1
            how = "bibcode" if shells[0] == b else f"arXiv {shells[0]}"
            print(f"ABSTRACT-ONLY  {b}  (as {how}; no pdf, no ltx_document html, md ≤ {BODY_MIN_BYTES} B)")
        elif (via := [sidecars[c] for c in candidates if c in sidecars]):
            # 이름 규칙이 다 빗나간 뒤에만 본다 — 사이드카가 기록한 매핑. 본문 요구는 그대로.
            base = via[0]
            if names.get(base):
                print(f"HELD    {b}  (as {base}, via {base}.PROVENANCE.txt)")
            else:
                missing += 1
                print(f"SIDECAR-ONLY  {b}  (via {base}.PROVENANCE.txt; no body under that name)")
        else:
            missing += 1
            print(f"ABSENT  {b}  (checked {', '.join(candidates)})")
    print(f"\n{len(bibcodes) - missing}/{len(bibcodes)} held, {missing} absent or abstract-only — cache index {len(names)} names.")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
