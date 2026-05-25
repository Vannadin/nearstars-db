---
description: Query the LLM Wiki for a topic — read relevant pages and synthesize an answer with citations
allowed-tools: Read, Bash, Glob, Grep
---

Query the wiki for: $ARGUMENTS

Procedure (from `.agents/skills/llm-wiki/SKILL.md` §7):

1. Read `docs/wiki/index.md` to identify clusters likely relevant to the query topic.
2. Read the relevant cluster's hub + key members directly.
3. If the topic spans multiple clusters, read across them.
4. Synthesize a focused answer with `[[wikilink]]` or `[text](path)` citations to specific source pages.
5. If the answer would benefit future sessions (substantial analysis, comparison, or synthesis), ask the user whether to file it as a new page in `docs/wiki/syntheses/` or `plans/`.
6. Append a `query` entry to `docs/wiki/log.md` with the question + pages read + any synthesis filed.
7. Update `docs/wiki/hot.md` "Last 3 log entries".

Output the answer first (concise, with citations), then a brief note on which pages were read and any follow-up suggestions.

Length: vary with the question — simple lookups under 100 words, complex analyses up to 500 words.
