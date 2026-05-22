# Firefly cfg skill — iteration 1 benchmark

## Pass rate (mechanical schema assertions)

| Eval | with_skill | without_skill |
|---|---|---|
| trappist-1-e (Earth-analog) | 12/12 | 12/12 |
| trappist-1-b (airless) | 3/3 | 3/3 |
| proxima-cen-b (Earth-analog) | 12/12 | 12/12 |
| **Total** | **27/27 (100%)** | **27/27 (100%)** |

Both conditions pass every objective schema check. Mechanical
assertions do not discriminate.

## Time (seconds)

| Eval | with_skill | without_skill | Δ |
|---|---|---|---|
| trappist-1-e | 65.0 | 93.7 | **−30.6%** |
| trappist-1-b | 38.4 | 49.6 | **−22.6%** |
| proxima-cen-b | 65.4 | 101.5 | **−35.6%** |
| Mean | 56.3 | 81.6 | **−31.0%** |

Skill wins by ~31% on time. Baseline agents spend extra time on
upstream GitHub research; skill agents read curated references in
the workspace.

## Tokens

| Eval | with_skill | without_skill | Δ |
|---|---|---|---|
| trappist-1-e | 53,385 | 58,803 | −9% |
| trappist-1-b | 36,963 | 33,758 | +10% |
| proxima-cen-b | 51,889 | 50,933 | +2% |
| Mean | 47,412 | 47,831 | ~0% |

Token cost ~equal. Skill loads references (token cost); baseline does
WebFetch + raw schema deduction (also token cost). Net neutral.

## Qualitative differentiators (not captured in assertions)

1. **NearStars naming convention.** With-skill consistently produces
   `name = Trappist1e` / `ProximaCenB` (camelCase, no dashes), and
   omits `:NEEDS[…]` from body-level nodes. Baseline (proxima)
   incorrectly added `:NEEDS[NearStars]` to the body — wrong mod name
   (should be `NearStarsSystem`) and wrong placement (NEEDS is for the
   pack node, not bodies).

2. **Korean header comments (CLAUDE.md §6).** Both with-skill cfgs
   open with a Korean one-liner describing the file's role. Baselines
   use English comments instead.

3. **Aurora-echo on streaks.** Skill's phase3-mapping §2 notes "if
   aurora present, `trail_streak` can echo aurora primary." Both
   with-skill agents applied this; both baselines rejected it on
   physical grounds ("aurora is EVE/aurora-mod territory, not reentry
   plasma"). Both interpretations are defensible — this is a
   stylistic call, not a schema correctness issue.

4. **Palette consistency.** With-skill cfgs use exact RGB values from
   composition-color.md §3 (Earth-like row). Baselines derived
   composition-driven tweaks (warmer trail for elevated CO2). Both
   produce plausible aesthetic outcomes; the skill produces *predictable*
   outcomes across runs.

5. **Source citations.** With-skill outputs cite specific reference
   files (composition-color §3, phase3-mapping §7). Baseline outputs
   cite Firefly source by name; one baseline invented a non-existent
   class `ModuleFirefly.cs` (actually `AtmoFxModule.cs`).

## Analyst observations

- **Non-discriminating assertions.** The 12-assertion schema check
  passes for all conditions; it confirms the skill produces valid
  output but doesn't show it's *better* than a competent freelancer.
  For iteration 2, consider adding NearStars-convention-specific
  assertions (Korean header, exact NEEDS placement, palette
  consistency across multiple Earth-analog bodies).

- **Skill's time win is real.** ~30% faster, scaling with task
  difficulty. The savings come from skipping upstream-repo research.
  For a single-shot cfg this matters less; for batch generation
  (entire NearStars system: ~50 bodies), it compounds.

- **The aurora-echo guidance may be over-applied.** Both with-skill
  agents echoed aurora colors into streaks despite the skill's
  language being permissive ("can echo"). The skill could clarify
  this is *only* appropriate when Phase 3 explicitly notes aurora-
  driven streak chemistry, otherwise streak follows trail palette.

- **Baseline competence is surprisingly high.** A general-purpose
  agent with web access and the Firefly repo URL can produce a valid
  cfg without the skill. The skill's value is *consistency,
  convention compliance, and speed*, not unlocked capability.

## Iteration 2 considerations

Adjustments to consider before swap-to-live:

1. **Tighten aurora-echo wording** in phase3-mapping.md §2:
   - Current: "optional Phase 3 fields ... aurora_color_primary_hex →
     `trail_streak` (optional)"
   - Proposed: "ONLY echo aurora colors into trail_streak/wrap_streak
     if Phase 3's atmosphere synthesis explicitly notes that aurora-
     emitting species contribute to reentry plasma chemistry.
     Default: follow the bulk-gas trail palette unchanged."

2. **Add NearStars-convention assertion** for future evals (Korean
   header present; no body-level :NEEDS; pack-mod name is
   `NearStarsSystem`).

3. **Otherwise: the skill is ready to swap to live.** Schema-passing
   rate is 100%; time savings are real; convention compliance is
   better than baseline.
