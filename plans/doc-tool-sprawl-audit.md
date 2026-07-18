---
title: Doc / tool sprawl audit — findings + lifecycle-gate plan
status: promoted   # active | promoted | archived
created: 2026-06-03
promoted: 2026-07-19 → phase2/sprawl-lifecycle-gate/
---

# Doc / tool sprawl audit — findings + lifecycle-gate plan

> **Promoted 2026-07-19** to [`phase2/sprawl-lifecycle-gate/`](../phase2/sprawl-lifecycle-gate/plan.md)
> after a re-audit (F1 fixed, F3 partial, F4/F5/F7 + §2.4 + sprawl gate still open,
> plus new phase-convention divergence findings). This note is now historical context.

**NearStars connection.** Every session and every skill run spins off side
artifacts — working dirs (`phase3/<system>/`, `_recovered/`, `_audit/`),
scratch JSON/MD, one-off `scripts/refs/` population scripts, ground-truth
files, errata, manual-followup logs. This note audits whether those
artifacts are **systematically generated and managed** or merely accreting,
and scopes the fixes. It informs whether `scripts/check.sh` and `AGENTS.md`
need a lifecycle/cleanup rule. Raised as an idea 2026-06-03.

**Scope.** In: inventory of what gets created where (committed-canonical vs
scratch vs gitignored-regenerable vs orphaned), conformance to the
`AGENTS.md §2` four-home convention, and a concrete fix plan. Out:
implementing the fixes — this note is **not yet greenlit**; a future session
promotes it to `phase2/sprawl-lifecycle-gate/` when greenlit. One cleanup
(orphan scratch removal, see §2 F2) was already executed in the audit
session; everything else is pending.

**External references.** None — internal audit. Anchors:
[`AGENTS.md §2`](../AGENTS.md), [`scripts/check.sh`](../scripts/check.sh),
[`docs/reference/tools.md`](../docs/reference/tools.md). Related memory:
`project-doc-tool-sprawl-audit`, `reference-check-command`,
`project-naming-canonical`.

---

## 1. Executive summary

| Question | Answer |
|----------|--------|
| Is artifact creation systematic or sprawling? | **Systematic by design, sprawling at the edges.** The four-home + ko-mirror + 7-gate system is real and mostly holds (mirrors 90/90, dead-links 0, schema PASS). |
| Where is the real gap? | **Lifecycle, not location.** Conventions govern *where new things go*, not *when scratch is reaped or promoted*. |
| Worst single finding? | **F1 — a rotted guardrail.** `check.sh` gate 5 has been failing on a stale false-positive, training everyone to ignore the red line. |
| What's already fixed? | **F2 orphan scratch** — 5 dead dirs deleted in the audit session (empty dirs + `_recovered/`). |
| What's the fix shape? | One quick gate-5 repair + one new sprawl/orphan gate + one `AGENTS.md §2.4` lifecycle rule + tool-index backfill. |

---

## 2. Findings (severity order)

Evidence captured 2026-06-03 via `git ls-files` / `git status` / `bash
scripts/check.sh`. Counts are reproducible.

### F1 — Rotted guardrail: `check.sh` gate 5 is red [HIGH]

Gate 5 ("경로 마이그레이션 잔여물") greps tracked file *contents* for the
pattern `alpha-cen-proxima-system|trappist-1-system|docs/wiki|llm-wiki|skills-lock`.
The `docs/wiki` token now matches [`scripts/build_docs.py`](../scripts/build_docs.py),
which **legitimately generates** `docs/wiki/` (17 rendered HTML files; the
wiki was re-introduced post-LLM-wiki-rollback and is actively maintained —
last touched commit `9df6ae3`, 2026-05-31). So the gate false-positives on
its own generator and `check.sh` exits non-zero every run. A guardrail that
is always red is worse than none — the "일부 점검 실패" line gets ignored.

**Fix.** Drop `docs/wiki` from the gate-5 pattern (the migrated-away path
was the *old flattened* form, not the live `docs/wiki/` render). Verify
`bash scripts/check.sh` exits 0 afterward.

### F2 — Orphaned scratch dirs after output is committed [MEDIUM] — *cleanup done*

6 `phase3/<system>/` working dirs were pure local scratch (0 tracked files)
while their committed output (`docs/phase3/*.html` + `.md` + `_bib/*.yaml`)
already existed. **Deleted in the audit session** (all untracked → no git
impact):

