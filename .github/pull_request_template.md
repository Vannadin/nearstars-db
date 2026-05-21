## Summary

<!-- 1-3 bullets. Focus on the "why" more than the "what". -->

-

## Type of change

<!-- Check one. Each type has different review requirements. -->

- [ ] **DB / pipeline change** — touches `db/`, `scripts/pipeline/`, or
      `phase2/<topic>/`. Validation must pass.
- [ ] **Reference doc** — adds/edits `docs/reference/`. Long-lived
      schema or format documentation.
- [ ] **Research note** — adds/edits `plans/<topic>.md`. No code or
      data changes expected.
- [ ] **Build / tooling** — `.github/`, `run_pipeline.sh`, agent skill
      definitions under `.agents/`.

## Checklist

Required for every PR (see [AGENTS.md §3](../AGENTS.md#3-hard-rules-for-any-pr)):

- [ ] No local absolute paths (`/home/...`, `/Users/...`, `C:\...`) in
      any added file.
- [ ] No `dist/`, `db/backups/`, `.DS_Store`, or
      `.claude/settings.local.json` accidentally staged.
- [ ] Commit author is `VaNnadin <vannadin00@gmail.com>` (set per-repo,
      not global).
- [ ] Commits are semantic — one logical change per commit, describable
      in one sentence.

For **DB / pipeline changes**, additionally:

- [ ] `python3 scripts/pipeline/validate.py` exits with `FAIL: 0`.
- [ ] `derived` blocks do not invent defaults; `null` source ⇒ `null`
      derived.
- [ ] All new curated measurements carry `bibcode` (and `doi` when
      available). No `pscomppars` as a source.
- [ ] New Python files start with a one-line Korean role comment
      (AGENTS.md §3.6).

For **research notes**, additionally:

- [ ] File is at `plans/<topic>.md`, not in a new top-level directory.
- [ ] Started from [`plans/_template.md`](../plans/_template.md).
- [ ] First paragraph states the NearStars connection.
- [ ] Frontmatter has no `todos:` field (research notes don't carry
      implementation checklists — see [`plans/README.md`](../plans/README.md)).

## Test plan

<!-- How did you verify this works? Commands run, files inspected,
     scenarios checked. Be concrete. -->

-
