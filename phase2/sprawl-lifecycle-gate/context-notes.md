# Context notes — sprawl-lifecycle-gate

Append-only decision log. Started 2026-07-19.

## 2026-07-19 — re-audit + scope decisions

- **Re-audit (Opus agent, read-only) confirmed:** June F1 fixed, F3 partial; F4/F5/F7
  + §2.4 + sprawl gate outstanding. New findings: phase4 root = 10 loose files
  (4 viewers + 6 review .md) with no home rule; 6 `.log` committed under
  `phase3/stability-sim/results/**` (gitignore only guarded the sim root);
  viewer HTML in 3 competing homes; tau_cet vs tau_ceti slug split (phase4 only).
- **Filenames preserved on all moves.** Board YAML narratives and rendered
  docs/phase4 HTML cite these files by bare filename in prose
  (`polyphemus-art-direction.md line 235–236`, `synthetic-orbit-noise 정책 rule 2`).
  Renaming would stale dozens of gated evidence strings; moving within phase4/
  with the same filename keeps every prose reference resolvable.
- **phase4 root taxonomy chosen:** `<system>.yaml` boards + `SPEC.md` + `README.md`
  only. `_audit/` mirrors the phase3 convention (point-in-time audits AND coverage
  trackers — facet-checklist.md included, it is coverage tracking). `policies/`
  holds SPEC annexes that boards cite as policy (synthetic-orbit-noise is *active*
  policy — proxima_cen.yaml applies its rule 2 — so it stays beside SPEC rather
  than moving to plans/). `art-direction/` per memory: art-pass references
  accumulate separately from boards. `viewers/` holds frozen design-exploration
  HTML (the polyphemus viewer is explicitly FROZEN in tools.md; these are captured
  artifacts, not maintained docs/ outputs — so they stay in the working tree, not
  docs/phase4/).
- **stability-sim results tree left intact** (145 tracked files incl. `_viewers/`):
  it is the sim pipeline's own output tree with its manifest; relocating it would
  mean rewiring the generators. Only `.log` files are reaped (never curation
  state). gitignore pattern widened to `phase3/stability-sim/**/*.log`.
- **Session logs owner:** `2026-05-28-tier1-postmortem.md` +
  `2026-05-29-next-session-prompt.md` → `phase2/tier1-stellar/` (the restarted
  Tier 1 effort those documents fed). `scripts/check_language.py` exemption paths
  updated in the same commit.
- **Slug unification deferred** to its own session: touching phase4 board
  filenames + docs/phase4 dir names + any emit-script references is a traced
  rename, not a mechanical move. Must land before emit wiring.
- **docs/ root versioned duplicates** (`index.v1.html`, `index-v2-sample.html`,
  `style.v2.css`) NOT deleted — deletion of existing content needs owner
  confirmation (CLAUDE.md §11).
- **phase4/README.md content is stale** ("Phase 4 is NOT yet built" — it partially
  is, since 2026-07-10). Only links fixed here; content refresh flagged to owner,
  not silently rewritten.
- **Evidence-log exception discovered during untracking.** 2 of the 6 committed
  logs are cited as provenance by gated Phase 4 board rows / art-direction docs
  (`_snapshot500/elements.log` ← alpha_centauri.yaml orbit snapshot;
  `_ring_clearing.log` ← ring-clearing gate + tools.md). Untracking those would
  break the evidence chain, so §2.4 gained an explicit exception: board-cited
  logs stay tracked via gitignore negation + gate-9 allowlist. The 4 uncited
  logs were untracked.
- **Pre-existing mirror debt surfaced by gate 2:** 7 missing ko mirrors, all
  `plans/principia-interstellar-branch/**` (other sessions' program). Backfilled
  via translation agent so check.sh can go green — not caused by this cleanup.
  5 stale-mirror warnings left as-is (content work, non-blocking):
  3× docs/reference, R4 (in-flight), and `ko/phase3/stability-sim/STABILITY_REPORT.md`
  — the last one is itself a §2.1 anomaly (phase3 is English-only; the ko file
  predates the generalized rule). Removal needs owner confirmation.
