# The cold-flank general fix — checklist

Brief 22, 2026-08-31 (owner-approved order ①). The refusal machinery exists to keep the
**answer** honest; the shoot and temperature loops route **trials** through the same
refusals, so a solve can die in a state no converged answer would occupy. Direction, as
approved: **a trial-path refusal steers the bracket instead of killing the solve.**

## Pre-registered BEFORE any code was read beyond the brief's three pointers

**Acceptance criteria, sharpest first.**

- [x] ① C13 end B solves **without the ghost silicate stub** — both planets, both `imf`
      expressions (λ differs 1.8e-4 relative across the ±ULP residual — inside the
      ε-ladder envelope; solvability no longer depends on it)
- [x] ② Uranus's end B (float residual exactly 0.0 under both expressions) solves —
      λ 0.209729 · R −1.57 % · conv=True

**Outcome branches, five, registered before running.**

1. One general route covers all three cases (C11's over-broad refusal · the
   Queyroux–Neptune route death · C13 end B) → structural repair.
2. C13 covered, the others not → the family was site-specific patterns; **name which one
   is not covered**.
3. Steering works but **a converged answer moves** → anchor movement: report with cause,
   never absorb; `--refresh` only if a path-fingerprint function/constant changed, same
   commit.
4. **A refusal was load-bearing** — some trial refusal is really the answer's refusal (the
   answer does use that evidence) → the corridor's boundary was right, C13 end B stood
   only on the stub, and the row must be corrected: **26 % / 41 % were stub-dependent**.
5. A kind outside the register → name it and extend the register.

"Not found" is a legitimate ending — say what was searched and how.

**Hard constraints.** Anchors bit-identical (report movement with cause); gate FAIL 0 and
say what this adds to gate time; no new runtime dependency; English commits, one logical
change each; declare–integrate–report, no tuning declarations until answers look right.

## Work items (filled as the work proceeds)

- [x] Read the corridor: `interior.py` p_ceiling clamp (~960), the outer-layer narrowing
      pattern (~976), the shoot's PhaseGap handling, the temperature loop's too_cold
      steering. (The suspected `_cold_phases` pre-check turned out to be notes-only; the
      traced killer of end B's T=0.0 gap was the **centre seed** — notes §1)
- [x] Verify the directing session's three readings against the code (they are readings,
      not verdicts; the code wins)
- [x] Reconstruct each of the three cases' death mechanism precisely enough to say which
      line kills it
- [x] Design the minimal general route; implement (three edits, notes §2)
- [x] Acceptance ① and ② measured (notes §3)
- [x] Coverage measured — Queyroux–Neptune converges to the anchor's own solution under
      the window patch + fix (79 s); C11 named as a different genus (branch 2)
- [x] Anchors: convergence-point integrations bit-identical; `--refresh` in the landing
      commit — anchor diff shows only fingerprint/date/seconds
- [ ] Full gate (`check.sh`) FAIL 0; the new test section adds ~3–4 s — **INTERRUPTED at
      14:04 KST 2026-08-31** (owner's compute freeze 14:04–15:04): the run was killed
      mid-flight and NOT completed. Resume point: rerun `./scripts/check.sh` from the top
      after 15:04; everything else on this list was already measured before the freeze
      (acceptance, coverage, `--refresh` with its diff trace)
- [x] `interior-core.md`: rules paragraph + C13/C5 row updates; bracket numbers
      re-verified stub-free (branch 4 did not fire)
- [x] Context notes; report to nearstars-cb with reproduction instructions for
      judgment-changing numbers
