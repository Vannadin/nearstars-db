# Checklist — pipeline-flow-program

## WP0 — pipeline contract — DONE (1f15fe4)
- [x] `docs/reference/pipeline-contract.md` written (phase defs / boundary table / join keys / per-class done criteria / resolution order / write-only register / phase2 history index)
- [x] ko mirror (committed with WP2, eae3990)
- [x] `guideline.md` §9 → pointer to the contract (legacy defs removed)
- [x] AGENTS.md §1 table row points to pipeline-contract.md
- [x] principia-cfg planet-contract.md stale claims fixed

## WP2 — boundary gates (check.sh gate 10) — DONE (eae3990)
- [x] `scripts/pipeline/phase3_decisions.py` shared Decisions-table parser
- [x] `scripts/check_pipeline_flow.py`: phase4 body↔db check (fiction marker rule) — 0 violations
- [x] roster completeness matrix check (db/roster.yaml; 10 known gaps → warnings)
- [x] Decisions parse check — all 77 reports parse clean
- [x] check.sh gate 10 wired; all gates green
- [x] planet report slug rule documented (host slug + letter; Barnard divergence) — contract §2

## WP3 — phase2 data shapes — DONE (0d97f46)
- [x] shape normalization re-scoped: mechanical dict→list migration REJECTED (method
      cannot be guessed — comes from the cited paper). Instead: §A1 canonical-shape
      rule (list+method, upgrade on touch), shared accessor schema.pick_recommended()
      (build_systems refactor, rebuild drift 0), gate 10e legacy-dict census (402/115)
- [x] measurement-floor policy per star class → curation-data-contract SPEC §A0
- [x] floor coverage worklist (all ≤50 ly curated hosts): gate 10d — 129 hosts
      (a:3 bd:3 fgkm:120 wd:3), --floor-detail for per-host lines

## WP6 — paper references as links (owner directive 2026-07-20, mid-program)
- [x] Convention written into CONVENTIONS.md §3.3 (+ko)
- [x] Retrofit script `scripts/retrofit_paper_links.py` (whitelist-safe, idempotent)
- [x] Run over all reader-facing md (+root README/CONVENTIONS): 1,967 links / 217 files;
      phase3 HTML + wiki renders rebuilt

## WP1 — resolver — DONE (dry-run scope)
- [x] `scripts/pipeline/resolve_emit_values.py` (db → phase3 → phase4 merge, dry-run)
- [x] dry-run validated on alpha_centauri + proxima_cen + tau_cet (fiction bodies
      resolve phase4-only; tau_cet planet rows absent — matches gate 10b)
- [x] **finding**: phase3/phase4 field vocabularies are disjoint (0 collisions) →
      field-alignment map is the named emit prerequisite — contract §3 + emit-hardening
- [x] emit-hardening checklist gains alignment-map + rewire-4-emitters items
