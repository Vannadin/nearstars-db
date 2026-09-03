<!-- Brief 49 — ar5iv HTML→markdown 추출기가 표를 잃는 세 원인(최상위 float·부록·캡션 미출력)의 진단·수리·재생성 기록 -->
# The paper extractor lost tables — diagnosis, repair, regeneration (Brief 49, context notes)

2026-09-03. **§1–§2 are the pre-registration and were committed before the fix.** Verifiers: (직) directing
seat (traced causes ① and ②, patched and measured them), (여기) work seat (found cause ③, ran the survey).

## 1. Three causes, two of them the directing seat's and one that was not a loss at all

`scripts/phase3/fetch_arxiv_texts.py::html_to_markdown` walks
`article.find_all(class_=["ltx_section","ltx_subsection","ltx_subsubsection"])` and then iterates
**`sec.children`** — direct children only. A `figure.ltx_table` float is emitted only if its immediate
parent is one of those three classes. Reproduced (여기) by printing every table float's ancestor chain:

- **① Article-level floats.** `0707.2895` (Seager+ 2007) puts all four tables directly under
  `article.ltx_document` — no walked ancestor at all. **This is the paper `eos.py`'s `fe_eps` and
  `mgsio3_en` fits come from**; eight of eleven values `eos.py` carries from its Table 1 are absent from
  the `.md` (Brief 48). The transcription itself is correct — read from the html or the PDF.
- **② Appendices.** `ltx_appendix` is not in the class list. `2203.01065` (RM22) keeps Tables 1–6 (in
  subsections) and loses **7–10**, all under `section.ltx_appendix` — Table 8 is the rocky-dynamo ladder's
  anchor table (Brief 47 read it from the html).
- **③ Captions are never emitted for tables, anywhere.** `_format_table` formats rows only; the float's
  `ltx_caption` is dropped (figures get theirs via `_format_figure`, tables do not). Across the whole cache
  only 11 of 1588 `.md` files contain "Table N:" — prose mentions. **So Zhang & Rogers (`2208.06523`) was
  never a loss**: its five tables are direct children of walked sections and their bodies are in the `.md`
  (Table 1's `| Fe | 40 …` rows, Table 5's `| Spin-polarized … 1.754 × 10⁹` rows); only the captions are
  missing. The directing seat's "third cause" is this, and it also means **Brief 48's caption-parity signal
  measured caption absence, not body absence** — RM22 showed all ten "missing" while 1–6 were present.

The directing seat's patch (walk `ltx_appendix`; after the section pass emit any `ltx_table` float whose
parent was not walked) recovered Seager 75,610 → 78,732 chars (4 tables, `156.2` back) and RM22
74,456 → 90,279 chars (4 tables, `0.0007` back). No network: the HTML is cached and re-extraction is
the script's own documented cheap path.

## 2. What is built, and the pre-registration

1. **Walker**: add `ltx_appendix` to the walked classes; after the pass, emit every `ltx_table` float not
   already emitted. **Double-emission guard = identity**: floats emitted during the section pass are
   recorded in a set (by `id()`), and the sweep skips them — an invariant on the objects themselves, not
   on the parent's class.
2. **Captions**: emit the float's `ltx_caption` as a `**Table N: …**` line before the body, so the `.md`
   carries what the html says the table is. One line per table — the ④ noise question is measured after.
3. **Regenerate** every `.md` from its cached `.html` (all 1588 backed up to the scratchpad first), then
   re-run `scripts/check_paper_tables.py` and report before/after. **Because captions now exist, the
   caption-parity signal becomes what it was meant to be**; the density signal stays.
4. **③ spot-check before declaring success**: the recovered Seager Table 1 against `eos.py`'s eleven values
   (156.2, 8300, 6.08 for `fe_eps`; 3220, 125, 5.0 for `mgsio3_en`; 4100, 247, 3.97, −0.016 for
   `mgsio3_pv`; 1460, 23.7, 4.15 for ice VII), and RM22's recovered Table 8 against the Brief 47 note.
5. **Downgrade the Brief 48 rule** to a fallback with the history; keep the Seager case as the evidence.

**Branches**: ① both causes fixed and the report's rows drop sharply; ② rows drop but a residue remains →
name its shape; ③ regeneration changes a `.md` a value was read from **in a way that contradicts the
code** → **stops everything**; ④ recovered tables make the `.md` worse to read → say so and reconsider.

**Expectation (여기)**: ① fires — the article-level and appendix losses are the whole of the body loss on
the cited set, so the density-signal rows (four) and the true body losses vanish, and with captions emitted
the caption signal drops to zero on the cited set except where the html itself lacks a caption. ③ does not
fire: Seager's values were read from the html that the recovered table is generated from. ④ marginal: one
bold line per table, and the tables themselves were already there for most papers. Residue (②) possible
where a float sits under a class none of us has seen yet — reported if found.

## 3. Result — filled after the run

*(pending)*
