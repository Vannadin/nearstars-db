# Phase 3 논문 점수 채점기 — authority(권위) + relevance(관련성) → 임계값 이하 자동 skip
"""Score and filter Phase 3 bibliography papers.

Why: Pure ADS+arXiv keyword search returns conference abstracts,
proposals, instrument papers, and references-to-tangential-work alongside
high-authority observation and modeling papers. Manual triage scales
poorly past ~50 papers. After citation-graph expansion the bibs grow
to ~1000+ entries each, requiring a programmatic filter.

This script annotates each paper in a bibliography with:
  - authority_score   (journal/venue quality, 0–10)
  - relevance_score   (planet/system topical relevance, 0–10)
  - combined_score    (sum, 0–20)
  - filter_decision   ("keep" | "skip" | "borderline")
  - filter_reason     (string explanation)

Then optionally writes a `filtered_papers` array containing just the
kept entries (the full `papers` array is preserved for audit).

Usage:
  python3 scripts/phase3/score_papers.py docs/phase3/_bib/trappist-1-d.yaml
  python3 scripts/phase3/score_papers.py docs/phase3/_bib/trappist-1-d.yaml \
      --keep-threshold 8 --planet "TRAPPIST-1 d"

Score is deterministic: runs offline against bib metadata, no API calls.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

# ────────────────────────────────────────────────────────────────────
# Authority scoring — venue + access + version cues
# ────────────────────────────────────────────────────────────────────

# Top-tier exoplanet journals (peer-reviewed). bibcode segment match.
TOP_JOURNALS = {
    "Nature": 5,
    "NatAs":  5,  # Nature Astronomy
    "Sci":    5,
    "PNAS":   4,
    "ApJ":    4,
    "ApJL":   4,
    "A&A":    4,
    "A&AL":   4,
    "PSJ":    4,
    "AJ":     4,
    "AJL":    4,
    "MNRAS":  4,
    "MNRASL": 4,
    "Icar":   3,
    "JGRE":   3,
    "EPSL":   3,
    "GeCoA":  3,
    "AsBio":  3,
    "PASP":   3,
    "PASA":   3,
    "P&SS":   2,
    "AcAau":  2,
}

# Conference proceedings / abstracts — lower authority but still cite
CONFERENCE_VENUES = {
    "epsc.conf": -3, "EPSC":   -3,
    "EGUGA":     -3,
    "AGUFM":     -3,
    "DPS":       -3,
    "BAAS":      -3,
    "AAS":       -3,
    "IAU":       -2,
    "EAS":       -3,
    "AbSciCon":  -3,
    "absc.conf": -3,
    "ESS":       -3,  # AAS Earth & Sky meeting abstracts
}

PROPOSAL_PATTERNS = ["prop", "jwst.prop", "hst.prop", "xrp", "GO-", "GTO-"]
DATA_CATALOG_PATTERNS = ["yCat", "VizieR", "zndo", "Online Data Catalog"]
RETRACTION_KEYWORDS = ["Erratum", "Retraction", "retracted"]


def score_authority(p: dict) -> tuple[int, str]:
    """Return (score 0-10, reason string). Default if no signal: 3 (neutral)."""
    bib = p.get("ads_bibcode") or ""
    doi = p.get("doi") or ""
    title = p.get("title") or ""
    reasons = []

    score = 3  # neutral baseline

    # Journal in bibcode (bibcode format: YYYYJOURN....VOLPAGE.A)
    journal_match = re.match(r"^\d{4}([A-Za-z&]+)", bib)
    if journal_match:
        jnl = journal_match.group(1)
        # Try to match longest prefix
        matched = None
        for jkey in sorted(TOP_JOURNALS, key=len, reverse=True):
            if jnl == jkey or bib.startswith(f"{bib[:4]}{jkey}"):
                matched = jkey
                break
        if matched:
            score += TOP_JOURNALS[matched]
            reasons.append(f"journal={matched}")

    # Conference / proceedings penalty
    for vkey, vpen in CONFERENCE_VENUES.items():
        if vkey in bib:
            score += vpen
            reasons.append(f"conf={vkey}")
            break

    # Proposal penalty
    for pkey in PROPOSAL_PATTERNS:
        if pkey in bib:
            score += -4
            reasons.append("proposal")
            break

    # Data catalog penalty
    for ckey in DATA_CATALOG_PATTERNS:
        if ckey in bib or ckey in title:
            score += -3
            reasons.append("data_catalog")
            break

    # Retraction / erratum penalty (still keep for context but lower)
    for rk in RETRACTION_KEYWORDS:
        if rk.lower() in title.lower():
            score += -2
            reasons.append("erratum")
            break

    # Has arxiv preprint → +2 (more reproducible, full text accessible)
    if p.get("arxiv_id"):
        score += 2
        reasons.append("has_arxiv")

    # Has DOI → small bonus (peer-reviewed indicator)
    if doi and not bib.lower().startswith("20") == False:  # always true; just check doi truthiness
        if doi:
            score += 1
            reasons.append("has_doi")

    # Clip to [0, 10]
    score = max(0, min(10, score))
    return score, ", ".join(reasons) or "neutral"


# ────────────────────────────────────────────────────────────────────
# Relevance scoring — planet / system topical fit
# ────────────────────────────────────────────────────────────────────

# Tokens that indicate strong topical relevance for terrestrial-rocky cfg work
RELEVANT_TOPICS = [
    r"\btidal\b", r"\binduction heating\b", r"\bspin[- ]orbit\b",
    r"\bobliquity\b", r"\beccentricit", r"\bresonan", r"\borbital stability\b",
    r"\batmosphere\b", r"\batmospheric\b", r"\bCO[_ ]?2\b", r"\bN[_ ]?2\b",
    r"\bO[_ ]?2\b", r"\bH[_ ]?2O\b", r"\bwater vapor\b", r"\bcloud\b",
    r"\bhaze\b", r"\baerosol\b", r"\bgreenhouse\b", r"\bclimate\b", r"\bGCM\b",
    r"\bradiative\b", r"\bphotochemi", r"\boutgassing\b", r"\bescape\b",
    r"\btransmission spectrum\b", r"\bemission spectrum\b",
    r"\beclipse depth\b", r"\bphase curve\b", r"\bdayside\b", r"\bnightside\b",
    r"\bequilibrium temperature\b", r"\bbrightness temperature\b", r"\balbedo\b",
    r"\bhabitable zone\b", r"\bhabitability\b", r"\btemperate\b", r"\bocean\b",
    r"\bsnowball\b", r"\baquaplanet\b", r"\bliquid water\b",
    r"\bsurface composition\b", r"\bmineralog", r"\bcrust\b", r"\bmantle\b",
    r"\bmagma ocean\b", r"\bvolcani", r"\btectonic\b", r"\bbedrock\b",
    r"\binterior structure\b", r"\bwater mass fraction\b", r"\bcore mass\b",
    r"\bdensity\b", r"\bmagnetic field\b", r"\bcosmic shoreline\b",
    r"\bM dwarf\b", r"\bM[- ]dwarf\b", r"\bultracool\b", r"\bUV\b", r"\bXUV\b",
    r"\bflare\b", r"\bsuperflare\b", r"\bstellar wind\b",
    r"\bmoon\b", r"\bsatellite\b", r"\bring\b",
]
RELEVANT_TOPICS_COMPILED = [re.compile(p, re.IGNORECASE) for p in RELEVANT_TOPICS]

# Skip patterns — papers about clearly-unrelated topics
SKIP_PATTERNS = [
    re.compile(r"\b(SETI|technosignature|narrowband signal|FAST telescope|fast radio burst|FRB)\b", re.IGNORECASE),
    re.compile(r"\bbiofluorescen", re.IGNORECASE),
    re.compile(r"\bmethyl chloride\b", re.IGNORECASE),
    re.compile(r"\bdetector noise\b", re.IGNORECASE),
    re.compile(r"\bnoise floor\b", re.IGNORECASE),
    re.compile(r"\binstrument\b.*\bperformance\b", re.IGNORECASE),
    re.compile(r"\bhot Jupiter\b", re.IGNORECASE),
    re.compile(r"\bgas giant\b", re.IGNORECASE),
    re.compile(r"\bsubgiant\b", re.IGNORECASE),
    re.compile(r"\bMini[- ]Neptune\b", re.IGNORECASE),
    re.compile(r"\bsub[- ]Neptune\b", re.IGNORECASE),
    re.compile(r"\bcosmic ray\b", re.IGNORECASE),
    re.compile(r"\btardigrade\b", re.IGNORECASE),
]

# Non-TRAPPIST systems mentioned as primary subject (heuristic — title-level)
OTHER_SYSTEM_PRIMARY = [
    re.compile(r"^(?!.*TRAPPIST).*\b(LHS\s?1140|GJ\s?1132|GJ\s?436|GJ\s?9827|"
               r"K2[- ]18|Proxima|Kepler[- ]?\d+|TOI[- ]\d+|HD\s?\d+|WASP[- ]?\d+|"
               r"55\s?Cnc|HR\s?\d+)\b", re.IGNORECASE),
]


def score_relevance(p: dict, planet_letter: str | None, system_name: str = "TRAPPIST-1") -> tuple[int, str]:
    """Return (score 0-10, reason). Planet-letter-specific match is rewarded most."""
    title = p.get("title") or ""
    abstract = p.get("abstract") or ""
    body = f"{title}  {abstract}"
    reasons = []
    score = 0

    # System name match in title (+4), in abstract (+2)
    if re.search(rf"\b{re.escape(system_name)}\b", title, re.IGNORECASE):
        score += 4
        reasons.append("sys_in_title")
    elif re.search(rf"\b{re.escape(system_name)}\b", abstract, re.IGNORECASE):
        score += 2
        reasons.append("sys_in_abstract")

    # Planet letter match in title (+5), in abstract (+3)
    if planet_letter:
        pat = rf"\b{re.escape(system_name)}[- ]?{planet_letter}\b"
        if re.search(pat, title, re.IGNORECASE):
            score += 5
            reasons.append(f"planet_{planet_letter}_in_title")
        elif re.search(pat, abstract, re.IGNORECASE):
            score += 3
            reasons.append(f"planet_{planet_letter}_in_abstract")

    # Topical keywords (cap at +3 contribution)
    topic_hits = sum(1 for r in RELEVANT_TOPICS_COMPILED if r.search(body))
    topic_bonus = min(3, topic_hits // 2)  # 2 hits = +1, 4 hits = +2, 6+ hits = +3
    if topic_bonus:
        score += topic_bonus
        reasons.append(f"topics={topic_hits}")

    # Skip patterns — strong negative
    for spat in SKIP_PATTERNS:
        if spat.search(body):
            score -= 5
            reasons.append(f"skip_pattern={spat.pattern[:30]}")
            break

    # Other system as primary subject (TRAPPIST not in title) — moderate negative
    for opat in OTHER_SYSTEM_PRIMARY:
        if opat.search(title):
            score -= 3
            reasons.append("other_system_primary")
            break

    score = max(0, min(10, score))
    return score, ", ".join(reasons) or "no_signal"


# ────────────────────────────────────────────────────────────────────
# Filter decision
# ────────────────────────────────────────────────────────────────────

def filter_decision(authority: int, relevance: int, threshold: int = 8) -> tuple[str, str]:
    """Combine scores into a keep/borderline/skip decision."""
    combined = authority + relevance
    if combined >= threshold + 2:
        return "keep", f"combined={combined}>={threshold+2}"
    elif combined >= threshold:
        return "borderline", f"combined={combined} (>= keep threshold {threshold} but <{threshold+2})"
    elif relevance == 0:
        return "skip", "no_relevance_signal"
    else:
        return "skip", f"combined={combined}<{threshold}"


# ────────────────────────────────────────────────────────────────────
# CLI
# ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Score and filter a Phase 3 bibliography.")
    parser.add_argument("bibliography", help="Path to a bib YAML")
    parser.add_argument("--planet", default=None,
                        help='Planet name e.g. "TRAPPIST-1 d" (auto-detected from bib if omitted)')
    parser.add_argument("--system", default="TRAPPIST-1",
                        help='System name (default TRAPPIST-1; auto-detected if --planet given)')
    parser.add_argument("--keep-threshold", type=int, default=8,
                        help="Combined-score threshold for 'keep' (default 8)")
    parser.add_argument("--mark-skipped-below", type=int, default=None, metavar="N",
                        help="After scoring, set status=skipped on pending papers "
                             "whose combined_score<N. Prevents fetch_arxiv_texts.py "
                             "from wasting API calls on low-tier papers. Typical N=14.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print summary, don't modify the YAML")
    args = parser.parse_args()

    path = Path(args.bibliography)
    if not path.exists():
        print(f"Not found: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path) as f:
        bib = yaml.safe_load(f)

    # Auto-detect planet from bib metadata if not given
    planet_name = args.planet or bib.get("planet") or ""
    # Extract planet letter (last token if single char)
    planet_letter = None
    tokens = planet_name.strip().split()
    if tokens and len(tokens[-1]) == 1 and tokens[-1].isalpha():
        planet_letter = tokens[-1].lower()
    system_name = args.system
    if planet_name and " " in planet_name:
        # e.g. "TRAPPIST-1 d" → system = "TRAPPIST-1"
        system_name = " ".join(tokens[:-1]) if planet_letter else planet_name

    print(f"[Phase 3] Scoring {path.name}")
    print(f"  system='{system_name}', planet_letter='{planet_letter or '(system-level)'}'")
    print(f"  keep_threshold={args.keep_threshold}")

    papers = bib.get("papers", []) or []
    counts = {"keep": 0, "borderline": 0, "skip": 0}
    for p in papers:
        a, ar = score_authority(p)
        r, rr = score_relevance(p, planet_letter, system_name)
        decision, dr = filter_decision(a, r, args.keep_threshold)
        p["authority_score"] = a
        p["relevance_score"] = r
        p["combined_score"] = a + r
        p["filter_decision"] = decision
        p["filter_reason"] = f"auth({ar}) + rel({rr}) → {dr}"
        counts[decision] += 1

    # Re-sort: keep > borderline > skip, then by combined_score desc
    rank = {"keep": 0, "borderline": 1, "skip": 2}
    papers.sort(key=lambda p: (rank.get(p["filter_decision"], 3), -p["combined_score"]))
    bib["papers"] = papers

    # Cache the kept set (preserves the audit trail of skipped)
    bib["filtered_papers"] = [p for p in papers if p["filter_decision"] in ("keep", "borderline")]

    # Optional: mark pending papers below a score threshold as skipped so
    # fetch_arxiv_texts.py doesn't waste arXiv API calls on them. Idempotent.
    marked = 0
    if args.mark_skipped_below is not None:
        thr = args.mark_skipped_below
        for p in papers:
            if p.get("status") == "pending" and p["combined_score"] < thr:
                p["status"] = "skipped"
                p["skip_reason"] = f"below_score_threshold ({p['combined_score']} < {thr})"
                marked += 1
        print(f"  marked-skipped-below {thr}: {marked} papers")

    total = len(papers)
    print(f"\n  Total: {total}")
    print(f"    keep:       {counts['keep']:5d}  ({100*counts['keep']/max(1,total):.1f}%)")
    print(f"    borderline: {counts['borderline']:5d}  ({100*counts['borderline']/max(1,total):.1f}%)")
    print(f"    skip:       {counts['skip']:5d}  ({100*counts['skip']/max(1,total):.1f}%)")

    if args.dry_run:
        print("\n[dry-run] not modified")
        return

    # Write back
    with open(path, "w") as f:
        yaml.safe_dump(bib, f, sort_keys=False, allow_unicode=True, width=140)
    print(f"  Saved → {path}")


if __name__ == "__main__":
    main()
