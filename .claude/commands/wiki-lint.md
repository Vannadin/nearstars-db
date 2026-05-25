---
description: Run LLM Wiki health check — orphans, EA leaks, frontmatter coverage, missing cross-refs
allowed-tools: Read, Edit, Bash, Glob, Grep
---

Run the LLM Wiki lint workflow per `.agents/skills/llm-wiki/SKILL.md` §5.

Scan the **public + local-only wiki tiers** (NOT raw tier — skip `docs/phase3/_papers/`, `db/`, `phase2/`, `phase3/` content directories used as raw inputs).

Checks:

1. **Frontmatter audit** — every wiki-tier `.md` should have YAML frontmatter with `type:`, `cluster:`, `tier:`, `created:`, `updated:`. List violations.
2. **Orphan check** — list wiki pages with 0 inbound markdown/wikilink references. Exclude entry-point pages (`AGENTS.md`, `README.md`, `docs/wiki/index.md`, hot/log/overview).
3. **Stale-claim check** — pages with `updated:` older than 90 days but in actively-edited clusters. Suggest re-read.
4. **Confidence-low audit** — list pages with `confidence: low`. Suggest follow-up sources.
5. **Cluster health** — every hub has `cluster_role: hub` and `## In this cluster` (or equivalent `## Related` listing members). Every member is listed by its hub.
6. **Cross-tier link audit** — public-tier files must NOT inline EA-derived field names. Scan for the blocklist in SKILL.md §9: `sunReflectionStrength`, `reflectionColor`, `ambientColor`, `cloudColorMultiplier`, `cloudScatteringMultiplier`, `cloudSkyIrradianceMultiplier`, `volumetricsColorMultiplier`, `EVEIntegration_preserveCloudColors`, `layerRaymarchedVolumeV5`. List violations.
7. **Missing-page suggestions** — concepts/entities mentioned 3+ times across pages but lacking their own page.

Output an informational report. Do NOT auto-fix. Append a `lint` entry to `docs/wiki/log.md` with the summary, and update `docs/wiki/hot.md` "Last 3 log entries".

Report format: counts + top 5 examples per category. Total under 400 words.
