# NearStars-DB — Paper reference count

Calculated 2026-05-22 by deduplicated scan of ADS bibcode / DOI /
title-only fields across the project tree.

## Headline numbers

- **557 unique paper references** project-wide
- **328 Phase 3 bibliography entries** across 7 TRAPPIST-1 planets
  (249 unique after dedup)
- **156 Phase 2 measurements** referenced in `db/stellar_props_curated.json`
  + `db/planets_curated.json`
- **312 unique references** across all 149 `db/systems/*.json` files

## Phase 3 breakdown (TRAPPIST-1)

| Planet | Bibliography size |
|---|---|
| TRAPPIST-1 b | 66 |
| TRAPPIST-1 c | 32 |
| TRAPPIST-1 d | 32 (pilot) |
| TRAPPIST-1 e | 64 |
| TRAPPIST-1 f | 15 |
| TRAPPIST-1 g | 66 |
| TRAPPIST-1 h | 53 |
| **Total** | **328** entries / **249** unique |

## Per-system reference counts (top 20 by ref count)

| System | Unique refs |
|---|---|
| TRAPPIST-1 | 16 |
| AU Mic | 11 |
| 55 Cnc | 9 |
| 47 UMa | 7 |
| HD 20794 | 7 |
| GJ 433 | 7 |
| GJ 876 | 7 |
| Barnard's Star | 7 |
| Alpha Centauri A | 6 |
| GJ 1132 | 6 |
| GJ 1148 | 6 |
| GJ 180 | 6 |
| GJ 581 | 6 |
| GJ 667 C | 6 |
| GJ 687 | 6 |
| HD 219134 | 6 |
| HD 40307 | 6 |
| HD 62509 | 6 |
| L 98-59 | 6 |
| LHS 1140 | 6 |
| LTT 1445 A | 6 |

## Methodology

- Bibliography entries deduplicated by (ADS bibcode | DOI | normalized title)
- Phase 3 includes the 6 newly-added planets + d pilot
- Phase 2 set is across all curated systems
- A single paper that informs both Phase 2 and Phase 3 counts once
- Conference abstracts without arXiv preprints are included (they still
  cite real research)

## Suggested promotional copy

> NearStars-DB curates **149 stellar systems within 100 ly**, cross-referenced
> against **557+ scientific papers** — including JWST atmosphere observations,
> N-body resonance analyses, and 3D climate models — to drive a faithful
> KSP Kopernicus + Principia mod.

Or shorter:

> 149 systems. 557 paper references. 7 fully synthesized Phase 3 worlds.

## Related

- [system-trappist-1 entity pages](../../docs/phase3/trappist-1-e.md) — parent topic this workspace contributes to
