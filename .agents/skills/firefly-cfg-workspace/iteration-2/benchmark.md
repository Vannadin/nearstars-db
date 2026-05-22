# Firefly cfg skill — iteration 2 benchmark

## Pass rate (mechanical schema assertions)

| Eval | iter1 with_skill | iter2 with_skill |
|---|---|---|
| trappist-1-e | 12/12 | 12/12 |
| trappist-1-b | 3/3 | 3/3 |
| proxima-cen-b | 12/12 | 12/12 |

Schema correctness held: 27/27. The change was qualitative, not
schema-breaking.

## Time

| Eval | iter1 with_skill | iter2 with_skill | Δ |
|---|---|---|---|
| trappist-1-e | 65.0s | 54.8s | **−16%** |
| trappist-1-b | 38.4s | 35.2s | −8% |
| proxima-cen-b | 65.4s | 58.7s | −10% |
| Mean | 56.3s | 49.6s | **−12%** |

Marginally faster. The cleaner Step 3 split (bulk vs. secondary) and
the worked example §7 give the agent a closer template to follow.

## Color derivation comparison (the actual change)

### TRAPPIST-1 e (1 bar N₂ 78% + O₂ 5% + CO₂ 1% + H₂O 0.1–1%)

| Color key | iter1 (aurora-echo) | iter2 (composition-secondary) | Reason for change |
|---|---|---|---|
| trail_streak | `77 255 77 2.5` | `96 191 159 2.5` | iter1: aurora #4DFF4D echo (category error). iter2: CO₂ 1% via CN 388 + C2 Swan 516 (composition-color §4). |
| wrap_streak | `255 77 77 2` (aurora red) | `96 191 159 2` (CO₂ secondary) | Both streaks now share the same secondary chemistry — internally consistent. |

### Proxima Cen b (1 bar N₂ 95% + CO₂ 5%)

| Color key | iter1 | iter2 | Reason |
|---|---|---|---|
| trail_streak | `77 255 77 2.5` (aurora) | `96 191 159 2.5` (CO₂ 5%) | Coincidentally similar green color — but for the right reason now. |
| wrap_streak | `255 77 77 2` (aurora red) | `96 191 159 2` (CO₂) | Major shift: was warm red, now cool green. |

### TRAPPIST-1 b

No change (airless skip held).

## Qualitative observations

1. **Aurora-echo eliminated.** Both with-skill iter2 agents
   explicitly noted they did NOT use aurora hex values, citing the
   skill's "physical regime difference" guidance in Step 3 and
   composition-color.md's "Do NOT use aurora colors" note. The
   category error is closed.

2. **Composition-driven streaks self-consistent.** Both bodies have
   CO₂ as the strongest secondary (1% and 5%); both correctly select
   the CN/C2 Swan green from composition-color §4. The selection rule
   (strongest visible emitter wins) is being applied as documented.

3. **Worked example §7 acted as scaffold.** Both with-skill agents
   noted "this matches the documented §7 example almost verbatim."
   That's expected — both bodies are N₂+O₂+CO₂ class. The convergence
   confirms the skill drives consistent output across cases of the
   same atmosphere class.

4. **H₂O selection rule survived.** TRAPPIST-1 e has H₂O 0.1–1%
   alongside CO₂ 1%. The agent explicitly applied selection rule 1
   ("CN+C2 Swan beat Hα at sub-1% concentration") and chose CO₂. Good
   evidence the secondary-selection rule is being read and applied,
   not just defaulting.

5. **No `:NEEDS[NearStars]` typo.** The iter1 baseline incorrectly
   tagged the body with `:NEEDS[NearStars]` (wrong mod name). iter2
   with-skill keeps the body clean (no body-level NEEDS) and reserves
   `:NEEDS[NearStarsSystem]` for the pack — matching the skill's
   §2 NearStars-fixed convention.

## Verdict

Iteration 2 fixed the physics category error without regressing
schema correctness or convention compliance. Schema pass rate stayed
at 100%; time improved ~12%; the aurora-echo design flaw is closed.

**Ready to swap to live.**
