<!-- Phase 3 디스크색 결정 운영 포인터 — 방법론·인용은 docs/reference로 위임, curator 실행 단계만 -->
# Debris-disk color synthesis (operational pointer)

The full method, the white-balance convention, the validation, and the
**ADS-verified annotated bibliography** now live in the reference doc:

> **`docs/reference/debris-disk-color-methodology.md`** (+ `ko/` mirror)

Read that for the physics (Mie `Q_sca(λ)`, grain-size integral, blowout-size
floor, per-composition optical constants, CIE→sRGB reusing the atmosphere doc's
colorimetry engine and the refractiveindex.info portal). This note keeps only the
curator's operational steps.

## Operational steps

1. **Tool:** `scripts/phase3/disk_color_mie.py`. The per-belt grain size /
   composition / source citations live as comments in its `BELTS` table; those
   are consolidated into the reference doc §8.
2. **Emit BOTH variants** (Sol-Configs model), same hue, different chroma:
   - **faithful** — `SAT_FAITHFUL = 0.82` (muted, physically honest).
   - **vivid** — `SAT_VIVID = 2.6` (saturation-boosted for visual appeal).
   The cfg writer offers both packs; the user picks.
3. **Validate before committing** — use `band_ratio()` (B/I) against a measured
   analog. The synthesis is calibrated on AU Mic (blue, Krist 2005, B/I≈1.74 vs
   ~1.6) and Fomalhaut (neutral, Kalas 2005, B/I≈0.87 vs ~1.0).
4. **Measure, don't synthesize, for imaged belts** — if the belt has a resolved
   scattered-light color (Fomalhaut main = Kalas 2005, AU Mic = Krist 2005), use
   the MEASURED color. Synthesize only for thermal/mm-only belts, and flag
   `confidence: low` in the host's Phase 3 Open items.
5. **DB:** `db/disks_curated.json` stores geometry only — the tint provenance is
   in the tool / Phase 3 report, not `meta_notes` (JSON round-trip was not clean).
   See [[project-nearstars-ring-fabrication]].
