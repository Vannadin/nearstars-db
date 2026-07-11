<!-- nearstars-methodology 스킬 추출 작업 체크리스트 -->
# nearstars-methodology skill extraction — checklist

- [x] Gather source material (methodology-index.md discipline note, planetary-dynamo-scaling.md structure, R6 prompt anatomy, build_bibliography.py, phase3 skill delegation section)
- [x] Draft SKILL.md (`.claude/skills/nearstars-methodology/`) — two modes (A recipe doc / B research prompt), ADS discipline, template structures, delegation & token discipline
- [x] Light test: 1 with-skill subagent run, Mode B authoring scenario (synthetic-eccentricity parameters), no live ADS research
- [x] Write assertions (8) + grade deterministically (counts re-verified against db/planets_curated.json — agent's 204/20/35/149 exact)
- [x] Result: 8/8 assertions passed
- [x] Apply skill fixes from the run's friction report (Mode B path rule, authoring/executing role split, delegation-guidance-travels-inside-the-prompt)
- [x] Launch eval viewer for owner review
- [ ] Owner review feedback processed (iterate if needed)
- [ ] Move workspace to `.agents/skills/nearstars-methodology-workspace/` (house convention) after review
- [ ] Commit skill + workspace
