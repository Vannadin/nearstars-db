---
description: Ingest one or more files into the LLM Wiki (frontmatter + Related)
allowed-tools: Read, Edit, Write, Bash, Glob, Grep
---

Run the LLM Wiki ingest workflow on the file(s) listed in $ARGUMENTS.

Procedure (from `.agents/skills/llm-wiki/SKILL.md` §4):

1. For each file path in $ARGUMENTS:
   a. Read the file.
   b. Determine its type (concept / entity / source / synthesis / workspace) from its path and content. See SKILL.md §2.
   c. Determine its tier (public / local-only). Use `git check-ignore` to verify.
   d. If frontmatter missing, add YAML frontmatter per the type spec in SKILL.md §2. Assign `cluster:` per the cluster definitions in §3.
   e. If a `## Related` section is missing, append one near the end of the file. Each entry: a markdown link + one-line description of the *relationship* (not just the destination). Avoid pure name-listing.
2. Update `docs/wiki/index.md` — add the file under its cluster section if not already listed.
3. Append a structured `ingest` entry to `docs/wiki/log.md` (use the format shown there).
4. Update `docs/wiki/hot.md` "Last 3 log entries" and "Active pages".
5. For each public-tier file, scan for EA-identifier leaks (SKILL.md §9 blocklist). If found, flag in the log entry but do NOT auto-fix.

Safety rules from SKILL.md §10 apply throughout — never write to raw tier, never delete pages, never commit local-only paths.

Report at the end: list of files modified, frontmatter coverage delta, any issues found. Keep report under 200 words.
