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

## Tie-breaking by visual interest

This project's output is a *game* (KSP planet pack). When two
scenarios are observationally indistinguishable or genuinely
uncertain, the tie-breaker is **player engagement** — default to the
more visually distinctive option. The alternative is preserved as a
cfg variant.

The hierarchy is strict and one-way:

1. **Observation always wins.** If a paper rules out a scenario at
   ≥3σ, that scenario is dead regardless of how interesting it would
   be. Don't bend data for visuals.
2. **Theory with strong support wins next.** If a GCM ensemble or
   coupled atmosphere-interior model converges on a specific
   outcome, prefer that over a more dramatic but theoretically
   unsupported alternative.
3. **At genuine ties — pick interesting.** When two scenarios are
   both observation-consistent and both have plausible theoretical
   support, the more visually distinctive one becomes the default.

### What counts as "interesting" for KSP visuals

- **Specific over generic.** A cryovolcanic plume on g over an
  ice-covered ocean is more interesting than a featureless ice
  ball. Iron oxide patches biased to the substellar quadrant on b
  is more interesting than uniform basalt.
- **Distinctive over uniform.** "Eyeball Earth" geometry on e (dark
  open-water disk surrounded by ice) beats a uniformly ice-covered
  e. A 35% spot-coverage stellar disk (Wakeford 2019) beats a
  smooth M-dwarf disk.
- **Active over passive.** Io-class volcanism on c (Barr 2018,
  Dobos 2019) beats a weathered-dead-rock c, all else equal.
  Visible magma at substellar on b beats uniform fresh basalt.
- **Strong color over muted.** When albedo / illumination physics
  permits a range of perceived hues, pick within the more
  saturated end. Red-orange basaltic accent under M-dwarf light
  beats neutral gray.

### What counts as "scenario alternative" (cfg variant)

The non-default option from a genuine tie should be preserved in
the synthesis "Open items" as a cfg variant. This gives the
downstream cfg writer (`kopernicus-cfg` / `principia-cfg`) the
option to render either version. Examples:

- TRAPPIST-1 f canonical: 1 bar CO₂ + substellar open-water lens
  (more interesting). Variant: 0.1 bar CO₂ snowball (more
  observation-conservative).
- TRAPPIST-1 c canonical: Io-class active volcanism with localized
  fresh basalt (Barr 2018 / Dobos 2019). Variant: weathered global
  basalt (less geologically active).
- TRAPPIST-1 h canonical: thin atmosphere with H₂O-ice surface +
  Dong 2018 retention argument (more interesting → atmosphere
  visible). Variant: airless rocky surface (cosmic-shoreline
  conservative).

### Documenting the choice

Every "Confidence: low" row in a Decisions table that involved a
tie-break should explicitly say so in the Basis column:

```markdown
| `surface_tint_rgb_hex_accent` | `#7a2a10` (cooling lava red) | low |
  Tie-break: interesting-first (per [[feedback-phase3-interesting-first]]).
  Photolytic oxidation (less interesting) or cooling-lava red
  (more interesting) both fit the airless ultramafic surface;
  cfg picks lava for visual distinctiveness. |
```

This makes the policy visible to the next session reading the
synthesis, and to the downstream cfg writer.

### What this is NOT

- Not an excuse to invent features the literature doesn't support.
  "Pulsar-illuminated aurorae on TRAPPIST-1 b" would be interesting
  but isn't theoretically supported by any paper, so it doesn't
  qualify.
- Not a reason to override Confidence labels. A Confidence=high
  measurement stays high; tie-breaking is a tool for Confidence=low
  aesthetic choices only.
- Not retroactive without checking. If applying this rule to an
  existing synthesis row would change the cfg value, log it as an
  Open item rather than silently editing.

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
