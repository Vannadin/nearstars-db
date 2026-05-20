# principia-cfg — Checklist

## Done

- [x] SKILL.md (frontmatter, trigger phrases, NearStars decisions, DB↔cfg mapping table)
- [x] references/nodes.md — Principia node syntax subset actually emitted
- [x] references/db-mapping.md — JSON path → cfg field with conversions
- [x] references/file-layout.md — output path + NEEDS-tag rationale
- [x] references/planet-contract.md — forward contract for planet support
- [x] references/pitfalls.md — 10 common Principia-cfg mistakes
- [x] scripts/emit_principia_cfg.py — DB → 2 cfg files (Sol real scale, stars only)
- [x] scripts/dev_backfill_spt_mass.py — one-off helper to fill 14 missing-mass stars during skill testing
- [x] Body-name normalization rule (preserve uppercase tokens, capitalize lowercase tokens)
- [x] Strict-abort validation, all errors collected before exit
- [x] `--system` flag accepts multiple stems
- [x] End-to-end verification: 152 bodies emit, GM/distance/velocity sanity-checked
- [x] Aligned output path to `dist/NearStars-Configs/Patches/Principia/` per `docs/reference/mod-release-layout.md` §1
- [x] Softened `:FOR[NearStarsSystem]` discussion in file-layout.md + SKILL.md (acknowledges `mod-release-layout.md` §2.1 convention for other patches)
- [x] checklist.md + context-notes.md (this artifact)

## Out of scope for MVP (intentional)

- [ ] Sol quarter-scale variant (`Quarter_NearStars-InitialState.cfg`) — different `solar_system_epoch`, needs separate Cartesian coords
- [ ] RSS variant — same epoch as Sol real, coords reusable, but separate NEEDS tag
- [ ] Planet body emission — gated on planet ICRF Cartesian appearing in DB; see `references/planet-contract.md`
- [ ] Per-star rotation pole (`axis_right_ascension`, `axis_declination`) — DB has no measurements

## Open / deferred (will need attention)

- [ ] **Backfill 14 stars with mass measurements**. Current state: skill aborts with 14 errors if run against full DB. Either (a) curate real values from literature, or (b) accept `dev_backfill_spt_mass.py` output as Phase-1 values and commit to `db/stellar_props_curated.json`.
- [ ] **KSP load-test the emitted cfg**. The skill is logically correct against the Principia reference, but no actual KSP run has confirmed Principia accepts the patches.
- [ ] **Validate `--system` selection against systems that don't exist in the file set** — current behavior aborts with clear message, fine for now.
