# Context notes — nearstars-phase3 optimization

Append-only. Newest decisions at the top.

---

## 2026-05-22 — Session start, 🔴 critical batch

### Why all four [I1]~[I4] in one commit instead of four

User chose "심각도별로 분할 커밋" (severity-bucketed commits). [I1]~[I4]
are all under the same severity (🔴 critical) and all touch the same
file region (SKILL.md Step 5, Step 8, "Key Policies" section). Per
CLAUDE.md §9, one logical change = one commit; "remove duplication
with memory, synthesis-template, and inline script logic" describes
in one sentence, so it groups.

### Why keep `project-nearstars-phase-distinction` in [I1] but drop `feedback-phase3-process` and `feedback-phase3-depth`

- `phase-distinction` is **referenced multiple times in Step 1 and
  Step 8** as a hard gate. Keeping the inline pointer makes the
  precondition (Phase 2 must exist) visible at the workflow level.
- `phase3-process` is documented in `feedback-phase3-process` memory
  as "the canonical per-pass order", but the order is already the
  literal workflow steps in the skill. The pointer is redundant.
- `phase3-depth` says "deep-read, not abstract-only" — this is
  already enforced by Step 7 (triage) + Step 8 (deep-read with
  cfg-decision focus). The pointer is redundant.

### Why move the field table to synthesis-template.md, not to a new file

synthesis-template.md already has the canonical field list under
"Standard field list" with grouped subsections (Orbital / Physical /
Atmosphere / Surface / Interior / Sky-star). The Step 8 "Looking
for / Why" table maps the same fields to *what to look for in the
paper*. Adding "what to look for" as a column or sub-block in
synthesis-template keeps the field list and its extraction guidance
together — easier to maintain in one file.

### Why `--mark-skipped-below` instead of a Python helper module

The inline Python in Step 5 is ~12 lines, does one job (set
`status: skipped` + add `skip_reason` for rows below a threshold), and
no other script needs it. A flag on score_papers.py is the lowest-
friction option: same yaml, idempotent (already-skipped rows are
no-ops), zero new files.

## Related

- [phase3 procedure (skill)](../../.agents/skills/nearstars-phase3/SKILL.md) — parent topic this workspace contributes to
