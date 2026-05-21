# Phase 3 bibliography YAML → ar5iv HTML 다운로드 + 텍스트 추출 (멱등)
"""Fetch ar5iv HTML for each arxiv-bearing paper in a bibliography YAML.

For each `pending` paper with an arxiv_id:
  1. Download https://ar5iv.labs.arxiv.org/html/<arxiv_id>
  2. Save raw HTML to docs/phase3/_papers/<arxiv_id>.html
  3. Extract markdown-ish text via BeautifulSoup, save to <arxiv_id>.md
  4. Update YAML: status → fetched (or failed with reason)

Idempotent: if HTML file already exists, the network fetch is skipped;
the markdown is re-extracted (cheap). Use --retry-failed to retry
previously-failed papers.

Usage:
  python3 scripts/phase3/fetch_arxiv_texts.py docs/phase3/_bib/trappist-1d.yaml
  python3 scripts/phase3/fetch_arxiv_texts.py docs/phase3/_bib/trappist-1d.yaml --retry-failed
  python3 scripts/phase3/fetch_arxiv_texts.py docs/phase3/_bib/trappist-1d.yaml --limit 5
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import urllib.error
import urllib.request

import yaml
from bs4 import BeautifulSoup, NavigableString, Tag


BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAPERS_DIR = os.path.join(BASE, "docs", "phase3", "_papers")

AR5IV_URL = "https://ar5iv.labs.arxiv.org/html/{}"

# ar5iv 는 자체 rate limit 명시 없으나 정중함 차원에서 2초 간격.
FETCH_SLEEP_S = 2.0


# ── network ──────────────────────────────────────────────────────────────────

def fetch_ar5iv(arxiv_id: str, timeout: int = 60) -> str:
    """ar5iv HTML 다운로드. UA 헤더 포함."""
    url = AR5IV_URL.format(arxiv_id)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "NearStars-Phase3-Fetcher/1.0 (research)"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


# ── HTML → markdown ──────────────────────────────────────────────────────────

def _is_skip_class(tag: Tag) -> bool:
    """ar5iv 의 navigation/footer/bibliography 영역은 건너뜀."""
    if not isinstance(tag, Tag):
        return False
    cls = tag.get("class") or []
    if any(c in cls for c in ("ltx_bibliography", "ltx_pagination",
                              "ltx_note_outer", "ltx_navigation",
                              "ar5iv-footer", "ar5iv-toc")):
        return True
    return False


def _text_only(node) -> str:
    """텍스트만 추출, 공백 정리."""
    if node is None:
        return ""
    t = node.get_text(" ", strip=True) if isinstance(node, Tag) else str(node)
    return " ".join(t.split())


def _format_table(tag: Tag) -> str:
    """HTML table → 간이 markdown table. 복잡한 cell 은 텍스트만 추출."""
    rows = []
    for tr in tag.find_all("tr"):
        cells = [_text_only(c) for c in tr.find_all(["th", "td"])]
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    md = []
    md.append("| " + " | ".join(rows[0]) + " |")
    md.append("|" + "|".join(["---"] * width) + "|")
    for r in rows[1:]:
        md.append("| " + " | ".join(r) + " |")
    return "\n".join(md)


def _format_figure(tag: Tag) -> str:
    """figure 의 caption 만 추출 (이미지 자체는 못 봄)."""
    cap = tag.find("figcaption")
    if cap:
        return f"**Figure (caption):** {_text_only(cap)}"
    return ""


def html_to_markdown(html: str) -> str:
    """ar5iv HTML → 간이 markdown.
    제목/섹션 헤더/문단/표/figure-caption 추출. 수식은 LaTeX 보존 (ar5iv 가
    `\\(...\\)` 형태로 마크함). 참고문헌은 건너뜀."""
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("article") or soup.find("body") or soup

    out: list[str] = []

    # 제목
    title = soup.find("h1", class_="ltx_title_document") or soup.find("h1")
    if title:
        out.append(f"# {_text_only(title)}\n")

    # 저자
    authors = soup.find("div", class_="ltx_authors")
    if authors:
        out.append(f"*{_text_only(authors)}*\n")

    # 초록
    abstract = soup.find(class_="ltx_abstract")
    if abstract:
        out.append("## Abstract\n")
        for p in abstract.find_all(class_="ltx_p"):
            out.append(_text_only(p) + "\n")

    # 본문: 섹션 단위로 walk
    for sec in article.find_all(class_=["ltx_section", "ltx_subsection",
                                         "ltx_subsubsection"], recursive=True):
        if _is_skip_class(sec):
            continue
        # 헤더 레벨
        if "ltx_subsubsection" in sec.get("class", []):
            level = "### "
        elif "ltx_subsection" in sec.get("class", []):
            level = "## "
        else:
            level = "## "
        head = sec.find(class_=["ltx_title_section", "ltx_title_subsection",
                                 "ltx_title_subsubsection"])
        if head:
            out.append(f"\n{level}{_text_only(head)}\n")

        # 섹션 내 콘텐츠 walk — 단, 중첩 subsection 헤더는 위에서 따로 처리하므로
        # 여기서는 같은 섹션의 paragraphs/tables/figures 만.
        for child in sec.children:
            if not isinstance(child, Tag):
                continue
            if _is_skip_class(child):
                continue
            cls = child.get("class") or []
            if "ltx_para" in cls:
                for p in child.find_all(class_="ltx_p"):
                    out.append(_text_only(p) + "\n")
            elif child.name == "table" or "ltx_table" in cls:
                md = _format_table(child if child.name == "table"
                                   else child.find("table") or child)
                if md:
                    out.append("\n" + md + "\n")
            elif child.name == "figure" or "ltx_figure" in cls:
                cap = _format_figure(child)
                if cap:
                    out.append("\n" + cap + "\n")

    text = "\n".join(out)
    # 공백 정리: 연속 빈 줄 1개로
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text.strip() + "\n"


# ── main loop ────────────────────────────────────────────────────────────────

def process_paper(paper: dict, html_dir: str, md_dir: str, force_refetch: bool) -> tuple[str, str | None]:
    """단일 paper 처리. Returns (new_status, error_or_none)."""
    arxiv_id = paper.get("arxiv_id")
    if not arxiv_id:
        return ("skipped", "no_arxiv_id")

    safe_id = arxiv_id.replace("/", "_")
    html_path = os.path.join(html_dir, f"{safe_id}.html")
    md_path   = os.path.join(md_dir,   f"{safe_id}.md")

    if not force_refetch and os.path.exists(html_path):
        # Skip network; re-extract markdown if missing
        if not os.path.exists(md_path):
            with open(html_path) as f:
                html = f.read()
            with open(md_path, "w") as f:
                f.write(html_to_markdown(html))
        return ("fetched", None)

    try:
        html = fetch_ar5iv(arxiv_id)
    except urllib.error.HTTPError as e:
        return ("failed", f"http_{e.code}")
    except urllib.error.URLError as e:
        return ("failed", f"url_error: {e.reason}")
    except Exception as e:
        return ("failed", f"{type(e).__name__}: {e}")

    # 일부 ar5iv 페이지는 200 OK 인데 내용이 "could not be processed" 안내문.
    if "could not be processed" in html.lower() or "not yet available" in html.lower():
        return ("failed", "ar5iv_processing_unavailable")

    with open(html_path, "w") as f:
        f.write(html)
    try:
        md = html_to_markdown(html)
    except Exception as e:
        return ("failed", f"parse_error: {type(e).__name__}: {e}")

    with open(md_path, "w") as f:
        f.write(md)
    return ("fetched", None)


def main():
    parser = argparse.ArgumentParser(description="Fetch ar5iv text for bibliography papers.")
    parser.add_argument("bibliography", help="Path to YAML produced by build_bibliography.py")
    parser.add_argument("--retry-failed", action="store_true",
                        help="Re-fetch papers previously marked as failed")
    parser.add_argument("--limit", type=int, default=None,
                        help="Stop after N fetches (debug)")
    parser.add_argument("--force-refetch", action="store_true",
                        help="Refetch even if HTML on disk exists")
    args = parser.parse_args()

    with open(args.bibliography) as f:
        data = yaml.safe_load(f)

    papers = data.get("papers", [])
    os.makedirs(PAPERS_DIR, exist_ok=True)
    html_dir = md_dir = PAPERS_DIR

    n_fetched = n_failed = n_skipped = n_already = 0
    fetched_this_run = 0

    for i, paper in enumerate(papers):
        cur = paper.get("status", "pending")

        # 처리 대상 결정
        if cur == "fetched" and not args.force_refetch:
            n_already += 1
            continue
        if cur == "failed" and not args.retry_failed:
            n_failed += 1
            continue
        if cur == "skipped":
            n_skipped += 1
            continue

        # rate limit (이미 disk 에 있어 network skip 인 경우는 sleep 불필요)
        arxiv_id = paper.get("arxiv_id")
        safe_id = (arxiv_id or "").replace("/", "_")
        will_hit_network = (not args.force_refetch and arxiv_id and
                            not os.path.exists(os.path.join(html_dir, f"{safe_id}.html")))
        if will_hit_network and fetched_this_run > 0:
            time.sleep(FETCH_SLEEP_S)

        title = (paper.get("title") or "")[:80]
        print(f"  [{i+1}/{len(papers)}] {arxiv_id or '(no arxiv)':<18} {title}")

        status, err = process_paper(paper, html_dir, md_dir, args.force_refetch)
        paper["status"] = status
        paper["fetch_error"] = err
        if status == "fetched":
            n_fetched += 1
            if will_hit_network:
                fetched_this_run += 1
        elif status == "failed":
            n_failed += 1
            print(f"      [FAIL] {err}", file=sys.stderr)
        elif status == "skipped":
            n_skipped += 1

        if args.limit and fetched_this_run >= args.limit:
            print(f"\n  --limit {args.limit} reached; stopping.")
            break

    # save updated YAML
    with open(args.bibliography, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True, width=120)

    print(f"\n[Phase 3] Done.")
    print(f"  Fetched (this run + previously): {n_fetched + n_already}")
    print(f"  Failed: {n_failed}   Skipped (no arxiv): {n_skipped}")
    print(f"  Papers: {PAPERS_DIR}")
    print(f"  Bibliography updated: {args.bibliography}")


if __name__ == "__main__":
    main()