- empty dirs: `phase3/55_cnc/`, `phase3/yz_cet/`, `phase2/disk-vertical-structure/`
- recovery leftovers: `phase3/barnards_star/_recovered/` (12 files),
  `phase3/teegardens_star/_recovered/` (9 files) + their `.DS_Store`

**Preserved** (not orphans — these are stranded decision logs, see F3):
`phase3/eps_ind_a/context-notes.md`, `phase3/hd_219134/context-notes.md`.

The residual risk is recurrence — nothing *prevents* the next session from
re-littering. That is what the F-fix gate (§3.2) addresses.

### F3 — Inconsistent trio-commit lifecycle [MEDIUM]

`AGENTS.md §2` says `phase3/<system>/` carries the trio
(plan + checklist + context-notes), same as `phase2/`. In practice the
commit decision is ad-hoc: some dirs commit it (`trappist_1`=10 files,
`stability-sim`=16, `au_mic`=3, `vega`=3, `61_vir`=3), others never do
(`eps_ind_a` / `hd_219134` have only an *untracked* `context-notes.md`;
`55_cnc` / `yz_cet` were empty). So "where is this synthesis's decision
log?" has a different answer per system. No rule says when a working dir is
committed (as the decision log) vs discarded.

**Decision needed:** for the 2 preserved context-notes — commit them (per
the proposed §2.4 rule, the decision log is the artifact worth keeping) or
delete. Recommend **commit**: they hold append-only synthesis reasoning more
detailed than the rendered report.

### F4 — Un-indexed one-off scripts in `scripts/refs/` [MEDIUM]

7 of 10 `scripts/refs/*.py` are **absent from
[`docs/reference/tools.md`](../docs/reference/tools.md)**, violating the
"index every new tool" rule (memory `feedback-tools-lookup`):
`build_molecular_db`, `migrate_element_db_v2`, `populate_phosphor_emission`,
`populate_reentry_aurora`, `populate_spectro_refinements`,
`populate_tier_c_upgrades`, `wavelength_to_rgb`. (Indexed: `render_element_colors_doc`,
`validate_element_colors`, `build_plasma_temperature_colors`.) These are
mostly one-shot DB-population / migration scripts whose output YAML is
committed; the script then lingers with no index entry and no
re-runnable-vs-single-use marker.

**Fix.** Backfill the 7 `tools.md` lines (+ ko mirror), and add a one-line
`# one-shot:` / `# regenerable:` header convention so single-use migrations
are distinguishable from re-runnable builders.

### F5 — Mixed scratch + canonical, no lifecycle marker [LOW]

`phase3/_audit/` commits intermediate scratch (`harvested-audit-*.json`,
`triaged-*.json`, `findings-all-63-*.json`, `static-flags-*.json`) alongside
canonical outputs (`errata-2026-06-03.md`, `integrity-audit-*.md`,
`F1-ground-truth.md`) with nothing marking "keep" vs "throwaway
intermediate". Same shape: two date-stamped session logs loose at
`phase2/` root (`2026-05-28-tier1-postmortem.md`,
`2026-05-29-next-session-prompt.md`) instead of in a `<topic>/` dir.

**Fix.** Covered by the §2.4 lifecycle rule (intermediate JSON either gets a
`_scratch/` subdir that is gitignored, or is deleted once the canonical
output lands).

### F6 — Untracked artifacts pending a decision [LOW]

Current working tree (mostly another session's in-flight streams — leave
alone): `title-candidates.md` (loose at repo root, belongs in `plans/` if
kept), `docs/phase2/yz-cet.html` (rendered output not committed),
`plugins/NearStarsFluxTube/` (intentional backlog prototype, memory
`project-nearstars-flux-tube-plugin` — not sprawl).

### F7 — Doc ↔ tool drift: mirror scope in `AGENTS.md` is narrower than the enforcer [LOW]

`AGENTS.md §2.1`'s English-only exclusion list enumerates only
`phase2/<topic>/{checklist,context-notes}.md`. The actual enforcer,
[`scripts/check-mirrors.sh`](../scripts/check-mirrors.sh), is broader on two
axes: (a) it only scans `docs/`, `plans/`, and `README.md` at all — the
entire `phase2/` and `phase3/` trees are never mirror-checked; (b)
`should_exclude()` additionally drops any `*/_*` path component (`_papers/`,
`_bib/`, `_audit/`, `_archive/`) and any `*/{checklist,context-notes}.md`.
The tool's behaviour is correct — audit/working docs like
`phase3/_audit/*.md` are operational, not reference, so they need no Korean
mirror. The doc simply never caught up; a reader of `AGENTS.md` alone would
wrongly conclude `phase3/_audit/` needs a mirror. Surfaced 2026-06-03 when
the question "why do the `_audit/` docs have no ko mirror?" came up.

