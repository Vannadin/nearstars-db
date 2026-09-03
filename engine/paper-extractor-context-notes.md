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
3. **Regenerate** every `.md` from its cached `.html` (all 729 `.md` backed up to the scratchpad first), then
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

## 3. Result — 2026-09-03

**Branch ① fired, with a residue (②) of three rows and one incident that the pre-registration did not
foresee.** ③ did not fire. ④ did not fire.

**Fix** (`scripts/phase3/fetch_arxiv_texts.py`): `ltx_appendix` joins the walked classes; table floats are
emitted through `_format_table_float`, which puts the `ltx_caption` as a `**Table N: …**` line before the
body; floats emitted in the section pass are recorded by `id()` and a final sweep emits every `ltx_table`
float not in that set under a `## Tables not reached by the section walk` heading. Verified on the three
diagnostics before regenerating: Seager 75,610 → 80,103 chars, 4 captions, `156.2` / `8300` / `6.08` /
`3220` recovered; RM22 74,456 → 92,429, 10 captions, `0.0007` / `0.084` / Table 8 recovered; Zhang & Rogers
128,064 → 137,137, 5 captions (bodies were already there).

**③ spot-check — passed, so nothing stopped.** The recovered Seager Table 1 rows carry exactly what `eos.py`
carries: `Fe (ε) | 156.2 ± 1.8 | 6.08 ± 0.12 | 8.30 | V` (fe_eps: 8300, 156.2 GPa, 6.08);
`H₂O (ice VII) | 23.7 ± 0.9 | 4.15 ± 0.07 | 1.46 | BME`; `MgSiO₃ (en) | 125 | 5 | 3.22 | BME`;
`MgSiO₃ (pv) | 247 ± 4 | 3.97 | 4.10 | BME4`. RM22's recovered Table 8 rows match Brief 47's note digit for
digit (Mercury 0.0003 / 0.0004, Venus 0.0007 / 0, Mars 0.084 / 0.10, Ganymede 0.003 / 0.002).

**Regeneration, and the incident.** The first pass rewrote 576 of 714 `.md` files (557 grew, 9 shrank).
**Five of the nine shrank to 50 characters** — `1605.07211`, `1703.01424`, `1703.01430`, `2411.07922`,
`2510.11940`: their `.html` is an arxiv.org **abstract page** (ar5iv had failed) and their `.md` had been
**made by hand from the PDF** (header: *"PDF-extracted text (ar5iv render failed; extracted from
arxiv.org/pdf/… via pdftotext, 2026-05-30)"*). **Regeneration overwrote a person's work with a title line.**
Restored from the backup within the same session; then the whole cache was reconciled: **61 `.html` files
are not ar5iv renders** (abstract pages, search pages, the aanda bot page) and their `.md` files are never
regenerated; a first over-broad restore (matching the word "manual" anywhere) reverted 51 legitimate
renders, which were re-regenerated. **Final state against the backup: 510 `.md` changed (506 grew, 4 shrank),
53 manual/non-ar5iv files untouched.** The four that shrank (`2006.00500`, `2410.21856`, `2502.09186`,
`physics0305021`) lost only bibliography and acknowledgement text — the old files were whole-page dumps
from an earlier extractor, and the walker skips `ltx_bibliography` by design; their body prose and headers
are present. Accepted as ④-negative: the `.md` is better structured, not worse.

The two guards are now in the script as `--regenerate-md` (no network; skips non-ar5iv `.html`; skips a
`.md` whose head carries a manual-extraction signature) and the mode is idempotent: a second run reports
`rewritten 0, unchanged 653, skipped_non_ar5iv 61`.

**The deliverable — `scripts/check_paper_tables.py` before/after on the cited set: 46 rows → 3 rows.**
The three (② residue), read at source:
- `1707.06701` Table 1 — **false positive** of the density signal: the body is in the `.md` (42 rows); the
  html window counts math markup as numbers.
- `1802.09602` Table 2 — the html has **no `ltx_table` float at all**; the table is not marked as one
  (an image or an unclassed tabular), so no extractor can reach it. Residue shape: table not a float.
- `2301.04062` Table 11 — the float exists (appendix) but its `<table>` has **0 rows**; nothing to emit, and
  `_format_table_float` drops the caption when the body is empty. Residue shape: empty float.

**Brief 48's rule is downgraded** to a fallback with the history (handoff); the Seager case stays as the
evidence that made this worth fixing.

## 4. Audit of Brief 49 — 2026-09-03

**① The count was stale: 561 changed, not 510.** Reconciled against `md_backup_before_49` after the audit
(여기, 직 independently): identical 168 · grew 557 · shrank 4 · missing 0 → **561**. The 510 was taken
*before* the second pass that re-regenerated the 51 legitimate renders the over-broad restore had
reverted — exactly the 51 difference. The earlier figure stays in §3 as written; this is its correction.

**② Content, on three instruments, and the case that shows why one is not enough.** The audit's 6-gram
retention on 30 random changed files: min 0.996; the four shrinkers retain 73–81 % with 69–93 % of the
missing grams in the last 30 % of the text and every missing sentence a reference entry, DOI line or
acknowledgement — my reading holds. **`1906.05426`** (Io volcanism, AO observations) is the one to keep:
**size** says grew (146k → 172k), the audit's **6-gram** instrument said alarming (30 %, on a tokenisation
that carries math tokens; on word tokens here it is 0.99), and the **sentence** check says fine (audit 39 of
40 prose sentences, the miss a caption fragment; here 43 of 43 sampled). Three instruments, three answers;
the sentence check is the one that speaks to the question.

**③ The guard's invariant was backwards — inverted.** Both guards were negative tests for things that are
not ours ("not an ar5iv render", "smells manual"); a hand-written file that fails to smell would be
overwritten. Now the generator **stamps its own output** — first line
`<!-- generated by fetch_arxiv_texts.py from <id>.html, <date> -->` — and `--regenerate-md` **overwrites
only stamped files**; everything else is skipped and counted (`skipped_unstamped`). The two old guards stay
as belt-and-braces for files that predate the stamp. **The first stamped run did not overwrite content**: an
unstamped `.md` receives the stamp only if its body is **byte-identical** to the extractor's output for its
`.html` — proof that this extractor made it — and the run reported `stamped_identical 653, rewritten 0,
skipped_non_ar5iv 61`; the second run `unchanged 653`. Verified after: 653 stamped files, 0 whose body differs
from the extractor's output. The 61 non-ar5iv `.md` (five hand-made) remain unstamped and untouchable.

**④ Ledger, both instrument failures.** Directing seat: *"Zhang & Rogers lost all five tables"* — a
caption-parity count read as a body count; it never lost any. Audit seat: its first scan for ar5iv error
pages matched ordinary footer text and returned a dozen false hits, discarded unreported — *a regex without
its false-positive check is the same disease as a count without its rule.*

**Why the incident is a near-miss and not a loss.** Before the first regeneration I copied all 729 `.md`
files to the scratchpad. Five files that a person had written from PDFs on 2026-05-30 were overwritten with
a title line minutes later, and they came back because that copy existed. Not process hygiene — that
specific act saved that specific work.
