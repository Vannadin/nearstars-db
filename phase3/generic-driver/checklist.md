# Phase 3 generic driver — checklist

Goal: replace per-system ad-hoc Python (currently `add_missing_papers.py`
per system) with a single declarative `system.yaml` + generic driver
that runs Steps 2–6 of the nearstars-phase3 SKILL.

## Stage 1 — Schema + scripts

- [ ] Define `phase3/<system>/system.yaml` schema (planets, score
  thresholds, expand parameters, paper injections)
- [ ] Write `scripts/phase3/inject_papers.py <system>` — generic
  replacement for per-system `add_missing_papers.py`
- [ ] Write `scripts/phase3/run_phase3.py <system> [--stage N]` —
  driver for Steps 2–6 (build / system-bib / expand / score / fetch)

## Stage 2 — Verification scripts

- [x] `scripts/phase3/verify_triage.py <system>` — all `combined_score
  >= 14` papers have explicit triage classification
- [x] `scripts/phase3/check_block_parity.py <slug>` — ko/en block
  counts match before `build_html.py` runs
- [ ] ~~verify_decisions.py~~ dropped (see context-notes — Decisions
  table format mismatch made it too noisy without a Bibliography
  cross-reference parser)

## Stage 3 — Migration

- [ ] Convert `phase3/alpha_centauri_proxima/add_missing_papers.py`
  → `system.yaml` (inject the same 9 bibcodes)
- [ ] Run `inject_papers.py alpha_centauri_proxima`, compare bib YAML
  diffs — must match prior add_missing_papers.py output
- [ ] Delete the per-system Python file
- [ ] Add `system.yaml` for `trappist_1` (no injections needed, but
  records planets + thresholds for run_phase3.py)

## Stage 4 — Wire into skill + tools

- [ ] Update `.claude/skills/nearstars-phase3/SKILL.md` Steps 2–6
  to call `run_phase3.py <system>` instead of per-stage invocations
- [ ] Register new scripts in `docs/reference/tools.md` (en + ko)
- [ ] Add example `phase3/_template/system.yaml`

## Verification

- [ ] `python3 scripts/phase3/inject_papers.py alpha_centauri_proxima
  --check` exit 0 (idempotent against current bib state)
- [ ] `python3 scripts/phase3/verify_triage.py alpha_centauri_proxima`
  passes for currently-completed systems
- [ ] `python3 scripts/phase3/verify_decisions.py proxima-cen-b` passes
- [ ] `python3 scripts/phase3/check_block_parity.py trappist-1-d` passes
- [ ] `./scripts/check.sh` clean

## Related

- [Phase 2 generic-apply workspace](../../phase2/generic-apply/checklist.md) — paired refactor track
- [nearstars-phase3 skill](../../.claude/skills/nearstars-phase3/SKILL.md) — parent procedure