**Fix.** Generalize §2.1's exclusion clause to "only `docs/`, `plans/`, and
`README.md` are mirrored; the `phase2/` and `phase3/` working trees and any
`_*` subtree are English-only" instead of enumerating individual files.
Bundle with the §2.4 AGENTS.md edit (§3.3).

---

## 3. Implications for NearStars — the fix plan

The gap is a **lifecycle rule**, not more location rules. Three changes,
each its own commit, in order. A future session executes; promote this note
to `phase2/sprawl-lifecycle-gate/` when starting.

### 3.1 Fix gate-5 false-positive (unblocks the health check) [do first]

- Edit [`scripts/check.sh`](../scripts/check.sh) gate 5: remove `docs/wiki`
  from `patterns` (keep `llm-wiki` / `skills-lock` / the `-system` slugs).
- Verify: `bash scripts/check.sh` exits 0 (currently exits 1 on this alone).
- One commit: `fix(check): drop stale docs/wiki false-positive from gate 5`.

### 3.2 Add a sprawl / orphan gate to `check.sh` [gate 8]

New gate flags, as warnings or failures (decide threshold):

- (a) **empty dirs** directly under `phase2/` or `phase3/`
  (`find phase2 phase3 -type d -empty`).
- (b) **reapable working dirs** — a `phase3/<system>/` or `phase2/<topic>/`
  with 0 tracked files AND a committed `docs/phase3/<slug>*.html` (output
  shipped, working dir is now scratch).
- (c) **un-indexed refs scripts** — any `scripts/refs/*.py` whose basename
  is absent from `docs/reference/tools.md`.
- One commit: `feat(check): add gate 8 — sprawl/orphan detection`.

### 3.3 Edit `AGENTS.md §2` — lifecycle rule (§2.4) + mirror-scope fix (§2.1, F7)

Two edits to `AGENTS.md §2`, one commit. First, generalize the §2.1
English-only clause (F7): replace the file enumeration with "only `docs/`,
`plans/`, and `README.md` are mirrored; the `phase2/` and `phase3/` working
trees and any `_*` subtree are English-only" — matching what
`check-mirrors.sh` already enforces. Second, add §2.4 — state the missing
reap/promote rule explicitly:

- When a working dir's output lands in `docs/`, either **commit the trio**
  (it becomes the decision log) or **delete the dir**. Never leave a
  zero-tracked working dir with shipped output.
- `_recovered/` and empty scratch dirs are **never committed** and should be
  deleted once their content is merged.
- Intermediate audit/scratch JSON lives in a gitignored `_scratch/` subdir,
  not committed beside canonical errata.
- One-off scripts get a `tools.md` line + a `# one-shot:` / `# regenerable:`
  header.
- One commit: `docs(agents): generalize §2.1 mirror scope + add §2.4 artifact-lifecycle rule`.

### 3.4 Backfill tool index (F4) + decide F3 context-notes

- Add the 7 missing `scripts/refs/*.py` lines to `tools.md` (+ ko mirror).
- Commit or delete `phase3/{eps_ind_a,hd_219134}/context-notes.md`
  (recommend commit — see F3). If committing, follow the new §2.4 trio rule.
- Commits: `docs(tools): index 7 scripts/refs builders` and (if committing
  notes) `docs(phase3): commit eps Ind A / HD 219134 synthesis decision logs`.

---

## 4. Open questions

- **Warning vs failure** for gate 8 — should reapable working dirs fail CI,
  or only warn? Leaning warn (they are local-only and harmless to git), with
  empty-dir and un-indexed-script sub-checks as hard fails.
- **`_scratch/` vs delete** for intermediate audit JSON — keep a gitignored
  trail for re-triage, or trust `git log`? `phase3/_audit/` currently keeps
  everything; the disk-color and F1 audits suggest the intermediate JSON is
  occasionally re-read, which argues for a gitignored `_scratch/` over
  outright deletion.
- Should the gate also cover `plans/` lifecycle (status: archived files that
  were never deleted)? Out of scope for v1.
