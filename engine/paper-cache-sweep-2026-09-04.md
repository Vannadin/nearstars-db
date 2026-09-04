<!-- check_paper_held.py 의 ABSENT 판정 21건 재조사 — 거짓 부재 6건과 캐시 명명 부류 표. 도구 수리는 오너 결정 대기, 노트만 — 원문 무편집 -->
<!-- Landed 2026-09-04 from the parallel seat's scratch (PAPER-CACHE-SWEEP.md), body unedited. Paths refer to the shared paper cache and the main checkout's scripts/refs/check_paper_held.py at that date. -->

# B. check_paper_held.py false-ABSENT sweep — the 21 ABSENT verdicts resolved
Parallel seat, 2026-09-04. Read-only. Cache = `/Users/vana/Desktop/NearStars/docs/phase3/_papers`
(1648 entries, 897 distinct stems, 8 subdirectories), listing snapshotted to `cache_ls.txt`.

Method: for each ABSENT bibcode, `ls -d * */*` grepped for author surname, year, journal
token, title keyword; plus a structural pass that enumerated **every** stem which is neither
a bibcode nor an arXiv id (80 stems) so nothing depends on my guessing the right keyword.

## Held, but the tool missed it — 6 of 21

| bibcode | file(s) on disk | naming class |
|---|---|---|
| `2010JGRA..11512220M` Mauk & Fox 2010 | `mauk_fox_2010_electron_belts.pdf` (+ `mauk_fox_2010.json`, `_mf2010_agu.html/.md`) | **descriptive** `author_year_topic` |
| `2009JGRA..11410210S` Summers, Tang & Thorne 2009 | `summers_tang_thorne_2009_kp_limit.pdf` | descriptive |
| `2014JGRA..119.6313S` Summers 2014 | `summers_2014_limiting_spectrum.pdf` | descriptive |
| `2021zndo...4782323M` Mauk & Fox Zenodo software | `mauk_fox_KP.nb`, `mauk_fox_KP_run.pdf`, `mauk_fox_KP_run.txt`, `mauk_fox_KP_doc.docx` | descriptive; the repo's own `kennel_petschek_recipe.md:11` names exactly these four files for this bibcode |
| `1997JGR...102.9497S` Shue 1997 | `_shue1997.pdf` / `.txt` | **underscore + author-year** |
| `1998JGR...10317691S` Shue 1998 | `_shue1998.pdf` / `.txt` | underscore + author-year |

Identity verified by opening the text, not by filename: `_shue1997.txt` line 1 = "JOURNAL OF
GEOPHYSICAL RESEARCH, VOL. 102, NO. A5, PAGES 9497-9511, MAY 1, 1997 / A new functional form
to study the solar wind control of the magnetopause size and shape"; `_shue1998.txt` line 1 =
"VOL. 103, NO. A8, PAGES 17,691-17,700, AUGUST 1, 1998 / Magnetopause location under extreme
solar wind conditions". Both match their bibcodes' volume/page fields exactly.

## Genuinely absent — 15 of 21

`1931TeMAE..36...77C` (Chapman & Ferraro 1931) · `1966JGR....71....1K` (Kennel & Petschek
1966) · `1961JGR....66.4027L` (Lenchek 1961) · `1974pdrb.book.....S` (Schulz & Lanzerotti
1974) · `1994JGR....9911043B` (Bagenal 1994) · `1983JGR....88.6889D` (Divine & Garrett 1983)
· `1983JGR....88.3945C` (Cooper 1983) · `2016GeoRL..43.5616R` (Ripoll 2016) ·
`2020JGRA..12526735R` (Ripoll 2020) · `2011SSRv..162..113B` (Bertucci 2011) ·
`1980JGR....85.7663B` (Brace 1980) · `2009JGRA..114.0B30M` (Martinecz 2009) ·
`1996Natur.384..537K` (Kivelson 1996) · `2013ApJ...776L..33H` (Heller & Zuluaga 2013, also
checked as arXiv 1309.0811 — the cache holds `1309.2631`, a different id) ·
`2024JGRA..12932193M` (Mourenas 2024).

`kennel_petschek_recipe.md` is the only near-hit for K&P 1966 and it is a **generated recipe
note that cites the paper** (its `:5` line quotes the bibcode), not the paper — correctly
ABSENT.

## What the repair needs to know: the naming classes actually present

The tool's docstring records three rules (bibcode; arXiv new/old with `/`→`_`; `&`→`_`) and
warns at `scripts/refs/check_paper_held.py:29-33` "DOUBT THAT THIS TOOL KNOWS EVERY CACHE
NAMING RULE". The structural pass found two more that produce false absences, plus three
suffix/subdir shapes that a naive stem match would also trip on:

| class | examples | affects the verdict? |
|---|---|---|
| **descriptive `author_year_topic`** | `mauk_fox_2010_electron_belts.pdf`, `summers_tang_thorne_2009_kp_limit.pdf`, `summers_2014_limiting_spectrum.pdf`, `kollmann2018.txt`, `kollmann2018_pmc.html`, `mauk_fox_KP.nb`, `mauk_uranus.json`, `roussos_sat.json` | **yes** — no bibcode anywhere in the name |
| **underscore + author-year** | `_shue1997`, `_shue1998`, `_winslow2013`, `_arridge2006`, `_kanani2010`, `_vignes2000`, `_fray2009`, `_roussos2022`, `_icegiant2020`, `_spp_review` | **yes** |
| underscore + arXiv id | `_2310.12382.pdf`, `_2410.10686.pdf`, `_astro-ph_0605240.pdf` | yes, unless the leading `_` is stripped |
| suffixed bibcode | `2020PhRvL.125s5501Q_SM.pdf` (supplementary), `2011PNAS..10817901M.SI.pdf` | only for the supplement, not the paper |
| subdirectory payload | `aqua/`, `chabrier_direos2019/`, `chabrier_direos2021/`, `militzer2024_zenodo/`, `2013JChPh.139m4505L.src/` | data archives, not papers |
| non-paper scratch JSON | `_batch_abs.json`, `_kp_citing.json`, `_kp_title.json`, `_relkp.json`, `_rk.json`, `pinned1.json`, `depater.json`, `earth_outer.json`, `jup_inner.json`, `jup_synch.json` | should NOT count as held |

A note for whoever repairs it: for the two classes that cause false absences there is no
name-derivable mapping back to a bibcode — `summers_2014_limiting_spectrum.pdf` cannot be
parsed into `2014JGRA..119.6313S`. So the fix has to be a **recorded mapping** (a sidecar
index, or a `PROVENANCE.txt` per descriptive file carrying its bibcode), not a smarter regex.
`kennel_petschek_recipe.md` is already exactly that mapping for four of the six, written by
hand — which is evidence the convention is reachable, and evidence it is not enforced.

## Scope note
This sweep covers only the 21 ABSENT verdicts from my 24-bibcode query on the magnetosphere
doc. Six other bibcodes that doc cites were never queried (`2010GeoRL..3722107T`,
`1979ITNS...26.4896S`, `1992STIN...9315580S`, `2016JGRE..121..871B`, `1989JGR....9411791K`,
`2024NatAs...8..596K`) and are not judged here.
