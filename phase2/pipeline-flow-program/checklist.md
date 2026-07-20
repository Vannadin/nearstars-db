# Checklist — pipeline-flow-program

## WP0 — pipeline contract
- [ ] `docs/reference/pipeline-contract.md` written (phase defs / boundary table / join keys / per-class done criteria / resolution order / write-only register / phase2 history index)
- [ ] ko mirror
- [ ] `guideline.md` §9 → pointer to the contract (legacy defs removed)
- [ ] AGENTS.md §1 table row points to pipeline-contract.md
- [ ] principia-cfg planet-contract.md stale claims fixed

## WP2 — boundary gates (check.sh gate 10)
- [ ] `scripts/pipeline/phase3_decisions.py` shared Decisions-table parser
- [ ] `scripts/check_pipeline_flow.py`: phase4 body↔db check (fiction marker rule)
- [ ] roster completeness matrix check
- [ ] Decisions parse check over emit-relevant reports
- [ ] check.sh gate 10 wired; all gates green

## WP3 — phase2 data shapes
- [ ] planets_curated dict→list migration (script, canonical writer, validate rule)
- [ ] measurement-floor policy per star class → curation-data-contract SPEC
- [ ] floor coverage report (all ≤50 ly curated hosts) generated for the backfill program

## WP6 — paper references as links (owner directive 2026-07-20, mid-program)
- [ ] Convention written into CONVENTIONS.md §3.3 (+ko)
- [ ] Retrofit script: bare bibcodes/arXiv ids in md narrative → ADS/arXiv markdown links (skip code blocks, YAML machine fields)
- [ ] Run over docs/ + plans/ + phase2–4 md + ko mirrors; rebuild HTML renders

## WP1 — resolver
- [ ] `scripts/pipeline/resolve_emit_values.py` (db → phase3 → phase4 merge, dry-run)
- [ ] dry-run validated on alpha_centauri + proxima_cen + tau_cet
- [ ] contract §resolution updated with actual field mapping
- [ ] emit-hardening checklist gains "rewire 4 emitters to resolver" item (deferred to emit)
