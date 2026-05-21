<!-- Phase 3 상충 데이터 처리 정책 — 어느 논문 값을 헤드라인으로 쓸지, 어떻게 기록할지 -->
# Phase 3 conflict resolution

Two or more papers will often give different numbers for the same
cfg field. This file documents the resolution policy used when
producing the Decisions table.

## Default priority order

For a given field, prefer in this order:

1. **Most recent peer-reviewed paper** with a direct measurement
   that applies to the specific planet
2. **Most recent peer-reviewed paper** with a direct measurement
   that applies to the system
3. **Most recent peer-reviewed paper** with a model prediction
   appropriate to the planet's regime
4. **Most authoritative theoretical paper** that derived the value
   from independent physics

"Most recent" is the published year (or arXiv submission year if
unpublished). Ties: use the higher-authority venue per
[`scoring-reference.md`](scoring-reference.md).

## When measurement papers disagree

Example: TRAPPIST-1 b's tidal heating flux.

- Bolmont 2020 (cited in older work): 0.04–0.2 W/m² (low end of
  interior-structure-dependent range)
- Bolmont 2026 (arXiv 2601.03408): 0.5–1 W/m² nominal, up to ~400
  W/m² constrained by JWST nightside

Resolution rule: take the most recent peer-reviewed paper as the
headline value, but explicitly mention the older estimate's range
in the prose synthesis (Surface or Atmosphere section). This
preserves the audit trail of how the field's understanding evolved.

Table row:
```
| `tidal_heating_w_m2` | 0.5–1 (low-e) up to ~400 (max-e, JWST-capped) | medium | Bolmont 2026 — internal-structure dependent; JWST cap |
```

Prose:
> "Bolmont 2026 revises older estimates substantially upward.
> For b's measured CMF (Agol 2021) at low eccentricity, surface flux
> is 0.5–1 W/m² nominal. Higher-e solutions reach 10²–10³ W/m² but
> are ruled out by the JWST nightside constraint (Gillon 2025;
> T_2σ ≤ 291 K → Φ_2σ ≤ 407 W/m²)."

## When model papers disagree on the same physics

Example: TRAPPIST-1 g's water mass fraction.

- Unterborn 2018 (1706.02689): ≥50 wt% if inward-migration formation
- Bourgeois 2024 (2008.09599): 0.11–0.24 from magma-ocean evolution
- Acuña 2025 (similar paper for f): 16% ± 9.9% from MAGRATHEA

Resolution rule: if the models use **different assumptions** rather
than different methods, take the **wider range** as the headline,
noting both bounds.

```
| `water_mass_fraction` | 0.11–0.50 | medium | Bourgeois 2024 (0.11–0.24); Unterborn 2018 inward-migration model gives upper bound ≥50 wt% — highest in system either way |
```

## When recent peer-reviewed paper contradicts your prior synthesis

If you wrote a synthesis row last session and a new paper contradicts
it on a follow-up pass:

1. **Don't silently overwrite.** Add a new row or replace the value
   with the new one, and add an "Open items" note explaining the
   change.
2. **Update the Basis column** to the new paper's reference.
3. **Note the original paper in the prose** as superseded (e.g.,
   "X 2020 gave Y; superseded by Z 2025 which finds Y'").

## When two papers disagree and there's no peer-reviewed tiebreaker

Take the **higher-confidence model** (typically the one with more
self-consistency between interior + atmosphere + climate modules),
mark Confidence as "low" or "medium" in the table, and document both
options in "Open items for follow-up" as a cfg-variant decision.

## When the user's prior synthesis was wrong

Treat your own past work as you would any other source. If the
paper-validation pass (Step 10 in the workflow) reveals the cfg
value contradicts the cited paper:

1. Fix the value in the Decisions table.
2. Update the prose synthesis section.
3. Add a one-line "errata" note in `context-notes.md` explaining
   what changed and why.

This happened in the TRAPPIST-1 b/c/e/g/h first pass (see
[[feedback-phase3-validation]]). The validation pass exists
specifically to catch this.

## When a paper cites a number you can't verify

Some papers cite figures from earlier work without giving the
specific number themselves. If you can't trace back to a primary
source:

1. Don't use the cited number as a Decisions table headline value.
2. Use the closest measurable proxy from the primary source.
3. If no proxy exists, leave the field blank (`-` or `n/a`) with
   Confidence "low" and a Basis line explaining the gap.

It's better to admit ignorance than to propagate an unverifiable
number into the cfg.

## Documenting conflicts in the synthesis

The "Open items for follow-up" section is the canonical place to
park disagreements that aren't resolved in the current synthesis.
Format:

```markdown
- The `water_mass_fraction` range is wide (0.11–0.50) due to a
  disagreement between Bourgeois 2024 and Unterborn 2018. If a
  later paper (e.g., Acuña 2027) provides a tighter joint constraint
  with both atmospheric escape and interior structure, the row
  should be re-fit.
```

When the next session opens, the synthesis writer reads "Open items"
first to know what's still unsettled.
