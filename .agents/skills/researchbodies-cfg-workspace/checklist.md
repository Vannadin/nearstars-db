# ResearchBodies cfg skill — Checklist

## Research
- [x] Clone JPLRepo/ResearchBodies source into workspace
- [x] Schema inventory (delegated): nodes + keys, source-cited
- [x] Confirm ONDISCOVERY format (node name, bodyName match, value use)
- [x] Confirm IGNORELEVELS value format (4 bools, order, meaning)
- [x] Confirm global vs per-body split (cost/odds/telescope = global)
- [x] Capture a shipped example cfg verbatim
- [x] Confirm Kopernicus / barycenter (radius<100m) handling
- [x] Confirm difficulty enum + how IGNORELEVELS interacts with it
- [x] RO / RP-1 compatibility check (source + web)

## DB / Phase 4 mapping
- [x] Locate detection data (raw.discoverymethod + sources[] bibcode)
- [x] Decide mapping INPUT = Phase 4 `discoverability:` block (owner)
- [x] Draft category → difficulty mapping proposal (A/B/C)
- [x] Owner picks grading = Scheme A
- [x] Define Phase 4 `discoverability:` input schema (db-mapping.md)

## Skill build
- [x] references/ondiscovery.md
- [x] references/ignorelevels.md
- [x] references/global-settings.md
- [x] references/db-mapping.md
- [x] references/pitfalls.md
- [x] references/rp1-compat.md (deferred RP-1 integration documented)
- [x] SKILL.md (frontmatter + body)
- [x] scripts/emit_researchbodies_cfg.py
- [x] Dry-run emit on example (6 bodies, valid output + warnings work)

## Graduate
- [x] Live skill at .claude/skills/researchbodies-cfg/
- [ ] Update docs/reference/tools.md index
- [ ] Update memory pointer (project_nearstars_discoverability_researchbodies)
- [ ] check.sh green

## Deferred (future update)
- [ ] RP-1 integration patch (allowTrackingStationLvl1 + part/contract)
- [ ] Fill Phase 4 `discoverability:` blocks during facet-walk
- [ ] Run bulk emit at project end (with other cfg writers)
- [ ] Telescope moon-exclusion Harmony plugin → DELEGATED to Schultz
      (brief: plugin-brief-telescope-moon-filter.md). No cfg change needed.
